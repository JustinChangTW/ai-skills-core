# LINE Sticker Production

Create, iterate, validate, and package upload-ready static LINE sticker sets with customizable character style and on-sticker text. Use when a user asks for LINE stickers, LINE貼圖, a reusable sticker character, Creators Market assets, or a follow-up sticker collection that must retain an approved character style.

## 基本資料

- Skill ID：`visual-line-sticker-production`
- 分類：`07-presentations-visual`
- 版本：`未標示`
- 主要指令：[SKILL.md](SKILL.md)

## 使用時機

- 適合：a user asks for LINE stickers, LINE貼圖, a reusable sticker character, Creators Market assets, or a follow-up sticker collection that must retain an approved character style.

## 快速使用

在支援 Skills 的環境中，可以直接描述任務；若要明確指定，可使用：

```text
$visual-line-sticker-production 請依我的目標與現有資料完成任務，並列出需要我確認的事項。
```

建議一併提供目標、使用情境、已知資料、限制條件，以及希望取得的成果格式。若資料不足，Skill 會依核心指令只詢問真正影響結果的問題。

## 內容結構

- `SKILL.md`：AI 執行此能力時採用的核心指令
- `agents/`：介面顯示與觸發設定（1 個檔案）
- `references/`：按需求載入的參考資料（3 個檔案）
- `scripts/`：可重複執行的輔助工具（2 個檔案）

## 維護說明

本 README 供人員瀏覽、搜尋與版本管理；真正影響 AI 行為的是 `SKILL.md` 及其引用的資源。修改功能時，應優先更新核心指令，再重新檢查本說明是否仍一致。
