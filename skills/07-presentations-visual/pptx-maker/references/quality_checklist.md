# Quality checklist

這份 checklist 用來記錄 pptx-maker 目前是否符合 `skill-creator-advanced` 的 readiness gate 規範。
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
- [x] 有明確 default follow-through policy / ask-first 邊界
- [x] 有工具或路由使用規則
- [ ] 有 worked examples / examples 支撐輸出品質

## Common error checks
- [x] 沒有失效的本地引用路徑
- [x] frontmatter / 命名 / description 沒有被 validator 擋下
- [x] 結構與文字格式沒有被 linter 擋下
- [ ] readiness gate 所期待的關鍵區塊已完整具備
- [x] checklist 已與新版 readiness gate 結構對齊

## Skill-specific checks
## Pptx Maker Quality Checklist

在發版、驗收或實際拿這個 skill 跑任務前，用這份清單檢查它是否仍然守住邊界與產出品質。

### Triggering
- [ ] 明確的「把已規劃內容做成投影片」查詢會觸發。
- [ ] 只有內容規劃、受眾分析、講稿潤飾的查詢不會誤觸發。
- [ ] 混合語言用語如 `PPTX`、`template`、`deck`、`speaker notes` 仍能正確路由。

### Boundary management
- [ ] 有清楚說明何時應交棒給 `slide-content-planner`。
- [ ] 沒有把「做簡報」泛化成從構思到製作全部都接。
- [ ] 修改既有 deck 時有要求明確範圍，不會擅改無關頁面。

### Route selection
- [ ] 每次正式輸出前都會先說明選擇哪條製作路線及理由。
- [ ] 路線與輸入相符：新建 deck、模板套用、SVG 組裝、既有 PPTX 編修不會混淆。
- [ ] 工具不足時會停下並回報，不會假裝可以完成。

### Production quality
- [ ] 每一頁都有對應的內容來源或 build spec。
- [ ] 成品保留合理的可編輯性，沒有默默把整頁點陣化。
- [ ] 版型、字級、間距與視覺層級一致。
- [ ] 文字沒有溢出、裁切、重疊或超出安全邊界。
- [ ] 必要時已處理 speaker notes、來源、logo、頁碼、圖表標註等交付要求。

### Deliverables
- [ ] 有明確列出輸出檔案、採用路線、未完成項與風險。
- [ ] 若目前只產出中間稿，也有誠實標註為 build spec、模板映射表或待補素材清單。

### Skill maintenance
- [ ] `SKILL.md` 沒有模板占位文字。
- [ ] `assets/evals/evals.json` 與 `assets/evals/regression_gates.json` 可被讀取。
- [ ] 沒有留下無用 placeholder script 或與技能無關的檔案。
