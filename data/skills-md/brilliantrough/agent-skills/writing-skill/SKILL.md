---
name: writing-skill
description: 把反复出现的经验、对话结论或踩坑固化成可移植的 skill，或在既有 skill 上增删改查。Use when asked to 写个skill/固化成skill/沉淀成skill/把这个流程做成skill，when a lesson keeps being retaught across sessions or machines，or when reviewing or trimming an existing skill. 判定"该进 skill 还是记忆"是第一步；算力平台四层落盘走 accel-skill-template，中文行文风格走 readable-docs，本机事实去情境化后回流前跑 platform-environment-skill-audit。
---

# writing-skill：把经验写成可移植的 skill

## 1. 先判定：这内容配不配做 skill

| 判定 | 去处 |
| --- | --- |
| 跨机器/跨项目会重复的**方法**（怎么做、怎么避坑） | skill |
| 只对本机/本项目成立的**事实**（路径、版本、状态） | 记忆系统或 host 层文档，不是 skill |
| 一次性任务、还没第二次发生 | 什么都不写，等它重复 |
| agent 本来就会的通识 | 不写；skill 只写它不知道的差异点（确切键名/命令/版本行/坑） |

混了本机事实的通用方法 → 写成 skill 时占位符化（`{{路径}}`），本机值进 host 层或记忆；platform-environment-skill-audit 管回流的脱敏底线。

## 2. 定形（写之前想清楚）

- **命名**：kebab-case，动词或名词短语，≤64 字符，目录名=name；前缀可对齐家族（exp-*、accel-*）。
- **放哪**：仓库 base 组（全机型通用）/ accel 组（算力场景）/ 本机 `~/.agents/skills/`（只此一机）。进仓库的记得进 setup 脚本对应名单（selfcheck 会查）。
- **分工**：与相邻 skill 的边界一句话写进 description（"装环境用 X，写代码用本 skill"），避免双触发或都不触发。
- **演化性质（写时定档，多数 skill 会演化）**：三档——①**经验演化型**（kb-*、personal-ui-taste）：实机/使用经验持续流入，skill 内要有演化说明：什么触发更新、更新什么、怎么回流（知识类记日期与证据，品味类记 evolution 事件）；②**事实冻结型**（accel 三件套）：装时特化一次，之后不动，靠"当日回流"交棒；③**固定指令型**：一次性流程，无演化，过期即废弃。档位不同，安装策略也不同（演化型可覆盖刷新，冻结型只装一次）。

## 3. description（决定生死的字段）

- 第三人称或祈使，**what + when + 触发词**：做什么、什么时候用、用户会怎么说到它（含中文口语触发词）。
- 只写触发所需，不写实现细节；≤1024 字符。
- 反例："处理文件"（不命中任何话术）；正例："Extract text and tables from PDF files. Use when working with PDF files or when the user mentions PDFs, forms"。

## 4. 正文（高熵、直白、引导强）

- **上限 ~150 行**；每行都该是活的——删掉任何一行 skill 都变差才算合格（sprawl 是失败模式：注意力随行数摊薄）。
- **steps 与 reference 分开**：步骤内联在 SKILL.md；查表类、只有部分分支才需要的推到同目录附属文件，指针只一层深。
- **每步有完成判据**：这步做完的标志是什么（可观察的输出/状态），没有判据的步骤是废话步骤。
- **自由度按脆弱性给**：易错处给精确命令（照抄可跑），判断处给启发式一句话；不要给菜单让 agent 自己挑。
- **细节=差异点**：确切命令、键名、版本行、真实踩过的坑（症状→原因→处置）；砍掉概念解释、背景介绍、"请注意"。
- **leading words**：同一概念在三处重复叙述 → 收敛成一个引导词；每个多余句子都是下次维护的债。
- **时效内容带日期**（版本行、矩阵），未验证的标 `(未验证)`；不写死会过期的结论而不给重查命令。
- 中文为主（readable-docs 的风格规则适用：短语、分点、表格、直白）。

## 5. 收尾检查（写完自查）

1. **触发测试**：拿 2–3 句真实用户话术模拟，description 会不会命中？相邻 skill 会不会抢？
2. **熵检查**：通读一遍，删掉纯解释性句子后剩下的才是信息量；解释比代码长就删解释。
3. **去情境化检查**：grep 本机痕迹（用户名/主机路径/IP），该占位符的占位符。
4. **首次真用**：skill 的价值在第二次被触发时验证；用歪了改 description，用漏了补触发词，别预先设计用不到的分支（YAGNI）。

## 6. 演化

固定回路（演化发生地＝真机）：服务器上直接改本机副本 → 下载到开发机 → 合入仓库 push → 各机拉新版（覆盖刷新组自动、只装一次组显式重装）。最小修改落回 skill 本体，不改结构；规则被推翻时更新对应小节并注明证据。各档协议：知识类（kb-*）按其「演化」节记日期+证据；算力平台类走 accel-skill-template 落盘规则；品味类走 personal-ui-taste evolution 协议。坑：本机副本有未回流修改时别重跑 setup 的覆盖刷新（会冲掉）。
