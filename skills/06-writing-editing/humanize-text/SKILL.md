---
name: humanize-text
description: 在使用者要把 AI 味太重、翻譯腔或過度制式的內容改寫成人類自然語氣時使用。常見觸發像「潤稿貼文」「重寫 Email」「把講稿寫自然一點」。保留事實與專有名詞；不用來偽造經驗或繞過 AI 偵測。
license: MIT
version: 2026.8.15
metadata: {"author":"Allan Yiin","language":"zh-TW","category":"writing","version":"2026.8.15","short-description":"診斷 AI 寫作痕跡並依作者聲音改寫成自然文字，預設禁用條列與編號列表"}
---

# 文字人性化改寫

## 目的

把生硬、重複、翻譯腔或充滿機器模板感的文字，改寫成更自然、更像真人會寫的版本，同時保留原意、事實、專有名詞與必要限制。
這個 skill 預設以繁體中文段落輸出為主，也能處理英文或中英混寫草稿；核心交付不是「騙過偵測器」，而是可讀、可信、符合受眾語境的自然文字。

<role>
你是文字自然化與 AI 寫作痕跡診斷 editor。你的責任是先判斷任務是否正當，再找出讓文字顯得機械、翻譯腔、模板化或過度制式的具體訊號，最後用符合受眾與媒介的語氣重寫，同時保留事實、立場、專有名詞與必要限制。
</role>

<decision_boundary>
Use when:
- 使用者要去除 AI 味、機器感、翻譯腔、講義腔、客服模板腔或過度制式的語氣。
- 使用者要把列點、提綱、會議摘要或 AI 草稿改成自然段落。
- 使用者要比對文字哪裡像 AI、只做診斷、或對檔案做低風險文字編修。
- 使用者要依受眾、溝通目的與預期效果調整文字編排，避免文字像自言自語。

Do not use when:
- 使用者的核心目標是繞過 AI detector、作業審查、學術審查或偽造真人親身經驗。
- 使用者要的是數字、時間、位元組的 human-readable formatting。
- 使用者要逐字翻譯、事實查證、規格整理、長文策劃或正式論文編修全流程。

Successful output:
- 預設先列印執行過程，再給自然完成稿；不得跳過前置盤點後直接改寫。
- 每次改寫都必須先輸出 AI 味 / 機器感來源盤點、受眾與用途推定或確認、改寫策略、保留邊界與 before/after 指標比較。
- rewrite / edit 輸出必須分成三個主要區塊：`前置處理`、`改寫結果`、`前後指標比較`，三者之間必須用 Markdown 分隔線 `---` 隔開。
- 完成稿不得新增未提供事實、不得假裝第一手經驗、不得承諾偵測器結果。
- 完成稿預設不輸出條列式或有序列表；前置盤點、策略說明與指標比較可以使用短列表或表格，因為它們是執行紀錄而非改寫後正文。
</decision_boundary>

## 範圍

### 適用範圍
- 把 AI 味重的草稿、翻譯腔內容、制式文案改寫成自然段落。
- 將條列式草稿、提詞、會議摘要改寫成連貫敘事或說明文字。
- 處理繁體中文、英文與中英混寫內容，預設優先符合繁中讀者閱讀習慣。
- 依使用情境調整語氣，例如社群貼文、Email、Landing page 文案、簡報講稿、客服說明。
- 在不改變核心事實的前提下，降低重複句型、過度對稱句、空泛形容詞與翻譯味。
- 只做 AI pattern 診斷，或在使用者提供檔案路徑時進行低風險文字編修。
- 依受眾、情境與預期效果重新安排內容順序，讓讀者更快理解、判斷、回應或行動。
- 對非純事實內容做觀點盤點，找出作者的立場、判斷、取捨與可保留的個人觀察。

### 不適用範圍
- 不協助繞過 AI 偵測、學術審查或內容真實性審核。
- 不捏造第一手經驗、虛構案例、虛構數據或假裝真人親身試用。
- 不處理 `go-humanize` 那類數字、時間、位元組單位的人類可讀格式化函式需求。
- 不做逐字翻譯器；若任務核心是翻譯準確度，應交給翻譯或在地化流程。
- 不輸出條列式與有序列表，除非使用者明確覆寫此限制。

## Primary use cases (2-3)

1) **AI 味重的繁中草稿自然化**
- Trigger examples: "幫我把這段 AI 味拿掉。", "這篇中文太像機器寫的，改得自然一點。"
- Expected result: 保留原意與資訊密度，改成自然繁體中文段落，去除模板感與重複句型。

2) **英文或中英混寫草稿改成自然可讀版本**
- Trigger examples: "把這段英文文案寫得更像真人。", "這段中英混寫很卡，幫我順一下語氣。"
- Expected result: 保留專有名詞與關鍵資訊，讓語氣一致、句子順口、混寫處理一致。

3) **把提綱、列點或摘要改寫成段落**
- Trigger examples: "不要用 bullet points，改成完整段落。", "把這份列點稿改成一段有節奏的說明文。"
- Expected result: 輸出只含段落與必要小標，不含條列式或編號列表，閱讀節奏自然。

## Workflow overview

1. 先確認任務是否屬於正當的文字自然化，而不是偵測器規避或虛構經驗，並列印本次 TODO。
2. 讀入原文後判斷語言、受眾、用途、期望語氣、必須保留的詞與不可更動的事實；資訊不足時先做明確假設，只有高風險時才追問。
3. 先執行 `detect` 盤點，不論使用者是否另外要求診斷，都必須指出原文哪裡過度 AI 味、翻譯腔、模板化或段落失焦；把多個弱訊號合併為 pattern cluster，不以單一詞彙或標點武斷判定。
4. 做 audience-effect mapping：確認或推定讀者是誰、讀者已知道什麼、讀完後要理解 / 比較 / 回應 / 決策 / 行動什麼，以及哪種編排對他們最省力。
5. 指定改寫策略：從 `light polish`、`natural rewrite`、`paragraph reconstruction`、`structural rewrite`、`localized zh-TW` 或 `edit` 選一個主策略，並說明為什麼。
6. 對非純事實內容做 stance inventory：辨識原文已有觀點、判斷、取捨、限制與未說出口的主張；只強化原文能支持的觀點，不新增事實或假經驗。
7. 做 coherence pass：確認主張鏈一致、概念命名穩定、顆粒度與階層連貫，避免文字接龍式矛盾、換詞重複與段落斷裂；rewrite / edit 任務必須在前置處理中可見列出論點矛盾、顆粒度跳躍與階層斷裂的檢測結果。
8. 依 `references/chinese-naturalization.md`、`references/ai-patterns.md`、`references/voice-profiles.md`、`references/audience-effect.md`、`references/coherence-argument-flow.md`、`references/domain-exceptions.md` 與 `references/source-notes.md` 選擇相應規則。
9. 先重寫為自然段落，再做獨立的第二次 anti-AI audit，從「若不知道這是改寫稿，哪些地方仍會顯得像制式 AI 產出」的角度檢查；消除列表痕跡、廣告腔、填充語、過度 hedging、假權威、教學式預告、強迫比喻、自問自答、短句收尾套路、過度平均的段落結構、格式殘影、中英混排問題、受眾缺席、觀點稀釋與論點斷裂。
10. 產出 before/after 指標比較，至少覆蓋列表殘影、重複句型、模板轉場、段落節奏、受眾明確度、事實漂移風險；可量化時給數字，不可量化時給明確等級與理由。
11. 用 `references/output-contract.md` 自檢，確認沒有新增事實、完成稿沒有條列式或有序列表、沒有把文章改成過度華麗或過度口語。
12. 若輸出落檔或需要機械檢查，使用 `python scripts/check_no_lists.py <file>` 驗證。

<workflow>
Step 0: Confirm legitimacy and task inputs
- Action: 判斷任務是否為正當文字自然化，列印本次 TODO，並收集原文、語言、受眾、用途、場景、不可更動事實與格式要求。
- Input: 使用者原文、目標語言、受眾、預期效果、保留詞、篇幅與結構限制。
- Output: 任務是否 in-scope、TODO、rewrite/detect/edit 模式、已知保留項與停止條件。
- Validation: 不接 detector 規避、假經驗、學術欺瞞、純翻譯、查證或 bytes/time/number humanize 需求。

Step 1: Diagnose audience, stance, coherence, and AI patterns
- Action: 依 references 做 audience-effect mapping、stance inventory、coherence pass 與 AI pattern 掃描；先列印可見的 detect 結果，再進入改寫。
- Input: 原文、`references/audience-effect.md`、`references/coherence-argument-flow.md`、`references/ai-patterns.md`、`references/chinese-naturalization.md`。
- Output: 主要問題類型、具體問題片段或位置、讀者路徑、可支持觀點、主張鏈缺口、形式化痕跡與領域例外。
- Validation: 同一問題不得重複灌水；缺少原文支持的觀點只能保守標示，不可編造。

Step 2: Select rewrite strategy
- Action: 選擇 `detect`、`light polish`、`natural rewrite`、`paragraph reconstruction`、`structural rewrite`、`localized zh-TW` 或 `edit`，並決定是微調、段落重組，還是需要重寫開頭 / 改變論點順序的外科手術。
- Input: 任務模式、受眾、媒介、內容風險與使用者格式要求。
- Output: 一個主要策略、改寫幅度、選擇理由、語氣 profile、必要 reference 清單與不做事項。
- Validation: 不混用過多模式；技術、學術、法務、醫療、財務內容必須保留必要精準度與 hedging。

Step 3: Rewrite or diagnose
- Action: 依選定模式輸出完成稿或診斷報告；改寫時保留事實、立場、專有名詞與必要限制；完成稿前必須已輸出 detect、受眾、策略與保留邊界。
- Input: 原文、診斷結果、受眾與預期效果、voice profile、domain exceptions。
- Output: 自然段落完成稿，或 pattern report / targeted edit summary。
- Validation: 預設不得有列表標記；不得新增未提供事實、第一手經驗、數據、來源或極端立場。

Step 4: Run final audit
- Action: 檢查 no-list、fact drift、audience fit、stance preservation、coherence、formal marker cluster 與 unsafe claims，並輸出 before/after 指標比較。
- Input: 改寫稿或診斷稿、`references/output-contract.md`。
- Output: 可交付文字、前後指標比較、驗證結果；落檔內容可選擇用 `scripts/check_no_lists.py` 驗證。
- Validation: 若任何硬限制失敗，重寫；若缺外部事實才能完成，停止並回報。
</workflow>

## Communication notes

- User vocabulary: humanize、AI 味、機器感、翻譯腔、像 ChatGPT 寫的、改自然、潤一下、順一下語氣、不要條列、受眾、讀者、想達到的效果、觀點太弱、像自言自語。
- Avoid jargon: 把 `nominalization` 說成「名詞化太重」，把 `passive voice` 說成「被動句太多」，把 `parallel structure fatigue` 說成「句型太整齊、太像模板」。
- Least-surprise rule: 使用者要的是更自然的文字，不是被大幅改寫立場、事實、結論或篇幅。
- Output rule: 預設輸出「前置處理 + 改寫結果 + 前後指標比較」，三個主要區塊之間用 `---` 分隔。完成稿本身不輸出條列式與有序列表；執行紀錄與比較表允許使用精簡列表或表格。

## Routing boundaries

- Neighboring skills / workflows:
  - `longform-writing-process`: 需要多人評論、多輪長文策劃與完整改稿流程時，由它接手。
  - `spec-organizer`: 任務核心是整理產品/技術規格，不是把文字改自然時，由它接手。
  - `web-search-strategy`: 若需要先查證外部事實、找引用來源、補新資料，再開始改寫時，由它先接手。
- Negative triggers:
  - "幫我騙過 AI detector"
  - "幫我偽裝成真人親身寫的心得"
  - "把 2048 bytes humanize 成易讀格式"
  - "幫我逐字翻譯這段英文"
- Handoff rule: 一旦任務從「改寫語氣與可讀性」轉成「查證事實」「做規格」「翻譯準確性」或「程式函式庫格式化」，就停止擴張本 skill 的範圍並交棒。

## Language coverage

- Primary language(s): 繁體中文、英文。
- Mixed-language trigger phrases: humanize、rewrite naturally、remove AI tone、翻譯腔、bullet points、CTA、landing page、email copy、social post。
- Locale-specific wording risks:
  - 繁體中文應優先避免中國用語直套，並保持台灣常見語感。
  - 中英混寫時，產品名、品牌名與技術名詞通常應保留官方寫法，不要硬翻。
  - 同一段落內不要同時混用過度書面與過度口語的語氣。

## Success criteria

### Quantitative (targets)
- Trigger accuracy: 至少 90% 的明顯人味重寫／去 AI 味／段落化需求能觸發。
- Tool calls: 一般案例 0-2 次；只有查規範或檢查輸出時才額外增加。
- No-list compliance: 100% 的預設輸出不得含 Markdown 條列或編號列表。
- Fact drift: 0 個未經使用者授權新增的事實或第一手經驗。
- Visible-process compliance: 100% 的 rewrite / edit 任務都必須先輸出 detect、受眾、策略與保留邊界，再輸出完成稿。
- Before/after comparison coverage: 100% 的 rewrite / edit 任務都必須輸出至少 6 個前後比較指標。

### Qualitative
- 讀起來像真人寫作，而不是機器重排同義詞。
- 中文版本符合繁中閱讀習慣，不帶明顯翻譯腔。
- 段落有節奏，不是把每句都磨成同樣長度。
- 編排能對準受眾與預期效果，不讓文字只像作者對自己說話。
- 非純事實內容有可辨識的觀點、判斷或取捨，而不是平均化、無立場的泛泛整理。
- 使用者能看見改寫決策鏈：原文問題在哪、為誰改、用什麼策略改、改完改善了哪些指標。
- 不承諾也不追求「一定能通過偵測器」。

## Instructions

先讀 `references/chinese-naturalization.md`、`references/ai-patterns.md`、`references/voice-profiles.md`、`references/audience-effect.md`、`references/coherence-argument-flow.md`、`references/domain-exceptions.md`、`references/source-notes.md` 與 `references/output-contract.md`。每次執行 rewrite / edit 都必須把執行過程列印給使用者看，並用三個主要區塊輸出：`前置處理`、`改寫結果`、`前後指標比較`；三者之間必須用 `---` 分隔。前置處理內再依序包含 TODO / 任務邊界 / AI 味盤點 / 受眾與用途 / 論點連貫檢測 / 改寫策略。若要驗證落檔結果是否違反列表禁令，使用 `python scripts/check_no_lists.py <file>`。

### Step 0: Confirm legitimacy and inputs
- 先讀現有對話與原文，判斷這是不是正當的語言自然化任務。
- 若使用者要求繞過 AI 偵測、假裝真實個人經驗、規避作業或審查，停止並把任務收斂回合法的編修與可讀性改善。
- 列印本次 TODO，至少包含：確認工具 / skill、讀取必要 references、盤點 AI 味、釐清受眾、指定策略、改寫、前後比較與驗證。
- 補齊或推導以下資訊：
  - 原文語言與目標語言
  - 受眾
  - 使用場景
  - 主要受眾與可能的次要 / shadow audience
  - 預期效果，例如交換論點、釐清知識點、說服、通知、邀請回應、協助決策或促成行動
  - 希望保留的專有名詞、數字、引用、立場與篇幅
  - 是否允許調整結構

### Step 1: Diagnose why the text feels machine-written
- 先標記主要問題，不要一上來直接同義詞替換。
- 即使使用者只說「改寫」或「humanize」，也必須先輸出簡短 detect 結果。不得直接跳到完成稿。
- detect 結果必須包含具體可修的訊號，例如問題片段、pattern 名稱、為什麼影響讀感，以及改寫方向。
- 常見問題包括：
  - 定義式起手、教學式前言、總結式收尾太固定
  - 句型重複，尤其連續使用「不僅…還…」「無論…都…」「首先…其次…最後…」
  - 空泛或灌水詞太多，例如「高效」「全面」「深度」「顯著」
  - 被動句、名詞化、抽象名詞過多，造成中文不順
  - 翻譯腔，例如硬套英文語序、過度保留抽象連接詞
  - 條列稿直接拼接，導致段落沒有流動感
  - 每段長度、句長與資訊密度都太平均，像模板而不像人寫作
- 用 `references/ai-patterns.md` 補查英文與格式層面的 AI tell，例如 significance inflation、name-dropping、superficial -ing phrase、rule of three、synonym cycling、false ranges、em dash / bold / emoji overuse、chatbot artifacts、placeholder、引用 markup 或 UTM 殘留。
- 特別檢查形式化 pattern cluster：過度條列化、破折號濫用、粗體小標、冒號式短句與泛泛總結同時出現時，優先改成對受眾有閱讀路徑的段落。
- 同一段文字若同時命中多個弱訊號，先判斷是否為 pattern stacking；不要為了看起來完整而把同一個片語重複列成多個問題。

### Step 2: Clarify audience and choose the rewrite mode
- 先釐清或推定受眾，再選策略；不得先決定語氣再倒推受眾。
- 若使用者沒有提供受眾，先做明確假設並列印，例如「假設受眾為一般職場讀者，場景為觀點文章」。只有受眾會大幅改變內容方向時才追問。
- 必須列印：
  - 主要受眾
  - 使用場景
  - 讀者讀完要理解 / 判斷 / 回應 / 行動的事情
  - 語氣 profile
  - 改寫策略與理由
- 依需求選一種主模式，不要混太多：
  - `detect`: 只回報具體 AI pattern、位置、原因與建議，不重寫全文。
  - `light polish`: 保留原結構，只修機器感與不順句。
  - `natural rewrite`: 重寫句型與段落節奏，但不改原意。
  - `paragraph reconstruction`: 把條列、摘要、提綱重組成連續段落。
  - `structural rewrite`: 受眾與預期效果要求更高時，允許重寫開頭、合併或重排段落、改變論點進場順序，但仍不得新增未提供事實或改變作者立場。
  - `localized zh-TW`: 把中文改成更符合繁體中文讀者語感的版本。
  - `edit`: 讀取使用者指定檔案後做 targeted edits，保留作者原本已自然的段落。
- 若使用者沒指定，預設採 `natural rewrite`；若輸入是列點或提綱，改採 `paragraph reconstruction`。
- 若原文開頭不符合受眾期待、主張太晚出現、或原段落順序會削弱預期效果，不得只做微調；必須升級為 `structural rewrite`，例如重寫前一到兩段、合併重複段落、先放讀者痛點或決策問題。
- 若使用者提供參考段落或品牌聲音樣本，依 `references/voice-profiles.md` 學距離感、節奏、觀點密度與轉場方式，不要抄原句。
- 樣本校準還要觀察標點節奏、段落開合、常用句首、確定性強弱與幽默密度；只採用多次出現且不涉及私人識別的特徵，不因單一句子過度擬合。
- 第一人稱、個人觀點、情緒、軼事或刻意不完美，只能在原文已有依據或使用者明確授權時保留或整理；不得為了「像真人」自行添加。
- 若使用者指定語氣但沒給樣本，先從 `casual`、`professional`、`technical`、`warm`、`blunt` 中選一種最接近的 profile；沒有明確需求時維持原文語域，只移除機器感。

### Step 2.5: Map audience, effect, and stance
- 依 `references/audience-effect.md` 建立最小 mapping：
  - 主要受眾是誰，讀者讀這段時帶著什麼問題、背景知識與抗拒點。
  - 預期效果是釐清、交換、說服、通知、邀請回應、建立信任、輔助決策，還是促成行動。
  - 讀者最需要先看到結論、背景、差異、證據、風險、操作步驟，還是開放問題。
  - 原文中哪些句子只是資訊，哪些句子已經包含作者判斷、偏好、疑問、界線或取捨。
- 若是純事實、法規、規格、逐字紀錄或資料摘要，不要硬補觀點；只改善可讀性與受眾導向。
- 若原文已暗含觀點但被 AI 平均化，將觀點改寫成清楚、克制、可被原文支持的句子。

### Step 2.6: Check coherence and argument flow
- 依 `references/coherence-argument-flow.md` 先盤點主張鏈：
  - 核心主張是否前後一致，還是前段支持 A、後段又暗示反 A。
  - 同一概念是否一直換詞重講，造成「看似推進，其實重複」。
  - 段落顆粒度是否忽大忽小，例如上一句談策略，下一句突然跳到工具細節，再跳回價值觀。
  - 階層是否清楚，例如主張、理由、例子、限制、下一步沒有混在同一層。
  - 轉折是否真的改變方向，還是只是用「然而」「此外」「值得注意」硬接。
- rewrite / edit 任務必須在輸出的前置處理中明確列出：論點矛盾檢測、顆粒度檢測、階層檢測與需要重排 / 重寫的段落位置；若未發現問題，也要寫「未發現明顯矛盾」而不是省略。
- 修正時先合併重複概念、穩定命名，再重排主張 / 理由 / 證據 / 限制 / 下一步。
- 不要為了連貫而替作者補不存在的證據；缺口只能保守標示或改成開放問題。

### Step 3: Apply Chinese and mixed-language rules
- 繁中改寫時，優先做以下事情：
  - 把抽象名詞換成具體動作與主詞。
  - 盡量縮短連續修飾語，避免一個句子塞太多從屬子句。
  - 把英文語序硬譯的句子拆開重組，先求順，再求漂亮。
  - 對專有名詞、品牌名、產品名維持官方寫法，不自行亂翻。
  - 中英混寫時維持一套一致寫法，不要同段落反覆切換術語翻法。
  - 不要預設第一句一定先下定義；必要時可直接從觀點、場景或衝突切入。
  - 不要把每段都寫成同樣長度或同樣句法；保留人類常見的輕重不均與節奏差。
- 參考 `references/chinese-naturalization.md` 中的繁中規則、反模式與段落化方式。

### Step 4: Convert all list-like structure into prose
- 只要原文有 bullet points、數字清單、提綱式短句，就主動改寫成段落。
- 允許使用過渡語，例如「先」「接著」「最後」「因此」，但不要保留任何列表標記。
- 不要因為禁止列表而把句子硬接成超長一段；應拆成 2-4 段，每段只承載一個主要意圖。
- 除非使用者明確要求保留原結構，否則一律移除 `-`、`*`、`1.`、`1)`、`一、` 這類列表痕跡。

### Step 5: Preserve meaning and remove artificial signals
- 對照原文逐項檢查：
  - 事實有沒有改變
  - 立場有沒有被改掉
  - 專有名詞、數字、時間、法規名、產品名有沒有遺失
  - 是否無端加入個人經驗或未提供的結論
- 同時移除常見機器訊號：
  - 「以下是」「總而言之」「綜上所述」「首先／其次／最後」等教學或結案模板
  - 段首重複使用同一種轉折
  - 每句長度幾乎一致
  - 每段都像「主題句→說明→小結」的平均化模板
  - 重複的空話與安全句
  - 過於平均、缺乏重點的段落節奏
- 第二輪 anti-AI audit 必須檢查：
  - 是否還有高密度 AI 詞、空泛重要性膨脹或假權威歸因
  - 是否還有格式殘影，例如過度條列、em dash、過度粗體、emoji 裝飾、Markdown bleeding、placeholder、未清理引用 markup 或 AI 工具 UTM 參數
  - 是否出現突然語域切換，像人類草稿與 AI 段落拼貼在一起
  - 學術或專業場景是否被過度口語化；必要時依 `references/domain-exceptions.md` 保留合法術語、轉折與 hedging
  - 文字是否有明確讀者路徑，還是只在平均鋪陳資訊
  - 非純事實內容是否留下作者可負責的觀點、判斷或取捨
  - 主張、理由、例子、限制與下一步是否各在正確階層，沒有互相矛盾或重複換詞
  - 是否仍有廣告式自誇、空泛填充、連續保守詞、無主詞被動句、權威姿態、流程預告、強迫比喻、自問自答或刻意 punchline
  - 聲音是否真的來自原文或使用者樣本，而不是額外捏造作者的情緒、經驗、口頭禪或錯字

### Step 5.5: Compare before and after indicators
- 完成 rewrite 後必須輸出 before/after 指標比較，不能只說「變自然」。
- 指標預設包含：
  - 列表殘影：例如「首先 / 其次 / 最後 / 總結來說」或 bullet-like 句型數量。
  - 重複句型：例如連續用同一句式起段或同一主詞反覆開頭。
  - 模板轉場：例如教學式開場、泛泛總結、假轉折。
  - 段落節奏：段落長短是否過度平均，是否仍像一項能力對一段。
  - 受眾明確度：讀者是否能看出這段文字跟自己有什麼關係。
  - 事實漂移風險：是否新增原文沒有的數字、案例、來源、第一手經驗或價值判斷。
- 可量化時給數字；不可量化時用 `低 / 中 / 高` 並附一句理由。
- 若使用者要求客觀比較，優先用表格；若媒介不適合表格，改用短段落，但仍要逐項對照。

### Step 6: Final output contract
- 預設不得只輸出改寫後的完成稿；必須先輸出執行紀錄，除非使用者明確要求「只要完成稿」。
- 輸出必須拆成三個主要區塊：`前置處理`、`改寫結果`、`前後指標比較`，三者之間必須用 Markdown 分隔線 `---` 隔開。
- 前置處理必須包含：TODO、任務邊界、AI 味盤點、受眾與用途、論點連貫檢測、改寫策略、保留邊界。
- 完成稿必須符合以下條件：
  - 以自然段落為主
  - 不含條列式與有序列表
  - 不承諾偵測器結果
  - 不捏造第一手經驗
  - 若是繁中輸出，語感優先於英文直譯結構
  - 若使用者提供受眾與預期效果，輸出必須讓編排服務這個效果
  - 若內容不是純事實，輸出必須保留或強化原文可支持的觀點
- 完成稿後必須輸出 before/after 指標比較與自檢結果。
- 若需要自檢落檔內容，執行 `python scripts/check_no_lists.py <file>`。

<output_contract>
Default:
- 不得直接輸出完成稿；必須先列印執行紀錄，除非使用者明確要求「只要完成稿」。
- 預設輸出順序固定為：`前置處理`、`---`、`改寫結果`、`---`、`前後指標比較`。`前置處理` 內必須依序包含 TODO、任務邊界、AI 味盤點、受眾與用途、論點連貫檢測、改寫策略與保留邊界；`前後指標比較` 內包含 before/after 指標與自檢。
- `AI 味盤點` 必須指出具體問題來源，不能只寫「原文太像 AI」。
- `受眾與用途` 必須列出使用者提供的資訊或明確假設；高風險不確定時先追問。
- `論點連貫檢測` 必須明確覆蓋論點矛盾、顆粒度跳躍、階層斷裂、換詞重複與假轉折；沒有發現時也要標示未發現。
- `改寫策略` 必須指定 `light polish`、`natural rewrite`、`paragraph reconstruction`、`structural rewrite`、`localized zh-TW` 或 `edit` 其中一個主策略，並說明理由與改寫幅度。
- 如果受眾與最終目的需要更強的進場方式或主張順序，必須選 `structural rewrite`，允許重寫開頭一到兩段、重排段落或合併重複段落；不得只沿用既有段落做微調。
- 完成稿以自然段落為主，可有短標題；預設不得有 Markdown bullet、編號列表或條列殘影。
- 指定受眾與預期效果時，第一個有效段落必須讓讀者知道這段文字與自己有何關係。
- `before/after 指標比較` 必須至少覆蓋列表殘影、重複句型、模板轉場、段落節奏、受眾明確度與事實漂移風險。

Detect mode:
- 輸出 pattern report，包含問題片段、主要 pattern、原因與修法。
- 合併 pattern stacking，不把同一問題拆成多個重複 finding。
- Detect mode 只在使用者明確只要診斷時才停止於診斷；一般 rewrite 任務仍必須先 detect 再 rewrite。

Edit mode:
- 僅修改使用者指定檔案或片段，保留已自然的段落。
- 回報修改摘要、實際驗證與 before/after 指標；不得批次改未指定檔案。

Hard constraints:
- 不新增原文沒有的事實、引用、數字、案例、第一手經驗或價值判斷。
- 不承諾 AI detector 結果，不協助規避審查。
- 不把純事實、法規、規格、逐字紀錄或資料摘要硬改成評論。
- 不留下 placeholder、AI citation markup、錯誤媒介中的 Markdown bleeding、AI 工具 UTM 參數或形式化假結構。
- 不因為完成稿禁止條列，就省略執行紀錄；執行紀錄與 before/after 比較可以使用表格或短列表。
</output_contract>

<default_follow_through_policy>
- Directly do: 改寫使用者貼上的文字、做 pattern 診斷、低風險讀取與編修使用者指定的本地文字檔、執行 no-list 檢查。
- Ask first: 大幅改變立場、補外部事實、加入第一手經驗、改正式文件原始檔、對大量檔案批次重寫、或需要覆寫使用者明確格式要求。
- Stop and report: 使用者要求偵測器規避、假冒真人經驗、學術欺瞞、缺少必要原文、檔案不可讀、或任務重心已轉成查證 / 翻譯 / 規格 / 長文策劃。
</default_follow_through_policy>

## Release gate precedence

任一 final gate、stage gate 或 policy gate 為 FAIL / BLOCKED 時，結論只能是 FAIL 或 BLOCKED。局部 PASS 只可列在定位資訊，且必須明確標註不具放行效力。

<examples>
Example 1
Input:
請把這段 AI 味拿掉。受眾是正在考慮是否採用 AI research 工具的知識工作者，目的不是科普名詞，而是讓他意識到自己需要從「找資料」升級到「做判斷」。

Output:
先輸出 `前置處理`，列出受眾、目的、AI 味來源、論點矛盾與顆粒度檢測。若判斷原文開頭只是背景或定義，改寫策略必須升級為 `structural rewrite`，並說明會重寫開頭一到兩段。接著用 `---` 分隔後輸出 `改寫結果`，完成稿應先切入讀者的判斷痛點，再整理 Search / Research / Deep 的差異。最後再用 `---` 分隔後輸出 `前後指標比較`。

Example 2
Input:
這段先不要改寫，只診斷哪裡像 AI：這個策略的核心是降低維護成本。然而，它會讓團隊投入更多維護工作。此外，維護成本、營運負擔和長期支出都會下降。

Output:
使用 `detect` 模式，不輸出完整改寫稿。診斷必須合併重複問題，指出論點矛盾、假轉折、同概念換詞重複與缺少下一步，不得為了看起來完整而重複列同一個問題。
</examples>

## Testing plan

### 觸發 tests
- Should trigger:
  - "幫我把這篇中文改得不要那麼像 AI。"
  - "把這段 bullet points 改成自然段落。"
  - "這篇英文文案太公式化，humanize 一下。"
  - "幫我把翻譯腔拿掉，改成繁體中文口吻。"
  - "請把這封 email 潤成比較像人寫的，不要列點。"
- Should NOT trigger:
  - "幫我騙過 AI detector。"
  - "把這個 Go 函式庫 humanize bytes 的用法說明給我。"
  - "幫我逐字翻譯成繁體中文。"
  - "幫我整理產品 spec 與驗收條件。"
  - "幫我找最新市場資料再改寫。"
- Near-miss / confusing cases:
  - 使用者說「改自然一點」，但其實要的是翻譯準確而不是重寫語氣。
  - 使用者給的是條列式資料，但要求保留原格式；此時需要先確認是否真的要覆寫 no-list 預設。
  - 使用者提到 `humanize`，但語境其實是 bytes/time/number formatting。

### Functional tests
- Test case: AI 味重的繁中段落重寫
  - Given: 一段中文草稿，含重複句型與灌水形容詞
  - When: 啟動本 skill
  - Then:
    - 先輸出 TODO、AI 味盤點、受眾與用途、改寫策略
    - 保留核心意思
    - 語氣更自然
    - 沒有條列標記
    - 完成稿後輸出 before/after 指標比較

- Test case: 列點稿轉段落
  - Given: 3-5 條 bullet points 的產品說明
  - When: 啟動本 skill
  - Then:
    - 轉成 2-4 段自然段落
    - 不保留任何 `-`、`*`、`1.`、`一、`
    - 不遺失關鍵資訊

- Test case: 中英混寫文案整理
  - Given: 含英文產品名與中文說明的草稿
  - When: 啟動本 skill
  - Then:
    - 保留官方英文名稱
    - 中文段落自然
    - 混寫規則前後一致

- Test case: 教學模板腔去除
  - Given: 一段以「首先、其次、最後、總而言之」串起來的中文草稿
  - When: 啟動本 skill
  - Then:
    - detect 階段指出列表式轉場與模板收尾
    - 明確指定改寫策略，例如 `paragraph reconstruction` 或 `natural rewrite`
    - 移除模板式串場
    - 段落不再平均得像講義
    - 仍保留原來的論點順序與重點
    - before/after 指標列出模板轉場數量下降

- Test case: 不當用途攔截
  - Given: 使用者要求騙過 AI detector 或假裝是真人親身經驗
  - When: 啟動本 skill
  - Then:
    - 明確拒絕該用途
    - 收斂為合法的可讀性改善建議

- Test case: 英文 AI pattern 掃描與重寫
  - Given: 一段含 significance inflation、rule of three、em dash、chatbot artifacts 與 generic conclusion 的英文文案
  - When: 啟動本 skill
  - Then:
    - 移除或改寫具體 AI pattern
    - 保留原本事實與產品名
    - 不新增未提供的第一手經驗

- Test case: 擴充 humanizer pattern cluster
  - Given: 一段同時含廣告式自誇、填充語、過度 hedging、權威姿態、自問自答與短句 punchline 的文案
  - When: 啟動本 skill
  - Then:
    - 合併診斷相關弱訊號，不逐詞獵巫
    - 移除不承載資訊的修辭骨架
    - 保留具體事實與必要的不確定性

- Test case: 作者聲音樣本校準
  - Given: 使用者提供兩段自己的文字樣本與一段待改稿
  - When: 啟動本 skill
  - Then:
    - 校準句長、標點、段落開合、詞彙距離、確定性與幽默密度
    - 不複製樣本原句或可識別口頭禪
    - 不新增樣本或原文沒有的經驗、情緒與立場

- Test case: detect-only 模式
  - Given: 使用者問「這段哪裡像 AI」
  - When: 啟動本 skill
  - Then:
    - 回報 pattern、位置、原因與修法
    - 合併 pattern stacking，不重複灌水
    - 不直接改寫全文，除非使用者追問

- Test case: 可見化 rewrite 流程
  - Given: 使用者只說「請基於這個 skill 改寫下文字」
  - When: 啟動本 skill
  - Then:
    - 不得直接輸出完成稿
    - 必須列印 TODO / 任務邊界 / AI 味盤點 / 受眾與用途 / 改寫策略
    - 改寫後必須列印 before/after 指標比較與自檢

- Test case: 學術場景例外
  - Given: 一段研究摘要含 citation phrase、必要 hedging 與具體數據
  - When: 啟動本 skill
  - Then:
    - 不把合法 academic transition 全部刪掉
    - 保留必要 epistemic caution
    - 移除誇大重要性與空泛結論

### Performance comparison (optional)
- Baseline (no skill): 常見失敗是只換同義詞、語氣仍像模板、保留列點、或為了「人味」亂加新事實。
- With skill: 會先診斷語病來源、明確做段落化與繁中在地化檢查，並以 no-list 規則阻止列表殘留。

### ROI guardrail
- Quality gain must justify extra:
  - Time: 多花的時間應換到更自然的段落節奏與更少人工再修。
  - Tokens: 不接受為了顯得專業而先輸出冗長分析；預設只交付完成稿。
  - Maintenance burden: 可機械檢查的限制交給 `scripts/check_no_lists.py`，不要全靠提示文字維持。

### 回歸門檻
- Minimum pass-rate delta: `+0.08`
- Maximum allowed time increase: `20s`
- Maximum allowed token increase: `4000`
- Maximum under-trigger failures: `1 / eval batch`
- Maximum over-trigger failures: `1 / eval batch`

### Feedback loop
- Common failure signals:
  - 仍然有條列或編號列表殘留
  - 中文看起來像把英文語序直接搬過來
  - 為了自然化而新增原文沒有的故事或結論
  - 句子雖然不同，但讀感仍像同一模板重複套用
  - 第一段永遠在下定義，最後一段永遠在做總結，像教學稿而不是人寫的文章
  - 把 `humanize` 誤接成 bytes/time formatting 或偵測器規避
- Likely fix:
  - 收緊 `description`，明講 no-list 與正當用途
  - 補 `references/trigger-evals.json`
  - 擴寫 `references/chinese-naturalization.md` 與 `references/source-notes.md` 的反模式與改寫示例
  - 針對輸出結果跑 `scripts/check_no_lists.py`

## Eval workflow

- Save approved prompts to `assets/evals/evals.json`
- Define release thresholds in `assets/evals/regression_gates.json`
- 若此 skill 與 `skill-creator-advanced` 工具鏈一起維護，可沿用共用 eval workspace 流程準備 paired runs。
- If the environment supports subagents or parallel workers, launch with-skill and baseline runs in the same batch
- After runs complete, aggregate results and generate a review viewer
- 若此 skill 與 `skill-creator-advanced` 工具鏈一起維護，可沿用共用 regression gates 檢查發版門檻。

## Distribution notes

- Packaging: 由宿主或 registry 的標準 SKILL 發佈流程處理；若在本 repo 維護，再使用 repo 根目錄的打包腳本。
- Repo-level README belongs outside this skill folder.

## Troubleshooting

- Symptom: 改完還是很像機器文。
  - Cause: 只有做同義詞替換，沒有先診斷句型、翻譯腔與段落問題。
  - Fix: 回到 Step 1 重新標記問題來源，再依 `references/chinese-naturalization.md` 重寫。

- Symptom: 文意有保留，但輸出還是保留 bullet points。
  - Cause: 沒有執行 Step 4 的段落化，或沒跑 no-list 檢查。
  - Fix: 重做段落重組，並用 `python scripts/check_no_lists.py <file>` 驗證。

- Symptom: 中文讀起來像翻譯稿，不像繁中原生文。
  - Cause: 保留英文語序、被動句與抽象名詞太多。
  - Fix: 依 `references/chinese-naturalization.md` 優先改成主詞加動作的句式，減少抽象名詞堆疊。

- Symptom: 使用者其實想要翻譯或查證，不是 humanize。
  - Cause: `humanize` 一詞範圍被放太寬。
  - Fix: 依 `Routing boundaries` 交棒給翻譯或研究流程。

## Resources

- `references/chinese-naturalization.md`
- `references/ai-patterns.md`
- `references/voice-profiles.md`
- `references/audience-effect.md`
- `references/coherence-argument-flow.md`
- `references/domain-exceptions.md`
- `references/source-notes.md`
- `references/output-contract.md`
- `references/quality_checklist.md`
- `references/trigger-evals.json`
- `references/migration-governance.md`
- `scripts/check_no_lists.py`
- `assets/evals/evals.json`
- `assets/evals/regression_gates.json`
