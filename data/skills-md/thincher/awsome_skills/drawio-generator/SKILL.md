---
name: drawio-generator
description: Generate draw.io diagrams from Mermaid, XML, or CSV code. Use this skill when the user requests any visual diagram including flowcharts, UML diagrams, ERD, architecture diagrams, mind maps, timelines, org charts, network topology, wireframes, BPMN, or any other visual representation. The skill creates a markdown link that opens the diagram in draw.io.
---

# Draw.io Diagram Generator

Generate interactive draw.io diagrams that users can open and edit in their browser.

## Supported Diagram Types

Draw.io supports virtually any diagram type:
- **Standard**: Flowcharts, org charts, mind maps, timelines, Venn diagrams
- **Software**: UML (class, sequence, activity, use case), ERD, architecture diagrams
- **Cloud/Infrastructure**: AWS, Azure, GCP, Kubernetes, network topology
- **Engineering**: Electrical circuits, digital logic, P&ID, floor plans
- **Business**: BPMN, value streams, customer journeys, SWOT
- **UI/UX**: Wireframes, mockups, sitemaps
- **And more**: Infographics, data flows, decision trees, etc.

## Format Selection Guide

| Format | Best For |
|--------|----------|
| **Mermaid** | Flowcharts, sequences, ERD, Gantt, state diagrams, class diagrams |
| **CSV** | Hierarchical data (org charts), bulk import from spreadsheets |
| **XML** | Complex layouts, precise positioning, custom styling, icons, shapes |

## How to Use

### Step 1: Determine the best format for the diagram

- Use **Mermaid** for most standard diagrams (flowcharts, sequence diagrams, ERD)
- Use **CSV** for hierarchical data like org charts
- Use **XML** when you need precise control over positioning or custom shapes

### Step 2: Generate the diagram code

Write the diagram code in the chosen format (see examples below).

### Step 3: Execute the Python script

Run the script `scripts/generate_drawio_url.py` (relative to this SKILL.md file) to create the markdown link.

## Format Templates 


### Mermaid
```
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
```

### XML (draw.io native)
```xml
<mxGraphModel>
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <mxCell id="2" value="Box" style="rounded=1;fillColor=#d5e8d4;" vertex="1" parent="1">
      <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>
```

### CSV (hierarchical data)
```
# label: %name%
# style: rounded=1;whiteSpace=wrap;html=1;
# connect: {"from":"manager","to":"name","invert":true}
# layout: auto
name,manager
CEO,
CTO,CEO
CFO,CEO
```


## CRITICAL: XML Well-Formedness

When generating draw.io XML, the output **must** be well-formed XML:
- **NEVER use double hyphens (`--`) inside XML comments.** Use single hyphens or rephrase (e.g., `<!-- Order 1 to OrderItem -->` not `<!-- Order 1 --- OrderItem -->`)
- Escape special characters in attribute values (`&amp;`, `&lt;`, `&gt;`, `&quot;`)

## Script Usage

The script `generate_drawio_url.py` is located in the `scripts/` subdirectory relative to this SKILL.md file. Execute it with command-line arguments:

```bash
python scripts/generate_drawio_url.py -t mermaid -c "graph TD\n    A --> B"
python scripts/generate_drawio_url.py --type xml --code "<mxGraphModel>...</mxGraphModel>"
python scripts/generate_drawio_url.py -t csv -c "name,manager\nCEO,\nCTO,CEO"
```

**Arguments:**
- `-t, --type`: Diagram type (required), choices: `mermaid`, `xml`, `csv`
- `-c, --code`: Diagram code content (required)

The script outputs a markdown link: `[点击查看图表](<URL>)`

Present the markdown link directly to the user.
