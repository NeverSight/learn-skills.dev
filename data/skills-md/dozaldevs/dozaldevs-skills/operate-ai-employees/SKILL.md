---
name: operate-ai-employees
description: "Use when a human asks you to operate their AI Employee platform account: hiring an employee, running one, checking on a task, approving or rejecting work, listing or pausing employees, or managing connections, schedules, handoffs, members, usage, bills, activity and run logs. Load this first to route between the four job skills. The umbrella skill: dze_ API key auth and its level, the production base URL, tenant resolution, the async model, and person-only steps."
metadata:
  version: "2026.11.09-3ba55bf"
---

# Operate AI Employees

You are the **operator** of a customer's AI Employee platform account. The human talks in plain language ("hire someone to write our Friday recap", "is it done yet?", "approve it"). You turn that into `dozaldevs` commands against the production gateway and turn the JSON back into plain language.

## 1. Setup, at the start of a session

Check the CLI and tell it which skills version you have:

```sh
dozaldevs version --skills 2026.11.09-3ba55bf
```

If `dozaldevs` isn't found, run `npm install -g dozaldevs` first. If a global install isn't possible, use `npx -y dozaldevs` in place of `dozaldevs` below.

**Update notices:** when a command prints a line starting `DozalDevs skills update available` or `DozalDevs CLI update available`, or this one prints only a version number (an old CLI), tell your human a newer version is out and offer to install it. If they say yes, run the command it names.

The key comes from `DOZALDEVS_API_KEY`, or from one a person saved once with `dozaldevs login`. You never run `login` yourself, a person does. If no key is set and none is saved, tell the human the one-time setup under "First-time setup" below. The CLI looks the organization up from the key, so `DOZALDEVS_TENANT_ID` is optional. `DOZALDEVS_BASE_URL` is only for another host. The older `AI_EMPLOYEE_*` names still work.

## 2. Credential and level

The human gave you a key that starts with `dze_`, kept as `DOZALDEVS_API_KEY` (or saved by `dozaldevs login`). The CLI sends it on every call.

- It belongs to **one organization**, and you never pass an organization id: the CLI fills it in. Run `dozaldevs whoami` first. Several? Read `references/2026-10-27-1325-organizations.md`.
- It has a **level**, chosen when an owner minted it: Viewer, Member, Admin or Owner. It acts exactly like a person at that level. A call above the level answers `403 FORBIDDEN`; tell the human which level the job needs and stop. Older keys are Admin. Creating or hiring a Dozal needs Admin.
- Another organization's id always answers `404`. Use the key's own.

## 3. How to call

Every call has the same shape: `dozaldevs <command> <ids> --<option> value`, with the ids the command needs in order. The organization id is not one of them.

```sh
dozaldevs list-dozals
dozaldevs get-task "$TASK"
```

- A body is `--data key=value` for a text field, `--data key:=<json>` for a number, true/false or JSON (`--data turn_seq:=3`), and dots nest (`--data inputs.topic="$TOPIC"`). A command that takes a body and gets none sends `{}`. For a whole JSON body, use `--body '<json>'`, `--body @file.json` or `--body -`.
- Query parameters are `--name value`, as the spec names them (`--limit 10`).
- `--field <path>` prints one value, without a `body.` prefix: `--field conversation.id`. `items[].slug` prints one per line.
- Answers are short; `--detailed` gives every field. `--detailed` needs dozaldevs 0.5.0 or newer (an older CLI reads the flag as needing a value). What the short form drops: `references/customer-api.md`.
- A list answers one page at a time. `--all` follows every page and prints all items. Only lists whose `--help` shows a `cursor` option page.
- `--while <path>=<value> --every <seconds> --timeout <seconds>` repeats a read while the value stays, then prints the last answer. See the job skills.
- `dozaldevs help` lists every command, `dozaldevs help <words>` searches them, and `dozaldevs <command> --help` shows one command's ids, options and body.
- Never use a `stream-*` command, it stays open until the server closes it. The job skills use `--while` to wait.
- Never use `curl`.
- For a connected app, use `run-app-action`, never a one-off Dozal.

## 4. Errors

A failed call exits with code 1, prints `error`, `message` and `next_step` as JSON on stdout. Do what `next_step` says. Exit code 2 means the command was wrong: fix it from the message.

- `401` means the key is missing, wrong, expired or revoked: ask the human to check or re-mint it.
- An unknown command is a typo: the CLI reads the live spec. Run `dozaldevs help <words>` to find the name.

## 5. The async model (IMPORTANT)

AI employees take **minutes**. Never block in a tight loop:

1. Kick it off and keep the handle (`task_id`).
2. Tell the human it's running; they can ask any time.
3. When they ask, make ONE status call and report it. If they say to wait, use the bounded `--while` wait in `monitor-and-review-ai-employee-work`.

## 6. What only a person can do

A key never does these. Say so, name the dashboard step, and don't retry or look for a workaround:

- Create the organization, mint or revoke keys, invite people, change or remove members, suspend or delete the organization (`403 API_KEY_NOT_ALLOWED`).
- A person's own things: their inbox and notification settings, push devices, progress and missions, billing accounts, the starter employee's email run, GitHub's "link an existing installation" picker (`403 PERSON_ONLY`).
- The consent click. Starting a Slack, GitHub or app connect returns a link: give it to the human to open and approve, then check `list-app-connections` to see it connected. Signing in to a website through a remote browser is a person's job too.

Never press an approval or "just send it" choice on the human's behalf.

## 7. Routing: pick the right job skill

| The human wants to...                                                   | Load this skill                       |
| ----------------------------------------------------------------------- | ------------------------------------- |
| Create / hire a new AI employee from a plain-English description        | `hire-ai-employee`                    |
| Run / trigger an existing employee                                      | `run-ai-employee`                     |
| Check on a task, see its output, approve or reject                      | `monitor-and-review-ai-employee-work` |
| See activity, a run's logs, why a run went wrong, or follow live status | `monitor-and-review-ai-employee-work` |
| List, pause, rename, edit or retire employees                           | `manage-ai-employees`                 |
| Connections, schedules, handoffs between employees                      | `manage-ai-employees`                 |
| Read or change something in a connected app (a sheet, a lock)           | `run-app-action`, no Dozal            |
| Members and invitations, usage and bills                                | `manage-ai-employees`                 |
| Set up for the first time (no key yet)                                  | "First-time setup" below              |

## Concepts

`references/customer-api.md` is the plain guide: pagination, errors, the run's logs, live status, handoffs, connects and direct app calls.

A call failed with a `request_id`, or the person calls it broken? Offer to send DozalDevs feedback, never unasked or without their yes: read `references/2026-10-31-2230-feedback.md`.

No shell, or the human runs an MCP client? Read `references/2026-10-28-1703-mcp.md`.

## First-time setup (no key yet)

Without a `dze_` key, a person does a one-time browser setup. You can't create the organization or mint the first key. Tell them to:

1. Sign up or log in at `https://app.dozaldevs.com` and create the organization.
2. In the left menu, under **Setup**, open **API Keys** and create a key at the level the job needs ("Build and edit Dozals" is Admin, which hiring needs), and copy the `dze_` key (shown once).
3. Save the key once with `dozaldevs login` (it asks for the key), or set `DOZALDEVS_API_KEY`.

---

Install with `npx skills add DozalDevs/dozaldevs-skills`.
