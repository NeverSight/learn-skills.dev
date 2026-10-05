---
name: grill-design
description: "Clarify and record user-confirmed UI design requirements through focused question sets, optionally after grill-workflow and before prototype or specification. Use when the user wants custom visual direction, design preferences, or resolution of a design conflict; do not use for product scope or implementation."
---

# Grill Design

Turn the user's design intent into a scoped, inspectable agreement that
`$ui-design` can apply. This is an optional design-discovery workflow; it does
not generate UI or modify the reusable `ui-design` skill.

## Read and establish scope

Read `AGENTS.md` if present, relevant product decisions from `$grill-workflow`,
`docs/requirement.md`, `CONTEXT.md`, existing brand/design guidance, and relevant
specs/prototypes or nearby UI. Read only the surface being discussed.

Identify the project, feature, or screens to which the design applies. Reuse
confirmed answers rather than asking again. Do not infer preferences from the
current implementation or from a reference the user has not explained.

If product scope or primary behavior is materially unsettled, return that
question to `$grill-workflow`. Keep design discovery separate from permission,
data, business-rule, and architecture decisions.

## Ask focused sets

Ask one manageable set per turn, grouping independent questions whose
prerequisites are known. Give questions stable IDs, keep partial answers, and
use replies to select the next relevant set. Do not ask a fixed questionnaire
or require the user to choose every CSS token.

Cover only consequential gaps, for example:

- Intended feeling and audience: what should the interface communicate?
- References and anti-references: which specific qualities should carry over
  or be avoided? A reference is not permission to copy every part of it.
- Existing brand/assets and what must be preserved versus may be changed.
- Content density, hierarchy, layout, navigation presentation, and prominent
  actions within the already agreed behavior.
- Color, typography (including language support), surfaces, imagery/icons,
  and motion when these affect the desired direction.
- Relevant devices, themes, interaction states, and accessibility constraints.

Use concrete alternatives and consequences when helpful. Translate vague
words such as "modern" or "premium" into observable choices before recording
an agreement. For example, clarify whether "compact" means less decorative
spacing, more visible records, or smaller controls; those choices differ.
Offer a recommendation grounded in the domain when the user wants guidance,
but keep it a Proposal until confirmed. "You decide" can explicitly delegate
specified choices; record that latitude instead of inventing confirmed values.

Respect explicit styling preferences even when they differ from the defaults
in `ui-design`. Identify feasibility or accessibility conflicts with concrete
consequences and ask for a workable resolution; do not silently replace the
user's requested direction with the agent's aesthetic.

## Confirm and record

Distinguish Fact, Proposal, Agreed, and Open question. Record clear user answers
as Agreed; ask only about ambiguous or conflicting answers. Before finishing,
show a concise consolidated brief and obtain confirmation of any synthesized
choices that have not already been explicitly agreed. Silence is not consent.

Use the existing authoritative design-requirements location if the project
already has one; otherwise use `## UI Design Requirements` in
`docs/requirement.md`. Preserve unrelated content and update existing entries
rather than appending competing briefs. Link the record in the final handoff.

Use this minimum shape, adapted to the project's established document style:

```markdown
## UI Design Requirements

- Scope: <project, feature, or named screens>
- Status: Agreed | draft
- Source: <explicit user decisions or authoritative existing record>
- Discovery: completed | pending

| ID | Scope | Status | Kind | Design decision | Basis / reference | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| D-01 | <scope> | Agreed / Proposal | constraint / preference / delegated | <observable choice> | <confirmed answer or reference aspect> | <relevant visual or interaction check> |

### Open questions

<Only unresolved choices, with their affected scope; omit when none.>
```

Mark discovery completed only when the finish condition is met, including in
a new-project summary, so setup does not repeat the opt-in or the interview.
Keep IDs stable and unique within the record. A constraint is required within
its scope; a preference guides choices where constraints leave room; delegated
choices remain implementation latitude. Record reference paths/URLs and the
specific quality selected, rather than asserting an entire reference is agreed.
Never claim a linked reference was inspected unless it was actually accessible.
Do not invent exact dimensions, fonts, assets, or numeric tokens from mood words.

Existing confirmed `CONTEXT.md` Design Direction and brand rules remain active.
If a new choice conflicts, show both and obtain explicit agreement about the
replacement or scoped exception before recording it. Record what it overrides
and where; do not rewrite source template metadata or silently erase prior
agreements. Behavioral sources remain authoritative; a design brief cannot
approve a product change or weaken task acceptance criteria.

For a new project without standard context documents, keep a confirmed handoff
summary instead of initializing partial files. `$setup-project` persists that
summary in the same authoritative location. Preserve pending design intent and
visual-validation intent through setup. Do not modify skill source files,
production code, prototype revisions, specs, tasks, or ADRs in this workflow.

## Finish and hand off

Finish when consequential design choices are agreed or explicitly delegated,
and no conflict blocks the intended UI work. Leave non-blocking details open;
do not keep interviewing merely because more preferences could be collected.

Report the scoped agreement and its path (or new-project summary), remaining
questions, and exactly one recommended next skill without invoking it:

- Unresolved product or behavioral decision → `$grill-workflow`.
- Missing project context → `$setup-project`, carrying the design summary.
- User wants to see the agreed direction → `$to-prototype` (or
  `$edit-prototype` for explicitly targeted existing revisions).
- Context ready and no visual validation requested → `$write-spec`.

If a design question still blocks completion, keep the record draft and continue
that question here. Do not mark proposals Agreed to advance the workflow.
