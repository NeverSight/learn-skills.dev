---
name: markdown-formatter
description: Format, validate, and optimize Markdown documents for consistency, readability, and professional presentation
---

# Markdown Formatter Skill

Create beautifully formatted Markdown documents that are consistent, readable, and professionally presented. This skill helps you maintain high-quality documentation standards.

## Purpose

This skill helps you:
- Format Markdown files for consistency
- Validate Markdown syntax
- Optimize for readability
- Generate table of contents
- Fix common formatting issues
- Enforce style guidelines
- Create reusable templates
- Convert between Markdown formats

## When to Use

Use this skill when you need to:
- Standardize Markdown formatting across projects
- Clean up and improve documentation
- Validate Markdown syntax before publishing
- Generate automated table of contents
- Create professional README files
- Format code examples consistently
- Apply style guides to documentation
- Convert between Markdown dialects

## Key Features

1. **Formatting** - Consistent styling for headers, lists, links
2. **Validation** - Check for syntax errors and issues
3. **TOC Generation** - Automatic table of contents
4. **Linting** - Enforce style rules and best practices
5. **Conversion** - Convert to/from HTML, PDF, and other formats
6. **Templates** - Ready-to-use document templates
7. **Batch Processing** - Format multiple files at once
8. **Custom Rules** - Define project-specific formatting rules

## Instructions

When using this skill:

1. **Provide Content** - Share raw Markdown or file path
2. **Specify Style** - Choose formatting style or guidelines
3. **Set Options** - Configure TOC, links, code formatting
4. **Format** - Apply consistent formatting
5. **Validate** - Check for errors and issues
6. **Review** - Verify output meets requirements
7. **Deploy** - Use formatted Markdown in your project

## Guidelines

- **Consistency First** - Use the same style throughout documents
- **Readability Matters** - Format for easy scanning and reading
- **Semantic HTML** - Use proper Markdown elements for meaning
- **Accessible** - Ensure documents work for all readers
- **Version Control** - Keep Markdown in Git for tracking changes
- **Link Validation** - Check that all links are valid
- **Code Quality** - Format code blocks properly

## Examples

### Example 1: Formatting a README

**Input (Raw Markdown):**
```markdown
# My Project
this is a great project
## Installation
pip install myproject
## Usage
use it like this
```python
import myproject
```
## Features
- fast
- reliable
- easy
```

**Output (Formatted):**
```markdown
# My Project

This is a great project.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Installation

```bash
pip install myproject
```

## Usage

Use it like this:

```python
import myproject
```

## Features

- Fast and performant
- Reliable and stable
- Easy to use and integrate
```

### Example 2: Generate Table of Contents

**Command:**
```
Format this document and generate a table of contents
```

**Generated TOC:**
```markdown
## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
3. [Usage Examples](#usage-examples)
   - [Basic Usage](#basic-usage)
   - [Advanced Features](#advanced-features)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)
6. [Contributing](#contributing)
7. [License](#license)
```

## Formatting Rules

### Headers
```markdown
# H1: Document Title
## H2: Main Sections
### H3: Subsections
#### H4: Sub-subsections
```

### Lists
```markdown
### Unordered Lists
- Item 1
- Item 2
  - Nested item
  - Another nested

### Ordered Lists
1. First step
2. Second step
3. Third step
```

### Code Blocks
````markdown
```language
code goes here
```

```python
def hello():
    print("Hello, World!")
```

```bash
echo "This is a bash command"
```
````

### Links and Images
```markdown
[Link text](https://example.com)
[Reference link][1]

![Alt text](image.png)
![Reference image][logo]

[1]: https://example.com
[logo]: /path/to/logo.png
```

### Tables
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |
```

## Style Guidelines

### Capitalization
- Capitalize headings consistently
- Use sentence case for body text
- ALL CAPS only for acronyms or emphasis

### Spacing
- One blank line between sections
- Blank line before and after code blocks
- Consistent indentation (2 or 4 spaces)

### Emphasis
```markdown
*italic* or _italic_
**bold** or __bold__
***bold italic***
~~strikethrough~~
`inline code`
```

## Common Issues Fixed

| Issue | Fix |
|-------|-----|
| Inconsistent heading levels | Normalize to proper hierarchy |
| Broken links | Update or remove broken links |
| Missing blank lines | Add proper spacing |
| Misaligned tables | Reformat for readability |
| Inconsistent code block language tags | Add or correct language identifiers |
| Unordered links | Organize using reference-style links |
| Missing alt text | Add meaningful alt text to images |

## Validation Checks

The formatter validates:
- [ ] Proper heading hierarchy
- [ ] Valid link formatting
- [ ] Balanced bracket and parentheses
- [ ] Proper code block fencing
- [ ] Table structure and alignment
- [ ] Image path validity
- [ ] Duplicate heading IDs

## Output Formats

This skill can export to:
- **Markdown** (.md) - Standard format
- **HTML** (.html) - Web-ready
- **PDF** (.pdf) - Printable documents
- **HTML Slides** - Presentation format
- **EPUB** (.epub) - E-book format

## Markdown Flavors Supported

- CommonMark (standard)
- GitHub Flavored Markdown (GFM)
- MultiMarkdown
- Pandoc Markdown
- Custom dialects

## Related Resources

- [Markdown Syntax Guide](./references/markdown-guide.md)
- [Style Guidelines](./references/style-guide.md)
- [Formatting Templates](./assets/templates/)
- [Validation Scripts](./scripts/)
- [Example Documents](./assets/examples/)

## Best Practices

1. **Use descriptive headers** - Make document structure obvious
2. **Link liberally** - Connect related sections and external resources
3. **Format code properly** - Always use code blocks with language tags
4. **Add images thoughtfully** - Illustrate complex concepts
5. **Create tables for data** - Make comparisons clear
6. **Write for scanners** - Many users skim, not read
7. **Keep it DRY** - Avoid repeating information

## Support

For Markdown formatting help:
1. Review the examples above
2. Check the syntax guide in `references/`
3. Use validation scripts in `scripts/`
4. Browse templates in `assets/templates/`
