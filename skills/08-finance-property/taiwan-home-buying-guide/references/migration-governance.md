# Migration governance

## Compatibility

更新時同步檢查 frontmatter 名稱、`agents/openai.yaml`、`skill_lifecycle.yaml`、eval skill name、觸發與負面案例、輸出欄位、參考檔路由及安全邊界。不得默默破壞既有呼叫方式。

## Rename

只有名稱造成可測量的觸發混淆時才改名。記錄新舊名稱、受影響 prompts、UI metadata、evals、相容期間與回退方式。

## Split

若投資、法拍、海外或租賃需求開始擠壓「臺灣自住買方」主要工作，拆成鄰近 Skill，不以增加說明把它擴成萬能房產 Skill。

## Merge

只有兩個 Skills 的主要工作、工具、輸出與安全邊界一致，且合併能降低觸發混淆時才合併；合併前跑鄰近與負面 eval。

## Deprecate

被更完整且邊界一致的 Skill 取代，或持續無法維護台灣法規與來源時，標示退役，指出替代 Skill、最後可用版本與遷移期限。

## Rollback

更新造成誤觸發、遺漏官方時效查核、違法貸款建議、證據信心退化或輸出契約破壞時，回退到最後通過官方驗證與功能案例的版本。

## Migration Evidence

所有改名、拆分、合併、退役或回退決策記錄：舊版／新版、原因、測試、影響檔案、相容風險、回退方式、負責人及下次檢查日期。證據寫入 readiness report 或 release artifact，不以口頭宣稱取代測試。
