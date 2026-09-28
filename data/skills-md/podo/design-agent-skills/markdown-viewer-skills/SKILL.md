---
name: markdown-viewer-skills
description: |
  14 visualization skills across 5 rendering engines: Vega-Lite, PlantUML,
  JSON Canvas, HTML/CSS, and Infographic templates. The most complete data
  visualization and diagram collection — charts, UML, cloud architecture,
  network diagrams, mind maps, and 70+ infographic templates.
triggers:
  - "markdown viewer"
  - "vega chart"
  - "PlantUML"
  - "JSON Canvas"
  - "infographic"
  - "UML diagram"
  - "cloud architecture diagram"
  - "network diagram"
das:
  category: data-visualization
  upstream: "https://github.com/markdown-viewer/skills"
  version: latest
  install: false
---

# markdown-viewer-skills

> Catalogue stub — full package: [markdown-viewer/skills](https://github.com/markdown-viewer/skills)

## Decision tree

Run this before any chart, diagram, or infographic work:

1. **Is the package already installed?**
   Check: `~/.design-agent-skills/skills/vega/SKILL.md` exists (representative skill).
   - Yes → invoke the relevant skill by name and proceed
   - No → go to step 2

2. **Do you have shell access?**
   - Yes → run the install command below, then invoke the skill
   - No → show the install command; in Claude Code, send it as a chat message starting with `!` — add `-g` for global install or omit for project-only

## Install command

```bash
npx skills add markdown-viewer/skills
```

## Invoke after install

14 skills across 5 rendering engines:

| Skill | Engine | Use case |
|-------|--------|----------|
| `vega` | Vega-Lite | bar, line, scatter, heatmap, radar, word cloud |
| `infographic` | HTML/CSS | 70+ templates: KPI cards, timelines, roadmaps, SWOT |
| `canvas` | JSON Canvas | mind maps, knowledge graphs, concept maps |
| `architecture` | HTML/CSS | layer diagrams, 13 layouts × 12 styles |
| `infocard` | HTML/CSS | editorial info cards, 13 layouts × 14 styles |
| `uml` | PlantUML | 14 UML types + 9,500 mxgraph icons |
| `cloud` | PlantUML | AWS, Azure, GCP, Kubernetes icons |
| `network` | PlantUML | Cisco/Citrix network device icons |
| `security` | PlantUML | IAM, encryption, firewall, compliance |
| `archimate` | PlantUML | enterprise architecture, ArchiMate layers |
| `bpmn` | PlantUML | business process, EIP, Lean Mapping |
| `data-analytics` | PlantUML | ETL/ELT, data warehouse, ML workflows |
| `iot` | PlantUML | IoT devices, sensors, edge computing |
| `mindmap` | PlantUML | mind map syntax with directional branches |

## What it does

The most complete visualization skill collection: 14 skills across 5 rendering engines with 98%+ format coverage. Covers everything from simple charts to enterprise architecture diagrams, cloud topology, and polished infographic templates.
