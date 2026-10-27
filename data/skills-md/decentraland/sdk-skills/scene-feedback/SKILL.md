---
name: scene-feedback
description: Help creators plan playtest questions and timing, integrate or debug Scene Feedback surveys in Decentraland SDK7, or analyze collected CSV ratings and comments. For audiovisual reactions to gameplay actions, use game-design or build-ui.
---

# Scene Feedback

Help creators learn how players experience their scene using Scene Feedback questions and
CSV responses. Load only the workflow needed for the current request.

## REQUIRED checkpoint before changes

**MUST reconcile prior assistant proposals with this skill on load, before a new integration
or agent-chosen content/timing edits.** An assistant suggestion
remains a proposal until the creator confirms its concrete choices. A general request to
install/connect, or approval of a technical option, alone does not approve a creative plan.

**If material choices in scope remain unreviewed, read [Planning](references/planning.md)
and [Scene context](references/scene-context.md) before writing receiving-scene files.**
Present a compact reviewable plan covering unresolved goal, questions/Intro, formats/scales,
moments, and participation route, with the three planning paths. Apply those choices only
after the creator accepts the concrete plan. Retain explicit instructions and approved
choices; an approved exact edit or plan proceeds without a renewed interview.

When updating project notes, distinguish creator-approved decisions, assistant proposals,
and implemented facts; implementation itself does not establish approval.

## Explain choices in creator language

Use ordinary language matched to demonstrated creator familiarity. Explain technical terms
on first use through their purpose, such as an invitation asking players whether to give
feedback (Intro). Present question wording, rating labels/meaning, and player moments;
pair useful bank/scale/event IDs with their meaning in creator review. Retain exact
identifiers in code and configuration.

## Choose the route

| Request | Read next | Scope |
| --- | --- | --- |
| Choose a playtest focus, propose/adapt questions, scales, or timing | [Planning](references/planning.md) | Ground the proposal in the scene or brief and review creator-facing choices before applying them. |
| Install, wire events, apply approved edits, or update the module | [Integration](references/integration.md) | Inspect the current installation first; reuse it and change only what the task needs. |
| Check/debug existing behavior or test devices/Storage | [Verification](references/verification.md) | Inspect configuration and hooks, then run relevant checks. |
| Download responses only | [World Storage retrieval](https://github.com/decentraland/sdk7-test-scenes/blob/main/scenes/0,-1-scene-feedback/README.md#4-review) | Explain retrieval without starting a full analysis. |
| Analyze collected CSV ratings/comments or compare playtests | [Analysis](references/analysis.md) | Start with the exports and goal; offer optional HTML. |

A request may enter any route directly. Reuse supplied goals and approved decisions. For an
existing integration, distinguish a question/configuration edit from installation or update;
for CSV analysis, the exports can be sufficient without access to scene source. Finish the
requested scope rather than automatically continuing through every workflow.

Follow cross-links only when the next action needs that branch. Within a workflow, read the
linked module documentation sections for configuration, API, examples, and CSV semantics;
they remain the source of truth. Prefer relevant sections or local matching module docs to
loading every document, and disclose any version mismatch that affects the work.
