---
name: perfect-presentation
description: >
  Use this skill when creating ANY presentation, slide deck, or .pptx file.
  Triggers: "зроби презентацію", "create presentation", "make slides", "pitch deck",
  any topic + "presentation". Generates Python code using python-pptx library.
  Requirements: ≥15 slides, deep research, infographics, academic design,
  citations on every slide, speaker notes 800–2000 words per slide.
version: 2.0.0
---

# Perfect Presentation Skill

## Core Rules (NEVER break these)

1. **Output is Python code only** — never write slide content as plain text, only as `python-pptx` code
2. **≥15 slides** — always
3. **Language** — match the language the user specifies; default to English
4. **Academic & technical** — highly professional, specific, no filler content
5. **Citations mandatory** — cite sources at the bottom of every slide AND in notes
6. **Speaker notes 800–2000 words** — explain every bullet point in depth
7. **Popular-science + empathetic tone** in notes — ideal for beginner students
8. **Never use placeholder text** — all content must be real, researched, specific

---

## Phase 1 — Deep Research (MANDATORY before writing any code)

Before writing a single line of Python, research the topic thoroughly.

### Research Checklist

```
□ Core definition and scope (with authoritative source)
□ Historical background and key milestones (with years)
□ Key statistics and quantitative data (with source + year)
□ Major current trends (with evidence)
□ Key organizations, researchers, or companies involved
□ Challenges and open problems
□ Future outlook and predictions
□ At least 2 real case studies with measurable outcomes
□ Expert quotes or frameworks (cited)
□ Contrasting viewpoints or debates in the field
```

### Source Citation Format

Use this format for citations on slides and in notes:

```
On slide (bottom footer):  [Author/Org, Year] or [URL shortened]
In notes (full citation):  Author, A. (Year). Title. Publisher/URL. DOI if available.
```

If a source is not available online, cite: `[Title of Document, Organization, Year]`

---

## Phase 2 — Slide Architecture (≥15 slides)

| # | Slide Type | Content Focus |
|---|-----------|--------------|
| 1 | **Title Slide** | Topic, subtitle, presenter, institution, date |
| 2 | **Agenda** | Numbered sections with brief descriptions |
| 3 | **Executive Summary** | 3–4 key takeaways from the entire presentation |
| 4 | **Context & Relevance** | Why this topic matters now; problem statement |
| 5 | **Historical Background** | Timeline of key developments |
| 6 | **Key Statistics** | 3–4 large-format data callouts with sources |
| 7 | **Core Concept I** | First major deep-dive topic |
| 8 | **Core Concept I — Detail** | Supporting evidence, examples, data |
| 9 | **Core Concept II** | Second major deep-dive topic |
| 10 | **Core Concept II — Infographic** | Chart, diagram, or process flow |
| 11 | **Current Trends** | 3–5 active trends with evidence |
| 12 | **Trend Data** | Chart or comparison supporting trends |
| 13 | **Case Study** | Real-world example: context → action → result |
| 14 | **Challenges & Risks** | Specific obstacles with citations |
| 15 | **Opportunities** | Forward-looking recommendations |
| 16 | **Future Outlook** | Predictions, scenarios, roadmap |
| 17 | **Key Takeaways** | Top 5 insights from the entire deck |
| 18 | **References** | Full bibliography (APA or similar) |
| 19 | **Q&A / Thank You** | Closing slide |

> For complex/technical topics: expand to 20–25 slides with additional deep-dives

---

## Phase 3 — Design System

### Color Palette: Academic High-Contrast

Use a **dark header / light body "sandwich" structure** for maximum legibility:

```python
# DARK elements (headers, title slides, section dividers)
DARK_BG      = "1C2B3A"   # Deep navy — main dark background
DARK_TEXT    = "F0F4F8"   # Near-white text on dark backgrounds
ACCENT       = "2E86AB"   # Professional blue accent

# LIGHT elements (content slides)
LIGHT_BG     = "FAFBFC"   # Off-white slide body
LIGHT_TEXT   = "1A1A2E"   # Near-black text on light backgrounds
LIGHT_MUTED  = "5A6A7A"   # Muted gray for captions, citations

# Highlight / callout
HIGHLIGHT    = "E8F4FD"   # Very pale blue for card backgrounds
RULE_COLOR   = "2E86AB"   # Accent lines, borders
```

**Topic-based palette alternatives:**

| Domain | DARK_BG | ACCENT | Use when |
|--------|---------|--------|----------|
| Medical/Health | `1B3A2F` | `27AE60` | Biology, medicine, environment |
| Technology/AI | `1A1A2E` | `6366F1` | CS, AI, engineering |
| Economics/Business | `1C2B3A` | `D4AF37` | Finance, economics, management |
| Social Sciences | `2C1654` | `9B59B6` | Psychology, sociology, law |
| Default Academic | `1C2B3A` | `2E86AB` | General / mixed topics |

### Typography: Serif Titles + Sans-serif Body

```python
from pptx.util import Pt
from pptx.dml.color import RGBColor

# Title fonts (serif — scholarly authority)
FONT_TITLE   = "Georgia"      # or "Palatino Linotype"
SIZE_TITLE   = Pt(36)
SIZE_H1      = Pt(28)
SIZE_H2      = Pt(22)

# Body fonts (sans-serif — clean legibility)
FONT_BODY    = "Calibri"      # or "Arial"
SIZE_BODY    = Pt(14)
SIZE_SMALL   = Pt(11)
SIZE_CITATION = Pt(9)
SIZE_STAT    = Pt(52)         # For large stat callouts
```

### Layout Dimensions (python-pptx uses EMU — use Inches/Cm helpers)

```python
from pptx.util import Inches, Cm, Pt

SLIDE_W = Inches(13.33)   # Widescreen 16:9
SLIDE_H = Inches(7.5)

MARGIN_L   = Inches(0.6)
MARGIN_R   = Inches(0.6)
MARGIN_TOP = Inches(0.5)
CONTENT_W  = Inches(12.1)  # SLIDE_W - MARGIN_L - MARGIN_R
```

---

## Phase 4 — Python Code Structure

### Required Setup

```python
pip install python-pptx
```

### Boilerplate: Every presentation starts with this

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu
import copy

# ── Presentation setup ────────────────────────────────────────
prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]  # Blank layout — always use this

# ── Design tokens ─────────────────────────────────────────────
C_DARK_BG    = RGBColor(0x1C, 0x2B, 0x3A)
C_DARK_TEXT  = RGBColor(0xF0, 0xF4, 0xF8)
C_ACCENT     = RGBColor(0x2E, 0x86, 0xAB)
C_LIGHT_BG   = RGBColor(0xFA, 0xFB, 0xFC)
C_LIGHT_TEXT = RGBColor(0x1A, 0x1A, 0x2E)
C_MUTED      = RGBColor(0x5A, 0x6A, 0x7A)
C_HIGHLIGHT  = RGBColor(0xE8, 0xF4, 0xFD)
C_WHITE      = RGBColor(0xFF, 0xFF, 0xFF)

FONT_TITLE = "Georgia"
FONT_BODY  = "Calibri"

# ── Core helper: set paragraph text with full formatting ──────
def add_text_box(slide, text, left, top, width, height,
                 font_name=FONT_BODY, font_size=Pt(14),
                 bold=False, italic=False, color=None,
                 align=PP_ALIGN.LEFT, word_wrap=True):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = word_wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = font_size
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color
    return txBox

# ── Helper: add a filled rectangle ───────────────────────────
def add_rect(slide, left, top, width, height, fill_color, line_color=None):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
    else:
        shape.line.fill.background()  # no border
    return shape

# ── Helper: set slide background color ───────────────────────
def set_bg(slide, color: RGBColor):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

# ── Helper: add speaker notes ────────────────────────────────
def add_notes(slide, notes_text: str):
    """Add speaker notes to a slide. notes_text must be 800–2000 words."""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text

# ── Helper: add citation footer ──────────────────────────────
def add_citation(slide, citation_text: str):
    """Add a small citation line at the bottom of the slide."""
    add_text_box(
        slide, f"Source: {citation_text}",
        left=Inches(0.6), top=Inches(7.05),
        width=Inches(12.1), height=Inches(0.35),
        font_name=FONT_BODY, font_size=Pt(8),
        italic=True, color=C_MUTED,
        align=PP_ALIGN.LEFT
    )

# ── Helper: add left accent bar (visual motif) ───────────────
def add_accent_bar(slide):
    add_rect(slide,
        left=Inches(0), top=Inches(0),
        width=Inches(0.1), height=Inches(7.5),
        fill_color=C_ACCENT
    )

# ── Helper: add slide number ─────────────────────────────────
def add_slide_number(slide, number: int, total: int):
    add_text_box(
        slide, f"{number} / {total}",
        left=Inches(12.0), top=Inches(7.1),
        width=Inches(1.2), height=Inches(0.3),
        font_name=FONT_BODY, font_size=Pt(8),
        color=C_MUTED, align=PP_ALIGN.RIGHT
    )
```

---

## Phase 5 — Slide Patterns (python-pptx)

### Pattern 1: Title Slide (dark background)

```python
def build_title_slide(prs, title, subtitle, presenter, institution, date):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, C_DARK_BG)

    # Accent line (horizontal, centered)
    add_rect(slide,
        left=Inches(0.6), top=Inches(3.9),
        width=Inches(12.1), height=Inches(0.04),
        fill_color=C_ACCENT
    )

    # Main title
    add_text_box(
        slide, title,
        left=Inches(0.8), top=Inches(1.2),
        width=Inches(11.7), height=Inches(1.8),
        font_name=FONT_TITLE, font_size=Pt(40),
        bold=True, color=C_DARK_TEXT,
        align=PP_ALIGN.LEFT
    )

    # Subtitle
    add_text_box(
        slide, subtitle,
        left=Inches(0.8), top=Inches(3.1),
        width=Inches(11.7), height=Inches(0.7),
        font_name=FONT_BODY, font_size=Pt(18),
        color=C_ACCENT, align=PP_ALIGN.LEFT
    )

    # Presenter + institution + date
    add_text_box(
        slide, f"{presenter}  |  {institution}  |  {date}",
        left=Inches(0.8), top=Inches(4.1),
        width=Inches(11.7), height=Inches(0.4),
        font_name=FONT_BODY, font_size=Pt(12),
        color=C_MUTED, align=PP_ALIGN.LEFT
    )

    add_notes(slide, """[TITLE SLIDE NOTES — 800+ words]
Introduce yourself and your credentials relevant to this topic. Explain why this presentation matters right now and what the audience will gain. State the central question the presentation answers. Outline the structure briefly. Set the tone: this is a rigorous but accessible exploration of [TOPIC].

Mention: How long will this take? Will there be Q&A? Where can they access the slides?

Transition: "Let's begin with an overview of what we'll cover today."

Sources for this slide: [none — title slide]""")

    return slide
```

### Pattern 2: Content Slide (light background, standard layout)

```python
def build_content_slide(prs, title, bullets, citation, notes_text,
                        slide_num, total_slides):
    """
    bullets: list of strings — each becomes one bullet point
    citation: str — source shown at bottom
    notes_text: str — 800–2000 words
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, C_LIGHT_BG)
    add_accent_bar(slide)

    # Title bar (dark background strip)
    add_rect(slide,
        left=Inches(0), top=Inches(0),
        width=Inches(13.33), height=Inches(1.1),
        fill_color=C_DARK_BG
    )
    add_text_box(
        slide, title,
        left=Inches(0.3), top=Inches(0.1),
        width=Inches(12.7), height=Inches(0.9),
        font_name=FONT_TITLE, font_size=Pt(26),
        bold=True, color=C_DARK_TEXT,
        align=PP_ALIGN.LEFT
    )

    # Bullet points
    txBox = slide.shapes.add_textbox(
        Inches(0.7), Inches(1.25),
        Inches(11.9), Inches(5.5)
    )
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, bullet in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"• {bullet}"
        p.space_after = Pt(8)
        run = p.runs[0]
        run.font.name = FONT_BODY
        run.font.size = Pt(14)
        run.font.color.rgb = C_LIGHT_TEXT

    add_citation(slide, citation)
    add_slide_number(slide, slide_num, total_slides)
    add_notes(slide, notes_text)
    return slide
```

### Pattern 3: Statistics Infographic Slide

```python
def build_stats_slide(prs, title, stats, citation, notes_text,
                      slide_num, total_slides):
    """
    stats: list of dicts:
      [{"number": "87%", "label": "Adoption Rate", "context": "by 2025 (McKinsey, 2023)"}]
    Max 4 stats recommended.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, C_DARK_BG)
    add_accent_bar(slide)

    # Title
    add_text_box(
        slide, title,
        left=Inches(0.3), top=Inches(0.15),
        width=Inches(12.7), height=Inches(0.8),
        font_name=FONT_TITLE, font_size=Pt(28),
        bold=True, color=C_DARK_TEXT,
        align=PP_ALIGN.LEFT
    )

    # Stat boxes
    n = len(stats)
    box_w = (12.1 - 0.3 * (n - 1)) / n
    start_x = 0.6

    for i, stat in enumerate(stats):
        x = start_x + i * (box_w + 0.3)

        # Card background
        add_rect(slide,
            left=Inches(x), top=Inches(1.2),
            width=Inches(box_w), height=Inches(5.8),
            fill_color=RGBColor(0x25, 0x3C, 0x50)
        )

        # Big number
        add_text_box(
            slide, stat["number"],
            left=Inches(x + 0.1), top=Inches(1.5),
            width=Inches(box_w - 0.2), height=Inches(2.0),
            font_name=FONT_TITLE, font_size=Pt(56),
            bold=True, color=C_ACCENT,
            align=PP_ALIGN.CENTER
        )

        # Label
        add_text_box(
            slide, stat["label"],
            left=Inches(x + 0.1), top=Inches(3.6),
            width=Inches(box_w - 0.2), height=Inches(0.7),
            font_name=FONT_BODY, font_size=Pt(15),
            bold=True, color=C_DARK_TEXT,
            align=PP_ALIGN.CENTER
        )

        # Context / source
        add_text_box(
            slide, stat["context"],
            left=Inches(x + 0.1), top=Inches(4.4),
            width=Inches(box_w - 0.2), height=Inches(0.6),
            font_name=FONT_BODY, font_size=Pt(10),
            italic=True, color=C_MUTED,
            align=PP_ALIGN.CENTER
        )

    add_citation(slide, citation)
    add_slide_number(slide, slide_num, total_slides)
    add_notes(slide, notes_text)
    return slide
```

### Pattern 4: Two-Column Slide

```python
def build_two_col_slide(prs, title, left_header, left_points,
                        right_header, right_points,
                        citation, notes_text, slide_num, total_slides):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, C_LIGHT_BG)
    add_accent_bar(slide)

    # Title bar
    add_rect(slide,
        left=Inches(0), top=Inches(0),
        width=Inches(13.33), height=Inches(1.1),
        fill_color=C_DARK_BG
    )
    add_text_box(
        slide, title,
        left=Inches(0.3), top=Inches(0.1),
        width=Inches(12.7), height=Inches(0.9),
        font_name=FONT_TITLE, font_size=Pt(26),
        bold=True, color=C_DARK_TEXT
    )

    # Divider line between columns
    add_rect(slide,
        left=Inches(6.9), top=Inches(1.2),
        width=Inches(0.04), height=Inches(5.8),
        fill_color=C_ACCENT
    )

    col_w = Inches(5.9)

    for col_x, header, points in [
        (Inches(0.5), left_header, left_points),
        (Inches(7.1), right_header, right_points),
    ]:
        # Column header
        add_text_box(
            slide, header,
            left=col_x, top=Inches(1.25),
            width=col_w, height=Inches(0.5),
            font_name=FONT_BODY, font_size=Pt(16),
            bold=True, color=C_ACCENT
        )
        # Bullets
        txBox = slide.shapes.add_textbox(col_x, Inches(1.85), col_w, Inches(5.0))
        tf = txBox.text_frame
        tf.word_wrap = True
        for i, pt in enumerate(points):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = f"• {pt}"
            p.space_after = Pt(7)
            run = p.runs[0]
            run.font.name = FONT_BODY
            run.font.size = Pt(13)
            run.font.color.rgb = C_LIGHT_TEXT

    add_citation(slide, citation)
    add_slide_number(slide, slide_num, total_slides)
    add_notes(slide, notes_text)
    return slide
```

### Pattern 5: Timeline Slide

```python
def build_timeline_slide(prs, title, events, citation, notes_text,
                         slide_num, total_slides):
    """
    events: [{"year": "2017", "title": "...", "desc": "..."}]
    Max 6 events recommended.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, C_LIGHT_BG)
    add_accent_bar(slide)

    # Title bar
    add_rect(slide,
        left=Inches(0), top=Inches(0),
        width=Inches(13.33), height=Inches(1.1),
        fill_color=C_DARK_BG
    )
    add_text_box(
        slide, title,
        left=Inches(0.3), top=Inches(0.1),
        width=Inches(12.7), height=Inches(0.9),
        font_name=FONT_TITLE, font_size=Pt(26),
        bold=True, color=C_DARK_TEXT
    )

    # Horizontal timeline line
    line_y = Inches(4.0)
    add_rect(slide,
        left=Inches(0.8), top=line_y,
        width=Inches(11.7), height=Inches(0.06),
        fill_color=C_ACCENT
    )

    n = len(events)
    step = 11.7 / (n - 1) if n > 1 else 11.7

    for i, ev in enumerate(events):
        x = 0.8 + i * step
        is_top = (i % 2 == 0)

        # Dot
        dot = slide.shapes.add_shape(
            9,  # OVAL
            Inches(x - 0.12), line_y - Inches(0.12),
            Inches(0.24), Inches(0.24)
        )
        dot.fill.solid()
        dot.fill.fore_color.rgb = C_ACCENT
        dot.line.fill.background()

        # Year label
        add_text_box(
            slide, ev["year"],
            left=Inches(x - 0.5), top=line_y + (Inches(0.2) if is_top else -Inches(0.55)),
            width=Inches(1.0), height=Inches(0.35),
            font_name=FONT_BODY, font_size=Pt(11),
            bold=True, color=C_ACCENT,
            align=PP_ALIGN.CENTER
        )

        # Event title
        add_text_box(
            slide, ev["title"],
            left=Inches(x - 0.75),
            top=line_y + (Inches(0.55) if is_top else -Inches(1.8)),
            width=Inches(1.5), height=Inches(1.2),
            font_name=FONT_BODY, font_size=Pt(11),
            color=C_LIGHT_TEXT,
            align=PP_ALIGN.CENTER
        )

    add_citation(slide, citation)
    add_slide_number(slide, slide_num, total_slides)
    add_notes(slide, notes_text)
    return slide
```

### Pattern 6: Case Study Slide

```python
def build_case_study_slide(prs, title, org, context, action, result,
                           lesson, citation, notes_text,
                           slide_num, total_slides):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, C_LIGHT_BG)
    add_accent_bar(slide)

    # Title bar
    add_rect(slide,
        left=Inches(0), top=Inches(0),
        width=Inches(13.33), height=Inches(1.1),
        fill_color=C_DARK_BG
    )
    add_text_box(
        slide, title,
        left=Inches(0.3), top=Inches(0.1),
        width=Inches(12.7), height=Inches(0.9),
        font_name=FONT_TITLE, font_size=Pt(26),
        bold=True, color=C_DARK_TEXT
    )

    # Org badge
    add_rect(slide,
        left=Inches(0.5), top=Inches(1.2),
        width=Inches(3.5), height=Inches(0.55),
        fill_color=C_ACCENT
    )
    add_text_box(
        slide, org,
        left=Inches(0.5), top=Inches(1.2),
        width=Inches(3.5), height=Inches(0.55),
        font_name=FONT_BODY, font_size=Pt(14),
        bold=True, color=C_WHITE,
        align=PP_ALIGN.CENTER
    )

    sections = [
        ("Context",  context,  Inches(1.85)),
        ("Action",   action,   Inches(3.05)),
        ("Result",   result,   Inches(4.25)),
        ("Lesson",   lesson,   Inches(5.45)),
    ]

    for label, text, y in sections:
        add_rect(slide,
            left=Inches(0.5), top=y,
            width=Inches(1.1), height=Inches(0.9),
            fill_color=C_HIGHLIGHT
        )
        add_text_box(
            slide, label,
            left=Inches(0.5), top=y + Inches(0.25),
            width=Inches(1.1), height=Inches(0.4),
            font_name=FONT_BODY, font_size=Pt(11),
            bold=True, color=C_ACCENT,
            align=PP_ALIGN.CENTER
        )
        add_text_box(
            slide, text,
            left=Inches(1.75), top=y + Inches(0.1),
            width=Inches(11.0), height=Inches(0.75),
            font_name=FONT_BODY, font_size=Pt(13),
            color=C_LIGHT_TEXT
        )

    add_citation(slide, citation)
    add_slide_number(slide, slide_num, total_slides)
    add_notes(slide, notes_text)
    return slide
```

### Pattern 7: References Slide

```python
def build_references_slide(prs, references, slide_num, total_slides):
    """
    references: list of full citation strings (APA format recommended)
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, C_LIGHT_BG)
    add_accent_bar(slide)

    # Title bar
    add_rect(slide,
        left=Inches(0), top=Inches(0),
        width=Inches(13.33), height=Inches(1.1),
        fill_color=C_DARK_BG
    )
    add_text_box(
        slide, "References",
        left=Inches(0.3), top=Inches(0.1),
        width=Inches(12.7), height=Inches(0.9),
        font_name=FONT_TITLE, font_size=Pt(26),
        bold=True, color=C_DARK_TEXT
    )

    txBox = slide.shapes.add_textbox(
        Inches(0.7), Inches(1.25),
        Inches(11.9), Inches(5.9)
    )
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, ref in enumerate(references):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = ref
        p.space_after = Pt(5)
        run = p.runs[0]
        run.font.name = FONT_BODY
        run.font.size = Pt(11)
        run.font.color.rgb = C_LIGHT_TEXT

    add_slide_number(slide, slide_num, total_slides)
    add_notes(slide, "This slide lists all sources cited throughout the presentation. Encourage the audience to consult these references for deeper study. Mention that the slide deck with clickable links will be shared after the session.")
    return slide
```

---

## Phase 6 — Speaker Notes Requirements

### MANDATORY Standards

| Standard | Requirement |
|----------|-------------|
| Length | **800–2000 words** per slide |
| Tone | Popular-science + empathetic (accessible to beginners) |
| Content | Explain every bullet point on the slide in detail |
| Citations | Include full source citations in notes |
| Structure | Opening → Key points → Evidence → Transition |
| Transition | Every note ends with a bridge to the next slide |

### Notes Template (copy for each slide)

```
SLIDE [N]: [TITLE]
─────────────────────────────────────────────────────

OPENING:
[2–3 sentences that introduce this slide's theme and connect to the previous one]

EXPLANATION OF EACH POINT:

▸ [Bullet point 1 — exact text from slide]:
[3–5 sentences explaining what this means, why it matters, and how it connects
to the broader topic. Use an analogy or real-world example for clarity.
Mention any nuance or debate in the field.]

▸ [Bullet point 2 — exact text from slide]:
[Same format: explanation + example + nuance]

▸ [Bullet point 3]:
[Same format]

KEY INSIGHT:
[1–2 sentences synthesizing what these points collectively tell us]

COMMON MISCONCEPTION (if applicable):
[Address something students often get wrong about this topic]

REAL-WORLD CONNECTION:
[A concrete example, news story, or application that makes this tangible]

SOURCES CITED ON THIS SLIDE:
- [Full APA citation for source 1]
- [Full APA citation for source 2]
- [URL if applicable]

TRANSITION:
"Having established [summary of this slide], we can now turn to [next slide topic]..."
```

---

## Phase 7 — Citations

### Rules (MANDATORY)

1. **Every content slide** must have at least one citation
2. **Citation on slide**: small footer text (9pt, italic, muted color) — author + year or URL
3. **Citation in notes**: full APA citation
4. **References slide**: collects all citations from the entire presentation

### Citation Formats

```python
# On-slide citation (brief):
"McKinsey Global Institute, 2023"
"OECD (2022). https://doi.org/..."
"Nature, Vol. 612, 2022"

# In notes (full APA):
"McKinsey Global Institute. (2023). The state of AI in 2023. McKinsey & Company. https://www.mckinsey.com/..."
"OECD. (2022). Artificial Intelligence in Society. OECD Publishing. https://doi.org/10.1787/eedfee77-en"
```

---

## Phase 8 — QA Checklist

Before saving the file, verify:

```
CONTENT
□ ≥15 slides generated
□ Every slide has real, specific content (no "Lorem ipsum" or vague text)
□ Every slide has at least one citation
□ References slide includes all cited sources
□ Topic stays focused — no off-topic tangents

DESIGN
□ Title/section slides use dark background (C_DARK_BG)
□ Content slides use light background (C_LIGHT_BG)
□ All titles use FONT_TITLE (Georgia/Palatino)
□ All body text uses FONT_BODY (Calibri/Arial)
□ Accent bar on every content slide
□ Slide numbers on all slides except title
□ No text overflow — all text boxes have sufficient height

SPEAKER NOTES
□ Every slide has notes
□ Every notes section is 800–2000 words
□ Every bullet on every slide is explained in notes
□ Full citations in notes
□ Transition phrase at end of every notes section

PYTHON CODE
□ Code runs without errors: python presentation.py
□ Output file is valid .pptx
□ All slides render correctly
```

---

## Phase 9 — Final Code Template

```python
# presentation.py
# Topic: [TOPIC]
# Language: [LANGUAGE]
# Generated with: python-pptx

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# [paste all helpers from Phase 4]
# [paste all pattern functions from Phase 5]

TOTAL_SLIDES = 19  # update to actual count

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

# ── Slide 1: Title ────────────────────────────────────────────
build_title_slide(prs,
    title="[FULL TOPIC TITLE]",
    subtitle="[DESCRIPTIVE SUBTITLE]",
    presenter="[NAME]",
    institution="[INSTITUTION / COURSE]",
    date="[DATE]"
)

# ── Slide 2: Agenda ───────────────────────────────────────────
build_content_slide(prs,
    title="Agenda",
    bullets=[
        "1. Context & Background",
        "2. Core Concepts",
        "3. Current Trends & Data",
        "4. Case Study",
        "5. Challenges & Opportunities",
        "6. Future Outlook",
        "7. Key Takeaways & References"
    ],
    citation="[no external source]",
    notes_text="""[Full notes 800+ words]""",
    slide_num=2, total_slides=TOTAL_SLIDES
)

# ... continue for all 15–19 slides ...

# ── Save ──────────────────────────────────────────────────────
prs.save("presentation.pptx")
print("✅ Presentation saved: presentation.pptx")
```

---

## Quick Reference: Running the Result

```bash
# Install dependency
pip install python-pptx

# Generate presentation
python presentation.py

# Verify output
python -c "
from pptx import Presentation
prs = Presentation('presentation.pptx')
print(f'Slides: {len(prs.slides)}')
for i, slide in enumerate(prs.slides, 1):
    notes = slide.notes_slide.notes_text_frame.text
    print(f'  Slide {i}: {len(notes)} chars in notes')
"
```
