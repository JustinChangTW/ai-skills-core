# 品質檢查清單

這份 checklist 用來記錄 humanize-text 目前是否符合 `skill-creator-advanced` 的 readiness gate 規範。
本次 audit 以 `quick_validate.py`、`format_check.py`、`audit_skill_references.py` 與 `SKILL.md` 結構掃描為基礎，並保留 skill 專屬檢核項。

## 最終關卡
- Audit date: 2026-05-11
- Compliance level: 中高
- Overall status: DRAFT BLOCKED / PUBLISH BLOCKED
- Automated checks:
  - [x] `python -m json.tool skills\humanize-text\assets\evals\evals.json` passed
  - [x] `python -m json.tool skills\humanize-text\references\trigger-evals.json` passed
  - [x] `python scripts\audit_skill_references.py --repo-root .` passed
  - [x] `python skills\skill-creator-advanced\scripts\audit_structure.py skills\humanize-text --json` passed
  - [x] `python skills\skill-creator-advanced\scripts\audit_workflow_contract.py skills\humanize-text --json` passed
  - [x] `python skills\skill-creator-advanced\scripts\audit_lifecycle.py skills\humanize-text --json` passed
  - [x] `python skills\skill-creator-advanced\scripts\audit_lifecycle_state.py skills\humanize-text --json` passed
  - [x] `python skills\skill-creator-advanced\scripts\audit_eval_coverage.py skills\humanize-text --json` passed
  - [x] `python skills\skill-creator-advanced\scripts\audit_golden_trigger_set.py skills\humanize-text --json` passed
  - [x] `python skills\skill-creator-advanced\scripts\audit_migration_governance.py skills\humanize-text --json` passed
  - [ ] `python skills\skill-creator-advanced\scripts\release_gate.py skills\humanize-text --stage draft --json` blocked by incomplete benchmark evidence
- Key observations:
  - humanize-text 的 JSON、format、structure、workflow、lifecycle、eval coverage、golden trigger、migration governance 與 reference audit 已通過。
  - draft release gate 目前只剩 benchmark audit 失敗；現有 release evidence 缺 `run_summary`、benchmark metadata 與 paired benchmark 結構，不能用人工 notes 假裝通過。
- Key improvements in 2026-05-11 update:
  - 補入 role、decision boundary 與 default follow-through policy。
  - 補入通用 AI pattern catalog、voice profiles、domain exceptions。
  - 補入 detect / rewrite / edit 模式與第二輪 anti-AI audit。
  - 補入 audience-effect mapping、stance inventory、formal marker cluster 檢查。
  - 補入 coherence pass，檢查論點矛盾、換詞重複、顆粒度跳躍、階層斷裂與假轉折。
  - 補入三段式輸出契約，要求 `前置處理`、`改寫結果`、`前後指標比較` 之間使用 Markdown 分隔線。
  - 補入 `structural rewrite` 策略，避免高目的性改寫只沿用既有段落微調。
  - 補入可見化執行流程，要求 rewrite / edit 任務先列印 TODO、AI 味盤點、受眾與用途、改寫策略與保留邊界。
  - 補入 before/after 指標比較，要求以列表殘影、重複句型、模板轉場、段落節奏、受眾明確度與事實漂移風險檢查改寫結果。
  - 擴充 functional eval，覆蓋英文 pattern、detect-only、學術例外、格式殘影、受眾缺席、觀點平均化、過度條列 / 破折號痕跡與論點連貫性。
  - 補入 `compatibility` frontmatter、`<workflow>`、`<output_contract>`、`references/readiness_report.md`、`skill_lifecycle.yaml` 與 draft release evidence。
- Structural gaps to keep improving:
  - 尚未建立 paired with-skill / baseline benchmark archive
  - worked examples 仍偏少，後續可補到 references 而非塞入 SKILL.md

## 格式檢查
- [x] skill folder 名稱符合 kebab-case
- [x] `SKILL.md` 存在且通過基本 frontmatter 驗證
- [x] `format_check.py` 為 0 errors / 0 warnings
- [x] `SKILL.md` 內提到的本地 `scripts/`、`references/`、`assets/` 路徑都存在
- [x] `references/quality_checklist.md` 已存在且已依本次 audit 更新
- [x] `SKILL.md` 中沒有待清理的 `TODO` / `[TODO]`

## 需求與政策檢查
- [x] `SKILL.md` 有明確 workflow / instructions
- [x] 有獨立 `role` 區塊或等價角色定義
- [x] 有獨立 decision boundary 區塊或等價使用邊界
- [x] 有明確 output contract / output shape 要求
- [x] 有明確 workflow contract / Action-Input-Output-Validation 摘要
- [x] 有明確 default follow-through policy / ask-first 邊界
- [x] 有工具或路由使用規則
- [ ] 有 worked examples / examples 支撐輸出品質

## 常見錯誤檢查
- [x] 沒有失效的本地引用路徑
- [x] frontmatter / 命名 / description 沒有被 validator 擋下
- [x] 結構與文字格式沒有被 linter 擋下
- [x] readiness gate 所期待的關鍵區塊已大致具備
- [x] checklist 已與新版 readiness gate 結構對齊

## Skill 專屬檢查
Use this checklist before packaging or shipping a new version.

### 結構
- [ ] Folder name is kebab-case
- [ ] SKILL.md exists
- [ ] YAML frontmatter starts and ends with ---
- [ ] Frontmatter has name and description
- [ ] No README.md inside skill folder

### 觸發
- [ ] Triggers on obvious "humanize / 去 AI 味 / 改自然 / 不要列點" queries
- [ ] Triggers on zh, en, and mixed-language paraphrases
- [ ] Does not trigger on bytes/time/number humanize library requests
- [ ] Does not trigger on detector evasion or cheating requests
- [ ] Does not steal pure translation, research, or spec-writing queries

### Functionality
- [ ] Core workflow preserves meaning and key terms
- [ ] Traditional Chinese guidance is explicit and actionable
- [ ] Rewrite / edit output prints visible process before final prose
- [ ] Process output includes AI-pattern diagnosis, audience/use case, rewrite strategy, and preservation boundaries
- [ ] Process output uses three major sections: `前置處理`, `改寫結果`, and `前後指標比較`, separated by `---`
- [ ] Process output includes visible argument-coherence checks for contradiction, repeated terms, granularity jumps, hierarchy breaks, and fake transitions
- [ ] Rewrite strategy can escalate to `structural rewrite` when audience and purpose require a new opening or reordered argument flow
- [ ] Final prose defaults to paragraph prose
- [ ] Final prose contains no bullet or ordered lists
- [ ] Before/after comparison covers list residue, repeated sentence patterns, template transitions, paragraph rhythm, audience clarity, and fact-drift risk
- [ ] Output does not promise detector bypass
- [ ] Output does not fabricate personal experience

### 維護
- [ ] Trigger evals are saved in references/trigger-evals.json
- [ ] Functional evals are saved in assets/evals/evals.json
- [x] Regression gates are defined in assets/evals/regression_gates.json
- [x] No-list checker script exists and is documented
- [x] Pattern catalog, voice profiles, and domain exceptions are covered by functional evals
- [x] Audience-effect mapping and stance inventory are covered by functional evals
- [x] Formal marker cluster cleanup is covered by functional evals
- [x] Coherence and argument-flow checks are covered by functional evals
- [x] Draft readiness report exists
- [x] Draft lifecycle file exists
- [x] Draft release evidence exists
- [x] Cross-platform compatibility is declared in frontmatter

