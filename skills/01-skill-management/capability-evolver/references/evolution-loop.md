# 使用回饋與持續演化

不要讓 Skill 自動重寫自己。只有出現可觀察證據時才演化：失敗、使用者修正、誤觸發、漏觸發、來源漂移、安全事件、候選維護停止或安裝驗證退化。

每筆事件記錄：

- `trigger`：當時請求。
- `expected`／`actual`：預期及實際結果。
- `host`／`version`：環境與候選版本。
- `evidence`：可重現資料或使用者回饋。
- `severity`／`reproducibility`：影響與可重現性。
- `proposed_surface`：description、workflow、reference、script、eval、gate或no-change。

將記錄交給 `skill-evolution`，採最小相容修改。每次接受的修改都補一個接近真實的回歸案例；修改後重跑原案例、至少一個相鄰邊界案例與一個負面案例。有足夠評分資料才交給 `skill-optimizer` 比較新舊版本。原始對話、個資、Token與公司資料不得存入 Skill folder。
