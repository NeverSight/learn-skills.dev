---
name: fix-hard
description: '[Fix & Debug] ⚡⚡⚡ Use subagents to plan and fix hard issues'
argument-hint: [issues]
---

**Ultrathink** to plan & start fixing these issues follow the Orchestration Protocol, Core Responsibilities, Subagents Team and Development Rules:
<issues>$ARGUMENTS</issues>

## ⚠️ MUST READ Before Starting

**Be skeptical. Critical thinking. Everything needs traced proof.** — Never accept code at face value; verify claims against actual behavior, trace data flow end-to-end, and demand evidence (file:line references, grep results, runtime confirmation) for every finding.

**IMPORTANT: You MUST read these shared protocols before any code changes. Do NOT skip.**

- **⚠️ MUST READ** `.claude/skills/shared/anti-hallucination-protocol.md` — Assumption validation, evidence chains, context anchoring
- **⚠️ MUST READ** `.claude/skills/shared/knowledge-graph-template.md` — Per-file analysis structure (for investigation phases)

**Core Rule:** Verify every assumption with actual code evidence before making changes. Search for all usages, read implementations, trace dependencies. If confidence < 90%, investigate further or ask user.

## Workflow:

If the user provides a screenshots or videos, use `ai-multimodal` skill to describe as detailed as possible the issue, make sure developers can predict the root causes easily based on the description.

### Fulfill the request

**Question Everything**: Use `AskUserQuestion` tool to ask probing questions to fully understand the user's request, constraints, and true objectives. Don't assume - clarify until you're 100% certain.

- If you have any questions, use `AskUserQuestion` tool to ask the user to clarify them.
- Ask 1 question at a time, wait for the user to answer before moving to the next question.
- If you don't have any questions, start the next step.

### Fix the issue

Use `sequential-thinking` skill to break complex problems into sequential thought steps.
Use `problem-solving` skills to tackle the issues.
Analyze the skills catalog and activate other skills that are needed for the task during the process.

1. Use `debugger` subagent to find the root cause of the issues and report back to main agent.
2. Use `researcher` subagent to research quickly about the root causes on the internet (if needed) and report back to main agent.
3. Use `planner` subagent to create an implementation plan based on the reports, then report back to main agent.
4. Then use `/code` SlashCommand to implement the plan step by step.
5. Final Report:

- Report back to user with a summary of the changes and explain everything briefly, guide user to get started and suggest the next steps.
- Ask the user if they want to commit and push to git repository, if yes, use `git-manager` subagent to commit and push to git repository.

* **IMPORTANT:** Sacrifice grammar for the sake of concision when writing reports.
* **IMPORTANT:** In reports, list any unresolved questions at the end, if any.

**REMEMBER**:

- You can always generate images with `ai-multimodal` skills on the fly for visual assets.
- You always read and analyze the generated assets with `ai-multimodal` skills to verify they meet requirements.
- For image editing (removing background, adjusting, cropping), use `ImageMagick` skill or similar tools as needed.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
