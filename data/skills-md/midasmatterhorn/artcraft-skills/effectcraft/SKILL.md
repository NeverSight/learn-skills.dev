---
name: effectcraft
description: >-
  EffectCraft is an open-source, pure-Rust motion-graphics, compositing and VFX app for macOS,
  Windows, Linux and the web — a clean-room, After Effects-shaped studio with compositions,
  layers, keyframes, 308 effects, expressions, Classic/Advanced 3D, tracking, roto, After Effects
  project interchange (`.aep`/`.aepx` in, `.aep` out — a verified subset that reports what it
  cannot carry), a render queue, Lottie, replayable repro scripts, and a plug-in surface
  (WebAssembly ABI 1/2 effect plug-ins, the Plug-in Library, out-of-process external helpers),
  driven by a CLI, an MCP server, a localhost JSON control channel and JavaScript scripting.
  Trigger this skill whenever the user mentions EffectCraft, `.ecproj`/`.ecprojx`/`.ectemplate`/
  `.ecpreset`, `effectcraft-cli`, its MCP tools or control channel; asks what it can or cannot do,
  which formats or shortcuts it has, or how to script, batch, render, verify, replay, repair or
  troubleshoot it; or describes the job without naming the app ("make a title card", "animate this
  logo", "key this green screen", "render a ProRes", "export Lottie", "open this .aep"). Also use
  it when choosing between EffectCraft and FilmCraft, or preparing and verifying assets for it.
  `.aep` interchange is a documented subset, not parity: expect a report of what did not come
  across, and never promise an After Effects-identical render.
---

# EffectCraft

**Audit basis.** Refreshed 2026-11-12 against tag **v0.24.1**, commit **`582344dd4ef462362c02e56e3094de7af01847ab`** (`git rev-parse HEAD` and `git describe --tags` in the pinned checkout agree), and the installed EffectCraft bundle is 0.24.1 — its recorded `--version` string is `effectcraft 0.24.1` and its bundle id is `ai.storyteller.effectcraft`. The previous release this skill described was v0.22.0 (`42e3c6a6c119d973aa59ab0437487ea6cae6a15d`). No `effectcraft-cli` binary is installed on the authoring machine (the `.app` contains none), so every count below is a static count from the code, not from `info`/`commands`.

**v0.22.0 → v0.24.1 delta.** 476 files changed, +35,892/−4,162 (`git diff --shortstat v0.22.0..HEAD`; the checkout is a two-commit shallow clone, so the file diff is the count that can be made locally). Five movements matter to this skill.

1. **Replayable repro scripts are a new agent surface.** `crates/engine/src/replay.rs` (new) defines a JSON-lines script — a `start` line, `command` steps with optional `expect_error`, and `expect`/`expect_no_error` assertions — and the session journal exports it: `journal.export {path?}` and `help.exportRepro {path?}` in the new `crates/engine/src/cmd/journal.rs` (both `journal: false`). `effectcraft-cli replay SCRIPT.jsonl [--keep-going]` runs one headless (`apps/effectcraft-cli/src/main.rs`), `crates/host/tests/it/repros.rs` replays every `tests/repros/*.jsonl` as a regression test, and the last-resort panic guard writes `Repros/crash-<time>-<command>.jsonl` in the settings folder. Scripts are capped at 64 MiB (`MAX_SCRIPT_BYTES`); see `docs/agents.md` §Repro scripts.
2. **Layer ▸ Un-precompose and a naming pass.** `layer.unprecompose {layer?, force?, dryRun?}` (`crates/engine/src/cmd/layer.rs`, implementation in `crates/engine/src/cmd/layer/timing.rs`, UI in `crates/ui-egui/src/panels/unprecompose.rs`) expands a pre-comp layer into copies of its composition's layers in one undo step; anything that would change the picture is an error listing every reason unless `force`, and `dryRun` returns the warnings only. 72 effect display names were renamed with ids, parameter ids, command ids and serialized names untouched (`RENAMED` in `crates/effects/src/display_names.rs`, policy and table in `docs/feature-naming.md`) — the 69 `CC …` effects plus `Lumetri Color` → `Color Grading`, `Mocha shape` → `Tracked Shape Matte`, `Key Light` → `Screen Color Key` — and every old display name remains a case-insensitive lookup and search alias (`crates/effects/src/lib.rs`). The renderer now reads **GPU Acceleration** / **Software Rendering**, and the **Lumetri Scopes** panel's title is **Video Scopes** (id unchanged).
3. **After Effects import grew again, and `file.import` takes projects.** New `crates/aep/src/import/lumetri.rs` (Lumetri Color: master RGB curve, Hue vs Sat, colour wheels, ~62 mapped controls) and `crates/aep/src/import/puppet.rs` (After Effects' Puppet arrives with its name and switch but without meshes/pins, reported per mesh). The quick-win block covers HDR Highlight Compression, Echo, Linear Wipe, Offset and Color Stabilizer; the third-party block covers CC Color Neutralizer, EXtractoR and IDentifier (`docs/aep-import.md`). Keyed or expression-driven Orientation imports with its value or keys (#3087), a placed `.ai`/`.pdf` is framed by its ArtBox (#3099), an image sequence needs no filename prefix and honours Force alphabetical order (#3213), and the loss report now carries a per-category `unlisted` count (`crates/aep/src/import/report.rs`, `MAX_DETAILS = 20`). The menus now say **File ▸ Import / Export ▸ Adobe After Effects Project…**, and `file.import` accepts `.aep`/`.aepx` (and `.ecproj`/`.ecprojx`), returning them under `projects` (`crates/engine/src/cmd/file.rs`).
4. **Render, GPU and preview behaviour.** The Render Queue sizes GPU frames in flight from measured memory: `memory.gpuFramesInFlight` (`auto|1|2|3`, `EFFECTCRAFT_GPU_INFLIGHT`) in `crates/engine/src/settings/prefs/sections.rs`, resolved in `crates/export/src/pipeline.rs`; a saved frame-rate override is clamped to the supported rates and says so, and an output module's Crop/Resize is capped at 30 000 px per side (`crates/project/src/render_queue.rs`). A decoded footage picture uploads once and is shared by every layer that shows it (`crates/gpu/src/upload.rs`, new); the disk cache stores the files each cached frame read and re-checks them (`crates/render/src/disk_cache/entry_files.rs`, new). The preview now renders at most two frames on the GPU at once so video memory stays flat (`MAX_GPU_RENDERS = 2` in `crates/ui-egui/src/frames.rs`, #3028). Also: time stretch is held to ±1 % … ±9900 % (`crates/project/src/limits.rs`), a numbering gap in an image sequence holds the previous frame (`crates/project/src/sequence.rs`), a text layer's name follows its text until renamed (`crates/project/src/layer.rs`), and 3D rotation order, keyed Orientation, linear-to-eased keyframes and Timewarp now behave as in After Effects (#1876).
5. **Control channel and confinement.** A `renderQueue.render` through `engine.execute` (or a scripted render) keeps the window responsive: only a whitelist of methods answers while it waits (`ui.inspect`, `ui.elements`, command/menu listings, resize, focus, and the queries named in `docs/control-protocol.md`), the rest error, the **Stop Render** button is the automation id `scriptRender.stop` (`crates/ui-egui/src/app/frame.rs`), and the 60 s transport timeout still applies. Confined automation is stricter: a confined batch step cannot take its params from a `$N` reference, and a render refuses an output folder holding a symbolic link that leads outside the write roots, including numbered sequence folders (`crates/automation/src/confine.rs`).

The registry went **700 → 703 ids** (+3, nothing removed): `layer.unprecompose`, `journal.export`, `help.exportRepro`. The macro-extracted count (the figure earlier rounds quoted) went 697 → 698; the other five ids are built as literal `CommandSpec` values or through `journal.rs`'s `spec()` helper — the method and the correction are in `evidence.md`. Everything else the previous audit counted is **unchanged at v0.24.1** and listed with its evidence below.

**v0.21.0 → v0.22.0 delta.** 203 commits. After Effects projects became readable and writable (a new `crates/aep` crate, `file.importAep`/`file.exportAep`, with per-category loss reports and a refusal unless `allowLosses`), the extension surface grew (native plug-in API 2, external effect helpers in `crates/helper-host`, the 8-command Plug-in Library, `effect.plugins.install`), OpenEXR output gained `exrCompression` (10 methods) and `exrBitDepth` (half/float), and `layer.quickSetAnchor`, `mask.setRoundness`, the CLI `--save` lock and the Roto Brush session cache landed. The macro-extracted command count went 681 → 697 in that release.

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may differ; every count quoted here was re-measured at v0.24.1, and every cited path was re-resolved against that tag. The method for each count is in `evidence.md`.

## Overview

EffectCraft is a free, open-source, clean-room reimplementation of Adobe After Effects 2026 for motion graphics and visual effects: compositions, layers, keyframes, 308 effects, layer styles, expressions, Classic and Advanced 3D, tracking, roto/paint, a render queue, Lottie and timeline interchange, and After Effects project import/export (a verified subset since v0.22.0). It is pure Rust with no FFmpeg: media codecs come from the sibling FilmCraft project, pinned by revision in `Cargo.toml`. It is **alpha**: `docs/gaps.md` self-rates ≈91% feature breadth but ≈45% "ready for real work", and `README.md` says it is not yet recommended for production client work. FilmCraft is the editing/NLE sibling; EffectCraft is the compositor. Source: GitHub `storytold/effectcraft`, MIT OR Apache-2.0. Everything a user can do is an engine command (703 registered ids), so the CLI, MCP, the control channel and scripts are peer entry points rather than a separate API.

## Capabilities (verified)

### Project and document model

- **Native `.ecproj`** is versioned, pretty-printed JSON headed by `savedBy` and `schema` (**2**, re-exported from the pinned `craft-ecproj-format` crate through `crates/project/src/settings.rs`), with `activeComp`/`openComps`/`compTimes`, `settings`, `items`, `nextId`, `renderQueue`, render templates and preferences (`crates/project/src/lib.rs`). Saving re-reads the text before writing and writes atomically; a project whose `savedBy` is a newer version still opens, with a warning.
- **XML project copy `.ecprojx`** is the same data as `EffectCraftProject` XML (lossless); Save a Copy As XML writes it, `file.open` reads it back (`crates/engine/src/cmd/file.rs`).
- **Autosave, crash recovery and MCP checkpoints**: `mcp --autosave` writes a checkpoint after each mutating call (`crates/engine/src/settings/autosave.rs`, `docs/agents.md`). Out-of-range values are repaired on open and reported in the result's `repaired` list, not rejected (`crates/project/src/limits.rs`).
- **One project per app process**, with compositions open as tabs in the timeline group's tab row (overflow menu for the rest). **34 panel kinds** in `PanelKind::ALL` plus the parameterised `Viewer(u32)` and `ScriptPanel(u32)`, **15 named workspaces** (`crates/ui-egui/src/dock.rs`), and any panel can move to its own native window.

### After Effects project interchange

- **Import** `file.importAep {path, allowLosses?, dryRun?, applySettings?}` reads `.aep` (RIFX) or `.aepx` and adds its items in a folder named after the file, in one undo step, returning `{folder, comps, items, report}`; the first composition opens. `file.import` hands an `.aep`/`.aepx` to the same importer and reports it under `projects`. Covered areas include the project tree, project settings, compositions, layer/footage/text/precomp/solid layers with switches and blend modes, transforms and keyframes with eases, expressions, cameras and lights, track mattes, masks, shape groups, text documents and text animators, markers, time remapping, layer styles, image sequences, placed `.ai`/`.pdf` pages, and a table of effects that now includes Lumetri Color, Curves, Mesh Warp and the quick-win and third-party blocks (`docs/aep-import.md`, `crates/aep/src/import`, `crates/aep/src/container/effect_map.rs`). Everything else is counted in the report (up to 20 example lines per category plus an `unlisted` count); **without `allowLosses` an import that would lose anything is refused and changes nothing**. `applySettings` defaults to true only when the project has no compositions.
- **Export** `file.exportAep {path, allowLosses?, dryRun?}` writes an `.aep` that After Effects 2026 opens, every chunk built in code (no template file is read), returning `{path, bytes, report}` (`docs/aep-export.md`, `crates/aep/src/export`). The same loss rule applies: unsupported items are reported, and without `allowLosses` nothing is written.
- Details, the report categories and a round-trip recipe are in **`references/after-effects-projects.md`**.

### Composition, animation, expressions

- **Compositions** use exact integer `Tick` time at 254,016,000,000 ticks/s; `comp.new` defaults to 1920×1080, 29.97 fps, 10 s, and accepts `renderer: classic3D|advanced3D` (`crates/engine/src/cmd/comp.rs`). Layer kinds cover footage, precomp, solid, text, shape, null, camera, light, 3D model and parametric primitive; adjustment layers are solids with the adjustment switch.
- **Parenting, track mattes, all 38 blend modes and motion blur** are in the document model (`crates/color/src/blend.rs`; blend modes unchanged at v0.24.1).
- **Keyframes**: linear/Bezier/hold, per-side speed and influence (Easy Ease), auto/continuous Bezier, roving keys, Keyframe Velocity/Interpolation, and a Graph Editor with value and speed graphs. Time remap/stretch/reverse/freeze are `layer.*` commands; a stretch is held to ±1 % … ±9900 % (`crates/project/src/limits.rs`).
- **Expressions** run on `boa` with the AE object model (`thisComp`, `thisLayer`, `thisProperty`, `valueAtTime`, `velocityAtTime`, `wiggle`, `temporalWiggle`, `smooth`, `loopIn/Out`, `sampleImage`, `sourceRectAtTime`, `nearestKey`, `propertyGroup`, text style API) and AE legacy array maths (`crates/expr/src/lib.rs`).
- **Layer operations**: `layer.unprecompose` (see the delta), `layer.quickSetAnchor {point, layers?}` (nine content points, compensates Position and its keys; 3D, locked and expression-driven layers are skipped), precompose, time remap/stretch and the rest of `layer.*` (`crates/engine/src/cmd/layer.rs`).

### Effects, text, shapes, masks

- **308 registered effects, 2988 parameters, 280 GPU-capable, all 32-bit float, 21 categories, 0 marked partial** — unchanged at v0.24.1 (`docs/effects.md`, generated from the registry and enforced by the `effects_doc_is_current` test in `crates/effects/src/catalog.rs`; `PARTIAL` is an empty slice). Effects are addressed by id (`ec.<category>.<name>`) or display name; **72 names changed in this release** while ids stayed, and every old name still resolves (`crates/effects/src/display_names.rs`, `crates/effects/src/lib.rs`).
- **76 built-in presets**: 8 text animators, 23 backgrounds, 23 transitions and 22 behaviors (unchanged; `crates/engine/presets/*.json`, applied with `anim.applyBuiltinPreset`), plus `.ecpreset` save/apply.
- **Text, shapes and masks**: point/paragraph text with style runs, variable fonts, text animators; a text layer's name follows its first line until the user renames it (`crates/project/src/layer.rs`); shape operators (trim, repeater, round corners, offset, zig zag, twist, wiggle, merge, gradient stroke); masks with **7 modes**, feather, expansion, vertex editing, Mask Interpolation and `mask.setRoundness` (per-corner radius in px).
- **Cryptomatte**: `effect.pickCryptomatte` replaces/edits the effect's Selection with the ID under a point, in one undo step; `effect.cryptomatteAt` only reports.

### 3D, tracking, roto and paint

- **Classic 3D and Advanced 3D**: 3D layers, one/two-node cameras with depth of field, Parallel/Spot/Point/Ambient/Environment lights, ray-cast shadows; Advanced 3D adds PBR materials, six primitives, imported models and environment lighting.
- **Tracking**: point/transform tracking, stabilize, affine/perspective corner-pin tracks, mask tracking including face outline/detailed features, Warp Stabilizer, and a 3D Camera Tracker that creates cameras, solids, nulls, text and shadow catchers and reports how many frames a partial solve solved.
- **Roto Brush, Object Matte and SAM 2**: stroke/propagate/freeze with optional MobileSAM or a SAM 2.1 model, and a classical fallback when the tracker fails; frozen mattes stay usable in a session without the model file. `roto.model.select` takes `classical | mobilesam | sam2.1-hiera-tiny | sam2.1-hiera-small | sam2.1-hiera-base-plus | sam2.1-hiera-large` (`crates/engine/src/analysis/models.rs`). Face tracking can use the optional MediaPipe Face Landmarker.
- **Paint, Liquify and puppet pins** are commands; **Content-Aware Fill and Scene Edit Detection** run as background jobs with `wait` (Content-Aware Fill's synthesis runs on the GPU); **Auto-trace** is synchronous. `effectcraft-cli bench --roto` measures the trackers.

### Import formats (only what the code registers)

| Kind | Extensions / route | Evidence |
|---|---|---|
| Stills | `png jpg jpeg gif webp tif tiff bmp exr tga hdr psd psb svg pdf ai eps` (17; animated WebP as footage) | `crates/media/src/lib.rs` `STILL_EXTENSIONS` |
| Film scans | `dpx cin` (8/10/12/16-bit; log shown as stored) | `crates/media/src/dpx.rs` |
| Video | `mp4 m4v mov mkv webm mxf avi`; H.264, HEVC, VP9, AV1, ProRes, DNxHD, MPEG-2, MJPEG; MXF OP1a/OP-Atom; AVI import is partial (AVI 1.0/OpenDML: Motion JPEG, H.264, HEVC, uncompressed; no AVI output) | `crates/project/src/footage.rs`, `docs/file-format-parity.md` |
| Audio | `wav wave bwf aif aiff mp3 mp2 m4a aac flac ogg opus` — the list lives in the pinned FilmCraft codec crate and is only re-exported here, so confirm on your install | `crates/media/src/lib.rs` (`filmcraft_media::AUDIO_EXTENSIONS`) |
| 3D models | `gltf glb obj stl fbx` (glTF: meshes/PBR/skins/animations; FBX 7.x: meshes/materials only) | `crates/media/src/lib.rs`, `crates/model/src/fbx.rs` |
| After Effects projects | `.aep`, `.aepx` via `file.importAep` or `file.import` (see above) | `crates/aep/src/import`, `docs/aep-import.md` |
| Data | `json csv tsv` as data footage (plain `file.import`; Lottie needs `file.importLottie`) | `crates/engine/src/cmd/file.rs` `DATA_EXTENSIONS` |
| Lottie | `.json`, `.lottie` via `file.importLottie`; export `file.exportLottie` | `crates/lottie/` |
| Timelines | `.xml` (FCP7), `.fcpxml`, `.otio`, `.edl`, `.aaf`, `.omf` | `crates/interchange/src/lib.rs` |
| Color / fonts | LUTs `.cube .3dl .csp .spi1d/.spi3d`, CDL; bundled + installed fonts, `EFFECTCRAFT_FONT_DIRS` | `docs/file-format-parity.md`, `crates/text/src/font_dirs.rs` |

`.json` through plain `file.import` is **data footage**, not Lottie. PSD/PDF/AI/EPS import as footage or as a composition (`importAs`). An image sequence is one numbered file with `sequence: true`, or a folder; a gap in the numbering holds the previous frame.

### Export formats

The Render Queue writes **14 formats** (`crates/project/src/render_queue.rs`, `OutputFormat::ALL`; unchanged at v0.24.1):

| Family | Formats |
|---|---|
| Video | H.264 MP4 (+AAC), HEVC MP4 (`hvc1`), AV1 MP4 (`av01`), ProRes MOV (Proxy→4444 XQ; 4444 with alpha), uncompressed 8-bit MOV, WebM (VP9 or AV1 + Opus) |
| Stills | PNG, JPEG, TIFF, OpenEXR (`exrCompression` × 10, `exrBitDepth` half/float — scan-line), Targa (24-bit RGB or 32-bit RGBA) sequences; animated GIF |
| Audio | WAV, AIFF (16-bit PCM) |

Render Settings/Output Modules cover quality, resolution, time span (**Work Area by default**), frame rate (a saved override is clamped to the supported rates), proxy use, overrides, colour depth, field rendering, motion blur, frame blending, skip existing frames, crop/ROI/resize (capped at 30 000 px per side), extra outputs, post-render actions and logs. The movie encoders tag the frames' own colour in the H.264/HEVC/AV1 bitstreams.

- **Single frames** also export as a layered PSD (`comp.saveFrameAsPsd`) or a multi-layer OpenEXR (`comp.saveFrameAsExr`).
- **After Effects project** `.aep` via `file.exportAep` (subset with a loss report; `.aepx` is not written).
- **Lottie** `.json`/`.lottie` with a `warnings` list.
- **Timeline interchange** `.xml` (FCP7 default), `.fcpxml`, `.otio`, `.edl`, `.aaf`, `.omf`.
- **Essential Graphics template `.ectemplate`** and **animation preset `.ecpreset`**.

### Automation and platform (every count re-measured at v0.24.1)

| Surface | Count | vs v0.22.0 | Evidence |
|---|---|---:|---|
| Registry command ids | **703** | **+3, none removed** | `crates/engine/src/cmd.rs` `command_specs()` (83 `specs()` modules) plus 5 ids built outside the macros |
| UI-only command ids | 111 | unchanged | `crates/ui-egui/src/menus/commands.rs` |
| MCP tools | 36 (27 headless + 9 bridge-only) | unchanged | `crates/automation/src/tools.rs` |
| Control-channel methods | 24 (21 dispatch arms) | unchanged | `crates/ui-egui/src/control.rs` |
| CLI subcommands | 13 | +`replay` | `apps/effectcraft-cli/src/main.rs` |
| Render Queue formats | 14 | unchanged | `crates/project/src/render_queue.rs` |
| EXR compression / bit depth | 10 / 2 | unchanged | same |
| Effects / parameters | 308 / 2988 | unchanged | `docs/effects.md` (generated, test-enforced) |
| GPU / categories / partial | 280 / 21 / 0 | unchanged | same; `crates/effects/src/catalog.rs` |
| Blend modes | 38 | unchanged | `crates/color/src/blend.rs` |
| Layer styles | 9 (+ Blending Options) | unchanged | `crates/project/src/styles.rs` |
| Mask modes | 7 | unchanged | `crates/project/src/props.rs` |
| Menu languages / panel catalogs | 13 / 11 | unchanged | `crates/ui-egui/src/i18n.rs`, `crates/ui-egui/src/i18n/ui.rs` |
| Built-in presets | 76 (8/23/23/22) | unchanged | `crates/engine/presets/*.json` |
| Panel kinds / workspaces | 34 (+2 parameterised) / 15 | unchanged | `crates/ui-egui/src/dock.rs` |
| WebAssembly plug-in ABI | 1 and 2 | ABI 2 added | `crates/effects/src/plugin.rs` |

- **CLI** `effectcraft-cli`: 13 subcommands — `info commands exec run props get set render-frame render bench script replay mcp` — with `--json`, `--project`, `--demo`, `--empty`, `--save`, `--save-as`, `--bridge`, `--gpu`, per-codec render flags, `--queue` and `--progress`; `run --args-file F` reads one argument per line, `run --commands FILE|-` reads JSON steps, `render` also takes `--exr-compression`/`--exr-depth`, and `render`/`render-frame` take `--template T.ectemplate --values V.json`. `replay SCRIPT.jsonl` runs a repro script headless and exits 1 on the first failure.
- **MCP** over stdio: **36 tools** — 27 headless and 9 bridge-only (`screenshot`, `ui_inspect`, `ui_elements`, `ui_click`, `ui_drag`, `ui_key`, `ui_type`, `ui_set`, `control`) — plus resources `effectcraft://document` and `effectcraft://commands` (`crates/automation/src/server.rs`; unchanged at v0.24.1).
- **Control channel**: `effectcraft --control <port>` (or `EFFECTCRAFT_CONTROL_PORT`) speaks newline JSON on `127.0.0.1`: **24 methods** — `engine.execute`, `ui.menu.invoke`, `engine.commands`, `ui.menu.list`, `render.frame`, `ui.inspect/elements/set/screenshot/click/move/drag/scroll/key/type`, `ui.panel.show/close`, `ui.playback`, `ui.resize`, `ui.focus`, `ui.viewer.locate/hit`, `ui.timeline.locate`, `app.quit`. While a `renderQueue.render` waits, only the documented subset answers (`docs/control-protocol.md` §Waiting for a render).
- **Two command tiers**: engine ids run headless (CLI/MCP/`engine.execute`); UI-only ids dispatch only in the live app. No command is a disabled stub (`stubs::specs()` is empty).
- **Extensions** (details in `references/extensions.md`): WebAssembly effect plug-ins (`.wasm`/`.wat`, ABI 1 `ec_render` or ABI 2 `ec_render2` with neighbouring frames, sandboxed in `wasmi` with no imports), a **native plug-in API 2**, **external helpers** (out-of-process native effect hosts, protocol v1), a **Plug-in Library** (8 `library.*` commands over a reviewed catalog with SHA-256 checks, accepting both ABIs), scripts and ScriptUI panels (`.jsx`/`.js`, Startup/Shutdown folders, script shortcuts).
- **Scripts/ScriptUI**: `.jsx`/`.js` with the AE object model and dockable ScriptUI panels; `script.run`, `file.runScript`, CLI `script FILE.jsx`.
- **Web build** (`apps/effectcraft-web`) runs the same engine/UI as WASM with OPFS/IndexedDB storage and `window.effectcraft`; it is not the installed macOS app. External helpers are desktop-only.
- **GPU**: a wgpu compute compositor for Metal/Vulkan/Direct3D 12/WebGPU; CPU is the reference; headless CLI/MCP render on the CPU and say so unless started with `--gpu`.
- **Localization** (unchanged at v0.24.1): menu catalogs in **13** languages (cs, de, es, fr, pl, pt-br, sv, ru, uk, ka, ja, zh-hans, zh-hant); panel/tooltip catalogs in **11** (no de, ru). Korean and Italian remain absent (`crates/ui-egui/src/i18n.rs` `CATALOG_CODES`).

## Known limitations and not-implemented

- **After Effects interchange is a subset, not parity.** `.aep`/`.aepx` import and `.aep` export cover what the reader/writer decoded and tests; effects outside the importer's table, Puppet meshes and pins, undecoded text/style settings and approximated keyframes arrive as report entries, and orientation curves interpolate per angle where After Effects slerps — and without `allowLosses` the whole operation is refused. `.aepx` is not written. A clean report means "nothing was dropped", not "it looks the same".
- **Still no `.ffx` presets, `.mogrt` templates, AE SDK plug-ins (`.aex`/`.plugin`) or `.prproj`.** Only `.ecproj`/`.ecprojx`, `.ecpreset` and `.ectemplate` are native project/sidecar formats; `.prproj` must be converted to FCP7 XML in Premiere first.
- **Fidelity against After Effects is mostly unmeasured.** Live comparisons (scalar ease plus Tint, Tritone, Black & White, Exposure, Levels (Individual Controls), Curves, Luma Key, Extract, 4-Color Gradient and Fill) match After Effects 2026 renders within 1–3/255; Brightness & Contrast up to 6.2/255. Everything else is self-graded — never promise AE-identical renders (`docs/fidelity/README.md`).
- **Alpha stability.** `docs/gaps.md` still lists open defects; re-check the tracker rather than quoting this skill. Crash reporting is a separate helper process that only reports an unexpected desktop exit (`apps/effectcraft/src/crash_report.rs`); it is not an agent surface.
- **No hardware video decode/encode** (VideoToolbox, NVENC, Quick Sync, VA-API). HEVC/AV1 have no B-frames, multi-reference or SAO/CDEF; Opus has no FEC/DTX.
- **Output/import gaps**: no 16-bpc uncompressed, MXF, DNxHR, DPX or Photoshop *sequence* output, and no AVI output (AVI import only); no ProRes RAW, USD/USDZ, Substance `.sbsar`, camera raw, HEIF/AVIF, BRAW/R3D/ARRIRAW.
- **FBX/DPX/PDF caveats**: FBX is 7.x only, with no animation, skinning, cameras or lights; DPX/Cineon log values are shown as stored; PDF/AI/EPS import lacks JPX/JBIG2 and Illustrator procset EPS.
- **Scripting gaps**: no `.jsxbin`; no separate Legacy ExtendScript engine mode (the `boa` engine implements the documented object model); `BridgeTalk` names the host but cannot message other applications; Startup scripts each get their own global scope, so definitions do not carry between them.
- **No CLI inside the macOS `.app`** — the universal `effectcraft-cli` comes from its separate release zip (see *Getting the CLI* under How to operate); building it (`cargo build --release -p effectcraft-cli`) is a developer path only — full Rust toolchain and a source checkout. **The control channel has no authentication**, binds `127.0.0.1`, serves at most 16 connections, times out at 60 s and rejects lines over 4 MiB (`apps/effectcraft/src/control_server.rs`).
- **Extensions are an install surface, not a sandbox boundary for agents.** Native helpers run native code and start only when asked (`effect.helpers.scan`) or when `EFFECTCRAFT_HELPERS=1`; agents confined with `--automation-read-root`/`--automation-write-root` cannot run `effect.helpers.scan` or `effect.helpers.load`, cannot pass `$N`-referenced params through a confined batch, and a render refuses outward links. A WebAssembly module written for ABI 1 still loads, but a module that needs neighbouring frames must declare `ec_api_version` 2 and export `ec_render2`.
- **Repro scripts are not private.** A repro holds command ids and parameters only — never project or media contents — but parameters can include file paths, layer names and text typed into text layers (`crates/engine/src/replay.rs`, `docs/agents.md`). Read one before sharing it.
- **Docs drift — trust code/runtime.** Five docs still say **306 effects** (`docs/architecture.md`, `docs/roadmap.md`, `docs/gaps.md`, `docs/hardware-parity.md`, `docs/target-app-parity.md`); `docs/target-app-parity.md` says "411 registered engine commands"; `README.md` still claims proprietary project formats are unsupported; `docs/gaps.md` still rates "Opening existing After Effects work ≈ 0%" and says `.aep` cannot be read; and `app.capabilities`' `PARITY` string (`crates/engine/src/cmd/query.rs`) still says "307 registered" effects. The gap-4 "no PR CI gate" note is closed — `.github/workflows/ci.yml` runs `cargo xtask ci` on every pull request.

## How to operate

### Launch (macOS)

```sh
open -a EffectCraft                                  # empty Untitled Project (not the demo)
open -a EffectCraft Project.ecproj                   # open a project
open -a EffectCraft --args --control 9877 --demo     # agent-driven window + demo project
EffectCraft.app/Contents/MacOS/EffectCraft --control 9877 --demo   # the binary inside the bundle
```

Flags: `--control <1-65535>` (or `EFFECTCRAFT_CONTROL_PORT`), `--demo`, `--empty`, `--home`, `--version`; after `--` every argument is a file. An unknown option or a bad port exits before the window opens (`apps/effectcraft/src/main.rs`). The app starts **empty** by default, unlike most one-shot CLI commands, which start with the demo.

### Getting the CLI (the launcher installs the app, not the CLI)

The ArtCraft Launcher installs `EffectCraft.app`; it does not put `effectcraft-cli` on your `PATH`. It ships **no** CLI binary inside the bundle — the bundle holds only `EffectCraft` — so a launcher-only install has no `effectcraft-cli` at all. The CLI is published on the app's GitHub release, `effectcraft-cli-0.24.1-macos-universal.zip` (77.3 MB), so `effectcraft-cli` answering *command not found* means "not installed yet", not "not supported".

Find it, in this order:

1. **On `PATH`** — `command -v effectcraft-cli`. If it answers, `effectcraft-cli --version` must report the version this skill was written against (0.24.1). A different version means the CLI and the app have drifted: re-read *Verify against your installed version* before trusting ids.
2. **Bundle copy** — Skip it: `find "/Applications/EffectCraft.app" -name 'effectcraft-cli'` finds nothing (verified), so go to step 3.
3. **Install it from the release** — user-local, no `sudo`:

```sh
APP_VER=0.24.1
REL="https://github.com/storytold/effectcraft/releases/download/v$APP_VER"
ASSET="effectcraft-cli-$APP_VER-macos-universal.zip"
mkdir -p "$HOME/.local/bin" "$HOME/Downloads/effectcraft-cli" && cd "$HOME/Downloads/effectcraft-cli"
curl -fLO "$REL/$ASSET" && curl -fLO "$REL/SHA256SUMS.txt"
expected=$(grep -F "$ASSET" SHA256SUMS.txt | awk '{print $1}')
actual=$(shasum -a 256 "$ASSET" | awk '{print $1}')
[ "$expected" = "$actual" ] && echo "checksum OK" || { echo "checksum MISMATCH — stop"; exit 1; }
unzip -oq "$ASSET"
install -m 0755 "effectcraft-cli-$APP_VER-macos-universal/effectcraft-cli" "$HOME/.local/bin/effectcraft-cli"
"$HOME/.local/bin/effectcraft-cli" --version
```

`~/.local/bin` must be on `PATH` for the shell that runs the skill: `export PATH="$HOME/.local/bin:$PATH"` (put it in your shell profile to keep it).

Rules: never `sudo` into `/usr/local`, never unzip into `/Applications`, and never replace an existing `effectcraft-cli` of a different version without telling the user. Building from source (`cargo install --path apps/effectcraft-cli --locked`) is a developer path only — full Rust toolchain, minutes of compiling; prefer the release binary above.

### CLI

`<comp>` is an id, name or `-` (active comp); `<layer>` is an id, `#n` or name; values are JSON or bare strings.

| Subcommand | What it does |
|---|---|
| `info` | version, mode (headless/bridge), command and effect counts, project and active comp |
| `commands` / `exec --list` | list engine commands; `--filter TEXT`, `--enabled`, `--schemas` |
| `exec <id> [json]` | run one command |
| `run <id> [json] …` | run several in order, stopping at the first error; `--args-file F`, `--commands FILE\|-` |
| `props <comp> <layer>` | property tree with paths; `--flat`, `--time S`, `--depth N`; an enum prints its label beside the number |
| `get` / `set <comp> <layer> <path> [value]` | read/write one property (`--time`, `--expression`) |
| `render-frame` | PNG frame; `--time/--frame`, `--max-side/--scale`, `--transparent`, `--template/--values` |
| `render` | one comp (`--comp`, `--out`, codec flags, `--exr-compression`, `--exr-depth`, `--template/--values`) or the project queue (`--queue`); `--progress` |
| `bench` | render timings, GPU vs CPU, `--ops` everyday-operation timings, `--roto` tracker quality |
| `script FILE.jsx` | run AE-style JavaScript; `--eval CODE` |
| `replay SCRIPT.jsonl` | run a repro script headless; `--keep-going`; exits 1 on the first failure |
| `mcp` | MCP server on stdio; `--autosave`, `--bridge PORT`, `--automation-read-root`, `--automation-write-root` |

- **Most commands open the demo project** unless you pass `--project F.ecproj`, a positional `*.ecproj`, or `--empty`. `commands`, `script` and `mcp` start empty; `replay` builds its session from the script's `start` line (`new`, `demo` or a project path) and refuses a competing `--project`/`--demo`/`--empty`/`--bridge`.
- `--save` writes back to the opened project, `--save-as F` writes a copy, and two concurrent `--save` runs over one project serialise on an OS lock file next to the project (`apps/effectcraft-cli/src/project_lock.rs`). `--gpu` attaches the GPU compositor; CPU is the default.
- `render` needs `--out` (or `--queue`); `render --comp …` renders exactly one item; `--progress` prints progress lines on stderr.
- `mcp --automation-read-root DIR / --automation-write-root DIR` (repeatable) confine agent file access.

### MCP

`effectcraft-cli mcp` serves JSON-RPC 2.0 over stdio, one message per line. It has **36 tools**:

| Group | Tools |
|---|---|
| Commands | `list_commands`, `describe_command`, `execute_command`, `command_list`, `command_run`, `batch`, `command_batch` |
| Project / properties | `get_project`, `doc_inspect`, `get_comp`, `get_layer`, `get_property`, `set_property`, `add_keyframe`, `add_effect`, `list_effects`, `list_fonts`, `get_state` |
| Files / history / scripting | `open_project`, `save_project`, `undo`, `redo`, `history`, `run_script`, `script_ui` |
| Render | `render_frame`, `render_preview` |
| Bridge-only (9) | `screenshot`, `ui_inspect`, `ui_elements`, `ui_click`, `ui_drag`, `ui_key`, `ui_type`, `ui_set`, `control` |

Resources `effectcraft://document` and `effectcraft://commands`. `batch` is atomic (`$N.key` references); `command_batch` stops at the first error by default. A `renderQueue.render` call with `_meta.progressToken` emits progress notifications and can be cancelled.

### Control channel

`effectcraft --control 9877` accepts one JSON object per line and replies per line. **24 methods**: engine/menus (`engine.execute`, `ui.menu.invoke`, `engine.commands`, `ui.menu.list`), render (`render.frame`), inspect (`ui.inspect`, `ui.elements`, `ui.set`, `ui.screenshot`), input (`ui.click`, `ui.move`, `ui.drag`, `ui.scroll`, `ui.key`, `ui.type`), panels/playback (`ui.panel.show`, `ui.panel.close`, `ui.playback`, `ui.resize`, `ui.focus`), viewer/timeline (`ui.viewer.locate`, `ui.viewer.hit`, `ui.timeline.locate`) and `app.quit`. `ui.elements` lists widgets drawn in the last frame `{id,label,rect}`; `ui.screenshot` returns a PNG.

While a `renderQueue.render` (through `engine.execute`) or a scripted `renderQueue.render()` waits, the window stays responsive: inspection and command/menu listings still answer, other requests error, and the **Stop Render** button answers to `scriptRender.stop`. Drive Stop from a second connection — requests on one connection are answered in order — and remember the 60 s request timeout still applies.

### Document model and workflow

One project per app process in one main window; each open composition is a tab in the timeline group's tab row. Panels follow After Effects, dock/float on craft-ui's shared docking, and any panel can move to its own native window. Each layer carries a property tree addressed by paths such as `transform/position`, `effects/#1/blurriness` or `@<uid>`.

1. Create a composition (`comp.new`) and add layers (`layer.new*`, `file.import`, `layer.replaceSource`).
2. Animate (`prop.set`/`prop.addKey`) and ease (`keys.select` + `keys.easyEase`).
3. Apply effects (`effect.apply`), edit `effects/#1/...`, preview and save.
4. Export via `renderQueue.add` + `renderQueue.render`, or Lottie/timeline/template/AE-project commands.

```sh
effectcraft-cli exec comp.new '{"name":"Main","width":1920,"height":1080,"frameRate":30,"duration":3}' --empty --save-as main.ecproj
effectcraft-cli exec layer.newText '{"text":"Hello","name":"Title","size":160,"fill":"#ffffff"}' main.ecproj --save
effectcraft-cli run main.ecproj \
  prop.addKey '{"layer":"Title","path":"transform/position","time":0,"value":[-400,540]}' \
  prop.addKey '{"layer":"Title","path":"transform/position","time":1,"value":[960,540]}' \
  keys.select '{"keys":[{"layer":"Title","path":"transform/position","time":0},{"layer":"Title","path":"transform/position","time":1}]}' \
  keys.easyEase '{"which":"both"}' --save
effectcraft-cli render main.ecproj --comp Main --out title.mp4 --format h264 --progress
effectcraft-cli exec file.importAep '{"path":"in.aep","allowLosses":true}' out.ecproj --save
```

Each headless CLI invocation is a new session: edits survive only if saved; group selection-dependent steps in one `run` (or one MCP session).

### Open / save / export, exact formats

- **Open** `.ecproj`, `.ecprojx`, or `.xml` whose root is `EffectCraftProject`; `file.import` merges another EffectCraft project, an After Effects one, or footage; `file.importAep` merges an After Effects one. **Save** `.ecproj`, or XML when the path is `.ecprojx`/`.xml`; Save a Copy, Save a Copy As XML and Increment and Save exist.
- **Export** the 14 Render Queue formats, single-frame layered PSD or multi-layer OpenEXR, `.aep`, Lottie, timeline formats, `.ectemplate`, `.ecpreset`. A `.xml` path is ambiguous: `file.open` expects an EffectCraft XML project, `file.importTimeline` expects FCP7 XML — use `.ecprojx` for projects.
- **Rejected**: `.prproj`, `.ffx`, `.mogrt` and `.aex`; the AE exporter writes `.aep` only, never `.aepx`.

### Keyboard shortcuts (only verified ones)

`Cmd+N` New Composition, `Cmd+K` Composition Settings, `Cmd+Shift+X` Trim Comp to Work Area, `Cmd+Alt+N` New Project, `Cmd+O` Open, `Cmd+S` Save, `Cmd+Alt+Shift+S` Increment and Save, `Cmd+Shift+S` Save As, `Cmd+I` Import, `Cmd+M` Add to Render Queue, `F9` Easy Ease, `Cmd+Alt+K` Keyframe Interpolation, `Cmd+Shift+K` Keyframe Velocity, `Cmd+Alt+H` Toggle Hold, `Cmd+Alt+T` Enable Time Remapping, `Cmd+G`/`Cmd+Shift+G` Group/Ungroup Shapes, `Cmd+Alt+/` (Cmd+Opt+/ on macOS) Replace Source. Property reveals (`A/P/S/R/T/M/F/E/L/U`, the double presses and Alt+Shift) are documented in `docs/agents.md` §"Timeline: layer order, properties and shortcuts" and `docs/control-protocol.md` (`timeline.reveal.*`, `timeline.keyAt.*`). Shortcuts are command data; for anything else read `effectcraft-cli commands --json` — do not invent shortcuts.

## Working with an AI agent

### Choose the surface

- **Headless (preferred)**: `effectcraft-cli exec/run` for one-shots or `effectcraft-cli mcp` for a persistent session; `mcp --autosave` checkpoints dirty work after each mutating call.
- **Live app**: start `effectcraft --control 9877`, then `mcp --bridge 9877` or the raw control channel. **Web**: no TCP channel; use `window.effectcraft`.

### Prepare inputs

- Convert unsupported sources: camera raw/ProRes RAW/BRAW/R3D/USDZ/Substance → H.264/ProRes/WebM or PNG/EXR/TIFF sequences; 3D → glTF/GLB/OBJ/STL/FBX 7.x; audio → WAV/AIFF; data → JSON/CSV/TSV.
- An `.aep` is a legitimate input now: run `file.importAep` with `dryRun: true` first, read the report (including `unlisted` counts), then decide whether to pass `allowLosses: true`. Never assume an After Effects project imports whole.
- Image sequences: pass one numbered file with `sequence: true` (or import the folder); a gap holds the previous frame; keep media next to the project (relative paths resolve against the project folder on open).
- Query `list_fonts`/`text.fonts` first; extra fonts come from `EFFECTCRAFT_FONT_DIRS`.

### Inspect and repair project files

- `.ecproj` is documented by the code: `savedBy`, `schema`, `activeComp`, `openComps`, `settings`, `items`, `nextId`, `renderQueue`. Item, layer and property ids share one counter; keep `nextId` above every id. Never bump `schema`.
- Prefer commands over JSON surgery; after a hand edit, reopen and check the `repaired` list in `file.open`'s result.
- For moved media: `footage.missing`, `footage.relink {item, path}` or `file.relinkFootage {folder, dryRun}`.
- `layer.revealSource` is the safe way to find a layer's Project item in the UI.

### Scripting

- Scripts run against the AE object model; `run_script`/`script` keep edits (wrap in `app.beginUndoGroup()`/`endUndoGroup()`). The CLI `script` exits 1 with `file:line:col`.
- Reads are allowed under the script's own folder and the project folder; writes and network require Settings ▸ Scripting & Expressions.
- Setting an array property to the wrong length throws `Array is not of the correct dimension` — pad or trim arrays in generated scripts.
- A Text animator is addressed by index (**counting from 1**) or by uid, and a uid wins over an index.

### Replay a bug or a crash

- `journal.export` returns the commands run since the project was opened; `help.exportRepro` writes the same to `Repros/` (or a path you give inside a write root). A crash writes `Repros/crash-<time>-<command>.jsonl` automatically.
- A script's steps are `{"command", "params"}`, `{"expect": {"query", "params"?, "pointer"?, "equals"?}}`, `{"expect_error": …}` and `{"expect_no_error": true}`, under an optional first `{"start": "new"|"demo"|{"project": path}}`.
- `effectcraft-cli replay SCRIPT.jsonl` reports each step and exits 1 on the first failure; `--keep-going` continues. Use it to turn a user's bug into a regression test (`tests/repros/`), not to drive production work.
- Read a repro before sharing it: parameters can contain file paths, layer names and text.

### Extensions (plug-ins, helpers, library)

- Loading a WebAssembly plug-in or a helper **executes third-party code**. Do it only when the user asked for that plug-in, prefer the Plug-in Library's catalog (SHA-256 checked) over an arbitrary path, and never install into an app another process is using.
- A helper that crashes or times out shows an error on the effect and is turned off after three failures; `effect.helpers.scan {"retry": true}` re-enables it.
- See `references/extensions.md` for the ABIs, the commands, the sandbox limits and what an agent must not do.

### Verify exports

- Read the result: `renderQueue.render` returns per-item statuses; CLI `render` exits 1 if any item failed.
- Re-import the output and render a frame to prove it decodes; use `--transparent` for alpha.
- Lottie: inspect `warnings`; timeline: inspect `warnings`, `missing` and `prerendered`; `.aep`: inspect `report`.
- Odd comp sizes: H.264/HEVC dimensions round down to even. EXR lossy methods (`pxr24` on float, `b44`/`b44a` on half, `dwaa`/`dwab`) change samples — check the compression when a comparison must be exact.

### Do not

- Assume an `.aep` will round-trip unchanged, or that `.ffx`/`.mogrt`/`.aex`/`.prproj` open at all.
- Drive the GUI without `--control` (discover widgets with `ui.elements`), edit a `.ecproj` the app has open, or expose the control port (no authentication).

### Concurrency and safety

- Save early; `open_project`/`file.newProject` replaces a dirty project without a prompt. Without `--autosave`, MCP work is memory-only.
- Concurrent `--save` CLI runs are serialised by a lock file beside the project, so the last writer wins in order rather than losing an edit — but a lock file is not a merge: do not edit one project from two agents.
- After a broken bridge connection, mutating calls have an **unknown outcome**; inspect before retrying.
- Scripts may read files only in their own or the project's folder; confine agent file access with `--automation-read-root` / `--automation-write-root`.

## Verification protocol

Alpha-software discipline; run this for every delegated task.

1. **Copy first.** Work on a scratch `.ecproj` (`--save-as` / Save a Copy), never the only copy; update the app only between projects.
2. **Round-trip in a fresh process.** New → comp/layers/keyframes/effects → save → reopen via `info --project` → render a frame and a short movie.
3. **Check both artifacts.** A `render-frame` PNG at a known time and the final MP4/MOV/sequence; confirm dimensions, duration, audio and alpha against version 0.24.1's behaviour.
4. **Check the time span.** Queued items default to **Work Area**; CLI `render` defaults to the whole comp unless `--work-area`.
5. **Check format constraints.** H.264/HEVC even dimensions; ProRes 4444 for alpha; WebM VP9 for VP9 alpha; WAV/AIFF are 16-bit PCM; EXR defaults to ZIP at 32-bit float, and any lossy compression method must be named deliberately.
6. **After Effects interchange:** `file.importAep` with `dryRun: true` first, then a real import, render one frame of each imported comp, and finally `file.exportAep {dryRun: true}` to see what the writer would drop. A clean report is not a render match.
7. **Interchange and Lottie:** inspect warnings/missing/prerendered, re-import the result.
8. **Keep the repro.** If a step fails, export `journal.export` (or use the crash file) and replay it before changing anything; that script is the reproducible statement of the bug.
9. **Report, don't hide.** Give the exact command, version, file and observed result. Fidelity differences against After Effects are expected and are the most useful report.

## Sources & evidence

- Repository: `https://github.com/storytold/effectcraft`; inspected tag `v0.24.1`, commit `582344dd4ef462362c02e56e3094de7af01847ab` (`git rev-parse HEAD` and `git describe --tags`, 2026-11-12); the `v0.22.0` tree (`42e3c6a6c119d973aa59ab0437487ea6cae6a15d`) was extracted read-only with `git archive` for set and count diffs. Fast-moving alpha — verify against your installed version.
- Installed app at this pin: `EffectCraft.app` — version **0.24.1**, bundle id `ai.storyteller.effectcraft`; `Contents/MacOS` holds only the app binary (no CLI), and the recorded `--version` string for this bundle is `effectcraft 0.24.1`. **No GUI was launched and the app binary was not executed** in this audit; only `Info.plist` and the repo were read. No `effectcraft-cli` binary is installed, so no CLI count was executed.
- Read: `README.md`, `Cargo.toml`, `docs/` (`agents`, `mcp`, `control-protocol`, `architecture`, `file-format-parity`, `gaps`, `effects`, `effects-parity`, `feature-naming`, `fidelity/README`, `footage`, `plugins`, `publishing-plugins`, `external-helpers`, `scripting-parity`, `aep-import`, `aep-export`, `aep-format`, `preferences`, `web`); `crates/aep/` (container incl. `effect_map`, import incl. `lumetri`/`puppet`/`report`, export); `crates/engine/src/{cmd.rs,replay.rs,cmd/journal.rs,cmd/aep.rs,cmd/layer.rs,cmd/layer/timing.rs,cmd/file.rs,cmd/batch.rs,cmd/content_fill.rs,cmd/query.rs,analysis/models.rs,settings/prefs/sections.rs,system/library.rs}`; `apps/effectcraft-cli/src/{main,project_lock}.rs`; `apps/effectcraft/src/{main,control_server,crash_report,diagnostic_state}.rs`; `crates/project/src/{lib,render_queue,styles,limits,footage,sequence,layer,settings,props}.rs`; `crates/media/src/lib.rs` (the format lists); `crates/{interchange,lottie,expr,automation,plugin,helper-host}/src`; `crates/effects/src/{lib,catalog,plugin,display_names}.rs`; `crates/plugin/src/{lib,wasm}.rs`; `crates/color/src/blend.rs`; `crates/export/src/{exr_out,pipeline}.rs`; `crates/gpu/src/upload.rs`; `crates/render/src/disk_cache/entry_files.rs`; `crates/ui-egui/src/{control,dock,i18n.rs,i18n/ui.rs,menus/commands.rs,menus/frontend.rs,app/frame.rs,panels/unprecompose.rs}`. No build, test or render was run.
- Counting method (repeated in `evidence.md`): engine ids are the unique first string arguments of `cmd!`/`query!` registry invocations under `crates/` and `apps/` (test trees excluded, multi-segment ids matched whole) — 703 macro sites / 698 ids at v0.24.1, 702 / 697 at v0.22.0 — plus the ids built outside those macros (3 literal `CommandSpec` values at both tags, and `journal.export`/`help.exportRepro` from `journal.rs`'s `spec()` helper at v0.24.1), giving **703** vs 700. Effects and parameters come from the generated, test-enforced `docs/effects.md`; the other sets are the literal arrays and match arms named in the table above.
