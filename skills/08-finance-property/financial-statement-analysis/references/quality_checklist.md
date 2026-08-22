# Quality checklist

這份 checklist 用來檢查 `financial-statement-analysis` 是否符合 repo 的結構要求，以及是否真的落實「先口徑、再三表、後比率、最後紅旗」的工作方式。

## Final gate
- Audit date: 2026-03-26
- Compliance level: 中高
- Overall status: MANUAL_FIXTURE_BENCHMARK_PASS
- Automated checks:
  - [x] `python scripts\\check_skill_name_surface.py --repo-root .`
  - [x] `python scripts\\validate_skills.py --repo-root .`
- Key observations:
  - [x] 新增 skill 的 frontmatter、description 與 references 路徑皆已通過驗證
  - [x] 沒有命名衝突或 description discoverability 問題
  - [x] overlap audit 顯示與既有 skills 沒有明顯 query 搶奪風險
  - [x] 已補齊 8 個 should-trigger 與 8 個 should-not-trigger eval cases
  - [x] 已補 zh / en / mixed 的 trigger 測試矩陣與 boundary cases
  - [x] 已完成 fixture-style paired benchmark、grading 與 review viewer artifacts
  - [x] 已將 workspace 中需長期保留的 benchmark 摘要與 fixture examples 回收進主 skill references
  - [ ] 尚未完成 live router telemetry 或真人盲評

## Format checks
- [x] Folder name is kebab-case
- [x] `SKILL.md` exists and is valid UTF-8
- [x] No `README.md` inside the skill folder
- [x] `references/output-template.md` exists
- [x] `references/source-hierarchy.md` exists
- [x] `references/ratio-and-red-flag-guide.md` exists
- [x] `references/overlap-matrix.md` exists
- [x] `assets/evals/evals.json` and `assets/evals/regression_gates.json` are valid JSON
- [x] No broken local references in `SKILL.md`

## Triggering
- [x] Evals include obvious requests like "幫我解讀這份財報" and "看現金流跟淨利有沒有背離"
- [x] Evals include 10-K / 10-Q / 年報 / 季報 / 三表 / 盈餘品質 / 紅旗等中英混寫說法
- [x] Evals include non-trigger cases for 即時股價、短線交易、技術分析
- [x] Evals include boundary cases against `longdoc-evidence-reader`, `concept-alignment`, and document-writing skills
- [x] Evals cover zh-TW, English finance terms, and mixed-language prompts
- [x] `references/trigger-eval-summary.md` 已整理 fixture trigger audit 與 overlap 指標
- [ ] 尚未完成 live trigger recall run，缺 production dispatch 層級的 `hit@1` / `false positive`

## Output contract
- [x] Fixture benchmark confirms first heading is exactly `## 財報解讀` on should-trigger cases
- [x] Fixture benchmark confirms the five required `###` headings appear in order on should-trigger cases
- [x] `### 分析範圍與口徑`
- [x] `### 核心發現`
- [x] `### 三表橋接與盈餘品質`
- [x] `### 比率、同業與期間對比`
- [x] `### 風險紅旗與待確認事項`
- [x] Important claims include source annotations or clearly labeled filing/note references in fixture outputs
- [x] Facts, inference, and gaps are separated in fixture outputs

## Analysis quality
- [x] The analysis checks accounting policies and notes before ratio interpretation
- [x] The analysis includes a `淨利 -> CFO` bridge or clearly states why it cannot
- [x] Capex / debt / dividend / equity changes are cross-checked against the balance sheet
- [x] Ratio selection is industry-aware instead of exhaustive
- [x] IFRS vs US GAAP comparability risks are surfaced when relevant
- [x] One-time items, reclassifications, leases, or capitalized development costs are not silently ignored

## Risk discipline
- [x] Red flags are presented as risk signals, not direct fraud accusations
- [x] Each red flag includes a plausible alternative explanation
- [x] The answer lists what still needs confirmation from notes or filings
- [x] The skill does not jump from financial analysis straight to a trading instruction

## Freshness and sourcing
- [x] Provided files and official filings are prioritized over secondary summaries
- [ ] Time-sensitive facts are verified with current official or regulatory sources
- [ ] Relative dates are converted into concrete dates when needed
- [ ] Peer comparisons state the comparison basis, period, and accounting standard

## Scope discipline
- [x] The skill does not degrade into raw page extraction only at the design level
- [x] The skill does not degrade into pure translation or document rewriting at the design level
- [x] The skill asks follow-up questions only when missing scope or wrong assumptions would materially change the analysis by contract

## Common error checks
- [x] The skill does not skip accounting-policy or footnote review and jump straight to ratio commentary
- [x] The skill does not present unsupported accusations, trading calls, or certainty beyond filing evidence
- [x] The skill does not collapse into page extraction, translation, or memo rewriting when the primary job is financial interpretation
- [x] The skill keeps facts, inference, and evidence gaps distinct instead of blending them into one conclusion block

## Eval ops
- [x] `references/test_plan.md` exists
- [x] Workspace prepared with paired `with_skill/` and `without_skill/` directories
- [x] At least one iteration has grading, timing, and benchmark artifacts
- [x] `review.html` exists for a fixture paired run
- [x] Long-term references extracted from workspace before deletion:
  - `references/trigger-eval-summary.md`
  - `references/fixture-examples.md`
