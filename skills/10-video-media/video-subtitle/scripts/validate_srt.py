#!/usr/bin/env python3
"""Validate common SRT structure and timing mistakes."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TIMING = re.compile(
    r"^(?P<sh>\d{2}):(?P<sm>\d{2}):(?P<ss>\d{2}),(?P<sms>\d{3})"
    r" --> "
    r"(?P<eh>\d{2}):(?P<em>\d{2}):(?P<es>\d{2}),(?P<ems>\d{3})$"
)


def to_ms(match: re.Match[str], prefix: str) -> int:
    return (
        int(match[f"{prefix}h"]) * 3_600_000
        + int(match[f"{prefix}m"]) * 60_000
        + int(match[f"{prefix}s"]) * 1000
        + int(match[f"{prefix}ms"])
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--allow-overlap", action="store_true")
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8-sig").replace("\r\n", "\n").strip()
    blocks = re.split(r"\n{2,}", text)
    errors: list[str] = []
    previous_end = 0
    for expected, block in enumerate(blocks, 1):
        lines = block.splitlines()
        if len(lines) < 3:
            errors.append(f"cue {expected}: expected number, timing, and text")
            continue
        if lines[0].strip() != str(expected):
            errors.append(f"cue {expected}: sequence is {lines[0].strip()!r}")
        match = TIMING.match(lines[1].strip())
        if not match:
            errors.append(f"cue {expected}: invalid timing syntax")
            continue
        start, end = to_ms(match, "s"), to_ms(match, "e")
        if end <= start:
            errors.append(f"cue {expected}: end must be after start")
        if not args.allow_overlap and start < previous_end:
            errors.append(f"cue {expected}: overlaps previous cue")
        if not any(line.strip() for line in lines[2:]):
            errors.append(f"cue {expected}: empty text")
        previous_end = max(previous_end, end)

    if errors:
        print("\n".join(errors))
        return 2
    print(f"valid SRT: {len(blocks)} cues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

