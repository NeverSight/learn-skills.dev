---
name: daily-report-from-notes
description: Daily report from messy field notes for construction and design work, covering field, records, daily-report. The day's notes are a mix of texts, voice-note reminders and scribbles, and the report needs to be written before you go home — with the facts intact and nothing invented. Use when the user asks for help with daily report from messy field notes, or is working on field, records, daily-report in a construction, engineering or design context. Produces a reviewable draft, never a final answer.
license: CC BY 4.0
section: Site and field operations
tags: field, records, daily-report
updated: 2026-09-24
source: construction-prompts/prompts/07-site-operations/01-daily-report-from-notes.md
---

# Daily report from messy field notes

The day's notes are a mix of texts, voice-note reminders and scribbles, and the report needs to be
written before you go home — with the facts intact and nothing invented.

## Inputs to collect

Ask the user for any of these you do not already have. Never invent project facts, dates,
costs or clause references to fill a gap.

- `{{date}}`
- `{{instructions}}`
- `{{issues}}`
- `{{labour}}`
- `{{plant}}`
- `{{project_name}}`
- `{{safety_observations}}`
- `{{visitors}}`
- `{{weather_and_conditions}}`
- `{{work_completed}}`

## Instructions

```text
You are a site engineer writing today's daily report from my raw notes.

Project: {{project_name}}, report for {{date}}
Weather and site conditions: {{weather_and_conditions}}
Labour on site: {{labour}}
Plant and equipment: {{plant}}
Work completed today: {{work_completed}}
Issues, delays and stoppages: {{issues}}
Instructions received: {{instructions}}
Visitors and inspections: {{visitors}}
Safety observations: {{safety_observations}}

Write the report under these headings: weather and conditions; resources on site; work
carried out; delays and disruption; instructions and communications; visitors and
inspections; safety; outstanding items for tomorrow.

Rules: use only the facts I gave you. Where something is unclear, write [confirm] rather
than filling the gap. Keep the language plain and factual, suitable as a contemporaneous
record. No adjectives about performance and no opinions.
```

## What good output looks like

- No invented detail: unclear items are marked `[confirm]` rather than smoothed over.
- Records delays and instructions precisely, because the daily report is evidence.
- Reads as a factual record, not a story with opinions about how the day went.

## Follow-ups

- "List the items I marked [confirm] as questions to answer before this is filed."
- "Turn the delays section into a chronology with times, ready for the delay file."
- "Summarise this report in three lines for the client's weekly update."

## Guardrails

Daily reports become evidence in delay and defect disputes. Nothing may be added that did not
happen, weather and labour figures must come from real records, and anything that could be read as
an admission or an instruction should be reviewed before it is filed.

---

*Part of the construction agent skills library — CC BY 4.0. Verify anything that leaves your
company: a named person owns every output.*
