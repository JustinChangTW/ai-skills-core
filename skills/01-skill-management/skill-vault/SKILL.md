---
name: skill-vault
description: 將個人或團隊的 Agent Skills 分類、匯出、檢查並安全備份到私人 GitHub，且驗證遠端內容可還原。當使用者說「備份我的 Skills」「更新 ai-skills-core」「確認 GitHub 備份完整」「還原 Skills」或要制定 Skill 備份規則時使用。Do not use for 建立／優化 Skill 內容、一般程式專案備份或搜尋新 Skill。成功結果是沒有憑證外洩、清單與校驗碼一致、遠端抽查成功，並留下可追溯的備份報告。
version: 2026.8.22
metadata:
  author: Justin Chang
  language: zh-TW
  category: ops
  short-description: Skills 私人 GitHub 備份、驗證與還原管家
---

# Skill Vault｜Skills 備份管家

這個 Skill 管理 Agent Skills 從本機來源到私人 GitHub 的可驗證備份生命週期。它保留完整 Skill 資源、建立人類可讀導覽、阻擋敏感資料、驗證遠端版本，並確保備份實際可還原。

## Single responsibility

- Primary job: 建立、更新、驗證與還原一套可追溯的 Skills GitHub 備份。
- Not this skill's job: 撰寫或優化領域 Skill、搜尋外部 Skill、備份一般程式專案、管理 GitHub 帳號與權限政策。
- Split / handoff rule: Skill 內容需建立或修改時交給 `skill-creator`；需搜尋新能力時交給 `capability-evolver`；本 Skill 只在內容確定後負責保存與驗證。

<role>
你是 Skills 備份與復原管理員。以資料保全、最小權限、可還原性及清楚導覽為核心，先檢查再發布，絕不把「已複製」誤稱為「已完成備份」。
</role>

<decision_boundary>
Use when:
- 使用者要把一個或多個 Skills 備份、更新或移轉到 GitHub。
- 使用者要檢查備份是否完整、是否含敏感資料、是否能還原。
- 使用者要整理 Skills 分類、目錄、README、校驗碼與備份規則。

Do not use when:
- 使用者要建立、改寫、評估或安裝 Skill，而不是備份既有成品。
- 目標是一般程式碼、照片或文件備份，且沒有 Agent Skills 結構。
- 使用者只詢問 Git 或 GitHub 的一般操作方式。

Inputs:
- Skills 來源位置或可列出的 Skill 集合。
- 目標 GitHub repository、分支與公開性；預設要求 private。
- 既有分類規則、保留範圍及使用者對遠端寫入的明確授權。

Successful output:
- 每個 Skill 的核心檔案與相依資源均存在，分類及導覽可用。
- 機密掃描、結構檢查、清單與 SHA-256 校驗通過。
- 遠端 commit 可讀，抽查 Skill、分類 README、腳本及二進位素材成功。
- 提供版本識別、檔案／Skill 數量、驗證結果、例外與還原方式。
</decision_boundary>

## Primary use cases

1. **首次建立備份庫**
   - Trigger examples:「把我的 Skills 備份到私人 GitHub」「建立 Skills 備份庫」
   - Required inputs: Skills 來源、目標 repository；分類可由現況推導後供使用者確認。
   - Expected result: 私人備份庫、分類、總目錄、每類與每 Skill 說明、校驗碼及驗證工具。
2. **增量更新**
   - Trigger examples:「更新 Skills 備份」「把新 Skill 也放進 ai-skills-core」
   - Required inputs: 既有備份庫與新增／異動來源。
   - Expected result: 僅更新必要內容，保留既有分類與歷史，遠端抽查通過。
3. **完整性檢查與還原**
   - Trigger examples:「確認 GitHub 備份完整」「從 GitHub 還原我的 Skills」
   - Required inputs: repository、版本或分支、還原目標位置。
   - Expected result: 校驗報告或隔離目錄中的可用還原副本；不覆蓋現用 Skills。

## Routing boundaries

- `skill-creator`: 決定 Skill 的指令品質、結構與行為；完成後由本 Skill 備份。
- `capability-evolver`: 搜尋、比較、安裝或更新外部 Skills；安裝完成後由本 Skill 備份。
- 一般 Git 工具: 執行底層版本控制；本 Skill負責 Skills 專屬分類、排除、驗證與復原規則。

## Host and storage

- Primary hosts: Codex、支援 Agent Skills 與 GitHub 工具的 ChatGPT 環境。
- Secondary hosts: Claude Code、其他能讀取 `SKILL.md` 的 Agent 環境；需依其安裝路徑調整還原位置。
- Core portable surface: `SKILL.md`、`agents/`、`references/`、`scripts/`、`assets/`、schemas、policies、examples 及備份用 README。
- Mutable state: 暫存快照、認證與執行紀錄必須放在 workspace、系統憑證庫或暫存區，不得放進 Skill 或 repository。

<workflow>
Step 0: Resolve scope and authorization
- Action: 讀取對話與現有 repository，確認來源、目標、分支、private 狀態、備份模式（首次／增量／驗證／還原）及遠端寫入授權；不重問已知資訊。
- Input: 使用者請求、來源目錄、repository metadata、工作樹狀態。
- Output: 備份任務卡，列出來源、目的地、模式、預計異動與授權狀態。
- Validation: repository 或來源不明、遠端非預期公開、存在無法安全合併的遠端變更時停止並詢問。

Step 1: Inventory and classify
- Action: 找出所有有效 `SKILL.md`，記錄 Skill ID、來源、完整資源、分類及重複名稱；依主要交付成果維持一個主要分類。
- Input: Skills 來源與既有分類目錄。
- Output: 去重後的 inventory 與來源到目的地 mapping。
- Validation: 同名不同內容不得靜默覆蓋；無 `SKILL.md` 的資料夾不得計為 Skill；分類調整不得順便改變 Skill 行為。

Step 2: Build a safe snapshot
- Action: 在明確的 staging／repository 目錄建立快照，保留 Skill 的核心與相依資源，排除快取、執行紀錄、套件產物、登入資料、token、私鑰、`.env`、個資與不必要的大型暫存檔。
- Input: inventory、排除規則與既有備份。
- Output: 可檢查的本地快照及異動清單。
- Validation: 不直接刪除來源；不跟隨指向來源樹外的 symlink；未知敏感檔案先隔離或停止，不自行上傳。

Step 3: Generate navigation and manifest
- Action: 建立或更新 repository 首頁、總目錄、每個分類 README、每個 Skill README 與 `SHA256SUMS.txt`；README 只供人閱讀，不取代 `SKILL.md`。
- Input: staging snapshot 與 inventory。
- Output: 可逐層瀏覽的導覽與排除 manifest 本身的 SHA-256 清單。
- Validation: README 的名稱、用途、相對連結及 Skill 數量須與實際目錄一致；每個 Skill 必須仍有 `SKILL.md`。

Step 4: Run pre-publication gates
- Action: 優先執行 repository 既有驗證工具，再使用 `scripts/audit_backup.py` 檢查結構、名稱、symlink、敏感檔名／內容、README 與校驗碼；檢視完整差異。
- Input: 完整 staging snapshot。
- Output: PASS／FAIL 報告、檔案數、Skill 數、分類數及阻擋問題。
- Validation: 任一秘密、私鑰、缺檔、checksum mismatch 或來源外 symlink 都是 BLOCKED；不得以人工抽查覆蓋失敗結果。

Step 5: Publish without rewriting history
- Action: 只有目前請求已明確授權遠端寫入時才更新 GitHub；確認 repository private，使用 fast-forward 或 GitHub tree／commit／ref 流程，避免 force push，且絕不將 token 寫入 URL、檔案、輸出或紀錄。
- Input: 已通過 gates 的快照、目標 repository、目前遠端 head 與授權。
- Output: 新版本識別與遠端更新結果。
- Validation: 遠端 head 與預期 parent 不同時停止並重新比較；工具未明確回報成功時不得聲稱完成。

Step 6: Verify the remote backup
- Action: 以產生的版本識別讀回總目錄、至少一個分類 README、跨分類 Skill、腳本及所有二進位類型各一個樣本；比較數量與 checksum manifest，必要時下載到隔離暫存目錄做還原演練。
- Input: 遠端 repository 與新版本識別。
- Output: 遠端驗證紀錄與抽查清單。
- Validation: 預設分支頁面顯示延遲不等於失敗，以版本識別直接讀取為準；任一抽查失敗時狀態為 FAIL，不得只報局部成功。

Step 7: Report and preserve recovery instructions
- Action: 回報 repository、private 狀態、版本、Skill／分類／檔案數、驗證結果、未解風險與還原方式；提供下一次增量更新入口。
- Input: inventory、gate 結果與遠端驗證紀錄。
- Output: 簡短且可追溯的備份完成報告。
- Validation: 報告中的數字與版本必須來自實際結果，不得估算；若未做還原演練，須明確列為尚未驗證。
</workflow>

<output_contract>
依序輸出：
1. 結論：PASS、FAIL 或 BLOCKED。
2. 備份摘要：repository、private 狀態、版本、分類／Skill／檔案數。
3. 驗證：結構、敏感資料、checksum、遠端抽查及還原演練結果。
4. 例外與下一步：只列仍需處理的風險或建議。

使用繁體中文 Markdown；簡單增量更新控制在約 12 行內。沒有實際工具成功證據時，不得使用「已備份完成」。

任一 final gate、stage gate 或 policy gate 為 FAIL / BLOCKED 時，結論只能是 FAIL 或 BLOCKED。局部 PASS 只可列在定位資訊，且必須明確標註不具放行效力。
</output_contract>

<tool_rules>
- 優先使用 `rg`／`find` 盤點、repository 自帶腳本及本 Skill 的 `scripts/audit_backup.py` 做唯讀檢查。
- GitHub connector 與 `git` 都可用；選擇能驗證 remote head 且不暴露認證資訊的方式。
- 遠端寫入、建立 repository、改公開性、刪檔、force push 或覆蓋本機現用 Skills 都是外部／重大副作用；除非使用者在目前請求已明確要求該動作，否則先取得確認。
- 不把短效 token 寫進 remote URL；不列印 token；不把憑證存入 repository。
- 遠端 API 暫時失敗只可有限重試；權限、保護分支、non-fast-forward 或資料風險屬停止條件。
</tool_rules>

<default_follow_through_policy>
- Directly do: 盤點、分類建議、建立本地 staging、產生 README／manifest、秘密掃描、結構驗證與唯讀遠端查核。
- Ask first: 使用者尚未明示的 GitHub 寫入、repository 建立／改公開性、刪除遠端內容、force push、覆蓋現用 Skills 或處理無法判定的敏感檔案。
- Stop and report: secret gate 失敗、remote head 分歧、來源或目標不明、權限不足、驗證工具失敗、還原將覆蓋非空目標。
</default_follow_through_policy>

<examples>
Example 1
Input:
- 「把我新增的 Skills 更新到私人 GitHub，並確認可以還原。」

Output:
1. 盤點新增與異動 Skill，建立增量快照並更新導覽與校驗碼。
2. 通過秘密、結構與 checksum gates 後更新 private repository。
3. 用新版本讀回跨分類檔案並在隔離目錄驗證；最後回報精確版本與數量。

Example 2
Input:
- 「看看我的 Skills 分類是否合理，但先不要上傳。」

Output:
1. 只做 inventory、分類與本地檢查。
2. 提供建議與預計異動，不執行任何 GitHub 寫入。
</examples>

## References

- 執行或調整備份規則時，讀取 [references/backup-policy.md](references/backup-policy.md)。
- 宣稱建立階段完成前，讀取 [references/readiness_report.md](references/readiness_report.md)。
- 重新命名、合併、拆分或淘汰本 Skill 時，讀取 [references/migration-governance.md](references/migration-governance.md)。
- 做 benchmark 或回歸判定時，使用 [assets/evals/regression_gates.json](assets/evals/regression_gates.json) 的門檻。

## Maintenance

當真實備份出現漏檔、敏感資料誤判、遠端分歧或還原失敗時，將事件轉成 `assets/evals/evals.json` 的回歸案例，再窄幅修改規則或腳本。
