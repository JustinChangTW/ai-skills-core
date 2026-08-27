# Justin 的私人 AI Skills 備份庫

這個版本庫保存個人使用的 AI Skills。每個大分類與每個 Skill 都有一份供人閱讀的繁體中文 `README.md`，並保留完整資料夾，包括 `SKILL.md`、`references/`、`scripts/`、`assets/`、測試案例與介面設定（若原 Skill 有提供）。

## 分類

| 目錄 | 用途 | 代表 Skills |
|---|---|---|
| `01-skill-management` | Skill 搜尋、建立、優化與演進 | 能力進化器、Skill Creator、Optimizer |
| `02-cybersecurity` | 資安稽核、程式安全、惡意程式與威脅情資 | 臺灣 ISMS、Secure Code Review、暗網情資 |
| `03-research-knowledge` | 深度研究、論文、長文件與知識編譯 | arXiv、研究寫作、知識能力編譯器 |
| `04-speaking-communication` | 一般口語、觀點演講、說服與話術辨識 | 口語表達教練、TED 風格演講、倫理說服 |
| `05-taipei-tm` | 台北市健言社 TM 專用角色 | 講員、講評、總評、主席、計時 |
| `06-writing-editing` | 寫作、自然化、技術文件與包容性編修 | Humanizer、長文、技術文件 |
| `07-presentations-visual` | 簡報規劃、PPTX、視覺與圖像製作 | 簡報自然化、投影片規劃、PPTX |
| `08-finance-property` | 財報、隱形冠軍與臺灣買房 | 財報分析、隱形冠軍雷達、買房攻略 |
| `09-software-problem-solving` | 軟體設計、需求、問題拆解與 MCP | 前端、Spec、Vibe Coding、MCP 診斷 |
| `10-video-media` | 剪輯、字幕、短影音、旅遊與教學影片 | Video Editor、Short、Subtitle |
| `11-learning-exams` | 證照考試、題目拆解、記憶與複習 | 證照英文小老師 |
| `12-governance-policy` | 政府預算、政策、議事程序與公共事實查核 | 臺灣政府預算查核員 |

完整清單見 [CATALOG.md](CATALOG.md)，檔案完整性見 [SHA256SUMS.txt](SHA256SUMS.txt)。

## 管理原則

1. 一個 Skill 只放在一個主要分類，避免重複版本。
2. 跨領域關係寫在目錄，不複製 Skill。例如「安全程式碼審查」可交接「臺灣 ISMS 稽核」。
3. 新增 Skill 時，依主要工作成果分類，不依使用的工具或偶然關鍵字分類。
4. 分類不確定時，先放最常被使用者尋找的類別，再在總目錄增加標籤。
5. 不備份登入資訊、快取、執行紀錄、`.env`、私鑰、Token 或憑證。

## 還原方式

從指定分類找到 Skill 資料夾，將完整資料夾匯入支援 Agent Skills 的環境。不同平台的安裝位置可能不同；不要只複製 `SKILL.md`，否則 references、scripts 或 assets 可能遺失。

## 更新備份

`scripts/export-skills.sh` 會從本機個人 Skills 目錄重新匯出、清除 Python 快取，並替所有分類及 Skill 更新 `README.md`；執行後請先查看差異、執行 `scripts/validate-backup.sh`，確認無敏感資訊再提交。
