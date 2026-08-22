# Migration Governance

`humanize-text` is an active writing skill. No rename, split, merge, deprecation, or retirement is planned for this revision.

## Current Identity

- Skill name: `humanize-text`
- Public job: naturalize AI-like or overly formal writing while preserving facts, stance, and key terms.
- Primary neighboring skills: `longform-writing-process`, `spec-organizer`, `web-search-strategy`

## Rename / Split / Merge Rules

- Rename only if the public trigger surface changes beyond humanize / AI tone removal / natural rewrite tasks.
- Split only if file editing, detector diagnosis, or longform writing becomes large enough to require separate workflows.
- Merge only if another writing skill fully owns text naturalization and can preserve the no-list, visible-process, audience-effect, and coherence requirements.

## Deprecate

Deprecation requires all of the following:

- A replacement skill exists and is documented.
- Trigger evals show the replacement covers direct, indirect, and negative cases.
- Migration notes explain old and new trigger phrases.
- Existing references and eval assets are either moved or explicitly retired.

## Migration Evidence

No migration evidence is required for this revision because the skill identity is unchanged. If a future rename, split, merge, or deprecation is proposed, release evidence must include:

- Old and new skill names or folder paths.
- Trigger eval comparison before and after migration.
- Handoff notes for neighboring skills.
- Compatibility notes for existing users and hosts.
- A rollback plan if the replacement under-triggers or over-triggers.

## Compatibility Notes

This revision preserves the existing skill name, folder name, homepage, and primary trigger surface. The main behavioral change is stricter output structure and stronger rewrite-depth selection, not a migration of identity.
