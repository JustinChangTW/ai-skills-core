---
name: arxiv-research
description: 搜尋、篩選、閱讀及查證 arXiv 預印本，支援主題、作者、分類、論文 ID、日期排序、版本辨識、引用追蹤與證據摘要。當使用者要找 AI、資安、電腦科學、數學或物理論文，追蹤最新研究、比較多篇論文、驗證技術主張、建立文獻回顧或詢問 arXiv 論文時使用。不得把預印本描述成已同儕審查，也不得以引用數取代品質判斷。
---

# arXiv 學術研究

以可追溯方式搜尋及分析 arXiv。優先使用可用的網路搜尋／開頁工具；需要精確查詢、批次結果或固定格式時，執行 `scripts/search_arxiv.py`。

## 工作流程

1. 把問題轉成英文核心術語、同義詞、縮寫及排除詞；保留使用者原始研究問題。
2. 先廣搜，再以作者、分類、標題或日期縮小。查詢語法與常用分類見 `references/query-guide.md`。
3. 保存論文 ID、版本、標題、作者、首次提交日、更新日、分類及原始連結。
4. 閱讀摘要後才篩選；重要主張必須讀取 PDF／HTML 正文的相關段落，不得只憑摘要推論。
5. 查明出版狀態。若只確認 arXiv，標示「預印本／同儕審查狀態未確認」；若聲稱已正式發表，另外查證 DOI、期刊或會議官方頁面。
6. 對關鍵結論至少記錄研究方法、資料集／樣本、主要結果、限制與適用邊界。
7. 需要引用關係時，查 Semantic Scholar、Crossref或出版社原頁並交叉驗證；引用數只作採用訊號。
8. 以繁體中文回答，將可驗證事實、推論及未知事項分開，附原始論文連結。

## 精確查詢

```bash
python scripts/search_arxiv.py "retrieval augmented generation security" --max 10 --sort date
python scripts/search_arxiv.py --author "Ross Anderson" --max 10
python scripts/search_arxiv.py --category cs.CR --sort date --max 20
python scripts/search_arxiv.py --id 2402.03300
python scripts/search_arxiv.py "phishing detection" --format json
```

執行腳本前確認輸入只是查詢文字，不拼接 shell。腳本只向 `export.arxiv.org` 發出唯讀 GET；不需 API key，不登入、不發布、不修改遠端資料。

## 證據標示

- `已核實`：由論文正文、正式出版頁或資料集直接支持。
- `摘要支持`：目前只由 arXiv 摘要支持，尚未讀取正文。
- `合理推論`：由多項證據推導，明確說明推論過程。
- `未知`：版本、審查、數據或限制無法核實。

遇到醫療、法律、金融或資安高風險決策，提高證據門檻；arXiv 只能作研究線索，不取代臺灣法規、主管機關文件、正式標準或專業意見。

## 輸出格式

簡單查詢列出最相關的 3–10 篇，每篇包含標題、作者、年份、arXiv ID及版本、相關理由、方法、主要發現、限制、審查狀態，以及摘要頁與 PDF 連結。

文獻回顧另外提供搜尋式、納入／排除條件、證據矩陣、研究缺口及查詢截止日。不要捏造論文、DOI、作者、引文或實驗數字；無法核實時標成未知。

## 來源與邊界

此相容版移植自 Hermes Agent `arxiv` v1.0.0（MIT），保留 arXiv REST API 的唯讀查詢方法，改用 Codex／ChatGPT Work 可用流程，並增加繁體中文、證據分級及高風險研究護欄。
