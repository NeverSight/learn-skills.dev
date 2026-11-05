---
name: verifying-outcomes
description: Use when the user asks to 'verify', 'did this actually work', 'is X really done' — or before you claim a task is complete and before closing an issue or merging a PR. Goal-backward verification — checks whether the desired outcome was achieved, not whether tasks were marked done.
license: Apache-2.0
compatibility: Works in any repo. Uses Read, Grep, Glob, Bash.
metadata:
  authors:
    - Artem Rozumenko <artem_rozumenko@epam.com>
  version: "0.1.0"
---

# Verifying Outcomes

**"Tasks completed" ≠ "goal achieved."** Your job is to verify the outcome, ruthlessly and from evidence.

If the goal is fuzzy, ask for clarification before starting. Don't verify a moving target.

## Five Checks

### 1. STATE the goal
Restate it as a concrete, testable outcome — not as a list of tasks. Write it at the top of the report verbatim.

### 2. What must be TRUE
List the logical conditions that must hold for the goal to be met. These are assertions about behavior, not about work performed.
- ✅ "API returns 200 for valid requests and 401 for missing tokens"
- ❌ "Endpoint was implemented"

### 3. What must EXIST
List concrete artifacts: files, endpoints, configs, migrations, tests, docs. For each, use `Read` / `Glob` / `Grep` to confirm it exists **and contains the expected content**. Existence alone isn't enough — empty stubs fail.

### 4. What must be CONNECTED
Things that exist but aren't wired up are useless. Verify:
- Imports / exports
- Route registrations, DI bindings, plugin lists
- Config keys actually read by the code
- Tests actually run by the test command (not orphaned files)
- Migrations actually included in the migration manifest

Use `Grep` to trace from the artifact to its consumer. If you can't find the consumer, it isn't connected.

### 5. Where will this BREAK
- Edge cases and error paths
- Missing input validation
- Hardcoded values that should be config / env vars
- Missing or unhandled env vars (`Grep` for `os.getenv` / `process.env` without defaults)
- Race conditions, timeouts, retries
- Test coverage gaps for the new behavior

## Output

```
## Verification: <goal verbatim>

### Verdict: PASS | PARTIAL | FAIL

### TRUE
- <verified condition> — <how you verified>
- ...

### EXISTS
- <artifact> — <path:line> — <what you confirmed>
- ...

### CONNECTED
- <integration point> — <evidence>
- ...

### RISKS
- <where this will break, and why>
- ...

### Summary
<1–2 sentences>
```

## Rules

- **Cite file paths and line numbers** for every claim. No hand-waving.
- A check you can't perform is a **FAIL** for that check, not a pass-by-default.
- PARTIAL is for "outcome works on the happy path but a listed risk is real and unaddressed." Don't use it as a polite FAIL.
- Be honest. The point of this skill is to catch the things the implementer missed — flattery defeats the purpose.
