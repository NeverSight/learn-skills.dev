---
name: wtk-qa
description: "Run one tagged QA planning or execution phase through `/wtk-qa [plan] <flow>`. Use for verifier-owned journey work."
argument-hint: "[plan] <flow>"
---

# QA

Run this phase for: $ARGUMENTS. If empty, stop and ask for the flow.

Use the accepted `qa` stage through [agent selection](../wtk/references/agent-selection.md).
The coordinator dispatches or reuses a non-author checking session in the current checkout;
this wrapper does not automatically fork or require a named role. A session that authored the
product change returns dispatch responsibility to the coordinator before walking QA.

Run exactly one phase over journeys tagged with the flow: [wtk-qa-plan](../wtk-qa-plan/SKILL.md)
when the first argument is `plan`, else [wtk-qa-execute](../wtk-qa-execute/SKILL.md).
Read only that phase skill in full. If no journey carries the tag, report and stop.
