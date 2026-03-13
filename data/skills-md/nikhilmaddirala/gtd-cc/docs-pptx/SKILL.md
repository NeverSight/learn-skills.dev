---
name: docs-pptx
description: This skill should be used when the user asks to "convert pptx to markdown", "parse powerpoint presentation", "extract slides to markdown", "convert presentation to markdown with images", "make powerpoint accessible", or needs to transform PowerPoint files into markdown format with inline images and alt-text descriptions.
version: 0.2.0
---

# PPTX to Markdown Conversion

Convert PowerPoint presentations to markdown format with inline slide images and AI-generated alt-text descriptions. The conversion produces a complete markdown document suitable for documentation, archival, version control, or AI analysis.

## When to Use This Skill

Use this skill for PowerPoint presentations that need markdown conversion for:

- Documentation and archival of presentation content
- Making presentations accessible to AI analysis workflows
- Creating searchable, version-controllable presentation archives
- Generating accessible presentations with detailed alt-text
- Preserving presentation content in a portable text format

## Conversion Workflow

The conversion has two main phases:

**Deterministic (scripted):**
1. PPTX → PDF conversion using LibreOffice
2. PDF → JPEG slide images using poppler-utils
3. Text extraction using markitdown
4. Markdown assembly with inline images

**Non-deterministic (AI-assisted):**
5. Alt-text generation using multimodal image understanding

## Step 1: Run the Conversion Script

Execute the provided Python script to handle all deterministic conversion steps:

```bash
./scripts/convert_pptx_to_markdown.py <input.pptx> <output_dir>
```

**Example:**
```bash
./scripts/convert_pptx_to_markdown.py source/presentation.pptx output/
```

**Optional flags:**
- `--dpi 150` - Image resolution (default: 150, higher=better quality/larger files)
- `--title "Custom Title"` - Override auto-detected presentation title

**Output structure:**
```
output/
├── presentation.md              # Final markdown with inline images
├── presentation-text.md         # Extracted text (intermediate)
├── pdf/
│   └── presentation.pdf         # Generated PDF (intermediate)
└── slide-images/
    └── slide-01.jpg ... slide-N.jpg  # Slide images at specified DPI
```

**Requirements:**
- LibreOffice (soffice command)
- poppler-utils (pdftoppm command)
- Python 3.11+ with uv

See references/troubleshooting.md for installation instructions for your operating system.

**Progress output:** The script shows progress for each step and reports any errors with clear messages.

## Step 2: Generate Alt-Text Descriptions

After the script completes, create detailed image descriptions for accessibility:

1. Read all slide images in `output/slide-images/`
2. Analyze each slide's visual content:
   - Chart types and structure (bars, lines, tables, dual-panels)
   - Color schemes and what they represent
   - Key data points and trends
   - Layout and visual hierarchy
   - Business insights from visualizations
3. Write comprehensive descriptions to `output/alt-texts.md`

**Format for alt-texts.md:**
```markdown
# Alt-Text Descriptions

## Slide 1

[Detailed description of title slide, branding, layout]

## Slide 2

[Description of chart type, colors, data structure, insights]

...
```

**Alt-text best practices:**
- Describe chart types explicitly (stacked bars, line graphs, tables)
- Explain color coding and what colors represent
- Note key data points and trends visible
- Include business context where relevant
- Make descriptions useful for both screen readers and AI analysis

## Step 3: Validate Output

Verify conversion succeeded:

- [ ] All slides converted to images (count matches slide count in presentation)
- [ ] Final markdown created with inline image references
- [ ] Images display correctly when viewing markdown
- [ ] Alt-texts.md created with descriptions for all slides
- [ ] No error messages in script output

**Quick validation:**
```bash
# Count slides in output
ls output/slide-images/slide-*.jpg | wc -l

# View the final markdown
cat output/presentation.md
```

## Troubleshooting

If the conversion script fails, see **references/troubleshooting.md** for solutions to common issues:

- LibreOffice not found or conversion errors
- Image export failures with poppler-utils
- System library errors with markitdown
- Missing slide markers in extracted text
- Broken image links in markdown

The troubleshooting reference includes detailed solutions, alternative approaches, and debugging strategies.

## Integration with CSF Workflows

This skill is particularly useful for CSF presentation processing:

- Convert Stage 7 (Presentation) deliverables to markdown for archival
- Generate alt-texts that capture chart types and business metrics
- Enable searching across presentations for specific analyses
- Version control presentation content alongside code and data
- Make analytical insights accessible to AI workflows

When working with CSF presentations, pay attention to:
- Color schemes (typically red/orange/blue for Price/CSF/MCV)
- Dual-panel comparison layouts (channel vs channel analysis)
- Stacked bar charts showing component breakdown
- Performance tables and metric comparisons

## Example

See **examples/uk_bbq_presentation/** for a complete reference conversion:
- Source: 15-slide CSF study presentation
- Output: Markdown with inline images and detailed alt-texts
- Demonstrates: Business analytics charts, dual-panel layouts, color-coded metrics

View the example to understand expected output format and alt-text patterns.

## Best Practices

- **Preserve originals**: Never modify source files in shared folders; work with copies
- **Validate immediately**: Check each conversion before moving to alt-text generation
- **Descriptive alt-texts**: Make descriptions valuable for both accessibility and AI understanding
- **Consistent DPI**: Use 150 DPI for good quality/size balance (adjust if needed)
- **Version control**: Commit markdown outputs to track presentation changes
- **Document process**: Note any special handling needed for specific presentations

## Key Files

- **scripts/convert_pptx_to_markdown.py** - Main conversion script (Python with uv)
- **references/troubleshooting.md** - Common issues and solutions
- **examples/uk_bbq_presentation/** - Complete reference example

## Quick Start

```bash
# 1. Run conversion script
./scripts/convert_pptx_to_markdown.py source/presentation.pptx output/

# 2. Generate alt-texts (AI-assisted)
# Read slide images and write detailed descriptions to output/alt-texts.md

# 3. Validate results
ls output/slide-images/ | wc -l  # Should match slide count
cat output/presentation.md        # View final markdown
```

The script handles all deterministic steps with proper error handling. Focus on generating high-quality alt-text descriptions that preserve the analytical and visual context of the presentation.
