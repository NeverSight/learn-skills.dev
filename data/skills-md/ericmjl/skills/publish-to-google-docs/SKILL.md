---
name: publish-to-google-docs
description: Quickly publish markdown notes to styled Google Docs using pandoc and a Word template. Use when creating Google Docs from markdown, applying branding to documents, or pushing content to Drive for sharing.
license: MIT
---

# Publish Markdown to Google Docs

Quickly publish markdown notes to styled Google Docs using pandoc and a Word template.

## When to use

- User wants to publish a markdown note to Google Docs
- User says "publish to Google Docs", "create a Google Doc from markdown", or "push this to Drive"
- User wants to apply consistent branding/styling to documents before sharing

## Prerequisites

1. **pandoc** - Must be installed (see self-healing below)
2. A Word template (.docx) with desired styles
3. OAuth credentials for Google Drive (one-time setup)

## Self-healing: Installing pandoc

If pandoc is not installed, ask the user how they would like to install it:

**Preferred option (pixi):**

```bash
pixi global install pandoc
```

**Alternative options by platform:**

| Platform | Command |
|----------|---------|
| macOS (Homebrew) | `brew install pandoc` |
| macOS (MacPorts) | `port install pandoc` |
| Windows (Chocolatey) | `choco install pandoc` |
| Windows (winget) | `winget install --source winget --exact --id JohnMacFarlane.Pandoc` |
| Linux (Conda) | `conda install -c conda-forge pandoc` |
| Any (download) | Download from <https://github.com/jgm/pandoc/releases/latest> |

Use the `question` tool to present these options if pandoc is missing.

## Workflow

### Step 1: Check pandoc availability

```bash
which pandoc && pandoc --version
```

If not found, prompt user to install (see self-healing above).

### Step 2: Convert markdown to docx with pandoc

```bash
pandoc INPUT.md --from markdown --to docx --reference-doc=TEMPLATE.docx --output=OUTPUT.docx
```

The `--reference-doc` flag applies the template's styles (fonts, headings, margins) to the output.

### Step 3: Upload to Google Drive

```bash
uv run scripts/upload_to_drive.py --input OUTPUT.docx --title "Document Title"
```

Returns a shareable Google Docs link.

## Example

```bash
# Convert and upload
pandoc "proposal.md" --from markdown --to docx --reference-doc="template.docx" --output="proposal.docx"
uv run scripts/upload_to_drive.py --input "proposal.docx" --title "My Proposal"
```

## Scripts

### upload_to_drive.py

Uploads a docx file to Google Drive using OAuth2 user authentication.

**Usage:**

```bash
uv run scripts/upload_to_drive.py --input /path/to/file.docx --title "Document Title"
```

**Setup (one-time):**

1. Go to https://console.cloud.google.com/apis/credentials
2. Create an OAuth 2.0 Client ID (Desktop app)
3. Set environment variables:

```bash
export GOOGLE_CLIENT_ID='your-client-id.apps.googleusercontent.com'
export GOOGLE_CLIENT_SECRET='your-client-secret'
```

**Features:**

- Opens browser for Google login on first run
- Saves credentials locally for future use
- Use `--logout` to remove saved credentials
- Use `--no-share` to keep document private

## Template Style Requirements

For best results, your template should have these styles defined:

| Style | Usage |
|-------|-------|
| Title | Document title (# heading) |
| Heading 1 | Major sections (## heading) |
| Heading 2 | Subsections (### heading) |
| Heading 3 | Sub-subsections (#### heading) |
| Normal | Body paragraphs |

## Notes

- Pandoc handles all markdown correctly: lists, bold, italic, tables, code blocks, links
- The template's fonts, colors, and margins are preserved via `--reference-doc`
- Images from the template are not copied - this only applies styles
