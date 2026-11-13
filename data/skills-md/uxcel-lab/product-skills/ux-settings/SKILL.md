---
name: ux-settings
description: Design or critique a settings / preferences page — organizing many options without overwhelm, plus the save model (autosave vs. explicit Save, confirmation, revert). Applies the always-true core (only relevant settings, frequency-ordered groups, plain labels, visible current status, destructive actions last, clear save feedback) and gates context-dependent levers (autosave vs. Save button, search, advanced-settings split, sensitive-change confirmation) with trade-offs. Trigger when the user asks to design or review a settings page, preferences screen, account settings, app configuration, or a save/confirmation pattern.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Settings Skill

## How this skill behaves (read first)

This is a **generative** skill. Settings is a pattern users know — the job is *get in, change one thing, get out* — and the default failures fight that: a flat dump of every option, the page used as a junk drawer for links that fit nowhere else, technical-jargon labels, no current status shown, destructive actions sitting up top where they're hit by accident, and changes that save with no feedback (or autosave where the user expected a deliberate Save). A settings screen has two design problems in one — **how the options are organized** and **how changes are saved** — and each has its own rules. So this skill gates:

1. **Establish scale, platform, and sensitivity** — how many settings, mobile vs. web, and whether sensitive data is involved decide the structure and the save model.
2. **Apply the always-true core** — relevance, grouping, plain labels, visible status, destructive-last, clear save feedback.
3. **Surface the context-dependent decisions** (autosave vs. Save button, search, advanced split, confirmation/2FA) with trade-offs.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, `ux-microcopy-audit`, `ux-information-architecture-audit`, `ux-dark-patterns-audit`, and `ux-mobile-responsiveness-audit`** for validation.

Scope & composition (per `docs/orchestration-policy.md` §9): this skill covers the **settings page and its save model** and composes lower-scope skills rather than re-deriving them. **Core children (built as part of the page):** the **choice of control** (toggle vs. checkbox vs. radio vs. slider) via `ux-selection-controls`. **Peers that own a sub-part (defer):** the **search input itself** to `ux-search` and **notification-preference depth** to `ux-notifications-and-toasts` (they own those sub-parts if reached). **Inherit, don't regenerate:** under an existing design system, take color/type/spacing from its tokens — only set those when designing from scratch.

---

## Step 0 — Establish context before designing

Ask if not known; state the assumption if proceeding without an answer:

- **How many settings?** A handful needs only grouping; dozens need search, an advanced-settings split, and disciplined frequency ordering. Don't add search to a five-option page; don't ship fifty options as one flat list.
- **Platform.** Mobile changes save expectations and adds the device-vs-app permission split (notifications/location toggles live partly in the OS). macOS users expect autosave; Windows users expect explicit Save/Apply — match the platform habit.
- **Sensitive data?** Email, password, billing, payment methods — these warrant confirmation and often two-factor verification before a change applies.
- **Audience.** General users need plain language; only a developer-facing product can assume technical terms.

---

## The always-apply core (correct for almost every settings page)

### Organize so users get in and out fast
- **Only real settings belong here.** Settings is for user preferences (notifications, privacy, appearance, account). Don't use it as a catch-all for links that fit nowhere else — that confuses and distracts.
- **Group related settings** by type (account, security, notifications…) or use case, separated with headings and white space — not one continuous list and not a wall of divider lines (visual noise).
- **Order by frequency.** The settings users change most sit at the top and are clearly visible; rarely-touched ones go lower; advanced/expert-only options hide behind an "Advanced" disclosure.
- **Make settings easy to reach** — a known spot (top corner on web, bottom bar or top corner on mobile), never buried in submenus.

### Make each control self-explanatory
- **Plain-language labels and short helper text.** Write the way the audience talks (research real vocabulary from support tickets, reviews, forums); explain non-obvious controls in a brief line placed right next to the control (proximity), not floating.
- **Show current status beside each setting** — the toggle/selected value or a one-line summary of the current configuration — so users can review choices without drilling in.
- **Label toggles by the action, not the state** — "Shake to send feedback," not "Shake to send feedback off"; the control's visual state shows on/off.

### Protect the user
- **Destructive actions (log out, delete/deactivate account) go at the bottom,** set apart by color, an icon, or extra white space — reducing accidental taps. (Note: *hiding* logout/delete to trap users is a dark pattern — put them last, don't bury them. → dark-patterns.)
- **Surface urgent system alerts at the top** — a privacy-policy change, expiring trial, or low storage deserves a badge and top placement, not a buried line.

### Close the loop on saving
- **Give clear save feedback through button states:** Save disabled until something changes → active once it does (signaling unsaved changes) → loading while saving → a non-intrusive success toast/banner confirming it saved (with Undo for reversible changes).
- **Let users leave without saving.** Closing or pressing Back should not silently persist changes; if they abandon unsaved sensitive edits, use a short, specific confirmation dialog.

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Autosave vs. explicit Save** | Autosave for single-action, easy-to-undo controls (a standalone toggle/checkbox that takes effect immediately) | Multi-field or deliberate changes, or sensitive data, where users want to confirm | Autosave atomic toggles; an explicit Save for grouped/sensitive edits; respect platform habit (macOS autosave / Windows Save) |
| **Search within settings** | More than a handful of options, or sub-menus users must scroll through; show *related* results not just exact (search "Siri" → Accessibility, Notifications…) with auto-suggest | A short page where grouping already makes everything visible | Add once scrolling/sub-menus appear — *after* first minimizing the option count |
| **Advanced-settings split (progressive disclosure)** | A mix of common and expert/complex options | Hiding a commonly-needed setting behind "Advanced" | Primary visible to all; advanced disclosed on request — ≤ the depth users can follow |
| **Confirmation / two-factor on a change** | Changing sensitive data (email, password, billing) or destructive actions | Trivial reversible toggles (confirmation fatigue) | Confirm + 2FA for sensitive/destructive; let everyday toggles apply freely |
| **Confirmation-dialog wording** | When you do confirm, the heading states the one action; CTAs are unambiguous | Generic "Warning" / "Are you sure?"; "Cancel" next to a delete (ambiguous — cancel what?) | Specific heading + action-word buttons (Leave, Stay, Delete) → microcopy |
| **Mobile: deep-link to OS settings** | A permission (notifications on/off, location) lives in the device Settings | Pretending the app can fully toggle an OS-level permission | Manage in-app what you can; explain *why* and route to system Settings for the rest |
| **Defaults** | Set defaults to the experience most users expect (validate with research/card sorting) | Defaulting from team preference/assumption | Research-backed defaults; card-sort the grouping and naming when unsure |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics`, `microcopy`, and `dark-patterns` are Tier A (auto-run); `accessibility`, `aesthetics`, `information-architecture`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — visibility of system status (current values, save state), user control & freedom (leave without saving, Undo), error prevention (confirm sensitive/destructive changes), recognition over recall.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — control labels and states announced, target sizes, focus order, contrast on status indicators.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — grouping legibility, white space over divider-line noise, a scannable hierarchy rather than a flat list.
- **`ux-microcopy-audit`** *(Tier A)* — this skill leans hard on copy: plain labels, action-based toggle labels, helper text, and confirmation-dialog headings/CTAs.
- **`ux-information-architecture-audit`** *(Tier B — offer)* — whether the grouping scheme and ordering match users' mental model (card-sort evidence), and whether labels carry scent.
- **`ux-dark-patterns-audit`** *(Tier A)* — destructive actions placed last but *not hidden*; no confirmshaming on cancellation; no forced retention friction.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer)* — touch targets, the app-vs-OS permission split, save-button reach (sticky bottom), one-handed use.

If the audits surface a conflict (e.g., security wants confirmation on everything vs. fast settings), resolve back toward the primary task: **users came to change one thing and leave — protect the dangerous changes, get out of the way on the rest.**

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Dump every option in one flat list | Group by type/use case with headings + white space |
| Use settings as a junk drawer for stray links | Only real preferences; everything else lives elsewhere |
| Order by internal logic | Order by how often users change each setting; advanced hidden |
| Technical/jargon labels | Plain words from how users actually talk; short helper text nearby |
| Hide the current value | Show each setting's status beside it |
| "Notifications: Off" as a toggle label | Action-based label ("Email notifications") + visual on/off state |
| Destructive actions up top — or hidden entirely | Last, set apart by color/space; present, not buried (→ dark-patterns) |
| Save silently / not at all | Save state: disabled → active → loading → success toast (+ Undo) |
| Autosave a multi-field or sensitive edit | Explicit Save for deliberate/sensitive; autosave atomic toggles |
| "Are you sure?" / "Cancel" on a delete dialog | Specific heading + unambiguous action-word CTAs |
| Bolt search onto a 5-item page | Minimize options first; add search when scrolling/sub-menus appear |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy + IA + dark-patterns + mobile-responsiveness |

---

## Source lessons (Uxcel)

- [How to Design Useful Settings Pages](https://uxcel.com/lessons/settings-best-practices-572)
- [Saving Changes](https://uxcel.com/lessons/saving-changes-390)
- [Mobile Settings Design](https://uxcel.com/lessons/mobile-settings-745)
