#!/usr/bin/env python3
"""Audit a categorized Agent Skills backup before or after publication."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


SECRET_PATTERNS = {
    "AWS access key": re.compile(rb"AKIA[0-9A-Z]{16}"),
    "GitHub token": re.compile(rb"(?:github_pat_[A-Za-z0-9_]{50,}|gh[pousr]_[A-Za-z0-9]{30,})"),
    "OpenAI API key": re.compile(rb"sk-[A-Za-z0-9_-]{32,}"),
    "private key": re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}
SENSITIVE_NAMES = re.compile(r"(?:^|/)(?:\.env(?:\..*)?|.*credentials.*|.*secret.*|.*\.pem|.*\.key)$", re.I)
CATEGORY_NAME = re.compile(r"^\d{2}-[a-z0-9-]+$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tracked_files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts and path.name != "SHA256SUMS.txt"
    )


def write_manifest(root: Path, files: list[Path]) -> None:
    lines = [f"{sha256(path)}  ./{path.relative_to(root).as_posix()}" for path in files]
    (root / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def verify_manifest(root: Path, files: list[Path], errors: list[str]) -> None:
    manifest = root / "SHA256SUMS.txt"
    if not manifest.is_file():
        errors.append("missing SHA256SUMS.txt")
        return
    expected = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^([0-9a-f]{64})  \./(.+)$", line)
        if not match:
            errors.append(f"invalid checksum line: {line[:80]}")
            continue
        expected[match.group(2)] = match.group(1)
    actual_names = {path.relative_to(root).as_posix() for path in files}
    if set(expected) != actual_names:
        missing = sorted(actual_names - set(expected))
        stale = sorted(set(expected) - actual_names)
        if missing:
            errors.append(f"manifest missing {len(missing)} file(s): {missing[:5]}")
        if stale:
            errors.append(f"manifest has {len(stale)} stale file(s): {stale[:5]}")
    for path in files:
        relative = path.relative_to(root).as_posix()
        if relative in expected and sha256(path) != expected[relative]:
            errors.append(f"checksum mismatch: {relative}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path, help="Skills backup repository root")
    parser.add_argument("--write-manifest", action="store_true", help="Regenerate SHA256SUMS.txt")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()
    root = args.repo.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not (root / "skills").is_dir():
        errors.append("missing skills/ directory")
        categories = []
    else:
        categories = sorted(path for path in (root / "skills").iterdir() if path.is_dir())

    skill_dirs: list[Path] = []
    seen_names: dict[str, Path] = {}
    for category in categories:
        if not CATEGORY_NAME.fullmatch(category.name):
            warnings.append(f"non-standard category name: {category.name}")
        if not (category / "README.md").is_file():
            errors.append(f"missing category README: {category.relative_to(root)}")
        for folder in sorted(path for path in category.iterdir() if path.is_dir()):
            skill_file = folder / "SKILL.md"
            if not skill_file.is_file():
                continue
            skill_dirs.append(folder)
            if not (folder / "README.md").is_file():
                errors.append(f"missing skill README: {folder.relative_to(root)}")
            text = skill_file.read_text(encoding="utf-8", errors="replace")
            match = re.search(r"^name:\s*['\"]?([^'\"\n]+)", text, re.M)
            if not match:
                errors.append(f"missing frontmatter name: {skill_file.relative_to(root)}")
                continue
            name = match.group(1).strip()
            if name != folder.name:
                errors.append(f"name/folder mismatch: {name} != {folder.name}")
            if name in seen_names:
                errors.append(f"duplicate skill name: {name}")
            seen_names[name] = folder

    for path in root.rglob("*"):
        if ".git" in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            errors.append(f"symlink not allowed in backup: {relative}")
        if path.is_file() and SENSITIVE_NAMES.search(relative):
            errors.append(f"sensitive filename: {relative}")

    files = tracked_files(root)
    for path in files:
        data = path.read_bytes()
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(data):
                errors.append(f"possible {label}: {path.relative_to(root)}")

    if args.write_manifest and not errors:
        write_manifest(root, files)
    verify_manifest(root, files, errors)

    result = {
        "status": "PASS" if not errors else "FAIL",
        "repo": str(root),
        "categories": len(categories),
        "skills": len(skill_dirs),
        "files_excluding_manifest": len(files),
        "errors": errors,
        "warnings": warnings,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['status']}: {len(categories)} categories, {len(skill_dirs)} skills, {len(files)} files")
        for item in errors:
            print(f"ERROR: {item}")
        for item in warnings:
            print(f"WARNING: {item}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
