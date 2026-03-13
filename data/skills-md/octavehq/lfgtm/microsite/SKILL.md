---
name: microsite
description: Personalized ABM microsite builder that generates self-contained HTML landing pages using GTM intelligence. Use when user says "microsite for [company]", "personalized landing page", "ABM page", or asks for a personalized web page for a target account.
---

# /octave:microsite - Personalized ABM Microsite Builder

Generate personalized, single-page ABM microsites as beautiful self-contained HTML, powered by your Octave GTM knowledge base. Instead of "Hey, want to see a demo?" you send "We built something for you" with a link. The microsite shows effort, personalization, and immediately demonstrates you understand their business.

**Why microsites work:** They flip the cold outreach dynamic. A personalized landing page — "Built for [Company]" — is a pattern interrupt. It proves you researched the account, tailored your message, and invested time before asking for theirs.

**How this differs from other skills:**
- vs `/octave:one-pager` — one-pager is a post-meeting leave-behind; microsite is a pre-meeting attention grabber for outreach
- vs `/octave:proposal` — proposal is formal and detailed; microsite is concise and designed to generate interest
- vs `/octave:deck` — deck is for presenting; microsite is for sharing a link

## Usage

```
/octave:microsite <target> [--angle <approach>] [--style <preset>]
```

## Examples

```
/octave:microsite acme.com                                    # Personalized microsite for Acme
/octave:microsite acme.com --angle competitive                # Competitive angle (they use rival)
/octave:microsite jane@acme.com --angle pain-point            # Person-specific, pain-led
/octave:microsite "enterprise healthcare companies"           # Segment-level microsite template
/octave:microsite acme.com --style octave-brand               # Specific style preset
/octave:microsite acme.com --angle trigger                    # Trigger-based (recent news/event)
```

## Instructions

When the user runs `/octave:microsite`:

### Step 1: Understand the Context

If not provided via flags, ask the user interactively:

**Target — "Who is this for?"**

```
Who is this microsite for?

Provide any of the following:
- Company domain (e.g., acme.com)
- Person email (e.g., jane@acme.com)
- Segment description (e.g., "enterprise healthcare companies")

Target:
```

**Angle — "What approach should this take?"**

```
What angle should the microsite lead with?

1. Pain-point led — address a specific challenge they face
2. Competitive displacement — show a better way than their current approach
3. Value-led — lead with results and metrics from similar companies
4. Trigger-based — connect to a recent event, news, or milestone
5. Industry-specific — demonstrate deep expertise in their vertical

Your choice:
```

**Call to Action — "What should they do next?"**

```
What action should the microsite drive?

1. Book a demo
2. See a case study
3. Watch a video / product tour
4. Start a free trial
5. Reply to an email / start a conversation
6. Custom (describe it)

Your choice:
```

**Brand — "Use your company's brand styling?"**

```
Should the microsite use your company's brand?

1. Yes — extract from my website (provide URL)
2. Yes — I'll provide brand assets (colors, fonts, logo)
3. No — I'll pick from style presets
4. Use Octave brand styling

Your choice:
```

### Step 2: Octave Context Gathering

Based on the target, angle, and CTA, use Octave MCP tools to build deep personalization context. **Always tell the user what you're researching and why.**

**Call as many tools as needed.** The more you know about the account, the more personalized the microsite. A great microsite layers company enrichment + playbook messaging + proof points + competitive intel into a narrative that feels hand-crafted. Don't stop at one tool when four would give you a stronger page.

**List vs Search — when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all our proof points" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full proof point details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question — "how do we help healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, uploaded assets, or source docs |

---

#### For All Microsites (Always Run)

Start with enrichment and qualification — this drives the personalization that makes microsites work:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Always — industry, size, tech stack, signals power the entire page |
| ICP fit scoring | `qualify_company({ companyDomain })` | Always — matched segment determines which playbook to pull |
| Matching playbook | `search_knowledge_base({ query: "<industry> <persona>", entityTypes: ["playbook"] })` | Always — messaging, value props, and positioning for their segment |
| Playbook + value props | `get_playbook({ oId, includeValueProps: true })` | After finding the best-fit playbook — drives the solution section |
| Brand voice | `list_brand_voices()` | Always — consistent tone across the microsite |

---

#### For Person-Specific Microsites

When the target is an email address or named contact:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | When a specific person is the target — role, background, priorities |
| Person qualification | `qualify_person({ person: { ... } })` | When you need persona match for messaging precision |
| Find related contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When you want to identify other stakeholders who might see the page |

---

#### For Social Proof & Credibility

The proof section is what turns a microsite from marketing fluff into a compelling story:

| What you need | Tool | When to use |
|---------------|------|-------------|
| All proof points | `list_entities({ entityType: "proof_point" })` | Fetch proof points with full data — metrics, quotes, logos |
| All references | `list_entities({ entityType: "reference" })` | Customer references in their industry |
| Proof by topic | `search_knowledge_base({ query: "<industry> results", entityTypes: ["proof_point", "reference"] })` | When you need proof points about a specific topic or industry |
| Uploaded case studies | `search_resources({ query: "<industry> case study" })` | When the workspace has uploaded case study docs or assets |

---

#### For Competitive Angle

When the angle is competitive displacement:

| What you need | Tool | When to use |
|---------------|------|-------------|
| All competitors | `list_all_entities({ entityType: "competitor" })` | Quick scan of competitive landscape |
| Competitor details | `get_entity({ oId })` | Deep dive on the specific competitor they likely use |
| Competitive positioning | `search_knowledge_base({ query: "<competitor> differentiation", entityTypes: ["playbook", "competitor"] })` | Messaging angles for competitive deals |
| Competitive wins | `list_findings({ query: "<competitor>" })` | Real conversation intel about competitive situations |

---

#### For Trigger-Based Angle

When the angle is tied to a recent event or news:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Recent intel | `list_findings({ query: "<company>", startDate: "<90 days ago>" })` | Conversation-based insights and signals |
| Events | `list_events({ filters: { accounts: ["<account_oId>"] } })` | Deal events, meetings, interactions |
| Event details | `get_event_detail({ eventOId })` | Deep dive on a specific trigger event |

---

#### Additional Context

| What you need | Tool | When to use |
|---------------|------|-------------|
| Products | `list_all_entities({ entityType: "product" })` | When you need product capabilities for the solution section |
| Use cases | `list_all_entities({ entityType: "use_case" })` | When you want to show relevant use cases |
| Synthesized prep | `generate_call_prep({ companyDomain })` | When you want a comprehensive brief to work from |

---

**Output of this step:** Present a content outline to the user for approval:

```
MICROSITE OUTLINE: Built for [Company]
=======================================

Target: [Company name / Person name]
Angle: [Pain-point / Competitive / Value-led / Trigger-based]
CTA: [Book a demo / See case study / etc.]
Sections: [4-5 sections]

---

SECTION OUTLINE
---------------

1. HERO
   Headline: "[Built for Company] — [hook based on angle]"
   Subhead: "[One-sentence value statement]"

2. [SECTION 2 NAME]
   • [Key point grounded in research]
   • [Key point grounded in research]
   • [Key point grounded in research]

3. [SECTION 3 NAME]
   • [Content informed by playbook/value props]
   • [Content informed by playbook/value props]
   • [Content informed by playbook/value props]

4. [SECTION 4 NAME]
   • [Proof point 1 — metric, company, quote]
   • [Proof point 2 — metric, company, quote]
   • [Proof point 3 — metric, company, quote]

5. CTA
   Headline: "[Action-oriented ask]"
   Button: "[CTA text]"

---

Octave Sources Used:
• Company profile: [Company name] — [key insights used]
• Playbook: [Playbook name] — [messaging angle]
• Proof points: [N] references pulled from [industries]
• Competitive intel: [If applicable]
• Person profile: [If applicable]

---

Does this outline look good? I can:
1. Proceed to style selection and generation
2. Change the angle or messaging
3. Add or remove sections
4. Adjust the CTA
```

**Wait for user approval before proceeding.**

### Step 3: Style & Brand

Two layers of brand apply to microsites:
1. **Your brand** (the sender's brand) — logo, colors, fonts. This is what the microsite is styled with.
2. **Their context** (the recipient's company) — the personalization that shows you researched them. This appears as content, not styling.

**If user chose brand extraction in Step 1:**

Use the same tiered brand extraction approach as the deck skill:

1. **Tier 1: browser-use** (best quality) — open the website, screenshot, extract computed styles (colors, fonts, logos) via JS eval, confirm with user
2. **Tier 2: WebFetch** (fallback) — fetch homepage HTML/CSS, parse CSS custom properties, font-family declarations, logo URLs, and meta theme-color
3. **Tier 3: Manual** (if neither works) — ask user to provide hex colors, font names, and logo files directly

**If user chose a style preset:**

Reference the deck skill's [STYLE_PRESETS.md](../deck/STYLE_PRESETS.md). Use the same CSS variable system. Recommended defaults for microsites:

| Angle | Recommended Preset |
|-------|--------------------|
| Pain-point led | `midnight-pro` |
| Competitive displacement | `neon-pulse` |
| Value-led | `executive-dark` |
| Trigger-based | `aurora-gradient` |
| Industry-specific | `soft-light` |

Tell the user what you picked and why. Let them override.

### Step 4: Generate HTML

Build a single, self-contained HTML file. A microsite is a single scrolling page — visually striking, mobile-responsive, and heavily personalized.

#### Output Directory

Every microsite gets its own folder under `.octave-microsites/`:

```
.octave-microsites/
└── <kebab-case-company>-<YYYY-MM-DD>/
    └── <company>-microsite.html
```

Example: `/octave:microsite acme.com` produces `.octave-microsites/acme-2026-02-11/acme-microsite.html`

The entire `.octave-microsites/` directory is in `.gitignore` — nothing here gets committed.

#### Page Sections by Angle

**Pain-Point Led:**

1. **Hero** — "Built for [Company]" + "[Company], here's how [industry] leaders are solving [pain point]"
2. **The Challenge** — their specific pain, grounded in industry context and company signals
3. **The Solution** — 3 capabilities mapped to their pain points (card layout)
4. **Social Proof** — 2-3 relevant proof points (metrics, logos, quotes) from their industry
5. **CTA** — "See how this works for [Company]" + button

**Competitive Displacement:**

1. **Hero** — "Built for [Company]" + "There's a better way than [current approach]"
2. **The Gap** — what their current solution likely cannot do (without naming competitor directly)
3. **What's Possible** — vision of what better looks like, with metrics from switchers
4. **Who's Moved** — proof points from companies who switched, similar industry/size
5. **CTA** — "See the difference" + button

**Value-Led:**

1. **Hero** — "Built for [Company]" + "[Industry] companies see [metric] with [your product]"
2. **Why [Company]** — personalized fit: their signals + your value props
3. **Results** — 3 big numbers from relevant case studies
4. **How It Works** — 3-step simple process
5. **CTA** — "Get your custom demo" + button

**Trigger-Based:**

1. **Hero** — "Built for [Company]" + "[Congratulations on / Given recent...]"
2. **The Opportunity** — connecting their trigger event to your value
3. **Relevant Results** — proof from similar situations
4. **CTA** — timely, specific ask

#### HTML Architecture

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Built for [Company] | [Your Company]</title>
  <!-- Google Fonts (preconnect + stylesheet) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from chosen preset — same system as deck) === */
    :root { ... }

    /* === Reset & Base === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: var(--font-body);
      background: var(--bg);
      color: var(--text-primary);
      line-height: 1.6;
    }

    /* === Layout === */
    .section {
      width: 100%;
      padding: clamp(3rem, 8vh, 6rem) clamp(1.5rem, 5vw, 3rem);
    }
    .section-inner {
      max-width: 800px;
      margin: 0 auto;
    }
    .hero {
      min-height: 100vh;
      min-height: 100dvh;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      position: relative;
    }

    /* === Typography (all clamp-based) === */
    .heading-1 { font-size: clamp(2.2rem, 5.5vw, 4rem); font-family: var(--font-display); }
    .heading-2 { font-size: clamp(1.6rem, 3.5vw, 2.5rem); font-family: var(--font-display); }
    .heading-3 { font-size: clamp(1.1rem, 2vw, 1.4rem); font-family: var(--font-display); }
    .body-text { font-size: clamp(0.95rem, 1.4vw, 1.1rem); }
    .body-lg { font-size: clamp(1.05rem, 1.8vw, 1.3rem); }

    /* === Components (cards, metrics, proof blocks) === */
    /* === Scroll-triggered animations === */
    /* === Mobile responsive === */
    /* === prefers-reduced-motion === */
  </style>
</head>
<body>

  <!-- Hero: full viewport, gradient background, "Built for [Company]" -->
  <section class="section hero" id="hero">
    <div class="bg-gradient"></div>
    <div class="section-inner">
      <span class="built-for animate-in">Built for [Company]</span>
      <h1 class="heading-1 animate-in">[Headline based on angle]</h1>
      <p class="body-lg text-secondary animate-in">[Subhead]</p>
    </div>
  </section>

  <!-- Section 2-4: Content sections based on angle -->
  <section class="section" id="[section-id]">
    <div class="section-inner">
      <!-- Section content -->
    </div>
  </section>

  <!-- CTA: final section with clear action -->
  <section class="section hero" id="cta">
    <div class="section-inner">
      <h2 class="heading-1 animate-in">[CTA headline]</h2>
      <p class="body-lg text-secondary animate-in">[Supporting line]</p>
      <a href="[cta-link]" class="cta-button animate-in">[Button text]</a>
    </div>
  </section>

  <script>
    // Intersection Observer for scroll-triggered .animate-in elements
    // Smooth scroll for anchor links
    // Counter animation for metric numbers (if present)
    // prefers-reduced-motion check
  </script>

</body>
</html>
```

#### Key Design Principles

These rules are non-negotiable for microsites:

1. **First impression matters** — the hero must be visually striking with a gradient background, full viewport height, and the company name front and center
2. **Personalization must be visible immediately** — company name in the hero, not buried below the fold
3. **Keep it SHORT** — 4-5 sections max, each scannable in 5 seconds. This is not a blog post.
4. **One CTA, repeated** — the same ask in the hero (subtle) and the closing section (prominent). Do not confuse with multiple different asks.
5. **Mobile-first** — this WILL be opened from email on a phone. All `clamp()` values must work at 375px width. Test aggressively.
6. **No sidebar, no navigation bar** — single vertical scroll. Smooth, clean, focused.
7. **Self-contained** — inline CSS, no external requests beyond Google Fonts. NO tracking pixels, analytics, or third-party scripts.

#### Content Density Limits

| Section | Max Content |
|---------|------------|
| Hero | 1 "Built for" tag + 1 headline (2 lines max) + 1 subhead (2 lines max) |
| Challenge / Gap | 1 heading + 3-4 short paragraphs or bullet points |
| Solution / Cards | 1 heading + 3 cards (icon + title + 2-line description each) |
| Proof / Metrics | 1 heading + 3 proof blocks (metric + company + 1-line quote each) |
| CTA | 1 heading + 1 supporting line + 1 button |

If content exceeds limits, cut ruthlessly. Microsites are scannable, not comprehensive.

#### Animation Patterns

Scroll-triggered entrance animations using Intersection Observer:

```css
.animate-in {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}
.animate-in.visible {
  opacity: 1;
  transform: translateY(0);
}
/* Stagger children within a section */
.animate-in:nth-child(1) { transition-delay: 0.1s; }
.animate-in:nth-child(2) { transition-delay: 0.2s; }
.animate-in:nth-child(3) { transition-delay: 0.3s; }
.animate-in:nth-child(4) { transition-delay: 0.4s; }
```

Additional effects (use sparingly):
- **Counter animation** for metrics: numbers count up when scrolled into view
- **Fade-scale** for cards: `transform: scale(0.96)` to `scale(1)` on reveal
- **Gradient shift** on hero: subtle background gradient animation via CSS keyframes

Always respect `prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  .animate-in { opacity: 1; transform: none; transition: none; }
}
```

#### Responsive Breakpoints

```css
/* Tablet */
@media (max-width: 768px) {
  .card-grid { grid-template-columns: 1fr; }
  .hero { min-height: 80vh; }
}

/* Mobile */
@media (max-width: 480px) {
  .section { padding: clamp(2rem, 6vh, 3rem) 1.25rem; }
  .heading-1 { font-size: clamp(1.8rem, 8vw, 2.5rem); }
}
```

#### Section Templates

Each section follows the pattern: `<section class="section" id="[id]"><div class="section-inner">...</div></section>`. Hero and CTA sections add the `hero` class for full-viewport layout.

**Hero:** `built-for` tag + `heading-1` headline + `body-lg` subhead + optional soft CTA link to `#cta`
**Challenge / Problem:** `heading-2` + 3 pain-point blocks (each: `heading-3` + `body-text`)
**Solution / Cards:** `heading-2` + `card-grid` with 3 cards (each: icon + `heading-3` + `body-text`)
**Proof / Metrics:** `heading-2` + `proof-grid` with 3 proof blocks (each: `big-number` metric + label + short quote with attribution)
**Process / Steps:** `heading-2` + numbered steps (each: `step-number` + `heading-3` + `body-text`)
**CTA:** `heading-1` headline + `body-lg` supporting line + `cta-button` link + optional contact info

All content elements use the `animate-in` class for scroll-triggered entrance animations.

### Step 5: Delivery

After generating the HTML file:

1. **Open the microsite** in the default browser
2. **Test mobile viewport** if browser-use is available (resize to 375px width)
3. **Present a summary:**

```
MICROSITE READY
===============

Folder: .octave-microsites/<company>-<date>/
File:   .octave-microsites/<company>-<date>/<company>-microsite.html
Target: [Company name]
Angle:  [Pain-point / Competitive / Value-led / Trigger-based]
CTA:    [Book a demo / etc.]
Style:  [Preset name or "Custom Brand"]
Size:   [file size]

How to share:
• Host on any static file server, S3 bucket, or Netlify drop
• Or send the HTML file directly as an attachment
• Best shared as a link in your outreach email

---

Want me to:
1. Adjust the messaging or tone
2. Change the angle (e.g., switch from pain-led to value-led)
3. Add or remove sections
4. Create versions for different contacts at the same company
5. Generate the outreach email that includes this link (/octave:generate)
6. Done
```

## MCP Tools Used

### Research & Enrichment
- `enrich_company` - Full company intelligence profile
- `enrich_person` - Full person intelligence report
- `find_person` - Find contacts at a company by title/role
- `qualify_company` - ICP fit scoring for a company
- `qualify_person` - ICP fit scoring for a person

### Library -- Fetching Entities
- `list_all_entities` - Quick scan of all entities of a type (minimal fields, no pagination)
- `list_entities` - Fetch entities with full data and pagination (proof points, references, etc.)
- `get_entity` - Deep dive on one specific entity
- `get_playbook` - Retrieve a playbook with full content and value props
- `list_value_props` - Value propositions for a specific playbook

### Library -- Searching
- `search_knowledge_base` - Semantic search across library entities and resources
- `list_resources` - Browse uploaded docs, URLs, and Google Drive files
- `search_resources` - Semantic search across uploaded resources

### Intelligence & Signals
- `list_findings` - Recent conversation findings and insights
- `list_events` - Deal events (won, lost, created, etc.)
- `get_event_detail` - Full details for a specific event

### Content Generation
- `generate_call_prep` - Synthesized prep brief for accounts
- `generate_content` - Generate positioning or messaging content

### Brand & Style
- `list_brand_voices` - Available brand voices in workspace
- `list_writing_styles` - Available writing styles in workspace

## Error Handling

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The microsite builder can still work without Octave — you provide the content manually, and I'll handle structure, style, and HTML generation. The result won't have Octave-powered personalization, but it will still look great.
>
> To reconnect: check your MCP configuration or run `/octave:workspace status`

**Company Not Found:**
> I couldn't find detailed intelligence for [target].
>
> Options:
> 1. Proceed with general positioning from your library — I'll use your best-fit playbook
> 2. Try a different domain or email
> 3. Provide company details manually (industry, size, challenges) and I'll personalize from that

**No Relevant Proof Points:**
> I couldn't find proof points in [their industry / of their size].
>
> Options:
> 1. Use your strongest proof points from adjacent industries
> 2. Use general metrics without company-specific quotes
> 3. Skip the proof section and lead with a stronger solution narrative

**No Competitor Data (for Competitive Angle):**
> I don't have data on the competitor they likely use.
>
> Options:
> 1. Switch to a different angle (pain-point led or value-led)
> 2. Use general competitive positioning without naming the competitor
> 3. Provide competitor details manually and I'll build the narrative

**No Matching Playbook:**
> No playbook matches this audience profile directly.
>
> I'll use your general value props and positioning. After the microsite is built, consider creating a playbook for this segment: `/octave:library create playbook`

**Browser-Use Unavailable (Brand Extraction):**
> Browser automation isn't available for brand extraction.
>
> Falling back to web fetch. If that doesn't capture your brand accurately, you can provide colors and fonts manually.

## Related Skills

- `/octave:one-pager` - Post-meeting leave-behind (microsite is pre-meeting)
- `/octave:research` - Deeper research on the account
- `/octave:generate` - Generate the outreach email that includes the microsite link
- `/octave:prospector` - Find more companies to create microsites for
- `/octave:abm` - Full ABM campaign planning with stakeholder mapping
- `/octave:campaign` - Campaign strategy that includes microsites
- `/octave:deck` - Presentation deck (for meetings, not sharing a link)
- `/octave:battlecard` - Competitive intelligence (for competitive angle microsites)
