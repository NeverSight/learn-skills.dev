---
name: design-taste-frontend
description: Anti-slop frontend skill for landing pages, portfolios, and redesigns. The agent reads the brief, infers the right design direction, and ships interfaces that do not look templated. Real design systems when applicable, audit-first on redesigns, strict pre-flight check.
---

# tasteskill: Anti-Slop Frontend Skill

> Landing pages, portfolios, and redesigns. Not dashboards, not data tables, not multi-step product UI.
> Every rule below is **contextual**. None of it fires automatically. First read the brief, then pull only what fits.

---

## 0. BRIEF INFERENCE (Read the Room Before Anything Else)

Before touching code or tweaking dials, **infer what the user actually wants**. Most LLM design output is bad because the model jumps to a default aesthetic instead of reading the room.

### 0.A Read these signals first
1. **Page kind** - landing (SaaS / consumer / agency / event), portfolio (dev / designer / creative studio), redesign (preserve vs overhaul), editorial / blog.
2. **Vibe words** the user used - "minimalist", "calm", "Linear-style", "Awwwards", "brutalist", "premium consumer", "Apple-y", "playful", "serious B2B", "editorial", "agency-y", "glassy", "dark tech".
3. **Reference signals** - URLs they linked, screenshots they pasted, products they named, brands they're competing with.
4. **Audience** - B2B procurement panel vs. design-conscious consumer vs. recruiter scanning a portfolio. The audience picks the aesthetic, not your taste.
5. **Brand assets that already exist** - logo, color, type, photography. For redesigns, these are starting material, not optional input (see `reference/redesign-protocol.md`).
6. **Quiet constraints** - accessibility-first audiences, public-sector, regulated industries, trust-first commerce, kids' products. These constraints OVERRIDE aesthetic preference.

### 0.B Output a one-line "Design Read" before generating
Before any code, state in one line: **"Reading this as: \<page kind> for \<audience>, with a \<vibe> language, leaning toward \<design system or aesthetic family>."**

Example reads:
- *"Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind utilities + Geist + restrained motion."*
- *"Reading this as: solo designer portfolio for hiring managers, with an editorial / kinetic-type language, leaning toward native CSS + scroll-driven animation + custom typography."*
- *"Reading this as: redesign of a public-sector service site, with a trust-first language, leaning toward GOV.UK Frontend or USWDS."*

### 0.C If the brief is ambiguous, ask one question, do not guess
Ask exactly **one** clarifying question - never a multi-question dump - and only when the design read genuinely diverges. Example: *"Should this feel closer to Linear-clean or Awwwards-experimental?"*

If you can confidently infer from context, **do not ask**. Just declare the design read and proceed.

### 0.D Anti-Default Discipline
Do not default to: AI-purple gradients, centered hero over dark mesh, three equal feature cards, generic glassmorphism on everything, infinite-loop micro-animations everywhere, Inter + slate-900. These are the LLM defaults. Reach past them deliberately based on the design read.

### 0.E Mode Routing (deck vs longform)
**Deck / slide briefs** (slides, deck, keynotes, 演示, PPT, "8 slides about X") - do NOT apply the longform Sections 1-14 as-is. Read **`reference/deck-mode.md`** before generating. Boundaries lock the skeleton; the style contract tells you what to respect and where to play. Every other brief (landing, portfolio, editorial, redesign, app) stays on the core rules in this file + `reference/pre-flight-checklist.md`.

**Deck briefs split into two style routes (ask once, 3-4 questions - 风格意象 / 语气词 / 明确禁忌 / 受众):**
- **素材模式 (default)** - the brief's style can be matched by a style in the material library (refero-styles/). 选型管线（一条顺序，勿跳步）：`showcase/selection-index.json` 筛选（mood / tone / density / scheme 机器可读字段，`best_for` / `avoid_for` 给适用性判断）→ 收窄 2-4 套短名单 → `showcase/gallery/` 看预览截图（slide 0/4/7）→ 读短名单的 DESIGN.md 定稿 → 值层 1:1 生成（15.3）。Material is the source of truth；`design-manifest.json` 为字段明细源。
  - manifest 字段语义与 30 套已知例外（缺 radius 分组 / `--leading-body` 回退等）见 `manifest-schema.md`；扩库标注（新增风格时）的词表白名单与字段规范见 `annotation-guide.md`（校准锚点：`metadata/motherduck.json`）。
- **自由发挥模式 (fallback)** - the brief needs a style OUTSIDE the library (hand-drawn wedding invite, cartoon kids product, a totally custom voice). Fill `freeplay-declaration.md` FIRST (the self-authored mini design-system: palette voice / typographic voice / signature moves / anti-convergence statement / CJK) → generate against that declaration → QA gate 2/3 run as normal, gate 1 (value-layer 1:1) downgrades to "declared-token self-consistency" (see 15.6). The declaration is both the generation discipline and the QA anchor.
- **交付意图识别（部署分享）**：brief 或后续对话出现"部署 / 上线 / 发链接 / 公开分享 / 发布 / Vercel / 妙搭 / 飞书"等交付意图时——deck 生成并通过 15.6 QA 之后，**先完整读取 `deploy-guide.md`**（公开 URL 的执行规范：环境自备自检、Vercel / 妙搭两条出口完整流程、字体改造与失败处理），再按 15.9 交付。不要凭记忆操作平台 CLI；showcase 30 套是样品，默认部署对象是用户自己的 deck。
- If a match is borderline, default to 素材模式 (real brand systems are the anti-slop ammunition).

---

## 1. THE THREE DIALS (Core Configuration)

After the design read, set three dials. Every layout, motion, and density decision below is gated by these.

* **`DESIGN_VARIANCE: 8`** - 1 = Perfect Symmetry, 10 = Artsy Chaos
* **`MOTION_INTENSITY: 6`** - 1 = Static, 10 = Cinematic / Physics
* **`VISUAL_DENSITY: 4`** - 1 = Art Gallery / Airy, 10 = Cockpit / Packed Data

**Baseline:** `8 / 6 / 4`. Use these unless the design read overrides them. Do not ask the user to edit this file - overrides happen conversationally.

### 1.A Dial Inference (design read → dial values)
| Signal | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| "minimalist / clean / calm / editorial / Linear-style" | 5-6 | 3-4 | 2-3 |
| "premium consumer / Apple-y / luxury / brand" | 7-8 | 5-7 | 3-4 |
| "playful / wild / Dribbble / Awwwards / experimental / agency" | 9-10 | 8-10 | 3-4 |
| "landing page / portfolio / marketing site (default)" | 7-9 | 6-8 | 3-5 |
| "trust-first / public-sector / regulated / accessibility-critical" | 3-4 | 2-3 | 4-5 |
| "redesign - preserve" | match existing | +1 | match existing |
| "redesign - overhaul" | +2 | +2 | match existing |

### 1.B Use-Case Presets
| Use case | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (Agency / creative) | 9 | 8 | 3 |
| Landing (Premium consumer) | 7 | 6 | 3 |
| Portfolio (Designer / studio) | 8 | 7 | 3 |
| Portfolio (Developer) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| Public-sector service | 3 | 2 | 5 |
| Redesign - preserve | match | match+1 | match |
| Redesign - overhaul | +2 | +2 | match |

### 1.C How the Dials Drive Output
Use these (or user-overridden values) as global variables. Cross-references throughout this document refer to these exact variable names - never invent aliases like `LAYOUT_VARIANCE` or `ANIM_LEVEL`.

---

## 2. BRIEF → DESIGN SYSTEM MAP

Once you have the design read (Section 0) and dials (Section 1), pick the right foundation. Do not invent CSS for things that have an official package. Do not pretend an aesthetic trend is an official system.

### 2.A When to reach for a real design system (use official packages)
| Brief reads as… | Reach for | Why |
|---|---|---|
| Microsoft / enterprise SaaS / dashboards | `@fluentui/react-components` or `@fluentui/web-components` | Official Fluent UI, Microsoft tokens, accessibility done |
| Google-ish UI, Material-flavored product | `@material/web` + Material 3 tokens | Official, theme-able via Material Theming |
| IBM-style B2B / enterprise analytics | `@carbon/react` + `@carbon/styles` | Official Carbon, mature data-density patterns |
| Shopify app surfaces | `polaris.js` web components / Polaris React | Required for Shopify admin UI |
| Atlassian / Jira-style product | `@atlaskit/*` + `@atlaskit/tokens` | Official Atlassian DS |
| GitHub-style devtool / community page | `@primer/css` or `@primer/react-brand` | Official Primer; Brand variant for marketing |
| Public-sector UK service | `govuk-frontend` | Legally / regulatorily expected |
| US public-sector / trust-first | `uswds` | Same |
| Fast local-business / agency MVP | Bootstrap 5.3 | Boring, fast, works |
| Modern accessible React foundation | `@radix-ui/themes` | Primitives + polished theme |
| Modern SaaS where you own the components | shadcn/ui (`npx shadcn@latest add ...`) | You own the code, easy to customise; never ship default state |
| Tailwind-based modern SaaS / AI marketing | Tailwind v4 utilities + `dark:` variant | Default for indie + small team builds |

**Honesty rule:** if the brief reads as one of the systems above, install and use the **official** package. Do not recreate its CSS by hand. Do not import a system's tokens but then override 90% of them.

**One system per project.** Do not mix Fluent React with Carbon in the same tree. Do not import shadcn/ui components into a Material 3 app.

### 2.B When the brief is an aesthetic, not a system
For these directions, there is **no single official package**. Build with native CSS + Tailwind + a maintained component library. Be honest in code comments about what is borrowed inspiration vs. official material.

| Aesthetic | Honest implementation |
|---|---|
| Glassmorphism / "frosted glass" | `backdrop-filter`, layered borders, highlight overlays. Provide solid-fill fallback for `prefers-reduced-transparency`. |
| Bento (Apple-style tile grids) | CSS Grid with mixed cell sizes. No single library owns this. |
| Brutalism | Native CSS, monospace, raw borders. No library. |
| Editorial / magazine | Serif type, asymmetric grid, generous whitespace. No library. |
| Dark tech / hacker | Mono + accent neon, terminal motifs. No library. |
| Aurora / mesh gradients | SVG or layered radial gradients. No library. |
| Kinetic typography | Native CSS animations, scroll-driven animations, GSAP for hijacks. No library. |
| **Apple Liquid Glass** | Apple documents this for Apple platforms only. **There is no official `liquid-glass.css`.** Web implementations are approximations using `backdrop-filter` + layered borders + highlights. Label clearly as approximation. |

---

## 3. DEFAULT ARCHITECTURE & CONVENTIONS

Unless the design read picks a real design system (Section 2.A), these are the defaults:

### 3.A Stack
* **Framework:** React or Next.js. Default to Server Components (RSC).
  * **RSC SAFETY:** Global state works ONLY in Client Components. In Next.js, wrap providers in a `"use client"` component.
  * **INTERACTIVITY ISOLATION:** Any component using Motion, scroll listeners, or pointer physics MUST be an isolated leaf with `'use client'` at the top. Server Components render static layouts only.
* **Styling:** **Tailwind v4** (default). Tailwind v3 only if the existing project demands it.
  * For v4: do NOT use `tailwindcss` plugin in `postcss.config.js`. Use `@tailwindcss/postcss` or the Vite plugin.
* **Animation:** **Motion** (the library formerly known as Framer Motion). Import from `motion/react` (`import { motion } from "motion/react"`). The `framer-motion` package still works as a legacy alias - prefer `motion/react` in new code.
* **Fonts:** Always use `next/font` (Next.js) or self-host with `@font-face` + `font-display: swap`. Never link Google Fonts via `<link>` in production.

### 3.B State
* Local `useState` / `useReducer` for isolated UI.
* Global state ONLY for deep prop-drilling avoidance - Zustand, Jotai, or React context.
* **NEVER** use `useState` to track continuous values driven by user input (mouse position, scroll progress, pointer physics, magnetic hover). Use Motion's `useMotionValue` / `useTransform` / `useScroll`. `useState` re-renders the React tree on every change and collapses on mobile.

### 3.C Icons
* **Allowed libraries (priority order):** `@phosphor-icons/react`, `hugeicons-react`, `@radix-ui/react-icons`, `@tabler/icons-react`.
* **Discouraged:** `lucide-react`. Acceptable only when the user explicitly asks for it or the project already depends on it.
* **NEVER hand-roll SVG icons.** If a glyph is missing, install a second library or compose from primitives - do not draw icon paths from scratch.
* **One family per project.** Do not mix Phosphor with Lucide in the same component tree.
* **Standardize `strokeWidth` globally** (e.g. `1.5` or `2.0`).

### 3.D Emoji Policy
Discouraged by default in code, markup, and visible text. Replace symbols with icon-library glyphs. **Override:** allow emojis only when the user explicitly asks for a playful / chat-style / social-native vibe - and even then use them sparingly with intent.

### 3.E Responsiveness & Layout Mechanics
* Standardize breakpoints (`sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`).
* Contain page layouts using `max-w-[1400px] mx-auto` or `max-w-7xl`.
* **Viewport Stability:** NEVER use `h-screen` for full-height Hero sections. ALWAYS use `min-h-[100dvh]` to prevent layout jumping on mobile (iOS Safari address bar).
* **Grid over Flex-Math:** NEVER use complex flexbox percentage math (`w-[calc(33%-1rem)]`). ALWAYS use CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`).

### 3.F Dependency Verification (mandatory)
Before importing ANY 3rd-party library, check `package.json`. If the package is missing, output the install command first. **Never** assume a library exists.

---

## 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)

LLMs default to clichés. Override proactively. Every rule has a context-aware override path.

### 4.1 Typography
* **Display / Headlines:** Default `text-4xl md:text-6xl tracking-tighter leading-none`.
* **Body / Paragraphs:** Default `text-base text-gray-600 leading-relaxed max-w-[65ch]`.
* **Sans font choice:** `Inter` discouraged as default — pick `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`, or a brand-appropriate serif first. Override: explicit neutral / Linear-style ask, or public-sector / accessibility-first brief.
* **Pairings to know:** `Geist` + `Geist Mono`, `Satoshi` + `JetBrains Mono`, `Cabinet Grotesk` + `Inter Tight`, `GT America` + `IBM Plex Mono`.
* **SERIF DISCIPLINE (very discouraged as default):** "feels creative / premium / editorial" is NOT a reason for serif — "creative brief = serif" is the single most-tested AI tell. Serif acceptable ONLY when the brief names a serif font, OR the aesthetic is genuinely editorial / luxury / publication / heritage AND you can articulate why this serif fits this brand. Everything else defaults to sans-serif display (Geist Display, ABC Diatype, Söhne Breit, Cabinet Grotesk Display, Migra Sans, GT Walsheim, Inter Display, PP Neue Montreal). `Fraunces` / `Instrument_Serif` banned as defaults.
* **EMPHASIS RULE:** emphasize inside a headline with italic/bold of the SAME font — never inject a serif word into a sans headline (or vice versa); mixed-family emphasis is amateur.
* **If a serif is justified** (rare): rotate from this pool, never the same serif across consecutive projects — PP Editorial New, GT Sectra Display, Cardinal Grotesk, Reckless Neue, Tiempos Headline, Recoleta, Cormorant Garamond, Playfair Display, EB Garamond, IvyPresto, Migra, Editorial Old, Saol Display, Söhne Breit Kursiv, Domaine Display, Canela, Schnyder, Tobias, NB Architekt, ITC Galliard.
* **ITALIC DESCENDER CLEARANCE (mandatory):** italic display words with descenders (`y g j p q`) clip at `leading-[1]` / `leading-none` — use `leading-[1.1]` minimum + `pb-1` / `mb-1` reserve. Audit every italic display word before shipping.

### 4.2 Color Calibration
* Max 1 accent color. Saturation < 80% by default. **One palette per project** — no warm/cool-gray fluctuation.
* **THE LILA RULE:** AI-purple / blue-glow is discouraged as default — no automatic purple button glows, no random neon gradients. Neutral bases (Zinc / Slate / Stone) + one high-contrast accent (Emerald, Electric Blue, Deep Rose, Burnt Orange…). Override: brief explicitly asks purple → embrace with intent (consistent palette, harmonised neutrals, restrained gradients), not generic gradient slop.
* **COLOR CONSISTENCY LOCK (mandatory):** one accent on the WHOLE page — a warm-grey site never gets a blue CTA in section 7; a rose site never a teal footer badge. Audit every component before shipping.
* **PREMIUM-CONSUMER PALETTE BAN (mandatory, second-most-recurring tell):** the LLM default for premium-consumer briefs (cookware / wellness / artisan / luxury / heritage / DTC) is warm beige + brass/clay/oxblood + espresso text. Banned as default:
  - Backgrounds `#f5f1ea #f7f5f1 #fbf8f1 #efeae0 #ece6db #faf7f1 #e8dfcb` · Accents `#b08947 #b6553a #9a2436 #9c6e2a #bc7c3a #7d5621` · Text `#1a1714 #1a1814 #1b1814`.
  - **Rotate these families instead:** Cold Luxury (silver-grey + chrome + smoke) · Forest (deep green + bone + amber) · Black and Tan (off-black + warm tan, no beige) · Cobalt + Cream · Terracotta + Slate · Olive + Brick + Paper · monochrome + one saturated pop. Never ship the same family twice in a row.
  - Override: brief explicitly names those colors, or genuinely vintage/artisan brand AND you can articulate why.

### 4.3 Layout Diversification
* **ANTI-CENTER BIAS:** centered Hero/H1 avoided when `DESIGN_VARIANCE > 4` — force Split Screen, left-content/right-asset, asymmetric whitespace, or scroll-pinned structures. Override: editorial / manifesto / launch-announcement briefs where the message is the design.

### 4.4 Materiality, Shadows, Cards
* Cards only when elevation communicates real hierarchy; otherwise `border-t`, `divide-y`, or negative space.
* Tint shadows to the background hue — no pure-black drop shadows on light backgrounds.
* `VISUAL_DENSITY > 7`: generic card containers banned; data metrics breathe in plain layout.
* **SHAPE CONSISTENCY LOCK (mandatory):** ONE corner-radius scale per page (all-sharp / all-soft 12-16px / all-pill). Mixed systems only with a documented rule followed everywhere (e.g. "buttons pill, cards 16px, inputs 8px"). Round buttons in a square layout = broken.

### 4.5 Interactive UI States
Implement full cycles, not "static successful state only":
* **Loading:** skeletal loaders matching final layout shape, no generic spinners · **Empty:** beautifully composed + how to populate · **Error:** inline (forms), contextual (toasts only for transient).
* **Tactile feedback:** `:active` → `-translate-y-[1px]` or `scale-[0.98]`.
* **BUTTON CONTRAST CHECK (mandatory, a11y):** verify text-vs-background on every button — white-on-white, `bg-white` CTA + `text-white`, borderless transparent-over-page = banned. WCAG AA (4.5:1 body, 3:1 large 18px+). Ghost buttons over photos need backdrop / scrim / stroke.
* **CTA BUTTON WRAP BAN (mandatory):** button text fits ONE line at desktop — shorten the label (primary CTAs ≤3 words, ideally 1-2) or widen the button, never `max-width` a CTA. Wrapped CTA = Pre-Flight Fail (`reference/pre-flight-checklist.md`).
* **NO DUPLICATE CTA INTENT (mandatory):** one label per intent per page — "Get in touch" / "Contact us" / "Let's talk" / "Start a project" are ALL "contact": pick ONE everywhere (nav / hero / footer). Same for signup and portfolio intent clusters.
* **FORM CONTRAST CHECK (mandatory, a11y):** inputs, placeholders, focus rings, helper text, error text all pass WCAG AA against the section background. Audit every form.

### 4.6 Data & Form Patterns
* Label ABOVE input; helper text present in markup; error text BELOW input; `gap-2` blocks. No placeholder-as-label. Ever.

### 4.7 Layout Discipline (Hard Rules — failing any = shipping broken work)
* **Hero fits the initial viewport:** headline ≤2 lines, subtext ≤20 words AND ≤3-4 lines, CTAs visible without scroll. Too long → cut copy or reduce font scale. A value-prop that needs >20 words is unclear, not the rule too tight.
* **Hero font-scale discipline:** plan font + asset size together. Large asset + headline >6 words → do NOT start at `text-7xl/8xl`. Default `text-4xl md:text-5xl lg:text-6xl`; `text-6xl md:text-7xl` only for 3-5-word headlines. A 4-line hero headline is always a font-size error.
* **HERO TOP PADDING CAP (mandatory):** max `pt-24` desktop — more reads as a layout bug. Breathing room comes from font / asset scale, not top padding.
* **HERO STACK DISCIPLINE (max 4 text elements):** ① eyebrow OR brand strip (pick ≤1) ② headline ③ subtext ④ CTAs (1 primary + ≤1 secondary). **Banned inside hero:** tagline below CTAs, trust micro-strip, pricing teaser, feature bullets, avatar row — those become sections directly below. Eyebrow AND tagline together → drop the tagline.
* **Logo wall UNDER the hero, never inside it** — not in the same flex row as hero copy.
* **Nav renders on ONE line at desktop** (condense / drop / hamburger if not) · **height cap 80px, default 64-72px.**
* **Bento grids need rhythm:** no 6 consecutive left-image/right-text rows — alternate full-width rows, asymmetric tiles, vertical breaks. **BENTO CELL COUNT (mandatory):** exactly as many cells as content (3 items → 3 cells); an empty cell = planned wrong → re-shape, never paste a blank tile.
* **Section-Layout-Repetition Ban:** one layout family max ONCE per page; an 8-section page uses ≥4 different families.
* **ZIGZAG ALTERNATION CAP (mandatory):** max 2 consecutive image+text-split sections — the 3rd is a Pre-Flight Fail (`reference/pre-flight-checklist.md`). Break with full-width / vertical-stack / bento / marquee.
* **EYEBROW RESTRAINT (mandatory, #1 violated rule):** max 1 eyebrow per 3 sections (hero counts; 9-section page ≤3). If section A has one, the next 2 cannot. Pre-Flight check (`reference/pre-flight-checklist.md`) is mechanical: count small-caps `uppercase tracking` labels; > ceil(sections/3) → fail. Default move: drop it — the headline alone is enough.
* **SPLIT-HEADER BAN (mandatory):** "big headline left + small explainer right" banned as default — stack headline + body vertically (max-width 65ch). Allowed only when the right column carries a real visual / interactive element, not filler text.
* **Bento Background Diversity (mandatory):** ≥2-3 cells per multi-cell grid get real variation (image, brand-appropriate gradient, pattern, tint). Typography-only cream-on-cream bento = AI default.
* **Mobile collapse declared per section** in the same component — no "Tailwind handles it" assumptions.

### 4.8 Image & Visual Asset Strategy
Landing pages are visual products; text-only pages with fake-screenshot divs are slop.
* **Priority order:** ① image-gen tool (MUST create section-specific assets — hero photography, product shots, textures — at the right aspect ratio; do not skip because hand-rolled CSS feels faster) → ② real web images (`https://picsum.photos/seed/{descriptive-seed}/{w}/{h}`, brief-provided URLs, open-license sources if allowed) → ③ last resort: clearly-labeled placeholder slots (`<!-- TODO: hero product photo 1600x1200 -->`) + tell the user which images to provide. Never fill the page with hand-rolled SVG illustrations or div fake screenshots.
* **Even minimalist sites need real images:** ≥2-3 per page (hero + product/lifestyle + supporting); B&W minimalist photography for restrained briefs. Pure-text is incomplete work, not minimalism.
* **Real logos for social proof:** Simple Icons (`https://cdn.simpleicons.org/{slug}/ffffff`) or devicon (tech stacks). Invented brand → invent a matching SVG mark (monogram / ligature / abstract glyph); plain text wordmarks look generic. Logos must render in both light/dark mode. **LOGO-ONLY rule (mandatory):** logo wall = logos and nothing else — no industry/category labels underneath; alt-text optional.
* **Hand-rolled decorative SVGs strongly discouraged, never default** — acceptable only for explicit briefs ("draw me an SVG logo"), single simple geometric marks, or confident output quality.
* **Div-based fake screenshots banned.** Show a product via real screenshot URL, generated image, real mini component preview, or editorial photography. **Hero needs a real visual** — text + gradient blob is a placeholder, not a hero.

### 4.9 Content Density
Landing pages live on the first impression. Cut ruthlessly.
* **Section shape default:** headline ≤8 words + sub-paragraph ≤25 words + one visual asset OR one CTA.
* **No data-dump sections:** 20-row tables / 30-row award lists / giant pricing matrices → top 3-5 highlights + "View full list" link, marquee / carousel for breadth, or a different page if the data IS the product.
* **Lists >5 items need a different component, not a longer list:** 2-column grouped split · card grid · tabs/accordion · horizontal scroll-snap pills · carousel · marquee. A 10-row hairline spec list is the worst default — group into 2-3 chunks with sparse dividers or move to card-per-spec.
* **Spec sheets (the Marrow pattern):** `border-b` under every row is banned for cookware / hardware / apparel / artisan briefs. Alternatives: 2-col spec cards (name + large display value + one-line "why it matters") · scroll-snap horizontal pills · 3 clustered chunks with one soft divider each ("Materials" / "Cooking" / "Warranty") · featured-vs-rest (3-4 hero spec tiles + "View full specifications" disclosure).
* **COPY SELF-AUDIT (mandatory before ship):** re-read every visible string (headlines, subheads, eyebrows, buttons, body, captions, alt text, footer, errors); flag & rewrite: grammatically broken, unclear referents, hallucination-flavored ("elegant nothing" phrases, cute-but-wrong wordplay), or LLM-trying-to-sound-thoughtful (fake-craftsman labels, mock-poetic micro-meta). Unsure → replace with a plain functional sentence. AI-cute copy is worse than boring copy.
* **Fake-precise numbers banned** (`92%`, `4.1×`, `48k`, `5.8 mm`): fine only from real data (brief / brand / public metrics) or explicitly labeled mock — never AI-invented spec aesthetics.
* **One copy register per page** — no mixing technical mono, editorial prose, and marketing punch unless the brand voice explicitly calls for it.

### 4.10 Quotes & Testimonials
* Quote body ≤3 lines, never 6 (small footer-style testimonials may stretch slightly — spirit: "fits in a glance"). Longer → cut; a landing-page quote is a snippet.
* No em-dashes in quote text (`reference/ai-tell-catalog.md` §9.G bans them entirely).
* Attribution: name + role + optionally company. Never name only ("- Sarah").
* Real typographic quotes (" ") or none at all — not straight ASCII (").

### 4.11 Page Theme Lock
ONE theme per page; sections do not invert. Dark page = ALL sections dark — no light warm-paper section sandwiched between dark ones. Exception: an explicit "Color Block Story" / deliberate single theme switch with a strong transition — allowed once per page, never random alternation. Same-family background tints fine (`bg-zinc-950` + `bg-zinc-900`); `bg-amber-50` mid-page on a `bg-zinc-950` site is broken. Design-system theming (Radix Themes, shadcn `<Theme>`) is set ONCE at `layout.tsx` / page root.
---

## 5. CONTEXT-AWARE PROACTIVITY

These are tools, not defaults. Use them when the design read calls for them. **None of these fire automatically.**

* **Liquid Glass / Glassmorphism:** premium consumer, Apple-adjacent, luxury, media-overlay vibes; NOT dashboards, public-sector, "boring B2B." Beyond `backdrop-blur`: 1px inner border (`border-white/10`) + subtle inner shadow (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`); solid-fill fallback under `prefers-reduced-transparency`.
* **Magnetic Micro-physics:** `MOTION_INTENSITY > 5` AND premium / playful / agency brief. EXCLUSIVELY Motion's `useMotionValue` / `useTransform` outside the render cycle — never `useState` (Section 3.B).
* **Perpetual Micro-Interactions** (Pulse, Typewriter, Float, Shimmer, Carousel): `MOTION_INTENSITY > 5` AND the section actively benefits (status indicators, live feeds, AI-feel). Informational sections stay still — not every card needs a loop. Spring Physics (`type: "spring", stiffness: 100, damping: 20`), no linear easing.
* **"Motion claimed, motion shown."** `MOTION_INTENSITY > 4` → the page must actually move: hero entry transitions, scroll-reveal on key sections, hover physics on CTAs at minimum. A static page claiming `MOTION_INTENSITY: 7` is broken. Cannot ship working motion → drop the dial to 3, ship clean static. Never half-build breaking motion (cut-off ScrollTriggers, jumpy enters, missing cleanups).
* **MOTION MUST BE MOTIVATED (mandatory).** Every animation must answer "what does it communicate?" — hierarchy, storytelling, feedback, or state transition. "It looked cool" / "GSAP is available" are invalid reasons. Each ScrollTrigger / marquee / pinned section needs a one-sentence reason or it gets dropped.
* **MARQUEE MAX-ONE-PER-PAGE (mandatory).** Text marquees ("logos endlessly scrolling", "manifesto scrolling sideways") at most ONCE per page — two reads as lazy filler. Pick the one section where it serves the content; the rest get different layouts.
* **GSAP Sticky-Stack / Horizontal-Pan:** must be a REAL sticky-stack / pinned pan, not a sequential reveal. Canonical skeletons: `reference/motion-skeletons.md` — read before implementing. Shared signature failure: trigger fires before the section is pinned → fix `start: "top top"`, pin the wrapper, scrub the inner track.

### 5.A Canonical Motion Skeletons (externalized - read before implementing)
Sticky-Stack / Horizontal-Pan / Scroll-Reveal Stagger 三个模式的完整代码骨架（安装、HTML 结构、GSAP trigger 配置）外置于 `reference/motion-skeletons.md`——**实现任一模式前完整读取对应骨架并照抄 trigger 配置**（`start: "top top"`、pin、scrub 参数是踩坑收敛值），勿凭记忆重写。
### 5.D Forbidden Animation Patterns

* **`window.addEventListener("scroll", ...)`** is banned. It runs on every scroll frame, jank-prone, no batching. Use Motion's `useScroll()`, GSAP's `ScrollTrigger`, IntersectionObserver, or CSS `scroll-driven animations` (`animation-timeline: view()`).
* **Custom scroll progress calculations using `window.scrollY`** in React state. Same reason. Re-renders on every frame.
* **`requestAnimationFrame` loops that touch React state.** Use motion values (`useMotionValue` + `useTransform`) instead.
* **Layout Transitions:** Use Motion's `layout` and `layoutId` props for visible state changes (re-ordering lists, expanding modals, shared elements between routes). Do not wrap static content in `layout` props "for safety" - it costs measurement work.
* **Staggered Orchestration:** Use `staggerChildren` (Motion) or CSS cascade (`animation-delay: calc(var(--index) * 100ms)`) for reveal moments where sequence matters. For `staggerChildren`, parent (`variants`) and children MUST share the same Client Component tree.

---

## 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS

### 6.A Hardware Acceleration
* Animate ONLY `transform` and `opacity`. Never animate `top`, `left`, `width`, `height`.
* Use `will-change: transform` sparingly - only on elements that will actually animate.

### 6.B Reduced Motion (mandatory)
* **Any motion above `MOTION_INTENSITY > 3` MUST honor `prefers-reduced-motion`.** This is non-negotiable.
* In Motion: wrap with `useReducedMotion()` and degrade to static.
* In CSS: gate animations behind `@media (prefers-reduced-motion: no-preference)` or provide an override block under `@media (prefers-reduced-motion: reduce)` that disables.
* Infinite loops, parallax, scroll-hijack, and magnetic physics MUST collapse to static / instant under reduced motion.

### 6.C Dark Mode (mandatory for any consumer-facing page)
* Design for **both modes from the start**. Never ship light-only or dark-only without explicit user instruction.
* Use Tailwind `dark:` variant OR CSS variables for tokens. Pick one strategy per project.
* **Do not prescribe specific dark-mode colors here.** The brief decides. Maintain visual hierarchy, brand identity, and WCAG AA contrast (AAA for body) across both modes.
* Respect `prefers-color-scheme: dark`. Default to system preference unless the brand insists on one mode.

### 6.D Core Web Vitals Targets
* **LCP** < 2.5s. Hero image must be `next/image priority` or preloaded.
* **INP** < 200ms. Heavy work off main thread.
* **CLS** < 0.1. Reserve space for images, fonts, embeds.
* Run Lighthouse before declaring a page done.

### 6.E DOM Cost
* Apply grain / noise filters EXCLUSIVELY to fixed, `pointer-events-none` pseudo-elements (e.g., `fixed inset-0 z-[60] pointer-events-none`). NEVER on scrolling containers - continuous GPU repaints destroy mobile FPS.
* Be aware of bundle size. Motion is not tiny. Three.js is large. Lazy-load anything that's not above-the-fold.

### 6.F Z-Index Restraint
NEVER spam arbitrary `z-50` or `z-10`. Use z-index strictly for systemic layer contexts (sticky navbars, modals, overlays, grain). Document the z-index scale in a project constants file.

---

## 7. DIAL DEFINITIONS (externalized)
各拨盘等级的完整技术定义外置于 `reference/dial-definitions.md`：需确认 DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY 各级别的具体行为范围时读取。

## 8. DARK MODE PROTOCOL

Dual-mode by default. Never assume light-only unless the brief is print-emulating editorial.

### 8.A Token Strategy (pick one, stick to it)
* **Tailwind `dark:` variant** (default for utility-first projects): every color utility paired with its dark variant (`bg-white dark:bg-zinc-950`, `text-gray-900 dark:text-gray-100`).
* **CSS variables** (for shadcn/ui, Radix Themes, or component libraries with theming): define semantic tokens (`--surface`, `--surface-elevated`, `--text-primary`, `--accent`) and swap values under `[data-theme="dark"]` or `@media (prefers-color-scheme: dark)`.

### 8.B Do Not Prescribe Specific Colors Here
The brief and brand decide. This skill enforces only:
* **Contrast** - WCAG AA minimum for body text, AAA target for hero copy.
* **Hierarchy parity** - visual hierarchy that works in light must work in dark. If a CTA pops in light, it pops in dark.
* **Brand fidelity** - primary brand color stays recognisable. Don't desaturate the brand into a dark mode.
* **No pure `#000000` and no pure `#ffffff`** - use off-black (zinc-950, near-black warm gray) and off-white. Pure values kill depth.

### 8.C Default Mode
Respect `prefers-color-scheme` unless the brand insists. Add a manual toggle if either mode would lose key brand expression.

### 8.D Test in Both Modes Before Finishing
Open the page in both modes during development. Do not ship a page you've only seen in one mode.

---

## 9. AI TELLS (externalized)
AI slop 特征完整目录外置于 `reference/ai-tell-catalog.md`：生成前速查反模式 + Pre-Flight 逐条对照时读取（含 Production-Test Tells 与 Em-Dash Ban）。

## 10. REFERENCE VOCABULARY (externalized)
模式命名词汇表外置于 `reference/pattern-vocabulary.md`：§4/§5 或 `reference/redesign-protocol.md` 引用布局模式名、或需向用户准确描述布局方案时读取，用既有命名，勿自造近义词。
## 11. REDESIGN PROTOCOL (externalized)
重设计完整协议外置于 `reference/redesign-protocol.md`：Brief 判定为 redesign 时**生成前完整读取**（含模式检测 / 审计清单 / 保留规则 / 不可静默修改清单）。

## 12. COMPONENT APPROACH (no generic block library - by design)

预置代码只存在于**机械层**：`showcase/_skeleton.html`（deck 舞台机械）与 `reference/motion-skeletons.md`（GSAP 动效骨架）。通用版式/装饰积木（hero / pricing / bento…）**刻意不做**：可复用的页面区块配方会把每个项目推向同一模板——正是 §4.7 版式去重、AI-Tells (`reference/ai-tell-catalog.md`) 与 check-structure 反趋同门要防的病。风格层的"积木"由素材库承担（每套 DESIGN.md 的 components / signature moves）。若未来 longform 路径出现组件级重复失败，以 `reference/` 模式片段形式补充，不建独立 blocks/ 架构。
## 13. OUT OF SCOPE

This skill is NOT for:
* Dashboards / dense product UI / admin panels (use Fluent, Carbon, Atlassian, or Polaris from Section 2.A).
* Data tables (use TanStack Table or AG Grid).
* Multi-step forms / wizards (use Form-specific patterns; this skill won't make them better).
* Code editors (use Monaco / CodeMirror with their official skinning).
* Native mobile (use Apple HIG / Material directly).
* Realtime collab UIs (presence, cursors, OT-aware - different problem class).

If the brief is one of the above, **say so explicitly**, point to the right tool, and only apply this skill's marketing-page / about-page / landing-page parts to the surfaces where they apply.

---

## 14. FINAL PRE-FLIGHT CHECK (externalized)
完整 Pre-Flight Checklist 外置于 `reference/pre-flight-checklist.md`：**生成完成后、交付前逐项执行**。标注 [auto] 的项可用 `python showcase/check-landing.py <html>` 自动验证。

## 15-16. DECK MODE + STYLE CONTRACT (externalized)
Deck 模式完整规则外置于 `reference/deck-mode.md`：0.E 判定为 Deck brief 时**生成前完整读取**（§15 舞台骨架 / QA / CONFIG + §16 风格合约 / CJK 兜底）。

# APPENDICES (externalized to reference/)
- **设计系统安装命令** → `reference/design-systems.md`：§2 选定设计系统、装依赖前读（命令是 reality anchor，防幻觉版本号）。
- **Canonical Sources** → `reference/canonical-sources.md`：自造任何通用组件（按钮/表格/toast/导航…）前，先读对应官方源。
- **Apple Liquid Glass 诚实近似** → `reference/liquid-glass.md`：brief 要求玻璃拟态 / Apple 风 / backdrop-blur 时读（标注过的近似方案，非官方实现）。
