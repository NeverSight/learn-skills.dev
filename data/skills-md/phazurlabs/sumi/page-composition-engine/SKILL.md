---
name: page-composition-engine
description: "100+ full-page recipes giving exact block order, spacing rhythm, visual pacing, and content hierarchy for landing pages, dashboards, e-commerce, auth, settings, and profiles. Use when composing a whole page. For a single section in isolation, use layout-block-intelligence."
---

# Page Composition Engine — 100+ Full-Page Recipes

## The Art of Page Composition

A page is not a collection of random sections — it's a narrative. Every page tells a story through the deliberate sequencing of layout blocks. The composition engine provides complete recipes: which blocks to use, in what order, with what spacing rhythm, to achieve a specific goal.

"Every page is a conversation. The hero opens with a promise. The features deliver evidence. The testimonials provide social validation. The CTA asks for commitment." — This is not decoration; it's persuasion architecture.

## Page Archetypes

### Marketing Pages (External-Facing)
Pages designed to attract, inform, and convert visitors.
- Landing pages, product pages, pricing pages, about pages, case study pages

### Product Pages (Internal App)
Pages within the authenticated product experience.
- Dashboards, settings, profiles, lists, detail pages, create/edit pages

### Transactional Pages (Flow Steps)
Pages that are part of a multi-step process.
- Auth pages, checkout, onboarding, wizards

### Content Pages (Information)
Pages primarily delivering content.
- Blog posts, documentation, help center, changelog

## Composition Theory

### The Block Stacking Model

Every page follows a **narrative arc** through its blocks:

```
┌─────────────────────────┐
│   HOOK                  │  ← Hero: Capture attention
├─────────────────────────┤
│   CREDIBILITY           │  ← Logos/Social proof: Establish trust
├─────────────────────────┤
│   VALUE                 │  ← Features: Explain the offering
├─────────────────────────┤
│   EVIDENCE              │  ← Testimonials/Case studies: Prove it
├─────────────────────────┤
│   CONVERSION            │  ← Pricing/CTA: Ask for action
├─────────────────────────┤
│   OBJECTION HANDLING    │  ← FAQ: Remove doubts
├─────────────────────────┤
│   CLOSE                 │  ← Footer: Navigation + trust
└─────────────────────────┘
```

### Visual Rhythm

**Alternating density** prevents scroll fatigue:
- Dense block (feature grid) → Light block (CTA banner) → Dense block (testimonials) → Light block (stats)

**Background alternation** creates section separation:
- White → Gray-50 → White → Primary-950 (dark CTA) → White → Gray-50

### Spacing Between Blocks

| Context | Desktop | Mobile |
|---------|---------|--------|
| Default between blocks | 96-120px | 48-64px |
| Tight (related blocks) | 48-64px | 32-40px |
| Breathing room (after dense block) | 120-160px | 64-80px |
| Zero (blocks that visually connect) | 0px | 0px |

### Above-the-Fold Strategy

The first viewport (above the fold) must accomplish:
1. **What** — Clear heading explaining the product
2. **Why** — Subheading with the key benefit
3. **How** — Primary CTA button
4. **Trust** — Social proof element (logos, rating, user count)

Research shows content below the fold IS seen (80%+ of users scroll), but first-viewport quality determines IF they scroll.

### Content-to-Chrome Ratio

- Marketing pages: 90% content, 10% chrome (nav + footer)
- App pages: 75-85% content, 15-25% chrome (nav + sidebar + toolbars)
- Dashboards: 70-80% content, 20-30% chrome

## Landing Page Recipes

### LP-01: SaaS Product Landing Page
The workhorse B2B SaaS landing page.

```
1. NAV-01    Top bar (logo + links + "Get Started" CTA)
2. HERO-02   Split hero (headline left, product screenshot right)
3. PROOF-01  Customer logos bar ("Trusted by...")
4. FEAT-05   Alternating feature rows (3 features, zigzag layout)
5. STATS-01  4-column stats ("10K+ users", "99.9% uptime", etc.)
6. PROOF-03  Testimonial cards (3 customers)
7. FEAT-01   3-column icon+text grid (secondary features)
8. CTA-01    Simple CTA banner (heading + button)
9. PRICE-01  3-column pricing table
10. FAQ-01   Accordion FAQ
11. CTA-04   CTA with email input
12. FOOTER-03 4-column footer
```

**Background rhythm:** white → gray-50 → white → dark → white → gray-50 → white → dark → white → gray-50

### LP-02: Mobile App Landing Page
```
1. NAV-01    Top bar
2. HERO-12   App store hero (device mockup)
3. PROOF-01  Customer logos / press bar
4. FEAT-01   3-column feature grid (icon + text)
5. FEAT-06   Bento grid (screenshots in various sizes)
6. PROOF-04  Single large testimonial quote
7. STATS-01  4-column stats
8. PROOF-03  Testimonial cards
9. CTA-01    CTA with app store badges
10. FAQ-01   FAQ accordion
11. FOOTER-02 3-column footer
```

### LP-03: Startup / Coming Soon Page
```
1. NAV-01    Minimal top bar (logo + CTA only)
2. HERO-01   Centered text hero (bold headline + waitlist CTA)
3. PROOF-12  User count ("Join 5,000+ on the waitlist")
4. FEAT-01   3-column value props (icons + text)
5. TEAM-01   Team grid (founders)
6. FAQ-01    FAQ accordion
7. CTA-04    Email capture CTA
8. FOOTER-08 Minimal footer
```

### LP-04: Enterprise B2B Landing Page
```
1. NAV-02    Top bar with mega menu
2. HERO-02   Split hero (text + enterprise product screenshot)
3. PROOF-01  Customer logos bar (Fortune 500 logos)
4. PROOF-18  Trust badges (SOC2, HIPAA, GDPR)
5. FEAT-05   Alternating feature rows (4+ features)
6. PROOF-09  Case study snippets (3 case studies)
7. STATS-01  Impact metrics
8. FEAT-01   Integration/platform icons grid
9. PROOF-03  Enterprise testimonials
10. CTA-08   CTA with "Book a Demo" + "Contact Sales"
11. FAQ-01   FAQ accordion
12. FOOTER-04 5-column footer with compliance badges
```

### LP-05: E-commerce Product Landing Page
```
1. NAV-03    Top bar with search + cart
2. HERO-14   Product hero (product image + price + buy CTA)
3. PROOF-07  Star rating + review count
4. FEAT-01   3-column product benefits
5. CONTENT-06 Product image gallery
6. PROOF-08  Review cards (customer reviews)
7. FEAT-11   Comparison (this product vs. alternatives)
8. PROOF-15  Metric callouts ("1M+ sold")
9. CTA-01    Buy CTA banner
10. FAQ-01   Product FAQ
11. CONTENT-08 Related products grid
12. FOOTER-03 Footer with trust badges + payment icons
```

## App Page Recipes

### APP-01: Dashboard Home Page
```
1. NAV-06    Sidebar nav (persistent)
2. NAV-01    Top bar (search + user menu)
3. DASH-01   KPI card row (4 primary metrics)
4. DASH-04   Chart container (primary chart — line or area)
5. DASH-05   Chart container (secondary chart — bar)
6. DASH-09   Activity feed (recent events)
```

### APP-02: Settings Page
```
1. NAV-06    Sidebar nav (with "Settings" active)
2. NAV-11    Settings sub-navigation (General, Account, Billing, etc.)
3. FORM-06   Settings form (grouped sections with save buttons)
```

### APP-03: Profile Page
```
1. NAV-06    Sidebar nav
2. CONTENT-04 Profile header (avatar + name + bio + edit button)
3. STATS-04   Stats bar (posts, followers, etc.)
4. NAV-11    Profile tabs (Posts, Activity, About)
5. CONTENT-02 Content list (user's items)
```

### APP-04: List/Feed Page
```
1. NAV-06    Sidebar nav
2. NAV-01    Top bar
3. DASH-22   Filter bar (search + filters + sort + view toggle)
4. DASH-13   List view OR DASH-16 Grid view
5. DASH-25   Empty state (if no items)
```

### APP-05: Detail/Item Page
```
1. NAV-06    Sidebar nav
2. NAV-10    Breadcrumb bar
3. CONTENT-04 Item header (title + metadata + actions)
4. CONTENT-13 Tabbed content (Details, Activity, Comments)
5. FORM-06   Edit form (if editable)
```

## Auth Page Recipes

### AUTH-01: Login Page
```
1. Two-column layout:
   Left: Brand panel (logo + tagline + illustration)
   Right: FORM-03 Login form (email + password + social login + forgot password link)
```

### AUTH-02: Signup Page
```
1. Two-column layout:
   Left: Brand panel (logo + value props + social proof)
   Right: FORM-04 Signup form (name + email + password + terms checkbox)
```

### AUTH-03: Onboarding Flow (3-step)
```
Step 1: Profile setup (avatar + name + role)
Step 2: Preferences (team size + use case + integrations)
Step 3: Workspace setup (invite team + import data)
Each step: progress indicator + back/next buttons
```

## Responsive Composition Rules

### Desktop → Tablet
- 3-column grids → 2-column grids
- Sidebar nav → collapsible sidebar or top nav
- Side-by-side sections → stacked
- Section padding: reduce by 25%

### Tablet → Mobile
- 2-column grids → single column
- Horizontal nav → hamburger menu
- Side images → stacked above text
- Pricing tables → horizontal scroll or accordion
- Section padding: reduce by 50% from desktop
- Font sizes: reduce by 1-2 scale steps

### Block Reordering on Mobile
Some blocks reorder on mobile for thumb-reach and visual hierarchy:
- CTA button moves from inline to sticky bottom bar
- Social proof moves closer to hero (trust first)
- Navigation images/illustrations hide (content first)

## Routing

For **marketing pages** — seven complete recipes (SaaS landing, mobile app
landing, startup launch, enterprise B2B, e-commerce product, agency portfolio,
event) each with block order and rationale: read
`references/marketing-page-recipes.md`.

For **product pages** — nine recipes (dashboard home, settings, profile,
list/feed, detail, editor/canvas, chat, calendar, analytics): read
`references/app-page-recipes.md`.

For **the spacing that holds a page together** — the section spacing scale,
stacking rhythm rules, visual rhythm patterns, the responsive reduction formula,
container width strategy, grid systems, Z- and F-pattern layouts, and the rhythm
diagnostics for when a page feels wrong but you cannot say why: read
`references/spacing-rhythm-system.md`.

## Cross-References

- **layout-block-intelligence** — Individual block specs and variants
- **responsive-block-patterns** — Detailed breakpoint transformations
- **conversion-optimization-patterns** — Which compositions convert best
- **screen-flow-patterns** — Screen types that use these compositions
- **sector-style-intelligence** — Industry-specific page templates
