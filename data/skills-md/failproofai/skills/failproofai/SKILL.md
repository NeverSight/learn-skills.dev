---
name: failproofai
description: |-
  The complete FailproofAI skill — setup, local runtime, Cloud, SDK, policies, publishing, evaluator, commands, concepts, and troubleshooting. Give it to an agent that needs to understand or operate FailproofAI without another skill.

  Trigger when the user wants to:
  • set up from zero — install, connect, wire 12 agent CLIs, verify a session lands;
  • move history — backfill sessions, flush the spool, add capture paths, or migrate a machine;
  • run the daemon — start, inspect, upgrade or remove it, diagnose delivery;
  • find the right surface — audits, sessions, policies, keys and orgs, fleet deploys, self-hosting;
  • fix a live machine — a stopped daemon, a session that never lands, a dead hook.

  It can stand alone. When focused sibling skills are installed, route policy authoring to `failproofai-policy-author`, pack publishing to `failproofai-policy-publish`, Cloud and fleet work to `fp-cloud-cli`, eval planning to `failproofai-eval-brainstorm`, and instrumentation to `failproofai-sdk`.
---

# FailproofAI

Observability and enforcement for every harness your agents run in — coding CLIs, chat
gateways, self-hosted assistants, and your own instrumented agents.

    Session  →  Audit  →  Finding  →  Issue  →  Policy
    what happened   is it a pattern   what broke   who owns it   stop it recurring

This is the single umbrella for the whole product. It orients, explains every vertical,
sets a machine up, moves data, operates the fleet, and carries enough reference material to
work alone. When focused sibling skills are installed, route to them for a smaller context.

Source pointers are grep anchors inside the `failproofai` package — `node_modules/failproofai/`
in an installed project, the repo root in a checkout. They survive refactors; line numbers
do not.

## The one thing that will confuse you

**FailproofAI is one product with two halves, and each half has its own binary.** Almost
every early mistake is a category error between them.

| | Local | **FailproofAI Cloud** |
|---|---|---|
| Binary | `failproofai` | `fp` — current. `agenteye` is the legacy binary, still installable |
| Install | `npm i -g failproofai` (Node ≥20.9) | `uv tool install fp-cloud-cli` / pipx |
| Does | hooks, policies, enforcement, capture, machine enrollment | query sessions, audits, issues, alerts, keys, orgs; publish, deploy and roll back policy |
| Needs an account | **no** — works fully offline | yes |
| Config | `~/.failproofai/` | `~/.failproofai/fpcli/cli-auth.json`, mode 0600 |

**Never write `uv tool install fp-cli`.** `fp_cli` is the Python module; the distribution is
`fp-cloud-cli`. The module name installs nothing.

Separate packages and separate auth — but **not** separate config trees any more. The cloud
CLI's session file moved *inside* the local home, so `~/.failproofai/` existing tells you
nothing about whether you are signed in to the cloud, and being signed in tells you nothing
about whether the local half is set up. Check each with its own command. (`~/.fp/cli.json`
and `$FP_HOME/cli.json` are read once for adoption and never written.)

A machine can run the local half forever without ever connecting to the cloud, and that is a
legitimate end state — do not treat "not connected" as a broken install.

### The cloud half was called AgentEye

It is now **FailproofAI Cloud**. Use that name; never introduce "AgentEye" yourself. But
recognise it, because the old name is still load-bearing in places a rename cannot cheaply
reach, and an agent that meets one of these needs to know it is the same product:

| Still says AgentEye | What it is |
|---|---|
| `X-AgentEye-Org`, `X-AgentEye-Client`, `X-AgentEye-Signature`, cookie `ae_session`, OpenAPI title "AgentEye API" | the wire and the session. `fp` still sends every one of these |
| `AGENTEYE_HOME`, `~/.agenteye/events` | the **local daemon's** legacy SDK spool, which it still watches |
| `AGENTEYE_KEY` (collector ingest), `AGENTEYE_API_KEY` (dashboard admin) | ingest credentials. `FP_API_KEY` was named deliberately *not* to collide — never tell anyone to reuse either |
| `ghcr.io/agenteye-enterprise`, k8s namespace `agenteye`, ClickHouse `agenteye.events` | self-hosted infrastructure |
| dist `agenteye-evaluator`, module `agenteye_evaluator`, UA `agenteye-server/<version>` | the RETIRED v1 evaluator package. Scoring is Evaluator v2 now: author a hosted evaluation in the dashboard, or run a worker on the SDK (`failproofai_sdk.evaluator` / `@failproofai/sdk/evaluator`) |
| `incidents:read`/`:write`/`:ack`, `alerts:ack`, the `INCIDENT_ID` positional on `issues show` | retired grants and arguments the server still parses |

**The env prefix follows the binary.** `fp` reads `FP_HOME`, `FP_JSON`, `FP_TOKEN`,
`FP_API_KEY`, `FP_ORG`, `FP_DASHBOARD_URL`, `FP_INSECURE` (plus `FAILPROOFAI_HOME`) and
**zero** `AGENTEYE_*` variables. Legacy `agenteye` reads `AGENTEYE_HOME`,
`AGENTEYE_CLI_TOKEN`, `AGENTEYE_CLI_JSON`. Note the dropped infix: it is `FP_TOKEN` and
`FP_JSON`, **not** `FP_CLI_TOKEN`/`FP_CLI_JSON` — a mechanical `AGENTEYE_` → `FP_` rewrite
produces names nothing reads. `AGENTEYE_ENVIRONMENT` is read by neither CLI. And
`AGENTEYE_TOKEN` in the SDK install doc is an invented name for a GitHub PAT, defined by no
artifact — it must not become `FP_TOKEN`.

What never modernises is the other half of that rule: headers, the cookie, registry paths,
namespaces and the daemon's own `AGENTEYE_HOME` spool. Rename an env var when the binary
changed; never rename a literal something on the wire still reads.

**Two binaries can be on PATH, and `fp` wins.** Resolve it once, at the start:

```bash
command -v fp agenteye        # fp first — prefer it whenever both resolve
```

Legacy `agenteye` (0.1.13) has no `policies`, `fleet`, `guardrails` or `usage` at all, so a
missing command there means "wrong binary", not "not shipped".

**"Audit" is also two unrelated things** — see *Audits: pick the right one*. Getting that
fork wrong wastes the most time of anything in this product.

## Route first

Read this before doing any work. Two of the specialists — `fp-cloud-cli` and `failproofai-sdk`
— are mirrors, synced from a private repo and marked do-not-hand-edit; duplicating or patching
them here is a maintenance bug. `failproofai-eval-brainstorm` is a mirror too, and answers the
question the retired `agenteye-evaluator` skill used to: **what is worth measuring**. It stops at
the proposal — the dashboard's eval authoring page composes, backtests and deploys the
evaluation itself, so nothing here scaffolds an evaluator service any more.

| The request is | Go to |
|---|---|
| Stop a behaviour — "agents keep force-pushing", turn audit findings into enforcement, make a CLAUDE.md real, write/enable a policy | **`failproofai-policy-author`** |
| Publish tested policies as a GitHub pack others can install | **`failproofai-policy-publish`** |
| Publish a Cloud policy version, deploy it to fleet machines, observe, enforce, or roll back | **`fp-cloud-cli`** |
| Query FailproofAI Cloud — browse sessions, events, errors, evals; triage issues/alerts; manage keys, users, roles, settings | **`fp-cloud-cli`** (the cloud CLI skill) |
| Decide what to score — which dimensions are worth tracking, grounded in real sessions | **`failproofai-eval-brainstorm`** |
| Instrument an agent that is **not** one of the 12 supported CLIs — Python or TypeScript/JavaScript, on a framework (LangChain/LangGraph, CrewAI, LlamaIndex, Pydantic AI, Vercel AI SDK, Mastra) or hand-built | **`failproofai-sdk`** |
| Run your own evaluator worker (the eval pod) — LLM judges or checks on your own infra, in Python or TypeScript | **`failproofai-sdk`** |
| Every surface at once — product architecture, commands, terminology, setup, and skill selection | **stay here** |
| Anything local-machine: install, connect, daemon, backfill, flush, capture paths, upgrade, uninstall | **stay here** |
| Keys and org *concepts*, self-hosting, "what is X" | **stay here** |

Two routes run the other way:

- **Policy work on an unset-up machine.** A policy cannot be enforced without an installed
  CLI and (for cloud policy) a daemon. Do *Set up a machine* first, then hand off. The one
  exception is `fp policies test`, which needs nothing but `node` on PATH.
- **"My SDK events never appear in the dashboard."** Split by evidence, not symptom. Verify
  the delivery half here (`config --status`, then `flush --wait`) before sending them to
  `failproofai-sdk` — the bug is usually delivery, not instrumentation.

If a specialist skill is not installed, do the job here — `references/` carries a compact
version of each. Say which specialist would have done it better and how to install it:

```bash
npx skills add FailproofAI/skills --skill failproofai-policy-author
```

## Establish state before you act

Never advise from assumption. Five commands, in this order, cost seconds:

```bash
command -v failproofai fp agenteye           # which halves exist at all
failproofai config --status                  # cloud rows, daemon, layout/version, pause state
failproofai policies                         # what is enabled, and in which scope
fp --json whoami                             # cloud session — read .logged_in, not the exit code
command -v claude codex copilot cursor-agent opencode pi hermes openclaw droid devin agy goose
```

`fp whoami` **exits 0 whether or not you are signed in**; signed out it prints
`{"logged_in": false, "auth_mode": "none"}`. Branch on the field. Any instruction to treat a
non-zero exit as "not signed in" is wrong and will misreport a healthy machine.

`config --status` is the single most informative command in the product. It prints the
pause state first, then the connection rows, then the version triad. Read all three:

| Row says | Means |
|---|---|
| `Ingest REJECTED (401/403) — N batches parked` | the key stopped being accepted **after** connecting. Nothing is arriving. Reconnect |
| policy connected, ingest absent | an `events:add`-only or `policies:pull`-only key. Half the machine works |
| daemon `stopped` / version differs from CLI | enforcement is **failing closed** — see *Troubleshoot* |
| paused | enforcement suspended, max 8h, one session only |

`config --status` overrides its own "connected" line with the delivery-health verdict, so
trust the rejection row over the connection row when they disagree.

## Set up a machine from zero

State the fork before running anything, because it decides whether you need sudo:

- **Local only** — hooks and policies on this machine, nothing leaves it, no account. Never
  run `--connect`. This is a complete, supported setup.
- **Cloud connected** — adds centrally-managed policy, session capture and the fleet view.
  Requires the daemon, which requires sudo.

```bash
npm install -g failproofai        # Node >= 20.9
failproofai config                # the interactive wizard
```

**Only the interactive `failproofai config` wizard installs the daemon.** `config --connect`
deliberately avoids sudo and merely warns. Without a daemon there is no policy pull, no
transcript capture and no delivery — so a `--connect`-only machine looks configured and
ships nothing. This is the single most common broken setup.

The wizard is **six steps**, and the two that matter most are the ones people forget:
daemon (step 0, takes sudo, runs *before* any hook config is touched so a failure leaves the
machine untouched) and scope. It needs a TTY — see *Running these as an agent*.

`references/setup.md` has the full wizard walkthrough, the non-interactive path, and what
each step writes.

### Verify it, do not assume it

```bash
failproofai config --status       # daemon running? both credentials present?
failproofai policies              # hooks installed for the CLIs you expect?
```

Then make one real tool call in the target agent CLI and confirm a decision appears in the
local dashboard's Policies → Activity log (`failproofai`, port 8020). An install that has
never evaluated a single event is not a verified install.

## Connect to the cloud and prove both halves

One URL and one token configure **two independent capabilities**:

| Capability | Permission | Verified against | Written to |
|---|---|---|---|
| Pull managed policy | `policies:pull` | `GET <base>/enforcement/v1/desired-state` | `credentials.json` |
| Push events/transcripts | `events:add` | empty `POST <base>/v1/events` | collector block + ingest credential |

```bash
failproofai config --connect https://app.befailproof.ai --token "<one-time-secret>"
```

Each half is probed **before** anything is written, and only what verified is written. So a
partial success is normal and is reported per-half.

Four traps here, all of which have bitten people:

- **The exit code tracks only the policy half.** An `events:add`-only key writes a working
  ingest credential and still exits 1. Never `&&`-chain on this command — read the output.
- **Transcripts are sent by default.** `--no-transcripts` limits to hook decisions. It is
  matched by exact string, and the `config` branch validates *no* unknown flags — so
  `--no-transcript`, `--notranscripts`, any typo, is silently ignored and full transcripts
  (prompts, file contents) ship. Confirm with `config --status`, not with the exit code.
- **The machine id does not default to the hostname**, despite what `config --help` says. It
  is an explicit `--machine-id`, else the one already on disk, else a random UUID. The
  hostname is only the mutable **label**. Passing `--machine-id "$(hostname)"` on several
  machines silently merges them into one.
- **Use a scoped key, not an admin key.** `events:add` + `policies:pull` is the whole
  requirement. The secret is shown exactly once.

## Bring in existing history

This is the "transfer" surface. Four commands, each for a different situation:

| Situation | Command |
|---|---|
| Connected later than the work happened; dashboard cleared; machine re-enrolled | `failproofai backfill --since 30d` |
| Spooled batches not shipped yet; want them now | `failproofai flush --wait` |
| Sessions live somewhere the collector does not watch (second profile, team share, container home) | `failproofai harness add-path <harness> <label>=<path>` |
| Upgraded npm but the daemon/layout is behind | `failproofai update` |

```bash
failproofai backfill --since 7d --dry-run    # always preview first
failproofai backfill --since 7d
# wait for the daemon's next tick before flushing — see below
failproofai flush --wait
```

**`backfill` then `flush --wait` back to back is a race that reports success while nothing
shipped.** `backfill` only writes a *request file* that the daemon drains on its next tick;
`flush` exits 0 with "Nothing spooled" the instant the spool is empty. Run `backfill`, wait
for the collector to actually re-read (watch `config --status`), then `flush`.

The collector will not re-read a file it already holds a cursor for — that is exactly what
`backfill` exists to override. `--since` takes `30d`, `6m`, or `YYYY-MM-DD`; default 30 days.

`references/transfer.md` covers re-enrolling into a different org, keeping vs resetting the
machine id, and moving capture paths.

## Install hooks and policies across the 12 agent CLIs

```bash
failproofai policies --install --cli claude --scope user
failproofai policies add block-rm-rf
```

Supported: `claude`, `codex`, `copilot`, `cursor`, `opencode`, `pi`, `hermes`, `openclaw`,
`factory` (binary `droid`), `devin`, `antigravity` (binary `agy`), `goose`.

Four things to get right:

- **Scope is not just a location.** `--scope project` writes a committable `npx -y failproofai`
  command with no machine-specific paths; `user`/`local` write an absolute binary path.
  Hermes and OpenClaw are **user-scope only** — they have no project config at all.
- **Bare `--install` with no policy names is interactive on a TTY** (an arrow-key picker that
  will block an agent forever) and, off a TTY, silently installs only the 11 default-enabled
  builtins out of 39. Name the policies explicitly.
- **Installs are additive.** Repeated `--install` unions with what is already enabled; a
  second `--custom` adds another path. There is no "exactly these and nothing else" — use
  `--uninstall` to subtract.
- **Convention policies load by filename.** Any file matching `policies.{js,mjs,ts}` in
  `.failproofai/policies/` (project) or `~/.failproofai/policies/` (user) auto-loads.
  `block-force-push.mjs` is **skipped silently** and enforces nothing; name it
  `block-force-push-policies.mjs`.

**Enforcement is not uniform across the 12 harnesses.** A `deny` only stops something where
that harness consumes the verdict — `PreToolUse` is the only event that blocks everywhere.
`PostToolUse` is observation-only on 10 of 12. `references/harnesses.md` has the matrix; for
authoring, `failproofai-policy-author` owns it in depth.

One builtin, `block-failproofai-commands`, is **always on and cannot be disabled** — it
bypasses the enabled set entirely, including during a pause and when the config fails to
parse. That is deliberate: it is what stops an agent disabling its own guardrails.

## Audits: pick the right one

This fork is unavoidable and is the most common source of wasted effort.

| | Local audit | Cloud audit |
|---|---|---|
| Command | `failproofai audit` | dashboard, or `fp audits …` |
| Scans | this machine's own agent history, offline | sessions already delivered to the cloud |
| Account | **not needed** | required |
| Scheduling | `audit --schedule [days]`, emails you | server-side cadence |
| Output | localhost:8020 dashboard + a JSON cache | findings → issues in the dashboard |

`failproofai audit` parses **exactly six arguments** — `--help`/`-h`, `--status`,
`--schedule [days]`, `--no-schedule`, `--email` (one of the four flags product-wide that also
accepts an `=`), and the undocumented daemon-spawned `--scheduled`. Everything else is rejected by a catch-all, so
`--since`, `--cli`, `--json` and `--port` all fail: there is no way to narrow or redirect a
scan. A bare `failproofai audit` also **does not exit** — it serves the dashboard until
Ctrl+C. Never call it in a foreground agent shell. The cache is written *before* the server
starts, so if you must run it unattended:

```bash
timeout 180 failproofai audit >/dev/null 2>&1 || true    # exits 124; cache is written
cat ~/.failproofai/audit/dashboard.json                  # layout 4 path
```

Turning findings into enforcement is `failproofai-policy-author`'s job — it reads that same
cache. Send them there rather than hand-writing policies here.

## Read sessions and traces

A trace is the ordered, nested view of one session. The documented investigation order:

1. Confirm the goal and the environment the run actually had.
2. Find the **first divergence**, not the last error — the last error is usually a symptom.
3. Inspect the model context and the tool input immediately before it.
4. Check retries, latency, human interventions and policy decisions around that point.

Most of this surface is the dashboard. The queryable slice is the cloud CLI — hand off to
`fp-cloud-cli` for anything beyond a one-shot setup verification. `references/sessions.md`
has the event kinds and what is CLI-reachable versus dashboard-only.

## Prevent: observe → enforce → roll back

The rollout the product actually supports, and every step of it is CLI-drivable — no
dashboard required:

| Step | Command |
|---|---|
| 1. Prove the policy decides correctly, offline | `fp policies test ./rule.mjs --command "…"` |
| 2. Publish an **immutable version** | `fp policies publish <policy-id> ./rule.mjs` |
| 3. Deploy it pinned, **in observe**, to one machine | `fp fleet deploy <machine-id> --add <policy-id>@3:observe` |
| 4. Run a real session, then read what it would have done | `fp guardrails summary`, `fp guardrails timeline` |
| 5. Promote that one machine to enforce, then expand | `fp fleet deploy <machine-id> --add <policy-id>@3:enforce` |
| 6. Roll back | `fp fleet rollback <machine-id>` |

Three things that bite before you get through it:

- **`fp policies publish` deploys nothing.** It mints a new version, never edits one in
  place, and that version sits unused until a `fleet deploy` names it. Publishing and
  shipping are separate acts.
- **A bare `--add` on a new policy enforces it.** `:observe` is not the default — omitting
  the effect is how a first deploy goes straight to enforcement on a live machine. Always
  write the effect. Effects are exactly `enforce` and `observe`.
- **Every `policies`/`fleet`/`guardrails` subcommand except `policies test` exits 2 under an
  API key.** This rollout is a human-session operation; CI cannot drive it.

Step 1 needs no server, no auth, no fleet and nothing installed in the working directory —
the CLI shims the `failproofai` module itself. It wants only `node` on PATH:

```bash
fp policies test ./rule.mjs --command "git push --force origin main"
# {"ok":true,"decision":"deny","policies":[{"name":"no-force-push","decision":"deny",…}]}
```

State its limit honestly: that proves the policy parses, registers and decides for the input
you handed it. It cannot prove the daemon feeds it the same context on a real machine. Only
step 4 shows that.

`fp-cloud-cli` owns this in depth — the `id@v:effect` ref grammar, `--set` versus
`--add`, the concurrency guard, and why `disable` stops enforcement while `delete` does not.

## Operate the fleet and the organization

Admin → enforcement shows **assigned** versus **reported** deployment plus last check-in, and
`fp fleet list` / `fp fleet diff <machine-id>` show the same split from the terminal. The two
diverging is the signal: a machine that never pulled, or stopped reporting.

Permissions are flat `resource:action` tokens (`events:add`, `policies:pull`, `audits:write`).
Presets `read-only` / `standard` / `admin` seed grants. Two rules worth carrying:

- `keys:update` and `orgs:admin` are **human-only** and must never sit on an API key — an
  "admin" *key* is deliberately weaker than an admin *user*.
- The server **widens** grants at auth time (`alerts:read` also carries `issues:read`), but
  the dashboard and CLI display the **stored** grant. Stored ≠ effective.

Depth is in `references/cloud.md`; live key/user/org operations belong to `fp-cloud-cli`.

## Troubleshoot by symptom

| Symptom | First check | Usual cause |
|---|---|---|
| Nothing in the cloud dashboard | `config --status` | no daemon (ran `--connect` only), or ingest rejected |
| Machine not receiving policies | `config --status` policy row | key lacks `policies:pull`, or daemon not running |
| **Every tool call denied, on every CLI** | `config --status` daemon row | daemon unreachable or version-skewed → **fail-closed** |
| Custom policy does nothing | filename | must end `policies.{js,mjs,ts}` |
| Sessions stop at a date | `backfill --since` | cursor advanced before there was anywhere to send |
| `flush` says "Nothing spooled" but dashboard is empty | ran it too soon after `backfill` | the daemon tick had not run |

**Fail-closed is deliberate.** Once daemon configuration is recorded there is no silent
in-process fallback: an unreachable or protocol-skewed daemon denies everything, including
`UserPromptSubmit`, so the user cannot even ask their agent what happened. Fix the daemon
(`failproofai update`, or restart the unit); as a last resort set `daemon.configured` to
false in `~/.failproofai/config.json`. Running any CLI command self-heals three provable
cases automatically.

**Windows is unsupported** for everything cloud- or capture-related — the daemon is
Linux/macOS only. `flush` refuses outright, but `config --connect` still stores credentials,
so a Windows machine can look connected and never ship anything.

## Upgrade, relocate, remove

There is a **version triad** — npm CLI, daemon binary, `~/.failproofai` layout — and they
move independently.

```bash
npm install -g failproofai@latest    # replaces the CLI and NOTHING else
failproofai update                   # migrations + matching daemon binary + restart
```

`npm i -g failproofai@latest` alone is never enough on a daemon machine: the old daemon
binary stays, the layout stays, and the machine goes fail-closed on version skew. Always
follow with `failproofai update`. Use `failproofai migrate --dry-run` to see layout steps
alone.

```bash
failproofai uninstall            # hook entries from every CLI + the daemon service
failproofai uninstall --purge    # also deletes ~/.failproofai
```

Run `uninstall` **before** `npm rm -g failproofai` — npm runs no uninstall script, so
removing the package alone leaves the hooks and the root-owned service behind. `--yes`
removes the service without asking.

## Running these tools as an agent

Collected here because getting one wrong wastes a turn or hangs the session:

- **No `--flag=value`.** Every parser is hand-rolled and rejects the equals form. Across both
  binaries there are exactly four exceptions — `--cli=`, `--effect=`, `--out=` and
  `--email=`. Everything else takes a space, `pack --only` and `--category` included.
- **`fp` globals go before the command.** `fp --json sessions` works; `fp sessions --json` is
  a usage error and exits 2. A command's own options come after it: `fp --json keys create
  ci-bot`. The globals are `--json --base-url --org --token --api-key --insecure/--secure
  --timeout --quiet --no-color`.
- **Commands that never exit:** `failproofai audit` (serves until Ctrl+C) and the bare
  `failproofai` dashboard. Use `timeout`, or ask the user to run them.
- **Commands that need a TTY:** the `failproofai config` wizard, and `policies --install`
  with no policy names. Off a TTY the latter silently narrows to the 11 defaults.
- **Exit codes that lie:** `config --connect` reports only the policy half; `flush --wait`
  exits 0 on an empty spool whether or not delivery works. Read stdout.
- **Nothing here needs sudo except the daemon**, and only the wizard and `update` ask for it.
- Never run `--connect`, `--disconnect`, `uninstall`, a user-scope install or
  `fp fleet deploy` on your own initiative. They change what the user's machines do
  everywhere — enrollment sends data off the machine, and a deploy can start denying tool
  calls on someone else's box. Propose the command; let them run it.

## References

| Load when | File |
|---|---|
| "what is a finding / trace / deployment" — the nouns and the loop | `references/concepts.md` |
| Installing, the wizard's six steps, connecting, provisioning without a TTY | `references/setup.md` |
| Backfill, flush, capture paths, re-enrolling, upgrade, uninstall | `references/transfer.md` |
| The daemon: what it is, how it runs, how it fails, how to fix it | `references/daemon.md` |
| Builtins, packs, local config files and merge order, scopes | `references/policies.md` |
| Which of the 12 harnesses enforces what, and where each config lives | `references/harnesses.md` |
| Local vs cloud audit, findings, issues, alerts, agent contracts | `references/audits.md` |
| Sessions, events, traces, queries, dashboards, the Assistant | `references/sessions.md` |
| FailproofAI Cloud: CLI surface, HTTP API, keys and permissions, orgs, self-hosting | `references/cloud.md` |
| Every `failproofai` command and flag, env vars, on-disk paths | `references/cli.md` |
| Symptom → check → cause → fix, in depth | `references/troubleshooting.md` |
| End-to-end setup across the local and Cloud halves | `references/end-to-end-setup.md` |
| Complete command catalog for both binaries | `references/commands.md` |
| Observe, enforce, evaluate, audit, and manage as product workflows | `references/product-verticals.md` |
| Environment variables and configuration locations | `references/env-vars.md` |
| Legacy literals that must not be renamed | `references/literals.md` |
| Product terminology | `references/glossary.md` |
| Every sibling skill, ownership boundary, and documentation map | `references/skill-directory.md` |
