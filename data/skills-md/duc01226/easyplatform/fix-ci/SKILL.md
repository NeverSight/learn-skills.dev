---
name: fix-ci
description: '[Fix & Debug] ⚡ Analyze Github Actions logs and fix issues'
argument-hint: [github-actions-url]
---

## ⚠️ Anti-Hallucination Reminder

**Be skeptical. Critical thinking. Everything needs traced proof.** — Never accept code at face value; verify claims against actual behavior, trace data flow end-to-end, and demand evidence (file:line references, grep results, runtime confirmation) for every finding.

**Before modifying ANY code:** Verify assumptions with actual code evidence. Search for usages, read implementations, trace dependencies. If confidence < 90% on any change, investigate first or ask user. See `.claude/skills/shared/anti-hallucination-protocol.md` for full protocol.

## Github Actions URL

<url>$ARGUMENTS</url>

## Workflow

1. Use `debugger` subagent to read the github actions logs with `gh` command, analyze and find the root cause of the issues and report back to main agent.
2. Start implementing the fix based the reports and solutions.
3. Use `tester` agent to test the fix and make sure it works, then report back to main agent.
4. If there are issues or failed tests, repeat from step 2.
5. After finishing, respond back to user with a summary of the changes and explain everything briefly, guide user to get started and suggest the next steps.

## Notes

- If `gh` command is not available, instruct the user to install and authorize GitHub CLI first.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
