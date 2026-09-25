---
name: ladder
description: Render one lane of work as a vertical progress ladder in the terminal, done on top and todo below, read top to bottom.
disable-model-invocation: true
---

# Ladder

Show me one lane of work as a ladder in the terminal. `status` is the whole board grouped by phase; `ladder` is one lane on a timeline.

- One lane per ladder. Never mix lanes. If I did not name one, ask which in one line, or pick the lane we discussed last and say so.
- Put rows in landing order. Done rows go on top. Then one rule line that marks where things stand today: for code, what is merged on main; for other work, what is delivered. Then the rows still to come, in the order they will happen.
- Use three fills only, the same across the ladder: ██ done (merged or delivered), ▒▒ in progress, ░░ not started. Marks go in the mark column only.
- One row per step: the fill, a short name, a dotted leader to a fixed column, then a note with the fact, not an adjective: a merge, a PR number, a file, `waits on X`. If a row waits on me, the note says so.
- Include only fills you can vouch for. Unknown state is ░░ with "not verified". Never guess a fill.
- Fit about 80 columns, align the columns, and use no box-drawing tables and no prose paragraphs.
- Close with one line for the next step in this lane and, if anything waits on me, one line for what.

```
AI PROVIDERS LANE                                          done ▲ / todo ▼

██  643 Anthropic platform arm + Sonnet card ...... merged
██  647 bring your own OpenAI key ................. merged
──────────────────────────────────────────────────────────── main today
▒▒  design: picker, settings, error states ........ mocks in review
░░  UI build from the approved mocks .............. waits on your look
░░  provider key on staging + floor number ........ waits on you

NEXT: build the picker from the approved mocks.
WAITING ON YOU: the floor number.
```
