---
name: groove-utilities-memory-retrospective
description: "Analyse workflow trends: session ratings, recurring mistakes, and learnings over a period. Use for weekly or monthly reflection."
license: MIT
allowed-tools: Read Glob Bash(git:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-utilities-memory-retrospective

Use $ARGUMENTS to specify period: `week` (default), `month`, or `all`.

## Outcome

A period retrospective is output to the conversation: session rating trend, recurring mistake patterns, top learnings captured, and a short workflow health summary. No files are written.

## Acceptance Criteria

- Session ratings trend shown (if `learned/signals.md` has data)
- Mistake patterns summarised (from resolved incidents in task backend)
- Top learnings listed by topic (from `learned/*.md` dated entries)
- Workflow health summary: one sentence on overall trend
- All output goes to conversation only

## Steps

1. Memory path is always `.groove/memory/`

2. Determine date range from $ARGUMENTS:
   - `week`: last 7 days (today - 7)
   - `month`: last 30 days
   - `all`: all available data
   - Default if absent: `week`

3. **Session ratings** — read `.groove/memory/learned/signals.md` if it exists:
   - Parse table rows matching the date range: `| YYYY-MM-DD | N/5 | context |`
   - Compute: count, average rating, trend (last 3 vs first 3 if enough data)
   - If no data: note "No session ratings recorded yet"

4. **Mistakes** — query the task backend for resolved incidents under "Groove Memory" → "Mistakes":
   - `beans list --parent <mistakes-epic-id> -t bug -s completed` for resolved; `-s in-progress` for open
   - Group by title keywords to identify recurring patterns
   - Count total resolved vs open incidents
   - If no task backend or no data: note "No incidents recorded yet"

5. **Learnings** — glob `.groove/memory/learned/*.md` (exclude `signals.md`):
   - For each file: read and collect dated entries (`## YYYY-MM-DD` headings) within the date range
   - Group by topic (filename stem)
   - Count entries per topic; show the most recent bullet per topic as a sample
   - If no files: note "No learnings captured yet"

6. **Git activity** — run `git log --oneline --since="<start-date>"` to count commits in the period as a proxy for work volume

7. Output retrospective to conversation in this format:

```
## Groove Retrospective — <period> (<start-date> to <today>)

### Session Ratings
<count> sessions rated | avg: <N>/5 | trend: <up/down/flat or n/a>
<sparkline of ratings if ≥3 data points, e.g. ▂▄█▆▇>

### Mistakes
<N> incidents resolved | <N> open
Top patterns:
- <root cause pattern> (N occurrences)
- ...
(No recurring patterns) if all unique

### Learnings
<N total entries across <M> topics>
- patterns (<N> entries): <most recent bullet>
- anti-patterns (<N> entries): <most recent bullet>
- ...

### Workflow Health
<git commits in period> commits | <1-sentence summary of overall trend>
e.g. "Stable week — ratings above 4, one incident (resolved), 3 new patterns captured."
```

## Sparkline generation

Use block characters to render a simple ratings sparkline:
- 1/5 → ▁, 2/5 → ▂, 3/5 → ▄, 4/5 → ▆, 5/5 → █
- Only show if ≥ 3 ratings in the period

## Constraints

- Read only — do not write to any file
- If a data source file is absent, skip that section gracefully with a one-line note
- Parse table rows defensively: skip malformed rows rather than erroring
- Date filtering: match rows where the `YYYY-MM-DD` date falls within the range; skip rows without a valid date
- Output to conversation only — never write to AGENTS.md or memory files
