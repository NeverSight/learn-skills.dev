---
name: drawio-generator
description: Generate professional draw.io architecture diagrams from text descriptions. The agent generates mxGraph XML directly, validates it, and iterates until correct. Includes 8900+ vendor stencils (AWS, Azure, GCP, Cisco, Kubernetes, etc.). Use when the user asks for draw.io diagrams, architecture diagrams, cloud infrastructure diagrams, or system design visualizations.
---

# Draw.io Diagram Generator

Generate professional-grade Draw.io (mxGraph) XML diagrams from natural language. You ARE the LLM — generate the XML directly, validate it, fix issues, and deliver.

## Critical Rules

### Structure Rules
- **S1: Check Stencil Names** 🚨 NEVER guess stencil names. Check `stencils/*.md` for EXACT names. Wrong: `mxgraph.cisco.router` → Correct: `mxgraph.cisco.routers.router`
- **S2: Stencils Require fillColor** Many stencils have no default color. Always add `fillColor`/`strokeColor`. Exception: edge/link stencils are connectors, not devices.
- **S3: Root Cells Required** Must include `<mxCell id="0"/>` and `<mxCell id="1" parent="0"/>` or diagram won't render.
- **S4: Labels Below Stencils** Use `verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;align=center;` for device/icon labels.
- **S5: mxCell Must Be Siblings** ALL mxCell elements must be siblings under `<root>` — NEVER nest mxCell inside another mxCell.
- **S6: Container Transparency** For container shapes, use `fillColor=none;` to make background transparent and prevent covering child elements.
- **S7: No Array Elements** ⚠️ NEVER use `<Array>` elements in mxGeometry — this CRASHES draw.io! Let draw.io auto-route edges. Use `exitX/exitY/entryX/entryY` style params instead.
- **S8: No XML Comments** NEVER include `<!-- ... -->` in generated XML — breaks editing.

### Layout Rules
- **L1: Starting Margin** Begin positioning from x=40, y=40.
- **L2: Element Spacing** Keep 40-60px gaps between connected shapes; 150-200px for routing channels between groups.
- **L3: Compact Layouts** Use vertical stacking or grid layouts. Keep within x: 0-800, y: 0-600 viewport. Avoid spreading elements too far apart.

### Edge Routing Rules — CRITICAL for Clean Diagrams
- **E1: No Shared Paths** Multiple edges between same nodes must use DIFFERENT exit/entry positions (`exitY=0.3` and `exitY=0.7`, NOT both 0.5).
- **E2: Bidirectional Use Opposite Sides** A→B: `exitX=1`, `entryX=0`. B→A: `exitX=0`, `entryX=1`.
- **E3: Explicit Exit/Entry Points** Every edge should specify: `exitX`, `exitY`, `entryX`, `entryY` in style.
- **E4: Route Around Obstacles** If any shape is between source and target, let draw.io auto-route with `edgeStyle=orthogonalEdgeStyle`. Do NOT use `<Array>` waypoints.
- **E5: Plan Layout First** Organize shapes into columns/rows. Trace each edge mentally: "What shapes are between source and target?"
- **E6: Natural Connection Points** NEVER use corners (`entryX=1,entryY=1`). Top-to-bottom: `exitY=1`, `entryY=0`. Left-to-right: `exitX=1`, `entryX=0`.
- **E7: Diagonal Routing Principle** When connecting distant nodes diagonally, route along the PERIMETER of the diagram, NOT through the middle where other shapes exist.

### Pre-Generation Checklist
1. Do any edges cross over non-source/target shapes? → Rearrange layout
2. Do any two edges share the same path? → Adjust exit/entry points
3. Are any connections at corners? → Use edge centers instead
4. Could rearranging shapes reduce crossings? → Revise layout

## Workflow

### 1. Understand the Request

Determine:
- **Diagram type**: Cloud architecture, microservices, network, UML, ERD, etc.
- **Components**: Systems, services, databases, actors involved
- **Relationships**: Connections (sync/async, data flow, dependencies)

If the user provides a file (PDF, DOCX, TXT, MD), read it and extract entities, relationships, and processes.

### 2. Read the Prompt References

Before generating, read these files for rules and styling guidance:
- `references/drawio_system_prompt.txt` — the master system prompt with all XML rules
- `references/color_palette.md` — professional colors by component type
- `references/drawio_xml_rules.md` — quick-reference for mxGraph syntax

Also study `assets/example_simple.drawio` as a structural reference.

### 3. Select Stencils (if applicable)

If the diagram involves vendor-specific icons (AWS, Azure, GCP, Cisco, Kubernetes, etc.):
1. Identify which stencil library to use from the table below
2. Read the corresponding `stencils/<category>.md` file for EXACT shape names
3. Note the required `fillColor` and recommended dimensions for each shape

**NEVER guess stencil names** — always verify against the stencil file.

### 4. Plan the Layout (Multi-Phase for Complex Diagrams)

For diagrams with >15 components, use this phased approach:

- **P1: Plan** — Identify diagram type, choose canvas size, select stencil libraries. Plan element positions first, then derive zone boundaries.
- **P2: Zones** — Write zone/container cells FIRST in XML (drawio renders by document order). Solid fill: `rounded=1;fillColor=#BAC8D3;strokeColor=none;opacity=60`. Dashed border: `rounded=1;dashed=1;dashPattern=8 8;fillColor=none;strokeColor=#0BA5C4`.
- **P3: Elements** — Position shapes on grid (multiples of 10/20). Keep consistent device style per stencil family.
- **P4: Connections** — Add edges last. Network links: `endArrow=none;endFill=0`. Data flow: `endArrow=classic`. Dashed for logical/VPN: `dashed=1`.
- **P5: Labels** — Add floating text, legends. Verify every element has a `value` or adjacent label.
- **P6: Chunking** — When a diagram exceeds ~30 elements, split XML output into chunks.

### 5. Generate the Draw.io XML

Following the system prompt rules, generate the complete mxFile XML. Key rules:

- Use the exact root skeleton: `<mxfile>` → `<diagram>` → `<mxGraphModel>` → `<root>`
- Always include `<mxCell id="0"/>` and `<mxCell id="1" parent="0"/>`
- Shapes: `vertex="1" parent="1"` with unique descriptive IDs
- Edges: `edge="1" parent="1"` with valid `source` and `target`
- **NEVER** use `<Array>` elements — crashes draw.io
- Use color palette by component type
- Position shapes at grid multiples of 10 or 20
- Labels match the user's language

Save the XML to a `.drawio` file using `write_to_file`.

### 6. Validate (ReAct Loop)

Run the validator script on the saved file:

```bash
python .agent/skills/drawio-generator/scripts/validate_drawio.py <output_file.drawio>
```

- If ✅ valid → proceed to step 7
- If ❌ errors → read the error messages, fix the XML, save again, re-validate
- Repeat until all checks pass

Common fixes:
- **Duplicate IDs**: Renumber cells sequentially
- **Broken edges**: Ensure source/target IDs exist as vertex cells
- **Array elements**: Remove `<Array>` children from edge geometries
- **Malformed XML**: Fix unclosed tags, unescape `&` or `<` in labels

### 7. Deliver

Tell the user:
- Where the `.drawio` file was saved
- Brief design concept (what architectural decisions you made)
- How to open: draw.io desktop, [app.diagrams.net](https://app.diagrams.net), or VS Code Draw.io extension

### 8. Iterative Refinement

If the user wants changes to an existing diagram:
1. Read the current `.drawio` file
2. Modify the XML preserving existing IDs where possible
3. Save, validate, and deliver the updated file

## Stencil Libraries

drawio provides 8900+ pre-built stencils across 48 categories. **Full stencil reference:** See `stencils/*.md` files.

| Category           | Stencil File                                         | Use Case                              |
| ------------------ | ---------------------------------------------------- | ------------------------------------- |
| **AWS**            | `aws4.md`                                            | AWS cloud architecture (1031 shapes)  |
| **Azure**          | `azure.md`, `mscae.md`                               | Azure cloud & enterprise architecture |
| **GCP**            | `gcp2.md`                                            | Google Cloud architecture             |
| **Cisco**          | `cisco.md`, `cisco19.md`, `cisco_safe.md`            | Network topology                      |
| **Kubernetes**     | `kubernetes.md`, `kubernetes2.md`                    | Container orchestration               |
| **Network**        | `networks.md`, `networks2.md`                        | General network diagrams              |
| **Virtualization** | `citrix.md`, `citrix2.md`, `veeam.md`, `vvd.md`      | Infrastructure diagrams               |
| **Software**       | `bpmn.md`, `flowchart.md`, `sitemap.md`, `mockup.md` | Process & UI design                   |
| **Hardware**       | `rack.md`, `cabinets.md`, `electrical.md`            | Data center & electrical              |
| **Office**         | `office.md`, `atlassian.md`, `salesforce.md`         | Business diagrams                     |
| **Cloud (Other)**  | `alibaba_cloud.md`, `ibm_cloud.md`                   | Other cloud providers                 |

### Stencil Usage Example

```xml
<!-- Cisco router with label below -->
<mxCell id="router1" value="Core Router" style="shape=mxgraph.cisco.routers.router;html=1;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;align=center;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="78" height="53" as="geometry"/>
</mxCell>

<!-- AWS Lambda -->
<mxCell id="lambda1" value="Lambda" style="shape=mxgraph.aws4.lambda;html=1;fillColor=#ED7100;strokeColor=none;verticalLabelPosition=bottom;verticalAlign=top;" vertex="1" parent="1">
  <mxGeometry x="200" y="100" width="54" height="56" as="geometry"/>
</mxCell>

<!-- Kubernetes pod -->
<mxCell id="pod1" value="API Pod" style="shape=mxgraph.kubernetes.pod;html=1;fillColor=#326CE5;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;" vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="50" height="50" as="geometry"/>
</mxCell>
```

## Common Shapes Reference

### Basic Shapes
```xml
<mxCell id="rect" value="Box" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="20" y="20" width="100" height="50" as="geometry"/></mxCell>
<mxCell id="rounded" value="Rounded" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="140" y="20" width="100" height="50" as="geometry"/></mxCell>
<mxCell id="circle" value="Circle" style="ellipse;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="260" y="10" width="70" height="70" as="geometry"/></mxCell>
<mxCell id="db" value="Database" style="shape=cylinder;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="350" y="5" width="60" height="80" as="geometry"/></mxCell>
<mxCell id="cloud" value="Cloud" style="ellipse;shape=cloud;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="430" y="10" width="100" height="70" as="geometry"/></mxCell>
```

### Container / Swimlane
```xml
<!-- Swimlane with child elements (relative positioning) -->
<mxCell id="lane1" value="Frontend" style="swimlane;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="200" height="200" as="geometry"/></mxCell>
<mxCell id="step1" value="Step 1" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="lane1">
  <mxGeometry x="20" y="60" width="160" height="40" as="geometry"/></mxCell>
```
**Note:** Children use `parent="lane1"` with coordinates RELATIVE to the swimlane. Edges always use `parent="1"`.

### Edge Patterns
```xml
<!-- Basic directional edge -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="1" source="a" target="b">
  <mxGeometry relative="1" as="geometry"/></mxCell>

<!-- Bidirectional: use different exit/entry Y positions -->
<mxCell id="e1" value="Request" style="edgeStyle=orthogonalEdgeStyle;exitX=1;exitY=0.3;entryX=0;entryY=0.3;endArrow=classic;html=1;" edge="1" parent="1" source="nodeA" target="nodeB">
  <mxGeometry relative="1" as="geometry"/></mxCell>
<mxCell id="e2" value="Response" style="edgeStyle=orthogonalEdgeStyle;exitX=0;exitY=0.7;entryX=1;entryY=0.7;endArrow=classic;html=1;" edge="1" parent="1" source="nodeB" target="nodeA">
  <mxGeometry relative="1" as="geometry"/></mxCell>
```

## Common Style Reference

- **Arrow Types:** Inheritance(`endArrow=block;endFill=0`) Implementation(`endArrow=block;endFill=0;dashed=1`) Association(`endArrow=open;endFill=1`) Dependency(`endArrow=open;dashed=1`) Aggregation(`startArrow=diamondThin;startFill=0`) Composition(`startArrow=diamondThin;startFill=1`)
- **Shape Styles:** `rounded`(0,1) `fillColor`(hex) `strokeColor`(hex) `strokeWidth`(num) `dashed`(0,1) `opacity`(0-100) `fontColor`(hex) `fontSize`(num) `fontStyle`(0=normal,1=bold,2=italic,3=both) `align`(left,center,right) `verticalAlign`(top,middle,bottom) `shadow`(0,1)
- **Edge Styles:** `edgeStyle`(orthogonalEdgeStyle,entityRelationEdgeStyle,elbowEdgeStyle) `curved`(0,1) `endArrow`/`startArrow`(classic,block,open,oval,diamond,none) `endFill`/`startFill`(0=hollow,1=filled)
- **State Colors:** Pending(`#dae8fc`,`#6c8ebf`) Success(`#d5e8d4`,`#82b366`) Error(`#f8cecc`,`#b85450`) Warning(`#fff2cc`,`#d6b656`) Complete(`#e1d5e7`,`#9673a6`)

## Common Pitfalls

| Issue                        | Solution                                              |
| ---------------------------- | ----------------------------------------------------- |
| Shape not visible            | Verify `vertex="1"` and `parent="1"` attributes       |
| Edge not connecting          | Ensure `source` and `target` match cell IDs           |
| Styles not applying          | Check semicolon separators in style string            |
| Text not showing             | Add `html=1;whiteSpace=wrap;` to style                |
| Stencil not rendering        | Verify exact name in `stencils/*.md`, add `fillColor` |
| Edges crossing shapes        | Rearrange layout to minimize crossings                |
| Multiple edges overlapping   | Use different `exitY`/`entryY` values (0.3 and 0.7)   |
| Corner connections look ugly | Use edge centers instead (`exitX=1,exitY=0.5`)        |
| Diagram too spread out       | Keep within x: 0-800, y: 0-600 viewport               |
| XML crashes draw.io          | Remove `<Array>` elements, fix unclosed tags          |

## Tips for AI Generation

1. **Plan layout first**: Sketch positions mentally before writing XML — identify potential edge crossings
2. **Use grid alignment**: Position shapes at multiples of 10 or 20
3. **Unique IDs**: Use descriptive IDs like `client`, `server`, `db` instead of random strings
4. **Consistent spacing**: Keep 40-60px gaps between connected shapes; 150-200px for routing channels
5. **Layer backgrounds first**: Define zone/container cells before shapes inside them
6. **Color zones**: Use light background colors with `strokeColor=none` for region highlighting
7. **Verify edges mentally**: Before generating, trace each edge and ask "Does this cross any shape?"
8. **Escape special characters**: Use `&lt;` for <, `&gt;` for >, `&amp;` for &, `&quot;` for "

## Files

| Path                                  | Purpose                                         |
| ------------------------------------- | ----------------------------------------------- |
| `scripts/validate_drawio.py`          | XML validator — run after every generation      |
| `references/drawio_system_prompt.txt` | Master system prompt with all mxGraph rules     |
| `references/drawio_xml_rules.md`      | Quick-reference for XML syntax                  |
| `references/color_palette.md`         | Professional colors by component type           |
| `assets/example_simple.drawio`        | Working example for structural reference        |
| `stencils/*.md`                       | Stencil libraries — 48 categories, 8900+ shapes |
