# 台北市健言社 TM 三分鐘講員教練

為台北市健言社TM講員準備三分鐘演講。Use when 使用者要解題、撰稿或練習不帶稿。This skill only owns speaker preparation. Do not use when 使用者擔任講評、總評、主席或計時，也不適用國際Toastmasters Table Topics。成功結果是符合社規且講員能自然說出的演講。

## 基本資料

- Skill ID：`taipei-tm-speaker-coach`
- 分類：`05-taipei-tm`
- 版本：`2026.8.16`
- 主要指令：[SKILL.md](SKILL.md)

## 使用時機

- 適合：使用者要解題、撰稿或練習不帶稿。This skill only owns speaker preparation.
- 不適合：when 使用者擔任講評、總評、主席或計時，也不適用國際Toastmasters Table Topics
- 預期成果：符合社規且講員能自然說出的演講

## 快速使用

在支援 Skills 的環境中，可以直接描述任務；若要明確指定，可使用：

```text
$taipei-tm-speaker-coach 請依我的目標與現有資料完成任務，並列出需要我確認的事項。
```

建議一併提供目標、使用情境、已知資料、限制條件，以及希望取得的成果格式。若資料不足，Skill 會依核心指令只詢問真正影響結果的問題。

## 內容結構

- `SKILL.md`：AI 執行此能力時採用的核心指令
- `agents/`：介面顯示與觸發設定（1 個檔案）
- `references/`：按需求載入的參考資料（7 個檔案）
- `assets/`：產出時可使用的素材或範本（3 個檔案）

## 維護說明

本 README 供人員瀏覽、搜尋與版本管理；真正影響 AI 行為的是 `SKILL.md` 及其引用的資源。修改功能時，應優先更新核心指令，再重新檢查本說明是否仍一致。
