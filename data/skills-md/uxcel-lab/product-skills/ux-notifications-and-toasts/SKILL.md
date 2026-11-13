---
name: ux-notifications-and-toasts
description: Design or critique notifications — pick the right type (badge, banner, snackbar, toast, alert, push) for the message's urgency, and respect user attention with timing, frequency, and opt-out controls. Trigger when the user asks to design or review notifications, toasts, snackbars, badges, banners, alerts, push notifications, or a notification strategy.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Notifications & Toasts Skill

## How this skill behaves (read first)

This is a **generative** skill. The default failure modes: **urgency inflation** (everything is an alert; success messages interrupt), **frequency abuse** (repeat pings for the same event until users kill all notifications), and **attention disrespect** (badges for non-notifications, pings with no user value). A notification spends the user's attention — the type must match the message's *actual* urgency, and the system must stay worth listening to. This skill gates:

1. **Establish urgency, audience moment, and channel** — these pick the type.
2. **Apply the always-true core** — type-urgency match, frequency discipline, content brevity, user control.
3. **Surface the engagement levers** (push strategy, personalization, rich media) with trade-offs — this is dark-patterns-adjacent territory.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, `ux-microcopy-audit`, and `ux-dark-patterns-audit`** for validation.

---

## Step 0 — Establish context before designing

Ask if not known; state the assumption if proceeding without an answer:

- **How urgent is the message, really?** Needs action *now* (failed payment) → persistent alert. Useful soon (storage near limit) → warning. FYI (saved, sent) → transient snackbar/toast. Just "something's new" → badge. Be honest — urgency inflation is the root failure.
- **Where is the user?** In the app and active → don't interrupt: increment a badge or insert the update inline. Away → push (if opted in). Mid-task → batch for later.
- **Whose goal does it serve?** A notification that serves only the business (re-engagement nag) costs trust. If users wouldn't thank you for it, reconsider.
- **Platform** — Android toasts/snackbars vs. iOS conventions; push character limits (~39 title / ~150 body).

---

## The always-apply core (correct for almost every case)

### Match the type to the urgency

- **Badge** — dot (or count) top-right of an icon, for *unread notifications only* — never scores, weather, or marketing. Dot shape, conventional placement; disappears once seen.
- **Status badge** — at-a-glance state (online, in-progress, completed) — informational, not a ping.
- **Banner** — temporary strip (top/bottom) for events worth a glance (new message preview); doesn't block.
- **Snackbar** — bottom-of-screen confirmation in context, often with one action ("Message sent" + Undo). Never covers a FAB or important controls.
- **Toast** — low-priority system messages; can't be dismissed, can stack — use sparingly.
- **Alert** — persists until resolved; for things that demand attention. **Success = green + check, auto-dismissing; info = ℹ; warning = time-to-act heads-up; error = red + exclamation, immediate action.** Don't dress an info message as a warning.
- **Push** — reaches users outside the app; the highest-cost channel, opt-in and easiest to lose (see gated table).

### Frequency discipline

- **One event, one notification.** No re-pings for the same unread message; group related notifications instead.
- **Foreground grace:** when the app is open, update the badge or insert content into the view — don't fire a system notification at someone already looking at the screen.
- **Contextual and personal beats broadcast:** segment, reference the user's actual journey (usage limit approaching, feature they use), never spray.

### Content

- **Concise and scannable:** short title carrying the message, plain language, no jargon. Push: ~39-char title, ~150-char body — shorter is better.
- **Actionable where possible:** snackbar Undo, push actions that resolve without opening the app.

### User control (non-negotiable)

- **Easy to mute or turn off** — globally and per-type, with frequency options. Users who can tune notifications keep them; users who can't, kill them (or the app).
- **No blame or shame in opt-out flows.**

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Push notifications at all** | Time-sensitive, user-valued updates (order shipped, message received) | Re-engagement nags, generic promos — the fastest route to opt-out | Transactional first; promotional only with explicit, granular opt-in |
| **Push opt-in ask** | Primed, at a relevant journey moment, with the value stated | Raw system dialog at first launch | Prime → ask in context (see `ux-modals-and-dialogs` for permission patterns) |
| **Personalization** | Name, past behavior, preferences — measurably higher engagement | Creepy specificity; data users didn't expect you to use | Personalize from in-app behavior; stay transparent |
| **Rich media (images/GIFs)** | Visual content adds real information (product image, delivery photo) | Decoration that bloats a simple message | Text-first; media when it informs |
| **Location-based (geofencing)** | Genuine contextual value (gate change, store nearby with an active order) | Surveillance-flavored marketing pings | High bar; explicit permission, obvious value |
| **Timing optimization** | Send in users' active hours, their time zone | Optimizing for clicks over usefulness (11pm "we miss you") | User-behavior-based timing, capped frequency |
| **Badge counts vs. dots** | Counts for countable unread items (inbox) | Counts that grow unbounded and induce anxiety | Dot for "something new"; count where the number helps |
| **Performance monitoring** | Track opens/CTR *and* opt-outs/mutes as fatigue signals | Celebrating opens while opt-outs climb | Treat opt-out rate as the primary health metric |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics`, `microcopy`, and `dark-patterns` are Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — visibility of system status without disruption, match between urgency and presentation, user control and freedom.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — color-plus-icon urgency coding (never color alone), screen-reader announcement of transient messages, snackbar timing sufficient to read.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — alert styling restraint, badge/banner visual noise across the interface.
- **`ux-microcopy-audit`** *(Tier A)* — title/body brevity, plain language, CTA verb quality, opt-out wording.
- **`ux-dark-patterns-audit`** *(Tier A)* — the backlog flags this skill as attention-respect territory: manufactured urgency, nag loops, buried mute settings, guilt-trip opt-outs.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer; applies only on mobile)* — when the context is mobile: snackbar/FAB layout, push rendering across OSes.

If the audits surface a conflict (e.g., engagement targets vs. notification fatigue), resolve back toward the primary task: a notification system only works while users trust it — protect that trust over any single campaign.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Every message styled as an urgent alert | Type matched to real urgency; most messages are quiet |
| Re-ping the same unread message hourly | One event, one notification; group the rest |
| System notification while the user is in the app | Badge increment or inline insert |
| Badge count showing the weather | Badges for unread notifications only |
| Success modal interrupting the flow | Auto-dismissing snackbar/success alert |
| Snackbar covering the FAB | Snackbar above all content, clear of controls |
| Push permission dialog at first launch | Primed, contextual ask with stated value |
| "We miss you 😢" at 11pm | Time-zone-aware, behavior-based, user-valued pings |
| Mute buried four screens deep | Per-type controls, easy global off |
| 150 characters of jargon | ~39-char title that carries the message |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy + dark-patterns |

---

## Source lessons (Uxcel)

- [Notification Types & When to Use Them](https://uxcel.com/lessons/notification-types-756)
- [Best Practices for Designing Notifications](https://uxcel.com/lessons/notifications-best-practices-164)
- [Push Notification Strategies That Drive Engagement](https://uxcel.com/lessons/push-notification-strategies-that-drive-engagement-774)
- [Designing Mobile Notifications & Dialogs](https://uxcel.com/lessons/mobile-notifications--dialogs-142)
