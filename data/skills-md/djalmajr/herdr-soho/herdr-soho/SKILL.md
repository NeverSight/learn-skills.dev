---
name: herdr-soho
description: >
  Run a team of agents in Herdr panes, one pane per job (scouter, planner,
  designer, implementer, tasker, reviewer, security-reviewer, researcher,
  inspector). The calling agent stays the orchestrator: it spawns one CLI
  agent per role in sibling panes, dispatches self-contained briefs, collects
  file-based reports, and owns integration, gates, and git. Use when running
  inside Herdr (HERDR_ENV=1) for any non-trivial work: the user asks for a
  herd, team, roles, a designer or reviewer agent, parallel workers, or the
  task needs a survey (several files, another repo, tool
  conventions), touches more than a couple of files, or the project's
  AGENTS.md routes work through this skill (or through its former name,
  herdr-agents). Do not use outside Herdr; a one-or-two-file change with no
  product decision is done directly.
argument-hint: "<objective> | roles | roster | spawn <role> | run <role> <brief> | release <agent>"
user-invocable: true
metadata:
  short-description: Role agents (design, review, implement…) orchestrated through Herdr
---

# /herdr-soho

*soho* stands for **SO**ftware **HO**use (formerly `herdr-agents`).

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
3. **Every brief has Goal, Expected result (or Acceptance criteria),
   Forbidden, Report and a no-commit line — and Owned files when the role
   can edit.** `dispatch` lints it (`brief_lint=warn|strict`; a read-only
   role needs no `Owned files` section) and tells every worker that nobody
   watches its terminal (no interactive questions) and never to invent
   names, endpoints, flags, credentials, URLs or requirements. Credentials,
   URLs and seeds named in a brief must be verified first (`git grep`, the
   seed script), not guessed.
4. **Reviewer from another model family** than the implementers, before push.
   **A review item marked `partial` is not a pass.** The reviewer could not
   verify it (often no network, or a source it could not reach). Give the
   reviewer what it lacked, or verify the item yourself, before commit,
   push or release; `wait` and `dispatch` flag reports with `partial` items.
5. **State never under `.agents/` or `.codex/`** (Codex sandbox denies them).
6. **Nested orchestrators must not be sandboxed Codex**: its sandbox blocks
   the Herdr socket. Use `claude` (or Codex with its sandbox disabled).
7. **Read `$S friction` at the end of every run** and file what the skill
   caused as an issue (see "Improving this skill").

## Preconditions

In a third-party fork, run `$S setup --local` before the first `$S init`
if the state directory is not yet Git-ignored. Otherwise `init` can add that
directory to the fork's tracked `.gitignore` before local setup runs.

```bash
test "${HERDR_ENV:-}" = 1 && command -v herdr >/dev/null && { command -v node >/dev/null && [ "$(node -p 'process.versions.node' | cut -d. -f1)" -ge 20 ] || command -v bun >/dev/null; } && $S init
```

If the check fails, say you are not inside Herdr (or Node.js 20+/Bun is
missing) and stop. If the check fails and you are running under Codex, run
`herdr-soho doctor` before concluding you are outside Herdr. Never control a
Herdr session from outside Herdr. The `herdr` skill
(`herdr --skill`) is the authority for CLI syntax; this skill adds the role
layer on top of it and never replaces it.

## First run

`$S init` and `$S doctor` print `first_run: true` when the project file has
no team choice yet (no `multi_role`, `role.<role>.kind`, or `lane.<name>.kind`)
and the state root has no roster row. `init` also sets `first_run` in its
JSON. A header-only roster file is still a first run. `first_run: false`
means this project already chose a team, or agents are already open.

When `first_run` is true, **before any spawn**, tell the user what is about
to happen and wait for a yes. Use their language. Adapt this model; do not
open a pane in the same turn.

Português:

> Vou abrir até 3 painéis ao lado deste (4 no total, contando este).
> Dois escrevem o código em paralelo (e pesquisam quando preciso) e um revisa.
> (Com 3 painéis no total, um escreve e um revisa; com 2, um escreve e eu reviso.)
> Eles não fazem commit nem push; isso fica comigo.
> Você pode acompanhar qualquer painel ou fechar o que não quiser.
> Cada assistente gasta a cota da própria conta.
> Posso abrir?

English:

> I will open up to 3 panels beside this one (4 in total, counting this one).
> Two write the code in parallel (and research when needed) and one reviews.
> (With 3 panels in total, one writes and one reviews; with 2, one writes and I review.)
> They do not commit or push; I do that.
> You can watch any panel or close one you do not want.
> Each assistant spends its own account's quota.
> May I open them?

A refusal stops the team. On a yes, walk the steps in
[Setup: guided configuration](#setup-guided-configuration) if the project
still has no assistant choice, write that, then spawn. Skip this speech
when `first_run` is false.

## Narrate the work

Each visible action gets one line, in the user's language: no JSON, no exit
codes, and none of the words `lane`, `kind`, or `panes`.

- Abri o painel de implementação para escrever esta fatia.
- O painel de revisão está ocupado; espero ele terminar.
- A revisão da fatia 2 achou 3 problemas.
- Opened the implementation panel to write this slice.
- The review panel is busy; waiting for it to finish.
- Review of slice 2 found 3 problems.

Close with who did what: which panel researched, which wrote, which
reviewed, and what you integrated.

## What is happening

When the user asks what is happening ("o que está acontecendo?", "what's
going on?"), run `$S explain` and answer in their language from that text.
It is plain text, not JSON: how many panels, what each one is doing
(working, idle, waiting for a report, or out of quota), the current job and
assistant, and what the current choice recommends. With nothing running it
says what the team is and how to start.

## Names: who is who in the roster

Run `$S init` first, after any required first `setup --local` in a fork. It
runs `doctor` (advisory: inside Herdr,
Herdr client vs server version, the **official `herdr` skill present and
identical to `herdr --skill`**, kinds in `PATH`, state dir writable,
config sane), then renames the caller's own agent to `orchestrator`
(config `orchestrator_name`; `orchestrator-2` when taken) so the Herdr
sidebar and `roster` show who leads, and prints the context (pane, tab,
workspace, layout, state dir). Act on `warn` lines before spawning; a
stale official skill means the CLI syntax you read may be wrong. `spawn`
does the rename lazily. When `first_run` is true, follow
[First run](#first-run) before any spawn.

With lanes on (the default), a worker is named after its lane (`build`,
then `build-2` for the second worker of a lane that holds two, `review`,
and `docs` for the documenter in flex mode). Agent names are global in
Herdr: a name another workspace already uses gets the next free suffix, and
a `--name` that is taken does the same with a warning. Pass `--name` for
something more telling. `lanes=off` keeps the old names: the role (`scouter`,
`implementer`, …), then `implementer-2`. A nested orchestrator uses the
`sub-orchestrator` role and stays outside the lanes unless a `lane.*.roles`
list includes it.

The orchestrator's pane is titled too: `init` sets
`orchestrator: <project>` when the pane has no title, and
`$S title "<objective>"` sets `orchestrator: <objective>` (the objective
is cut at 60 code points). Set it right after `init` and again whenever
the objective changes, so the sidebar shows what this session leads.

The name says the role; the pane title says the task. Every `dispatch`
titles the worker's pane `<role>: <task>`, the task being the brief's first
line when it is an H1 title (`# Brief — <task>`), else the brief's file
name; the title gains ` ✓` once the report exists, and `release` without
`--close` clears it. So the user always sees what each worker is doing, even
when one worker is reused across tasks.

## Roles

| Role | Default kind | Effort | Mode | Use for |
|---|---|---|---|---|
| `scouter` | grok | high | read-only | Map code, find paths, compressed findings for handoff |
| `researcher` | grok | high | read-only | Source-verified answers about external libraries/APIs |
| `planner` | — | — | — | The orchestrator. `spawn planner` exits 12 and opens no pane |
| `designer` | agy | high | edit | UI work under the project design system (tokens, states, a11y) |
| `implementer` | grok | xhigh | edit | Production code for one slice with per-item report |
| `tasker` | grok | low | edit | Mechanical edits in volume with an exact contract |
| `reviewer` | codex | high | read-only | Patch-anchored correctness findings before push |
| `security-reviewer` | claude | high | read-only | Evidence-backed vulnerability findings |
| `inspector` | agy | high | read-only | Screenshots in both themes, UX findings, no fixes |
| `ui-reviewer` | agy | high | read-only | Light review of UI-only changes against the design contract |
| `documenter` | codex | high | edit (docs only) | Documentation of what already landed, after review; never code |
| `sub-orchestrator` | claude | medium | read-only | Runs this skill from another pane; never codex sandboxed (socket blocked) |

**Which assistant for which work.** The `Default kind` column is what a
fresh install uses when nothing is configured, not a policy. The team is a
per-user or per-project choice written in the configuration (the guided
setup asks, offering only assistants whose probe answers): which assistant
and model build, which review, at what effort. The one rule that does not
move: the reviewer of a slice comes from **another model family** than its
implementer (cursor running a grok model is the xai family, like `grok`).
The family check enforces it for workers; for code the orchestrator wrote,
pass `--for <your family>` to the reviewer's dispatch (`anthropic`,
`openai`, `xai` or `google`; a kind with a fixed family such as `claude`
or `codex` works too). **Before choosing or changing a team,
read [references/agent-profiles.md](references/agent-profiles.md):** what
each assistant did well and badly in each role in real use, and a
recommendation per role. Examples:
- UI with e2e goes to a kind that can open a port, not a sandboxed `codex`;
- untrusted-input slices need a stronger model than a small one, or a
  brief that lists the hostile variants to test;
- a `codex` reviewer at `high` found real P1s in 2 to 3 min, where
  `xhigh` cost 2 to 4 times the slice.

Definitions live in [roles/](roles/). Resolution order: project
`.agents/herdr-roles/<role>.md` → this skill's `roles/<role>.md`. `--kind`
at spawn time overrides the frontmatter default. Kinds map to model
families (`references/kinds.md`; for `cursor` the family comes from the
resolved model id — `grok-4.7-xhigh` is xai); a reviewer must come from a
**different family** than the implementer of the same slice. The script refuses to
dispatch a reviewer whose family matches a live edit agent unless
`--allow-same-family` is passed. Pass `--for <author>` to compare only with
whoever wrote the slice: an agent in the roster, a kind with a fixed family
(`codex`, `claude`, …) or a family. Use it when another family's editor is
alive, such as a cursor designer while a cursor reviewer checks codex code,
and for code the orchestrator wrote itself (`--for anthropic` when it runs
on claude).
The role bodies also carry worker-side rules the orchestrator does not
repeat in every brief: the `implementer` runs a mutation check in a
throwaway copy of the project outside the repository whenever other
workers may share the tree (in place only when alone, and restored only
after the file's sha256 still matches — a changed file is someone else's
edit: not restored, and reported), gives that copy its own build output
(`CARGO_TARGET_DIR=<copy>/target`, for example) and runs `$S
mutation-guard <copy>` before mutating — the guard fails when the copy
sits inside the source (or the source inside it), holds a symlink into
the source, or when `CARGO_TARGET_DIR`, `CARGO_BUILD_TARGET_DIR`, a
`--env NAME` or a `.cargo/config[.toml]` `target-dir` points into the
source (a relative value resolved against the copy) (exit 1; 0 when isolated, 2 for bad usage; nothing is written, and
a path it cannot resolve fails closed) — and never cleans a shared cache
or the source's build output to recover; the `implementer`, `tasker` and
`designer` stop every process they started before writing the report,
by the PIDs they kept, checked by PID only (never a listing of every
command line, which can hold credentials; a sandboxed codex blocks `ps`); and the `designer` reports how the UI was
verified (`ui_verification`). The `reviewer` never edits the repository
and mutates only in a throwaway copy.

## Effort, model, approvals

Role frontmatter, config and `spawn` flags share three knobs. Precedence,
highest first: flag → `lane.<name>.*` (every role in a lane shares one
kind and model, because it is one session) → config `role.<role>.<knob>` →
config `effort.<kind>` (effort only) → role frontmatter → config
`model.<kind>.<position>` → config `model.<kind>` → the CLI's own
default. Kind and model travel together per layer: a lane or role model
from a layer below the layer that set the effective kind is discarded
(the chain continues with the next source), and `--kind` without
`--model` discards every configured lane/role model — a kind picked by
flag is assumed to come with the CLI's default model. The role file's own
`model` belongs to the role file's `kind`: when the effective kind comes
from a config layer or a flag, that model is discarded too. When a lane
sets a model but no kind, each role in it keeps its own kind, and `doctor`
checks the lane model against the kind of every role of the lane. Shipped: `effort.grok=xhigh`, `effort.cursor=xhigh` (grok 4.7
accepts `--reasoning-effort xhigh|high|medium|low`), because those plans
are rarely exhausted; spend budget where there is headroom. A project overrides any of it in `.agents/herdr-soho.conf`
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
model.codex.orchestrator=astra      model.codex.worker=sol|gpt-5
model.cursor.worker=grok|muse       model.agy.worker=gemini|opus
model.grok.worker=grok
```

The planner does not get a worker model: the orchestrator plans in this
session. `spawn planner` exits 12.

**Generic kinds (`pi`, `opencode`).** These multi-model harnesses
ship **no default model** in the skill (no `model.pi.*` or
`model.opencode.*` in the defaults): set a `provider/id` yourself in the
user or project file (`model.<kind>.worker`, `role.<role>.model`, a lane's
model, or `--model`); with none set, the CLI uses its own default. Effort
maps to `--thinking` (ceiling `max`) on pi; the opencode TUI maps no effort
flag (`--variant` is only in `opencode run`) and spawn warns instead of
failing. Approvals: opencode `full` → `--auto` (`edits` is not mapped;
warning), and pi has no approval prompts at all (`edits` is a no-op with a
warning). Family is **by model**: the same-family reviewer check is skipped
unless the model id is recognizable, so pick the reviewer's family by hand.
Config and provider examples:
[references/kinds.md](references/kinds.md#generic-kinds-pi-opencode).

The top-level orchestrator is not spawned by the skill; launch it yourself
with the same intent (`claude --model fable`, `codex -m gpt-6-astra`).
`$S model <kind> <spec> [effort]` shows how a value resolves; `$S models
<kind>` lists the ids newest first. For Codex the effort ceiling comes from
the chosen model's advertised reasoning levels, not from the kind.

- **`effort`** is one normalized ladder, `low < medium < high < xhigh < max`,
  translated to each CLI's own flag and **clamped** to what the kind
  supports (`kinds` prints the ceiling: claude, pi and codex `max`; cursor
  and grok `xhigh`; agy, gemini `high`; the opencode TUI maps no effort).
  For Codex the chosen model's advertised levels apply on top, and a model
  that `~/.codex/models_cache.json` does not list stays at `xhigh`.
  Asking for `max` on `agy` yields `high` with a warning. **No effort anywhere means the agent's own
  configured default** (for example Codex `model_reasoning_effort` in
  `~/.codex/config.toml`); the skill never guesses one.
- **`model`** is passed through to the kind's model flag. Cursor has no
  effort flag: effort is a suffix of the model id, so `--model gpt-5.3-codex
  --effort high` becomes `gpt-5.3-codex-high` when `cursor-agent
  --list-models` lists it, otherwise the plain model with a warning. Cursor
  model ids are strict: a spec that cannot resolve to an id in
  `cursor-agent --list-models` fails before a pane is created, because the
  CLI rejects unknown and unsupported parameterized ids instead of
  forwarding them. The strictness is on the spec resolution: the step that
  appends the effort suffix re-queries the list and, when it does not
  confirm the resolved id, passes the model through unchanged with the
  warning `cursor model '<m>' not in --list-models; passing it through
  unchanged` instead of failing the spawn. Verify the effective context
  window in the Cursor TUI; a model's
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
so pair it with sandboxed kinds or narrow `approvals`. The same dialog
three times in a row is left blocked —
`auto_approve: the same dialog came back 3 times for '<agent>'; leaving it
blocked` (a different dialog resets the count) — and the `blocked` JSON
line carries the dialog in `dialog` (the last 20 non-empty visible lines).
With it off, a
blocked worker is reported (`blocked`, exit 7) and a human decides.
A **question** is never answered for the worker, with or without
`auto_approve`: when the blocked screen is a decision prompt (Codex's answer
form, Claude Code's option picker, OpenCode's question dialog), the wait
reports `question` (exit 7) with the screen text in the JSON `question`.

## Detecting completion (the only reliable signal is the report file)

Herdr reports lifecycle *state*, not turns; every integration flickers
`idle`/`done` mid-task. The skill therefore treats **the report file** as
the completion signal and gives you three ways to observe it. Never write
your own polling loop over `herdr agent get`. The report contract in every
composed prompt (brief and amendment) says the worker alone writes that
report, once the whole brief is done — a subagent or background task never
writes it, because the orchestrator reads the report's existence as
completion; and it says that every command output in the report is pasted
from the run, never retyped or reconstructed. The contract also names the
report path, and the dispatch's path is authoritative: a brief's `# Report`
section can name a different literal path (a hand-written or reused brief),
but the worker writes to the dispatch's path anyway, and the dispatch's
report routing (the JSON, `last-report`, the wait marker) never follows the
brief's.

```bash
$S dispatch impl brief.md            # blocks until impl's report exists (default)
$S dispatch a brief-a.md --no-wait   # fan out…
$S dispatch b brief-b.md --no-wait
$S wait a b                          # …then block until every report exists
$S wait a b --any                    # or until the first one lands
$S status a b                        # non-blocking: done | working | blocked | question | no-report-yet | gone | unavailable | quota | provider-error | capacity | not-received
```

**Amending a brief in flight.** To change a worker's brief — while it is
busy or already reported — write the amendment in a file and run
`$S dispatch <agent> amend.md --amend`; never send `herdr agent prompt`
by hand. The amendment gets a new report that `wait` watches, and the pane
keeps its current task. For a busy worker the message arrives when the CLI
delivers it (most queue it).

**One stable report path per task.** Every attempt still writes its own
versioned report, but a task (a dispatch and its amendments) also has
`task_report`: `<state>/reports/<agent>-<ts>.current.md`, named in the
`dispatch` and `wait` JSON right after `report`, and on a
`<!-- task report: … -->` line from `collect`. It is a regular file (no
symlink) with the content of the task's current report: absent while
that report is pending, written by `wait` when it reports `done` and by
`collect`. An accepted `--amend` makes the amendment's report the current
one (the earlier ones stay, listed in `<state>/task-report-<agent>.json`
under `history`) and removes the copy until the amendment reports. A
dispatch or amendment the transport refused restores `last-report-<agent>`,
the pointer and the copy as they were, so the wait never follows a report
that will not come.

`wait` prints one JSON line per agent (`done`, `blocked`, `question`,
`settled-no-report`, `gone`, `unavailable`, `quota`, `provider-error`,
`capacity`, `not-received`, `timeout`) and exits 0 only when all reports
exist (7 blocked/`question`, 6 settled/`gone`, 4 `unavailable`, 9 timeout,
11 quota, 14 `provider-error`/`capacity`, 15 `not-received`). When
several agents finish in one `wait`, the exit is the most severe of those:
4, then 11, then 14, then 15, then 7, then 6. Argument order does not
change it. A `timeout` line carries `elapsed_ms` (this wait's own),
`state` (the last probe tag, `working` or `pending`), `checkpoint` and
`activity_age_s`. A worker still `working` whose screen really changed
within the stuck window (`stuck_warn_minutes`, 20 min when 0 or not a
number) is a **neutral checkpoint**: `checkpoint: true`, no friction line,
only `herdr-soho: checkpoint: '<agent>' is still working (screen changed
<N>s ago); wait again: herdr-soho wait <agent> --timeout <t>` on stderr.
Reading a screen is not activity: a change counts only when the
normalized screen (counters and progress glyphs do not count) moves away
from the hash an earlier probe recorded, a failed (empty) read counts for
nothing, and the change is dated at that earlier probe
(`wait/<agent>.probe-at`), the oldest moment it could have happened — a
long gap between two waits never reads as fresh. Any other timed-out
agent (`checkpoint: false`) gets a friction line naming the state and
doubling the timeout this wait used: `timeout waiting for '<agent>'; it
may still be working (state: <state>). Run: herdr-soho wait <agent>
--timeout <2×>` (a non-numeric timeout drops the suggestion). The exit is
9 either way. Every composed prompt asks for each item's state as `[done]`,
`[partial]` or `[skipped]`. A `done` line gains `partial: N` (only when
N > 0, after `report`) when N lines of the report outside code blocks
carry `[partial]`, and the wait warns:
`report of '<agent>' marks N item(s) partial: a partial item is not a
pass; read them before commit, push or release` (an unreadable report
counts 0 and the line is unchanged). The warn fires once per agent per
report: a marker holds the report path already warned, a second `wait` on
the same report keeps the `partial` key but warns nothing, and a new
report path warns again. The four review roles
(`reviewer`, `security-reviewer`, `ui-reviewer`, `inspector`) open the
report with the exact first line
`findings: N (P0 a, P1 b, P2 c, P3 d) | verdict: pass|fail`, in English
whatever the report language (`fail` when a P0 or P1 remains or the
change must not go as it is). When a `done` report carries it, the JSON
line gains `verdict`, `findings` and `severity` (right after `report`,
before `partial`); the numbers are kept as parsed — a header whose P0..P3
sum differs from `findings` gets the warning
`report of '<agent>': findings <N> but P0..P3 add up to <sum>`, and a
done report of a review role without the header gets
`report of '<agent>' has no 'findings: N (P0 a, P1 b, P2 c, P3 d) | verdict:
pass|fail' first line`. The review roles also tell the worker: before
calling a test, assertion or command wrong, run it when the brief allows
it and quote the output; when it cannot run it, say so and lower its
confidence — reading the code is not proof that a test fails. The
`dispatch` JSON carries the same `partial: N` right after `report_exists`
(after `amend`, when present), and the review fields (`verdict`,
`findings`, `severity`) right after `report_exists` (after `amend`, when
present). With `--no-wait`, `dispatch` can also return `wait_status: queued`
when a working target shows prompt evidence; this exits 0 and the prompt is
picked up when its current turn ends. The JSON is one line with `wait_status` first, so
`dispatch … | tail -1` returns the whole JSON. When the wait settled on a
report different from the dispatch's own — an amendment sent mid-wait
re-pointed `last-report-<agent>` — the JSON gains `settled_report: <path>`
right after `report`, and `report_exists` qualifies that report; the key
is absent when the wait followed the dispatch's own report. Before the send,
`dispatch` also warns when the new brief owns files another roster agent
is still editing (its report still pending): `brief <path> owns files that
'<agent>' is still editing: <paths>` (up to five paths; for a read-only
role: `reviewing files that '<agent>' is still editing: <paths>`) —
advisory, it never blocks. Paths are compared as files, directories
and globs (`src/**/*.ts` crosses `src/a/b.ts`; `roles/reviewer*.md`
crosses `roles/reviewer.md`). A codex worker's composed prompt (brief and
amendment) carries the sandbox notes when its opening args do not grant
the access (`danger-full-access` or
`--dangerously-bypass-approvals-and-sandbox` drop both): `Your sandbox cannot write under .git: do not run git mv, git
checkout, git add or git commit. Describe renames and restores in the
report; the orchestrator runs them.`, and — unless an arg ends in
`network_access=true`, as `-c sandbox_workspace_write.network_access=true`
does — `Your sandbox has no network, local ports
included: tests that start a local server fail with "Operation not
permitted". Mark them [partial] and say so; the orchestrator runs them.
Still write the integration tests the brief asks for, even if you cannot
run them here; do not replace them with unit tests of helpers, and add a
test seam (an injectable value) when the code depends on something fixed,
such as the build type.` Args carrying `danger-full-access` get neither
note. When another live roster agent with an edit role works in the same
tree (the same roster cwd), the composed prompt — brief or amendment —
adds `Another worker edits this same tree now: run the global checks the
brief asks for, but report failures in files you do not own as outside
your slice (name the files), not as [partial] items of yours.` (a Herdr
failure listing the agents skips the line: it is advisory).
`provider-error` is a worker stopped by its model provider (for example
`Request timed out`, `Connection error`, `Retry failed after N attempts`,
`503: {…}`, `401`, `Incorrect API key`, or a revoked refresh token). The
JSON `cause` is sanitized. A terminal authentication failure observed after
`spawn` starts the CLI exits 14 without registering that worker; an
authentication failure on the first `wait` or `status` observation also
returns 14. `dispatch --no-wait` can return 14 after an accepted prompt when
the new failure is visible and the current report is still missing. A
completed report takes precedence over a later auth or quota screen. An
authentication screen already present before
the prompt, with no evidence the worker took that prompt, is `not-received`.
If the same auth cause was already visible before dispatch, `--no-wait` leaves
it unattributed even if the line reappears: redraw or replay can mimic a new
failure. Use `wait` or `status` to inspect the stopped worker.
`capacity` is a provider that refused because it was full (for example an
error type naming `capacity` or `overload`, or status 529). The exact
patterns live in one place, `scripts/lib/provider.mjs`. On `capacity` the
wait first sends the worker
"continue" up to `provider_retries` times, `provider_retry_delay` seconds
apart (each one logged in friction), and reports `capacity` only when that
did not help. Transient provider errors and capacity need two identical
probes before they count; a terminal authentication failure is reported on
the first observation. A worker whose screen changes only in
its counters for `stuck_warn_minutes` (20) while `working` gets one
friction line ("may be stuck in one tool call"); the wait goes on. A
missing, empty or non-numeric screen-age marker counts from now (rewritten
in place), never from the Unix epoch.

`dispatch` also checks that the prompt arrived. If the target is already
`working`, dispatch skips the settle wait and sends no key after the prompt.
Within `prompt_check_seconds` (15, 0 off), a moved `state_change_seq` while
working or a non-empty report confirms receipt. The generic `Read the file `
marker from an earlier prompt does not count. Only this dispatch's unique
composed prompt path in the recent screen confirms that the
prompt is queued; with `--no-wait`, dispatch returns `queued`, and otherwise
it continues waiting for the report. If a working target shows no evidence,
dispatch returns `not-received` (exit 15) and says no key was sent. For a
target that was not working before sending, dispatch keeps the settle and
arrival checks: it waits up to `prompt_settle_seconds` (20, 0 off) for
`interactive_ready` true in `herdr agent get` (when present) and two
consecutive identical visible screen reads 500 ms apart; passing the
deadline warns and sends anyway. If the prompt text sits in the agent's input
box, it sends one Enter (JSON `enter_sent`); if the screen never moved, or
moved without the composed prompt path visible in recent screen outside the
last 3 non-empty lines, it resends the prompt once (`resent`) followed by a
fresh window with the strict rules; if nothing works, it returns
`not-received` (exit 15) — read the pane before sending anything else. A
`queued` dispatch records the moment, the agent's `state_change_seq`, and the
composed prompt path in `<state>/wait/<agent>.queued`. A later `wait` keeps
running its normal probes while the same working turn continues. Once the
target leaves working, quota, provider, and dialog probes run first. The prompt
is still in the input box only when this dispatch's path is among the last 3
non-empty visible lines. If so, `wait` retries Enter once per
`prompt_check_seconds` window, up to 3 retries. If the path is outside those
lines, `wait` ends `not-received` (exit 15) and keeps that result in
`.not-received` for later `wait` and `status` calls. A new working seq or a
report clears the queued marker. A
`not-received` `dispatch` records the moment and the agent's
`state_change_seq`, and a `wait` afterwards
retries one Enter per `prompt_check_seconds` window while the prompt is
still visible in the agent's input box, up to 3 retries: the agent
starting to work, or its state having changed since the marker (a
different `state_change_seq`), clears the markers and the wait goes on
as usual, and
after the 3 retries — or when the prompt is no longer in the input box
with the agent not working — the wait ends `not-received` (exit 15).
`status` reports `not-received` read-only for a queued marker only while that
dispatch's path is still in the input box; quota, provider, and question
results take precedence. For a `.not-received` marker it remains read-only
(exit 15, no key sent), and a moved seq clears the report there too. `gone` is only
`agent_not_found`. `unavailable` is a permission or transport failure of
`herdr agent get` (cause on stderr and in JSON `error`): retry or restore
access; do not spawn a replacement, and do not `release` or `release --close`
without `--force` while the query is unavailable. A `herdr agent get`
killed by a signal (exit ≥ 128, e.g. 137 under load) without a structured
error is transient: one more try after 1 s, then 2 s, before counting; if
it persists, the cause is
`herdr agent get was killed (exit <rc>, <signal>: memory pressure or an
external kill)`. A report counts as done
once its size stops changing between two polls.

`status` ends every TSV line with `task_s` (seconds from the dispatch —
the mtime of `last-report-<agent>` — to the report, or to now while it is
missing; `-` with no dispatch) and `activity_s` (for a `working` agent,
seconds since the last screen change a wait observed, dated as above; `-`
in any other state or with no observed change), and adds both as the last
keys of its JSON lines (`null` when unknown). It writes no marker and
prints no screen text. `notify=on` in the config raises a Herdr toast
per finished worker. `roster` shows a `REPORT` column (`none | pending |
ready`) for a quick glance.

## Configuration

Plain `key=value` files, read in this order, each layer overriding only the
keys it sets:

1. `config.defaults` in the skill (documented defaults)
2. `~/.config/herdr-soho/config` — user-wide
3. `<repo>/.agents/herdr-soho.conf` — per project
4. `<state>/session.conf` — the **session** layer: per Herdr workspace,
   inside the git-ignored state dir, never versioned
5. `HERDR_SOHO_<KEY>` environment variables
6. command-line flags

**Former herdr-agents names.** This skill was called `herdr-agents`. While a
project or machine still has only the old names, the CLI reads them:
`HERDR_AGENTS_<KEY>` when `HERDR_SOHO_<KEY>` is unset,
`~/.config/herdr-agents/config` and `.agents/herdr-agents.conf` while the new
file is absent (the first write to that file — `config set`,
`setup --panes`, `doctor --fix` — copies the old file to the new
name and leaves it in place), and the `.herdr-agents/` state directory
while `.herdr-soho/` does not exist. `setup` migrates an old
`<!-- herdr-agents:start/end -->` block in place — it renames the markers
and the `herdr-agents` names inside it and keeps the rest of its text, a
project's own lines included — and replaces the old Claude hooks; `doctor`
prints one `legacy …` warning for each old name still in use.

**Session layer.** `session set <key> <value>` writes the workspace's
`<state>/session.conf`: it overrides the project and user files, but flags
and `HERDR_SOHO_*` still win — the place for "only this session" (for
example, run every lane on a personal provider just for this week:
`session set lane.build.kind pi` + `session set lane.build.model
my-provider/my-model`). `session show` prints the entries; `session clear
[key]` drops one key or the whole file. `config` prints session values with
the source `session`. Outside Herdr (no resolvable workspace) the layer
does not exist.

`$S config` prints every effective value with its source: the scalar keys
in order, then the dotted keys (`args.*`, `role.*`, `model.*`, `effort.*`,
`lane.*`, sorted) — the file's own spelling when a layer holds the key,
the rebuilt dotted name for a key that only exists in the environment.
Keys:
`orchestrator_name`, `layout` (`split`: panes in the caller's tab until it is
full, then herd tabs; `tab`: herd tabs only), `max_workers` (live workers
at once, orchestrator not counted; default the sum of the lane capacities,
3 for four panes; `spawn` exits 8 at the cap; `0` = no cap),
`split_max_panes` (panes per tab, caller included; default `panes`), `split_min_pane` (smallest pane a spawn may
leave, fraction of the tab; default 0.18), `regrid` (exact grids after every
spawn/release), `herd_label` + `herd_label_max` (template and length of the
automatic herd-tab labels; default `{roles}` → `impl+rev`, 16 characters;
see "Herd tab labels"), `brief_lint` (`warn|strict|off`; read-only roles
need no `Owned files` section), `brief_lint_aliases` (alternate brief
section headings, `Section=Heading|Heading` items; a heading prefix that
starts a level 1–3 header satisfies the section — see "Briefs are
contracts"), `reuse_workers`
(default `on`, also when no config sets it: `spawn` returns an idle
worker of the same role, kind and cwd whose last report exists instead of
opening a pane, and a reuse never counts against `max_workers`; `--reuse`/`--fresh`
override per call; a reused worker keeps earlier briefs in context: compact
or clear its session before an unrelated slice instead of opening another
pane — see "One agent, one growing session"), `multi_role` (default `on`; one
idle agent may take another role — see "Setup: guided configuration"), `feedback` +
`feedback_repo` (see "Improving this skill"), `approvals`
(default for roles without one), `auto_approve` + `max_auto_approvals`
(answer a worker's approval dialog with the CLI's default "yes" and keep
waiting; off by default, see below), `max_effort`
(global ceiling), `family_check` (`strict|warn|off`), `settled_grace`,
`spawn_timeout`, `dispatch_timeout`, `state_dir`, `report_language`,
`notify`, `args.<kind>` (native flags always appended, the place for
hook-trust or workspace-trust bypasses you accept), `role.<role>.kind`
(swap the kind of a role without copying its file), `role.<role>.args`
(native args for a role, with `lanes=off`; with lanes on every role runs
in a lane, a lane session is shared by every role in it, and only
`lane.<name>.args` applies; both only for the kind configured for that
role or lane), `panes` (`2|3|4`,
default 4), `lanes` (`on|off`), `pane_mode` (`strict|flex`, default
`strict`), `flex_extra` (temporary workers flex may add, default 1),
`flex_roles` (who may use them, default `reviewer,documenter`), and
`lane.<name>.roles|kind|model|effort|approvals|panes|args` (`panes` = the
lane's capacity; `args` = native args for every worker of the lane). The
scoped args are appended after `args.<kind>`, before the native args after
`--`. The `doctor` warns about a scoped key in a config file that the
current lane mode cannot apply. A worker keeps the native args it opened
with (roster column 14), so after a change to these keys an idle worker
started with other args is not reused: `lanes=off` opens a new one, and a
lane answers `kind-mismatch` (exit 13) until you release its worker.

## Commands

All mechanics go through `scripts/herdr-soho` (needs `herdr` and Node.js
20+ or Bun — no `bash`, no `jq`):

```bash
S=<path-to-this-skill>/scripts/herdr-soho      # POSIX; Windows: <path-to-this-skill>\scripts\herdr-soho.cmd
$S init                                    # doctor + name yourself `orchestrator`, title an untitled pane, print context (`first_run`)
$S title "<objective>"                     # this pane's title: `orchestrator: <objective>`
$S title --clear                           # clear this pane's title
$S doctor [--fix --panes 2|3|4] [--user|--session]   # advisory check (`first_run: true|false`); --fix normalizes the project, user or session file
$S explain                                 # plain text: what is running, or how to start
$S setup [--target FILE] [--no-hooks]      # AGENTS.md block + Claude hooks (idempotent)
$S setup --detect                          # JSON: installed kinds, summaries, models (incl. custom providers), recommended reviewer; writes nothing
$S setup --probe [--kind K --model M]      # JSON: ready|no-auth|quota|error per kind/model + own pi/opencode models (≤5 per kind; rest in skipped_custom); no panes
$S setup --plan …                          # diff -u per file (config files: key before → after) of what setup/--set/--user-set/--session-set would write; writes nothing
$S session set <key> <value>               # this-session override in <state>/session.conf (above project, below flags/env); also <key>=<value>
$S session show | session clear [key]
$S roles                                   # roles with the kind, model and effort in effect and where each comes from
$S role reviewer                           # resolved file + frontmatter
$S spawn implementer [--name impl] [--kind codex] [--direction right|down]
$S dispatch impl <brief.md> [--timeout 900000] [--amend]   # role prompt + brief → agent, waits; --amend amends the agent's current brief
$S collect impl [--lines N] [--verify]      # prints the report file (or recent output); an agent still working or blocked with no report gets a short stderr line and exit 4 (no terminal dump) unless --lines is passed; --verify re-checks the report's sha256 lines (exit 16 on changed/missing, 4 when the report cannot be read)
$S run scouter <brief.md>                    # spawn + dispatch + collect in one call
$S wait a b [--any] [--timeout MS]         # block on report files
$S stats [--since <date>] [--by role|kind|model|agent|effort] [--json] # tasks, times and review findings; <date> is YYYY-MM-DD or ISO 8601
$S friction                                # errors/warnings of this workspace (review at end)
$S lint <brief.md> [--role <role>]       # the dispatch's brief warnings, before sending; no dispatch, no state
$S send <ref|name> <message…> [--now] [--timeout MS] | --file <path>
                                             # peer message to another agent (any kind, local or another machine): ref local/w12:p1 or a name on the local server; waits for a busy target to settle by default
$S mutation-guard <copy> [--source <dir>] [--env NAME]…  # refuse a mutation copy that shares source or build output (exit 1)
$S find [words] [--machine <label>]… [--all] [--json]   # live panes with a paste-ready reference (<machine>/<ws>:<pane>), filtered by the words
$S friction add "<text>" [--brief <path>]  # record one friction note (level note, command friction; --brief appends ` (brief: <path>)`)
$S feedback send <report.md> "<summary>"   # feedback=local: save the report in feedback_dir as from-<project>-<date>.md (never overwrites) and send one line to feedback_to
$S regrid                                  # exact grids: caller's tab (split) + every herd tab
$S tab-label                               # herd tabs: id, label, auto|manual
$S tab-label "onda 2" [--tab ID]           # pin a label (newest herd tab, or --tab); --auto goes back
$S spawn reviewer --tab-label "onda 2"     # place the worker in the herd tab of that name (created if needed)
$S layout-plan                             # where the next spawn lands (anchor, direction, overflow reason)
$S status a b                              # non-blocking completion check; no names exits 2 and points to `roster`
$S config                                  # effective configuration and sources (incl. the session layer)
$S config set <key> <value> [--project|--user]   # write one key (default: the project file); also <key>=<value>
$S roster                                  # live agents with role/kind/pane/state/report and the current task (TASK, from the pane title; '-' when none, cut to 40 characters)
$S release impl [--close]                  # forget the agent; --close closes a pane we created
$S clean [--older-than 7]                  # drop gone agents, delete old briefs/reports
$S kinds                                   # kind → executable, family, effort ceiling
$S spawn implementer --effort xhigh --approvals full      # normalized effort + no prompts
$S spawn scouter --kind cursor --model gpt-5.3-codex --effort high --approvals full
$S spawn implementer -- -s workspace-write -a never      # native agent args after --
```

`stats` scans composed prompts and reports in the workspace state and
temporary routing directories. It counts accepted dispatches and legacy
pairs without a sidecar. Kind, model and effort come from the dispatch
snapshot; an absent snapshot or empty field groups as `(unknown)`. With
`--by` omitted, it groups by role and JSON has `roles`, `lost_briefs`
and `review`; with `--by` (including `--by role`), JSON has `by`,
`groups`, `lost_briefs` and `review`. The review table covers reviewer,
security-reviewer, ui-reviewer and inspector. Other date formats exit 2.
Each counted pair is exactly one of a task, amendment or reuse. A
non-amendment that switches from the agent's previous known role counts
under `reuses`, not `tasks`. Each group also has `no_report`, `minutes`,
`partials` and `not_received`. The last field records a dispatch's
arrival-check result even if a later wait recovers. JSON
`lost_briefs` maps each group to the stored composed-prompt paths for
lost pairs, and the text output lists them below the tables.

`find` lists the live panes (one line per pane) of the local Herdr and,
with `--machine <label>` (repeatable) or `--all` (every enabled machine
of `herdr machine list`), of other machines, filtered by the search words
(name, kind, status, workspace/tab labels, ids, cwd or title; every word
must match, case-insensitive). Each line starts with the reference
`<machine>/<ws>:<pane>` — copy it and paste it into the chat to name
that pane in a later command (`--json` prints one full entry per line
instead). A single search word that is a reference matches only that
machine's pane and queries that machine. Exit 0 with at least one entry,
1 with none, 2 on bad usage, 4 when the local machine is unavailable; a
remote machine that fails prints a stderr line and the rest is still
listed.

`scripts/herdr-soho` is a POSIX `sh` launcher: it runs
`scripts/herdr-soho.mjs` with `node` (20+) — or `bun` when Node.js 20+
is not available (missing or older) — with the same arguments. If neither
runtime is usable it prints `herdr-soho: needs Node.js 20+ or Bun` and
exits 2.
`scripts/herdr-soho.cmd` is the same launcher for Windows. The `setup`
SessionStart hook checks these locations in order: project
`.agents/skills`, project `.claude/skills`, `$HOME/.agents/skills`, then
`$HOME/.claude/skills`. It invokes the first launcher with
`sh "<skill-root>/scripts/herdr-soho" doctor`.

**Naming.** With lanes on, the agent is named after the lane (`build`,
`build-2`, `review`, `docs`). A name already live anywhere in Herdr gets the
next free suffix (with a warning when it was a `--name`). `lanes=off` names it after the role
(`implementer`, then `implementer-2`). Pass `--name` for a custom name
(`[a-z][a-z0-9_-]{0,31}`). Use that name in `dispatch`, `collect`, and
`release`; never pane IDs.

**Reviewer family check.** `dispatch` of a `reviewer` or `security-reviewer`
compares its model family with every edit agent this skill spawned.
An edit agent is `implementer`, `designer`, `tasker`, any role whose
frontmatter `mode` is `edit`, or a worker whose `roles` history includes
one of those — a worker that edited and was later reused as `scouter`
still counts. Same family → exit 5 unless `--allow-same-family`.

`--for <author>[,…]` narrows the check to the slice's author, and the rest
of the roster is not scanned. Each author is one of:
- an agent in the roster (its family column);
- a family: `anthropic`, `openai`, `xai` or `google`;
- a kind with a fixed family (`claude`, `codex`, `grok`, `agy`, `gemini`).
  `cursor`, `pi` and `opencode` have a family per model: name the family;
- an agent already released from the roster: its family comes from the
  kind and model recorded in its accepted dispatches in this workspace.
  No accepted dispatch, or dispatches that disagree on one known family,
  fail (exit 2) and ask for the family instead. A live roster entry of
  the same name wins, and the name must match exactly.

An agent whose family is unknown cannot narrow the check. The family is
first derived from its kind and model; when it is still unknown, the
whole roster is checked, as without `--for`, and a warning says so.

This is the way to check code the orchestrator wrote itself (`--for
<your family>`), and to review one slice while an editor of the reviewer's
family works on another one. `--allow-same-family` switches the protection
off; `--for` keeps it for the slice under review.

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
with the orchestrator) live at once, the orchestrator not counted — the
cap counts live agents by name and pane: a roster line counts only when a
live agent with the same name sits in the line's pane (a line without a
known pane falls back to the name, counted once); a stale line — the name
alive in another pane — counts nothing. `spawn` past the cap exits 8 and
names
the live workers: `release --close` the ones whose reports you already
collected, or let `reuse_workers` hand back an idle worker
(`multi_role=on` may hand back another role; see "Setup: guided configuration").
Plan waves of up to three slices instead of fanning out wider. `spawn` retries
for a few seconds while the new shell reaches its prompt, starts the agent
with `--no-focus`. Right after the start, `spawn` watches a 5 s window:
a CLI that updates itself at start and exits (the Codex auto-update is the
only one observed) is relaunched once, in the same pane with the same args
(`'<name>' (<kind>) updated itself at start and exited; started it again`);
an agent that exits right after start without that marker — or on the
relaunch — makes `spawn` exit 4 with the last screen lines (up to 5,
` / `-joined); the pane stays open for inspection and no roster line is
written. A name is only free when no live agent uses it, so a roster line
left with a name (or the pane a spawn reuses) belongs to an agent that
exited: `spawn` removes it (`replaced the stale roster line of '<name>'
(pane <pane>)`), and `roster`/`status` show a line whose name is alive in
another pane as `gone`, not the other agent's state. `herdr agent start` still focuses that new pane; spawn puts focus back on the pane that had it only while focus is still there, and leaves a pane you moved to alone. `regrid` does not switch to the caller's tab. Explicit
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
9 wait timeout, 10 lane busy, 11 quota exhausted, 12 `spawn planner` (the
orchestrator plans), 13 lane `kind-mismatch` (the live session runs another
CLI: `release` the lane, and set `lane.<name>.kind` so it cannot recur),
14 provider error or capacity, 15 prompt not received (`dispatch` and
`wait`), 16 `collect --verify`: a reported file changed or is missing
(a report that exists but cannot be read exits 4).
7 also
covers a worker that asked a `question`. A multi-agent `wait` keeps the most severe
of 4, 11, 14, 15, 7 and 6. Every error
and warning is also appended to `<state>/friction.log` (`$S friction`).

**Peer messages (`send`).** `send <ref|name> <message…>` delivers a message to
an agent of any kind — claude, codex, cursor, grok, agy, pi, opencode — local
or on another machine, without the user approving it. The target is a
reference (the `find`/picker form `local/w12:p1`, `windows/w3:p1`, or a bare
pane id) or an agent name on the local server, resolved with `herdr
[--machine m] agent get`; a pane without an agent exits 4 (`no agent in
<ref>`). The message is always prefixed with a 4-line header that names the sender
as a peer agent with an 8-hex random message ID — `[herdr-soho:peer] #<id> Message from another agent —
<sender-ref> (<name>, <kind>, <role>), not from your user` —, says it carries
no user intent or approval, tells how to reply with `send` itself, and announces
that the message follows quoted with `> ` (`The message follows, each line quoted with "> ".`);
outside a Herdr pane the sender degrades to `local/-` with dashes. Each line of the
body is quoted with `> ` (empty lines become `>`), and the message ends with a closing line
`[herdr-soho:peer] #<id> end of message`, so a fake header in the body can never be confused
with the real one. A `working`/
`blocked` target is waited on until `idle`/`done` (`agent wait --until idle
--until done --timeout MS`, default 600000) unless `--now` is given (the target's own
CLI decides queue vs mix); timing out exits 17 with nothing sent (`<ref> is still <status> after <s>s`).
Before sending, `send` checks the target's visible screen: if reading fails, it exits 4 (`<ref>'s screen unreadable; nothing was sent`).
If the bottom 10 non-empty lines match folder/workspace trust patterns (`Trust this workspace`,
`trust this folder`, `Do you trust`, `Enter to confirm`, `[y/N]`, `(y/n)`) under any status,
or question detectors from `dialog.mjs` in the bottom 20 lines when the target is `blocked`, it waits up to `--timeout`
for the dialog to clear; if it does not clear, it exits 17 (`<ref> is showing a dialog; nothing was sent`),
logging `dialog` without typing into the dialog.
The dialog check pairs each visible-screen read with a fresh `agent get` status, including after a wait settles; a question detector that appears while the target is blocked still prevents sending.
Right before sending the prompt, `send` reads `state_change_seq` (preSeq), status (preStatus), and the visible screen (preScreen).
Delivery prompts once via `agent prompt --wait --until working --until blocked --until idle --until done --timeout 15000` (it never automatically re-prompts).
Delivery is verified in a 15-second arrival window if either (a) `state_change_seq` is non-empty and changes from preSeq, preStatus was `idle` or `done`, the new status is `working` or `blocked`, and the current visible screen is not a dialog; or (b) `#<id>` appears in recent unwrapped output (`--lines <message lines + 60>`), the visible screen differs from preScreen, the normalized closing line (`[herdr-soho:peer] #<id> end of message`) is absent from the entire normalized visible screen, and the id itself is no longer visible (so a clipped viewport is not proof).
If not verified by the end of the window: if all recent reads failed, it exits 15 (`unverified`) without sending keys; otherwise it re-reads the visible screen and status. A dialog exits 17 without a key; an Enter is sent only if the normalized `#<id>` occurs in the last 15 non-empty visible lines, then a second proof window runs.
If still not verified, it logs `lost` and exits 15 (`<ref> did not take the message (no sign of it in its state or transcript)`).
The target project decides acceptance: the `inbound`
key (`auto` | `off`, default `auto`) is consulted for a **local** target in
the target's directory, with the target's session layer (its
`HERDR_WORKSPACE_ID`) and none of the sender's `HERDR_SOHO_*`/
`HERDR_AGENTS_*` variables — the sender's config can never authorize or
refuse on the target's behalf — and `off` refuses with exit 18 before
anything is sent. For a **remote** target the policy is not consulted (the
sending machine cannot read the remote project): the header is the only
protection there. Every attempt appends one line to `<state>/
peer-messages.tsv` (`ts from to result chars id`, never the body; skipped with
`HERDR_SOHO_NOWRITE=1`). Exit codes: 0 sent, 2 usage, 4 Herdr/target
unavailable or unreadable screen, 15 not received / lost / unverified, 17 still busy or showing dialog, 18 refused by `inbound=off`.

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
  Reuse the pane for the next slice instead of closing it (a new pane
  reloads the CLI, its skills and its rules). Before the dispatch, compare
  the worker's last task (`roster` TASK) with the new brief:
  - same slice or same subject (a fix round, the next step of the same
    area): reuse it as it is, and send fix rounds with `--amend`;
  - another subject in the same project: while it is idle, send its CLI's
    compaction command (`/compact` in Claude Code, Codex and pi) with
    `herdr agent prompt <name> "/compact"` (a slash command is not a brief,
    so `dispatch` does not apply). Then read the pane once with
    `herdr agent read <name>` until the CLI confirms it (Codex prints
    `Context compacted`), and dispatch;
  - nothing of the old context helps (an unrelated subject): clear the
    session the same way instead (`/new` in Codex and pi, `/clear` in
    Claude Code), then dispatch;
  - a CLI without such a command: `release <name> --close` and spawn again.
  Close a worker (`release <name> --close`) only when this session will not
  use it again; a plain `release` leaves its pane running outside the
  roster. A name still live in Herdr (including one released without
  `--close`, or a pane passed with `--pane`) makes the spawn choose a
  suffixed name. A worker's report covers only the current brief and its
  explicit amendments.
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
  and a `wait` without `--timeout` both allow the role's effective timeout:
  the role file's `timeout` frontmatter (ms), else `dispatch_timeout`
  (15 min), scaled by the role's effective effort (`xhigh` × 1.5, `max`
  × 2, everything else × 1); a `wait` over several agents allows the
  largest of their roles' timeouts. An explicit `--timeout` always wins.
  The report file is the source of truth, whatever `wait_status` says.
- **A Claude Code orchestrator's Bash caps each call at 10 minutes**,
  shorter than a long review: run `wait` (or a `dispatch` that waits) in
  the background, with the harness's own notification waking you — not
  `timeout` in front of it. `wait --any` wakes you per report: it exits 0
  as soon as one report lands (the JSON line for it is printed), so run it
  again for the remaining agents; the wait's own timeout (the roles'
  effective timeouts, above) still applies.
- **A codex worker's sandbox is narrower than it believes.** A codex
  worker (`-s workspace-write`) cannot write under `.git` (`git mv` and
  `git checkout -- <file>` fail on `.git/index.lock`) and has no network,
  local ports included. Its composed prompt says so (the sandbox notes in
  "Detecting completion"): the worker describes renames and restores in
  the report and the orchestrator runs them, and network tests are marked
  `[partial]` and run by the orchestrator. A role or lane that needs
  network: `args.codex=-c sandbox_workspace_write.network_access=true`
  (every codex worker), or `role.<role>.args`/`lane.<name>.args` with the
  same flag when that role or lane is configured with kind codex. They are flags of one CLI: they reach a worker only when the spawn runs the kind the configuration resolves for that role or lane (a `--kind` flag to another kind drops them, with a warning), because a codex `-c <key>=<value>` is `--continue` to claude, which resumes the orchestrator's conversation in the same cwd, and `--cloud` to cursor. `spawn` also refuses a resume flag for claude or cursor (`-c`, `--continue`, `-r`, `--resume`, `--cloud`) from any source, before a pane opens. The Herdr control socket is blocked
  the same way, so a nested orchestrator must not be a sandboxed codex.
- **`release` without `--close` leaves the agent running.** `--close` ends
  it by closing the pane. Panes passed with `--pane` are never closed.
  `run` does not release.
- **Worktrees are yours to create.** `git worktree add .worktrees/<slug>`
  (or `herdr worktree create`) and pass the path with `--cwd`. The roster
  stays in the main repo; linked worktrees share the main checkout's state.
  Briefs for a worker in a worktree should use absolute paths; `dispatch`
  warns when a cited relative path exists only in the orchestrator's checkout.
  A worker whose cwd is not the repo root gets its
  brief and report routed through `$TMPDIR/herdr-soho/<ws>/reports/`,
  which every known sandbox can write. You merge its diff back yourself
  (`git -C <worktree> diff | git apply`, or cherry-pick). `spawn` (a new
  worker and a reuse) warns per other live edit-role agent in the same
  cwd: `'<a>' and '<b>' both edit <cwd>: builds and test runs see each
  other's changes in progress; give each a git worktree (spawn --cwd
  <worktree>) to isolate them` — the fix is one worktree per worker (or
  per branch). A `done` report the routing kept under
  `$TMPDIR/herdr-soho/<ws>/reports/` is mirrored back into the state dir,
  best effort: the report to `reports/` under the same name and the
  composed prompt next to it to `briefs/` minus the `.brief`; a copy
  failure warns and the `done` stands, and `last-report-<agent>` and the
  `wait` JSON line keep pointing at the original.
- **Detection quality varies by kind.** `claude` and `codex` have Herdr
  integrations; `grok` and `agy` are screen-detected, so `idle`/`done` is
  less reliable for them and `unknown` is common.
- **Language.** Everything you tell the user is in the user's language:
  the first-run speech, the setup questions, narration, and the final
  summary. Briefs are in the user's language too. Identifiers stay in
  English (role names, pane names, file paths). Workers report in the
  language of the brief. `$S explain` prints English plain text; translate
  it when you answer.
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
`<repo>/.herdr-soho/<workspace-id>/`, and the script adds that path to
`.gitignore`. Sandboxed workers can write there: Codex `workspace-write`
allows the repo root, `/tmp` and `$TMPDIR` but **denies its own config roots
(`.agents/`, `.codex/`)**, which is why the state is not under `.agents/`.
Override the root with `HERDR_SOHO_DIR` only if every worker can write
there. Reports are files by contract, so collection does not depend on
scraping an alternate-screen TUI.

## Fluxo paralelo

Keep at most `panes` panes, counting this session (plus the temporary one
of flex mode, below). The orchestrator is the planner and does not spawn
one. The other panes are lanes: sessions that take, in order, any role in
their group. A lane may hold more than one worker (its capacity).
`reuse_workers` stays on. Before each `spawn`, the roster is consulted:

- an idle or done worker of the lane whose report exists (or that never
  received a brief) → reuse it and switch the role (column 4 plus the roles
  history). If `lane.<name>.kind` is empty and this role's kind, model, or
  effort differs from the live session, `spawn` prints
  `{"status":"kind-mismatch","lane":…,"name":…,"session_kind":…,"requested_kind":…}`
  (plus model and effort) and exits 13. When `lane.<name>.kind` is set,
  that kind is the CLI for every role in the lane: a live session on that
  kind is reused, and a session still running another CLI (opened before
  the key existed) also exits 13, because the key does not retarget a
  running process. Either way: `release <name> --close`, set
  `lane.<name>.kind` if it is missing, then spawn again;
- no idle worker and fewer live workers than the lane's capacity → open a
  new one (`build`, then `build-2`);
- the lane is full (every worker `working`, `blocked` or with a report
  pending) → `spawn` prints `{"status":"busy","lane":…,"name":…}` and exits
  10, naming all of them. Run `wait <name>`, then dispatch. Do not open
  another pane — except the temporary one of flex mode;
- a `gone` worker → its roster row is dropped and it does not count;
- a worker of the lane cannot be queried (`unavailable`) and none is idle →
  exit 4 before any new pane: the worker may still be live; restore access
  and retry, never spawn a replacement for it;
- every live worker of a full lane has edited and the role is a review role
  (`locked`) → exit 5: a session never reviews code it wrote; use a review
  lane, or release one of them.

Presets (no `lane.*.roles` set; resolved at run time from `panes` and
`pane_mode`, never written into the config):

| panes | lanes (capacity) | the orchestrator |
|---|---|---|
| 4 (default) | `build` (2): implementer, designer, tasker, scouter, researcher · `review` (1): reviewer, security-reviewer, ui-reviewer, inspector | orchestrates, plans, explores |
| 3 | `build` (1) · `review` (1) | idem |
| 2 | `build` (1) | also reviews, from another model family than the build lane (pick it by hand) |

Research is build work: a free builder maps the code or reads another
repository, or the orchestrator does it. `max_workers` defaults to the sum
of the capacities (3, 2, 1) and `split_max_panes` to `panes`, unless the
user, the project or the environment sets them. `lane.<name>.panes` changes
one lane's capacity.

**Strict or flex** (`pane_mode`, default `strict`). Strict opens no
temporary worker: each lane stays within its capacity (a
`lane.<name>.panes` you set raises it; `max_workers` is only the global
cap and opens no slot in a lane), and documentation is build work (the
`documenter` role sits in the build lane). Flex may open up to `flex_extra` (1) **temporary** workers
above `panes`, only for the roles in `flex_roles` (`reviewer,documenter`):
a second reviewer (one per builder, or `reviewer` and `security-reviewer`
on the same slice in parallel — both from another family than the
builders) or the documenter (lane `docs`). With one free slot, the review
comes first: it unblocks the push; documentation waits. With 2 panels,
flex's extra reviewer takes the review off the orchestrator. A temporary
worker is marked `burst` in the roster; `release` closes its pane even
without `--close`. In flex, `max_workers` and `split_max_panes` grow by
`flex_extra`, so the extra pane stays in this tab.

The **documenter** edits documentation only (README, guides, references,
ADRs, CHANGELOG), never code, and works after a slice passed review, from
the spec and the committed diff. Documentation that describes behavior
(commands, flags, config) goes to a reviewer; the rest the orchestrator
checks. A session that has only been the documenter does not count as an
edit agent for the reviewer family check; one that edited code before (an
earlier role in its history) still does.

`sub-orchestrator` is outside the lanes unless the user adds it to one: a
nested herd would open more panes and blow the cap. `lanes=off` keeps
per-role names and `multi_role` reuse.

Decompose into small slices with disjoint files. Dispatch with `--no-wait`
and collect with `wait --any`. While the builders work, plan the next slice
and integrate the report that just landed; the reviewer's queue is the
slice that blocks the push first. Do not leave a builder idle while there
is work. A full lane means `wait`, then dispatch — not a new pane.

`spawn <role>` resolves the lane. A role with no lane is an error, except
under `lanes=off` (and, with `panes=2`, a review role says the orchestrator
reviews). Two orchestrators spawning into the same lane at the same moment
may pass its capacity by one: nothing reserves a slot before the agent
starts.

## Orchestrator flow — `/herdr-soho <objective>`

On `first_run: true`, do [First run](#first-run) and get a yes before any
pane opens. While work is in flight, one line per visible action
([Narrate the work](#narrate-the-work)). When the user asks what is
happening, run `$S explain` ([What is happening](#what-is-happening)).

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
`reviewer` from another model family before push. The family check cannot
see your own edits by itself: dispatch that reviewer with `--for <your
family>`.

1. **Direction first.** If the objective hides a product decision, ask a
   one-line question before planning. Never write a long plan before
   direction.
2. **Decompose yourself.** Slices with disjoint files, explicit interfaces,
   and an order. Shared resources (i18n catalogs, small stores, constants)
   are either delivered ready in the brief or owned by exactly one agent.
3. **Pick roles.** The orchestrator plans. Do not `spawn planner`. Research
   → `scouter`/`researcher` (a builder). UI → `designer`. Code →
   `implementer`. Bulk mechanical → `tasker`. Every slice that changes
   code gets a `reviewer` from another model family; auth/secrets/input
   handling also gets `security-reviewer`; visible UI also gets `inspector`.
   When a slice falls on a known weak spot of the configured kind, use
   another assistant for it. The weak spots are in
   [references/agent-profiles.md](references/agent-profiles.md), for
   example UI or e2e on a sandboxed `codex`, or untrusted input on a small
   model.
   - **With `lanes=off`:** `spawn <role> --name <new> --kind <kind>`.
   - **With lanes on:** a lane is one CLI, and `spawn --kind` against a
     live session of another CLI exits 13. First `release --close` every
     live worker of the lane (`build` and `build-2` when it holds two),
     then `session set lane.<name>.kind <kind>` (and its model), then
     spawn.

   Behaviour that only the target machine shows (paths, shells, OS
   services) is not fixed by another kind on this machine. The worker
   reports it could not run it, and the run happens on the target.

   Keep the pipeline in [Fluxo paralelo](#fluxo-paralelo) full.
4. **Write one brief per slice** from [templates/brief.md](templates/brief.md):
   goal, owned files, forbidden files, local sources by path, project rules
   that apply, checks the worker may run, report format. **No commit, push,
   or PR in worker briefs** — the orchestrator owns git.
5. **Spawn and dispatch.** Default topology: sibling pane in the current tab,
   same cwd, `--no-focus`. Use a worktree when the user asks or two edit
   agents share the same cwd — `spawn` warns about exactly that (give each
   `spawn --cwd <worktree>`). Parallel edit agents run only
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

When a wait returns `blocked` or `question`, inspect `herdr agent read
<name>` (the JSON `question` already holds the question's screen) and ask
the user before answering an approval or question dialog. A timeout or
`agent_prompt_stalled` does not prove the prompt was lost — read first, do
not resend blindly.

## Briefs are contracts

What makes a simpler, cheaper worker reliable is the orchestrator's brief,
in any layout and for any delegated role: a clear goal, the **expected
result**, **acceptance criteria** each with the command that proves it, and
the **decisions already made** so the worker never has to invent a name, a
format, a rule or a requirement. A brief where the worker would have to
guess is the orchestrator's planning failure. Use `templates/brief.md` and
run the checklist in
[references/orchestration-contract.md](references/orchestration-contract.md#brief-checklist-lessons-from-real-failures)
before every dispatch — each of its items is a real gap that cost a review
round: ambiguous predicates, option labels without semantics, missing
invariants (file mode, atomic writes, interrupts, sandboxes, Windows),
missing input validation, briefs with too many items, no rule for which
tests to run while iterating, oversized writes, first-run dialogs in new
folders. When a worker reports a gap, answer it as a decision in the next
brief.

**The lint explains why each missing section costs the worker.**
`dispatch` lints the brief structure (`brief_lint`, default `warn`; a
read-only role needs no `Owned files` section). The warning names the
reason of every missing section, in the section order: `brief <path> is
missing sections: [Goal] [Expected result] — <reason>; <reason>` (strict
appends `(brief_lint=strict)` and exits 2). The reasons: `Goal` — the
worker does not know what the slice is for; `Expected result` — nothing
says when the slice is done; `Owned files` — workers without owned files
collide; `Forbidden` — nothing keeps the worker out of other files;
`Report` — without a report section the worker may never write one; the
no-commit line — the worker may commit or push. A separate check flags the
empty-inline-code symptom in `warn` and `strict` alike — at most three
per-line warnings, then one for the rest; only `brief_lint=off` silences
it:

```text
brief <path> line <n> has empty inline code (``): a shell heredoc without
quotes may have run the backticks
```

`brief_lint_aliases`
(comma-separated `Section=Heading|Heading` items) lets a level 1–3 header
that starts with one of a section's headings, case-insensitive, satisfy
the section: the aliasable sections are `Goal`, `Expected result`,
`Owned files`, `Forbidden` and `Report` (the no-commit line has no heading
to alias); a malformed item is ignored with
`brief_lint_aliases: ignored '<item>' (use Section=Heading|Heading)` and
the valid items still apply. Built-in prefixes also accept Portuguese headings:
Goal (`Objetivo`, `Meta`), Expected result (`Resultado esperado`, `Critérios
de aceitação`, `Critérios de aceite`, `Pronto quando`), Owned files
(`Arquivos`, `Escopo`), Forbidden (`Proibido`, `Fora do escopo`,
`Restrições`) and Report (`Relatório`), with case- and accent-insensitive
matching. Portuguese built-in headings count only when, after the prefix and
leading spaces, the title ends or continues with a non-letter, non-digit;
English headings and configured aliases keep simple prefix matching. In
`Owned files`, a line
whose text starts after any list marker and leading spaces or `*`/`_`
emphasis with `nenhum`, `nenhuma`, `não`, `nunca`, `exceto`, `not`, `never`,
`none`, `except`, `excluding` or `outside` contributes
no paths; a negation later in the line does not exclude its paths.

**Lint before you send.** `$S lint <brief.md> [--role <role>]` prints the
same warnings the dispatch would print for that brief (the role defaults to
`implementer`; a read-only role needs no `Owned files`), and creates no
dispatch, no state and no friction line. It exits 0 when the brief is clean
(`brief <path>: ok`), 1 with warnings, 2 when `brief_lint=strict` finds
missing sections (the same message the dispatch dies with), and 3 for an
unknown role; `brief_lint=off` prints `lint off` and exits 0.

**Failure matrix, only for state that is published, retained or deleted.**
A slice that publishes, retains, prunes or deletes state (backups, releases,
caches, retention) gets the optional `Failure matrix` section of
[templates/brief.md](templates/brief.md), with the three fixed markers
`[crash]` (a crash between publish and prune/delete), `[retry]` (a step
repeated or retried) and `[clock]` (a clock that goes backwards). The
implementer writes one executable fixture per marker and the reviewer
probes each one; both keep local fixture proof apart from operational
proof. When the section is there, the lint (dispatch and `lint`) names the
missing markers: `brief <path> failure matrix is missing: [clock] — a clock
that goes backwards is not covered` (a warning in `warn` and `strict`).
Any other slice leaves the section out and gets no matrix.

**Stop after the gates.** The edit roles stop proving once every check the
brief lists passes: a failure outside their files or caused by an external
limit is a `[partial]` item with its evidence, and a test that would widen
the scope goes to the report's open questions.

## Making the rule stick

The trigger above is only read when a prompt looks like a delegation
request. "Configure X, see how repos A and B do it" does not look like
one, and the orchestrator will read A and B itself. Run once per project:

```bash
$S setup                      # block in AGENTS.md (or a non-symlink CLAUDE.md) + Claude hooks
$S setup --target CLAUDE.md   # when CLAUDE.md is the canonical file
$S setup --plan --local       # preview the local block, hooks and git exclusion
$S setup --local              # for a third-party fork: local block + Claude hooks
$S setup --local --no-hooks   # keep the fork's Claude settings file untouched
$S setup --no-hooks           # instruction block only
```

Like ai-memory's routing snippet, `setup` writes the delegation rules
between `<!-- herdr-soho:start -->` / `<!-- herdr-soho:end -->`
markers in the project's canonical instruction file and merges two hooks
into `.claude/settings.json`: `UserPromptSubmit` (a one-line reminder on
every prompt while `HERDR_ENV=1`) and `SessionStart` (doctor warnings).
The block holds the workflow and the brief contract only; how many panes,
which assistants and which models stay in the configuration, so the block
never contradicts a project's team. A symlinked instruction or settings file
(`AGENTS.md -> CLAUDE.md`) is written through: the link stays a link. The
hook commands are `sh` invocations, so they run only where a POSIX
shell exists (on Windows, via Git Bash or WSL). Re-running replaces the
block and the hooks; the file is never touched
when the rewrite fails. Generated project files never embed the installer's
absolute path: the `SessionStart` hook prefers the project's `.agents/skills/`
or `.claude/skills/` copy, then checks the same roots under the user's home.
`setup` warns when none can be resolved; `doctor` and `init` warn when the block
or hooks are missing. Validate setup changes with
`scripts/run-tests.sh --env outside test-setup.sh`.
Codex, Grok, Cursor and agy have no prompt hooks; for them the block is
the guard.

For a fork whose tracked instructions belong to an upstream, `setup --local`
puts the block in root `CLAUDE.local.md` and keeps that file and the state
directory out of Git through the repository's local `info/exclude`. It leaves
`AGENTS.md`, `CLAUDE.md` and the tracked `.gitignore` alone, while writing the
Claude hooks unless `--no-hooks` is given. `doctor` accepts the local block.
The hooks go to `.claude/settings.json`; local setup neither excludes that
file nor checks whether the fork tracks it. Use `--no-hooks` when that file
must remain untouched. Repeat `--local` on later setup calls, or, after the
first local setup, run `session set setup_target local` for this Herdr
workspace. A project config can hold that key only if the fork already
ignores the config file. `CLAUDE.local.md` is read by Claude Code; other
harnesses need their own local instruction route.
Run this before the first `init` when the state directory is not already
ignored; `init` can otherwise add it to the tracked `.gitignore`.

## Setup: guided configuration

`setup` writes the instruction block. It does not guess which CLIs this
machine has. On a first run — and whenever `doctor` reports a missing or
legacy config (`panes` missing, an empty `lane.<name>.kind` whose roles
resolve to different kinds, `split_max_panes` above `panes`, a per-role kind
on a lane that has its own kind, `role.planner.*`, a role or lane model
discarded because the effective kind comes from a higher layer without a
model, a kind+model pair that does not resolve against the kind's model
list), or a quota stop (exit 11) — the orchestrator walks the user through
the choices. **Every step uses
the harness's structured-question tool** (Claude Code: `AskUserQuestion`,
Codex: `ask_user_question`, OpenCode: `question`) with **three options — the
first marked as the recommendation, with a one-line reason — plus a
free-text field** where the user says exactly what they want (the tool's
free-text/"other" field; when the tool has none, a fourth "say it yourself"
option). Never an open question without suggestions, never ask the user to
write flags, keys, or model ids. `setup` also warns while the project file
sets neither `multi_role`, any `lane.<name>.kind`, nor any
`role.<role>.kind`; `max_workers` alone, including the value
`doctor --fix` writes, is not that choice.

Steps, in order, in the user's language (never the words `lane`, `kind`, or
`panes`):

1. **Consent (first run).** Before any pane opens, say what the team is
   (the first-run speech) and ask whether to open it. Options: *Yes, open
   it* (recommended — the work parallelizes this way), *More info before
   anything opens*, *No, do it without the team* + free text. A refusal
   stops the team.
2. **How many agents at once.** Options: *4 panels* (recommended — two
   write code in parallel and one reviews), *3 panels* (lighter on quota:
   one writes, one reviews), *2 panels* (the lightest: one writes and the
   review happens here) + free text. Map the answer: 4 → `setup --panes
   4`; 3 → `setup --panes 3`; 2 → `setup --panes 2`. Then **an extra panel
   when needed?** Options: *No, never more than that* (recommended — the
   default, `pane_mode=strict`), *Yes, one temporary panel for a second
   review or the documentation* (`pane_mode=flex`), *Decide later* + free
   text.
3. **Which assistant does each job.** Run `$S setup --detect` (writes
   nothing), then `$S setup --probe` — a minimal non-interactive prompt per
   kind/model with a short timeout, no panes; statuses `ready | no-auth |
   quota | error`, and `recommended_reviewer` (a ready kind from another
   family than the build one). **Only assistants whose probe is `ready`
   become options**, including models of personal providers (the
   `custom_models` entries of `--detect`, as `provider/model`, with the
   declared max reasoning level when there is one). The aggregate probe
   already tested each listed own model (up to 5 per kind, the rows with
   `source: "custom"`): offer one only if its own row is `ready`. A model
   that landed in `skipped_custom` was not tested: run
   `$S setup --probe --kind K --model provider/model` first, and offer it
   only if that row is `ready`. Three questions:
   - **Writing code** (the build lane): recommended is the assistant the
     user file already names for building when its probe is `ready`;
     otherwise the ready assistant with the highest effort ceiling. There
     is no fixed ranking of providers.
   - **Review**: must be another model family than the build one; use
     `recommended_reviewer` as the recommended option (codex before claude).
   - **Research**: recommended is the fastest/cheapest ready assistant — a
     fast/flash model when the probe lists one, otherwise the cheapest
     ready family.
   Among the ready assistants, let
   [references/agent-profiles.md](references/agent-profiles.md) pick the
   recommendation and give its reason. It says which assistant did well
   in each job in real use, and which pairs of writer and reviewer found
   real problems.
   Each option is the assistant name plus its one-line `summary`
   (translated); the recommendation carries the one-line reason.
   **Own provider on `pi` or `opencode`:** before offering such a
   `provider/model`, read the `warnings` of its `custom_models` entry in
   `--detect` (the same traps `doctor` reports; no value is ever printed):
   a literal key instead of an environment reference, a pi `maxTokens`
   without 8192 tokens over the reasoning budget of the effort in use, an
   opencode model without a numeric `thinking_token_budget`. When one is
   present, ask: *Fix it for me* (recommended — show the exact change first),
   *I'll fix it myself*, *Use it as it is* + free text. Why:
   [references/kinds.md — Reasoning models on your own server](references/kinds.md#reasoning-models-on-your-own-server).
4. **Where each choice is saved.** One question per choice: *only this
   project* (the team shares it — the project file), *my personal default*
   (all my projects — the user file), *only this session* (temporary — the
   session layer) + free text. Personal providers and models go to the
   **user layer by default**.
5. **Confirm.** Build one `setup --plan …` from the answers — `--panes`
   and `--lane name=kind:model:effort` for the team, `--set key value` /
   `--user-set key value` for config keys, `--session-set key value` for
   the session — and show its output: the exact change of every file it
   would touch — `key before → after` for the config files, a unified
   diff for the instruction file, `.claude/settings.json` and (when the
   write would add it) `.gitignore` or the local `info/exclude` with
   `--local` (it writes nothing). Options: *Write it*
   (recommended
   — it matches your answers), *Adjust* (the user says what changes; the
   plan is rebuilt and shown again), *Cancel* + free text.
6. **Write.** `setup --panes 2|3|4 --lane name=kind[:model[:effort]]…`,
   `config set <key> <value> [--user]`, `session set <key> <value>` — the
   same keys the plan showed — then `setup` (instruction block + hooks) and
   `doctor`; act on whatever still warns. If the plan used `--local`, keep
   `--local` on both setup writes (`setup --local --panes …`, then
   `setup --local`) unless `setup_target=local` is already effective.

### How the answers are built (mechanics)

`setup --detect` prints JSON and writes no files: every known kind with
`installed`, `family`, `effort_ceiling`, a short English `summary` (translate
it for the user), up to three newest model ids when the CLI answers (a
missing or silent CLI yields an empty list, not a failure), and
`custom_models` for the generic kinds — the models the user declared in
`~/.pi/agent/models.json` (pi) and in `opencode.json` (project and user),
as `provider/model`, with the highest declared reasoning level when there
is one. Secrets stay in those files: only ids and levels are read. It also
prints `panes`, `lanes`, the effective lanes and the presets for 2, 3 and 4 (each lane with its capacity, `panes`),
the effective value and source of `max_workers`, `multi_role`,
`reuse_workers`, each `role.<role>.kind`, each `model.<kind>.worker`, and
`recommended_reviewer` (installed kinds only; the probe refines it to the
kinds that answer a real prompt).

`setup --probe [--kind K --model M] [--timeout SECONDS]` runs one tiny
non-interactive prompt per kind/model (claude `-p`, codex `exec`, grok
`-p`, agy/gemini `-p`, cursor-agent `-p`, pi `-p --no-session`, opencode
`run`; `--timeout` or `HERDR_SOHO_PROBE_TIMEOUT` whole seconds ≥ 1,
default 20) and classifies: `ready`, `no-auth` (login message), `quota`
(the same provider messages the wait detects), or `error` (a timeout is
an error). The `cause` never copies CLI text — it is a fixed category:
`not installed`, `timeout after <N>s`, `not authenticated`, `quota
exhausted` (with `; renews <date/time>` only when the renewal line
carries one), or `exit <code>`. It opens no pane, needs no Herdr, and
never prints the CLI output — only the classification and cause. Without
`--kind` it probes every known kind with the model `spawn` would use
(`model.<kind>.worker`, then `model.<kind>`, else the CLI default; the
rows carry `source: "configured"`), plus up to 5 own models of each
installed `pi`/`opencode` from `--detect` (`source: "custom"`, in detect
order); the rest of the list is reported as `skipped_custom` (`{kind,`
`id}`), each probeable with `--kind K --model provider/model`.

`setup --plan` (same arguments as `setup`/`config set`/`session set`, via
`--panes`, `--lane`, `--set`, `--user-set`, `--session-set`) simulates each
write in its own temp dir and prints a `diff -u` (`a/<path>` and `b/<path>`)
of the instruction file (`AGENTS.md`/`CLAUDE.md`), `.claude/settings.json`,
and — when the write would add it — the repo's `.gitignore` (the
`.herdr-soho/` entry that `setup` and `session set` refresh); the config
files (`.agents/herdr-soho.conf`, the user file, `session.conf`) keep the
`key  before → after` lines. It writes nothing — not even the state dir.
Use it for the confirmation step and whenever the user asks "what would
that change?".

`doctor --fix --panes 2|3|4 [--user|--session]` does the same normalization
on a legacy file (`--session` targets the workspace's `session.conf` and
exits 2 outside a resolvable Herdr workspace). A file whose lanes are a preset (none, a new one, or the old
`build/explore/review` and `build/read`) keeps no lane roles, `max_workers`
or `split_max_panes`: the preset is resolved at run time. A capacity you
set on a lane the preset has (`lane.build.panes=3`) is kept.
`lane.read.*` moves to `lane.review.*` when the new preset has a review lane
and that key is not set yet; `lane.explore.*` and keys of lanes the preset
does not have are removed, each with a line saying why. A file with custom
lanes keeps them and gets `max_workers` equal to the sum of their
capacities and `split_max_panes` equal to `panes` — each plus `flex_extra`
in flex mode, so the temporary worker still fits. Both get `panes` and
`reuse_workers=on`. `doctor` itself warns about the old presets and about
lane keys for lanes that no longer exist. For each lane it
resolves every role's kind and model (the value in that file, otherwise the
role frontmatter). When they agree it writes `lane.<name>.kind` / `.model`
and only then removes those `role.<role>.*` keys. When they disagree it
leaves the keys, lists `role=kind`, and tells you to ask and run
`setup --lane <name>=<kind>[:<model>[:<effort>]]`. `role.planner.*` is
removed either way. Comments stay. It prints the file it updated as a
`diff -u` with `a/<file>` and `b/<file>` labels (`no changes in <file>`
when nothing moved), like `setup --plan`. Without `--panes` and without `panes`
in the file, `--fix` exits 2 and tells you to ask 2, 3 or 4 — it does not
choose. In that case, run steps 2–5 above (the panels question, then the
plan and confirmation) and finish with `doctor --fix`.

`multi_role=on` (the default, including when the key is unset): `spawn`
without `--fresh` reuses an idle worker of another role when the kind, the
cwd and the resolved model are the same, the worker's `approvals` are
at least the request (`ask` < `edits` < `full`), and the native args it
opened with (roster column 14) are the ones this spawn would pass (native
args hold for the whole process). The same
role is tried first. A worker that has held an edit role — `implementer`, `designer`,
`tasker`, or any role with `mode: edit` — is never reused as `reviewer`,
`security-reviewer`, `ui-reviewer` or `inspector`. Spawn then opens a new
worker, and `max_workers` applies. `multi_role=off` reuses only the same
role.

The roster file gains columns after the original eight. Old lines
stay valid and are reused only for the same role when `lanes=off`. The
columns are `model`, `approvals`, `roles` (comma-separated history, for
example `scouter,implementer`), `lane`, `burst` (a temporary worker of the
flex mode) and `args` (the configured native args it opened with:
`args.<kind>` plus `lane.<name>.args` or `role.<role>.args`), then `effort`
(column 15, the effective effort at spawn; empty when the CLI chose it). Column 4
stays the current role.
With lanes on, reuse stays inside the lane. With `lanes=off`, reuse across
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

- `wait`, `status` or `dispatch` returns `quota` (exit 11). The JSON carries
  `lane`, `kind`, `model`, the sanitized `match` and, when the screen showed
  one, `renewal`. Same question format as setup: three options + free text.
  *Switch the assistant* (recommended when another assistant's probe is
  `ready` — `recommended_reviewer` first; say which one), *Wait for the
  renewal* (when the JSON names a time), *Take the slice in this session*
  (pausing is the free text). When the work resumes on a new worker, put
  `git diff` of the partial edit in the brief so it continues instead of
  starting over.
- `spawn`, `wait`, `status` or `dispatch` returns a provider failure
  (exit 14). `spawn` prints the sanitized cause in its error and leaves the
  pane open; `wait`, `status` and `dispatch` return `provider-error` or
  `capacity` with a sanitized JSON `cause`, `lane`, `kind`, `model` and
  `retries` on capacity. Read the pane first. For a terminal authentication
  cause, repair the
  CLI's login or key before starting or dispatching again. For a timeout,
  outage or capacity stop, the options are *Resend the brief to the same
  worker* (recommended when a short probe shows the provider answers
  again), *Switch the assistant* (say which ready one), *Wait* + free text.
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
  `gh issue list --repo <feedback_repo> --search "<keywords>" --label herdr-soho`
  first to avoid duplicates. Every line of the log keeps the four columns
  (date, level, command, message; newlines are sanitized out of the
  message), and `friction add "<text>" [--brief <path>]` records a friction
  the tools do not log themselves (level `note`, command `friction`;
  `--brief` appends ` (brief: <path>)`).
- **Policy** is the `feedback` config key:
  - `ask` (default): tell the user what you would file, and file it only
    after they agree;
  - `on`: file it directly and mention it in your final message;
  - `off`: never file, just describe the friction in your final message;
  - `local`: a maintainer of the skill works on this machine. Send the
    report to that maintainer instead of filing an issue (below).
- **How:** fill [templates/issue.md](templates/issue.md) (scenario, what
  happened with exact error text or JSON line, what was expected, the
  output of `$S env` and `$S config`, evidence paths, optional proposed
  change), then:

  ```bash
  gh issue create --repo "$("$S" config | awk '$1=="feedback_repo"{print $2}')" \
    --title "herdr-soho: <one line>" --label herdr-soho --body-file /tmp/herdr-soho-issue.md
  ```

  Redact secrets and customer data from evidence. Never paste a full report
  from a private repo; quote the lines that show the problem.
- **With `feedback=local`:** write the same template to a file, then:

  ```bash
  $S feedback send /tmp/herdr-soho-friction.md "<one-line summary>"
  ```

  - The report is saved as `<feedback_dir>/from-<project>-<date>.md`, with
    `-b`, `-c`, … when that day already has one; it never overwrites.
    `feedback_dir` must be an absolute path to an existing directory
    (`doctor` warns otherwise).
  - The pane or agent in `feedback_to` gets one line with the summary and
    the path.
  - Without `feedback_to`, only the file is written.
  - It prints one JSON line. Exit 4 means the file was saved but the
    notice failed: tell the maintainer yourself.
  - Do not edit the skill, its installed copy, or another project's roles
    or config to work around the friction. The maintainer answers and
    tells you when a change needs your project's config.

## Testing the skill

The ported commands have JS tests that run under either runtime:

```bash
node --test scripts/test/                # JS tests (Node 20+)
bun test --timeout 60000 scripts/test/   # the same tests under Bun
```

Bun's default per-test timeout (5 s) is too short for the process-heavy
tests on slower hosts such as Windows, hence `--timeout`.

The regression matrix is every suite in `scripts/test-*.sh` — bash suites
that exercise the JS through the POSIX `scripts/herdr-soho` launcher — each run
both inside Herdr (`HERDR_ENV=1` with a test pane/workspace) and outside.
Run it through the parallel hermetic executor, never a hand-rolled loop:

```bash
scripts/run-tests.sh                              # every suite × inside+outside, parallel
scripts/run-tests.sh --env outside test-kinds.sh  # one suite while iterating
scripts/run-tests.sh --bash /bin/bash             # also run the matrix on that interpreter
scripts/run-tests.sh --jobs 4                     # cap the parallel jobs
```

The old bash↔JS parity tests are golden files under `scripts/test/golden/`
(recorded from the bash behavior before the port): an intentional behavior
change re-records them with `HERDR_SOHO_GOLDEN=update`, then review the
diff.

Every run gets its own `HOME`, `XDG_CONFIG_HOME` and `TMPDIR` inside a temp
dir and loses every `HERDR_SOHO_*` variable from the parent environment,
so no suite reads `~/.config/herdr-soho`, `~/.pi` or `~/.config/opencode`.
The temp dir is removed on exit (failure included) unless
`HERDR_SOHO_KEEP_TEST_LOGS=1`. Output is one `PASS|FAIL <suite> [<env>,
<bash>] <seconds>s` line per run plus a summary; on failure the last 30 log
lines of each failed run are printed. Exit: 0 all passed, 1 any failed,
2 invalid usage.

Test rule for briefs: while iterating, a worker runs only the suite that
covers the item (`scripts/run-tests.sh --env outside test-<x>.sh`); the full
matrix (`scripts/run-tests.sh`) runs once, right before the report.

## Safety

- Never `herdr server stop`; never close panes, tabs, or workspaces this
  skill did not create.
- Prefer `--current`, explicit pane IDs, and unique agent names. Parse IDs
  from JSON, never from sidebar order.
- Briefs and reports may contain repo content; keep secrets out of them.

## References

- [references/troubleshooting.md](references/troubleshooting.md) — observed failures, causes, fixes, and how to validate a kind; read before changing the script
- [references/orchestration-contract.md](references/orchestration-contract.md) — the delegation contract this skill enforces
- [references/kinds.md](references/kinds.md) — kind → family table, generic kinds (pi/opencode) with config and provider examples, and install notes
- [references/agent-profiles.md](references/agent-profiles.md) — strengths and weaknesses of each assistant per role, from real use; read before choosing a team
- [templates/brief.md](templates/brief.md), [templates/report.md](templates/report.md)
