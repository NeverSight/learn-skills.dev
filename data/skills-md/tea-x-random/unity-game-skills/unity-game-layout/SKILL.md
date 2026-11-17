---
name: unity-game-layout
description: "Lay out Unity boards and grids so logical cells, rendered tiles, pieces and input picking agree. Use when pieces miss tiles, sprites span cells incorrectly, taps select the wrong cell, isometric/perspective boards misalign, sorting is wrong, or mobile framing must adapt to aspect ratio and safe area. Covers grid→world→screen transforms and inverses, center/foot pivots, depth/Y sorting, Grid/Tilemap APIs, GetCellCenterWorld/CellToWorld/WorldToCell, ScreenToWorldPoint/ScreenPointToRay, orthographic/isometric/faux-perspective cameras, PPU consistency, cell picking, 2.5D layout and responsive fit."
---

# Unity Game Layout (coordinate systems & boards)

Most "the board looks broken / pieces float off their tiles / taps hit the wrong cell" bugs are ONE
bug wearing different masks: **the logical grid, the rendered grid, the placement math, and the picking
math each compute "where is cell (x,y)" slightly differently.** Fix that and all the masks fall off.

## The one rule: a single source of truth for the grid

Define **exactly one** function `CellToWorld(cell) -> worldCenter` and derive EVERYTHING from it:
the drawn grid lines, every piece's position, and the inverse used for input. Never hand-place the grid
lines with one set of numbers and the pieces with another — that divergence is the #1 cause of
misalignment. If you render a grid AND place pieces, both must call the same mapping.

> Validation gate (do this BEFORE building gameplay on the board): place a tiny marker dot at
> `CellToWorld(c)` for **every** cell, render the grid from the same function, screenshot, and confirm
> each dot sits dead-center in its cell. If they don't coincide, the mapping is wrong — stop and fix it
> before adding pieces, animation, or input. (This is the layout analogue of the solver-gate: prove the
> coordinate system before you build on it.)

## Grid space → world space → screen space (and back)

Three spaces, two conversions each way:

- **Grid space**: integer `(col, row)` cell indices. The game logic lives here.
- **World space**: Unity units. `CellToWorld(cell)` returns the cell's **center** in world.
- **Screen space**: pixels. The camera converts world↔screen.

**Forward (place a piece):** `cell → CellToWorld → world`, then assign `transform.position` (with the
anchor offset below). The camera handles world→screen.

**Inverse (which cell did the player tap?):** `screenPoint → world → WorldToCell → cell`. Do the inverse
of *the exact same* transform — never approximate by "nearest cell center," which drifts on non-uniform
(perspective/iso) boards.

### Unity Tilemap/Grid APIs — the corner-vs-center trap

If you use Unity's `Grid`/`Tilemap`, the API names are a notorious footgun (this was our exact bug):

- `Tilemap.GetCellCenterWorld(Vector3Int)` → the cell **center** in world. **This is the value you want
  to place a piece on a cell.** [1]
- `GridLayout.CellToWorld(...)` → the cell's **lower-left CORNER**, not its center. Placing a piece with
  `CellToWorld` leaves it offset by half a cell. [1]
- `GridLayout.WorldToCell(worldPos)` → the cell index containing a world point — the canonical
  world→cell step for picking (run `ScreenToWorldPoint` first). [1]

Rolling your own mapping (no Tilemap)? Make `CellToWorld` return the **center** directly, e.g. for a
plain orthographic board: `world = origin + new Vector2((col + 0.5f) * cellW, (row + 0.5f) * cellH)`.
The `+0.5` is the difference between corner and center — forget it and every piece sits on a grid line.

## Cell anchoring: center vs foot/pivot (why pieces "float")

A piece's **logical** position is the cell center, but you rarely want the sprite's *center* there —
a standing character/cone/goal should look like its **base sits on the cell**. Two clean options, pick
ONE and be consistent:

1. **Foot/pivot anchor (recommended for characters & props).** Author the sprite with its **pivot at
   the base** (feet / bottom-center), then set `transform.position = CellToWorld(cell)` directly — the
   pivot makes the base land on the cell center and the body extend upward. Isometric tile art does the
   same: a custom pivot at the center of the tile's 3D floor so the sprite's 3D sides extend below the
   grid cell. [2][5]
2. **Center anchor (flat tokens: gems, dots, balls).** Pivot at center, position at `CellToWorld(cell)`.

The bug to avoid — **manually nudging a center-pivot sprite "up by half its height"** so its bottom
hits the cell center. That couples the visual offset to the sprite's pixel height, so taller sprites
float higher and overlap the row behind, and it desynchronizes from picking (which still uses the cell
center). **Don't offset in code — bake the anchor into the sprite pivot.** Set the sprite's pivot once;
let `CellToWorld` be the only position math.

A multi-cell prop (a goal, a 2×1 building) must still be **anchored to a specific cell** (e.g. its
footprint origin) via `CellToWorld`, then sized in cell units — never hand-placed with a magic UV.

## Depth / Y-sorting for overlapping sprites

On any board where sprites overlap (iso, 2.5D, foot-anchored top-down), draw far/back sprites first:

- **Global, cleanest:** Project Settings → Graphics (or the URP 2D Renderer) → **Transparency Sort
  Mode = Custom Axis**, **Transparency Sort Axis = (0, 1, 0)** so lower-on-screen = in-front. For an
  Isometric **Z-as-Y** tilemap use **(0, 1, −0.26)** instead (the −0.26 biases higher-Z tiles to draw
  first). [3][4]
- **Per-sprite fallback:** `sortingOrder = -(int)(transform.position.y * k)` — higher Y ⇒ drawn behind.
- Set the SpriteRenderer **Sort Point = Pivot** (not Center) so foot-anchored sprites sort by their
  base; for tilemaps set Tilemap Renderer **Mode = Individual** so per-tile sprites sort. [3][4]
- Sort by the **pivot/foot**, consistent with the foot-anchor above — sorting by center makes tall
  sprites pop in front of things they're behind.

## Board types

- **Orthographic (square top-down):** `CellToWorld = origin + (col+0.5, row+0.5) * cellSize`. Inverse:
  `floor((world - origin)/cellSize)`. Picking via `Camera.ScreenToWorldPoint` then that inverse. [6]
- **Isometric / 2.5D (diamond):** forward `screen.x = (col − row) * (tileW/2)`,
  `screen.y = (col + row) * (tileH/2)`; default iso cell ratio is **2:1** (cellSize y = floorHeightPx /
  tileWidthPx, e.g. (1, 0.5)). Invert those two equations for picking — do NOT nearest-center. [4][7]
- **Faux-perspective / trapezoid (our soccer board):** define the 4 corners and map a cell via
  **bilinear interpolation**: `top = lerp(TL,TR,u); bot = lerp(BL,BR,u); world = lerp(top,bot,v)` with
  `u=(col+0.5)/cols, v=(row+0.5)/rows`. **Critical:** picking must **invert the bilinear map** (solve
  for u,v), or at minimum iterate cells and pick the nearest *center under the same map* — a naive
  screen-distance nearest-center skews near the far (narrow) edge where cells are small. The rendered
  grid lines must be drawn from the SAME corner interpolation. (Unity's Tilemap has no trapezoid mode,
  so this is custom — which makes the single-source-of-truth rule even more important.)

## Pixels-per-unit (PPU) consistency

Mismatched PPU is a silent scale bug: if the ground/tile art imports at one PPU and the piece sprites at
another, pieces are the wrong size relative to cells no matter how good the mapping is. **The project PPU
is READ, never picked:** the SSOT is `art-spec.yaml:craft.pixels_per_unit` (unity-art-direction); if no
art-spec exists yet, fall back to `asset-contract.yaml:runtime.pixels_per_unit` (unity-asset-pipeline),
which must be uniform across the registry. Never pick a local/hardcoded PPU value — one game = one PPU
(one pixel density, no mixels). Import all gameplay sprites at it and size the camera/cells around it.
Size a piece to **cell units** (e.g. "1.2 cells tall") computed from `CellToWorld`, not from raw pixels.

## Input picking, end to end

- **2D / orthographic:** `world = cam.ScreenToWorldPoint(screenPoint)` (z = distance to the board
  plane), then `cell = WorldToCell(world)` (or your analytic inverse). [8]
- **3D / perspective:** build a ray `cam.ScreenPointToRay(screenPoint)` and intersect the **ground
  plane** (`Physics.Raycast` against a ground collider, or `Plane.Raycast` for a math plane), then
  `WorldToCell(hit)`. In perspective you MUST ray-cast — screen distance to a piece is not depth. [9]
- Whatever the board, **picking inverts the same transform placement used** — that guarantees tap-cell
  == shown-cell.

## Camera framing & responsive (mobile) layout

- **Orthographic fit:** `orthographicSize = halfHeightWorld`; visible width = `size * 2 * camera.aspect`.
  To fit a fixed board to varying aspect ratios, compute `orthographicSize` from BOTH the board's world
  width/height and the screen aspect (use the larger of height-fit and width-fit so the board never
  crops), or letterbox. Don't hard-code a size for one device. [10]
- **Safe area (notch/home-indicator):** anchor HUD inside `Screen.safeArea` (a pixel Rect) — convert to
  anchors on a full-screen RectTransform so buttons/labels avoid the notch. [11]
- **World board vs UI HUD:** the board lives in world space (camera-framed); the HUD lives on a Canvas
  with `CanvasScaler = Scale With Screen Size` + a reference resolution + match. Keep them separate;
  don't anchor world pieces to UI or vice-versa. [12]

## Failure modes (the masks of the one bug)

- **Corner vs center:** placed with `CellToWorld`/forgot `+0.5` ⇒ everything half-a-cell off. [1]
- **Foot-anchor vs cell-center confusion:** nudging a center-pivot sprite up by half its height in code
  ⇒ tall pieces float and overlap the next row, and picking desyncs. Fix: bake pivot, don't offset.
- **Rendered grid ≠ placement math:** grid lines and pieces use different numbers ⇒ drift. One mapping.
- **Perspective/iso picking by nearest-center:** ignores the projection ⇒ wrong cell near far edge.
  Invert the actual transform / raycast.
- **PPU mismatch** between ground and pieces ⇒ pieces wrong size vs cells.
- **Multi-cell prop placed by a magic UV** instead of an anchored footprint ⇒ spans/overlaps cells.

## Checklist (gate before gameplay)

- [ ] One `CellToWorld(cell) -> center` function; grid lines, pieces, and picking all use it.
- [ ] Picking is the exact inverse (WorldToCell / invert bilinear / raycast) — not nearest-center.
- [ ] Anchor decided once (foot-pivot for actors, center for tokens) and **baked into sprite pivots**,
      not coded as a height offset.
- [ ] Sort Point = Pivot; Transparency Sort Axis (0,1,0) [or iso (0,1,−0.26)]; tilemap Mode Individual.
- [ ] All gameplay sprites at the project PPU read from `art-spec.yaml:craft.pixels_per_unit` (contract
      fallback); pieces sized in cell units.
- [ ] Alignment validated: a marker in every cell sits dead-center on the drawn grid (screenshot).
- [ ] Camera fits the board across aspect ratios; HUD inside `Screen.safeArea`.

## Sources

[1] Unity — Tilemap.GetCellCenterWorld / CellToWorld / WorldToCell (Scripting API). GetCellCenterWorld =
cell center; CellToWorld = lower-left corner; WorldToCell = world→cell. (3-0 verified)
[2] Unity — Create an isometric tilemap: custom Pivot at the center of the tile's 3D floor. (3-0)
[3] Unity — Sort sprites with a custom sorting axis: Tilemap Renderer Mode=Individual; Transparency Sort
Mode=Custom Axis; iso axis (0,1,−0.26). (3-0)
[4] Unity Blog — Isometric 2D environments with Tilemap: iso uses 2D sprites + renderer sort; Z-as-Y +
sort axis fakes stacking; default 2:1 cell. (3-0)
[5] Unity — Create isometric tilemap: Transparency Sort Axis (0,1,0) renders higher tiles behind. (3-0)
[6] techarthub — Unity coordinate system practical guide.
[7] clintbellanger — Isometric tiles math: `screen.x=(map.x−map.y)*W/2; screen.y=(map.x+map.y)*H/2` and
its inverse; also habrador "stuff on a grid". 
[8] Unity — Camera.ScreenToWorldPoint (screen→world); gamedevbeginner mouse-to-world (2D+3D).
[9] Unity — Camera.ScreenPointToRay + CameraRays manual; raycast a ground plane for perspective picking.
[10] Unity Discussions — orthographicSize vs aspect ratio for fitting a 2D board.
[11] Unity — Screen.safeArea; "wrap your UI inside the safe area".
[12] Unity — UI multi-resolution (CanvasScaler Scale With Screen Size).
