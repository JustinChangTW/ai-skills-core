# Telemetry Playbook

This skill should not store user-provided sensitive text in the skill folder.

## Useful Non-Sensitive Signals

- Trigger misses: relevant prompt did not load the skill.
- Over-trigger cases: general polishing or legal diagnosis prompts incorrectly loaded the skill.
- Output defects: missing risk summary, missing rewrite, unsupported legal/medical certainty, or broken technical compatibility.
- Source freshness defects: current official guidance was required but not checked.

## Review Cadence

- Review terminology and source anchors every 60 days.
- Add new eval cases after real failures, keeping stable IDs for existing cases.
