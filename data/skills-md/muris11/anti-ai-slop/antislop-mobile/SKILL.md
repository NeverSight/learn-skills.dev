---
name: antislop-mobile
description: "Mobile, responsive, and Flutter/native UI rules: real reflow, no horizontal overflow, 44px tap targets, touch-equivalent interactions, fixed bars that respect content, and no web-framework look forced into native. Map to antislop-master section K and R-03. Use when building or auditing mobile or cross-platform UI."
allowed-tools: Read Write Edit Glob Grep
---
# antislop-mobile

> Mobile, responsive, and Flutter/native rules for anti-ai-slop. Map to **K-1 … K-8** in `antislop-master`.
>
> "It works on desktop" is not a mobile design. A responsive page is a **reflow**, not a shrink.

---

## The reflow rule

- **A mobile layout is its own thing**, not the desktop grid squished. Columns collapse and stack; type and spacing use a mobile scale. (K-2)
- **No horizontal overflow** on the narrowest real device — this is the #1 hard fail. (K-1)
- **Touch elements ≥ ~44×44px** so a finger can land. (K-3)

## Interactions

- **Hover-only interactions need a touch equivalent** (a tap, a long-press, an always-visible affordance). (K-4)
- **Fixed bars (nav, bottom sheets) must not cover content** — add safe padding/margins. (K-5)
- **Keyboard on mobile**: forms must handle the on-screen keyboard (scroll into view, don't hide the field). (see G, K)

## Flutter / native

- **Don't paste the web-framework look straight into native.** Flutter has platform-aware tools (`Material`/`Cupertino`); use them. (K-6)
- **The web "centered hero + 3 cards" formula on a phone** is out of place. (K-8) On a small screen, one real thing at a time.
- **Respect native idiom** — bottom nav, swipe back, platform icons, safe areas. A web-centered page in a native shell is a tell. (K-6, K-7)
- **Use the platform's text/scroll/inset conventions**, not a re-skin of the desktop layout.

## Cross-check to master

- K-1 maps to the hard mobile gate: overflow/clipping = fail. (R-03)
- K-3/K-4 map to interaction and accessibility (G-9, G-10).
- K-6/K-7 are about platform *intent*, not imitation.

---

## Audit checklist

- [ ] Mobile reflows, doesn't shrink. (K-2)
- [ ] No overflow/clipping on the narrowest device. (K-1)
- [ ] Tap targets are comfortable. (K-3)
- [ ] Touch equivalents exist for hover interactions. (K-4)
- [ ] Fixed bars respect content. (K-5)
- [ ] Flutter/native shows platform intent, not a web copy. (K-6–K-8)

Findings cite the code from `antislop-master` plus one honest reason.
