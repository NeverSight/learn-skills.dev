---
name: ux-microcopy-audit
description: Audit interface copy — labels, buttons, errors, empty states, tooltips, notifications, form hints — against UX-writing standards. Produces a severity-rated issue list with concrete rewrites. Use when reviewing UI copy for clarity, tone, and consistency, or as a validation step on any generated screen.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Microcopy Audit Skill


## How this skill behaves (read first)

This is an **evaluative** skill — it reviews existing copy, auto-runs, and is built to be **called as a validation step** by generative skills (the `ux-microcopy` writer, plus `typography`, `dashboard`, `onboarding`, and component skills hand off here for their labels and messages).

It owns **copy quality**. Deliberate deferrals:

- **Manipulative copy** (confirmshaming, fake urgency, guilt) → the **dark-patterns audit** owns intent; flag and route.
- **Copy accessibility specifics** (alt text rules, screen-reader behavior) → the **accessibility audit**; this skill flags plain-language/clarity, defers the technical a11y mechanics.

**Scope discipline.** When invoked directly (the user named this audit), review **only this concern** — don't pull in sibling audits. It runs alongside other lenses only when an orchestrator (`ux-design-review`) or a generative skill calls it under `docs/orchestration-policy.md`, where it sits in **Tier A — always-relevant, auto-runs**. Explicit scope always wins.

---

## What this skill changes vs. default behavior

By default, copy review is impressionistic ("sounds fine") and partial — it misses the hidden copy (error states, empty states) and never checks consistency across a flow. This skill forces:

1. **A content inventory** — sweep *all* copy, including hidden states.
2. **Named criteria** — clarity, concision, action-orientation, consistency, tone fit, inclusivity — not vibes.
3. **A rewrite for each finding**, plus severity.
4. **A consistency pass across the whole flow**, which single-screen review can't do.

---

## The audit method (content inventory)

1. **Inventory the copy.** List every piece of text in the flow/product — and don't miss **hidden content**: error messages, empty states, tooltips, confirmations, notifications.
2. **Evaluate against the criteria below.** Capture screenshots/locations so fixes are easy to apply.
3. **Prioritize** — one step at a time; lead with what costs users most.
4. **Recommend rewrites**, not just flags.

---

## The criteria — what to check and what a violation looks like

### 1. Clarity & plain language
**Flag when:** jargon or high-register words; ambiguous phrasing; copy that needs re-reading.
- ❌ "Authentication credentials could not be validated."
- ✅ "That password doesn't match. Try again or reset it."

### 2. Concision
**Flag when:** filler words, multi-sentence labels, saying in 20 words what 6 would carry.

### 3. Action-orientation & specificity
**Flag when:** generic labels ("OK", "Yes", "Submit", "Start"); CTAs that don't say what happens or why.
- ❌ "Submit" → ✅ "Create account"

### 4. Consistency
**Flag when:** the same concept is named differently across the product ("scheduling" vs. "booking"), inconsistent button verbs, or platform-mismatched terms ("click" on mobile). One term per concept.

### 5. Tone fit
**Flag when:** the register is wrong for the moment — a joke on a payment error, cold/robotic copy on a welcome, hedging ("maybe") on a security action. Tone should match brand **and** moment.

### 6. Error & empty/success states
**Flag when:** errors state the problem but not the fix, blame the user, or use ALL-CAPS; empty states are blank instead of teaching the first action; success isn't acknowledged.

### 7. Inclusivity & clarity for all
**Flag when:** gendered pronouns where neutral works; non-descriptive links ("click here"/"More"); placeholder used as the only label. (Technical a11y → accessibility audit.)

### 8. Honesty
**Flag when:** confirmshaming, manufactured urgency, guilt, or confusing double-negatives. Note it and route to the **dark-patterns audit** for the intent classification.

---

## Severity rating

| Severity | Meaning |
|---|---|
| **Critical** | Copy blocks or misleads — an error with no path forward, a label that causes the wrong action, manipulative copy. |
| **Major** | Real friction — vague CTAs, jargon, inconsistent terms for the same concept, wrong tone in a sensitive moment. |
| **Minor** | Polish — wordiness, a slightly off but understandable phrase. |

---

## Audit output format

```
## Microcopy Audit — [Screen / Flow]
Context: [product voice · audience · the moment]

### Critical
- [Location] "current copy" → "rewrite" — why. (Criterion)
### Major
- …
### Minor
- …
### Working well ✓
- …

**Consistency notes:** terms used inconsistently across the flow.
**Top 3 rewrites:** highest-impact fixes.
```

End with the consistency notes and top rewrites — those are what a calling generator or writer acts on.

---

## How to run a good audit

1. **Inventory first**, including hidden states — that's where the worst copy hides.
2. **Check consistency across the whole flow**, not just each screen alone.
3. **Rewrite, don't just flag** — show the better version.
4. **Match tone to the moment**, not a single house style.
5. **Defer** manipulation intent to dark-patterns and technical a11y to accessibility.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| "The copy sounds fine" | Inventory all copy (incl. hidden states); name criteria; rate severity |
| Review one screen in isolation | Check terminology consistency across the whole flow |
| Flag without fixing | Provide the rewrite |
| Pass generic "OK/Submit" labels | Flag → verb + outcome |
| Miss error/empty states | Audit the hidden copy explicitly |
| Re-derive manipulation or a11y rules | Route to dark-patterns / accessibility |

---

## Source lessons (Uxcel)

- [Content Audits for UX Writing](https://uxcel.com/lessons/content-audits-840)
- [Ensuring Consistency in UX Copy](https://uxcel.com/lessons/consistency-561)
- [10 Microcopy Tips](https://uxcel.com/lessons/microcopy-tidbits-594)
- [Patterns in UX Writing](https://uxcel.com/lessons/patterns-313)
- [Writing Action-Based Messages](https://uxcel.com/lessons/action-based-messages-095)
- [Accessibility in UX Microcopy](https://uxcel.com/lessons/accessibility-in-microcopy-877)
