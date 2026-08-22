# Migration Guide Template

Use this template if the skill is renamed, split, deprecated, or merged.

## Change Type

- Rename:
- Split:
- Merge:
- Deprecation:

## Compatibility Impact

- Trigger phrases affected:
- Output contract affected:
- Reference files affected:
- Eval fixtures affected:

## Required Actions

- Update frontmatter name and description.
- Update `skill_lifecycle.yaml`.
- Update eval IDs only when the scenario changes; keep stable IDs for wording-only changes.
- Add compatibility notes for downstream wrappers or marketplace entries.
- Run stage gate for the relevant transition.
