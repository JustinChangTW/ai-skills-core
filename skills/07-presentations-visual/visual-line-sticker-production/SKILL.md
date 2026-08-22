---
name: visual-line-sticker-production
description: Create, iterate, validate, and package upload-ready static LINE sticker sets with customizable character style and on-sticker text. Use when a user asks for LINE stickers, LINE貼圖, a reusable sticker character, Creators Market assets, or a follow-up sticker collection that must retain an approved character style.
---

# LINE Sticker Production

Create normal static LINE sticker sets only. Support 8, 16, 24, 32, or 40 stickers plus a main image and chat thumbnail. Do not treat animated, message, custom, Big, Pop-up, or Effect stickers as this workflow.

## Host Contract

Use the host's native image-generation capability for every visual asset. In Codex, call the built-in image-generation tool. In ChatGPT Work, use its available native image-generation capability.

Never call an image API, require an API key, invoke an image CLI, or substitute code-drawn artwork. If native generation is unavailable, complete the brief, manifests, and production prompts, explain the capability gap, and stop before visual generation.

Keep the skill portable: do not require absolute paths, a local repository, or a particular shell. Store the current project's files wherever the host or user designates.

## Start and Reuse

If the user provides a `character-style-profile.md` and `collection-manifest.json`, ask whether to reuse unchanged, create a new style version, or start a new character. For reuse or a style revision, generate and obtain approval for one fresh anchor sample before generating the collection.

Otherwise, ask for one choice at a time. Default to **guided mode**.

| Mode | Ask for |
| --- | --- |
| Quick | style preset, count, language, text mode, subject, and any reference image |
| Guided | each checkpoint below, with concise examples and a confirmation gate |
| Art director | every sticker's pose, composition, color, prop, text placement, and avoid list |

Read `references/workflow-and-prompts.md` before intake. Read `references/line-static-spec.md` before generating or validating. Read `references/manifests.md` before creating project files or a reuse profile.

## Guided Workflow

1. **Rights and product details.** Collect creator, title, description, copyright, sale language, and confirmation that the creator owns or has permission for all character, reference, likeness, and trademark material. Check limits before freezing them.
2. **Set configuration.** Confirm an allowed sticker count, text mode, intended audience, conversation situations, and output location.
3. **Character and style lock.** Gather one or more reference images, a written character bible, a style preset, or custom art direction. Freeze character identity, silhouette, palette, line weight, proportions, recurring accessories, and avoid list in a draft profile.
4. **Text plan.** Offer four modes: exact text per sticker, model-proposed text from intent, mixed, or no on-image text. For any on-image text, present a numbered table with the exact final string, action/emotion, and composition. Do not generate the set until the table is approved.
5. **Anchor sample.** Build one concise prompt using the approved profile and a representative sticker. Generate one transparent-background asset, inspect it with the user for character continuity, spelling, readability, margins, and prohibited content. Update the profile only after approval.
6. **Generate assets.** Generate one independent sticker at a time; never request a contact sheet, collage, mockup, product photo, or multi-sticker grid. Use the locked character profile and the individual row's text verbatim. Generate separate main and chat-thumbnail images that visibly match the set.
7. **QA and repair.** Inspect every image for transparent background, exact text, safe margins, character drift, duplicate poses, and LINE review risks. Regenerate only failing assets. Use `scripts/prepare_line_assets.py` only after visual approval; it normalizes existing artwork and never draws or edits artwork.
8. **Package.** Run `scripts/verify_line_static_stickers.py` against the prepared folder and manifest. Resolve every error, then create the ZIP, QA report, manifest, and character profile. State that the user must review and upload the package in LINE Creators Market.
9. **Continuation gate.** Ask exactly: `要以相同角色風格製作下一組貼圖嗎？` Offer reuse unchanged, reuse with a style revision, new character, or finish. Preserve previous files; never overwrite an approved collection.

## Prompt Rules

Use the production-prompt template from `references/workflow-and-prompts.md`. Every prompt must state: one sticker only; transparent background; no mockup, panel, grid, watermark, URL, logo, or advertisement; visible margin; locked character details; one action/emotion; and the exact on-image text when applicable.

Treat image-generated text as unverified until visibly checked. If it differs in spelling, punctuation, legibility, or language, regenerate that asset with a single targeted correction. Do not silently replace text with programmatic drawing.

## Local Technical Tools

The scripts require Pillow and are optional host helpers, not required for ChatGPT Work's reasoning workflow.

```bash
python3 scripts/prepare_line_assets.py --stickers-dir selected/stickers --main selected/main.png --tab selected/tab.png --count 8 --out-dir ready
python3 scripts/verify_line_static_stickers.py --input-dir ready --manifest collection-manifest.json --report qa-report.json --zip-out line-sticker-upload.zip
```

They only prepare and verify already-approved PNGs. If scripts cannot run in the current host, provide the same manual checklist from `references/line-static-spec.md` and do not claim technical validation passed.
