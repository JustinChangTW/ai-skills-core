---
name: pptx-maker
description: 在使用者已經有逐頁內容、講稿、模板或 SVG，要真正做成可交付投影片時使用。常見觸發像「套版成 PPTX」「修改既有 deck」「把這批 SVG 組成簡報」。負責製作與交付；不從零規劃故事線或受眾策略。
license: MIT
metadata: {"author":"Allan Yiin","language":"zh-TW","category":"presentation","short-description":"將既有內容規劃落成可交付的投影片與 PPTX 製作流程"}
---

# Pptx Maker

## Purpose

這個 skill 專門處理「投影片製作」而不是「投影片構思」。它會先確認內容是否已足夠進入製作階段，再依可用素材與工具選擇合適的製作路徑，將逐頁規劃轉成 build spec，最後產出可開啟、可檢查、可交付的投影片檔案或明確的製作交付物。

核心目標是避免兩種常見錯誤：
- 一邊製作一邊偷偷重寫簡報邏輯，導致和已核定內容偏離。
- 為了快，直接用截圖或點陣圖把整頁貼回 PPTX，破壞可編輯性與後續維護。
- 沒先看最終播放與列印環境，就把螢幕上好看的設計直接搬去投影現場。

## Scope

### In scope
- 使用者已提供或可從上下文取得：逐頁大綱、講稿、內容規劃表、視覺方向、品牌規範、範本 PPTX、既有簡報、SVG/圖片素材中的至少一部分。
- 根據現況選擇製作路線：從零新建簡報、套用既有模板、修改既有 PPTX、將 SVG 組裝成 PPTX。
- 當使用者明示要指定設計語言時，優先支援 5 種建議風格：瑞士國際字體風格（Swiss Style）、Bento、扁平化設計（Flat Design）、Google Material、Memphis。這只是建議範圍，不具強制性，也不是預設值。
- 將內容規劃整理成逐頁製作規格：版型、層級、視覺元件、素材需求、備註與待補項。
- 產出投影片檔案或可直接交給後續產線的中間產物，並做視覺與結構 QA。
- 在必要時補查工具、格式限制、套件能力與檔案結構，但只查核和製作流程直接相關的關鍵資訊。

### Out of scope
- 從零規劃簡報主題、受眾洞察、說服結構、逐頁故事線。那屬於 `slide-content-planner`。
- 在內容尚未定稿時擅自新增整頁論點、重寫說服策略或重做研究。
- 純文案腦暴、只寫講稿、只整理資料、不做投影片落地。
- 不經使用者同意就把可編輯內容降級成整頁截圖、PNG 或其他不可維護格式。

## Primary use cases

1) **已經有內容規劃，要從零做成新投影片**
- Trigger examples: "幫我把這份逐頁規劃做成 PPTX", "依這個 slide plan 產出投影片", "我內容定了，接下來直接做簡報"
- Expected result: 先選定新建製作路線，再輸出逐頁 build spec、設計系統、投影片成品與 QA 結果。

2) **已有模板或品牌規範，要把內容套成正式 deck**
- Trigger examples: "照這份公司 template 做出簡報", "把規劃內容套進這個 PPTX 範本", "沿用現有品牌樣式做成投影片"
- Expected result: 先盤點模板版型，再做頁面映射、內容替換、素材補位與最終驗證，不亂改模板系統。

3) **修改既有簡報，但只改核定範圍**
- Trigger examples: "把這份既有簡報改成新版內容", "更新第 3 到第 8 頁，不要動其他頁", "補 speaker notes 並修正現有 PPTX"
- Expected result: 只針對指定頁面或指定元素做編修，保留未要求變動的部分，並確保輸出檔沒有損壞。

4) **將既有 SVG 依頁碼組裝成 PPTX**
- Trigger examples: "/svg2pptx", "把這批 SVG 轉成 PPTX", "依頁碼把 SVG 組成簡報"
- Expected result: 先確認頁碼、比例與文字可編輯性，再按順序輸出 PPTX，不用 PNG 回貼整頁替代。

5) **指定採用建議風格之一做成正式 deck**
- Trigger examples: "這份簡報請做成 Swiss Style", "我要 Bento 風格投影片", "請用 Flat Design 做", "這份 deck 套成 Google Material 風格", "做成 Memphis 風格簡報"
- Expected result: 先確認這是視覺語言要求而不是內容重寫需求，再依對應 reference 套用該風格的適用條件、結構規則、QA 與陷阱，不把任何一種風格當作默認答案。

## Workflow overview

1. 先確認是否真的已經進入「製作階段」，內容若未定稿則停止擴寫並交棒。
2. 盤點可用素材與工具，選定最合適的製作路線。
3. 將逐頁內容規劃整理為 slide build spec。
4. 依路線產出投影片，維持可編輯性、版型一致性與範圍控制。
5. 執行視覺與結構 QA，列出缺件、風險與交付內容。

## Communication notes

- User vocabulary: 投影片製作、PPTX、簡報模板、頁面版型、逐頁規劃、講稿、視覺稿、套版、產出成品。
- Avoid jargon: 將 slide master 說成「母片/主版型」，將 layout inventory 說成「模板版型盤點」，將 OOXML 說成「PPTX 解包後的 XML 結構」，不要假設使用者熟悉 PowerPoint 檔案內部格式。
- Least-surprise rule: 預設只把已核定內容落地，不偷改故事線；若素材或資訊不足，就把缺口標出來，不硬補未授權內容。
- Editing rule: 任何修改既有簡報的任務，都要明確寫出影響範圍；沒被要求的頁面、註解、主題與資產不要擅動。
- Style rule: 若使用者只指定某種風格，例如 Swiss、Bento、Flat、Material 或 Memphis，那是視覺執行要求，不代表可以順手改寫故事線或刪掉已核定內容；內容層取捨仍回到 build spec 與已核准規劃。
- Default rule: 本 skill 建議支援 5 種風格，但它們都只是可選解，不是預設值；未被明示指定時，不要自作主張把所有 deck 都做成某一種流行風格。

## Routing boundaries

- Neighboring skills / workflows:
  - `slide-content-planner`: 處理受眾、說服策略、逐頁內容規劃與視覺動線；當內容尚未定稿時由它接手。
  - `longdoc-evidence-reader`: 當來源資料很長、需要先萃取證據或內容再做簡報時先使用。
  - `image-generation`: 當卡在產生主視覺、插圖、封面圖像素材時可局部接手。
- Negative triggers:
  - "幫我規劃一份簡報內容"
  - "幫我想簡報要說什麼"
  - "只要把這段講稿潤一下"
  - "請幫我找資料支持這個論點"
- Handoff rule: 若缺少逐頁內容、受眾目標、預期頁數、品牌/模板/輸出形式等關鍵資訊而會直接影響成品，先回到內容規劃或資料整理，不要假裝已可直接製作。

## Language coverage

- Primary language(s): 繁體中文。
- Mixed-language trigger phrases: PPTX、PowerPoint、deck、template、layout、speaker notes、SVG、slide master、brand deck。
- Locale-specific wording risks:
  - 「做簡報」在中文可能同時代表規劃內容與製作成品，需先判斷使用者現在是在想內容還是在落地製作。
  - 「套版」有時只代表套用視覺樣式，有時也包含改內容；要先界定範圍。

## Success criteria

### Quantitative (targets)
- Trigger accuracy: 至少 90% 的明確「把內容做成投影片」查詢能觸發，且不應搶走純規劃型需求。
- Route selection clarity: 100% 的正式輸出都必須寫出為何選擇該製作路線。
- Slide mapping completeness: 100% 的投影片都能對應到內容來源與版型決策。
- Failures: 目標為 0 個損壞或無法開啟的輸出檔。

### Qualitative
- 不偷改內容意圖，除非明確標示為待確認建議。
- 優先保留可編輯性與可維護性，不把短期方便當成長期技術債。
- 對第一次合作的使用者也能清楚交付：選路理由、缺件、成品、QA 與下一步。

## Instructions

### Step 0: Confirm inputs
- Read the existing conversation/files first; ask follow-up questions only when a wrong assumption would materially change the outcome.
- 在開始任何步驟前，先確認此任務是否已經有適合的工具或既有 skill 可接手；若沒有，再選擇最穩定的人工/程式化流程。
- 至少補齊或從上下文推得以下資訊：
  - 目前是新建 deck、套模板、修改既有 deck，還是 SVG 組裝成 PPTX。
  - 是否已有 `slide-content-planner` 產出的逐頁內容規劃、講稿、視覺元素表，或其他等價輸入。
  - 交付形式：PPTX、SVG、HTML 中間稿、講者備註、縮圖檢查圖。
  - 播放與實體載體：線下投影、會議室螢幕、高亮 LED、錄影回看、是否需要列印 handout。
  - 是否指定設計語言，例如 Swiss、Bento、Flat、Material、Memphis、企業既有品牌、研究簡報既有模板。
  - 模板/品牌/尺寸：約定比例、色彩、字體、版型限制。
  - 素材：圖片、圖表資料、logo、圖示、引用來源、現有簡報。
- 若只有題目或粗略大綱，明確指出尚未進入製作階段，建議先交棒給 `slide-content-planner`。
- 若沒有明示的設計語言，不要擅自把 5 種建議風格中的任何一種當默認風格；先沿用既有品牌系統，或維持與內容目的相符的中性設計。

### Step 1: Choose the production path
- 依 `references/production_paths.md` 選擇最合適的路線，並說明原因：
  - `from-scratch-html`：沒有模板，要從規劃內容建立可編輯的簡報。
  - `template-remix`：已有品牌模板或樣板 deck，要做版型映射與內容替換。
  - `svg-to-pptx`：已有每頁 SVG 或需高控制向量稿，再組裝為 PPTX。
  - `ooxml-surgical-edit`：需要精準修改既有 PPTX 的版面、註解、備註、主題或 XML 層內容。
- 一旦選定路線，先把該路線需要的說明文件、腳本說明或工具文檔完整讀完，不要只看片段就開始做。投影片製作的錯常常不是概念錯，而是漏掉工具限制。
- 執行前先確認當前環境真的具備該路線需要的工具；工具不足時不要硬做，應停止並回報缺少什麼。
- 選路原則：
  - 需要保留模板的原始版型與母片：優先 `template-remix`。
  - 需要大幅新建但仍要可編輯：優先 `from-scratch-html` 或等價的可程式化 PPTX 路線。
  - 已有精準 SVG：優先 `svg-to-pptx`，避免重畫。
  - 只改既有 deck 的指定區塊：優先 `ooxml-surgical-edit` 或其他 scoped edit 路徑。
- 先決定視覺基底再開工：若是線下投影且未確認高亮 LED 且無列印需求，預設採用高對比淺色模式，不把深色模式當默認值。

### Step 2: Normalize the slide build spec
- 使用 `references/slide_build_spec_template.md` 的欄位，為每一頁建立製作規格；至少包含：
  - 頁碼/頁名
  - 內容來源或對應的原規劃頁
  - 核心訊息
  - 版型類型
  - 文案區塊與層級
  - 視覺語言（例如 Swiss / Bento / Flat / Material / Memphis / 品牌模板 / 中性商務）
  - 視覺元件與素材需求
  - 載體假設（投影 / LED / 線上 / 列印）與字級底線
  - 備註、待確認事項、不可修改限制
- 若輸入來自 `slide-content-planner`，優先沿用它的「逐頁內容規劃」與「視覺元素規劃表」，不要重新發明欄位。
- 若單頁內容超過版型負荷，不要硬塞；先拆頁或標記需回頭調整規劃。

### Step 3: Produce slides with scope discipline
- 先套用共通守門規則：
  - 物理環境優先於螢幕美感。線下投影預設使用白/淺灰底 + 深色字的高對比淺色模式；只有在已確認高亮 LED、環境可控且無列印需求時，才採深色模式。
  - 大型實體場地預設標題約 80-120px、內文/副標至少 32-48px；若版面塞不下，先拆頁或減字，不要縮到網頁字級。
  - 投影片表面只放觀眾 3 秒內可讀完的關鍵字、數字與圖表標示；完整解釋留在講者備註或口說。
  - 優先順應既有工具/API/狀態流，不直接改中間狀態檔或用臨時腳本繞過標準流程；若工具鏈不支援，應停止並回報，而不是硬改到不可維護。
- 若已被明示指定某種設計語言，先讀 `references/style_families.md` 判斷它是否屬於本 skill 建議支援的 5 種風格，以及是否真的適合當前 deck。
- 若已確認採用對應風格，再讀其 reference 並把其中規則套進 build spec：
  - `references/swiss_style.md`
  - `references/bento_style.md`
  - `references/flat_design.md`
  - `references/material_design.md`
  - `references/memphis_style.md`
- `from-scratch-html`
  - 先定義整份 deck 的設計系統：比例、邊界、字級階層、色彩與常用模組。
  - 若走 HTML/CSS 路線，將共用色彩、字級、間距抽成共享變數或 tokens，不要每頁各自硬寫。
  - 每頁先做結構，再補細節；不要一開始就塞滿視覺特效。
  - 如使用 HTML 轉 PPTX 類流程，先確保尺寸、可用字體、圖像與漸層處理方式符合工具限制。
- `template-remix`
  - 先盤點模板可用版型與 placeholder 類型，再做對應。
  - 若環境已有 `inventory`、`rearrange`、`replace`、`thumbnail` 類腳本，優先使用這些可重複工具，不要手工亂改。
  - 版型要配合內容數量，不要把 2 個概念硬塞進 3 欄模板。
  - 未被指定的母片、主題與附錄頁不要擅自刪改。
- `svg-to-pptx`
  - 先確認頁碼、比例與資源命名規則。
  - 儘量保留文字與向量資訊；不要為求快整頁輸出成 PNG 回貼。
- `ooxml-surgical-edit`
  - 解包後只動必要檔案，且每批修改後都要立即驗證。
  - 與 slide、notes、comments、theme 相關的變更要保持關聯檔一致。

### Step 4: Validate the output
- 對照 `references/quality_checklist.md` 做 QA，至少檢查：
  - 檔案能否正常開啟。
  - 文字是否溢出、被遮擋或超出安全邊界。
  - 每頁是否保有單一核心訊息，沒有因製作過程把重點沖散。
  - 配色、字級、間距、對齊與視覺模組是否一致。
  - 若是線下投影，弱投影設備下是否仍保有足夠對比；若需要 handout，列印後是否仍可讀。
  - 逐頁表面文字是否維持 3 秒內可掃讀，而不是變成講稿全文。
  - 需要講者備註、註解、來源、logo、頁碼時，是否真的有寫入。
- 若採用特定風格，追加對照對應 reference 的 style QA：
  - `references/style_families.md`
  - `references/swiss_style.md`
  - `references/bento_style.md`
  - `references/flat_design.md`
  - `references/material_design.md`
  - `references/memphis_style.md`
- 若環境支援縮圖、PDF 轉圖或其他預覽工具，務必先做逐頁視覺檢查再交付；若不支援，明確說明未驗證部分。

### Step 5: Deliverables and handoff
- 交付時固定列出：
  - 產出檔案與格式。
  - 採用的製作路線與理由。
  - 未完成或待使用者補件的項目。
  - 已知風險與後續建議。
- 若任務只做到中間產物，也要明說目前交付的是 build spec、模板映射表或待補素材清單，而不是假裝已完成成品。

### Step 6: Skill maintenance checks
- 若此 skill 與 `skill-creator-advanced` 工具鏈一起維護，可先跑共用格式檢查與最小驗證。
- 若此 skill 與 `skill-creator-advanced` 工具鏈一起維護，可再做一次共用最小合規驗證。
- Validate this skill against `references/quality_checklist.md`

## Testing plan

### Triggering tests
- Should trigger:
  - "幫我把這份逐頁內容規劃做成 10 頁 PPTX"
  - "依這個公司模板把簡報套出來"
  - "修改現有簡報第 4 到第 7 頁，不要動其他頁"
  - "把這批 SVG 依頁碼組成簡報"
  - "請把這份 deck 做成 Material 風格"
  - "我要 Memphis 風格的投影片"
- Should NOT trigger:
  - "幫我規劃一份董事會簡報內容"
  - "請幫我想這份簡報的故事線"
  - "把這段講稿改得更有說服力"
  - "整理這份報告的重點給我"
- Near-miss / confusing cases:
  - "幫我做簡報"：需先判斷對方是要規劃內容還是要產出成品。
  - "套版一下"：需判斷只是換視覺樣式，還是連內容替換一起做。
  - "修 PPT"：需確認是單純微調既有檔案，還是其實要重做整份 deck。

### Functional tests
- Test case: 從 `slide-content-planner` 輸出製作新 deck
  - Given: 已有逐頁內容規劃、視覺元素表、品牌色與 16:9 比例。
  - When: 要求將其落成新的 PPTX。
  - Then: 先選定新建製作路線，再產出 slide build spec、投影片成品與 QA 結果，不重寫原先故事線。

- Test case: 套用現有模板
  - Given: 一份 20 頁模板 PPTX 與一份 8 頁核定內容。
  - When: 要求套成正式簡報。
  - Then: 先盤點模板版型，再做映射與內容替換；不把內容硬塞到不適合的欄位數。

- Test case: 精準修改既有 deck
  - Given: 使用者指定只更新第 3 到第 5 頁內容，並新增 speaker notes。
  - When: 要求直接修改現有 PPTX。
  - Then: 只改指定範圍，未指定頁面保持不變，輸出檔案可正常開啟且 notes 存在。

### Performance comparison (optional)
- Baseline (no skill): 容易把規劃與製作混在一起，缺少選路依據，常出現硬塞版型、整頁截圖回貼或修改範圍失控。
- With skill: 先選路、先建規格、再做 QA，能更穩定產出可維護且可交付的簡報。

### ROI guardrail
- Quality gain must justify extra:
  - Time: 若只是 1-2 個文字微調，完整製作流程可能過重，應縮成 scoped edit。
  - Tokens: 不要把所有設計理論與模板知識都塞進主流程；細節放 `references/`。
  - Maintenance burden: 若某一條製作路線極少用且依賴脆弱工具，應明確降級為選用路徑，而不是主流程強依賴。

### Regression gates
- Minimum pass-rate delta: 0.0
- Maximum allowed time increase: 45 seconds
- Maximum allowed token increase: 7000
- Maximum under-trigger failures: 1 per 10 obvious prompts
- Maximum over-trigger failures: 1 per 10 obvious non-trigger prompts

### Feedback loop
- Common failure signals:
  - 明明內容未定稿，卻直接進入製作。
  - 使用了錯誤製作路線，導致輸出不可編輯或很難維護。
  - 修改既有 deck 時影響到不該變動的頁面。
  - 內容能開啟但視覺上溢出、遮擋、比例錯誤。
- Likely fix:
  - 若是 over-trigger，收窄 description 中「做簡報」的語意，改強調「已經有規劃內容，現在要落地製作」。
  - 若是 route 選錯，補強 `references/production_paths.md` 的選路條件與反例。
  - 若常出現溢出版面，補充 build spec 與 QA 規則，而不是靠臨時微調。

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

- Symptom: 做出來的投影片看似完整，但其實偷偷改掉原本故事線或頁面順序。
  - Cause: 沒有先把內容規劃轉成 build spec，就直接進入製作。
  - Fix: 回到 Step 2，逐頁鎖定內容來源、頁面目的與不可變動限制。

- Symptom: 套模板後版面很擠、欄位不對、資訊顯得像硬塞。
  - Cause: 先選模板版型，後想內容，或沒有盤點 placeholder。
  - Fix: 改走 `template-remix` 正規流程，先盤點模板，再依內容數量挑版型。

- Symptom: 匯出的 PPTX 雖然能開，但文字不可編輯或畫面失真。
  - Cause: 為求快把整頁 rasterize，或選錯工具鏈。
  - Fix: 優先使用可保留編輯性的路線；若不得不降級，需明示取捨並徵得同意。

- Symptom: 現場投影後畫面偏灰、後排看不清，或列印 handout 幾乎不能用。
  - Cause: 沒先確認播放載體，就沿用深色背景、小字與螢幕導向的對比設定。
  - Fix: 回到 Step 0/3，以投影與列印條件重設視覺基底、字級底線與留白；必要時退回 `slide-content-planner` 先減字或拆頁。

- Symptom: 為求快直接改中間狀態或繞過標準工具流，結果 deck 無法穩定展示或後續難以維護。
  - Cause: 沒有順應既有 API、狀態機與工具設計模式。
  - Fix: 回到 Step 1/3，改走受支援的製作路徑；若現有工具不足，回報缺口，不用臨時繞路假裝完成。

## Resources

- `references/production_paths.md`：製作路線決策表與守門規則
- `references/slide_build_spec_template.md`：逐頁製作規格模板
- `references/quality_checklist.md`：投影片成品與製作流程 QA 清單
- `references/style_families.md`：5 種建議風格的選型邏輯與導引用法
- `references/swiss_style.md`：瑞士國際字體風格的適用條件、做法、QA 與陷阱
- `references/bento_style.md`：Bento 風格的適用條件、做法、QA 與陷阱
- `references/flat_design.md`：扁平化設計的適用條件、做法、QA 與陷阱
- `references/material_design.md`：Google Material 風格的適用條件、做法、QA 與陷阱
- `references/memphis_style.md`：Memphis 風格的適用條件、做法、QA 與陷阱
- `references/svg2pptx_output.md`：SVG 組裝成 PPTX 的輸出規則
- `references/test_plan.md`：更完整的觸發與功能測試案例
