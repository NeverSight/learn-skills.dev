---
name: Debugging Expert
description: A systematic workflow for resolving complex errors, compilation failures, and data consistency issues.
---

# Debugging Expert Skill

This skill guides the agent through a rigorous root cause analysis process, treating bugs as scientific anomalies to be investigated.

## 🔬 The Protocol

### Phase 1: Isolation
1.  **Reproduce**: Can you trigger the bug reliably?
2.  **Minimize**: What is the smallest action that triggers it?
3.  **Boundaries**: Is it Frontend (Browser) or Backend (Server)?
    -   *Action*: Check Browser Network Tab. Request sent? Payload correct?
    -   *Action*: Check Backend Logs. Request received? Error stack trace?

### Phase 2: Visibility (The "Light It Up" Strategy)
If the bug is silent (no error, but wrong result):
1.  **Trace it**: Add logging at entry (Controller), middle (Service), and exit (Mapper/DB).
2.  **Raw Payload**: Log the `raw input` (e.g. Map instead of POJO) to verify data integrity before binding.
3.  **Version Check**: Add a `FATAL` or `static block` log with a version number (e.g., "V1.2") to prove the code running IS the code you just wrote.

### Phase 3: The "Build Hygiene" Check
**CRITICAL**: If code looks correct but behaves wrongly, suspect the Build.
1.  **Clean**: Manually remove `target/` directories.
2.  **Recompile**: Run `mvn clean package`.
3.  **Inspect**: grep build logs for "ERROR" or "WARNING" that was ignored.

### Phase 4: Resolution & Cleanup
1.  **Fix**: Apply the smallest effective change.
2.  **Verify**: Re-run the reproduction steps.
3.  **Cleanup**: Remove all temporary `System.out.println`, logs, and visual markers.

## How to use
Invoke this skill when you are "stuck" or when a bug persists despite "obvious" fixes.
