# Doc Type Routing

先決定文件主類型，再開始寫。若沒有這一步，最常見的結果就是把教學、操作手冊、FAQ、背景說明與 API 參考混在一起，讀者既學不到也查不到。

## 1. Primary routing via Diataxis

### Tutorial

適用於帶新手完成一段學習旅程。重點是循序漸進、一次只教必要內容、每一步都有成功回饋。

用在：
- 首次安裝後跑出第一個畫面
- 新使用者完成第一個 workflow
- 新工程師熟悉專案基本開發流程

不要混入太多 reference 細節；有需要時連到其他文件。

### How-to guide

適用於讀者已知道自己要完成什麼任務，只需要最短路徑做到。

用在：
- 如何部署到 staging
- 如何重設密碼
- 如何匯出報表
- 如何設定 webhook 或 API key

重點是任務完成，不是概念教學。

### Reference

適用於查詢精確事實。內容應完整、可掃描、低歧義。

用在：
- API usage docs
- CLI flags
- 設定檔欄位
- 錯誤碼
- webhook payload

不要塞長篇故事；讀者通常是帶著明確查詢來的。

### Explanation

適用於幫讀者理解背景、架構、設計取捨與限制。

用在：
- 為什麼系統要這樣切分
- 權限模型說明
- 為什麼 v2 API 與 v1 不相容
- 為什麼 runbook 要先做哪些判斷

重點是理解，不是立即執行。

## 2. Common wrappers

以下類型通常是外層容器，裡面仍應標明主要文件類型。

### README

通常混合 overview、quick start 與導覽，但主目標應是讓讀者知道這是什麼、適合誰、下一步去哪。

### Runbook

本質上常是 how-to + reference。讀者通常在壓力下閱讀，所以順序應是症狀、診斷、修復、升級。

### Migration guide

本質上常是 how-to + explanation。重點在破壞性變更、升級順序、驗證與回退。

### FAQ

本質上常是 reference 的另一種呈現。只有在問題真的會被反覆問到時才值得建立。

## 3. Decision questions

開始前先回答：

1. 讀者是新手還是熟手？
2. 讀者是想學習、完成任務、查細節，還是理解背景？
3. 這份文件最成功時，讀者能做出什麼具體行動？
4. 若讀者只看前兩個標題，會不會知道自己是否來對地方？

## 4. Anti-patterns

- 把 tutorial 寫成 reference：新手看不懂順序，老手也找不到任務路徑。
- 把 reference 寫成故事：資訊不易查找，且版本細節容易被埋掉。
- 把 how-to 寫成 explanation：懂很多背景，但做不到目標任務。
- 一份文件同時想服務所有人：最後誰都服務不好。
