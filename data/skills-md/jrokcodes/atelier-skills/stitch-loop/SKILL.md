---
name: stitch-loop
description: Teaches agents to iteratively build websites using Stitch with an autonomous baton-passing loop pattern
allowed-tools:
  - "stitch*:*"
  - "chrome*:*"
  - "Read"
  - "Write"
  - "Bash"
---

# Stitch Build Loop

You are an **autonomous frontend builder** participating in an iterative site-building loop. Your goal is to generate a page using Stitch, integrate it into the site, and prepare instructions for the next iteration.

## Overview

The Build Loop pattern enables continuous, autonomous website development through a "baton" system. Each iteration:
1. Reads the current task from a baton file (`next-prompt.md`)
2. Generates or edits a page using Stitch (SDK or MCP)
3. Integrates the page into the site structure
4. Writes the next task to the baton file for the next iteration

## Prerequisites

**Required:**
- Stitch access via **SDK** (preferred) or **MCP Server** (legacy)
  - SDK: `@google/stitch-sdk` installed at `Atelier/tools/stitch-sdk/`
  - MCP: `@_davideast/stitch-mcp` configured in `settings.local.json`
- A Stitch project (existing or will be created)
- A `DESIGN.md` file (generate one using the `design-md` skill if needed)
- A `SITE.md` file documenting the site vision and roadmap

**Optional:**
- Chrome DevTools MCP Server — enables visual verification of generated pages

## The Baton System

The `next-prompt.md` file acts as a relay baton between iterations:

```markdown
---
page: about
mode: generate
---
A page describing how jules.top tracking works.

**DESIGN SYSTEM (REQUIRED):**
[Copy from DESIGN.md Section 6]

**Page Structure:**
1. Header with navigation
2. Explanation of tracking methodology
3. Footer with links
```

For editing an existing screen (SDK only):

```markdown
---
page: about
mode: edit
screenId: 9089d99853df49049cb03bb99d969b3c
---
Change the primary CTA button color to #2BBCB3 and increase its padding to px-8 py-3.
Move the search bar to full width.
```

**Critical rules:**
- The `page` field in YAML frontmatter determines the output filename
- The `mode` field controls generation behavior: `generate` (default) or `edit`
- When `mode: edit`, include `screenId` to target the existing screen
- The prompt content must include the design system block from `DESIGN.md` (for generate mode)
- You MUST update this file before completing your work to continue the loop

## Execution Protocol

### Step 1: Read the Baton

Parse `next-prompt.md` to extract:
- **Page name** from the `page` frontmatter field
- **Prompt content** from the markdown body

### Step 2: Consult Context Files

Before generating, read these files:

| File | Purpose |
|------|---------|
| `SITE.md` | Site vision, **Stitch Project ID**, existing pages (sitemap), roadmap |
| `DESIGN.md` | Required visual style for Stitch prompts |

**Important checks:**
- Section 4 (Sitemap) — Do NOT recreate pages that already exist
- Section 5 (Roadmap) — Pick tasks from here if backlog exists
- Section 6 (Creative Freedom) — Ideas for new pages if roadmap is empty

### Step 3: Generate with Stitch

Use the Stitch SDK (preferred) or MCP tools to generate the page:

#### Option A: SDK (preferred)

```javascript
// Run via: STITCH_API_KEY="$(cat ~/.claude/secrets/your-api-key.txt)" node -e '...'
import { stitch } from "@google/stitch-sdk";

const project = stitch.project(projectId);
const screen = await project.generate(prompt);          // New screen
// OR for iteration on existing screen:
const edited = await existingScreen.edit(editPrompt);   // Surgical edit
const html = await screen.getHtml();   // HTML download URL
const image = await screen.getImage(); // Screenshot URL
```

1. **Get or create project**:
   - If `stitch.json` exists, use `stitch.project(projectId)`
   - Otherwise, call `stitch.callTool("create_project", { title })` and save the ID to `stitch.json`
2. **Generate or edit screen**:
   - **New page**: `project.generate(prompt)` — full prompt including design system block
   - **Edit existing**: `screen.edit(editPrompt)` — surgical changes to an existing screen (see Step 3.5)
3. **Retrieve assets**: Use `screen.getHtml()` and `screen.getImage()` to get download URLs
   - Download and save as `queue/{page}.html` and `queue/{page}.png`

#### Option B: MCP (legacy)

1. **Discover namespace**: Run `list_tools` to find the Stitch MCP prefix
2. **Get or create project**:
   - If `stitch.json` exists, use the `projectId` from it
   - Otherwise, call `[prefix]:create_project` and save the ID to `stitch.json`
3. **Generate screen**: Call `[prefix]:generate_screen_from_text` with:
   - `projectId`: The project ID
   - `prompt`: The full prompt from the baton (including design system block)
   - `deviceType`: `DESKTOP` (or as specified)
4. **Retrieve assets**: Call `[prefix]:get_screen` to get:
   - `htmlCode.downloadUrl` — Download and save as `queue/{page}.html`
   - `screenshot.downloadUrl` — Download and save as `queue/{page}.png`

### Step 3.5: Iterate with Edit (SDK only)

After generating a screen, review the output. If it's 80-90% right but needs 1-2 tweaks, use `screen.edit()` instead of regenerating from scratch:

```javascript
// Surgical edit — preserves everything else on the screen
const edited = await screen.edit("Change the primary CTA button color to #2BBCB3 and increase padding to px-8 py-3");
```

**When to edit vs regenerate:**
| Situation | Action |
|-----------|--------|
| Layout is wrong | Regenerate with updated prompt |
| Colors/typography off | Edit: "Change heading font to Clash Display, accent color to #2BBCB3" |
| Missing element | Edit: "Add a floating chat button in bottom-right, 56px teal circle" |
| Content wrong | Edit: "Replace hero headline with 'AI That Works For Your Practice'" |
| Everything wrong | Regenerate from scratch |

**Edit rules** (same as STITCH-MASTERY iteration rules):
- ONE or TWO changes per edit call
- Be surgical and specific with exact values (hex codes, px dimensions)
- Bad: "Fix the layout and change colors" / Good: "Change card background to rgba(17,17,17,0.60)"

You can also generate design **variants** for comparison:
```javascript
const variants = await screen.variants("Try different color schemes", {
  variantCount: 3,
  creativeRange: "REFINE",        // REFINE | EXPLORE | REIMAGINE
  aspects: ["COLOR_SCHEME"],      // LAYOUT | COLOR_SCHEME | IMAGES | TEXT_FONT | TEXT_CONTENT
});
```

### Step 4: Integrate into Site

1. Move generated HTML from `queue/{page}.html` to `site/public/{page}.html`
2. Fix any asset paths to be relative to the public folder
3. Update navigation:
   - Find existing placeholder links (e.g., `href="#"`) and wire them to the new page
   - Add the new page to the global navigation if appropriate
4. Ensure consistent headers/footers across all pages

### Step 4.5: Visual Verification (Optional)

If the **Chrome DevTools MCP Server** is available, verify the generated page:

1. **Check availability**: Run `list_tools` to see if `chrome*` tools are present
2. **Start dev server**: Use Bash to start a local server (e.g., `npx serve site/public`)
3. **Navigate to page**: Call `[chrome_prefix]:navigate` to open `http://localhost:3000/{page}.html`
4. **Capture screenshot**: Call `[chrome_prefix]:screenshot` to capture the rendered page
5. **Visual comparison**: Compare against the Stitch screenshot (`queue/{page}.png`) for fidelity
6. **Stop server**: Terminate the dev server process

> **Note:** This step is optional. If Chrome DevTools MCP is not installed, skip to Step 5.

### Step 5: Update Site Documentation

Modify `SITE.md`:
- Add the new page to Section 4 (Sitemap) with `[x]`
- Remove any idea you consumed from Section 6 (Creative Freedom)
- Update Section 5 (Roadmap) if you completed a backlog item

### Step 6: Prepare the Next Baton (Critical)

**You MUST update `next-prompt.md` before completing.** This keeps the loop alive.

1. **Decide the next page**: 
   - Check `SITE.md` Section 5 (Roadmap) for pending items
   - If empty, pick from Section 6 (Creative Freedom)
   - Or invent something new that fits the site vision
2. **Write the baton** with proper YAML frontmatter:

```markdown
---
page: achievements
---
A competitive achievements page showing developer badges and milestones.

**DESIGN SYSTEM (REQUIRED):**
[Copy the entire design system block from DESIGN.md]

**Page Structure:**
1. Header with title and navigation
2. Badge grid showing unlocked/locked states
3. Progress bars for milestone tracking
```

## File Structure Reference

```
project/
├── next-prompt.md      # The baton — current task
├── stitch.json         # Stitch project ID (persist this!)
├── DESIGN.md           # Visual design system (from design-md skill)
├── SITE.md             # Site vision, sitemap, roadmap
├── queue/              # Staging area for Stitch output
│   ├── {page}.html
│   └── {page}.png
└── site/public/        # Production pages
    ├── index.html
    └── {page}.html
```

## Orchestration Options

The loop can be driven by different orchestration layers:

| Method | How it works |
|--------|--------------|
| **CI/CD** | GitHub Actions triggers on `next-prompt.md` changes |
| **Human-in-loop** | Developer reviews each iteration before continuing |
| **Agent chains** | One agent dispatches to another (e.g., Jules API) |
| **Manual** | Developer runs the agent repeatedly with the same repo |

The skill is orchestration-agnostic — focus on the pattern, not the trigger mechanism.

## Design System Integration

This skill works best with the `design-md` skill:

1. **First time setup**: Generate `DESIGN.md` using the `design-md` skill from an existing Stitch screen
2. **Every iteration**: Copy Section 6 ("Design System Notes for Stitch Generation") into your baton prompt
3. **Consistency**: All generated pages will share the same visual language

## Common Pitfalls

- ❌ Forgetting to update `next-prompt.md` (breaks the loop)
- ❌ Recreating a page that already exists in the sitemap
- ❌ Not including the design system block in the prompt
- ❌ Leaving placeholder links (`href="#"`) instead of wiring real navigation
- ❌ Forgetting to persist `stitch.json` after creating a new project

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Stitch generation fails | Check that the prompt includes the design system block |
| Inconsistent styles | Ensure DESIGN.md is up-to-date and copied correctly |
| Loop stalls | Verify `next-prompt.md` was updated with valid frontmatter |
| Navigation broken | Check all internal links use correct relative paths |
| SDK `screen.edit()` fails | Verify screenId is correct; fall back to full regeneration |
| Edit produces poor quality | Use full regeneration for major layout changes; edit is for 1-2 tweaks only |
| MCP server not starting | Switch to SDK proxy: `node Atelier/tools/stitch-sdk/proxy.js` |
