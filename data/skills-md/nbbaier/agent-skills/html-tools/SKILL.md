---
name: html-tools
description: Build single-file HTML tools — self-contained HTML+JS+CSS applications that solve a specific problem without a build step. Use this skill whenever the user asks to build a utility, converter, viewer, debugger, or any small interactive web tool. Also trigger when the user says "build me a tool that...", "make a quick app for...", "I need a single-file HTML page that...", or wants to create something that could be hosted as a static file. This skill is specifically for practical, utility-focused tools (not landing pages, portfolios, or marketing sites — use frontend-design for those).
---

# HTML Tools

Build single-file HTML applications that combine HTML, JavaScript, and CSS into one portable file. These tools solve specific problems, load instantly, require no build step, and can be hosted anywhere as static files.

This skill codifies patterns from building 150+ such tools. The goal is always: one file, no build step, no framework overhead, maximum utility.

## When to Use This Skill

Use this when the user wants a **utility or tool** — something interactive that transforms, displays, debugs, converts, or processes data. Common types:

- Converters (JSON↔YAML, Markdown→HTML, CSV→table, format transformers)
- Viewers/Inspectors (clipboard contents, EXIF data, keyboard events, CORS checks)
- Processors (image croppers, OCR, diff generators, text transformers)
- API-powered tools (calling CORS-enabled APIs like GitHub, PyPI, Bluesky, iNaturalist)
- LLM-powered tools (calling OpenAI/Anthropic/Gemini APIs directly via CORS)
- Developer utilities (regex testers, color pickers, encoding tools, hash generators)

If the user wants a polished marketing page or portfolio, use the `frontend-design` skill instead.

## Core Principles

1. **Single file**: All HTML, JS, and CSS in one `.html` file. Trivially copyable, hostable, and shareable.

2. **No React, no build step**: Avoid React (JSX requires transpilation). Use vanilla JS or lightweight CDN libraries. If the user specifically requests React, explain the tradeoff and offer both options.

3. **CDN dependencies only**: Load from cdnjs.cloudflare.com or cdn.jsdelivr.net with pinned versions. Fewer dependencies is better, but don't reinvent well-solved problems.

4. **Keep it small**: A few hundred lines is ideal. At this size, the code is easy to understand, easy to rewrite, and easy to hand to another LLM for modification.

5. **Copy-paste as primary I/O**: Many great tools accept pasted input, transform it, and offer a "Copy to clipboard" button for the output. Default to this interaction pattern unless the problem calls for something else.

## File Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Tool Name]</title>
    <!-- CDN dependencies with pinned versions -->
    <style>
        /* All CSS inline */
    </style>
</head>
<body>
    <!-- Tool UI -->
    <script>
        /* All JS inline */
    </script>
</body>
</html>
```

Always include the viewport meta tag for mobile. Use semantic HTML where practical.

## Pattern Selection Guide

When building a tool, consider which patterns from `references/patterns.md` apply. Here is a quick decision framework:

**How does data get in?**
- User types/pastes text → paste input pattern
- User has a file → file input pattern (no server needed, JS reads it directly)
- Tool is configured by a link → URL parameter pattern
- User drags something in → drag-and-drop pattern

**How does data get out?**
- User needs text output → copy-to-clipboard button (always include this)
- User needs a file → downloadable file via Blob URL
- User needs a visual → render directly in the page

**Does the tool need to remember anything?**
- Small state, shareable → persist in URL hash/query params
- Larger state or secrets (API keys) → localStorage
- Nothing → keep it stateless

**Does the tool need external data?**
- Public API with CORS → fetch directly from the browser
- LLM API → store user's API key in localStorage, call API via CORS
- No CORS on the API → explain limitation, suggest a proxy or different approach

**Does the tool need heavy computation?**
- Python logic → Pyodide (Python compiled to WebAssembly, loads from CDN)
- Other compiled tools → check if a WebAssembly port exists (Tesseract.js, FFmpeg.wasm, etc.)
- Pure JS is fine → just use it

Read `references/patterns.md` for detailed code examples and implementation guidance for each pattern.

## Implementation Checklist

When building an HTML tool, verify:

- [ ] Single `.html` file with inline CSS and JS
- [ ] No build step required
- [ ] Dependencies loaded from CDN with pinned versions
- [ ] Mobile-friendly (viewport meta tag, responsive layout)
- [ ] "Copy to clipboard" button if tool produces text output
- [ ] Clear, descriptive `<title>` tag
- [ ] Error handling for common failure modes (bad input, network errors, missing APIs)
- [ ] Loading indicators for async operations
- [ ] Clean, functional UI — not fancy, but usable and clear

## Style Notes

HTML tools are utilities, not showcases. Prioritize clarity and function over visual flair. A clean sans-serif font, sensible spacing, and clear visual hierarchy are enough. Don't over-design.

That said, the tool should look intentional, not broken. Use a system font stack, consistent padding, and visible interactive affordances (buttons look like buttons, inputs look like inputs).

## Remixing and Composition

When the user has an existing HTML tool and wants to extend it or build something similar, read the existing tool's source first. Working tools are the best documentation for browser API patterns, library usage, and interaction flows. Use them as a starting point rather than building from scratch.
