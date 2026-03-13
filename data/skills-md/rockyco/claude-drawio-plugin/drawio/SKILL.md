---
name: drawio
description: Create diagrams using Draw.io XML format. Use when the user asks to create diagrams, flowcharts, architecture diagrams, RTL micro-architecture, FSM state diagrams, DATAFLOW decomposition, system topology, wireframes, or any visual drawings. Generates `.drawio` XML files. Preferred over excalidraw for FPGA/HLS diagrams due to simpler format, auto-centered text, and uniform XML for all diagram types including RTL microarch.
---

# Draw.io Diagram Creation

Generate `.drawio` files as XML using the Write tool. No scripts or executables needed.

## Key Advantages Over Excalidraw

| Feature | Draw.io | Excalidraw |
|---------|---------|------------|
| Text in shapes | `value` attribute, auto-centered | Separate text element + containerId + centering math |
| Tokens per element | ~30-50 | ~80-120 |
| RTL microarch format | Same XML as all other diagrams | Requires separate hand-crafted SVG |
| Arrow routing | Built-in orthogonal routing styles | Manual point arrays |
| Binding system | None needed | Bidirectional binding bugs common |
| Interactive editing | Desktop + VSCode extension + web | Web app only |

## File Wrapper

Every `.drawio` file uses this XML structure:

```xml
<mxfile host="Claude" modified="2026-01-01T00:00:00.000Z" agent="Claude Code" version="1.0">
  <diagram id="diagram-1" name="Page-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1"
                  connect="1" arrows="1" fold="1" page="1" pageScale="1"
                  pageWidth="1200" pageHeight="800" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- All diagram elements go here as children of cell "1" -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

- `mxCell id="0"` - Root cell (always required, never modify)
- `mxCell id="1" parent="0"` - Default layer (always required, parent for all content cells)
- All content cells use `parent="1"`
- `dx`/`dy` control scroll offset; `pageWidth`/`pageHeight` control canvas size
- Set `pageWidth`/`pageHeight` to fit content (1200x800 default, increase for complex diagrams)

## Cell Types

### Vertex (Shape)

```xml
<mxCell id="node-1" value="Module Name" style="rounded=1;fillColor=#dbeafe;strokeColor=#1971c2;fontStyle=1;fontSize=12;html=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="60" as="geometry"/>
</mxCell>
```

- `id` - Unique identifier (use descriptive names: `dsp-mul`, `bram-hist`, `io-data-in`)
- `value` - Text displayed inside the shape. Supports HTML: `<b>`, `<br>`, `<font color='#xxx'>`
- `style` - Semicolon-separated style properties (see Style Reference below)
- `vertex="1"` - Marks this as a shape (not an edge)
- `parent="1"` - Parent is the default layer
- `mxGeometry` - Position (x,y) and size (width, height)

### Edge (Connection)

```xml
<mxCell id="edge-1" value="data_t" style="endArrow=classic;strokeColor=#1971c2;strokeWidth=2;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="node-1" target="node-2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

- `source`/`target` - IDs of connected shapes
- `value` - Edge label text (optional)
- `edge="1"` - Marks this as a connection
- `exitX`/`exitY` - Exit point on source (0-1 normalized). 1,0.5 = right center
- `entryX`/`entryY` - Entry point on target (0-1 normalized). 0,0.5 = left center
- Set `relative="1"` on mxGeometry for edges

### Edge with Waypoints

For non-straight routing (L-shaped, around obstacles):

```xml
<mxCell id="edge-2" value="" style="endArrow=classic;strokeColor=#1971c2;strokeWidth=2;html=1;edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="node-1" target="node-3">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="200"/>
      <mxPoint x="300" y="400"/>
    </Array>
  </mxGeometry>
</mxCell>
```

- `edgeStyle=orthogonalEdgeStyle` - Auto-routes with right-angle bends
- `Array as="points"` - Explicit waypoints for manual routing
- Orthogonal routing handles obstacle avoidance automatically

**No degenerate waypoints**: Every mxPoint in the `<Array as="points">`
must differ from its neighbors by at least 1px in either x or y.
Consecutive identical mxPoints produce no routing effect and are noise.

**Edge clearance**: When multiple edges share waypoint corridors (same x for
vertical segments, same y for horizontal), offset by >= 30px to prevent visual
merging. See `references/best-practices.md` Section 9 for full audit checklist.

### Detached Edge (sourcePoint/targetPoint)

When two shapes have intervening shapes between them and auto-routing cannot
find a clean path, use a detached edge with explicit coordinates instead of
`source`/`target` attributes:

```xml
<mxCell id="edge-nco-rotation" value="sin/cos"
        style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#4f46e5;
               strokeWidth=1;dashed=1;endArrow=block;endFill=1;html=1;
               fontSize=9;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="1240" y="175"/>
      <mxPoint x="1240" y="430"/>
    </Array>
    <mxPoint x="1160" y="175" as="sourcePoint"/>
    <mxPoint x="1180" y="430" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

- No `source`/`target` attributes - edge is not bound to any shape
- `sourcePoint` and `targetPoint` are absolute (x,y) coordinates
- Waypoints provide full path control between the endpoints
- Use when shapes are stacked vertically with intervening shapes, or when
  auto-routing consistently produces paths that cross through other shapes
- Trade-off: endpoints do not auto-update when shapes are moved

### Edge Quality Rules (BLOCKING)

These 7 rules prevent the most common visual defects in generated diagrams.
Rule 0 is the foundational requirement. Violation of rules 0-5 produces a
diagram that looks broken when rendered. Rule 6 is a post-generation
optimization pass for layout quality.

0a. **Explicit Connection Points for Non-Waypoint Edges** - Every edge
   WITHOUT manual waypoints (`<Array as="points">`) that has `source` and
   `target` attributes MUST specify ALL FOUR connection point properties in
   its style: `exitX`, `exitY`, `entryX`, `entryY`, plus zero-offsets
   `exitDx=0;exitDy=0;entryDx=0;entryDy=0;`. Omitting any property causes
   auto-routing, which produces different paths on different renderers.
   Self-loops (source == target) also require explicit exit/entry. Detached
   edges (using sourcePoint/targetPoint instead of source/target) are exempt.
   ```
   GOOD: exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;
   BAD:  exitX=1;exitY=0.5;  (missing exitDx/exitDy/entryX/entryY/entryDx/entryDy)
   BAD:  (no exit/entry properties at all - fully auto-routed)
   ```

0b. **No Explicit Connection Points for Waypoint Edges** - Every edge WITH
   manual waypoints (`<Array as="points">`) MUST NOT have explicit
   `exitX`/`exitY`/`entryX`/`entryY` or Dx/Dy properties. Draw.io's
   auto-router dynamically selects the optimal connection point aligned with
   the first/last waypoint. Adding explicit connection points overrides this
   and creates routing jogs where the edge leaves/enters a shape in the
   wrong direction before correcting course toward the waypoint.
   ```
   GOOD (waypoint edge): edgeStyle=orthogonalEdgeStyle;strokeColor=#1971c2;strokeWidth=2;html=1;
   BAD  (waypoint edge): exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.49;...
   ```
   **Waypoint face separation**: When 2+ waypoint edges connect to the SAME
   face of a shape, their first/last waypoints (the one nearest the shape)
   must differ by >= 30px in the perpendicular axis. This makes the
   auto-router pick different face connection points naturally, without
   needing explicit CPs.
   ```
   Shape left face spans Y=[120, 260]. Three edges enter from the left:
   BAD:  edge-A last WP (140, 190), edge-B last WP (150, 190), edge-C last WP (140, 220)
         Auto-router stacks A and B at ~same Y, C barely separated
   GOOD: edge-A last WP (140, 155), edge-B last WP (150, 190), edge-C last WP (140, 225)
         Auto-router distributes entries across the face span
   ```
   Perpendicular axis: Y for left/right faces, X for top/bottom faces.
   The >= 30px spacing ensures the auto-router resolves to visually
   distinct face points.

1. **Face Points Only (Corners Forbidden)** - Edge endpoints (`exitX/exitY`,
   `entryX/entryY`) must be ON a face: one coordinate at 0 or 1, the other
   anywhere in [0,1]. Default to midpoints (0.5). When 2+ edges share the
   same face - counting BOTH entering and exiting edges together -
   distribute positions (0.25, 0.5, 0.75) instead of stacking at
   0.5. For waypoint edges sharing a face, do NOT add explicit CPs -
   instead, position their nearest waypoints >= 30px apart in the
   perpendicular axis so the auto-router naturally separates them (Rule 0b).
   This includes the mixed case where one edge enters and another
   exits the same face at the same Y (or X) coordinate. Never use
   corners where BOTH coordinates are 0 or 1 - orthogonal
   routing creates a diagonal stub from the corner that looks broken.
   ```
   GOOD: exitX=1;exitY=0.5;    (right midpoint - default)
   GOOD: exitX=0;exitY=0.75;   (left face, 75% down - distributed)
   GOOD: entryX=0.5;entryY=1;  (bottom midpoint)
   BAD:  exitX=1;exitY=1;      (corner - creates diagonal stub)
   BAD:  entryX=0;entryY=0;    (corner - creates diagonal stub)
   ```
   **Mixed entry/exit overlap** - If edge A enters the right face at
   `entryY=0.5` and edge B exits the right face at `exitY=0.5`, they
   collide at the same point. Fix by distributing one to 0.25:
   ```
   BAD:  A entryX=1;entryY=0.5 + B exitX=1;exitY=0.5  (overlap at midpoint)
   GOOD: A entryX=1;entryY=0.25 + B exitX=1;exitY=0.5 (separated)
   ```

2. **No Arrow Overlap** - No two edge line segments may share the same pixel
   corridor. Parallel segments on the same axis must be >= 30px apart. See
   Section 9 of `references/best-practices.md` for the full audit checklist.

3. **Minimum 30px Last-Segment Length** - The final segment of an L-shaped or
   elbow arrow (the segment entering the target) must be >= 30px long. Short
   final segments make arrowheads overlap the previous segment, creating an
   ambiguous integral-sign shape. Fix by adding a waypoint that pushes the
   bend further back.
   ```
   BAD (10px final):    ---+    GOOD (40px final):   --+
                            |                            |
                            v                            |
                                                         v
   ```

4. **Label Text Must Not Obscure Arrow Lines** - Edge labels MUST NOT use
   `labelBackgroundColor`. Arrow lines should remain visible through/around
   label text. Use perpendicular label offsets instead: add
   `<mxPoint y="-15" as="offset" />` inside the edge's mxGeometry to shift
   labels above the arrow line. For vertical arrow segments, use
   `<mxPoint x="10" y="0" as="offset" />` instead. For standalone text cells that intentionally
   cover edge paths (phase labels, titles), use `fillColor=#FFFFFF`.
   ```
   GOOD: style="endArrow=classic;strokeColor=#1971c2;fontSize=9;html=1;"
   BAD:  style="endArrow=classic;strokeColor=#1971c2;fontSize=9;labelBackgroundColor=#FFFFFF;html=1;"
   ```

5. **Dashed Box Titles Center-Aligned** - DATAFLOW stage border labels and any
   title text inside dashed containers must use `align=center;` in their style.
   The DATAFLOW Stage Border style already includes `align=center;`, but
   standalone title text cells placed inside stage borders must also include it.

6. **Straight-Arrow Alignment Principle** - Arrows should be straight lines
   whenever geometrically possible. This is the single most impactful layout
   quality rule. Before adding waypoints or accepting jogged routing, check
   whether repositioning the connected shapes would make the arrow straight:
   - **Horizontal arrows**: All connected shapes must share center-y.
     Formula: `shape.y = target_center_y - shape.height / 2`
   - **Vertical arrows**: All connected shapes must share center-x.
     Formula: `shape.x = target_center_x - shape.width / 2`
   - **Inherently non-straight arrows** (acceptable): fan-out from one source
     to N targets at different y positions, fan-in from N sources at different
     y positions to one target, and cross-stage routing in DATAFLOW diagrams.
     These use precision Y/X positioning (see Pipeline Register Connection Rule)
     or waypoint routing.
   When pipeline registers define a horizontal corridor (all sharing center_y),
   every processing block in that corridor must also share that center_y.

7. **Layout Improvement Pass** - After initial placement and edge routing,
   run this 7-step audit to optimize layout quality:
   1. **Edge-shape crossthrough**: Trace each edge path segment by segment.
      If any segment crosses through a shape it does not connect to, reroute
      via an alternative face or add waypoints to go around the obstacle.
      If data arrows repeatedly cross storage elements, relocate the storage
      elements rather than adding waypoints - the layout is wrong.
   2. **Connection point distribution**: Find shapes with 2+ edges on the
      same face, counting both entering and exiting edges together.
      Distribute entry/exit points across faces. If forced to share a face:
      - **Non-waypoint edges**: use positions (0.25, 0.5, 0.75) via explicit CPs
      - **Waypoint edges**: reposition their nearest waypoints >= 30px apart
        in the perpendicular axis (Rule 0b) - never add explicit CPs
      - **Mixed groups**: distribute non-waypoint edges via CPs; reposition
        waypoint edges via waypoint spacing
   3. **Route determinism**: In crowded areas where auto-routing produces
      ambiguous paths, add explicit waypoints so every segment is
      deterministic. The auto-router should only handle the first/last
      few pixels from exit/entry points to the nearest waypoint.
   4. **Cross-stage simplification**: Edges crossing 2+ stages must route
      OUTSIDE all stage boxes entirely (above or below the dashed borders,
      not just above the blocks inside). Keep >= 20px from the nearest
      stage box edge. Bypass streams route below; direct outputs from
      middle stages route above.
   5. **Container tightening**: Set container height to
      `max_child_bottom_y - container_y + 30px`. Adjust legend position
      to match the tightened layout.
   6. **Center alignment for straight connections**: When shapes are
      connected by arrows that should be straight lines, align their
      centers on the shared axis:
      - **Vertical arrows** (exitX=0.5, entryX=0.5): all connected
        shapes must share the same center-x. `shape.x = center_x - width / 2`
      - **Horizontal arrows** (exitY=0.5, entryY=0.5): all connected
        shapes must share the same center-y. `shape.y = center_y - height / 2`
      Different dimensions with the same top/left coordinate creates
      angled arrows that should be straight.
   7. **Label-edge clearance**: Verify that FIFO label boxes and
      annotation labels do not overlap edge routing paths. Labels must
      have >= 15px clearance from the nearest edge segment. If an edge
      at y=445 runs through a label at y=432-462, reposition the label
      above (y < 430) or below (y > 460) the edge.

   See `references/best-practices.md` Section 4 and Section 9 for detailed
   techniques with before/after XML examples.

### Standalone Text (Label)

```xml
<mxCell id="label-1" value="Phase 1: Input" style="text;fontSize=14;fontStyle=1;fillColor=none;strokeColor=none;html=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="50" width="120" height="30" as="geometry"/>
</mxCell>
```

- `fillColor=none;strokeColor=none` - Invisible container (text only)
- Use for titles, annotations, phase labels, bit-width annotations

## Style Reference

Style strings are semicolon-separated key=value pairs. Always include `html=1;` to enable HTML labels.

### Shape Styles

| Property | Values | Description |
|----------|--------|-------------|
| `rounded` | `0` (sharp) / `1` (rounded) | Corner style |
| `fillColor` | `#hex` | Background fill |
| `strokeColor` | `#hex` | Border color |
| `strokeWidth` | number | Border thickness (default 1) |
| `dashed` | `0` / `1` | Dashed border |
| `dashPattern` | `string` | e.g., `8 4` for custom dash |
| `fontStyle` | `0`/`1`/`2`/`3` | 0=normal, 1=bold, 2=italic, 3=bold+italic |
| `fontSize` | number | Text size in points |
| `fontColor` | `#hex` | Text color |
| `fontFamily` | name | e.g., `Courier New` for monospace |
| `html` | `1` | Enable HTML in value (ALWAYS include) |
| `whiteSpace` | `wrap` | Enable text wrapping |
| `align` | `left`/`center`/`right` | Horizontal text alignment |
| `verticalAlign` | `top`/`middle`/`bottom` | Vertical text alignment |
| `shape` | `ellipse`/`rhombus`/`cylinder`/`hexagon` | Non-rectangle shapes |
| `opacity` | 0-100 | Element transparency |

### Edge Styles

| Property | Values | Description |
|----------|--------|-------------|
| `endArrow` | `classic`/`block`/`open`/`none` | Arrowhead at target |
| `startArrow` | `classic`/`block`/`open`/`none` | Arrowhead at source |
| `strokeColor` | `#hex` | Line color |
| `strokeWidth` | number | Line thickness |
| `dashed` | `0` / `1` | Dashed line |
| `dashPattern` | `string` | Custom dash pattern |
| `edgeStyle` | `orthogonalEdgeStyle`/`elbowEdgeStyle`/`entityRelationEdgeStyle` | Routing algorithm |
| `curved` | `0` / `1` | Curved routing |
| `exitX`/`exitY` | 0-1 | Exit point on source shape |
| `entryX`/`entryY` | 0-1 | Entry point on target shape |
| `labelPosition` | `left`/`center`/`right` | Label horizontal position |
| `verticalLabelPosition` | `top`/`middle`/`bottom` | Label vertical position |

### Connection Points (exitX/exitY and entryX/entryY)

```
(0,0)-----(0.5,0)-----(1,0)       CORNERS (both 0 or 1): FORBIDDEN
  |                      |
(0,0.5)              (1,0.5)       FACE MIDPOINTS: default choice
  |                      |
(0,0.75)             (1,0.25)      FACE POINTS: use to distribute
  |                      |
(0,1)-----(0.5,1)-----(1,1)       CORNERS (both 0 or 1): FORBIDDEN
```

**CORNERS FORBIDDEN for edges**: A connection point is valid when exactly one
coordinate is 0 or 1 (placing it on a face). Both coordinates at 0 or 1 is a
corner - orthogonal routing creates a diagonal stub that looks broken. Default
to midpoints (0.5). When 2+ edges share the same face, distribute them using
fractional positions (0.25, 0.75) to prevent overlap. Corners are acceptable
for shapes (e.g., container nesting) but never for edge connection points.

**Waypoint edges**: DO NOT set connection points on waypoint edges.
Draw.io's auto-router dynamically selects the optimal face point that
minimizes the path to the first/last waypoint. Explicit coordinates
override this and create routing jogs. Use `fix_drawio_edges.py` to
strip explicit connection points from waypoint edges. When 2+ waypoint
edges share a face, separate them by positioning their nearest waypoints
>= 30px apart in the perpendicular axis (see Rule 0b).

For ellipses, same normalized coordinates apply to the ellipse bounding box.

## FPGA Component Styles

### Semantic Color Palette

| Component | Fill | Stroke | Text Color | Use For |
|-----------|------|--------|------------|---------|
| DSP / Computation | `#dbeafe` | `#1971c2` | `#1e3a5f` | DSP48, multipliers, adders, accumulators |
| Memory / Storage | `#e0e7ff` | `#4f46e5` | `#3730a3` | BRAM, ROM, shift registers, circular buffers |
| Control / FSM | `#fef3c7` | `#d97706` | `#92400e` | FSM blocks, CORDIC, controllers |
| FIR IP | `#fef9c3` | `#ca8a04` | `#854d0e` | hls::FIR instances |
| Data I/O | `#d1fae5` | `#059669` | `#065f46` | Data streams (hls::stream) |
| Control I/O | `#fce7f3` | `#db2777` | `#9d174d` | Async control ports (index_t, scalar) |
| DATAFLOW Stage | `#f8fafc` | `#94a3b8` | `#475569` | Stage boundaries |
| Accumulator | `#99e9f2` | `#0c8599` | `#0c8599` | Running accumulators |
| Pipeline Register | `#e9ecef` | `#868e96` | `#495057` | Pipeline stage boundaries |

### Complete FPGA Style Strings

**DSP48 Block:**
```
rounded=0;fillColor=#dbeafe;strokeColor=#1971c2;fontColor=#1e3a5f;fontStyle=1;fontSize=11;html=1;whiteSpace=wrap;
```

**BRAM / Memory:**
```
rounded=1;fillColor=#e0e7ff;strokeColor=#4f46e5;fontColor=#3730a3;fontStyle=1;fontSize=11;html=1;whiteSpace=wrap;dashed=1;
```

**Control / FSM:**
```
rounded=1;fillColor=#fef3c7;strokeColor=#d97706;fontColor=#92400e;fontStyle=1;fontSize=11;html=1;whiteSpace=wrap;
```

**FIR IP:**
```
rounded=0;fillColor=#fef9c3;strokeColor=#ca8a04;fontColor=#854d0e;fontStyle=1;fontSize=11;html=1;whiteSpace=wrap;
```

**Data I/O Port (Ellipse):**
```
shape=ellipse;fillColor=#d1fae5;strokeColor=#059669;fontColor=#065f46;fontSize=10;html=1;
```

**Control I/O Port (Ellipse):**
```
shape=ellipse;fillColor=#fce7f3;strokeColor=#db2777;fontColor=#9d174d;fontSize=10;html=1;
```

**DATAFLOW Stage Border:**
```
rounded=1;fillColor=#f8fafc;strokeColor=#94a3b8;dashed=1;dashPattern=8 4;strokeWidth=1.5;fontStyle=1;fontSize=13;fontColor=#475569;html=1;verticalAlign=top;align=center;
```

**Accumulator:**
```
rounded=0;fillColor=#99e9f2;strokeColor=#0c8599;fontColor=#0c8599;fontStyle=1;fontSize=11;html=1;whiteSpace=wrap;
```

**Pipeline Register (thin tall rect):**
```
rounded=0;fillColor=#e9ecef;strokeColor=#868e96;fontColor=#495057;fontSize=9;html=1;
```

**Pipeline Register Connection Rule**: Pipeline registers are thin tall
rectangles (width <= 20px, height/width >= 5). Arrows MUST connect to
their LEFT or RIGHT face only (`exitX=0`/`exitX=1`, `entryX=0`/`entryX=1`).
NEVER connect to top (Y=0) or bottom (Y=1) faces - the 8px connection
surface produces visually awkward routing. When a pipeline register fans
out to N targets at different y positions, compute each connection's Y
fraction as `(target_center_y - preg_y) / preg_height` and add
`entryPerimeter=0`/`exitPerimeter=0` to the connection style for exact
positioning. The tool `fix_drawio_edges.py` detects top/bottom violations
and reroutes them automatically.

**FIFO Indicator:**
```
rounded=1;fillColor=#eff6ff;strokeColor=#1971c2;dashed=1;dashPattern=4 2;fontSize=10;fontColor=#1971c2;fontStyle=2;html=1;
```

**Resource Summary / Legend Box:**
```
rounded=1;fillColor=#f9fafb;strokeColor=#d1d5db;fontSize=11;fontColor=#4b5563;html=1;align=left;verticalAlign=top;whiteSpace=wrap;
```

### Arrow Styles

**Data Bus (solid blue):**
```
endArrow=classic;strokeColor=#1971c2;strokeWidth=2;html=1;
```

**Control Signal (dashed red):**
```
endArrow=classic;strokeColor=#e03131;strokeWidth=1.5;dashed=1;dashPattern=6 3;html=1;
```

**Memory Access (dashed indigo):**
```
endArrow=classic;strokeColor=#4f46e5;strokeWidth=1.5;dashed=1;dashPattern=4 2;html=1;
```

**Feedback Path (dotted gray):**
```
endArrow=classic;strokeColor=#868e96;strokeWidth=1;dashed=1;dashPattern=2 2;html=1;
```

**Coefficient Feed (dashed blue, thin):**
```
endArrow=classic;strokeColor=#1971c2;strokeWidth=1.5;dashed=1;dashPattern=4 2;html=1;
```

## HLS Diagram Types

### 1. System Block Diagram (Phase 1, 7)

Shows module topology with data/control streams and FIFO depths.

**Layout**: Left-to-right data flow. Modules as rounded rectangles. Splitters as small diamonds. I/O ports as ellipses at edges.

**Canvas**: `pageWidth="1400" pageHeight="600"`

**Required elements**:
- Input/output port ellipses (data I/O style)
- Module blocks with name + brief description
- Data stream arrows (solid blue) with type labels
- Control signal arrows (dashed red) with type labels
- Splitter nodes for fan-out
- FIFO depth annotations on Phase 7 integration diagrams
- Resource summary box (Phase 6+ with DSP/BRAM/LUT/FF)
- Legend box

### 2. DATAFLOW Decomposition (Phase 5)

Shows internal DATAFLOW stages (EXTRACT/COMPUTE/APPLY or TMCS 4-stage).

**Layout**: Left-to-right stages in dashed borders. Internal FIFOs between stages.
All stages share the same top y. Max height ratio between stages: 1.5x.
Arrows that skip stages route OUTSIDE all stage boxes: above for direct outputs
from middle stages, below for bypass/passthrough streams. Keep >= 20px clearance
from the nearest stage box edge.

**Canvas**: `pageWidth="1200" pageHeight="600"`

**Required elements**:
- Stage boundary rectangles (DATAFLOW stage style, dashed)
- Function blocks inside each stage
- Internal FIFO streams between stages (with depth labels)
- Data I/O ports at diagram edges
- Control I/O ports if FSM+DATAFLOW
- Bypass/passthrough streams (below main flow)
- Stage labels: "EXTRACT", "COMPUTE", "APPLY" (or TMCS stages)
- **FIFO label z-order**: FIFO boxes between stages must be placed AFTER all
  edges in the XML (Layer 4). See Z-Order section.
- **Vertical alignment**: Components connected by top-to-bottom arrows within
  a stage must share the same center-x coordinate

### 3. FSM State Diagram (Phase 5)

Shows finite state machine transitions.

**Layout**: States arranged in a flow: typically left-to-right or top-to-bottom for the main path, with loops shown as self-referencing edges.

**Canvas**: `pageWidth="1000" pageHeight="600"`

**Required elements**:
- State boxes as rounded rectangles (control/FSM style)
- Initial state indicator (extra bold border or filled arrow from a dot)
- Transition arrows with condition labels
- Self-loop transitions (edge with same source and target, use waypoints to create visible loop)
- Entry/exit actions as italic text inside state boxes

**Self-loop pattern:**
```xml
<mxCell id="self-loop-1" value="!ctrl.empty()" style="endArrow=classic;strokeColor=#d97706;strokeWidth=1.5;html=1;curved=1;" edge="1" parent="1" source="state-wait" target="state-wait">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="200" y="50"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### 4. RTL Micro-Architecture (Phase 5, 6)

Detailed datapath diagram showing FPGA primitives, pipeline stages, and data flow with bit-width annotations.

**Layout**: Left-to-right data flow. I/O ports at edges. Pipeline stages separated by pipeline register columns. Storage elements (BRAMs, ROMs) directly above their computation consumer with matching center-x, vertical coefficient arrows entering the consumer's top face - this keeps horizontal data corridors clear. When a block receives fan-in from N sources, position it at the vertical midpoint of those sources: `block_center_y = (source_top_center_y + source_bottom_center_y) / 2`. When pipeline registers define the main datapath corridor, all processing blocks connected by horizontal arrows within that corridor must share the same center-y as the pipeline registers.

**Canvas**: `pageWidth="1400" pageHeight="700"` (increase for complex modules)

**Required elements**:
- I/O port ellipses (data + control)
- DSP48 blocks for computation
- BRAM/shift register blocks for storage
- Pipeline register columns (thin tall rectangles)
- Accumulator blocks with feedback arrows
- Comparator diamonds for detection logic
- MUX diamonds for selection logic
- Bit-width annotations on data bus arrows (e.g., "18b", "32b cplx")
- Phase boundary labels
- Resource summary box with DSP/BRAM/LUT/FF counts
- Legend box with color key
- DATAFLOW stage borders (if applicable)

## HTML Labels in Shapes

Draw.io supports rich HTML in the `value` attribute. Always include `html=1;` in style.

### Multi-Line Labels

```xml
value="<b>DSP: Multiply</b><br>26 x (18b x 16b)<br><font color='#6b7280' style='font-size:9px'>26 DSP48E1</font>"
```

### Bold Title + Details

```xml
value="<b>hls::FIR (80 taps)</b><br>SP=4 | 10 DSP48E1"
```

### Monospace Technical Labels

```xml
value="<font face='Courier New'>circ_buf[16384]</font><br>BRAM, no partition"
```

### Subscript/Superscript

```xml
value="x[n] = r<sub>n</sub> + j*q<sub>n</sub>"
```

## Architecture Summary JSON (.arch.json)

Every diagram has a companion `.arch.json` file (~500-1500 tokens) for machine consumption. The schema is format-independent (same for excalidraw and draw.io diagrams).

Schema: `.claude/schemas/arch_diagram_schema.json`

**Key fields by diagram type:**

| Type | Required Fields | Optional Fields |
|------|----------------|-----------------|
| `system_block` | title, type, phase, version, nodes, edges | resources, patterns, hardware_params, control_signals |
| `module_architecture` | title, type, phase, version, nodes, edges | module_pattern, patterns_applied, control_inputs |
| `fsm_states` | title, type, phase, version, states | nodes |
| `dataflow` | title, type, phase, version, stages, edges | nodes |
| `system_integration` | title, type, phase, version, nodes, edges | fifo_depths, system_resources, latency_budget, per_module_resources |

## Construction Checklist

When generating a draw.io diagram:

1. **Start with the wrapper** - Copy the mxfile/diagram/mxGraphModel/root skeleton
2. **Set canvas size** - Adjust pageWidth/pageHeight based on diagram complexity
3. **Place I/O ports first** - Ellipses at left/right edges
4. **Add main blocks** - Position on a 10px grid, left-to-right data flow
5. **Add stage borders** - Dashed rectangles behind groups of blocks (use lower z-order by placing them earlier in XML)
6. **Connect with edges** - Data bus (solid blue), control (dashed red), memory (dashed indigo). Non-waypoint edges MUST specify `exitX/exitY/exitDx=0/exitDy=0` AND `entryX/entryY/entryDx=0/entryDy=0` (Rule 0a). Waypoint edges MUST NOT have explicit connection points (Rule 0b). Use face midpoints as default (Rule 1). Ensure last segment >= 30px
7. **Audit edge quality** - Run all 7 Edge Quality Rules: (0a) explicit connection points on non-waypoint edges, (0b) no explicit connection points on waypoint edges, (1) face points only, corners forbidden, distribute when shared, (2) no arrow overlap (>= 30px clearance), (3) last segment >= 30px, (4) label backgrounds match canvas, (5) stage titles center-aligned, (6) layout improvement pass (crossthrough, distribution, determinism, simplification, tightening, center alignment, label-edge clearance). Verify z-order: annotation labels AFTER edges in XML
8. **Add labels** - Title, subtitle, bit-width annotations, phase labels
9. **Add resource summary** - Bottom-left box with DSP/BRAM/LUT/FF
10. **Add legend** - Bottom-right box with arrow/block color key
11. **Generate .arch.json** - Companion file with graph structure

### Z-Order (4-Layer Model)

Elements render in document order (earlier = behind, later = on top). Use this
4-layer ordering to prevent edges from covering labels or labels from hiding
behind stage borders:

```
Layer 1 (back):  Stage borders, container rectangles (dashed backgrounds)
Layer 2:         Component shapes (blocks, ellipses, storage elements)
Layer 3:         Edges (all arrows and connections)
Layer 4 (front): Annotation labels (FIFO boxes, standalone labels that overlay edges)
                 Legend box, resource summary box
```

**Critical**: FIFO label boxes and inter-stage annotation boxes must be defined
AFTER all edges in the XML. If placed before edges, the edges render on top and
visually cover the labels. This is the most common cause of "partially covered
FIFO boxes" in DATAFLOW diagrams.

### ID Convention

Use descriptive IDs for readability:
- Shapes: `io-data-in`, `dsp-mul`, `bram-hist`, `stage-extract`, `ctrl-fsm`
- Edges: `edge-data-in-to-sr`, `edge-ctrl-offset`, `edge-feedback`
- Labels: `label-title`, `label-phase1`, `label-bitwidth-18b`

### Grid Alignment

- Position all elements on 10px grid (x, y, width, height all multiples of 10)
- Minimum shape size: 80x40
- Standard spacing: 40-60px between shapes, 20-30px within groups
- I/O port ellipses: 70x30 minimum

## Rendering to PNG

Always generate a `.png` alongside the `.drawio` file so humans can review without opening an editor.

### Primary: draw.io Desktop CLI (AppImage)

Fastest and most deterministic. Renders headless via Electron + xvfb-run:

```bash
# One-time install (no sudo needed):
curl -sL -o /tmp/drawio.AppImage \
  "https://github.com/jgraph/drawio-desktop/releases/download/v29.5.1/drawio-x86_64-29.5.1.AppImage"
chmod +x /tmp/drawio.AppImage

# Render single diagram (2x scale for crisp output):
xvfb-run -a /tmp/drawio.AppImage --no-sandbox --export --format png --scale 2 \
  -o output.png input.drawio

# Batch render all .drawio files in a directory:
find path/to/diagrams -name "*.drawio" | while read f; do
  outpng="${f%.drawio}.png"
  xvfb-run -a /tmp/drawio.AppImage --no-sandbox --export --format png --scale 2 \
    -o "$outpng" "$f"
done
```

Options:
- `--scale 2`: 2x resolution (recommended for readability)
- `--format png|svg|pdf|jpg`: Output format
- `--no-sandbox`: Required for non-root execution
- `xvfb-run -a`: Virtual framebuffer (no display needed), auto-select server number

GPU errors in output (`Exiting GPU process due to errors during initialization`) are harmless
and do not affect rendering quality.

### Fallback: Playwright MCP

Use when the AppImage is unavailable. Injects XML into draw.io web editor via the
"Edit Diagram" dialog:

```
1. browser_navigate: https://app.diagrams.net/?splash=0&ui=atlas
2. browser_wait_for: time=5
3. Open Extras > Edit Diagram dialog
4. Inject XML via browser_evaluate using native HTMLTextAreaElement setter:
   () => {
     const xml = atob("<base64-encoded mxGraphModel XML>");
     const ta = document.querySelectorAll('textarea');
     const setter = Object.getOwnPropertyDescriptor(
       window.HTMLTextAreaElement.prototype, 'value'
     ).set;
     setter.call(ta[ta.length-1], xml);
     ta[ta.length-1].dispatchEvent(new Event('input', { bubbles: true }));
     return 'OK';
   }
5. Click OK button
6. browser_press_key: key=Control+Shift+H (fit to window)
7. browser_take_screenshot: filename=diagram.png
```

**Key detail**: The textarea value MUST be set using the native HTMLTextAreaElement
prototype setter, NOT direct assignment. Draw.io's React editor only detects
changes through the native setter + dispatched events.

**Browser sizing**: Use `browser_resize(1920, 1080)` before rendering for adequate
viewport. Default viewport is too small for complex diagrams.

## Comparison with Excalidraw

| Criterion | Draw.io | Excalidraw |
|-----------|---------|------------|
| Format | XML (~5 attrs/cell) | JSON (~50 props/element) |
| Tokens/element | ~30-50 | ~80-120 |
| Text centering | Automatic (value attr) | Manual formula (containerId + x,y calc) |
| Binding system | None needed | Bidirectional (boundElements + containerId) |
| RTL microarch | Same XML format | Separate SVG format required |
| Arrow routing | Built-in orthogonal | Manual point arrays |
| Hand-drawn look | No (always formal) | Yes (roughness > 0) |
| Editing options | Desktop + VSCode + web | Web only |
| CLI rendering | draw.io desktop or Playwright | excalirender |
| Common bugs | Style string typos | Binding mismatches, centering errors |

**When to use Draw.io**: FPGA/HLS architecture diagrams, formal technical documentation, any diagram that will be edited by others in VSCode or desktop tools.

**When to use Excalidraw**: Brainstorming, informal whiteboarding, diagrams that benefit from hand-drawn aesthetic.

## References

For detailed specifications, see:
- `references/element-reference.md` - Complete mxCell property reference
- `references/best-practices.md` - Layout guidelines, FPGA conventions, common mistakes
- `references/fpga-shapes.md` - Complete XML snippets for every FPGA component
- `references/examples.md` - 4 complete working diagrams (system, DATAFLOW, FSM, RTL microarch)
- `references/comparison.md` - Detailed empirical comparison with Excalidraw
- `templates/fpga-library.xml` - Importable custom shape library
