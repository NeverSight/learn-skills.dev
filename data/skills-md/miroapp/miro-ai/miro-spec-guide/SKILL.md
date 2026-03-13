---
name: miro-spec-guide
description: >-
  Learn how to extract Miro specifications to local files and use them for
  AI-assisted planning and implementation. Use when working with Miro specs or
  when user wants to download board content for reference.
---

# Miro Spec Extraction Guide

## What is miro-spec?

The miro-spec plugin extracts specification content from Miro boards and saves it to local files. This enables AI to reference specs during planning and implementation without requiring repeated API calls.

## When to Use miro-spec

Use miro-spec when you need to:
- Extract product requirements from Miro boards
- Save design specifications for implementation
- Download prototypes and diagrams for reference
- Create local copies of documentation from Miro
- Work with specs offline or in version control

## Command: /miro-spec:get

Extract specs from a Miro board or item:

```bash
/miro-spec:get [url]
```

### URL Types

**Board URLs** - Extract all spec items:
```
https://miro.com/app/board/uXjVK123abc=/
```

**Item URLs** - Extract single item:
```
https://miro.com/app/board/uXjVK123abc=/?moveToWidget=3458764612345
```

## Understanding .miro/specs/ Directory

### Directory Structure

```
.miro/specs/
├── documents/      # Miro documents (Markdown format)
├── diagrams/       # Diagram descriptions (Markdown)
├── prototypes/     # Prototype containers (Markdown) and screens (HTML)
├── tables/         # Table data (JSON)
├── frames/         # Frame summaries (Markdown)
├── other/          # Unknown types like slides (Markdown)
├── images/         # Downloaded images (PNG)
└── index.json      # Metadata index
```

### Content Types

**Documents** (`.md`)
- Markdown content with formatting
- Preserved headings and structure
- Clean text format

**Diagrams** (`.md`)
- AI-generated description of diagram
- Flow analysis and component relationships
- Key elements and connections

**Prototypes** (`.md` / `.html`)
- Containers: Markdown with navigation map (`.md`, suffix `-container`)
- Screens: HTML markup with UI layout (`.html`, suffix `-screen`)
- UI component structure

**Tables** (`.json`)
- Structured data with column definitions
- All rows and cell values
- Column types and metadata

**Frames** (`.md`)
- AI-generated summary of frame contents
- Overview of contained items
- Organizational structure

**Images** (`.png`)
- Automatically extracted from prototypes
- Referenced by relative paths in prototype screens
- Named by Miro item ID

## Extraction Workflow

### 1. Run Extraction Command

```bash
/miro-spec:get https://miro.com/app/board/uXjVK-spec=/
```

### 2. Handle Existing Content

If `.miro/specs/` already has files, choose:
- **Clean and extract fresh** - Start over
- **Add to existing** - Keep current files
- **Cancel** - Abort

### 3. Review Extraction Summary

Output shows:
```
Extracted 5 documents, 3 diagrams, 2 prototypes, 1 table
Downloaded 12 images
Saved to .miro/specs/
```

### 4. Check Metadata Index

Open `.miro/specs/index.json` to see:
- All extracted items with types
- File paths for each item
- Original Miro URLs
- Extraction timestamp

## Board URLs vs Item URLs

### Board URLs

**When to use:**
- Extract complete specifications
- Get all related documents and diagrams
- Comprehensive spec extraction

**What it does:**
- Lists all items on the board
- Filters for spec-related types
- Extracts each item individually

**Example:**
```bash
/miro-spec:get https://miro.com/app/board/uXjVK123abc=/
```

### Item URLs

**When to use:**
- Extract single document or diagram
- Get specific prototype screen
- Targeted extraction

**What it does:**
- Extracts only the specified item
- Faster for single items
- Uses `moveToWidget` parameter

**Example:**
```bash
/miro-spec:get https://miro.com/app/board/uXjVK123abc=/?moveToWidget=3458764612345
```

## How Images Are Extracted

### Automatic Image Discovery

1. Plugin scans prototype screen HTML content
2. Finds Miro image URLs in `src` attributes
3. Extracts board_id and item_id from URLs
4. Downloads each image using Miro MCP

### URL Replacement

Original HTML:
```html
<img src="https://miro.com/api/v2/boards/uXjVK123abc=/images/3458764612345"/>
```

After extraction:
```html
<img src="../images/3458764612345.png"/>
```

### Benefits

- Images work offline
- No API calls to view documents
- Faster loading from local files
- Can be committed to version control

## Using Specs for Implementation Planning

### Workflow Example

1. **Extract specs:**
   ```bash
   /miro-spec:get https://miro.com/app/board/uXjVK-product-spec=/
   ```

2. **Review what was extracted:**
   Check `.miro/specs/index.json` to see available specs

3. **Ask AI to plan implementation:**
   "Based on the specs in .miro/specs/, create an implementation plan for the user authentication feature"

4. **AI reads relevant files:**
   AI automatically reads documents, diagrams, and tables during planning

5. **Implement with context:**
   AI uses spec content to guide code generation

### Example AI Prompts

**Planning with specs:**
```
"Review the product requirements in .miro/specs/documents/ and create a technical implementation plan"
```

**Using specific diagrams:**
```
"Reference the architecture diagram in .miro/specs/diagrams/3458764612345.md and implement the database schema"
```

**Validating implementation:**
```
"Compare the authentication flow I implemented against the spec in .miro/specs/prototypes/3458764612346.html"
```

## Best Practices

### Extraction Strategy

- Use board URLs for initial comprehensive extraction
- Use item URLs for updating specific documents
- Extract before starting implementation
- Re-extract when specs change

### Directory Management

- Keep `.miro/specs/` in `.gitignore` if specs are temporary
- Commit to version control if specs should be shared
- Clean extraction when board structure changes significantly
- Add to existing when updating individual items

### Working with Specs

- Always check `index.json` first to understand what's available
- Read HTML files directly for full document content
- Use markdown files for quick diagram overviews
- Parse JSON files for structured table data

### Performance Tips

- Extract from specific frames using item URLs if board is large
- Clean old extractions to avoid confusion
- Use board URLs sparingly (can be slow for large boards)
- Cache extractions between implementation sessions

## Common Workflows

### Extract Product Requirements

```bash
# Extract all PRD documents
/miro-spec:get https://miro.com/app/board/uXjVK-prd=/

# Review extracted docs
cat .miro/specs/index.json | grep documents

# Plan implementation
"Plan implementation based on requirements in .miro/specs/"
```

### Update Single Specification

```bash
# Extract updated design doc
/miro-spec:get https://miro.com/app/board/uXjVK=/.../?moveToWidget=3458764612345

# Choose "Add to existing" when prompted
# Review changes in .miro/specs/documents/3458764612345.html
```

### Extract Architecture Diagrams

```bash
# Extract board with diagrams
/miro-spec:get https://miro.com/app/board/uXjVK-architecture=/

# Check diagram summaries
ls .miro/specs/diagrams/
cat .miro/specs/diagrams/*.md
```

## Troubleshooting

**No items extracted from board:**
- Board may not contain document/frame/table items
- Try using item URL for specific content
- Check if board URL is correct

**Images not downloading:**
- Some images may not be accessible via MCP
- Original URLs preserved if download fails
- Documents still readable with external image URLs

**Files not found after extraction:**
- Check `.miro/specs/index.json` for actual paths
- Verify extraction completed successfully
- Look for error messages in extraction output

**Large boards taking too long:**
- Use item URLs to extract specific content
- Extract individual frames instead of entire board
- Consider filtering by content type

## See Also

- [Spec Storage Format](references/spec-storage.md) - Detailed file format documentation
- [Miro MCP Tools](../../miro/skills/miro-mcp/SKILL.md) - Understanding Miro MCP capabilities
- Plugin README - Installation and setup instructions
