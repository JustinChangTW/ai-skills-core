---
name: technical-documentation-writer
description: 在使用者要撰寫、重寫、盤點或補強技術文件時使用。常見觸發像「幫我寫 README」「補 Quick Start」「整理 migration guide」「寫 runbook」。輸出可執行文件；不適用於 PRD、驗收規格或簡報內容規劃。
license: MIT
metadata: {"author":"Allan Yiin","language":"zh-TW","category":"documentation","short-description":"技術文件撰寫、改寫、盤點與品質控管工作流程"}
---

# Technical Documentation Writer

這個 skill 用來把零散的產品知識、repo 現況、操作步驟或既有草稿，整理成可發布、可維護、對目標讀者真的有幫助的技術文件。核心不是把句子寫漂亮，而是先選對文件類型，再補齊前置條件、步驟、驗證方式、錯誤處理與維護資訊，避免寫出「看起來完整但實際不能照做」的文件。

## Purpose

你應可靠地完成四件事：
- 先判斷這份文件主要是 tutorial、how-to、reference 還是 explanation，再決定結構。
- 先盤點現有證據，再撰寫文件；程式碼、現有 docs、CLI help、設定檔、官方文件都算證據。
- 對技術文件加入可執行細節：前置條件、步驟、範例、驗證點、常見錯誤、風險提醒。
- 在交付最終稿時，明示假設、版本範圍、待確認缺口與建議後續文件。

## Scope

### In scope
- README、Quick Start、Getting Started、安裝與設定指南
- 教學文件、操作手冊、使用者指南、任務型 how-to
- API 使用說明、SDK 使用範例、CLI 指令說明的人工整理版
- 故障排除、runbook、FAQ、on-call 操作流程
- migration guide、release notes、貢獻指南、文件盤點與 gap analysis
- 既有技術文件的改寫、重組、補證據、補範例與補維護欄位

### Out of scope
- PRD、產品 spec、需求訪談、驗收條件設計
- 純行銷文案、品牌故事、思想領導長文
- 只靠臆測替不存在的功能、API 或操作流程補文件
- 完全自動生成大型 API reference 且沒有程式碼、schema 或官方來源可驗證
- 法律、醫療、資安合規等高風險內容的最終專業背書

## Primary use cases (2-3)

1) **從 repo 或產品資訊建立入門文件**
- Trigger examples: "幫我寫 README", "整理安裝與快速開始", "幫新同事做 onboarding 文件"
- Expected result: 產出一份讓新讀者能成功完成首次安裝、首次執行或第一個任務的文件，包含前置條件、步驟、驗證與常見失敗。

2) **改寫或補強既有技術文件**
- Trigger examples: "把這份 API 文件重寫清楚", "這份使用手冊太亂了請整理", "幫我補 troubleshooting 與 FAQ"
- Expected result: 保留正確技術資訊，重組資訊架構、簡化語言、補範例與警告，並指出仍待確認的事實缺口。

3) **做文件盤點與規劃**
- Trigger examples: "幫我做 docs audit", "目前文件缺哪些", "規劃使用者文件架構"
- Expected result: 交付文件地圖、優先順序、缺口清單、每份文件的目標受眾與建議模板，而不是直接亂寫一堆文件。

## Workflow overview

1. 先辨識受眾、任務成功條件與文件主類型，必要時用 `Diataxis` 路由。
2. 盤點可用證據：現有文件、程式碼、CLI/help 輸出、設定檔、變更紀錄、官方來源。
3. 建立 doc brief：目標讀者、入口狀態、前置條件、版本範圍、完成後能做到什麼。
4. 依文件類型選模板，先產出結構，再補內容、範例、驗證點與錯誤處理。
5. 用檢查表與 `scripts/doc_quality_audit.py` 做品質審查，補齊缺口。
6. 交付最終稿，同時列出假設、已知缺口與建議的下一份文件。

## Communication notes

- User vocabulary: README、Quick Start、API docs、runbook、tutorial、FAQ、migration guide、docs audit、developer guide
- Avoid jargon: 若使用 Diataxis、progressive disclosure、operator 等詞，必須順手翻成讀者語言，不要把分類名詞當前提。
- Least-surprise rule: 預設讀者想要的是「能照著做」與「知道何時會失敗」，不是華麗敘事；若資訊不足，先標示假設與待確認點，不要假裝完整。

## Routing boundaries

- Neighboring skills / workflows: `spec-organizer` 負責需求/spec；`longform-writing-process` 負責長文論述與多輪評論；`slide-content-planner` 負責簡報；`skill-creator-advanced` 負責 skill 本身的設計與評估。
- Negative triggers: "幫我寫 PRD", "整理驗收條件", "把這段文案寫得更有說服力", "做簡報大綱", "規劃系統開發 spec"
- Handoff rule: 如果核心問題是定義需求與驗收而非說明既有系統，交給 `spec-organizer`；如果主要目標是觀點文章或品牌內容，交給 `longform-writing-process`；如果使用者已指定要做簡報，交給 `slide-content-planner`。

## Language coverage

- Primary language(s): 繁體中文、英文
- Mixed-language trigger phrases: "幫我寫 onboarding doc", "整理 API usage docs", "補一份 troubleshooting guide", "做 docs gap analysis"
- Locale-specific wording risks: 指令、檔名、環境變數、HTTP 欄位與程式碼片段保留原文；敘述與警告可在中文與英文術語並陳，避免誤譯。

## Success criteria

### Quantitative (targets)
- Trigger accuracy: 90% 以上的明顯文件請求應命中
- Tool calls: 一般任務 2-8 次；大型 repo 文件盤點可更高，但需有明確證據價值
- Failures: 不應捏造不存在的功能、參數或步驟；遇到未知處應明示缺口

### Qualitative
- 最終文件可讓目標讀者知道從哪裡開始、怎麼驗證成功、失敗時怎麼處理
- 文件結構穩定、標題清楚、可掃描，命令與範例可直接複製
- 同一份內容未來能維護，會標出版本範圍、適用對象與已知限制

## Instructions

### Step 0: Confirm inputs
- Read the existing conversation/files first; ask follow-up questions only when a wrong assumption would materially change the outcome.
- 至少確認四件事：目標讀者、文件目標、可用素材、版本或環境範圍。
- 若使用者沒講清楚，先用最小風險假設補上並明示，不要立刻停下來追問。

### Step 1: Route the document type before drafting
- 先判斷主文件類型：tutorial、how-to、reference、explanation，必要時再加 README、runbook、migration guide 等外層容器。
- 文件只能有一個主類型；若混合，明示主要與次要類型，避免把教學、參考與概念說明攪在一起。
- 路由規則見 `references/doc-type-routing.md`。

### Step 2: Gather evidence, not guesses
- 優先讀本地證據：repo、現有文件、程式碼、CLI help、設定檔、範例輸出、issue/commit 訊息。
- 若內容涉及外部產品、API、套件版本、政策、價格、規格或其他可能變動的事實，必須查官方來源再寫。
- 若找不到支撐某一步驟的證據，改寫成明確假設或待確認事項，不要補空想細節。

### Step 3: Build a doc brief
- 在寫正文前先整理一份簡短 doc brief：讀者是誰、起始狀態、完成後能做到什麼、前置條件、適用版本、風險與排除項目。
- 若任務是 docs audit，doc brief 要改成文件盤點表：現有文件、缺口、優先順序、建議新增文件。
- 若任務是改寫現有文件，先指出原稿的主要問題：資訊缺口、順序混亂、 jargon 過多、沒有驗證點、沒有 error handling。

### Step 4: Outline using the right template
- 依主文件類型挑模板，先定標題層級與資訊順序，再填內容。模板見 `references/doc-types-and-templates.md`。
- README/Quick Start 應先回答「這是什麼、為誰而寫、如何快速成功一次」。
- Tutorial 應以學習路徑為主；How-to 應以任務完成為主；Reference 應以完整與可查詢為主；Explanation 應以理解背景與取捨為主。

### Step 5: Draft for execution, not decoration
- 每個程序至少要有：前置條件、操作步驟、預期結果、驗證方式；高風險操作再加 rollback 或注意事項。
- 命令、檔案路徑、環境變數、HTTP request/response 範例要可複製，並清楚標出 placeholder。
- API 文件至少補齊：版本範圍、認證方式、參數、成功/失敗範例、限制、常見錯誤。
- Runbook 與 troubleshooting 至少補齊：症狀、可能原因、診斷步驟、修復步驟、升級/通報條件、事後預防。
- Migration guide 至少補齊：破壞性變更、升級順序、相容性、驗證與回退策略。

### Step 6: Finalization and QA
- 用 `references/quality_checklist.md` 逐項檢查：準確性、可執行性、可掃描性、維護性。
- 若有草稿檔案，執行 `python scripts/doc_quality_audit.py path/to/draft.md --type tutorial` 或其他相應類型做快速審查。
- 交付時要附上：文件主類型、使用的主要證據來源、仍待確認的缺口、建議下一份文件或後續維護點。

## Testing plan

### Triggering tests
- Should trigger:
  - "幫我根據這個 repo 寫 README 與 Quick Start"
  - "把這份 API 文件重寫成新手看得懂的版本"
  - "幫我做一份客服後台的操作手冊與 FAQ"
  - "整理 release note 跟 migration guide"
  - "做 docs audit，告訴我目前文件缺哪些"
- Should NOT trigger:
  - "幫我寫 PRD 與驗收條件"
  - "把這篇技術觀點文章潤稿"
  - "做投影片大綱"
  - "想一個產品 slogan"
- Near-miss / confusing cases:
  - "整理架構決策紀錄" 可能是 explanation docs，也可能比較接近 spec，需看任務重點
  - "幫我寫 API 規格" 若是在定義尚未存在的 API，應交給 `spec-organizer`
  - "做 release communication" 若偏外部公告或行銷，不應由本 skill 接手

### Functional tests
- Test case: 從現有 repo 與零散筆記產出 onboarding README
  - Given:
    - repo 有安裝步驟、環境需求與啟動指令，但散落在多個檔案
  - When:
    - 使用者要求寫一份讓新工程師能在 15 分鐘內跑起來的 README
  - Then:
    - 回覆先整理 doc brief，再產出有前置條件、步驟、驗證與 troubleshooting 的 README 草稿

- Test case: 改寫混亂的 API 使用說明
  - Given:
    - 使用者提供一份舊版 API 文件與幾個最新 endpoint 範例
  - When:
    - 要求重寫成新版 API usage guide
  - Then:
    - 回覆會標出版本範圍、缺口與待確認項目，並產出可查詢的章節與 request/response 範例

- Test case: docs audit
  - Given:
    - 現有文件只覆蓋安裝與部分 FAQ
  - When:
    - 使用者要求盤點缺哪些文件
  - Then:
    - 回覆產出文件地圖、優先順序、受眾與建議模板，不會假裝所有文件都已寫完

### Performance comparison (optional)
- Baseline (no skill): 容易直接開寫，混淆文件類型，缺少驗證點與 error handling
- With skill: 先路由類型與讀者，再以證據與模板驅動，文件更可執行、更可維護

### ROI guardrail
- Quality gain must justify extra:
  - Time: 額外盤點與 QA 時間應換來更少返工與更少讀者卡關
  - Tokens: 只有在會改善可執行性與準確性時才擴充範例與背景說明
  - Maintenance burden: 模板與檢查表要能重用，不要把單次偏好寫成僵硬流程

### Regression gates
- Minimum pass-rate delta: +0.10
- Maximum allowed time increase: 45 秒
- Maximum allowed token increase: 7000
- Maximum under-trigger failures: 1 / 10 obvious prompts
- Maximum over-trigger failures: 1 / 10 negative prompts

### Feedback loop
- Common failure signals:
  - 文件看起來完整，但缺少前置條件或驗證方式
  - 把 tutorial、reference、explanation 混成同一份，導致讀者不知怎麼用
  - 直接重寫語句，卻沒有檢查資訊是否過時
  - docs audit 只列主題，沒有受眾與優先順序
- Likely fix:
  - description 補更明確 trigger phrases 與 out-of-scope
  - workflow 補強 doc brief 與證據盤點
  - 在 `references/doc-types-and-templates.md` 補更明確模板
  - 擴增 evals 中的 near-miss 與 mixed-language prompts

## Eval workflow

- Save approved prompts to `assets/evals/evals.json`
- Define release thresholds in `assets/evals/regression_gates.json`
- 若此 skill 與 `skill-creator-advanced` 工具鏈一起維護，可沿用共用 eval workspace 流程準備 paired runs。
- If the environment supports subagents or parallel workers, launch with-skill and baseline runs in the same batch
- After runs complete, aggregate results and generate a review viewer
- 若此 skill 與 `skill-creator-advanced` 工具鏈一起維護，可沿用共用 regression gates 檢查發版門檻。

## Distribution notes

- Packaging: 由宿主或 registry 的標準 SKILL 發佈流程處理；若在本 repo 維護，再使用 repo 根目錄的打包腳本。
- Repo-level README belongs *outside* this skill folder.

## Troubleshooting

- Symptom: 文件內容很完整，但讀者仍不知道先做什麼
- Cause: 沒先決定主文件類型，資訊順序跟任務流程不一致
- Fix: 回到 `references/doc-type-routing.md`，重選主類型並縮小單份文件的目標

- Symptom: 文件語言通順，但操作步驟不可靠
- Cause: 直接依記憶補內容，沒有查 repo、CLI help 或官方來源
- Fix: 回到 Step 2 重做證據盤點，把無法證實的內容降級為假設或待確認

- Symptom: docs audit 結果太空泛
- Cause: 只列主題，沒有定義讀者、任務與優先順序
- Fix: 對每份建議文件都補上受眾、任務、輸入、輸出與建議模板

## Resources

- `references/doc-type-routing.md`: 用 Diataxis 和常見技術文件類型做路由
- `references/doc-types-and-templates.md`: 常見文件模板與段落骨架
- `references/quality_checklist.md`: 發布前品質檢查表
- `references/test_plan.md`: trigger / functional / regression 測試計畫
- `references/source-synthesis.md`: 本 skill 整合的來源與取捨說明
- `scripts/doc_quality_audit.py`: 針對草稿做快速結構審查
