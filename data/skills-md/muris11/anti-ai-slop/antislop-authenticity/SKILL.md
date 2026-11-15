---
name: antislop-authenticity
description: "Content-authenticity and product-intent rules: fake metrics, testimonials, logos, compliance/performance claims, and evidence-over-claims. Map to antislop-master section H (P5) and E. Use when auditing or writing any claim, stat, or testimonial."
allowed-tools: Read Write Edit Glob Grep
---
# antislop-authenticity

> Content-authenticity and product-intent rules for anti-ai-slop. Map to **H-1 … H-5** (P5 — never ship) and **E-1 … E-8** (copy) in `antislop-master`.
>
> This tier is different. P0–P3 are about *taste*; P5 is about *honesty*. The rule is absolute: **never fabricate evidence.**

---

## The absolute rule (P5)

**Empty is better than deceptive.** If you don't have a real source, a real customer, a real certification, or a real benchmark, you say so — or you say nothing. Fabricating one of these is not a "design choice"; it is a lie that ships.

## What is never okay

- **Fake metrics**: "$3M saved", "99.9% uptime", "10x faster" with no source, period, or method. (H-1)
- **Fake testimonials**: invented names, AI avatar photos, glowing quotes from people who never used it. (H-2)
- **Fake customer logos**: the "our customers include" strip of brands you don't have. (H-3)
- **Unverifiable compliance/security/performance claims**: "SOC2 Type II certified", "bank-grade encryption", "99.99% SLA" you can't point to. (H-4)
- **Vague evidence presented as fact**: "99% of users agree" with no study. (H-5)

## Product intent (the flip side)

Authentic copy is **specific and grounded**. Replace the hype with the actual:

| Instead of | Write the real thing |
|---|---|
| "Supercharge your workflow" | what the workflow was and what changed |
| "Trusted by thousands" | your real user count, or nothing |
| "The future of X" | the actual problem you solve |
| "Seamlessly integrate" | the one integration that works today |

## The evidence test

For every claim, ask three questions:
1. **Do we have the data?** (a number with a source)
2. **Can a skeptic check it?** (a link, a doc, a name, a period)
3. **Would we defend it in writing?** (if not, cut it)

If all three aren't strong, replace the claim with an honest placeholder or remove it.

## Holding the line

- When the user asks for a fake metric/testimonial to "fill the page", **flag it.** You implement real content or an honest placeholder (e.g. a clearly-marked `[source]`/`_lorem_`), not fabricated realism.
- **Evidence-over-claims** is the standard: show, don't assert.

---

## Audit checklist

- [ ] Every number has a source and a period. (H-1)
- [ ] No invented testimonials or AI avatars. (H-2)
- [ ] No fake customer logos. (H-3)
- [ ] Compliance/security/performance claims are backed or removed. (H-4)
- [ ] Copy names the real product, not the hype. (E-1–E-8)

Findings cite the code from `antislop-master` plus one honest reason.
