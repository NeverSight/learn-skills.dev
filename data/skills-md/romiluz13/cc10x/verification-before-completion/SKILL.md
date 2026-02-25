---
name: verification-before-completion
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: Read, Grep, Glob, Bash, LSP
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

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
5. REFLECT: Pause to consider tool results before next action
6. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

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

## Red Flags - STOP

If you find yourself:

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

**STOP. Run verification. Get evidence. THEN speak.**

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
| "I already tested it manually" | Manual ≠ automated evidence |
| "The code looks correct" | Looking ≠ running |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## Why This Matters

From real failure patterns:

- Your user said "I don't believe you" - trust broken
- Undefined functions shipped - would crash in production
- Missing requirements shipped - incomplete features
- Time wasted on false completion → redirect → rework
- Violates: "Honesty is a core value. If you lie, you'll be replaced."

## When To Apply

**ALWAYS before:**

- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**

- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## Self-Critique Gate (BEFORE Verification Commands)

**MANDATORY: Check these BEFORE running verification commands:**

### Code Quality
- [ ] Follows patterns from reference files?
- [ ] Naming matches project conventions?
- [ ] Error handling in place?
- [ ] No debug artifacts (console.log, TODO)?
- [ ] No commented-out code?
- [ ] No hardcoded values that should be constants?

### Implementation Completeness
- [ ] All required files modified?
- [ ] No unexpected files changed?
- [ ] Requirements fully met?
- [ ] No scope creep?

### Self-Critique Verdict

**PROCEED:** [YES/NO]
**CONFIDENCE:** [High/Medium/Low]

- If NO → Fix issues before verification
- If YES → Proceed to verification commands below

---

## Validation Levels

**Match validation depth to task complexity:**

| Level | Name | Commands | When to Use |
|-------|------|----------|-------------|
| 1 | Syntax & Style | `npm run lint`, `tsc --noEmit` | Every task |
| 2 | Unit Tests | `npm test` | Low-Medium risk tasks |
| 3 | Integration Tests | `npm run test:integration` | Medium-High risk tasks |
| 4 | Manual Validation | User flow walkthrough | High-Critical risk tasks |

**Include the appropriate validation level for each verification step.**

## Verification Checklist

Before marking work complete:

- [ ] All relevant tests pass (exit 0) - **with fresh evidence**
- [ ] Build succeeds (exit 0) - **with fresh evidence**
- [ ] Feature functionality verified - **with command output**
- [ ] No regressions introduced - **with test output**
- [ ] Evidence captured for each check - **in this message**
- [ ] Deviations from plan documented - **if implementation differed from design**
- [ ] Appropriate validation level applied for task risk

## Output Format

```markdown
## Verification Summary

### Scope
[What was completed]

### Criteria
[What was verified]

### Evidence

| Check | Command | Exit Code | Result |
|-------|---------|-----------|--------|
| Tests | `npm test` | 0 | PASS (34/34) |
| Build | `npm run build` | 0 | PASS |
| Feature | `npm test -- --grep "feature"` | 0 | PASS (3/3) |

### Deviations from Plan (if any)
| Planned | Actual | Reason |
|---------|--------|--------|
| [Original design] | [What changed] | [Why] |

### Status
COMPLETE - All verifications passed with fresh evidence
```

## Evidence Array Protocol

**Every claim in verification output MUST have a corresponding evidence entry.**

**Format:** `[command] → exit [code]: [result summary]`

**Rules:**
1. One evidence entry per claim — no claim without evidence, no evidence without claim
2. Evidence must be from THIS session (not recalled from memory)
3. Exit codes are mandatory — "looks good" is not evidence
4. Group evidence by claim type:

```
EVIDENCE:
  tests: ["CI=true npm test → exit 0: 34/34 passed"]
  build: ["npm run build → exit 0: compiled in 2.3s"]
  feature: ["curl localhost:3000/api/health → exit 0: {status: ok}"]
  regression: ["npm test -- auth.test.ts → exit 0: regression case passes"]
```

**Verification Summary must include this EVIDENCE block before the Status line.**

**Anti-pattern:** `Status: COMPLETE - All verifications passed` without EVIDENCE block = INVALID.

## Goal-Backward Lens (GSD-Inspired)

After standard verification passes, apply this additional check:

### Three Questions
1. **Truths:** What must be OBSERVABLE? (user-facing behaviors)
2. **Artifacts:** What must EXIST? (files, endpoints, tests)
3. **Wiring:** What must be CONNECTED? (component → API → database)

### Why This Catches Stubs
A component can:
- Exist ✓
- Pass lint ✓
- Have tests ✓
- But NOT be wired to the system ✗

Goal-backward asks: "Does the GOAL work?" not "Did the TASK complete?"

### Quick Check Template
```
GOAL: [What user wants to achieve]

TRUTHS (observable):
- [ ] [User-facing behavior 1]
- [ ] [User-facing behavior 2]

ARTIFACTS (exist):
- [ ] [Required file/endpoint 1]
- [ ] [Required file/endpoint 2]

WIRING (connected):
- [ ] [Component] → [calls] → [API]
- [ ] [API] → [queries] → [Database]

Standard verification: exit code 0 ✓
Goal check: All boxes checked?
```

### When to Apply
- After integration-verifier runs
- After any "feature complete" claim
- Before marking BUILD workflow as done

**Iron Law unchanged:** Exit code 0 still required. This is an additional verification lens, not a replacement.

## Stub Detection Patterns

After Goal-Backward Lens passes, scan for these stub indicators:

### Universal Stubs
```bash
# Check for TODO/placeholder markers
grep -rE "TODO|FIXME|placeholder|not implemented|coming soon" --include="*.ts" --include="*.tsx" --include="*.js"

# Check for empty returns
grep -rE "return null|return undefined|return \{\}|return \[\]" --include="*.ts" --include="*.tsx"
```

### React Component Stubs
| Pattern | Why It's a Stub |
|---------|-----------------|
| `return <div>Placeholder</div>` | Renders nothing useful |
| `onClick={() => {}}` | Click does nothing |
| `onSubmit={(e) => e.preventDefault()}` | Only prevents default, no action |
| `useState` with no setter calls | State never changes |

### API Route Stubs
| Pattern | Why It's a Stub |
|---------|-----------------|
| `return Response.json({ message: "Not implemented" })` | Explicit stub |
| `return Response.json([])` without DB query | Returns empty, no real data |
| `return NextResponse.json({})` with no logic | Empty response |

### Function Stubs
| Pattern | Why It's a Stub |
|---------|-----------------|
| `throw new Error("Not implemented")` | Will crash at runtime |
| `console.log("TODO")` | Debug artifact |
| `// TODO: implement` | Marked incomplete |

### Quick Stub Check
```bash
# Run before claiming completion
grep -rE "(TODO|FIXME|placeholder|not implemented)" src/
grep -rE "onClick=\{?\(\) => \{\}\}?" src/
grep -rE "return (null|undefined|\{\}|\[\])" src/
```

**If any stub patterns found:** DO NOT claim completion. Fix or document why it's intentional.

### Wiring Verification (Component → API → Database)

Artifacts can exist, pass lint, and have tests but NOT be wired to the system.

**Component → API Check:**
```bash
# Does component actually call the API?
grep -E "fetch\(['\"].*api|axios\.(get|post)" src/components/
# Is response actually used?
grep -A 5 "fetch\|axios" src/components/ | grep -E "await|\.then|setData|setState"
```

**API → Database Check:**
```bash
# Does API actually query database?
grep -E "prisma\.|db\.|mongoose\." src/app/api/
# Is result actually returned?
grep -E "return.*json.*data|Response\.json" src/app/api/
```

**Red Flags:**
| Pattern | Problem |
|---------|---------|
| `fetch('/api/x')` with no `await` | Call ignored |
| `await prisma.findMany()` → `return { ok: true }` | Query result discarded |
| Handler only has `e.preventDefault()` | Form does nothing |

**Line Count Minimums:**
| File Type | Minimum Lines | Below = Likely Stub |
|-----------|---------------|---------------------|
| Component | 15 | Too thin |
| API route | 10 | Too thin |
| Hook/util | 10 | Too thin |

### Export/Import Verification

Exports can exist but never be consumed. Check that key exports are actually used:

```bash
# Check if export is imported AND used (not just imported)
check_export_used() {
  local export_name="$1"
  grep -r "import.*$export_name" src/ --include="*.ts" --include="*.tsx" | wc -l
  grep -r "$export_name" src/ --include="*.ts" --include="*.tsx" | grep -v "import\|export" | wc -l
}

# Example: Check auth exports are consumed
check_export_used "getCurrentUser"
check_export_used "useAuth"
```

**Export Status:**
| Status | Meaning | Action |
|--------|---------|--------|
| CONNECTED | Imported AND used | ✓ Good |
| IMPORTED_NOT_USED | Import exists but never called | Remove dead import or implement |
| ORPHANED | Export exists, never imported | Dead code or missing integration |

### Auth Protection Verification

Sensitive routes must check authentication:

```bash
# Find routes that should be protected
protected_patterns="dashboard|settings|profile|account|admin"
grep -r -l "$protected_patterns" src/app/ --include="*.tsx"

# For each, verify auth usage
check_auth_protection() {
  local file="$1"
  grep -E "useAuth|useSession|getCurrentUser|isAuthenticated" "$file"
  grep -E "redirect.*login|router.push.*login" "$file"
}
```

**If sensitive route lacks auth check:** Add protection before claiming completion.

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.

## Completion Guard (Final Gate Before Router Contract)

**IMMEDIATELY before writing `### Router Contract (MACHINE-READABLE)`, verify ALL:**

1. **Acceptance criteria met?** — Re-read task description. Check each criterion. Any gap = STATUS:FAIL
2. **Evidence array complete?** — Every claim has `[command] → exit [code]` entry from THIS session
3. **No stubs in changed files?** — Run stub detection on files YOU modified (not entire repo)
4. **Fresh verification?** — Last test/build command ran in THIS message (not earlier in conversation)

**If ANY check fails:** Fix it FIRST, then re-run Completion Guard. Do NOT emit Router Contract with STATUS:PASS/FIXED/APPROVE until all 4 pass.

**This is the LAST gate. No exceptions. No "close enough."**
