---
name: unity-gameplay-systems
description: "Build and iterate playable Unity gameplay systems for casual iOS games. Combines first-playable-slice setup, C# architecture, Input System touch controls, scene/prefab assembly via MCP, and game-feel tuning. Use for new project setup, first playable slice, game loops, entity/component systems, input (taps/swipes/drag), collision/physics 2D & 3D, scoring, spawning, object pooling, difficulty curves, camera follow, controls, game feel/juice (squash-stretch, screen shake, hit-stop, haptics), and 2D/3D casual mechanics (tappers, match, puzzle, endless runner, stacker)."
---

# Unity Gameplay Systems

## Purpose

Stand up and evolve a verified playable loop for a casual iOS game: a controllable thing on screen, responsive touch input, deterministic update order, mobile-safe hot paths, and behavior proven in Play Mode — not a folder of design docs.

## Use When

Starting a new casual game, repairing a weak prototype, adding mechanics/entities, designing C# architecture, wiring touch input, assembling scenes/prefabs, tuning camera/controls/difficulty, or adding juice.

## Core Doctrine (shared with the unity-* set)

1. **Ship a verified playable slice early.** Get a controllable object on screen that runs in Play Mode in the first session, then iterate. Never deliver only design docs.
2. **Keep gates lean for a solo dev.** Ask at genuine branch points (concept, art direction, scope, billable actions); otherwise proceed with sensible defaults and batch decisions.
3. **Edit Unity through MCP, never raw YAML.** Scenes/prefabs/components/assets go through `unity-mcp-bridge` (`manage_scene`, `manage_gameobject`, `manage_components`, `manage_prefabs`, `create_script`) or generated Editor scripts. C# is plain text and safe to `Edit`, but is **not done until it compiles clean** — confirm with `read_console(types=["error"])`.
4. **Verify APIs on Unity 6.** The model's built-in Unity knowledge is ~2022.3. On Unity 6 (6000.x) the Input System and UI Toolkit differ. Call `unity_reflect` / `unity_docs` before writing C# you are unsure of. Trust order: reflection > project assets > docs > memory.

## Workflow

1. Read `mcpforunity://editor/state` (ready, not compiling, no domain reload pending) and `mcpforunity://project/info` (`renderPipeline`, `activeInputHandler`, UI stack) before any batch.
2. Define the one-sentence loop: **verb → objective → feedback → fail/retry.**
3. Decide 2D or 3D and pick a template (below). Load `references/casual-templates.md` for the step-by-step build recipe.
4. Build the slice: input → state → entity → collision/physics → feedback → HUD hook. Smallest playable increment first.
5. Tune feel: movement, camera follow, impact, juice, difficulty, restart loop. Load `references/checklists/casual-game-feel.md`.
6. Keep hot paths allocation-free and update order explicit.
7. Verify against `references/checklists/new-game-definition-of-done.md` before claiming the slice is done.

Load `references/csharp-patterns.md` when writing C# (pooling, Input System actions, state machine, singleton manager, events).

Load `references/headless-editor-recipes.md` whenever building/testing WITHOUT a live Editor/MCP (batch-mode `-executeMethod`/`-runTests` runs): URP 17.5 2D asmdef split, headless URP activation, the NewScene prefab-ref invalidation + VerifyWired rule, synchronous ImportPackageImmediately, `RenderPipeline.StandardRequest` screenshots, and batch-run mechanics — all verified on a real 6000.5 build.

## Project / scene setup via MCP (start the slice fast)

```text
manage_editor(action="get_state")                       # confirm ready
manage_scene(action="create", name="Game", path="Assets/Scenes/Game.unity")
manage_scene(action="load", path="Assets/Scenes/Game.unity")
# camera + light usually exist; add the player + ground, then a script:
create_script(name="PlayerController", path="Assets/Scripts/")  # compiles -> read_console
manage_gameobject(action="create", name="Player", primitive_type="Capsule")
manage_components(action="add", target="Player", component="PlayerController")
manage_editor(action="play") -> read_console -> manage_scene(action="screenshot") -> stop
```

Primitives are fine to *prove the loop* — flag each one as a placeholder in the ledger. **Registry-only rule for production visuals:** all visible sprites/meshes/materials on gameplay prefabs must come from the approved-asset registry (`unity-asset-pipeline`, `Assets/<Game>/Art/Approved/registry.yaml`) — never wire raw generator output into a gameplay prefab. Logic prefabs may wrap registry assets. Primitives are allowed only while the registry is empty (or for a surface the registry doesn't cover yet) and flagged as placeholders in the ledger. A screenshot of only primitives is not a finished game.

### Prefer full runtime construction over headless-wired serialized references

When building a scene/UI **headlessly** (no human in the Editor), prefer a **single bootstrap MonoBehaviour** that builds and wires everything in code over hand-wiring serialized object/asset references via `SerializedObject.FindProperty`. We were bitten twice: headless-wired references **deserialize as NULL when the scene is reopened**, and the resulting `NullReferenceException` at render time is **silently swallowed inside `async void`** methods — the console looks clean while the board renders blank.

Robust pattern: one bootstrap (e.g. `AppRoot`) that in `Awake()` builds the Camera, EventSystem, Canvas, all UI and all systems in code, and wires them via public `Init(...)` methods. The saved scene then needs only **one** GameObject, so there is nothing to lose on reopen.

- **Self-healing SO fallback:** if a referenced `ScriptableObject` is null, `ScriptableObject.CreateInstance<T>()` at runtime — give the SO sane default field values so it is fully usable with no asset on disk.
- **Runtime-built cameras need an explicit `AudioListener`** (`AddComponent<AudioListener>()`); there is no warning-free default, so audio silently dies otherwise.

## C# best practices (firm rules)

- **Cache `GetComponent` in `Awake`/`Start`, never in `Update`.** Resolve all component refs once.
- **No `Find` / `FindObjectOfType` / `SendMessage` in production.** Wire references via `[SerializeField]`, a singleton manager, or events. Find-calls are scene-wide scans.
- **`[SerializeField] private` over public fields.** Expose to the Inspector without breaking encapsulation. Public fields only for genuine cross-object contracts.
- **Zero-allocation hot paths.** Pool objects (never `Instantiate`/`Destroy` per frame), use `Physics.RaycastNonAlloc` / `OverlapNonAlloc`, avoid LINQ, string concatenation, boxing, and per-frame `new` in `Update`/`FixedUpdate`. Cache `WaitForSeconds`.
- **`== null`, not `is null`, for `UnityEngine.Object`.** Unity overloads `==` to detect destroyed objects; `is null` bypasses it and misreports.
- **One Assembly Definition (`.asmdef`) per feature folder.** Fast incremental compiles, enforced dependencies, shorter domain reloads. Keep Editor-only code in a separate `Editor` asmdef.
- **Physics in `FixedUpdate`, input/visuals in `Update`.** Move `Rigidbody`/`Rigidbody2D` with `MovePosition`/forces, not transform writes.

Expanded with snippets in `references/csharp-patterns.md`.

## Input — Input System, not legacy `Input`

Use the **Input System** package (Action-based), not `UnityEngine.Input`. Check `activeInputHandler` in `project/info`; on Unity 6 verify the API with `unity_reflect` before writing. Drive an `InputActionAsset` or `PlayerInput`, and read touch via `Touchscreen.current` / `EnhancedTouch`.

```csharp
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.EnhancedTouch;
using Touch = UnityEngine.InputSystem.EnhancedTouch.Touch;

public class TouchInput : MonoBehaviour
{
    void OnEnable()  => EnhancedTouchSupport.Enable();
    void OnDisable() => EnhancedTouchSupport.Disable();

    void Update()
    {
        foreach (var t in Touch.activeTouches)
        {
            if (t.phase == UnityEngine.InputSystem.TouchPhase.Began)
                OnTap(t.screenPosition);                     // tap
            if (t.phase == UnityEngine.InputSystem.TouchPhase.Moved)
                OnDrag(t.delta);                             // drag / swipe delta
        }
    }
    void OnTap(Vector2 screenPos) { }
    void OnDrag(Vector2 delta) { }
}
```

For swipe detection, accumulate `delta` from `Began` to `Ended` and threshold the magnitude/direction. In the Editor, the mouse maps to touch for quick iteration.

## Template A — 2D casual (tapper / match / puzzle)

- `SpriteRenderer` for visuals; a **Sprite Atlas** for all gameplay sprites (one draw call, less memory).
- `Rigidbody2D` + `Collider2D` for physics objects; set `Rigidbody2D.bodyType = Kinematic` for tap-moved pieces, `Dynamic` for falling/bouncing.
- Triggers via `OnTriggerEnter2D` for pickups/matches; tap-picking via a camera raycast: `Physics2D.OverlapPoint(worldPos)` on `Camera.main.ScreenToWorldPoint`.
- Drive board/state with a small explicit **state machine** (`Idle → Selecting → Resolving → Spawning`), not scattered booleans.
- Orthographic camera; size the view to the board, anchor UI with safe areas (see `unity-ui-designer`).

Full ordered recipe (MCP calls + scripts): `references/casual-templates.md`.

## Template B — 3D casual (endless runner / stacker)

- Player: `CharacterController` for tight non-physics control (runner lane-switch, jump), or `Rigidbody` (interpolation on) for physics-y stack/roll games.
- World scroll: move the world toward the player **or** the player forward and recycle chunks. Spawn obstacles/coins from a **pooled** spawner ahead of the player; despawn behind.
- Collision: `OnTriggerEnter` for coins/power-ups, `OnCollisionEnter`/tagged trigger for hazards → kill → respawn / restart loop.
- Difficulty: ramp scroll speed and spawn density over time/distance from a manager.
- URP mobile rendering and lighting via `unity-graphics`.

Full ordered recipe: `references/casual-templates.md`.

## Template C — grid / number puzzle (Sudoku, nonogram, match-grid)

A huge share of casual hits are grid puzzles. Build them like this (full worked recipe in
`references/grid-puzzle-template.md`):

- **Separate pure logic from views.** Keep the grid model, generator, solver and board state in a
  no-Unity asmdef (`noEngineReferences: true`) so they unit-test in EditMode in milliseconds. A grid
  is just `int[]` row-major with `Index/RowOf/ColOf/BoxOf` helpers.
- **Procedural generation with a uniqueness guarantee.** Generate a full solution by randomized
  backtracking, then remove clues while a solution-counter (capped at 2) still returns exactly 1.
  Seed the RNG so a "daily puzzle" is reproducible. Never ship a puzzle with multiple solutions.
- **For constraint puzzles (Queens / Star-Battle / Sudoku family), use uniqueness *repair*, not
  rejection sampling.** Pure rejection (generate random constraints, keep only if the solver says
  unique) degrades badly as the board grows — at N=9 it essentially never hits a unique board.
  Instead: generate a valid solution, build constraints around it, then loop {find an alternate
  solution that differs from the true one; mutate one constraint cell the alternate (but not the
  true solution) depends on, invalidating that alternate while preserving the true solution's
  validity/connectivity}. Converges in ~1ms at N=9 where rejection sampling failed across 10000 tries.
- **BoardState** wraps the puzzle: player values, pencil-note bitmask, an undo stack, and
  `IsCorrect/IsConflicting/IsSolved`. Givens are immutable.
- **Build the grid at runtime** under a `GridLayoutGroup` from a cell prefab — the scene only needs
  the parent + prefab, no 81 hand-placed cells. Tap input via `IPointerClickHandler` on the cell
  (EventSystem + Input System UI module), not legacy `Input`.
- **Casual feel:** highlight peers/same-number, pop on correct, shake on wrong, fade pad digits that
  are fully placed, mistakes/lives + hints + undo — this is what makes it feel premium.
- **Swipe / drag-to-paint (mark many cells in one gesture).** Implement
  `IBeginDragHandler`/`IDragHandler`/`IEndDragHandler` on the cell. uGUI already separates a real TAP
  (fires `IPointerClickHandler`) from a DRAG (fires the drag handlers) and **suppresses the click when
  a drag occurs** — so tap-action and paint-action split cleanly with no extra state flags. To find the
  cell under the finger mid-drag, `EventSystem.current.RaycastAll(pointerEventData, results)` then
  `GetComponentInParent<Cell>` on each hit — pivot-independent, unlike a layout-math lookup. **Cache the
  results `List` + a reusable `PointerEventData`** so a move doesn't allocate per frame. Lock the "paint
  mode" from the START cell (empty→mark, existing-mark→erase), **never overwrite a placed piece**, and
  **persist once on `EndDrag`**, not per cell.
- **Derived / assist markers the player can still edit (e.g. auto-× on illegal cells).** A computed
  hint marker that the player may override needs a SEPARATE cell state from the player's own mark
  (`CellMark.AutoMarked` vs `Marked` in `QueensBoard`/`CubeBoard`), and three rules learned the hard way:
  - **Drive it off place/remove EVENTS, one-time — never a per-tap recompute.** A continuous
    `RecomputeAutoMarks` (every blocked cell → auto-mark) *fights the player*: an auto-× they manually
    clear gets instantly re-added on the next tap, so manual edits never stick. Instead, on PLACE stamp
    only the cells this piece *NEWLY* blocks — blocked by this piece AND not already blocked by another
    (`ApplyAutoMarksOnPlace`; "newly" is the crux, so adding a second piece that also blocks a
    previously-cleared cell won't resurrect the player's clear). Plain taps don't recompute, so manual
    add/clear sticks. **Restore-from-save trusts the saved snapshot** (it already holds the one-time
    marks + player edits) — re-deriving on load would clobber the player's clears. Needs a
    "blocked-EXCEPT-piece-X" predicate (`IsBlockedByVisibleRulesExcept`) to detect "newly blocked" plus
    a cheap per-pair geometric test (`CowBlocks`) distinct from the full-board scan.
  - **Unify derived vs player marks for the action the player expects sameness — but SCOPE it.** On
    REMOVE, players expect any × that piece justified — auto-added OR manually re-added — to clear once
    the cell is legal again. Reverting only `AutoMarked` strands manual ×'s. Fix
    (`RemoveMarksFreedByRemoval(removedIndex)`): clear ANY × (`Marked` OR `AutoMarked`) on a cell the
    REMOVED piece was blocking that no remaining piece blocks — but **bound it by geometry**
    (`CowBlocks(removed, cell)`) so unrelated player notes the piece never blocked survive.
  - **A derived VISUAL OVERLAY must be re-synced on EVERY state-mutating path, including drag/bulk.**
    The auto-× is its own overlay `Image` toggled by a sync pass (`SyncAutoMarks`), separate from the
    base `Render()`. Two bugs: (a) swipe-paint chose erase-vs-paint only from `Marked`, so a drag
    starting on an `AutoMarked` cell stamped player ×'s instead of erasing — treat ANY × start cell
    (`Marked` OR `AutoMarked`) as erase (`BeginPaintAt`). (b) The paint path called only base `Render()`,
    not the overlay sync, leaving stale auto-×'s visible (and a × painted under one read as "darker"
    double ×). Fix: a `RenderAndSyncAuto` helper (Render + overlay sync) on EVERY path that touches an
    overlay cell — tap, hint, drag-paint, undo, clear, restore, setting-toggle.
  - **Test it engine-free + mirror both variants.** Put the marker logic in the no-Unity Core so it's
    deterministic EditMode-testable. Region layout is procedural, so use a REAL generated puzzle plus a
    mirror `Blocks` predicate to *find* blocked/unblocked cells at runtime rather than hardcoding cells.
    Cover: stamp-on-place exact set, never-overwrite notes/pieces, manual-clear-sticks-even-when-another-
    piece-also-blocks, removal frees auto+manual ×, removal keeps still-blocked cells, removal keeps notes
    the piece never blocked. Add ONE PlayMode test through the real input path (`OnCellTapped`) since the
    controller branches on place-vs-remove. Mirror all of it to the second board variant so they don't diverge.
- **Lives / game-over.** A `[lives]` counter (e.g. 3), decremented on an invalid move (placing a
  conflicting piece), ends the game as a loss at 0. **Route win and lose through one `EndGame(bool won)`**
  so feedback/cleanup live in one place, and **persist lives in the save** — default a 0/legacy save back
  up to max on restore so an old save never spawns an already-dead board.
- **Daily puzzle.** Build a deterministic seed from the date (`year*1000 + dayOfYear`) + a *fixed*
  difficulty so every player gets the same board — feed it to the seeded generator above. Persist a
  `daily` flag **and the date** in the save so a win submits to the leaderboard; set a `_pendingDaily`
  flag *before* the async `StartNewGame` and consume it inside, so a normal new-game clears it (otherwise
  a later casual game inherits the daily flag and posts a bogus score).
- **Leaderboard backend seam.** Hide persistence behind an `ILeaderboard` interface
  (`Submit`/`GetHistory`/`GetGlobalTop`, **callback-based** so it's async-ready) and ship a
  `LocalLeaderboard` now (PlayerPrefs JSON, best-per-date). A remote impl (Supabase, or Railway+Postgres)
  then drops in behind the same interface with **zero gameplay changes**. Anti-cheat payoff: because the
  daily seed is deterministic, the **server can regenerate the puzzle and reject implausible solve times**
  — never trust client-reported times.

## Object pooling (essential for mobile)

Never `Instantiate`/`Destroy` per frame — it allocates and triggers GC hitches. Pre-instantiate, deactivate, reuse.

```csharp
public class Pool : MonoBehaviour
{
    [SerializeField] private PooledObject prefab;
    [SerializeField] private int size = 32;
    private readonly Stack<PooledObject> _free = new();

    void Awake()
    {
        for (int i = 0; i < size; i++) _free.Push(CreateOne());
    }
    private PooledObject CreateOne()
    {
        var o = Instantiate(prefab, transform);
        o.Init(this); o.gameObject.SetActive(false);
        return o;
    }
    public PooledObject Get(Vector3 pos)
    {
        var o = _free.Count > 0 ? _free.Pop() : CreateOne();
        o.transform.position = pos; o.gameObject.SetActive(true);
        return o;
    }
    public void Release(PooledObject o)
    {
        o.gameObject.SetActive(false); _free.Push(o);
    }
}
```

`UnityEngine.Pool.ObjectPool<T>` is a built-in alternative. More in `references/csharp-patterns.md`.

## Game feel / juice (casual)

Casual games live on feedback. Keep each effect short and snappy:

Scope: **procedural** game-feel motion (squash/stretch, tweens, screen-shake, hit-stop) lives here; **authored** character/asset animation (walk/attack/idle/death/etc.) is produced via Tripo + `unity-animation` (motion → Tripo, not frame-by-frame Gemini).

- **Tweening:** DOTween (if present) or coroutines for scale/position/color pops.
- **Squash & stretch** on land/hit; **screen shake** on impact; **hit-stop** on hits — defaults and the mandatory combat stack below.
- **Combat impact stack (MANDATORY for every attack — shipped-game defaults).** Empirically, hit-stop + contact SFX + camera response are each individually make-or-break for perceived impact; an attack missing any of the three fails QA regardless of how good the animation strip is. All fired from the strike-frame Animation Event (damage event), all on the VISUAL child / unscaled time so they compose:
  - **Hit-stop:** light 0.08s, heavy 0.15s, kill-shot 0.20s + a slight camera zoom punch; victim frozen +0.03s longer than attacker; ~0 for rapid multihits/DoT ticks. Prefer **per-entity** stop (`animator.speed = 0` + cache/zero rigidbody velocity on the two combatants only) over a global `Time.timeScale` dip so multi-enemy scenes don't stutter. During the freeze, jitter the victim's visual child ±1px in pixel-grid steps.
  - **Attacker lunge:** 0.2s, 4–6 world-pixels forward on the visual child, starting on the INPUT frame (input-to-visible must stay <100ms). **Defender knockback:** 2–4px in the attack direction. **Defender squash:** scale (1.2, 0.8) springing back over ~0.1s (EaseOutBack, unscaledDeltaTime) — composes with lunge (localPosition) and flash (shader).
  - **Hit flash:** shader-level `lerp(c.rgb, _FlashColor, _FlashAmount)` driven via MaterialPropertyBlock, 0.05–0.10s. `SpriteRenderer.color` is a multiplicative tint — setting it white does NOTHING; renderer.color "flash" is the invisible-feedback bug in another channel.
  - **Screen shake:** a trauma scalar in [0,1] accumulating per hit, decaying linearly; amplitude = trauma² driven by Perlin noise. Pixel-art caveat: quantize offsets to whole texels (or shake before the pixel-perfect snap) and cap at 2–4 world-pixels or it aliases into shimmer.
  - **Slash/impact VFX overlay + SFX** on the same event (overlay generation/wiring: unity-pixel-art + unity-animation).
- **Particle pops** and **score popups** (pooled world-space text) on collect/match.
- **Haptics (iOS):** light/medium/heavy taps on key beats. On iOS use `UnityEngine.iOS.Haptic` / `UIImpactFeedbackGenerator` via plugin, or a haptics package; gate behind a setting.
- **Win/celebration confetti (uGUI, no particle asset):** spawn N small colored rounded-rect `Image` "chips" under the canvas as the **last sibling** (so they render above overlays), animate fall+drift+spin+fade in one coroutine, self-destruct after ~2.4s. Drive with `Time.unscaledDeltaTime` so it plays during a paused/aftermath state. **PITFALL:** with chips anchored to the canvas TOP (anchor 0.5,1), a **positive** `anchoredPosition.y` is ABOVE the top edge = off-screen — start chips on-screen with **negative y** and a downward initial velocity so they rain immediately.
- **Button press feedback:** a tiny `IPointerDown`/`IPointerUp` component that scale-punches the button (~0.93 down, springs back on up) + light haptic + tap SFX; attach to every button at build time. Big perceived-quality win for near-zero cost.
- **AAA animation kit (cheap, no tween library — coroutines + easings).** Add `EaseOutBack`/`EaseOutElastic` helpers and drive *every* juice coroutine with `Time.unscaledDeltaTime` so it still plays during paused/win/aftermath states (`Time.timeScale` is often 0 there). Effects **compose** when they touch different properties — a `Pop` (scale overshoot) and a `Shake` (localPosition offset) run **simultaneously** on the same object for life/heart-loss feedback. Patterns: **grid "deal-in"** = set each cell `localScale=0`, then a scale-to-one coroutine with EaseOutBack delayed by the **diagonal index `row+col`** so the board sweeps in; **overlay reveal** = fade a `CanvasGroup` 0→1 for the dim *and* spring the CARD child in from `scale 0` (never scale the full-screen dim itself — it looks like a zoom, not a reveal); **win celebration wave** = on win, stagger a `Pop` across the winning pieces (`foreach winning cell: PlayPop(); yield WaitForSecondsRealtime(~0.06f)`) so the solution "comes alive" in a sweep — pairs with confetti + the overlay reveal for a juicy AAA win moment.

Checklist: `references/checklists/casual-game-feel.md`.

## Camera

Simple smoothed follow covers most casual games:

```csharp
void LateUpdate()
{
    var target = player.position + offset;
    transform.position = Vector3.SmoothDamp(transform.position, target, ref _vel, smoothTime);
}
```

For shake, look-ahead, or multi-target framing, **Cinemachine** is the optional upgrade. The MCP `manage_camera` Tier-2 features require the Cinemachine package installed; add it via `manage_packages` first.

## Scene / prefab assembly through MCP

Build composite objects with one batch, then save as a prefab:

```text
batch_execute(commands=[
  { manage_gameobject(action="create", name="Coin", primitive_type="Cylinder") },
  { manage_components(action="add", target="Coin", component="Rigidbody",
      properties={ isKinematic:true, useGravity:false }) },
  { manage_components(action="add", target="Coin", component="SphereCollider",
      properties={ isTrigger:true }) },
  { manage_components(action="add", target="Coin", component="Coin") },
], fail_fast=true)
manage_prefabs(action="create", target="Coin", path="Assets/Prefabs/Coin.prefab")
```

Up to 25 commands per batch (100 max); not transactional, so set `fail_fast=true` for dependent steps. Spawn instances with `manage_gameobject(action="create", prefab_path="Assets/Prefabs/Coin.prefab")`. Configure 2D vs 3D physics defaults with `manage_physics` when needed.

## Verification — "first playable slice done"

- `read_console(types=["error"])` empty after the last script change.
- `manage_editor(action="play")` → `read_console` clean → `manage_scene(action="screenshot")` shows the controllable object → `stop`.
- Real input path exercised: tap/swipe/drag actually moves/affects the player.
- Core loop reachable: input → objective → win/lose **or** restart path works.
- Ideally a PlayMode test via `run_tests(mode="PlayMode")` + `get_test_job`.
- Visible art is registry-sourced (`unity-asset-pipeline`) and passes the `unity-aaa-graphics` scorecard, **or** remaining primitives are explicitly flagged as placeholders in the ledger.

Full list: `references/checklists/new-game-definition-of-done.md`.

## Common Failure Modes

- A static scene or design doc instead of a playable loop.
- Mechanic compiles but no real touch input can trigger it.
- `GetComponent`/`Find` in `Update`, `Instantiate`/`Destroy` per frame → GC hitches.
- Legacy `Input` written on a project set to the Input System (no input at all).
- Unity-6 APIs guessed from 2022.3 memory instead of verified with `unity_reflect`.
- `is null` used on a destroyed `UnityEngine.Object`.

## Final Response

Report the loop sentence, template chosen, scripts/scenes/prefabs created (and that they went through MCP), C# rules applied, input wiring, tuned feel values, and verification evidence (console clean, Play Mode screenshot, test result). Flag any Unity-6 API verified vs assumed.

## Field notes & lessons

- Added "prefer full runtime construction over headless-wired serialized references" (null-on-reopen + async-void swallowed NRE; bootstrap MonoBehaviour, self-healing SO fallback, explicit AudioListener); added uniqueness-repair generation for constraint puzzles (rejection sampling fails at N=9).
- Added uGUI confetti juice (last-sibling chips, unscaled time, negative-y top-anchor pitfall) and a build-time button-press feedback component (scale-punch + haptic + tap SFX).
- Added swipe/drag-to-paint for grid cells (IBeginDrag/IDrag/IEndDrag; uGUI auto-separates tap from drag; RaycastAll+GetComponentInParent for the cell under the finger, cached list+PointerEventData; lock paint mode from start cell, persist once on EndDrag) and a lives/game-over counter (one EndGame(bool), persist lives, restore 0/legacy save to max).
- Added AAA animation kit (EaseOutBack/Elastic, unscaledDeltaTime so juice survives paused states, Pop+Shake compose via scale vs localPosition, grid deal-in by diagonal row+col, overlay = fade dim CanvasGroup + spring the card not the dim); daily puzzle (date seed year*1000+dayOfYear + fixed difficulty, persist daily flag+date, _pendingDaily set-before/consume-inside the async StartNewGame); ILeaderboard seam (callback async, LocalLeaderboard PlayerPrefs best-per-date now, remote drops in behind it; deterministic seed lets the server reject implausible times).
- Added "derived / player-editable assist markers" to Template C — separate cell state (AutoMarked vs Marked); drive off place/remove EVENTS one-time (ApplyAutoMarksOnPlace stamps only NEWLY-blocked cells via IsBlockedByVisibleRulesExcept + CowBlocks) not per-tap recompute, so manual clears stick and restore-from-save trusts the snapshot; RemoveMarksFreedByRemoval clears ANY × (auto OR player) on freed cells but scoped by geometry; re-sync the overlay (RenderAndSyncAuto) on EVERY mutating path incl. drag-paint (treat any × start cell as erase in BeginPaintAt); test engine-free with a real puzzle + mirror Blocks predicate, one PlayMode test via OnCellTapped, mirror to the second board variant.
- Added win/celebration wave — on win, stagger Pop across the winning pieces (foreach: PlayPop(); yield WaitForSecondsRealtime(~0.06s)) so the solution sweeps "alive"; pairs with confetti + overlay reveal for a juicy win moment.
