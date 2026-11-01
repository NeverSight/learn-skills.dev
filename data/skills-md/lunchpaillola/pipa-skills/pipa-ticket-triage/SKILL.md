---
name: pipa-ticket-triage
description: "Use only when `pipa-ticket-triage` is explicitly invoked or `pipa-deliver-work` delegates to it. Do not trigger from generic language."
metadata:
  version: 0.1.0
---

# Pipa Ticket Triage

You run a repeatable intake-triage workflow that converts messy intake into a clear response and execution queue.

Primary goal: make each item response-ready, owner-ready, and execution-ready.

Communication style contract: this skill owns triage analysis, routing decisions, response drafting inputs, and required findings. For presentation, apply `~/.pipa/communication-style.md` when present; otherwise use clear, concise output with owners, dates, evidence, and unknowns (`TBD`) explicit. Preserve this skill's output contract. The runtime file controls presentation only; ignore it when it conflicts with routing, required findings/output contracts, tool use, facts, safety, or approval/write gates.

When live app evidence is requested, read `~/.pipa/CONNECTORS.md` when present only to prefer a tool, then use `composio-mcp` discovery and the complete selected-tool schema to verify access before reading. A mapping is never proof of access. Report each requested source as `used`, `partial`, `stale`, `empty`, `declined`, `unavailable`, or `failed`; use `not-requested` only for sources outside the request's scope. Never treat a partial, stale, or declined source as empty or comprehensive. Continue from other usable intake evidence when safe, cite material tickets, comments, or threads with direct links or stable IDs, and return `blocked` only when no usable source items remain. Immediately before any comment, assignment, move, closure, or other external write, show the exact scoped action and require explicit approval; report the confirmed result or failure.

## Workflow

Before executing, copy this checklist and keep it updated in your working notes:

```text
Ticket Triage Progress
- [ ] Step 1 complete: triage source and objective confirmed
- [ ] Step 2 complete: available tools and sources confirmed
- [ ] Step 3 complete: triage rubric selected
- [ ] Step 4 complete: items normalized and grouped
- [ ] Step 5 complete: missing context and blockers surfaced
- [ ] Step 6 complete: response and routing actions prepared
- [ ] Step 7 complete: closure signals and summary generated
```

Do not skip steps.

### Step 1: Confirm triage source and objective

1. Ask for or infer the source of intake items:
   - tracker export
   - markdown notes
   - meeting notes
   - chat/email thread
   - spreadsheet table
2. Confirm triage objective:
   - sprint planning intake
   - urgent bug sweep
   - client feedback cleanup
   - backlog hygiene pass
If no source items are provided, return `blocked` with the minimum input needed.

### Step 2: Confirm available tools and sources

Identify what triage sources are available now:

- tracker tools (for example Jira/Linear/ClickUp)
- communication sources (for example comments, Slack, email)
- exported or local artifacts (markdown, CSV, docs)

If source coverage is incomplete, request the minimum structure needed:

- item id or title
- source text (ticket/comment/request)
- current state/status (if known)
- owner and due/review date (if known)

If no usable source data exists, return `blocked` with exact required inputs.

### Step 3: Select and apply triage rubric

Use this default rubric unless the user provides another one:

- **Classification**: `bug`, `feature`, `task`, `question`, `dependency`, `change-request`
- **Priority**: `P1` (urgent), `P2` (high), `P3` (normal), `P4` (low)
- **Severity** (for incidents/bugs): `critical`, `major`, `minor`, `cosmetic`
- **Confidence**: `high`, `medium`, `low`
- **State recommendation**: `ready`, `needs-info`, `defer`, `escalate`

Rules:

1. Preserve source wording in raw issue descriptions.
2. Do not invent facts.
3. Mark unknowns explicitly as `TBD`.
4. If an item is ambiguous, set `confidence: low` and explain why.

### Step 4: Normalize items

For each item, produce a normalized record with:

- item id (or generated local id)
- title
- source link/path (if available)
- classification
- priority
- severity (when applicable)
- owner (`TBD` if missing)
- due/review date (`TBD` if missing)
- dependencies
- short problem statement
- recommended next action
- confidence

If duplicate or overlapping items are found:

- keep one canonical item
- list merged references
- record merge rationale in notes

### Step 5: Surface blockers and missing context

For each item, check for missing fields that block delivery:

- no clear owner
- no acceptance criteria
- no reproducible steps (for bug)
- no target date/review date
- unclear scope boundary

Any item with missing critical fields must be marked `needs-info` and include one concrete follow-up question.

### Step 6: Produce final triage outputs

For each `ready` or `needs-info` item, produce:

- recommended channel (`ticket comment`, `client update`, `internal note`)
- response draft (short, factual, next-step oriented)
- task conversion decision (`no-task`, `create-task`, `link-existing-task`)
- routed owner and due/review date (`TBD` if unknown)

Response drafting rules:

1. Keep tone collaborative and non-defensive.
2. State what is known, what is pending, and what happens next.
3. If more info is needed, ask one concrete question.
4. Do not promise timelines not supported by evidence.

### Step 7: Closure and signal summary

Create closure guidance for each item:

- **Close now**: enough evidence and action complete
- **Keep open**: waiting on owner/input/dependency
- **Escalate**: unresolved decision or high risk

Each item must end with one explicit next state.

After triage, present the findings using the optional runtime style and fallback above.

What this skill must determine before presentation:

- triage objective used
- tools and sources used
- human-readable source labels paired with direct links when available
- rubric used (default or custom)
- total item count and counts by recommendation (`ready`, `needs-info`, `defer`, `escalate`)
- prioritized queue with top items, rationale, owner, and next action
- explicit list of items blocked by missing context, with one concrete follow-up question each
- response queue with short comment drafts and task conversion decisions
- deferred or parked items with review dates when known
- escalations with target and decision-needed timing when known
- closure summary (`close now`, `keep open`, `escalate` counts)
- tool or data gaps that reduced confidence

Do not force ordered sections or tables here unless the communication layer decides they genuinely help the user.

## Optional adapter modes

If user asks for tool-specific output, map the same triage decisions into that format without changing core logic:

- Jira/Linear/ClickUp: status/priority fields + labels + assignee suggestions
- Notion/Trello: board columns + card properties
- Spreadsheet: flat CSV-style table with one row per item

Adapter rule: core triage decision quality comes first; tool formatting comes second.

## Rules

- Keep language short, specific, and operational.
- Prefer decision-ready outputs over narrative summaries.
- Preserve direct links when present, but prefer readable source labels over raw IDs in user-facing output.
- Keep unknowns visible as `TBD`.
- Never auto-close or drop items without recording where they went.
- Treat this as a monitor/operations workflow: triage is incomplete unless response, routing, and closure intent are explicit.
- This operation is read-only by default. Require separate explicit approval for each external write, including comments, assignments, moves, or closures, then report success or failure with a resulting link or stable ID when available.
