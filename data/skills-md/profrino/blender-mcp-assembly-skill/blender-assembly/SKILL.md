---
name: blender-assembly
description: "Use this skill whenever building, assembling, or creating any 3D model in Blender via MCP tools (mcp__blender__execute_blender_code). Covers all object types: furniture, vehicles, architecture, characters, props, mechanical parts, scenes. Trigger any time Blender Python code will create geometry with primitives, bmesh, or modifiers. Even simple objects benefit from correct primitive math and verification. Always invoke this skill before writing any Blender geometry code - it prevents the three most common geometry bugs that cause exploded-looking models."
---

# Blender Assembly Skill

This skill prevents geometry errors when building 3D models in Blender via MCP. It addresses three bugs that are easy to make and hard to spot until the model looks wrong:

1. **Cube size math** — `primitive_cube_add(size=1)` creates vertices at ±0.5, so `scale=0.4` gives half-extent 0.2, not 0.4. This silently halves every dimension, misplacing all connected parts.
2. **Euler rotation on cylinders** — rotating a cylinder to point in a direction using Euler angles frequently points it along the wrong axis due to XYZ rotation order.
3. **Invisible gaps** — parts placed "near" each other with no geometric overlap look exploded when rendered. Even a 5mm gap is visible at model scale.

## Phase 1: Connection Planning (before any code)

Create a **connection map** listing every joint before writing any geometry. This forces correct thinking about where parts touch.

For each joint, write:
- The two parts that connect
- Which face/edge of each meets the other
- The target overlap (minimum 0.005m / 5mm)

```
Connection Map:
  tabletop_bottom (Z=0.73) <-> leg_top (Z=0.74)     overlap: 0.01m on Z
  leg_bottom (Z=0.01)      <-> floor (Z=0.00)        sits on floor
  drawer_back              <-> desk_body_front        overlap: 0.01m on Y
```

Write this as a comment block in your first code cell, before any bpy calls.

## Phase 2: Geometry Creation Rules

### Rule 1: Always Use size=2 for Cube Primitives

A cube with `size=S` has vertices at `±S/2`. After `scale=K`, the half-extent is `K * S/2` — **not** `K`.

**Always use `size=2`.** With `size=2`, vertices are at ±1, so after `scale=K` the half-extent equals `K` directly. The math is transparent and the factor-of-2 error disappears.

```python
# CORRECT — size=2, scale = desired half-extent
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.75))
obj.scale = (0.60, 0.30, 0.02)   # box is 1.2m wide, 0.6m deep, 0.04m tall

# WRONG — size=1, scale misread as full extent
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.75))
obj.scale = (0.60, 0.30, 0.02)   # box is only 0.6m wide — half of intended!
```

Cylinders and spheres use `radius` which is already the actual radius — no conversion needed.

### Rule 2: Use bmesh for Directional Geometry — Never Rotate Cylinders

Never create a cylinder and rotate it to point in a direction. Euler rotation order (XYZ) makes this fail silently — the cylinder often ends up on the wrong axis.

For any geometry that must span from point A to point B (legs, beams, axles, supports, pipes, rails), **build it with bmesh using explicit vertex positions**:

```python
import bpy, bmesh, math

def make_beam(name, start, end, hw=0.012, hh=0.010):
    """Build a rectangular beam from start to end — no rotations needed."""
    dx, dy, dz = end[0]-start[0], end[1]-start[1], end[2]-start[2]
    L = math.sqrt(dx*dx + dy*dy + dz*dz)
    if L < 1e-6:
        return None
    fx, fy, fz = dx/L, dy/L, dz/L
    # Right vector (cross forward with world-up; fallback to world-X if beam is vertical)
    ux, uy, uz = (0,0,1) if abs(fz) < 0.99 else (1,0,0)
    rx = fy*uz-fz*uy; ry = fz*ux-fx*uz; rz = fx*uy-fy*ux
    rL = math.sqrt(rx*rx+ry*ry+rz*rz); rx,ry,rz = rx/rL,ry/rL,rz/rL
    upx = ry*fz-rz*fy; upy = rz*fx-rx*fz; upz = rx*fy-ry*fx

    mesh = bpy.data.meshes.new(name)
    obj  = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bm = bmesh.new()
    verts = []
    for base in [start, end]:
        for sx, sy in [(-1,-1),(1,-1),(1,1),(-1,1)]:
            verts.append(bm.verts.new((
                base[0]+rx*hw*sx+upx*hh*sy,
                base[1]+ry*hw*sx+upy*hh*sy,
                base[2]+rz*hw*sx+upz*hh*sy,
            )))
    v = verts
    for f in [(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(0,3,2,1),(4,5,6,7)]:
        bm.faces.new([v[i] for i in f])
    bm.to_mesh(mesh); bm.free()
    return obj
```

Use for: chair/table legs, beams, axles, pipes, frame members, railings, any angled strut.
Skip for: vertical posts, wheels, hubs — anything aligned with a world axis where no rotation is needed.

### Rule 3: Always Call transform_apply Immediately After Setting Scale

When creating objects in a loop, `bpy.context.active_object` can silently reference the wrong object by the end of the loop, causing a scale assignment to fail or apply to the wrong mesh. Call `transform_apply` immediately after every scale assignment — inside the loop, before anything else:

```python
# CORRECT
bpy.ops.mesh.primitive_cube_add(size=2, location=(x, y, z))
obj = bpy.context.active_object
obj.name = name
obj.scale = (sx, sy, sz)
bpy.ops.object.transform_apply(scale=True)   # ← immediately, inside the loop

# WRONG — scale may silently not apply
obj.scale = (sx, sy, sz)
# ... more operations ...
bpy.ops.object.transform_apply(scale=True)   # too late; active_object may have changed
```

### Rule 4: Derive Spanning Dimensions from Verified Neighbour Bounds

Never hardcode a dimension for a part that must reach between two existing parts. Hardcoded values drift from actual geometry. Instead, call `verify_bounds()` on both neighbours and compute the required size from their real extents:

```python
# CORRECT — measure first, then size the new part
b_a = verify_bounds("Part_A")
b_b = verify_bounds("Part_B")
half_span = (b_b['x'][1] - b_a['x'][0]) / 2   # actual half-width needed to bridge A and B

# WRONG — dimension set independently of actual neighbour positions
half_span = 0.28   # guessed; will be wrong if neighbours shifted even slightly
```

Apply this rule whenever one part must cover, fill, or connect two others on any axis. Always measure the gap from real bounds; never guess.

### Rule 5: Compensate for Subsurf Shrinkage

Subdivision surface modifiers pull geometry inward. A box spanning 0.0–0.30m may only reach 0.26m after level-2 subsurf.

**Extend geometry 10–15% past the target boundary** before applying subsurf, then verify:

```python
target_reach = 0.28
build_to     = target_reach * 1.13   # 13% longer to compensate for shrinkage
```

Alternative: use bevel modifier instead of subsurf for structural parts — it adds smooth edges without shrinking the shape.

## Phase 3: Verify After Every Part

Call these helpers after creating each part. Catching a gap immediately is far cheaper than debugging an exploded model later.

```python
def verify_bounds(name):
    """Print and return world-space bounding box."""
    obj = bpy.data.objects[name]
    vs  = [obj.matrix_world @ v.co for v in obj.data.vertices]
    b = {
        'x': (min(v.x for v in vs), max(v.x for v in vs)),
        'y': (min(v.y for v in vs), max(v.y for v in vs)),
        'z': (min(v.z for v in vs), max(v.z for v in vs)),
    }
    print(f"{name}: X[{b['x'][0]:.4f},{b['x'][1]:.4f}]"
          f" Y[{b['y'][0]:.4f},{b['y'][1]:.4f}]"
          f" Z[{b['z'][0]:.4f},{b['z'][1]:.4f}]")
    return b

def verify_overlap(name_a, name_b, axis='z', min_overlap=0.005):
    """Confirm two parts physically overlap on the given axis."""
    a = verify_bounds(name_a)
    b = verify_bounds(name_b)
    overlap = min(a[axis][1], b[axis][1]) - max(a[axis][0], b[axis][0])
    ok = overlap >= min_overlap
    print(f"  {name_a} <-> {name_b} [{axis.upper()}]: "
          f"{'OK' if ok else 'GAP WARNING'} ({overlap:.4f}m)")
    return overlap
```

Run `verify_overlap` for **every joint** in your connection map before moving to the next part. If it shows a gap, fix the position before continuing.

## Phase 4: Finalization

Apply to every mesh object:

```python
def finalize(name):
    """Apply transforms, set origin to geometry, shade smooth for the named object."""
    obj = bpy.data.objects[name]
    bpy.ops.object.select_all(action='DESELECT')   # scope the ops below to `obj` only
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.ops.object.shade_smooth()
    bpy.ops.object.select_all(action='DESELECT')
    return obj

def audit_all():
    """Final check — all parts should have rotation (0,0,0) and scale (1,1,1)."""
    meshes = sorted([o for o in bpy.data.objects if o.type == 'MESH'], key=lambda o: o.name)
    all_ok = True
    for obj in meshes:
        rot = tuple(round(c, 3) for c in obj.rotation_euler)
        scl = tuple(round(c, 3) for c in obj.scale)
        ok  = rot == (0.0,0.0,0.0) and scl == (1.0,1.0,1.0)
        if not ok: all_ok = False
        print(f"  [{'OK' if ok else '!!'}] {obj.name:30s} rot={rot} scl={scl}")
    print(f"\nAll transforms clean: {all_ok}")
    return all_ok
```

## Workflow Checklist

Every Blender model, every time:

1. **Plan connections** — write the connection map first, before any bpy code
2. **Use `size=2`** for all cube primitives — scale = actual half-extent directly
3. **Use `make_beam()`** for any geometry pointing from A to B — no Euler rotations
4. **`transform_apply(scale=True)` inside every loop** — call it immediately after `obj.scale = (...)`, never outside the loop
5. **Derive spanning dimensions from `verify_bounds()`** — never hardcode a size that must match a neighbour; measure the actual extent and compute from it
6. **Overshoot subsurf** — extend 10–15% past target; verify bounds after apply
7. **`verify_bounds()`** — print world-space extents after every single part
8. **`verify_overlap()`** — check every joint; fix gaps before moving on
9. **`finalize()`** — apply transforms, set origin, shade smooth on every part
10. **`audit_all()`** — confirm rotation=0 and scale=1 across the whole scene
