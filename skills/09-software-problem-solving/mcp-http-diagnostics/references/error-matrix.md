# Error Matrix

## Fast triage

### `POST initialize -> 200`
- 意義：Streamable HTTP endpoint 可用。
- 下一步：立即做 `tools/list`。

### `POST initialize -> 401`
- 意義：需要 bearer token。
- 下一步：補 `Authorization: Bearer ...`，不要誤判成 server 壞掉。

### `POST initialize -> 404` 或 `405`
- 意義：URL 很可能不是正確的 Streamable HTTP endpoint。
- 下一步：
  - 若使用者給的是 base URL，補試 `.../mcp`
  - 若仍失敗，再檢查是否其實是 legacy SSE 或其他 HTTP API

### `POST initialize -> 400` 且錯誤是 `protocol_version_mismatch`
- 意義：版本不合，或 header/body 版本不一致。
- 下一步：
  - 確保 header 與 body 的 `protocolVersion` 相同
  - 依序回退版本候選

### `POST tools/list -> 404` 且錯誤是 `session_not_found`
- 意義：session 遺失、過期或沒帶對。
- 下一步：重新 `initialize`，用新 session id 重送。

### `GET /mcp -> 406`
- 意義：`Accept` 錯了；這不是判活方式。
- 下一步：改回 `POST initialize` 或用 `Accept: text/event-stream` 搭配既有 session。

### 根路徑 `GET / -> 200` 且 body 描述 `transport=streamable_http`
- 意義：這可以幫你確認 server 類型，但它不是比 `POST initialize` 更快的成功路徑。

## Core rule

如果目標是「確認有沒有連上、拿工具清單」，真正權威的流程永遠是：

`POST initialize` -> session headers -> `POST tools/list`
