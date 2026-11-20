---
name: agy-cmd
description: Google Antigravity 桌面端与 IDE 高阶能力自动路由器与内置斜杠指令参谋。当用户开启或关闭全局自动路由、询问某任务该敲什么内置指令、对比相近指令（如 /grill-me 与 /plan、/goal 与 /boost 或 /run-workflow），或遇到模糊新需求、多文件复杂改动、批量同质语义任务与反复未修好的疑难故障需要匹配反重力原生工具与斜杠指令时使用；严禁混入终端 CLI 专属命令。
---

# agy-cmd：高阶能力自动路由器与内置指令参谋

谷歌反重力（Antigravity）把许多高阶开发能力（需求单题追问、先审施工图、多智能体并发脚本、三层深度推演等）分散在 19 个内置斜杠指令与底层工具中。本 Skill 提供两项核心服务：

1. **全局自动路由管理与双轨调度**：通过内置脚本一键安装 `~/.gemini/config/rules/agy-auto-router.md`（`trigger: always_on`），让所有新对话在用户不敲斜杠指令时自动调起对应的原生底层能力，并在前端专属模式场景下首行提示可复制命令；
2. **极简指令选型参谋与分类速查**：当用户主动描述任务求推荐指令，或查询桌面端指令区别与清单时，零反问直接交付带 `@` 挂载的可复制命令块与近邻排他理由。

## 关键不变量

1. **双轨分工清晰**：凡是 Agent 拥有原生底层工具的能力（`ask_question` 单题追问、`Implementation Plan` 先审后改、`run_workflow` 并发编排、`swarm` 留言板协作、`browser` 子智能体、`generative_ui` 可视化），在用户直接派活时**当场自动调用执行**，不退化为光说不练；凡是仅限前端输入框触发的外层模式（`/boost`、`/goal`、`/teamwork`、`/compact`、`/btw`），在推进分析的同时于首行给出可复制命令。
2. **轻量任务零打扰**：1～2 个文件的明确局部修改、普通问答、以及可用 `rg` 或简短本地脚本秒级完成的确定性字符查找，直接执行，不强塞实施方案或推销斜杠指令。
3. **严守桌面端与 IDE 纯净边界**：禁止推荐任何终端 `agy` CLI 专属指令（如 `/undo`、`/rewind`、`/branch`、`/fork`、`/clear`、`/new`、`/resume`、`/switch`、`/effort`、`/codesearch`、`/diff`、`/statusline`、`/title`、`/voice`、`/exit`）。桌面端被问及撤回或分叉时，如实指路界面历史回退按钮、Review Changes 面板或 `@历史会话`。
4. **选型模式零反问**：用户求推荐指令时，信息充足直接给 1 个最优可复制命令；缺前提时并列给 A/B 两条条件分支命令，禁止停下来反问，也不主动出题考核。

## 工作流程

### 模式 A：开启、查看或关闭全局自动路由

当用户说“开启自动路由”“安装自动触发规则”“检查 `agy-cmd` 有没有全局生效”或“关闭自动路由”时，运行内置脚本 [scripts/setup_auto_router.py](scripts/setup_auto_router.py)：

- **开启并同步桌面端全局规则**（需向用户说明将在 `~/.gemini/config/rules/agy-auto-router.md` 写入常驻规则）：
  ```bash
  python scripts/setup_auto_router.py --install
  ```
- **查看当前状态**：
  ```bash
  python scripts/setup_auto_router.py --status
  ```
- **一键移除并恢复默认**：
  ```bash
  python scripts/setup_auto_router.py --remove
  ```

安装完成后告知用户：新开任意对话窗口即可 100% 自动生效，无需每次手动敲 `/agy-cmd`。

### 模式 B：日常开发任务双轨自动调度

依据：Sheridan & Verplank 自动化分级模型与分面分类法。

当用户在普通任务中直接派活且命中以下高阶场景时，按对应轨道直接行动：

| 任务特征 | 调度轨道 | Agent 立即执行的动作 |
| --- | --- | --- |
| 新功能或新工具只有模糊方向，核心规则与边界未定 | **自动代执行**（同 `/grill-me`） | 禁止猜需求硬写代码或一次抛多题问卷；调用 `ask_question` 每次只问 1 个关键决策问题并置顶 `(Recommended)` 推荐项，逐步追问对齐 |
| 目标明确，但预计改动 3 个及以上文件或调整核心架构 | **自动代执行**（同 `/plan`） | 先只读扫描相关代码与依赖，创建带 `RequestFeedback: true` 的 `Implementation Plan` 产物，获用户批准前不修改业务代码 |
| 对 5 个及以上文件或目录执行需大模型语义理解的同质检查/改造 | **自动代执行**（同 `/run-workflow`） | 先读取内置 `run-workflow` Skill，调用 `run_workflow` 工具编写 Python `parallel()` 脚本并发处理（纯正则/字符查找除外，直接用本地命令） |
| 2～4 个独立模块并行开发且需专门测试员验收 | **自动代执行**（同 `/swarm`） | 读取内置 `swarm` Skill，使用 `swarm` 工具组织 Worker 与 Verifier 协作 |
| 需点击操作动态网页、查线上渲染数据或截图验 UI | **自动代执行**（同 `/browser`） | 直接委派 `browser` 子智能体执行 |
| 同一疑难 Bug 已修 2 次以上未果、偶发并发死锁或复杂算法优化 | **首行提醒 + 继续排查** | 回复第 1 行提示可复制 `/boost <精炼问题>`（付费计划），同时正常读取提交记录与代码开展排查 |
| 要求无人值守死磕到底修通全部报错与测试、中途别停 | **首行提醒 + 持续执行** | 回复第 1 行提示可复制 `/goal <精炼目标>` 以挂载防停机控制器，同时全力推进当前修复 |

### 模式 C：指令选型参谋与分类速查

依据：Diátaxis 任务与参考分离原则、外在认知负荷消减。

1. **选型处方（用户问“这活该敲什么指令”）**：对照下表静默锁定指令，按 **「首选指令（含套餐提示）→ 带 `@` 挂载的可复制代码块 → 1 句触发效果 → 1 句近邻排他理由（高阶套餐附普通号平替）」** 在 150 字内交付（跨阶段任务给先后两步连招）：
   - 动手前对齐：模糊想法用 `/grill-me`；跨多文件先出方案用 `/plan`。
   - 重活与多智能体：单线死磕用 `/goal`；疑难故障多路推演用 `/boost`（付费计划）；异构分工加质检用 `/swarm`（Pro / Ultra）；同质批处理脚本用 `/run-workflow`（Pro / Ultra）；跨天大迁移用 `/teamwork`（付费计划）。
   - 旁支与工具：顺嘴无痕提问用 `/btw`；长对话浓缩瘦身用 `/compact`；真机操作网页用 `/browser`；内嵌交互图表用 `/generative_ui`（仅桌面端 App）；当前会话定时用 `/schedule`；常驻面板定时用 `/automation`（仅桌面端 App）；纠偏存永久规则用 `/learn`；插件管理用 `/plugin`；编写 `hooks.json` / `mcp_config.json` 规范转交 `/agy-customizations`；外部配置与旧版迁移用 `/migrate-agent-settings`、`/migrate-workflows`；查官方文档用 `/antigravity-guide`。
2. **分类速查或深度辨析（用户问“列一下所有指令”或“X 和 Y 差在哪”）**：先读取 [references/desktop-commands-matrix.md](references/desktop-commands-matrix.md)，再输出结构化对照表。
