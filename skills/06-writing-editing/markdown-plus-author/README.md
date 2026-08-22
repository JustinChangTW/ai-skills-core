# Markdown+ Author

Write or revise Markdown+ documents — plain Markdown that stays valid in any markdown viewer while adding bullet-list blocks with `**#id**` headers, inline-code `key:value` metadata, and viewer-side projection cues. Use when the user asks to write or rewrite a dev note, decision record, research report, tech spec, status report, executive brief, runbook, ADR, status report, or any AI-readable structured document; or when the user asks to convert plain Markdown or existing HTML into Markdown+. Do not use for slide decks, email drafts, or one-off short replies. Successful output is a single CommonMark-valid Markdown file whose blocks can be queried by a parser and projected into human-friendly HTML, with no `:::` fences, no raw HTML wrappers, no base64, code fences and ASCII trees preserved verbatim, and a prose companion for every figure/table/chart.

## 基本資料

- Skill ID：`markdown-plus-author`
- 分類：`06-writing-editing`
- 版本：`未標示`
- 主要指令：[SKILL.md](SKILL.md)

## 使用時機

- 適合：the user asks to write or rewrite a dev note, decision record, research report, tech spec, status report, executive brief, runbook, ADR, status report, or any AI-readable structured document; or when the user asks to convert plain Markdown or existing HTML into Markdown+.
- 不適合：for slide decks, email drafts, or one-off short replies.
- 預期成果：is a single CommonMark-valid Markdown file whose blocks can be queried by a parser and projected into human-friendly HTML, with no `:::` fences, no raw HTML wrappers, no base64, code fences and ASCII trees preserved verbatim, and a prose companion for every figure/table/chart.

## 快速使用

在支援 Skills 的環境中，可以直接描述任務；若要明確指定，可使用：

```text
$markdown-plus-author 請依我的目標與現有資料完成任務，並列出需要我確認的事項。
```

建議一併提供目標、使用情境、已知資料、限制條件，以及希望取得的成果格式。若資料不足，Skill 會依核心指令只詢問真正影響結果的問題。

## 內容結構

- `SKILL.md`：AI 執行此能力時採用的核心指令
- `agents/`：介面顯示與觸發設定（1 個檔案）
- `references/`：按需求載入的參考資料（7 個檔案）
- `assets/`：產出時可使用的素材或範本（2 個檔案）

## 維護說明

本 README 供人員瀏覽、搜尋與版本管理；真正影響 AI 行為的是 `SKILL.md` 及其引用的資源。修改功能時，應優先更新核心指令，再重新檢查本說明是否仍一致。
