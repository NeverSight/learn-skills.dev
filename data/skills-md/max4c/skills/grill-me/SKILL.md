---
name: grill-me
description: Interview the user relentlessly about a plan, spec, or ticket until every branch of the decision tree is resolved. Produces a per-dimension ambiguity report (Goals / Acceptance / Boundaries / Alternatives / Assumptions) and an aggregate gate. Use this skill whenever the user is drafting a spec, proposing a design, debating an approach, or describing work to hand off — even if they don't say "grill me". Explicit triggers include "grill me", "stress-test this", "am I missing anything", "what are the risks", or any time a non-trivial plan is being finalized. Also invoked as a subroutine by max:write-prd Phase 5, max:tech-spec Phase 6, max:improve-codebase Phase 5, bugbook:flow Phase 2d, bugbook:prep Phase 3, and bugbook:ticket Phase 2d.
---

# Grill Me

Interview relentlessly about every aspect of the artifact until we reach shared understanding. Walk each branch of the decision tree, resolving dependencies one-by-one. For each question, provide your recommended answer.

Ask one question at a time. If a question can be answered by exploring the codebase, explore instead of asking.

The goal: a spec, ticket, or plan that an agent with zero context could execute without asking the user anything.

---

## Composition

This skill is designed to be called directly by the user AND invoked as a subroutine by other skills that need active interrogation. Known callers:

- `max:write-prd` — Phase 5 grill gate against the drafted PRD
- `max:tech-spec` — Phase 6 grill gate against the drafted tech spec
- `max:improve-codebase` — Phase 5 grill gate against the architectural proposal
- `bugbook:flow` — Phase 2d spec grill (via `max:write-prd`, indirectly) plus fallback direct invocation
- `bugbook:prep` — Phase 3 ticket grill for "needs input" tickets
- `bugbook:ticket` — Phase 2d spec grill for non-trivial feature-tier tickets

When invoked as a subroutine, the caller pre-loads the artifact into the conversation. You detect the mode from context (what's being grilled) and follow the subroutine exit protocol — write resolved answers back to the artifact before returning control to the caller.

## Modes

Detect from context:

- **Freeform** — standalone "grill me". Target is whatever plan or design is currently in the conversation. Threshold: 0.4.
- **Spec** — invoked from a caller that's drafting a project spec (e.g., `bugbook:flow` Phase 2d or `max:write-prd` Phase 5). Read the spec artifact, then grill section by section (Goals, Requirements, Non-Goals, Constraints, Approach, Open Questions). Threshold: 0.2 (strict).
- **Ticket** — invoked from a caller auditing a single work item (e.g., `bugbook:prep` Phase 3). Read the ticket body, then grill only on the audit-flagged gaps — not the whole ticket. Threshold: 0.3.

If the mode is ambiguous, ask. It usually isn't.

---

## What to target

The decisions that cause wasted work downstream, grouped by the five ambiguity dimensions:

- **Goals** — where would two reasonable people build different things? Is the outcome specific enough to distinguish "done" from "almost done"?
- **Acceptance** — can a machine verify "done"? Are the success criteria concrete behaviors, not aspirations?
- **Boundaries** — what's tempting to touch that should stay untouched? Are Non-Goals explicit?
- **Alternatives** — what did we rule out, and why? What did we NOT consider that we should have?
- **Assumptions** — which codebase facts are being guessed at? Which constraints are we trusting without evidence?

Plus, for retries only:

- **Iteration context** — what specifically prevents repeating the previous failure? Is the previous attempt's root cause clearly understood?

---

## Ambiguity scoring (the exit discipline)

At exit, judge each of the five dimensions on this rubric. Score qualitatively — don't count questions or do arithmetic. The LLM is already assessing clarity during the interview; let that judgment speak directly.

### The 0-to-1 rubric

| Score | Label | What it means |
|---|---|---|
| **0.0** | Clear | Every claim is specific, verifiable, and unambiguous. An outside agent could execute without asking. |
| **0.25** | Mostly clear | One or two minor gaps. The intent is obvious; small details are inferred from context. |
| **0.5** | Mixed | Some parts are crisp, others are vague. An agent would need to make judgment calls that could go either way. |
| **0.75** | Mostly vague | Intent is directional, details are soft. An agent would likely pick a different interpretation than the user intended. |
| **1.0** | Fully ambiguous | Aspirational language, no concrete criteria, unresolved fundamentals. An agent would guess wildly. |

### Per-dimension anchors

**Goals (what we're building)**
- 0.0 — "Users can filter tickets by priority with p95 response time under 50ms on a 10k-ticket dataset."
- 0.25 — "Fast filtering by priority." (missing concrete latency target but behavior is clear)
- 0.5 — "Better ticket browsing." (direction is clear, scope is not)
- 0.75 — "Improve the ticket experience."
- 1.0 — "Make tickets good."

**Acceptance (done-when criteria)**
- 0.0 — Numbered checklist of verifiable outcomes. Each item can be tested by a computer or a reviewer with specific steps.
- 0.25 — Checklist exists but one or two items use subjective language ("feels fast", "looks good").
- 0.5 — Criteria describe the intended behavior in prose but a reviewer would need to interpret them.
- 0.75 — "Working", "done", "shipped" without concrete verification steps.
- 1.0 — No acceptance criteria at all.

**Boundaries (what NOT to touch)**
- 0.0 — Explicit Non-Goals section listing files/behaviors/scope that are out of scope, with reasons.
- 0.25 — Non-Goals exist but incomplete — one obvious scope-creep risk isn't mentioned.
- 0.5 — General statement of scope ("just the sidebar") without enumerating what's excluded.
- 0.75 — No boundaries stated; scope is whatever the agent thinks it should be.
- 1.0 — Clear scope creep risk with no guardrails.

**Alternatives (what we ruled out)**
- 0.0 — 2-3 alternatives considered with explicit tradeoffs and the reason the chosen approach won.
- 0.25 — Main alternative considered, reason for rejection stated, but other plausible options not examined.
- 0.5 — Chosen approach is described without any discussion of alternatives.
- 0.75 — Chosen approach is justified only by "it's how we do it" or "it's the obvious choice" without examining why.
- 1.0 — No mention of alternatives; the first idea is the plan.

**Assumptions (what we're trusting)**
- 0.0 — Every load-bearing assumption is named and verified (codebase checked, constraints confirmed).
- 0.25 — Assumptions named but one or two rely on memory rather than verification.
- 0.5 — Mix of verified and hand-waved assumptions.
- 0.75 — Most assumptions are unstated; the plan relies on things being "like they usually are".
- 1.0 — Unverified guesses treated as facts.

### Aggregate and thresholds

Aggregate = mean of the five dimensions.

| Mode | Threshold | Meaning |
|---|---|---|
| Spec | 0.2 | Strict. Specs feeding into autonomous overnight execution need to be airtight. |
| Ticket | 0.3 | Moderate. Tickets are smaller units and can absorb some ambiguity. |
| Freeform | 0.4 | Loose. Exploratory grilling benefits from letting conversation wander without tripping the gate. |

---

## Exit procedure

1. **Judge each dimension.** Using the rubric, assign a score 0/0.25/0.5/0.75/1.0 to each of Goals, Acceptance, Boundaries, Alternatives, Assumptions.
2. **Compute aggregate** as the mean.
3. **Print the report** in this exact format:

```
Ambiguity Report:
  Goals:        0.25  ⚠ one gap
  Acceptance:   0.1   ✓ clear
  Boundaries:   0.0   ✓ clear
  Alternatives: 0.5   ⚠ underexplored
  Assumptions:  0.1   ✓ clear
  ──────────────────────────────
  Aggregate:    0.19  ✓ below threshold (0.2 spec)

Push lightly on: goals specificity, alternatives.
```

Use `✓` for scores ≤ 0.25, `⚠` for 0.5, `✗` for ≥ 0.75.

4. **Apply the gate.**
   - If aggregate ≤ threshold: pass. Exit cleanly.
   - If aggregate > threshold: print the report, say "Aggregate above threshold. Want to push harder, or exit anyway?", and wait. If the user says "exit", "enough", "ship it", or similar, exit with the report flagged. If the user says "push harder", return to grilling, focusing on the weakest dimensions.

5. **On exit from subroutine modes (spec/ticket):** write the resolved answers back to the artifact before returning control to the caller.
   - **Spec mode:** append the Ambiguity Report as a new section to the spec artifact. If the caller is `bugbook:flow`, use `bugbook page update "<page>" --section "Ambiguity Report" --create-section --content-file -`. If the caller is generic (e.g., `max:write-prd`), append to the markdown file the caller produced.
   - **Ticket mode:** append the resolved answers to the ticket body and optionally include the report.

6. **Freeform mode:** print the report to terminal only. No persistence.

---

## When to exit early (user override)

The user can override the gate at any time by saying "enough", "exit", "ship it", "good enough", or similar. When this happens, print the report anyway so the override is informed, then exit. Never hide the report on override — the point of the report is that the user sees exactly what's weak.

---

## Scoring discipline

- **Don't count questions or do arithmetic.** The rubric is qualitative. Judge each dimension at exit based on your assessment of the artifact's current state, not by tallying unresolved items during the interview.
- **Score the artifact, not the interview.** If the user answered a question but the answer is still vague, that dimension is still ambiguous.
- **Be honest about your own uncertainty.** If you're unsure whether a dimension is 0.25 or 0.5, pick the higher (more ambiguous) score. The gate is permissive (default 0.4 freeform) — it's OK to err toward calling things vague.
- **Don't penalize unknowable things.** If a dimension is ambiguous because the user genuinely doesn't know yet and needs to prototype, that's a legitimate Open Question, not a scoring failure. Score it as "Assumption: 0.25" with a note, not "Assumption: 1.0".
