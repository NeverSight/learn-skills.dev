---
name: iblai-marketing-landing
description: Build a high-converting landing page for your app using a proven 12-section conversion framework.
globs:
alwaysApply: false
---

# /iblai-marketing-landing

Build a high-converting landing page for your app. Uses a proven 12-section
conversion framework based on 8,000+ pages and 4,000+ brands — not guesswork,
not trends, not "good design." Structure.

Follow [BRAND.md](https://raw.githubusercontent.com/iblai/vibe/refs/heads/main/BRAND.md) for
colors, typography, spacing, and the Apple-inspired design language.

**Component hierarchy** (always prefer in this order):
1. **ibl.ai components** (`@iblai/iblai-js`) — use SDK components first
2. **shadcn/ui** — use for everything else (`npx shadcn@latest add <component>`)
3. **shadcn-space blocks** — pre-built page sections (`npx shadcn@latest add @shadcn-space/<block>`)
4. **Custom components** — only as a last resort

Do NOT write custom components when an ibl.ai, shadcn, or shadcn-space
equivalent exists. Both ibl.ai and shadcn share the same Tailwind theme and
render in ibl.ai brand colors automatically.

You MUST run `/iblai-ops-test` before telling the user the work is ready.

After all work is complete, start a dev server (`pnpm dev`) so the user
can see the result at http://localhost:3000.

Use `pnpm` as the default package manager. Fall back to `npm` if pnpm
is not installed.

---

## The Framework

The page follows a psychological flow engineered to match how people think,
scroll, and decide:

```
Top    → Trust        (Hero, Proof bar, Transformation)
Middle → Belief       (Benefits, Features, Social proof, UGC)
Bottom → Decision     (Comparison, FAQ, Final CTA)
```

Every section exists for a reason. Skipping sections costs conversions.

---

## PHASE 1: DISCOVERY

Before building anything, understand what the landing page is selling.

### Step 1: Examine the Codebase

Read CLAUDE.md, README, any marketing copy, App Store metadata, and the
app's core features. Form a mental model of:

- **What the app does** (one sentence)
- **Who it's for** (target audience)
- **The core transformation** (before → after)
- **Key differentiators** (why this over alternatives)

### Step 2: Ask the User

Present what you've discovered and ask:

1. "What is the primary goal of this landing page?" (sign-ups, purchases, trials, waitlist)
2. "Who is the target visitor?" (persona, skill level, context)
3. "What are 3 outcomes your product delivers?"
4. "Do you have testimonials, reviews, or social proof to include?"
5. "Do you have a comparison point?" (competitor, old way of doing things)
6. "What's the primary CTA?" (start free trial, get started, buy now, join waitlist)

If the user skips questions, use sensible defaults derived from the codebase.

---

## PHASE 2: PAGE BLUEPRINT

Design the section-by-section flow. Present the blueprint to the user for
approval before writing any code.

### The 12 Sections

Every section is marked [REQUIRED], [RECOMMENDED], or [OPTIONAL].
Include all REQUIRED sections. Include RECOMMENDED unless the user
explicitly opts out. Include OPTIONAL when the content exists.

---

#### Section 1: HERO + PROOF BAR [REQUIRED]

![Hero + Proof Bar](https://raw.githubusercontent.com/iblai/vibe/refs/heads/main/skills/iblai-landing/pics/hero-proof-bar.png)
**This is where the page is won or lost. You have seconds.**

- **Headline** — Bold, transformation-focused. Not the product name. States the
  outcome the visitor wants. Max 10 words.
- **Subheadline** — One sentence expanding on the headline. Specific and
  credible.
- **Primary CTA** — Above the fold. Action-oriented text ("Start Free Trial",
  not "Submit"). Use the ibl.ai gradient button style.
- **Social proof bar** — Logos, review counts, trust badges, user count.
  Instant credibility. Do NOT wait until later to prove yourself.

**Layout:** Full-width hero section. Centered content, max-w-4xl. Headline
uses Display Hero typography (56px/600/1.07). CTA uses pill shape (980px
radius). Proof bar sits directly below the CTA as a row of logos/badges.

**Key principle:** Attention → Trust → Action. All above the fold.

---

#### Section 2: TRANSFORMATION [REQUIRED]
![The Transformation](https://raw.githubusercontent.com/iblai/vibe/refs/heads/main/skills/iblai-landing/pics/the-transformation.png)
**Right after the hero. Answers: "How easy is this going to be?"**

- Step 1 → Step 2 → Step 3
- Three steps maximum. Each has an icon, short title, and one-line description.
- The simpler it looks, the more people buy.
- If your process feels heavy, your conversion rate drops. Every time.

**Layout:** Three-column grid (stacks on mobile). Each step is a card with
a number badge, icon, title, and description. Use alternating
light/dark section backgrounds per BRAND.md.

---

#### Section 3: BENEFITS [REQUIRED]

![Benefits](https://raw.githubusercontent.com/iblai/vibe/refs/heads/main/skills/iblai-landing/pics/benefits.png)

**Deep, visual, outcome-led. Not features — outcomes.**

- 3-4 benefit blocks, each with:
  - Visual (image, screenshot, or graphic)
  - Headline (specific, measurable outcome)
  - Supporting proof (stat, testimonial snippet, or detail)
- Benefits alternate layout: image-left/text-right, then text-left/image-right.

**Bad:** "High quality materials"
**Good:** "Built to last 10+ years. Tested across 5,000+ uses."

Specificity = trust. Trust = conversion.

**Layout:** Alternating two-column sections. Images should be actual app
screenshots or product shots where possible.

---

#### Section 4: FEATURES [RECOMMENDED]


![Features](https://raw.githubusercontent.com/iblai/vibe/refs/heads/main/skills/iblai-landing/pics/features.png)

**The scan section. For people who won't read everything (most users).**

- Short features with icons and one-liners.
- 6-8 features in a 2x3 or 2x4 grid.
- Each feature: icon + title (3-5 words) + one sentence.
- Let visitors skim their way to conviction.

**Layout:** Grid layout. Use Lucide icons. Keep text minimal.

---

#### Section 5: MID-PAGE CTA + PROOF [REQUIRED]


![Mid-Page CTA + Proof](https://raw.githubusercontent.com/iblai/vibe/refs/heads/main/skills/iblai-landing/pics/mid-page-cta-proof.png)

**Most brands drop the ball here. They assume people scroll to the bottom.**

- Repeat the primary CTA mid-page.
- Add star ratings, review count, or trust signal alongside.
- Intent peaks at different points — meet visitors where they are.

**Layout:** Centered section with CTA button, star rating display, and
a one-line trust statement. Use the ibl.ai gradient background.

---

#### Section 6: WHAT'S INCLUDED [RECOMMENDED]

![What's Included](https://raw.githubusercontent.com/iblai/vibe/refs/heads/main/skills/iblai-landing/pics/whats-included.png)

**One of the highest-impact sections. One of the most ignored.**

- Removes uncertainty. Exactly what they get. No ambiguity.
- Checklist format: green checkmarks with clear item descriptions.
- When people are unsure → they don't buy. When it's crystal clear → they convert.

**Layout:** Two-column checklist or single column with check icons.
Can include a product image or mockup alongside.

---

#### Section 7: SOCIAL PROOF — LAYERED [REQUIRED]


![Social Proof - Layered](https://raw.githubusercontent.com/iblai/vibe/refs/heads/main/skills/iblai-landing/pics/social-proof-layered.png)

**Not just one testimonial block. Layered.**

- Written reviews with name, role, and photo/avatar
- Star ratings
- Video testimonials (if available — video proof consistently outperforms static
  because it's harder to fake and easier to believe)
- Mix formats: quote cards + star ratings + optional video thumbnails

**Layout:** Testimonial grid or carousel. Each card has avatar, name, role,
star rating, and quote text. Use Card component from shadcn.

---

#### Section 8: UGC / VIDEO CONTENT STRIP [OPTIONAL]

![UGC / Video Content Strip](https://raw.githubusercontent.com/iblai/vibe/refs/heads/main/skills/iblai-landing/pics/ugc-video-content-strip.png)

**Where attention spikes again. Builds belief + increases dwell time.**

- Scrolling content strip with thumbnails and play buttons.
- User-generated content, demo videos, or walkthrough clips.
- Longer time on page = higher likelihood to convert.

**Layout:** Horizontal scrolling strip. Thumbnail cards with play button
overlay. Only include if the user has video content.

---

#### Section 9: COMPARISON TABLE [RECOMMENDED]

![Comparison Table](https://raw.githubusercontent.com/iblai/vibe/refs/heads/main/skills/iblai-landing/pics/comparison-table.png)

**Where decisions get made. You vs alternatives. Side by side.**

- Clear ticks (green) and crosses (red). No fluff. Just clarity.
- "Why should I choose you?" — answered instantly.
- 4-6 comparison rows covering the most important differentiators.
- Most brands avoid this. The best brands lean into it.

**Layout:** Two-column comparison table. Product column highlighted.
Use the shadcn Table component. Green checkmarks vs red X marks.

---

#### Section 10: FAQ [REQUIRED]


![FAQ](https://raw.githubusercontent.com/iblai/vibe/refs/heads/main/skills/iblai-landing/pics/faq.png)

**Not filler. It's objection handling.**

- Every question is a doubt, a hesitation, a reason someone didn't buy.
- Cover: pricing, returns, compatibility, use case, data/privacy, support.
- 6-8 questions minimum.
- Handle it here or lose the sale.

**Layout:** Accordion component (shadcn Accordion). Full-width, centered
content. Questions should be phrased as the visitor would ask them.

---

#### Section 11: IMAGE STRIP / PRODUCT VISUALS [OPTIONAL]

![Image Strip / Product Visuals](https://raw.githubusercontent.com/iblai/vibe/refs/heads/main/skills/iblai-landing/pics/image-strip-product-visuals.png)

**Right before the close: more visuals, more context, more immersion.**

- Different angles, lifestyle shots, in-use moments.
- Reinforces desire at the perfect moment.
- People need to see what they're buying.

**Layout:** Full-width image grid or horizontal scroll strip.

---

#### Section 12: FINAL CTA — EMOTIVE CLOSE [REQUIRED]


![Final CTA - Emotive Close](https://raw.githubusercontent.com/iblai/vibe/refs/heads/main/skills/iblai-landing/pics/final-cta-emotive-close.png)

**The last push. Must feel different from the mid-page CTA.**

- Emotive headline — speaks to the transformation, not the product.
- Clear CTA button (same action as hero, different emotional framing).
- Trust badges underneath: guarantees, payment icons, security badges.
- Everything here reduces hesitation and increases action.

**Layout:** Full-width section with dark or gradient background. Centered
headline (Section Heading typography), CTA button, and a row of trust
badges/icons below.

---

### Step 3: Present the Blueprint

Present the complete section sequence as a numbered list showing:
- Section number and name
- Specific headline/content for THIS product
- Which optional sections are included and why
- Which optional sections are skipped and why

Ask the user to confirm, reorder, add, or remove sections before proceeding.

---

## PHASE 3: CONTENT

For each section in the approved blueprint, draft:

- **Headline** (bold, short, transformation-focused)
- **Subheadline** (if needed)
- **Body copy** (specific, credible, no filler)
- **CTA text** (action-oriented)
- **Social proof copy** (stats, testimonials, badges)

### Content Principles

- Write like a human, not a marketer. Short sentences. No jargon.
- Every headline should pass the "would I say this to a friend?" test.
- Stats should feel specific and credible — round numbers feel fabricated
  (83% > 80%, 4,847 users > "thousands").
- CTAs should describe what happens next: "Start my free trial" not "Submit".
- Benefits lead with the USER's outcome, not the product's features.
- Specificity = trust. Trust = conversion.

Present content section-by-section. Get approval before implementation.

---

## PHASE 4: IMPLEMENTATION

### Step 1: Set Up the Page

Create the landing page at `app/(landing)/page.tsx` (or `app/page.tsx` if the
user wants it as the home page). Use a route group so the landing page can have
its own layout without the app's auth providers.

```
app/
├── (landing)/
│   ├── layout.tsx      ← Minimal layout (no auth, no sidebar)
│   └── page.tsx        ← The landing page
└── (app)/
    ├── layout.tsx      ← App layout with providers
    └── ...
```

### Step 2: Install Components

Add shadcn components needed for the landing page:

```bash
npx shadcn@latest add button card accordion table badge separator
```

Check if shadcn-space has relevant blocks before building from scratch:

```bash
npx shadcn@latest add @shadcn-space/hero-1
npx shadcn@latest add @shadcn-space/features-1
npx shadcn@latest add @shadcn-space/testimonials-1
npx shadcn@latest add @shadcn-space/faq-1
npx shadcn@latest add @shadcn-space/cta-1
```

Adapt shadcn-space blocks to match the approved content. Do NOT use them
as-is if they don't fit the framework structure.

### Step 3: Build Section by Section

Build each section as a separate component in `components/landing/`:

```
components/landing/
├── hero.tsx
├── transformation.tsx
├── benefits.tsx
├── features.tsx
├── mid-cta.tsx
├── whats-included.tsx
├── social-proof.tsx
├── ugc-strip.tsx           (if included)
├── comparison.tsx          (if included)
├── faq.tsx
├── image-strip.tsx         (if included)
└── final-cta.tsx
```

Each component should be self-contained with its own content. The page
file assembles them in order.

### Implementation Guidelines

**Typography:** Follow BRAND.md Apple-inspired hierarchy:
- Hero headline: 56px, weight 600, line-height 1.07, letter-spacing -0.28px
- Section headings: 40px, weight 600, line-height 1.10
- Body: 17px, weight 400, line-height 1.47, letter-spacing -0.374px

**Layout:**
- Full-width sections with max-w-5xl centered content
- Alternating light (`#f5f5f7`) / white (`#ffffff`) section backgrounds
- Generous vertical padding: py-20 to py-32 between sections
- Each section near full-viewport height where appropriate

**CTA Buttons:**
- Primary: ibl.ai gradient (`bg-gradient-to-r from-[#2563EB] to-[#93C5FD] text-white`)
- Pill shape on hero CTA (rounded-full)
- Minimum 44x44px touch target

**Responsive:**
- Hero headline: 56px → 40px → 28px on mobile
- Grids: 3-col → 2-col → 1-col
- Touch targets: minimum 44x44px
- Test at 360px, 768px, and 1440px widths

**Animations (subtle only):**
- Fade-in on scroll for each section (use Intersection Observer or
  `framer-motion` if already in the project)
- No heavy animations, parallax, or scroll-jacking
- Animations must not block content visibility

### Step 4: Add Navigation

Add a minimal sticky navigation bar at the top:
- Logo (left) — use ibl.ai logo or the app's logo
- Navigation links (center) — anchor links to key sections
- CTA button (right) — same as hero CTA
- Glass blur effect per BRAND.md: `backdrop-filter: saturate(180%) blur(20px)`
  on `rgba(255,255,255,0.8)` (light) or `rgba(0,0,0,0.8)` (dark)

### Step 5: Add Footer

Minimal footer with:
- Logo
- Navigation links
- Legal links (privacy policy, terms of use)
- "Powered by ibl.ai" credit (if appropriate)

### Step 6: Verify

Run `/iblai-ops-test` before telling the user the work is ready:

1. `pnpm build` — must pass with zero errors
2. `pnpm dev` — start dev server
3. Visual check at mobile (360px), tablet (768px), and desktop (1440px)
4. Every CTA must be clickable and link to the correct action
5. All images must load (no broken images)
6. Page must scroll smoothly through all sections

---

## IMPORTANT GUIDELINES

### The Psychology

This isn't random. The exact flow is engineered to match how people scroll:
- **Top → Trust** — Hero proves you're worth their time. Transformation shows
  it's easy. Benefits show it works.
- **Middle → Belief** — Features let skimmers catch up. Mid-page CTA catches
  peak intent. Social proof removes doubt.
- **Bottom → Decision** — Comparison eliminates alternatives. FAQ removes
  objections. Final CTA makes the ask with emotional weight.

### What NOT to Do

Conversion doesn't come from:
- Colors, fonts, or animations
- Clever wordplay or puns in headlines
- Stock photos of people shaking hands
- Generic copy ("We're passionate about...")
- Hiding the CTA until the bottom

Conversion comes from:
- What you say (specific, credible, outcome-focused)
- Where you say it (the right section in the right order)
- When you say it (meeting intent where it peaks)

### Content Quality

- Every headline must be specific to THIS product. No generic templates.
- Every stat must be real or clearly marked as a target/placeholder.
- Every testimonial must feel authentic (real name, real role, specific detail).
- If content doesn't exist yet, mark sections with `{/* TODO: Replace with real content */}`
  and use realistic placeholder content, not lorem ipsum.

### Performance

- Images: Use Next.js `<Image>` with proper `width`/`height` and lazy loading.
- Fonts: System sans-serif stack only (no custom font downloads).
- No heavy JS libraries for visual effects.
- Target Lighthouse performance score > 90.

**Brand guidelines**: [BRAND.md](https://raw.githubusercontent.com/iblai/vibe/refs/heads/main/BRAND.md)
