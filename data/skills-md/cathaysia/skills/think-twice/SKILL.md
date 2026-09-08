---
name: think-twice
description: "Think Twice: automatically run a critical self-review after proposing a debugging solution. Use this skill whenever the agent is debugging an issue, fixing a bug, resolving an error, troubleshooting a failure, or proposing a code fix. Activate this skill even when the fix seems straightforward — quick patches are exactly where blind spots hide."
---

# Think Twice

## Why This Skill Exists

Debugging often creates tunnel vision. When you finally find the root cause and a
fix clicks into place, the relief of "it works now" bypasses critical thinking.
The result: over-engineered guards for impossible edge cases, hardcoded test
hacks that leak into production, security shortcuts that felt harmless in dev,
and dead code that nobody cleans up.

This skill forces a deliberate pause — after you've proposed a solution but
before you finalize it — to pressure-test the fix from four angles that
debugging tunnel vision routinely misses.

## When to Activate

Trigger this self-review **after** you have a concrete solution (code diff,
proposed change, or implementation plan) for a debugging task. This includes:

- Fixing a bug or error
- Resolving test failures
- Troubleshooting runtime issues
- Patching security vulnerabilities
- Working around environment-specific problems

Do **not** activate during initial exploration, root cause analysis, or when
the user is still describing the problem. Wait until you have a proposed fix.

## The Review Process

After proposing your solution, pause and conduct the following four-checkpoint
review. Present your findings in a clearly labeled section titled
**Think Twice — Self-Review** so the user can see the reasoning.

---

### Checkpoint 1: Over-Engineering Check

Ask yourself whether the fix is proportional to the actual problem.

**Red flags to watch for:**

- Defending against scenarios that the current codebase will never encounter
  (e.g., adding i18n fallback logic in a single-language internal tool)
- Adding large abstractions to handle a case that affects < 1% of users, when
  a simple comment or known-limitation note would suffice
- Building configuration systems for values that are effectively constants
- In a development/prototype context: adding production-grade retry logic,
  circuit breakers, or rate limiters that the project doesn't need yet
- In a dev environment: treating security hardening as a blocker when the
  service only runs on localhost

**How to evaluate:**

Think about who actually uses this code and what environment it runs in. A
fix for an internal CLI tool doesn't need the same rigor as a fix for a
public-facing API. Match the weight of the fix to the weight of the problem.

**If you find over-engineering**, do not silently simplify. Instead:

1. Explain what you believe is over-engineered and why (e.g., "This retry
   logic handles network partitions, but this service only runs locally
   during development").
2. Present both options clearly:
   - **Option A (current):** The original, more defensive solution.
     Describe what it covers and the cost (lines of code, complexity,
     added dependencies).
   - **Option B (simplified):** A leaner alternative that solves the
     actual problem without the extra guardrails. Describe what it
     drops and why that's acceptable in this context.
3. Ask the user which option they prefer before proceeding.

---

### Checkpoint 2: Production Safety Check

Ask yourself whether this fix would be safe to deploy to production as-is.

**Red flags to watch for:**

- Hardcoding `http://` instead of deriving protocol from the environment
  (e.g., `protocol: "http"` vs `NODE_ENV === "development" ? "http" : "https"`)
- Disabling authentication, CORS, or CSRF protections to "make it work"
- Logging sensitive data (tokens, passwords, PII) that was added for debugging
- Using `eval()`, `dangerouslySetInnerHTML`, or equivalent unsafe APIs without
  justification
- Catching and silently swallowing errors that should propagate
- Leaving `TODO: remove before production` comments as the only safeguard
- Weakening input validation to work around a test case
- Using `*` in CORS origins or overly permissive IAM/permissions

**How to evaluate:**

Imagine this exact diff being merged and deployed with no further review. Would
it pass a security-conscious code review? If not, either fix it now or clearly
flag it as a known debt with a concrete remediation plan.

---

### Checkpoint 3: Performance Impact Check

Ask yourself whether the fix introduces unnecessary runtime cost.

**Red flags to watch for:**

- Adding synchronous I/O or blocking calls in a hot path
- Introducing O(n²) or worse complexity when O(n) is achievable
- Hardcoding test-specific logic behind runtime checks
  (e.g., `if (isTestMode) { ... }` scattered through business logic)
- Adding middleware, interceptors, or hooks that run on every request but
  only serve the debugging scenario
- Fetching data that's already available, or re-computing values that could
  be cached
- Loading entire modules or datasets when only a small subset is needed

**How to evaluate:**

Trace the execution path of your fix during normal (non-debugging) operation.
If it adds work that only exists to support the debug/test scenario, it's
leaking test concerns into production. Restructure so test-specific behavior
lives in test infrastructure, not in application code.

---

### Checkpoint 4: Band-Aid Fix Check

Ask yourself whether the fix actually solves the root cause, or merely
suppresses the symptom.

**Red flags to watch for:**

- Silencing warnings or errors instead of addressing their cause
  (e.g., `deprecation_warnings=False`, `@SuppressWarnings`, `# type: ignore`,
  `eslint-disable` without explanation)
- Wrapping code in a bare `try/except` or `catch` that swallows the real error
- Adding `sleep()`, retry loops, or polling as a workaround for a race
  condition instead of fixing synchronization
- Pinning a dependency to an old version to avoid a breaking change rather
  than migrating
- Setting flags or environment variables to disable a feature that is
  misbehaving instead of fixing it (e.g., `SKIP_VALIDATION=true`)
- Using `any` type casts or force-unwraps to bypass type errors
- Resetting state or clearing caches at suspicious points to "make the
  bug go away"
- Reinventing the wheel instead of using established libraries or built-in
  solutions (e.g., hand-rolling hex encoding instead of using the standard
  library, shelling out to `rsync`/`scp` in Ansible instead of using
  built-in modules like `copy`/`synchronize`, writing custom CSV parsers
  instead of using `csv`/`pandas`)

**How to evaluate:**

Ask: "If I removed this fix, would the underlying problem still exist?" If
yes, you've suppressed a symptom, not fixed the disease. A band-aid is
sometimes acceptable as a short-term measure, but it must be:

1. Clearly documented with a comment explaining what the real fix would be.
2. Tracked (e.g., a TODO with a ticket reference or a concrete follow-up
   plan) so it doesn't become permanent.
3. Flagged to the user — explain that this is a workaround, not a proper
   fix, and let them decide whether to accept it.

---

## Output Format

After running the four checkpoints, present results as follows:

```
### Think Twice — Self-Review

| Checkpoint        | Result                       | Notes           |
|-------------------|------------------------------|-----------------|
| Over-Engineering  | ✅ Proportional / ⚠️ Issue   | (brief summary) |
| Production Safety | ✅ Safe / ⚠️ Risk found      | (brief summary) |
| Performance       | ✅ No impact / ⚠️ Concern    | (brief summary) |
| Band-Aid Fix      | ✅ Root cause / ⚠️ Workaround| (brief summary) |
```

If any checkpoint flags an issue (⚠️), include a **Remediation** section below
the table with specific, actionable changes. Apply these changes before
presenting the final solution to the user.

If all checkpoints pass (✅), do not print the table or mention the review.
Just proceed silently with the solution.

## Important

- This review should feel lightweight — a quick sanity check, not a full audit.
  Aim for 30 seconds of reasoning, not 5 minutes. The value comes from
  consistently catching obvious mistakes, not from exhaustive analysis.
- Do not skip this review just because the fix is "small" or "obvious." Small
  fixes are where the worst blind spots hide.
- If the user explicitly says they want a quick-and-dirty fix or a temporary
  workaround, still run the review but frame findings as "things to clean up
  later" rather than blocking the fix.
