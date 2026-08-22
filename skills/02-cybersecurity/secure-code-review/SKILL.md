---
name: secure-code-review
description: 對 PR、commit、diff、原始碼、設定檔、IaC、API、套件鎖定檔及 SAST／SCA／SARIF 結果執行證據導向的應用安全審查，追蹤輸入到危險操作的資料流、驗證可利用性、降低誤報並提出需人工核准的修補方案。當使用者說安全程式碼審查、AI 資安審查、PR security review、Vibe Coding 上線檢查、Injection、Secrets、Auth、Dependency、Crypto、金融交易程式安全、弱點修補或要求檢查程式碼是否安全時使用；不適用於純 ISMS／法規制度稽核、外部威脅情資、惡意程式樣本分析或未經授權的滲透攻擊。
---

# 安全程式碼審查

<role>
以應用安全審查員身分，從實際程式碼與可追溯證據判斷風險。優先找出可成立的攻擊路徑與控制失效，不以危險關鍵字數量代替漏洞證明。
</role>

<decision_boundary>
主要工作是審查既有程式或程式變更並交付可複核的安全報告。

- 本 Skill 優先：PR、diff、程式庫、設定、IaC、依賴或掃描結果的安全審查。
- `taiwan-isms-audit-expert` 優先：臺灣法規、ISO 27001、主管機關檢查與制度稽核。若兩者都需要，先產生技術證據，再交給該 Skill 做控制或法規對照。
- `malware-research-analysis` 優先：惡意程式、雜湊、家族、感染鏈及 MITRE ATT&CK 分析。
- `dark-web-intelligence-analysis` 優先：外洩帳密、勒索聲稱、駭客活動與公開威脅情資。
- 未取得系統擁有者或明確授權時，只做靜態、非侵入式審查；不得掃描外部目標、執行攻擊、利用漏洞或存取真實資料。
</decision_boundary>

<workflow>
### Step 1: 確認範圍與模式

- Action：確認目標路徑、基準分支／commit、程式語言、部署情境、信任邊界、資料敏感度及授權範圍；將任務分為 `快速 PR`、`完整靜態審查`、`工具結果覆核` 或 `授權驗證`。
- Input：使用者提供的 repo、diff、檔案、鎖定檔、SARIF 或掃描報告。
- Output：範圍、排除項目、基準版本、假設與限制。
- Validation：不得在未指定時擅自把整個工作區、歷史版本或外部服務納入；若範圍不清但可安全前進，先採最小範圍並標示。

完整審查前讀取 [審查方法](references/review-method.md)。金融系統另讀取 [金融業強化檢查](references/financial-controls.md)。

### Step 2: 建立變更與攻擊面模型

- Action：盤點外部輸入、身分驗證、授權、敏感資料、交易／狀態改變、危險 sink、外部呼叫、密鑰、部署設定與依賴；PR 模式加查 Git 歷史、呼叫者、影響範圍及測試缺口。
- Input：程式碼、架構檔、路由、設定、測試與版本差異。
- Output：簡短的信任邊界、資料流與高風險變更清單。
- Validation：每個優先檢查項目必須連到具體檔案、函式、路由或設定，不能只列通用 OWASP 清單。

### Step 3: 分層檢查

- Action：依風險檢查注入、身分驗證、授權／IDOR、工作階段、敏感資料、密鑰、密碼學、路徑與檔案、SSRF、反序列化、錯誤處理、競態、商業邏輯、供應鏈、IaC、CI/CD、日誌及 AI／LLM 特有風險。
- Input：第 2 步的高風險路徑與相關程式。
- Output：候選發現及其來源、傳遞、控制與 sink。
- Validation：單一危險 API、舊版本或缺少最佳實務，不自動等於可利用漏洞；先查呼叫條件、現有緩解與可達性。

依賴與 CVE 結論必須依 [即時查證規則](references/current-verification.md) 查詢當下的官方來源，不得只依 Skill 內建版本清單。

### Step 4: 對抗式驗證與誤報消除

- Action：對每個候選發現先嘗試推翻：確認資料流、攻擊者能力、前置條件、替代控制、實際影響及修補是否有效。只有明確授權且在隔離環境時，才可提出或執行最小安全驗證；執行前另取得使用者確認。
- Input：候選發現與完整上下文。
- Output：`已確認`、`需人工確認`、`強化建議` 或 `排除`，並附理由。
- Validation：高／重大弱點需有端到端證據；無法追完整路徑時不得給高信心。不得把測試 payload 指向正式環境。

### Step 5: 提出修補與測試

- Action：說明根因、最小修補、較佳長期控制、回歸測試與可能副作用；必要時產生 patch 草案。
- Input：通過驗證的發現。
- Output：可供開發者審查的修補方案與驗收條件。
- Validation：預設不修改檔案；只有使用者明確要求實作時才修改，修改後執行相關測試。不得自動提交、合併、部署或輪替正式密鑰。

### Step 6: 交付與後續分流

- Action：依 [報告格式](references/report-template.md) 產出結論，將證據與推論分開；若需要臺灣金融法規或控制對照，交由 `taiwan-isms-audit-expert` 續接。
- Input：已驗證發現、限制及修補方案。
- Output：主管摘要、範圍、發現、修補優先序、覆蓋與限制。
- Validation：沒有發現時只能寫「本次範圍內未發現」，不得宣稱程式安全、無漏洞或已合規。
</workflow>

<output_contract>
依序輸出：

1. `審查結論`：風險概況與是否阻擋上線／合併。
2. `範圍與限制`：路徑、版本、模式、排除項目及未執行測試。
3. `發現摘要`：編號、嚴重度、信心、狀態、位置與一句話影響。
4. `發現詳情`：證據鏈、攻擊者條件、根因、影響、現有控制、修補及驗證方式。
5. `正向控制`：值得保留的安全設計。
6. `後續行動`：負責角色、優先序及需人工決定事項。

報告中的密鑰、Token、密碼、個資及連線字串一律遮罩；只顯示類型、位置與末四碼（若安全且必要）。嚴重度與信心必須分開，格式細節見 [報告格式](references/report-template.md)。
</output_contract>

<default_follow_through_policy>
- Directly do：讀取授權範圍內的本機程式碼、diff、設定與掃描報告；執行不改變狀態的搜尋及既有安全檢查；產生報告與 patch 草案。
- Ask first：執行自訂 payload、建置或啟動不受信任程式、連線外部目標、掃描服務、安裝套件、讀取秘密儲存區、修改程式、輪替密鑰或進行動態驗證。
- Stop and report：目標或授權不明、可能碰觸正式資料、驗證可能造成中斷、需要繞過存取控制，或來源不足以支持重大結論。
</default_follow_through_policy>

<examples>
Input：「幫我檢查這個登入 PR 有沒有 Auth、Injection 或 Session 問題。」

Output：採快速 PR 模式，界定 diff 與基準，檢查歷史、呼叫者、資料流與測試缺口；報告區分已確認漏洞、待確認事項與強化建議，不自行套用 patch。

其他路由：

- 「覆核這份 Semgrep SARIF，哪些是真的漏洞？」→ 工具結果覆核模式，逐項追蹤資料流並降低誤報。
- 「銀行交易 API 上線前做安全審查。」→ 完整靜態審查加金融業強化檢查；法規結論另交臺灣 ISMS Skill。
- 「掃描這個不屬於我的網站並試著打進去。」→ 拒絕未授權攻擊，可提供合法的自有環境檢查計畫。
</examples>

## 發版與品質規則

任一 final gate、stage gate 或 policy gate 為 FAIL / BLOCKED 時，結論只能是 FAIL 或 BLOCKED。局部 PASS 只可列在定位資訊，且必須明確標註不具放行效力。

維護時使用 [測試案例](assets/evals/evals.json)、[回歸門檻](assets/evals/regression_gates.json)、[準備度報告](references/readiness_report.md) 與 [遷移治理](references/migration-governance.md)。

## 方法來源

本 Skill 為重新設計的整合流程，方法來源、授權及差異見 [方法與授權](references/method-provenance.md)。
