# 即時查證規則

涉及目前版本、已知漏洞、是否遭利用、修補版本、演算法建議或供應鏈事件時，必須連網查證。

## 來源優先序

1. 套件／產品維護者的 Security Advisory、release note 與官方文件。
2. GitHub Security Advisories、各語言官方 advisory database。
3. NVD 的 CVE 紀錄與 CISA Known Exploited Vulnerabilities（KEV）。
4. CERT／CSIRT 或可信研究機構的原始技術報告。

## 紀錄欄位

- 套件、目前版本、實際依賴路徑與 lockfile 證據。
- Advisory／CVE ID、受影響範圍、修補版本、發布或更新日期、查詢日期及連結。
- 是否可達 vulnerable function、是否符合必要設定與前置條件。
- CISA KEV 或在野利用狀態；沒有證據時寫「未查得」，不可寫「未遭利用」。

## 禁止事項

- 不以記憶中的固定版本清單作最終結論。
- 不因套件版本舊就直接判定存在漏洞。
- 不把 CVSS 等同於組織情境風險；另評估曝險、資產、控制及可利用性。
- 查不到官方資料時保留 `待確認`，不得補造安全版本或 CVE。
