# Migration governance

重新命名、合併、拆分、淘汰或取代 `skill-vault` 時，必須記錄舊名稱、新名稱、原因、生效日、相容策略、回復條件，以及受影響的目錄、README、觸發案例與 host 設定。

## Rename

保留舊觸發語句的測試，更新資料夾、目錄與所有本地引用。

## Deprecate

指定替代 Skill、通知文字、移除日期與 rollback 條件。

## Merge

只有在合併後仍維持「Skills 備份與復原」單一責任時允許。

## Split

分別定義備份、驗證或還原的路由邊界與交接規則。

## Compatibility

檢查既有名稱、路徑、目錄、README、host 設定與使用者慣用觸發語句；有意破壞相容性時須提供遷移與 rollback 方法。

## Migration Evidence

記錄 migration_type、from、to、effective_date、compatibility_policy、references_checked、evals_updated、wrappers_updated 與 release_gate_result。

任何 migration 都必須更新 evals、readiness report 與備份庫目錄，並重新通過 publish gate；不得用別名靜默改變遠端寫入權限。
