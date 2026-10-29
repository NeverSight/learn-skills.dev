---
name: run-ai-employee
description: "Use when a human wants to run, trigger, start, or test-run an existing AI employee, e.g. run the recap bot now, kick off the guest responder, or run it once per topic from a list of inputs. Triggers the employee, can dry-run to list required inputs, and hands back task handles without blocking. Load operate-ai-employees first for auth; use monitor-and-review-ai-employee-work to check the result."
metadata:
  version: "2026.10.29-05b8d58"
---

# Run an AI Employee

This starts an existing AI employee working. The work runs in the cloud and takes **minutes**, so this skill is **fire-and-handle**: start it, hand the human the task ID, and let them check back. You do NOT sit in a polling loop.

> Prerequisite: load `operate-ai-employees` first. It sets up the `dozaldevs` CLI and the key. You also need the employee's `slug` (its stable identifier, distinct from `role_name`, which is only the display name). If you don't know the slug, find the employee first (`manage-ai-employees`). A key needs **Member** level or above to run one.

Exact bodies and answers: `dozaldevs run-dozal --help` and `../operate-ai-employees/references/customer-api.md`.

## Trigger

An employee with no inputs needs no data; an empty body is sent for you:

```sh
dozaldevs run-dozal "$SLUG"
```

When it takes inputs, pass them by key, with shell variables in place of the values:

```sh
dozaldevs run-dozal "$SLUG" --data inputs.topic="$TOPIC"
```

- `202` gives a `task_id` and a `status_url`. Keep the `task_id`.
- A `200` with `deduped: true` means the same trigger was already received, so nothing new started.
- Missing required inputs come back as `422 MISSING_REQUIRED_INPUTS` with the list in `missing`. Ask the human for those values and retry.
- `400 MISSING_CONNECTION` means an app the employee needs isn't connected. `402 PAYMENT_REQUIRED` means the account can't run work right now. Tell the human; a person fixes both.

## Check first with a dry run

`--dry_run true` checks the trigger without starting anything. Use it to learn which inputs are required (the `422` lists them), or how many runs a list would start:

```sh
dozaldevs run-dozal "$SLUG" --dry_run true
```

## One run per line

Some employees take a list as one input and start a run for each line. The `202` for those has a `runs` list (one `task_id` per line) and a `failures` list for any line that didn't start. Report each run and each failure to the human. A list over the limit is refused up front with `422 TOO_MANY_ITEMS`, and a dry run returns a `run_count` so you can check first. How an employee gets set up this way is in the "One run per line" section of `../operate-ai-employees/references/customer-api.md`.

```sh
dozaldevs run-dozal "$SLUG" --data inputs.addresses="$ADDRESSES"
```

## What to tell the human (fire-and-handle)

Respond right away, do NOT wait for completion:

> "Started! Your **Weekly Recap Writer** is on it (task `a1b2c3d4`). It usually takes a few minutes. Ask me 'is the recap done?' whenever and I'll check."

Then **stop**. The human controls when to check.

## Checking later

When the human asks if it's done, load `monitor-and-review-ai-employee-work` and make one status call with the `task_id`. If they want to wait for it, that skill covers how.

## Inputs

The keys are defined by the employee. If the human's request implies one ("run the recap for last week"), pass it: `--data inputs.report_date="$REPORT_DATE"`. Unsure which inputs exist? Do a dry run first.
