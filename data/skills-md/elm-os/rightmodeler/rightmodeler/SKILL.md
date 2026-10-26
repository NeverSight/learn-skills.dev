---
name: rightmodeler
license: MIT
description: >-
  Find where an agent pipeline can swap frontier models for cheaper ones without
  losing quality. Drive the installed rightmodeler TypeScript CLI through its
  resumable pipeline, interpret its machine protocol, present per-family verdicts,
  and open a reviewed model-swap pull request when the evidence supports one. Use
  when the user wants to cut model spend, right-size models per task, benchmark
  cheaper model substitutions, or analyze an agentic pipeline for cost optimization.
---

# rightmodeler TypeScript CLI runbook

**Current path:** use the installed TypeScript CLI, published on npm as
`rightmodeler` (workspace package `@rightmodeler/cli`) with bin `rightmodeler`.
The legacy Python engine has been retired; the CLI is the only engine.

The CLI is resumable. It stores checkpoints and reports under `.rightmodeler/` in
the target repository unless `--store` overrides that location. Re-run the same
command after satisfying a named input or budget boundary. Do not delete the store
to restart.

The installed CLI ships its own documentation; section 3 shows how to read it.

## 0. Reference files

- `reference/harnesses/index.md`: read before preparing a Mode B run. It routes by framework
  shape to one file per pipeline: where the model id is bound, whether correlation headers are
  forwarded, whether a base-URL override is honoured and which variable carries it, how to mock
  side-effecting tools, the entry point, and how to detect downstream coupling.
- `reference/evidence.md`: read before presenting the result in section 8. It defines the
  evidence ladder, the minimums, every abstention reason, every evidence exclusion reason, the
  release gate ids, and judge selection.

## 1. Establish scope and goal

Ask only for inputs that are not already known:

- The repository root.
- The trace file path. Interactive `init` and `estimate` can discover supported
  local, Claude Code, and Codex files, but agent and other non-interactive runs
  should keep passing `--traces` explicitly for deterministic operation.
- The goal and stopping stage. Use `report` for a complete recommendation run.
- How to call models. By default, an API route: the OpenAI-compatible provider base URL and
  the name of the environment variable that already contains its API key. A plan route runs
  candidates or the judge through the user's own `claude` or `codex` CLI, signed in on this
  machine (section 5); use one only after the user agrees, as below.
- On an API route, the maximum allowed replay spend in US dollars, if the operator wants a
  cap. Never ask for, suggest, or set a cap when a plan route is used, unless the user asks
  for one.
- Model, provider, quality, or ownership constraints that affect the run.
- Models the user wants tried, if any. By default rightmodeler tries only models that cost
  less than the recorded one and were released in the last 90 days. Name models with
  `--candidate`, or move the window with `--released-since` or `--released-until`, only when
  the user asks.

Never ask for, read, echo, or store an API key or login token, and never open `~/.claude`,
the Keychain, or `~/.codex/auth.json`. The user sets the named environment variable in their
own shell. Never inline a key's value, and never put a key in a base URL or a header.

Before choosing a plan route, name the route for each role, tell the user what a plan route
means, and get their yes:

- It uses the plan's usage allowance, the same limits as the user's own Claude Code or Codex
  sessions (and this agent's, when it runs on the same plan). It has no cap on calls or
  spend: the run makes as many calls as it needs, and the plan's usage limit is the only stop.
- Prompts from the traces go to Anthropic or OpenAI under the plan account's data settings.
- The CLI adds its own context to every call (for `claude`, including the signed-in account's
  email and the date; for `codex`, including the user's global instructions file) and cannot
  set temperature or an output limit, so the results measure the model inside a coding CLI.
  `rightmodeler docs model-routes` has the details.

On a plan route, rightmodeler checks the sign-in itself. Never offer a plan route in CI:
rightmodeler refuses one when `CI` is set, so use an API route there. Mode B confirmation
(`--modeb-config`) needs an API route for both roles.

## 2. Detect onboarding state

Run from any directory, but always pass an absolute repository path:

```bash
REPO=/absolute/path/to/repository
if [ -d "$REPO/.rightmodeler" ]; then
  echo "Existing rightmodeler state found. Resume from checkpoints."
else
  echo "No rightmodeler state found. Start onboarding."
fi
```

An existing `.rightmodeler/` means resume, not overwrite. Before spending money,
summarize whether this is a new or resumed run and restate the agreed scope.

## 3. Locate the CLI

Prefer an already installed bin. Then prefer the dependency-local bundled bin.
Fall back to the published package through `npx`:

```bash
if command -v rightmodeler >/dev/null 2>&1; then
  RIGHTMODELER=(rightmodeler)
elif [ -x ./node_modules/.bin/rightmodeler ]; then
  RIGHTMODELER=(./node_modules/.bin/rightmodeler)
else
  RIGHTMODELER=(npx --yes rightmodeler)
fi

"${RIGHTMODELER[@]}" --help
"${RIGHTMODELER[@]}" init --help
"${RIGHTMODELER[@]}" docs
# Replace <name> with a name from the list above, for example getting-started, commands,
# exit-codes, evaluators, modeb, gateways, model-routes, github, or github-actions.
"${RIGHTMODELER[@]}" docs <name>
```

Both help commands must exit 0. If either exits 10 or greater, stop and report the
installation or command-line failure. There is no fallback engine.
The shipped docs describe the version actually installed and take precedence over
this runbook if versions differ. If `init --help` does not list `--route`, the installed
CLI predates plan routes; use an API route. If it does not list `--candidate`, the installed
CLI predates candidate selection options; leave `CANDIDATE_ARGS` empty.

### Windows PowerShell

The examples in this runbook use bash. When your shell tool runs Windows
PowerShell instead, locate the CLI like this:

```powershell
$env:NoDefaultCurrentDirectoryInExePath = "1"
$cli = Get-Command rightmodeler.cmd -ErrorAction SilentlyContinue
if ($cli) { rightmodeler.cmd --help } else { npx.cmd --yes rightmodeler --help }
exit $LASTEXITCODE
```

Then run each command on one line with the same arguments, and keep these rules:

- Call `npx.cmd` or `rightmodeler.cmd`, not `npx` or `rightmodeler`: for the bare
  names, Windows PowerShell 5.1 runs the `.ps1` scripts npm installs, which its
  default execution policy blocks.
- Start each call with `$env:NoDefaultCurrentDirectoryInExePath = "1";` so that a
  program planted in the repository cannot run in place of the CLI.
- End each call with `; exit $LASTEXITCODE`, so the shell reports the CLI's exit
  code. Without it, `powershell -Command` turns every non-zero exit code into `1`,
  and codes `2` and `3` mean something else.
- Read the output from the tool result instead of redirecting it with `>`, which
  writes UTF-16 in Windows PowerShell 5.1.
- Set variables with `$env:NAME = "value"`, and quote paths with double quotes that
  do not end in a backslash.

## 4. Preview the plan

Previewing is read-only and needs neither traces nor provider credentials:

```bash
"${RIGHTMODELER[@]}" init --plan --output json --repo "$REPO"
```

Require exit 0. Parse stdout as one JSON object. Its `stages` array names each stage
and marks it `pending`, `stale`, or `complete`; `executedStages` must be empty.
Present the stage plan before starting the run. A parse failure is a runtime failure,
not an empty plan.

## 5. Run through the agreed stage

Set the agreed inputs. `THROUGH=report` runs the complete pipeline. On an API route the
API key must already exist in the environment variable named by `API_KEY_ENV`.

The spend cap is optional. Leave `MAX_COST_USD` empty to run uncapped: every case and
judge cell then runs to completion, which is the right choice when completeness and
evidence quality matter more than cost. Set a cap only when the operator wants a hard
stop; a capped run halts at the boundary with a named remedy and resumes after the cap
is raised. When a plan route is used, leave `MAX_COST_USD` empty unless the user asks for a
cap: plan routes are uncapped, and the plan's usage limit is the only stop. A cap the user
asks for there counts list-price equivalents, not a bill, and is soft, because a coding CLI
sets no output limit.

Use `--policy <path>` for release policy JSON covering the quality floor, shortlist size, and
model allow and deny lists; `--pricing-file <path>` for per-token pricing when a catalog
publishes none; `--catalog-reference <url-or-path>` for an upstream model list that fills what
a catalog lacks, which on a plan route is the price list (by default Vercel AI Gateway's
public list); `--header 'name: value'`, repeatable, for a gateway that routes on request
headers, never for a secret; `--max-concurrency <n>` for the maximum concurrent provider
requests, or on a plan route the maximum CLI processes at once, not a limit on calls;
`--matchers <path>` for a declarative matcher definitions JSON file; `--candidate <id>`,
repeatable, to replay exactly the models the user names, in each family where each one is
cheaper than the recorded models and fits every call site, whatever its release date;
`--released-since <date-or-days>` (a date such as `2026-01-01`, or `365d`) and
`--released-until <date>` to move the release window from its default of the 90 days before
the shortlist is planned; and
`--modeb-config <path>` to select the container image, app spec, step map, and `backend`,
`docker` by default or `cloud` for a remote sandbox. For a Mode B run, read
`reference/harnesses/index.md` first and follow the file it routes to.

Leave `ROUTE_ARGS` empty for an API route. Set it only after the user agrees to a plan route
(section 1), and then always name both roles: a plan `--route` is refused without a
`--judge-route`, and the judge must come from a vendor other than both the candidates' and
the recorded model's.

- Both roles on plans, with `PROVIDER_BASE_URL` empty: for traces that record an Anthropic
  model, `ROUTE_ARGS=(--route claude-login --judge-route codex-login)`; for an OpenAI model,
  `ROUTE_ARGS=(--route codex-login --judge-route claude-login)`.
- Plan candidates judged through a multi-vendor gateway, keeping `PROVIDER_BASE_URL` and
  `API_KEY_ENV`: for example `ROUTE_ARGS=(--route claude-login --judge-route api)`.
- API candidates judged through a plan, keeping `PROVIDER_BASE_URL` and `API_KEY_ENV`: for
  example `ROUTE_ARGS=(--route api --judge-route claude-login)`. Candidates from the judge's
  vendor are left out. A direct OpenAI or Anthropic key serves one vendor and lists no prices:
  judge through the other vendor's CLI and add
  `--catalog-reference https://ai-gateway.vercel.sh/v1/models` to `ROUTE_ARGS`.

This run never reads a route saved by an interactive `init` or `estimate`. To reuse one, ask
the user for the flags that run printed.

Leave `CANDIDATE_ARGS` empty unless the user named models to try or asked for older or
specific release dates, for example `CANDIDATE_ARGS=(--candidate openai/gpt-6-luna)` or
`CANDIDATE_ARGS=(--released-since 365d)`. `--candidate` cannot be combined with the release-date
options. Pass the same `CANDIDATE_ARGS` on every later command for the same store: a command
without them goes back to the default shortlist.

```bash
TRACES=/absolute/path/to/traces.json
THROUGH=report
PROVIDER_BASE_URL=https://provider.example/v1
API_KEY_ENV=RIGHTMODELER_API_KEY
ROUTE_ARGS=()
CANDIDATE_ARGS=()
MAX_COST_USD=
RUN_LOG=$(mktemp)
ERROR_LOG=$(mktemp)

API_ARGS=()
if [ -n "$PROVIDER_BASE_URL" ]; then
  API_ARGS=(--base-url "$PROVIDER_BASE_URL" --api-key-env "$API_KEY_ENV")
fi

CAP_ARGS=()
if [ -n "$MAX_COST_USD" ]; then
  CAP_ARGS=(--max-cost-usd "$MAX_COST_USD")
fi

if "${RIGHTMODELER[@]}" init \
  --yes \
  --through "$THROUGH" \
  --traces "$TRACES" \
  "${ROUTE_ARGS[@]}" \
  "${CANDIDATE_ARGS[@]}" \
  "${API_ARGS[@]}" \
  "${CAP_ARGS[@]}" \
  --output jsonl \
  --repo "$REPO" \
  >"$RUN_LOG" 2>"$ERROR_LOG"; then
  EXIT_CODE=0
else
  EXIT_CODE=$?
fi
```

Parse every nonblank stdout line as one JSON object. Fail loudly with the line
number if any line is invalid. Events are `stage_started`, `stage_completed`,
`stage_skipped`, `warning`, and a final `result`. Preserve their order. Do not infer
success from the presence of output; branch on `EXIT_CODE` first.

This copy-pasteable parser validates the stream and prints each event:

```bash
node - "$RUN_LOG" <<'NODE'
const fs = require("node:fs");
const path = process.argv[2];
const lines = fs.readFileSync(path, "utf8").split(/\r?\n/);
for (let index = 0; index < lines.length; index += 1) {
  if (lines[index].trim() === "") continue;
  try {
    console.log(JSON.stringify(JSON.parse(lines[index])));
  } catch (error) {
    throw new Error(`Invalid JSONL at line ${index + 1}: ${error.message}`);
  }
}
NODE
```

Completed stages are checkpointed. On a resumed run, `stage_skipped` is expected
for current stages. Keep the existing `.rightmodeler/` directory and re-run the
same command so stale or incomplete work resumes at the first boundary.

## 6. Interpret pipeline exit codes

Use the pipeline contract from `rightmodeler docs exit-codes`:

- `0`: success with no actionable recommendation. Successful planning and partial
  `--through` runs also return 0.
- `1`: a complete `init` or `report` found an actionable recommendation.
- `2`: the run needs input at a resumable boundary, or a plan reached its usage limit.
- `3`: the cost budget was reached at a resumable boundary.
- `10` or greater: command-line or runtime failure.

For exit 0 or 1, require a final JSONL `result` event. For exit 1, also require
`result.recommendationExists` to be true. For a complete exit-0 run, require it to
be false. Partial runs can exit 0 without a recommendation.

For exit 2 or 3, parse stderr as exactly one JSON object with `code`, `message`, and
`remedy`. Stdout may contain valid events for stages completed before the boundary.

## 7. Pause at resumable boundaries

On exit 2, name the missing input from `message`, give the exact `remedy`, and wait
for the user or repository owner to provide it. Common remedies include adding
`--traces`, adding `--base-url`, naming an API-key environment variable with
`--api-key-env`, or supplying required confirmation configuration. Never guess a
missing value. Resume with the same store after the input is available.

A `missing_traces_path` remedy can append up to the three newest discovered paths
and the number of additional candidates, followed by `Pass --traces <path>.`
Treat those paths as suggestions only. In the runbook command, continue to pass
the operator-approved trace path explicitly.

Model routes add these exit-2 codes. Report the `message` and `remedy`, then:

- `plan_usage_limit`: the plan reached its usage limit. Tell the user the reset time that
  `message` quotes, or that the vendor gave none, and stop. Rerun the same command only after
  the reset and when the user says so; completed calls are kept. Never retry in a loop, and
  never switch routes without asking.
- `plan_login_required`: the CLI is not signed in with a plan, would use an API key, or lost
  its login. Ask the user to follow the remedy from their own terminal: sign in with the
  command it names, or remove the API key setting it names. Never read or edit that setting
  yourself. Then rerun.
- `plan_cli_unavailable`: the CLI is missing, too old, or changed in a way rightmodeler
  rejects, or `CI` is set. Relay the remedy. Never unset `CI` yourself; in CI, use an API
  route.
- `judge_family_unknown`: model ids name no vendor, so the judge's vendor cannot be checked.
  Replay checks it before any model call. Relay the remedy and ask the user which fix to use.
- `no_neutral_judge`: no judge is available from a vendor other than the candidates' and the
  recorded model's. Replay checks it before any model call. Relay the remedy and ask the user
  for a third-vendor catalog, another judge route (a plan route only after their yes), or an
  evaluator.

Candidate selection adds these exit-2 codes. Each fires before any model call. Report the
`message` and `remedy`, and ask the user before widening the window or naming models, because
either changes what replay spends on:

- `no_recent_candidates`: no model cheaper than a recorded model was released inside the
  release window. Offer the remedy's choices: an earlier `--released-since`, models named with
  `--candidate`, or `--catalog-reference` when the catalog's dates are placeholders.
- `release_dates_unavailable`: a release-date option was passed, but the catalog has no usable
  release dates. Offer `--catalog-reference`, `--candidate`, or removing the date options.
- `unknown_candidate`: a `--candidate` is not in the provider catalog, or matches more than one
  model. Ask the user which catalog id they meant.
- `named_candidates_ineligible`: no named model can be tried at any call site; the message gives
  each model's reason. Relay the reasons and ask which models to name instead.

On exit 3, report that the configured budget boundary stopped the run. Include the
error `message` and `remedy`, the configured `--max-cost-usd`, and the last completed
stage from stdout. Do not raise the budget without explicit user authorization.

On exit 10 or greater, report stderr and stop. Fix the command or runtime failure
before resuming. Do not reinterpret it as a recommendation or abstention.

## 8. Present the result

For exit 0 or 1, read the final result event and present one row per entry in
`familyOutcomes`. Read `reference/evidence.md` for what each abstention reason and gate id means
before summarizing. Include:

- Family identifier.
- Decision and whether it is an effective recommendation.
- Selected candidate, if any.
- Evaluator pass rates, availability, and worst-case bound.
- Confirmation status and any blocker.
- Abstention reason, if present.

Also report `reportPath`. A complete run writes `.rightmodeler/project/reports/report.md`. The
JSON report is kept inside the versioned store rather than written as a plain file, so take the
machine-readable outcome from the final `result` event rather than from a path.

If a plan route ran, name the route that replayed candidates and the route that judged,
relay the report's `## Model routes` section, and say that spend on a plan route is a
list-price equivalent drawn from the plan's allowance, not a bill. Report every `warning`
event with its `code` and `message`; on a plan route these include `plan_route_key_withheld`,
`plan_usage_warning`, `codex_global_instructions`, `judge_vendor_candidates_dropped`, and
`plan_route_cases_left_out`. Candidate selection can add `release_window_skipped`,
`shortlist_no_recent_candidates`, and `shortlist_candidate_left_out`.

Treat family verdicts as the decision unit. Do not promote a single successful case
into a family recommendation. Exit 0 can still contain useful rejects and
abstentions; present them instead of saying that nothing happened.

## 9. Apply and watch a proven swap

Only proceed when the complete result has an effective recommendation. `apply`
runs the machine gates and opens a draft pull request. It does not merge.

`GITHUB_TOKEN_ENV` below names the environment variable that holds the GitHub token;
never pass the token itself. A GitHub App installation token or a classic token with the
`repo` scope supports `apply` and `watch` fully. A fine-grained personal access token
supports `apply`; `watch` then cannot read check runs, uses commit statuses only, and
prints a `github_checks_unavailable` warning, which is expected, not a failure. In GitHub
Actions, the job's `GITHUB_TOKEN` also works when the job grants the permissions it needs.
`"${RIGHTMODELER[@]}" docs github` lists those permissions, the other token details, and
the GitHub App permissions.

First run the machine-gated dry run:

```bash
GITHUB_OWNER=example-org
GITHUB_REPO=example-repository
GITHUB_API_URL=https://api.github.com
GITHUB_TOKEN_ENV=GITHUB_TOKEN

"${RIGHTMODELER[@]}" apply \
  --owner "$GITHUB_OWNER" \
  --github-repo "$GITHUB_REPO" \
  --github-base-url "$GITHUB_API_URL" \
  --github-token-env "$GITHUB_TOKEN_ENV" \
  --dry-run \
  --output jsonl \
  --repo "$REPO"
```

Apply exit codes are command-specific: 0 means the dry run is clean or changes were
applied, 1 means a machine gate refused the change, 2 means the store has no completed
run, and 10 or greater means a runtime failure. On exit 2, read the JSON error on stderr,
such as `stage_not_completed`, and handle it as in section 7. If the dry run exits 0,
run the same command without `--dry-run` to open the draft pull request and request
review from the resolved owners.

After the command returns the pull request number, watch one reconciliation pass:

```bash
PR_NUMBER=123
"${RIGHTMODELER[@]}" watch \
  --owner "$GITHUB_OWNER" \
  --github-repo "$GITHUB_REPO" \
  --pr "$PR_NUMBER" \
  --github-base-url "$GITHUB_API_URL" \
  --github-token-env "$GITHUB_TOKEN_ENV" \
  --output jsonl \
  --repo "$REPO"
```

Watch exits 0 when no action is needed, 1 when review or continuous-integration
actions were taken, and 10 or greater on a runtime failure. Exit 2 has two meanings.
Either another watcher holds the lock, and stdout ends with a `result` event whose
result has `"status":"lock_held"`, so try again later; or the store has no completed
run, and stderr has a JSON error such as `stage_not_completed`, so handle it as in
section 7. Report any `{"event":"warning"}` line to the user with its `code` and
`message`, and continue. Repeat watch on repository events or the project's schedule.
The resolved owners review the draft pull request and decide whether to merge. The CLI
must never merge it.

To run this loop in GitHub Actions, print the tested workflow with
`"${RIGHTMODELER[@]}" docs github-actions` and follow its Setup section.

## 10. Offer to send feedback

rightmodeler has no telemetry, so the team learns what went wrong or what is missing only
when a user chooses to say so. After a run, or when the CLI stopped on a blocker that its
`message` and `remedy` did not explain, you may offer once to send feedback to the
rightmodeler team for the user. Send it too when the user asks. With no user to ask, as in
CI, send nothing.

Before sending, show the user the exact JSON body and get their yes. Never send on your own,
and never send the same feedback twice.

The body may hold a plain-language description of what happened or what is missing, which
coding agent you are, the CLI version, the command, the exit code, and the error `code`. It
must never hold trace content, prompts, model outputs, source code, file contents, keys, or
tokens. Leave out the user's email address unless they give one for a reply.

```bash
curl -sS --max-time 30 -X POST https://www.rightmodeler.com/api/feedback/agent \
  -H 'Content-Type: application/json' \
  -w '\n%{http_code}\n' \
  --data-binary @- <<'JSON'
{
  "message": "What happened or what is missing, in plain language.",
  "agent": "claude-code",
  "version": "<cli version>",
  "context": "rightmodeler init --through report; exit 2; plan_login_required"
}
JSON
```

Only `message` is required, at most 5,000 characters. `agent` names the coding agent sending
it and `version` is what `"${RIGHTMODELER[@]}" --version` prints, each at most 100 characters;
`context` is a line or two, at most 1,000. Add `"contact": "<email>"` only when the user gave
an address for a reply. The body must be valid JSON, so write a line break inside a string
as `\n`.

The command prints the response body, then the HTTP status on its own line:

- `{"ok":true}` and `200`: the feedback was sent. Tell the user.
- Anything else is a failure. `{"error":"<reason>"}` comes with `400` when the request was
  rejected, and with `500` or `502` when the email could not be sent. A curl error and `000`
  mean the request did not complete. Tell the user once, quoting the reason, and move on.
  Never retry in a loop, and send again only when the user asks.
