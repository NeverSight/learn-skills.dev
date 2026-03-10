---
name: detect-diagram-crossings
description: Detect and analyze edge crossings and overlaps in SVG workflow diagrams using geometric intersection algorithms and visual analysis. Use when validating diagram layouts.
---

# Detect Diagram Crossings

## Purpose
Provide a rigorous, multi-method approach to detecting edge crossings and overlaps in SVG flowchart diagrams. This skill combines mathematical geometric analysis with visual inspection to ensure diagrams have clean, crossing-free layouts.

## When to Use
- **Validating Diagram Layouts**: After creating or modifying workflow diagrams
- **Quality Assurance**: Before committing diagram changes to ensure no crossings
- **Debugging Visual Issues**: When users report crossing/overlap problems
- **Comparative Analysis**: Testing multiple layout versions to find the best one

## Detection Methods

### Method 1: Parametric Line Intersection (Mathematical)
The primary detection method uses parametric line equations to mathematically determine if two line segments intersect.

**Algorithm:**
1. Parse SVG paths into line segments (sequences of points connected by lines)
2. For each pair of line segments from different paths:
   - Calculate intersection using parametric equations:
     - Line 1: P = P1 + t(P2 - P1)
     - Line 2: P = P3 + u(P4 - P3)
   - Solve for parameters t and u
   - Intersection occurs if 0.01 < t < 0.99 AND 0.01 < u < 0.99
3. Exclude endpoint connections (valid node-to-node connections)
4. Report all internal segment intersections as crossings

**Why This Works:**
- Mathematically precise: detects exact intersection points
- Coordinate-based: doesn't rely on visual rendering
- Tolerance-aware: excludes near-endpoint intersections (within 1% of segment length)

**Limitations:**
- May not detect visual overlaps that aren't true mathematical intersections
- Doesn't account for stroke width or arrow markers
- Requires well-formed SVG path data

### Method 2: Node-Path Proximity Analysis
Detects when paths pass through or very close to node bodies (not at connection points).

**Algorithm:**
1. Extract all node bounding boxes from `<rect>` elements: (x, y, width, height)
2. Parse each path's `d` attribute into individual **line segments**
3. **For EACH segment of EACH path** (not just waypoints):
   - **Vertical segments** (same x, different y): Check if x is within any node's x-range AND the y-range of the segment overlaps with the node's y-range
   - **Horizontal segments** (same y, different x): Check if y is within any node's y-range AND the x-range of the segment overlaps with the node's x-range
   - **Diagonal segments**: Check if the line passes through the node's bounding box
4. For each detected intersection:
   - Exclude segments that START or END at a node edge (valid connection points)
   - Report all segments that PASS THROUGH a node's interior

**Critical: Segment-by-Segment Analysis**
A multi-segment path like `M 890 1180 L 550 1180 L 550 820 L 890 820` has THREE segments:
1. Horizontal: (890,1180) → (550,1180) at y=1180
2. Vertical: (550,1180) → (550,820) at x=550
3. Horizontal: (550,820) → (890,820) at y=820

Each segment must be checked independently against ALL nodes. A single path can cross MULTIPLE nodes.

**Why This Works:**
- Catches paths that visually obscure nodes
- Identifies routing issues where paths don't avoid nodes
- Complements line intersection by checking path-node relationships
- **Detects all nodes crossed by multi-segment paths, not just the first one**

### Method 3: Path Overlap and Shared Point Analysis
Detects paths that share segments or start/end points, causing visual confusion.

**Algorithm:**
1. Extract all path endpoints (start and end coordinates)
2. Extract all path segments with their coordinates
3. Check for:
   - **Shared endpoints**: Multiple paths starting or ending at exact same point
   - **Overlapping segments**: Two paths sharing the same line segment (same x or y and overlapping range)
   - **Convergence points**: Multiple paths arriving at the same node edge within close proximity

**Why This Works:**
- Identifies visual clutter where paths merge
- Catches paths that are hard to distinguish
- Highlights areas needing offset routing for clarity

### Method 4: Routing Quality Analysis
Detects suboptimal path routing that could be improved for visual clarity.

**Algorithm:**
1. **Shared Start Points**: Check if multiple paths originate from the exact same coordinate
   - Example violation: UAT Tester → UAT PR and UAT Tester → Developer both starting at (890, 1180)
   - Fix: Offset one path to start from a different point on the same node edge

2. **Off-Center Connections**: For nodes with only one incoming/outgoing path on an edge, verify the connection is centered
   - Example violation: Path connecting to lower-left of a node instead of center-left
   - Fix: Adjust path endpoint to center of the edge

3. **Unnecessary Segments**: Check if paths use more segments than necessary
   - Example violation: 4-segment path when a 2-segment orthogonal path would work without crossings
   - Fix: Simplify the path to use the minimum number of segments

4. **Suboptimal Routes**: Check if shorter intersection-free routes exist
   - Example violation: Retro Report → Workflow Engineer going left-down-right instead of right-up-left
   - Fix: Reroute using the shorter valid alternative

**Why This Works:**
- Ensures visual consistency and professionalism
- Reduces clutter by minimizing unnecessary path complexity
- Improves readability by using the most direct valid routes

### Method 5: Visual Screenshot Analysis
Uses actual rendered output to catch visual issues that math might miss.

**Algorithm:**
1. Capture high-resolution screenshot of rendered diagram
2. Visually inspect for:
   - Lines crossing over each other
   - Paths obscuring node labels
   - Arrow markers colliding with nodes/paths
   - Color overlaps making paths indistinguishable
3. Document specific coordinates of visual crossings

**Why This Works:**
- Catches rendering artifacts (antialiasing, stroke width effects)
- Validates user-perceived quality
- Identifies issues in arrow markers and decorations
- Accounts for font rendering and text overlaps

## Systematic Detection Checklist

When detecting issues manually (without scripts), follow this checklist:

### Step 1: Build Node Inventory
Create a table of ALL nodes with their bounding boxes:
```
| Node Name | x-min | x-max | y-min | y-max |
|-----------|-------|-------|-------|-------|
| Developer | 780   | 1000  | 780   | 820   |
| Tech Writer | 490 | 710   | 960   | 1000  |
...
```

### Step 2: Parse Each Path into Segments
For each path, break down the `d` attribute into individual segments:
```
Path: "M 890 1180 L 550 1180 L 550 820 L 890 820"
Segments:
  1. Horizontal at y=1180: x from 890 to 550
  2. Vertical at x=550: y from 1180 to 820
  3. Horizontal at y=820: x from 550 to 890
```

### Step 3: Check EVERY Segment Against EVERY Node
For each segment, systematically check against all nodes:
- **Vertical segment at x=X, y from Y1 to Y2**: 
  - Does X fall within [node.x-min, node.x-max]?
  - Does [Y1, Y2] overlap with [node.y-min, node.y-max]?
  - If BOTH yes → **CROSSING DETECTED**
  
- **Horizontal segment at y=Y, x from X1 to X2**:
  - Does Y fall within [node.y-min, node.y-max]?
  - Does [X1, X2] overlap with [node.x-min, node.x-max]?
  - If BOTH yes → **CROSSING DETECTED**

### Step 4: Check Path Start/End Points
For each path, check if its start or end point is shared with other paths:
- Same exact coordinates = **SHARED ENDPOINT**
- Different paths arriving at same node edge within 5px = **CONVERGENCE**

### Step 5: Check Path-Path Intersections
For each pair of paths, check if their segments intersect:
- Two horizontal segments at same y with overlapping x-range = **OVERLAP**
- Two vertical segments at same x with overlapping y-range = **OVERLAP**
- Horizontal and vertical segments that cross = **CROSSING**

## Hard Rules

### Must
- **Build a complete node inventory FIRST** before analyzing any paths
- **Parse each path into individual line segments** - never analyze paths as single entities
- **Check EVERY segment against EVERY node** - a single path can cross multiple nodes
- Run all detection methods for thorough validation
- Report exact coordinates of intersection points
- Identify which paths AND which specific segments are involved in each crossing
- Calculate parametric intersection parameters (t, u values) for path-path crossings
- Test with actual SVG data from the diagram file
- Create visual annotations showing crossing locations
- **Report shared endpoints and overlapping path segments** as separate issues

### Must Not
- Rely on only one detection method
- Report endpoint connections as crossings
- Skip proximity analysis
- Ignore visual rendering validation
- **Treat a multi-segment path as a single line** - always decompose into segments
- **Stop after finding one crossing on a path** - continue checking remaining segments
- **Assume segment routing based on comments** - verify actual coordinates

## Testing Approach

### Test 1: Node Inventory Verification
Build the complete node inventory table and verify all nodes are captured.

### Test 2: Path Segment Decomposition
Decompose ALL paths into segments and verify segment count matches expected.

### Test 3: Systematic Segment-Node Checking
For each segment, check against ALL nodes (not just visually nearby ones).

### Test 4: Mathematical Verification
Run parametric line intersection detection on all path-path segment pairs.

### Test 5: Shared Point Detection
Check for paths sharing start/end points or overlapping segments.

### Test 6: Visual Inspection
Analyze rendered screenshot for visual crossing artifacts.

## Actions

### 1. Run Full Detection Suite

Execute the comprehensive Python detection script:
```bash
python3 .github/skills/detect-diagram-crossings/detect_crossings.py website/ai-workflow.html
```

This will:
- Parse SVG and extract all paths and nodes
- Decompose paths into individual line segments
- Run segment-by-segment node crossing detection
- Check path-path intersections
- Detect shared endpoints and overlapping segments
- Generate a detailed report with node inventory, path inventory, and issues

### 2. Run Extended Validation (Recommended)

Execute the JavaScript detection script for additional quality checks:
```bash
node .github/skills/detect-diagram-crossings/detect_all.js website/ai-workflow.html
```

This performs additional validation including:
- **Shared start points**: Multiple paths must not start at the same point of a node
- **Off-center connections**: If a path is the only connection to a node edge, it must connect at the center
- **Unnecessary segments**: Flags paths with more than 2 segments when a simpler 2-segment orthogonal path would work
- **Suboptimal routes**: Identifies paths that take longer routes when a shorter intersection-free alternative exists

**Note**: The JavaScript script requires Node.js and jsdom. Install dependencies with:
```bash
cd .github/skills/detect-diagram-crossings && npm install jsdom
```

### 3. Validate Fix

After modifying the diagram, re-run both detection scripts to confirm improvements:
```bash
python3 .github/skills/detect-diagram-crossings/detect_crossings.py website/ai-workflow.html
node .github/skills/detect-diagram-crossings/detect_all.js website/ai-workflow.html
```

Both scripts exit with:
- Exit code 0: No errors (warnings are OK for Python script)
- Exit code 1: Errors detected

## Detection Metrics

### Success Criteria
- ✅ **Zero mathematical crossings**: All parametric tests pass
- ✅ **Zero proximity issues**: No path segments through node bodies
- ✅ **Zero shared start points**: Each path starts from a unique point on a node
- ✅ **Zero segment overlaps**: No path segments overlap with other path segments
- ✅ **Centered single connections**: Paths connecting to nodes with no other connections use center of edge
- ✅ **Minimal segment paths**: No paths use more segments than necessary
- ✅ **Optimal routes**: No significantly shorter intersection-free alternatives exist
- ✅ **Clean visual rendering**: Screenshot confirms no visual crossings
- ✅ **All paths routed**: Every connection has a clear, non-crossing path

### Quality Thresholds
- **Excellent**: 0 crossings by all methods
- **Good**: 0 mathematical crossings, minor visual artifacts only
- **Fair**: 1-2 mathematical crossings in complex areas
- **Poor**: 3+ crossings or major visual overlaps
- **Unacceptable**: Multiple obvious crossings visible in screenshot

## Common Mistakes to Avoid

### Mistake 1: Incomplete Path Decomposition
**Wrong**: Checking only path endpoints or waypoints
**Right**: Parse `d` attribute into ALL individual line segments

### Mistake 2: Stopping Early
**Wrong**: Finding one crossing on a path and moving to next path
**Right**: Check ALL segments of the path against ALL nodes

### Mistake 3: Visual Proximity Assumption
**Wrong**: Assuming a path doesn't cross a node because they look far apart
**Right**: Mathematically verify segment coordinates against node bounds

### Mistake 4: Ignoring Multi-Node Crossings
**Wrong**: Reporting "path crosses Tech Writer" and stopping
**Right**: Continue checking - same path might also cross Documentation, UAT Tester, etc.

### Mistake 5: Missing Shared Points
**Wrong**: Only checking for geometric crossings
**Right**: Also check for paths sharing exact start/end coordinates

## Common Issues and Solutions

### Issue: False Positives at Endpoints
**Symptom**: Detections at valid node-to-node connections  
**Fix**: Increase endpoint tolerance from 0.01 to 0.05

### Issue: Missed Visual Crossings
**Symptom**: Math says no crossings but visually there are  
**Fix**: Check stroke width, arrow markers, and rendering artifacts

### Issue: Paths Too Close to Nodes
**Symptom**: Proximity warnings but no crossings  
**Fix**: Add routing margins, use wider node spacing

## Best Practices

1. **Test Early and Often**: Run detection after every layout change
2. **Use All Three Methods**: Don't rely on just mathematical analysis
3. **Document Findings**: Save screenshots and coordinate data
4. **Iterative Refinement**: Fix one crossing at a time, re-test after each fix
5. **Validate Visually**: Always check rendered output, not just data

## Example Output

```
CROSSING DETECTION REPORT
=========================

Method 1: Parametric Line Intersection
- Paths analyzed: 30
- Crossings detected: 0
- Status: ✅ PASS

Method 2: Node-Path Proximity  
- Nodes analyzed: 25
- Proximity issues: 0
- Status: ✅ PASS

Method 3: Shared Points Analysis
- Shared endpoints: 0
- Overlapping segments: 0
- Status: ✅ PASS

Method 4: Visual Screenshot Analysis
- Resolution: 1920x2000px
- Visual crossings: 0
- Status: ✅ PASS

OVERALL: ✅ NO CROSSINGS DETECTED
Diagram has a clean, crossing-free layout.
```

## Worked Example: UAT Rework Path Analysis

This example demonstrates the complete detection process for a problematic path.

### Input Path
```svg
<!-- UAT rework path -->
<path d="M 890 1180 L 550 1180 L 550 820 L 890 820" stroke="#ff6b6b" .../>
```

### Step 1: Decompose into Segments
| Segment | Type | Fixed Coord | Range |
|---------|------|-------------|-------|
| 1 | Horizontal | y=1180 | x: 550-890 |
| 2 | Vertical | x=550 | y: 820-1180 |
| 3 | Horizontal | y=820 | x: 550-890 |

### Step 2: Relevant Node Bounds
| Node | x-min | x-max | y-min | y-max |
|------|-------|-------|-------|-------|
| UAT Tester | 780 | 1000 | 1140 | 1180 |
| Tech Writer | 490 | 710 | 960 | 1000 |
| Documentation | 490 | 710 | 1050 | 1085 |
| Developer | 780 | 1000 | 780 | 820 |

### Step 3: Check Each Segment Against Each Node

**Segment 1** (Horizontal y=1180, x: 550-890):
- UAT Tester: y=1180 within [1140,1180]? YES (touches edge). x:[550,890] overlaps [780,1000]? YES → **CROSSING (edge)**
- Tech Writer: y=1180 within [960,1000]? NO → OK
- Documentation: y=1180 within [1050,1085]? NO → OK
- Developer: y=1180 within [780,820]? NO → OK

**Segment 2** (Vertical x=550, y: 820-1180):
- UAT Tester: x=550 within [780,1000]? NO → OK
- Tech Writer: x=550 within [490,710]? YES. y:[820,1180] overlaps [960,1000]? YES → **CROSSING**
- Documentation: x=550 within [490,710]? YES. y:[820,1180] overlaps [1050,1085]? YES → **CROSSING**
- Developer: x=550 within [780,1000]? NO → OK

**Segment 3** (Horizontal y=820, x: 550-890):
- UAT Tester: y=820 within [1140,1180]? NO → OK
- Tech Writer: y=820 within [960,1000]? NO → OK
- Documentation: y=820 within [1050,1085]? NO → OK
- Developer: y=820 within [780,820]? YES (touches edge). x:[550,890] overlaps [780,1000]? YES → **ENDPOINT (valid)**

### Step 4: Final Report for This Path
```
UAT Rework Path Crossings:
- Segment 1 (y=1180): Touches UAT Tester bottom edge at x=780-890 (start point)
- Segment 2 (x=550): CROSSES Tech Writer (y=960-1000)
- Segment 2 (x=550): CROSSES Documentation (y=1050-1085)
- Segment 3 (y=820): Ends at Developer node (valid endpoint)

ISSUES FOUND: 2 node crossings (Tech Writer, Documentation)
```
