---
name: design-map
description: "Visualize the design discussed so far as an artifact page with architecture diagrams, decisions, alternatives, and open questions. Use when the user asks to see the current design as an artifact, diagram, or map. matt-design owns design interviews and spec confirmation; matt-auto owns implementation."
---

# Design Map

Render the current design so the user can inspect it. Work from the conversation,
a supplied spec (draft or confirmed), or matt-design's current decision table.
Do not restart the interview, make missing design decisions, confirm a spec,
create tickets, or launch implementation. A draft with open questions is a valid
input, not a reason to demand a confirmed spec.

1. **Collect the current design.** Reuse the supplied goals, actual module names,
   structure, alternatives, settled decisions, and open questions. Read relevant
   files only to resolve factual gaps. If there is no design content at all,
   ask for the topic/source or suggest `$matt-design`; do not invent a design.
2. **Map the evidence.** Distinguish existing structure, proposed changes,
   user-confirmed decisions, and unresolved choices. Show the available detail;
   mark unknowns explicitly. Do not run a self-grill or select alternatives on
   the user's behalf. Preserve decision ids when supplied.
3. **Render the artifact.** Follow
   [references/artifact-page.md](references/artifact-page.md) for the page,
   diagram geometry, theme checks and feedback. On Codex also read
   [references/codex-delivery.md](references/codex-delivery.md). Invoking this
   skill to visualize is already a request for the page; do not ask again.
   Use Korean prose/labels and real code identifiers. Keep diagrams small and
   legible; split overviews/details instead of compressing a large structure.
4. **Deliver and iterate.** Verify the rendered page, then give its artifact
   link, delivered URL/tab, or local HTML path and reason. Reuse the same route
   for updates. Visual corrections update the page. Design feedback is an open
   change request for the caller or `$matt-design`; preserve it in the page
   without silently changing a confirmed decision or spec. When the user
   settles it in the design conversation, render the updated design.

The page visualizes the source; it does not replace the spec or authorize work.
Do not write a new implementation spec or offer an execution handoff as part of
visualization. If tools cannot publish, return the HTML file and explain the
limitation. If render verification cannot run, report that limitation explicitly.

## Legacy execution requests

An explicit request to execute a previously confirmed design-map spec belongs
to `$matt-auto --spec <path>`, not this renderer. Read
[references/codex-execution.md](references/codex-execution.md) only for that
legacy request. Ordinary visualization never enters it.
