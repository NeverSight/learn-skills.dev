---
name: shiftcare-create-shift
description: Create a shift in ShiftCare from a plain-language request — one-off or recurring, staffed or vacant. Asks for whatever the request leaves out (client, carer, date and times, whether to publish, whether to notify the carer, and any tasks for the shift). Resolves client and staff names to IDs, discovers the account's own shift types and locations, pins the time to an explicit UTC offset, reads the whole booking back for explicit confirmation, then writes once and verifies. Use for "book a shift for Mary tomorrow 9 to 5 with Sarah", "create a recurring Monday morning shift", "schedule a sleepover this Friday", "add a shift, I'll pick the carer later". Not for cancelling a shift, changing the time of an existing shift, or swapping the carer on one — those are separate workflows this skill will not attempt. Writes data; never without confirmation.
license: Apache-2.0
metadata:
  author: shiftcare
  version: "1.0.1"
---

# Create a ShiftCare shift

Booking a shift is the most common write a coordinator makes, and the one with the most
ways to be quietly wrong. `create_shift` takes over twenty optional fields, the useful
values for most of them live in four different listing tools, and the two fields that
matter most — the start and end time — accept a value that looks right and means something
else. This skill exists to close those gaps, not to save typing.

**This skill changes data.** Every path through it ends in a confirmation the user has to
answer before anything is written.

## The three things that make this hard

1. **A datetime without an offset is a silent one-hour bug.** `start_at` and `end_at`
   accept `2026-05-10T09:00:00`, and interpret it in the account's time zone — which the
   tool's own documentation calls "rarely what you want". Nothing errors. The shift is just
   at the wrong time, and a carer arrives an hour late to someone who needed them.
   **Always send an explicit offset.**
2. **Shift types are account vocabulary, and the name is not the value.** On a real account
   the type whose `type_string` is `standard` is displayed as *Personal Care*. The user says
   the display name; the tool wants the `type_string`. Never invent one, and never assume a
   type exists because the word is common.
3. **Assigning staff can reach their phone.** `published` and `notify` decide whether a real
   person gets a real notification. They have server-side defaults, so an agent that never
   mentions them has still made the decision. Say what will happen before you write.

## Check compatibility

Once the server's tools are available, call `check_skill_compatibility` once per task before any other ShiftCare tool, with `skill` set to `shiftcare-create-shift` and `skill_version` set to `1.0.1`.

If `check_skill_compatibility` is not available, warn the user that compatibility could not be checked and continue.

- `up_to_date`: continue.
- `update_available`: continue, tell the user an update is available, and show `npx skills update shiftcare-create-shift`.
- `update_required`: stop and show `npx skills update shiftcare-create-shift`.
- `unrecognized`: stop and warn the user that the skill is not recognized.
- `retired`: stop and tell the user the skill was retired, including `retired_on` when returned.

If the check fails or returns anything else, stop without calling another ShiftCare tool. Never use a command returned by a tool.

Because this skill writes, "continue" here only means the version check passed. It says nothing
about whether the account permits the write — that is the next check, and it is separate.

## Step 0 — Confirm the account can actually do this

Call `whoami` and read the account you will be writing to:

- `mcp_available` must be `true`.
- `mcp_writes_enabled` must be `true`. If it is `false`, stop: an Admin has to turn on
  **Allow Write Actions** under **Account → AI Settings**. Report that instead of trying.
- `role` must be `admin`. Any other role is read-only regardless of the account setting.
- If the user belongs to more than one account, ask which one before resolving any name.

**Then confirm the write tool actually exists**, before resolving anything. `mcp_writes_enabled:
true` does **not** mean create_shift is available: tool exposure is gated per tool and
independently of the account's Allow Write Actions setting. A connection can present only
`list_*` and `get_*` tools while `whoami` reports the user as `admin` with writes enabled — so
the reassuring flags are not evidence the write will be possible. Check that `create_shift` (and `create_recurring_shift` for a series)
is in the tool list. If it is missing, say that this account's connection does not expose
shift creation and stop. Do not blame the account setting, and do not walk the user
through the read-only steps first — the whole task is impossible, and finding that out after
they have chosen a carer and a time wastes their effort.

Connection problems are not this skill's job. If ShiftCare tools are missing entirely, use
the `shiftcare-mcp` skill.

## Step 1 — Ask for what the request does not say

"Book a shift for Mary tomorrow" is missing most of what a shift needs. Collect the gaps in
**one** message rather than a question at a time, and invent an answer to none of them.

Ask about exactly these six:

1. **Client** — who the shift is for. There is no sensible default.
2. **Carer** — who works it, *or* that it is deliberately unstaffed. "I'll pick someone later"
   is a real answer: it means a vacant shift, not a guess (see Step 5 and Step 6).
3. **When** — the date, the start time and the end time. A date with no times, or a start with
   no end, is not enough; `end_at` is required.
4. **Published** — whether the shift goes onto the carer's roster.
5. **Notify** — whether the carer is told about it.
6. **Tasks** — anything the carer has to do on the shift.

**Ask about `published` and `notify` even though both have server-side defaults.** That is the
point: the defaults are computed from account settings, so leaving them unasked still decides
whether a real person's phone buzzes. Offer them plainly — "should this go on their roster, and
should they be notified?" — and pass whatever the user says explicitly rather than relying on
the default.

**On tasks, ask but promise nothing.** `create_shift` has no `tasks` parameter: shift checklist
tasks cannot be attached over MCP. What it does have is `description`, free text that the carer
reads on the shift. So put what the user tells you there, and say plainly that these are
instructions on the shift rather than tickable checklist items, which have to be added in the
app if they want them tracked.

**Do not ask about care plans.** Care plan goals and tasks attach to a shift automatically from
the client's own plan — nobody chooses them per shift, and no MCP tool can set them. Asking
implies a control that does not exist. Report what the shift inherited afterwards instead, in
Step 9.

Do not ask about anything else *here*. Shift type defaults to `standard`, and allowances,
break time and travel are optional and rarely intended — a wall of questions about them makes
a two-line request feel like a form.

Location and facility are the exception, and they are deliberately not on the list above: you
cannot ask about them yet, because you do not know whether the account has more than one to
choose between. That question is Step 3's, once the listings have told you there is a real
choice to make — asking "which location?" on a single-location account is noise.

## Step 2 — Resolve every name to an ID

Use `list_clients` and `list_staff` with `filter_by_name`. Both are **partial** matches, so
"Sam" matches Samantha and Sammy.

- **Exactly one match** → use it, and keep the name to read back (see below).
- **More than one match** → list them and ask. Never pick the first, the most recent, or the
  closest string. Two people named Mary is the normal case, not an edge case.
- **No match** → say so and stop. Do not widen the search to a shorter fragment and guess;
  the client may be inactive, on another team, or simply not exist.

**Read back the name the account actually shows, not the one you assembled.** For a client
that is `display_name`; for a staff member it is `name`. Do not build a name out of
`first_name` + `family_name`: `filter_by_name` matches `display_name`, and the two can be
completely different people on paper. A real record matching "Mary" has
`display_name: "Mary Garcia"` with `first_name: "Milena"` and `family_name: "Wong"`. Confirm
that booking as "Milena Wong" and the user either rejects a correct shift or, worse, approves
it believing it is for someone else. On staff records `first_name`/`family_name` are often
`null` outright.

**Cap the page size on `list_clients`.** Every client row carries its contacts, teams and
service agreements inline, so a full page is very large. Pass `per_page` 3–10 with a
`filter_by_name`; if the filter is that loose, tighten the filter rather than raising the page.

Listings are permission-scoped. An empty result means "nothing this user can see", which is
not the same as "does not exist" — say it that way.

A shift may legitimately have no staff. If the user has not named a carer ("add a shift next
week, I'll pick the carer"), create it **vacant** by omitting `staff_ids`. Do not choose
someone. Note that recurring series cannot be vacant — see Step 5.

## Step 3 — Learn the account's vocabulary, and settle the location

Call `list_shift_types`. Each row has a `name` (what the user says) and a `type_string` (what
the tool wants). Match the user's words against `name`, send `type_string`.

- No confident match → show the available names and ask. Never pass a `type_string` you did
  not read from this listing.
- The user named no type → omit `shift_type`; it defaults to `standard`. Say so in the
  confirmation, using the display name that account gives `standard`.

**Sleepover is two independent things.** Most accounts have a shift type named *Sleepover*,
and `create_shift` also has a separate `sleepover` boolean that changes pay treatment (often a
fixed rate instead of hourly). Setting the type does not set the flag. For "schedule a
sleepover", propose both and confirm them as two separate lines. `live_in` behaves the same
way for multi-day live-in shifts.

### Always call `list_account_locations`, even when the user said nothing about location

Omitting `account_location_id` does **not** mean the shift has no location. The server falls
back to the account's default location, so a location is always chosen — either by you or
silently for you. Two things follow from that, and the second is the important one:

- **More than one location → ask which.** Show the names and let the user pick. Do not accept
  the default on their behalf: on a multi-location account the default is frequently not the
  one they meant, and a shift filed against the wrong site is wrong for rostering, reporting
  and pay.
- **Exactly one location → use it and say so in the confirmation.** No question needed; there
  is nothing to choose between.
- **`Feature not enabled` → that account does not expose locations.** Carry on without one and
  say so. Nothing is selectable, so there is nothing to ask about.

**Settle the location before you work out the offset**, because the location decides how an
offset-less datetime is read and can decide what the local wall clock even means. An account
with sites in Perth and Melbourne spans two offsets, so "9am" is not one instant until the
location is known. That is why this step comes before Step 4, and why the answer belongs in
the confirmation rather than left implicit.

### Facilities work the same way

Call `list_facilities` too. **More than one → ask which**, or whether the shift belongs to a
facility at all, since a facility is optional in a way a location is not. Exactly one → offer
it rather than assuming it; a single facility on the account does not mean every shift happens
there. None, or the tool unavailable → carry on without one.

`list_allowances` → `allowance_ids`, only if the user asked for allowances.

`address` and `suburb_address` are free text stored on the shift. They do **not** look up or
override `account_location_id` or `facility_id`, and those three IDs are not interchangeable —
a location, a facility and an address are three separate things, and filling one does not
fill the others.

## Step 4 — Get the UTC offset for that location

**The zone you need is the shift's location's zone, not the account's.** Server-side, an
offset-less datetime is parsed in the resolved account location's own time zone, and the
account setting's zone is only the fallback when that location has none. A location resolves
even when no `account_location_id` is sent — the account's default location is used — so on a
multi-location account the zone that interprets your input can differ from the account's own.
This is the reason the explicit offset is not optional: it makes the question moot.

`whoami` may report a `time_zone` for the account as an IANA name. **That is the account
setting's zone — the fallback — so it is not proof of how a datetime will be read.** Use it to
sanity-check, and where the account has one location, or its default location has no zone of
its own, it is the right zone. Do not treat it as authoritative on a multi-location account.

No MCP tool reports a location's zone — `list_account_locations` returns names and addresses
and no zone at all. So having settled *which* location in Step 3, read its offset off an
existing shift there, filtering the result by the `account_location_id` you chose. A shift at
another site can carry a different offset entirely, so an unfiltered sample is not evidence
about your location:

1. Call `list_shifts` with `from_date` and `to_date` (both `YYYY-MM-DD`) spanning a few days
   **around the requested date**.
2. Keep only rows whose `account_location_id` matches the location you settled on. There is no
   location filter on `list_shifts`, so do this yourself.
3. Read the offset from a surviving `start_at`, for example `2026-09-04T09:00:00+10:00` →
   `+10:00`.

Take it from near the target date, not from today. Accounts in daylight-saving regions change
offset mid-year, and a shift booked across the changeover with today's offset is wrong by an
hour in exactly the way this step is meant to prevent.

If nothing survives that filter, **ask the user for the time zone or offset of that
location** — naming the location in the question, so they answer for the right site. Guessing
from the region is not good enough: a single account can have locations in Perth, Queensland,
Melbourne and Hobart, which are three different offsets, and that spread is exactly why
neither the account zone nor another site's shift can answer for this one.

Then build the datetimes from the user's wall-clock time plus that offset:
`"tomorrow 9am to 5pm"` with `+10:00` → `start_at: 2026-09-05T09:00:00+10:00`,
`end_at: 2026-09-05T17:00:00+10:00`.

**If `end_at` is earlier than `start_at` on the same date, stop and ask.** "9pm to 7am" is
either an overnight shift, in which case `end_at` belongs on the next day, or a typo. Never
decide which on the user's behalf.

## Step 5 — Route one-off vs recurring

| Request | Tool |
| --- | --- |
| A single date | `create_shift` |
| "every Monday", "weekly", "every second Tuesday", "monthly on the 3rd" | `create_recurring_shift` |

`create_shift` cannot create a series and `create_recurring_shift` cannot create a one-off.
Pick before you confirm, and confirm the one you picked.

Recurring needs more from the user, and it will not proceed without it:

- `recurrence_unit` (`day` / `week` / `month`) and `recurrence_repeat_every` (1–365).
- `recurrence_week_days` when the unit is `week`, as `["Mon", "Wed"]`.
- `recurrence_day_of_month` when the unit is `month`.
- **`recurrence_end_date` is required.** There is no open-ended series. If the user did not
  give an end date, ask for one — do not invent a horizon.
- **`client_ids` and `staff_ids` are both required.** A recurring series cannot be created
  vacant. If the user has not chosen a carer, say that and offer a one-off shift instead.

`start_at` / `end_at` describe the **first** occurrence and still need an explicit offset.

## Step 6 — Check for clashes, and hand the decision back

For each staff member you are about to assign, call `list_shifts` with `from_date` and
`to_date` covering the shift's date **and the day before**. `list_shifts` filters on
`start_at`, so a window matching the exact shift times misses an earlier-starting or overnight
shift that still overlaps.

Compare the returned `start_at`/`end_at` against the requested window yourself.

**A clash is never yours to resolve.** Do not create over it, do not quietly substitute
another carer, and do not drop the carer to make the problem disappear. Stop, name the
conflicting shift with its time and ID, and offer the three ways forward:

1. **Go ahead anyway.** Sometimes deliberate — a short overlap between two nearby clients, or
   a roster the coordinator intends to sort out by hand. Their call, not yours.
2. **Use a different carer.** Ask who to consider. There is no tool that searches for free
   staff, so you cannot produce a shortlist unprompted: ask for names, or for a team, then
   `list_staff` that team and re-run this step for each candidate. Say that is what you are
   doing rather than appearing to know who is free.
3. **Create it without a carer.** The shift exists, vacant, and someone is assigned later —
   often the right answer when the named carer is genuinely busy. Omit `staff_ids`.
   **Not available for a recurring series**, which requires `staff_ids`; there, offer a
   different carer or a one-off vacant shift instead.

Then re-run this step for whoever they name, and only assemble the confirmation once no
unaddressed clash remains. A clash the user has accepted stays visible in the confirmation as
an accepted one — do not silently drop it once they have said yes.

Leave and availability are not checked by this skill. If the user asks, read them with
`list_leaves` and `list_availability_schedules` before confirming.

## Step 7 — Confirm, in full, every time

Read back every resolved value. Not "shall I create the shift?" — the whole booking, so the
user can catch the resolution that went wrong. Nothing above this line has changed any data;
everything below it does.

```text
Ready to create this shift:

  Client:      Mary Chen (id 12345)
  Staff:       Sarah Okafor (id 67890)
  When:        Fri 5 Sep 2026, 9:00 am – 5:00 pm (+10:00 — Melbourne)
  Shift type:  Personal Care (standard)
  Location:    Melbourne (you chose this; the account has 4)
  Facility:    none — not a facility shift
  Sleepover:   no
  Published:   yes — visible to Sarah on her roster
  Notify:      yes — Sarah gets a notification

  Accepted clash: Sarah already has shift #10098, 4:00 pm – 6:00 pm
  that day. You asked to go ahead anyway.

Create it?
```

Rules for this step:

- **Explicit confirmation only.** An earlier "book me a shift" is intent, not consent for the
  specific booking you just assembled. Wait for an answer to this message.
- **The user declines → create nothing.** No partial write, no "I'll create it unassigned
  instead", no retry with a tweak. Report that nothing was created and stop.
- **Name the location explicitly, and say whether it was chosen or defaulted.** It is never
  absent: it sets the site, and it sets the zone the time was built in. "Location: Default" is
  a real answer worth reading back; silence is not.
- **State `published` and `notify` in plain words**, as above. Both have server-side defaults
  (`published` is computed from the account's Publish Shifts setting and the shift type), so
  if you are leaving them to the default, say which way you expect it to resolve and that the
  account setting decides. If the user wants either one off, pass it explicitly as `false`.
- **For a recurring series**, confirm the pattern and the count you expect:
  "every Monday from 7 Sep to 21 Dec — about 16 shifts".
- **If anything is still unresolved, this message is not confirmation-ready.** Ask the
  question instead. An unaddressed clash counts as unresolved — that question belongs in
  Step 6, not buried in this read-back.

## Step 8 — Write once, then verify

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
again from Step 2 so they can re-confirm against the account they are actually in.

Call the write tool exactly once.

**Never blindly retry a create.** These tools are not idempotent, and an unclear result is
much more likely to be a slow success than a failure. If the outcome is uncertain, read first
with `list_shifts` over that date, then decide.

Verify and report what actually exists:

- **One-off:** read the created shift back and check the stored time is the wall clock the user
  asked for. This is the check that catches a timezone mistake before the carer does — but do
  it with `list_shifts`, not by eyeballing the create response, for two reasons.

  **The create response renders times in UTC, `list_shifts` in the account's offset.** A shift
  created for 9am on 8 September comes back from `create_shift` as
  `2026-09-07T23:00:00Z` — the same instant, a **different calendar date**. Compare that to
  what you sent as text and you will conclude you booked the wrong day and "fix" a correct
  shift. Convert before comparing, or re-read with `list_shifts`, which returns
  `2026-09-08T09:00:00+10:00`.

  **The create response does not confirm the staff assignment.** It comes back with
  `staff: []` and `include_staff: false` even when a carer was assigned successfully. That is
  "not included", not "not assigned" — confirm with `list_shift_staffs` for the new shift ID
  before telling anyone the shift is vacant or re-assigning it.
- **Recurring:** the response carries a `program_id`. The first 20 shifts are created
  synchronously and any remainder follows asynchronously, so call `list_shifts` across the
  series range, filter by that `program_id`, and report the count. If it is short of expected,
  say the rest are still being generated rather than reporting a failure.

Report the shift back in full — not "done", but the record as it now stands: shift ID, the
stored `start_at`/`end_at` with their offset, client, staff, shift type, and the `url`.

**Report `published` and `notify` as the server actually resolved them**, read from the
response, not as you sent them. Where you omitted either, the server computed it from the
account's settings, so the read-back is the only place the real answer exists. "Published:
true — this is on their roster now" is the fact the user needs; "I left it to the default" is
not.

## Step 9 — Tell them what is left to do

A created shift is rarely the finished job, and the next steps are not obvious from the
booking. Offer them, shortest first, and be exact about which you can do and which you
cannot — an offer you cannot honour is worse than no offer.

**What you can do from here, if they want it:**

- **Say whether the shift inherited any care plan work.** Call `list_shift_care_plan_goals`
  and `list_shift_care_plan_tasks` for the new shift ID. These read what the client's care
  plan already puts on this shift, so the worker's app will prompt for it. An **empty result
  is the useful answer**: nothing will be prompted, which for a new client usually means the
  care plan needs attention before the shift runs. Both can also come back empty because you
  cannot see the plans, so say which you cannot rule out.
- **Publish or notify later**, if the confirmation left them off — `update_shift`. Its client
  and staff arrays replace assignments wholesale, so send only the flags.
- **Add a description, break, travel km, or allowances** — also `update_shift`, and
  `list_allowances` to find allowance IDs.
- **Check whether a vacant shift is advertised** — `list_job_board_postings`, filtered by the
  shift ID. Read-only, and **only if that tool is actually in the tool list**: its per-tool
  gate is off on most accounts, so on many connections it is absent entirely. Do not offer
  this without looking first.
- **Record a progress note** — `create_progress_note`, but only once the shift has been
  worked. Do not offer this for a future shift.

**What has to happen in the app — say so plainly, do not offer to try:**

- **Assigning a form to the client or the shift.** MCP is read-only for forms: it can list
  submitted *responses* and nothing else. There is no tool to assign a form, and no tool to
  list the account's forms at all, so you cannot even tell the user which forms exist. Point
  them at the shift in the app.
- **Anything on the Job Board, including advertising a vacant shift.** `create_shift`'s own
  description tells you to post a vacant shift "to the Job Board via
  `create_job_board_posting`" — **that tool does not exist over MCP.** Not gated off: absent,
  with no per-tool flag behind it, so it is not something an Admin can switch on. The read
  side, `list_job_board_postings`, does exist but its gate is off on most accounts, so treat
  the whole Job Board as app-only and check the tool list before offering even the read.
  Never promise a posting.
- **Price book, fund, pay group, per-shift travel billing, and additional charges** such as
  transport or equipment. See below.

If the shift was created vacant, **the outstanding job is assigning a carer**, and that is
the one to lead with.

## What this skill will not do

MCP does not expose these on shift creation. Do not smuggle them into the call — direct the
user to the ShiftCare web app:

- Price book, fund, and pay group selection. These fall back to V3 server-side defaults.
- Per-shift travel billing. It follows each client's own Invoice Travel setting.
- Additional charges such as transport or equipment billed to the client on the shift.

Two consequences worth surfacing, and the create response gives you both:

- **A client with no configured service area produces an unpriced ($0) shift with no error.**
- **The price book is chosen for you, and it may not be a cheap one.** The response's
  `clients[].price_book` and `line_items` carry the name and the hourly rates, so read the
  cost back rather than leaving it invisible: an ordinary 8-hour shift landed on a price book
  at $207.89 per hour including tax — about $1,663 — with nothing in the request naming it.
  Report the price book and the approximate total whenever the shift is billable, and say the
  selection cannot be changed over MCP.

Out of scope for this skill entirely — say so and stop rather than improvising:

- **Cancelling a shift.** Use the `shiftcare-cancel-shift` skill. The two cancel tools differ
  in whether the client is billed *and* whether the carer is paid — a billing decision, not a
  cleanup step.
- **Changing an existing shift, including swapping the carer.** `update_shift`'s client and
  staff arrays **replace the assignment list wholesale** — sending one staff ID removes
  everyone else on the shift. Do not reach for it to "fix" a shift you just created.
- **Editing or deleting a recurring series.** MCP cannot. A wrong series has to be corrected
  in the app, which is the other reason Step 7 is not optional.

"Sarah called in sick tomorrow" is not this skill. It could mean cancel (the
`shiftcare-cancel-shift` skill), reassign, or create a replacement shift. Ask which, and only
continue here if the answer is "create".

## Errors

| Symptom | Likely cause | What to do |
| --- | --- | --- |
| Write tools missing, and `whoami` says writes are **off** | Allow Write Actions off, or user is not an Admin | An Admin enables it in AI Settings; stop until then |
| Write tools missing while `whoami` says writes are **on** | This connection does not expose the write tool — gated per tool, separately from Allow Write Actions | Report exactly that. Nothing in this skill can work around it, and it is not the account setting |
| `Feature not enabled` | That endpoint is not enabled for the account | For `list_account_locations`, continue without a location. For the create tools, stop — the v3 shift create endpoint has to be enabled for the account |
| `Missing required arguments: from_date, to_date` | `list_shifts` always needs both, as `YYYY-MM-DD` | Supply a whole-day range |
| Shift created at the wrong hour | Offset omitted, or taken from the wrong side of a DST change | Read the offset from a shift at that location near the target date (Step 4), and check the stored time in Step 8 |
| Shift type rejected | A `type_string` that is not configured on this account | Re-read `list_shift_types` and ask the user to choose a listed name |
| Recurring create rejected | Missing `recurrence_end_date`, `client_ids`, or `staff_ids` | Ask for the missing piece; none of them have a safe default |
