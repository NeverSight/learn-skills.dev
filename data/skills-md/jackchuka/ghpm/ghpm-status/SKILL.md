---
name: ghpm-status
description: "GitHub Project health dashboard. Shows workflow distribution, component health, team workload, items needing attention, and available views."
argument-hint: "[scope (ex. team/component)]"
allowed-tools: Bash(gh:*), Read, Grep
---

# ghpm-status

> **PREREQUISITE:** Read `../ghpm-shared/SKILL.md` for prerequisites and error handling.

Comprehensive project health dashboard. The goal is to give the user a rich, actionable overview — not just counts, but breakdowns that surface where work is concentrated, who's overloaded, and what needs attention. Think of this as the dashboard a project manager checks every morning.

## Arguments

- `/ghpm-status` — full dashboard for the project
- `/ghpm-status <scope>` — scoped to a team or component name (matched against field options in `.ghpm/config.json`)

## Workflow

### Phase 1: Load Config and Cache

Follow the startup sequence in `../ghpm-shared/SKILL.md` and load cache per `../ghpm-shared/references/cache.md`.

### Phase 2: Aggregate

Count items by workflow column (using the `workflow.field` name from config to find the matching field on each item). Include a count for items with no status.

If a scope argument was provided, filter items first:
- Match the argument against all field option names in `.ghpm/config.json` (case-insensitive).
- If no exact match, try semantic/fuzzy matching. The user may use informal or umbrella terms that don't match any single field option but logically group several. Use your understanding of the project's team/component names to infer which options the user likely means, and combine them. Explain the mapping you chose (e.g., "Interpreting '<term>' as <option1> + <option2>").
- If you still can't determine a reasonable match, list available options and ask the user to clarify — but try hard to infer first.
- Filter items to only those matching the scope before aggregating.

Build the following sections from the cached items. Each section adds a different dimension of insight. Include all sections where the data exists — skip a section only if the project doesn't have that field.

#### Component Health

If a "Component" (or similar grouping) field exists, break down items by component × status. This reveals which areas of the project are healthy vs struggling. Show completion percentage per component and flag components with low completion or high active workload.

#### Epic Tracker

If items have a "Level" or type field that distinguishes epics from tasks, show epic-level status separately. Active epics (InProgress) are especially useful — list them with their component and assignees. Flag unassigned active epics as a risk.

#### Team Workload

Count InProgress items per assignee. This surfaces overload — anyone with 8+ concurrent InProgress items deserves a flag. Also count unassigned InProgress items.

#### Attention Items

Identify items needing attention:
- **Untriaged**: items with no status, no component, or no assigned team (check which fields exist in config — not all projects have these fields).
- **No assignee**: items in non-Done columns with empty assignees. Call out ReadyForDev items without owners specifically — they're bottlenecked.
- **Active InProgress**: items in InProgress status — count as a workload indicator. No date info is available, so don't claim staleness.

#### Available Views

List available views with their layout type and filter text. Do NOT attempt to count items per view — filter parsing is handled by `/ghpm-view`. Just show the view name, layout, and raw filter so the user knows what's available.

For key normalization when matching fields, see `../ghpm-shared/references/cache.md`.

### Phase 3: Format Output

Format per conventions in `../ghpm-shared/references/format.md`. Use markdown tables for breakdowns — they're easier to scan than flat text. Include a brief "Key Observations" section at the end that highlights 3-5 actionable insights (bottlenecks, risks, overloaded contributors).

The output should feel comprehensive. A good dashboard is one where the user doesn't need to ask follow-up questions to understand the project's health.

If scoped, prefix with the scope name: `<Project Title> — <scope> — <filtered count> of <total> items`

End with: `Use /ghpm-view <name> to drill into a view.`

## Tips

- Read-only — never modifies the project or its items.

## See Also

- [ghpm-shared](../ghpm-shared/SKILL.md) — Prerequisites and error handling
- [ghpm-view](../ghpm-view/SKILL.md) — Drill into a specific view
- [ghpm-suggest](../ghpm-suggest/SKILL.md) — Get work recommendations
