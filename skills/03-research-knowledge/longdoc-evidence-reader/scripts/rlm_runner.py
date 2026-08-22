"""Recursive Language Model (RLM) runner over a Python REPL.

Refactored to fix several bugs and add discipline that proved necessary
for non-thinking models (reasoning_effort='none' / 'minimal'):

- Imports `extract_repl_blocks` and `parse_final_answer` from `rlm_repl`
  rather than re-defining FINAL parsing here. Single source of truth.
- Calls `context.total_chars()` / `context.chunk_lengths()` as methods
  (not attributes) — matches `ContextStore` definition.
- Forces ONE-TURN-ONE-ACTION: when an assistant message contains both a
  `repl` block AND a `FINAL(...)`, the FINAL is ignored and the model is
  pushed to wait for stdout. This prevents non-thinking models from
  emitting a premature unknown answer before seeing search results.
- Provides the new EVIDENCE-first system prompt by default.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from context_store import Chunk, ContextStore
from rlm_providers import ChatProvider, Message
from rlm_repl import (
    ReplSession,
    extract_repl_blocks,
    parse_final_answer,
)


# Default regex for the "Source: ... \"<quote>\"" tail of a FINAL answer.
# The first capture group must be the verbatim quote.
DEFAULT_CITATION_QUOTE_RE = re.compile(
    r'Source[:\s][^"\n]*"([^"]{8,})"',
    re.IGNORECASE,
)

# Phrases that mean "I don't know" — any FINAL containing one of these
# bypasses citation verification.
DEFAULT_UNKNOWN_MARKERS: Tuple[str, ...] = (
    "無法從報告中找到",
    "無法找到",
    "I don't know",
    "I cannot find",
    "Not found in the document",
)


@dataclass
class RLMConfig:
    """Controls the RLM loop."""

    root_model: str
    sub_model: Optional[str] = None
    temperature: float = 0.2
    max_steps: int = 25
    repl_output_max_chars: int = 6000
    # How much to tell the root model about the environment each step
    include_locals_preview: bool = True
    # Optional: override the system prompt entirely
    system_prompt_override: Optional[str] = None
    # Optional: appended to the default system prompt (e.g., to document
    # extra helpers injected via `extra_globals`). Ignored if
    # `system_prompt_override` is set.
    extra_helpers_doc: Optional[str] = None

    # ----- citation verification (opt-in, default ON) -----
    # When True, FINAL answers must contain a verbatim quote that exists
    # in the chunks. "I don't know" answers bypass this check.
    verify_citations: bool = True
    # Compiled or raw regex; first capture group must be the quote.
    citation_quote_pattern: Any = DEFAULT_CITATION_QUOTE_RE
    # Markers that signal a legitimate "no answer" response.
    citation_unknown_markers: Tuple[str, ...] = DEFAULT_UNKNOWN_MARKERS
    # How many times to push back and re-ask before giving up.
    max_citation_rejections: int = 2
    # When verifying, normalize whitespace and lowercase, then check
    # whether the first `citation_match_head_chars` of the quote appear
    # as a substring in any chunk. Trades exact-equality for tolerance to
    # whitespace/casing variations from pypdf.
    citation_match_head_chars: int = 60


def _normalize_for_match(text: str) -> str:
    """Whitespace-normalize and lowercase text for tolerant substring match."""
    return re.sub(r"\s+", " ", text).strip().lower()


def quote_appears_in_chunks(
    quote: str,
    chunks: Sequence[Chunk],
    *,
    head_chars: int = 60,
    min_quote_chars: int = 8,
) -> bool:
    """Return True if (a normalized prefix of) `quote` appears in any chunk.

    Public utility — exposed so callers can reuse the same matching logic
    used by `RecursiveLanguageModel` for their own validation.
    """
    if not quote or len(quote) < min_quote_chars:
        return False
    norm_q = _normalize_for_match(quote)[:head_chars]
    for ch in chunks:
        if norm_q in _normalize_for_match(ch.text):
            return True
    return False


def verify_final_citation(
    final_text: str,
    chunks: Sequence[Chunk],
    *,
    pattern: Any = DEFAULT_CITATION_QUOTE_RE,
    head_chars: int = 60,
) -> Tuple[bool, Optional[str]]:
    """Inspect a FINAL answer string; return (ok, extracted_quote).

    `ok` is True iff:
      - `pattern` matches, and
      - the captured quote (first group) appears verbatim in some chunk.

    Returns `(False, None)` if the citation block is missing entirely.
    Returns `(False, "<quote>")` if the citation is present but the quote
    cannot be found in any chunk (likely fabrication).
    """
    rx = pattern if hasattr(pattern, "search") else re.compile(pattern, re.IGNORECASE)
    m = rx.search(final_text)
    if not m:
        return False, None
    quote = m.group(1).strip()
    ok = quote_appears_in_chunks(quote, chunks, head_chars=head_chars)
    return ok, quote


def default_system_prompt(
    *,
    context_type: str,
    context_total_length: int,
    context_lengths: List[int],
    subcalls_enabled: bool,
    batch_warning: bool = True,
    extra_helpers_doc: Optional[str] = None,
) -> str:
    """Strict EVIDENCE-first system prompt for the RLM root LM.

    Differences from the paper's Appendix D template:

    1. ONE-TURN-ONE-ACTION rule.  Each assistant message does either a
       `repl` search OR a FINAL — never both. Models that mix the two
       (common with reasoning_effort='none') get their FINAL ignored.
    2. EVIDENCE-first FINAL.  FINAL must include
       `Source: pdf#pageN, "<verbatim 8-20 word quote>"`.  The runner
       (caller) is expected to verify the quote against the actual chunks
       to catch fabricated citations.
    3. "I don't know" is a valid answer.  If after focused search the
       model can't find a verbatim quote, it must emit
       `FINAL(無法從報告中找到。)` rather than guess.
    4. Drops FINAL_VAR from the surface.  It's still parsed for
       backward compatibility, but the prompt no longer recommends it —
       in practice models often write `FINAL(summary)` thinking they are
       referencing a variable, getting the literal string "summary"
       saved as the answer.
    """

    base = f"""You are answering a query against a long document loaded as `context`.
You will iterate in a Python REPL until you can produce a final answer.

ENVIRONMENT
- `context` is a {context_type}; total {context_total_length} characters.
- Chunk char lengths: {context_lengths}.
- The REPL persists state across turns. The last bare expression in a
  cell is auto-displayed (Jupyter-style), so `find_chapter("X")` prints
  its result without an explicit `print()`.
- Use `print()` to emit text you want to read in REPL_FEEDBACK.
- You will only see truncated stdout; build up answers in variables.

ANSWERING DISCIPLINE (NON-NEGOTIABLE)

1. ONE TURN = ONE ACTION.
   Each assistant message does EITHER (A) run `repl` blocks to search
   the context, OR (B) emit `FINAL(...)` with the answer. NEVER both.
   If you mix them, the runner will IGNORE your FINAL and push back the
   stdout, costing you a step.  Decide based on what stdout actually
   shows you, not on what you guess it will show.

2. EVIDENCE-FIRST FINAL.
   When you commit, format FINAL exactly like this:

       FINAL(<answer in user's language>. Source: pdf#pageN, "<verbatim 8-20 word quote>")

   The quote will be auto-verified against the chunks. Fabricated
   quotes are rejected. Copy the quote from `context[i].text` or from
   the snippet field of an index helper — do not paraphrase.

3. "I DON'T KNOW" IS A VALID ANSWER.
   If after 2-3 focused searches you cannot find a verbatim quote that
   answers the query, your FINAL must be exactly:

       FINAL(無法從報告中找到。)

   No source needed for unknown.  Hallucinated numbers or named
   benchmarks are FAR worse than honest "I don't know".

4. NO HEDGING.
   Once you have evidence, COMMIT.  Do not append qualifications like
   "but this might not be X-specific".  Either the evidence answers
   the question, or it does not.

5. SEARCH STRATEGY.
   Prefer narrow searches over reading whole chunks.  Useful starting
   moves: `ContextStore(context).find_regex(pattern, max_hits=10)` ;
   `ContextStore(context).grep_keywords([kw1, kw2])` ;
   `context[i].text[start:end]`.  Try 2-4 different search angles
   before giving up — narrative sentences ("X led with 50 models, Y
   with 30") are usually MORE useful than chart-fragment dumps.

CODE BLOCKS
Wrap Python in triple backticks with `repl`:
```repl
hits = ContextStore(context).find_regex(r"keyword[^.]+\\d+")
for h in hits[:5]:
    print(h)
```
"""

    if subcalls_enabled:
        base += """
SUB-LLM CALLS
A `llm_query(text: str) -> str` function is available; it queries a
sub-LLM that can take large input.  Use it sparingly for semantic
analysis (e.g., "summarize this 50k-char chunk") — not for fact lookup
that REPL search can do directly.
"""
        if batch_warning:
            base += """
IMPORTANT: `llm_query` is expensive. Batch related information into
each call when possible (aim ~50k–200k chars per call).  Avoid making
one `llm_query` per line.
"""

    if extra_helpers_doc:
        base += "\n" + extra_helpers_doc.strip() + "\n"

    return base.strip()


class RecursiveLanguageModel:
    """A practical RLM implementation (REPL + optional recursive subcalls).

    Loop:
      - Ask root LM for code / actions.
      - Execute any `repl` blocks inside a persistent REPL.
      - If the same message contains a FINAL, decide whether to accept
        it (no repl blocks, or it's the last step) or reject it (repl
        blocks present and budget remains) — see ONE-TURN-ONE-ACTION.
      - Otherwise feed stdout back as REPL_FEEDBACK and continue.
      - Stop when root LM emits a FINAL we accept.
    """

    def __init__(
        self,
        *,
        root: ChatProvider,
        sub: Optional[ChatProvider] = None,
        config: RLMConfig,
    ) -> None:
        self.root = root
        self.sub = sub
        self.config = config

    def run(
        self,
        query: str,
        context: ContextStore,
        *,
        extra_globals: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Run the RLM loop until a FINAL answer is accepted.

        Parameters
        ----------
        query:
            The user's natural-language question.
        context:
            The chunked document. The runner injects `context.chunks` into
            the REPL as `context`.
        extra_globals:
            Optional dict of extra names to inject into the REPL (e.g.,
            `numeric_index`, `chapter_index`, `find_chapter`, etc., as
            built by `index_builders.py`). Document them in the system
            prompt via `RLMConfig.extra_helpers_doc`.
        """
        subcalls_enabled = self.sub is not None and self.config.sub_model is not None

        # Build REPL with helpers.
        repl = ReplSession(max_stdout_chars=self.config.repl_output_max_chars)

        def llm_query(text: str, *, model: Optional[str] = None) -> str:
            if not subcalls_enabled:
                raise RuntimeError("Subcalls disabled (no sub provider / sub_model)")
            assert self.sub is not None
            use_model = model or self.config.sub_model
            assert use_model is not None
            msgs: List[Message] = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful sub-LLM. Follow the user's instructions "
                        "precisely. When asked for a fact, return only the fact "
                        "with a verbatim quote when possible."
                    ),
                },
                {"role": "user", "content": text},
            ]
            return self.sub.chat(
                msgs,
                model=use_model,
                temperature=self.config.temperature,
                max_tokens=2048,
            )

        repl.inject_many({
            "context": context.chunks,
            "ContextStore": ContextStore,
            "llm_query": llm_query,
        })
        if extra_globals:
            repl.inject_many(extra_globals)

        if self.config.system_prompt_override is not None:
            sys_prompt = self.config.system_prompt_override
        else:
            sys_prompt = default_system_prompt(
                context_type="List[Chunk]",
                context_total_length=context.total_chars(),
                context_lengths=context.chunk_lengths(),
                subcalls_enabled=subcalls_enabled,
                batch_warning=True,
                extra_helpers_doc=self.config.extra_helpers_doc,
            )

        messages: List[Message] = [
            {"role": "system", "content": sys_prompt},
            {
                "role": "user",
                "content": (
                    f"QUERY:\n{query}\n\n"
                    "Reminder: ONE TURN = ONE ACTION (search OR FINAL, never both). "
                    "FINAL must include Source citation with a verbatim 8-20 word quote."
                ),
            },
        ]

        last_repl_feedback = ""
        citation_rejection_count = 0
        for step in range(1, self.config.max_steps + 1):
            if last_repl_feedback:
                messages.append(
                    {
                        "role": "user",
                        "content": f"REPL_FEEDBACK_STEP_{step-1}:\n{last_repl_feedback}",
                    }
                )

            assistant_text = self.root.chat(
                messages,
                model=self.config.root_model,
                temperature=self.config.temperature,
                max_tokens=4096,
            )
            messages.append({"role": "assistant", "content": assistant_text})

            # Always run repl blocks first (if any), so REPL state is
            # advanced and stdout is captured before we decide on FINAL.
            blocks = extract_repl_blocks(assistant_text, allowed_langs=("repl", "python"))
            this_turn_stdout = ""
            if blocks:
                feedback_parts: List[str] = []
                for i, code in enumerate(blocks, start=1):
                    result = repl.exec(code)
                    feedback_parts.append(
                        (
                            f"[block {i}]\nCODE:\n{code}\n"
                            f"STDOUT:\n{result.stdout or ''}\n"
                            f"ERROR:\n{result.error or ''}"
                        ).strip()
                    )
                    this_turn_stdout += (result.stdout or "")
                if self.config.include_locals_preview:
                    preview = repl.locals_preview(max_items=25, max_value_chars=200)
                    feedback_parts.append(f"LOCALS_PREVIEW:\n{preview}")
                last_repl_feedback = "\n\n---\n\n".join(feedback_parts)
            else:
                last_repl_feedback = ""

            # Now consider FINAL.
            fa = parse_final_answer(assistant_text)

            # ONE-TURN-ONE-ACTION enforcement: if the model emitted both
            # a search and a FINAL in the same message, the FINAL was
            # decided BEFORE this turn's stdout existed. Reject it and
            # push back stdout, unless we're on the last allowed step
            # (in which case we accept whatever we have to avoid a
            # max_steps RuntimeError).
            if fa is not None and blocks and step < self.config.max_steps:
                last_repl_feedback = (
                    (last_repl_feedback + "\n\n---\n\n" if last_repl_feedback else "")
                    + (
                        "TURN DISCIPLINE: You emitted FINAL in the same message as "
                        "`repl` blocks. The FINAL is IGNORED because you decided it "
                        "before seeing this turn's stdout. Read the stdout above, "
                        "then on the NEXT turn either run more searches OR emit "
                        "FINAL — never both."
                    )
                )
                continue

            if fa is not None:
                if fa.kind == "var":
                    val = repl.get(fa.value)
                    if val is None:
                        # FINAL_VAR referenced an undefined name. Push back
                        # so the model can try again. Don't crash.
                        last_repl_feedback = (
                            (last_repl_feedback + "\n\n---\n\n" if last_repl_feedback else "")
                            + (
                                f"FINAL_VAR({fa.value}) referenced an undefined name. "
                                "Either define that variable in a `repl` block, or "
                                "switch to FINAL(<literal answer text>)."
                            )
                        )
                        continue
                    final_text = str(val)
                else:
                    # kind == "text"
                    final_text = fa.value

                # Citation verification (opt-in via RLMConfig).
                if (
                    self.config.verify_citations
                    and citation_rejection_count < self.config.max_citation_rejections
                ):
                    is_unknown = any(
                        marker in final_text
                        for marker in self.config.citation_unknown_markers
                    )
                    if not is_unknown:
                        ok, quote = verify_final_citation(
                            final_text,
                            context.chunks,
                            pattern=self.config.citation_quote_pattern,
                            head_chars=self.config.citation_match_head_chars,
                        )
                        if not ok:
                            citation_rejection_count += 1
                            if quote is None:
                                reason = (
                                    "missing or malformed `Source: ... \"<quote>\"` "
                                    "tail. The runner expects FINAL to contain a "
                                    "Source citation with a verbatim 8-20 word quote."
                                )
                            else:
                                reason = (
                                    f"the quoted text {quote[:80]!r} does not appear "
                                    "verbatim in any chunk. It looks fabricated. "
                                    "Re-run a `repl` search to find a real quote."
                                )
                            last_repl_feedback = (
                                (last_repl_feedback + "\n\n---\n\n" if last_repl_feedback else "")
                                + f"CITATION REJECTED: {reason} "
                                "Either correct the citation OR emit "
                                "FINAL(無法從報告中找到。) if you genuinely cannot find evidence."
                            )
                            continue

                return final_text

            # No blocks AND no FINAL — nudge the model.
            if not blocks:
                last_repl_feedback = (
                    "No `repl` code blocks and no FINAL found. Either run a "
                    "`repl` block to inspect `context`, or emit FINAL(...)."
                )

        raise RuntimeError(
            f"RLM exceeded max_steps={self.config.max_steps} without producing FINAL(...)."
        )
