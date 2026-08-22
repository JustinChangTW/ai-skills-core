# 來源筆記

這份筆記把新增附件與外部文章轉成 `humanize-text` 可直接採用的規則，避免只停在觀念摘要。

## Local PDF provenance

- 原始檔曾位於作者本機下載目錄；此資料只作 2026-03 初版規則來源紀錄，不是 runtime dependency，也不要求跨平台 host 存取本機路徑。
- 可直接吸收的結論：
  - 「不像人」常不是單一語病，而是多個訊號疊加，例如過度平滑、安全、模板化、句長過度均勻、標點節奏過度規整、在地語感不對。
  - 推論期最可落地的做法不是亂加錯字，而是 `style spec + few-shot + negative constraints + rewriting/postprocess`。
  - 去模板、去重複、調整句長與標點節奏、做地區化，是比「刻意裝不完美」更穩的做法。
  - 對繁中尤其要處理台灣語境、過度正式、列表感與轉折詞濫用。

## Web notes

### GitHub humanizer skills reviewed on 2026-05-11

來源：
- https://github.com/blader/humanizer
- https://github.com/yelban/humanizer.TW
- https://github.com/Aboudjem/humanizer-skill
- https://github.com/jpeggdev/humanize-writing
- https://github.com/matsuikentaro1/humanizer_academic

可直接吸收的結論：
- 成熟 humanizer skill 不只做同義詞替換，而是先建立可掃描的 AI pattern catalog，再重寫。
- 常見英文 AI tell 包含重要性膨脹、假權威歸因、表面 `-ing` 分析、rule of three、synonym cycling、false ranges、copula avoidance、chatbot artifacts、knowledge-cutoff disclaimers、格式殘影與泛泛正向結尾。
- 中文版本需要獨立處理時代開場白、互聯網黑話、書面代詞、翻譯腔、結尾套話與台灣語感，不能只是翻譯英文規則。
- Voice calibration 應學句長、段落入口、轉場方式與觀點密度，不該抄樣本句子，也不該偽造第一手經驗。
- detect / rewrite / edit 三種模式可以降低誤用：只診斷時不應擅自全文改寫，修改檔案時應做 targeted edits。
- 學術與醫療文本不能盲目移除所有正式轉折與 hedging；合法 citation phrase、研究保守語氣與資料完整性必須保留。
- Pattern stacking 需要合併判斷；同一片語命中多個弱訊號時，不要灌水成多個獨立 finding。

Rules promoted to the skill:
1. 新增 `references/ai-patterns.md` 作為通用 AI pattern catalog。
2. 新增 `references/voice-profiles.md` 作為 sample calibration 與 profile 選擇規則。
3. 新增 `references/domain-exceptions.md` 作為學術、醫療、技術、法務與正式文件的保留規則。
4. 在 `SKILL.md` 增加 `detect`、`rewrite`、`edit` 模式與第二輪 anti-AI audit。
5. 擴充 functional eval，覆蓋英文 pattern、detect-only、學術例外與格式殘影。

### Hermes humanizer 2.5.1 integration reviewed on 2026-08-15

來源：
- https://github.com/NousResearch/hermes-agent/tree/main/skills/creative/humanizer
- 上游版本：`2.5.1`
- 上游作者：Siqi Chen / blader；Hermes port；MIT License

吸收項目：
- 補入廣告式自誇、填充語、過度 hedging、無主詞被動句、權威姿態、流程預告、強迫比喻、自問自答、戲劇碎句與 punchline 等 pattern cluster。
- 擴充 voice fingerprint，納入標點節奏、段落開合、確定性與幽默密度。
- 將第二輪 anti-AI audit 改為獨立盲檢角度，而不是只重複第一輪規則。

未照單全收：
- 不為了「personality and soul」新增作者沒有提供的情緒、第一人稱、軼事、錯字、離題或價值判斷。
- 不把任何單一詞彙、破折號或句型視為 AI 證據；只依情境與 pattern stacking 判斷。
- 不把 humanization 描述成可繞過 AI detector；核心仍是可讀性、聲音一致性與事實忠實。

### Audience-centered and rhetorical writing references reviewed on 2026-05-11

來源：
- https://owl.purdue.edu/owl/subject_specific_writing/professional_technical_writing/effective_workplace_writing/index.html
- https://owl.purdue.edu/owl/general_writing/academic_writing/rhetorical_situation/elements_of_rhetorical_situations.html
- https://owl.purdue.edu/owl/general_writing/academic_writing/rhetorical_situation/purposes.html
- https://www.uis.edu/learning-hub/writing-resources/handouts/learning-hub/rhetorical-situation

可直接吸收的結論：
- 有效文字必須先理解 rhetorical situation；文字、作者、受眾、目的與情境共同決定如何溝通。
- workplace writing 與 user-centered / reader-centered writing 都要求先考慮讀者的期待、特徵、目標與使用情境，而不是只套用文件模板。
- 作者目的與讀者目的可能不同；改寫時要讓文字同時服務作者想達成的效果與讀者實際需要。
- 受眾分析會改變資訊排序：決策者需要取捨，執行者需要下一步，新手需要差異與例子，反對方需要風險與證據。

Rules promoted to the skill:
1. 新增 `references/audience-effect.md`，把受眾、預期效果、讀者路徑與觀點盤點寫成改寫前置步驟。
2. 在 `SKILL.md` workflow 中加入 audience-effect mapping 與 stance inventory。
3. 在 output contract 中要求指定受眾時，完成稿必須讓第一個有效段落對準讀者需求。
4. 擴充 eval，覆蓋「消失的受眾」與「觀點被平均化」案例。
5. 依使用者回饋補入 `structural rewrite`：當原開頭、段落順序或主張進場方式不服務受眾與目的時，必須升級改寫策略，允許重寫開頭一到兩段、提前讀者痛點或重排論點。

### Formal marker cluster notes reviewed on 2026-05-11

來源：
- https://www.grammarly.com/blog/punctuation-capitalization/why-you-should-love-the-em-dash/
- https://www.tryleap.ai/learn/what-is-em-dash-problem
- https://fastai.news/2026/04/07/why-ai-stopped-using-the-em-dash-and-why-you-should-too/
- https://reporter.rit.edu/7526/views/em-dashes-useful-for-writers-overused-by-ai/

可直接吸收的結論：
- 破折號本身是合法標點，可用來補充、強調或標示思路轉折；問題在於高頻、規律、搭配其他 AI pattern 出現。
- 形式化痕跡通常是 cluster，而不是單一符號：破折號、過度條列、粗體小標、短分節、空泛強調與泛泛總結一起出現時，機器感會明顯上升。
- 修法不應變成禁止破折號，而是回到功能：能用逗號、冒號、括號、句號或自然段落更清楚時，就替換；真正符合作者節奏時才保留。

Rules promoted to the skill:
1. 在 `references/ai-patterns.md` 補入「過度條列化」與「破折號過度使用」兩個 pattern。
2. 在 `SKILL.md` 與 `output-contract.md` 補入 formal marker cluster 檢查。
3. 擴充 functional eval，覆蓋 bullet / dash / bold heading 的群聚清理。

### Coherence and argument flow references reviewed on 2026-05-11

來源：
- https://owl.purdue.edu/owl/general_writing/academic_writing/paragraphs_and_paragraphing/index.html
- https://owl.purdue.edu/owl/graduate_writing/thesis_and_dissertation/paragraph_organization_flow.html
- https://owl.purdue.edu/owl/general_writing/common_writing_assignments/argument_papers/body_paragraphs.html
- https://owl.purdue.edu/owl/general_writing/the_writing_process/proofreading/revising_for_cohesion.html

可直接吸收的結論：
- 段落應有 unity 與 coherence；一段承載一個主控概念，句子要能邏輯連接。
- flow 不是多加轉折詞，而是讓段落互相連接、回扣更大的主張。
- 好的論證段落需要 transition、topic sentence、evidence / analysis 與 warrant，讓材料能支持主張。
- 讀者需要穩定的 topics 與熟悉資訊作為句子開頭，否則會覺得論點跳躍、失焦。

Rules promoted to the skill:
1. 新增 `references/coherence-argument-flow.md`，把主張鏈、概念命名、顆粒度、階層與轉折寫成 coherence pass。
2. 在 `SKILL.md` workflow 中加入 coherence pass，防止論點矛盾、換詞重複與階層斷裂。
3. 擴充 eval，覆蓋論點矛盾、同概念換詞重複與顆粒度跳躍。
4. 依使用者回饋要求 rewrite / edit 任務在前置處理中可見列出論點矛盾、顆粒度跳躍、階層斷裂、換詞重複與假轉折的檢測結果；未發現問題時也要明寫。

### Humanize workflow feedback incorporated on 2026-05-11

來源：實際使用 `humanize-text` 改寫 Search / Research / Deep Research 觀點文後的使用者回饋。

可直接吸收的結論：
- 可見化流程不能只是一串小標；`前置處理`、`改寫結果`、`前後指標比較` 三個主要交付區塊必須用分隔線隔開，讓讀者清楚知道哪裡是診斷、哪裡是正文、哪裡是驗證。
- coherence pass 若沒有明確輸出論點矛盾、顆粒度與階層檢測，使用者無法確認 skill 是否真的做了論點層面的檢查。
- 高目的性改寫不能只沿用既有段落微調。若受眾與目的要求更強的開場或更清楚的主張路徑，應升級為 structural rewrite，包含重寫開頭、調整論點順序與合併重複段落。

Rules promoted to the skill:
1. 在 `SKILL.md` 與 `references/output-contract.md` 補入三段式輸出契約與 `---` 分隔線要求。
2. 在 `references/coherence-argument-flow.md` 補入可見論點連貫檢測要求。
3. 在 `references/audience-effect.md` 補入 structural rewrite 的觸發條件與邊界。
4. 在 `assets/evals/evals.json` 補入 visible section separators 與 structural opening rewrite 的回歸案例。

### LINE 文章

來源：[line.newspaper.tw/2026/03/imitate.html](https://line.newspaper.tw/2026/03/imitate.html)

- 可直接吸收的結論：
  - 人類文章常有不平均的重點分配，不會每段都像模板一樣平均。
  - 太工整、太完整、太像「把該講的都講完」反而容易露出機器感。
  - 更自然的寫法通常會保留取景角度、情緒焦點與選擇性細節，而不是平均鋪陳。

### BruceWind 文章

來源：[iambrucewind.com/20251116-brucewind-aiwriting](https://iambrucewind.com/20251116-brucewind-aiwriting/)

- 可直接吸收的結論：
  - AI 常以定義、摘要、教學式鋪陳起手，轉折詞過多，整篇太像講義。
  - 要減少「AI 味」，應刪掉不必要的解說骨架，不要讓第一段總在下定義，最後一段總在總結。
  - 更像人的改寫不是把文章弄亂，而是讓段落有輕重、語氣有立場、細節有取捨。

## Rules promoted to the skill

1. 預設掃描並移除教學模板句。
2. 若段落長度與句法過於平均，主動打散節奏。
3. 若使用者提供風格樣本，學節奏、距離感與觀點密度，不抄句子。
4. 優先把內容改得「像作者有取捨」，而不是「像系統把所有點列完」。
5. 在繁中情境下，先修語感與在地性，再談華麗修辭。

