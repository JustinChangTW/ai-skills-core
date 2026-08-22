# Readiness Report

- Skill: alternative-solution-designer
- Version: 2026.5.22
- Audit date: 2026-05-22
- Stage: draft
- Overall status: DRAFT PASS pending live benchmark evidence

## Scope

This revision keeps the primary job unchanged: reframe a constrained problem, compare genuinely different alternative solution routes, and produce a lowest-friction path. The update adds generalized cost-role reversal, participant-value checks, and release-gate evidence without encoding a single domain case into the skill body.

## Gate Evidence

- Static format: `python skills\skill-creator-advanced\scripts\format_check.py skills\alternative-solution-designer`
- Structure: `python skills\skill-creator-advanced\scripts\audit_structure.py skills\alternative-solution-designer --json`
- Workflow contract: `python skills\skill-creator-advanced\scripts\audit_workflow_contract.py skills\alternative-solution-designer --json`
- Eval coverage: `python skills\skill-creator-advanced\scripts\audit_eval_coverage.py skills\alternative-solution-designer --json`
- Eval quality: `python skills\skill-creator-advanced\scripts\audit_eval_quality.py skills\alternative-solution-designer --json`
- Golden trigger set: `python skills\skill-creator-advanced\scripts\audit_golden_trigger_set.py skills\alternative-solution-designer --json`
- Reference audit: `python skills\skill-creator-advanced\scripts\audit_skill_references.py skills\alternative-solution-designer --json`
- Draft release gate: `python skills\skill-creator-advanced\scripts\release_gate.py skills\alternative-solution-designer --stage draft --json`

## Coverage

- Direct trigger cases: zh and en.
- Indirect trigger cases: zh and mixed.
- Negative near-miss case: direct spec request that should hand off to spec-oriented workflow.
- Functional coverage: OCR/LLM pipeline reframe, agent workflow replacement, high-labor cost role reversal, manual review workaround.

## Known Limitations

- Live paired benchmark evidence is not included in this draft report.
- Outputs are advisory; operational, labor, legal, safety, or financial decisions still require domain-specific validation.
## Requirement / Policy Checks

- The skill keeps a single primary job: alternative-solution analysis.
- The workflow requires web or primary-source checking when freshness, law, safety, cost, or technical claims can affect the answer.
- External participant strategies require value-equivalence, quality-control, safety, legal, insurance, labor, and trust-risk checks.
- Gate language follows fail-first precedence: partial PASS results cannot override FAIL or BLOCKED gates.

## Common Error Checks

- Avoid optimizing the original solution before reframing the problem.
- Avoid producing three variants of the same approach.
- Avoid one-off domain examples in the generic skill body.
- Avoid treating external participants as free labor without reciprocal value and risk controls.
- Avoid claiming release readiness when live benchmark evidence is missing.

## Publish Gate Status

- Draft release gate: PASS on 2026-05-22.
- Revise stage gate: PASS on 2026-05-22.
- Publish gate: FAIL until a real benchmark artifact is produced. The only blocking publish finding is `benchmark_missing`; this report intentionally does not fabricate benchmark results.
