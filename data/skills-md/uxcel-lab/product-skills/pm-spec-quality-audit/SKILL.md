---
name: pm-spec-quality-audit
description: Run a structured quality audit on a product spec, PRD, or requirements document. Produces a severity-rated issue list with concrete fixes — catches untestable requirements, happy-path-only flows, missing scope exclusions, absent dependencies/constraints/assumptions, implementation details leaking into functional specs, and unvalidated assumptions presented as facts. Use when reviewing a spec, PRD, or requirements doc, or as the validation step after writing one.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Spec Quality Audit Skill

## What this skill changes vs. default behavior

By default, Claude reviews a spec by praising its structure and suggesting wording polish — it rarely tests whether a requirement is *buildable as written*, whether different teams would interpret it differently, whether the document quietly skipped what's **out** of scope, or whether "validated" claims have any evidence behind them. This audit forces four things: every finding names the violated principle; every requirement is tested with "could QA write a pass/fail check from this without asking what you meant?"; the document is checked for what's *missing* (scope exclusions, DCA, corner cases), not just what's present; and findings come severity-rated by build damage with concrete rewrites.

This is an **evaluative** skill: it auto-runs whenever a spec, PRD, or requirements document is being reviewed — and as the validation step after `pm-product-spec` generates one.

**Scope discipline.** When invoked directly (the user named this audit), review **only this concern** — don't pull in sibling audits. It runs alongside other lenses only when the `pm-product-review` orchestrator or a generative skill calls it under `docs/orchestration-policy.md`, where it sits in **an artifact-specific lens — offered (for specs/PRDs)**. Explicit scope always wins.

---

## The framework — what to check and what a violation looks like

### 1. Problem anchoring & traceability

A spec opens with the problem or opportunity and why it matters now — even when everyone "already knows." Every requirement traces back to a user or business outcome; a spec that consistently links requirements to intent keeps long projects from drifting into disconnected implementation.

**Flag when:** the document opens with the solution; requirements exist that serve no stated problem or goal; the "why" lives only in the author's head.

- ❌ Spec begins: "Build a referral widget on the dashboard with three invite slots."
- ✅ Spec begins: "Acquisition cost rose 40% this year; referred users retain 2× better. Goal: a referral mechanism that produces ≥15% of new signups."

### 2. Right layer — requirement vs. functional vs. technical

The 3-layer hierarchy: business/user requirement (*what users experience* — PRD), functional spec (*how the product behaves*, even with no UI), technical spec (*how the code achieves it* — engineering's territory). Mixing layers causes the two classic failures: vague specs that are really requirements, and PM overreach into architecture.

**Flag when:** a functional spec prescribes frameworks, data models, or architecture; a "spec" contains only outcome wishes with no behavior; PRD goals and implementation details are interleaved in the same section.

- ❌ "The price calculator must be implemented as a Node microservice with Redis caching." (in a PM's functional spec)
- ✅ "The price calculation must accept a base price, discount rules, and an optional promo code, and return a validated final price — even when no UI exists for the calculation."

### 3. Testability of every requirement

A requirement is done when QA — or anyone — could write a pass/fail check from it without asking the author. Subjective adjectives are the signature violation. Testability applies across types: functional (action → response), usability (task completion), performance (load, error rate), accessibility (contrast, keyboard, screen reader).

**Flag when:** "fast," "intuitive," "user-friendly," "seamless" appear without a defined measure; success criteria have no number, unit, or condition; there's no way to tell whether a requirement is satisfied.

- ❌ "The page should load quickly."
- ✅ "The page loads in under three seconds on a standard mobile network."

### 4. Complete flows, not happy paths

Requirements must describe full workflows — including corner cases, errors, and returning/partial states — not just outcomes. "Users can create an account" hides every implementation decision that matters.

**Flag when:** only the success path is specified; no behavior defined for errors, interruptions, or returning users; a multi-step flow is written as a single outcome sentence.

- ❌ "Users can create a document."
- ✅ "After clicking 'Create document,' a draft is created; users can edit it, but it is saved only after a name and folder are defined. If the user leaves mid-flow, the draft persists for 30 days."

### 5. Scope honesty — exclusions stated

Scope must say what is **out**, not just what's in. Unstated exclusions are where misalignment and scope creep hide. Use cases should note where functionality is *excluded*, not just included.

**Flag when:** no exclusions are listed anywhere; "scope" is a feature list with no boundaries; stakeholder expectations the spec silently doesn't cover.

- ❌ Scope: "Redesigned checkout flow." (Is guest checkout in? Refunds? Mobile app parity?)
- ✅ "In: web checkout, guest checkout. Out (this release): mobile app checkout, refund flow changes, loyalty-point redemption."

### 6. Dependencies, constraints & assumptions (DCA)

The section most often missing — and where delivery actually breaks. Dependencies need owners and internal/external classification; constraints need a named flex side (time, cost, or scope — all three fixed is a failure plan); assumptions must be phrased as testable statements with validation status and a mitigation action, not vague beliefs.

**Flag when:** no DCA section exists; dependencies have no owner ("legal needs to approve" — who, by when?); all of time, cost, and scope are treated as fixed; assumptions read as facts ("users will find onboarding intuitive").

- ❌ Assumption: "Users will prefer the new flow."
- ✅ Assumption: "80% of new users complete onboarding within two minutes — validating via usability test by March 15 (owner: UX). If disproven: revert to two-step entry."

### 7. Validation evidence — review ≠ validation

Review checks internal quality (clear, consistent, feasible — done with eng/UX/business); validation checks the solution works for real users (prototype tests, user sessions — done *before* the spec is finalized, so insights inform it). A spec that claims validation needs an evidence trail: findings linked to the requirements they changed.

**Flag when:** "validated with users" appears with no method, participant count, or linked findings; user validation is scheduled *after* development as a checkbox; disconfirmed assumptions didn't change the spec; no review with dependency owners before the spec was finalized.

- ❌ "The flow has been validated." (by whom? against what?)
- ✅ "5-participant prototype test (Mar 3): 3 of 5 missed 'Continue as guest' → requirement 4.2 updated to make guest checkout a primary action."

### 8. Audience fit & whole-picture framing

A spec scoped only to one team's slice produces features that work in isolation and fail when integrated — always present the full picture first, then per-team detail. Format must match the reader: annotated design files for frontend, workflow/data-flow diagrams for backend, high-level outcomes for business stakeholders; internal docs can carry proprietary detail, external ones only safe commitments.

**Flag when:** the spec covers one team's work with no system context; backend behavior specified only via UI mockups; business stakeholders handed API-level detail (or engineers handed only vision prose); one document straining to serve internal and external audiences at once.

- ❌ A checkout spec that documents the new payment UI but never mentions the order-service and email-receipt changes it depends on.
- ✅ Full-flow overview first; then per-team sections — annotated Figma for frontend, a data-flow diagram for the payments backend.

> **Tension note:** completeness vs. focus — a spec bloated with implementation noise is as broken as a thin one; flag *missing decisions*, not missing padding. Removing detail that belongs in design/tech docs is an improvement, not a gap. And stability vs. adaptability — PRDs should stay flexible while specs stabilize once development starts; don't flag a PRD for being less precise than a spec.

---

## Severity rating

Rate each finding by **build damage** — what the document, left as-is, would cause teams to build:

| Severity | Meaning |
|---|---|
| **Critical** | Teams would build the wrong thing or different things (untestable core requirements, undefined major flows, unstated scope boundaries on contested areas, solution with no problem) |
| **Major** | Delivery will break or drift (missing DCA, no owners on external dependencies, happy-path-only flows, unvalidated assumptions driving major decisions, one-team tunnel vision) |
| **Minor** | Hygiene that degrades trust in the doc (inconsistent terminology, missing acceptance criteria on secondary requirements, stale sections) |
| **Cosmetic** | Phrasing polish; don't pad the report with these |

Overlaps: whether the *success metrics* themselves are valid (vanity, gameable, unfalsifiable) belongs to `pm-okr-metric-validity-audit` — this audit checks the metrics are *present and specific*, that one checks they're *worth hitting*. Ranking discipline of what made it into scope belongs to `pm-prioritization-rigor-audit`. Deeper assumption-testing method — was the riskiest assumption tested, with the right-fidelity method and honest evidence — belongs to `pm-assumption-rigor-audit`.

---

## Output format

```
## Spec Quality Audit — [Document]
Context: [doc type (PRD/functional/technical) · audience · development stage, if known]

### Critical
- [Issue] — what's wrong → concrete rewrite or addition. (Principle)
### Major
- …
### Minor
- …
### Working well ✓
- …

**Top 3 priorities:** the highest build-damage fixes, with suggested rewrites.
```

Always end with the prioritized top issues — a flat list helps no one act.

---

## How to run a good audit

1. **Establish context first** — which document is this (PRD vs. functional vs. technical spec)? Audit it against its own layer's job, not another's. Where is it in the lifecycle (draft for review vs. approved and in development — post-approval changes cost more)?
2. **Check for absences, not just flaws** — the worst spec defects are missing sections (scope exclusions, DCA, error flows), which a read-through of what's present won't surface. Walk the checklist.
3. **Only flag real costs** — a lean spec for a small reversible feature doesn't need a compliance section. Scale rigor to risk and project size.
4. **Prioritize, don't enumerate** — three build-damaging findings beat fifteen nitpicks.
5. **Be specific in fixes** — rewrite the requirement, name the missing owner, draft the exclusion line. Never just "make it more testable."

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Praise structure and polish wording | Test each requirement: could QA write a pass/fail check from it? |
| Review only what's written | Walk the checklist for what's *missing* — exclusions, DCA, error flows |
| Accept "validated with users" at face value | Ask for method, participants, and which requirements the findings changed |
| Treat review and validation as the same step | Review = internal quality; validation = real-user evidence, gathered before specs finalize |
| Let "fast/seamless/intuitive" pass as requirements | Rewrite with a number, unit, and condition |
| Flag a PRD for lacking spec precision | Audit each document against its own layer's job |
| Demand more detail everywhere | Flag missing *decisions*; cut implementation noise that belongs in tech/design docs |
| Re-audit the success metrics' validity | Defer to `pm-okr-metric-validity-audit`; check presence and specificity here |
| Deliver an unranked issue dump | Severity by build damage + top-3 priorities with rewrites |

---

## Source lessons (Uxcel)

- [Reviewing and Validating Specifications](https://uxcel.com/lessons/reviewing-and-validating-specifications-295)
- [Understanding Product Specifications](https://uxcel.com/lessons/understanding-product-specifications-734)
- [Types of Product Specifications](https://uxcel.com/lessons/types-of-product-specifications-646)
- [Product Specs vs. Product Requirements Documents](https://uxcel.com/lessons/product-specs-vs-product-requirements-documents-679)
- [Dependencies, Constraints, and Assumptions](https://uxcel.com/lessons/dependencies-constraints-and-assumptions-327)
