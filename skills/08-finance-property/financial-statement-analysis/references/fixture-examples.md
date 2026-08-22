# Fixture examples

這份文件保留 `financial-statement-analysis-workspace` 中最有代表性的 fixture 輸出，用來保存「這個 skill 應該怎麼答」與「什麼情況應該 handoff」。

它只保留可重用範例，不保留整批 run artifact、HTML review viewer、逐次 timing 或 grading 明細。

## Example 1: 應觸發的財報解讀輸出骨架

來源：`iteration-1 / eval-001-zh-single-company-10k-interpretation / with_skill`

適用情境：
- 使用者要求解讀 10-K / 年報 / 財報
- 重點在現金流、負債、盈餘品質、三表一致性

預期輸出形狀：

```md
## 財報解讀

### 分析範圍與口徑
- 本次先以使用者提供的 filing / report 為主要來源，預設聚焦 10-K、現金流、負債與盈餘品質。
- 若缺公司名稱、期間、幣別或合併範圍，結論只列到可確認層級，不假裝精確定案。
- 先檢查會計政策與附註，再進行三表與比率判讀。

### 核心發現
- 這題的判讀核心不是 headline profit，而是報表口徑、現金轉換與負債結構是否互相支持。
- 若損益表與現金流量表敘事不一致，優先視為盈餘品質風險，而不是先接受表面成長故事。

### 三表橋接與盈餘品質
- 先做 `淨利 -> 非現金項目 -> 營運資金 -> CFO` 的橋接。
- 再檢查 Capex、借款、股利與權益變動是否能在現金流量表與資產負債表之間對上。

### 比率、同業與期間對比
- 只保留和本題直接相關的比率。
- 若涉及跨準則或跨市場比較，先標示可比性限制。

### 風險紅旗與待確認事項
- 待確認附註、一次性項目與營運資金異常。
- 風險提示要保持為風險訊號，不直接定性。
```

## Example 2: 不應觸發時的 handoff 輸出

來源：
- `iteration-1 / eval-009-zh-real-time-trading-call-should-not-tri / with_skill`
- `iteration-1 / eval-010-en-page-citation-extraction-should-not-t / with_skill`
- `iteration-1 / eval-014-mixed-board-memo-writing-should-not-trig / with_skill`

適用情境：
- 即時交易判斷
- citation extraction / page-level evidence only
- 已有分析、只要 memo / report 改寫

預期輸出形狀：

```md
這個請求不應直接進入 `financial-statement-analysis` 完整流程。

原因：使用者要的是更相鄰 skill 的 outcome，而不是先做附註、三表橋接、比率與紅旗分析。

建議做法：先交給更相鄰的 workflow 處理；如果後續真的回到財報體質判讀，再啟動 `financial-statement-analysis`。
```

對應 handoff：
- 即時交易 / 短線判斷：不要硬套財報解讀
- citation only：交給 `longdoc-evidence-reader`
- memo / report 改寫：交給 `technical-documentation-writer`

## What not to preserve

下列內容在 workspace 中有用，但不應作為主 skill 長期保存內容：
- `review.html`
- `benchmark.json` 全量 run 明細
- 每個 eval 的 `grading.json`
- 每個 eval 的 `timing.json`
- 每個 eval 的 `metrics.json`
- `with_skill/` 與 `without_skill/` 的整批 fixture 回應副本

保留原則：
- 主 skill 留「規則、範例、eval 定義、gate、摘要」
- workspace 留「一次執行的產物」
