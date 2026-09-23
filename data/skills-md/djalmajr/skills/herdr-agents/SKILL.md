---
name: herdr-agents
description: >
  Run an omp-style team of role agents (scouter, planner, designer, implementer,
  tasker, reviewer, security-reviewer, researcher, inspector) inside Herdr. The calling
  agent stays the orchestrator: it spawns one CLI agent per role in sibling
  panes, dispatches self-contained briefs, collects file-based reports, and
  owns integration, gates, and git. Use when running inside Herdr
  (HERDR_ENV=1) for any non-trivial work: the user asks for a herd, team,
  roles, a designer or reviewer agent, parallel workers, "like omp agents",
  or the task needs a survey (several files, another repo, tool
  conventions), touches more than a couple of files, or the project's
  AGENTS.md routes work through this skill. Do not use outside Herdr; a
  one-or-two-file change with no product decision is done directly.
argument-hint: "<objective> | roles | roster | spawn <role> | run <role> <brief> | release <agent>"
user-invocable: true
metadata:
  short-description: Role agents (design, review, implement…) orchestrated through Herdr
---

# /herdr-agents

Turn the calling agent into an **orchestrator** and give it a team of
**role agents** running as real CLI agents in Herdr panes. The orchestrator
is not configured anywhere: it is whichever agent runs this skill from a
Herdr pane (`HERDR_ENV=1`). Every other role is a file under `roles/` whose
`kind` says which CLI agent plays it. Roles are markdown
files with frontmatter (like omp's `.omp/agents/*.md`); the `herdr` CLI is the
transport. The orchestrator decomposes, briefs, waits, integrates, verifies,
and commits. Workers implement, research, or review one slice each and report
to a file.

## Non-negotiables (each one is a mistake that was actually made)

1. **The report file is the completion signal.** Use `dispatch` (waits),
   `wait`, or `status`. Never hand-roll a loop over `herdr agent get`.
2. **Never `release --close` a worker whose report is missing** while it is
   working. The script refuses; `--force` is for a worker you are abandoning.
3. **Every brief has Goal, Owned files, Forbidden, Report and a no-commit
   line.** `dispatch` lints it (`brief_lint=warn|strict`). Credentials, URLs
   and seeds named in a brief must be verified first (`git grep`, seed
   script), not guessed.
4. **Reviewer from another model family** than the implementers, before push.
5. **State never under `.agents/` or `.codex/`** (Codex sandbox denies them).
6. **Nested orchestrators must not be sandboxed Codex**: its sandbox blocks
   the Herdr socket. Use `claude` (or Codex with its sandbox disabled).
7. **Read `$S friction` at the end of every run** and file what the skill
   caused as an issue (see "Improving this skill").

## Preconditions

```bash
test "${HERDR_ENV:-}" = 1 && command -v herdr jq >/dev/null && $S init
```

If the check fails, say you are not inside Herdr (or `jq` is missing) and
stop. Never control a Herdr session from outside Herdr. The `herdr` skill
(`herdr --skill`) is the authority for CLI syntax; this skill adds the role
layer on top of it and never replaces it.

## Names: who is who in the roster

Run `$S init` first. It runs `doctor` (advisory: inside Herdr, `jq`,
Herdr client vs server version, the **official `herdr` skill present and
identical to `herdr --skill`**, kinds in `PATH`, state dir writable,
config sane), then renames the caller's own agent to `orchestrator`
(config `orchestrator_name`; `orchestrator-2` when taken) so the Herdr
sidebar and `roster` show who leads, and prints the context (pane, tab,
workspace, layout, state dir). Act on `warn` lines before spawning; a
stale official skill means the CLI syntax you read may be wrong. `spawn`
does the rename lazily.

Workers are named after their role: `scouter`, `implementer`, `reviewer`…;
a second worker of the same role becomes `implementer-2`. Pass `--name` for
something more telling (`impl-auth`, `rev-ui`). A nested orchestrator uses
the `sub-orchestrator` role and is therefore named `sub-orchestrator`.

## Roles

| Role | Default kind | Effort | Mode | Use for |
|---|---|---|---|---|
| `scouter` | grok | high | read-only | Map code, find paths, compressed findings for handoff |
| `researcher` | grok | high | read-only | Source-verified answers about external libraries/APIs |
| `planner` | claude | high | read-only | Decision-ready plan for a large or unfamiliar objective: options, one recommendation, slices, risks, questions; the orchestrator still decides |
| `designer` | agy | high | edit | UI work under the project design system (tokens, states, a11y) |
| `implementer` | grok | xhigh | edit | Production code for one slice with per-item report |
| `tasker` | grok | low | edit | Mechanical edits in volume with an exact contract |
| `reviewer` | codex | high | read-only | Patch-anchored correctness findings before push |
| `security-reviewer` | claude | high | read-only | Evidence-backed vulnerability findings |
| `inspector` | agy | high | read-only | Screenshots in both themes, UX findings, no fixes |
| `sub-orchestrator` | claude | medium | read-only | Runs this skill from another pane; never codex sandboxed (socket blocked) |

**Which kind for which work** (policy of 2026-09-21). **Heavy work goes to
`grok`** — production code (`implementer`, `xhigh`), edits in volume
(`tasker`), surveys and research (`scouter`, `researcher`): grok 4.7 has
`xhigh` reasoning and a plan with headroom. Order of preference for that
work: `grok` > `cursor` (running grok 4.7 too) > `codex` > `claude`.
**Judgement and leadership go to `codex` and `claude`** — `reviewer`
(codex), `security-reviewer` (claude), `planner` and `sub-orchestrator`
(claude), and the orchestrator itself. **Visual work goes to `agy`**
(`designer`, `inspector`): it reads screens well. The one rule that does
not move: the reviewer of a slice comes from **another family** than its
implementer, and cursor running grok is the xai family like `grok` — so
reviewers default to codex/claude, never grok/cursor. The role defaults
encode this; keep it when overriding.

Definitions live in [roles/](roles/). Resolution order: project
`.agents/herdr-roles/<role>.md` → this skill's `roles/<role>.md`. `--kind`
at spawn time overrides the frontmatter default. Kinds map to model
families (`references/kinds.md`; for `cursor` the family comes from the
resolved model id — `grok-4.7-xhigh` is xai); a reviewer must come from a
**different family** than the implementer of the same slice. The script refuses to
dispatch a reviewer whose family matches a live edit agent unless
`--allow-same-family` is passed. It cannot see code the orchestrator wrote
itself: in that case pick a reviewer kind from another family by hand.

## Effort, model, approvals

Role frontmatter, config and `spawn` flags share three knobs. Precedence,
highest first: flag → config `role.<role>.<knob>` → config
`effort.<kind>` (effort only) → role frontmatter → config
`model.<kind>.<position>` → config `model.<kind>` → the CLI's own
default. Shipped: `effort.grok=xhigh`, `effort.cursor=xhigh` (grok 4.7
accepts `--reasoning-effort xhigh|high|medium|low`), because those plans
are rarely exhausted; spend budget where there is headroom. A project overrides any of it in `.agents/herdr-agents.conf`
without copying role files.

**Models track the latest release.** A model value is an exact id, a CLI
alias (Claude: `fable`, `opus`, `sonnet` already mean "latest"), or a
regex over the ids the CLI lists (`cursor-agent --list-models`,
`agy models`, `grok models`, the Codex model cache); `a|b` tries
alternatives in order. A regex resolves to the **newest** matching model
at spawn time, so `opus` keeps meaning the newest Opus. Position is
`orchestrator` for the `sub-orchestrator` role and `worker` for everything
else. Shipped defaults:

```ini
model.claude.orchestrator=fable     model.claude.worker=opus
model.codex.orchestrator=astra      model.codex.worker=gpt-5
model.cursor.worker=grok|muse       model.agy.worker=gemini|opus
model.grok.worker=grok
role.planner.model=fable            # planner gets the orchestrator-class model
```

The top-level orchestrator is not spawned by the skill; launch it yourself
with the same intent (`claude --model fable`, `codex -m gpt-6-astra`).
`$S model <kind> <spec> [effort]` shows how a value resolves; `$S models
<kind>` lists the ids newest first. For Codex the effort ceiling comes from
the chosen model's advertised reasoning levels, not from the kind.

- **`effort`** is one normalized ladder, `low < medium < high < xhigh < max`,
  translated to each CLI's own flag and **clamped** to what the kind
  supports (`kinds` prints the ceiling: claude `max`; codex, cursor and
  grok `xhigh`; agy, gemini `high`). Asking for `max` on `agy` yields
  `high` with a warning. **No effort anywhere means the agent's own
  configured default** (for example Codex `model_reasoning_effort` in
  `~/.codex/config.toml`); the skill never guesses one.
- **`model`** is passed through to the kind's model flag. Cursor has no
  effort flag: effort is a suffix of the model id, so `--model gpt-5.3-codex
  --effort high` becomes `gpt-5.3-codex-high` when `cursor-agent
  --list-models` lists it, otherwise the plain model with a warning. Cursor
  model ids are strict: a spec that cannot resolve to an id in
  `cursor-agent --list-models` fails before a pane is created, because the
  CLI rejects unknown and unsupported parameterized ids instead of forwarding
  them. Verify the effective context window in the Cursor TUI; a model's
  native harness may expose a different window than Cursor does.
- **`approvals`** decides how much a worker may do without a human:
  `ask` (default, the CLI's normal prompts), `edits` (auto-accept file
  edits), `full` (no prompts for tools or MCP servers, still inside the
  CLI's own sandbox). Per kind, `full` maps to: claude
  `--permission-mode bypassPermissions` + `enableAllProjectMcpServers`;
  codex `-s workspace-write -a never`; grok `bypassPermissions
  --always-approve`; agy `--dangerously-skip-permissions`; cursor `--trust
  --force --approve-mcps`. Two dialogs are **not** bypassed on purpose:
  hook trust (Codex `--dangerously-bypass-hook-trust`) and the first-visit
  workspace-trust prompt on some CLIs. If you accept that risk, pass the
  CLI's own flag after `--`; otherwise `spawn` exits 7 with the screen and
  you answer once by hand.

Unattended runs (the usual case for a herd) need `--approvals full` or
`approvals: full` in a project role override. Roles ship with `ask` so a
fresh install never bypasses prompts silently.

**Auto-approval as a fallback.** When a worker still blocks (a kind without
a full mapping, a dialog `full` does not cover, or `ask` on purpose),
`auto_approve=on` makes `dispatch`/`wait` send the CLI's default "yes" keys
and keep waiting, up to `max_auto_approvals` per dispatch. Each answer is
counted in the dispatch JSON (`auto_approved`) and logged under
`<state>/wait/<agent>.approvals.log`. It approves whatever the worker asks,
so pair it with sandboxed kinds or narrow `approvals`. With it off, a
blocked worker is reported (`blocked`, exit 7) and a human decides.

## Detecting completion (the only reliable signal is the report file)

Herdr reports lifecycle *state*, not turns; every integration flickers
`idle`/`done` mid-task. The skill therefore treats **the report file** as
the completion signal and gives you three ways to observe it. Never write
your own polling loop over `herdr agent get`.

```bash
$S dispatch impl brief.md            # blocks until impl's report exists (default)
$S dispatch a brief-a.md --no-wait   # fan out…
$S dispatch b brief-b.md --no-wait
$S wait a b                          # …then block until every report exists
$S wait a b --any                    # or until the first one lands
$S status a b                        # non-blocking: done | working | blocked | no-report-yet | gone | unavailable
```

`wait` prints one JSON line per agent (`done`, `blocked`, `settled-no-report`,
`gone`, `unavailable`, `timeout`) and exits 0 only when all reports exist
(7 blocked, 6 settled/`gone`, 4 `unavailable`, 9 timeout). `gone` is only
`agent_not_found`. `unavailable` is a permission or transport failure of
`herdr agent get` (cause on stderr and in JSON `error`): retry or restore
access; do not spawn a replacement, and do not `release` or `release --close`
without `--force` while the query is unavailable. A report counts as done
once its size stops changing between two polls. `notify=on` in the config raises a Herdr toast
per finished worker. `roster` shows a `REPORT` column (`none | pending |
ready`) for a quick glance.

## Configuration

Plain `key=value` files, read in this order, each layer overriding only the
keys it sets:

1. `config.defaults` in the skill (documented defaults)
2. `~/.config/herdr-agents/config` — user-wide
3. `<repo>/.agents/herdr-agents.conf` — per project
4. `HERDR_AGENTS_<KEY>` environment variables
5. command-line flags

`$S config` prints every effective value with its source. Keys:
`orchestrator_name`, `layout` (`split`: panes in the caller's tab until it is
full, then herd tabs; `tab`: herd tabs only), `max_workers` (live workers
at once, orchestrator not counted; default 3 = four panes with the caller;
`spawn` exits 8 at the cap; `0` = no cap), `split_max_panes` (panes per
tab, caller included; default 4), `split_min_pane` (smallest pane a spawn may
leave, fraction of the tab; default 0.18), `regrid` (exact grids after every
spawn/release), `herd_label` + `herd_label_max` (template and length of the
automatic herd-tab labels; default `{roles}` → `impl+rev`, 16 characters;
see "Herd tab labels"), `brief_lint` (`warn|strict|off`), `reuse_workers`
(default `on`, also when no config sets it: `spawn` returns an idle
worker of the same role, kind and cwd whose last report exists instead of
opening a pane, and a reuse never counts against `max_workers`; `--reuse`/`--fresh`
override per call; a reused worker keeps earlier briefs in context, so pass
`--fresh` when a slice must start clean), `multi_role` (default `on`; one
idle agent may take another role — see "Ask how to configure"), `feedback` +
`feedback_repo` (see "Improving this skill"), `approvals`
(default for roles without one), `auto_approve` + `max_auto_approvals`
(answer a worker's approval dialog with the CLI's default "yes" and keep
waiting; off by default, see below), `max_effort`
(global ceiling), `family_check` (`strict|warn|off`), `settled_grace`,
`spawn_timeout`, `dispatch_timeout`, `state_dir`, `report_language`,
`notify`, `args.<kind>` (native flags always appended, the place for
hook-trust or workspace-trust bypasses you accept), `role.<role>.kind`
(swap the kind of a role without copying its file).

## Commands

All mechanics go through `scripts/herdr-agents.sh` (needs `bash`, `jq`):

```bash
S=<path-to-this-skill>/scripts/herdr-agents.sh
$S init                                    # doctor + name yourself `orchestrator`, print context
$S doctor                                  # advisory environment check
$S setup [--target FILE] [--no-hooks]      # AGENTS.md block + Claude hooks (idempotent)
$S setup --detect                          # JSON: installed kinds, models, worker config
$S roles                                   # available roles and their sources
$S role reviewer                           # resolved file + frontmatter
$S spawn implementer [--name impl] [--kind codex] [--direction right|down]
$S dispatch impl <brief.md> [--timeout 900000]   # role prompt + brief → agent, waits
$S collect impl                             # prints the report file (or recent output)
$S run scouter <brief.md>                    # spawn + dispatch + collect in one call
$S wait a b [--any] [--timeout MS]         # block on report files
$S friction                                # errors/warnings of this workspace (review at end)
$S regrid                                  # exact grids: caller's tab (split) + every herd tab
$S tab-label                               # herd tabs: id, label, auto|manual
$S tab-label "onda 2" [--tab ID]           # pin a label (newest herd tab, or --tab); --auto goes back
$S spawn reviewer --tab-label "onda 2"     # place the worker in the herd tab of that name (created if needed)
$S layout-plan                             # where the next spawn lands (anchor, direction, overflow reason)
$S status a b                              # non-blocking completion check
$S config                                  # effective configuration and sources
$S config set <key> <value> [--project|--user]   # write one key (default: the project file)
$S roster                                  # live agents with role/kind/pane/state/report
$S release impl [--close]                  # forget the agent; --close closes a pane we created
$S clean [--older-than 7]                  # drop gone agents, delete old briefs/reports
$S kinds                                   # kind → executable, family, effort ceiling
$S spawn implementer --effort xhigh --approvals full      # normalized effort + no prompts
$S spawn scouter --kind cursor --model gpt-5.3-codex --effort high --approvals full
$S spawn implementer -- -s workspace-write -a never      # native agent args after --
```

**Naming.** A spawned agent is named after its role (`implementer`,
`reviewer`); a second one of the same role becomes `implementer-2`, then
`-3`. Pass `--name` for a custom name (`[a-z][a-z0-9_-]{0,31}`). Use that
name in `dispatch`, `collect`, and `release`; never pane IDs.

**Reviewer family check.** `dispatch` of a `reviewer` or `security-reviewer`
compares its model family with every edit agent this skill spawned.
An edit agent is `implementer`, `designer`, `tasker`, any role whose
frontmatter `mode` is `edit`, or a worker whose `roles` history includes
one of those — a worker that edited and was later reused as `scouter`
still counts. Same family → exit 5 unless `--allow-same-family`. Code
written by the orchestrator itself is invisible to this check; choose the
reviewer kind by hand then.

`spawn` in `layout=split` keeps workers in the caller's tab **without
cramming it**: the candidate (caller + this skill's workers in the tab)
with the largest area is halved on its longer side (`--ratio 0.5`; width
fraction ≥ height fraction → `right`, else `down`), then `regrid` rebuilds
the tab as an **exact grid** over caller + workers — the caller stays
top-left in the least crowded column (3 cells: caller full height, two
workers stacked; 4 cells: 2×2). When the tab holds `split_max_panes` panes
(default 4 = caller + 3), or no pane can be halved without going below
`split_min_pane` (default 0.18 of the tab), the worker **overflows** into
a herd tab — the first with room, else a new one, labelled after the
roles in it (`impl+rev`) or the wave you name (`spawn` prints
`placement: split|herd`; `layout-plan` shows the decision and why).
`release --close` frees the slot, so the next spawn lands in the caller's
tab again. `layout=tab` uses the herd tabs only. Every herd tab is rebuilt
as an exact grid too (columns = ⌈√n⌉, rows balanced), keeping its label.
`regrid` also does the reverse: when the caller's tab has room again
(workers released, cap raised) it pulls overflowed workers back from the
herd tabs, first tab first pane, until caller + workers reach
`split_max_panes`; a herd tab that empties closes itself. Workers pass through
a temporary `herd-park` tab during a caller-tab regrid because Herdr
refuses to move a pane inside its own tab; agents keep running. There is
a cap on workers overall: at most `max_workers` (default **3**, four panes
with the orchestrator) live at once. `spawn` past the cap exits 8 and names
the live workers: `release --close` the ones whose reports you already
collected, or let `reuse_workers` hand back an idle worker
(`multi_role=on` may hand back another role; see "Ask how to configure").
Plan waves of up to three slices instead of fanning out wider. `spawn` retries
for a few seconds while the new shell reaches its prompt, starts the agent
with `--no-focus`. `herdr agent start` still focuses that new pane; spawn puts focus back on the pane that had it only while focus is still there, and leaves a pane you moved to alone. `regrid` does not switch to the caller's tab. Explicit
`--direction`/`--ratio` split the chosen (or, when the tab is full, the
caller's) pane as asked and skip the automatic regrid for that call.
Anything after `--` goes to the agent CLI (`herdr agent start … -- <args>`).
**Herd tab labels.** A herd tab is named after what runs in it, not
`herd-2`. Automatic labels come from `herd_label` (default `{roles}`: the
distinct roles in the tab, arrival order, abbreviated — `impl`, `rev`,
`insp`, `des`, `scout`, `res`, `task`, `sec`, `sub`, `plan`; project roles
keep their file name — so `impl+rev`; a repeat becomes `impl+rev 2`; also
`{n}` workers, `{i}` tab position from 2, `{orch}`), cut to
`herd_label_max` (16) characters, and are recomputed after every
`spawn`/`release`/`regrid`. **When the work has a name, name the tab after
the slice or wave, not the role**: `spawn <role> --tab-label "onda 2"`
puts the worker in the herd tab of that label (created when missing,
regardless of room in the caller's tab; a full one spills into
`onda 2 ·2`), and `$S tab-label "paridade"` pins the label of the newest
herd tab (`--tab ID` for another). Keep labels ≤ 16 characters — the
sidebar cuts the rest. Pinned labels and tabs renamed by hand in Herdr
are `manual` and never overwritten (`tab-label --auto` returns a tab to the
automatic label); `roster` shows the `TAB` of every worker.
`dispatch` writes a composed prompt (role body + brief + report contract) to
the state dir and sends a one-line pointer to it, so long briefs never
depend on terminal paste limits. Exit codes: 2 usage/env, 3 unknown
role/agent, 4 Herdr failure (`unavailable`), 5 same-family reviewer, 6 settled without
report, 7 agent blocked (startup or approval), 8 `max_workers` reached,
9 wait timeout. Every error
and warning is also appended to `<state>/friction.log` (`$S friction`).

## What is implicit (read once)

- **The role is the first message, not a system prompt.** The worker still
  obeys its own harness: the project's `CLAUDE.md`/`AGENTS.md`, its hooks,
  skills, MCP servers, and memory. When the role and the repo instructions
  conflict, the worker's harness decides, not this skill. With
  `worker_context=full` expect workers to spend their first minute reading
  project rules and memory. `worker_context=lean` cuts that: the composed
  prompt forbids reading instruction files unless the brief names them,
  Codex gets `project_doc_max_bytes=0`, Claude gets no skill catalog.
  Lean only works when the brief quotes every rule that applies, which is
  what the brief template asks for anyway.
- **Permissions belong to the worker.** A CLI in its default approval mode
  stops on the first approval and the wait returns `blocked`. Use
  `--approvals full` (or `edits`) for unattended runs; anything the mapping
  does not cover goes after `--`. Never answer a `blocked` dialog without
  the user's consent.
- **Startup dialogs.** Update prompts, logins, and trust dialogs make
  `agent start` return `agent_not_ready`; `spawn` records the agent anyway,
  prints the screen, and exits 7. Ask the user, answer with
  `herdr agent send-keys <name> …`, then `herdr agent wait <name>`.
- **One agent, one growing session.** Several `dispatch` calls to the same
  name land in the same conversation; the worker remembers earlier briefs.
  `collect` prints only the latest report; older ones stay in `reports/`.
  Spawn a fresh agent when context must not leak between slices.
- **`dispatch` only knows agents this skill spawned.** An agent started by
  hand in Herdr is not in the roster; use `herdr agent prompt` directly.
- **State is per repo and per Herdr workspace.** Orchestrators in another
  workspace do not see these agents; two orchestrators in the same
  workspace share the roster. Nothing is deleted automatically; run `clean`.
- **Waits track state, not turns.** Herdr can report `idle`/`done` while a
  worker is mid-task (Codex does this during MCP calls). `dispatch` and
  `wait` therefore wait for the report file until the agent is not
  `working` **and** its screen has not changed for `settled_grace` seconds
  (45), or the timeout is spent. `timeout` means "run `wait` again", not
  "lost".
- **`approvals: ask` does not guarantee a prompt.** It means the CLI's own
  default; a Claude Code with `defaultMode: auto` never blocks. To force
  manual approval pass the native flag after `--`.
- **Timeouts.** `spawn` waits 60 s for readiness (`--timeout`). `dispatch`
  uses the role's `timeout` frontmatter (ms), else 15 min. The report file
  is the source of truth, whatever `wait_status` says.
- **`release` without `--close` leaves the agent running.** `--close` ends
  it by closing the pane. Panes passed with `--pane` are never closed.
  `run` does not release.
- **Worktrees are yours to create.** `git worktree add .worktrees/<slug>`
  (or `herdr worktree create`) and pass the path with `--cwd`. The roster
  stays in the main repo; a worker whose cwd is not the repo root gets its
  brief and report routed through `$TMPDIR/herdr-agents/<ws>/reports/`,
  which every known sandbox can write. You merge its diff back yourself
  (`git -C <worktree> diff | git apply`, or cherry-pick).
- **Detection quality varies by kind.** `claude` and `codex` have Herdr
  integrations; `grok` and `agy` are screen-detected, so `idle`/`done` is
  less reliable for them and `unknown` is common.
- **Language.** Write briefs in the user's language (identifiers in
  English); the worker reports in the language of the brief.
- **No remote machines.** `--machine` targets are not supported; IDs and
  the roster are local to this server.
- **Briefs are copied verbatim** into the composed prompt on disk. Keep
  secrets and customer data out of them.
- **Workers have their own command guards.** A Codex guardian on this kind
  of setup rejects `rm -f`-style commands regardless of approvals. Briefs
  describe outcomes, not destructive shell idioms.
- **Layout.** At most `max_workers` (3) workers live at once, so the
  caller's tab normally holds a 2×2 grid (`split_max_panes` 4). Workers
  that still do not fit (`split_min_pane`, or a raised cap) go to herd tabs
  labelled after their roles (`impl+rev`) or after the wave you name with
  `--tab-label`; set `layout=tab` to keep the caller's tab untouched.

State (briefs, reports, roster) lives **inside the project**, under
`<repo>/.herdr-agents/<workspace-id>/`, and the script adds that path to
`.gitignore`. Sandboxed workers can write there: Codex `workspace-write`
allows the repo root, `/tmp` and `$TMPDIR` but **denies its own config roots
(`.agents/`, `.codex/`)**, which is why the state is not under `.agents/`.
Override the root with `HERDR_AGENTS_DIR` only if every worker can write
there. Reports are files by contract, so collection does not depend on
scraping an alternate-screen TUI.

## Orchestrator flow — `/herdr-agents <objective>`

**Not everything is delegated.** A task that fits in one or two files
with no product decision — a doc or config edit, a one-off fix of a few
dozen lines, answering a question, a verification you can run faster than
you can write the brief — is done by the orchestrator directly. Rule of
thumb: if writing the brief takes longer than making the change, make the
change. Delegate multi-file slices, UI under a design contract, anything
touching auth, secrets or input handling, work that parallelizes, and any
change that needs a reviewer. Research is delegated too: reading more
than a handful of files, another repository, or several tools' conventions
to inform a decision is `scouter` work; the orchestrator asks for a report
with a recommendation and decides on it, instead of doing the survey
itself and burning its own context. Product code you write yourself still gets a
`reviewer` from another model family before push; the family check cannot
see your own edits, so pick that reviewer's kind by hand.

1. **Direction first.** If the objective hides a product decision, ask a
   one-line question before planning. Never write a long plan before
   direction.
2. **Decompose yourself.** Slices with disjoint files, explicit interfaces,
   and an order. Shared resources (i18n catalogs, small stores, constants)
   are either delivered ready in the brief or owned by exactly one agent.
3. **Pick roles.** Large or unfamiliar objective (more than about three
   probable slices, unknown code area, or a planning artifact requested) →
   `planner` first; its report feeds your decomposition and never replaces
   it. Research → `scouter`/`researcher`. UI → `designer`. Code →
   `implementer`. Bulk mechanical → `tasker`. Every slice that changes
   code gets a `reviewer` from another model family; auth/secrets/input
   handling also gets `security-reviewer`; visible UI also gets `inspector`.
4. **Write one brief per slice** from [templates/brief.md](templates/brief.md):
   goal, owned files, forbidden files, local sources by path, project rules
   that apply, checks the worker may run, report format. **No commit, push,
   or PR in worker briefs** — the orchestrator owns git.
5. **Spawn and dispatch.** Default topology: sibling pane in the current tab,
   same cwd, `--no-focus`. Use a worktree only when the user asks or two edit
   agents must touch the same files. Parallel edit agents run only
   file-local checks; the full suite runs once at integration.
6. **Collect and integrate.** Read each report, then `git diff`. Worker
   "green" is not done. Fixed order after N deliveries: repo formatter →
   typecheck → project gates → full suite → smoke on touched surfaces.
7. **Review before push.** Dispatch `reviewer` (and `security-reviewer` when
   relevant) on the integrated diff. Fix P0/P1 yourself or via the
   implementer, then re-review the delta.
8. **Report and release.** Say what was proved, not more ("no regression
   observed in <tests + smokes>"). Release agents you spawned **only after
   their report file exists** (`release --close` kills a worker mid-task);
   close only panes this skill created and only when the user did not ask
   to keep them.

When a wait returns `blocked`, inspect `herdr agent read <name>` and ask the
user before answering an approval or question dialog. A timeout or
`agent_prompt_stalled` does not prove the prompt was lost — read first, do
not resend blindly.

## Making the rule stick

The trigger above is only read when a prompt looks like a delegation
request. "Configure X, see how repos A and B do it" does not look like
one, and the orchestrator will read A and B itself. Run once per project:

```bash
$S setup                      # block in AGENTS.md (or a non-symlink CLAUDE.md) + Claude hooks
$S setup --target CLAUDE.md   # when CLAUDE.md is the canonical file
$S setup --no-hooks           # instruction block only
```

Like ai-memory's routing snippet, `setup` writes the delegation rules
between `<!-- herdr-agents:start -->` / `<!-- herdr-agents:end -->`
markers in the project's canonical instruction file and merges two hooks
into `.claude/settings.json`: `UserPromptSubmit` (a one-line reminder on
every prompt while `HERDR_ENV=1`) and `SessionStart` (doctor warnings).
Re-running replaces the block and the hooks; the file is never touched
when the rewrite fails. Generated project files never embed the installer's
absolute path: the `SessionStart` hook prefers the project's `.agents/skills/`
or `.claude/skills/` copy, then checks the same roots under the user's home.
`setup` warns when none can be resolved; `doctor` and `init` warn when the block
or hooks are missing. Validate setup changes with `bash scripts/test-setup.sh`.
Codex, Grok, Cursor and agy have no prompt hooks; for them the block is
the guard.

## Ask how to configure

`setup` writes the instruction block. It does not guess which CLIs this
machine has. While the project file sets neither `max_workers`,
`multi_role`, nor any `role.<role>.kind`, `setup` warns and the
orchestrator does this before spawning:

1. Run `$S setup --detect`. It prints JSON and writes no files: every known
   kind with `installed`, `family`, `effort_ceiling`, and up to three newest
   model ids when the CLI answers (a missing or silent CLI yields an empty
   list, not a failure); plus the effective value and source of
   `max_workers`, `multi_role`, `reuse_workers`, each `role.<role>.kind`,
   and each `model.<kind>.worker`.
2. Ask the user with this harness's structured-question tool, offering only
   **detected** kinds:
   - how many workers may run at once (`max_workers`; `0` means no cap);
   - which kind and model for each group — implementation (`implementer`,
     `tasker`), review and security (`reviewer`, `security-reviewer`),
     research (`scouter`, `researcher`), UI (`designer`, `inspector`,
     `ui-reviewer`);
   - whether one agent may hold several roles (`multi_role` `on` or `off`).
3. Write each answer with `$S config set <key> <value>` (the project file
   `<repo>/.agents/herdr-agents.conf` by default; `--user` writes
   `~/.config/herdr-agents/config`).
4. Run `$S setup` to install the block and the hooks.

`multi_role=on` (the default, including when the key is unset): `spawn`
without `--fresh` reuses an idle worker of another role when the kind, the
cwd and the resolved model are the same and the worker's `approvals` are
at least the request (`ask` < `edits` < `full`). The same role is tried
first. A worker that has held an edit role — `implementer`, `designer`,
`tasker`, or any role with `mode: edit` — is never reused as `reviewer`,
`security-reviewer`, `ui-reviewer` or `inspector`. Spawn then opens a new
worker, and `max_workers` applies. `multi_role=off` reuses only the same
role.

The roster file gains three columns after the original eight. Old lines
stay valid and are reused only for the same role. The new columns are
`model`, `approvals`, and `roles` (comma-separated history, for example
`scouter,implementer`). Column 4 stays the current role. Reuse across
roles rewrites that line in place and appends the new role. The reused
spawn JSON includes `previous_role`. `dispatch` reads column 4, so the
composed prompt is the new role. `roster` prints the current role and,
when the text fits in the column, the history.

## Project root

Briefs and reports are scratch artifacts under the state dir, never in the
repo. When the work belongs to a planning initiative (`planning/<initiative>/`
or the project's equivalent), copy the final per-slice report next to the
story it implements; a status line in an overview does not replace it.
Worktrees created for a slice live under the repo's `.worktrees/` and are
listed, not deleted, at release.

## Prompting

Use the harness's structured-question tool when:

- The objective could be UI or not UI and the answer changes which roles are
  spawned.
- A reviewer would come from the same family as the implementer and no
  other kind is installed (options: accept, swap kind, skip review).
- Releasing would close panes with unread output or worktrees with
  uncommitted changes.
- `feedback=ask` and you have an improvement issue to file (show the title
  and the scenario summary; options: file it, skip, edit).

Ask free-form for the objective when `$ARGUMENTS` is empty. In no-pause
mode, record these as *Open questions* in the final report and proceed with
the recommended option.

## Improving this skill (file an issue when you hit friction)

The orchestrator is the first to notice when this skill gets in the way: a
kind mapping that is wrong, a wait that lied, a command you needed and did
not have, a role prompt that made a worker misbehave. Turn that into an
issue on the skill's repo so the maintainer can improve it incrementally.

- **When:** any friction caused by the skill itself (not by the project or
  the worker's task). `$S friction` lists every error and warning the
  script produced in this workspace; review it at the end of the run. One
  issue per distinct problem; check
  `gh issue list --repo <feedback_repo> --search "<keywords>" --label herdr-agents`
  first to avoid duplicates.
- **Policy** is the `feedback` config key: `ask` (default) — tell the user
  what you would file and file it only after they agree; `on` — file it
  directly and mention it in your final message; `off` — never file, just
  describe the friction in your final message.
- **How:** fill [templates/issue.md](templates/issue.md) (scenario, what
  happened with exact error text or JSON line, what was expected, the
  output of `$S env` and `$S config`, evidence paths, optional proposed
  change), then:

  ```bash
  gh issue create --repo "$(bash $S config | awk '$1=="feedback_repo"{print $2}')" \
    --title "herdr-agents: <one line>" --label herdr-agents --body-file /tmp/herdr-agents-issue.md
  ```

  Redact secrets and customer data from evidence. Never paste a full report
  from a private repo; quote the lines that show the problem.

## Safety

- Never `herdr server stop`; never close panes, tabs, or workspaces this
  skill did not create.
- Do not put `omp` in the herd by default; it is a separate multi-model
  harness. Start it only if the user asks for that kind.
- Prefer `--current`, explicit pane IDs, and unique agent names. Parse IDs
  from JSON, never from sidebar order.
- Briefs and reports may contain repo content; keep secrets out of them.

## References

- [references/troubleshooting.md](references/troubleshooting.md) — observed failures, causes, fixes, and how to validate a kind; read before changing the script
- [references/orchestration-contract.md](references/orchestration-contract.md) — the delegation contract this skill enforces
- [references/kinds.md](references/kinds.md) — kind → family table and install notes
- [templates/brief.md](templates/brief.md), [templates/report.md](templates/report.md)
