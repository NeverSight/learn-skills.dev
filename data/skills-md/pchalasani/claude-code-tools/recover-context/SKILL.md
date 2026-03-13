---
name: recover-context
description: Extract full context of the last task from the most recent parent session
  shown in the session lineage. Strategically uses sub-agents to avoid bloating your
  own context.
---

# recover-context

Use this skill to extract context from a parent session when a session lineage is
present (shown in the first user message of this conversation).

## Instructions

1. **Identify the most recent parent session** from the lineage chain (the last
   file in the chronological list).

2. **Use sub-agents to explore** (to avoid bloating your own context):
   - If you have the Task tool with subagent support, use the `session-searcher`
     subagent (subagent_type: `session-searcher`) to analyze the most recent session
   - If sub-agents are NOT available, use the `aichat:session-search` skill instead

3. **Extract the following from the most recent session:**
   - What was the last task being worked on?
   - What was the current state of that task (completed, in-progress, blocked)?
   - Any pending items or next steps mentioned?
   - Key decisions made or approaches chosen

4. **Also check for associated documents:**
   - Issue specs or task descriptions referenced in the session
   - Any markdown files created during that session (check WORKLOG/, issues/, etc.)
   - Code files that were being modified

5. **Report back concisely:**
   - State your understanding of the task context
   - List any files you found that are relevant
   - Ask the user how they'd like to proceed

## Example Sub-agent Prompt

If using the Task tool with `session-searcher` subagent:

```
Analyze the session file at [path from lineage] and extract:
1. The last task being worked on (look at the final 20-30 messages)
2. Current state of that task
3. Any referenced markdown files (issue specs, work logs, etc.)
4. Pending next steps or blockers

Return a concise summary.
```

## Constraints

- Do NOT read large session files directly into your own context
- ALWAYS delegate to sub-agents or the session-search skill
- Keep your summary concise - the user knows what they were working on
- Focus on the LAST task, not the entire session history
