# Production Paths

這份文件用來決定「已經有內容之後，該怎麼把它做成投影片」。

先問四件事：
- 有沒有既有模板或現成 deck？
- 產出目標是新建 PPTX、修改既有 PPTX，還是把 SVG 組成簡報？
- 需要保留多少可編輯性？
- 目前環境有哪些工具真的可用？

## Route 1: `from-scratch-html`

### Use when
- 沒有既有模板，或模板限制太多，不適合直接套版。
- 已經有逐頁內容規劃，需要新建一份可編輯的簡報。
- 可使用 HTML 轉 PPTX、PptxGenJS 或等價的程式化產線。

### Typical workflow
1. 完整閱讀該工具鏈的 HTML/CSS/PPTX 相關說明。
2. 定義 deck 的比例、邊界、字級與視覺系統。
3. 逐頁建立結構化稿面。
4. 用程式化方式產出 PPTX。
5. 產出縮圖或預覽，檢查溢出與對齊。

### Guardrails
- 先建立整份 deck 的設計系統，不要每頁各寫一套。
- 若工具對字體、漸層或 icon 有限制，先確認替代做法。
- 不要在同一頁同時塞過多 layout 實驗，先求穩定與可讀。

## Route 2: `template-remix`

### Use when
- 使用者提供品牌模板、既有 deck、母片規範或版型庫。
- 目標是沿用既有視覺系統，而不是重新發明整份視覺語言。

### Typical workflow
1. 完整閱讀模板相關工具說明，特別是 inventory / rearrange / replace / thumbnail 類流程。
2. 盤點模板的可用版型與 placeholder 類型。
3. 將逐頁內容映射到最合適的模板頁。
4. 複製、重排、替換內容與素材。
5. 檢查對齊、欄位數與字量是否匹配。

### Guardrails
- 先數內容，再選版型，不要先選漂亮版型再硬塞內容。
- 模板若只有 2 欄版，不能假裝可無痛容納 4 個並列概念。
- 除非使用者要求，否則不要改動母片、主題與未使用的版型。

## Route 3: `svg-to-pptx`

### Use when
- 已有逐頁 SVG，或視覺控制需求高到必須先做向量稿。
- 產線允許用 SVG 作中間格式再輸出為 PPTX。

### Typical workflow
1. 先確認所用轉換工具的 SVG 支援限制。
2. 確認頁碼、尺寸比例與資源命名。
3. 逐頁檢查 SVG 是否對應正確內容。
4. 依頁碼順序組裝為 PPTX。
5. 檢查字型、向量、疊圖與比例是否正確。

### Guardrails
- 不要把 SVG 再整頁轉成 PNG 回貼，除非使用者明確接受不可編輯。
- 若文字可保留為向量或可編輯元素，優先保留。
- 匯出前先確認每頁尺寸一致。

## Route 4: `ooxml-surgical-edit`

### Use when
- 需要修改既有 PPTX 的指定頁面、speaker notes、comments、theme 或其他 XML 細節。
- 任務範圍明確，且不應重做整份 deck。

### Typical workflow
1. 完整閱讀 OOXML 結構與驗證規則。
2. 解包 PPTX。
3. 只修改必要的 slide / notes / comments / theme 檔案。
4. 每一批修改後立刻驗證。
5. 回包並再次開啟檢查。

### Guardrails
- 一次只做一批可驗證修改，避免累積錯誤到最後才發現。
- 任何關聯檔變更都要成對處理，例如 slide 與 rels、notes 與對應 slide。
- 未被要求的頁面不要順手整理或重命名。

## Escalate or stop when

- 內容還沒定稿，但使用者以為可以直接製作。
- 缺少核心素材，會導致大量內容需要臆測。
- 可用工具無法支援所選路線。
- 使用者要求維持可編輯性，但目前唯一可行方式只剩整頁 rasterize。
