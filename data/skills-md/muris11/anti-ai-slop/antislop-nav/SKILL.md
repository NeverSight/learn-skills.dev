---
name: antislop-nav
description: "Navigation, header, hero-structure, and footer rules: a real IA with no dead links, no floating-nav-by-default, no mega-footer full of fake groups. Map to antislop-master D-8/D-10 and G-2. Use when building or auditing navigation and site chrome."
allowed-tools: Read Write Edit Glob Grep
---
# antislop-nav

> Navigation and site-chrome rules for anti-ai-slop. Map to **D-8, D-10** (components) and **G-2** (dead links, P4) in `antislop-master`.
>
> Navigation is the *information architecture made visible*. If it looks nice but doesn't actually route, it's the highest-value slop.

---

## Header / nav bar

- **Floating / glassmorphic navbar by default is a tell** — it's a choice only when it serves a real purpose (e.g. a persistent tool that needs to float). (D-7)
- **The nav must reflect the real IA.** If the product has 3 real areas, do not show 6 links to look "full".
- **No links to sections that don't exist.** (G-2) This is a hard fail.
- **Tap/click targets** must be comfortable — small text links as the *only* way to navigate is an accessibility fail. (K-3)

## Hero-structure hand-offs

- The hero should set up the **primary action or the primary promise** — not just a headline plus "Learn more". (see C-1)
- **Avoid the dual-CTA hero** ("Get Started" + "Learn More") as a default. One primary next step is clearer. (C-1)

## Footer

- **A mega-footer of fake link groups is P4.** Every group, every link must be real, else cut it. (D-10, G-2)
- **Footer is not a dump for every page.** It holds the genuinely-last-resort links: legal, contact, status, core resources.
- **No "Company / Product / Resources / Legal" block template** filled with placeholders.

## Breadcrumbs & scroll

- Long/structure-deep pages should offer a way **back** (breadcrumbs or a consistent back path), not a one-way scroll. (navigation completeness)
- Fixed bars must not cover content. (K-5)

## Audit checklist

- [ ] Nav reflects the real IA, not a template. (D-8)
- [ ] No dead links anywhere. (G-2)
- [ ] One clear primary action in the hero. (C-1)
- [ ] Footer is real; fake groups removed. (D-10)
- [ ] Keyboard can reach every nav item. (G-10)

Findings cite the code from `antislop-master` plus one honest reason.
