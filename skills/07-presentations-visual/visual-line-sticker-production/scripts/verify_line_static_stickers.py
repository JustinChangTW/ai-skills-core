#!/usr/bin/env python3
"""Verify a prepared static LINE sticker folder and optionally build its upload ZIP."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

try:
    from PIL import Image
except ImportError as error:
    raise SystemExit("Pillow is required: python3 -m pip install pillow") from error

VALID_COUNTS = {8, 16, 24, 32, 40}
MAX_IMAGE_BYTES = 1_000_000
MAX_ZIP_BYTES = 60_000_000
TEXT_LIMITS = {"creator": 50, "title": 40, "description": 160, "copyright": 50}


def conservative_line_units(value: str) -> int:
    """Count ASCII as 1 and all other Unicode code points as 2, conservatively."""
    return sum(1 if ord(character) < 128 else 2 for character in value)


def inspect_png(path: Path, max_size: tuple[int, int] | None, exact_size: tuple[int, int] | None) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"Missing {path.name}"]
    if path.suffix.lower() != ".png":
        return [f"{path.name} is not a PNG"]
    if path.stat().st_size > MAX_IMAGE_BYTES:
        errors.append(f"{path.name} exceeds 1 MB")
    try:
        with Image.open(path) as image:
            image.load()
            width, height = image.size
            if image.mode != "RGBA":
                errors.append(f"{path.name} must be RGBA PNG, got {image.mode}")
            if exact_size and (width, height) != exact_size:
                errors.append(f"{path.name} must be {exact_size[0]}x{exact_size[1]}, got {width}x{height}")
            if max_size and (width > max_size[0] or height > max_size[1]):
                errors.append(f"{path.name} exceeds {max_size[0]}x{max_size[1]}")
            if width % 2 or height % 2:
                errors.append(f"{path.name} has an odd width or height")
            alpha = image.getchannel("A") if "A" in image.getbands() else None
            if alpha is None or alpha.getextrema()[0] != 0:
                errors.append(f"{path.name} does not have a transparent background")
            elif (bbox := alpha.getbbox()):
                left, top, right, bottom = bbox
                if min(left, top, width - right, height - bottom) < 10:
                    errors.append(f"{path.name} has less than 10 px transparent safety margin")
            else:
                errors.append(f"{path.name} contains no visible artwork")
            dpi = image.info.get("dpi")
            if dpi and (dpi[0] < 71.5 or dpi[1] < 71.5):
                errors.append(f"{path.name} DPI is below 72")
    except OSError as error:
        errors.append(f"{path.name} cannot be read: {error}")
    return errors


def load_manifest(path: Path) -> tuple[dict, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except (OSError, json.JSONDecodeError) as error:
        return {}, [f"Cannot read manifest: {error}"]


def inspect_manifest(manifest: dict) -> list[str]:
    errors: list[str] = []
    product = manifest.get("product")
    if not isinstance(product, dict):
        return ["Manifest needs a product object"]
    for field, limit in TEXT_LIMITS.items():
        value = product.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"Manifest product.{field} is required")
        elif conservative_line_units(value) > limit:
            errors.append(f"Manifest product.{field} exceeds {limit} conservative LINE units")
    count = manifest.get("sticker_count")
    if count not in VALID_COUNTS:
        errors.append("Manifest sticker_count must be one of 8, 16, 24, 32, 40")
    stickers = manifest.get("stickers")
    if not isinstance(stickers, list) or len(stickers) != count:
        errors.append("Manifest stickers must contain exactly sticker_count rows")
    if manifest.get("rights_confirmed") is not True:
        errors.append("Manifest rights_confirmed must be true before packaging")
    return errors


def build_zip(input_dir: Path, destination: Path) -> None:
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(input_dir.glob("*.png")):
            archive.write(path, arcname=path.name)
    if destination.stat().st_size > MAX_ZIP_BYTES:
        raise ValueError("Upload ZIP exceeds 60 MB")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--zip-out", type=Path)
    args = parser.parse_args()

    manifest, errors = load_manifest(args.manifest)
    errors.extend(inspect_manifest(manifest))
    count = manifest.get("sticker_count") if isinstance(manifest, dict) else None
    if count in VALID_COUNTS:
        for index in range(1, count + 1):
            errors.extend(inspect_png(args.input_dir / f"{index:02d}.png", (370, 320), None))
    errors.extend(inspect_png(args.input_dir / "main.png", None, (240, 240)))
    errors.extend(inspect_png(args.input_dir / "tab.png", None, (96, 74)))

    report = {"valid": not errors, "errors": errors, "input_dir": str(args.input_dir), "manifest": str(args.manifest)}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if errors:
        print("Validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    if args.zip_out:
        args.zip_out.parent.mkdir(parents=True, exist_ok=True)
        try:
            build_zip(args.input_dir, args.zip_out)
        except ValueError as error:
            print(error)
            return 1
    print(f"Validation passed. Report: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
