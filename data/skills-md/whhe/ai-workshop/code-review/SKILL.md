---
name: code-review
description: "Risk-priority code review with proportional verification and an optional fix loop. Use when the user asks to review code changes, evaluate merge readiness, audit for security or performance risks, or identify regressions in a branch or PR."
---

IRON LAW: Every finding MUST cite file, line range, and code evidence. No evidence = no finding.

# Code Review — Risk-Priority with Proportional Verification

## Workflow

- [ ] Step 1: Preflight ⚠️ REQUIRED
- [ ] Step 2: Risk-Priority Audit (Passes A–F) ⚠️ REQUIRED
- [ ] Step 3: Present Findings ⚠️ REQUIRED
- [ ] Step 4: Fix Loop (conditional — scope set by Step 3)
- [ ] Step 5: Pre-Publish Self-Check ⚠️ REQUIRED

### 1. Preflight — Establish Baseline ⚠️ REQUIRED

Collect in parallel:

- Branch state: `git status --short --branch`
- Commits vs base: `git log --oneline --decorate --no-merges <base>..HEAD`
- Change scope: `git diff --stat <base>...HEAD` and `git diff --name-only <base>...HEAD`

Default `base` to `main`; override if user specifies another branch.
For a **PR URL**, use the platform API to fetch diff and metadata (description, comments, CI status).

Explore related modules, usages, contracts, entry points, ownership boundaries, and critical paths.

### 2. Risk-Priority Audit ⚠️ REQUIRED

Review **all commits** on the branch. Execute passes in order.

#### Pass A — Behavioral Regression & Compatibility

- Did any branch logic, default value, feature flag, or input/output contract change?
- Are API parameters, defaults, and legacy-data handling backward-compatible?
- Does naming/return-value semantics match the existing codebase? Flag "interface says X, implementation does Y" drift.

For every change impacting existing logic, state: original behavior → new behavior, impact scope, risk.

#### Pass B — SOLID & Architecture

- **SRP**: Does this module have exactly one reason to change?
- **OCP**: Can a new variant be added without editing existing code?
- **LSP**: Can any subclass substitute the parent without the caller knowing?
- **ISP**: Do all implementers use all interface methods?
- **DIP**: Is business logic tied to concrete I/O, storage, or hardcoded values?
- Overly loose types (`Any`/`any`/`dict`/untyped) masking domain constraints?

Prefer incremental refactor plans over large rewrites. Load [solid-checklist.md](references/solid-checklist.md) for deeper smell prompts.

#### Pass C — Security & Reliability

- Can an unauthenticated or unauthorized user reach this code path? Could tenant A's data leak to tenant B?
- What happens if two requests hit this code simultaneously? Could state change between check and act?
- If this operation fails halfway, is data left consistent?
- Unpinned deps, dependency confusion, known CVEs?
- TLS verification disabled on HTTP clients (`verify=False`, `InsecureSkipVerify`, `rejectUnauthorized: false`)?

Call out both **exploitability** and **impact**. Load [security-checklist.md](references/security-checklist.md) for deeper threat-model analysis.

#### Pass D — Performance & Stability

- What if this runs with 10×/100× data? Are resources bounded and released?
- N+1 queries? CPU-intensive work in a hot path that could be cached or batched?
- On failure: enough context to debug? Secrets leaked in logs or error output?
- What if this value is null, 0, or empty?

Load [code-quality-checklist.md](references/code-quality-checklist.md) for detailed sub-checks.

#### Pass E — Removal Candidates

- Identify unused, redundant, or feature-flagged-off code.
- Distinguish **safe delete now** vs **defer with plan**.

Load [removal-plan.md](references/removal-plan.md) if candidates are found.

#### Pass F — Test Coverage & Language-Specific Checks

- Decide whether the changed observable contract has enough discriminating verification for its risk. Reuse existing tests and checks before adding new ones.
- Missing tests count as regression risk only when the changed logic is materially unverified and the risk cannot be covered by a smaller existing, static, or manual check.
- For a bug fix, add a focused regression test only when the current suite fails to catch the original failure and the case is stable and valuable to preserve. Do not add a duplicate when an existing discriminating test already fails on that same original failure before the fix, or when the change is documentation, configuration, wiring-only, or behavior-preserving refactoring.
- Require integration-level coverage only when a cross-module contract or boundary is not meaningfully verified by focused checks. Do not duplicate unit and integration tests that prove the same observable outcome.
- **Assertion discriminability**: verify fixtures and assertions can distinguish real behavior from bypass/no-op — including cases where filtered and unfiltered results would look the same under the data you used, or where one happy path cannot prove a branch ran. Strengthen with cardinality, identity or negative cases, or observable effects appropriate to the feature.

Language-specific gotchas (non-obvious items the general passes may miss):

| Language | Check | Flag when | Pass |
|----------|-------|-----------|------|
| Python | Naive/aware `datetime` mixing | Naive and aware datetime objects compared, subtracted, or assigned to the same field without explicit conversion | A |
| Python | ORM lazy-load on detached instance | An ORM relationship or deferred column is accessed after the session that loaded the object is closed | D |
| Python | ORM dialect portability | Queries rely on engine-specific SQL or vendor-only functions, raw SQL fragments, or dialect-only types instead of APIs the ORM can translate for every backend the project supports. Confirm compilation or execution against each dialect/version in that supported set | A, D |
| TS/React | `useEffect`/`useMemo`/`useCallback` dependency issues | A reactive dependency is missing, redundant, or is an unstable reference (new object/array/function created each render) | D |
| JS/Node | Global patches/polyfills without guards | A monkey-patch or polyfill executes unconditionally — no environment check, feature detection, or scope isolation | A |

### 3. Present Findings ⚠️ REQUIRED

**Report first** — present findings before making any changes.
Load [output-template.md](references/output-template.md) for document structure, severity levels, and evidence rules.

After presenting:
- If the user's original request **explicitly included fixing** (e.g., "review and fix", "fix everything", "review then fix all issues"): automatically proceed to Fix Loop for **all findings** — no confirmation needed. Override the default only if the user explicitly scoped the fix (e.g., "fix High only"). **Negative examples** — these do NOT count as fix requests: "review this fix", "review my bugfix branch", "check if this fix is correct" — here "fix" describes existing work, not an instruction to apply fixes.
- Otherwise: ask user how to proceed (fix all / fix High only / fix specific items / no changes). Do NOT implement changes until user confirms.

### 4. Fix Loop (conditional)

⛔ Enter only after Step 3 determines the fix scope. Fix only issues within that scope.

Each iteration:

1. Run the smallest relevant verification to establish a pre-fix baseline.
2. Apply the minimal fix (avoid introducing new behavior), adding or updating a targeted test only when the risk assessment above shows that it is needed to protect the changed contract.
3. Re-run the same verification to confirm the fix.
4. **Adversarial re-review** of the **entire diff** — same scope as Step 1 Preflight (`<base>..HEAD` or all uncommitted changes, now including any fixes applied so far). Do NOT scope the review to only the latest patch; fixes can introduce regressions elsewhere in the change.

   The re-review must be **adversarial**: its default stance is that the fix introduced new problems. The reviewer must actively try to refute the fix's correctness before accepting it. Only flag issues that would cause observable failure in production or violate a documented contract — theoretical concerns that require multiple unlikely preconditions do not count as findings.

   **Iteration equivalence**: every re-review — whether iteration 1 or 3 — must start from the same baseline context: project structure, conventions, and the current full diff. No prior re-review findings, fix rationale, or iteration history may carry forward. Only the diff content differs across iterations (it grows as fixes accumulate).

   - **Preferred**: spawn a fresh subagent per iteration (iteration equivalence is automatic — each subagent starts with zero prior context). The prompt must:
     1. Provide only the full diff and project context — no description of the fix intent or rationale.
     2. Instruct: "Your job is to find problems in these changes. Default to 'this is wrong' and require evidence to accept. For each modified region, attempt to construct a realistic scenario where the code fails (e.g., edge cases, concurrency, null/empty inputs, type mismatches, caller breakage — adapt to what is relevant). Only flag issues that would cause observable failure in production or violate a documented contract — theoretical concerns that require multiple unlikely preconditions do not count. Mark clean if you cannot construct such a scenario after trying."
     3. Apply Passes A, C, D, F with the adversarial stance (skip B and E — re-review targets regressions, not architecture or cleanup).
   - **Fallback** (subagents unavailable): to satisfy iteration equivalence, reset context before each re-review — discard all prior re-review findings, fix rationale, and iteration history, then re-read the full diff from scratch (`git diff` or `git diff <base>..HEAD`). Apply Passes A, C, D, F as if this were the first and only re-review (skip B and E — re-review targets regressions, not architecture or cleanup). Before each pass, ask: "How could the changes in this pass be wrong?" Quality degrades across iterations as accumulated context becomes harder to discard — prefer the subagent path when available.
5. Expand scope only if the re-review (step 4) surfaces new issues within the agreed fix scope. If out-of-scope findings are discovered, record them in the Fix Loop Iterations table and report to user at the end of the Fix Loop.

Cap at **3 iterations**. If still unstable or if in-scope findings remain after the final re-review, stop and report to user before proceeding.

**Iteration tracking**: Record each iteration's findings and fixes. The final report must include a per-iteration summary (iteration number, issue addressed, fix applied, verification result, re-review outcome) so the user can trace the fix history (see [output-template.md](references/output-template.md) § Fix Loop Iterations).

Test strategy (adapt per project):

- Run the smallest existing check that exercises the changed contract, then broaden only when the change crosses a boundary or the focused check reveals a relevant dependency.
- **Python**: run the target test or existing focused check first, then the related directory only when warranted by the change.
- **Frontend**: run the affected component/page check first, then related suites only when the change crosses their contract.
- **API changes**: verify the changed request/response or error contract with existing coverage; add one discriminating case only when that contract is otherwise unverified.
- Do not create tests solely to increase coverage, mirror implementation branches, or make a report look complete. A test that cannot fail for a plausible regression is not useful. Record why no new test was needed when existing checks or the low-risk scope are sufficient.
- **Missing prerequisites** (command not found, deps missing): state "unverified" with impact scope; provide reproducible commands; never fake results.

### 5. Pre-Publish Self-Check ⚠️ REQUIRED

Run the self-check in [output-template.md](references/output-template.md) § Pre-Publish Self-Check before finalizing.

## Constraints & Anti-Patterns

**Never:**

- Dismiss implicit behavior changes from default-value modifications.
- Label an unverified item as "passed."
- Bypass critical checks to make tests pass (removing auth, swallowing exceptions, downgrading security).
- Commit or push without explicit user request.
- Make fixes before presenting findings.

**Avoid:**

- Listing style/naming issues before security and correctness.
- Reporting "no issues found" without listing what was checked.
- Copy-pasting code without explaining what is wrong.
- Treating all findings as equal severity.
- Guessing at behavior instead of reading actual code and diff.

## Resources

Load on demand — only when a finding needs deeper analysis.

| File | When to load |
|------|--------------|
| [solid-checklist.md](references/solid-checklist.md) | Pass B finding needs smell prompts or refactor heuristics |
| [security-checklist.md](references/security-checklist.md) | Pass C finding needs threat-model detail |
| [code-quality-checklist.md](references/code-quality-checklist.md) | Pass D finding needs stability/performance sub-checks |
| [removal-plan.md](references/removal-plan.md) | Pass E found removal candidates |
| [output-template.md](references/output-template.md) | Step 3 & 5 — document structure, evidence rules, self-check |
