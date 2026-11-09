---
name: roblox-code
description: Write the Luau for a Roblox game the way it survives contact with a real playtest - server-authoritative, Knit services and controllers, plain RemoteEvents, every tunable in Config, every rule that can be pure written as a pure Core module with a headless spec - and PROVE it on disk before Studio ever sees it, through four gates (rojo build, lune run test, selene, stylua) that run in about a second and need no Studio at all. Scaffolds a complete project that is green on all four before a line of game code exists. Use whenever the user wants Roblox game code written, a game project set up, Rojo/Wally/Knit wired up, gameplay systems or services built, code reviewed for exploitability or replication bugs, or asks why their remote fires but nothing happens, why a script edit had no effect, why duplicate modules appeared, or why the character fights their own movement code.
---

# Roblox code that can be proven without Studio

> **First time on this machine?** Read `LOCAL.md` in this folder. If it does not exist, run the
> `roblox-skills-setup` skill (or copy `LOCAL.template.md` to `LOCAL.md` and fill it in).
> `LOCAL.md` holds your paths and tool locations; it is yours and is never shared.

The hard constraint on this platform is not the language, it is **feedback**. A
running Roblox game is close to uninspectable from outside: `capture_screenshot`
is edit-mode only, `execute_luau` only ever reaches the edit DataModel, and
`VirtualInputManager` is unavailable from plugin context. During a playtest, the
only channel back is `LogService`.

Everything below follows from that one fact. If the game cannot be watched while
it runs, then **as much of it as possible must be decidable while it sits still.**

```
write code on disk
  -> rojo build      does it parse and assemble?         ~1s
  -> lune run test    does the pure logic still hold?     no engine, no Studio
  -> selene           lint
  -> stylua --check   format
  -> rojo serve       Studio sees it     <- the FIRST time Studio is involved
  -> playtest         a human, plus LogService
```

Four gates before Studio. `scripts/check.py` runs them in that order and stops
at the first, because a project that will not build makes every later message
noise rather than signal.

---

## The five standing rules

These came out of a v1 post-mortem on a real game that had to be rebuilt. They
are not style preferences.

**1. Disk is the only source of truth.** Studio connects via `rojo serve`. Never
edit a script inside Studio, never `set_script_source` over MCP. MCP is for
geometry, inspection and screenshots. (v1 died of Studio-to-disk drift.)

**2. Pure logic lives in `src/shared/Core/`, Instances live at the edges.** If a
function can be written without touching an Instance, it must be. That is the
only reason any of this is testable at all.

**3. Gameplay and cross-client paths go through one `Net.luau`** of plain
RemoteEvents, every name declared in one place. Knit is lifecycle and DI
scaffolding, not transport. When you cannot watch the game run, the most
primitive debuggable transport wins.

**4. Cosmetics can never break gameplay.** Effects resolve async, fail inert,
every one pcall-isolated. (v1's grapple was killed by a tracer.)

**5. Every tunable lives in `src/shared/Config/`.** A balance pass must be a data
edit, never a code edit.

---

## Server authority

> The server owns the game. Clients own the display.

| Responsibility | Lives on |
|---|---|
| Game state: health, inventory, score, ownership | **Server** |
| Game logic: damage, purchases, spawning, scoring | **Server** |
| Validation and anti-cheat | **Server** |
| Input, camera, local UI, visual feedback | Client |

Every value that arrives from a client is a **request**. Validate type, then
range, then ownership, before it changes anything:

```lua
remote.OnServerEvent:Connect(function(player: Player, target: unknown)
	if typeof(target) ~= "Vector3" then return end
	local char = player.Character
	if not char or not char.PrimaryPart then return end
	if (target - char.PrimaryPart.Position).Magnitude > MAX_REACH then return end
	-- only now is it a fact
end)
```

The exception worth naming: movement in a fast first-person game is usually
client-authoritative because server-authoritative movement feels awful. That is
a deliberate, documented trade, not an oversight - but it means the *consequences*
of movement (scoring, elimination, rewards) must stay on the server.

---

## Start a project

```bash
python ~/.claude/skills/roblox-code/scripts/new_project.py "Coin Dash" \
    --dir ~/Projects/CoinDash
cd ~/Projects/CoinDash
aftman install && wally install
python ~/.claude/skills/roblox-code/scripts/check.py
```

That last command must print **all gates green** before any game code is written.
Verified on a clean scaffold: rojo build, 3 tests, selene and stylua all pass.
A scaffold that cannot clear its own gates hides the first real failure behind
noise, so step 0 of every build order is "the gates are green with nothing in
the game yet".

What the scaffold gives you: pinned toolchain (rojo 7.4.1, wally 0.3.2, selene
0.28.0, stylua 0.20.0, lune 0.8.9), Knit + Promise + Signal + Trove, the boot
pair, `Net.luau`, `GameConfig`, one worked Core module with its spec, the
headless runner, and a build stamp in both boot scripts.

---

## Check it

```bash
python ~/.claude/skills/roblox-code/scripts/check.py            # all gates
python ~/.claude/skills/roblox-code/scripts/check.py --fix      # let stylua rewrite
python ~/.claude/skills/roblox-code/scripts/check.py --skip-lint  # build + tests only
```

`rojo build` is the single highest-value command in Roblox development and it is
under-used: it parses every file and assembles the whole tree in about a second,
so it catches a syntax error, a bad `$path`, a file Rojo will not accept, and a
malformed instance file, all without Studio open.

---

## Writing a Core module and its spec

This is the shape that makes the gates worth having. Rules go in, Instances stay
out, and the spec pins the *intent*, not the implementation:

```lua
-- src/shared/Core/Flock.luau
-- Positions come in as flat x/z scalars, NOT Vector3. See the rule below.
function Flock.strays(xs: { number }, zs: { number }, cx: number, cz: number, radius: number): { number }
```

```lua
-- tests/Flock.spec.luau
local Flock = require("../src/shared/Core/Flock")

return {
	["a sheep exactly on the radius is not a stray"] = function()
		-- The boundary is the whole question: off by one here means the wolf
		-- takes a sheep the player was told was safe.
		assert(#Flock.strays({ 10 }, { 0 }, 0, 0, 10) == 0)
	end,
}
```

**Core modules take plain numbers, not Roblox datatypes.** Measured: `Vector3`
and `CFrame` are not globals in Lune, so a Core module that uses them cannot be
required by a spec at all. `require("@lune/roblox")` does provide them, but
importing it into the module under test defeats the point of Core being pure.
Pass `(x, y, z)` scalars across the boundary and build the `Vector3` at the edge,
in the Service or Controller. Every Core module on the reference project follows
this and it is the reason the suite runs at all.

A spec that restates the implementation is worth nothing. A spec that pins the
boundary a designer argued about is worth the whole suite.

More patterns, including the Knit service and controller shapes and the Net
transport: `references/patterns.md`.

---

## The traps that cost real days

Full detail with symptoms in `references/traps.md`. The short list, because
knowing these exist is most of the value:

**A remote payload has THREE ends.** Sender, server relay, receiver. Change the
arguments at one and the untouched middle silently drops every packet - no error
anywhere. Grep the arity across all three before believing a fix.

**Two Rojo connections duplicate every new file.** Two plugin connections create
each new ModuleScript twice, `Knit.AddControllers` then throws on the duplicate
name, and every controller dies at once. One server, one connect.

**ROJO OWNS ITS SUBTREE. A RUNTIME CHILD OF ONE IS DELETED ON THE NEXT CONNECT.**
Anything that must survive a sync has to live in the SOURCE Rojo serves - not in
code that creates it at runtime. This is not intermittent; it is what
reconciliation *is*. Measured 2026-09-09: a service dressed the map at runtime,
replacing 897 prop boxes with MeshParts. It worked - correct kinds, correct
placement, the map finally looked like a map. Then Rojo reconnected and every
tree vanished, because `Workspace.Map` is sourced from a file, and 897 instances
that are in the game and in no source file are, correctly, stale instances to
remove. It reads exactly like "Rojo is broken" and it is the opposite.

The trap underneath it: **`MeshId` is not settable from a Rojo `.model.json`
property table**, which is what pushes people to a runtime step in the first
place. The way out is not runtime - it is `.rbxmx`, Roblox's own XML model
format, where `MeshId` and `TextureID` are ordinary `<Content>` properties:

```xml
<Item class="MeshPart" referent="RBX1"><Properties>
  <Vector3 name="InitialSize"><X>5</X><Y>8.2</Y><Z>5</Z></Vector3>
  <Vector3 name="size"><X>10</X><Y>16.4</Y><Z>10</Z></Vector3>
  <Content name="MeshId"><url>rbxassetid://MESH_ID</url></Content>
  <Content name="TextureID"><url>rbxassetid://IMAGE_ID</url></Content>
</Properties></Item>
```

`InitialSize` is the mesh's NATURAL size and is what Roblox scales `size`
against; omit it and the mesh is stretched by whatever the importer guessed.
And **edit an rbxmx with an XML parser, never a regex** - a part carrying a
PointLight has a nested `<Item>`, so a flat scan produces unbalanced XML.
`rojo build` catches that, and is the reason to run it after any file rewrite.

**`ScaleTo` is a `Model` method, not a `MeshPart` one.** A MeshPart scales by
setting `.Size`. `clone:ScaleTo(n)` on a MeshPart throws on the first one it
touches - and no static check sees it, because it is a runtime member lookup.

**An established TCP connection is not a synced session.** An unaccepted "Would
you like to connect?" prompt blocked syncing for an entire session while
everything looked connected. That is what the build stamp in the boot scripts is
for: if that exact line is not in Output, Studio is not running your code and no
edit you make can possibly matter.

**A Knit method named the same as its cache field returns the function.** Silent,
type-checks fine, and the value you get back is a function rather than data.

**A bare `pcall` hides the throw.** Always capture and warn the error, or the
failure becomes invisible and you debug the wrong layer for an hour.

**A grounded Humanoid brakes scripted velocity to a stop.** Setting WalkSpeed to
0 is itself a brake, and `ChangeState(Freefall)` loses to the 240Hz state
machine. `SetStateEnabled(Running, false)` with a guaranteed restore is the only
thing that holds.

**`execute_luau` drops all output if the script yields.** Split it into two
calls, or schedule with `task.delay` and return immediately.

**A verifier that cannot find its target must FAIL, not pass.** A check scoped to
the wrong name reported green while 361 defects shipped underneath it. "Not
found" is a failure result.

---

## Anti-patterns

| Anti-pattern | Why it bites | Instead |
|---|---|---|
| `wait()`, `spawn()`, `delay()` | Deprecated scheduler, imprecise | `task.wait/spawn/delay/defer` |
| A number hardcoded in a Service | Balance passes become code changes | `src/shared/Config/` |
| Remote names as bare strings | Typos fail silently | Declared in `Net.luau` |
| Knit auto-remotes for gameplay | Undebuggable when play mode is opaque | `Net.luau` |
| Client-stored state | Exploitable by definition | Server |
| `require` inside a loop | Repeated resolution | Cache the reference |
| Deep `require` chains | Circular dependency hell | Knit's service locator |
| Unbounded `RunService.Heartbeat` work | Frame cost scales with players | Budget it, or use tags |

---

## When Studio is finally involved

`rojo serve`, then check the build stamp in Output. After that, the MCP is for
inspection only: `get_script_source` to confirm what Studio actually holds,
`grep_scripts` to find call sites, `get_output_log` for errors.

Two things to know about the boundary:

- `execute_luau`'s `require` is **cached**, so a changed module keeps running the
  old code. Verify via `.Source`, not by re-requiring.
- Play mode cannot be inspected. A human has to watch it, and the finding they
  bring back is real data - on one build, the only defect that mattered
  came from a playtest, not from any automated verification, because the test
  stage was not a faithful stand-in for a live player character.
