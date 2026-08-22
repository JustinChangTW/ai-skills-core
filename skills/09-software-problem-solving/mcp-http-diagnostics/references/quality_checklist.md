# Quality checklist

這份 checklist 用來記錄 mcp-http-diagnostics 目前是否符合 `skill-creator-advanced` 的 readiness gate 規範。
本次 audit 以 `quick_validate.py`、`format_check.py`、`audit_skill_references.py` 與 `SKILL.md` 結構掃描為基礎，並保留 skill 專屬檢核項。

## Final gate
- Audit date: 2026-03-24
- Compliance level: 中
- Overall status: PARTIAL
- Automated checks:
  - [x] `quick_validate.py` passed
  - [x] `format_check.py` passed
  - [x] `audit_skill_references.py` passed
- Key observations:
  - 自動檢查全數通過。
  - 本次將舊 checklist 升級為 readiness gate 結構。
- Structural gaps to keep improving:
  - 缺少明確 role 區塊
  - 缺少明確 decision boundary 區塊
  - output contract 不夠明示
  - default follow-through policy 不夠明示
  - 缺少 worked examples / examples 區塊

## Format checks
- [x] skill folder 名稱符合 kebab-case
- [x] `SKILL.md` 存在且通過基本 frontmatter 驗證
- [x] `format_check.py` 為 0 errors / 0 warnings
- [x] `SKILL.md` 內提到的本地 `scripts/`、`references/`、`assets/` 路徑都存在
- [x] `references/quality_checklist.md` 已存在且已依本次 audit 更新
- [x] `SKILL.md` 中沒有待清理的 `TODO` / `[TODO]`

## Requirement and policy checks
- [x] `SKILL.md` 有明確 workflow / instructions
- [ ] 有獨立 `role` 區塊或等價角色定義
- [ ] 有獨立 decision boundary 區塊或等價使用邊界
- [ ] 有明確 output contract / output shape 要求
- [ ] 有明確 default follow-through policy / ask-first 邊界
- [x] 有工具或路由使用規則
- [ ] 有 worked examples / examples 支撐輸出品質

## Common error checks
- [x] 沒有失效的本地引用路徑
- [x] frontmatter / 命名 / description 沒有被 validator 擋下
- [x] 結構與文字格式沒有被 linter 擋下
- [ ] readiness gate 所期待的關鍵區塊已完整具備
- [x] checklist 已與新版 readiness gate 結構對齊

## Skill-specific checks
### Triggering
- [ ] 看到「streamable http 連結」「`/mcp` 連不上」「列工具清單」能正確觸發
- [ ] 不會因為一般 MCP 教學或修 server 程式而誤觸發

### Workflow
- [ ] 先做 `POST initialize`，不是先做裸 `GET /mcp`
- [ ] `initialize` 成功後立刻做 `tools/list`
- [ ] 只有在失敗時才看根路徑描述或 legacy transport
- [ ] 不把宿主 `list_mcp_resources` 當成 user-provided URL 的真實狀態

### Output
- [ ] 先給可用/不可用結論
- [ ] 有回報實際 endpoint 與 negotiated protocol version
- [ ] 有整理工具名稱與參數重點
- [ ] 失敗時有具體下一步，不只說「連不上」

### Determinism
- [ ] 優先使用 `scripts/probe_streamable_http.py`
- [ ] probe script 可在無第三方套件下執行
- [ ] probe script 能處理 auth、protocol fallback、base URL 補 `/mcp`
