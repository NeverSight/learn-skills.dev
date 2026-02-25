---
name: fix-test
description: '[Fix & Debug] ⚡⚡ Run test suite and fix issues'
argument-hint: [issues]
---

Analyze the skills catalog and activate the skills that are needed for the task during the process.

## ⚠️ Anti-Hallucination Reminder

**Be skeptical. Critical thinking. Everything needs traced proof.** — Never accept code at face value; verify claims against actual behavior, trace data flow end-to-end, and demand evidence (file:line references, grep results, runtime confirmation) for every finding.

**Before modifying ANY code:** Verify assumptions with actual code evidence. Search for usages, read implementations, trace dependencies. If confidence < 90% on any change, investigate first or ask user. See `.claude/skills/shared/anti-hallucination-protocol.md` for full protocol.

## Reported Issues:

<issues>$ARGUMENTS</issues>

## Workflow:

1. Use `tester` subagent to compile the code and fix all syntax errors if any.
2. Use `tester` subagent to run the tests and report back to main agent.
3. If there are issues or failed tests, use `debugger` subagent to find the root cause of the issues, then report back to main agent.
4. Use `planner` subagent to create an implementation plan based on the reports, then report back to main agent.
5. Use main agent to implement the plan step by step.
6. Use `tester` agent to test the fix and make sure it works, then report back to main agent.
7. Use `code-reviewer` subagent to quickly review the code changes and make sure it meets requirements, then report back to main agent.
8. If there are issues or failed tests, repeat from step 2.
9. After finishing, respond back to user with a summary of the changes and explain everything briefly, guide user to get started and suggest the next steps.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
