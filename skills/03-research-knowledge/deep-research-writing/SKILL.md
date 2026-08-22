---
name: deep-research-writing
description: 執行不限領域的跨來源深度研究，主要工作只有把分散證據整合成可追溯的研究成品。當使用者說「深入研究」「幫我找完整資料」「比較各方證據」「做文獻回顧」或需要多來源回答複雜問題時使用。不要用於單一事實快查、只摘要一份文件、純文案潤稿或已由特定領域 Skill 完整處理的任務；成功輸出須區分事實、推論、爭議與未知並附原始來源。
version: 2026.8.15
---

# 深度研究與證據寫作

把開放題目轉成可重現的研究流程及有證據支撐的成品。研究主題不限領域；依問題選擇資料來源與證據標準，不把單一資料庫當成全部世界。

## Single responsibility

- Primary job: 完成跨來源、可追溯的研究，並把證據寫成符合受眾需求的成品。
- Not this skill's job: 單頁摘要、一般潤稿、單一即時事實、直接投資／醫療／法律決策，或代替領域專業判斷。
- Split / handoff rule: 需要專業判準時組合領域 Skill；需要 arXiv 預印本時交給 `arxiv-research`；需要超長檔案證據時交給 `longdoc-evidence-reader`；完成研究後若只要語氣修訂，再交給 `humanize-text`。

<role>
擔任跨領域研究設計者、來源查核者與證據型寫作者。優先追原始來源，主動找反證，保留時間截點及不確定性，不以流暢文字掩蓋證據缺口。
</role>

<decision_boundary>
Use when:
- 問題需要多來源蒐集、比較、交叉查證或形成完整論證。
- 使用者要研究報告、文獻回顧、白皮書、調查文章、競品／產業分析或歷史回測。
- 研究主題跨學術、政策、科技、商業、歷史、人文、教育、生活或其他領域。

Do not use when:
- 一個權威來源即可回答的簡單查詢。
- 只需閱讀或摘要使用者提供的一份短文件。
- 使用者只要創作、改寫、翻譯或排版，沒有證據研究需求。
- 任務要求偽造資料、引用、訪談、經驗或規避合法存取限制。

Inputs:
- 研究問題或想了解的主題；可選提供用途、受眾、地區、時間截點、篇幅、指定或禁用來源。

Successful output:
- 明確研究範圍、可追溯來源、證據分級、相反證據、限制、結論及引用；資訊不足時呈現未知而非補寫。
</decision_boundary>

## Primary use cases

1. **探索型研究**：例如「深入研究某項新科技可能造成的影響」。產出研究地圖、關鍵證據、爭議與後續問題。
2. **比較與決策研究**：例如「比較幾種方案的成本、風險與證據」。產出一致口徑的比較矩陣及條件式建議。
3. **證據型長文**：例如「把資料寫成研究報告或白皮書」。產出有引用、限制與結論強度標示的完整文章。

## Routing boundaries

- `arxiv-research`: 找、讀、核實 arXiv 論文；本 Skill 負責把學術證據與其他來源整合。
- `longdoc-evidence-reader`: 從超長 PDF 或大型資料集回收證據；本 Skill 負責研究設計與綜合。
- `longform-writing-process`: 已有可靠素材、主要需求是長文起草與修訂時由它接手。
- 領域 Skills: 金融、資安、臺灣法規、房市或財報的專業判準優先交由相應 Skill，本 Skill組織跨來源證據。

## Host / portability targets

- Primary hosts: ChatGPT Work、Codex。
- Secondary hosts: 支援 Agent Skills 的環境；無法使用同名工具時改用等價的唯讀搜尋、開頁及檔案工具。
- Core portable surface: `SKILL.md` 加參考文件，不依賴帳號、MCP或秘密金鑰。
- Mutable state: 研究筆記與產出放在任務工作區，不寫入 Skill 目錄。

<workflow>
Step 0: 界定研究任務
- Action: 從對話推斷研究問題、用途、受眾、地區、時間截點、深度及交付格式；只有缺失會實質改變研究時才提問。
- Input: 使用者問題與既有材料。
- Output: 一段研究任務書及3–7個子問題。
- Validation: 子問題共同服務同一主問題；列明範圍外事項及截止日。

Step 1: 設計來源策略
- Action: 依 `references/source-strategy.md` 選擇至少兩種合適來源類型，優先原始來源，建立關鍵字、同義詞、語言、納入及排除條件。
- Input: 研究任務書與子問題。
- Output: 搜尋計畫與來源優先序。
- Validation: 不以新聞轉述取代可取得的原始文件；不為湊數加入低相關來源。

Step 2: 蒐集與建立證據帳本
- Action: 搜尋、開啟並閱讀來源，逐項記錄主張、來源、日期、版本、原文位置、支持或反駁方向及限制。
- Input: 搜尋計畫與取得的資料。
- Output: 證據帳本及來源清單。
- Validation: 每個關鍵主張都有來源；直接引用不超出必要範圍；無法取得全文時明確標記。

Step 3: 查核與分級
- Action: 依 `references/evidence-quality.md` 評估來源層級、獨立性、時效、研究設計、利益衝突與一致性；主動搜尋反證及替代解釋。
- Input: 證據帳本。
- Output: 已核實事實、摘要支持、合理推論、爭議及未知項目。
- Validation: 兩個轉載同一來源不算兩份獨立證據；數字口徑、基期、地區與時間一致。Stop and report：若關鍵來源不可追溯或證據不足以安全形成結論，停止擴寫並回報缺口。

Step 4: 綜合與形成結論
- Action: 對每個子問題比較支持與反對證據，標示結論強度，找出因果與相關混淆、樣本偏差及資料缺口。
- Input: 分級後證據。
- Output: 論證地圖、比較矩陣或事件時間線，以及條件式結論。
- Validation: 結論強度不高於證據強度；推論必須說明推導，未知不得改寫成事實。

Step 5: 撰寫與品質檢查
- Action: 依受眾與格式撰寫成品；逐項核對人名、日期、數字、引用、連結、版本、反方觀點及研究限制。
- Input: 綜合結果與交付要求。
- Output: 符合 `<output_contract>` 的研究成品。
- Validation: 所有重要主張可追溯；來源靠近所支持的句子；明列查詢截止日與未解問題。
</workflow>

<output_contract>
依序輸出：
1. `研究結論`：直接回答主問題，標示信心與適用條件。
2. `研究範圍與方法`：時間截點、地區、搜尋方向及納入／排除規則。
3. `主要證據`：按子問題呈現事實、證據強度、反證與來源。
4. `綜合分析`：比較、因果鏈、替代解釋或研究缺口。
5. `限制與未知`：無法核實、資料偏差及可能改變結論的條件。
6. `來源`：直接連向原始頁面；需要正式報告時使用一致引用格式。

可依任務加入表格、時間線或證據矩陣，但不得用視覺形式掩蓋來源。簡短研究可合併第2至4節，仍須保留限制與來源。
</output_contract>

<tool_rules>
- 即時、易變、利害重大或使用者要求查證的資訊必須上網核實。
- 優先官方文件、原始資料、學術正文及第一手聲明；技術問題優先官方文件與研究論文。
- 只在必要時使用登入、付費資料庫或大量爬取；涉及帳號、資料外送或費用先取得同意。
- 不繞過付費牆、robots、存取控制或網站條款；不可取得全文時使用合法摘要並標記限制。
- 不把使用者內部文件、個資或機密傳到外部服務，除非使用者明確授權且工具資料流透明。
</tool_rules>

<default_follow_through_policy>
- Directly do: 界定問題、唯讀搜尋、來源查核、證據分級、分析及撰寫草稿。
- Ask first: 登入外部帳號、購買資料、啟用爬蟲／MCP、上傳內部資料、發布、投稿、寄信或寫入外部系統。
- Stop and report: 來源不可追溯、證據不足以支持要求的結論、研究要求違法存取、或高風險決策缺少必要專業證據。
</default_follow_through_policy>

## Gate 優先規則

- 任一 final gate、stage gate 或 policy gate 為 FAIL / BLOCKED 時，結論只能是 FAIL 或 BLOCKED。
- 局部 PASS 只可列在定位資訊，且必須明確標註不具放行效力。

<examples>
Example 1
Input:
- 「研究生成式 AI 對高中生學習的影響，正反證據都要，寫成家長看得懂的報告。」
Output:
- 界定年齡與時間截點，查學術研究、教育機構資料與反方證據，區分學習成效、動機、依賴及隱私，最後提出條件式結論、限制與來源。

Example 2
Input:
- 「幫我整理這封 Email，語氣自然一點。」
Output:
- 不觸發；交給文字潤飾能力，因為不需要跨來源研究。
</examples>

<model_notes>
- GPT-style models: 明確遵守證據帳本、分級及逐項 QA，不省略反證搜尋。
- Reasoning models: 可自行調整搜尋路徑，但不得改變來源優先、查證及輸出契約。
- Multi-turn split: 大型研究先交付研究計畫與初步證據，再完成綜合與寫作；每階段保留截止日及未解問題。
</model_notes>

## Testing plan

觸發與功能案例位於 `assets/evals/evals.json`；發布門檻位於 `assets/evals/regression_gates.json`；Skills 介面圖示位於 `assets/icon.svg`。建立或改版後必須執行結構、語意、引用、eval coverage及 stage gate，結果記錄於 `references/readiness_report.md`。重新命名、淘汰、合併或拆分時遵守 `references/migration-governance.md`。
