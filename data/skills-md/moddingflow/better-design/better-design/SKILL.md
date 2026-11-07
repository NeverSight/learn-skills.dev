---
name: better-design
description: "Design, improve, and validate UI/UX for applications, websites, native interfaces, and games: an art direction derived from the product, a coherent visual system kept in the project's DESIGN.md (read first, created when missing, the single source of interface values), measured layout geometry (equal spacing, shared alignment lines, content centered inside small controls, nothing clipped or touching its container edge), a catalog of AI-slop patterns that rejects page narration and redundant helper text, a living motion language (press feedback, transitions, choreography, reduced motion), an Apple-like ultra-minimal default style, an opt-in pool of signature effects, clear actions, accessibility, drag and drop anticipated from the start (drop zones for every upload), and real states (including skeleton loaders and loading splash) without AI slop. Use for interface creation, redesigns, focused UI changes, animation and interaction polish, design plans, and UX audits; not for backend-only tasks."
license: MIT
metadata:
  version: "1.7.1"
---

# Better Design

Make the requested task clear and actionable: the user can see where they are,
understands an action before activating it, receives a result, and can recover from an error.
Evaluate coherence, expressiveness, and accessibility separately. Do not promise perfect UX.

## 1. Establish scope and visual grounding

- Choose a mode: creation, focused improvement, audit, or plan. Keep audits read-only;
  do not implement changes in a plan. Do not add features the user did not request.
- Establish the platform from the request and project. Only when context is absent, use
  responsive web, semantic HTML, and WCAG 2.2 AA as the initial target.
- Define the actual device and viewport matrix before composing or changing a responsive
  surface. For a website, include mobile, tablet, desktop, and ultrawide layouts that the
  product supports; for a mobile game, include small and typical phones plus tablets. Design
  constraints and layout behavior must adapt to those surfaces rather than merely shrinking
  a desktop composition. For browser work, include browser zoom in the matrix because 75%,
  100%, and 150% can expose different clipping, density, reflow, and interaction failures.
- Before any UI work, look for the project's DESIGN.md (root, `docs/`, `design/`, or the path
  named in agent instructions) and read it completely. It is the single source of interface
  values: fonts, type scale, color roles, spacing, radii, component sizes, icons, and motion.
  Take every value in new or changed code from it by role or token name; never eyeball,
  round, or introduce a near-duplicate. Rules are in [design-md.md](references/design-md.md).
- Inspect the existing screen in the current runtime or through confirmed current captures,
  then inspect nearby components, tokens, styles, and project rules. The absence of DESIGN.md
  does not mean there is no design system: the code tokens are then the system.
  Preserve unrelated work in progress.
- Distinguish an implementation defect from a redesign request. Address the cause first:
  unclear ordering, an unpredictable action, poor feedback, data loss, or lost content.
- Make decisions in this order: explicit task and constraints → DESIGN.md and the existing system →
  platform conventions → domain tasks → this skill's configurable baseline.
  Functionality and applicable accessibility requirements apply at every level.
- **Default visual direction.** When the user names no visual style and the project has no
  DESIGN.md, brand, code tokens, or live UI to inherit, build in the house style: premium
  ultra-minimal in the spirit of Apple (black canvas, near-white Geologica at weights 500 and
  340, two grays, one blue for links and focus, pill actions, surfaces separated by tone,
  real content as the only color). Rules and the ready DESIGN.md preset are
  in [house-style.md](references/house-style.md); read it whole before writing any style.
  Two misreadings send agents elsewhere, so check them explicitly (house-style.md section 1):
  the product's domain, industry, audience, or name is not a visual cue ("a coffee roastery",
  "for developers"), and untouched scaffold defaults are not a system to inherit (the
  shadcn/ui default theme, Tailwind's default palette, create-next-app, Vite, or Expo
  starters, Bootstrap, MUI, or Chakra defaults); map the house style onto them instead.
  When it applies, start from the reference file
  [house-style.html](assets/house-style.html), not a blank page: take its tokens, type
  classes, nav, buttons, tiles, and section rhythm (or port them into the stack's
  components), then replace its content (house-style.md section 1). Any visual cue from the
  user (colors, mood, theme, reference, brand, audience style) overrides it: follow the
  request, and apply only the parts of the house style the request leaves open and does not
  contradict. Never restyle an existing product into it unless asked. Games keep their own
  art direction.
- Preserve the established brand, density, game-like, editorial, or expressive composition.
  Do not replace them with a generic gray CRM. For a real conflict, choose the smallest
  accessible adjustment and explain the specific deviation.
- Clarify only unknowns that materially change the decision; state reasonable assumptions
  briefly. This skill does not introduce a new approval or HTML gate. Existing project
  requirements for prototypes, approval, and builds remain applicable.

## 2. Define the task and a proportionate contract

- Describe the primary scenario in plain language and its observable outcome.
  Walk through entry → action → result → error/retry → back/cancel.
- Separate the primary task, secondary actions, and help. Choose names and patterns familiar
  to the user; keep navigation and action locations consistent across screens.
- A single fix needs only a short record of the changed decision and checks.
  For a new flow, write a compact contract before implementation; it is a working tool,
  not a mandatory document for the user.
- Use [design-contract.md](references/design-contract.md) for structure,
  numeric defaults, and exceptions. The [JSON example](assets/design-contract.example.json)
  illustrates the format; do not add it wholesale to the project for a small change.
- Limit the contract to the platform, goals, existing system, direction, affected components,
  their actions/states, responsive behavior, and acceptance evidence.
  A planned check is not a completed check.

## 3. Set an art direction before styling

Negative rules only move output to the next most common template; character comes from a
process. When creating or redesigning a surface whose identity is part of the task (brand,
landing, portfolio, consumer app, game, editorial, launcher), follow
[art-direction.md](references/art-direction.md) before choosing tokens. When the house style
applies (section 1), palette, type, shape, and motion tokens come from its preset; still write
the concept, and let it choose the imagery, each section's leading element, and one signature
detail (house-style.md section 10). Otherwise:

- Derive a one-sentence concept from the product's domain, audience, and content — an object,
  place, or craft from that world — not from adjectives such as "modern, clean, minimal".
  Add three target qualities and three concrete anti-qualities.
- Collect 3–5 real references (user-provided ones first; never AI-generated images) and note
  for each exactly what is taken: rhythm, density, number presentation, material, light.
- Sketch 2–3 directions that differ by their leading device (typographic, image-led,
  structural), then choose one with a reason tied to the task and audience.
- Derive palette and type from the concept: a palette with a stated origin and tinted
  neutrals; three type candidates and a reasoned choice. Plan one or two signature details;
  the optional pool in [effects-library.md](references/effects-library.md) holds tested ones.
- Derive the motion character from the same concept: how things in that world move (tempo,
  weight, physics, whether anything springs) plus one signature motion detail. Palette, type,
  and motion must read as one voice; see [motion.md](references/motion.md).
- Within DESIGN.md, an existing brand, or a design system the direction is inherited: take it
  from DESIGN.md or state it in one sentence from the live surface, and work inside it. Dense working tools express character
  through precision and data typography; with no system and no user cue they take the house
  style's app scale and palette with the neutral fallback's density.
- Record the direction in the contract (`direction`, including `direction.motion`) and plan
  `distinctiveness` and `motion` checks. Write the chosen direction and its tokens into
  DESIGN.md so later screens and sessions build from the same values.

## 4. Build a coherent system of decisions

- Reuse tokens and components from DESIGN.md and the code tokens. For a new system, define
  semantic roles for color, typography, spacing, radius, layers, and motion; then select
  component variants.
- Keep the sets closed so every screen is built from the same parts: one or two font families,
  a stepped type scale of a few roles, a fixed spacing scale, a few radii, and fixed component
  sizes (for example button sm/md/lg). Same role, same value on every screen. A missing value
  is a system decision: add the role to DESIGN.md and the code tokens in the same change.
- Create DESIGN.md from the [template](assets/DESIGN.template.md) when creating an interface
  from scratch (from the [house-style preset](assets/DESIGN.house-style.md) when the house
  style applies), or when a redesign or multi-component change finds none; derive it from the
  live code tokens rather than inventing values, and record contradictions instead of silently
  fixing them. Do not create it for a one-element fix unless asked; offer it in one line.
  Keep DESIGN.md and code tokens in sync within every change that touches either.
- The API expresses intent, size, density, and state. Preserve native props, form participation,
  links, and accessible names; do not require onClick on a submit button or a link with href.
- Do not tune every element with its own hex, gap, shadow, and radius. Change a shared token
  or variant when the cause is shared. Layout math, a 1px border, 0, fr, %, calc,
  aspect-ratio, and allowed project values are not violations by themselves.
- Choose text size by role and container.
- Construct geometry; never place it by eye. Follow [layout-geometry.md](references/layout-geometry.md)
  for every screen, panel, and game menu, and measure the result (section 8). Fix a
  misalignment at its cause (pivots, anchors, a missing layout group, sprite padding, font
  metrics), never by nudging one element:
  - **Equal intervals.** Siblings of one kind sit in a layout container (flex/grid `gap`,
    Unity layout groups, Godot box containers, UMG boxes) with one spacing token, so every gap
    between them is identical. A different gap must mean a new group and a clear step up the
    scale. Proximity ladder: inside a control < between items < between groups ≤ padding.
  - **Shared lines.** Items in a row share their top/center/bottom (mixed heights share
    centers); items in a column and every label in a settings list start on one vertical
    keyline, with controls on a second keyline. Use a grid or a fixed label column, never
    per-row offsets. Sets of buttons share one size.
  - **Content inside small controls** is centered by its visible ink (cap height, trimmed
    icon pixels), not by the font line box or a padded sprite rect; asymmetric icons get a
    declared optical offset baked into the component. Icon + label pairs use one gap token.
  - **Breathing room.** Nothing overflows or sits on its container's edge: padding is at
    least the gaps it contains, with reserve for the longest localization, hover scale, and
    focus rings; interactive UI stays inside the safe area at every supported aspect ratio.
    When content does not fit, change the layout, not the margins.
- Select typography through a process, not a blacklist: shortlist three families derived from
  the concept (era, material, voice, data density), then choose with a stated reason. The
  family must be legible at its real sizes and languages and provide the weights, styles,
  numerals, glyph coverage (including Cyrillic when supported), and fallback behavior required.
  No family is forbidden, but a family picked out of habit is a defect: swapping one trend
  default (Inter, Uni Sans) for the next (Space Grotesk, DM Sans, Instrument Serif) without
  a reason is the same template. Stylish type must never make the interface harder to read.
- Build hierarchy through dominance and contrast: one leading element per screen or section,
  a clearly stepped type scale (display 3–5× body on expressive surfaces, smaller steps in
  dense tools), intentional asymmetry where it serves the concept, and adjacent sections that
  differ in structure rather than repeating one block pattern.
- The golden ratio may inform proportions, hierarchy, cropping, or whitespace when it improves
  the composition, but it is a visual tool rather than a mandatory formula. Prefer the actual
  task, content, responsive constraints, readability, and existing system whenever they conflict.
- Do not make a primary screen a wall of uninterrupted prose when its content can be
  understood through actions, grouping, or visual anchors. Break dense explanations into
  scannable sections and pair them, where useful, with meaningful controls, icons,
  illustrations, previews, diagrams, or other task-relevant imagery. A dashboard or
  account area, for example, should expose its main sections and next actions rather
  than only describing what a user could configure. Do not add decorative visuals that
  compete with comprehension or create false affordances.
- Use color for meaning and emphasis; do not convey state with color alone.
  Pair error/success/required/selected information with text, an icon, shape, pattern,
  or another non-color cue that remains visible in grayscale and for color-vision deficiencies.
- Verify contrast on the actual adjacent foreground/background pair after opacity, overlays,
  gradients, imagery, and every required theme are applied; do not round a near-threshold result.
  Meet at least 4.5:1 for normal text and meaningful images of text, and 3:1 only for large
  text (at least 24 CSS px regular or 18.5 CSS px bold). Aim higher for thin, small, or unusual type.
- Ensure a 3:1 minimum contrast ratio for visual information needed to identify an active control,
  its focus or state, and meaningful graphical objects against their adjacent color. A border is
  required only when it is what makes the control identifiable; when it is used for that purpose,
  it must meet the same 3:1 threshold. A truly inactive control may use lower contrast, but must
  remain clearly unavailable and never be the only way to complete the primary task.
- Choose one coherent icon set. Do not redraw a standard icon when a suitable project one exists.
  Custom graphics, diagrams, and SVG are allowed when appropriate to the task. Use familiar,
  meaningful icons to reinforce an action or state, especially for compact and high-frequency
  controls: for example, pair a Play label with a right-pointing launch triangle. Icons support
  text; do not use an ambiguous icon as the only label for an unfamiliar action.
## 5. Keep the interface alive with motion

A static interface feels dead: a control that does not answer the finger, a panel that
appears from nowhere, a number that swaps without a trace, a list that jumps. Motion is part
of the system like color and type, with a character, tokens, hierarchy, and rules. The goal is
**no dead moment and no idle movement**, not more animation. For creation, redesign, and any
change that adds, removes, or transitions elements or states, follow
[motion.md](references/motion.md); for a focused fix, inherit the existing motion tokens.

- Every movement serves a named function: feedback, causality (where it came from and went),
  orientation (spatial model), a changed value, or signs of life. No function, no movement.
- Every interactive element answers input immediately, on pointer/touch-down, before the
  result arrives: a button compresses and springs back, a toggle travels, a tab indicator
  slides. Feedback never delays the action itself or the interface's readiness for input.
- **Interaction baseline (required, not polish).** Models skip this unless it is built in, so
  for any UI you create or redesign, adopt the [interaction kit](assets/motion/) before
  building components: `interaction-kit.css` + `interaction-kit.js` (or their port into the
  stack's Button/Link/Switch components), mapped to DESIGN.md motion tokens. It gives every
  control the three-layer press (compress by ~4 px of perimeter in ≤ 90 ms with a fill step,
  a bloom from the touch point, a spring release with ~1% overshoot), hover and focus
  transitions, a 90 ms minimum press so quick taps are visible, keyboard press, switches,
  checkboxes, sliding segmented indicators, pending/done/error button states, icon swaps,
  menus that grow from their trigger, and height-animated disclosures. A lone 1–2 px nudge or
  a 0.97 scale with an instant return is not press feedback; see motion.md section 5.
- Every user-caused state change transitions instead of cutting: overlays grow from their
  trigger, inserted and removed rows push their neighbours, sections expand in height,
  skeletons crossfade into content, and changed numbers roll to the new value. A visible
  consequence can travel to where it counts (a collected reward flying into the balance).
- Build motion as a system: a small set of duration, easing, and spring tokens by role;
  shorter for frequent actions and longer for larger distances; exits faster than entrances;
  one physics for the whole product. Never `transition: all` or an untuned default `ease`.
- Choreograph: one dominant movement per event, others subordinate; small amplitudes
  (a few pixels and scale 0.95–0.98, not from zero); stagger capped to a handful of items;
  shared elements move rather than disappear and reappear.
- Keep motion interruptible and retargetable from the current value, carry gesture velocity,
  animate composited properties (transform, opacity), and hold the frame budget on weak devices.
- Ambient life is rare, slow, peripheral, derived from the concept, and stops when hidden or
  offscreen. Infinite pulses, floating orbs, and scroll-reveal on every section are noise.
- Reduced motion replaces spatial movement with crossfades or instant changes; it never
  removes feedback or state. Respect flashing and pause/stop/hide limits, and never make an
  animation the sole carrier of important state.

### Optional effects pool

When an expressive surface needs a signature detail and the habitual answer (a card that
lifts, a button that grows) would read as a template, choose from
[effects-library.md](references/effects-library.md): live and baked ordered dither, film
grain, a light orbiting the primary button, brushed-metal words, blueprint section rails,
hover responses that are not lift-and-scale, a header that morphs into a capsule, a
distance-driven coverflow, a barcode ruler scrubber, a swipe story stack, and packets on
routing wires; a dot language (dot-grid fields with a pointer spotlight, images and text
rebuilt from dots, a dotted globe with routes, pulsing dot bands, dot-column data, 5×5 LED
status icons, bolted plates and corner brackets, a comet on the active card); and
scroll-linked scenes (edge fades on overflow rows, timed dot navigation, media that settles
into a frame, section theme flips). Tested code is in [assets/effects/](assets/effects/)
with a bench page.

- The pool is opt-in. Pick by concept and named function, never by default; a surface
  without any pool effect is complete. In the house style, use the effects its section 9
  marks as fitting, in monochrome variants unless the product brings a color. Dense tools take only hover responses, the header
  morph, and a scrubber over real data.
- Keep the page budget (one live field and one globe per page, one ring and one sheen per
  viewport, two to four pool effects in total) and record the chosen IDs in DESIGN.md and
  `direction.motion`. Dots are a material: one pitch on the spacing scale, faint tinted
  dots, and something on the page actually made of dots; a bare dot wallpaper is slop.
- Adopt the selected block with its fallback, reduced-motion, offscreen-pause, and
  accessibility parts; map `--fx-*` tokens to DESIGN.md roles; never import the whole file.

## 6. Replace AI slop with decisions

A slop pattern is a choice made from the model's habit rather than from the product: it would
move to any other site unchanged. The full catalog, with a detection signal, a replacement,
and a legitimate exception for every pattern, is [ai-slop.md](references/ai-slop.md); it is the
single source for these rules. Read it before rendering a created or redesigned surface, and
run its slop scan on the screenshots afterwards. Removing a pattern without its replacement
only produces a blander template. The catalog groups, by ID:

- **Composition and cards**: identical icon-heading-text card grids, icon tiles stacked above
  headings and oversized icons, nested card layers, colored side stripes and thick accent
  borders on rounded cards, hero-metric layouts, display-size hero headlines, marketing
  sections inside working tools, everything centered, decorative grid backgrounds.
- **Color and light**: the AI palette (purple-to-blue gradients, cyan on dark), gradient
  text, glass and neon "lazy cool", radial halos, spotlights and orbs, default cream/beige.
- **Typography**: habitual default fonts, flat hierarchy, italic serif display headlines,
  eyebrow labels and pill badges above headings.
- **Motion**: everything asking for attention at once, pulsing status dots, scroll reveals
  on every section (details in motion.md).
- **Imagery**: rough hand-drawn SVG scenes and mascots, stock imagery and mixed icon sets,
  sparkles as the only AI marker.
- **Copy and behavior**: page introductions that narrate an obvious purpose, toggle descriptions
  that paraphrase their labels, helper text added to every row by default, the same meaning
  repeated within one task region, generic
  marketing claims, forced "Not X. Y." contrasts, a dash in every sentence, fake content,
  dead controls and fake success.

A pattern that DESIGN.md records as an intentional brand choice is not slop. These are constraints on mindless use, not a ban on color, type, cards, or expression.
Evaluate semantics: a nested DOM container is not automatically a decorative card.
Try hierarchy, alignment, and spacing first. Verify that removing decoration does not
destroy useful grouping. Do not use “minimalism” as a reason to hide an action
or remove a needed hint, label, shortcut, error, or explanation of an unfamiliar concept.

Treat interface copy as part of this review. Apply the information test in the catalog's
Copy section to every introduction, subtitle, hint, and tooltip: what specific fact would
the user lose if it disappeared? If it only restates the heading, label, or visible state,
remove it, even when reworded. Do not add a description just because a component has a slot.
Keep verified consequences, constraints, requirements, recovery, and necessary accessible
instructions; never invent facts to replace filler. This applies to ordinary working UI as
well as expressive pages. Documentation may explain features when that is its actual purpose.

## 7. Implement behavior together with appearance

- Read the applicable sections of [behavior-and-content.md](references/behavior-and-content.md).
  Give every action an observable result and every risk a recovery path.
- Make supporting descriptions optional in components and remove their wrappers/spacing when
  unused. Start a working page with its task, data, or controls; add orientation only when it
  supplies information users need beyond the title. Use the catalog's copy rules as the source.
- Populate the required states of affected components. Hover applies to a pointer;
  selected/checked/expanded apply to their respective semantics; pending/error/retry
  apply to asynchronous operations. Do not invent loading/error states for a static section.
- Give a command a button, navigation a link, and a field a persistent label.
  An icon action needs a name. Support keyboard/assistive devices, visible focus,
  and expected Back/Cancel behavior.
- Preserve entered data on error, show the reason and the next step. Do not disguise
  a loading failure as an empty list. Prevent duplicate submissions and stale responses.
- Give every asynchronous region an explicit loading state chosen by expected duration and
  known content shape (see the loading section of behavior-and-content.md). Use a skeleton
  loader that mirrors the real layout for initial content loads; keep action progress inside
  the control; use determinate progress for long operations. Reserve a loading splash for
  genuine bootstrap, when the app cannot show anything meaningful until it finishes required
  long steps such as network discovery, sign-in or session restore, mandatory sync, or asset
  loading. A splash shows real stages, offers retry or offline paths on failure, never adds
  an artificial delay, and is skipped when cached data allows showing the interface.
- Anticipate drag and drop instead of waiting for it to be requested. Every place where the
  user brings content in (file or image upload, avatar, cover, attachment, import, asset or
  mod slot) gets a drop zone in its first version, next to a real "Choose file" button.
  Make it self-explanatory at rest (icon, "Drop files here or choose", accepted types and
  limits) and give it distinct, non-color-only states: file dragged over the window, over
  the zone, will-reject, uploading with per-file progress, done with preview and
  remove/replace, failed with a reason and retry. A drop outside the zone never opens the
  file or loses the form. User-ordered collections (gallery, playlist, priorities, kanban)
  get drag to reorder or move, always with a button/menu and keyboard alternative.
  Details are in the drag-and-drop section of behavior-and-content.md.
- Implement motion together with each state, not as a later polish pass: every state a
  component gains (pressed, open, selected, pending, inserted, removed, error, success) gets
  its transition from the motion catalog and tokens, plus its reduced-motion variant.
- For significant irreversible operations, use applicable undo, confirmation, or review.
  Do not turn every save into a confirmation dialog.
- Implement only the requested flow completely. In a prototype, mark fixtures;
  honestly present an unavailable backend as a limitation rather than simulating completion.

## 8. Validate the real surface

- For web, read [web-quality.md](references/web-quality.md); for native/desktop/game,
  read the relevant section of [platform-adapters.md](references/platform-adapters.md).
  Use the current project tools, runtime, and platform accessibility APIs.
  Retrieve documentation for a specific library through the method prescribed by the environment.
- First run applicable type/build/lint and token checks; then safe
  interaction/keyboard, error, recovery, responsive, and visual checks.
- Check DESIGN.md conformance: every style literal in changed code is a DESIGN.md token or a
  legitimate layout value, and the rendered set of font families, font sizes, control heights,
  radii, and text colors stays inside DESIGN.md, with the same role rendering the same value
  across screens. Procedure is in design-md.md; record it as a `tokens` check.
- Inspect current renders at the required states and sizes: hierarchy, legibility,
  focus, overflow, overlaps, and missing actions. Do not infer correctness from JSX.
- Measure layout geometry instead of eyeballing it: dump the rendered layout with the
  dumper for the stack ([web, Unity, Godot](assets/layout-dump/)) and run
  [check_layout.py](scripts/check_layout.py) at every resolution in the matrix; fix each
  `uneven-gap`, `misaligned-*`, `off-center`, `overflow`, `tight-edge`, and `overlap` at its
  cause and re-run until clean. Then inspect 1:1 or zoomed crops of every button row, list
  start edge, and small control; a full-screen thumbnail cannot show a 2px error. Record a
  `layout` check. Procedure and annotations are in layout-geometry.md section 6.
- Review visible copy and accessible names/descriptions across each affected task region.
  Run the catalog's information test against headings, labels, states, and neighboring text;
  include semantic paraphrases, not just exact duplicates. After removal, verify that necessary
  instructions and consequences remain, accessible relationships still resolve, and the layout
  has no empty description gaps. Report representative removals and justified retained help.
- Validate every viewport and browser-zoom target in the defined platform matrix, including
  the smallest and widest supported surfaces. Confirm that composition, touch targets,
  controls, imagery, text wrapping, safe areas, scrolling, and state feedback adapt without
  clipping, overlap, accidental horizontal scrolling, or loss of a primary action.
- Test long real data, 200% text, applicable themes, and reduced motion.
  Pseudo-expansion is useful for text changes; test RTL when it is supported
  or requested. Do not expand a local fix into an i18n or design-system migration.
- Walk through actions using safe fixtures with expected outcomes. Do not automatically
  activate every control in a live system: a test might delete a record or send a message.
- Check loading states on the real surface: throttle or delay fixtures to see the skeleton,
  its replacement without layout shift, the timeout/error path, and splash stages and failures.
- Drag real files onto every upload surface: the window-level and zone-level highlights, no
  flicker over child elements, a wrong type and an oversized file rejected with a reason,
  several files at once, a drop beside the zone that neither opens the file nor clears the
  form, and the button, keyboard, and paste paths still working. On touch, the zone reads as a
  picker without "drag" wording.
- Run the motion probe on every created or changed page:
  `node scripts/motion_probe.mjs <url-or-file>` (headless Chrome, no dependencies). It hovers,
  presses (releasing outside, so nothing activates), and keyboard-focuses each interactive
  element and fails on missing press feedback, missing focus, or a stuck state; it warns on
  weak presses, instant returns, missing hover, and `transition: all`. Fix until it reports
  zero errors, rerun with `--reduced-motion`, and record the result in the `motion` check.
- Check motion in motion, not in stills: record or step through key transitions at slowed
  speed; walk the primary flow for dead moments (input without visible response within about
  100 ms, state that cuts); spam-click and cancel mid-transition to catch queues and stuck
  states; list everything that moves while idle and justify it; verify reduced motion and
  frame timing on a weak profile. Details are in the validation section of motion.md.
- For a new or redesigned expressive surface, run a separate critique pass on current
  screenshots after it works: the swap test (would it fit a competitor unchanged?), the squint
  test (does a blurred grayscale capture still show hierarchy and one dominant element?), and
  a comparison against the concept and references, and the slop scan from ai-slop.md with
  pattern IDs. Rework whatever reads as "from any template".
- The offline helper [validate_design.py](scripts/validate_design.py) validates its own
  contract format and a limited token subset; instructions are in [validation.md](references/validation.md).
  Its PASS confirms only the listed structural/color checks.
  The helper does not include browser, screen-reader, or full WCAG auditing.

## 9. Accept against tasks and evidence

- Blocker: the primary scenario is broken, data is lost, a significant action is inaccessible,
  a required name/focus is missing, there is a keyboard trap, or important content is hidden.
- Error: implemented behavior or an applicable project rule diverges from the contract; changed
  code uses a value outside DESIGN.md without adding the role, or leaves DESIGN.md and code
  tokens out of sync; the slop scan finds unjustified patterns at error severity; an
  asynchronous region has no loading state or shows a failure as empty; a splash is used
  without a genuine bootstrap need; any element overflows or touches its container or the
  safe area, sibling gaps of one kind differ, a row, column, or settings keyline is off by
  more than the tolerance, or text/icons sit off-center in their controls without a declared
  optical offset; a file or image upload has no drop zone, its drop zone
  has no visible drag-over state, or drag is the only way to add or reorder;
  or, when identity is part of the task, the result fails
  the swap test or contradicts the recorded direction; a created or redesigned surface is
  dead (controls without press feedback, overlays and list changes that hard-cut), or the
  motion probe reports errors or was not run on a created/changed page; a pool
  effect is adopted without its fallback, reduced-motion, or pause path, or exceeds the page
  budget without a recorded reason; motion
  blocks input, queues on repeated input, janks, or disappears entirely under reduced motion
  together with the feedback; or anything flashes or loops without a pause path.
  Newly authored page narration, label paraphrases, or repeated helper text without new
  information are errors even in dense tools; removing necessary instructions or inventing
  product claims to replace filler is also an error. Apply these checks within the task scope.
  Warning: a taste heuristic, excess cards/pills/shadows, suspicious density, or subjective tone;
  motion off-token or with an unnamed function, decorative scroll reveals, idle noise;
  for dense working tools a generic look is a warning, not an error.
  Confirm the context before changing it. Do not present a counter as an assessment of beauty.
- Fix confirmed significant defects within task scope and recheck what is affected.
  Stop polishing when scenarios are accepted and, where identity is part of the task, the
  distinctiveness and motion checks pass; do not limit work to an arbitrary number of passes if a
  blocker remains. A critique pass that finds nothing deserves a second look.
- Report what changed, which actions/states were actually checked, where the result is,
  and which checks were unavailable. Mark untested work as unverified, not PASS.
- Do not claim complete WCAG conformance from a scanner, screen-reader testing from an
  accessibility tree, field p75 from local Lighthouse, or percentage UX improvement from one screen.
- To evaluate the generator itself, use [evaluations.md](references/evaluations.md).
  The basis and boundaries of normative requirements are in [sources.md](references/sources.md).
