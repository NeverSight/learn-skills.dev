---
name: landing-page-optimization
description: Use when working on landing pages — creation, copywriting, design, optimization, or conversion rate improvement. Covers hero sections, above-the-fold content, value propositions, CTAs, landing page templates, and high-converting page structure. Applies to sales pages, lead capture pages, product pages, and marketing site pages. Use this skill for landing page copy, landing page design, landing page optimization, CTA writing, conversion rate optimization, hero section content, value proposition work, and any page builder or landing page template tasks.
---

# Landing Page Optimization

Build, write, and optimize high-converting landing pages combining proven copy frameworks, the 11-essential-elements structure, and a clear creation workflow.

---

## 1. Copy Framework

### Gather Before Writing

Collect these inputs before drafting any copy:
- Product/service name and core value proposition
- Target audience and their primary pain point
- Key differentiator vs alternatives
- Desired visitor action (CTA goal)
- Available social proof (testimonials, stats, logos)

### Choose a Framework

| Framework | When to Use |
|-----------|-------------|
| **PAS** (Problem → Agitate → Solution) | Strong pain point, emotional product |
| **AIDA** (Attention → Interest → Desire → Action) | General purpose, awareness campaigns |
| **StoryBrand** (Hero → Guide → Plan → CTA → Success) | Brand narrative, relationship-driven sales |

### Section Copy Guide

**Hero** — Value prop in ≤10 words; subheadline adds specificity; CTA + 1 trust signal above fold.

Headline formulas:
- `[Achieve outcome] without [pain point]`
- `The [adjective] way to [desired result]`
- `Stop [bad thing]. Start [good thing].`

**Problem** — Name the pain in the audience's language; 2–3 specific scenarios; emotional, not clinical.

**Solution** — How the product solves it; 3–5 features written as benefits ("saves 2 hrs/day" not "automated scheduling").

**How It Works** — 3–4 steps, each with a clear action verb; close with CTA.

**Social Proof** — Testimonial template: `"[Specific result]..." — Name, Title, Company`. Aim for 4–6 testimonials; include stats and logos if available.

**Pricing** — Highlight recommended plan; include guarantee copy; one CTA per plan card.

**FAQ** — 5–10 objection-handling questions; cover pricing, refunds, technical requirements, comparison to alternatives.

**Final CTA** — Repeat the primary CTA; add urgency or risk-reversal ("Cancel anytime", "30-day guarantee"); larger and more dramatic than hero CTA.

### CTA Copy Rules
- Start with an action verb
- Be specific: "Start My Free Trial" > "Submit"
- First-person phrasing often converts better ("Get My Guide")
- Avoid: "Click Here", "Learn More", "Submit"

### Copy Best Practices
- Active voice, present tense; benefits before features
- Specific numbers over vague claims ("saves 2 hours" not "saves time")
- Short sentences; scannable with headers and bullets
- Address objections before the reader voices them
- Multiple CTAs (same action) throughout — not multiple competing actions

---

## 2. Design Principles (11 Essential Elements)

Every landing page needs all 11 elements. See `references/11-essential-elements.md` for full detail on each.

| # | Element | Conversion Purpose | Design Note |
|---|---------|-------------------|-------------|
| 1 | URL | SEO slug with keywords | — |
| 2 | Header/Logo | Brand trust, navigation | Sticky with blur-on-scroll |
| 3 | Hero Title + Subtitle | Clear value prop, H1 with keywords | Distinctive display font, 4–6rem |
| 4 | Primary CTA | Hero conversion | Contrasting color, micro-interaction on hover |
| 5 | Social Proof | Credibility, reduce hesitation | Animated counts, overlapping avatars |
| 6 | Images/Videos | Product demonstration | Device mockups or demo video; no stock photos |
| 7 | Benefits/Features | Justify the purchase | 3–6 items with icons; benefits-first copy |
| 8 | Testimonials | Peer validation | 4–6 with photo + name + role; specific results |
| 9 | FAQ | Objection removal | Accordion; 5–10 questions |
| 10 | Final CTA | Second conversion chance | Full-width section; urgency elements |
| 11 | Footer | Trust + legal | Contact info, privacy policy, social links |

### Aesthetic Direction

Pick ONE direction and execute it consistently:

| Direction | Feel | Suits |
|-----------|------|-------|
| Minimalist | Clean whitespace, monochromatic | Premium SaaS, professional services |
| Bold/Maximalist | Rich layers, vivid colors | Creative agencies, consumer brands |
| Retro-Futuristic | Geometric, neon, monospace | Dev tools, gaming, tech startups |
| Organic | Soft shapes, earth tones | Wellness, food, sustainability |
| Editorial | Strong type hierarchy, asymmetric grids | Media, content platforms |

**Avoid**: purple gradients on white (overused AI aesthetic), perfectly symmetric layouts on every section, stock photos of people pointing at laptops, default yellow stars.

### Tech Stack (when building)

Next.js 14+ · TypeScript · Tailwind CSS · ShadCN UI

Build order: Design system → SEO metadata → Header → Hero (with animations) → Media → Benefits → Testimonials → FAQ → Final CTA → Footer.

See `references/component-examples.md` for production-ready ShadCN component implementations.

---

## 3. Creation Workflow

Follow this sequence for any landing page project:

**Step 1 — Define the Goal**
- Single conversion action (one CTA target)
- Audience segment this page serves
- Traffic source (ad, email, organic) — shapes tone and assumed context

**Step 2 — Structure First**
Use the full 11-element structure. Resist shortcutting: pages missing Social Proof or FAQ consistently underperform.

**Step 3 — Write Copy**
Apply the Copy Framework (§1). Write hero copy first — if the value prop isn't clear in 10 words, clarify the offer before continuing.

**Step 4 — Design**
Choose aesthetic direction, define design system (fonts, colors, motion), then build section by section.

**Step 5 — Optimize**
- Above the fold: value prop + CTA + one trust signal visible without scrolling
- Multiple CTAs with identical action (not competing goals)
- Minimal form fields; reduce every friction point
- Mobile-first; test on real devices
- Performance: LCP <2.5s, CLS <0.1, no layout shifts

**Step 6 — Launch Checklist**
- [ ] Headline is benefit-focused, specific, ≤10 words
- [ ] Single primary CTA throughout
- [ ] Social proof present and specific
- [ ] Mobile responsive
- [ ] Page loads <3s
- [ ] Trust signals visible above fold
- [ ] FAQ covers top 5 objections
- [ ] Analytics tracking configured

---

## References

- `references/11-essential-elements.md` — Detailed breakdown of each element with implementation guidance and good/bad examples
- `references/component-examples.md` — Production-ready ShadCN UI components for Hero, Benefits, Testimonials, FAQ, Final CTA, and Footer sections
