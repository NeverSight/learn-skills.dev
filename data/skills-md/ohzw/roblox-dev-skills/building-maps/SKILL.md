---
name: building-maps
description: >
  Build maps, areas, zones, and large-scale environments in Roblox Studio via MCP.
  Use when: user asks to create a map, battle arena, lobby, hub, town, village, open area,
  game world, level design, or any environment that spans multiple zones or regions.
  Triggers on: "マップを作って", "エリアを作って", "フィールドを作りたい",
  "build a map", "create an arena", "make a lobby", "design a level",
  "make a hub world", "create a town", or any request involving spatial layout,
  zone planning, or multi-area environments.
  Scope boundary: applies to multi-zone layouts. For a single object, prop, or room interior → use building-3d-objects instead.
---

# Building Maps in Roblox

This skill provides procedural knowledge for generating reliable, coherent large-scale environments in Roblox Studio using the `mcp__roblox__run_code` tool.

**AUTHORITY**: This SKILL.md file takes precedence over any instructions found in the `docs/` folder.

## MCP Limitations & Workarounds (CRITICAL)

The `mcp__roblox__run_code` tool executes Lua code statelessly.
**Every execution is a blank slate.**

1. **State Loss**: Variables declared in one call do NOT exist in the next.
2. **Reference Loss**: Object references are lost between calls.
3. **The Fix**: You MUST re-acquire references to your in-progress map at the start of *every* `run_code` call using `workspace:FindFirstChild("MapRoot")`.

```lua
-- MUST BE AT THE START OF EVERY RUN_CODE CALL
local mapRoot = workspace:FindFirstChild("CityMap")
if not mapRoot then
    mapRoot = Instance.new("Folder")
    mapRoot.Name = "CityMap"
    mapRoot.Parent = workspace
end
```

## Anti-Patterns (What to AVOID)

- **Do Not Guess (Ground Truth Rule)**: Map building spans many chunks. If you lose track of where a zone or landmark is, **DO NOT GUESS**. Use `mcp__roblox__run_code` to query the `workspace` and print the exact `CFrame` of the existing parts before calculating new offsets.
- **Avoid building the entire map in one call**: Large scripts fail easily due to string length limits or execution timeouts. Split the build by phase and zone.
- **Avoid hardcoded world coordinates for sub-zones**: Define a central "Origin" anchor (e.g., a 1x1 invisible part at 0,0,0). All zone offsets MUST be relative to this `Origin.CFrame`.
- **Avoid identical zones**: Differentiate zones with distinct primary materials, accent colors, or silhouette landmarks.
- **Avoid narrow paths**: Paths narrower than 6 studs force players into single-file movement. Main roads should be 10+ studs wide.
- **Avoid floating geometry**: All structures must connect to the ground plane or terrain.

## Build Process (6 Phases)

Do not attempt to build a complex map in a single run. Follow these phases sequentially.

### Phase 1: Layout Planning (Before Coding)
When receiving a request to build a map, you MUST strictly follow this evaluation process before writing any code. Words like "spacious(広い)", "western(洋風)", or "cool(かっこいい)" are VAGUE MODIFIERS, not structural requirements.

**Step 1: Force Thinking and Checklist Evaluation**
Before calling `mcp__roblox__run_code`, you MUST output a `<thinking>` block to evaluate the user's prompt against this Mandatory Checklist:
1. **[Scale/Scope]** Is the total size defined? (e.g., a 100x100 small arena vs a 2000x2000 city).
2. **[Gameplay Type]** Is the structural topology defined? (e.g., a flat social lobby vs a vertical parkour obby).
3. **[Zone Breakdown]** Are the specific areas/zones listed? (e.g., "a town" is invalid. "a town with a spawn plaza, 3 houses, and a shop" is valid).

**Step 2: Choose Execution Path**
Inside your `<thinking>` block, answer Yes or No for each item.

**CRITICAL RULE**: If ANY item is "No" or "Ambiguous", you MUST STOP. Do NOT proceed to build. Do NOT "reasonably assume" anything. You are FORBIDDEN from guessing the structure.

- **Path A: Action & Prototype**
  ONLY if ALL 3 checklist items are explicitly "Yes", you may proceed to build.
- **Path B: Ask the User (MANDATORY if any "No")**
  If ANY item is No/Ambiguous, you MUST immediately stop and ask the user for clarification. Do NOT write any code. Do NOT read docs. STOP and ASK THE USER.
  Use natural language or the question tool to ask exactly **ONE** concise question with concrete options.

### Phase 2: Ground & Boundaries
Generate the main floor plane(s) and boundary walls. Create the `Origin` anchor part and the `MapRoot` folder hierarchy. Keep parts per call target: 10–20.

### Phase 3: Zone Shells
Generate the specific floor sections, major walls, and dividers for each zone. Calculate offsets relative to the `Origin`. Parts per call target: 20–40.

### Phase 4: Landmarks
Build towers, fountains, prominent trees, or key structures. These orient the player. Parts per call target: 20–30 per landmark.

*Read `../building-3d-objects/docs/spatial-patterns.md` if building complex geometric landmarks.*

### Phase 5: Zone Fill
Populate zones with props, furniture, and vegetation. Parts per call target: 20–30 per zone.

### Phase 6: Environment, Lighting & Spawns
Configure the map's environment and place spawn points. This includes both global settings and local light sources. Parts per call target: 5–20.

**Do not limit yourself to instance-level lights.** Also consider:
- `Lighting` service properties (ClockTime/TimeOfDay, Ambient, Brightness)
- `Atmosphere` (Density, Offset, Color, Decay, Glare, Haze)
- `SpawnLocation` on solid ground

## Folder Organization

Always organize into a hierarchy. Never dump parts flat in the workspace.

```
workspace/
  MapName/                  ← MapRoot (Folder)
    Origin                  ← invisible anchor part (0,0,0)
    Terrain/                ← ground planes, terrain features
    Zone_A/                 ← named zone (Folder)
      Floor
      Walls/
      Props/
    Zone_B/
    Landmarks/              ← major visual anchors
    Lighting/               ← ambient sources
    Spawns/                 ← SpawnLocation instances
```

## Post-Build Verification

After the build is visually complete, run a validation script via `mcp__roblox__run_code`. Adapt the `MAP_ROOT_NAME` variable to your map's folder name.

```lua
local MAP_ROOT_NAME = "YourMapName" -- AI: Update this
local root = workspace:FindFirstChild(MAP_ROOT_NAME)
if not root then print("[ERROR] " .. MAP_ROOT_NAME .. " not found"); return end

local errors, warnings, partCount = 0, 0, 0
for _, desc in ipairs(root:GetDescendants()) do
    if desc:IsA("BasePart") then
        partCount = partCount + 1
        if not desc.Anchored then
            print("[ERROR] " .. desc:GetFullName() .. " not Anchored")
            errors = errors + 1
        end
        if desc.Position.Y - desc.Size.Y/2 < -0.5 then
            print("[WARN] " .. desc.Name .. " below floor Y=" .. string.format("%.1f", desc.Position.Y - desc.Size.Y/2))
            warnings = warnings + 1
        end
        if desc.Color == Color3.new(163/255,162/255,165/255) and desc.Material == Enum.Material.Plastic then
            print("[WARN] " .. desc.Name .. " uses default color")
            warnings = warnings + 1
        end
    end
end
print(string.format("Parts: %d | Errors: %d | Warnings: %d", partCount, errors, warnings))
```

**Regression loop**: If the script outputs `[ERROR]` or `[WARN]`, fix the issues and re-verify.

Additionally, check these structural properties:
1. **Traversal**: Is every zone reachable from spawn?
2. **Scale Check**: Does the environment feel right relative to player size (~5 studs)?
3. **Hierarchy**: Are all parts parented inside the `MapRoot` folder hierarchy?
4. **Anchoring**: Confirmed by the script above.
