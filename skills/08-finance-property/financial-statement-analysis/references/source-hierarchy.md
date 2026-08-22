# Source hierarchy and comparison rules

## Source priority

1. 使用者提供的原始財報、年報、季報、10-K、10-Q、法說補充資料。
2. 官方或監管申報來源。
3. 公司 IR / investor relations 網站。
4. 標準化資料庫或二手整理。
5. 媒體或第三方評論。

原則：
- 能回到原始申報，就不要只停在二手摘要。
- 若使用標準化資料庫做快速比較，結論仍應回原始申報驗證。

## Official source examples

### Taiwan
- 公開資訊觀測站（MOPS）與 XBRL 財務報告下載。
- 臺灣證券交易所或櫃買中心公告頁。

### United States
- SEC EDGAR filing pages。
- SEC CompanyFacts / XBRL 資料。
- 公司 10-K / 10-Q 原始申報頁面。

### Cross-market comparison
- 公司 IR 頁面可作補充，但若與監管申報衝突，以監管申報優先。
- Bloomberg、LSEG / Refinitiv、TEJ 等資料庫適合做初步 peers 篩選，不應成為唯一依據。

## Current-data rule

若使用者要求：
- 最新
- 當季
- 目前
- 今天
- 最近一次申報

則必須額外確認：
- 資料發布日期
- 事件發生日期
- 財報涵蓋期間
- 是否已被更正、重編或有後續公告

## Comparison normalization checklist

同業或跨期比較前，至少檢查：
- 幣別是否一致
- 期間長度是否一致
- 合併或個別報表是否一致
- 會計準則是否一致
- 是否有重大併購、處分、重編或分拆
- 是否有明顯一次性損益
- 是否有租賃、開發成本資本化、存貨成本公式或現金流分類差異

## IFRS vs US GAAP watchpoints

- 存貨：
  - IFRS 不使用 LIFO
  - US GAAP 可能有 LIFO 與 LIFO reserve 議題
- 存貨跌價與減損：
  - IFRS 某些情況允許迴轉
  - US GAAP 通常較保守
- 研發/開發支出：
  - IFRS 開發成本在條件成立下可能資本化
  - US GAAP 多數研發費用化
- 現金流分類：
  - IFRS 對利息/股利分類較有彈性
  - US GAAP 分類通常較固定
- 資產後續衡量：
  - IFRS 可能出現重估模式
  - US GAAP 多以歷史成本為主

## Minimum sourcing standard for conclusions

每個重要結論至少要能回指到以下其中一種：
- 報表行項
- 附註或會計政策段落
- 官方申報頁面
- 官方資料 API / XBRL 項目

若做不到，就應標示為：
- 推論
- 待確認
- 缺資料，暫不下結論
