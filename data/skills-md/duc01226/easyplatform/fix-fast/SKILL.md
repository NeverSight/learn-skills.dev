---
name: fix-fast
description: '[Fix & Debug] ⚡ Analyze and fix small issues [FAST]'
argument-hint: [issues]
---

Analyze the skills catalog and activate the skills that are needed for the task during the process.

## ⚠️ Anti-Hallucination Reminder

**Be skeptical. Critical thinking. Everything needs traced proof.** — Never accept code at face value; verify claims against actual behavior, trace data flow end-to-end, and demand evidence (file:line references, grep results, runtime confirmation) for every finding.

**Before modifying ANY code:** Verify assumptions with actual code evidence. Search for usages, read implementations, trace dependencies. If confidence < 90% on any change, investigate first or ask user. See `.claude/skills/shared/anti-hallucination-protocol.md` for full protocol.

## Mission

**Think hard** to analyze and fix these issues:
<issues>$ARGUMENTS</issues>

## Workflow

1. If the user provides a screenshots or videos, use `ai-multimodal` skill to describe as detailed as possible the issue, make sure developers can predict the root causes easily based on the description.
2. Use `debugger` subagent to find the root cause of the issues and report back to main agent.
3. Activate `debug` skills and `problem-solving` skills to tackle the issues.
4. Start implementing the fix based the reports and solutions.
5. Use `tester` agent to test the fix and make sure it works, then report back to main agent.
6. If there are issues or failed tests, repeat from step 2.
7. After finishing, respond back to user with a summary of the changes and explain everything briefly, guide user to get started and suggest the next steps.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
