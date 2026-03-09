---
name: json-render-templates
description: Json-render protocol templates for flowchart, form, dashboard, info cards, gallery, table, kanban, and diagram.
triggers:
  intent_patterns:
    - "json.render|visual ui|diagram|layout|flowchart|form|dashboard|card grid|gallery|kanban|table"
  context_signals:
    keywords: ["json-render", "flowchart", "form", "dashboard", "cards", "gallery", "table", "kanban", "diagram"]
  confidence_threshold: 0.6
priority: 7
requires_tools: [bash]
max_tokens: 200
cooldown: 60
---

# json-render-templates

Generate json-render protocol payloads for visual layouts: flowcharts, forms, dashboards, info cards, galleries, tables, kanban boards, and diagrams. All templates and serialization logic are handled by run.py.

## 调用

```bash
python3 skills/json-render-templates/run.py render --template dashboard --title 'Product Dashboard' --data '{"metrics":[{"label":"Active users","value":12450}]}'
```
