---
name: traigent-setup-audit
description: "Point Traigent at an existing agent project and get a five-minute, free, local audit of what is weak before spending anything. Use when asked to audit my agent project, check if I am ready to optimize, review my eval setup, tell me what is wrong with my dataset or scorer, find which tunable knobs are actually used, check whether my scorer is repeatable, or when a user has an agent and does not know where to start with Traigent. Reads the code, runs only the user's own deterministic scorer, makes no model calls and no Traigent calls, then names what code alone could not settle and which skill settles it."
license: Apache-2.0
metadata:
  traigent-audience: sdk-user
  traigent-topic: agent-optimization
  traigent-stage: front-door
  traigent-maturity: experimental
  author: Nimrod
  version: "0.2.4"
---

# Traigent Setup Audit

## When to Use

Requires `traigent>=0.27.0` for the two companion SDK commands named at the end of
this file. The audit script itself is standard library only and runs with no SDK
installed and no key configured.

Use this skill when a user has an agent project and one of these is true:

- "audit my agent project" / "is this ready to optimize?"
- "what is wrong with my evaluation dataset?"
- "is my scorer any good?"
- "which of my tunable knobs actually do anything?"
- they have Traigent installed, have not run anything, and do not know where to start.

Use it **first**, before `traigent-optimize-run`, `traigent-boost-agent` or a first
paid run. It is a read-only front door: it hands over to the other skills, and
reimplements none of them.

Do not use it to run an optimization, to size a run, or to reach a Traigent
service. This tier calls nothing.

## What it does, and what it costs

Everything here is static inspection of the project's own files, plus one
sandboxed call of the user's own deterministic scorer. Nothing is charged.

**Say what is enforced, with the level next to it.** The audit process itself
opens no socket. Your scorer runs in a separate process, and how strongly that
process is contained depends on the machine — the audit measures it, reports it
as `network_guard`, and repeats it in the card header. Never relay "no network"
without the level.

| `network_guard` | What holds | What it means |
|---|---|---|
| `isolated (unshare)` / `isolated (bwrap)` | a Linux network namespace with no route to the host network | ctypes, a subprocess, the private `_socket` module and a reloaded `socket` all reach nothing |
| `python-level` | Python's socket entry points replaced with a refusal inside the probe | ordinary socket use is stopped, but code using ctypes, a subprocess or `_socket` is **not** stopped by it — what keeps those from running is the classifier, which is a static read, not a boundary |

At the python-level guard: the audit itself makes no network call; your scorer
runs in a subprocess with Python's socket entry points disabled — code that uses
ctypes, a subprocess or the private `_socket` module can still reach the network,
so only scorers classified deterministic are probed; **that classification is a
static read of the module's imports and calls, not a sandbox.** It reads imports,
`getattr` on a sensitive module, a module named at runtime through the import
builtin or importlib, `sys.modules`, and the `os.exec*` family — and it fails
closed, so a name it cannot read counts as executing. It is still a reading of
source, not a boundary. Where a namespace is available, that is the boundary.

The level is preflighted, not guessed: a sandbox is only claimed after running
`<sandbox> true` on this machine and seeing it exit 0.

## Run it

Resolve `<skill-dir>` to the directory holding this `SKILL.md`; plugin and
flat-install locations differ. Any Python 3.11+ interpreter works — the script
imports nothing outside the standard library, and in particular never imports
`traigent`.

```bash
python3 <skill-dir>/scripts/audit_project.py --root /path/to/project
```

Useful options:

```bash
python3 <skill-dir>/scripts/audit_project.py \
  --root /path/to/project \
  --json /tmp/traigent-setup-audit.json \
  --dataset /path/to/eval.jsonl \
  --scorer evaluators/exact.py:score \
  --repeats 5
```

- `--json` writes the same report as machine-readable JSON.
- `--dataset` audits one file instead of searching the tree.
- `--scorer FILE.py:FUNCTION` picks which scorer to probe. Without it the audit
  probes a scorer only when exactly one deterministic candidate was found.
- `--repeats` is how many times the same pair is re-scored (default 5).

Exit code is `0` whenever the audit ran, whatever it found, and `2` on a usage
error. A finding is not a failure.

## What it checks

| Area | What is read | What is reported |
|---|---|---|
| Agent | `@traigent.optimize` decorators, parsed with `ast` | entry points with `file:line`; each declared knob marked read, never read, or possibly read through a mapping |
| Dataset | JSONL / JSON arrays / CSV whose rows carry an input-like key (`input`, `input_data`, `question`, `prompt`, `query`, `messages`) | the count of rows with no `input`/`input_data` key (keyed `question`/`prompt`/`query`/`messages`, or with no input-like key at all), since `eval_dataset` loads only those two keys and refuses the whole file on the first such row; row count against the `traigent-dataset-curate` minimums; rows with no gold key; exact and near-duplicate inputs; whether a holdout slice exists, how large it is, and whether it overlaps another slice; label balance where the gold values are few and repeated |
| Scorer | functions named `score*`/`evaluate*`/`grade*`/`metric*`, or taking `expected` second | classification (deterministic / LLM judge / code-executing / hybrid); for a deterministic one, repeat-scoring plus a known-good, partial and known-bad probe |
| Setup | the project interpreter, the environment, `.env*` files, `git check-ignore` | installed SDK version; which key **names** are set; whether `.env` is git-ignored; which model ids the configuration space declares |

Row minimums come from `traigent-dataset-curate`: 10-20 for a smoke check, 30-100
for a first tuning slice, 30+ for a holdout slice, 100+ for a high-variance task.

An LLM-judge or code-executing scorer is **never run**. The audit groups those by
reason and prints one counted line per reason — not one line per file — and
routes them to `traigent-eval-audit`.

**Arriving from `traigent-first-run`.** Files under `traigent-runs/` are walkthrough
artifacts (a substitute agent, the run record, and the first run's own `tuning.jsonl` +
`holdout.jsonl` working copies): the card counts them on one line, tagged as first-run
material, names where the first run's reserved slice sits (`traigent-boost-agent` continues
from it), and never takes one as the project's entry point, dataset or scorer — the next
step is chosen from the project's own material, so a graduate whose source dataset is still
one unsplit file is routed to `traigent-dataset-curate` on its own rows. In the project's own
directories, a dataset file named `holdout`/`heldout`/`validation`/`val` beside another
dataset file in the same directory (`eval`/`test` in a file name usually mean the tuning set
and are not read as a holdout) is read as a declared holdout slice: its rows are the holdout
count for both files, the holdout file is judged against the holdout minimum only, and the
overlap check runs across the pair by normalized input; per-row split markers, when present,
win.
The SDK version is read from installed package metadata in `.venv`, then
`.venv-traigent`, then the audit's own interpreter, without starting the project's
interpreter, and the card says which one it is installed in. For a venv created
with `include-system-site-packages = true`, the user site and the base
installation named in its `pyvenv.cfg` are read too, by path.

A function is reported as a scorer when its **name** says so (`score*`,
`evaluate*`, `grade*`, `metric*`, `*_score`, `*_scorer`). A second parameter
named `expected` is only a hint: validators such as `check_stage(body, expected)`
and test helpers share that shape, so a signature-only match is reported only
when its first parameter is `output` — the SDK's own binding contract — or the
module is named like an evaluator. Private names and test files are excluded.
Every near-miss is counted on the card and listed in the JSON, so a real scorer
ruled out this way is visible rather than silently dropped; point `--scorer` at
it if the filter got it wrong.

The key check reads names only. No key value is read, printed or written, in the
card or in the JSON.

## Report the findings as evidence

The script already writes the card. When relaying it:

- Quote the counts and the `file:line` the script produced. "`temperature` is
  declared at `agent.py:9` and the decorated body never reads it" is a finding;
  "your config space has problems" is not.
- For anything not present, say what was searched for and where: "searched for
  `@traigent.optimize` in 41 Python files, found none". Never "you don't have a
  decorated function" — the user may have one the search did not reach.
- Never promise an improvement. This audit measures nothing about outcome.

The card's own `## Next step` section already picks **one** step and quotes the
finding that forced it, in the user's numbers. Relay that one; do not add a
second, and do not reorder it. It is chosen by the first of these that fires —
the order is what stops a bigger dataset being recommended while the scorer it
would be measured with is still unreliable:

| Finding | Next step |
|---|---|
| no `@traigent.optimize` anywhere | `traigent-setup-quickstart`, then `traigent-setup-decorator` |
| a decorated function with no knobs, or no knob its body reads | `traigent-optimize-config-space` |
| no scorer found | `traigent-eval-build` |
| the probed scorer is not repeatable, or ranks a known-bad answer above a known-good one | `traigent-eval-build`, then `traigent-eval-audit` |
| a scorer exists but none could be measured here | `traigent-eval-audit` |
| no evaluation dataset found | `traigent-dataset-curate` |
| a dataset with any row that has no `input`/`input_data` key | `traigent-dataset-curate` |
| a dataset under the tuning or holdout minimum | `traigent-dataset-curate` |
| nothing above fires | `traigent-optimize-run`, mock dry-run first |

Stopping after the free audit is always a valid outcome, and the card says so.
Repeat it rather than pushing the next step.

## What code alone could not tell you

Each gap below is real, and each one needs a Traigent service call — which sends
data off the machine and can cost money. **None of them runs in this tier.**
Run `tier2_checks.py --from-audit report.json` (next section) to see the
approval cards, one per check, each naming what runs, what leaves the machine,
the cost and the stop rule.

None of these is *settled* by asking Traigent. What a Tier 2 check does is
**retrieve the service's verdict if it has one** — and on a real run it may have
none.

| Question the code cannot answer | What retrieving it gets you | Skill to hand over to |
|---|---|---|
| Does the scorer agree with an independent signal on real model output? | whether this run has an independent correctness signal and an evaluator-quality verdict at all — the service may abstain | `traigent-eval-audit` |
| Which individual rows are mislabelled, redundant or too hard? | any examples the service flagged for review, and the per-example scoring metadata it already holds — a flag is not proof, and the result may be empty | `traigent-dataset-curate` |
| Does tuning move the score at all, and which knob moves it? | one separately approved bounded run within your cap and stop rule, then a knob ranking over its trials | `traigent-optimize-run`, then `traigent-analyze-variable-importance` |
| What should I do next, given my own numbers? | an advisory run plan before a run, and the service's suggested next action with its confidence after one | `traigent-analyze-guidance` |

**A completed run is necessary for the readers above, and it is not
sufficient.** The service can abstain because the task has no independent
correctness signal it supports, return zero rows, redact a projection, or hold
no computed result. Each Tier 2 card states what the same check returned on our
own dogfood run, so an empty answer is expected rather than surprising, and
**"stop here" can be the recommended card.** Never buy a run merely to make an
analysis service answer.

In this skill the live interaction-profile fetch described at the end of this
file is a Tier 2 read: do not perform it before the first approval; use the
static defaults.

Quote the Tier 1 finding that motivates each offer, in the user's own numbers.
"8 rows, under the 30-row tuning minimum; a per-example result would say which
of the 8 the service flagged" is motivation. A generic pitch is not.

## Tier 2 — Traigent-backed checks (approval-gated)

Tier 2 is a second script in the same directory. It reads the Tier 1 JSON and
offers, per open question, **one** named Traigent check. It has two modes, and
the default one is the safe one.

**Offer mode (no flags beyond the report).** Prints one approval card per
applicable check and makes **zero network calls** and spawns **zero processes**.
The two halves of that are held up by different things, and the header says
which is which: the network half is **measured** — it installs the same network
guard `audit_project.py` uses and then verifies it, and prints the level it got.
The process half is **by construction**, because that guard covers sockets only
and a subprocess still runs under it: the two checks that shell out are reachable
only through `--approve`. In run mode the number of processes actually spawned is
counted and printed alongside the requests.

```bash
python3 <skill-dir>/scripts/tier2_checks.py --from-audit /tmp/traigent-setup-audit.json
```

**Run mode.** Runs only the checks named with `--approve`, each touching only the
endpoints its card named, and writes a receipt of every request and every process.

```bash
python3 <skill-dir>/scripts/tier2_checks.py \
  --from-audit /tmp/traigent-setup-audit.json \
  --run-id <completed-run-id> \
  --approve evaluator-quality \
  --approve decision-brief \
  --receipt /tmp/tier2-receipt.json \
  --backend-url https://portal.traigent.ai
```

Exit code is `0` whenever the approved checks ran, whatever they returned, and
`2` on a usage error — an unknown check id, a run-dependent check with no
`--run-id`, `plan` with no `--cost-limit`, a missing key, or a plaintext backend
URL. Nothing is attempted before those refusals.

### The approval card

Every card carries the same nine lines, and the user reads them before anything
leaves the machine:

| Line | What it must say |
|---|---|
| Question it answers | the open question from Tier 1, in one clause |
| What it retrieves | what the service **hands back if it has it** — never what it settles |
| Caveat | what this same check returned on our own dogfood run, including when that was nothing |
| Why, in your numbers | the Tier 1 finding that motivates it — counts and `file:line` from **this** project, never a generic pitch |
| What runs | the HTTP method and path, or the CLI command and its flags |
| Leaves this machine | every field that is sent |
| Your API key | where the key travels — the `X-API-Key` request header — or that no key is sent at all. Present on **every** card |
| Cost | `$0 read`, or `real provider spend` |
| Needs | what must exist first (a portal run id, a cap, a provider key) |
| Stop rule | how many requests, and what happens when one fails |

Exactly one card is marked `(recommended)`, chosen by the same ladder Tier 1
uses: with a run in hand, an unreliable scorer is read about before a dataset is
grown, because the dataset would otherwise be measured with that scorer. With no
run in hand and a local fix still open, **the recommended card is `stop-here`** —
recommending a reader then would be recommending a paid run whose only purpose is
to make an analysis service answer, and it may still abstain. **Stopping after
Tier 1 is always a valid option and the offer says so. Silence is not approval** —
nothing runs until `--approve` names it.

### The catalogue

| id | Open question it answers | What runs | Needs | Cost |
|---|---|---|---|---|
| `model-ids` | are my declared model ids real? | `traigent models --provider <provider> --check <model-id> --json`, once per declared id (provider inferred from the id prefix; an id that matches none is skipped with a line, never guessed) | a provider key | $0; egress goes to the provider, not to Traigent |
| `plan` | what should my first run be? | `traigent plan --backend-url <url> --task-description <text> --dataset-size <n> --has-holdout/--no-holdout --objective <objective> --max-trials <n> --cost-limit <usd> --json` | a key and `--cost-limit` | $0 read |
| `evaluator-quality` | is my scorer reliable on real model output? | `GET /api/v1/analytics/runs/{run_id}/evaluator-quality` | `--run-id` | $0 read |
| `example-insights` | which rows are mislabelled, redundant or too hard? | `GET /api/v1/analytics/runs/{run_id}/example-insights` | `--run-id` | $0 read |
| `example-scoring` | has per-example scoring already been computed? | `GET /api/v1/analytics/example-scoring/{run_id}/summary`, and `GET /api/v1/analytics/example-scoring/{run_id}/dataset-quality` **only if** the summary says `computed: true` | `--run-id` | $0 read; no compute is requested |
| `decision-brief` | what should I do next, given my own numbers? | `GET /api/v1/analytics/runs/{run_id}/decision-payload` | `--run-id` | $0 read |
| `list-runs` | which completed portal runs do I already have? | `GET /api/v1/experiments`, then `GET /api/v1/experiment-runs/{experiment_id}/runs` per experiment | `--list-runs` | $0 read |
| `bounded-run` | does tuning move the score, and which knob? | **nothing here.** The card hands over to `traigent-optimize-run` (mock dry-run first) and you return with `--run-id` | knobs the body reads, a dataset, a scorer | real provider spend |
| `stop-here` | is the honest next move to stop? | nothing at all | nothing | $0 |

### `example-scoring` reads; it does not compute

On our own dogfood run of 2026-09-13 the summary returned `computed: false` and
the compute endpoint that would have produced a result returned **HTTP 500**.
This skill therefore does not trigger scoring at all: it reads the summary, and
reads dataset quality only when the summary says results already exist.
**`computed: false` means "the scoring service has not computed results for this
run". It is never read as permission to start a job.** Compute stays out of this
skill until there is a successful runtime witness for that endpoint and a known,
enforceable charging boundary for it; a successful read establishes neither.

### Most of these need a completed run first — and that is not enough

Four checks read a run the service already holds. Without `--run-id` their cards
are printed with the dependency stated plainly rather than hidden: pass
`--list-runs` and approve `list-runs` to find an existing run id, or hand over to
`traigent-optimize-run` to produce one. A completed run is **necessary and not
sufficient**: the service may abstain, return zero rows, redact its projection,
or hold nothing computed. **Never approve a run merely to make one of these
answer.**

`bounded-run` is never executed by this skill; approving it is a usage error,
because starting a paid run is that skill's job and its stop rule, not this
one's. `stop-here` cannot be approved either — it is the option of doing nothing
further here, and it is a complete outcome.

`model-ids` is offered only when the configuration space actually declared model
ids. `bounded-run`'s card says "define a configuration space first" when no knob
was found, because there is nothing for a run to search yet.

### Finding the portal run id

`--list-runs` offers a card of its own, because the reply names your experiments
and runs and the key travels to get it. Approved, it lists every **completed**
portal run newest first with its project id, experiment id, experiment name and
description, status, `completed_at`, and configuration-run count — enough to pick
the intended run rather than the most recent one. **Nothing is auto-selected:**
you pass the one you chose as `--run-id`. Silently taking the newest run means
silently analysing someone else's experiment.

A **local session id is not a portal run id.** The `tv0_…` id and the
`optimization_id` in a local session file return 404 on every analytics endpoint;
only the `run_id` from `GET /api/v1/experiment-runs/{experiment_id}/runs` works.
The listing asks for at most 10 experiments and prints how many came back, so a
full page is reported as possibly incomplete rather than as the whole account.

### How the request is made

The key is read from `TRAIGENT_API_KEY` and travels in the `X-API-Key` request
header — the header the SDK itself sends, and the only one the portal accepts
for an API key. Sending an API key as a bearer token instead returns 401 on every
route, including the identity route: that header is the JWT path. The request
also carries the SDK's own `User-Agent` — the exact value
`traigent.cloud.user_agent.get_sdk_user_agent()` builds, which is the
distribution name, a slash and the installed version — because the portal's edge
refuses the standard-library default with HTTP 403 (`error code: 1010`) before
the service ever sees it.

**Base URLs differ by client, and getting it wrong fails quietly-ish:**

| Caller | Base URL to give it | What the other one does |
|---|---|---|
| this skill's Tier 2 script, `BackendAnalyticsClient`, `traigent plan --backend-url` | the **origin**: `https://portal.traigent.ai`, no `/api/v1` | with `/api/v1` the path doubles and `traigent plan` 404s |
| `ExampleInsightsClient` (the SDK class the dataset skill uses) | the **`/api/v1` base** | with the origin the version prefix is missing from the path it builds, and the request gets 405 |

Tier 2 takes the origin and refuses a `--backend-url` carrying a path, rather
than silently repairing it — the same URL is what you paste into the other
skills. `--backend-url`, else `TRAIGENT_BACKEND_URL`, else
`https://portal.traigent.ai`; a plaintext `http://` URL is refused unless the
host is loopback, which exists so the tests can run a local server. `traigent
plan` needs `--backend-url` explicitly when the key comes from the environment
rather than a stored login, so Tier 2 always passes it.

Transport is `httpx`, already a dependency of the Traigent SDK — Tier 2 adds no
new install. Tier 2 never imports `traigent`; it reads the installed
distribution's version from package metadata.

### Reading a plan

`plan` is advisory text to read, not a script to run. The relay prints three
things next to the payload: that `cost_limit_usd` is **the cap you passed,
echoed back and not a budget the service authored**; the `evidence_level`
verbatim; and the `objectives` block as returned, so you can see each
objective's orientation yourself. On our own dogfood run the plan came back at
`evidence_level: low`, suggested models the account could not reach, named a
command that had been retired from the SDK, and returned the cost objective
oriented to maximize. Check any command a plan names against `--help` before
running it.

### Honesty rules, enforced in code and in tests

- **Verdicts are relayed as returned.** `status: abstain` prints as an abstain
  with its reason and the sentence that it is **not a pass**. `evaluators: []`
  prints as "no evaluator was assessed". A `low` confidence stays `low` and is
  never upgraded.
- **A non-200 is a status, not a body.** The response body is reduced to its
  length: an error body has been observed echoing the request back, key included.
- **An unexpected payload is said to be unexpected.** Anything that is not a
  `success: true` envelope with a `data` object yields "the service returned an
  unexpected payload" and no verdict at all.
- **`computed: false` is reported as not computed**, never as a finding about
  your rows and never as permission to start a scoring job.
- **A 404 is a 404.** A run id the service does not know — a local session id,
  say — produces a status line and no verdict of any kind.
- **An offer says what it retrieves, and what it returned for us.** No check is
  offered without the caveat from our own run beside it.
- **No local budget arithmetic.** Every number printed is the service's own or
  the cap you passed. The plan's `cost_limit_usd` echoes **your** cap, and the
  relay says so.
- **No lift is promised.** A flat or negative result is a real outcome.
- **The key is never printed** — not in a card, not in the receipt, not on a
  command line, not in an error. If a response echoes a value equal to it, that
  response is withheld rather than relayed.

### The receipt is the evidence

`--receipt <path>` writes every HTTP request (method, path, status, response
bytes, elapsed) and every process spawned (argv, exit code, output sizes — the
key is in neither). Keep it: it is the record of what left the machine, and it is
what the tests compare against the server's own log.

The path in each row is the one that was **put on the wire**, read back off the
request, not the string the script assembled. Those can differ — an HTTP client
resolves `..` segments and drops a fragment after the caller hands it a URL — and
a receipt that disagrees with the server's log is worse than no receipt. Two
further rules follow from the same place: a `--run-id` that is not run-id shaped
(8-64 characters of letters, digits, `-` or `_`) is refused before any request,
and every id that becomes a path segment is escaped first — including the
experiment ids that come out of the **service's own reply**. One `list-runs`
approval is also capped at the page it asked for, so a reply carrying more
experiments than requested cannot turn one approval into hundreds of
authenticated requests; the extra are reported as not fetched.

## Optimization Economics — Read This Before Sizing a Run

**Do not default to recommending zero spend.** The canonical Traigent posture on
spending, the five characterization questions with their exact options, the
tailoring rules (including the three-option paging rule), the explanation duty,
and the local survey draft contract all live in one file that ships inside this
skill: **`references/economics-characterization.v0.md`**. Read it from this
skill's own directory before you propose, size, or decline a run — it is
deliberately not restated here. It is generated from
`docs/shared/economics-characterization.v0.md` in the traigent-skills repo,
which is where any edit goes; the copy shipped here is byte-identical.

**Characterize, never compute a budget locally.** Collect the characterization
and relay it; the Traigent service authors the budget, exactly as it authors the
run-plan and the next-step decision — **budget authorship belongs to the
service.** Do not compute, adjust, or recommend a budget locally: no budget
arithmetic in markdown, no floor/cap table, no "roughly $X/day" of your own. The
reference describes what the service computes; it is not a local calculator, and
when the service returns no economics result, say so plainly and continue with
**no budget number at all** rather than inventing one.

**This skill's part:** the free tier produces the counts a sizing conversation
needs — rows, holdout size, knobs the body actually reads, scorer repeatability
— and Tier 2 relays the service's own plan against the cap the user set. The
cap is the user's; the plan is the service's; neither is this skill's.

**Mandatory whenever you relay any of it:** show the options, recommend exactly
one, and explain **why in the user's own numbers** — their agent, their volumes,
their error costs. The explanation is a product requirement, not decoration.

Safety is unchanged and unweakened: mock/dry-run first, **explicit user approval
before any paid run**, an explicit spend cap, and the recorded stop rule. The
service sets *how much* to invest; it never affects *whether* approval is
required — it always is.

## What this audit does not establish

- **Repeatability is not correctness.** A scorer that returns the same wrong
  number every time passes the probe. Agreement with a human is a separate
  question, and the free tier cannot answer it.
- **No lift is promised.** Nothing here says optimization will improve the agent.
  A flat or negative result is a real outcome and gets reported as one.
- **Knob wiring is detected statically.** A knob read through a mapping the
  parser cannot follow is reported as *possibly read*, never as unread, and a
  configuration space the parser cannot read is reported as unread, never as
  absent. Neither is a clean verdict; confirm those by hand.
- **The containment depends on the machine.** At `python-level` there is no
  namespace, so the classifier is what keeps ctypes and subprocess scorers from
  running — not the guard, and a static read of source is not a boundary. The
  card names the level it had.
- **A scorer's own output is not the probe's result.** The probe frames its
  result line and the audit reads only that line, copies only known keys of
  known shape, and drops and counts everything else. A scorer that prints a
  convincing result line makes the probe report `tampered-result`, never a pass.
- **Every cap is printed.** Row, file-size and file-count ceilings, unparsable
  lines and skipped files each become a finding that forces `attention`, so a
  truncated analysis never reads as a clean one.
- **Model ids are collected, not validated.** Checking an id against a provider
  is a network call, which this tier does not make. Tier 2's `model-ids` check
  is where that happens, after approval.
- **Tier 2 relays a verdict; it does not produce one.** What the service returns
  is the service's, and an abstain, an empty result or a `low` confidence is
  reported as exactly that. This skill never fills a gap the service left.
- **Only Python is inventoried in this version.** A JavaScript or TypeScript
  project is not searched for entry points or scorers; see `traigent-js`.
- **A green audit is not a green run.** It means nothing obvious is in the way.

## Two SDK commands worth knowing, and why they are not part of the audit

Both exist in `traigent>=0.27.0`. The audit does **not** shell out to either, so
that its zero-network property stays provable rather than inherited.

- `traigent check my_module.py --dry-run` discovers `@traigent.optimize`-decorated
  functions by **importing** the module, which executes it. Without `--dry-run` it
  goes further and runs a real optimization validation, which makes model calls.
  Offer it as a companion once the user is ready to execute their own code; it is
  never a prerequisite for this audit, which parses the same file instead.
- `traigent models --check MODEL_ID` validates a model id against a **provider's**
  known model surface, not against a Traigent backend. For Anthropic it answers
  from a shipped snapshot and a pattern, with no network at all; for OpenAI,
  Mistral and Nous it asks the provider SDK to list models, and for Azure and
  Bedrock it makes an HTTP or AWS call. Because that is provider-dependent egress
  needing a provider key, it is out of this tier. It is the first, zero-cost item
  of the approval-gated tier.

## Safety

- Tier 1 contacts no provider and no Traigent service. The audit process
  installs the socket refusal before any project file is read, and re-checks it
  rather than assuming it.
- User code runs only in the probe subprocess, only for a scorer classified
  deterministic, under a 30-second timeout — inside a network namespace where one
  is available. The project's interpreter is started for nothing else: the SDK
  version is read from installed package metadata. The one git call
  (`git check-ignore` on `.env`) runs with the project's `core.fsmonitor` and
  hooks switched off and the probe's allowlisted environment, so no command the
  project configures runs there. A judge, a code-executing
  scorer, or a scorer **whose own file** imports ctypes, `subprocess`,
  `multiprocessing` or `_socket` is disclosed and routed, never run. Modules it
  imports from your project are not read, so at the `python-level` guard review
  those by hand.
  Naming one with `--scorer` does not override that; the audit refuses it and
  says so.
- A failure inside your scorer is reported as the exception TYPE and a
  `file:line`. Its message and the process's stderr are never relayed, because
  both have been observed carrying an API key.
- A key value is never read, shown or stored — only whether a known key **name**
  is set, and in which file it is declared.
- The scorer probe runs with only an allowlisted environment: `PATH`, `HOME`,
  locale (`LANG`, `LANGUAGE`, `LC_*`), `TZ` and temp-dir variables. Every other
  variable, credentials included, is withheld, so a scorer that needs one fails
  the probe and is reported by type and location. This is not a filesystem
  boundary: files under your home directory and the project, a `.env` included,
  stay readable to the scorer.
- Anything in the second tier — every paid call and every byte that leaves the
  machine — waits for an explicit approval. Silence is not approval. Offer mode
  runs under the same network guard as Tier 1 and reports the level it had, so
  "no socket was opened" is measured rather than asserted; "no process was
  spawned" is a property of the code path, not of that guard, and every approved
  run writes a receipt with both counts in it.

## See Also

- `traigent-setup-quickstart` — install the SDK and set a key.
- `traigent-setup-decorator` — wire a first `@traigent.optimize` function.
- `traigent-dataset-curate` — build, split and grow the evaluation dataset.
- `traigent-eval-build` — write or wire a scorer.
- `traigent-eval-audit` — assess an evaluator or LLM judge.
- `traigent-optimize-run` — run the first bounded optimization.
- `traigent-analyze-guidance` — ask the Traigent service what to do next.
- `traigent-boost-agent` — the full lifecycle, once this audit is clear.

<!-- INTERACTION_POLICY v1 (synced — do not edit inline; edit docs/shared/interaction-policy.v1.md) -->
## Traigent Interaction Policy
Track an interaction profile and adapt to it. Persona (stable): control=`delegate|guided|inspect`,
expertise=`se|ds|unknown`. Mood (this session): pace=`execute|balanced|explore`. Default when
unknown: `guided,se,balanced`. Infer from explicit user statements first, then recent behavior;
an explicit correction wins immediately. Never store or send this profile anywhere by default.

### Fetch the live profile (when available)
At session or skill start, if a configured Traigent client is available, seed the profile from the
backend with the skill name:

```python
policy = None
try: policy = await client.get_interaction_policy(skill="<this skill>")
except Exception: pass
```

Treat the returned `profile` as the STARTING seed: its control/expertise/pace axes plus
`question_budget`, `options_max`, and `jargon_level` replace the static defaults below. Explicit user
corrections in-conversation ALWAYS override the seed. If the call is unavailable or
`fallback_policy="static_v1"`, simply use the static defaults below; the SDK already fails soft.

- Always be concise.
- Match terminology to expertise. For `se`: plain engineering words; define each Traigent or
  statistics term once in plain language (no Bayesian / variance-decomposition / Pareto jargon
  unless asked). For `ds`: compact optimization and statistical terms are fine.
- Presenting options: show at most 3, mark exactly one **Recommended**, and give one short
  persona-appropriate trade-off per option.
- Autonomy. For `delegate` or `execute`: pick the recommended reversible action and proceed, asking
  only at hard gates. For `guided`: offer options with a recommendation at the key decisions. For
  `inspect` or `explore`: give brief rationale or evidence before asking, and ask before branch
  choices.
- Hard gates — always confirm regardless of persona: paid or provider model calls, sending data or
  private content off the machine, destructive edits, decisions the Traigent service is meant to
  return, and any missing fact the step truly requires.
- Recommend the next skill only after a result-bearing step (a run finishes, an analysis
  completes, a configuration validates) or an explicit decision point. Omit recommendations
  during setup or mid-walkthrough. Cap at 3 recommendations per response, each on its own line
  with a one-line eligibility reason (e.g., "traigent-analyze-results — ✓ run succeeded" or
  "traigent-optimize-run — ✓ config validated").
- Never weaken Traigent safety: dry-run before any paid run; get explicit approval before real cost
  or before any data leaves the machine; treat service-returned plans and next steps as
  authoritative. Never put the persona profile or any private content into telemetry, run metadata,
  experiment names, logs, or provenance files.
<!-- /INTERACTION_POLICY v1 -->
