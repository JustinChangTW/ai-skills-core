#!/usr/bin/env python3
"""Convert JSON subtitle cues to SRT after strict validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def timestamp(seconds: float) -> str:
    if seconds < 0:
        raise ValueError("timestamp cannot be negative")
    total_ms = round(seconds * 1000)
    hours, rem = divmod(total_ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, millis = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--allow-overlap", action="store_true")
    args = parser.parse_args()

    cues = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(cues, list) or not cues:
        parser.error("input must be a non-empty JSON array")

    blocks: list[str] = []
    previous_end = 0.0
    for index, cue in enumerate(cues, 1):
        start = float(cue["start"])
        end = float(cue["end"])
        text = str(cue["text"]).strip()
        if start < 0 or end <= start:
            parser.error(f"invalid timing at cue {index}")
        if not args.allow_overlap and start < previous_end:
            parser.error(f"overlap at cue {index}")
        if not text:
            parser.error(f"empty text at cue {index}")
        blocks.append(
            f"{index}\n{timestamp(start)} --> {timestamp(end)}\n{text.replace(chr(13), '').strip()}"
        )
        previous_end = max(previous_end, end)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

