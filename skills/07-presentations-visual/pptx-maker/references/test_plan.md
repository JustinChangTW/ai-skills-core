# Test Plan

這份測試計畫專門驗證 `pptx-maker` 是否守住它的邊界，同時真的能幫助投影片落地。

## Trigger tests

### Should trigger
- 幫我把這份核定好的逐頁規劃做成 12 頁 PPTX。
- 用這個公司 template 把內容套成正式 deck。
- 這批 SVG 都編好了，幫我依頁碼組成 PowerPoint。
- 更新現有簡報第 4 到第 6 頁，不要動其他頁。

### Should not trigger
- 幫我規劃一份簡報內容。
- 我想知道這份簡報要怎麼說服董事會。
- 幫我把這篇長報告整理成重點。
- 幫我潤飾講稿文字。

### Near-miss
- 幫我做簡報。
- 幫我套版。
- 幫我修 PPT。

## Functional tests

### Case 1: Approved content to new deck
- Given: 已有逐頁內容規劃、視覺元素表、色彩方向與輸出格式。
- When: 要求產出新 PPTX。
- Then:
  - 先確認內容已定稿。
  - 選定新建製作路線。
  - 產出 slide build spec。
  - 有 QA 與交付說明。

### Case 2: Template adaptation
- Given: 一份公司模板與一份 8 頁內容。
- When: 要求正式套版。
- Then:
  - 先盤點模板。
  - 版型選擇與內容數量相符。
  - 不會重寫原本的說服結構。

### Case 3: Scoped deck edit
- Given: 一份既有簡報與明確指定修改頁面。
- When: 要求只改局部內容並補 notes。
- Then:
  - 明確限制修改範圍。
  - 維持其他頁面不變。
  - 有輸出驗證步驟。

## Failure signals

- 把「做簡報」一律當成內容規劃來處理。
- 沒有選路就直接動手做，最後才發現工具不支援。
- 為了快把整頁變成圖片，卻沒有告知可編輯性損失。
- 修改現有 deck 時擴散到未要求區域。
