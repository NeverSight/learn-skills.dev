---
name: unblock
description: >
  Structures coding tasks around Unblocked MCP context. Hydrates a plan with
  organizational knowledge (PRs, Slack, Jira, docs, code history), submits it
  for critical review against team patterns, then generates and reviews code.
  Two mandatory review gates prevent pattern mismatches and reinvented wheels.
  Use for any code change: features, bug fixes, refactors, or investigations.
---

# Unblocked Dev Workflow

Every coding task follows a strict loop. **No code is written until the plan has been
reviewed by Unblocked, and no code is considered done until it has been verified against
context.** This catches problems at both ends — before code is written and after.

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  1. HYDRATE        (Unblocked)                               │
│     │              Query context from connected data         |
|     |              sources like PRs, Slack,                  │
│     │              Jira, docs, code history                  │
│     ▼                                                        │
│  2. DRAFT PLAN     (Agent)                                   │
│     │              Design implementation using               │
│     │              hydrated context                          │
│     ▼                                                        │
│  3. REVIEW PLAN    (Unblocked)                      ◄──┐     │
│     │              Critically evaluate the plan        │     │
│     │              against org knowledge               │     │
│     ▼                                                  │     │
│  4. REVISE PLAN    (Agent)                             │     │
│     │              Incorporate feedback                │     │
│     │              [Major issues] ─────────────────────┘     │
│     │              [Minor/none]                              │
│     ▼                                                        │
│  5. GENERATE CODE  (Agent)                                   │
│     │              Implement the validated plan              │
│     ▼                                                        │
│  6. REVIEW CODE    (Unblocked)                      ◄──┐     │
│     │              Verify generated code against       │     │
│     │              context, patterns, conventions      │     │
│     ▼                                                  │     │
│  7. REVISE CODE    (Agent)                             │     │
│     │              Fix issues found in review          │     │
│     │              [Issues found] ─────────────────────┘     │
│     │              [Pass]                                    │
│     ▼                                                        │
│     DONE                                                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

Labels: **(Unblocked)** = query Unblocked MCP tools; **(Agent)** = the AI coding agent executes this phase.

**Both review gates are mandatory.** The plan review prevents writing wrong code. The code
review catches what slipped through — pattern mismatches, missed conventions, and gaps
between what was planned and what was generated.

## Principles

- **Multiple specific queries > one broad query.** Ask 3-4 focused questions, not one vague one.
- **Two review gates, not one.** The plan review prevents writing wrong code. The code review catches what slipped through. Both are mandatory.
- **Plans must be specific enough to review.** If the plan is vague, the review can't catch problems. Name files, reference patterns, cite decisions.
- **Default to existing patterns.** When Unblocked shows the team does something a certain way, follow it — even if you think another way is "better." Consistency wins.
- **Loop back, don't patch forward.** If either review finds issues, loop back and fix them properly. Don't try to compensate in the next phase.

## Scaling to Task Size

Not every change needs equal ceremony. Scale the workflow to fit the task:

- **Trivial changes** (typo fix, rename, one-line config tweak): Skip to Phase 5 (Generate Code), but always run Phase 6 (Review Code) before finishing.
- **Small changes** (add a helper, adjust logic in one file): Run Phases 1-2 lightly — one or two queries — then proceed through the rest.
- **Standard changes** (new feature, bug fix, refactor): Run the full workflow as written.
- **Large changes** (cross-cutting refactor, new subsystem): Run the full workflow, expect multiple review loops, and consider breaking the task into smaller pieces.

**When in doubt, run the full workflow.** The cost of an unnecessary hydration query is seconds; the cost of missing context is a rewrite. Even the abbreviated path for trivial changes keeps the code review gate (Phase 6).

## Reference Workflows

For specialized task types, load the relevant reference file for additional guidance:

- **Debugging a bug** → `references/debugging-context.md` — investigation structure for root cause analysis
- **Implementing a feature** → `references/feature-context.md` — discovery workflow for touch points and constraints
- **Exploring unfamiliar code** → `references/exploring-context.md` — architecture and convention discovery queries

---

## Phase 1: Hydrate Context (Unblocked)

Before planning, gather context from Unblocked. Run **multiple targeted queries** — specific
questions dramatically outperform broad ones.

**Required queries (run all of these):**

1. `unblocked_context_engine`: "How does [feature area] work in this codebase?"
2. `unblocked_context_engine`: "What conventions does the team follow for [relevant pattern]?"
3. `historical_context`: "What decisions were made about [related area]?"
4. `data_retrieval`: recent PRs and issues related to the area being changed

**Also query for potential pitfalls:**

5. `historical_context`: "Has the team tried [this kind of change] before? What happened?"
6. `unblocked_context_engine`: "What are the known gotchas or edge cases in [area]?"

**Example** — "add rate limiting to the API":
```
unblocked_context_engine: "How does the API middleware pipeline work?"
unblocked_context_engine: "Are there existing rate limiting or throttling mechanisms?"
unblocked_context_engine: "What patterns does the team use for middleware configuration?"
historical_context: "What decisions were made about API authentication and middleware?"
historical_context: "Has rate limiting been attempted or discussed before?"
data_retrieval: "PRs merged in the last 2 weeks touching the API layer"
```

**Collect and carry forward:**
- Existing modules to extend (not reinvent)
- Naming conventions and code style patterns
- Architectural patterns the team actually uses
- Related recent work that might conflict or coordinate
- Prior decisions and rejected approaches
- Known edge cases and gotchas

**All of this context feeds into Phase 2. Do not start planning without it.**

---

## Phase 2: Draft Plan (Agent)

Design the implementation **referencing specific findings from Phase 1**. The plan must
reflect the team's actual patterns, not generic best practices.

**The plan should explicitly:**

- Name the existing modules, utilities, and patterns it will follow (from Phase 1)
- Call out how it aligns with prior team decisions discovered during hydration
- Note any area where the plan diverges from existing patterns and explain why
- Identify files that will be created or modified
- Describe the approach at enough detail that it can be critically reviewed

**Do NOT write vague plans.** A plan that says "add middleware for rate limiting" cannot be
meaningfully reviewed. A plan that says "add a `rateLimiter` middleware in `src/middleware/`
following the same pattern as `authMiddleware`, using the `express-rate-limit` library that's
already in `package.json`, storing counters in Redis via the existing `src/lib/redis` client"
can be.

---

## Phase 3: Review Plan (Unblocked)

**CRITICAL GATE — Do not skip this phase.**

Before writing any code, submit the plan to Unblocked for critical review. The goal is to
catch problems when they're cheap to fix — before they become code.

**Required queries (run all of these, referencing the specific plan):**

1. `unblocked_context_engine`: "We plan to [summarize approach]. Does this align with how
   [related system] works in this codebase? Are there existing patterns we should follow
   instead?"

2. `unblocked_context_engine`: "We plan to modify/create [specific files]. What do we need
   to know about these files and their dependencies? Are there conventions for how changes
   in this area are typically structured?"

3. `historical_context`: "Has the team tried [planned approach] before? Were there any
   problems or rejected alternatives?"

4. `unblocked_context_engine`: "What could go wrong with [planned approach]? Are there
   edge cases, performance concerns, or integration issues we should consider?"

**What you're looking for in the review:**

- **Pattern mismatches:** The plan uses approach X, but the team already has an established
  way to do this (approach Y). This is the #1 thing the review catches.
- **Missing context:** The plan doesn't account for a related system, a recent change, or
  a known constraint that Unblocked surfaces.
- **Rejected approaches:** The team tried this before and it didn't work, or explicitly
  decided against it.
- **Naming/convention violations:** The plan introduces names, structures, or patterns that
  don't match the codebase.
- **Scope blindness:** The plan misses files or systems that need to change together.

**After reviewing the Unblocked responses, explicitly state:**
- What the review found (even if everything looks good)
- Whether the plan needs revision
- What specific changes are needed

---

## Phase 4: Revise Plan (Agent)

Incorporate all feedback from the plan review. This is not cosmetic — if Unblocked surfaced
that the team already does something a different way, the plan must change to match.

**For each piece of feedback from Phase 3:**
- State what was found
- State how the plan is being updated
- If you disagree with the feedback, explain why (but default to matching existing patterns)

**If the revision is major** (changed approach, different files, new dependencies), **loop
back to Phase 3** and run the plan review again on the revised plan. Minor revisions
(naming fixes, adding a missing import, adjusting a detail) do not need re-review.

**Present the final revised plan to the user before proceeding to codegen.**

---

## Phase 5: Generate Code (Agent)

Implement the validated, reviewed plan. The plan has been grounded in real context and
reviewed against organizational knowledge — now execute it.

**During codegen:**
- Follow the plan. Don't deviate from reviewed decisions without reason.
- If you encounter something unexpected that contradicts the plan, pause and re-query
  Unblocked rather than guessing.
- If a build or runtime error occurs, use `failure_debugging` with the error message
  and surrounding context. This often surfaces known issues or past fixes.

---

## Phase 6: Review Code (Unblocked)

**CRITICAL GATE — Do not skip this phase.**

After codegen, verify the generated code against organizational context. The plan review
caught problems in the approach — this step catches problems in the execution.

**Required queries (run all of these, referencing the actual code that was written):**

1. `unblocked_context_engine`: "We wrote [summarize what was generated — new files, modified
   files, key patterns used]. Does this match how the team typically implements [this kind of
   thing] in this codebase?"

2. `unblocked_context_engine`: "Looking at [specific pattern/approach in generated code],
   is this consistent with the conventions in [area of codebase]? Are there existing utilities
   or helpers we should be using instead?"

3. `unblocked_context_engine`: "What are the team's testing conventions for [area changed]?
   Do the changes we made follow those patterns?"

4. `historical_context`: "Have there been issues in the past with [the approach taken in
   generated code] in this area of the codebase?"

**What you're looking for in the review:**

- **Reinvented wheels:** The code creates something that already exists as a utility, helper,
  or shared module in the codebase. This is the #1 thing the code review catches.
- **Convention drift:** The code works but doesn't match how the team writes this kind of
  code — wrong error handling pattern, different naming style, non-standard file organization.
- **Missing patterns:** The team has established patterns for this kind of change (e.g.,
  always add a migration, always update the API docs, always emit an event) that the
  generated code doesn't follow.
- **Context gaps:** The code doesn't account for something Unblocked surfaces — a related
  system that needs updating, a known edge case, a constraint from a dependent service.

**After reviewing the Unblocked responses, explicitly state:**
- What the review found (even if everything looks clean)
- Whether the code needs revision
- What specific changes are needed

---

## Phase 7: Revise Code (Agent)

Fix all issues surfaced by the code review. These are not suggestions — if Unblocked showed
that the team does something a different way, the code must change to match.

**For each issue from Phase 6:**
- State what was found
- State what is being changed
- Make the fix

**If the revision is significant** (new files, changed approach, different utilities), **loop
back to Phase 6** and run the code review again. Small fixes (rename a variable, swap to an
existing utility, add a missing import) do not need re-review.

**After all issues are resolved, present a summary to the user:**
- What was built
- What the plan review caught and changed
- What the code review caught and fixed
- Any remaining considerations or follow-ups

---

## Tool Selection

| Question | Tool |
|---|---|
| How/why does X work? | `unblocked_context_engine` |
| What was decided about X? | `historical_context` |
| Recent PRs/issues in area X | `data_retrieval` |
| Contents of a specific PR/issue URL | `link_resolver` |
| Debug a build/runtime failure | `failure_debugging` |
