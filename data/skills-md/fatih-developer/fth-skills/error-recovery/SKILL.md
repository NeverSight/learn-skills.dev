---
name: error-recovery
description: When a step fails during an agentic task, classify the error (transient, configuration, logic, or permanent), apply the right recovery strategy, and escalate to the user when all strategies are exhausted. Triggers on error messages, exceptions, tracebacks, "failed", "not working", "retry", or when 2 consecutive steps fail.
---

# Error Recovery Protocol

When an error occurs, stop, think, and try the right recovery strategy. No blind retries — understand the error signal first, then act.

**Core principle:** Every error carries a signal. Read the signal first, then act.

---

## Error Classification

Classify every error into one of 4 categories — the recovery strategy depends on the category:

### Transient Error
Retrying usually fixes it. Infrastructure or network related.
- Examples: timeout, rate limit (429), connection drop, temporary service outage
- Strategy: **Wait & Retry** with exponential backoff

### Configuration Error
Environment or setup issue. Code is correct but setup is wrong.
- Examples: missing env variable, wrong file path, permission denied, missing dependency
- Strategy: **Fix & Continue** — identify the issue, fix it, re-run

### Logic Error
Code or approach is wrong. Retrying produces the same error.
- Examples: KeyError, TypeError, wrong algorithm, expectation mismatch
- Strategy: **Alternative Approach** — try a different method

### Permanent / External Error
Out of control, cannot be fixed. External service or permission boundary.
- Examples: 403 Forbidden, 404 Not Found, quota exceeded, API deprecated
- Strategy: **Escalation** — inform the user, ask for direction

---

## Retry Strategy

For transient errors, use exponential backoff:

```
Attempt 1: Retry immediately
Attempt 2: Wait 2 seconds
Attempt 3: Wait 4 seconds
Attempt 4: Wait 8 seconds -> move on or escalate
```

**Maximum retries:** 3 attempts. If all 3 fail → re-evaluate the category.

Rate limit (429) special rule:
- If response has `Retry-After` header, wait that duration
- Otherwise wait 60 seconds, then retry

---

## Decision Tree

```
Error received
    |
Classify the error
    |
+------------------------------------+
| Transient?  -> Wait & Retry (max 3)|
| Config?     -> Fix & Continue      |
| Logic?      -> Alternative approach|
| Permanent?  -> Escalation          |
+------------------------------------+
    |
Every strategy fails -> Escalation
```

---

## Escalation Protocol

Escalate to the user when:
- 3 retries failed
- Permanent / external error
- 2 consecutive different strategies failed
- Error category cannot be determined

```
ERROR ESCALATION
================================
Failed step : [step name]
Error       : [error message summary]
Category    : [Transient / Config / Logic / Permanent]
Tried       : [what was attempted — short list]
Result      : All strategies exhausted
================================
Options:
  A) [Alternative approach suggestion]
  B) [Simpler / partial solution]
  C) Skip this step, continue
  D) Stop the task
```

---

## Partial Success

For bulk operations where some items succeed and some fail:

```
PARTIAL SUCCESS
================================
Successful : N / Total
Failed     : M items
================================
Failed items:
  - [item]: [reason]

Options:
  A) Retry only failed items
  B) Continue with successful items, skip failed
  C) Cancel all
```

---

## Error Log

Log every error and recovery attempt:

```
[ERROR LOG]
Step     : [step name / number]
Error    : [message]
Category : [type]
Attempt 1: [strategy] -> [result]
Attempt 2: [strategy] -> [result]
Result   : Recovered / Escalated
```

---

## When to Skip

- Error is expected behavior (e.g., "file not found" when checking existence)
- User said "ignore errors, continue"
- One-off, non-repeatable task

---

## Guardrails

- **Never blind-retry a logic error** — retrying won't help, change the approach.
- **Always log every attempt** — even successful recoveries need a record.
- **Cross-skill**: integrates with `checkpoint-guardian` (risk assessment before retry), `memory-ledger` (logs errors and fixes), and `agent-reviewer` (retrospective analysis).
