---
name: design-md
description: >-
  Reference library of 74 real-world brand design systems (Claude, Linear, Stripe,
  Vercel, Figma, Apple, Tesla, Spotify, Notion, Supabase, and more) captured as
  DESIGN.md files — colors, typography, components, layout, elevation. Use when the
  user wants UI, a landing page, or a component that matches a specific brand's look;
  wants to pick a design direction from real design systems; says "like <brand>",
  "make it feel like Linear / Stripe / Apple"; or needs a concrete design-token
  starting point before frontend work. Pairs with frontend-design and
  tailwind-design-system.
---

# design-md — 74 brand design-system references

A curated set of `DESIGN.md` files distilled from well-known brand websites. Each one
captures a real design system in AI-readable form: **color palette with semantic roles,
typography hierarchy, component rules, layout principles, and depth / elevation**. Hand
one to a coding agent and it can generate UI that matches that brand's look.

Source content: **[voltagent/awesome-design-md](https://github.com/voltagent/awesome-design-md)** (MIT).
This skill is a thin *index + workflow* layer over that library.

## When to use this skill

- The user asks for UI / a landing page / a component in a named brand's style
  ("like Linear", "make it feel like Stripe", "give it an Apple vibe").
- You need to pick a **design direction** from real systems instead of inventing one.
- You want a concrete set of design tokens (colors / type scale / component rules) as a
  starting point before handing off to `frontend-design` / `tailwind-design-system`.

## Workflow

1. **Pick a brand** — scan the index below by *mood + primary color* and choose the
   closest match to the brief.
2. **Load its DESIGN.md** — read `<library>/design-md/<brand>/DESIGN.md`, using the
   slug from the index (e.g. `linear.app`, `x.ai`, `bmw-m`).
3. **Follow it** — treat the color roles, type scale, components, and elevation as a
   hard spec. For a visual reference, open the sibling `preview.html` / `preview-dark.html`.
4. *(optional)* Hand off to `frontend-design` → `tailwind-design-system` → `shadcn` →
   `design-review` to turn the direction into production components.

## Locating the library (`<library>`)

`<library>` is a local clone of the awesome-design-md repo. Resolve it in order:

1. The `DESIGN_MD_DIR` environment variable, if set.
2. Common locations: `~/Developer/awesome-design-md`, `~/dev/awesome-design-md`,
   `~/awesome-design-md`, or an `awesome-design-md/` folder in the current project.
3. If none exist, clone one (shallow is fine):

   ```bash
   git clone --depth 1 https://github.com/voltagent/awesome-design-md.git ~/Developer/awesome-design-md
   ```

Brand files always live at `<library>/design-md/<brand>/DESIGN.md`.

> The index below (primary color + one-liner) is enough to pick a direction on its own.
> Read the full DESIGN.md only when you need the complete token detail.

---

## The 74 brands (primary color + one-liner)

### AI & LLM
- **claude** `#cc785c` — Warm cream canvas, coral CTAs, serif display; humanist where most AI brands go cool blue.
- **x.ai** `#ffffff` — Near-black canvas broken only by white pill outlines; minimal, cold frontier-AI.
- **cohere** `#17171c` — Enterprise AI: white editorial space, deep green-black product bands, mineral surfaces, rounded media cards.
- **mistral.ai** `#fa520f` — Signature sunset gradients (mustard / orange / deep red) over mountain photography.
- **minimax** `#0a0a0a` — Black-pill CTAs on stark white marketing, paired with vivid gradient product surfaces.
- **together.ai** `#000000` — AI infra: near-black hero bands with a three-color orange-magenta gradient.
- **replicate** `#ea2804` — Warm-cream indie ML-playground aesthetic with a confident hot-orange accent.
- **runwayml** `#000000` — Cinematic reel: dark, editorial, full-bleed video *is* the UI.
- **elevenlabs** `#292524` — Voice AI that reads like a quiet editorial print magazine.
- **ollama** `#000000` — Defiantly minimal; the home page looks like a Markdown README.
- **composio** `#0007cd` — AI-agent tooling: dark, technical, a single deep-electric-blue voltage.
- **voltagent** `#00d992` — Dev-focused AI agent platform: relentless near-black + one neon green.
- **lovable** `#f7f4ed` — Warmth through restraint on a soft cream canvas (AI app builder).

### Developer tools & platforms
- **cursor** `#f54e00` — AI code editor with a warm-cream editorial canvas instead of the usual dark IDE, plus warm orange.
- **vercel** `#171717` — Black-and-ink duet on near-white, blown open at hero scale by a multi-color mesh gradient.
- **linear.app** `#5e6ad2` — The deepest near-black canvas in the set + a single lavender-blue accent; software-craft luxury.
- **framer** `#ffffff` — Pure-black artboard, GT Walsheim white type with aggressive negative tracking.
- **webflow** `#080808` — Visual web builder: deep near-black against a generous white canvas.
- **figma** `#000000` — Black-and-white editorial frame interrupted by oversized hand-cut pastel color blocks.
- **warp** `#f7f5f0` — Agentic terminal on a warm near-charcoal canvas (a tint warmer than pure black).
- **raycast** `#ffffff` — Marketing site that reads like one extended product screenshot.
- **opencode.ai** `#201d1d` — Terminal-native: the entire page set in Berkeley Mono.
- **expo** `#000000` — React Native platform styled as a quietly-confident infrastructure brand.
- **sentry** `#150f23` — Deep purple-violet midnight canvas, electric-lime accents, slightly subversive illustration.
- **posthog** `#f7a501` — Playful warm-cream canvas with hand-drawn hedgehog mascots as marginalia.
- **hashicorp** `#000000` — Near-black ground with per-product accents (Terraform purple, Vault yellow, Consul pink).
- **sanity** `#0b0b0b` — A nocturnal command center: dark, precise, deeply structured dev-content platform.
- **mintlify** `#0a0a0a` — Docs infra: atmospheric sky-gradient marketing heroes + clean white docs, dual-mode.
- **supabase** `#3ecf8e` — Open-source database: clean white / near-black with a single signature emerald CTA.
- **mongodb** `#00ed64` — Dark deep-teal hero bands with bright MongoDB-green CTAs + stark white docs.
- **clickhouse** `#faff69` — High-performance database on near-pure black with electric-yellow voltage.
- **ibm** `#0f62fe` — Faithful to Carbon: white surfaces, IBM Blue accent, deliberately flat-square aesthetic.
- **resend** `#fcfdff` — Near-pure black canvas, off-white text, a deep editorial-serif Domaine headline mark (dev email).
- **clay** `#0a0a0a` — Claymation-meets-data for a GTM orchestration platform; vibrant and playful.

### Productivity & collaboration SaaS
- **notion** `#5645d4` — All-in-one workspace: deep-navy hero band decorated with brand illustration.
- **miro** `#1c1c1e` — AI visual workspace anchored by a canary-yellow wordmark; confident, a little playful.
- **airtable** `#181d26` — Sober editorial workflow software with full-bleed signature cards (coral / dark green / peach).
- **cal** `#111111` — Calendar-software-first: white canvas, black primary CTAs, custom Cal Sans display.
- **slack** `#4a154b` — Deep aubergine primary, cream-lavender hero gradients, blue inline links.
- **intercom** `#111111` — Customer-service editorial: soft cream-white, Saans type, a single confident Fin blue.
- **zapier** `#ff4f00` — Workflow automation: warm-cream neutrals with a deep-orange accent.
- **superhuman** `#1b1938` — Fast email split between a deep-indigo editorial hero and a violet-sky atmosphere.

### Finance & crypto
- **stripe** `#533afd` — Deep-navy ink, electric-indigo primary, and a recurring atmospheric mesh gradient.
- **coinbase** `#0052ff` — Institutional-grade exchange styled as a quietly-confident financial-services brand.
- **binance** `#fcd535` — Deep near-black canvas with the iconic Binance yellow on every CTA.
- **kraken** `#7132f5` — Clean, trustworthy crypto exchange with commanding purple on white.
- **revolut** `#494fdf` — Stark black canvas, cobalt-violet brand, a wide palette of saturated product colors.
- **wise** `#9fe870` — Global money transfer: unusually heavy near-black display type (900 @ 64–126px) + bright green.
- **mastercard** `#eb001b` — Warm editorial magazine built from soft stone and signal orange-red.

### E-commerce, consumer & mobility
- **airbnb** `#ff385c` — Warm marketplace: clean white canvas + Airbnb Rausch coral as the single voltage.
- **shopify** `#000000` — Cinematic commerce platform running two parallel design tracks.
- **nike** `#111111` — Photography-first commerce with towering uppercase Futura burned into campaign imagery.
- **pinterest** `#e60023` — Photography-first discovery: Pinterest-red CTA, masonry pin grid, soft warm-cream chrome.
- **starbucks** `#006241` — Warm retail flagship wearing storefront-apron green across every surface.
- **uber** `#000000` — Transportation super-app: black-and-white duet framed by a custom geometric display.
- **meta** `#0064e0` — Hardware commerce (Quest, Ray-Ban Meta) + brand surfaces with a product-merchandising voice.

### Media & entertainment
- **apple** `#0066cc` — Photography-first interface that turns marketing into a museum gallery.
- **spotify** `#1ed760` — Near-black immersive player where album art is the color, plus Spotify green.
- **theverge** `#3cffd0` — A Condé Nast magazine wired to a chiptune soundboard; neon.
- **wired** `#000000` — Flagship tech magazine: strict black wordmark on white, editorial duet.
- **playstation** `#0070d1` — Black / white / PlayStation-blue chapters scrolling like a console launch trailer.

### Automotive
- **tesla** `#3e6ae1` — Radical subtraction: the product is everything, a single electric blue.
- **ferrari** `#da291c` — Luxury supercar brand rendered as cinematic editorial.
- **bmw** `#1c69d4` — Measured, settled corporate-automotive (distinct from BMW M's bombast).
- **bmw-m** `#ffffff` — Motorsport engineering: near-black canvas, white BMW Type Next in confident uppercase.
- **lamborghini** `#ffc000` — A cathedral of darkness: jet-black stage, the machine under a spotlight.
- **bugatti** `#ffffff` — Austere luxury: near-pure black, white letterspaced uppercase, full-bleed photography.
- **renault** `#ffed00` — The 2021 flat-line diamond mark, stark black-and-white, signature Sunlight Yellow.

### Enterprise, hardware, telecom & aerospace
- **hp** `#024ad8` — White-paper enterprise-consumer system with HP Electric Blue as the lone signal CTA.
- **nvidia** `#76b900` — Engineering-grade: black hero / paper-white body dual mode + NVIDIA green.
- **vodafone** `#e60000` — Telecom super-brand: editorial photography heroes with massive uppercase display.
- **spacex** `#000000` — Mission-oriented aerospace: pure black with full-bleed rocket / Mars video heroes.

### Retro (90s–00s)
- **dell-1996** `#e91d2a` — Catalog-era enterprise web: literal black page frame + flat color-block ribbon cards.
- **nintendo-2001** `#e60012` — Brushed-periwinkle "console chrome" where every panel is a beveled metal plate.

---

## Picking hints

- **Warm / humanist**: claude, cursor, warp, posthog, lovable, zapier, pinterest, starbucks, mastercard
- **Dark / high-contrast tech**: linear.app, vercel, x.ai, sanity, clickhouse, spacex, resend, together.ai
- **Minimal / product-first**: tesla, apple, bugatti, raycast, ollama, uber
- **Single bold accent**: supabase (green), stripe (indigo), binance (yellow), airbnb (coral), kraken (purple), spotify (green)
- **Editorial / magazine**: elevenlabs, wired, theverge, ferrari, mastercard, cohere
- **Racing / luxury black**: lamborghini, bmw-m, ferrari, bugatti

When unsure about color, don't invent a palette — copy the semantic color roles straight from the chosen brand's DESIGN.md.
