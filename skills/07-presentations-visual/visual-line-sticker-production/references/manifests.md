# Project Files and Reuse

Create these files in the user's chosen project folder. Keep their contents portable and do not store credentials, local absolute paths, or hidden system instructions.

## `collection-manifest.json`

```json
{
  "schema_version": 1,
  "collection_id": "friendly-otter-v1",
  "character_id": "friendly-otter",
  "style_version": "1.0",
  "product": {
    "creator": "",
    "title": "",
    "description": "",
    "copyright": "",
    "language": "zh-Hant"
  },
  "sticker_count": 8,
  "text_mode": "exact",
  "rights_confirmed": false,
  "stickers": [
    {"id": "01", "text": "", "intent": "", "action": "", "composition": "", "approved": false}
  ],
  "assets": {"main": "main.png", "tab": "tab.png"}
}
```

Use `text_mode` values `exact`, `intent-led`, `mixed`, or `none`. Include exactly `sticker_count` sticker rows before generation.

## `character-style-profile.md`

```markdown
# Character Style Profile

- Character ID:
- Style version:
- Rights / reference-image permissions:
- Identity invariants:
- Palette:
- Line / rendering style:
- Proportions and recurring accessories:
- Allowed props and expressions:
- Avoid list:
- Approved anchor-sample notes:
- Prompt scaffold:
```

## Reuse rules

- **Reuse unchanged:** copy the profile and preserve `character_id` and `style_version`; create a new `collection_id` and a fresh manifest.
- **Style revision:** preserve `character_id`, increment `style_version`, state the change, and require a new anchor approval.
- **New character:** create a new profile and `character_id`; never overwrite the older collection or its approved profile.
