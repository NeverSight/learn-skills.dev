---
name: md2pdf2
description: >
  Generate beautiful, professionally styled PDF documents from Markdown content using customizable
  Handlebars (HBS) templates and the md2pdf2 CLI tool. Use this skill whenever the user wants to
  convert markdown to PDF, create a styled PDF report/document from text or markdown, generate a
  PDF with a custom template or theme, produce professional documents (resumes, reports,
  newsletters, invoices, briefs) as PDFs from markdown input. Trigger this skill even when the
  user just says "create a PDF", "export to PDF", "make a nice PDF", or provides markdown and
  wants a polished document output. Prefer this skill over the plain pdf skill when template
  customization or markdown-to-PDF conversion is the core need.
---

# MD2PDF2 Skill

Convert Markdown to beautiful, professionally styled PDFs using the `md2pdf2` CLI tool with Handlebars templates.

## Overview

`md2pdf2` is a Node.js CLI tool that converts Markdown → HTML (via HBS template) → PDF using Puppeteer. It supports:
- Custom `.hbs` Handlebars templates with `{{{content}}}` for markdown body
- CSS styling (inline or external)
- PDF format options (A4, Letter, etc.)
- Frontmatter metadata (title, author, date, etc.)
- Built-in templates: `default`, `modern`, `minimal`, `newsletter`, `resume`

---

## Workflow

### Step 1 — Understand the request

Determine:
1. **Content**: Does the user have markdown, or should you generate it from their description?
2. **Template/Style**: Which built-in template fits, or should you create a custom `.hbs`?
3. **Output filename**: Default to `output.pdf` unless specified.

### Step 2 — Set up the environment

```bash
# Install md2pdf2 globally (or use npx)
npm install -g md2pdf2 2>/dev/null || true
# Verify
which md2pdf2 || npx md2pdf2 --version
```

If global install fails (permissions), use `npx md2pdf2` in all commands.

### Step 3 — Prepare files in /home/claude/

**a) Write markdown content** to `/home/claude/input.md`

Always include YAML frontmatter for metadata:
```markdown
---
title: Document Title
author: Author Name
date: 2024-01-01
---

# Your Content Here
```

**b) Create or select a template**

For custom templates, write a `.hbs` file. See the [Template Guide](#template-guide) below.

For built-in templates, pass `--template <name>` (default, modern, minimal, newsletter, resume).

**c) Write config if needed** to `/home/claude/md2pdf2.config.js`:
```js
export default {
  template: './custom.hbs',   // path to HBS template (optional)
  pdfOptions: {
    format: 'A4',             // 'A4' | 'Letter' | 'Legal'
    margin: { top: '2cm', right: '2cm', bottom: '2cm', left: '2cm' }
  }
}
```

### Step 4 — Run the conversion

```bash
cd /home/claude && npx md2pdf2 convert input.md -o /mnt/user-data/outputs/output.pdf
# With custom template:
npx md2pdf2 convert input.md --template custom.hbs -o /mnt/user-data/outputs/output.pdf
# With built-in template name:
npx md2pdf2 convert input.md --template modern -o /mnt/user-data/outputs/output.pdf
```

### Step 5 — Present the file

Use `present_files` with the output path.

---

## Template Guide

### Minimal valid HBS template

```hbs
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Georgia, serif; max-width: 800px; margin: 0 auto; padding: 40px; }
    h1 { color: #2c3e50; }
  </style>
</head>
<body>
  <h1>{{title}}</h1>
  <p>{{author}} — {{date}}</p>
  {{{content}}}
</body>
</html>
```

**Key variables available in templates:**
- `{{{content}}}` — rendered HTML from markdown (use triple braces — no escaping)
- `{{title}}` — from frontmatter
- `{{author}}` — from frontmatter
- `{{date}}` — from frontmatter
- `{{> partialName}}` — include a partial from `templates/parts/`

**Built-in Handlebars helpers:**
- `{{currentDate}}` — returns current date (e.g., "January 15, 2024")
- `{{slice str start end}}` — slice a string (e.g., `{{slice title 0 1}}` for first character)
- `{{hasPartial "name"}}` — check if a partial exists

### Beautiful template recipes

See `templates/` folder in this skill for ready-to-use templates:
- `professional-report.hbs` — corporate report with cover page
- `resume.hbs` — clean two-column CV layout
- `newsletter.hbs` — styled newsletter with header/footer

---

## Built-in Templates Quick Reference

| Template | Best For |
|---|---|
| `default` | General purpose, clean |
| `modern` | Bold, colorful, Inter font |
| `minimal` | Simple serif, academic |
| `newsletter` | Email-style newsletter |
| `resume` | CV/resume formatting |

---

## Troubleshooting

**`md2pdf2: command not found`** → Use `npx md2pdf2` instead.

**Puppeteer/Chrome errors in sandbox** → Add `--no-sandbox` flag if supported, or check if headless Chrome is available: `google-chrome --version || chromium --version`.

**Template not found** → Ensure the `.hbs` file path is relative to the working directory where you run the command.

**Styles not applying** → Check CSS is inside `<style>` tags in the HBS template, not external (external CSS won't load in Puppeteer's sandboxed env without explicit file:// paths).

---

## Example: Full workflow

```bash
# 1. Write content
cat > /home/claude/input.md << 'EOF'
---
title: Q4 Sales Report
author: Finance Team
date: 2024-12-31
---

## Executive Summary
Revenue grew 23% YoY...

## Key Metrics
| Metric | Value |
|--------|-------|
| Revenue | $4.2M |
| Growth | 23% |
EOF

# 2. Convert with modern template
cd /home/claude && npx md2pdf2 convert input.md --template modern -o /mnt/user-data/outputs/q4-report.pdf

# 3. Verify
ls -la /mnt/user-data/outputs/q4-report.pdf
```
