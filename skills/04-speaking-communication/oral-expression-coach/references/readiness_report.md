# Readiness report

- Skill: `oral-expression-coach`
- Audit date: 2026-08-11
- Skill revision: 2026.8.11
- Archetype: coach / reviewer
- Primary job: 診斷並訓練真實口語表達
- Host: ChatGPT / Codex agent skills
- Benchmark: 未執行，不宣稱訓練成效或跨 Host 表現
- External limits: 實際聲音與台風需錄音／影片；醫療問題需專業評估

## Boundaries

- In scope: 即席、會議、主管報告、自我介紹、面試、問答、聲音與台風的可觀察訓練。
- Out of scope: 純稿件潤飾、TM三分鐘故事演講、簡報製作、操弄型說服、語言／心理醫療診斷。

## Validation evidence

- Official frontmatter and folder validation: PASS on 2026-08-11.
- Workflow, semantics, eval coverage, migration and reference hygiene: PASS on 2026-08-11.
- Final official gate and eval quality: PASS on 2026-08-11.
- 進階工具要求 top-level `version`，與目前官方 frontmatter schema 衝突；官方驗證結果為安裝依據。

## Format and structure checks

- SKILL.md 採單一主要工作、明確鄰近邊界、六步 workflow、固定 output contract 與停止條件。
- 詳細框架、診斷、情境及練習分離至按需 references。

## Common error checks

- 無音訊時不得判斷音量、語速、語調或發音。
- 無影片時不得判斷眼神、表情或肢體。
- 不虛構面試與工作經驗，不以單次表現診斷醫療狀況。
- 一次只修正一個最大瓶頸，不用漂亮逐字稿取代實際練習。
