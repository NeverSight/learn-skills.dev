---
name: spec-product-prd
description: Use when 需要在 sdlc-dev 的产品需求 Spec 流程执行 R2，将 requirements/solution.md 转写为可交付、可验收、可测试的 requirements/prd.md，且需要避免猜路径、在缺少 solution.md 时仍继续生成、或用“待确认问题/Open Questions”替代验证清单。
---

# spec-product-prd（R2：基于方案生成 PRD）

## 概览

R2 的目标是把 `{FEATURE_DIR}/requirements/solution.md` 的**推荐决策**转写为 `{FEATURE_DIR}/requirements/prd.md`：让研发能拆任务、QA 能写用例、干系人能评审与验收。

- **可验证优先**：PRD 的核心是 **场景 + 业务规则 + AC（可测试）**
- **不确定性收敛**：PRD 中**不出现**“待确认问题 / Open Questions”清单；未知统一进**验证清单**（Owner/截止/信号/动作）
- **不重复 R1**：方案对比/为何选择/讨论过程留在 `solution.md`；PRD 只写交付规格

## 何时使用 / 不使用

- **使用时机**
  - R1 已完成并产出 `requirements/solution.md`，需要把交付规格（范围/AC/里程碑/风险依赖）冻结为独立 PRD 评审
  - 需求不满足“简单需求可跳过 R2”的口径（见下方分流）
- **不要用在**
  - `spec-context` 失败（上下文定位失败）→ **立刻停止**
  - `requirements/solution.md` 不存在 / 明显未收敛（缺结论摘要/范围 In-Out/推荐方案/验证清单）→ **停止并回到 R1**

## 输入 / 输出（落盘约定）

- **硬门禁输入**：`FEATURE_DIR`（必须由 `spec-context` 获取）
- **读取**
  - `{FEATURE_DIR}/requirements/solution.md`（必读，作为唯一决策入口）
  - `{FEATURE_DIR}/requirements/raw.md`（按需：补证据入口/原始措辞）
  - `project/memory/glossary.md`（如存在：术语与口径）
- **写入**
  - `{FEATURE_DIR}/requirements/prd.md`（R2 产物，优先按模板生成）

## 门禁（必须先过，否则停止）

**REQUIRED SUB-SKILL：先执行 `spec-context` 并回显 `FEATURE_DIR=...`。**

```powershell
. ".\.aisdlc-cli\scirpts\spec-common.ps1"
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
Write-Host "FEATURE_DIR=$FEATURE_DIR"
```

- `spec-context` 失败 → **停止**
- `{FEATURE_DIR}/requirements/solution.md` 缺失 → **停止**（不得“先出一版 PRD 再说”）

> 违反门禁=违反精神：无论“时间紧/老板催/流程卡点”，都禁止猜路径、禁止跳过 `solution.md` 硬写 PRD。

## 核心流程（分流 + 规格化落盘）

### 0) 先做 R2 分流（可选，但强烈建议）

如果满足任一“简单需求”口径，则**不应生成独立 `prd.md`**，而应回到 R1 的 `solution.md` 追加 **Mini-PRD** 小节后直接进入 design：

- 纯规则/配置/文案类变更（不改变任务流与页面结构）
- 变更范围极小且无歧义（通常 1–2 处改动，无复杂权限/状态分支权衡）
- 在 `solution.md` 用少量条目即可写清 AC 且能直接验收

> 禁止用“issue + checklist”替代 Mini-PRD：本流程的最小交付规格必须落在 `solution.md`（可追溯、可继续对话、可入库）。

### 1) 从 `solution.md` 提取 PRD 的“可交付信息”

把 `solution.md` 中与交付/验收直接相关的内容抽成清单（不要发散新结论）：

- 目标一句话、In/Out、MVP 边界
- 核心场景（建议 ≤ 3 个）与成功标准
- 功能项（可拆解）与优先级（P0/P1/P2 或 Must/Should/Could/Won’t）
- 会影响 AC 的业务规则/口径（能引用就引用；不确定就进验证清单）
- 已知风险/依赖/假设（转写到 PRD 的验证清单表）

### 2) 用模板生成/更新 `{FEATURE_DIR}/requirements/prd.md`

优先对齐模板：`skills/spec-product-prd/prd-template.md`（只借结构，不把未知当已知）。

写作要求（最容易跑偏的点）：

- **场景驱动**：第 3 节场景要能直接导出第 6 节 AC
- **AC 可测试**：每条 AC 都能写成“输入/操作/期望结果”而非主观描述
- **优先级对齐里程碑**：MVP 至少覆盖 P0/Must；Out/Won’t 口径明确
- **不确定性只出现一次**：只写在第 8 节“风险/依赖与验证清单”表里

### 3) R2 自检（写完立刻过一遍）

- In/Out 与 `solution.md` 一致，且不歧义
- 每个核心场景都有 AC（可直接转测试用例）
- 功能优先级与里程碑一致：MVP 覆盖 Must/P0
- 业务规则/口径可追溯；不可追溯的条目已进入验证清单
- 关键异常与边界覆盖会影响 AC 的情况（权限/失败/幂等等）
- 文档中不出现“待确认问题 / Open Questions / 待定项”清单

## Quick reference（高频规则速查）

- **必须**
  - 先跑 `spec-context`，只用 `FEATURE_DIR` 拼路径
  - 必读 `solution.md`，PRD 只做“转写/规格化”，不新增决策
  - PRD 里必须有：In/Out、核心场景、AC、验证清单（Owner/截止/信号/动作）
- **禁止**
  - 猜路径（例如手写 `.aisdlc/specs/...`）
  - `solution.md` 缺失仍生成 PRD（“先写再问/先出一版”）
  - 写“待确认问题/Open Questions/待定项”列表（用验证清单表替代）

## 红旗清单（出现任一条：停止并纠正）

- 没跑 `spec-context` 就开始读写 `requirements/*.md`（或开始“猜 FEATURE_DIR”）
- `solution.md` 不存在/未收敛，却仍打算“先写 PRD 占坑”
- PRD 里出现 `待确认 / Open Questions / 待定 / TBD` 之类清单
- AC 充满主观词（“友好/清晰/合理/尽快”）而没有可验证动作
- 里程碑写了，但功能优先级与 MVP 范围对不上（MVP 不覆盖 P0/Must）

## 常见借口与反制（基线测试中的高频点）

| 借口（原话/近似原话） | 常见违规行为 | 必须的反制动作 |
|---|---|---|
| “**老板 10 分钟后评审…先写再问**” | 跳过 `spec-context` / 猜路径 / 先写 PRD 再补依据 | **门禁不过就停止**；需要先交付时，只能交付“验证清单 + 下一步动作”，不能交付“猜出来的 PRD” |
| “**路径靠猜，错了再改**” | 写到错误目录，导致后续引用/追溯全部断裂 | 只认 `FEATURE_DIR=...` 输出；所有路径用 `$FEATURE_DIR` 拼接 |
| “**没有 solution 也先出一版 PRD**” | 用 raw+常识脑补，导致范围与决策漂移 | `solution.md` 缺失/未收敛 → **停止并回到 R1**（先把决策入口稳定） |
| “**把不确定都标成待确认问题就行**” | PRD 出现 Open Questions 清单，没人负责、无法收敛 | 用第 8 节验证清单表：Owner/截止/信号/动作齐全；其他章节不再出现“待确认” |
| “**简单需求就写个 issue/checklist 吧**” | 交付规格散落系统外，无法追溯与迭代 | 简单需求要么走 R2，要么在 `solution.md` 追加 Mini-PRD；禁止用 issue 替代落盘 |

## 一个好例子（把“待确认问题”改写成可执行验证清单）

**坏写法（禁止）**：

- 待确认：最大导出行数是多少？
- 待确认：性能指标是什么？

**好写法（写到 PRD 第 8 节验证清单表）**：

| 风险/假设/依赖 | 验证信号 | 方法 | Owner | 截止 | 触发动作 |
|---|---|---|---|---|---|
| 假设：MVP 同步导出在 ≤50,000 行内可接受 | 导出耗时 ≤30s 且不触发超时/内存告警 | 用真实数据分布压测；记录 P95 | DEV | 评审后 3 天 | 若超阈值：切换异步导出方案，并更新 PRD 的里程碑与 AC |

