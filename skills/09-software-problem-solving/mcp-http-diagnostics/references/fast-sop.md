# MCP Streamable HTTP 快速 SOP

目標：在 30-90 秒內確認 user-provided URL 是否真的是可用的 Streamable HTTP MCP endpoint，並拿到工具清單。

## 最短成功路徑

1. 若使用者已提供完整 `.../mcp`，直接打該 URL，不要先改路徑。
2. 直接做 `POST initialize`，不要先做裸 `GET /mcp`。
3. 成功後立刻記錄：
   - `Mcp-Session-Id`
   - `MCP-Protocol-Version`
4. 立刻做 `POST tools/list`。
5. 回覆「是否可用 + 工具清單 + 下一步」。

## 不該先做的事

- 不要先查宿主 `list_mcp_resources`。那只代表宿主目前已掛上的 server，不代表使用者給的 URL 有沒有活著。
- 不要先做 repo 全域搜尋。先確認端點活著，必要時再回頭讀程式碼。
- 不要把 `GET /mcp -> 400` 直接判成故障。對 Streamable HTTP，這常常只是你走錯握手路徑。
- 不要優先用不穩定的 ad-hoc HTTP 指令。先用 deterministic Python probe。

## 推薦命令

```bash
python scripts/probe_streamable_http.py "http://127.0.0.1:9091/mcp" --pretty
```

## 什麼時候才看根路徑 `/`

只有在 `POST initialize` 失敗時，才去看根路徑是否回傳：

- transport 類型
- 建議 endpoint，例如 `/mcp`
- 是否其實是別種 transport
