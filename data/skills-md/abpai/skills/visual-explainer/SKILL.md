---
name: visual-explainer
description: Generate beautiful, self-contained HTML pages that visually explain systems, code changes, plans, and data. Use when the user asks for a diagram, architecture overview, diff review, plan review, project recap, comparison table, or any visual explanation of technical concepts. Also use proactively when you are about to render a complex ASCII table (4+ rows or 3+ columns) — present it as a styled HTML page instead.
license: MIT
compatibility: Requires a browser to view generated HTML files. Optional surf-cli for AI image generation.
metadata:
  author: nicobailon
  version: "0.5.2"
---

# Visual Explainer

Generate self-contained HTML files for technical diagrams, visualizations, and data tables. Always open the result in the browser. Never fall back to ASCII art when this skill is loaded.

**Visuals are required.** When this skill is loaded, the output must contain at least one primary visual artifact that carries real information, not just decorative styling around prose. Valid primary visuals include:
- an architecture, flow, sequence, state, ER, or dependency diagram
- a timeline, roadmap, or execution path visual
- a dashboard or KPI band with charts, bars, or status visual encoding
- a semantic HTML table for comparisons, audits, or inventories
- a walkthrough strip, stepper, or before/after comparison layout

If the page is a report, review, recap, audit, or plan analysis, include **at least two visual forms**:
- one structural visual: diagram, flow, architecture map, timeline, or dependency view
- one evidence visual: table, KPI dashboard, comparison panel, heatmap-style status grid, or other compact evidence display

Pure prose sections, even if well-designed, do not satisfy this requirement.

**Proactive table rendering.** When you're about to present tabular data as an ASCII box-drawing table in the terminal (comparisons, audits, feature matrices, status reports, any structured rows/columns), generate an HTML page instead. The threshold: if the table has 4+ rows or 3+ columns, it belongs in the browser. Don't wait for the user to ask — render it as HTML automatically and tell them the file path. You can still include a brief text summary in the chat, but the table itself should be the HTML page.

## Workflow

### 1. Think (5 seconds, not 5 minutes)

Before writing HTML, commit to a direction. Don't default to "dark theme with blue accents" every time.

**Who is looking?** A developer understanding a system? A PM seeing the big picture? A team reviewing a proposal? This shapes information density and visual complexity.

**What type of diagram?** Architecture, flowchart, execution flow, code flow, sequence, data flow, schema/ER, state machine, mind map, data table, walkthrough, timeline, or dashboard. Each has distinct layout needs and rendering approaches (see Diagram Types below).

**What aesthetic?** Pick one and commit:
- Monochrome terminal (green/amber on black, monospace everything)
- Editorial (serif headlines, generous whitespace, muted palette)
- Blueprint (technical drawing feel, grid lines, precise)
- Neon dashboard (saturated accents on deep dark, glowing edges)
- Paper/ink (warm cream background, hand-drawn feel, sketchy borders)
- Hand-drawn / sketch (Mermaid `handDrawn` mode, wiggly lines, informal whiteboard feel)
- IDE-inspired (borrow a real color scheme: Dracula, Nord, Catppuccin, Solarized, Gruvbox, One Dark)
- Data-dense (small type, tight spacing, maximum information)
- Gradient mesh (bold gradients, glassmorphism, modern SaaS feel)

Vary the choice each time. If the last diagram was dark and technical, make the next one light and editorial. The swap test: if you replaced your styling with a generic dark theme and nobody would notice the difference, you haven't designed anything.

### 2. Structure

**Read the reference template** before generating. Don't memorize it — read it each time to absorb the patterns.
- For flowcharts, sequence diagrams, ER, state machines, mind maps: read `./templates/mermaid-flowchart.html`
- For data tables, comparisons, audits, feature matrices: read `./templates/data-table.html`
- For interactive step-through walkthroughs, tutorials, concept explanations: read `./templates/walkthrough.html`
- For dashboards, KPI summaries, metrics overviews: read `./templates/dashboard.html`
- For timelines, roadmaps, milestone tracking: read `./templates/timeline.html`
- For text-heavy architecture diagrams, or hybrid pattern (Mermaid overview + detail cards): read `./templates/architecture.html`
- For non-editorial aesthetics, also read `./references/aesthetic-palettes.md` for ready-made palettes.

**For CSS/layout patterns and SVG connectors**, read `./references/css-patterns.md`.

**For pages with 4+ sections** (reviews, recaps, dashboards), also read the "Section Navigation" section in `./references/css-patterns.md` for sticky sidebar TOC on desktop and horizontal scrollable bar on mobile.

**Choosing a rendering approach:**

| Diagram type | Approach | Why |
|---|---|---|
| Execution flow / code flow | **Excalidraw pipeline (required)** | These are flowcharts in practice; Excalidraw output is clearer and less cluttered |
| Flowcharts (`flowchart`/`graph`) | **Excalidraw pipeline** | Cleaner hand-drawn output: Mermaid text -> `@excalidraw/mermaid-to-excalidraw` -> Excalidraw SVG export |
| Other Mermaid diagrams (sequence, ER, state, mind map, data flow) | **Mermaid** | Broader syntax support where Excalidraw conversion is limited |
| Architecture (text-heavy) | CSS Grid cards + flow arrows | Rich card content (descriptions, code, tool lists) needs CSS control. See `templates/architecture.html` |
| Architecture (hybrid, 15+ elements) | Mermaid overview + CSS Grid detail cards | Simplified 5-8 node Mermaid for the big picture, then detail cards below. See hybrid pattern in `templates/architecture.html` |
| Data table | HTML `<table>` | Semantic markup, accessibility, copy-paste behavior |
| Walkthrough / tutorial | Vanilla JS step-through | Progressive disclosure with visual + text per step |
| Timeline | CSS (central line + cards) | Simple linear layout doesn't need a layout engine |
| Dashboard | CSS Grid + inline SVG | Card grid with sparklines and progress bars |

**Report composition rule.** For reports, reviews, recaps, audits, and plan explainers, do not build a page that is mostly stacked text cards. Start by choosing the visual anchor first, then add supporting sections around it. The default shape is:
1. one hero visual near the top
2. one compact evidence section near the top half of the page
3. prose only after the visual model is established

**Visual anchor rule.** Put the main diagram, timeline, walkthrough, or dashboard in the first screenful when possible. If the most important thing on load is a paragraph, the page is under-visualized.

**Visual fallback ladder.** If the ideal diagram type is blocked by missing data or rendering limits, downgrade to the next best visual form instead of dropping to prose:
1. Excalidraw flowchart or Mermaid diagram
2. CSS architecture map / walkthrough / timeline
3. KPI dashboard plus semantic table
4. before/after comparison panels

Never skip the visual entirely.

For code-heavy pages (reviews, architecture docs), add Prism.js for syntax highlighting (see `libraries.md`).

**Mermaid theming (fallback path):** Use `theme: 'base'` with custom `themeVariables` so colors match your page palette. Use `look: 'classic'` unless the user asks for sketch style. Use `layout: 'elk'` for complex graphs (requires `@mermaid-js/layout-elk` — see `./references/libraries.md`). Override Mermaid SVG classes with CSS for pixel-perfect control.

**Mermaid zoom controls:** Always add zoom controls (+/−/reset buttons) to every `.mermaid-wrap` container. Complex diagrams render at small sizes and need zoom to be readable. Include Ctrl/Cmd+scroll zoom on the container. Prefer CSS `zoom` over `transform: scale()` for static base scaling — see CSS Zoom section in `css-patterns.md`. See the zoom controls pattern in `./references/css-patterns.md` and the reference template at `./templates/mermaid-flowchart.html`.

**AI-generated illustrations (optional).** If [surf-cli](https://github.com/nicobailon/surf-cli) is available, generate images via `surf gemini "prompt" --generate-image /tmp/ve-img.png --aspect-ratio 16:9`, base64 encode, and embed as data URIs. Check with `which surf`; skip gracefully if unavailable. See `./references/css-patterns.md` for image container styles.

### 3. Style

Apply these principles to every diagram:

**Typography is the diagram.** Pick a font pairing from the 5 named pairings in `libraries.md` and commit to it for the page:

1. **DM Sans + Fira Code** — clean, modern, distinctive (recommended default)
2. **Instrument Serif + JetBrains Mono** — refined editorial
3. **IBM Plex Sans + IBM Plex Mono** — technical, professional
4. **Bricolage Grotesque + Fragment Mono** — bold, characterful
5. **Plus Jakarta Sans + Azeret Mono** — rounded, approachable

**Editorial default (Threaded/Medium-style):** When the request asks for Medium/editorial aesthetics, default to Merriweather (content/heading) + Inter (UI/meta), slate-heavy palette, generous line-height, and restrained borders.

**Forbidden as generic primary body font:** Roboto, Arial, Helvetica. These are invisible defaults — they say "no design decision was made." Use only as system fallbacks in the `font-family` stack.

Load via `<link>` in `<head>`. Include a system font fallback in the `font-family` stack for offline resilience. The heading font should always have character — if you swapped it for Arial and nobody noticed, you haven't designed anything.

**Color tells a story.** Use CSS custom properties for the full palette. Define at minimum: `--bg`, `--surface`, `--border`, `--text`, `--text-dim`, and 3-5 accent colors. Each accent should have a full and a dim variant (for backgrounds). Name variables semantically when possible (`--pipeline-step` not `--blue-3`). Support both themes. Put your primary aesthetic in `:root` and the alternate in the media query:

```css
/* Light-first (editorial, paper/ink, blueprint): */
:root { /* light values */ }
@media (prefers-color-scheme: dark) { :root { /* dark values */ } }

/* Dark-first (neon, IDE-inspired, terminal): */
:root { /* dark values */ }
@media (prefers-color-scheme: light) { :root { /* light values */ } }
```

**Surfaces whisper, they don't shout.** Build depth through subtle lightness shifts (2-4% between levels), not dramatic color changes. Borders should be low-opacity rgba (`rgba(255,255,255,0.08)` in dark mode, `rgba(0,0,0,0.08)` in light) — visible when you look, invisible when you don't.

**Backgrounds create atmosphere.** The editorial default is flat white (`#ffffff`) — whitespace IS the atmosphere. For dark-first aesthetics, use subtle gradients or faint grid patterns. The background should feel intentional, not accidental.

**Visual weight signals importance.** Not every section deserves equal visual treatment. Executive summaries and key metrics should dominate the viewport on load (larger type, more padding, subtle accent-tinted background zone). Reference sections (file maps, dependency lists, decision logs) should be compact and stay out of the way. Use `<details>/<summary>` for sections that are useful but not primary — the collapsible pattern is in `./references/css-patterns.md`.

**Surface depth creates hierarchy.** Vary card depth to signal what matters. Hero sections get elevated shadows and accent-tinted backgrounds (`ve-card--hero` pattern). Body content stays flat (default `.ve-card`). Code blocks and secondary content feel recessed (`ve-card--recessed`). See the depth tiers in `./references/css-patterns.md`. Don't make everything elevated — when everything pops, nothing does.

**Links are explicit.** Never rely on browser default link colors. Style all `<a>` elements with `color: var(--accent)` and keep underlines. See the Link Styling section in `css-patterns.md`.

**Animation earns its place.** Use staggered `fadeUp` for cards, `fadeScale` for KPIs and badges, `countUp` for hero numbers. Always respect `prefers-reduced-motion`. CSS transitions and keyframes handle all cases.

**Forbidden visual defaults** — these make every AI-generated page look the same:
- **Colors** (as accent/primary in Mermaid themeVariables or CSS): `#8b5cf6`, `#7c3aed`, `#6366f1` (indigo/violet — the Tailwind "AI purple"); `#06b6d4`, `#22d3ee` (cyan — overused in dark-mode AI dashboards); `#ec4899`, `#f472b6` (magenta/pink — the gradient mesh cliche)
- **Effects**: Animated glowing shadows on cards; emoji as section headers or bullet points; three-dot code chrome (`...` buttons at the top of fake code windows); gradient text for headings
- **Layouts**: Uniform card grids where every card is the same size and weight — vary depth tiers; symmetric everything — visual weight should follow information hierarchy; identical spacing between all sections — hero sections get more breathing room

**Prose quality** — prose in generated pages must not read like AI wrote it:
- Forbidden vocabulary: delve, crucial, pivotal, landscape (abstract), tapestry, testament, intricate, interplay, leverage, utilize, facilitate, showcase, underscore, foster, Additionally. Replace with plain equivalents.
- No promotional language ("boasts", "renowned", "groundbreaking"), significance inflation, pseudo-profound flourishes, or generic conclusions ("The future looks bright").
- No filler phrases ("It's important to note", "In order to"), rule of three, inline-header bold lists as the only structural element, em dash overuse (>1 per paragraph), or contrastive negation ("Not just X, but Y").
- Be specific: numbers, file paths, function names — not "various components." Use short words: "use" not "utilize." Vary sentence rhythm. State what happened, not what it "represents."

### 4. Deliver

**Default to one file.** The ideal output is one self-contained HTML file that includes the visuals, narrative, styling, and any lightweight interactivity in a single deliverable.

**Output location:** Write to `~/.agent/diagrams/`. Use a descriptive filename based on content: `modem-architecture.html`, `pipeline-flow.html`, `schema-overview.html`. The directory persists across sessions.

**If multiple files are truly needed, make one main file.** The main HTML file must:
- open cleanly on its own
- explain what the companion files are for
- link to every companion file with obvious labels
- act as the index/entry point you open in the browser and share with the user

Do not generate a loose set of sibling files with no clear starting page.

**Open in browser:**
- macOS: `open ~/.agent/diagrams/filename.html`
- Linux: `xdg-open ~/.agent/diagrams/filename.html`

**Tell the user** the file path so they can re-open or share it.

**In the chat response, name the visuals you included.** Example: "Created a report with an execution flow diagram and a risk table at `~/.agent/diagrams/foo.html`." This makes the visual output explicit and nudges future runs away from prose-only reports.

If companion files were generated, name the main file first and mention that it links to the supporting files.

## Diagram Types

### Mermaid Diagrams (Flowcharts, Execution/Code Flows, Sequences, ER, State Machines, Mind Maps, Data Flow)

**Use Excalidraw for flowcharts first.** For `flowchart`/`graph` syntax, convert Mermaid text to Excalidraw and render exported SVG. This is the default because it produces cleaner, less AI-looking diagrams.

**Execution/code flows are flowcharts.** Command pipelines, runtime execution paths, pre-commit chains, CI/CD step maps, and function call flow summaries should use this Excalidraw flowchart path.

**Use Mermaid for non-flowchart types.** Sequence, ER, state, mind map, and data-flow diagrams should use Mermaid directly (or fallback to Mermaid if Excalidraw conversion fails).

**`stateDiagram-v2` label caveat:** Transition labels have a strict parser — colons, parentheses, `<br/>`, HTML entities, and most special characters cause silent parse failures. If your labels need special characters, use `flowchart LR` instead with rounded nodes and quoted edge labels (`|"label text"|`).

### Architecture / System Diagrams

**Topology-focused** (connections matter more than card content): Use Mermaid. **Text-heavy overviews** (card content matters more than connections): CSS Grid with explicit row/column placement. Sections as rounded cards with colored borders. Vertical flow arrows between sections. Use when cards need descriptions, code references, tool lists, or other rich content that Mermaid nodes can't hold.

### Data Tables / Comparisons / Audits
Use a real `<table>` element — not CSS Grid pretending to be a table. Tables get accessibility, copy-paste behavior, and column alignment for free. The reference template at `./templates/data-table.html` demonstrates all patterns.

**Use proactively.** Any time you'd render an ASCII box-drawing table in the terminal, generate an HTML table instead. This includes: requirement audits, feature comparisons, status reports, configuration matrices, test result summaries, dependency lists, permission tables, API endpoint inventories.

### Walkthrough / Tutorial

Interactive step-through for progressive disclosure of concepts, processes, or tutorials. Each step has a visual element and explanatory text. Navigation via prev/next buttons, clickable dots, and keyboard arrows. The reference template at `./templates/walkthrough.html` demonstrates the pattern — vanilla JS, no framework dependencies.

### Timeline / Roadmap Views
Vertical or horizontal timeline with a central line (CSS pseudo-element). Phase markers as circles on the line. Content cards branching left/right. Date labels on the line. Color progression from past (muted) to future (vivid).

### Dashboard / Metrics Overview
Card grid layout. Hero numbers large and prominent. Sparklines via inline SVG `<polyline>`. Progress bars via CSS `linear-gradient`. KPI cards with trend indicators.

## File Structure

Every diagram is a single self-contained `.html` file. No external assets except CDN links (fonts, optional libraries). Structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Descriptive Title</title>
  <link href="https://fonts.googleapis.com/css2?family=...&display=swap" rel="stylesheet">
  <style>
    /* CSS custom properties, theme, layout, components — all inline */
  </style>
</head>
<body>
  <!-- Semantic HTML: sections, headings, lists, tables, inline SVG -->
  <!-- No script needed for static CSS-only diagrams -->
  <!-- Optional: <script> for Mermaid or interactive walkthroughs -->
</body>
</html>
```

## Quality Checks

Before delivering, verify:
- **Visual minimum met** (see requirements above).
- **First screen test**: Without scrolling, can the reader already see a meaningful visual model of the subject?
- **Single-file preference respected**: If you generated more than one file, there was a real reason, and the main file links to each supporting file.
- **Both themes**: Toggle your OS between light and dark mode. Both should look intentional, not broken.
- **Information completeness**: Does the diagram actually convey what the user asked for? Pretty but incomplete is a failure.
- **No overflow**: Resize the browser to different widths. No content should clip or escape its container. Every grid and flex child needs `min-width: 0`. Side-by-side panels need `overflow-wrap: break-word`. See the Overflow Protection section in `./references/css-patterns.md`.
- **File opens cleanly**: No console errors, no broken font loads, no layout shifts.
- **Squint test**: Blur your eyes or zoom the browser to 25%. The visual hierarchy should still be obvious — hero sections dominate, reference material recedes, section boundaries are clear. If everything blurs into the same weight, the depth tiers aren't working.
- **Print-friendly**: Cmd+P should produce a clean PDF. See `css-patterns.md` for print styles.

## Constraints

Hard rules — not guidelines. Violating these creates broken or unusable output.

- **Max 15 Mermaid nodes per diagram** (soft target 10-12). Beyond this, use `subgraph` to group, split into multiple diagrams, or use the hybrid pattern (simplified Mermaid overview + CSS Grid detail cards). For systems with 15+ elements, the hybrid pattern in `templates/architecture.html` is preferred.
- **Prefer `flowchart TD` for 5+ nodes.** Top-down vertical flow reads naturally and scales on narrow viewports. Use `flowchart LR` only for simple 3-4 node linear flows.
- **Section navigation required for pages with 4+ sections.** Read the Section Navigation section in `css-patterns.md` and include the TOC. Long pages without navigation are hostile to readers.
- **Pagination or virtual scroll for tables with 50+ rows.** Either paginate (show 25 at a time with prev/next) or truncate with a "Show all" toggle. Large DOM tables are slow and unusable.
- **Never exceed 1000 lines of HTML.** If approaching this, split into multiple pages or collapse secondary sections with `<details>`.
- **Never use `innerHTML` with user-provided content.** Use `textContent` or DOM APIs. This prevents XSS in interactive elements.
- **Maximum 5 KPI cards in a row.** More than 5 gets cramped. Use a second row or collapse less important metrics.
- **Test Mermaid syntax separately.** If the diagram is complex (10+ nodes), validate the Mermaid syntax in isolation before embedding. A broken diagram = a broken page.
- **Report pages must not be prose-dominant.** If more than half of the main sections are plain narrative cards with no visual encoding, redesign the page.
- **Do not split output across multiple files unless needed.** If you do, one main HTML file must link to all companion files and serve as the clear entry point.

