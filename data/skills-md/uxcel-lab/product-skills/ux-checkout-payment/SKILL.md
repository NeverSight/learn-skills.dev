---
name: ux-checkout-payment
description: Design or critique a checkout, cart, payment, or booking flow — the path from "ready to buy" to "order confirmed." Applies the conversion-protecting core (guest checkout, transparent cost summary, inline validation, processing feedback, confirmation) and gates context-dependent levers (name fields, payment-method count, single- vs. multi-step, booking date pickers, promo-code prominence) with trade-offs. Trigger when designing or reviewing a checkout page, shopping cart, payment form, card-entry screen, promo/discount code, booking/reservation flow, or when checkout/cart abandonment needs improving.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Checkout & Payment Flow Skill

## How this skill behaves (read first)

This is a **generative** skill. Checkout is the highest-stakes flow in the product — every bit of friction here is paid for in abandoned carts, and the defaults are *leaky*. The instinctive design — force account creation, show one long form, validate only on Submit, drop a blank promo box, surface the final price with no breakdown, and dead-end after payment — bleeds motivated buyers at the last step. This flow is a sequence — **cart → identity → details/address → payment → processing → confirmation** (booking swaps the front for *search availability → select*) — and which stages need investment depends on what's being bought. So this skill gates:

1. **Establish what's being bought and for whom** — that decides the stages, the fields, and the payment mix.
2. **Apply the always-true core** — the conversion-protecting patterns that hold for essentially every transaction.
3. **Surface the context-dependent decisions** (name fields, payment-method count, single- vs. multi-page, booking pickers, promo prominence) with trade-offs.

Then it hands the result to the audit lenses for validation (candidates; posture per `docs/orchestration-policy.md`). **Composition (§9):** checkout composes `ux-inputs-and-forms`, `ux-buttons`, and `ux-selection-controls` as core children, and defers confirmation-modal mechanics to `ux-modals-and-dialogs` and toast behavior to `ux-notifications-and-toasts` (peers — they own those sub-parts if reached). Under an existing design system, inherit color/type/spacing tokens.

---

## Step 0 — Establish context before designing

Ask if not known; state the assumption if proceeding without an answer:

- **What's being bought?** **One-time purchase** (physical goods → shipping address + cart summary; digital → no shipping) vs. **booking/reservation** (date/time/availability is the core, front-loaded by a search step) vs. **subscription** (recurring terms, trial-to-paid, must state billing cadence clearly). This reshapes which stages exist.
- **Platform** — mobile tightens everything: input steppers over dropdowns for quantity, single name field, contextual numeric keypads, OTP autofill, ≥48×48dp touch targets spaced ≥8dp. Desktop has room for labels and side-by-side summary.
- **Audience / region** — international means single name field, country-first address hierarchy, and a region-appropriate payment mix (credit cards are *not* universal — weak in Germany, China, etc.). Domestic single-region relaxes these.
- **Account model** — does the product genuinely need an account to function, or is that just data collection? This decides how hard guest checkout is fought for.

Anchor on the one fact that governs the whole flow: **the user already decided to buy.** Every screen's only job is to remove reasons to stop.

---

## The always-apply core (correct for almost every checkout)

### Protect the conversion

- **Offer guest checkout — and make it the prominent option.** Forcing signup before purchase is intimidating and a top abandonment cause; delaying account creation lifts completion. Offer registration *after* the order is placed (one-click, since you already have their details).
  - ❌ Account-selection step where "Create account" is the big button and guest checkout is a buried text link.
  - ✅ "Continue as guest" is the primary, most prominent path; account creation offered on the confirmation screen.
- **Remove distractions from the checkout page.** Its only purpose is completion. Strip the top nav and footer links, kill ads and pop-ups, and let users edit items in place rather than leaving. Keep only essentials (e.g. a live-support link).
  - ❌ Full site header, mega-menu, newsletter pop-up, and footer link farm on the payment page.
  - ✅ Logo, a back-to-cart affordance, support link — nothing else competing with the pay button.

### Make the cost trustworthy

- **Summarize the order before payment, with the *full* cost breakdown** — line items, quantity, thumbnail (matching the chosen variant/color), product-page links, delivery charges, and taxes. Showing only a final total erodes trust; revealing fees late is a dark pattern.
- **In the cart, show a clear summary and keep the checkout button after the order details** so users review before proceeding. Indicate item count (a visible cart badge), allow quantity edits via steppers, in-cart variant editing, and bulk removal — never make a mistake mean starting over.

### Reduce the typing

- **Enable autofill everywhere** — browser autofill for name/address/email/phone, saved card details, card scanning, and OTP autofill so users don't toggle apps mid-payment. Pair with security measures since the data is sensitive.
- **Use input masks and smart defaults on card entry** — auto-format the card number into groups, auto-detect card type from the first digits (no manual brand picker), and fetch currency from the selected country.

### Validate kindly, fail gracefully

- **Inline validation on every field, on blur — not on Submit.** A form that hides errors until submit gets abandoned. Validate when the user leaves the field (not keystroke-by-keystroke, which feels intrusive), and confirm successes, not just failures.
- **Error messages are explicit, concise, polite, precise, constructive, human** (NN/g). Never blame the user; say what went wrong and how to fix it. Better still, write labels/placeholders clearly enough to prevent the error.

### Never leave the user hanging

- **Show payment processing.** Payments take seconds-to-minutes; a loading/status screen reassures users and prevents double-submits and panic.
- **Confirm success on screen *and* by email.** A success message (clearly visible, persistent enough to read) → a confirmation screen → a detailed email: order summary, full cost breakdown, estimated delivery/next steps, tracking, support details, and a guest-to-account registration offer. Outline what happens next ("we'll email shipping updates," "activate your subscription") — don't imply the job's done at payment.

### Reinforce security (perceived and real)

- **Add visual security cues** at the payment step: HTTPS + a padlock, and trust seals/SSL badges (Norton, TRUSTe, BBB, etc.). Most users judge security on gut feel; these cues raise it. (Lack of perceived security and too few payment options are documented abandonment causes.)

### Promo codes that don't leak conversions

- **Never show a blank promo box with a big Apply button** — it makes users without a code feel they're missing a deal, so they leave to hunt for one and don't return. Use a subtle **"Have a promo code?" link that expands into the input on click.**
- **Apply with a click, not recall** — let users select from available codes or apply from an email/ad directly; auto-apply global promos (signup, threshold) rather than asking them to retype. **Reflect the discount in the total**, shown near it, and give clear **success / error / remove** states (expired-code errors should link to other available offers).

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0. **Applying all of these by default is the failure mode — e.g. splitting every checkout into five pages, or offering every payment method on earth.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Single "Full Name" vs. separate First/Last** | Single: global audience, mobile, fewer errors & faster typing (esp. cultures with family-name-first) | Separate: marketing personalization ("Hey John"), or medical/government/financial ID requirements, or APIs that need them split | Single field unless an identity/personalization requirement forces a split |
| **Number of payment methods** | More methods help international sales and cut the "no convenient method" abandonment (~9%) | Too many causes choice paralysis and each adds cost | Offer the methods *relevant to your audience/region*, most-popular first; expand as you grow — don't list everything |
| **Single-page vs. multi-step checkout** | Multi-step (with a progress tracker) when there are many fields — chunking lowers cognitive load | A short form split into needless pages adds clicks | Single page if short; multi-step **with a progress tracker** (or one-page accordion) when long. Always signal where they are and how many steps remain |
| **Country-first address hierarchy** | Shipping internationally/nationally — country/state determines which fields and formats apply | Single-region store with one fixed format | Ask country/state first when regions vary; then show only relevant, well-labeled fields with example placeholders |
| **Booking: date-range picker & availability** | Booking/reservation flows — the picker *is* the core interaction | One-time product purchase (no scheduling) | Prominent search bar at top; highlight selected range with hover states; make *today* obvious; autofill on range select; keep departure/destination (or equivalents) grouped in natural order and swappable; persist the query on the results page |
| **Booking: save / bookmark results** | Discretionary, comparison-heavy bookings (travel, stays) where decisions span sessions | Quick transactional bookings | Offer a bookmark/heart with a tooltip for save-for-later; skip for fast single-step bookings |
| **Promo code prominence** | Expandable link (default) keeps non-promo users focused | A persistent open field is fine *only* if a code is near-universal (e.g. a campaign landing) | Collapsed "Have a code?" link → expands on click; plus a selectable list when you control which codes exist |

> **One context that flips several defaults at once: mobile.** It pushes you toward the single name field, input steppers, contextual keypads, OTP autofill, and large spaced touch targets simultaneously — design the mobile checkout as its own thing, not a squeezed desktop one.

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After designing or revising, hand the output to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole flow through `ux-design-review`. Here, **`dark-patterns`, `heuristics`, and `microcopy` are Tier A (auto-run); `accessibility`, `aesthetics`, `mobile-responsiveness`, and `information-architecture` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only when the platform is mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-dark-patterns-audit`** *(Tier A)* — the highest-priority hand-off here. Checkout concentrates the worst offenders: **hidden costs surfaced late** (drip pricing), **forced account creation**, **sneak-into-basket** add-ons/insurance pre-checked, **forced continuity** (trial auto-converting silently), and **confirmshaming** a decline. The transparent cost summary, guest checkout, and clear subscription terms in the core exist to keep this audit clean.
- **`ux-heuristics-audit`** — visibility of system status (cart badge, processing state, applied discount, step progress), user control (edit cart, remove promo, go back without losing data), error prevention and recovery.
- **`ux-accessibility-audit`** — keyboard operability of pickers/steppers, touch targets (≥48dp, ≥8dp spacing), contrast, focus management across steps, labels on every field.
- **`ux-aesthetics-audit`** — cart/summary hierarchy (product name + price emphasized), the pay button as the clear focal point, no clutter competing with completion.
- **`ux-microcopy-audit`** — field labels and placeholders that prevent errors, human error messages, CTA wording, the confirmation/next-steps copy, and subscription/billing terms stated plainly.
- **`ux-mobile-responsiveness-audit`** — when context is mobile: steppers, contextual keypads, one-handed reach, the mobile-specific name/address treatment.
- **`ux-information-architecture-audit`** — for multi-step or booking flows: whether the step sequence and the availability/results structure match users' mental model.

If the audits surface a conflict (e.g. more payment methods vs. choice paralysis, or security badges vs. visual clutter), resolve back toward the primary task: **the user already decided to buy — remove reasons to stop, add nothing that doesn't speed completion.**

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Force account creation before purchase | Prominent guest checkout; offer registration after the order |
| Show the final price only | Full cost breakdown — items, shipping, taxes — before payment |
| Reveal fees/shipping at the last step | Surface all costs in the cart and summary up front (→ dark-patterns) |
| Keep full nav, footer, ads, pop-ups on the checkout page | Strip distractions; only completion-essential links remain |
| Validate the whole form on Submit | Inline validation on blur; confirm successes too |
| "Invalid input." / blame the user | Explicit, polite, constructive message — what's wrong and how to fix it |
| Blank promo box + big Apply button | Collapsed "Have a code?" link; click-to-apply; reflect discount in total |
| Dropdown to change quantity on mobile | Input stepper; in-cart editing; bulk remove |
| Manual card-type picker, unformatted number field | Auto-detect type, input mask, autofill, OTP autofill |
| Freeze or jump silently while charging | Show a processing state; then on-screen + email confirmation |
| End at "Payment complete." | Confirmation + next steps + detailed email + registration offer |
| Split a 4-field form across 4 pages | Single page if short; multi-step **with progress** only when long |
| Offer every payment method available | The methods relevant to the audience/region, popular first |
| Ship without checking | Hand off to dark-patterns + heuristics + accessibility + aesthetics + microcopy |

---

## Source lessons (Uxcel)

- [How to Design Checkout Pages that Convert](https://uxcel.com/lessons/checkout-best-practices-484)
- [Making a Payment](https://uxcel.com/lessons/making-a-payment-097)
- [Best Practices for Designing Shopping Carts](https://uxcel.com/lessons/shopping-cart-best-practices-071)
- [Best Practices for Designing Booking Flows](https://uxcel.com/lessons/booking-best-practices-107)
- [Entering a Promo Code](https://uxcel.com/lessons/entering-a-promo-code-897)
