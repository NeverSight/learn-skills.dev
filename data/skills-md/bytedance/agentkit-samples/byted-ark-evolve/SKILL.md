---
name: byted-ark-evolve
description: >
  Agent self-evolution system. Collects signals from user feedback,
  stores execution trajectories (golden + correction pairs), analyzes
  patterns, proposes mutations to workspace files, and generates HTML reports.
  Trigger with "/evolve" or when the user asks to improve agent behavior.
  Also use when the user says "remember this pattern", "don't do X again",
  or "that was a good approach, save it".
metadata:
  version: "0.3.1"
  author: "volcengine/modelark"
  tags: "evolution meta-skill self-evolving"
---

# Evolution Skill

Agent 自进化系统。进化单位是整个 Agent（Identity + Context + Protocol + Capability + Runtime）。

## 核心原则

1. **Quality > Reliability > Efficiency > Cost** — 不允许牺牲质量换效率
2. **帕累托约束** — 任何 mutation 如果导致某个维度退化，BLOCK 并请用户决策
3. **写入即生效** — 用户确认变更后写入 workspace 文件，下次 session 即可加载新配置
4. **先对齐再执行** — 进化方案必须先呈现给用户确认

## 数据安全与权限边界

- **本地存储**：所有运行时数据(信号、轨迹、变异、报告)写入用户本地 `~/.{*claw*}/workspace/evolution-data/`，不上传任何外部服务。
- **无外网调用**：脚本不发起 HTTP/socket 请求(可代码层验证：无 `requests` / `urllib` / `http.client` / `socket` 等导入用于网络通信)。
- **变更前置确认**：mutation 写入 workspace 文件前，必须由用户在对话中显式接受提案；用户未接受前不会修改任何文件。
- **作用范围**：写入仅限 `~/.{*claw*}/workspace/` 目录及其子目录；不访问 `/etc/`、`~/.ssh/`、`~/.aws/` 等敏感路径。
- **可审计**：每次 apply 通过 git commit 留痕，用户可随时 `git log` 查看完整变更历史。
- **可追溯**：每条 mutation 在 SQLite DB 中保留 source(evolution / user-direct / snapshot-diff)、决策状态、时间戳。
- **可禁用**：删除 `evolution-data/` 目录或卸载 skill 即完全停止；删除 `~/.{*claw*}/workspace/` 不会影响其他 skill。

## 数据目录

> **Runtime 适配**：workspace 根路径自动探测 `~/.{*claw*}/workspace/`(优先 `.arkclaw` → `.openclaw` → 其他含 `claw` 的目录),也可用 `CLAW_WORKSPACE` 环境变量显式指定。新装默认创建在 `~/.arkclaw/workspace/`。

```
evolution-data/
├── file-registry.json    ← 初始化扫描结果
├── evolution.db          ← SQLite（信号、变异、轨迹）
├── snapshot.json         ← Workspace 文件 hash 快照（兜底变更检测）
├── trajectories/
│   ├── golden/           ← 正确执行轨迹
│   └── corrections/      ← 错误→修正对
├── dashboard.html        ← Dashboard 页面（dashboard-render.py 自动生成）
└── reports/
    ├── evolution-*.json  ← 进化报告数据（JSON）
    └── evolution-*.html  ← 进化报告页面（渲染后）
```

## References（按需读取，不随 session 加载）

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| `references/layer-model.md` | 5 层模型 + 归因规则 | 进化分析时 |
| `references/pareto-rules.md` | 帕累托约束 + 验证标准 | 进化分析时 |
| `references/file-semantic-map.md` | 已知文件→层/语义/风险映射 | 初始化 + 归因时 |
| `references/init-rules.md` | 状态判定规则 + 占位符列表 | 初始化时 |
| `references/signal-types.md` | 信号识别规则 + 示例 | 信号收集时 |
| `references/trajectory-templates.md` | 轨迹存储格式 + 示例 | 轨迹写入时 |
| `references/evolution-steps.md` | 进化分析详细流程（Step 0-7） | /evolve 执行时 |
| `references/onboarding.md` | 新手引导内容 | 首次安装时 |
| `references/report-schema-example.json` | 报告 JSON 数据格式示例 | 生成报告时 |
| `references/dashboard-schema-example.json` | Dashboard JSON 数据格式示例 | 生成 Dashboard 时 |

---

## 零、初始化（/evolve init）

首次安装或 Agent 版本变化时执行。

触发条件：
- `evolution-data/` 不存在
- `file-registry.json` 中 `agent_version` 与当前不一致

### 首次安装流程（建议连贯执行）

**Step A — 新手引导（纯展示，无需用户确认）**

检测到首次安装时，建议直接展示以下引导内容(无需额外询问"是否要看引导")：

> **欢迎使用进化系统**
>
> 这个系统让我能从你的反馈中学习。简单来说：
> - 你日常的纠正、建议会被自动记录
> - 攒够一定数量后，我会分析这些反馈并提出改进方案
> - **所有改动必须经你确认才会执行**
>
> **可用命令**
>
> | 命令 | 说明 |
> |------|------|
> | `/evolve` | 手动触发一次进化分析 |
> | `/evolve init` | 重新初始化 |
> | `/evolve scan` | 扫描历史对话提取反馈 |
> | `/evolve dashboard` | 生成进化 Dashboard |
> | `/evolve help` | 查看完整引导 |
>
> 现在开始初始化扫描——扫描完成后，你还可以选择扫描历史对话来加速学习。

展示完毕后建议进入 Step B,无需用户额外确认。

详细引导内容（用户说 `/evolve help` 时展示完整版）：读取 `references/onboarding.md`

**Step B — 初始化扫描（涉及文件写入，需用户确认）**

```bash
python skills/byted-ark-evolve/scripts/workspace-init.py
```

1. 全量扫描 workspace（排除 .git/ node_modules/ __pycache__/ evolution-data/）
2. 按 `references/init-rules.md` 判定每个文件状态（evolvable / user-owned / skill-owned / needs_review）
3. 按 `references/file-semantic-map.md` 标注已知文件语义，未知文件标 needs_review
4. 生成 `evolution-data/file-registry.json`
5. 如果 DB 不存在，执行 `db-init.py`
6. 输出摘要

needs_review 文件：进化分析时由 Agent 读取并补分类，写回 registry。

**Step C — 历史对话扫描（可选，需用户确认）**

Step B 完成后，提供历史对话扫描选项：

```bash
# 先估算成本
python skills/byted-ark-evolve/scripts/scan-history.py estimate --days 7
python skills/byted-ark-evolve/scripts/scan-history.py estimate --days 30
```

展示给用户：

> 检测到 N 段历史对话。是否要扫描过去的对话来提取已有的反馈信号？
> 这可以让进化系统从你已有的使用习惯开始学习，而非从零开始。
>
> 1. 扫描最近 7 天（N 段对话，预计消耗 ~X tokens，约 $Y）
> 2. 扫描最近 30 天（N 段对话，预计消耗 ~X tokens，约 $Y）
> 3. 跳过，从零开始
>
> 你也可以随时用 `/evolve scan` 手动触发。

用户选择后：

```bash
# 提取对话内容
python skills/byted-ark-evolve/scripts/scan-history.py extract --days 7
```

Agent 逐段对话读取，按 `references/signal-types.md` 规则识别信号，调用 `signal-record.py` 记录（标记 `context` 为 `history-scan`）。

完成后展示摘要："从 X 段对话中提取了 Y 条反馈（N 条纠正、M 条建议…）"

如果用户选择跳过，直接结束初始化。

---

## 〇、User-Direct 变更追踪

用户直接指令 Agent 修改 workspace 文件时，自动记录到 evolution.db。

**追踪层 A（可选 Hook）**：用户启用 PostToolUse Hook 后，监听 Edit/Write 事件，目标在 workspace 内则记录 `source='user-direct'`(Hook 仅观察执行结果，不阻断工具调用)。
**追踪层 B（快照兜底）**：进化分析启动时对比 `snapshot.json`，捕获 Hook 漏掉的变更（手动编辑、Bash 写入等），记录为 `source='snapshot-diff'`。

Mutation source 三种值：
- `evolution` — 进化分析产生（走 proposed→approved→applied 流程）
- `user-direct` — Hook 实时捕获（跳过 proposed/approved，直接 applied）
- `snapshot-diff` — 快照对比发现（缺失意图，仅标注"检测到变更"）

---

## 一、信号收集

在日常对话中，识别用户反馈信号并记录到 SQLite。

信号类型：correction / negative / positive / suggestion / preference / clarification
Layer 归因：identity / context / protocol / capability / runtime

详细识别规则和示例：读取 `references/signal-types.md`

记录：
```bash
python skills/byted-ark-evolve/scripts/signal-record.py \
  --type correction --layer protocol --severity high \
  --text "用户原话" --context "当时在做什么"
```

当用户说"记住这个"、"以后别这样"等,建议及时记录为信号。

---

## 二、轨迹存储

两种轨迹：
- **Golden**：做对了 → `evolution-data/trajectories/golden/`
- **Correction**：做错了→修正 → `evolution-data/trajectories/corrections/`

存储格式和模板：读取 `references/trajectory-templates.md`

执行任务前，检索相关 correction trajectory，主动复述修正要点。

---

## 三、Gate 检查

```bash
python skills/byted-ark-evolve/scripts/gate-check.py
```

自动触发条件（满足任一）：
- ≥5 条 correction/negative/clarification 信号
- ≥3 条 high severity 信号
- 同一 layer ≥3 条信号
- ≥7 天无进化且有新信号

约束：24h 冷却 + 饱和检测。
手动触发：`/evolve` 跳过 Gate。

---

## 四、进化分析（/evolve）

**推荐流程：所有进化变更通过 orchestrator pipeline 执行，以保证 DB 状态与变更可追溯。**

- 不建议 agent 自行分析信号后直接修改 workspace 文件
- 不建议跳过 DB 记录环节(Python sqlite3 是标准库内置模块,无需额外工具)
- **标准流程**：`orchestrator.py timer-review` → 生成提案 JSON → `ingest_outputs` 写入 DB → 用户确认 → `apply-proposal` 应用变更
- **原因**：绕过 DB 记录会导致 Dashboard 无数据、变更不可追溯、验证流程断裂

### 编排命令

```bash
# /evolve 手动触发（跳过 Gate，≥1 信号即可，完整 7 步）：
python skills/byted-ark-evolve/scripts/orchestrator.py timer-review --skip-gate --worker-mode agent

# Gate 自动触发（阈值达标时）：
python skills/byted-ark-evolve/scripts/orchestrator.py timer-review --worker-mode agent

# session 开始时自动检查：
python skills/byted-ark-evolve/scripts/orchestrator.py session-start

# 用户确认提案后应用：
python skills/byted-ark-evolve/scripts/orchestrator.py apply-proposal --group <proposal_group_id>
```

说明：
- `--worker-mode agent`：真实调用 `openclaw agent --local` 完成 review worker 分析
- `--worker-mode mock`：用于本地稳定测试，不依赖模型调用
- orchestrator 会生成 `pending-evolution.json` / `daily-digest.json`，但 **DB 仍是主状态源**

## Gene 集成（v0.3.1，本地静态库）

Gene 是 **mutation 的标准化模板库**。本版本随 skill 包发布静态库 `references/gene-library.json`，**无云端调用**。

边界：
- Gene **不是分析器**，不负责根因归因
- Gene **不是执行器**，不直接修改任何文件
- Gene **不是本地规则匹配器**，本地脚本不负责做 gene 相关性判定

职责分工：
- **Agent / subagent**：读取信号、日志、轨迹，完成归因分析
- **Gene 静态库**：提供 mutation 模板候选（id / summary / pattern_key / rule_text）
- **Evolution skill**：编排 load → Agent 判断 gene 候选 → 生成 mutation → 用户确认 → 执行

### 何时调用 Gene

以下场景必须进入 Gene 流程：
1. `/evolve` 手动触发后，在 Step 2 归因完成后进入 Step 2.5 Gene 候选筛选
2. 自动进化触发后，在 mutation 设计前进入 Step 2.5
3. 用户说"记住这个模式 / 下次也这么做"时，优先浏览 gene 库，判断是否已有可复用模板

### Gene 命令

```bash
python skills/byted-ark-evolve/scripts/gene.py --list
python skills/byted-ark-evolve/scripts/gene.py --show <gene_id>
python skills/byted-ark-evolve/scripts/gene.py --summary
```

规则：
- 库随 skill 版本发布（更新需升级 skill 版本），无 `--fetch` 命令
- Agent 在 Step 2.5 阅读 signal + attribution + gene 内容，判断"哪些 gene 的方案如果提前应用，能避免当前负向反馈或 error 再次发生"
- Step 3 中，Agent 基于选中的 gene template 生成 mutation proposal

详细流程（Step 0-7，含 Step 2.5 Gene 候选筛选）：读取 `references/evolution-steps.md`

概要：快照 Diff → 扫描信号 → **轨迹聚类（Skill 候选检测）** → 归因分析 → **Gene 候选筛选（静态库 + Agent 判断）** → 设计 Mutation → **用户确认** → **组装 JSON + 渲染报告/Dashboard** → **输出进化总结** → 标记已处理 → 更新快照

### 轨迹 → Skill 涌现（Step 1.5）

进化分析时自动检测轨迹中的可提取模式：
- Golden 轨迹同类 ≥3 条 → 建议提取为独立 skill
- Correction 轨迹同因 ≥2 条 → 建议加入防护规则

流程：检测 → 呈现候选给用户 → 用户确认 → 调用 **skill-creator** 生成。
如果用户未安装 skill-creator，提示安装。

### 用户确认交互规范

设计完 mutation 后，**必须先呈现方案给用户确认，未确认前不执行任何写入**。

展示格式（逐条列出）：

```
### 进化方案（共 N 条变更）

1. 📝 [AGENTS.md] — 新增「中文编码规范」
   - 层归因：Protocol
   - 变更类型：追加（user-owned 文件，仅允许追加）
   - 帕累托检查：✅ 通过
   - 摘要：在末尾新增 section，规定中文 API 调用使用 Python

2. 📝 [SOUL.md] — 修改「任务执行流程」
   - 层归因：Identity
   - 变更类型：修改（evolvable 文件）
   - 帕累托检查：✅ 通过
   - Before: 「直接执行用户指令」
   - After:  「先检索相关 correction，再执行」

以上 N 条变更是否执行？你可以：
- 全部接受
- 全部拒绝
- 逐条选择（如"接受 1，拒绝 2"）
```

关键规则：
- 每条 mutation 必须列出目标文件、变更类型、帕累托结果
- user-owned 文件特别标注"仅追加"
- 用户明确回复前，不执行任何写入操作
- 被拒绝的 mutation 标记为 `rejected`，保留记录

### 进化完成总结

报告生成后，在对话中直接输出一段**自然语言总结**（不是文件路径，是让用户直接看懂的摘要）：

```
本次进化处理了 X 条反馈，产生 Y 条待处理提案/变更：
- [AGENTS.md] 新增了「中文编码规范」— 因为你 4 次提到不要用 curl 发中文
- [SOUL.md] 调整了任务执行流程 — 增加了执行前检索修正记录的步骤

被拒绝：W 条
完整报告：evolution-data/reports/evolution-<date>.html

下一步：当你再次遇到相关场景时，我会观察这些改进是否生效。
```

规则：
- 用自然语言，不用术语（不说 mutation / signal / layer）
- 每条变更说明"改了什么"+"为什么改"
- 告知报告路径，但不以路径为主要输出
- 提及后续验证计划

归因时参考 `references/layer-model.md` + `evolution-data/file-registry.json`
写入时参考 `file-registry.json` 中的 write_policy（evolvable→section-edit / user-owned→append-only）
帕累托检查参考 `references/pareto-rules.md`

### 报告生成流程（模板方式）

1. 组装报告数据为 JSON（参考 `references/report-schema-example.json`）
2. 写入 `evolution-data/reports/evolution-<date>.json`
3. 调用 `python scripts/report-render.py <json> --output <html>` 渲染 HTML
4. （可选）组装 Dashboard JSON（参考 `references/dashboard-schema-example.json`）→ `dashboard-render.py`

Agent 只负责填写纯数据 JSON，Python 脚本负责所有条件渲染逻辑（如：有无被拒绝的变更、是否饱和、高严重度信号展示等）。

---

## Pending Proposal 生命周期（v0.2.2）

`pending-evolution.json` 的定位是**给人看的待处理提案队列**，不是“第二天早上专属提醒”。

规则：
- 夜间 timer review 只生成 proposal，不自动 apply
- 只要 proposal 仍然有效且未被用户处理，后续任意一次 `session_start` 都应该可以再次展示
- 展示状态与决策状态分离：`pending -> presented -> accepted/rejected/stale/superseded`
- `pending-evolution.json` / `daily-digest.json` 是导出层；**DB 才是主状态源**

推荐命令：

```bash
python skills/byted-ark-evolve/scripts/pending-evolution.py export
python skills/byted-ark-evolve/scripts/pending-evolution.py show
python skills/byted-ark-evolve/scripts/pending-evolution.py present --group <proposal_group_id>
python skills/byted-ark-evolve/scripts/pending-evolution.py decide --group <proposal_group_id> --decision accepted
python skills/byted-ark-evolve/scripts/pending-evolution.py stale --older-than-hours 72
```

## 五、验证

验证状态：待验证 → 已观察 → 已验证 / 已复发 / 部分生效

状态说明：
- **待验证**：刚提出，等待在真实场景中验证
- **已观察**：初步通过 1 次，但不可完全信赖
- **已验证**：≥3 次跨 session 无复发，确认行为改变
- **已复发**：验证后再次违反，需要加固
- **部分生效**：部分场景有效，部分未覆盖

详细规则和 credit 权重：读取 `references/pareto-rules.md` 验证标准章节

---

## 六、快速命令

| 用户说 | Agent 做 |
|--------|---------|
| `/evolve` | 执行 `orchestrator.py timer-review --skip-gate --worker-mode agent`，完整 7 步进化（≥1 条信号即可，不受 Gate 阈值和冷却限制） |
| `/evolve init` | 首次安装时执行：初始化扫描 + 生成文件注册表 |
| `/evolve scan` | 扫描历史对话，提取已有的反馈信号 |
| `/evolve detect` | 批量检测历史对话中的信号候选（`scan-history.py detect`） |
| `/evolve dashboard` | 生成并打开 Dashboard（`dashboard-render.py` → `evolution-data/dashboard.html`） |
| `/evolve help` | 展示新手引导（读取 `references/onboarding.md`） |
| "记住这个模式" | 记录 positive 信号，作为后续进化分析的正向参考 |
| "以后别这样做" | 记录 correction 信号，标记需要改进的行为 |
| "进化状态" | 快速查看：`query.py dashboard`（文本）；完整页面：组装 JSON → `dashboard-render.py`（HTML） |
| "gene 列表 / gene 概况" | 调用 `gene.py --list` / `gene.py --summary` |
| "进化报告" | 组装 JSON（参考 `references/report-schema-example.json`）→ `report-render.py` |

---

## 七、查询工具

```bash
python skills/byted-ark-evolve/scripts/query.py dashboard          # Dashboard
python skills/byted-ark-evolve/scripts/query.py signals --unprocessed  # 未处理信号
python skills/byted-ark-evolve/scripts/query.py signals --layer protocol  # 按层
python skills/byted-ark-evolve/scripts/query.py mutations --status pending  # 变异
python skills/byted-ark-evolve/scripts/query.py mutations --source user-direct  # 用户直接变更
python skills/byted-ark-evolve/scripts/query.py trajectories       # 轨迹统计
python skills/byted-ark-evolve/scripts/query.py gene-matches       # 最近一次 gene 候选筛选结果

# 信号候选检测（v0.2.9 新增）
python skills/byted-ark-evolve/scripts/scan-history.py detect --days 7            # 检测近 7 天对话中的信号候选
python skills/byted-ark-evolve/scripts/scan-history.py detect --min-confidence high  # 仅高置信候选
```


## Apply 闭环（v0.2.4）

**用户接受提案后，建议通过以下命令完成应用，以保证 git commit / snapshot / dashboard 同步更新。**

```bash
python skills/byted-ark-evolve/scripts/apply-proposal.py --group <proposal_group_id>
```

该命令会自动完成全部闭环操作：
1. 应用该 group 下的 mutations 到目标文件
2. 执行 git commit（每个 proposal_group 一次 commit）
3. 调用 snapshot save
4. 写回 review/result 到 DB
5. 重新生成 dashboard.html

也可通过 orchestrator 调用（效果相同）：
```bash
python skills/byted-ark-evolve/scripts/orchestrator.py apply-proposal --group <proposal_group_id>
```

## Dashboard 固定模板（v0.2.5+）

Dashboard 采用**模板与数据分离**架构，确保样式固定、不受模型影响。

### 架构

| 文件 | 职责 | 更新方式 |
|------|------|----------|
| `scripts/dashboard-template.html` | 固定 HTML/CSS/JS 模板 | 仅开发者手动迭代 |
| `scripts/dashboard-render.py` | 查 DB + references/gene-library.json → JSON → 注入模板 | orchestrator 自动调用 |
| `evolution-data/dashboard.html` | 最终输出，用户浏览器打开 | 每次 pipeline 自动生成 |

### 使用

```bash
# 手动生成
python skills/byted-ark-evolve/scripts/dashboard-render.py --db evolution-data/evolution.db --data-dir evolution-data/

# 自动生成（timer-review / apply-proposal 完成后自动触发）
```

### 三个 Tab

- **Overview**：全局统计、趋势图、改动验证、层分布
- **Activity**：日期选择器 + 单次进化报告详情（来源反馈、改动 diff、状态）
- **Genes**：基因表格 + 手风琴展开关联改动

