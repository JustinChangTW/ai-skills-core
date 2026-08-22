# Quality checklist

這份 checklist 用來記錄 ethical-persuasion-strategy 目前是否符合 `skill-creator-advanced` 的 readiness gate 規範。
本次 audit 以 `quick_validate.py`、`format_check.py`、`audit_skill_references.py` 與 `SKILL.md` 結構掃描為基礎，並保留 skill 專屬檢核項。

## Final gate
- Audit date: 2026-03-24
- Compliance level: 中
- Overall status: PARTIAL
- Automated checks:
  - [x] `quick_validate.py` passed
  - [x] `format_check.py` passed
  - [x] `audit_skill_references.py` passed
- Key observations:
  - 自動檢查全數通過。
  - 本次將舊 checklist 升級為 readiness gate 結構。
- Structural gaps to keep improving:
  - 缺少明確 role 區塊
  - 缺少明確 decision boundary 區塊
  - output contract 不夠明示
  - default follow-through policy 不夠明示
  - 缺少 worked examples / examples 區塊

## Format checks
- [x] skill folder 名稱符合 kebab-case
- [x] `SKILL.md` 存在且通過基本 frontmatter 驗證
- [x] `format_check.py` 為 0 errors / 0 warnings
- [x] `SKILL.md` 內提到的本地 `scripts/`、`references/`、`assets/` 路徑都存在
- [x] `references/quality_checklist.md` 已存在且已依本次 audit 更新
- [x] `SKILL.md` 中沒有待清理的 `TODO` / `[TODO]`

## Requirement and policy checks
- [x] `SKILL.md` 有明確 workflow / instructions
- [ ] 有獨立 `role` 區塊或等價角色定義
- [ ] 有獨立 decision boundary 區塊或等價使用邊界
- [ ] 有明確 output contract / output shape 要求
- [ ] 有明確 default follow-through policy / ask-first 邊界
- [x] 有工具或路由使用規則
- [ ] 有 worked examples / examples 支撐輸出品質

## Common error checks
- [x] 沒有失效的本地引用路徑
- [x] frontmatter / 命名 / description 沒有被 validator 擋下
- [x] 結構與文字格式沒有被 linter 擋下
- [ ] readiness gate 所期待的關鍵區塊已完整具備
- [x] checklist 已與新版 readiness gate 結構對齊

## Skill-specific checks
Use this checklist before shipping a new version of this skill.

### Structure
- [ ] Folder name is kebab-case
- [ ] SKILL.md exists and is valid UTF-8
- [ ] YAML frontmatter has `name` and `description`
- [ ] Description clearly says when this skill should trigger
- [ ] No README.md exists inside the skill folder

### Triggering
- [ ] Triggers on "說服策略", "買單", "buy-in", "message house", "反對點 FAQ", "A/B 測試", "護欄指標"
- [ ] Triggers on paraphrases such as "怎麼讓客戶接受", "怎麼讓主管核准", "怎麼降低變革反彈"
- [ ] Does NOT trigger on pure copywriting, translation, or direct slide design requests
- [ ] Does NOT steal work from `longform-writing-process`, `slide-content-planner`, or `spec-organizer`
- [ ] Handles mixed Chinese and English trigger phrases

### Strategy quality
- [ ] Defines a concrete target behavior instead of vague "說服成功"
- [ ] Diagnoses audience variables before generating tactics
- [ ] Chooses a persuasion route based on involvement and ability
- [ ] Maps each tactic to a concrete mechanism and execution step
- [ ] Includes message house, objection handling, and evidence design
- [ ] Includes at least one primary KPI and one set of guardrail metrics

### Safety quality
- [ ] Refuses fake scarcity, dark patterns, coercion, misinformation, and political microtargeting
- [ ] Distinguishes verified facts from assumptions and hypotheses
- [ ] Includes transparency, privacy, fairness, and exit-path checks
- [ ] Rewrites high-risk requests into safer alternatives when possible

### Maintenance
- [ ] Evals in `assets/evals/evals.json` reflect realistic prompts
- [ ] Regression gates are defined in `assets/evals/regression_gates.json`
- [ ] Wording stays practical and avoids abstract filler
- [ ] Detailed guardrails and diagnostics stay in `references/` instead of bloating `SKILL.md`
