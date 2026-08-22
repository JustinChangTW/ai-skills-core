# 免費來源路由

所有最新狀態、API限制與授權條款均需回官方來源重新確認。

| 任務 | 優先免費來源 | 補充來源 | 限制 |
|---|---|---|---|
| 已知資料外洩 | Have I Been Pwned 公開查詢／已驗證網域功能 | Mozilla Monitor | API、敏感外洩與大量網域功能可能付費；查 Email 涉及個資 |
| Infostealer 線索 | Hudson Rock 免費工具 | HIBP stealer-log相關功能 | 免費資料深度與欄位有限 |
| 惡意 URL／樣本／C2 | URLhaus、MalwareBazaar、ThreatFox、Feodo Tracker | AlienVault OTX | 社群資料可能誤判；禁止開啟 IOC 或下載樣本 |
| 已遭利用漏洞 | CISA KEV | 各國 CERT、產品供應商公告 | KEV 不等於組織一定受影響，需比對資產與版本 |
| 攻擊者、活動與 TTP | MITRE ATT&CK、官方 CERT、原廠事件報告 | OTX Pulses | 名稱可能不同，活動歸因通常有不確定性 |
| 自有網段感染／暴露 | Shadowserver 免費網路擁有者報告 | 自有 EASM、SIEM、EDR | 需驗證網路所有權；DNS sinkhole來源可能不是實際感染終端 |
| 釣魚及仿冒網域 | Certificate Transparency、URLhaus、PhishTank | DNS／RDAP、官方品牌通報 | 相似名稱不等於惡意；不要對可疑站點主動登入 |
| 勒索事件聲稱 | 勒索事件公開聚合與CERT／公司公告 | 新聞與研究報告 | 勒索站聲稱屬未驗證資訊；不得直接進站或下載證據包 |
| 公開秘密外洩 | GitHub等平台的官方秘密掃描與組織告警 | 自有程式碼掃描 | 僅調查有權限的組織與儲存庫，不搜尋或使用他人秘密 |
| 臺灣情資 | TWCERT/CC、數位發展部、主管機關與受影響業者公告 | 國際CERT交叉驗證 | 媒體轉載不能取代原始公告 |

## 最小查詢組合

- 帳密疑似外洩：HIBP＋Hudson Rock線索；再以Entra ID／AD／VPN／EDR內部紀錄驗證。
- 惡意IOC：abuse.ch平台＋OTX或原廠報告；檢查首次、最後觀察及可信度。
- 勒索聲稱：公開聚合＋企業／CERT公告；沒有內部證據時維持「未驗證聲稱」。
- 漏洞攻擊：CISA KEV＋供應商公告＋資產版本；再查WAF／EDR／網路日誌有無利用痕跡。
- 仿冒品牌：CT／RDAP＋URLhaus或PhishTank；使用安全截圖或供應商資料，不直接互動。

OpenCTI Community或MISP適合日後作為儲存、關聯與去重中樞；它們本身不是情報來源，也不會讓免費資料變成完整暗網資料。
