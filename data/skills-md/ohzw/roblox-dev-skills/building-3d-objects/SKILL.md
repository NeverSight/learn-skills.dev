---
name: building-3d-objects
description: >
  Build 3D objects, props, and room-scale structures in Roblox Studio via MCP.
  Use when: user asks to create, build, or place a single physical object —
  furniture, animals, vehicles, gates, towers, decorations, street props,
  room interiors, or any individual tangible structure.
  Triggers on: "○○を作って", "○○を置いて", "build me a ___", "create a ___",
  "make a ___" in the context of Roblox Studio.
  Also use when user mentions CSG, Union, Subtract, Part placement, or 3D modeling
  in Roblox. If the user is in a Roblox project and asks to "make" or "build"
  something physical, this skill should trigger even without explicit mention of
  "3D" or "Roblox".
  Scope boundary: applies if the result can be grouped into a single `Model`.
  For full maps, arenas, lobbies, hubs, or multi-zone environments → use building-maps instead.
  Dispatch rule: When the user requests multiple related/variant objects
  (e.g., "5 types of swords", "3 chair styles"), dispatch ALL variants to
  a SINGLE agent. Do NOT spawn parallel agents. Consistency requires
  sequential building by one agent.
---

# Building 3D Objects in Roblox

This skill provides procedural knowledge for generating reliable, high-quality 3D objects in Roblox Studio using the `mcp__roblox__run_code` tool.

**AUTHORITY**: This SKILL.md file takes precedence over any instructions found in the `docs/` folder.

## MCP Limitations & Workarounds (CRITICAL)

The `mcp__roblox__run_code` tool executes Lua code statelessly.
**Every execution is a blank slate.**

1. **State Loss**: Variables declared in one call do NOT exist in the next.
2. **Reference Loss**: Object references are lost between calls.
3. **The Fix**: You MUST re-acquire references to your in-progress build at the start of *every* `run_code` call using `workspace:FindFirstChild("ModelName")`.

```lua
-- MUST BE AT THE START OF EVERY RUN_CODE CALL
local model = workspace:FindFirstChild("MyDesk")
if not model then
    model = Instance.new("Model")
    model.Name = "MyDesk"
    model.Parent = workspace
end
```

## Anti-Patterns (What to AVOID)

- **Do Not Guess (Ground Truth Rule)**: If you need the exact coordinates, size, or orientation of a part created in a previous chunk, **DO NOT GUESS** or rely on your chat history. Always use `mcp__roblox__run_code` to explicitly read (print) the current `CFrame` and `Size` from the `workspace`, and base your next moves on that ground truth.
- **Avoid unanchored parts**: `Anchored` defaults to `false`. Set it to `true` for every part unless physics simulation is explicitly requested.
- **Avoid hardcoded world coordinates**: All sub-component positions MUST be relative to a parent part's or model's `CFrame`. Hardcoded coordinates break when the model is moved.
- **Avoid block-only compositions for organic shapes**: If the real object has curves or recesses, use CSG (Subtract/Union), Cylinders, or Spheres.
- **Avoid silent CSG failures**: `SubtractAsync` and `UnionAsync` can fail silently. Always wrap in `pcall` and verify the result is a `BasePart`.

## Build Process (4 Phases)

Follow these phases sequentially. Do not attempt to build a complex object in a single run.

### Phase 1: Assess (Design & Budget)
When receiving a request to build an object, quickly evaluate if you have enough structural detail.

**Quick Check:**
- Do you know the specific components/parts to build? (Not just "kitchen" but "counter, sink, stove, island")  
- Do you know the approximate scale? (Player-sized? Miniature? Room-scale?)
- Do you know if it's static or has moving parts?

**Decision:**
- **If YES to all**: Proceed to Phase 2. Make reasonable assumptions for colors and minor details.
- **If NO to any**: STOP. Tell the user: "I need more details to build this properly. Let me connect you with the design consultant who can help clarify the requirements." Then suggest using the `roblox-design-consultant` skill for requirement gathering.

### Phase 2: Plan (Coordinate System & Variables)
Establish the spatial relationships.

**Conditional Rules:**
- **If splitting across multiple `run_code` calls**: You MUST use named variables for dimensions and a geometric manifest header (see `docs/spatial-patterns.md`).
- **If part count > 5**: Snap dimensions to a consistent grid (e.g., 0.1 or 0.5 studs) to avoid floating-point drift.

*Read `docs/spatial-patterns.md` now if either condition applies.*

### Phase 3: Build (Geometry & CSG)
Generate the parts.

**CSG Rules:**
- Apply an `EPSILON` (e.g., 0.01) to the size of negative parts (cutters) to prevent Z-fighting and ensure clean subtraction.
- Copy the full `CFrame` from the base part to the resulting CSG part. `CFrame.new(pos)` resets rotation.
- Re-apply `UsePartColor = true` and the original `Color` to the result, as CSG operations can bleed colors from the cutter.

*Read `docs/csg-patterns.md` now if your build requires curves, holes, or hollow spaces.*

### Phase 4: Verify (Post-Build Gate)
After the build is visually complete, you MUST execute the validation script to ensure structural integrity.

1. Read the contents of `scripts/validate.luau`.
2. Adapt the `TARGET_MODEL_NAME` variable.
3. Execute the script via `run_code`.
4. **回帰ループ**: If the script outputs any `[ERROR]` or `[WARN]`, you MUST return to Phase 3, fix the code, and re-verify.

## Supplementary Documentation

Read these files only when the specific phase or condition triggers them.

| File | When to Read |
|------|--------------|
| `docs/spatial-patterns.md` | Phase 2: Multi-call builds or >5 parts |
| `docs/csg-patterns.md` | Phase 3: Using SubtractAsync or UnionAsync |
| `docs/platform-rules.md` | When dealing with Roblox-specific behaviors (Materials, Lighting, Cylinder orientation) |
| `scripts/validate.luau` | Phase 4: Mandatory post-build verification |
