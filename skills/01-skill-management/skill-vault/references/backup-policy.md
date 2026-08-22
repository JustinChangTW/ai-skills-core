# Skills GitHub 備份政策

## 目標

備份必須同時達成：內容完整、沒有敏感資料、歷史可追溯、遠端可讀、可在隔離位置還原。只完成複製或上傳，不等於備份完成。

## Repository 基線

- 預設使用 private repository；改為 public 必須由使用者明確決定並重新做授權與敏感資料審查。
- 預設分支使用 `main`；採 fast-forward 更新，不以 force push 解決分歧。
- repository 名稱宜短、可辨識且不含個資，例如 `ai-skills-core`。
- 不在 remote URL、設定檔、README、腳本或 commit message 中保存 token。

## 備份內容

每個 Skill 至少保留 `SKILL.md`，並完整保存實際存在的 `agents/`、`references/`、`scripts/`、`assets/`、`schemas/`、`policies/` 與 `examples/`。repository 另外提供：

- 首頁 `README.md`
- 總目錄 `CATALOG.md`
- 每個分類的 `README.md`
- 每個 Skill 的人類導覽 `README.md`
- 排除自身的 `SHA256SUMS.txt`
- 可重複執行的匯出、README 產生及驗證工具

備份用 README 不應成為 Agent 的執行指令；`SKILL.md` 才是行為來源。

## 禁止內容

- `.env`、API key、GitHub token、私鑰、憑證與登入 cookie
- 執行紀錄、對話紀錄、session、cache、`__pycache__`、`.pyc`
- 未經確認的個資、客戶資料、公司機密或受授權限制的內容
- `.git/`、臨時壓縮檔、建置產物及可重新產生的大型檔案
- 指向來源樹外的 symlink

## 分類原則

1. 一個 Skill 只有一個主要分類。
2. 依主要交付成果分類，不依偶然關鍵字或使用工具分類。
3. 跨領域關係以目錄、標籤或 handoff 表達，不複製第二份 Skill。
4. 同名不同內容必須人工決定合併、改名或保留哪一份，不可靜默覆蓋。
5. 新分類只有在既有分類無法清楚容納多個 Skills 時才建立。

## 發布 gates

遠端寫入前必須全部通過：

1. 每個 Skill 有 `SKILL.md`；frontmatter name 與資料夾名一致。
2. 每個分類與 Skill 有可用 README；相對連結與數量一致。
3. 敏感檔名與敏感內容掃描無命中。
4. 不含 symlink、未知來源的二進位或來源目錄外內容。
5. `SHA256SUMS.txt` 與實際檔案集合及內容一致。
6. 完整 diff 已檢視；沒有非預期刪除或大幅縮減。
7. 目標 repository、private 狀態、分支與 remote head 已確認。

## 遠端驗證與還原

- 用新 commit 識別直接讀回首頁、總目錄、分類 README 及跨分類 Skills。
- 每一種二進位副檔名至少抽查一個檔案；必要時比較 blob SHA 或下載後 SHA-256。
- 至少每季或重大改版後，把指定版本還原到新建的空白暫存目錄，執行 manifest 與 Skill 數量驗證。
- 還原預設不得覆蓋現用 Skills；先產生差異與衝突清單，再由使用者決定安裝。

## 建議保留策略

- 日常採增量版本；重大調整加上易懂標籤，例如 `skills-2026-08`。
- GitHub 不是唯一備份：重要資料另保留一份加密離線或不同供應商副本，符合 3-2-1 原則。
- 定期執行唯讀驗證比只排程上傳更重要；自動化失敗時應通知，而不是靜默略過。
