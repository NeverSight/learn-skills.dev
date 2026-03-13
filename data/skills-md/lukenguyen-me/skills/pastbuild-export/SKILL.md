---
name: pastbuild-export
description: Generate Past Build project JSON for portfolio import. Analyzes codebase to extract project name, description, tech stack, and structure for the Past Build import format.
---

# Past Build Export

Turn any codebase into a compelling portfolio piece for pastbuild.com. This skill extracts what makes your project interesting and formats it for easy import.

## When to Use

Users ask things like:
- "Export this to Past Build"
- "Create a portfolio JSON for my project"
- "Generate Past Build format for [project]"

Your job: analyze the codebase, identify the highlights, and output clean JSON.

## What Makes a Strong Project Entry

Past Build isn't a resume template. It's a way to showcase *why* you built something and *what makes it interesting*. Focus on:

**Technical decisions worth talking about** - Not just "used React", but "chose React Server Components to reduce client bundle by 40%"

**Problems you solved** - "I built this after debugging race conditions for three days" tells a story

**Unique features** - What makes this project different from a generic starter template?

**Measurable impact** - "Processes 10K requests/second" or "reduced build time from 45s to 8s"

## JSON Structure

```json
{
  "version": 1,
  "name": "Project Name",
  "description": "One sentence that captures what this project accomplishes",
  "projectStatus": "ongoing" | "finished",
  "projectDate": "YYYY-MM-DD",
  "sections": [
    {
      "id": "uuid-v4",
      "title": "Feature-focused headline",
      "subtitle": "Why this matters + technical insight",
      "order": 0,
      "media": []
    }
  ],
  "links": [...],
  "exportedAt": "2024-01-01T00:00:00.000Z"
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `version` | Yes | Always `1` |
| `name` | Yes | Project name from package.json or repo |
| `description` | Yes | One sentence, pitch-style |
| `projectStatus` | No | `"ongoing"` or `"finished"` |
| `projectDate` | No | When the project was built (git log --reverse helps) |
| `sections` | Yes | 2-5 feature sections work best |
| `links` | No | GitHub, demo, docs |
| `exportedAt` | Yes | Current ISO timestamp |

## Extracting Project Info

### Where to Find Information

| Source | What to Look For |
|--------|------------------|
| `package.json`, `pyproject.toml`, `go.mod` | Name, dependencies, tech stack |
| `README.md` | What the project claims to do, features, origin story |
| Source files | Architecture patterns, complex logic, interesting solutions |
| Git history | When it started, what evolved over time |

### Section Strategy

Each section should cover one compelling aspect of the project. Think:

**"What would I want to show someone if they only had 30 seconds?"**

Good sections answer questions like:
- "What interesting problem does this solve?"
- "What technical challenge did you tackle?"
- "What makes this different from a boilerplate?"

Bad sections just restate generic categories:
- "Overview" (too vague)
- "Tech Stack" (boring, expected)
- "Features" (what doesn't have features?)

### Writing Subtitles That Work

The subtitle is where the story lives. Avoid generic placeholders.

**Weak:** "How authentication works"
**Strong:** "I built custom JWT handling after our team hit session expiration bugs in production - now tokens refresh silently without user disruption"

**Weak:** "Performance optimizations"
**Strong:** "Reduced TTI from 3.2s to 0.8s by deferring non-critical chunks and preloading only what was above the fold"

**Weak:** "Database design"
**Strong:** "Schema designed to handle 10M+ rows without sacrificing query speed - I denormalized just enough to make joins practical"

## Example: SaaS Dashboard

```json
{
  "version": 1,
  "name": "MetricFlow Analytics",
  "description": "A real-time analytics dashboard helping SaaS teams monitor key metrics without switching between tools.",
  "projectDate": "2026-02-01",
  "sections": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "title": "Real-time data pipelines over WebSocket",
      "subtitle": "Built to handle 10K+ concurrent connections without dropping updates - I learned the hard way that polling just doesn't cut it for live dashboards.",
      "order": 0,
      "media": []
    },
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
      "title": "Drag-and-drop widget customization",
      "subtitle": "Users compose their own view by dragging widgets onto a canvas - I used a grid-based layout system to make positioning intuitive yet responsive.",
      "order": 1,
      "media": []
    },
    {
      "id": "c3d4e5f6-a7b8-9012-cdef-345678901234",
      "title": "Multi-tenant RBAC with granular permissions",
      "subtitle": "Each organization gets complete isolation - I implemented row-level security at the database level rather than application level for true data separation.",
      "order": 2,
      "media": []
    }
  ],
  "links": [
    { "id": "l1", "text": "Live Demo", "url": "https://metricflow.example.com" },
    { "id": "l2", "text": "GitHub", "url": "https://github.com/username/metricflow" }
  ],
  "exportedAt": "2026-02-12T01:30:00.000Z"
}
```

## Example: Developer Tool / CLI

```json
{
  "version": 1,
  "name": "GitWip CLI",
  "description": "A developer tool that intelligently groups related git changes into sensible work-in-progress commits.",
  "projectDate": "2026-01-15",
  "sections": [
    {
      "id": "e1f2a3b4-c5d6-7890-abcd-ef1234567890",
      "title": "Smart commit grouping with semantic analysis",
      "subtitle": "Instead of asking 'what files did you change?', it analyzes imports and file patterns to auto-group related changes - this reduced our team's WIP commit noise by 70%.",
      "order": 0,
      "media": []
    },
    {
      "id": "f2a3b4c5-d6e7-8901-bcde-f23456789012",
      "title": "Cross-branch stash management",
      "subtitle": "I built this after losing work twice when stashing on one branch and applying on another - it tracks stash context so nothing ever gets applied to the wrong branch.",
      "order": 1,
      "media": []
    },
    {
      "id": "g3a4b5c6-e7f8-9012-cdef-345678901234",
      "title": "Optimized for monorepos with millions of files",
      "subtitle": "Standard git status is too slow in large repos - I implemented a Rust-based status scanner that cuts status time from 8s to 200ms in our main monorepo.",
      "order": 2,
      "media": []
    }
  ],
  "links": [
    { "id": "l1", "text": "npm Package", "url": "https://npmjs.com/package/gitwip" },
    { "id": "l2", "text": "Documentation", "url": "https://gitwip.dev/docs" }
  ],
  "exportedAt": "2026-02-12T01:30:00.000Z"
}
```

## Quick Reference

**UUID Generation:**
```python
import uuid
str(uuid.uuid4())
# → a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Git date extraction:**
```bash
git log --reverse --format=%ai | head -1
```

**For project status:**
- `ongoing`: Recent commits, active features planned
- `finished`: Side project that reached its goals, no active development

## More Examples

See [EXAMPLES.md](references/EXAMPLES.md) for additional examples across different project types.
