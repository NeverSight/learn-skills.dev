---
name: ppt-image-first-workflow
description: Conversation-first, image-first PPT generation workflow skill using GPT Image 2 for full-page visual slides packaged into PPTX files.
triggers:
  - help me make a PPT
  - create a presentation for me
  - build a slide deck
  - turn this report into slides
  - make a defense presentation
  - I need a product pitch deck
  - generate a PPT from my notes
  - design a slide deck with visual previews
---

# ppt-image-first-workflow

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A **conversation-first, image-first** PPT workflow skill that takes a vague presentation request through structured stages: content baseline → style preview → plan lock → generation → review. Pages are rendered as full-image visuals via **GPT Image 2** and packaged into PPTX containers — not drawn as native editable PowerPoint objects.

---

## What This Project Does

`ppt-image-first` is a multi-stage workflow orchestrator, not a template stamper. It:

1. Collects minimal intake info (purpose, audience, page count, materials, identity anchors)
2. Builds a `content_report.md` if user materials are thin
3. Aligns style boundaries with 3 short questions
4. Generates real image previews (cover, TOC, body pages) across multiple style directions
5. Iterates on style until user confirms
6. Runs a "style reverse inference" check to lock stable visual traits
7. Produces planning artifacts: `design_spec.md`, `slide_blueprint.md`, `spec_lock.md`
8. Generates final per-page images via GPT Image 2
9. Packages images into a `.pptx` file
10. Runs a structured review-and-retouch loop

**Output type:** Image-first PPTX — each slide is a full-page rendered image. Text/shapes inside slides are NOT individually editable PowerPoint objects.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/NyxTides/ppt-image-first.git
cd ppt-image-first

# Install Python dependencies
pip install -r requirements.txt

# Copy the skill file into your agent's skill directory
# For Claude Code:
cp SKILL.md ~/.claude/skills/ppt-image-first.md

# For Codex CLI:
cp SKILL.md ~/.codex/skills/ppt-image-first.md

# For Opencode:
cp SKILL.md ~/.opencode/skills/ppt-image-first.md
```

### Environment Variables

```bash
# Required: OpenAI API key for GPT Image 2 generation
export OPENAI_API_KEY=your_key_here

# Optional: output directory for generated files (default: ./output)
export PPT_OUTPUT_DIR=./my_decks

# Optional: default aspect ratio (default: 16:9)
export PPT_ASPECT_RATIO=16:9
```

---

## Project Structure

```text
ppt-image-first/
├─ SKILL.md                          # Agent skill definition
├─ references/
│  ├─ workflow.md                    # Full stage-by-stage workflow spec
│  ├─ conversation_framework.md      # Intake + confirmation dialogue rules
│  └─ preview-flow.md                # Image preview generation logic
├─ templates/
│  ├─ content_report_reference.md    # Template: content baseline doc
│  ├─ design_spec_reference.md       # Template: visual design spec
│  ├─ slide_blueprint_reference.md   # Template: per-page blueprint
│  └─ spec_lock_reference.md         # Template: execution constraints
└─ assets/
   ├─ preview_shell/index.html       # Style comparison UI shell
   ├─ candidate_picker_shell/index.html  # Multi-candidate selection UI
   └─ review_shell/index.html        # Review & retouch UI shell
```

---

## Workflow Stages

### Stage 1 — Intake & Baseline Judgment

Collect only essential info. Do NOT present a long form.

```python
INTAKE_FIELDS = [
    "purpose",          # defense / product pitch / research report / training
    "audience",         # professor panel / investors / internal team
    "page_count_hint",  # rough number or duration ("20 slides" / "10 min talk")
    "materials",        # what the user already has
    "identity_anchor",  # school / company / lab / brand name
]
```

After intake, output a **baseline judgment** (2–4 sentences) and pause at **需求确认 (requirements confirmation)**.

### Stage 1.25 — Content Baseline (`content_report.md`)

If user materials are thin (topic only, or scattered notes), generate a structured content report **before** any style work.

```python
# content_report.md structure
CONTENT_REPORT_SECTIONS = [
    "core_thesis",          # The one central claim or narrative spine
    "key_sections",         # 4–7 logical sections with bullet points
    "data_and_evidence",    # Stats, facts, examples to reference
    "narrative_arc",        # How sections connect: problem → solution → proof
    "slide_count_estimate", # Recommended page breakdown per section
]
```

### Stage 1.5 — Style Boundary Alignment

Ask exactly **3 short questions**:

```
1. Overall tone: light / dark / neutral middle?
2. Direction: conventional professional / visually distinctive?
3. How many style directions to preview first? (recommend 2–3)
```

### Stage 2 — Style Proposals & Previews

Generate N style directions. For **each direction**, produce real image previews:

```python
PREVIEW_PAGES_PER_DIRECTION = [
    "cover_page",     # Title + identity anchor
    "toc_page",       # Table of contents / agenda
    "body_page",      # Representative content page
]
```

Use the `assets/preview_shell/index.html` to display comparisons.

### Stage 2.5 — Style Refinement (optional)

If user wants to iterate on one direction rather than lock in, continue from that direction only. Do NOT force a final decision.

### Stage 2.75 — Style Reverse Inference

After user selects a direction, analyze the confirmed preview images and extract:

```python
STYLE_INFERENCE_CATEGORIES = {
    "must_continue":    [],  # Traits clearly present, clearly liked
    "confirm_extend":   [],  # Traits that worked here, check if wanted deck-wide
    "do_not_lock":      [],  # Accidental/contextual traits, not repeatable rules
}
```

### Stage 3 — Planning Artifacts

Generate in order:

```python
PLANNING_ARTIFACTS = [
    "design_spec.md",      # Global visual rationale + continuity constraints
    "slide_blueprint.md",  # Per-page: intent, content payload, visual strategy
    "spec_lock.md",        # What CAN and CANNOT change during generation
]
```

Pause at **生成前确认 (pre-generation confirmation)** before proceeding.

### Stage 4 — Generation

Ask the user:

```
Generate mode:
A) One final image per slide (faster)
B) Multiple candidates per slide, then pick (slower, more control)
```

If **B**, use `assets/candidate_picker_shell/index.html` before finalizing.

### Stage 5 — Review & Retouch

Use `assets/review_shell/index.html`. Structured feedback format:

```python
REVIEW_FEEDBACK_SCHEMA = {
    "slide_index": int,
    "issue_type": "visual | content | layout | consistency",
    "description": str,
    "suggested_fix": str,  # optional
}
```

---

## Core Python Usage

### Generating a Slide Image via GPT Image 2

```python
import openai
import base64
from pathlib import Path

client = openai.OpenAI()  # reads OPENAI_API_KEY from env

def generate_slide_image(
    prompt: str,
    slide_index: int,
    output_dir: str = "./output/slides",
    size: str = "1792x1024",  # 16:9 approximation
) -> Path:
    """Generate a single slide image using GPT Image 2."""
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        n=1,
        size=size,
    )
    
    image_b64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)
    
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    slide_path = out_path / f"slide_{slide_index:02d}.png"
    slide_path.write_bytes(image_bytes)
    
    print(f"[slide {slide_index}] saved → {slide_path}")
    return slide_path
```

### Building PPTX from Slide Images

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pathlib import Path

def build_pptx_from_images(
    image_paths: list[Path],
    output_path: str = "./output/deck.pptx",
    width_inches: float = 13.33,   # 16:9 widescreen
    height_inches: float = 7.5,
) -> Path:
    """Package a list of full-page slide images into a PPTX file."""
    prs = Presentation()
    prs.slide_width = Inches(width_inches)
    prs.slide_height = Inches(height_inches)
    
    blank_layout = prs.slide_layouts[6]  # blank layout — no placeholders
    
    for idx, img_path in enumerate(image_paths):
        slide = prs.slides.add_slide(blank_layout)
        slide.shapes.add_picture(
            str(img_path),
            left=Inches(0),
            top=Inches(0),
            width=Inches(width_inches),
            height=Inches(height_inches),
        )
        print(f"[pptx] added slide {idx + 1}: {img_path.name}")
    
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out))
    print(f"[pptx] saved → {out}")
    return out
```

### Full Pipeline: Images → PPTX

```python
import os
from pathlib import Path

def run_generation_pipeline(
    slide_prompts: list[str],
    deck_title: str = "deck",
    output_dir: str = "./output",
) -> Path:
    """
    Given a list of per-slide prompts, generate images and package into PPTX.
    slide_prompts should come from slide_blueprint.md — one prompt per page.
    """
    slides_dir = Path(output_dir) / "slides"
    image_paths = []
    
    for i, prompt in enumerate(slide_prompts):
        path = generate_slide_image(
            prompt=prompt,
            slide_index=i + 1,
            output_dir=str(slides_dir),
        )
        image_paths.append(path)
    
    pptx_path = build_pptx_from_images(
        image_paths=image_paths,
        output_path=f"{output_dir}/{deck_title}.pptx",
    )
    return pptx_path


# Example usage
if __name__ == "__main__":
    prompts = [
        # From slide_blueprint.md — generated by the workflow
        "Cover slide for a meteorology thesis defense. Title: 'Urban Heat Island Effects in Coastal Cities'. "
        "University name: Coastal Institute of Atmospheric Science. Dark navy background, white typography, "
        "subtle cloud texture, professional academic style. 16:9 widescreen.",
        
        "Table of contents slide. Sections: 1. Background 2. Data & Methods 3. Results 4. Discussion 5. Conclusion. "
        "Same dark navy color scheme, numbered list with clear hierarchy, minimal decorative elements.",
        
        "Body slide: 'Key Findings'. Three main data points as large stat callouts: +2.3°C average temp increase, "
        "67% of monitored stations affected, 15-year trend data. Dark navy background, accent color teal, "
        "clean data-forward layout.",
    ]
    
    output = run_generation_pipeline(
        slide_prompts=prompts,
        deck_title="meteorology-defense",
        output_dir="./output",
    )
    print(f"Done: {output}")
```

### Generating Multiple Candidates per Slide

```python
def generate_slide_candidates(
    prompt: str,
    slide_index: int,
    n_candidates: int = 3,
    output_dir: str = "./output/candidates",
) -> list[Path]:
    """Generate N candidate images for one slide for user selection."""
    paths = []
    for c in range(n_candidates):
        path = generate_slide_image(
            prompt=prompt,
            slide_index=slide_index,
            output_dir=f"{output_dir}/slide_{slide_index:02d}",
        )
        # rename to include candidate index
        new_path = path.parent / f"candidate_{c + 1}.png"
        path.rename(new_path)
        paths.append(new_path)
        print(f"[candidate {c + 1}/{n_candidates}] slide {slide_index}")
    return paths
```

---

## Planning Artifact Templates

### `design_spec.md` (minimal structure)

```markdown
# Design Spec

## Global Direction
[1–2 sentences on visual identity and rationale]

## Color Palette
- Primary: #______
- Secondary: #______
- Accent: #______
- Background: #______

## Typography
- Heading: [font / weight / size range]
- Body: [font / weight / size range]

## Layout Principles
- [Grid / alignment rules]
- [Spacing conventions]
- [What should appear on every slide vs. never]

## Continuity Constraints
- [What MUST remain consistent across all slides]
- [What is allowed to vary]
```

### `slide_blueprint.md` (per-page entry)

```markdown
## Slide 03 — Key Findings

**Intent:** Deliver the three most important statistical results as scannable callouts.
**Content payload:**
  - Stat 1: +2.3°C average increase
  - Stat 2: 67% of stations affected
  - Stat 3: 15-year trend confirmed
**Visual strategy:** Large number callouts, minimal prose, accent color on numbers.
**Carry-through elements:** Logo bottom-left, slide number bottom-right, dark navy bg.
**Generation prompt:**
  > Body slide titled 'Key Findings'. Three large stat callouts: '+2.3°C', '67%', '15 Years'.
  > Dark navy background, teal accent on numbers, white body text, clean grid layout, 16:9.
```

### `spec_lock.md` (minimal structure)

```markdown
# Spec Lock

## Locked (do not change)
- Background color: dark navy #0A1628
- Logo placement: bottom-left corner
- Slide number placement: bottom-right
- Heading font: [confirmed font]

## Flexible (may vary per page)
- Accent color intensity
- Layout grid (2-col vs. 3-col for body pages)
- Illustration vs. data visualization choice

## Do Not Fabricate
- Speaker's name, institutional affiliation
- Statistics not present in content_report.md
- Dates, locations, citation details

## Generation Strategy
- Mode: single final per slide (or: multi-candidate then pick)
- Retouch allowed: yes, via review_shell feedback loop
```

---

## Common Patterns

### Pattern: Thin Materials → Content First

```python
# When user provides only a topic, not full content:
# 1. Generate content_report.md BEFORE any style work
# 2. Use content_report.md as the source for all slide prompts
# 3. Never generate style previews from an empty premise

def should_generate_content_report(user_materials: str) -> bool:
    """Heuristic: if materials are under ~200 words, build content baseline first."""
    return len(user_materials.split()) < 200
```

### Pattern: Style Preview Shell Integration

```python
import subprocess
import json
from pathlib import Path

def launch_preview_shell(preview_images: dict[str, list[Path]]) -> None:
    """
    Write preview manifest and open the preview shell in browser.
    preview_images: {"direction_A": [cover, toc, body], "direction_B": [...]}
    """
    manifest = {
        direction: [str(p) for p in pages]
        for direction, pages in preview_images.items()
    }
    
    shell_dir = Path("assets/preview_shell")
    manifest_path = shell_dir / "preview_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    
    # Open in default browser
    subprocess.run(["open", str(shell_dir / "index.html")])  # macOS
    # subprocess.run(["xdg-open", str(shell_dir / "index.html")])  # Linux
```

### Pattern: Review Feedback → Retouch Prompt

```python
def feedback_to_retouch_prompt(
    original_prompt: str,
    feedback: dict,
) -> str:
    """Convert structured review feedback into an updated generation prompt."""
    issue = feedback["description"]
    fix = feedback.get("suggested_fix", "")
    
    retouch_instruction = f"REVISION: {issue}"
    if fix:
        retouch_instruction += f" Fix: {fix}"
    
    return f"{original_prompt}\n\n{retouch_instruction}"
```

---

## Troubleshooting

### Image generation returns an error

```python
# Check: OPENAI_API_KEY is set
import os
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not set"

# Check: size parameter is valid for gpt-image-1
# Valid sizes: "1024x1024", "1536x1024", "1024x1536", "auto"
# For 16:9 slides, use "1536x1024" (landscape)
```

### PPTX images appear blurry

```python
# Use the highest resolution size available
# Then let python-pptx scale to fill the slide — do NOT upscale manually
size = "1536x1024"  # use this instead of "1024x1024" for landscape slides
```

### Style consistency breaks across slides

```
Root cause: prompt drift — each slide prompt diverges from the locked spec.
Fix:
  1. Prepend spec_lock.md's "Locked" section to EVERY slide prompt
  2. Use a prompt prefix template:

STYLE_PREFIX = """
[STYLE LOCK] Dark navy #0A1628 background. Heading font: Inter Bold.
Logo bottom-left. Slide number bottom-right. Teal accent #2DD4BF on highlights.
DO NOT add gradients, textures, or decorative borders not in this spec.
"""

full_prompt = STYLE_PREFIX + slide_specific_prompt
```

### `content_report.md` content ends up in slides verbatim

```
This is a workflow sequencing error.
content_report.md is a SOURCE document, not a script.
The slide_blueprint.md should ADAPT content into slide-appropriate payloads.
Each slide blueprint entry must go through:
  content_report → narrative selection → slide payload → generation prompt
Never pipe content_report text directly into image generation prompts.
```

### Review shell not loading images

```bash
# Images must be accessible from the shell's local path
# Serve the output directory locally if needed:
cd output && python -m http.server 8080
# Then open assets/review_shell/index.html with base path set to localhost:8080
```

---

## Key Constraints to Respect

| Constraint | Rule |
|---|---|
| **Confirmation gates** | There are 3 mandatory pause points: requirements confirm, pre-generation confirm, review. Do not skip them. |
| **Preview = real images** | Never substitute text mockups, ASCII art, or placeholder boxes for image previews. |
| **Content before style** | If materials are thin, `content_report.md` must be generated before any style work begins. |
| **spec_lock.md is binding** | Fields in the "Locked" section must be enforced in every generation prompt. |
| **No fabrication** | Never invent names, statistics, affiliations, dates, or citations not present in user materials or `content_report.md`. |
| **Review is mandatory** | After first full generation, always enter the review loop — do not present output as final by default. |
| **Aspect ratio** | Default is 16:9. Do not change unless user explicitly requests it. |

---

## References

- `references/workflow.md` — Complete stage-by-stage workflow specification
- `references/conversation_framework.md` — Intake rules and confirmation dialogue patterns
- `references/preview-flow.md` — Image preview generation and shell integration details
- `templates/` — Reference templates for all four planning artifacts
