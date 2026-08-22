---
name: video-social
description: Adapt an approved master video into platform-specific social deliverables without changing its core message. Use for LINE sharing, YouTube, Shorts, Instagram, Reels, Facebook, TikTok-style delivery, aspect-ratio variants, compression, thumbnails, captions, filenames, and upload packages. Trigger for 社群影片、LINE影片、平台尺寸、多版本輸出、影片壓縮、上傳版本, or social distribution requests.
---

# Video Social

Export platform variants from an approved master while keeping quality, captions, and safe areas consistent.

## Workflow

1. Start from the approved master, not raw media.
2. Confirm the target platforms, audience, and whether each version is a post, story, reel, short, or ordinary video.
3. Verify current platform limits from official documentation when duration, size, codec, or upload rules matter. Do not rely on remembered limits.
4. Create an export matrix covering aspect ratio, frame size, crop strategy, caption position, duration, bitrate/quality, filename, and thumbnail.
5. Reframe intentionally. Use padding or a designed background when cropping would remove important content.
6. Render a small test segment for each distinct composition, then export final variants.
7. Verify playback and report the files. Do not post or upload unless the user separately asks.

## Defaults

- Preserve the approved message and cut.
- Use H.264/AAC MP4 and `yuv420p` for broad compatibility unless the target requires otherwise.
- Keep captions and logos inside platform-safe areas.
- For LINE, prioritize readable captions and practical file size.
- Do not add watermarks, engagement bait, or platform logos unless requested.
- Never overwrite the master.

## Resources

Read `references/export-matrix.md` for variant planning, reframing, compression, and QA.
