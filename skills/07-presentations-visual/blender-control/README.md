# Blender 操控工作流

當使用者要用 Blender、BlenderMCP 或 Blender Python 操控 3D 場景、產品建模、材質、modifier、相機動畫、匯出與渲染時使用。此 skill 會把自然語言需求轉成可驗證的 Blender 操控計畫、必要參數、程式碼或 MCP 工具調用；不適用於一般 3D 概念教學、純圖片生成、法律/商業報價或沒有 Blender 執行環境的幻想式承諾。

## 基本資料

- Skill ID：`blender-control`
- 分類：`07-presentations-visual`
- 版本：`未標示`
- 主要指令：[SKILL.md](SKILL.md)

## 快速使用

在支援 Skills 的環境中，可以直接描述任務；若要明確指定，可使用：

```text
$blender-control 請依我的目標與現有資料完成任務，並列出需要我確認的事項。
```

建議一併提供目標、使用情境、已知資料、限制條件，以及希望取得的成果格式。若資料不足，Skill 會依核心指令只詢問真正影響結果的問題。

## 內容結構

- `SKILL.md`：AI 執行此能力時採用的核心指令
- `agents/`：介面顯示與觸發設定（1 個檔案）
- `references/`：按需求載入的參考資料（4 個檔案）
- `assets/`：產出時可使用的素材或範本（2 個檔案）

## 維護說明

本 README 供人員瀏覽、搜尋與版本管理；真正影響 AI 行為的是 `SKILL.md` 及其引用的資源。修改功能時，應優先更新核心指令，再重新檢查本說明是否仍一致。
