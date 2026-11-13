---
name: zotero-evidence-review
description: Search, analyze, verify, and export Zotero-grounded evidence packages with Markdown evidence reports, a sentence-level Citation Insertion Sheet, evidence-backed manuscript polishing, and EndNote-compatible RIS references. Paste a paragraph and ask for citations; the skill will split sentences, search Zotero first, expand to PubMed when available, verify support, polish wording without widening claims, and export a traceable RIS. Requires Zotero MCP to be configured.
license: MIT
compatibility: Codex, OpenCode, ZCode (zcode)
metadata:
  workflow: academic-research
  requires: zotero-mcp
  optional: pubmed-mcp
  version: 4.0.0
  references: references/method-parameter-search.md,references/recall-first-retrieval.md,references/retrieval-rescue-protocol.md,references/endnote-section-collections.md,references/writing-options-card.md,references/citation-insertion-sheet.md,references/report-layout.md
---

# Zotero Evidence Review Skill

## Overview

Use Zotero MCP tools to search the user's Zotero library intelligently, and use PubMed MCP tools as a biomedical expansion and metadata-standardization layer whenever they are visible in the active Agent IDE session. This skill combines **semantic search** (concept matching via embeddings) with **keyword/structured search**, performs **paragraph evidence and citation analysis** from draft text, verifies **citations against full text**, and generates Markdown + EndNote-compatible RIS outputs for ordinary literature search, target literature search, paragraph citation matching, and paragraph polishing workflows unless the user explicitly chooses chat-only/no-export mode. When a rewrite request asks for alternatives, it uses the shared [WRITING_OPTIONS_CARD](references/writing-options-card.md) so every candidate has a rhetorical angle, evidence level, citation set, and explicit selection status.

For paragraph citation-support requests, the default is one complete **Paragraph Citation Package Workflow** rather than two separate workflows: paragraph → claim extraction → existing numbered citation repair when supplied references are present → one Zotero local search pass → evidence matrix and sentence-level citation recommendations → **evidence-backed manuscript polishing** → **Copy-ready Manuscript Text → Claim–Evidence Matrix with Chinese claim summaries → Citation Insertion Sheet** → optional WRITING_OPTIONS_CARD → annotated/diff paragraph → Zotero metadata + PDF links → automatic PubMed expansion as a second evidence source when available → combined evidence synthesis and deduplication → reference export standardization by PMID/DOI → metadata QC → Markdown evidence report → EndNote RIS. Chat-only paragraph analysis and explicit `preserve wording` requests are opt-out modes for the corresponding layers.

## 0.1 Route contract: one request, one evidence owner

Use this compact contract before calling an MCP tool. It keeps the three Zotero writing skills complementary and prevents a single request from producing competing corpora or reports:

| User need | Primary owner | This Skill does | Handoff / stop condition |
|---|---|---|---|
| Find and learn peer papers before writing | `zotero-literature-learning` | Do not start a second corpus; consume its `MATERIALS_PACKAGE` only when claim support is requested | Stop after `handoff.done_when` or return to this Skill for claim verification/RIS |
| Support a concrete claim or paragraph | `zotero-evidence-review` | Search, inspect, verify, place citations, canonicalize metadata, and export | Every selected record has an inspected source status and a RIS action |
| Decide what to fix across a manuscript | `zotero-manuscript-thinking` | Do not silently rewrite the whole paper; consume `style_profile`/`argument_profile` and issue a prioritized plan | Stop at `P0–P3` plan or hand off one concrete action |
| Verify one source against one claim | `zotero-evidence-review` | Read the cited item/PDF and classify support | Return `fully supported`, `partially supported`, `contradicted`, or `not addressed` |

The route is part of the output contract. Record `route`, `source_layer`, `inspection_status`, `claim_ids`, `output_files`, and `stop_reason` in the report or chat summary. If the request changes route (for example, from style learning to citation support), record the handoff instead of silently restarting discovery.

---

## 0.2 默认稿件交付契约：证据驱动润色 + 引文插入表

对英文段落执行“找引文、补引用、使用技能、根据文献优化、润色、polish、improve wording、field-native、rewrite based on literature、insert citations”等请求时，完成证据核查后**默认同时执行证据驱动的英文润色**。这层润色不是另起一个无证据的语言任务，而是把证据等级、研究设计、术语边界和同领域写法一起反映到可投稿的英文中。只有用户明确说“保留原文措辞 / 只找引文 / 不润色 / citation-only”时才跳过润色层。

默认交付顺序固定为（先给作者可粘贴内容，再给逐句核查依据；唯一报告布局见 [references/report-layout.md](references/report-layout.md)）：

1. `Copy-ready Manuscript Text`：作为报告的第一块实质内容，保留原文语言，完成语法、逻辑、领域惯用表达和证据强度校准，并在句内放入选定引文。
2. **紧随其后的 `Claim–Evidence Matrix`**：逐句/逐主张对应修改后的正文，固定包含 `sentence_id`、`claim_id`、修改后句子或从句、`主张摘要（中文）`、推荐引文、`Evidence role`、单一 `Evidence level`、`Source layer`、`Support verdict`、`insertion_anchor` 和 `Manual action`。作者先看这一张表，就能判断每个引文为什么放在该处。
3. `Citation Insertion Sheet`：把矩阵中的可用引文转成实际操作清单，逐句给出插入锚点、可复制的作者–年份引文、快速检索词、canonical record、PMID/DOI 和 RIS 动作；不重复完整证据解释。
4. `Annotated Recommended Text`：说明每处改写、证据边界、引用作用和审稿风险。
5. `Diff / Change Log`：列出原短语、改后短语、改动类型、原因和证据等级。
6. 审计附录：`Evidence Logic Chain`、`SENTENCE_CITATION_MATRIX`、`Citation Support Ledger`、参考文献表、Metadata QC 和 RIS；这些部分不得引入新的引用决定。

### Manual Citation Fast Path（手动添加引文快速路径）

1. 先复制 `Copy-ready Manuscript Text`，其中的作者–年份引文已经放在句子或从句的正确位置。
2. 立即查看其后的 `Claim–Evidence Matrix`：按 `sentence_id` 找到对应的 `claim_id`，确认该引文支持的是哪一个具体主张，以及证据等级和措辞边界。
3. 在 Zotero 或 EndNote 中用 `search_tokens`（通常为 `FirstAuthor Year` 或短标题）搜索，在 `insertion_anchor` 处插入 `copy_ready_citation`。
4. 用 `Citation Insertion Sheet` 做逐句勾选；PMID、DOI 和 Zotero key 只用于核查、去重和追踪，不直接粘贴进正文。
5. 最后在审计附录中用 `SENTENCE_CITATION_MATRIX` 和 `Citation Support Ledger` 检查是否有遗漏、重复或只支持部分从句的引文；如果与前面的矩阵冲突，以矩阵和 Ledger 的已核查记录为准并记录修正。

### 引用样式与插入规则

- 默认 `citation_style = author_year`，可接受 `numbered_vancouver`、`apa_like` 或用户提供的期刊样式；用户未指定时不要擅自改成编号制。
- 作者–年份的可复制字符串与检索词分开保存，例如 `copy_ready_citation = (Mir et al., 2013)`，`search_tokens = Mir 2013`。
- 插入锚点必须写到句子或从句之后（例如 `after “incident NAFLD”`），不能只写“本段末尾”。一个引文只覆盖它实际支持的 claim。
- Citation Insertion Sheet 使用 canonical record 的 DOI/PMID/Zotero key 追踪同一条记录；RIS 是给 Word/EndNote/Zotero 的稳定导入交接，不默认直接修改用户的 Word 或 Zotero 库。
- 末尾给出一行操作说明：Word + Zotero 用 `Author Year` 搜索后插入；EndNote 导入 RIS 后用 `Insert Citation` 搜索；手动稿件直接复制 `copy-ready citation`。编号制由 Word/EndNote 在最终文档中自动重排。

### 证据驱动英文润色的边界

- A/B 证据允许中等强度陈述；C 必须使用 plausibility、may、consistent with 等桥接措辞；D 明确写成当前研究结果；E 删除、验证或改为 knowledge gap。
- 语言润色不得扩大原始 claim，不得把观察关联写成因果，不得把短睡眠、睡眠质量或复合生活方式指标改写成 insomnia，也不得把外部文献写成当前研究结果的证明。
- 润色至少检查四层：grammar/clarity、field-native phrasing、argument flow、evidence calibration；每一层都要在 `Diff / Change Log` 中留下可读原因。

## 素材学习入口

当用户要求“先收集素材、阅读 Zotero 全文、学习同领域论文写法，再开始改稿”时，优先交接给 `zotero-literature-learning`。它负责候选筛选、摘要/全文分层阅读、peer corpus 和 Evidence/Style/Argument Profile；本 Skill 继续负责逐条证据支持、引用核实和 RIS。不要让两个 Skill 为同一任务各自建立一套文献出口。

## 0. Intent Detection

Route the user's request before choosing tools. Use the input shape and explicit trigger words; do not ask the user to choose a mode when the intent is clear.

| Intent | User input features | Route to |
|--------|---------------------|----------|
| `method_parameters` | Requests for method/software parameters, thresholds, hyperparameters, defaults, settings, adjustment advice, or the exact Methods passage (e.g. "GSMR 参数怎么设", "原文在哪段") | **Module 1.2: Methodology Parameter Extraction and Report** |
| `search` | Keywords, concepts, natural-language questions, broad topic discovery, or requests such as "search", "find papers", "what literature do I have about…" | **Module 1: Semantic + Structured Search**, then auto-export Search Report + RIS unless chat-only/no-export is explicit |
| `target_literature_search` | Topic/question asks which papers use a data source, method, phenotype, cohort, disease area, or research direction; user wants literature discovery, screening, search report, MD, RIS, or EndNote export, and no manuscript paragraph is supplied | **Module 1.8: Target Literature Search and Export** |
| `paragraph` | A pasted manuscript paragraph, draft section, or multi-sentence passage that asks for chat-only evidence analysis, with no citation/export/full-workflow trigger | **Module 2: Paragraph Evidence & Citation Analysis** |
| `manuscript_strategy` | Requests for a whole-manuscript view, language/表达 quality, field-native wording, peer-paper or target-venue style calibration, Methods/Results/Introduction/Discussion logic, reproducibility, result narration, argument spine, contribution, novelty, reviewer-risk, revision priority, or "从整体上看看/跳出来看"; also a full manuscript or repeated local revisions that trigger the checkpoint conditions below | **Module 2.8: Manuscript-Level Thinking Checkpoint**, implemented by the companion `zotero-manuscript-thinking` Skill |
| `package` | Requests using `/zotero-evidence-review`, saved files, EndNote/RIS export, evidence package, "使用技能", "完整工作流", "找证据", "找引文", "补引用", "推荐引用", "citation", "refs", "参考文献", "文献引用", "生成报告", "保存结果", "导出参考文献", or a paragraph/search request that asks for citation placement, reusable writing outputs, file outputs, or evidence-backed polishing (`润色`, `英文表达`, `地道`, `改进写作`, `改写`, `根据文献优化`, `基于调研润色`, `polish`, `improve wording`, `field-native`, `rewrite based on literature`, `make it more academic`, `insert citations`) | **Paragraph Citation Package Workflow (Module 2 + Module 2.5): analysis stage, evidence-backed polishing and Citation Insertion Sheet, then export stage with automatic PubMed expansion after Zotero local search when available** |
| `reference_update` | A paragraph or manuscript passage with existing numbered citations/references, or requests such as "检查参考文献", "更新参考文献", "编号引用", "6不支持", "citation 6 does not support", "replace citation", "refresh RIS", "regenerate RIS" | **Module 2.2: Existing Numbered Citation Repair**, then **Module 2.5 Evidence Package Export** when files/RIS are requested or implied; treat this as a full reference-update workflow unless the user explicitly opts out |
| `verify` | Words such as "verify", "核实", "check", "confirm" plus a specific citation/paper and a concrete claim, quote, statistic, or citation-supported statement | **Module 3: Citation Verification Protocol** |
| `health` | "library status", "库状态", "health check", "健康检查", "preflight", "index status", or questions about Zotero database readiness | **Module 0.5: Library Health Check** |

### Routing Rules

**Method-parameter precedence**: when the user asks what settings a method used, what a parameter means or how to adjust it, or where the source describes it, route to **Module 1.2** before generic `search` or `target_literature_search`. If the user asks which studies merely use a method, route to Module 1.8. If the user supplies manuscript text for citation analysis, use Module 2. Read [references/method-parameter-search.md](references/method-parameter-search.md) for the evidence and report requirements.

**Manuscript-strategy precedence**: when a request contains both a broad package trigger such as `使用完整工作流` and a whole-manuscript goal such as `整体审视`, `语言表达`, `语言地道`, `同领域论文写法`, `target venue`, `Methods`, `Results`, `Introduction/Discussion`, `可复现`, `结果叙事`, `主线`, `贡献`, `审稿风险`, or `修订优先级`, route to `manuscript_strategy` / Module 2.8 first. Run citation package export only for the concrete evidence actions selected by the checkpoint.

**Zero-friction paragraph entry**: when the user invokes `/zotero-evidence-review` and pastes a paragraph with wording such as `帮我找这个段落的引文`, `给这段找参考文献`, `帮我补引用`, `find citations for this paragraph`, or `find references for each sentence`, treat the request as unambiguous citation-support work. Do not ask the user to choose a module, repeat the workflow, or provide claim IDs. Preserve the paragraph language and run the default **Paragraph Citation Package Workflow** automatically. Unless the user explicitly opts out of files, produce the Markdown evidence report, sentence-level citation matrix, Citation Support Ledger, and EndNote-compatible RIS.

1. **Slash command and simple-request entry**: `/zotero-evidence-review` is the recommended user-facing entry point. Treat it as a request to run this skill and auto-route from the user's short request; do not require the user to name modules or repeat the full workflow. When the short request asks for ordinary literature search, target literature search, evidence, citation support, paragraph polishing, reusable writing output, or an evidence package, default to the appropriate export workflow and write the Markdown report plus RIS unless the user explicitly opts out. When the request asks for a whole-manuscript diagnosis or revision strategy, route to Module 2.8 and the companion `zotero-manuscript-thinking` Skill before local rewriting.
2. **Paragraph-first, package by default for citation work**: if the user provides a paragraph, run Module 2 first. If the same request includes `/zotero-evidence-review`, `使用技能`, `完整工作流`, "find evidence", "find/add/recommend citations", `找证据`, `找引文`, `找这个段落的引文`, `给这段找参考文献`, `补引用`, `推荐引用`, `citation`, `refs`, `参考文献`, `文献引用`, or any request for saved/reusable writing outputs, continue automatically to the Paragraph Citation Package Workflow / Module 2.5 and write the Markdown report plus RIS file. If the paragraph is identified as part of a larger manuscript and the request changes the argument, contribution, conclusion, or section role, run the compact Module 2.8 checkpoint before presenting the copy-ready text; do not run a full checkpoint for a standalone paragraph with no manuscript context.
3. **Existing numbered citation repair first**: if the user provides manuscript text plus a numbered reference list, or explicitly says an existing citation number does not support the claim, route to **Module 2.2: Existing Numbered Citation Repair** before ordinary package export. Preserve the user's supplied citation numbers in the audit tables, but do not promise to preserve final manuscript numbering after RIS import; EndNote/Word will renumber according to the final included reference list and citation style.
4. **Reference-update requests default to the complete workflow**: requests containing `检查参考文献`, `更新参考文献`, `编号引用`, `replace citation`, `refresh RIS`, or `regenerate RIS` are not chat-only spot checks by default. Run claim mapping, support verification, replacement search when needed, metadata canonicalization, and final Markdown + RIS export unless the user explicitly opts out.
5. **Target literature search separation**: if the user asks "which papers use X", "find papers about X", "search Zotero for X", "export a literature list/report/RIS", or equivalent, and does not provide a manuscript paragraph to revise, route to `target_literature_search`, not the Paragraph Citation Package Workflow. This mode writes a Markdown search report and Search RIS by default, but it must not require Copy-ready Manuscript Text, sentence-level citation placement, or paragraph diff output.
6. **Search and target search export default / Target search export request**: if the user provides an ordinary topic/search question, route to **Module 1 Semantic + Structured Search** and write a Search Report + RIS by default. If the question asks for a data source, method, phenotype, cohort, disease area, research direction, `导出 MD`, `生成报告`, `保存报告`, `RIS`, `EndNote`, `文献清单`, `literature list`, or equivalent, route to **Module 1.8 Target Literature Search and Export** and write `LITERATURE_SEARCH_REPORT` + Search RIS by default. Only explicit `只在聊天输出`, `不要生成文件`, `不导出`, or `chat only` keeps search results in chat.
7. **Chat-only opt-out**: if the user explicitly says `只在聊天输出`, `不要生成文件`, `不导出`, `chat only`, or equivalent, stop after the relevant chat workflow and do not write package files.
8. **Verification requires specificity**: only route to `verify` when both a cited source (or item key/DOI/title) and a claim/quote/statistic are present. Otherwise, route to `search` or ask a clarification.
9. **Health check is read-only by default**: route health/status requests to Module 0.5 and do not run repair actions unless the user explicitly confirms them.
10. **Evidence package request**: if the user asks for saved reports, EndNote/RIS, an evidence package, or the default citation-support workflow above, run the underlying search/paragraph workflow first, then route to the Paragraph Citation Package Workflow / Module 2.5 for file generation. For topic-only search and target literature search exports, use Module 1 / Module 1.8 and `LITERATURE_SEARCH_REPORT` instead of `EVIDENCE_REVIEW_REPORT`.
11. **Manuscript-level checkpoint**: when Module 2, 2.2, or 2.5 detects the conditions in `zotero-manuscript-thinking/SKILL.md` (full-manuscript context, repeated local revisions, or high-risk evidence boundary), run the checkpoint before final wording. It decides what to fix first, preserves claim IDs and A–E evidence levels, and hands off concrete actions to the existing evidence, audit, revision, or writing modules. It is diagnostic; it does not silently rewrite the whole manuscript or commit the user to new experiments.
12. **Ambiguous intent**: if the request cannot be confidently routed, output this numbered menu and ask the user to choose:

```markdown
我可以按以下哪种方式处理？
1. 语义+结构搜索（关键词/概念/问句）
2. 目标文献检索与文献清单导出（主题/方法/数据集/表型）
3. 段落证据与引文分析（粘贴段落、找证据、补引用）
4. Evidence Package 导出（Markdown 报告 + EndNote RIS）
5. 精确核实（具体引用 + 具体主张/数据/引文）
6. 已有编号引文修复（段落 + 6/18/19 等参考文献编号）
7. 库健康度检查（库状态、索引、PDF覆盖率）
8. 全文论证与修订策略（主线、Methods/Results、贡献、证据边界、审稿风险）
```

### Dual-MCP Auto Search and Export Defaults

Use these defaults for every non-health, non-verify workflow:

1. **Dual-MCP auto search**: run Zotero first for local-library evidence, then automatically attempt PubMed expansion for biomedical ordinary search, target literature search, paragraph citation matching, paragraph polishing, method-parameter retrieval, and reference-update workflows when a PubMed-capable MCP tool is visible.
2. **Automatic export by default**: ordinary `search`, `target_literature_search`, paragraph citation matching, paragraph polishing, `method_parameters`, `package`, and `reference_update` workflows write Markdown + RIS outputs by default. The only general opt-out is explicit `只在聊天输出`, `不要生成文件`, `不导出`, or `chat only`.
3. **Ordinary search output**: Module 1 ordinary Zotero search default output is **Search Report + RIS**. Use a `LITERATURE_SEARCH_REPORT`-compatible search report without paragraph-only sections, and write Search RIS from inspected included records.
4. **Target search output**: Module 1.8 target literature search default output is `LITERATURE_SEARCH_REPORT` + Search RIS, with Core / Strong Related / Method Background / Disease GWAS Only / Noise / Verify classification and exclusion reasons.
5. **Method-parameter output**: Module 1.2 writes `LITERATURE_SEARCH_REPORT` + Search RIS by default and adds the `METHOD_PARAMETER_EVIDENCE` section. That section must contain inspected source passages, section/page locations, and Zotero item/PDF links. Do not add paragraph-writing sections unless the user also supplies a manuscript paragraph.
6. **Paragraph output**: Module 2 + Module 2.5 paragraph citation matching, paragraph polishing, and citation insertion default output is `EVIDENCE_REVIEW_REPORT` + Citation RIS, including Copy-ready Manuscript Text, the sentence-level Citation Insertion Sheet, Annotated Recommended Text, a Diff / Change Log, Citation Support Ledger, and evidence-backed wording changes.
7. **PubMed truth boundary**: PubMed expansion can be recorded as `Completed` only after an actual PubMed search ran and selected PMID metadata was inspected. If PubMed tools are absent or fail, record the planned/attempted query and use `⚠️ Tool unavailable; search not executed` or `Failed; query reported`; never create PubMed-only RIS records from planned, failed, or uninspected PubMed results.
8. **No route mixing**: search reports, target literature search reports, and method-parameter reports never include Copy-ready Manuscript Text, sentence-level citation placement, or paragraph diff unless the user supplies a manuscript paragraph. Paragraph evidence packages never use Search RIS as a substitute for claim-level Citation RIS.

### End-to-End Workflow Map

Use this map as the default execution path so the workflow remains continuous and auditable:

```text
intent routing → optional read-only library readiness check → Module 1 search, Module 1.2 method-parameter extraction, Module 1.8 target literature search/export, Module 2 paragraph analysis, Module 2.2 existing numbered citation repair, or Module 2.8 manuscript-level thinking checkpoint → Zotero canonical metadata + inspected Methods passages and PDF page links → automatic PubMed expansion as a second evidence source when available → combined evidence synthesis and deduplication → reference export standardization by PMID/DOI → metadata QC → Markdown report + RIS unless chat-only/no-export is explicit → final path-only summary
```

Operational checkpoints:

1. **Before searching**: identify scope, language, explicit opt-out, and whether the request is ordinary `search`, `method_parameters`, `target_literature_search`, or the full **Paragraph Citation Package Workflow (Module 2 + Module 2.5)**. If there is no chat-only/no-export opt-out, plan Markdown + RIS output from the start.
2. **Before MCP-dependent work**: apply **0.25 MCP Readiness and Runtime Availability**. Zotero MCP is required for local evidence work; PubMed MCP is optional and can only be used when a PubMed/NCBI-capable callable tool is visible in the active session.
3. **During Zotero work**: search Zotero first, deduplicate candidate evidence, and retrieve inspected metadata before using an item in a report or RIS record.
4. **During PubMed work**: when PubMed tools are visible, use `pubmed_search` for expansion, `pubmed_get_details` or `pubmed_extract_info` for selected PMIDs, `pubmed_find_related` for key-paper expansion, and `pubmed_detect_fulltext` / `pubmed_download_fulltext` only for OA full text when enabled and useful.
5. **Existing numbered citations**: when the user supplies numbered citations or a reference list, preserve `Original citation number` in all audit/report tables; check whether each numbered source supports the mapped claim; mark unsupported numbered citation cases explicitly as `Replace`, `Remove`, or `Verify` rather than silently carrying them into the final RIS.
6. **Before PubMed claims**: only mark PubMed as `Completed` if a PubMed-capable tool is configured and visible, the PubMed search actually ran, and selected PMID metadata was inspected. Otherwise report the query with `⚠️ Tool unavailable; search not executed`, `Failed; query reported`, or `Not executed` with reason.
7. **Before PubMed-only RIS**: include PubMed-only records only when PubMed status is `Completed` and metadata has been inspected with `pubmed_get_details`, `pubmed_extract_info`, or an equivalent visible PubMed metadata tool.
8. **Before writing files**: run metadata quality checks for missing fields, possible Zotero/PubMed mismatch, duplicate warning, and RIS inclusion/exclusion action.
9. **Before final response**: confirm the Markdown report follows `EVIDENCE_REVIEW_REPORT` for paragraph citation packages or `LITERATURE_SEARCH_REPORT` for target literature search exports, the RIS is plain RIS records only, and the chat response lists only generated paths plus critical warnings.

---

## 0. Durable Output Language Policy

Use a Chinese-first durable report by default whenever the user writes in Chinese or does not explicitly request an English-only report. This policy applies to saved Markdown evidence reports and final chat summaries; it does not localize official bibliographic metadata or RIS syntax.

| Output component | Default language / format |
|------------------|---------------------------|
| User-facing report headings, explanations, synthesis, warnings, gap analysis, reviewer-risk notes, metadata QC explanations | Chinese |
| English manuscript paragraphs or manuscript fragments supplied by the user | Preserve English; polish in English unless translation is explicitly requested |
| Chinese manuscript paragraphs | Preserve Chinese; revise in Chinese unless translation is explicitly requested |
| Article titles, journal names, author names, DOI, PMID, Zotero item keys, database names, URLs, and official metadata | Keep official/original form, usually English |
| PubMed execution status values | Keep machine-recognizable values such as `Completed`, `⚠️ Tool unavailable; search not executed`, and `Failed; query reported`, with Chinese explanation nearby when useful |
| EndNote RIS file | Plain standard RIS only; RIS field tags and bibliographic metadata must not be translated or wrapped in Markdown |

Rules:

- The saved `EVIDENCE_REVIEW_REPORT` should be readable as a Chinese research workflow report: Chinese section titles, Chinese analytical prose, Chinese caveats, and Chinese QC notes.
- Do not force English manuscript polishing into Chinese. If the draft paragraph is English, the recommended manuscript text and diff paragraph may remain English while the evidence explanation around it is Chinese.
- Do not translate official paper titles, journal names, author names, DOI, PMID, or RIS fields unless the user explicitly asks for a separate human-readable translation outside the RIS file.
- Never localize RIS tags (`TY`, `AU`, `TI`, `JO`, `DO`, `ER`, etc.) and never add Chinese explanations, Markdown headings, comments, or code fences to the `.ris` file.
- In short: 该用中文报告的部分用中文；该保留英文/官方格式的稿件、文献元数据与 RIS 字段保持英文或原始格式。

---

## 0.25 MCP Readiness and Runtime Availability

Use this readiness gate before any workflow that depends on Zotero or PubMed. The static validator can only inspect this Markdown specification; it does not connect to Zotero, does not execute PubMed, and does not prove that runtime MCP tools are available in the active Agent IDE session.

### Dependency model

| Layer | Requirement | Runtime availability rule |
|-------|-------------|---------------------------|
| Zotero MCP | Required (`metadata.requires: zotero-mcp`) | The active session must expose callable Zotero tools before local library search, metadata inspection, PDF/notes access, or RIS generation from Zotero records. |
| PubMed MCP | Optional (`metadata.optional: pubmed-mcp`) | The active session must expose callable PubMed / NCBI-capable tools before PubMed expansion can be executed or reported as completed. |
| Static validation | Repository-side guardrail only | `scripts/validate-skill.py` checks structure, dependency metadata, templates, and safety text; it does not run a live MCP smoke test. |

### Runtime readiness checklist

1. **Zotero readiness**: confirm Zotero MCP tools are visible before claiming local-library search, semantic search, metadata retrieval, PDF links, annotations, or notes were inspected.
2. **PubMed readiness**: confirm the active session exposes a PubMed-capable callable tool before PubMed expansion. For PancrePal-style servers, expected tools include `pubmed_search`, `pubmed_get_details`, `pubmed_extract_info`, `pubmed_find_related`, `pubmed_detect_fulltext`, `pubmed_download_fulltext`, `pubmed_system_status`, and `pubmed_manage_cache`.
3. **Zotero is not PubMed**: do not treat Zotero MCP as a PubMed search client. Zotero records may contain DOI/PMID links, but live PubMed expansion requires a separate visible PubMed/NCBI-capable tool.
4. **No silent fallback**: if a required tool is unavailable, report the limitation and provide a copyable query or next step. Do not imply that unavailable tools were executed.

### Zotero live connection smoke test

Before any Zotero-dependent workflow, run a lightweight read-only Zotero MCP smoke test. Tool visibility alone is not enough, because a tool can be listed in the active session while the Zotero MCP server is disconnected.

Required first check:

1. `zotero_get_recent` with `limit=3`.

Optional supporting checks:

2. `zotero_list_libraries`.
3. `zotero_get_search_database_status`.

If the first smoke test fails, returns `Not connected`, reports a transport/session error, or returns no callable result:

- stop the Zotero-dependent workflow immediately;
- report `Zotero MCP visible but not connected`;
- do not run semantic search, structured search, metadata inspection, PDF/full-text reading, note/annotation retrieval, duplicate checking, RIS export, or evidence package generation;
- suggest keeping Zotero Desktop open and restarting the active ZCode/MCP session;
- if direct local Zotero HTTP API is known to be reachable, state that the issue is the ZCode ↔ Zotero MCP connection layer, not Zotero Desktop itself.

Do not treat local Zotero HTTP API availability as equivalent to Zotero MCP readiness. This skill depends on callable Zotero MCP tools in the active session.

### Zotero Sequential Execution Guardrail

Treat Zotero discovery and Zotero item inspection as a dependency chain, not a batch job. Do not schedule `zotero_search_items`, `zotero_semantic_search`, or `zotero_advanced_search` in the same tool-call batch as downstream tools that require returned Zotero item keys, including `zotero_get_item_metadata`, `zotero_get_item_children`, `zotero_get_items_children`, `zotero_get_item_fulltext`, `zotero_read_pdf_pages`, `zotero_get_annotations`, `zotero_get_notes`, or RIS generation from Zotero records.

Run one Zotero search step, inspect its result, and only then decide whether the next Zotero step has valid item keys or attachment keys. If `zotero_get_search_database_status`, `zotero_search_items`, `zotero_semantic_search`, `zotero_advanced_search`, or any required upstream Zotero call fails, stop the Zotero inspection chain immediately, report the attempted query/error briefly, and do not schedule dependent metadata, PDF, notes, annotation, collection, full-text, or RIS steps.

If a Zotero search query fails or returns no usable items, revise and retry the query at most once when broadening is appropriate. The retry must be a separate MCP call after inspecting the failed or empty result, not a downstream call pre-scheduled in the same tool-call batch.

### Scheduled Tool Failure Handling

When an MCP result says `Tool skipped because a previous tool call in the scheduled sequence failed`, treat the skipped tool as **not executed**. Do not interpret it as a Zotero/PubMed search miss, zero-hit result, or metadata failure. Identify and report the first failed tool in that scheduled sequence as the root cause; then, if the skipped search or inspection is still needed, rerun that specific upstream tool as a separate MCP call after the failure has been inspected.

Never chain additional Zotero or PubMed dependent calls after a scheduled-sequence failure. First stabilize the upstream search/status call, then continue with one inspected step at a time.

### PubMed status decision tree

Use these status values consistently in reports and final warnings:

| Condition | Required report status | RIS consequence |
|-----------|------------------------|-----------------|
| No PubMed-capable tool is visible in the active session | `⚠️ Tool unavailable; search not executed` | Do not create PubMed-only RIS records. Include the planned PubMed query for manual use. |
| PubMed tool is visible, but workflow is explicit chat-only or non-biomedical and PubMed was intentionally skipped | `Not executed` with reason | Do not create PubMed-only RIS records. |
| PubMed tool is visible, but the search call failed | `Failed; query reported` | Do not create PubMed-only RIS records. Report query/error briefly. |
| PubMed search actually ran and selected PMID metadata was inspected with `pubmed_get_details` or `pubmed_extract_info` | `Completed` | PubMed-only RIS records are allowed only for selected records with sufficient inspected metadata. |

Only actual PubMed execution plus inspected metadata can justify `Completed` or PubMed-only RIS inclusion. Tool visibility alone is not enough.

### PubMed Sequential Execution Guardrail

Treat Zotero local search and PubMed expansion as separate evidence phases. PubMed expansion is a dependency chain, not a batch job: do not schedule `pubmed_search` in the same tool-call batch as downstream tools that require returned PMIDs, including `pubmed_get_details`, `pubmed_extract_info`, `pubmed_find_related`, `pubmed_detect_fulltext`, or `pubmed_download_fulltext`.

Run one PubMed step, inspect its result, and only then decide whether the next PubMed step has valid inputs. If `pubmed_system_status`, `pubmed_search`, or any required upstream PubMed call fails, stop the PubMed chain immediately, mark the PubMed section as `Failed; query reported`, report the attempted query/error briefly, and do not schedule dependent details, related, full-text, export, or PubMed-only RIS steps.

When Zotero local search succeeds but PubMed expansion fails, keep and report the inspected Zotero evidence normally. The PubMed expansion block must remain `Failed; query reported`, and PubMed-only records must not be added to RIS unless PubMed status is `Completed` with inspected metadata.

If a PubMed search returns zero usable PMIDs, revise and retry the query at most once when broadening is appropriate. If no usable PMIDs are returned after that, report zero hits and do not fabricate PMIDs or continue to PubMed metadata inspection.

---

## 0.5 Library Health Check

Use when the user asks for Zotero library status or readiness, including phrases such as "库状态", "健康检查", "preflight", "索引状态", "library status", "health check", or "index status". This mode gives a read-only overview of whether the library is ready for semantic search, evidence review, citation verification, and paragraph analysis.

### Checks

| Check | Zotero MCP tool | What to report |
|-------|-----------------|----------------|
| Semantic index status | `zotero_get_search_database_status` | Indexed item count, full-text index coverage if available, last update time, and whether `zotero_update_search_database` is recommended |
| PDF coverage | `zotero_advanced_search` for total library items and items with attachments/PDFs | Number of items with PDF / total items, percentage, and whether full-text verification may be limited |
| Duplicate items | `zotero_find_duplicates` | Number of duplicate groups and whether manual merge review is recommended |
| Missing abstracts | `zotero_advanced_search` with empty abstract conditions | Number of items without abstracts and whether metadata enrichment is recommended |

### Process

1. Run the four checks above when the user asks for a health check.
2. Keep all actions read-only. Do not update the semantic index, merge duplicates, edit metadata, move items, or add/delete items during the health check.
3. If a check cannot be completed because a tool is unavailable, Zotero is not reachable, or a query is unsupported, mark that row as `⚠️` and explain the limitation. Do not estimate or invent counts for incomplete checks.
4. Recommend fixes, but ask for explicit confirmation before running any repair action such as `zotero_update_search_database`, duplicate merging, metadata editing, or batch tagging.

### Output Format

```markdown
## Zotero Library Health Check

| Check | Status | Result | Suggested action |
|-------|--------|--------|------------------|
| Semantic index | ✅ / ⚠️ / ❌ | Indexed: N items; last update: YYYY-MM-DD | No action / Run incremental update / Consider full rebuild only with confirmation |
| PDF coverage | ✅ / ⚠️ / ❌ | PDFs: N / total (X%) | Add PDFs for key missing items; update full-text index if needed |
| Duplicate items | ✅ / ⚠️ / ❌ | Duplicate groups: N | Review duplicates manually before merging |
| Missing abstracts | ✅ / ⚠️ / ❌ | Missing abstracts: N | Enrich metadata for high-priority items |

### Summary
- Overall readiness: ✅ good / ⚠️ usable with limitations / ❌ needs maintenance
- Safe next step: [one recommended read-only or confirmation-required action]
```

### Safety Rules

- Health check is read-only.
- Never merge duplicates, update tags, rebuild indexes, edit metadata, move collections, or delete items without explicit user confirmation.
- Prefer incremental semantic database updates over force rebuilds.
- If recommending repair actions, separate them from the health report and ask the user which action to run.

---

## Tool Selection

Choose the right Zotero MCP tool for each task:

- **Conceptual literature discovery** → `zotero_semantic_search` first.
- **Exact title, DOI, PMID, author, keyword** → `zotero_search_items` or `zotero_advanced_search`.
- **Method/software parameters and source passages** → **Module 1.2**; read [references/method-parameter-search.md](references/method-parameter-search.md). Search for candidate records, then inspect the selected methods pages; metadata search alone does not establish a parameter value.
- **Citation-key lookup** → `zotero_search_by_citation_key`.
- **Metadata, abstracts, BibTeX/JSON export** → `zotero_get_item_metadata`; required before writing RIS records for Zotero items.
- **Attachments / PDF links** → `zotero_get_item_children` or `zotero_get_items_children` to find attachment keys; use `zotero_get_pdf_outline` and `zotero_read_pdf_pages` to locate and inspect relevant pages.
- **Full text** → `zotero_get_item_fulltext` or `zotero_read_pdf_pages`.
- **Annotations and reading notes** → `zotero_get_annotations` and `zotero_get_notes`.
- **Collection-level search** → `zotero_get_collections`, `zotero_search_collections`, `zotero_get_collection_items`.
- **Semantic database status** → `zotero_get_search_database_status`.
- **Semantic database update** → `zotero_update_search_database`. Only when needed; prefer incremental `update-db`.
- **RIS output** → generate from inspected Zotero metadata and verified PubMed metadata only; never infer missing bibliographic fields from memory.

When PubMed MCP tools are visible, use them as a separate biomedical evidence layer rather than a replacement for Zotero:

- **Broad PubMed expansion** → `pubmed_search` with Boolean terms, MeSH terms, filters, `sort_by`, and `format`; use `format="compact"` for scanning and `format="detailed"` for selected evidence.
- **Canonical PMID metadata** → `pubmed_get_details` for selected PMIDs before citing, deduplicating, or writing RIS records.
- **Targeted metadata extraction** → `pubmed_extract_info` for `basic_info`, `authors`, `abstract_summary`, `keywords`, or `doi_link` when a full record is unnecessary.
- **Citation-chaining / key-paper expansion** → `pubmed_find_related` with `type="similar"` or `type="reviews"` after identifying a key PMID.
- **OA full-text triage** → `pubmed_detect_fulltext` when `FULLTEXT_MODE=enabled` and the workflow needs full text beyond abstracts.
- **OA PDF download** → `pubmed_download_fulltext` only for OA articles, after checking availability; downloaded PDFs are external cache artifacts, not Zotero attachments unless the user later confirms import/attachment actions.
- **PubMed diagnostics** → `pubmed_system_status` and `pubmed_manage_cache` for troubleshooting; do not clear caches without explicit confirmation.
- **EndNote-compatible export** → if a PubMed tool/server directly offers RIS, NBIB, EndNote, BibTeX, or citation export in the active tool list, prefer that exporter for PubMed-only records; otherwise generate RIS from inspected `pubmed_get_details` metadata using the local RIS rules below.

## Safety Rules

Always ask for explicit confirmation before:

- deleting Zotero items, notes, or annotations;
- merging duplicate items;
- batch-updating tags;
- moving many items between collections;
- force-rebuilding the semantic database;
- adding many items at once;
- overwriting notes or annotation comments.

Never fabricate citations, titles, authors, years, journal names, DOI, PMID, Zotero item keys, or RIS records.
If no relevant source is found in Zotero, say so clearly and suggest an external search query instead.

---

## 1. Semantic + Structured Search

### Process

1. If the user asks in natural language, first expand their query into structured search terms.
2. Run **semantic search** first (concept matching, finds conceptually related papers even without keyword overlap).
3. If results are insufficient, fall back to **keyword search** with relevant filters (tags, authors, year range, item type).
4. For biomedical topics, automatically attempt PubMed expansion after the Zotero search when a PubMed-capable MCP tool is visible; inspect selected PMID metadata before citing or exporting PubMed-only records.
5. Unless the user explicitly says chat-only/no-export, write a Search Report + RIS after the chat summary. Ordinary search auto-exports Search Report + RIS; only `只在聊天输出`, `不要生成文件`, `不导出`, or `chat only` keeps the result in chat.
6. Present chat results with the standardized format below while the saved report uses the `LITERATURE_SEARCH_REPORT`-compatible search report structure.

### Auto-Export Default for Ordinary Search

Module 1 ordinary Zotero search default output is **Search Report + RIS**. Treat ordinary topic discovery as a lightweight literature-search export path unless the user explicitly opts out. Use the same output root as target literature search:

```text
zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_literature_search.md
zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_references.ris
```

Rules:

- Ordinary search reports must stay search-focused: include query decomposition, Zotero and PubMed search reproducibility, included records, metadata QC, and export files; do not include Copy-ready Manuscript Text, Annotated Recommended Text, sentence-level citation placement, or paragraph diff.
- Search RIS contains inspected included records only. PubMed-only records require actual completed PubMed search plus inspected PMID metadata.
- If PubMed is unavailable, still write the Zotero-based report/RIS when Zotero evidence was inspected, and record the planned PubMed query with `⚠️ Tool unavailable; search not executed`.
- If Zotero MCP is visible but not connected, stop without search or export and report `Zotero MCP visible but not connected`.

### Query Expansion Examples

| User says | Expanded structured query |
|-----------|--------------------------|
| "气候变化 心血管疾病 风险" | `q: "climate change cardiovascular disease risk", semantic: true, tags: ["cardiovascular"], year: 2020-2026` |
| "孟德尔随机化 药物靶点 2型糖尿病" | `q: "Mendelian randomization drug targets type 2 diabetes", semantic: true, tags: ["MR", "drug targets"], itemType: "journalArticle"` |
| "肠道菌群 抑郁症 机制" | `q: "gut microbiota depression mechanism", semantic: true, year: 2020-2026` |

### Standardized Output Format

Present **all** hits in a single scannable table — one row per paper. Do **not** emit a nested bullet block per paper.

```markdown
| # | Citation (Author Year) | Type | Role | Key | Sim. | Why relevant |
|---|------------------------|------|------|-----|------|--------------|
| 1 | Wang 2022 | semantic | method | Y2FFFQSB | 0.84 | LST/sedentary GWAS; 99 loci |
```

- **Type** = semantic / keyword / tag / collection.
- **Role** = background / mechanism / clinical / method / limitation.
- **Sim.** = similarity score, or "—" for keyword/tag hits.
- **Why relevant** = one short clause, not a sentence list.

Then add a compact **Refs** appendix so full metadata appears exactly once (and only here). Output format: see **Appendix: Output Templates → REFS_BLOCK**.

After the table + Refs, refer to papers only as `Author Year (KEY)` — never re-list title/journal/DOI again.

---

## 1.2 Methodology Parameter Extraction and Report

Use this module when the user asks for a method/software setting, parameter value or default, how a parameter was selected or adjusted, or the original Methods passage that reports it. Use Module 1.8 instead when the request is only to find papers that use a method. Read [references/method-parameter-search.md](references/method-parameter-search.md) before executing this workflow.

This module follows the normal Zotero readiness and dual-MCP sequence, then inspects the selected paper's full text. Separate original-method settings, software defaults, explicit author recommendations, and values chosen by application studies. Report the complete relevant Methods paragraph in the original language, exact section, printed page and physical PDF page when available, a Zotero item link, and a page-specific PDF link. Do not infer parameter values or adjustment effects from abstracts or search snippets.

Unless the user explicitly opts out, use the existing `LITERATURE_SEARCH_REPORT` + Search RIS workflow and include `METHOD_PARAMETER_EVIDENCE` as a dedicated section. Do not add manuscript rewriting sections unless a manuscript paragraph is part of the request.

---

## 1.5 Collection and Tag Search

Use collection or tag filters when:

- the user names a specific research project;
- the user asks for papers from a known Zotero folder or collection;
- the query is broad and the user's library is large;
- the user asks for reviewed, important, included, excluded, or to-read items;
- the user references systematic-review screening status, dissertation chapters, project folders, or reading-list tags.

### Suggested Workflow

1. **Detect structure hints**
   - Treat project names, folder names, collection names, and tag-like labels as possible Zotero structure filters.
   - Common tag hints include `reviewed`, `important`, `included`, `excluded`, `to-read`, `待读`, `已纳入`, `排除`, `重点`, and project-specific tags.
2. **Search collections by name**
   - Use `zotero_search_collections` when the user names a folder/project.
   - If several collections match, show a short numbered list and ask the user to choose.
3. **Retrieve collection items**
   - Use `zotero_get_collection_items` for the selected collection.
   - Use `detail: "summary"` for overview and `detail: "keys_only"` when the collection is large and a follow-up search is needed.
4. **Search within the collection if needed**
   - Use `zotero_search_items` with `collection_key` when keyword/metadata filtering is enough.
   - Use semantic search for conceptual relevance, then intersect or annotate results with collection membership when exact collection-scoped semantic search is unavailable.
5. **Apply tag filters**
   - Use `zotero_search_by_tag` for explicit tag requests.
   - Combine tag filters with query terms when the user asks for status-specific literature, e.g. included studies about an outcome.
6. **Combine relevance with structure**
   - Rank by semantic/keyword relevance, but clearly mark collection and tag membership.
   - Prefer papers inside the named collection/tag when the user explicitly scopes the request.

### Output Notes

- In search result tables, use `Type = collection` or `tag` when the hit is included because of Zotero organization.
- Add collection/tag context in `Why relevant`, e.g. `in PCOS-review collection; tagged included`.
- Do not move items between collections or batch-update tags without explicit user confirmation.

---

## 1.8 Target Literature Search and Export

Use this module when the user wants to discover, screen, classify, or export papers around a topic, method, dataset, phenotype, cohort, disease area, or question, without asking to revise a manuscript paragraph.

Core output is a literature search report, not a paragraph evidence package. Target literature search must not require Copy-ready Manuscript Text, sentence-level citation recommendations, Claim–Evidence Matrix, or a paragraph diff unless the user separately provides a manuscript paragraph.

### Input Decomposition

Before searching, split the user request into these fields:

| Field | Example |
|---|---|
| Topic | brain-related GWAS data |
| Core concept | brain imaging-derived phenotypes; neuroimaging GWAS; cortical thickness; subcortical volume |
| Target relation | which papers use these data / methods / phenotypes |
| Search scope | Zotero local library first; automatic PubMed expansion for biomedical topics when visible |
| Output request | Search Report + RIS by default / chat table only when explicit opt-out |
| Inclusion boundary | uses target data, method, cohort, phenotype, or closely adjacent evidence layer |
| Exclusion boundary | pure disease GWAS, generic GWAS Catalog, or methods papers that do not use the target data |

### Topic Decomposition Rules

For target_literature_search, decompose the request before building queries. Record the decomposition in saved reports so the user can see the search boundary.

| Component | What to extract | Search use |
|---|---|---|
| Target object | The thing the user wants papers about, such as `brain-related GWAS data`, `IL-6 MR`, or `gut microbiota and depression` | Main topic label and semantic search anchor |
| Data / method / phenotype / cohort | Specific data resources, methods, phenotypes, cohorts, exposures, or outcomes | Keyword and exact-phrase search terms |
| Must-have concepts | Concepts that must be present for `Core`, such as brain imaging-derived phenotypes for brain GWAS searches | Inclusion rule and Core classification |
| Adjacent concepts | Related concepts that may be `Strong Related`, such as brain cell eQTL, TWAS, pQTL, or Mendelian randomization | Recall expansion and optional RIS inclusion |
| Exclusion concepts | Common false positives, such as generic GWAS Catalog, disease-only GWAS, methods-only GWAS, animal-only studies, or wrong population | Noise-control queries and exclusion reasons |
| Time / source constraints | Year range, Zotero collection/tag, PubMed expansion, review vs primary studies, language, or study type | Structured filters and reproducibility notes |

Decomposition rules:

- If the user says "哪些文献使用了 X 数据/方法/表型/队列/GWAS", treat `X` as the must-have target relation. A paper is `Core` only when metadata, abstract, notes, or inspected full text indicates it uses that data/method/phenotype/cohort directly.
- If the request is broad, generate 3-6 must-have and adjacent concepts before searching. Do not rely on one generic keyword.
- Preserve user constraints such as collection/tag, year range, study type, species, language, or "Zotero only" in the search plan.
- If no boundary is specified, default to Zotero local library first, automatic PubMed expansion for biomedical topics when visible, Search Report + RIS output, and no year restriction.
- When the user asks for `核心文献`, privilege direct target use and primary source papers over broad reviews or generic methods.
- Record `exclusion concepts` and `time/source constraints` explicitly in `LITERATURE_SEARCH_REPORT` so later reruns can reproduce both inclusion and exclusion boundaries.

### Output Modes

| Mode | Trigger | Output |
|---|---|---|
| Chat Search | Explicit `只在聊天输出`, `不要生成文件`, `不导出`, or `chat only` | Chat table + Refs only |
| Search Report | Explicit report-only request with no RIS/EndNote/literature-list wording | `LITERATURE_SEARCH_REPORT` Markdown file |
| Search Report + RIS | Default for target literature search and ordinary search unless chat-only/no-export is explicit | `LITERATURE_SEARCH_REPORT` Markdown file + Search RIS |

If the user says `导出 MD`, `生成报告`, `保存报告`, `RIS`, `EndNote`, `文献清单`, `literature list`, or equivalent, use Search Report + RIS when RIS/EndNote is mentioned, otherwise Search Report. If the user only asks to search/find papers, still write Search Report + RIS by default; use Chat Search only when the prompt explicitly opts out of files.

### Search Workflow

```text
Zotero readiness smoke test
→ semantic search for broad recall
→ keyword searches for precise concepts
→ candidate pooling
→ deduplicate by DOI / title / Zotero key
→ classify candidates into Core / Strong Related / Method Background / Disease GWAS Only / Noise / Verify
→ inspect Zotero metadata for selected candidates
→ automatic PubMed expansion for biomedical topics when visible
→ generate search report
→ generate Search RIS for selected Included records
```

Workflow rules:

1. Run the Zotero MCP smoke test from **0.25 MCP Readiness and Runtime Availability** before local target literature search. If Zotero MCP is visible but not connected, stop without search or export.
2. Run `zotero_semantic_search` first for broad recall, then one or more separate `zotero_search_items` / `zotero_advanced_search` keyword passes for precise terms when needed. Keep Zotero sequential execution rules: search first, inspect results, then retrieve metadata for selected keys.
3. Pool candidates from semantic, keyword, collection, and tag searches. Deduplicate by DOI first, then PMID, normalized title, then Zotero key.
4. Classify every candidate before export. Do not treat "related" as enough for inclusion; explain the data, method, phenotype, cohort, or topic relation.
5. Retrieve `zotero_get_item_metadata` for every included, optional, or verify candidate before writing it to a report or RIS.
6. PubMed expansion is automatic for target literature search when a PubMed-capable tool is visible and the topic is biomedical or the user requested external expansion. PubMed-only RIS records still require `Completed` PubMed status and inspected PMID metadata.
7. If the target search is chat-only, do not write files. Otherwise, write the default two deliverables: one literature search Markdown report and one Search RIS file. If the user explicitly requests report-only with no RIS/EndNote/literature-list output, omit the RIS line and state why in Export Files.

### Scripted Package Writer (Phase 3 Handoff)

When target literature search candidates have already been searched, classified, and metadata-inspected, the workflow may hand them to the repository writer:

```text
python3 scripts/write_literature_search_package.py --input candidates.json
```

Supported CLI options:

- `--input candidates.json`: input file containing inspected candidate metadata.
- `--output-root zotero-evidence-output`: output root; default package folder is `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/`.
- `--slug brain_gwas`: explicit brief topic slug; otherwise infer from the run topic when possible.
- `--timestamp YYYY-MM-DD_HHMMSS`: deterministic timestamp for reproducible package tests.
- `--include-optional`: include eligible `RIS action = Optional` records in Search RIS.
- `--no-ris`: write only the Markdown literature search report.
- `--dry-run`: validate and print planned paths without writing files.
- `--self-test`: run the local fixture-based writer self-test.

Input contract:

- JSON is required; YAML is accepted only when PyYAML is already installed. Do not add a new dependency just to parse YAML.
- Top-level input keys are `run`, `topic_decomposition`, `query_expansion`, `criteria`, `findings`, `candidates`, `reading_order`, `reproducibility`, and `critical_warnings`.
- The writer does not call Zotero or PubMed; it only formats data supplied by the already executed workflow.
- Candidate `category` values must remain exactly `Core`, `Strong Related`, `Method Background`, `Disease GWAS Only`, `Noise`, or `Verify`.
- Candidate `RIS action` values must remain exactly `Include`, `Optional`, `Exclude`, or `Verify`.
- PubMed-only records require `pubmed_status = Completed` and `metadata_inspected = true` before entering Search RIS.
- RIS default writes only `RIS action = Include`; `--include-optional` is required for eligible optional records.
- The writer never writes `Exclude` or `Verify` records to Search RIS.
- Use `scripts/fixtures/literature_search_package_sample.json` as the minimal local schema example and smoke-test fixture.

### Query Expansion Matrix

Build a small search plan before executing Zotero searches. Use semantic search for recall, then keyword and exact-phrase searches for precision, and finally noise-control terms to explain exclusions.

| Query type | Purpose | Construction rule | Example |
|---|---|---|---|
| Semantic query | Broad recall of conceptually related papers | Combine target object + must-have concepts + adjacent concepts in one natural-language query | `studies using brain-related GWAS data, brain imaging-derived phenotypes, neuroimaging GWAS` |
| Keyword query | Precise retrieval by title/abstract/metadata terms | Use 3-8 short queries from data/method/phenotype/cohort concepts | `"brain imaging-derived phenotypes GWAS"` |
| Exact phrase query | Confirm named resources, cohorts, genes, methods, or phrases | Quote exact terms, dataset names, phenotype labels, DOI/PMID/title fragments, or method names | `"cortical thickness" "GWAS"` |
| Negative / noise-control query | Identify common false positives and exclusion buckets | Search or screen for likely noise terms, then mark why they were excluded rather than silently dropping them | `"GWAS Catalog"`, `"schizophrenia GWAS"` when the target is brain imaging GWAS |

Query expansion examples:

| User question | Semantic query focus | Keyword / exact phrase queries | Noise-control concepts |
|---|---|---|---|
| 哪些文献使用了大脑相关 GWAS 数据？ | brain-related GWAS data; brain imaging-derived phenotypes; neuroimaging GWAS | `"brain imaging-derived phenotypes GWAS"`; `"cortical thickness surface area GWAS"`; `"subcortical brain morphometry GWAS"`; `"basal ganglia GWAS"` | disease-only GWAS; generic GWAS Catalog; methods-only GWAS; psychiatric GWAS without brain imaging |
| 导出关于 IL-6 MR 的文献 MD 和 RIS | IL-6 Mendelian randomization; IL6R; inflammatory biomarkers; causal inference | `"IL-6" "Mendelian randomization"`; `"IL6R" "Mendelian randomization"`; `"interleukin-6 receptor" "MR"` | non-MR observational IL-6 studies; cytokine reviews without MR; unrelated inflammatory markers |
| 检索 Zotero 中关于肠道菌群和抑郁症的文献 | gut microbiota depression mechanism; microbiome depression; gut-brain axis | `"gut microbiota" depression`; `"microbiome" depression`; `"gut-brain axis" depression`; `"Mendelian randomization" microbiota depression` | non-human-only if user asked clinical; unrelated gut disease; depression-only papers without microbiota |

Rules:

- Every saved `LITERATURE_SEARCH_REPORT` must include the generated semantic query and at least one keyword/structured query, or explain why one search mode was not executed.
- Exact phrase queries are especially important for named datasets, cohorts, phenotypes, genes, methods, or abbreviations.
- Do not use negative/noise-control terms to hide results. Use them to make exclusion reasons auditable.
- Retry a failed or zero-hit query at most once by broadening terms; record both the original and revised query in Search Reproducibility.

### Query Expansion Example

For the user question `哪些文献使用了大脑相关 GWAS 数据？`, use a broad semantic query plus precise keyword queries:

```markdown
Semantic query:
studies using brain-related GWAS data, brain imaging-derived phenotypes, neuroimaging GWAS,
cortical thickness, cortical surface area, subcortical brain volumes, basal ganglia GWAS,
MRI-derived brain phenotypes

Keyword queries:
- "brain imaging-derived phenotypes GWAS"
- "neuroimaging GWAS"
- "cortical thickness surface area GWAS"
- "subcortical brain morphometry GWAS"
- "basal ganglia GWAS"
- "brain MRI GWAS Mendelian randomization"
- "brain cell type GWAS eQTL"
```

### Literature Classification

Use these categories in chat tables, `LITERATURE_SEARCH_REPORT`, metadata QC, and Search RIS decisions:

| Category | Definition | Default RIS action |
|---|---|---|
| Core | Directly uses the target data, method, phenotype, cohort, or topic-defining resource, such as brain IDPs GWAS or cortical thickness GWAS | Include |
| Strong Related | Uses adjacent but relevant evidence, such as brain cell eQTL plus GWAS or NIDP TWAS | Include / Optional |
| Method Background | Important method paper, but does not directly use the target topic data | Optional / Exclude |
| Disease GWAS Only | Studies only disease or psychiatric GWAS without the requested brain imaging, brain structure, target phenotype, or method layer | Exclude |
| Noise | False positive or retrieval noise | Exclude |
| Verify | Metadata, abstract, or relation is insufficient; full text or manual check is needed | Verify |

### Classification Decision Rubric

Apply this rubric after metadata or abstract inspection. When evidence is insufficient, choose `Verify` rather than guessing.

| Category | Include evidence | Boundary examples | Tie-breaker |
|---|---|---|---|
| Core | The paper directly uses the target data, method, phenotype, cohort, or resource named in the request | A brain IDP GWAS paper for "brain-related GWAS"; an IL-6 MR paper for "IL-6 MR" | If direct target use is visible in title/abstract/metadata, choose `Core` even if it also has a broad disease outcome |
| Strong Related | The paper uses a nearby data layer or method that helps interpret the target set but is not the exact target | brain cell eQTL + GWAS for brain GWAS; microbiome MR adjacent to gut-brain-axis search | Choose `Strong Related` only when the relation is explicit enough to explain in one clause |
| Method Background | The method is important for understanding the search topic, but the paper does not use the requested target data | general MR method paper in an IL-6 MR search; GWAS method paper without brain phenotype | Include in RIS only if the user asks for background/method papers |
| Disease GWAS Only | The paper studies disease/psychiatric GWAS but lacks the requested data layer, phenotype, or method relation | schizophrenia GWAS without brain imaging for brain IDP search | Exclude unless the user broadens the scope to disease GWAS |
| Noise | The result is off-topic, wrong organism/population, wrong data layer, generic catalog, duplicate, or unrelated retrieval noise | GWAS Catalog entry; unrelated cytokine paper; gut disease without depression/microbiome relation | Exclude and record the concrete reason |
| Verify | Metadata, abstract, or available snippets suggest possible relevance but cannot prove target use | title is vague; missing abstract; no PDF; ambiguous abbreviation | Do not include in Search RIS by default |

Tie-breaker rules:

- Prefer `Verify` over `Core` when target use is only inferred from a vague title.
- Prefer `Method Background` over `Core` when a paper teaches or benchmarks a method but does not apply it to the requested target.
- Prefer `Disease GWAS Only` over `Strong Related` when the only overlap is a disease label and the requested data/method layer is absent.
- Prefer `Noise` over `Verify` when metadata clearly indicates the wrong topic, wrong data layer, duplicate, or generic catalog record.

Include a classification criteria table in saved reports:

```markdown
## 2. 纳入与排除标准
| Decision | Criteria |
|---|---|
| Include | Core; Strong Related when relation is explicit and useful for the user's target set |
| Exclude | Disease GWAS Only, Noise, and Method Background when it does not use the target data/method |
| Verify | Candidate appears relevant but relation or metadata remains unconfirmed |
```

### Noise / Exclusion Reasons

Every excluded or verify candidate in a saved report must carry one short reason code plus a human-readable reason.

| Reason code | Use when | Typical RIS action |
|---|---|---|
| `wrong data layer` | The paper uses a different omics, phenotype, exposure, or measurement layer than requested | Exclude |
| `disease-only GWAS` | The paper is disease/psychiatric GWAS without the requested data/method/phenotype relation | Exclude |
| `method-only` | The paper is methodological background without direct target use | Optional / Exclude |
| `generic catalog` | The result is a catalog/database/index entry rather than a target-use study | Exclude |
| `metadata insufficient` | Metadata/abstract is too sparse to confirm target use | Verify |
| `duplicate` | The candidate duplicates another selected DOI/PMID/title/Zotero record | Exclude |
| `off-topic` | The candidate does not match the topic after metadata inspection | Exclude |
| `wrong population` | The study population/species/context violates the user boundary | Exclude |
| `no inspected metadata` | The candidate was returned by search but metadata was not inspected | Verify / Exclude |

Report excluded candidates in a table, not only in prose:

```markdown
| Citation | Category | Exclusion reason code | Human-readable reason | RIS action |
|----------|----------|-----------------------|-----------------------|------------|
| Author Year | Noise | wrong data layer | Uses disease GWAS only; no brain imaging phenotype | Exclude |
```

### Search RIS Rules

Target literature search uses **Search RIS**, separate from paragraph **Citation RIS**.

- **Citation RIS** is for paragraph citation-support workflows. It contains final recommended manuscript citations, depends on Citation Support Ledger, and excludes sources that do not support the mapped claim.
- **Search RIS** is for target literature search. It represents the selected literature set, not manuscript citation placement.
- In target_literature_search mode, RIS represents the selected literature set, not manuscript citation placement. Do not require Copy-ready Manuscript Text or sentence-level citation recommendations before writing RIS.
- Search RIS includes `Category = Core` by default.
- Search RIS may include `Strong Related` when the report marks the relation and `RIS action = Include` or `Optional`.
- Search RIS excludes `Method Background`, `Disease GWAS Only`, and `Noise` by default.
- `Verify` candidates are excluded from Search RIS unless the user explicitly asks to export unverified candidates; if exported by override, mark them clearly in the Markdown report with `RIS action = Verify`.
- All RIS metadata rules from `RIS_REFERENCE_FILE` still apply: records must use inspected metadata, unresolved metadata mismatch is excluded, and PubMed-only records require completed PubMed metadata inspection.

### Output Requirements

For chat-only target literature search, output a compact table:

```markdown
| # | Citation | Year | Category | Role | Zotero key | DOI/PMID | Why included | RIS action |
|---|----------|------|----------|------|------------|----------|--------------|------------|
| 1 | Author Year | 2024 | Core | brain IDPs GWAS | KEY | DOI / PMID | directly uses target data | Include |
```

Then include `Refs` once, using **Appendix: Output Templates → REFS_BLOCK**.

For saved target literature search outputs, use **Appendix: Output Templates → LITERATURE_SEARCH_REPORT** and this final chat format:

```markdown
Generated Literature Search Package:
- Status: Ready / Caution / Partial / Unknown
- Markdown report: `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_literature_search.md`
- EndNote RIS: `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_references.ris`
- Included records: {N}

Critical Warnings:
- {warning or No critical warnings}
```

If the user requested only a Markdown report and no RIS, omit the EndNote RIS line and state `Included records: {N}` for the report table.

## 1.9 Recall-first candidate retrieval

Use this module for paragraph citation work whenever the user expects broad coverage, says “不要遗漏/尽量全面/系统找全”, or when a claim has several plausible evidence families. The goal is high recall within a declared scope; no database search can prove that the literature is literally complete.

Read [references/recall-first-retrieval.md](references/recall-first-retrieval.md) before searching. For each claim, decompose the population/object, exposure/method, outcome/process, design/evidence type, context/tissue, synonyms and exclusions. Then run independent retrieval lanes:

```text
Zotero semantic (`zotero_semantic`) → Zotero structured/keyword (`zotero_structured`)
→ PubMed broad MeSH + title/abstract (`pubmed_broad`)
→ PubMed design/method query (`pubmed_design_or_method`)
→ PubMed related expansion (`pubmed_related`) for one or two strong anchors
→ DOI/PMID/title deduplication → directness/quality/full-text screening
```

Do not stop after the first supporting paper. Record every lane's query, raw hit count, unique IDs, inspected records, newly discovered direct-support candidates and tool status. Run at least one semantic and one structured Zotero lane; when PubMed is available, run at least two independent PubMed query families. Stop only after two consecutive query rounds add no new direct-support candidate and no new concept block, or when the declared scope/time limit is reached. The saved report must include `Recall Audit`, `recall_status`, `coverage_gaps`, and a reason for stopping. If PubMed is unavailable or fails, the status is `partial`/`blocked`, never `saturated`.

### Precision gate for “准确又好” citation matching

High recall creates candidates; it does not decide what belongs in the manuscript. After retrieval, apply this precision gate separately to every sentence and claim:

1. **Preserve meaning before searching**: keep the sentence's population/object, exposure or method, outcome/process, direction, study design, tissue/context, time frame, and uncertainty. Expand abbreviations and synonyms for retrieval, but never broaden the manuscript claim silently.
2. **Use independent query families**: build one Zotero semantic query, one short Zotero structured query, one PubMed broad MeSH/title-abstract query, and one PubMed design/method or population query when PubMed is available. Do not make one over-constrained query the only route.
3. **Rank by claim fit**: directness to the exact claim > population/context match > design/evidence match > inspected full text or abstract > metadata confidence > recency. Semantic similarity, journal prestige, citation count, and recency alone cannot justify inclusion.
4. **Inspect before recommending**: a search hit or abstract snippet is a discovery lead. A recommended citation must have inspected Zotero metadata/abstract/full text or inspected PubMed details/abstract, an evidence location, a support verdict, and a sentence/claim mapping.
5. **Select narrowly**: recommend the smallest set of high-value citations that directly supports the sentence. Use `Include` for direct support, `Optional` for explicit background/bridge context, and `Verify` or `Exclude` for partial, contradictory, unaddressed, or uninspected records. Never cite a review as if it directly tested an empirical claim when the primary study is available.
6. **Calibrate the wording**: A/B evidence can support moderately confident association wording; C requires plausibility or context wording; D must remain current-study wording; E must be removed, verified, or strongly hedged. If no paper supports the sentence as written, report the gap and propose a narrower sentence instead of forcing a citation.
7. **Check sentence coverage**: every sentence receives a `sentence_id`, `citation_need`, and author check in `SENTENCE_CITATION_MATRIX`; every included RIS record maps back to at least one sentence and claim. A package is not `Ready` if the citation-required coverage is incomplete.

The default direct-paragraph request therefore needs only the paragraph. Section, target journal, date range, and preferred number of citations are optional refinements; do not block the first pass on their absence. If a missing scope constraint would materially change the evidence set, state the assumption in the report and ask one focused follow-up after returning the initial evidence map.

The candidate pool and final support set are separate. Keep near misses and excluded records in the Markdown audit with reasons, but put only `Include`/`Optional` records that pass canonicalization and claim-level support into Citation RIS. Preserve `retrieved_by: Zotero | PubMed | Zotero + PubMed` after deduplication so the report shows where a citation came from.

An empty Zotero result is a local-library result, not a literature-completeness result: continue to the PubMed lanes when PubMed is available. If Zotero MCP is disconnected, report the local lane as unavailable and keep any independently completed PubMed evidence clearly labeled; the package status is at least `Partial` when the user's requested scope required both sources.

### Expected-citation rescue path

When the user supplies an author–year citation, DOI, PMID, title fragment, or an expected paper that
was not retrieved, read [references/retrieval-rescue-protocol.md](references/retrieval-rescue-protocol.md)
before broadening the topic. Classify the first failure as `tool_unavailable`, `query_error`,
`zero_hits`, `metadata_unusable`, or `support_gap`. Use the identifier-first ladder (DOI → PMID →
Zotero key → exact title → normalized title → author/year plus distinctive title tokens), then relax
one claim dimension at a time while retaining the population/object and outcome anchors. A gene-only,
method-only, or author-only fallback is a discovery lead and must not enter the evidence set without
restoring the original anchors. Add `failure_class`, `rescue_ladder_used`, `anchors_preserved`,
`rescue_status`, and `manual_next_query` to the Recall Audit. `no_direct_match` means completed
retrieval and inspection found no direct support; it is different from `blocked`, where a tool or
access boundary prevented completion.

---

## 2. Paragraph Evidence & Citation Analysis

Use when the user pastes a manuscript paragraph, draft passage, or multi-sentence text and asks for evidence, citation support, writing suggestions, or citation insertion. This module replaces the former separate evidence-chain and writing-suggestion modes.

### Core Principle

Run **one Zotero search pass** for the paragraph, then produce the evidence layers from the same result set. The author-facing handoff follows [references/report-layout.md](references/report-layout.md):

1. **Copy-ready Manuscript Text** — polish the paragraph and place eligible author–year citations at sentence/clause anchors.
2. **Claim–Evidence Matrix immediately after the copy-ready text** — map each revised sentence/clause to its claim, add the Chinese `主张摘要（中文）`, and assign exactly one A–E evidence level, source layer, support verdict, insertion anchor, and manual action.
3. **Citation Insertion Sheet** — convert the matrix into a searchable, checkable insertion list. Keep `SENTENCE_CITATION_MATRIX`, `Citation Support Ledger`, and bibliographic metadata in the audit appendix so the author does not need to reconcile duplicate front-of-report decisions.

Internally, claims are still extracted and evaluated before wording is finalized; the output order is intentionally optimized for the author's manual workflow.

### Source Layer: Current-study Finding vs External Evidence

Assign every extracted claim exactly one `Source layer` before interpreting evidence. This boundary prevents the workflow from using external literature to incorrectly "prove" the user's current-study findings.

| Source layer | Definition | Required wording pattern |
|--------------|------------|--------------------------|
| `Current study` | A result, observation, statistic, model output, table/figure result, or interpretation supplied by the user or produced in the current manuscript/analysis. | `In our analysis...`, `The present study identified...`, `Our findings suggest...`, `本研究发现...` |
| `Zotero external evidence` | Evidence from inspected Zotero library records, including metadata, abstracts, notes, annotations, or full text. | `Previous studies show...`, `Published evidence supports...`, `Zotero-indexed literature reports...` |
| `PubMed external evidence` | Evidence from PubMed expansion records after a completed PubMed search and inspected PMID metadata. | `PubMed-indexed studies report...`, `Published evidence from PubMed supports...` |
| `Interpretive bridge` | A cautious inference connecting current-study findings to external evidence, mechanism, or plausibility. | `These findings are consistent with...`, `may suggest...`, `provide biological plausibility for...` |
| `Unsupported gap` | A claim for which no adequate direct, indirect, mechanistic, or verified evidence was retrieved. | `requires validation`, `was not directly supported by retrieved evidence`, `needs verification` |

Claims that must normally be marked `Current study` unless the user explicitly states they are from an external cited source:

- SMR, MR, TWAS, GWAS, colocalization, fine-mapping, LDSC, MAGMA, PRS, genetic correlation, QTL or eQTL/pQTL integration;
- pathway enrichment, gene-set enrichment, cell-type enrichment, cell enrichment, tissue enrichment, network analysis, module detection;
- candidate gene prioritization, drug-target prioritization, target ranking, causal-gene nomination;
- differential expression, single-cell analysis, spatial transcriptomics, omics integration, mediation analysis;
- cohort, clinical, statistical-model, sensitivity-analysis, subgroup-analysis, or figure/table results supplied by the user;
- manuscript wording such as `we found`, `our analysis identified`, `the present study shows`, `本研究发现`, `我们的结果提示`, or equivalent.

External literature can support background, prior association, method, mechanism, or biological plausibility. It must not be described as proving, confirming, validating, or replicating a current-study finding unless the retrieved external source directly tests the same claim with a comparable design, exposure, outcome, population, and direction.

Required interpretation rules:

- If a claim is `Current study`, assign evidence level `D` unless an inspected comparable external replication supports the same finding.
- If external evidence only provides mechanism or background for a current-study claim, use `Interpretive bridge` wording and evidence level `C` or `D`, not `A`.
- If no direct or plausible evidence is found, mark `Source layer = Unsupported gap` and evidence level `E`.
- The Claim–Evidence Matrix must include both `Source layer` and `Evidence level` so readers can see whether a statement is current-study output, external evidence, a bridge inference, or a gap.

Recommended wording:

- Current study: `In our analysis...`, `The present study identified...`, `Our findings suggest...`.
- External evidence: `Previous studies show...`, `Published evidence supports...`, `Prior literature reports...`.
- Interpretive bridge: `These findings are consistent with...`, `may suggest...`, `provide biological plausibility for...`.
- Unsupported gap: `requires validation`, `was not directly supported by retrieved evidence`, `should be verified before use`.

Forbidden wording unless directly supported by comparable external evidence:

- `Previous studies confirmed our SMR/TWAS/MR result`.
- `Published literature proves our candidate gene prioritization`.
- `External evidence validates our enrichment result`.
- `This citation demonstrates that our current-study association is causal`.
- `The retrieved papers confirm the current study's BMI-independent or pleiotropy result`.

### Unified Evidence Level

Assign every extracted claim exactly one evidence level from `A` to `E`. Use the same level in chat output, Markdown evidence reports, reviewer-risk assessment, and manuscript wording recommendations so evidence strength does not drift across reports.

| Level | Name | Definition | Judgment criteria | Recommended wording | Avoid |
|-------|------|------------|-------------------|---------------------|-------|
| `A` | Exact direct support | External literature directly supports the exact claim. | The retrieved source matches the claim's exposure/intervention, outcome, direction, population/context, and study-design implication closely enough to support the sentence as written. | `supported`, `directly supported`, `reported`, `shown to be associated with` when the source design supports that wording | Adding causal, population, subgroup, or independence claims not present in the source |
| `B` | Close direct support | External literature directly supports a closely related claim, but not the exact manuscript claim. | At least one key element differs, such as phenotype, population, exposure definition, mechanism detail, time scale, or study design. | `consistent with`, `supports a related claim`, `aligns with evidence that...` | `proves`, `confirms`, or wording that treats the related source as exact support |
| `C` | Plausibility support | Evidence is mechanistic, background, review-based, pathway-level, methodological, or otherwise indirect. | The source supports biological plausibility, context, mechanism, terminology, or method, but does not directly test the full claim. | `biologically plausible`, `may align with`, `may contribute to`, `provides mechanistic context` | Treating mechanism or background as direct empirical support |
| `D` | Current-study only | The claim is primarily a finding from the user's current study; external literature can only provide context or plausibility unless direct replication is retrieved. | The claim comes from the user's data, analysis, tables, figures, or wording such as `our analysis`, `we found`, `本研究发现`, or `the present study identified`. | `in our analysis`, `our findings suggest`, `the present study identified`, `consistent with prior evidence` | `previous studies confirmed our finding` unless a comparable external replication was inspected |
| `E` | Unsupported / contradicted / verify | The claim is unsupported, contradicted, unverifiable with available sources, or requires citation/metadata verification. | No adequate evidence was found; retrieved evidence conflicts with the claim; or a key citation, concept, DOI/PMID, title, or metadata field remains unverified. | `remove`, `verify`, `hedge strongly`, `requires validation`, `not directly supported by retrieved evidence` | Presenting the claim as established fact |

Evidence-level rules:

- `D` explicitly means `current-study only`. Do not use external mechanistic or background literature as direct proof of the user's own SMR, MR, TWAS, GWAS, enrichment, candidate-gene, cohort, or statistical finding.
- `C` cannot be upgraded to `A` or `B` unless direct empirical evidence for the same claim is retrieved and inspected.
- `E` claims must not appear in manuscript-ready text as confident factual statements; remove, verify, convert to a knowledge gap, or hedge strongly.
- Recommended Manuscript Text must follow the level: A/B can use moderate confidence, C/D require cautious or bridge wording, and E requires removal, verification, or strong hedging.
- Every matrix, sentence matrix, placement table, ledger, and reviewer-risk row must contain exactly one level: `A`, `B`, `C`, `D`, or `E`. Never write compound labels such as `A/B`, `A/C`, or `C/D`. If a sentence contains multiple claims with different levels, split the claim rows; if a single sentence must remain intact, use the most conservative level and explain the split in `Manual action`.

Do not repeatedly search Zotero for each output layer. Do not ask the user to choose between "find evidence" and "add citations" modes.

When the request is a citation-support or export request, this module is the analysis stage of the **Paragraph Citation Package Workflow (Module 2 + Module 2.5)**. In that full workflow, the agent must continue to Module 2.5 after the Zotero local search and paragraph analysis; PubMed expansion is attempted automatically after Zotero local search when a PubMed-capable tool is configured and visible. Chat-only use of Module 2 requires an explicit opt-out such as `不要生成文件` or `只在聊天输出`.

### Process

1. **Sentence splitting + claim extraction**
   - Split the paragraph into sentences.
   - Extract 1-2 core factual/conceptual claims per sentence.
   - Preserve sentence order so claim IDs can be mapped back to citation placement.
2. **Batch query construction + one search pass**
   - Combine all claims into a compact batch of search queries.
   - Run `zotero_semantic_search` first for conceptual matching.
   - If coverage is insufficient, run one keyword/structured fallback with `zotero_search_items` or `zotero_advanced_search` using the same claim set.
   - Deduplicate results and build one reusable candidate evidence pool.
   - If an expected citation is missing, execute the retrieval rescue ladder before changing the topic;
     keep rescue candidates separate from the direct-support set until metadata and claim support are inspected.
3. **Two-layer analysis from the same evidence pool**
   - **Layer A: Claim-evidence matrix** — map each claim to the best available citation(s), add a concise Chinese `主张摘要（中文）`, assign exactly one source layer and one A-E evidence level, record support strength, and mark gap status.
   - **Layer B: Sentence-level citation recommendations** — map each sentence to the citation(s) that should be inserted, carry forward the same source layer and A-E evidence level, and explain why.
   - **Layer C: Evidence-backed manuscript polishing** — after Layer A/B, revise grammar, field-native phrasing, argument flow, and claim strength while preserving the original meaning and evidence boundary. This layer is mandatory for English paragraph citation packages unless the user explicitly opts out.
   - **Author-facing handoff order** — write the polished `Copy-ready Manuscript Text` first, then place the revised-sentence `Claim–Evidence Matrix` immediately after it. The matrix must use the fixed columns in `references/report-layout.md`; this is a presentation order and does not change the internal requirement to evaluate claims before final wording.
   - **Citation Insertion Sheet** — after the matrix, record every eligible citation placement with the exact insertion anchor, copy-ready citation string, search tokens, canonical record, PMID/DOI, evidence role, support verdict, and RIS action. The sheet is the operational handoff for Word, Zotero, EndNote, and manual insertion.
   - **SENTENCE_CITATION_MATRIX** — create one stable row for every input sentence, even when the sentence is a current-study result, common knowledge, an interpretive bridge, or an unsupported gap. Place it in the Audit Appendix; it must not introduce a different citation decision from the front-of-report matrix. Each row must be traceable through `sentence_id → claim_id → citation → RIS action`.
   - **CITATION_COVERAGE_SUMMARY** — report sentence counts, citation-required coverage, unsupported sentences, and any citation candidate that cannot be traced to a matrix row or Citation Support Ledger row.
   - Do not use a different strength label or source boundary in Layer B than the level assigned in Layer A. If sentence-level wording combines multiple claims, use the most conservative evidence level and explicitly separate current-study wording from external-evidence wording.
   - Use the exact `citation_need` values `citation_required`, `citation_optional`, `current_study`, `common_knowledge`, `interpretive_bridge`, or `unsupported`. A sentence may be marked `current_study` without an external citation, but it must still receive a matrix row and an author check.
   - A citation is sentence-level coverage only when the cited record is linked to the sentence's `claim_ids`, has an inspected evidence route, and has a non-blocked `RIS action`. Do not count a search hit, an uninspected record, or a citation attached elsewhere in the paragraph as coverage.
   - Never use one citation to imply support for every sentence in a paragraph. If a citation supports only one clause, split the sentence or map the citation only to that sentence/claim.
4. **Diff paragraph**
   - Provide a revised paragraph showing citation insertions and necessary wording changes.
   - Mark deletions with `~~strikethrough~~` and additions with `**bold**`.
   - Keep unchanged text unmarked so the user can see exactly what changed.
   - Add a separate Citation Insertion Sheet with stable `sentence_id`, insertion anchor, copy-ready citation, search tokens, canonical record, PMID/DOI, evidence role, support verdict, and RIS action. Do not repeat the full evidence explanation there.
   - Add a Diff / Change Log covering grammar/clarity, field-native phrasing, argument flow, evidence calibration, terminology alignment, and citation placement.
   - End with a change summary in this format: `改动：+N词/-M词，修改原因：[简短说明]`.
5. **Gap summary + package/external handoff**
   - Summarize claims with no adequate Zotero evidence.
   - For chat-only Module 2 output, propose external search queries for each gap and ask whether to start external search using **External Source Fallback**.
   - For the full **Paragraph Citation Package Workflow**, do not stop at the gap prompt: continue to Module 2.5, where automatic PubMed expansion is attempted after Zotero local search when a PubMed-capable tool is configured and visible.
   - If no PubMed-capable tool is available in package mode, include the copyable PubMed query and status `⚠️ Tool unavailable; search not executed` in the Markdown report instead of implying PubMed was searched.

### Evidence and Rationale Labels

Use the unified evidence level above as the primary strength label for every claim. The labels below describe the evidence type or citation role and should be used alongside the A-E level inside the tables, especially in the "Strength", "Evidence level", and "Citation rationale" columns:

- **Direct evidence**: directly supports the claim.
- **Indirect evidence**: supports part of the mechanism, context, or related association.
- **Mechanistic evidence**: explains a biological, behavioral, theoretical, or methodological mechanism.
- **Methodological evidence**: supports the design, measurement, or analytical method.
- **Background/context**: useful for introduction, framing, or terminology.
- **Contrasting evidence**: reports inconsistent or opposite findings; use to hedge or qualify wording.
- **Replace citation**: a library source is more recent, more specific, or better aligned than an existing citation.
- **Terminology alignment**: Zotero sources consistently use a different term or construct.
- **Gap**: no adequate Zotero evidence found.

The former writing-suggestion categories are not shown as a standalone section; fold citation rationale into the sentence-level table, while keeping the actual evidence-backed rewrite visible in Copy-ready Manuscript Text and the Diff / Change Log.

### Output Format

Always use this **table-first, no-repetition** layout. Full metadata appears once in the `Refs` block; everywhere else cite sources as `Author Year (KEY)`.

Use this structure:

```markdown
## 段落分析：<主题短语>

### 可直接使用的稿件文本（Copy-ready Manuscript Text）
{polished manuscript text with eligible author–year citations}

### 紧随正文的主张—证据矩阵（Claim–Evidence Matrix）
{one row per revised sentence/clause; include sentence_id, claim_id, citation, evidence level, source layer, support verdict, and insertion_anchor}

### Citation Insertion Sheet
{operational rows for search_tokens and manual insertion}

### 注释版推荐文本（Annotated Recommended Text）
{evidence boundary, writing rationale, and reviewer risk}

### Diff / Change Log
{original-to-revised wording changes and citation effects}

### SENTENCE_CITATION_MATRIX / Citation Support Ledger / Refs
{traceability, metadata, and export records}

### Gap 与外部搜索
- ⚠️ 主张2 无库内证据 → 建议查询：`"Z causes W" mechanism`
- 是否启动外部搜索？(y/n)
```

### Gap Handling

When any row in the Layer A claim-evidence matrix has `Gap? = ⚠️ 是`, handle the gap according to workflow mode.

- **Full Paragraph Citation Package Workflow**: continue to Module 2.5 automatically. PubMed expansion is the built-in biomedical expansion step after Zotero local search when a PubMed-capable tool is configured and visible; if unavailable, report the query and `⚠️ Tool unavailable; search not executed`.
- **Chat-only Module 2**: enter the interactive gap-handling flow below after presenting the paragraph analysis. Do not run external searches unless the user confirms.

Interactive chat-only flow:

1. **Count gap claims**
   - Report the number of unsupported or insufficiently supported claims.
   - Preserve claim IDs from Layer A so the user can trace each gap back to the paragraph.
2. **Construct bilingual external queries**
   - For each gap, generate an English `query` and a Chinese `query_zh` when the paragraph or user request is Chinese.
   - Prefer standard biomedical terminology and MeSH terms when applicable.
   - Keep queries specific enough to retrieve direct evidence, e.g. exposure/intervention + outcome + mechanism/study type.
3. **Ask before external search**
   - Show a compact gap summary and ask: `发现 N 处证据缺口，是否启动外部文献搜索？(y/n)`
   - If the user says yes, follow **External Source Fallback**.
   - Use external MCP tools such as Crossref/OpenAlex/Semantic Scholar or paper-search/PubMed only when those tools are configured and visible in the current environment. If they are unavailable, provide ready-to-copy external search queries instead of implying that the search was executed.
4. **Return top external candidates**
   - For each gap, return up to top-3 external results.
   - Mark every result as external and include source, title, authors, year, DOI/URL, and why it may fill the gap.
   - Do not treat external results as library evidence until added to Zotero and inspected.
5. **Ask before adding to Zotero**
   - After external results are shown, ask whether to add selected items to Zotero using `zotero_add_by_doi` or `zotero_add_by_url`.
   - Adding items requires explicit user confirmation.
   - Support collection placement in the confirmation prompt:
     - **指定分类**: ask the user for the target collection name/key, then pass it via the `collections` parameter.
     - **当前分类**: if the current working context includes a collection key, offer to add to that collection automatically; confirm the collection name/key before adding.
     - **未指定分类**: add to the main library only after confirmation.

Use this output shape:

```markdown
### Gap Handling
- 发现 2 处证据缺口。

| Gap claim | query | query_zh | Suggested external source |
|-----------|-------|----------|---------------------------|
| #2 Z导致W | `Z causes W mechanism MeSH_term` | `Z 导致 W 机制` | PubMed / Semantic Scholar |

是否启动外部文献搜索？(y/n)

<!-- If yes, after external search: -->
### External candidates
| Gap | External result | Source | DOI/URL | Why relevant |
|-----|-----------------|--------|---------|--------------|
| #2 | Author 2024 | PubMed | 10.xxxx/xxxx | Directly tests Z→W |

是否将以上结果添加到 Zotero？请选择：
1. 添加到当前分类：<collection name/key>
2. 添加到指定分类（请提供分类名/key）
3. 只添加到主库
4. 不添加
```

### Rules

- Keep the paragraph's original language unless the user asks for translation.
- Prefer 3-7 high-value citations over exhaustive citation stuffing.
- If evidence is indirect, mixed, observational, or mechanistic only, assign evidence level C unless a more specific rule requires D or E, and recommend hedging language rather than causal wording.
- Carry evidence levels into writing suggestions: A/B may support moderately confident citation placement, C/D require bridge or hedge wording, and E should be removed, verified, or reframed as a gap.
- Separate current-study findings from external evidence in manuscript wording: write current results as `In our analysis...` or `The present study identified...`, then use external citations only as `Previous studies show...` or `These findings are consistent with...` bridge support.
- Use the same Zotero result pool for both Layer A and Layer B; only search again if the user explicitly requests deeper follow-up.
- Do not fabricate missing support. Mark gaps clearly. In chat-only mode, hand off to external search only after asking; in the full Paragraph Citation Package Workflow, continue to Module 2.5 and report PubMed expansion status honestly.

### Sentence coverage contract

In addition to the claim matrix and citation ledger, create a visible `SENTENCE_CITATION_MATRIX` for every paragraph package. This is the sentence-level source of truth for deciding whether each sentence needs a citation and whether the proposed citation is eligible for RIS export.

- Use the exact `citation_need` values `citation_required`, `citation_optional`, `current_study`, `common_knowledge`, `interpretive_bridge`, or `unsupported`.
- Create exactly one stable row per input sentence (`S01`, `S02`, …), preserve sentence order, and link each row to one or more `claim_ids`.
- A `citation_required` sentence must have an eligible inspected citation or an explicit unsupported/verify decision. Search hits, uninspected records, and citations attached to another sentence do not count as coverage.
- Carry `source_layer`, `evidence_level`, `support_verdict`, and `RIS action` from the mapped claim and Citation Support Ledger; do not invent a stronger sentence-level label.
- `current_study`, `common_knowledge`, and `citation_optional` may use `—` for recommended citations, but still require an author check. Current-study sentences must remain framed as results of the present study.
- Never use one paper to imply support for every sentence in a paragraph. If a paper supports only one clause, split the sentence or map the record only to the supported sentence/claim.
- Add `CITATION_COVERAGE_SUMMARY` with total sentences, citation-required sentences, covered sentences, unsupported/verify sentences, unmapped claims, orphan RIS candidates, and an overall status of `complete`, `partial`, `blocked`, or `not_applicable`.
- Do not mark the package `Ready` when a citation-required sentence is unmapped, when an eligible citation has no sentence/claim trace, or when required metadata remains uninspected.

## 2.2 Existing Numbered Citation Repair

Use when the user provides a manuscript paragraph or section with existing numbered citations plus a reference list, or when they say a citation number does not support the claim, e.g. `6不支持`, `citation 6 does not support`, `检查参考文献`, `更新参考文献`, `编号引用`, `replace citation`, `refresh RIS`, or `regenerate RIS`. This module is a focused reference-update workflow: it checks whether supplied numbered references support the exact mapped claims, improves manuscript wording, and prepares clean Markdown/RIS export decisions.

### Core Principle

Do not treat a supplied citation number as valid merely because it appears in the draft. Map `citation number → supplied reference metadata → claim`, inspect the source through Zotero/PubMed/metadata tools when available, and assign a concrete action: `Keep`, `Replace`, `Remove`, `Verify`, or `Add supporting citation`.

### Process

1. **Parse numbered citations and references**
   - Extract in-text numbered citations such as `6`, `6,18`, `[6,18]`, superscript-like digits, and ranges when present.
   - Extract the supplied numbered reference list and preserve each `Original citation number` exactly as the user provided it.
   - Normalize citation numbers only for matching; do not silently renumber the user's manuscript text.
2. **Map citations to claims**
   - Split the manuscript text into sentences and claims as in Module 2.
   - For every cited sentence, record `citation number → supplied reference metadata → claim` and carry it into `Claim supported by this number` in the repair table.
   - If one citation group supports different parts of a sentence, split the sentence or clause so each citation is judged against the specific claim it is meant to support.
3. **Handle explicit unsupported-number reports**
   - When the user says a specific marker is unsupported, such as `6不支持`, `#6 unsupported`, or `citation 6 does not support`, first locate every sentence or clause carrying that exact marker.
   - Parse the supplied reference for that original number before searching for replacements; do not assume the number points to the correct paper.
   - Inspect metadata, abstract, notes, annotations, or full text when available, and decide whether the paper supports the exact mapped claim rather than only a related topic.
   - Produce an explicit verdict row for that number even if no replacement is found.
   - If the number belongs to a citation group such as `6,18`, judge each number separately and state which part of the claim, if any, each source supports.
4. **Check support and choose an action**
   - Retrieve Zotero metadata for each supplied reference when possible by title, DOI, PMID, author/year, or citation key.
   - Use PubMed metadata as an external standardization layer only when PubMed tools are visible and actually executed.
   - Judge each supplied numbered citation as `Supported claim? = yes / partial / no / unverified / contradictory`.
   - Map those labels to verification verdicts when reporting: `yes = fully supported`, `partial = partially supported`, `no = not addressed for this claim`, `unverified = not inspected or metadata unresolved`, and `contradictory = contradicted`.
   - Mark unsupported numbered citation rows explicitly as `Replace`, `Remove`, or `Verify`; do not carry unsupported references into RIS by default.
   - Mark background-only sources as `partial` when they support context but not the exact directional, causal, BMI-independent, or horizontal-pleiotropy claim.
5. **Find replacements only when needed**
   - If a supplied citation is `partial`, `no`, `unverified`, or `contradictory`, search Zotero first for a better source.
   - If package mode is active and PubMed tools are visible, run PubMed expansion after Zotero search to identify replacement candidates.
   - Record `Replacement candidate` and `Replacement reason`; if no replacement is found, recommend wording changes or removal.
   - For `6 = Wang et al. 2022 Nat Genet physical activity/sedentary behavior GWAS`, treat the paper as background for sedentary-behavior GWAS unless inspection shows direct PCOS evidence. If it is mapped to `LST directionally contributes to PCOS susceptibility`, normally mark `Supported claim? = partial / no`, search for a more direct PCOS-sedentary, MR, or reproductive-health genetics source, and set the original `RIS action = Exclude / Optional` depending on whether the revised text keeps it as background.
6. **Repair the manuscript wording**
   - Preserve the manuscript language.
   - Avoid awkward, weak, or overconfident openings such as `Several genetic observations were consistent with...` when the evidence is mainly current-study genetic analyses.
   - Treat weak openings, overconfident framing, and current-study findings presented as external evidence as explicit writing issues; include them in the annotated text table and in `Claims to Revise or Remove`.
   - Prefer clearer current-study framing such as `Our genetic analyses provided convergent but not definitive evidence that longer leisure screen time may contribute to PCOS susceptibility.`, `Together, these analyses suggest a putative directional relationship between sedentary behavior and PCOS risk, while remaining compatible with residual pleiotropy and phenotype heterogeneity.`, `Together, these genetic analyses suggest...`, or `In our analysis, ...`, followed by external evidence only as background, method, or interpretive bridge.
   - For MR, LST, PCOS, BMI-independent, horizontal pleiotropy, winner's curse, sample overlap, phenotype heterogeneity, ancestry-specific effects, and related causal or directional wording, require hedge wording unless a directly inspected source supports the stronger claim.
7. **Export decisions**
   - Preserve `Original citation number` in the Markdown audit tables, and explicitly state `Original citation number preserved for audit` plus `Final numbering handled by EndNote/Word` in the numbering notes or table rows.
   - The final RIS represents the recommended final included references, not necessarily the original numbering. EndNote/Word will renumber citations according to the imported RIS and citation style.
   - `RIS action` must be one of `Include`, `Exclude`, `Verify`, or `Optional`. Unsupported or unresolved references should be `Exclude` or `Verify`, not `Include`, unless the user explicitly requests retention.
   - Include a replaced or partially supported original numbered citation in RIS only if the revised manuscript text still uses it as background/context and the report marks that limited role clearly.
   - If supplied numbered citations are present, their `Original citation number`, mapped claim, `Support verdict`, action, and `RIS action` must propagate into the Citation Support Ledger so the final citation chain remains auditable from the user's original numbering to the recommended RIS decision.

### Output Format

Use this table in chat and in the Markdown evidence report whenever supplied numbered references are inspected:

```markdown
### Existing Numbered Citation Repair
| Original citation number | Supplied reference | Claim supported by this number | Support verdict | Verification verdict | Evidence level | Action: Keep / Replace / Remove / Verify / Add supporting citation | Replacement candidate | Original citation number preserved for audit | Final numbering handled by EndNote/Word | RIS action | Reason |
|--------------------------|--------------------|--------------------------------|-----------------|----------------------|----------------|--------------------------------------------------------------------|-----------------------|----------------------------------------|----------------------------------------|------------|--------|
| 6 | Wang 2022 Nat Genet sedentary-behavior GWAS | sedentary behavior contributes directionally to PCOS susceptibility | partial / no | partially supported / not addressed for this claim | E | Replace / reframe as background | Shao 2026 / other direct PCOS-sedentary or MR reproductive-health genetics source | yes | yes | Exclude / Optional | Supports sedentary-behavior GWAS/background, not the specific PCOS directional claim unless text is reframed |
```

Rules:
- `Support verdict` must use `yes / partial / no / unverified / contradictory` and must map to the human-readable `Verification verdict`.
- `Original citation number preserved for audit = yes` records the user's original numbering for traceability only; `Final numbering handled by EndNote/Word = yes` warns that imported RIS records will be renumbered by the citation processor.
- `Supplied reference` should be concise, e.g. `Wang 2022`, with full metadata appearing only in the reference table or Refs block.
- `Supported claim? = no`, `Support verdict = no`, or `contradictory` requires `Action = Replace`, `Remove`, or `Verify` and normally `RIS action = Exclude`.
- `Supported claim? = partial` may be kept only as background/context if the manuscript wording is changed so the citation no longer appears to directly support an unsupported claim.
- Add a Critical Warning for every central unsupported numbered citation, unresolved citation metadata problem, or citation-number/reference mismatch.

---

## 2.5 Evidence Package Export

Use when the user asks to save results, generate an evidence package, export EndNote references, or produce durable files after a search or paragraph evidence review. In the current default, ordinary search, target literature search, paragraph citation matching, paragraph polishing, and reference-update workflows all produce durable Markdown + RIS outputs unless the prompt explicitly says chat-only/no-export. For paragraph citation-support requests, this module is the export stage of the unified **Paragraph Citation Package Workflow (Module 2 + Module 2.5)**: **Module 2 → Module 2.5** means analysis first, then export.

Visible default pipeline for paragraph citation/export work:

```text
paragraph → claim extraction → existing numbered citation repair when supplied references are present → one Zotero local search pass → evidence matrix and sentence-level citation recommendations → evidence-backed polishing → **copy-ready manuscript text → revised-sentence Claim–Evidence Matrix snapshot → Citation Insertion Sheet** → annotated text and diff → citation support ledger → Zotero metadata + PDF links → automatic PubMed expansion as a second evidence source when available → combined evidence synthesis and deduplication → reference export standardization by PMID/DOI → metadata QC → Markdown evidence report → EndNote RIS
```

For completeness-oriented requests, replace “one Zotero local search pass” with the Module 1.9 recall-first sequence and include its `Recall Audit` before selection. “Found one supporting paper” is not a stopping condition.

The default deliverable is exactly two files inside a skill-named, topic-specific output folder. The Markdown report contains the Citation Insertion Sheet; it is not a third evidence file:

```text
zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_evidence_review.md
zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_references.ris
```

Do not create extra JSON, BibTeX, EndNote XML, DOI lists, or log files unless the user explicitly requests them. The Markdown report is the human-readable evidence workspace; the RIS file is the EndNote import file.

The RIS file is the single citation handoff between this Skill and EndNote. Before presenting it, run `scripts/ris_lint.py` with `--fail-on-warnings` when the file is available and include an `ENDNOTE_IMPORT_HANDOFF` block with record count, canonical metadata source, deduplication rule, linter status and import instructions. This Skill never edits an EndNote `.enl`, `.Data` or `sdb.eni` file. The user confirms the destination library and performs the import in EndNote.

### 2.5A Multi-option writing card

When the request asks for multiple rewrites, different rhetorical angles, or a more field-native alternative, read [WRITING_OPTIONS_CARD](references/writing-options-card.md) and add a `WRITING_OPTIONS_CARD` to the Markdown report. Generate at most three candidates after the meaning gate and claim/evidence mapping. Each candidate must include `option_id`, `option_name`, `rhetorical_angle`, `target_section`, `rhetorical_job`, `copy_ready_text`, `claim_delta`, `evidence_level`, `citation_set`, `style_basis`, `why_this_works`, `when_to_choose`, `risks`, and `author_check`. Keep `selection_status: pending` until the author chooses; do not silently promote the first candidate to final text.

All candidates share facts, numbers, units, directions, study design, and evidence boundaries unless `claim_delta` says otherwise. Bind each candidate's citations to the Citation Support Ledger. After selection, set `selected_option_id`, mark selected supported citations `RIS action = Include`, mark citations used only by unselected candidates `RIS action = Optional`, and run `POST_WRITE_AUDIT`. Uninspected, contradictory, or not-addressed sources remain `Verify` or `Exclude`.

PubMed-only records do not have a Zotero item key. Report their DOI/PMID and a `zotero_import_status: pending` value rather than fabricating a `zotero://select/items/...` link. If the user explicitly asks to sync selected records into Zotero, use `zotero_add_by_doi` (preferred) or the documented DOI/URL import path, then refresh the search database and re-fetch metadata before returning the new Zotero key. Do not add, tag, move, or delete Zotero items by default.

The installed `format-references-endnote` Skill is an optional downstream document converter for explicit `[PMID: ...]` markers; it is not the discovery layer and must not replace a mixed Zotero + PubMed RIS with a PubMed-only re-fetch. The installed `endnote-workflow` Skill is a separate Windows/EndNote 20 DOCX workflow and is read-only with respect to the library. `bib-formatter` can validate or reformat RIS but does not import records.

When the user supplies manuscript section and paragraph boundaries, add the optional section-aware handoff described in [references/endnote-section-collections.md](references/endnote-section-collections.md). Assign stable paths such as `Discussion/Discussion-01` or `Methods/Methods-02`, preserve `Manuscript section`, `Manuscript paragraph`, `Manuscript group`, `Claim`, and `Evidence role` fields, and run `scripts/write_endnote_collection_package.py` after the canonical RIS has passed metadata QC. The package writer creates one deduplicated master RIS with EndNote-readable keyword fields plus selective per-group RIS files, a manifest, and a manuscript-to-reference map. It does not infer support, silently drop unassigned records, or edit an EndNote library.

Target literature search exports are handled by **Module 1.8 Target Literature Search and Export** and use a different Markdown suffix:

```text
zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_literature_search.md
zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_references.ris
```

The RIS filename may be shared, but its meaning differs by route: paragraph workflows write **Citation RIS**; target literature search workflows write **Search RIS**.

### Trigger Conditions

Route to this module when the user asks for any of the following:

- `/zotero-evidence-review` plus a short request to find evidence, add citations, export a report, or create reusable writing outputs; this simple-request entry defaults to the complete workflow unless there is an explicit chat-only opt-out.
- Ordinary literature search or topic discovery that does not supply a manuscript paragraph; run Module 1 first, then write a search-focused Markdown report plus Search RIS unless chat-only/no-export is explicit.
- `Evidence Package`, `Markdown report`, `EndNote`, `RIS`, `保存报告`, `导出参考文献`, `生成文件`, or `输出文件` attached to a paragraph, manuscript passage, citation-support request, or non-target evidence workflow.
- Default citation-support workflow triggers: `使用技能`, `完整工作流`, `找引文`, `补引用`, `推荐引用`, `citation`, `refs`, `reference`, `参考文献`, or `文献引用` when attached to a paragraph, manuscript passage, or literature-search request.
- A paragraph evidence review plus a request to save or export results.
- A literature search where the user wants a reusable evidence report rather than a target literature search report. Topic-only requests for "which papers use X", "search Zotero for X", "export a literature list/report/RIS", or equivalent route to Module 1.8.

Do not route to this module when the user explicitly opts out with `只在聊天输出`, `不要生成文件`, `不导出`, `chat only`, or equivalent.

### Workflow

1. **Run or reuse the evidence workflow**
   - For paragraph input, run **Module 2** first as the analysis stage of the **Paragraph Citation Package Workflow (Module 2 + Module 2.5)**.
   - For paragraph input with supplied numbered citations or reference lists, run **Module 2.2 Existing Numbered Citation Repair** after claim extraction and before final citation placement/export; preserve `Original citation number`, mark unsupported numbered citation cases, and carry `Original citation number`, `Support verdict`, `Action`, and `RIS action` into the Citation Support Ledger, the report, and RIS QC tables.
   - For paragraph citation-support requests such as `/zotero-evidence-review`, `使用技能`, `找证据`, `找引文`, `补引用`, `推荐引用`, `citation`, `refs`, `参考文献`, or `文献引用`, default to the full workflow and write both `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_evidence_review.md` and `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_references.ris` unless the user explicitly opts out of file generation.
   - For target_literature_search topic input, run **Module 1.8** and save `LITERATURE_SEARCH_REPORT` plus Search RIS by default; do not run paragraph claim extraction, Copy-ready Manuscript Text, sentence-level citation placement, or paragraph diff.
   - For other topic/search input, run **Module 1** first, produce a search-focused report, and convert the final inspected included papers into Search RIS unless the user explicitly opts out.
   - For biomedical paragraph/search requests, the package workflow runs the recall-first PubMed expansion after the Zotero semantic and structured lanes when a PubMed-capable tool is configured and visible.
   - Other external source fallback beyond this built-in PubMed expansion still follows **Module 5: External Source Fallback** and requires availability checks and user confirmation where specified.
2. **Collect canonical metadata**
   - For every Zotero item considered for the final report or RIS, retrieve metadata with `zotero_get_item_metadata`.
   - Retrieve child attachments with `zotero_get_item_children` or `zotero_get_items_children` when PDF links are needed.
   - Use Zotero metadata as the authority for Zotero items. Do not fill missing authors, titles, journals, pages, DOI, PMID, or years from memory.
3. **Run automatic PubMed expansion as a second evidence source when available**
   - After Zotero local search, construct a PubMed query from the topic, extracted claims, and core biomedical concepts.
   - Execute PubMed search automatically in ordinary search, target literature search, and full paragraph package workflows when the topic is biomedical and a PubMed-capable tool is configured and visible in the current MCP tool list.
   - Treat a PubMed-capable tool as visible only when the active session exposes a callable tool whose name or description clearly indicates PubMed / NCBI E-utilities search, such as `pubmed`, `simple-pubmed`, `pubmed-data-server`, `ncbi`, `esearch`, `efetch`, `search-pubmed`, `get_paper_fulltext`, or equivalent biomedical database search capability.
   - Do not assume Zotero MCP itself can search PubMed. Zotero MCP may contain Zotero records with PMID links, but PubMed expansion requires a separate visible PubMed/NCBI-capable tool.
   - Treat Zotero and PubMed as independent retrieval lanes: local Zotero evidence first, then broad and design/method PubMed queries for additional or confirming evidence; do not collapse the search to the first supporting paper.
   - For PancrePal PubMed MCP, use `pubmed_search` first, then call `pubmed_get_details` for PMIDs that may enter the report/RIS; use `pubmed_extract_info` for targeted DOI/authors/abstract extraction when token efficiency matters.
   - For one or two highly relevant PMIDs, use `pubmed_find_related` with `type="reviews"` or `type="similar"` when the user asks for comprehensive coverage, review evidence, or adjacent mechanisms.
   - If full-text support is needed and full-text tools are visible, use `pubmed_detect_fulltext` before any OA PDF download; do not treat downloaded PubMed PDFs as Zotero-local evidence unless the user explicitly imports or attaches them.
   - If no PubMed-capable tool is available, include the copyable PubMed query in the report and mark PubMed expansion as `⚠️ Tool unavailable; search not executed`.
   - If a PubMed-capable tool is visible but the search fails, mark PubMed expansion as `Failed; query reported`, report the attempted query/error briefly, and do not create PubMed-only RIS records.
4. **Combine Zotero and PubMed evidence results**
   - Build a combined candidate table containing Zotero records and PubMed expansion records.
   - Deduplicate evidence candidates by DOI first, then PMID, normalized title, then fuzzy first-author + year + journal.
   - Preserve source labels separately from export metadata: `Zotero`, `PubMed`, or `Zotero + PubMed`.
   - When the same article appears in both Zotero and PubMed, mark source as `Zotero + PubMed` and retain Zotero item/PDF/collection links in the report.
   - When a PubMed record is not present in Zotero and is relevant, mark source as `PubMed` and recommendation as `consider importing` or `recommend citing`.
   - If DOI/PMID/title conflicts suggest two records may not be the same article, mark `Possible metadata mismatch` and keep them unresolved until checked.
   - Include a Citation Support Ledger linking each claim/sentence to its recommended citation, source layer, evidence level, inspection route, evidence location, support verdict, RIS action, and required wording/action.
   - For every recommended citation, record whether the source was inspected through `Zotero metadata`, `Zotero full text`, `Zotero abstract`, `PubMed details`, `PubMed abstract`, or `Not inspected`; search-result snippets alone are insufficient.
   - Use support verdicts exactly from `supports`, `partly supports`, `background only`, `contradicts`, `not addressed`, or `not inspected`.
   - Do not include `not inspected`, `contradicts`, or `not addressed` citations in RIS by default; set `RIS action = Exclude` or `Verify`. Use `Optional` for `background only` unless copy-ready wording explicitly frames it as background/context.
5. **Standardize RIS references at export time by PMID/DOI**
   - After selecting final recommended references, standardize the RIS metadata using identifiers rather than relying only on local Zotero fields.
   - If a selected reference has a PMID and PubMed metadata can be retrieved, use the PMID/PubMed record as the preferred source for RIS citation fields.
   - If no PMID is available but a DOI is available and DOI metadata can be retrieved, use DOI metadata as the preferred source for RIS citation fields.
   - If neither PMID nor DOI metadata is available, use inspected Zotero metadata for Zotero records or inspected PubMed metadata for PubMed records.
   - Keep Zotero source labels and links in the Markdown report, but use the standardized PMID/DOI-derived metadata for the EndNote RIS when available.
   - Never silently standardize: report each selected reference's `Evidence source` and `RIS standardization source` in the Markdown QC table.
6. **Run metadata quality control**
   - Check missing metadata before RIS export: DOI, PMID, journal / publication title, year, volume, issue, pages, and authors.
   - Check Zotero-vs-PubMed and identifier-derived metadata conflicts for DOI, PMID, normalized title, publication year, and journal.
   - Check possible duplicate records by DOI, PMID, normalized title, and fuzzy author + year + journal.
   - Report missing metadata, metadata mismatch, and duplicate warning rows in the Markdown report.
   - Exclude unresolved metadata conflicts from RIS by default; do not silently write questionable records.
7. **Select RIS references**
   - For paragraph workflows, write **Citation RIS**: include final recommended Zotero citations and any eligible PubMed-only recommended citations that support the manuscript wording.
   - For target_literature_search workflows, write **Search RIS**: include the selected literature set from `LITERATURE_SEARCH_REPORT`, including `Core` by default and `Strong Related` only when marked Include/Optional; exclude `Method Background`, `Disease GWAS Only`, `Noise`, and unresolved `Verify` by default.
   - Include PubMed-only papers only when they are marked `recommend citing` or `consider importing`, and only when PubMed metadata is sufficient and comes from an actually completed PubMed search.
   - Exclude low-relevance hits, duplicate records, and unresolved metadata conflicts by default.
8. **Run pre-write QA self-check, then write the two files**
   - Before writing Markdown or RIS content to disk, run the internal **Evidence Package QA Self-Check Prompt** against the complete draft report, planned RIS records, PubMed execution log, metadata QC table, and intended output paths.
   - If the self-check finds missing status, missing critical warnings, missing copy-ready text, missing claim evidence level/source layer, current-study/external-evidence confusion, inaccurate PubMed status, invalid RIS content, absolute paths, unresolved metadata mismatch, or overconfident E-level wording, revise the draft report/RIS first and repeat the self-check.
   - Create or reuse the package output directory according to **Default Output Directory** only after the draft passes the pre-write self-check.
   - Save the Markdown report with the `EVIDENCE_REVIEW_REPORT` template.
   - Save the RIS file with the `RIS_REFERENCE_FILE` template and rules.
   - Run the post-write QA gate before announcing completion: confirm the written Markdown/RIS still match the same checks, and that final chat exposes only status, relative paths, and critical warnings.
   - Final chat output must use this exact compact structure and include no internal checklist details:

```markdown
Generated Evidence Package:
- Status: {Ready / Caution / Partial / Superseded / Unknown}
- Markdown report: `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_evidence_review.md`
- EndNote RIS: `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_references.ris`
- Section-aware requests: add `*_all_references.ris`, `endnote-import/{Section}/{Paragraph}.ris`, `*_collection_manifest.json`, and `*_manuscript_reference_map.md` through `scripts/write_endnote_collection_package.py`

Critical Warnings:
- {warning or No critical warnings}
```

### Default Output Directory

By default, write evidence packages under a deterministic skill output root, then a topic-and-timestamp run folder. Do not write evidence package files into the repository/project root.

```text
zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/
```

The fixed `zotero-evidence-output/` root identifies the files as this skill's output. The run folder combines an LLM-generated brief topic slug with a current local date-time suffix, so repeated runs for the same topic remain easy to sort and unlikely to collide.

The folder must contain only the default two deliverables unless the user explicitly requests additional files:

```text
zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_evidence_review.md
zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_references.ris
```

If the selected run folder already exists, create `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_v2/`, `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_v3/`, etc. Do not overwrite an existing evidence package unless the user explicitly confirms replacement.

### Default Naming

Use an **LLM-generated brief topic slug** plus a current local date-time suffix. The brief topic slug must be inferred from the user's paragraph, claim, or search question; the user should not need to provide it manually.

Naming components:

- `brief_topic_slug`: a short, specific summary of the topic, usually 2-6 words.
- `YYYY-MM-DD_HHMMSS`: current local date and time to seconds, e.g. `2026-06-18_143512`.
- Markdown suffix: `_evidence_review.md`.
- RIS suffix: `_references.ris`.

Slug rules:

- Use lowercase ASCII words when possible.
- Convert spaces, punctuation, slashes, and repeated separators to single underscores.
- Keep meaningful domain abbreviations such as `pcos`, `mr`, `gwas`, or `il6`.
- Keep the slug short but descriptive, usually 2-6 words, e.g. `sedentary_behavior_pcos`.
- Do not use generic literals such as `topic`, `review`, `references`, `output`, `results`, or `zotero` alone.

Default package paths:

```text
zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_evidence_review.md
zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_references.ris
```

If files already exist inside the selected folder, append `_v2`, `_v3`, etc. to the run folder or filenames. Do not overwrite an existing evidence package unless the user explicitly confirms replacement.

### Run Relationship and Superseded Mechanism

Evidence package runs can be related when the user revisits the same topic, expands a previous search, or generates evidence for a different manuscript section using overlapping literature. The skill must record relationships in the new report without silently rewriting old reports.

Run relationship rules:

- Do not automatically modify old evidence package files. Only update, mark, or rewrite prior reports when the user explicitly asks to organize, summarize, consolidate, or supersede existing outputs.
- When a new evidence package is highly similar to existing packages, the new report metadata may list `Related prior packages` with paths, dates, topic slugs, and short relationship notes.
- Similarity judgment should use topic slug similarity, core keyword overlap, user-provided topic/paragraph overlap, selected references overlap, DOI/PMID overlap, and shared claim/manuscript-section context.
- If the new report is broader, newer, more complete, or has stronger search reproducibility / metadata QC than a prior package on the same claim scope, write `Potentially supersedes` in the new report.
- If the new report supports a different manuscript section, sub-claim, method/background/mechanism layer, or a narrower adjacent topic, write `Complementary to` rather than superseding.
- If relationship is uncertain, write `Related; supersession unclear` and explain the missing comparison information.
- `Superseded` package status must be assigned only when the report itself is explicitly being marked as replaced or when the user asks to manage prior outputs. A new report can say it `Potentially supersedes` an older report without changing the old report's status.
- Generate a project-level summary only when the user asks to整理/总结已有输出, consolidate runs, compare packages, or create a project overview. Do not create project-level summary files during ordinary evidence package generation.

Required metadata structure:

```markdown
| Related prior packages | {none / path + date + topic slug + relationship: Potentially supersedes / Complementary to / Related; supersession unclear} |
| Run relationship rationale | {topic slug similarity; core keyword overlap; selected references overlap; DOI/PMID overlap; manuscript section relationship} |
```

### Evidence Package Status

Every generated evidence package must receive exactly one status: `Ready`, `Caution`, `Partial`, `Superseded`, or `Unknown`. The status tells the user whether the package can be used for manuscript writing and what level of caution is required.

| Status | Definition | Trigger conditions | User guidance |
|--------|------------|-------------------|---------------|
| `Ready` | Searches completed as planned, central claims have direct or close support, metadata QC has no unresolved high-risk issue, and selected RIS records passed inspection. | All required evidence was inspected; PubMed is `Completed` when required for a biomedical topic or explicitly not required; central claims are mostly A/B; no unresolved metadata mismatch; no key citation/concept is unverified. | Can be used for drafting with normal scholarly caution. |
| `Caution` | The package is usable but has important caveats. | No direct evidence for a central claim; central evidence is mostly C/D; PubMed unavailable but not essential; duplicate records were detected and safely excluded or resolved; causal, BMI-independent, or pleiotropy wording requires hedge wording. | Use hedge wording and review warnings before manuscript use. |
| `Partial` | A required evidence layer or citation/metadata check is incomplete. | PubMed query failed when PubMed evidence is required; a key citation, PMIDs/DOIs, PMOS, or concept remains unverified; unresolved metadata mismatch affects selected references; PubMed-only evidence was planned but cannot be inspected; RIS cannot safely include a key record. | Do not treat as final; complete verification before submission. |
| `Superseded` | A later evidence package or updated run replaces this package. | The report explicitly identifies a newer package as replacing this one. Do not mark old files superseded automatically unless the user asks to manage prior outputs. | Keep for history only; use the newer package. |
| `Unknown` | The available workflow state is insufficient to determine status. | Tool results, search execution, metadata QC, or claim-level evidence status are unclear or unavailable. | Manual review required. |

Downgrade rules:

- `PubMed query failed` → at least `Partial` when PubMed evidence is required for a central biomedical claim; otherwise at least `Caution`.
- `PMOS`, key concept, citation, DOI/PMID, or title not verified → `Partial` for central claims, otherwise `Caution`.
- `No direct evidence for central claim` → at least `Caution`.
- `Metadata mismatch unresolved` → `Partial`, and the affected reference must be excluded from RIS.
- `Duplicate unresolved but excluded safely` → `Caution`.
- `All required evidence inspected and risks low` → `Ready`.
- If multiple triggers apply, use the most conservative status.

Status must appear in the Markdown report metadata, in the export-file section, and in the final chat summary after files are written.

### Critical Warnings

Critical warnings are the front-loaded reviewer-risk controls for problems that could mislead manuscript writing, citation use, or final submission. They must appear immediately after `Metadata and Use Status` and before `## 3. 核心结论（Bottom Line）` in every `EVIDENCE_REVIEW_REPORT`.

A case must be added to `Critical Warnings` when any of the following conditions applies:

- PubMed tool unavailable or PubMed query failed when PubMed is relevant to the biomedical evidence package.
- A central claim has no direct evidence.
- External evidence contradicts the draft claim.
- A central citation, concept, DOI/PMID, terminology, abbreviation, or claim remains unverified.
- Metadata mismatch remains unresolved for any candidate or selected reference.
- Duplicate Zotero records affect selected references or could change the canonical citation/RIS record.
- A current-study finding could be mistaken for external evidence support.
- Causal wording is not directly supported.
- BMI-independent wording is not directly supported.
- Horizontal pleiotropy wording is not directly supported.

Critical warning rules:

- Each warning must contain `Affected claim`, `Risk`, and `Required action`.
- The warning must be specific enough for the user to locate and revise the affected claim or citation.
- Critical warnings must be consistent with package `Status`; unresolved high-risk warnings usually require `Caution`, `Partial`, or `Unknown`, not `Ready`.
- Critical warnings must not be hidden only in later reviewer-risk or metadata-QC sections.
- If no critical warnings apply, write exactly: `No critical warnings`.
- Critical warnings may be referenced in `Annotated Recommended Text`, reviewer-risk assessment, metadata QC, and final chat summary, but they must not be inserted into `Copy-ready Manuscript Text`.
- The final chat summary must always display `Status` and `Critical warnings`; if none apply, write `No critical warnings`.

Required output structure: use the single author-first, no-repetition layout in [references/report-layout.md](references/report-layout.md). The matrix's `Manual action` column is the author-facing equivalent of the legacy `Recommended action` field.

```markdown
## Critical Warnings
| Affected claim | Risk | Required action |
|----------------|------|-----------------|
| ... | PubMed unavailable / no direct evidence / contradiction / unverified citation or concept / metadata mismatch / duplicate record / current-study vs external-evidence confusion / unsupported causal wording / unsupported BMI-independent claim / unsupported horizontal pleiotropy claim | Revise wording / verify citation / remove claim / complete PubMed search / resolve metadata / deduplicate records / mark as current-study only |
```

If there are no warnings:

```markdown
## Critical Warnings
No critical warnings
```

### Search Reproducibility

Every evidence package must include a reproducible search log so the Zotero and PubMed search process can be audited, repeated, or completed later. The section must cover Zotero semantic search, Zotero keyword search, and PubMed search even when one source returns no hits or cannot be executed.

Search reproducibility rules:

- Record every Zotero semantic query, Zotero keyword query, Zotero keyword/structured query, PubMed query, PubMed max results, and PubMed status used or planned.
- Each row must include `Source`, `Query`, `Mode`, `Max results`, `Status`, `Included`, and `Notes`.
- `Mode` must distinguish at least `semantic`, `keyword`, `structured`, `PubMed`, `PMID details`, `related`, or `full-text inspection` when applicable.
- `Max results` must record the requested limit/max_results for each search; if not available, write `Not recorded`, not a guessed number.
- `Status` must use explicit values such as `Completed`, `Not executed`, `⚠️ Tool unavailable; search not executed`, `Failed; query reported`, `No hits`, or `Partial`.
- PubMed failed or unavailable cases must still record the attempted or planned PubMed query and the failure reason.
- `Included` must record the included_count for that search row; for PubMed rows, list included PMIDs in `Notes` when available.
- `Notes` must record excluded records and reasons, failed reason, included PMIDs, duplicate/metadata exclusion notes, and whether full text was inspected.
- `full_text_inspected` must be marked as exactly `yes`, `no`, or `partial` in `Notes` for searches whose included evidence depends on full-text/PDF inspection.
- Excluded records must be traceable by citation, PMID/DOI, or local Zotero label when available, with a short exclusion reason such as `off-topic`, `wrong population`, `not direct evidence`, `metadata mismatch`, `duplicate`, `no full text`, or `contradicts claim`.

Required output structure:

```markdown
## Search Reproducibility
| Source | Query | Mode | Max results | Status | Included | Notes |
|---|---|---|---:|---|---:|---|
| Zotero | {semantic query} | semantic | {max_results or Not recorded} | Completed / No hits / Failed | {included_count} | full_text_inspected: yes/no/partial; included: {citation keys}; excluded: {record + reason} |
| Zotero | {keyword query} | keyword / structured | {max_results or Not recorded} | Completed / No hits / Failed | {included_count} | full_text_inspected: yes/no/partial; included: {citation keys}; excluded: {record + reason} |
| PubMed | {attempted or planned PubMed query} | PubMed | {max_results} | Completed / ⚠️ Tool unavailable; search not executed / Failed; query reported / Not executed | {included_count} | included PMIDs: {PMIDs or none}; excluded: {PMID/citation + reason}; failed reason: {if any}; full_text_inspected: yes/no/partial |
```

### Copy-ready vs Annotated Output

Every evidence package must separate manuscript-ready prose from evidence-review annotations, and must expose the operational citation handoff separately from both.

`Copy-ready Manuscript Text` is the text users can copy directly into a manuscript:

- Preserve the manuscript's original language unless translation is explicitly requested.
- Do not include internal review notes, workflow explanations, QC comments, tool-status commentary, or phrases such as `citation should be verified`.
- Do not mention PubMed/Zotero execution status inside the copy-ready prose.
- Keep cautious wording required by evidence level and source layer.
- If evidence is insufficient, use hedge wording, knowledge-gap wording, or remove the unsupported claim.
- If a concept, citation, DOI/PMID, or claim is unverified, do not write it as established fact.
- Use only citations that are recommended and not blocked by metadata/citation warnings.

`Citation Insertion Sheet` is the operational citation handoff layer:

- It is mandatory for paragraph citation packages unless no eligible citations are recommended.
- It uses one row per citation placement, with `sentence_id`, `insertion_anchor`, `copy_ready_citation`, `search_tokens`, `canonical_record`, `PMID`, `DOI`, `evidence_role`, `support_verdict`, and `RIS_action`.
- `copy_ready_citation` is the text to paste into an author–year manuscript; `search_tokens` are the short terms to type into Zotero/EndNote. Do not substitute a DOI or Zotero key for the visible citation string.
- A global Author–Year Quick Lookup table must list each included/optional record once, so a user can find all occurrences of the same paper quickly.

`Annotated Recommended Text` is the evidence-review explanation layer:

- It may explain citation placement, evidence level, source layer, caveats, reviewer risk, and metadata/tool limitations.
- It must identify which sentences or clauses are `Current study`, `Zotero external evidence`, `PubMed external evidence`, `Interpretive bridge`, or `Unsupported gap`.
- It should explain when a citation supports direct evidence, related evidence, mechanism, method, background, plausibility, or only a bridge inference.
- It may state that a citation, concept, DOI/PMID, or PubMed search requires verification.

Required output structure:

```markdown
## 2. 可直接使用的稿件文本（Copy-ready Manuscript Text）
### WRITING_OPTIONS_CARD（仅在用户要求多个版本时）
{候选版本、比较表、selection_status 和 selected_option_id；候选正文不得混入内部审计说明}

> {manuscript-ready text only; no workflow notes or internal caveats}

## 3. 主张—证据矩阵（Claim–Evidence Matrix）
| sentence_id | claim_id | Revised sentence / clause | 主张摘要（中文） | Recommended citation | Evidence role | Evidence level | Source layer | Support verdict | insertion_anchor | Manual action |
|-------------|----------|---------------------------|------------------|----------------------|---------------|----------------|--------------|-----------------|------------------|---------------|
| S01 | C01 | ... | ... | Author Year | direct / background / method / bridge | A / B / C / D / E | Zotero external evidence / PubMed external evidence / Current study / Interpretive bridge / Unsupported gap | supports / partly supports / background only / ... | after “...” | insert / hedge / split / verify / remove |

## 4. Citation Insertion Sheet
{sentence-level citation handoff; use the CITATION_INSERTION_SHEET template}

## 5. 注释版推荐文本（Annotated Recommended Text）
| Sentence / clause | Recommended text | Source layer | Evidence level | Citation rationale | Caveat / reviewer risk |
|-------------------|------------------|--------------|----------------|--------------------|------------------------|
| ... | ... | Current study / Zotero external evidence / PubMed external evidence / Interpretive bridge / Unsupported gap | A / B / C / D / E | ... | ... |
```

### Markdown Report Requirements

The report must use Chinese-first user-facing headings and analytical prose by default, while preserving manuscript language and official bibliographic metadata according to **0. Durable Output Language Policy**. It must include these sections in order, including PubMed status even when PubMed was unavailable or failed:


1. `Metadata and Use Status`
2. `Critical Warnings`
3. `核心结论`
4. `可直接使用的稿件文本（Copy-ready Manuscript Text）`
5. `主张—证据矩阵（Claim–Evidence Matrix）` — immediately after the copy-ready text and aligned to the revised sentences/clauses
6. `Citation Insertion Sheet`
7. `注释版推荐文本（Annotated Recommended Text）`
8. `Diff / Change Log`
9. `引文放置建议`
10. `Evidence Logic Chain`
11. `参考文献表`
12. `Search Reproducibility`
13. `Zotero 检索总结`
14. `PubMed 扩展检索`
15. `综合写作建议`
16. `Claims to Revise or Remove`
17. `证据缺口与审稿风险`
18. `元数据质量控制`
19. `导出文件`

Add source and export-standardization detail to the `Reference Table` and `Metadata Quality Control` so the reader can tell whether evidence came from Zotero, PubMed, or both, and whether the RIS was standardized from PMID/PubMed, DOI metadata, or inspected source metadata.

Critical warning report rules:

- `Critical Warnings` must appear immediately after `Metadata and Use Status` and before `## 1. 核心结论（Bottom Line）`.
- Each warning must include `Affected claim`, `Risk`, and `Required action`.
- Critical warnings must include PubMed failures, missing direct evidence for central claims, contradictory evidence, unverified citations/concepts, unresolved metadata mismatch, duplicate selected references, current-study/external-evidence confusion, unsupported causal wording, unsupported BMI-independent wording, and unsupported horizontal pleiotropy wording.
- If no critical warnings apply, write exactly `No critical warnings`.

Search reproducibility report rules:

- `Search Reproducibility` must include Zotero semantic search, Zotero keyword/structured search, and PubMed search rows.
- Each row must record query, mode, max_results, status, included_count, and excluded_reason through the `Source`, `Query`, `Mode`, `Max results`, `Status`, `Included`, and `Notes` columns.
- PubMed failed or unavailable cases must record the attempted or planned PubMed query and failed reason.
- `Notes` must include included PMIDs when available, excluded records and reason, and `full_text_inspected: yes/no/partial`.

Reference canonicalization report rules:

- `Reference Canonicalization Gate` must be completed before `Metadata Quality Control` and before RIS export decisions are finalized.
- The gate may appear as an explicit subsection inside `元数据质量控制（Metadata Quality Control）` rather than as a separate top-level report section, so the public report preserves the required 19-section order.
- Every selected reference must check DOI, PMID, title, first author, and year.
- DOI- or PMID-identical records must be merged into one canonical record, with duplicate Zotero keys recorded.
- PubMed-vs-Zotero conflicts must be marked `Possible metadata mismatch` and unresolved mismatch must not enter RIS.
- RIS action must be exactly one of `Include`, `Exclude`, `Verify`, or `Optional`, with a reason for each action.

Citation support ledger rules:

- `Citation Support Ledger` must appear in every evidence package report that recommends citations, updates numbered citations, or writes RIS.
- The ledger must contain `Claim / sentence`, `Recommended citation`, `Source layer`, `Evidence level`, `Inspection route`, `Evidence location`, `Support verdict`, `RIS action`, and `Required wording/action` columns.
- Allowed `Inspection route` values are `Zotero metadata`, `Zotero full text`, `Zotero abstract`, `PubMed details`, `PubMed abstract`, or `Not inspected`.
- Allowed `Support verdict` values are `supports`, `partly supports`, `background only`, `contradicts`, `not addressed`, and `not inspected`.
- All citations in Copy-ready Manuscript Text, Citation Insertion Sheet, Annotated Recommended Text, Citation Placement, Reference Table, Reference Canonicalization Gate, or RIS must have a matching ledger row.
- `not inspected`, `contradicts`, and `not addressed` rows must not enter RIS by default and must use `RIS action = Exclude` or `Verify` unless the user explicitly overrides after seeing the warning.
- `background only` rows may use `RIS action = Optional`, or `Include` only when the recommended wording makes the background role explicit.
- Existing Numbered Citation Repair rows must propagate `Original citation number`, mapped claim, `Support verdict`, action, replacement candidate, and `RIS action` into Citation Support Ledger rows. Unsupported numbered citations must also appear in Critical Warnings or Claims to Revise or Remove.

Copy-ready and annotated text rules:

- `Copy-ready Manuscript Text` must be directly copyable into the manuscript and must not contain internal review notes, workflow explanations, tool-status comments, or `citation should be verified` wording.
- `Citation Insertion Sheet` must be present for eligible citations and must trace each row to `sentence_id → claim_id → ledger → RIS action`.
- `Annotated Recommended Text` must explain citation placement, source layer, evidence level, caveats, and reviewer risk in a table.
- `Diff / Change Log` must identify each substantive wording change and state whether it addresses grammar/clarity, field-native phrasing, argument flow, evidence calibration, terminology, or citation placement.
- Unsupported or unverified concepts must not be stated as facts in copy-ready text.
- Caveats, verification needs, PubMed failures, and metadata concerns belong in `Annotated Recommended Text`, `Gaps and Reviewer-risk Assessment`, or `Metadata Quality Control`, not inside copy-ready prose.

Evidence-level report rules:

- The Claim–Evidence Matrix must contain an `Evidence level` column using only `A`, `B`, `C`, `D`, or `E`.
- Citation Placement must carry forward the same evidence level used for the relevant claim.
- Reviewer-risk Assessment must state the evidence level in `Evidence basis` so risk judgments are traceable to the same A-E framework.
- Copy-ready Manuscript Text must be automatically hedged by level: A/B may be moderately confident; C uses plausibility wording; D uses current-study wording plus cautious external-evidence bridge language; E is removed, marked for verification in annotated/risk sections, or strongly hedged.

Evidence-boundary report rules:

- The Claim–Evidence Matrix must contain a `Source layer` column using only `Current study`, `Zotero external evidence`, `PubMed external evidence`, `Interpretive bridge`, or `Unsupported gap`.
- Citation Placement and Reviewer-risk Assessment must preserve the same source layer used for the relevant claim.
- Current-study findings must be written as current-study results, not as facts proven by citations.
- External evidence may support biological plausibility, prior association, method, or mechanism, but must not be used to prove SMR, TWAS, MAGMA, colocalization, enrichment, candidate-gene, or other current-study outputs.
- Interpretive bridge sentences must use cautious wording such as `consistent with`, `may suggest`, or `provide biological plausibility`.

Reference table rules:

- Do not expose Zotero item keys as the primary reading object.
- Hide item keys inside `[Item](zotero://select/items/0_{item_key})` links.
- Use `[PDF](zotero://open-pdf/library/items/{attachment_key})` when a PDF attachment key is available; otherwise use `—`.
- Use `[DOI](https://doi.org/{doi})` and `[PMID](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)` links when identifiers are available.
- Use `Not available` for unknown collection membership.

### Reference Canonicalization Gate

Before generating RIS, every selected reference must pass a canonical reference quality-control gate. This gate prevents duplicate keys, incorrect PMID/DOI linkage, abnormal author fields, metadata conflicts, and duplicate RIS export.

Reference canonicalization rules:

- Every selected reference must check DOI, PMID, title, first author, and year before RIS export.
- Every selected reference must record a canonical identifier: DOI / PMID / Zotero key. Prefer DOI when reliable, then PMID, then canonical Zotero key when no external identifier is available.
- If DOI or PMID is the same across candidates, merge them into one canonical record and export at most one RIS record.
- If multiple Zotero keys point to the same work, choose one canonical Zotero key and record all duplicate keys.
- Duplicate check result must be explicit: `unique`, `merged by DOI`, `merged by PMID`, `possible duplicate`, `duplicate excluded`, or `unresolved duplicate`.
- Metadata source of truth must be explicit: `PMID/PubMed`, `DOI metadata`, `Zotero metadata`, or `manual verification required`.
- If PubMed and Zotero metadata conflict for DOI, PMID, title, first author, or year, mark `Possible metadata mismatch`.
- RIS action must be exactly one of `Include`, `Exclude`, `Verify`, or `Optional`.
- Unresolved mismatch must not enter RIS; mark RIS action as `Verify` or `Exclude` until resolved.
- `Optional` is allowed only for relevant background or context references that are not required for the core manuscript claim.
- Each row must include a reason explaining the canonical identifier choice, duplicate decision, metadata source of truth, and RIS action.

Required output structure:

```markdown
## Reference Canonicalization Gate
| Selected reference | Canonical identifier | DOI | PMID | Title check | First author check | Year check | Canonical Zotero key | Duplicate keys | Duplicate check result | Metadata source of truth | RIS action | Reason |
|--------------------|----------------------|-----|------|-------------|--------------------|------------|----------------------|----------------|------------------------|--------------------------|------------|--------|
| Author Year | DOI / PMID / Zotero key: ... | matched / missing / conflict | matched / missing / conflict | matched / conflict | matched / conflict | matched / conflict | KEY | KEY2; KEY3 / none | unique / merged by DOI / merged by PMID / possible duplicate / duplicate excluded / unresolved duplicate | PMID/PubMed / DOI metadata / Zotero metadata / manual verification required | Include / Exclude / Verify / Optional | ... |
```

### Metadata Quality Control

Before writing RIS records, build a quality-control table for every candidate reference:

| Check | What to inspect | Markdown action | RIS action |
|-------|-----------------|-----------------|------------|
| Missing metadata | DOI, PMID, authors, year, journal, volume, issue, pages | Add `Missing metadata` warning with exact missing fields | Omit unknown fields; do not infer |
| Metadata mismatch | Zotero, PubMed, PMID-derived, and DOI-derived DOI, PMID, normalized title, year, journal | Add `Possible metadata mismatch` with conflicting values | Exclude until resolved unless the user explicitly accepts a canonical source |
| Duplicate warning | Same DOI/PMID/title or fuzzy author + year + journal across Zotero and PubMed | Add `Possible duplicate` and list candidate citations | Include only the selected canonical record |
| Evidence source | Whether the evidence record came from Zotero, PubMed, or both | Mark `Zotero`, `PubMed`, or `Zotero + PubMed` | Source label does not determine RIS metadata by itself |
| RIS standardization source | Which identifier/source supplied the final EndNote RIS fields | Mark `PMID/PubMed`, `DOI`, `Zotero metadata`, or `PubMed metadata` | Prefer PMID/PubMed, then DOI, then inspected source metadata |
| PubMed not executed | PubMed-capable tool unavailable | Mark `⚠️ Tool unavailable; search not executed` | Do not create PubMed-only RIS records |
| PubMed search failed | PubMed-capable tool was visible but returned an error | Mark `Failed; query reported` and include the attempted query/error briefly | Do not create PubMed-only RIS records |

### RIS Metadata Rules

RIS records must be generated from inspected metadata only.

| Source | Allowed metadata |
|--------|------------------|
| Selected reference with PMID | Prefer PMID/PubMed metadata for RIS standardization when retrieved |
| Selected reference with DOI but no PMID | Prefer DOI metadata for RIS standardization when retrieved |
| Zotero record without identifier-derived standardization | `zotero_get_item_metadata` output; DOI/PMID/ISBN from Zotero metadata |
| PubMed record without DOI standardization | PubMed returned metadata from a completed search |
| Missing field | Leave blank or omit; do not infer |
| Metadata conflict | Mark in Markdown report; exclude from RIS unless the conflict is resolved |

Zotero-to-RIS mapping:

| Zotero field | RIS field |
|--------------|-----------|
| `itemType` | `TY` (`journalArticle` -> `JOUR`; `book` -> `BOOK`; `conferencePaper` -> `CONF`; `preprint` -> `UNPB` or `JOUR` when already journal-indexed; `report` -> `RPRT`; `thesis` -> `THES`; `webpage` -> `ELEC`; `bookSection` -> `CHAP`; `dataset` -> `DATA`; `patent` -> `PAT`) |
| `creators` | `AU`, one line per author |
| `date` | `PY` and optionally `Y1` |
| `title` | `TI` |
| `publicationTitle` | `JO` / `T2` |
| `journalAbbreviation` | `J2` |
| `volume` | `VL` |
| `issue` | `IS` |
| `pages` | `SP` / `EP` when separable |
| `DOI` | `DO` |
| `PMID` | `AN` or `N1` |
| `url` | `UR` |
| `abstractNote` | `AB` when needed |
| `language` | `LA` |
| `tags` | `KW`, one line per retained scholarly keyword/tag |
| item key | `N1  - Zotero key: XXXXXXXX` only; do not show as citation text |

RIS tag compatibility rules:

- Filter out Zotero workflow/personal tags before writing `KW`, including tags that start with `/`, emoji-only tags, pure-symbol tags, and tags used only for local reading status.
- Keep scholarly subject tags such as MeSH terms, disease names, methods, exposures, and study-design terms.
- Use UTF-8 plain text, but avoid unusual symbols in RIS fields when an ASCII equivalent is available.
- If a creator name appears inverted or nonstandard, verify it against inspected Zotero/PubMed/DOI metadata before normalizing; otherwise disclose the issue in Markdown QC and exclude the record from RIS by default.

### Quality Gates

Before reporting success, check:

- Markdown report exists and includes metadata/use status, critical warnings immediately after metadata/use status, copy-ready manuscript text, annotated recommended text, Zotero search summary, a PubMed Expansion section with query and execution status, Search Reproducibility with Zotero semantic search, Zotero keyword/structured search, PubMed search, attempted/planned PubMed query when unavailable or failed, included PMIDs, excluded records and reasons, `full_text_inspected: yes/no/partial`, claim–evidence matrix, Citation Support Ledger, integrated writing advice, reviewer-risk assessment, Reference Canonicalization Gate, metadata quality-control section, and export file section.
- Metadata and Use Status records `Related prior packages` and `Run relationship rationale`; new reports may say `Potentially supersedes`, `Complementary to`, or `Related; supersession unclear`, but old reports are not automatically modified and project-level summary files are generated only when the user requests consolidation.
- Reference Canonicalization Gate checks DOI, PMID, title, first author, and year for every selected reference; records canonical identifier, canonical Zotero key, duplicate keys, duplicate check result, metadata source of truth, RIS action, and reason; merges same DOI/PMID records; blocks unresolved mismatch from RIS.
- Critical Warnings contains every high-risk issue that meets the trigger conditions and uses `Affected claim`, `Risk`, and `Required action`; if there are no critical warnings, it says exactly `No critical warnings`.
- Citation Support Ledger contains every recommended citation and every RIS candidate, records inspection route and evidence location, uses allowed support verdicts, and blocks `not inspected`, `contradicts`, and `not addressed` rows from RIS by default.
- Copy-ready Manuscript Text is directly copyable, preserves the manuscript language, and contains no internal review notes, workflow explanations, tool-status comments, or `citation should be verified` wording.
- Annotated Recommended Text explains citation placement, source layer, evidence level, caveats, and reviewer risk separately from the copy-ready prose.
- Metadata/use status includes exactly one package status: `Ready`, `Caution`, `Partial`, `Superseded`, or `Unknown`.
- Every claim in the claim–evidence matrix has a source layer and an A-E evidence level.
- Current-study findings, including SMR, TWAS, MAGMA, colocalization, enrichment, candidate-gene prioritization, and user-supplied statistical results, are marked as `Current study` and are not described as proven by external literature.
- Reviewer-risk assessment uses the same A-E evidence levels in the `Evidence basis` column when explaining risk.
- Copy-ready Manuscript Text is hedged according to evidence level: A/B can be moderately confident, C/D must be cautious, and E must be removed, verified, or strongly hedged.
- Copy-ready Manuscript Text separates current-study wording from external-evidence wording and uses interpretive bridge language when connecting the two.
- PubMed status truthfully reflects tool execution: `Completed` requires an actual completed PubMed search and inspected metadata; unavailable, failed, or not-executed searches must not be described as completed.
- PubMed-only RIS records are included only when the PubMed search completed and the record metadata was inspected.
- RIS file is plain RIS only, with no Markdown headings, explanations, comments, or code fences.
- Every RIS record starts with `TY  -` and ends with `ER  -`.
- Recommended Zotero citations use metadata consistent with Zotero.
- PubMed-only recommended citations use metadata consistent with completed PubMed search results; if PubMed was not executed, no PubMed-only RIS records are created.
- Missing metadata, metadata mismatch, and duplicate warning cases are disclosed in the Markdown report and not silently written into RIS.
- All generated-file paths shown in the report and final chat are relative paths; local absolute paths such as `/Users/...` are not allowed.

### Evidence Package QA Self-Check Prompt

The skill must run this internal QA prompt immediately before writing Markdown/RIS files and again after writing them. Use it as a gate, not as user-facing content. Do not announce completion until failures are corrected or explicitly reported as blocking warnings.

```text
你是一名科研 evidence package QA 工程师。请在 zotero-evidence-review skill 写入 Markdown 和 RIS 前执行自检。
检查：
1. Report 是否包含 Status、Critical Warnings、Copy-ready Manuscript Text、Citation Insertion Sheet 和 Diff / Change Log；
2. Claim–Evidence Matrix 是否包含 Evidence level 和 Source layer；
3. Citation Support Ledger 是否覆盖所有推荐引文/RIS候选，并记录 Inspection route、Evidence location、Support verdict、RIS action；Citation Insertion Sheet 是否逐行追溯到同一 ledger 行；
4. 是否把 current-study finding 错写成 external evidence；
5. 是否存在 direct causality、BMI independence、horizontal pleiotropy 等过度表述；
6. PubMed status 是否真实反映工具执行情况；
7. PubMed-only RIS 是否只来自 completed PubMed search；
8. unresolved metadata mismatch 是否被排除出 RIS；
9. not inspected / contradicts / not addressed 的 citation ledger 行是否被排除出 RIS 或标记 Verify；
10. RIS 是否无 Markdown heading/code fence；
11. 所有路径是否为相对路径；
12. 若发现问题，先修正报告再宣布生成完成。
输出：内部自检清单，不必完整暴露给用户；最终 chat 只显示 status、paths 和 critical warnings。
```

Pre-write QA gate checklist:

- `Status`: Markdown report metadata and export section contain exactly one status from `Ready`, `Caution`, `Partial`, `Superseded`, or `Unknown`; final chat will repeat the same status.
- `Critical Warnings`: the section exists immediately after metadata/use status; it either contains a table with `Affected claim`, `Risk`, `Required action`, or exactly `No critical warnings`; warnings are consistent with package status.
- `Copy-ready Manuscript Text`: copy-ready text exists, preserves manuscript language, contains no internal QA/tool notes, and excludes unverifiable or unsupported assertions.
- `Citation Insertion Sheet`: every eligible citation placement has a sentence anchor, copy-ready citation string, search tokens, canonical record, identifier fields, support verdict, and RIS action; repeated records have one global quick-lookup row.
- `Evidence-backed polishing`: English prose has an explicit wording pass for grammar/clarity, field-native phrasing, argument flow, and evidence calibration; the Diff / Change Log records the reason for each material change.
- `Claim evidence level`: every Claim–Evidence Matrix row has `Evidence level` using `A`, `B`, `C`, `D`, or `E`; Citation Placement and Reviewer-risk Assessment preserve the same level.
- `Citation Support Ledger`: every citation in copy-ready text, Citation Insertion Sheet, annotated text, Citation Placement, Reference Table, Reference Canonicalization Gate, and RIS has a ledger row with inspection route, evidence location, support verdict, RIS action, and required wording/action; `not inspected`, `contradicts`, and `not addressed` rows are excluded from RIS or marked `Verify`.
- `Source layer`: every claim-level row distinguishes `Current study`, `Zotero external evidence`, `PubMed external evidence`, `Interpretive bridge`, or `Unsupported gap`; current-study findings are not described as proved by external literature.
- `Overclaim control`: direct causality, BMI independence, horizontal pleiotropy, mediation/mechanism, and genetic-prioritization claims are hedged unless directly supported; E-level claims are removed, marked for verification, or strongly hedged rather than written as established facts.
- `PubMed status`: `Completed` is used only when PubMed search actually executed and relevant metadata was inspected; unavailable/failed/not-executed cases use the exact allowed status and include the planned or attempted query.
- `RIS provenance`: PubMed-only RIS records appear only when PubMed status is `Completed`; no PubMed-only RIS records are written for unavailable, failed, or planned-only PubMed searches.
- `Metadata mismatch`: unresolved metadata mismatch and unresolved duplicate records are disclosed in the report and excluded from RIS unless the user explicitly selected a canonical source.
- `RIS format`: RIS contains only RIS records; no Markdown headings, prose, comments, or code fences; every record starts with `TY  -` and ends with `ER  -`.
- `Relative paths`: Markdown report, Export File section, final chat, and any in-report links to generated files use relative paths only; no `/Users/...`, home-directory, or other local absolute paths.
- `Final response hygiene`: final chat displays only package status, generated relative paths, and critical warnings; do not expose the full internal checklist unless the user asks for debug details.

Post-write QA gate:

- Re-check the written Markdown and RIS against the same checklist before final response.
- If the post-write gate fails, correct the files first when safe; if correction is impossible, do not say the package is complete—return `Status: Partial` or `Unknown` with the blocking critical warning and paths to any partial files.

### Output Format

In chat, after files are written, output only:

```markdown
Generated Evidence Package:
- Status: Ready / Caution / Partial / Superseded / Unknown
- Critical warnings:
  - No critical warnings
  - `<affected claim>` — Risk: `<risk>`; Required action: `<required action>`
- Markdown report: `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_evidence_review.md`
- EndNote RIS: `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_references.ris`

Warnings:
- `<non-critical metadata/tool/status warning if any; otherwise omit this section>`
```

---

## 2.8 Manuscript-Level Thinking Checkpoint

Use this module when the user asks for a whole-manuscript diagnosis, writing-language improvement, Methods/Results/Introduction/Discussion logic review, reproducibility or result-narrative review, revision strategy, argument-spine review, contribution/novelty review, reviewer-risk assessment, or when Module 2/2.2/2.5 meets the automatic checkpoint conditions. The operational details live in the companion [zotero-manuscript-thinking Skill](../zotero-manuscript-thinking/SKILL.md); this section defines how it joins the Zotero evidence workflow.

### Purpose and scope

The checkpoint answers **what should be fixed first across the manuscript**, with language precision as a first-class output. It treats Methods as the reproducibility contract and Results as the evidence narrative, so both must be checked against the paper contract and each other. When the user asks for field-native or target-venue wording, it may also build a small `Domain Style Calibration` corpus from inspectable peer papers and pass the resulting pattern profile to the language editor. It does not replace sentence-level evidence matching, citation verification, paper-to-raw-result auditing, or the dedicated language/section polishers. It must preserve the existing `Current study` / external-evidence boundary and A–E evidence levels.

### Required inputs

1. Establish `manuscript_scope` as A (full manuscript), B (paper skeleton), or C (single paragraph).
2. Record the actual files/sections read and the files not read.
3. Extract a `paper contract`: question, population/object, method, main finding, contribution, and boundary.
4. If any of the first, fifth, or sixth fields is undefined, mark it as an unresolved P0 issue rather than filling it with generic prose.
5. If the request asks for “地道”, a target venue, or peer-paper comparison, establish a `style_corpus_ledger` before rewriting: target profile, section-specific article type, 3–5 matched papers when available, inspected scope, access status, selection rationale, and `calibration_confidence`. Fewer than three suitable papers is `low`; unavailable sources are `none`.

### Zotero-native style-corpus path

When `Domain Style Calibration` is active, the corpus must be retrieved and inspected through the
same read-only Zotero chain used for evidence work:

```text
zotero_get_recent(limit=3)
  → zotero_semantic_search
  → inspect results and select candidates
  → [one separate zotero_search_items or zotero_advanced_search fallback if needed]
  → zotero_get_item_metadata
  → zotero_get_item_children / zotero_get_items_children
  → zotero_get_pdf_outline (prefer the parent item key)
  → zotero_read_pdf_pages (parent or confirmed-readable attachment key)
  → [zotero_get_item_fulltext only as a documented fallback]
```

Run each dependent call only after inspecting the previous result. Record item/attachment keys,
section/subsection, physical PDF page, a minimal source fragment, its abstracted writing pattern,
and `full / partial / metadata-only` inspection status in the style-corpus ledger. Prefer the
parent item key for PDF outline/page resolution: some local bridges list an attachment but cannot
resolve the attachment key to a file. Treat a textual `Error`, `Code:`, `502`, or equivalent
failure in a tool `result` as a failed call even when the wrapper says `isError: false`; record
`fulltext fallback / page unavailable` when the documented full-text fallback succeeds. A search
hit, abstract, or metadata record can justify selecting a candidate, but cannot justify a claim
about full-text writing style. If the smoke test or any upstream call fails, stop dependent calls
and report the exact status; do not convert a skipped PDF call into `no PDF` or `no style pattern`.

### Thinking route

Use `thinking-model-router` and select one primary route by mechanism: `thinking-systems` for argument/section interactions, `thinking-first-principles` for contribution and unsupported conventions, `thinking-steel-manning` for the strongest reviewer objection, or `thinking-socratic` for an undefined question/assumption. Add `thinking-model-combination` only when the primary leaves a material blind spot; cap the run at three models and predeclare the conflict rule. If no route clearly improves the diagnosis, use `NONE` and reason directly.

The route record must include:

```text
route: <skill id or NONE>
role: <job this route performs>
unique_question: <question only this route answers>
blind_spots: <what remains unexamined>
exit: <when to stop or re-route>
```

### Minimum analysis

1. Run the meaning gate and language audit: preserve objects, comparisons, numbers, uncertainty, terminology, citation ownership, and claim verbs; produce a language issue table rather than generic fluency comments.
2. If the request asks for field-native or venue-calibrated wording, run `Domain Style Calibration` after section logic and before the final language pass. Extract rhetorical moves, sentence functions, claim verbs/hedges, terminology, citation ownership and information rhythm; for Methods also extract reproducibility detail order and reporting conventions, and for Results extract result-block order, quantitative anchors and figure/table linking. Do not copy peer prose or import claims.
3. If Introduction is present, map paragraph jobs across context → known → specific gap → method fit → objective/contribution; if Methods is present, map design → sample/variables → procedure → QC/statistics → ethics/data availability and audit its links to Results; if Results is present, map setup/QC → primary finding → support/sensitivity → validation and keep interpretation bounded; if Discussion is present, map finding → interpretation → literature comparison → alternative/limitation → bounded implication.
4. Rebuild the five-sentence argument spine: known problem, specific gap, study question/design, main result with evidence location, and bounded implication.
5. Build a claim–evidence–section map. Every core claim gets a section/figure/table location, source layer, A–E evidence level, direct evidence location, boundary, and gap status.
6. Assign each section one reader-facing job and identify broken handoffs between Introduction, Methods, Results, Discussion, and Conclusion. Check that Methods describes what Results reports and that Results reports what the figures/tables actually show.
7. Run one reviewer stress test: alternative explanation, causal/predictive/mechanistic overreach, scope words, citation context, and whether the conclusion introduces unsupported claims.
8. Rank issues as P0/P1/P2/P3 using reviewer risk × argument leverage × feasibility. Action types are `retrieve evidence`, `re-analyze`, `restructure`, `reframe`, `rewrite`, `remove`, and `verify`.

### Handoff rules

- Missing or weak external support → Module 1 / 2 / 2.2 / 3, with claim IDs preserved.
- Current-study result written as external proof → Module 2 + Module 2.5, with source layer and A–E level preserved.
- Number, scope, figure, or result fidelity risk → `paper-claim-audit`.
- Methods reproducibility gap, missing reporting detail, or Methods–Results mismatch → `methods-section-writer` / `method-writing` / `methods-reverse-engineer`, carrying the study design, reporting guideline, unresolved fields, and claim IDs.
- Results hierarchy, paragraph flow, or support-versus-primary confusion → `results-section-structurer` / `results-section-revision`, carrying finding IDs, quantitative anchors, and figure/table locations.
- Results text versus figure/table labels, numbers, units, or directions → `result-figure-consistencycheck` plus `paper-claim-audit`.
- Reviewer-comment triage or feasibility decision → `revision-strategy-planner`.
- Chinese surface language or formatting → `writing-core`.
- English medical terminology, syntax, tone, and meaning preservation → `medical-english-precision-editor`; if style calibration ran, pass its peer-pattern table and confidence with the handoff.
- Introduction paragraph roles, gap, objective, and contribution chain → `academic-introduction-polisher`.
- Discussion finding–interpretation–limitation chain → `academic-discussion-polisher`.
- Full paper production and independent review orchestration → `paper-spine`.

Do not silently start new experiments, delete text, or rewrite the whole manuscript from a checkpoint. If a proposed action needs missing data or user authorization, mark it `待决策`.

### Compact checkpoint output

When running automatically inside a paragraph package, output only:

```markdown
### Manuscript-level checkpoint
- Scope: A / B / C; files read: ...
- Primary route: ...; unique question: ...
- Language issue: ...
- Methods/Results/Introduction/Discussion logic issue: ...
- Methods–Results alignment: ...
- Highest P0/P1 issue: ...
- Why this changes the local edit: ...
- Next handoff: ...
- Unknowns: ...
```

For a standalone whole-manuscript request, use `MANUSCRIPT_STRATEGIC_REVIEW` in the Appendix and write the full report when file output is requested. Do not create a RIS file for a structural diagnosis unless the underlying evidence workflow independently requires one.

## 3. Citation Verification Protocol

Use when the user asks to verify whether a specific claim, quote, statistic, or citation is actually supported by a cited paper or reference. The protocol automatically detects the reference language and chooses the appropriate verification path.

### Language Detection

1. Retrieve Zotero metadata with `zotero_get_item_metadata` when an item key, title, DOI, or citation can be matched.
2. Determine language from the `language` field first.
3. If `language` is empty or ambiguous, infer from title, abstract, publication title, and full-text/attachment language.
4. Route automatically:
   - **English or non-Chinese scholarly literature** → Full-text PDF path.
   - **Chinese-language references**（期刊论文、图书、学位论文、政策文件）→ CNKI CDP / WebSearch path.
5. If the source language cannot be determined, state the uncertainty and choose the path most likely to verify the available bibliographic data.

### Shared Preflight

1. Confirm the exact claim, quote, statistic, or citation metadata to verify.
2. Confirm the target paper/reference from Zotero metadata or the user's supplied citation.
3. Estimate token budget for full-text verification: `Pages × 700 + 1000`.
4. Warn if remaining tokens < 50k.
5. Confirm whether full text, PDF attachment, abstract, notes, or external bibliographic pages are available.

### Path A: Full-text PDF Verification

Use for English or non-Chinese scholarly papers with full text available in Zotero.

1. Prefer read-only MCP page/full-text access first: use `zotero_read_pdf_pages` page ranges or `zotero_get_item_fulltext` when available, and keep the source in Zotero rather than exporting files.
2. If direct MCP page reading is unavailable and the environment permits temporary files, extract complete PDF text to a temporary file as a fallback; otherwise state which pages/sections could not be accessed.
3. Read every available page sequentially in 250-300 line chunks.
4. Record exact page/line locations for each claim, quote, and statistic.
5. Cross-check numerical data (N=X, p<0.05, CI, effect size, sample size) against the original.
6. Compare the user's claim against Zotero metadata, abstract, tables, figures, and author wording.
7. Judge whether the citation fully supports, partially supports, contradicts, or does not address the claim.

### Path B: Chinese Reference Verification

Use for Chinese-language references, including 中文期刊论文、图书、学位论文、政策文件.

#### Primary Method: CNKI CDP Direct Search

Use this route only when Chrome/CDP MCP browser tools are configured and available in the current environment:

1. Navigate to `kns.cnki.net/kns8s/AdvSearch`.
2. Check for CAPTCHA via screenshot, not snapshot text alone.
3. Enter the exact Chinese title into the search field.
4. Click search and wait for results.
5. Extract structured data from the results table.
6. Compare title / authors / journal or publisher / year.

#### Fallback: Multi-Source WebSearch

When CDP is unavailable and a WebSearch-capable tool is configured, execute all of the following:

1. `"<full title>"` exact match.
2. `<title> <author>` broader match.
3. `"<title>" site:cnki.net`.
4. `"<title>" site:wanfangdata.com.cn`.
5. `"<title>" site:xueshu.baidu.com`.

If neither CDP nor WebSearch tools are available, do not claim that CNKI or web verification was completed. Provide the exact searches above as manual verification queries and mark the route as `⚠️ Tool unavailable` until the user supplies results or enables the required tool.

#### Chinese Reference Verdicts

- **Confirmed**: exact title + author + journal/publisher + year all match.
- **Likely Real**: title matches and at least 2 of the remaining 3 metadata fields match.
- **Metadata Error**: the work exists but citation metadata is wrong.
- **Likely Fabricated**: no credible match after available CNKI/CDP and multi-source fallback checks.

Rules:
- Do NOT claim "Uncertain (needs CNKI verification)" as a final verdict.
- No DOI ≠ fabricated; most Chinese papers lack DOIs.
- Always give a definitive verdict: Confirmed / Likely Real / Metadata Error / Likely Fabricated.

### Self-Audit Checklist

Before claiming "verification complete":
- [ ] Retrieved and inspected Zotero metadata when available.
- [ ] Detected or inferred source language.
- [ ] Used the correct verification path for the source language.
- [ ] For full-text papers: read complete text or clearly stated which pages/sections were available.
- [ ] Located page/line evidence for all checked claims where full text is available.
- [ ] Verified numerical data (N, p value, CI, effect size, dates, page numbers) when relevant.
- [ ] Checked author wording and avoided overstating association as causation.
- [ ] For Chinese references: checked CNKI CDP or all required fallback searches.
- [ ] Stayed within token budget or warned the user before proceeding.

### Output Format

Output format: see **Appendix: Output Templates → VERIFICATION_REPORT**.

---

## 4. Chinese Academic Writing Rules

When responding in Chinese:

- Keep article titles, journal names, author names, DOI, PMID, and item keys in English.
- Do not translate official paper titles unless the user asks.
- Distinguish association, causation, mediation, prediction, and mechanism.
- Use cautious wording when evidence is indirect, observational, or inconsistent.
- Do not use a Zotero item as evidence unless its metadata, abstract, full text, note, or annotation has been inspected.
- Clearly mark whether each citation is for background, method, mechanism, or direct empirical evidence.
- When the evidence is insufficient, suggest hedging: "可能"、"提示"、"与…相关" rather than "证明"、"导致".

### Output Formatting Rule

- Prefer tables over nested bullet lists. List each paper's full metadata (title/journal/DOI/link) **once** in a reference table or Refs block; everywhere else cite as `Author Year (KEY)`.
- Never repeat the same paper's bibliographic block across multiple sections.
- Reserve prose bullets for caveats, wording fixes, and gaps — not for restating table contents.

---

## 5. External Source Fallback

When Zotero returns insufficient results, first check which external-search tools are configured in the current environment. Do not imply that any external MCP server is available unless its tools are actually present.

Potential free MCP servers that may be useful when installed:

| Source | Covers | API Key | Best for |
|--------|--------|---------|----------|
| crossref-academic-mcp-server | Crossref + OpenAlex + Semantic Scholar | None | DOI lookup, citation graph, author profile |
| paper-search-mcp | arXiv + PubMed + bioRxiv | None | Preprints, biomedical literature |
| academix | OpenAlex + DBLP + Semantic Scholar + arXiv + CrossRef | None | CS/AI/ML papers, multi-source aggregation |

### Workflow

1. Search Zotero first.
2. If insufficient, identify available external-search tools.
3. If suitable external tools are available, search them and mark all external results with source labels.
4. If no suitable external tools are available, provide ready-to-copy external search queries and say that the search was not executed.
5. Ask the user whether to add found papers to Zotero.
6. Before adding, ask where to place the items:
   - current collection, when a current collection key/name is known;
   - a specified collection name/key provided by the user;
   - main library only.
7. Use `zotero_add_by_doi` or `zotero_add_by_url` with the `collections` parameter when a target collection is confirmed.

---

## Usage Examples

Use short prompts. `/zotero-evidence-review` is the easiest way to call this skill; the workflow is chosen automatically from the request.

### Zero-friction paragraph citation request

You can invoke the skill and paste only the paragraph. No manual claim IDs, search terms, or module selection are required:

> "/zotero-evidence-review 帮我找到这个段落每句话合适的引文，并生成可导入 EndNote 的 RIS：\n> {粘贴段落}"

The skill will automatically split the paragraph into sentences, extract claims, search Zotero with semantic and structured lanes, run PubMed expansion when the MCP is visible, inspect selected metadata/abstract/full text, produce the `SENTENCE_CITATION_MATRIX` and `CITATION_COVERAGE_SUMMARY`, and write the Markdown report plus Citation RIS. If the user says only `帮我找这段的参考文献` without naming a file format, use the same package default; add `只在聊天输出` or `不要生成文件` to opt out of files.

### Search

> "/zotero-evidence-review 搜 Zotero 里关于肠道菌群和抑郁症的文献"

The skill will:
1. Expand to: `semantic_search("gut microbiota depression Mendelian randomization")` + `search_library(q="gut microbiota depression MR", tags=["Mendelian Randomization", "depression"])`
2. Attempt PubMed expansion when a PubMed-capable MCP tool is visible because this is a biomedical topic.
3. Write a search-focused Markdown report plus Search RIS by default, and return a compact path summary. If the prompt says `只在聊天输出`, `不要生成文件`, `不导出`, or `chat only`, stop at the chat table + Refs.

### Methodology Parameter Retrieval

> "/zotero-evidence-review GSMR 的 HEIDI 阈值、SNP 筛选参数怎么设？请给出原文方法段落和 Zotero PDF 页链接。"

The skill will:
1. Route to Module 1.2 and search original-method, software-implementation, recommendation, and applied-study sources as distinct roles.
2. Inspect the relevant methods pages and report each setting with its complete locating paragraph, section/page numbers, item links, and PDF page links.
3. Write a search report + Search RIS by default, or keep the result in chat when explicitly requested.

### Paragraph Evidence & Citation Analysis

> "/zotero-evidence-review 帮我给下面这段草稿找证据并补引用：
> '慢性炎症通过激活 JAK-STAT 信号通路促进动脉粥样硬化斑块形成，而 IL-6 受体阻断剂可显著降低心血管事件风险。'"

The skill will treat this as citation-support work unless the user explicitly says `不要生成文件`, `只在聊天输出`, `不导出`, or `chat only`:
1. Route the paragraph to Module 2 and extract claims: (a) chronic inflammation → JAK-STAT → atherosclerosis, (b) IL-6R blockade → reduced CVD risk.
2. Build one batch query set and run Zotero semantic search plus one keyword fallback if needed.
3. Reuse the same result pool for Layer A (claim-evidence matrix), Layer B (sentence-level citation recommendations), and the diff paragraph.
4. Continue to Module 2.5 in the full **Paragraph Citation Package Workflow (Module 2 + Module 2.5)**: collect Zotero metadata/PDF links, attempt automatic PubMed expansion after Zotero local search when a PubMed-capable tool is configured and visible, run matching/QC, and write the Markdown report plus EndNote RIS.
5. If the user opted out of files, stop after the chat-only Module 2 output and ask whether to start external search for remaining gaps.

### Strict Verification

> "请验证'IL-6 受体阻断剂可降低心血管事件风险'这句话，确认原文确实这么说了"

The skill will:
1. Extract claim: IL-6R blockade → reduced CVD risk
2. Find the cited paper in Zotero
3. Extract and read full PDF sequentially
4. Report exact line number and quote
5. Judge: fully supports / partially supports / does not support

### Paragraph Citation Insertion

> "/zotero-evidence-review 帮我润色这段讨论，并补充合适的引用：
> '我们的研究发现某基因与 2 型糖尿病之间存在显著关联。这一结果与以往研究一致。'"

The skill will:
1. Route the pasted paragraph to Module 2
2. Search once for relevant genetic association studies in the library
3. Recommend sentence-level citations and explain the citation rationale
4. Suggest more precise wording using diff format when the evidence requires hedging
5. Continue to Module 2.5 and generate the Markdown evidence report plus EndNote RIS unless the prompt says `不要生成文件`, `只在聊天输出`, `不导出`, or `chat only`

Chat-only example:

> "/zotero-evidence-review 只在聊天输出，不要生成文件：帮我给这段草稿找证据并补引用。"

---

## Notes

- Always prefer **semantic search** first for conceptual queries.
- For author/year specific lookups, use keyword search with exact fields.
- Zotero links use the format: `zotero://select/items/0_{ItemKey}`
- Module 1.2 report details and page-level Zotero links follow [references/method-parameter-search.md](references/method-parameter-search.md).
- If the user has not built the semantic index yet, prompt them to run `zotero-mcp update-db`.
- If full-text is needed, suggest `zotero-mcp update-db --fulltext`.
- Token budget for full verification: estimate 700 tokens per page + 1000 overhead.

---

## Appendix: Output Templates

Use these named templates whenever a module references an appendix template. For chat-only outputs, keep full bibliographic metadata in `REFS_BLOCK` only; elsewhere cite papers as `Author Year (KEY)`. For ordinary search, target literature search, and method-parameter reports, use `LITERATURE_SEARCH_REPORT` plus `RIS_REFERENCE_FILE` unless chat-only/no-export is explicit. Module 1.2 adds its detailed `METHOD_PARAMETER_EVIDENCE` block as described in [references/method-parameter-search.md](references/method-parameter-search.md). For paragraph evidence packages, use `EVIDENCE_REVIEW_REPORT` plus `RIS_REFERENCE_FILE`.

### RECALL_AUDIT

```markdown
## Recall Audit
- recall_status: saturated / partial / blocked / scope_limited
- scope: ...
- query_families_run: ...
- raw_hits: ...
- unique_candidates: ...
- inspected_candidates: ...
- direct_support_candidates: ...
- new_direct_candidates_last_round: ...
- coverage_gaps: ...
- reason_for_stop: ...

| Query ID | Lane | Query | Tool status | Raw hits | New unique IDs | New direct candidates | Action |
|---|---|---|---|---:|---:|---:|---|
| Q01 | zotero_semantic | ... | Completed / Failed / Not executed | ... | ... | ... | retain / revise / stop |
```

### QUICK_CITATION_INSERTION_GUIDE

```markdown
## 快速插入引文
1. Word + Zotero：按 Citation Insertion Sheet 的 `search_tokens` 搜索 canonical record，确认作者/年份后插入到 `insertion_anchor`；不要手改 Zotero field。
2. EndNote：先导入 Citation RIS，再用 `Insert Citation` 搜索 `search_tokens`；最终编号和参考文献表由 EndNote/Word 生成。
3. 手动稿件：复制 `copy_ready_citation`；同时保留 `canonical_record`、PMID/DOI 作为核对凭据。
```

### ENDNOTE_IMPORT_HANDOFF

```markdown
## ENDNOTE_IMPORT_HANDOFF
- ris_path: ...
- record_count: ...
- included_records: ...
- optional_records: ...
- excluded_or_verify_records: ...
- deduplication_rule: DOI → PMID → normalized title + first author + year
- ris_lint: passed / failed / not run
- canonical_metadata_sources: PMID/PubMed / DOI / Zotero
- import_action: User imports the UTF-8 RIS into the selected EndNote library
- direct_library_write: not supported; no `.enl`/`.Data` files modified
- optional_document_handoff: format-references-endnote only when explicit `[PMID: ...]` markers are present
```

### ENDNOTE_COLLECTION_MANIFEST

```markdown
## ENDNOTE_COLLECTION_MANIFEST
- collection_package: `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/`
- master_ris: `{run_stem}_all_references.ris`
- group_root: `endnote-import/`
- hierarchy: `Introduction/Introduction-01`, `Methods/Methods-01`, `Results/Results-01`, `Discussion/Discussion-01`
- assignment_key: `section + paragraph_id + claim_ids + evidence role`
- import_rule: import master RIS once; per-group RIS files are selective handoffs and may duplicate records
- group_encoding: RIS `KW` fields plus JSON manifest and Markdown map
- unassigned_policy: retain under `Unassigned/Unassigned`
- direct_library_write: not supported by the package writer
```

### ZOTERO_IMPORT_HANDOFF

```markdown
## ZOTERO_IMPORT_HANDOFF
| Candidate | DOI / PMID | Zotero item key | zotero_import_status | Action |
|---|---|---|---|---|
| Author Year | DOI / PMID | pending | pending / imported / failed | import by DOI only after explicit request |
```

### WRITING_OPTIONS_CARD

```markdown
## WRITING_OPTIONS_CARD
- task_id: ...
- input_scope: ...
- target_section: ...
- corpus_status: inspected / partial / unavailable
- calibration_confidence: high / medium / low / none
- selection_status: pending / selected / author-rejected
- selected_option_id: A / B / C / none

| Option | Rhetorical angle | What changes | Claim delta | Evidence level | Citation set | When to choose | Main risk |
|---|---|---|---|---|---|---|---|
| A | ... | ... | none | ... | ... | ... | ... |
| B | ... | ... | none | ... | ... | ... | ... |
| C | ... | ... | none | ... | ... | ... | ... |

### Option A — ...
- rhetorical_job: ...
- copy_ready_text: ...
- style_basis: ...
- why_this_works: ...
- author_check: ...
```

### REFS_BLOCK

```markdown
**Refs**
- `KEY` — Author (Year). *Title*. *Journal* volume(issue):pages. DOI/PMID/URL. `zotero://select/items/0_KEY`
```

Rules:
- Full metadata appears exactly once.
- Include DOI when available; use PMID or URL when DOI is unavailable.
- Do not repeat title/journal/DOI in claim matrices or recommendation tables.

### CLAIM_EVIDENCE_MATRIX

```markdown
| sentence_id | claim_id | Revised sentence / clause | 主张摘要（中文） | Recommended citation | Evidence role | Evidence level | Source layer | Support verdict | insertion_anchor | Manual action |
|---|---|---|---|---|---|---|---|---|---|---|
| S01 | C01 | X is associated with Y | X与Y存在关联 | Wang 2022 (KEY) | direct | A | Zotero external evidence | supports | after “Y” | insert |
| S02 | C02 | The present study identified Z | 本研究发现Z | — | current-study | D | Current study | current-study only | — | keep current-study wording |
| S03 | C03 | The finding is biologically plausible | 该发现具有生物学合理性 | Chen 2021 (KEY3) | bridge | C | Interpretive bridge | background only | after “plausible” | hedge |
| S04 | C04 | Z causes W independently of BMI | Z独立于BMI导致W | — | gap | E | Unsupported gap | not addressed | — | verify or remove |
```

Rules:
- One row per sentence/claim mapping. Include a concise Chinese `主张摘要（中文）` even when the manuscript is English.
- Use claim IDs consistently in gap handling and sentence-level recommendations.
- `Source layer` must be exactly one of `Current study`, `Zotero external evidence`, `PubMed external evidence`, `Interpretive bridge`, or `Unsupported gap`.
- `Evidence level` must be exactly one of `A`, `B`, `C`, `D`, or `E` as defined in **Module 2 → Unified Evidence Level**.
- Never write compound levels such as `A/B`, `A/C`, or `C/D`. Split claims or use the most conservative single level and explain the choice in `Manual action`.
- `Evidence type` should describe the support role, e.g. `直接证据`, `相近直接证据`, `间接机制证据`, `背景证据`, `current-study only`, `contradicted`, or `requires verification`.
- Mark unsupported, contradicted, or insufficiently verified claims as `Unsupported gap`, evidence level `E`, and `Gap? = ⚠️ 是`.
- Mark current-study findings as `Current study` and evidence level `D` unless external literature directly replicates the same finding in a comparable study.
- External evidence used only for mechanism/background must be represented as `Interpretive bridge` or evidence level C/D, not as proof of the current-study finding.
- Evidence level C or D requires hedge wording in manuscript recommendations; evidence level E requires removal, verification, or strong hedging.

### CITATION_INSERTION_SHEET

```markdown
## Citation Insertion Sheet
- citation_style: author_year / numbered_vancouver / apa_like / user_supplied
- default_action: paste `copy_ready_citation` into the manuscript, then use Zotero/EndNote to resolve the canonical record
- numbering_note: final numbered citations are generated by Word/EndNote after import; this sheet preserves sentence anchors for auditability

| sentence_id | insertion_anchor | copy_ready_citation | search_tokens | canonical_record | PMID | DOI | evidence_role | support_verdict | RIS_action |
|-------------|------------------|---------------------|---------------|------------------|------|-----|---------------|-----------------|------------|
| S01 | after “...” | (Author et al., 2024) | Author 2024 | Author 2024 (KEY) | PMID / — | DOI / — | direct / background / method / bridge | supports / partly supports / background only | Include / Optional / Verify / Exclude |

### Author–Year Quick Lookup
| first_author_year | copy_ready_citation | search_tokens | canonical_record | PMID | DOI | uses |
|-------------------|----------------------|---------------|------------------|------|-----|------|
| Author 2024 | (Author et al., 2024) | Author 2024 | Author 2024 (KEY) | PMID / — | DOI / — | S01, S04 |
```

Rules:
- Create one row for every citation placement in Copy-ready Manuscript Text, even when the same paper appears in multiple sentences.
- `insertion_anchor` must identify the clause or sentence ending where the citation belongs; `after paragraph` is not sufficient.
- `copy_ready_citation` follows `citation_style`; for `author_year`, use the exact punctuation selected by the user or the neutral form `(Author et al., 2024)`.
- `search_tokens` must be short, human-searchable terms such as `Mir 2013`, not a hidden Zotero key.
- `canonical_record`, PMID, DOI, support verdict, and RIS action must match the Citation Support Ledger and Reference Canonicalization Gate.
- Include only eligible `Include`/`Optional` citations in the copy-ready text. `Verify`/`Exclude` records stay in the annotated tables and must not appear as settled citations.
- The global quick lookup table contains each canonical record once and lists all sentence IDs where it is used.

### Diff / Change Log
| sentence_id | original_phrase | revised_phrase | change_type | reason | evidence_level | citation_effect |
|-------------|-----------------|----------------|-------------|--------|----------------|-----------------|
| S01 | ... | ... | grammar/clarity / field-native phrasing / argument flow / evidence calibration / terminology / citation placement | ... | A / B / C / D / E | added / moved / removed / unchanged |

改动摘要：+N词/-M词；主要原因：...

### WRITING_SUGGESTIONS_TABLE

```markdown
| 句子（前15字） | 推荐引文 | Source layer | Evidence level | 引用理由 |
|--------------|---------|--------------|----------------|---------|
| "慢性炎症通过…" | Wang 2022 (KEY) | Zotero external evidence | A | 直接证据；支持炎症通路与结局相关 |
| "我们的SMR发现…" | Li 2023 (KEY2) | Current study / Interpretive bridge | D | 当前研究发现只能由本研究表述；引用仅支持机制合理性 |
| "IL-6受体阻断…" | — | Unsupported gap | E | ⚠️ 库内无直接证据；建议改为更谨慎表述并外部检索 |
```

Rules:
- One row per sentence, not one row per paper.
- `Source layer` must match the most relevant claim in `CLAIM_EVIDENCE_MATRIX`; if a sentence connects current-study output to external evidence, mark the boundary explicitly as `Current study / Interpretive bridge`.
- `Evidence level` must match the most relevant claim in `CLAIM_EVIDENCE_MATRIX`; if a sentence combines multiple claims, use the most conservative level.
- Fold citation-addition, rewording, context, replacement, gap, and terminology advice into the `引用理由` column.
- Prefer a minimal set of high-value citations rather than citation stuffing.

### DIFF_REVISED_PARAGRAPH

```markdown
<!-- diff 格式规则：
  - 删除的词/短语：用 ~~删除~~ 标注
  - 新增的词/短语：用 **新增** 标注
  - 未改动内容保持原样
  - 段落末尾附改动摘要："改动：+N词/-M词，修改原因：[简短说明]"
-->
> 原文改动：~~证明~~ **提示** X 与 Y 相关 **Wang 2022 (KEY)**，并通过 Z 通路影响 W **Li 2023 (KEY2)**。
>
> 改动：+2引用/+1限定词/-1强因果词，修改原因：库内证据支持关联和机制线索，但不足以支持强因果表述。
```

Rules:
- Use `~~删除~~` only for text that should be removed or weakened.
- Use `**新增**` for inserted citations, hedges, qualifiers, or terminology changes.
- Leave unchanged text unmarked.

### LITERATURE_SEARCH_REPORT

```markdown
# 文献检索报告：{topic}

## 1. 检索任务
| Field | Value |
|---|---|
| Topic | {topic} |
| User question | {original user question} |
| Search date | {YYYY-MM-DD} |
| Search mode | target_literature_search / search |
| Zotero status | Connected / Failed / Zotero MCP visible but not connected |
| PubMed status | Completed / ⚠️ Tool unavailable; search not executed / Failed; query reported / Not executed |
| Output | Chat Search / Search Report / Search Report + RIS |
| Status | Ready / Caution / Partial / Unknown |
| Status rationale | {one sentence explaining search completeness and major caveat} |

## 2. Topic Decomposition
| Component | Value |
|---|---|
| Target object | {target object} |
| Data / method / phenotype / cohort | {data, methods, phenotypes, cohorts, exposures, outcomes} |
| Must-have concepts | {concepts required for Core classification} |
| Adjacent concepts | {concepts allowed for Strong Related classification} |
| Exclusion concepts | {false-positive concepts to screen and report} |
| Time / source constraints | {year range, collection/tag, Zotero-only, PubMed expansion, study type, language, or none} |

## 3. Query Expansion Plan
| Query type | Query | Purpose | Expected signal | Noise-control note |
|---|---|---|---|---|
| Semantic query | {semantic query} | broad recall | Core / Strong Related candidates | {noise concepts to watch} |
| Keyword query | {keyword query} | precise metadata/title/abstract retrieval | target data/method/phenotype mentions | {expected false positives} |
| Exact phrase query | {exact phrase query or Not used} | named dataset/cohort/method/phenotype confirmation | direct target use | {why exact phrase matters} |
| Negative / noise-control query | {noise-control query or screening terms} | identify false positives for exclusion | Disease GWAS Only / Noise / Method Background | {how exclusions are reported} |

## 4. 纳入与排除标准
| Decision | Criteria |
|---|---|
| Include | Core; Strong Related when the relation to the target data/method/phenotype/cohort is explicit |
| Exclude | Method Background without target use; Disease GWAS Only; Noise; unresolved duplicates or metadata mismatch |
| Verify | Candidate appears relevant but metadata, abstract, or full-text relation remains insufficient |

## 5. 结果分类标准
| Category | Include rule | Exclude rule | Default RIS action |
|---|---|---|---|
| Core | Directly uses the requested target data/method/phenotype/cohort/resource | Exclude if target use is only inferred from a vague title | Include |
| Strong Related | Explicitly uses adjacent evidence useful for the target set | Exclude if relation is only a shared disease label or generic method | Include / Optional |
| Method Background | Important method/context paper without direct target use | Exclude from Search RIS unless background methods were requested | Optional / Exclude |
| Disease GWAS Only | Disease or psychiatric GWAS without requested data/method/phenotype layer | Exclude from target data/method literature set | Exclude |
| Noise | Off-topic, wrong data layer, generic catalog, duplicate, wrong population, or unrelated retrieval | Exclude and record reason code | Exclude |
| Verify | Possible relevance but metadata/abstract/full text is insufficient | Exclude from RIS until verified unless user overrides | Verify |

## 6. 核心发现
- {3-5 concise Chinese findings about the literature set, categories, and evidence gaps}

## 7. 检索结果总表
| # | Citation | Year | Category | Role | Zotero key | DOI/PMID | Why included | Exclusion reason code | RIS action |
|---|----------|------|----------|------|------------|----------|--------------|-----------------------|------------|
| 1 | Author Year | 2024 | Core / Strong Related / Method Background / Disease GWAS Only / Noise / Verify | ... | KEY / PubMed-only | DOI / PMID / none | directly uses target data / excluded because ... | none / wrong data layer / disease-only GWAS / method-only / generic catalog / metadata insufficient / duplicate / off-topic / wrong population / no inspected metadata | Include / Optional / Exclude / Verify |

## 8. 分类结果
### Core
| Citation | Data / method used | Why core |
|----------|--------------------|----------|
| Author Year | ... | ... |

### Strong Related
| Citation | Relation | Why related |
|----------|----------|-------------|
| Author Year | ... | ... |

### Method Background
| Citation | Method role | RIS action |
|----------|-------------|------------|
| Author Year | ... | Optional / Exclude |

### 方法学参数与原文定位（Module 1.2 only）
| 参数 | 原文设定 | 来源角色 | 解释/调整证据 | 方法学小节 | 印刷页 / PDF页 | Zotero PDF |
|---|---|---|---|---|---|---|
| {parameter} | {exact setting, units, conditions} | Original method / Software implementation / Author recommendation / Applied-study choice | {source-supported effect or 未报告} | {section/subsection} | {printed page / physical PDF page} | [PDF 第{N}页](zotero://open-pdf/library/items/{attachment_key}?page={N}) |

#### 原文定位段落
##### {Author Year — source role}
条目：[Zotero 条目](zotero://select/items/0_{parent_item_key})
位置：{main text or supplement; section/subsection; printed page; physical PDF page}
参数：{parameter names}

> {Complete relevant Methods paragraph verbatim}

解释/调整边界：{source-based interpretation; distinguish analyst interpretation}
PDF 定位：[打开 PDF 第{N}页](zotero://open-pdf/library/items/{attachment_key}?page={N})

### Disease GWAS Only / Noise / Verify
| Citation | Category | Reason | RIS action |
|----------|----------|--------|------------|
| Author Year | Disease GWAS Only / Noise / Verify | ... | Exclude / Verify |

## 9. 噪音与排除原因
| Citation | Category | Exclusion reason code | Human-readable reason | RIS action |
|----------|----------|-----------------------|-----------------------|------------|
| Author Year | Noise / Disease GWAS Only / Method Background / Verify | wrong data layer / disease-only GWAS / method-only / generic catalog / metadata insufficient / duplicate / off-topic / wrong population / no inspected metadata | ... | Exclude / Verify / Optional |

## 10. 推荐阅读顺序
| Priority | Citation | Why read first |
|----------|----------|----------------|
| 1 | Author Year | Defines target dataset / most central evidence / best review starting point |

## 11. Search Reproducibility
| Source | Query | Mode | Max results | Status | Hits | Included | Notes |
|---|---|---|---:|---|---:|---:|---|
| Zotero | {semantic query} | semantic | {max_results or Not recorded} | Completed / No hits / Failed | {hits} | {included_count} | full_text_inspected: yes/no/partial; included: {keys}; excluded: {record + reason} |
| Zotero | {keyword query} | keyword / structured | {max_results or Not recorded} | Completed / No hits / Failed | {hits} | {included_count} | full_text_inspected: yes/no/partial; included: {keys}; excluded: {record + reason} |
| Zotero | {exact phrase query or noise-control query} | exact phrase / noise-control | {max_results or Not recorded} | Completed / No hits / Failed / Not executed | {hits} | {included_count} | exclusion_reason: {reason code}; full_text_inspected: yes/no/partial |
| PubMed | {attempted or planned PubMed query} | PubMed | {max_results} | Completed / ⚠️ Tool unavailable; search not executed / Failed; query reported / Not executed | {hits} | {included_count} | included PMIDs: {PMIDs or none}; failed reason: {if any}; full_text_inspected: yes/no/partial |

## 12. Metadata QC
| Citation | DOI | PMID | PDF | Missing metadata | Duplicate / mismatch | Evidence source | RIS standardization source | RIS action |
|----------|-----|------|-----|------------------|----------------------|-----------------|----------------------------|------------|
| Author Year | DOI / missing | PMID / missing | [PDF](zotero://open-pdf/library/items/ATTACHMENT_KEY) / — | none / fields | none / possible duplicate / Possible metadata mismatch | Zotero / PubMed / Zotero + PubMed | PMID/PubMed / DOI / Zotero metadata / PubMed metadata | Include / Optional / Exclude / Verify |

## 13. Export Files
- Markdown report: `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_literature_search.md`
- EndNote RIS: `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_references.ris` / Not requested
- Included records: {N}
- Search RIS rule: selected literature set only; Core included by default; Strong Related included only when explicitly marked Include/Optional; Method Background, Disease GWAS Only, Noise, and unresolved Verify excluded by default.
- Critical warnings: {No critical warnings / PubMed unavailable / Zotero MCP disconnected / metadata mismatch / unresolved Verify candidates}
```

Rules:
- Use `LITERATURE_SEARCH_REPORT` for target_literature_search and ordinary Module 1 search exports, not paragraph citation-support packages.
- Do not include Copy-ready Manuscript Text, Annotated Recommended Text, paragraph diff, Claim–Evidence Matrix, or sentence-level citation placement unless the user also supplies a manuscript paragraph.
- `Category` must use only `Core`, `Strong Related`, `Method Background`, `Disease GWAS Only`, `Noise`, or `Verify`.
- `RIS action` must use only `Include`, `Optional`, `Exclude`, or `Verify`.
- `Exclusion reason code` must use one of `wrong data layer`, `disease-only GWAS`, `method-only`, `generic catalog`, `metadata insufficient`, `duplicate`, `off-topic`, `wrong population`, `no inspected metadata`, or `none`.
- Keep full official bibliographic metadata in the result table, metadata QC table, or Refs block only; avoid repeating full title/journal/DOI in every section.
- Search Reproducibility must record every Zotero semantic query, Zotero keyword/structured query, and PubMed query when planned or executed.
- Search Reproducibility should include exact phrase or noise-control searches when they were needed to classify exclusions.
- PubMed `Completed` requires actual PubMed execution and inspected PMID metadata; otherwise use `⚠️ Tool unavailable; search not executed`, `Failed; query reported`, or `Not executed`.
- Search RIS records must still follow `RIS_REFERENCE_FILE`: plain RIS only, inspected metadata only, no Markdown, no fabricated DOI/PMID, and no PubMed-only records unless PubMed status is `Completed` with inspected metadata.
- Report generated paths as relative paths only.

### EVIDENCE_REVIEW_REPORT

```markdown
# 证据综述：{topic}

## 1. Metadata and Use Status

来源：Zotero 本地库；PubMed: {Completed / ⚠️ Tool unavailable; search not executed / Failed; query reported / Not executed only for explicit chat-only or non-PubMed workflows}

| Field | Value |
|-------|-------|
| 生成日期 | {YYYY-MM-DD} |
| Package status | Ready / Caution / Partial / Superseded / Unknown |
| Status rationale | {one sentence explaining the main trigger for this status} |
| User guidance | {可直接用于写作 / 必须使用 hedge wording / 不建议作为最终证据包 / 仅保留历史记录 / 需要人工检查} |
| Citation style | {author_year / numbered_vancouver / apa_like / user_supplied} |
| Related prior packages | {none / path + date + topic slug + relationship: Potentially supersedes / Complementary to / Related; supersession unclear} |
| Run relationship rationale | {topic slug similarity; core keyword overlap; selected references overlap; DOI/PMID overlap; manuscript section relationship} |
| 来源 | Zotero 本地库；PubMed: {Completed / ⚠️ Tool unavailable; search not executed / Failed; query reported / Not executed only for explicit chat-only or non-PubMed workflows} |
| 输入 | {user paragraph, claim, or search question} |

## 2. Critical Warnings
| Affected claim | Risk | Required action |
|----------------|------|-----------------|
| ... | PubMed unavailable / no direct evidence / contradiction / unverified citation or concept / metadata mismatch / duplicate record / current-study vs external-evidence confusion / unsupported causal wording / unsupported BMI-independent claim / unsupported horizontal pleiotropy claim | Revise wording / verify citation / remove claim / complete PubMed search / resolve metadata / deduplicate records / mark as current-study only |

If no critical warnings apply, write exactly:

No critical warnings

## 3. 可直接使用的稿件文本（Copy-ready Manuscript Text）
> {manuscript-ready text only; preserve the manuscript's original language unless translation is requested; hedge according to A-E evidence level; do not include workflow notes, internal caveats, or verification reminders}

## 4. 主张—证据矩阵（Claim–Evidence Matrix）
| sentence_id | claim_id | Revised sentence / clause | 主张摘要（中文） | Recommended citation | Evidence role | Evidence level | Source layer | Support verdict | insertion_anchor | Manual action |
|-------------|----------|---------------------------|------------------|----------------------|---------------|----------------|--------------|-----------------|------------------|---------------|
| S01 | C01 | ... | ... | Author Year | direct / background / method / bridge | A / B / C / D / E | Zotero external evidence / PubMed external evidence / Current study / Interpretive bridge / Unsupported gap | supports / partly supports / background only / contradicts / not addressed / not inspected | after “...” | insert / hedge / split / verify / remove |

## 5. Citation Insertion Sheet
{sentence-level citation handoff; use the CITATION_INSERTION_SHEET template}

## 6. 注释版推荐文本（Annotated Recommended Text）
| Sentence / clause | Recommended text | Issue type / writing issue | Source layer | Evidence level | Citation rationale | Caveat / reviewer risk |
|-------------------|------------------|----------------------------|--------------|----------------|--------------------|------------------------|
| ... | ... | weak opening / overconfident framing / current-study vs external-evidence confusion / unsupported numbered citation / none | Current study / Zotero external evidence / PubMed external evidence / Interpretive bridge / Unsupported gap | A / B / C / D / E | ... | ... |

## 7. Diff / Change Log
| sentence_id | original_phrase | revised_phrase | change_type | reason | evidence_level | citation_effect |
|-------------|-----------------|----------------|-------------|--------|----------------|-----------------|
| S01 | ... | ... | grammar/clarity / field-native phrasing / argument flow / evidence calibration / terminology / citation placement | ... | A / B / C / D / E | added / moved / removed / unchanged |

改动摘要：+N词/-M词；主要原因：...

## 8. 审计附录（Audit Appendix）

### 核心结论（Bottom Line）
- {1-3 句中文证据判断；如稿件原文为英文，可在中文判断后保留必要英文术语}

### 引文放置建议（Citation Placement）
| 句子 / 位置 | Original citation number | 推荐引文 | 用途 | Source layer | Evidence level | 措辞建议 |
|-------------|--------------------------|----------|------|--------------|----------------|----------|
| ... | 6 / 18 / none | Author Year | background / direct / method / caveat / bridge | Current study / Zotero external evidence / PubMed external evidence / Interpretive bridge / Unsupported gap | A / B / C / D / E | ... |

### SENTENCE_CITATION_MATRIX
| sentence_id | Original sentence | claim_ids | citation_need | source_layer | evidence_level | Recommended citations | Support verdict | Evidence location | Wording action | RIS action | Author check |
|-------------|-------------------|-----------|---------------|--------------|----------------|-----------------------|-----------------|-------------------|----------------|------------|--------------|
| S01 | ... | C01 | citation_required / citation_optional / current_study / common_knowledge / interpretive_bridge / unsupported | Zotero external evidence / PubMed external evidence / Current study / Interpretive bridge / Unsupported gap | A / B / C / D / E | Author Year (KEY) / — | supports / partly supports / background only / contradicts / not addressed / not inspected | Zotero full text p. X / PubMed abstract / none | keep / hedge / reframe / split sentence / remove / verify | Include / Optional / Exclude / Verify | confirm placement / confirm current-study framing / confirm gap |

### CITATION_COVERAGE_SUMMARY
| Metric | Count / status | Rule |
|--------|----------------|------|
| Input sentences | N | Every sentence has one `sentence_id` |
| Sentences with `citation_required` | N | Each has an eligible citation or an explicit gap decision |
| Citation-required sentences covered | N / N (%) | Sentence → claim → inspected source → eligible RIS action is complete |
| Current-study sentences | N | Written as current-study findings; external citations cannot prove them |
| Optional/common-knowledge/bridge sentences | N | Citation decision is explicit even when no RIS record is needed |
| Unsupported or verify sentences | N | Must be hedged, split, removed, or sent to external search |
| Unmapped claims | N | Must be zero before package status can be `Ready` |
| RIS candidates without a sentence/claim mapping | N | Must be zero; otherwise set `Partial` and exclude the orphan record |
| Coverage status | complete / partial / blocked / not_applicable | `Ready` requires `complete` when citation work is requested |

Rules:
- Create exactly one row per input sentence and preserve input order. `sentence_id` values must be stable within the package (`S01`, `S02`, …).
- `claim_ids` must point to the Claim–Evidence Matrix. A sentence with two independent claims must list both claims; no claim may disappear from the sentence matrix.
- `citation_required` requires an eligible citation or an explicit unsupported/verify gap decision. `current_study`, `common_knowledge`, and `citation_optional` may legitimately use `—`.
- `source_layer` and `evidence_level` must match the mapped claim rows. For mixed sentences, use the most conservative level and state the boundary in `Wording action`.
- `Support verdict`, `RIS action`, and inspection route must agree with the Citation Support Ledger. `not inspected`, `contradicts`, and `not addressed` cannot use `RIS action = Include`.
- `Evidence location` must identify a page, section, abstract element, annotation, or `none`; a search-result snippet alone is insufficient.

### Citation Support Ledger
| Claim / sentence | Recommended citation | Source layer | Evidence level | Inspection route | Evidence location | Support verdict | RIS action | Required wording/action |
|------------------|----------------------|--------------|----------------|------------------|-------------------|-----------------|------------|-------------------------|
| ... | Author Year / none | Current study / Zotero external evidence / PubMed external evidence / Interpretive bridge / Unsupported gap | A / B / C / D / E | Zotero metadata / Zotero full text / Zotero abstract / PubMed details / PubMed abstract / Not inspected | Zotero note/PDF page/annotation; PMID abstract; DOI metadata; or none | supports / partly supports / background only / contradicts / not addressed / not inspected | Include / Exclude / Verify / Optional | keep / hedge / reframe as background / remove / replace citation / complete inspection |

Ledger rules:
- Every citation appearing in Copy-ready Manuscript Text, Annotated Recommended Text, Citation Placement, Reference Table, Reference Canonicalization Gate, or RIS must appear in this ledger.
- `Inspection route` must name the inspected evidence path; search-result snippets alone are not an inspection route.
- `Support verdict` must be one of `supports`, `partly supports`, `background only`, `contradicts`, `not addressed`, or `not inspected`.
- `not inspected`, `contradicts`, and `not addressed` must not enter RIS by default; use `RIS action = Exclude` or `Verify`.
- `background only` may be `Optional` or included only when the manuscript wording explicitly frames the source as background/context rather than direct support.
- If Existing Numbered Citation Repair is present, propagate `Original citation number`, `Support verdict`, action, replacement candidate, and `RIS action` into the relevant ledger rows.

The matrix is the sentence-level source of truth for placement. The Citation Support Ledger remains the record-level source of truth for metadata, support verdict, and RIS eligibility.

### Existing Numbered Citation Repair
| Original citation number | Supplied reference | Claim supported by this number | Support verdict | Verification verdict | Evidence level | Action: Keep / Replace / Remove / Verify / Add supporting citation | Replacement candidate | Original citation number preserved for audit | Final numbering handled by EndNote/Word | RIS action | Reason |
|--------------------------|--------------------|--------------------------------|-----------------|----------------------|----------------|--------------------------------------------------------------------|-----------------------|----------------------------------------|----------------------------------------|------------|--------|
| 6 | Wang 2022 Nat Genet sedentary-behavior GWAS | sedentary behavior contributes directionally to PCOS susceptibility | partial / no | partially supported / not addressed for this claim | C / E | Replace / reframe as background | Shao 2026 / other direct PCOS-sedentary or MR reproductive-health genetics source | yes | yes | Exclude / Optional | Supports sedentary-behavior GWAS/background, not the specific PCOS directional claim unless text is reframed |

## 9. Evidence Logic Chain
| Step | Current-study element | External evidence link | Source layer | Evidence level | Inference limit |
|------|-----------------------|------------------------|--------------|----------------|-----------------|
| 1 | {e.g., SMR/TWAS/MAGMA/colocalization/enrichment/current finding} | {citation or none} | Current study / Zotero external evidence / PubMed external evidence / Interpretive bridge / Unsupported gap | A / B / C / D / E | {what can and cannot be inferred} |

## 10. 参考文献表（Reference Table）
| # | Citation | Year | Study type | Main use | Evidence source | Zotero | PDF | DOI | PMID | Collection |
|---|----------|------|------------|----------|-----------------|--------|-----|-----|------|------------|
| 1 | Author et al., *Journal* | 2024 | Systematic review | ... | Zotero / PubMed / Zotero + PubMed | [Item](zotero://select/items/0_KEY) | [PDF](zotero://open-pdf/library/items/ATTACHMENT_KEY) | [DOI](https://doi.org/10.xxxx/xxxx) | [PMID](https://pubmed.ncbi.nlm.nih.gov/PMID/) | Collection name |

## 11. Search Reproducibility
### Recall Audit
- recall_status: saturated / partial / blocked / scope_limited
- scope: ...
- query_families_run: ...
- raw_hits: ...
- unique_candidates: ...
- inspected_candidates: ...
- direct_support_candidates: ...
- new_direct_candidates_last_round: ...
- coverage_gaps: ...
- reason_for_stop: ...

| Source | Query | Mode | Max results | Status | Included | Notes |
|---|---|---|---:|---|---:|---|
| Zotero | {semantic query} | zotero_semantic | {max_results or Not recorded} | Completed / No hits / Failed | {included_count} | raw hits: {}; new unique IDs: {}; new direct candidates: {}; included: {citation keys}; excluded: {record + reason} |
| Zotero | {keyword query} | zotero_structured | {max_results or Not recorded} | Completed / No hits / Failed | {included_count} | raw hits: {}; new unique IDs: {}; new direct candidates: {}; included: {citation keys}; excluded: {record + reason} |
| PubMed | {broad MeSH/title-abstract query} | pubmed_broad | {max_results} | Completed / ⚠️ Tool unavailable; search not executed / Failed; query reported / Not executed | {included_count} | included PMIDs: {PMIDs or none}; raw hits: {}; new unique IDs: {}; new direct candidates: {}; failed reason: {if any} |
| PubMed | {design/method query} | pubmed_design_or_method | {max_results} | Completed / ⚠️ Tool unavailable; search not executed / Failed; query reported / Not executed | {included_count} | included PMIDs: {PMIDs or none}; raw hits: {}; new unique IDs: {}; new direct candidates: {}; failed reason: {if any} |

## 12. Zotero 检索总结（Zotero Search Summary）
| 检索路径 | Query | Hits | Included | 备注 |
|----------|-------|-----:|---------:|------|
| Semantic search | ... | 0 | 0 | ... |

## 13. PubMed 扩展检索（PubMed Expansion）
日期：{YYYY-MM-DD}
数据库：PubMed
状态：Completed / ⚠️ Tool unavailable; search not executed / Failed; query reported

检索式：`{copyable PubMed query}`

| # | Citation | PMID | DOI | In Zotero? | Evidence use | Recommendation |
|---|----------|------|-----|------------|--------------|----------------|
| 1 | Author et al., Year | [PMID](https://pubmed.ncbi.nlm.nih.gov/PMID/) | [DOI](https://doi.org/10.xxxx/xxxx) | Yes / No / Possible mismatch | ... | Use / Consider importing / Exclude |

## 14. 综合写作建议（Integrated Writing Advice）
### 原始主张
{original text}

### Zotero 证据
- ...

### PubMed 证据
- ...

### 推荐修改
> ...

### 为什么这样表述更安全
...

## 15. Claims to Revise or Remove
| Claim | Problem | Evidence level | Source layer | Required revision |
|-------|---------|----------------|--------------|-------------------|
| ... | unsupported / overconfident / weak opening / current-study miscast as external evidence / unsupported numbered citation / metadata unresolved | A / B / C / D / E | Current study / Zotero external evidence / PubMed external evidence / Interpretive bridge / Unsupported gap | hedge / remove / verify / replace citation / reframe as background / move to gap statement |

## 16. 证据缺口与审稿风险（Gaps and Reviewer-risk Assessment）
| Affected claim / sentence | Risk | Severity | Evidence basis | Suggested fix |
|---------------------------|------|----------|----------------|---------------|
| ... | ... | High / Moderate / Low | Source layer: Current study / Interpretive bridge / Unsupported gap; Evidence level A / B / C / D / E; ... | ... |

## 17. 元数据质量控制（Metadata Quality Control）

### Reference Canonicalization Gate
| Selected reference | Original citation number | Canonical identifier | DOI | PMID | Title check | First author check | Year check | Canonical Zotero key | Duplicate keys | Duplicate check result | Metadata source of truth | RIS action | Reason |
|--------------------|--------------------------|----------------------|-----|------|-------------|--------------------|------------|----------------------|----------------|------------------------|--------------------------|------------|--------|
| Author Year | 6 / none | DOI / PMID / Zotero key: ... | matched / missing / conflict | matched / missing / conflict | matched / conflict | matched / conflict | matched / conflict | KEY | KEY2; KEY3 / none | unique / merged by DOI / merged by PMID / possible duplicate / duplicate excluded / unresolved duplicate | PMID/PubMed / DOI metadata / Zotero metadata / manual verification required | Include / Exclude / Verify / Optional | Canonical identifier chosen after DOI, PMID, title, first author, and year checks; Possible metadata mismatch if conflicts remain; unsupported numbered citation rows are excluded or marked Verify |

### Metadata QC Table
| Citation | Original citation number | Missing metadata | Metadata mismatch | Duplicate warning | Evidence source | RIS standardization source | RIS action |
|----------|--------------------------|------------------|-------------------|-------------------|-----------------|----------------------------|------------|
| Author Year | 6 / none | DOI / PMID / pages / none | Possible metadata mismatch: Zotero DOI ... vs PubMed DOI ... / none | Possible duplicate with Author Year / none | Zotero / PubMed / Zotero + PubMed | PMID/PubMed / DOI / Zotero metadata / PubMed metadata | Include / exclude / needs manual check |

## 18. 导出文件（Export File）
- Markdown report: `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_evidence_review.md`
- EndNote RIS: `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_references.ris`
- Evidence source: Zotero local library and PubMed expansion are separate evidence steps; combined results are deduplicated by DOI/PMID/title when available.
- Package status: Ready / Caution / Partial / Superseded / Unknown.
- Status rationale: {main trigger for the assigned status}.
- RIS standardization source: PMID/PubMed metadata when available and retrieved; DOI metadata when PMID is unavailable and DOI lookup succeeded; otherwise inspected Zotero or PubMed source metadata.
- RIS inclusion rule: final recommended citations only; low-relevance hits and unsupported numbered citation rows excluded.
- Numbering rule: `Original citation number` is retained for auditability only; final EndNote numbering is controlled by the manuscript citation processor after RIS import.
- Metadata warnings: {missing fields, mismatches, duplicate warnings, or none}

When section and paragraph IDs are supplied, include `ENDNOTE_COLLECTION_MANIFEST` after the standard EndNote handoff. Do not create a second untracked RIS source: the section-aware master RIS is a tagged derivative of the canonical RIS, and the per-group files are selective views.

### ENDNOTE_IMPORT_HANDOFF
- RIS path: `zotero-evidence-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_references.ris`
- Record count: {N}
- Included / Optional / Exclude / Verify: {counts}
- Deduplication rule: DOI → PMID → normalized title + first author + year
- RIS lint: passed / failed / not run
- Canonical metadata sources: PMID/PubMed / DOI / Zotero
- Import action: user imports the UTF-8 RIS into the selected EndNote library
- direct library write: not supported; no `.enl`, `.Data`, or `sdb.eni` files modified
- Optional document handoff: `format-references-endnote` only when explicit `[PMID: ...]` markers are present
- PubMed-only Zotero import: not executed unless explicitly requested; never invent a Zotero item key
- Section/paragraph grouping: use `ENDNOTE_COLLECTION_MANIFEST` when manuscript boundaries are supplied; master RIS is deduplicated and group RIS files are selective
```

Rules:
- If supplied numbered citations are present, include the Existing Numbered Citation Repair table and carry `Original citation number`, `Claim supported by this number`, `Support verdict`, `Verification verdict`, `Action: Keep / Replace / Remove / Verify / Add supporting citation`, `Replacement candidate`, `Original citation number preserved for audit`, `Final numbering handled by EndNote/Word`, and `RIS action` into Citation Placement, Reference Canonicalization Gate, and Metadata QC.
- If the manuscript has a weak opening, overconfident framing, or current-study findings that could be mistaken for external evidence support, flag the issue in Annotated Recommended Text and Claims to Revise or Remove before presenting the copy-ready text.
- Keep Zotero item keys hidden in links or notes, not as primary citation labels.
- If a PDF attachment is unavailable, use `—` in the PDF column.
- If collection membership is unknown, use `Not available`.
- If PubMed was not actually searched, clearly mark the status and include only the planned or attempted query, not invented results.
- Always include the metadata quality-control table; use `none` when there are no missing metadata, metadata mismatch, or duplicate warning cases.
- Every claim-level table in the report must use the same source layer definitions from Module 2; do not merge current-study findings and external evidence into a single unsupported proof statement.
- Every claim-level table in the report must use the same A-E evidence level definitions from Module 2; do not introduce alternate strength scales such as `strong/moderate/weak` without also mapping them to A-E.

### MANUSCRIPT_STRATEGIC_REVIEW

```markdown
# Manuscript Strategic Review: {topic}

## 1. Scope and Input Ledger
- manuscript_scope: A / B / C
- files_read: ...
- files_not_read: ...
- target_venue: ...
- research_mode: ...

## 2. Router Decision
- domain: academic writing / research argument
- problem_type: diagnose + optimize
- work_layers: language / domain_style_calibration / introduction_logic / discussion_logic / whole_paper
- route: {thinking-systems / thinking-first-principles / thinking-steel-manning / thinking-socratic / NONE}
- role: ...
- unique_question: ...
- blind_spots: ...
- exit: ...

## 3. Paper Contract
| Field | Extracted statement | Evidence/location | Status |
|---|---|---|---|
| Question | ... | ... | defined / unresolved |
| Population/object | ... | ... | defined / unresolved |
| Method | ... | ... | defined / unresolved |
| Main finding | ... | ... | defined / unresolved |
| Contribution | ... | ... | defined / unresolved |
| Boundary | ... | ... | defined / unresolved |

## 4. Language Audit
| Location | Original phrase | Problem type | Risk of meaning drift | Revision strategy | Author check |
|---|---|---|---|---|---|

## 5. Domain Style Calibration
- target_profile: ...
- corpus_status: inspected / partial / unavailable
- calibration_confidence: high / medium / low / none
- style_corpus_ledger: ...

### Zotero Style Evidence Ledger
| Peer ID | Zotero item/attachment | Section | PDF page | Short source fragment | Abstracted pattern | Inspection status |
|---|---|---|---:|---|---|---|

### Observed patterns
| Pattern ID | Section/job | Peer evidence | Pattern | Boundary |
|---|---|---|---|---|

### Draft-to-profile comparison
| Pattern ID | Draft location | Mismatch | Safe action | Meaning check |
|---|---|---|---|---|

### Author decisions
- Keep: ...
- Confirm: ...
- Do not adopt: ...

## 6. Introduction Logic Map
| Paragraph | Primary job | Main claim | Evidence/citation role | Missing bridge | Action |
|---|---|---|---|---|---|

## 7. Methods Logic Map
| Subsection | Operational job | Required details | Results cross-link | Missing/ambiguous | Action |
|---|---|---|---|---|---|

## 8. Results Logic Map
| Result block | Reader question | Finding/quantitative anchor | Figure/table | Support vs primary | Interpretation boundary | Action |
|---|---|---|---|---|---|---|

## 9. Discussion Logic Map
| Paragraph | Finding used | Interpretation level | Literature comparison | Alternative/limitation | Implication boundary | Action |
|---|---|---|---|---|---|---|

## 10. Argument Spine
1. Known problem: ...
2. Specific gap: ...
3. Question/design: ...
4. Main result and evidence location: ...
5. Bounded implication: ...

## 11. Claim–Evidence–Section Map
| Claim ID | Claim | Section/figure | Source layer | Evidence level | Evidence location | Boundary | Gap |
|---|---|---|---|---|---|---|---|

## 12. Holistic Diagnosis
| ID | Location | Problem | Evidence / basis | Risk | Leverage | Priority | Action type | Next owner | Done when |
|---|---|---|---|---|---|---|---|---|---|

## 13. Reviewer Stress Test
| Objection | Evidence | Required wording/action | Status |
|---|---|---|---|

## 14. Prioritized Revision Plan
### Round 1 — meaning and section logic
...
### Round 2 — language
...
### Round 3 — evidence and consistency
...

## 15. Handoff and Stop Conditions
...

## 16. Unresolved Unknowns
...
```

Rules:
- Use this report for diagnosis and sequencing; it is not a submission-readiness certificate.
- Preserve claim IDs, source layers, and A–E evidence levels when handing work to downstream modules.
- Mark uninspected Zotero/PubMed evidence as `not inspected`; never infer search completion.
- If scope is B or C, state which whole-manuscript conclusions are unavailable.

### RIS_REFERENCE_FILE

```ris
TY  - JOUR
AU  - Last, First
PY  - 2024
Y1  - 2024/01/01
TI  - Article title
JO  - Journal name
J2  - Journal abbreviation
VL  - 12
IS  - 3
SP  - 100
EP  - 110
DO  - 10.xxxx/xxxx
AN  - PMID
UR  - https://doi.org/10.xxxx/xxxx
KW  - Zotero tag
N1  - Zotero key: XXXXXXXX
ER  -
```

Rules:
- The RIS file must contain RIS records only; no Markdown headings, prose, code fences, or comments. It also must not contain audit tables, citation-repair notes, or original-number annotations.
- Every record starts with `TY  -` and ends with `ER  -`.
- Use one `AU  -` line per author and one `KW  -` line per retained scholarly keyword/tag.
- Filter out personal/workflow tags before writing `KW`, including emoji-only tags, pure-symbol tags, tags beginning with `/`, and local reading-status tags.
- Split page ranges into `SP` and `EP` when possible; if not possible, write the original page string to `SP` and omit `EP`.
- Omit unknown fields rather than guessing.
- Add `N1  - Zotero key: XXXXXXXX` for Zotero items only.
- PubMed-only records require metadata from an actually completed PubMed search and completed metadata inspection; when PubMed is unavailable or metadata has not been inspected, do not create PubMed-only RIS records.
- Exclude unresolved metadata mismatch and unresolved duplicate warning records unless the user explicitly selects the canonical record.
- Include final recommended citations only. Original numbered references marked `no`, `contradictory`, or `unverified` must be excluded by default; references marked `partial` may enter RIS only when the revised manuscript keeps them as background/context and the Markdown report marks that limited role with `RIS action = Optional` or `Include`.

### VERIFICATION_REPORT

```markdown
## Verification Report

| Claim / citation | Paper / reference | Path | Evidence location | Support level / verdict | Issue |
|------------------|-------------------|------|-------------------|-------------------------|-------|
| "X causes Y" | Author 2020 | Full-text PDF | p. 6 / line 436 | Partial support | supports association, not causation |
| "N=500" | Author 2021 | Full-text PDF | p. 3 / line 152 | ✅ Correct | — |
| 中文题名 + 作者 + 年份 | 中文期刊 | CNKI/WebSearch | CNKI result row | Confirmed | — |
```

Rules:
- `Path` must identify the verification route: `Full-text PDF`, `CNKI`, `WebSearch`, or another explicit route.
- `Evidence location` should include page/line when full text is available, or result source/row when verifying Chinese bibliographic metadata.
- `Support level / verdict` must be decisive: fully supported, partially supported, contradicted, not addressed, Confirmed, Likely Real, Metadata Error, or Likely Fabricated.
