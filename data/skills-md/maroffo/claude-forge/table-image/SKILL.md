---
name: table-image
description: "Render markdown tables as hand-drawn sketch images. Use when user wants a table rendered as an image, visual table, or diagram illustration."
tools: Bash, Read
compatibility: "Requires GEMINI_API_KEY or GOOGLE_API_KEY in environment. Uses ~/.claude/skills/_generate_image.py"
---

# ABOUTME: Render markdown tables and diagrams as hand-drawn sketch images via Gemini
# ABOUTME: Converts tabular data into ink-style editorial illustrations with wide aspect ratio

# Table Image Skill

Render markdown tables and diagrams as hand-drawn sketch images using Gemini's image generation.

## Workflow

### 1. Receive Table Content

Get the markdown table from the user. The table should be in standard markdown format.

### 2. Construct the Prompt

Build a prompt using this structure:

```
Black and white hand-drawn sketch, loose ink strokes. A clean technical table drawn on
white paper. Minimalist, high contrast, editorial tech illustration. Compact layout,
minimal margins, cropped tightly to the table edges, the table fills the frame. --ar 24:9

[paste the full markdown table here]
```

### 3. Generate

```bash
uv run ~/.claude/skills/_generate_image.py "<constructed prompt>" --ar 24:9 -o table.png
```

### 4. Report

Report the saved file path and suggest reviewing the image.

## Example

**Input table**:
```markdown
| Feature | Go | Python | Ruby |
|---------|-----|--------|------|
| Concurrency | goroutines | asyncio | threads |
| Typing | static | dynamic | dynamic |
| Speed | fast | moderate | moderate |
```

**Prompt**:
```
Black and white hand-drawn sketch, loose ink strokes. A clean technical table drawn on
white paper. Minimalist, high contrast, editorial tech illustration. Compact layout,
minimal margins, cropped tightly to the table edges, the table fills the frame. --ar 24:9

| Feature | Go | Python | Ruby |
|---------|-----|--------|------|
| Concurrency | goroutines | asyncio | threads |
| Typing | static | dynamic | dynamic |
| Speed | fast | moderate | moderate |
```

## Notes

- Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` in environment
- Default output: `table.png` in current directory
- Default aspect ratio: 24:9 (wide, fills frame with table)
- Uses shared script: `~/.claude/skills/_generate_image.py`
- For complex tables, results improve when the table has clear headers and consistent column widths
