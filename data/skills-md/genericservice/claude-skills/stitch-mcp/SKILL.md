---
name: stitch-mcp
description: Design and build UIs with Google Stitch using @_davideast/stitch-mcp as the proxy and CLI. Covers screen generation, editing, variants, design systems, site building, prompt engineering, and the DESIGN.md spec. Updated for Stitch's March 2026 infinite canvas, 4-mode AI, and first-class design systems.
version: 3.1.0
---

# Stitch MCP

You are an expert Design Systems Lead and Prompt Engineer for **Google Stitch**. You help users create high-fidelity, consistent UI designs by bridging vague ideas and precise design specifications through Stitch's AI-powered design tools.

This skill uses a hybrid approach:
- **`@_davideast/stitch-mcp` (Primary for Agents):** A developer-focused CLI and MCP proxy. This is the **preferred tool for AI agents** as it provides high-level "virtual tools" for local serving, site scaffolding (Astro), and asset management.
- **`@google/stitch-sdk` (Official Engine):** The official programmatic library from Google Labs. Use this for writing custom Node.js scripts or building Stitch capabilities into your own applications.
- **Direct Stitch HTTP MCP:** A direct connection for basic agent tool access when local CLI proxying isn't available.

### Tooling Comparison

| Feature | `@_davideast/stitch-mcp` | `@google/stitch-sdk` |
| :--- | :--- | :--- |
| **Primary Audience** | AI Coding Agents (Claude, Gemini) | Application Developers |
| **Local Serving** | Yes (`serve` command) | No |
| **Site Scaffolding** | Yes (`site` command) | No |
| **Virtual Tools** | Yes (`build_site`, `get_screen_code`) | No (raw API only) |
| **Auth** | OAuth Wizard (`init`) | API Key / Manual |

**Recommendation:** For agent-driven development and local build loops, always use **`@_davideast/stitch-mcp`**. It acts as the bridge that allows agents to "see" and "build" with your Stitch designs locally. Use the SDK only if you are writing a custom application that needs to call the Stitch API programmatically.

## Setup

### MCP Connection (for agent tool access)

Add the Stitch MCP server with your API key. For Claude Code:

```bash
claude mcp add stitch -s user --transport http "https://stitch.googleapis.com/mcp" \
  --header "X-Goog-Api-Key: your-api-key"
```

For other MCP clients (Cursor, VS Code, Gemini CLI):

```json
{
  "mcpServers": {
    "stitch": {
      "url": "https://stitch.googleapis.com/mcp",
      "headers": { "X-Goog-Api-Key": "your-api-key" }
    }
  }
}
```

### Authentication

**API key (simplest):**
```bash
export STITCH_API_KEY="your-api-key"
```
Get your key from [Stitch Settings](https://stitch.withgoogle.com/settings).

**OAuth (guided wizard):**
```bash
pnpx @_davideast/stitch-mcp init
```
Handles gcloud installation, OAuth, credentials, and MCP client config in one command.

### Verify Setup

```bash
pnpx @_davideast/stitch-mcp doctor --verbose
```

---

## Quick Reference

| Intent | Approach | Command/Tool |
|:---|:---|:---|
| List projects | CLI | `pnpx @_davideast/stitch-mcp view --projects` |
| Browse screens | CLI | `pnpx @_davideast/stitch-mcp view --project <id>` |
| Preview screens locally | CLI | `pnpx @_davideast/stitch-mcp serve -p <id>` |
| Build an Astro site | CLI | `pnpx @_davideast/stitch-mcp site -p <id>` |
| Generate a screen | MCP tool | `generate_screen_from_text` |
| Edit a screen | MCP tool | `edit_screens` |
| Generate variants | MCP tool | `generate_variants` |
| Get screen HTML | Virtual tool | `get_screen_code` |
| Get screen image | Virtual tool | `get_screen_image` |
| Build site from screens | Virtual tool | `build_site` |
| Create design system | MCP tool | `create_design_system` |
| Any MCP tool via CLI | CLI | `pnpx @_davideast/stitch-mcp tool <name>` |

---

## Platform Overview (March 2026)

Stitch uses an **AI-native infinite canvas** where multiple assets (images, text, code, UI screens) coexist in one workspace.

- **4 AI generation modes** via `modelId`:
  - `GEMINI_3_FLASH` -- Fast generation, lower cost (default for iteration)
  - `GEMINI_3_1_PRO` -- Highest quality, best for final screens
  - `GEMINI_3_PRO` -- **Deprecated**. Do not use.
- **5 screens generated simultaneously** per prompt
- **Design systems are first-class** -- create, update, list, and apply via MCP tools
- **Variant generation** -- explore alternatives with creative range control
- **Device types**: `DESKTOP`, `MOBILE`, `TABLET`, `AGNOSTIC`
- **Daily credit system** for generation usage

---

## CLI Commands

The CLI gives agents bash-level access without depending on MCP tool availability. Use `--json` flags for machine-readable output.

### Browse Projects and Screens

```bash
# Interactive browser (human)
pnpx @_davideast/stitch-mcp view --projects

# Inspect a screen
pnpx @_davideast/stitch-mcp view --project <project-id> --screen <screen-id>
```

### Preview Screens Locally

```bash
# Start a Vite dev server with all project screens
pnpx @_davideast/stitch-mcp serve -p <project-id>

# Agent-friendly: list screens as JSON without starting server
pnpx @_davideast/stitch-mcp serve -p <project-id> --list-screens

# Agent-friendly: start server and output JSON with URLs
pnpx @_davideast/stitch-mcp serve -p <project-id> --json
```

### Build an Astro Site from Screens

```bash
# Interactive route builder (human)
pnpx @_davideast/stitch-mcp site -p <project-id>

# Agent-friendly: list screens with suggested routes
pnpx @_davideast/stitch-mcp site -p <project-id> --list-screens

# Agent-friendly: generate site with explicit routes
pnpx @_davideast/stitch-mcp site -p <project-id> --routes '[
  {"screenId": "abc123", "route": "/"},
  {"screenId": "def456", "route": "/about"}
]'
```

### Invoke Any MCP Tool from CLI

```bash
# List all available tools
pnpx @_davideast/stitch-mcp tool

# See a tool's schema
pnpx @_davideast/stitch-mcp tool generate_screen_from_text -s

# Call a tool with data
pnpx @_davideast/stitch-mcp tool create_project -d '{"title": "My App"}'

pnpx @_davideast/stitch-mcp tool generate_screen_from_text -d '{
  "projectId": "123456",
  "prompt": "A modern dashboard with stat cards and activity chart",
  "deviceType": "DESKTOP"
}'
```

---

## MCP Tools (via SDK or proxy)

The official `@google/stitch-sdk` provides a `stitchTools()` helper that exposes the same core tools as the proxy. Proxy-based tools include additional "virtual tools" for simplified asset downloading.

### Standard Stitch Tools

**Project management:**
- `create_project` -- Create a new project. Args: `{ title }`
- `get_project` -- Get project details. Args: `{ name: "projects/<id>" }`
- `list_projects` -- List all projects. Args: `{}` or `{ filter: "view=owned" }`

**Screen management:**
- `list_screens` -- List screens in a project. Args: `{ projectId }`
- `get_screen` -- Get screen details + download URLs. Args: `{ name, projectId, screenId }`

**Generation:**
- `generate_screen_from_text` -- Generate a screen from prompt. Args: `{ projectId, prompt, deviceType?, modelId? }`
- `edit_screens` -- Edit existing screens. Args: `{ projectId, selectedScreenIds, prompt, modelId? }`
- `generate_variants` -- Generate design variants. Args: `{ projectId, selectedScreenIds, prompt, variantOptions }`

**Design systems:**
- `create_design_system` -- Create and attach a design system
- `update_design_system` -- Update an existing design system
- `list_design_systems` -- List design systems for a project
- `apply_design_system` -- Apply a design system to screens

### Virtual Tools (added by proxy)

These combine multiple API calls into single operations:

**`get_screen_code`** -- Fetches a screen and downloads its HTML in one call.

**`get_screen_image`** -- Fetches a screen and downloads its screenshot as base64.

**`build_site`** -- Maps screens to routes and returns the design HTML for each page.
```json
{
  "projectId": "123456",
  "routes": [
    { "screenId": "abc", "route": "/" },
    { "screenId": "def", "route": "/about" }
  ]
}
```

---

## Generation

### Generate a Screen

```json
{
  "projectId": "4044680601076201931",
  "prompt": "A modern dashboard for a fitness app with real-time stats cards, activity chart, and weekly goals tracker. Clean, minimal, dark theme with electric blue (#2563eb) accents.",
  "deviceType": "DESKTOP",
  "modelId": "GEMINI_3_1_PRO"
}
```

Generation can take a few minutes. **Do not retry on timeout** -- the generation may still succeed. Use `get_screen` to check later.

| Use case | Model |
|----------|-------|
| Rapid iteration, drafts | `GEMINI_3_FLASH` |
| Final screens, high-fidelity | `GEMINI_3_1_PRO` |
| Quick edits | `GEMINI_3_FLASH` |

### Edit a Screen

```json
{
  "projectId": "4044680601076201931",
  "selectedScreenIds": ["98b50e2ddc9943efb387052637738f61"],
  "prompt": "Change the primary button color to deep blue (#1a365d) and add a subtle drop shadow. Keep everything else the same.",
  "modelId": "GEMINI_3_FLASH"
}
```

**Tips:**
- One focused change per call produces better results
- Reference components by name: "navigation bar", "hero section", "card grid"
- Include hex codes for precise color matching
- Say "Keep everything else the same" to prevent unwanted changes

### Generate Variants

```json
{
  "projectId": "4044680601076201931",
  "selectedScreenIds": ["98b50e2ddc9943efb387052637738f61"],
  "prompt": "Explore alternative layouts for the hero section",
  "variantOptions": {
    "variantCount": 3,
    "creativeRange": "EXPLORE",
    "aspects": ["LAYOUT", "COLOR_SCHEME"]
  }
}
```

| Range | Behavior |
|-------|----------|
| `REFINE` | Subtle refinements, closely adhering to the original |
| `EXPLORE` | Balanced exploration (default) |
| `REIMAGINE` | Radical explorations that fundamentally rethink the design |

**Targetable aspects:** `LAYOUT`, `COLOR_SCHEME`, `IMAGES`, `TEXT_FONT`, `TEXT_CONTENT`

### Design System Management

```json
{
  "projectId": "4044680601076201931",
  "designSystem": {
    "displayName": "Pulse Fitness",
    "theme": {
      "colorMode": "DARK",
      "customColor": "#e11d48",
      "headlineFont": "MONTSERRAT",
      "bodyFont": "INTER",
      "labelFont": "SPACE_GROTESK",
      "roundness": "ROUND_EIGHT",
      "colorVariant": "VIBRANT",
      "designMd": "High-energy fitness brand. Bold headlines, dark backgrounds, racing red accents."
    }
  }
}
```

**Color variants:** `MONOCHROME`, `NEUTRAL`, `TONAL_SPOT`, `VIBRANT`, `EXPRESSIVE`, `FIDELITY`, `CONTENT`, `RAINBOW`, `FRUIT_SALAD`

**Fonts (29):** `INTER`, `MONTSERRAT`, `GEIST`, `DM_SANS`, `IBM_PLEX_SANS`, `SORA`, `RUBIK`, `SPACE_GROTESK`, `PLUS_JAKARTA_SANS`, `WORK_SANS`, `MANROPE`, `LEXEND`, `PUBLIC_SANS`, `SPLINE_SANS`, `EPILOGUE`, `BE_VIETNAM_PRO`, `HANKEN_GROTESK`, `NUNITO_SANS`, `ARIMO`, `SOURCE_SANS_THREE`, `METROPOLIS`, `NEWSREADER`, `NOTO_SERIF`, `DOMINE`, `LIBRE_CASLON_TEXT`, `EB_GARAMOND`, `LITERATA`, `SOURCE_SERIF_FOUR`

**Roundness:** `ROUND_FOUR`, `ROUND_EIGHT`, `ROUND_TWELVE`, `ROUND_FULL`

**designMd:** Free-form markdown describing design intent. Injected into AI context during generation.

### Downloading Assets

Use the virtual tools for the simplest path:

```
get_screen_code   -> returns HTML directly
get_screen_image  -> returns screenshot as base64
```

Or download manually after `get_screen`:

```bash
curl -sL "$HTML_URL" -o .stitch/designs/page.html
curl -sL "${IMAGE_URL}=w1200" -o .stitch/designs/page.png
```

Append `=w{width}` to screenshot URLs for full resolution (CDN serves thumbnails by default).

---

## Prompt Enhancement Pipeline

Before calling any generation or editing tool, enhance the user's prompt.

### 1. Check for Design System Context

- Check for a local `.stitch/DESIGN.md` file as the primary reference.
- Use `list_design_systems` to check if one is attached to the project.
- If a design system exists, its tokens are already applied. Only repeat in the prompt if overriding.
- If none exists, always include the design system block in the prompt.

### 2. Refine UI/UX Terminology

Replace vague terms with specific component names. See [references/design-mappings.md](references/design-mappings.md).

| Vague | Professional |
|:---|:---|
| "menu at the top" | "sticky navigation bar with logo and list items" |
| "big photo" | "hero section with full-width imagery" |
| "list of things" | "responsive card grid with hover states" |
| "popup" | "modal dialog with overlay and smooth entry animation" |

### 3. Structure the Final Prompt

```markdown
[Overall vibe, mood, and purpose of the page]

**PAGE STRUCTURE:**
1. **Header:** [Description of navigation and branding]
2. **Hero Section:** [Headline, subtext, and primary CTA]
3. **Primary Content Area:** [Detailed component breakdown]
4. **Footer:** [Links and copyright information]
```

When no design system is attached, add:

```markdown
**DESIGN SYSTEM:**
- Platform: [Web/Mobile], [Desktop/Mobile]-first
- Theme: [Light/Dark]
- Palette: [Primary] (#hex), [Secondary] (#hex), [Background] (#hex)
- Style: [Roundness], [Shadow/Elevation], [Typography vibe]
```

### 4. Surface AI Feedback

After any generation or edit, always present the `outputComponents` (text description and suggestions) to the user.

---

## Build Loop

Iterative multi-page site generation using a "baton" system.

### Prerequisites

- A Stitch project
- A `.stitch/SITE.md` file documenting site vision and roadmap

### The Baton: `.stitch/next-prompt.md`

```markdown
---
page: about
---
A page describing how the product works with a clear value proposition.

**Page Structure:**
1. Header with navigation
2. Explanation of methodology
3. Team section with photos
4. Footer with links
```

### Execution Protocol

1. **Read the baton** -- Parse `.stitch/next-prompt.md` for the `page` name and prompt
2. **Consult context** -- Read `.stitch/SITE.md` for sitemap, roadmap, vision
3. **Generate** -- Call `generate_screen_from_text` or use CLI `tool` command
4. **Download** -- Use `get_screen_code` / `get_screen_image` virtual tools
5. **Integrate** -- Move to site directory, wire navigation, fix asset paths
6. **Update SITE.md** -- Mark page complete
7. **Write next baton** -- Update `.stitch/next-prompt.md` with next page

### Alternative: Use `build_site` for bulk generation

If you have multiple screens already generated, use `build_site` to map them all to routes at once:

```bash
pnpx @_davideast/stitch-mcp site -p <project-id> --routes '[
  {"screenId": "abc", "route": "/"},
  {"screenId": "def", "route": "/about"},
  {"screenId": "ghi", "route": "/contact"}
]'
```

This generates a deployable Astro project with all screens mapped to routes.

### File Structure

```
project/
  .stitch/
    metadata.json      # Stitch project & screen IDs
    SITE.md            # Site vision, sitemap, roadmap
    next-prompt.md     # Current task (the baton)
    designs/           # Staging area for Stitch output
      {page}.html
      {page}.png
  site/public/         # Production pages
```

---

## Agentic Workflow & Vibe Coding

- **Iterative Design:** Do not expect pixel-perfect UI on the first generation. Draft a V1 screen, review the HTML/image output, isolate specific layout or styling issues, refine exactly ONE variable (e.g., color, padding, or prompt phrasing) at a time, and regenerate until it matches the design intent.
- **Vibe Coding:** Commit your working HTML/CSS states and `next-prompt.md` files locally before attempting risky redesigns or merging multiple generated screens into the main application.

## DESIGN.md (Official Spec)

DESIGN.md is a **dual-representation** design system document following the [google-labs-code/design.md](https://github.com/google-labs-code/design.md) specification. The file combines machine-readable design tokens (YAML front matter) with human-readable design rationale (markdown prose). Tokens give exact values. Prose tells *why* those values exist and how to apply them.

### Creating a DESIGN.md

1. **From concept** -- Describe aesthetic intent; generate YAML tokens and markdown
2. **From existing brand** -- Provide URL or image; extract palette, typography
3. **From existing project** -- Use `get_project` + `get_screen` to synthesize

Feed content into the `designMd` field when calling `create_design_system`.

### File Structure & Validation

A DESIGN.md file has two layers:
1. **YAML front matter** — Machine-readable design tokens, delimited by `---` fences at the top. Supported token schemas: `colors`, `typography`, `rounded`, `spacing`, `components`.
2. **Markdown body** — Human-readable rationale organized into `##` sections.

Validate a DESIGN.md file, catch broken token references, and check WCAG contrast ratios using the official CLI:
```bash
npx @google/design.md lint DESIGN.md
```

### Official Format Example

```markdown
---
name: Heritage
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 3rem
  body-md:
    fontFamily: Public Sans
    fontSize: 1rem
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 0.75rem
rounded:
  sm: 4px
  md: 8px
spacing:
  sm: 8px
  md: 16px
---

## Overview
Architectural Minimalism meets Journalistic Gravitas. The UI evokes a premium matte finish — a high-end broadsheet or contemporary gallery.

## Colors
The palette is rooted in high-contrast neutrals and a single accent color.
- **Primary (#1A1C1E):** Deep ink for headlines and core text.
- **Secondary (#6C7278):** Sophisticated slate for borders, captions, metadata.
- **Tertiary (#B8422E):** "Boston Clay" — the sole driver for interaction.
- **Neutral (#F7F5F2):** Warm limestone foundation, softer than pure white.

## Typography
Headlines use semi-bold weight. Body text at 14-16px regular.

## Elevation
No shadows. Depth via border contrast and surface color variation.

## Components
- **Buttons**: Rounded (8px), primary uses brand blue fill, secondary uses outline
- **Inputs**: 1px border, surface-variant background, 12px padding
- **Cards**: No elevation, 1px outline border, 12px corner radius

## Do's and Don'ts
- Do use primary color only for the single most important action per screen
- Don't mix rounded and sharp corners in the same view
- Do maintain WCAG AA contrast ratios (4.5:1 for normal text)
- Don't use more than two font weights on a single screen
```

Stitch auto-generates **named colors** from base values: `surface`, `on-primary`, `error`, `outline`, etc., following Material color role conventions.

---

## Design Modes

Stitch is a suite of specialized design engines, not one model.

| Mode | `modelId` | Best for |
|------|-----------|----------|
| **Thinking with 3 Pro** | `GEMINI_3_1_PRO` | Complex logic, production candidates. Slower but pixel-perfect. |
| **Redesign (Nano Banana Pro)** | *(UI only)* | Stylistic transforms, vibe design, modernizing old interfaces. |
| **2.5 Pro** | *(UI only)* | High-fidelity HTML, A/B comparisons alongside 3 Pro. |
| **Fast** | `GEMINI_3_FLASH` | Rapid wireframing, Figma exports, quick iteration. |

**Tip:** Run the same prompt in Thinking 3 Pro and 2.5 Pro to compare. Use Fast for exploration, 3 Pro for finals.

### Style Word Bank (for Redesign mode)

Combine art-direction keywords from these categories:

**Layout & Structure:** Bento Grid, Editorial, Swiss Style, Split-Screen

**Texture & Depth:** Glassmorphism, Claymorphism, Skeuomorphic, Grainy/Noise

**Atmosphere & Era:** Brutalist, Cyberpunk, Y2K, Retro-Futurism

**Color & Contrast:** Duotone, Monochromatic, Pastel Goth, Dark Mode OLED

---

## Official Prompting Best Practices

**Starting a design:**
- Begin with a broad concept OR specific core functionalities
- Use adjectives to set vibe: "vibrant and encouraging" vs "minimalist and focused"

**Editing screens:**
- Make **one major change at a time**
- Be **specific**: target the exact element, screen, and visual change
- Example: "Change primary CTA button on login to larger size using brand primary blue"

**Theme control:**
- Colors: specific hex ("change primary to forest green") or mood-based ("warm, inviting palette")
- Fonts/Borders: "playful sans-serif font", "fully rounded button corners"
- Images: be specific about location and content

**Variations (distinct from editing):**
- For "what if" exploration, not incremental refinement
- Make **big swings** -- combine theme + layout changes
- Can run variations on top of a variation
- Pick best base, lower to `REFINE`, merge elements from other options

---

## Common Pitfalls

- Do not retry generation on timeout -- it may still succeed. Use `get_screen` to check.
- Do not use `GEMINI_3_PRO` -- deprecated. Use `GEMINI_3_FLASH` or `GEMINI_3_1_PRO`.
- Append `=w{width}` to screenshot URLs before downloading (or use `get_screen_image` virtual tool).
- Keep edits focused. One change per call produces better results.
- In the build loop, always update `.stitch/next-prompt.md` before completing.
- Do not recreate pages that already exist in the sitemap.
- If MCP tools are unavailable, use the CLI fallback: `pnpx @_davideast/stitch-mcp tool <name> -d '{...}'`
- To diagnose auth issues: `STITCH_API_KEY=your-key pnpx @_davideast/stitch-mcp doctor`
 `STITCH_API_KEY=your-key pnpx @_davideast/stitch-mcp doctor`
t already exist in the sitemap.
- If MCP tools are unavailable, use the CLI fallback: `pnpx @_davideast/stitch-mcp tool <name> -d '{...}'`
- To diagnose auth issues: `STITCH_API_KEY=your-key pnpx @_davideast/stitch-mcp doctor`
