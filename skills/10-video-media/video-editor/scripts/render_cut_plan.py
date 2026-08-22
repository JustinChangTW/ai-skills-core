#!/usr/bin/env python3
"""Validate and render a single-source trim/reorder plan with FFmpeg."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def load_plan(path: Path) -> dict:
    plan = json.loads(path.read_text(encoding="utf-8"))
    source = Path(plan["source"]).expanduser().resolve()
    output = Path(plan["output"]).expanduser().resolve()
    if not source.is_file():
        raise ValueError(f"source does not exist: {source}")
    if source == output:
        raise ValueError("output must not overwrite source")
    segments = plan.get("segments")
    if not isinstance(segments, list) or not segments:
        raise ValueError("segments must be a non-empty list")
    normalized = []
    for index, segment in enumerate(segments):
        start = float(segment["start"])
        end = float(segment["end"])
        if start < 0 or end <= start:
            raise ValueError(f"invalid segment {index}: {start}..{end}")
        normalized.append({"start": start, "end": end})
    return {
        "source": source,
        "output": output,
        "segments": normalized,
        "crf": int(plan.get("crf", 20)),
        "preset": str(plan.get("preset", "medium")),
        "audio_bitrate": str(plan.get("audio_bitrate", "192k")),
    }


def has_audio(source: Path) -> bool:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a:0",
        "-show_entries",
        "stream=index",
        "-of",
        "csv=p=0",
        str(source),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return bool(result.stdout.strip())


def build_command(plan: dict) -> list[str]:
    audio = has_audio(plan["source"])
    filters: list[str] = []
    concat_inputs: list[str] = []
    for index, segment in enumerate(plan["segments"]):
        start = segment["start"]
        end = segment["end"]
        filters.append(
            f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[v{index}]"
        )
        concat_inputs.append(f"[v{index}]")
        if audio:
            duration = end - start
            fade = min(0.03, duration / 4)
            filters.append(
                f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS,"
                f"afade=t=in:st=0:d={fade},afade=t=out:st={max(0, duration-fade)}:d={fade}[a{index}]"
            )
            concat_inputs.append(f"[a{index}]")
    filters.append(
        "".join(concat_inputs)
        + f"concat=n={len(plan['segments'])}:v=1:a={1 if audio else 0}[vout]"
        + ("[aout]" if audio else "")
    )
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-i",
        str(plan["source"]),
        "-filter_complex",
        ";".join(filters),
        "-map",
        "[vout]",
    ]
    if audio:
        command += ["-map", "[aout]"]
    command += [
        "-c:v",
        "libx264",
        "-crf",
        str(plan["crf"]),
        "-preset",
        plan["preset"],
        "-pix_fmt",
        "yuv420p",
    ]
    if audio:
        command += ["-c:a", "aac", "-b:a", plan["audio_bitrate"]]
    command += ["-movflags", "+faststart", str(plan["output"])]
    return command


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        plan = load_plan(args.plan)
        command = build_command(plan)
    except (KeyError, ValueError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"invalid cut plan: {exc}", file=sys.stderr)
        return 2

    print(json.dumps({"command": command}, ensure_ascii=False, indent=2))
    if not args.execute:
        return 0
    if plan["output"].exists() and not args.force:
        print(f"output exists; use --force: {plan['output']}", file=sys.stderr)
        return 3
    plan["output"].parent.mkdir(parents=True, exist_ok=True)
    if args.force:
        command.insert(1, "-y")
    else:
        command.insert(1, "-n")
    result = subprocess.run(command)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())

