---
name: ux-heuristics-audit
description: Run a structured usability audit of any UI against Nielsen's 10 heuristics. Produces a severity-rated, prioritized issue list — each finding tagged with the violated heuristic and a concrete fix. Use when auditing a screen, flow, or component for usability problems, or as a validation step after generating UI.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Usability Heuristics Audit Skill


## What this skill changes vs. default behavior

Without this skill, a usability review tends to produce a flat list of generic suggestions ("make it cleaner", "improve the CTA") with no framework, no severity, and no link to *why* something is a problem. This skill forces four things:

1. **Every finding names the heuristic it violates** — not a vague opinion.
2. **Every finding gets a severity rating** based on frequency × impact × persistence — so the list is prioritized, not equal-weighted.
3. **Every finding has a concrete, specific fix** — not "consider improving."
4. **The audit resists over-flagging.** Heuristics are principles, not a checklist to max out. A finding only earns a place if it plausibly costs a real user time, confidence, or task completion.

**Scope discipline.** When invoked directly (the user named this audit), review **only this concern** — don't pull in sibling audits. It runs alongside other lenses only when an orchestrator (`ux-design-review`) or a generative skill calls it under `docs/orchestration-policy.md`, where it sits in **Tier A — always-relevant, auto-runs**. Explicit scope always wins.

---

## The 10 heuristics — what to check and what a violation looks like

Work through each. For every issue, capture: **violated heuristic**, **severity**, **what's wrong**, **fix**.

### 1. Visibility of system status
The system should always keep users informed about what's happening through timely feedback. A good interface answers: *What just happened? Where am I? What's happening now? What's next?*

**Flag when:** an action produces no feedback (button click with no state change, form submits with no confirmation); loading/processing has no indicator; the user's current location in a flow is unclear; background operations (saving, syncing, uploading) are silent.

- ❌ User taps "Save" and nothing visibly changes — did it work?
- ✅ "Save" shows a spinner, then a checkmark + "Saved" with a timestamp.

### 2. Match between the system and the real world
Speak the user's language — familiar words, phrases, concepts — not system or developer jargon. Follow real-world conventions and expected ordering.

**Flag when:** copy uses internal/technical terms ("authentication failed: token expired"), unfamiliar icons, or metaphors that don't map to user expectations; information appears in an unnatural order.

- ❌ "Error 0x80: invalid credential object."
- ✅ "That password doesn't match. Try again or reset it."

### 3. User control and freedom
Users make mistakes and change their minds. Provide clearly marked "emergency exits" — undo, redo, back, cancel, close — without forcing them through extended dialogue.

**Flag when:** destructive actions have no undo; there's no obvious way to exit a state, modal, or flow; multi-step processes trap the user with no back option; exits are hidden or ambiguously labeled.

- ❌ Deleting an item is instant and permanent with no recovery.
- ✅ Delete shows "Undo" for several seconds; or deleted items recover for 30 days.

### 4. Consistency and standards
The same words, actions, and elements should mean the same thing throughout (internal consistency) and follow platform conventions (external consistency). Covers visual, functional, placement, and data-format consistency.

**Flag when:** the same action is labeled differently in different places; primary buttons move position between screens; similar components behave differently; date/phone/number formats differ across forms; platform conventions are broken (e.g. non-standard back behavior).

- ❌ "Delete", "Remove", and "Trash" all used for the same action across screens.
- ✅ One verb for one action, in a consistent position and style everywhere.

### 5. Error prevention
Preventing mistakes beats good error messages. Use smart defaults, input constraints, forgiving formatting, suggestions, and confirmations for high-cost actions. Distinguish **slips** (accidental) from **mistakes** (wrong mental model).

**Flag when:** forms allow easily-preventable invalid input; no inline validation before submit; no confirmation on destructive/irreversible actions; rigid input formats reject valid data ("remove the spaces from your card number").

- ❌ Form only reveals 5 errors after the user hits Submit.
- ✅ Inline validation flags each field as the user leaves it; card field accepts any spacing.

### 6. Recognition rather than recall
Minimize memory load — make options, actions, and information visible rather than forcing users to remember them across contexts.

**Flag when:** users must remember info from a previous screen to act on the current one; no autocomplete/suggestions/recent items where they'd help; data the user already entered isn't pre-filled; features are invisible until you know they exist.

- ❌ Billing form makes the user re-type the shipping address they just entered.
- ✅ "Same as shipping address" is pre-selected; recent searches and viewed items resurface.

### 7. Flexibility and efficiency of use
Serve both novices and experts. Show common functions by default; provide accelerators (shortcuts, gestures, macros, customization) for experienced users.

**Flag when:** only one rigid path to complete a task; no shortcuts/accelerators for frequent or power users; no way to customize or save preferences for repeated workflows. *Context note: weight this heavily for productivity/pro tools, lightly for simple consumer or single-use flows.*

- ❌ Power users must click through the same 6-step menu path every time.
- ✅ A keyboard shortcut and a saved/favorite action exist alongside the menu path.

### 8. Aesthetic and minimalist design
Interfaces should contain only what supports the user's task. Every element that doesn't add value competes with the elements that do. Minimalist = functional, not bare.

**Flag when:** screens are cluttered with low-value elements; decorative content crowds out task-critical content; everything is emphasized (so nothing is); too many options shown at once instead of progressive disclosure.

- ❌ A pricing card with 6 badges, 3 shadows, and 30 feature rows competing for attention.
- ✅ One emphasized element, top features only, the rest behind "See all."

> **Heuristic tension:** #8 (minimalism) and #9/#10 (more help, more docs) and #7 (more options) pull against each other. Don't recommend adding help text, options, and content *and* flag clutter in the same breath. Resolve toward the user's primary task.

### 9. Help users recognize, diagnose, and recover from errors
Error messages should be in plain language, state what went wrong, and offer a constructive way forward — politely.

**Flag when:** error messages show codes or jargon; messages state the problem but not the solution; tone is blaming or robotic; messages use ALL CAPS (harder to read, feels like shouting, hurts accessibility); errors aren't placed next to the field that caused them.

- ❌ "INVALID INPUT."
- ✅ "This email is already registered. Log in instead, or use a different address." (next to the field)

### 10. Help and documentation
Ideally the design needs no explanation — but provide help that's easy to find when users get stuck. Distinguish **proactive** help (onboarding, contextual tips) from **reactive** help (searchable docs, tutorials).

**Flag when:** complex features have no contextual guidance; help is buried or unsearchable; onboarding can't be skipped or dismissed; tips aren't relevant to the current task.

- ❌ A complex feature with no tooltip, no onboarding, no findable docs.
- ✅ A dismissible contextual tip on first use + searchable, task-categorized help.

---

## Severity rating

Rate each finding the way a heuristic evaluation does — by combining three factors (per Nielsen):

- **Frequency** — how often will users hit it? (rare ↔ constant)
- **Impact** — how hard is it to overcome when hit? (annoyance ↔ blocker)
- **Persistence** — once-only (users learn around it) or repeated every time?

Collapse those into one of four levels:

| Severity | Meaning |
|---|---|
| **Critical** | Blocks task completion or causes data loss / irreversible error. Fix before ship. |
| **Major** | Frequent + high-friction; users can recover but waste time or lose confidence. |
| **Minor** | Noticeable friction, low frequency or easy to overcome. |
| **Cosmetic** | Polish; fix if time allows. Don't pad the report with these. |

If an issue is both an accessibility violation (contrast, keyboard, screen-reader, alt text) **and** a usability issue, note it but **defer the accessibility specifics to the accessibility-audit skill** rather than duplicating — call that skill if a full a11y pass is warranted.

---

## Audit output format

```
## Usability Heuristic Audit — [Screen / Flow Name]
Context: [platform · audience · primary user task, if known]

### Critical
- [Issue] — what's wrong → fix. (Heuristic #N: name)

### Major
- [Issue] — what's wrong → fix. (Heuristic #N: name)

### Minor
- [Issue] — what's wrong → fix. (Heuristic #N: name)

### Working well ✓
- [What already satisfies the heuristics — name them]

**Top 3 priorities:** the three fixes with the highest frequency × impact.
```

Always end with the prioritized top 3 — a long flat list helps no one act.

---

## How to run a good audit (not a checklist dump)

1. **Establish context first.** Platform (mobile/web/desktop), audience (novice/expert), and the primary task change which heuristics matter and how hard to weight them. If unknown and it materially affects findings, ask one question before flagging.
2. **Only flag real costs.** A finding must plausibly cost a real user time, confidence, or completion. "It could be slightly cleaner" is not a finding.
3. **Respect heuristic tension.** Minimalism vs. more help/options/feedback conflict by design. Don't recommend both at once — resolve toward the primary task.
4. **Prioritize, don't enumerate.** 3 critical findings beat 25 cosmetic ones. The severity rating and top-3 exist to force this.
5. **Be specific in fixes.** "Add feedback" → "show a spinner on the Save button, then a 'Saved' confirmation."

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| "Improve the usability of this screen" | Name the heuristic, severity, and exact fix per issue |
| Treat every issue as equally important | Rate Critical/Major/Minor/Cosmetic; surface top 3 |
| Flag clutter AND recommend more help text/options | Resolve the minimalism-vs-help tension toward the main task |
| Re-derive accessibility findings here | Note overlap; defer specifics to the accessibility-audit skill |
| Audit without knowing the platform/audience | Establish context; weight heuristics accordingly |
| Pad the report with cosmetic nitpicks | Report only issues that cost a real user time or confidence |
| "Error 0x80 / INVALID INPUT" left unflagged | Flag jargon, codes, ALL CAPS, blaming tone (Heuristic #9) |
| Permanent destructive action with no exit | Flag missing undo/cancel/back (Heuristic #3) |

---

## Source lessons (Uxcel)

- [10 Usability Heuristics by Jakob Nielsen](https://uxcel.com/lessons/usability-heuristics-270)
- [Usability Heuristics](https://uxcel.com/lessons/usability-heuristics-553)
- [Mental Models & User Control](https://uxcel.com/lessons/mental-models-user-control-375)
- [Writing Problem Messages](https://uxcel.com/lessons/problem-messages-893)
- [Minimizing Cognitive Load](https://uxcel.com/lessons/minimizing-cognitive-load-834)
- [Understanding Design Audit Types](https://uxcel.com/lessons/understanding-design-audit-types-317)
