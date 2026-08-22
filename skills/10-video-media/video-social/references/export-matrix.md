# Social export matrix reference

## Matrix fields

| Platform/use | Orientation | Frame | Crop strategy | Caption safe area | Duration rule | Quality | Filename |
|---|---|---|---|---|---|---|---|

Fill duration and file-size rules only after checking current official platform
documentation when those limits affect delivery.

## Reframing choices

1. Crop when the important subject remains visible.
2. Track the subject when it moves.
3. Use blurred or designed padding when a crop would remove essential context.
4. Create a separate layout when captions, slides, or UI are too dense for the target.

## Compression

- Prefer CRF-based H.264 encoding for quality-controlled delivery.
- Use two-pass or target bitrate only when a strict file-size ceiling matters.
- Never upscale a low-resolution master solely to match a nominal platform size.
- Inspect text and faces after compression, not just file size.

## QA

- Test the opening frame, captions, logo, final frame, and audio.
- Confirm no target is hidden by platform controls.
- Check each output's dimensions, codecs, duration, and size with `ffprobe`.
- Keep filenames explicit, such as `topic-line-1080x1920.mp4`.
