# Technical Documentation Writer

在使用者要撰寫、重寫、盤點或補強技術文件時使用。常見觸發像「幫我寫 README」「補 Quick Start」「整理 migration guide」「寫 runbook」。輸出可執行文件；不適用於 PRD、驗收規格或簡報內容規劃。

## 基本資料

- Skill ID：`technical-documentation-writer`
- 分類：`06-writing-editing`
- 版本：`未標示`
- 主要指令：[SKILL.md](SKILL.md)

## 快速使用

在支援 Skills 的環境中，可以直接描述任務；若要明確指定，可使用：

```text
$technical-documentation-writer 請依我的目標與現有資料完成任務，並列出需要我確認的事項。
```

建議一併提供目標、使用情境、已知資料、限制條件，以及希望取得的成果格式。若資料不足，Skill 會依核心指令只詢問真正影響結果的問題。

## 內容結構

- `SKILL.md`：AI 執行此能力時採用的核心指令
- `agents/`：介面顯示與觸發設定（1 個檔案）
- `references/`：按需求載入的參考資料（5 個檔案）
- `scripts/`：可重複執行的輔助工具（1 個檔案）
- `assets/`：產出時可使用的素材或範本（2 個檔案）

## 維護說明

本 README 供人員瀏覽、搜尋與版本管理；真正影響 AI 行為的是 `SKILL.md` 及其引用的資源。修改功能時，應優先更新核心指令，再重新檢查本說明是否仍一致。
