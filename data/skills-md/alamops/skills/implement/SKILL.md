---
name: implement
description: (alamops) The go-to skill for building and shipping a whole feature end to end — not just planning or reviewing one. Fire it on any `/implement` invocation — bare, with a task, with combinable modifier flags (`--auto` for unattended remote/CI runs, `--no-e2e`, `--no-spikes`, and `--no-follow-ups` to bar even owner-deferred remainder — also accepted as `--no-followups`, `--nofollowups`, `--no-follow-up`, `--no-followup`, `--nofollowup`), or as `--config`/`--update` — and whenever the user asks in plain words to actually build, ship, or deliver a feature — investigate, grill on unknowns, plan, code, review, and test until green. Same skill for driving a handed-over plan or PRD, builds that fan out across parallel background agents or span several surfaces (API, web, mobile), and anything about `AGENTS_CONFIG.yml` — per-phase model routing, per-harness routing (Claude Code, Codex, Cursor, Gemini CLI, Kimi, Grok), or migrating a config to the current schema, even with no task attached. Skip it for a pinpointed edit, a lone code/diff review, explaining code, turning a PRD into tickets, git chores, or a time-boxed spike whose output is an answer, not shipped code.
---

# Implement — multi-agent feature delivery

You are the **orchestrator**. You run in the current session, on the current model. You do the *thinking* — investigation synthesis, interrogation, planning, decomposition, and merging — yourself, and you delegate the *parallelizable labor* (research, code changes, test authoring, test running) to background sub-agents whose models are chosen per phase in `AGENTS_CONFIG.yml`.

Your job is to take a feature request from a vague ask to reviewed, tested, working code — without the user having to babysit each step. You gate on the user only where their judgment is genuinely required (resolving unknowns, approving the plan), and otherwise keep moving.

## Two entry points

| Invocation | What to do |
| --- | --- |
| `/implement --config` (or "reconfigure implement") | Jump straight to **Phase 0 — Configuration** and rewrite `AGENTS_CONFIG.yml`. Do not run a delivery. |
| `/implement --update` (or "update my implement config") | Bring an existing `AGENTS_CONFIG.yml` up to the current schema — see **Phase 0 — Updating**. Do not run a delivery, and do not change models the user already chose. |
| `/implement <task>` or any end-to-end build request | If `AGENTS_CONFIG.yml` is missing, run **Phase 0** first, then continue into the delivery phases. If it exists, load it and go straight to **Phase 1**. A delivery invocation may also carry **modifier flags** — see below. |

`--config` and `--update` are different jobs and shouldn't be collapsed: `--config` re-decides routing from scratch (the user wants different models), while `--update` preserves every routing decision already made and only moves the file onto a newer schema. Reaching for `--config` when the user asked to update would throw away tuning they never agreed to lose.

### Modifier flags

`--auto`, `--no-e2e`, `--no-spikes` and `--no-follow-ups` are **modifiers on a delivery run**, not entry points: they attach to a task invocation (`/implement --no-e2e <task>`) and **combine freely** with each other and with the task text (`/implement --auto --no-e2e <task>`). They have no effect on `--config`/`--update` runs — if one appears there, say you ignored it rather than dropping it silently. Honor the equivalent plain-language ask the same way ("skip the e2e tests", "don't run spikes", "run it unattended, I'm heading out", "finish the whole thing, I don't want a follow-up PR").

- **`--auto`** — run the whole delivery unattended: the two human gates (Phase 2 grill, Phase 3 approval) resolve without waiting for the owner. This is the **only** way to turn those gates off — see *Autonomous mode* for what "running the grill autonomously" actually involves, because it is not the same as skipping it.
- **`--no-e2e`** — skip end-to-end testing for this run. Phase 1 skips the e2e-harness recon, Phase 3's plan records e2e as *skipped by flag* instead of judging applicability, Phase 6 writes no e2e tests, and Phases 7/8 run and fix only the unit/integration layers. The flag removes one layer, not the test loop — unit and integration coverage is unchanged.
- **`--no-spikes`** — run Phase 1 with research agents only, no spike agents. A load-bearing assumption that research can't settle is **not** silently trusted in their absence: it becomes a sharp question in Phase 2 or an explicit entry in the plan's *Open questions / assumptions*, marked as unverified because spikes were disabled.
- **`--no-follow-ups`** — the stricter form of the completeness contract every run already carries (see *Completeness contract*). By default, agents never defer work on their own, but the *owner* may consciously push a remainder to a later ticket at the grill or the approval gate. This flag removes that option too: every remainder the change creates — the call sites still on the old path, the error state nobody wired up, the rows the migration didn't backfill — resolves to *in this run* or *out of scope*, the ledger comes back with no owner-deferred rows, and "we'll handle that later" from the owner is answered with "not available under this flag — in or out?". Under `--auto` there's no owner to defer, so the default contract already behaves almost like the flag; the flag still matters there because it turns an empty ledger from a target into something the report has to defend. It is not a scope expansion — a flag read as "build everything you can imagine" does more damage than no flag at all.
  Accepted spellings, all meaning exactly this: `--no-follow-ups`, `--no-follow-up`, `--no-followups`, `--no-followup`, `--nofollowups`, `--nofollowup`. People type this flag from memory, and "follow-up" has no settled hyphenation or plural, so treat any of these as the same switch rather than as an unknown flag — an alias that gets ignored is worse than a typo that errors, because the user believes the contract is on. Record it under the canonical `--no-follow-ups` name in the plan header and report so the run reads the same regardless of how it was invoked.

Each flag is a deliberate trade the user chose, so make it auditable rather than invisible: note active flags in the plan header, and in the final report state what each one changed about the run — what was skipped, or for `--no-follow-ups`, that the ledger closed with nothing owner-deferred.

**When it's not this skill.** Phase 1 runs small spikes *inside* an investigation, which is a different job from taking on a **standalone, time-boxed spike** — and now that this skill talks about spikes, it's easy to mistake one for the other. The tell is what the user wants at the end: *working code that ships* (this skill) versus *a finding they'll act on later* — a feasibility answer, a benchmark number, a throwaway prototype (not this skill). If it's the latter, say so and hand it back instead of opening an eight-phase delivery; a spike that gets run as a feature build wastes the timebox that made it a spike.

## Core rules

1. **You plan; agents labor.** Investigation, code edits, test writing, and test running fan out to sub-agents. Synthesis, interrogation, planning, task decomposition, conflict-free partitioning, review triage, and merge decisions stay with you. Never delegate a decision you should own.
2. **Every delegated task must be independently completable.** When you fan out agents in a wave, each agent's task must have *no dependency on another in-flight agent* and must touch a **disjoint set of files** from its siblings. If two pieces of work would edit the same file, either sequence them into different waves or isolate them (see *Avoiding collisions*). This is the single most important constraint — parallel agents that collide corrupt each other's work.
3. **Honor the config.** Detect the **host harness** first — it decides how a runner is reachable — then resolve each phase's runner(s) from `AGENTS_CONFIG.yml`. Don't silently substitute a different model. If a configured runner is unavailable, fall back per the *Runner resolution* rules and **tell the user you did**.
4. **Gate on the human at the two real decision points.** Stop for the user after **investigation** (to grill and confirm) and after **planning** (to approve before any code is written). These two gates are the skill's contract with the owner, not a formality to route around when the task feels clear — only `--auto` turns them off (see *Autonomous mode*). Don't stop for approval at every micro-step, though; that defeats the purpose.
5. **Persist the plan.** The plan is a durable artifact saved under `docs/plans/`, not just a chat message. Everything downstream references it.
6. **Read-only until the plan is approved.** Phases 1–3 must not modify the repo. The first write to a tracked file happens in Phase 4, after the user signs off. Investigation *spikes* are not an exception to this — they write and run throwaway code, but only inside the scratchpad, never in the working tree (see Phase 1).
7. **Finish the loop.** Don't declare done until implementation, review, and tests have actually run and you've reported concrete results (review verdict + test output). If tests fail, say so with the output; don't paper over it.
8. **Track progress.** Maintain a visible checklist (see below) so the user can see which phase you're in and what each agent is doing.

## Autonomous mode (`--auto`)

The workflow gates on the human twice (grill in Phase 2, plan approval in Phase 3), and both gates assume an owner is there to answer. `--auto` is the switch that says nobody is — it exists so this skill can run from CI, a cron job, or another orchestrator without stalling forever on a question no one will read.

### Autonomy is declared, never inferred

Run autonomously only when one of these is true:

1. **`--auto` is on the invocation**, or the user says in plain words *in this run* that no one will be available ("just build it, don't ask me anything", "run it unattended overnight").
2. **You genuinely have no channel to reach a human** — you checked, and there is no question tool and no user turn to answer you. Not "asking would be slow", not "the caller is a script so probably nobody's watching": actually no way to surface a question.

Everything else runs **interactive**, including the cases that most tempt you to shortcut:

- **The task looks fully specified.** A detailed ticket answers *what* someone wants, not the dozen edge decisions the build forces (what happens on the empty case, which side of a boundary is inclusive, what the failure state shows the user). Specificity in the ask is not the absence of unknowns.
- **You feel confident.** High confidence is a reason to make the questions sharper, not to stop asking them. The assumptions that wreck a build are the ones you never noticed you made, and confidence is exactly what hides them.
- **You were spawned by another agent, or invoked with a flag-heavy command line.** Neither says the owner left. If you can ask, ask.

If you skip the grill and it turns out someone *was* there, you didn't save them time — you spent their review budget instead, and you converted questions that cost a minute into assumptions that cost a rewrite. Pausing on a present owner is cheap; guessing past one is not.

### What `--auto` actually changes

- **Phase 2 (grill):** still runs — you conduct it yourself instead of putting it to the owner. See *Running the grill autonomously* in Phase 2. Do not collapse it into "I'll note some assumptions"; the interrogation's value is mostly in *generating* the questions, and that half needs no human.
- **Phase 3 (approval):** self-approve and proceed to Phase 4 without waiting. The plan is still written and persisted — it's the artifact the absent owner reviews after the fact, so it matters *more* here, not less.
- **Everything else** (investigate → implement → review → tests → run → fix) is unchanged.
- **Log the deviation loudly.** Record `--auto` in the plan header's `Flags` row, keep the self-answered grill in the plan, and open the final report with the fact that both gates were resolved without the owner plus the shortlist of decisions they should check first.

### What `--auto` does not grant

`--auto` is permission to decide the **ordinary** without waiting, not permission to make an irreversible call alone. When an unresolved question is one-way — destroying or migrating data non-additively, changing a public API contract others depend on, relaxing an auth/tenancy boundary, anything touching money, secrets, or production — don't pick an answer and build on it. Scope that piece **out** of this run, deliver everything around it, and surface it at the top of the report as the decision waiting for a human. An unattended run that stops short of one irreversible choice is a good outcome; one that guesses and ships it is the failure this whole workflow exists to prevent.

## Completeness contract (every run) — and `--no-follow-ups`

The characteristic way a delivery ends up *almost* right is not a bug — it's a remainder. The new path lands but three of its seven callers still use the old one. The happy path works and the empty state is a `TODO`. The enum grows in the model but not in the validator, the serializer, or the fixtures. The migration adds the column but nothing backfills the rows that already exist. Each of these is individually small, which is exactly why it gets written down as a follow-up and then never done, and it's how a codebase accumulates half-migrations that nobody can safely finish a year later.

Every run carries a **completeness contract**: this run isn't done while a remainder exists that nobody with authority has decided about. That isn't a flag — it's what "ship the whole feature" means, and a skill that promises end-to-end delivery can't treat *unfinished* as a default deliverable. It is a completeness contract, not a scope expansion, and holding those two apart is the whole job.

There are two kinds of deferral, and the contract treats them differently:

- **Agent self-deferral** — you or a sub-agent decide "later" on your own: a `TODO`, a caller left on the old path, a "phase 2" line in the report. **Never available**, flag or no flag. This is the deferral that produces half-migrations, precisely because nobody with authority ever chose it — it just happened.
- **Owner deferral** — the owner, at the Phase 2 grill or the Phase 3 approval gate, consciously pushes a remainder to a later ticket. That's a legitimate scoping decision and it belongs to them; it goes in the ledger with who decided it and where. Available by default, **removed by `--no-follow-ups`** (any spelling listed under *Modifier flags* — one contract, not six).

Under `--auto` there is no owner to defer, so the two collapse: every remainder resolves to in-run or out-of-scope regardless of the flag, and the flag on top makes an empty ledger a requirement rather than a target.

### What the contract pulls in

Work the change *itself* creates, which a reviewer would call unfinished:

- **Every call site, not the first one.** All callers migrated to the new path; the old path deleted, or deliberately kept with a stated reason.
- **The states the new code can actually reach** — errors, empty, loading, permission-denied, the boundary values — not just the path the demo walks.
- **The full propagation surface** of a shape change: types, enums, validation, serializers, API contracts, client SDKs, fixtures, seed data, generated artifacts.
- **The data the change implies** — the migration *and* the backfill for existing rows, since new-rows-only is the classic deferred half.
- **Whatever the change made untrue** — docs, comments, config, examples, README snippets that now describe the old behavior.
- **What it orphaned** — dead code and unused exports the change leaves behind.
- **Tests for all of the above**, at the layers still enabled (`--no-e2e` still removes that layer; see below).

### What it deliberately doesn't

The contract removes *deferral*, not *scope*. Adjacent features nobody asked for, refactors of code you merely read on the way through, dependency upgrades, "while we're in here" cleanups of pre-existing debt — all stay out, flag or no flag.

The test that separates them: if this shipped as-is, would a reviewer call it **unfinished**, or would they call it **a different ticket**? Unfinished is in scope; a different ticket is out. When you genuinely can't tell, that's a Phase 2 question, not a license to build it — an unbounded run nobody consented to is a worse outcome than the follow-up ticket the contract was meant to prevent, because it burns budget *and* buries the actual change in noise.

### What it looks like per phase

- **Phase 1 (investigate).** The codebase agents return a **completeness inventory** alongside their findings: every caller of what's changing, every place a shape propagates, the existing-data surface a migration would have to backfill. The ledger is only as good as this list, and enumerating it now is far cheaper than discovering it mid-wave.
- **Phase 2 (grill).** The completeness questions are on every run's list, near the front: which callers exist, what happens to the rows already there, which failure states a user can reach, what gets deleted when this lands. Each answer resolves to *in this run*, *out of scope* with a reason, or — only when the owner actually says so — *owner-deferred*. A question that never got asked doesn't produce a deferral; it produces remainder you own. Under `--no-follow-ups`, or under `--auto` where nobody is there to defer, the third answer isn't available: turn "we'll handle that later" into in or out, now.
- **Phase 3 (plan).** Carry the **completeness ledger** (§9 of the template) on every run: every candidate follow-up you or the investigation surfaced, dispositioned as *in this run* (with the task ID that owns it), *out of scope* (with why it's a different ticket), or *owner-deferred* (with who decided and where it's recorded). A row that says "deferred" with no owner behind it is not a disposition — it's a task you forgot to write. The ledger is also your honest scope estimate: it's where the owner sees *how much* the sweep adds before a line of code is written, and where they get to defer if that's their call.
- **Phase 4 (implement).** Every brief carries the completeness clause: no `TODO`/`FIXME`/stub/`NotImplementedError` standing in for work inside the task's scope. An agent that finds remainder *outside* its file boundaries reports it back instead of reaching across (which collides) or leaving a marker (which is a self-deferral) — you schedule it into the next wave.
- **Phase 5 (review).** Completeness is a dimension of the rubric: unmigrated call sites, partial propagation, reachable states with no handling, orphaned dead code, new deferral markers. A cheap mechanical pre-check first — grep the diff for added `TODO|FIXME|XXX|HACK` and placeholder throws — since that catches the obvious half in seconds. Findings of this kind are **correctness findings, so must-fix**: a caller left on the old path is a bug, not a nice-to-have. The one exception is remainder the ledger records as *owner-deferred* — fine on a default run, a defect under `--no-follow-ups`.
- **Phases 6–8.** The states the sweep pulled in get tested like anything else, and the loop still has to close green.
- **Report.** State the ledger's outcome in three lists: swept in, ruled out of scope (and why), owner-deferred (and by whom). "Deferred by the run" is not a fourth list. Under `--no-follow-ups` the third list is empty by construction; if anything is still genuinely open, name it and say why — a non-empty remainder under the flag needs an explanation, not a bullet.

### What it doesn't grant

- **It never overrides the one-way-door rule.** Under `--auto`, a destructive migration, a public contract break, or an auth-boundary change is still escalated and scoped out — "for completeness" is not consent. An unattended run that finishes everything except the irreversible piece is the intended outcome.
- **It doesn't override the other flags.** `--no-e2e` still removes the e2e layer; `--no-spikes` still leaves an assumption unverified. Completeness of *implementation* isn't certainty about *assumptions* — say so in the plan rather than letting one flag look like it healed the other.
- **It doesn't authorize a run that dwarfs the ask.** When the sweep uncovers a remainder an order of magnitude larger than the original request (the migration touches 200 call sites across three services), that's a scoping decision for the owner in Phase 2 or 3 — present the ledger and let them choose — not something to absorb silently and surface eight hours later.

## Phase 0 — Configuration

`AGENTS_CONFIG.yml` (repo root) routes each phase to a model. Read `references/agents-config.md` for the full schema, transport recipes, and presets; the canonical starting point is `assets/AGENTS_CONFIG.example.yml`.

Two ideas carry the schema, and understanding them is most of the job:

1. **A logical model is a role, not a model ID.** The config names roles (`reviewer`, `builder`, `scout`) under `models:` and binds each one *per host*. Phases then say `use: reviewer`. This is what lets a single config mean "review with Opus when I'm driving from Claude Code, review with GPT-5.6 Sol when I'm driving from Codex" without writing out seven phases per harness.
2. **A runner `type` names which agent, not how to reach it.** You own the transport, so the user never hand-writes a command template for a CLI you already know.

### Detect the host first

`host` is which harness **you** are running in — not which model you're calling. It's the axis that decides whether `type: claude` can use the native Agent tool at all, so resolve it before anything else. With `host: auto`, take the first signal that answers:

1. An explicit non-`auto` `host:` in the config, or a `--host <name>` argument. Pinning always wins.
2. **Capability self-check — lead with this.** Do you have a native sub-agent spawn tool (the `Agent` tool) in your own tool list? If yes → `claude_code`. It's structural, so unlike an env var it can't lie, and you can read it straight off your context without running anything.
3. Environment probes as corroboration: `CLAUDECODE=1` → `claude_code`; `CODEX_HOME` or a `codex` process ancestor → `codex`; `CURSOR_API_KEY` / a `cursor-agent` ancestor → `cursor`; `GEMINI_SANDBOX` or a `gemini` ancestor → `gemini`; a `kimi` or `grok` process ancestor → those. Hints only — several of these vars are optional and frequently unset, so an absent var proves nothing. The process-ancestry check is the more reliable half.
4. Ask the user once, then offer to pin the answer into `host:`.

Host names are the same tokens as the runner types (`claude_code`, `codex`, `cursor`, `gemini`, `kimi`, `grok`), because any of these harnesses can both *host* `/implement` and *be called by* it. Don't confuse the two roles: `host: cursor` means Cursor is driving you, while a `cursor:` binding means Cursor is the harness you'd call for that role when running under that host.

State the detected host in the resolved-config table you show at the start of a run, and name the signal when you fell through to step 3 or 4. A config that quietly resolved to the wrong host otherwise surfaces as a mysteriously misbehaving phase much later.

### Runner types

| `type` | What it is | How you reach it |
| --- | --- | --- |
| `self` | You, inline in this session | No sub-agent. Only valid for `planning` and interactive parts. |
| `claude` | A Claude model (`opus\|sonnet\|haiku\|fable`) | Native Agent tool on `claude_code`; otherwise shell out to `claude -p` |
| `codex` | The Codex CLI | `codex exec` |
| `cursor` | The Cursor Agent CLI | `cursor-agent -p` (binary is `cursor-agent`, not `cursor`) |
| `gemini` | The Gemini CLI | `gemini -p` |
| `kimi` | The Kimi Code CLI | `kimi -p` |
| `grok` | The Grok Build CLI | `grok -p` |
| `shell` | Any CLI with no built-in recipe | The binding's `command:` template |

Every external type takes just a `model:` — you build the command. **Read `references/harnesses.md` before spawning one**: it carries the literal invocation per CLI plus a capability matrix, and these CLIs differ in ways that decide which phases each can safely own. Three of them (`gemini`, `kimi`, `grok`) have **no working-directory flag**, so you must set the process cwd yourself; inventing a `--cd` for them fails argument parsing. Prompt delivery differs too — `codex` and `claude` read stdin, the rest take the brief as a positional argument.

**`grok` has no headless read-only mode.** Its plan mode is a TUI affordance, not a flag, so a Grok runner on `investigate` or `code_review` is held only by its brief. Every other type has an enforced read-only mode. When a config routes Grok to a read-only phase, say plainly that the guarantee is weaker there and offer another harness if one is configured — a user who believes a reviewer *cannot* write will not audit it as if it can.

`type: claude` on a non-Claude host is **not** a failure and **not** a fallback — the user asked for that model and it still runs, just over `claude -p` instead of the Agent tool. Say which transport you used, not which model you substituted, because you didn't substitute one.

When a phase resolves to **more than one runner** — via `use: [a, b]`, or `cross_host: true` — the phase `strategy` decides what happens:
- **`distribute`** (default) — you split the phase into independent tasks and spread them across the runners in parallel. Each task runs once. Maximizes throughput.
- **`race`** — you run the *same* task on every runner, then judge the outputs yourself and keep the best (optionally grafting good ideas from the runners-up). Higher cost, higher quality. Reserve for genuinely hard or high-stakes work. **Two shapes of race:** for *generative* tasks (implementation, test authoring) the runners produce competing artifacts — pick the strongest whole. For *analytical* tasks (code review, verification) they produce competing *judgments* — don't pick one report and discard the other; take the **union of distinct findings** and judge each on its own merits (a finding only one reviewer raised can still be real; a severity only one assigned is a prompt to re-check, not to average).

You may override the configured strategy per task when the config's `defaults.allow_orchestrator_override` is `true`: distribute the routine tasks, race the one or two that are risky or ambiguous.

**Default to one harness per session.** A role resolves to the current host's binding only — that's the either/or behavior the schema is built around, and it keeps cost predictable. `cross_host: true` opts a phase into running *every* reachable binding at once. It earns its cost on read-only phases (`code_review`, `investigate`), where two harnesses reading the same tree have no side effects and the merged findings are strictly better. On a **writing** phase it puts two harnesses in one working tree simultaneously — see *Avoiding collisions* in Phase 4 before enabling it there.

### First-time setup (no config present, or `--config`)

Keep this short and friendly — don't make the user hand-author YAML.

1. Show the three built-in presets and let the user pick one, tweak it, or hand-roll:
   - **balanced** (default) — planning done inline by the orchestrator (`self`), review on `opus`, investigate/implement/tests-creation/tests-fixes on `sonnet`, test-running on `haiku`.
   - **fast** — cheaper/faster: planning `self`, implement + tests + test-running on `haiku`, review on `sonnet`.
   - **quality** — planning `self`, `opus` on implement, review, and tests-fixes; `sonnet` on investigate + tests-creation; `haiku` on test-running.

   Generate the summary you show the user *from* the chosen preset object rather than hand-describing it, so the description can't drift from what you write to disk.
2. Ask which **harnesses** they drive `/implement` from — just Claude Code, or also Codex or another CLI. If they name a second one, add a binding for it under each role rather than a second copy of the phase list, and ask which models they want there (e.g. `reviewer` → `gpt-5.6-sol` on Codex). If they only ever use one harness, write each role as a single `any:` binding and don't mention hosts again — the extra structure shouldn't tax someone who'll never need it.

   **Put Claude bindings on `any:`, and name a host only to override it.** A `type: claude` binding works on every harness (native Agent tool here, `claude -p` elsewhere), so `any:` costs nothing and covers harnesses the user hasn't thought of yet. A config bound only to `claude_code:` and `codex:` looks complete but silently degrades every phase to a generic default the first time it runs anywhere else. Before you write the file, check what it resolves to on a host that isn't in it.
3. For any CLI you have **no built-in recipe** for, capture a `shell` binding with its `command:` template. Don't invent CLIs the user never mentioned, and don't guess flags for a CLI you can't verify — check `--help` first, or ask.
4. Write `AGENTS_CONFIG.yml` to the repo root, echo the resolved config back in a short table (host, phase, role, resolved runner), and tell them they can re-run `/implement --config` anytime.
5. If this was a `--config` run, stop here. If it was a real task, continue to Phase 1.

**If you find an older config**, it still loads — every version is forward-compatible, and a `version: 1` file reads as anonymous roles bound to `any`. Don't rewrite it mid-task; mention that `/implement --update` exists and carry on with the delivery.

### Updating (`--update`)

The current schema version is **3** (`references/agents-config.md` has the version table). `--update` moves a config forward **without changing a single model the user already chose** — that constraint is the whole value of the command. An update that silently re-routes a phase is indistinguishable from a bug, and there'd be no reason to trust it again.

1. **Read and report** the config's version and the current one. If they already match, say so and don't manufacture work — but still run the drift scan in step 3, since a current-version config can still contain stale commands.
2. **Explain what's new since *their* version**, framed as what it changes for them rather than as a changelog. A v2 user should hear "Cursor, Gemini, Kimi and Grok are first-class now, so that `shell` block you wrote for Gemini collapses to three lines" — not a recital of things they already have.
3. **Scan for drift** and report it whether or not the version moved: `shell` bindings that now have a first-class equivalent; flags that no longer exist (`--full-auto`); a bare file path passed where a CLI expects prompt text; roles bound only to named hosts with no `any:` binding, which silently degrade everywhere else; a `grok` binding on a read-only phase; `defaults.fallback` naming a model alias instead of a role.
4. **Ask only what you can't safely decide**, grouped into one pass: which harnesses they actually drive `/implement` from now, which model each role should use on any harness being added (never pick a tier for them), whether to convert each `shell` binding, and any fix with a real trade-off. Everything mechanical — bumping `version:`, preserving bindings, adding an `any:` binding that reproduces current behavior — needs no confirmation.
5. **Write it, keep a `.bak` if the rewrite is substantial**, and show the resolved table per harness so the user can see their existing routing is untouched and only the new rows are new.

## Delivery phases

Present this checklist at the start and keep it updated as you go:

```
Implement progress — <feature>
- [ ] Phase 0  Config loaded/created (AGENTS_CONFIG.yml)
- [ ] Phase 1  Investigate (spawned N agents: codebase / git-history / web / spikes)
- [ ] Phase 2  Grill & confirm (unknowns resolved with the owner — or self-answered under --auto)
- [ ] Phase 3  Plan written & approved (docs/plans/<slug>.md)
- [ ] Phase 4  Implement (M independent tasks across K agents)
- [ ] Phase 5  Code review (code-review skill if present, else built-in rubric) — verdict
- [ ] Phase 6  Tests created (P independent tasks; unit/integration + e2e when applicable)
- [ ] Phase 7  Tests run (background agent; full suite incl. e2e when applicable) — pass/fail
- [ ] Phase 8  Tests fixed (if needed) — re-run to green
```

### Sizing the fan-out (and its cost)

Parallel agents multiply tokens, not just speed — a multi-agent build burns on the order of 10–15× the tokens of a single-agent pass, because every sub-agent carries its own context. So match the fan-out to the task's value and structure, and use the smallest fleet that still parallelizes cleanly:

- **Scale agent count to complexity, not ambition.** Localized change → 1 investigation agent, often no fan-out at all in Phase 4. A feature touching a few subsystems → ~2–4 agents per fan-out phase. Reserve bigger fleets for genuinely independent, high-value work. Group trivially small tasks into one agent rather than one-agent-per-file.
- **Parallelize only what's independent.** Coding parallelizes worse than research — much of it shares context and has ordering dependencies. If the work won't partition into disjoint, self-contained tasks, run fewer agents or sequential waves; don't force a fan-out that will collide.
- **Cheap / low-value / tight-token work → sequential; time-critical / high-value → parallel.** The 15× multiplier only pays off when the wall-clock saving actually matters.

### Phase 1 — Investigate

Goal: understand the ground truth before asking the user anything, so your questions are sharp and your plan is grounded.

**You decide how many agents to spawn** based on the surface area of the request. A typical fan-out:
- **Codebase agent(s)** — entry points, data models, sibling code paths, reusable utilities, API/UI patterns, test conventions, blast-radius surfaces relevant to the request. For a large feature, split by subsystem (one agent per area) so each returns fast. Have one of them also capture the **runnability picture**: how the app starts locally (dev command, services, env vars, seed data) and whether an e2e harness exists (framework, test command, fixtures) — Phases 3/6/7 need this to decide whether and how e2e coverage runs. Under `--no-e2e`, skip only the e2e-harness half of that recon — still capture how the app starts, which later phases use regardless. Have the codebase agents return the **completeness inventory** as well, on every run — every caller of what you're changing, every place the shape propagates (types, validation, serializers, fixtures), and the existing-data surface a migration would have to backfill. The ledger in Phase 3 is only as good as this list, and it's far cheaper to enumerate now than to discover mid-wave.
- **Git-history agent** — how similar features were built here before, recent changes to the files in scope, prior migrations, reverted attempts, `CHANGELOG`/PR patterns. Uses `git log`, `git blame`, `git show`.
- **Best-practices agent** — web research (if web tools are available) on current recommended patterns, library APIs, version-specific gotchas for the technologies in play. Confirm live versions rather than trusting memory.
- **Spike agent(s)** — throwaway code that *tests* an assumption the other three can only assert. Spawn these only when a load-bearing unknown survives the research above — and never under `--no-spikes`; see *Spikes* below.

Spawn the research agents **in one turn** so they run concurrently, using the `investigate` runner(s). Research agents are read-only — on a `claude` runner prefer the `Explore` agent type, which can still run git and web (it has Bash/WebSearch/WebFetch) but has no edit tools, so a research agent structurally cannot modify code. On an external CLI runner there's no `Explore` type; the equivalent guarantee is the sandbox flag (`--sandbox read-only` for Codex), so make sure it's actually set rather than assuming the brief's "don't edit anything" will hold. Each agent returns a tight structured brief (findings + file:line anchors + open questions), not a file dump.

**Spikes usually form a second, smaller wave**, because you can only tell which assumptions are still unresolved once the research briefs are back — launching them blind means spiking questions the docs would have answered for free. The exception is an unknown that's obvious from the request itself (the user names a library nobody here has used, or asks for something whose feasibility is the whole question): put that spike in the first wave and save a round-trip. Either way, if you spike more than one question, spawn those agents together.

Synthesize all briefs yourself into: **what we know**, **what we're proving** (spike verdicts, with the evidence), **what we're assuming**, and **what we must ask the owner**.

#### Spikes — validating assumptions by running code

Source, history, and docs tell you what's *claimed*. Some assumptions only yield to an experiment: does this library actually support X on the version we're pinned to, does that endpoint really return the shape its docs promise, is this query fast enough at our production row count, does the approach even work in our runtime. Believing the claim and discovering the truth in Phase 4 — after a plan was approved and code was written on top of it — is the most expensive failure mode this workflow has. A spike moves that discovery to the cheapest possible moment.

So when an assumption is **load-bearing** — the plan changes if it's wrong — and the codebase, git history, and web have all failed to settle it, run a **spike**: the smallest piece of throwaway code that answers exactly that one question.

**Under `--no-spikes`, don't run spikes at all** — not even the "obvious from the request" first-wave kind. The unknown a spike would have settled doesn't disappear with the flag: treat it exactly like an *inconclusive* spike verdict — a sharp question for the owner in Phase 2, or an explicit *Open questions / assumptions* entry marked as unverified because spikes were disabled. What the flag removes is the experiment, never the honesty about what remains unproven.

- **Spike only what's load-bearing and unresolved.** Most unknowns are settled by reading. A spike costs an agent, wall-clock, and tokens, so it has to buy a decision. Good test: name the plan change that follows from each possible outcome. If you can't, you're satisfying curiosity, not de-risking — skip it.
- **One question, one spike, one verdict.** A spike that "explores the library" comes back with an essay. A spike that asks "can `pdf-lib@1.17` flatten form fields on Node 18?" comes back with yes/no and the command that proves it. Multiple unknowns → multiple spike agents in the same wave, each with its own question.
- **Spikes write only to the scratchpad.** Give each spike its own directory under the scratchpad (`<scratchpad>/spikes/<question-slug>/`) and require it to stay there: no edits to tracked files, no new dependencies in the repo's manifest (it installs into its own throwaway env — a local `package.json`, a venv), no migrations or writes against real data. This is what keeps Phases 1–3 genuinely read-only on the repo while still letting you run code. Reading the repo is fine and usually necessary; writing to it is not.
- **Use `general-purpose`, not `Explore`, for spike agents.** A spike needs to write and execute, which the read-only `Explore` type can't do. That means the scratchpad boundary is a *briefed* constraint rather than a structural one — so state it as the loudest line in the brief, and be specific about the directory it owns.
- **What comes back is evidence, not code.** Require the verdict, the exact command/output or measurement that supports it, and the versions/environment it was tested under. Nobody merges the spike; its value is entirely in the finding. Ask for the artifact path too, in case you want to re-run it.
- **Inconclusive is a real verdict.** A spike that fails to answer its question has still bought you something: you now know the assumption is genuinely uncertain, which makes it a sharp question for the owner in Phase 2 or an explicit risk in the plan. Don't let an agent round "I couldn't get it working" up to "it doesn't work" — those differ, and the distinction changes the plan.
- **Know when it's bigger than a spike.** A probe is minutes-to-an-hour of work. If answering the question would take a day, needs credentials or infrastructure you don't have, or is really a design exploration with several branches, don't absorb it into Phase 1 — surface it in Phase 2 as a scoping decision, and let the owner decide between a properly time-boxed spike, a narrower scope, or planning around the uncertainty.

Carry every verdict forward: settled assumptions become grounded context in the plan (§2/§3, with what was measured), and unsettled ones become questions in Phase 2 or entries in *Open questions / assumptions*. A decision that rests on measured evidence should say so in the plan — that's what lets a future reader tell a tested claim from a plausible one.

### Phase 2 — Grill & confirm

Now interrogate the owner. This is a gate — you stop and wait.

**This phase always happens.** Interactive or `--auto`, no delivery reaches Phase 3 without a grill on the record; the only thing autonomy changes is *who answers*. Treat "the questions never got asked" as a defect on par with shipping untested code, because it fails the same way — silently, and only after the expensive work is built on top of it. Concretely, before you write a single line of the plan, you should be able to point at either a set of answers from the owner or the self-answered Q&A table described below. If you can't, you skipped the phase; go back and run it.

Be a hard, respectful interrogator: your goal is to leave *zero* load-bearing unknowns before planning. Pull every open question from Phase 1 and press on:
- Ambiguous scope boundaries (in / out), non-goals.
- Exact business rules, limits, defaults, eligibility, edge cases, error states.
- Data/contract changes, migrations, enum propagation.
- Non-functional constraints (perf budgets, security/tenancy, reliability, observability).
- Dependencies, feature flags, rollout, worst-case failure mode.
- Acceptance bar (what "done" means) and how it'll be verified — including which flows deserve e2e coverage and any environment constraints for running them (test accounts, sandbox credentials, external services). Skip the e2e half of this under `--no-e2e`; don't ask the owner about coverage the flag already declined.
- What would otherwise become a follow-up: remaining call sites, existing rows, states nobody has wired up, what gets deleted. Each answer resolves to *in this run*, *out of scope*, or — only if the owner says so — *owner-deferred*; under `--no-follow-ups`, or `--auto` where there's no owner, the last isn't available (see *Completeness contract*). This is a question on every run, because a remainder nobody was asked about is one you own.

Ask in **one or two structured passes** (group by topic; use the question tool where it fits). Don't drip questions one at a time. Push back on vague answers — "make it fast" → "what P95 latency is acceptable?". If the user says "you have enough, just go", proceed but **log every remaining assumption explicitly** in the plan's *Open Questions / Assumptions* section.

**Lead with what you proved.** Where a Phase 1 spike settled something, state the measured result instead of asking about it — "the export runs in 4.2s over 50k rows, so no background job" respects the owner's time and shows the question is closed. Where a spike came back inconclusive, or where it *contradicted* what the docs or the team believed, that's now one of your sharpest questions: put the evidence in front of the owner and ask how they want to proceed, since a false premise they still hold is exactly what will derail the plan.

#### Running the grill autonomously (`--auto`)

Under `--auto` you play both roles. Write the questions first, *then* answer them — in that order, and without letting the second half soften the first. The temptation is to only "ask" what you already know the answer to, which produces a comfortable transcript and finds nothing; the point of writing the interrogation before answering it is that the questions come from the topic list above, not from your existing plan.

1. **Draft the same question set you'd have sent the owner** — the full structured pass, edge cases and non-goals included. Don't trim it because you're the one answering.
2. **Answer each from the strongest source available**, and name which one you used: Phase 1 evidence (spike verdict, file:line anchor) → the repo's own conventions and how sibling features already decided this → the ecosystem/library default → your judgment. An answer sourced from the codebase is a finding; an answer sourced from judgment is a guess, and the plan should let a reader tell them apart at a glance.
3. **When you're down to judgment, take the reversible option.** Nobody is going to catch an over-broad reading before it ships, so choose the narrower scope, the safer default (deny over allow, flag-off over flag-on, additive over destructive), and write down the alternative you passed on so the owner can flip it cheaply. That preference is about *scope* — which features to build, which defaults to pick. It is not a license to leave the change half-applied: a migration that reached four of seven callers isn't the narrower option, it's the broken one, and it's the harder state to unwind. "Narrower" chooses between tickets, never between finished and unfinished — remainder still resolves to in-run or out-of-scope per *Completeness contract*.
4. **Mark each answer's confidence and blast radius.** What matters isn't how unsure you are, it's what breaks if you're wrong. Flag every low-confidence answer to a question whose other outcome would have changed the plan's *shape* — those are what a human reads first.
5. **Record the whole exchange in the plan** as a Q&A table in §8 (question / answer / source / confidence). This is the artifact that makes an unattended run auditable; without it the owner has to reverse-engineer your reasoning from the diff.
6. **Escalate the one-way doors instead of answering them** — per *What `--auto` does not grant*. Scope them out, build the rest, and put them at the top of the report.

### Phase 3 — Plan

Using the `planning` runner (default `self` — you write it inline; only delegate if the config says so), produce a **complete, robust plan** and save it to `docs/plans/<feature-slug>.md` (create the folder if missing; suffix `-YYYY-MM-DD` if a file with that slug already exists, to avoid clobbering).

The plan must be decomposition-ready — it's the contract every downstream agent works from. Include:

```markdown
# Plan — <Feature Name>
| Field | Value |
| --- | --- |
| Date | <YYYY-MM-DD> |
| Source | <task / PRD path / conversation> |
| Config | AGENTS_CONFIG.yml (<preset or custom>) |
| Flags | <active modifier flags, e.g. --auto --no-e2e, or "none"> |
| Gates | <"grilled + approved by owner", or "self-resolved under --auto"> |
| Branch | TBD — set in Phase 4 |
| Base SHA | TBD — set in Phase 4 |

## 1. Objective & success criteria
## 2. Context & constraints  (grounded findings from Phase 1, with file:line anchors;
   spike verdicts with what was measured and under which versions)
## 3. Approach & key decisions  (alternatives considered; why this one — mark which
   decisions rest on spike evidence vs. on reasoning)
## 4. Work breakdown — implementation tasks
   For each task: an ID, a one-line goal, the **exact files it owns** (disjoint from
   its wave-siblings), dependencies (which task/wave must land first), and acceptance.
## 5. Work breakdown — test tasks  (unit / integration / e2e; which impl task each covers)
   State explicitly whether e2e applies — and to which user flows — or why it doesn't
   (including "skipped via --no-e2e" when that flag is active).
   If it applies, record the run recipe from Phase 1: e2e command, how the app and its
   services start, seed data, and any credentials/environment prerequisites.
## 6. Execution waves  (which tasks run in parallel; the barrier between waves)
## 7. Blast radius & risks  (callers, sibling paths, migrations, rollback, feature flags)
## 8. Open questions / assumptions  (questions the owner left open, assumptions you
   are proceeding on; under --auto, the self-answered grill as a Q&A table —
   question / answer / source / confidence — plus any one-way decision scoped out
   for a human. Not a bin for remainder — that lives in §9)
## 9. Completeness ledger  (every run: every candidate follow-up, each marked
   *in this run* with the task ID that owns it, *out of scope* with why it's a
   different ticket, or *owner-deferred* with who decided it and where — the third
   is unavailable under --no-follow-ups, and under --auto since nobody is there
   to defer. A bare "deferred" is not a row)
```

The **work breakdown is the heart of the plan**: partition the feature into tasks whose file ownership does not overlap within a wave, and order the waves so cross-task dependencies are respected. This is what makes Phase 4/6 safely parallel.

Build the ledger (§9) *before* the breakdown and let it feed the breakdown, not the other way around — a remainder you notice while writing tasks tends to get written down; a remainder you enumerate first gets a task.

**Present the plan to the user and get explicit approval before writing any code.** Offer to adjust. This is the second and final hard gate — *unless `--auto` is active*, in which case self-approve and continue (see *Autonomous mode*).

### Phase 4 — Implement

**Baseline first, before any agent writes.** This is the first phase that touches code, so set up a clean, diffable starting point:
- **Branch.** If you're on the default branch (`main`/`master`) or the user hasn't named a target branch, create a feature branch from the plan slug (e.g. `implement/<feature-slug>`) and announce it. A multi-agent fan-out should never write directly to the default branch, and both the review diff and worktree isolation below assume a branch to work on.
- **Record the base.** Capture `git rev-parse HEAD` as `<base>` and note whether the tree was already dirty (`git status --porcelain`). Fill the `Branch` and `Base SHA` rows the plan template reserved for this (a metadata-only edit to an approved plan — not a scope change; leave everything else untouched). Phase 5's review and the final report diff against exactly this ref, so pre-existing edits aren't misattributed to the build.

For each wave in the plan, spawn one `general-purpose` sub-agent per task, **in a single turn**, using the `implementation` runner(s).

Give each agent a **self-contained brief**: the objective, the exact files it owns (and a firm instruction not to touch anything else), the relevant findings/anchors from the plan, the acceptance criteria, and the project conventions to follow (match surrounding code — naming, error handling, test idiom). The agent should return a summary of what it changed, any deviations, and any remainder it found outside its owned files.

Every brief carries the **completeness clause**: finish the task's scope with no `TODO`/`FIXME`/stub/`NotImplementedError` standing in for in-scope work, and report remainder found outside the owned files back to you instead of reaching across a boundary (which collides) or leaving a marker (which is a self-deferral). The "touch nothing else" rule *guarantees* agents will run into remainder they aren't allowed to fix — the clause is what keeps that from quietly becoming a `TODO`. What comes back, you schedule into the next wave, or into the ledger if it's genuinely out of scope (*Completeness contract*).

- **Validate the wave before spawning it.** Cross-check the file-ownership lists of the tasks you're about to launch together: if any two name the same file, it isn't a valid wave — re-partition or split it before spawning. This 30-second check is the cheapest place to catch a collision.
- **Respect wave barriers.** Wait for all agents in a wave to finish before starting the next wave, since later waves depend on earlier ones. Within a wave there are no dependencies, so they run fully concurrently.
- **distribute vs race.** Under `distribute`, each task goes to one runner (round-robin or by suitability — give the cheaper runner the mechanical tasks, the stronger one the subtle tasks). Under `race`, send the same task to every runner and pick the best result yourself.
- **Avoiding collisions.** The plan already partitions files by task, so same-wave agents shouldn't collide *on source files*. Two hazards remain:
  - **Shared tooling side effects.** File-disjointness isn't enough when a wave mixes runner types. An external CLI runner (`codex`/`shell`) and an in-tree `claude` sub-agent occupy the **same working tree** at once, and the CLI may rewrite shared surfaces the file partition never mentioned — formatters, `package-lock`/lockfiles, the git index, generated code. Whenever an external CLI runner shares a wave with any other runner, give it its own checkout (worktree isolation) or serialize it after the in-tree agents. This is also why `cross_host: true` belongs on read-only phases: on a writing phase it guarantees exactly this collision.
  - **Unavoidable shared files.** If two tasks must both edit a central file (e.g. a registry), either (a) sequence them into separate waves, or (b) run the colliding agents with `isolation: "worktree"`. Prefer clean partitioning — reach for worktrees only when partitioning is genuinely impossible.
  - **Merging worktrees.** Isolated agents commit on their own branch; afterward **you** merge them into the working branch one at a time (`git merge` per worktree) and resolve any conflicts yourself. Because merging is the step most likely to strand or clobber work, treat it as a last resort behind re-partitioning.
- **Checkpoint after each wave.** Do a quick sanity pass (build/typecheck if cheap), then commit the wave (`wave N: <summary>`). The plan plus these commits are your resume points: if a later wave, the review, or a test run fails, you pick up from the last green wave instead of restarting the build — never discard completed work on a downstream failure.

See *Spawning runners* below for the exact mechanics of Claude vs shell runners.

### Phase 5 — Code review

Spawn a `general-purpose` agent on the `code_review` runner to review the diff produced in Phase 4 — `git diff <base>...HEAD` using the `<base>` recorded at the start of Phase 4 (plus any still-uncommitted changes) — returning structured findings (category, severity, file, line, suggestion).

**Tests don't exist yet at this point** — they're written in Phase 6, right after. So the diff under review is production code *without* its tests by design. **Explicitly brief the review agent not to flag missing/absent test coverage as a finding** — that's pipeline sequencing, not a defect, and left unsaid every reviewer will raise it as a spurious must-fix. (Test *quality* is reviewed implicitly when Phase 6's tests land; the closed loop is Phase 7 running them.)

**Which rubric:** decide *before* spawning the agent by checking your own available-skills list (shown at the top of your context) — skill availability is session-scoped, not repo-scoped, so you can see it directly rather than trusting the sub-agent to.
- If a `code-review` skill is listed **and** the user/config hasn't asked for strict standalone behavior → instruct the agent to load and follow it.
- Otherwise (`/implement` is standalone by design) → hand the agent the built-in rubric below.

**A skill lives in your harness, not in an external CLI.** If the review runner resolved to `codex`/`shell`, that subprocess cannot load a `code-review` skill no matter what you tell it — it has no access to your skill list. Paste the rubric text into the brief instead of naming a skill the agent can't reach. Getting this wrong produces a review that silently falls back to the agent's own instincts while your report claims the skill's rubric was applied.

Either way, **require the agent to state in its report which rubric it actually used**, so you can confirm the intended path was taken rather than infer it.

> **Built-in review rubric (fallback):** walk every changed file and flag, with file:line evidence — **bugs** (logic errors, unhandled edge cases, error-handling gaps); **security** (tenant isolation, authorization, atomicity/TOCTOU, retry safety, multi-step flow completeness, orphaned state, secrets/input validation); **performance** (in-memory aggregation, sequential fan-out, duplicate scans); **consistency** (enum/validation drift, schema↔code column drift, duplicated business rules); **blast radius** (callers, sibling paths, retries, stale state, downstream systems); and **completeness** (call sites left on the old path, partial propagation of a shape change, reachable states with no handling, orphaned dead code, new `TODO`/`FIXME`/stub markers). Report problems only — no "looks good" findings — each with category, severity, file, line, and a concrete fix. Do **not** flag absent tests (Phase 6 adds them). Read-only: never edit code during review.

Before spawning the reviewer, run the cheap mechanical pre-check yourself: grep the diff for added `TODO|FIXME|XXX|HACK` and placeholder throws. Whichever rubric the reviewer uses, brief it on the completeness dimension explicitly (unmigrated call sites, partial propagation, reachable-but-unhandled states, orphaned dead code, deferral markers) — a `code-review` skill won't know this run's ledger.

Triage the findings yourself. Fold **must-fix** items (bugs, security, correctness) into a fix list for Phase 8 — and completeness findings are correctness: a caller left on the old path is a bug, not a nice-to-have. The one carve-out is remainder the ledger already records as *owner-deferred*; that's fine on a default run and a defect under `--no-follow-ups` (*Completeness contract*). Note genuine nice-to-haves for the user. Don't auto-apply — you decide what's in scope, then fix via agents in Phase 8.

### Phase 6 — Tests creation

Same mechanics as Phase 4, using the `tests_creation` runner(s) and the plan's **test work breakdown**. Partition test tasks by the module/file under test so agents don't collide. Each agent extends the project's existing test setup and fixtures (from Phase 1 findings) rather than inventing a parallel harness, and covers the acceptance criteria plus negative paths for its assigned area.

**Include e2e coverage whenever it's applicable — not as a bonus, but as part of "tested".** (Under `--no-e2e`, none of this section's e2e work happens — no e2e tests, no harness setup; rely on the plan's *skipped by flag* record instead of an applicability judgment.) Unit and integration tests validate pieces in isolation; a class of bugs only surfaces in the assembled system — broken wiring between layers, auth/session behavior, migrations meeting real data, a UI flow that dies on the second step. For those, an e2e test is often the *only* automated way to catch the bug before a user does. E2e applies when the feature has a user-visible flow or crosses a process boundary (UI→API→DB, service→service, CLI→filesystem) and the app can be run locally per Phase 1's runnability findings. It doesn't apply to pure library/helper changes fully exercised by unit tests — in that case the plan says so explicitly and moves on; "not applicable" is a recorded decision, never a silent omission.

When it applies: extend the project's existing e2e harness (Playwright, Cypress, Detox, supertest-against-a-live-server, whatever Phase 1 found) with tests for the feature's critical paths — the happy path plus the failure states a real user could plausibly hit. Keep them deterministic: proper readiness waits and seeded data, not sleeps and shared mutable state. If the repo has **no** e2e harness, don't invent heavyweight infrastructure unilaterally — raise it in the plan (Phase 3), and if approved, stand up the minimal ecosystem-standard harness scoped to the feature's flows.

### Phase 7 — Tests running

Spawn **one background agent** on the `tests_running` runner to run the suite (the project's test command — discover it in Phase 1) and report back: pass/fail counts, the failing tests, and the relevant output. Background is ideal here — you'll be notified when it finishes. If the command is unknown, ask the user once for it (and note it in the plan for next time).

**When the plan includes e2e, the agent runs the e2e suite too — entirely by itself.** "It needs a running app" is a setup step for the agent, not a reason to hand the run back to the human. The agent owns the whole lifecycle, following the run recipe recorded in the plan:
1. **Prepare** — install what's missing (e.g. `npx playwright install`), provision local services (db, queue), seed fixture data.
2. **Start** — launch the app and its dependencies as background processes and *wait for readiness* (poll the health endpoint or port; don't fire tests at a half-booted server).
3. **Run** — execute the e2e command headless; on failure, capture the artifacts that make failures diagnosable (screenshots, traces, server logs), not just the exit code.
4. **Tear down** — stop the processes it started, so a re-run begins clean.

Only when a step is *genuinely* impossible to automate — real payment gateways, physical devices, human 2FA, credentials the agent doesn't hold — does it stop short. Even then it doesn't abandon the run: it automates everything up to that point, runs the **maximal subset** that can pass without the blocked step, and reports exactly what remains as a precise manual runbook (commands, URLs, expected results) so the human's share is minutes of clicking, not detective work. A partially-automated e2e run with a clear handoff beats a skipped one every time.

### Phase 8 — Tests fixes (conditional)

If Phase 5 surfaced must-fix findings, or Phase 7 reported failures, spawn fix agents exactly like Phase 4 — independent, file-disjoint tasks on the `tests_fixes` runner, each scoped to one failure cluster or finding. Then **re-run Phase 7**. Loop until green or until you hit a wall you can't resolve without the user — at which point stop and report the remaining failures with evidence, rather than looping forever. Cap at a sensible number of rounds (say 3) before checking in.

For a failing **e2e** test, have the runner re-run it once before dispatching a fix agent — e2e is the flakiest layer, and the fix differs by diagnosis: a consistent failure means the product code (or the test's assumptions) is wrong; a pass-on-retry means the *test* is at fault, and the fix agent should repair the flake properly (readiness waits, deterministic seeds — not sleeps or retries baked into the test).

## Spawning runners

**`type: claude` on a `claude_code` host:** use the Agent tool. Set `subagent_type` (`Explore` for read-only investigation, `general-purpose` for implementation/tests/review), `model` to the configured alias (`opus|sonnet|haiku|fable`), and `run_in_background: false` when you need the result inline before the next wave (Phases 4/6), or leave it in the background for Phase 7. Launch all agents of one wave in a single message so they run concurrently.

**`type: claude` on any other host:** shell out — `claude -p --model <alias> --add-dir {CWD} --permission-mode <plan|acceptEdits> --output-format text`, brief on stdin. Use `plan` for read-only phases and `acceptEdits` for writing ones.

**`type: codex | cursor | gemini | kimi | grok`:** write the brief to a file under the scratchpad, then run the CLI's recipe from **`references/harnesses.md`** — read it rather than reconstructing a command from memory, because the six differ on every axis that matters. Two traps it exists to prevent:

- **Naming a file in argv doesn't make a CLI read it.** Only `codex` and `claude` take the brief on stdin; the rest want the text as a positional argument. Passing a path to those sends the agent the literal string `/path/to/brief.md` — a failure that reads as the model ignoring its instructions rather than as a bug.
- **Only `codex` (`-C`) and `cursor` (`--workspace`) have a working-directory flag.** For `gemini`, `kimi`, and `grok`, set the process cwd yourself; there is no `--cd` to invent.

Permission level always follows the phase — the harness's read-only flag on `investigate`/`code_review`, its auto-approve flag on the writing phases. **`grok` is the exception with no read-only flag at all**; if it's routed to a read-only phase, put the constraint in the brief as forcefully as you can and tell the user the guarantee is weaker there.

**`type: shell`:** substitute the config's `command` template — `{PROMPT}` / `{TASK_FILE}` / `{CWD}` / `{OUTPUT_FILE}` — and pipe `stdin:`'s file in if the binding sets one.

For every external CLI runner, use `run_in_background: true` on long runs and collect the output when it completes. **Before the first such call in a phase, verify the binary exists** (`command -v <bin>` — note it's `cursor-agent`, not `cursor`). If it's missing, fall back per below and tell the user. If a command fails on *argument parsing*, the CLI has moved past the recipe — check its `--help`, adapt, and tell the user the built-in recipe is stale rather than silently retreating to another model.

### Writing a delegated brief

A sub-agent can't pause to ask you questions — its first (and only) instruction has to carry everything it needs. Brief quality is the single biggest lever on multi-agent results: vague briefs cause overlapping work and rework. Every brief you send — investigation, implementation, tests, fixes — nails four things:

- **Objective** — the one outcome this agent owns, in a sentence.
- **Output format** — exactly what to return, and keep it uniform across siblings so you can consume them together (e.g. "a findings brief with file:line anchors"; "a summary of files changed + any deviations"; "review findings as category / severity / file / line / fix").
- **Tools & sources** — where to look and what to use (specific files/dirs, `git log`, web for library X), so the agent doesn't rediscover the map from scratch.
- **Boundaries** — the exact files this agent owns, plus a firm "touch nothing else — that's another agent's job." Explicit boundaries are what stop parallel agents from colliding or duplicating each other's work.

Example (implementation task): *"**Objective:** add a `TransactionHistory` class. **Output:** a summary of what you changed + any deviations. **Tools/sources:** create `wallet/history.py`; mirror the style of `wallet/account.py:1-40`; no new deps. **Boundaries:** you own `wallet/history.py` only — do not edit `account.py`, the tests, or config; a later task wires it in."*

Example (spike task): *"**Objective:** answer one question — can `pdf-lib@1.17` flatten AcroForm fields on Node 18, or do we need a native binding? **Output:** verdict (yes / no / inconclusive), the exact command and its output that proves it, the versions you tested, and the path to what you built. **Tools/sources:** build a minimal repro in `<scratchpad>/spikes/pdf-flatten/` with its own `package.json` and install there; read `fixtures/sample-form.pdf` from the repo. **Boundaries:** write nothing outside that directory — do not add deps to the repo's `package.json` and do not modify any tracked file. This is throwaway code: I want the finding, not an implementation, so stop as soon as the question is answered and report 'inconclusive' rather than grinding if it isn't."*

### Runner resolution & fallback

Resolve a phase in three steps: look up its `use:` role(s) in `models:`; take the binding for the **detected host**, else the role's `any:` binding; if neither exists, use `defaults.fallback` (itself a role name, resolved the same way). All fallbacks route through `defaults.fallback` — never a hardcoded alias — so a user who sets it gets that honored.

- An external CLI runner whose binary isn't installed → that binding's `unavailable_fallback`, else `defaults.fallback`.
- A `claude` runner with an unrecognized model alias → `defaults.fallback`, warn.
- A role named in `use:` that isn't defined in `models:` → `defaults.fallback`, warn.
- `type: self` on a phase other than `planning` → treat as a `defaults.fallback` runner and warn (only planning/interaction can be done inline).
- Missing phase entry entirely → use the `balanced` preset's value for that phase.
- `strategy: race` with one resolved runner → a normal single run; nothing to race.

**Announce every substitution.** A silent downgrade is the worst failure mode here: the run completes, looks fine, and is quietly worse than what the user configured.

**A model failing for any *other* reason is not a fallback trigger.** A bad model slug, expired auth, or exhausted quota should surface as the error it is — the fix belongs to the user, and quietly rerouting to a different model hides the one piece of information they need.

## Reporting back

When the loop completes, give the user a tight wrap-up:
- **Plan:** `docs/plans/<slug>.md`.
- **Gates:** whether the grill and plan approval went through the owner, or were self-resolved under `--auto`. If autonomous, lead with this and link the plan's §8 Q&A table, plus anything you scoped out as a one-way decision — an absent owner's first question is "what did you decide for me?", and it should be answered before they have to ask.
- **Implemented:** the waves/tasks that ran and which runner did each.
- **Review verdict:** counts by severity + must-fixes addressed.
- **Tests:** final pass/fail with the command used, split by layer (unit/integration vs e2e). If e2e was skipped — as not applicable or via `--no-e2e` — say so and why; if any e2e step couldn't be automated, include the manual runbook for the remainder.
- **Open items:** the completeness ledger's outcome — swept in, ruled out of scope (and why), owner-deferred (and by whom, pointing at the grill answer). "Deferred by the run" is not a category: a remainder with no owner decision behind it is a defect to fix before reporting, not a bullet to list. Then the assumptions logged (calling out those left unverified because `--no-spikes` disabled the experiment) and any remaining failures you couldn't resolve. Under `--no-follow-ups` the owner-deferred list is empty by construction; anything still open needs a reason, since the flag's whole promise is that there isn't one.
- **Next step:** e.g. "review `docs/plans/<slug>.md`", or "run `/code-review` on the branch before pushing".

## Adapting to reality

These eight phases are the backbone, not a straitjacket. A tiny change may collapse investigation to a single agent and the grill to two questions. A research-heavy feature may loop investigation → grill twice before planning. If the user says "skip tests" or "no need to review", honor it and note it. The value is in the *orchestration discipline* — grounded investigation, resolved unknowns, a durable plan, collision-free parallel execution, and a closed test loop — not in rigidly performing all eight steps regardless of the task.

The one place to hold the line is the pair of human gates, because they're the only part of that discipline you can't restore later. Scaling the grill *down* to match a small change is right — one question instead of twelve. Dropping it to zero is a different move, and it's the one that quietly turns a delivery into a guess. If nobody is there to answer, that's what `--auto` is for, and even then the questions still get written down.
