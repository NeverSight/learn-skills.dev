---
name: chooseable-options
description: when configuring user choices across plans, studies, workflows. Routing matrix, MCP skill indexes, API menus. Not for standalone use.
---

# GG → Chooseable Options → Decision Menus

> **Snapshot age:** reviewed `2026-04-21` (~12 days old as of today).
> Verify release-sensitive answers with the skill indexes before responding with high confidence.

## Overview

Use this skill to answer "what are the next logical steps here?" with a compact option menu.
Print SCREAMING_SNAKE_CASE tokens in chat, and when the harness exposes an Ask User tool, also
open that native picker so the user can choose without typing a token. It is the lightweight
router for next-step selection across workflow, quality, governance, and specialist-skill lanes.

This skill is not a replacement for planning, decisions, study, or step-by-step execution. Its job
is to normalize the current situation, recommend the best next route, and make the available
alternatives easy to scan before the user commits to a lane.

## When to Use This Skill

**TRIGGER when:**
- The user explicitly asks what to do next, asks for chooseable options, or asks for the next logical steps.
- A study, plan, spec, audit, or session-analysis artifact exists and several plausible next actions compete for attention.
- The user wants a compact routing menu before entering planning, decisions, step-by-step, study, research, or skill-authoring workflows.
- A skill-authoring or governance task needs a context-aware menu of likely next actions.

**SKIP when:**
- A deeper workflow is already explicitly chosen and should run directly.
- The current state is a single blocker choice that needs the decisions workflow.
- The work is already an ordered manual queue that needs step-by-step execution.

## Common Misconceptions

| # | Misconception | Correction | Key concept |
|---|---------------|------------|-------------|
| 1 | This skill replaces planning, decisions, study, or step-by-step workflows. | It is a router only. It recommends the lane and then hands off to the owning skill. | Router, not executor |
| 2 | The skill reads every SKILL.md file in full to build the menu. | It uses the two-layer model: inventory awareness first, then targeted reads of shortlisted skills only. | Two-layer awareness |
| 3 | The skill invents routes when the matrix does not cover the scenario. | It escalates to the appropriate workflow skill instead of improvising. | Escalation over invention |
| 4 | More options makes the menu more helpful. | The first-pass menu must stay compact: 3-7 options maximum. | Compact first pass |
| 5 | The skill embeds the full downstream workflow after the user chooses. | It hands off explicitly, passing the normalized scenario and downstream target. | Explicit handoff |
| 6 | Any routing matrix entry can be used | Use reviewed routes only; escalate if matrix is unclear | Matrix fidelity |
| 7 | Printing tokens is enough when an Ask User tool exists. | Print the token list **and** invoke the native picker in the same turn. | Dual surface |
| 8 | Invent an Ask User tool when the harness has none. | If no matching tool is in this turn's list, the printed list is complete. | Availability, not invention |

## Non-Negotiable Policy

1. Treat this skill as a router and option presenter only.
2. Always normalize the current scenario before offering next actions. Use `references/context-normalization.md`.
3. Use the two-layer awareness model: inventory awareness from the project skill index first, then targeted `SKILL.md` reads for shortlisted candidates only.
4. Treat `references/routing-matrix.md` as the reviewed routing layer. Do not improvise routes from memory.
5. Present exactly one recommended option first. Keep the first-pass menu to 3-7 options.
6. Every option must name the downstream owning skill or workflow.
7. Always print `CHOOSEABLE_OPTIONS` as SCREAMING_SNAKE_CASE tokens with descriptions. When an Ask User tool is in this turn's tool list, also invoke it in the same turn (see `references/ask-user-harness.md`). Do not require the user to type a token when a picker is available.
8. Escalate instead of overloading this skill:
   - blocker-rich choice space -> `decisions/SKILL.md`
   - ordered human-in-the-loop queue -> `step-by-step/SKILL.md`
   - ready implementation scope -> `plan/SKILL.md`
   - insufficient evidence -> `study/SKILL.md` or `research-online/SKILL.md`
9. If the routing matrix shows `REVIEW_REQUIRED` for a changed skill surface, update the matrix before closure whenever it is safe to do so.

## Output Contract

Default user-facing output:

1. `Current scenario`
2. `Why these are the next logical steps`
3. `CHOOSEABLE_OPTIONS` (printed tokens **and** native picker when available)
4. `What happens after selection`

`CHOOSEABLE_OPTIONS` rules:

1. Recommended option first.
2. Flat bullets in chat, always:

```markdown
CHOOSEABLE_OPTIONS
- `WRITE_IMPLEMENTATION_PLAN` (Recommended): Create an execution plan from this study → plan
- `DECIDE_OPEN_QUESTIONS`: Resolve remaining blockers → decisions
- `EXPLAIN_FINDINGS_VISUALLY`: Thorough HTML explanation → explain
```

3. Each option names the owning downstream skill or workflow.
4. Use concise action names that scan cleanly in terminal-based AI tools.
5. In the same turn, if an Ask User tool is available, invoke it using `references/ask-user-harness.md` so the user can pick without typing a token.

## Options Quality Checklist

Use this checklist before presenting any option menu.

| # | Checklist Item | Why It Matters | Gate |
|---|---------------|---------------|------|
| 1 | **Scenario normalized** — Context from context-normalization.md applied | Enables informed routing | Pre-menu |
| 2 | **Skill index consulted** — Candidate routes identified from project index | Enables two-layer model | Pre-menu |
| 3 | **Routing matrix reviewed** — Shortlisted routes from routing-matrix.md | Ensures matrix fidelity | Pre-menu |
| 4 | **Recommended option first** — Best route appears as first option | Enables fast decision | Draft |
| 5 | **Menu compact** — 3-7 options maximum | Prevents overwhelming | Draft |
| 6 | **Options scoped** — Each option names owning skill/workflow | Enables clarity | Draft |
| 7 | **Escalation path clear** — Routes not covered escalate properly | Prevents improvisation | Draft |
| 8 | **Handoff ready** — Normalized scenario passed to downstream skill | Enables continuity | Closeout |
| 9 | **Native picker** — Ask User tool invoked when present this turn | Lets the user choose without typing tokens | Closeout |

### Quality Tiers

| Tier | Criteria | Use When |
|------|----------|----------|
| **Minimal** | Items 1-4, 8 | Simple routing decision |
| **Standard** | Items 1-6, 8-9 | Multi-option routing |
| **Full** | All 9 items | Complex governance scenarios |

### Pre-Presentation Verification

```
□ Scenario normalized using context-normalization.md
□ Skill index consulted for candidate routes
□ Routing matrix reviewed for shortlisted routes
□ Recommended option is first
□ Menu has 3-7 options
□ Each option names owning skill
□ Escalation paths clear for uncovered scenarios
□ Handoff ready with normalized scenario
□ Native Ask User tool invoked if it is in this turn's tool list
```

## Options Consistency Validator

Before presenting, verify:

### Consistency Check Matrix

| Check | What to Verify | How to Fix |
|-------|---------------|------------|
| **Scenario vs Routes** | Routes match normalized scenario | Re-normalize |
| **Routes vs Matrix** | Routes from routing matrix, not improvised | Use matrix |
| **Options vs Skills** | Each option names owning skill | Add skill name |
| **Handoff vs Scenario** | Downstream receives normalized scenario | Prepare handoff |
| **Picker vs Tokens** | Native picker options match the printed token list (same tokens, recommended first) | Rebuild both from one option set |

### Red Flags (Never Present)

- [ ] Options without owning skill named
- [ ] Menu with more than 7 options
- [ ] Recommended option not first
- [ ] Improvised routes not in matrix
- [ ] Scenario not normalized before routing
- [ ] Ask User tool present this turn but only a text list was shown

## Workflow

1. Normalize the active scenario with `references/context-normalization.md`.
2. Read the project skill index to shortlist candidate routes.
3. Open only the most relevant shortlisted `SKILL.md` files.

| Task type | Load these surfaces first | Skip |
|-----------|--------------------------|------|
| Study artifact | `Post-Study Proposals`, deepening section, frontmatter `description` | Unrelated workflow skills |
| Governance | Project-local skill manager `SKILL.md` | Specialist execution skills |
| Specialist | Target specialist `SKILL.md`, `AUTO_TRIGGER_WHEN`, `Cross-Skill Coordination` | Broad workflow skills unless sequencing is needed |
| Open-ended / router | `references/routing-matrix.md`, frontmatter `description`, `AUTO_SUGGEST_WHEN` | Full corpus reads |
| Presenting the menu | `references/ask-user-harness.md` | Unrelated workflow skills |

Load only the subset the task needs.

4. Use `references/routing-matrix.md` to choose the recommended first route, secondary routes, and skills that should not be suggested in the current scenario.
5. Build the compact option set.
6. Print the token list. If an Ask User tool is in this turn's tool list, invoke it in the same turn (`references/ask-user-harness.md`).
7. Hand off explicitly after the user chooses (picker answer or typed token). Pass the normalized scenario summary and downstream skill target.

## Cross-Skill Coordination

- `plan/SKILL.md` - hand off when evidence is sufficient for durable implementation planning.
- `decisions/SKILL.md` - use when unresolved blocker choices, approvals, or tradeoffs need a richer decision surface.
- `step-by-step/SKILL.md` - use when the work is already an ordered manual queue.
- `study/SKILL.md` - use when context is too ambiguous for confident routing, or a completed study needs bounded deepening before planning.
- `explain/SKILL.md` - use when the artifact is too dense, or a completed study with a chosen direction needs a "what can already be implemented now?" bridge.
- `research-online/SKILL.md` - use when current external facts are the missing evidence for ranking next steps.
- Project-local skill manager - use when the next action is skill authoring or lifecycle review.

## HANDOFF_OUTPUTS

### To downstream workflow or governance skills

- normalized scenario key
- short explanation of why the route is recommended
- alternative routes that remained viable
- notable `Do Not Route To` exclusions from the routing matrix
- any missing evidence or review obligations

### To `plan/SKILL.md`

- source artifact path or summary
- recommended execution sequence
- unresolved blockers or follow-up studies

### To `decisions/SKILL.md`

- active blocking choice summary
- upstream artifact path
- recommended option if one exists

### To `step-by-step/SKILL.md`

- normalized manual queue or queue source
- current active step candidate
- verification notes already known

### To `explain/SKILL.md`

- source artifact path or explanation target
- exact question the explanation should answer
- chosen direction and explicit non-goals when the source is a completed study
- concrete implementation-ready change inventory when the ask is "what can already be implemented now?"
- recommended downstream lane after explanation

### To `study/SKILL.md`

- source artifact path
- exact reason the router recommends a bounded study-deepening pass
- whether deeper analysis should stay visible
- alternative lanes that remain viable after the deepening pass

### To skill-authoring manager skills

- whether the change is new-skill or materially-changed-skill work
- whether chooseable-options review was completed
- repeated-`--skill-path` publish requirement when the matrix changed

## Common Pitfalls

1. **Reading every SKILL.md file.** The two-layer model requires inventory awareness first, then targeted reads. Opening every skill file defeats the purpose of lightweight routing.
2. **Ignoring the study's own closeout proposals.** When the source is a study, always inspect its `Post-Study Proposals` before overriding with general routing.
3. **Presenting implementation before resolving blockers.** The route-selection rules state: prefer blocker resolution before implementation. See `references/context-normalization.md`.
4. **Forcing planning when evidence is thin.** If the concrete change inventory, regression scope, or doc blast radius is still underexplored, keep a bounded study-deepening option visible.
5. **Omitting the explanation lane for ready studies.** When a completed study has a chosen direction and concrete implementation-ready inventory, keep `explain/SKILL.md` visible as the "what can already be implemented now?" bridge.
6. **Skipping the native picker when an Ask User tool is available.** Print tokens and call the picker in the same turn. See `references/ask-user-harness.md`.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Too many options in the first-pass menu | Not applying the 3-7 option limit or failing to group related choices | Group into `IMPLEMENTATION_OPTIONS`, `RESEARCH_OPTIONS`, etc., and present the recommended group member first |
| Routing matrix shows `REVIEW_REQUIRED` for a skill used this turn | A skill changed routing semantics without matrix update | Update the relevant row in `references/routing-matrix.md` before closing the turn |
| Recommended route contradicts the artifact's own closeout menu | The artifact's closeout was written before a skill change | Honor the artifact's closeout unless new evidence clearly contradicts it; note the discrepancy |
| User rejects all options and asks for more | Scenario was under-normalized or evidence is too thin | Re-run normalization with `references/context-normalization.md` or escalate to `study/SKILL.md` |
| User has to type a token even though a picker exists | Native Ask User tool was not invoked | Call the matching tool from `references/ask-user-harness.md` in the same turn as the printed list |
| Picker failed or tool missing | Harness has no Ask User tool this turn | Keep the printed SCREAMING_SNAKE_CASE list; do not invent a tool |

## Local Corpus Layout

`references/` contains 3 flat files (no subfolders):

- `context-normalization.md` - scenario-detection order, evidence inputs, escalation rules, ranking and tie-break logic.
- `routing-matrix.md` - reviewed routing lanes, in-batch workflow coverage, expert capability bridges, pending review queue.
- `ask-user-harness.md` - detect and call the current harness's Ask User tool; map tokens onto native options.

## Guidance Alignment

- Apply repository guidance consistently with the project's top-level guidance files (for example `AGENTS.md` or equivalent).
- Snapshot verified: `2026-04-21`.
- If this skill or another skill changes routing semantics, review `references/routing-matrix.md` in the same workflow and run the project skill sync command so IDEs pick up the new version.
- When the source artifact is a study, inspect that study's own `Post-Study Proposals` and any study-local deepening guidance before composing the final option menu.
