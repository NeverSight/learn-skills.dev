---
name: debug-mode
description: Diagnose and fix reproducible runtime bugs with temporary structured logs, root-cause evidence, verification, and cleanup. Use for explicit debug-mode or instrumented debugging requests. Continue active sessions across reproduction replies. Use trace-mode when the goal stops at code location.
---

# Debug Mode

Start a session only when the current user invokes `$debug-mode`, says `debug mode`, or requests instrumented debugging.
Resume whenever an active debug session exists, including after user replies or context compaction.
The session becomes active when Step 3 arms the server.
It ends only after verified cleanup or explicit abandonment.
If neither condition applies, stop before analysis, collection, or instrumentation.

This workflow builds on the sibling [`trace-mode`](../trace-mode/SKILL.md) workflow.
It extends location evidence through correction, verification, and cleanup.
The sibling scripts require Node.js 24 or later.

The initial stage is:

```text
analyze code -> hypothesize -> trace with trace-mode -> reproduction gate
```

Work autonomously until the probes and collector are ready, then yield at the reproduction gate.
Reproduction and verification are closed gates:

- Every manual attempt starts `PENDING` and requires a fresh checkpoint.
- Only a valid result from that checkpoint unlocks the next stage.
- While `PENDING`, keep the session and probes active; the only progress is completing the checkpoint.
- Logs, tests, static analysis, tool activity labels, and results from earlier attempts never unlock a gate.

Read [`references/checkpoints.md`](references/checkpoints.md) at every gate for result validation,
fallback routing, and the current-attempt log boundary.

## 1. Analyze the Code Path

Start repository legwork from the reported symptom.
Read relevant entry points, handlers, state transitions, existing logs, and recent changes.
Map candidate paths from the user's trigger to the observed outcome.
Write a Bug Card:

- Symptom and expected behavior
- Known trigger, route, command, input, or fixture
- Candidate runtime path and disputed boundaries
- Relevant environment, frequency, changes, and evidence
- Observable acceptance criterion

Record unavailable facts as `unknown`.
Resolve consequential unknowns through code reading or discriminating runtime probes.

**Complete when:** one candidate path links trigger to symptom, and each disputed branch has a named probe boundary.

## 2. Build the Hypothesis Matrix

Write two to five ranked hypotheses before adding probes.
Anchor the matrix in code analysis and available evidence.
Use this shape:

```text
H1 <short cause>
Prediction: <runtime state, path, or timing>
Probe: <event names and code locations>
CONFIRMED when: <specific record condition>
REJECTED when: <specific record condition>
```

A hypothesis without a concrete prediction requires more code reading.
Prefer probes that separate multiple hypotheses.

**Complete when:** every hypothesis has falsifiable conditions and a distinguishing planned probe.

## 3. Trace Through Trace Mode

Read the sibling [`trace-mode`](../trace-mode/SKILL.md) skill.
Use its event planning, server startup, and instrumentation steps with the Bug Card.
Read [`references/probes.md`](references/probes.md) for the debug event extension.
Return here before its standalone trace checkpoint.

This workflow is the caller.
The trace-mode workflow must hand back active probes and the five server values.

**Complete when:** every hypothesis has an active probe and all five server values are known.

## 4. Cross the Reproduction Gate

Prepare and present one pre-fix checkpoint through the selected path in
[`references/checkpoints.md`](references/checkpoints.md).

- `PENDING`: yield with the session active.
- Pre-fix `B` or `C`: route the result through the state table, adjust the attempt, and return here with a fresh checkpoint.
- Pre-fix `A`: read [`references/prove-fix-verify.md`](references/prove-fix-verify.md) and continue there.

**Complete when:** a valid pre-fix `A` unlocks the evidence stage, or the current `B`/`C` result has been routed without advancing it.

## Exception Branch

Read [`references/troubleshooting.md`](references/troubleshooting.md) only when collection, reproduction, or delivery fails.
