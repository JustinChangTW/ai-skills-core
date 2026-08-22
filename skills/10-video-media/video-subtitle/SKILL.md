---
name: video-subtitle
description: Create, edit, validate, style, translate, and burn subtitles for local video or audio. Use for speech transcription, timestamped Traditional Chinese subtitles, SRT/VTT/ASS output, subtitle correction, caption timing, bilingual captions, open captions, or soft subtitle tracks. Trigger when the user asks for 字幕、逐字稿、語音轉文字、中文字幕、雙語字幕、字幕燒錄, or supplies media plus transcript text.
---

# Video Subtitle

Produce accurate, readable subtitles with local-first handling and explicit timing verification.

## Workflow

1. Inspect the source with `ffprobe`.
2. Select the safest transcription source:
   - use supplied SRT/VTT/ASS when available;
   - prefer a local Whisper-compatible engine for sensitive media;
   - use an external transcription API only with explicit authorization;
   - if no engine is available, ask for transcript text or create timing from user-approved cues.
3. Preserve Taiwanese names, Japanese place names, product names, numbers, and technical terms. Build a correction glossary when needed.
4. Split captions at natural phrase boundaries. Avoid leaving conjunctions or particles alone.
5. Save editable SRT first. Use `scripts/srt_from_json.py` for structured cues and `scripts/validate_srt.py` before rendering.
6. Preview a representative section with the real font and final frame size.
7. Deliver the editable subtitle file and, when requested, a burned-in or soft-subtitle video.

## Caption Defaults

- Use Traditional Chinese unless the user requests another language.
- Prefer 1–2 lines, about 12–20 CJK characters per line for phone video.
- Keep ordinary captions on screen roughly 1–6 seconds; use shorter timing only for deliberate fast captions.
- Leave adequate bottom safe area for mobile controls and platform overlays.
- Use high-contrast text with outline or shadow. Verify that the chosen font contains Traditional Chinese glyphs.
- Do not silently rewrite the speaker's meaning. Mark uncertain words for review.

## Output

- Preserve the original media.
- Name editable files clearly: `.srt`, `.vtt`, or `.ass`.
- For broad phone compatibility, burn subtitles into H.264/AAC MP4 only after the editable subtitle has been checked.
- Verify the final frame, audio synchronization, and the first/last subtitle timing.

## Resources

- `scripts/srt_from_json.py`: convert validated cue JSON into SRT.
- `scripts/validate_srt.py`: check sequence numbers, timestamps, overlaps, and empty captions.
- `references/subtitle-style.md`: layout, timing, font, and export guidance.
