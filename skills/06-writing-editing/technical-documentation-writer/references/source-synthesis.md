# Source Synthesis

這份 skill 主要整合了 5 個外部來源的共同強項，並刻意去掉重複或過度模板化的部分。

## 1. GitHub awesome-copilot: documentation-writer

採用的要點：
- 先釐清讀者與文件目標，再開始寫
- 文件應使用清楚、簡潔、可維護的 Markdown 結構
- 技術文件要主動補範例、前置條件與 troubleshooting

沒有直接照搬的部分：
- 過於通用的寫作建議。這些建議對任何寫作都成立，對 skill 觸發與流程幫助有限。

來源：
- https://github.com/github/awesome-copilot/blob/main/skills/documentation-writer/SKILL.md

## 2. OpenClaw: afrexai-technical-docs

採用的要點：
- 用 Diataxis 做文件類型路由
- 對程序型文件強調前置條件、步驟、驗證與已知限制
- 依讀者層級調整資訊密度與術語

沒有直接照搬的部分：
- 某些角色或產品綁定的描述，因為這份 skill 需要更通用。

來源：
- https://github.com/openclaw/skills/blob/main/skills/1kalin/afrexai-technical-docs/SKILL.md

## 3. MCP Market: documentation-builder

採用的要點：
- 覆蓋的文件範圍不只 README，還包括架構文件、API 文件、貢獻指南與 release notes
- 強調從現有產品資訊或程式碼整理成文件，而不是只做語言潤飾

來源：
- https://mcpmarket.com/tools/skills/documentation-builder

## 4. MCP Market: write-user-docs

採用的要點：
- 補足 user guide、manual、FAQ、step-by-step instructions 等偏終端使用者文件
- 將「任務完成」放在文件成功標準之前面

來源：
- https://mcpmarket.com/tools/skills/write-user-docs

## 5. MCP Market: user-guides-and-tutorials

採用的要點：
- 補強 onboarding、feature walkthrough、training content、migration guide
- 強調從零開始建立一套文件時，需要先做 docs gap analysis

來源：
- https://mcpmarket.com/tools/skills/user-guides-and-tutorials

## Synthesis decisions

- 保留 Diataxis 做主路由，因為它最能防止文件類型混淆。
- 保留 docs audit / gap analysis，因為很多「請幫我寫文件」其實先該盤點缺口。
- 補上一個 deterministic 的 `doc_quality_audit.py`，讓這個 skill 不只是寫法建議。
- 明確排除 PRD、spec、投影片與純行銷寫作，避免和其他 skill 搶任務。
