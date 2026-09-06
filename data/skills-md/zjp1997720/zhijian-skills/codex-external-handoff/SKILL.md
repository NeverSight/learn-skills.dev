---
name: codex-external-handoff
description: 从 WorkBuddy、Claude Code 或其他本地 Agent 无头调用 Codex App Server，创建可见、命名、持久的 Codex Thread，并执行继续追问、状态查询、结果取回、取消和打开。用于复杂研究、跨项目取材、章节审校、确定性工程或重要决策；一次性格式检查和无需保留上下文的小提取继续用 codex exec --ephemeral，Codex 内部组队不走本 Skill。
---

# Codex External Handoff

## 目标

让外部 Agent 把正式任务交给本地 Codex，同时保留后台执行的顺畅和可见 Thread 的监督、恢复与人工接管能力。

## 运行入口

从已安装 Skill 目录调用脚本：

```bash
HANDOFF="skills/codex-external-handoff/scripts/codex_external_handoff.py"
python3 "$HANDOFF" doctor
```

首次使用、Codex 升级或调用失败时先运行 `doctor`。正式任务先读取 [task-package.md](references/task-package.md)；排查协议或兼容问题时读取 [app-server-contract.md](references/app-server-contract.md)。

## 路由

- 需要跨项目检索、复杂研究、架构设计、代码审校、确定性工程、重要判断、继续追问或人工接管：使用本 Skill 创建持久 Thread。
- 输出用完即丢、无需监督、无需追问的格式检查或简单提取：直接使用 `codex exec --ephemeral`。
- Codex 已经是当前宿主且任务只涉及内部多 Agent 分工：使用 Codex 原生团队能力，不经外部交接。

## 执行

1. 形成最小任务包，明确目标、允许读取的范围、禁止事项、证据要求和验收标准。正文较长时写入临时或项目登记的任务文件。
2. 默认以 `read-only + approvalPolicy=never` 创建 Thread。只有任务包明确授权写入并列出目标路径时，才传 `--sandbox workspace-write`；本 Skill 不提供 `danger-full-access`。
3. 创建并立即返回 `job_id`、`thread_id` 和打开地址：

```bash
python3 "$HANDOFF" ask \
  --title "架构设计与方案审查" \
  --task-file /absolute/path/to/task.md \
  --cwd "$PWD" \
  --model gpt-5.6-sol \
  --effort high
```

4. 后台任务用以下命令管理：

```bash
python3 "$HANDOFF" status <JOB_ID_OR_THREAD_ID>
python3 "$HANDOFF" result <JOB_ID_OR_THREAD_ID>
python3 "$HANDOFF" continue <JOB_ID_OR_THREAD_ID> --task-file /path/to/follow-up.md
python3 "$HANDOFF" cancel <JOB_ID_OR_THREAD_ID>
python3 "$HANDOFF" open <JOB_ID_OR_THREAD_ID>
```

`ask` 默认后台运行；本轮必须等结果时增加 `--wait`。复杂规划、全库只读取材和重要审校可用 `max`，普通执行和草稿检查用 `high`。

5. 读取 `result` 的结构化结论、证据、风险、产物和建议状态增量。外部 Agent 负责核验和决定是否采纳；Codex Thread 不直接修改项目权威状态或绕过人工确认。

## 交接合同

- `job_id` 是本地后台运行回执，`thread_id` 是可继续、可恢复、可在 Codex App 打开的权威会话标识。
- 任务正文只在启动前暂存，Worker 读取后删除；运行回执保存在本机 Codex 状态目录，不进入项目 Git。
- 默认线程工作目录是当前项目根。跨项目检索仍保持项目根 `cwd`，在任务包中声明只读来源范围。
- 同一 Thread 同一时刻只运行一个外部任务；需要并行判断时创建多个新 Thread，不并发续问同一 Thread。
- 外部 Agent 或最终集成者是 canonical 文件和状态的唯一写入者。Codex 只返回证据、产物和建议增量，除非任务包明确授权写入并满足项目安全边界。

## 完成标准

交接只有在以下信息齐全时完成：`job_id`、`thread_id`、Thread 标题、运行状态、结构化结果或明确错误、证据、风险、产物路径、建议状态增量，以及可用的 `codex://threads/<threadId>` 或 `codex resume <threadId>`。

路由用例位于 `evals/`；运行实现由 `scripts/codex_external_handoff.py` 和 `tests/` 验证。
