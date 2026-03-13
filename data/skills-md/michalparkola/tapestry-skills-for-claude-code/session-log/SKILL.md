---
name: session-log
description: Summarize the current conversation session and append results to the weekly agent-log. Use when user says "log this", "session log", "summarize this session", or asks to write results to the agent-log.
allowed-tools: Read,Write,Edit,Bash
---

# Session Log

Summarize the current conversation and append to the weekly agent-log file.

## Output Location

`YYYY-wWW Agent Log.md`

Where `YYYY-wWW` is the ISO week of today's date. Calculate with:

```bash
date +%Y-w%V
```

## Format Rules

1. **Reverse chronological order** — newest day on top
2. **One `##` heading per day** — format: `## YYYY-MM-DD`
3. **Bullets, not subheadings** — inside a day, use plain bullet `- Topic title` as topic separator, not `###`. No bold, no formatting on topic lines.
4. **Details as nested bullets** — one sentence per sub-bullet, can nest if needed for details. No bold. Nesting uses a TAB.
5. **CHUNK markers** — if a topic produced a reusable output (a plan, a summary, a framework, a draft message), add nested bullet: `CHUNK: <descriptive title>`
6. **No explanatory text** — no intros, no "in this session we discussed", no meta-commentary
7. **Append, don't replace** — when a day heading already exists, add new bullets under it without removing existing content

## Example

```markdown
## 2026-02-28

- Analiza strategii X vs framework Y + moje obserwacje
  - Strategia jest silna w A i B, słaba w C — brakuje fosy i horyzontu 3+lat.
  - Naming produktu "Rescue" implikuje że kupujący jest ofiarą, co blokuje referencje.
  - Anty-segment nie jest sprawdzalny z zewnątrz — to opis doświadczenia, nie filtr.
  - CHUNK: 3-zdaniowe podsumowanie strategii
  - CHUNK: Scorecard po 6 osiach
- Decyzja: follow-up z klientem
  - Nie wysyłać feedbacku (nie prosił), wysłać link do artykułu jako wartość bez CTA.
```

## Step-by-Step Workflow

### 1. Determine the target file

```bash
WEEK=$(date +%Y-w%V)
```

Target: `${WEEK} agent-log.md`

### 2. Read existing file (if any)

The file may already have entries from earlier sessions this week. Read it first to avoid overwriting.

### 3. Review the full conversation and determine dates

Scan the entire conversation history. Identify:
- **Topics** — distinct subjects discussed (group related back-and-forth into one topic)
- **Decisions** — what was decided or concluded
- **Outputs** — any reusable artifacts (summaries, plans, draft messages, frameworks, scorecards)

**Date attribution:** A conversation may span multiple days. Determine the correct date for each topic using these signals (in priority order):
1. **System reminders** about date changes ("The date has changed. Today's date is now...")
2. **File names** with dates (e.g., `2026-02-26 client email.md` was created/discussed on that date)
3. **Context from session summaries** — if the session was continued from a compacted conversation, the summary may mention which work happened when
4. **Default** — if no date signal exists, use today's date

Group topics by their actual date, not just "today."

### 4. Write the log entry

For each date that has topics:
- If that date's heading (`## YYYY-MM-DD`) already exists in the file, append new topics under it
- If the date heading is not yet in the file, add it in the correct reverse-chronological position
- If the file doesn't exist, create it

**Cross-week dates:** If a topic belongs to a date in a different ISO week than the target file, note this to the user and ask whether to add it to the current file or the correct week's file.

**Condensation rules:**
- Multiple related exchanges → one topic bullet
- Back-and-forth refinement → only the final conclusion matters
- If user edited/corrected something → use the corrected version, ignore earlier drafts

**Append rules:**
- If today's `## YYYY-MM-DD` heading already has bullets, add new ones at the end — never delete or rewrite existing bullets
- If a topic from this session overlaps with an existing bullet, add the new details as additional nested bullets under a new topic bullet — don't merge into existing text

### 5. Confirm

Tell the user what was logged (topic titles only, one line).

## Important Notes

- The user may have a preferred topic title style — if they edited a previous entry, match that style
- Keep bullets ruthlessly short — one sentence, no semicolons chaining multiple thoughts
- CHUNKs reference outputs that exist in the conversation, not in files — they're bookmarks for the user to find later
- Do NOT include the full chunk content in the log — just the marker
- Language: match the language the conversation was conducted in (use the user's language)
