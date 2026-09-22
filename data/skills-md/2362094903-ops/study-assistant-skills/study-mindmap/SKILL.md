---
name: study-mindmap
description: >
  Mind-map sub-skill (orchestrated by study-assistant; also usable standalone). Use whenever a chapter knowledge-point mind map needs to be generated or refreshed — the user says "思维导图" "知识图谱" "脑图", or any knowledge point's mastery/status changed. Renders knowledge.json into a zero-dependency offline-capable interactive HTML with collapse/expand, drag/zoom, search, and mastery coloring.
---

# Study Mind Map

Render the knowledge tree in `knowledge.json` into an interactive HTML mind map. **Never hand-write the HTML.**

New layout:

```bash
python3 ~/.claude/skills/study-mindmap/scripts/build_mindmap.py \
  <study-dir>/internal/state/knowledge.json --chapter <N>
```

Output: `<study-dir>/internal/mindmaps/chapter-XX.html`. Legacy root `knowledge.json` outputs to legacy `mindmaps/`.

## Preconditions

`knowledge.json` must exist and pass `validate_workspace.py`. This skill renders only; it does not split chapters into points.

Each leaf should be a small teachable/testable unit. A missing formula, law, graph-reading method, or definition is worse than an extra point.

## Features to mention to the learner

- Click nodes to collapse/expand.
- Drag to pan, wheel to zoom.
- Search highlights matches and expands their path.
- Leaf colors: 灰 = 未学, 红 = 薄弱, 黄 = 基本, 浅绿 = 熟练, 绿 = 精通.
- High-importance points show a star.
- Hover shows id, importance, status, mastery, note.

## Regenerate when

- Any point status/mastery/note changes.
- The knowledge list is revised.

Re-running overwrites the file in place. The browser tab only needs refresh.
