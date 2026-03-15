---
name: one-pager
description: Personalized one-pager / leave-behind generator rendered as self-contained HTML. Use when user says "one-pager for [company]", "leave-behind", "follow-up doc", "demo summary", or asks for a concise customer-facing document.
---

# /octave:one-pager - Personalized One-Pager Builder

Generate personalized, self-contained HTML one-pager documents (leave-behinds) powered by your Octave GTM knowledge base. Unlike generic templates, this skill enriches every section with real account intelligence -- company signals, persona pain points, playbook messaging, and proof points -- to create a document that feels written specifically for the recipient.

One-pagers are single scrollable pages designed to be sent after a demo, meeting, or call. They summarize why your product is a fit for this specific account. Think of it as the document you email or print, not present.

## Usage

```
/octave:one-pager <target> [--for <occasion>] [--style <preset>]
```

## Examples

```
/octave:one-pager acme.com                              # General one-pager for Acme
/octave:one-pager jane@acme.com --for demo-followup     # Post-demo leave-behind
/octave:one-pager acme.com --for discovery              # Post-discovery summary
/octave:one-pager "enterprise healthcare segment"       # Segment-level one-pager
/octave:one-pager acme.com --for renewal --style soft-light  # Renewal doc with specific style
/octave:one-pager jane@acme.com --for event-followup    # Post-conference/event follow-up
```

## Occasions

| Occasion | Output Focus |
|----------|--------------|
| `demo-followup` | Recap what was shown, reinforce value, clear next steps |
| `discovery` | Summarize pain points heard, position solution fit |
| `intro` | General company intro tailored to the account (default) |
| `event-followup` | Post-conference/event personalized summary |
| `renewal` | Reinforce value delivered, expansion opportunities |

## Instructions

When the user runs `/octave:one-pager`:

### Step 1: Understand the Context

If not provided via flags, ask the user interactively:

**Target -- "Who is this for?"**

```
Who is this one-pager for?

Provide any of the following:
- Company domain (e.g., acme.com)
- Person email (e.g., jane@acme.com)
- Segment description (e.g., "enterprise healthcare")

Target:
```

**Occasion -- "What's the context?"**

```
What's the occasion for this one-pager?

1. Demo follow-up - Sent after a product demo
2. Discovery follow-up - Sent after a discovery call
3. General intro - First touch or general positioning
4. Event follow-up - Sent after a conference/event meeting
5. Renewal - Reinforcing value for an existing customer

Your choice:
```

**Tone -- "What tone should it strike?"**

```
What tone fits best?

1. Formal executive - Polished, concise, boardroom-ready
2. Conversational - Warm, approachable, peer-to-peer
3. Technical - Data-driven, detailed, practitioner-focused

Your choice:
```

### Step 2: Octave Context Gathering

Based on target, occasion, and tone, use Octave MCP tools to build rich context for the one-pager. **Always tell the user what you're researching and why.**

**Call as many tools as needed to build a complete picture.** The best one-pagers come from layering multiple sources -- company enrichment + playbook messaging + proof points + conversation intel all combine to create a document that feels genuinely personalized. Don't stop at one tool when three would give you a stronger narrative.

That said, not every tool applies to every one-pager. Use your judgment about which are relevant to *this specific* situation. The tables below show what's available -- pick the combination that gives you the richest context for the occasion and target.

**List vs Search -- when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory -- "show me all our playbooks" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content -- "get full proof point details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question -- "how do we position for healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, uploaded assets, or source docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

**Follow-up one-pagers -- ground them in what actually happened:**

If this one-pager follows a previous interaction (demo, discovery call, event meeting), pull findings and events to anchor the narrative in real data rather than generic positioning:

- `list_findings({ query: "<company or contact>", startDate: "<relevant period>" })` -- surfaces what was actually said in calls: objections raised, features requested, pain points confirmed, competitor mentions
- `list_events({ filters: { accounts: ["<account_oId>"] } })` -- deal stage changes, meetings held, emails sent -- shows the journey so far
- `get_event_detail({ eventOId })` -- deep dive on specific events (e.g., the demo, the discovery call) to pull exact context

This turns a generic "here's why we're a fit" document into "here's what we heard from you, and here's how we address it" -- much more compelling for the recipient.

---

#### For Account-Specific One-Pagers

Start with company and person enrichment, then pull positioning context:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Almost always -- gives industry, size, tech stack, signals |
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | When a specific person is the recipient |
| Key contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When you need to identify the right stakeholder(s) |
| ICP fit scoring | `qualify_company({ companyDomain })` | When you need to frame "why us" for this account |
| Matching playbook | `search_knowledge_base({ query: "<industry> <persona>", entityTypes: ["playbook"] })` | To find the best-fit messaging framework |
| Playbook + value props | `get_playbook({ oId, includeValueProps: true })` | After finding a relevant playbook -- gets full content + value props |
| Value props | `list_value_props({ playbookOId })` | Fetch value props for a specific playbook |
| Proof points | `list_entities({ entityType: "proof_point" })` | Fetch proof points with full data -- metrics, quotes, logos |
| References | `list_entities({ entityType: "reference" })` | Fetch customer references with full details |
| Topic-specific proof | `search_knowledge_base({ query: "<industry> results", entityTypes: ["proof_point", "reference"] })` | When you need proof points *about* a specific topic or industry |
| Competitive context | `search_knowledge_base({ query: "<signals>", entityTypes: ["competitor"] })` | When competitor is mentioned or likely in the deal |
| Recent intel | `list_findings({ query: "<company>", startDate: "<90 days ago>" })` | Conversation-based insights for follow-up docs |
| Deal events | `list_events({ filters: { accounts: ["<account_oId>"] } })` | Deal progression for follow-up context |
| Event details | `get_event_detail({ eventOId })` | Deep dive on specific interactions |
| Synthesized prep | `generate_call_prep({ companyDomain })` | When you want a single comprehensive brief to work from |
| Uploaded assets | `search_resources({ query: "<topic>" })` | Relevant uploaded docs or reference materials |

---

#### For Segment-Level One-Pagers

When the target is a segment description rather than a specific company:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Matching playbook | `search_knowledge_base({ query: "<segment description>", entityTypes: ["playbook"] })` | Find the playbook for this segment |
| Playbook + value props | `get_playbook({ oId, includeValueProps: true })` | Full messaging framework for the segment |
| Personas | `list_entities({ entityType: "persona" })` | Understand who the typical buyer is in this segment |
| Segments | `list_all_entities({ entityType: "segment" })` | Quick scan to match the description to a defined segment |
| Proof points | `list_entities({ entityType: "proof_point" })` | Fetch proof points relevant to this segment |
| References | `list_entities({ entityType: "reference" })` | Customer references in this segment |
| Products | `list_entities({ entityType: "product" })` | Product capabilities relevant to segment needs |
| Use cases | `list_all_entities({ entityType: "use_case" })` | Use cases that resonate with this segment |
| Uploaded resources | `search_resources({ query: "<segment topic>" })` | Relevant uploaded collateral |

---

**Output of this step:** Present a content outline to the user for approval:

```
ONE-PAGER OUTLINE: [Title]
===========================

Target: [Company / Person / Segment]
Occasion: [Demo follow-up / Discovery / Intro / Event / Renewal]
Tone: [Formal / Conversational / Technical]

---

PROPOSED SECTIONS
-----------------

1. HEADER
   - "Prepared for [Company]"
   - Date, your company logo

2. THE CHALLENGE
   - [Pain point 1 from enrichment/findings]
   - [Pain point 2 from enrichment/findings]

3. OUR APPROACH
   - [Value prop 1 from playbook, tailored]
   - [Value prop 2 from playbook, tailored]
   - [Value prop 3 from playbook, tailored]

4. KEY DIFFERENTIATORS
   - [Differentiator 1 — brief description]
   - [Differentiator 2 — brief description]
   - [Differentiator 3 — brief description]

5. PROOF POINTS
   - [Customer result / metric 1]
   - [Customer result / metric 2]
   - [Quote or reference if available]

6. NEXT STEPS
   - [CTA based on occasion]
   - Contact info

---

Octave Sources Used:
- Company profile: [Company name] — [key insights]
- Playbook: [Playbook name] — [messaging angle]
- Proof points: [N] references pulled
- Findings: [N] recent signals (if follow-up)

---

Does this outline look good? I can:
1. Proceed to style selection and generation
2. Add or remove sections
3. Change the messaging angle
4. Adjust the tone or emphasis
```

**Wait for user approval before proceeding.**

### Step 3: Style Selection

One-pagers use the same 12 style presets and brand extraction system as the deck skill. See [STYLE_PRESETS.md](../deck/STYLE_PRESETS.md) for full CSS variable definitions.

Ask the user:

```
How would you like to style the one-pager?

1. Pick from presets — 12 styles from dark executive to light minimal
2. Use my brand — extract from my website or provide brand assets
3. Auto-pick — I'll choose based on the occasion and tone
4. Surprise me

Your choice:
```

**Option 1: Preset Picker** -- Show the same preset table from the deck skill (see `/octave:deck` Step 4, Option 2).

**Option 2: Brand Extraction** -- Follow the same brand discovery flow from the deck skill (see `/octave:deck` Step 3). Supports browser-use tier, WebFetch tier, and manual fallback. Confirm brand config with user before proceeding.

**Option 3: Auto-Pick** -- Map occasion + tone to recommended presets:

| Occasion + Tone | Recommended Preset |
|------------------|--------------------|
| Demo follow-up, formal | `midnight-pro` |
| Demo follow-up, conversational | `soft-light` |
| Discovery, formal | `executive-dark` |
| Discovery, conversational | `swiss-modern` |
| Intro, formal | `midnight-pro` |
| Intro, conversational | `soft-light` |
| Intro, technical | `electric-studio` |
| Event follow-up | `aurora-gradient` |
| Renewal, formal | `executive-dark` |
| Renewal, conversational | `soft-light` |

Tell the user what you picked and why. Let them override.

### Step 4: Generate HTML

Build a single, self-contained HTML file. **No external dependencies** except Google Fonts. This is a single scrollable document -- NOT slides.

#### Output Directory

Every one-pager gets its own folder under `.octave-one-pagers/`:

```
.octave-one-pagers/
└── <kebab-case-name>-<YYYY-MM-DD>/
    └── <name>.html
```

Example: `/octave:one-pager acme.com` produces `.octave-one-pagers/acme-one-pager-2026-02-11/acme-one-pager.html`

The entire `.octave-one-pagers/` directory is in `.gitignore` -- nothing here gets committed.

#### HTML Architecture

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[One-Pager Title]</title>
  <!-- Google Fonts (preconnect + stylesheet) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from chosen preset) === */
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

    /* === Page Container (narrower than deck) === */
    .page {
      max-width: 800px;
      margin: 0 auto;
      padding: clamp(2rem, 5vw, 4rem) clamp(1.5rem, 4vw, 3rem);
    }

    /* === Typography (all clamp-based) === */
    .heading-1 { font-size: clamp(1.75rem, 4vw, 2.75rem); }
    .heading-2 { font-size: clamp(1.25rem, 2.5vw, 1.75rem); }
    .heading-3 { font-size: clamp(1rem, 1.8vw, 1.25rem); }
    .body-text { font-size: clamp(0.875rem, 1.3vw, 1rem); }
    .body-sm { font-size: clamp(0.75rem, 1.1vw, 0.875rem); }

    /* === Section Spacing === */
    .section { margin-bottom: clamp(2rem, 4vh, 3rem); }
    .section-title {
      font-family: var(--font-display);
      color: var(--brand-primary);
      margin-bottom: clamp(0.75rem, 1.5vh, 1.25rem);
    }

    /* === Components === */
    .card { ... }
    .metric-card { ... }
    .proof-quote { ... }
    .cta-block { ... }
    .divider { ... }

    /* === Print Styles === */
    @media print {
      body { background: white; color: #1a1a1a; }
      .page { max-width: 100%; padding: 0.5in; }
      .card { break-inside: avoid; border: 1px solid #e5e5e5; }
      .section { break-inside: avoid; }
      a { color: inherit; text-decoration: underline; }
    }

    /* === Responsive === */
    @media (max-width: 600px) {
      .grid-3 { grid-template-columns: 1fr; }
      .grid-2 { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="page">
    <!-- Header -->
    <!-- The Challenge -->
    <!-- Our Approach -->
    <!-- Key Differentiators -->
    <!-- Proof Points -->
    <!-- Next Steps -->
  </div>
</body>
</html>
```

Key differences from the deck skill's HTML:
- **No scroll snap** -- natural scrolling, single continuous page
- **No navigation dots or progress bar** -- not a presentation
- **No slide-level animations** -- subtle entrance animations are fine, but no Intersection Observer per-section
- **Narrower container** -- `max-width: 800px` (vs deck's 1100px)
- **Print-friendly** -- includes `@media print` styles for PDF/print output
- **No `overflow: hidden` sections** -- content flows naturally

#### Document Sections

**Header:**
```html
<header class="section header">
  <!-- Logo if available (from brand extraction or Octave workspace) -->
  <img src="[logo-url]" alt="[Company]" class="logo" />
  <h1 class="heading-1">[Document Title]</h1>
  <p class="body-text text-secondary">Prepared for [Target Company] | [Date]</p>
</header>
```

**The Challenge:**
```html
<section class="section">
  <h2 class="heading-2 section-title">The Challenge</h2>
  <p class="body-text">
    [2-3 sentences about their pain points, drawn from enrichment data,
    findings, or persona pain points. Specific to this account.]
  </p>
</section>
```

**Our Approach:**
```html
<section class="section">
  <h2 class="heading-2 section-title">Our Approach</h2>
  <div class="value-props">
    <div class="value-prop">
      <h3 class="heading-3">[Value Prop Headline]</h3>
      <p class="body-text text-secondary">[1-2 sentences tailored to their situation]</p>
    </div>
    <!-- Repeat for 3-4 value props -->
  </div>
</section>
```

**Key Differentiators:**
```html
<section class="section">
  <h2 class="heading-2 section-title">Why [Your Company]</h2>
  <div class="grid-3">
    <div class="card">
      <h3 class="heading-3">[Differentiator]</h3>
      <p class="body-sm text-secondary">[1-2 sentences]</p>
    </div>
    <!-- 3 cards max -->
  </div>
</section>
```

**Proof Points:**
```html
<section class="section">
  <h2 class="heading-2 section-title">Results</h2>
  <div class="proof-points">
    <div class="metric-card">
      <span class="big-number">[Metric Value]</span>
      <span class="body-sm text-secondary">[Metric Label]</span>
    </div>
    <!-- 2-3 metrics or quotes -->
  </div>
  <!-- Optional quote -->
  <blockquote class="proof-quote">
    "[Customer quote]"
    <cite>-- [Name, Title, Company]</cite>
  </blockquote>
</section>
```

**Next Steps:**
```html
<section class="section cta-block">
  <h2 class="heading-2 section-title">Next Steps</h2>
  <p class="body-text">[Clear CTA based on occasion]</p>
  <div class="contact-info">
    <p class="body-sm">[Name] | [Email] | [Phone]</p>
    <p class="body-sm">[Meeting link if available]</p>
  </div>
</section>
```

#### Content Density Rules

Keep it tight. A one-pager should be scannable in under 2 minutes:

| Section | Max Content |
|---------|------------|
| Header | Company name + title + date + "Prepared for" |
| The Challenge | 2-3 sentences max |
| Our Approach | 3-4 value props, each 1-2 sentences |
| Key Differentiators | 3 cards max, each heading + 1-2 sentences |
| Proof Points | 2-3 metrics or quotes |
| Next Steps | 1 CTA + contact info |

If content exceeds these limits, prioritize ruthlessly. The one-pager is a teaser, not a whitepaper.

### Step 5: Delivery

After generating the HTML file:

1. **Open the one-pager** in the default browser
2. **Present a summary:**

```
ONE-PAGER READY
================

Folder: .octave-one-pagers/<name>-<date>/
File:   .octave-one-pagers/<name>-<date>/<name>.html
Style:  [Preset name or "Custom Brand"]
Size:   [file size]

Viewing:
- Open in any browser -- single scrollable page
- Print-friendly -- Cmd+P / Ctrl+P for clean printout
- Email as attachment or save as PDF

Customization tips:
- Colors: Edit the :root CSS variables at the top of the file
- Content: Each <section class="section"> is one block
- Fonts: Change the Google Fonts <link> and font-family values
- Layout: Adjust max-width in .page for wider/narrower output

---

Want me to:
1. Adjust content or messaging
2. Change the style/colors
3. Export as PDF (print dialog)
4. Create a version for a different contact at the same company
5. Create a full presentation deck for this account (/octave:deck)
6. Done
```

## MCP Tools Used

### Research & Enrichment
- `enrich_company` - Full company intelligence profile
- `enrich_person` - Full person intelligence report
- `find_person` - Find contacts at a company by title/role
- `qualify_company` - ICP fit scoring for a company
- `qualify_person` - ICP fit scoring for a person
- `find_company` - Find companies matching criteria

### Library -- Fetching Entities
- `list_all_entities` - Quick scan of all entities of a type (minimal fields, no pagination)
- `list_entities` - Fetch entities with full data and pagination (proof points, references, personas, etc.)
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
> The one-pager builder can still work without Octave -- you'll provide the content manually, and I'll handle structure, style, and HTML generation.
>
> To reconnect: check your MCP configuration or run `/octave:workspace status`

**Company/Person Not Found:**
> I couldn't find detailed intelligence for [target].
>
> Options:
> 1. Proceed with what we have -- I'll use general positioning from your library
> 2. Try a different domain or email
> 3. Provide the content manually and I'll build the one-pager

**No Matching Playbook:**
> No playbook matches this audience profile directly.
>
> I'll use your general value props and positioning. After the one-pager is built, consider creating a playbook for this segment: `/octave:library create playbook`

**No Proof Points Available:**
> No proof points found matching this account's industry or segment.
>
> Options:
> 1. Proceed without the proof points section
> 2. Use general proof points from your library
> 3. Provide customer results manually and I'll format them

**No Findings for Follow-Up:**
> No conversation findings found for [target] in the recent period.
>
> This means I'll build the one-pager from enrichment data and library content rather than grounding it in specific past conversations. You can provide meeting notes or context manually if you have them.

## Related Skills

- `/octave:deck` - Full presentation deck (when one page isn't enough)
- `/octave:research` - Deeper research on the account
- `/octave:brief` - Internal account dossier (vs external leave-behind)
- `/octave:proposal` - Formal business case
- `/octave:microsite` - Personalized web page for ABM
