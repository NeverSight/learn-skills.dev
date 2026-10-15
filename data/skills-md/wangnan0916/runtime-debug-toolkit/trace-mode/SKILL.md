---
name: trace-mode
description: Trace runtime behavior and locate responsible code paths with temporary structured logs and NDJSON evidence. Use for runtime handlers, state transitions, and async boundaries. Use debug-mode when the goal includes a product fix. Continue active traces across capture replies.
---

# Trace Mode

This workflow adds temporary logs, analyzes one runtime trace, and locates the responsible code boundary.
It reports evidence without changing product behavior.
The bundled scripts require Node.js 24 or later.

Run this trace loop:

```text
analyze code -> plan events -> arm server -> instrument -> trigger -> analyze logs -> locate code -> clean
```

## 1. Frame the Trace

Start from the user's runtime question or observed behavior.
Read relevant entry points, handlers, state transitions, and existing logs.
Write a Trace Card:

- Runtime question
- Trigger, route, command, input, or fixture
- Candidate code path
- Unknown boundary or state transition
- Observable answer

Record unavailable facts as `unknown`.
Resolve consequential unknowns through code reading or targeted events.

**Complete when:** one candidate path reaches the unknown boundary, and the trace has one observable answer.

## 2. Plan the Events

Read [`references/probes.md`](references/probes.md) before editing instrumentation.
Plan two to eight low-volume events around the disputed boundary.
Each event must distinguish a path, transition, or relevant value.

**Complete when:** every unknown has a named event and an expected record condition.

## 3. Arm the Server

Read [`references/collector.md`](references/collector.md) before running a server command.
Select its startup permission path from the execution environment's declared sandbox limits.
Use the safe wrapper unless the user supplied a complete healthy server contract.
For a phone or remote producer that cannot reach loopback, use the Cloudflare
Quick Tunnel branch in that reference.
Capture every printed value.

**Complete when:** `LOG_SERVER_URL`, `SESSION_ID`, `LOG_DIR`, `LOG_FILE`, and `HEALTH_URL` are known.

## 4. Instrument the Path

Add the planned events using the generic helpers or an equivalent runtime client.
Wrap every helper and event in the required session markers.
Inspect every payload field against the privacy allowlist.
Keep runtime standard output unchanged.

**Complete when:** every planned event is marked, session-correct, low-volume, and privacy-reviewed.

## 5. Capture One Trace

Immediately before the attempt, record the current complete-line boundary from
[`references/checkpoint.md`](references/checkpoint.md).

Run the trigger directly when it is safe and available. Otherwise present one fresh manual
checkpoint through the path selected in that reference.

- `PENDING`: yield with the session and probes active.
- `B` or `C`: route the result through the state table, adjust the attempt, and return here with a fresh boundary and checkpoint.
- `A`: continue with only the current-attempt records.

Existing records and tool activity labels never complete this step.

**Complete when:** a direct trigger or valid `A` produces every planned probe after `ATTEMPT_START_LINE` for the stated trigger.

## 6. Analyze and Locate

Read only complete records appended to `LOG_FILE` after `ATTEMPT_START_LINE`.
Confirm that every planned probe is present, then inspect the records in file order and compare the relevant values.
Return to Step 2 when expected events are missing.

Write the location report:

```text
Question: <runtime question>
Location: <file, function, and boundary>
Evidence: <ordered events and relevant values>
Confidence: <high, medium, or low with reason>
Next step: <smallest useful follow-up>
```

**Complete when:** current-attempt evidence answers the question and identifies the responsible code boundary.

## 7. Clean or Hand Off

For a standalone trace, remove every `LOG_SERVER_PROBE <session_id>` region.
Search for the marker, session ID, and both region forms.
Delete `LOG_FILE` unless the user requests retained evidence.
Keep the shared server running unless the user requests shutdown.
Stop any cloudflared process started for this session when the standalone trace ends.

When another workflow called this skill, hand back the active probes and evidence.
The caller then owns later edits, verification, and cleanup.

**Complete when:** standalone traces leave no instrumentation, or the caller receives an explicit active-trace handoff.

## Failure Branch

Read [`references/troubleshooting.md`](references/troubleshooting.md) only after startup, capture, or delivery fails.
