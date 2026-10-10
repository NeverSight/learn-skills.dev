---
name: roblox-physics
description: Physics and spatial queries - Raycast/Blockcast/Spherecast, overlap queries, collision groups, Touched pitfalls, assemblies and welds, mover constraints replacing BodyMovers, mechanical constraints, network ownership, CFrame math, vehicles/projectiles, and server authority (BindToSimulation, prediction, rollback). Use when moving parts, detecting hits, building vehicles or projectiles, or fixing jitter, flinging, or ownership bugs.
---

# Roblox physics and spatial queries

## Spatial queries (use these, not Touched, for gameplay decisions)

```luau
--!strict
local params = RaycastParams.new()
params.FilterType = Enum.RaycastFilterType.Exclude
params.FilterDescendantsInstances = {} -- e.g. { character } of the shooter
params.IgnoreWater = true

local function castRay(origin: Vector3, direction: Vector3): RaycastResult?
	-- direction's length is the max distance
	return workspace:Raycast(origin, direction, params)
end

local result = castRay(Vector3.new(0, 50, 0), Vector3.new(0, -100, 0))
if result then
	print(result.Instance, result.Position, result.Normal, result.Material, result.Distance)
end

-- Swept volumes: thick bullets, melee arcs, ground checks with width.
local sphereHit = workspace:Spherecast(Vector3.new(0, 10, 0), 2, Vector3.new(0, 0, 50), params)
local boxHit = workspace:Blockcast(CFrame.new(0, 10, 0), Vector3.new(4, 4, 4), Vector3.new(0, 0, 50), params)

-- Volume overlap: explosions, hitboxes, zone checks.
local overlap = OverlapParams.new()
overlap.FilterType = Enum.RaycastFilterType.Exclude
overlap.MaxParts = 50
local partsInBox = workspace:GetPartBoundsInBox(CFrame.new(0, 5, 0), Vector3.new(10, 10, 10), overlap)
local partsInSphere = workspace:GetPartBoundsInRadius(Vector3.zero, 15, overlap)
print(sphereHit, boxHit, #partsInBox, #partsInSphere)
```

- **Reuse** params objects; update `FilterDescendantsInstances` (or `params:AddToFilter(instance)`) instead
  of allocating per call.
- `RespectCanCollide = true` to ignore non-collidable parts; `CollisionGroup = "Name"` to query as a group.
- `GetPartsInPart(part, params)` does exact geometry overlap (costlier); `GetPartBoundsIn*` use bounding boxes.
- Deprecated: `FindPartOnRay*`, `Ray.new`, `FindPartsInRegion3*` → use the APIs above.
- Client queries only see streamed-in parts; authoritative checks run on the server.

## Touched: know its limits

`Touched` fires from the physics engine, only for parts that physically contact, is fired by whoever
simulates the part (clients can spoof or suppress it for parts they own), and can fire many times per
contact. Use it for triggers (pads, pickups) with a debounce and server-side validation; use spatial
queries for hit detection and zones.

```luau
--!strict
local Players = game:GetService("Players")

local pad = Instance.new("Part")
pad.Anchored = true
pad.Parent = workspace

local recently: { [Player]: boolean } = {}

pad.Touched:Connect(function(hit)
	local character = hit:FindFirstAncestorOfClass("Model")
	local player = character and Players:GetPlayerFromCharacter(character)
	if not player or recently[player] then
		return
	end
	recently[player] = true
	print(`{player.Name} stepped on the pad`)
	task.delay(1, function()
		recently[player] = nil
	end)
end)
```

## Collision groups

```luau
--!strict
-- Collision group APIs now live on WorldRoot (workspace); the PhysicsService versions are superseded.
workspace:RegisterCollisionGroup("Players")
workspace:RegisterCollisionGroup("Ghosts")
workspace:CollisionGroupSetCollidable("Players", "Ghosts", false)

local ghost = Instance.new("Part")
ghost.CollisionGroup = "Ghosts" -- assign by name (CollisionGroupId/SetPartCollisionGroup are deprecated)
ghost.Parent = workspace
```

Register groups once at server start (max 32, see `workspace:GetMaxCollisionGroups()`). `CanCollide = false` removes all collisions;
`CanQuery = false` hides a part from raycasts; `CanTouch = false` disables `Touched` (saves CPU);
`NoCollisionConstraint` disables collision between two specific parts.

## Assemblies and joints

- An **assembly** = parts rigidly connected (welds, `WeldConstraint`, `Motor6D`, rigid constraints). It
  simulates as one body; the root part (`part.AssemblyRootPart`) determines network ownership.
- Anchor static geometry. Unanchored + welded to an anchored part = anchored assembly.
- Weld at edit time with `WeldConstraint` (keeps current offset); in code set `Part0`/`Part1` and parent.
- Move whole models with `model:PivotTo(cframe)`. Moving many parts at once: `workspace:BulkMoveTo`.
- Read/set physics via `AssemblyLinearVelocity`/`AssemblyAngularVelocity`, `part:ApplyImpulse()`,
  `ApplyAngularImpulse()`, `AssemblyMass`. `Velocity`/`RotVelocity` are deprecated.
- `CustomPhysicalProperties = PhysicalProperties.new(density, friction, elasticity, frictionWeight, elasticityWeight)`.
- Units: 1 stud ≈ 0.28 m, `workspace.Gravity` default 196.2 studs/s².

## Mover constraints (replace BodyMovers)

| Goal | Constraint | Replaces |
| --- | --- | --- |
| Hold/drive a velocity | `LinearVelocity` (`VelocityConstraintMode` Vector/Plane/Line) | `BodyVelocity` |
| Move toward a position | `AlignPosition` (`Mode = OneAttachment` + `Position`, `Responsiveness`, `MaxForce`) | `BodyPosition` |
| Rotate toward an orientation | `AlignOrientation` (`CFrame`/`LookAtPosition`) | `BodyGyro` |
| Constant force | `VectorForce` (`RelativeTo = World`) | `BodyForce`, `BodyThrust` |
| Spin | `AngularVelocity` | `BodyAngularVelocity` |
| Pull toward point | `LineForce` | `RocketPropulsion` |
| Torque | `Torque` | — |

All need an `Attachment` (`Attachment0`). Set `MaxForce`/`MaxTorque` realistically (not `math.huge`
unless intended) or objects fling. Mechanical constraints: `HingeConstraint` (Motor/Servo actuators for
wheels, doors), `PrismaticConstraint` (sliders, elevators), `SpringConstraint` (suspension),
`RopeConstraint`, `RodConstraint`, `BallSocketConstraint`, `CylindricalConstraint` (wheel + steering),
`UniversalConstraint`, `RigidConstraint`.

Vehicle and projectile recipes, CFrame cookbook: [references/recipes.md](references/recipes.md).

## Network ownership

- The server auto-assigns ownership of unanchored assemblies to a nearby client (smooth for that client,
  exploitable by it). Characters are owned by their player.
- `part:SetNetworkOwner(nil)` = server simulates (secure, laggier for players); `SetNetworkOwner(player)`
  for a vehicle driver; `SetNetworkOwnershipAuto()` to restore. Call on the root part, server-side, after
  the assembly is in `Workspace`. Anchored parts have no owner.
- Ownership changes cause hitches; don't flip it every frame. Visualize with the viewport's
  **Visualization options → Network owners** toggle.

## Server authority (competitive games)

Workspace `AuthorityMode = Server` makes the server simulate everything while clients **predict** a few
frames ahead and **roll back/resimulate** on mispredictions. Requirements: `NextGenerationReplication`,
`PlayerScriptsUseInputActionSystem`, `SignalBehavior = Deferred`, `UseFixedSimulation`, `StreamingEnabled`
(setting `AuthorityMode` sets these). Core rules:
- Game logic lives in functions bound with `RunService:BindToSimulation(fn)` inside a ModuleScript required
  by both server and client.
- Clients affect the game only through **Input Actions** (InputContexts parented under the `Player`),
  not `UserInputService` events.
- Sync custom state through **attributes** on predicted instances, written only inside simulation callbacks.
- Don't cache `AnimationTrack`s; query `Animator:GetTrackByAnimationId()` each step.

Rollout status can change — check the docs. Details and patterns: [references/server-authority.md](references/server-authority.md).

## Stability tips

- Jitter: conflicting ownership, constraints fighting, huge mass ratios (> 1:100), or setting CFrame on
  unanchored parts every frame (use constraints instead).
- Flinging: `MaxForce = math.huge` on light parts, overlapping collisions at spawn, NaN/huge velocities.
- Sleeping assemblies stop simulating until disturbed — wake with a small impulse if needed.
- Adaptive timestepping (`Workspace.PhysicsSteppingMethod = Adaptive`) saves CPU; use fixed for precise mechanisms.

## Related skills

`roblox-security` (ownership exploits), `roblox-characters-animation`, `roblox-networking`,
`roblox-performance`, `roblox-input`.
