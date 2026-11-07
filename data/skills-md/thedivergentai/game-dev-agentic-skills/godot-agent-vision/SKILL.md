---
name: godot-agent-vision
description: "Agentic eyes for Godot work: cross-platform screenshot CLI (asset/region/window/screen) to budgeted WebP, TEMP editor viewport bridge under .gdskills/, and Taste Receptor Atlas v2 (~237 micro-receptors × 0–2: hierarchy, contrast, typography×41, affordance, space, color, icon, composition, light/FX, motion-tells, anti-slop, originality, identity). Use when agents must see UI, assets, or the editor — not for in-game screenshot Autoloads. Keywords: agent vision, screenshot, WebP, visual QA, taste receptors, typography, UI review, asset sheet, editor viewport, anti-slop."
---

# Godot Agent Vision

Host-side **eyes** for coding agents building Godot projects: capture → budgeted WebP → **scored** visual review. Not a game Autoload, not an exportable screenshot API.

> **Do NOT Load** every reference for one task. Load the MANDATORY file for the active mode, then only the rubric axes you are scoring.

## NEVER Do

- **NEVER ship the editor bridge as an Autoload** or leave `addons/_gdskills_agent_vision/` committed — stage, capture, teardown.
- **NEVER leave `--keep-bridge` on** after debugging — skips teardown and dirties the consumer project.
- **NEVER dump uncompressed PNG walls into model context** — WebP only; default **short-edge 512**; `--detail` only when pixels fail (especially type).
- **NEVER replace scored taste with binary PASS/FAIL or vibes** — score applicable rows in [taste-receptors.md](references/taste-receptors.md) (Atlas v2, **237** receptors × 0–2); V1–V8 /120 in [vision-review-rubric.md](references/vision-review-rubric.md) is rollup only.
- **NEVER invent taste** without loading Family deep refs when those pixels are present: TYPE → [typography-sight.md](references/typography-sight.md); HIER/CTRST → [hier-contrast-receptors.md](references/hier-contrast-receptors.md); SPACE/AFF → [space-affordance-receptors.md](references/space-affordance-receptors.md); COLOR/ICON → [color-icon-receptors.md](references/color-icon-receptors.md); COMP/LIGHT/MOT → [composition-fx-receptors.md](references/composition-fx-receptors.md); plus [anti-slop-sight.md](references/anti-slop-sight.md) / [ui-taste-sight.md](references/ui-taste-sight.md).
- **NEVER treat purple-gradient / glow-card / cream-serif AI defaults as “good UI”** unless the capture owns that identity with legible critical info and type discipline (`SLOP-STACK` / `TYPE-DISPLAY-HUD-SPLIT`).
- **NEVER put ornate display faces on ammo/HP/timers** — `TYPE-DISPLAY-HUD-SPLIT` ship blocker; data type is boring on purpose.
- **NEVER promise silent window-by-title on Wayland** — region, `grim`, X11, or editor bridge.
- **NEVER trust black fullscreen BitBlt/mss frames** — exclusive fullscreen / some GPU paths return empty; windowed, region, DXGI-only if justified, or editor bridge.
- **NEVER commit `.gdskills/vision/**`** — ensure `.gdskills/` is gitignored first.

## When to use

| Need | Mode | MANDATORY loads |
|------|------|-----------------|
| Asset files / sheets | `asset` | [capture-modes.md](references/capture-modes.md), [webp-budgets.md](references/webp-budgets.md), rubric V6–V8 + [originality-sight.md](references/originality-sight.md) |
| Desktop rectangle | `region` | capture-modes + budgets + rubric axes in frame |
| Godot/editor/game window | `window --title` | capture-modes (OS limits!) |
| Full monitor | `screen` | last resort (secret chrome) |
| Editor 2D/3D pixels | `editor` | [editor-bridge-lifecycle.md](references/editor-bridge-lifecycle.md) |

After capture: **Read** WebP(s) → score **Taste Receptor Atlas** (not vibes) → zero-list + ordered fixes keyed to receptor IDs. If any **TYPE-*** / micro-seam ≤1 for illegibility at 512 short-edge, re-capture `--detail` or text crop before locking.

## Setup (agent host)

```text
pip install -r skills/godot-agent-vision/requirements-vision.txt
# optional macOS window titles:
# pip install pyobjc-framework-Quartz
```

Requires a display session. Use repo/project venv Python.

## Available Scripts

> **Do NOT Load** every script. Call only what the mode needs.

### [capture.py](scripts/capture.py)
Main CLI: `doctor`, `list-windows`, `screen`, `region`, `window`, `asset`, `editor`. Prints `wrote=`, `bytes=`, `budget=short-edge:N|long-edge:N`.

### [webp_encode.py](scripts/webp_encode.py)
Default **fit short-edge 512**; `--detail` / `--max-edge` switches to long-edge cap (1568). Never upscales. Soft re-encode if &gt;1MB.

### [asset_sheet.py](scripts/asset_sheet.py)
Single asset or ≤2×2 contact sheet with labels; `res://` resolution against `--project-root`.

### [ensure_gitignore.py](scripts/ensure_gitignore.py)
Appends `.gdskills/` so vision scratch never stages.

### [stage_editor_bridge.py](scripts/stage_editor_bridge.py)
Stages TEMP addon, optional `--godot` launch, handshake wait, WebP encode, teardown + `project.godot` plugin strip.

### Editor bridge templates
- [plugin.cfg](scripts/editor_bridge/plugin.cfg) / [plugin.gd](scripts/editor_bridge/plugin.gd) — `@tool` EditorPlugin polls `request` → `raw/*.png` → `done`
- [capture_viewport.gd](scripts/editor_bridge/capture_viewport.gd) — Control crop helper (`get_global_rect` → `Image.get_region`)

## Capture CLI (golden path)

```text
python skills/godot-agent-vision/scripts/capture.py doctor
python skills/godot-agent-vision/scripts/capture.py window --project-root . --title Godot
python skills/godot-agent-vision/scripts/capture.py asset --project-root . --paths res://ui/icons --sheet
python skills/godot-agent-vision/scripts/capture.py editor --project-root . --editor-mode 3d --godot "%GODOT_PATH%"
# typography / OCR / dense layout only:
python skills/godot-agent-vision/scripts/capture.py window --project-root . --title Godot --detail
```

Default out: `{project}/.gdskills/vision/YYYYMMDD-HHMMSS-<mode>[-label].webp`

**MANDATORY** platform landmines: [capture-modes.md](references/capture-modes.md). **MANDATORY** budgets: [webp-budgets.md](references/webp-budgets.md).

## Editor bridge (TEMP)

Stages templates → `addons/_gdskills_agent_vision/` → `.gdskills/vision/{request,raw,done}` → WebP → **delete addon** + restore `enabled=`.

**MANDATORY:** [editor-bridge-lifecycle.md](references/editor-bridge-lifecycle.md). Prefer EditorPlugin over EditorScript (`await` across RefCounted is unsafe).

## Structured review (Taste Receptor Atlas → optional /120)

**MANDATORY primary:** [taste-receptors.md](references/taste-receptors.md) — **237** micro-receptors across 13 families (HIER, CTRST, TYPE×41, AFF, SPACE, COLOR, ICON, COMP, LIGHT, MOT, SLOP, ORIG, ID), each **0/1/2**, grade by % of applicable, hard gates. Routing + V-rollup: [vision-review-rubric.md](references/vision-review-rubric.md).

| When scoring… | Load |
|---------------|------|
| Any review | **MANDATORY** [taste-receptors.md](references/taste-receptors.md) |
| TYPE-* / HUD numerals / menus | **MANDATORY** [typography-sight.md](references/typography-sight.md) |
| HIER-* / CTRST-* | [hier-contrast-receptors.md](references/hier-contrast-receptors.md) |
| SPACE-* / AFF-* | [space-affordance-receptors.md](references/space-affordance-receptors.md) |
| COLOR-* / ICON-* | [color-icon-receptors.md](references/color-icon-receptors.md) |
| COMP-* / LIGHT-* / MOT-* | [composition-fx-receptors.md](references/composition-fx-receptors.md) |
| SLOP-* / UI cross-check | [anti-slop-sight.md](references/anti-slop-sight.md), [ui-taste-sight.md](references/ui-taste-sight.md) |
| ORIG-* | [originality-sight.md](references/originality-sight.md) |
| ID-* | [identity-sight.md](references/identity-sight.md) |

## Expert Knowledge Delta

### Capture / OS
- Windows: **Per-Monitor DPI V2 before geometry**; `mss` before DPI-clobbering imports; `monitors[0]` virtual union can be negative-origin; longest title match for Godot’s path-in-title windows.
- Windows black frames: minimized / exclusive fullscreen / GPU-protected content — not “empty UI.” Prefer windowed + region or editor bridge; DXGI is optional weight, not default.
- macOS: Screen Recording attaches to **responsible binary**; wallpaper-only = hard fail; `screencapture` CLI attribution breaks under agents — prefer in-process Quartz/mss.
- macOS Retina: pick **logical points** (automation) vs **backing pixels** (OCR) and do not mix without scale metadata.
- Linux: Wayland → skip mss; `grim` on wlroots; **no silent title grab**; portal paths are interactive.
- Asset `res://` resolves against `--project-root`; missing paths must error loudly — never invent files.

### WebP / context
- Vision tokens track **pixel area**; request size tracks codec. Default **short-edge 512** for identity/overview/anti-slop; escalate long-edge **1568** only for glyphs, seams, dense full-layout.
- Contact sheets **≤2×2** with gutters — 3×3+ makes panel text sub-pixel after model downscale.
- Never upscale tiny icons to fill 512/1568 — wastes tokens without information.

### Editor bridge
- EditorPlugin (Node) can `await RenderingServer.frame_post_draw` safely; EditorScript is RefCounted and can free mid-await.
- Capture: `EditorInterface.get_editor_viewport_2d/3d` → `get_texture().get_image()` after **≥1–2** frame waits; set main screen `2D`/`3D` first or texture is stale/empty.
- Empty `get_image()` ⇒ missing await or wrong main screen — not proof the GPU is fine.
- Handshake: write PNG under `raw/`, **then** `done` flag; Python waits for size-stable PNG.
- Teardown must strip `res://addons/_gdskills_agent_vision/plugin.cfg` from `[editor_plugins] enabled=` and delete the addon — underscore name signals private/temp.
- Control crops: full editor image + `get_global_rect` → `Image.get_region`, clamped to bounds.

### Sight / taste (why the atlas is heavy)
- Score **receptors**, not vibes: hierarchy is composite **size×contrast×motion×sat** (`HIER-WEIGHT-MATH`); peripheral HUD must read as shape (`HIER-PERIPH-READ`); contrast is **worst-case** on plates (`CTRST-GRAD-WORST`, `CTRST-BODY-45`).
- Agents default to AI UI centroids (purple wash, neon glow cards, cream+serif, Lucide soup). **T≥3** without ownership ⇒ `SLOP-STACK=0` / overall **F**.
- **Typography is ship-blocking (41 TYPE receptors):** `TYPE-DISPLAY-HUD-SPLIT`, `TYPE-OPSZ-MATCH`, `TYPE-NUM-TABULAR`/`TIMER-STABLE`, `TYPE-GLYPH-INTEGRITY`, `TYPE-FACE-CAP` — display cuts at HUD size and tabular wobble are zeroes, not “style.”
- Color/icon: 4–6 semantic roles + accent budget ~5–15%; silhouette test on icon sets; CVD shape backup (`COLOR-ONLY` / `ICON-SIL`).
- Composition/FX/motion: power-point vs HUD conflict (`COMP-POWER-CONFLICT`); bloom/particles must not replace hierarchy or occlude UI; freeze-frames leak shake/tween artifacts (`MOT-*`) — sequence capture when peak ambiguous.
- Originality: filter scènes à faire first; fail franchise silhouette/mark matches and stacked construction tells.
- Identity: palette roles + edge grammar + motif recurrence (2–4) + type pairing + icon grid + HUD↔menu↔key-art DNA — gradient-alone is not a brand.

## Decision tree

1. Files on disk? → `asset` (± sheet) → Read → score COLOR/ICON/ORIG/ID/SLOP (+ TYPE if labels) → fixes.
2. Known window? → `window` (else `region`) → Read → score all applicable atlas families → fixes.
3. Editor viewport fidelity? → `editor` → teardown → score → fixes.
4. Else `screen` (last resort).
5. TYPE/CTRST illegible at 512? → `--detail` or text crop → re-score those receptors.
6. MOT/hit-peak ambiguous? → 2–8 frame sequence → re-score MOT/LIGHT hit receptors.

## Reference

> Progressive disclosure: open Official Documentation only for a specific API; load Related Skills when routing to a peer domain — do not preload the whole lattice.

### Official Documentation
- [EditorPlugin](https://docs.godotengine.org/en/stable/classes/class_editorplugin.html) — TEMP bridge host; enable/disable lifecycle.
- [EditorInterface](https://docs.godotengine.org/en/stable/classes/class_editorinterface.html) — `get_editor_viewport_2d/3d`, main screen switch before grab.
- [Using Viewports](https://docs.godotengine.org/en/stable/tutorials/rendering/viewports.html) — viewport textures feeding `Image` captures.
- [Image](https://docs.godotengine.org/en/stable/classes/class_image.html) — `save_png`, `get_region` for Control crops.
- [SubViewport](https://docs.godotengine.org/en/stable/classes/class_subviewport.html) — editor/game nested view surfaces.
- [RenderingServer](https://docs.godotengine.org/en/stable/classes/class_renderingserver.html) — `frame_post_draw` wait before texture readback.
- Migration hops: [migration-notes.md](references/migration-notes.md)

### Related Skills

#### Prerequisites
- [godot-project-foundations](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-project-foundations/SKILL.md) — project root / `.gitignore` hygiene before vision scratch.
- [godot-ui-containers](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-ui-containers/SKILL.md) — layout must be honest before vision blames Theme.

#### Complements
- [godot-ui-theming](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-ui-theming/SKILL.md) — Theme/StyleBox/font APIs after V3/V8 finds chrome/type debt.
- [godot-ui-rich-text](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-ui-rich-text/SKILL.md) — BBCode/fonts that must stay coherent with HUD type roles.
- [godot-auditor](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-auditor/SKILL.md) — architectural anti-slop kinship.
- [godot-debugging-profiling](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-debugging-profiling/SKILL.md) — runtime/orphan issues beyond pixels.
- [godot-builder](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-builder/SKILL.md) — CLI/`GODOT_PATH` patterns when launching editor for bridge captures.

#### Downstream / consumers
- Genre and UI skills that ship screens — route here when agents must **see** results, not guess.

#### Master
- [godot-master](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-master/SKILL.md) — Decision matrix row **Agent Eyes / Visual QA**.
