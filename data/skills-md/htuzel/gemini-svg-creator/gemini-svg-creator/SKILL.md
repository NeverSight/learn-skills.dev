---
name: "gemini-svg-creator"
description: "Create professional SVG graphics powered by Gemini 3.1 Pro via the Gemini MCP server. Generates logos, icons, illustrations, infographics, patterns, animated SVGs, and UI elements with a dual-model refinement loop (Claude orchestrates + Gemini generates). Gemini 3.1 Pro has SOTA animated SVG capabilities and advanced reasoning. Use this skill when the user asks to: create an SVG, design a logo, make an icon, draw an illustration, create an infographic, design a pattern, make an animated SVG, generate vector graphics, create SVG art, or any request involving SVG creation or generation. Also triggers on: 'generate SVG', 'draw me', 'design graphic', 'create vector', 'SVG illustration', 'SVG icon', 'SVG animation', 'create badge', 'design emblem', 'make a diagram'."
compatibility: "Requires @rlabs-inc/gemini-mcp MCP server with a Gemini API key. Recommended: set GEMINI_PRO_MODEL=gemini-3.1-pro-preview in your MCP server env for best SVG quality."
metadata:
  version: "1.0.0"
  mcp_server: "@rlabs-inc/gemini-mcp"
  recommended_model: "gemini-3.1-pro-preview"
---

# Gemini SVG Creator

Generate high-quality SVG graphics by orchestrating **Gemini 3.1 Pro** via `mcp__gemini__gemini-query`. Claude handles prompt engineering, quality analysis, and optimization; Gemini 3.1 Pro handles SVG generation with its SOTA animated SVG and reasoning capabilities.

## Prerequisites

This skill requires the `@rlabs-inc/gemini-mcp` MCP server. On first use, verify setup:

1. **Check MCP server is available**: Try calling `mcp__gemini__gemini-query`. If it fails, tell the user to add the Gemini MCP server:
   ```
   claude mcp add -e GEMINI_API_KEY=<your-key> -e GEMINI_PRO_MODEL=gemini-3.1-pro-preview gemini -- npx -y @rlabs-inc/gemini-mcp
   ```
2. **Recommend Gemini 3.1 Pro**: If the MCP server works but uses an older model, suggest adding `GEMINI_PRO_MODEL=gemini-3.1-pro-preview` to the MCP server env for best SVG quality. The user can update their `.claude.json` or run `claude mcp remove gemini` then re-add with the env variable above.
3. **API key**: Requires a Google AI Studio API key (`GEMINI_API_KEY`). Get one free at https://aistudio.google.com/apikey

## Model Notes — Gemini 3.1 Pro

- **Model ID**: `gemini-3.1-pro-preview` (configured via `GEMINI_PRO_MODEL` env)
- **Thinking levels**: `low`, `medium`, `high` (default). Use `medium` for simple SVGs, `high` for complex/animated
- **Strengths**: Animated SVG generation, anatomically accurate illustrations, semantic SVG comments, complex scene composition, CSS animation with proper keyframes
- **Context**: 1M input tokens, 64K output tokens
- **Known quirk**: May have high latency under load. If timeout occurs, retry once
- **Temperature**: Keep default (1.0) — lower values degrade reasoning quality

## Workflow

```
1. Understand request → Determine SVG category + complexity
2. Build prompt → Load category template from references/prompt-templates.md
3. Generate → Call Gemini 3.1 Pro with crafted prompt (thinkingLevel by complexity)
4. Analyze → Claude reviews SVG for issues
5. Refine → Send fix prompt back to Gemini (up to 2 rounds)
6. Optimize → Claude cleans up final SVG (see references/svg-optimization.md)
7. Save → Write .svg file(s) and present to user
```

## Step 1: Understand & Classify

Determine the SVG category and complexity:

| Category | Triggers | Complexity |
|----------|----------|------------|
| **logo** | logo, brand, wordmark, lettermark, emblem, badge | medium |
| **icon** | icon, symbol, pictogram, glyph, favicon | low |
| **illustration** | illustration, scene, drawing, artwork, graphic | high |
| **infographic** | infographic, data visualization, chart, diagram | high |
| **pattern** | pattern, texture, background, tile, seamless | medium |
| **animated** | animated, animation, motion, loading, spinner | high |
| **animated-scene** | animated illustration, character animation, story | high |
| **ui-element** | button, card, banner, header, component | low-medium |

Gather any missing essentials:
- **What** to depict (subject, content, data)
- **Style** preference (minimalist, gradient, hand-drawn, isometric, etc.)
- **Colors** (specific hex values, or a mood like "warm", "corporate", "playful")
- **Size/ratio** (square, wide, tall — defaults to `0 0 800 600` if unspecified)
- **Animation** (if animated: what moves, speed, loop behavior)

Do NOT over-question. If the user gave a clear description, proceed immediately.

## Step 2: Build the Prompt

Read `references/prompt-templates.md` for the system prompt and category-specific suffix.

Construct the Gemini prompt as:

```
[Master System Prompt for Gemini 3.1 Pro]

[Category-Specific Suffix]

[Style Modifier (if applicable)]

Now create: [user's description, enriched with design details]

Colors: [specified or "choose a harmonious palette suited to the subject"]
ViewBox: [specified or default]
```

**Prompt enrichment rules:**
- Add composition guidance (center the subject, use negative space, layer foreground/background)
- Specify element count to control complexity (fewer = cleaner)
- Name specific SVG features when relevant (gradients, filters, clipPaths, masks)
- For text in SVGs, specify: font-family (use web-safe), font-size, font-weight, fill
- For animations, describe timing, easing, and which elements move
- Leverage Gemini 3.1 Pro's strength: request semantic HTML comments describing each section

## Step 3: Generate

Select thinking level based on complexity:

| Complexity | thinkingLevel | Use for |
|------------|---------------|---------|
| low | `low` | Simple icons, basic shapes |
| medium | `medium` | Logos, patterns, UI elements |
| high | `high` | Illustrations, animations, complex scenes |

Call Gemini 3.1 Pro:

```
mcp__gemini__gemini-query(
  prompt: <constructed prompt>,
  model: "pro",
  thinkingLevel: <selected level>
)
```

Extract the SVG from the response. Strip any markdown fences, explanatory text, or preamble — keep only `<svg>...</svg>`.

**If timeout/error occurs**: Retry once. Gemini 3.1 Pro may have high latency for complex SVGs.

## Step 4: Analyze

Review the returned SVG for:

1. **Validity** — Well-formed XML? All tags closed? Attributes quoted?
2. **Completeness** — Does it match what was requested? Missing elements?
3. **Quality** — Proportions correct? Colors harmonious? Text readable?
4. **Structure** — Has viewBox? Uses `<defs>` for reusables? Groups organized?
5. **Bloat** — Unnecessary elements? Excessive precision? Redundant attributes?
6. **Animation** (if animated) — All @keyframes defined? prefers-reduced-motion? Smooth loops? `stdDeviation` not `stdDev`?

Score mentally: if 2+ issues found, proceed to refinement.

## Step 5: Refine (up to 2 rounds)

If issues exist, send a targeted fix prompt to Gemini:

```
Here is an SVG that needs fixes:

<svg>...the current SVG...</svg>

Issues to fix:
1. [specific issue and how to fix it]
2. [specific issue and how to fix it]

[Include Quality Checklist Prompt from references/prompt-templates.md]
```

Call `mcp__gemini__gemini-query` again with `model: "pro"`, same or higher `thinkingLevel`.

After 2 refinement rounds, stop refining and proceed to optimization — diminishing returns beyond this.

## Step 6: Optimize

Apply Claude-side cleanup (see `references/svg-optimization.md` for full checklist):

1. **Strip wrapping** — Remove markdown fences, text outside `<svg>` tags
2. **Fix xmlns** — Ensure `xmlns="http://www.w3.org/2000/svg"` present
3. **Fix viewBox** — Ensure viewBox is set and frames content properly
4. **Consolidate colors** — Move inline colors to `<defs><style>` classes
5. **Add accessibility** — Add `<title>` and `<desc>`, `role="img"`, `aria-labelledby`
6. **Clean decimals** — Round to 2 decimal places
7. **Remove dead code** — Empty groups, hidden elements, unused defs
8. **Fix deprecated** — `xlink:href` → `href`
9. **Fix filter typos** — `stdDev` → `stdDeviation` (common Gemini output error)
10. **Animation safety** — Ensure `prefers-reduced-motion` media query present for animated SVGs

## Step 7: Save & Present

Save SVG file(s) using the Write tool:
- Use descriptive filename: `{subject}-{style}.svg` (e.g., `rocket-minimalist.svg`)
- For multiple variations, use numbered suffixes or style names
- Default save location: current working directory, or user-specified path

Present to the user:
- Show the SVG inline (the raw code)
- Describe what was created and key design choices
- Offer to iterate: "Want me to adjust colors, style, or add variations?"

## Multi-Variation Workflow

When the user wants multiple concepts or variations:

1. Generate each variation as a separate Gemini call with modified prompts
2. Name files clearly: `logo-concept-1-geometric.svg`, `logo-concept-2-organic.svg`
3. Present all variations with brief rationale for each
4. Let user pick favorites for refinement

## Style Quick Reference

| Style | Key characteristics |
|-------|-------------------|
| Minimalist | Few elements, monochrome/2-color, geometric, whitespace |
| Flat | No gradients/shadows, bold solids, clear silhouettes |
| Gradient | Linear/radial gradients, smooth transitions, modern depth |
| Hand-drawn | Imperfect lines, organic shapes, warm and friendly |
| Isometric | 30-degree angles, consistent depth, flat-shaded faces |
| Glassmorphism | Semi-transparent, blur filters, frosted glass, subtle borders |
| Retro | Muted palette, halftone textures, rounded shapes |
| Line Art | Strokes only, no fills, consistent width, single color |
| Neon | Dark background, bright strokes, glow filter, high contrast |
| Geometric | Circles/rects/triangles only, mathematical precision, bold blocks |

For full prompt templates per style, see `references/prompt-templates.md`.

## Resources

- **references/prompt-templates.md** — Master system prompt (Gemini 3.1 Pro optimized), category suffixes, animation templates, style modifiers, quality checklist
- **references/svg-optimization.md** — Post-generation cleanup checklist, common Gemini 3.1 Pro SVG issues and fixes
