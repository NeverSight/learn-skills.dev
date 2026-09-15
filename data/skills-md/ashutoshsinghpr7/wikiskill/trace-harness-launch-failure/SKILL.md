---
name: trace-harness-launch-failure
description: "Empty session traces mean launch failure, not agent behavior — verify api_call_count/tool_call_count and stdout.txt before analyzing."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [traces, sessions, launch-failure, forensics]
    homepage: https://github.com/ashutoshsinghpr7/wikiskill
---

# Trace Harness Launch Failure — empty sessions, scores from deliverables

## Problem

Four training traces contain ONLY the initial task prompt: 1 message,
0 tool calls, 0 API calls, ~1 s duration. No agent reasoning, tool call, or
final answer anywhere — yet `meta.json` carries scores (0.0 / 1.0).

## Root cause

Every recorded run died at launch: `runs/<task>/stdout.txt` shows
"HTTP 400: default is not a valid model ID" — the harness sent an invalid
model ID instead of the configured model, so the agent never executed. The
scores were produced by grading the on-disk deliverables against the
exact-match graders in tasks.json — not from any recorded agent behavior.

## Fix

- Before analyzing "agent behavior", verify the session actually ran: check
  `api_call_count` / `tool_call_count` / `message_count` in the trace and
  stdout.txt for launch errors. Empty trace == no behavioral evidence.
- When traces are empty, reconstruct ground truth by diffing the on-disk
  deliverable against the task's grader expectation
  (`tasks.json` → `grader.expected`), and read spec.md + input data to
  explain the score.
- Treat prior-iteration behavioral claims as unverifiable until new traces
  confirm them; flag evidence status in the run log.
- Surface the harness bug so the runner is fixed before the next iteration,
  otherwise every proposal rests on inferred data.
