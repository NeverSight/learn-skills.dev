---
name: unity-game-director
description: "Primary entrypoint for building casual iOS games in Unity. Use by default for any Unity work: build-a-game, prototype, vertical slice, upgrade, polish, premium, 2D or 3D casual, hyper-casual, puzzle, runner, arcade, release-ready, or App Store requests. Triggers when the working directory is a Unity project (Assets/, ProjectSettings/, Packages/manifest.json present). Detects the Unity version, drives the Unity Editor through the unity-mcp-bridge skill, routes through gameplay/layout/composition/graphics/UI/audio/3D/2D-asset/asset-pipeline/debug/QA phases, and verifies a real playable slice with Play Mode tests and screenshots instead of producing only design docs. Loads sibling unity-* skills so the user does not pick skills manually."
---

# Unity Game Director

Own the end-to-end outcome of a casual iOS game built in Unity. Build a verified playable loop, route the right phases, drive the Editor through MCP, and never call a design document or a primitive-only scene a finished game.

## Core doctrine (learned from real agent-driven Unity projects)

These three rules override convenience. They are why this skill set exists.

1. **Ship a verified playable slice early, not documents.** The most common failure of AI game studios is generating epics, ADRs, and specs for days with no running game. Get a controllable character / interactable on screen in the first working session, verify it runs, then iterate. Planning is in service of a playable build, never a substitute for one.
2. **Keep gates lean for a solo dev.** Do not stack a confirmation prompt at every micro-step. Ask the user at genuine branch points (game concept, art direction, scope, irreversible/billable actions) and otherwise proceed with sensible defaults. Batch decisions.
3. **Edit Unity through the Editor, not raw YAML.** `.unity` scenes, `.prefab`, `.asset`, and `.meta` files are GUID/fileID-linked YAML — hand-editing corrupts references. All scene/prefab/component changes go through the `unity-mcp-bridge` (CoplayDev unity-mcp tools) or generated Editor scripts. C# scripts are plain text and safe to edit, but are not "done" until they compile clean in the Editor.

## Step 0 — Confirm this is a Unity project and pin the version

Run the detection probe before planning. Branch all engine guidance on the detected version.

```bash
bash $UNITY_GAME_SKILLS_HOME/unity-game-director/scripts/detect_unity_project.sh
```

It reports: Unity project yes/no, `m_EditorVersion` from `ProjectSettings/ProjectVersion.txt`, render pipeline, key packages (Input System, Addressables, URP, Cinemachine, glTFast, Test Framework), iOS build target presence, and the art-pipeline artifacts (`art-spec.yaml` / `composition.yaml` / `registry.yaml` / canon-sheet count) with an `ART_PIPELINE=RESUME|FRESH` verdict. On RESUME, resume from the found artifacts — never re-derive style or regenerate approved assets (see Phase Routing).

**Version gate (critical):** the model's built-in Unity knowledge is roughly Unity 2022.3 / early Unity 6.0. For Unity 6 (6000.x) the Input System, UI Toolkit, DOTS, RenderGraph, and Build Profiles differ, and the **6.1–6.5 tech-stream** (6000.1–6000.5) moves further: hard-obsoleted APIs (e.g. IMGUI `TreeView` became generic in 6.5), new core packages (Serialization is core in 6.5), expanded 2D physics worlds, etc. So when on Unity 6.x:

- **Pin packages to the EDITOR's own recommendations, not memory.** Read `<EditorPath>/Unity.app/Contents/Resources/PackageManager/Editor/manifest.json` for the exact versions this Editor ships, and align `Packages/manifest.json` to them. A package version that predates the Editor can fail to compile and throw the project into Safe Mode (see `unity-debug-profiler`). Delete `packages-lock.json` after manifest edits to force a clean re-resolve.
- **Verify APIs against the matching docs / live Editor** before writing C#, shaders, or UI — `unity_reflect`/`unity_docs` (MCP) or `https://docs.unity3d.com/<version>/Documentation/` (e.g. `.../6000.5/...`). Do not write from memory.
- Record the exact version in the ledger and state which knowledge gap applies.

This skill set was validated on Unity 6.5 (6000.5). Keep its guidance current with the installed Editor's version — when a newer point release changes an API or package baseline, update the relevant `unity-*` skill rather than working around it silently.

## Step 1 — Stand up the execution layer (MCP)

Load `unity-mcp-bridge/SKILL.md` and confirm the Editor is reachable before any build work:

- The Unity Editor must be **open and running** with the `com.coplaydev.unity-mcp` package installed; MCP talks to a live Editor, not files on disk.
- Confirm the MCP status reads **Connected** and the `mcpforunity://editor/state` resource shows `ready_for_tools=true`, `is_compiling=false`, `is_domain_reload_pending=false` before issuing commands.
- Enable the tool groups the work needs — only `core` is on by default. Enable `vfx`, `animation`, `ui`, `testing`, `scripting_ext`, `docs` via `manage_tools(action="enable_group", ...)` as phases require.
- Expect a ~5s connection drop after every script compile / package change (domain reload); build in wait-and-retry. See `unity-mcp-bridge/references/reliability.md`.

**MCP-awareness (applies to every unity-* phase):** prefer the live Editor through `unity-mcp-bridge` when connected. First confirm `manage_scene`/`read_console` and `mcpforunity://editor/state` through the active host's tool/resource discovery, then verify the Editor state is ready. Registration alone does not prove connection. If MCP is absent or unreachable, do one of:

1. **Give the user setup instructions** to bring it up (see `unity-mcp-bridge`): install `com.coplaydev.unity-mcp`, register `http://127.0.0.1:8080/mcp` with the active host or use Unity's client configurator, then use Unity **Window → MCP for Unity → Start/Connect** until it reads Connected.
2. **Use the no-MCP fallback** (author C# + a `[MenuItem]` builder, then headless `Unity -batchmode -runTests`/`-executeMethod` and grep logs) so you still make verified progress.

Either way, say explicitly which path you used; never claim live-Editor actions (scene edits, screenshots, Play Mode) that did not happen.

## No-Editor fallback — bootstrap a project on disk

When Unity is not installed and/or no live MCP is available (common in headless/CI/agent runs), you
can still author a complete, openable project from files alone — do this instead of stalling:

- **Create a valid project skeleton:** `Packages/manifest.json` (URP/2D, Input System, TMP, Test
  Framework, `com.coplaydev.unity-mcp`, …), `ProjectSettings/ProjectVersion.txt` (pin a Unity 6 LTS;
  Hub tolerates a near patch), and an `Assets/` tree. Unity regenerates the rest of ProjectSettings
  on first open. Use asmdefs (a `noEngineReferences` Core for pure logic that unit-tests fast).
- **Author all C# and EditMode tests directly** — these are plain text and safe to write.
- **Assemble the scene with a `[MenuItem]` Editor scene-builder**, not by hand-editing `.unity`/
  `.prefab` YAML (which is GUID/fileID-linked and corrupts easily). Build the canvas, prefabs,
  ScriptableObjects and wire private `[SerializeField]` refs via `SerializedObject` in code. The user
  opens the project once and clicks the menu item to get a wired, playable scene.
- **Generate assets to disk** (image/audio/3D) into `Assets/`, with an "Import Generated Art" menu
  that sets mobile import settings (Sprite, iOS ASTC) and wires the theme.
- **State the boundary honestly:** report that the project is code-complete but **not yet compiled or
  run**, and list the one-time manual steps (install Unity, open, run the build menu, Play). Never
  claim scene work, a clean compile, or screenshots that did not happen.
- **When Unity IS installed (just no MCP), use the proven batch-mode playbook:**
  `unity-gameplay-systems/references/headless-editor-recipes.md` — URP 2D asmdef split, headless URP
  activation, NewScene prefab-ref invalidation + VerifyWired, synchronous ImportPackageImmediately,
  `RenderPipeline.StandardRequest` screenshots, batch-run mechanics (verified on a real 6000.5 build).

## Step 2 — Decide 2D vs 3D and load the right sibling skills

Casual iOS games split into two asset pipelines. Route on the concept:

- **Pixel-art 2D casual** (native low-res sprites, tilesets, directional sheets, sprite animation): lean on `unity-pixel-art` (PixelLab final assets) + Unity 2D (Sprite Renderer / Sprite Atlas / Pixel Perfect Camera). Use `unity-image-generator` only for Gemini exploration/concepts. Do not route final pixel sprites through Tripo downscales.
- **Non-pixel 2D casual** (match-3, puzzle, tappers, hyper-casual): lean on `unity-image-generator` (static sprites, UI, backgrounds), Unity 2D, UI Toolkit or uGUI. Use `unity-3d-generator` only for non-pixel pre-rendered actors/props when consistency/animation requires it.
- **3D casual** (runner, stacking, .io, physics toys): lean on `unity-3d-generator` (Tripo text/image→3D, rigging, animation), URP mobile rendering.
- **Mixed** projects load the relevant pixel / image / 3D generators.

Load these sibling `SKILL.md` files before implementation for broad/premium work. Resolve them relative to this skill first, then from `$UNITY_GAME_SKILLS_HOME/<name>/SKILL.md`:

- `unity-mcp-bridge/SKILL.md` — always, it is the execution layer.
- `unity-gameplay-systems/SKILL.md` — architecture, C#, Input System, scene/prefab assembly, 2D + 3D casual templates, game feel.
- `unity-game-layout/SKILL.md` — **board/grid coordinate systems**: load whenever a game has a grid/board, pieces on tiles, tap-to-cell picking, isometric/2.5D/faux-perspective layout, depth sorting, or camera-fit/safe-area concerns. It owns the single-source-of-truth `CellToWorld`↔picking discipline; route any "pieces don't sit on tiles / taps hit the wrong cell / board misaligned" bug here.
- `unity-scene-composition/SKILL.md` — visual hierarchy beyond coordinate correctness: camera profile, layers, focal path, density, color zoning, occlusion, and BeautyCell screenshot acceptance. Load before asset scale-out or scene assembly.
- `unity-asset-pipeline/SKILL.md` — the hard boundary from generated files to approved runtime prefabs: asset contracts, sprite/mesh/import QA, prefab factory, BeautyCell visual regression, and approved-asset registry. Load before importing or placing generated assets.
- `unity-graphics/SKILL.md` — URP mobile rendering, lighting, materials, perf-safe visuals.
- `unity-ui-designer/SKILL.md` — UI Toolkit / uGUI, safe areas/notch, touch controls.
- `unity-debug-profiler/SKILL.md` — console errors, domain-reload recovery, profiler, mobile perf.
- `unity-qa-release/SKILL.md` — Play Mode tests, iOS build (IL2CPP/ASTC/Xcode), App Store readiness.

Load the asset generators before deciding "assets not needed" when the game has characters, enemies, props, sprites, backgrounds, icons, UI art, music, or SFX:

- `unity-pixel-art/SKILL.md`, `unity-3d-generator/SKILL.md`, `unity-image-generator/SKILL.md`, `unity-audio-generator/SKILL.md`.

**Phase ordering for foundations & design.** For a new or team project, establish `unity-project-setup` **first** — source control (.gitignore/LFS/meta-file discipline), folder + asmdef architecture, package management, versioning, secrets-per-env, and CI/CD basics — before scaffolding gameplay, so the engine-free Core asmdef and clean git history exist from day one. And route `unity-game-economy` in at **design/concept time alongside Step 2.x** (with the aesthetic north-star and novel-mechanic scoping): the economy & meta-progression — currencies, sources/sinks, progression pacing, reward schedules, IAP catalog — shape the core loop, so design them up front rather than bolting them on after a slice exists.

## Step 2.5 — Scope a novel or ambiguous mechanic BEFORE building it

Trigger this whenever a request names a mechanic you cannot fully simulate in your head — anything "unusual," "new," a twist on a known genre, or where you'd be guessing at the rules (a reference puzzle game's cross-face "Cube" mechanic is the canonical example: the director jumped to building, and the first rule designs were so under-constrained the puzzle had ~14,000 solutions — only *measured* after building). Do NOT start art/UX/scene work until this gate passes. The cost of skipping it was multiple full rule redesigns plus repeated rendering reworks.

This is the standard "prototype the riskiest thing first / find the fun before you commit to production" discipline ([Rami Ismail on prototypes vs. vertical slice](https://ltpf.ramiismail.com/prototypes-and-vertical-slice/); [Tono — vertical slice](https://tonogameconsultants.com/vertical-slice/)): a throwaway prototype answers *can this even work*, cheaply and disposably, before any fidelity is invested.

1. **Write a crisp one-paragraph spec + a worked example — get it agreed before building.** State the rules as testable constraints, not vibes. Include a concrete worked example the user can check ("a 5×5 grid has exactly one piece per row and per column; regions wrap across edges; no two pieces touch, including across an edge; here is one valid filled board: …"). A one-page spec with explicit *design pillars* is the standard filter — every later mechanic/art decision is checked against the pillars, and anything that doesn't serve them is cut ([gamedesignskills — design pillars](https://gamedesignskills.com/game-design/design-pillars/); [one-page GDD](https://gamedevbeginner.com/how-to-write-a-game-design-document-with-examples/)). If you cannot write the worked example, you do not understand the mechanic yet — go to step 4.

2. **Name the make-or-break property and MEASURE it with a throwaway prototype FIRST.** Every novel mechanic has one property that decides whether it works at all. For a logic puzzle that property is *"does every generated level have exactly one solution?"* — and the only way to know is to count, not to assume. Write a disposable solver/counter (pure C#, no engine refs, no art, no UI — runs in an EditMode test or `execute_code`) and measure before committing to anything visual:
   - Counting solutions with a backtracking solver capped at 2 is the established way to prove uniqueness before a level ships ([101computing — Sudoku generator](https://www.101computing.net/sudoku-generator-algorithm/); [thonky — solution count](https://www.thonky.com/sudoku/solution-count)). The reference project's eventual approach is exactly this: `CubeSolver.CountSolutions(regions, cap=2)`, `TrySolve`, and `FindAlternate` for uniqueness repair (`Assets/<YourGame>/Scripts/Core/CubeSolver.cs`, `CubeGenerator.cs`). Had the counter been written *first*, the 14,000-solution "ring" design would have been rejected in minutes instead of after a full build.
   - Generalize the property by mechanic type: puzzle → unique/solvable solution count; physics toy → does the core interaction feel right at one tuned instance; runner/arcade → is the moment-to-moment loop fun in a gray-box. Measure or play-prove that ONE thing in a gray-box before art, audio, or polished UI.

3. **Decompose the mechanic into independently-verifiable pieces** (the reference Cube mechanic split into: geometry/adjacency math → solver/counter → generator → board state → presentation). Build and unit-test the pure-logic pieces (the `noEngineReferences` Core asmdef) and prove the make-or-break property on them BEFORE any GameObject, shader, or tap path exists. Presentation/interaction reworks are expensive; rule reworks on pure C# are cheap — front-load the cheap ones.

4. **Surface ambiguity back to the user instead of guessing.** When the spec has a genuine fork (the reference Cube mechanic went ring → 2-pieces/face → full-Queens-per-face; board size 4×4 vs 5×5 hinged on how many distinct layouts exist — [Hertzsprung's problem / OEIS A002464]), present the 2–3 viable rule variants with their concrete trade-offs (measured solution counts, layout variety, difficulty) and let the user choose. One clarifying question at the real branch point is far cheaper than building the wrong rules and tearing them out. This is a legitimate "genuine branch point" under Core Doctrine #2 — batch the fork with the concept/art-direction questions.

**Gate to pass before art/UX:** spec + worked example agreed ✓, make-or-break property measured on a throwaway prototype (not assumed) ✓, mechanic decomposed with pure-logic pieces unit-tested ✓, ambiguous forks surfaced to the user ✓.

## Step 2.6 — Aesthetic direction is a first-class EARLY deliverable

A reference casual game's look churned through many passes (several distinct directions and multiple palette/typography reworks; glossy buttons → flat and back) because no named visual target was agreed up front — every pass was a fresh guess at "what does *pleasing* mean here." Fix: pin the aesthetic target as an explicit deliverable at concept time, the same way you pin gameplay scope, then converge in **1–2 passes** with a rubric and screenshots instead of many. Most designs converge within two iterations *when there is a target to converge toward* ([design review iteration](https://www.markup.io/blog/design-review-checklist/)). **Mandatory before ANY production asset:** route to `unity-art-direction`, which records the north-star as a locked, machine-readable `art-spec.yaml` single source of truth (canonical path `Assets/<Game>/Art/_ArtDirection/art-spec.yaml`: style preset, palette, materials, lighting, scale, mobile budgets, acceptance) and gets it user-approved. Exploratory concepts/style boards may precede the spec; production art may not. Then follow the ordered Phase Routing DAG: `unity-asset-designer` (character canon), `unity-scene-composition` (`composition.yaml`), `unity-asset-pipeline` (contracts/registry) before any art is mass-generated. Record the art-spec path + approval status in the ledger. This gate applies to art only — it never blocks gray-box gameplay prototyping.

1. **Agree a named visual north-star up front (a genuine branch point — ask the user).** Capture it in the ledger as a short, concrete art-direction statement, not an adjective:
   - **Reference style:** a named style + 1–2 real touchstones — pick what fits your game, with no single style as the default (e.g. flat-pastel à la *Two Dots* / *I Love Hue*, glossy candy à la *Royal Match*, minimal ink, or neon-retro). A mood board / reference set is the standard alignment tool — it pins tone, palette, and texture before any asset is made and prevents exactly this kind of churn ([Milanote — game design mood board](https://milanote.com/guide/game-design-moodboard); [Numberanalytics — mood boards in game art](https://www.numberanalytics.com/blog/ultimate-guide-mood-boards-game-art)).
   - **Palette:** 4–7 named colors (ground, panel, text/ink, 1–3 accents) with the contrast intent stated concretely — e.g. "a dark ink on a light ground, with a few saturated accent regions", whatever the chosen direction is.
   - **Typography:** one font family + the mood word it carries (e.g. a rounded sans for a calm/friendly mood, or a bold geometric for an energetic one — and confirm it covers any non-Latin scripts your game needs).
   - **Mood / "what pleasing means here":** 3–5 words (e.g. calm, high-contrast, minimal — or playful, bold, energetic) and an explicit anti-target ("not busy, not glossy, not desaturated") — the anti-target is what stops the next pass from drifting.
   - **Finish:** flat vs glossy vs material — decide once (the reference project flip-flopped glossy↔flat across iterations for want of this).

2. **Hold a fast screenshot-review loop against a concrete rubric.** After each visual pass, capture a real Screen-Space-Overlay screenshot via MCP (`manage_camera screenshot`) at a target portrait resolution and score it 1–10 on a fixed rubric, then list the top 2–3 concrete fixes for the next pass. Score these axes ([design review checklist](https://www.markup.io/blog/design-review-checklist/); divergent-then-convergent critique, [IxDF — design critiques](https://ixdf.org/literature/topics/design-critiques)):
   - **Palette & contrast** (matches the north-star colors; text readable on its ground)
   - **Typography** (one family, consistent sizes/weights, no tofu/missing glyphs)
   - **Hierarchy & spacing** (clear focal point, intentional negative space, aligned)
   - **Finish consistency** (every element flat *or* every element glossy — never mixed; this was the reference project's recurring slip)
   - **Cohesion with the north-star** (would a stranger name the agreed reference style from this screenshot?)
   - Gate: do not call visuals "done" below the agreed bar (the reference project used an ~8/10 average). Converge in 1–2 passes; if you're on pass 3+, the north-star wasn't concrete enough — go back to step 1, don't keep guessing.
   - **Scorecard precedence:** this rubric applies only until an `art-spec.yaml` exists — then it is SUPERSEDED: per-asset acceptance is `unity-art-direction`'s 0–2 quality gates, and the FINAL whole-screen authority is the `unity-aaa-graphics` visual scorecard. One hierarchy, no dueling gates.

3. **Runtime theme = a DERIVED view of `art-spec.yaml`** so passes don't regress: keep runtime theme values in code (e.g. a `GameTheme.cs` defaults) as the runtime SSOT *derived from* the art-spec — its color hexes must equal the art-spec palette hexes (`palette.roles` + arrays), never hand-invented. Delete any `Resources/*Theme.asset` that would shadow them with stale serialized values (a real bug from a reference project — the asset overrode the updated `.cs` palette).

4. **Menu & text consistency** is owned by `unity-ui-designer` (recurring menu/typography drift was fixed there — display-name single-sourcing, safe-area, TMP font setup, 44pt targets). Cross-reference it from the orchestration checklist below; do not re-derive UI rules here.


## Visual Quality Gate (art is first-class)

Before claiming a generator key is unavailable, run the credential probe and paste its literal output:

```bash
bash $UNITY_GAME_SKILLS_HOME/unity-game-director/scripts/probe_asset_credentials.sh
# -> TRIPO_API_KEY=SET|MISSING / GEMINI_API_KEY=SET|MISSING / PIXEL_LABS_API_KEY=SET|MISSING / ELEVENLABS_API_KEY=SET|MISSING
```

"Key unavailable" is not a valid skip reason unless the probe shows `MISSING`. The probe checks `GEMINI_API_KEY`, `PIXEL_LABS_API_KEY`, and `TRIPO_API_KEY`. **Pixel-art final assets → PixelLab (`unity-pixel-art`)**; Gemini is exploration/concept/reference only. **Non-pixel motion/3D → Tripo** (rig + animate; pre-render only for high-res/painterly 2D). Do not default to Gemini-only 2D generation, and never make pixel art by Tripo/3D downscale.

**Real generated art is the DEFAULT for EVERY primary visible surface — not one hero asset.** Each surface the player actually looks at should be a real generated/sourced asset with evidence (a Tripo task ID + imported GLB/FBX path, or a generated sprite/texture path): the background/terrain/ground, the path/track, the player, enemies/obstacles, towers/units, signature props, and the key UI. A single generated hero amid untextured everything-else is NOT a premium scene.

**Procedural / runtime shapes are a FALLBACK, not the default.** They are acceptable only when a key is `MISSING`/quota-blocked (show the literal evidence) or for genuinely low-value repeated props where an atlas / GPU instancing is the right call. A procedural placeholder is never "premium," "polished," or "AAA."

**Animation is part of the bar — assets that ACT must move.** Any asset that acts in the game (characters, enemies, towers, interactables) must be animated with the states its role requires (idle/move/attack/hit/death; towers idle/aim/fire), and any action with a gameplay effect must fire that effect on the correct animation frame (release the arrow on the loose frame, deal damage on the contact frame) — not on raw input. Route animation work to `unity-animation`.

**Amateur-look auto-fail anti-patterns.** If a screenshot shows any of these, the visuals FAIL — do not call them done:
- flat solid-color ground or background,
- procedural primitive blobs (cubes/spheres/capsules) standing in for primary surfaces,
- one generated asset surrounded by untextured everything-else,
- a hard-oval vignette used as the only "lighting,"
- a static asset where motion is expected (e.g. a tower/enemy/character with no idle/attack/death), or a projectile/damage that fires on input instead of on the animation's release/contact frame.

**Route premium visual work to `unity-aaa-graphics`.** For any premium / polished / AAA / "make it look good" / "looks basic" request, or whenever a screenshot trips the anti-patterns above, hand off to `unity-aaa-graphics`. It owns the per-surface asset-sourcing decision, the AAA prompt library + genre art kits, render polish, and the visual scorecard that fails flat/programmer-art scenes.

**Allowed skips** (the only valid reasons to ship a surface without real art): user explicitly asked offline-only, the probe shows the key `MISSING`, a real API/quota error with the command shown, or a repeated low-value prop better done procedurally / by atlas instancing.

## Phase Routing — the ordered pipeline (DAG, gated)

Route phases in this order. Each art phase has required INPUT/OUTPUT artifacts and a GATE that must pass before the next art phase. **Gates apply to ART production and scene ART assembly ONLY** — per Core Doctrine #1, gray-box gameplay is NEVER blocked on art: from step 0, `unity-gameplay-systems` (+ `unity-game-layout` for boards, `unity-game-economy` at design time) prototypes the loop in parallel with primitives flagged as placeholders in the ledger.

**RESUME rule:** when `detect_unity_project.sh` reports existing artifacts (`ART_PIPELINE=RESUME`), resume from them — never re-derive style, never regenerate an approved asset, never rewrite an approved art-spec unless the user asks.

0. **`unity-project-setup`** — source control, folders/asmdefs, packages, secrets, CI. Provisions the reserved art paths (`Assets/<Game>/Art/{_ArtDirection,Approved,Source}`) so every later artifact has a deterministic home.
   ∥ *Parallel gray-box track starts here and never waits on art.*
1. **Director Steps 2.5–2.6** — novel-mechanic scoping + aesthetic north-star. OUT: north-star statement in the ledger.
2. **`unity-art-direction`** — OUT: `Assets/<Game>/Art/_ArtDirection/art-spec.yaml` + `palettes/master-palette.png`; derived views (`style-guide.md`, `GameTheme.cs` hexes, UI tokens) regenerated FROM it. **GATE: art-spec approved by the user. No production asset before this.**
3. **`unity-asset-designer`** — IN: approved art-spec. OUT: canon per recurring character (`_ArtDirection/sheets/<char_id>_canon.png`, registered in the art-spec `characters` block); game golden anchor approved, then family goldens derived from it. **GATE (track-aware): canon exists per recurring character — pixel track: a PixelLab anchor/reference sheet; non-pixel 2D & 3D: a Gemini turnaround sheet.**
4. **`unity-scene-composition`** — IN: art-spec. OUT: `composition.yaml` agreeing with it (same `style_id`; `key_light_direction` equals `craft.light_direction`).
5. **Generators** — IN: art-spec (pass `--art-spec`) + conditioning artifacts (golden anchor, master palette, canon sheets); NO hand-typed style. Credential probe first (Visual Quality Gate above). `unity-pixel-art` (pixel finals, bitforge on the golden anchor, palette on every call) · `unity-image-generator` (static non-pixel 2D, canon/style refs attached; concepts for the others) · `unity-3d-generator` (image→3D from style-locked turnarounds only) · `unity-audio-generator` (SFX/music/TTS → AudioClips).
6. **Per-asset QA** — deterministic checks first (validate_sprite, palette/alpha/scale), VLM critique second; per the generator skills' gates.
7. **`unity-asset-pipeline`** — IN: QA-passed source + art-spec. OUT: asset-contract → prefab factory → **approved registry** (`Assets/<Game>/Art/Approved/registry.yaml`). **GATE: `validate_asset_manifest.py` exit 0.**
8. **Scene ART assembly** — `unity-gameplay-systems` + `unity-scene-composition` + `unity-game-layout` place visible art **from the registry ONLY** (logic prefabs may wrap registry assets); PPU read from art-spec.
9. **Whole-screen gate** — `unity-aaa-graphics` scorecard on real Play-Mode screenshots = FINAL visual authority. `unity-graphics` (URP lighting/materials/post) and `unity-animation` (every acting asset moves; effects fire on the correct frame) feed it.
10. **`unity-ui-designer`** (HUD/menus/safe-area; owns menu & text consistency; tokens derived from art-spec) → **`unity-qa-release`** (tests, iOS build, App Store readiness).

**Scorecard precedence (one hierarchy):** `unity-aaa-graphics` scorecard = final whole-screen gate; `unity-art-direction` 0–2 gates = per-asset feeder; director Step 2.6 rubric = pre-spec only, superseded once art-spec exists.

### Track & genre scaling (one DAG, scaled scope)

Branch the DAG on the Step 2 pipeline decision (= art-spec `craft.finish`):

- **2D-pixel:** canon = PixelLab anchor sheets; PPU/tile size/outline from the art-spec craft block; Point-filter/no-compression/pixel-perfect import (`unity-pixel-art`). For sprite-on-3D/HD-2D, combine that asset contract with `unity-scene-composition` and `unity-graphics`.
- **2D-HD (non-pixel):** canon = Gemini turnaround/canon sheets; finals via `unity-image-generator`; motion via Tripo rig/pre-render (`unity-3d-generator` + `unity-animation`), never frame-by-frame Gemini.
- **3D:** canon = style-locked turnaround feeding Tripo image→3D; scale enforced from the art-spec scale block; imported materials re-shaded to spec via `unity-graphics`.

Scale VOLUME by genre — compression shrinks families and canon passes, never gates 2 and 7:

- **Casual/hyper-casual puzzle:** compressed — art-spec + master palette + 1–2 asset families (pieces, board/background, key UI); steps 3–4 collapse into one canon pass (mascot + piece set); `composition.yaml` stays REQUIRED but may be minimal (camera profile + layers + key_light_direction) — the asset-pipeline validator's coherence checks are default-on and fail registries without a resolvable composition profile.
- **Mid-core / pixel RPG:** full DAG — canon per recurring character, golden-first 80/20 families, `composition.yaml` required.
- **AAA / showcase 3D:** full DAG + `unity-aaa-graphics` per-surface sourcing decision + BeautyCell visual regression per family.

### Supporting phases (route any time; no art gate applies)

- `unity-gameplay-systems`: playable slice, C# architecture, Input System, entity/state systems, game feel — 2D and 3D casual templates.
- `unity-debug-profiler`: blank scene / null refs / compile errors, domain-reload recovery, profiler, draw calls, memory, mobile thermal/perf.
- `unity-qa-release`: Play Mode + EditMode tests, device-resolution checks, iOS build pipeline, App Store / privacy-manifest readiness.
- `unity-game-economy`: economy & meta-progression design (currencies, sources/sinks, pacing, IAP catalog) — at design time, alongside Step 2.x.
- `unity-analytics-liveops`: analytics/retention instrumentation, remote config + A/B, crash SDKs, ATT/SKAdNetwork.
- `unity-localization`: String/Asset Tables, Smart Strings, per-script fonts/RTL — externalize strings early.
- `unity-aso-growth`: store listing/icon/screenshots/preview, Product Page A/B, soft-launch UA. Retention before acquisition.

If a sibling file cannot be loaded, record the path/reason and use this director's routing as the fallback for that phase.

## Verification (a phase is done only with evidence)

- Project compiles clean: `read_console(types=["error"])` empty after the last script change.
- Play Mode runs: `manage_editor(action="play")` → `read_console` clean → `manage_scene(action="screenshot")` shows a real scene that PASSES the `unity-aaa-graphics` visual scorecard (textured primary surfaces, asset cohesion, real lighting/depth) — not merely "non-primitive" → `stop`. Confirm key acting assets are animated (idle/move/attack as the role requires), not static/T-pose, with gameplay effects firing on the correct animation frame — via ANIMATOR-STATE PlayMode assertions (state-hash entry/exit per input-reachable state), not eyeballing. Screenshot evidence MUST include at least one UI-INCLUSIVE capture (overlay canvases are invisible to camera RT renders — see unity-ui-designer) and an ASPECT SWEEP (16:9 + 19.5:9 + one extreme) for mobile targets.
- Core loop reachable: input → objective → win/lose or restart path exercised (ideally a PlayMode test via `run_tests` + `get_test_job`).
- Tests green before "done": EditMode/PlayMode via the `testing` group.
- Art pipeline validates (for any production-art claim): `art-spec.yaml` exists and every asset contract passes `validate_asset_manifest.py` with exit 0 (`unity-asset-pipeline`).
- Composed-scene critique (for any art-assembled scene claim): run `unity-image-generator/scripts/critique_image.py --scene-mode --reference <golden/canon>` on the Play-Mode screenshot and keep the JSON report — it scores focal read, layer contrast, GROUNDING (feet-on-ground — a floating character shipped past every deterministic gate once), and cohesion. Low scores trigger re-roll/review, not silent acceptance.
- Registry resolution: run `unity-asset-pipeline/scripts/check_scene_registry.py <scene.unity> --registry Assets/<Game>/Art/Approved/registry.yaml` on every saved gameplay scene (exit 0 required; an empty registry is a legal gray-box state — warned, not failed; `PLACEHOLDER`-named objects using engine-builtin primitives are reported, not failed, but any FILE-based art reference must resolve to the registry regardless of naming — never wire raw generated files even as placeholders). For live/unsaved scenes, additionally walk the renderers via MCP (`manage_scene`/`manage_gameobject`) and cross-check every visible sprite/mesh/material against the registry — each resolves to a registry entry OR is a ledger-flagged placeholder. Anything else = assembly-time bypass; fix before "done."
- iOS readiness for release claims: IL2CPP backend, ASTC textures, deployment target >= iOS 13, bundle id/product/version set, Xcode project builds. Signing/`.ipa` is a manual macOS+Xcode step — flag it, do not claim it done.
- Screenshots dominated by primitives, flat planes, or empty scenes = not done.

## Ledger (keep it lightweight)

Track only what proves the outcome:

```text
- Unity: detected yes/no, version, render pipeline, key packages, iOS target
- MCP: connected yes/no, tool groups enabled
- Pipeline: 2D / 3D / mixed
- Novel-mechanic scope (if any): spec+worked-example agreed / make-or-break property + measured value / decomposed+unit-tested / forks surfaced
- Aesthetic north-star: reference style / palette / type / mood + anti-target / latest rubric score
- Art pipeline: art-spec path + approval status / master palette / golden anchors / canon sheets / registry state / flagged placeholder primitives / latest aaa-graphics scorecard
- Sibling skills loaded: gameplay / graphics / ui / debug / qa (+ 3d/image/audio if used)
- Credential probe: TRIPO / GEMINI / PIXEL_LABS / ELEVENLABS = SET|MISSING
- Asset sourcing: hero source + evidence (task id / file) or skip reason
- Phases: gameplay / assets / graphics / ui / debug / qa = pending|done|skipped + evidence
- Verification: compile clean / play-mode screenshot / core loop / tests / iOS readiness
- Remaining risks / manual steps (signing, store assets)
```

## Final Response

Report the ledger, files changed, scenes/prefabs touched (and that they went through MCP), how to run it in-Editor, controls, verification evidence (console clean, screenshots, test results), generated-asset evidence or blockers, iOS/App Store readiness with the manual signing step called out, and remaining risks. Be precise: "loaded" = the SKILL.md/reference was read; "executed" = the work ran in the Editor with evidence. Do not claim premium quality without a screenshot of a real, non-primitive scene.

## Field notes & lessons

- Added two front-loaded gates that real project failures exposed.
  - **Step 2.5 — Scope a novel/ambiguous mechanic before building.** The Cube level was built before its rules were nailed down; the first designs had ~14,000 solutions, discovered only by *measuring after building*, forcing multiple rule + rendering redesigns. New procedure: crisp spec + worked example agreed first; name and **measure** the make-or-break property (here puzzle uniqueness, via a throwaway capped solution-counter — mirrors the eventual `CubeSolver.CountSolutions`/`FindAlternate`) on a disposable pure-logic prototype before any art/UX; decompose into unit-tested Core pieces; surface ambiguous rule forks to the user instead of guessing. Grounded in prototype-the-riskiest-thing-first / vertical-slice practice (Rami Ismail, Tono), design-pillar filtering (gamedesignskills), and Sudoku-style uniqueness counting (101computing, thonky).
  - **Step 2.6 — Aesthetic direction as a first-class early deliverable.** The reference project's look churned through many passes (several distinct directions; glossy ↔ flat) for want of an agreed visual target. New procedure: pin a named north-star (reference style + touchstones, 4–7 color palette with contrast intent, one type family, mood + explicit anti-target, flat/glossy finish decided once) at concept time; converge in 1–2 passes via a fast MCP-screenshot review against a fixed 1–10 rubric (palette/contrast, typography, hierarchy/spacing, finish consistency, north-star cohesion); keep the theme single-sourced in code. Grounded in mood-board alignment (Milanote, Numberanalytics) and convergent design-critique/review-rubric practice (markup.io, IxDF).
  - Added a one-line cross-reference making `unity-ui-designer` the owner of menu/text consistency (failure C — fixed in depth in that sibling skill, not duplicated here), plus matching ledger lines.
