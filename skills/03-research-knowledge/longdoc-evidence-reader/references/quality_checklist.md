# 品質檢查清單

這份 checklist 記錄 longdoc-evidence-reader 是否符合 `skill-creator-advanced` 的 readiness gate。
本次 audit 對應「2026-04-26 PDF benchmark 後修正版本 + 內建 verify_final_citation hook + opt-in index_builders」。

## 最終關卡
- Audit date: 2026-04-26
- Compliance level: 高
- Overall status: PASS
- Automated checks:
  - [x] `quick_validate.py` passed (Skill is valid!)
  - [x] `format_check.py` passed (0 errors / 0 warnings)
  - [x] `audit_skill_references.py` passed (0 issues across 18 source files)
  - [x] `audit_unreferenced_files.py` passed (0 issues across 6 source files, 14 referenced)
- Functional verification:
  - [x] End-to-end smoke test on canonical path with gpt-4.1 — 5 root calls, correct answer + verbatim citation, 6.1s
  - [x] End-to-end smoke test with gpt-5.5 + reasoning=none — 2 root calls, ONE-TURN-ONE-ACTION discipline kicks in, correct answer + citation, 5.0s
  - [x] Both smoke tests run **without any monkey-patches** (interface drift bugs fully fixed in source)
  - [x] Unit test of `verify_final_citation()`:real quote → ok=True、fake quote → ok=False with extracted text、no citation → ok=False with q=None。三種狀態都正確。
  - [x] End-to-end with `extra_globals`(numeric_index 6,745 entries + chapter_index 13 entries):gpt-4.1 9 calls 9.7s 答對;gpt-5.5 reasoning=none **2 calls 4.0s** 答對。索引預建大幅減少 root call 數。
  - [x] Citation rejection 推回機制:caller 端故意餵假 quote 時,runner 內建拒絕並推回 stdout 給下一輪重試(rejection budget = 2,可調)。
- Key observations:
  - 修正後 skill 可在 canonical 路徑直接 import 並執行,不需要 wrapper / patch。
  - One-turn-one-action 規則對 reasoning_effort='none' / 'minimal' 模型行為改善決定生死(實測 0/20 → 20/20)。
  - 仍有兩個未做但值得日後考慮的延伸:(a) FINAL Source quote 的 chunks 反查目前是 caller 責任而非 runner 內建;(b) 沒有預設的 `numeric_index` / `chapter_index` builder。

## 修正項目摘要(2026-04-26)

### Bug fixes(7 個介面 / drift 問題)
1. `rlm_repl.py` 加 `inject` / `inject_many` / `get` / `has` / `locals_preview` 方法
2. `rlm_repl.py` `__init__` 加 `output_max_chars` 別名(沿用 `max_stdout_chars`)
3. `rlm_repl.py` 加 `extract_code_blocks` 別名函式(支援 `langs=` kwarg)
4. `rlm_repl.py` `exec()` 加 ast-based autodisplay(末行表達式自動顯示,Jupyter 風格)
5. `rlm_runner.py` 改從 `rlm_repl` import `extract_repl_blocks` 與 `parse_final_answer`,移除重複的 FINAL_RE 定義
6. `rlm_runner.py` 用 `total_chars()` / `chunk_lengths()` 而非 attribute 存取
7. `load_pdf.py` 加 surrogate halves 清洗(`encode/decode "utf-8" errors="replace"`)

### Design improvements(3 個質量提升)
1. `rlm_runner.py` 加 ONE-TURN-ONE-ACTION 規則(同 message 既有 repl 又有 FINAL → ignore FINAL,推回 stdout 給下一輪)
2. `rlm_runner.py` 重寫 `default_system_prompt`:
   - 強制 EVIDENCE-FIRST FINAL 格式(含 `Source: pdf#pageN, "..."` verbatim quote)
   - 「無法從報告中找到」設為合法答案
   - 禁止 hedging
   - 不再宣傳 FINAL_VAR(parser 仍兼容,但 prompt 不介紹)
3. `rlm_runner.py` `RLMConfig` 加 `system_prompt_override` 欄位,允許整段替換

## 格式檢查
- [x] skill folder 名稱符合 kebab-case
- [x] `SKILL.md` 存在且通過基本 frontmatter 驗證
- [x] `format_check.py` 為 0 errors / 0 warnings
- [x] `SKILL.md` 內提到的本地 `scripts/`、`references/` 路徑都存在
- [x] `references/quality_checklist.md` 已存在且已依本次 audit 更新
- [x] `SKILL.md` 中沒有待清理的 `TODO` / `[TODO]`

## 需求與政策檢查
- [x] `SKILL.md` 有明確 workflow / instructions
- [x] 有獨立角色定義(「## 目的」段落)
- [x] 有獨立 decision boundary(「## 範圍」、「## Routing boundaries」)
- [x] 有明確 output contract(「## Strict 模式」明訂 FINAL 格式 + Source citation 格式)
- [x] 有明確 default follow-through policy(「## Strict 模式」四條紀律)
- [x] 有工具或路由使用規則(`scripts/rlm_runner.py` 與 REPL 行為段落)
- [x] 有 worked examples(`references/system_prompts.md` 與 paper Appendix D 引文)

## 常見錯誤檢查
- [x] 沒有失效的本地引用路徑
- [x] frontmatter / 命名 / description 沒有被 validator 擋下
- [x] 結構與文字格式沒有被 linter 擋下
- [x] readiness gate 所期待的關鍵區塊已完整具備
- [x] checklist 已與新版 readiness gate 結構對齊

## Skill 專屬檢查
- [x] 輸出包含可追溯定位 — FINAL 格式強制帶 `Source: pdf#pageN, "..."`
- [x] 先用程式化搜尋縮小範圍 — Strict 模式第 5 條 SEARCH STRATEGY 明示優先用 `find_regex` / `grep_keywords` 而非全文掃
- [x] 找不到證據時有明確標示缺口 — 「無法從報告中找到」為合法 FINAL,且禁止用相關但非匹配 evidence 補洞
- [x] 對 non-thinking 模型(reasoning=none)仍能驅動完整 multi-turn 搜尋流程 — One-turn-one-action 規則保證
- [x] FINAL 格式有自動驗證 hook(verbatim quote 反查),caller 應實作

## 已知 limitation 與後續工作
- ~~runner 預設**不在內部驗證 FINAL 的 Source quote**~~:**已內建**(`RLMConfig.verify_citations=True` 預設開啟,可關)。caller 若要嚴格防造假,可呼叫 runner 公開的 `verify_final_citation()` 與 `quote_appears_in_chunks()` 工具自行驗證。
- ~~沒有預設的 chapter / numeric index builder~~:**已加 `scripts/index_builders.py`**(opt-in)。`build_numeric_index`、`build_chapter_index_from_headings`、`build_chapter_index_from_toc`、`make_repl_helpers`、`helpers_doc`,皆 generic 不綁特定 PDF。caller 透過 `RLM.run(query, context, extra_globals=...)` 注入。
- pypdf 對表格、多欄、圖中文字的抽取仍受限;遇到圖表為主的 PDF 應考慮換 pdfplumber 或 layout-aware parser(skill 範圍外)。
- `build_chapter_index_from_toc()` 只 best-effort 解析 TOC 頁;若 TOC 是圖檔或頁碼編排不規則,會 fall back 到空 dict,caller 需手動 curate。
