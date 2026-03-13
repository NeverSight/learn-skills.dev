---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
---

# Verification Before Completion

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Visual Verification (Frontend)

When frontend code is modified and browser tools are available, visual verification is part of the gate function. Triggers when: browser tools exist, frontend files changed (`.tsx`, `.jsx`, `.vue`, `.svelte`, `.css`), dev server running. Skip silently if not applicable.

See `references/visual-verification.md` for full protocol.

## Gap Closure Loop

When verification fails, don't just report — fix and re-verify:

```
IF verification fails:
  1. CREATE gap-fix task
  2. CREATE re-verification task (blocked by fix)
  3. WAIT for gap fix completion
  4. RUN re-verification
  5. IF still fails AND attempt < 3: → Increment attempt, GOTO step 1
  6. IF still fails AND attempt >= 3: → ESCALATE to human
```

See `references/gap-closure-protocol.md` for TaskCreate blocks and attempt tracking.

## Verification Task Enforcement

**Before making ANY completion claim, create a verification task:**

```
TaskCreate: "Verify: [specific claim]"
  description: "Evidence required: [verification command]. Must capture command output and exit code."
  activeForm: "Verifying [claim]"
```

**ENFORCEMENT:**
- Task description MUST specify the verification command
- Task CANNOT be marked `completed` without evidence in the conversation
- Evidence = actual command output showing pass/fail
- Subsequent completion claims blocked until verification task completed

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |
| UI renders correctly | Visual smoke test: page loads, no console errors | "Code looks right", build passes |

## Red Flags — STOP

Using "should", "probably", "seems to". Expressing satisfaction before verification ("Great!", "Perfect!", "Done!"). About to commit/push/PR without verification. Trusting agent success reports. Relying on partial verification. Thinking "just this once". **ANY wording implying success without having run verification.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Reference Files

- `references/visual-verification.md`: Full visual/frontend verification protocol
- `references/gap-closure-protocol.md`: Gap-fix → re-verify → escalate enforcement
- `references/key-patterns-examples.md`: Verification patterns with examples
- `references/why-this-matters.md`: Context from failure memories
- `references/when-to-apply.md`: When verification is required
- `references/SKILL.test.md`: Pressure test scenarios

<!-- compressed: 2026-02-11, original: 780 words, compressed: 558 words -->
