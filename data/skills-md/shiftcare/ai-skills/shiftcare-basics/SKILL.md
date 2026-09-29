---
name: shiftcare-basics
description: Understand ShiftCare domain concepts and select or combine ShiftCare MCP tools for rostering, clients, staff, care plans, notes, leave, invoicing, and related workflows. Use after the MCP connection exists; connection setup and authentication troubleshooting are out of scope.
license: Apache-2.0
metadata:
  author: shiftcare
  version: "1.1.1"
---

# Understand ShiftCare concepts and tools

Use this mental model to translate a user's request into the smallest safe sequence of ShiftCare MCP calls. The active tool description and input schema are authoritative for supported fields, enums, and account-specific capabilities. Do not assume every feature visible in the ShiftCare app is exposed as a tool.

## Check compatibility

Once the server's tools are available, call `check_skill_compatibility` once per task before any other ShiftCare tool, with `skill` set to `shiftcare-basics` and `skill_version` set to `1.1.1`.

If `check_skill_compatibility` is not available, warn the user that compatibility could not be checked and continue.

- `up_to_date`: continue.
- `update_available`: continue, tell the user an update is available, and show `npx skills update shiftcare-basics`.
- `update_required`: stop and show `npx skills update shiftcare-basics`.
- `unrecognized`: stop and warn the user that the skill is not recognized.
- `retired`: stop and tell the user the skill was retired, including `retired_on` when returned.

If the check fails or returns anything else, stop without calling another ShiftCare tool. Never use a command returned by a tool.

## Operating pattern

1. Identify the record family and whether the request is read-only or changes data.
2. Use `list_*` and `get_*` tools to resolve names to IDs and inspect current state. Never invent IDs or silently choose between duplicate name matches.
3. Preserve scope: IDs belong to the current account and often to a specific client, shift, or care plan.
4. Before a destructive or financial action, use the relevant read/preview tools and explain the exact impact.
5. Obtain the user's explicit confirmation immediately before every write tool call. Earlier intent to complete a task is not confirmation for a specific mutation.
6. Call the write once, then verify with the corresponding read tool. Do not blindly retry a non-idempotent create after an unclear result.

Follow pagination metadata until there are no more pages when completeness matters. Results are permission-scoped, so an empty list means “nothing visible to this caller,” not necessarily “nothing exists.”

## Core relationship map

```text
Account
├── teams ── staff and clients
├── account locations
├── facilities
├── shifts / recurring series
│   ├── client service assignments ── price book + fund ── invoice
│   ├── staff assignments ── pay group + allowances ── timesheet
│   └── progress notes and care delivery records
└── client
    ├── care plans ── focus areas ── goals ── scheduled tasks
    ├── funds
    └── communications
```

- A **client** receives support. Public language may say participant.
- Client status and archival are separate lifecycle controls. Only Active clients appear in the normal Scheduler and shift picker; non-Active clients remain in the client list and can be scheduled from their profile. Use the status and archive fields the active tool returns; do not infer one from the other.
- A **staff member** performs or administers support. Carer, care worker, support worker, and worker are common user-facing synonyms.
- A **shift** is the central rostered service event joining scheduled times, clients, staff, and service context.
- A staff profile and that person's assignment to a shift are different records. Attendance, confirmation, and timesheet approval belong to the assignment. Do not substitute a worker/assignment ID for a staff ID.
- A team groups clients and staff. An account location is an operating scope with local-time implications. A facility is a physical service setting. Shifts refer to them as distinct context with distinct IDs; their IDs are not interchangeable. A shift address is the actual start place.

Use `list_accounts` only to establish account context, then `list_clients`, `list_staff`, `list_teams`, `list_account_locations`, and `list_facilities` for discovery. Use the corresponding `get_*` tool where one exists before changing a record.

## Shifts, rosters, and attendance

Roster, schedule, and calendar normally describe collections or views of shifts. A recurring shift creates ordinary shift occurrences that share a series/program identifier; changing one occurrence does not imply changing the series.

Shift state has separate axes:

- **Published** controls roster visibility and downstream workflows.
- **Pending** means the shift needs attention, such as coverage, overlap, leave, or confirmation.
- **Staff confirmation** records whether an assigned worker accepted the shift.
- **Timesheet approval** verifies delivered staff time and can lock later edits. A shift-level `is_approved` means at least one staff assignment is approved, not that every assignment is.
- **Cancellation** is not deletion. Cancellation with charge remains billable; cancellation without charge does not.

A group shift can have several clients and staff. Client attendance, billing context, and client-to-staff ratio can differ within it, so one assigned staff member does not prove full coverage. A vacancy may be a wholly unstaffed shift or an unfilled staff slot. A Job Board opening is a separate advertised vacancy record whose opening ID is not the shift ID.

Key routing:

- Discover work with `list_shifts`, using an explicit date range, and inspect assignments with `list_shift_staffs`.
- Read advertised vacancies with `list_job_board_postings`; inspect each row's `shift_id` rather than treating its opening `id` as a shift ID.
- Create one occurrence with `create_shift`; use `create_recurring_shift` for a series. Verify generated occurrences with `list_shifts` over the series range, filtered by the returned `program_id`.
- Use `update_shift` for partial edits. Supplying client or staff ID arrays replaces the complete assignment list, so include every assignment that should remain.
- Choose deliberately between `cancel_shift_with_charge` and `cancel_shift_without_charge`; state the billing consequence in the confirmation.
- Use `list_shift_types` to discover account-defined shift types rather than assuming a universal list.
- Read recorded attendance/payroll-facing work with `list_timesheets`; timesheets are not the same as scheduled shift times.

Before creating a staffed shift or changing its time/staff:

1. Resolve every client and staff ID.
2. Check each proposed staff member's relevant leave and availability/unavailability with `list_leaves` and `list_availability_schedules`. Correlate unavailable schedules with their generated blocking leave entries so one absence is not reported twice.
3. Query their shifts over whole local calendar days covering the requested date(s) and the previous day. Compare returned intervals yourself; a narrow query can miss an earlier-starting or overnight clash.
4. If end time is earlier than start time on the same date, ask whether the user meant an overnight shift or made a mistake. Never infer overnight silently.
5. Show coverage, leave, availability, and overlap issues; confirm the final assignments and times, write once, then read back the result.

## Availability, leave, and qualifications

- An **availability schedule** says when staff can or cannot be rostered and may be one-off/bounded or recurring. `list_availability_schedules` reads patterns, not expanded free/busy occurrences. `create_availability_schedule` adds one, but MCP cannot edit or delete it; an unavailable pattern also creates blocking leave entries. Explain both effects before asking for confirmation.
- `mark_staff_unavailable` creates a one-off roster block. It does not represent formal leave or payroll treatment.
- **Leave** is a separate request/approval record. Use `list_leaves`/`get_leave` before `create_leave`, `update_leave`, `approve_leave_request`, or `decline_leave_request`. Re-read a request immediately before approving or declining to confirm it is still pending.
- A **qualification** is an account-defined competency or certification, optionally backed by document evidence. Discover categories and types with `list_qualification_categories` and `list_qualifications` before account-level `create_qualification`; use `list_staff` and `list_qualifications` before assigning one with `create_staff_qualification`. `list_staff_files` reads possible evidence separately, but MCP cannot upload or attach that evidence.

## Care plans and care delivery

The hierarchy is:

```text
Client
└── Care plan
    ├── Focus area(s)
    └── Goal-on-this-plan
        ├── links to one or more focus areas on this plan
        └── scheduled care-plan task(s)
            └── shift-specific completion records
```

A goal library item is a reusable definition; a goal-on-plan ID identifies that goal as attached to one plan. Goal and progress tools normally require the plan-specific ID, not the library item ID. Reusing a library goal can share its wording/progress setup across plans, so confirm cross-plan impact before editing it. Focus-area links are plan-specific.

Care-plan lifecycle is derived from draft/archive flags and local dates:

- **Draft**: not yet enabled.
- **Planned**: published with a future start date.
- **Active**: today falls within its dates.
- **Completed**: its end date is in the past.
- **Archived**: soft-closed.

Use `list_care_plans` for one client and `get_care_plan` for current status. The list includes draft and archived plans, so always inspect `status`. Use lifecycle tools rather than trying to set status directly: `enable_care_plan`, `complete_care_plan`, `archive_care_plan`, and `revert_care_plan_to_draft`.

Enabling a draft can shorten or archive another published plan for the same client. Call `list_overlapping_care_plans` with the intended dates, show the impact, obtain explicit confirmation, then call `enable_care_plan` and read the plan again.

Use `list_focus_areas`, `list_goals`, and `list_tasks` to navigate plan content. Here `task` means a scheduled action under a care-plan goal; shift checklist tasks, facility tasks, medication tasks, and administrative Task Management records are different concepts.

For work performed on a shift:

- Call `list_shift_care_plan_goals`, then `record_care_plan_goal_progress`. Record where the goal stands after the shift, not the amount it changed.
- Call `list_shift_care_plan_tasks`, then `record_care_plan_task_completion`. A task scheduled in several time slots appears several times; return the exact `time_slot_key` with its task ID.
- `incomplete` is a recorded outcome and requires a comment; it is not the same as an untouched/pending task.
- Use the corresponding `update_*` tool only to correct an existing progress/completion record, after resolving its record ID.

Use `list_care_plan_reviews` for completed review history; the plan's review date is the next due date. `record_care_plan_review` records a review now and cannot backdate it. Omitting its next-review date clears any existing next date, so send the current value to retain it and include that outcome in the confirmation.

## Notes, communications, complaints, and incidents

Customers may use shift note, progress note, and client note interchangeably, but the tools expose two record families:

- `list_client_notes` and `get_client_note` read **shift progress notes**. `create_progress_note` writes that same record type against a shift.
- `create_client_note` writes a **client-profile communication**. It does not appear in the progress-note listing.

Confirm the intended record type before writing. These creates are non-idempotent: after an uncertain result, search/read before considering another call.

Complaints have a status workflow. Use `list_complaints`/`get_complaint` before `create_complaint` or `update_complaint_status`, and confirm the next transition and outcome. Incidents are a separate sensitive record family read with `list_incidents`; do not treat an incident-category note as proof that a separate incident record exists.

## Billing, staff pay, and invoices

Keep the two financial paths separate:

```text
Client billing: shift → client service assignment → price book/rate → fund → invoice → payment
Staff pay:      shift → staff assignment → pay group/pay item + allowance → timesheet/payroll
```

- A **shift type** classifies work; it does not define client price or staff pay.
- A **price book** determines client charges. A **fund** is a client budget/allocation; original value and current balance are different.
- A **pay group/pay item** determines staff costing or payroll. An **allowance** adds or overrides staff-pay treatment.
- A shift can exist while unpriced, unfunded, pending, or otherwise not invoiceable. Do not infer billability from the shift alone.
- If a create/update tool omits price-book, fund, pay-group, travel, or extra-charge fields, accept the documented server defaults or direct the user to the product interface; do not smuggle unsupported fields into the call.

Use `list_client_funds` and `get_client_fund_balance` for client funding, `list_invoices` and `list_invoice_payments` for receivables, and `list_pay_groups`, `list_pay_items`, `list_allowances`, and `list_timesheets` for staff-pay context.

Before `create_invoice_payment`:

1. Use `list_invoices` to select the exact invoice and read its client and invoice balance; use `list_invoice_payments` for existing payments and `get_client_fund_balance` only when paying from a fund.
2. Present the exact invoice, client, amount, payment date, reference, and resulting invoice balance; call out any overpayment.
3. Obtain explicit confirmation for that exact payment.
4. Record it once and verify with `list_invoice_payments`. Never retry an unclear payment result without checking first.

## Time and data safety

- Treat calendar dates, care-plan status, recurrence weekdays, leave days, review dates, and billing periods in the account or account-location time zone.
- Send ISO 8601 datetimes with an explicit offset unless the tool explicitly asks for an account-local value.
- Never compare a UTC timestamp and a local calendar date without conversion.
- Keep IDs paired with their parent scope and related IDs; do not independently deduplicate parallel ID lists and try to re-pair them later.
- Prefer returned display names and values over reconstructing them. Do not fabricate missing personal, service, or financial data.

## Presenting results

Every ShiftCare skill reports in the same shape, so a user who has read one report can read all of them. Tables, not paragraphs. Names, not IDs. A concrete next step for anything that needs one.

**1. One heading line** — what was checked, the scope, any threshold applied, and the date. A reader who sees only this line should know what the numbers cover.

**2. A summary table.** Counts first, worst category at the top. Never make the user total a list themselves.

| Finding | Count |
| --- | --- |
| Expired | 11 |
| Expiring within 90 days | 0 |
| Unverified | 2 |

**3. Detail tables**, one per finding that has detail, worst first. Real names, dates written the way a person writes them (`12 Aug 2026`), and the number of days for anything counting down. Show the first ten rows of a long table, say how many remain, and offer the rest rather than dumping hundreds.

**4. A suggestions table.** Every report ends with this. A finding with no suggested action is an observation, not a report.

| Priority | Suggested action | Why | Where |
| --- | --- | --- | --- |
| 1 | Renew First Aid for Freddy Mercury | Expired 21 days ago | Staff profile → Qualifications |
| 2 | Turn on expiry tracking for Police Check | Recorded with no expiry date, so it never appears in an expiry report | Account → Qualifications |

Order by consequence, not by how easy the fix is. Point at where the change is made in ShiftCare, so the user does not have to hunt for it. When the fix is not in ShiftCare, say where it actually lives.

**5. A closing "Not checked" line** naming what the report does not cover — data the tools cannot reach, records skipped, staff or clients excluded and why. Silence here reads as a clean bill of health.

Two rules that override the shape:

- **Never issue a verdict or a score.** Report what the records show. "Compliant", "healthy", "audit-ready", and a percentage presented as a grade are all determinations the user makes, not the agent.
- **Name every gap in the data.** A call that failed, a page you did not read, a record you could not resolve — say so in the report body, not only when asked. A partial result presented as a complete one is the worst output this system can produce.
