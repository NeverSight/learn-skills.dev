---
name: afk-fleet
description: >-
  Run an unattended, standing fleet that autonomously implements a repo's ready GitHub-issue backlog —
  dispatching worktree-isolated workers, gating each on CI, and auto-merging green PRs until stopped.
  Use when the user wants to go AFK on the issues ("launch workers to do the issues", "run the fleet",
  orchestrate agents against GitHub issues with orca), or asks for one of its modes: --plan (dry-run),
  --tick (single pass), --takeover (inherit a dead fleet's claims). Another skill can invoke it to
  staff an already-decomposed backlog. NOT for decomposing a PRD/epic into issues, implementing a
  single named issue by hand, or reviewing a PR.
---

# afk-fleet

An **unattended fleet** that implements a decomposed GitHub-issue backlog by itself, and keeps
running for days **without any session's context growing without bound**. Three roles, each
context-bounded:

| Role | What it is | Lifetime |
|---|---|---|
| **launcher** | The interactive session you invoke `/afk-fleet` in. It authorizes once, then loops: spawn a tick → ingest a one-line summary → pace → repeat. | Long-lived, but only accumulates ~one compact summary per tick (auto-compaction keeps it flat). |
| **tick** | A **fresh-context [Agent] subagent** that does exactly **one reconciliation pass** against GitHub, then returns a compact structured summary and dies. | Short. Its bulky context is discarded on return. |
| **worker** | A fire-and-forget autonomous coding agent (Claude Code or qoderclicn — the run's **runtime**), one per issue: orca creates its worktree + branch, then starts it with the run's **worker launch command** so it runs on the same runtime as the launcher. Communicates only through GitHub (its PR, and issue comments). | Independent of the coordinator — never read by it. |

**This skill only *consumes* a backlog.** It does not decompose a PRD/epic into issues — that is
upstream work, and epics are explicitly excluded from dispatch. Assume the issues already exist,
worker-sized, labelled, and dependency-ordered.

## Why it runs forever (bounded by construction)

Permanent runtime is achieved by a **succession of disposable ticks**, not by one long-lived
coordinator staying disciplined. No coordinator context is ever alive long enough to fill up:

- Each **tick is a fresh subagent context**, dropped on return — the reset is structural, not a
  hoped-for compaction.
- The **launcher** does no coordination itself; it only ingests a compact per-tick summary, so its
  own growth is a tiny constant per cycle (and auto-compaction is the safety net).
- **A cycle whose observable state is unchanged spawns no tick at all** — the launcher's
  `afk cycle` gate (pure code, zero LLM tokens) proves the no-op before any LLM context is
  created, and a forced full tick every `force_tick_after_skips` cycles backstops what a state hash
  can't see (ADR-0007). Idle days cost tool calls, not contexts.
- **All durable state lives in GitHub**, so any fresh tick reconstructs the exact working set:
  `afk-claim/<n>` ref = claim (owned by a **fleet instance**) · PR (`Closes #n`) = result · an
  `afk:verdict` marker comment = a worker's machine-readable reason for opening **no** PR
  (already-satisfied / blocked / giving-up) · `afk-attempt/<n>` label = retry count ·
  `afk-heartbeat/<id>` ref = owner liveness. Nothing is remembered between ticks. (The human-facing **status board** comment is a
  *derived projection* of this state onto the issue surface, re-rendered each tick — never itself a
  source of truth, and never read back by a tick.)

## Modes

- `/afk-fleet` — **launcher** (default): bootstrap, then loop spawning ticks. The main entry.
- `/afk-fleet --plan` — **dry-run**: a **tick short-circuited before the Act phase**. It does the full
  rebuild (frontier + in-flight + stale classification), prints the dispatch plan, and exits —
  merges/dispatches/reclaims **nothing**, needs no authorization. Same rebuild code path as `--tick`,
  so the plan can't drift from what a live tick would do (ADR-0002).
- `/afk-fleet --tick` — **one reconciliation pass** and exit with a summary. This is what the
  launcher spawns each cycle (and what you'd run headless). It auto-merges only under the run
  authorization its launcher injects; invoked cold without it, it dispatches but calls no
  `afk merge`.
- `/afk-fleet --takeover` — a **launcher bootstrap variant** for when a fleet hard-stopped (quota) and
  you will not wait ~75 min for its lease to lapse: the *full* bootstrap, then the opening working set
  is seeded from a dead peer's claims instead of the frontier alone. Thereafter an ordinary standing
  fleet. See [Takeover mode](#takeover-mode---takeover).

## Launcher (default mode)

### Bootstrap (once, with the human present)

1. **Load config** — `afk config --file <target repo>/docs/agents/afk-fleet.md` parses + validates
   the file against the one schema (unknown key or wrong shape → **error, with you present — fix the
   file, don't guess**) and returns the **canonical config JSON**: every key present, defaults
   filled (ADR-0009). That JSON is what the launcher holds and injects into every tick — nothing
   downstream re-parses YAML or re-applies defaults. Missing file → offer to create it from the
   template ([references/config-template.md](references/config-template.md)) and stop; never run on
   guessed settings.
2. **Establish this fleet instance** — mint a short unique **instance id** (this launcher run's
   identity, held only in the launcher and injected into every tick, exactly like the authorization
   below). Then `afk probe --repo <repo> --config '<config>'`, which answers two compatibility questions
   and returns the run's config — **hold its `config` from here on, in place of step 1's**:
   - **Claim namespace** — the returned `config` carries the `claim_namespace` that actually works, so
     every later call inherits it through `--config` with nothing extra to pass. If it reports
     `"blocked": true` (an org ruleset forbids `refs/afk/*`; `detail` is the server's rejection), that
     namespace is the `refs/heads` fallback: **warn** that claim refs are then ordinary branches that
     may trigger `on: push` CI. See
     [Cooperative multi-fleet](references/cooperative-multi-fleet.md). An `{"error": …}` here means the
     remote could not be pushed to at all (auth, network) — fix that; it is not a namespace question.
   - **Branch protection** (only when `gate.ci: local`) — `protection.verdict == "error"` means
     `merge.target` **requires status checks**, so `gh pr merge` would be rejected however green the
     local gate is: **stop here, with the human present** — drop the required checks on that branch or
     switch to `gate.ci: required`. (`gh pr merge --admin` is not an option: it bypasses human review
     too.) A `"warn"` verdict (the read was inconclusive — no admin rights) is reported and continues.
3. **Settle the worker launch command** — `afk worker-command`. The tool first detects the
   **runtime** (ADR-0014): `QODERCN_CLI=1` in the environment → `qoderclicn` (always stock — no
   custom provider, no wrapping — returns its default and never asks); otherwise → `claude`, and
   the existing provider-parity flow applies. Workers start in a *fresh login shell*
   that inherits none of this session's environment, so a Claude launcher running on a custom provider
   (`ckimi`, `csk`, a direnv, a wrapper script) would otherwise dispatch workers that silently fall
   back to stock Anthropic and stay there for days (ADR-0010). For the Claude runtime, the tool reports:
   - `"status": "stock"` — no `ANTHROPIC_BASE_URL`; take its `command` and **ask nothing**.
   - `"status": "ask"` — a custom provider. Show the `base_url` and the `candidates` it found (the
     login shell's Claude-starting aliases, `wraps_env: true` marking the ones that carry a provider),
     ask *"which command should workers start with?"*, then **verify the answer**:
     `afk worker-command --check "<their answer>"`. `unresolved` → say what didn't resolve and re-ask
     (an unresolvable command starts no worker at all: the claim goes PR-less into the retry ladder
     and escalates, on a typo). `confirmed` with `"yolo": false` → warn that it carries no unattended
     flag, so a worker will park on a permission prompt — indistinguishable to the fleet from one that
     finished. `"yolo": null` just means the resolution couldn't show it.

   Hold the resulting `command` **verbatim** and inject it into every tick. It is **opaque** — never
   parse it, never compose one yourself, never append flags to it (appending to an alias that expands
   to a subshell isn't even valid syntax). This is what keeps every credential inside the wrapper the
   human already trusts: the fleet copies no environment, writes no file, and puts no key on any
   command line.
4. **Preview** — spawn a **plan tick** (a `--tick` in plan mode) as an [Agent] subagent and show the
   dispatch plan it returns (which issues, order, concurrency, gate steps, merge target). The frontier
   is computed **inside the subagent, never in the launcher's own context**; the launcher only ingests
   the returned plan (ADR-0002).
5. **Authorize (the one gate)** — state plainly: *"I will push worker branches and **auto-merge**
   green PRs to `<target>` in `<repo>` unattended — this overrides the standing 'never push without
   asking' rule, for this repo, for this run. Confirm?"* Get an explicit yes. This authorization is
   **for the whole run**, held only in the launcher (never a config key); every tick inherits it via
   its spawn prompt, and it dies when you stop the launcher.

The instance id, the run authorization, and the worker launch command are the run's **three
launcher-held facts**: settled once with you present, carried in every tick's spawn prompt, never
written to a file, gone when the launcher stops.

### Takeover mode (`--takeover`)

For when a fleet **hard-stopped** — its provider quota ran out, its process was killed — and you are
standing right there. The lease will hand its claims to a peer, but only after `claim_lease_ttl`
(~75 min), because a heartbeat is the only *machine-visible* line between "dead" and "alive but slow".
The present human is the oracle that knows *now*; the dying fleet cannot help, since a hard stop runs no
code at all (no drain, no release) — [ADR-0011](../../docs/adr/0011-takeover-and-progress-preservation.md).

Run the **full** [Bootstrap](#bootstrap-once-with-the-human-present) above — config, a *new* instance id,
the worker launch command, the one push+auto-merge authorization — so this is a real fleet instance. Only
the opening working set differs:

1. **List what GitHub still remembers.** The dead launcher forgot its own id; the claim markers
   (`instance=<id> host=<host>`) and heartbeat refs did not:
   ```bash
   <skill>/scripts/afk.py takeover --list --repo <repo> --instance <my instance id> --config '<config json>'
   ```
   Show the human each instance's id, host, claim count and heartbeat age, and ask which to take. Rows
   are flagged so the wrong answer is visible: `fresh: true` (looks alive), `claim_count: 0` (drained
   cleanly — nothing to take), `is_me: true` (this run).
2. **Force-take the selection:**
   ```bash
   <skill>/scripts/afk.py takeover --from <dead id> --instance <my instance id> --repo <repo> --config '<config json>'
   ```
   The *same* atomic `--force-with-lease` push a stale reclaim uses, only skipping the staleness gate —
   so a fleet that is not actually dead still wins the race and the result reports it under `lost`.
   On `"action": "confirm"` — the target's heartbeat is still fresh — relay the warning **verbatim**, get an
   explicit yes, then re-run with `--yes`; on `"error"`/`"none"`, show it and continue as an ordinary
   launcher run.
3. **Then it is an ordinary standing fleet.** Enter the [Loop](#loop) unchanged: the first tick sees the
   taken claims as `mine` and recovers each by
   [continuation](references/recovery.md) — tier 1 when the
   dead fleet ran on *this* box, since its worktrees are still here — **and** works the frontier up to
   `concurrency`, until you stop it.

A takeover **is not a retry** (it never reads or increments `afk-attempt/<n>`) and **does not shorten the
lease** — the unattended safety net stays exactly as wide; this is only the human-gated fast path across
it. Because continuation makes each take start further along, repeatedly taking one claim converges
rather than loops.

### Loop

Repeat until you stop it. The launcher's whole inter-cycle memory is **one opaque value** — the
`state` the last `afk cycle` returned. Hand it back verbatim; never read into it, never do arithmetic
on it (ADR-0017). Every counter the loop needs — the last fingerprint, the skip streak, the empty
streak, what is in flight — lives in there, maintained by code.

1. **Open the cycle:**
   ```bash
   <skill>/scripts/afk.py cycle --repo <repo> --instance <id> --config '<config json>' [--state '<state json>']
   ```
   (No `--state` on the very first cycle.) It gathers what a tick's Rebuild would observe
   (issues+labels, PRs+checks, claim refs) **inside the tool** — the raw JSON never enters the
   launcher — and returns `{action, reason, state}`:
   - `"action": "skip"` (nothing observable moved) → spawn nothing. A skipped cycle owes two things and
     the result already carries both: the lease was refreshed **inside this call** if the fleet holds
     claims (`heartbeat`), so a skipped cycle can never lapse a lease; and `sleep_seconds` is the pace.
     Keep `state` and go to step 4.
   - `"action": "tick"` (`first` / `changed` / `forced` / `gate_off`) → continue.
2. **Spawn a tick** — call the [Agent] tool (fresh context) to run one reconciliation pass, passing
   only `{repo, config, authorized: true, instance_id, worker_command}`. Constrain its return with a schema:
   `{merged:[…], escalated:[…], dispatched:[…], reclaimed:[…], in_flight:N, frontier_remaining:N, note}`.
   `in_flight` (claims the fleet still holds) and `frontier_remaining` (dispatchable issues it did not
   take) are **integers and mandatory** — the next step refuses a summary without them rather than
   pace a fleet holding claims as if it held none.
3. **Close the cycle** — hand the summary back, untouched:
   ```bash
   <skill>/scripts/afk.py cycle --repo <repo> --instance <id> --config '<config json>' \
        --state '<state json>' --summary '<the tick's summary json>'
   ```
   → `{state, sleep_seconds}`. Keep `state`; surface a short progress line to the user from the summary,
   then discard the summary.
4. **Sleep `sleep_seconds`** (`ScheduleWakeup`). The number already encodes the pacing rules — you
   apply none yourself: `busy_interval` (~1–2 min) while the last tick did anything or anything is in
   flight, so green PRs merge promptly; `idle_interval` (~25 min) once `idle_ticks_before_sleep`
   consecutive cycles were **empty** (a tick that did nothing, or a skip, with nothing in flight and
   nothing left on the frontier); and never past `claim_lease_ttl`/2 while the fleet holds any claim.
5. **Stop** on the user's word: run one final **drain** tick that `afk release <n>`s claims with no PR
   yet and retains those with an open PR (see [Cooperative multi-fleet](references/cooperative-multi-fleet.md)), then
   spawn no more ticks. In-flight workers finish on their own; their PRs are inherited and merged by a
   peer (or a later run) once the lease expires; escalated issues stay labelled for the human.

The launcher never dispatches, merges, or reads a worker itself, never computes the frontier in its own
context, and never reads the tick's files (the `afk.py`/`afk_decide.py` source, `worker-prompt.md`) — it
reads only the repo config, calls `afk` subcommands, and spawns ticks. All coordination happens inside a
tick; even the bootstrap preview is a plan-tick subagent. This keeps the launcher thin *by construction*
(ADR-0002), not by later compaction.

## Tools (`scripts/afk.py`) — the deterministic muscle

Every **deterministic** step the skill runs is a subcommand of `afk.py`, each printing one JSON object:
the tick orchestrates and judges, but calls the tool for the fixed mechanics rather than re-deriving
git/gh/orca incantations from prose each pass (ADR-0004). That holds for the **Act half** too: starting
a worker, landing a PR, failing, escalating and closing a claim are each **one call that performs the
whole ordered sequence** and returns an `outcome` wherever your judgment is needed (ADR-0017). A tick
therefore runs **no raw `git`, `gh pr merge`, `gh issue edit` or `orca worktree`/`terminal create`** of
its own — the only orca command it types is the liveness probe. The full interface table — every
subcommand with its arguments and return shape — is disclosed in
[references/tools.md](references/tools.md); read it when you need a signature not already shown inline
at its call site.

**One calling convention.** Every subcommand **requires** the run's `--config '<config json>'` (all but
the two bootstrap ones that run before a config exists — `afk config`, `afk worker-command`), and every
one that touches GitHub takes `--repo <repo>`. **Pass both on every call** — the config is what carries
the claim namespace, the lease, the labels and the gate mode. A call without `--config` is refused
(exit 3); it never runs on defaults. The inline examples below abbreviate both away
(`afk release <n>`) only to stay readable.

**The tool is one executable word.** `<skill>/scripts/afk.py` is executable — call it by its path, with
no interpreter in front. If you shorten it, hold only the **path** in a variable or define a shell
function (`afk() { <skill>/scripts/afk.py "$@"; }`); never put a multi-word command (`AFK="python3 …"`)
in a variable — zsh does not word-split it, so every `$AFK …` in the batch fails with exit 127 while
the commands chained after it still run.

**Exit 3 is never an outcome.** A subcommand that could not do its job prints `{"error": …}` and exits
3. That is an operational failure (auth, network, a rejected push, an unreadable remote, a claim that
could not be deleted, a bad command line) — stop and report it in the tick summary's `note`; do not
read it as "nothing to do". The converse holds too: an exit-0 result is always a real answer — an
empty `mine` means you hold nothing, `"released": true` means the claim is gone.

## A tick (`--tick`) — one reconciliation pass

A tick is stateless: it rebuilds from GitHub, acts, summarizes, and exits. It never waits for the
workers it dispatches. In `--plan` mode it stops after step 1 (**Rebuild**) and returns the plan
instead of acting — same rebuild, zero side effects (this is what the launcher's bootstrap preview
spawns).

1. **Rebuild the working set from GitHub** (never from memory) — **one read-only call** (ADR-0008):
   ```bash
   <skill>/scripts/afk.py rebuild --repo <repo> --instance <id> --config '<config json>'
   ```
   It gathers issues + PRs + claim/heartbeat refs once (the same gatherer the launcher's cycle
   gate reads through — the raw 200-issue JSON lives and dies inside the tool) and returns the whole
   working set: `{frontier: {dispatch, excluded}, mine: [{number, status, board_phase, pr, checks,
   attempt}…], peer_live, stale: [{number, sha}…], free_slots, fingerprint, now}`. Then act on it:
   - **Frontier** — `frontier.dispatch` is the dispatchable set (`open` + `ready_label` + no
     `epic_labels` + **unclaimed** + **no open linked PR** + zero open `blocked_by`) — the published
     contract; `--plan` and live agree because both are this one code path. `free_slots` is how many
     of them `concurrency` leaves room for.
   - **In-flight** — each of **`mine`** arrives subclassified, and its `status` names what you do
     next: *awaiting_merge* → `afk merge` (see [Merge](#merge-serialized)); *awaiting_ci* → leave;
     *failure* → `afk fail` (see [Failure handling](#failure-handling--bounded-retry--escalate-never-silently-drop));
     *closed* → the issue is already closed but its claim outlived it (a merge or close that died
     before releasing): `afk release <n>`, nothing else; *no_pr* → see below. (In `gate.ci: local` only
     *awaiting_merge*, *closed* and *no_pr* occur — no checks are read, and the gate runs inside
     `afk merge` instead; ADR-0012.) For *no_pr*, **never decide from terminal chrome alone.** A worker
     that ran to completion, concluded there was no PR to open, posted its reason, and went idle looks
     *identical* to one still coding — both are "a connected terminal with a title". Run the orca
     **liveness** probe (bounded, never a transcript read) for the one thing code cannot see — is the
     terminal `busy`, `idle`, or is there `none` — then make **one call**:
     ```bash
     <skill>/scripts/afk.py no-pr --issue <n> --terminal <busy|idle|none> \
          [--terminal-idle-seconds <s>] --repo <repo> --config '<config json>'
     ```
     (`--terminal-idle-seconds` is how long the terminal has shown no activity, if the probe says.)
     The tool gathers the rest itself — the issue's worktree on this machine (asked of orca) and its
     git progress, the worker's `afk:verdict` marker, the state of every issue that marker says it is
     blocked by — computes how long the worker has been quiet, and returns `{outcome, action,
     idle_seconds, open_blockers, worktree, progress, worker_verdict, nudged_at}`. `outcome` / `action` are the
     tool's conclusion; `worker_verdict` is only what the worker *declared* in its marker (one of the
     inputs). Act on `action` — each is one call:
       - **coding** / `leave` (terminal busy, or a sign of life within `worker_idle_grace_seconds`) →
         still implementing, **leave it**. Commits ahead or a dirty tree are *standing* facts, never
         signs of life (ADR-0013) — they do not keep a claim here;
       - **idle_done** / `close_release` (verdict `already-satisfied`, **no** changes on the branch)
         → **verify the empty diff vs base** in the `worktree` it returned, then
         `afk close --issue <n> --instance <id>`;
       - **idle_blocked** / `redispatch` (verdict `blocked`, every named blocker now closed) →
         `afk dispatch --issue <n>` again (the claim is kept; not a retry);
       - **idle_blocked** / `escalate` (a blocker in `open_blockers` is still open, or the verdict
         named none) → **escalate the DAG gap**:
         `afk escalate --issue <n> --instance <id> --reason "<the unmet dependency>"`;
       - **idle_stalled** / `nudge` (idle past grace with **no verdict at all**, not yet nudged) →
         the worker stopped without an outcome — usually it is waiting on a question nobody will
         answer. `afk nudge --issue <n> --instance <id>` tells it to carry on, **once**: no attempt is
         spent, nothing is discarded, and the nudge buys it one more grace period (ADR-0018);
       - **idle_failed** / `next_attempt` (verdict `giving-up`, an `already-satisfied` refuted by work
         on the branch, or still **no verdict** a grace period after the nudge) →
         `afk fail --issue <n> --reason "<why>"` (retry → escalate); after an unanswered nudge
         `afk fail` appends the worker's last screen to the reason itself;
       - **dead** / `orphan` (no live worker/terminal at all) → **orphaned claim**: `afk dispatch
         --issue <n>` recovers it by **continuation** — it resumes from the worktree still here, else
         from the pushed branch, and starts from base only when nothing survived (see
         [Recovery by continuation](references/recovery.md)). Or `afk release <n>` if the issue should
         go back to the frontier instead.
     The liveness probe and the empty-diff verification stay judgment; `no-pr` is a separate call from
     `rebuild` because it asks *this machine* about a worktree, and `rebuild` stays machine-independent
     (ADR-0008).
   - **Stale peer claims** — **`stale`** (a peer owns it and its `afk-heartbeat/<id>` is expired past
     `claim_lease_ttl`) is the only foreign claim I may take *unattended*: `afk reclaim <n> --instance
     <id> --expect-sha <the sha rebuild reported>` (atomic — fails if it moved), then `afk dispatch
     --issue <n>` — a reclaimed claim's worker is dead by definition, so it is recovered by
     **continuation** like any dead claim of mine (the worktree is reused when the dead peer ran on
     *this* box). **`peer_live`** is left strictly alone. The human-gated, lease-skipping sibling of
     this reclaim is [`--takeover`](#takeover-mode---takeover).
2. **Act**, in this order — every step is one `afk` call that performs its whole sequence:
   - **Merge** each *awaiting_merge* claim, one at a time: `afk merge --issue <n> --instance <id>`
     (see [Merge](#merge-serialized) for its outcomes). A `merged` outcome has already upserted the
     status board, released the claim and removed the worktree.
   - **Fail / escalate** what the rebuild and the merges turned up (see
     [Failure handling](#failure-handling--bounded-retry--escalate-never-silently-drop)).
   - **Dispatch** to fill the free slots (`free_slots`, plus one for every claim this tick settled),
     taking `frontier.dispatch` in order:
     ```bash
     <skill>/scripts/afk.py dispatch --issue <n> --instance <id> --worker-command '<worker_command>' \
          --repo <repo> --config '<config json>'
     ```
     One call claims the issue, has **orca** create the worktree + branch at the remote's current base
     tip ([ADR-0005](../../docs/adr/0005-orca-owns-the-worktree.md)), starts the agent with the run's
     **worker launch command**, waits for it, fills [the worker prompt](references/worker-prompt.md)
     with the real branch + path, delivers it, and upserts the status board. Read the result:
       - `{"started": true, "claim": "won"|"held", tier, action, prompt, worktree, branch, terminal}` →
         a worker is running. **Do not wait for it.**
       - `{"started": false, "claim": "lost", "owner": …}` → a peer won the race; skip the issue.
       - `{"error": …}` → **not** a lost race: something failed (orca, the push, a worker that never
         became ready). Stop dispatching and report it in `note`. If the claim was already taken it is
         still held, so the next tick finds a claim of mine with no worker and dispatches it again.

     Pass `--worker-command` **verbatim** — the opaque string settled at bootstrap step 3 (ADR-0010,
     ADR-0014); never compose or append to it. What the call guarantees, so you need not: the worker
     starts from the base the **remote** has now, never a stale local branch; its prompt carries the
     branch orca actually created (`<user>/…`); the prompt is delivered as a brief file plus a
     one-line pointer (a whole prompt typed at an agent lands as a paste it asks to have confirmed)
     and is **submitted** — typed but unsubmitted, a worker sits idle forever, indistinguishable from
     one that finished.
   - **Heartbeat** — `afk heartbeat --instance <id> --config <config>`; it refreshes only if due
     and only matters while I hold ≥1 claim. Cheap, stateless (it reads the old ts from the ref itself).
   - **Render progress** (if `progress_comment`) — for each `mine` row this tick did **not** settle or
     start, upsert the human-facing **status board** so a person reading the issue sees how far along
     it is (esp. the otherwise-invisible "claimed, coding, no PR yet" phase — the claim lives in the
     hidden `refs/afk/*` and the assignee is unused). `afk status <n> --phase <board_phase> --instance
     <id> [--pr <pr>] [--attempt <k>] --repo <repo>` renders a progress checklist and writes the one
     marker-tagged comment **only when it changed** (idempotent — re-entrant ticks and retries never
     spam). Neither value is yours to derive: pass the `board_phase` and the `attempt` that `rebuild`
     put on the claim's `mine` row. The **terminal** phases (merged, escalated, closed) and the first
     `claimed` are written by the transition that reaches them — `afk merge`, `afk escalate`, `afk
     close`, `afk dispatch` — before it releases the claim. The board is human-read only — no tick ever
     parses it back (ADR-0006).
3. **Return** the compact summary and **exit**. Count `in_flight` (claims still mine) and
   `frontier_remaining` (dispatchable issues not taken) as integers — the launcher's pacing reads them.
   Freshly-dispatched workers' PRs are picked up by a later tick.

## Cooperative multi-fleet

Several fleet instances — on several machines, even under one shared GitHub account — may work the
same repo at once: ownership lives in atomic git refs under the hidden `refs/afk/*` namespace,
liveness in a per-instance lease ([ADR-0003](../../docs/adr/0003-cooperative-multi-fleet-claims.md)).
The operative rules (claim before work, release on every terminal transition, reclaim only stale) are
in [Guardrails](#guardrails); the mechanism and the raw git each subcommand runs are disclosed in
[references/cooperative-multi-fleet.md](references/cooperative-multi-fleet.md) — read it when you need
to understand *how* a claim, heartbeat, or reclaim works under the hood. It also defines the
**phantom lock** failure a skipped claim-ref delete causes.

## Recovery by continuation (a dead claim is continued, never restarted)

A claim whose worker died — an **orphaned claim** of mine, a **stale claim** reclaimed from a dead
peer, or one inherited through a **takeover** — is recovered *from its durable progress*, never
re-dispatched from base while progress exists. `afk dispatch --issue <n>` does this on its own: it
selects the tier (1 reuse the worktree / 2 recreate at the branch tip / 3 start from base — nothing is
ever torn down on this path) and delivers the matching continue-or-fresh prompt. Your judgment is the
one thing it cannot supply — *is the recovered state sane to build on?* When that is in doubt, read
[references/recovery.md](references/recovery.md): `afk recovery --issue <n>` shows what would be
continued, and `--start fresh` on the dispatch discards it instead.
**The claim is kept** throughout; the `afk-attempt/<n>` counter is neither read nor incremented
(continuation answers *"did the worker die?"*, the retry ladder *"is the work failing?"*). This is
**not the retry path** — a red gate / adversarial refute / `giving-up` verdict starts *fresh*
by design (see
[Failure handling](#failure-handling--bounded-retry--escalate-never-silently-drop)).

## Completion gate

A PR may merge only when **all** configured gates are green. Which **machine gate** applies is
`gate.ci` ([ADR-0012](../../docs/adr/0012-local-completion-gate.md)): `required` (default) waits for
the PR's GitHub checks; `local` makes `gate.local_command` the gate, re-run at merge time, and never
reads checks. `afk merge` applies whichever is configured ([Merge](#merge-serialized)); the invariants
behind them — the local gate's two-run rule, the ephemeral CI sub-read, and the adversarial-verify
procedure when `gate.adversarial_verify` is on — are disclosed in
[references/completion-gate.md](references/completion-gate.md). Read it before running an adversarial
verify or switching a repo to `gate.ci: local`.

## Merge (serialized)

Within a tick, merges are **strictly serialized** — one `afk merge` at a time — so parallel workers
never corrupt the target branch:

```bash
<skill>/scripts/afk.py merge --issue <n> --instance <id> --repo <repo> --config '<config json>'
```

One call runs the whole sequence: **sync** the branch up to the latest `merge.target` (by **merging,
never rebasing** — ADR-0012) and push it → **re-confirm the gate** against that exact head → `gh pr
merge` **pinned to the gated head** (per `merge.strategy`) → status board → **release the claim** →
remove the worktree (if `worktree_cleanup`). It needs no worktree path from you: it finds the issue's
worktree through orca, and recreates one at the PR head when this machine has none (a `--takeover`
from another machine). It stops, with an `outcome`, wherever the next move is yours:

| `outcome` | What happened | What you do |
|---|---|---|
| `merged` | Landed; board upserted, claim released, worktree removed. | Count it in `merged`; the slot is free. |
| `conflict` | The sync conflicted. The merge is **left in progress** in `worktree`, `files` unmerged; nothing was pushed. | Your judgment: resolve in that worktree, **commit**, and re-run `afk merge` — or, if it is not yours to resolve, `afk fail --issue <n> --reason "<the conflict>"`. |
| `gate_red` | `local`: the merge-time gate was red, and its `gate.excerpt` is now a PR comment. `required`: the PR's checks are red. | `afk fail --issue <n> --reason "<the failure>"`. |
| `awaiting_ci` | `required`: checks are pending — or the sync just pushed a new head, so CI must speak about *that* head first. | Leave it; a later tick merges. |
| `no_checks` | `required`, and the PR has no checks at all — the progressive gate. | If you judge the issue's acceptance criteria met, re-run with `--allow-no-checks`; else `afk fail`. |
| `needs_verify` | `gate.adversarial_verify` is on, the machine gate is green, and `--verified` does not name `head`. | Run the [adversarial verify](references/completion-gate.md) against `head`. Passed → re-run with `--verified <head>`; refuted → `afk fail`. |

The invariant every path keeps: **what lands on the target was gated in the form it lands.** A sync
that moved the head invalidates checks and verifications of the old one, and gh refuses the merge if
the branch moved after the gate. An `{"error": …}` settles nothing — the claim is still yours.

The fleet's mandate **ends at a green merge to `merge.target`.** Deploying is a separate,
human-gated step — never done here.

## Failure handling — bounded retry → escalate, never silently drop

Per issue, on any of {gate red — a *failure* row's CI checks *or* a red merge-time gate —
adversarial refute, a **sync** conflict you could not resolve, a `no_pr` claim classified
**idle_failed** — a `giving-up` verdict, or a worker still idle with **no verdict at all** a grace
period after its one nudge}:

```bash
<skill>/scripts/afk.py fail --issue <n> --instance <id> --worker-command '<worker_command>' \
     --reason "<why it failed>" --repo <repo> --config '<config json>'
```

`--reason` is your one contribution: the failure, **re-read from where it already lives** — the PR's
CI checks, the merge-time gate excerpt on the PR, the verifier's review comment, the conflicted files —
never carried in context. The call does the rest and reports which way it went:

- `"action": "retry"` — under `retry` attempts (default 2). The attempt count lives as an
  **`afk-attempt/<n>` label** on the issue (not in tick memory) and `afk fail` is its one writer: it
  swaps the label up by one, **discards the failed attempt** (closes its PR, deletes its branch, removes
  its worktree — so the claim cannot loop on the same red PR) and starts a **fresh** worker from base
  under the same claim, handing it your reason. `worker` in the result says where it is.
- `"action": "escalate"` — the attempts are exhausted. In one fixed order: status board → relabel
  (add `escalate_label`, remove `ready_label` and the attempt label) → comment your reason (if
  `escalate_comment`) → release the claim. The PR and the worktree are left for the human.

An issue that should go to a human **without** consuming a retry — a DAG gap — takes the same ordered
transition directly: `afk escalate --issue <n> --instance <id> --reason "<…>"`. Never silently drop or
silently merge bad work.

**`no_pr` idle routing (not all of it is a failure).** Of the six `afk no-pr` outcomes (defined in
the tick's In-flight list), only **idle_failed** enters the retry ladder above. **idle_stalled** is
nudged first and costs no attempt. **idle_blocked** skips
retry accounting entirely — re-dispatched when its `blocked_by` issues resolve, escalated as a DAG gap
when they don't — and **idle_done** closes the issue after an empty-diff check; neither is a failure.

## Concurrency

`concurrency` (default 3) bounds parallel workers. Semantic ordering is the backlog's dependency DAG
(your responsibility when decomposing); textual conflicts between parallel PRs are caught by the
serialized sync-before-merge and routed through failure handling. Early machinery issues that all
touch shared root config are naturally throttled by the DAG — chain them with `blocked_by`.

## Guardrails

- **Authorize before any push or merge.** The launcher runs only on the bootstrap authorization, and a
  cold `--tick` auto-merges only with an injected run authorization — without one it dispatches but
  never calls `afk merge`.
- **Keep every credential inside the worker's own shell.** Push only to worker branches and the merge
  to `merge.target`; deploying, secrets, and every other remote stay out of scope. Carry no credential
  to a worker — no copied `ANTHROPIC_*` (or any) env, no env file, no token from a secret manager: the
  opaque **worker launch command** exists so the wrapper the human named does this itself (ADR-0010).
  Copying the launcher's env would also break the fleet outright — `ORCA_TERMINAL_HANDLE` and friends
  would make every worker report as the launcher's terminal, collapsing the liveness probe.
- **Dispatch worker-sized issues only.** Epics/PRDs stay upstream; if the frontier is all epics, report
  "nothing decomposed yet."
- **Read workers through GitHub, never their transcripts.** A worker's result is its PR (`Closes #n`);
  a not-going-to-PR outcome is its `afk:verdict` marker comment; blockers are issue comments. Liveness
  is a bounded probe that `afk no-pr` combines, for a `no_pr` claim, with the worktree's git progress
  and the worker's verdict marker (see In-flight — the probe alone is never a finished/coding
  verdict). A full transcript never enters a tick or the launcher; the one terminal read is
  `afk nudge` / `afk fail` taking the last screen of a worker that went silent, to say *where* it
  stopped — never its result (ADR-0018).
- **Claim before work; release on every terminal transition.** `afk dispatch` creates the
  `afk-claim/<n>` ref first — if the create is rejected, a peer owns it and nothing is started.
  `afk merge`, `afk escalate` and `afk close` each delete it as their last step; an orphan-release and a
  *closed* row are yours to `afk release`. A leaked ref is a phantom lock. Reconcile only your own claims, and take a peer's
  only when its heartbeat is expired (a **stale claim**) — the single exception is an explicit human
  [`--takeover`](#takeover-mode---takeover).
- **Preserve a dead worker's progress.** Recover a dead claim by **continuation** (a plain
  `afk dispatch`), and discard an attempt only where discarding is the point — `afk fail`'s retry, or
  an explicit `--start fresh`. Never run `orca worktree rm` yourself: on a worktree that still holds
  work it is the one unrecoverable act in the fleet.
- **Take a live lease only on a human's word.** `afk takeover --from` runs only on the human's
  explicit selection from `--list`, with `--yes` only after relaying the fresh-heartbeat warning and
  getting an explicit yes; unattended, the lease is the only path (never `--yes` to ease a tick).
- **Respect human reservation.** A human reserves an issue by removing `ready_label` (the fleet no
  longer reads the assignee); keep the tracker honest so a peer fleet or a human never double-takes.
- **Stay off the reserved namespaces.** The fleet manages the `afk-attempt/<n>` labels, the
  `refs/afk/*` ref namespace (the claim and heartbeat refs), the single status-board comment tagged
  `<!--afk:status-->`, and the worker-authored `<!--afk:verdict …-->` markers (which it parses) — leave
  them to the fleet, and reuse those prefixes / markers for nothing else.
