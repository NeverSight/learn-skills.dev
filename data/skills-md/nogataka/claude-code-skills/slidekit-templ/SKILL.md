---
name: slidekit-templ
description: "Convert PDF presentations to HTML slide templates using a visual reproduction approach. Pipeline: PDF → slide screenshots → Claude writes HTML matching each screenshot. Use when the user wants to convert a PDF to HTML slide templates, reproduce a presentation as HTML, or create reusable templates from existing decks. Triggers: 'pdf to html', 'convert pdf to template', 'reproduce this deck as html', 'create template from pdf'."
---

# PDF to HTML Slide Converter

Convert PDF presentations to high-fidelity HTML slides by visually reproducing each slide from screenshots.

## Pipeline

```
PDF → (pdftoppm) → Slide images
                        ↓
    Claude reads each image + writes HTML
                        ↓
         001.html, 002.html, ... + print.html
```

## Dependencies

```bash
brew install poppler
```

## Workflow

### Phase 1: Generate Slide Images

```bash
python ~/.claude/skills/pdf-to-html/scripts/pdf_to_images.py input.pdf output_dir
```

This produces `output_dir/slide-01.jpg`, `slide-02.jpg`, etc.

### Phase 2: Analyze the Deck

Before writing any HTML:

1. Read ALL slide images to understand the full deck
2. Identify the **color palette** (3-4 colors: primary dark, accent, secondary)
3. Identify the **font style** (serif/sans-serif, weight patterns)
4. Note the **header/footer pattern** used across content slides
5. Note the **overall style** (creative, elegant, modern, professional, minimalist)

### Phase 3: Load Design System

Read these files to load the HTML design system rules:

1. `~/.claude/skills/slidekit-create/SKILL.md` — Mandatory constraints, PPTX conversion rules, anti-patterns, design guidelines, HTML boilerplate, pre-delivery checklist
2. `~/.claude/skills/slidekit-create/references/patterns.md` — 15 layout patterns with DOM trees, component snippets

**All rules in slidekit-create apply.** Key constraints:

- Slide size: 1280x720px
- Tailwind CSS 2.2.19 + Font Awesome 6.4.0 + Google Fonts via CDN
- No JavaScript
- Root DOM: `<body>` → single wrapper `<div>`
- Text in `<p>` / `<h*>` (not `<div>`)
- No text in `::before` / `::after`

### Phase 4: Write HTML Slides

For each slide image, one at a time:

1. **Read the slide image** carefully
2. **Pick the closest layout pattern** from slidekit-create's 15 patterns
3. **Write the HTML** that visually reproduces the slide:
   - Match colors precisely (use hex values observed in the image)
   - Match text content exactly (all text, numbers, labels)
   - Match spatial layout (element positions, proportions)
   - Use the consistent header/footer across content slides
   - Use Font Awesome icons where the original has icons or bullets
4. **Save as** `{output_dir}/{NNN}.html` (zero-padded: 001.html, 002.html, ...)

#### HTML Boilerplate

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <title>{Slide Title}</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family={PrimaryFont}:wght@300;400;500;700;900&family={AccentFont}:wght@400;600;700&display=swap" rel="stylesheet" />
    <style>
        body { margin: 0; padding: 0; font-family: '{PrimaryFont}', sans-serif; overflow: hidden; }
        .font-accent { font-family: '{AccentFont}', sans-serif; }
        .slide { width: 1280px; height: 720px; position: relative; overflow: hidden; }
        /* Custom color classes: .bg-brand-dark, .bg-brand-accent, .bg-brand-sub, etc. */
    </style>
</head>
<body>
    <div class="slide">
        <!-- Content -->
    </div>
</body>
</html>
```

### Phase 5: Generate print.html

After all slides are written, generate `{output_dir}/print.html`:

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8" />
    <title>View for Print</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #FFFFFF; }
        .slide-frame {
            width: 1280px; height: 720px;
            margin: 20px auto;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            border: 1px solid #e2e8f0;
            overflow: hidden;
        }
        .slide-frame iframe { width: 1280px; height: 720px; border: none; }
        @media print {
            body { background: #FFFFFF; }
            .slide-frame {
                page-break-after: always; box-shadow: none; border: none;
                margin: 0 auto;
                transform: scale(0.85); transform-origin: top center;
            }
        }
    </style>
</head>
<body>
    <!-- One iframe per slide -->
    <div class="slide-frame"><iframe src="001.html"></iframe></div>
    ...
</body>
</html>
```

### Phase 6: Visual QA

**Compare each generated HTML against the original screenshot.**

For each slide:

1. Read the original slide image (`slide-NN.jpg`)
2. Read the generated HTML file
3. Check for:
   - Missing or incorrect text
   - Wrong colors or color contrast issues
   - Layout misalignment (elements shifted, wrong proportions)
   - Missing decorative elements (bars, shapes, badges)
   - Overflow or clipping issues
4. Fix any issues found
5. Re-verify after fixes

Do not declare success until at least one full comparison pass reveals no issues.
