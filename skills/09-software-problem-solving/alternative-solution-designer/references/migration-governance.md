# Migration Governance

## Rename

Renaming this skill requires preserving the current `alternative-solution-designer` slug as an alias or documenting a migration path for hosts that route by folder name. Rename changes must include trigger evals proving that existing phrases such as 替代解法, 換思路, workaround, and fallback design still route correctly.

## Deprecate

Deprecation requires a replacement skill or documented fallback workflow. The deprecation notice must describe what happens to existing evals, references, and user-facing trigger phrases.

## Merge

A merge with neighboring skills is allowed only when the primary job remains coherent. Merge candidates must document overlap with spec-organizer, frontend-design, vibe-coding-guidelines, and skill-creator-advanced, then prove that near-miss prompts do not route incorrectly.

## Split

A split is required if the skill begins producing implementation specs, UI designs, code, or release artifacts as a primary output rather than alternative-solution analysis. Split evidence must identify which eval cases move to the new skill and which remain here.

## Compatibility

Backward compatibility means existing users can still ask for alternative approaches, different routes, simpler workflows, no-LLM paths, rule-based paths, and lowest-friction options without learning new trigger wording. New rules must remain generic and should not encode one-off domain cases into the main skill body.

## Migration Evidence

Migration evidence must include updated trigger evals, functional evals, neighboring skill overlap notes, and a readiness report that names the old version, new version, date, and validation commands.
