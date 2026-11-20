---
name: landing-page
description: Plans and builds a focused, responsive landing page for one audience and one primary action, covering section order, value proposition and headline, CTA hierarchy, above-the-fold content and Core Web Vitals. Use when asked to build a landing page, homepage, launch or waitlist page, rewrite a hero section, or fix a page that is not converting. Not for plan cards and comparison tables (use pricing-page).
---

# Landing Page

Produces a single-purpose landing page that tells one audience what the product does, why it matters to them, and what to do next, shipped as fast, responsive, accessible code.

## When to use
- "Build a landing page for my SaaS / app / course / waitlist."
- "Our homepage isn't converting" or "rewrite the hero section."
- A product launch, campaign, or feature announcement that needs its own page.
- Turning a feature list, pitch deck, or README into a structured marketing page.
- Reviewing an existing landing page for structure, message hierarchy, or speed.

## Workflow
1. Pin down the brief: one audience, one primary action (sign up, start trial, book demo, join waitlist), the core problem solved, and what real proof exists (customers, metrics, testimonials). Ask only if the audience or primary action is unknown; otherwise state assumptions and proceed.
2. Write the message before any layout: headline (outcome for that audience), subhead (how it works or what is different), primary CTA label, and one friction reducer if it is true ("No credit card required").
3. Outline sections in this default order and cut any without real content: hero (headline, subhead, primary CTA, product visual) → social proof → problem and benefits → how it works (3 steps) → features → objections and FAQ → final CTA.
4. Draft copy per section: benefits first, features as evidence, every claim verifiable. Use ux-writing for buttons and microcopy.
5. Wireframe mobile first at 375px, then desktop at 1280–1440px; confirm what is visible before scrolling on both.
6. Build with the project's tokens, or set them up with color-system and typography-system; use layout-spacing for section rhythm and responsive-design for breakpoints.
7. Optimize the LCP element, fonts, and JavaScript; test with Lighthouse or PageSpeed Insights on a throttled mobile profile.
8. Run the Final check and list every placeholder (logos, quotes, numbers) the owner must replace with real data.

## Rules
**Focus**
- One primary action per page: every primary-styled button points to it. Secondary actions (watch demo, read docs) use outline or text-link styling.
- The header holds the logo, at most 3–5 links, and the primary CTA. Paid-campaign pages may drop the nav links entirely.

**Hero and above the fold**
- At 375×667 and 1440×900, the headline, subhead, and primary CTA are visible without scrolling.
- One `h1`, roughly 10 words or fewer, wrapping to at most 3 lines on mobile.
- Headline formulas without hype: "[Outcome] for [audience]", "[Do the job] without [main pain]", "The [category] built for [specific audience]". No "revolutionary", "best-in-class", or "10x" unless measured and sourced.
- Show the real product (screenshot, short muted loop, or interactive demo) in or right after the hero; generic stock imagery explains nothing.

**CTAs**
- Labels are verb + object ("Start free trial", "Book a demo"), never "Submit" or "Click here".
- Repeat the primary CTA after the how-it-works or features section and again in the final section.
- Buttons are at least 44px tall, label contrast ≥4.5:1, and the button edge ≥3:1 against its background.

**Proof and readability**
- Use only real logos (with permission), testimonials with real name, role, and company, and numbers the owner can source. Flag placeholders as TODO.
- Body text ≥16px (18px is common on marketing pages), line length 45–75 characters, line-height 1.5–1.7.

**Performance**
- Targets at the 75th percentile: LCP ≤2.5s, INP ≤200ms, CLS ≤0.1.
- The LCP image is never lazy-loaded: `fetchpriority="high"`, explicit `width` and `height`, `srcset` and `sizes`, AVIF or WebP. Images below the fold get `loading="lazy"`.
- Fonts: at most 2 families, WOFF2, subsetted, `font-display: swap`; preload only the 1–2 files used above the fold.
- Background video is muted, has a poster image, and does not autoplay under `prefers-reduced-motion: reduce`.

## Output
- A brief block: audience, primary action, value proposition, assumptions.
- Complete page code: semantic HTML (`header`, `main`, labelled `section`s, `footer`) with CSS custom properties, or React + Tailwind if the project already uses it. No new dependencies unless asked.
- Final copy for every section; FAQ built with `details` and `summary` or an accessible disclosure.
- Head tags: `title`, meta description, Open Graph tags (use social-graphics for the share image).
- A list of placeholders and performance notes (LCP element, preloaded font files).

## Avoid
- Several competing primary CTAs (trial, demo, newsletter, download) with equal styling.
- Hero carousels; they split the message and hide most of it behind interaction.
- Headlines that could describe any product ("Unlock your potential").
- Fabricated metrics, testimonials, ratings, or customer logos.
- Fake urgency: countdowns that reset, invented scarcity.
- Text baked into images; hero animations or scripts that delay LCP.
- Endless feature grids with no benefit statements or visuals.

## Final check
- [ ] One audience and one primary action are named, and every primary CTA points to that action.
- [ ] Headline, subhead, and CTA are visible without scrolling at 375×667 and 1440×900.
- [ ] Single `h1`, logical heading order, skip link, meaningful `alt` text (or `alt=""` for decoration).
- [ ] Text contrast ≥4.5:1 (≥3:1 for large text); button and input boundaries ≥3:1.
- [ ] LCP image is not lazy-loaded and has dimensions and `fetchpriority`; fonts are WOFF2 with `font-display: swap`.
- [ ] No horizontal scrolling from 320px to 1920px wide.
- [ ] Every claim, number, and testimonial is real or clearly flagged as a placeholder.
