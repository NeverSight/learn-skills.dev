---
name: proposal
description: Formal business case and proposal generator that produces customer-facing HTML documents with ROI framing and implementation details. Use when user says "create a proposal", "business case", "proposal for [company]", "formal pitch", or asks for a closing document.
---

# /octave:proposal - Octave-Powered Proposal Builder

Generate formal business case and proposal documents powered by your Octave GTM intelligence. These are the documents that close deals — sent to champions to sell internally, shared with procurement, and presented to executives. Unlike a one-pager (summary) or a deck (live presentation), proposals are comprehensive, customer-facing documents built for async review, internal circulation, and executive sign-off.

The output is a multi-section scrollable HTML document with a sticky table of contents, print-friendly layout, and the same CSS variable / style preset system as `/octave:deck`.

## Usage

```
/octave:proposal <target> [--style <preset>]
```

## Examples

```
/octave:proposal acme.com                                # Full proposal for Acme
/octave:proposal acme.com --style executive-dark         # With specific style
/octave:proposal "enterprise security platform deal"     # Context-based
/octave:proposal acme.com --style midnight-pro           # Dark professional style
/octave:proposal "renewal for DataCorp Q2"               # Renewal proposal
```

## Instructions

When the user runs `/octave:proposal`:

### Step 1: Understand the Context

If not provided via flags or obvious from the prompt, ask the user interactively:

**Target — "Who is this proposal for?"**

```
Who is this proposal for?

Provide any of the following:
- Company domain (e.g., acme.com)
- Person name or email (e.g., jane@acme.com)
- Deal context (e.g., "enterprise security platform deal with Acme")

Target:
```

**Stage — "Where is this deal?"**

```
What stage is this deal in?

1. Early exploration — they're interested, you're making the case
2. Mid-funnel evaluation — they're comparing options, full persuasion needed
3. Late-stage decision — they know the product, focus on commercials
4. Renewal — existing customer, results + what's next

Your choice:
```

| Stage | Impact on Proposal |
|-------|-------------------|
| Early exploration | Concise, don't overwhelm. Focus on problem + solution + proof. |
| Mid-funnel evaluation | Comprehensive. Full persuasion with every section. |
| Late-stage decision | Commercial focus. Investment, implementation, next steps. |
| Renewal | Backward-looking results + forward-looking roadmap. |

**Champion — "Who will use this document internally?"**

```
Who is your champion — the person who will circulate this internally?

Provide name, title, or role (e.g., "Sarah Chen, VP Engineering").
If unknown, I'll write for a general executive audience.

Champion:
```

**Key Concerns — "Any known objections or priorities?"**

```
Are there known objections, requirements, or priorities?

Examples:
- "They're worried about implementation timeline"
- "Security compliance is a hard requirement"
- "Competing against Gong and Chorus"
- "Budget is tight, need strong ROI story"

Key concerns (or skip):
```

**Pricing — "Include pricing?"**

```
Should the proposal include a pricing / investment section?

1. Yes — I'll include it (provide pricing details or I'll frame it)
2. No — leave pricing out
3. TBD — include a placeholder section

Your choice:
```

### Step 2: Octave Context Gathering

Based on the target, stage, champion, and concerns, use Octave MCP tools to build rich context. **Always tell the user what you're researching and why.**

**Call as many tools as needed to build a complete picture.** Proposals demand depth — company enrichment + playbook messaging + proof points + conversation intel + competitive context all combine to create a document that feels tailored, not templated. Don't stop at one tool when five would give you a stronger narrative.

Not every tool applies to every proposal. Use your judgment about which are relevant to *this specific* situation. The tables below show what's available — pick the combination that produces the most compelling case.

**List vs Search — when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all our proof points" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full proof point details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question — "how do we help in healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, existing proposals, pricing docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

**Follow-up proposals — ground them in what actually happened:**

If this proposal follows previous interactions with the account (demo, discovery call, pilot), pull findings and events to anchor the narrative in real data rather than generic positioning:

- `list_findings({ query: "<company or contact>", startDate: "<relevant period>" })` — surfaces what was actually said in calls: objections raised, features requested, pain points confirmed, competitor mentions
- `list_events({ filters: { accounts: ["<account_oId>"] } })` — deal stage changes, meetings held, emails sent — shows the journey so far
- `get_event_detail({ eventOId })` — deep dive on specific events to pull exact context

This turns a generic proposal into "here's what we heard from you, and here's exactly how we're addressing it."

---

#### Company & Contact Research

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Almost always — gives industry, size, tech stack, signals |
| Champion profile | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | When champion is known — tailor language to their role |
| Key stakeholders | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When you need to understand the buying committee |
| ICP fit scoring | `qualify_company({ companyDomain })` | When you need to quantify "why us" for this account |
| Person qualification | `qualify_person({ person: { ... } })` | When champion fit matters for framing |

---

#### Playbook & Messaging

| What you need | Tool | When to use |
|---------------|------|-------------|
| All playbooks | `list_all_entities({ entityType: "playbook" })` | Quick scan to find the right playbook |
| Matching playbook | `search_knowledge_base({ query: "<industry> <persona>", entityTypes: ["playbook"] })` | Find the best-fit playbook for this account |
| Playbook details | `get_playbook({ oId, includeValueProps: true })` | Full playbook content + value props — drives the proposal narrative |
| Value props | `list_value_props({ playbookOId })` | Fetch value props for the selected playbook |

---

#### Proof Points & Social Proof

This is critical for proposals. Buyers share these documents internally — social proof is what gets budget approved.

| What you need | Tool | When to use |
|---------------|------|-------------|
| All proof points | `list_entities({ entityType: "proof_point" })` | Fetch all proof points with full data — metrics, quotes, logos |
| All references | `list_entities({ entityType: "reference" })` | Fetch customer references with full details |
| Proof by topic | `search_knowledge_base({ query: "<industry> results", entityTypes: ["proof_point", "reference"] })` | Proof points relevant to their industry or use case |
| Uploaded case studies | `search_resources({ query: "case study" })` | Existing case study documents or PDFs |

---

#### Competitive Context

| What you need | Tool | When to use |
|---------------|------|-------------|
| Competitor profiles | `search_knowledge_base({ query: "<competitor>", entityTypes: ["competitor"] })` | When a competitor is in the deal |
| Competitor deep dive | `get_entity({ oId })` | Full competitor strengths, weaknesses, positioning |
| Products for comparison | `list_entities({ entityType: "product" })` | When you need feature-level differentiation |
| Competitive resources | `search_resources({ query: "<competitor>" })` | Uploaded battlecards, analyst reports |

---

#### Conversation History & Deal Intel

| What you need | Tool | When to use |
|---------------|------|-------------|
| Recent findings | `list_findings({ query: "<company>", startDate: "<relevant period>" })` | What was said in calls — objections, priorities, feature requests |
| Deal events | `list_events({ filters: { accounts: ["<account_oId>"] } })` | Timeline of the relationship |
| Event details | `get_event_detail({ eventOId })` | Deep dive on a specific call or meeting |
| Synthesized prep | `generate_call_prep({ companyDomain })` | Comprehensive brief to work from |

---

#### Existing Resources

| What you need | Tool | When to use |
|---------------|------|-------------|
| All resources | `list_resources()` | Browse uploaded docs, URLs, Drive files |
| Search resources | `search_resources({ query: "<topic>" })` | Find existing proposals, pricing docs, case studies |

---

**Output of this step:** Present a structured proposal outline to the user for approval before generating.

```
PROPOSAL OUTLINE: [Title]
==========================

Target: [Company name]
Champion: [Name, Title]
Stage: [Deal stage]
Key Concerns: [Listed concerns]
Include Pricing: [Yes / No / TBD]

---

SECTIONS TO INCLUDE
--------------------

1. COVER PAGE
   - "Prepared for [Company]"
   - Date, your company branding

2. TABLE OF CONTENTS
   - Clickable section navigation

3. EXECUTIVE SUMMARY
   - The situation, the opportunity, what you're proposing
   - Expected outcomes

4. THE CHALLENGE
   - [Specific pain point 1 — grounded in conversation data]
   - [Specific pain point 2 — from enrichment signals]
   - Cost of inaction

5. OUR SOLUTION
   - [Capability 1 mapped to pain point 1]
   - [Capability 2 mapped to pain point 2]
   - [Capability 3 — additional value]

6. WHY US
   - [Differentiator 1]
   - [Differentiator 2]
   - [Competitive advantage if competitor in deal]

7. PROOF OF RESULTS
   - [Case study 1 — same industry/size]
   - [Case study 2 — similar use case]
   - [Key metrics]

8. IMPLEMENTATION PLAN
   - Phases, timeline, milestones
   - What's needed from them

9. INVESTMENT
   - [Pricing / ROI framing / TBD placeholder]

10. NEXT STEPS
    - Specific actions, dates, owners

11. APPENDIX (optional)
    - Technical details, security, compliance

---

Octave Sources Used:
- Company profile: [Company] — [key insights]
- Playbook: [Playbook name] — [messaging angle]
- Proof points: [N] references pulled
- Competitive intel: [If applicable]
- Findings: [N] recent signals

---

Does this outline look good? I can:
1. Proceed to style selection and generation
2. Add / remove / reorder sections
3. Go deeper on any section
4. Change the narrative angle
```

**Wait for user approval before proceeding.**

### Step 3: Style Selection

Proposals should feel premium and professional. The default recommendation depends on the audience:

| Audience | Recommended Default |
|----------|-------------------|
| Enterprise / executive | `executive-dark` |
| Technical / modern | `midnight-pro` |
| Conservative / traditional | `paper-minimal` |
| General | `executive-dark` |

Ask the user:

```
How would you like to style the proposal?

1. Use recommended — [preset name] (best for [audience])
2. Pick from presets — show me all 12 options
3. Use my brand — extract from a website or provide brand assets
4. Surprise me — auto-pick based on context

Your choice:
```

**If user picks "Show me all 12 options":**

```
STYLE PRESETS
=============

DARK THEMES
  1. midnight-pro      — Dark navy, white text, blue accents. Executive feel.
  2. executive-dark    — Charcoal + gold. Premium boardroom aesthetic.
  3. octave-brand      — Octave purple on dark navy. Product-aligned.
  4. electric-studio   — Pure black + electric blue. Tech-forward.
  5. neon-pulse        — Dark + neon green/cyan. Developer/hacker energy.
  6. dark-botanical    — Dark + warm gold/rose. Elegant and premium.

LIGHT THEMES
  7. swiss-modern      — White + red accent. Bauhaus minimal.
  8. soft-light        — Warm white + sage green. Calm and approachable.
  9. paper-minimal     — Off-white + black type. Editorial simplicity.

VIBRANT THEMES
  10. solar-flare      — Deep orange gradients. Bold and energetic.
  11. aurora-gradient   — Purple-to-teal gradients. Visionary and modern.
  12. monochrome-bold  — High-contrast B&W. Statement typography.

Your choice (number or name):
```

Full CSS variable definitions for each preset are in the deck skill's [STYLE_PRESETS.md](../deck/STYLE_PRESETS.md).

**Brand extraction is encouraged for proposals.** A proposal that carries the customer's or your own brand colors looks significantly more professional and intentional. Follow the same brand discovery flow as `/octave:deck` Step 3 (browser-use > WebFetch > manual fallback).

### Step 4: Generate HTML

Build a single, self-contained HTML file. **No external dependencies** except Google Fonts. Everything else inlined.

#### Output Directory

Every proposal gets its own folder under `.octave-proposals/`:

```
.octave-proposals/
└── <kebab-case-name>-<YYYY-MM-DD>/
    ├── <name>.html                    # Final HTML proposal
    └── <name>-content.md              # Markdown export (if requested)
```

Example: `/octave:proposal acme.com` -> `.octave-proposals/acme-corp-proposal-2026-02-11/acme-corp-proposal.html`

The entire `.octave-proposals/` directory is in `.gitignore` — nothing here gets committed.

#### Section Selection by Stage

Not all sections appear in every proposal. Stage determines what's included:

| Stage | Sections Included | Notes |
|-------|-------------------|-------|
| Early exploration | Cover, TOC, Exec Summary, Challenge, Solution, Proof, Next Steps | Keep it concise, don't overwhelm |
| Mid-funnel evaluation | All sections (1-11) | Full persuasion, comprehensive |
| Late-stage decision | Cover, TOC, Exec Summary, Investment, Implementation, Next Steps | They know the product, focus on commercials |
| Renewal | Cover, TOC, Exec Summary (results achieved), Solution (what's new), Investment, Next Steps | Backward-looking + forward |

#### Document Sections — Full Proposal

**1. Cover Page**
- Title: "Proposal for [Company]" or a more compelling headline
- Subtitle: "Prepared by [Your Company]"
- Date
- Your company logo (if brand was extracted)
- Champion name and title (if known)
- Confidential notice

**2. Table of Contents**
- Clickable anchor links to each section
- Section numbers and titles
- Sticky sidebar navigation on wider screens

**3. Executive Summary**
- 3-4 paragraphs, each with a clear purpose:
  - The situation: what's happening in their business/industry
  - The opportunity: the gap between where they are and where they could be
  - What you're proposing: your solution in one clear statement
  - Expected outcomes: measurable results they can expect
- This section should stand alone — many executives read only this

**4. The Challenge**
- Their specific pain points, grounded in conversation data if available
- Industry context — why this matters now
- Cost of inaction — what happens if they do nothing
- 2-3 challenge areas, each with a heading and 2-3 supporting points

**5. Our Solution**
- How you solve their specific problems, mapped to the challenges above
- 3-4 key capabilities, each with:
  - A heading
  - A description of what it does
  - How it specifically addresses their pain point
- Visual: capability cards or a numbered list

**6. Why Us**
- Differentiators that matter to *them* (not generic features)
- If competitor is in the deal: honest, respectful comparison
- Unique strengths: technology, approach, team, track record
- Avoid feature checklists — frame as business advantages

**7. Proof of Results**
- Case studies grouped by relevance to their situation
- For each: company name, challenge, solution, results (metrics)
- Customer quotes if available from proof points
- Logo wall of recognizable customers
- Industry-specific proof prioritized

**8. Implementation Plan**
- Timeline with phases: onboarding, configuration, rollout, optimization
- Milestones and deliverables per phase
- What's needed from them (data, access, stakeholders)
- Time to first value
- Visual: timeline or process steps

**9. Investment**
- If pricing included: pricing table with tiers or packages
- ROI framing: "For [investment], you get [value]"
- Comparison: cost vs. cost of current process / inaction
- Payment terms or structure if relevant
- If TBD: placeholder section with "Investment details to be discussed based on scope"

**10. Next Steps**
- Specific actions with owners and dates
- 3-5 concrete steps: "Schedule technical review", "Finalize scope", etc.
- Contact information
- Call to action: make it easy to say yes

**11. Appendix (optional)**
- Technical specifications
- Integration details
- Security and compliance certifications
- Team bios
- Detailed feature breakdown
- Terms and conditions reference

#### HTML Architecture

The proposal uses the same CSS variable system as `/octave:deck` (see [STYLE_PRESETS.md](../deck/STYLE_PRESETS.md)) but with a document layout instead of slides.

**Core structure:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Proposal Title] - [Company Name]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* CSS Variables from chosen preset — :root { ... } */
    /* Reset & Base — smooth scroll, body with --font-body, --bg, --text-primary, line-height: 1.7 */
    /* Document Layout — .proposal-wrapper: flex, max-width 1100px, margin auto */
    /* Sidebar TOC — .toc-sidebar: width 220px, sticky, top 2rem; links with active state via --brand-primary */
    /* Main Content — .proposal-content: max-width 850px, flex 1, clamp padding */
    /* Sections — .proposal-section: margin-bottom clamp, scroll-margin-top for anchor offset */
    /* Cover Page — .cover-page: min-height 100vh, flex center, text-align center */
    /* Typography — h1-h3 with clamp() font sizes, --font-display; p with --text-secondary */
    /* Components — .card, .metric-card, .big-number, .quote-block, .timeline-step, .step-number, .pill, .pricing-table, .logo-grid */
    /* Print Styles (critical) — hide sidebar, full-width content, page-break-after on cover, page-break-inside avoid on sections/cards */
    /* Responsive — hide sidebar below 900px */
    /* prefers-reduced-motion — disable transitions */
  </style>
</head>
<body>
  <div class="proposal-wrapper">
    <nav class="toc-sidebar">
      <h4>Contents</h4>
      <a href="#executive-summary">Executive Summary</a>
      <a href="#the-challenge">The Challenge</a>
      <!-- ... one link per section -->
    </nav>
    <main class="proposal-content">
      <section class="cover-page" id="cover">...</section>
      <section class="proposal-section" id="executive-summary">...</section>
      <!-- Continue for each section -->
    </main>
  </div>
  <script>
    // Intersection Observer for active TOC highlighting
    // Smooth scroll behavior
  </script>
</body>
</html>
```

**Print styles are non-negotiable for proposals.** Buyers print these documents. Always include:
- `page-break-after: always` on cover page
- `page-break-inside: avoid` on sections and cards
- `page-break-after: avoid` on h2 (keep headings with their content)
- Hide sidebar, expand content to full width
- Set body font-size to 11pt for readability

#### Key Differences from Deck HTML

| Concern | Deck | Proposal |
|---------|------|----------|
| Layout | Full-viewport slides, scroll-snap | Scrollable document, max-width content |
| Navigation | Nav dots, keyboard slide-to-slide | Sticky sidebar TOC with anchor links |
| Content density | Strict per-slide limits | Paragraphs, long-form content allowed |
| Print | Not a priority | Critical — buyers print proposals |
| Page breaks | N/A | Between major sections for printing |
| Typography | Display/impact focused | Readability focused, longer line heights |
| Width | Full viewport | Max 850px content + 220px sidebar |
| Animation | Entrance animations per slide | Subtle — scroll-based fade-in at most |

#### Typography Recommendations

Proposals benefit from serif headings paired with sans-serif body text for a formal, authoritative feel:

| Preset | Heading Font | Body Font |
|--------|-------------|-----------|
| executive-dark | Playfair Display | Inter |
| midnight-pro | Inter | Inter |
| paper-minimal | Libre Baskerville | Source Sans 3 |
| swiss-modern | Inter | Inter |

For brand-extracted styles, prefer the brand's own fonts. If none are available, default to the heading/body pairing from the chosen preset.

#### Content Writing Guidelines

Proposals are persuasive documents, not feature lists. Follow these principles:

1. **Lead with their world, not yours.** Open every section from the customer's perspective.
2. **Ground in specifics.** Use company name, industry data, conversation quotes. Generic = ignored.
3. **Quantify everything.** "Reduce onboarding time by 60%" beats "Faster onboarding."
4. **One idea per paragraph.** Executives skim. Make every paragraph earn its place.
5. **Active voice.** "We deploy in 4 weeks" not "Deployment is completed in 4 weeks."
6. **Address objections before they arise.** If you know a concern, handle it in the relevant section.
7. **End every section with a forward pull.** Give the reader a reason to keep going.

### Step 5: Delivery

After generating the HTML file:

1. **Open the proposal** in the default browser
2. **Present a summary:**

```
PROPOSAL READY
==============

Folder: .octave-proposals/<name>-<date>/
File:   .octave-proposals/<name>-<date>/<name>.html
Sections: [N] sections included
Style:  [Preset name or "Custom Brand"]
Stage:  [Deal stage]
Size:   [file size]

Included Sections:
- Cover Page
- Table of Contents
- Executive Summary
- The Challenge
- Our Solution
- Why Us
- Proof of Results
- Implementation Plan
- Investment
- Next Steps

Navigation:
- Scroll to read — sticky sidebar shows your position
- Click any TOC item to jump to that section
- Print: Cmd+P / Ctrl+P — page breaks between sections

---

Want me to:
1. Adjust specific sections — go deeper, change tone, add detail
2. Add pricing — provide numbers and I'll format the investment section
3. Change the style — different preset or brand colors
4. Create a version for a different stakeholder (e.g., technical vs. executive)
5. Export as PDF — print instructions for full fidelity
6. Create a companion deck — presentation version of this proposal
7. Done
```

**Stakeholder variants:** If the user asks for a version for a different audience (e.g., "make one for the CTO"), adjust:
- Emphasis: shift from business value to technical architecture
- Language: match the stakeholder's domain
- Sections: add/remove appendix items, shift proof points to technical ones
- Tone: executive = strategic, technical = detailed, procurement = ROI-focused

**PDF export guidance:**

```
To save as PDF (recommended for sharing):

1. Open the proposal in your browser (already open)
2. Press Cmd+P (Mac) or Ctrl+P (Windows)
3. Set margins to "Default" or "Minimum"
4. Enable "Background graphics" for colors and styling
5. Select "Save as PDF"

The proposal is designed with page breaks between sections for clean printing.
```

## MCP Tools Used

### Research & Enrichment
- `enrich_company` — Full company intelligence profile
- `enrich_person` — Full person intelligence report
- `find_person` — Find contacts at a company by title/role
- `qualify_company` — ICP fit scoring for a company
- `qualify_person` — ICP fit scoring for a person

### Library — Fetching Entities
- `list_all_entities` — Quick scan of all entities of a type (minimal fields)
- `list_entities` — Fetch entities with full data and pagination
- `get_entity` — Deep dive on one specific entity
- `get_playbook` — Retrieve a playbook with full content and value props
- `list_value_props` — Value propositions for a specific playbook

### Library — Searching
- `search_knowledge_base` — Semantic search across library entities and resources
- `list_resources` — Browse uploaded docs, URLs, and Google Drive files
- `search_resources` — Semantic search across uploaded resources

### Intelligence & Signals
- `list_findings` — Recent conversation findings and insights
- `list_events` — Deal events (won, lost, created, stage changes)
- `get_event_detail` — Full details for a specific event

### Content Generation
- `generate_call_prep` — Synthesized prep brief for accounts
- `generate_content` — Generate positioning or messaging content

### Brand & Style
- `list_brand_voices` — Available brand voices in workspace
- `list_writing_styles` — Available writing styles in workspace

## Error Handling

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The proposal builder can still work without Octave — you'll provide the content manually, and I'll handle structure, style, and HTML generation.
>
> To reconnect: check your MCP configuration or run `/octave:workspace status`

**Company Not Found:**
> I couldn't find detailed intelligence for [domain].
>
> Options:
> 1. Proceed with what we have — I'll use general positioning from your library
> 2. Try a different domain
> 3. Provide company context manually and I'll build the proposal

**No Proof Points Available:**
> No proof points or references matched this account's industry or use case.
>
> Options:
> 1. Proceed without a Proof of Results section
> 2. Add generic proof points (I'll use your best available)
> 3. Provide case study details manually
> 4. Skip for now and add later

**No Pricing Information:**
> No pricing resources found in your workspace.
>
> Options:
> 1. Provide pricing details and I'll format them
> 2. Include a TBD placeholder — "Investment details to be discussed"
> 3. Omit the investment section entirely

**No Matching Playbook:**
> No playbook matches this audience profile directly.
>
> I'll use your general value props and positioning. After the proposal is built, consider creating a playbook for this segment.

## Related Skills

- `/octave:deck` — Presentation version of the pitch (for live presenting)
- `/octave:one-pager` — Summary version (when a full proposal is too heavy)
- `/octave:brief` — Internal prep document (for your team, not the customer)
- `/octave:research` — Deeper research on the account before writing
- `/octave:battlecard-doc` — Competitive reference document (if competitor in deal)
- `/octave:generate` — Generate content with brand voice control
- `/octave:pipeline` — Deal-level strategy and coaching
