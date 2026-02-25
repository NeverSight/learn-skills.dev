---
name: xhs-images
description: Xiaohongshu (Little Red Book) infographic series generator with multiple style options. Breaks down content into 1-10 cartoon-style infographics. Use when user asks to create "小红书图片", "XHS images", or "RedNote infographics".
---

# Xiaohongshu Infographic Series Generator

Break down complex content into eye-catching infographic series for Xiaohongshu.

## Usage

```bash
# Auto-select style and layout based on content
/xhs-images posts/ai-future/article.md

# Specify style
/xhs-images posts/ai-future/article.md --style notion

# Specify layout
/xhs-images posts/ai-future/article.md --layout dense

# Combine style and layout
/xhs-images posts/ai-future/article.md --style tech --layout list

# Direct content input
/xhs-images
[paste content]
```

## Options

| Option | Description |
|--------|-------------|
| `--style <name>` | Visual style (see Style Gallery below) |
| `--layout <name>` | Information layout (see Layout Gallery below) |

## Two Dimensions

| Dimension | Controls | Options |
|-----------|----------|---------|
| **Style** | Visual aesthetics: colors, lines, decorations | cute, fresh, tech, warm, bold, minimal, retro, pop, notion, productivity, insight |
| **Layout** | Information structure: density, arrangement | sparse, balanced, dense, list, comparison, flow |

Style × Layout can be freely combined. Example: `--style notion --layout dense` creates an intellectual-looking knowledge card with high information density.

## Style Gallery (Quick Reference)

| Style | Description | Best For |
|-------|-------------|----------|
| `cute` | Sweet, adorable, girly - classic XHS aesthetic | Lifestyle, beauty, fashion |
| `fresh` | Clean, refreshing, natural | Health, wellness, self-care |
| `tech` | Modern, smart, digital | Tech tutorials, AI content |
| `warm` | Cozy, friendly, approachable | Personal stories, life lessons |
| `bold` | High impact, attention-grabbing | Important tips, warnings |
| `minimal` | Ultra-clean, sophisticated | Professional content |
| `retro` | Vintage, nostalgic, trendy | Throwback, classic tips |
| `pop` | Vibrant, energetic, eye-catching | Fun facts, announcements |
| `notion` | Minimalist hand-drawn line art | Knowledge sharing, SaaS |
| `productivity` | Structured, light mode, clean UI | How-to tutorials, tools |
| `insight` | High clarity, dark mode, premium | Mental models, deep thoughts |

**For detailed style specs (colors, elements, typography)**: See `references/styles.md`

## Layout Gallery (Quick Reference)

| Layout | Density | Best For |
|--------|---------|----------|
| `sparse` | 1-2 points, 60-70% whitespace | Covers, quotes, impactful statements |
| `balanced` | 3-4 points, 40-50% whitespace | Regular content, tutorials |
| `dense` | 5-8 points, 20-30% whitespace | Summary cards, cheat sheets |
| `list` | 4-7 items, 30-40% whitespace | Top N lists, checklists |
| `comparison` | 2×2-4 points, 30-40% whitespace | Before/After, pros/cons |
| `flow` | 3-6 steps, 30-40% whitespace | Processes, timelines |

**For detailed layout specs and Style×Layout matrix**: See `references/layouts.md`

## Auto Selection Logic

### Auto Style Selection

| Content Signals | Selected Style |
|----------------|----------------|
| Beauty, fashion, cute, girl, pink | `cute` |
| Health, nature, clean, fresh | `fresh` |
| Tech, AI, code, digital, app, tool | `tech` |
| Life, story, emotion, feeling | `warm` |
| Warning, important, must, critical | `bold` |
| Professional, business, elegant | `minimal` |
| Classic, vintage, old, traditional | `retro` |
| Fun, exciting, wow, amazing | `pop` |
| Knowledge, concept, productivity, SaaS | `notion` |
| How-to, tutorial, tool recommendation | `productivity` |
| Mental model, deep thought, insight | `insight` |

### Auto Layout Selection

| Content Signals | Selected Layout |
|----------------|-----------------|
| Single quote, one key point, cover | `sparse` |
| 3-4 points, explanation, tutorial | `balanced` |
| 5+ points, summary, cheat sheet | `dense` |
| Numbered items, top N, checklist | `list` |
| vs, compare, before/after, pros/cons | `comparison` |
| Process, flow, timeline, ordered steps | `flow` |

### Layout by Position

| Position | Recommended Layout |
|----------|-------------------|
| Cover | `sparse` |
| Content | `balanced` / `dense` / `list` (content-appropriate) |
| Ending | `sparse` or `balanced` |

## File Management

### With Article Path

Save to `xhs-images/` subdirectory in the same folder as the article:

```
posts/ai-future/
├── article.md
└── xhs-images/
    ├── outline.md
    ├── prompts/
    │   ├── 01-cover.md
    │   └── ...
    ├── 01-cover.png
    └── 02-ending.png
```

### Without Article Path

Save to `xhs-outputs/YYYY-MM-DD/[topic-slug]/`

## Workflow

### Step 1: Analyze Content & Select Style/Layout

1. Read content
2. If `--style` specified, use that style; otherwise auto-select
3. If `--layout` specified, use that layout; otherwise auto-select per image
4. Determine image count:
   - Simple topic: 2-3 images
   - Medium complexity: 4-6 images
   - Deep dive: 7-10 images

### Step 2: Generate Outline

Plan for each image with style and layout specifications. Save as `outline.md`:

```markdown
# Xiaohongshu Infographic Series Outline

**Topic**: [topic]
**Style**: [selected style]
**Default Layout**: [selected layout or "varies"]
**Image Count**: N
**Generated**: YYYY-MM-DD HH:mm

---

## Image 1 of N

**Position**: Cover
**Layout**: sparse
**Core Message**: [one-liner]
**Filename**: 01-cover.png

**Text Content**:
- Title: xxx
- Subtitle: xxx

**Visual Concept**: [style + layout appropriate description]

---
...
```

### Step 3: Generate Images One by One

For each image:

1. Read style details from `references/styles.md` (load target style section only)
2. Read layout details from `references/layouts.md` (load target layout section only)
3. Create prompt file in `prompts/` directory
4. Generate using:

```bash
/gemini-web --promptfiles [SKILL_ROOT]/prompts/system.md [TARGET_DIR]/prompts/01-cover.md --image [TARGET_DIR]/01-cover.png
```

**Prompt Format**:

```markdown
Infographic theme: [topic]
Style: [style name]
Layout: [layout name]
Position: [cover/content/ending]

Visual composition:
- Main visual: [style-appropriate description]
- Arrangement: [layout-specific structure]
- Decorative elements: [style-specific decorations]

Color scheme:
- Primary: [from style spec]
- Background: [from style spec]
- Accent: [from style spec]

Text content:
- Title: 「xxx」(large, prominent)
- Key points: [based on layout density]

Layout instructions: [from layout spec]
Style notes: [from style spec]
```

### Step 4: Completion Report

```
Xiaohongshu Infographic Series Complete!

Topic: [topic]
Style: [style name]
Layout: [layout name or "varies"]
Location: [directory path]
Images: N total

- 01-cover.png ✓ Cover (sparse)
- 02-content-1.png ✓ Content (balanced)
- 03-ending.png ✓ Ending (sparse)

Outline: outline.md
```

## Content Breakdown Principles

1. **Cover (Image 1)**: Strong visual impact, core title, attention hook → `sparse` layout
2. **Content (Middle)**: Core points per image, density varies by content
3. **Ending (Last)**: Summary / call-to-action / memorable quote → `sparse` or `balanced`

## Notes

- Image generation typically takes 10-30 seconds per image
- Auto-retry once on generation failure
- Use cartoon alternatives for sensitive public figures
- Output language matches input content language
- Maintain selected style consistency across all images in series
