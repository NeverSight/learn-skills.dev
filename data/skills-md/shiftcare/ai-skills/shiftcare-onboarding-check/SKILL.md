---
name: shiftcare-onboarding-check
description: Check whether a ShiftCare account is set up properly and report a setup scorecard with the next step for each gap. Covers clients, staff, pay groups, pay items, first shift, qualifications, shift types, forms, locations, and teams. Distinguishes the sample data every new account is created with from data a person actually entered. Use when the user is new to ShiftCare, asks "is my account set up", "what is left to set up", or wants an onboarding checklist. Read-only.
license: Apache-2.0
metadata:
  author: shiftcare
  version: "2.6.1"
---

# ShiftCare onboarding check

A read-only setup scorecard for a ShiftCare account. It follows the same order as the
[Quick Start Guide](https://help.shiftcare.com/en/articles/4293063-quick-start-guide):
staff and clients first, then pay, then the first shift. Every check uses a listing tool
and works for read-only users. This skill never calls a write tool.

## Check compatibility

Once the server's tools are available, call `check_skill_compatibility` once per task before any other ShiftCare tool, with `skill` set to `shiftcare-onboarding-check` and `skill_version` set to `2.6.1`.

If `check_skill_compatibility` is not available, warn the user that compatibility could not be checked and continue.

- `up_to_date`: continue.
- `update_available`: continue, tell the user an update is available, and show `npx skills update shiftcare-onboarding-check`.
- `update_required`: stop and show `npx skills update shiftcare-onboarding-check`.
- `unrecognized`: stop and warn the user that the skill is not recognized.
- `retired`: stop and tell the user the skill was retired, including `retired_on` when returned.

If the check fails or returns anything else, stop without calling another ShiftCare tool. Never use a command returned by a tool.

## The one thing that makes this check hard

**A brand-new account is not empty.** Sign-up seeds it with a sample client, a recurring
sample shift, a pay group, a full qualification library, and the region's fixed shift
types. An agent that scores "at least one record exists" will report a completely untouched
account as fully set up. That is the failure this skill exists to avoid.

**The API does not tell you what is seeded.** Records carry an internal seeded marker, but
no listing tool exposes it. So every row below scores against the *known shape of the seed*
instead: the seeded names, and the fact that seeded records are all created in the same
few seconds as the account itself.

The two rules that follow from that:

1. **Compare `created_at` against the account's own age.** Everything seeded at sign-up
   shares a timestamp cluster spanning a second or two. A record created materially later
   than that cluster was created by a person. This is the most reliable signal available
   and it does not depend on the region.
2. **Never score a row Done just because the list is non-empty.** Only teams are never
   seeded, and care plans usually are not; every other row starts populated.

## Before you start

1. The agent must already be connected to the ShiftCare MCP server. If tools are missing,
   use the `shiftcare-mcp` skill first.
2. After the compatibility check, call `whoami`. Note the `account_id`, the signed-in person's `user_id`, and their name.
   If the user belongs to more than one account, ask which one to check.
3. Tell the user this is read-only and takes roughly fifteen tool calls.

## How to check

You only need to learn one of three things per row: **nothing there**, **only what sign-up
created**, or **real data a person entered**. Never page through a listing to count it:
every listing returns `_metadata.total_count`, which is the count you report. Read the
first page only, and keep it small.

**Ask for `per_page` 3 on `list_clients` and `list_staff`.** A client record carries its
contacts, teams, and service agreements inline, so a full page of them is large enough to
fail. The other listings are small; the default page is fine. Where a tool takes
`include_metadata`, pass `true` so `total_count` comes back. Never list every record back
to the user; give the count and name at most three.

### What sign-up creates, everywhere

| Thing | The seeded shape |
| --- | --- |
| Sample client | Display name **Sample**, first name **Freddy**, family name **Mercury**, email `sampleclient<digits>@email.com`, mobile `00000000` |
| Demo client | **Margaret Demo** — present when the care-signals demo content is seeded |
| Sample shifts | A daily recurring program named **Sample Shift** against the sample client, plus a **Care Signals demo shift** where that content is seeded. This yields dozens or hundreds of shifts, so a large shift count means nothing on its own |
| Demo progress notes | Roughly ten notes on the demo client, authored by the registered owner and attached to the Care Signals demo shift, seeded in one burst |
| Owner staff record | The person who registered gets a staff record automatically |
| Pay group | One group named **Default Casual** |
| Pay items | Seven, not four: four named **Weekdays - Mon Tue Wed Thu Fri** carrying `reference_no` **Weekday Day 0/1/2/3**, plus **Saturday**, **Sunday**, **Public Holidays** |
| Price book | **Demo Price Book** — a price book, so it does not appear under pay groups |

Anything outside those shapes was added by a person.

### What sign-up creates differently per region

**The seed is regional.** The sample address, the fixed shift types, and the whole
qualification library differ by country, so the counts and names below are the ones to
compare against — using AU's numbers on a UK account will score a seeded account as
configured.

**The API does not tell you the region.** Neither `whoami` nor `list_accounts` returns a
country. Take it from the ShiftCare MCP server you are connected to (there is one per
region), and confirm it against what you see: the sample address on the seeded client and
shifts, the currency, and the client `type` values.

| | AU / default | UK | US | CA |
| --- | --- | --- | --- | --- |
| Sample address on seeded client and shifts | 512 Harris Street, Ultimo, NSW 2007, Australia | 1 Poultry, London, UK | 124 Oak St, Portland, OR 97204 | 4040 Birch Road, Calgary, AB, T3C 1W1 |
| Seeded qualifications | **67** in 8 categories | **35** in 6 | **59** in 7 | **48** in 7 |
| Fixed shift types (v2) | **13** | **13** | **12** | **12** |
| Fixed shift types (v1, older accounts) | 10 | 10 | 9 | 9 |
| Default client types | Self Managed, Plan Managed, Ndis Managed, Aged Care levels, Sil | Private Pay, Respite, NHS Funded, Local Authority, Direct Payments | Private Pay, Respite, Hospice, Long Term Insurance, Medicaid, Veteran's Affairs | Private Pay, Respite, Hospice, Ndi |

AU, US and CA share one shift-type vocabulary — Personal Care, Respite Care, Domestic
Assistance, Transport, Night Shift, Support coordination, Client Expense, On Call, Recall
To Work, Board and Lodging, Remote Work, 24 Hour Care, with **Sleepover** on AU only.
**UK is a different vocabulary entirely**: Companionship / Sitting / Respite Care, Waking
Night, Sleeping Night (Sleepover), Live-In Care (24-Hour), On-Call / Emergency Visit,
Double-Up Call, Transport / Escort to Appointments, Care Coordination / Care Planning,
Introductory / Assessment Visit, Training / Shadowing Visit, Travel Time / Mileage,
alongside Personal Care and Domestic Assistance. Those UK names look bespoke and are not —
do not read them as evidence someone configured the account.

One timing note for the `created_at` rule: outside AU the seeding runs in the background
after sign-up, so the burst can land seconds or minutes after the account rather than in
the same second. The records still share a tight cluster with each other, which is what
you are matching on.

### The rows

Rows 1–7 are **foundations** — what an account needs before it can be used at all. Rows
8–10 are **follow-through**: whether anyone has actually run a shift through the system end
to end. An account can look fully configured and still have never done real work, which is
the more useful thing to tell the user.

| # | Setup item | Tool | Done when | Still seed data / not done when |
| --- | --- | --- | --- | --- |
| 1 | Clients added | `list_clients` | A client that is not **Sample** / **Freddy Mercury**, not **Margaret Demo**, and was created later than the account's seeding burst | Only the seeded clients, both at the region's sample address |
| 2 | Staff added | `list_staff` | At least **3** staff besides the signed-in person and besides any seeded staff, ideally with a carer `role` | Only the owner's own record. Do not count the signed-in person: that record was created for them at sign-up, not added by them. Match them by `whoami.user_id`, which equals their `list_staff` `id` |
| 3 | Pay groups | `list_pay_groups` | Any group other than **Default Casual**, or the user confirms Default Casual is what they use | Exactly one group named **Default Casual** |
| 4 | Pay items | none; read `pay_items` from the row 3 response | Any item whose `name` is outside the four seeded names, or any item on a second pay group | Seven items under Default Casual carrying the seeded `reference_no` values |
| 5 | Qualifications defined | `list_qualifications` | A qualification created later than the seeding burst, or a count above the region's seeded total | The count equals the region's seeded total and the whole list shares one created-at burst |
| 6 | Shift types | `list_shift_types` | Any type outside the region's fixed list | Exactly the region's fixed list, at its exact count. Expect seed data here on almost every account |
| 7 | Care plans | `list_care_plans` per client, then `list_care_plan_goal_library` | A plan on a client that is not seeded, or any library goal with `provided_by_shiftcare` **false** | Plans only on the seeded client, every library goal `provided_by_shiftcare` true. Empty is common and means **Not done**, not seed |
| 8 | A real shift booked | `list_shifts`, ±90 days, `per_page` 3, `include_clients` true | A shift whose client is not a seeded client and whose address is not the region's sample address | Every shift belongs to a seeded client or sits at the sample address. Ignore the count; the seeded program recurs daily |
| 9 | A shift actually worked | `list_timesheets` first; `list_shift_events` with `shift_ids` from row 8 as the fallback | A timesheet with both `clockin_at` and `clockout_at` set, or a shift carrying events named **start** and **finish** (`offline_clock_in` / `offline_clock_out` count too) | Timesheets exist but no clock times, and shifts carry only `create`, `update`, `notes` events. `list_shifts` with `status: "approved"` is a cheap first pass — it means at least one worker was verified |
| 10 | A shift invoiced | `list_invoices`, then `list_invoiceable_items` for the same period | At least one invoice exists | No invoices. If `list_invoiceable_items` returns a non-zero `estimated_total` while `list_invoices` is empty, say so plainly: there is billable work sitting uninvoiced |
| 11 | Progress notes | `list_progress_notes` | A note on a client that is not seeded, or written by someone other than the owner, or created outside the seeding burst | Around ten notes, all on the seeded demo client, all authored by the registered owner, all sharing one created-at second, all on the Care Signals demo shift |
| 12 | Teams (optional) | `list_teams` | Any team | Never seeded, so zero means genuinely none. Fine to leave empty |
| 13 | Forms | `list_form_responses`, `include_metadata` true, `per_page` 3; plus `list_forms` where that tool is present | A submitted response: it names the `form_id` and `form_name` of a published form somebody built or published **and** filled in. Where `list_forms` exists, a **published** form counts on its own — sign-up clones the template library as **draft**, and `list_forms` returns published forms only, so anything it returns was published by a person. Report an `incident` form separately — submitting one is what opens an incident ticket | No responses visible, and either no `list_forms` or it returns nothing. Both tools absent → **Cannot check** |

**Row 9 matters most, and it has two sources.** Prefer `list_timesheets`: each timesheet
can carry `shift_id`, `status`, `clockin_at`, `clockout_at` and the two clocking locations,
which answers the question directly and covers a whole date range in one call.

**But those six fields are gated by an account feature flag, not by a request parameter.**
There is no `include_clocking_data` argument you can pass — the API decides. So when a
timesheet comes back with only `staff_id`, `date`, `client_ids` and `items`, that means the
flag is off for the account, **not that nobody clocked in**. Never read their absence as a
negative. Fall back to `list_shift_events` and look for events named `start` and `finish`;
it needs `shift_id` or `shift_ids` — there is no account-wide listing — so pass up to 20
ids from row 8. If neither source can answer, this row is **Cannot check**, which drops its
15 points out of the denominator rather than scoring zero.

Also note a timesheet exists for every rostered shift whether or not anyone turned up, so
the timesheet count alone says nothing.

**Row 10.** `list_invoiceable_items` needs a start and end date in the account time zone
and answers "what could be billed", which is the useful contrast when no invoices exist.

**Row 11 has two traps.** `list_progress_notes` requires both `time_zone` and
`created_from`, and **rejects a `created_from` more than 90 days ago** — so it only ever
sees notes *created* in the last 90 days. On an older account real notes can exist and not
appear, so a zero result is "none in the last 90 days", never "none". The tool is also
named `list_client_notes` on some servers; use whichever is present. Customers call these
progress notes, shift notes, client notes or communications, and **in the US usually care
notes** — mirror the user's own word back in the report.

**Row 13 has two sources, and the tool list decides which you have.** `list_form_responses`
is the one most servers expose: each row carries `form_id`, `form_name`, `responder_type` and
`status`, so one response proves a published form exists and has been used — that is the
follow-through signal, and the strongest Done. `list_forms` lists the definitions themselves
and is exposed on fewer servers; where you have it, send `form_type` explicitly — `general`,
then `incident` — because the unfiltered list also returns types no filter can select, and the
template library comes back mixed in with real forms with nothing to tell them apart. A
published template still counts: someone chose to publish it. `get_form` reads one form's
questions and is not needed here.

Two scoping traps make an empty result weak evidence. Responses to a form with **Private
Responses** on — the default for a new form — are visible only to an admin, so a coordinator
credential can see none of them. And form visibility runs through the account's Manage Forms
policy. Report "no submissions visible to this credential" rather than "no forms", and when
`list_forms` is absent say plainly that a published form nobody has filled in yet would not
show.

**Incidents are a capability, not a milestone.** `list_incidents` works, and zero incidents
is a good sign rather than a gap — never score it and never put it under "Remaining", which
would read as "go and have an incident". But do surface it: most new accounts do not know
incident reporting exists. It belongs in "Worth knowing about" below, phrased as a
capability they have not needed yet.

Name matching is a heuristic. If a client looks seeded but the user may have renamed it, or
looks real but oddly named, ask — "Is this a real client, or the sample one sign-up
created?" — rather than deciding for them.

If a tool returns an error or "not found", report that row as **Cannot check**, not as
**Not done**. Some listings are enabled per account.

### Not checkable through this server

Say so plainly instead of guessing:

- **Forms, on a server without `list_forms`.** The tool is gated per server and per account.
  Where it is absent, row 13 is **Cannot check**; ask the user instead of scoring it.
- **Job board.** Sign-up seeds three postings — **Sample Morning Shift**, **Sample
  Afternoon Shift**, **Sample Evening Shift** — at the region's sample address with the
  description "Please add instructions here for your carers". There is a
  `create_job_board_posting` tool but no listing tool on the production servers, so the
  seeded three cannot be told from real ones. Where a `list_job_board_postings` tool does
  exist, note that it returns **unfilled** openings only: a filled posting drops off the
  list, so absence is not evidence nothing was advertised.
- **Action items / coordination tasks.** Seeded by cloning, and exposed by no MCP tool.
  `list_tasks` is a different thing entirely — it lists the scheduled tasks under a care
  plan's goals and requires a `care_plan_id`.
- **Account locations.** Feature-gated per account and not part of the Quick Start path.
- **Price books / client rates.** **Demo Price Book** is created at sign-up. The only clue
  in the API is `pricebook_name` on timesheet items, which is too weak to score.
- **Invoice settings.** See
  [Setting up and customising your invoice settings](https://help.shiftcare.com/en/articles/8491142-setting-up-and-customising-your-invoice-settings).

## Report

This skill is a guided tour as much as an audit. The user is new: half its value is
showing them what ShiftCare can do that they have not discovered, not only scoring what
they skipped. Give four things, in this order: a health score, a checklist split into done
and remaining, a short "Worth knowing about" list, then the next steps.

### 1. Health score

Score each row and total out of 100 — this is the only place a number appears; the
checklist itself carries no per-row points. **Done** scores full, **Partial** half, **Still
seed data** / **Not done** zero. A **Cannot check** row is dropped from both the score and the
denominator — then say the score is out of the reduced total, rather than penalising the
user for a listing they cannot see.

| Row | Weight | Group |
| --- | --- | --- |
| 1 Clients | 10 | Foundations, 55 |
| 2 Staff | 10 | |
| 3 Pay groups | 10 | |
| 4 Pay items | 5 | |
| 5 Qualifications | 5 | |
| 6 Shift types | 5 | |
| 7 Care plans | 10 | |
| 8 Real shift booked | 10 | Follow-through, 40 |
| 9 Shift worked, clocked in and out | 15 | |
| 10 Shift invoiced | 15 | |
| 11 Progress notes | 2 | Extras, 5 |
| 12 Teams | 1 | |
| 13 Forms | 2 | |

Report it as a band with the number alongside:

- **0–20 Not started.** Everything is still the sign-up sample data.
- **21–50 Getting set up.** Real records exist; nothing has been run end to end.
- **51–80 Operating.** Shifts are being worked; part of the loop is still open.
- **81–100 Fully onboarded.**

Follow-through is deliberately worth 40 of the 100. An account that has configured
everything but never worked or invoiced a shift should not score above "Getting set up",
because it has not yet proven the product does its job.

### 2. Checklist

Render it as **one table per group**, in row order, so it reads like a checklist rather
than prose. Use a status glyph in the first column so the eye can scan it:

- ✅ **Done**
- 🟡 **Partly** — real progress, not finished
- ⬜ **To do** — nothing there yet
- 🌱 **Sample only** — what is there came with the account
- ❔ **Can't check** — no tool, or the listing is disabled

Columns: Status, Step, What we found, Try this.

**Do not put point values in the rows.** The weighted score belongs once, at the top, as a
number and a band. Per-row numbers turn a checklist into a mark sheet and read as a
grading. Show group progress as a count of finished steps — "2 of 7 done" — instead.

**Every unfinished row gets a "Try this": one concrete action the user can do next**, in
the imperative, naming the actual thing to create. Not "set up staff" but "Add a carer".
Finished rows get a dash. Use these, adjusted to what the account is missing:

| Step | Try this |
| --- | --- |
| Clients | Add a real client with their address and contact details |
| Staff | Add a new staff member with the **carer** role; and one with the **office / admin** role to help you run the roster |
| Pay groups | Create a pay group for your award, or confirm Default Casual is what you pay — cover every day type, midnight to midnight |
| Pay items | Add pay items so weekdays, Saturday, Sunday and public holidays are all covered with no gap in the hours |
| Qualifications | Mark one qualification as required for all carers — First Aid is the usual first |
| Shift types | Add a shift type your service uses that is not in the standard list |
| Care plans | Create a care plan for a client, with one goal and a recurring task under it |
| Book a real shift | Roster a shift for a real client and assign a carer to it |
| Clock on and off | Have the carer clock in and clock out of that shift on the mobile app |
| Invoice it | Generate an invoice for the shift once it has been worked |
| Progress notes | Write a progress note against a shift — what happened, and any follow-up |
| Teams | Create a team and add staff and clients to it |
| Forms | Publish the incident report template, or a checklist your carers will fill in, from Forms |

**Whenever the report suggests creating a pay group, pay items, or a price book, attach
this note.** It is the most common way a new account ends up with shifts that will not
price or pay:

> Cover all four day types — **weekdays, Saturday, Sunday and public holidays** — and take
> each one from **12am through to 12am**, so the whole 24 hours is accounted for. A shift
> that starts in an hour no pay item covers will not be paid, and the same gap in a price
> book leaves it unbilled. Weekdays are usually split into several bands (overnight,
> daytime, evening, late) — that is fine, as long as the bands join up and run 0 to 24
> between them. The seeded **Default Casual** is the shape to copy: four weekday bands
> covering 0–6, 6–20, 20–22 and 22–24, plus Saturday, Sunday and Public Holidays each
> running the full 0–24.

Keep "What we found" to one short sentence naming the count and the evidence, and always
say when something is sample data rather than absent.

### 3. Worth knowing about

Two to four capabilities the account has not used, that are not scored and are not
failures. Say what each one is for in a sentence, and how they would start. Draw on
whatever the checks turned up as untouched, plus the ones no tool can score:

- **Incident reporting.** Log an incident against a client or shift, assign it, track it to
  resolution, and flag it as NDIS-reportable. Zero incidents is a good thing — worth
  knowing it is there before the first one happens.
- **Job board.** Advertise an unfilled shift to your carers and let them claim it. Sign-up
  leaves three sample postings behind as examples.
- **Forms.** When row 13 found nothing published: the account comes with a set of form
  templates for assessments, checklists and incident reports, ready to publish or adapt.
- **Care plans, progress notes, teams, qualifications** — pull in whichever of these the
  checks showed as untouched, described as a capability rather than a gap.

Keep it short and concrete. This section is the tour, not a feature list.

### 4. Next steps

Only the remaining rows, in Quick Start order, each with its help article:

| Setup item | Next step |
| --- | --- |
| Clients | [Adding and Managing Client Profiles](https://help.shiftcare.com/en/articles/13458486-adding-and-managing-client-profiles) |
| Staff | [Add a Carer or Office User to Your Account](https://help.shiftcare.com/en/articles/3022336-add-a-carer-or-office-user-to-your-account) |
| Pay groups and pay items | [Quick Start Guide](https://help.shiftcare.com/en/articles/4293063-quick-start-guide), Pay Groups section |
| Qualifications and shift types | [Customise categories for staff qualifications, client documents, and shift types](https://help.shiftcare.com/en/articles/4920353-customise-categories-or-types-for-staff-or-client-documents-or-shift-types-compliance-report) |
| Care plans | Build a plan on a real client's profile. See the [Quick Start Guide](https://help.shiftcare.com/en/articles/4293063-quick-start-guide) |
| First shift | [Create a Shift in the Scheduler/Roster](https://help.shiftcare.com/en/articles/3852009-create-a-shift-in-the-scheduler-roster) |
| Clocking on and off | Have a carer clock in and out on the mobile app. See the [Quick Start Guide](https://help.shiftcare.com/en/articles/4293063-quick-start-guide) |
| Invoicing | [Quick Start Guide](https://help.shiftcare.com/en/articles/4293063-quick-start-guide), invoicing section |
| Progress notes | Have a carer write a note against a real shift |
| Teams | [Teams](https://help.shiftcare.com/en/articles/3022481-teams) |
| Forms | [Creating and Managing Custom Forms](https://help.shiftcare.com/en/articles/9382119-creating-and-managing-custom-forms) |

Example of the tone to use:

> **Health: 12 / 100 — Not started.**
>
> You have two clients, but both of them came with the account: "Sample" (Freddy Mercury)
> and "Margaret Demo". All 70 shifts come from the sample recurring shift. Nobody has
> clocked on yet, and there is $343.20 of billable work waiting to be invoiced.

## Offering to fix gaps


The user may ask you to create what is missing. Before agreeing, check `whoami`:
`mcp_writes_enabled` must be `true` and `role` must be `admin`, otherwise explain that an
Admin needs to enable **Allow Write Actions** and point at the help article for the item
instead.

When writes are allowed, treat each fix as a separate task: collect the details, read the
resolved values back to the user (for a shift: client, staff, date, start and end time
with time zone, shift type), and call the write tool only after the user has said yes.
Never batch several writes behind one confirmation.

Keep a running list of what you create — what it was, its name, and the ID the tool
returned — and read it back when the user asks what changed or wants to start over. Offer
to undo what the tools can undo: a shift can be cancelled, a care plan archived. Clients,
staff and pay items have no delete tool, so say so and point at the web app instead of
leaving the user to guess.
