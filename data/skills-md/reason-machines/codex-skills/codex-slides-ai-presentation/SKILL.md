---
name: codex-slides-ai-presentation
description: Create AI-generated slide decks inside Codex with full visual control, parallel rendering, and PPTX/PDF export
triggers:
  - create a presentation with codex slides
  - generate slides about
  - make a deck using codex slides
  - build a powerpoint presentation
  - create slides from my files
  - turn this into a slide deck
  - make an ai presentation
  - generate a visual deck
---

# Codex Slides AI Presentation

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## What is Codex Slides?

**Codex Slides** is an open-source AI slide studio that runs inside Codex. It transforms prompts, repos, or files into production-ready presentations with:

- **⚡ Fast parallel rendering** — 10+ slides in ~4–5 minutes
- **118 visual systems** — 45 deck templates + 73 community styles
- **24 guided scenarios** — research, data stories, redesign, localization
- **Full visibility** — watch research → outline → style → render → edit → export
- **Production export** — PPTX and PDF with speaker notes
- **Zero extra API keys** — runs on your existing `codex login`
- **Browser-first workflow** — every step visible and steerable

Think of it as the **open-source, agent-native alternative to Gamma and Tome**.

## Installation

### Quick Install

```bash
# Install from Codex Plugin Marketplace
codex plugin marketplace add nexu-io/codex-slides
codex plugin add codex-slides@codex-slides
```

### Verify Installation

```bash
# List installed plugins
codex plugin list

# Check MCP tools are available
codex mcp list
```

You should see **38 MCP tools** registered for `codex-slides`.

## Core Workflow

### 1. Open Codex Slides in Browser

Always start by opening the Codex Slides UI in the **Codex Browser**:

```text
Open Codex Slides in the Codex Browser and keep it visible.
```

This ensures you can see and approve each step: questions, outline, visual direction, and rendering.

### 2. Basic Deck Creation

```text
Create a 12-slide market deck about 2026 humanoid robotics.
Let me confirm the questions, outline, and visual direction before rendering.
```

**What happens:**
1. Opens a new durable project
2. Shows clarification questions (audience, language, aspect ratio, etc.)
3. Generates outline → you review/edit
4. Suggests visual directions → you choose
5. Renders slides progressively or in parallel
6. Opens editor for refinement

### 3. Generate from Files

```text
Open Codex Slides and create a 10-slide investor deck from the files in ./pitch-materials/
Use the Corporate template and 16:9 aspect ratio.
```

Codex Slides can read:
- **Markdown** — research notes, briefs, outlines
- **JSON/YAML** — structured data, configs
- **Code** — repos, architecture docs
- **PDFs** — existing presentations, reports
- **Images** — logos, charts, screenshots

### 4. Fast Mode (Parallel Rendering)

```text
Create a 15-slide training deck about TypeScript best practices.
Use fast mode to render all slides in parallel.
Set aspect ratio to 16:9 and resolution to 2K.
```

**Fast mode:**
- Renders **all slides simultaneously** (not one-by-one)
- Queues overflow if engine limits hit
- Locks outline and visual direction upfront
- Dramatically faster for 10+ slide decks

## MCP Tools Reference

Codex Slides exposes **38 MCP tools** for agent control. Key tools:

### Project Management

```typescript
// Create a new project
create_project({
  name: "Q4 Product Launch",
  description: "Internal stakeholder deck",
  aspect_ratio: "16:9",
  language: "en"
})

// Open existing project
open_project({ project_id: "proj_abc123" })

// List all projects
list_projects({ limit: 20, offset: 0 })
```

### Outline Control

```typescript
// Generate outline from prompt
generate_outline({
  project_id: "proj_abc123",
  topic: "Cloud migration strategy",
  slide_count: 10,
  audience: "Engineering leadership"
})

// Edit outline
update_outline({
  project_id: "proj_abc123",
  outline: {
    slides: [
      { title: "Current State", talking_points: ["Legacy on-prem", "Cost analysis"] },
      { title: "Migration Plan", talking_points: ["Phase 1: Lift & shift", "Phase 2: Refactor"] }
    ]
  }
})
```

### Visual Direction

```typescript
// Get style recommendations
get_style_recommendations({
  project_id: "proj_abc123",
  topic: "Product roadmap 2026"
})

// Apply a style
apply_style({
  project_id: "proj_abc123",
  style_id: "corporate-blue" // or community style like "infographic-modern"
})
```

### Slide Generation

```typescript
// Render all slides (fast mode)
render_all_slides({
  project_id: "proj_abc123",
  mode: "parallel", // or "sequential"
  resolution: "2K" // "1K" | "2K" | "4K"
})

// Render single slide
render_slide({
  project_id: "proj_abc123",
  slide_index: 3,
  resolution: "2K"
})
```

### Editing

```typescript
// Add a slide
add_slide({
  project_id: "proj_abc123",
  position: 5,
  title: "Next Steps",
  talking_points: ["Q1 milestones", "Resource requirements"]
})

// Reorder slides
reorder_slides({
  project_id: "proj_abc123",
  from_index: 3,
  to_index: 1
})

// Update speaker notes
update_speaker_notes({
  project_id: "proj_abc123",
  slide_index: 2,
  notes: "Emphasize cost savings vs. legacy system"
})
```

### Export

```typescript
// Export to PowerPoint
export_pptx({
  project_id: "proj_abc123",
  include_speaker_notes: true
})

// Export to PDF
export_pdf({
  project_id: "proj_abc123",
  include_speaker_notes: false,
  quality: "high" // "standard" | "high" | "print"
})
```

## Common Patterns

### Pattern 1: Research-Based Deck

```text
Open Codex Slides and create a research-backed deck about quantum computing advances.

1. Run multi-round web research on recent quantum breakthroughs
2. Generate a 12-slide outline based on the research
3. Use the "Technology Report" template
4. Set aspect ratio to 16:9 and resolution to 2K
5. Let me review the outline before rendering
6. Save the research brief in Design Files
```

### Pattern 2: Source-to-Slides Workflow

```text
Open Codex Slides in the Browser.

Create a 8-slide deck from the following sources:
- ./docs/architecture.md
- ./README.md
- ./benchmarks/performance.json

Target audience: technical investors
Visual direction: Corporate Modern
Aspect ratio: 16:9
Include code snippets where relevant.
```

### Pattern 3: Redesign Existing Deck

```text
Open Codex Slides and import ./old-pitch.pptx

Tasks:
1. Extract the outline and speaker notes
2. Apply the "Startup Pitch" template
3. Update visual direction to "Bold Gradient"
4. Re-render all slides in 4K resolution
5. Export as PPTX with original notes preserved
```

### Pattern 4: Multi-Language Localization

```text
Open the existing "Product Launch" project in Codex Slides.

Create localized versions:
1. Duplicate the project 3 times
2. Translate outline and notes to: Japanese, Spanish, German
3. Keep the same visual direction and layout
4. Render all versions in parallel (fast mode)
5. Export each as separate PPTX files
```

### Pattern 5: Data Visualization Deck

```text
Open Codex Slides and create a data story from ./sales-data.json

Requirements:
- 10 slides focusing on Q4 performance
- Use the "Dashboard Infographic" style
- Aspect ratio: 16:9
- Include charts, trend lines, and KPI callouts
- Target audience: board members
- Add speaker notes explaining each metric
```

## Configuration

### Project Settings

Projects are stored in `~/.codex-slides/projects/` (or configured path):

```typescript
// .codex-slides/config.json
{
  "projects_path": "~/Documents/CodexSlides",
  "default_aspect_ratio": "16:9",
  "default_resolution": "2K",
  "default_language": "en",
  "parallel_render_limit": 5,
  "design_files_auto_sync": true
}
```

### Environment Variables

```bash
# Optional: Override default paths
export CODEX_SLIDES_PROJECTS_DIR="$HOME/my-presentations"
export CODEX_SLIDES_CACHE_DIR="$HOME/.cache/codex-slides"

# Optional: Rendering preferences
export CODEX_SLIDES_DEFAULT_RESOLUTION="4K"
export CODEX_SLIDES_PARALLEL_LIMIT="8"
```

### Aspect Ratios

Available aspect ratios:
- `16:9` — Standard widescreen (default)
- `4:3` — Classic presentation
- `1:1` — Square (social media)
- `9:16` — Vertical (mobile, stories)
- `3:4` — Portrait

### Resolution Options

- `1K` — Fast preview (1024px)
- `2K` — Balanced quality (2048px, recommended)
- `4K` — Print-ready (4096px)

## Visual Systems

### 45 Deck Templates

Organized by category:

**Business:**
- Corporate Modern
- Startup Pitch
- Investor Deck
- Quarterly Business Review

**Technical:**
- Developer Documentation
- API Reference
- Architecture Overview
- Technical Training

**Creative:**
- Brand Guidelines
- Portfolio Showcase
- Case Study
- Campaign Presentation

**Education:**
- Academic Lecture
- Workshop Materials
- Training Course
- Research Findings

**Data:**
- Analytics Report
- Dashboard Summary
- Data Story
- Performance Review

### 73 Community Styles

Grouped by visual approach:

- **Reports** (8 styles) — clean, structured, text-focused
- **Infographics** (9 styles) — visual data, icons, callouts
- **Diagrams** (6 styles) — flowcharts, systems, processes
- **Data & Maps** (7 styles) — charts, geography, metrics
- **Dashboards** (5 styles) — KPIs, real-time, grids
- **Posters** (8 styles) — bold, event-focused, single-page
- **Product** (6 styles) — feature showcases, UI mockups
- **Brand** (7 styles) — identity, guidelines, mood boards
- **Architecture** (5 styles) — buildings, blueprints, renders
- **Photography** (6 styles) — image-first, minimal text
- **Editorial** (4 styles) — magazine, longform, narrative
- **Illustration** (2 styles) — custom graphics, hand-drawn

## Code Examples

### TypeScript: Programmatic Deck Creation

```typescript
import { CodexSlidesClient } from '@codex-slides/sdk';

async function createProductDeck() {
  const client = new CodexSlidesClient({
    projectsDir: process.env.CODEX_SLIDES_PROJECTS_DIR || '~/.codex-slides/projects'
  });

  // Create project
  const project = await client.createProject({
    name: 'Product Roadmap 2026',
    description: 'Engineering team quarterly planning',
    aspectRatio: '16:9',
    language: 'en'
  });

  // Generate outline
  const outline = await client.generateOutline({
    projectId: project.id,
    topic: 'Q1-Q4 feature roadmap with dependencies',
    slideCount: 12,
    audience: 'Engineering and product teams',
    sources: ['./roadmap.md', './jira-export.json']
  });

  // Apply visual style
  await client.applyStyle({
    projectId: project.id,
    styleId: 'corporate-blue'
  });

  // Render in parallel (fast mode)
  await client.renderAllSlides({
    projectId: project.id,
    mode: 'parallel',
    resolution: '2K'
  });

  // Export
  const pptxPath = await client.exportPPTX({
    projectId: project.id,
    includeSpeakerNotes: true
  });

  console.log(`Deck created: ${pptxPath}`);
}
```

### TypeScript: Batch Processing

```typescript
import { CodexSlidesClient } from '@codex-slides/sdk';
import fs from 'fs/promises';

async function generateWeeklyReports() {
  const client = new CodexSlidesClient();
  const teams = ['Engineering', 'Product', 'Design', 'Marketing'];

  for (const team of teams) {
    const dataFile = `./reports/${team.toLowerCase()}-metrics.json`;
    const data = JSON.parse(await fs.readFile(dataFile, 'utf-8'));

    const project = await client.createProject({
      name: `${team} Weekly Report`,
      aspectRatio: '16:9',
      language: 'en'
    });

    await client.generateOutline({
      projectId: project.id,
      topic: `${team} KPIs and highlights for week of ${data.weekOf}`,
      slideCount: 6,
      audience: 'Leadership team',
      sources: [dataFile]
    });

    await client.applyStyle({
      projectId: project.id,
      styleId: 'dashboard-modern'
    });

    await client.renderAllSlides({
      projectId: project.id,
      mode: 'parallel',
      resolution: '2K'
    });

    await client.exportPDF({
      projectId: project.id,
      quality: 'high'
    });
  }
}
```

### TypeScript: Custom Research Pipeline

```typescript
import { CodexSlidesClient } from '@codex-slides/sdk';

async function researchDeck(topic: string, depth: 'shallow' | 'deep') {
  const client = new CodexSlidesClient();

  const project = await client.createProject({
    name: `Research: ${topic}`,
    aspectRatio: '16:9',
    language: 'en'
  });

  // Run multi-round research
  const researchBrief = await client.runResearch({
    projectId: project.id,
    topic,
    rounds: depth === 'deep' ? 3 : 1,
    sources: 'web', // 'web' | 'files' | 'both'
    saveToDesignFiles: true
  });

  // Generate outline from research
  const outline = await client.generateOutline({
    projectId: project.id,
    topic,
    slideCount: 15,
    audience: 'Technical stakeholders',
    researchBriefId: researchBrief.id
  });

  // Rank and apply best visual direction
  const recommendations = await client.getStyleRecommendations({
    projectId: project.id,
    topic
  });

  await client.applyStyle({
    projectId: project.id,
    styleId: recommendations[0].id // Top recommendation
  });

  // Render
  await client.renderAllSlides({
    projectId: project.id,
    mode: 'parallel',
    resolution: '4K'
  });

  return project;
}
```

## CLI Usage

### Basic Commands

```bash
# Create a deck from CLI
codex-slides create \
  --topic "Cloud security best practices" \
  --slides 10 \
  --aspect-ratio 16:9 \
  --template corporate-modern \
  --output ./security-deck.pptx

# Generate from files
codex-slides create \
  --sources ./docs/*.md \
  --topic "API documentation" \
  --slides 8 \
  --style developer-docs \
  --fast-mode \
  --output ./api-deck.pptx

# List projects
codex-slides list

# Open project in browser
codex-slides open proj_abc123

# Export existing project
codex-slides export proj_abc123 \
  --format pptx \
  --resolution 4K \
  --output ./final-deck.pptx
```

### Advanced CLI

```bash
# Research-backed deck
codex-slides create \
  --topic "Blockchain scalability solutions 2026" \
  --research deep \
  --slides 12 \
  --audience "Technical investors" \
  --style infographic-modern \
  --fast-mode \
  --resolution 2K \
  --speaker-notes \
  --output ./blockchain-deck.pptx

# Batch export all projects
codex-slides export --all \
  --format pdf \
  --resolution 4K \
  --output-dir ./exports

# Duplicate and localize
codex-slides duplicate proj_abc123 \
  --name "Product Launch (Japanese)" \
  --translate ja \
  --render \
  --export ./launch-ja.pptx
```

## Troubleshooting

### Issue: Browser not opening

**Solution:**
```bash
# Ensure Codex Browser is available
codex browser status

# Explicitly open Codex Slides
codex browser open http://localhost:3000

# Check plugin is running
codex plugin status codex-slides
```

### Issue: Slides not rendering

**Check:**
1. Is the outline finalized? Rendering pauses if outline is in draft state.
2. Is a visual style applied? Default will be used if none selected.
3. Check parallel render limit (default: 5 concurrent slides).

```typescript
// Adjust parallel limit
await client.updateConfig({
  parallel_render_limit: 8
});
```

### Issue: Export fails

**Common causes:**
- Project has no rendered slides
- Speaker notes contain invalid characters
- Output path not writable

```bash
# Verify project state
codex-slides status proj_abc123

# Test export to temp directory
codex-slides export proj_abc123 --output /tmp/test.pptx
```

### Issue: Slow rendering

**Optimizations:**
1. Use fast mode (parallel rendering)
2. Lower resolution (1K for drafts, 2K for reviews, 4K for finals)
3. Reduce slide count in outline
4. Simplify visual style (text-heavy styles render faster)

```text
Switch to 1K resolution and re-render all slides in fast mode.
```

### Issue: Design Files not syncing

```bash
# Force refresh design files
codex-slides sync-design-files proj_abc123

# Check design files path
ls ~/.codex-slides/projects/proj_abc123/design-files/
```

### Issue: MCP tools not found

```bash
# Reinstall plugin
codex plugin remove codex-slides
codex plugin marketplace add nexu-io/codex-slides
codex plugin add codex-slides@codex-slides

# Verify MCP registration
codex mcp list | grep codex-slides
```

## Best Practices

### 1. Always Keep Browser Visible

Codex Slides is **browser-first**. Keep the UI open so you can:
- Approve outlines before rendering
- Choose visual direction
- Watch progress in real-time
- Catch errors early

### 2. Use Design Files for Context

Upload brand guidelines, logos, color palettes, and reference materials to **Design Files**:

```text
Add the brand guidelines PDF and logo SVG to Design Files.
Use the brand colors from the guidelines when rendering slides.
```

### 3. Save Successful Projects as Templates

```text
Save this project as a reusable template named "Engineering Roadmap Q-Series".
Include the visual direction and outline structure.
```

### 4. Leverage Fast Mode for Long Decks

For 10+ slides, always use fast mode:

```text
Create a 20-slide training deck about Python async programming.
Use fast mode to render all slides in parallel.
```

### 5. Iterate in the Editor

Don't regenerate entire decks. Use in-place editing:

```text
Mark the title area on slide 3 and change it to "Market Opportunity".
Redraw slide 7 with more emphasis on the chart.
Add a new slide after slide 5 about competitive landscape.
```

### 6. Export Incrementally

Export drafts early and often:

```text
Export the current deck as PDF for review, even though only 8 of 12 slides are rendered.
```

---

## Quick Reference Card

**Installation:**
```bash
codex plugin marketplace add nexu-io/codex-slides
codex plugin add codex-slides@codex-slides
```

**Basic Usage:**
```text
Open Codex Slides in the Codex Browser and create a 10-slide deck about [topic].
Let me review the outline and visual direction before rendering.
Use fast mode and 16:9 aspect ratio.
```

**From Files:**
```text
Create an 8-slide deck from ./docs/*.md
Use the Technical template and 2K resolution.
```

**Export:**
```text
Export the current project as PPTX with speaker notes.
Also export as PDF in 4K for printing.
```

**Key MCP Tools:**
- `create_project` → new deck
- `generate_outline` → structure
- `apply_style` → visual direction
- `render_all_slides` → fast mode
- `export_pptx` / `export_pdf` → final output

**Aspect Ratios:** 16:9 (default), 4:3, 1:1, 9:16, 3:4  
**Resolutions:** 1K (draft), 2K (standard), 4K (print)  
**Templates:** 45 deck templates + 73 community styles  
**Languages:** Multi-language support with localization

---

**Resources:**
- GitHub: https://github.com/nexu-io/codex-slides
- Docs: https://github.com/nexu-io/codex-slides#readme
- Media Kit: https://github.com/nexu-io/codex-slides/blob/main/docs/MEDIA_KIT.md
