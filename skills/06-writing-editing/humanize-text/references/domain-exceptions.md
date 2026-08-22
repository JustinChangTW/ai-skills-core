# 領域例外與保留規則

`humanize-text` 預設會減少模板感、轉折詞、抽象名詞與過度 hedging。但不是所有正式語言都是 AI 味。遇到學術、醫療、法務、技術文件、財務揭露或正式公告時，必須先保留領域可信度，再處理機器感。

## 通用例外原則

1. 正式文件需要的精準、保守與一致，不應被改成口語。
2. 合法引用、統計數字、限制條件、風險揭露與必要 hedging 必須保留。
3. 只移除空泛包裝、過度重要性膨脹、重複句型與無來源的權威語氣。
4. 改寫後若讓法律、醫療、財務或研究含義變強，必須退回保守表述。

## 學術與研究寫作

應保留：

1. 有引用或具體數據支撐的 attribution，例如「prior studies have shown」「evidence suggests」。
2. 必要轉折，例如 `Notably`、`Furthermore`、`In contrast`、`Nevertheless`，但不能在同一段密集堆疊。
3. 研究結論需要的 hedging，例如 `may`、`suggests`、`was associated with`。
4. 一致術語，例如同一研究對象不要在 patients、participants、subjects 之間無理由輪替。

應修正：

1. `groundbreaking`、`pivotal`、`evolving landscape` 這類誇大重要性的詞。
2. 無引用的「studies show」「experts argue」。
3. 多層 hedge 堆疊，例如「may suggest that ... has the potential to」。
4. 過度壓縮的 dash compound 或抽象短語，導致讀者看不出實際關係。
5. 非地點用法的 loose `where`，可改成 `with`、新句或更清楚的介系詞結構。

## 醫療與科學語境

醫療與科學內容不得為了自然化而弱化資料完整性。數字、信賴區間、p 值、研究設計、樣本數與限制條件都要保留。觀察性或探索性發現不能改成因果宣稱；RCT 或明確主要終點的結果可以較直接。

## 技術文件

技術文件的人味來自可執行、清楚與少廢話，不是加入情緒。保留 API 名、參數、錯誤碼、路徑、版本與警告。可刪掉「comprehensive guide」「let's dive in」這類暖場，但不要刪掉必要的 prerequisites、steps 或 constraints。

若使用者要求保留列表，技術文件可以保留真正的步驟、CLI flags、API fields 或 enum 清單；此時 no-list 預設被使用者與媒介需求覆寫。

## 商務與行銷

商務文案可保留必要的 CTA 與品牌語氣，但要刪除空泛形容詞、過度感謝、過度興奮與成就膨脹。具體角色、產品用途、客戶問題、限制與下一步，比「創新」「卓越」「世界級」更自然。

## 客服與教學

可以保留溫和語氣與承接句，但刪掉「很棒的問題」「當然可以」這類對話殘影。若使用者正在求助，先解決問題，再調整語氣。

## 法務、財務與正式公告

不要自行簡化會改變法律或財務含義的詞。可修掉重複、冗詞與不自然句型，但需保留定義、條件、限制、免責與日期。

