---
name: terra-cli
description: >-
  Read and change Terra API account configuration from the terminal with the
  terra CLI, instead of clicking in the Terra API dashboard: environments
  (dev-ids), enabled providers, data scopes, webhook destinations, API keys and
  data tokens, delivered webhook events, users, health scores, team, and
  billing. Also reaches any admin or data API endpoint directly with terra api
  and terra data-api. Use when a task needs Terra API account state read or
  changed, when you would otherwise tell the user to open
  dashboard.tryterra.co, when a webhook did not arrive or has to be resent,
  when a user connection has to be created or verified, when you want to try a
  data API request before writing the code that sends it, or when the user
  mentions terra-cli, terra login, terra agent setup, TERRA_ADMIN_TOKEN, a
  dev-id, or an x-api-key.
license: MIT
compatibility: Requires the terra CLI on PATH; install with Homebrew or npm
allowed-tools:
  - Bash(terra *)
  - Bash(brew install tryterra/tap/terra)
  - Bash(npm install -g @tryterra/cli)
metadata:
  author: terra
  version: "2.0.0"
---

# Terra API CLI

Terra API account configuration is normally changed by clicking in the
dashboard at [dashboard.tryterra.co](https://dashboard.tryterra.co): which
providers are enabled, which data types they send, where webhooks are
delivered, which credentials exist. You cannot click. `terra` does the same
things from the terminal, so a task that needs account state read or changed is
yours to finish rather than something to hand back.

**Run the command. Do not tell the user to open the dashboard.** Say what you
ran and what came back. Hand the task back only where the CLI genuinely cannot
do it: signing up, approving a login, or anything needing a human in a browser.

## Preflight

Run these before the first real command. They are read-only.

| Check         | Command                                 | A bad answer                                                            |
| ------------- | --------------------------------------- | ----------------------------------------------------------------------- |
| Installed     | `terra version`                         | Command not found. Install it (below).                                  |
| Authenticated | `terra whoami --format json`            | `"authenticated": false`, exit 2. Stop and tell the user how to log in. |
| Environment   | `terra environments list --format json` | Empty means the account has no dev-id yet.                              |

Install with `brew install tryterra/tap/terra` on macOS, which brings shell
completions, and `npm install -g @tryterra/cli` elsewhere and on Windows. apt
and scoop carry it too.

Three traps in that check, in the order they bite:

- **`whoami` always answers with the same JSON shape**, including
  `"authenticated": false`, so parse the field or branch on the exit code.
  A command that ran is not a command that succeeded.
- **Authenticated is not the same as scoped.** The default `terra login` grants
  every non-dangerous admin scope and deliberately leaves out `keys:read`,
  `tokens:admin`, `tokens:write`, `billing:write` and `team:write`. `keys:read`
  is the one that bites: without it `terra data-api` cannot fetch the
  environment's key and `terra environments api-key retrieve` cannot run. Read
  `scopes` from `whoami` before promising either. The fix is
  `terra login --scope keys:read`, which is the user's to run.
- **Do not log in on the user's behalf.** `terra login` needs a human to
  approve in a browser. `TERRA_ADMIN_TOKEN` is the headless path and needs no
  browser. Where a browser exists but you cannot hold a process open,
  `terra login --start` prints a device code as JSON and exits, and
  `terra login --complete <device-code>` finishes once a human has approved.

## The one rule: two APIs

Terra API is two HTTP APIs, and confusing them is the most expensive mistake
here.

> If a public docs guide teaches it, it is the data API, and it belongs in the
> code you are writing. If you would do it by clicking in the dashboard, it is
> the admin API, and it belongs in a `terra` command.

**The data API** (`access.tryterra.co/api/v2`, authenticated with a `dev-id`
and an `x-api-key`) is the integration itself: sending a user through the
widget, receiving webhooks, deauthenticating, and reading activity, sleep,
daily, body, nutrition, menstruation, athlete, workout and lab-report data.
The application you are writing calls this one.

**The admin API** (`/api/v3/admin`, authenticated with an admin token) manages
and debugs that integration: environments, providers, data scopes,
destinations, credentials, delivered events, connections, team, billing. It is
the API the dashboard itself uses, and **the application never calls it**. You
do, when setting the integration up or working out why it did something.

So "why did this webhook not arrive" and "which providers are on" are admin API
questions this CLI answers. "What does a sleep payload contain" and "how do I
connect a user" are data API questions whose answer goes into the code.

`terra` reaches both. Every admin command is generated from the API
description, so that surface is covered whole. The data API has no generated
commands: `terra data-api <path>` reaches any endpoint.

## Task index

Find the row, then read the reference file before running anything more than
the one-liner.

| Goal                                                            | Start with                                                                 | Reference                                                                    |
| --------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Audit an account, or get started                                | `terra whoami`, `terra environments list`                                  | [references/account-audit.md](references/account-audit.md)                   |
| Turn a provider on, point webhooks somewhere, choose data types | `terra unified-api sources list --env <dev-id>`                            | [references/environment-setup.md](references/environment-setup.md)           |
| Work against a tunnel, test a handler, wire up CI               | `terra unified-api destinations list --env <dev-id>`                       | [references/local-development.md](references/local-development.md)           |
| A webhook never arrived, arrived wrong, or has to be resent     | `terra events list --env <dev-id> --outcome failed`                        | [references/webhook-debugging.md](references/webhook-debugging.md)           |
| One user's data is missing, late, or wrong                      | `terra users list --env <dev-id> --reference-id <ref>`                     | [references/support-triage.md](references/support-triage.md)                 |
| Connect a user, or check whether a connection worked            | `terra data-api /auth/generateWidgetSession -X POST -d reference_id=<ref>` | [references/user-connections.md](references/user-connections.md)             |
| Read or backfill a user's health data, try a request by hand    | `terra data-api /sleep -q user_id=<uuid> -q to_webhook=false`              | [references/data-api.md](references/data-api.md)                             |
| It works in one environment and not another                     | `terra unified-api sources list --env <dev-id> --format json`              | [references/comparing-environments.md](references/comparing-environments.md) |
| Is this account ready to go live                                | `terra entitlements list`                                                  | [references/going-to-production.md](references/going-to-production.md)       |
| Credentials: API keys, data tokens, admin tokens, rotation      | `terra environments api-key retrieve --reveal`                             | [references/credentials.md](references/credentials.md)                       |
| Add or remove a person, audit who holds what                    | `terra team members list`                                                  | [references/team-and-access.md](references/team-and-access.md)               |
| What is this account charged, is the product on it              | `terra billing invoices upcoming retrieve`                                 | [references/billing-and-usage.md](references/billing-and-usage.md)           |
| Write a script or a CI step, or parse output                    | `terra <command> --format json --json <fields>`                            | [references/scripting.md](references/scripting.md)                           |
| Find out whether a command exists at all                        | `terra reference --format json`                                            | [references/command-map.md](references/command-map.md)                       |

Health scores, planned workouts, models and company records have generated
commands too. [references/command-map.md](references/command-map.md) has the
whole surface grouped by noun.

## Discovering commands

Command names are derived from the API description, so **do not guess them and
do not walk `--help` a level at a time**. One call gives you everything:

```sh
terra reference --format json      # the whole tree, machine-readable
terra reference billing            # one subtree, as prose, far fewer tokens
terra help <command>               # every parameter, not just the common ones
```

`terra <command> --help` truncates a long parameter list and says so; `terra
help <command>` does not. Commands read as `terra <group> <resource> <verb>`,
with verbs from the API: `list`, `retrieve`, `create`, `update`, `replace`,
`delete`. Products name themselves first (`terra unified-api sources list`) and
the platform layer sits at the root (`environments`, `users`, `events`,
`tokens`, `team`, `billing`).

Three things to know when reading `terra reference --format json`:
`global_flags` sits at the document root and applies to every node, so a flag
missing from a leaf may still be accepted there; a flag with no `default` has
the zero value for its type, not an unknown one; and `long` carries the
required scope and the behavior the flag list does not show.

## Guardrails that stop an unattended run

These are the failures an agent hits that a human at a keyboard does not.

**A command whose response contains credential material refuses to print it
without `--reveal`.** It fails rather than printing a redacted body, so the
flag is not optional once you have decided to run the command:

```
terra data-tokens create               terra environments api-key retrieve
terra data-tokens secret retrieve      terra environments api-key rotate
terra team invitations create          terra tokens rotate
terra unified-api destinations create  terra unified-api sources credentials retrieve
```

`terra unified-api destinations create` is the one that surprises people: it
returns the destination's signing secret, so creating a webhook destination
needs `--reveal` even though nothing about the request looks secret.

**A destructive command confirms first, and with no terminal to confirm on it
fails rather than hanging.** Pass `--yes` when you mean it:

```
terra billing subscriptions cancel-incomplete  terra tokens delete
terra billing subscriptions create             terra tokens rotate
terra data-tokens delete                       terra unified-api destinations delete
terra environments api-key rotate              terra unified-api sources credentials replace
terra team invitations delete                  terra unified-api sources disable
terra team members delete                      terra unified-api sources scopes replace
terra workouts metadata delete                 terra unified-api widget update
terra workouts metadata replace
```

**A `replace` clears every field you do not supply.** That applies to
`unified-api data scopes replace`, `unified-api sources credentials replace`,
`unified-api sources scopes replace` and `workouts metadata replace`, and to
one command whose name does not say so: **`terra unified-api widget update` is
a full replace**. Retrieve the current document first, edit it, send it whole.

**`--dry-run` prints the request and sends nothing.** It is on every command,
including `terra api` and `terra data-api`, and needs no credential. Use it to
confirm which environment resolved and what body was built before a mutation.
`--json` is refused alongside it; filter the preview with `--jq`.

Mutations carry an `Idempotency-Key` automatically and reuse it across
retries, so a retried request cannot double-apply. `terra api` never generates
one, because it cannot know whether the endpoint deduplicates.

## Environments

Most commands act on one environment, a dev-id, resolved as `--env`, then
`TERRA_ENV`, then the profile default from `terra environments use`. A command
that needs one and finds none fails before sending a request.

`--env` takes the environment's name as readily as its dev-id, matched without
regard to case, and an exact dev-id always wins over a name. Prefer the dev-id
from `terra environments list`: it needs no resolution and cannot be ambiguous.
When several environments exist, name them and ask which one rather than
guessing, because a mutation against the wrong dev-id is a production change.

## Output

Output is JSON when piped and a table on a terminal. Two flags keep large
responses out of context, and both work in every format:

```sh
terra users list --env dev-prod --json user_id,provider,active
terra users list --env dev-prod --jq '[.[] | select(.active)] | length'
```

`--json <fields>` narrows the response to the fields you name and is refused
before the request is sent if a field does not exist; run it with no value to
list what is available. `--jq` runs a built-in jq over the response, so it
works where jq is not installed. **Reach for one of them on every list command
rather than piping a whole document around.**

Lists fetch one page. `--paginate` walks to the end and prints NDJSON whatever
`--format` says, **capped at 10 pages by default**; pass `--max-pages 0` for no
limit. The cap is announced on stderr rather than truncating silently, which is
easy to miss when stdout is piped into a filter.

## Exit codes

| Code | Meaning                                                                                |
| ---- | -------------------------------------------------------------------------------------- |
| 0    | Success                                                                                |
| 1    | The API returned an error, so the problem may be state rather than the command         |
| 2    | Not authenticated, or the token was rejected                                           |
| 3    | Input failed validation before the request was sent, so retrying unchanged cannot help |
| 4    | Usage error: unknown command, bad flag, wrong arguments                                |
| 5    | The product is not on the account                                                      |
| 6    | Internal error in the CLI                                                              |
| 7    | Canceled: a confirmation prompt was declined                                           |

Branch on these rather than matching message text. Errors print the API's own
remediation text, which usually names the fix, including which scope to request.

## Anti-patterns

- **Telling the user to open the dashboard.** There is a command. Find it with
  `terra reference`.
- **Guessing a command name.** Names come from the API description. `terra
reference --format json` is one call.
- **Reading data without `to_webhook=false`.** `terra data-api /sleep -q
user_id=...` with no `to_webhook=false` sends the data to the configured
  webhook and answers with an acknowledgement, which reads like an empty
  result. The CLI says so on stderr and does not add the parameter for you.
- **Running a destructive command unattended without `--yes`,** or a
  credential-returning one without `--reveal`. Both fail; see the lists above.
- **`if ! terra ...; then`.** Inside the negation `$?` is always 0, so every
  case falls through. Run the command, then branch on `$?` directly.
- **Piping a whole list document into context.** Use `--json <fields>` or
  `--jq`.
- **Trying to change a destination's URL with `update`.** It takes only
  `--active` and `--event-types`. Repointing means delete and recreate, and the
  new destination has a new signing secret the handler has to be given.
- **Assuming an old event is still there.** Delivery history and payloads are
  retained about 14 days.
- **Reaching for `terra api` where a generated command exists.** The generated
  command validates input, formats output, and knows the operation is
  destructive. Use the raw commands for uncovered endpoints, or to see exactly
  what the API returned.
- **Mixing the two credentials.** An admin token does not authenticate the data
  API and an environment API key does not authenticate the admin API.

## When you do not know something

This skill carries how the CLI behaves. For what an endpoint returns or how a
product works, ask rather than guessing from training data:

```sh
terra ask "how do I verify a webhook signature?"
terra ask "which providers support sleep data" --format json
```

`terra ask` answers from Terra API's published documentation and cites the
pages it came from. It needs an authenticated CLI. Quote the question into one
argument, and put one starting with a dash after `--`. **`sources` is the
signal that an answer came from the documentation, and `confidence` is not**:
an answer citing no sources did not come from the docs, and the CLI says so on
stderr. Finding nothing exits 0, so check `sources` rather than the exit code.

For the docs directly, look a page up rather than guessing its URL:
[docs.tryterra.co/llms.txt](https://docs.tryterra.co/llms.txt) indexes every
page, appending `.md` to any docs URL returns markdown, and the same docs are
served over MCP at `https://docs.tryterra.co/~gitbook/mcp`.

Use the CLI for account state and the docs for contracts. Neither replaces the
other: `terra reference` will not say what a sleep payload contains, and the
docs will not say which providers this account has enabled.

## Other Terra API skills

This skill is the CLI: reading and changing account state, and reaching
endpoints by hand. Terra API publishes separate skills for the integration code
you write, covering webhook handling and data storage (`terra-unified-api`),
the mobile and streaming SDKs, and each product. Making a webhook handler or a
data model correct is their job; finding out what the account is actually
configured to do is this one's.

`terra agent setup` installs every skill the catalog publishes into the coding
agents this project uses, and `terra agent setup --status-only` reports what
would change without writing. Do not assume the set named above is current: the
catalog is what it is at install time, not what this file remembers.
