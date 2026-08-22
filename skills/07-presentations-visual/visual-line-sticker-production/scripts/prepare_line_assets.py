#!/usr/bin/env python3
"""Normalize visually approved transparent PNGs for a static LINE sticker upload.

This script never draws, erases, or alters artwork. It crops to existing nontransparent
content, scales proportionally, and centers it on the required transparent canvas.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as error:
    raise SystemExit("Pillow is required: python3 -m pip install pillow") from error

STICKER_SIZE = (370, 320)
MAIN_SIZE = (240, 240)
TAB_SIZE = (96, 74)
MARGIN = 10
VALID_COUNTS = {8, 16, 24, 32, 40}


def source_has_transparency(image: Image.Image) -> bool:
    return "A" in image.getbands() and image.getchannel("A").getextrema()[0] == 0


def prepare(source: Path, destination: Path, size: tuple[int, int], margin: int) -> None:
    with Image.open(source) as raw:
        image = raw.convert("RGBA")
    if not source_has_transparency(image):
        raise ValueError(f"{source.name}: needs a genuinely transparent background")
    bbox = image.getchannel("A").getbbox()
    if not bbox:
        raise ValueError(f"{source.name}: has no visible content")
    content = image.crop(bbox)
    max_width = max(1, size[0] - 2 * margin)
    max_height = max(1, size[1] - 2 * margin)
    scale = min(max_width / content.width, max_height / content.height)
    scaled_size = (max(1, round(content.width * scale)), max(1, round(content.height * scale)))
    content = content.resize(scaled_size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    position = ((size[0] - content.width) // 2, (size[1] - content.height) // 2)
    canvas.alpha_composite(content, position)
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, "PNG", optimize=True, dpi=(72, 72))
    if destination.stat().st_size > 1_000_000:
        raise ValueError(f"{destination.name}: exceeds LINE's 1 MB image limit after preparation")


def collect_stickers(stickers_dir: Path) -> list[Path]:
    return sorted(path for path in stickers_dir.iterdir() if path.is_file() and path.suffix.lower() == ".png")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stickers-dir", type=Path, required=True)
    parser.add_argument("--main", type=Path, required=True)
    parser.add_argument("--tab", type=Path, required=True)
    parser.add_argument("--count", type=int, required=True, choices=sorted(VALID_COUNTS))
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    stickers = collect_stickers(args.stickers_dir)
    if len(stickers) != args.count:
        raise SystemExit(f"Expected {args.count} PNG sticker sources, found {len(stickers)}")

    try:
        for index, source in enumerate(stickers, start=1):
            prepare(source, args.out_dir / f"{index:02d}.png", STICKER_SIZE, MARGIN)
        prepare(args.main, args.out_dir / "main.png", MAIN_SIZE, MARGIN)
        prepare(args.tab, args.out_dir / "tab.png", TAB_SIZE, MARGIN)
    except ValueError as error:
        raise SystemExit(str(error)) from error

    print(f"Prepared {args.count} stickers, main.png, and tab.png in {args.out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
