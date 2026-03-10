---
name: cover-image
description: "Generate editorial cover images from article context. Use when user wants a cover image, hero image, or editorial illustration for an article or blog post. Not for table/diagram images (use table-image)."
tools: Bash, Read
compatibility: "Requires GEMINI_API_KEY or GOOGLE_API_KEY in environment. Uses ~/.claude/skills/_generate_image.py"
---

# ABOUTME: Generate editorial cover images from article context using Gemini image generation
# ABOUTME: Distills articles into hand-drawn sketch visual metaphors with ink stroke style

# Cover Image Skill

Generate editorial cover images using Gemini's image generation. Distill article content into a visual metaphor rendered as a hand-drawn sketch.

## Workflow

### 1. Understand the Article

Read the article/context provided by the user. Identify the core concept, tension, or insight that could become a visual metaphor.

### 2. Craft the Prompt

Build a prompt using this structure:

```
Black and white hand-drawn sketch, loose ink strokes, technical architectural drawing style.
[visual metaphor distilled from article context]. High contrast, minimalist, white background,
editorial tech illustration. --ar 16:9
```

**Visual metaphor guidelines:**
- Translate abstract concepts into concrete imagery (e.g., "microservices" -> "separate buildings connected by bridges")
- Prefer architectural/technical metaphors over literal depictions
- Keep the scene simple: one strong central image, not a collage
- Avoid text, labels, or UI elements in the image

### 3. Show Prompt for Approval

Present the crafted prompt to the user. Wait for confirmation before generating.

### 4. Generate

```bash
uv run ~/.claude/skills/_generate_image.py "<approved prompt>" --ar 16:9 -o cover.png
```

### 5. Report

Report the saved file path and suggest reviewing the image.

## Example

**Article about**: "Why we migrated from monolith to microservices"

**Prompt**:
```
Black and white hand-drawn sketch, loose ink strokes, technical architectural drawing style.
A massive ancient stone building cracking apart, its fragments floating and reorganizing into
a constellation of small interconnected structures, linked by thin precise lines.
High contrast, minimalist, white background, editorial tech illustration. --ar 16:9
```

## Notes

- Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` in environment
- Default output: `cover.png` in current directory
- Default aspect ratio: 16:9 (landscape, editorial)
- Uses shared script: `~/.claude/skills/_generate_image.py`
