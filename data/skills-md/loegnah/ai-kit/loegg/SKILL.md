---
name: loegg
description: loegnah's agent style and workflow orchestrator. Use for loegg, /loegg, or requests to work in this style.
disable-model-invocation: true
---

# Loegg

Execution modes live at `mode/<name>-mode.md`, bundled skills live at `<category>/<name>/SKILL.md` (`meta/`, `discover/`, `craft/`, `critic/`), and playbooks live at `playbooks/<title>.md`.

## Non-negotiables

The Principles section below grounds every trigger. In your reply, name each principle that shaped a decision and the specific choice it changed.

Remaining triggers:

- Configuring or updating loegg models and reasoning budgets (`setup`) -> the **loegg-setup** skill (`meta/setup/SKILL.md`).
- Asking how loegg works, which skill fits a task, or requesting prompt examples (`help`) -> the **loegg-help** skill (`meta/help/SKILL.md`).
- Stress-testing a plan, resolving ambiguous requirements, or explicitly invoking `grill` before building -> the **loegg-grill** skill (`discover/grill/SKILL.md`).
- Deep/multi-angle review or competing candidates (`arena`), triggered either by an explicit heavy/depth request ("다양한 관점/시각", "다각도로", "심층", "심화", "빡세게", "깊게") or by the agent's own judgment that a high-stakes step needs multi-model verification -> the **loegg-arena** skill (`craft/arena/SKILL.md`).
- <!-- <condition or trigger> -> the **<skill-name>** skill (`<category>/<skill-name>/SKILL.md`). -->

## Principles

Read the leaf skill in full for any principle you apply.

**Core**

- <!-- **<Principle Title>.** <When it applies and what it requires.> -->

**Architecture**

- <!-- **<Principle Title>.** <When it applies and what it requires.> -->

**Verification**

- <!-- **<Principle Title>.** <When it applies and what it requires.> -->

**Delegation**

- <!-- **<Principle Title>.** <When it applies and what it requires.> -->

**Meta**

- <!-- **<Principle Title>.** <When it applies and what it requires.> -->

## Autonomy

- **Just do it.** <!-- Reversible work that proceeds without asking. -->
- **Always pause.** <!-- Irreversible or high-risk actions that require confirmation. -->

## Execution Mode & Subagents

Select and read the execution mode before running a task:

- **Direct Mode (Default)**: Read `mode/direct-mode.md` when working interactively with the user in conversation. Clarify open decisions with the user and pause at requested review checkpoints.
- **Agent Mode (Autonomous)**: Read `mode/agent-mode.md` when the user invokes `/loegg agent` or asks the agent to run autonomously to completion without interactive checkpoints.

### Heavy Multi-Agent Escalation (`arena`, etc.)

Routine steps (including plain `"검토해봐"`) run directly in the main agent to avoid unnecessary token spend. Escalate a step to heavy multi-agent execution (`craft/arena/SKILL.md`) in two cases:

1. **Explicit depth/intensity signal from the user**: The user asks for multi-angle or deep work ("다양한 관점/시각", "다각도로", "심층", "심화", "빡세게", "깊게", or `arena`).
2. **Agent's own judgment**: Even without those keywords, the agent judges that the current step faces a high-stakes architectural fork, subtle failure mode, or costly lock-in risk where a single perspective is not enough.

## Writing the reply

- <!-- Reply style, language, formatting, and evidence rules. -->

## Comments

- <!-- Code comment rules. -->

## Playbooks

Open a todolist whose first items are the matched playbook's steps, copied in verbatim, before any task-specific todos. Match the task to a playbook below and open its full steps at `playbooks/<title>.md`.

- <!-- **<Playbook Name>.** <When to use this playbook.> (`playbooks/<name>.md`) -->
