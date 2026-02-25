---
name: code-review-patterns
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: Read, Grep, Glob, LSP
---

# Code Review Patterns

## Overview

Code reviews catch bugs before they ship. But reviewing code quality before functionality is backwards.

**Core principle:** First verify it works, THEN verify it's good.

## Signal Quality Rule

**Flag ONLY when certain. False positives erode trust and waste remediation cycles.**

| Flag | Do NOT Flag |
|------|-------------|
| Will fail to compile/parse (syntax, type, import errors) | Style preferences not in project guidelines |
| Logic error producing wrong results for all inputs | Potential issues dependent on specific inputs/state |
| Clear guideline violation (quote the exact rule) | Subjective improvements or nitpicks |

## Quick Review Checklist (Reference Pattern)

**For rapid reviews, check these 8 items:**

- [ ] Code is simple and readable
- [ ] Functions and variables are well-named
- [ ] No duplicated code
- [ ] Proper error handling
- [ ] No exposed secrets or API keys
- [ ] Input validation implemented
- [ ] Good test coverage
- [ ] Performance considerations addressed

## The Iron Law

```
NO CODE QUALITY REVIEW BEFORE SPEC COMPLIANCE
```

If you haven't verified the code meets requirements, you cannot review code quality.

## Two-Stage Review Process

### Stage 1: Spec Compliance Review

**Does it do what was asked?**

1. **Read the Requirements**
   - What was requested?
   - What are the acceptance criteria?
   - What are the edge cases?

2. **Trace the Implementation**
   - Does the code implement each requirement?
   - Are all edge cases handled?
   - Does it match the spec exactly?

3. **Test Functionality**
   - Run the tests
   - Manual test if needed
   - Verify outputs match expectations

**Gate:** Only proceed to Stage 2 if Stage 1 passes.

### Stage 2: Code Quality Review

**Is it well-written?**

Review in priority order:

1. **Security** - Vulnerabilities that could be exploited
2. **Correctness** - Logic errors, edge cases missed
3. **Performance** - Unnecessary slowness
4. **Maintainability** - Hard to understand or modify
5. **UX** - User experience issues (if UI involved)
6. **Accessibility** - A11y issues (if UI involved)

## Security Review Checklist

**Reference:** [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Check against industry standard vulnerabilities.

| Check | Looking For | Example Vulnerability |
|-------|-------------|----------------------|
| Input validation | Unvalidated user input | SQL injection, XSS |
| Authentication | Missing auth checks | Unauthorized access |
| Authorization | Missing permission checks | Privilege escalation |
| Secrets | Hardcoded credentials | API key exposure |
| SQL queries | String concatenation | SQL injection |
| Output encoding | Unescaped output | XSS attacks |
| CSRF | Missing tokens | Cross-site request forgery |
| File handling | Path traversal | Reading arbitrary files |

### Security Quick-Scan Commands

**Run before any review:**
```bash
# Check for hardcoded secrets
grep -rE "(api[_-]?key|password|secret|token)\s*[:=]" --include="*.ts" --include="*.js" src/

# Check for SQL injection risk
grep -rE "(query|exec)\s*\(" --include="*.ts" src/ | grep -v "parameterized"

# Check for dangerous patterns
grep -rE "(eval\(|innerHTML\s*=|dangerouslySetInnerHTML)" --include="*.ts" --include="*.tsx" src/

# Check for console.log (remove before production)
grep -rn "console\.log" --include="*.ts" --include="*.tsx" src/
```

## LSP-Powered Code Analysis

**Use LSP for semantic understanding during reviews:**

| Task | LSP Tool | Why Better Than Grep |
|------|----------|---------------------|
| Find all callers of a function | `lspCallHierarchy(incoming)` | Finds actual calls, not string matches |
| Find all usages of a type/variable | `lspFindReferences` | Semantic, not text-based |
| Navigate to definition | `lspGotoDefinition` | Jumps to actual definition |
| Understand what function calls | `lspCallHierarchy(outgoing)` | Maps call chain |

**Review Workflow with LSP:**
1. `localSearchCode` → find symbol + get lineHint
2. `lspGotoDefinition(lineHint=N)` → understand implementation
3. `lspFindReferences(lineHint=N)` → check all usages for consistency
4. `lspCallHierarchy(incoming)` → verify callers handle changes

**CRITICAL:** Always get lineHint from localSearchCode first. Never guess line numbers.

**Critical Security Patterns:**

| Pattern | Risk | Detection | Fix |
|---------|------|-----------|-----|
| Hardcoded secret | API key exposure | `grep -r "sk-" src/` | Use env var |
| SQL concatenation | SQL injection | `query(\`SELECT...${id}\`)` | Parameterized query |
| `innerHTML = userInput` | XSS | grep for innerHTML | Use textContent |
| `eval(userInput)` | Code injection | grep for eval | Never eval user input |
| Missing auth check | Unauthorized access | Review API routes | Add middleware |
| CORS `*` | Cross-origin attacks | Check CORS config | Whitelist origins |

**OWASP Top 10 Quick Reference:**
1. Injection (SQL, Command, XSS)
2. Broken Authentication
3. Sensitive Data Exposure
4. XXE (XML External Entities)
5. Broken Access Control
6. Security Misconfiguration
7. Cross-Site Scripting (XSS)
8. Insecure Deserialization
9. Using Vulnerable Components
10. Insufficient Logging

**Full security review:** See [OWASP Top 10](https://owasp.org/www-project-top-ten/)

**For each security issue found:**
```markdown
- [CRITICAL] SQL injection at `src/api/users.ts:45`
  - Problem: User input concatenated into query
  - Fix: Use parameterized query
  - Code: `db.query(\`SELECT * FROM users WHERE id = ?\`, [userId])`
```

## Quality Review Checklist

| Check | Good | Bad |
|-------|------|-----|
| **Naming** | `calculateTotalPrice()` | `calc()`, `doStuff()` |
| **Functions** | Does one thing | Multiple responsibilities |
| **Complexity** | Linear flow | Nested conditions |
| **Duplication** | DRY where sensible | Copy-paste code |
| **Error handling** | Graceful failures | Silent failures |
| **Clarity** | Explicit, readable flow | Nested ternaries, dense one-liners |
| **Testability** | Injectable dependencies | Global state |

## Type Design Red Flags (Typed Languages)

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Exposed mutable internals | External code breaks invariants | Return copies or readonly |
| No constructor validation | Invalid instances created | Validate at construction |
| Invariants in docs only | Not enforced, easily broken | Encode in type system |
| Anemic domain model | Data without behavior | Add methods enforcing rules |

## Hidden Failure Patterns

| Pattern | Why It Hides Failures |
|---------|----------------------|
| `?.` chains without logging | Silently skips failed operations |
| `?? defaultValue` masking | Hides null/undefined source errors |
| Catch-log-continue | User never sees the failure |
| Retry exhaustion without notice | Fails silently after N attempts |
| Fallback chains without explanation | Masks root cause with alternatives |

## Clarity Over Brevity

- Nested ternary `a ? b ? c : d : e` → Use if/else or switch
- Dense one-liner saving 2 lines → 3 clear lines over 1 clever line
- Chained `.map().filter().reduce()` with complex callbacks → Named intermediates

## Pattern Recognition Criteria

**During reviews, identify patterns worth documenting:**

| Criteria | What to Look For | Example |
|----------|------------------|---------|
| **Tribal** | Knowledge new devs wouldn't know | "All API responses use envelope structure" |
| **Opinionated** | Specific choices that could differ | "We use snake_case for DB, camelCase for JS" |
| **Unusual** | Not standard framework patterns | "Custom retry logic with backoff" |
| **Consistent** | Repeated across multiple files | "All services have health check endpoint" |

**If you spot these during review:**
1. Note the pattern in review feedback
2. Include in your **Memory Notes (Patterns section)** - router will persist to patterns.md via Memory Update task
3. Flag inconsistencies from established patterns

## Performance Review Checklist

| Pattern | Problem | Fix |
|---------|---------|-----|
| N+1 queries | Loop with DB call | Batch query |
| Unnecessary loops | Iterating full list | Early return |
| Missing cache | Repeated expensive ops | Add caching |
| Memory leaks | Objects never cleaned | Cleanup on dispose |
| Sync blocking | Blocking main thread | Async operation |

## UX Review Checklist (UI Code)

| Check | Verify |
|-------|--------|
| Loading states | Shows loading indicator |
| Error states | Shows helpful error message |
| Empty states | Shows appropriate empty message |
| Success feedback | Confirms action completed |
| Form validation | Shows inline errors |
| Responsive | Works on mobile/tablet |

## Accessibility Review Checklist (UI Code)

| Check | Verify |
|-------|--------|
| Semantic HTML | Uses correct elements (button, not div) |
| Alt text | Images have meaningful alt text |
| Keyboard | All interactions keyboard accessible |
| Focus | Focus visible and logical order |
| Color contrast | Meets WCAG AA (4.5:1 text) |
| Screen reader | Labels and ARIA where needed |

## Severity Classification

| Severity | Definition | Action |
|----------|------------|--------|
| **CRITICAL** | Security vulnerability or blocks functionality | Must fix before merge |
| **MAJOR** | Affects functionality or significant quality issue | Should fix before merge |
| **MINOR** | Style issues, small improvements | Can merge, fix later |
| **NIT** | Purely stylistic preferences | Optional |

## Multi-Signal Review Methodology

**Each Stage 2 pass produces an independent signal. Score each dimension separately.**

**HARD signals** (any failure blocks approval):
- **Security:** One real vulnerability = dimension score 0
- **Correctness:** One logic error producing wrong output = dimension score 0

**SOFT signals** (concerns noted, don't block alone):
- **Performance:** Scaling concern without immediate impact
- **Maintainability:** Complex but functional code
- **UX/A11y:** Missing states but core flow works

**Aggregation rule:**
1. If ANY HARD signal = 0 → STATUS: CHANGES_REQUESTED (non-negotiable)
2. CONFIDENCE = min(HARD scores), reduced by max 10 if SOFT signals are low
3. Include per-signal breakdown in Router Handoff for targeted remediation

**Evidence requirement per signal:**
Each signal MUST cite specific file:line. A signal without evidence = not reported.

## Do NOT Flag (False Positive Prevention)

- Pre-existing issues not introduced by this change
- Correct code that merely looks suspicious
- Pedantic nitpicks a senior engineer would not flag
- Issues linters already catch (don't duplicate tooling)
- General quality concerns not required by project guidelines
- Issues explicitly silenced via lint-ignore comments

## Priority Output Format (Feedback Grouping)

**Organize feedback by priority (from reference pattern):**

```markdown
## Code Review Feedback

### Critical (must fix before merge)
- [95] SQL injection at `src/api/users.ts:45`
  → Fix: Use parameterized query `db.query('SELECT...', [userId])`

### Warnings (should fix)
- [85] N+1 query at `src/services/posts.ts:23`
  → Fix: Batch query with WHERE IN clause

### Suggestions (consider improving)
- [70] Function `calc()` could be renamed to `calculateTotal()`
  → More descriptive naming
```

**ALWAYS include specific examples of how to fix each issue.**
Don't just say "this is wrong" - show the correct approach.

## Red Flags - STOP and Re-review

If you find yourself:

- Reviewing code style before checking functionality
- Not running the tests
- Skipping the security checklist
- Giving generic feedback ("looks good")
- Not providing file:line citations
- Not explaining WHY something is wrong
- Not providing fix recommendations

**STOP. Start over with Stage 1.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Tests pass so it's fine" | Tests can miss requirements. Check spec compliance. |
| "Code looks clean" | Clean code can still be wrong. Verify functionality. |
| "I trust this developer" | Trust but verify. Everyone makes mistakes. |
| "It's a small change" | Small changes cause big bugs. Review thoroughly. |
| "No time for full review" | Bugs take more time than reviews. Do it properly. |
| "Security is overkill" | One vulnerability can sink the company. Check it. |

## Output Format

```markdown
## Code Review: [PR Title/Component]

### Stage 1: Spec Compliance ✅/❌

**Requirements:**
- [x] Requirement 1 - implemented at `file:line`
- [x] Requirement 2 - implemented at `file:line`
- [ ] Requirement 3 - NOT IMPLEMENTED

**Tests:** PASS (24/24)

**Verdict:** [Meets spec / Missing requirements]

---

### Stage 2: Code Quality

**Security:**
- [CRITICAL] Issue at `file:line` - Fix: [recommendation]
- No issues found ✅

**Performance:**
- [MAJOR] N+1 query at `file:line` - Fix: Use batch query
- No issues found ✅

**Quality:**
- [MINOR] Unclear naming at `file:line` - Suggestion: rename to X
- No issues found ✅

**UX/A11y:** (if UI code)
- [MAJOR] Missing loading state - Fix: Add spinner
- No issues found ✅

---

### Summary

**Decision:** Approve / Request Changes

**Critical:** [count]
**Major:** [count]
**Minor:** [count]

**Required fixes before merge:**
1. [Most important fix]
2. [Second fix]
```

## Review Loop Protocol

After requesting changes:

1. **Wait for fixes** - Developer addresses issues
2. **Re-review** - Check that fixes actually fix the issues
3. **Verify no regressions** - Run tests again
4. **Approve or request more changes** - Repeat if needed

**Never approve without verifying fixes work.**

## Final Check

Before approving:

- [ ] Stage 1 complete (spec compliance verified)
- [ ] Stage 2 complete (all checklists reviewed)
- [ ] All critical/major issues addressed
- [ ] Tests pass
- [ ] No regressions introduced
- [ ] Evidence captured for each claim
