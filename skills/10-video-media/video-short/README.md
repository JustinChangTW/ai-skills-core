# Video Short

Turn long-form or raw video into concise short-form clips with a clear hook, coherent payoff, vertical reframing, readable Traditional Chinese captions, and platform-safe composition. Use for Shorts, Reels, TikTok-style clips, 直式短影音、精華短片、長片剪短、60秒影片, highlight extraction, or multiple short clips from one source.

## 基本資料

- Skill ID：`video-short`
- 分類：`10-video-media`
- 版本：`未標示`
- 主要指令：[SKILL.md](SKILL.md)

## 快速使用

在支援 Skills 的環境中，可以直接描述任務；若要明確指定，可使用：

```text
$video-short 請依我的目標與現有資料完成任務，並列出需要我確認的事項。
```

建議一併提供目標、使用情境、已知資料、限制條件，以及希望取得的成果格式。若資料不足，Skill 會依核心指令只詢問真正影響結果的問題。

## 內容結構

- `SKILL.md`：AI 執行此能力時採用的核心指令
- `agents/`：介面顯示與觸發設定（1 個檔案）
- `references/`：按需求載入的參考資料（1 個檔案）

## 維護說明

本 README 供人員瀏覽、搜尋與版本管理；真正影響 AI 行為的是 `SKILL.md` 及其引用的資源。修改功能時，應優先更新核心指令，再重新檢查本說明是否仍一致。
