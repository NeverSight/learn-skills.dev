---
name: roblox-world-building
description: Building worlds with code - parts, models and pivots, materials, Lighting (LightingStyle, Atmosphere, post-processing), day/night, Terrain API, in-game CSG and destruction (GeometryService Subtract/Union/Fragment), ProceduralModel, EditableMesh/EditableImage, particles/beams/trails/highlights. Use when creating maps, environments, lighting, destructible objects, procedural levels, or visual effects.
---

# World building with code

## Parts and models

```luau
--!strict
local function makePart(size: Vector3, cframe: CFrame, props: { [string]: any }?): Part
	local part = Instance.new("Part")
	part.Anchored = true
	part.Size = size
	part.CFrame = cframe
	part.TopSurface = Enum.SurfaceType.Smooth
	part.BottomSurface = Enum.SurfaceType.Smooth
	for key, value in props or {} do
		(part :: any)[key] = value
	end
	return part -- caller sets Parent last
end

local floor = makePart(Vector3.new(64, 1, 64), CFrame.new(0, 0, 0), {
	Material = Enum.Material.Slate,
	Color = Color3.fromRGB(90, 90, 100),
})
local model = Instance.new("Model")
model.Name = "Arena"
floor.Parent = model
model.WorldPivot = floor.CFrame
model.Parent = workspace
model:PivotTo(CFrame.new(0, 10, 0) * CFrame.Angles(0, math.rad(45), 0))
```

- Set properties first, **parent last** (one replication/physics insert). Anchor static geometry.
- Move/rotate models with `PivotTo`/`GetPivot`; `Model.WorldPivot` / `PrimaryPart` define the pivot.
- Group logically related parts in Models (streaming, LOD, `ModelStreamingMode`), not giant containers.
- Decorative parts: `CanCollide/CanTouch/CanQuery = false`, `CastShadow = false` for tiny details.
- Materials: `Enum.Material.*`; custom looks via `MaterialVariant` in `MaterialService` (set
  `part.MaterialVariant = "Name"`) or `SurfaceAppearance` on MeshParts (PBR). `Decal.Texture` is
  superseded by `ColorMapContent`.
- Many identical meshes are cheap (instanced); many unique meshes/unions are not.

## Lighting

| Property | Guidance |
| --- | --- |
| `Lighting.LightingStyle` | `Realistic` (naturalistic) or `Soft` (stylized). Replaces the superseded `Lighting.Technology`. |
| `Lighting.PrioritizeLightingQuality` | Prefer quality (e.g. shadow maps with Soft) vs performance on lower-end devices. |
| `ClockTime` / `GeographicLatitude` | Sun position; animate `ClockTime` for day/night. |
| `Brightness`, `ExposureCompensation`, `Ambient`/`OutdoorAmbient` | Overall exposure and fill light. |
| `EnvironmentDiffuseScale`/`EnvironmentSpecularScale` | Skybox contribution to lighting and reflections. |
| Children | `Atmosphere` (haze/density, replaces fog), `Sky`, `Clouds` (in Terrain), `BloomEffect`, `ColorCorrectionEffect`, `ColorGradingEffect`, `DepthOfFieldEffect`, `SunRaysEffect`, `BlurEffect`. |

```luau
--!strict
-- Server: smooth day/night cycle (one full day every 20 minutes).
local Lighting = game:GetService("Lighting")
local RunService = game:GetService("RunService")

local DAY_LENGTH_SECONDS = 20 * 60

RunService.Heartbeat:Connect(function(deltaTime)
	Lighting.ClockTime = (Lighting.ClockTime + deltaTime * 24 / DAY_LENGTH_SECONDS) % 24
end)
```

For per-frame visual changes, prefer computing `ClockTime` on each client from
`workspace:GetServerTimeNow()` (no replication traffic, perfectly smooth). Local lights: `PointLight`,
`SpotLight`, `SurfaceLight` — few with `Shadows = true`.

## Terrain

```luau
--!strict
local terrain = workspace.Terrain

terrain:FillBlock(CFrame.new(0, -10, 0), Vector3.new(512, 20, 512), Enum.Material.Grass)
terrain:FillBall(Vector3.new(0, 0, 0), 24, Enum.Material.Air) -- carve a crater
terrain:FillBlock(CFrame.new(40, -2, 0), Vector3.new(30, 4, 30), Enum.Material.Water)
terrain:FillCylinder(CFrame.new(-40, 5, 0), 20, 8, Enum.Material.Rock)
```

- Bulk generation: build a `Region3` (aligned with `:ExpandToGrid(4)`) and use `ReadVoxels`/`WriteVoxels`
  with materials/occupancy arrays (4-stud voxels), in chunks, yielding between chunks.
- `terrain:Clear()`; water look via `Terrain.WaterColor`, `WaterWaveSize`, etc.
- Procedural heightmaps: sample `math.noise(x * scale, z * scale, seed)` with octaves; use a `Random.new(seed)`
  for deterministic worlds; generate on the server or use Parallel Luau for heavy math.

## In-game solid modeling and destruction (GeometryService)

```luau
--!strict
local GeometryService = game:GetService("GeometryService")

-- Punch a hole through a wall (e.g. explosions, building games).
local function carve(wall: BasePart, cutter: BasePart): { Instance }?
	local ok, results = pcall(function()
		return GeometryService:SubtractAsync(wall, { cutter }, {
			CollisionFidelity = Enum.CollisionFidelity.Default,
			RenderFidelity = Enum.RenderFidelity.Automatic,
			SplitApart = true, -- disconnected pieces become separate parts
		})
	end)
	if not ok or not results then
		return nil
	end
	for _, piece in results do
		if piece:IsA("BasePart") then
			piece.Anchored = wall.Anchored
			piece.Parent = wall.Parent
		end
	end
	wall:Destroy()
	return results
end

return carve
```

- `UnionAsync`, `IntersectAsync`, `SubtractAsync` return new unparented parts; `FragmentAsync(part, sites)`
  shatters a part (Voronoi) using points from `GenerateFragmentSites`; `SweepPartAsync` extrudes a part
  along CFrames; `CalculateConstraintsToPreserve` keeps welds/constraints when replacing parts.
- Operations are expensive: run on the server, rate-limit, and pool/clean up fragments.

## ProceduralModel (parameter-driven models)

`ProceduralModel` instances regenerate their contents from a **generator ModuleScript** exposing
`Attributes` (parameters) and `OnGenerate(params, targetContainer)`; works at edit time (undo/redo,
Team Create) and runtime. Generate from Studio, Assistant, or the Studio MCP (`generate_procedural_model`).
Creator Store procedural models are sandboxed automatically.

## Runtime meshes and images

`AssetService:CreateEditableMesh()` / `CreateEditableMeshAsync(content)` and `CreateEditableImage` enable
runtime geometry and pixel editing (deformable terrain chunks, painting, custom avatars). Published games
require the owner to be ID + 13+ verified and **Enable Mesh / Image APIs** in Creator Dashboard; strict
client memory budgets apply; only assets owned by/shared with the game owner can be loaded. Display via
`AssetService:CreateMeshPartAsync(Content.fromObject(editableMesh))`.

## Effects

- `ParticleEmitter` (use `:Emit(n)` for bursts), `Beam` (between attachments; lasers, ropes), `Trail`
  (swords, projectiles), `Highlight` (outline/fill; limited count), `Explosion` (sets off physics —
  set `DestroyJointRadiusPercent = 0` and `BlastPressure = 0` for visual-only).
- Spawn cosmetic effects on clients; destroy or pool them (`Debris:AddItem(obj, seconds)` is fine).

## Related skills

`roblox-performance` (rendering cost, streaming), `roblox-architecture` (streaming settings),
`roblox-studio-mcp` (build in Studio through MCP), `roblox-physics` (constraints, destruction physics).
