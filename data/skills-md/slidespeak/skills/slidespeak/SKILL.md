---
name: slidespeak
description: Generate, edit, and manage PowerPoint presentations via the SlideSpeak API. Use this skill when users want to create presentations from text or documents, edit existing presentations, or work with presentation templates.
allowed-tools: Bash Read Write
metadata:
  {
    "openclaw":
      {
        "emoji": "🦜",
        "homepage": "https://slidespeak.co",
        "requires": { "env": [ "SLIDESPEAK_API_KEY" ] },
        "primaryEnv": "SLIDESPEAK_API_KEY",
      },
  }
---

# SlideSpeak Presentation Skill

This skill enables you to create and edit PowerPoint presentations using the SlideSpeak API.

## IMPORTANT: Timing Behavior

**Presentation generation takes 30-60 seconds.**

### Option 1: Wait for completion (default)
Run the command and wait. The script polls internally until complete:
```bash
node scripts/slidespeak.mjs generate --text "Topic"
```
- Blocks until the task finishes (typically 30-60 seconds)
- Returns the complete result with download URL

### Option 2: Return immediately with `--no-wait`
If you cannot wait for the command to complete, use `--no-wait`:
```bash
node scripts/slidespeak.mjs generate --text "Topic" --no-wait
```
Returns immediately with:
```json
{
  "success": true,
  "data": {
    "task_id": "abc123...",
    "message": "Task started. Check status with: node scripts/slidespeak.mjs status abc123..."
  }
}
```

Then poll the status until complete:
```bash
node scripts/slidespeak.mjs status <task_id>
```
When `task_status` is `SUCCESS`, use the `request_id` to download.

### Timeout behavior
If the script times out while waiting, it returns the task_id so you can continue polling:
```json
{
  "success": true,
  "data": {
    "complete": false,
    "task_id": "abc123...",
    "task_status": "STARTED",
    "message": "Task still processing. Check status with: node scripts/slidespeak.mjs status abc123..."
  }
}
```

## Setup

The `SLIDESPEAK_API_KEY` environment variable must be set. Get your API key from https://app.slidespeak.co/settings/developer

## Quick Reference

All commands use the helper script at `scripts/slidespeak.mjs`. The script handles API authentication and waits for async tasks to complete automatically (no manual polling needed).

### Generate a Presentation from Text

```bash
node scripts/slidespeak.mjs generate --text "Your topic or content" --length 6
```

Options:
- `--text` (required): Topic or content for the presentation
- `--length`: Number of slides (default: 10)
- `--template`: Template name or ID (default: "default")
- `--language`: Output language (default: "ORIGINAL")
- `--tone`: casual, professional, funny, educational, sales_pitch
- `--verbosity`: concise, standard, text-heavy
- `--no-images`: Disable stock image fetching
- `--no-cover`: Exclude cover slide
- `--no-toc`: Exclude table of contents

### Generate from an Uploaded Document

First upload the document, then generate:

```bash
# Upload a document (PDF, DOCX, PPTX, etc.)
node scripts/slidespeak.mjs upload /path/to/document.pdf

# Use the returned document_uuid to generate
node scripts/slidespeak.mjs generate --document <document_uuid> --length 10
```

Supported formats: `.pdf`, `.docx`, `.doc`, `.pptx`, `.ppt`, `.xlsx`, `.txt`, `.md`

### List Available Templates

```bash
# Default templates
node scripts/slidespeak.mjs templates

# Branded templates (if configured)
node scripts/slidespeak.mjs templates --branded
```

### Download a Presentation

After generation completes, use the `request_id` to download:

```bash
node scripts/slidespeak.mjs download <request_id>
```

Returns a JSON object with a short-lived download URL.

### Edit an Existing Presentation

Edit slides in an existing presentation:

```bash
# Insert a new slide at position 2
node scripts/slidespeak.mjs edit-slide \
  --presentation-id <id> \
  --type INSERT \
  --position 2 \
  --prompt "Content about market analysis"

# Regenerate slide at position 3
node scripts/slidespeak.mjs edit-slide \
  --presentation-id <id> \
  --type REGENERATE \
  --position 3 \
  --prompt "Updated content for this slide"

# Remove slide at position 4
node scripts/slidespeak.mjs edit-slide \
  --presentation-id <id> \
  --type REMOVE \
  --position 4
```

Edit types:
- `INSERT`: Add a new slide at the position
- `REGENERATE`: Replace existing slide content
- `REMOVE`: Delete the slide (no prompt needed)

### Check Task Status

For debugging or manual polling:

```bash
node scripts/slidespeak.mjs status <task_id>
```

### Get Account Info

```bash
node scripts/slidespeak.mjs me
```

## Slide-by-Slide Generation

For precise control over each slide, use the slide-by-slide endpoint. See `references/API.md` for the full schema.

```bash
node scripts/slidespeak.mjs generate-slides --config slides.json
```

Where `slides.json` contains:
```json
{
  "slides": [
    {"title": "Introduction", "layout": "title", "content": "Welcome message"},
    {"title": "Key Points", "layout": "bullets", "item_amount": 4, "content": "Main discussion points"}
  ],
  "template": "default"
}
```

## Webhooks

Subscribe to receive notifications when tasks complete:

```bash
# Subscribe
node scripts/slidespeak.mjs webhook-subscribe --url "https://your-webhook.com/endpoint"

# Unsubscribe
node scripts/slidespeak.mjs webhook-unsubscribe --url "https://your-webhook.com/endpoint"
```

## Error Handling

The script outputs JSON with either:
- Success: `{"success": true, "data": {...}}`
- Error: `{"success": false, "error": "message"}`

## Common Workflows

### Create a presentation about a topic
```bash
node scripts/slidespeak.mjs generate --text "Introduction to Machine Learning" --length 8 --tone educational
```

### Create a presentation from a PDF report
```bash
# Upload the PDF
RESULT=$(node scripts/slidespeak.mjs upload report.pdf)
DOC_ID=$(echo $RESULT | jq -r '.data.document_uuid')

# Generate presentation
node scripts/slidespeak.mjs generate --document "$DOC_ID" --length 12
```

### Edit a presentation to add a new slide
```bash
node scripts/slidespeak.mjs edit-slide \
  --presentation-id "abc123" \
  --type INSERT \
  --position 5 \
  --prompt "Add a slide about quarterly revenue growth with charts"
```

## Additional Resources

For detailed API documentation including all parameters, layout types, and constraints, read `references/API.md`.