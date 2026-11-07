---
name: bake-calendar-add
description: "Turn a short bake utterance such as 'bake two for Dana' into one three-day all-day entry on the Google bake calendar, running from the start day through the bake day so overlapping bakes show as stacked bars. The day named is the handoff day, which is the bake day, as in 'bake two for Dana on Tuesday', and the start day is computed two days earlier. A day after 'starting' sets the start day instead, and with no day the start is today. Also removes a bake, deleting its entry, or both entries of an older two-entry bake, as in 'delete the bake for Dana'. Use when the user says to bake some number of loaves for a person, asks to put a bake on the bake calendar, dictates a bake order with a count and a name, or asks to delete, undo or cancel a bake."
---

## Adding a bake to the bake calendar

A bake takes three days.

On the evening of day one the starter is fed.

On day two the dough is mixed, stretched and folded, shaped, and left to ferment overnight.

On day three the loaves are baked and handed off.

So the bake day falls two days after the start day.

A bake is one all-day entry spanning all three days, so a bake that overlaps another shows as a stacked bar.

### Step 1 — parse the utterance

Pull three parameters from the utterance: the loaf count, the person, and a day.

The day the user names is normally the handoff day, the day the baked goods go to the person, which is the bake day.

A day introduced by "start" or "starting" is the start day instead.

With no day named, the start day is today.

Example: "bake two for Dana on Tuesday" is count 2, person dana, bake day Tuesday, so the start day is Sunday.

Example: "bake two for Dana for Tuesday" and "bake two for Dana Tuesday" mean the same as the first example.

Example: "bake two for Dana starting Sunday" is count 2, person dana, start day Sunday, so the bake day is Tuesday.

Example: "bake two for Dana" is count 2, person dana, start day today.

The count may be a digit or a spelled-out number.

The utterance is usually dictated, so it may carry transcription errors, such as "two" heard as "tulos" or "Lowe's loabes".

When a word plainly stands in for the count or for "loaves", read it as that.

Never correct a person's name on a guess; use it as given, and if it looks like a mishearing, say so in the report.

### Step 2 — resolve the dates

A named weekday means the next occurrence of that weekday, counting today if today is that weekday.

"Tomorrow" and a calendar date are fine as days too.

The days run start, middle, bake, so the bake day is the start day plus two days, and the start day is the bake day minus two days.

Never make the user count the two days; compute the other day from the one they gave.

When a bake day was named, the start day is two days before it.

When a start day was named, the bake day is two days after it.

With no day named, the start day is today.

When the start day would fall before today, create the entry anyway and say in the report that the start day has already passed.

### Step 3 — create the entry

Create one all-day event with the Google Calendar create_event tool on the bake calendar.

Bake calendar ID: `f5ba1ec696cefa533636d49aa5809be88a8c7e1c02ae2b31466d56e78ac0ad58@group.calendar.google.com`

If the call fails on that ID, run list_calendars, find the calendar named bake, and retry.

Pass `allDay` as true, with `startTime` at midnight of the start day and `endTime` at midnight of the day after the bake day, no UTC offset.

The end is exclusive, so the event covers the start day, the middle day and the bake day.

For a start day of 2026-10-25, `startTime` is `2026-10-25T00:00:00` and `endTime` is `2026-10-28T00:00:00`.

The title is all lowercase, including the first letter and the person's name:

```
bake <count> loaves for <name>
```

For a count of 1, write `loaf` in place of `loaves`.

Write the count as a digit or word the way the user said it; "two" stays "two".

Give the event a `description`, a bake id that identifies it so it can be removed later:

```
bake:<name>:<start day>
```

The name is lowercase with spaces turned into hyphens, and the start day is `YYYY-MM-DD`, for example `bake:dana:2026-10-25`.

Do not query the calendar first; the entry is added, not deduplicated.

### Step 4 — report

State the start day and the bake day with their weekdays, and the title, in one short line.

Add a line only when it changes what the user would do next, such as a start day already in the past, or a name that looks like a mishearing.

Do not ask for confirmation before creating the entry.

## Removing a bake from the bake calendar

Use this when the user asks to delete, undo, remove or cancel a bake, for example "delete the bake for Dana" or "undo the Dana bake starting Sunday".

A bake is normally one three-day entry.

Bakes created before the three-day format are two single-day entries, a start entry and a bake entry two days later, that share the same bake id.

### Step 1 — find the bake

Pull the person from the utterance, and the start day or bake day if the user gave one.

Call list_events on the bake calendar, one call, from 9 days before today to 60 days after, with `fullText` set to `bake:<name>`.

Group the matches by the bake id in their description.

When nothing matches by id, fall back to events on the bake calendar in the same window whose title ends with `for <name>`.

The fallback covers entries created before bake ids existed.

Pair fallback entries as the start entry and the bake entry two days later.

### Step 2 — pick one bake

When exactly one bake matches, use it.

When the user gave a day, keep only the bake whose start day or bake day matches it.

When several bakes still match, list them as the start day, the count and the name, and ask which one.

When none match, say so and delete nothing.

### Step 3 — delete the entries

Call delete_event on the bake calendar for each event in the matched bake, in one parallel batch.

That is one event for a three-day bake and two events for an older bake.

Do not ask for confirmation once exactly one bake is matched; Google Calendar keeps deleted events in its trash for 30 days.

If an older bake has only one of its two entries, delete it and say that its partner was missing.

### Step 4 — report

Name each deleted title with its dates, one short line each.
