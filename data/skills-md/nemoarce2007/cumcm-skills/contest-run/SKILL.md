---
name: contest-run
description: 按 GRAPH.md 编排 CUMCM 全流程：读题到合规打包。用户要「从赛题做到提交」「三天全流程」「国赛一条龙」时使用。单点改摘要、只画图、只跑代码时不要使用。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: user
  graph-node: orchestrator
disable-model-invocation: true
---

# contest-run

编排器。自己不写公式、不写长文。逐节点调用模型技能，读边条件。

必读：[docs/GRAPH.md](../../docs/GRAPH.md)、[docs/LOOP.md](../../docs/LOOP.md)、[docs/STATE.md](../../docs/STATE.md)。赛期排期见 [references/schedule.md](references/schedule.md)。

## 何时使用

必须使用：用户要从赛题做到可提交；或 `status` 在中途但用户说「按图继续」。

禁止使用：只修一个图表/一段文字；工作区无 `contest-state.json`（先 `setup-cumcm-skills`）。禁止调用 `ask-cumcm`、`setup-cumcm-skills`、`grill-problem` 以外的用户技能——`grill-problem` 仅当题目未锁定时调用一次。

## 循环

目标：`status=shippable` 或停在带 `gate_failures` 的节点并报告给人。

每轮：看 `status` 与 GRAPH「边条件」，调用恰好一个下一节点技能，等该技能验收结束再决定边。

`max_rounds`: 24（节点数 × 回跳余量）

## 步骤

1. 读 `contest-state.json`。无文件 → 停，让用户跑 setup。
2. `status=uninitialized` 或题目原文不在 `problem/` → 调用 `grill-problem`，不得跳过。
3. 否则按 GRAPH 主图前进。失败边优先于前进边。
4. 小问 ≥2 且已 `assumptions_locked`：N6–N8 可按小问串行（默认）或在用户允许时并行；并行前冻结 `assumptions` 与 `symbols`。
5. 每完成一节点，向用户输出一行：`节点 <name> status=<新> 失败=<n>`。
6. 若在赛期：按 schedule.md 提醒当前阶段该收什么。不要因为临近截止而跳过 `grill-problem` 或三大检验，也不要把未跑出的数写进摘要。

## 验收

- [ ] 从未在本技能内直接撰写论文章节
- [ ] 每次只激活一个下一节点（并行 fan-out 时每个子问仍各自走完 verifier）
- [ ] 未在红灯时把 status 标为 `shippable`

## 输出

只通过被调技能写状态。编排器可追加 `gate_failures` 的 `next` 字段。

## 下一跳

`shippable` 后停止，列出提交物：电子版论文（首页摘要）、附录代码、支撑包、`AI工具使用详情.pdf`（若使用 AI）。
