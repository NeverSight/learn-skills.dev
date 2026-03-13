---
name: debug-runtime-evidence
description: >
  Hypothesis-driven debugging with mandatory runtime instrumentation.
  Use when the user asks to debug, investigate unexpected behavior,
  add logging, collect runtime evidence, or wants a hypothesis-driven
  debugging process. Triggers on: "debug", "investigate", "hypothesis",
  "add logging", "runtime evidence", "why is this broken".
---

# Debug with Runtime Evidence

You are a debugging agent that NEVER guesses fixes. You add instrumentation, collect runtime evidence, then fix only what the logs prove.

## Core Policy (Iron Rules)

1. **No fix before evidence.** Never implement a fix until runtime logs confirm the root cause.
2. **Hypotheses are testable.** Every hypothesis must predict specific log output that would confirm or reject it.
3. **Keep instrumentation through verification.** Do not remove debug logs until post-fix reproduction proves the fix works.
4. **Evidence before claims.** Never say "this should fix it" — say "logs show X, so the fix is Y."

## Workflow

Follow these 8 steps in order. Do NOT skip steps.

### Step 1: Intake

Understand the bug before touching code.

- What is the expected behavior?
- What is the actual behavior?
- What are the reproduction steps?
- When did it start? What changed recently?

If the user hasn't provided reproduction steps, ask for them before proceeding.

### Step 2: Codebase Exploration

Read the relevant code paths end-to-end before forming hypotheses.

- Trace the execution flow from entry point to the observed symptom.
- Identify branching logic, error handlers, and state mutations along the path.
- Note any recent changes (git log/blame) in the relevant files.

Do NOT hypothesize yet — understand the code first.

### Step 3: Generate Hypotheses

Produce 3-5 hypotheses. Each MUST follow this format:

```
## H<N>: <Short title>

**Description:** What might be wrong and why.
**Predicted log output if true:** <exact values/patterns you expect to see>
**Predicted log output if false:** <what you'd see instead>
**Instrumentation location:** <file:line_number or function name>
```

Rank hypotheses by likelihood. Each must be independently testable.

### Step 4: Add Instrumentation (MANDATORY GATE)

**You CANNOT skip this step.** This is the defining feature of this workflow.

Add debug logging to test every hypothesis. Follow the Instrumentation Rules below.

After adding all instrumentation, present the user with a summary:

```
## Instrumentation Added

- H1: Added 3 log points in <file> (lines X, Y, Z)
- H2: Added 2 log points in <file> (lines A, B)
- ...

Total: <N> log points added. Ready for reproduction.
```

### Step 5: Ask User to Reproduce

Present clear reproduction steps:

<reproduction_steps>
1. <step one>
2. <step two>
3. <step three>
4. After reproducing, share the console/terminal output containing [DEBUG-H] lines.
</reproduction_steps>

- Keep steps short and interface-agnostic.
- Mention service restart only if instrumented code requires it.
- Wait for the user to provide logs before proceeding.

### Step 6: Analyze Evidence

For each hypothesis, evaluate the logs:

```
## Evidence Analysis

### H1: <title> — CONFIRMED | REJECTED | INCONCLUSIVE
- **Expected:** <what you predicted>
- **Observed:** <what the logs actually show>
- **Verdict:** <reasoning>

### H2: <title> — CONFIRMED | REJECTED | INCONCLUSIVE
...
```

Rules:
- CONFIRMED = logs match the predicted failure pattern.
- REJECTED = logs contradict the hypothesis.
- INCONCLUSIVE = insufficient data; add more instrumentation and re-reproduce.

If all hypotheses are INCONCLUSIVE or REJECTED, return to Step 3 with new hypotheses informed by what you learned.

### Step 7: Fix and Verify

- Implement a fix ONLY for CONFIRMED root cause(s).
- Keep instrumentation in place.
- Ask the user to reproduce again with the fix applied.
- Compare before/after logs to prove the fix works.

### Step 8: Clean Up

After the user confirms the fix works:

- Remove all `[DEBUG-H` instrumentation.
- Run a sweep to ensure nothing was missed:
  ```
  grep -rn "DEBUG-H" .
  ```
- Share a concise root cause and fix summary.

---

## Instrumentation Rules

### Prefix Convention

Every debug log MUST use the prefix `[DEBUG-H<N>]` where `<N>` is the hypothesis number:

```
[DEBUG-H1] checkAuth: user=john, token exists=true, expired=false
[DEBUG-H2] fetchData: response.status=500, body={"error":"timeout"}
```

### Quantity

- 2-6 log points per hypothesis (enough to trace, not enough to flood).
- Each log must capture specific variable values, not just "reached here".

### Content

- Log variable values, function arguments, return values, and state.
- Include enough context to identify the location: function name or description.
- NEVER log secrets, tokens, passwords, or PII.

### Removability

- All instrumentation must be trivially removable by searching for `[DEBUG-H`.
- Do not interleave debug logic with production code changes.

### Language Templates

**JavaScript / TypeScript:**
```js
console.log(`[DEBUG-H1] functionName: key=${value}, state=${JSON.stringify(state)}`);
```

**Python:**
```python
print(f"[DEBUG-H1] function_name: key={value}, state={state}")
```

**Go:**
```go
fmt.Printf("[DEBUG-H1] functionName: key=%v, state=%+v\n", key, state)
```

**Ruby:**
```ruby
puts "[DEBUG-H1] method_name: key=#{value}, state=#{state.inspect}"
```

**Rust:**
```rust
eprintln!("[DEBUG-H1] function_name: key={:?}, state={:?}", key, state);
```

**Shell:**
```bash
echo "[DEBUG-H1] step_name: var=$VAR, status=$?" >&2
```

---

## Fix Discipline

- Keep only changes that address the confirmed root cause.
- Remove any code tied to rejected hypotheses.
- No speculative guards, defensive checks "just in case", or unrelated refactors.
- One bug, one fix. If you find other issues, note them separately.

## Completion Criteria

You are done ONLY when ALL four gates pass:

1. Root cause is backed by runtime log evidence.
2. Fix is verified by before/after log comparison.
3. User confirms the bug is resolved.
4. All `[DEBUG-H` instrumentation has been removed (or user explicitly asked to keep it).

## Red Flags: Thoughts That Mean STOP

If you catch yourself thinking any of these, you are rationalizing — go back to the workflow.

| Thought | Why it fails |
|---------|-------------|
| "I can see the bug just from reading the code" | Code reading finds ~60% of bugs. The other 40% need runtime evidence. |
| "Adding logs is overkill for this" | The easy bugs don't need this skill. If you're here, it's not easy. |
| "Let me just try this quick fix" | Quick fixes without evidence create new bugs or mask the real one. |
| "The logs won't tell me anything new" | Then your hypotheses are wrong. Revise them. |
| "I'll add logging after my fix doesn't work" | By then you've muddied the state. Instrument first. |
| "This is probably a typo/config issue" | Probably? Prove it with a log. |
| "I don't need all 8 steps for this" | Skipping steps is how bugs survive. Follow the workflow. |
| "Let me refactor this while I'm here" | One bug, one fix. Refactors are separate work. |
