# 品質檢查清單

這份 checklist 用來記錄 alternative-solution-designer 目前是否符合 `skill-creator-advanced` 的 readiness gate 規範。
本次 audit 以 `quick_validate.py`、`format_check.py`、`audit_skill_references.py` 與 `SKILL.md` 結構掃描為基礎，並保留 skill 專屬檢核項。

## 最終關卡
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

## 格式檢查
- [x] skill folder 名稱符合 kebab-case
- [x] `SKILL.md` 存在且通過基本 frontmatter 驗證
- [x] `format_check.py` 為 0 errors / 0 warnings
- [x] `SKILL.md` 內提到的本地 `scripts/`、`references/`、`assets/` 路徑都存在
- [x] `references/quality_checklist.md` 已存在且已依本次 audit 更新
- [x] `SKILL.md` 中沒有待清理的 `TODO` / `[TODO]`

## 需求與政策檢查
- [x] `SKILL.md` 有明確 workflow / instructions
- [ ] 有獨立 `role` 區塊或等價角色定義
- [ ] 有獨立 decision boundary 區塊或等價使用邊界
- [ ] 有明確 output contract / output shape 要求
- [ ] 有明確 default follow-through policy / ask-first 邊界
- [x] 有工具或路由使用規則
- [ ] 有 worked examples / examples 支撐輸出品質

## 常見錯誤檢查
- [x] 沒有失效的本地引用路徑
- [x] frontmatter / 命名 / description 沒有被 validator 擋下
- [x] 結構與文字格式沒有被 linter 擋下
- [ ] readiness gate 所期待的關鍵區塊已完整具備
- [x] checklist 已與新版 readiness gate 結構對齊

## Skill 專屬檢查
Use this checklist before shipping a new version of this skill.

### 結構
- [ ] Folder name is kebab-case
- [ ] SKILL.md exists and is valid UTF-8
- [ ] YAML frontmatter has `name` and `description`
- [ ] Description clearly says when this skill should trigger
- [ ] No README.md exists inside the skill folder

### 觸發
- [ ] Triggers on "替代解法", "不同思路", "不要只優化原解", "最低摩擦解"
- [ ] Triggers on paraphrases such as "有沒有更簡單作法", "可不可以不用這條路"
- [ ] Does NOT trigger on direct bug-fixing or code-writing requests
- [ ] Does NOT steal work from `spec-organizer`, `frontend-design`, or implementation-oriented skills
- [ ] Handles mixed Chinese and English trigger phrases

### 分析品質
- [ ] Includes a one-sentence essence reframe
- [ ] Classifies the problem into at least 1 structure model
- [ ] Includes at least 2 cross-domain analogies
- [ ] Identifies relaxable assumptions and new possibilities
- [ ] Splits the current flow into modules and evaluates reorder / replace / remove options
- [ ] Lists mature technologies or non-technical levers with maturity labels

### 解法品質
- [ ] Provides at least 3 genuinely different solution types
- [ ] Each solution includes concept, concrete action, why simpler/stabler, and trade-offs
- [ ] Provides one lowest-friction solution that mainly changes UI or process
- [ ] Corrects wrong user assumptions instead of silently following them
- [ ] Ends with an actionable next experiment or pilot

### 維護
- [ ] Evals in `assets/evals/evals.json` reflect realistic prompts
- [ ] Regression gates are defined in `assets/evals/regression_gates.json`
- [ ] Wording stays practical and avoids abstract filler
- [ ] Detailed pattern lists stay in `references/` instead of bloating `SKILL.md`

