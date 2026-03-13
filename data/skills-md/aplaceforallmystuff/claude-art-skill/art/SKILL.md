---
name: art
description: Complete visual content system for Claude Code. Default aesthetic - light backgrounds, teal/burnt orange accents, hand-drawn sketch style.
user-invocable: true
triggers:
  - USE WHEN user wants to create visual content, illustrations, or diagrams
  - USE WHEN user mentions art, header images, visualizations, or any visual request
  - USE WHEN user references mermaid, flowchart, technical diagram, or infographic

# Workflow Routing
workflows:
  - USE WHEN user wants blog header or editorial illustration: workflows/workflow.md
  - USE WHEN user wants visualization or is unsure which format: workflows/visualize.md
  - USE WHEN user wants mermaid flowchart or sequence diagram: workflows/mermaid.md
  - USE WHEN user wants technical or architecture diagram: workflows/technical-diagrams.md
  - USE WHEN user wants taxonomy or classification grid: workflows/taxonomies.md
  - USE WHEN user wants timeline or chronological progression: workflows/timelines.md
  - USE WHEN user wants framework or 2x2 matrix: workflows/frameworks.md
  - USE WHEN user wants comparison or X vs Y: workflows/comparisons.md
  - USE WHEN user wants annotated screenshot: workflows/annotated-screenshots.md
  - USE WHEN user wants recipe card or step-by-step: workflows/recipe-cards.md
  - USE WHEN user wants aphorism or quote card: workflows/aphorisms.md
  - USE WHEN user wants conceptual map or territory: workflows/maps.md
  - USE WHEN user wants stat card or big number visual: workflows/stats.md
  - USE WHEN user wants comic or sequential panels: workflows/comics.md
  - USE WHEN user wants sketchnote, visual notes, or meeting summary illustration: workflows/sketchnotes.md
  - USE WHEN user wants to edit, modify, or transform existing image: workflows/image-editing.md
---

# Art Skill

Complete visual content system supporting **multiple brand aesthetics**.

---

## Aesthetic Routing

The art skill supports multiple visual identities. **Before generating any visual, determine which aesthetic applies.**

### How to Select an Aesthetic

1. **Check if the user specifies a brand/project** (e.g., "my-brand icon", "acme newsletter header")
2. **Check for content-type exceptions** (see Content-Type Override Rules below)
3. **Check if the target output has a site-specific style guide** (e.g., `HERO-IMAGE-TEMPLATE.md`)
4. **If no brand specified, use the default aesthetic**

### Content-Type Override Rules

**CRITICAL:** Some content types intentionally use different aesthetics than their host site.

| Content Type | Detection Pattern | Aesthetic to Use | DO NOT Use |
|--------------|------------------|------------------|------------|
| **Satirical/Parody Content** | User explicitly says "satire", "parody", "joke product" | Match the satire target's aesthetic (e.g., corporate B2B for business parody) | Host site's aesthetic |
| **Easter Eggs** | Path contains `easter-eggs/`, explicitly marked as easter egg | Depends on easter egg theme, ask user if unclear | Host site's default |

**Rule:** When content-type override detected, DO NOT check host site style guides. The content is intentionally divergent.

### Base Prompt Prefix Standard (MANDATORY)

**Every aesthetic MUST define a Base Prompt Prefix** — a locked consistency block that gets prepended to every image generation prompt for that aesthetic. This ensures visual cohesion across a set of illustrations.

**What the prefix locks down:**
- Line weight and quality
- Background treatment
- Camera angle / perspective
- Fill ratio (illustration vs. whitespace)
- Color balance percentages
- Shadow intensity and direction
- Text treatment (if applicable)

**Where to find each prefix:**
- Each aesthetic file (`.md`) contains a "Base Prompt Prefix" section with the locked values
- Project-specific aesthetics (e.g., lead magnet `AESTHETIC.md`) inherit from their parent brand and override only what changes
- **Always read the aesthetic file and use its prefix before generating** — never freestyle prompt parameters that have been locked

**When creating new aesthetics via `aesthetic-definer`:** The agent MUST produce a base prompt prefix as part of the output. An aesthetic without a consistency lock is incomplete.

### Available Aesthetics

| Brand | Aesthetic File | Style |
|-------|---------------|-------|
| **Default** | `~/.claude/skills/art/aesthetic.md` | Hand-drawn sketch, cream backgrounds, teal/orange accents |

**To add a new aesthetic:** Create a new file at `~/.claude/skills/art/aesthetics/[name].md` using the default aesthetic as a template. See `aesthetics/README.md` for the required format.

### Aesthetic Loading Rule

**Read the matching aesthetic file BEFORE writing any prompt or generating any image.** The aesthetic file is the source of truth for that brand's colors, style parameters, anti-patterns, and prompt integration phrases.

---

## Workflow Routing

| Content Type | Workflow |
|--------------|----------|
| Blog headers / Editorial | `workflows/workflow.md` |
| Adaptive orchestrator | `workflows/visualize.md` |
| Flowcharts / Sequences | `workflows/mermaid.md` |
| Architecture diagrams | `workflows/technical-diagrams.md` |
| Classification grids | `workflows/taxonomies.md` |
| Chronological | `workflows/timelines.md` |
| 2x2 matrices | `workflows/frameworks.md` |
| X vs Y | `workflows/comparisons.md` |
| Screenshot markup | `workflows/annotated-screenshots.md` |
| Step-by-step | `workflows/recipe-cards.md` |
| Sketchnotes / visual notes | `workflows/sketchnotes.md` |
| Quote cards | `workflows/aphorisms.md` |
| Idea territories | `workflows/maps.md` |
| Big numbers | `workflows/stats.md` |
| Sequential panels | `workflows/comics.md` |
| **Edit existing image** | `workflows/image-editing.md` |

---

## Image Generation

**Default model:** nano-banana-2 (Gemini 3.1 Flash Image)

```bash
bun run ~/.claude/skills/art/tools/generate-image.ts \
  --model nano-banana-2 \
  --prompt "[PROMPT]" \
  --size 2K \
  --aspect-ratio 1:1 \
  --output /path/to/output.png
```

### Alternative Model

| Model | When to Use |
|-------|-------------|
| **nano-banana-pro** | Maximum quality, professional asset production, complex multi-turn editing |

### Model Selection Guide

**Nano Banana 2 (default):**
- Best for: Most image generation tasks, fast iteration
- Strengths: Pro-level quality at Flash speed, reference images, web search grounding, 512px-4K range
- Use when: Default choice for all standard image generation
- API model: `gemini-3.1-flash-image-preview`

**Nano Banana Pro:**
- Best for: Professional asset production, maximum reasoning
- Strengths: Advanced reasoning, multi-turn refinement, style transfer
- Use when: Quality matters more than speed, complex compositional tasks
- API model: `gemini-3-pro-image-preview`

**API keys in:** `~/.claude/.env`
- `GOOGLE_API_KEY` - Required for both models
- `REMOVEBG_API_KEY` - Background removal (optional)

### Quick Preview Workflow (512px)

Use `--size 512px` for fast, cheap previews before committing to full resolution:

```bash
# 1. Preview at 512px (fast, low cost)
bun run ~/.claude/skills/art/tools/generate-image.ts \
  --prompt "[PROMPT]" --size 512px --output /tmp/preview.png

# 2. Happy? Regenerate at full size
bun run ~/.claude/skills/art/tools/generate-image.ts \
  --prompt "[PROMPT]" --size 2K --output /path/to/final.png
```

### Thinking Flag (Nano Banana 2 only)

Add `--thinking` to give the model more reasoning time for complex compositions:

```bash
bun run ~/.claude/skills/art/tools/generate-image.ts \
  --prompt "Complex multi-element scene..." \
  --thinking high --output /path/to/output.png
```

| Level | Use When |
|-------|----------|
| `minimal` | Default — balances quality and latency |
| `high` | Complex layouts, precise positioning, multi-element scenes |

Only works with `nano-banana-2`. Thinking is always on (minimal by default). Use `high` when composition accuracy matters more than speed.

### Common Diagram Pitfalls (Avoid These)

**Learned from 2026-01-16 portfolio diagram session:**

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Hex codes in prompts | `#1A8A9B` renders as visible text | Use "teal color" not "#1A8A9B" |
| Vague flow direction | Arrows go random directions | Explicitly state "LEFT TO RIGHT" or "TOP TO BOTTOM" |
| Duplicate labels | Text appears both inside and below elements | Specify "SINGLE label BELOW only, not inside" |
| Implicit positioning | Elements placed confusingly | Use "horizontal row" or "vertical column" explicitly |
| Assumed numbering | Numbers placed inconsistently | State "numbered 1-7 in sequence" |

**Pre-flight checklist for architecture diagrams:**
- [ ] No hex codes - use color names only
- [ ] Flow direction explicitly stated
- [ ] Label position explicitly stated (inside OR below, not both)
- [ ] Layout explicitly stated (horizontal/vertical)
- [ ] Key element highlighting specified

### Site-Specific Style Override (CRITICAL)

**Before generating images for a specific website, CHECK for style guides:**

```bash
# Check project root for style documentation
ls HERO-IMAGE-TEMPLATE.md    # Site-specific image style
ls STYLE-GUIDE.md            # Design system
```

**If found, the site's style guide OVERRIDES the default aesthetic.**

**Default aesthetic.md applies when:** No site-specific style guide exists.

### Consistent Dimensions for Related Images

When generating multiple images for the same page/section:
- Use **identical resize dimensions** for all images
- Document the size used: `# All diagrams: 800x500`
- Prevents distortion when displayed together

---

### Nano Banana Prompting Guide

**For detailed prompting techniques:** `~/.claude/skills/art/nano-banana-guide.md`
**Applies to both Nano Banana 2 and Nano Banana Pro** — same prompt patterns, same API structure.

Includes:
- Core prompt formula: `[Action] the [Subject] by [Specific Change]. The goal is [Desired Outcome].`
- Action verb vocabulary (recolor, retouch, style, adjust, enhance, transform, add, remove, replace, blend)
- Mood and atmosphere vocabulary tables
- Color palette phrases
- Aspect ratio selection guide
- Iterative refinement workflow
- Brand integration template

---

## Quick Decision Tree

```
What does user need?

├─ Unsure which approach? → VISUALIZE (analyzes & orchestrates)
├─ Flowchart/sequence/state diagram? → MERMAID
├─ Abstract metaphor for article? → Editorial (workflow.md)
├─ System/architecture with labels? → Technical Diagram
├─ Categories in grid? → Taxonomy
├─ Change over time? → Timeline
├─ 2x2 matrix or mental model? → Framework
├─ Side-by-side contrast? → Comparison
├─ Markup existing screenshot? → Annotated Screenshot
├─ Step-by-step process? → Recipe Card
├─ Sketchnote or visual meeting notes? → Sketchnote
├─ Quote as social visual? → Aphorism
├─ Idea territories as map? → Conceptual Map
├─ Single striking number? → Stat Card
├─ Multi-panel story? → Comic
└─ Edit/modify/transform existing image? → IMAGE EDITING
```

---

## Platform Constraints

| Platform | Dimensions | Max Size | Notes |
|----------|------------|----------|-------|
| YouTube thumbnail | 1280x720 (16:9) | **2MB** | Use `--size 1080p` or compress after |
| LinkedIn post | 1200x627 | 5MB | |
| Twitter/X post | 1200x675 (16:9) | 5MB | |
| Newsletter header | 1200x600 | 1MB | Email platform limit |
| Instagram square | 1080x1080 | 8MB | |

**If generated image exceeds size limit:**
```bash
# Compress PNG with pngquant
pngquant --quality=65-80 --force --output compressed.png original.png

# Or convert to optimized JPEG
convert original.png -quality 85 compressed.jpg
```

---

## Assimilation Note

**Source:** Personal_AI_Infrastructure Art Skill
**Assimilated:** 2026-01-04
**Adapted:** PAI's dark/neon aesthetic → warm/cream aesthetic

**For complete visual styling rules, ALWAYS read:** `~/.claude/skills/art/aesthetic.md`
