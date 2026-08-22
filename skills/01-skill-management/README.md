# Skill 管理

搜尋、建立、檢核、優化與持續演進 AI Skills。

本分類目前收錄 **4 個 Skills**。若任務跨越多個分類，先依主要交付成果選擇 Skill，再視需要交接其他能力。

## Skills 清單

| Skill | 中文名稱 | 主要用途 |
|---|---|---|
| [`allanyiin-skill-creator-advanced`](allanyiin-skill-creator-advanced/README.md) | Skill 進階製作 | 在使用者要建立、改版或檢核 skill 時使用 |
| [`allanyiin-skill-evolution`](allanyiin-skill-evolution/README.md) | Skill Evolution（技能演化） | 適用於使用者要把失敗的 agent 執行、人工修正、regression、trigger 失敗或 skill library drift 轉成具體 skill 更新、eval、rollback、merge、split 或 retirement 決策。不適用於沒有失敗證據的全新 skill 建立；那類任務請用 skill-creator-advanced |
| [`allanyiin-skill-optimizer`](allanyiin-skill-optimizer/README.md) | Skill Optimizer | 在使用者要用 benchmark、rollout、held-out validation、bounded edits 或 SkillOpt 式流程系統化優化既有 skill 時使用。輸出可重跑的 optimization plan、eval split、候選修改、gate 結果與採納/回退決策；不適用於從零建立 skill、沒有評分資料的失敗事後檢討，或直接微調模型權重 |
| [`capability-evolver`](capability-evolver/README.md) | 能力進化器（Capability Evolver） | 根據使用者的實際任務盤點能力缺口，從官方目錄、可信 Skill 儲存庫或公開來源尋找、稽核、比較及推薦最合適的 Skill，經使用者選定後安全安裝或更新，使可用能力持續進化 |

## 使用方式

1. 先從上表選擇最接近主要成果的 Skill。
2. 點進 Skill 的 `README.md` 查看用途、適用情境與快速指令。
3. 在支援 Skills 的環境中直接描述任務，或用 `$skill-name` 明確指定。
4. 真正影響 AI 執行行為的是各 Skill 目錄內的 `SKILL.md`。

回到 [Skills 總目錄](../../CATALOG.md) 或 [版本庫首頁](../../README.md)。
