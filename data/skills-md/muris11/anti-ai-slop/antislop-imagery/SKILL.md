---
name: antislop-imagery
description: "Imagery and decoration rules: generic illustrations, stock AI imagery, aurora/3D blobs, noise/grain, dot grids, decorative icons-in-squares, and excessive borders/transparency. Map to antislop-master A-11/A-12/A-14, D-3. Use when choosing or auditing visuals and backgrounds."
allowed-tools: Read Write Edit Glob Grep
---
# antislop-imagery

> Imagery and decoration rules for anti-ai-slop. Map to **A-11, A-12, A-14** (background/decoration) and **D-3** (icons) in `antislop-master`.
>
> Decoration should *support* the product's meaning. When the same blobs, grids, and stock illustrations appear on every site, they stop meaning anything.

---

## Background & decoration

- **Aurora / mesh-gradient blobs** behind heroes: usually a filler that adds no product meaning. (A-11)
- **Decorative dot-grid / blueprint grid** backgrounds: only with an identity tie, never as a default. (A-12)
- **Noise / grain overlay** applied "for texture" with no art direction. (A-12 family)
- **3D blobs / floating abstract shapes** that do no work — they're a default, not a decision. (A-11)
- **Excessive borders**: a 1px gray border on nearly every component flattens hierarchy. (A-14)
- **Excessive transparency**: overlay-on-overlay that hurts readability. (A-10)

Every one of these is **P3** — fine if it serves brand identity, slop if it's there because the template had it.

## Illustrations & stock

- **Generic Undraw / Storyset-style illustrations** (people near abstract shapes, same palette, no product tie) are a strong tell. (see A-9)
- **Stock AI imagery** that "looks like AI" — same lighting, same "futuristic abstract city", same teal/purple cast — is a P1/P2. (A-1, A-7)
- **Illustration must connect to the product.** A finance app showing "person at a desk with a plant" is generic; something that visualizes the actual workflow is real.
- **Prefer real screenshots/UI/** evidence-of-the-product — it carries more authenticity than any illustration. (authenticity H)

## Icons

- **Icon floated inside a rounded square on every card**, even where it adds nothing, is the pattern. (D-3)
- **The same icon set / the "sparkle-magic" icon** as a default. (see D-3)
- An icon should **say something specific** (the action, the object). A decorative icon where a label would be clearer is a downgrade.
- **Use a real semantic icon**, not decoration — and never icon-plus-label for something a label alone explains.

## Images & media

- **Real images beat placeholders.** If you must use a placeholder, make it obviously a placeholder — not plausible fake content. (authenticity H, E-6)

---

## Audit checklist

- [ ] Background/decoration has an identity tie, not a template fill. (A-11, A-12)
- [ ] No generic stock/illustration with no product meaning. (A-9)
- [ ] Icons communicate something specific; no icon-in-a-box on everything. (D-3)
- [ ] Borders and transparency preserve hierarchy. (A-14, A-10)
- [ ] Placeholders are honest, not fake-plausible. (H)

Findings cite the code from `antislop-master` plus one honest reason.
