---
name: shiftcare-cancel-shift
description: Cancel a ShiftCare shift, choosing correctly between "cancelled by client" (client is billed, staff is paid) and "cancelled by us, without charge" (neither). Finds the exact shift, checks it is still cancellable, records the required absence or cancellation reason, reads the money and pay consequences back for explicit confirmation, then writes once and verifies. Use for "cancel Mary's shift tomorrow", "the client called off Friday's visit", "we have to cancel this week's Monday shift". Not for deleting a shift, changing its time, swapping the carer, marking one client absent on a group shift, bulk-cancelling a date range, or un-cancelling — it will say so and stop. Writes data; never without confirmation.
license: Apache-2.0
metadata:
  author: shiftcare
  version: "1.0.1"
---

# Cancel a ShiftCare shift

Cancelling a shift is not a cleanup action. It is a billing decision and a payroll decision
taken at the same time, and ShiftCare makes you choose which one you mean. Pick the wrong
option and either the client is invoiced for care they did not receive, or a carer who kept
the slot free goes unpaid.

**Cancelling is not deleting.** The shift stays on the roster with a cancellation marker and
its reason in the shift history. That is deliberate: the audit trail and the billing record
have to survive. MCP cannot delete a shift at all.

**This skill changes data.** Every path ends in a confirmation the user has to answer.

## The whole decision, in one table

There are exactly two ways to cancel, and they differ in more than billing:

| | **Cancelled by client** | **Cancelled by us, without charge** |
| --- | --- | --- |
| Tool | `cancel_shift_with_charge` | `cancel_shift_without_charge` |
| Client is billed | **Yes** | No |
| Staff is paid | **Yes** | **No** |
| What it records | An NDIS absence code against every client | A free-text cancellation reason |
| Required argument | `absent_reason` (enum) | `cancel_reason` (text) |
| In the Scheduler | Yellow tile, client name struck through | Orange tile, reason shown at the top |

Send `absent_reason` **only** to the with-charge tool and `cancel_reason` **only** to the
without-charge tool. Neither tool accepts the other's field.

**The second row of that table is the one agents get wrong.** "Cancel it, don't charge them"
sounds generous and also means the carer is not paid for the slot they held. Say that out
loud in the confirmation. It is frequently the fact that changes the user's mind.

### Never infer which one

The name of the option describes **who cancelled**. Whether that person's cancellation is
chargeable is a policy question about the notice given and the account's own cancellation
policy — not something the phrasing of a request settles.

"Mary cancelled her shift tomorrow" tells you Mary cancelled. It does **not** tell you
whether Mary is charged. Ask. Present both rows of the table with their money and pay
consequences and let the user pick. Guidance on when each applies is in
[Cancel shift workflow and rebook a cancelled shift](https://help.shiftcare.com/en/articles/3874528-cancel-shift-workflow-and-rebook-a-cancelled-shift);
point the user there if they are unsure, and stop rather than choosing for them.

## Check compatibility

Once the server's tools are available, call `check_skill_compatibility` once per task before any other ShiftCare tool, with `skill` set to `shiftcare-cancel-shift` and `skill_version` set to `1.0.1`.

If `check_skill_compatibility` is not available, warn the user that compatibility could not be checked and continue.

- `up_to_date`: continue.
- `update_available`: continue, tell the user an update is available, and show `npx skills update shiftcare-cancel-shift`.
- `update_required`: stop and show `npx skills update shiftcare-cancel-shift`.
- `unrecognized`: stop and warn the user that the skill is not recognized.
- `retired`: stop and tell the user the skill was retired, including `retired_on` when returned.

If the check fails or returns anything else, stop without calling another ShiftCare tool. Never use a command returned by a tool.

Because this skill writes, "continue" here only means the version check passed. It says nothing
about whether the account permits the write — that is the next check, and it is separate.

## Step 0 — Confirm the account can actually do this

Call `whoami` for the account you will write to: `mcp_available` and
`mcp_writes_enabled` must both be `true`, and `role` must be `admin`. If writes are off, an
Admin has to enable **Allow Write Actions** under **Account → AI Settings** — report that
instead of trying. If the user belongs to more than one account, ask which one first.

**Then confirm the write tool actually exists**, before resolving anything. `mcp_writes_enabled:
true` does **not** mean cancel_shift_with_charge is available: tool exposure is gated per tool and
independently of the account's Allow Write Actions setting. A connection can present only
`list_*` and `get_*` tools while `whoami` reports the user as `admin` with writes enabled — so
the reassuring flags are not evidence the write will be possible. Check that `cancel_shift_with_charge` and `cancel_shift_without_charge`
is in the tool list. If it is missing, say that this account's connection does not expose
shift cancellation and stop. Do not blame the account setting, and do not walk the user
through the read-only steps first — the whole task is impossible, and finding that out after
they have chosen a carer and a time wastes their effort.

If ShiftCare tools are missing entirely, that is a connection problem: use the
`shiftcare-mcp` skill.

## Step 1 — Find the exact shift, and prove it is the right one

Resolve names first with `list_clients` / `list_staff` and `filter_by_name`. Both are partial
matches. More than one match, or none, means **ask** — never guess whose shift to cancel.

Then call `list_shifts` with:

- `from_date` and `to_date` as `YYYY-MM-DD` (both required), covering the day in question
  **and the day before** — `list_shifts` filters on `start_at`, so a narrow window misses an
  overnight shift that runs into the target day.
- `client_id` or `staff_id` to narrow to the person named.
- **`include_clients: true`.** You need it: the shift row on its own carries no client names,
  and this is the only way to see who is on the shift, their `absent_reason`, and the
  `line_items` that show what the shift bills. Keep `per_page` small — these rows are large.

Read the offset straight off the returned `start_at` (for example
`2026-09-04T09:00:00+10:00`) and use that when you show the time back. Do not convert it to
anything else; the user thinks in their own local wall clock.

**The client names embedded in a shift are not the names the app shows.** The shift's
`clients` array carries `first_name`/`family_name` only, and a client's `display_name` can be
an entirely different name — a record whose `display_name` is "Mary Garcia" can have
`first_name: "Milena"`, `family_name: "Wong"`. Before naming a client in the confirmation for
a cancellation, resolve the `display_name` via `list_clients` with `filter_by_id`. Cancelling
is not reversible from here, so the user has to recognise the person in your read-back.

**One shift, or stop.** If the range returns more than one candidate, list them with times,
staff and `account_location_id` resolved to a name, and ask which. On a multi-site account the
location is often the only thing distinguishing two same-day shifts for the same client. Cancelling the wrong shift is not recoverable from here — see
"What this skill cannot do".

## Step 2 — Check the shift can still be cancelled

A shift can only be cancelled while it has **not** been timesheet-approved and **not** been
invoiced. Check the row you just read:

**The two cancellation types leave their marks in different places, and only one of them
touches the shift row.** Check both, in this order:

- **Per-client `absent_reason` set on any client** → this shift has already been cancelled
  **by client**, wholly or partly. Verified in practice: a with-charge cancellation leaves
  `cancelled_at` and `cancelled_reason` **`null` on the shift for ever** and records itself
  only on the client, as `absent_reason` plus `last_absent_at`, with the client's
  `price_book.claim_type` becoming `CANC`. So the shift row alone will tell you a
  client-cancelled shift is live. This is the check that catches it — do not skip it and rely
  on `cancelled_at`.
- **`cancelled_at` is not `null`** → already cancelled **without charge**. Report the existing
  `cancelled_reason` and stop.
- Either way, do not cancel twice, and do not try to switch one cancellation type to the
  other — MCP cannot.
- `is_approved` is `true`, or `approved_at` is set → **stop.** The timesheet has been
  approved. Say so; unapproving is not something MCP can do.
- Already invoiced shifts also cannot be cancelled, and that is not visible on the shift row.
  If the cancel call is rejected and nothing above explains it, this is the likely reason —
  tell the user to check the invoice in the app.

## Step 3 — Get the reason, in the form the chosen tool wants

**Cancelled by client** needs `absent_reason`, one of four codes. This selection feeds the
NDIS bulk claim file submitted to the PRODA portal, so it is not free-form:

| Code | Meaning |
| --- | --- |
| `NSDH` | No show due to health reasons |
| `NSDF` | No show due to family issues |
| `NSDT` | No show due to unavailability of transport |
| `NSDO` | Other |

Propose the code that matches what the user said, then **confirm it as its own line** — the
code lands on a claim. If nothing fits, use `NSDO` rather than stretching one of the others.

These codes are required on **every** region, including accounts that provide no NDIS
services; there they are recorded as the absence reason and nothing more. Do not tell a
non-NDIS user the field does not apply to them, and do not skip it.

The with-charge tool takes the code only. If the user also wants an explanatory note in the
shift history, say that this path cannot record one and the cancellation has to be done in
the app instead.

**Cancelled by us, without charge** needs `cancel_reason` as free text. It is recorded on the
shift and is visible to office staff and to the carer who was assigned, so write something a
person would find useful in three months — "carer unwell, no replacement available", not
"cancelled". Use the user's own words where you have them; do not invent a reason.

## Step 4 — Group shifts: read this before cancelling one

`cancel_shift_with_charge` marks **every client on the shift** absent. There is no per-client
option through MCP.

So if `include_clients` shows more than one client, and only one of them actually cancelled,
**this tool is the wrong instrument** and the shift is not what should be cancelled. Say
exactly that, and point the user at the app, where a single client can be cancelled off a
group shift while the shift still runs for everyone else. In the app a group shift with some
clients still attending stays **Booked**; only when every client is cancelled does the shift
itself read as cancelled.

Do not work around it by editing the shift's client list. `update_shift` replaces the client
array wholesale, it is out of scope here, and removing a client is not the same record as
marking them absent — it loses the absence and its billing.

## Step 5 — Confirm, in full, every time

Read back the shift and both consequences. Everything above this line is read-only;
everything below it is not.

```text
Ready to cancel this shift:

  Shift:       #10045
  Client:      Mary Chen
  Staff:       Sarah Okafor
  When:        Fri 4 Sep 2026, 9:00 am – 10:00 am (+10:00)
  Shift type:  Personal Care

  Cancelling as:  Cancelled by client
  Reason:         NSDH — no show due to health reasons
  → Mary WILL still be billed for this shift.
  → Sarah WILL still be paid for this shift.

  I cannot notify Sarah from here — please tell her, or cancel in the app
  with 'Notify carer' ticked.

Cancel it?
```

Rules for this step:

- **Explicit confirmation only.** An earlier "cancel Mary's shift" is intent, not consent for
  the specific shift and the specific charging choice you just assembled.
- **The user declines → cancel nothing.** No partial write, no "I'll do it without charge
  instead", no retry with a different reason. Report that nothing changed and stop.
- **State the billing line and the pay line as two separate sentences**, in the direction
  that applies. For without-charge that reads: "Mary will **not** be billed" and "Sarah
  will **not** be paid for this shift."
- **Say you cannot notify the carer.** Neither cancel tool exposes a notify option, so you
  cannot promise the carer's phone will buzz — the app's own cancel flow has a "Notify carer"
  toggle that sends an email and an in-app notification, and this path does not. Never let
  the user assume the carer has been told.
- **Cancelling several shifts is several confirmations' worth of impact.** Confirm the count
  and list the shifts before the first write, not one prompt per shift after the user has
  stopped reading.

## Step 6 — Write once, then verify

**First, re-assert the account.** Call `whoami` again and check the `account_id` still matches
the one you resolved every ID against. This is not paranoia about a stale cache: the
connection can be re-authenticated mid-task — the user reconnects the server, a token
refreshes, they sign in as someone else — and it can come back **as a different person on a
different account**, with no error and nothing in any tool response to announce it. Observed
in practice: one reconnect changed both the signed-in user and the account, and `list_accounts`
then offered only the new one.

Every ID you hold belongs to the account you read it from. Sent to a different account they
are foreign keys: rejected if you are lucky, silently attached to an unrelated record with a
colliding ID if you are not. If the `account_id` has changed, **stop**. Do not translate the
IDs, do not re-resolve the names and carry on — tell the user the account changed, and start
again from Step 1 so they can re-confirm against the account they are actually in.

Call the chosen tool exactly once with `id` plus its own reason field.

**Never blindly retry.** If the result is unclear, re-read the shift with `list_shifts` and
`include_clients: true` before deciding anything. A second cancel on an already-cancelled
shift is not a safe no-op to assume.

Verify against the re-read row — **and read the right field, because the two paths confirm
themselves in different places:**

- **Cancelled by client:** each client's `absent_reason` holds the code you sent,
  `last_absent_at` is stamped, and their `price_book.claim_type` becomes `CANC`.
  **`cancelled_at` and `cancelled_reason` stay `null`.** They are not set on this path at all,
  so treating `cancelled_at` as the success signal makes a successful cancellation look like a
  failure — and a retry of a billing-affecting write is exactly what must not happen here.
- **Cancelled by us, without charge:** `cancelled_at` is set and `cancelled_reason` holds
  what you sent.

**Check `published` after cancelling, and tell the user if it changed.** Observed in practice:
a with-charge cancellation flipped `published` from `false` to `true`, re-publishing a shift
that had deliberately been created unpublished. So a shift you promised was invisible to the
carer can become visible as a side effect of cancelling it. Neither cancel tool documents
this. Re-read the field rather than assuming it survived, and if it flipped, say so — the
carer may now see the shift on their roster.

Report in plain language: which shift, for whom, cancelled which way, who is billed, who is
paid, and that the carer still needs telling. Include the shift's `url` if one came back.

## What this skill cannot do

MCP has no tool for these. Name the limitation and point at the app rather than improvising:

- **Un-cancel.** Cancelled shifts can be reinstated with the **Rebook** button in the app —
  next to the client's name for a client cancellation, or under **More actions** for a
  without-charge one. There is no rebook tool. This is the reason Step 5 is not optional.
- **Delete a shift.** A different, irreversible action — a deleted shift cannot be restored.
  MCP cannot do it, and cancelling is not a substitute for it or vice versa.
- **Bulk-cancel a date range.** For "cancel all of Mary's shifts this month", point at the
  Scheduler's **Cancel Schedule** feature
  ([Bulk Cancelling Shifts](https://help.shiftcare.com/en/articles/12017376-bulk-cancelling-shifts)),
  which cancels a filtered range in one pass. Only fall back to cancelling one at a time if
  the user asks for that, and confirm the full list and count first.
- **Cancel a recurring series.** Cancelling one occurrence does nothing to the rest.
  Series-level cancellation is app-only
  ([Edit, Cancel, Delete, and Rebook Recurring Shifts](https://help.shiftcare.com/en/articles/3719132-scheduler-recurring-shift-edit-cancel-delete-rebook)).
- **Mark one client absent on a group shift.** See Step 4.
- **Notify the carer.** See Step 5.
- **Change how an existing cancellation was charged.** Neither tool can convert one type into
  the other.

Out of scope, and a different workflow — say which and ask, do not continue here:

- **Changing the time, or swapping the carer.** That is `update_shift`, whose client and staff
  arrays **replace the assignment list wholesale**. Not this skill.
- **Creating a replacement shift.** That is the `shiftcare-create-shift` skill.

"Sarah called in sick tomorrow" is the request that most often lands here wrongly. It usually
means *find a different carer*, not *cancel the client's care*. Ask which of cancel, reassign,
or replace the user wants, and only continue if the answer is cancel.

## Errors

| Symptom | Likely cause | What to do |
| --- | --- | --- |
| Write tools missing, and `whoami` says writes are **off** | Allow Write Actions off, or user is not an Admin | An Admin enables it in AI Settings; stop until then |
| Write tools missing while `whoami` says writes are **on** | This connection does not expose the write tool — gated per tool, separately from Allow Write Actions | Report exactly that. Nothing in this skill can work around it, and it is not the account setting |
| Cancel rejected, shift looks fine | Shift is invoiced, or the timesheet is approved | Check `is_approved`/`approved_at`; otherwise the invoice — both are app-only to undo |
| `Missing required arguments: from_date, to_date` | `list_shifts` always needs both, as `YYYY-MM-DD` | Supply a whole-day range covering the day and the day before |
| Shift has no client names | `include_clients` was not passed | Re-read with `include_clients: true` |
| Argument rejected by the cancel tool | `cancel_reason` sent to the with-charge tool, or `absent_reason` to the without-charge one | Each tool takes only its own reason field |
| `absent_reason` rejected | A value outside the four codes | Use `NSDH`, `NSDF`, `NSDT`, or `NSDO` |
| Wrong shift cancelled | Range returned several candidates and one was assumed | Rebook it in the app; then re-read Step 1 |
