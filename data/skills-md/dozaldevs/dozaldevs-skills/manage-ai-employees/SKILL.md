---
name: manage-ai-employees
description: "Use when a human wants to see, list, pause, reactivate, rename or inspect their existing AI employees (config, status active/paused/draft), or manage connected apps, schedules, handoffs, members and invitations, usage and bills, e.g. what employees do I have, pause the recap bot, how did last Friday go. Not for running one now (run-ai-employee), a task's output, approval or logs (monitor-and-review-ai-employee-work), or creating one (hire-ai-employee). Load operate-ai-employees first."
metadata:
  version: "2026.10.29-05b8d58"
---

# Manage AI Employees

This lists and manages the human's existing AI employees and the account around them.

> Prerequisite: load `operate-ai-employees` first. It sets up the `dozaldevs` CLI and the key, and explains levels, paging and errors.

The CLI fills in the organization for every call. For a command's arguments and body, run `dozaldevs <command> --help`. Error codes and concepts: `../operate-ai-employees/references/customer-api.md`. This file is only the behavior you can't read off the spec.

## List employees

```sh
dozaldevs list-dozals
```

The answer is `{ "items": [...], "page": { "next_cursor", "limit", "has_more" } }`. A list shows one page; add `--all` to get every item. Useful fields:

- `role_name`: the display name (renameable).
- `slug`: the stable identifier `run-ai-employee` needs. It never changes, even after a rename.
- `status`: `active` (live), `paused` (was live, temporarily off), `draft` (saved, never activated), `superseded` (replaced).
- `identity`, `overview`: what it is, in plain language.

Present a friendly roster, not raw JSON: "You have 2 employees: **Weekly Recap Writer** (active, runs Fridays) and **Guest Responder** (active)."

## Pause, reactivate, rename, edit

`update-dozal` takes the archetype UUID from the list (not the name) and needs **Admin**. Pausing keeps its "was live" identity, and a paused employee won't run, even on its schedule. Use `paused` for a live employee, never `draft`.

```sh
dozaldevs update-dozal "$DOZAL" --data status=paused
```

Use `--data status=active` to reactivate; it re-checks connections.

Each content edit bumps the Dozal's `version` and must send the current one as `base_version` (else `400 BASE_VERSION_REQUIRED`):

```sh
dozaldevs list-dozals --id "$DOZAL" --field items[0].version
dozaldevs update-dozal "$DOZAL" --data role_name="$NEW_NAME" --data base_version:="$VERSION"
```

If someone changed it since, `409 VERSION_CONFLICT`: read again and redo your change. Reverts and template updates need `base_version` too; a status-only update needs none. Approving or denying a suggested cleanup needs no version; `409 SUGGESTION_OUT_OF_DATE` means it was withdrawn: re-read, don't retry.

Each save answers `changes`, what really changed; trust it over a re-read. Test an update first: `--validate_only true`. Fields only `update-dozal` changes, seeing what it's told, undoing: `references/checking-and-undoing.md`.

To change what the employee actually does ("make the summary shorter", "also post to Slack"), use the Hiring Dozal's edit chat described in `hire-ai-employee`:

```sh
dozaldevs start-hiring-chat --data kind=edit --data archetype_id="$DOZAL"
```

When the chat shows the finished change (`presented` true, `open_questions` empty), show the human what will change and, on "yes", save it with the chat's current `turn_seq`. Nothing changes on the live employee until then.

```sh
dozaldevs apply-hiring-chat "$CHAT" --data turn_seq:="$TURN_SEQ"
```

`409 VERSION_CONFLICT` on apply means it changed elsewhere: run `restart-hiring-chat` to pick that up.

## Connections

```sh
dozaldevs list-integrations
dozaldevs list-integrations-needing-attention
dozaldevs list-app-connections
```

In order: what's connected, what needs fixing, and apps with their health.

Connecting is two steps and the second is a person's. Start it, which returns a `url`. Give it to the human, who opens it and approves. Then run `list-integrations` to see it connected. Don't claim it worked before you've seen that.

```sh
dozaldevs start-app-connection --toolkit "$APP" --field url
dozaldevs start-slack-install
dozaldevs start-github-install
```

GitHub's "link an installation that already exists" is a person's job (`403 PERSON_ONLY`). Confirm before disconnecting anything, because employees that use it stop working.

## Schedules

```sh
dozaldevs list-schedules
dozaldevs get-dozal-schedule "$DOZAL"
```

In order: scheduled employees with their next run, and one employee's next and last run. To change the timing, edit the employee as above. `run-schedule-now` (it takes the employee's `$SLUG`) makes the next scheduled run start now, and `resume-dozal-schedule` switches a scheduled employee back on after repeated failures paused it. Find out why it failed first (`monitor-and-review-ai-employee-work`).

```sh
dozaldevs run-schedule-now "$SLUG"
dozaldevs resume-dozal-schedule "$DOZAL"
```

## Handoffs

A handoff makes one employee start another when it finishes. `get-handoff-graph` shows the whole workflow, `list-dozal-handoffs` one employee's. Say plainly which employee starts which.

```sh
dozaldevs get-handoff-graph
dozaldevs list-dozal-handoffs "$DOZAL"
dozaldevs create-handoff --data upstream_archetype_id="$UPSTREAM" --data downstream_archetype_id="$DOWNSTREAM"
dozaldevs update-handoff "$HANDOFF" --data status=inactive
dozaldevs delete-handoff "$HANDOFF"
```

`update-handoff` turns one `active` or `inactive`; `delete-handoff` removes it.

## Members and invitations

```sh
dozaldevs list-members
dozaldevs list-invitations
dozaldevs revoke-invitation "$INVITATION"
```

`revoke-invitation` cancels a pending one. A key can't invite anyone or change or remove a member (`403 API_KEY_NOT_ALLOWED`): tell the human to do that in the dashboard.

## Usage and bills

Read only. `get-cost` shows what the organization was charged over a date range (`--from ... --to ...`), `list-run-costs` the runs with what each cost, `get-run-cost` one run, `get-billing` the balance and status. Report figures as given. Paying, buying credits, billing accounts and moving the organization between accounts are a person's (`PERSON_ONLY` or `API_KEY_NOT_ALLOWED`).

```sh
dozaldevs get-cost --from "$FROM" --to "$TO"
dozaldevs list-run-costs --from "$FROM" --to "$TO"
dozaldevs get-run-cost "$TASK"
dozaldevs get-billing
```

## Review recent runs

```sh
dozaldevs list-tasks --limit 10
```

It returns the same `items` and `page` envelope. For one run's output or logs, use `monitor-and-review-ai-employee-work` with its `id`.

## Removing an employee

`delete-dozal` is a recoverable soft-delete. Confirm with the human first. Pausing is usually the better first step.

```sh
dozaldevs delete-dozal "$DOZAL"
```

## Saved setups

`save-org-snapshot` stores the organization's employees, departments, handoffs, rules and knowledge under a `label` as the next version. Sites, connections, secrets, channels, members, keys, templates and billing are not saved and never touched. Needs **Admin**.

```sh
dozaldevs save-org-snapshot --data label="$LABEL"
dozaldevs list-org-snapshots
dozaldevs apply-latest-org-snapshot --data label="$LABEL"
dozaldevs get-org-snapshot-apply "$APPLY"
```

Also `get-org-snapshot`, `delete-org-snapshot` and `apply-org-snapshot` (one version by id). Applying cancels every open run and deletes employees that aren't in the saved setup, so confirm with the human first. It answers `202` with an `apply_id` and runs in the background: poll `get-org-snapshot-apply` until `status` isn't `running`. `partial` means some employees weren't put back (`dozal_outcomes`). `409 APPLY_IN_PROGRESS`: one is already running. `404`: unknown label or id. Warm-up runs, preserved employees and the rest: `references/org-snapshots.md`.
