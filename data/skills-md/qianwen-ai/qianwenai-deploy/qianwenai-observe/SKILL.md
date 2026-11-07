---
name: qianwenai-observe
version: "1.0"
description: >-
  用自然语言汇报由 qianwenai-deploy 部署到阿里云国内站（aliyun.com）的应用的健康、性能、
  资源状态和实际费用，无需进入控制台。读取项目目录下的 .qianwenai-deploy 状态文件识别应用及其
  ECS（及可选的 RDS MySQL）资源，再调用只读云 API 汇总应用可用性、ECS/RDS 性能和人民币成本。
  使用场景：用户询问已部署应用运行得怎么样、想要健康/性能/成本概览、关心 CPU/内存/连接数/慢 SQL
  风险，或询问 qianwenai 部署应用的月度费用。
  不使用场景：没有 .qianwenai-deploy 状态文件；目标是阿里云国际站（用 qwencloud-observe）；
  用户想变更或恢复资源（用 qianwenai-operate）。
prerequisites:
  - 已配置国内站凭证的 aliyun CLI 3.x
  - 项目目录存在 .qianwenai-deploy 状态文件
  - Python >= 3.8（仅当用 scripts/render_report.py 渲染报告文件时需要）
input: >-
  含 .qianwenai-deploy 的项目目录。可选：时间范围（15 分钟 / 1 小时 / 24 小时，默认 1 小时）。
output: >-
  自然语言概览：一句话总体状态，然后应用 / ECS / RDS / 成本四部分摘要、带证据的风险项、数据时间
  和未知项。发现故障时提供进入 qianwenai-operate 的下一步入口。
---

# 千问 AI 可观测

对由 `qianwenai-deploy` 部署的应用做只读可观测，回答「应用运行得怎么样、预计花多少钱」，无需进入
控制台。所有价格为**人民币（¥）**。

## 快速路径

1. **识别应用** — 读取项目目录下的 `.qianwenai-deploy`（见 `references/workflow.md`）。
2. **选择时间范围** — 默认最近 1 小时；用户可选 15 分钟 / 1 小时 / 24 小时。
3. **逐层检查** — 应用、ECS、（可选）RDS、成本。每项返回统一结果状态之一；单项失败不阻断其他层。
4. **汇报** — 一句话结论，然后逐层摘要、风险项、数据时间、未知项。

## 范围

| 范围内 | 范围外 |
|--------|--------|
| 由 `qianwenai-deploy` 部署的应用（存在状态文件） | 无 `.qianwenai-deploy` 状态文件的应用 |
| 单 ECS，或 ECS + RDS MySQL 8.0 | 其他拓扑 / 自建服务器 |
| 只读的可用性、性能、成本概览 | 任何资源变更 → 用 `qianwenai-operate` |
| 报告运行时状态（可用性、性能、成本） | 源码审查、找 bug/漏洞、判断哪行代码写错、改代码 |
| 阿里云国内站，人民币 | 国际站 → 用 `qwencloud-observe` |

## 代码问题不在能力范围内

本 skill 只做只读观测，报告运行时的可用性、性能和成本，不做源码审查、缺陷定位或代码修改。

涉及代码时，明确告知用户：改代码属于本 skill 能力之外，需由用户自行决定并执行，相应后果由用户
自行承担。

## 前置条件

> **Aliyun CLI**：执行 `aliyun version`（需 3.x）。所有查询用驼峰原生形态直连 OpenAPI，
> 不依赖插件。凭证仅用 `aliyun configure list` 查看状态。
> **绝不**读取、回显、打印或索要 AK/SK/Token。若无有效凭证配置集，停止并请用户在本会话之外配置凭证。
> 见 `references/cli_installation_guide.md`。

## 状态与评分

每层返回一个状态——`healthy`（正常）· `degraded`（可用但有风险）· `unavailable`（不可用）·
`unknown`（无法判断）——并带上检查时间、目标资源、关键证据、数据来源。单项查询失败时继续检查其他层，
把失败项标记为 `unknown`——绝不静默省略、绝不编造数据。

每层还会打一个分，各层分数相加得到 0-100 的健康分并给出 A/B/C/D 分级
（`>=90` A · `>=75` B · `>=60` C · `<60` D）。共评四个维度：

| 维度 | 权重（含 RDS） | 权重（无 RDS） | 信号 |
|------|----------------|----------------|------|
| 应用 | 35 | 45 | 可达性、`/healthz`、响应时间、错误率 |
| ECS | 30 | 45 | CPU、内存、磁盘使用率、磁盘 IO、网络 |
| RDS | 25 | — | 连接数、慢 SQL、空间、行锁等待 |
| 可用性 | 10 | 10 | ECS/RDS 运行状态、近期系统事件、EIP 状态与带宽、安全组暴露面 |

当应用没有 RDS 时，其权重重分配给应用和 ECS。**成本从不计分**——单独展示为实际账单加一段基于
利用率的优化说明。

备份 / 快照缺失和安全组收敛建议只作为风险与建议项呈现，**不计入健康分**；EIP 未绑定、带宽贴顶、
缺 80/443 入方向规则等影响可用性的信号计入可用性维度。

## 怎么检查

先识别应用，再逐层看。执行每步命令前先读对应指南。某一项失败不影响其他层——标记为 `unknown`
继续往下。

这些层的检查彼此独立且只读——识别应用后，把各层的只读 API 并行发起（后台 `&` + `wait`），
不要串行等待；同一台 ECS 上的云助手命令合并成一条脚本一次性取回，减少往返。

1. **识别应用** — 读 `.qianwenai-deploy`，拿到地域和资源 ID。见
   [workflow](references/workflow.md)。
2. **应用能访问吗？** — 探测公网地址和 `/healthz`，检查应用和 Nginx 服务及端口，汇总近期错误。见
   [observe-application](references/observe_application.md)。
3. **服务器怎么样？** — ECS 状态，以及时间范围内的 CPU、网络、磁盘、内存。见
   [observe-ecs](references/observe_ecs.md)。
4. **数据库怎么样？**（仅当应用含 RDS）— 状态、连接数、QPS/TPS、空间、行锁等待，以及脱敏慢 SQL。见
   [observe-rds](references/observe_rds.md)。
5. **公网与暴露面怎么样？** — EIP 状态与带宽、安全组 80/443 放行与暴露风险。见
   [observe-network](references/observe_network.md)。
6. **有没有维护和备份？** — ECS 系统事件、系统盘快照、RDS 备份。见
   [observe-resilience](references/observe_resilience.md)。
7. **花了多少钱？** — 应用的实际费用，可选本月外推。见 [observe-cost](references/observe_cost.md)。
8. **评分并汇总** — 给每层打分，相加得到健康分与分级，再写一个自然语言结论。见
   [workflow](references/workflow.md)。

默认看最近一小时；尊重用户明确指定的 15 分钟 / 1 小时 / 24 小时，并在汇报中注明所用范围。

## 怎么告诉用户

先给健康分与分级加一句话结论，再给应用、服务器、数据库（如有）、成本各一行短摘要，每行附背后的证据。
点出风险项，说明有哪些没能判断以及原因，并给出数据时间。项目目录存在 `operate_audit.jsonl` 时，
带上最近一次运维动作（时间、动作、结果），让本次评分对上最近的恢复。发现真实故障时，主动提议用
`qianwenai-operate` 进入故障诊断：用 AskUserQuestion 给出 **立即诊断并修复** / **只看不动**，
选择前者即进入 `qianwenai-operate`。同时把已采集的证据写入项目目录的 `observe_handoff.json`
（故障层、关键指标、数据时间戳，不含任何密码/签名 URL），供 operate 作为诊断起点、免于重复只读检查。

```text
健康分：87 / 100（B，良好）——应用正常，关注 RDS 连接趋势。

应用：访问正常，当前响应时间 186 ms，应用和 Nginx 服务正常。
ECS：运行正常，最近一小时 CPU 平均 31%，未发现持续高负载。
RDS：运行正常，活跃连接数从 12 上升到 38，建议关注连接池趋势。
成本：2026-08 账期实际费用 ¥88.30（ECS ¥52.10，RDS ¥36.20）。

数据截至：2026-08-03 16:20 UTC+8
```

给完摘要后，主动问一句是否需要导出报告文件，例如：「需要我导出一份 Markdown 或 HTML 报告吗？」
由用户决定，不强制。

## 交互形态

- **只读信息**（体检结论、状态、费用）：纯文本，每条判断后附一行证据（指标、状态、时间戳）。
- **改状态动作**（进入 operate、导出报告等）：用 AskUserQuestion，提问答清 **做什么** · **影响** ·
  **怎么验证**，确认前不执行。
- **主动纪律**：健康时安静；仅在有风险或真实故障时主动开口，且一次只提一个后续动作（诊断 / 导出报告）
  让用户选。

## 渲染报告文件（可选）

当用户想要一份保存的 Markdown 或 HTML 报告时，把各层的状态、分数、关键指标和证据汇总成一个
JSON 对象，交给 `scripts/render_report.py` 渲染，不要手写最终排版。HTML 输出是多卡片报告
（含健康分与异常的总览、每层一张带指标表的卡片、成本卡、建议卡）；Markdown 是其轻量等价物。

1. 打印 schema 并填写：`python3 scripts/render_report.py --schema`。每层需要 `state`、
   `score`/`max_score`、`metrics[]` 和 `detail`；`assessment.health_score` 必须等于各层分数之和
   且与分级匹配；成本只承载实际账单金额。
2. 渲染前先校验：`python3 scripts/render_report.py --validate -i data.json`。按提示修正问题
   （状态非法、`unknown` 缺 reason、分级与分数不符、成本里出现预估）。
3. 按用户选择的格式渲染：
   `python3 scripts/render_report.py -i data.json -f md -o report.md`（或 `-f html`）。

## 交接给运维（可选）

发现真实故障且用户选择进入 `qianwenai-operate` 时，向项目目录写 `observe_handoff.json`，让 operate
以此为诊断起点、优先验证被点名的那一层：

```json
{
  "from": "qianwenai-observe",
  "generated_at": "2026-08-03T16:20:00+08:00",
  "fault_layer": "rds",
  "symptoms": ["RDS 活跃连接从 12 升到 190，接近上限"],
  "metrics": {"rds_active_connections": 190, "app_http_code": 200}
}
```

`fault_layer` 取 `app` / `nginx` / `ecs` / `rds` / `network` / `disk` 之一。只写只读观测得到的
证据，**绝不**写入密码、连接串或签名 URL。文件仅作线索，operate 仍会独立复核后再提恢复动作。

## 安全

| 规则 | 说明 |
|------|------|
| 只读 | 云助手命令必须只读；绝不修改实例/应用状态。 |
| 不碰密码 | 绝不读取或输出 `.qianwenai-deploy.local` 中的密码。 |
| 脱敏 | 日志输出中的 AccessKey、Token、密码、连接串密码、Cookie 必须脱敏。 |
| 慢 SQL | 只输出 SQL 模板/脱敏 SQL，限制长度；绝不展示字面参数值。 |
| 成本 | 只展示实际费用（¥）及账期；绝不展示预估。尚无账单时把成本标记为 `unknown`。 |

## 所需权限

见 `references/ram_policies.md`。除惰性装 agent 的 `cms:InstallMonitoringAgent` 外均为只读：
`ecs:DescribeInstances`、`ecs:RunCommand` +
`ecs:DescribeInvocations`（只读命令）、`cms:DescribeMetricList`、
`cms:DescribeMonitoringAgentStatuses`、`cms:InstallMonitoringAgent`、`ecs:DescribeSecurityGroupAttribute`、
`ecs:DescribeInstanceHistoryEvents`、`ecs:DescribeSnapshots`、`vpc:DescribeEipAddresses`、
`bssopenapi:QueryInstanceBill`、`bssopenapi:QueryBill`，以及（含 RDS 时）
`rds:DescribeDBInstances`、`rds:DescribeDBInstanceAttribute`、`rds:DescribeDBInstancePerformance`、
`rds:DescribeSlowLogRecords`、`rds:DescribeBackups`。

## 更多细节

各层指南已在上面「怎么检查」中链接。另有两份配置参考：

- [CLI 配置](references/cli_installation_guide.md) — 安装与凭证检查。
- [CLI 踩坑速查](references/api_gotchas.md) — 参数形态、时间格式、响应解析易错点。
- [RAM 权限](references/ram_policies.md) — 本 skill 所需的只读权限。
