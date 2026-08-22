---
name: video-editor
description: Edit local video files with a review-first FFmpeg workflow. Use for trimming, cutting, merging, reordering, removing pauses, changing speed or aspect ratio, normalizing audio, adding overlays, producing previews, or exporting MP4/MOV/WebM deliverables. Trigger when the user asks to 剪影片、剪片、合併影片、刪除片段、調整影片、輸出成片, or supplies video files for editing.
---

# Video Editor

Edit video locally and preserve the source. Prefer deterministic FFmpeg operations and reviewable plans over opaque one-shot edits.

## Workflow

1. Locate the source files and confirm that the user owns or may edit them.
2. Run `scripts/media_probe.py` on every source. Record duration, dimensions, frame rate, codecs, audio channels, and rotation.
3. Restate the requested result as a compact edit plan. Resolve only choices that materially change the cut.
4. For speech-driven cuts, obtain a timestamped transcript before deciding what to remove. Never delete uncertain phrases solely because they look like filler.
5. Save a machine-readable cut plan. Use `scripts/render_cut_plan.py` for trim, reorder, and concatenate jobs.
6. Render a short or 720p preview first when the edit is subjective, long, or expensive.
7. Inspect the preview with `ffprobe`; sample frames or audio around cut boundaries when timing matters.
8. Apply feedback, then render the final deliverable.

## Output Rules

- Never overwrite an input file.
- Default to MP4, H.264, AAC, `yuv420p`, and `+faststart` unless the request or source requires otherwise.
- Keep aspect ratio unless the user explicitly requests reframing.
- Preserve natural speech. Add 20–50 ms audio fades at hard spoken-word cuts when needed to avoid clicks.
- Quote paths and avoid shell interpolation for user-provided filenames.
- Put previews and final renders in a dedicated output folder.
- Report the final duration, dimensions, codecs, and file size.

## Safety and Privacy

- Prefer local processing for private, financial, workplace, or personal video.
- Do not upload media to transcription, voice, or editing services without explicit authorization.
- Do not download copyrighted online video unless the user supplied it or clearly has rights to use it.
- Flag destructive editorial choices, face/identity changes, or misleading rearrangements before rendering.

## Resources

- `scripts/media_probe.py`: inspect media and emit normalized JSON.
- `scripts/render_cut_plan.py`: validate and optionally execute a non-destructive cut plan.
- `references/workflow.md`: plan schema, quality presets, and verification checklist.
