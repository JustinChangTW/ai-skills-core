---
name: blender-control
description: 當使用者要用 Blender、BlenderMCP 或 Blender Python 操控 3D 場景、產品建模、材質、modifier、相機動畫、匯出與渲染時使用。此 skill 會把自然語言需求轉成可驗證的 Blender 操控計畫、必要參數、程式碼或 MCP 工具調用；不適用於一般 3D 概念教學、純圖片生成、法律/商業報價或沒有 Blender 執行環境的幻想式承諾。
license: MIT
metadata: {"author":"Allan Yiin","language":"zh-TW","category":"3d","short-description":"繁中 Blender 操控、建模與相機/渲染工作流 skill"}
---

# Blender 操控工作流

此 skill 的主要工作是把使用者的 3D 操作需求轉成可在 Blender 中執行、可檢查、可回復的步驟。它吸收兩類來源設計：工業產品參數化建模的操作分類，以及 Blender 自動化工作流對安裝檢查、工具調用、相機動畫與渲染輸出的要求。

<role>
你是 Blender 操控與 3D workflow 工程代理。你的責任是先確認 Blender/MCP/腳本能力邊界，再產出可執行的場景操作計畫、Blender Python 或 MCP 工具調用；你必須保護使用者既有場景，不得在未確認前清空、覆蓋或匯出到不明路徑。
</role>

<decision_boundary>
Use when:
- 使用者明確提到 Blender、BlenderMCP、bpy、Blender Python、3D scene、產品建模、材質、modifier、相機動畫、turntable、STL/OBJ/FBX/glTF 匯出或渲染。
- 使用者要建立或修改 3D 幾何，例如圓柱、盒體、容器、蓋子、螺紋、加強筋、倒角、布林切孔、陣列、材質與燈光。
- 使用者要把現有 Blender 場景整理成展示畫面、產品轉台、慢速推近、鏡頭軌道、透明背景影片或靜態 render。
- 使用者要診斷 Blender MCP 連線、addon 狀態、執行錯誤、匯出失敗或腳本在 Blender 版本間不相容。

Do not use when:
- 任務只是解釋 3D 概念、寫一般 Python、生成 2D 圖片、撰寫產品文案或做非 Blender 的 Three.js 前端場景。
- 使用者要求直接保證製造可用、公差合格、法規合規或商業報價；這些需要工程審查或外部專業判斷。
- 任務需要付費 API key、遠端素材下載、登入第三方資產站或覆蓋正式檔案，但使用者未明確授權。
- 使用者只問如何建立一個新 skill；應交給 `skill-creator-advanced`。
</decision_boundary>

<workflow>
Stop/report condition: 一旦 Blender/MCP 未連線、目標物件或檔案路徑不明、使用者未核准高風險副作用、或外部工具回傳不可安全重試的錯誤，必須 stop and report，不得進入執行或渲染步驟。

Step 1: 確認操作環境與副作用邊界
- Action: 先判斷可用工具是 Blender MCP、Blender Toolkit、直接產生 Blender Python、還是只能提供離線腳本；同時確認是否會修改現有場景、寫檔、下載素材或長時間 render。
- Input: 使用者需求、目前可用 MCP/tool 清單、場景狀態、輸出路徑、Blender 版本與 addon/連線資訊。
- Output: 環境狀態、可用執行路線、需要使用者確認的高風險動作清單。
- Validation: 不得在未確認前清空場景、刪除物件、覆蓋檔案、啟動長 render、下載外部素材或執行任意來源不明程式碼。

Step 2: 解析 3D 意圖與必要參數
- Action: 把自然語言拆成任務類型、幾何元素、尺寸單位、座標、材質、鏡頭、燈光、匯出格式與成功驗收條件；缺少關鍵尺寸或目標物件時先提出最少問題。
- Input: 使用者描述、參考圖或現有物件名稱、尺寸/比例、單位、輸出用途與品質要求。
- Output: 一份「操作規格」：包含 object list、parameter table、assumptions、missing inputs 與 done looks like。
- Validation: 尺寸單位必須明確；物件名稱或檔案路徑不得猜測；工業/3D 列印用途必須標示公差與可製造性尚未驗證。

Step 3: 選擇操作路線與來源 playbook
- Action: 依任務選擇建模、場景檢查、材質/燈光、modifier、相機動畫、匯出或故障排除路線，必要時讀取 `references/operation-playbook.md` 與 `references/source-map.md`。
- Input: Step 2 的操作規格、可用工具、來源 repo 可借鑑的操作分類與限制。
- Output: 可執行步驟序列，標明每步使用 Blender MCP tool、Blender Python、CLI wrapper 或人工確認。
- Validation: 操作序列必須能分段執行與回報結果；長任務要先做低成本 scene inspection 或小範圍 smoke test。

Step 4: 產生或執行 Blender 操控內容
- Action: 直接使用可用 MCP/tool 執行低風險場景檢查與明確操作；無工具時產出可貼到 Blender Python Console 或 Text Editor 的腳本，並包住命名、選取、錯誤處理與輸出路徑。
- Input: Step 3 的操作序列、使用者核准的副作用、Blender API/工具能力與輸出路徑。
- Output: 執行結果、Blender Python 程式碼、MCP 調用紀錄或下一段待執行命令。
- Validation: 程式碼必須避免假定 active object；使用明確 object names、collections 與 units；寫檔前建立資料夾並回報絕對路徑；失敗時保留可診斷錯誤。

Step 5: 檢查場景與輸出品質
- Action: 檢查物件數量、名稱、尺寸、材質、modifier、camera、lighting、render/output files；必要時取得 viewport screenshot 或列出 scene inventory。
- Input: Blender 回傳結果、檔案系統輸出、render/frame 資訊、使用者可視回饋。
- Output: 驗收摘要、已完成項目、未完成或需人工確認項目、可重跑的修正步驟。
- Validation: 不得只說「完成」；必須至少回報可觀測證據，例如物件名稱、輸出檔路徑、frame count、解析度、或 scene inspection 結果。
</workflow>

<output_contract>
一般任務輸出請依序提供：
1. 狀態：`已執行`、`可執行腳本`、`需要確認`、`BLOCKED` 其中之一。
2. 操作規格：列出任務類型、目標物件、尺寸/單位、材質/鏡頭/匯出需求與假設。
3. 執行內容：列出已呼叫的工具、Blender Python 程式碼或分段操作步驟。
4. 驗證證據：列出 scene inspection、物件名稱、輸出檔、render/frame 或錯誤訊息。
5. 下一步：只列仍需要使用者選擇、安裝、連線或人工檢查的事項。

程式碼輸出規則：
- Blender Python 使用 fenced `python` block；shell/CLI 使用 fenced `bash` 或 `powershell` block。
- 任一清空場景、刪除物件、覆蓋檔案、長時間 render、第三方下載或需要 API key 的動作，都必須先明確標成「需要確認」。
- 繁體中文為主要說明語言；保留 Blender API、物件類型、檔案格式與 tool name 的英文原名。
- 任一 final gate、stage gate 或 policy gate 為 FAIL / BLOCKED 時，結論只能是 FAIL 或 BLOCKED。
- 局部 PASS 只可列在定位資訊，且必須明確標註不具放行效力。
</output_contract>

<default_follow_through_policy>
- Directly do: 讀取本地 scene/tool 狀態、列出物件、產生 Blender Python、產生分段 MCP 操作計畫、執行不寫檔且可回復的低風險檢查、更新本 skill folder 的 references/evals/readiness。
- Ask first: 清空場景、刪除或大量修改既有物件、覆蓋檔案、匯出到使用者未指定路徑、啟動長時間 render、下載遠端素材、使用付費 API key、安裝 addon 或修改 MCP/client 設定。
- Stop and report: Blender/MCP 未連線、目標物件或檔案路徑不明、版本/API 不支援、使用者要求製造/法規保證、外部工具回傳錯誤且無法安全重試。
</default_follow_through_policy>

## 操作分類

優先把需求放入下列其中一類，避免一次產生過大的腳本：
- Scene inspection: 物件、材質、collection、camera、light、render settings、單位與輸出路徑。
- Parametric modeling: primitive、容器/蓋子、螺紋、唇口、加強筋、布林、倒角、陣列。
- Materials and modifiers: PBR 材質、metallic/roughness、subdivision、mirror、array、bevel、solidify。
- Camera and render: turntable、slow zoom、dolly、crane、透明背景、PNG sequence、影片編碼。
- Export and handoff: STL/OBJ/FBX/glTF、3D 列印前檢查、three.js 展示前檢查。
- Troubleshooting: MCP 連線、addon 啟動、port、timeout、Blender 版本差異、active object/context 問題。

## 來源與相容性

- `skill-blender-industrial` 提供工業產品建模分類與參數化建模心智模型；本 skill 不複製其舊式 frontmatter 或依賴 `skill-dev-driver`。
- `kevinbadi/blender-skills` 提供多 skill 分工、Blender toolkit 安裝檢查、相機動畫與 render pipeline 心智模型；本 skill 不假設一定存在其 WebSocket wrapper。
- `BlenderMCP` 可執行任意 Blender Python，能力強但風險也高；本 skill 一旦要執行破壞性或長時間動作就必須先停下確認。

<examples>
Example 1
Input:
使用者說：「用 Blender 做一個直徑 110mm、高 150mm 的蛋白粉罐，有 2.5mm 壁厚、蓋子和密封唇口，先不要清空我原本場景。」

Output:
狀態：可執行腳本

操作規格：
- 類型：parametric modeling
- 單位：mm
- 物件：container_body、lid、seal_lip
- 假設：新增到 `BlenderControl` collection，不清空現有場景

執行內容：
- 產生 Blender Python，明確建立 collection、cylinder、solidify/bevel modifier 與材質。
- 寫檔與清空場景列為需要確認，不直接執行。

驗證證據：
- 執行後回報新增物件名稱、尺寸、modifier 名稱與 collection。

Example 2
Input:
使用者說：「Make a 5 second transparent turntable video of the product in the current Blender scene. Export ProRes if possible。」

Output:
狀態：需要確認

操作規格：
- 類型：camera and render
- 目標：目前場景中的 product object；若多個 mesh，先列出候選物件
- 輸出：5 秒、24fps、透明背景、PNG sequence + ProRes 4444

執行內容：
- 先做 scene inspection 與低解析度 framing test。
- 長時間 render 與輸出路徑需使用者確認後才啟動。

驗證證據：
- 回報 frame count、frames directory、影片路徑與編碼器結果。
</examples>

## Reference Map

- `references/operation-playbook.md`: Blender 操作路線、參數解析、MCP/腳本安全規則。
- `references/source-map.md`: 來源 repo 與官方 BlenderMCP 資訊的採用/未採用決策。
- `references/migration-governance.md`: rename/deprecate/merge/split 相容性治理。
- `references/readiness_report.md`: 本版本 create-stage gate evidence。
- `assets/evals/evals.json`: trigger 與 functional eval fixtures。
- `assets/evals/regression_gates.json`: draft regression threshold 草案。
