# 方法與授權

本 Skill 以使用者需求重新設計，未直接複製第三方 Skill；吸收下列公開方法概念：

- GitHub `awesome-copilot/security-review`：日常程式碼審查分類、信心標示、修補先提案後核准。來源採 MIT License：<https://github.com/github/awesome-copilot/tree/main/skills/security-review>
- Trail of Bits `differential-review`：風險優先的差異審查、Git 歷史、安全回歸、影響範圍與測試缺口。原始專案授權依其 repository 為準：<https://github.com/trailofbits/skills/tree/main/plugins/differential-review>
- Cloudflare `security-audit-skill`：攻擊面盤點、具體攻擊路徑、對抗式誤報消除與獨立複核。來源採 MIT License：<https://github.com/cloudflare/security-audit-skill>

主要差異：本 Skill 預設單一代理亦可執行、採最小範圍與只讀模式、不自動做動態攻擊、強制遮罩秘密、要求即時官方漏洞查證，並加入臺灣金融業技術檢查及跨 Skill 分流。
