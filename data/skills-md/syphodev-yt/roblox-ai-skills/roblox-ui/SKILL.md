---
name: roblox-ui
description: Build Roblox game UI headlessly - HUD overlays, shops, inventories, quest lists, settings - from a JSON spec, and generate the icon set that goes in it. Emits a PNG mockup, a Rojo .model.json and a Luau builder from ONE resolved tree, so the preview cannot drift from what ships. Use whenever the user wants a Roblox GUI, menu, shop UI, HUD, inventory screen or UI mockup made rather than clicked together in Studio, wants game icons generated, wants a UI built from a theme file, or asks why their UI looks flat, breaks on mobile, or renders differently in Studio than in the design.
---

# Roblox UI, headless

> **KAGGLE IS OFF (2026-10-19). Do not use it for any stage.** Its terms only allow
> personal, non-commercial, ML/data-science use, and running these skills' GPU
> stages there got the author's account banned for "resource abuse". Never make a
> second Kaggle account either. See the notice at the top of `roblox-3d-model`
> for the routes to use instead.

> **First time on this machine?** Read `LOCAL.md` in this folder. If it does not exist, run the
> `roblox-skills-setup` skill (or copy `LOCAL.template.md` to `LOCAL.md` and fill it in).
> `LOCAL.md` holds your paths and tool locations; it is yours and is never shared.

## Quick start: your first HUD in one minute

`examples/coin_hud.json` is a complete, passing spec (a coin counter, top-left).
Copy it next to your game, change it, and build:

```bash
python scripts/ui_build.py examples/coin_hud.json --out build    # PNG + .model.json + Luau
python scripts/verify_ui.py examples/coin_hud.json               # layout, text fit, touch sizes
```

- `"theme": "default"` uses `references/theme.json`. To restyle, copy that file
  next to your spec, edit it, and set `"theme": "mytheme.json"` (see Themes below).
- A label your code fills in at runtime ships as `"<unbound>"` and lists its
  longest real values in `"samples"`, which is what the text-fit check measures.
- Icons need an icons folder passed with `--icons`; leave them out until you have one.

Two halves that meet in the middle: **procedural structure** (about 80% of what
reads as modern Roblox UI needs no image at all) and a **generated icon set** for
the part that does.

Design numbers live in `references/ui-recipes.md`, measured from Roblox staff
posts and four community guides. Read it before inventing a value.

---

## The one idea this skill is built on

**A mockup drawn in a design tool is a picture of a UI, and it drifts.** So there
is no design tool here. One JSON spec resolves to one tree, and that tree emits:

| Output | What it is for |
|---|---|
| `Page.png` | The fast local probe. Sub-second, no Studio, no plugin. |
| `Page.model.json` | The deliverable. Drops into a Rojo project. |
| `Page.lua` | The transport. Paste into `execute_luau`, no Rojo session needed. |

The PNG cannot disagree with the `.model.json` about a size, a colour or a
layout, because neither is authored: both are rendered from the same resolved
tree. The Studio screenshot stays ground truth for what the renderer
approximates (font metrics, gradient banding).

This is the UI stage's version of the 2D concept gate in `roblox-3d-model`: put
the checkpoint where judging is cheap and reliable. UI is the only stage that is
natively 2D, so what you screenshot is what ships.

---

## A PLACEHOLDER MUST BE A STRING THE LIVE CODE CAN NEVER PRODUCE

**Never use `--`, `0`, `...`, `—` or an empty string as a dynamic label's
placeholder. Use a sentinel like `<unbound>`.** And then gate on it: every label
carrying the sentinel must be named by some controller, or the build fails.

Measured in a real build. A shipped HUD had four labels - an ammo counter and three
rows of a freezing panel - that **no line of code anywhere could write**. The
ammo count lived in a server-side table that was never broadcast; the freezing
rows were fed from a roster that did not carry a frozen flag. They rendered `--`
for entire runs, in front of the user, while sheep actually froze to death.

Nothing caught it, and the reason is the interesting part:

- `verify_ui.py` passed, because it checks **layout** - nothing touching, nothing
  off-centre, no box round a button. A dead label is laid out perfectly.
- The PNG mockup agreed with the game, because **both are drawn from the same
  tree**. That agreement is this skill's core strength and it is exactly why it
  cannot see this class of bug.
- `--` **reads as a plausible empty value.** It looks like "no ammo yet", not
  like "this label is wired to nothing". A sentinel that no formatter could ever
  emit turns a silent defect into an obvious one on the first screenshot.

The gate is about twenty lines: walk the built `.model.json`, collect every named
node whose `Text` is the sentinel, and require the name to appear in the client
source. Two shapes count as a reference - the literal (`"AmmoCount"`) and an
**assembled** one (`` `BankRow{i}` .. "Name" ``), so split the name on digit runs
and require each segment; a name with no digits must appear literally. Getting
that wrong matters: a first version understood only the literal form and reported
ten *working* labels as dead. **A gate that cries wolf gets switched off, which
is worse than not having one** - so when a new check disagrees with something you
have seen working in game, the check is wrong until proven otherwise.

Then prove the gate fails. Rename one binding, watch it go red, put it back. A
check that cannot fail is not a check.

## Read this first: seven things that will bite

**1. CLIP takes 77 tokens and truncates the rest SILENTLY.** The first icon batch
sent 161. Every isolation clause - "single object", "plain grey background", "no
text" - was cut before the model saw it, and four prompts came back as scenes and
pattern wallpaper. One warning line in a log was the only sign. `kaggle_run.py` (in `roblox-3d-model`)
now refuses to push an over-budget prompt, and the framing that decides usability
goes in the prompt HEAD, ahead of the subject.

**2. The Kaggle client RETURNS errors, it does not raise them.**
`dataset_create_new` on an existing dataset returns `status="error"` and the old
code caught only exceptions, so the fallback to `dataset_create_version` never
ran and the dataset sat on version 1 forever. Every reroll silently regenerated
the FIRST batch's prompts, on time, looking plausible. Prompts now carry a
`batch_id`, the kernel echoes it, and `fetch` refuses a mismatch.

**3. `ClipsDescendants` does not clip ROTATED descendants.** The angled chevron
header in every second Roblox UI reference is this trap. It lints clean, exits 0,
and throws diagonal bands across the viewport. Use a `UIGradient` hard
transparency step instead. Construction: draw the
angle as a gradient on the unrotated element, never as a rotated child inside a
clipping parent.

**4. Do not chroma key a generated icon.** Keyers compare Cb/Cr and magenta
shares the Cr axis with red, so a magenta key eats the reds and pinks that fill
an icon set. Generate on flat grey and flood fill from the border instead: this
style has a thick opaque outline, so the fill stops dead at the artwork.
`icon_cutout.py` does it.

**5. A dark stroke of 4 is a HEADING value.** Applied to 24px brown body text on
a cream panel it reads as mud. `textStroke` is explicit per label, and 0 is the
right answer for small dark text.

**6. THE PNG AND THE .model.json CAN AGREE ON EVERY VALUE AND STILL DISAGREE ON
ARRANGEMENT.** This is the one real limit of the "same tree" guarantee, and every
instance of it was found by a Studio render, never by the preview:

- Shadow and Face as SIBLINGS meant a `UIListLayout` gave each shadow its own
  cell - four tabs rendered as eight. Each element is now wrapped so the wrapper
  is the single layout item.
- The decorative `Highlight` frame inside a laid-out face claimed a slot and
  shoved price text out of its button. `UICorner`/`UIGradient`/`UIStroke` are not
  `GuiObject`s so layouts ignore them; only a Frame is caught.
- No `LayoutOrder` meant a grid came back in arbitrary order.
- `TextScaled` fills the whole label box while the renderer uses
  `height * textScale`, so Studio text ran large until a `UITextSizeConstraint`
  capped it.

- `TextScaled` **does not overflow, it SHRINKS** - without limit. So the symptom
  of text that does not fit is never text outside a frame, it is text that has
  quietly become unreadable. The renderer now shrinks to fit exactly as Roblox
  does, and `verify_ui`'s `text_fit` check measures how far each label had to
  shrink and fails below 55% of its designed size or 11pt on the worst device.
  It caught three on the first run, all descriptive text sized for a monitor.

**Render one page in Studio before trusting a set of them.**

**7. Never replace a directory inside a cloud-synced folder.**
`mv` plus `cp -r` made the sync client write conflict copies named
`<file>-<machine name>.png` holding the NEW images while the OLD files kept the
canonical names. 37 icons updated, 4
silently did not, and it surfaced only as two stale icons in a screenshot. Copy
file by file.

---

## Workflow

### 1. Icons

Every icon in this skill is generated or drawn by the skill itself (no third-party icon pack is needed). A page builds before any icon exists: an `icon` element with no matching PNG is skipped in the preview and carries a named placeholder in the emitted tree.

**Generate on Cloudflare, not on a GPU.** Measured on the same prompts:

| | Kaggle / SDXL | Cloudflare / FLUX.1-schnell |
|---|---|---|
| Per icon | 59s | **1.2s** |
| 33-icon set | ~40 min | **~40s** |
| Rejected by the checks | 12 of 38 | **0 of 33** |

The reason is hardware, not prompting. Kaggle hands out a Tesla P100 (sm_60,
2016) or a T4, with no way to choose, and **neither supports bf16** - which every
current model is built around. A 12B FLUX-class model dies with CUDA OOM on that
card even with CPU offload. Cloudflare runs it on their hardware and returns a
PNG.

    python scripts/gen_icons_cf.py --manifest <your icons manifest>.json         --out <project>/_cf_raw
    python scripts/icon_cutout.py --in <project>/_cf_raw --out <project>/icons         --size 256 --sheet <project>/icons_sheet.png
    python scripts/glyphs.py --out <project>/icons --size 256
    python scripts/upload_icons.py --icons <project>/icons --map <project>/icons.json

`references/icons.example.json` shows the manifest format (a shared `style`
anchor plus one short subject prompt per icon). Needs `CF_ACCOUNT_ID` and
`CF_API_TOKEN` (Account > Workers AI > Read). The
budget is **10,000 neurons/day**, and the MEASURED cost is **~141 neurons per
1024px 4-step image**, so about **70 images/day**. The published per-tile formula
predicts 57.6 and is 2.4x optimistic - trust the dashboard, not the price list.

Two operational facts: the endpoint takes **only `prompt` and `steps`** (width,
height and seed return HTTP 400, so there is **no seed** and a reroll is a real
reroll), and the safety filter throws false positives - "one metal grain silo
tower" came back NSFW, which needs a **reword, not a retry**.

Then **look at the sheet**. The check that matters is `extra_objects`: image
models pluralise small nouns, and a sheet of seven chickens passes every colour
statistic ever written. A multi-object generation is CROPPED to the best object
plus anything clustered with it, and flagged `SALVAGED` so it gets looked at.

**SYMBOLS ARE DRAWN, NOT GENERATED**, and that held for every model tried.
`glyphs.py` draws close, tick, heart, star, lock, plus, minus and arrow with a
dilation-based uniform outline. Generated attempts returned a scribble for the X,
a down-arrow for the tick and a games controller for the heart. Geometry is not
an image-generation problem, and a drawn set is consistent by construction.

Kaggle is OFF for everything, icons and meshes alike (see the notice at the top):
its terms ban this use. Use the Cloudflare route above.

### 2. Pages

Write a small spec generator (a Python script that builds the dicts with
`scripts/ui_kit.py`), not five hand-edited JSON files. A typical set is five
pages: HUD, shop, inventory, quests, settings.

```bash
python scripts/ui_build.py <your spec>.json --out mockups --icons icons
# builds all three outputs; pass --png / --model / --luau to build only some
```

Elements: `panel`, `button`, `frame`, `label`, `icon`. Containers take
`layout: {type: list|grid, ...}`, `padding` and `aspect`. Sizes and positions are
UDim2 `[sx, ox, sy, oy]` with an `anchor` - Roblox's rules, not CSS.

Every `panel` and `button` expands to **the depth stack** automatically: a shadow
offset down in a darker, hue-shifted-toward-blue colour, a face with a top-lit
`UIGradient` at rotation -90, and a dark outer `UIStroke` of identical thickness
everywhere. That stack is the whole difference between flat and professional in
both community guides, and it is not a per-element decision.

The guides' **inset bright highlight is OFF by default**. It reads as a lit
edge on a saturated Figma button and as a second border with a visible gap in
Roblox; on cream panels it looked like white lines drawn on everything. The
gradient already carries the top-light. Re-enable per element with
`highlight: true`, or theme-wide.

### 3. Into Studio

Paste `Page.lua` into `execute_luau`, then `capture_screenshot`. A `ScreenGui`
under `StarterGui` renders live in the viewport, so the UI is checkable in EDIT
mode with no playtest: the viewport renders a `ScreenGui` under `StarterGui` live,
so drive the real controller into it and screenshot. Clear the injected
instances afterwards so the saved place carries no drift.

Icons still need real asset IDs. `to_instances` emits
`rbxassetid://ICON_<NAME>` placeholders - upload with `roblox-3d-model`'s
`upload_asset.py` as **assetType Image, never Decal** (a Decal wraps an image and
has a different id; assigning it renders nothing, with no error), then
substitute.

---

### 4. Responsiveness

Pages are authored at a **reference resolution in offset** - which is how the
guides build, and what keeps a design predictable - and mapped to the player's
viewport by **one `UIScale` on the CanvasFrame**, driven by
`references/UIController.client.lua` from `ViewportSize`.

There is deliberately **no floor** on that scale. A floor of 0.60 was tried and
was the wrong lever: it made the page render at 768x432 on a 640x360 phone, so it
stopped FITTING, which is worse than being small.

Touch targets are protected at the source instead. 44pt on a 640x360 phone means
**88px at a 1280x720 reference**, so `ui_kit.TOUCH_H` is 88 and every interactive
control is sized from it. That is what "mobile first" actually costs, and it is
why the shop TILE is the button rather than a small pill inside it.

`verify_ui.py` evaluates every page at four real viewports (640x360, 896x414,
1024x768, 1920x1080), applies the scale, and fails anything under the minimum
with the exact px it needs. Run it before believing a page works anywhere but
your monitor.

---

## Layout hygiene: the three things a human notices in one second

These are the complaints a player makes about a UI that passed every other check
on this list, and they are now enforced by `verify_ui.py` rather than left to
taste. They are measured on the RESOLVED rectangles at the reference resolution,
not read off the property tree, because every one of them is a rendering fact.

**1. ELEMENTS MUST NEVER TOUCH.** Minimum 8px between siblings at the reference
resolution; an overlap is a failure, a gap under 8px is a warning. Two controls
with no space between them read as one control with a line through it, and at the
smallest supported scale a 1px gap is a 0px gap. Anything meant to sit on top of
something else - a sweep over a cooldown dial, a value over a bar - declares
itself with `"overhang": true`, so that "these overlap" always means either a bug
or a decision somebody wrote down. Checks: `sibling_overlap`, `sibling_gap`.

**2. CENTRED IS A MEASUREMENT, NOT A PROPERTY.** An element that asks to be
centred has its rendered centre compared against its parent's, to 1.5px. The
classic Roblox bug is a `0.5` scale position with no `0.5` anchor: the element
lands **half its own size** off centre, which looks almost right, and it is
exactly the error the checker names when it sees it. Never eyeball centring off a
mockup - the mockup is drawn from the same numbers that are wrong. Check:
`off_centre`.

**3. NO BOX DRAWN AROUND A CONTROL.** A frame that exists only to position
something must be `"transparent": true`. An opaque container hugging one child -
within 6px on every side - is not a container, it is an outline nobody asked for,
and it is the box-around-a-button defect. The same
applies to a bar's track hugging its fill. If a control needs a visible border,
that is a stroke or a padded panel with a stated padding, not an accidental
wrapper. Check: `wrapper_box`.

**A note on what these checks cost.** They fire on layouts that were signed off
by eye and by every other gate, which is the point - but a warning is not a
licence to widen every gap to 8px mechanically. Read what it names, then either
fix the spacing or declare the overlap. What is not acceptable is leaving it
unexamined because the page "looks fine" in the mockup at 1280x720.

## Iterate on `verify_ui.py`, not on the mockup

The mockup PNG is for a human and for sign-off. It is not the iteration loop:
an image is re-sent on every later tool call in the same context, so re-opening
it after each tweak is the most expensive way to ask a question the checker
already answers in text. `verify_ui.py` names the element, the number and the
rule it broke. **Fix against the text, then look at the PNG once, when the page
is done.**

This is not a licence to skip the look. The checker cannot see taste, colour
weight, or whether a screen reads at a glance - and it is drawn from the same
resolved tree as the layout, so it agrees with the layout by construction. One
honest look at the end, at the reference resolution.

## Non-negotiables

- **Scale, not Offset**, for size and position. The exception is
  `UIStroke.Thickness`, which genuinely has no scale.
- **Touch targets 44pt minimum.** Action buttons 70x70 on small screens.
- **Keep the thumbstick zone (bottom left), the jump zone (bottom right) and the
  36px top bar clear.** Put a hotbar bottom-CENTRE for exactly
  this reason.
- **One frame per page**, transparent, so a scripter toggles one `.Visible`.
- **`UIAspectRatioConstraint` inside grid cells**, or tiles distort.
- **Stroke thickness identical across the screen.** Mixed weights is the single
  clearest tell of beginner or generated UI.
- **Text must fit its box at a legible size**, checked by `text_fit`. Do not
  "solve" a long string by shrinking the label; widen the box or shorten the text.
- **Never hardcode a text colour.** Use `ink`, `inkSoft`, `onDark` from the theme.
  A test on a dark theme produced perfect layout with invisible item
  names because one component had a light-panel brown baked in.
- **Green price buttons, with the currency icon on them.** A convention, not a
  preference.
- **Nothing touches, everything that says it is centred is centred, and no frame
  draws a box round its child.** See "Layout hygiene" above - three checks, all
  enforced.

---

## Themes: writing your own theme file

A spec's `"theme"` is either an inline object or a path to a JSON file, resolved
relative to the spec. `references/theme.json` is the default and the template to
copy. Every value in it is read by the renderer and the emitter from the one
file, so changing it restyles the PNG and the `.model.json` together.

| Key | Meaning |
|---|---|
| `stroke` | Outer `UIStroke` thickness on panels and buttons (default theme: 5) |
| `textStroke` | Default text stroke (4); override per label, 0 for small dark text |
| `corner` | Corner radius as a scale (0.2) |
| `shadowOffset` | Pixels the depth-stack shadow sits below the face (7) |
| `outline` | Hex colour of every stroke |
| `backdrop` | Preview-only ground: one hex, or two hexes for a vertical gradient |
| `backdropImage` | Optional preview-only screenshot of your game world to judge the UI over; never emitted |
| `palette` | Named colours (`panel`, `gold`, `green`, `ink`, `onDark`, ...). Elements refer to them by name; never hardcode a text colour |
| `font`, `fontStyle` | `FredokaOne` (default, bundled), `BuilderSans`, `SourceSans`, `Merriweather`, `Montserrat`. Only Fredoka previews exactly; the others fall back to a system font in the PNG and Studio is truth |
| `flat` | `true` emits solid fills instead of the top-lit gradient |
| `highlight` | `true` turns the inset highlight on theme-wide |
| `motion` | Hover, press and open-style numbers, emitted as attributes and played by `references/UIController.client.lua` |

Panels take `alpha` for translucency.

**Surfaces carry a PATTERN layer, not just a gradient.** `scripts/patterns.py` draws
sheen, stripes, dots, clouds and grain; any panel/button/frame takes
`"pattern": {name, colour, opacity, tile, fade}`. Leaving it out is why a UI built
from shapes alone reads flat. Upload `pattern_*.png` with the icons. A patterned
surface moves its children into a `Content` frame so a layout never grabs the
pattern.

**Motion is data too.** A theme's `"motion"` block (hover scale/rotate/time/style,
press scale/time, page open style) is emitted as attributes and played by
`references/UIController.client.lua`. Many games open menus INSTANTLY and put the
motion on buttons and content. The PNG cannot prove motion - playtest it.

## References

- `references/ui-recipes.md` - the measured numbers, the depth stack, page
  composition, and the sources
- `references/icons.example.json` - an example icon manifest showing the prompt
  budget and the shared style anchor
- `references/theme.json` - the default theme, the template for your own
- `references/fonts/` - Fredoka and Fredoka One, used by the renderer. These font
  files are licensed under the SIL Open Font License (OFL) and may be redistributed.

## `verify_labels.py` - the dead-label gate

```bash
python verify_labels.py --ui src/ui --client src/client
```

Every label carrying the placeholder sentinel must be named by some controller,
or the build fails. This is the gate for the placeholder rule at the top of this
file, and it is proven to fail: rename one binding and it goes red.

It understands two shapes of reference - the literal (`"AmmoCount"`) and one
ASSEMBLED from a row index (`` `BankRow{i}` .. "Name" ``), because a first
version understood only the literal and reported ten WORKING labels as dead.
`--sentinel` overrides the default `<unbound>`; whatever you choose, it must be a
string the live code can never produce.
