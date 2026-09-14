---
name: feature-shape
description: Explore a feature idea through conversation, repository analysis, and comparison of approaches; prepare a concise brief. Use before specification or to examine a product or architecture decision in depth. Use feature-plan for an existing brief and delivery planning.
---

# Feature Shape

Own completion of the user's requested design outcome across turns. Help the
user understand the problem and choose a direction through a coherent proposal,
then deepen the parts that need discussion. Follow requests to explore a topic
further while retaining the broader objective.
The user's instructions, earlier decisions, and requested scope take precedence
over this skill's default workflow.

## Explore

1. Establish what should change for the user and how they will recognize success.
   Reuse the conversation, existing brief, and code; do not repeat answered questions.
2. Check ownership, local instructions, and the main integration points.
   Distinguish facts confirmed in the repository from assumptions and recommendations.
3. Compare viable approaches, including a simpler solution or keeping the current
   behavior when that meets the need. Explain meaningful costs and consequences;
   recommend the simplest approach that meets today's supported workflow.
   Future scale, providers, migrations, or reuse need a concrete requirement;
   their possibility alone does not justify building support now.
4. Proactively explain the mechanism at the level needed to assess the proposal:
   data, owners, calls, persisted state, lifecycle, and failure behavior. Establish
   the overall path before drilling into individual details. Use an example or
   small diagram when helpful. Check current external documentation when a
   decision depends on a mechanism's actual guarantees.
5. Establish the smallest useful scope and what belongs later. Turn an unknown
   that could change the architecture into a specific question to investigate,
   and identify the evidence needed to resolve it.
   Make acceptable limitations explicit: safe rejection and a fresh attempt or
   bounded manual recovery may suffice without automatic recovery. Preserve
   authorization, data integrity, and resource bounds needed by the current flow.

Ask for a decision when unresolved alternatives materially change the product,
scope, or accepted trade-offs and the answer cannot be inferred from context.
Present a concrete recommendation and its consequences, focusing on one decision
at a time. Resolve technical details independently within the established
direction; continue work that does not depend on the answer. Do not treat
silence as acceptance.

After the user answers, continue the outstanding design work. A technical next
step within the requested outcome is work to perform, not a reason to end the
turn or ask the user to repeat it as a command. Keep side ideas in a short
"Later" section without expanding the current work.

## Brief

When the direction is clear enough, assemble concise input for planning:

- the goal and an example of the expected behavior;
- initial scope, exclusions, and accepted limitations with their practical cost;
- the recommended approach, a relevant alternative, and the reason for the choice;
- confirmed integration points;
- accepted decisions, proposals, and open questions;
- success criteria and the most important things to verify.

The brief may remain in the conversation. Save it when the user requests a
document or durable input for another session; follow the repository's existing
brief location and conventions. Update an existing brief instead of creating
additional versions alongside it. Do not add a process log or execution plan.

## Finish

When the requested outcome includes a specification and delivery plan, continue
into `$feature-plan` once the direction is sufficiently clear, without requiring
a separate invocation from the user. Use the conversation or brief as input;
if the skill is unavailable, prepare the requested output directly. For
exploration-only requests, keep the result within that scope. A brief does not
itself authorize implementation; preserve any existing authorization for
subsequent work.

Finish when the requested design outcome is complete or further progress needs
the user's decision after independent work is exhausted. Respond naturally in
the user's language with the result and any remaining decision or limitation.
