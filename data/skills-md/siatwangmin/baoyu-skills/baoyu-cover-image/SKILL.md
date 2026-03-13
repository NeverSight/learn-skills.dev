---
name: baoyu-cover-image
description: Generates article cover images with 4 dimensions (type, style, text, mood) and 20 hand-drawn styles. Supports cinematic (2.35:1), widescreen (16:9), and square (1:1) aspects. Use when user asks to "generate cover image", "create article cover", "make cover", or mentions "封面图".
---

# Cover Image Generator

Generate elegant cover images for articles with 4-dimensional customization.

## Usage

```bash
# Auto-select all dimensions based on content
/baoyu-cover-image path/to/article.md

# Quick mode: skip confirmation, use auto-selection
/baoyu-cover-image article.md --quick

# Specify dimensions
/baoyu-cover-image article.md --type conceptual --style blueprint
/baoyu-cover-image article.md --text title-subtitle --mood bold

# Visual only (no title text)
/baoyu-cover-image article.md --no-title

# Direct content input
/baoyu-cover-image
[paste content]

# Direct input with options
/baoyu-cover-image --style notion --aspect 1:1 --quick
[paste content]
```

## Options

| Option | Description |
|--------|-------------|
| `--type <name>` | Cover type: hero, conceptual, typography, metaphor, scene, minimal |
| `--style <name>` | Cover style (see Style Gallery) |
| `--text <level>` | Text density: none, title-only, title-subtitle, text-rich |
| `--mood <level>` | Emotional intensity: subtle, balanced, bold |
| `--aspect <ratio>` | 16:9 (default), 2.35:1, 4:3, 3:2, 1:1, 3:4 |
| `--lang <code>` | Title language (en, zh, ja, etc.) |
| `--no-title` | Alias for `--text none` |
| `--quick` | Skip confirmation, use auto-selection for missing dimensions |

## Four Dimensions

| Dimension | Controls | Values | Default |
|-----------|----------|--------|---------|
| **Type** | Visual composition, information structure | hero, conceptual, typography, metaphor, scene, minimal | auto |
| **Style** | Visual aesthetics, colors, technique | 20 built-in styles | auto |
| **Text** | Text density, information hierarchy | none, title-only, title-subtitle, text-rich | title-only |
| **Mood** | Emotional intensity, visual weight | subtle, balanced, bold | balanced |

Dimensions can be freely combined. Example: `--type conceptual --style blueprint --text title-only --mood subtle` creates a calm technical concept visualization.

## Type Gallery

| Type | Description | Best For |
|------|-------------|----------|
| `hero` | Large visual impact, title overlay | Product launch, brand promotion, major announcements |
| `conceptual` | Concept visualization, abstract core ideas | Technical articles, methodology, architecture design |
| `typography` | Text-focused layout, prominent title | Opinion pieces, quotes, insights |
| `metaphor` | Visual metaphor, concrete expressing abstract | Philosophy, growth, personal development |
| `scene` | Atmospheric scene, narrative feel | Stories, travel, lifestyle |
| `minimal` | Minimalist composition, generous whitespace | Zen, focus, core concepts |

## Auto Type Selection

When `--type` is omitted, select based on content signals:

| Signals | Type |
|---------|------|
| Product, launch, announcement, release, reveal | `hero` |
| Architecture, framework, system, API, technical, model | `conceptual` |
| Quote, opinion, insight, thought, headline, statement | `typography` |
| Philosophy, growth, abstract, meaning, reflection | `metaphor` |
| Story, journey, travel, lifestyle, experience, narrative | `scene` |
| Zen, focus, essential, core, simple, pure | `minimal` |

## Style Gallery

| Style | Description |
|-------|-------------|
| `elegant` (default) | Refined, sophisticated |
| `blueprint` | Technical schematics |
| `bold-editorial` | Magazine impact |
| `chalkboard` | Chalk on blackboard |
| `dark-atmospheric` | Cinematic dark mode |
| `editorial-infographic` | Visual storytelling |
| `fantasy-animation` | Ghibli/Disney inspired |
| `flat-doodle` | Pastel, cute shapes |
| `intuition-machine` | Technical, bilingual |
| `minimal` | Ultra-clean, zen |
| `nature` | Organic, earthy |
| `notion` | SaaS dashboard |
| `pixel-art` | Retro 8-bit |
| `playful` | Fun, whimsical |
| `retro` | Halftone, vintage |
| `sketch-notes` | Hand-drawn, warm |
| `vector-illustration` | Flat vector |
| `vintage` | Aged, expedition |
| `warm` | Friendly, human |
| `watercolor` | Soft hand-painted |

Style definitions: [references/styles/](references/styles/)

## Auto Style Selection

When `--style` is omitted, select based on content signals:

| Signals | Style |
|---------|-------|
| Architecture, system design | `blueprint` |
| Product launch, marketing | `bold-editorial` |
| Education, tutorial | `chalkboard` |
| Entertainment, premium | `dark-atmospheric` |
| Tech explainer, research | `editorial-infographic` |
| Fantasy, children | `fantasy-animation` |
| Technical docs, bilingual | `intuition-machine` |
| Personal story, emotion | `warm` |
| Zen, focus, essential | `minimal` |
| Fun, beginner, casual | `playful` |
| Nature, wellness, eco | `nature` |
| SaaS, dashboard | `notion` |
| Workflow, productivity | `flat-doodle` |
| Gaming, retro tech | `pixel-art` |
| Knowledge sharing | `sketch-notes` |
| Creative proposals | `vector-illustration` |
| History, exploration | `vintage` |
| Lifestyle, travel | `watercolor` |
| Business, professional | `elegant` |

## Text Dimension

| Value | Title | Subtitle | Tags | Use Case |
|-------|:-----:|:--------:|:----:|----------|
| `none` | - | - | - | Pure visual, no text |
| `title-only` | ✓ (≤8字) | - | - | Simple headline (default) |
| `title-subtitle` | ✓ | ✓ (≤15字) | - | Title + supporting context |
| `text-rich` | ✓ | ✓ | ✓ (2-4) | Information-dense |

Full guide: [references/dimensions/text.md](references/dimensions/text.md)

## Auto Text Selection

When `--text` is omitted, select based on content signals:

| Signals | Text Level |
|---------|------------|
| Visual-only, photography, abstract, art | `none` |
| Article, blog, standard cover | `title-only` |
| Series, tutorial, technical with context | `title-subtitle` |
| Announcement, features, multiple points, infographic | `text-rich` |

Default: `title-only`

## Mood Dimension

| Value | Contrast | Saturation | Weight | Use Case |
|-------|:--------:|:----------:|:------:|----------|
| `subtle` | Low | Muted | Light | Corporate, thought leadership |
| `balanced` | Medium | Normal | Medium | General articles (default) |
| `bold` | High | Vivid | Heavy | Announcements, promotions |

Full guide: [references/dimensions/mood.md](references/dimensions/mood.md)

## Auto Mood Selection

When `--mood` is omitted, select based on content signals:

| Signals | Mood Level |
|---------|------------|
| Professional, corporate, thought leadership, academic, luxury | `subtle` |
| General, educational, standard, blog, documentation | `balanced` |
| Launch, announcement, promotion, event, gaming, entertainment | `bold` |

Default: `balanced`

## Compatibility Matrices

### Type × Style

| | elegant | blueprint | notion | warm | minimal | watercolor | bold-editorial | dark-atmospheric |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| hero | ✓✓ | ✓ | ✓ | ✓✓ | ✓ | ✓✓ | ✓✓ | ✓✓ |
| conceptual | ✓✓ | ✓✓ | ✓✓ | ✓ | ✓✓ | ✗ | ✓ | ✓ |
| typography | ✓✓ | ✓ | ✓✓ | ✓ | ✓✓ | ✓ | ✓✓ | ✓✓ |
| metaphor | ✓✓ | ✗ | ✓ | ✓✓ | ✓ | ✓✓ | ✓ | ✓ |
| scene | ✓ | ✗ | ✗ | ✓✓ | ✓ | ✓✓ | ✓ | ✓✓ |
| minimal | ✓✓ | ✓ | ✓✓ | ✓ | ✓✓ | ✓ | ✗ | ✓ |

### Type × Text

| | none | title-only | title-subtitle | text-rich |
|---|:---:|:---:|:---:|:---:|
| hero | ✓ | ✓✓ | ✓✓ | ✓ |
| conceptual | ✓✓ | ✓✓ | ✓ | ✓ |
| typography | ✗ | ✓ | ✓✓ | ✓✓ |
| metaphor | ✓✓ | ✓ | ✓ | ✗ |
| scene | ✓✓ | ✓ | ✓ | ✗ |
| minimal | ✓✓ | ✓✓ | ✓ | ✗ |

### Type × Mood

| | subtle | balanced | bold |
|---|:---:|:---:|:---:|
| hero | ✓ | ✓✓ | ✓✓ |
| conceptual | ✓✓ | ✓✓ | ✓ |
| typography | ✓ | ✓✓ | ✓✓ |
| metaphor | ✓✓ | ✓✓ | ✓ |
| scene | ✓✓ | ✓✓ | ✓ |
| minimal | ✓✓ | ✓✓ | ✗ |

✓✓ = highly recommended | ✓ = compatible | ✗ = not recommended

## File Structure

Output directory depends on `default_output_dir` preference:

| Preference | Output Path |
|------------|-------------|
| `same-dir` | `{article-dir}/` |
| `imgs-subdir` | `{article-dir}/imgs/` |
| `independent` (default) | `cover-image/{topic-slug}/` |
| Pasted content | `cover-image/{topic-slug}/` (always) |

```
<output-dir>/
├── source-{slug}.{ext}    # Source files (text, images, etc.)
├── prompts/cover.md       # Generation prompt
└── cover.png              # Output image
```

**Slug Generation**:
1. Extract main topic from content (2-4 words, kebab-case)
2. Example: "The Future of AI" → `future-of-ai`

**Conflict Resolution**:
If `cover-image/{topic-slug}/` already exists:
- Append timestamp: `{topic-slug}-YYYYMMDD-HHMMSS`
- Example: `ai-future` exists → `ai-future-20260118-143052`

**Source Files**:
Copy all sources with naming `source-{slug}.{ext}`:
- `source-article.md`, `source-reference.png`, etc.
- Multiple sources supported: text, images, files from conversation

## Workflow

### Progress Checklist

Copy and track progress:

```
Cover Image Progress:
- [ ] Step 0: Check preferences (EXTEND.md) ⚠️ REQUIRED if not found
- [ ] Step 1: Analyze content + determine output directory ⚠️ MUST ask if not configured
- [ ] Step 2: Confirm options (4 dimensions) ⚠️ REQUIRED unless --quick or all specified
- [ ] Step 3: Create prompt
- [ ] Step 4: Generate image
- [ ] Step 5: Completion report
```

### Flow

```
Input → [Step 0: Preferences/Setup] → Analyze → [Output Dir ⚠️] → [Confirm: 4 Dimensions] → Prompt → Generate → Complete
                                                                          ↓
                                                                  (skip if --quick or all specified)
```

### Step 0: Load Preferences (EXTEND.md) ⚠️

**Purpose**: Load user preferences or run first-time setup. **Do NOT skip setup if EXTEND.md not found.**

Use Bash to check EXTEND.md existence (priority order):

```bash
# Check project-level first
test -f .baoyu-skills/baoyu-cover-image/EXTEND.md && echo "project"

# Then user-level (cross-platform: $HOME works on macOS/Linux/WSL)
test -f "$HOME/.baoyu-skills/baoyu-cover-image/EXTEND.md" && echo "user"
```

┌──────────────────────────────────────────────────┬───────────────────┐
│                       Path                       │     Location      │
├──────────────────────────────────────────────────┼───────────────────┤
│ .baoyu-skills/baoyu-cover-image/EXTEND.md        │ Project directory │
├──────────────────────────────────────────────────┼───────────────────┤
│ $HOME/.baoyu-skills/baoyu-cover-image/EXTEND.md  │ User home         │
└──────────────────────────────────────────────────┴───────────────────┘

┌───────────┬───────────────────────────────────────────────────────────────────────────┐
│  Result   │                                  Action                                   │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Found     │ Read, parse, display preferences summary (see below) → Continue to Step 1 │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Not found │ ⚠️ MUST run first-time setup (see below) → Then continue to Step 1        │
└───────────┴───────────────────────────────────────────────────────────────────────────┘

**Preferences Summary** (when EXTEND.md found):

Display loaded preferences:

```
Preferences loaded from [project/user]:
• Watermark: [enabled/disabled] [content if enabled]
• Type: [preferred_type or "auto"]
• Style: [preferred_style or "auto"]
• Text: [preferred_text or "title-only"]
• Mood: [preferred_mood or "balanced"]
• Aspect: [default_aspect]
• Output: [default_output_dir or "not set — will ask in Step 1.5"]
• Quick mode: [enabled/disabled]
• Language: [language or "auto"]
```

**First-Time Setup** (when EXTEND.md not found):

**Language**: Use user's input language or saved language preference.

Use AskUserQuestion with ALL questions in ONE call:

**Q1: Watermark**
```yaml
header: "Watermark"
question: "Watermark text for generated cover images?"
options:
  - label: "No watermark (Recommended)"
    description: "Clean covers, can enable later in EXTEND.md"
```

**Q2: Preferred Type**
```yaml
header: "Type"
question: "Default cover type preference?"
options:
  - label: "Auto-select (Recommended)"
    description: "Choose based on content analysis each time"
  - label: "hero"
    description: "Large visual impact - product launch, announcements"
  - label: "conceptual"
    description: "Concept visualization - technical, architecture"
```

**Q3: Preferred Style**
```yaml
header: "Style"
question: "Default cover style preference?"
options:
  - label: "Auto-select (Recommended)"
    description: "Choose based on content analysis each time"
  - label: "elegant"
    description: "Refined, sophisticated - professional business"
  - label: "notion"
    description: "SaaS dashboard - productivity/tech content"
```

**Q4: Default Aspect Ratio**
```yaml
header: "Aspect"
question: "Default aspect ratio for cover images?"
options:
  - label: "16:9 (Recommended)"
    description: "Standard widescreen - YouTube, presentations, versatile"
  - label: "2.35:1"
    description: "Cinematic widescreen - article headers, blog posts"
  - label: "1:1"
    description: "Square - Instagram, WeChat, social cards"
  - label: "3:4"
    description: "Portrait - Xiaohongshu, Pinterest, mobile content"
```

Note: More ratios (4:3, 3:2) available during generation. This sets the default recommendation.

**Q5: Default Output Directory**
```yaml
header: "Output"
question: "Default output directory for cover images?"
options:
  - label: "Independent (Recommended)"
    description: "cover-image/{topic-slug}/ - separate from article"
  - label: "Same directory"
    description: "{article-dir}/ - alongside the article file"
  - label: "imgs subdirectory"
    description: "{article-dir}/imgs/ - images folder near article"
```

**Q6: Quick Mode**
```yaml
header: "Quick"
question: "Enable quick mode by default?"
options:
  - label: "No (Recommended)"
    description: "Confirm dimension choices each time"
  - label: "Yes"
    description: "Skip confirmation, use auto-selection"
```

**Q7: Save Location**
```yaml
header: "Save"
question: "Where to save preferences?"
options:
  - label: "Project (Recommended)"
    description: ".baoyu-skills/ (this project only)"
  - label: "User"
    description: "~/.baoyu-skills/ (all projects)"
```

**After setup**: Create EXTEND.md with user choices, then continue to Step 1.

Full setup details: `references/config/first-time-setup.md`

**EXTEND.md Supports**: Watermark | Preferred type | Preferred style | Preferred text | Preferred mood | Default aspect ratio | Default output directory | Quick mode | Custom style definitions | Language preference

Schema: `references/config/preferences-schema.md`

### Step 1: Analyze Content

Read source content, save it if needed, and perform analysis.

**Actions**:
1. **Save source content** (if not already a file):
   - If user provides a file path: use as-is
   - If user pastes content: save to `source.md` in target directory
2. Read source content
3. **Content analysis**:
   - Extract: topic, core message, tone, keywords
   - Identify visual metaphor opportunities
   - Detect content type (technical/personal/business/creative)
4. **Language detection**:
   - Detect source content language
   - Note user's input language (from conversation)
   - Compare with language preference in EXTEND.md

**1.5 Determine Output Directory** ⚠️

**MUST ask user when `default_output_dir` is not set in EXTEND.md and input is a file path.**

| Input | Behavior |
|-------|----------|
| File path + preference set | Use configured `default_output_dir` |
| File path + **no preference** | ⚠️ **MUST** ask with AskUserQuestion ↓ |
| Pasted content | `cover-image/{topic-slug}/` (always independent) |

`default_output_dir` preference values:

| Preference Value | Output Path |
|------------------|-------------|
| `same-dir` | `{article-dir}/` |
| `imgs-subdir` | `{article-dir}/imgs/` |
| `independent` | `cover-image/{topic-slug}/` |

**AskUserQuestion** (when no preference, file path input only):
- `{article-dir}/imgs/` - Images subdirectory near article
- `{article-dir}/` - Same directory as article
- `cover-image/{topic-slug}/` - Independent directory
- Save as default - Remember this choice for future runs

### Step 2: Confirm Options ⚠️

**Purpose**: Validate all 4 dimensions + aspect ratio.

**Skip Conditions**:
| Condition | Skipped Questions | Still Asked |
|-----------|-------------------|-------------|
| `--quick` flag | Type, Style, Text, Mood | **Aspect Ratio** (unless `--aspect` specified) |
| All 4 dimensions + `--aspect` specified | All | None |
| `quick_mode: true` in EXTEND.md | Type, Style, Text, Mood | **Aspect Ratio** (unless `--aspect` specified) |
| Otherwise | None | All 5 questions |

**Important**: Aspect ratio is ALWAYS asked unless explicitly specified via `--aspect` CLI flag. User presets in EXTEND.md are shown as recommended option, not auto-selected.

**Quick Mode Output** (when skipping 4 dimensions):

```
Quick Mode: Auto-selected dimensions
• Type: [type] ([reason])
• Style: [style] ([reason])
• Text: [text] ([reason])
• Mood: [mood] ([reason])

[Then ask Question 5: Aspect Ratio]
```

**Confirmation Flow** (when NOT skipping):

**Language**: Auto-determined (user's input language > saved preference > source language). No need to ask.

Present options using AskUserQuestion:

**Question 1: Type** (if not specified via `--type`)
- Show recommended type based on content analysis + preferred type from EXTEND.md

```yaml
header: "Type"
question: "Which cover type?"
multiSelect: false
options:
  - label: "[auto-recommended type] (Recommended)"
    description: "[reason based on content signals]"
  - label: "hero"
    description: "Large visual impact, title overlay - product launch, announcements"
  - label: "conceptual"
    description: "Concept visualization - technical, architecture"
  - label: "typography"
    description: "Text-focused layout - opinions, quotes"
```

**Question 2: Style** (if not specified via `--style`)
- Based on selected Type, show compatible styles (✓✓ first from compatibility matrix)
- Format: `[style name] - [why it fits this content]`

```yaml
header: "Style"
question: "Which cover style?"
multiSelect: false
options:
  - label: "[best compatible style] (Recommended)"
    description: "[reason based on type + content]"
  - label: "[style2]"
    description: "[reason]"
  - label: "[style3]"
    description: "[reason]"
```

**Question 3: Text** (if not specified via `--text`)
- Based on selected Type, show compatible text levels (✓✓ first from compatibility matrix)

```yaml
header: "Text"
question: "Text density level?"
multiSelect: false
options:
  - label: "title-only (Recommended)"
    description: "Simple headline, ≤8 characters"
  - label: "none"
    description: "Pure visual, no text elements"
  - label: "title-subtitle"
    description: "Title + supporting context"
  - label: "text-rich"
    description: "Title + subtitle + keyword tags"
```

**Question 4: Mood** (if not specified via `--mood`)
- Based on content analysis, show recommended mood

```yaml
header: "Mood"
question: "Emotional intensity?"
multiSelect: false
options:
  - label: "balanced (Recommended)"
    description: "Medium contrast and saturation, versatile"
  - label: "subtle"
    description: "Low contrast, muted colors, calm"
  - label: "bold"
    description: "High contrast, vivid colors, dynamic"
```

**Question 5: Aspect Ratio** (ALWAYS ask unless `--aspect` specified via CLI)

Note: Even if user has a preset in EXTEND.md, still ask this question. The preset is shown as the recommended option.

```yaml
header: "Aspect"
question: "Cover aspect ratio?"
multiSelect: false
options:
  - label: "[user preset or 16:9] (Recommended)"
    description: "[based on preset or default: Standard widescreen, versatile]"
  - label: "2.35:1"
    description: "Cinematic widescreen - article headers, blog posts"
  - label: "4:3"
    description: "Traditional screen - PPT slides, classic displays"
  - label: "3:2"
    description: "Photography ratio - blog articles, Medium posts"
  - label: "1:1"
    description: "Square - Instagram, WeChat moments, social cards"
  - label: "3:4"
    description: "Portrait - Xiaohongshu, Pinterest, mobile-first content"
```

**After response**: Proceed to Step 3 with confirmed dimensions.

### Step 3: Create Prompt

Save to `prompts/cover.md`:

```markdown
# Content Context
Article title: [full original title from source]
Content summary: [2-3 sentence summary of key points and themes]
Keywords: [5-8 key terms extracted from content]

# Visual Design
Cover theme: [2-3 words visual interpretation]
Type: [confirmed type]
Style: [confirmed style]
Text level: [confirmed text level]
Mood: [confirmed mood]
Aspect ratio: [confirmed ratio]
Language: [confirmed language]

# Text Elements
[Based on text level:]
- none: "No text elements"
- title-only: "Title: [max 8 chars headline]"
- title-subtitle: "Title: [headline] / Subtitle: [max 15 chars context]"
- text-rich: "Title: [headline] / Subtitle: [context] / Tags: [2-4 keywords]"

# Mood Application
[Based on mood level:]
- subtle: "Use low contrast, muted colors, light visual weight, calm aesthetic"
- balanced: "Use medium contrast, normal saturation, balanced visual weight"
- bold: "Use high contrast, vivid saturated colors, heavy visual weight, dynamic energy"

# Composition
Type composition:
- [Type-specific layout and structure]

Visual composition:
- Main visual: [metaphor derived from content meaning]
- Layout: [positioning based on type and aspect ratio]
- Decorative: [style elements that reinforce content theme]

Color scheme: [primary, background, accent from style, adjusted by mood]
Type notes: [key characteristics from type definition]
Style notes: [key characteristics from style definition]

[Watermark section if enabled]
```

**Content-Driven Design**:
- Article title and summary inform the visual metaphor choice
- Keywords guide decorative elements and symbols
- The skill controls visual style; the content drives meaning

**Type-Specific Composition**:

| Type | Composition Guidelines |
|------|------------------------|
| `hero` | Large focal visual (60-70% area), title overlay on visual, dramatic composition |
| `conceptual` | Abstract shapes representing core concepts, information hierarchy, clean zones |
| `typography` | Title as primary element (40%+ area), minimal supporting visuals, strong hierarchy |
| `metaphor` | Concrete object/scene representing abstract idea, symbolic elements, emotional resonance |
| `scene` | Atmospheric environment, narrative elements, mood-setting lighting and colors |
| `minimal` | Single focal element, generous whitespace (60%+), essential shapes only |

**Title guidelines** (when text level includes title):
- Max 8 characters, punchy headline
- Use hooks: numbers, questions, contrasts
- Match confirmed language

**Watermark Application** (if enabled in preferences):
Add to prompt:
```
Include a subtle watermark "[content]" positioned at [position].
The watermark should be legible but not distracting from the main content.
```
Reference: `references/config/watermark-guide.md`

### Step 4: Generate Image

**Backup Existing Cover** (if regenerating):
If `cover.png` already exists in the output directory:
- Rename to `cover-backup-YYYYMMDD-HHMMSS.png`

**Image Generation Skill Selection**:
1. Check available image generation skills
2. If multiple skills available, ask user preference
3. Call selected skill with:
   - Prompt file path
   - Output image path: `cover.png`
   - Aspect ratio parameter

**On failure**: Auto-retry once before reporting error.

### Step 5: Completion Report

```
Cover Generated!

Topic: [topic]
Type: [type name]
Style: [style name]
Text: [text level]
Mood: [mood level]
Aspect: [ratio]
Title: [title text or "visual only"]
Language: [lang]
Watermark: [enabled/disabled]
Location: [directory path]

Files:
✓ source-{slug}.{ext}
✓ prompts/cover.md
✓ cover.png
[✓ cover-backup-{timestamp}.png (if regenerated)]
```

## Image Modification

| Action | Steps |
|--------|-------|
| **Regenerate** | Backup existing → Update prompt → Regenerate with same settings |
| **Change type** | Backup existing → Confirm new type → Update prompt → Regenerate |
| **Change style** | Backup existing → Confirm new style → Update prompt → Regenerate |
| **Change text** | Backup existing → Confirm new text level → Update prompt → Regenerate |
| **Change mood** | Backup existing → Confirm new mood → Update prompt → Regenerate |
| **Change aspect** | Backup existing → Confirm new aspect → Update prompt → Regenerate |

All modifications automatically backup the existing `cover.png` before regenerating.

## Notes

- Cover must be readable at small preview sizes
- Visual metaphors > literal representations
- Title: max 8 chars, readable, impactful
- **Two confirmation points**: Step 0 (first-time setup if no EXTEND.md) + Step 2 (options) - can skip Step 2 with `--quick`
- Use confirmed language for title text
- Maintain watermark consistency if enabled
- Check compatibility matrices when selecting combinations
- `--no-title` is preserved as alias for `--text none`

## References

**Dimensions**:
- `references/dimensions/text.md` - Text density dimension
- `references/dimensions/mood.md` - Mood intensity dimension

**Styles**: `references/styles/<name>.md` - Style definitions

**Config**:
- `references/config/preferences-schema.md` - EXTEND.md schema
- `references/config/first-time-setup.md` - First-time setup flow
- `references/config/watermark-guide.md` - Watermark configuration

## Extension Support

Custom configurations via EXTEND.md. See **Step 0** for paths and supported options.
