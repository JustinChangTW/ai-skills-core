# Migration governance

## Rename

Preserve the old trigger name as an alias or migration note for at least one review cycle. Update evals and handoff references before removing it.

## Deprecate

Mark the lifecycle state, identify the replacement, keep removal reversible, and notify the user before disabling the active Skill.

## Merge

Merge only when both Skills share the same primary job and workflow. Preserve unique triggers as boundary evals and document the destination.

## Split

Split when use cases no longer share one workflow or require materially different permission levels. Define which Skill owns each outcome.

## Compatibility

Keep the core Agent Skills instructions portable. Host wrappers may translate tool names but must not weaken evidence, approval or privacy rules.

## Migration Evidence

Require a before／after routing map, affected triggers, rollback path and passing near-miss evals before completing a rename, deprecation, merge or split.
