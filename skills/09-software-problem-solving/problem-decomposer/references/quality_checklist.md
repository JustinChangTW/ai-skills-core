# Quality checklist

這份 checklist 用來記錄 problem-decomposer 目前是否符合 `skill-creator-advanced` 的 readiness gate 規範。
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
- [x] 有明確 output contract / output shape 要求
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
在發佈這個 skill 前，至少確認下列事項。

### Triggering
- [ ] 明顯的「難題拆解」「WBS/依賴/驗收」「系統性問題拆解」「PoC/Go-No-Go 拆解」查詢會觸發。
- [ ] 單純 bug fix、spec 撰寫、替代解法、Mermaid 作圖不會誤觸發。
- [ ] 中文、英文縮寫混用時仍可判斷是否屬於本 skill。

### Problem framing
- [ ] 有先判斷問題類型，而不是直接套固定框架。
- [ ] 有先區分現象、目標落差、根因假設與對策，沒有把它們混成一層。
- [ ] 有把原問題改寫成成功狀態、In/Out、假設與限制。
- [ ] 有明確說明主框架與輔助框架，沒有把 MECE、WBS、系統思考混為一談。
- [ ] 若使用 issue tree，同一層有一致的分類基準，且區分原因樹、對策樹與工作分解。

### Execution design
- [ ] 每個工作包至少包含目的、輸出、驗收與依賴。
- [ ] 有標出關鍵路徑或可並行工作，不只是列待辦。
- [ ] 若需要多人協作，已補 RACI 或等價責任分派。
- [ ] 若問題高不確定，已補 Baseline、PoC、緩衝或決策門檻。

### System and feedback
- [ ] 系統性問題有補回饋迴路、延遲與槓桿點。
- [ ] 有至少一組追蹤指標，例如 WIP、Cycle Time、返工率或 KR 達成度。
- [ ] 有固定回饋節奏，例如週檢視、雙週調整、月度 PDCA。

### Output quality
- [ ] 最終輸出符合 `references/output-template.md` 的主體結構。
- [ ] 報告能直接轉成待辦、排程、對齊文件或決策會議材料。
- [ ] 有明確列出最先做的 3 件事與待確認事項。

### Maintenance
- [ ] `SKILL.md` 版本號已更新。
- [ ] `assets/evals/evals.json` 包含 should-trigger、should-not-trigger、near-miss。
- [ ] `assets/evals/regression_gates.json` 反映目前門檻。
