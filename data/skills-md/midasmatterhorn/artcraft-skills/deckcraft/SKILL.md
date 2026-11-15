---
name: deckcraft
description: >-
  DeckCraft is the ArtCraft open-source, clean-room PowerPoint-compatible presentation app for
  macOS (also Windows, Linux, FreeBSD and the web): slides, masters and layouts, shapes, 3-D,
  text, tables, charts, SmartArt, media, transitions, animations, slide shows, and `.deckcraft`,
  `.pptx`/`.potx`/`.ppsx`, outline text, Markdown and `.rtf`, PDF/PNG/JPEG/GIF files — driven by 329
  scriptable commands, a 12-subcommand CLI, a JSON control channel, a 25-tool MCP server and, in
  the web build, a `window.deckcraft` page API. Trigger this skill whenever the user mentions
  DeckCraft, `.deckcraft`, `deckcraft-cli`, asks what DeckCraft can or cannot do, which formats or
  shortcuts it supports, wants to build, edit, inspect, convert, render, present, export, verify,
  repair or troubleshoot a deck, wants assets prepared for it, or wants it automated or scripted —
  even if the app is not named but the job is presentation work ("make a deck", "turn this outline
  into slides", "export these slides to PDF", "why did my PPTX lose its animations?", "drive a
  presentation app with an agent"). Do not use it for Microsoft PowerPoint itself.
---

**Audit basis.** Refreshed 2026-11-12 against tag **v0.18.1**, commit **`7cc73ab1895ed2e30c8afbcada20c70b9ea0a440`** — `git rev-parse HEAD` in the pinned checkout confirms it, and the installed DeckCraft bundle matches (its binary prints `deckcraft 0.18.1`). The previous release this skill described was **v0.16.0** (`a3e2254d3de32ed1718f156f070b54a34b949b54`); v0.17.0 and v0.18.0 lie in between, so the delta below covers all three.

**v0.16.0 → v0.18.1 delta.** 121 files changed (+2 939/−7 950) between the two tags; the checkout is squashed at each tag, so the diff — not the commit list — is the evidence. **No registry moved:** 329 command ids (234 ordinary / 57 `noundo` / 38 `query`), 57 engine shortcuts, 52 UI commands, 12 CLI subcommands, 25 control methods (+2 aliases), 25 MCP tools, and every transition, animation, theme, layout, shape-preset, chart, SmartArt, starter, icon and warp set are identical id-for-id at both tags (counts below, re-measured at this tag). The wave is **media-crate consolidation, a web page API, and PPTX/robustness fixes**: the in-tree `opus`, `ogg`, `isobmff` and `matroska` crates are gone (workspace 24 → **20 crates**) and Opus/Ogg/MP4/MOV/Matroska now come from `craft-media`/`craft-audio` in craft-libs (`Cargo.toml`, `crates/media/Cargo.toml`, `docs/architecture.md`); the web build installs **`window.deckcraft`**, a promise-based page API over the control channel with `request`/`execute`/`commands`/`docInspect`/`uiInspect`/`screenshot` (`apps/deckcraft-web/src/api.rs`, `packaging/web/README.md`); an over-budget chart is now kept as its original part and written back whole (`Chart.verbatim`, `crates/pptx/src/read/chart.rs`) under presentation-wide budgets of 4 000 000 points and 256 MiB of chart decode; 3-D scene/extrusion XML on text bodies and groups is preserved (`crates/model/src/text.rs`, `crates/pptx/src/read/dml.rs`); SmartArt whose diagram has no parent-child connections keeps its node text (`crates/pptx/src/dgm.rs`); `shape.adjust`/`shape.quickStyle` reject a negative or fractional index (`crates/engine/src/cmd/shape/appearance.rs`); `format.paragraph` rejects an unknown `align` instead of silently left-aligning and accepts `centre`/`justifyLow` (`crates/engine/src/cmd/format/paragraph.rs`); `shape.lock` applies a group-and-child pair once (`crates/engine/src/cmd/shape.rs`); reopening a photo album seeds within the album limits and an album too large for the editor is refused instead of truncated (`crates/engine/src/cmd/insert/album.rs`); sentence case no longer capitalises after a decimal point (`crates/model/src/edit.rs`); MCP `batch` and JSON-RPC batches cap at 1 000 entries and 64 MiB of results (`crates/mcp/src/{tools,server}.rs`); the UI caps live video decoders at 16 (`crates/ui-egui/src/media.rs`); undo memory accounting now includes notes, comments and tags (`crates/engine/src/lib.rs`); and a ready update now installs at exit, with the Flatpak manifests granting the updater host access (`crates/ui-egui/src/dialogs/updates_ui.rs`, `apps/deckcraft/src/main.rs`, `packaging/linux/flatpak/`).

**v0.15.0 → v0.16.0 delta.** 144 files changed (+6 733/−717) between the two tags (carried from that round's audit — this checkout no longer carries the `v0.15.0` tag, so the range cannot be re-diffed here). No id set moved; the wave was PPTX fidelity plus validation: `file.save` began refusing `.png`/`.jpg`/`.jpeg` ("use file.export"), handout `perPage` became exactly 1/2/3/4/6/9, `view.slideMaster` and table `cells`/`comment.next`/`comment.prev` gained strict validation, `shape.flip` was refused on SmartArt, `shape.connect` reached grouped shapes, deleting a slide pruned custom shows, `slide.reuse` scaled content to the destination size and brought custom table styles, outlines omitted footer/date/slide-number placeholders, the PDF text layer used evaluated fields, the native manifest was capped at 256 MiB with a hidden `.deckcraft.<pid>.<n>.saving` sibling, PPTX round-trips gained overflow/spacing/`normalizeH`/`thaiDist`/point bullets/RTL/`altLang`/reflections, the system clipboard returned, Transition Preview started from the previous slide, See All Slides opened in the presenter window, and the web `?host=parent` bridge landed (`crates/engine/src/cmd/file.rs`, `crates/pptx/`, `crates/ui-egui/src/show.rs`, `apps/deckcraft-web/src/host.rs`).

**v0.14.1 → v0.15.0 delta.** 52 files changed (carried from that round's audit; neither tag is present in this checkout). The command-id set was unchanged at **329 ids, 329 `cmd!` sites** (an earlier note's "234 ids" was the ordinary-kind subset). Wave: the WASM presenter view opening in a separate browser window, H.264 temporal direct motion-vector scaling, PPTX tags parts parsed once with a cap on copied tags, and resizing allowed on all selected shapes. craft-libs was pinned at `c5a1cbfb…`, which v0.16.0 kept while adding `2e2312dd…` for the web app.

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may differ; every count quoted here was re-measured at this tag on 2026-11-12, and code paths that moved were re-cited. The measurement method for each count is in `evidence.md`.

## Overview

DeckCraft is a clean-room, open-source (MIT OR Apache-2.0), pure-Rust presentation application targeting Microsoft PowerPoint for Mac parity — and better speed, openness and agent control (README.md; AGENTS.md; `Cargo.toml`). It builds decks with masters, eleven layouts, eight original themes, shapes, text, tables, charts, SmartArt, audio and video; presents them full screen or in a window with transitions and animations; and exchanges PowerPoint `.pptx` plus its own `.deckcraft` (README.md §"What works today"). It is **alpha**: the parity docs still claim **84% feature breadth** (P0 92%, P1 82%, P2 55%) and **~55% ready for real work**, both by the project's own measurement (ROADMAP.md; `docs/target-app-parity.md`; `docs/parity-checklist.md`). The workspace is **20 crates plus three apps** (`apps/deckcraft`, `apps/deckcraft-cli`, `apps/deckcraft-web`) on Rust edition 2024 (`Cargo.toml`); video decoders and `bitstream` stay in-tree, while the Opus decoder and the Ogg/MP4/MOV/Matroska demuxers come from craft-libs (`crates/media/Cargo.toml`). The UI runs on egui 0.37 with craft-ui's shared widgets. Source: GitHub `storytold/deckcraft`.

Everything user-visible is a **command with an id**, and `Session::execute` is the single dispatch path shared by the ribbon, keyboard, CLI, control channel and MCP (`crates/engine/src/lib.rs`; `crates/engine/src/cmd.rs`).

## Capabilities (verified)

### Automation surface at a glance

| Surface | At v0.18.1 | Change vs the v0.16.0 skill |
|---|---|---|
| Engine commands (`CommandSpec`) | **329**, ids unique (234 ordinary / 57 `noundo` / 38 `query`) | unchanged at v0.18.1 |
| Engine shortcuts | **57** commands (56 distinct strings; one real collision, `Cmd+Shift+V`) | unchanged at v0.18.1 |
| UI-only commands (`UI_COMMANDS`) | **52**, 15 with shortcuts | unchanged at v0.18.1 |
| CLI subcommands | **12** (`info render render-transition convert run commands describe app mcp bench links version`) | unchanged at v0.18.1 |
| Control-channel methods | **25** canonical, plus the aliases `ui.menu.invoke` and `command` (27 accepted strings) | unchanged at v0.18.1 |
| MCP tools | **25**, plus resources `deckcraft://document`, `deckcraft://commands` | unchanged at v0.18.1 (batch caps added) |
| Web page API | `window.deckcraft`: `request`, `execute`, `commands`, `docInspect`, `uiInspect`, `screenshot` | **new at v0.18.1** |
| Transitions | **49** rows (48 + `none`) | unchanged at v0.18.1 |
| Animations | **107** entries (24 entrance, 17 emphasis, 23 exit, 40 motion-path incl. `customPath`, 3 media) | unchanged at v0.18.1 |
| Themes / layouts / shape presets | **8** themes × 4 colour variants / **11** layouts + `Custom` / **183** presets in 9 categories | unchanged at v0.18.1 |
| Charts / SmartArt / starters / icons / text warps | **28** chart types (7 `chartEx` + `RegionMap`) / **45** layouts, 9 styles, 17 colour sets / **6** starter decks / **70** Lucide 1.56.0 icons / **40** warps | unchanged at v0.18.1 |
| Pattern fills | **48**-preset gallery (54 DrawingML names known) | unchanged at v0.18.1 |
| 3-D presets | **28** cameras offered (62 known), 12 bevels, 12 materials, 15 light rigs | unchanged at v0.18.1 |
| UI languages | **1** — English only, no string catalogue | unchanged at v0.18.1 |

Every count was re-derived from this tag's code on 2026-11-12, never copied: commands from the `cmd!(` sites in `crates/engine/src/cmd/` (329 sites, 329 unique ids; command-id sets diffed between `v0.16.0` and `HEAD` — nothing added, nothing removed), shortcuts and their collision from the `cmd!` shortcut arguments, control methods from the `match req.method` arms in `crates/ui-egui/src/control.rs`, MCP tools from `crates/mcp/src/tools.rs`, UI commands from `UI_COMMANDS` in `crates/ui-egui/src/lib.rs`, CLI from `apps/deckcraft-cli/src/help.rs::SUBCOMMANDS`, transitions and animations from `TRANSITIONS`/`ANIMATIONS` in `crates/model/src/anim.rs`, shape presets from `CATALOG` in `crates/geom/src/preset/catalog.rs`, warps from `CATALOG` in `crates/geom/src/warp.rs`, patterns from `PATTERN_GALLERY`/`PATTERN_LABELS` in `crates/ui-egui/src/panels/fillui.rs`, and the rest from their registries (`crates/model/src/theme.rs`, `crates/model/src/chart.rs`, `crates/engine/src/cmd/smartart.rs`, `crates/engine/src/templates.rs`, `crates/engine/src/icon_data.rs`, `crates/engine/src/cmd/three_d.rs`, `crates/engine/src/cmd/insert/text_fields.rs`). Languages: no `locales/` directory, no i18n crate, no string catalogue in the workspace.

The MCP surface is 25 tools: `list_commands`, `run_command`, `batch`, `new_presentation`, `open_presentation`, `save_presentation`, `export`, `inspect_document`, `inspect_slide`, `render_slide`, `add_slide`, `go_to_slide`, `add_shape`, `add_text_box`, `set_text`, `insert_picture`, `insert_table`, `insert_chart`, `select`, `pointer`, `select_tool`, `key`, `type_text`, `screenshot` and `call_app` (the last two connected-mode only; full table in `references/commands-and-formats.md`). `batch` now refuses more than **1 000 commands** and stops once its gathered results pass **64 MiB** (`crates/mcp/src/tools.rs`); the JSON-RPC batch handler has the same caps (`crates/mcp/src/server.rs`).

### Deck structure and design
- **Slides, masters and layouts.** Eleven standard layouts plus `Custom` (`LayoutType`, `crates/model/src/lib.rs`). Slide/notes/handout masters, placeholder inheritance, sections, notes, comments, headers/footers, custom shows and slide sizes are modelled; **deleting a slide prunes it from every custom show**, undoably (`crates/engine/src/cmd/slide.rs`).
- **Themes.** Eight original themes — DeckCraft, Harbor, Ember, Meadow, Nocturne, Paper, Coral Reef, Slate — with colour, font and effect schemes and four colour variants (`builtin_themes`, `theme_variants` in `crates/model/src/theme.rs`). Design ▸ Browse for Themes imports `.thmx`, `.pptx` or `.potx`.
- **Starter decks.** Six originals — Briefing, Lesson, Pitch, Field Notes, Quarterly, Evening Talk — via `file.new {template}` / `file.templates`.
- **Shapes.** 183 preset shape/connector generators in 9 gallery categories (`crates/geom/src/preset/catalog.rs`), with adjust handles, glued connectors, freeform/curve/scribble, ink-to-shape, merge operations, gradient/picture/pattern fills, dashes, arrowheads, shadows, glow, soft edges and reflections. **`shape.connect` glues to a shape inside a group** and an unknown id is an error; **`shape.flip` is refused on a SmartArt graphic**; **Merge Shapes drops the merged shapes' animations and clears triggers that pointed at them**; **`shape.adjust`/`shape.quickStyle` reject a negative or fractional `index`** (an index past 16/41 is still clamped), and **`shape.lock` applies a group+child pair once**.
- **3-D.** Format Shape ▸ 3-D Format/Rotation: 28 camera presets offered (62 known), 12 bevels, 12 materials, 15 light rigs, X/Y/Z rotation, depth and contour (`crates/engine/src/cmd/three_d.rs`); `a:scene3d`/`a:sp3d` stay as raw XML and round-trip, and at this tag so do **`a:scene3d`/`a:sp3d`/`a:flatTx` on a text body and `a:scene3d` on a group** (≤64 KiB, element names validated on write: `crates/model/src/text.rs`, `crates/pptx/src/write/dml.rs::valid_raw3d`). Rendering is approximate — see limitations.
- **Text.** In-place editing with DrawingML run/paragraph properties, bullets and numbering (**point-sized bullets are preserved** through native and PPTX saves), columns (1–16), autofit, vertical and RTL text, fields, hyperlinks, tab stops, line spacing, 40 WordArt warps, AutoFormat/Smart Quotes, and paragraph alignment including `thaiDist`. **`format.paragraph` now rejects an unknown `align` instead of silently left-aligning**, and accepts `centre`/`justifyLow` as synonyms (`crates/engine/src/cmd/format/paragraph.rs`); sentence case no longer capitalises the word after a decimal point (`crates/model/src/edit.rs`).
- **Tables.** Styled tables with cell merges (diagonal borders included), row/column insert, delete and distribute, widths/heights, borders, cell fill/margins/alignment, drag- or Shift+arrow range selection, draw/erase line; **centred cell anchoring, per-cell horizontal overflow and RTL column direction round-trip**. Cell commands take `cells: [[row, col], …]` — exactly two integers a cell, inside the table.

### Content
- **Pictures.** PNG, JPEG, GIF (animated, inside groups too), WebP, BMP, TIFF decode; EMF/WMF draw through `deckcraft-metafile`, including EMF+-only files. Crop, brightness/contrast, duotone, alpha, artistic effects, compress and Set Transparent Colour are modelled; **Compress Pictures measures grouped pictures at their displayed size**. Photo albums take at most **48 items, 32 MiB a picture and 64 MiB in all**; **reopening an album is seeded within those limits, and editing an album larger than the editor can carry is refused** rather than deleting the rest (`crates/engine/src/cmd/insert/album.rs`).
- **Charts.** 28 types including the seven Office-2016 `chartEx` types, plus radar, stock, region map and combo; chart text colour, palette, gridlines, data labels, bin options and six trendline kinds with forecast and equation/R². An unchanged chart keeps its embedded workbook; pattern fills read and write (`a:pattFill`). **Past 1 000 000 points a chart, or past 4 000 000 points/256 MiB of decode across the presentation, a chart is shown empty and its original part is written back whole (`Chart.verbatim`)** — its data is not modelled while it is in that state (`crates/pptx/src/read/chart.rs`, `crates/pptx/src/write/chart.rs`).
- **SmartArt.** A graphic is a group whose outline is edited in a Text Pane; 45 layouts, 9 styles, 17 colour sets, Add/Promote/Demote/Remove, layout switching, picture fill, convert to/from text or shapes; written to `.pptx` as a real diagram. **A diagram whose `dgm:dataModel` has no parent-child connections keeps its node text in `ptLst` order** instead of dropping it (`crates/pptx/src/dgm.rs`).
- **Media.** Audio: MP3, AAC/M4A, ALAC, WAV, AIFF, CAF, FLAC, Ogg Vorbis, Opus. Video: H.264, HEVC, VP9 and AV1 in MP4/MOV and WebM/Matroska, decoded in software. The video decoders are DeckCraft's own crates; the Opus decoder and the Ogg/MP4/MOV/Matroska demuxers are craft-audio/craft-media from craft-libs (`crates/media/Cargo.toml`, `Cargo.toml`). Trim, fades, volume, poster frame, show-media-controls and embedded 3-D model parts are modelled. At most **16 video decoders** are live at once in the editor/show; more videos play their sound without a picture and try again on their next play or seek (`crates/ui-egui/src/media.rs`).
- **Reuse Slides.** `slide.reuseList` lists the other file's slides, `slide.reuse` inserts the chosen ones; **reused geometry and text are scaled to the destination slide size**, and the source's custom table styles come along (reused slides fit the destination — picker thumbnails are still missing).
- **Other insertables.** 70 Lucide 1.56.0 stroke icons as custom shapes (`insert.icon`), WordArt, symbols, date/time fields (13 formats), slide numbers, photo albums (insert and edit), Zoom links, and an Equation dialog that inserts pretty-printed text, not OMML.

### Presenting
- **48 transitions plus "None"** (49 rows), including Morph with objects/words/characters options; **Preview plays the transition from the previous slide**, as PowerPoint does.
- **Animations.** 107 picker entries (24 entrance, 17 emphasis, 23 exit, 40 motion-path including Custom Path, 3 media controls); start modes, by-paragraph builds, click triggers, repeat, auto-reverse, bounce end and rewind; animation remove/move/timing/options reject invalid indexes.
- **Slide show.** Full-screen show or `browsed` (in a window), presenter view in a second window, pen and laser pointer, black/white screens, **See All Slides opening in the presenter window (G)**, zoom (Ctrl+wheel around the pointer), hyperlinks/actions, custom shows, kiosk looping, rehearse timings and media playback (`show.setup {type: speaker|browsed|kiosk}`).
- **Views.** Normal, Outline, Slide Sorter, Notes Page and Reading; slide/notes/handout master views; Animation Pane with Play From; grayscale view mode follows into the slide thumbnails.

### Files
- **Native `.deckcraft`:** a zip with a stored `mimetype`, `presentation.json`, `media/<id>` and `chart-parts/<index>` entries; readers ignore unknown fields, and legacy `.slidecraft` files still open. Load budgets: **256 MiB `presentation.json`**, 2 GiB per entry, 4 GiB total media + chart sidecars, 100 000 items; the notes page is clamped to the slide-size bounds. Kept 3-D body/group XML also round-trips here (`BodyProps.raw3d`).
- **PowerPoint `.pptx`:** read and write; `.potx` and `.ppsx` are written with their own main content types. Unknown parts are kept where the model does not understand them. Embedded TrueType/OpenType/EOT fonts are read, written and drawn; a MicroType Express subset is kept and written back but not drawn, so its text uses a stand-in. At this tag the writer also keeps text overflow (`vertOverflow`/`horzOverflow`, `anchorCtr`), `compatLnSpc`, normalised character height, Thai distributed alignment, RTL table direction, run `altLang`, reflection transforms, the show-media-controls flag, effects' parent time-node delays, and **3-D XML on text bodies and groups**.
- **Outlines:** plain text and Markdown (headings become slides) and `.rtf` — PowerPoint's Outline/RTF save type — imported by content sniffing and by extension, and exported with bold/italic/underline and outline levels; **footer, date and slide-number placeholders are left out**, as in PowerPoint's outline view.
- **PDF:** slides, notes pages or handouts (1/2/3/4/6/9), Letter/A4/Legal/A3, portrait/landscape, hidden-slide and slide-range options, selectable invisible text layer (**evaluated field values, so a slide number shows as its number**), web and mail links only, bookmarks; slide artwork is a raster image, at most 64M pixels per slide.
- **Images and GIF:** PNG/JPEG per slide (one, `slide`, or `all`; `transparentBackground`; DPI = scale × 72) and an animated GIF of the deck (one frame per slide, 256-colour palette, 16–3840 px wide, 0.1–600 s per slide, loop or play once, slide range incl. `"1-3,5"`, hidden slides skipped, ≤500 frames / ≤200M pixels).
- **AutoRecover:** unsaved presentations are written to a recovery folder and reopened at the next start; saving or closing removes the entry.

### Platforms
- **macOS universal app**, signed, notarized and stapled; Windows x64/arm64/x86 (the MSI declares `perUserOrMachine` scope, so the launcher decides per-user or machine-wide); Linux (AppImage, Flatpak, deb, rpm, tarball; riscv64 tarball), FreeBSD and a static WebAssembly site.
- Rendering is CPU-side through `vello_cpu`; the UI is egui 0.37/eframe. The web build uses WebGPU with a WebGL2 fallback (`?webgl`), starts blank or in show with `?blank`/`?show`, downloads instead of saving, has no audio output, no TCP control channel and no persisted preferences — unless a same-origin page frames it: **`?host=parent`** (+ `&author=`) sends the presentation to open and stores what it saves, and `data-host="page"` uses DOM events instead of an iframe. Every web build also installs **`window.deckcraft`** (craft-web-api), whose promise functions call the same control methods as the desktop server (`apps/deckcraft-web/src/api.rs`).
- **Desktop clipboard:** Ctrl+C/X/V use the **system** clipboard at this tag (v0.11.1–v0.15.0 only had an in-app clipboard).

## Known limitations and not-implemented

### File exchange and PowerPoint fidelity
- **No external deck corpus.** Every PPTX test uses decks this repo authors; fidelity on real corporate decks, templates, fonts and `chartex` is mostly unmeasured, and "opens in PowerPoint without repair" is a docs claim, not independently verified here.
- **Known PPTX round-trip losses:** media playback options (#74) are still lost — volume, autoplay, loop, rewind, play-across-slides, hide-while-not-playing and full-screen are model-only, while trim, fades, bookmarks and the document-level show-media-controls flag do round-trip; a combo chart's secondary value axis is read but not written when the chart is rebuilt; editing a chart's data drops its embedded workbook (an unchanged chart keeps it); imported SmartArt is redrawn with DeckCraft's simpler layouts; relationship-bearing SmartArt/OLE kept only as XML loses drawing and data parts (#203). Animation rewind **does** round-trip (`c:tn` `fill="remove"`).
- **Charts over budget are placeholders.** Past 1 000 000 points for one chart, or 4 000 000 points / 256 MiB of chart decode across the presentation, the chart shows empty and its original part is kept for writing back; chart commands have no series to edit in that state (`crates/pptx/src/read/chart.rs`, `crates/model/src/chart.rs::Chart.verbatim`).
- **Unsupported input:** legacy `.ppt`/`.pot`/`.pps`, OpenDocument `.odp` and `.pptm`/`.potm`/`.ppsm` are not read (macros are neither preserved nor run); password-protected decks fail with a clear error and there is no password protection on save.
- **A Finder-open `.ppsx` still does not start its show.** Only `open_from_system` (the command-line path) checks for `.ppsx`; the Apple-event path calls `open_path` without it (`crates/ui-egui/src/app/files.rs`, `apps/deckcraft/src/apple_events.rs`).
- **Internal docs still lag the code.** `docs/control-protocol.md` says a 16 MiB request line (code: 256 MiB); `docs/animation-parity.md` says 14 exit effects (code: 23); `docs/architecture.md` says 320 commands and 24 crates (code: 329 and 20); `docs/target-app-parity.md` says 328; `ROADMAP.md` says "226 commands"; `docs/mcp.md` omits the batch caps; and `format.align`'s parameter doc omits `thaiDist`. Trust the code and `deckcraft-cli commands`/`describe`.

### Pictures and media
- **SVG is not rendered.** `insert.picture` accepts `image/svg+xml`, but no decoder draws it, so an inserted SVG shows nothing and a PPTX that stores a PNG fallback beside its SVG shows that fallback.
- **HEIC is not supported**, WMA is recognised and probed but not decoded, WMV is not playable, and online video embeds are not supported. EMF/WMF render inside decks but are not sniffed by `insert.picture`.
- **Pasting a screenshot from another app is unverified on Windows** (#1414 stays open); the system clipboard itself is wired (eframe's `clipboard` feature), so the open question is the Windows image path, not the clipboard API.
- **At most 16 videos hold a decoder at once** in the editor/show; the rest play sound only until a decoder frees up (`crates/ui-egui/src/media.rs`).
- **Web build is silent and stateless:** no audio output, no TCP control channel, no persisted preferences.

### Output
- **PDF artwork is rasterized.** Each slide is placed as a print-DPI image (capped at 64M pixels per slide raster) under an invisible real-text layer; text is selectable/searchable but the artwork is not vector.
- **No native print dialog.** File ▸ Print (Cmd+P) builds a PDF in the temp folder and opens it in the system viewer.
- **No MP4/MOV export.** Only the animated GIF exists: one static frame per slide, no transitions or build animations.

### Platform and UI
- **No native macOS menu bar.** `menus::menu_tree()` exists but nothing installs it; use the ribbon, the command palette (Cmd+Shift+P) or commands.
- **Presenter view is a second window but is not assigned to the second display** by DeckCraft; on Linux and the BSDs it stays off when winit reports exactly one display.
- **CPU rasterization and software video decode**; no GPU slide rendering or hardware decode. **English-only UI**, no string catalogue. Pen pressure works, tilt does not.

### Feature depth
- **Charts are partial:** chart-element editing and some `chartex` behaviour are thinner than PowerPoint's.
- **Animations are partial:** 64 non-path effects of roughly 190 in PowerPoint.
- **SmartArt is shallow:** 45 simple layouts against PowerPoint's ~200, no picture layouts or 3-D styles; the Reuse Slides picker has no thumbnails.
- **No recording:** the Record tab's Record button is disabled ("Recording narration needs audio capture").
- **Equations are not authored as OMML:** the Equation dialog inserts pretty-printed Unicode text. OMML in an imported `.pptx` is kept and written back (`RunKind::Math`, `a14:m`; `crates/pptx/src/{read,write}/dml.rs`) but drawn as its flattened text, so it is not typeset.
- **No AI/cloud features** (Copilot/Designer/Speaker Coach/live captions); only offline Design Ideas arrangements. **No add-ins or VBA** by policy; MCP/CLI is the automation alternative.

### Automation and data-safety behaviours to know
- **`file.close` closes a dirty document without prompting.** The UI's Close (`app.closePresentation`, Cmd+W) prompts; the raw engine command does not. Do not call `file.close` on unsaved work.
- **`app.quit` over the control channel quits without asking.** `{"save": true}` saves every dirty presentation first and answers with an error if one can't be saved (an untitled deck opens a Save dialog there), so save explicit paths before quitting.
- **`file.save`/`file.saveAs` without a `path` (and no stored path) ask the UI** and return `{"needsPath": true}`, writing nothing in headless use — always pass `path`.
- **`file.save`/`file.saveAs`/`run --save` refuse `.png`/`.jpg`/`.jpeg`** — `save_bytes` returns an error telling you to use `file.export`. MCP `save_presentation` and control-channel `app.save` inherit the same refusal.
- **A non-image extension still falls through:** `file.save {path: "x.odp"}` (or any extension no writer maps) is written as native `.deckcraft` bytes under that name, and `file.export` does the same. Check the extension you pass.
- **`run` stops at the first failing command and saves nothing.**
- **Reads are bounded and saves follow links:** every path read needs a regular file of at most 2 GiB, and a save canonicalizes the target (so it writes through a symlink), preserves the existing file's permissions, and writes via a hidden `.deckcraft.<pid>.<n>.saving` sibling that must also be inside the automation write root.
- **MCP batches are bounded:** 1 000 entries and 64 MiB of results; a batch full of `inspect_slide` answers on a notes-heavy deck can hit the byte cap and stop early (`crates/mcp/src/tools.rs`).
- **The control channel has no authentication.** It binds loopback only; do not expose or port-forward it. The web `window.deckcraft` object is the same command authority inside the page: any script of the page's origin can call it, so treat a page that embeds DeckCraft as trusted code (`packaging/web/README.md`).

## How to operate

### Check what is installed
```sh
command -v deckcraft-cli                 # headless CLI: a separate download, not in the .app
# the app bundle's own binary prints its version and exits before opening a window:
#   <DeckCraft.app>/Contents/MacOS/DeckCraft --version   →   deckcraft 0.18.1
#   <DeckCraft.app>/Contents/MacOS/DeckCraft --help      →   usage, then exit
```
The `.app` bundle contains no `deckcraft-cli`. The CLI ships as the separate signed/notarized release asset `deckcraft-cli-<ver>-macos-<arch>.zip` (the packaging default is `<arch>` = `universal`); download/unzip it, build it with `cargo build --release -p deckcraft-cli`, or automate through the control channel instead.

### Launch
```sh
open -a DeckCraft                          # normal GUI
open -a DeckCraft --args --sample          # sample deck
open -a DeckCraft talk.pptx                # open a file
open -a DeckCraft --args --control 7990 --sample
```
GUI flags: `--control PORT`, `--sample`, `--show`, `--help`/`-h`, `--version`/`-V`, and file paths; `-psn_*` is ignored. The port can also come from `DECKCRAFT_CONTROL_PORT`. The desktop parser is hand-rolled: an unknown argument is treated as a file path, so a mistyped flag shows up as a failed open, not a usage error.

### CLI
`deckcraft-cli` is the most reliable automation surface; it needs no window.

| Command | What it does |
|---|---|
| `info FILE` | JSON: slides, layouts, theme fonts, sections, slide size (`document.inspect`) |
| `render (FILE \| --sample) [--slide N \| --all] [--scale S] [--edit] [--transparent] OUT` | PNG per slide; `--all` writes `slide-01.png…`; default scale 2; `--slide` 0-based |
| `render-transition FILE --slide N --t T[,T...] [--width PX] OUT.png` | Frames of the transition into slide N |
| `convert IN OUT` | Save in OUT's extension: `.deckcraft`, `.pptx`/`.potx`/`.ppsx`, `.pdf`, `.txt`/`.md`/`.rtf`, `.png`/`.jpg` (first slide), `.gif`; other extensions are refused |
| `run [--in FILE \| --sample] [--cmd ID[=JSON] \| --cmd-file FILE]... [--save OUT] [--export OUT [--export-params JSON]] [--print]` | Run commands, then save/export; stops and saves nothing on the first error |
| `commands [FILTER]` / `describe COMMAND` | List ids/params; explain one |
| `app [--port PORT] COMMAND [JSON]` / `--method METHOD [JSON]` | One request to a running `deckcraft --control` (default port 7979) |
| `mcp [--connect PORT] [--sample] [--automation-read-root DIR]... [--automation-write-root DIR]...` | MCP server on stdio; both root flags and both spellings repeatable |
| `bench (FILE \| --sample) [--runs N] [--json]` | Time open/draw/save/PPTX reopen/PDF export and peak memory |

`--cmd-file FILE` reads one command per line from a UTF-8 file (blank lines and full-line `#` comments skipped, CRLF and a BOM accepted, 16 MiB a line), which avoids shell quoting and command-line length limits; it can repeat and mix with `--cmd` in order.

Examples:
```sh
deckcraft-cli commands format.
deckcraft-cli describe shape.insert
deckcraft-cli run --cmd 'slide.new={"layout":"titleOnly","title":"Q3 results"}' \
  --cmd 'shape.insert={"preset":"roundRect","rect":[80,160,320,120],"text":"Revenue"}' \
  --save q3.deckcraft
deckcraft-cli render q3.deckcraft --all --scale 1 out/
deckcraft-cli convert q3.deckcraft q3.pdf
deckcraft-cli run --in q3.deckcraft --export q3.rtf
```
`--print` prints each command's **answer**; it is not a printer flag. `convert` gives no PDF-layout options and only the first slide for PNG/JPEG; use `run --export` or `file.export` for notes/handouts and all slides.

### Conventions that prevent most automation bugs
- Coordinates are **points** on a 960×540 (16:9) slide unless the deck says otherwise; a rect is `[x, y, width, height]`.
- **Slide indices are 0-based**; `render --all` names files from 1 (`slide-01.png`), while `file.export all` names `stem1.png`, `stem2.png`.
- **Shape ids are looked up on the page being edited** — the current slide in Normal view, the master/layout/notes page in Master views — never another slide; `slide.go {index}` changes the current slide; `slide.new` inserts after it and selects the new slide (pass `at` for an index).
- Commands that add a shape select it; `format.*` acts on the selection, while many shape commands take `ids` directly — **`ids` entries that don't resolve are an error, not a silent fall back to the selection**.
- Text bodies use `\n` for a new paragraph and a leading tab per level for bullets.
- **Every index parameter is strict:** a negative or fractional `index`/`from`/`at`/`master`/`layout` is an error; a valid index past the last slide is also an error; `review.spellingChange` rejects an overflowing `start`; `comment.next`/`comment.prev` reject a malformed `index`; animation remove/move/timing/options reject invalid indexes; table row/column and `cells` commands reject invalid cells and out-of-table entries; `shape.adjust`/`shape.quickStyle` reject a negative/fractional `index` (values past 16/41 clamp).
- **`format.align` also accepts `thaiDist`**, although its parameter doc string lists only left/center/right/justify/justifyLow/distributed, and **an unknown `align` name still falls back to left**; `format.paragraph` and `format.paragraphDialog` accept the same names (plus `centre`, `justifyLow`) and **error** on anything else.

### Documents, open/save/export
- One process can hold several presentations; `file.new`/`file.open` add documents, `window.next` cycles the active one, and `view.newWindow` opens a second, non-editing window on the same deck.
- **Open:** `file.open {path}` — native `.deckcraft`, `.pptx`/`.potx`/`.ppsx`, and `.txt`/`.md`/`.rtf` outlines (RTF by content sniffing, not only extension), plus `.thmx`/`.pptx`/`.potx` through `design.browseTheme`. Open is lenient for PPTX: unknown parts skipped/kept, unreadable slides reported in `lostSlides`, damaged files open as a repaired copy, and media lengths/sizes are filled in from headers.
- **Save:** `file.save {path, format?: deckcraft|pptx}` / `file.saveAs {path, format?}` / `file.saveTemplate {path}`; the format follows the extension unless `format` is given. **Images are refused: use `file.export`.** Writes go to a hidden `.deckcraft.<pid>.<n>.saving` sibling (also checked against the automation write root) renamed over the target, so a failed save never truncates the old file.
- **Export:** `file.export {path, format?, ...}`. PNG/JPEG: `slide?`/`all?`/`scale?`/`transparentBackground?`; PDF: `layout`, `perPage` (handouts only, exactly 1/2/3/4/6/9), `paper`, `orientation`, `dpi`, `slides`, `includeHidden`, `textLayer`, `frame`; GIF: `width`, `secondsPerSlide`, `loop`, `slides`, `includeHidden`; outline: `txt`/`outline`/`rtf`. All requested image indices are validated before any file is written.
- **Native format as source of truth:** keep the `.deckcraft` master and treat `.pptx` as an exchange copy. Native save is lossless for DeckCraft's model (chart payloads included); PPTX has the known losses above.

### Drive a running app
Start `deckcraft --control 7990`, then either `deckcraft-cli app …` or raw JSON lines:
```sh
deckcraft-cli app --port 7990 --method ui.screenshot '{"path":"shot.png"}'
deckcraft-cli app --port 7990 shape.insert '{"preset":"star5","rect":[100,100,200,200]}'
```
```json
{"id":1,"method":"engine.execute","params":{"command":"shape.insert","params":{"preset":"star5","rect":[100,100,200,200]}}}
{"id":2,"method":"ui.screenshot","params":{"path":"shot.png"}}
```
Use `ui.inspect` first to learn the window, `canvasRect`, `slideRect` and `canvasScale`, the active tool, dialogs and documents; `ui.pointer` takes **slide points**, while `ui.move`/`ui.click`/`ui.drag` take **window points** (egui coordinates, as `ui.inspect` reports them). The MCP equivalent is `deckcraft-cli mcp --connect 7990`. For headless MCP:
```json
{"mcpServers":{"deckcraft":{"command":"deckcraft-cli",
  "args":["mcp","--automation-read-root","work/deck","--automation-write-root","work/deck/out"]}}}
```
Paths outside the roots are refused with ordinary tool errors; a root left out grants none of its access, `--flag=DIR` works, each flag may be repeated (multiple roots per kind), and roots cannot be combined with `--connect`.

### Drive a web build from its page
A web build (embedded or standalone) installs `window.deckcraft`; calls are promises over the same methods, so `execute("shape.insert", …)` is exactly the desktop `engine.execute`:
```js
await window.deckcraft.execute("shape.insert", { preset: "roundRect", rect: [100, 100, 240, 120], text: "Hello" });
const doc = await window.deckcraft.docInspect();
const { data } = await window.deckcraft.screenshot();   // base64 PNG
```
A call rejects if the app does not answer within 30 s (`packaging/web/README.md`); the shared craft-libs `web-api` contract also refuses a 65th call waiting at once and releases a call the page gave up on (not audited in depth here). This is a page-local surface, not a network one — there is no port to connect to.

### Environment and logs
- Settings/logs: `~/Library/Application Support/DeckCraft/` (`ui.json`, `prefs.json`, `logs/deckcraft.log`, rotated, capped at 16 MiB); recovery: `…/DeckCraft/Recovery/`.
- `DECKCRAFT_CONTROL_PORT` sets the control port; `DECKCRAFT_NO_AUDIO=1` plays silently; `DECKCRAFT_NO_PREFS=1` skips preferences; `DECKCRAFT_NO_RECOVERY=1` skips AutoRecover; `DECKCRAFT_DICTIONARIES` adds dictionary folders; `RUST_LOG` sets log levels.

## Working with an AI agent

### Choose the surface
1. **Headless CLI** (`deckcraft-cli run`, `render`, `convert`, `info`, `mcp`) — best for generating decks, batch exports and verification. No window, no GUI state.
2. **MCP stdio** (`deckcraft-cli mcp`) — best when the agent has an MCP client; use `run_command`/`batch` for anything the 25 tools do not wrap, and `inspect_document`/`inspect_slide` before editing. A headless server starts with no document: call `new_presentation` or `open_presentation` first. `batch` stops at the first error unless `keepGoing`, and is capped at 1 000 commands / 64 MiB of results; tools reject unknown argument names rather than guessing.
3. **Control channel** (`deckcraft --control`) — only when a human and agent must share a live window, or UI-only state (dialogs, selection, screenshots) matters. Always `ui.inspect`/`ui.screenshot` before pointer work; never click blind.
4. **Web page API** (`window.deckcraft`) — only inside a page that already runs the web build; it is the same command authority with a 30 s promise timeout and no network port. Use it to build editor-like web integrations, not to reach a desktop app.

### Prepare inputs
- **Pictures:** PNG, JPEG, WebP, GIF, BMP, TIFF (not SVG, not HEIC; EMF/WMF only when already inside a deck). Pre-render logos and icons to PNG with transparency.
- **Audio/video:** MP3, AAC/M4A, ALAC, WAV, AIFF, CAF, FLAC, Ogg, Opus; H.264/HEVC/VP9/AV1 in MP4/MOV/WebM/MKV. Transcode WMA/WMV first. Keep a deck to a handful of simultaneously playing videos — 16 decoders is the hard cap.
- **Outlines:** a Markdown file with `#` headings, a tab-indented plain-text file, or `.rtf` (`\outlinelevel` paragraphs, falling back to `\li` indent) imports directly (`slide.fromOutline`); footer/date/slide-number placeholders are skipped on export.
- **Themes:** `.thmx`, or a `.pptx`/`.potx` whose first master holds the theme and layouts.

### Inspect, repair and convert
- `.deckcraft` is a zip: inspect `presentation.json`, `media/<id>` and `chart-parts/<index>` with `unzip -l`/`unzip -p`. Repair damaged media by restoring the member; do not rewrite the JSON unless the schema is understood. Older files with inline chart bytes still load and migrate on save; a manifest over 256 MiB is refused.
- Do **not** hand-edit a `.pptx` zip to "fix" it: use DeckCraft commands and re-export. Unknown PPTX parts are preserved by the writer, but hand-edited XML can break content types or relationships.
- Convert between `.deckcraft`, `.pptx`, `.pdf`, `.txt`/`.md`/`.rtf` and images with `convert`, remembering that `convert` writes only the first slide for PNG/JPEG and uses default PDF options.
- A chart written back verbatim (over budget) will not respond to chart edits; replace it with a fresh `insert.chart` if the data must be editable.

### Verify exports
- Read the command result: exports return `{path, bytes}` or `{files}`; assert the file exists and its size is plausible. A zero-byte or missing file is a failure even if the process exited 0.
- Re-open the result: `deckcraft-cli info out.pptx` and compare slide count/titles/layouts; `deckcraft-cli render out.pptx --all` and look at the PNGs.
- For PDF, check page count and extracted text; the text layer is selectable but the artwork is raster, and evaluated fields (a slide number) appear as their values.
- For `.pptx` and `.ppsx`, the strongest test is opening it in PowerPoint/Keynote and checking for a repair prompt, animations, media and theme fonts. The project has not tested a real-deck corpus.
- For GIF, verify the `GIF89a` header, dimensions, frame count and delay; transitions/builds are intentionally absent.

### Do not
- Do not insert SVG, HEIC, or EMF/WMF via `insert.picture` and expect them to draw.
- Do not promise `.ppt`, `.odp`, `.pptm`, macros, password protection or MP4 export.
- Do not call `file.close` or `app.quit` on unsaved work; use `app.quit {"save": true}` only after saving explicit paths.
- Do not use `file.save`/`--save` for `.png`/`.jpg`: it is refused; use `file.export`/`--export`/`convert`. And do not trust an unmapped extension in `file.save`/`file.export` — it writes native bytes.
- Do not assume PDF is vector or that a `.pptx` round-trip is lossless.
- Do not rely on font metrics matching PowerPoint exactly; substitute faces change line breaks. Verify visually.
- Do not expose the control channel beyond loopback; it has no authentication. Do not run untrusted scripts in a page that hosts `window.deckcraft`.
- Do not trust `docs/` where it contradicts the code (request-line size, exit-effect count, command and crate counts, MCP batch caps, the `thaiDist` parameter doc are stale at this tag).

## Verification protocol

Alpha software with active auto-updates: verify every deliverable, keep a native master, and never trust a silent export.

1. **Pin the version.** Record the bundle's `--version` (`deckcraft 0.18.1` for this audit) before work. Update only between projects, not mid-deck; command ids, formats and export options move between releases.
2. **Work in a throwaway directory.** Copy sources in; never run destructive tests on the only copy of a deck. Keep a `.deckcraft` master plus dated backups.
3. **Round-trip a small test first.** New deck → one slide, shape, table, chart, picture, transition and note → save `.deckcraft` → export `.pptx` → reopen the `.pptx` → inspect counts and render PNGs. Fix workflow problems before touching the real deck.
4. **Save before every export.** A failed export must not be the only copy of your changes. `file.save` is atomic via a hidden `.saving` sibling; exports are ordinary writes.
5. **Check every export explicitly.** Existence and non-zero size; images: dimensions (and alpha, when `transparentBackground` was used); PDF: page count and selectable text; PPTX: reopen and render; GIF: header, dimensions, frame count; RTF: re-open as an outline.
6. **Look at the pixels.** `deckcraft-cli render … --all` (or MCP `render_slide`) and inspect the PNGs. Text overflow, missing fonts, blank SVG/EMF pictures and chart scaling are visual failures that a successful exit code will not catch.
7. **Open in the target app.** If PowerPoint is available, open the exported `.pptx` and check for repair prompts and lost animations/media. If not, state that fidelity is unverified rather than claiming parity.
8. **Keep the native file.** The `.deckcraft` master preserves DeckCraft-only constructs (including chart payloads) and is the safest thing to reopen after a failure.
9. **Record what changed.** Note version, command lines/JSON params, export options and any manual GUI steps, so a failed export can be reproduced.

## Sources & evidence

- **Repo:** https://github.com/storytold/deckcraft — tag `v0.18.1`, commit `7cc73ab1895ed2e30c8afbcada20c70b9ea0a440` (`git rev-parse HEAD`), inspected **2026-11-12**; `v0.16.0` (`a3e2254d…`) was diffed for every set and behaviour claim (121 files, +2 939/−7 950). The pinned checkout is shallow and squashed (one release commit per tag, only `v0.16.0` and `v0.18.1` present), so the tag-to-tag diff is the evidence for the delta.
- **Installed bundle:** `/Applications/DeckCraft.app`, `CFBundleIdentifier` `ai.storyteller.deckcraft`, version `0.18.1`; `--version` prints `deckcraft 0.18.1`; universal x86_64+arm64, Developer ID signed (Learning Machines LLC), notarized and stapled (`spctl` accepts it).
- **Key files read:** `README.md`; `Cargo.toml`; `ROADMAP.md`; `docs/{architecture,gaps,file-format-parity,animation-parity,target-app-parity,control-protocol,mcp}.md`; `packaging/web/README.md`; `apps/deckcraft/src/{main,control_server,apple_events,logging}.rs`; `apps/deckcraft-cli/src/help.rs`; `apps/deckcraft-web/src/{api,host}.rs`; `crates/engine/src/cmd.rs` and `crates/engine/src/cmd/` (id parse over every module, plus `file.rs`, `format/paragraph.rs`, `insert/text_fields.rs`, `shape/{appearance,size}.rs`, `insert/album.rs`, `reuse.rs`, `review.rs`, `smartart.rs`, `three_d.rs`, `table.rs`); `crates/engine/src/{io,lib,connect,file_access,spell,tools}.rs`; `crates/model/src/{anim,chart,theme,text,lib,edit,trendline,resolve}.rs`; `crates/geom/src/{preset/catalog.rs,warp.rs}`; `crates/format/src/lib.rs`; `crates/pptx/src/{lib,read,write,dgm}.rs` and `crates/pptx/src/{read,write}/{chart,dml,shapes}.rs`; `crates/pdf/src/lib.rs`; `crates/mcp/src/{tools,server,backend,headless}.rs`; `crates/ui-egui/src/{lib,control,show,media,widgets}.rs`, `crates/ui-egui/src/panels/{fillui,notes}.rs`, `crates/ui-egui/src/app/files.rs`, `crates/ui-egui/src/ribbon/{animations,home}.rs`; `packaging/macos/Info.plist.in`.
- **Shared libraries (not audited):** `craft-media`/`craft-audio` at `75895c0321d8cb6e175a42466cba050352b117c5`; `craft-pdf`/`craft-update`/`craft-ui` at `6e03f65bf45181db77ba6229716e6624db9eb25b`; the web app's `craft-web-api`/`craft-web-host` at `fd5e2feff6ea25bed371a99cc732b3968d621505` (the page-API contract is documented in the craft-libs `web-api` crate README).
- **Docs that are stale at this tag (code wins):** `docs/control-protocol.md` (16 MiB vs the code's 256 MiB); `docs/animation-parity.md` (14 exits vs 23); `docs/architecture.md` (320 commands and 24 crates vs 329 and 20) and `docs/target-app-parity.md` (328); `ROADMAP.md` ("226 commands"); `docs/mcp.md` (no batch caps); `format.align`'s parameter doc (omits `thaiDist`).
- **Not independently verified:** PowerPoint's acceptance of exported `.pptx`/`.ppsx` without repair on real decks, render fidelity against PowerPoint, runtime command execution, `deckcraft-cli` execution (not installed on this machine), the web `window.deckcraft` API in a browser, and any GUI behaviour. Claims here are code and document inspection plus bundle metadata and `--version` checks; no GUI was launched and no deck was rendered.
