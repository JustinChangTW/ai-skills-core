from __future__ import annotations

import ast
import builtins
import contextlib
import io
import re
import textwrap
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple


REPL_BLOCK_RE = re.compile(
    r"```(?P<lang>[a-zA-Z0-9_+-]*)\n(?P<code>.*?)\n```",
    re.DOTALL,
)


@dataclass
class ReplResult:
    code: str
    stdout: str
    error: Optional[str] = None


# Default expanded builtins. Adds __import__ + a few exception/utility
# names that RLM-emitted code commonly relies on. Keeping this list in
# one place makes it easy to audit what the REPL can do.
_DEFAULT_ALLOWED_BUILTINS: Dict[str, Any] = {
    name: getattr(builtins, name)
    for name in (
        "print", "len", "range", "enumerate", "min", "max", "sum", "sorted",
        "list", "dict", "set", "tuple", "str", "int", "float", "bool", "abs",
        "any", "all", "zip", "map", "filter", "isinstance", "type", "repr",
        "round", "iter", "next", "reversed", "ValueError", "TypeError",
        "KeyError", "IndexError", "Exception",
        "__import__",  # required for `import re`, `import json`, etc.
    )
    if hasattr(builtins, name)
}
_DEFAULT_ALLOWED_BUILTINS["re"] = __import__("re")
_DEFAULT_ALLOWED_BUILTINS["math"] = __import__("math")
_DEFAULT_ALLOWED_BUILTINS["json"] = __import__("json")
_DEFAULT_ALLOWED_BUILTINS["textwrap"] = __import__("textwrap")


class ReplSession:
    """A lightweight persistent Python REPL session.

    Notes:
    - This is *not* a hardened sandbox. For real deployments, run this in a
      container / seccomp jail / separate process with timeouts.
    - In this skill we use it as the execution substrate for RLM-style context
      interaction.
    - `exec()` auto-displays the value of a trailing bare expression, similar
      to a Jupyter cell. This prevents the common LLM failure mode where the
      model writes `find_chapter("X")` (no print) and gets empty stdout.
    """

    def __init__(
        self,
        initial_globals: Optional[Dict[str, Any]] = None,
        allowed_builtins: Optional[Dict[str, Any]] = None,
        max_stdout_chars: int = 8_000,
        *,
        output_max_chars: Optional[int] = None,  # alias for max_stdout_chars
    ):
        # Tolerate older callers that pass `output_max_chars`.
        if output_max_chars is not None:
            max_stdout_chars = output_max_chars

        self.globals: Dict[str, Any] = dict(initial_globals or {})
        if allowed_builtins is None:
            allowed_builtins = dict(_DEFAULT_ALLOWED_BUILTINS)
        self.globals["__builtins__"] = allowed_builtins
        self.max_stdout_chars = max_stdout_chars

    # ----- inspection helpers -----

    def inject(self, name: str, value: Any) -> None:
        """Add or overwrite a name in the REPL globals.

        Equivalent to `repl.globals[name] = value` but explicit.
        Required by RecursiveLanguageModel.run() to seed `context`,
        `llm_query`, etc.
        """
        self.globals[name] = value

    def inject_many(self, items: Dict[str, Any]) -> None:
        """Inject multiple names at once."""
        for name, value in items.items():
            self.inject(name, value)

    def get(self, name: str, default: Any = None) -> Any:
        """Read a value from REPL globals; returns `default` if not present."""
        return self.globals.get(name, default)

    def has(self, name: str) -> bool:
        return name in self.globals

    def snapshot(self, *, max_items: int = 30) -> str:
        """Return a brief variable listing to help the root model orient."""
        keys = [k for k in self.globals.keys() if not k.startswith("__")]
        keys = sorted(keys)
        shown = keys[:max_items]
        extra = "" if len(keys) <= max_items else f" (+{len(keys)-max_items} more)"
        return ", ".join(shown) + extra

    def locals_preview(self, *, max_items: int = 25, max_value_chars: int = 200) -> str:
        """Return `name = repr(value)` lines for the most relevant globals.

        Skips dunder names. Trims long reprs. Used by the RLM loop to give
        the root model a compact view of what it has built up.
        """
        keys = sorted(k for k in self.globals.keys() if not k.startswith("__"))
        out: List[str] = []
        for k in keys[:max_items]:
            try:
                preview = repr(self.globals[k])
            except Exception as e:  # noqa: BLE001 — repr can fail
                preview = f"<repr error: {e}>"
            if len(preview) > max_value_chars:
                preview = preview[:max_value_chars] + "..."
            out.append(f"{k} = {preview}")
        if len(keys) > max_items:
            out.append(f"... and {len(keys) - max_items} more")
        return "\n".join(out)

    # ----- execution -----

    def exec(self, code: str) -> ReplResult:
        """Execute code; auto-display trailing bare expression like Jupyter.

        Why: plain `exec()` discards expression results. Models often write
        `find_chapter("X")` expecting it to print, see empty stdout, and
        conclude "nothing found". Auto-display fixes this.
        """
        # Try to rewrite the AST so a trailing Expr stmt prints its value.
        # Fallback to plain exec on parse failure (e.g. partial code).
        try:
            tree = ast.parse(code)
            if tree.body and isinstance(tree.body[-1], ast.Expr):
                last = tree.body[-1]
                # Don't re-wrap explicit print/display calls.
                explicit_call = (
                    isinstance(last.value, ast.Call)
                    and (
                        getattr(last.value.func, "id", None) in {"print", "pprint", "display"}
                        or getattr(last.value.func, "attr", None) == "print"
                    )
                )
                if not explicit_call:
                    sentinel = "__autodisplay_result__"
                    assign = ast.Assign(
                        targets=[ast.Name(id=sentinel, ctx=ast.Store())],
                        value=last.value,
                    )
                    ast.copy_location(assign, last)
                    tree.body[-1] = assign
                    ast.fix_missing_locations(tree)
                    rewritten = ast.unparse(tree)
                    rewritten += (
                        f"\nif {sentinel} is not None:\n"
                        f"    try:\n"
                        f"        print(repr({sentinel})[:4000])\n"
                        f"    except Exception:\n"
                        f"        pass\n"
                    )
                    code = rewritten
        except SyntaxError:
            # Leave code unchanged; the exec() below will surface the SyntaxError.
            pass

        buf = io.StringIO()
        err: Optional[str] = None
        with contextlib.redirect_stdout(buf):
            try:
                exec(code, self.globals, self.globals)
            except Exception as e:  # noqa: BLE001
                err = f"{type(e).__name__}: {e}"
        out = buf.getvalue()
        if len(out) > self.max_stdout_chars:
            out = out[: self.max_stdout_chars] + "\n... [stdout truncated]"
        return ReplResult(code=code, stdout=out, error=err)


def extract_repl_blocks(text: str, *, allowed_langs: Tuple[str, ...] = ("repl", "python")) -> List[str]:
    """Extract fenced code blocks from an LLM message.

    By default, only blocks labelled ```repl or ```python are executed.
    """
    blocks: List[str] = []
    for m in REPL_BLOCK_RE.finditer(text):
        lang = (m.group("lang") or "").strip().lower()
        code = m.group("code")
        if lang in allowed_langs:
            blocks.append(textwrap.dedent(code).strip() + "\n")
    return blocks


def extract_code_blocks(text: str, *, langs: Optional[Iterable[str]] = None) -> List[str]:
    """Backward-compatible wrapper around `extract_repl_blocks`.

    Older code paths in this skill (and external code that adopted the
    earlier API name) call `extract_code_blocks(text, langs={"repl","python"})`.
    Newer code paths use `extract_repl_blocks(text, allowed_langs=(...))`.
    Keep both pointing at one implementation to avoid drift.
    """
    if langs is None:
        return extract_repl_blocks(text)
    return extract_repl_blocks(text, allowed_langs=tuple(langs))


FINAL_RE = re.compile(r"\bFINAL\((?P<content>.*?)\)\s*$", re.DOTALL)
FINAL_VAR_RE = re.compile(r"\bFINAL_VAR\((?P<var>[a-zA-Z_][a-zA-Z0-9_]*)\)\s*$", re.DOTALL)


@dataclass
class FinalAnswer:
    kind: str  # "text" or "var"
    value: str


def parse_final_answer(text: str) -> Optional[FinalAnswer]:
    """Parse FINAL(...) or FINAL_VAR(name) from a model message.

    We intentionally require it to appear near the end to avoid accidental matches.
    """
    t = text.strip()
    m = FINAL_VAR_RE.search(t)
    if m:
        return FinalAnswer(kind="var", value=m.group("var").strip())
    m = FINAL_RE.search(t)
    if m:
        # Strip matching surrounding quotes if present.
        content = m.group("content").strip()
        if (content.startswith('"') and content.endswith('"')) or (
            content.startswith("'") and content.endswith("'")
        ):
            content = content[1:-1]
        return FinalAnswer(kind="text", value=content)
    return None
