---
name: powerpoint-ppt
description: PowerPoint (.pptx) manipulation via MCP server. Use for creating slides, formatting presentations, managing placeholders, adding images, applying templates, or extracting text from .pptx files.
license: Complete terms in LICENSE.txt
---

# PowerPoint Presentation Workflows

Use this skill when a `.pptx` deck is the output and slide composition matters.

## Current MCP Reality

Presentation MCP tooling is host-dependent. Some clients expose Office presentation tools directly, while others do not. Do not assume stable public tool names. If the current client lacks those tools, use the included local automation script or generate the content structure first and import it into PowerPoint.

## Activation Conditions

- Creating a deck from structured content
- Applying templates, branding, and slide layouts
- Updating text, images, or charts inside an existing presentation
- Extracting slide text for review or translation

## Practical Workflow

1. Confirm whether the client exposes presentation tools.
2. Prefer template-driven decks over manual one-off slide formatting.
3. Keep one idea per slide and treat text density as a defect.
4. Validate the final deck visually before calling it done.

## Deck Checklist

- [ ] Title slide is present
- [ ] Slide layouts are consistent
- [ ] Fonts and colors match the template
- [ ] Images are high-resolution and not stretched
- [ ] Final slides were reviewed in slideshow size, not just as raw XML or text

## References & Resources

### Documentation
- [PowerPoint References](./references/) - Supporting notes for formatting, structure, and automation expectations

### Scripts
- [PPT Automation Script](./scripts/ppt-automation.py) - Local fallback for building or updating presentation content

### Examples
- [Presentation Examples](./examples/presentation-examples.md) - Example deck structures and content patterns

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [microsoft-development](../microsoft-development/SKILL.md) | Microsoft ecosystem context and official docs |
| [excel-sheet](../excel-sheet/SKILL.md) | Pull charts or tables from spreadsheets into slides |
| [word-document](../word-document/SKILL.md) | Turn long-form reports into summary decks |
