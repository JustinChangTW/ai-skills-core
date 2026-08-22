---
name: financial-statement-analysis
description: 在使用者要解讀財報、比較三表、檢查盈餘品質或辨識財務紅旗時使用。常見觸發像「幫我看這份年報」「解讀 10-K / 10-Q」「看現金流和淨利有沒有背離」「比較兩家公司的財報體質」。輸出口徑清楚、可追溯的財報分析結論；不直接取代即時股價判斷、投資建議或純證據摘錄。
license: MIT
metadata: {"author":"Allan Yiin","language":"zh-TW","category":"analysis","short-description":"以附註、三表橋接、比率與紅旗清單為核心的財報解讀工作流程"}
---

# Financial Statement Analysis

## Purpose

這個 skill 用來把財報數字還原成可檢查的經營敘事，而不是只報幾個比率或直接喊多空。
它的核心順序固定是：先確認財報口徑與會計政策，再做三表一致性與盈餘品質檢查，最後才做比率、同業/期間比較與風險紅旗判讀。

## Scope

### In scope
- 解讀年報、季報、10-K、10-Q、法說補充資料中的財務表現與風險。
- 檢查損益表、資產負債表、現金流量表與附註是否互相支持。
- 比較同一家公司多期財報，或同業公司在相同口徑下的財務體質。
- 辨識盈餘品質、營運資金壓力、槓桿風險、一次性項目與常見會計紅旗。
- 需要把結論回指到報表行、附註、會計政策或官方申報來源。

### Out of scope
- 即時股價、盤中交易、技術分析、短線買賣建議。
- 只有單一頁面摘錄、頁碼搜尋或引用整理，沒有要求完整解讀流程的任務。
- 只有翻譯、改寫或整理成報告/簡報，沒有實際財報分析判斷的任務。
- 法律、審計、稅務或正式會計意見書。
- 在沒有財報、附註或可信來源時，硬做精確估值或投資結論。

## Primary use cases (2-3)

1) **單一公司財報解讀**
- Trigger examples: "幫我看這份 10-K 的重點", "解讀這家公司的年報，重點看現金流和負債。"
- Expected result: 先交代會計口徑與資料範圍，再整理核心發現、三表橋接、比率與風險紅旗。

2) **多期或同業比較**
- Trigger examples: "比較這家公司 2023-2025 的財報體質", "幫我比較兩家同業的獲利品質與槓桿風險。"
- Expected result: 用一致口徑比較趨勢或同業差異，明確說明哪些差異來自會計政策、分類方式或資本結構。

3) **盈餘品質與紅旗診斷**
- Trigger examples: "淨利一直成長，但現金流很差，幫我看是不是有問題", "幫我找這份財報有沒有會計操縱紅旗。"
- Expected result: 從淨利到 CFO 的橋接、營運資金變動、Capex/負債/權益變化與附註交叉驗證，指出紅旗與待確認缺口。

## Workflow overview

1. 先界定公司、期間、幣別、合併或個別報表、會計準則與資料來源。
2. 先讀附註與會計政策，確認收入認列、存貨、折舊/攤銷、租賃、減損、研發資本化等會不會改寫比率含義。
3. 由損益表出發，建立淨利到 CFO 的橋接，再對照 Capex、借款、股利與權益變動做三表一致性檢查。
4. 只在口徑清楚後才計算比率，並按產業決定哪些比率有解釋力。
5. 區分已確認事實、合理推論與缺口，最後整理紅旗、待確認事項與使用者該怎麼解讀。

## Communication notes

- User vocabulary: 財報、財務報表、年報、季報、10-K、10-Q、三表、現金流、盈餘品質、財務比率、估值、紅旗。
- Avoid jargon:
  - 把 `earnings quality` 說成「盈餘品質」
  - 把 `working capital bridge` 說成「營運資金橋接」
  - 把 `reclassification` 說成「重分類/口徑重整」
- Least-surprise rule:
  - 使用者期待的是「先講口徑，再講結論」，不是先丟一堆比率。
  - 若資料不足，直接點出缺口，不用推測補洞。
  - 除非使用者明確要求，預設不直接給買進/賣出建議。

## Routing boundaries

- Neighboring skills / workflows:
  - `longdoc-evidence-reader`: 任務只是從長年報或 10-K 找頁碼、段落與證據鏈。
  - `concept-alignment`: 使用者先要對齊 IFRS、US GAAP、產業結構或近期事件背景。
  - `technical-documentation-writer`、`slide-content-planner`: 財報分析完成後，要轉成報告、memo 或簡報。
  - `fermi-estimation`: 任務是粗估市場規模、產能或需求，不是解讀既有財報。
- Negative triggers:
  - "幫我看今天這支股票能不能買。"
  - "把這份 10-K 附註逐頁找出來。"
  - "直接幫我把英文財報翻成中文。"
  - "先幫我查這個產業最近發生什麼事。"
- Handoff rule:
  - 任務重點如果變成「證據摘錄」「背景研究」「文件改寫」或「即時交易判斷」，就不該由本 skill 硬攔。

## Language coverage

- Primary language(s): 繁體中文，次要支援英文財務術語與中英混寫請求。
- Mixed-language trigger phrases: financial statements、earnings quality、10-K analysis、cash flow divergence、ratio analysis、red flags、peer comparison。
- Locale-specific wording risks:
  - 「財報」先確認是合併還是個別、年報還是季報。
  - 「現金流很好/很差」必須對照利息分類、租賃本金、一次性項目與營運資金方向。
  - 「便宜/昂貴」如果沒有估值基準與期間口徑，不能直接下定論。

## Success criteria

### Quantitative (targets)
- Trigger accuracy: 至少 90% 的明顯財報解讀/三表分析需求能命中。
- Output completeness: 100% 交代分析範圍、口徑、三表橋接、風險紅旗與待確認缺口。
- Freshness-sensitive facts: 100% 對「最新/當季/目前/今天」這類要求改用當下查證的官方或監管來源。
- False certainty: 0 次把缺資料的推測包裝成已確認結論。

### Qualitative
- 先看附註與會計政策，再看比率。
- 先做三表一致性，再做故事敘述。
- 會區分經營改善、一次性因素與會計分類差異。
- 會明確標示哪些結論來自報表事實，哪些只是推論。

## Instructions

使用 `references/output-template.md` 的段落順序作為預設輸出骨架，交付前對照 `references/quality_checklist.md` 自檢。
若要看 should-trigger 與 handoff 的 fixture 形狀，另外參考 `references/fixture-examples.md`。

### Global rules
- 先確認分析標的是哪一份財報，以及使用者要的是「單一公司解讀」「多期比較」「同業比較」還是「紅旗診斷」。
- Provided files 與官方申報優先於二手摘要；若需要最新資料、同業當前倍數或目前申報狀態，必須上網查官方或監管來源。
- 先看會計政策與附註，再算比率；不要先算先講。
- 同業或跨期比較必須盡量統一口徑：會計準則、期間長度、幣別、合併範圍、重大一次性項目。
- 若發現 IFRS 與 US GAAP 差異會影響結論，要直接寫明，例如利息/股利現金流分類、LIFO、減損迴轉、研發資本化或資產重估。
- 若使用者沒有提供足夠資料支撐判斷，不要用猜測填滿模板。

### Step 0: Confirm inputs
- Read the existing conversation/files first; ask follow-up questions only when a wrong assumption would materially change the outcome.
- 至少確認以下資訊：
  - 公司名稱、期間、幣別、財報類型
  - 合併或個別報表
  - 會計準則或申報市場
  - 使用者真正要解的問題：體質、成長、槓桿、現金流、估值或紅旗
- 若使用者提到「最新」「目前」「今天」「本季」，一定要查具體日期與最新申報狀態。

### Step 1: Define scope and accounting basis
- 先列資料來源與分析範圍，不要直接跳到結論。
- 先讀附註與會計政策摘要，特別檢查：
  - 收入認列方式
  - 存貨成本公式與跌價/迴轉
  - 折舊與攤銷政策
  - 租賃上表與租賃負債
  - 減損與減損迴轉
  - 研發或開發成本資本化
- 若口徑不一致，先建立「報導口徑」與「分析口徑」的差異說明。

### Step 2: Build the three-statement bridge
- 從損益表的淨利或營業利益出發，對照現金流量表與資產負債表。
- 先做 `淨利 -> 非現金項目 -> 營運資金變動 -> CFO` 的橋接。
- 再檢查：
  - Capex 與固定資產/使用權資產變動是否一致
  - 借款、償債、增資、股利與權益/有息負債變動是否一致
  - 權益變動表是否能解釋期初到期末權益變化
- 若三表之間只能靠「其他」項目勉強對上，要列入紅旗或待確認事項。

### Step 3: Compute ratios only after normalization
- 用最少但有解釋力的比率，不要堆表。
- 優先考慮：
  - 獲利能力：毛利率、營業利益率、淨利率、ROA、ROE、ROIC
  - 償債能力：流動比率、速動比率、負債權益比、利息保障倍數、淨負債/EBITDA
  - 營運效率：DSO、DIO、DPO、CCC、總資產週轉率
  - 現金能力：CFO/淨利、CFO/總負債、FCF
- 同業比較時，優先使用同產業、相近商業模式與相近會計準則的公司。
- 若某比率在該產業本來就失真，例如拿 CCC 評銀行，必須直接指出不適用。

### Step 4: Identify red flags and alternative explanations
- 至少檢查以下紅旗：
  - 淨利成長但 CFO 長期疲弱
  - DSO、DIO 或其他營運資金指標惡化
  - 毛利率異常跳升但缺乏價格/產品/成本解釋
  - Capex、無形資產或「其他資產」異常上升
  - 一次性利益、資產處分或重分類讓本業看起來變好
  - 關聯人交易、回購/回售安排或特殊目的結構
- 每個紅旗都要同時寫：
  - 觀察到的事實
  - 可能的合理解釋
  - 為何仍需要警戒
  - 還缺哪些附註或資料才能定性

### Step 5: Render the final answer in the exact contract
- 預設輸出依 `references/output-template.md` 的標題順序。
- 每個主要結論都要盡量回指到報表行、附註、會計政策或官方申報來源。
- 明確區分：
  - 已確認事實
  - 分析推論
  - 缺口 / 待確認事項
- 除非使用者明確要求，不要把財報分析直接延伸成投資指令或目標價。

### Step 6: Finalization and QA
- 對照 `references/quality_checklist.md` 檢查是否先講口徑再講結論。
- 若做了同業或跨期比較，確認口徑一致或已明示調整。
- 若內容含「最新」或當前市場資訊，確認資料日期與事件日期。
- Run `python scripts\\check_skill_name_surface.py --repo-root .`
- Run `python scripts\\validate_skills.py --repo-root .`

## Testing plan

### Triggering tests
- Should trigger:
  - "幫我解讀這份 10-K，重點看現金流、負債跟盈餘品質。"
  - "比較這家公司最近三年的財報體質，順便看三表有沒有矛盾。"
  - "這家公司淨利很好看，但現金流很差，幫我找紅旗。"
  - "請幫我比較兩家同業的財報，注意 IFRS 跟 US GAAP 口徑差異。"
- Should NOT trigger:
  - "幫我看今天這支股票要不要買。"
  - "把這份年報附註所有頁碼列出來。"
  - "直接把這份英文財報翻成中文。"
  - "先幫我查這個產業最近有什麼新聞。"
- Near-miss / confusing cases:
  - 使用者上傳 10-K，但只要頁碼與證據摘錄，這比較像 `longdoc-evidence-reader`。
  - 使用者說要看財報，其實只是在要即時股價判斷或 valuation call，不應誤判成完整財報解讀。
  - 使用者要比較跨市場公司，若不先統一口徑，很容易把會計差異誤判成體質差異。

### Functional tests
- Test case: 單一公司年報解讀
  - Given: 使用者提供一份年報或 10-K，要理解體質與風險
  - When: 啟動本 skill
  - Then:
    - 先交代資料範圍與會計口徑
    - 會從三表橋接出發，而不是直接列比率
    - 會區分已確認事實、推論與缺口

- Test case: 同業跨準則比較
  - Given: 使用者要比較 IFRS 與 US GAAP 公司
  - When: 啟動本 skill
  - Then:
    - 會先說明哪些比率或現金流分類可能不可直接比
    - 會做口徑調整或清楚標示不可比處
    - 不會把制度差異直接寫成經營優劣

- Test case: 盈餘品質紅旗診斷
  - Given: 使用者指出淨利成長但現金流背離
  - When: 啟動本 skill
  - Then:
    - 會做淨利到 CFO 的橋接
    - 會點出營運資金、一次性項目或資本化疑點
    - 會列待確認附註與需要追查的項目

- Test case: 應拒絕即時交易任務
  - Given: 使用者要的是今天的買賣建議
  - When: 啟動本 skill
  - Then:
    - 不會假裝財報解讀已足夠支撐短線交易結論
    - 不會硬套完整財報分析模板

### Performance comparison (optional)
- Baseline (no skill): 常見失敗是先報比率、忽略附註與會計政策、沒有做三表橋接、把一次性因素誤當成體質改善。
- With skill: 會先處理口徑，再做三表一致性、比率與紅旗分析，能顯著降低誤判與過度自信。

### ROI guardrail
- Quality gain must justify extra:
  - Time: 只有在能換到更可靠的體質判讀與風險揭露時，才值得做完整橋接與口徑調整。
  - Tokens: 不為了完整而把所有比率都列一遍；只保留真正有解釋力的項目。
  - Maintenance burden: 詳細比率與資料來源規則放在 `references/`，避免主檔膨脹。

### Regression gates
- Minimum pass-rate delta: `+0.10`
- Maximum allowed time increase: `120s`
- Maximum allowed token increase: `10000`
- Maximum under-trigger failures: `1 / eval batch`
- Maximum over-trigger failures: `1 / eval batch`

### Feedback loop
- Common failure signals:
  - 先講結論、沒先講口徑
  - 只列比率，沒有三表橋接
  - 把 IFRS / US GAAP 差異當成公司體質差異
  - 沒有分清事實、推論與缺口
  - 直接延伸成買賣建議
- Likely fix:
  - 收緊 description 中對「財報解讀」「三表」「盈餘品質」「紅旗」的 trigger wording
  - 補強 `references/source-hierarchy.md` 與 `references/ratio-and-red-flag-guide.md`
  - 在 evals 中加入跨準則比較與拒絕即時交易案例

## Eval workflow

- Save approved prompts to `assets/evals/evals.json`
- Define release thresholds in `assets/evals/regression_gates.json`
- 若此 skill 與 `skill-creator-advanced` 工具鏈一起維護，可沿用共用 eval workspace 流程準備 paired runs。
- If the environment supports subagents or parallel workers, launch with-skill and baseline runs in the same batch
- After runs complete, aggregate results and generate a review viewer

## Distribution notes

- Packaging: 由宿主或 registry 的標準 SKILL 發佈流程處理；若在本 repo 維護，再使用 repo 根目錄的打包與驗證腳本。
- Repo-level README belongs *outside* this skill folder.

## Troubleshooting

- Symptom: 回答只是在複述財報數字，沒有真正解讀。
  - Cause: 沒有從附註、三表橋接與口徑差異切入。
  - Fix: 回到 Step 1 與 Step 2，先重建口徑與橋接，再下結論。

- Symptom: 比率很多，但看不出重點。
  - Cause: 沒有依產業與問題選比率，只是在堆指標。
  - Fix: 只保留最能解釋使用者問題的 4-8 個指標，並寫明理由。

- Symptom: 同業比較很混亂，結論互相打架。
  - Cause: 沒有先統一會計準則、分類與期間口徑。
  - Fix: 依 `references/source-hierarchy.md` 重新做口徑對齊，必要時直接標示不可比。

- Symptom: 看到紅旗就直接定性成舞弊。
  - Cause: 把紅旗篩檢當成定罪。
  - Fix: 每個紅旗都補上合理替代解釋與待確認證據，維持「風險提示」而非「直接判決」。

## Resources

- `references/output-template.md`
- `references/quality_checklist.md`
- `references/overlap-matrix.md`
- `references/test_plan.md`
- `references/trigger-eval-summary.md`
- `references/source-hierarchy.md`
- `references/ratio-and-red-flag-guide.md`
- `assets/evals/evals.json`
- `assets/evals/regression_gates.json`
