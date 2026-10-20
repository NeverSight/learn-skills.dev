---
name: spec-evolution
description: Use when auditing delivery-surface completeness of this repository's skills and root prompt, or when a goal-loop P5 delivery re-checks the skills it touched. Triggers on skills missing tests or design docs, incomplete skill surfaces (references/scripts/templates), registration gaps across README/index/collections, frontmatter description length limits, oversized files, cross-skill relative links, and root-prompt net growth.
license: MIT
---

# 机械化演进回路 (Spec Evolution)

## 概述 (Overview)

演进回路有两个端：**变异端**产出新规则候选，**选择端**判断哪条候选更好。本仓库的头号失败模式是「出问题就加一条」——那正是**只有变异、没有选择**的产物（ball of mud）。

本技能只做**选择端**，且只做其中**机械可证**的那部分：把「哪条规则需要修」从模型的**意见**换成脚本的**退出码**。

**立论**：凡不能被一条命令复现的「改进建议」，一律不产生 finding。

## 触发条件 (When to Use)

| 触发 | 说明 |
| :--- | :--- |
| **独立调用**（主路径） | 用户或智能体显式执行全量审计（7 技能 + 根提示词）；`--skills` 可缩窄范围 |
| **`goal-loop` P5 增量挂载** | 交付归档阶段复查**本次交付触及**的 `skills/<n>/`；不做全量扫描 |

**不适用**（结构性排除，详见 [references/checks-spec.md](references/checks-spec.md) §5）：
- 评价「这个技能该不该存在」「职责是否重叠」「设计是否过重」——无客观信号，是谄媚高发区；
- 评价判据阈值本身是否合理（如「1000 行是否应为 800 行」）。

## 硬不变式 (Hard Invariants)

1. **零 LLM、零网络**：判定器不得调用任何模型，不得访问网络。同一份输入永远得到同一份输出。
2. **只读**：采集与判定**不修改任何文件**。修改由人类裁决后另行发起。
3. **事实与发现分离**：采集器只回答「是什么」，判定器才回答「哪里不对」。二者分属不同进程，禁止合并。
4. **人类裁决不外判**：报告由判定器写到「人类裁决」标题即停止。任何由模型代填的裁决内容均视为**门禁违规**（GI-4 断言防护）。

## 快速开始 (Quick Start)

```bash
python3 skills/spec-evolution/scripts/collect-facts.py --out /tmp/facts.json
python3 skills/spec-evolution/scripts/judge.py --facts /tmp/facts.json \
        --json /tmp/findings.json --report /tmp/report.md
echo "exit=$?"        # 0 = 无 BLOCKER/HIGH；1 = 存在 BLOCKER/HIGH；2 = 用法或输入错误
```

缩窄范围（P5 增量复查时用于缩短耗时）：

```bash
python3 skills/spec-evolution/scripts/collect-facts.py --no-gates --skills goal-loop,doc-governance --out /tmp/facts.json
```

> ⚠️ `--no-gates` 会**跳过 S1 门禁事实采集**，因而 **C-09 在本轮不执行**：报告对该项输出「未采集门禁事实 —— C-09 未执行」而非「无失败」，退出码也不再反映既有门禁状态。**放行前的最终复查必须不带 `--no-gates`。**

## 判据表 (Criteria)

十条判据的完整定义、严重度语义与已知表达上限见 [references/checks-spec.md](references/checks-spec.md)。

| ID | 判据 | 严重度 |
| :--- | :--- | :--- |
| **C-01** | 技能无 `tests/` 或其中无 `test_*.py` | HIGH |
| **C-02** | 技能无架构设计书 `docs/explanation/architecture/<n>-design.md` | MID |
| **C-03** | 技能交付面缺 `references/` / `scripts/` / `templates/`，或存在但为空 | MID |
| **C-04** | `description` 字符数 > 500（**软性建议值**，非硬限） | MID |
| **C-05** | `description` 字符数 ≥ 1024（Agent Skills 规范**硬限**） | HIGH |
| **C-06** | 单文件行数 > 1000 | MID |
| **C-07** | 技能在 4 个注册面中存在缺登记 | HIGH |
| **C-08** | 技能内存在跨技能相对链接 | HIGH |
| **C-09** | 既有门禁任一非零退出 | **BLOCKER** |
| **C-10** | 根提示词相对基线净增长 | MID |

## 锚点契约 (Anchors)

每条 finding 携带可被人直接核验的锚点。**锚点路径不存在时判定器自身报错退出 2**（防锚点幻觉）。三种形式与校验规则见 [references/anchor-contract.md](references/anchor-contract.md)。

## 退出码 (Exit Codes)

| 码 | 含义 |
| :--- | :--- |
| `0` | 无 **BLOCKER/HIGH**（可含 MID advisory；C-09 未采集时该项不参与判定） |
| `1` | 存在 **BLOCKER/HIGH** |
| `2` | 用法或输入错误（含锚点路径不存在 = 锚点幻觉） |

> 权威定义在 `scripts/judge.py` 与 [references/checks-spec.md](references/checks-spec.md)；本表与之一致。

## 红线 (Red Lines)

- **不得**自动修复 finding——那会让本技能沦为「自动改自己规则的规则」，即 ball of mud 的机器化版本。
- **不得**往 `contexts/AGENTS.md` 增加条款——该文件准入判据禁止净增长。
- **不得**把本技能接入 CI 或引入第三方依赖。
