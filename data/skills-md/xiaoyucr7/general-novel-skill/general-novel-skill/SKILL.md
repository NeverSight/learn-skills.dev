---
name: general-novel-skill
description: 用于中文网文/网络小说的创作、续写、修订、分析与发布。当用户要开书定位、写大纲或章纲、写章续写日更、写短篇、去AI味或润色修订、导入旧稿、拆文仿写、扫榜调研、准备简介标签封面等上架物料，或需要追踪人物状态、伏笔与时间线、控制节奏、校准文风、中断后恢复进度时使用。
license: MIT
metadata:
  author: 熊小雨
  version: 8.2.0
  mcp_server: mcp_server/server.py
---

# General Novel Skill

把小说工程的文件视为持久记忆，把当前请求路由到最小必要工作流。入口只做路由。
动手前先读 `references/workflow/session-invariants.md`（权威顺序、章事务、ending_mode、失败码、停止点）。
题材、平台与单点工艺按本表加载，不得一次性读取全部参考资料。

## Route the request

先按用户明确动作路由，再看项目状态，最后才用关键词猜测。

| Intent | Required reading |
|---|---|
| 无工程的试写、先写一章看看 | `references/workflow/quick-start.md`；第 1–3 章加读 `references/craft/opening.md`。交付标「草稿，未入事务」，已有工程不得借此绕过章事务 |
| 开书、定位、长篇规划 | `references/workflow/book-init.md`、`references/workflow/outline-system.md` |
| 补纲/改纲、调整未写剧情 | `references/workflow/outline-system.md` → `references/workflow/task-router.md` 的改纲协议；不混入正文修订 |
| 写章、续写、日更 | `references/workflow/chapter-loop.md`、`references/craft/scene-rendering.md`；第 1–3 章加读 `references/craft/opening.md`（硬目标，以及「首句钩子与可测的能力」）。serial 章尾按场景渲染的「连载章尾」，招式见 `references/craft/hooks.md`；授权停在发现上时执行同文件「发现即收」。排除、不在场与能力限制读 `references/craft/character-consistency.md` 的「排除要闭合」 |
| 修订、去 AI 味、解决电报体 | `references/workflow/revision.md`、`references/craft/anti-ai-style.md` |
| 导入旧稿 | `references/workflow/import-book.md`；需要深度反推时再读 `references/workflow/import-deep.md` |
| 中断恢复、状态诊断 | 运行 `python scripts/resume.py "{book}"`，再读 `references/workflow/task-router.md` |
| 质量审核、跨视角复核 | `references/craft/quality-checklist.md`、`references/workflow/cross-review.md` |
| 拆文、仿写 | `references/workflow/deconstruct-pipeline.md`、`references/workflow/imitation.md` |
| 扫榜、市场与联网调研 | `references/workflow/market-scan.md`、`references/workflow/research.md` |
| 短篇创作 | `references/workflow/short-story-loop.md`；结尾专项再读 `references/craft/short-story-ending.md` |
| 平台选择、投稿、发布 | `references/platforms/platform-guide.md` |
| 简介、标签、封面、上架物料 | `references/workflow/publishing-pack.md` |
| Dashboard 工作台、浏览/编辑工程文件 | `references/workflow/dashboard-workbench.md`；按用户授权范围操作 |
| 记住、更正、忘记作者偏好 | `references/workflow/author-preferences.md`；只记录明确授权的创作偏好 |
| 统计分数、图谱证据、旧追踪溢出、评测 | `references/workflow/evidence-review.md` |
| 玄幻、修仙、武道、系统及其他超现实设定的设计/写作/审核 | 在当前动作工作流上加读 `references/craft/fictional-world.md` |

请求组合多个模式、项目状态含糊或依赖不可用时，必须先读
`references/workflow/task-router.md`。题材确定后只加载 `references/genres/INDEX.md` 匹配出的
一张主题材卡；只有交叉题材冲突确实影响当前决策时才补读第二张。

口语说法对不上本表时，查 `references/workflow/commands.md`，只用来找对应关系。

### Load on demand

下表的资料不属于任何路由的必读项，只在出现对应需要时加读一篇，不成批加载。

| 出现的需要 | 加读 |
|---|---|
| 脑洞还没成形、作者不知道写什么 | `references/workflow/ideation.md`，产出创意种子后回到开书流程 |
| 规划百万字以上体量、担心中期无内容可写 | `references/workflow/book-scaling.md` |
| 扫榜后要一份结构化的选题决策报告 | `references/workflow/market-scan-deep.md` |
| 拆文产物的目录与文件格式 | `references/workflow/deconstruct-output-spec.md`；多本对标并存时再读 `references/craft/cross-book-recall.md` |
| 把一本书的文风复用到另一本 | `references/workflow/style-library.md` |
| 短篇投稿的导语、开头与付费断点 | `references/platforms/short-submission.md` |
| 智斗、计谋博弈场景 | `references/craft/wit-battle.md` |
| 反转设计 | `references/craft/reversal.md` |
| 打脸、升级、拉情绪、悬疑揭秘等桥段的分步写法 | `references/craft/genre-formulas.md` |
| 女频读者偏好与感情线 | `references/craft/female-channel.md` |
| 改编已有素材、排查长篇自我重复 | `references/craft/adaptation-method.md` |
| 连载中章首开法雷同或各章语气过于均一 | `references/craft/chapter-entry-modes.md`、`references/craft/novelist-personas.md` |
| 校准文风指纹与机器闸口的阈值 | `references/craft/corpus-baseline.md` |
| 给章节建结构化元数据侧车 | `references/craft/chapter-meta.md`；可选，生成脚本尚未提供，需要时手写 |

章事务的逐步操作、长篇必要上下文、短篇边界、失败码和交付停止点都在
`references/workflow/session-invariants.md`，不在本入口展开。
