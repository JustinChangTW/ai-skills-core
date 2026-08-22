#!/usr/bin/env python3
"""Validate a reviewable tutorial step plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def check_box(box: dict, label: str) -> list[str]:
    errors: list[str] = []
    for key in ("x", "y", "width", "height"):
        value = box.get(key)
        if not isinstance(value, (int, float)) or not 0 <= value <= 1:
            errors.append(f"{label}.{key} must be between 0 and 1")
    if isinstance(box.get("x"), (int, float)) and isinstance(box.get("width"), (int, float)):
        if box["x"] + box["width"] > 1:
            errors.append(f"{label} exceeds frame width")
    if isinstance(box.get("y"), (int, float)) and isinstance(box.get("height"), (int, float)):
        if box["y"] + box["height"] > 1:
            errors.append(f"{label} exceeds frame height")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    errors: list[str] = []
    steps = plan.get("steps")
    if not isinstance(steps, list) or not steps:
        errors.append("steps must be a non-empty list")
        steps = []
    last_start = -1.0
    for index, step in enumerate(steps, 1):
        start = step.get("start")
        end = step.get("end")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            errors.append(f"step {index}: start/end must be numbers")
            continue
        if start < 0 or end <= start:
            errors.append(f"step {index}: invalid timing")
        if start < last_start:
            errors.append(f"step {index}: steps are not in chronological order")
        if not str(step.get("title", "")).strip():
            errors.append(f"step {index}: title is required")
        if not str(step.get("instruction", "")).strip():
            errors.append(f"step {index}: instruction is required")
        if "focus" in step:
            errors.extend(check_box(step["focus"], f"step {index}.focus"))
        for redaction_index, redaction in enumerate(step.get("redactions", []), 1):
            errors.extend(
                check_box(redaction, f"step {index}.redactions[{redaction_index}]")
            )
        last_start = start
    if errors:
        print("\n".join(errors))
        return 2
    print(f"valid tutorial plan: {len(steps)} steps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

