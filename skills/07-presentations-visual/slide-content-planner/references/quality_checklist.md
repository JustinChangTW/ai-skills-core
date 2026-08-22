# Quality checklist

這份 checklist 用來記錄 slide-content-planner 目前是否符合 `skill-creator-advanced` 的 readiness gate 規範。
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
- [ ] 有工具或路由使用規則
- [ ] 有 worked examples / examples 支撐輸出品質

## Common error checks
- [x] 沒有失效的本地引用路徑
- [x] frontmatter / 命名 / description 沒有被 validator 擋下
- [x] 結構與文字格式沒有被 linter 擋下
- [ ] readiness gate 所期待的關鍵區塊已完整具備
- [x] checklist 已與新版 readiness gate 結構對齊

## Skill-specific checks
用這份清單在交付「內容規劃」前做自檢（也可作為後續設計/製作的驗收依據）。

### A. 結構與交付物完整度
- [ ] 有先輸出【信息抽取】（6 欄位齊全：主題/目標行為或觀點/受眾/頁數/主色/比例；缺失以假設值標註）
- [ ] 有輸出【投影片內容規劃】（逐頁，包含：標題、takeaway、支撐點、證據需求、講稿）
- [ ] 有輸出【視覺元素規劃表】（逐頁；每頁至少 1 個視覺化主角）
- [ ] 含封面頁與 Q&A 頁
- [ ] 不含目錄頁（除非使用者明確要求）

### B. 敘事與說服力
- [ ] One-slide one-takeaway：每頁只有 1 個核心訊息
- [ ] 故事線完整（問題/背景→洞見→方案→行動/下一步）
- [ ] 目標行為/觀點改變可被衡量（或至少可被具體描述）
- [ ] 明確列出阻力與反對意見（並在某些頁面設計對應的反駁/化解）

### C. 視覺化與版型多樣性（規劃層）
- [ ] 沒有任何「只有文字」的頁面（至少要有 icon/diagram/chart/table/infographic 模組）
- [ ] 版型不會連續多頁雷同（至少 3 種模組輪替，例如：數據圖表頁/流程頁/對比頁/案例頁）
- [ ] 封面包含明確主視覺（不可只放素面文字）
- [ ] 有規劃視覺動線（底邊指向尖端；避免反向）

### D. 證據與來源
- [ ] 涉及數據/新聞/研究的頁面，規劃中有「資料來源/查證需求」欄位
- [ ] 若需上網查證，列出可執行的查詢關鍵字或來源類型（官方報告/期刊/新聞機構）

### E. 可落地性
- [ ] 規劃的每頁內容足以交給設計/製作人員落地（不需要再猜測）
- [ ] 有標註需要使用者補充的輸入（例如：產品 KPI、客戶案例、內部數據、日期/地區範圍）

---

### Structure (skill packaging)
- [ ] Folder name is kebab-case
- [ ] SKILL.md exists (case-sensitive)
- [ ] YAML frontmatter starts/ends with ---
- [ ] Frontmatter has name + description
- [ ] No < or > in frontmatter
- [ ] No README.md inside skill folder
