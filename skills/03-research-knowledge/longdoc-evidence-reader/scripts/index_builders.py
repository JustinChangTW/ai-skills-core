"""Optional pre-built indexes that caller can inject into the RLM REPL.

These are generic, content-agnostic helpers. They do **not** hard-code
anything about a specific PDF. For best-effort heuristics that don't
parse cleanly on every PDF (especially the chapter detectors), the
docstrings note the failure modes.

Typical usage from caller:

    chunks = load_pdf_as_chunks(pdf_path, chunk_by="page").chunks
    numeric_index = build_numeric_index(chunks)
    chapter_index = build_chapter_index_from_headings(chunks)
    helpers = make_repl_helpers(
        chunks,
        chapter_index=chapter_index,
        numeric_index=numeric_index,
    )

    extra_globals = {
        "chapter_index": chapter_index,
        "numeric_index": numeric_index,
        **helpers,
    }
    rlm.run(query, context, extra_globals=extra_globals)

The runner will inject these names into the REPL and (if supplied) append
a documentation block to the system prompt so the root model knows they
exist.
"""

from __future__ import annotations

import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from context_store import Chunk


# ----- numeric index -------------------------------------------------------

# `<value><unit>` pairs that show up in research-style PDFs.
# Add more domain-specific units (e.g., "qubits", "FLOPS") if your source
# warrants. Keep matches conservative — false positives bloat the index.
_NUM_PATTERN = re.compile(
    r"(?P<value>\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)\s*"
    r"(?P<unit>%|percent|billion|million|trillion|thousand|"
    r"\bB\b|\bM\b|\bK\b|tons?|tonnes?|MtCO2e?|tCO2e?|"
    r"GW|MW|kW|kWh|TWh|GWh|"
    r"models?|incidents?|cases?|countries|companies|clusters?|"
    r"\$\d|USD)",
    re.IGNORECASE,
)

_DOLLAR_PATTERN = re.compile(
    r"\$\s*(?P<value>\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*"
    r"(?P<unit>billion|million|trillion|B\b|M\b|K\b)?",
    re.IGNORECASE,
)


def _page_from_source(source: str) -> int:
    """Extract page number from a Chunk source label like `pdf:foo.pdf#page=42`.

    Returns -1 if no page marker.
    """
    m = re.search(r"#page=?(\d+)", source)
    return int(m.group(1)) if m else -1


def build_numeric_index(
    chunks: Sequence[Chunk],
    *,
    window: int = 60,
) -> List[Dict[str, Any]]:
    """Regex-extract numeric facts with surrounding context for each chunk.

    Each entry is a dict:
        {
            "chunk_idx": int,
            "page": int,         # -1 if not page-tagged
            "value": str,        # raw numeric token from the text
            "unit": str,         # e.g. "%", "billion", "tons"
            "snippet": str,      # ±`window` chars around the match
        }

    Notes:
    - Only catches numbers immediately followed by a recognized unit. A
      bare "5,427" with no unit on either side will NOT appear here.
    - Use `find_numbers(keyword)` to filter by keyword in snippet.
    - For non-research PDFs, you may want to extend `_NUM_PATTERN`.
    """
    out: List[Dict[str, Any]] = []
    for ci, ch in enumerate(chunks):
        page = _page_from_source(ch.source)
        text = ch.text
        for m in _NUM_PATTERN.finditer(text):
            start = max(m.start() - window, 0)
            end = min(m.end() + window, len(text))
            snippet = text[start:end].replace("\n", " ").strip()
            out.append({
                "chunk_idx": ci,
                "page": page,
                "value": m.group("value"),
                "unit": m.group("unit").strip(),
                "snippet": snippet,
            })
        for m in _DOLLAR_PATTERN.finditer(text):
            start = max(m.start() - window, 0)
            end = min(m.end() + window, len(text))
            snippet = text[start:end].replace("\n", " ").strip()
            out.append({
                "chunk_idx": ci,
                "page": page,
                "value": "$" + m.group("value"),
                "unit": (m.group("unit") or "").strip(),
                "snippet": snippet,
            })
    return out


# ----- chapter index -------------------------------------------------------

# Default heading regex. Matches "Chapter 3: Title", "CHAPTER 3 - Title",
# "Section 3.2 Title", etc. Tweak for your source format.
_DEFAULT_HEADING_PATTERN = re.compile(
    r"\b(?:Chapter|CHAPTER|Section|SECTION)\s+"
    r"(?P<num>\d+(?:\.\d+)?)\s*[:\-–\s]+\s*"
    r"(?P<title>[A-Z][A-Za-z0-9 ,&'\-]{3,80})",
)


def build_chapter_index_from_headings(
    chunks: Sequence[Chunk],
    *,
    pattern: Optional[re.Pattern] = None,
    max_entries_per_chunk: int = 3,
) -> Dict[str, Dict[str, int]]:
    """Scan all chunks for chapter-heading patterns; build a chapter→page map.

    Returns a dict of `{chapter_name: {"start_page": int, "end_page": int}}`.
    `end_page` is the page just before the next chapter starts (or the last
    page for the final chapter).

    Failure modes (best-effort, not always correct):
    - Multi-column PDFs where pypdf interleaves chapter titles into body text.
    - Documents that don't use the word "Chapter" (e.g. legal codes, papers).
    - Headings split across page breaks.

    For high-stakes routing, prefer `build_chapter_index_from_toc()` which
    parses a TOC page, or hand-curate the dict.
    """
    rx = pattern or _DEFAULT_HEADING_PATTERN

    # Collect first appearance of each (num, title) tuple.
    # Use insertion order to preserve document flow.
    seen: Dict[str, int] = {}  # chapter_label -> start_page
    for ci, ch in enumerate(chunks):
        page = _page_from_source(ch.source)
        if page < 0:
            continue
        local_count = 0
        for m in rx.finditer(ch.text):
            num = m.group("num").strip()
            title = m.group("title").strip()
            label = f"Chapter {num}: {title}"
            if label not in seen:
                seen[label] = page
            local_count += 1
            if local_count >= max_entries_per_chunk:
                break

    if not seen:
        return {}

    # Resolve end_page from successor's start_page - 1.
    items = list(seen.items())  # preserves insertion order in Python 3.7+
    last_page = max(_page_from_source(c.source) for c in chunks)
    out: Dict[str, Dict[str, int]] = {}
    for i, (label, start) in enumerate(items):
        end = (items[i + 1][1] - 1) if i + 1 < len(items) else last_page
        out[label] = {"start_page": start, "end_page": end}
    return out


# Match a TOC line like "Chapter 3 Responsible AI ... 126" or
# "3 Responsible AI 126". Tolerates dot-leaders and varied whitespace.
_TOC_ENTRY_RE = re.compile(
    r"(?:Chapter\s+)?(?P<num>\d+)\s+"
    r"(?P<title>[A-Za-z][A-Za-z0-9 ,&'\-]{3,60}?)"
    r"\s*\.{0,}\s*(?P<page>\d{1,4})\b",
)


def build_chapter_index_from_toc(
    chunks: Sequence[Chunk],
    *,
    scan_pages: int = 10,
) -> Dict[str, Dict[str, int]]:
    """Try to parse a Table-of-Contents page and build chapter→page map.

    Scans the first `scan_pages` chunks for a TOC-like layout. Falls back
    to an empty dict if no TOC entries can be confidently parsed.

    Failure modes:
    - TOC is rendered as an image (pypdf returns nothing useful).
    - Numbers in TOC don't map 1:1 to actual page positions (some books
      restart numbering for the front matter).
    - TOC uses non-standard delimiters (e.g., tab characters that pypdf
      collapses).

    For high-stakes routing, prefer hand-curating the dict.
    """
    candidates: List[Dict[str, Any]] = []
    for ch in chunks[:scan_pages]:
        for m in _TOC_ENTRY_RE.finditer(ch.text):
            num = int(m.group("num"))
            title = m.group("title").strip()
            page = int(m.group("page"))
            # Sanity: page should be plausible. Reject anything > 10000.
            if 1 <= page <= 10000 and 1 <= num <= 50:
                candidates.append({"num": num, "title": title, "page": page})

    if not candidates:
        return {}

    # Deduplicate by num: keep the first plausible occurrence.
    by_num: Dict[int, Dict[str, Any]] = {}
    for c in candidates:
        if c["num"] not in by_num:
            by_num[c["num"]] = c

    items = sorted(by_num.values(), key=lambda c: c["num"])
    last_page = max(_page_from_source(c.source) for c in chunks)
    out: Dict[str, Dict[str, int]] = {}
    for i, c in enumerate(items):
        end = (items[i + 1]["page"] - 1) if i + 1 < len(items) else last_page
        label = f"Chapter {c['num']}: {c['title']}"
        out[label] = {"start_page": c["page"], "end_page": end}
    return out


# ----- helper closures -----------------------------------------------------

def make_repl_helpers(
    chunks: Sequence[Chunk],
    *,
    chapter_index: Optional[Dict[str, Dict[str, int]]] = None,
    numeric_index: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Callable]:
    """Build a dict of REPL helpers for caller to inject.

    Returns:
        {
            "find_chapter":  fn(name_substr) -> List[entry]
            "chunks_in_pages": fn(start, end) -> List[chunk_idx]
            "find_numbers":  fn(keyword, max_hits=30) -> List[entry]
            "quote_at":      fn(chunk_idx, start_char, length=300) -> str
        }

    All four are pure functions over the captured `chunks` (and the indexes
    if provided). Pass to `RLM.run(extra_globals={...})` along with the raw
    indexes themselves.
    """
    chunks_list = list(chunks)
    chapter_idx = dict(chapter_index or {})
    numeric_idx = list(numeric_index or [])

    def find_chapter(name_substr: str) -> List[Dict[str, Any]]:
        """Return chapter entries whose label contains substring (case-insensitive)."""
        s = (name_substr or "").lower()
        return [
            {"chapter": k, **v} for k, v in chapter_idx.items() if s in k.lower()
        ]

    def chunks_in_pages(start_page: int, end_page: int) -> List[int]:
        """Return chunk indices whose page is in [start_page, end_page]."""
        out: List[int] = []
        for ci, ch in enumerate(chunks_list):
            p = _page_from_source(ch.source)
            if start_page <= p <= end_page:
                out.append(ci)
        return out

    def find_numbers(keyword: str, max_hits: int = 30) -> List[Dict[str, Any]]:
        """Return numeric_index entries whose snippet contains the keyword."""
        s = (keyword or "").lower()
        if not s:
            return []
        hits = [n for n in numeric_idx if s in n["snippet"].lower()]
        return hits[:max_hits]

    def quote_at(chunk_idx: int, start_char: int = 0, length: int = 300) -> str:
        """Return a verbatim slice from a chunk for evidence quoting."""
        if chunk_idx < 0 or chunk_idx >= len(chunks_list):
            return f"<invalid chunk_idx {chunk_idx}>"
        return chunks_list[chunk_idx].text[start_char : start_char + length]

    return {
        "find_chapter": find_chapter,
        "chunks_in_pages": chunks_in_pages,
        "find_numbers": find_numbers,
        "quote_at": quote_at,
    }


def helpers_doc(
    *,
    chapter_index: Optional[Dict[str, Dict[str, int]]] = None,
    numeric_index: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """Return a system-prompt fragment describing the injected helpers.

    Caller can pass the result to `RLMConfig.extra_helpers_doc` so the
    root model knows what's available.
    """
    lines: List[str] = ["EXTRA HELPERS (already injected)"]
    if chapter_index:
        n = len(chapter_index)
        lines.append(
            f"- `chapter_index`: dict of {n} chapter -> "
            "{start_page, end_page}"
        )
        lines.append(
            "- `find_chapter(name_substr)`: filter chapters by partial name"
        )
        lines.append(
            "- `chunks_in_pages(start, end)`: list chunk indices in a page range"
        )
    if numeric_index:
        n = len(numeric_index)
        lines.append(
            f"- `numeric_index`: list of {n} pre-extracted numbers, each "
            "{value, unit, snippet, page, chunk_idx}"
        )
        lines.append(
            "- `find_numbers(keyword, max_hits=30)`: search numeric_index "
            "by substring in snippet"
        )
    if chapter_index or numeric_index:
        lines.append(
            "- `quote_at(chunk_idx, start_char, length=300)`: verbatim slice "
            "from a chunk for evidence quoting"
        )
        lines.append(
            "Use these BEFORE falling back to `context[i].text` scans — "
            "they are precomputed and much faster."
        )
        return "\n".join(lines)
    return ""
