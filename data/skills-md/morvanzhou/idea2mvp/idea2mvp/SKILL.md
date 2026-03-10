---
name: idea2mvp
description: "Discover product ideas, validate them, and build MVPs. Search trending tools across Product Hunt, GitHub, Indie Hackers, XiaoHongShu, V2EX, SSPAI, etc. Validate feasibility via market research and competitive analysis. Build MVPs. Send reports via email. Triggers: 'find ideas', 'search products', 'trending tools', 'product ideas', 'validate my idea', 'build MVP', 'market research', 'competitive analysis', 'indie hacker', 'send email', '找想法', '搜产品', '找灵感', '产品调研', '验证想法', '构建MVP', '发邮件', '发送报告'."
---

# Idea → MVP：从灵感发现到产品落地

## Overview

本 skill 覆盖产品从 0 到 1 的完整流程：**发现灵感 → 验证想法 → 实现 MVP**。全程使用中文输出。

用户可以从任意阶段切入：
- 没有想法 → 从阶段一开始
- 已有想法需验证 → 从阶段二开始
- 想法已验证想动手 → 从阶段三开始

## Runtime Data — 运行时数据目录

本 skill 遵循 **skill 源码与运行时数据分离** 的原则：

- **Skill 源码**（`SKILL.md`、`scripts/`、`references/`）保持不可变，可安全分享和版本管理。
- **所有可变状态**（配置、搜索结果、用户数据、缓存）统一存放在项目根目录的 `.skills-data/idea2mvp/` 下。

```
<project_root>/.skills-data/idea2mvp/
    .env            — 配置文件（Token、搜索偏好、邮件 SMTP 等）
    data/           — 持久化数据
        search-results/ — 各平台搜索结果（ph_results.txt、github_results.txt 等）
        idea-brief/      — 灵感确认文档（按时间戳归档）
        user-profile.md、报告等
    cache/          — 可安全删除的缓存（如小红书浏览器登录数据）
    logs/           — 日志文件
```

**路径约定**：
- 配置文件路径：`.skills-data/idea2mvp/.env`
- 搜索结果目录：`.skills-data/idea2mvp/data/search-results/`
- 用户画像文件：`.skills-data/idea2mvp/data/user-profile.md`
- 灵感确认文档：`.skills-data/idea2mvp/data/idea-brief/{YYYY-MM-DD_HHmm}.md`（每次生成带时间戳）
- 历史推荐记录：`.skills-data/idea2mvp/data/seen-tools.jsonl`（跨会话去重，自动过期）
- 浏览器缓存：`.skills-data/idea2mvp/cache/xhs_browser_data/`

**Git 忽略**：在 `.gitignore` 中添加 `.skills-data/` 即可忽略所有 skill 运行时数据。

**⚠️ 凭证安全原则**：所有 Token、密码等敏感配置统一存放在 `.skills-data/idea2mvp/.env` 中，由脚本内部调用 `load_env()` 自动读取。**严禁在命令行中内联传递凭证**（如 `TOKEN=xxx python3 scripts/...`），这会导致敏感信息泄露到终端历史和日志中。

**⚠️ 脚本执行规范**：所有 Python 脚本通过环境变量 `PROJECT_ROOT` 确定项目根目录（即 `.skills-data/` 的创建位置）。执行脚本时**必须传入 `PROJECT_ROOT`**，格式为：

```bash
PROJECT_ROOT=/path/to/project python3 scripts/xxx.py [参数]
```

> `PROJECT_ROOT` 不是敏感信息，写在命令行中没有安全问题。如果未传入，脚本会 fallback 到 `cwd`，但当 agent 将工作目录切换到 skill 源码目录时会导致 `.skills-data/` 被错误创建在 skill 目录下。因此**必须显式传入**。

## 三阶段工作流

### 阶段一：灵感发现（Find Ideas）

**目标**：通过多平台搜索，发现近期流行的实用小工具和独立产品，提炼痛点并生成可拓展的产品 Ideas。

**执行**：读取 `references/find-ideas.md`，按照其中的搜索策略、筛选标准、Idea 扩展方法和报告模板执行。在与用户讨论的过程中，留意用户透露的行业背景、产品偏好、技术经验等信息，记录到 `.skills-data/idea2mvp/data/user-profile.md`。

**核心步骤**：
1. **了解用户背景**：先读取 `.skills-data/idea2mvp/data/user-profile.md`（如存在），根据用户的行业经验、技术背景、产品偏好等针对性调整搜索关键词和搜索范围。如不存在则按默认关键词执行
2. **确认搜索偏好**：检查 `.skills-data/idea2mvp/.env`，如未配置偏好则询问用户：是否配置 Product Hunt Token 以使用 API 搜索？是否使用 Playwright 控制浏览器搜索小红书？用户选择跳过的数据源会写入 `.skills-data/idea2mvp/.env`（`SKIP_PH_API=true` / `SKIP_XHS_PLAYWRIGHT=true`），后续自动跳过不再询问。注意：小红书未开放公网搜索，跳过 Playwright 时直接跳过小红书搜索，不使用 `web_search` 替代
3. 并行搜索 Product Hunt、中文社区（小红书/V2EX/少数派）、Indie Hackers、独立开发者社区、GitHub Trending
4. **跨会话去重**：运行 `PROJECT_ROOT=<项目根目录> python3 scripts/seen_tools.py read` 获取最近 90 天已推荐工具列表，筛选时跳过这些工具
5. 筛选 5-8 个最有启发性的工具，深度分析痛点和模式
6. 生成 5 个可拓展的产品 Ideas
7. 输出完整的工具探索报告，并运行 `PROJECT_ROOT=<项目根目录> python3 scripts/seen_tools.py add` 将本次推荐的工具追加到去重记录

**阶段输出**：工具探索报告（含工具推荐 + 产品 Ideas + 趋势洞察）。

**阶段过渡**：报告输出后，与用户深入讨论感兴趣的 Idea 方向。沟通完成后，询问用户是否生成一份**灵感确认文档**（Markdown 文件），内容包括：
- 用户选定或倾向的 Idea 方向
- 用户在沟通中表达的产品偏好、行业经验、个人优势
- 用户关心的关键问题和顾虑
- 讨论中产生的新想法或调整

此文档作为阶段二的输入上下文，确保验证阶段能延续阶段一的沟通成果，避免有价值的对话信息丢失。文件保存至 `.skills-data/idea2mvp/data/idea-brief/{YYYY-MM-DD_HHmm}.md`，文件名即时间戳，方便后续回溯查看。

---

### 阶段二：想法验证（Validate Ideas）

**目标**：通过结构化的多步骤流程验证想法的可行性，以交互式咨询的方式逐步推进。

**执行**：**先读取 `.skills-data/idea2mvp/data/user-profile.md`**（如存在），了解用户的行业背景、技术经验和认知水平，据此调整沟通深度和验证侧重点。然后读取 `references/validate-ideas.md`，按照其中的七步验证流程执行，每个环节都需要和用户确认信息，让用户参与评价和决策。评分时参考 `references/evaluation-framework.md`。沟通过程中持续将用户表现出的认知水平、行业见解、技术倾向等信息更新到 `.skills-data/idea2mvp/data/user-profile.md`。

**七步流程概览**：
1. **想法澄清** — 通过反向提问帮用户厘清产品概念
2. **市场调研** — 搜索竞品、分析市场格局和空白点
3. **需求验证** — 在社区中验证真实需求和付费意愿
4. **技术可行性** — 评估技术栈、MVP 范围和开发周期
5. **商业模式** — 设计盈利模式和获客策略
6. **风险评估** — 识别致命风险和应对方案
7. **综合评分** — 五维度评分 + 最终建议 + 行动计划

**关键机制**：
- 每步完成后输出阶段文档，等用户确认后再推进
- 发现根本性障碍时触发 **Idea 扩展机制**（参考 `references/idea-expansion.md`），不简单否定，而是提出替代方向
- 用户可在任何阶段决定放弃或转向

**阶段输出**：可行性评估报告（参考 `assets/report-template.md`）。

若建议推进，询问用户是否进入阶段三。

---

### 阶段三：实现 MVP（Build MVP）

**目标**：基于验证结果，用用户能理解和维护的技术方案，规划并实现最小可行产品。

**执行**：读取 `references/build-mvp.md`，按照其中的 MVP 实现流程执行。**必须先读取 `.skills-data/idea2mvp/data/user-profile.md`**，根据用户技术背景选择技术栈和沟通方式。涉及前端界面开发时，读取 `references/frontend-design.md`，按照其中的设计规范产出有辨识度的界面。

**核心步骤**：
1. **了解技术背景** — 读取 `.skills-data/idea2mvp/data/user-profile.md`，如信息不足则主动询问用户的技术经验，确认用户能接受的交付形式
2. **确认 MVP 范围** — 基于阶段二的技术评估，锁定核心功能列表（只做必须的）
3. **技术方案设计** — 优先选择用户熟悉的技术栈；如需使用用户不熟悉的技术，在用户能理解的层度上解释为什么需要、怎么用
4. **逐步实现** — 按功能模块逐步编码实现，每完成一个模块与用户确认
5. **运行指引** — 提供用户能独立操作的启动步骤，确保用户能把 MVP 跑起来
6. **部署准备** — 提供部署方案和上线建议

**阶段输出**：可运行的 MVP 代码 + 用户能看懂的启动/部署指引

---

## 工具使用

- **`web_search`**：阶段一搜索工具/趋势，阶段二搜索竞品/社区讨论/市场数据
- **`agent-browser`**：深入访问产品页面、社区帖子、用户评价。（如未安装，先执行：`npx skills add https://github.com/vercel-labs/agent-browser --skill agent-browser` 安装 skill）.
- **代码编辑工具**：阶段三实现 MVP

## 用户画像文件（贯穿全流程）

在三个阶段的对话过程中，持续维护一份 **`.skills-data/idea2mvp/data/user-profile.md`** 文件，记录从对话中了解到的用户信息：

- **技术背景**：熟悉的编程语言、框架、工具链，技术水平自评
- **行业经验**：所在行业、工作角色、相关领域经验
- **认知水平**：对产品、市场、商业模式等概念的理解程度
- **资源条件**：可投入时间、预算、团队情况
- **偏好与风格**：沟通偏好、决策风格、风险偏好

**信息采集方式**：
- **不要专门盘问用户**，而是在自然对话中捕捉。例如：用户说"我之前用 Python 写过爬虫"→ 记录技术背景；用户问"什么是 LTV"→ 记录认知水平；用户说"我是设计师"→ 记录行业经验
- 阶段一讨论 Idea 时，用户的选择倾向、关注点、提问方式都能反映其背景
- 阶段二验证过程中，用户对技术方案、商业模式的反应能进一步补充画像
- 只在阶段三信息明显不足时才主动询问技术背景

**使用规则**：
- 在任何阶段的首次交互时，检查是否已存在 `.skills-data/idea2mvp/data/user-profile.md`，如存在则先读取
- 每当从对话中捕捉到新的用户背景信息，及时追加更新（不需要征求用户同意）
- 当需要向用户解释技术概念、商业术语或做方案推荐时，先读取此文件，在用户能理解的认知层度上沟通
- 阶段三选择技术栈时，必须读取此文件，优先使用用户熟悉的技术

> 所有 `user-profile.md` 的路径统一为 `.skills-data/idea2mvp/data/user-profile.md`。如项目根目录下已有旧版 `user-profile.md`，首次读取时将其迁移到新路径。

## 交互规范

1. **开场**：判断用户意图，引导到对应阶段
2. **语言**：全程中文
3. **态度**：专业、客观、有建设性，用数据和事实说话
4. **阶段过渡**：明确告知进度，征求用户意见后再推进
5. **适配用户**：解释和沟通的深度应匹配用户的技术和认知背景（参考 `.skills-data/idea2mvp/data/user-profile.md`）

## Bundled Resources

### references/

- **`references/find-ideas.md`** — 灵感发现的完整执行指南：搜索策略、关键词模板、筛选标准、Idea 扩展思维框架、报告输出模板。阶段一使用。
- **`references/validate-ideas.md`** — 想法验证的七步流程详细指南：每步的目标、执行步骤和输出模板。阶段二使用。
- **`references/idea-expansion.md`** — Idea 扩展与延伸方法论：底层模式提炼、问题诊断、场景迁移、替代方向生成。阶段二中发现障碍时使用。
- **`references/evaluation-framework.md`** — 评估框架：五维度评分标准、盈利模式参考、获客渠道对比、MVP 验证方法论。阶段二评分时使用。
- **`references/build-mvp.md`** — MVP 实现指南：用户技术背景适配、范围确认、技术方案设计、编码实现流程、分层运行指引、部署方案。阶段三使用。
- **`references/frontend-design.md`** — 前端设计规范：设计思考流程、字体/色彩/动效/构图/背景的视觉标准、实现原则。阶段三涉及前端界面时使用。
- **`references/send-email.md`** — 邮件通知使用指南：配置方式、脚本用法。当用户要求将某些信息通过邮件发送时，按此指南执行。

### assets/

- **`assets/report-template.md`** — 可行性评估报告模板。阶段二最终输出使用。

### scripts/

- **`scripts/producthunt_trending.py`** — 通过 Product Hunt 官方 API v2 获取热门产品。需在 `.skills-data/idea2mvp/.env` 配置 `PRODUCTHUNT_TOKEN`。若用户设置了 `SKIP_PH_API=true` 则跳过脚本，改用 `web_search`。
- **`scripts/github_trending.py`** — 通过 GitHub Search API 搜索近期热门工具类项目。支持按天数、星数、语言、主题过滤。无需 Token。阶段一搜索 GitHub 时优先使用。
- **`scripts/v2ex_topics.py`** — 通过 V2EX 公开 API 获取热门/最新话题。无需认证。支持关键词过滤和工具话题筛选。阶段一搜索中文社区时优先使用。
- **`scripts/xiaohongshu_search.py`** — 使用 Playwright 自动化浏览器搜索小红书笔记。模拟真人操作（搜索 → 逐个点入详情页提取完整内容），需首次扫码登录。若用户设置了 `SKIP_XHS_PLAYWRIGHT=true` 则直接跳过小红书搜索（小红书未开放公网搜索，搜索引擎无法抓取）。Playwright 依赖通过 `pip install playwright` 安装。
- **`scripts/sspai_search.py`** — 通过少数派搜索 API 获取工具/产品相关文章。无需认证。支持单/多关键词搜索，自动去重、按点赞数排序。还支持 `--detail <id>` 获取文章完整正文内容。阶段一搜索中文社区时优先使用。
- **`scripts/indiehackers_search.py`** — 通过 Indie Hackers 内置的 Algolia 搜索 API 获取独立开发者产品。无需认证。返回产品名称、月收入、领域标签、商业模式等。支持 `--min-revenue` 过滤低收入产品。阶段一搜索英文独立开发者社区时优先使用。
- **`scripts/send_email.py`** — 通过 SMTP 发送邮件通知。可将搜索报告或任意文本内容发送到指定邮箱。支持从 `--body`、`--file`（多文件合并）或 stdin 传入内容。需在 `.skills-data/idea2mvp/.env` 中配置 `EMAIL_SMTP_HOST`、`EMAIL_SENDER`、`EMAIL_PASSWORD`、`EMAIL_RECEIVER`。仅使用 Python 标准库，无额外依赖。发送前，先将生成的 Markdown 内容保存到 `.skills-data/idea2mvp/cache/` 目录，再通过 `--file` 传入发送。
- **`scripts/seen_tools.py`** — 已推荐工具的去重记录管理。`read` 子命令返回最近 N 天（默认 90）的历史推荐并自动清理过期条目；`add` 子命令追加新记录。存储格式为 JSON Lines（`.skills-data/idea2mvp/data/seen-tools.jsonl`）。阶段一生成报告前后使用。

