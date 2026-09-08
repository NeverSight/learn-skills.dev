---
name: plan-to-eat-cli
description: Use when the user wants to interact with Plan to Eat (plantoeat.com) — meal plan, recipes, planner notes/ingredients/leftovers, freezer, shopping list — and the `plan-to-eat` CLI is available but the plan-to-eat MCP server is NOT connected. Same capabilities as the MCP server, driven through the shell. Triggers on "what's on my meal plan", "plan X for Wednesday dinner", "add a note to Tuesday breakfast", "move dinner to Friday", "freeze leftovers", "what's in the freezer", "what's in my shopping list" — when those must be answered with shell commands.
version: 0.5.0 # x-release-please-version
metadata:
  openclaw:
    requires:
      env:
        - PLAN_TO_EAT_USERNAME
        - PLAN_TO_EAT_PASSWORD
      bins:
        - node
      anyBins:
        - plan-to-eat
        - npx
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

# plan-to-eat CLI

The `plan-to-eat` CLI exposes the same 30 capabilities as the `plan-to-eat` MCP
server, as subcommands. Use this skill when you have a shell but no
`plan-to-eat__*` tools.

**If the MCP tools *are* available, use them instead** — see the `plan-to-eat`
skill. They avoid a subprocess per call and return structured JSON directly.

## Setup check

```bash
plan-to-eat --version
```

**Command not found** — the CLI isn't on `PATH`. Work down this list before giving up:

1. **Run it without installing.** The CLI ships in the npm package and needs Node 18+:

   ```bash
   npx -y -p plan-to-eat-mcp plan-to-eat --version
   ```

   Note the `-p`. The package exposes two bins, and the one named `plan-to-eat-mcp` — what plain `npx plan-to-eat-mcp` resolves to — is the **MCP server**, which will sit and wait on stdio. `-p plan-to-eat-mcp plan-to-eat` is what selects the CLI. If this works, prefix every command in this skill the same way.
2. **Install it properly.** Faster than `npx` per call, and puts `plan-to-eat` on `PATH`. **Show the user this rather than running it yourself** — it writes outside the working directory:

   ```bash
   npm i -g plan-to-eat-mcp
   ```
3. **Working from a clone?** `node <repo>/dist/cli/main.js --version`. If `dist/` is missing, the build step was skipped — `npm install && npm run build` in the repo, then retry.
4. **Node missing entirely** (`node --version` fails) — stop and tell the user; don't install a runtime for them.

**"Missing PLAN_TO_EAT_USERNAME and/or PLAN_TO_EAT_PASSWORD"** — credentials aren't set. They come from the environment or a `.env` in the working directory:

| Var | Required | Default |
|---|---|---|
| `PLAN_TO_EAT_USERNAME` | yes | — |
| `PLAN_TO_EAT_PASSWORD` | yes | — |
| `PLAN_TO_EAT_SESSION_FILE` | no | `~/.plan-to-eat-session.json` |

Ask the user to set them. **Never ask them to paste a password into the conversation, and never put credentials in a command you run** — no `PLAN_TO_EAT_PASSWORD=... plan-to-eat ...` one-liners, they land in shell history and in the transcript.

If none of this works, point the user at the project README rather than trying to scrape the web app.

## Using it

**Always pass `--json`.** The default output is a human-readable table meant for
the user's eyes; `--json` gives you the raw payload to reason over. Show the
user the table form only if they asked to see it.

```bash
plan-to-eat <command> [args] --json
```

Names map from the tool names one-to-one: `add_planner_recipe` is
`add-planner-recipe`. Both spellings work.

**Discover, don't guess:**

```bash
plan-to-eat --help                      # every command, grouped
plan-to-eat add-planner-recipe --help   # arguments, which are positional, enum values
```

**Argument forms:**

- Positional or flagged — `get-recipe 123` = `get-recipe --id 123`. `--help`
  says which arguments are positional and in what order.
- Flags accept dashes or underscores: `--start-date` = `--start_date`.
- Booleans are bare flags: `--include_consumed`.
- Arrays repeat, or take JSON: `--event_ids 11 --event_ids 22` = `--event_ids '[11,22]'`.
- Objects take JSON: `--ingredients '{"title":"bread","amount":"2"}'` (repeat per item).

**Quote anything with spaces**, especially note and ingredient text:
`plan-to-eat add-planner-note "Defrost chicken" 2026-05-04 breakfast`.

**Exit codes:** `0` success, `1` for bad arguments, missing credentials, or an
upstream error. Read stderr — argument errors name the offending flag and the
expected type.

## Core concepts

**Recipe** — numeric `id`. `list-recipes --json` returns the catalog (~500
summaries); `get-recipe <id> --json` gives directions, comments, and the full
ingredient list. **Recipe IDs are not guessable** — look them up first.

**Planner event** — one calendar entry: `{ id, date, section, kind, recipe_id?, description?, servings }`.
`kind` is `recipe`, `note`, or `ingredient`. `section` is `breakfast`, `lunch`,
`dinner`, or `snacks`. `date` is `YYYY-MM-DD`.

**Frozen recipe** — `{ id, recipe_id, count, servings, frozen_on }`. `count` is
portions remaining, `servings` is per-portion size. Consuming is a soft-delete:
the API zeroes `count` and keeps the row.

**A "week"** is whatever 7 days the user means. `get-planner-week <start>` runs
to `start + 6 days` unless you pass an end date. If the user says "this week"
without a start day, convert relative to today.

## Common workflows

Resolving a recipe by name is the usual first step. Filter the catalog rather
than eyeballing it:

```bash
plan-to-eat list-recipes --json | jq -r '.[] | select(.title|test("lasagna";"i")) | "\(.id)\t\(.title)"'
```

If `jq` isn't available, pipe to `node -e` or read the JSON yourself.

### "What's on the meal plan this week?"
```bash
plan-to-eat get-planner-week 2026-05-04 --json
```
Recipe events arrive with `recipe_title` already joined — no second lookup
needed. Group by `date`, then `section`, for a readable answer.

### "Plan [recipe] for Wednesday dinner"
```bash
plan-to-eat add-planner-recipe <recipe_id> 2026-05-06 dinner --json
```
The response carries the new event `id`. If the user named a servings count,
follow with `set-planner-servings <event_id> <n>`.

### "Add a prep note / a grocery item to a slot"
```bash
plan-to-eat add-planner-note "Defrost chicken" 2026-05-04 breakfast --json
plan-to-eat add-planner-ingredient "2 lbs ground beef" 2026-05-06 dinner --json
```
Use `add-planner-ingredient` for grocery-style text tied to a meal. For the real
shopping list, use `get-shopping-list`.

### "Move Tuesday dinner to Wednesday"
```bash
plan-to-eat get-planner-week <week start> --json     # find the event id
plan-to-eat move-planner-event <event_id> 2026-05-06 dinner --json
```

### "Change that meal to 4 servings"
```bash
plan-to-eat set-planner-servings <event_id> 4 --json
```
Recipe events only.

### "Edit that note to say X"
```bash
plan-to-eat update-planner-entry-text <id> "X" --json
```
Note the asymmetry: notes are *created* with title text but *edited* through
`description`. The CLI hides most of this, but it's why the read shape shows
note text under `description`.

### "Is [recipe] already planned this week?"
```bash
plan-to-eat find-planned-dates <recipe_id> --start-date 2026-05-04 --end-date 2026-05-10 --json
```
Do this before scheduling if the user is trying to avoid repeats.

### "Plan Tuesday's lasagna as leftovers Thursday"
```bash
plan-to-eat add-leftover-meal <source_event_id> 2026-05-07 dinner --json
```
One call — it duplicates and moves. Omit the date/section to leave the leftover
in the source slot. For a plain copy, `duplicate-planner-event <id>`.

### "Reorder breakfast: pancakes first, then bacon"
```bash
plan-to-eat reorder-planner-events --event_ids <pancakes> --event_ids <bacon> --json
```
All ids must share a date and section.

### "Freeze 3 portions of last night's chili"
```bash
plan-to-eat freeze-recipe-portions <recipe_id> <event_id> 3 1.0 --json
plan-to-eat list-frozen-recipes --json      # confirm, and get the new entry id
```
`event_id` is the planner event the portions came from.

### "What's in the freezer?" / "We ate the freezer chili"
```bash
plan-to-eat list-frozen-recipes --json
plan-to-eat list-frozen-recipes --include_consumed --json   # with history
plan-to-eat delete-frozen-recipe <frozen entry id> --json
```
Freezer entries carry `recipe_id`, not titles — `get-recipe` each one if the
user wants names.

### "Remove that from the plan"
```bash
plan-to-eat delete-planner-event <id> --json
```

## Gotchas

- **`section` comes back as `supper` on some accounts.** Plan to Eat normalizes
  to a per-account preference. Always *send* `dinner`; treat `supper` as the
  same slot when reading.
- **Note and ingredient text lives in `description` on read**, not `title` —
  `title` is null for notes. Table output already accounts for this.
- **Create and duplicate can return `null`.** The upstream API returns empty
  bodies, so the client recovers the new event by diffing the event list before
  and after. A concurrent change can defeat that. Re-run `get-planner-week` to
  find the event rather than assuming the write failed.
- **Convert relative dates yourself.** "Tuesday" must become a real
  `YYYY-MM-DD` before it reaches the CLI. The date check only validates shape,
  so `2026-13-99` passes argument parsing and fails upstream.
- **`add-planner-recipe` won't create a recipe.** For something not in the book,
  `create-recipe` first, or use a note/ingredient entry for freeform text.
- **`find-planned-dates` is keyed on `recipe_id`, not title.** To search by
  name, filter `list-recipes`.
- **Writes are real and immediate.** There's no dry-run and no undo. Confirm
  with the user before deleting anything you didn't just create.

## Full reference

[docs/TOOLS.md](https://github.com/alex-zwingli/plan-to-eat-mcp/blob/main/docs/TOOLS.md) documents every command's arguments, return
shape, and quirks.
