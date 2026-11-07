---
name: silentkit-interface
description: >-
  Engineering reference for the interface layer of a ghost client: an in-game "click GUI" (floating panels,
  navigator, module list, settings rendering), the HUD/overlay system, a custom 2D render abstraction and font
  pipeline, theming and animation, keybind UX, and an optional web/remote control surface. Use when building or
  extending the client menu, HUD, or render stack. Brand-neutral and framework-agnostic.
---

# SilentKit · Interface

The menu, HUD, and render layer of a ghost client. Brand-neutral: patterns and composition, not any one project's
code. Keep this separate from gameplay logic (`silentkit-modules`) and loading (`silentkit-runtime`).

---

## 1. The render abstraction (`Render2D`)

Everything the client draws goes through one small immediate-mode 2D API so modules never touch the engine's
constantly-changing render internals directly. A thin per-version adapter implements it; everything else is stable.

Core surface (one instance per draw pass, carrying an **alpha multiplier** and **letter-tracking** so a whole subtree
fades/spaces uniformly):
- `rect / roundedRect(x,y,w,h,r[,cornerFlags],color)`, `roundedOutline(...,thickness,...)`, `line`, `lineGradient`,
  `circle / circleOutline`, `arc(cx,cy,r,thickness,startDeg,sweepDeg,color)`, vertical/horizontal gradient fills.
- `shadow(x,y,w,h,r,blur,color)` for soft drop shadows and `blurRect(region,r,tint)` for frosted panels (falls back to
  a solid fill before the blur texture exists).
- `text / textShadow / textCentered / textRight(str,x,y,color,font,size)`, `textWidth(...)`, and a `fit(str,maxW,...)`
  that ellipsizes — plus `component(...)` for styled/translatable text. A per-glyph **tracked** draw lays styled text
  out on float advances so letter-spacing works.
- `item(stack,x,y,size[,decorations])` for inventory icons; the engine's sprite blit for effect icons.
- **Pixel snapping**: `snapX/snapY` round a coordinate to a whole *physical* pixel through the current pose, so hairline
  strokes and shared panel edges don't shimmer at fractional GUI scales. An anti-alias width (`pixel()`) scales edge
  softness to the backing scale.

A separate **world projector** turns world coordinates into GUI-space screen points: it captures the **exact**
modelview (camera × view-bob × hurt-shake, camera at the origin) and projection (dynamic FOV, nausea) the level is
drawn with *this frame*, so overlays (ESP, tracers, nametags, radar dots) line up with the moving world. It returns
`{x, y, onScreen, distance, behind}`; a 12-edge box helper and bearing math sit on top. For a 2D screen-projected box,
keep the corners that are *in front of* the camera and bound them, rather than dropping the whole box when one corner
crosses behind you (that discard is the classic projected-ESP flicker).

For overlays that should **depth-test against the world** (3D boxes, trajectory ribbons), add a small **world-space
render abstraction** alongside the projector instead of screen-projecting: build camera-relative geometry on the CPU and
submit it inside the level render pass. Lines become camera-facing **ribbon quads** — side `= normalize(tangent × eyeRay)`,
world half-width `= (halfPx+1px)·worldPerPx·depth` so on-screen width is depth-independent, a 1px feather in a UV channel,
core width in a per-vertex `LineWidth` attribute — and any edge crossing behind the camera is **clipped to a near plane**
(lerping position and colour), never dropped. Register the render type as a **visible/hidden pair** that partitions the
screen by depth (reversed-Z: visible `GEQUAL`, hidden `LESS`), sharing one small depth bias so coplanar geometry doesn't
z-fight; callers draw the hidden (through-wall) pass faded. This one pair backs box-ESP, trajectories and markers.

Keep colors as ARGB ints with a `withAlpha` helper; never hardcode engine color objects. One adapter per engine
version means a UI change ships once, not N times. Where the engine exposes a pipeline/render-type system, back
`Render2D` with a few custom pipelines (rounded-rect, blur, line) rather than per-call GL state.

---

## 2. Fonts

Two viable strategies:
1. **Engine text renderer** — simplest; good enough if the engine's font is acceptable and consistent across versions,
   and necessary as a *fallback* for glyphs/codepoints your own atlas doesn't cover (server scoreboards lean on exact
   space-glyph layouts, so detect non-covered codepoints and fall back to the engine's pixel font at native size with
   zero tracking).
2. **Self-contained glyph rasterizer** — ship a TrueType/CFF rasterizer + a glyph-atlas cache. Costs more but renders
   identical UI across every engine version and at arbitrary scale, and frees the look from the engine's font. Use it
   when the brand/identity depends on exact type, or when you support many engine versions.

Either way: define named font **roles** (`display`, `body`/`medium`, `semibold`, `mono`) backed by a configurable
family, with a base size and a type scale; measure with `textWidth` for layout; give uppercase labels letter-spacing.
Let the user pick HUD and menu families independently, and prefer a crisp system rounded face where present (detect it;
fall back otherwise). Reserve digit widths in metered readouts (FPS, counts) so the layout doesn't twitch as numbers
change.

---

## 3. The click GUI — floating panels

A Vape/Drip-style floating-panels menu reads as modern and is simple to compose:

- **Panels** are draggable, collapsible cards (a category list, the navigator, a settings pane). Each remembers its
  rect; persist rects so layout survives restarts. Add **snap-to-grid** on drag and **saved named layouts** (and a
  one-click auto-arrange). A shared `Panel` base handles the drag/collapse/header; concrete panels only draw their body.
- **Navigator** — the root panel: a home list of categories, plus special sub-pages (Client Settings, Style/Theme,
  Accounts) that slide in. Sub-pages are second-level lists built from the existing Setting objects, so the GUI has
  almost no bespoke state — it renders modules' real settings.
- **Module list** — rows with a label, a toggle switch, and small **badges** (flags-here / needs-X / safe), driven by
  per-module metadata. Clicking a row opens its settings inline (or in the settings pane). A category panel + a
  module-rows renderer keep this generic.
- **Settings rendering** — one renderer per Setting type: a toggle, a slider (with an inline value you can type — back
  it with a tiny expression evaluator so "3*8" works), a segmented mode control, a color picker (with a gradient/accent
  editor), a keybind capture, a text field, an item-list editor, and a collapsible Section / tabbed / pop-out group.
  Drive `.visibleWhen(...)` so conditional rows fold away. A per-module **filter box** ("type 'color'") tames dense
  panels. Dropdowns and context menus render in a top-most pop-up layer so they're never clipped by a panel's scissor.

**High-value additions (most already pay for themselves):** a **command palette / search panel** (fuzzy launcher:
toggle any module, jump to a setting, run an action); a **favorites / pinned quick-access** panel; **module context
menus** (bind / favorite / reset / copy / share); a **live hover preview / tooltip** (`HoverTip` — a tiny demo or
description of what a module does); a **server-info card**; a **density/scale/reduced-motion** control for
accessibility; an **in-menu changelog** with a "new" dot on recently-added modules. Keep one-module-open-at-a-time as a
toggle so dense panels stay readable.

---

## 4. HUD / overlay system

- A **HudModule** subtype renders to the screen each frame from a shared **anchor + offset** model (anchor to a screen
  corner/edge/centre, then a dx/dy), so elements reposition correctly at any resolution. A **WorldOverlay** renders in
  world space via the projector. A shared backdrop draws each element's background/corner/padding from the Style page
  unless the element overrides it. A **HUD editor** screen lets the user drag elements, with snapping to screen
  edges/centre and to the hotbar, and a grid.
- A thin **single-line readout base** (`TextHud`: label + value, with a Layout setting — label-first / value-first /
  value-only / bracketed) covers the dozens of trivial readouts (FPS, ping, coords, biome, speed, health…) with almost
  no per-module code.
- Standard elements: watermark, FPS, CPS, keystrokes, coordinates, armor, potions, ping, target plate, radar, compass,
  rearview mirror, now-playing, nearby-players, combat-predictor, notifications. Make them **adaptive** — a combat
  layout in a fight, an explorer layout while roaming — switched off a shared combat/world state.
- A **HUD-overrides** layer can intercept and restyle or hide vanilla HUD elements (hotbar, scoreboard, boss bar,
  effect icons) so your HUD and the engine's don't double up.
- **Recording mode** — hide the client's own visuals for clean screen capture (HUD and/or world overlays), toggleable;
  pair with a name-protect / streamer mode that swaps your username out of all drawn text.

---

## 5. Theming

- Define every color as a **token** on a theme object (bg, card, line, fg, dim, faint, accent, accent-2, good, warn,
  bad). Components read tokens, never literals. One accent change re-skins the whole UI. A `Style` module owns these
  plus corner radius, padding, panel opacity, blur strength/quality, border/shadow toggles and the font roles, and is
  the single source every render path reads.
- Support **palette presets** and a **gradient accent editor**, plus **share codes** (serialize the theme to a string
  to copy in/out) so a look travels like a config. Support a **chroma** (time-animated hue cycle) and **gradient** text
  mode for list elements, laid along the list so it flows.
- Blur-behind panels, soft shadows, and subtle motion sell "polished"; keep animation deliberate (one orchestrated
  open, hover micro-interactions) — scattered effects read as noise. Keep a config **version** on the style blob and
  migrate old keys forward (renamed fonts, changed defaults) so a saved theme survives a redesign.

---

## 6. Animation

A small animation toolkit keeps motion consistent and frame-rate-independent:
- A **`Smooth`** value that exponentially approaches a target each frame on real `dt` (the same `1 − e^(−rate·dt)`
  approach the gameplay layer uses) — use it for every fade, slide, bar fill, and hover state so nothing is a per-tick
  step or FPS-dependent.
- An **easing** library (smoothstep, cubic, back/overshoot) and a small keyframe **`Animation`** driver for one-shot
  orchestrated transitions (the menu open). Gate all of it behind a reduced-motion / animation-speed control.

---

## 7. Sounds & feedback

A small UI-sound layer (soft clicks, toggles, hover ticks) with a volume + pack setting. Pair with the toast /
notification queue (a shared ring buffer rendered as sliding toasts) so actions confirm themselves (toggle → toast),
and so module-toggle feedback can stand down when the on-screen module list already shows the change. Keep all of it
behind a master "UI sounds" switch.

---

## 8. Keybind UX

- A **keybind manager page**: every bind on one screen, **double-bound keys flagged**, and press-a-key-to-find.
- Support multi-bind (one key toggling several modules), a "hold vs toggle" bind mode, and binding from the module row
  directly. Capture via a key-event overlay; store as engine-neutral key tokens. Route all binds through one manager so
  conflicts and hold-mode are handled in one place.

---

## 9. Optional: web / remote control surface

If the client has a backend, mirror the menu on the web: the client holds a lightweight heartbeat that pushes its
current config to a per-user row and polls for edits; the website renders the same settings and patches one module at
a time. Make web edits land only while the client is online. This also gives a natural home for a phone companion
(push notifications, a live map, remote loadout switch) and an **update notifier** (compare versions server-side, toast
the client). Keep the transport generic (any small key/value backend).

---

## 10. Composition checklist

- One render abstraction; one adapter per engine version; a world projector that captures the frame's real matrices.
- Settings are the single source of truth — the GUI renders them, it doesn't duplicate state.
- Tokens for every color; one accent drives the theme; design both light and dark if the engine can be either; version
  and migrate the style/config blob.
- Panels persist their layout; snap + saved layouts; auto-arrange; pop-ups in a top-most layer.
- Badges + command palette + per-module filter make a big module set navigable.
- HUD elements are anchor-placed and adaptive; a trivial-readout base covers the long tail; a recording mode hides the
  client's own visuals.
- Every fade/slide goes through one frame-rate-independent `Smooth`; reduced-motion respected.
