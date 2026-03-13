---
name: bug-fix
description: Analyze bugs, present repair options, then implement and verify the user-selected fix path.
compatibility: Use in environments with code exploration (Read/Grep/Glob), editing (Edit), and validation commands (Bash).
---

# Bug Fix Skill

> Reproduce and analyze bugs, propose options, and apply a safe selected fix.

<when_to_use>

| Situation | Example |
|------|------|
| Type errors | `Property 'X' does not exist on type 'Y'` |
| Runtime errors | `Cannot read property ... of undefined` |
| Logic bugs | duplicate rendering, wrong calculation, stale state |
| API failures | 4xx/5xx, response shape mismatch |
| Intermittent issues | failures under specific conditions |

</when_to_use>

<argument_validation>

If ARGUMENT is missing, ask immediately:

```text
Which bug should be fixed?
- Error message / stack trace
- Expected vs actual behavior
- Reproduction steps
- Related files (if known)
```

</argument_validation>

<mandatory_reasoning>

## Mandatory Sequential Thinking

- Always run `sequential-thinking` before implementation.
- Simple bug: at least 3 thoughts
- Medium complexity: 5 thoughts
- High complexity: 7+ thoughts

Recommended sequence:

1. Complexity classification
2. Reproduction and symptom framing
3. Root-cause hypotheses
4. Option comparison
5. Final recommendation

</mandatory_reasoning>

<workflow>

| Step | Task | Tool |
|------|------|------|
| 1 | Validate input and summarize reproducible signals | - |
| 2 | Build analysis plan with sequential-thinking | sequential-thinking |
| 3 | Explore relevant code and isolate root cause | Read/Grep/Glob |
| 4 | Present 2-3 fix options | - |
| 5 | Wait for user selection | - |
| 6 | Implement selected option | Edit |
| 7 | Run type/test/build verification | Bash |
| 8 | Report outcome and changed files | - |

</workflow>

<option_presentation>

Use this format:

```markdown
## Bug Analysis Result
Root cause: ...
Impact scope: ...

### Option 1: ... (Recommended)
- Pros:
- Cons:
- Risk:
- Files:

### Option 2: ...
- Pros:
- Cons:
- Risk:
- Files:

### Option 3: ... (Temporary)
- Pros:
- Cons:
- Risk:
- Files:

Recommendation: Option N (reason ...)
Which option should I apply? (1/2/3)
```

</option_presentation>

<implementation_rules>

- Do not modify code before user option selection.
- Avoid speculative edits; use evidence-based fixes only.
- Keep scope limited to the requested bug and direct impact.
- Always include validation output in the final report.

</implementation_rules>

<validation>

Execution checklist:

- [ ] ARGUMENT validated
- [ ] sequential-thinking completed
- [ ] Root-cause evidence collected
- [ ] 2-3 options presented
- [ ] User choice confirmed
- [ ] typecheck/test/build executed
- [ ] outcome + touched files reported

Forbidden:

- [ ] speculative fix without evidence
- [ ] immediate implementation without options
- [ ] implementation without explicit user choice
- [ ] completion claim without validation

</validation>
