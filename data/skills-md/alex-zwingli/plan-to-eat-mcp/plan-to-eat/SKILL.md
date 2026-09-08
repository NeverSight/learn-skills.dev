---
name: plan-to-eat
description: Use when the user wants to interact with Plan to Eat (plantoeat.com) via the connected plan-to-eat MCP server — viewing or updating their meal plan, managing recipes, scheduling notes/ingredients/leftovers on the planner, tracking the freezer, or checking the shopping list. Triggers on phrases like "what's on my meal plan", "plan X for Wednesday dinner", "add a note to Tuesday breakfast", "move dinner to Friday", "freeze leftovers", "what's in the freezer", "what's in my shopping list".
version: 0.5.0 # x-release-please-version
metadata:
  openclaw:
    requires:
      env:
        - PLAN_TO_EAT_USERNAME
        - PLAN_TO_EAT_PASSWORD
    primaryEnv: PLAN_TO_EAT_PASSWORD
    envVars:
      - name: PLAN_TO_EAT_USERNAME
        required: true
        description: Plan to Eat login email.
      - name: PLAN_TO_EAT_PASSWORD
        required: true
        description: Plan to Eat password.
      - name: PLAN_TO_EAT_SESSION_FILE
        required: false
        description: Where the cookie session is cached. Set to "" to disable caching.
    emoji: "🍽️"
    homepage: https://github.com/alex-zwingli/plan-to-eat-mcp
    license: MIT
---

# plan-to-eat MCP

This skill teaches you to use the `plan-to-eat` MCP server effectively. The server gives you full read/write access to a Plan to Eat account: recipe book, weekly planner, shopping list.

## Setup check

If the user references Plan to Eat but no `plan-to-eat__*` tools are available, the MCP server isn't wired into this session.

- If you have a shell and the `plan-to-eat` CLI is installed, use the **`plan-to-eat-cli`** skill instead — same 30 capabilities, driven through subcommands.
- Otherwise the server isn't installed yet. Offer the setup below. Don't try to scrape the web app instead.

### If it isn't installed

The server is published to npm as [`plan-to-eat-mcp`](https://www.npmjs.com/package/plan-to-eat-mcp) and needs Node 18+. **Show these commands to the user rather than running them yourself** — they change the host's configuration, and the credentials must come from the user's own shell, not from you.

```bash
# Claude Code:
claude mcp add plan-to-eat -- npx -y plan-to-eat-mcp

# Claude Desktop, Cursor, Windsurf, Cline, Zed — the same stdio block:
#   "command": "npx", "args": ["-y", "plan-to-eat-mcp"]
```

No clone or build step. To pin a version, use `plan-to-eat-mcp@0.5.0`; to avoid the per-launch npx resolve, `npm i -g plan-to-eat-mcp` and use the `plan-to-eat-mcp` bin as the command with no args.

Claude Code users who want the skills *and* the server together can instead install the plugin from a clone:

```bash
git clone https://github.com/alex-zwingli/plan-to-eat-mcp.git
cd plan-to-eat-mcp && npm install && npm run build
claude plugin marketplace add "$(pwd)"
claude plugin install plan-to-eat@plan-to-eat
```

**Credentials** come from two environment variables the host passes through:

| Var | Required | Default |
|---|---|---|
| `PLAN_TO_EAT_USERNAME` | yes | — |
| `PLAN_TO_EAT_PASSWORD` | yes | — |
| `PLAN_TO_EAT_SESSION_FILE` | no | `~/.plan-to-eat-session.json` |

Ask the user to export them in their shell profile. **Never ask them to paste a password into the conversation, and never put credentials in a command you run.** After installing, the host has to be restarted before the tools appear.

Prefer these MCP tools when they're available: no subprocess per call, and structured results without a JSON round-trip.
## Core concepts

**Recipe** — identified by numeric `id`. Fetch the catalog with `list_recipes` (returns ~500 entries with summaries); drill into one with `get_recipe` for directions/comments/full ingredient list. **Recipe IDs are not guessable** — always look them up before referencing.

**Planner event** — a single entry on the calendar. Shape:
```
{ id, date, section, kind, recipe_id?, description?, servings, ... }
```
- `kind` is `recipe`, `note`, or `ingredient`
- `section` is `breakfast`, `lunch`, `dinner`, or `snacks`
- `date` is `YYYY-MM-DD`
- note and ingredient text reads back under `description`; `title` is `null` for notes

**Frozen recipe** — a freezer entry tracking N portions of a previously cooked recipe. Shape: `{ id, recipe_id, count, servings, frozen_on }`. `count` is portions remaining; `servings` is per-portion size. The API soft-deletes by zeroing `count` rather than removing the row.

**A "week"** is whatever 7-day window the user means. Use `get_planner_week` with a `start_date`; `end_date` defaults to `start_date + 6 days`. If the user says "this week" without specifying a start day, ask or pick today.

## Common workflows

### "What's on the meal plan this week?"
```
get_planner_week({ start_date: "2026-05-04" })
```
Recipe events come pre-enriched with `recipe_title` — you don't need to join against `list_recipes`. Group the response by `date` then `section` for a readable answer.

### "Plan [recipe] for Wednesday dinner"
1. `list_recipes` → filter client-side to find the recipe id by title (case-insensitive match)
2. `add_planner_recipe({ recipe_id, date, section: "dinner" })`
3. If the user mentioned servings: follow up with `set_planner_servings({ event_id, servings })` using the id returned from step 2

### "Add a prep note: defrost chicken Monday morning"
```
add_planner_note({ date: "2026-05-04", section: "breakfast", title: "Defrost chicken" })
```

### "Add 2 lbs ground beef to Wednesday dinner"
```
add_planner_ingredient({ date: "2026-05-06", section: "dinner", title: "2 lbs ground beef" })
```
Use this for grocery-style additions tied to a meal slot. For the actual shopping list, use `get_shopping_list`.

### "Move Tuesday dinner to Wednesday"
1. `get_planner_week` to find the event id
2. `move_planner_event({ event_id, date: "<Wed>", section: "dinner" })`

### "Change [meal] from 2 servings to 4"
1. `get_planner_week` → find event id (must be a recipe event)
2. `set_planner_servings({ event_id, servings: 4 })`

### "Edit that note to say X"
```
update_planner_entry_text({ id, description: "X" })
```
**Note**: this tool uses `description` on the wire, even though `add_planner_note` uses `title` on create. Rails inconsistency — just remember it.

### "Is [recipe] already on the plan this week?"
1. `list_recipes` → resolve recipe id
2. `find_planned_dates({ recipe_id, start_date, end_date })`

### "Duplicate Tuesday's dinner to Friday"
```
duplicate_planner_event({ id, plan_leftover: false })
// returns a copy on the same date — then move it
move_planner_event({ event_id: <new id>, date: "<Fri>", section: "dinner" })
```
Set `plan_leftover: true` if the user explicitly says "as a leftover".

### "Plan Tuesday's lasagna as leftovers on Thursday"
Use the leftover convenience tool — it does the duplicate + move in one call:
```
add_leftover_meal({ source_event_id: <Tuesday lasagna event id>, date: "<Thu>", section: "dinner" })
```
Omit `date`/`section` to leave the leftover on the same day/slot as the source.

### "Reorder breakfast: pancakes first, then bacon"
```
reorder_planner_events({ event_ids: [<pancakes id>, <bacon id>] })
```
All ids should be in the same date+section.

### "Freeze 3 portions of last night's chili"
1. Find the planner event id for the chili (`get_planner_week`).
2. `freeze_recipe_portions({ recipe_id, event_id, count: 3, servings: 1.0 })` — `event_id` is the planner event the portions came from.
3. Confirm with `list_frozen_recipes` to surface the new entry id.

### "What's in the freezer?"
```
list_frozen_recipes()  // active only (count > 0)
list_frozen_recipes({ include_consumed: true })  // history too
```
Recipe titles aren't pre-joined — call `get_recipe` per `recipe_id` if the user wants names.

### "We ate the freezer chili"
```
delete_frozen_recipe({ id: <frozen entry id> })
```
This is a soft-delete: API sets `count` to 0; the entry stays in history.

### "Remove that from the plan"
```
delete_planner_event({ id })
```

## Gotchas

- **`section` can come back as `supper`** — Plan to Eat normalizes to the user's per-account preference. Always send `dinner` on input; recognize `supper` as the same thing on read.
- **Create/duplicate may return `null`** — under the hood the API returns empty bodies, so the MCP recovers the new event by diffing `list_planner_events` before/after. If a concurrent change happens, the diff can miss. Re-list to find the new event.
- **Don't blindly accept the user's date** — Plan to Eat dates are `YYYY-MM-DD`. If the user says "Tuesday", convert to a real date relative to today.
- **Recipe events need a real `recipe_id`** — `add_planner_recipe` will not create a new recipe. To plan something not in the book, either `create_recipe` first, or use `add_planner_note` / `add_planner_ingredient` for freeform text.
- **Don't use `find_planned_dates` to look up recipes by title** — it's keyed on `recipe_id`. For "what recipes do I have", use `list_recipes`.

## Full tool reference

See [docs/TOOLS.md](https://github.com/alex-zwingli/plan-to-eat-mcp/blob/main/docs/TOOLS.md) — `docs/TOOLS.md` in a clone — for argument schemas, return shapes, and notes on each of the 30 tools.
