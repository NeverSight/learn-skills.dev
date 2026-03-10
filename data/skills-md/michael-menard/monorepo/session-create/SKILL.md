---
name: session-create
description: Open a new context session at the start of a leader agent workflow. Records agentName, storyId, and phase in wint.contextSessions, emitting a structured SESSION CREATED block for downstream workers to inherit.
mcp_tools_available: [mcp__postgres-knowledgebase__sessionCreate]
---

# /session-create - Open a Context Session

## Description

Opens a new context session at the beginning of a leader agent's workflow. The session record tracks token usage, agent identity, and story context across multi-agent workflows. Workers inherit this session via the companion `session-inherit` skill.

Session tracking is **telemetry** — it must never gate or block a workflow. If the session cannot be created (DB unavailable, null return), the leader emits a warning and continues normally.

## Usage

```
/session-create                                      # called at start of leader workflow
/session-create storyId=WINT-1234 phase=execute      # with story and phase context
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `agentName` | Yes | _(current agent name)_ | The name of the leader agent opening the session |
| `storyId` | No | null | Story ID for this workflow (e.g. `WINT-1234`) |
| `phase` | No | null | Current workflow phase (e.g. `execute`, `plan`, `qa`) |
| `sessionId` | No | _(auto-generated UUID)_ | Override the session UUID (rarely needed) |

## What It Does

This skill:
1. Calls `mcp__postgres-knowledgebase__sessionCreate` with `agentName`, `storyId`, and `phase`
2. Records the returned `session_id` and emits the structured `SESSION CREATED` output block
3. Handles null returns (DB error) gracefully — emits `SESSION UNAVAILABLE` and continues

## Execution Steps

### Step 1: Invoke sessionCreate

Call the MCP tool with required and optional fields:

```javascript
const result = await mcp__postgres_knowledgebase__sessionCreate({
  agentName: 'dev-execute-leader',   // required — name of THIS agent
  storyId: 'WINT-2090',              // optional
  phase: 'execute',                  // optional
  // sessionId: crypto.randomUUID()  // omit to auto-generate
})
```

**SessionCreateInput fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `agentName` | string (min 1) | Yes | Name of the leader agent |
| `sessionId` | UUID string | No | Auto-generated if omitted |
| `storyId` | string \| null | No | Story identifier |
| `phase` | string \| null | No | Workflow phase label |
| `inputTokens` | int >= 0 | No | Default: 0 |
| `outputTokens` | int >= 0 | No | Default: 0 |
| `cachedTokens` | int >= 0 | No | Default: 0 |
| `startedAt` | Date | No | Defaults to now() |

### Step 2: Handle the result

**Success path** — `result` is not null:

```javascript
if (result && result.sessionId) {
  // Emit the structured output block (see Output section below)
}
```

**Null-return path** — DB error or connection failure:

```javascript
if (result === null) {
  // Emit SESSION UNAVAILABLE warning and continue
}
```

### Step 3: Emit structured output

On success, always emit the following block so workers can parse the session ID:

```
SESSION CREATED
  session_id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
  agent:      dev-execute-leader
  story_id:   WINT-2090
  phase:      execute
```

> The `session_id` line must match the regex: `/SESSION CREATED\n\s+session_id:\s+([0-9a-f-]{36})/`

## Output

### Success

After a successful `sessionCreate` call, emit:

```
SESSION CREATED
  session_id: {uuid returned by sessionCreate}
  agent:      {agentName}
  story_id:   {storyId or "—"}
  phase:      {phase or "—"}
```

### Null Return (Graceful Degradation)

If `sessionCreate` returns `null` (DB unavailable or insertion error):

```
SESSION UNAVAILABLE — continuing without session tracking
```

Then continue the workflow normally. Do **not** block, retry, or raise an error. Session tracking is telemetry, not a gate.

## Session Lifecycle

The full session lifecycle across a multi-agent workflow:

1. **Leader opens** — calls `session-create` → `sessionCreate` → emits `SESSION CREATED`
2. **Workers inherit** — each worker calls `session-inherit` → `sessionQuery(activeOnly: true)` → emits `SESSION INHERITED`
3. **Workers update tokens** — call `sessionUpdate({ sessionId, mode: 'incremental', inputTokens, outputTokens })`
4. **Leader closes** — the leader (and ONLY the leader that opened the session) calls `sessionComplete`
5. **Periodic cleanup** — `sessionCleanup({ retentionDays: 90 })` archives old sessions (future: WINT-2100)

> Workers MUST NOT call `sessionComplete`. See the `session-inherit` skill for the full restriction.

## Graceful Degradation

Session tracking is purely telemetry. The following conditions must NOT block the workflow:

| Condition | Behavior |
|-----------|----------|
| DB connection unavailable | Emit `SESSION UNAVAILABLE — continuing without session tracking` and proceed |
| `sessionCreate` returns null | Same as above |
| MCP tool unavailable | Log warning, proceed without session |
| Network timeout | Log warning, proceed without session |

The leader's downstream work (plan execution, file writes, code generation) must continue regardless of session state.

## Examples

### Minimal invocation

```javascript
const session = await mcp__postgres_knowledgebase__sessionCreate({
  agentName: 'dev-execute-leader',
})
// Emits:
// SESSION CREATED
//   session_id: 3fa85f64-5717-4562-b3fc-2c963f66afa6
//   agent:      dev-execute-leader
//   story_id:   —
//   phase:      —
```

### Full invocation with context

```javascript
const session = await mcp__postgres_knowledgebase__sessionCreate({
  agentName: 'dev-execute-leader',
  storyId: 'WINT-2090',
  phase: 'execute',
})
// Emits:
// SESSION CREATED
//   session_id: 3fa85f64-5717-4562-b3fc-2c963f66afa6
//   agent:      dev-execute-leader
//   story_id:   WINT-2090
//   phase:      execute
```

### Null-return path

```javascript
const session = await mcp__postgres_knowledgebase__sessionCreate({
  agentName: 'dev-execute-leader',
  storyId: 'WINT-2090',
  phase: 'execute',
})

if (!session) {
  // Emit:
  // SESSION UNAVAILABLE — continuing without session tracking
  // then continue with the rest of the workflow normally
}
```

## Integration Notes

- The `session_id` from `SESSION CREATED` should be passed to spawned workers via their prompt context so they can call `session-inherit`
- Workers use `sessionQuery({ activeOnly: true, limit: 50 })` and filter client-side — they do NOT receive a `sessionId` filter directly
- The leader is solely responsible for calling `sessionComplete` at the end of its workflow
