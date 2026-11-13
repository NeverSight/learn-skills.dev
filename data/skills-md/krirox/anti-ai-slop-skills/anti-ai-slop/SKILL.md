---
name: anti-ai-slop
description: Detect and eliminate "AI slop" aesthetics in websites, web apps, landing pages, dashboards, components, and any frontend UI Claude generates or reviews. Use this skill BEFORE writing any HTML, CSS, React, Tailwind, or frontend code, AND when the user asks to review, audit, redesign, "de-slop," critique, fix, or improve a website/app/UI/landing page/component for being generic, AI-generated, soulless, templated, or "looking AI-made." Trigger on phrases like "make this not look AI", "remove the AI feel", "looks like ChatGPT made it", "v0 vibes", "looks like every SaaS site", "Tailwind default look", "feels generic", "review my landing page", "build a landing page", "design a hero section", "make a dashboard", "build a SaaS site", or any frontend build/critique request. This skill is mandatory for all frontend output to prevent distributional convergence on the purple-gradient/glassmorphism/rounded-card mean.
---

# Anti-AI-Slop Skill

## What "AI slop" actually is

AI slop in UI is **distributional convergence**: models trained on millions of "modern SaaS" sites collapse to the statistical average — purple gradients, rounded-2xl cards, Inter at 64px, three-feature grids. The output is technically polished but has no opinion, no friction, no specificity. Real products have weird corners that betray actual users. AI output is smooth because it's averaged.

The job of this skill is to **resist the average**. Every default the model wants to reach for is suspect.

---

## The 4 root causes (memorize these)

Every slop tell traces back to one of these:

1. **No hierarchy** — everything is the same weight, so nothing leads the eye
2. **No specificity** — generic copy, generic visuals, no concrete numbers or named entities
3. **No restraint** — gradients + glassmorphism + neon + emoji + 3D + animation, all at once
4. **No opinion** — the design could belong to any company; no aesthetic risk taken

If a fix doesn't address one of these four, it's cosmetic.

---

## The slop checklist (use BEFORE writing any frontend)

Before generating any UI code, run this checklist mentally and consciously violate the defaults:

### Visual defaults to refuse
- [ ] Purple-to-blue / indigo-to-violet gradient anywhere
- [ ] Glassmorphism (frosted card on gradient blob)
- [ ] `rounded-2xl` on every element
- [ ] Tailwind defaults untouched (`slate-900`, `indigo-500`, `emerald-400`, `from-purple-500 to-blue-500`)
- [ ] Inter / Geist / Roboto as the only font choice
- [ ] Centered hero: huge headline + subtitle + two buttons (primary gradient, secondary outline)
- [ ] Stock 3D blob shapes, isometric illustrations, or generated abstract art
- [ ] Lucide/Heroicons used identically with no custom touch
- [ ] Emoji as section icons (🚀 ⚡ 🎯)
- [ ] Drop shadow + scale-105 as the only hover state
- [ ] Same fade-up animation on every element on scroll

### Copy defaults to refuse
- [ ] "Transform your workflow with AI-powered..."
- [ ] "Seamlessly", "Unlock", "Revolutionize", "Empower", "Elevate", "Effortlessly", "Delve", "Unleash"
- [ ] Parallel-structure feature triplets ("Build faster. Ship smarter. Scale further.")
- [ ] "In the fast-paced digital landscape..."
- [ ] Vague benefits with zero numbers, zero named users, zero specifics
- [ ] Em-dashes used as rhetorical pauses (the ChatGPT signature)
- [ ] Walls of perfectly grammatical, soulless paragraphs

### Structural defaults to refuse
- [ ] Standard SaaS skeleton: nav → hero → 3-feature grid → testimonials → pricing → CTA → footer
- [ ] Fake testimonials with stock avatars and similar phrasing
- [ ] "Trusted by" logo strip with placeholder logos
- [ ] Free / Pro / Enterprise pricing with the middle tier highlighted
- [ ] FAQ accordion with questions no one asked
- [ ] Floating chatbot bubble in the bottom right

### State/interaction defaults to refuse
- [ ] Only the happy path renders — no empty states, error states, loading skeletons
- [ ] Generic spinner instead of skeleton screen or contextual feedback
- [ ] Buttons labeled "Submit" / "Click here" / "Learn more"
- [ ] Forms with no validation feedback
- [ ] Dashboards with fake "real-time" data and no empty/zero state

### Motion & Interaction Slop
- [ ] Generic `transition-all duration-300` on every hover state
- [ ] Meaningless staggered fade-ups on scroll

### Asset, Data & Code Slop
- [ ] Using "Lorem Ipsum" or generic placeholder text
- [ ] Generic Unsplash photos (e.g., people pointing at laptops)
- [ ] Perfectly symmetrical 8-point grid layouts everywhere (`p-4`, `gap-8`)
- [ ] Massive inline Tailwind strings and generic component names (`FeatureCardItem`)

If 3+ of these slip into a draft, it's slop. Restart with deliberate violations.

---

## The deliberate-violation playbook

For each slop default, there's a non-slop move. Pick one or more per project and commit hard.

| Slop default | Deliberate violation |
|---|---|
| Purple/blue gradient | Single flat color with one accent (e.g., off-white + ink black + one ugly-on-purpose color: mustard, oxblood, neon green) |
| Rounded-2xl everywhere | Sharp corners (0px radius) OR mixed radii with intent (pill buttons + square cards) |
| Inter / Geist | Editorial serif (Tiempos, GT Sectra), monospace body (JetBrains Mono, IBM Plex Mono), or weird display face for headings only |
| Centered hero with two buttons | Asymmetric layout, off-grid placement, headline that runs off the edge, single CTA, or no hero at all |
| 3D blobs / abstract shapes | Real screenshots of the product, hand-drawn marks, photographs, charts of real numbers, raw text |
| Lucide icons | Custom inline SVGs, dingbats, no icons at all, or text labels only |
| Drop-shadow hover | Border thickening, color inversion, marginal offset (translate by 2-4px), background swap |
| Fade-up scroll animation | No scroll animation, OR a single weird intentional one (e.g., text reveal, marquee, a pinned scroll moment) |
| Vague benefit copy | Concrete numbers, named customers, specific use cases, dated claims ("Used by 1,247 teams since March") |
| Three-feature grid | Long-form prose, a single big screenshot with annotations, a comparison table, or a manifesto |
| Free/Pro/Enterprise | Honest single price, usage-based with calculator, "pay what you want," or a manifesto-style pricing page |
| Soulless ChatGPT prose | First-person voice, contractions, opinions, jokes, dated references, the founder's name |
| Motion/transition slop | Instantaneous cuts (0ms), spring physics, or cinematic slow reveals; no `transition-all` |
| Asset/placeholder slop | Highly specific mock data (e.g., "Sarah Jenkins - Logistics"), CSS patterns, or ASCII art |
| Symmetrical grid slop | Break the 8-pt grid: massive typographic scale contrast, asymmetrical padding |
| Generic code architecture | Semantic HTML, hyper-specific component names (`OverdueInvoiceWarning` instead of `AlertBox`) |

---

## Aesthetic directions (pick one, don't blend)

Slop happens when you blend everything. Premium happens when you commit. Pick ONE direction per project:

- **Brutalist** — system fonts, 1-2px hard borders, no shadows, raw HTML feel, high contrast, ugly-on-purpose
- **Editorial / magazine** — serif headlines, generous line-height, asymmetric grid, body text as a real column, actual paragraphs
- **Swiss / functional** — Helvetica or Inter, strict grid, hairline rules, lots of negative space, one accent color, no rounded corners
- **Terminal / monospace** — full mono stack, ASCII art, command-line aesthetic, green-on-black or amber-on-black optional
- **Maximalist / Y2K** — clashing colors, layered images, marquees, deliberate visual noise, 2003 web energy
- **Photographic / product-first** — large product photos or screenshots dominate, type plays a supporting role
- **Documentary / data-dense** — tables, footnotes, citations, dates, source links — looks like a research report

Whichever you pick: **commit at every level** (color, type, spacing, motion, copy, structure). Mixing brutalist hero + glassmorphic features + Y2K footer = slop.

---

## Copy rules (this is half the battle)

Visual slop is easy to spot. Copy slop is what gives it away even when the design is clean.

**Banned phrases** (instant slop tell):
- "Seamlessly," "effortlessly," "seamless integration"
- "Unlock the power of," "unleash your potential"
- "Revolutionize," "transform," "elevate," "empower"
- "In the fast-paced [anything]"
- "Whether you're a [X] or a [Y]..."
- "Take your [X] to the next level"
- "The future of [X] is here"
- Any sentence with three em-dashes
- Parallel triplets: "Faster. Smarter. Better."

**Replace with**:
- Specific numbers: "Cuts onboarding from 6 weeks to 3 days for the 47 ops teams using it"
- Named subjects: who uses it, who built it, what they did before
- Concrete verbs: "imports," "exports," "splits," "merges," "queues" — not "leverages," "facilitates," "enables"
- Opinions: "We think Jira is a productivity tax. This isn't that."
- Dated claims: "As of March 2026..." beats vague present-tense claims

**Voice test**: read the copy aloud. If it sounds like a press release or a LinkedIn post, it's slop. If it sounds like a person who has actually used the thing speaking to a friend, it's not.

---

## State coverage (the fastest non-slop signal)

AI slop only renders the happy path. Real apps live in their states. When building a UI, always include:

1. **Empty state** — what shows before any data exists. Specific, opinionated, useful. Not "No items yet ✨"
2. **Loading state** — skeleton screens, not spinners. Match the layout of the loaded state.
3. **Error state** — actual error copy that explains what happened and what to do next. Not "Something went wrong."
4. **Edge state** — one item, 1000 items, very long names, missing fields, offline, partial permissions
5. **Zero state vs empty state** — first-time-ever-user gets different copy than "you cleared your inbox"

Including 2-3 of these instantly removes the slop signal even if the rest of the design is templated.

---

## When reviewing existing UI for slop

Use this scoring rubric on a screenshot, URL, or code:

**Score each 0-3 (0 = clean, 3 = pure slop):**

1. Visual signature — gradients, glassmorphism, rounded everything, default Tailwind palette
2. Typography — single Inter/Geist font, no hierarchy, walls of body text
3. Hero pattern — centered headline, two buttons, vague subtitle
4. Feature blocks — three-card grid with parallel headlines and emoji icons
5. Copy register — buzzwords, no numbers, no named entities, em-dash overuse
6. Structural skeleton — generic SaaS page anatomy in default order
7. Social proof — fake testimonials, placeholder logos, no real evidence
8. State coverage — only happy path, generic spinners, "Submit" buttons
9. Specificity — would this design fit any company in any industry?
10. Aesthetic commitment — clear direction, or a blend of trends?

**Total**: 0-7 = strong; 8-15 = workable; 16-23 = slop; 24-30 = pure AI slop.

Report the score, name the top 3 worst offenders, give the user one deliberate-violation move per offender. Don't dump the whole list — pick the highest-leverage fixes.

---

## Output format when generating UI

When Claude is generating frontend code as part of a request, **before writing any code**:

1. State the aesthetic direction in one line ("Going editorial: serif headlines, monospace body, single oxblood accent.")
2. State the 2-3 deliberate violations being made ("No gradients. No rounded corners. No three-feature grid — using a single annotated screenshot instead.")
3. Then write the code

This forces commitment. It also lets the user redirect before 200 lines of slop get generated.

---

## When reviewing UI for slop

Format the response as:

1. **Slop score: X/30**
2. **Top 3 offenders** — name the specific tell, not vague "feels generic"
3. **One fix per offender** — concrete, copy-pasteable, from the deliberate-violation playbook
4. **One question** — what aesthetic direction is the user actually going for? (Answers everything else.)

Don't list all 30 things wrong. Pick the highest leverage. The user can ask for more.

---

## The meta-rule

Every default the model wants to reach for is suspect. The "obvious" choice (gradient hero, three feature cards, Lucide icons, Inter font, rounded-2xl) is obvious **because the training data is full of it**. That's the definition of slop.

Before shipping any frontend output, ask: **"What did I do here that another AI wouldn't have done by default?"** If the answer is nothing, restart.
