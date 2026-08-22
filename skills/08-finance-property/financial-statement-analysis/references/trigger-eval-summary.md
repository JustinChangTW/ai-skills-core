# Trigger eval summary

這份摘要整理 `financial-statement-analysis` 目前已有的 trigger / overlap 證據。

## Coverage

- Total eval cases: 16
- Should trigger: 8
- Should not trigger: 8
- Language mix:
  - zh: 6
  - en: 5
  - mixed: 5

## Manual fixture routing audit

這輪使用 `iteration-1` 的 fixture-style paired run 檢查設計是否能區分：
- 需要完整財報解讀的請求
- 應 handoff 到鄰近 skill 的請求

結果：
- should-trigger cases correctly handled by `with_skill`: 8 / 8
- should-not-trigger cases correctly handed off / held off by `with_skill`: 8 / 8
- fixture false positives in `with_skill`: 0 / 8 should-not-trigger cases
- fixture false negatives in `with_skill`: 0 / 8 should-trigger cases

## Fixture benchmark snapshot

從 `iteration-1` 回收的 benchmark 摘要：
- with_skill pass rate: `1.00`
- without_skill pass rate: `0.02`
- pass-rate delta: `+0.98`
- with_skill mean time: `17.0s`
- without_skill mean time: `12.0s`
- time delta: `+5.0s`
- with_skill mean tokens: `1040`
- without_skill mean tokens: `470`
- token delta: `+570`

判讀：
- 這個 skill 在 fixture 條件下有明顯結構與路由收益。
- 額外成本主要是更完整的輸出結構，不是大量工具重試。

注意：
- 這是 fixture-style paired run，不是 production router telemetry。
- 它證明目前 description、boundary、eval assets 與 review pipeline 已可運作，但不等於真實上線流量表現。

## Neighbor confusion matrix

Repo-level overlap audit：
- `hit@1 = 0.0840`
- `hit@3 = 0.2183`
- Top neighbors:
  - `longdoc-evidence-reader` score `0.0840`
  - `alternative-solution-designer` score `0.0698`
  - `mermaid-diagram` score `0.0645`

判讀：
- 目前沒有達到 repo overlap audit 的高風險閾值。
- 主要邊界風險仍集中在 `longdoc-evidence-reader`，原因是兩者都可能處理 10-K / 年報 / 附註，但 outcome 不同。

## Remaining caution

- 若要宣稱真正的 `hit@1` / `false positive` production performance，仍需在實際 skill dispatch 環境執行 live trigger eval。
- 若要降低作者偏見，後續 benchmark 最好補真人 reviewer 或盲評。
