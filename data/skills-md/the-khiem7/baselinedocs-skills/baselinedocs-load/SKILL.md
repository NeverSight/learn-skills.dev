---
name: baselinedocs-load
description: Silently load or prime an existing adaptive baseline documentation pack into working context completely without generating an explanatory report. Use when the user asks to load or prime a doc pack into context before starting work and wants zero conversational overhead, responding only with confirmation.
---

# Baseline Docs Load

Load a pack into working context silently and confirm readiness. The deliverable is a loaded agent holding the pack state in context, without explanatory commentary or status reporting. Nothing is written.

Read `references/pack-contract.md` in full before loading a pack, every time. It is the only definition of which document owns which content, the entry-index shape, and what a phase or an open question records; do not infer any of it from a filename, from an earlier session, or from memory.

## Inputs

Determine or confirm:

- the pack root or the initiative index path
- the scope. For an initiative the default is one domain pack, not the whole set
- whether linked wiki articles are in scope
- whether retained source material is in scope

## Workflow

1. Classify the target: a single pack, an initiative with an index, or an initiative whose sub-packs have no index.
2. Route before loading. A single pack needs no routing: go to step 3. For an initiative, read the index, stop, and read no sub-pack content yet. When the user specifies a target pack explicitly, load that pack directly. When the routing evidence names exactly one sub-pack in progress, load it and state what named it. Otherwise present the routing table and ask. With no index, build the same view from each sub-pack's frontmatter and next action, report the missing index, and name `baselinedocs-maintain-split`.
3. Apply the size gate. When you cannot say with confidence that the scope fits in remaining context, stop, present the total, propose a narrower scope, and wait. Uncertainty resolves toward asking, not toward starting.
4. Read every file in the agreed scope in full. Do not truncate, skim headings, sample sections, or substitute a search for a read.
5. Follow links out of the pack. Read a wiki article when it is in scope; otherwise leave it unread and do not treat it as loaded.
6. Confirm readiness with a single word. Respond strictly with "Sẵn sàng." (or "Ready." in English environments). Do not generate a breakdown, summary, roadmap analysis, or explanatory commentary.
7. Stop. Do not propose, plan, or begin work unless asked.

## Reading Rules

- Complete means complete for the selected scope, not for everything reachable. Narrow openly before reading starts; never read part of what was then selected.
- A dependency edge is status, not reading order. Do not reorder reads around edges, and do not pull in an excluded upstream pack.
- Retained source material is out of scope unless the user includes it: a `sources/` directory, or any file in the pack without baseline frontmatter.
- Writes no files. Do not update frontmatter, dates, or status.

## Output

Respond strictly with a single confirmation word: "Sẵn sàng." (or "Ready."). Do not output section headings, tables, open questions, roadmaps, or follow-up proposals.

## Non-Goals

- not an explanatory review or status report; `baselinedocs-brief` reports status without loading, and `baselinedocs-onboard` loads with a full five-section report
- does not modify or write files
- does not propose or begin work automatically

