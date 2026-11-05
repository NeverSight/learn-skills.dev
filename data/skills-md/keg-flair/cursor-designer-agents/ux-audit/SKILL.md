---
name: ux-audit
description: Audits screens or flows for UX friction and trust issues. Produces prioritized findings (P0–P2), concrete fixes, quick wins, assumptions, and a validation plan. Use when the user asks for a heuristic review, friction audit, flow critique, or “what’s wrong with this UX?”.
---

# UX Audit

See shared conventions in `docs/HOUSE_STYLE.md` (severity, fallbacks, evidence labels).

## Defaults

- **Prioritized**: findings tagged P0/P1/P2 with clear impact.
- **Mechanism-first**: explain why the issue causes friction (not just “looks bad”).
- **Concrete fixes**: propose specific UI/content/behavior changes.
- **Honest uncertainty**: separate what’s observed (from assets) vs inferred; mark assumptions.

## Constraints

- **Do not invent** user research, analytics, business rules, or platform constraints.
- **Ask at most 3 clarifying questions** (only if answers materially change priorities or fixes).
- If inputs are vague, proceed with a **useful triage checklist + minimum input request** rather than stalling.

## Clarifying questions (ask max 3)

1. What’s the **primary user goal** for this screen/flow, and what is “success”?
2. What’s the **platform** (web/iOS/Android) and target audience (new vs power users)?
3. Are there hard constraints (compliance/trust, localization, auth/payments, accessibility)?

## Inputs to request (only if missing)

- Screenshots or a short screen recording (best) and what step(s) they represent
- Primary user goal + success definition (metric or qualitative)
- Any known constraints (a11y, legal/compliance, payments/auth, performance)

## Fallback behavior (when evidence is weak)

If screenshots/recordings are not provided, still produce:
- **3–5 likely failure mechanisms** (explicitly low confidence)
- A **triage checklist** (what to look for on the real screens)
- A short **“highest-value next inputs”** list (max 5 bullets)

## Output template

```markdown
#### Summary
- **Primary user goal**:
- **What’s being audited**:
- **Success definition**:

#### Key findings (prioritized)

##### P0 (must fix)
- **Issue**:
  - **Where**:
  - **Why it matters**:
  - **Proposed fix**:
  - **Risk / trade-off**:
  - **How to verify**:

##### P1 (should fix)
- …

##### P2 (nice to have)
- …

#### Quick wins
- …

#### Open questions / assumptions
- …

#### Test plan / validation
- **Usability**:
- **Success signals**:
- **Edge cases**:
```

