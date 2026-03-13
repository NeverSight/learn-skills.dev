---
name: document-polisher
description: "Transform any DOCX document with world-class brand styling. Choose from 10 premium brand aesthetics (The Economist, McKinsey, Deloitte, KPMG, Stripe, Apple, IBM, Notion, Linear, Figma) to polish documents with professional typography, colors, and formatting. Use when users want to: (1) Apply premium brand styling to documents, (2) Make documents look more professional, (3) Match a specific brand's visual identity, (4) Create polished reports, proposals, or presentations."
---

# Document Polisher

Transform any document into a polished, professionally-styled masterpiece using world-class brand aesthetics.

## Overview

This skill applies premium brand styling from 10 carefully curated brands to DOCX documents. Each brand has been analyzed for its typography, color palette, and design principles to create authentic-looking documents.

## Brand Selection Menu

When a user wants to polish a document, ALWAYS present this selection menu:

```
╔══════════════════════════════════════════════════════════════════════════╗
║                        DOCUMENT POLISHER                                 ║
║                    Select Your Brand Style                               ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  EDITORIAL                                                               ║
║  ─────────                                                               ║
║  1. The Economist    │ Deep navy + serif typography                      ║
║                      │ Best for: Reports, analysis, thought leadership   ║
║                                                                          ║
║  CONSULTING                                                              ║
║  ──────────                                                              ║
║  2. McKinsey         │ Sharp corners + bold blue accents                 ║
║                      │ Best for: Strategy decks, executive summaries     ║
║                                                                          ║
║  3. Deloitte         │ Teal-blue + pill-shaped elements                  ║
║                      │ Best for: Audits, assessments, formal reports     ║
║                                                                          ║
║  4. KPMG             │ Two-tone blue + condensed headings                ║
║                      │ Best for: Financial reports, compliance docs      ║
║                                                                          ║
║  TECH                                                                    ║
║  ────                                                                    ║
║  5. Stripe           │ Dark blue + purple gradients                      ║
║                      │ Best for: API docs, developer guides, specs       ║
║                                                                          ║
║  6. Apple            │ Minimalist + generous whitespace                  ║
║                      │ Best for: Product docs, user guides               ║
║                                                                          ║
║  7. IBM              │ Plex typography + Carbon design                   ║
║                      │ Best for: Technical docs, enterprise reports      ║
║                                                                          ║
║  8. Linear           │ Modern purple + precise typography                ║
║                      │ Best for: Product specs, changelogs, dev docs     ║
║                                                                          ║
║  PRODUCTIVITY                                                            ║
║  ────────────                                                            ║
║  9. Notion           │ Clean blue + subtle accents                       ║
║                      │ Best for: Wikis, project plans, documentation     ║
║                                                                          ║
║  DESIGN                                                                  ║
║  ──────────                                                              ║
║  10. Figma           │ Vibrant multi-color palette                       ║
║                      │ Best for: Creative briefs, design docs, brands    ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

## Workflow

### Step 1: Ask the User

When a user wants to polish a document:
1. Display the brand selection menu above
2. Ask: "Which brand style would you like to apply? You can also tell me the purpose of your document and I'll recommend a style."

### Step 2: Apply the Styling

**IMPORTANT: Always use the Python script with python-docx. Never use direct XML/OOXML manipulation as it can corrupt documents.**

#### Primary Method: Python Script (REQUIRED)

The script uses python-docx to safely recreate documents with brand styling. It:
- Reads the source document
- Creates a new document with brand styles applied
- Copies all content with proper formatting
- Preserves bold, italic, lists, and structure

```bash
# Ensure python-docx is installed in the environment
pip install python-docx

# Apply brand styling
python scripts/apply_brand.py <input.docx> <brand_name> <output.docx>

# Examples:
python scripts/apply_brand.py report.docx economist polished_report.docx
python scripts/apply_brand.py proposal.docx mckinsey styled_proposal.docx
python scripts/apply_brand.py guide.docx stripe tech_guide.docx
```

#### Available Brand Names:
- `economist` - The Economist (editorial, serif)
- `mckinsey` - McKinsey & Company (consulting, sharp)
- `deloitte` - Deloitte (consulting, teal)
- `kpmg` - KPMG (consulting, bold blue)
- `stripe` - Stripe (tech, dark blue/purple)
- `apple` - Apple (tech, minimalist)
- `ibm` - IBM (tech, enterprise)
- `notion` - Notion (productivity, clean)
- `linear` - Linear (tech, modern purple)
- `figma` - Figma (design, colorful)

### What the Script Does

1. **Loads brand configuration** from `templates/brand-mapping.json`
2. **Creates a fresh document** (avoids corruption from XML editing)
3. **Applies document-level styles:**
   - Normal text style (font, size, color)
   - Heading 1, 2, 3 styles (font, size, color, spacing)
   - Title style
   - Page margins
4. **Copies content with formatting:**
   - Preserves headings at correct levels
   - Maintains bullet and numbered lists
   - Keeps bold, italic, underline formatting
   - Preserves paragraph alignment
   - Copies tables with styling
5. **Saves as new file** (never overwrites original)

## Brand Reference Files

Detailed brand guidelines are stored in the `brands/` directory:

| Brand | Reference File | Key Elements |
|-------|---------------|--------------|
| The Economist | `brands/economist.md` | Georgia serif, #1F2E7A navy, minimal borders |
| McKinsey | `brands/mckinsey.md` | Helvetica Neue, #051C2C dark, sharp corners |
| Deloitte | `brands/deloitte.md` | Open Sans, #007CB0 teal, rounded elements |
| KPMG | `brands/kpmg.md` | Open Sans, #1E49E2 blue |
| Stripe | `brands/stripe.md` | Helvetica Neue, #0A2540 + #9966FF purple |
| Apple | `brands/apple.md` | Helvetica Neue, #0071E3 blue, minimal |
| IBM | `brands/ibm.md` | Arial, #0F62FE blue, sharp corners |
| Notion | `brands/notion.md` | Arial, #0075DE blue, block-based |
| Linear | `brands/linear.md` | Arial, #5E6AD2 purple, modern |
| Figma | `brands/figma.md` | Arial, multi-color palette |

## Style Mapping

The `templates/brand-mapping.json` file contains structured data for programmatic styling:

```json
{
  "brands": {
    "economist": {
      "name": "The Economist",
      "colors": {
        "primary": "#1F2E7A",
        "accent": "#E3120B",
        "textPrimary": "#0D0D0D"
      },
      "typography": {
        "headingFont": "Georgia",
        "bodyFont": "Georgia"
      },
      "styles": {
        "h1": { "size": 28, "color": "#1F2E7A", "bold": true },
        "h2": { "size": 22, "color": "#1F2E7A", "bold": true },
        "body": { "size": 11, "color": "#0D0D0D" }
      }
    }
  }
}
```

## Examples

### Example 1: Polish a Report with McKinsey Style

User: "Make my quarterly report look more professional"

1. Show brand menu
2. User selects "McKinsey"
3. Apply styling:

```bash
cd /path/to/project
source venv/bin/activate  # if using virtual environment
python .claude/skills/document-polisher/scripts/apply_brand.py quarterly_report.docx mckinsey polished_quarterly_report.docx
```

### Example 2: Apply Economist Style to a Guide

User: "Style this guide like The Economist"

```bash
python .claude/skills/document-polisher/scripts/apply_brand.py guide.docx economist guide_economist.docx
```

### Example 3: Tech Documentation with Stripe Style

User: "Make this API doc look like Stripe's documentation"

```bash
python .claude/skills/document-polisher/scripts/apply_brand.py api_doc.docx stripe api_doc_stripe.docx
```

## Dependencies

- **Python 3.x**
- **python-docx**: `pip install python-docx`

The script will check for python-docx and provide installation instructions if missing.

## Tips for Best Results

1. **Match brand to content**: Use consulting brands for business docs, tech brands for technical content
2. **Consider your audience**: Economist for academics, Stripe for developers, Apple for consumers
3. **Don't over-brand**: The goal is professional polish, not exact brand copying
4. **Test with PDF export**: Some styling looks different in PDF vs Word
5. **Use virtual environment**: Keeps dependencies isolated

## Troubleshooting

### "Module not found: docx"
```bash
pip install python-docx
```

### Document looks wrong
- Ensure the source document uses standard Word styles (Heading 1, 2, 3, Normal)
- Check that lists use built-in List Bullet/List Number styles

### Script path issues
Always run from the project root or use absolute paths:
```bash
python /full/path/to/.claude/skills/document-polisher/scripts/apply_brand.py input.docx brand output.docx
```

## Adding New Brands

To add a new brand:
1. Use FireCrawl to extract branding: `mcp__firecrawl__firecrawl_extract_branding`
2. Create a new file in `brands/<brand_name>.md`
3. Add entry to `templates/brand-mapping.json` with:
   - `name`, `description`, `category`
   - `colors`: primary, accent, background, textPrimary, textSecondary
   - `typography`: headingFont, bodyFont
   - `styles`: h1, h2, h3, body with size, color, bold
4. Test with sample documents
