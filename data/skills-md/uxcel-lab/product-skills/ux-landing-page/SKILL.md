---
name: ux-landing-page
description: Design or critique a landing page — a focused, conversion-oriented page built around a single goal (sign up, buy, book a demo, subscribe). Applies the always-true core (one focus, a compelling headline, an obvious value proposition, a prominent CTA, trust signals) and gates context-dependent levers (keeping or cutting site nav, perks/reciprocity, chat widget, long vs. short scroll) with trade-offs. Trigger when the user asks to design or review a landing page, marketing page, hero section, product/campaign page, or "page that converts."
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Landing Page Skill

## How this skill behaves (read first)

This is a **generative** skill, and a landing page has exactly **one job**: move the visitor toward a single conversion goal. The default failure is the **everything page** — full site nav, several competing offers, a vague headline, walls of copy, and a CTA you have to scroll to find — so attention scatters and nobody converts. (Users form a first impression in ~0.05s and read as little as ~20% of the copy.) The opposite failure is a beautiful hero with no value proposition and no reason to trust it. So this skill gates:

1. **Establish the single conversion goal and who's arriving** — that decides what stays on the page and what gets cut.
2. **Apply the always-true core** — one focus, a sharp headline, an obvious value proposition, a prominent CTA, trust signals, fast and responsive.
3. **Surface the context-dependent decisions** (cut vs. keep nav, perks, chat, scroll length) with trade-offs.

Then it **hands off to `ux-aesthetics-audit`, `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-microcopy-audit`, `ux-dark-patterns-audit`, and `ux-mobile-responsiveness-audit`** for validation.

Scope & composition (per `docs/orchestration-policy.md` §9): this skill covers the **landing page itself** and composes lower-scope skills rather than re-deriving them. **Core children (built as part of the page):** **CTA button mechanics** via `ux-buttons`. **Downstream (offer, don't auto-build):** **pricing tables** via `ux-pricing` and the **post-click sign-up/checkout** via `ux-login-signup` and `ux-checkout-payment`. **Inherit, don't regenerate:** under an existing design system, take color/type/spacing from its tokens — only set those when designing from scratch.

---

## Step 0 — Establish context before designing

Ask if not known; state the assumption if proceeding without an answer:

- **What's the single conversion goal?** Sign up, buy, book a demo, subscribe, download. One page, one primary action — everything else is subordinate. If stakeholders want several goals, that's a prioritization conversation, not five equal buttons.
- **Who's arriving, and how aware are they?** A specialized audience tolerates (some) domain terms; a general or top-of-funnel audience needs plain language and more context before the ask. Traffic source (an ad for one feature vs. a homepage) shapes how tightly the page must match the promise that brought them.
- **Campaign landing page vs. a page within the site?** A dedicated campaign page often *removes* global nav to protect focus; a page inside the main site usually keeps it for wayfinding. This single choice flips several defaults.
- **Product type & brand** — bounds image style, tone, and whether playful copy fits.

---

## The always-apply core (correct for almost every landing page)

### Focus — protect the single goal
- **Remove anything that doesn't support the primary action.** Cut secondary offers, decorative imagery that doesn't carry meaning, and (on campaign pages) even global navigation. Every element should earn its place by moving the visitor toward the goal.
- **Make copy scannable.** Limit paragraphs to ~3–4 lines, add a descriptive subheading every couple of paragraphs, and lead with the point — users skim, they don't read.

### The message — headline + value proposition
- **A compelling, concise headline.** It's the first thing that earns the ~0.05s first impression; keep it clear, relevant to the offer, and short. Avoid cleverness that obscures what this is.
- **Make the value proposition obvious and high on the page.** In clear language (plus a supporting visual), answer three questions: *what is it, how does it benefit me, how does it work?* This is the elevator pitch — it shouldn't require scrolling to find.
- **No jargon.** Use the audience's words; if a technical term is unavoidable for a specialist audience, define it first. Jargon costs readability *and* credibility.

### The ask — the CTA
- **One prominent primary CTA, visible without scrolling.** Accent/contrasting color, generous size (≥44×44px target), active-verb label that names the action ("Start free trial," not "Submit"). On long pages, repeat the CTA at intervals.
- **If content continues below the fold, add a scroll cue** (e.g., a downward arrow) so visitors don't assume the page ends at the hero.

### The trust — why believe you
- **Social proof.** Reviews, ratings, testimonials, usage stats — people don't want to be first; most trust peer recommendations and public opinions. Show real, specific proof.
- **Brand authority.** Logos of well-known customers, partners, or media mentions reassure visitors the offer is legitimate.

### The mechanics — it has to actually work
- **Responsive across devices** — headline and CTA especially must render and stay tappable from desktop to phone.
- **Fast load** — aim under ~2.5s; slow pages (especially on mobile) bleed visitors before they see anything.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0. **Stacking every persuasion lever — perks + urgency + pop-ups + sticky chat — is the failure mode; it reads as a hard sell and erodes trust.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Keep vs. remove global navigation** | Keep on a page within the main site (wayfinding) | Remove on a single-goal campaign page where nav is an exit | Match to page type; when the goal is one conversion, cut nav that competes |
| **Perks / reciprocity** (discount, free shipping, bonus) | A genuine incentive that fits the offer; reciprocity nudges action | Manufactured "free gift" that cheapens trust, or perks irrelevant to the goal | Use a real, relevant incentive — keep it honest (→ dark-patterns) |
| **Chat / support widget** | Considered purchases where first-time visitors have questions | Mobile — sticky chat overlays filters/CTAs/Checkout and frustrates | Offer it; make sticky chat a **desktop-only** treatment |
| **Scroll length** (short hero-only vs. long-form) | Long-form for complex/considered offers needing education and proof | A long page for a simple, low-consideration action | Match length to decision complexity; keep one goal regardless of length |
| **Social-proof type** (testimonials / stats / logos / ratings) | Pick what your audience trusts most and what you can show honestly | Vague or unverifiable claims ("loved by thousands") | Specific, real proof over generic superlatives |
| **Personality / humor in copy** | Brands where it fits and the decision is low-stakes | Serious/high-trust offers (finance, health) or where it muddies the value prop | Warmth yes; never at the cost of a clear value proposition |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics`, `microcopy`, and `dark-patterns` are Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — visual hierarchy with one clear focal point (the CTA / value prop), the hero not overcrowded, scannable rhythm rather than text walls.
- **`ux-heuristics-audit`** *(Tier A)* — does the page match the promise of the ad/link that brought the user; is the next step obvious; is system status clear on the CTA action.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — CTA contrast and target size, heading hierarchy, image alt text, readable body type.
- **`ux-microcopy-audit`** *(Tier A)* — headline clarity, value-proposition wording, jargon, CTA label quality.
- **`ux-dark-patterns-audit`** *(Tier A)* — the conversion-pressure traps a landing page invites: fake urgency/scarcity countdowns, manipulative or fabricated social proof, confirmshaming the decline, and pop-ups that trap. Persuasion should be honest.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer)* — headline/CTA rendering and reach on phones, the sticky-chat caveat, fast mobile load, tap targets.

If the audits surface a conflict (e.g., marketing wants three offers and a countdown), resolve back toward the primary task: **one visitor, one decision — remove anything that doesn't help them make it.**

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Cram multiple offers + full nav + walls of text | One goal; cut everything that doesn't serve it |
| Clever headline that hides what this is | Clear, concise headline relevant to the offer |
| Bury the value proposition below the fold | Answer what/benefit/how, plainly, up high |
| Impress with jargon | Audience's language; define unavoidable terms |
| "Submit" / a low-contrast button mid-page | Active-verb CTA, accent color, ≥44px, visible without scrolling |
| Decorative stock imagery that carries no meaning | Contextual images that reinforce the message |
| Ask for the conversion with no reason to trust | Social proof + brand authority, specific and real |
| Stack urgency + perks + pop-ups + sticky mobile chat | Honest incentives; sticky chat desktop-only (→ dark-patterns) |
| Assume the hero is the whole page | Scroll cue when content continues below the fold |
| Ship a slow, desktop-only layout | Responsive; headline & CTA intact on mobile; load < ~2.5s |
| Ship without checking | Hand off to aesthetics + heuristics + accessibility + microcopy + dark-patterns + mobile-responsiveness |

---

## Source lessons (Uxcel)

- [How to Design Landing Pages That Convert](https://uxcel.com/lessons/landing-page-best-practices-635)
