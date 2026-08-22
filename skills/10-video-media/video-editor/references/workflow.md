# Video edit workflow reference

## Cut-plan schema

```json
{
  "source": "/absolute/path/input.mp4",
  "output": "/absolute/path/output/final.mp4",
  "segments": [
    {"start": 0.0, "end": 12.4},
    {"start": 15.2, "end": 31.8}
  ],
  "crf": 20,
  "preset": "medium",
  "audio_bitrate": "192k"
}
```

Segments are concatenated in the listed order. Use absolute paths. The renderer
refuses to overwrite its input and defaults to dry-run.

## Quality presets

| Purpose | Resolution | CRF | Preset |
|---|---:|---:|---|
| Fast preview | source or 720p | 26–28 | veryfast |
| General final | source up to 1080p | 18–22 | medium |
| Archive intermediate | source | 14–18 | slow |

Do not upscale unless explicitly requested. For LINE or messaging delivery,
prefer a moderate bitrate/CRF and test the final file size.

## Verification checklist

- Duration and segment order match the approved plan.
- First and last frames are not accidentally black.
- Spoken-word cuts have no clipped syllables or clicks.
- Audio stays synchronized after speed changes and concatenation.
- Dimensions, rotation, and aspect ratio are correct.
- H.264 output uses `yuv420p` for broad phone compatibility.
- Final file opens and reports both video and audio streams when expected.
