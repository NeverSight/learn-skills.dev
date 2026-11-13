---
name: zotero-manuscript-thinking
description: "论文修改中的整体审视与写作策略子 Skill：优先检查语言精确度、领域地道表达、Methods/Results 的可复现性与结果叙事、段落衔接、Introduction/Discussion 逻辑、研究主线、证据边界和审稿风险，并输出可执行的优先级修订计划。触发词包括整体审视、语言地道、同领域论文写法、Methods、Results、Introduction/Discussion、主线、贡献、审稿风险和修订优先级；不用于单句语法、拼写、格式或单条引用核实。"
license: MIT
compatibility: codex,opencode,zcode
metadata:
  parent_skill: zotero-evidence-review
  workflow: manuscript-level-diagnosis
  version: 0.7.0
  optional: zotero-mcp, pubmed-mcp
  reference: references/domain-style-calibration.md,references/polish-quality-gate.md,references/writing-options-card.md
---

# Zotero Manuscript Thinking

这个子 Skill 处理“抬头看整篇论文”的问题，但把写作语言作为第一类质量对象。它不是另一轮逐句润色，也不把所有论文都套进同一个写作模板；它先做一个极简的意义和证据边界检查，再判断当前最需要解决的是语言精确度、领域地道表达、Methods 的可复现性、Results 的证据叙事、段落衔接、Introduction 的 gap/贡献链、Discussion 的证据—解释链，还是全文论证结构，最后把问题交给合适的局部工作流。

当用户要求“像本领域高水平论文一样自然”“参考同领域代表性文章”“像某个期刊/会议的写法”时，启动可选的 `Domain Style Calibration`：从 Zotero/PubMed 或用户指定的 3–5 篇可核验论文中提取段落功能、句子功能、术语、claim verb、引用归属和信息节奏等模式，再对照用户自己的稿件。它学习的是可解释的写作决策，不复制原文，也不把“高分”当作未经证明的事实。

它可以独立调用，也可以作为 `zotero-evidence-review` 在段落证据分析或引用修复后的 manuscript-level checkpoint。默认只输出诊断和优先级计划，不自动改写整篇论文，不自动承诺新实验。 如果用户尚未收集可核验的 peer corpus，先交给 `zotero-literature-learning` 建立素材包；本 Skill 消费其 `style_profile`、`evidence_profile` 和 `argument_profile`，不重复做无目标的批量检索。用户出现“知道意思但不会写、句子太啰嗦、方法名拿不准、Results 不知道如何推进”等卡点时，先触发 `WRITING_BLOCK_LEARNING`，再决定是否进入全文诊断。用户要求“给几个版本”“从不同角度写”时，读取 [WRITING_OPTIONS_CARD](references/writing-options-card.md)，输出可比较的候选和选择交接，不把某一版静默标为最终答案。

## 0.1 修订顺序：先保意义，再校准领域语言

本 Skill 的最终措辞必须通过 [polish-quality-gate.md](references/polish-quality-gate.md)。它把
“写得更顺”拆成 meaning、section logic、field-native、language precision 和 evidence-boundary
五道门，并把最具体的叶子 Skill 作为最终编辑器：`academic-introduction-polisher`、
`academic-discussion-polisher`、`medical-english-precision-editor`、`writing-core`、
`academic-reference-matcher` 和 `academic-ref-check`。本 Skill 负责诊断、交接和回查，不用
通用的“顶刊腔”替代章节专用编辑。

每次运行都把“整体观”和“地道表达”放进同一条可回查的修订链，避免先把句子改漂亮、再发现主张已经变强：

```text
meaning gate → section logic → peer-style calibration (if requested) → language pass → evidence/consistency audit
```

每一步都留下一个决定，而不是只输出一版“更流畅”的文本：

| 步骤 | 要回答的问题 | 最小产物 | 继续条件 |
|---|---|---|---|
| `meaning gate` | 主语、比较、数字、方向、证据等级和范围是否明确且可保持 | `paper_contract` + `claim IDs` | 核心主张可定位；否则标 `P0/unknown` |
| `section logic` | 本段/本节在读者路径中承担什么任务，是否与前后文衔接 | 对应 `Logic Map` | 段落任务和下一问题清楚 |
| `peer-style calibration` | 3–5 篇可核验同类论文如何组织同一功能、使用哪些术语和 claim verbs | `Domain Style Calibration` | 只采用可追溯模式；语料不足则降置信度 |
| `language pass` | 句法、术语、信息节奏和学术语域是否自然，不改变科学含义 | `Language Audit` + copy-ready text | 每个高风险改动有 `author_check` |
| `evidence/consistency audit` | 改写后是否仍与图表、Methods、Results、引用和 profile 一致 | `POST_WRITE_AUDIT` | 发现漂移就回退措辞或交证据模块 |

“地道”只有在目标 section、文章类型和可检查的 peer pattern 支持下才成立；没有可核验语料时，使用 `genre-neutral` 表达并明确 `calibration_confidence: none/low`。

## 1. 何时触发

### 1.0 任务分层

先把请求标记为一个或多个工作层级；没有领域语料请求时，默认顺序是 `meaning gate → language → section logic → whole-paper spine`；出现明确写作卡点时，先运行 `writing_block`，不把局部表达问题扩大成整篇重写。如果用户要求领域地道或目标期刊校准，在意义门禁后加入 `section logic → domain style calibration → language`；语料不足时必须保留 `calibration_confidence: low/none`，不能强行给出“本领域标准写法”。Methods 和 Results 的语言校准必须与各自的证据职责一起检查，不能只做表面同义替换。

| 层级 | 主要问题 | 默认交付 |
|---|---|---|
| `language` | 句子是否准确、自然、连贯、符合学术语域，是否因改写改变了证据强度 | Copy-ready 文本 + 语言问题表 |
| `writing_block` | 写作者知道科学内容但卡在句式、段落功能、方法命名或结果推进 | `WRITING_BLOCK_LEARNING` + `WRITING_OPTIONS_CARD` + 2–3 个候选 + author check |
| `domain_style_calibration` | 与同领域、同文体、同目标期刊/会议的可核验论文比较写作模式；可作用于 Methods/Results 等各 section | Domain Style Calibration + 对照后的 Copy-ready 文本 |
| `introduction_logic` | 背景、已知、具体 gap、方法适配、研究目标和贡献是否逐段推进 | Introduction logic map + 修改顺序 |
| `methods_logic` | 设计、样本、变量、流程、统计和质量控制是否足以让读者复现，并与 Results 对齐 | Methods Logic Map + reproducibility audit |
| `results_logic` | 结果块、定量锚点、图表引用和证据边界是否形成清楚的发现叙事 | Results Logic Map + result-to-claim audit |
| `discussion_logic` | 结果、解释、文献比较、替代解释、限制和意义是否形成证据支持的链条 | Discussion logic map + 风险表 |
| `whole_paper` | Introduction 的承诺是否由 Results/Discussion 回收，全文是否围绕同一个问题收束 | argument spine + P0–P3 计划 |

最终编辑器选择规则：Introduction 优先 `academic-introduction-polisher`；Discussion 优先
`academic-discussion-polisher`；英文医学句法和术语优先 `medical-english-precision-editor`；
中文学术表达和去 AI 化优先 `writing-core`；补引文或核实引用使用
`academic-reference-matcher`；参考文献身份、DOI、去重和格式使用 `academic-ref-check`。
交接时必须携带段落任务、claim IDs、must-preserve ledger、证据等级和 `author_check`。

如果用户只给一个句子，使用 `language`；给出完整 Methods、Results、Introduction 或 Discussion 时，先做对应的 section logic，再做语言；给出全文或“整体改进”时，运行各章节适用的逻辑层和全文层，但语言层仍是主要输出之一。

### 1.1 显式触发

当用户提出以下请求时，直接调用本 Skill：

- “整体看看这篇论文”“从全篇角度改进”“帮我看主线/逻辑/贡献/创新点”；
- “像审稿人一样看”“为什么这篇稿子不够有说服力”“如何提高论文质量”；
- “这段改了几次还是不顺”“局部都改好了但全文还是散”；
- “给出论文修改策略/优先级/下一轮怎么改”，或要求结合全文、摘要、图表、结果和参考文献判断。
- “语言要地道”“像这个领域的高水平论文”“参考几篇代表性文章来改”“像某期刊/会议的写法”“不要翻译腔但要保留专业性”。
- “Methods 写得不够可复现”“方法学和 Results 对不上”“Results 像图注堆砌”“结果叙事不清”“统计结果表达不规范”。
- “知道结果但不知道怎么写”“这句话太长/太啰嗦”“annotation 这个词是否准确”“Methods overview 怎么压缩”。

### 1.2 自动 checkpoint

在 `zotero-evidence-review` 的 Module 2、Module 2.2 或 Module 2.5 中，如果满足以下任一条件，先运行一次紧凑的 manuscript-level checkpoint，再给出局部改写：

1. 用户同时提供了标题、摘要、提纲或两个以上章节；
2. 同一章节已经进行了两轮以上局部修改；
3. 出现 `Unsupported gap`、证据等级 E、Current study 与 external evidence 混淆、强因果表述或核心主张无对应结果的风险；
4. 局部建议会改变研究问题、贡献、方法解释、结果解释、章节顺序或结论范围。

只有单个段落且没有全文上下文时，不假装完成整篇诊断；输出 `scope-limited checkpoint`，明确哪些判断需要全文材料。

如果用户明确要求领域写法，额外建立 `style_corpus_ledger`：记录目标领域、文章类型、目标 venue、读者、实际检查的论文、未检查的论文、全文/摘要访问状态和选择理由。没有至少三篇可匹配且可检查的论文时，输出低置信度，不把个别作者的习惯写成领域规范。

### 1.3 不触发

以下情况直接使用现有模块即可：

- 只改一个句子的语法、拼写、格式或术语；
- 只核实一条引用或一个数字；
- 论文结构已经明确，用户只要求按指定风格改写；
- 没有新增信息，重复运行只会复述上次诊断。

## 2. 输入与范围门禁

先建立 manuscript scope，不能把当前工作目录中的所有文件都当作论文材料。优先读取用户明确指定的文件；没有明确指定时，按以下顺序寻找并报告实际使用的输入：

| 输入层级 | 最低材料 | 可以回答的问题 | 输出限制 |
|---|---|---|---|
| A：完整稿件 | title/abstract、Introduction、Methods、Results、Discussion/Conclusion、figures/tables、references | 全文论证链、章节分工、证据覆盖和审稿风险 | 可做完整诊断 |
| B：论文骨架 | title/abstract、提纲、目标段落、主要图表或结果摘要 | 主线、贡献和局部修改对全篇的影响 | 标记未读章节，不下完整结论 |
| C：单段落 | 一个段落及其邻近上下文 | 句内主张、证据边界和局部风险 | 只做 scope-limited checkpoint |

每次运行开头记录：

- `manuscript_scope`：A / B / C；
- `files_read`：实际读取的文件或章节；
- `files_not_read`：影响判断的缺失材料；
- `research_mode`：只使用现有结果，还是用户明确允许补充分析；
- `target_venue`：已知则记录，未知则写 `unspecified`。

不因缺少原始数据而否定用户已经提供的结果，但不得把未读的结果文件、图表或全文内容当作已验证事实。

## 2.1 语言质量审阅协议

语言审阅的目标是提高可读性和科学精确度，不是把文章写得更华丽、更像模板或更有“顶刊腔”。先检查意义是否保持，再修改句子；如果语言问题来自论证缺口，标记为 section logic 或 whole-paper 问题，不用同义词掩盖。

### 语言检查维度

逐段检查以下八个维度，只有发现问题才记录；Methods 和 Results 还要运行后面的章节专项协议：

1. **Meaning fidelity**：主语、对象、比较关系、时间范围、数量和不确定性是否保持；改写后是否悄悄变成更强的因果、独立性、临床意义或普遍性。
2. **Claim precision**：`show/demonstrate/indicate/suggest/may` 等动词是否与 A–E evidence level 匹配；不要用 `prove`、`clearly` 或空泛的 `significant` 制造确定性。
3. **Sentence clarity**：主语和谓语是否明确，修饰语是否就近，长句是否包含多个未标明的逻辑关系，代词和指代是否可回溯。
4. **Paragraph cohesion**：每段是否有一个中心任务；主题句、证据句、解释句和收束/过渡是否顺序合理；`however`、`therefore`、`although`、`consistent with` 是否表达真实关系。
5. **Information density and rhythm**：是否有重复背景、堆叠名词、连续等长句、过度压缩或信息缺失；语言优化不能删掉对象、样本、方法条件、指标口径和边界。
6. **Academic register**：中文避免机械的“首先/其次/最后”和空壳强调，但不把所有连接词一律删除；英文避免翻译腔、过度名词化和虚假正式感。
7. **Terminology and consistency**：同一概念、缩写、时态、单位、组别和图表名称在全文中保持一致；首次出现时补全必要定义。
8. **Citation ownership**：句子中的发现属于本研究还是外部文献必须清楚；引用放置应紧跟其支持的 claim，不能用一条背景引用覆盖整段新结果。

对 Methods 和 Results 追加一个“词义—证据职责”检查，避免用看似专业的名词替代实际分析：

| 观察到的动作 | 优先考虑的表达 | 只有在以下条件满足时才使用更强表达 |
|---|---|---|
| 给变异/基因赋予功能标签 | `functionally annotated variants/genes` | 确实输出功能类别或标签 |
| 进行基因、组织或通路层面的统计分析 | `conducted gene-, tissue-, and pathway-level analyses` | 三类分析确实执行且可定位 |
| 检查组织表达或通路过度代表 | `tissue-expression` / `pathway-enrichment analyses` | 有对应富集或过度代表方法 |
| 整合多组学以排序候选对象 | `integrated ... data to prioritize candidate genes/cell types` | 输出是优先级排序，不写成因果证明 |
| 报告观察到的关系 | `was associated with` / `showed` | 设计和证据允许的范围内使用 `indicated` 或 `suggested` |

如果方法动作无法落入表格，保留较窄的术语并列出 `author_check`；不要把 `annotation`、`characterization` 或 `causal` 当作默认的“高级词”。

### 语言问题输出

语言层至少保留以下字段，不要只给“更流畅”的笼统评价：

```markdown
| Location | Original phrase | Problem type | Risk of meaning drift | Revision strategy | Author check |
|---|---|---|---|---|---|
```

`Revision strategy` 只能使用 `clarify subject`、`split sentence`、`repair connector`、`reduce repetition`、`restore boundary`、`calibrate verb`、`standardize term`、`reorder paragraph` 或 `retain`。Copy-ready 文本保留原稿语言；Annotated notes 说明为什么改，以及是否需要作者核对。

### 语言与逻辑的关系

- 句子不顺但主张清楚 → 交给 `medical-english-precision-editor`（英文医学稿）或 `writing-core`（中文/通用学术表达）。
- 段落顺序、中心句或过渡不清 → 先在本 Skill 的 section logic 层修复，再交给语言编辑。
- 语言变得更漂亮但证据强度变高 → 立即回退，按 Source layer 和 A–E level 重写。
- 用户要求“像顶刊”时，解释为更紧的逻辑、更少的重复、更精确的措辞和可控的外推，不使用华丽词汇或夸大创新替代证据。

### 语言质量验收门

完成一轮局部或章节润色后，必须输出 `POST_WRITE_AUDIT`，并使用
[polish-quality-gate.md](references/polish-quality-gate.md) 的五道门。`accepted: pass` 需要
`claim_unchanged: yes`、`numbers_units_direction_unchanged: yes`、
`citation_ownership_preserved: yes`、`new_unsupported_claim: no`，且不存在高风险的
`unknown`。任何 evidence-boundary `fail` 都要回退措辞或交给证据模块；不能用“更地道”覆盖
未解决的科学含义问题。连续两轮只替换同义词而没有改变已诊断问题时停止，报告剩余的
`author_check`，避免无效的反复润色。

### 2.1A 领域地道语言与目标语料校准

把“地道”拆成可审查的目标，而不是凭模型直觉判断。详细的选文和记录格式见
[references/domain-style-calibration.md](references/domain-style-calibration.md)。

1. **先定义目标**：记录 `domain`、`article_type`、`target_venue`、`section`、`audience`、`language` 和不可改变的术语/结果/证据边界。目标 venue 未知时，使用 genre-neutral profile，并明确写出未知。
2. **再选语料**：优先从用户 Zotero 库中选择同一 section、文章类型、子领域/方法/对象相近的 3–5 篇论文；需要扩展时才用 PubMed 或其他当前可用工具。每篇记录 DOI/PMID/venue/year、选择理由、实际检查的范围和访问状态。搜索结果标题或 snippet 只能作为发现线索。Zotero MCP 的顺序固定为：`zotero_get_recent` 连接检查 → `zotero_semantic_search` → 必要时一次独立的 `zotero_search_items`/`zotero_advanced_search` fallback → `zotero_get_item_metadata` → `zotero_get_item_children`/`zotero_get_items_children` 找 PDF → `zotero_get_pdf_outline` 定位章节 → `zotero_read_pdf_pages` 读取相关页，必要时用 `zotero_get_item_fulltext` 兜底；不得把这些依赖调用放在同一批次。
3. **只抽取模式**：比较 rhetorical moves、sentence functions、claim verbs/hedges、信息节奏、术语/缩写、citation ownership 和 reader path。不要复制长句、独特短语、数据、贡献或结论；也不要把某个期刊的格式规则误报成领域语言规范。
4. **做对照而不是照抄**：输出 `peer pattern → draft mismatch → safe action → meaning check` 表。允许的动作是 `adopt_move`、`reorder`、`clarify_subject`、`calibrate_verb`、`replace_nonstandard_term`、`compress_repetition`、`add_bridge`、`retain` 和 `do_not_adopt`。最终 Copy-ready 文本只能来自用户自己的主张和证据。
5. **标置信心并停止**：3 篇以上且相关 section 都检查过为 `high`；语料混合或只有摘要为 `medium/low`；无可检查语料为 `none`。新增论文如果不改变行动就停止扩展，避免把草稿拉向不相干的文体。每个可采用的模式都要留下 Zotero item/attachment、section、PDF page、短片段和抽象模式；metadata-only 记录不能支撑全文语言判断。

输出必须包含 `Domain Style Calibration`、`corpus_status`、`calibration_confidence`、peer corpus、观察到的模式、草稿对照和作者需确认的选择。与父 Skill 交接时，同时填充 `Zotero Style Evidence Ledger`，使每条可采用模式都能回溯到 item/attachment、章节和 PDF 页码；不要使用“高分论文写法”作为事实结论，除非用户提供了明确、可核验的选文标准。

## 2.2 Introduction 逻辑协议

对 Introduction 的完整审阅，先给每段分配一个主要 rhetorical job，再修改句子。常用顺序是：

1. 研究现象或问题的具体重要性；
2. 已知事实与已有解释；
3. 仍未解决的具体变量、关系、尺度或可识别性 gap；
4. 为什么当前数据/设计/方法能够解决该 gap；
5. 研究目标、主要贡献和必要的边界。

检查以下失效模式：背景过宽、文献按作者罗列、`few studies have...` 作为唯一 gap、方法清单没有回答“为什么能补 gap”、贡献提前超过 Results、Introduction 的承诺在后文没有回收。每段只保留一个主要任务；每个 `however` 必须真正改变前文的逻辑方向。

输出 `Introduction Logic Map`：

```markdown
| Paragraph | Primary job | Main claim | Evidence/citation role | Missing bridge | Action |
|---|---|---|---|---|---|
```

把 Introduction 的 `gap → objective → contribution` 与 paper contract 对齐。需要逐段重写或中英转换时，交给 `academic-introduction-polisher`；交接必须带上 gap 类型、段落任务、需要保留的证据强度和不可新增的主张。

## 2.3 Discussion 逻辑协议

对 Discussion 的完整审阅，围绕“结果允许我们解释到哪一步”组织段落，而不是把 Results 再说一遍。每个主要发现应沿以下路径推进：

`finding → interpretation → comparison with literature → alternative explanation/constraint → bounded implication`

检查以下失效模式：把 Discussion 写成第二个 Results、机制解释没有独立约束、把相关写成因果、把模型输出写成直接观察、没有处理替代解释、限制只写成泛泛的“仍需更多研究”、future work 没有可区分的对象/方法/预测、Conclusion 新增未验证主张。

输出 `Discussion Logic Map`：

```markdown
| Paragraph | Finding used | Interpretation level | Literature comparison | Alternative/limitation | Implication boundary | Action |
|---|---|---|---|---|---|---|
```

限制句必须说明“什么受限、影响哪条推断、主结论是否仍成立”；未来工作必须说明研究对象、方法或观测，以及能够区分替代解释的预测。需要逐段重构、翻译或润色时，交给 `academic-discussion-polisher`；交接必须带上 finding IDs、证据等级、替代解释和需要核对的引用。

## 2.4 Methods 逻辑协议

Methods 的地道表达首先服务于可复现性和可审查性。不要把 Methods 改成漂亮的流程摘要，也不要用“按常规方法”“如前所述”掩盖关键条件。先识别研究设计和适用的报告规范，再按读者实际执行研究的顺序检查：

1. **设计与场景**：研究设计、场所、时间窗、伦理与注册信息是否明确；不要把事后看到的结果写成预先设定的分析。
2. **样本与变量**：来源、纳入/排除、分组、暴露/干预、结局、测量工具和分析单位是否定义一致；同一变量在 Methods、Results、表格和图注中使用同一术语。
3. **操作流程**：关键步骤、顺序、时间、剂量/浓度、设备/试剂、软件版本、阈值、质量控制和重复结构是否足以复现；缺失信息标为 `unknown` 或 `author check`，不能按领域惯例补写。
4. **统计分析**：模型、协变量、假设检查、效应量、置信区间、多重比较、缺失值、敏感性分析和显著性阈值是否与 Results 实际报告相匹配；不要把 p 值写成唯一结果，也不要将预设和探索性分析混为一谈。
5. **方法—结果对齐（Methods–Results alignment）**：每个 Results 中出现的主要变量、样本、模型、比较和验证步骤都应在 Methods 找到来源；Methods 声称会做但 Results 没有报告的内容要标记为未回收或解释缺失。

Methods 的段落通常采用“目的/设计 → 操作条件 → 质量控制或判定规则”的节奏。可以根据领域语料校准主动/被动语态、时态、术语和报告规范，但不得为了模仿 peer paper 删除可复现细节或改变实际执行顺序。

输出 `Methods Logic Map`：

```markdown
| Subsection | Operational job | Required details | Results cross-link | Missing/ambiguous | Action |
|---|---|---|---|---|---|
```

需要完整 Methods 改写时，交给 `methods-section-writer` 或 `method-writing`；需要从 peer paper 或用户提供的全文重建实际流程时，交给 `methods-reverse-engineer`。交接必须携带 study design、reporting guideline、未解决的可复现性字段和不可新增的参数。

## 2.5 Results 逻辑协议

Results 的语言要让读者清楚“做了什么比较、观察到什么、证据在哪里”，同时把解释留在 Discussion。先建立结果层级，再润色句子：

1. **结果顺序**：根据研究问题组织样本/数据质量、主要结果、支持性分析、敏感性/亚组分析和验证，而不是机械按分析执行时间或图号递增。
2. **段落功能**：每段先交代为什么读者现在需要这个分析，再报告一个主要发现；用定量锚点（n、效应量、方向、单位、CI、P 或其他适当指标）支撑发现，并准确指向图/表/补充材料。
3. **结果边界**：Results 可以报告观察到的关联、差异、模型性能和验证表现，但不把它们提前写成机制、因果、临床价值或“证明”；`show/indicate/suggest` 必须与研究设计和 A–E evidence level 匹配。
4. **图表一致性**：正文、图注、表格、分组、时间点、单位、样本量和方向必须一致；不能从图像目测精确数字，也不能为了叙事删除不支持主线的结果。
5. **读者推进**：避免连续使用 `we next asked`、`to investigate this` 等程序化开头；每个小节结尾说明下一分析承接什么问题，但不提前写 Discussion 的解释。

输出 `Results Logic Map`：

```markdown
| Result block | Reader question | Finding/quantitative anchor | Figure/table | Support vs primary | Interpretation boundary | Action |
|---|---|---|---|---|---|---|
```

Results 结构混乱时交给 `results-section-structurer`；科学内容已稳定、但段落开头、过渡和节奏生硬时交给 `results-section-revision`；正文与图注/表格数值或标签不一致时交给 `result-figure-consistencycheck` 和 `paper-claim-audit`。交接必须携带 finding IDs、图表位置、原始数字/单位、证据等级和不允许改变的结果方向。

## 3. 思考路由：先选一个主模型

本 Skill 使用 `thinking-model-router` 的约束：先定义领域和问题类型，再按机制选择一个 primary route；只有 primary 留下实质盲点时才组合模型，最多三个。论文修改的默认特征是：

```text
domain: academic writing / research argument
problem_type: diagnose + optimize
constraints: evidence-bound, information often incomplete, revisions are reversible,
             but overclaim and unsupported novelty have high reviewer cost
```

如果宿主使用 Skill namespace 调用叶子模型，按 router 规定把 `thinking-systems` 等 route 映射为 `thinking-skills:thinking-<slug>`；不要自行发明未在 catalog 中出现的模型名。

在选择思考模型前，先选择最具体的写作工作流。语言编辑、Methods/Results 专用 Skill 和 Introduction/Discussion 专用 polisher 已经是机制明确的叶子 Skill，不需要为了形式再调用一个思考模型：

| 观察到的主要问题 | 首选工作流 | 何时再加思考模型 |
|---|---|---|
| 句子不自然、翻译腔、术语/时态/指代不稳，但主张明确 | `medical-english-precision-editor` 或 `writing-core` | 只有证据强度或段落逻辑也不清楚时 |
| Introduction 段落功能、gap、目标或贡献推进不清 | `academic-introduction-polisher` | 贡献本身依赖未经证明的惯例时加 `thinking-first-principles` |
| Methods 缺少可复现细节，或 Methods 与 Results 的变量/模型/样本对不上 | `methods-section-writer`、`method-writing` 或 `methods-reverse-engineer` | 设计选择或预设/探索性边界不清时加 `thinking-socratic` |
| Results 像图注堆砌、主结果被支持性分析淹没或解释混入 Results | `results-section-structurer` 或 `results-section-revision` | 主结果层级与全文贡献冲突时加 `thinking-systems` |
| Results 正文、图注、表格的数字/标签/方向不一致 | `result-figure-consistencycheck` + `paper-claim-audit` | 发现会改变核心结论时加 `thinking-steel-manning` |
| Discussion 中结果、解释、替代解释、限制或意义链断裂 | `academic-discussion-polisher` | 审稿人可能提出强反驳时加 `thinking-steel-manning` |
| 多章节互相牵扯，局部改写无法稳定主线 | 本 Skill 的 `whole_paper` | 以 `thinking-systems` 为 primary |

按观察到的主要问题选择 route：

| 主要症状 | Primary route | 只回答的关键问题 |
|---|---|---|
| 各章节都合理但合起来没有方向，结果、讨论和结论互相牵扯 | `thinking-systems` | 哪些章节/主张/证据之间的反馈和断裂造成了整体问题？最高杠杆的结构改动是什么？ |
| “创新性”依赖惯例、空泛定位或没有拆到研究对象/方法/结果 | `thinking-first-principles` | 去掉未经证明的写作惯例后，这篇论文不可替代的最小贡献是什么？ |
| 论文看起来顺，但审稿人可能从替代解释、因果跳跃或范围外推发起攻击 | `thinking-steel-manning` | 最强的反对意见是什么？哪条证据或限定会迫使我们改写主张？ |
| 研究问题、术语、比较对象或成功标准不清楚 | `thinking-socratic` | 哪一个未定义的前提正在拖累全文？解决它后下一步改什么？ |
| 一个 primary 已经完成，但仍有一个高风险盲点需要独立检查 | `thinking-model-combination` | 哪个互补模型能回答 primary 没有回答的唯一问题？冲突时按什么证据规则裁决？ |

`domain_style_calibration` 本身不是一个思考模型；它是一个语料校准工作流。若对照发现问题来自章节之间的反馈、读者路径或贡献定位，再按上表选择一个 primary route；不要为了“像论文”额外叠加模型。

不要为了“全面”同时运行多个近邻模型。路由输出至少包含：`route`、`role`、`unique_question`、`blind_spots`、`exit`。若没有明显机制匹配，使用 `NONE`，直接按本 Skill 的证据和结构门禁分析。

### 3.1 组合规则

默认顺序是 `narrow → stress → decide`：

1. 一个结构或贡献模型确定主要问题；
2. 只有出现高风险反驳盲点时，追加一次 steel-man 或证据审计；
3. 用证据等级、结果可追溯性和修改可逆性裁决冲突；
4. 只保留真正改变行动计划的洞见。

15 分钟内没有新洞见、模型只是换词复述，或输入不足以支撑模型时，停止路由并报告不确定性。

## 4. 统一执行流程

### Step 1：写出 paper contract

从实际稿件中压缩出一份可核对的契约，不补写缺失内容：

```text
question: 这篇论文回答什么可检验问题？
population_or_object: 研究对象、数据或样本是什么？
method: 用什么方法回答？
main_finding: 最主要的结果是什么？
contribution: 相对于已有工作新增了什么？
boundary: 结果不能推出什么？
```

若 `question`、`main_finding` 或 `boundary` 无法从材料中稳定提取，先标为 `undefined`，把“定义它”列为 P0，而不是用漂亮措辞填空。

### Step 2：重建五句 argument spine

用五句短句重建：

1. 已知问题或重要性；
2. 现有证据的具体缺口；
3. 本研究的问题、设计和比较对象；
4. 最主要的结果及其证据位置；
5. 结果允许的解释、贡献和边界。

每句标注 `Current study`、`Zotero external evidence`、`PubMed external evidence`、`Interpretive bridge` 或 `Unsupported gap`。若第 2 句没有 gap、第 4 句找不到结果位置或第 5 句超出证据，先修主线，不先做语言润色。

### Step 3：画 claim–evidence–section 图

建立一张轻量矩阵，每个核心 claim 一行：

| Claim ID | 主张 | 所在章节/图表 | Source layer | Evidence level | 直接证据位置 | 解释边界 | 缺口 |
|---|---|---|---|---|---|---|---|
| C1 | ... | Results/Fig. 2 | Current study | D | ... | ... | none |

检查三种错位：

- 章节说了一个结果，但没有对应表格、图或分析；
- Discussion 把 C 级机制合理性写成 A 级直接证据；
- Introduction 的承诺没有在 Results/Discussion 中回收，或 Conclusion 新增了结果。

### Step 3A：先做语言层审阅

对用户要求修改的章节先做一次轻量语言 pass，生成语言问题表和一版保守的 Copy-ready text。只修复会影响理解、科学精确度或学术自然度的问题；不要在全文结构未稳定时追求逐词完美。把每个改动标记为“语言变化”或“可能改变科学含义”，后者必须进入 Author check。

### Step 3A.1：需要选择时生成多方案卡片

当用户要求多个版本、不同角度或领域化表达时，按 [WRITING_OPTIONS_CARD](references/writing-options-card.md) 生成最多三个候选。先完成 meaning gate 和 section logic，再分别给出 `Conservative`、`Field-native`、`Logic-forward` 或章节专用角度；每个候选都必须带 `option_id`、`rhetorical_angle`、`claim_delta`、`evidence_level`、`citation_set`、`style_basis`、`when_to_choose`、`risks` 和 `author_check`。在作者选择前设置 `selection_status: pending`，选择后才生成最终 copy-ready 文本并运行最小 `POST_WRITE_AUDIT`。

### Step 3B：针对各章节做 section logic pass

- 若包含 Introduction，输出 `Introduction Logic Map`，确认具体 gap、方法适配和 contribution 在段落之间递进；
- 若包含 Methods，输出 `Methods Logic Map`，确认设计、样本、变量、流程、统计和质量控制足以复现，并与 Results 的实际报告对齐；
- 若包含 Results，输出 `Results Logic Map`，确认结果块按研究问题推进，主要结果与支持性/验证性结果分层，定量锚点和图表引用准确，且没有把 Discussion 的解释混入 Results；
- 若包含 Discussion，输出 `Discussion Logic Map`，确认每个主要 finding 都经过 interpretation、literature comparison、alternative/limitation 和 bounded implication；
- 若提供多个章节，检查 Introduction 的最后一个承诺是否在 Methods 中有设计支撑、在 Results 中有证据位置、并在 Discussion 中被逐项回收；同时检查 Methods 的分析顺序与 Results 的叙事顺序是否发生不可解释的错位。

### Step 3C：需要时建立领域风格画像

仅当用户请求“地道/领域写法/目标 venue 校准”或稿件存在稳定的术语与表达风格漂移时执行。先完成 Step 3B，再读取
[references/domain-style-calibration.md](references/domain-style-calibration.md)，生成 `style_corpus_ledger` 和 `Domain Style Calibration`。若 Zotero/PubMed 不可用，继续做 genre-neutral language pass，并明确 `corpus_status: unavailable`；不得把模型常识写成已经核验的领域模式。

### Step 4：检查章节角色和读者路径

给每个章节分配一个主要工作：

| 章节 | 主要任务 | 应该回答 | 常见失效 |
|---|---|---|---|
| Introduction | 建立问题与 gap | 为什么现在要做？ | 背景堆积、gap 模糊、贡献提前夸大 |
| Methods | 让设计可审查 | 如何回答问题？ | 方法清单没有与问题/结果绑定 |
| Results | 展示证据 | 发现了什么？ | 讨论混入结果、图表没有叙事顺序 |
| Discussion | 解释和限定 | 结果意味着什么？ | 重复 Results、把关联写成因果、忽略替代解释 |
| Conclusion | 收束贡献与边界 | 读者应带走什么？ | 新增未验证主张、泛化超出样本 |

把“作者想说什么”与“读者下一步需要知道什么”分开记录。优先修复阻断读者路径的结构问题，再处理局部句式。

### Step 5：运行 primary thinking route

按第 3 节选出的模型运行一次，保留：

- `route_used` 与选择理由；
- 该模型唯一回答的问题；
- 它发现的一个结构性洞见；
- 它没有覆盖的盲点；
- 一个可以证伪或迫使改写的观察。

不要把模型名称当作结论。结论必须落回稿件中的章节、claim、图表、引用或缺失材料。

### Step 6：做一次审稿人压力测试

从最强反对意见出发，至少检查：

1. 结果是否被写成超出设计的因果、预测或机制结论；
2. 替代解释、混杂、样本或数据范围是否影响主结论；
3. 关键引用是否真的支持该句，而不是只支持背景；
4. “首次”“重要”“独立”“一致”“临床意义”等范围词是否有足够证据；
5. 去掉一张图、一个分析或一条引用后，主线是否仍成立。

每项写出 `objection → evidence → required wording/action`。没有证据时写 `unknown`，不要替审稿人编造结果。

### Step 7：按杠杆和风险排序

给每个问题打分：

```text
priority_score = reviewer_risk (1–5) × argument_leverage (1–5) × feasibility (1–5)
```

分数只是排序工具，不替代判断。优先级含义：

- `P0`：会改变核心结论、研究问题或证据合法性；先补材料、重分析、删掉或重构；
- `P1`：会显著影响读者理解或审稿判断；优先调整主线、章节顺序、图表叙事或讨论边界；
- `P2`：局部证据、引用、术语或段落问题；交给 Zotero evidence/citation 模块；
- `P3`：语言、格式和风格润色；最后处理。

将行动类型限定为：`retrieve evidence`、`re-analyze`、`restructure`、`reframe`、`rewrite`、`remove`、`verify`。只有用户明确授权且材料足够时才把 `re-analyze` 写成下一步；否则标记为待决策。

### Step 8：生成短迭代计划并设置停止条件

输出最多三轮：

1. `Round 1 — meaning and section logic`：修 question/gap/contribution、Introduction/Discussion 段落任务、结果顺序和结论边界；
2. `Round 2 — language`：在意义稳定后做句法、衔接、术语、密度、语气和中英文自然度检查；
3. `Round 3 — evidence and consistency`：核引用、补图表映射、检查全文术语/claim verb 一致性和投稿格式。

每轮必须有可观察的完成条件，例如“Introduction 的 gap 能在两句内说清，且每个核心贡献在 Results/Discussion 有证据位置”。当主线、证据边界和读者路径已经稳定，再停止整体诊断，转回局部编辑。

## 5. 输出契约

完整运行使用 `MANUSCRIPT_STRATEGIC_REVIEW`；自动 checkpoint 只输出其中的“状态、最高优先级问题、下一步”三部分。报告必须包含：

1. `Scope and Input Ledger`；
2. `Router Decision`；
3. `Paper Contract`；
4. `Language Audit`；
5. `Domain Style Calibration`（仅在请求或 checkpoint 条件满足时）；
6. `Introduction Logic Map`（若提供 Introduction）；
7. `Methods Logic Map`（若提供 Methods）；
8. `Results Logic Map`（若提供 Results）；
9. `Discussion Logic Map`（若提供 Discussion）；
10. `Argument Spine`；
11. `Claim–Evidence–Section Map`；
12. `Holistic Diagnosis`；
13. `Reviewer Stress Test`；
14. `Prioritized Revision Plan`；
15. `Revision Decision Log`：每项改动的原句/动作、证据边界、peer pattern（如有）、`author_check` 和完成条件；
16. `WRITING_OPTIONS_CARD`（用户要求多个版本时）与候选比较表；
17. `Handoff and Stop Conditions`；
18. `Unresolved Unknowns`。

局部改写也必须返回一个最小 `POST_WRITE_AUDIT`：`claim_unchanged`、`numbers_units_direction_unchanged`、`citation_ownership_preserved`、`methods_results_aligned`、`new_unsupported_claim` 和 `author_check`。任何一项无法确认都写 `unknown`，不以“更地道”代替回查。

问题表至少使用以下字段：

```markdown
| ID | Location | Problem | Evidence / basis | Risk | Leverage | Priority | Action type | Next owner | Done when |
|---|---|---|---|---|---|---|---|---|---|
```

最终聊天摘要只需要给出：`Scope`、`Primary route`、`P0/P1` 项、下一步模块和关键未知项；不要把完整内部推理过程当成论文正文。

## 6. 与现有 Zotero 工作流的交接

本 Skill 负责“决定先改什么”，现有模块负责“把这一项做实”：

| 诊断结果 | 交接模块 | 交付物 |
|---|---|---|
| 缺少外部支持或引用错位 | `zotero-evidence-review` Module 1 / 2 / 2.2 / 3 | evidence matrix、citation repair、verification |
| Current study 与 external evidence 混淆 | Module 2 + Module 2.5 | source-layer、A–E level、copy-ready/annotated text |
| 数字、范围或图表说法可能不忠实于结果 | `paper-claim-audit` | paper-to-raw-evidence audit |
| 审稿意见需要分流和排序 | `revision-strategy-planner` | feasibility-aware revision plan |
| 中文表面表达、AI 化或排版问题 | `writing-core` | 三轮结构/语言/排版检查 |
| 英文医学稿的术语、句法、语气和意义保持 | `medical-english-precision-editor` | precision edit with meaning-preservation notes |
| 需要与同领域/目标 venue 论文校准地道表达 | `writing-core` 或 `medical-english-precision-editor` | 携带 `Domain Style Calibration`、peer pattern、confidence 和不可改变的 claim/term 约束 |
| 写作卡点需要先从 Zotero 学习表达、方法命名或结果推进 | `zotero-literature-learning` → `evidence-driven-writing`（引用驱动段落） | `writing_block_card`、source locations、2–3 个候选版本、evidence map/paragraph blueprint 和 author checks |
| Introduction 的段落功能、gap、目标和贡献链 | `academic-introduction-polisher` | logic map + revised Introduction |
| Methods 的可复现性、报告规范和与 Results 的对齐 | `methods-section-writer` / `method-writing` / `methods-reverse-engineer` | Methods Logic Map + reproducibility audit + author checks |
| Results 的顺序、段落推进和主/支持结果分层 | `results-section-structurer` / `results-section-revision` | Results Logic Map + revised Results |
| Results 与图注、表格、数字或方向不一致 | `result-figure-consistencycheck` / `paper-claim-audit` | discrepancy report + claim-level repair |
| Discussion 的 finding–interpretation–limitation 链 | `academic-discussion-polisher` | logic map + revised Discussion |
| 需要全文生产、图表和独立审查编排 | `paper-spine` | 同一任务中的完整论文生产/修订流程 |

交接时必须携带 `claim IDs`、章节位置、证据等级、风险和 `Done when`，避免下游重新猜测问题。

## 7. 安全与质量门

- 不编造数据、结果、引用、审稿意见、贡献或实验可行性。
- 不把“高分论文”“顶刊写法”当作未经核验的事实；peer papers 只能提供可追踪的写作模式，不能替代作者的证据或贡献。
- 不复制同领域论文的长句、独特短语、数据、贡献叙述或结论；输出必须从用户自己的主张和证据生成。
- 没有匹配且可检查的 peer corpus 时，明确 `corpus_status: unavailable/partial`，使用 genre-neutral 建议，不声称完成领域校准。
- 不把 Zotero/PubMed 的背景或机制文献写成当前研究结果的直接证明。
- 不为 Methods 补写未提供的样本、参数、软件版本、统计模型、伦理信息或实验步骤；缺失项必须标为 `unknown` / `author check`。
- 不为 Results 改变数字、方向、样本量、单位、置信区间、P 值、图表归属或分析性质；不把支持性、探索性或验证性分析升级为主要发现。
- 不把 Methods 中计划执行的分析写成已经完成的 Results，也不把 Results 中观察到的结果倒灌成事后预设。
- 不把“模型认为更好”当作证据；所有高优先级判断必须指向实际稿件、结果、图表或引用。
- 不自动删除用户内容；`remove` 只是建议动作，执行前保留原文并说明原因。
- 不把结构诊断误报为投稿 readiness、统计有效性或独立同行评审。
- 如果 Zotero/PubMed 不可用，继续做结构诊断，但把证据状态写为 `not inspected`，不伪造检索完成。
- 如果输入材料互相矛盾，优先标记冲突并停止扩展结论；不要用措辞掩盖冲突。
- 多方案必须共享数字、方向、研究设计和证据边界；任何 claim delta 都必须显式标记并要求作者确认。
- 同一问题连续两轮没有新证据或新行动时停止，避免重复建议。

## 8. 触发示例

```text
/zotero-manuscript-thinking
请从全文角度审视这篇论文：先判断主线、贡献、证据边界和最值得优先修改的三件事，不要直接重写全文。
```

```text
/zotero-manuscript-thinking
请参考 Zotero 中 3–5 篇与本研究同领域、同文章类型的代表性论文，检查这段 Introduction 的语言和段落推进是否符合该领域常见写法。先给出 Domain Style Calibration 和 confidence，再给保守的 copy-ready 改写；不要复制原文，不要改变 claim 强度。
```

```text
/zotero-manuscript-thinking
请参考 Zotero 中同领域、同研究设计的论文，检查我的 Methods 是否足以复现，并核对每个 Results 变量、模型和图表是否在 Methods 中有来源。先给 Methods Logic Map、Results Logic Map 和缺失项，再做保守润色；不要补写未提供的参数或改变结果数字。
```

```text
/zotero-evidence-review
帮我补充下面段落的引用并润色。段落来自 Discussion；在给出改写前，如果它会影响全文结论，请先做一次 manuscript-level checkpoint。
```

## 9. 结束条件

满足以下条件即可结束整体诊断并转回局部工作：

- paper contract 的 question、finding、contribution 和 boundary 已能从材料中核对；
- argument spine 的每个核心 claim 都有章节、结果或证据位置；
- P0/P1 问题已经有明确 action 或被明确标为缺材料；
- 主要审稿反驳有对应的证据、限定或待验证项；
- 如果启用了领域校准，peer corpus、选择理由、访问状态和 `calibration_confidence` 已记录，且每个建议都能回溯到模式或明确的 genre rationale；
- 后续修改可以交给具体模块，且不需要继续添加新的思考模型。

若这些条件无法满足，输出 `Partial`，列出阻断材料和下一次最小输入。
