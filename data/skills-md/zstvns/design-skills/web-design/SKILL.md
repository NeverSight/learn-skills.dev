---
name: web-design
description: "Apply a brand's defined visual system to a real, conversion-focused website — designing and building it in custom code, with real copy given its proper emphasis. Use when the user mentions 'website design,' 'design my site,' 'build a landing page,' 'homepage,' 'marketing site,' 'product page,' 'pricing page,' 'redesign our website,' 'hero section,' or wants to ship a site. This is where the approved identity becomes a live, shipped surface — not a mockup, working code."
metadata:
  version: 1.12.0
---

# Web Design

You apply a brand's **defined visual system** to a live website and **ship the code** — designing and building at the same time, in custom code. This is the first Application skill: the color roles, type rules, motif, and signature element from `creative-direction` become a real conversion surface, built around real copy.

Read `design-principles` first. This skill is where its rules meet a browser: hierarchy is the job, restraint protects the message, contrast-not-competition, "state why or the default stands." Most of what separates a *designed* site from an *assembled* one is here.

> **Position in the sequence:** after `creative-direction` (the system) and `logo-design` (the mark), the first of the Application skills. It consumes the identity; it does not define one. **Custom code is the medium** — this skill builds bespoke HTML/CSS (and the project's framework if one exists), not Webflow or Framer.

## Front-Door Diagnosis — Settled Brand, or Rework?

Before anything, diagnose where the brand is. Open `.agents/design.md`, `.agents/brand.md`, and `.agents/product-marketing.md` — by this stage **all three should exist.** Then ask one question:

> *Are we applying a settled brand, or reworking one from scratch?*

Four routes, in the plain language a client uses:

- **Refine the existing elements** ("we like our brand, the site's just weak") → Optimization. **Proceed** — this is the skill's home.
- **Light creative direction** ("keep the name and logo; new type, color, graphics") → light Evolution. Proceed only if `design.md` already records those new choices; if it doesn't, the deltas are undefined → **route back to `creative-direction`** for the light pass first.
- **Full rebrand** ("new everything") → Revolution → **stop and route back to `creative-direction`.** Do not design a site on an undefined system.
- **Heavy Evolution** (the core system is genuinely changing) → **route back** too.

Routing back holds **even if the user arrives with a logo already** — a mark without the system around it isn't enough to build a coherent site; push them back. The rule of thumb: **route back whenever the visual system is being defined or changed; proceed only when it's settled.**

**If `.agents/design.md` is missing, that *is* the "go back" signal** — there's no system to apply yet. Route to `creative-direction`. If `.agents/product-marketing.md` is missing or the page has no copy, route to the marketing library's `copywriting` / `website-copy` first: **the site is built around the copy, never the reverse.**

## Copy First — the System Is the Stage, Not the Show

The single most important input is the words. Read the copy in `.agents/product-marketing.md` (audience, voice, positioning, and the page copy itself). **The designer's job is to take what's being said and give it proper emphasis, joy, and delight** — not to build a template and pour copy into the gaps. Wireframe-first thinking is the fastest tell of an assembled page. If the copy isn't written, get it written first.

**Size follows the content, not a template.** The headline scale is dictated by what the copy actually is — a hook line that's meant to be *completed* by a second line (a typed continuation, a rotating phrase) means a *smaller* headline, not a giant one-liner sitting alone. A hero with a lone hook and no follow-through reads as unfinished. Design the content you have; don't force it into a fixed hero shell.

The visual system serves the message. Design serves the message. The site is the stage; the copy is the show.

## When You Reference an Existing Site, Be Faithful to It

Redesigning a live site, or building "like" a reference? Then **look at what's actually happening on that site** — don't approximate it from memory. Full method in [references/faithful-replication.md](references/faithful-replication.md).

- **Port every section.** Inventory the source top to bottom and carry each section over — right copy, right order. A "redesign" that silently drops the terminal-signup, the capabilities section, or the orbital product visual isn't a redesign, it's a different site.
- **Match the action the site is driving.** Read what it's *encouraging the visitor to do* and reproduce that mechanism, not just the words. If the hero invites you to enter a URL and get a free plan, the redesign's hero needs that URL field and that button — the primary action is the point of the page.
- **Pull the real assets.** Integration/partner logos are real and available (a Relume or brand-asset library, the source's own markup, a brand-SVG source like simple-icons). **Use the real logos** — never substitute an icon-plus-text stand-in, and never ship a low-contrast logo strip.
- **Tell the visual's real story.** A product illustration has to communicate what the product *does* — e.g., an orbital that shows work (writing, optimizing, launching, researching) looping *around* the agent, not decoration that misses the point.
- **Run the match loop.** Write a source-specific checklist before coding, then grade the build against side-by-side screenshots at 1440 and 390px — with section count/order and hero proportions *measured*, not eyeballed. Two rounds, then hand off for human review. See [references/faithful-replication.md](references/faithful-replication.md) → Match loop.

You are not producing a comp for someone else to implement. **You design by building** — the design decisions *are* the code. Output real, production front-end:

- **Match the project's stack if one exists** (Next.js / Tailwind / shadcn per the repo's conventions); otherwise ship clean, self-contained HTML/CSS. Framework-agnostic by default.
- **No Webflow, no Framer.** This skill exists because the work has moved to custom code — bespoke markup you can push as far as the craft demands, with none of the builder-tool ceilings.
- **Spacing in rem, fluid with `clamp()`** — never fixed px in production. Horizontal padding percentage-based; section padding fluid. See [references/craft-details.md](references/craft-details.md).
- Cross-reference the marketing library's `website-build-*` skills **only** if the user explicitly wants a platform build (Webflow/Framer) — that's the exception this skill was built to move away from.

## Apply the System

Pull the system from `.agents/design.md` — don't re-derive it, don't invent alongside it:

0. **Place the locked logo; never rebuild it.** Take the mark from the canonical files the `logo-design` skill wrote — `.agents/assets/logo/logo-lockup.svg` (nav, footer), `logo-icon.svg` (favicon, tight spaces), the `-inverse` / mono variants on dark or single-colour grounds. It is **one locked element**: don't set the wordmark yourself, don't pick your own gap, don't recolour it to match an accent, don't crop it or drop it in a box, don't scale it below its minimum size, and respect its clear space. If the surface needs a variant that isn't in the folder, route back to `logo-design` — don't improvise one in CSS.
1. **Color by role.** Background, text (primary/secondary), **action/CTA**, support. Five stops per color, not ten. Use the tokens as defined.
2. **The CTA color is one deliberate, always choice — and it is *not* a text or graphic color.** Pick a single color that reads as *progression forward* (a green or blue, heuristically) and use it for the primary action everywhere. It must be **chromatically distinct** from the color carrying your headlines, icons, and decoration — otherwise the button doesn't pop, it blends. **Use it only on actual CTAs** — never a headline, never a decorative accent. A *separate* brand accent carries repeated emphasis (and even that with restraint); if the forward color starts showing up on labels and graphics, it stops meaning "act." Never style a non-interactive element like a button, either — a fake CTA erodes the real one. And give the CTA a **differentiated shape** — a pill or rounded form, not the same squared rectangle as every card — so the action reads at a glance.
3. **Type by role, for contrast not competition.** Display, heading, body — each with a clear job. Don't default to bold; body is regular/book weight, heavier weights reserved for moments that earn it. Heading leading 1.1–1.3, body 1.5–1.6. Secondary text is a softer shade/opacity than headings — hierarchy even within one face. **Change body copy to the secondary text color across the whole page in one systematic pass**, not section by section (see [references/craft-details.md](references/craft-details.md) → work systematically).
4. **The motif carries the brand — but restrained where the message must win.** Deploy the signature element as texture, pattern, or a recurring detail (this is where distinctiveness must *survive application* — see `design-principles`). **In the hero, calm it down:** a busy motif behind the headline and primary action is distraction, not identity. Let the message and the CTA lead; thread the motif more assertively in later sections.
5. **Eyebrows sparingly.** A mono/uppercase kicker over *every* section is clutter — it flattens hierarchy instead of building it. Use an eyebrow only where a section genuinely needs the label; most sections lead with the headline.
6. **Depth, light, and surface transitions** per the system's intent — multi-layer shadow stacks (not flat `shadow-md`), gradual background shifts and earned dark/light flips over hard-edged banded sections.

## Build Section by Section — Give Each Thing a Lane

Work the page as a sequence, never each section in isolation. Full per-section playbook in [references/section-patterns.md](references/section-patterns.md).

- **Name each section's one job**, then give the element that carries it its own lane and scale it to that rank. A positioning line gets a stage; a trust strip gets a full-width lane, not a corner of the hero; a hero object gets a spotlight. Supporting detail recedes.
- **Rhythm is a vocabulary of section *types*, not a column count.** Rotate through genuinely different section types — each a different *medium* — and never play the same one twice: asymmetric hero, a **full-bleed human/video moment**, an illustration/contrast beat, an oversized aphorism, a **pinned scroll-telling sequence** (a heading pins while statements cycle beneath giant ghost numerals — choreograph it with `motion-design`), colored cards, a spotlit object reveal, a carousel. **Change the medium** (UI → video → illustration → photo → cards), not just the layout. Then **unify** the variety with one through-line texture + strict color discipline, use **scale contrast** (ghost numerals vs. tiny copy), and leave **quiet between the loud** beats. The failure mode: *one instrument played the whole song* — the same card/panel idiom repeated with only the column count changing. Full vocabulary in [references/section-patterns.md](references/section-patterns.md); study conversionfactory.co for how it's paced.
- **Balance every text section with a visual.** A text-only section that should carry an image reads as unfinished. Show the product in **layered, overlapping mockups** — a device, a card, a sticker at a slight rotation, real depth — the way strong marketing sites do, rather than a flat screenshot or nothing.
- **Consolidate.** Three substantial sections beat five thin ones. Whitespace is emphasis, not just breathing room.
- **CTAs, logos, and hover states are content, not decoration.** Primary and secondary CTAs stay distinct in every state including hover. Partner/integration logos get one normalized trust lane — **real logos**, optical (not pixel) sizing, one color story, and enough contrast to actually read.

## Motion — Carry the Brand's Motion Character, Then Hand Off

**Motion is part of the system, not a garnish added at the end** — and like color and type, its character is **brand-derived**. Read the motion character from `.agents/design.md` and the **emotional target**: a playful, eccentric brand earns springy, generous, frequent motion; a serious, premium brand earns subtle, controlled, sparing motion. **"Slick" is not the universal goal** — rendering a playful brand's motion tastefully minimal flattens it into a generic one. Never substitute a house default for the brand's own feel.

Then split the work by the job each animation is doing — this is the line between what you handle here and what `motion-design` handles:

- **Functional / UI motion — build it here.** Hover and focus states, press feedback, the CTA's states, disclosure and menu transitions, section reveals. This motion has a job: feedback, orientation, cause and effect. Keep it **utilitarian regardless of how playful the brand is** — fast, unobtrusive, out of the way.
- **Expressive / storytelling motion — hand off to `motion-design`.** Choreographed page-load sequences, the **pinned scroll-telling beat**, signature product-visual behavior, hero moments, and any content-specific idea whose purpose *is* the feeling. That's where brand latitude gets spent, and where the twelve principles pay off.

### The floor you build to here

These are the `motion-design` rules that matter most on a marketing site — apply them inline; you don't need the full skill to get them right:

- **A named easing set, and `ease-out` as the workhorse.** Custom curves, not raw `linear` (the loudest amateur tell) and not one undifferentiated `ease` on everything. Entrances and exits both read better decelerating into rest.
- **UI transitions under ~300ms.** Hover/press in the 100–200ms range; anything slower has to earn the wait. Match duration to the *mass* of the thing moving — small fast, big slow.
- **Press feedback.** A subtle scale-down (~`0.97`) on `:active` so the interface feels like it's listening.
- **Entrances overlap and stagger; they never queue.** Grouped elements share timing and offset by small delays (~40–80ms) rather than each waiting for the last to finish. This one move is most of the distance between "fine" and "expensive."
- **Animate `transform` and `opacity` only.** Animating `width`/`height`/`top`/`left`/`box-shadow` triggers layout or paint and janks — and that jank reads as a cheap build.
- **Reveals are hierarchical, not uniform.** Fade-up on every element identically is a named slop trope ([references/web-slop.md](references/web-slop.md)) — the failure is the *sameness*, not the amount. Reveal what carries the message; leave the rest still.
- **`prefers-reduced-motion` is non-negotiable.** Ship a reduced path (opacity-only or instant) for every non-trivial animation, and kill ambient/parallax motion entirely under it.

**Reach for GSAP when the motion gets real.** CSS transitions and `@keyframes` are the right tool for hover, focus, press, and simple reveals — don't pull in a library for what the platform does natively. But for **smooth, complex, choreographed motion**, GSAP is the best option available and now entirely free (all plugins included, since Webflow took it over): **ScrollTrigger** for scroll-driven sequences and pinning (exactly the pinned scroll-telling beat above), **SplitText** for staggered word/line reveals, and **Flip** for shared-element/layout transitions. Its timelines make overlapping, staggered choreography far easier to control than hand-tuned CSS delays, and its interpolation is noticeably smoother on demanding sequences.

Full craft — the twelve principles, the technique toolkit, easing/duration tokens, and the motion-slop checklist — lives in `motion-design`. Reach for it whenever the site needs expressive motion rather than just a competent floor.

## Tooling & References — Use What's Connected, Fall Back Gracefully

The build is faster and the rhythm richer when you lean on real tools — but **never block on a missing one; degrade to the next option.** Check `.agents/brand.md` → **Toolkit** first for what the operator has (including the image generator behind the page's rich media), and write back anything new you find connected. **Imagery comes from the `art-direction` library** (`.agents/assets/imagery/approved/`) — place what's there; route anything new back to `art-direction` rather than sourcing it ad hoc.

- **Relume MCP** *(preferred accelerator, when connected)* — generate the **sitemap** (top-level and parent/child pages), **wireframe** from its component library (which varies layouts and seeds rhythm), and a **style guide** whose base color auto-expands to 5-stop tints and sets the single always-CTA color — all of which ports into the build. Group pages by shared format (all solution pages one structure, varied content).
- **`frontend-design` skill** — when Relume isn't available, for distinctive, production-grade frontend.
- **Claude Design** — optional canvas exploration with the published system, handed off to Claude Code; the handoff is a starting point for the custom build, not the build.
- **`web-design-guidelines`** — the UX/UI + accessibility compliance pass.
- **Mobbin / Refero MCP** — pattern intake: study how strong sites solve a section before you build it.
- **Reference-site intake** — pull in the popular sites the client admires; name what to steal and what to avoid.
- **GSAP** *(preferred for real motion — free, all plugins)* — timeline-based choreography, **ScrollTrigger** (scroll sequences + pinning), **SplitText** (staggered text reveals), **Flip** (shared-element transitions). Use CSS for simple states; use GSAP when the sequence is complex or must be genuinely smooth. See the Motion section above and `motion-design`.
- **three.js / WebGL** — when the brand genuinely warrants ambitious 3D or interactive depth (not as decoration).

## Validate Before You Ship

Run your own build through the same gauntlet the audit runs — **adversarially, on the rendered page in a browser, not the code in your head** (see `design-principles` → Judge Your Own Work on the Competitor's Bar). Render it, screenshot it, and:

- **Score it against the audit categories** vs. the confirmed competitor set at a rival's harshness — Creative Direction, Color, Type, Layout. Would this earn 4–5?
- **Run the web-slop check** ([references/web-slop.md](references/web-slop.md)) and **list what it finds** — the tropes actually on the page (bold-as-default, banded sections, uniform icon grids, CTA color bleeding everywhere, eyeballed nested radii). "No slop here" is a reflex, not a result; produce the list or an earned, specific "none, because —."
- **Cover-the-logo carry-through:** with the mark hidden, is the built page still recognizably this brand? If the distinctiveness lived only in the logo, the system didn't survive application.
- **Responsive.** Check every real breakpoint the build uses; mobile fixes are additive overrides, never touching the desktop base.
- **Accessibility report.** Check and report each item as **Passed**, **Issue found** (with the fix), **Needs manual testing**, or **N/A**:
  - Heading order and semantic tags
  - Alt text (decorative images marked decorative)
  - Accessible names on icon buttons, links, and form fields
  - Visible form error states
  - Contrast
  - Reflow at each real breakpoint
  - Reduced motion and autoplay
  - Meaning carried only by color or animation
  - `<html lang>`

  **Never mark Passed anything you could not fully test** — an unverified item is not a pass. Screen-reader flow is always Needs manual testing. What to check per item, how to test it on the rendered page, and the report format: [references/accessibility-report.md](references/accessibility-report.md). For the full interface/accessibility compliance pass, use `web-design-guidelines`.
- **Motion check — watch it, don't screenshot it.** Static captures cannot audit motion. Play the page back: does the timing/easing match the brand's character, or did you default to a generic ease? Is anything on `linear`, queuing instead of overlapping, or janking on a layout property? Toggle `prefers-reduced-motion` and confirm the page is calm and usable.
- **Copy check.** Does the layout give the words their proper emphasis, or did the design bury the message?
- **Agent parity.** AI agents and crawlers get the same page visitors see. No hidden text, no content swapped by user agent, user-writable content (reviews, CMS entries, form-fed text) sanitized before it's published, and the real content present in the server-rendered HTML — not only after client JS runs. View the raw HTML response with JS off and confirm the copy is there. (Principle: [agent security is product security](https://webflow.com/blog/agent-security-is-product-security).)

## The Deliverable

- **The shipped site** — production front-end code in the user's project, designed and built together, applying the approved system.
- **Append the "Application Notes" section of `.agents/design.md`** (the living record — see `creative-direction` → design-doc-template.md): component conventions adopted, the tokens as used, any place the system flexed and whether the flex is now canon — dated — so later pages and `collateral-design` inherit decisions instead of re-deriving them. Don't duplicate the founding sections — reference them.

## Non-Negotiables

- [ ] Front-door diagnosis run; Revolution / heavy Evolution routed back to `creative-direction` (even if a logo already exists)
- [ ] `.agents/design.md`, `brand.md`, `product-marketing.md` read; system applied, not re-invented
- [ ] **Locked logo placed from `.agents/assets/logo/`** — not rebuilt, recoloured, cropped, boxed, or re-typeset; correct variant for the ground
- [ ] Copy exists and drives the layout — no wireframe-first, no filler
- [ ] If referencing an existing site: every section ported, the primary action reproduced, **real logos** pulled (no icon+text stand-ins); **match loop run** (section count/order and hero proportions measured at 1440 + 390px, max two rounds, then human review)
- [ ] Real custom code shipped (project stack matched or clean HTML/CSS) — not a comp, not Webflow/Framer
- [ ] CTA color is a single forward color, distinct from text/graphics, used *only* on CTAs (never headlines/decoration), pill/rounded, reserved; no fake CTAs; separate brand accent carries emphasis; five stops; bold not the default
- [ ] Eyebrows sparing; hero motif calmed so message + action lead; motif carried assertively later; distinctiveness survives cover-the-logo
- [ ] Rhythm goes beyond the column trio — unexpected layouts and varied media (vector/photo/icon/illustration); text sections balanced with layered visuals
- [ ] Columns top-aligned, content left-aligned by default (center only genuinely-centered blocks); each section demarcated (header + spacing) so repeated L-R rows don't blur into one
- [ ] Headline size follows the content; contrast checked; no widows (headlines balanced); real photography pulled where imagery is called for
- [ ] Craft floor met (rem/clamp, layered shadows, optical alignment, nested radii, distinct CTA states); global changes done systematically
- [ ] **Motion character taken from the brand** (playful ≠ premium; no house default); functional motion kept utilitarian and expressive/storytelling motion handed to `motion-design`
- [ ] **Motion floor met** — named easing with `ease-out` as workhorse (no raw `linear`), UI transitions under ~300ms, press feedback, entrances overlap/stagger rather than queue, `transform`/`opacity` only, reveals hierarchical not uniform, `prefers-reduced-motion` honored
- [ ] **Tabbed through every interactive piece on the rendered page** — each one built on a headless behavior library, not hand-rolled ARIA (see [references/tooling.md](references/tooling.md) → Interactive behaviors)
- [ ] **Focus confirmed to return to the trigger after each popup or dialog closes**
- [ ] Adversarial self-audit on the *rendered* page (web-slop tropes listed, not "none"); responsive + accessibility pass; spelling/grammar + OG image checked
- [ ] **Agent parity** — agents and crawlers get the page visitors get: no hidden text or UA-swapped content, user-writable content sanitized, real content in the server-rendered HTML

## Related Skills

- `design-principles` — the craft beliefs this skill applies
- `creative-direction` — supplies the visual system (hard prerequisite); route back for Revolution / heavy Evolution
- `art-direction` — the photography, illustration, icons, and textures this skill places; route new imagery needs there
- `logo-design` — the mark, applied here
- `brand` — the audit whose categories are this skill's acceptance test
- `motion-design` — the motion layer on top of this one: build the functional/UI floor here, hand off expressive choreography, scroll-telling, and signature motion there (it expects a structurally-sound surface, so run it *after* the build)
- `collateral-design` — applies the same system to fixed-format mediums (decks, print, ads, social, OG images, email graphics)
- `design-critique` *(planned — not yet shipped)* — will judge the shipped site against the emotional target and latitude
- `frontend-design` — distinctive production-grade frontend when a build accelerator isn't connected
- marketing library: `copywriting` / `website-copy` (the copy comes first), `cro` (optimize existing pages), `web-design-guidelines` (accessibility), `website-build-*` (only for an explicit platform build)
- tooling (use when connected, fall back gracefully): **Relume MCP** (sitemap · wireframe · style guide), **Mobbin / Refero MCP** (pattern intake); see [references/tooling.md](references/tooling.md)
