# 遷移治理

此 Skill 目前為新建版本，沒有取代既有 Skill。

- Rename：若改名，保留舊名稱的明確轉址與負向觸發測試，確認新舊名稱不會同時搶任務。
- Merge：不得併入 `taiwan-isms-audit-expert`，除非程式碼審查與制度稽核仍維持獨立工作流程及輸出。
- Split：若未來動態測試需要大量工具、較高權限或不同授權流程，必須拆成獨立 Skill。
- Deprecate：先標記替代者、遷移日期與使用者影響，通過負向及鄰近 Skill 回歸測試後才停用。
- Evidence：所有名稱、邊界或 lifecycle 變更須更新 `skill_lifecycle.yaml`、evals 與 readiness report。
