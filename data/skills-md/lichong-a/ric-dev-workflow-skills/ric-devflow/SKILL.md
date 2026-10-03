---
name: ric-devflow
description: 当用户请求软件开发、缺陷修复、项目续作、重构、迁移或基础设施变更时主动使用；先确认宿主、安装范围与同源完整性，按需补齐 DevFlow Skill 和当前平台原生角色，再持续路由四角色交付。解释、一般建议、独立审核或测试、单纯文档与极小无风险编辑不启动完整流程。
---

# RIC DevFlow 入口

本入口负责准备和路由，不是第五个业务角色，不代替 Planner、Reviewer、Tester 或 Implementer，也不授予业务批准。保留用户原任务、约束、已有授权及进度，按以下顺序执行。

1. **任务分类**：范围内完整开发进入完整流程；显式 `ric-devflow-<role>` 或精确角色委派只准备该角色的必要闭包。解释、一般建议、独立只读审核/测试、单纯文档编辑、极小无风险编辑及无关 Skill 请求不隐式启动完整 DevFlow；遵从用户明确选择。
2. **宿主与身份**：依据实际宿主声明、可用工具及原生启动上下文确认 Codex、Claude Code 或 ZCode 和主/子会话；配置目录存在不作身份依据。不明确、不支持或身份矛盾时保留原任务并报告精确缺口。已启动子角色缺件时只回交宿主，不安装、不再派生代理。
3. **安装范围**：记录逻辑 `discovered_path`、可信候选 `source_root` 和 `install_scope`；写入跟随逻辑发现位置或已确认范围，不能由 symlink 的 realpath 反推。仅源码路径且范围未知时，先明确范围再写入。
4. **可用性与缺件守卫**：先检查 `references/bootstrap.md` 及当前动作必要文件可读，未齐备前不打开缺失链接。完整开发检查五 Skill 与当前宿主四原生角色；独立角色仅核验入口、该角色及必要传递引用/配置。已确认同源、安装完整、角色可用时直接路由。能力提示绑定宿主/会话、逻辑来源/范围、源 SHA、当前角色/动作闭包及配置/启用/加载状态，以可信变更信号或一次清单/类型/模式/内容核验确认未变后复用，不重读恢复正文；需要建立提示或补查时只取[同会话能力提示](references/bootstrap.md#同会话能力提示)。miss 本身不联网、安装或建 Root，无 Root 只用会话、已有 Root 仅用 .local，旧调用不代表本次调用；批量核验不等于整包加载。
5. **仅缺件或配置缺口时恢复**：主会话先确认发布源 `https://github.com/lichong-a/ric-dev-workflow-skills`，优先可信完整本地 checkout 或安装记录完整 SHA；无记录只从已确认源取一次候选并固定 SHA，不猜历史、不执行下载代码。逐字核对本次闭包全部现存包文件及类型（含入口）；源/范围不明、候选不完整、定制/异版本、未知文件或断链时保持目标零写入。匹配后才从可信候选源读取 `skills/ric-devflow/references/bootstrap.md` 及当前平台一份参考，预检全部 Skill、原生配置、父目录的冲突/禁用/权限，再排他创建缺项、写前复核、写后读回，中断后重新核对。详细流程见[准备与恢复](references/bootstrap.md)；平台只选 [Codex](references/platforms/codex.md)、[Claude Code](references/platforms/claude-code.md) 或 [ZCode](references/platforms/zcode.md)之一。已启动子角色缺件仅回交宿主，不安装、不派生、不绕过拒绝。
6. **加载核验**：补装或复用后均分别核验文件、宿主加载和实际调用；先看当前会话可用角色信息，再以已获授权的下一次必要交接按需验证，不额外启动四个探测代理。文件与配置正确但目标未加载或当前会话无调用能力时，按[加载与调用核验](references/bootstrap.md#文件加载调用分别核验)立即提醒重启当前 Agent、在同一项目重新调用 Skill，并给出恢复说明；仅缺工具且原因未知时不保证重启解决。其他失败按原原因处理，不重复安装、不伪造调用或 Gate；重启后重验，同一缺口仍在则诊断，不循环提示重启。
7. **角色路由**：准备就绪后才读取目标角色入口。Codex 的 Root Planner 保持直接调度；Claude/ZCode 主会话按[原生平级调用](references/shared/orchestration.md#原生平级调用)转发，唯一 Planner 作决定并写状态，四子角色均不派生代理。无角色工具或目标未加载时报告缺口，不用通用代理冒充。

| 任务 | 准备完成后读取 | Codex 原生 ID | Claude/ZCode 原生 ID |
|---|---|---|---|
| 完整开发或显式规划 | [Planner](../ric-devflow-planner/SKILL.md) | `ric_devflow_planner` | `ric-devflow-planner` |
| 显式或委派审核 | [Reviewer](../ric-devflow-reviewer/SKILL.md) | `ric_devflow_reviewer` | `ric-devflow-reviewer` |
| 显式或委派测试 | [Tester](../ric-devflow-tester/SKILL.md) | `ric_devflow_tester` | `ric-devflow-tester` |
| 单个已批准 Task/实现类 Defect | [Implementer](../ric-devflow-implementer/SKILL.md) | `ric_devflow_implementer` | `ric-devflow-implementer` |

表中未选择角色的链接仅是导航，不是独立角色的安装依赖。加载顺序为任务分类 → 选中角色 → 当前动作的参考章节 → 必要模板/语言/领域材料；不因看到链接递归展开全包。初次准备只核验可用性，后续阶段到达时再读规则；同会话已读且未变的内容复用。包准备完成不改变 G0–G10、职责分离、Spec/测试批准、真实 SHA 绑定、冻结 DAG 或 VERIFIED 到 DONE 条件。
