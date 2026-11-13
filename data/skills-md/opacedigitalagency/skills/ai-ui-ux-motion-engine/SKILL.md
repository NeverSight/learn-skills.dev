---
name: ai-ui-ux-motion-engine
description: Design, redesign, build, audit and validate distinctive production websites with cinematic scroll reveals, product films, burst or exploded-view effects, reference-led design systems, purposeful motion and multi-pass refinement. Use for landing pages, product sites, portfolios, interactive storytelling, premium or immersive web experiences, scroll-controlled product inspection, assembly or disassembly sequences, camera moves, image/video-led recreation, hero refinement, motion graphics, and anti-generic visual polish in Astro, React, Next.js, Vue, Svelte or static HTML/CSS. Infer cinematic intent from the requested experience or reference; the user does not need to say "wow" or name a tool.
---

# AI UI/UX Motion Engine

Create a project-specific experience from evidence. Treat references as
structural, visual and interaction inputs, never as permission to clone
branding, copy, code or protected assets.

## Non-negotiable rules

- Read applicable `AGENTS.md`, source-of-truth documents, design systems and
  current working-tree changes before editing.
- Define the bounded target, acceptance criteria, dependencies, spend and
  validation plan.
- Use the fastest route that can meet the accuracy target. For real products,
  default to `evidence-accurate` when authoritative sources exist; never trade
  accuracy silently for spectacle. State early when CAD, compositing or real
  footage is required.
- Preserve the existing stack unless the user explicitly authorises a change.
- Label observations, facts, proposals, generated visualisations and unknowns.
- Keep content and actions usable without motion, JavaScript or unrestricted
  data use.
- Never claim cinematic parity, product accuracy, accessibility, performance
  or release readiness without direct evidence.
- Never configure a paid service, accept provider terms or spend credits
  without user authority.

## Mandatory cinematic-intent gate

Activate this gate whenever the request or reference implies any of:

- a cinematic, premium or immersive scroll experience;
- a product opening, assembling, exploding, bursting or transforming;
- a camera orbit, dolly, macro inspection or authored product journey;
- photographic motion controlled by scrolling;
- a reference whose impact comes from changing viewpoint or object state.

The user does not need to use a trigger word or know which tool is required.

Before editing the page:

1. Classify truth mode:
   - `illustrative`: invented details are acceptable;
   - `identity-locked`: the same fictional or concept product must stay stable;
   - `evidence-accurate`: visible counts, geometry, labels and mechanics must
     match authoritative product evidence.
2. Confirm the reference or desired scenes, available source images or CAD,
   number and placement of flagship/supporting moments, target devices, media
   provider access and permitted credit/attempt cap.
   If the reference is a video, inspect keyframes plus any available transcript,
   prompt pack and description links; do not reconstruct its workflow from a
   summary or isolated screenshot.
3. State the dependency plainly. Photographic camera movement or physical
   transformation requires suitable source media plus an image/video
   generation, 3D or compositing route. CSS cannot invent unseen product views.
4. If the required provider or source material is unavailable, stop the
   cinematic asset work. Offer the static layout/fallback honestly; never
   substitute fades, zooms or stock background video and call it equivalent.
5. Create a cinematic brief from
   `assets/cinematic-brief.example.json`, validate it with
   `scripts/validate-cinematic-brief.mjs`, and obtain spend/terms authority
   before generation.
6. Produce one isolated private proof of the signature moment before redesigning
   the page or generating the full library.
7. Reject drift with automated technical checks and an overview contact sheet.
   Sample only risky transitions densely; inspect every frame only for a
   detected defect or evidence-critical mechanics. Use at most the approved
   attempts; then simplify the action, change technique or report the blocker.
8. Integrate only an approved asset. Never put a weak proof into a live hero to
   see whether surrounding UI rescues it.

Keep the first response concise: confirm the accuracy target, source readiness,
provider/spend authority, desired placements and delivery/time budget. Do not
ask the user to choose implementation details the skill can determine.

“First time” means selecting the correct professional route and bounded proof
immediately. It cannot guarantee that a stochastic provider’s first render
will pass.

When required information is missing, make the first response short:

> This experience depends on cinematic source motion, not ordinary CSS. I can
> produce it with an approved media provider and suitable references, but I
> first need the required accuracy, key scenes/placements, source assets,
> provider access and credit cap. I will prove one private signature sequence
> before changing the page and will not substitute basic photo reveals.

Read [cinematic-intake.md](references/cinematic-intake.md),
[generated-product-scrubber.md](references/generated-product-scrubber.md) and
[cinematic-prompts.md](references/cinematic-prompts.md) completely when this
gate activates.

## Standard workflow

### 1. Establish the brief and baseline

Record goal, audience, routes, content/evidence rules, target devices,
framework, release boundary and current build/test state. Read
[workflow.md](references/workflow.md).

### 2. Extract references

Map composition, typography, colour, imagery, entrances, scroll, hover, drag,
camera movement, object state and timing. Distinguish reusable principles from
identity-specific material. For a local recording run:

```bash
bash scripts/extract-reference-frames.sh <video> <output-directory>
```

Read [media-pipeline.md](references/media-pipeline.md).

### 3. Lock one direction

Write seven implementable lines covering goal/audience, tone, composition,
typography, colour/media, motion/reduced-motion and one signature
differentiator. Do not proceed on “clean and modern” alone.

### 4. Select the architecture

Choose the lightest mechanism that preserves the intended experience:

- CSS for local state and entrance changes;
- Intersection Observer or native scroll animation for simple reveals;
- an existing motion library for coordinated component motion;
- GSAP for deliberate pinning/timelines;
- generated or filmed media for photographic camera/object change;
- all-intra video or canvas frames for exact scroll scrubbing;
- WebGL/3D for freely manipulable viewpoints or reliable exact mechanics.

For cinematic product motion, the media is the experience. Prove it first; do
not expect CSS transforms to create the missing film.

Use the lean scalable default:

- one master flagship per major journey;
- reuse approved chapters, crops and clean reversals where they stay truthful;
- add a 3–5 second supporting shot only for a genuinely new fact;
- use code-native motion everywhere else.

Target 15–30 minutes for a private proof when sources/provider are ready,
30–60 minutes for an approved flagship plus scroll delivery, and 5–10 minutes
for a derivative or supporting integration. Allow 75–120 minutes only for new
or inconsistent source packs, evidence-critical mechanics, CAD or compositing.
These are targets, not guarantees. If a timebox is exceeded, report the
evidence and obtain approval before continuing.

### 5. Implement in bounded passes

Build semantic content, macro layout, the approved signature motion,
micro-states, responsive composition and editorial polish. Keep text, labels
and actions in the DOM rather than baking them into generated media.

Prevent process bloat: prove media before page work; perform provider and
source research once per run; do not create multiple redesigns or documentation
passes before proof; run a focused component test first and the full regression
once after final integration; capture technical evidence automatically.

When the client/model supports subagents, default to parallel execution whenever
two or more independent streams exist and delegation saves time. Parallelise
source audit, provider capability/current cost, brief validation, media
preparation/QC, browser checks and documentation. Give visual interpretation,
truth mode, creative direction, spend and acceptance to the lead
high-capability multimodal model; use faster capable models for bounded
mechanical work. Never assign visual QC to a model that cannot inspect the
media, let agents edit the same files concurrently, or parallelise paid
generation, approvals or dependent steps. Rejoin before decisions.

### 6. Validate

After each component, test pointer, keyboard, touch, reduced motion, target
viewports, console/runtime behaviour and focused checks. For cinematic media,
also verify identity/count/geometry, first/end states, forward/backward scrub,
crop and fallback. Then run:

```bash
node scripts/audit-motion-safety.mjs <project-directory>
node scripts/validate-scroll-media.mjs <shipping-scroll-master.mp4> \
  --poster <shipping-poster.jpg>
node scripts/validate-package.mjs
```

Fail closed: if the media validator fails, the poster reappears after the first
decoded frame, seeks overlap, rapid direction changes expose stale or blank
frames, the poster changes crop or scale against the first decoded frame, or
the film is only still-image crossfades, do not ship the scrubber. Use the
numbered canvas sequence or a static fallback until the complete gate passes.
Six settled checkpoints alone are insufficient.

Run the project’s full regression baseline before handoff. Read
[verification.md](references/verification.md).

## Resource routing

- [cinematic-intake.md](references/cinematic-intake.md): mandatory questions,
  pushback, tiers, spend and stop rules.
- [cinematic-prompts.md](references/cinematic-prompts.md): exact reusable
  single-action, flagship and illustrative prompt contracts.
- [generated-product-scrubber.md](references/generated-product-scrubber.md):
  cinematic production and scroll-delivery golden path.
- [media-pipeline.md](references/media-pipeline.md): references, ffmpeg,
  all-intra video, frames, posters and delivery.
- [tool-connections.md](references/tool-connections.md): provider preflight and
  external-tool boundaries.
- [motion-patterns.md](references/motion-patterns.md): code-native motion.
- [framework-recipes.md](references/framework-recipes.md): stack-specific
  implementation.
- [accessibility-performance.md](references/accessibility-performance.md):
  motion safety and performance.
- [prompts.md](references/prompts.md): user-facing request templates.
- [source-coverage.md](references/source-coverage.md): provenance and known
  limitations.

Reusable assets and scripts:

- `assets/cinematic-brief.example.json`
- `assets/cinematic-scroll-controller.js`
- `scripts/validate-cinematic-brief.mjs`
- `scripts/render-cinematic-prompt.mjs`
- `scripts/prepare-scroll-media.sh`
- `scripts/validate-scroll-media.mjs`

## Completion report

Report the selected direction, media tier and truth mode; references/provider,
model/settings, attempts and credits; files changed; QC and browser evidence;
fallbacks; unresolved visual inference; and private, staged or production
release status.
