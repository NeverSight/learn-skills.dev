---
name: ppt-artisan
description: Create and convert PowerPoint presentations from Markdown using Marp. Use when the user wants to generate slides, manage themes, or convert MD to PPTX/PDF.
status: implemented
category: Data & Content
last_updated: '2026-02-13'
tags:
  - automation
  - gemini-skill
---

# PowerPoint Artisan (ppt-artisan)

This skill creates high-impact, boardroom-ready presentations. It goes beyond simple Markdown conversion by integrating with custom brand themes and high-resolution visual assets.

## Capabilities

### 1. Visual-First Presentation Generation

- **Theme Awareness**: Automatically checks `knowledge/templates/themes/` for client-specific CSS before falling back to default themes.
- **High-Impact Layouts**: Leverages the `theme_design_guide.md` to structure information using cards, multi-column grids, and "Lead" slides.
- **Asset Integration**: Mandates the use of absolute paths for images and prefers SVG diagrams (from `diagram-renderer`) for scalability.

### 2. Multi-Format Conversion

- **PPTX**: Default format for editable presentations.
- **PDF/HTML**: Formats for quick preview and digital distribution.

## Fidelity Modes (Audience-Driven Density)

Adjust the information density based on the target audience:

1.  **Executive Mode (High Summary)**:
    - **Goal**: Rapid decision-making and high-level vision.
    - **Design**: "1-Slide-1-Message." Focus on ROI, major milestones, and business risks. Max 10-15 slides.
2.  **Standard Mode (Balanced)**:
    - **Goal**: Operational alignment and project management.
    - **Design**: Structured overview with key technical metrics. Good for kick-offs and monthly reviews.
3.  **Deep Dive Mode (Technical Exhaustiveness)**:
    - **Goal**: Implementation, auditing, and knowledge transfer.
    - **Design**: "Anti-Summarization." Mandatory tables, code evidence, and granular sub-topic separation. No slide limit (e.g., 40+ slides).

## High-Fidelity Authoring Workflow

1.  **Audience Identification**: Confirm the density mode before drafting.
2.  **Storyboard Strategy**: Define slide count targets per chapter based on the selected mode.
3.  **Synthesis**: Combine sections with professional templates.

## Best Practices

- **Topic-Per-Slide (Deep Dive)**: Instead of brief bullets, provide detailed technical specs. A professional system design should naturally exceed 40 slides.
- **Visual Evidence**: Use two-column layouts to place conceptual diagrams next to technical tables.
- **High Fidelity**: Always use `--allow-local-files` to ensure assets render.

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
