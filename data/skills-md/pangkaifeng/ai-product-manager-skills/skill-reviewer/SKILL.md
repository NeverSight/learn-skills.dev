---
name: skill-reviewer
description: >
  Skill 评审 / Skill 审计：当用户要检查、评审、优化 Codex/Agent Skill 或 SKILL.md 时使用。
  可用中文唤起：“帮我 review 这个 Skill”“检查这个 SKILL.md”“这个能力适不适合做成 Skill”
  “优化 Skill 触发描述”“看下这个 Skill 有没有问题”。重点检查触发边界、输入输出、工作流门槛、
  工具边界、context budget、资源拆分、评估准备度和治理风险。
---

# Skill 评审器（skill-reviewer）

## 中文速查

- 中文名：Skill 评审器 / Skill 审计
- 英文稳定名：`skill-reviewer`
- 你可以这样叫我：`帮我 review 这个 Skill`、`检查这个 SKILL.md`、`这个能力适不适合做成 Skill`、`优化 Skill 触发描述`
- 适合：评审 Skill 质量、触发边界、输入输出、工具边界、资源组织、评估设计和团队复用风险
- 不适合：直接创建新 Skill；创建或导入新 Skill 优先用 `team-skill-creator`

## Overview

使用这个 Skill 做团队级 Skill 评审。把 Skill 当作可复用能力单元，而不是一段长提示词。从目标倒推：触发契约、输入输出契约、工作流门槛、工具边界、随包资源、context budget、评估闭环和治理方式都必须服务于目标结果。

## Workflow

1. 定位待评审对象。优先使用包含 `SKILL.md` 的 Skill 目录；如果用户只提供文本，就评审文本并说明目录/资源检查不可用。
2. 在给最终建议前建立评审上下文：目标用户、业务/领域目标、预期触发语、运行环境、所需工具、输入输出、失败成本、复用频率和当前痛点。
3. 如果缺少关键上下文，最多问 5 个具体问题。不要因可选上下文阻塞；如果用户要求快速评审，就在明确假设下继续。
4. 当本地 Skill 目录或 `SKILL.md` 路径可用时，运行确定性检查：

```bash
python3 <this-skill>/scripts/check_skill.py /path/to/skill-or-SKILL.md
```

5. 边检查边建立 Evidence Summary：读了哪些文件、跑了哪些命令、确定性发现、直接观察、推断判断和假设。
6. 涉及团队交付、评分、非平凡优化、context budget 或跨生态元数据时，读取 `references/team-skill-rubric.md`。
7. 涉及行业级评审、跨 harness 资产或最佳实践问题时，读取 `references/industry-skill-patterns.md`。
8. 只有在需要验证 `SKILL.md` 声明时，才深入检查 `references/`、`scripts/`、`assets/`、eval 文件或示例 prompt。
9. 输出按优先级排序的问题和具体修复方案。用户要求优化时，优先给可执行 patch、重写段落、脚本建议或 eval 清单，而不是只评论。

## Context Intake

Confirm the following before final review, or write them as assumptions:

- Purpose: what repeatable task the Skill supports, and why it should be a Skill rather than a prompt, tool, workflow, plugin, or app.
- Users: who invokes it, how they naturally ask, and whether it is personal, team, or production-grade.
- Trigger examples: 3-5 requests that should trigger it and 2-3 that should not.
- Inputs and outputs: required user input, discoverable environment context, final deliverable, output format, and Definition of Done.
- Execution boundary: tools, scripts, APIs, permissions, side effects, sandbox constraints, confirmation requirements, and fallback behavior.
- Evaluation: success criteria, smoke prompts, non-trigger prompts, deterministic checks, capability evals, regression traces, grader type, and release requirements.

Only ask questions that materially affect the review. If the artifact already answers a question, do not ask it again.

## Evidence Levels

Use these labels for high-priority findings:

- `deterministic`: script output, file existence, frontmatter, command output, schema checks, or other mechanical evidence.
- `observed`: direct reading of `SKILL.md`, references, scripts, assets, evals, or sample artifacts.
- `inferred`: design judgment based on the Skill goal, structure, and likely failure modes.
- `needs context`: missing business goal, user profile, runtime environment, or failure cost prevents a final judgment.

Do not present inferred or needs-context findings as deterministic failures.

## Review Dimensions

Check these dimensions in order:

1. Necessity and boundary: repeated value, stable failure modes, clear scope, and not better handled by a deterministic tool or one-off prompt.
2. Trigger contract: `description` is trigger-first, covers natural-language use, and avoids being a workflow summary; non-trigger boundaries are clear when needed.
3. Input/output contract: required inputs, discoverable context, deliverables, output format, and Definition of Done are explicit.
4. Workflow gates and degrees of freedom: steps are actionable; the Skill says when to ask, assume, stop, retry, escalate, confirm, or verify.
5. Progressive disclosure and assets: `SKILL.md` stays concise; details go to `references/`; deterministic logic goes to `scripts/`; templates/static resources go to `assets/`.
6. Context budget: metadata, body, references, scripts, tools, and schema exposure are bounded and not duplicated.
7. Tool and safety boundary: permissions, side effects, destructive operations, credentials, network use, tool failures, and fallback behavior are clear.
8. Evaluation readiness: smoke prompts, non-trigger prompts, capability evals, regression evals, deterministic graders, and model/human graders are appropriate to risk.
9. Maintainability and governance: naming, ownership, compatibility, version/deprecation expectations, shared resources, and update path are clear.

## Definition of Done

A review is complete only when it includes:

- Verdict: `Ready`, `Needs revision`, or `Not a good Skill candidate`.
- Evidence Summary: what was inspected, what commands ran, what was not verified, and what assumptions were made.
- P0/P1/P2 findings sorted by severity, each with evidence level, evidence, impact, and repair.
- A scorecard covering the review dimensions.
- Explicit assumptions or blocking questions when context is incomplete.
- A concrete improvement artifact when useful: rewritten `description`, section structure, patch, script suggestion, or eval checklist.

## Output Format

Use this structure:

```markdown
**Evidence Summary**
- Files inspected: <paths or "not available">
- Commands run: <commands or "none">
- Evidence limits: <assumptions, missing context, or unavailable checks>

**Verdict**
<Ready / Needs revision / Not a good Skill candidate>，用 1-2 句话说明理由。

**Highest Priority Issues**
- [P0/P1/P2][deterministic/observed/inferred/needs context] <issue>: <why it matters>. Evidence: <file/line, command output, or cited observation>. Repair: <specific change>.

**Scorecard**
| Dimension | Score | Notes |
|---|---:|---|
| Necessity and boundary | 0-5 | ... |
| Trigger contract | 0-5 | ... |
| Input/output contract | 0-5 | ... |
| Workflow gates and degrees of freedom | 0-5 | ... |
| Progressive disclosure and assets | 0-5 | ... |
| Context budget | 0-5 | ... |
| Tool and safety boundary | 0-5 | ... |
| Evaluation readiness | 0-5 | ... |
| Maintainability and governance | 0-5 | ... |

**Recommended Patch**
<Include rewritten description, section outline, script suggestion, or patch when useful. Omit if not useful.>

**Eval Checklist**
<Minimum smoke prompts, non-trigger prompts, deterministic checks, or regression cases when useful.>

**Open Questions**
<Only questions that block a more certain judgment.>
```

Severity rules:

- `P0`: makes the Skill unusable, unsafe, or obviously mis-triggered in normal use.
- `P1`: causes unstable output, hidden failure, major context bloat, or poor team reuse.
- `P2`: maintainability, clarity, evaluation, or governance improvement that should be handled but does not block use.

## Resource Guide

- Use `scripts/check_skill.py` for deterministic structure, frontmatter, resource, and soft-warning checks.
- Use `references/team-skill-rubric.md` for detailed scoring anchors, evidence levels, common anti-patterns, and improvement patterns.
- Use `references/industry-skill-patterns.md` for trigger-only description, fresh verification evidence, context budget, workflow gates, eval taxonomy, cross-harness metadata, and goal-backward review.
