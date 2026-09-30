---
name: cjules
description: Use the cjules CLI to drive the Jules API — create, list, watch, inspect, message, approve, log, and patch sessions; manage sources; switch between saved API-key accounts. Invoke when the user mentions Jules, jules.google.com session URLs, Jules sessions/sources, or runs `cjules ...`.
---

# cjules — Jules API CLI

`cjules` is a Crystal CLI for the [Jules API](https://jules.google/docs/api). It complements the official tooling with multi-account auth, bulk operations, watch/tail mode, gitPatch extraction, and pipe-friendly outputs.

## When to invoke

- User mentions a Jules session, source, or `jules.google.com/session/<id>` URL.
- User asks to create a new Jules task, list/inspect their sessions, send a follow-up, approve a plan, or apply a session's patch.
- User runs `cjules ...` and needs help building the command.
- User wants to switch between multiple Jules API keys.

Do **not** invoke for unrelated Crystal projects, generic Git questions, or other AI coding agents.

## Setup check (run first when unsure)

```sh
cjules accounts current   # prints active alias, exits 1 if none
cjules config show        # full config, masked keys
```

If no account exists: `cjules login --alias <name>` (prompts for the key with hidden input). For non-interactive contexts: `cjules login --alias <name> --key <KEY>` or `--stdin`.

## Core commands

| Command | Use it for |
|---|---|
| `cjules new [PROMPT\|-]` | Create a session. Auto-detects `--repo` from `git remote origin` and `--branch` from `HEAD`. |
| `cjules ls` | List sessions. Filters: `--state`, `--repo`, `--since`, `--search`. Outputs: `-f table\|json\|jsonl\|yaml`. |
| `cjules get <ID>` | Show one session in full. |
| `cjules watch <ID>` | Tail activities until session reaches a terminal state. `--interval N` to change polling. |
| `cjules msg <ID> <TEXT\|->` | Send a follow-up message into an active session. |
| `cjules approve <ID>` | Approve a plan. Aborts unless state is `AWAITING_PLAN_APPROVAL`; pass `--force` to skip the precheck. |
| `cjules logs <ID> [-f md\|json\|text]` | Export the full activity log. Markdown is the default and the most useful format for a human report. |
| `cjules patch <ID> [--list\|--apply\|--interactive\|--index N]` | Print, list, `git apply`, or interactively apply the session's gitPatch artifacts. |
| `cjules pr <ID> [--open]` | Print (or open) the pull-request URL produced by the session. |
| `cjules rm <ID...>` or `cjules rm --state X --older-than Y --repo R` | Delete sessions individually or in bulk. Confirmation unless `-y`. |
| `cjules sources ls / get <ID>` | Inspect connected GitHub repos. |

## Multi-account auth

Resolution order: `JULES_API_KEY` env > `JULES_ACCOUNT` env > config's active alias.

```sh
cjules login --alias work        # adds; activates only if no account is currently active
cjules login --alias side --activate
cjules accounts ls               # `*` marks active
cjules accounts use personal     # switch persistently
cjules --account=personal ls     # one-off override
cjules logout work               # remove a single account
```

## Output / pipe patterns

Always prefer `-f jsonl` when piping to `jq` (one session per line, no commas):

```sh
# Most-recent failed session ID
cjules ls --state FAILED --limit 1 -f jsonl | jq -r .id

# Re-fetch and apply the patch from the latest completed session
ID=$(cjules ls --state COMPLETED --since 24h --limit 1 -f jsonl | jq -r .id)
cjules patch $ID --apply

# Markdown report of a session for a PR description
cjules logs $ID -f md > report.md
```

## Common recipes

**Triage failures**
```sh
cjules ls --state FAILED --since 7d
cjules logs <id> -f md | less
```

**Bulk cleanup**
```sh
cjules rm --state COMPLETED --older-than 30d         # asks for confirmation
cjules rm --state FAILED --older-than 7d -y          # non-interactive
```

**Apply a session's changes locally**
```sh
cjules patch <id> --list           # see all patches with their base commits
cjules patch <id> --index 0        # print the first patch body
cjules patch <id> --apply          # `git apply` the latest patch in CWD
cjules patch <id> -i               # interactively select hunks to apply
```

**Live-tail a running session**
```sh
cjules watch <id> --interval 5
```

**Continue a stalled / waiting session**
```sh
cjules ls --state AWAITING_USER_FEEDBACK
echo "please also update the README" | cjules msg <id> -
```

## Gotchas

- **Session IDs are 20-digit numbers** (e.g. `18077675164109662449`). Pass the *full* ID to commands. Both `sessions/<id>` and bare `<id>` are accepted.
- **Source IDs use slashes**: `sources/github/<owner>/<repo>` (the `cjules sources ls` ID column shows the slash form). `cjules new --repo OWNER/REPO` maps to that internally.
- **`approve`** is a no-op on completed sessions at the API level; cjules now precheckes the state and aborts early. Use `--force` only if you really want to call `approvePlan` regardless.
- **`watch`** polls; it does not use server push. Default interval is 3s. Increase for long sessions.
- **`patch --apply`** runs `git apply` in the current working directory. Run it from the right repo / branch.
- **`patch --interactive`** requires a TTY (it prompts per hunk). Use `--apply` in scripts instead.
- **Bulk `rm` filters require either `--state`, `--older-than`, or `--repo`** — calling `cjules rm` with no args and no filters is rejected.
- **Prompt input** for `new` and `msg` accepts a positional arg, `--file PATH`, `-` for stdin, or piped stdin (when neither tty nor explicit). When stdin isn't a tty, the alias/key prompts in `login` are disabled — pass `--alias` and `--key`/`--stdin` explicitly.
- **`--repo` filter** matches the source string with `String#includes?`. `hahwul/hwaro-examples` will match `sources/github/hahwul/hwaro-examples`.
- **Date filter `--since`** accepts `30s`, `5m`, `2h`, `7d`, `1w` (case-insensitive). Anything else errors out fast.
- **TTY-only behavior**: color output, hidden key input on `login`, and the `pick` numeric fallback rely on a TTY. Set `NO_COLOR=1` to force plain output; pipe stdin to make `login` non-interactive.

## Error codes

`cjules` exits `0` on success, `1` for runtime / API failures (with the API's message printed), and `2` for usage / argument errors. API failures print `API error (HTTP <code>): <detail>` to stderr.

## When something looks wrong

1. `cjules config show` — confirms which key, base URL, and account is active.
2. `cjules accounts ls` — confirms the saved aliases.
3. `JULES_ACCOUNT=<alias> cjules ls` — bypasses config to test a specific key.
4. Re-run with `--no-color` to capture clean output for an issue report.
