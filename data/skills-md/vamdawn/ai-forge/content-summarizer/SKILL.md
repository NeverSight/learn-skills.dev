---
name: content-summarizer
description: "Fetch, analyze, and summarize web content into structured Obsidian notes. Supports articles, GitHub repositories, and Reddit/HN/Twitter threads. Automatically detects URL type and selects the appropriate fetcher strategy and note template. Triggers include requests like 'summarize this article', 'take notes on this', 'save this repo', 'summarize this thread', or any URL-based request intended to be saved as an Obsidian note."
argument-hint: "[url]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3 *), Bash(mkdir *), Bash(curl *), Bash(gh *), Bash(agent-browser *), Skill(agent-browser *), WebFetch
---

始终按以下七步工作流执行。每一步必须完成后才能进入下一步。

## 工作流

### Step 0: 识别内容类型

若 `$ARGUMENTS` 为空（用户未提供 URL），询问用户提供 URL 后再继续。

**多 URL 处理** — 若 `$ARGUMENTS` 包含多个 URL（用户希望合并总结）：
1. 从中提取所有 URL，对每个 URL 分别运行检测脚本
2. 确定一个主类型（以主要内容的类型为准，如一篇博客 + 一条推特讨论 → 主类型为 `article`）
3. 在 Step 1 中分别抓取每个 URL 的内容
4. 在 Step 2 中整合分析，生成一篇合并笔记，在笔记中为每个来源标注原始链接

**必须运行检测脚本** — 使用 Glob 定位本 skill 目录下的 `scripts/detect_content_type.py`，然后用 `python3` 运行该脚本并传入 URL 作为参数（多 URL 时对每个 URL 分别调用）。不得跳过此步骤手动判断类型。脚本返回 JSON，包含 `type`、`platform`、`fetcher`、`template`、`metadata` 字段。脚本根据 URL 模式匹配返回 `references/fetchers/` 下对应的策略文件路径和 `references/templates/` 下对应的模板路径；未匹配已知平台时默认返回通用策略。

记录脚本返回的所有字段，进入 Step 1。若脚本执行失败或返回无法解析的结果，回退到默认值：`type=article`、`fetcher=references/fetchers/common.md`、`template=references/templates/article.md`。

### Step 1: 抓取内容

先用 Glob 将 `fetcher`（相对路径）解析为 skill 目录内的**唯一绝对路径**，再用 Read 读取该绝对路径对应文件，遵循其中的**抓取策略**获取内容。严格按策略中的优先级顺序尝试，首选方案失败后再尝试下一个。

若 `fetcher` 解析失败（0 个或多个匹配），回退到 `references/fetchers/common.md` 并重复“Glob 解析绝对路径 → Read”流程；仍无法唯一定位时终止并报告错误。

平台专用抓取规则（如 Twitter/X）只在对应 `references/fetchers/*.md` 中维护；主 `SKILL.md` 不重复定义。读取到专用 fetcher 后，必须完整执行其“抓取策略”“验证门”和字段映射约定。

所有类型均需估算阅读元数据：
- `word_count` — 大致字数（中文按字数，英文按 word count）
- `reading_time` — 预估阅读时长（中文 300 字/分钟，英文 200 words/min，向上取整，格式 `"N min"`）
- `difficulty` — 内容难度：`beginner`（无需背景知识）、`intermediate`（需要一定领域了解）、`advanced`（需要深度专业知识）

**抓取失败时**（URL 不可达、404、paywall、内容为空）：
- 告知用户失败原因
- 请用户手动提供内容（粘贴文本或提供替代 URL）
- 获得内容后继续 Step 2

**验证门**：确认已获取到有效的正文内容后才能进入 Step 2。如果抓取结果为空或仅含导航/广告文本，视为抓取失败。

### Step 2: 分析与摘要

遵循 Step 1 已读取的 fetcher 文件中的**分析策略**和**评分解读**处理内容。

所有类型均需完成：

**2a. 提取核心信息** — 按类型特定的策略提取

**2b. 生成一行摘要**（`description` 字段）— 用于 frontmatter、索引条目和快速浏览的单句摘要

**2c. 评分** — 按三个维度（1-5 分）评估内容：

| 维度 | 1（低） | 3（中） | 5（高） |
|:-----|:--------|:--------|:--------|
| **novelty** | 广为人知的常见知识 | 有部分新角度或新组合 | 全新观点或鲜为人知的信息 |
| **quality** | 缺乏论据、逻辑松散 | 论证基本完整但不算深入 | 论证严密、证据充分、来源权威 |
| **actionability** | 纯理论/纯新闻，无可执行要点 | 有一些可参考的建议 | 提供具体步骤/代码/工具可直接应用 |

各维度在不同内容类型下的具体解读见对应 fetcher 文件的"评分解读"section。

计算 `overall_score` 为三项评分的四舍五入均值。根据 `overall_score` 确定 `recommended_action`：
- `deep_read`: overall_score ≥ 4
- `skim`: overall_score = 3
- `reference`: overall_score = 2
- `archive`: overall_score ≤ 1

以用户语言输出摘要（用户使用中文时默认中文）。

### Step 3: 确定输出路径

**发现输出根目录** — 扫描目录树，定位存放笔记的目录（查找 frontmatter 中含 `source:` 的 Markdown 文件所在目录，或名称暗示内容集合的目录）。如有多个候选或找不到，询问用户。

**分类目录发现（动态推断）：**

1. 扫描输出根目录下的现有子目录，推断命名惯例
2. 将内容匹配到现有分类子目录
3. 需要时创建新分类，遵循现有命名惯例
4. 用户显式指定路径时优先使用

### Step 4: 写入 Obsidian 笔记

**4a. 读取模板** — 先用 Glob 将 `template`（相对路径）解析为 skill 目录内的**唯一绝对路径**，再用 Read 读取模板文件，确保笔记结构严格匹配模板。不得凭记忆构建笔记结构。若 `template` 为 null，根据判断的类型选择：
- `article` → `references/templates/article.md`
- `repo` → `references/templates/repo.md`
- `thread` → `references/templates/thread.md`

若模板路径解析失败（0 个或多个匹配），按上面的类型默认值回退，并重复“Glob 解析绝对路径 → Read”流程；仍无法唯一定位时终止并报告错误。

**4b. 标签对齐** — 写入笔记前，用 Grep 搜索 vault 中所有 frontmatter tags（搜索模式 `^  - ` 在 `*.md` 文件中），收集已有标签集合。为新笔记选择标签时：
- 优先复用已有标签（如 vault 中已有 `架构` 则不创建 `软件架构`）
- 仅在确认无近义已有标签时才创建新标签

**4c. 写入笔记** — 遵循所选模板的结构、callout 用法和适配规则。如果项目的 CLAUDE.md 要求使用 `obsidian-markdown` skill，该 skill 提供基础格式规范，笔记模板在其上叠加内容特定结构。

**个人反思 section**：用对话上下文（用户为什么分享此内容、正在做什么）草拟初始条目。上下文不足时留占位提示。

**多媒体处理**：遵循 `references/templates/article.md` 中的"多媒体处理"指南。

保存笔记到 Step 3 确定的分类子目录。

### Step 5: 构建索引

将新笔记整合到 vault 的索引系统：

1. **确保索引文件存在** — 在分类子目录中查找已有的 `*INDEX*` 或 `*index*` 文件确定命名模式。如不存在，按 [references/templates/index.md](references/templates/index.md) 创建。

2. **添加索引条目** — 格式：`` - `YYYY-MM-DD` [[Title]] - description ``。按发布日期排序（最新在前）。`publish` 不可用时回退到 `creation` 日期。

3. **正向链接** — 在笔记正文中，用 `[[wikilinks]]` 链接到 vault 中已有的相关概念笔记。具体操作：
   - 用 Grep 在 vault 中搜索笔记涉及的关键概念词（如技术名词、方法论名称）
   - 找到匹配的已有笔记后，在正文相关位置插入 `[[wikilink]]`
   - 未找到匹配时不必创建新笔记，仅链接已有的

4. **反向链接** — 在 1-3 个最相关的已有笔记中，添加指向新笔记的 wikilink。具体操作：
   - 用 Grep 搜索 vault 中与当前内容主题相关的笔记（搜索关键词、相同标签）
   - 在找到的相关笔记中，选择最合适的位置（如"相关阅读"、"推荐资源"、"个人反思"的关联部分）追加链接
   - 如果找不到明显相关的已有笔记，跳过此步骤而非强行添加

5. **更新 MOC** — 在输出根目录的父级查找 `*MOC*` 文件（如 `0_Resources_资源库_MOC.md`）：
   - 在"最近收录"列表顶部插入新条目，格式：`` - `YYYY-MM-DD` [[Title]] ``，按该 MOC 文件中明确标注的列表长度要求保持条目数量，未明确标注时默认不超过 10 条（移除最旧的）
   - 更新分类统计表格中对应分类的篇数（重新计算该分类 INDEX 文件中的条目数）
   - 如果是新分类（表格中不存在），在表格末尾追加一行
   - 如果未找到 MOC 文件，跳过此步骤

### Step 6: 质量核验

逐项检查以下清单。发现遗漏时立即修复，全部通过后才算完成。

- [ ] Frontmatter 完整：tags, type, source, authors, publish, creation, date_saved, word_count, reading_time, difficulty, status, novelty, quality, actionability, overall_score, recommended_action, description
- [ ] 阅读元数据存在：word_count, reading_time, difficulty
- [ ] AI 评分存在：novelty, quality, actionability, overall_score, recommended_action
- [ ] 内容类型正确识别（article / repo / thread）
- [ ] 笔记正文结构匹配内容类型的模板（Step 4a 已读取模板确认）
- [ ] Tags 与 vault 已有标签对齐（Step 4b 已搜索确认）
- [ ] TL;DR 紧跟标题下方，与 frontmatter 的 `description` 一致
- [ ] 原始链接存在于 TL;DR 上方
- [ ] 核心观点捕捉了逻辑关系，而非孤立要点
- [ ] 个人反思 section 已填充或有可操作的占位提示
- [ ] 有效的 Obsidian 语法（callouts, wikilinks, highlights）
- [ ] 语言与用户语言一致
- [ ] 笔记保存在正确的分类子目录
- [ ] 索引条目已添加
- [ ] 正向 wikilinks 指向 vault 中已有笔记（或确认无匹配）
- [ ] 反向链接已添加到相关已有笔记（或确认无匹配）
- [ ] MOC 已更新：最近收录列表和分类篇数（若 MOC 存在）
