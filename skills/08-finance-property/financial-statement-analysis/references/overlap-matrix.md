# Overlap matrix

這份矩陣把 `financial-statement-analysis` 最容易混淆的鄰近 skills 拆開，避免 query stealing。

## 1) `longdoc-evidence-reader`

- Shared vocabulary:
  - annual report
  - 10-K
  - 10-Q
  - notes
  - footnote
- This skill wins when:
  - 使用者要的是財務體質判讀、三表橋接、盈餘品質、紅旗或同業比較。
  - 使用者要把附註與三表串成經營解讀，而不是只找定位。
- Neighbor wins when:
  - 使用者只要頁碼、段落、附註定位、逐條引用或證據鏈。
  - 任務重點是「找哪裡寫了什麼」，不是「這代表什麼」。
- Negative trigger to add:
  - 「頁碼」
  - 「citation only」
  - 「逐頁找出」

## 2) `concept-alignment`

- Shared vocabulary:
  - IFRS
  - US GAAP
  - revenue recognition
  - lease
  - impairment
- This skill wins when:
  - 使用者已經有公司或財報，要做具體財報判讀。
  - 使用者關心的是制度差異如何影響該公司的報表解讀。
- Neighbor wins when:
  - 使用者先要制度背景、定義、歷史脈絡或近期監管事件。
  - 任務還沒進入特定公司分析。
- Negative trigger to add:
  - 「先做概念對齊」
  - 「先不要分析公司」
  - 「先整理制度差異」

## 3) `technical-documentation-writer`

- Shared vocabulary:
  - memo
  - report
  - summary
  - board deck
- This skill wins when:
  - 使用者要先做分析，還沒有現成結論。
  - 核心價值在財務判斷本身。
- Neighbor wins when:
  - 使用者已經有分析結果，只要重寫成 memo、報告、FAQ 或文件。
  - 主要工作是表達，不是判讀。
- Negative trigger to add:
  - 「幫我改寫」
  - 「整理成 memo」
  - 「寫成報告」

## 4) `slide-content-planner`

- Shared vocabulary:
  - comparison
  - company performance
  - financial story
- This skill wins when:
  - 使用者仍在判讀數字和風險。
  - 尚未進入簡報故事線或頁面結構。
- Neighbor wins when:
  - 已有分析結論，下一步是安排逐頁訊息、圖表與敘事順序。
- Negative trigger to add:
  - 「做成簡報」
  - 「規劃逐頁」
  - 「整理成 deck」

## 5) `fermi-estimation`

- Shared vocabulary:
  - growth
  - market
  - company
  - business
- This skill wins when:
  - 使用者要解讀既有財報或申報文件。
  - 核心問題是會計口徑、三表一致性或紅旗。
- Neighbor wins when:
  - 使用者要粗估 TAM、需求、容量、產能或市場規模。
  - 即使提到公司，核心也不是解讀報表。
- Negative trigger to add:
  - 「粗估」
  - 「TAM」
  - 「市場規模」

## Boundary test prompts

- 本 skill 應接：
  - 「幫我看這份 10-K，淨利跟現金流背離在哪裡？」
  - 「比較兩家同業財報，注意 IFRS 跟 US GAAP 差異。」
  - 「從財報角度看這家公司槓桿和股利是否可持續。」

- 鄰近 skill 應接：
  - `longdoc-evidence-reader`:
    - 「把 10-K 裡所有 revenue recognition 的頁碼列出來。」
    - 「找出 goodwill impairment 在附註哪幾頁提到。」
  - `concept-alignment`:
    - 「先整理 IFRS 與 US GAAP 差異，不要分析公司。」
    - 「先做會計制度背景對齊。」
  - `technical-documentation-writer`:
    - 「我已經有分析重點，幫我改寫成董事會 memo。」
    - 「把這份財務分析整理成正式報告。」
