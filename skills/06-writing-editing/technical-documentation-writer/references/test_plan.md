# Test Plan: technical-documentation-writer

## 1) Triggering tests

Goal: the skill loads when it should, and stays off when it should not.

### Should trigger (8-10)

Use obvious requests, paraphrases, real user wording, and file-type/tool variants.

- 幫我寫文件
- 整理開發者指南
- 把這份 API 說明重寫清楚
- 建立 onboarding 教學
- 做 docs gap analysis
- [TODO: add paraphrases from real user wording]

For each item, record:
- Expected: trigger
- Actual:
- Notes:

### Should NOT trigger (8-10)

- [TODO: unrelated request that should stay off]
- [TODO: near-miss that looks similar but belongs to another skill]
- [TODO: broad generic query that should not trigger this skill]

For each item, record:
- Expected: no trigger
- Actual:
- Notes:

### Near-miss / confusing cases

- [TODO: similar wording but different outcome]
- [TODO: same tool name but different workflow]

### Multilingual coverage

- zh:
  - [TODO: pure Chinese phrasing]
- en:
  - [TODO: pure English phrasing]
- mixed:
  - [TODO: Chinese + English tool/file phrasing]

### Neighboring skills / overlap map

- Closest competing skill:
  - [TODO]
- Why this skill should win:
  - [TODO]
- Why another skill should win in adjacent cases:
  - [TODO]

### Trigger diagnostics

#### Under-trigger signals
- [ ] Obvious request failed to load the skill
- [ ] Only one specific wording works
- [ ] Real user phrasing fails but clean paraphrase works

#### Over-trigger signals
- [ ] Unrelated requests load the skill
- [ ] Broad generic keywords cause false positives
- [ ] Requests that belong to another skill still load this one

#### Likely fix direction
- If under-trigger dominates: revise `description`
- If over-trigger dominates: narrow scope or add negative triggers
- If both happen: split scope or rewrite `description` from scratch

## 2) Functional tests

Goal: outputs and tool usage are correct end-to-end.

Create test cases in Given/When/Then form. Prefer real tasks over invented textbook prompts.

### Test case A (happy path)
- Given:
- When:
- Then:

### Test case B (edge case)
- Given:
- When:
- Then:

### Test case C (failure mode / error handling)
- Given:
- When:
- Then:

### Test case D (recovery path)
- Given:
- When:
- Then:

### Failure classification
- If a test fails, label the primary cause:
  - Trigger problem
  - Workflow / instruction problem
  - Resource / script problem
  - External tool / MCP problem

## 3) Performance comparison

Goal: prove the skill improves baseline.

### Baseline (without skill)
- Result quality:
- Total messages / back-and-forth:
- Tool calls:
- Failed tool calls / retries:
- Token usage (if available):
- User corrections required:
- Main failure points:

### With skill
- Result quality:
- Total messages / back-and-forth:
- Tool calls:
- Failed tool calls / retries:
- Token usage (if available):
- User corrections required:
- Main failure points:

### Benchmark summary
- Better than baseline?
- If yes, why?
- If no, what got worse?
- Is the skill helping, or just adding more instructions?

### ROI review
- Is the quality gain worth the extra time/tokens?
- Does this skill reduce user corrections?
- Does this skill reduce operational risk or only add complexity?
- If this were maintained for 6 months, would it still be worth keeping?

## 4) Iteration log

### Round 1
- Change made:
- Hypothesis:
- Result:
- Next move:

### Round 2
- Change made:
- Hypothesis:
- Result:
- Next move:

## 5) Operationalize these cases

- Mirror approved prompts into `assets/evals/evals.json`
- Create an iteration workspace with the shared skill-creator toolchain, for example `python skills/skill-creator-advanced/scripts/prepare_eval_workspace.py <path/to/skill>`
- Save with-skill and baseline outputs in the paired workspace layout
- Generate `benchmark.json` / `benchmark.md`
- Generate `review.html` for human review
- Define release gates in `assets/evals/regression_gates.json`
- Validate release gates with the shared skill-creator toolchain, for example `python skills/skill-creator-advanced/scripts/check_regression_gates.py <benchmark.json> --config <gates.json>`

## 6) Release readiness checklist

- [ ] format_check.py has 0 errors
- [ ] quick_validate.py passes
- [ ] All functional tests pass
- [ ] Multilingual trigger coverage reviewed
- [ ] Neighboring skill overlap reviewed
- [ ] Under-trigger risks addressed
- [ ] Over-trigger risks addressed
- [ ] Baseline comparison completed
- [ ] ROI review completed
- [ ] Regression gates pass
- [ ] Real-user or near-real test prompts included
- [ ] Version bumped (top-level version: YYYY.M.D)
- [ ] Distribution instructions updated (repo-level docs outside skill folder)
