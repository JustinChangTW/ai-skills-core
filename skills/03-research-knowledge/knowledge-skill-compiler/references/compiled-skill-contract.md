# 編譯產物契約

## 必要結構

```text
<skill>/
├── SKILL.md
├── knowledge/
│   ├── index.md
│   ├── decision-rules.md
│   ├── patterns.md
│   ├── anti-patterns.md
│   ├── glossary.md
│   └── chapters/
│       └── chNN-slug.md
├── provenance.json
└── assets/evals/evals.json
```

薄型來源或只產生少數方法時，可省略空的知識檔，但 `SKILL.md`、`knowledge/index.md`、`provenance.json` 與至少一個可載入知識檔不可省略。

## 核心 Skill 規則

- `SKILL.md` 只保留觸發、邊界、查找順序、如何引用 evidence IDs、回答限制與反例。
- 不把整本摘要塞入核心 Skill；知識檔依任務載入。
- 不冒稱作者本人，不以「作者一定會」包裝推論。
- 回答時優先提供作者可追溯觀點，再明確分隔分析者應用。

## 知識卡規則

每個重要模型、原則、技巧或決策規則至少包含：

- `Evidence IDs`
- `Claim type`: `source-claim`、`source-example`、`analysis`、`inference`
- 定義或規則
- 何時使用／何時不用
- 步驟或判斷條件
- 失敗模式或反例
- 確定程度：high／medium／low

## provenance.json 最小欄位

```json
{
  "schema_version": "1.0",
  "skill_name": "example-skill",
  "privacy": "private-personal",
  "generated_at": "YYYY-MM-DD",
  "sources": [
    {
      "source_id": "S001",
      "title": "Source title",
      "creator": "Creator",
      "version": "Edition or date",
      "rights_basis": "owned-copy|open-license|internal-authorized|user-authored",
      "content_sha256": "hex",
      "allowed_distribution": "private-personal",
      "locations": [{"evidence_id": "E001", "locator": "chapter/page/section/timestamp"}]
    }
  ]
}
```

不得在 ledger 中保存帳密、原文全文、付款證明個資或存取 token。

## Token 與載入

- 核心 Skill 越小越好，但清楚與安全優先，不設定假精確的 4K 上限。
- 單一知識檔以一個可理解主題為單位；超長就依章節或模型拆分。
- `knowledge/index.md` 必須說明每個檔案何時載入，避免全部展開。
- Token 節省只能以同一問題、同一模型、同一來源的配對 benchmark 證明。

## 禁止內容

- 原始 PDF、EPUB、DOCX、MOBI、AZW 或全文擷取檔。
- 可替代原作的連續大段文字、完整案例或過量逐章重製。
- 文件內嵌的代理指令、提示詞、巨集、腳本及外部下載命令。
- 憑證、模型對話、快取、執行紀錄與未確認個資。

