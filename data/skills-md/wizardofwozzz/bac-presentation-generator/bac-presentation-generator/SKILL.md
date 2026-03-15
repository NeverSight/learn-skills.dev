---
name: bac-presentation-generator
description: Transforms markdown files into brand-compliant BAC HTML presentations with professional styling, proper typography, and integrated branding. Supports manual browser-based PDF export.
---

# BAC Presentation Generator

Transforms markdown files into brand-compliant BAC HTML presentations with professional styling, proper typography, and integrated branding. Generated HTML files can be manually exported to PDF via browser print functionality.

## When to Use This Skill

Use this skill when you need to:
- Convert markdown into BAC-branded HTML presentation slides
- Create professional client-facing presentations that comply with BAC brand guidelines
- Generate aesthetically pleasing slide decks with proper typography, colors, and layout
- Transform presentation content into a 16:9 slide format suitable for export to PDF
- Create presentations with title slides, content slides, and section dividers

Do NOT use this skill for:
- Creating PowerPoint (.pptx) files (this outputs HTML only)
- Creating Google Slides presentations
- Documents that require continuous flow (use bac-document-generator instead)
- Animated or interactive presentations (this generates static slides)
- Situations requiring automatic PDF generation (use manual browser print instead)

## Core Workflow

Follow this workflow exactly. Each step must be completed before proceeding to the next.

### Step 1: Analyze Presentation Structure

**Objective**: Understand the presentation content structure and identify slide elements.

**Actions**:
1. Read the provided markdown file completely
2. Identify presentation metadata (title, client, date, version, etc.)
3. Count and categorize slide content:
   - Title slide (first slide with H1 + H2)
   - Section dividers (slides with only H1 or H1+H2)
   - Content slides (slides with H2 + content)
4. Catalog content elements within slides:
   - Headings (H2-H4 for content slides)
   - Bullet points and lists
   - Tables and data
   - Code blocks or quotes
5. Note any BAC-specific requirements mentioned by the user

**Output**: Mental model of presentation structure (do not create files yet)

### Step 2: Evaluate Brand Compliance Requirements

**Objective**: Define evaluation criteria for the output presentation.

**Actions**:
1. Reference `reference/BRAND_GUIDELINES.md` for:
   - Color palette requirements
   - Typography specifications
   - Logo placement rules
   - Spacing and layout principles
2. Determine presentation type and appropriate styling:
   - Client proposal: formal, comprehensive branding
   - Internal update: clean, data-focused
   - Sales pitch: compelling, visually engaging

**Evaluation Criteria** (presentation must meet ALL):
- [ ] Uses only BAC brand colors (primary blue #0066FF, navy #042A4C, approved grays)
- [ ] Typography uses Moderat and Suisse Int'l (with web-safe fallbacks)
- [ ] Logo appears on title slide (top-left, proper clearance)
- [ ] Slides are 16:9 aspect ratio (1920×1080px)
- [ ] Footer on content slides (company name + slide numbers)
- [ ] Tables styled consistently with brand (blue headers, alternating rows)
- [ ] Headings follow typographic hierarchy
- [ ] Professional spacing and layout on all slides
- [ ] PDF-export ready (print styles, page breaks per slide)
- [ ] No style violations (wrong colors, fonts, or layouts)

### Step 3: Generate HTML Presentation

**Objective**: Convert markdown to brand-compliant HTML slides with low variability.

**Actions**:
1. Use the conversion script at `scripts/convert_md_to_html.js`
2. Run: `node scripts/convert_md_to_html.js <input.md> <output.html>`
3. The script will:
   - Parse YAML frontmatter metadata
   - Split content by `---` delimiter into slides
   - Detect slide type (title, section, or content)
   - Convert markdown within each slide to HTML
   - Apply BAC CSS template from `templates/bac-presentation-template.html`
   - Insert logo on title slide
   - Add footer with slide numbers on content slides
   - Generate proper slide structure

**Critical**: Do NOT manually write HTML. Always use the script to ensure consistency.

**Slide Types**:
- **Title Slide**: First slide with H1 + H2, logo, metadata table
- **Section Slide**: H1 only (or H1+H2), centered, blue gradient background
- **Content Slide**: H2 heading + markdown content (lists, tables, text)

**Markdown Syntax**:
- Use `---` on its own line to separate slides
- First slide should have `# Main Title` and `## Subtitle`
- Section dividers: Use `# Section Name` with no other content
- Content slides: Start with `## Slide Title` followed by content

### Step 4: Validate Brand Compliance

**Objective**: Verify the generated presentation meets all evaluation criteria.

**Actions**:
1. Open the generated HTML file in a browser
2. Check against the evaluation criteria from Step 2:
   - Visual inspection of colors, fonts, spacing
   - Logo placement and sizing on title slide
   - Slide type detection (title, section, content)
   - Table formatting (blue headers, alternating rows)
   - Heading hierarchy within slides
   - Footer presence on content slides
   - Print preview (Cmd/Ctrl + P) for PDF export readiness
3. Review slide sequence and content flow
4. Identify any violations or styling issues

**If violations found**: Review `reference/BRAND_GUIDELINES.md` and adjust the template or script as needed.

### Step 5: Guide PDF Export (Manual Step)

**Objective**: Provide clear instructions for manual PDF generation via browser print.

**IMPORTANT**: PDF generation is now a manual process. The skill generates HTML only. After generating the HTML file, provide the user with these step-by-step instructions:

**PDF Generation Instructions to Provide to User**:

1. **Open the HTML file** in your web browser:
   - Recommended browsers: Chrome, Safari, Firefox, or Edge
   - Simply double-click the `.html` file, or right-click → "Open with" → [Browser]

2. **Open Print Dialog**:
   - **Mac**: Press `Cmd+P`
   - **Windows/Linux**: Press `Ctrl+P`

3. **Configure Print Settings** (CRITICAL for proper output):
   - **Destination**: Select "Save as PDF"
   - **Paper size**:
     - Ideal: Custom "1920 x 1080" pixels (16:9 landscape)
     - Alternative: "A4 Landscape" or "Letter Landscape"
   - **Background graphics**: MUST be enabled (checkbox: "Background graphics" or "Print backgrounds")
     - This is essential - BAC brand colors are background styles
     - Without this, the PDF will lose all colors, gradients, and styling
   - **Headers and footers**: Turn OFF (uncheck this option)
     - Slide footers are built into the slides themselves
     - Browser headers/footers would interfere
   - **Margins**: None or Minimum

4. **Save the PDF**:
   - Click "Save" or "Print"
   - Choose a descriptive filename (e.g., "Cloud-Migration-Presentation-v1.0.pdf")
   - Save to desired location

**Browser-Specific Notes**:
- **Chrome/Edge**: Settings → More settings → Check "Background graphics"
- **Safari**: Show Details → Check "Print backgrounds"
- **Firefox**: Options → Check "Print backgrounds"

**Final Check**: Open the saved PDF and verify:
- All brand colors appear (blue #0066FF, navy #042A4C, greys, gradients)
- Logo is visible and properly positioned on title slide
- Section slides have blue gradient backgrounds
- Tables have colored headers and alternating row backgrounds
- Footer with company name and slide numbers appears on content slides
- No browser-generated headers/footers
- All slides render correctly (one slide per page)
- No cut-off content or layout issues
- Presentation looks professional and brand-compliant

**If colors are missing**: The user forgot to enable "Background graphics" - they must regenerate the PDF with that setting enabled.

## File References

When you need detailed specifications, reference these files:

- `reference/BRAND_GUIDELINES.md` - Complete brand specifications extracted from official guidelines
- `reference/VALIDATION_CHECKLIST.md` - Presentation-specific validation checklist
- `templates/bac-presentation-template.html` - Base HTML/CSS template with BAC slide styling
- `scripts/convert_md_to_html.js` - Conversion script (Node.js required)

## Terminology

Use consistent terms throughout:
- **Brand compliance**: Adherence to BAC brand guidelines for colors, typography, and layout
- **Slide types**: Title, section, and content slides
- **Evaluation criteria**: Specific checkpoints that must be met for brand compliance
- **PDF-export ready**: HTML that renders correctly when printed to PDF with one slide per page
- **Template**: The base HTML/CSS file that defines BAC slide styling
- **Conversion script**: JavaScript tool that transforms markdown to branded HTML slides

## Common Issues and Solutions

### Issue: Slide delimiter not working
**Solution**: Ensure `---` is on its own line with blank lines before and after. Format:
```
Content above

---

Content below
```

### Issue: Title slide not detected
**Solution**: First slide must have both `# Main Title` and `## Subtitle` to be recognized as title slide.

### Issue: Section slide shows as content slide
**Solution**: Section slides should have ONLY H1 (and optionally H2), with no other content. Remove lists, paragraphs, or tables.

### Issue: Fonts don't render correctly
**Solution**: The template includes web-safe fallbacks. For final PDFs, fonts will render as specified in CSS.

### Issue: Tables are too wide for slide
**Solution**: Tables automatically scale to slide width. For complex tables, consider splitting into multiple slides or simplifying the data.

### Issue: Logo doesn't appear
**Solution**: Verify `assets/HOR_Fullcolour_Positive_RGB.png` exists. Script uses base64 encoding for portability.

### Issue: Colors look wrong in PDF
**Solution**: Check browser's print preview. Ensure "Background graphics" is enabled. This is the most common issue.

### Issue: Slide numbers not showing
**Solution**: Slide numbers only appear on content slides, not on title or section slides (by design).

## Requirements

- Node.js installed (for conversion script)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Markdown source file with proper slide delimiters (`---`)
- Access to this skill directory

## Success Criteria

The skill succeeds when:
1. Markdown is converted to HTML slides without errors
2. All evaluation criteria are met
3. Slide types are correctly detected (title, section, content)
4. PDF exports cleanly with one slide per page
5. Presentation looks professional and matches BAC brand standards
6. User approves final output

## Notes

- This skill emphasizes **low freedom during execution** (use scripts and templates) but **high freedom during analysis** (understand and adapt to content structure)
- Always validate before delivering to user
- Keep evaluation criteria visible and check systematically
- If user requests deviations from brand guidelines, confirm explicitly before proceeding
- Presentations should follow best practices: concise content, visual hierarchy, minimal text per slide
