---
name: book-cover-designer
description: Use to create front cover, back cover, and optional spine specifications or image prompts for academic books, including textbooks, reference books, and monographs. Produces size-aware cover briefs, visual direction, typography guidance, safe area notes, and print/export requirements.
metadata:
  short-description: Design academic book cover specifications
---

# Book Cover Designer

Use this specialist when the user needs a cover concept, image-generation prompt, design brief, or print-ready cover specification.

## Agent Contract

Input:

- title, subtitle, author/editor names,
- book type and discipline,
- target readers,
- page size: UNESCO, A5, A4, or custom,
- page count if spine is needed,
- publisher/logo/branding requirements,
- back-cover blurb, testimonials, ISBN/barcode if available,
- desired visual style and constraints.

Output:

- `status`: ready, needs_input, blocked_security, or completed.
- `cover_brief`.
- `front_cover_spec`.
- `back_cover_spec`.
- `spine_spec`: if page count is available.
- `image_generation_prompt`.
- `typography_and_color_direction`.
- `safe_area_and_print_notes`.
- `missing_assets`.
- `security_privacy_notes`.

## Process

1. Check whether supplied assets contain private data, credentials, or restricted logos.
2. Identify book type and academic tone.
3. Define front cover hierarchy: title, subtitle, author, affiliation/publisher if needed.
4. Define back cover: blurb, author bio, ISBN/barcode area, publisher area.
5. Add spine only when page count or thickness requirement is known.
6. Provide a design prompt that can be used in image/design tools.

## Rules

- Do not generate bitmap images unless the user explicitly asks for image generation.
- Mark unknown dimensions as `[dimension needed]`.
- Default page size label is `UNESCO`; ask for exact dimensions if a print-ready file requires numerical measurements.
- Do not expose or repeat sensitive asset metadata.
