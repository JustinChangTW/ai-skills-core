# Information Priority Playbook

這份文件把「不要做 stacked dashboard」轉成可執行的資訊架構流程。

## 1. 先承認 stacked UI 的成因

常見根因不是 CSS 不夠強，而是：

- 把 prompt 寫成功能清單，沒有寫成任務模型
- 用元件庫預設組裝出 card grid / sidebar / summary rail
- 為了降低出錯風險，把每個需求都做成自洽區塊
- 沒有 state model，導致所有狀態一次渲染
- 沒有資訊揭露規則，導致 reference content 永久常駐
- LLM 偏好把需求拆成可列舉 section，而不是先處理閱讀動線與視覺節奏
- 訓練資料與元件庫大量偏向 dashboard / admin panel / card farm 版型
- stack 型 layout 最容易做成穩定的 responsive 實作，因此模型會把它當低風險預設
- 若沒有額外要求 product/design critique，模型通常只會完成顯性需求，不會主動 aggressive simplification

## 2. 任務模型先於版面

在畫任何 wireframe 前，先回答：

- 使用者當前唯一主目標是什麼
- 次要目標是什麼
- 哪些只是低頻參考資訊
- 哪些只在錯誤或例外時才該出現

建議先寫成一個短表：

| 項目 | 任務角色 | 頻率 | 首屏是否必須 | 不顯示的風險 |
|---|---|---|---|---|
| 主輸入 / 主編輯區 | action-critical | 高 | 是 | 無法開始任務 |
| 結果摘要 | decision-supporting | 中 | 視 state 而定 | 無法做下一步判斷 |
| 系統進度 / 驗證狀態 | status-feedback | 中高 | 視 state 而定 | 不知道系統正在做什麼 |
| 規則 / FAQ / 指引 | reference | 低 | 否 | 可稍後查閱 |
| 補件 / 重試 / 錯誤處理 | exception-handling | 低 | 否 | 只有失敗時才需要 |
| 稽核 / 歷史紀錄 | audit/history | 低 | 否 | 不該占用主舞台 |

更完整的 task model 應至少拆成：

| 層級 | 定義 |
|---|---|
| primary goal | 進頁後當下唯一最重要的任務 |
| secondary goal | 完成主任務前後會用到，但不是第一眼焦點 |
| low-frequency goal | 可以查，但不應常駐 |
| rare goal | 只在例外、補件或特殊狀況才出現 |

## 3. 用狀態模型決定顯示時機

資訊是否可見，優先由 state 決定，不是由元件庫決定。

常見狀態：

- `empty`
- `drafting`
- `validating`
- `resolved`
- `blocked`
- `submitted`

對每個 state 寫清楚：

- 進入條件
- 使用者現在要做什麼
- 畫面必須顯示什麼
- 哪些資訊要隱藏
- 哪個 CTA 是唯一主 CTA
- 離開條件

範例：

- `empty`：只顯示主輸入、簡短提示、主 CTA
- `validating`：顯示進度與取消/等待，收起規則與長說明
- `blocked`：顯示錯誤原因、補件或重試入口
- `resolved`：顯示結果摘要與下一步 CTA

## 4. 強制做資訊分類

每個區塊都要被標記為：

- `action-critical`
- `decision-supporting`
- `status-feedback`
- `reference`
- `exception-handling`
- `audit/history`

沒有被分類的區塊，不應直接上版面。

## 5. 先產出資訊架構表，再產出 UI

至少要做這張表：

| 資訊項目 | 使用頻率 | 是否首屏必須 | 所屬任務階段 | 顯示條件 | 建議容器 | 是否可收合 |
|---|---|---|---|---|---|---|
| 送件按鈕 | 高 | 是 | resolved | 驗證通過後 | sticky footer | 否 |
| 評分規則 | 中低 | 否 | any | 使用者主動查看 | accordion | 是 |
| 補件上傳 | 低 | 否 | blocked | 驗證失敗時 | inline panel | 否 |

這張表的目的不是美觀，而是強迫在 layout 前就做 reveal / hide 決策。

## 6. Disclosure rules

把 progressive disclosure 寫成硬規則，而不是審美建議：

- 首屏只能有 1 個主操作區。
- 只有在系統真的有處理進度時，才常駐 1 個狀態區。
- 最多只允許 1 個 supporting summary 在首屏。
- `reference` 類資訊預設用 accordion、drawer、modal 或 secondary tab。
- `exception-handling` 只在對應錯誤 state 顯示。
- 長說明優先內嵌在對應控制項旁，不要做成大型說明卡。
- 右欄若不能直接改變當前決策，就不應常駐。
- 首屏超過 2-3 個主要視覺群組，就先合併、延後或拆步驟。

## 7. 什麼時候該拆成 step flow

若同時符合下列兩項以上，優先拆成 wizard / step flow / tabs，而不是同頁堆疊：

- 任務有明確先後順序
- 使用者一次只需要看一部分資訊
- 後一步高度依賴前一步結果
- 例外處理只在特定節點發生
- 首屏已出現 4 個以上大群組

## 8. 先做內容審核，再做版面審查

在產 UI 前，先要求模型回答：

- 哪些資訊是現在必須看
- 哪些資訊是下一步才需要看
- 哪些資訊只有出錯才需要看
- 哪些資訊很少用到，但要可查
- 哪些資訊不應該出現在首屏

對每個延後揭露的區塊，再補一行：

- 為什麼現在可以先隱藏
- 何時應該顯示
- 顯示時應該進哪種容器

這一步的目的，是把「做得簡潔一點」改成可驗證的 reveal / hide 決策。

## 9. 可機器判讀的 metadata schema

若任務複雜，先把主要區塊寫成結構化資料，再生成 UI：

```json
[
  {
    "id": "input_links",
    "role": "action-critical",
    "priority": "high",
    "visibility": "always",
    "stage": ["empty", "drafting"],
    "container": "inline"
  },
  {
    "id": "submission_summary",
    "role": "decision-supporting",
    "priority": "medium",
    "visibility": "conditional",
    "stage": ["resolved"],
    "container": "summary-panel"
  },
  {
    "id": "upload_evidence",
    "role": "exception-handling",
    "priority": "medium",
    "visibility": "conditional",
    "stage": ["blocked"],
    "container": "inline-panel"
  }
]
```

這種做法比只用自然語言提示穩定，因為模型或程式都能直接依欄位決定 render 策略。

## 10. 兩階段生成比單次切版更可靠

建議流程：

1. 第一階段：先輸出 task model、state model、資訊架構表、visibility plan。
2. 第二階段：再生成 UI。
3. 第三階段：以 UX reviewer 身分刪掉首屏不必要資訊、合併重複區塊、把低頻內容收合。

若任務是 workflow / workbench / review tool，預設不要一口氣直接產 JSX。

## 11. 自我審查問題

- 這頁唯一最重要的任務是什麼
- 如果只能保留 3 個區塊，我會保留哪 3 個
- 哪些資訊其實只是 `reference`
- 哪些面板只在特定 state 才應該出現
- 右欄是否只是因為版面有空位而存在
- 空狀態是否清楚說明缺什麼、為什麼缺、下一步做什麼
- 是否有任何大卡片只是重複說明，而不是推進任務

## 12. Prompt template

```text
This is not a dashboard. It is a task-first workflow screen.

Before producing UI, output:
1. primary task sentence
2. task model
3. state model
4. information-role classification
5. information architecture table
6. visibility plan

Constraints:
- avoid dashboard/card farm/stacked sections layout
- keep only one primary CTA in the first viewport
- first viewport max 2-3 visual groups
- reference content must be on-demand
- exception-handling appears only in matching states
- merge or defer sections instead of giving every feature its own card
```

額外可加：

```text
Before generating layout, review all requested features and classify them into:
- must see now
- next-step only
- error-only
- on-demand reference
- should not be in first viewport

For every deferred block, explain why it is hidden now and what event reveals it.
```

## 13. 來源概念

- Task analysis：先拆任務與子任務，再驗證功能是否真的支援使用者目標。
- Progressive disclosure：把進階資訊延後到次級介面，而不是平鋪首屏。
- State-driven UI：用有限狀態與轉移決定顯示時機，避免不可能狀態同時出現。
