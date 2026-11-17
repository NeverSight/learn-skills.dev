---
name: unity-mcp-bridge
description: "Drive a live Unity Editor through CoplayDev MCP for Unity from GPT/Codex, Claude Code, or another MCP client. Use for real Editor actions: scenes, GameObjects, components, prefabs, materials, scripts, Play Mode, tests, console, asset import and builds. Covers HTTP setup, tool groups, editor readiness, domain-reload reconnects, no_unity_session recovery, headless iOS builds, and device-only debug HUDs. This is the execution layer beneath unity-game-director and other unity skills; use the documented headless CLI fallback when MCP is unavailable."
---

# Unity MCP Bridge

This skill is how every other unity-* skill changes the project. It wraps **MCP for Unity** (CoplayDev, package `com.coplaydev.unity-mcp`): agent host → MCP (HTTP/stdio) → Python FastMCP server → WebSocket → Unity C# Editor package → Editor API. **It controls a live, open Editor — not files on disk.**

## Prerequisites

- Unity Editor **open and running** with the package installed. Minimum Unity **2021.3 LTS**; iOS Build Profiles (the build `profile` param) need **Unity 6+**.
- Python **3.10+** with `uv`/`uvx`.
- The MCP status panel (`Window → MCP for Unity`) must read **Connected**.

## Setup for the active agent host (do once per project)

1. **Install the Unity package** — Package Manager → + → Add package from git URL:
   `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#main`
   (or `openupm add com.coplaydev.unity-mcp`).
2. **Run the setup wizard** that auto-opens after import; confirm Python + `uv` are detected (green).
3. **Register the active client.** In Unity, use `Window → MCP for Unity → Configure All Detected Clients`, or configure `http://localhost:8080/mcp` in the host's MCP settings. Claude Code also supports:
   ```bash
   claude mcp add --scope local --transport http UnityMCP http://localhost:8080/mcp
   ```
   Verify the Unity status panel says **Connected**.

**Transport: prefer HTTP.** stdio is single-agent only (new connections stomp old ones) and does not sync tool-group visibility or custom tools reliably.

## Availability check & troubleshooting (do this FIRST, every session)

Before assuming you can drive the Editor, confirm the MCP is actually reachable — registration is not connection:

```bash
curl -s -m 3 -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/mcp   # HTTP transport server alive?
```

Also use the active host's tool/resource discovery. `manage_scene`, `read_console`, and `mcpforunity://editor/state` must be visible; a CLI registration list is secondary evidence.

If the Unity MCP tools (`manage_scene`, `read_console`, …) don't appear in tool search, they are not connected — do not pretend to use them. Diagnose in order:

1. **"✘ Failed to connect" / nothing on :8080** → the Unity-side server isn't running. In Unity open **Window → MCP for Unity**, wait for any compile/domain reload to finish, and **Start/Connect** the server; the panel must read **Connected**. The HTTP server hosts `:8080` — if it won't start, check `uv`/`uvx` (3.10+ Python) are installed and on PATH.
2. **Not registered at all** → use Unity's "Configure All Detected Clients" or add `http://127.0.0.1:8080/mcp` in the active host's MCP settings.
3. **Registered + server up but tools still absent in this session** → the server probably started after the agent session. Restart the active host/session so MCP tools register at startup, then confirm them through tool/resource discovery. Start Unity MCP first, then the agent host.
4. **Editor closed** → MCP can't work (it drives a live Editor). Either open it, or use the **no-MCP fallback** below.

**No-MCP fallback (fully supported):** when MCP can't connect and you must make progress, drive Unity headlessly via the CLI instead — author C# + an Editor `[MenuItem]`, then `Unity -batchmode -runTests` / `-executeMethod` and grep the logs (see `unity-qa-release` › Headless batchmode verification). Always say which path you used; never claim live-Editor actions that did not happen.

## Readiness check — do this before every batch of commands

Read `mcpforunity://editor/state` and proceed only when:
`ready_for_tools == true`, `is_compiling == false`, `is_domain_reload_pending == false`.

Also read `mcpforunity://project/info` once up front to branch correctly: `renderPipeline` (shader names differ URP vs Built-in), `activeInputHandler` (Input System vs legacy), and the UI stack flags (UI Toolkit vs uGUI/TMP).

## Tool groups — only `core` is enabled by default

Non-core tools do not exist until you enable their group. Enable what the phase needs:

```text
manage_tools(action="enable_group", group="vfx")          # manage_texture, manage_shader, manage_vfx
manage_tools(action="enable_group", group="animation")    # manage_animation
manage_tools(action="enable_group", group="ui")           # manage_ui (UI Toolkit)
manage_tools(action="enable_group", group="testing")      # run_tests, get_test_job
manage_tools(action="enable_group", group="scripting_ext")# manage_scriptable_object, execute_code
manage_tools(action="enable_group", group="docs")         # unity_reflect, unity_docs  (anti-hallucination)
manage_tools(action="enable_group", group="profiling")    # manage_profiler
```

`core` already includes scene, gameobject, component, asset, prefab, material, editor, console, build, packages, camera, physics, graphics, and all script tools. `manage_tools`, `batch_execute`, `set_active_instance`, `manage_script`, `apply_text_edits`, `find_in_file` are always on.

Full parameter reference: load `references/tools-reference.md`. Read-only resources: `references/resources-reference.md`. Upstream task recipes: `references/upstream-workflows.md`. ProBuilder: `references/probuilder-guide.md`. The hard-won reliability rules: **load `references/reliability.md`** before any script/compile/build sequence.

## The golden command patterns

**Create/edit a C# script** (auto-imports + compiles — do NOT also call `refresh_unity`):
```text
create_script(...) | script_apply_edits(op=replace_method|insert_method|anchor_insert|...) | apply_text_edits(precondition_sha256=...)
-> wait: poll editor/state until is_compiling==false
-> read_console(types=["error"])           # only proceed if clean
-> then AddComponent / use the type
```
Use `validate_script` (Roslyn) before compiling and `get_sha` + `precondition_sha256` to avoid clobbering.

**Anti-hallucination for any C#/shader/UI you generate:** call `unity_reflect` (live reflection over Unity/package/project APIs) or `unity_docs` first. Trust order: reflection > project assets > docs > memory. Mandatory on Unity 6.x.

**Bulk scene/object building:** `batch_execute(commands=[...])` — up to 25 per call (100 max). NOT transactional; set `fail_fast=true` for dependent steps.

**See what you built:** `manage_scene(action="screenshot", batch="surround", include_image=true, max_resolution=512)` so the agent can visually iterate.

**Import a generated GLB/FBX** (from unity-3d-generator): write the file directly into `Assets/...` on disk (you have filesystem access), then `refresh_unity(scope="assets", wait_for_ready=true)`. `manage_asset(action="import")` only reimports and **cannot set import settings** — configure scale/rig/materials/compression via `execute_code` driving `ModelImporter`. Instantiate with `manage_gameobject(action="create", prefab_path=...)`.

**Play-mode check:** `manage_editor(action="play")` → `read_console` → screenshot → `manage_editor(action="stop")`. For real tests: `run_tests(mode="PlayMode")` → poll `get_test_job(job_id, wait_timeout=...)`.

**`execute_code` is a C# 6 method body via CodeDom** (the tool's `compiler:"auto"` falls back to CodeDom unless Microsoft.CodeAnalysis/Roslyn is installed). It is **real C#, not the JS sandbox** — `System.DateTime.Now` etc. are fine. But the CodeDom path means: **NO `using` directives, NO local functions, NO C#7+ syntax** (e.g. some tuple forms). Write flat method-body code with **fully-qualified type names** (`UnityEditor.EditorApplication.isCompiling`), build multi-line output with `System.Text.StringBuilder`, and `return` a value to read it back. Pass `compiler:"roslyn"` only if Roslyn is actually installed.

**After any C# edit, gate on a clean compile before using the new type:** `refresh_unity(mode="force", scope="scripts", compile="request", wait_for_ready=true)`, then poll `UnityEditor.EditorApplication.isCompiling` via `execute_code` (or `read_console(types=["error"])`) until clear. Using a freshly-added type before compile finishes silently fails or throws.

**Portrait iPhone screenshot recipe (no MCP param exists for this).** `manage_camera/manage_scene screenshot` captures at the Game view's current size, so for true portrait phone framing of Screen-Space-Overlay UI you must add and select a portrait FixedResolution size yourself, via `execute_code` + reflection:
1. Get the `GameViewSizes` ScriptableSingleton (`UnityEditor.GameViewSizes.instance`) → `GetGroup(currentGroupType)`, then find-or-`AddCustomSize(new GameViewSize(GameViewSizeType.FixedResolution, w, h, baseText))` (all under `UnityEditor`, accessed by reflection — these types are internal).
2. Select it on the `UnityEditor.GameView` window via the private `SizeSelectionCallback(index, null)`, set the internal `selectedSizeIndex`, then `Repaint()`. The window's `targetSize` property is the **authoritative render size** (correctly reads e.g. `(1242,2688)`) — read it back to confirm, don't trust `Screen.width/height`.
3. Capture overlay UI with **`UnityEngine.ScreenCapture.CaptureScreenshot(path)`** (writes at end of frame at the Game View's *target* render size). `manage_camera(action="screenshot")` with **no `camera` arg** also routes to this ScreenCapture path; do NOT pass a `camera` — a camera-render path **excludes Screen-Space-Overlay canvases**, so you capture only the camera background (a blank/incorrect image).
Common portrait sizes: **1242x2688** (iPhone XS Max/11 Pro Max), **1170x2532** (iPhone 12/13/14), **1080x1920**.

**`Screen.width/height` is unreliable inside `execute_code`** — it returns the editor window / last-active-view pixels (e.g. `1739x1036`), NOT the Game View's fixed render target, because the code doesn't run in the Game View's render context. Don't gate layout/capture logic on it. Read the real render size from the GameView `targetSize` property, or the laid-out UI size from the Canvas `RectTransform.rect` (the CanvasScaler lays out to the actual render target). (This supersedes the older "thin-strip `Screen`" note: the issue is the render context, not a strip.)

**Throttled editor → stale Game View captures.** An unfocused / background-throttled Editor doesn't repaint the Game View, so `ScreenCapture.CaptureScreenshot` can write the **last rendered frame** rather than the current state (e.g. a UI panel you just hid still appears). Mitigate by keeping the Editor focused during capture, or force a render right before capturing: `EditorApplication.QueuePlayerLoopUpdate()` + `Canvas.ForceUpdateCanvases()` + the GameView window's `.Repaint()` — or capture on-device. Always **verify the screenshot's content**, not just its pixel dimensions.

**Capturing a transient VFX before the screenshot fires.** A one-shot effect shorter than the MCP round-trip (e.g. a <2.5s confetti burst) is already gone by the time `screenshot` runs. Immediately after spawning it, set `UnityEditor.EditorApplication.isPaused = true` via `execute_code` — coroutine-driven animation freezes at its first-frame layout so the screenshot captures it; restore `isPaused = false` after. The spawned objects must start on-screen or the frozen frame is empty.

**iOS build sequence:** `manage_build(action="platform", target="ios")` → `manage_build(action="settings", property="bundle_id"|"product_name"|"company_name"|"version")` → set `scripting_backend="il2cpp"` (iOS requires it) → `manage_build(action="scenes", ...)` → `manage_build(action="build", target="ios", output_path="Builds/iOS/<name>")` → poll `action="status"`. Output is an **Xcode project folder, not an .ipa** — signing/archive happens outside MCP via `xcodebuild` on macOS.

## Headless iOS build via MCP + on-device diagnostics

The Editor `manage_build(action="build")` flow above works for routine builds, but for a CI-shaped, fully-scripted iOS build — and for diagnosing things that only break **on the device** — drive a static build method and a runtime debug HUD instead. Full walkthrough + copy-paste code: **load `references/ios-build-and-device-diagnostics.md`**. The load-bearing facts:

**Trigger the build through a static method, not the `build` tool.** Author an Editor build entry point (`[MenuItem]` + a parameterless static `PerformiOSBuild()` that calls `UnityEditor.BuildPipeline.BuildPlayer(...)` — see `Assets/<YourGame>/Editor/BuildScript.cs`) and invoke it from `execute_code`:
```text
execute_code(code="YourGame.EditorTools.BuildScript.PerformiOSBuild();")
```
`BuildPipeline.BuildPlayer` blocks the Editor **main thread** for the whole build, so the MCP `execute_code` round-trip **times out / returns no result even when the build succeeds** — the build is still running after the tool gives up. **Do not trust the `execute_code` return value** (success *or* failure). Poll for real completion instead:
- watch the **mtime of the output `Build/iOS/Info.plist`** (the generated Xcode project's plist) — a fresh mtime means the build finished writing, and
- `read_console` for the build-result log line the method emits (e.g. `[BuildScript] iOS build Succeeded -> Build/iOS (...)`).

A non-`Succeeded` build calls `EditorApplication.Exit(1)` in batchmode/CI; in an open Editor it just logs the failure result — so the console line is your source of truth, not the tool result.

**The bridge drops during long compiles, domain reloads, and especially heavy/repeated iOS builds + package resolution.** Any heavy *main-thread* work — a synchronous `BuildPipeline.BuildPlayer`, or an OpenUPM / EDM4U package import/resolve — makes the bridge unresponsive (you'll see "WebSocket is not initialised" / "Unexpected receive error"). The Editor stays alive, but MCP starts returning **`no_unity_session`** ("Unity session not available"). This is *not* the ~5s domain-reload blip — under back-to-back iOS builds and package resolution it recurs constantly. **Recovery: `refresh_unity` often reconnects** (it reports "Refresh recovered after Unity disconnect/retry"); when `refresh_unity` itself times out, **the user must click/focus the Editor window**. When you hit `no_unity_session`, stop retrying blindly — try one `refresh_unity`, and if that doesn't recover, **explicitly tell the user you need them to click the Editor**, then re-check `mcpforunity://editor/state` before resuming.

**A backgrounded Editor won't process a `manifest.json` change.** Editing `Packages/manifest.json` (adding a scoped registry / new package) is NOT resolved until the **Editor is focused** — the package never lands in `Library/PackageCache` and `packages-lock.json` stays unchanged until then. After writing to the manifest, tell the user to focus the Editor, then confirm the package resolved (check `packages-lock.json` / `manage_packages`) before relying on it.

**`execute_code` for build/Editor scripting is C# 6 / CodeDom** (same constraints as elsewhere in this skill): no top-level `using` (use fully-qualified names like `UnityEditor.BuildPipeline`), no JS-isms (`Date.now`, `Math.random`). It is the right tool for one-off Editor scripting — invoking build methods via reflection, reading `UnityEditor.CloudProjectSettings`, toggling `UnityEditor.Advertisements.AdvertisementSettings`, etc.

**On-device diagnostics: a temporary IMGUI debug HUD.** Device-only failures — native iOS plugins, Game Center sign-in, ad SDK lifecycle — have **no Editor console** to read, so MCP can't see them. Surface them on the device screen itself with a **TEMPORARY** `OnGUI`/IMGUI `MonoBehaviour` that renders static diagnostic strings (auth state, display name, last native error, SDK status) over the ScreenSpaceOverlay UI (see `Assets/<YourGame>/Scripts/Game/Net/DebugHud.cs`). Three things that matter:
- **Offset it below the safe area** via `Screen.safeArea` — `top = (Screen.height - Screen.safeArea.yMax) + pad` — or the notch / Dynamic Island clips the top lines (this was a real follow-up fix).
- **Make it tap-to-hide** (toggle on an `EventType.MouseDown` hit-test of the band, `Event.current.Use()`).
- **Plumb native error strings all the way through** to it (e.g. a static `LastIdentityError` the Swift/ObjC++ bridge writes) so the failure is actually visible, not just a bool.
- Gate it to device (`Application.platform == RuntimePlatform.IPhonePlayer`) and **remove it before release.**

## Critical reliability facts (full list in references/reliability.md)

- **Every script compile / package add-remove / scripting-backend change triggers a domain reload** that drops the connection for ~5s and invalidates in-flight calls. Wait and retry; re-fetch SHA after.
- The Editor must be focused enough to process; a modal reload dialog will stall the bridge until clicked (known issue).
- `manage_asset(action="import")` cannot configure importer properties (not implemented) — use `execute_code`/`ModelImporter`.
- `manage_asset(action="search")` can hang Unity on large/whole-project searches — keep `page_size` small (~25), `generate_preview=false`.
- iOS/Android builds have a known bug forcing wrong texture compression — set/verify **ASTC for iOS** yourself via `execute_code`, don't trust defaults.
- Don't disable required Unity modules (physics, animation, uielements, screencapture, imageconversion, unitywebrequest, newtonsoft-json, test-framework) — it breaks compilation.
- Multiple Editors open: use `set_active_instance` to avoid acting on the wrong project.

If MCP is down or the Editor is closed, fall back to authoring C# + an Editor script (`[MenuItem]`) the user runs manually, and say so — never claim scene/prefab work happened without an Editor round-trip.

## Field notes & lessons

- Documented `execute_code` = CodeDom C# 6 method body (no `using`/local-functions/C#7+, fully-qualified names, StringBuilder+return); added post-edit compile gate (refresh_unity force + poll `isCompiling`); added portrait iPhone screenshot recipe via `GameViewSizes` reflection.
- Added "capturing a transient VFX before the screenshot fires" — pause via `EditorApplication.isPaused = true` right after spawn to freeze a sub-round-trip effect for the screenshot, then restore.
- Broadened the `no_unity_session` cause to any heavy main-thread work (sync `BuildPipeline.BuildPlayer` *and* OpenUPM/EDM4U package import/resolve → "WebSocket is not initialised"), and made `refresh_unity` the first recovery step before asking the user to focus the Editor; added "a backgrounded Editor won't resolve a `manifest.json` change until focused" (no `Library/PackageCache` / `packages-lock.json` update until focus). iOS build: noted the export is just fast (~10–20s incremental) Xcode-project generation (heavy native compile is later in Xcode/fastlane), the timed-out return is `success:false, data:null`, and to call `PerformiOSBuild()` synchronously rather than via `EditorApplication.delayCall` (a concurrent domain reload can clear the pending delayCall). Screenshots: prefer `ScreenCapture.CaptureScreenshot` (captures Screen-Space-Overlay at the GameView target size) and never pass a `camera` (camera-render path excludes overlay canvases = blank); pin size via `GameViewSizes.instance.GetGroup` + `AddCustomSize` and read back the authoritative GameView `targetSize`; `Screen.width/height` is unreliable in `execute_code` (returns editor-window pixels, not the render target — read Canvas `RectTransform.rect`/`targetSize` instead, reconciling the old thin-strip note); and a throttled/unfocused Editor writes a stale last-rendered frame — force `QueuePlayerLoopUpdate()` + `Canvas.ForceUpdateCanvases()` + GameView `.Repaint()` and verify content, not just dimensions.
- Added "Headless iOS build via MCP + on-device diagnostics" section + `references/ios-build-and-device-diagnostics.md` — drive the build through a static `PerformiOSBuild()` via `execute_code` (it times out / returns nothing even on success because `BuildPipeline.BuildPlayer` blocks the main thread; poll `Build/iOS/Info.plist` mtime + `read_console` instead); the `no_unity_session` drop under back-to-back builds + package resolution recovers by the user focusing the Editor; and the temporary `OnGUI` debug HUD pattern for device-only failures (Game Center / ads / native plugins), offset below `Screen.safeArea`, tap-to-hide, native errors plumbed through, removed before release.
