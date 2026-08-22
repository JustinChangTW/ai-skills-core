# Tutorial plan reference

## Schema

```json
{
  "source": "/absolute/path/recording.mp4",
  "orientation": "vertical",
  "title": "Visit Japan Web 操作教學",
  "steps": [
    {
      "start": 2.4,
      "end": 8.2,
      "title": "步驟一",
      "instruction": "點選「登入」",
      "focus": {"x": 0.2, "y": 0.68, "width": 0.6, "height": 0.12},
      "redactions": [
        {"x": 0.1, "y": 0.12, "width": 0.8, "height": 0.08}
      ]
    }
  ]
}
```

Coordinates are normalized from 0 to 1 relative to the unrotated display frame.

## Annotation design

- Use one accent color throughout.
- Place arrows outside the target, pointing inward.
- Use a focus rectangle or zoom, not both, unless the screen is dense.
- Keep step text short enough to read without pausing.
- Ease zooms in and out; avoid sudden motion that hides the interface.

## Privacy review

Check every frame around keyboard entry, notifications, account pages, QR codes,
addresses, booking numbers, email addresses, and payment screens. Redaction must
begin before the sensitive element appears and end after it disappears.

## Final verification

- Each instruction names the control visible on screen.
- The target marker lands on the correct control.
- No step begins after the relevant click.
- Phone text remains legible at actual messaging-app display size.
- Redactions remain aligned through zoom and crop operations.
