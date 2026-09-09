---
name: distill-response
description: "Distill a prior AI response into a standalone, navigable explanation of its decision spine, or elaborate a labeled item from an earlier distillation while preserving orientation."
---

# Distill Response

Produce an executive compression: the shortest standalone explanation that
preserves the source's decision spine and gives the reader a stable map for
follow-up exploration.

## Route the Request

1. Use initial-distillation mode when the user asks to distill one or more
   assistant responses. Use the responses identified in the invocation, or the
   immediately preceding assistant response when none is identified.
2. Use elaboration mode when the user asks to expand a labeled item from an
   earlier distillation. Locate the most recent distilled map that established
   that label; do not replace it with an intervening elaboration of a sibling
   item. When the requested label is a subpart established during an
   elaboration, use that elaboration as the local source while retaining the
   original map for orientation.
3. Ask which map or item the user means only when repeated labels or multiple
   distillations make the intended source materially ambiguous.
4. Apply any requested lens or length as an additional constraint. Let
   understanding determine the length when the user gives no limit.

Use the recovery and mapping steps in both modes. Finish with **Distill** in
initial-distillation mode and **Elaborate an Item** in elaboration mode.

Finish routing when the mode and exact source material are identifiable from
the conversation.

## Recover the Decision Spine

Read the complete source and recover the content that governs understanding:

- the central conclusion or outcome;
- the mental model: the important relationships, causes, or flow;
- consequential insights and technical decisions, including their rationale;
- material tradeoffs, consequences, constraints, and uncertainties;
- critical evidence or caveats that qualify the conclusion; and
- current state and next action when the source includes them.

Use only applicable categories. Preserve the source's level of certainty and
distinctions that would change a reader's interpretation or decision. Build the
decision spine only from source-supported claims.

Finish recovery when every consequential claim within the selected scope is
represented in the decision spine.

## Build a Navigable Map

Organize the decision spine into stable, addressable ideas. Give each major
idea a short descriptive label when there is more than one idea the reader may
want to revisit. Expose the relationships among those ideas instead of leaving
the reader to reconstruct them from separate facts.

Choose the smallest form that makes those relationships clear:

- use prose for a simple conclusion or linear explanation;
- use a labeled list or short sections for several distinct ideas;
- use a table for exact mappings or comparisons; and
- use a flow, timeline, tree, or compact text diagram when sequence, causality,
  hierarchy, branching, or interaction is materially easier to understand
  visually.

Do not add a visual merely because one is possible. Every visual must make an
important relationship easier to grasp or remember than prose alone.

## Distill

In initial-distillation mode, rewrite around the decision spine rather than the
source's order. Collapse examples into the principle they establish and
repeated explanations into one clear statement. Retain an example,
implementation detail, command, path, citation, or exact value only when it is
needed to understand, verify, decide, or act.

Lead with the bottom line. Keep labels concise and consistent so the reader can
name an item in a later question without ambiguity. Supply enough context for
the result to stand alone, and emit the distilled response directly.

Finish when a reader who has not reread the source can explain what matters,
why it matters, the consequential choices and tradeoffs, and what follows. Every
remaining detail must support that explanation; removing any further content
would weaken it.

## Elaborate an Item

In elaboration mode, focus on the requested item at the requested depth. Briefly
state where it fits in the overall map and why it matters, but do not repeat the
full overview unless the explanation depends on it or the user asks for it.

Preserve the established labels for other items. When the elaboration exposes
meaningful subparts, give those subparts stable labels so the user can continue
drilling down. Use an example, analogy, or visual only when it resolves the
specific uncertainty more clearly than additional prose.

Finish when the requested uncertainty is resolved at the requested depth, the
source's certainty and caveats remain intact, and the reader can place the
expanded item back in the established map without rereading unrelated material.
