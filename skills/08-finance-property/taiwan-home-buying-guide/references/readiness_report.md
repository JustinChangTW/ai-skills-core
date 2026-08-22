# Readiness report

- Skill: `taiwan-home-buying-guide`
- Audit date: 2026-08-11
- Archetype: pipeline / reviewer
- Primary job: 臺灣自住買方購屋決策支援
- Host: ChatGPT / Codex agent skills
- Skill revision: 2026.8.11
- Creation evidence: 官方 quick validation PASS；進階 Gate 的 top-level version 要求與官方 frontmatter schema 衝突，不作為安裝放行依據。
- Benchmark: not run; no ROI、核貸成功率或價格準確率宣稱
- External limits: 官方網站可用性、銀行個案授信、未公開社區與產權文件仍需人工或專業確認

## Boundaries

- In scope: 入門、找房、估價、CP、房仲、議價、貸款試算、盡職調查、簽約交屋導航。
- Out of scope: 海外房產、純租屋、銷售文案、違法授信規避、專業法律／估價／結構／核貸決定。

## Release evidence

驗證完成後，以實際命令結果更新；人工文字不得覆蓋機械 FAIL。

## Format and structure checks

- Official frontmatter and folder validation: PASS on 2026-08-11.
- Required role, boundary, workflow, output and follow-through blocks: authored.

## Requirement and policy checks

- Current-source verification, financial/legal professional boundaries, privacy and illegal-loan refusal are mandatory.

## Common error checks

- Prevents treating listing price as market value, promised LTV as approval, few comps as precise valuation, or a low price as high CP without hidden-cost review.
