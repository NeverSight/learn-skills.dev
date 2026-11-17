---
name: unity-asset-designer
description: "Create the reference artifacts that keep Unity game assets on-model before production generation. Use for recurring characters/mascots, model turnarounds, canon sheets, icon/item/prop families, style guides, art bibles, palette or silhouette drift, mismatched character tokens/app icons, or making assets look like one world. Defines palette, shape language, shading, lighting and anti-style; produces multi-view/expression/color-callout sheets and coherent family sheets; conditions downstream image/3D generation on those references; and runs silhouette, at-size, palette, line-weight and shading consistency QA. Feeds unity-image-generator, unity-pixel-art, unity-3d-generator, unity-ui-designer and the art-spec."
---

# Unity Asset Designer

The **art-direction and consistency front-end** to the asset generators. It does NOT call image/3D APIs or import into Unity — those are owned by `unity-image-generator` and `unity-3d-generator`. It decides **what reference sheets to make, how they pin the look, and how every production asset conforms to them**, then hands concrete prompts + reference images down to the generators. Its job is to make a game's art look like it belongs to **one world**.

## Why this skill exists (the real failure it prevents)

In a reference casual game, the look churned through many passes and **a recurring mascot character had to read as a small board token, a menu mascot, and the app icon** — with no single visual reference all three conformed to, they drifted, icons drifted, and "make it look pleasing" was re-guessed every pass (see `unity-game-director` Step 2.6). The fix is a **reference-sheet-first** workflow borrowed from studio production: lock the visual DNA once, draw each character on a turnaround sheet that becomes canon, generate icon/item sets in one uniform pass, then derive every production asset by **conditioning on the sheet** instead of generating from scratch. Without unified rules for color, proportion, and lighting, assets "drift apart within a month" ([aeno art bible](https://www.aeno.nl/uploads/Art-bible.pdf), [GameDev.net — what is an art bible](https://gamedev.net/forums/topic/644435-what-is-an-art-bible-and-any-tips-to-make-one-better/)).

## Where it sits in the skill stack (read these; do NOT re-explain their domains)

- **Up:** `unity-game-director` Step 2.6 produces the **named aesthetic north-star** (reference style + touchstones, 4–7 color palette, type family, mood + anti-mood, flat/glossy finish) as an early deliverable. THIS skill *operationalizes that north-star* into concrete, reusable reference sheets. If the north-star isn't pinned yet, send the user back there first — don't invent it here. `unity-art-direction` owns the machine-readable `art-spec.yaml` single-source-of-truth + 12-preset style library + mobile art budgets, and this skill produces the on-model reference/turnaround sheets that its golden-asset/family production pipeline calls for.
- **Down (2D):** `unity-image-generator` owns the Gemini API mechanics + Unity 2D import (Sprite mode, PPU, atlas, ASTC). THIS skill hands it ready-to-run prompts + reference images; it imports and slices.
- **Down (3D):** `unity-3d-generator` owns Tripo + the ModelImporter pipeline. **A turnaround sheet IS the ideal image input for image-to-3D** — hand the front/side/back views to it.
- **Sideways:** `unity-ui-designer` owns UI **design tokens** (typography scale, semantic color roles, radii). All color hexes come from `art-spec.yaml:palette.roles`; `GameTheme.cs` and the UI color tokens are **runtime derived views of art-spec.yaml** — the only style SSOT (colors must equal the spec hexes; typography/spacing/radii are GameTheme-native). Regenerate them from the spec; never hand-agree a second palette.

Load `unity-game-director/SKILL.md` (north-star) and the relevant generator SKILL before producing prompts, so handoffs are clean.

## The methodology (ordered — top of the funnel down to a Unity asset)

Build the funnel **top-down once**, then generate production assets bottom-up many times. Each upstream artifact is the reference for everything below it.

### 1. Lock the visual DNA in art-spec.yaml — express it ONCE (style guide is a derived view)

From the director's north-star, lock the visual DNA **in `art-spec.yaml`** (owned by `unity-art-direction`; canonical path `Assets/<Game>/Art/_ArtDirection/art-spec.yaml`). If the spec exists, READ it — never re-derive style; if a field below is missing, WRITE it into the spec (palette roles/ramps, `shape_language`, `craft.light_direction`, lighting) — not into a competing document. `style-guide.md` is regenerated FROM the spec as a readable derived view. Not adjectives — testable rules. An art bible records the art decisions so later work can check them and stay consistent ([GameDev.net](https://gamedev.net/forums/topic/644435-what-is-an-art-bible-and-any-tips-to-make-one-better/)). Required fields:

- **Palette** — 4–7 named colors with **semantic roles** (ground, panel, ink/text, 1–3 accents) + the decorative/region palette kept separate, each with hex + a contrast intent. Written to `art-spec.yaml:palette.roles` (+ `palette.ramps` for pixel games). `GameTheme.cs` / `unity-ui-designer`'s color tokens are runtime **derived views of art-spec.yaml** (the only style SSOT; colors must equal the spec hexes) — regenerate from the spec, never fork.
- **Shape language** — round/soft vs sharp/angular, and what it signals (round = friendly/approachable; sharp = tense/dangerous). Shape language drives gameplay readability and instant recognition ([pixune — shape language](https://pixune.com/blog/shape-language-technique/), [80Level — shape language & readability](https://medium.com/@EightyLevel/character-design-shape-language-and-readability-6ee4bb6f98a6)).
- **Shading model** — flat / cel / soft-gradient / painterly — **decide once** (a reference game flip-flopped glossy↔flat for want of this). State outline rule (none / uniform N-px dark outline) and line weight.
- **Lighting direction** — one named key direction (e.g. "single soft light from top-left, no rim") so every asset is lit the same; write it to `art-spec.yaml:craft.light_direction` (composition.yaml's `key_light_direction` must equal it). Lighting is the main tool for mood; inconsistent lighting is the fastest drift ([aeno art bible](https://www.aeno.nl/uploads/Art-bible.pdf)).
- **Mood + anti-mood** — 3–5 words for each (e.g. "calm, minimal, high-contrast" or "bold, energetic, gritty" / NOT "busy, glossy, desaturated, cluttered"). The anti-mood is what stops the next generation from drifting.
- **(Upstream optional) mood board / color script** — a small reference set pins tone/palette/texture before any asset is made ([Milanote game-design moodboard](https://milanote.com/guide/game-design-moodboard), [StudioBinder video-game mood board](https://www.studiobinder.com/blog/video-game-mood-board/)); a color script maps how color is used across the game's surfaces/states ([RodTejada — moodboard & color script](https://rodtejada.wordpress.com/2010/10/30/the-moodboard-and-color-script/)). For a small casual game the north-star + style guide usually suffice; add a generated **style tile** (one small image showing palette + a sample object in the locked style) to use as the literal reference image in step 4.

Output: updated `art-spec.yaml` (the SSOT every prompt below cites) + `style-guide.md` regenerated from it + optionally a generated **style tile** PNG, registered in the spec's `conditioning.style_anchor_images` so generators auto-attach it.

### 2. For each recurring CHARACTER / mascot: generate a MODEL / TURNAROUND SHEET first — treat it as canon

Before the character appears anywhere, make its sheet, freeze it, and REGISTER it: save to `Assets/<Game>/Art/_ArtDirection/sheets/<char_id>_canon.png` and write `characters.<id>.canon_sheet` + `characters.<id>.identity_string` (a FROZEN verbatim description — later prompts vary only pose/action clauses) into `art-spec.yaml`. An unregistered sheet is invisible to the generators and to session N+1. A turnaround/model sheet is the **single source of truth** for a character's appearance — it keeps proportions, details, and style consistent across every later use and every artist/generation ([21-draw — character design sheet](https://www.21-draw.com/how-to-make-a-character-design-sheet/), [CharacterHub — model sheets](https://characterhub.com/blog/character-resources/character-design-sheet), [spines — character turnaround](https://spines.com/character-turnaround/)). Put on the sheet:

- **Multi-view turnaround** — front, 3/4, side (profile), back (3–6 angles), aligned on shared horizontal guides (head height, eye line, shoulder) so the character matches across views.
- **Expression sheet** — a few extreme + subtle expressions (idle/happy/win/think) if the character emotes in-game.
- **Proportion / height callouts** — head-count height, key landmark lines.
- **Color callouts** — a swatch key of every color used, with role labels, tied to the style-guide palette.
- **Do / don't notes** — the on-model rules ("ears always rounded; never add a nose ring; outline stays uniform 4px") — these are what you check against in QA.

**Illustrative example:** make ONE **mascot model sheet** that shows the character as it must read at every use — as the small **board token** (6–9 cell px), as the **menu mascot** (circle header), and as the **app-icon** crop — all on the same sheet, same palette/shape/shading, with proportion + color callouts. That single sheet is what was missing when the token, mascot, and icon drifted.

Hand this sheet down two ways: as the **reference image for 2D derivation** (step 4) and, if the character becomes 3D, as the **image input to `unity-3d-generator`** (its image-to-3D wants exactly these orthographic front/side/back views).

**Pixel track (`craft.finish: pixel`): do NOT produce the canon with the Gemini turnaround workflow above** — pixel finals are PixelLab-only. Pixel canon = the approved PixelLab anchor plus its `rotate`-derived directional views composited into one sheet PNG at the same canon path (a 3-line PIL paste; for a single-view game the approved anchor alone, copied to the canon path, is the blessed canon). See `unity-pixel-art` step 4; register `canon_sheet` + `anchor_sprite` + `identity_string` in the art-spec `characters` block exactly as above.

### 3. For SETS of items / icons / props: generate an ITEM / ICON SHEET in a SINGLE pass

Never generate set items one at a time — they drift in scale, lighting, palette, and line weight. Generate the **whole set as one image / one grid in a single pass** so every cell shares lighting, palette, perspective, and stroke. Set-consistency rules (from icon-system practice): one **grid/base size**, one **stroke weight** across the set, one **corner-rounding**, one **palette**, and judge **at the size users see, not zoomed in** ([Material icons — style](https://m1.material.io/style/icons.html), [Flaticon — visual consistency](https://www.flaticon.com/blog/visual-consistency/), [DEV — app-icon consistency](https://dev.to/albert_nahas_cdc8469a6ae8/how-to-maintain-visual-consistency-across-your-app-icons-14ac)). Anything below ~20px loses detail — simplify ([uxplanet — practical icon design](https://uxplanet.org/practical-guide-to-icon-design-794baf5624c8)). Only **after** the sheet looks uniform do you slice/derive the individual assets (slicing/atlas mechanics are `unity-image-generator`'s job).

**Illustrative example:** make ONE **icon item sheet** with hint / clear / menu / leaderboard / settings (and hearts, star) in a single pass — same line treatment, same fills, same optical size — instead of the icon-by-icon churn that drifted. A `ProceduralIcons.cs` already enforces this in code (one SDF style, white-on-transparent, tinted at use); the sheet is the generated-art equivalent and the spec the procedural set conforms to.

### 4. Generate individual PRODUCTION assets by CONDITIONING on the sheet — not from scratch

Each production asset is derived by giving the image model the **sheet/style tile as a reference image** plus a **style-pinning prompt**, so it matches instead of reinventing. Modern image models (Gemini "nano-banana" family) fuse reference images with the prompt and support **role-tagged inputs** and **style-locking**: state each image's job ("use Image A for the character identity, Image B for the art style"), and reuse **verbatim style tokens** every time — if you said "emerald eyes / flat cel shading / single top-left light," do not paraphrase next time ([Google — Nano Banana Pro prompting](https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/), [Google Cloud — ultimate Nano Banana prompting](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)). Practical on-model rules:

- **Always pass the canon references as input images.** `unity-image-generator`'s `generate_image.py` accepts repeated `--input-image` with paired `--input-role` labels (`-i <canon_sheet> --input-role "character identity" -i <style_tile> --input-role "art style"`), or `--character <id>` to attach the art-spec canon sheet + frozen identity_string automatically; running with `--art-spec` also injects the spec's verbatim style paragraph. Then pin style in words: *"in the exact same style as the reference: [your full style token — shading model, palette, outline rule, light direction, shape language]."* Paste the token verbatim; never paraphrase it.
- **Lock the vocabulary.** Keep a short "style token" string in the style guide and paste it into every prompt unchanged. Drift usually comes from re-describing the look in new words.
- **Reuse the seed** when the model exposes one, for near-identical re-rolls of the same asset.
- **Identity reminder** in iterative/multi-turn edits: "use the same character identity / same art style as the previous image" ([chatsmith — consistent characters](https://chatsmith.io/blogs/ai-guide/using-gemini-nano-banana-consistent-characters-ai-images-00037)).
- Reality check: consistency "may vary" across edits even with references ([Google blog](https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/)) — which is exactly why step 5 is a gate, not a formality.

Copy-pasteable templates for all four artifacts live in **`references/prompt-templates.md`**.

### 5. Consistency QA — a reject-and-regenerate GATE (not a glance)

Before any asset is accepted, check it against its sheet and the style guide. Fail → re-prompt with a sharper style pin or a tighter crop of the reference, don't accept drift. Gates:

- **Silhouette test** — fill the asset solid black, remove interior detail: is it still recognizable and distinct? Iconic silhouettes read in **under ~0.5s**; if it's mush, fix the shape ([Disney — silhouette test PDF](https://www.waltdisney.org/sites/default/files/2020-05/T&T_Silhouette-final2.pdf), [Inviox — silhouette recognition timing](https://www.invioxstudios.com/blog/how-long-it-takes-for-players-to-recognize-a-character-silhouette), [bigredillustration — silhouette importance](https://bigredillustration.com/articles/importance-of-silhouette-in-character-design/)).
- **At-size readability** — view at the real in-game size (board token ~6–9 cells, icon ~24–44px, app icon thumbnail), NOT zoomed in. Below ~20px, less detail wins ([uxplanet](https://uxplanet.org/practical-guide-to-icon-design-794baf5624c8), [Material icons](https://m1.material.io/style/icons.html)).
- **On-model match** — palette (only style-guide colors), line weight, shading model, lighting direction all match the sheet; honor the sheet's do/don't notes.
- **Contrast** — subject reads on its actual ground (tie to the palette's contrast intent; e.g. dark ink on a light ground).
- **Set uniformity** (for item/icon sets) — lay every item side-by-side: same optical scale, stroke, palette, perspective. One outlier = regenerate the set, not the outlier (it'll never match).

Automate what can be automated: `unity-image-generator/scripts/critique_image.py <asset> --reference <canon_sheet> --art-spec <spec>` scores `on_model_vs_reference` (the judge SEES the canon), and `validate_sprite.py --art-spec` (+ `--palette-mode exact` for hard palette locks) checks the palette deterministically. A short rubric + the reject-loop checklist is in **`references/consistency-qa.md`**.

### 6. Handoff to the generators for production + Unity import

- **Pixel-art 2D:** pass the style guide / anchor brief to `unity-pixel-art` → it uses PixelLab for final native-canvas sprites/sheets, then imports with Point/no compression/no mipmaps/pixel-perfect settings. Gemini may explore concepts only.
- **Non-pixel 2D:** pass the final prompt + reference image to `unity-image-generator` → it generates, then imports (Sprite mode, PPU, FilterMode, ASTC for iOS) and slices sheets via the Sprite Editor / atlas. Sprite-sheet/atlas consistency (uniform cell size, packed into one atlas to cut draw calls) is its concern — your job was only that the source grid is *visually* uniform.
- **3D:** pass the turnaround sheet (front/side/back) to `unity-3d-generator` as the image-to-3D input → it runs Tripo, downloads to `Assets/`, and configures the ModelImporter.
- **Rigged characters:** a turnaround for a character that will be **rigged** must be in a **T-pose/A-pose** (full body, limbs separated, no occluding props) — that's the rigging-ready canon; action poses break Tripo's auto-rig (see `unity-3d-generator` → "Riggable characters need a clean full-body T-pose"). Author the action (draw/attack) as animation clips later, not in the sheet.
- **Motion routing:** pixel-art animation sheets go to `unity-pixel-art` / PixelLab anchor-first. Non-pixel animated assets go to **Tripo** (`unity-3d-generator`: rig + animate; pre-render only for high-res/painterly 2D). Gemini reference/turnaround sheets are references/static art only; frame-by-frame Gemini drifts and is fallback/concept only.
- **UI:** confirm the shared palette matches `unity-ui-designer`'s tokens before icons land in the HUD/menu.

## When to invoke this skill

- A game has a **recurring character/mascot** that appears in more than one form (token + mascot + icon).
- You need a **family of icons / set of items/props** that must look uniform.
- Art is **drifting** (the recurring failure): icons don't match, the character looks different per use, art palette ≠ UI palette.
- Before a **batch art generation** run — make the sheets first so the batch conditions on canon.
- NOT needed for a one-off background plate or a single decorative sprite with no siblings — go straight to `unity-image-generator`.

## Deliverables checklist (what "done" looks like)

- [ ] **art-spec.yaml fields locked** (palette roles/ramps, shape language, shading model + outline/line-weight, `craft.light_direction`, mood + anti-mood) with `style-guide.md` regenerated as a derived view. Optional style tile PNG registered in `conditioning.style_anchor_images`.
- [ ] **Model/turnaround sheet** per recurring character (multi-view + expressions + proportion + color callouts + do/don't), frozen as canon AND registered in the art-spec `characters` block (`canon_sheet` + frozen `identity_string`). (e.g. one mascot sheet covering token + mascot + icon.)
- [ ] **Item/icon sheet(s)** generated single-pass, uniform, before slicing. (e.g. hint/clear/menu/leaderboard/settings in one set.)
- [ ] Production assets derived by **conditioning on the sheet** (reference image + locked style tokens), not from scratch.
- [ ] **Consistency QA** passed: silhouette + at-size + on-model + contrast + set-uniformity, with a reject-and-regenerate loop.
- [ ] **Palette agrees with `unity-ui-designer` tokens** (both derived from `art-spec.yaml:palette.roles` — regenerate from the spec on mismatch).
- [ ] Handed concrete prompts/reference images to `unity-image-generator` / turnaround to `unity-3d-generator`; they own generation + Unity import.

## Final response (what to report)

State: the style guide (palette + shape + shading + lighting + mood/anti-mood) you locked; each sheet you produced and that it's frozen as canon; which production assets were derived by conditioning on a sheet (with the reference image used); the QA results (silhouette / at-size / on-model / contrast / set-uniformity, and any reject→regenerate); confirmation the palette matches the UI tokens; and the exact prompts/reference images handed off to which generator. Don't claim a generated asset exists unless `unity-pixel-art`/`unity-image-generator`/`unity-3d-generator` actually produced it — this skill produces the *plan and the conditioning*, the generators produce the *pixels/mesh*.

## Field notes & lessons

- **Rewired onto the art-spec SSOT (deep-review R1/R13).** Step 1 now reads/writes `art-spec.yaml` (style-guide.md, `GameTheme.cs`, UI tokens are runtime views DERIVED from it); step 2 registers every canon sheet + frozen `identity_string` in the spec's `characters` block at `_ArtDirection/sheets/`; step 4 hands generators repeated `--input-image`/`--input-role` (or `--character <id>`) now that `generate_image.py` supports multi-reference conditioning; the QA gate gained automated teeth (`critique_image.py --reference` on-model axis, `validate_sprite.py --palette-mode exact`). STYLE TOKEN placeholders in `prompt-templates.md` are filled from art-spec fields — the former hardcoded "round friendly shape language" + blanket NOT-list are gone (they violated image-generator's style-neutrality law).
- Created. The art-direction & asset-consistency layer above the generator skills, motivated by a reference game's real visual-consistency churn (the mascot as token vs mascot vs app icon drifting; icon-by-icon drift; art↔UI palette mismatch; "pleasing" re-guessed every pass). Defines the reference-sheet-first funnel: lock a **style guide / art bible** (palette w/ semantic roles shared with `unity-ui-designer` tokens, shape language, shading + line weight, lighting direction, mood + anti-mood) → **character model/turnaround sheets** as on-model canon (multi-view + expressions + proportion + color callouts + do/don't; a turnaround is also the image-to-3D input for `unity-3d-generator`) → **item/icon sheets in one pass** for set uniformity → derive production assets by **conditioning on the sheet** (Gemini/nano-banana reference-image + style-locking, verbatim style tokens, seed reuse) → a **consistency-QA gate** (silhouette <0.5s read, at-size readability, on-model palette/line/shading/lighting, contrast, set-uniformity; reject-and-regenerate) → handoff to `unity-image-generator` (2D + import/slice/atlas/ASTC) and `unity-3d-generator` (image-to-3D). Operationalizes `unity-game-director` Step 2.6's north-star; cross-references the UI design-token palette. Ground examples: a mascot model sheet (token+mascot+icon on-model) and an icon item sheet (hint/clear/menu/leaderboard/settings). Added `references/prompt-templates.md` (style-guide, character-sheet, item-sheet, derive-one-asset prompts) and `references/consistency-qa.md` (rubric + reject loop). Sources: art-bible/style-guide practice (aeno, GameDev.net, dusthandler Art_Bible); character model/turnaround sheets as single source of truth (21-draw, CharacterHub, spines); icon-set consistency (Material, Flaticon, uxplanet, DEV); silhouette/readability (Disney, Inviox, bigredillustration); shape language (pixune, 80Level); mood board/color script (Milanote, StudioBinder, RodTejada); Nano Banana reference-image/style-locking prompting (Google blog, Google Cloud, chatsmith).
