# Quality checklist

這份 checklist 用來記錄 technical-documentation-writer 目前是否符合 `skill-creator-advanced` 的 readiness gate 規範。
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
在打包或交付技術文件前，用這份清單做最後審查。重點不是文筆，而是準確、可執行、可維護。

### 1. Reader fit

- [ ] 已明確寫出目標讀者與入口狀態
- [ ] 已選定主文件類型：tutorial、how-to、reference、explanation
- [ ] 文件目標單一且清楚，沒有把多種文件硬塞在同一份
- [ ] 標題與段落順序符合讀者完成任務的自然流程

### 2. Accuracy and evidence

- [ ] 所有關鍵步驟都可追溯到 repo、現有文件、官方來源或使用者提供資料
- [ ] 涉及版本、外部 API、工具行為或會變動的事實時，已做最新查核
- [ ] 沒有捏造不存在的功能、指令、路徑、參數或畫面
- [ ] 無法確認的地方已標成假設、限制或待確認事項

### 3. Executability

- [ ] 前置條件、權限、依賴、環境限制寫清楚
- [ ] 每個操作程序至少有步驟、預期結果與驗證方式
- [ ] 命令與程式碼片段可直接複製，placeholder 清楚標示
- [ ] 高風險動作有警告、回退方式或升級通報條件
- [ ] 常見失敗、錯誤訊號或排查方向至少提一次

### 4. Scannability

- [ ] 文件能快速掃描，標題清楚，列表與表格只用在真的有助閱讀時
- [ ] 第一屏就回答「這份文件適合誰」「能解決什麼」
- [ ] 範例、警告與注意事項不被埋在長段落裡
- [ ] 中英混用術語已保持一致，不會一詞多譯

### 5. Maintainability

- [ ] 適用版本、適用角色與已知限制有寫出來
- [ ] 若屬於 docs set，已說明與其他文件的分工或連結
- [ ] docs audit 結果有優先順序，而不是只有願望清單
- [ ] 文件未來變更時，維護者知道要更新哪些章節

### 6. Skill packaging

- [ ] Folder name is kebab-case
- [ ] `SKILL.md` exists and frontmatter is valid
- [ ] Frontmatter has `name` and `description`
- [ ] No angle brackets appear in frontmatter
- [ ] No `README.md` lives inside the skill folder
- [ ] Evals are saved in `assets/evals/evals.json`
- [ ] Regression gates exist in `assets/evals/regression_gates.json`
