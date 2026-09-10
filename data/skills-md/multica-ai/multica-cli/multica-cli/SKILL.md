---
name: multica-cli
description: "Use when a local coding agent (Codex, Claude Code, Cursor, or similar) needs to operate Multica through the authenticated `multica` CLI: reading or updating issues, comments, metadata, labels, custom properties, subscribers, projects, agents, squads, runtimes, repos, skills, autopilots, attachments, or workspace state; searching issues; inspecting or cancelling agent runs; replying to a Multica issue from an external agent; creating or triaging issues; checking linked pull requests; or safely handling Multica mention/status side effects without relying on the Multica hosted agent runtime."
---

# Multica CLI

Use the local `multica` CLI as the source of truth. This skill teaches an
external agent how to drive Multica safely; it does not grant permissions.
Permissions come only from the user's installed CLI, selected profile,
workspace, and explicit approval to run commands.

## Start Safely

1. Verify the CLI and account state before doing work:

```bash
multica version
multica auth status
multica config show
```

**This skill requires `multica` v0.4.26 or newer.** Several commands it relies
on — notably `--no-start` on `issue status` / `assign` / `update` — do not exist
in earlier versions, and an older CLI will reject them outright. If
`multica version` reports anything below 0.4.26, stop and ask the user to
upgrade (`brew upgrade multica-ai/tap/multica`, or `multica update`) rather than
working around the missing flags.

If `multica auth status` reports no active session, the CLI is not logged in.
Stop and have the user authenticate; do not try to fake credentials:

```bash
multica login        # interactive auth + workspace setup
multica setup        # alternative: configure CLI, authenticate, start daemon
```

2. Use the correct workspace and profile. Discover what is available, then
prefer explicit flags when the user names them:

```bash
multica workspace list --output json                 # which workspaces exist
multica workspace switch <workspace-id>              # set the default for this profile
multica --profile <profile> --workspace-id <workspace-id> issue list --output json
```

3. Prefer `--output json` whenever a command supports it. Parse JSON rather than
scraping tables.

4. Never expose or store tokens, cookies, API keys, or CLI config secrets. Do
not bypass workspace permissions by calling private HTTP APIs directly.

## Command Reference

The flags below are the common ones for the issue workflow you will use most.
You do not need `--help` for these. Run `--help` only to confirm a rejected flag
or to explore the long-tail namespaces, whose shapes vary and are not duplicated
here. `[ ]` marks optional flags; `|` marks mutually exclusive ones.

```bash
# Read
multica issue get <id> --output json
multica issue list [--status <s>] [--assignee <name> | --assignee-id <uuid>] [--project <id>] [--priority <p>] [--metadata key=value] [--sort <col>] [--direction asc] [--limit N] [--offset N] --output json
multica issue search <query> [--include-closed] [--limit N] --output json
multica issue children <id> --output json
multica issue pull-requests <id> --output json
multica issue metadata list <id> --output json

# Comments (read) — see Reading Comments below before picking a mode
multica issue comment list <id> --roots-only --summary --compact --output json   # scan threads cheaply
multica issue comment list <id> --thread <comment-id> --tail 30 --compact --output json  # open one thread
multica issue comment list <id> --recent N --compact --output json               # N most active threads
#   also: --since <RFC3339>, --full (unfold resolved threads),
#         --before/--before-id <cursor> for pagination

# Create / update
multica issue create --title "..." [--description-file <path>] [--priority <p>] [--status <s>] [--assignee <name> | --assignee-id <uuid>] [--parent <id>] [--stage N] [--project <id>] [--due-date YYYY-MM-DD] [--start-date YYYY-MM-DD] [--attachment <path>] [--attachment-id <uuid>] [--allow-duplicate] --output json
multica issue update <id> [--title "..."] [--description-file <path>] [--status <s>] [--priority <p>] [--assignee <name> | --assignee-id <uuid>] [--parent <id> | --parent ""] [--stage N] [--due-date YYYY-MM-DD] [--start-date YYYY-MM-DD] [--no-start]

# Status / assignment  (status values: backlog | todo | in_progress | in_review | done | blocked | cancelled)
multica issue status <id> <status> [--no-start]
multica issue assign <id> --to <name> | --to-id <uuid> | --unassign [--no-start]

# Comment (write) — body always via file, see Write Workflow below
# --parent is required when a comment triggered your task; see Issue Comments
multica issue comment add <id> [--parent <comment-id>] --content-file <path> [--attachment <path>]

# Metadata
multica issue metadata set <id> --key <k> --value <v> [--type string|number|bool]
multica issue metadata delete <id> --key <k>

# Labels — issue label add/remove take a label UUID, so list the workspace labels first
multica label list --output json
multica issue label list <issue-id> --output json
multica issue label add <issue-id> <label-id>
multica issue label remove <issue-id> <label-id>

# Custom properties (workspace-defined fields)
multica property list --output json
multica issue property list <issue-id> --output json
multica issue property set <issue-id> --name <name> --value <v>
multica issue property unset <issue-id> --name <name>

# Subscribers (who gets notified; defaults to the caller)
multica issue subscriber list <issue-id> --output json
multica issue subscriber add <issue-id> [--user <name> | --user-id <uuid>]
multica issue subscriber remove <issue-id> [--user <name> | --user-id <uuid>]

# Runs — see Inspecting Runs below
multica issue runs <issue-id> --output json
multica issue run-messages <task-id> [--issue <issue-id>] [--since N] --output json
multica issue usage <issue-id> --output json
multica issue rerun <id> --output json
multica issue cancel-task <task-id> [--issue <issue-id>]
```

Note `issue assign` uses `--to` / `--to-id`, while `issue create` / `issue
update` use `--assignee` / `--assignee-id`.

Other namespaces follow the same shape; inspect them when the task needs them:

```bash
multica project --help
multica agent --help
multica squad --help
multica runtime --help
multica repo --help
multica skill --help
multica autopilot --help
multica attachment --help
multica label --help
multica property --help
multica chat --help
multica user --help
```

## Reading Comments

Comment history is the most token-expensive thing you will read, and the read
modes are not interchangeable.

- `--recent N` caps **threads, not comments**, and each thread carries every
  descendant. On an issue with fewer than N root threads this returns the whole
  history. It is not a cheap read.
- Prefer two bounded reads: scan with `--roots-only --summary` (each root also
  reports `reply_count` and `last_activity_at`), then open only the threads that
  matter with `--thread <id> --tail N`.
- Add `--compact` to any JSON read. It drops echoed, null, and bookkeeping
  fields while leaving content untouched — always correct for an agent read.
- **Resolved threads are folded by default.** The complete-thread modes collapse
  a resolved thread to its root plus conclusion and report the dropped count on
  the root. That is not data loss; pass `--full` when you actually need the
  settled discussion.

```bash
multica issue comment list <issue-id> --roots-only --summary --compact --output json
multica issue comment list <issue-id> --thread <comment-id> --tail 30 --compact --output json
```

## Finding Things

`multica issue search` matches titles, descriptions, **and comment bodies**, so
a decision that only ever lived in a thread is still findable. Reach for it
before concluding something does not exist.

```bash
multica issue search "retry backoff" --include-closed --output json
multica issue list --metadata pr_number=123 --output json
```

A bare number or an identifier-shaped query (`412`, `AGE-412`) matches the issue
with that number, and the prefix is not validated — pasting an identifier from
another tracker can put an unrelated local issue at the top. The `match_source`
field is a display hint, not a filter.

## Write Workflow

Treat writes as side-effecting. If the user did not clearly ask for the write,
ask before running it. This includes creating comments, issues, status changes,
assignments, reruns, cancellations, label and property changes, agent mentions,
squad mentions, webhook/autopilot changes, and repo checkout operations.

### File Paths Must Be Inside the Working Directory

`--content-file`, `--description-file`, and `--attachment` reject paths outside
the current working directory. This is deliberate: it stops a stale file from
another run or environment being picked up silently. Write the file into the
directory you are working in — **not `/tmp`, not a shared path** — or the
command fails.

```bash
# correct: relative to the working directory
multica issue comment add <issue-id> --parent <comment-id> --content-file ./reply.md
```

`--allow-external-file` overrides the check. Use it only when the user pointed
at that specific outside path, never to work around a failure you did not
diagnose.

### Issue Comments

For agent-authored comments, always write the body to a UTF-8 file and pass it
with `--content-file`. Do not use inline `--content` for structured comments:
shells can rewrite backticks, `$()` expressions, variables, quotes, and
newlines before the CLI receives them.

```bash
# Create reply.md with real newlines first, then:
multica issue comment add <issue-id> --parent <comment-id> --content-file ./reply.md
rm ./reply.md
```

`--parent` is conditional, not universal. When a comment triggered your task it
is **required** — the server rejects a top-level comment from such a task — and
its value must be the comment you are answering. When you are starting a new
top-level discussion on an issue, omit it. Never attach a reply to an unrelated
thread just to satisfy the flag.

Do not write literal `\n` escapes to fake line breaks.

### Issues and Metadata

Use files for long issue descriptions:

```bash
multica issue create --title "..." --description-file ./description.md
multica issue update <issue-id> --description-file ./description.md
```

`issue create` rejects a new issue when an active duplicate exists. Do not
reflexively retry with `--allow-duplicate` — read the existing issue first and
confirm the user really wants a second one.

Metadata is durable issue state, not a log. Read it on entry, but only write
high-signal facts future runs will re-read, such as `pr_url`, `pr_number`,
`pipeline_status`, `deploy_url`, `external_issue_url`, `waiting_on`,
`blocked_reason`, or `decision`.

```bash
multica issue metadata set <issue-id> --key pr_url --value <url>
multica issue metadata delete <issue-id> --key stale_key
```

Metadata is free-form per-issue KV. Custom **properties** are different: they
are workspace-defined typed fields, shared across issues, and creating or
archiving a definition is an admin-level change — set values, but leave the
definitions alone unless asked.

## Suppressing Agent Runs with `--no-start`

By default, `issue status`, `issue assign`, and `issue update` can enqueue a
fresh agent run — that is how work gets handed off. When you are only recording
ownership or progress for work that is **already underway**, that extra run is
wasted money and a duplicate worker.

```bash
multica issue status <id> in_progress --no-start
multica issue assign <id> --to <name> --no-start
multica issue update <id> --status in_review --no-start
```

Rule of thumb: handing fresh work to someone → omit it; writing down what is
already happening → pass `--no-start`.

## Mention Side Effects

Mention links are actions, not decoration:

```text
[@Name](mention://agent/<agent-id>)     # enqueues that agent
[@Name](mention://squad/<squad-id>)     # enqueues the squad leader
[@Name](mention://member/<user-id>)     # NOTIFIES that person
[@all](mention://all/all)               # broadcasts to the workspace
[MUL-123](mention://issue/<issue-id>)   # renders an issue link
[Name](mention://project/<project-id>)  # renders a project link
```

Three of these reach someone. `agent` and `squad` enqueue agent work that costs
money; `member` notifies a human, and `@all` notifies the whole workspace. Only
`issue` and `project` are inert links you can use freely.

Look up real UUIDs with JSON output before constructing mentions:

```bash
multica agent list --output json
multica squad list --output json
multica workspace member list --output json
```

Do not mention an agent just to thank, acknowledge, or sign off. Re-mentioning
an agent in a reply can trigger another run and create loops. The same restraint
applies to people: mention a member when they need to act, not to be polite.

## Status and Assignment Side Effects

Status changes are not cosmetic. They can enqueue or stop work.

- `backlog` parks an agent-assigned issue.
- Moving `backlog` to `todo` or another active status can enqueue the assignee.
- `done` and `cancelled` are terminal states.
- `in_review` is useful while a PR or human review is pending, but it is still a
  write.
- Any of these can be recorded without starting a run — see `--no-start` above.

When creating sub-issues for ordered work, use stages and `backlog` for later
steps. The parent assignee is woken only when every sub-issue in a stage
finishes:

```bash
multica issue create --title "Research" --parent <id> --assignee <agent> --stage 1 --status todo
multica issue create --title "Build" --parent <id> --assignee <agent> --stage 2 --status backlog
multica issue children <id> --output json
```

## Inspecting Runs

When an issue looks stuck or a result is confusing, read the execution history
instead of guessing from comments.

```bash
multica issue runs <issue-id> --output json                       # what ran, and how it ended
multica issue run-messages <task-id> --issue <issue-id> --output json  # what that run actually did
multica issue usage <issue-id> --output json                      # aggregated token cost
```

`--issue` lets you pass a short task-id prefix instead of the full UUID.

Two controls are genuinely disruptive — confirm both with the user first:

```bash
multica issue rerun <id> --output json          # re-enqueue the current assignment as a new task
multica issue cancel-task <task-id> --issue <issue-id>   # interrupt a running agent mid-flight
```

`cancel-task` interrupts an in-flight agent, so work in progress is lost. Never
run it to "clean up" state you have not read.

## Pull Requests

When code changes are made for a Multica issue, include the routable issue key
in the PR title, body, or branch so Multica can link it.

```text
MUL-123: fix login redirect
```

Use close intent only when merging the PR should close the issue:

```text
Closes MUL-123
Fixes MUL-123
Resolves MUL-123
```

Read linked PR state from Multica rather than guessing from GitHub search or
metadata:

```bash
multica issue pull-requests <issue-id> --output json
```

## When the CLI Cannot Do It

The CLI does not cover every Multica surface. When the command you need does not
exist, say so plainly, name the step, and point the user at Multica Web to
finish it. Never let a partial run read as a completed one, and never reach for
`curl` or a private HTTP API to close the gap.

Report what actually happened: which commands ran, which succeeded, and what is
left for the user. A refused or failed command is a result to report, not a
problem to route around.

## External Agent Boundaries

External agents do not receive Multica runtime context automatically. If the
user asks for work on a specific issue or comment, require or derive:

- issue id or issue key
- trigger comment id and parent thread, if replying
- intended workspace/profile, if more than one is configured
- whether writes are allowed
- whether mentions, status changes, reruns, or assignments are allowed

If any of these are missing and the operation would write state, ask before
proceeding. For read-only investigation, gather context with JSON output and
report what else is needed.
