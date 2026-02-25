---
name: markdown-to-pdf
description: Create a PDF from a local Markdown file using a local Python script (no remote services).
---

# Markdown to PDF

- Use this skill when a user asks to convert a Markdown file to PDF.
- Use the script at .github/skills/markdown-to-pdf/scripts/md_to_pdf.py for the conversion.
- The default body font size is 11pt in the script; adjust the CSS if needed.
- before installing dependencies ask if there is a proxy configuration required, if so apply proxy before installing dependencies.
- Install dependencies if missing: `python3 -m pip install markdown weasyprint`.
- Run the script with input and output paths:
  - `python3 .github/skills/markdown-to-pdf/scripts/md_to_pdf.py input.md output.pdf`
- Keep output simple and close to default Markdown rendering.
