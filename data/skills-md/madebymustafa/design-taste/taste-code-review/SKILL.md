---
name: taste-code-review
description: |
  Structured review of agent-generated code: a fixed pass order (behavior → structure → taste → security → performance → accessibility), severity-ranked findings, diff discipline, and a review checklist that stops "it works" from being the bar. Use when auditing any generated or changed code. Stack on the design-taste core skill.
triggers:
  - "code review"
  - "review my code"
  - "pull request"
  - "code audit"
  - "pr review"
  - "generated code"
---

# taste-code-review

> "It works" is the floor. Review in passes, not vibes — an agent that reviews without a method reviews without a memory.

## 1. THE PASS ORDER (Fix In This Order, Never Reversed)

1. **Behavior** — does it do the thing, including edge cases (empty states, error paths, repeated clicks, offline)? A feature that works for the happy path only is a bug wearing a feature.
2. **Structure** — is the code where it belongs? (File/component boundaries, one responsibility per unit, no 400-line function, imports clean, no dead code.)
3. **Taste** — naming, duplication, consistency with the codebase's conventions. Code that reads like poetry nobody asked for is worse than code that reads like a bus schedule — but a bus schedule with descriptive stops is best.
4. **Security** — injection (HTML/URL/SQL), secrets in code or logs, authz on every mutation, untrusted input boundaries.
5. **Performance** — obvious algorithmic waste, N+1 queries, work repeated per render, giant payloads in the critical path.
6. **Accessibility** — keyboard path, focus states, contrast, semantics, screen-reader names (the taste-accessibility checklist applies to code too).

Passes are ordered because a structural fix invalidates a line-level review — review the shape before the details.

## 2. FINDINGS (Severity-Ranked, Written To Be Acted On)

- Every finding gets: **severity** (blocker / should-fix / nit), **location** (file:line), **the problem in one sentence**, **the fix in one sentence**. A review with no location or no fix is a complaint, not a review.
- Blockers: wrong behavior, security holes, data loss, breaking the design system (see taste-code-craft).
- Should-fix: duplication, dead code, naming drift, missing edge handling, performance landmines.
- Nits: formatting, naming opinions — flagged but never blocking.
- **Never exceed ~10 findings on a diff that deserves fewer.** If everything's a blocker, the pass order was skipped, not the review.

## 3. DIFF DISCIPLINE (The Review Starts Before the Code)

- Review the smallest logical change: a PR that mixes a rename with a feature with a bugfix is three PRs wearing a trench coat — reject the packaging, keep the code.
- Read the diff as a series of decisions, not a stream of changes: "why does this exist" beats "what did it do".
- Generated code gets the same bar as written code — an agent that generated the code is not excused from reviewing it.
- Review the tests too: a test that only asserts the happy path is a marketing document, not a test.

## 4. THE FINAL QUESTION

Before signing off, one question: **would I merge this if I'd written it myself?** If the answer is no, say why in one sentence. If the answer is yes, the review passes with the findings attached — not everything must be perfect, but everything must be deliberate.

## 5. CHECKLIST (Fail the Review If…)

- [ ] Findings not ordered by severity or missing locations.
- [ ] No edge-case pass (empty/error/repeat/offline) recorded.
- [ ] Security pass skipped because "it's just a landing page".
- [ ] No check that the code matches the repo's existing conventions.
- [ ] Tests absent or happy-path-only for changed behavior.
- [ ] A generated-code diff reviewed with a lower bar than a human one.
- [ ] The review says "looks good" without the passes behind it.