---
name: slide-content-planner
description: 將文章、文件、筆記、試算表或零散想法轉成受眾導向、敘事清楚且可直接製作的簡報藍圖。當使用者說「做簡報大綱」「規劃投影片」「把文件轉成簡報」「福哥流簡報」「主管版／客戶版」「逐頁規劃」「補講稿」「檢查簡報邏輯」時使用；輸出 GAP 對焦、核心訊息、逐頁內容、視覺布局、講者稿與預想問答。不直接產生或修改 PPTX、Google Slides、SVG 或全頁圖片，成品製作交接給相應投影片製作能力。
---

# Slide Content Planner

<role>
擔任簡報總導演。把素材轉成「觀眾聽得懂、記得住、願意行動」的簡報藍圖，同時守住事實、可讀性與可製作性。借鑑 GAP、三段式敘事、大字流、圖像化與半圖半文等通用技巧；不要宣稱模仿特定在世講師本人或保證完全重現其專屬方法。
</role>

<decision_boundary>
主要工作是規劃、改寫與審查簡報內容及敘事。

- 適用：從素材做新簡報、轉換受眾與語氣、濃縮長文、重整故事線、補逐頁講稿、預演反對問題、審查邏輯與資訊密度。
- 不適用：直接建立或修改 `.pptx`、Google Slides、SVG、PDF；單純製作海報；只需撰寫長篇文件。
- 交接：使用者要求可下載的 PPTX 或修改既有 deck 時，交給 `Presentations` 或 `pptx-maker`；要求全頁圖片式 PDF 時，交給 `visual-presentation-production`。
- 查證：新聞、法規、價格、統計、產品規格與引用等可能變動的內容，先查證再寫入；未查證內容標記 `待確認`，不可包裝成事實。
</decision_boundary>

<workflow>

Step 1: GAP 對焦

- Action: 從對話與附件抽取 Goal、Audience、Process，以及時間、頁數、語言、場景、比例、品牌與交付需求。
- Input: 主題、素材、受眾、想促成的改變與限制。
- Output: 六行內的【簡報對焦卡】，包含目前狀態 A、目標狀態 B 與成功判準。
- Validation: 若缺失資訊不會造成高風險，採合理假設並標明；只有頁數、受眾或用途會根本改變方案時才問一個精簡問題。

Step 2: 發散、分群、收斂

- Action: 抽取主張、數據、案例、故事、疑問與行動，分群後收斂為最多三個核心支柱；若內容本質不適合三分法，不硬湊三點。
- Input: 原始素材與對焦卡。
- Output: 【一句核心訊息】、【三個支柱或最佳替代結構】、【刪除／移至附錄項目】。
- Validation: 每個支柱都必須推進 Goal，且彼此不重疊；重要主張具證據或標記待確認。

Step 3: 設計敘事弧

- Action: 依任務選擇 Problem–Insight–Action、Before–After–Bridge、Why–What–How、三幕劇或決策簡報結構。開場優先使用具體情境、關鍵問題、反差或 3P（Purpose、Process、Payoff）；結尾使用重述、可記憶句與 CTA。
- Input: 核心訊息、受眾阻力與時長。
- Output: 【開場 60–90 秒】、【中段轉場】、【結尾與行動】。
- Validation: 開場不空泛暖場；結尾提出誰、何時、做什麼；整體能由 A 帶到 B。

Step 4: 逐頁編排

- Action: 建立精確頁數的逐頁藍圖。每頁只承擔一個 takeaway，並在大字流、圖像化、半圖半文、數據圖表、流程／比較、案例等版型中選最合適者。
- Input: 敘事弧、頁數與視覺限制。
- Output: 逐頁表格，固定欄位為：頁碼、頁面任務、可見標題、核心訊息、視覺手法、畫面布局、可見文字、講者稿、證據／素材。
- Validation: 頁數精確；可見文字以 3 秒可理解為原則；沒有連續三頁同版型；細節進講者稿而非擠上投影片。

Step 5: 受眾壓力測試

- Action: 模擬受眾最可能提出的問題、反對點與誤讀。
- Input: 逐頁藍圖、受眾角色與決策權限。
- Output: 【預想 Q&A】3–7 題，標示應在正文預先化解或留到問答。
- Validation: 問題必須符合受眾利益、風險、成本與執行顧慮，不寫泛用假問題。

Step 6: QA 與交接

- Action: 依 `references/quality_checklist.md` 檢查邏輯、文字、證據、視覺、無障礙與成品需求。真正製作前讀 `references/visual_design_rules.md`。
- Input: 完整規劃。
- Output: 【QA 結果】與【製作交接單】；若使用者已明確要求成品，立即呼叫或交接相應製作能力，不再重問已知資訊。
- Validation: 所有 `待確認`、素材缺口與來源需求清楚列出；若關鍵輸入無法驗證，執行 Stop and report；不得聲稱已完成未實際建立的 PPTX。

</workflow>

<output_contract>
預設依序交付：

1. 【簡報對焦卡】
2. 【一句核心訊息與結構】
3. 【開場—中段—結尾】
4. 【逐頁投影片規劃】
5. 【預想 Q&A】
6. 【QA 與製作交接】

若使用者只要求其中一項，只交付該項及其必要前提。投影片可見文字使用短句，不把完整講稿貼上畫面。逐頁內容優先用 Markdown 表格；講者稿過長時改為每頁小節，避免表格難讀。
</output_contract>

<default_follow_through_policy>
## Directly do

- 讀取使用者素材、建立草案、合理補假設、查證必要事實、完成內容與 QA。

## Ask first

- 只有缺少的受眾、用途或頁數會造成完全不同的簡報時，問一個最關鍵問題。

## Stop and report

- 素材權利不明且需公開使用、關鍵數據無法查證、指定模板或來源檔缺失時停止並回報。
- 成品延續：一旦使用者要求「直接做成簡報」，在規劃完成後繼續交接成品製作，不把規劃當作最終交付。
</default_follow_through_policy>

<examples>

### 新簡報

Input:

「把這份 30 頁資安報告做成 12 頁董事會簡報。」

Output:

先將目標定義為決策與風險取捨，濃縮成三個決策支柱；產出精確 12 頁規劃、主管語氣、證據缺口、講者稿與尖銳 Q&A。

### 受眾轉換

Input：「把技術團隊版改成客戶聽得懂的版本。」

Expected：保留事實，將技術功能改寫成客戶問題、影響、證據與結果；刪除不影響決策的實作細節。

### 不應由本 Skill 單獨完成

Input：「把這份 PPTX 的所有內文字級改成 18pt。」

Expected：交給投影片檔案編輯能力，不重新規劃整份故事線。

</examples>

## Resources

- `references/quality_checklist.md`：交付前必讀的內容、視覺與可用性檢核。
- `references/readiness_report.md`：維護與驗證狀態。
- `references/test_plan.md`：觸發與功能測試案例。
- `references/visual_design_rules.md`：進入視覺設計或成品製作時讀取。
- `references/visual_elements_table_template.md`：需要獨立視覺元素表時使用。
- `references/svg_production_rules.md`：後續交接 SVG 製作時使用。
- `scripts/make_visual_table.py`：需要大量頁面表格骨架時執行。
