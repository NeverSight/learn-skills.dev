---
name: ui-workflow
description: Full UI design pipeline. Wireframes first, then a design PRD, optional Stitch MCP mockups, shadcn/ui components, an anti-vibe-code checklist, explicit interaction states, and a browser-based visual feedback loop.
when_to_use: When building any UI, including pages, components, dashboards, landing pages, or visual interfaces.
---

# UI Design Workflow

Follow this pipeline for any project involving UI. Steps 0, 1, 3, and everything under Best Practices need no external tooling. Step 2 is optional and depends on an MCP server you may not have installed.

## Step 0: Structural Wireframing (ASCII First)

- Before any visual design, produce ASCII wireframes for each screen or layout.
- This forces structural thinking (hierarchy, sections, flow) before aesthetics.
- Present wireframes for approval before moving to the PRD.

## Step 1: PRD Creation

- Write the design PRD **before writing any UI code**.
- Save it to wherever the project keeps planning docs, for example `docs/design/prd-design.md`.
- The PRD must include:
  - Page and screen inventory with clear names and purposes
  - Layout structure (grid, sections, hierarchy)
  - Component breakdown (buttons, forms, cards, navs, modals)
  - Color palette, typography, spacing system
  - Responsive behavior (breakpoints, mobile-first rules)
  - Interaction states (hover, active, disabled, loading, error, empty)
  - Accessibility requirements (contrast, aria, keyboard nav)
  - Data flow per screen (what data populates what)
- Format the PRD with tables, bullet lists, and clear headings. No ambiguity.

If you also have a dedicated design-direction skill installed (Anthropic's `frontend-design` plugin skill, or any house equivalent), invoke it here to set aesthetic direction before the PRD is written.

## Step 2: Mockup Generation (optional, via Stitch MCP)

Skip this step entirely if you do not use [Google Stitch](https://stitch.withgoogle.com/). Hand-built HTML mockups or any other design tool substitute fine; the rest of the pipeline does not depend on it.

With the Stitch MCP server connected:

- Use `generate_screen_from_text` to generate mockup screens from the PRD, one screen per screen defined in the PRD.
- Use `extract_design_context` on a finished screen to pull design tokens (palette, fonts, layout patterns), then feed that context into the next generation so every screen matches.
- Use `fetch_screen_code` to retrieve the production HTML and CSS.

### Stitch MCP setup

The server is the community `stitch-mcp` npm package. It talks to Google Stitch using your own Google Cloud credentials, so it is per-user setup, not per-project.

1. Create or pick a Google Cloud project and enable the Stitch API:

   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   gcloud auth application-default set-quota-project YOUR_PROJECT_ID
   gcloud beta services mcp enable stitch.googleapis.com
   ```

2. Install application default credentials so the server can authenticate as you:

   ```bash
   gcloud auth application-default login
   ```

3. Register the server with Claude Code:

   ```bash
   claude mcp add stitch --scope user -e GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID -- npx -y stitch-mcp
   ```

   Or add the equivalent block by hand to your MCP config:

   ```json
   {
     "mcpServers": {
       "stitch": {
         "command": "npx",
         "args": ["-y", "stitch-mcp"],
         "env": { "GOOGLE_CLOUD_PROJECT": "YOUR_PROJECT_ID" }
       }
     }
   }
   ```

Replace `YOUR_PROJECT_ID` with your own Google Cloud project ID. Never hardcode credentials into the config; the `gcloud auth application-default login` step is what supplies them.

## Step 3: Integration

- Use the generated code and design context as the foundation for the project UI.
- Maintain consistency across all screens by referencing the extracted design tokens.
- Any deviation from the PRD must be noted and justified.

---

# UI Best Practices

## Use shadcn/ui Components, Never Invent Primitives

- **Always** use `shadcn/ui` components for buttons, dialogs, cards, inputs, selects, tabs, and similar primitives.
- Never create a custom primitive when a shadcn equivalent exists.
- Add components via CLI: `npx shadcn@latest add button card dialog`
- If the project has not initialized shadcn yet, run `npx shadcn@latest init` first.
- Setup details and the component catalog live at [ui.shadcn.com](https://ui.shadcn.com/docs).

## Build and Reference Design Tokens

- Encode all colors, spacing, typography, radii, and shadows as CSS custom properties (design tokens).
- Store tokens in `globals.css` using the shadcn and Tailwind v4 pattern (`--primary`, `--background`, and so on).
- Reference tokens by name in prompts: "style this card using the `--primary` and `--card` tokens".
- Multiple themes become trivial once tokenized. Swap token values, nothing else.
- Use OKLCH color format for perceptual uniformity (the shadcn default).

## Critique-Then-Redesign Pattern

Claude is better at **redesigning** than at designing from scratch. Follow this loop:

1. Build a first pass. It does not need to look great.
2. Run: "Critique the design of [component/page]. List every issue."
3. Run: "Redesign [component/page], fixing all critique items."
4. The critique gives Claude specific context for a much better second pass.

## Visual Feedback Loop

- After generating UI code, render it in a real browser and look at the result. A browser automation MCP such as [Playwright MCP](https://github.com/microsoft/playwright-mcp) (`browser_snapshot`, `browser_take_screenshot`) does this well; install it with `claude mcp add playwright -- npx -y @playwright/mcp@latest`.
- Compare rendered output against the PRD and the design tokens.
- Fix discrepancies in a tight build, check, fix loop.
- This closes the gap between "code that looks right" and "UI that actually looks right".

## Feed Reference Screenshots

- When starting a new UI project, gather 2 to 5 screenshots of sites or apps whose design you admire.
- Ask Claude to break down each screenshot: layout, components, colors, typography, spacing.
- Cherry-pick the features you want and discard the rest.
- Feed the selected design features into the PRD and the design tokens.

## Specify All Interaction States

Every interactive element must have these states defined explicitly:

- **Default**, the resting appearance
- **Hover**, cursor over
- **Active/Pressed**, during click or tap
- **Focus**, keyboard navigation
- **Disabled**, non-interactive
- **Loading**, async operation in progress
- **Error**, validation failure
- **Empty**, no data or zero state

---

# Anti-Vibe-Code Checklist

Audit every screen against this list before shipping. These are the telltale signs of AI-generated UI.

**Icons & Emojis**
- Never use emojis as UI icons. They scream vibe-coded. Use Phosphor Icons (preferred), Lucide, or similar.
- Never use AI-selected decorative icons (colorful circles, gradient blobs). Use purposeful, monochrome interface icons.

**Colors**
- Never let AI choose colors. It always picks bright, clashing palettes.
- Introduce color through data visualizations (charts, sparklines), not through buttons and decorative icons.
- Muted, cohesive palettes with one dominant color plus one sharp accent.

**Layout & Information Architecture**
- Never let AI choose your layout. Human intervention gives the biggest ROI here.
- Eliminate redundant KPI cards. One instance per metric, maximum.
- Tighten sidebar spacing and left-align navigation items.
- Replace gradient profile avatar circles with proper account cards.
- Tuck secondary or rare links into popovers (click to reveal).
- Collapse busy action buttons into triple-dot overflow menus.
- Group related settings together (settings plus billing plus usage).

**Forms & Modals**
- If a form or flyout has few fields and lots of empty space, use a modal instead of a full page.
- Collapse advanced options by default. Show only core fields initially.
- Design layouts that let new features slot in easily. Tabs beat static sections.

**Pricing Pages**
- Maximum 3 to 4 pricing tiers. Five or more is confusing and screams AI-generated.
- Show actual discount amounts prominently, not just "save X%".
- Make price the largest text element, not the plan name.
- Follow proven SaaS pricing patterns (Resend, Supabase, Vercel).

**Landing Pages**
- Never ship a landing page with just text and generic icons. You need real graphics.
- Use actual product screenshots with perspective transforms (skew, rotation).
- Replace generic feature icons with cropped screenshots of the actual feature.

**Low-Hanging Fruit**
- Add data comparison toggles, for example splitting a chart into individual items.
- Add informational icons with color splashes in data rows.
- Replace boring bar charts with richer visualizations (maps, donut charts, sparklines).

## Keep the Codebase Clean

- Messy code degrades Claude's ability to produce good UI suggestions.
- Before starting new UI work, audit existing code for inefficiencies and dead code.
- Fix structural issues first. Clean code leads to better emergent UI output.

## HTML Style Guides as References

- For rapid style exploration, generate pure HTML single-file style guides with no build step.
- Use these as a visual library Claude can reference: "match the style from [guide name]".
