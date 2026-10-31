---
name: confluence-formatting
description: Use when formatting, translating, or structuring documentation for Confluence pages. Converts Markdown to Confluence Page Format (HTML with Confluence-specific markup). Handles headings, tables, lists, rich text, macros, panels, anchors, and labels.
---

# Confluence Formatting

Translate Markdown documentation into Confluence Page Format — HTML with Confluence-specific markup classes, data attributes, and macro syntax. This skill provides guidance and formatting tools only; it does not handle upload, API calls, or publishing mechanisms.

## When to Use

- Converting Markdown to Confluence-compatible HTML for publishing
- Structuring documentation destined for a Confluence space
- Formatting tables, panels, macros, or anchors for Confluence rendering
- The user mentions Confluence, publishing to Confluence, formatting for Confluence, or translating documentation to Confluence format

**NOT for:** uploading to Confluence, using the Confluence API, managing Confluence permissions or spaces, or generating Confluence Storage Format (XML).

## Procedure

### 1. Parse the Markdown input

Read the Markdown document and identify all structural elements:

- Headings (H1–H6) and their hierarchy
- Paragraphs, blockquotes, and horizontal rules
- Lists (ordered, unordered, nested)
- Tables with headers and rows
- Inline formatting (bold, italic, code, links, images)
- Block elements (code blocks, blockquotes, horizontal rules)
- Any semantic markers (callouts, notes, warnings, labels)

### 2. Map Markdown to Confluence Page Format

Use the mapping tables below to convert each Markdown element to its Confluence equivalent. Confluence Page Format uses HTML with specific CSS classes and data attributes:

#### Headings

| Markdown | Confluence |
|----------|-----------|
| `# Title` | `<h1 class="aui-page-header">` or `<h1 class="confluence-heading">` |
| `## Section` | `<h2 class="confluence-heading">` |
| `### Subsection` | `<h3 class="confluence-heading">` |
| `#### Sub-subsection` | `<h4 class="confluence-heading">` |

Include `id` attributes on headings for anchor references: `<h2 id="section-name" class="confluence-heading">Section Name</h2>`. Convert heading text to kebab-case for the ID.

#### Paragraphs and Text

- Wrap paragraphs in `<p class="text-parsed">` or plain `<p>` tags
- Apply inline formatting directly: `<strong>`, `<em>`, `<code>`, `<a href="...">`
- Preserve whitespace and line breaks within paragraphs

#### Lists

- Unordered lists: `<ul class="content-verbatim">` with `<li>` items
- Ordered lists: `<ol class="content-verbatim">` with `<li>` items
- Nested lists: nest `<ul>` or `<ol>` inside `<li>` elements
- Use `class="content-verbatim"` for list containers to preserve Confluence styling

#### Tables

- Table header: `<th class="confluenceTh">`
- Table cells: `<td class="confluenceTd">`
- Table wrapper: `<table class="confluenceTable">`
- Table body: `<tbody class="confluenceTdBody">`
- Table header row: `<thead class="confluenceThBody">`

Example:

```html
<table class="confluenceTable">
  <thead class="confluenceThBody">
    <tr>
      <th class="confluenceTh">Column 1</th>
      <th class="confluenceTh">Column 2</th>
    </tr>
  </thead>
  <tbody class="confluenceTdBody">
    <tr>
      <td class="confluenceTd">Row 1, Cell 1</td>
      <td class="confluenceTd">Row 1, Cell 2</td>
    </tr>
  </tbody>
</table>
```

#### Code Blocks

- Fenced code blocks: `<pre class="code"><code class="language-...">...</code></pre>`
- Inline code: `<code class="code">...</code>`
- Preserve language hints in the `code` class for syntax highlighting

### 3. Add Confluence-specific elements

#### Info Panels and Callouts

Use Confluence's panel macros for notes, warnings, tips, and important information:

```html
<div class="wrap">
  <div class="panel panelType-info">
    <p class="panelContent">This is an informational note.</p>
  </div>
</div>
```

Panel type variants:
- `panelType-info` — blue info panels
- `panelType-tip` — green tip panels
- `panelType-warning` — yellow warning panels
- `panelType-error` — red error panels
- `panelType-confluence` — default Confluence styling

#### Expand/Collapse Macros

For long documentation sections that benefit from collapsible content:

```html
<div class="expand">
  <div class="expand-control">Click to expand</div>
  <div class="expand-body">
    <p>Collapsible content goes here.</p>
  </div>
</div>
```

Use expand macros for:
- Detailed API reference sections
- Changelog entries
- Troubleshooting steps
- Any content that is secondary to the main flow

#### Anchors and Internal Links

Create anchor targets on headings and link to them:

```html
<!-- Anchor target on a heading -->
<h2 id="troubleshooting" class="confluence-heading">Troubleshooting</h2>

<!-- Link to the anchor -->
<a href="#troubleshooting">Go to Troubleshooting</a>
```

Convert all anchor IDs to kebab-case. Use anchors for:
- Table of contents generation
- Cross-references within the document
- Deep links to specific sections

#### Labels

Labels in Confluence are metadata, not inline markup. Note to the user:

> Labels are added through the Confluence UI via the "Labels" button at the bottom of the page editor. Common label patterns include: `documentation`, `api`, `guide`, `how-to`, and space-specific tags.

### 4. Structure the complete document

Assemble all converted elements into a single Confluence Page Format document:

1. Start with a page-level wrapper if producing a full page
2. Maintain heading hierarchy — do not skip heading levels
3. Place panels and callouts at appropriate semantic positions
4. Include anchor IDs on all headings that are referenced elsewhere
5. Wrap the output in appropriate Confluence page structure

For a complete page:

```html
<div class="wiki-content">
  <div class="index-section">
    <!-- Document content here -->
  </div>
</div>
```

### 5. Provide usage guidance

After generating the formatted output, include a guidance section that covers:

- **Where to paste the output** — in the Confluence page editor's "Insert more content" → "HTML" mode, or the source editor
- **How to add labels** — through the Confluence UI label button
- **How to set page properties** — title, space assignment, versioning notes
- **How to preview** — use Confluence's preview before publishing

## Pitfalls

- **Skipping heading levels** — going from H2 to H4 breaks the document outline. Maintain sequential heading hierarchy.
- **Inline HTML in panels** — panels should contain paragraph-level content, not block-level elements like other tables or code blocks. Nest complex content outside panels.
- **Forgetting anchor IDs** — if the document references sections by link, every referenced heading needs an `id` attribute.
- **Overusing panels** — too many panels make a page look cluttered. Reserve panels for content that is truly distinct from the main flow (warnings, tips, notes).
- **Hardcoding Confluence space URLs** — the skill formats content, not URLs. Space-specific URLs belong in the publishing step, not the formatting step.
- **Mixing Storage Format and Page Format** — Confluence Storage Format (XML) is a different format. This skill produces Page Format (HTML). Do not attempt to generate XML storage format output.

## Verification

After formatting, confirm:

- All Markdown headings map to Confluence heading classes with matching `id` attributes
- Tables use `confluenceTable`, `confluenceTh`, and `confluenceTd` classes
- Lists use `content-verbatim` class on container elements
- Code blocks use `code` class with language hints
- Panels use appropriate `panelType-` classes
- Internal links reference heading `id` attributes that actually exist in the document
- Heading hierarchy is sequential (no skipped levels)
- No upload mechanism, API calls, or publishing instructions are included

Quick checklist:

```
✓ Headings have id attributes and correct hierarchy
✓ Tables use Confluence table classes
✓ Lists have content-verbatim containers
✓ Code blocks have language hints
✓ Panels use appropriate panelType classes
✓ Internal links reference existing anchors
✓ No upload or publishing steps are included
```
