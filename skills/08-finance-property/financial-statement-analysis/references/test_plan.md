# Test Plan: financial-statement-analysis

## 1) Triggering tests

Goal: the skill loads when it should, and stays off when it should not.

### Should trigger (8-10)

Use obvious requests, paraphrases, real user wording, and file-type/tool variants.

- 幫我看這份年報
- 解讀 10-K / 10-Q
- 看現金流和淨利有沒有背離
- 比較兩家公司的財報體質
- 幫我做財報體檢，尤其看 notes 裡的租賃和減損
- Please analyze this annual report and focus on earnings quality
- Use the filing, not news articles, to assess financial health
- 幫我看這家公司舉債、股利和資本支出有沒有互相對得起來

For each item, record:
- Expected: trigger
- Actual:
- Notes:

### Should NOT trigger (8-10)

- 今天這支股票到底能不能買？看一下短線走勢
- 列出 10-K 裡 revenue recognition 與 lease obligations 的頁碼
- 把 annual report 翻成繁體中文，不需要分析
- 先整理 IFRS 跟 US GAAP 差異，不要分析任何公司
- 研究半導體產業近六個月發生了什麼事
- 把我已有的財務分析改寫成 board memo
- 幫我粗估這家公司的 TAM
- Give me a concise summary of the annual report with citations only

For each item, record:
- Expected: no trigger
- Actual:
- Notes:

### Near-miss / confusing cases

- 上傳 10-K，但只要 footnote page citations，不要 interpretation
- 先做 IFRS / US GAAP 概念對齊，再決定要不要分析公司
- 已經有分析結論，只要整理成 memo / report / slides
- 提到 company / market，但其實是在估算 TAM，不是看財報

### Multilingual coverage

- zh:
  - 幫我看這份年報
  - 這家公司淨利好看但現金流很差，幫我找紅旗
- en:
  - Please analyze this annual report and focus on earnings quality
  - Read the filing like a forensic analyst and tell me the red flags
- mixed:
  - 幫我看這份 10-Q，net income 不錯但 operating cash flow 很弱
  - 根據 quarterly filing 看 notes 裡的 lease liabilities / impairment / capex

### Neighboring skills / overlap map

- Closest competing skill:
  - `longdoc-evidence-reader`
  - `concept-alignment`
  - `technical-documentation-writer`
- Why this skill should win:
  - 使用者要的是財務判讀、三表橋接、比率比較與紅旗分析
- Why another skill should win in adjacent cases:
  - 只要頁碼/引用時由 `longdoc-evidence-reader` 接
  - 先整理制度背景時由 `concept-alignment` 接
  - 已有分析只要改寫成 memo / report 時由 `technical-documentation-writer` 接

### Trigger diagnostics

#### Under-trigger signals
- [ ] Obvious request failed to load the skill
- [ ] Only one specific wording works
- [ ] Real user phrasing fails but clean paraphrase works

#### Over-trigger signals
- [ ] Unrelated requests load the skill
- [ ] Broad generic keywords cause false positives
- [ ] Requests that belong to another skill still load this one

#### Likely fix direction
- If under-trigger dominates: revise `description`
- If over-trigger dominates: narrow scope or add negative triggers
- If both happen: split scope or rewrite `description` from scratch

## 2) Functional tests

Goal: outputs and tool usage are correct end-to-end.

Create test cases in Given/When/Then form. Prefer real tasks over invented textbook prompts.

### Test case A (happy path)
- Given: 使用者提供一份年報或 10-K，要理解公司體質與風險
- When: 啟動本 skill
- Then:
  - 先交代分析範圍與會計口徑
  - 從三表橋接出發，而不是直接列比率
  - 區分已確認事實、推論與缺口

### Test case B (edge case)
- Given: 使用者要求比較 IFRS 與 US GAAP 公司
- When: 啟動本 skill
- Then:
  - 先說明不可直接比較的口徑差異
  - 不把制度差異直接寫成經營優劣

### Test case C (failure mode / error handling)
- Given: 使用者只提供模糊指令，例如「幫我看財報好不好」
- When: 缺公司、期間、幣別或財報來源
- Then:
  - 只在缺口會實質改變結論時追問
  - 不在資料不足時假裝下確定結論

### Test case D (recovery path)
- Given: 使用者一開始要求財報解讀，但澄清後其實只要 citation extraction 或 memo rewriting
- When: 發現主要 outcome 已改變
- Then:
  - 停止擴張財報解讀
  - handoff 到對應鄰近 skill

### Failure classification
- If a test fails, label the primary cause:
  - Trigger problem
  - Workflow / instruction problem
  - Resource / script problem
  - External tool / MCP problem

## 3) Performance comparison

Goal: prove the skill improves baseline.

### Baseline (without skill)
- Result quality:
- Total messages / back-and-forth:
- Tool calls:
- Failed tool calls / retries:
- Token usage (if available):
- User corrections required:
- Main failure points:

### With skill
- Result quality:
- Total messages / back-and-forth:
- Tool calls:
- Failed tool calls / retries:
- Token usage (if available):
- User corrections required:
- Main failure points:

### Benchmark summary
- Better than baseline?
- If yes, why?
- If no, what got worse?
- Is the skill helping, or just adding more instructions?

### ROI review
- Is the quality gain worth the extra time/tokens?
- Does this skill reduce user corrections?
- Does this skill reduce operational risk or only add complexity?
- If this were maintained for 6 months, would it still be worth keeping?

## 4) Iteration log

### Round 1
- Change made:
- Hypothesis:
- Result:
- Next move:

### Round 2
- Change made:
- Hypothesis:
- Result:
- Next move:

## 5) Operationalize these cases

- Mirror approved prompts into `assets/evals/evals.json`
- Create an iteration workspace with the shared skill-creator toolchain, for example `python skills/skill-creator-advanced/scripts/prepare_eval_workspace.py <path/to/skill>`
- Save with-skill and baseline outputs in the paired workspace layout
- Generate `benchmark.json` / `benchmark.md`
- Generate `review.html` for human review
- Define release gates in `assets/evals/regression_gates.json`
- Validate release gates with the shared skill-creator toolchain, for example `python skills/skill-creator-advanced/scripts/check_regression_gates.py <benchmark.json> --config <gates.json>`

## 6) Release readiness checklist

- [ ] format_check.py has 0 errors
- [ ] quick_validate.py passes
- [ ] All functional tests pass
- [ ] Multilingual trigger coverage reviewed
- [ ] Neighboring skill overlap reviewed
- [ ] Under-trigger risks addressed
- [ ] Over-trigger risks addressed
- [ ] Baseline comparison completed
- [ ] ROI review completed
- [ ] Regression gates pass
- [ ] Real-user or near-real test prompts included
- [ ] Version bumped (top-level version: YYYY.M.D)
- [ ] Distribution instructions updated (repo-level docs outside skill folder)
