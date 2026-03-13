---
name: deepthink
description: Invoke IMMEDIATELY via python script when user requests structured reasoning for open-ended analytical questions. Do NOT explore first - the script orchestrates the thinking workflow.
---

# DeepThink

Structured multi-step reasoning for open-ended analytical questions where the
answer structure is itself unknown. Handles taxonomy design, conceptual
analysis, trade-off exploration, and definitional questions.

## Invocation

<invoke working-dir=".claude/skills/scripts" cmd="python3 -m skills.deepthink.think --step 1 --total-steps 14" />

Do NOT explore or analyze first. Run the script and follow its output.
