---
name: bibi-vision
description: >
  Extract visual content from a BibiGPT video (slides, OCR, on-screen text)
  and generate a mind map from a saved summary. Use when the user asks what
  is on screen, to analyze slides / PPT / frames, or to make an XMind mind
  map. Do not use to summarize audio or get a transcript (`bibi`), search
  the saved library (`bibi-library`), or manage channel feeds (`bibi-feed`).
  Do not invent digital humans, lip-sync, or shaders — BibiGPT does not
  expose those.
  Triggers: "what's on screen", "analyze the slides", "visual analysis",
  "画面分析", "PPT 上写了什么", "mind map", "思维导图", "extract visuals".
  Same `bibi` CLI binary and same BibiGPT account as the other skills.
agent_created: true
---

# BibiGPT Vision — frames, OCR, mind map

This skill is the visual half of BibiGPT. **Same CLI (`bibi`), same account**
as `bibi` / `bibi-library` / `bibi-feed`. It does not replace a transcript.

Landing: https://bibigpt.co/mcp · Install: https://bibigpt.co/agent · Quota: see `references/auth.md`

## When to use / when not

| Use this skill | Use a sibling instead |
|----------------|------------------------|
| What's on screen / slides / OCR / PPT | Audio summary or transcript → `bibi` |
| Generate a mind map (XMind) from a saved item | Saved-library search → `bibi-library` |
| Visual analysis task (`extract_video_visuals`) | Channel feed → `bibi-feed` |

Do **not** offer digital humans, talking-head, lip-sync, or shader generation.

`bibi video visuals` is **Pro-only** and rate-limited. If the API returns 403, send the user to https://bibigpt.co/shop

## 1. Detect mode

Run `scripts/bibi-check.sh` if present. Prefer CLI (`command -v bibi`), else `$BIBI_API_TOKEN`, else MCP `https://bibigpt.co/api/mcp`. Details: `references/auth.md`.

## 2. Intent routing

| User intent | Workflow |
|-------------|---------|
| Frames, slides, on-screen text, OCR | → `workflows/visual-analysis.md` |
| Mind map / XMind from a saved summary | → `workflows/mindmap.md` |

Need chapters or a transcript first? Call the `bibi` skill, then come back.

## 3. Minimum commands (CLI)

```bash
bibi video visuals --videoUrl "https://..." --json
bibi video mindmap --contentId <id> --summary "..." --json
```

Full flags: `references/cli.md`. MCP names: `extract_video_visuals`, `generate_video_mindmap`.
