---
name: gplay-cli-usage
description: "Conventions every gplay command shares: credential and package resolution, output formats, exit codes, `--dry-run`/`--confirm`/`GPLAY_READONLY` gates, the Edit lifecycle. Use when running any gplay command, wiring gplay into CI, branching on an exit code, or introspecting the Android Publisher API offline with `gplay schema`."
---

# gplay CLI conventions (foundation)

Conventions shared by every gplay command; the normative source is
[`docs/DESIGN.md`](https://github.com/PollyGlot/google-play-cli/blob/main/docs/DESIGN.md)
in the CLI repo. `--help` wins over this skill when they disagree:

```bash
gplay --help                       # the whole command tree
gplay <group> --help               # a namespace (releases, tracks, team, …)
gplay <group> <command> --help     # one command, with its real flags
gplay exit-codes                   # the semantic exit-code table + diagnostic codes
```

## Stability: the `[experimental]` banner

gplay is GA. A command whose `--help` opens with `[experimental]` sits outside
the Public contract (pin an exact release in CI, the banner says so); every
other surface holds until a major bump, so CI can pin `v1`
([stability](https://gplay.sh/docs/concepts/stability/)).

## `gplay schema`: the offline API map

Where `--help` documents gplay's own surface, `gplay schema <query>`
introspects the Android Publisher API offline (no credential, no HTTP):
methods, REST paths, types, enums. `[experimental]`; flags in
`gplay schema --help`.

```bash
gplay schema edits.tracks.update    # a method's request/response, one hop deep
gplay schema Track                  # a type's fields, types, enums
gplay schema --command "releases upload"   # the API methods a gplay command calls
```

## Which credential

Highest priority first: `--service-account <path-or-inline-JSON>`,
`--account <name>`, `GPLAY_SERVICE_ACCOUNT` (path or inline JSON), then the
active stored Account (`gplay auth login`). Setup and diagnosis of exits
`10`/`11`: `gplay-setup`.

## Which app (`--package` + project pinning)

Most commands need a target package. Resolution (ADR-0004):

1. `--package com.example.app` on the command, else
2. the package pinned in `.gplay/config.json` for the current repo.

Pin once with `gplay init` (or `gplay apps init`) so day-to-day commands need
no `--package`. Managing the registry of packages is the `gplay-apps` skill.

`customapps` and `team` address the **Developer account** instead, resolved
later-wins (ADR-0015): the id recorded by `gplay auth login --developer-id`,
`.gplay/config.local.json`, `GPLAY_DEVELOPER_ID`, then `--developer-id`; an
unresolved id exits `10`.

## Output: table on a TTY, JSON in a pipe

`--output table|json|markdown`, else `$GPLAY_DEFAULT_OUTPUT`, else auto (table
on a TTY, JSON in a pipe or CI; an unknown value exits `2`). In scripts ask
for `--output json`: read commands pass the API payload through (ADR-0003),
write commands return the request/diff body, so a CI gate is one `jq` line.
The offline commands (`team permissions`, `schema`) emit gplay-owned JSON.

Where a listing pages, it takes `--page-size` and `--page-token`, one page
per call: the next token is `nextPageToken` in JSON, and a stderr note in
table output. `reviews list` and `vitals anomalies` auto-paginate behind
`--limit` instead.

**stdout is data, stderr is logs.** Parse stdout; warnings, progress, and
`-v/--verbose` flow steps go to stderr and never pollute the JSON.

- A `--limit` cap prints a `warning:` on stderr only: read stderr, or pass
  `--limit 0` where allowed, to tell "all" from "capped".
- stderr masks credentials (PEM, JWT, tokens); stdout stays verbatim.

**Every single-value flag is accepted once.** A repeated flag (`--account a
--account b`, and even `-vv`) fails with exit `2` before auth and before any
HTTP call; only list-valued flags such as `--check` or `--stars` repeat.
Replace a flag when rebuilding a command line.

## Exit codes: branch on the number, not the text

`gplay exit-codes` prints the full table. The semantic codes:

| Code | Meaning | Retry-safe |
|---|---|---|
| 0 | Success | n/a |
| 1 | Generic error (fallback) | no |
| 2 | CLI misuse (unknown flag/command, bad value, missing arg) | no |
| 3 | A named safety flag is missing (`--confirm` / `--grant-admin`), re-run with it | yes, with the flag |
| 4 | Denied by environment policy (`GPLAY_READONLY`), a mutating command was refused | no, change the environment |
| 10 | Authentication failure | no |
| 11 | Authorization (403, SA not invited) | no |
| 20 | Client-side validation (bad AAB, unknown locale, …) | no |
| 30 | API 4xx (not found, conflict, gone, …) | no |
| 40 | API 5xx (upstream unhealthy) | **yes** |
| 50 | Network (timeout, DNS, refused) | **yes** |
| 60 | State conflict (open edit, rate-limited, ambiguous target) | sometimes |
| 70 | Findings present: a read-only check ran to completion and reported drift (`apps audit`) | n/a, not an error |

Policy by family: `3` append the named flag and re-run; `4` the environment
forbids the write, change the deployment; `40`/`50` back off and retry;
`2`/`10`/`11`/`20`/`30` fix the input; `60` read the diagnostic code; `70` a
check ran and reported findings, not an error.

### Diagnostic codes: discriminate failures that share an exit code

Under `--output json` a failure carries a stable envelope on **stdout**
(ADR-0044; stderr keeps the human prose):

```json
{"error":{"code":"EDIT_ALREADY_EXISTS","exitCode":60,"retryable":false,"message":"..."}}
```

`code` splits causes sharing an exit code (`60`: open Edit, expired Edit, rate
limit); branch on `retryable`. What the failed call targeted is
`resource: {kind, id}` (`kind`: `package`, `app`, `developerAccount`,
`gamesApplication`, `achievement`, `leaderboard`, `bucket`); read the target
there, since `package` is present only when `resource.kind` is `package`.
Catalog: `gplay exit-codes`, or `gplay schema --codes --output json` for a
machine.

## Safety: `--dry-run` everywhere, `--confirm` for live writes

- **`--dry-run`** is available on write commands: it validates inputs and
  prints the payload/diff it *would* send, with no HTTP call (and usually no
  auth needed). Reach for it before any production-affecting write. Under
  `--dry-run --output json` the preview lists the gates the live call needs
  in `requires`.
- **`--confirm`** gates the writes that reach real users or the live store,
  production releases, `metadata apply`, `compliance datasafety set`, and
  destructive local writes like `auth logout`. Omitting it exits `3`, naming
  the flag (`requires: ["confirm"]` in the JSON error envelope). `CI=true`
  never auto-confirms.
- **`--grant-admin`** is the stronger gate for conferring admin in
  `gplay-team`.
- **`GPLAY_READONLY=1`** (truthy = enforced) is the environment-level guard for
  agent deployments that must only read. Because the safety flags above are
  *advisory*, an agent holding the credential can pass them itself; set this in
  the environment and the kernel refuses **every mutating command** before
  credential resolution and before any network call, regardless of flags, while
  read commands and `--dry-run` previews keep working. Its refusal exits `4`.

## The Edit lifecycle: implicit by default, explicit when you batch

Google Play mutations run inside a transactional **Edit**
(`edits.insert → change → edits.commit`). gplay offers two ways to drive it.

**Implicit (the default).** Each write command opens its own Edit, makes the
change, commits, and discards the Edit on failure; gplay holds the Edit id.
`--keep-edit-on-failure` keeps a failed Edit open for debugging.

**Explicit (`gplay edits …`), when several writes must land in one commit.**

```bash
gplay edits begin            # pins the Edit under .gplay/ (needs `gplay init`)
gplay metadata apply …       # writes reuse the pinned Edit
gplay releases upload …
gplay edits validate         # Google's commit-time checks, the Edit stays open
gplay edits commit           # or: gplay edits discard
```

No auto-commit or auto-discard in explicit mode; `edits status` shows the pin
(`--live` asks the server whether it still knows the Edit). Per-command rules
(the exit `60` cases, a failed commit) are in `gplay edits <cmd> --help`.

Surfaces outside the Edit model, direct calls with no `editId` that
`edits begin` never batches: `compliance datasafety`, `device-tiers`,
`recovery`, `orders`, `vitals`, `games`, `subscriptions`, `iap`, `appstore`.

## Map of skills

| Surface | Skill |
|---|---|
| Auth onboarding | `gplay-setup` |
| App registry + details | `gplay-apps` |
| Releases (upload/promote/rollout) | `gplay-release-flow` |
| Tracks + testers | `gplay-tracks` |
| Reviews | `gplay-reviews` |
| Store listings + images | `gplay-metadata-sync` |
| Data Safety | `gplay-compliance` |
| Team users + grants | `gplay-team` |
| Managed Play private apps | `gplay-customapps` |
| Post-launch vitals (crashes/ANRs) | `gplay-vitals` |
| Orders (view/refund) | `gplay-orders` |
| Play Games config (achievements/leaderboards) | `gplay-games` |
| App recovery (bad-release remediation) | `gplay-recovery` |
| Device tier configs | `gplay-device-tiers` |
| Subscriptions + one-time products (catalog) | `gplay-monetization` |
| Alternative app stores (catalog export, hosted app review) | `gplay-appstore` |
| Play App Signing with a self-hosted KMS key | `gplay-signing` |
