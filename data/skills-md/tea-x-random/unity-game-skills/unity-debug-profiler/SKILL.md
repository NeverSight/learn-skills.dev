---
name: unity-debug-profiler
description: "Debug and profile casual iOS games in Unity through the unity-mcp-bridge. Use for compile errors, console errors, NullReferenceException, MissingReferenceException, missing/broken references, pink/magenta materials, blank or black scenes, won't enter Play Mode, domain-reload issues, MCP connection drops, and for performance profiling: frame rate, draw calls/batches/SetPass, GC allocations, memory and texture memory, mobile thermal throttling, IL2CPP/AOT managed-code stripping, and slow builds. Evidence-driven: read the actual console and profiler, verify Unity 6 APIs via MCP, and re-run to confirm fixes."
---

# Unity Debug Profiler

Find root causes from real evidence and optimize measured bottlenecks, for casual iOS games in Unity, driven entirely through the `unity-mcp-bridge` (CoplayDev unity-mcp). This is the debug/profile phase of `unity-game-director`.

## Doctrine (do not skip)

1. **Evidence-driven.** Read the actual console and profiler before theorizing. `read_console(types=["error"])` is the first move on any "it's broken." Never guess at a cause you could have read.
2. **Lean gates.** Diagnose, fix the root cause in the owning script/component, verify. Don't stack confirmation prompts at every micro-step.
3. **Unity 6 APIs differ from memory.** The model's built-in Unity knowledge is ~2022.3. On Unity 6 (6000.x), the Input System, URP/RenderGraph, profiler, and build APIs differ. Verify any C#/shader/API you write with MCP `unity_reflect` (live reflection) or `unity_docs` before writing it. Trust order: reflection > project assets > docs > memory.
4. **Verify fixes by re-running.** Re-compile, re-read the console clean, enter Play Mode, screenshot. A fix is not done until the evidence is clean.

## Step 0 — readiness

Read `mcpforunity://editor/state` and proceed only when `ready_for_tools==true`, `is_compiling==false`, `is_domain_reload_pending==false`. Read `mcpforunity://project/info` once to branch correctly: `renderPipeline` (URP vs Built-in shader names), `activeInputHandler`, UI stack. The render pipeline value is the single most common root cause of "pink materials."

## Console-first debugging

Compile errors block everything — scene work, Play Mode, and tests all fail or run stale until C# compiles clean. Fix compile errors first.

1. `read_console(types=["error"])` — compile errors AND runtime exceptions land here. Read the full message and the stack trace, not just the first line.
2. `read_console(types=["warning"])` — missing references, deprecated APIs, shader fallbacks often surface here before they become errors.
3. To get a clean signal: clear the console (`manage_editor`/console clear), reproduce the exact action, then read. A pile of stale errors hides the live one.
4. Map the top stack frame to a script + line; that file is where the fix goes.

Load `references/common-errors.md` for the full symptom → cause → fix table.

## Common Unity failure modes

- **NullReferenceException** — a `[SerializeField]` left unassigned in the Inspector/prefab; `GetComponent<T>()` returning null (component absent, or called before it exists); wrong script execution order so a dependency isn't ready in `Awake`/`OnEnable`. Fix: assign the field, null-check or require the component, cache in `Awake` and consume in `Start`, or set Script Execution Order.
- **MissingReferenceException** — referencing a `Destroy`d object, or a broken prefab/scene link (asset moved, GUID changed). Differs from NRE: the field *was* set but the target is gone. Fix: null-check after destroy, re-link the prefab reference, pool instead of destroy.
- **Pink / magenta materials** — shader didn't compile for the active pipeline, almost always a Built-in shader (`Standard`) in a URP project. Fix: Edit → Rendering → Materials → Convert/Upgrade to URP, or set the material to a URP shader (`Universal Render Pipeline/Lit`). Verify `renderPipeline` from project/info first.
- **Blank / black scene** — no camera (or camera disabled / wrong culling mask / clear flags), no light (URP Lit looks black unlit), camera near/far or position wrong, or the wrong scene is loaded/active. Check via the scene-debugging checklist before touching content.
- **Won't enter Play Mode** — a compile error (read console first), or an exception thrown in `Awake`/`OnEnable` that aborts entry, or "Enter Play Mode without domain reload" leaving stale static state. Fix the exception; if domain-reload-off causes stale statics, reset them in `OnEnable` or re-enable reload.
- **Safe Mode on open / mass `CS0619` from a package** — almost always a **package-version vs editor-version mismatch**, not your code. Hand-pinned versions in `Packages/manifest.json` (or a stale `packages-lock.json`) that predate the installed Editor break when the Editor hard-obsoletes an API (e.g. Input System ≤1.11.x using removed `TreeView`/`TreeViewItem` on a newer Unity 6). Fixes, in order: align each package to the Editor's recommended version (read `<Editor>/.../PackageManager/Editor/manifest.json`), delete `packages-lock.json` to force a clean re-resolve, and **drop packages you don't actually need** — a tap-driven uGUI game needs no Input System package (EventSystem + `StandaloneInputModule` handles touch; keep `activeInputHandler` = 0/Both). Verify the fix headlessly (see `unity-qa-release` batchmode verification) before reopening.

Load `references/checklists/scene-debugging.md` for a blank/broken scene.

## Domain-reload / MCP recovery

Cross-reference `unity-mcp-bridge/references/reliability.md`. Every C# compile, package add/remove, or scripting-backend change triggers a Unity **domain reload** that drops the MCP connection for ~5s and invalidates in-flight calls. Recovery pattern:

1. Issue the change (`create_script` / `script_apply_edits` / `apply_text_edits`). Do **not** also call `refresh_unity` — create/edit already import+compile.
2. Poll `mcpforunity://editor/state` until `is_compiling==false`, `is_domain_reload_pending==false`, `ready_for_tools==true`. The first poll(s) will fail/timeout during the drop — retry with backoff for ~10s.
3. `read_console(types=["error"])`; only continue (e.g. `AddComponent` referencing the new type) when clean.
4. If you held a file SHA, **re-fetch with `get_sha`** before `apply_text_edits` — the file may have been reimported (`stale_file`).

A modal Editor dialog ("reload scripts?" / reimport) stalls the bridge until clicked. If a sequence hangs with no progress, ask the user to check the Editor for a dialog. On macOS the WebSocket can also close (1005 / `no_unity_session`) on reload/test boundaries — reconnect and re-poll, don't assume the work failed.

## Profiling

Enable the group first: `manage_tools(action="enable_group", group="profiling")` (gives `manage_profiler`). Use `manage_graphics` for render stats (draw calls / batches / SetPass / triangles).

**MCP reading gotchas (these waste time):**
- `manage_graphics(action="stats_get")` returns `draw_calls`/`batches` = 0 for a Screen-Space-Overlay uGUI game — those counters reflect the SRP camera path, not the overlay canvas. Read the Render profiler counters instead: `manage_profiler(action="get_counters", category="Render")` → **SetPass Calls Count** (the meaningful batching metric; single digits = excellent), Triangles Count, Vertices Count. Output is large — pipe through `jq` for the specific counters.
- `manage_profiler(action="get_frame_timing")` reports `cpu_frame_time_ms` ~200ms in the Editor when the Game view is unfocused — that's WaitForTargetFPS/vsync IDLE, not work. Read `cpu_main_thread_frame_time_ms`, `cpu_render_thread_frame_time_ms`, and `gpu_frame_time_ms` for real per-frame work (sub-1ms each = comfortably 60fps with headroom). Don't mistake the idle-inflated total for a perf problem.

- **Target 60fps on mobile** → 16.6ms/frame budget. Capture a baseline first: FPS/frame time, draw calls, batches, SetPass calls, triangles, GC alloc/frame, texture memory.
- **CPU vs GPU bound:** if frame time tracks CPU main-thread (scripts/physics) it's CPU bound; if GPU time dominates it's fill/geometry bound. Optimize the one that's actually limiting.
- **Draw calls / batches / SetPass:** high SetPass = too many materials → atlas, share materials, GPU instancing, static batching for non-moving geometry.
- **GC allocations:** aim for **zero allocations per frame in steady state**. Per-frame `new`, LINQ, boxing, string concat, and uncached `GetComponent` cause GC spikes → frame hitches. Hunt them in the profiler GC Alloc column.
  - **Per-frame UI text is a double cost** — setting a `TMP_Text/.text` every frame (a timer via `$"{m:00}:{s:00}"` in `Update`) allocates a string *and* dirties the canvas, forcing a full uGUI rebuild every frame. Fix: cache the last value and only assign when it changes (gate on the integer second). This kills both the steady-state GC alloc and the per-frame rebuild. For a frequently-updating readout, put it on its own nested Canvas so its rebuild doesn't dirty the rest of the UI.
- **Texture memory & overdraw:** oversized/uncompressed textures and heavy transparent overdraw are the usual mobile GPU killers.
- **2D uGUI overlay games:** GPU/draw cost is usually trivial (SetPass single digits, sub-ms GPU). The real perf risks are (a) per-frame canvas rebuilds from changing UI every frame and (b) per-frame string/GC allocations — audit `Update()` methods for both *first* before chasing render cost.

Load `references/profiling-guide.md` for how to read stats via MCP, frame-budget math, and reduction tactics. Use `references/checklists/mobile-performance.md` to gate a perf pass.

## Mobile-specific (casual iOS)

- **Thermal throttling** under sustained load — the device downclocks after minutes, so a scene that hits 60fps cold may drop hot. Profile sustained, not just the first frame.
- **Memory ceilings** — iOS kills apps that exceed the device budget; watch total + texture memory.
- **ASTC texture sizes** — iOS textures should be ASTC-compressed and sensibly sized; uncompressed/RGBA32 atlases blow the memory budget (the build pipeline has a known wrong-compression bug — verify ASTC yourself).
- **Physics / Update cost** — `Update` on many objects, uncached lookups, and dense physics are common CPU spikes on mobile.
- **GC hitches** — even small per-frame allocations cause visible stutters on mobile; treat steady-state GC as a bug.
- **On-device profiling** — for real numbers, build a development/profiler-enabled player to the iOS target and connect the Profiler to the device; Editor numbers under-report mobile cost.

## IL2CPP / AOT gotchas (iOS)

iOS requires the **IL2CPP** backend with AOT compilation. The class of bug to flag here:

- **Managed code stripping** removes types/members only reached via reflection or serialization — works in the Editor (Mono, no stripping), throws `ExecutionEngineException` / missing-type at runtime on device. Fix: preserve them via a `link.xml`, `[Preserve]` attributes, or lower the stripping level.
- **Generic / AOT limits** — value-type generics instantiated only at runtime can fail AOT; reflection-heavy serializers (JSON.NET) and `MakeGenericType` are typical offenders.
- **Long build times** — IL2CPP + Xcode is far slower than Editor iteration; budget for it.

Detailed iOS build steps live in `unity-qa-release` — flag the stripping/AOT class of bug here, route the build there.

## Debug workflow

1. **Reproduce** the exact failing action.
2. **Read console** — `read_console(types=["error"])` then `["warning"]`; read stack traces.
3. **Isolate** to the owning script/component (top stack frame; or bisect the scene).
4. **Fix the C#** root cause (verify any Unity 6 API with `unity_reflect`/`unity_docs`).
5. **Wait for compile** — poll editor/state through the domain-reload drop.
6. **Read console clean** — no errors before proceeding.
7. **Verify in Play Mode** — `manage_editor(action="play")` → `read_console` → `manage_scene(action="screenshot")` → `manage_editor(action="stop")`. For loop coverage, `run_tests(mode="PlayMode")` → `get_test_job`.

## Final response

Lead with the root cause or the measured bottleneck. Report: checklists/references used, files changed (and that scene/prefab edits went through MCP), before/after metrics for perf work, console-clean + Play Mode screenshot evidence, and residual risks (e.g. on-device-only, thermal, signing).

## Field notes & lessons

- per-frame `TMP_Text/.text` (e.g. a timer) is a double cost — string alloc + full canvas rebuild every frame; cache the value and only assign on change, nested Canvas for hot readouts.
- for 2D uGUI overlay games, audit `Update()` for per-frame canvas rebuilds and string/GC allocs before chasing render cost — GPU/draw is usually trivial.
- `manage_graphics(stats_get)` reports draw_calls/batches=0 for Screen-Space-Overlay uGUI; use `manage_profiler(get_counters, category="Render")` SetPass Calls Count instead (pipe through jq).
- `get_frame_timing` `cpu_frame_time_ms` ~200ms in unfocused Editor is vsync IDLE, not work — read cpu_main_thread/cpu_render_thread/gpu_frame_time_ms for real per-frame cost.
