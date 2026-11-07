---
name: arabic-rtl-fixer-ai-skill
description: Create, edit, repair, and validate Arabic or Arabic-English content with logical-order Unicode, native RTL semantics, mixed-language handling, Arabic-capable typography, and format-specific QA. Use for Word, PowerPoint, PDF, web, spreadsheet, image, and reusable Arabic-copy tasks; pair it with the skill for the requested output format.
---

# Arabic Content Quality

Use this skill as the Arabic language, Unicode, RTL, and compatibility layer on top of the skill for the requested output format. Preserve the user's content, design, and target format.

## Core contract

- Store Arabic in normal logical Unicode order. Never reverse characters, words, or lines and never pre-shape letters into Arabic Presentation Forms.
- Do not add invisible bidi controls (`RLE`, `LRE`, `RLO`, `LRO`, `PDF`, `RLI`, `LRI`, `FSI`, `PDI`, `LRM`, `RLM`, or `ALM`) as a general RTL fix. Use native paragraph, container, or document direction.
- Do not delete `ZWJ` or `ZWNJ` blindly; they may be linguistically meaningful. Flag unexpected occurrences and remove them only when safe.
- Set Arabic language metadata (`ar-SA` unless the requested locale differs), native RTL direction, and intentional alignment independently.
- Keep long English passages, URLs, email addresses, file paths, citations, formulas, and code in separate LTR containers when the format permits.
- Choose a font with Arabic glyph coverage. Do not claim a font is embedded or portable unless verified. Supply PDF when fixed appearance matters.
- Use native list and numbering features. Do not fake bullets, indentation, tables, or reading order with spaces or typed glyphs.
- Preserve editable source files whenever editability is requested; PDF is a fixed-output companion, not a replacement.

Read [references/unicode-and-writing.md](references/unicode-and-writing.md) whenever authoring or repairing Arabic text. Then read only the reference for the target format:

- PowerPoint: [references/presentations.md](references/presentations.md), including the bundled PPTX audit/repair tool.
- Word/PDF: [references/documents-and-pdf.md](references/documents-and-pdf.md), including the bundled DOCX audit/repair tool.
- Web/UI/spreadsheets/images: [references/digital-formats.md](references/digital-formats.md)
- Final verification: [references/qa.md](references/qa.md)

## Workflow

1. Identify the Arabic locale, target application, editable source format, and whether the artifact is Arabic-first or bilingual. Infer these from the request when safe.
2. Author plain Unicode text, applying RTL through native format properties rather than invisible characters.
3. Separate incompatible base directions at paragraph, text-box, cell, or component boundaries.
4. Validate structure, then render the whole artifact and inspect Arabic shaping, ordering, wrapping, punctuation, numbers, bullets, tables, overflow, and font substitution.
5. Test in the user's target application when available. Do not treat a secondary renderer as proof of Microsoft PowerPoint, Word, browser, or Google behavior.
6. Report structural QA, visual/layout QA, target-application QA, and font portability separately. Never claim universal cross-application perfection without testing those applications.

## Safe automation boundary

The bundled OOXML tools have separate `audit` and `repair` commands. Audit is read-only. Repair must write a distinct output file, preserve the source, and must not overwrite an existing output unless the user explicitly supplies `--force`. A structural audit does not replace rendered or target-application QA.

## Source attribution

The bundled PPTX repair/audit helper is derived from Sultan Alsafran's MIT-licensed `arabic-presentations` skill. Preserve [THIRD_PARTY_LICENSE.md](THIRD_PARTY_LICENSE.md) when sharing or modifying this skill.
