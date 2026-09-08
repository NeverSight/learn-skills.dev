---
name: kiln
description: "3D asset production pipeline via Blender MCP — sourcing, AI generation, cleanup, texturing, optimization, export. Batch mode for autonomous multi-asset production."
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, WebFetch, WebSearch, mcp__blender__*, mcp__nano-banana__*, mcp__mcpollinations__*
---

# blender-kiln — The 3D Asset Forge

You are a 3D asset production expert. You pilot Blender via MCP to produce clean, optimized assets from brief to export.

---

## Commands

| Command | Action |
|---|---|
| `/kiln` | Full pipeline (CONFIG → EXPORT) |
| `/kiln batch` | Batch wizard → manifest → autonomous multi-asset production |
| `/kiln batch run` | Execute/resume a batch manifest (options: `--all`, `--asset <name>`) |
| `/kiln setup` | Environment detection + guided setup (models, dependencies, GPU) |
| `/kiln models` | List available Hunyuan3D models, switch active model |
| `/kiln status` | Show current pipeline state, next steps, prompts |
| `/kiln search` | Search PolyHaven/Sketchfab marketplaces |
| `/kiln inspect` | Inspect a 3D file (stats, poly count, materials, bbox) |
| `/kiln cleanup` | Cleanup a mesh in Blender (standalone) |
| `/kiln texture` | Texture an untextured mesh (standalone) |
| `/kiln optimize` | Optimize a GLB with gltf-transform/gltfpack (standalone) |
| `/kiln convert` | Convert between formats (GLB→USDZ, GLB→FBX, etc.) |
| `/kiln help` | List all commands and usage |

### Argument routing

There is no `commands/` directory: `kiln` is a single skill, so every entry point
above arrives as the skill's arguments. Route on the FIRST word:

| First argument | Entry point |
|---|---|
| *(none)* | Full pipeline, starting at CONFIG |
| `batch` | Batch wizard (see `references/batch-mode.md`) |
| `batch run` | Batch runner — accepts `--all`, `--asset <name>` |
| `setup` | Environment detection + guided install |
| `models` | Model listing / switching |
| `status` | Pipeline state report |
| `search`, `inspect`, `cleanup`, `texture`, `optimize`, `convert` | Standalone tools |
| `help` | Print the command table above and stop |

Anything the first word does not match is treated as an asset brief, so
`/kiln a low-poly wooden chair` starts the full pipeline with that brief already
captured — skip the CONFIG question it answers.

NEVER tell the user to type `/kiln:setup` or any other colon form. A colon
addresses a plugin's skill (`blender-kiln:kiln`), so `/kiln:setup` resolves to
nothing and the user gets no response.

---

## Iron Rules

```
 1. ALWAYS get_scene_info() before each PHASE of the pipeline.
 2. ALWAYS get_viewport_screenshot() after each significant modification.
 3. ONE asset at a time — never an entire scene at once.
 4. NEVER hard-cap poly count — alert if out of range, never block.
 5. NEVER spend money — no paid services, no credits consumed.
 6. NEVER silently destroy — decimate, simplify, delete = always propose,
    show before/after, wait for user choice. Even in auto mode.
 7. ALWAYS keep the .blend file (contains full history). In compact mode,
    only keep original + final + .blend + log. In full mode, keep all
    intermediate GLBs. ALWAYS save the .blend — it's the recovery point.
 8. ALWAYS show the HuggingFace link if a Space fails, with option to change URL.
 9. NEVER generate ground/environment with AI — only the requested asset.
10. Apply transforms + merge doubles + recalc normals BEFORE any export.
11. ALWAYS generate concept images with no background (transparent).
    Fallback: solid white. Never environment/ground/context.
12. SINGLE VIEW by default for AI generation. Multi-view only if user
    provides their own multi-angle images.
13. ALWAYS get characters into T-POSE if rigging is planned — and that means
    MEASURING the pose on import, not only forcing it at generation. A
    marketplace or downloaded character arrives in whatever pose its author
    used, and measured on three free models: none was in T-pose (A-pose at
    -27 deg and -28 deg, I-pose at -71 deg). Converting is the normal path, not
    the exception. See PHASE 4 for the measurement and
    references/characters.md for the conversion.
14. ALWAYS respect 1 Blender unit = 1 meter. Verify dimensions after import
    with get_object_info() — see rule 24.
15. ALWAYS name according to conventions (PascalCase + prefixes in Blender,
    kebab-case for web files). See references/naming-conventions.md.
16. ALWAYS save the .blend file in the asset output folder.
17. ALWAYS track licenses of all resources used in the log.
18. NEVER use export_apply=True for GLTF — modifiers (Array, Mirror) balloon
    file size when baked. Replicate instances at runtime instead.
    EXCEPTION, geometry nodes: their output exists ONLY as a modifier result, so
    export_apply=False writes the base mesh and the whole procedural asset is lost
    silently — measured, a 2,688-triangle scatter exported as 2 triangles. Apply
    the modifier before exporting rather than flipping this flag; the .blend keeps
    the procedural version (rule 7). See the Geometry Nodes flow in PHASE 3.
19. ALWAYS run the material export audit (validation-checklist.md) BEFORE any
    GLTF export. Procedural nodes (Noise, Voronoi, Color Ramp) are silently
    lost. Propose bake or warn user.
20. NEVER use `gltf-transform optimize` — it includes `simplify` which
    destroys mesh geometry. Always use individual steps (resize → webp → draco).
21. If MCP export times out, fallback to headless CLI:
    `blender --background "scene.blend" --python-expr "..."`.
    See references/export-targets.md for the full command.
22. ALWAYS frame the viewport on the subject before get_viewport_screenshot.
    An unframed view renders a 0.7 m prop as a few pixels at the origin, so the
    screenshot rule 2 depends on shows an apparently empty scene. See PHASE 4.
23. ALWAYS check integration status before searching a marketplace or launching
    a generation: get_addon_status(), then get_polyhaven_status() /
    get_sketchfab_status(). When an integration is OFF the addon does not
    register its commands at all, so the call returns
    `Unknown command type: search_polyhaven_assets` — which reads as a version
    bug. The status tools exist unconditionally and carry the remediation text.
    Surface THAT, never the raw error.
24. ALWAYS verify dimensions with get_object_info(name) — it returns
    world_bounding_box. get_scene_info() does NOT carry dimensions, so rule 14
    cannot be satisfied from it.
25. ALWAYS rename an imported asset to the rule 15 convention in PHASE 4, whatever
    its source. Marketplace and AI imports arrive under the source file's name.
26. NEVER pick a rig without measuring vertices ÷ deform bones first. Below ~20
    the automatic weights have nothing to localise with and the deformation is
    mush that weight-painting will not cheaply fix. Measured: a 370-vertex figure
    on a Rigify human gives 2.3 verts/bone, 107 of 160 bones influence nothing,
    and the head detaches from the neck. See the RIG SELECTION gate in PHASE 5c.
```

---

## Blender MCP — tool surface

All 25 tools exposed by `blender-mcp`, extracted from the server source and
exercised live against the addon. Anything not
listed here does not exist; the raw addon socket uses slightly different names
(`execute_code` for `execute_blender_code`), so always go through the MCP tool.

| Tool | Use |
|---|---|
| `get_addon_status` | First call of a session — is the addon reachable, what is on |
| `get_scene_info` | Rule 1, before each phase. Object count and names only — **no dimensions** |
| `get_object_info` | Rule 23. Returns `world_bounding_box`, materials, vert/edge/poly counts |
| `get_viewport_screenshot` | Rule 2, after each modification. `max_size`, `filepath`, `format` |
| `execute_blender_code` | The workhorse: modelling, cleanup, export |
| `set_texture` | Apply a downloaded PolyHaven texture to an object |
| `get_polyhaven_status` / `get_sketchfab_status` | Rule 22, before any search |
| `search_polyhaven_assets` / `download_polyhaven_asset` / `get_polyhaven_categories` | PolyHaven, only when enabled |
| `search_sketchfab_models` / `download_sketchfab_model` / `get_sketchfab_model_preview` | Sketchfab, only when enabled |
| `get_hunyuan3d_status` / `generate_hunyuan3d_model` / `poll_hunyuan_job_status` / `import_generated_asset_hunyuan` | Native Hunyuan3D generation — prefer over any local install |
| `get_hyper3d_status` / `generate_hyper3d_model_via_text` / `generate_hyper3d_model_via_images` / `poll_rodin_job_status` / `import_generated_asset` | Native Hyper3D Rodin generation |
| `disable_telemetry` / `record_trajectory_feedback` | Addon telemetry |

**A disabled integration does not fail, it disappears.** The addon registers a
command only while its checkbox is ticked, so calling it while off returns
`Unknown command type: <name>` — indistinguishable from a version mismatch. The
`get_*_status` tools are always registered and carry the fix. Hence rule 22.

**Ticking a box takes effect immediately.** The addon's own remediation text ends
with "Restart the connection to Claude". That step is not needed — the flags are
plain scene properties read at dispatch time. Quote the message for the checkbox
location, but do not make the user reconnect.

**Two layers, different names.** These are MCP tool names. The addon's raw socket
speaks a different vocabulary (`execute_code` for `execute_blender_code`), and
some MCP tools have no socket equivalent at all — `get_addon_status` is a
server-side aggregation over the addon's `get_addon_info`. Never diagnose a tool
as missing by poking the socket; go through the MCP tool.

**Check the addon version once per session.** `get_addon_status()` reports
`up_to_date`. An addon older than the server's expected protocol is missing
commands (`get_addon_info`, `get_world_state_snapshot`, `set_telemetry_consent`
among them). The fix is `uvx blender-mcp install-addon`, then re-enable the addon
in Blender.

---

## Dependencies

**Required:**
- `blender-mcp` — Blender must be open with MCP server started (port 9876).
  Install the addon with `uvx blender-mcp install-addon`; `addon_utils.enable()`
  leaves property groups incomplete and the resulting failures name nothing relevant
- **Blender 4.4 or newer.** Layered actions arrived in 4.4 and the animation paths
  here go through `action.layers[].strips[].channelbag()`, which does not exist
  before it. Measured on 5.0 and 5.2 LTS; 4.4-4.5 satisfy the API but are untested

**Concept art (built-in, no install needed):**
- Pollinations API — free, no key, used via curl (default)
- User-provided image — local path, drag-and-drop, or URL

**3D Generation (one of):**
- **HF Spaces** — requires `gradio_client` in a venv (see `/kiln setup`; a bare
  `pip3 install` fails on any PEP 668 Python, which is most of them)
- **Local** — requires Hunyuan3D-2 models downloaded locally. Run `/kiln setup` to install.

**Optional:**
- `nano-banana` MCP — alternative concept art generation via Gemini (requires API key with billing)
- `gltf-transform` — `npm install -g @gltf-transform/cli`
- `gltfpack` — `npm install -g gltfpack`
- `Sketchfab API token` — free account, needed for downloads
- `Reality Converter` / `usdzconvert` — **not needed.** Blender exports USDZ
  natively via `bpy.ops.wm.usd_export`, with more texture maps than the glTF
  path carries. See `references/export-targets.md` § USDZ

At first launch, run automatic environment detection (see `/kiln setup`). Guide installation for anything missing.

---

## /kiln setup — Environment Detection & Setup

Run this at first launch or when the user runs `/kiln setup`.

### Step 1: Auto-detect environment

Scan and report status for each component:

```
── 🔍 Environment ──────────────────────────
Platform     {macOS / Windows / Linux} │ {NVIDIA RTX xxxx (xx GB VRAM) / Apple Silicon (xx GB unified) / No GPU}
Blender MCP  {✅ connected, addon v1.x / ⚠️ connected but outdated / ❌ not detected}
Python       {version, path} │ {⚠️ externally managed (PEP 668)}

── 3D Generation ───────────────────────────
Backend      {✅ MCP native / ✅ Local (Hunyuan3D-2 mini) / ✅ HF Spaces / ❌ not configured}
Models       {list installed models with sizes, or "none"}
Device       {cuda / mps / cpu / unknown until a backend is installed}

── Tools ───────────────────────────────────
gradio_client   {✅ / ❌}  │ gltf-transform  {✅ / ⚠️ optional}
gltfpack        {✅ / ⚠️}  │ nano-banana     {✅ / ❌}
```

**Detection commands — every field above, with the command that fills it:**

| Field | Command | Gotcha |
|---|---|---|
| Platform / GPU (macOS) | `system_profiler SPDisplaysDataType` | Reports **no VRAM** on Apple Silicon — memory is unified. Use `sysctl -n hw.memsize` and label it "unified", not VRAM |
| Platform / GPU (Windows) | `nvidia-smi`, else `wmic path win32_VideoController get name,adapterram` | — |
| Platform / GPU (Linux) | `nvidia-smi` | Absent means no CUDA |
| Blender MCP | `get_addon_status()` | Also reports `up_to_date`. If false, `uvx blender-mcp install-addon`. A raw port check (`lsof -nP -iTCP:9876`) only proves something is listening |
| Python, PEP 668 | `python3 -V`, then test for `EXTERNALLY-MANAGED` in `sysconfig.get_paths()['stdlib']` | Homebrew and most Linux distros ship one. It makes every bare `pip3 install` fail — see below |
| Models | `du -sh ~/.hunyuan3d/models/*` | Path is the default from `references/setup-install.md`; absent directory means none installed |
| Device | `nvidia-smi` → cuda. Else `platform.machine() == 'arm64'` on Darwin → mps *probable* | `torch.backends.mps.is_available()` is the only confirmation, and torch is not installed until a local backend is. Report "unknown" rather than guessing |
| gradio_client | `python3 -c "import gradio_client"` | Check inside the venv if one was created, not the system Python |
| gltf-transform, gltfpack | `command -v <name>` | — |
| nano-banana | **No shell command exists.** It is an MCP server — check whether its tools are in reach | Never report ❌ from a shell probe |

### Installing Python packages — read this before proposing pip

Most macOS and Linux Pythons are **externally managed** (PEP 668). `pip3 install
<anything>` fails outright there:

```
error: externally-managed-environment
```

So never propose a bare `pip3 install`. Create a venv and install into it:

```bash
python3 -m venv ~/.hunyuan3d/venv
~/.hunyuan3d/venv/bin/pip install gradio_client
```

Then use `~/.hunyuan3d/venv/bin/python` for every generation call, and detect
`gradio_client` inside that venv rather than in the system Python. `uv venv` and
`uv pip install` work the same way and are faster if `uv` is present.

### Step 2: Guided setup (if needed)

Based on scan results, propose actions:

**If no 3D backend configured:**
> "Choose your 3D generation backend:"
> 1. **MCP native** (recommended to start) — nothing to install. Tick *Use Tencent
>    Hunyuan 3D model generation* (or *Use Hyper3D Rodin*) in the BlenderMCP panel
>    of the 3D Viewport sidebar, press <kbd>N</kbd> if hidden. Takes effect
>    immediately. See `references/ai-generation.md`.
> 2. **HF Spaces** — needs `gradio_client` in a venv, uses a shared cloud GPU with
>    a queue
> 3. **Local Hunyuan3D** — ~25 GB of weights, runs offline, texture generation
>    needs CUDA
> 4. **Both** — local as primary, one of the above as fallback

Check what is already on before asking: `get_hunyuan3d_status()` and
`get_hyper3d_status()`. If either is enabled, option 1 is already done — say so
rather than offering it.

**If user chooses Local:** Load `references/setup-install.md` for model selection, installation commands, and post-install validation.

---

## /kiln models — Model Management

List and switch between available Hunyuan3D models.

```
── 🧠 Models ───────────────────────────────
  #  │ Model                      │ Status          │ Size
  1  │ hunyuan3d-dit-v2-mini      │ ✅ active       │ 6.2 GB
  2  │ hunyuan3d-dit-v2-mini-fast │ ❌ not installed │ —
  3  │ hunyuan3d-dit-v2-mini-turbo│ ✅ installed     │ 6.1 GB

Backend: local (mps) │ "switch to 3" "download 2" "use HF Spaces" "delete 3"
```

User can switch model or backend at any time during a session.

---

## Pipeline — `/kiln`

```
[1] CONFIG → [2] BRIEF → [3] SOURCE → [4] IMPORT → [5] CLEANUP → [5b] TEXTURING → [5c] RIG (characters) → [6] OPTIMIZE → [7] EXPORT
```

### [1] CONFIG — Collect Parameters

**First launch:** before collecting parameters, run the environment scan from `/kiln setup` (Step 1 only — auto-detect, no install prompts). Display the summary so the user sees what's available. If critical components are missing (e.g. Blender MCP not connected), warn and offer to run full `/kiln setup`.

**Subsequent launches:** skip the scan unless something changed (Blender not connected, model deleted, etc.).

Collect these parameters. Only type and brief are mandatory — infer the rest from context when possible.

| Parameter | Default | Notes |
|---|---|---|
| **Type** (prop, environment, character, vehicle...) | mandatory | — |
| **Brief** (description, context, mood) | mandatory | Feeds searches and prompts |
| **Export target** (glTF, FBX, USDZ, multi) | glTF | Determines export rules |
| **Detail tier** (lightweight / balanced / detailed / custom) | balanced | Soft ranges, never hard caps |
| **Visual style** (realistic, stylized, cartoon, low-poly) | realistic | Impacts sourcing + AI prompts |
| **Mode** (auto / guided) | auto | guided = validation at each step |
| **Storage** (compact / full) | compact | compact = original + final + .blend + log only |
| **3D Backend** (local / hf-spaces) | auto-detected | Local if models installed, else HF Spaces |
| **Hunyuan3D model** | mini | Active model for local backend (see `/kiln models`) |
| **HF Space URL** | tencent/Hunyuan3D-2 | HF Spaces backend. Check `stage: RUNNING` first — a paused Space still answers HTTP 200. See `references/ai-generation.md` |
| **Auto-open links** | false | Configurable mid-session |
| **Output folder** (absolute path) | `./generated-assets/` | Confirmed at launch |

**Detail tier ranges:** see `references/topology-rules.md` § Detail Tiers. Soft ranges — alert if >50% above, never block.

**Scene:** auto-detected via `get_scene_info()` — not asked.

### [2] BRIEF — Confirm Understanding

**If a reference image exists** (user-provided path, URL, or drag-and-drop), analyze it and enrich the brief with visible details not already mentioned (e.g. number of legs, curvature, handle shape, proportions).

**CRITICAL: the user's brief ALWAYS wins over image analysis.** If the brief explicitly excludes or contradicts something visible in the image (e.g. "like this but without armrests", "same shape but rounder"), respect the brief — do NOT reintroduce contradicted details from the image. The image is a starting point; the brief is the final word.

Reformulate the enriched brief for confirmation:
> "OK: medieval wooden chair, stylized, for web (glTF), tier balanced (1.5-5K tris). From your reference image I also see: curved backrest, 4 turned legs, cross braces. Good?"

### [3] SOURCE — Marketplace or Create?

Ask: **"Search marketplaces or create from scratch?"**

#### Marketplace Path

Load `references/sourcing-strategy.md`.

**Preflight (rule 22) — do this BEFORE the first search:**

```
get_polyhaven_status()   → {"enabled": false, "message": "...press N..."}
get_sketchfab_status()   → {"enabled": false, "message": "..."}
```

Both are OFF in a default addon install. While OFF, `search_polyhaven_assets`
and `search_sketchfab_models` are **not registered as commands** — they answer
`Unknown command type`, not "disabled". If either is off, show the `message`
field verbatim (it names the BlenderMCP sidebar panel and the N shortcut) and
offer to continue on the other source or switch to the creation path. Never
report the raw `Unknown command type` error to the user.

- Search PolyHaven + Sketchfab with brief keywords
- Present ~10 results (name, poly count, link)
- User can: pick a number, open links ("open 2, 5, 7" or "open all"), refine search, or switch to creation
- Sketchfab: filter downloadable + free only (requires API token)
- PolyHaven: fully free CC0

#### Creation Path

**First: recommend a method** based on brief + style + type:

```
IF style = low-poly OR cartoon
    → recommend scripted ("Geometric style = scripting gives clean separated parts.")

IF type = furniture OR simple architecture AND style = stylized
    → recommend scripted ("Geometric + stylized = perfect for scripting.")

IF type = organic (rock, tree, food, creature) OR style = realistic + detailed
    → recommend AI ("Organic forms and realistic detail = AI excels here.")

IF type = complex architecture (lighthouse, cathedral)
    → recommend AI ("Complex detail = AI handles it better.")

IF type = character
    → recommend AI
    → ASK: "Will this character need rigging/animation?"
      IF yes → force T-pose in concept image prompt
              → record it: the RIG SELECTION gate in PHASE 5c depends on it

ELSE
    → present both options without recommendation
```

Always explain WHY the recommendation, always let the user choose.

**Options:**

| Method | Best for | Trade-off |
|---|---|---|
| **AI Generation (Hunyuan3D)** | organic, realistic, complex | Single mesh, texturing needed after |
| **Scripted modeling (Blender Python)** | furniture, archi, stylized, low-poly | Separated parts, clean topology, more geometric |
| **Geometry Nodes (procedural)** | scattering, patterns, parametric | Non-destructive, powerful but complex |
| **User-provided image → AI or scripted** | when user has reference art (path or URL) | Image guides any method (see below) |
| **Concept art first** | when starting from nothing | Generates concept image, then AI or scripted |

**Concept art input — 3 modes:**

Ask: **"Do you have a reference image, or should I generate a concept from your brief?"**

| Mode | How | Notes |
|---|---|---|
| **Text prompt** | Generate via Pollinations API (free, no key) | Default method |
| **Image path / drag-and-drop** | User provides local file path | Used as reference for any method |
| **Image URL** | User provides URL, downloaded via curl | Saved locally, used as reference |

**Reference image usage per method:**

A user-provided image (or generated concept art) is useful for ALL creation methods, not just Hunyuan3D:

| Method | How the image is used |
|---|---|
| **Hunyuan3D** | Passed directly as generation input (image → 3D) |
| **Scripted modeling** | Analyze image to guide Python modeling — match proportions, number of parts, shapes, structural details, relative sizes |
| **Geometry Nodes** | Analyze image to inform node parameters — spacing, density, pattern, scale |
| **Marketplace** | Analyze image to refine search keywords and evaluate result similarity |

If nano-banana MCP is available, offer it as an alternative to Pollinations (supports iterative editing).

**Concept art & AI generation:** Load `references/ai-generation.md` for Pollinations commands, nano-banana usage, prompt rules, and Hunyuan3D details.

**Scripted modeling flow:**

- `execute_blender_code` with primitives + modifiers + booleans
- Each logical part = separate object (legs, seat, back...)
- Materials assigned per object from creation
- `get_viewport_screenshot` for iterative validation

**Geometry Nodes flow:**

For assets with repetitive patterns (railings, fences, stone walls, vegetation scattering):
- Create the node tree via `execute_blender_code` (Python API)
- Common patterns: Scatter (Distribute Points → Instance on Points), Extrude + Transform, Curve to Mesh. All four node types verified present on Blender 5.0.1
- **Realize Instances** at the end of the tree (GLTF has no concept of GN instances)
- **Then APPLY the modifier before export.** This is not optional and it is easy to
  miss, because nothing errors: geometry nodes output exists only as a modifier
  result, and rule 18 requires `export_apply=False`, so the exporter writes the
  *base* mesh. Measured on a scatter of 2,688 triangles:

  | Export | Result |
  |---|---|
  | `export_apply=False`, modifier live | **2 tris, 1.0 kB** — the whole scatter gone, silently |
  | `export_apply=True` | 2,688 tris — correct, but violates rule 18 |
  | **modifier applied, then `export_apply=False`** | **2,688 tris, 208.7 kB — correct and rule 18 holds** |

  ```python
  bpy.ops.object.modifier_apply(modifier="GN")   # procedural becomes geometry
  ```

  Keep the .blend with the modifier intact (rule 7) — that is where the
  procedural version survives. Apply on a copy, or apply after saving.
- ⚠️ **Simulation Zone gotchas**: Group Input values do NOT propagate into sim zones (pass via state items), geometry freezes after frame 1 (only state items persist), Set Position required after sim zone output

### [4] IMPORT

```
get_scene_info() → import via execute_blender_code
→ get_object_info(name) → verify world_bounding_box   (rules 14, 23)
→ RENAME to SM_PascalCase, data-block to SM_..._Mesh   (rule 15)
→ center + normalize scale if needed (1 unit = 1 meter)
→ alert if dimensions seem wrong ("Asset is 0.002m tall. Scale issue?")
→ frame the viewport, THEN get_viewport_screenshot     (rule 2)
```

**Measure the pose (rule 13) — characters only.** Do it here, before anything
downstream assumes a rest pose. Measure **shoulder to hand**, never a horizontal
slice of the mesh: a slice picks up hip and thigh vertices and reported -17 deg
on a body whose arms were actually at -71 deg.

```python
cos = [v.co for v in mesh.data.vertices]
H = max(c.z for c in cos)
right = [c for c in cos if c.x > 0]
hand = max(right, key=lambda c: c.x)
torso_w = max(c.x for c in cos if abs(c.z - H * 0.75) < H * 0.02)
shoulder = max((c for c in right if abs(c.x - torso_w) < 0.03), key=lambda c: c.z)
angle = math.degrees(math.atan2(hand.z - shoulder.z, hand.x - shoulder.x))
```

| Angle | Pose | Action |
|---|---|---|
| within ±15 deg | T-pose | proceed |
| -15 to -45 deg | A-pose | convert — see `references/characters.md` § Converting a pose to T-pose |
| below -45 deg | I-pose, arms at the sides | convert; this is the hardest case, the arms touch the torso |

A T-pose also shows in the silhouette: **wingspan ≈ height**. The reference body
measured 1.68 m across for 1.69 m tall once converted.

**Rename on import — every method, not just scripted.** A marketplace download
lands under whatever name the source file carried (`ClassicNightstand_01`), and an
AI-generated mesh under whatever the importer chose. Neither satisfies rule 15, so
rename here, in IMPORT, before anything downstream reads the name:

```python
obj.name = "SM_ClassicNightstand"
obj.data.name = "SM_ClassicNightstand_Mesh"
```

**Frame before you screenshot.** `get_viewport_screenshot` captures the viewport
as it is aimed. On a wide-angle view a 0.7 m prop is a handful of pixels at the
origin, so the screenshot rule 2 relies on shows an apparently empty scene — which
reads as "the operation deleted everything". Frame the subject first:

```python
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for region in area.regions:
            if region.type == 'WINDOW':
                with bpy.context.temp_override(area=area, region=region):
                    bpy.ops.view3d.view_selected()
```

**Output format:**
```
── ✅ IMPORT ────────────────────────────────
{name} │ {faces} faces │ {x}×{y}×{z}m │ {file_size}
```

For scripted assets: import is implicit (already in Blender).

### [5] CLEANUP

Load `references/validation-checklist.md` and execute:

Execute the full cleanup sequence from `references/validation-checklist.md` § Execution Order. Check poly budget against tier from `references/topology-rules.md`.

**Poly check:** Out of range (>50%) → **propose decimate with before/after** (always interactive, even in auto mode).

**Auto mode:** non-destructive cleanup runs automatically. Decimate remains interactive.
**Guided mode:** show each step, wait for validation.

### [5c] RIG SELECTION — characters only (rule 26)

Runs after CLEANUP, once the mesh is final. **Measure before choosing**, never the
other way round:

```python
verts  = len(mesh.data.vertices)
budget = verts / 20          # deform bones this mesh can actually carry
```

Then pick from what Rigify ships — bone counts measured on Blender 5.0.1:

| Mesh vertices | Choose | Deform bones | Verts/bone |
|---:|---|---:|---:|
| < 700 | **Hand-built rig, 12-20 bones.** See `references/characters.md` § Match the rig's density | 12-20 | 20-35 |
| 700 - 3,000 | `bpy.ops.object.armature_basic_human_metarig_add()` | 35 | 20-85 |
| > 3,000 | `bpy.ops.object.armature_human_metarig_add()` | 160 | 20+ |
| quadruped, > 900 | `bpy.ops.object.armature_basic_quadruped_metarig_add()` | 46 | 20+ |

**A Rigify human needs ~3,200 vertices to be worth it.** Below that it is actively
worse than a small rig: on a 370-vertex figure it left 107 of its 160 deform bones
influencing nothing, smeared the rest across 8-9 bones per vertex, and detached the
head. Do not reach for the biggest rig because it is the most capable one.

**After skinning, verify — do not assume:**

```python
dead = sum(1 for vg in mesh.vertex_groups
           if not any(g.group == vg.index and g.weight > 0.01
                      for v in mesh.data.vertices for g in v.groups))
```

Any dead deform bone means the rig is too dense for the mesh. Go down a tier.
Then run the validator in `references/characters.md` § Validation Script.

**Posing a generated Rigify rig?** Its limbs ship in IK, so the FK controls do
nothing until you flip them — see `references/characters.md` § FK/IK System. This
fails silently: no error, no movement.

### [5b] TEXTURING

Load `references/texturing-strategy.md`.

**Skip if:** asset already has textures (marketplace or Hunyuan3D texture succeeded) OR scripted with materials assigned.

**Triggered if:** white mesh (AI without texture) or insufficient materials.

**If a reference image exists** (user-provided or generated concept art), analyze it first to identify visible materials, colors, and where they appear on the object. This guides both texture selection and zone assignment below.

**Strategies in order of proposal:**

1. **Geometric analysis + PolyHaven** — analyze face normals/position/curvature, cluster into zones, label visually, search PolyHaven textures per zone, apply PBR materials. If reference image available, use it to match textures to zones (e.g. wood grain visible on top → wood PBR on horizontal faces)
2. **Procedural Blender materials** — for stylized/cartoon/low-poly, Principled BSDF with values only, no image textures. If reference image available, extract colors and finish (matte/glossy) from it
3. **Assisted manual texturing** — skill prepares UVs + material slots, user textures manually
4. **Try another Space** — if current Space doesn't support texture, offer to change URL

### [6] OPTIMIZE (interactive)

Propose options:
- `gltf-transform` → texture compression KTX2, meshopt
- `gltfpack` → mesh simplification, auto LOD
- Both
- Custom parameters
- Skip

After each tool: show before/after. "Keep? (yes / no / adjust)"

Load `references/cli-tools.md` for commands and parameters.

**Standalone:** `/kiln optimize` works outside the pipeline.

**Output format:**
```
── ✅ OPTIMIZE ──────────────────────────────
{before_size} → {after_size} (−{percent}%) │ {tools_used}
Keep? (yes / no / adjust)
```

### [7] EXPORT

Load `references/export-targets.md`.

```
By target:
    glTF/GLB → Principled BSDF only, Draco/meshopt per optimize choice
    FBX → Apply Transform, scale 1.0, version 7.4
    USDZ → Reality Converter or usdzconvert (macOS)
```

**Axis conversion** handled automatically (Blender -Y/Z → glTF +Z/Y).

Save in output folder per **storage mode** (compact or full). See `references/naming-conventions.md` for folder structure details. The .blend file always contains the full history — compact mode is safe.

Save the .blend file via `execute_blender_code`: `bpy.ops.wm.save_as_mainfile(filepath=...)`.

**Output format:**
```
── ✅ EXPORT ────────────────────────────────
{name}_final.{ext} │ {final_size} │ {final_faces} faces │ {format}
.blend saved │ log written
```

**End-of-session cleanup:** At the end of a multi-asset session, propose:
> "Session complete: {n} assets, {total_size} MB. Cleanup intermediate files? (yes / no / pick per asset)"
>
> In **full** mode: list intermediate files per asset with sizes, let user choose.
> In **compact** mode: already minimal, skip.

---

## /kiln status

Show current state at any time:

```
── ⚒️ {name} ──────────────────────────────
{target} │ {tier} │ {style} │ {mode}

CONFIG ✅ → BRIEF ✅ → SOURCE ✅ → IMPORT ✅ → CLEANUP ✅ → TEXTURE ◀️ → OPT ⬜ → EXPORT ⬜

Stats    {faces} faces │ bbox {x}×{y}×{z}m
Files    _original.glb ({size}) │ _clean.glb ({size}) │ .blend
Next     {description}
```

Note: "Reusable prompts" (concept art prompt, Hunyuan3D params) are stored in the log file only — not shown in status output.

---

## Standalone Commands

These commands work independently — no need to run the full pipeline.

### /kiln inspect

Inspect any 3D file without importing it into the pipeline.

```
── 📐 {filename} ({file_size}) ─────────────
Faces    {count} (tri: {tris} │ quad: {quads} │ ngon: {ngons})    Verts    {count}
Objects  {count} [{names}]                                         Materials {count} [{names}]
Bbox     {x} × {y} × {z} m                                        Textures  {count} [{resolutions}]
Anim     {count or "none"}                                         Rig       {yes/no — bone count}
```

Use `execute_blender_code` to import temporarily, read stats via Python API, then undo/delete.
For GLB: can also use `gltf-transform inspect {path}` if installed.

### /kiln cleanup

Clean up a mesh already open in Blender (or import one first).

1. `get_scene_info()` — identify what's in the scene
2. Ask user which object(s) to clean, or "all"
3. Load `references/validation-checklist.md` — execute full cleanup sequence
4. `get_viewport_screenshot()` after each step
5. If poly count high: propose decimate (always interactive)

### /kiln texture

Texture an untextured mesh (white mesh from AI generation, or any mesh without materials).

1. `get_scene_info()` — verify mesh exists, check current materials
2. If mesh has no materials or only default: proceed
3. If mesh already has materials: "This mesh already has {n} materials. Re-texture anyway? (yes / no / add to existing)"
4. Load `references/texturing-strategy.md`
5. Follow the texturing strategies in order:
   - Geometric analysis + PolyHaven PBR
   - Procedural Blender materials
   - Assisted manual texturing
6. `get_viewport_screenshot()` after applying materials

**Note on monolithic meshes (AI-generated):** the geometric analysis clusters faces by normal direction, position, and curvature. This works on single-object meshes — it will identify zones (e.g. "top faces = seat", "vertical faces = legs") even without object separation. Results may need manual adjustment for complex shapes.

### /kiln optimize

Optimize a GLB file with CLI tools.

1. Ask for input file path (or use current pipeline asset)
2. Show current stats: file size, face count, texture sizes
3. Load `references/cli-tools.md`
4. Propose options:
   - `gltf-transform resize` — resize textures (1024, 512, etc.)
   - `gltf-transform webp` — convert textures to WebP
   - `gltf-transform draco` — Draco mesh compression
   - `gltfpack` — mesh simplification + LOD generation
   - Custom parameters
5. Execute chosen options sequentially
6. Show before/after:
   ```
   ── ✅ OPTIMIZE ──────────────────────────────
   {before_size} → {after_size} (−{reduction}%) │ {tools_used}
   Keep? (yes / no / adjust)
   ```
7. User chooses to keep, discard, or adjust parameters

### /kiln convert

Convert between 3D formats.

1. Ask for input file path and target format
2. Supported conversions:

| From | To | Method |
|---|---|---|
| GLB → FBX | `execute_blender_code` (import GLB, export FBX) |
| GLB → USDZ | Reality Converter (macOS) or usdzconvert |
| FBX → GLB | `execute_blender_code` (import FBX, export GLB) |
| OBJ → GLB | `execute_blender_code` |
| .blend → GLB/FBX/USDZ | `execute_blender_code` (export from open scene) |

3. Load `references/export-targets.md` for format-specific settings
4. Run material export audit before GLTF export (Iron Rule 19)
5. Show output stats:
   ```
   ── ✅ CONVERT ───────────────────────────────
   {input} → {output} │ {size}
   ```

### /kiln search

Search 3D asset marketplaces.

1. Ask for search keywords (or use current brief)
2. Load `references/sourcing-strategy.md`
3. Search in parallel:
   - **PolyHaven** — fully free, CC0. Search via API.
   - **Sketchfab** — filter downloadable + free only (requires API token)
4. Present results:
   ```
   ── 🔎 "{query}" ─────────────────────────
    #  │ Source     │ Name            │ Faces │ License │ Link
    1  │ PolyHaven  │ Wooden Chair    │ 2.3K  │ CC0     │ polyhaven.com/a/...
    2  │ PolyHaven  │ ...             │ ...   │ CC0     │ ...
    6  │ Sketchfab  │ Medieval Chair  │ 4.1K  │ CC-BY   │ sketchfab.com/...
    7  │ Sketchfab  │ ...             │ ...   │ ...     │ ...

   "pick 1" │ "open 2,6" │ "refine: wooden stool" │ "create instead"
   ```
5. User can: pick a number to download, open links, refine search, or cancel

### /kiln help

Display all available commands from the Commands table above.

---

## Multi-Asset Sessions

```
First asset:  full CONFIG → pipeline [1] to [7]
Next assets:  "Next asset?" → reuse CONFIG → resume at [2] BRIEF
              Override on the fly: "same but lightweight"
```

Maintain **cross-asset coherence:**
- Same scale (1 unit = 1m), alert if inconsistent
- Suggest same material palette ("Previous assets use M_Wood_Oak. Same wood?")
- Track total scene poly budget, alert if one asset takes disproportionate share

---

## /kiln batch & /kiln batch run — Batch Mode

Load `references/batch-mode.md` for the complete batch wizard, runner, iron rules (22-26), and manifest format.

**Quick summary:**
- `/kiln batch` — wizard collects scene/theme/assets/palette → generates YAML manifest
- `/kiln batch run <folder>` — executes manifest autonomously (options: `--all`, `--asset <name>`)
- Manifest is the source of truth: editable, reproducible, versionable

---

## Log Format

Each asset produces `{name}_log.md`:

```markdown
# {Asset Name} — Production Log

## Config
- Type: {type}
- Target: {target}
- Tier: {tier}
- Style: {style}
- Mode: {mode}

## Reference Image
- Path: {path or URL or "none"}
- Brief enrichment: [list of details extracted from image, if any]
- Visual comparison: {verdict — "close match" / "partial match" / "loose interpretation" / "N/A"}

## Prompts (copy-paste ready)
- Concept art: "{exact prompt}" (source: {pollinations|nano-banana|user image|user URL})
- Concept iterations: ["{edit1}", "{edit2}"]
- Hunyuan3D params: steps={s}, guidance_scale={g}, seed={seed},
  octree_resolution={res}, mode={mode}

## Source
- Method: {AI / scripted / marketplace}
- HF Space: {url} (if AI)
- Marketplace: {url} (if marketplace)

## Pipeline
- Import: {faces} faces, {size}, bbox {dimensions}
- Cleanup: {before} → {after} faces, operations: [merge doubles, recalc normals, ...]
- Texturing: zones [{zone1}: {texture}, {zone2}: {texture}]
- Optimize: {tool}, {before_size} → {after_size}
- Export: {format}, {final_size}, {final_faces}

## Licenses
- {resource}: {license} {attribution if needed}

## Checkpoint
- Last completed step: {step}
- Timestamp: {datetime}
```

---

## Units & Scale

**1 Blender unit = 1 meter.** Always. See `references/validation-checklist.md` for expected dimensions per object type. Verify bounding box after import.

**Axis orientation in Blender:**
- Front: **-Y**
- Up: **+Z**
- Origin: center of base

Axis conversion at export is automatic.

---

## Quick Reference: Loading Sub-resources

| Need | Load |
|---|---|
| Local install (models, commands, validation) | `references/setup-install.md` |
| Marketplace search | `references/sourcing-strategy.md` |
| AI generation (Hunyuan3D), concept art (Pollinations, nano-banana) | `references/ai-generation.md` |
| Topology rules, poly budgets | `references/topology-rules.md` |
| UV, materials, PBR | `references/uv-materials.md` |
| Texturing white meshes | `references/texturing-strategy.md` |
| Post-import cleanup | `references/validation-checklist.md` |
| Naming objects, materials, files | `references/naming-conventions.md` |
| Export settings per format | `references/export-targets.md` |
| CLI tools (gltf-transform, gltfpack) | `references/cli-tools.md` |
| Characters, rigging (phase 2) | `references/characters.md` |
| Batch mode (wizard, runner, manifest) | `references/batch-mode.md` |
