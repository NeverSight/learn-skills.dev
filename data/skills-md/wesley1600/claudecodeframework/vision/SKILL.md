---
name: vision
description: Analyzes and processes images using Claude's vision capabilities. Supports OCR, image classification, diagram comparison, chart analysis, visual Q&A, and more. Use when users need to understand, extract, or analyze visual content.
license: Apache-2.0
allowed-tools:
  - Read
  - Write
  - Bash
  - WebFetch
  - Task
---

# Vision Image Processing Skill

## Overview

This skill leverages Claude's multimodal vision capabilities to analyze, process, and extract insights from images. It supports a wide range of visual understanding tasks including optical character recognition (OCR), image classification, diagram analysis, chart interpretation, and visual comparison.

## When to Use This Skill

Activate this skill when users need to:

- **Extract text** from images, screenshots, or scanned documents (OCR)
- **Classify or categorize** images based on visual content
- **Analyze charts, graphs, or data visualizations** to extract insights
- **Compare multiple images** (diagrams, screenshots, designs)
- **Describe or caption** images in detail
- **Answer questions** about visual content
- **Detect objects, people, or elements** within images
- **Analyze UI/UX** from screenshots or mockups
- **Read handwritten text** or notes
- **Process receipts, invoices, or forms** for data extraction

## Core Capabilities

### 1. Optical Character Recognition (OCR)

Extract text from images with high accuracy:

**Instructions:**
- Use the Read tool to load the image file
- Analyze the image and extract all visible text
- Preserve formatting, layout, and structure when possible
- Handle multiple languages and fonts
- Identify and extract text from challenging contexts (handwriting, artistic fonts, rotated text)

**Output Format:**
- Provide extracted text in markdown format
- Include confidence notes for challenging sections
- Maintain document structure (headings, paragraphs, lists)

**Example Use Cases:**
- Screenshot text extraction
- Scanned document digitization
- Receipt and invoice processing
- Handwritten note transcription
- Sign and label reading

### 2. Image Classification and Categorization

Identify and classify image content:

**Instructions:**
- Analyze the overall subject and context
- Identify primary objects, scenes, or themes
- Provide classification labels with confidence levels
- Detect style, mood, and artistic elements
- Categorize by industry-relevant taxonomies when applicable

**Output Format:**
```markdown
## Primary Classification
- Category: [main category]
- Confidence: [High/Medium/Low]

## Detected Elements
- Object 1: [description]
- Object 2: [description]
...

## Additional Attributes
- Style: [style description]
- Setting: [environment/context]
- Colors: [dominant colors]
```

### 3. Chart and Graph Analysis

Extract insights from data visualizations:

**Instructions:**
- Identify chart type (bar, line, pie, scatter, etc.)
- Extract data points, values, and trends
- Read axes labels, legends, and annotations
- Summarize key insights and patterns
- Flag anomalies or notable data points

**Output Format:**
```markdown
## Chart Analysis

**Type:** [Chart Type]

**Data Summary:**
[Extracted data in table or structured format]

**Key Insights:**
1. [Insight 1]
2. [Insight 2]
3. [Insight 3]

**Trends:**
- [Trend description]

**Notable Points:**
- [Anomalies or important observations]
```

### 4. Diagram and Visual Comparison

Compare multiple images or diagrams:

**Instructions:**
- Load all images to be compared
- Identify similarities and differences
- Highlight structural, content, and style variations
- Create side-by-side comparison tables
- Note additions, deletions, or modifications

**Output Format:**
```markdown
## Visual Comparison

**Image 1:** [description]
**Image 2:** [description]

### Similarities
- [Similarity 1]
- [Similarity 2]

### Differences
| Aspect | Image 1 | Image 2 |
|--------|---------|---------|
| [Aspect] | [Description] | [Description] |

### Overall Assessment
[Summary of comparison]
```

### 5. Detailed Image Description

Generate comprehensive image descriptions:

**Instructions:**
- Describe the overall scene or subject
- Identify and describe all visible elements
- Note spatial relationships and composition
- Describe colors, lighting, and atmosphere
- Mention text, logos, or symbols if present
- Consider accessibility (generate alt-text compatible descriptions)

**Output Format:**
- Natural language description (paragraph form)
- Structured element list (bulleted)
- Technical details (dimensions, format, quality notes)

### 6. Visual Question Answering

Answer specific questions about image content:

**Instructions:**
- Carefully read the user's question
- Examine the relevant areas of the image
- Provide accurate, specific answers
- Reference visual evidence when answering
- Acknowledge uncertainty if details are unclear

**Best Practices:**
- Be precise and factual
- Avoid assumptions beyond what's visible
- Describe what you see, not what you infer (unless asked)
- Use spatial language (top-left, center, background, etc.)

### 7. UI/UX and Design Analysis

Analyze user interfaces and design elements:

**Instructions:**
- Identify UI components (buttons, forms, navigation)
- Assess layout and visual hierarchy
- Note design patterns and conventions
- Evaluate accessibility considerations
- Compare against design best practices
- Extract color schemes and typography

**Output Format:**
```markdown
## UI/UX Analysis

**Component Inventory:**
- [List of UI elements]

**Layout Assessment:**
- [Layout description and grid analysis]

**Design Patterns:**
- [Identified patterns]

**Accessibility Notes:**
- [Contrast, readability, touch targets]

**Recommendations:**
- [Improvement suggestions]
```

### 8. Document and Form Processing

Extract structured data from forms, receipts, and documents:

**Instructions:**
- Identify document type and structure
- Extract field names and values
- Organize data into structured format (JSON, CSV, tables)
- Handle multi-column layouts
- Preserve data relationships and hierarchies

**Output Format:**
```json
{
  "document_type": "invoice",
  "fields": {
    "invoice_number": "value",
    "date": "value",
    "total": "value"
  },
  "line_items": [...]
}
```

## Workflow and Best Practices

### Standard Vision Processing Workflow

1. **Load the Image(s)**
   - Use the Read tool to access image files
   - Support formats: PNG, JPG, JPEG, GIF, WebP, PDF (single page)

2. **Understand the Request**
   - Identify the specific task (OCR, classification, analysis, etc.)
   - Note any special requirements or focus areas

3. **Analyze the Visual Content**
   - Apply Claude's vision capabilities to examine the image
   - Extract relevant information based on the task

4. **Structure the Output**
   - Format results according to the task type
   - Use markdown for readability
   - Include confidence indicators where appropriate

5. **Validate and Refine**
   - Check for completeness
   - Verify accuracy of extracted data
   - Provide follow-up options if needed

### Quality Guidelines

- **Accuracy First:** Prioritize correct information over comprehensive coverage
- **Structured Output:** Use consistent formatting for similar tasks
- **Confidence Indicators:** Note when details are unclear or ambiguous
- **Context Awareness:** Consider the user's domain and use case
- **Accessibility:** Generate descriptions suitable for screen readers when appropriate

### Limitations and Considerations

- **Image Quality:** Low resolution or blurry images may reduce accuracy
- **Supported Formats:** Primarily raster images; vector graphics may need conversion
- **Privacy:** Be cautious with sensitive information (PII, credentials, etc.)
- **Complex Diagrams:** Highly technical diagrams may require domain expertise clarification
- **Real-Time Data:** Cannot access live data or external resources not in the image

## Advanced Features

### Batch Processing

For multiple images:

```markdown
Processing images in batch:
1. [Image1.png] - [Task result]
2. [Image2.png] - [Task result]
3. [Image3.png] - [Task result]

Summary: [Overall findings]
```

### Multi-Modal Context

Combine visual analysis with code, documents, or data:

- Cross-reference image content with codebase files
- Validate design implementations against mockups
- Extract data and populate code templates
- Generate code from UI screenshots

### Helper Script Integration

For advanced processing, the skill includes a Python helper script at `scripts/image_processor.py`:

- Image format conversion
- Metadata extraction
- Batch file operations
- Image preprocessing (resize, enhance, crop)

**Usage:**
```bash
python .claude/skills/vision/scripts/image_processor.py --operation [convert|metadata|batch] --input [path]
```

## Examples

### Example 1: OCR from Screenshot

**User Request:** "Extract the text from this screenshot"

**Process:**
1. Load image with Read tool
2. Identify all text regions
3. Extract and format text
4. Preserve structure

**Output:**
```markdown
## Extracted Text

### Heading
Main paragraph text goes here...

### List Items
- Item 1
- Item 2
- Item 3

---
Note: Text extracted with high confidence. Minor formatting adjustments made for readability.
```

### Example 2: Chart Analysis

**User Request:** "Analyze this sales chart and tell me the key trends"

**Process:**
1. Load chart image
2. Identify chart type and data
3. Extract values and labels
4. Analyze trends

**Output:**
```markdown
## Sales Chart Analysis

**Chart Type:** Line graph with 3 series (2023-2025)

**Data Points:**
| Month | 2023 | 2024 | 2025 |
|-------|------|------|------|
| Jan   | 120K | 145K | 180K |
| Feb   | 135K | 150K | 195K |
...

**Key Insights:**
1. Consistent year-over-year growth of ~20%
2. Seasonal peak in Q4 across all years
3. 2025 showing accelerated growth trend

**Recommendation:** Prepare for continued high demand in Q4 2025
```

### Example 3: UI Component Comparison

**User Request:** "Compare these two design mockups and highlight the differences"

**Process:**
1. Load both images
2. Identify UI components in each
3. Compare layouts and elements
4. Document changes

**Output:**
```markdown
## Design Mockup Comparison

### Added Elements (Mockup 2)
- Search bar in header
- User avatar in top-right corner
- Breadcrumb navigation

### Removed Elements
- Sidebar menu (replaced with top navigation)

### Modified Elements
| Component | Mockup 1 | Mockup 2 |
|-----------|----------|----------|
| Primary Button | Blue (#007AFF) | Green (#34C759) |
| Typography | Roboto 16px | SF Pro 15px |
| Card Spacing | 16px | 24px |

### Layout Changes
- Shifted from sidebar to top navigation
- Increased content area width by ~30%
- Changed from 3-column to 4-column grid
```

## Integration with Claude Code

This skill works seamlessly with other Claude Code features:

- **Read Tool:** Load images from the filesystem
- **Write Tool:** Save processed results or extracted data
- **Bash Tool:** Run helper scripts for preprocessing
- **Task Tool:** Coordinate complex multi-image workflows

## Quick Reference

| Task | Command Pattern | Output Type |
|------|----------------|-------------|
| OCR | "Extract text from [image]" | Markdown text |
| Classification | "Classify this image" | Category labels |
| Chart Analysis | "Analyze this chart" | Data + insights |
| Comparison | "Compare [img1] and [img2]" | Diff table |
| Description | "Describe this image" | Paragraph |
| Q&A | "What [question] in this image?" | Answer |
| UI Analysis | "Analyze this UI screenshot" | Component breakdown |

## Tips for Best Results

1. **Provide Context:** Mention the domain or purpose (e.g., "medical diagram," "e-commerce UI")
2. **Be Specific:** Request specific information rather than general analysis
3. **Multiple Angles:** For complex images, ask follow-up questions
4. **File Paths:** Use absolute or relative paths correctly
5. **Batch Operations:** Process multiple similar images together for consistency

## Support and Troubleshooting

**Common Issues:**

- **"Cannot read image"** → Verify file path and format
- **"Low confidence extraction"** → Image may be too low resolution
- **"Unable to detect chart data"** → Chart may be too complex or stylized

**Getting Better Results:**

- Use high-resolution images (300+ DPI for documents)
- Ensure good contrast and lighting
- Crop images to focus on relevant areas
- Provide context about the image content

---

## License

This skill is licensed under Apache-2.0.

## Version

Version: 1.0.0
Last Updated: 2025-11-18
Compatible with: Claude Code (all versions with vision support)
