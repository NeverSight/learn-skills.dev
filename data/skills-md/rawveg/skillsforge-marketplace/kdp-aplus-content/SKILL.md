---
name: kdp-aplus-content
description: Create Amazon-compliant A+ Content for KDP books with text, module layouts, and image specs. Use for A+ Content creation, book detail page design, module selection, compliance checking, rejection avoidance, or KDP marketing materials.
---

# KDP A+ Content Generator

Generate Amazon-compliant A+ Content for KDP books with proper module selection, text, and image specifications.

## Workflow

### 1. Gather Book Information

Ask the user for:
- **Book genre and type**: e.g., "Urban fantasy series, Book 3 of 5" or "Standalone romance novel"
- **Target content focus**: series showcase, author background, cover art, book sample, or combination
  - Example: "Show all books in my trilogy + author bio"
- **Available assets**: book covers, author photos, character art, etc.
  - Example: "I have cover images for all 5 books and a professional author headshot"
- **Book's ASIN**: if already published (e.g., "B08XXXXXX")
- **Existing book description or key selling points**
  - Example: "Epic battles, found family themes, LGBTQ+ representation"

### 2. Select Appropriate Modules

Based on content focus, recommend modules from `references/modules.md`:

**For series books**: Comparison Chart, Technical Specifications
**For author focus**: Single Image & Sidebar, Single Left Image
**For visual impact**: Image & Text Overlay, Image Header With Text
**For content preview**: Three Images and Text, Product Description Text

Maximum 5 modules per layout. Preview desktop and mobile display.

### 3. Generate Compliant Content

#### Text Content
- Spell out numbers under 10
- Use Oxford commas and proper capitalization
- Avoid promotional language ("buy now," "free," "affordable")
- No time-sensitive terms ("new," "latest," "now")
- Maximum 4 quotes (well-known publications/figures only with attribution)
- No competitor comparisons
- No guarantees or pricing

#### Module-Specific Text
Generate text appropriate for each module type:
- Headers: Capitalize major words
- Body text: Concise, scannable, highlight key points
- Comparison charts: Factual differences only
- Technical specs: Clear, organized information

### 4. Provide Image Specifications

For each module, specify from `references/image-specs.md`:
- Required dimensions (minimum and recommended)
- File format (JPG/PNG, RGB colorspace)
- Resolution (300 DPI recommended, 72 DPI minimum)
- File size (under 2 MB)
- Alt-text requirements

### 5. Compliance Check

Before finalizing, verify against `references/guidelines.md`:

**Top rejection reasons**:
- ✓ No pricing/promotional language
- ✓ No customer reviews
- ✓ No time-sensitive information
- ✓ Quotes limited to 4, properly attributed
- ✓ Images unique to A+ (not from product gallery)
- ✓ No competitor comparisons
- ✓ No guarantees or return policies
- ✓ Numbers under 10 spelled out
- ✓ Oxford commas used
- ✓ Headers properly capitalized

### 6. Output Format

Provide:
1. **Module layout recommendation** with reasoning
2. **Text content** for each module
3. **Image specifications** for each module (dimensions, format, DPI)
4. **Alt-text** for accessibility
5. **Compliance checklist** confirming all guidelines met

## Reference Files

Load as needed for detailed information:

- **`references/guidelines.md`**: Complete Amazon A+ Content Guidelines
  - Content restrictions and prohibitions
  - Image and text formatting rules
  - Claims and awards requirements
  - Common rejection reasons

- **`references/modules.md`**: All 17 module specifications
  - Module selection by use case
  - Detailed specifications per module
  - Layout best practices
  - AI-Ready module information

- **`references/image-specs.md`**: Technical image requirements
  - Format and resolution specifications
  - Module-specific image dimensions
  - DPI calculation methods
  - Quality guidelines and troubleshooting

## Important Notes

- A+ Content appears under "From the Publisher" section on book detail pages
- Review timeline: 8 business days (may be longer during high volume)
- Can apply same A+ Content to multiple ASINs (different formats of same book)
- Content auto-copied to other marketplaces supporting the same language
- US marketplace supports generative AI for English content (AI Ready modules)
- Must have all necessary rights for images and text
- Can update, duplicate, suspend, or delete content after publication

## Common Use Cases

**Series promotion**: Use Comparison Chart + Technical Specifications modules to showcase all books

**Author branding**: Use Single Image & Sidebar for author photo and bio

**Visual storytelling**: Use Image & Text Overlay or Image Header With Text for atmospheric content

**Content preview**: Use Product Description Text or Three Images and Text for book samples

**Multi-purpose layout**: Combine up to 5 modules (e.g., Image Header + Author Sidebar + Comparison Chart)
