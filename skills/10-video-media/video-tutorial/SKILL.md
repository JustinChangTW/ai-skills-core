---
name: video-tutorial
description: Turn screen recordings, phone recordings, app demos, or browser walkthroughs into concise step-by-step operation tutorial videos. Use for trimming idle time, organizing steps, adding Traditional Chinese captions, zoom/focus regions, click indicators, arrows, callouts, privacy redaction, title cards, narration, and LINE/mobile-friendly exports. Trigger for 操作教學影片、螢幕錄影教學、App教學、網站教學、手機操作說明, or tutorial-video requests.
---

# Video Tutorial

Create faithful operation tutorials whose annotations match the real interface.

## Workflow

1. Inspect the recording and determine platform, orientation, dimensions, duration, and whether narration exists.
2. Identify the exact task outcome and audience. Keep one tutorial focused on one outcome.
3. Extract overview frames, then inspect each interaction at higher frame density. Never infer a button from memory when it can be verified in the recording.
4. Create a step plan containing source times, step title, instruction, focus rectangle, and any redaction. Validate it with `scripts/validate_tutorial_plan.py`.
5. Remove loading, dead time, repeated attempts, notifications, and accidental personal information. Preserve enough lead-in before each click for viewers to orient themselves.
6. Add restrained zooms, focus frames, click indicators, arrows, and step cards. Keep annotations clear of the actual target.
7. Add Traditional Chinese subtitles or concise on-screen instructions. Use the `video-subtitle` workflow when available.
8. Render a representative preview. Verify every label and target against the recording before final export.
9. Deliver a 1080p master and any requested mobile or LINE variant.

## Tutorial Rules

- Use real screenshots or frames from the supplied recording; do not fabricate UI.
- Number steps consistently and use action-led text such as「點選登入」.
- Show one main action at a time.
- Keep important controls visible for at least 1 second before the action.
- Use normalized focus coordinates so annotations survive resizing.
- Blur or cover names, IDs, QR codes, addresses, account values, notifications, and other sensitive data.
- Do not show passwords, OTPs, API keys, or private company data.
- Never overwrite the source recording.

## Output Defaults

- Horizontal desktop tutorial: 1920×1080.
- Vertical phone tutorial: 1080×1920.
- LINE-friendly version: H.264/AAC MP4 with moderate compression and readable text.
- Preview first; final only after timing and labels have been checked.

## Resources

- `scripts/validate_tutorial_plan.py`: validate step timing, normalized focus regions, and redaction entries.
- `references/tutorial-plan.md`: plan schema, annotation design, privacy review, and verification.
