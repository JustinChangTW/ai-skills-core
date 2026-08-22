# Intake and Prompt Templates

## Customization choices

### Visual source

Choose one or combine them:

1. **Reference locked** — uploaded character images establish identity; record their role and permission.
2. **Character bible** — written species/person, silhouette, age impression, proportions, clothing, accessories, palette, line weight, and prohibited changes.
3. **Style preset** — choose a starting point such as soft chibi, bold cartoon, hand-drawn pencil, flat vector-like, or custom.
4. **Art direction** — specify layout, palette, stroke, texture, expression, props, and avoid list.

### Text mode

1. **Exact** — user supplies every final on-image string.
2. **Intent-led** — user gives situations; propose a numbered text table for approval.
3. **Mixed** — retain user-supplied strings and propose only marked gaps.
4. **No text** — communicate through expression/action alone.

Never change an approved exact string. For Traditional Chinese, keep text short and large; do not promise generated typography is correct until visually reviewed.

## Intake checklist

Collect and confirm these fields in order:

1. Mode, output location, sticker count, language, audience, and text mode.
2. Creator, title, description, copyright, and rights confirmation.
3. Character/style source, reference-image roles, palette, identity invariants, and avoid list.
4. A numbered sticker table: id, exact text or intent, emotion/action, composition, optional prop, and approval state.
5. Main-image and thumbnail direction.

Pause after the product details, after the table, and after the anchor sample. Do not turn a vague intent into final commercial text without showing it for approval.

## Production prompt

Use this compact template, replacing only bracketed fields:

```text
Asset: one independent static LINE sticker, not a sheet or collage.
Character lock: [approved character identity, silhouette, palette, line style, accessories, reference images].
Action and emotion: [one approved action/emotion].
Composition: [approved placement and optional prop].
On-image text, reproduce exactly: "[exact text]".
Style: [approved style].
Technical constraints: transparent background; content fully visible with about 10 px clear margin; high-contrast readable text; no border panel, mockup, grid, watermark, URL, brand logo, advertisement, unrelated characters, or extra words.
```

For textless stickers, remove the text line and add `No text anywhere in the image.`

## Visual inspection checklist

- Exactly one sticker and one coherent character.
- Transparent background, no simulated checkerboard or white rectangle.
- Text exactly matches approved text and remains readable at small chat size.
- Character identity, color, line quality, and accessories match the profile.
- Pose is distinct from the other planned stickers and fits a common conversation need.
- No prohibited commercial, rights, or safety content.
