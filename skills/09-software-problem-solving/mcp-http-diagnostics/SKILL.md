---
name: mcp-http-diagnostics
description: 在使用者要診斷 MCP HTTP 或 Streamable HTTP 端點、確認連線或列出工具時使用。常見觸發像「檢查這個 MCP 連結」「列出 tools」「看 /mcp 為什麼連不上」。輸出握手結果、工具清單與故障診斷；不負責實作或重構 server。
license: MIT
metadata: {"author":"OpenAI Codex","language":"zh-TW","category":"ops","short-description":"診斷 MCP HTTP 與 Streamable HTTP 端點、列出 tools，並輸出可追溯故障判斷"}
---

# Mcp Http Diagnostics

## Purpose

這個 skill 的目標是在最短時間內確認一個使用者提供的 MCP Streamable HTTP URL 是否真的可用，並穩定拿到工具清單。它避免把時間浪費在錯的檢查方式，例如先用裸 `GET /mcp` 判活、先查宿主已註冊的 MCP resources，或先做與連線確認無關的 repo 搜索。

## Scope

### In scope
- 使用者已提供明確的 MCP HTTP URL，要求確認連線、握手、session 狀態或工具清單。
- 對疑似 Streamable HTTP endpoint 做最小握手：`POST initialize` -> 取 `Mcp-Session-Id` / `MCP-Protocol-Version` -> `POST tools/list`。
- 快速診斷常見失敗：錯 endpoint、缺認證、protocol version mismatch、session 遺失、誤把 legacy SSE 當成 Streamable HTTP。
- 產出簡短可執行結論：能不能連、有哪些工具、下一步該補什麼。

### Out of scope
- 幫使用者設計或實作 MCP server 本身。
- 深入閱讀整份 MCP 規格、做架構比較或寫完整 client SDK。
- 對未提供 URL 的一般「MCP 是什麼」教學。
- 把任意外部 URL 自動註冊到宿主 MCP 工具層。這不是此 skill 的責任。

## Primary use cases (2-3)

1) **快速確認連得上且列出工具**
- Trigger examples: "請用這個 streamable http 連結。", "幫我看這個 MCP server 有哪些工具。"
- Expected result: 在 1-2 次核心 request 內完成 initialize 與 tools/list，回報工具名稱與必要參數摘要。

2) **判斷為什麼 `/mcp` 失敗**
- Trigger examples: "這個 `/mcp` 為什麼打不通？", "我 GET `/mcp` 只拿到 400。"
- Expected result: 指出是檢查方式錯誤、endpoint 錯誤、需要 bearer token、protocol mismatch，或 session 已失效。

3) **把 Streamable HTTP 與宿主註冊狀態切開**
- Trigger examples: "我給你 URL 了，為什麼 resources 還是空的？", "這個連結是不是已經被 Codex 掛上 MCP？"
- Expected result: 明確說明 user-provided URL 與宿主已註冊 MCP server 是兩回事，先用原始 HTTP probe 驗證遠端，再決定是否需要宿主整合。

## Workflow overview

1. 先把目標當成「使用者提供的 HTTP endpoint」，不要先假設它已被宿主註冊成 MCP tool。
2. 若有現成 probe script，優先用 `scripts/probe_streamable_http.py`；不要先用 `Invoke-WebRequest` 或 `list_mcp_resources` 當主檢查。
3. 對使用者提供的 exact URL 直接送 `POST initialize`；URL 未含 `/mcp` 時才把 `.../mcp` 加入候選。
4. 成功後立即從 response headers 取 `Mcp-Session-Id` 與 negotiated `MCP-Protocol-Version`。
5. 用同一組 session headers 送 `POST tools/list`，取得權威工具清單。
6. 只有在 initialize 失敗時，才做第二層分流：根路徑描述、認證、legacy SSE 或版本不合。
7. 回覆時先給結論，再給工具清單，再補錯誤診斷與下一步。

## Communication notes

- User vocabulary: MCP、streamable http、`/mcp`、連線狀態、工具清單、握手、session、headers。
- Avoid jargon: 若提到 `negotiate protocol version`，同時解釋成「先送版本，server 回它實際接受的版本」。
- Least-surprise rule: 使用者提供的是 URL 時，先驗證該 URL；不要先把時間花在本地 repo 搜索、宿主資源列舉或與端點無關的背景介紹。

## Routing boundaries

- Neighboring skills / workflows:
  - `web-search-strategy`: 需要去網路找官方文件、版本演進或外部整合案例時交給它。
  - `skill-creator-advanced`: 要把 MCP 診斷流程再進一步做成可發布、可 benchmark 的 skill 時交給它。
- Negative triggers:
  - "幫我設計一個新的 MCP 協議層"
  - "幫我直接修這個 server 的 Python 程式"
  - "幫我摘要整份 MCP spec"
- Handoff rule: 一旦問題從「確認連線與列工具」轉成「修改 server 程式碼」或「全面規格研究」，停止沿用此 skill 的最短路徑，交給更貼近主任務的 skill。

## Language coverage

- Primary language(s): 繁體中文、英文。
- Mixed-language trigger phrases: streamable http、initialize、tools/list、session id、protocol version、legacy SSE、bearer token。
- Locale-specific wording risks:
  - 使用者說「連不上」可能是宿主沒註冊，也可能是 HTTP endpoint 本身無法握手，兩者必須拆開。
  - 使用者說「GET `/mcp` 有回應」不等於 Streamable HTTP 可用；真正最短驗證仍是 `POST initialize`。

## Success criteria

### Quantitative (targets)
- Trigger accuracy: 90% 以上的「確認 streamable http 連線 / 列工具」請求能正確觸發。
- Tool calls: 一般案例 1 次 initialize + 1 次 tools/list；只有失敗分流時才增加。
- Failures: 不把「宿主 resources 空」誤判成「遠端 endpoint 掛掉」。

### Qualitative
- 先走最短成功路徑，而不是先做背景搜索。
- 失敗時能指出具體卡點與下一步，而不是只回「連不上」。
- 對同類 URL 能重複產出一致結論。

## Instructions

### Step 0: Confirm inputs
- Read the existing conversation/files first; ask follow-up questions only when a wrong assumption would materially change the outcome.
- 至少需要一個 URL。若使用者已提供完整 `http://host:port/mcp`，直接用它，不要自行改路徑。

### Step 1: Choose the fastest verification path
- 先判斷問題是不是「使用者提供 URL，要確認 Streamable HTTP 狀態或列工具」；若是，直接進 probe 流程。
- 不要先用 `list_mcp_resources` 或 `list_mcp_resource_templates` 來驗證 user-provided URL。它們只能看目前宿主已註冊的 server，不能代表這個 URL 自己是否可連。
- 不要把裸 `GET /mcp` 當成 health check。對 Streamable HTTP server，`GET /mcp` 常常需要既有 session 與 `Accept: text/event-stream`，直接打可能是 `400` 或 `406`，這不是最短成功路徑。
- 優先執行：
  - `python scripts/probe_streamable_http.py "http://127.0.0.1:9091/mcp"`

### Step 2: Run initialize before everything else
- 對 exact URL 先送：
  - Method: `POST`
  - Headers: `Content-Type: application/json`, `Accept: application/json`, `MCP-Protocol-Version: <candidate>`
  - Body:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25"
  }
}
```

- 若 `2025-11-25` 失敗且錯誤是 protocol mismatch，再依序回退 `2025-06-18`、`2025-03-26`、`2024-11-05`。
- 送 `initialize` 時，header 與 body 的 `protocolVersion` 必須一致；不要一個寫新版、一個寫舊版。
- 優先使用 `scripts/probe_streamable_http.py` 這種 deterministic Python client。PowerShell `Invoke-WebRequest` 在某些本機情境下可能出現不具診斷價值的例外，會拖慢判斷。

### Step 3: Treat response headers as the source of truth
- 若 `initialize` 成功：
  - 從 response headers 取 `Mcp-Session-Id`
  - 從 response headers 取 `MCP-Protocol-Version`
- 若 body 的 `result.dependencies.tools` 已存在，可先用它做快速肉眼確認，但正式工具清單仍以 `tools/list` 為準。

### Step 4: Call tools/list immediately
- 用同一個 endpoint 送 `POST tools/list`：
  - Headers 必帶 `Mcp-Session-Id` 與 negotiated `MCP-Protocol-Version`
  - `Accept` 維持 `application/json`
- 成功後整理：
  - tool 名稱
  - description
  - required input
  - optional input / defaults

### Step 5: Only if initialize fails, branch into troubleshooting
- 依 `references/error-matrix.md` 分流：
  - `401`: 缺 `Authorization: Bearer ...`
  - `404` / `405`: URL 可能不是 Streamable HTTP endpoint，若使用者給的是 base URL，再試 `.../mcp`
  - `400 protocol_version_mismatch`: 換候選版本重試
  - `404 session_not_found`: 重新 `initialize`
  - `406 not_acceptable` on `GET /mcp`: 代表你用錯 `Accept`，不是 server 掛掉
- 只有這時才去看根路徑 `GET /` 是否回傳 transport 描述，或判斷是不是 legacy SSE。

### Step 6: Finalization and QA
- 交付前比對 `references/fast-sop.md` 與 `references/quality_checklist.md`。
- 回覆順序固定為：
  1. 能不能連
  2. 用了哪個 endpoint 與 negotiated protocol version
  3. 工具清單
  4. 若失敗，具體卡點與下一步
- 若此 skill 與 `skill-creator-advanced` 工具鏈一起維護，可先跑共用格式檢查與最小驗證。
- Validate outputs against the checklist in `references/quality_checklist.md`

## Testing plan

### Triggering tests
- Should trigger:
  - "請用這個 streamable http 連結"
  - "幫我確認這個 `/mcp` 有沒有連上"
  - "把這個 MCP server 的工具列出來"
  - "為什麼我 GET `/mcp` 只有 400"
- Should NOT trigger:
  - "幫我做一個新的 MCP server"
  - "幫我修 OpenCV tool 的參數"
  - "幫我摘要 MCP 規格文件"
- Near-miss / confusing cases:
  - 使用者給的是 base URL 而不是 `/mcp` endpoint，此時應先試 exact URL，再補試 `.../mcp`。
  - 使用者看到 `GET /mcp -> 400` 就以為 server 掛掉，此 skill 必須直接糾正這個前提。
  - 宿主 `list_mcp_resources` 為空，不代表 user-provided URL 不可用。

### Functional tests
- Test case: streamable HTTP fast path
  - Given:
    - 使用者提供一個可用的 `http://127.0.0.1:9091/mcp`
  - When:
    - 先做 `POST initialize`，再做 `POST tools/list`
  - Then:
    - 取得 session id、negotiated protocol version，以及至少一個 tool 名稱

- Test case: wrong health check assumption
  - Given:
    - `GET /mcp` 回 `400` 或 `406`
  - When:
    - 改走 `POST initialize`
  - Then:
    - 若 server 正常，應能成功握手，並說明先前的 `GET` 不能作為判活依據

- Test case: auth required
  - Given:
    - server 對 `POST /mcp` 回 `401`
  - When:
    - 讀取錯誤 body / headers
  - Then:
    - 明確要求 bearer token，不誤判為 endpoint 不存在

### Performance comparison (optional)
- Baseline (no skill):
  - 先查宿主 resources、先看 repo、先用錯誤的 `GET /mcp`，通常需要多輪探索才意識到要做 initialize
- With skill:
  - 直接 1 次 initialize + 1 次 tools/list，失敗時才進 error matrix

### ROI guardrail
- Quality gain must justify extra:
  - Time:
    - 目標是把可用性判定壓到 30-90 秒內
  - Tokens:
    - 只保留與端點驗證直接相關的輸出
  - Maintenance burden:
    - 版本候選、錯誤矩陣與 probe script 必須保持精簡

### Regression gates
- Minimum pass-rate delta: 0.0
- Maximum allowed time increase: 20 秒
- Maximum allowed token increase: 1500
- Maximum under-trigger failures: 1
- Maximum over-trigger failures: 1

### Feedback loop
- Common failure signals:
  - 先去查宿主 resources，花很多時間才發現 URL 本身其實可連
  - 把 `GET /mcp` 的 `400` 當成 server 死掉
  - 用 PowerShell HTTP 指令得到無診斷價值的例外
- Likely fix:
  - 收斂 description 的 trigger phrases，並優先要求使用 `scripts/probe_streamable_http.py`

## Eval workflow

- Save approved prompts to `assets/evals/evals.json`
- Define release thresholds in `assets/evals/regression_gates.json`
- 若此 skill 與 `skill-creator-advanced` 工具鏈一起維護，可沿用共用 eval workspace 流程準備 paired runs。
- If the environment supports subagents or parallel workers, launch with-skill and baseline runs in the same batch
- After runs complete, aggregate results and generate a review viewer
- 若此 skill 與 `skill-creator-advanced` 工具鏈一起維護，可沿用共用 regression gates 檢查發版門檻。

## Distribution notes

- Packaging: 由宿主或 registry 的標準 SKILL 發佈流程處理；若在本 repo 維護，再使用 repo 根目錄的打包腳本。
- Repo-level README belongs *outside* this skill folder.

## Troubleshooting

- Symptom: `GET /mcp` 直接回 `400` 或 `406`
- Cause: 你把需要 session / 正確 `Accept` 的 endpoint 當成裸 health check
- Fix: 改做 `POST initialize`，成功後再談 `GET /mcp`

- Symptom: `tools/list` 回 `session_not_found`
- Cause: 少帶 `Mcp-Session-Id`，或原 session 已過期 / 被刪除
- Fix: 重新 `initialize`，用新的 session headers 重送

- Symptom: 宿主 MCP resources 是空的
- Cause: URL 尚未註冊到宿主工具層，與遠端 endpoint 可用性是不同問題
- Fix: 先用 raw HTTP probe 驗證 URL，再決定是否需要宿主整合

## Resources

- `scripts/probe_streamable_http.py`: 對 user-provided URL 做 deterministic initialize + tools/list
- `references/fast-sop.md`: 30-90 秒最短路徑
- `references/error-matrix.md`: 常見 HTTP / MCP 錯誤分流
- `references/quality_checklist.md`: 交付前自檢
