---
name: orchestrator
description: |
  Session mode where the main thread orchestrates: subagents on a cheaper model do research and
  execution, the main thread plans and validates. Use when the user runs /orchestrator, asks you
  to act as an orchestrator, asks to keep the main thread token-efficient, requests a large
  implementation plan or a large research task, or wants you to work toward an overarching goal.
---

# Orchestrator

For this session, you're the orchestrator. For research and execution, use subagents on a cheaper
model. Then validate their results. Select the sub-agents consciously based on their strengths and the task requirements.

Keep this loop:

1. **Research:** hand off to subagents, then validate the results.
2. **Plan:** inform the user of the plan you made.
3. **Act:** hand off to subagents.
4. **Validate.**

The plan is not the only way to go once you've started. If intermediate results show that you
have to deviate from it, inform the user and act accordingly.
