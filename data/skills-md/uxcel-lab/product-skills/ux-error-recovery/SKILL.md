---
name: ux-error-recovery
description: Design or critique how a product prevents, surfaces, and recovers from errors — input/validation errors, system & network failures, AI/prediction failures, destructive actions, and 404/dead-end pages. Leads with prevention (most errors are designable away), applies the always-true core (validate without interrupting, write recoverable messages, give a safety net, never dead-end) and gates context-dependent levers (confirm vs. undo, validation timing, humor, degradation, transparency vs. security) with trade-offs. Trigger when the user asks to design or review error states, error messages, form validation, a 404/error page, undo/confirmation flows, failure handling, or graceful degradation.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Error Recovery Skill

## How this skill behaves (read first)

This is a **generative** skill. Claude's default error handling is the failure mode: it writes "Something went wrong," validates only on submit, blames the user ("You entered an invalid value"), treats every error at the same severity, shouts in ALL CAPS or leaks codes ("Error 403: Forbidden"), offers no way back from a 404, and never thinks about *preventing* the error in the first place. Good error recovery inverts that. Its first move is to **prevent** errors (most are designable away with constraints, masks, and defaults), then make the unavoidable ones **recoverable** — tell the user what happened and what to do next, give them a safety net, and never leave a dead end. So this skill gates:

1. **Establish stakes, error source, and where in the journey the error happens** — these decide how much friction, confirmation, and escalation is warranted.
2. **Apply the always-true core** — prevent first, validate without interrupting, write recoverable messages, give a safety net, never dead-end.
3. **Surface the context-dependent decisions** (confirm vs. undo, validation timing, humor, AI degradation/confidence, transparency vs. security) with trade-offs.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, `ux-microcopy-audit`, `ux-dark-patterns-audit`, and (when mobile) `ux-mobile-responsiveness-audit`** for validation.

Scope & composition (per `docs/orchestration-policy.md` §9): this skill owns the **error/failure/recovery experience** — error states, message craft, validation behavior, undo/confirmation, degradation, and error pages — and composes lower-scope skills rather than re-deriving them. **Core children (built as part of the recovery experience):** **input-field anatomy** via `ux-inputs-and-forms`. **Peers that own a sub-part (defer):** **toast/notification type & frequency** to `ux-notifications-and-toasts` and **confirmation-modal mechanics** to `ux-modals-and-dialogs` (they own those sub-parts if reached). **Downstream (offer, don't auto-build):** **first-use / no-results / cleared empty screens** via `ux-empty-states`, the **password-reset flow** via `ux-login-signup`, **save-state confirmation** via `ux-settings`, and **help/contact at the point of error** via `ux-contact-support`. **Inherit, don't regenerate:** under an existing design system, take color/type/spacing from its tokens — only set those when designing from scratch.

---

## Step 0 — Establish context before designing

Ask if not known; state the assumption if proceeding without an answer:

- **What are the stakes if this goes wrong?** Error handling must match real-world consequences. A wrong balloon-color suggestion is minor disappointment; an unsafe-food recommendation, a wrong-account transfer, or a permanent delete is serious harm. Low-stakes can fail playfully; high-stakes demand detailed explanations, conservative defaults, undo, and a human-escalation path. When stakes are unclear, choose caution over convenience.
- **Is this a slip or a mistake?** *Slips* are autopilot lapses by users who know the system (clicking "Reply all" instead of "Reply") — fix with constraints, suggestions, good defaults, and undo. *Mistakes* come from a wrong mental model, usually in newer users (archiving instead of deleting because the icon is unclear) — fix with clearer labels, guidance, and closing the gap between the user's and the system's mental model (found through research). Don't assume users will "just learn" a confusing system; they leave.
- **Where in the journey does the error happen?** Three surfaces with different design: **input/validation** (a form field), **system/AI failure** (server, network, or a wrong prediction), and **navigation** (404, broken link). Each needs its own recovery move.
- **Platform.** Mobile tightens prevention — constrained keypads, input masks, OTP autofill, larger touch targets, and error text that stays visible above the keyboard.

---

## The always-apply core (correct for almost every error experience)

### 1. Prevent before you handle
- **Constrain the input.** Set boundaries so the wrong value can't be entered: a numeric keypad for phone/card fields, business-hours-only time pickers, grayed-out invalid options.
- **Use forgiving formats + input masks.** Let users type the way that's natural to them and format as they go (add the spaces/parens/hyphens, strip stray letters). Masks show *and* apply the format, cutting confusion for phone numbers, dates, card numbers.
- **Set reasonable defaults** that match what most users want — but never a default that benefits the business over the user (pre-checked subscriptions are a dark pattern, not a helpful default).
- **Ease memory burden.** Keep a visible running summary (multi-leg flights, multi-step bookings) and auto-detect SMS codes so users don't switch screens. Clear, skimmable labels and hints over walls of instruction.

### 2. Validate without interrupting
- **Validate after loss of focus, not on every keystroke and not only on submit.** Let users finish a field and shift focus before flagging it; a form that waits until the Submit click to reveal errors gets abandoned.
- **Real-time is the exception for requirement-based inputs** (new passwords) — show checkmarks as each rule is met so users aren't guessing.
- **Keep the error state visible until the input is *actually* valid** — not the moment the user starts retyping. The field returns to default/success only when the value truly passes, so users keep the context of what they're fixing.

### 3. Write messages that recover, not blame
- **Structure every message: what happened → why it matters → what to do next.** ("The code you entered doesn't match. Didn't get it? Resend code.") Lead with the *action*, not the problem ("Try better lighting or a different angle," not "Image recognition failed").
- **Plain, human language.** No jargon, no codes, no "unauthorized/restricted" robot-speak. Short — 1–2 sentences; people read even less when stressed.
- **Be precise, never generic.** "An error occurred" helps no one; name the field and the fix.
- **Be polite; never make users feel stupid.** No blame, no condescension.
- **No ALL CAPS** — it reads as shouting, slows reading 13–20%, and hurts accessibility for low-vision and dyslexic users.
- **Place the message next to the thing it's about** — beside the field, not in a banner they'll miss.

### 4. Give a safety net
- **Undo for reversible actions.** Make it immediate and obvious (the "Undo send" window). It removes the fear of permanent mistakes and lets people experiment.
- **Confirm only genuinely destructive / irreversible actions** — match the interruption to the regret. Overusing confirmations causes dialog fatigue and users stop reading them. Spatially displace the confirm button from the trigger so a double-tap can't auto-confirm.
- **Preserve work on failure.** When a system or AI step fails, don't make users start over — keep their input, highlight what needs checking, and carry context into a manual takeover.

### 5. Never dead-end
- **Every error offers a path forward** — retry, go home, search, or a relevant link. This is Nielsen's "help users recognize, diagnose, and recover from errors."
- **404s are a recovery surface, not a wall.** Explain plainly and apologetically why the page isn't there, stay on-brand, and give a clear exit: a search input and/or a short list of helpful links (spell-check the URL for close matches). Keep it uncluttered — concise copy + search is enough.
- **Offer help at the moment of error.** When the next step is "get help," link the right channel right there (defer the support experience itself to `ux-contact-support`).

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user decide. **Applying all of these by default is a mistake.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Confirm vs. undo** | Confirm irreversible, high-consequence actions (delete account, permanent data loss) | Confirming low-stakes/reversible actions (dialog fatigue); relying on undo alone for truly irreversible ones | Undo for reversible actions; confirm only high-consequence — and offer undo too where possible |
| **Validation timing** | Real-time for complex requirement inputs (passwords); on-blur for simple fields | Validating mid-typing on normal fields; validating only on submit | On-blur as the rule; real-time for password-style inputs |
| **Humor / personality in copy** | Friendly consumer brands, low-stakes errors, 404s | High-stakes (finance, health, security) or when the user came for support | Match brand; keep the functional path primary; skip the joke if unsure |
| **AI/model confidence display** | When it changes the user's decision and stakes are high (medical) | Meaningless precision (85.8% vs. 87%) that adds noise without changing behavior | Show only if actionable; prefer categorical (High/Med/Low) or N-best over raw percentages for laypeople |
| **Progressive degradation / fallback** | A feature or AI can partly fail — reduce capability step by step and offer manual takeover instead of a blackout | Sudden full manual handoff in unsafe moments; hiding that capability dropped | Degrade gracefully, preserve context, offer a manual path; always a human-escalation route when stakes are high |
| **Transparency vs. security in explanations** | Normal constraints users deserve to understand | Detail that teaches bad actors to exploit the system (spam filters, auth failures) | Guide the good-faith user's next action without revealing the vulnerability; "boring" failures for exploiters |
| **"Help us learn" feedback on errors** | Quick, binary, and you'll actually act on it (and tell users you did) | Interrupting recovery, or vanity collection that goes nowhere | Lightweight and post-resolution; framed as partnership, not "report a complaint"; optional |
| **404 richness (illustration/interactivity)** | Brand benefits and the page stays uncluttered | Forced jokes or clutter that raise cognitive load and bury the exit | Concise on-brand copy + search + top links; add visuals/interactivity only if genuinely on-brand |

High-stakes contexts (finance, health, security, destructive/irreversible actions) flip several defaults at once: more conservative defaults, mandatory confirmation *with* undo where possible, serious tone over humor, explicit human escalation, and security-aware (not fully transparent) explanations.

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics`, `microcopy`, and `dark-patterns` are Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — error prevention, "help users recognize, diagnose, and recover from errors," visibility of system status (the field stays in error until fixed; failures are surfaced), and user control & freedom (undo, escape from a 404).
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — errors signaled by more than color (icon/text, not red alone), error text programmatically associated with its field, focus moved to the message, no ALL CAPS, sufficient contrast on error/success states.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — an uncluttered 404/error page, error states that are noticeable without being alarming, no wall of text.
- **`ux-microcopy-audit`** *(Tier A)* — this skill lives on copy: the what-happened/why/what-next structure, action-first phrasing, plain human language, polite non-blaming tone, no jargon or codes.
- **`ux-dark-patterns-audit`** *(Tier A)* — the error-specific traps: confirmshaming on a cancel/delete confirmation, defaults set to benefit the business, a confirm button placed to catch an accidental double-tap, "Undo" hidden while the destructive path is one click, or feedback framed to guilt the user. Friction and confirmation should protect the user, never trap them.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer)* — constrained keypads, masks and OTP autofill, error text not hidden by the keyboard, touch-target size on retry/undo/confirm controls.

If the audits surface a conflict (e.g., the business wants a hard "are you sure?" wall on every action, or a guilt-tripping cancel confirmation), resolve back toward the primary task: **the user is already dealing with something going wrong — reduce friction, give them a clear way forward, and never use the error moment to manipulate them.**

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| "An error occurred" / "Error 403: Forbidden" | What happened → why it matters → what to do next, in plain language |
| Validate only when they hit Submit | Validate on loss of focus (real-time for passwords) |
| Clear the error state the moment they retype | Keep it visible until the value is actually valid |
| Blame the user; ALL CAPS | Polite, action-first, sentence case, beside the field |
| Treat every error at one severity | Match friction to stakes — undo for reversible, confirm only high-consequence |
| Confirm everything | Reserve confirmation for irreversible actions to avoid dialog fatigue |
| Lose the user's work when a step fails | Preserve input, highlight what needs checking, carry context into manual takeover |
| A bare 404 that sends users back where they came | Explain + search + helpful links, on-brand, uncluttered |
| Pre-checked/manipulative "defaults"; guilt-trip cancel dialogs | Helpful, user-benefiting defaults; respectful confirmations |
| Skip prevention and only handle errors after they happen | Constrain, mask, and default so the error can't occur |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy + dark-patterns (+ mobile-responsiveness) |

---

## Source lessons (Uxcel)

- [Showing Input Error](https://uxcel.com/lessons/showing-input-error-162)
- [Writing Problem Messages](https://uxcel.com/lessons/problem-messages-893)
- [The Nature of User Errors](https://uxcel.com/lessons/the-nature-of-user-errors-902)
- [Graceful Failure Design](https://uxcel.com/lessons/graceful-failure-design-394)
- [11 Best Practices for Designing 404 Pages](https://uxcel.com/lessons/best-practices-for--pages-112)
- [Safety Nets & Undo](https://uxcel.com/lessons/safety-nets-undo-430)
- [Common Patterns](https://uxcel.com/lessons/common-patterns-814)
