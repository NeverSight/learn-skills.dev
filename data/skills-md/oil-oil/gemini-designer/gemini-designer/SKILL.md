---
name: gemini-designer
description: Delegate design tasks to Gemini (gemini-2.5-flash-preview) via aicodemirror API. Use when you need UI/web design (single-page HTML), SVG icons/illustrations, color palettes, typography suggestions, layout advice, or any visual design reference. Gemini acts as your designer friend — ask it to create HTML page mockups, design SVG icons, suggest design systems, or give design feedback. Triggers on design-related requests like "design a page", "create an icon", "suggest colors", "make a logo", "UI mockup", "design reference".
---

# Gemini Designer — Your Design Partner

Delegate design tasks to Gemini via aicodemirror API. Gemini creates HTML page designs, SVG icons, and provides design advice.

## Critical rules

- ONLY interact with Gemini through the bundled shell script. NEVER call the API directly.
- Run the script ONCE per task. Read the output file and proceed.
- The script requires a Gemini API key. It checks (in order): `GEMINI_API_KEY` env var, `.env.local` in current/parent dirs, `~/.config/gemini-designer/api_key` file.

## How to call the script

The script path is:

```
~/.claude/skills/gemini-designer/scripts/ask_gemini.sh
```

### HTML page design

```bash
~/.claude/skills/gemini-designer/scripts/ask_gemini.sh "Design a modern landing page for a SaaS product called FlowSync" --html
```

### SVG icon

```bash
~/.claude/skills/gemini-designer/scripts/ask_gemini.sh "Create a minimal settings gear icon, 24x24, stroke style" --svg
```

### Design advice (text)

```bash
~/.claude/skills/gemini-designer/scripts/ask_gemini.sh "Suggest a color palette and typography for a developer blog"
```

### Custom output path (auto-infers type from extension)

```bash
~/.claude/skills/gemini-designer/scripts/ask_gemini.sh "Design a pricing card component" \
  -o ./designs/pricing-card.html
```

The script prints on success:

```
output_path=<path to output file>
```

Read the file at `output_path` to get Gemini's response.

## Output types

- `html` — Self-contained HTML file with inline CSS. Ready to open in browser. Use `--html` shorthand or `--output-type html`.
- `svg` — Clean SVG code. Can be saved directly or embedded in HTML/React. Use `--svg` shorthand or `--output-type svg`.
- `text` (default) — Design advice in markdown: color palettes, typography, layout suggestions.

If you pass `-o` with a `.html` or `.svg` extension and don't specify an output type, the type is auto-inferred from the file extension.

## When to use

- Need a visual reference or HTML mockup for a UI component or page
- Need SVG icons or simple illustrations
- Need color palette, typography, or layout suggestions
- Need design feedback or critique on an existing design
- Want a quick single-page HTML prototype to show a concept

## Workflow

1. Only describe what the page/component is for and the core content — do NOT add your own design opinions (colors, fonts, layout style, etc.) unless the user explicitly specified them.
2. Run the script with the appropriate output type flag (`--html`, `--svg`, or default text).
3. Read the output file.
4. For HTML/SVG: save to the project and iterate if needed.
5. For text advice: apply the suggestions to your implementation.

## Tips

- Keep the task prompt short and focused on what it is, not how it should look.
- If the user didn't specify a style/color/font, don't invent one — let Gemini decide.
- Only pass explicit user preferences (e.g. "dark mode", "use blue") when the user actually said so.
- Chinese prompts work well — Gemini responds in the same language.
