---
name: ia-presenter
description: Writes and validates iA Presenter markdown where tab-indentation controls slide visibility. Triggers on 'presentation', 'iA Presenter', 'slides from markdown', '.presenter file', or when working in iCloud~net~ia~presenter folder. Validates tab characters (not spaces) for visible text, --- slide separators, and image metadata syntax. (user)
---

# iA Presenter Markdown

Write and edit markdown files for iA Presenter, which generates beautiful slides from plain text.

## What is iA Presenter?

iA Presenter is a macOS/iOS/iPadOS app from Information Architects (iA) — the same company that makes iA Writer. It takes markdown files and renders them as presentation slides with automatic responsive layout. The app emphasizes **story-first** presentation design: you write your script, and the design adapts to your content rather than forcing content into templates.

Key differentiator: **visible/speaker notes separation** is controlled by indentation, not by a separate notes panel. This means your markdown file contains both what you show and what you say, distinguished only by whether lines are tab-indented.

## The Core Insight: Visible vs Speaker Notes

iA Presenter's key innovation is separating **what the audience sees** from **what you say** (speaker notes/teleprompter). This is controlled by indentation:

| Element | Visibility | How to Write |
|---------|------------|--------------|
| Headings | ALWAYS visible | `#`, `##`, `###` at line start |
| Tab-indented text | Visible on slide | `⇥Text here` (literal tab character) |
| Plain paragraphs | Speaker notes only | No indent — audience never sees this |
| Images/videos/tables | Visible by default | URL or path on its own line |
| Lists | Visible only if tabbed | `⇥1. Item` or `⇥- Item` |

**The tab character is load-bearing.** A leading tab makes body text visible to the audience. Without it, the text becomes speaker notes (shown in teleprompter, hidden from audience).

## File Format

iA Presenter uses `.iapresenter` bundles (directories), not plain `.md` files:

```
MyPresentation.iapresenter/
├── assets/          # Images, media (optional)
├── info.json        # Metadata
└── text.md          # The markdown content
```

**info.json template:**
```json
{
  "creatorIdentifier" : "net.ia.presenter",
  "net.ia.presenter" : {},
  "transient" : false,
  "type" : "net.daringfireball.markdown",
  "version" : 2
}
```

To create a new presentation programmatically:
1. Create `MyPresentation.iapresenter/` directory
2. Create `assets/` subdirectory (can be empty)
3. Create `info.json` with the template above
4. Create `text.md` with your markdown content

## When to Use

- Creating new presentations in iA Presenter format
- Editing existing `.presenter` or `.md` files for iA Presenter
- Validating that markdown will render correctly as slides
- Converting standard markdown to iA Presenter format
- Working in the `iCloud~net~ia~presenter` folder

## When NOT to Use

- Standard markdown files (no iA Presenter involvement)
- PowerPoint or Google Slides (use pptx skill instead)
- Reveal.js, Marp, or other slide frameworks (different syntax)
- HTML/CSS slide decks

## Slide Structure

### Slide Separation
```markdown
Content for slide 1

---

Content for slide 2
```
Three dashes (`---`) on their own line create a new slide.

### Heading Hierarchy
```markdown
# Title Slide Heading (H1 - largest)
## Section Heading (H2 - major sections)
### Content Heading (H3 - within slides)
```

Headings are ALWAYS visible. Use them for the key message the audience must see.

### Basic Slide Pattern
```markdown
### Visible Heading
	Visible subtitle or key point (TAB-indented)

Speaker notes go here without indentation. The audience never sees this.
You can write as much context as you need for yourself.

---
```

## Text Visibility Examples

### Title Slide
```markdown
	Fast and Focused
# Main Title
	Subtitle line

This introductory paragraph is speaker notes - invisible to audience.
```
Result: Three visible lines stacked (subtitle, title, subtitle), with speaker notes in teleprompter.

### Content Slide
```markdown
### The Key Point
	The heart of a great presentation is the message. Get the script right before anything else.

Most presentation tools ask you to choose a design first. iA Presenter flips the process. You focus on what matters: your story.
```
Result: Heading + one visible paragraph. The longer explanation is speaker notes.

### Multi-Column Layout
```markdown
### Column One
	Description for the first column goes here.

### Column Two
	Description for the second column goes here.

Speaker notes for this slide.
```
Result: Auto-arranges as two columns side-by-side.

### Visible Lists
```markdown
### Table of Contents
	1. Write
	2. Structure
	3. Iterate
	4. Design
	5. Action

The numbered list above is visible because each line is tab-indented.
```

## Images

### Basic Image
```markdown
https://example.com/image.jpg

Or a local path:
/Theme/image.webp
```
Images are visible by default. Just put the URL or path on its own line.

### Image with Metadata
```markdown
https://example.com/screenshot.png
x: left
y: top
title: "Caption text"
```

Available metadata:
- `x:` — horizontal position: `left`, `center`, `right`
- `y:` — vertical position: `top`, `center`, `bottom`
- `size:` — sizing: `contain`, `cover`
- `background:` — `true` to place behind other elements
- `filter:` — `lighten`, `darken`, `grayscale`, `sepia`, `blur`
- `opacity:` — `0%` to `100%`
- `title:` — caption/alt text

### Image Captions with H4
```markdown
#### Caption introducing the image

/assets/photo.jpg
```
Or image first, caption below:
```markdown
/assets/photo.jpg

#### Caption below the image
```

### Multiple Images (Grid)
```markdown
https://example.com/image1.jpg

https://example.com/image2.jpg

https://example.com/image3.jpg

https://example.com/image4.jpg

These images auto-arrange into a grid layout.
```

### Image + Text Layout
```markdown
### Heading on Left
	Visible description text that appears alongside the image.

https://example.com/image.png
x: right
y: top

Speaker notes explaining what we're showing.
```
Result: Text on left, image on right.

## Inline Formatting

Standard markdown formatting works:
- `**bold**` — **bold**
- `*italic*` — *italic*
- `~~strikethrough~~` — strikethrough
- `==highlight==` — highlighted text
- `[link text](url)` — hyperlinks
- `` `code` `` — inline code
- `$x^2$` — inline LaTeX math
- `// comment` — comment (only you see)

## Common Patterns

### Kicker (Small Text Above Title)
```markdown
	Small kicker text
# Main Title
	Subtitle below
```
Tab-indented text directly above a title creates a "kicker" — small headline often seen above main titles.

### Section Divider
```markdown
## 1. Write
	Start With a Script

Brief visible tagline. Then your speaker notes expand on it below.

---
```

### Quote/Callout Slide
```markdown
	**Key insight in bold.** Additional visible context that supports the main point.

The rest of your speaking notes. Expand, give examples, tell stories.
```

### Closing Slide
```markdown
## Now go and move mountains.

Final thoughts in speaker notes. Link to resources: [How-To](https://ia.net/presenter/how-to)
```

## Validation Checklist

When reviewing iA Presenter markdown:

1. **Tab characters exist** — Visible body text MUST start with a literal tab (not spaces)
2. **Slides are separated** — `---` between each slide
3. **One idea per slide** — Keep slides focused
4. **Headings are concise** — They're always visible; make them count
5. **Speaker notes are useful** — Don't waste the teleprompter space
6. **Images have paths** — URLs or local paths on their own lines

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Spaces instead of tabs | Text won't be visible | Use literal tab character |
| Too much visible text | Stuffed slides bore audiences | Move detail to speaker notes |
| Missing `---` | Slides won't separate | Add `---` between slides |
| Forgetting speaker notes | Wasting the teleprompter | Add context below visible content |

## Generating New Presentations

When creating iA Presenter markdown from scratch:

1. **Start with the story** — Write the narrative first
2. **Identify key points** — These become headings
3. **Decide what audience sees** — Tab-indent only essential text
4. **Add speaker notes** — Context, examples, transitions
5. **Add images last** — URLs/paths with positioning metadata
6. **Review slide count** — `---` separators should match intended slides

## Example: Complete Slide

```markdown
### Tell Your Story
	The heart of a great presentation is the message. Get the script right before anything else.

Most presentation tools ask you to choose a design and then adjust your story to fit it. iA Presenter flips the process.

Start with what you want to say. The design comes later, and it adapts to your content — not the other way around.

---
```

**Visible to audience:**
- "Tell Your Story" (heading)
- "The heart of a great presentation..." (tab-indented paragraph)

**Speaker notes (teleprompter only):**
- "Most presentation tools ask you to choose..."
- "Start with what you want to say..."

## Layout Algorithm

Presenter auto-selects layouts based on:
- Number of visual blocks (cells) in the slide
- Types of graphics in each block
- First heading level of each block
- Order of blocks

| Content | Result |
|---------|--------|
| 2-3 elements separated by blank lines | Side-by-side columns |
| 4+ elements | Grid layout |
| H4 + image | Caption layout |
| Image with `background: true` | Background image behind text |

**Cells:** Content separated by blank lines goes into different cells. One element per cell usually looks better.

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Spaces for indentation | Content invisible on slides | MUST use literal tab characters |
| Missing `---` separators | Slides run together | Add `---` between each slide |
| Empty speaker notes | Wasting teleprompter, no speaking context | Add narrative below visible content |
| All-headings slides | Headings are always visible — no notes | Balance headings with tab-indented text |
| Skip validation | Broken slides discovered during presentation | Test in iA Presenter app before presenting |
| Create .md instead of .iapresenter | Won't open correctly in app | Create bundle with text.md + info.json |

## Full Reference

See `references/syntax-reference.md` for complete documentation including:
- All text formatting (highlight, superscript, subscript)
- Footnotes and citations
- LaTeX math
- Code blocks with syntax highlighting
- Tables
- Custom themes and CSS classes
- Layout CSS classes for theming
