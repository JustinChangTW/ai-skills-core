#!/usr/bin/env python3
"""Inspect a media file with ffprobe and emit normalized JSON."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def parse_rate(value: str | None) -> float | None:
    if not value or value in {"0/0", "N/A"}:
        return None
    if "/" in value:
        numerator, denominator = value.split("/", 1)
        if float(denominator) == 0:
            return None
        return round(float(numerator) / float(denominator), 6)
    return float(value)


def probe(path: Path) -> dict:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_streams",
        "-show_format",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    raw = json.loads(result.stdout)
    streams = raw.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    fmt = raw.get("format", {})

    rotation = 0
    if video:
        rotation = int(video.get("tags", {}).get("rotate", 0) or 0)
        for item in video.get("side_data_list", []):
            if "rotation" in item:
                rotation = int(item["rotation"])

    return {
        "path": str(path.resolve()),
        "size_bytes": path.stat().st_size,
        "duration_seconds": float(fmt["duration"]) if fmt.get("duration") else None,
        "format_name": fmt.get("format_name"),
        "video": None
        if not video
        else {
            "codec": video.get("codec_name"),
            "width": video.get("width"),
            "height": video.get("height"),
            "frame_rate": parse_rate(video.get("avg_frame_rate")),
            "pixel_format": video.get("pix_fmt"),
            "rotation": rotation,
        },
        "audio": None
        if not audio
        else {
            "codec": audio.get("codec_name"),
            "sample_rate": int(audio["sample_rate"]) if audio.get("sample_rate") else None,
            "channels": audio.get("channels"),
            "channel_layout": audio.get("channel_layout"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"input file not found: {args.input}")
    try:
        payload = probe(args.input)
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"media probe failed: {exc}", file=sys.stderr)
        return 2
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

