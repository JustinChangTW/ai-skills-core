# Migration Governance

Audit date: 2026-06-14

## Rename

Current canonical name is `blender-control`. A future rename must preserve this name as an alias for at least one release cycle and update:

- `SKILL.md` frontmatter name and description.
- `skill_lifecycle.yaml`.
- `assets/evals/evals.json`.
- `references/readiness_report.md`.
- Catalog or marketplace surfaces in a separate repo-wide release step.

## Deprecate

Deprecation is allowed only when a newer Blender skill covers the same primary job with equal or better trigger coverage. The deprecation note must state:

- Replacement skill name.
- Compatibility window.
- User-facing migration message.
- Eval evidence showing no loss of direct, indirect, negative, and overlap-neighbor coverage.

## Merge

Merge with adjacent skills is allowed only when the primary job remains one coherent Blender control workflow. Merge is not allowed merely to absorb image generation, Three.js frontend, tutorial video, or general documentation tasks.

Required merge evidence:

- Overlap matrix.
- Before/after trigger eval results.
- Updated handoff rules.
- Draft release gate result.

## Split

Split this skill when one subdomain becomes too large or requires separate tools, such as:

- Dedicated Blender camera/video render skill.
- Dedicated industrial parametric modeling skill.
- Dedicated rigging/retargeting skill.

Required split evidence:

- New target skill boundaries.
- Negative trigger cases for both sides.
- Migration notes for old prompts.
- Stage gate results for the split artifacts.

## Compatibility

Compatibility policy:

- Preserve `blender-control` trigger wording for Blender, BlenderMCP, bpy, product modeling, material, modifier, camera animation, export, and troubleshooting tasks.
- Do not introduce a required dependency on one MCP server, WebSocket wrapper, external API, or paid service without a fallback route.
- Keep Traditional Chinese as the primary explanation language while preserving Blender API/tool names in English.

## Migration Evidence

Initial create-stage evidence:

- No previous local `blender-control` skill existed in this repo at creation time.
- The new skill is additive and does not modify neighboring skills.
- Source repos were used as design inputs, not copied wholesale.
- Full mechanical gate evidence is recorded in `references/readiness_report.md`.
