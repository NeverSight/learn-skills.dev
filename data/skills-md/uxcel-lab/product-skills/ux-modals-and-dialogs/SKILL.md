---
name: ux-modals-and-dialogs
description: Design or critique modals, dialogs, alerts, popovers, and bottom sheets — gate WHEN interrupting users is justified, then apply dismissal, title/button, and focus best practices. Trigger when the user asks to design or review a modal, dialog, popup, overlay, confirmation, alert, permission request, lightbox, or bottom sheet — or asks whether something should be a modal at all.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Modals & Dialogs Skill

## How this skill behaves (read first)

This is a **generative** skill. The default failure modes: **interrupting for everything** (modals for success messages, tips, newsletters — attention spent like it's free), **trapping users** (no visible close, no Esc, stacked modals), and **vague choices** ("Are you sure?" → Yes/No). A modal *takes the whole interface hostage* — that's justified only in high-stakes moments, and the price is paid back with crystal-clear purpose and effortless exit. This skill gates:

1. **Gate the interruption itself** — is a modal even justified here? The most important decision happens before any design.
2. **Apply the always-true core** — purpose in the title, explicit buttons, easy dismissal, focus management.
3. **Surface the type and timing decisions** (popup/fullscreen/popover/bottom sheet, permission priming) with trade-offs.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, `ux-microcopy-audit`, and `ux-dark-patterns-audit`** for validation.

---

## Step 0 — Gate the interruption (the decision that matters most)

A modal blocks everything. It earns that only for **high-stakes moments**:

- Confirming **destructive or irreversible actions** (delete account, discard draft) — show impact ("12 files will be deleted").
- **Critical errors or warnings** (system restart, unsaved changes at risk).
- **Information required to continue** the current task (login to save, payment details).

Everything else — success messages, tips, FYIs, promotions — uses **non-modal** patterns: inline messages, toasts, banners, popovers. Also establish:

- **Who triggers it?** User-initiated modals (clicked a button) are expected; **system-initiated** modals (timed popups, upgrade nags) interrupt without warning — avoid unless truly urgent (session expiry, critical update).
- **Timing** — never interrupt high-stakes flows in progress (mid-checkout is the classic crime).
- **Platform** — desktop alert vs. iOS alert / Android dialog conventions; bottom/action sheets for mobile action lists.

> If the content fails the high-stakes test, stop designing a modal and recommend the inline/toast alternative.

---

## The always-apply core (correct for every modal that survives the gate)

### Purpose, title, buttons

- **The title carries the whole message** — users skim or skip body text. "Discard draft?" not "Warning." Body text adds the *why* and context; nothing vital lives only in the body.
- **Explicit button labels answering the title:** ❌ "Yes" / "No" / "Cancel" ✅ "Discard draft" / "Keep editing." Users must know what each button does without reading anything else.
- **Maximum two action buttons.** A third ("Learn more") leaks users out of the decision.
- **Never blame or shame** in opt-out labels ("No thanks, I hate saving money" → dark-patterns flag).

### Dismissal is a right, not a feature

- **Multiple visible exits:** Close/Cancel button + the × in the corner + **Esc on desktop / Back on mobile**.
- **Click/tap outside closes it** — when no entered data would be lost; suppress only when dismissal would destroy work.
- **Never stack modals.** A modal on a modal is a hostage situation with extra steps.

### Focus and attention mechanics

- **Dark overlay** behind the modal — focuses attention, blocks outside interaction, doubles as a close target.
- **Keyboard focus moves into the modal on open** (onto the primary action); all controls keyboard-reachable.
- **Centered placement** — dead-center on mobile; horizontally centered and slightly above center on desktop (stable under window resizing).
- **Critical alerts look critical:** red accents and an alert icon for destructive/urgent confirmations, so habituated users don't dismiss on autopilot.

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Popup modal** | The standard high-stakes interrupt over dimmed content | Content that needs a whole page | Default modal type |
| **Fullscreen modal** | Complex focused tasks: multi-step forms, payments, T&Cs, mobile spotlight moments | Simple confirmations (overkill); anything users may need to escape fast — make dismissal obvious | Only when the task genuinely fills a screen |
| **Popover** | Extra detail/options anchored to an element, without blocking the page | Critical information (too easy to miss) | The non-modal default for contextual help |
| **Lightbox** | Image/video magnification with navigation, captions, zoom | Non-media content | Media-rich products only |
| **Bottom / action sheet (mobile)** | Lists of related actions or share targets, per OS convention | Critical confirmations (use an alert/dialog) | Android bottom sheet / iOS action sheet for action lists |
| **Success feedback** | Inline or on-page states | Success *modals* — interrupting to say "it worked" | Modal success only if users must acknowledge before continuing |
| **Permission requests** | In context, at the moment the feature needs it; **primed** with a pre-permission explainer; one permission at a time; a compelling reason (+81% grant likelihood) | At first launch, in batches, with "Recommended" pressure labels, or mid-task | Prime → contextual ask → graceful path to reverse a denial |
| **System-initiated modals** | Truly urgent: session expiry, security, data loss | Subscription nags, timed promos, rating begs | Almost never; use banners/badges instead |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics`, `microcopy`, and `dark-patterns` are Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — user control and freedom (exits), error prevention (explicit confirmations), match to expectations (platform conventions).
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — focus trap correctness, keyboard dismissal, screen-reader announcement, contrast of overlay content.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — modal visual hierarchy, overlay treatment, alert-styling restraint.
- **`ux-microcopy-audit`** *(Tier A)* — title clarity, button explicitness, body brevity, permission-reason wording.
- **`ux-dark-patterns-audit`** *(Tier A)* — this skill's interruptions are prime dark-pattern territory: nagging system modals, shame opt-outs, permission pressure, hard-to-find dismissal.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer; applies only on mobile)* — when the context is mobile: sheet conventions, dismissal gestures, fullscreen behavior.

If the audits surface a conflict (e.g., growth wants a signup modal on page load vs. user control), resolve back toward the primary task: the user was doing something — the modal must either protect that task or get out of its way.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Modal for a success message or a tip | Inline state / toast; modals for high-stakes only |
| Timed subscription popup mid-reading | User-initiated modals; system interrupts only for urgency |
| "Are you sure?" → Yes / No | "Discard draft?" → "Discard" / "Keep editing" |
| Three+ buttons including "Learn more" | Two actions, aligned to the title |
| No × , no Esc, no outside click | Close button + Esc/Back + outside click (when safe) |
| Modal opens on top of another modal | One modal at a time, ever |
| Vital info buried in body text | The title carries the message |
| Permission batch on first launch | Primed, contextual, one-at-a-time requests with reasons |
| "No thanks, I like missing out" | Neutral, respectful opt-out labels |
| Focus stays on the page behind | Focus moves into the modal, onto the primary action |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy + dark-patterns |

---

## Source lessons (Uxcel)

- [Types of UI Modals](https://uxcel.com/lessons/placeholder-955)
- [Best Practices for Designing UI Modals](https://uxcel.com/lessons/modals--dialogs-best-practices-166)
- [Designing Mobile Notifications & Dialogs](https://uxcel.com/lessons/mobile-notifications--dialogs-142)
- [How to Ask for User Permissions Unobtrusively](https://uxcel.com/lessons/ask-permission-best-practices-607)
