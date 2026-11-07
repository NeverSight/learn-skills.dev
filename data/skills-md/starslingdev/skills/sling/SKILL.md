---
name: sling
description: >-
  Diagnoses GitHub Actions failures and attributes CI time and cost using
  StarSling's `sling` CLI. Invoke this BEFORE using `gh` or fetching any logs
  whenever the user asks why a job or run failed, what made a run slow, about
  runner minutes or CI cost, asks to re-run or cancel a run, or pastes a
  GitHub Actions URL — `sling` returns server-classified failure causes and
  cost attribution that log-grepping misses; state changes route to `gh`. Not
  for repo-wide audits of workflow files (ci-score, ci-speedup, ci-secure),
  writing workflow YAML, or non-GitHub-Actions CI.
license: MIT
---

# sling CLI

`sling` is StarSling's agent-first CLI for GitHub Actions. It answers
questions about **live CI data** — one run, one job, one attempt, or an
account's runner-minutes — from StarSling's control plane, with structured
JSON on stdout and a stable exit-code table. **No `sling` command changes
GitHub or CI state**: it reads and analyzes. A few change only the user's
own machine — `login`/`logout` (the credential), `org switch` (the saved
default org) and `update` (the installed binary); the user runs `login`,
`logout` and `update`, never you; `org switch <slug>` is yours to run.

**This skill's job is picking the right tool per request.** Live question
about a run, a job, or spend → `sling`. Anything that *changes* CI state →
`gh`. A repo-wide audit of workflow *files* → hand off to the audit skill
that owns it and stop. Do not invent a `sling` subcommand for something
`sling` does not do; [the command
surface](references/command-surface.json) is the complete list.

Every fact in this skill's command reference was read off `sling` itself
(v0.1.124) rather than from documentation — see
[references/command-reference.md](references/command-reference.md) for the
verified per-command JSON shapes.

## Preflight: is `sling` installed and authenticated?

Do this once per session, before the first `sling` command.

1. **Is it on PATH?** `command -v sling`. If it is missing, `sling` is
   installed by a one-line installer published on the installation page at
   `https://docs.starsling.dev/sling-cli/installation` — point the user at
   that page and let them run it, rather than pasting an installer command
   from memory. It supports **Apple Silicon macOS and x64 glibc Linux
   only**; there is no Windows build, so on Windows say so plainly and use
   the `gh`-only path in step 6.

2. **Is the environment healthy?** `sling doctor --agent`. It emits
   `{"checks": [{"key", "ok", "detail", ...}]}` on stdout and **exits `10`
   when a real check fails** (`0` when healthy). The checks name the
   problem. Seven of the nine are actionable — `token`, `control_plane`,
   `clock_skew`, `git_remote`, `patch_tooling`, `version`, `org` — so act on
   the one that is `ok: false` instead of guessing (the other two,
   `auto_update` and `agent_skill`, are advisory only; see below) — and when SEVERAL are `ok: false`, act on
   `control_plane` first: an unreachable control plane fails `token` and `org`
   as dependents, and the `token` check still attaches `fix_command: "sling
   login"` — a wrong lead during an outage, since the device flow cannot reach
   the control plane either. Network first, never login. `"skipped": true` can
   also mean "not checked" for exactly this reason — read `detail`, not just
   the flag. A `version` check with `warn: true` is an upgrade
   notice, not a failure — its `fix_command` is `sling update` on a normal
   install, otherwise the installer one-liner (a shell pipeline) or nothing;
   either way surface it to the user rather than running it yourself.
   `version` reads `ok: false, skipped: true` when it could not
   compare at all (installer URL unreachable, served version unreadable) —
   that is "not checked", not "out of date".
   The `auto_update` and `agent_skill` rows are likewise advisory and can never make `doctor`
   unhealthy: a check counts as failing only when it is `ok: false` AND not
   `skipped`, and each row's only `ok: false` shape is also `skipped: true`.
   `auto_update` says whether this `sling` updates itself in the background.
   `agent_skill` says whether this skill is installed for a coding agent on
   the machine, and can read "not installed" while you are reading the skill,
   because it only looks in a fixed set of directories. Report either row
   with its detail and never run its `fix_command` yourself — installing and
   updating are the user's call
   (see [references/command-reference.md](references/command-reference.md)).

3. **Not authenticated** (`doctor`'s `token` check fails, or a command exits
   `4` **whose stderr does not name an org**): **ask the user to run `sling
   login` in their own terminal**, then wait for them to say it is done.
   Do not run it yourself, and never pass `--agent` to it.

   **Read the stderr before acting on exit `4`.** `You don't have access to
   org "<name>"` is a missing app installation, not a stale credential, and
   it belongs to step 5 rather than here. It ends `Run \`sling login\``
   anyway, because a generic decorator appends that to every auth-class
   error — so the code and the advice both point the wrong way. Signing in
   again succeeds and changes nothing, which reads to the user as a broken
   login rather than as the missing installation it is.

   Signing in needs a person at a browser: `sling login` prints a device
   code, opens a GitHub approval page, and blocks until someone approves it.
   Launched as a subprocess that is unworkable in both directions — the
   output arrives only once the command has already finished or timed out,
   so the code is never visible while it can still be used, and `--agent`
   would refuse the prompt outright with exit `2`. There is no automated
   path here, and pretending otherwise just hangs the session.

   The credential is saved per user at `~/.config/sling/credentials`, so
   once they have signed in, an agent running as them is authenticated with
   no further setup. Re-run `sling doctor --agent` to confirm, then carry
   on.

4. **Wrong org — you belong to several and have not picked one.** `doctor`'s
   `org` check naming multiple slugs, an exit `2` about org ambiguity, or an
   id that resolves to nothing but plausibly exists in another of your orgs:
   `sling org switch <slug>`, or pass `--org <slug>` on a single command that
   accepts it (see below).

   `--org` and `--repo <owner/name>` are per-command flags, accepted by most
   data commands but **not by `sling logs`**, which parses strictly and
   rejects both (`Unknown flag "--org"`); every rejection here is exit `2`. That is the command
   this routing table reaches for most, so fix a wrong org for a logs read by
   switching the default rather than by adding a flag to the call.
   **`sling time` rejects `--org` outright** — switch the default for it too.
   `runs list`, `jobs list`, `usage` and `top` take either flag but reject
   both together (`Use --org or --repo, not both.`) — keep `--repo`, which
   names its org, and drop `--org`. No command fills in `--repo` from the git
   remote: without it `runs list`, `usage` and `top` cover the whole org,
   `jobs list` needs `--run`, `--repo` or a window, and `sling time`'s repo
   view needs `--repo`. For "my" or "this repo" asks, pass `--repo` from the
   checkout's `origin`. It takes `owner/name` — a bare repo name is rejected.

   `doctor`'s `org` check also fails when you belong to **no** orgs, which
   looks similar and is not this. There is no slug to switch to — that is
   step 5.

5. **StarSling gate — the app is not installed anywhere you can see.**
   `sling` reports CI that the **StarSling GitHub App** collected, so a valid
   login sees nothing until the app is installed on a GitHub organization.
   Two shapes, one cause, one answer:

   - **An org exists and you cannot see it** — exit `4`, `You don't have
     access to org "<name>"`. **Rule out a typo first.** A slug that could
     never exist returns byte-identically, so this message alone does not
     establish that an org is real: `sling org switch <slug>` answers with
     `Unknown org "<slug>" — your orgs: …`, which both settles it and prints
     the list. Telling someone to install a GitHub App on an organization
     they mistyped is worse than saying nothing. The URL carve-out below
     does NOT cover the flag path: a third party's org passed via
     `--repo`/`--org` lands here at exit `4` (verified: `--repo
     vercel/skills`), same split — your own orgs are listed by `org switch`;
     a third party's routes to the `gh` read fallback of step 6. The message ends `Run \`sling login\``, which
     cannot work: the credential was never the problem. That suffix is
     appended to every auth-class error by a generic decorator, so read it as
     boilerplate rather than as advice about this case.
   - **You have no orgs at all** — exit `2`, `You don't belong to any orgs
     yet.`, and `doctor`'s `org` check saying the same. This is the ordinary
     state of someone who installed `sling` and signed in before ever
     installing the app; signing in succeeds and gives no hint that a step is
     missing. Do not read exit `2` here as a bad flag, and do not send them
     to `sling org switch` — there is nothing to switch to.

   A sandboxed agent shell can also fail an auth probe for reasons of its
   own, so retry once with host access before trusting a single failure.

   In either shape, **STOP and tell the user plainly** — every answer this
   skill gives comes from StarSling's record of their runs, so until the app
   is installed there is no run data to read and only the `gh` read path
   remains. Give them the path: install the app at
   `https://github.com/apps/starslingdev` on the organization whose CI they
   are asking about, or ask an owner to add them. Continue on the `gh`-only path ONLY if they say so, and name
   what is unavailable when you do.

   **A pasted URL from someone else's org never reaches this gate.** The
   resolver searches only orgs you belong to, so a foreign Actions URL fails
   with exit `3` (not-found), not exit `4` — verified live on a `mastra-ai`
   run URL. The app-install remedy applies only to orgs the user belongs to;
   for a third party, the right move is the `gh` read fallback of step 6.

   **Organizations only.** The app installs on a personal repository but
   StarSling does not pick up its jobs, so there is never data to report for
   one — say that rather than reporting an empty result.

6. **If `sling` cannot be installed or authenticated at all**, fall back to
   the `gh` read path for whatever is achievable (`gh run view`, `gh run
   view --log-failed`) and **tell the user plainly** that the richer
   diagnosis — `sling why`'s classification, `sling time`'s phase
   breakdown — is unavailable without `sling`. Do not silently degrade.

   Run the gh gate below before promising that path: with neither CLI
   available there is nothing left to fall back to, and saying so up front
   beats discovering it one failed command at a time.

## Always pass `--agent`

`--agent` is the machine-mode flag: JSON on stdout, no prompts, no colour.
Pass it on every **data** command and parse stdout as JSON. Do not also pass
`--json` — help pages render the pair together (`--json, --agent`), with
per-command wording.

**Do not describe it as an alias for a longer flag list.** The published docs
call it "exactly equivalent to `--json --compact --no-input --no-color
--yes`", and on v0.1.124 `--compact` is not a flag this binary has at all:
passing it changes nothing because unknown flags are ignored, not because it
does anything. Output is pretty-printed, indented JSON either way, so feed
stdout to a real JSON parser and never to a line-oriented one that assumes
one object per line.

**Never pass `--agent` to `sling login`.** Signing in requires a human to
open a browser and approve a device code, and `--agent` carries
`--no-input`, which refuses the prompt rather than showing it — turning the
one command that needs a person into exit `2`. `sling org switch` has the
same shape: under `--agent` its picker is refused, so give it an explicit
slug (`sling org switch acme --agent`).

- **Branch on the exit code, never on whether stdout looks empty.** Human
  chrome (spinners, summary rows, prompts) goes to stderr, and only when
  stderr is a TTY. `6` and `10` are outcomes rather than errors: they emit
  the **full JSON payload on stdout** with stderr empty — an unhealthy
  `sling doctor --agent` exits `10` and still returns every check, which is
  exactly what the preflight above asks you to read.

  **A non-zero exit does not mean stdout is empty, and a well-formed JSON
  body does not mean success.** `sling logs` on a job that stores no logs
  exits `3` and still prints `{"lines": [], "has_more": false, …}`;
  `sling resolve` on an ambiguous id exits `2` and still prints
  `{"candidates": […]}`. So read stdout as JSON *and* read the exit code,
  and when the two disagree the exit code decides. Reporting that empty
  `lines` array as "nothing in the log" is exactly the silent false negative
  this skill exists to prevent — the reason is on stderr, which stays worth
  reading even when stdout parsed cleanly.
- Under `--agent`, every **data** command returns JSON, `sling logs`
  included (`sling exit-codes` is help text: exit `0`, empty stdout, prose on
  stderr). A log-less job's payload carries its own machine discriminator —
  `"local": {"empty": {"kind": "absent"}}` — alongside `"lines": []`.
- JSON keys are `snake_case` on every command **except `whoami`**, which
  returns camelCase (`userId`, `githubLogin`, `expiresAt`). Key a parser per
  command, not on a local-vs-remote rule.

The traps in this contract are collected under [Gotchas](#gotchas) — worth
reading before the first parse.

## The routing table

**Decide with two questions, in order.**

**1. Does the request change anything, or only read?** If the user wants to
*change* CI state — re-run a job, cancel a run, trigger a workflow, flip a
workflow on or off, pull down an artifact — no `sling` command does it.
Use `gh` directly; do not attempt a `sling` subcommand for these under any
name. Updating `sling` itself (`sling update`) changes only the user's
machine, and the user runs it, never you.

**2. If it only reads: is it about one run, one job, or aggregate
cost/usage — or about the repo's CI *configuration* as a whole?** One run,
one job, or spend attribution → `sling`. The repo's workflow YAML, its
best-practice adherence, its security posture, or a multi-run optimization
sweep → hand off (see [Handoff](#handoff-to-the-audit-skills)) instead of
reading YAML yourself.

| User is asking about... | Route to | Command |
|---|---|---|
| Why a specific job failed | `sling` | `sling why <run\|job\|attempt id\|URL>` |
| Where a run's wall-clock went (queue wait vs. provision vs. steps vs. teardown) | `sling` | `sling time <run\|job\|attempt id\|URL>` |
| The same, as percentiles across a repo | `sling` | `sling time --repo <owner/name> --window <n>d` (`--repo` is required; for another org, switch the default) |
| Which part of a workflow is slow — its critical path, hop by hop | `sling` | `sling time --repo <owner/name> --workflow <name>` |
| Whether Afterburner, a provider or a tier changes the timings | `sling` | `sling time --repo <owner/name> --workflow <name> --group-by afterburner\|provider\|tier` — compare the per-hop `delta`; `--group-by` alone mixes different jobs |
| Recent runs and their status | `sling` | `sling runs list [--repo <owner/name>] [--branch --status --conclusion --trigger --workflow-path --label --window --limit]` |
| Detail on one run (its jobs, attempts, runner) | `sling` | `sling runs show <run id\|URL> [--wait] [--fail-fast]` |
| Which jobs in a run failed, or jobs across a repo | `sling` | `sling jobs list --run <id>` / `--repo <owner/name>` [`--afterburner engaged\|not-engaged`] |
| Which step in a job failed, and each step's duration | `sling` | `sling jobs show <job id\|URL>` |
| Only the log lines that matter for a failure | `sling` | `sling logs <run\|job\|attempt id\|URL> [--grep <re>] [--since <dur>] [--limit <n>]` |
| Turning a pasted Actions URL into a run/job/attempt id | `sling` | `sling resolve <id\|URL> [--target run\|job\|attempt]` — a run id covering several jobs is **ambiguous**: exit `2`, `{"candidates": […]}` on stdout. Pass one of the returned candidate ids (`att_<jobid>.<n>`) or `--target run`; `--target job`/`attempt` re-state the kind and return the same ambiguity |
| The biggest time or cost hotspots | `sling` | `sling top [--by workflow\|job\|label\|repo\|branch] [--metric ...]` |
| Runner-minutes and cost attributed per repo/workflow/label/day | `sling` | `sling usage [--group-by <axis>] [--window <n>d]` |
| What is owed this period, or past invoices | `sling` | `sling bill`, `sling bill history` |
| Which runner labels/sizes exist and what they cost | `sling` | `sling labels list` |
| Identity, org, credential, environment health | `sling` | `sling whoami`, `sling doctor`, `sling org switch` — and `sling login` / `sling logout`, which the **user** runs, not you: ask the user to run `sling logout` (it deletes the saved credential) |
| Updating `sling` itself, or turning its background updates off/on | the user | `sling update [--off\|--on]` — **ask the user to run `sling update`** (when `doctor`'s `version` row names another `fix_command`, give them that; when it reads up to date, say so); never run it yourself |
| **Re-run a run or its failed jobs** | `gh` | `gh run rerun <run-id> [--failed \| --job <job-id>] -R <owner/name>` |
| **Cancel an in-progress run** | `gh` | `gh run cancel <run-id>` |
| **Trigger a workflow (`workflow_dispatch`)** | `gh` | `gh workflow run <workflow> [-f key=value]` |
| **Enable or disable a workflow** | `gh` | `gh workflow enable\|disable <workflow>` |
| **Download an artifact** | `gh` | `gh run download <run-id>` |
| **Delete a run** | `gh` | `gh run delete <run-id>` |
| Approve or reject a pending deployment | `gh` | `gh api` — see [references/gh-fallback.md](references/gh-fallback.md) |
| The checks on a specific PR | `gh` | `gh pr checks <pr>` — then take the failing run/job id back into `sling why` / `sling time` |
| Secrets or repo/environment variables | `gh` | `gh secret`, `gh variable` |
| The contents of a workflow file | neither | Read the `.yml` directly — this is a file question, not a CLI action |
| A repo-wide grade, speed sweep, or security scan | neither | Hand off — see [Handoff](#handoff-to-the-audit-skills) |

**Ambiguous asks.** With no action verb (re-run / cancel / trigger / enable
/ disable / download) and a specific run, job, or spend in view, default to
`sling`: it is the read path and costs nothing to try. If the ask is
read-only but `sling` has no matching subcommand — "what does this
workflow's `on:` trigger include" is YAML content, not run data — read the
file rather than forcing it through either CLI.

**Compound asks** — "tell me why this run failed, then re-run it" — are two
steps, in order: do the `sling` half first (`sling why`), **report it**,
then do the `gh` half (`gh run rerun`) as an explicit, separately announced
action — and run the gh gate (below) before promising that second half: a
working `sling` says nothing about whether `gh` is signed in. Never chain
into a state change without telling the user what changed.

## Command reference

Full per-command flags and the verified JSON shape of every response:
[references/command-reference.md](references/command-reference.md). The
machine-readable list of every command that exists, which is what keeps this
skill from inventing one:
[references/command-surface.json](references/command-surface.json).

The short version, grouped the way `sling --help` groups them:

- **Auth & setup** — `login`, `logout`, `whoami`, `doctor`, `update`, `org switch`.
- **Inspect CI** — `runs list`, `runs show`, `jobs list`, `jobs show`,
  `logs`, `resolve`.
- **Diagnose** — `why` (classification, evidence, suggested actions, and a
  ready-to-use `prompt` field), `time` (wall-clock split into
  `queue_wait`, `provision`, `image_pull`, `cache_restore`,
  `checkout+patch`, `steps`, `cache_save`, `teardown`).
- **Cost & capacity** — `usage`, `top`, `bill`, `bill history`,
  `labels list`.

Two habits worth keeping:

- **`sling why` on a RUN (id or URL) can answer for ONE selected job at exit
  `0`** — verified on a cancelled three-job run, where it diagnosed the single
  failed job and never mentioned the other two or the cancellation. Before
  reporting that diagnosis as *the* cause of a run, confirm the run's job set
  (`jobs list --run <id>`) whenever the run has several jobs or did not
  conclude cleanly.
- **Start from `why` for a failure**, not from `logs`. `why` is classified
  server-side with no LLM in the loop, and its `suggested_actions[]` carry
  the exact follow-up command (usually a `sling logs --grep`) instead of
  making you guess a pattern. Its `prompt` field is written for an agent to
  act on directly.
- **`sling logs` is a filter, not a dump.** Reach for `--grep` and
  `--limit` before pulling a whole transcript; `has_more` plus `--cursor`
  pages the rest.

## Exit codes

Branch on `$?`, read immediately after the command. The inference fails in
both directions: a successful result can be empty, and a **failed command
can still print a full JSON body** — `logs` exits `3` with `{"lines": []}`,
`resolve` exits `2` with `{"candidates": […]}` — and so do `logs`, `why`
and `time` on a bare multi-job run id, with `why`/`time` putting **nothing on
stderr** at all. The invocation was valid: read the candidates off stdout and
pass one id (or `--target run`) rather than re-reading `--help` for a usage
error that is not there. Neither an empty stdout nor
a parseable one tells you what happened; only `$?` does.

| Code | Meaning | What to do |
|---|---|---|
| `0` | Success | — |
| `1` | Unexpected internal error (a crash) — **or a subcommand that does not exist** | Read stderr first. `unknown command "<name>" for "sling"` is a routing mistake, not a crash: the binary lists its real commands, so correct the name against that list rather than filing a bug — an invented or mistyped name lands here. stderr naming an environment variable (`SLING_HOST must be a valid https URL …`) is an environment fix, not a bug. Anything else: do not retry blindly, and surface the stderr text as a bug report |
| `2` | Usage — bad flags, a prompt refused under `--agent`, org ambiguity, **or no orgs at all** | Read the stderr first. `You don't belong to any orgs yet.` → step 5, the app is not installed; never a flag problem. Org-ambiguous → `sling org switch <slug>` (or `--org` where the command accepts it: not `logs` or `time`, and never beside `--repo`). Otherwise fix the invocation against `sling <cmd> --help` |
| `3` | Not found — no such run/job/attempt in any org you can access, or a real job that stores no logs | **A pasted URL from a third-party org lands here, not on exit `4`** — the resolver searches your orgs and reports not-found (`No run/job/attempt matches that id in an org you can access`). For an org the user does not belong to, do not suggest installing the app on it: fall back to the `gh` read path (public repos answer) and say the richer `sling` diagnosis is unavailable. Otherwise try `sling resolve`, confirm the org, then ask the user to confirm the id |
| `4` | Auth — **or no StarSling installation on that org, or a third party's org named via a flag.** Read the stderr text before acting | `You don't have access to org "<name>"` → the app is not installed there (or the user is not a member); point them at `https://github.com/apps/starslingdev`, do NOT retry login. Anything else → ask the user to run `sling login` themselves (a browser approval, never `--agent`), then retry once. If the retry exits `4` again, STOP and report what was verified — never ask for a second login |
| `5` | Control-plane or API error (5xx or transport) | Retry once after a short backoff (~2s); on a second failure fall back to the `gh` read equivalent and **say** `sling` was unreachable |
| `6` | Partial — telemetry incomplete, result still emitted (`time`, `why`) | Not an error. Use the result, and tell the user it is partial |
| `7` | Rate limited (HTTP 429) | Back off and retry once. On a second `429`, stop: fall back to the `gh` read equivalent and say `sling` was rate limited |
| `10` | Remote outcome failed — `doctor` unhealthy, or `runs show --wait` on a run that did not succeed | **Not a CLI error.** This is the answer: report the unhealthy check, or the run's failure |

`sling exit-codes` on v0.1.124 prints only `0`–`5`; codes `6`, `7`, and `10`
are real and documented (and `doctor --help` names `10` itself), so treat
that help text as abridged. Any non-zero code not in this table: surface
stderr to the user rather than guessing a recovery.

## Gotchas

These are the places where `sling` behaves differently from what its own
output, its `--help`, or its documentation implies. Each was found by
running the binary; none of them announce themselves at runtime. Everything
version-pinned here was verified against `sling` v0.1.124 and `gh` 2.93.0 —
re-verify on upgrade.

- **`doctor`'s `fix_command` is advice, not a verified command.** Some
  checks emit templates with unfilled placeholders: `git_remote` suggests
  `git remote add origin <github-url>` verbatim. Others are real commands
  that change the user's machine — `version`'s `sling update`, or an
  installer line — and are the user's to run. Never run a `fix_command`
  unchecked. (On 0.1.2 the `version` check named `sling update` before that
  command existed: a command name printed by a tool is not proof the tool
  has it.)
- **`sling update` exists, and the user runs it — never you.** It reinstalls
  `sling` on the user's machine (no GitHub or CI state changes); `--off` /
  `--on` toggle background updates. Under `--agent` it prints
  `{"result": "current"|"updated"|"failed"|"unmanaged", …}`; a failed check
  exits `5`, a failed install `1`, a copy the installer did not place `2`.
- **The version can change mid-session.** About once a day, after most
  commands, an installer-placed `sling` updates itself in a detached process —
  silent under `--agent`, never touching stdout or the exit code, and off
  when `CI` or `SLING_NO_AUTO_UPDATE` is set (not empty/`0`/`false`) or after
  `sling update --off`.
  When a result contradicts this skill, check `sling --version` (local, no
  network) before trusting one seen earlier. Opting out is the user's choice.
- **Exit `4` does not always mean the credential is stale, and its message
  misdirects when it does not.** An org StarSling was never installed on
  fails with `You don't have access to org "<name>". Run \`sling login\`` —
  the same shape as an expired session, ending in advice that cannot work.
  Read the message before acting on the code: a named org means the app is
  missing there, not that the login is.
- **An empty listing is a coverage hole, never a finding.** `sling runs list
  --repo <owner/name>` returns `{"runs": []}` and exit `0` both when the repo truly
  had no runs in the window and when StarSling is not watching that repo at
  all. The payload cannot tell them apart, so an empty result means this
  check did NOT run — say so with the reason you cannot rule out, rather than
  reporting "you have no CI runs" as a fact about their repo. A repo that does
  not exist at all returns the same empty shape at exit `0` (verified live), so
  when the answer matters, a cheap `gh` read — `gh repo view`, `gh run list` —
  settles which of the three it is. The same three-way-ambiguous empty comes
  back from `jobs list --repo` (`{"jobs": []}`), `usage --repo`
  (`{"rows": []}`) and `time --repo` (`{"phases": []}` — at exit `6`, which
  `time --repo` returns even on full data, so "partial" there carries no
  signal; the empty phase list is the coverage hole).
- **There is no client-side timeout.** A black-holed control plane (packets
  dropped, not refused) hangs `sling` indefinitely — verified past 45s — with
  no exit code and nothing on either stream. Wrap long calls in a timeout,
  and when one fires report the timeout itself: a killed command produced no
  result, and "no result" is never "no findings". A *refused* connection
  returns exit `5` cleanly.
- **Unknown flags are ignored, not rejected** (except by `logs` and `update`,
  which exit `2`). `sling runs list --bogus` exits `0` and returns unfiltered rows. Exit `0` is therefore not evidence
  that a filter applied — check the rows you got back before reporting a
  filtered answer.
- **`--help` lists an abridged flag set.** `runs list --help` omits
  `--trigger`, `--workflow-path`, `--label` and the window flags, all of
  which work. Absence from `--help` is not absence from the CLI; the fuller
  list is in [references/command-reference.md](references/command-reference.md).
- **`sling logs` returns JSON under `--agent`** — the same structured
  envelope as every other data command. (An earlier revision claimed the
  published docs disagreed; they do not — the docs document exactly this. The
  real doc discrepancy is smaller: they call the envelope one-object-per-line,
  and it is pretty-printed, indented JSON.)
- **A zero phase in `sling time` can mean "not measured".** In v1,
  `image_pull` and `cold_start` are bundled into `provision` and reported as
  `0` with a reason in `meta.truncated`. Read that array before telling a
  user a phase took no time — a measurement gap reported as a finding is a
  false finding.
- **Exit `10` is an answer, not a failure.** `doctor` unhealthy and `runs
  show --wait` on a failed run both exit `10`. Report what it says. Exit `6`
  likewise carries a real result, flagged partial.
- **`--agent` silently includes `--yes`.** Harmless on data commands, which
  change nothing, but do not treat a confirmation prompt as a safety net.
- **`sling runs show` gives no `job_id`** — its `jobs[]` carry `job_name`
  and `attempts[]` only. Use `jobs list --run <id>` or `resolve` when you
  need job ids.
- **`sling top` can report a repo as `(multiple)`** when one key spans
  repos. Do not print that as a repo name without saying what it means.
- **`sling bill` has two totals.** `amount_due_usd` is what is owed;
  `amount_usd` is before credits. `status: "open"` means the period is still
  accruing, so it is not a final number.

## Handoff to the audit skills

`sling` reads live run data and has **no ability to read workflow
configuration at all**, so it structurally cannot audit, grade, or scan a
repo. When a conversation turns into "audit my whole CI setup", "grade my
CI", "why is CI slow generally", or "is this secure", **stop and name the
right skill** rather than looping `sling` over every run:

| The ask | The skill |
|---|---|
| A configuration best-practices grade ("grade my CI", "CI score") | `ci-score` |
| A measured speed / runner-minute audit across many runs ("why is CI slow") | `ci-speedup` |
| A security scan of the workflow files ("is my CI secure") | `ci-secure` |

Each reads a local checkout and runs its own catalog. Name the skill and let
the user run it; do not approximate one of these from run data.

**Suggest, do not auto-chain.** After `sling usage` or `sling top` shows a
clear cost outlier, or `sling time` shows one phase dominating repeatedly,
end the answer by suggesting `ci-speedup` for the across-many-runs root
cause and fix — `sling` shows *that* this run is slow or expensive;
`ci-speedup` shows *why*, with a fix. Never invoke another skill without the
user asking.

## `gh` fallback

The mutating commands this skill routes to, with their real syntax:
[references/gh-fallback.md](references/gh-fallback.md).

**gh gate, before the first `gh` call.** If `gh` isn't installed or `gh auth
status` fails, `gh` cannot do any of it — and `gh` authenticates separately
from `sling`, so a working `sling` says nothing about whether `gh` is signed
in. Sandboxed agent shells (Codex) can't reach keyring credentials: retry
with host access before trusting a failure, and never report auth "expired"
off a sandboxed probe. When host access is not
   available to retry with, report `gh`'s availability as UNVERIFIED rather
   than expired or absent. Then STOP and tell the user plainly which half of
their request is unavailable — the reads still work through `sling`, the
state change does not. Give the path (https://cli.github.com; then `gh auth
login`), and never report an action as done that never ran.
