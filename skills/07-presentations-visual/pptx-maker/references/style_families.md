# Style Families for Slides

這份 reference 用來管理 `pptx-maker` 目前建議支援的 5 種風格。它們是建議範圍，不具強制性，也不是預設值。若使用者沒有明示指定風格，優先沿用既有品牌系統或維持與內容目的相符的中性設計。

## Recommended scope

目前建議支援的 5 種風格：
- [Swiss Style](./swiss_style.md)
- [Bento Style](./bento_style.md)
- [Flat Design](./flat_design.md)
- [Material Design](./material_design.md)
- [Memphis Style](./memphis_style.md)

這份清單的用途是讓 `pptx-maker` 在需要明示風格時，有一組穩定、可解釋、可 QA 的選項可用。它不是審美總表，也不代表所有高品質投影片都必須從中選一。

## Selection rules

- 若使用者已明示指定某一風格，先檢查它是否和品牌規範、受眾情境、播放載體與內容密度相容。
- 若使用者沒有指定，但品牌規範已鎖定視覺語言，沿用品牌，不要硬套 5 種建議風格。
- 若使用者只說「做得高級一點」或「做得有設計感」，不要自動選風格；先維持中性設計，或回到內容與載體需求決定。

## Quick mapping

### Swiss Style
- 適合：理性、客觀、極簡、對比強烈的內容。
- 適合頁型：封面、章節首頁、核心主張頁、關鍵數字頁、對比論證頁、結論頁。
- 避免：需要溫暖情緒、插畫感品牌或高度裝飾性的任務。
- 詳見：[swiss_style.md](./swiss_style.md)

### Bento Style
- 適合：多模組、多指標、產品亮點集合頁。
- 適合頁型：功能總覽頁、產品能力矩陣頁、KPI / dashboard 頁、案例集合頁、模組對照頁。
- 避免：單一路徑敘事、長推理頁面，或大型投影下會變得過碎的頁面。
- 詳見：[bento_style.md](./bento_style.md)

### Flat Design
- 適合：簡潔、快速掃讀、圖示化、低裝飾的頁面。
- 適合頁型：流程圖頁、功能說明頁、資訊圖頁、教學步驟頁、概念摘要頁。
- 避免：需要強烈材質感、深層空間感，或互動層級必須靠光影明示的情境。
- 詳見：[flat_design.md](./flat_design.md)

### Material Design
- 適合：卡片式資訊、明確層級、表面與動線關係清楚的產品或技術簡報。
- 適合頁型：產品功能頁、卡片式比較頁、系統架構頁、功能模組頁、操作流程頁。
- 避免：被錯用成重陰影堆疊或不必要的 app UI 模仿。
- 詳見：[material_design.md](./material_design.md)

### Memphis Style
- 適合：高能量、反常規、活動、創意、青年文化或需要強烈個性的內容。
- 適合頁型：活動封面、品牌宣傳頁、創意提案首頁、章節轉場頁、情緒氛圍頁。
- 避免：高度保守、正式、法規、財務審查等需要低噪音與權威穩重的情境。
- 詳見：[memphis_style.md](./memphis_style.md)
