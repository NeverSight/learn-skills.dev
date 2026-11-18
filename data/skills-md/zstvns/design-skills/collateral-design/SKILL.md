---
name: collateral-design
description: "Apply a brand's defined visual system to any fixed-format piece that isn't a website — decks and presentations, one-pagers and sales sheets, social posts and graphics, blog/OG thumbnails, business cards, brochures, flyers, posters, banners, billboards, and paid ads. Use when the user mentions 'design a deck,' 'pitch deck,' 'sales deck,' 'presentation,' 'slides,' 'one-pager,' 'sales sheet,' 'leave-behind,' 'social post,' 'social graphic,' 'blog thumbnail,' 'OG image,' 'business card,' 'brochure,' 'flyer,' 'poster,' 'banner,' 'billboard,' 'print,' 'ad creative,' 'display ad,' 'collateral,' or wants a branded document or graphic that isn't a website. Mostly screen-first; print is one destination among many. Ships as a true-size viewer plus real exports."
metadata:
  version: 1.13.0
---

# Collateral Design

You apply a brand's **defined visual system** to the collateral family: **decks, one-pagers, print pieces, and ads.** This is an Application skill — the color roles, type rules, motif, and mark from `creative-direction` and `logo-design` become finished, fixed-format artifacts. It sits beside `web-design`: same identity, different mediums.

Read `design-principles` first. Everything here is that skill meeting a page that can't scroll, can't reflow, and often can't be revised after it ships. Hierarchy is the job; restraint protects the message; coherence is *not* repetition — a deck, a sell sheet, and a feed ad can each look different and still be unmistakably one brand.

> **Position in the sequence:** after `creative-direction` (the system), `logo-design` (the mark), and alongside `web-design` — an Application skill. It **consumes** the identity; it does not define one. The medium is not one surface but a *family* of fixed-format deliverables, each with hard constraints web doesn't have: a set trim size, a projector's contrast floor, a thumbnail's legibility, a fold that reorders reading — and **no second chance**. The piece lands in one shot or not at all.

## The Thing That Makes Collateral Different

Web reflows, responds, and ships in commits you can revise tomorrow. Collateral does none of that. Three constraints run through every format here and shape every decision:

- **Fixed format.** A 16:9 slide, a US-Letter sheet, a 1080×1350 ad, a tri-fold's panel — the frame is set before you start, and the content is designed *to* it, not poured into whatever height it needs.
- **One shot.** No hover to reveal, no scroll to continue, no "fold" to push detail below. A projected slide has ~3 seconds; a feed ad has ~1. What doesn't land immediately doesn't land.
- **Exported, not live.** Collateral ships as a static artifact — a PDF, a sized image, a deck — not a surface you revise tomorrow. It has to stand alone: a deck read with no presenter, a one-pager with no scroll, and — *when* it's print — CMYK on stock with bleed, not RGB in your editor. Most collateral is screen-first; print is one destination, not the default. If it only works in your tool, with you narrating, it isn't finished.

Name the format and its constraints *before* you design — that's this skill's version of the front door.

## Front-Door Diagnosis — Settled Brand, or Rework?

Before anything, diagnose where the brand is. Open `.agents/design.md`, `.agents/brand.md`, and `.agents/product-marketing.md` — by this stage **all three should exist.** Then ask one question:

> *Are we applying a settled brand, or reworking one from scratch?*

- **Refine / apply the existing system** ("we have our brand, we need a deck") → Optimization or light Evolution. **Proceed** — this is the skill's home.
- **The system is being defined or changed** (full rebrand, heavy Evolution, or the new type/color/graphics aren't recorded yet) → **stop and route back to `creative-direction`.** Do not design collateral on an undefined system — you'll produce one-off art that nothing else will match, which is the opposite of collateral's job.

**If `.agents/design.md` is missing, that *is* the "go back" signal.** If `.agents/product-marketing.md` is missing or the piece has no copy, route to the marketing library's `copywriting` (or `sales-enablement` for a sales asset's substance) first: **the piece is built around the message, never the reverse.** Routing back holds even if the user already has a logo — a mark without the system around it isn't enough to keep a deck, a sheet, and an ad coherent.

## Copy First — This Is the Gate, Not a Preference

**Weak collateral is usually a copy problem wearing a design problem's clothes.** No amount of composition rescues generic lines; conversely, get genuinely good copy and the design gets good almost on its own, because there's finally something worth giving emphasis to. So this is a **gate, not a nicety**: if the copy isn't strong, stop and get it written — route to the marketing library's `copywriting` (or `sales-enablement` for a sales asset's substance). Placeholder-grade copy produces placeholder-grade design, and you will not be able to fix it downstream.

**The exception: pieces with no real message to carry.** A business card, a profile avatar, a letterhead, a folder — the content is a name, a role, a URL. These are pure identity applications and can be designed **immediately**, without waiting on copy. Everything that argues something — one-pagers, decks, social posts, ads, thumbnails — waits for the words.

## Message First — Especially Here

Collateral exists to carry a *specific message to a specific moment*: a deck persuades a room, a one-pager survives being left on a desk, an ad interrupts a scroll. The single most important input is what it needs to say and to whom. Read `product-marketing.md` (audience, voice, positioning) and the actual copy. **Your job is to give that message proper emphasis, joy, and delight** — not to build a template and drop text into the boxes. Template-first is the fastest tell of assembled collateral: the deck where every slide is a title and three bullets, the sheet that's a wall of equal-weight paragraphs.

If the copy isn't written, get it written first. **Size follows content, not a grid** — one killer proof point deserves a whole slide; a feature list deserves consolidation, not a cramped two columns.

## Apply the System — By Role, Across the Family

Pull the system from `.agents/design.md`; don't re-derive it, don't invent alongside it. The same role discipline as `web-design`, tuned for fixed formats:

1. **Color by role, in the right color space.** Background, text (primary/secondary), action/accent, support — five stops, not ten. **For anything going to print, work in CMYK and check the translation** — brand RGB/hex often shifts on press (see [references/print.md](references/print.md)). For decks and screen-PDF, RGB is fine, but mind projector contrast: subtle low-contrast pairs that read on your monitor die in a bright room.
2. **Type by role, for contrast not competition.** Display, heading, body — each with a job. Bold is not the default; body is a reading weight. **Fixed formats punish under-scaled type**: a deck read from the back of a room and an ad seen at thumbnail size both demand bigger, more decisive type than a website. Use the licensed brand faces; embed them in the file (PDF/PPTX) so they survive the handoff.
3. **Use the REAL assets from `.agents/design.md` — never a stand-in.** This file (plus `logo-design`'s output) holds the actual **logo files, brand colors, licensed typefaces, and motif** established upstream. Pull them; do not approximate them.
   - **Never substitute an icon-font glyph or a lookalike shape for the logo.** A Material Symbols / Lucide / emoji icon standing in for the mark is the single most damaging shortcut in this skill — it silently replaces the brand's most controlled asset with a generic one. If you can't locate the real file, **stop and ask** rather than approximating.
   - **Check you have the current version.** Identities get revised; a mark from an earlier round may be stale. Confirm the logo, palette, and type in `design.md` are the latest before applying them across a whole family — a full set built on a superseded mark is a full set to redo.
   - **The mark has a canonical path — place the file, don't prepare one.** `logo-design` delivers locked files to a fixed location and registers them in `design.md`'s Logo section. Read the table there and place the file by name:

     | Need | File |
     |---|---|
     | Default, everywhere | `.agents/assets/logo/logo-lockup.svg` |
     | Mark alone (tight space, avatar, favicon) | `logo-icon.svg` |
     | Dark ground | `logo-lockup-inverse.svg` |
     | One-colour (print, etch, single-ink) | `logo-lockup-black.svg` · `-white.svg` · `-gray.svg` |
     | Square / rounded | `avatar.svg` · `app-icon.svg` |
     | Surfaces that can't take SVG | `raster/` |

     **A ground is a variant choice, not a colour edit.** Light piece → the primary; dark piece → the *inverse* or *white* file. Do not make one asset inherit `currentColor` so the surrounding CSS decides its colour — that's not "one asset working everywhere," it's handing the brand's most controlled asset to whatever `color` happens to cascade in, which is how it ends up tinted to an accent. `currentColor` is legitimate **only** inside a file the identity designates as the one-colour variant, where the single ink is the point.
     - **If the variant you need doesn't exist, route back to `logo-design` and have it added.** Never improvise one at the point of use — not by recolouring, not by inverting in CSS, not by exporting your own.
   - **Read which mark was *chosen*, don't just grab a file.** A logo exploration leaves behind many candidates — three families, a shortlist, several wordmark experiments. **Find the stated recommendation / sign-off and use that one.** Picking whichever file looks plausible (or whichever the presentation happened to reference in a layout) is how a whole collateral family gets built on a rejected concept. If the recommendation isn't recorded, or the assets are still placeholders, **stop and ask** — this is not a guess worth making, because every piece in the family inherits the error.
   - **The logo is ONE locked element. Use it exactly as delivered.** Mark and wordmark come pre-locked in fixed proportion and fixed relationship — you place that single asset, you never rebuild the lockup out of parts, and you never re-space it. **A logo must behave identically in every medium.** Specifically, never:
     - **recolor it** — use only the delivered color variants (full-colour / inverse / white / black / mono). Tinting the mark to match an accent is a hard no.
     - **box it** — no container, chip, rounded square, or badge around the logo unless the identity itself defines one.
     - **crop it** — give it its full artwork bounds and clear space; a mark clipped by its own frame or viewBox is broken. Check the delivered viewBox actually contains the whole drawing.
     - **re-declare its coordinate space** — the delivered file's `viewBox` *is part of the asset*, not a layout choice. Never set a second one at the place of use: an `<svg viewBox="…">` wrapping a `<use>` of a `<symbol viewBox="…">` nests two viewports and silently re-maps the artwork, and stripping the symbol's own viewBox renders a fragment. Either way you get a subtly wrong mark on **every piece in the family**, and because it still reads as *a* logo it survives review after review. Size the placement with width/height (and `flex-shrink: 0`, since a viewBox-less `<svg>` has no intrinsic ratio for a flex parent to respect) — never with coordinates.
     - **rebuild or re-proportion it** — no setting the wordmark yourself next to the symbol, no adjusting the gap, no substituting a different cut per format.
   - **Same for color and type:** exact brand values and licensed faces from `design.md`, not visually-similar substitutes.
   - **Diff your render against the delivered file — visually, side by side, large.** Render the mark as you've placed it at ~200px next to the delivered artwork and confirm they are the same drawing: same stroke weight all the way round, same gap, same proportions. Then check it again at the *smallest* size you ship it. Verifying a *number* — the bounding box, the file hash, the path data — proves nothing about what renders, and a mark can be measurably "contained" and visibly distorted at the same time. If you never put your output next to the source of truth, you have not checked the logo.
   - **If the mark's detail collapses at the sizes collateral actually needs, that's a finding — not something to fudge.** A card, a slide footer, and an avatar are small; a mark with fine interior detail (thin ticks, knurled edges, hairlines) can turn to mush there. Report it back to `logo-design` and ask for a simplified small-size cut rather than shipping a muddy mark or quietly redrawing one yourself. Collateral is usually where this gets discovered, because it's the first place the mark is used small and repeatedly.
4. **The mark is present but rarely the hero — and use the right cut of it.** A logo belongs on collateral (slide footer, sheet corner, ad sign-off) sized for recognition, not dominance; a cover or pure brand piece is the exception — **and on those, size it like the hero it is.** A footer-scale mark dropped into the middle of a closing slide or a cover is its own error: if the mark is the only thing on the surface, undersizing it makes the piece look unfinished rather than restrained. Give it clear space; never stretch, recolor off-system, or drop it onto a busy field. **Inside a constrained shape — a circle, an avatar, a small badge — use the mark alone, not the full lockup.** Nesting a mark-plus-wordmark inside a ring or a tiny container crowds both; pick the symbol and let it breathe. And don't add the logo where it earns nothing: on a piece already carrying the brand's motif and type, a redundant mark is clutter.
5. **The motif carries the brand across the family — with restraint where the message must win.** The signature element (pattern, texture, recurring detail) is how a deck slide and an ad read as the *same brand* without being the same layout. This is where distinctiveness must **survive application** (see `design-principles`). Calm it wherever the message leads — a cover, a hero stat, an ad's one line — and let it work harder on connective, lower-stakes surfaces.
6. **One accent, reserved.** Whatever signals "the point / the action" — the one CTA on an ad, the key number on a slide — stays scarce. Sprinkled on every heading and box, it stops meaning anything.

## Compose the Frame — Dynamic, Not Filled

A fixed frame has no scroll to rescue a flat layout and no interaction to add interest, so composition carries most of the load. Full method in [references/composition.md](references/composition.md):

- **The canvas is a hard limit — content never exceeds it.** Headlines, stats, quotes, cards, CTAs must sit **entirely inside the safe area**; only *decoration* (washes, patterns, oversized motifs, bleeding photos) runs off the edge. Clipped content is a failure, not a rough edge — and the fix is to **shrink or cut the content**, never to let it spill. Check all four edges and the bottom of the last element before calling a piece done.
- **The logo goes at the BOTTOM, not the top.** The top of the frame belongs to the message. The mark signs off at the bottom (deck covers and pure brand pieces excepted), and **social posts get no logo at all** — the handle and avatar already brand them. On an identity piece this decides the whole layout: **on a business card the person's name is the message**, so the name leads at the top and the logo signs off at the bottom — not a wordmark banked at the top with the name pushed under it and a dead band of nothing in between.
- **Alignment is exact, spacing is systematic, punctuation hangs.** Off-centre is sloppiness; a pull-quote's opening `"` must hang outside the measure so the text's left edge stays true. Run the craft pass with `frontend-design` / `web-design-guidelines` — those principles apply verbatim to a fixed canvas. Overlap only where it creates depth or connects two things.
- **Don't port web components into print.** A browser frame, nav bar, app card, or form field pasted onto a sheet reads as a screenshot and usually drags the wrong typeface in with it. Share the *system* with the site, not its components — and set everything in the brand's actual face.
- **Draw imagery from the `art-direction` library** (`.agents/assets/imagery/approved/`), and route anything new back to `art-direction` — it specs, sources or generates, reviews, and treats it to the brand's grade.
- **A bad image is worse than no image.** Generic stock cheapens the piece; if you don't have imagery that's specific and good, solve it typographically or graphically instead.

- **Light first, dark second.** Default to a light composition, especially for print — a near-black printed piece is rare, drinks ink, scuffs, and goes muddy on uncoated stock. **Even a dark screen brand needs a light expression for paper.** Build that, then produce the dark variant for screen. If a piece genuinely should be dark, give it **depth** — a gradient with light in it, not flat black.
- **One motif language per frame *and* per family — check for the quiet second one.** Two line systems in one piece reads as indecision, and the second one is usually something you stopped seeing: a faint background grid sitting under the real motif, a hairline rule system, a texture inherited from a template. Sweep the whole family for it — if the deck and one thumbnail carry a grid while everything else carries the rings, the family has two languages, not one. And when a radial/concentric motif's **centre is visible on the canvas it reads as a bullseye** — a target that pulls the eye — instead of a big system sweeping through the frame; push the centre off-canvas or hollow it out.
- **Give it a background element that ties the composition together — and push it off the canvas.** Text and boxes on an empty ground is the flat case. Use a large gradient wash, an oversized cropped motif, a dotted/concentric field sweeping across the whole piece, a shape entering from off-frame. **Go bigger than feels safe, bring color into it, and let the frame crop it** — don't force it to fit. But **where type sits, the background yields** (mask, fade, or route around it): legibility wins. And watch the accumulation — wash *plus* rings *plus* grid *plus* giant numeral in one frame is how a piece starts reading as AI-generated. The tell isn't the pattern, it's the excess; add the element, then remove what it made redundant.
- **Use rich media — including real photography.** Varying the layout isn't enough if every band is still type and boxes. Bring photography, illustration, product imagery, and the icon set in generously.
- **Don't invent elements that aren't in the brand language.** Adding a device "just for print" — a decorative rule under a word, a gradient bar, a line system that appears nowhere else in the identity — is not enrichment, it's drift. Every graphic element on a piece should trace to `design.md`; if it doesn't, cut it. And if an invented line collides with the real motif, that's the tell.
- **Stop wrapping everything in cards.** A bordered/filled card around every block is a reflex, not a decision — it flattens hierarchy and adds visual noise. Structure with **typography and space first**: column headers, rules, generous gaps. Reserve a card for content that genuinely needs to read as a discrete object (an inverted pull-quote, one highlighted plan). A page of cards is the print equivalent of a page of divs.
  - **The exception is content sitting on the motif: there, use a card, not rules.** A hairline-ruled list laid over a line or concentric-ring pattern is two line systems fighting each other — the rules read as part of the motif and the content stops holding together. An **opaque card reads on top of a pattern**; a rule just competes with it. So the choice isn't cards-vs-no-cards, it's *what the content is sitting on*: bare ground → type and space; patterned ground → a solid block that lets the motif pass behind.
- **No buttons on printed pieces, and no synthetic obliques.** A pill CTA on a printed one-pager implies a click that can't happen — use a URL, short link, or QR code instead. And never fake an italic: if the face has no true italic cut, the slanted roman is a distorted amateur tell — express emphasis with weight, size, or color instead.
- **Compose on an 8-column grid, not a repeated two-column split.** A 2-col layout stamped down the whole piece is the fixed-format version of banded web sections. Vary the spans band to band (5+3 hero, 4+4, full-8 statement, 3+3+2, 6+2) while holding gutters and outer margin constant — same rhythm discipline `web-design` applies to sections.
- **Mix the media across bands**, not just the column counts: photography, vector, icons, a device mockup, a chart, an inverted pull-quote card. Every band as text-in-boxes is still flat.
- **A safe zone is a keep-out, not a starting line.** A platform's UI-safe band (the top and bottom of a story/reel, where the profile row and reply bar land) marks where content *may not go* — it is not where content should begin. Interior margin is **additive on top of it**: content starting exactly at the safe line looks jammed under the platform chrome even though nothing is technically clipped. This is also the trap in your own audit — set the required inset to *safe + margin*, or the measurement will pass a piece that visibly has no margin at all.
- **Don't stack two background devices in the same corner.** An oversized numeral piled onto the same corner as the motif crop reads as clutter, not depth — separate them (one high, one low). And an oversized element still has to **read**: a numeral cropped past recognition isn't a bold device, it's an unidentifiable shape. Big and legible, or smaller and whole.
- **Margin is the space *inside* the trim — scaled to the format.** A large sheet wants far more than screen instincts give it (~1/2–3/4in on letter); a **business card wants content sitting just inside the safe line**, not a half-inch in, or it reads empty and unresolved. Align just inside safe, then add margin in proportion to the piece's size.
- **Size type for where it will be seen.** Social and thumbnail type drawn to look balanced on a 1080 artboard arrives in a feed at a third that size and stops being readable. Design for the delivered size and **cut content rather than shrinking type** (see [references/ads.md](references/ads.md)).

## Build the System, Then Cascade

Collateral almost always comes in *sets* — a deck, a run of conference-speaker posts, a family of OG images, ten localized one-pagers. The craft is to **build one reusable template and cascade content through it**, not to decorate each piece by hand. This is the same discipline the rest of the library teaches (grids, hierarchy, brand adherence), pointed at repeated, fixed-format output. Full method in [references/build-the-system.md](references/build-the-system.md).

1. **Identify the format and size first.** Fixed-format means the destination and its dimensions are decided *before* you design — a 16:9 slide, an 8.5×11 PDF, a 1080×1350 post, an OG image, a printed banner. For print-bound pieces, set up for a **PDF export** with bleed / safe / carryover handled (see [references/print.md](references/print.md)); for screen, size to the exact placement and export at native resolution.
2. **Build one template as the system** — a grid, borders, defined slots for what repeats and what changes, the brand's type / color / motif, and **mixed media with variety** (photo, vector, icon, illustration, and richer treatments like gradients or shaders where the brand warrants). Anything you'd compose in Figma or Paper you can compose in code — *if you set up that structure first*.
3. **Stress-test against the worst-case content before cascading.** Find the **longest name / longest headline / densest bio** and design the type scale and slots around *that* instance — if it holds for the extreme, every shorter one fits. Give optional slots to elements that aren't always present.
4. **Cascade the content through the proven system** so the set reads as one brand — *one system, varied content*, no two pieces stamped identically.

## Design to the Format — Each Has Its Own Craft

Pick the format, then design to its real constraints. Deep dives per medium:

- **Decks & presentations** → [references/decks.md](references/decks.md). One idea per slide; the deck is a *sequence* with an arc, not a stack of independent slides. **Decide presented vs. read up front** — a talk-track deck (sparse, big visuals, the presenter carries the words) and a leave-behind/send deck (self-contained, denser, works with no narrator) are different artifacts, and building one as the other is the classic failure. Kill bullet soup: one statement + one visual beats five bullets. Data slides get **one takeaway, and the takeaway is the title** (charts via `dataviz`). A shared master (margins, safe title zone, footer) holds it together — but **vary the layouts** so it isn't 30 identical slides (rhythm across a deck is the same discipline as rhythm across web sections).
- **One-pagers, sales sheets & leave-behinds** → covered in [references/decks.md](references/decks.md) (the "self-contained surface" section). One primary message + ranked proof, on a single frame that works with **no presenter and no scroll** — it has to answer "what is this and why should I care" the instant it's picked up. Dense is fine; flat is not.
- **Print** → [references/print.md](references/print.md). Real dimensions in mm/in (never px), **bleed / trim / safe-margin** set correctly, **CMYK** and a checked color translation, **300 DPI** raster / vector where possible, rich vs. registration black, fold panels that respect reading order, stock and finish. Ship a **press-ready PDF**, not a screenshot.
- **Ads (paid social & display)** → [references/ads.md](references/ads.md). The **squint / scroll-stop test**: one message, legible at thumbnail, in ~1 second. Design to each **platform's size and safe zones** (feed 1:1 / 4:5, stories & reels 9:16 with UI-safe margins, IAB display sizes). Text discipline — a few decisive words, not a paragraph. **One CTA**, mark present but not shouting. Variations at scale: `ad-creative` owns the copy variants; you own the visual system that holds them together. Motion/video ad → route to `motion-design`.
- **Digital graphics — OG images, marketing / feature graphics, social templates, banners** → build these with the **system-and-cascade** method above: fixed pixel size, exported at native resolution, legible at the size actually served (an OG image is seen small, in a link preview). A full social *system* (profiles, ongoing formats) is also this skill's job — build it as a system with a cascade, not as one-off art; one-off branded graphics live here too.

## Coherence Across the Family — the Whole Point of Collateral

A single beautiful slide is not the job; a *set* that reads as one brand is. When you produce more than one piece — and you usually will — run the family test:

- **Same system, different layouts.** The deck, the sheet, and the ad should share color roles, type, mark, and motif but **must not be the same layout stamped three times.** Coherence is strategic (same feeling, same rules), not literal (same grid). A pile of identical templates is as much a failure as three pieces that don't look related.
- **Coherent with the site.** If `web-design` already shipped, the collateral extends that surface's system — same tokens, same mark treatment, same motif logic — so a prospect who saw the site recognizes the deck.
- **A legitimate flex is allowed.** A conference banner, an event one-pager, a premium leave-behind may stretch the everyday system *if it stays true to the strategy* (see `design-principles` → coherence, not repetition, which carries the flex-vs-drift call).

## Tooling & References — Use What's Connected, Fall Back Gracefully

Collateral is produced in the format's native tooling, not custom web code. Lean on what's connected; **never block on a missing tool — degrade to the next option** (full map in [references/tooling.md](references/tooling.md)). Check `.agents/brand.md` → **Toolkit** first for what the operator has — including the image generator that supplies a piece's imagery — and write back anything new you find connected:

- **`canvas-design` skill** — static art to PNG/PDF (posters, one-pagers, ads, print pieces) with design philosophy built in. A strong default for a single fixed-format graphic.
- **Claude Design** — when the system has been published there (see `creative-direction`), the first choice for decks and one-pagers non-designers will keep editing: inherits the brand, edits on canvas, exports PDF / PPTX / Google Slides. Imagery still comes from `art-direction`.
- **`slide-deck` (makerskills) / presentation tooling** — deck generation and structure.
- **`dataviz` skill** — *any* chart, stat tile, or dashboard on a slide or sheet. Read it before drawing the first chart so the data reads as one system.
- **Adobe MCP** (when connected) — layout and document rendering (`document_render_layout` / `render_vector`), InDesign / IDML for print production, Express, and `font_recommend` / `find_fonts` for licensed faces.
- **Paper / Pencil / Figma MCP** — design canvases when you want to compose visually and export.
- **Marketing library** — `ad-creative` (ad copy variants at scale), `sales-enablement` (one-pager / battle-card *substance*), `copywriting` (the words). This skill designs; those supply the message.
- **HTML/CSS as a fallback layout engine** — for a screen-PDF deck or a web-hosted one-pager, clean HTML/CSS → print-to-PDF is a legitimate path when no design tool is connected. For print, still export to the right size and color space.

## Validate Before You Ship

Run your own output through the same gauntlet the audit runs — **adversarially, on the rendered artifact, in its real context** (see `design-principles` → Judge Your Own Work on the Competitor's Bar):

- **Score it against the audit categories** vs. the confirmed competitor set at a rival's harshness — Creative Direction, Color, Type, Layout. Would this earn a 4–5?
- **Run the collateral-slop check** ([references/collateral-slop.md](references/collateral-slop.md)) and **list what it finds** — bullet soup, template-underneath decks, centered-everything sheets, clip-art icons, stock-photo clichés, CTA/accent bleed, low-contrast-on-projector, RGB-headed-to-print. "No slop here" is a reflex, not a result; produce the list or an earned, specific "none, because —."
- **Test it in its real moment, not your editor.** Project the slide (is it legible from the back, in a bright room?). Shrink the ad to thumbnail (does one message survive the squint?). Export the print piece to a press-ready PDF and check bleed/trim/CMYK. Read the deck as a silent PDF (does it stand without you talking?).
- **Review at the size it ships at — never only at reduced scale.** A shrunken contact sheet flatters everything: type that's unreadable at final size still *looks* fine at 30%. Small physical formats are where this bites hardest — check a business card at true 3.5×2in, not at 3× on screen, and hold a practical floor (**~7pt minimum for contact/role lines, ~10–12pt for a name**; at 300dpi that's ~30px and ~50px, so screen-native type sizes are far too small if carried over unchanged). If a piece was only ever reviewed scaled down, it wasn't reviewed.
- **Measure the type floor, don't look at it.** Convert every text element to points at the piece's own DPI (`px / dpi * 72`) and report anything under the floor. Undersized type on a print piece is invisible as a defect on screen — 25px on a 300dpi card looks perfectly comfortable and prints at 6pt — so it survives round after round of visual review, including on work that's already been approved. Same discipline as the canvas: it's a measurement.
- **Cover-the-logo carry-through.** With the mark hidden, is the piece still recognizably this brand? If the distinctiveness lived only in the logo, the system didn't survive application.
- **Family coherence.** Lay the pieces side by side: one brand, or three unrelated templates? Same feeling, varied layout?
- **Proof the words.** Spelling, grammar, numbers, and — for anything printed — a final read *at size*, because you can't patch a printed run.

## Deliver It in a Viewer — Reviewable at True Size

A set of collateral is hard to judge as a pile of files or a shrunken contact sheet. **Ship the work in a lightweight viewer** so it can be seen the way it will actually exist. Build it as a single self-contained HTML file alongside the exports — it costs little and it's where review actually happens. Full pattern in [references/viewer.md](references/viewer.md).

- **Switch between formats** — one-pager, social set, cards, thumbnails, deck — so the family can be compared in one place.
- **Render each piece at its true size**, with a zoom control: *Fit*, *100%* (native pixels), and **Actual size** (true physical scale via the piece's DPI — a 3.5×2in card rendered 3.5×2in, which is the only honest test of a card).
- **Present the deck as a deck** — click and arrow-key through it, a slide counter, a filmstrip to jump around, and a fullscreen present mode. A deck reviewed as static thumbnails hides its pacing.
- **Show pieces at trim by default; reveal bleed only when guides are tripped** — bleed is production, not how the piece looks. Guides on → bleed/trim/safe labeled with a legend, from a doc built at bleed size. **Anchor the trim box so nothing moves when the toggle flips** — the bleed appears *around* a piece that holds its exact size and position; no review overlay may reposition the artifact it describes.
- **Only surface controls that apply to the format** (no static/motion switch on a print one-pager — it can't animate), and put controls near what they affect rather than banked in a far corner.
- **Stage everything on a neutral mid-gray canvas with a visible outline** — never white, never the brand's own colors. A light piece needs a darker ground to read as an object, and a dark piece disappears into a dark stage. If you can't see where the artifact ends, you can't judge its margins.
- **Show social in real platform context, across platforms** — Instagram feed and story/reel, LinkedIn, X, Facebook — in device frames with the actual platform chrome, alongside the varied format set (square, 4:5, 9:16, 1.91:1).
- **Animate the social and screen pieces, and show static *and* motion** with a replay control — text rising in, staggered reveals, a drifting background element, a considered button entrance. Social is a moving medium; judging it static judges half of it. Defer to `motion-design` for the craft.
- **Keep the viewer chrome neutral and outside the artifact** — a plain grey shell, never the brand's own colors, and no helper text overlapping the piece. The chrome must not become part of what's being judged.
- **Build the audits in, and make them able to fail.** An overflow audit against a safe box **on every format, screen included** (interior margin; platform UI-safe bands on a 9:16), plus a type-floor audit in points at the piece's DPI. Report **coverage** — how many artboards were measured — because "clean" over zero artboards looks exactly like a pass, and prove the audit still catches a planted violation.
- **Give the reviewer a content layer they own** — copy and type sizes in a plain-data file, separate from the rendering code, which you never rewrite. Copy is the gate, so review *means* editing words; if that requires touching markup they can't do it, and a scripted rewrite of yours will destroy the edits they did make.
- **Make views deep-linkable** (`?v=cards&z=phys`) so specific pieces can be pointed at in review.
- **Cache-bust at page load, not at build time** — a stamp baked into the HTML never changes, so the browser serves stale code and edits stay invisible.

## The Deliverable

- **The finished artifact(s)** in the correct output format: a presentable/sendable deck (PDF, and editable source where relevant), a print-ready PDF (CMYK, bleed, correct trim), sized ad exports per placement, or a screen/print one-pager.
- **The viewer** (above) — a single HTML file that renders the set at true size and plays the deck, so the work can be reviewed as it will actually be seen.
- **Optional: a short note** on how the system was applied (which tokens, mark treatment, master/template conventions) appended to the project so later collateral and other mediums stay coherent. Don't duplicate `.agents/design.md` — reference it.

## Non-Negotiables

- [ ] Format and its constraints named up front (trim/size, color space, presented-vs-read, platform safe zones)
- [ ] Front-door diagnosis run; system being defined/changed routed back to `creative-direction` (even if a logo exists)
- [ ] `.agents/design.md`, `brand.md`, `product-marketing.md` read; system applied, not re-invented
- [ ] **Copy gate passed** — strong copy exists and drives the layout (weak copy = stop and get it written); identity-only pieces (business cards, avatars, letterhead) exempt
- [ ] **Real assets pulled from `.agents/design.md`** — locked logo files **placed from their canonical paths** (`.agents/assets/logo/…`), never an icon-font/emoji stand-in or a self-prepared copy; exact brand colors, licensed faces; confirmed to be the *current* version
- [ ] **Ground handled by variant, not by recolouring** — primary on light, inverse/white on dark, mono where one ink is the point; **no `currentColor` letting consumer CSS pick the mark's colour**; missing variant routed back to `logo-design`
- [ ] **Logo placed as the one locked asset** — never rebuilt, recoloured, boxed, cropped, re-proportioned, or given a second `viewBox`/coordinate space; identical behaviour in every medium
- [ ] **Logo render diffed against the delivered file** — side by side at ~200px *and* checked at the smallest shipped size; a numeric/bbox check is not a verification
- [ ] **No invented elements** — every graphic traces to `design.md`; nothing added "just for print"
- [ ] **Not everything in a card** — structure led by type, column headers and space; **but content sitting on the motif gets an opaque card, not hairline rules**
- [ ] Radial/concentric motifs **centred on the piece** they radiate through
- [ ] A **deck is treated as digital** (screen/web craft), not as a print piece
- [ ] Mark used at the right cut: **symbol alone inside a constrained shape** (circle/avatar/badge), no redundant logo where the motif and type already carry the brand; small-size legibility checked and any collapse **reported back to `logo-design`**
- [ ] **Nothing clipped** — verified by an automated overflow **measurement** against the safe box (not by eye), **on every format including screen** (interior margin; UI-safe bands on 9:16), with **coverage reported** (how many artboards measured) and the audit **proven able to fail** on a planted violation; only decoration bleeds; content shrunk or cut to fit rather than spilled
- [ ] **Type floor measured in points at the piece's DPI** (`px/dpi*72`), not judged on screen — nothing under ~7pt on a print piece
- [ ] **Logo at the bottom** (covers excepted); **no logo on social posts**; business-card back is the mark + at most one motif crop
- [ ] **Craft pass run** (`frontend-design` / `web-design-guidelines`): exact alignment, systematic spacing, hanging quote marks, overlap only where it earns depth
- [ ] **No web components ported into print**; every element in the brand's actual typeface
- [ ] Imagery is specific and good, or replaced by a typographic/graphic solution — no placeholder-grade stock
- [ ] Message exists and drives the layout — no template-first, no bullet soup, size follows content
- [ ] For a set: one reusable system/template built and **stress-tested against worst-case content** (longest name/headline, densest/sparsest) before cascading — one system, varied content
- [ ] **Light expression designed first** (print especially); dark is a second variant, and any dark piece has depth (gradient, not flat black)
- [ ] A **background element ties each composition together** (wash / oversized cropped motif / graphic line), behind the content and cropped by the frame — not text-and-boxes on an empty ground
- [ ] Composed on an **8-column grid with varied spans** and mixed media band to band — not one two-column split repeated
- [ ] **Interior margin scaled to the format** — large sheets well past safe; small formats (cards) sitting *just inside* safe, not ballooned into emptiness
- [ ] **Safe zones treated as keep-outs, not starting lines** — interior margin added *on top of* platform UI-safe bands, and the audit inset set to safe + margin
- [ ] **No button on a printed piece** (URL / short link / QR instead); **no synthetic obliques** anywhere
- [ ] **Social & thumbnail type sized for the delivered screen**, verified legible at a glance in a device mockup — content cut rather than type shrunk
- [ ] **Thumbnails checked at real scale in a scrolling list** (a scroll-test strip in the viewer); vertical (9:16) formats given true interior margin inside the UI-safe zones
- [ ] Anything animated **reviewed in motion**, replayable — not approved as a still
- [ ] **One motif, not several** — a single background language (rings *or* lines, never both in a frame), varied by scale/crop/density; swept for a **quiet second system** (background grid, stray rule set) and any **visible radial centre** pushed off-canvas or hollowed
- [ ] Motif applied **across the whole family including cards and social**, and shown that way in review — not just on the big pieces
- [ ] Motif pushed **off-canvas and given color**, yielding behind live text; background elements not accumulated into excess
- [ ] **Rich media present** — real photography / illustration (brand's own > licensed > openly-licensed comp, and placeholders labelled as such), cropped deliberately and tied into the system; not geometry-and-type only
- [ ] Color in the right space (CMYK + checked translation for print), five stops, accent reserved; type by role, bold not the default, scaled for the real viewing distance; brand faces embedded
- [ ] Real mark pulled and given clear space, present-not-dominant; motif carries the brand, calmed where the message leads
- [ ] Designed to the format's craft — decks: one idea/slide, presented-vs-read decided, varied masters, one-takeaway data slides; print: bleed/trim/safe, 300 DPI, folds; ads: squint test, safe zones, one CTA
- [ ] Family coherence checked — same system, varied layouts; coherent with the shipped site; any flex is deliberate, not drift
- [ ] Adversarial self-audit on the *rendered* artifact in its real moment (collateral-slop tropes listed, not "none"); cover-the-logo carry-through
- [ ] **Reviewed at true size, not only scaled down** — physical scale checked on small print formats, type above the practical floor (~7pt contact/role, ~10–12pt names)
- [ ] Delivered in a viewer: format switching, true-size zoom, deck clickable/arrow-navigable with present mode, bleed/trim/safe guides that **reveal without moving the piece**; **neutral gray canvas with visible piece outlines**; social shown **in-platform across platforms**, static *and* animated; chrome neutral and outside the artifact
- [ ] **Reviewer owns a plain-data content layer** (copy + type sizes) that the rendering code reads and you never rewrite — and no scripted whole-file rewrites over anything they edit
- [ ] Viewer assets **cache-busted at page load**, not with a stamp baked into the HTML
- [ ] Correct output format shipped (press-ready PDF / sized exports / sendable deck); spelling, grammar, numbers proofed at size

## Related Skills

- `design-principles` — the craft beliefs this skill applies
- `creative-direction` — supplies the visual system (hard prerequisite); route back for Revolution / heavy Evolution
- `art-direction` — the photography, illustration, icons, and textures this skill places; route new imagery needs there
- `logo-design` — the mark, applied here
- `brand` — the audit whose categories are this skill's acceptance test
- `web-design` — the same system on the web surface; keep collateral coherent with it
- `motion-design` — the same system in motion; animated and video ads route there
- `design-critique` *(planned — not yet shipped)* — will judge the finished collateral against the emotional target and the flex-vs-drift latitude
- marketing library: `copywriting` (the words come first), `sales-enablement` (one-pager / battle-card substance), `ad-creative` (ad copy variants at scale)
- method: [references/build-the-system.md](references/build-the-system.md) (build one system, stress-test, cascade); [composition.md](references/composition.md) (light-first, background element, 8-col grid, print margin); delivery: [references/viewer.md](references/viewer.md) (true-size viewer + playable deck); per-format deep dives: [decks.md](references/decks.md), [print.md](references/print.md), [ads.md](references/ads.md); [collateral-slop.md](references/collateral-slop.md)
- tooling (use when connected, fall back gracefully): **Claude Design** (decks and one-pagers, once the system is published there), **`canvas-design`** (static PNG/PDF art), **`slide-deck`** (decks), **`dataviz`** (charts), **Adobe MCP** (layout / print / InDesign), **Paper / Pencil / Figma MCP** (design canvases), or **code → PDF/image export**; see [references/tooling.md](references/tooling.md)
