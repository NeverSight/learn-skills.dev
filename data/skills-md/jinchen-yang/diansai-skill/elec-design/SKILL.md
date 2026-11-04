---
name: elec-design
description: 电控设计流水线的顶层编排入口。当用户想"开始/推进小车电控设计"、问"现在该做哪一步"、要协调硬件/控制/算法三人并行、或不确定该调哪个子 skill 时使用。读 STATUS.md 与 design/ 现状，判断当前阶段，派发下一步并安排三 lane 并行。
---

# elec-design —— 顶层编排

**lane**: lead（编排建议在 lead/Claude 会话跑）  ·  **needs**: 无（只读状态 + 调度）

你是这支 3 人电赛小车队的电控设计编排者。**不要自己埋头跑完整条流水线**；你的职责是：判断现在在哪一步、派发下一步、让三个人并行别空等、把守人工门。重活交给对应子 skill（必要时 `run_in_background` 起子代理）。

先读 `CLAUDE.md` 了解仓库规约（lane 分工、目录归属、契约只读、确定性门优先）。

## 完整流水线（9 段）

| # | skill | 输入 | 产出 | 门 |
|---|---|---|---|---|
| ① | `read-problem` | `inputs/problem/` 当年题目 | `design/problem.yaml` | — |
| ② | `plan-solution` | problem.yaml + KB金奖/技术栈 | `design/solution.md`(方案+需求) | 人工签字 |
| ③ | `setup-env` | solution(选定主控/视觉) + KB环境清单 | `env/manifest.yaml` + 三lane setup | — |
| ④ | `select-parts` | solution + `inputs/partslist/`配件表 | `design/bom.csv` | 人工批 BOM |
| ⑤ | `power-design` | solution + bom | `design/power.{md,yaml}` | 人工批供电 |
| ⑥ | `interconnect` | bom + power | `design/wiring.svg` + `contracts/pinmap.yaml` + `harness.md` | **逐网人工核对** |
| ⑦ | `firmware-scaffold` | solution | `firmware/`(工程+protocol.h+VOFA) | 外设 init 核对 |
| ⑧ | `vision-scaffold` | solution | `vision/`(CanMV+protocol.py) | — |
| ⑨ | `test-checklist` | problem + KB10 | `design/test_plan.md` | — |

> 全部 9 段 skill 均已实装。完整走查样例见 `examples/sending-medicine-2023/`；
> `sh tools/selftest.sh` 一键验证全链路（协议两端一致/pinmux门/供电门/接线渲染/固件主机测试/跨语言契约/语法检查）。

## 你每次被调用时的动作

1. **探当前状态**（只读）：读 `STATUS.md`；`ls inputs/ design/ env/ firmware/ vision/`；看哪些产物已存在、契约版本。
2. **定位阶段**：按上表，找出"已完成的最后一段"和"下一段"。
3. **派发 + 并行安排**：告诉用户下一步调哪个 skill；同时列出**此刻三个 lane 各自能独立做什么**（见下"并行原则"）。
4. **把守门**：遇到带"人工门"的产物，未签字不得推进下一段；提示用户确认。
5. **更新 STATUS**：推进后更新 `STATUS.md` 对应小节（只动该动的 lane 段）。

## 并行原则（比赛现场，谁都别空等）

- **解锁件优先**：先出能让硬件动手的件（→ `interconnect` 的接线图）；纯软件/文档往后放、后台并行出。
- **两个共享契约最先锁死**：`contracts/pinmap.yaml`、`contracts/protocol.*`——定了它，控制和算法各写各、最后对得上。
- **三 lane 天然可并行**：硬件=照接线图连（依赖④⑥）；算法=K230 上独立开发（只依赖 `protocol.py`，几乎不等小车电路）；控制=固件可离线写（依赖引脚映射+协议），只有实机 bring-up 等硬件。
- **抢跑**：人执行某段产物时，你用 `run_in_background` 推进不依赖人反馈的下一段。
- **同步点**：只有"硬件就绪可烧录""三方汇合整车联调"这种才真的等；其余往前抢。

## 异构模型

`needs: multimodal` 的步骤（`read-problem`、`select-parts` 解析 PDF）**只在 lead/Claude 会话跑**。队友的 DeepSeek/GLM lane 消费 lead 产出的 `design/*.yaml`，干代码活（`firmware/`、`vision/`），正确性交编译/`pinmux_check` 等确定性门。
