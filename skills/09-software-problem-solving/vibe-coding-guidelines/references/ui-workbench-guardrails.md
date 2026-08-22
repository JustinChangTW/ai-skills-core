# UI Workbench Guardrails

這份文件用來幫非程式開發者在做 vibe coding 時，把「避免 AI 產出 stacked dashboard / card farm UI」寫成 agent 可執行的規格。

## 0. 先理解為什麼 AI 會自然長成 stacked UI

常見原因不是模型不懂設計，而是它在優化低風險交付：

- 它把需求讀成功能清單，而不是任務路徑。
- 元件庫預設就是 sidebar + main + summary rail + cards。
- 每個需求包成一張 card，最不容易漏功能。
- 沒有 state model 時，最安全的做法就是把所有資訊一起攤開。
- 沒有被要求做 product / design critique 時，模型通常不會主動 aggressive simplification。

所以不要只要求「做乾淨一點」，而是要把 reveal / hide 規則寫明。

## 1. 不要只交功能清單

如果你只對 coding agent 說：

- 要有輸入區
- 要有狀態區
- 要有摘要
- 要有規則說明
- 要有上傳補件

它很容易直接做成 sidebar + main + right rail + 一堆 cards。這不是因為它不會設計，而是因為這種 layout 最安全、最容易實作、最不容易漏功能。

改成先給它這四類資訊：

- `primary task`：這一頁唯一最重要的任務
- `task model`：primary / secondary / low-frequency / rare goals
- `state model`：empty / drafting / validating / resolved / blocked / submitted 或等價狀態
- `visibility plan`：哪些內容首屏保留、哪些 on-demand、哪些只在特定 state 顯示

再加一層 content audit：

- `must-see-now`
- `next-step-only`
- `error-only`
- `on-demand-reference`
- `keep-off-first-viewport`

如果 agent 沒先做這層分類，它大概率還是會把功能停成一排卡片。

## 2. 可以直接貼進規格或 AGENTS.md 的約束

```text
這不是 dashboard，也不是 admin panel，而是單一主任務頁。

先輸出：
1. primary task sentence
2. task model
3. state model
4. information-role classification
5. information architecture table
6. visibility plan
7. content audit
8. deferred blocks with hidden reason + reveal trigger + container

限制：
- 避免 dashboard/card farm/stacked sections layout
- 首屏最多 2-3 個主要視覺群組
- 首屏只能有 1 個主 CTA
- reference 類資訊預設 on-demand
- exception-handling 只在對應 state 出現
- 不要把每個功能都做成獨立卡片
- 若右欄不能改變當前決策，就不要常駐
```

## 3. 資訊角色分類

要求 agent 把每個區塊標成：

- `action-critical`
- `decision-supporting`
- `status-feedback`
- `reference`
- `exception-handling`
- `audit/history`

沒有分類的區塊，不要直接進首屏。

## 4. 先要 IA，再要 UI

如果畫面是 workflow / workbench / reviewer / editor / setup flow，先要求 agent 產出：

- task model
- state model
- information architecture table
- reveal / hide rules
- content audit
- 每個 deferred block 的 `hidden_now_because`、`reveal_trigger`、`container`

之後才允許它開始寫程式。這會比直接說「幫我做乾淨簡潔的 UI」可靠得多。

## 5. 延後揭露要寫成可驗證格式

至少用這個表：

| 區塊 | 現在是否首屏必須 | hidden_now_because | reveal_trigger | container |
|---|---|---|---|---|
| 評分規則 | 否 | 對當下輸入動作不是必要 | 使用者主動查看規則 | accordion |
| 補件上傳 | 否 | 只有失敗時才需要 | state = blocked | inline panel |
| 歷史紀錄 | 否 | 不影響目前決策 | 使用者切到 history tab | tab |

如果 `hidden_now_because` 寫不出來，通常代表那塊不是該隱藏，而是需求本身仍不清楚。

## 6. 什麼時候應該拆成 step flow

若符合以下兩項以上，優先改成 tabs / wizard / step navigation：

- 任務有明確先後順序
- 後一步高度依賴前一步輸出
- 使用者一次只需要看局部資訊
- 例外處理只會在某些節點發生
- 首屏已經超過 3 個主要群組
- 已出現 4 個以上大型卡片區塊

## 7. 可以直接貼進 AGENTS.md 的檢核問題

把下面這段一起放進 `AGENTS.md` 或規格：

```text
在開始切版前，先回答：
- 這頁唯一最重要的任務是什麼？
- 如果首屏只能保留 3 個區塊，要保留哪 3 個？
- 哪些內容其實只是 reference？
- 哪些內容只應該在 blocked / resolved / submitted 顯示？
- 哪些區塊若沒有 reveal trigger，就不應常駐？
```

## 8. 再加一輪自我審查

要求 agent 在初版 UI 之後自問：

- 如果只能保留 3 個區塊，我會保留哪 3 個
- 哪些資訊其實只是 `reference`
- 哪些區塊只該出現在 `blocked` 或 `resolved`
- 是否有大型說明卡其實應改成 inline helper
- 右欄是否只是因為畫面有空位才存在

如果 agent 答不出這些問題，就代表它還在做 feature parking lot，而不是 task-first UI。
