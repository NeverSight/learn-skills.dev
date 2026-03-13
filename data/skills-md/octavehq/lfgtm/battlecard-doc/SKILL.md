---
name: battlecard-doc
description: Visual competitive battlecard document rendered as interactive HTML with expandable sections and color-coded comparisons. Use when user says "battlecard document", "visual battlecard", "competitive reference doc", or wants a formatted HTML version of competitive intelligence. Do NOT use for text-based competitive analysis — use /octave:battlecard instead.
---

# /octave:battlecard-doc - Visual Competitive Battlecard

Generate polished, self-contained HTML competitive battlecard documents powered by your Octave GTM knowledge base. Designed to be bookmarked and referenced during live competitive deals. Sticky sidebar navigation, color-coded win/loss indicators, expandable objection handlers, and visual scorecard bars make these documents scannable under pressure.

Unlike `/octave:battlecard` which outputs text-based competitive intelligence, this skill renders that intelligence as a styled, interactive HTML document with visual hierarchy. Unlike `/octave:deck` which builds presentations for audiences, this is an internal reference document for individual use.

## Usage

```
/octave:battlecard-doc [--competitor <name>] [--style <preset>]
```

## Examples

```
/octave:battlecard-doc --competitor "Gong"                # Deep-dive battlecard for vs Gong
/octave:battlecard-doc                                    # Pick competitor interactively
/octave:battlecard-doc --competitor "all"                  # Full competitive landscape doc
/octave:battlecard-doc --competitor "Gong" --style neon-pulse
```

## Instructions

When the user runs `/octave:battlecard-doc`:

### Step 1: Identify Competitor(s)

If `--competitor` is not specified, fetch the competitor list and let the user choose:

```
# Get all competitors
list_all_entities({ entityType: "competitor" })
```

Present:

```
Which competitor are you building a battlecard for?

COMPETITORS IN YOUR LIBRARY
1. [Competitor 1] - [Brief description]
2. [Competitor 2] - [Brief description]
3. [Competitor 3] - [Brief description]

OTHER
4. Full competitive landscape (all competitors)

Your choice:
```

If they pick a single competitor, confirm the scope:

```
What kind of document do you want?

1. Full battlecard — comprehensive reference with all sections
2. Quick reference — positioning + objections + trap questions only

Your choice:
```

If they pick "all" or "Full competitive landscape," confirm:

```
I'll create a landscape overview with condensed battlecards for each competitor.
This includes a market map, per-competitor cards, and cross-competitor patterns.

Sound good? (y/n)
```

### Step 2: Octave Context Gathering

Based on the competitor(s) selected, use Octave MCP tools to build rich competitive context. **Always tell the user what you're researching and why.**

**Call as many tools as needed to build a complete picture.** The best battlecard documents come from layering multiple sources -- competitor profiles + deal outcomes + conversation evidence + proof points all combine to create a reference grounded in real data. Don't stop at one tool when three would give you a stronger document.

**List vs Search -- when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory -- "show me all competitors" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content -- "get full competitor profiles" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found a competitor and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept -- "how do we compete on security?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need uploaded competitive intel docs or analyst reports |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

---

#### For Single Competitor Battlecard

| What you need | Tool | When to use |
|---------------|------|-------------|
| Competitor full profile | `get_entity({ oId: "<competitor_oId>" })` | Always -- the core source |
| All competitors (context) | `list_all_entities({ entityType: "competitor" })` | Quick scan of landscape around this competitor |
| Competitive positioning | `search_knowledge_base({ query: "<competitor> positioning", entityTypes: ["playbook", "competitor"] })` | Messaging angles and playbook positioning |
| Playbook with value props | `get_playbook({ oId, includeValueProps: true })` | After finding a relevant playbook -- gets differentiators |
| Your products | `list_entities({ entityType: "product" })` | Product capabilities for side-by-side comparison |
| Product deep dive | `get_entity({ oId: "<product_oId>" })` | Granular feature details for comparison |
| Competitive wins | `list_events({ startDate: "<180d ago>", filters: { eventTypes: ["DEAL_WON"], competitors: ["<oId>"] } })` | Real deal outcomes -- wins against this competitor |
| Competitive losses | `list_events({ startDate: "<180d ago>", filters: { eventTypes: ["DEAL_LOST"], competitors: ["<oId>"] } })` | Real deal outcomes -- losses to this competitor |
| Deal details | `get_event_detail({ eventOId })` | Deep dive on notable wins or losses for evidence |
| Conversation evidence | `list_findings({ query: "<competitor>", eventFilters: { competitors: ["<oId>"] } })` | Real objections and mentions from calls |
| Proof points | `list_entities({ entityType: "proof_point" })` | Competitive win proof points, switching stories |
| References | `list_entities({ entityType: "reference" })` | Customers who switched from this competitor |
| Proof points by topic | `search_knowledge_base({ query: "<competitor> win switch", entityTypes: ["proof_point", "reference"] })` | Switching and competitive win stories |
| Uploaded intel | `search_resources({ query: "<competitor>" })` | Analyst reports, competitive docs |

---

#### For Landscape Overview

| What you need | Tool | When to use |
|---------------|------|-------------|
| All competitors | `list_all_entities({ entityType: "competitor" })` | Always -- the full inventory |
| Competitor full data | `list_entities({ entityType: "competitor" })` | Full profiles for every competitor |
| Per-competitor deep dive | `get_entity({ oId })` | Detailed data for each competitor card |
| Competitive playbooks | `search_knowledge_base({ query: "competitive positioning", entityTypes: ["playbook"] })` | Cross-competitor positioning themes |
| Your products | `list_entities({ entityType: "product" })` | Product capabilities for comparison context |
| All deal outcomes | `list_events({ startDate: "<180d ago>", filters: { eventTypes: ["DEAL_WON", "DEAL_LOST"] } })` | Win rates across all competitors |
| Conversation evidence | `list_findings({ query: "competitive", startDate: "<90d ago>" })` | Cross-competitor objection patterns |
| Proof points | `list_entities({ entityType: "proof_point" })` | Competitive win stories across all |
| Uploaded intel | `search_resources({ query: "competitive landscape" })` | Analyst reports, market research docs |

---

**Output of this step:** Present a structured content brief to the user:

```
BATTLECARD OUTLINE: vs [Competitor]
====================================

Competitor: [Competitor name]
Data Sources: [N] deals analyzed, [N] conversation mentions, [N] proof points
Date Range: Last 180 days
Win Rate: [X%] ([N] wins / [N] losses)

---

SECTIONS
--------
1. Quick Positioning — one-liner + 30-second pitch
2. Competitor Overview — what they do, target, pricing, key customers
3. Where We Win — strengths table + real deal evidence
4. Where They Win — honest assessment + how to counter each
5. Objection Handlers — organized by category (pricing, feature, relationship, risk)
6. Trap Questions — discovery questions that expose weaknesses
7. Landmines to Set — evaluation criteria to plant early
8. Proof Points — switching stories, competitive wins, metrics
9. Win/Loss Scorecard — visual scoreboard with win rate and factors
10. Displacement Playbook — how to unseat them when entrenched

Octave Sources Used:
- Competitor entity: [name]
- Deals analyzed: [N] wins, [N] losses
- Conversation mentions: [N] findings
- Proof points: [N] relevant
- Playbooks: [list]

---

Does this outline look good? I can:
1. Proceed to style selection and generation
2. Add/remove sections
3. Go deeper on any area
4. Switch to landscape overview
```

**Wait for user approval before proceeding.**

### Step 3: Style Selection

Ask the user to select a visual style. Default recommendation for battlecards is `neon-pulse` (dark + neon green/cyan, high-energy) or `electric-studio` (pure black + electric blue).

```
Pick a style for your battlecard:

DARK (recommended for battlecards)
  1. neon-pulse       — Dark + neon green/cyan. High-energy. [DEFAULT]
  2. electric-studio  — Pure black + electric blue. Tech-forward.
  3. midnight-pro     — Dark navy + blue accents. Executive feel.
  4. executive-dark   — Charcoal + gold. Premium boardroom.

LIGHT
  5. swiss-modern     — White + red accent. Clean minimal.
  6. soft-light       — Warm white + sage green. Calm.
  7. paper-minimal    — Off-white + black type. Editorial.

VIBRANT
  8. solar-flare      — Deep orange gradients. Bold.
  9. aurora-gradient   — Purple-to-teal. Visionary.
  10. monochrome-bold — High-contrast B&W. Statement typography.

Your choice (number or name, or press Enter for neon-pulse):
```

If `--style` was provided via flag, skip this prompt and use that preset.

Full CSS variable definitions for each preset are in the deck skill's [STYLE_PRESETS.md](../deck/STYLE_PRESETS.md). Apply the same CSS variable system.

### Step 4: Generate HTML

Build a single, self-contained HTML file. **No external dependencies except Google Fonts.** Everything else inlined.

#### Output Directory

Save the battlecard under `.octave-decks/`:

```
.octave-decks/
└── battlecard-<competitor-kebab>-<YYYY-MM-DD>/
    └── battlecard-<competitor-kebab>.html
```

Example: `/octave:battlecard-doc --competitor "Gong"` produces `.octave-decks/battlecard-gong-2026-02-11/battlecard-gong.html`

For landscape: `.octave-decks/battlecard-landscape-2026-02-11/battlecard-landscape.html`

The entire `.octave-decks/` directory is in `.gitignore` -- nothing here gets committed.

---

#### Single Competitor -- Document Sections

**1. Header Banner**
- "vs [Competitor]" title with your product name
- Last updated date
- Data sources badges: "[N] deals | [N] calls | [N] proof points"

**2. Quick Positioning**
- "When you hear [Competitor], say..." -- highlighted callout box with brand accent border
- One-liner: single strongest differentiator
- 30-second pitch: elevator pitch positioned against this competitor

**3. Competitor Overview**
- What they do, target market, pricing, key customers, recent moves
- Card-based grid layout (2-3 columns)

**4. Where We Win**
- Comparison table: capability rows with green checkmarks (us) and red crosses (them)
- Win themes from actual deals: numbered list with quoted conversation evidence

**5. Where They Win (Be Honest)**
- Their genuine strengths listed honestly
- For each: a "How to counter/reframe" response
- Color-code: amber for their strengths, green counter callouts

**6. Objection Handlers**
- Expandable `<details>/<summary>` accordion elements
- Organized by category: Pricing, Feature, Relationship, Risk (with category badges)
- Each item: "They say X" (summary) -> "We say Y" + proof point (expanded)
- Include real conversation evidence when available

**7. Trap Questions**
- 5-8 discovery questions as numbered cards
- Each with: the question, why it works, expected response, follow-up

**8. Landmines to Set**
- Evaluation criteria to plant early that favor you
- Each with: criterion, why it matters, how it plays to your strength

**9. Proof Points**
- Customers who switched, competitive win stories, head-to-head metrics
- Card layout with metric highlights

**10. Win/Loss Scorecard**
- Visual win rate bar: CSS-based div widths (green for wins, red for losses)
- Win rate percentage displayed prominently
- Common win factors (green accent) and loss factors (red accent)

**11. Displacement Playbook**
- How to unseat entrenched competitors
- Migration story, switching cost offsets, success timeline
- Sequential step layout

---

#### Landscape Overview -- Document Sections

**1. Header** -- "Competitive Landscape" title + date + competitor count

**2. Market Map** -- Table: competitor, focus, threat level (color-coded badge), win rate mini-bar

**3. Per-Competitor Cards** -- Condensed card per competitor: name, positioning, key differentiator, top objection + counter, win rate bar. Grid layout.

**4. Cross-Competitor Patterns** -- Themes across multiple competitors, common objections, universal differentiators

---

#### HTML Architecture

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Battlecard: vs [Competitor]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from chosen style preset — see STYLE_PRESETS.md) === */
    :root { /* ... paste chosen preset variables here ... */ }

    /* === Reset & Base === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { background: var(--bg); color: var(--text-primary); font-family: var(--font-body); line-height: 1.6; }

    /* === Document Layout === */
    .doc-container { max-width: 950px; margin: 0 auto; padding: 2rem clamp(1rem, 4vw, 3rem); }

    /* === Sticky Sidebar Navigation === */
    .sidebar { position: fixed; top: 50%; transform: translateY(-50%); right: clamp(0.5rem, 2vw, 2rem); display: flex; flex-direction: column; gap: 0.25rem; z-index: 100; }
    .sidebar a { display: block; width: 8px; height: 8px; border-radius: 50%; background: var(--text-muted); transition: all 0.2s var(--ease); }
    .sidebar a.active { background: var(--brand-primary); transform: scale(1.5); }

    /* === Sections === */
    .section { margin-bottom: clamp(2rem, 4vh, 4rem); padding-top: 1rem; }
    .section-title { font-family: var(--font-display); font-size: clamp(1.25rem, 2.5vw, 1.75rem); font-weight: 600; margin-bottom: 1rem; }

    /* === Header Banner === */
    .header-banner { padding: clamp(2rem, 4vh, 4rem) 0; border-bottom: 1px solid var(--border); margin-bottom: clamp(2rem, 4vh, 3rem); }
    .header-banner h1 { font-family: var(--font-display); font-size: clamp(2rem, 4vw, 3rem); font-weight: 700; }
    .data-badge { display: inline-flex; padding: 0.25rem 0.75rem; border-radius: var(--radius-pill); background: var(--bg-card); border: 1px solid var(--border); font-size: 0.8rem; color: var(--text-secondary); }

    /* === Callout Box (Quick Positioning) === */
    .callout { padding: clamp(1rem, 2vh, 1.5rem); border-radius: var(--radius-lg); background: var(--bg-card); border-left: 4px solid var(--brand-primary); }

    /* === Cards & Grids === */
    .card { padding: clamp(1rem, 2vh, 1.5rem); border-radius: var(--radius-lg); background: var(--bg-card); border: 1px solid var(--border); }
    .card:hover { border-color: var(--border-strong); }
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }

    /* === Comparison Table === */
    .comparison-table { width: 100%; border-collapse: collapse; }
    .comparison-table th { text-align: left; padding: 0.75rem; border-bottom: 2px solid var(--border-strong); color: var(--text-secondary); font-size: 0.85rem; text-transform: uppercase; }
    .comparison-table td { padding: 0.75rem; border-bottom: 1px solid var(--border); }
    .win { color: var(--success); }
    .loss { color: var(--error); }
    .partial { color: var(--warning); }

    /* === Expandable Objection Handlers === */
    details { border: 1px solid var(--border); border-radius: var(--radius); margin-bottom: 0.5rem; }
    details[open] { border-color: var(--border-strong); }
    summary { padding: 0.75rem 1rem; cursor: pointer; background: var(--bg-card); font-weight: 500; list-style: none; }
    summary::before { content: '+'; font-family: var(--font-mono); color: var(--brand-primary); font-weight: 700; margin-right: 0.5rem; }
    details[open] summary::before { content: '-'; }
    .detail-body { padding: 1rem; border-top: 1px solid var(--border); }

    /* === Win/Loss Scorecard Bar === */
    .score-bar-container { display: flex; height: 2rem; border-radius: var(--radius); overflow: hidden; background: var(--bg-elevated); }
    .score-bar-win { background: var(--success); display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 0.8rem; }
    .score-bar-loss { background: var(--error); display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 0.8rem; }

    /* === Badges (category + threat level) === */
    .badge { display: inline-block; padding: 0.15rem 0.5rem; border-radius: var(--radius-pill); font-size: 0.7rem; font-weight: 600; text-transform: uppercase; }
    .badge-pricing { background: rgba(251, 191, 36, 0.15); color: var(--warning); }
    .badge-feature { background: rgba(59, 130, 246, 0.15); color: var(--brand-primary); }
    .badge-relationship { background: rgba(168, 85, 247, 0.15); color: #a855f7; }
    .badge-risk { background: rgba(248, 113, 113, 0.15); color: var(--error); }
    .threat-high { background: rgba(248, 113, 113, 0.15); color: var(--error); }
    .threat-medium { background: rgba(251, 191, 36, 0.15); color: var(--warning); }
    .threat-low { background: rgba(52, 211, 153, 0.15); color: var(--success); }

    /* === Step Numbers (Trap Questions, Landmines) === */
    .step-number { display: inline-flex; align-items: center; justify-content: center; width: 2rem; height: 2rem; border-radius: 50%; background: var(--brand-primary); color: var(--bg); font-weight: 700; font-size: 0.85rem; }

    /* === Responsive === */
    @media (max-width: 768px) { .grid-2, .grid-3 { grid-template-columns: 1fr; } .sidebar { display: none; } }
    @media print { .sidebar { display: none; } details { break-inside: avoid; } }
    @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
  </style>
</head>
<body>

  <nav class="sidebar" id="sidebar-nav">
    <!-- Generated by JS: one dot per section -->
  </nav>

  <div class="doc-container">

    <!-- 1. Header Banner -->
    <header class="header-banner" id="section-header">
      <p style="color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.8rem;">Competitive Battlecard</p>
      <h1>[Your Product] <span style="color: var(--text-muted);">vs</span> [Competitor]</h1>
      <div style="display: flex; gap: 0.75rem; margin-top: 1rem; flex-wrap: wrap;">
        <span class="data-badge">Updated [Date]</span>
        <span class="data-badge">[N] deals</span>
        <span class="data-badge">[N] calls</span>
        <span class="data-badge">[N] proof points</span>
      </div>
    </header>

    <!-- 2. Quick Positioning -->
    <section class="section" id="section-positioning">
      <h2 class="section-title">Quick Positioning</h2>
      <div class="callout">
        <p style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.5rem;">When you hear "[Competitor]", say:</p>
        <p style="font-size: 1.1rem; font-weight: 600;">"[One-liner]"</p>
      </div>
      <div class="card" style="margin-top: 1rem;">
        <p style="color: var(--text-secondary); font-size: 0.85rem;">30-Second Pitch</p>
        <p>"[Elevator pitch positioned against this competitor]"</p>
      </div>
    </section>

    <!-- 3. Competitor Overview (card grid) -->
    <!-- 4. Where We Win (comparison table + deal evidence) -->
    <!-- 5. Where They Win (honest strengths + counter cards) -->
    <!-- 6. Objection Handlers (details/summary accordion by category) -->
    <!-- 7. Trap Questions (numbered step cards) -->
    <!-- 8. Landmines to Set (numbered checklist) -->
    <!-- 9. Proof Points (metric cards) -->
    <!-- 10. Win/Loss Scorecard (score-bar + factor lists) -->
    <!-- 11. Displacement Playbook (sequential steps) -->

  </div>

  <script>
    // Sidebar: generate dots from .section elements
    // Intersection Observer highlights active section dot
    // Smooth scroll on dot click
    (function() {
      const sections = document.querySelectorAll('.section');
      const sidebar = document.getElementById('sidebar-nav');
      sections.forEach((section, i) => {
        const dot = document.createElement('a');
        dot.href = '#' + section.id;
        dot.title = section.querySelector('.section-title')?.textContent || '';
        if (i === 0) dot.classList.add('active');
        sidebar.appendChild(dot);
      });
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            sidebar.querySelectorAll('a').forEach(d => d.classList.remove('active'));
            const active = sidebar.querySelector('a[href="#' + entry.target.id + '"]');
            if (active) active.classList.add('active');
          }
        });
      }, { threshold: 0.3 });
      sections.forEach(s => observer.observe(s));
    })();
  </script>
</body>
</html>
```

Populate each placeholder section (`<!-- 3 -->` through `<!-- 11 -->`) with real content from the Octave context gathered in Step 2, using the component patterns shown above.

For **landscape overview** documents, replace the per-competitor sections with:
- **Market Map** -- `<table class="comparison-table">` with competitor rows, threat-level badges, and inline score bars
- **Per-Competitor Cards** -- `<div class="grid-2">` of `.card` elements, each with: name, positioning, differentiator, top objection/counter, win rate mini-bar
- **Cross-Competitor Patterns** -- themes, universal differentiators, common objections

---

#### Key HTML/CSS Principles

1. **Single page, natural scrolling** -- not a slide deck, a vertical reference document
2. **Sticky sidebar** with section navigation dots (hidden on mobile and print)
3. **Same CSS variable system as `/octave:deck`** -- apply the preset's `:root` block from STYLE_PRESETS.md
4. **Max-width 950px** centered on the page
5. **Objection handlers as `<details>/<summary>`** -- native HTML expand/collapse, no JS required
6. **Win/loss scorecard using CSS bars** -- div widths as percentages, green wins, red losses
7. **Color coding:** `--success` (green) for wins/strengths, `--error` (red) for losses/weaknesses, `--warning` (amber) for neutral
8. **Self-contained** -- all CSS inline in `<style>`, only external dependency is Google Fonts
9. **Responsive** -- grids collapse to single column below 768px
10. **Print-friendly** -- sidebar hidden, details preserved

### Step 5: Delivery

After generating the HTML file:

1. **Open the document** in the default browser
2. **Present a summary:**

```
BATTLECARD READY
================

Folder: .octave-decks/battlecard-<competitor>-<date>/
File:   .octave-decks/battlecard-<competitor>-<date>/battlecard-<competitor>.html
Style:  [Preset name]
Size:   [file size]

Competitor: [Competitor name]
Sections: [N] sections
Data sources: [N] deals, [N] conversation mentions, [N] proof points
Win rate: [X%] (last 180 days)

Navigation:
- Scroll naturally through the document
- Sidebar dots on the right track your position
- Click any dot to jump to that section
- Objection handlers: click to expand/collapse

---

Want me to:
1. Add more objection handlers
2. Go deeper on any section
3. Create displacement outreach for a specific person
4. Generate a version for a different persona
5. Create a presentation version (/octave:deck)
6. Export as PDF
7. Done
```

**If user requests PDF export:**

```
To save as PDF:
1. Open the file in your browser (should already be open)
2. Press Cmd+P (Mac) or Ctrl+P (Windows)
3. Select "Save as PDF" as the destination
4. Set margins to "Minimum" or "None" for best results
5. The sidebar navigation will be hidden in print
```

## MCP Tools Used

### Competitive Intelligence
- `list_all_entities` (competitor) -- List all competitors for selection or landscape
- `list_entities` (competitor) -- Full competitor profiles with data
- `get_entity` -- Deep dive on a specific competitor
- `search_knowledge_base` -- Competitive positioning, playbook matching, proof point discovery
- `list_findings` -- Real conversation mentions, objections, competitor references from calls
- `list_events` -- Deal win/loss outcomes against specific competitors
- `get_event_detail` -- Deep dive into specific competitive deals for evidence

### Library (Fetching / Searching)
- `get_playbook` -- Competitive playbooks with value props
- `list_value_props` -- Value propositions per playbook
- `list_entities` (product) -- Product capabilities for comparison
- `list_entities` (proof_point) -- Competitive win proof points and switching stories
- `list_entities` (reference) -- Customer references who switched from competitors
- `search_resources` -- Search uploaded analyst reports, battlecards, competitive docs

### Intelligence & Signals
- `list_findings` -- Conversation-based competitive insights and objection patterns
- `list_events` -- Deal stage changes, win/loss events with competitor filters
- `get_event_detail` -- Full details on specific competitive deals

## Error Handling

**No Competitors in Library:**
> No competitors found in your library.
>
> To build a battlecard, I need at least one competitor in your Octave library.
>
> Options:
> 1. Add a competitor first: `/octave:library create competitor`
> 2. Tell me the competitor name and I'll create a basic comparison from web research (limited data)

**No Deal Data for This Competitor:**
> No win/loss data found against [Competitor] in the last 180 days.
>
> I'll build the battlecard from library data, conversation mentions, and positioning. The win/loss scorecard and deal evidence sections will be limited.
>
> As you log deals with this competitor tagged, the battlecard will get richer with real evidence.

**Competitor Not in Library:**
> "[Name]" isn't in your competitor library yet.
>
> Options:
> 1. Create the competitor entity first: `/octave:library create competitor "[name]"`
> 2. I'll generate a basic battlecard from available information (playbooks, conversations, web research)

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The battlecard builder needs Octave data to generate competitive intelligence. Without it, I can't pull competitor profiles, deal outcomes, or conversation evidence.
>
> To reconnect: check your MCP configuration or run `/octave:workspace status`

**No Conversation Evidence:**
> No conversation mentions found for [Competitor].
>
> The objection handlers and trap questions will be based on library data and general competitive positioning rather than real conversation evidence. They'll improve as your team logs more calls where this competitor comes up.

## Related Skills

- `/octave:battlecard` -- Text-based competitive intelligence (this is the visual version)
- `/octave:brief` -- Account-focused dossier (when dealing with a specific account in a competitive deal)
- `/octave:deck` -- Competitive presentation for an audience (this is a reference doc)
- `/octave:wins-losses` -- Text-based win/loss analysis across competitors
- `/octave:campaign` -- Competitive campaign content and displacement outreach
- `/octave:research` -- Deep account research (feeds into account-specific competitive context)
- `/octave:insights` -- Surface competitive mentions from conversations
