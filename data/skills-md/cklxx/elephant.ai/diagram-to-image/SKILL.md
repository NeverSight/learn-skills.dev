---
name: diagram-to-image
description: Render Mermaid diagrams to PNG/SVG for sharing.
triggers:
  intent_patterns:
    - "mermaid|流程图|架构图|时序图|sequence diagram|flowchart"
    - "转成图片|导出图片|render.*(png|svg)|diagram.*(png|图片)"
    - "icon block|图标块|图标卡片|信息卡片"
  context_signals:
    keywords: ["mermaid", "diagram", "flowchart", "流程图", "架构图", "时序图", "图标", "png", "svg", "render", "导出"]
  confidence_threshold: 0.6
priority: 7
requires_tools: [bash]
max_tokens: 200
cooldown: 60
---

# diagram-to-image

Render Mermaid code into image files.

## Requirements
- `mmdc` (Mermaid CLI) installed and in PATH.
- Install command: `npm install -g @mermaid-js/mermaid-cli`

## Constraints
- `action=render` only.
- Input field is `code` (Mermaid source).
- Supported output formats: `png` (default), `svg`.
- Render timeout: 30s.
- Default output path: `/tmp/diagram_<ts>.<format>`.

## Usage

```bash
python3 skills/diagram-to-image/run.py render --code 'graph LR
A[Client] --> B[API]
B --> C[(DB)]' --format png --theme default --output /tmp/diagram_arch.png
```
