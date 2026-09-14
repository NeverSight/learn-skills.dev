---
name: daily
description: >-
  The single entry point into the daily-work arc — a hybrid menu/argument router.
  Trigger whenever the user invokes /dev-workflows:daily, types /daily, asks
  "what should I do now", "where was I", "start my day", "what's next today",
  "wrap up my day", "end my day", or seems unsure which skill fits their current
  daily-work moment. Bare invocation shows a 5-station menu (starting / working /
  filing findings / reporting / wrapping up); with an argument (start | work |
  file | report | wrap, synonyms accepted) it jumps straight to the station and
  hands off to the right skill: ado-backlog:my-work, the situational toolbox
  (grill-then-plan, debug-mantra, study-design-verify, naming-audit,
  fit-gap-analysis, problem-description, ticket-trace, scrutinize, review-pr,
  dual-verifier, drive-to-legacy, crm-archaeology, generating-test-cases), findings-to-ado-backlog or
  ado-create-work-items (github-backlog twins on request), management-talk, or
  invoice-generator.
argument-hint: "[start|work|file|report|wrap] | save [\"note\"]"
effort: max
---

<!-- generated: third-party requirements -->
> **Requires:** `pip install pyyaml` — this skill's scripts import `yaml`.

# daily — the one command to remember

Route the user to the right skill for their moment in the day. You are a router:
ask at most two short questions, then hand off. Do not do the station's work
yourself — the destination skill owns it.

## Parse the argument first

`$ARGUMENTS` (if any) selects a station. Match case-insensitively against the
station words and synonyms:

| Station | Words |
|---|---|
| START | `start`, `morning`, `begin`, `plate` |
| WORK | `work`, `working`, `stuck`, `doing` |
| FILE | `file`, `filing`, `findings`, `tickets` |
| REPORT | `report`, `status`, `update` |
| WRAP | `wrap`, `done`, `end`, `finish`, `invoice` |
| SAVE | `save`, `pause`, `checkpoint` |

- **Match a station word** → jump straight to that station (no menu).
- **Match a SAVE word** → run the **Save state** flow (below). SAVE is NOT a
  numbered station and never shows the menu; it captures the resume-point and
  returns.
- **No argument, or no match** → show the menu. An unrecognized word is NEVER an
  error; show the menu with a one-line note ("didn't recognize '<word>'").

## Welcome back (read state, before the menu)

On **bare `/daily`** and on **`/daily start`**, BEFORE showing the menu or handing
off to START, read the saved work-state. Run from any cwd inside the project:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/daily-state.py" show --json
```

- If the output is the literal text `no state yet` (a string, NOT JSON — it is
  printed under both plain and `--json` modes), **skip silently** and go straight
  to the menu / START. Never announce "no state."
- Otherwise `json.loads` the output and read `updated`, `station`, `status`,
  `focus`, and `next`. Compute the relative age yourself from `updated` (e.g.
  "2h ago") — it is NOT stored in the file. Then print one **welcome-back** line,
  the station in CAPS with its emoji, ticket if present:

  > *Last session (2h ago): 🔧 WORK on #6125 — cause confirmed. Suggested next → grill-then-plan.*

  Station emoji: ☀️ START · 🔧 WORK · 📋 FILE · 📣 REPORT · 🌙 WRAP.

Then continue: on bare `/daily` go to **Auto board** (below) before the menu; on
`/daily start` hand off to START. This is a read only — it never writes or commits.

## Auto board (bare `/daily`, after welcome-back)

On **bare `/daily`** only, after the welcome-back line (or after skipping it when
there is no state), **auto-render the work board as a supplement** before the menu —
so the user sees their resume-point AND their open work in one glance, without
picking a station. Invoke the **`my-work`** skill (`ado-backlog:my-work`; the
`github-backlog` twin `github-my-work` only if the project is GitHub-context or the
user asks).

- If the board cannot load (not logged in / offline / `ado-backlog` not installed),
  print a single line — *"board unavailable: <reason>"* — and continue. **A board
  failure must never block `/daily`**: the local log still shows. This is the
  local-first / board-as-a-component property — the resume-point is always available,
  even offline.

Then show the menu below. (`/daily start` already renders the board as its station,
so it is unchanged; this only adds the board to the bare, no-argument path.)

## The menu (bare /daily)

Present exactly five options and wait:

```
Where are you in your day?

  1. ☀️  Starting my day      — what's on my plate
  2. 🔧  Working / stuck      — route me to the right tool
  3. 📋  Filing findings      — turn findings into tickets
  4. 📣  Reporting status     — reshape work for leadership
  5. 🌙  Wrapping up          — daily summary from my commits

(Next time: /daily start · work · file · report · wrap)
💾 Save state anytime: /daily save "<note>"
```

The `Next time` line teaches the station shortcuts; the 💾 line teaches the save
accelerator — both graduate users from the menu. Save is a footer, not a sixth
option: the circle stays five stations (ADR 0004).

## Stations

### 1. START

First run the **Welcome back** read above (`daily-state.py show --json`) and, if
state exists, print the one-line welcome-back BEFORE the handoff — so the user sees
where they left off, then their board. Skip silently if there's no state.

Then invoke the **`my-work`** skill from the ado-backlog plugin
(`ado-backlog:my-work`). Mention the GitHub equivalent (`github-backlog`'s
`github-my-work`) ONLY if the user asks for GitHub.

### 2. WORK

Ask ONE question — "What's happening?" — with these options, then hand off:

| The user is… | Hand off to |
|---|---|
| designing something new | `grill-then-plan` |
| facing an effort too big for one session (foggy, multi-session) | `chart-map` (`/decision-map:chart`) to chart it; `work-map` (`/decision-map:work`) to continue a map already charted (maps live in `docs/decision-map/`) |
| dealing with something broken | `debug-mantra` — then follow the debug chain below |
| advising how a system should work | `study-design-verify` |
| auditing names / labels / mappings | `naming-audit` (or `fit-gap-analysis` for as-is vs to-be) |
| explaining a complex problem | `problem-description` |
| asking why code/a ticket exists | `ticket-trace` |
| wanting a second opinion | `scrutinize` (plans/local diffs) or `dual-verifier` (completed work) |
| reviewing a GitHub pull request | `review-pr` — context, safe workspace, scrutinize, then send-back / fix-it / chat-only |
| facing an unfamiliar legacy codebase | `drive-to-legacy` |
| facing an unfamiliar Dynamics 365 / Dataverse org | `crm-archaeology` |
| wanting a repeatable test-case suite (feature / change / fixed bug) | `generating-test-cases` |

**Debug chain (ADRs 0003 + 0011):** after `debug-mantra` produces a diagnosis, ask:
*"Does the fix involve a design choice (multiple viable approaches with
trade-offs)?"*
- **No (mechanical fix)** → fix → `post-mortem` → offer `generating-test-cases` (regression case) → `management-talk`.
- **Yes** → `grill-then-plan` to capture the decision FIRST → fix →
  `post-mortem` → offer `generating-test-cases` (regression case) → `management-talk`.

It runs both ways: if a user enters `grill-then-plan` directly to design a fix for
a current malfunction whose cause isn't verified yet, it hands off to `debug-mantra`
first, then grills against the confirmed cause (ADR 0011). The invariant either
way: *never plan a fix on an unverified cause.*

### 3. FILE

Get work into the tracker. Two shapes — pick by what the user has:

| The user has… | Hand off to |
|---|---|
| a batch of findings (audit / spreadsheet / review / pasted list) | `findings-to-ado-backlog` — the extract → triage → classify → create pipeline |
| specific item(s) to create directly (one bug, a few stories, a ready list) | `ado-create-work-items` — files them straight into ADO |

Ask ONE question only if the shape is unclear: *"A batch of findings, or specific
tickets to create directly?"* Default tracker is **ADO**; if the user wants GitHub,
use the github-backlog twins — `findings-to-github-issues` or `github-create-issues`.
Either route keeps the safety gates: a dry-run before any real create, and explicit
approval before writing to the org.

### 4. REPORT

Invoke `management-talk`.

### 5. WRAP

Invoke `invoice-generator`. Run it every day — it builds the summary from git
commits, so a day without invoicing still yields a Tribletext-ready record.

After `invoice-generator` finishes, write the end-of-day snapshot. Ask the user (in
one turn) for `station`, `status`, the active `focus` (topic, ticket if any), and
the `next` step, then call:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/daily-state.py" set \
  --station wrap --status <in-progress|blocked|paused|done> \
  --topic "<what you were on>" --next-action "<next step>" \
  [--ticket <id>] [--next-reason "<why>"] [--blocker "<text>" ...] \
  --note "<end-of-day note>"
```

After the snapshot, offer the optional **learn** beat that closes the arc:

> *Harvest today's lessons into the workflow with /reflect? (y/n)*

If the user accepts, hand off to the `reflect` skill; if they decline, skip
silently. Then run the **Commit offer** below. This is the resume-point the next session
reads on `/daily start`.

## Save state (the `save` action)

Reached by `/daily save`, `/daily pause`, or `/daily checkpoint` (see the argument
table) — and surfaced as the 💾 menu footer. NOT a station: it captures the
resume-point and returns; it never shows the menu or hands off to a station skill.

1. **Find where it writes** — show the user the resolved path so there are no
   surprises:
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/daily-state.py" resolve-path
   ```
   The script resolves `--path` flag → `DAILY_STATE_FILE` env → git root
   (`git rev-parse --show-toplevel`). If the script reports it is **not in a git
   repo**, ASK the user where to write (or to use cwd) and pass it via `--path`;
   never fail.

2. **Write the state** — pass only the fields you know; unset fields are preserved
   (read-modify-write), and `updated` is stamped by the script:
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/daily-state.py" set \
     --station <start|work|file|report|wrap> \
     --status <in-progress|blocked|paused|done> \
     --topic "<active work>" --next-action "<next step>" \
     [--ticket <id>] [--next-reason "<why>"] [--blocker "<text>" ...] \
     --note "<the note the user passed to /daily save>"
   ```
   `--topic` and `--next-action` are the required fields; the rest are optional.
   The note from `/daily save "<note>"` goes in `--note` (appended to the body).

3. **Offer commit** (see below), then return to whatever the user was doing.

## Commit offer (assisted, never automatic)

After ANY write (`save` or `wrap`), the skill writes the file first, then
**explicitly asks** — it never commits on its own:

> *Commit & push so the next session/machine sees it? (y/n)*

- **No / declined** → leave the file on disk uncommitted. Done. (For a same-machine
  resume this is usually fine — the file is already there.)
- **Yes** → stage **only** `daily-state.md` (never other files), commit, and push.
  Git lives in the skill, never in the script. Respect this workspace's git rules:
  if the resolved path is a non-repo root or one of several sub-repos, confirm the
  target repo with the user before committing.

## Graceful degradation

Stations 1 and 3 route to skills in OTHER plugins. If the target plugin is not
installed, say so explicitly and print the install command for the user's harness —
never fail silently:

```
ado-backlog is not installed. Install it with:
- Claude Code:  /plugin install ado-backlog@workflow-daily-work
- Antigravity:  stage the ado-backlog skills into your skills dir
                (see the plugin's .antigravity/INSTALL.md)
```

(Same pattern for `github-backlog`.)

## Rules

- At most two questions before handoff (station + the one station question).
- Never do the destination skill's job inline.
- Unknown argument → menu, never an error. `save`/`pause`/`checkpoint` route to
  the Save flow, not a station.
- The work-state file is read on bare `/daily` and `/daily start`, and written on
  `/daily save` and `/daily wrap`. `daily-state.py` owns ALL YAML; the skill owns
  git. Reads never write; writes always offer commit and never commit unprompted.
- A bundled **PreToolUse hook** (`hooks/commit-log.py`, registered in
  `hooks/hooks.json`) also appends every `git commit` message to `daily-state.md`
  `## Log` (via `daily-state.py log`) — but only **when the plugin is enabled**;
  hooks never travel with a skills-only install. Best-effort, and it never blocks a
  commit. So `## Log` is fed by `--note` on save/wrap, and — where the hook is
  active — by each commit as well.
- If `daily-state.py show` prints `no state yet`, skip the welcome-back silently —
  it is never an error.
- The full map lives in PLAYBOOK.md at the marketplace repo root — for humans;
  this skill is self-contained and never needs to read it.
