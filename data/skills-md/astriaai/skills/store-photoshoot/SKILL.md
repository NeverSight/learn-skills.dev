---
name: store-photoshoot
description: Use when turning a brand's whole online store (Shopify or WooCommerce) into a reusable Astria AI photoshoot — crawl the catalog, extract the brand's DNA, cast avatars, and build packs that re-shoot the entire collection (and every future drop) in the brand's own look. Trigger phrases — "build a photoshoot from my store", "crawl STORE_URL and make packs", "AI product photography for BRAND", "re-shoot our catalog". For a single lookbook/collection PAGE use `templatize-page` instead.
allowed-tools: Bash(astria:*), Bash(python3:*), Bash(curl:*), Read, Write, AskUserQuestion
---

# Store Photoshoot Builder

Given a brand's storefront URL, crawl the shop, extract its brand DNA, and build
a complete, reusable AI photoshoot system in an Astria workspace: a casting
board of brand avatars (when on-model shots are needed), product reference
tunes, and a set of **packs** (prompt templates) that can re-shoot the brand's
entire catalog — and every future collection — in the brand's own visual
language.

All Astria operations go through the `astria` CLI (see the **astria-api**
skill) — never raw API calls, never tokens in skill text. Scope every command
with `-w <workspace_id>`. Everything you register in Astria — faces, garments,
shoes, jewels, poses, backgrounds, props, logo lockups — is a **single-image
faceid reference tune** whose `name` is a controlled class noun (`woman`, `man`,
`boy`, `girl`, `dress`, `shirt`, `pants`, `shoes`, `ring`, `necklace`, `chain`,
`earrings`, `bracelet`, `pose`, `background`, `outfit`, `bottle`, …) and whose
`title` is the human/SKU label. Prompts address them as `<faceid:ID:1>
<class-noun>` — the class noun immediately after the token is the routing
mechanism that tells the model what to take from that reference.

**Deliverable of a full run:** a workspace containing (1) a confirmed Brand DNA
brief, (2) a 2–5 avatar casting board (on-model only), (3) product reference
tunes, (4) one pack per item-type / outfit formula with a fixed shot battery,
(5) a QA'd pilot render, then the scaled catalog, and (6) a workspace landing
page.

Related skills: **astria-api** (the CLI), **unique-headshot** (avatar casting),
**prompt-writing** (prompt grammar & parameters), **packs-guide** (packs),
**templatize-page** (silhouette/pose-swap technique, single page),
**landing-page-editor** (the `/w/:slug` page).

---

## Phase 1 — Crawl the store

**Detect the platform first**, then use its public JSON endpoints. Crawl
politely: sequential requests, a normal browser User-Agent.

**Shopify** — `{store}/products.json` returns JSON:
```
GET {store}/products.json?limit=250&page=N     # loop N=1,2,3… until "products" is empty
GET {store}/collections.json?limit=250          # collections + products_count
GET {store}/collections/{handle}/products.json  # per-collection membership
GET {store}/pages.json?limit=100                # About / editorial / brand-story pages
```
Per product capture: `title`, `product_type`, `tags`, `vendor`, `body_html`
(strip HTML), `variants[].price`, `images[].src` (CDN URLs — the tune training
source), `options` (sizes → audience signal).

**WooCommerce** — `{store}/products.json` returns the homepage, not JSON. Use
the Store API instead:
```
GET {store}/wp-json/wc/store/v1/products?per_page=100&page=N   # loop until empty
GET {store}/wp-json/wc/store/v1/products/categories?per_page=100
```
Per product: `id`, `name`, `sku`, `type` (`simple`|`variable`),
`prices.price` (÷ 10^`currency_minor_unit`), `images[].src`, `categories[].name`,
`variations`. Homepage `og:` meta and `/product-sitemap.xml` give the brand
name, logo, and a full product-URL list if the Store API is disabled.

**Fallbacks** — if JSON is gated (password/B2B): `{store}/sitemap.xml` →
`sitemap_products_*.xml`, or ask the customer for a product-export CSV, or for
direct image URLs.

**Image audit (critical).** Download 20–40 product images across categories and
*look at them* (actually view each image). Record, per category: shot style (on-model vs
packshot vs flat-lay vs atmosphere); angle coverage (front/back/side/detail);
the house background hex (sample corner pixels); model casting (age, gender mix,
ethnicity, styling); lighting fingerprint (softbox-even vs flash vs daylight).
The photoshoot you build must be recognizably *the same brand* — these
observations become the pack defaults. Front+back product photos also decide
which items can support back-view templates.

## Phase 2 — Extract the Brand DNA brief

Synthesize a structured brief and **confirm it with the customer before
building** — one round with your ask-user question tool (`AskUserQuestion` in
Claude Code, `ask_user` in the Astria chat agent): brand read, shoot register,
casting direction. Capture:

- `brand`, `vertical` (fashion | footwear | jewelry | beauty | supplements | home-decor | mixed)
- `categories`: product_type histogram → tune classes, SKU counts, back-photo availability
- `sku_scale`: boutique(<100) | catalog(100–1K) | factory(1K–10K) | enterprise(10K+)
- `audience`: gender (women/men/both/kids/family), age band (from sizes, copy, collection names), a **body-guard** line for prompts (see Phase 5)
- `positioning`: mass/family | contemporary | premium | luxury — from price stats (median/max variant price) and About/collection copy tone
- `aesthetic`: `background_hex` (from the image audit), lighting, brand comps
- `shoot_plan`: which registers (Phase 3), how many avatars
- `pilot_skus`: 8–15 products spanning the top categories

**SKU scale drives the architecture:** boutique → hand-picked hero looks, richer
editorial per look; catalog → pack-per-outfit-formula factory, `--create_crops`
for detail shots, one avatar per pack; factory+ → hardened templates run as
named batches (3 angles/look, per-colorway tunes) — prioritize best-sellers and
the newest collection, never try to shoot the whole 10K in the pilot.

## Phase 3 — Choose the photoshoot registers

A brand usually gets one primary register + one or two supporting. Ask the
customer which they want as the lead when the vertical supports several
(a single ask-user question). Avatars are cast **only** for on-model registers.

| Vertical | Primary | Supporting |
|---|---|---|
| Fashion (garments) | Studio lookbook on-model (front/45°/back battery) | Ghost/3D packshots; location campaign |
| Footwear | Product packshot 5-angle battery | On-model legs-down crops; atmosphere still-life |
| Jewelry | Still-life on tactile surfaces + worn close-ups | Extreme macro; hand-model for rings |
| Beauty (bottles/cremes/sprays) | Packshots on seamless + atmosphere (marble, stone, water, botanicals) | Texture macro; application close-ups |
| Supplements | Clean packshots + kitchen/gym lifestyle | Ingredient still-life; hand-holding product |
| Home decor | In-room styled atmosphere | Detail/texture macro; ghost packshot |

## Phase 4 — Create / target the workspace

Use the customer's existing workspace when they name one (`astria workspaces
list` → target with `-w <id>`); otherwise create one named after the brand
(via the workspace UI, or `astria api POST /workspaces` if available — confirm
the id with `astria workspaces list`). Note the house background hex — every
studio template pins it twice (in prose and via `--background_color`).

Two-greys convention: packshots on `#F2F2F2` (luminance-flattened), on-model
studio on `#F5F5F5`/`#e9e9e9`-family off-whites, luxury lookbooks on pure
`#FFFFFF` + flash — unless the brand's own photography says otherwise.

## Phase 5 — Cast the avatars (on-model registers only)

Avatars are synthetic faces generated from trait-dense prompts, **no reference
tune** — the **unique-headshot** method. Generate with
`astria generate --model recraft-4-1 --num-images 2 --aspect-ratio 1:1`, bare
shoulders, hair pulled back, **no jewelry on the face ref** (critical for
jewelry brands — earrings on a face ref contaminate every render), ≥1 unique
distinguishing feature, never repeat an ethnicity in a batch. Match casting to
the Brand DNA (audience age, ethnicity mix, positioning). Present a candidate
board (ask-user question with thumbnails), then register each winner:

```
astria tunes create -w <id> --title "<Name> — <brand>" --name woman|man|boy|girl --image-url <winner.jpg>
```

**Casting board size: 2–5 faces.** Production brands run one avatar per
ethnicity and hold **one avatar constant across all shots of a pack** —
consistency beats variety. Attach the brand's **body-guard** text (rides after
the person token in every prompt):
- kids/tween: `boy 1.30 high` / `girl 1.30 high`; toddler: `girl 1.5 yo toddler, proportional head`
- womenswear luxury: `tall supermodel proportions, elongated legs, long neck, narrow waist` + `sleek, low, slicked-back bun`
- menswear premium: `tall male supermodel proportions, elongated athletic body, broad shoulders narrow waist, masculine confident posture`
- explicit age when relevant: `11 y o teen girl`, `teen 15 y o man`

Footwear legs-down crops, pure packshot, and atmosphere plans skip avatars —
the model (if any) is described verbally and the face is cropped out.

## Phase 6 — Ingest product references

For each pilot SKU, create a faceid tune from the shop's CDN images:

```
astria tunes create -w <id> --title "<SKU or product title>" --name <class> \
  --image-url <front.jpg> [--image-url <back.jpg>]
```

- Map `product_type` → tune class with a controlled vocabulary. The class must
  be the *actual subject* — "jewelry" is a poor name; use `ring`/`necklace`/
  `chain`/`earrings`. Rename + retrain if wrong (`astria tunes update <id> --name ring`).
- **Variant products (`type: variable`):** do NOT blindly take `images[0]` — it
  is often the wrong colorway/variant. Match the chosen image to the intended
  variant (or ingest one tune per variant). A mismatch trains a faithful render
  of the *wrong* product.
- **Non-ASCII image URLs** (Hebrew/RTL/Cyrillic paths) must be
  **percent-encoded** before `--image-url`, or Astria returns HTTP 422 "could
  not download".
- Prefer clean product-only images over on-model shots for garment fidelity.
  Include the back photo only when the battery has back views. One tune per
  colorway. Keep the SKU code in the title — it's the join key back to the shop.
- Optionally register support tunes: a `background` set plate, `pose` refs
  (OpenPose skeletons or black product silhouettes — see **templatize-page**),
  brand `label`/`text` lockups for print fidelity, props (`chair`, `car`).

## Phase 7 — Author the packs (the core)

**A pack = one item-type or outfit formula × a fixed shot battery.** Shot
variety lives in the templates; per-SKU variety comes from swapping the
reference tokens. Create with `astria packs create --title "<Brand> — <Formula>"`
and author each template into the pack (see **astria-api** for pack-authoring).
Iterate until the pilot passes QA.

### 7.1 House prompt grammar (studio lookbook)

```
<shot/pose line: framing + angle + stance>
<faceid:AVATAR:1> woman <body-guard text>
<faceid:GARMENT_TOP:1> shirt <fit & layering directives>
<faceid:GARMENT_BOTTOM:1> pants <coverage directives>
<faceid:SHOES:1> shoes
[<faceid:BACKGROUND:1> background] plain background {HEX} softbox --background_color {HEX} [--create_crops 70]
```

- Weight is always `1.0`.
- Free text after each garment's class noun does the **fit/layering** work:
  `shirt over size, sleeves reach just past the elbow, shirt out of the pants`,
  `front shirt half tucked inside the pants`, `pants cover the shoes`,
  `buttoned shirt worn open over the shirt, top two buttons open, untucked hem`,
  `pants reach the shoes, no socks visible`.
- **Layer-visibility clauses** control partial garments: `visible hem of`,
  `visible waistband of`, `only the bottom hem is visible at the top of the frame`,
  `Absolutely no part of the dress fabric is visible` (for shoe macros).
- **Fidelity guards** where reference photos are messy: `ignore back label`,
  `don't change the color of the pants`, `Use the outfit reference only for the
  clothing: garment shape, fabric, color, print, trims, sleeve length…`,
  `Model identity, face, body, hands, nails and hair come from the model
  reference`, plus a negative tail (`Avoid hair down, bangs, copied room
  background, rug, carpet, barefoot, missing shoes; no plastic skin, no beauty
  filter, no extra limbs`).
- Params: **3:4, 4K, num_images 1** (2–4 for the hero front shot). Discover the
  default model with `astria models`. Detail shots come free via
  `--create_crops 66–72` (full frame + 2 crops) instead of separate prompts.

### 7.2 Shot batteries per item type

Author one pack per formula the shop actually sells; each bullet = one template.

- **Tops (shirt/polo/tee/sweater)** — front full · 35–45° front-side · back full · half-body front · waist/tuck detail · optional walking / left profile.
- **Coat / jacket / blazer** — front closed · front open over inner top · 45° · back (highlight structure) · half-body back over-shoulder · collar/shoulder macro.
- **Pants / jeans / shorts** — front · 45° · back · waistline crop · lower-half at 45° (`weight shifted to back leg, showcasing drape`) · walking.
- **Dress / skirt** — front · 45° · back · walking/movement (`fabric swishes`) · half-body · fabric macro · optional seated.
- **Footwear — packshots (no model):** strict side elevation (toe right, heel left, camera level with centerline) · straight-on front from low camera · rear three-quarter · overhead flat-lay · pair at 3/4 one shoe staggered · tight macro on stitching. Every template carries `no foot, no model, no extra objects, seamless light neutral grey studio background, realistic contact shadow beneath the product, natural scale, no compression or squashing` + `--background_color`.
- **Footwear — on-model:** lower-half 45° · legs-down crop (`close shot from the knees down, always focus on the shoes`) · low-angle shoe close-up (`see only hem of pants above the footwear`) · seated with shoes in foreground.
- **Bags & accessories** — 3-framing trio: front centered with negative space · three-quarter for depth · tight macro on hardware · plus one on-model hold/wear. Eyewear: `45 degree side-profile fully open, showing the temple arms` + front + worn close-up.
- **Jewelry** — three families (1:1): *still life* on smooth white fabric / silk / matte stone / sculpted ceramic, `not a close-up, medium distance framing` for negative space; *worn close-ups* `<faceid:WOMAN:1> woman wearing <faceid:JEWEL:1> earrings` with strict crops — necklace bust `upper chest and neck` or `cropped just below the eyes`; earrings `tight close-up, crop from ear to collarbone, side profile`; ring on a hand model (`hand resting on a stone tray beside an espresso`, always `manicured nails`); chain worn on bare chest/neck; *macro* 100mm. House stanza: `soft neutral-warm studio lighting, diffused directional light from front-side, very soft highlights, no yellow cast, balanced white tones, natural beige palette slightly warm but desaturated`. Rotate skin tone across templates.
- **Beauty (cremes/bottles/sprays/lotions)** — *packshot* front label-centered · 45° · back (label legible — register a `label` text tune if type fidelity matters) · line family shot; *atmosphere* product on marble/travertine/wet stone with droplets · botanical styling · backlit translucency · texture macro (cream smear, spray mist); optional application close-ups (hands/cheek/collarbone, no face identity). Surfaces & lighting borrow the jewelry vocabulary (`no yellow cast` for golds/ambers).
- **Supplements** — packshot battery + lifestyle atmosphere (morning kitchen with citrus and water; gym-bag still life; hand holding the jar label-forward) + ingredient flat-lay.
- **Home decor** — in-room atmosphere (one coherent interior per collection, palette-matched) · straight-on packshot on seamless · texture/detail macro · scale shot with a human element (hand on ceramic, figure near the lamp — face optional).

### 7.3 Campaign register (hero content, optional)

Not pack templates first — long-form prompts in the brand's language, promoted
to a pack once a scene wins. Structure with labeled sections
(`LOCATION / FOREGROUND / SUBJECT / BACKGROUND / CAMERA / LIGHTING / MOOD / STYLE`),
one coherent location vocabulary per campaign (reuse the same scene description
verbatim across the set; pin it with a `background`/`location` tune). Film/camera
vocabulary is the realism lever matched to positioning: luxury `85mm, shallow
depth of field, Kodak Portra 400 film grain`; street-cool `35mm, f/8, hard
direct on-camera flash, ISO 400`; family-candid `soft diffused overcast
daylight`. For premium work add an anti-CGI block (`visible pores, no smoothing,
natural fabric behavior, imperfect drape, soft analog 35mm grain`). Formats
9:16 / 16:9, 4K, num_images 2–3.

### 7.4 Pose control ladder

1. **Text first** (default): terse angle line, escalate to full photographic
   paragraphs (weight distribution, gaze, camera height, 20–30° body angle) when
   stances drift.
2. **Skeleton pose tunes**: train OpenPose stick-figure renders as `pose` tunes
   (front / 45° / back), lead the prompt with `<faceid:POSE:1> pose`, refine verbally.
3. **Silhouette lock** (to clone the brand's *existing* photography stance-for-
   stance): threshold a real catalog photo to a black silhouette, register as
   `pose`, prompt `replace the <faceid:POSE:1> pose … Keep the pose exactly as
   in the silhouette. Ignore the pose from the outfit.` (see **templatize-page**).

### 7.5 Video add-on (optional)

- Runway loop per look: Seedance, 16:9, 8–9s, three timestamped beats — walk in
  from left → stop center & pose → walk past camera and exit; `Static camera,
  continuous motion, no cuts`.
- Product turntable: one storyboard prompt, `slow smooth 360-degree rotation over
  8 seconds`, per-second angle checkpoints, a negative block (`avoid fast
  spinning, deformation, extra objects, text, logo`).

## Phase 8 — Pilot, QA, scale

1. Render the pilot: each pack × 2–3 SKUs of its category, one avatar held
   constant per pack. Keep it modest (≤ ~40 images).
2. QA each render: garment/jewel shape·color·print fidelity; layering (tucks,
   hems, waistbands); face = avatar (no drift); background exactly the house hex;
   anatomy (hands, feet); no leaked artifacts (room backgrounds, mannequin
   stands, care labels); `no yellow cast` on golds; brand text/logos legible.
3. **Stop and get sign-off before scaling** — mass generation is real spend.
   Fix by tightening the responsible clause (add a guard or negative), not by
   rerolling blindly. If an item renders wrong repeatedly, inspect the tune's
   training images (bad crops / wrong class / wrong variant are the usual cause).
4. Scale in phases: best-sellers/newest first for sign-off, then the rest.
   Iterate over the crawled product list — `tunes create` per SKU, one generate
   per template with the SKU's tokens swapped in. Name batches
   (`<BRAND> BATCH1 LOOK 1–N`).
5. Post-production at volume: background-removal passes for cutouts, 16:9
   recrops for banners, upscale passes for hero shots.

## Phase 9 — Landing page & handoff

Generate the workspace landing page from the brief (see **landing-page-editor**):
`astria landing set -w <id> --brief "<positioning, palette, collections, packs to feature>"`.
Report to the customer: workspace link, the casting board, each pack (`/p/<slug>`)
with its battery, pilot images, and the one-step instruction for future
collections — *point us at the new products; the packs re-shoot the whole drop
automatically.*

---

## Appendix — Style presets by positioning

| Positioning | Background | Lighting | Body / styling | Suffix vocabulary |
|---|---|---|---|---|
| Kids / family mass | `#e9e9e9` softbox | even softbox, `small smile` | height guard, playful poses | clean e-com, `--create_crops` |
| Contemporary basics | `#F5F5F5` seamless | soft studio light | natural relaxed stance | `Kodak film 400 grain` |
| Premium menswear | `#E7E7E7` / light gray | professional fashion editorial lighting | tall supermodel proportions | quiet-luxury comps (`COS / ARKET… Minimal. Architectural. Retail-ready.`) |
| Luxury womenswear | pure `#FFFFFF`, no floor | **direct on-camera flash** | sleek slicked-back bun, elongated legs | sharp e-commerce catalog image |
| Street / cool | dark or night urban | hard flash, underexposed bg, ISO 400 grain | candid mid-stride, `not posing` | `by William Eggleston` / Tillmans |
| Jewelry / beauty | cream-beige, tactile surfaces | soft neutral-warm, **no yellow cast** | manicured hands, rotated skin tones | quiet luxury product photography, 4K clarity |

Keep the preset reasoning inside the Brand DNA brief — the customer confirms it
once, and every template inherits it.
