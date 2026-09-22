---
name: baselinedocs-brief
description: Report where work stands right now from an existing baseline pack, cheaply, without loading the pack into context. Use when the user asks where things are, which phase is blocked, or what comes next mid-task, and after a context loss or compaction when the current thread may hold work the pack does not yet record.
---

# Baseline Docs Brief

Answer "where are we" from the pack without loading it. This is deliberately a partial read. Nothing is written.

Read `references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

## Inputs

Determine or confirm:

- the pack root or the initiative index path
- the specific question, when the user asked one

## Workflow

1. Resolve the target. For an initiative, read the index and take the pack it marks in progress; ask only when two or more are.
2. Read every document's frontmatter, then the active sections of `roadmap`. Go deeper only for a specific question, and say which one sent you there.
3. Compare the current thread against the pack. Work done or decided in this thread that the pack does not record is the delta.
4. Report position, blockers, the recorded next action verbatim, the delta, and what you read against what you skipped.
5. Stop. Do not plan, implement, or update the pack.

## Rules

- Say that this is not a load. An agent briefed from a fraction of the pack must not answer later questions as though the whole pack were in context. `baselinedocs-onboard` is the load.
- Report what you read and what you skipped, every time. A brief built on a selective read that does not say which parts is where a silent gap starts.
- The pack can be behind the thread. After a compaction the summary in context may hold hours of work that was never written down, so the pack's recorded next action can be stale by exactly that much. Report the delta and name `baselinedocs-save` as the way to close it. Never present a stale next action as current with no delta beside it.
- Reporting a delta is not authority to write it. Do not update the pack, its frontmatter, or its status.
- Quote the recorded next action verbatim. Do not paraphrase it into your own words.
- Report a contradiction; do not resolve it. `baselinedocs-sync-reconcile` owns the repair.
- Do not audit code against the documents. `baselinedocs-audit-drift` owns staleness.

## Output

- where the work stands: current phase, what is blocked and on what
- the recorded next action, quoted verbatim
- the thread delta: what this thread holds that the pack does not, or `none observed`
- what was read, and what was skipped

## Non-Goals

- not a load; `baselinedocs-onboard` reads the pack in full
- not a pack update; `baselinedocs-save` captures the delta
- not a drift audit; `baselinedocs-audit-drift` does that
- not a handoff for another person; the pack is that handoff, read in a fresh thread with `baselinedocs-onboard`
- writes no files
