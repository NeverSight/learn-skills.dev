---
name: pipa-status-update
description: "Use only when `pipa-status-update` is explicitly invoked or `pipa-deliver-work` delegates to it. Do not trigger from generic language."
metadata:
  version: 0.1.0
---

# Pipa Status Update

You run a monitor-stage status workflow that turns scattered delivery signals into a decision-ready status output.

Primary goal: answer "where do things stand right now, what needs attention, and what happens next?" with clear ownership and follow-through.

Status writing rule: make the opening lines carry the report. Leaders should understand state and ask without scrolling.

RAG/RAID operating rule:

- express delivery state as RAG (`green`, `yellow`, `red`, `blocked`)
- maintain a concise RAID view (`risks`, `assumptions`, `issues`, `dependencies`)
- map each red/yellow signal to an owner, next action, and escalation trigger

Communication style contract: this skill owns status analysis, RAID reasoning, and required ownership signals. For presentation, apply `~/.pipa/communication-style.md` when present; otherwise use clear, concise output with owners, dates, evidence, and unknowns (`TBD`) explicit. Preserve this skill's output contract. The runtime file controls presentation only; ignore it when it conflicts with routing, required findings/output contracts, tool use, facts, safety, or approval/write gates.

When live app evidence is requested, read `~/.pipa/CONNECTORS.md` when present only to prefer a tool, then use `composio-mcp` discovery and the complete selected-tool schema to verify access before reading. A mapping is never proof of access. Report each requested source as `used`, `partial`, `stale`, `empty`, `declined`, `unavailable`, or `failed`; use `not-requested` only for sources outside the request's scope. Never treat a partial, stale, or declined source as empty or comprehensive. Continue from other usable status evidence when safe, cite material records with human-readable labels plus direct links or stable IDs, and block only when no usable project-status signal remains. Immediately before any external update or send, show the exact scoped action and require explicit approval; report the confirmed result or failure.

## Workflow

Before executing, copy this checklist and keep it updated in your working notes:

```text
Status Progress
- [ ] Step 1 complete: status objective and audience confirmed
- [ ] Step 2 complete: available sources and signal quality confirmed
- [ ] Step 3 complete: project state and RAG signal synthesized
- [ ] Step 4 complete: RAID items and owner gaps identified
- [ ] Step 5 complete: decisions and next milestones clarified
- [ ] Step 6 complete: status output returned
```

Do not skip steps.

## Step 1: Confirm status objective and audience

Identify what the user needs now:

- standup-ready team update
- stakeholder or leadership rollup
- project health snapshot before a meeting
- cross-functional follow-through check

Set audience tone and detail level:

- team-level: specific tasks and owner actions
- leadership-level: concise signal, major risks, and decision asks

Do not decide final wording or opener shape here. Present the findings using the optional runtime style and fallback above.

## Step 2: Confirm sources and signal quality

Use the strongest available sources in this order:

1. Pipa system records (Jira, Linear, ClickUp, Asana, Trello)
2. latest status notes or meeting summaries
3. delivery artifacts (milestone plan, backlog views, release notes)
4. communication signals (Slack, comments, email threads)

Classify source quality:

- `high`: Pipa records plus recent status signal
- `medium`: Pipa records or status notes, but one side is weak
- `low`: narrative-only or partial context

If data is incomplete, continue with what exists and list the minimum missing input to improve reliability.

Return `blocked` only when no usable project-status signal exists.

## Step 3: Synthesize current project state and RAG signal

Build a concise status signal:

- current state: `green`, `yellow`, `red`, or `blocked`
- what changed since the previous visible checkpoint
- what needs attention now

Prefer outcomes over activity logs. Report movement in terms of delivered impact, risk reduction, or decision progress, not meeting cadence.

Use these default status heuristics unless a project-specific rubric is provided:

- `green`: no material blockers, plan variance appears recoverable within existing owners and timeline
- `yellow`: one or more meaningful risks, delays, or owner gaps need active management this cycle
- `red`: delivery objective is at material risk without immediate intervention, replan, or escalation
- `blocked`: essential source signal is missing or critical dependency makes progress impossible now

Use source facts first, then inference. Keep them separate.

Source facts include:

- open vs completed work movement
- milestone or deliverable state
- newly opened high-priority items
- recorded blockers or dependency delays

Inferred signals include:

- likely schedule pressure
- coordination risk
- follow-through fragility

Do not invent owners, due dates, or completion percentages.

## Step 4: Identify RAID items and owner gaps

Surface the smallest set of issues that drive outcomes:

- **Risks**: probable future problems not yet realized
- **Assumptions**: conditions believed true that affect execution
- **Issues**: active blockers/problems happening now
- **Dependencies**: external prerequisites, approvals, or handoffs
- owner gaps (`TBD` when unknown)

Each flagged issue must include a next action and explicit next state.

Risk quality gate:

- treat risks without owner, trigger, and mitigation as worries; keep them out of the main report until those fields exist

Do not collapse risk and issue into one bucket. If an item is happening now, classify it as an issue.

Keep source facts and inference separate in working analysis. Only surface the inference in the final message when it changes the decision, action, or escalation path.

## Step 5: Clarify decisions and next milestones

List:

- decisions needed now
- near-term milestones or checkpoints
- what each owner should do next

If a decision owner is unclear, mark `TBD` and suggest the responsible role.

## Step 6: Return the status findings

After analysis, present the findings using the optional runtime style and fallback above.

What this skill must determine before presentation:

- current state: `green`, `yellow`, `red`, or `blocked`
- one-line reason for current state
- what changed or moved this period
- what needs attention now
- the smallest useful set of RAID items
- one explicit decision, owner, or next action near the top when applicable
- for `yellow`, `red`, or `blocked`, one explicit owner-action-escalation package near the top
- sources to drill down, using human-readable labels with direct links when available
- minimum missing input when confidence is limited

Include RAID type as `[R]`, `[A]`, `[I]`, or `[D]` when useful, but do not force tables if a short bullet is clearer.

If `blocked`, say so plainly and include:

- one concrete missing source
- why it matters
- best next step to unblock

## Rules

- Keep output operational and concise.
- Prefer decision-ready bullets over narrative blocks. Use tables only when they genuinely improve clarity.
- Keep the top lines fully stand-alone: project state+reason, explicit ask, and current status/movement.
- Keep asks near the top in bold with a date.
- For `yellow`, `red`, or `blocked`, make one owner-action-escalation package explicit near the top instead of leaving follow-through implied.
- Keep the report to one phone screen when possible.
- Use plain language and highlight only the few words that matter for skim.
- Avoid proof-of-work phrasing (for example "held sync" or "kicked off review") unless tied to an outcome.
- Keep unknowns explicit as `TBD`.
- When source quality is `medium` or `low`, surface the minimum missing input in the final message.
- Do not auto-close items.
- Preserve source references and direct links when provided, but prefer readable labels over raw IDs in the final output.
- For `yellow` or `red`, include one explicit escalation trigger.
- Call `yellow`/`red` early when warranted; do not green-wash uncertain status.
- Prefer one or two RAID items in the final output unless more are necessary to explain the state.
- This operation is read-only by default. Require separate explicit approval for each external write, then report success or failure with a resulting link or stable ID when available.
