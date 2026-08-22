# 安全程式碼審查

對 PR、commit、diff、原始碼、設定檔、IaC、API、套件鎖定檔及 SAST／SCA／SARIF 結果執行證據導向的應用安全審查，追蹤輸入到危險操作的資料流、驗證可利用性、降低誤報並提出需人工核准的修補方案。當使用者說安全程式碼審查、AI 資安審查、PR security review、Vibe Coding 上線檢查、Injection、Secrets、Auth、Dependency、Crypto、金融交易程式安全、弱點修補或要求檢查程式碼是否安全時使用；不適用於純 ISMS／法規制度稽核、外部威脅情資、惡意程式樣本分析或未經授權的滲透攻擊。

## 基本資料

- Skill ID：`secure-code-review`
- 分類：`02-cybersecurity`
- 版本：`未標示`
- 主要指令：[SKILL.md](SKILL.md)

## 快速使用

在支援 Skills 的環境中，可以直接描述任務；若要明確指定，可使用：

```text
$secure-code-review 請依我的目標與現有資料完成任務，並列出需要我確認的事項。
```

建議一併提供目標、使用情境、已知資料、限制條件，以及希望取得的成果格式。若資料不足，Skill 會依核心指令只詢問真正影響結果的問題。

## 內容結構

- `SKILL.md`：AI 執行此能力時採用的核心指令
- `agents/`：介面顯示與觸發設定（1 個檔案）
- `references/`：按需求載入的參考資料（7 個檔案）
- `assets/`：產出時可使用的素材或範本（3 個檔案）

## 維護說明

本 README 供人員瀏覽、搜尋與版本管理；真正影響 AI 行為的是 `SKILL.md` 及其引用的資源。修改功能時，應優先更新核心指令，再重新檢查本說明是否仍一致。
