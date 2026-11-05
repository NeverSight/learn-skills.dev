---
name: text-replace
description: "Bulk replace text content in Figma designs — localization, data filling, content updates. Use when: replace/update/translate/localize + text/content/copy, or when filling designs with real data."
---

# Text Replace — Bulk Text Content Updates

Bulk replace text content across Figma designs. Supports localization, real data filling, and content updates. Works in chunks with visual verification to prevent overflow and truncation.

## Skill Boundaries

- Use this skill to **replace or update existing text content** in bulk.
- If the task is **creating new UI with text**, switch to [figma-create-ui](../figma-create-ui/SKILL.md).
- If the task is **reviewing text quality** (placeholder detection), switch to [design-review](../design-review/SKILL.md).
- If the task is **styling text** (font, size, color), use `text(method: "set_range")` directly.

## Workflow

### Step 1: Scan Text Nodes

```
ping                                          → verify plugin connection
text_scan(nodeId: "...")                      → discover all text nodes in target frame/page
```

**If `ping` fails (plugin not connected):** STOP. Do not fall back to other MCP servers. Tell user: open Figma → Plugins → FigCraft → wait for connection, then retry.

Categorize discovered text by role:
- Headings (large font, bold)
- Body text (paragraph content)
- Labels (form labels, section titles)
- Placeholders (input hints)
- CTAs (button text, links)

### Step 2: Chunk for Processing

Group text nodes by proximity (same parent frame = one chunk):
- For small designs (≤ 30 text nodes): process all at once
- For large designs (> 30 text nodes): process in chunks of 10–15 nodes
- Priority order: headings first → body text → labels/CTAs

### Step 3: Replace Per Chunk

For each chunk:

```
text(method: "set_content", nodeId: "...", content: "new text")
```

Key considerations:
- Check if the text node has a fixed width — keep replacement text similar in length or shorter
- For localization: some languages expand 30–50% (e.g., English → German), plan for overflow
- After each chunk: `export_image(scale: 2)` on the parent frame to verify visually

### Step 4: Verify Per Chunk

After replacing each chunk, check:
- Text fits within containers (no truncation)
- No overflow or clipping
- Line breaks are natural (no mid-word breaks)
- Layout hasn't shifted unexpectedly

If issues found: adjust text content or container width before proceeding to next chunk.

### Step 5: Final QA

```
lint_fix_all                                  → catch text overflow or layout issues
export_image(scale: 1)                        → full design screenshot for final review
```

## Export Scale Guidelines

| Purpose | Scale |
|---------|-------|
| Full page overview | 1 |
| Section check | 2 |
| Individual text detail | 3 |

## Common Use Cases

- Localization: translate UI text to another language
- Data filling: replace placeholder data with realistic content
- Content updates: update copy across multiple screens
- A/B testing: swap text variants for different versions
