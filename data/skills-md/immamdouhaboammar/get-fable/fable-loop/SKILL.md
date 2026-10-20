---
name: fable-loop
description: "Execute bounded recurring polling loops, CI build babysitting, interval-based status monitors, and self-paced test cycles with explicit timeouts and backoff. Use when monitoring async CI/CD pipelines, polling external service status, running interval test watches, or tracking long-running jobs — even if the user does not explicitly say \"fable-loop\" (e.g. \"babysit this build\", \"poll until completed\", \"watch CI status\", \"wait for deployment\"). Do NOT use for synchronous one-shot commands or unbounded infinite polling loops."
version: 1.3.0
pack: system
inputs:
  - loop_condition
requires:
  - exit_criteria
produces:
  - loop_receipt
gates:
  - budget_bounded
  - exit_condition_explicit
fallback: fable-recover
mutatesWorkspace: false
parallelSafe: true
neural_links:
  precursors:
    - fable-run
  continuations:
    - fable-verify
    - fable-handoff
  lateral_peers:
    - fable-run
  recovery: fable-recover
---

# Fable Loop

Repeat a check only when repetition can reveal new state, with explicit termination, backoff, error classification, and zero ambiguity about why the loop stopped.

## Mission
Polling is not "run the same command until it turns green." A good loop models a changing external condition, distinguishes pending from failure, respects rate/cost budgets, and terminates on success, terminal failure, cancellation, or exhausted budget.

If repeated execution cannot produce new information, the task belongs in diagnosis—not a loop.

## Activate When
- waiting for CI/deployment/build/batch-job state to change;
- monitoring a bounded asynchronous operation;
- checking eventually-consistent external state;
- repeating a safe measurement while a known process progresses;
- running a finite stabilization sample where repetition itself is the measurement.

## Do Not Activate When
- one command/probe is enough (`fable-run`/`fable-verify`);
- the same deterministic failure is repeating with no external state change (`fable-recover`);
- user expects a future notification/scheduled task rather than an in-session bounded loop;
- polling would create repeated non-idempotent side effects;
- no termination criteria or budget can be defined.

## Loop Classification
| Loop type | Success/terminal semantics |
| --- | --- |
| CI/build | pending → success or terminal failure/cancelled |
| Deployment | progressing → healthy/rolled back/failed |
| Batch job | queued/running → completed/failed |
| Eventual consistency | old state → expected state within deadline |
| Rate-limited API | pending/retryable → success or terminal auth/schema error |
| Stabilization sampling | N bounded observations → distribution/variance verdict |

## Protocol
### Stage 1 — Define the state machine
Before iteration, enumerate:
- success state;
- pending/retryable states;
- terminal failure states;
- malformed/unknown states;
- cancellation condition.

A loop that treats every non-success as "try again" is unsafe.

### Stage 2 — Set budgets
Define at least:
- maximum elapsed time/deadline;
- maximum iterations or request budget where relevant;
- initial interval/backoff policy;
- maximum interval;
- API/cost/rate constraints.

Use the stricter bound when several apply.

### Stage 3 — Check idempotency and side effects
Polling operation should be read-only/idempotent. If the endpoint/command triggers work, separate trigger from status observation and ensure retries cannot duplicate the action.

### Stage 4 — Execute one iteration and classify result
Record:
- iteration/time;
- observed state/value;
- transport/command result;
- classification: success / pending / retryable error / terminal failure / unknown;
- next delay/reason.

### Stage 5 — Apply backoff intelligently
Use a fixed interval when the expected update cadence is known and inexpensive; exponential/backoff+jitter when rate limits/transient service errors matter.

Respect explicit `Retry-After`/provider guidance where applicable. Do not make sub-second aggressive calls to a slow external job just because tools allow it.

### Stage 6 — Stop early on terminal information
Exit immediately on:
- success;
- explicit failed/cancelled state;
- non-retryable auth/schema/permission error;
- user cancellation;
- budget/deadline exhaustion.

Do not consume remaining iterations after the outcome is already known.

### Stage 7 — Detect lack of progress
When a status includes progress/version/timestamp, compare across iterations. A long unchanged state near/after expected SLA may become a diagnostic signal rather than permission to extend budget automatically.

### Stage 8 — Produce an honest receipt
Final receipt includes stop reason, elapsed time, iterations, last state, transient errors, and whether the condition was actually satisfied.

Timeout is not success. "Still running" is not failure unless the contract/deadline says so.

## Decision Rules
- Deterministic repeated failure with no changing external state → stop loop and recover.
- Retryable transport error may continue within budget; auth/permission/schema errors usually terminate until configuration changes.
- Treat provider `Retry-After` or job-recommended poll interval as a lower bound where applicable.
- Never repeat a non-idempotent trigger as a status poll.
- If each iteration costs meaningful money/quota, include cost/request budget, not only time.
- If expected completion exceeds the current session/task model, create a scheduled/condition-watch mechanism when available rather than pretending an in-session loop can run indefinitely.
- A loop may end `INCOMPLETE/TIMEOUT`; do not extend bounds silently just to obtain green.
- If progress is unchanged and deadline still distant, continue according to policy without noisy user updates; surface only meaningful state changes for long interactive runs.

## Invariants
- Exit criteria and budgets are explicit before looping.
- Each iteration is safe/idempotent or side-effect semantics are explicitly controlled.
- Terminal failures stop immediately.
- Pending and failure are distinct states.
- Backoff/rate limits are respected.
- Receipt records actual stop reason; no timeout-to-pass conversion.

## Failure Taxonomy
### Infinite/implicit loop
No enforceable budget. Reject and define bounds.

### Retry-all-errors
Auth/schema/permission/terminal job failures are treated as transient. Classify and stop appropriately.

### Duplicate side effect
Polling call re-triggers work. Separate status endpoint/idempotency key or stop.

### Thundering poll
Interval too aggressive for service/job cadence. Back off/respect provider guidance.

### False timeout diagnosis
Job still pending within expected SLA but loop labels it broken. Report timeout/incomplete separately from product failure.

### Stuck progress
State never changes when it should. Hand to recovery/operations diagnosis rather than extending forever.

### Session mismatch
Requested monitoring lasts beyond available execution window. Use scheduling/condition-watch capability when supported.

## Anti-Patterns
- raw `while true`/unbounded sleep loops;
- retrying every error class;
- polling by repeatedly re-submitting the job;
- extending timeout until success after each miss;
- 1-second polling for a 10-minute deployment;
- declaring failure just because status is pending;
- declaring success because the loop ended cleanly;
- hiding transient errors from the final receipt;
- using loops to avoid diagnosing deterministic repeated failures.

## Loop Receipt
```text
Condition/state machine:
Success / terminal failure states:
Time + iteration/request budgets:
Interval/backoff policy:
Idempotency/side-effect check:
Iterations: time → observed state → classification
Transient errors:
Stop reason:
Condition satisfied? yes/no
Final state:
Next action if incomplete/failed:
```

## Completion Criteria
Loop completes when:
- state machine, success/failure semantics, and budgets were explicit;
- polling respected idempotency/rate/cost constraints;
- terminal information stopped the loop early;
- timeout/stuck state is represented honestly;
- final receipt shows exactly why looping ended and what should happen next.

## Progressive Resources
- Deep guide: `references/polling-state-machines-and-backoff.md`
- Existing guidelines: `references/loop-control-guidelines.md`
- Example: `examples/poll-build-job.md`
