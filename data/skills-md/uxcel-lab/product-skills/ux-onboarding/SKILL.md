---
name: ux-onboarding
description: Design or critique a user-onboarding flow — the first-run experience that gets users to value fast. Gates context-dependent choices (onboarding method, progressive profiling, product tours) and applies the always-true core. Trigger when designing welcome screens, first-run experiences, product tours, activation flows, or when onboarding drop-off needs improving.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Onboarding Flow Skill


## How this skill behaves (read first)

This is a **generative** skill, and onboarding is a prime **over-design** trap: the default instinct is a multi-screen tour nobody reads plus a wall of upfront questions and "enable all permissions" prompts — which actively *blocks* the product and drives drop-off. The lessons are blunt: **most apps don't need a tutorial; users learn by using.** So this skill gates hard:

1. **First gate: does this even need onboarding?** Often the answer is "barely" — and the best onboarding is the lightest one that gets users to value.
2. **Apply the always-true core** — the principles that hold for any first-run experience.
3. **Choose the method and asks deliberately** — surface the context-dependent decisions with trade-offs; don't default to a 6-screen carousel.

Then **hand off to the audits** — especially `dark-patterns` (onboarding is where forced permissions/notifications and friend-spam concentrate).

---

## Step 0 — Establish context, starting with the gate

**Gate — does it need onboarding?** Per the lessons, onboarding is warranted mainly when:

- the **app is complex** (explain features as users reach them, not upfront), or
- you **genuinely need data** to function (e.g. a banking app), or
- workflows are **unique/unfamiliar**, or
- a tutorial is **expected** (e.g. mobile gaming).

If none hold, recommend the lightest touch — empty-state nudges and contextual tips — over a tour. Then capture:

- **Product complexity** — learn-by-doing vs. genuinely needs explanation.
- **What's truly required to start** — the minimum data/permissions, if any.
- **Audience** — novice vs. expert; one persona or several (drives persona-based branching).
- **Platform** — mobile (system permission prompts, tight space) vs. web.

State assumptions if proceeding without answers.

---

## The always-apply core (true for any onboarding)

- **Front-load value; deliver an early win.** Show the benefit before asking for anything. Duolingo ends onboarding with two real sentences. Early success drives retention.
- **Keep it short.** ~4–5 screens max; most users expect onboarding to take **≤60 seconds**. If it feels like a lecture, users skip it.
- **Ask for the minimum, and say why.** Don't bombard with questions before trust is built. Every field/permission needs a clear "why now"; if you can't justify it at launch, collect it later, contextually.
- **One thing at a time.** One contextual tip at a time; introduce features at the pace users meet them. Less is more.
- **Apply progressive disclosure.** Primary/most-common features first; reveal advanced options on request. Keep to ≤2 levels of depth.
- **Always skippable, with visible progress.** Tell users how many steps and where they are; let them exit. Never trap them in the tour.
- **Use empty states and success states.** A blank screen is an onboarding opportunity (educational content + a clear CTA); a success state early creates a positive first connection.
- **End with a clear, relevant CTA** — the next logical action ("Start shopping", "Create your first project").
- **Don't re-show completed onboarding.** Track state; repeating tips after completion is friction.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0. **Defaulting to "full walkthrough + ask everything" is the failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Onboard at all (and how heavy)** | App is complex, data-required, unfamiliar, or tutorial-expected | Simple learn-by-doing apps | Lightest touch that reaches value; prefer empty-state + contextual tips over a tour |
| **Method** (walkthrough / interactive tour / contextual tips / checklist / empty-state-led / permission priming) | Match to need: interactive tour for hands-on learning, checklist for multi-step setup, contextual tips for discoverable features | A static swipe-through carousel at first launch (usually skipped) | Interactive/contextual over static; see method notes below |
| **Customization / persona questions** | Answers genuinely change the experience (e.g. proficiency level, freelancer vs. enterprise) | Asking for data you won't use, or visual customization at first launch | Ask only if it reshapes onboarding; explain why; else defer |
| **Permission / notification timing** | Contextually, at the moment of value, with **permission priming** (explain benefit before the system prompt) | Requesting all permissions / "enable all notifications" upfront | Contextual + primed — **never force-all** (→ dark-patterns) |
| **Registration timing** | Account genuinely needed before value | Forcing signup before users see anything | Gradual engagement — let users preview/try first (delaying registration can lift signups ~29%) |
| **Feature / instructional onboarding** | Unique or newly-released features; genuinely unfamiliar workflows | At first launch for a self-evident app | Promote new features contextually, not in a launch tutorial |

### Method notes (the picker's menu)
- **Interactive tour** — hands-on, triggered in context (learn by doing).
- **Contextual tips** — minimal cues, one at a time, at point of need.
- **Checklist** — guided setup with progress; good sense of accomplishment for multi-step products.
- **Empty-state-led** — the screen itself teaches the first action; lightest touch.
- **Permission priming** — a value-explaining screen *before* the system permission dialog.
- **Walkthrough (static screens)** — only if necessary; ≤4–5 screens, focus on the few most exciting/essential things.

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`dark-patterns`, `heuristics`, and `microcopy` are Tier A (auto-run); `accessibility` and `aesthetics` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-dark-patterns-audit`** *(Tier A)* — the onboarding-specific traps: forced/upfront permissions, "enable all notifications", friend-spam contact access, confirmshaming a skip option. Onboarding should respect autonomy (mindful onboarding).
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — do the tips/overlays/tour screens create clutter or bury the primary action?
- **`ux-heuristics-audit`** *(Tier A)* — user control (skippable), visibility (progress, success states), recognition, help & documentation.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — tooltips/overlays reachable by keyboard and screen readers; the flow is skippable without a mouse.
- **`ux-microcopy-audit`** *(Tier A)* — onboarding copy (tips, CTAs, empty/success states) is clear, action-based, and on-voice.

If an audit flags overload or a forced action, resolve toward the gate: the lightest flow that still reaches value.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Add a tutorial because every app has one | Gate first — many apps just need empty-state + contextual tips |
| 6+ static walkthrough screens at first launch | ≤4–5 screens, or skip the carousel for in-context guidance |
| Ask every question / request all permissions upfront | Minimum asks; permission priming at the moment of value |
| Force signup before showing anything | Gradual engagement — preview/try first |
| Explain features before delivering value | Front-load an early win |
| Block users in the tour | Always skippable, with visible progress |
| Leave empty/success states blank | Use them to teach the first action and reward early success |
| Keep showing tips after completion | Track state; don't repeat |
| "Enable all notifications" to maximize re-engagement | Contextual, justified opt-ins (→ dark-patterns audit) |
| Ship without checking | Hand off to dark-patterns + aesthetics + heuristics + accessibility |

---

## Source lessons (Uxcel)

- [Best Practices for User Onboarding Flow Design](https://uxcel.com/lessons/onboarding-best-practices-341)
- [Best Practices for Onboarding UX](https://uxcel.com/lessons/best-practices-for-onboarding-ux-655)
- [Basics of Mobile Onboarding](https://uxcel.com/lessons/onboarding-734)
- [Progressive Disclosure in UX](https://uxcel.com/lessons/progressive-disclosure-597)
- [Attention & Well-being](https://uxcel.com/lessons/attention-well-being-732)
