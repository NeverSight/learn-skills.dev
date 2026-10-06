---
name: roblox-npc-ai
description: NPCs and enemy AI - PathfindingService (CreatePath, ComputeAsync, costs, modifiers, links, blocked paths), chase/follow loops, state machines, perception and line of sight, spawning/pooling, scaling to many NPCs. Use when creating enemies, pets, followers, shopkeepers, wave spawners, or fixing NPCs that get stuck, jitter, or lag the server.
---

# NPCs and AI

## Architecture

- NPC **logic runs on the server** (authoritative targets, damage, drops). Visual extras (idle
  animations, nameplates, effects) can run on clients.
- One NPC service drives all NPCs from a single loop (e.g. 5–10 Hz "think" rate, staggered), not one
  script + `while true` per NPC. Tag NPC models (`CollectionService`) and keep per-NPC state in a table.
- Server-owned physics: `npc.PrimaryPart:SetNetworkOwner(nil)` after spawning, so NPCs don't stutter
  when ownership moves between nearby players (and exploiters can't push them).
- Use `Humanoid` for NPCs that need walking/jumping/climbing; for simple movers (turrets, floating
  enemies, crowds) use an `AnimationController` + `Animator` and move with constraints or CFrames.

## Pathfinding

```luau
--!strict
local PathfindingService = game:GetService("PathfindingService")

local path = PathfindingService:CreatePath({
	AgentRadius = 2,
	AgentHeight = 5,
	AgentCanJump = true,
	AgentCanClimb = false,
	WaypointSpacing = 4,
	Costs = {
		Water = 20, -- avoid water (Enum.Material name)
		DangerZone = math.huge, -- PathfindingModifier.Label: never cross
	},
})

-- Walk `humanoid` to `goal`. Returns true on arrival, false if unreachable or interrupted.
local function walkTo(humanoid: Humanoid, goal: Vector3): boolean
	local root = humanoid.RootPart
	if not root then
		return false
	end
	local ok = pcall(function()
		path:ComputeAsync(root.Position, goal)
	end)
	if not ok or path.Status ~= Enum.PathStatus.Success then
		return false -- NoPath: try a fallback (direct MoveTo, new goal, teleport if stuck long)
	end

	local waypoints = path:GetWaypoints()
	local blocked = false
	local blockedConnection = path.Blocked:Connect(function(blockedIndex)
		blocked = true -- an obstacle appeared on a waypoint ahead; caller recomputes
		print("path blocked at waypoint", blockedIndex)
	end)

	for index = 2, #waypoints do
		local waypoint = waypoints[index]
		if waypoint.Action == Enum.PathWaypointAction.Jump then
			humanoid.Jump = true
		end
		humanoid:MoveTo(waypoint.Position)
		local reached = humanoid.MoveToFinished:Wait() -- false after 8 s timeout
		if not reached or blocked or humanoid.Health <= 0 then
			blockedConnection:Disconnect()
			return false
		end
	end
	blockedConnection:Disconnect()
	return true
end

return walkTo
```

- `CreatePath` + `ComputeAsync` is the current API (`FindPathAsync` is superseded). Reuse `Path` objects
  per agent type; `ComputeAsync` yields — never call it every frame for every NPC.
- **Chasing moving targets**: recompute when the target moved more than a few studs since the last
  compute or every ~0.5–1 s, and skip pathfinding entirely when there's a clear line of sight
  (`workspace:Raycast` from NPC to target) — just `MoveTo` the target.
- `PathfindingModifier` (child of a part/region, `Label` matching a `Costs` key, `PassThrough` for doors)
  and `PathfindingLink` (between two attachments, e.g. ladders, teleporters, boats; the waypoint has
  `Label` and `Action = Custom`) shape paths.
- Limits: start→goal straight-line distance ≤ 3,000 studs, 20,000-node budget; far goals need
  intermediate targets. Visualize the navmesh with Studio's **Navigation Mesh** visualization option.
- On clients, pathfinding sees only streamed-in geometry: compute paths on the server.

## Behavior: state machine

```luau
--!strict
type State = "Idle" | "Chase" | "Attack" | "Return"

type Npc = {
	model: Model,
	humanoid: Humanoid,
	home: Vector3,
	state: State,
	target: Model?,
	lastAttack: number,
}

local AGGRO_RANGE = 40
local ATTACK_RANGE = 5
local LEASH_RANGE = 80
local ATTACK_COOLDOWN = 1.2

local losParams = RaycastParams.new()
losParams.FilterType = Enum.RaycastFilterType.Exclude

local function hasLineOfSight(from: Vector3, target: BasePart, ignore: { Instance }): boolean
	losParams.FilterDescendantsInstances = ignore
	local result = workspace:Raycast(from, target.Position - from, losParams)
	return result == nil or result.Instance:IsDescendantOf(target.Parent :: Instance)
end

local function think(npc: Npc, findTarget: (Vector3, number) -> Model?)
	local root = npc.humanoid.RootPart
	if not root or npc.humanoid.Health <= 0 then
		return
	end
	local targetRoot = npc.target and npc.target:FindFirstChild("HumanoidRootPart") :: BasePart?
	local distance = if targetRoot then (targetRoot.Position - root.Position).Magnitude else math.huge

	if npc.state == "Idle" then
		npc.target = findTarget(root.Position, AGGRO_RANGE)
		if npc.target then
			npc.state = "Chase"
		end
	elseif npc.state == "Chase" then
		if not targetRoot or (root.Position - npc.home).Magnitude > LEASH_RANGE then
			npc.state = "Return"
		elseif distance <= ATTACK_RANGE then
			npc.state = "Attack"
		elseif hasLineOfSight(root.Position, targetRoot, { npc.model }) then
			npc.humanoid:MoveTo(targetRoot.Position)
		end -- else: request a path (throttled) via walkTo in a separate thread
	elseif npc.state == "Attack" then
		if not targetRoot or distance > ATTACK_RANGE * 1.5 then
			npc.state = "Chase"
		elseif os.clock() - npc.lastAttack >= ATTACK_COOLDOWN then
			npc.lastAttack = os.clock()
			local targetHumanoid = npc.target and npc.target:FindFirstChildOfClass("Humanoid")
			if targetHumanoid then
				targetHumanoid:TakeDamage(10)
			end
		end
	elseif npc.state == "Return" then
		npc.target = nil
		npc.humanoid:MoveTo(npc.home)
		if (root.Position - npc.home).Magnitude < 4 then
			npc.state = "Idle"
		end
	end
end

return think
```

For complex AI (many behaviors, priorities), use a behavior tree or utility AI; keep the same "think
at a fixed rate, act through small primitives" structure. See [references/scaling-npcs.md](references/scaling-npcs.md)
for spawning, pooling, and performance with hundreds of NPCs.

## Perception tips

- Find targets with `workspace:GetPartBoundsInRadius` against a collision group/filter containing only
  characters, or iterate `Players:GetPlayers()` (cheaper for small counts) and compare squared distances.
- Add reaction delays and field-of-view checks (`root.CFrame.LookVector:Dot(direction.Unit) > 0.5`)
  so NPCs feel fair.
- Stagger thinking: `npcIndex % 5 == frame % 5` spreads work across frames.

## Related skills

`roblox-characters-animation` (humanoids, animation), `roblox-physics` (ownership, raycasts),
`roblox-performance` (profiling, parallel Luau), `roblox-game-systems` (waves, combat, drops).
