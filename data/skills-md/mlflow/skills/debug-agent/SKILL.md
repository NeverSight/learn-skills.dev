---
name: debug-agent
description: >-
  Root-causes AI agent failures from MLflow traces without requiring a code
  change, regression suite, scorer, or evaluation run. Use when the user asks
  to debug, investigate, explain, or determine why an agent produced an output.
  Prefer an existing matching trace; reproduce only when no usable trace exists.
---

# Debug Agent

Diagnose the failure and report evidence. Do not edit the agent unless the user
also asks for a fix; for behavior changes, hand off to `fix-agent-issue` after
the diagnosis.

## Workflow

1. Find existing tracing configuration, tracking URI, and experiment. Do not
   recommend reinstalling or reinstrumenting MLflow when tracing already works.
2. Find a trace matching the reported input, time, session, user, or trace ID.
   If one exists, use it directly. Do not reproduce a production-only or
   externally dependent failure merely to satisfy a workflow.
3. Only when no usable trace exists, reproduce the issue once through the normal
   instrumented entry point and retrieve the resulting trace. If reproduction
   is unsafe or impossible, state what evidence is missing and stop.
4. Inspect the matching trace span by span. Read assessments first, then inputs,
   outputs, errors, LLM calls, retrieval results, and tool calls. Use
   `analyze-mlflow-trace` for detailed trace anatomy.
5. Correlate trace evidence with source code as needed. Reading source is fine;
   do not settle on a diagnosis without confirming it against the trace.
6. Report: observed behavior, expected behavior, trace evidence, root cause,
   confidence, and the smallest likely fix. Do not create tests or scorers for a
   diagnosis-only request.

## Boundaries

- If no trace can be produced because the app is uninstrumented, load
  `instrumenting-with-mlflow-tracing` and explain the limitation.
- Log the user's complaint as HUMAN feedback only when a concrete trace is
  identified and doing so is authorized.
- If the user asks to implement the fix, invoke `fix-agent-issue` with the trace
  ID and diagnosis so it can write regression coverage before editing.
