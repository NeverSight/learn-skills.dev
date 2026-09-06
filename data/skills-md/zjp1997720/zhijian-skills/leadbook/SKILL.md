---
name: leadbook
description: 生产独立高质量中文商业短书、白皮书、方法论书、操作手册和 PDF 引流品的写书工作流。适用于用户说“写白皮书”“写引流书”“写方法论短书”“写商业手册”“写 PDF 书”“写企业 AI 落地白皮书”“写个人 IP 白皮书”“写超级个体商业操作系统”“写内容获客手册”。正文必须独立成书，不写销售 CTA，不绑定课程、企微、咨询或分身系统；可额外生成书外分发说明和私域运营包。
---

# Leadbook

用于把一个商业主题写成独立、高质量、可公开传播的中文短书或白皮书。它继承 `tech-book` 的工程化写书骨架，但输出目标从技术出版改为普适商业认知与行动资产。

## 核心边界

- 正文必须独立成立：读者不购买任何产品，也能完整受益。
- 正文禁止硬 CTA：不写“加企微”“领取资料”“购买课程”“咨询我”等转化话术。
- 正文不绑定大鹏的分身系统、课程、定制、企业培训。
- 书外可以生成 `distribution-note.md` 和 `private-domain-pack.md`，但它们不得进入正式 PDF。
- 第一版默认写 30-50 页中文短书，不做 200 页大部头。
- Core 链路只依赖 Python 标准库，可完成脚手架、章节同步、Markdown 导出和质量检查。
- 通用模式默认使用公开 Web；小红书、公众号采集、Nowledge、Obsidian 和 Vault 都是可选 Provider，缺失时不得阻塞成书。
- 正式 PDF 可选使用 `$kami` 的中文 `long-doc.html` 风格：暖纸底、ink-blue、克制 editorial 排版。
- 正文配图优先使用 Kami 信息图：结构、流程、对比、公式、清单。`$imagegen` 主要用于封面、章节扉页和书外分发图。

## 快速开始

新建一本书时，优先运行脚手架：

```bash
LEADBOOK_SKILL_DIR="/path/to/installed/leadbook"
python3 "$LEADBOOK_SKILL_DIR/scripts/scaffold_leadbook.py" \
  "/path/to/books/超级个体商业操作系统" \
  --title "超级个体商业操作系统" \
  --content-profile methodology-book \
  --voice-profile product-architect \
  --author "大鹏"
```

脚手架会复制 `assets/repo-template/`，自动同步章节并生成带安全标记的标准 book repo。`--force` 只允许替换带 `.leadbook-project.json` 标记的既有 Leadbook 项目。之后按阶段工作，不要直接在聊天里散写全文。

完整成书属于耐久任务。每个 Phase 完成后运行 `python3 scripts/leadbook-stage.py mark <phase>`，把可恢复检查点写入 `.leadbook-run.json`。恢复时先运行 `python3 scripts/leadbook-stage.py next`，从第一个未完成阶段继续。具体规则见 [执行检查点](references/execution-checkpoints.md)。

运行前按需读 [运行时与隐私边界](references/runtime-and-privacy.md)。Kami、小红书和公众号采集都是可选 Provider，不阻塞 Core 链路。

## 工作流

### Phase 1：Book Brief

先写清楚这本书为什么存在。产出并维护：

- `BOOK_BRIEF.md`：书名、副标题、目标、边界、完成标准。
- `READER_PROFILE.md`：读者是谁、处境、痛点、阅读动机。
- `POSITIONING.md`：核心主张、反常识判断、竞争性视角。
- `book-state.yaml`：章节状态、证据状态、输出状态和交付成熟度。
- `VISUAL_PLAN.md`：正文信息图、封面视觉、章节扉页和输出路径。
- `IMAGEGEN_BRIEF.md`：仅用于 `$imagegen` 位图视觉，不用于正文信息图。
- `src/INTRODUCTION.md`：读者可见开场。正式写作时删除模板标记，写入真实处境、问题重定义和阅读路径。

如果用户只给书名，先根据书名拟一版 brief，再指出缺口。不要把缺口脑补成事实。

`BOOK_BRIEF.md` 必须写清 `content_profile`、`voice_profile` 和 `voice_anchor`。书型决定结构，专家文风决定读者感受到“谁在说”，名人锚点负责把 Agent 快速拉进具体思考姿态。没有 voice profile 和 voice anchor，书会退化成资料汇编。

`BOOK_BRIEF.md` 还必须写清 opening contract 和 chapter rhythm。一本商业书不是把章节模板重复 6 次；它要先把读者带进一个真实处境、误判或反常识 tension，再说明这本书会怎样推进判断。没有 opening contract，正文很容易从第一页开始就像工作坊手册。

Agent 默认自主推进：只给书名时，先生成 v0 brief、v0 evidence plan 和 v0 outline，并在文件里标记 assumptions。不要把可逆判断交给用户。只有作者真实经历、私密案例、商业承诺、身份背书、不可逆定位会显著改变事实边界时，才停下来确认。

### Phase 2：Research & Evidence

资料先行。正式写作前先读 `references/research-stack.md`，按最小最强工具集建立证据链。写作前维护：

- `SOURCE_MAP.md`：调研来源地图，记录来源层级、工具、关键词、用途和权重。
- `AUTHORITY_ACCOUNTS.md`：领域权威公众号/作者/机构地图，先确认值得抓取的账号，再抓文章。
- `CLAIM_LEDGER.md`：关键事实、数据、判断、来源和可信度。
- `CASE_LIBRARY.md`：案例、反例、场景、可公开程度。
- `BEHAVIOR_SEED_PLAN.md`：从 brief / reader / positioning / outline 自动推导行为层采集对象。
- `BEHAVIOR_LEDGER.md`：招聘、活动、公开项目、合作公告等行为信号。
- `TRANSACTION_LEDGER.md`：定价页、产品页、报名页、交付边界、购买异议等交易信号。
- `bibliography.md`：参考来源。
- 每章 `src/chapter-xx/refs.md` 和 `cases.md`。

默认从公开 Web 完成 L1、L3、L4、L5 四层证据。只有用户明确需要且环境真实可用时，才增加小红书、公众号或本地内容 Provider。公开来源必须记录能直接打开的具体 URL；搜索关键词、网站名、平台首页和“公开案例页”不算证据。

搜索年份使用当前年份和近三年，不写死年份。市场数据、平台规则、行业事实必须进 `CLAIM_LEDGER.md`。不能核验的数据写数量级或标记缺口。

默认证据层级：

1. `L1-fact`：高权重事实来源，用于行业数据、平台规则、政策、公司信息、报告。
2. `L2-demand`：小红书、公开评论、问答，用于用户痛点原话、标题钩子、评论反对意见、收藏/评论/转发信号。
3. `L3-behavior`：招聘 JD、活动议程、公开项目、合作公告，用于判断市场真实动作和组织资源配置。
4. `L4-transaction`：定价页、产品页、报名页、交付边界、购买异议，用于判断付费意愿和引流品定位。
5. `L5-discourse`：公众号、博客、访谈、对标作者，用于观点谱系、案例素材和叙事结构。
6. `L6-owned`：Nowledge / Obsidian / Vault，用于低权重内部上下文、自有案例、历史项目、用户原话或场景补充。

Nowledge/Obsidian 不作为高权重信息源。不得用它们单独支撑市场事实、行业判断、平台规则或高置信数据；如确实使用，优先写入 `CASE_LIBRARY.md`，并标记为自有案例、历史经验或场景。

小红书调研使用本地 REST fallback。当前 `xiaohongshu-mcp` 的 MCP `search_feeds` 工具可能超时；当搜索不稳定时，直接运行：

```bash
python3 scripts/xhs-research.py \
  "个人IP打造" "内容获客" "中小企业AI落地" \
  --limit 20 \
  --details 5
```

脚本会生成 `research/xhs/*.md` 和 `research/xhs/*.json`。把其中的平台事实和高频问题写入 `CLAIM_LEDGER.md`，把可复用案例、反例、读者场景写入 `CASE_LIBRARY.md`。小红书材料只能作为需求侧和内容侧证据；涉及行业事实、市场规模、政策规则时必须再用权威来源交叉验证。

公众号调研必须先做 `AUTHORITY_ACCOUNTS.md`。先用通用 Web 搜索或 `$wechat-article-search` 发现专家、机构、媒体、操盘者和反方声音，再用 `$wxmp-article-harvester` 对已确认账号批量归档。商业、运营、平台和 AI 相关主题默认抓最近 365 天文章；经典理论可补更早文章，但必须标记为 `evergreen`。

正确流程是：关键词发现 → 确认账号 → 批量归档 → 本地关键词筛选。网页和单篇公众号链接用通用网页抓取工具落地。所有资料都要回填到 `SOURCE_MAP.md`；只有被实际引用的事实才进入 `CLAIM_LEDGER.md`，避免把资料堆积误认为研究完成。

正式正文必须做证据去后台化：不要把“需求侧样本”“公众号元数据”“线索”“文章池”写给读者。后台材料要翻译成具体来源、具体场景、具体判断和边界。规则见 `references/research-stack.md`。

Phase 2 完成不等于“资料很多”。证据真正闭环的最低标准是：

- `bibliography.md` 已形成读者可见参考页，不只是几条占位列表。
- 每个写入 `book-state.yaml` 的章节 `refs` / `cases` 数，都已经回填到对应 `src/chapter-xx/refs.md` 和 `cases.md`。
- `outputs.references` 只有在读者可见参考页和章节映射都闭环后才能标 `true`。
- `SOURCE_MAP.md` 中标记 used/selected/fetched/exported/done 的来源都有具体 URL。
- `CLAIM_LEDGER.md` 的 fact、`BEHAVIOR_LEDGER.md` 和 `TRANSACTION_LEDGER.md` 的有效记录都能回到具体 URL。

行为层和交易层由 Agent 自动推导，不默认要求用户提供公司名或关键词。Agent 从 `BOOK_BRIEF.md`、`READER_PROFILE.md`、`POSITIONING.md`、`OUTLINE.md`、`SOURCE_MAP.md` 生成采集方向。用户只在行业取向、竞品范围或不可逆定位会改变书的立场时介入。

### Phase 3：Framework & Outline

根据书型选择 `content_profile`，根据作者姿态选择 `voice_profile`，再用 `voice_anchor` 指定最典型的名人锚点。详细规则见 `references/profiles.md`。

生成 `OUTLINE.md` 时：

- 用 `##` 表示正式章节。
- 章节路径统一为 `chapter-01`、`chapter-02`，不要用中文标题生成路径。
- 每章写清：这一章在整本书里的任务。它是重定义、论证、建模、案例、步骤、边界还是收束。
- 每章写清：结论或判断、读者问题、证据或来源、案例或反例、行动产出、作者判断。
- 每章写清：至少 1 个可视化机会。如果没有，也要说明为什么文字更清楚。
- 目录要体现读者路径，而不是只罗列概念名。需要时按 Part / 阶段组织。

整本书默认要有一个 reader-facing opening block，放在正文正式章节之前。它至少回答四件事：

1. 读者正处在什么真实场景或误判里。
2. 这本书到底要重新定义什么问题。
3. 读完以后读者会获得什么新判断和行动框架。
4. 这本书会怎样推进，不是简单罗列目录。

运行：

```bash
python3 scripts/sync-summary.py
```

这会生成 `src/SUMMARY.md`，创建章节目录，并以 merge 方式同步 `book-state.yaml`，保留已有研究、输出和章节进度。

### Phase 4：Chapter Writing

每章作为一个独立写作检查点。每次只加载：

1. `OUTLINE.md`
2. `BOOK_SUMMARY.md`
3. 当前章 `refs.md`
4. 当前章 `cases.md`
5. `glossary.md`
6. `CLAIM_LEDGER.md` 的相关条目

章节不再强制使用同一套标题骨架。统一标题会把白皮书、研究报告和 playbook 都压成课程手册。每章必须满足 chapter contract，但呈现结构按 `content_profile` 和章节任务调整。

每章必须包含这些内容，可以换标题、合并段落或换顺序：

- 结论或判断：本章直接给出什么判断。
- 读者问题：读者在什么具体场景里需要这一章。
- 证据或来源：事实、案例、行为信号、交易信号或需求材料来自哪里。
- 案例或反例：公开案例、自有案例、行为信号、交易信号或假设案例，并标明边界。
- 行动产出：读者读完能得到一个判断、步骤、清单、模板、自测或路线图。
- 作者判断：体现 `voice_profile` 的取舍、边界和立场。

正文不等于 workbook。能放进 `dist/worksheets/`、附录或章节尾工具箱的填写任务，不默认占正文主结构。只有 `playbook` 和 `course-manual` 才应高频使用练习、自测、模板块；`methodology-book`、`whitepaper`、`business-report` 优先保证论证推进、节奏变化和作者判断。

推荐结构按书型选择：

- `methodology-book`：问题定义 → 旧框架失效 → 系统模型 → 案例/反例 → 行动原则。
- `whitepaper`：事实背景 → 趋势判断 → 证据链 → 风险边界 → 对读者的影响。
- `playbook`：场景 → 错误做法 → 步骤 → 模板/清单 → 停手条件。
- `course-manual`：学习目标 → 解释 → 示例 → 练习 → 检查标准。
- `research-analyst`：数据断言 → 趋势判断 → 二阶影响 → 反方证据 → 边界条件。

全书需要足够的 toolbook 元素：对比表、步骤、提示框、错误清单、模板块、自测题、案例框、信息图。但不要为了凑数量把每章压成工作表。一般每章 1-2 个高价值元素就够；`playbook` 和 `course-manual` 可以提高密度，`methodology-book`、`whitepaper`、`business-report` 以判断推进和阅读节奏为先。

每章完成后更新 `BOOK_SUMMARY.md` 和 `book-state.yaml`。没有更新摘要和状态，不算完成。

六章以上或要求 PDF 的任务不得把研究、全书写作、构建和视觉 QA 压在一个不可恢复的长回合里。至少在 `research`、`outline`、`writing`、`build`、`visual-qa` 后写检查点；后台会话提前结束时，从 `.leadbook-run.json` 继续，不重新研究或重写已完成章节。

章节初始文件带 `<!-- leadbook-template: chapter -->` 标记。正式写作时删除该标记；Markdown 导出会自动跳过仍是模板的未写章节，让 `draft` 适合逐章 WIP。

更新状态时，`book-state.yaml` 里的 `refs` / `cases` 必须和对应 `refs.md` / `cases.md` 的真实有效记录一致。不能只在状态表里写“本章有 3 条 refs”，但章节证据文件仍停留在模板占位。

### Phase 5：Review & Quality Gate

正式合并前读 `references/quality-gates.md`。先合并正文，再跑正文底线检查：

```bash
python3 scripts/export-markdown.py
python3 scripts/check-leadbook.py --target draft dist/book.md
```

`leadbook` 有三档完成状态，不能混用：

- `draft`：正文可读，适合继续写作和内部修改；允许证据、视觉和附件未闭环。
- `review-ready`：主书完整，Markdown / HTML / PDF 可评审；参考资料、证据表、信息图、字体和状态表齐全。
- `publish-ready`：整套公开分发包完整；公众号/权威来源达到主题要求，工作表、参考资料页、书外分发说明和私域承接包全部完成。

只写完正文时，最多汇报 `review-ready`。没有通过 `publish-ready` 检查，不得说“可公开发布”“可作为完整引流品交付包”。

`draft` 检查重点：

- 正文是否独立成立。
- 是否出现硬 CTA 或产品绑定。
- 关键事实是否能回到 `CLAIM_LEDGER.md`。
- 正文是否把后台证据语言翻译成读者语言。
- `voice_profile` 和 `voice_anchor` 是否形成专家口吻，而不是资料汇编。
- 是否有空泛商业词。
- 每章是否有结论、问题、模型、案例、行动建议。
- `book-state.yaml` 是否准确记录证据、输出和交付状态。
- 如果 `outputs.references=true` 或 `quality.reference_page=true`，必须已经有像样的读者参考页，并且章节 `refs.md` / `cases.md` 不是空模板。
- 如果 `wxmp_pack` 仍是 `partial`，只能标为 `draft` 或 `review-ready`，不能标为 `publish-ready`。

`draft` 在构建前运行，允许 `VISUAL_PLAN.md` 中已经登记 Output Path 的 SVG / section image 尚未生成；检查器只给 warning。进入 `review-ready` 后，所有必填视觉资产必须真实存在。

### Phase 6：Build & Kami Output

合并正文：

```bash
python3 scripts/export-markdown.py
```

生成或更新 Kami 信息图：

```bash
python3 scripts/generate-kami-diagrams.py
```

Leadbook 信息图必须采用当前 `$kami` 的 diagram primitive 逻辑：图是嵌入正文的 SVG 结构素材，不是带边框、水印和内部大标题的大卡片。生成器必须保持：

- 已安装 Kami 时使用当前主线 Skill，默认路径 `~/.agents/skills/kami`；未安装时保留 Core Markdown 能力并使用内置基础 HTML 模板。
- 不写 `Kami information diagram`、模板名、水印或无关备注。
- 不在图内重复大标题；标题和解释交给正文段落与 caption。
- SVG 在 HTML/PDF 中按正文宽度输出，可见图形区域也要贴近正文宽度，不能只让透明画布变宽。
- 节点内中文必须居中、可读、不出框；长标签先改短，再换行。
- 箭头、节点、分隔线按固定网格落点；不能出现肉眼可见的漂浮箭头、错位、遮挡。

如果需要封面或章节扉页视觉，使用 `$imagegen` 生成位图，复制到 `assets/images/`，并回填 `IMAGEGEN_BRIEF.md`。正文解释性配图默认不用 `$imagegen`，用 Kami SVG 信息图。

生成 Kami HTML：

```bash
python3 scripts/export-kami-html.py dist/book.md dist/book.html
```

渲染 PDF：

```bash
python3 scripts/render-pdf.py dist/book.html dist/book.pdf
```

生成逐页视觉 QA 清单和页面图片：

```bash
python3 scripts/prepare-pdf-visual-audit.py
```

必须实际查看 `dist/qa/contact-sheet.png` 和逐页 PNG，把每页 `Checked`、`Issues`、`Fix Status` 与图表 ID 填完，将 `audit_state` 改为 `passed`。自动渲染只准备清单，不代表视觉通过。

输出阶段读 `references/kami-output.md`。PDF 里只放正式书籍正文和必要附录。`distribution-note.md`、`private-domain-pack.md` 只作为书外运营物料保存。

主书评审前必须运行：

```bash
python3 scripts/check-leadbook.py --target review-ready --update-state dist/book.md
```

公开发布前必须运行：

```bash
python3 scripts/check-leadbook.py --target publish-ready --update-state dist/book.md
```

只有带 `--update-state` 且返回 0 的检查器能把成熟度升级，并在 `dist/qa/gates/` 写入与当前 Markdown、HTML、PDF、视觉审计和参考资料摘要绑定的 receipt。正文、HTML、PDF 或参考资料变化后旧 receipt 自动失效；禁止手工把 `review_ready` / `publish_ready` 改为 true。

`publish-ready` 会检查整个项目，不只检查正文：`book-state.yaml`、公众号/权威账号状态、参考资料页、`dist/worksheets/`、`distribution-note.md`、`private-domain-pack.md`、HTML/PDF 和视觉资产都会进入硬门。若某个主题明确不需要公众号证据，必须在汇报里说明，并显式使用 `--allow-partial-wxmp`，不能默认跳过。

`review-ready` 和 `publish-ready` 都会检查章节证据映射：如果 `book-state.yaml` 声明某章已有 `refs` 或 `cases`，但对应 `src/chapter-xx/refs.md` / `cases.md` 仍是空模板，检查必须失败。整本书不能只在 `CLAIM_LEDGER.md` 和 `CASE_LIBRARY.md` 里堆后台材料。

`publish-ready` 还会默认检查行为层和交易层：`BEHAVIOR_LEDGER.md` 至少 3 条有效行为信号，`TRANSACTION_LEDGER.md` 至少 3 条有效交易信号，且 `book-state.yaml` 标记闭环。若主题明确不需要其中一层，必须在汇报里说明，并显式使用 `--allow-missing-behavior` 或 `--allow-missing-transaction`。

自动检查通过不等于视觉通过。宣称 `review-ready` 或 `publish-ready` 前，必须把 PDF 渲染成页面图片，至少逐页检查所有含图页面：正文宽度、图内文字、caption、分页、封面和目录。检查结果必须写入 `dist/qa/pdf-visual-audit.md`。没有页面级视觉 QA 审计文件，不得说成书可交付。

## 书外运营物料

当用户明确要“文章末尾怎么介绍这本书”“私域怎么承接”时，生成：

- `dist/distribution-note.md`：书籍定位、适合读者、读完能得到什么、文章末尾介绍和分发边界，不写进 PDF。
- `dist/private-domain-pack.md`：欢迎语、标签问题、读者分层、后续内容和边界说明，不写进 PDF。
- `dist/worksheets/`：至少一份读者可填写或可执行工作表，必须和主书核心模型直接对应。

这些材料服务分发，不改变书的正文。

## 资源说明

- `scripts/scaffold_leadbook.py`：创建新 leadbook repo。
- `assets/repo-template/scripts/xhs-research.py`：通过本地 `xiaohongshu-mcp` REST API 采集小红书搜索、笔记详情和评论样本，作为调研证据包。
- `assets/repo-template/scripts/generate-kami-diagrams.py`：根据 `VISUAL_PLAN.md` 生成新版 Kami SVG primitive 信息图。
- `assets/repo-template/scripts/prepare-pdf-visual-audit.py`：渲染全部 PDF 页面、生成 contact sheet 和逐页视觉 QA 清单。
- `assets/repo-template/scripts/leadbook-stage.py`：记录并验证可恢复阶段检查点。
- `assets/repo-template/`：每本书项目的模板和脚本。
- `assets/repo-template/BEHAVIOR_SEED_PLAN.md`：行为层自动推导计划模板。
- `assets/repo-template/BEHAVIOR_LEDGER.md`：行为层信号账本模板。
- `assets/repo-template/TRANSACTION_LEDGER.md`：交易层信号账本模板。
- `assets/repo-template/dist/qa/pdf-visual-audit.md`：PDF 页面级视觉 QA 审计模板。
- `references/research-stack.md`：最小最强调研工具集、权威账号地图、证据层级和来源权重规则。
- `references/profiles.md`：内容 profile 和专家 voice profile。
- `references/quality-gates.md`：正文质量门和禁区。
- `references/kami-output.md`：Kami 排版输出规则。
- `references/runtime-and-privacy.md`：Core/Optional Provider、依赖、凭证和隐私边界。
- `references/execution-checkpoints.md`：长任务阶段门、恢复方式与完成状态事务。
- `tests/test_leadbook.py`：Core、安全、状态、视觉和隐私回归测试。
- `evals/evals.json`：代表性调用与预期行为。
