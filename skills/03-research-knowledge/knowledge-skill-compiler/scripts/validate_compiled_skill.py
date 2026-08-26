#!/usr/bin/env python3
"""Validate the minimum structure and safety of a compiled knowledge Skill."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FORBIDDEN_EXTENSIONS = {".pdf", ".epub", ".docx", ".mobi", ".azw", ".azw3"}
SECRET_PATTERNS = [
    re.compile(r"github_pat_[A-Za-z0-9_]{30,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{32,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.candidate.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    for required in ["SKILL.md", "knowledge/index.md", "provenance.json"]:
        if not (root / required).is_file():
            errors.append(f"missing required file: {required}")

    knowledge_files = list((root / "knowledge").rglob("*.md")) if (root / "knowledge").is_dir() else []
    if len(knowledge_files) < 2:
        errors.append("knowledge/ must contain index.md and at least one knowledge file")

    for path in root.rglob("*") if root.exists() else []:
        if path.is_symlink():
            errors.append(f"symlink not allowed: {path.relative_to(root)}")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_EXTENSIONS:
            errors.append(f"source document must not be packaged: {path.relative_to(root)}")
        if path.is_file() and path.stat().st_size <= 2_000_000:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    errors.append(f"possible secret: {path.relative_to(root)}")
                    break

    provenance = root / "provenance.json"
    if provenance.is_file():
        try:
            data = json.loads(provenance.read_text(encoding="utf-8"))
            for key in ["schema_version", "skill_name", "privacy", "generated_at", "sources"]:
                if not data.get(key):
                    errors.append(f"provenance missing field: {key}")
            if data.get("privacy") not in {"private-personal", "internal-authorized", "public-authorized"}:
                errors.append("provenance privacy has unsupported value")
            if not isinstance(data.get("sources"), list) or not data.get("sources"):
                errors.append("provenance sources must be a non-empty list")
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"invalid provenance.json: {exc}")

    result = {"status": "PASS" if not errors else "FAIL", "errors": errors, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result["status"])
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

