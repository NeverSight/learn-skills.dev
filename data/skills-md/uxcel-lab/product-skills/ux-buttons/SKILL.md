---
name: ux-buttons
description: Design or critique UI buttons — pick the right button type for the action's importance, apply sizing/label/state best practices, and gate stylistic levers like shape, shadows, FABs, and icon-only buttons. Trigger when the user asks to design, choose, style, or review buttons, CTAs, button labels, button hierarchy, or button states.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Buttons Skill

## How this skill behaves (read first)

This is a **generative** skill. The default failure modes are opposite: **flat sameness** (every action gets the same generic button, no hierarchy, vague "Submit/OK" labels, missing states) and **decoration overload** (every button raised, shadowed, branded, icon-stuffed). A checklist is not a mandate, so this skill gates:

1. **Establish context** — platform, the screen's action hierarchy, brand personality, and whether any action is destructive.
2. **Apply the always-true core** — hierarchy-driven type selection, action-verb labels, full state coverage, accessible sizing and contrast.
3. **Surface the stylistic levers** (shape, elevation, icon-only, FAB, width strategy) as decisions with trade-offs — not defaults.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, and `ux-microcopy-audit`** for validation.

---

## Step 0 — Establish context before designing

Ask if not known; state the assumption if proceeding without an answer:

- **Platform** — mobile tightens everything: touch targets (≥48×48px), spacing between adjacent buttons, fixed widths for stacked buttons, tactile feedback. Desktop relies on hover/cursor cues instead.
- **Action hierarchy on this screen** — what is the *one* thing the user came to do? That action gets the only primary button; everything else is secondary or tertiary.
- **Brand personality** — serious/trustworthy vs. friendly/playful decides shape (sharp ↔ rounded ↔ pill) and how expressive styling can get.
- **Destructive or irreversible actions?** — these flip defaults: explicit verb labels ("Delete project," never "Yes"), semantic color (red family), never a FAB, never the visually dominant button by default.

---

## The always-apply core (correct for almost every case)

### Pick the type from the action's importance — not from looks

- **Primary** — the action the interface wants users to take. One per view, most visually prominent (saturated, contrasting fill). If everything is prominent, nothing is.
- **Secondary** — the alternative (Cancel next to Submit). Subdued: outlined/ghost works well, but the outline needs enough contrast to stay visible.
- **Tertiary** — rare or low-priority actions. Text buttons, muted colors, smaller weight; place them away from the primary to prevent accidental taps.
- **Grouping types**: a **menu/dropdown button** tucks related actions of equal importance into a list; a **split button** adds a default one-click action plus a dropdown — keep a visual separator so users don't expect the whole button to open the menu; a **toggle group** keeps 2–3 mutually exclusive options visible with one selected.
  - ❌ A dropdown as a catch-all bucket of unrelated actions ✅ Only related actions, grouped to simplify the decision

### Labels are commands

- **Specific action verbs** that state the result: ❌ "Yes" / "No" / "OK" / "Go" ✅ "Delete project" / "Save changes" / "Subscribe"
- **2–3 words, one line.** Two-line labels cause wrong choices. No italics, underline, or end punctuation; a heavier weight than body copy is enough.
- **Minimum 16px label size**, centered horizontally and vertically.
- **Icons go on the left** (in LTR languages) where they aid recognition — trailing icons are decoration, except the dropdown arrow, which the leading icon leaves room for.
- **Icon + label beats either alone.** A floppy disk means nothing to part of your audience; a label makes it explicit and gives screen readers something to announce.

### Design every state, not just the resting one

Enabled, **hover**, **pressed** (brief but crucial feedback that the tap registered), **focused** (a visible ring/border — vital for keyboard and assistive-tech users; don't style it so close to other states that it's ambiguous), and **disabled** (grayed out, clearly inert). Buttons that toggle something on/off must make the current direction explicit.

### Size, space, and contrast are not negotiable

- **Touch target ≥ 48×48px on mobile** (~9mm finger pad, per WCAG/Material guidance); on desktop, generous padding keeps click areas honest.
- **Padding rule of thumb:** horizontal padding ≈ 2× vertical; at minimum an uppercase "W" fits between label and edge.
- **Set a minimum width** for hug-content buttons — overly narrow buttons miss the target size and stop looking like buttons.
- **Adequate spacing between adjacent buttons** so fingers don't slide onto the wrong action.
- **Contrast:** button-vs-background and label-vs-button both meet WCAG (4.5:1 normal text, 3:1 large). On image backgrounds, add a semi-opaque layer. Exact ratios → defer to the `accessibility` audit.

### Be consistent and predictable

- **One button style system product-wide** — same colors, shapes, typography, and placement for the same actions everywhere (Principle of Least Astonishment).
- **It must look like a button.** Affordance beats creativity: users should never have to guess what's clickable.
- **Place buttons where users expect them** — at the natural end of the reading flow (Gutenberg/Z-pattern: primary action bottom-right of the content it concludes), never hidden.
- **Color carries meaning:** red for destructive, your accent for primary. Align with conventions; don't make users learn a private color language.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0. **Applying all of these by default is the decoration-overload failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Shape: sharp ↔ rounded ↔ pill** | Sharp = serious, solid (finance, insurance); rounded = friendly, safe; pill = playful, informal | Sharp corners on a warm consumer brand; pills in formal/enterprise UI | Slightly rounded rectangle — the familiar, trusted middle; pill radius = ½ height + extra horizontal padding |
| **Elevation / shadows** | Raised buttons to lift the primary action; flat for everything else | Shadows on transparent buttons or near labels (kills legibility); big dark default-black shadows | Shadow tinted near the button's color, <40% opacity, smaller than the button — depth cue, not decoration |
| **Icon-only buttons** | Routine actions with universal icons (edit, delete, search, home) in tight space | Any icon users must decode; anywhere without an accessible name | Icon + label; if icon-only, universal symbol + accessible name |
| **FAB** | One fixed, constructive, most-used action in an app (compose, add) | Destructive actions; more than one per page; content it would cover | At most one, only if the app has a single dominant create-action |
| **Branded buttons** ("Sign in with Google") | Third-party auth/integration points | Restyling them to match your UI — breaks trust and brand guidelines | Use the brand's official assets verbatim, placed where the action occurs |
| **Custom shapes** | The shape amplifies the function (arrow-shaped "Next") | Novelty that obscures clickability | Stick to conventions; if custom, reinforce affordance with contrast/size/shadow |
| **Width: hug vs. fixed** | Fixed width for stacked primary/secondary on mobile — balanced, scannable | Fixed width truncating long labels (i18n) | Hug with a minimum width on web; fixed for stacked mobile pairs |
| **Tactile feedback** | Mobile: subtle vibration on tap confirms registration | Stacking every visual + tactile effect at once (overwhelming) | Visual state change always; haptics as a light mobile enhancement |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics` and `microcopy` are Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — visibility of system status (states/feedback), consistency, error prevention around destructive buttons.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — contrast ratios, touch-target sizes, focus visibility, accessible names for icon-only buttons.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — hierarchy clarity and whether styling tipped into decoration overload (competing primaries, shadow soup).
- **`ux-microcopy-audit`** *(Tier A)* — label clarity, action-verb phrasing, consistency of command language across the product.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer; applies only on mobile)* — when the context is mobile: target sizes, spacing, and stacked-button layout.

If the audits surface a conflict (e.g., brand expressiveness vs. affordance), resolve back toward the primary task: the user must instantly recognize and successfully hit the right action.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Three equally prominent buttons on one screen | One primary; secondary/tertiary visibly subordinate |
| "Yes" / "No" / "OK" labels | Action verbs stating the result: "Delete project," "Save changes" |
| Icon-only button with a clever-but-obscure symbol | Universal icon + label (or accessible name at minimum) |
| Design only the resting state | Enabled, hover, pressed, focused, disabled — all distinct |
| 32px-tall tappable area on mobile | ≥48×48px touch target with breathing room between buttons |
| FAB for "Delete account" | FAB only for the app's main constructive action — or no FAB |
| Restyle "Sign in with Google" to match your palette | Official brand assets, untouched |
| Shadow every button for "depth" | Elevation only where it signals priority; tinted, subtle, smaller than the button |
| Different styles for the same action across screens | One consistent button system product-wide |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy |

---

## Source lessons (Uxcel)

- [UI Buttons & When to Use Them](https://uxcel.com/lessons/types-344)
- [Types of UI Buttons](https://uxcel.com/lessons/anatomy-ii-466)
- [Best Practices for Designing UI Buttons](https://uxcel.com/lessons/anatomy-iii-298)
- [Best Practices for Writing Button Labels](https://uxcel.com/lessons/button-label-best-practices-673)
- [11 Tips on Designing Mobile Buttons](https://uxcel.com/lessons/tips-on-designing-mobile-buttons-419)
- [UI Component States](https://uxcel.com/lessons/component-states-499)
