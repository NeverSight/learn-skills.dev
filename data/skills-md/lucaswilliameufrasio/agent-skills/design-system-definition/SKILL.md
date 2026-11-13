---
name: design-system-definition
description: >-
  Research, decide, and record a complete design definition for a product: brand
  concept, principles, tokens, typography, color, motion, components, content
  rules, ethical engagement patterns, platform adaptations, and a verifiable
  checklist. Use before a redesign or a new product's first screens, when the
  current look feels generic or inconsistent, when a previous redesign failed,
  or when future work needs one documented visual direction. Covers web, mobile,
  desktop, and terminal (TUI) interfaces. Research and audit come before visual
  decisions; record the directives in the repository's own documentation.
---

# Define a product design system

Produce a design definition that makes the product look serious and intentional,
communicates what the brand is and what the product is for, and is precise enough
that any later screen can be built or reviewed against it without guessing.

The order is the method: **understand → audit → research → decide → record →
prove**. Do not choose colors, fonts, or layouts before the product, its users,
and the current state are understood. Excellence here means every decision has a
reason that traces back to the product, the user, or the evidence.

This skill defines and documents. Repainting every screen is the companion
`interface-redesign` workflow; a definition is useful on its own.

## 1. Understand the product and its constraints

Read the repository's agent instructions, README, product/decision documents,
existing design notes, brand assets, routes/screens/commands, and test setup.
Record, from evidence:

- **Purpose:** what the product does, for whom, and the one job a first-time user
  must understand within seconds.
- **Brand:** name, existing marks, voice, language/locale, and anything the owner
  has said the brand must or must not feel like.
- **Audience and context:** who uses it, where (commute, desk, terminal, store
  floor), how often, on which devices, with which accessibility needs.
- **Surfaces:** web, mobile, desktop, TUI, or several. Note the stack and
  rendering model (server-rendered, hydrated, native toolkit, terminal library),
  because they constrain fonts, motion, color depth, and first paint.
- **Hard rules:** content honesty (no invented data, images, people, metrics,
  licenses, or testimonials), persisted data and public contracts that must
  survive, legal and privacy limits, and delivery rules.

Ask only about decisions the evidence cannot settle and that change the outcome
(for example, whether an established brand color is mandatory). Otherwise choose
a sensible default and state it.

## 2. Audit the current state before proposing anything

Look at the real product, not only the code. Capture the main screens at the
sizes that matter (for web: a narrow phone and a wide desktop; for TUI: 80×24 and
a wide terminal; for desktop: default window and minimum size) using the
repository's existing tooling or an approved viewer. Then write a short,
specific critique:

- what communicates the purpose well and must be kept;
- what makes it look generic, cheap, noisy, or untrustworthy (count the accents,
  fonts, radii, shadows, icon styles, and one-off components);
- usability heuristic violations (visibility of status, consistency, recognition
  over recall, error prevention, aesthetic and minimalist design), each tied to a
  screen;
- accessibility failures you can measure (contrast ratios, target sizes, focus
  visibility, motion, labels);
- if a previous redesign was judged poor, why: name the concrete causes so the
  new definition explicitly avoids them.

## 3. Research with sources

Research is evidence for decisions, not decoration. Keep a short source list
(title, URL or document, date consulted) in the final record.

Visual references chosen by the owner outrank the agent's own taste. Ask for
them, and when screenshots or links exist, follow the `reference-driven-design`
workflow to extract and record their traits before deciding foundations.

- **Category patterns:** how respected products in the same category structure
  discovery, browsing, playback, editing, or whatever the core job is. Extract
  patterns and conventions; never copy another product's identity, artwork,
  layout signature, or wording.
- **Platform guidance:** current WCAG for contrast and interaction, plus the
  native conventions of each target surface (see
  [platform foundations](references/platform-foundations.md)).
- **Psychology and heuristics:** choose the principles that apply to this product
  and its users, with an explicit ethical boundary for each engagement pattern
  (see [psychology and heuristics](references/psychology-and-heuristics.md)).
- **Design intelligence tools:** if a design-data skill or tool is already
  installed (for example a style/palette/typography search), use it as one input.
  Verify every suggestion against the product and the evidence; never persist an
  unverified suggestion as a decision. Do not install tools to do this.

When live research is unavailable, say so and label which guidance comes from
general knowledge rather than a consulted source.

## 4. Decide: concept, principles, and foundations

Make the decisions in this order, each with a one-line rationale.

1. **Concept.** One short phrase that ties the brand to the product's purpose and
   drives visual choices (a metaphor, a material, a behavior). It must be
   expressible with real content; it is not a slogan.
2. **Principles.** Three to five principles, each phrased as a testable rule with
   a "so we never …" consequence. Example shape: "Content leads — real artwork
   and titles carry the color; chrome stays neutral, so we never tint
   backgrounds with brand color."
3. **Color.** Semantic tokens, not raw values in components: background and
   surface steps, text (primary, secondary, subtle), border, one action/accent
   color, status colors (success, warning, error, info), and any category colors
   with their meaning. Compute and record contrast ratios for every text/surface
   pair that ships; body text meets at least 4.5:1, large text and essential UI
   at least 3:1. Restraint is the default: one accent used for actions and
   current state reads as more serious than several competing accents. Never
   rely on color alone to carry meaning.
4. **Typography.** Prefer one family with a clear weight range (a second only
   with a specific job). Define the scale (sizes, line heights, weights,
   tracking), numeric style for data, maximum line length, and how text wraps
   and truncates. Respect platform font loading and user text-size settings.
5. **Space, layout, shape, depth.** Spacing scale, grid and breakpoints (or
   terminal column rules), radii, borders, elevation, and when translucency is
   allowed (rarely over moving content; never where it hurts legibility).
6. **Iconography and imagery.** One icon style and size grid with accessible
   names; no emoji as interface icons. Imagery rules: only real, licensed
   assets; how to handle missing images honestly (initials, neutral placeholders,
   generated covers clearly marked); never use an album cover as a portrait or a
   stock photo as a real person.
7. **Motion.** Purpose for each animation, durations and easing per type
   (feedback, transition, emphasis), exits faster than entrances, and a
   reduced-motion behavior for each.
8. **Voice and microcopy.** Tone, the product's vocabulary (the same word for the
   same thing everywhere), empty/error/loading message patterns, and forbidden
   phrasing (fake urgency, guilt, dark-pattern copy).
9. **Components and states.** For each shared component: anatomy, variants,
   sizes, and every state (default, hover, focus, pressed, selected, disabled,
   loading, empty, error, offline, read-only). Include navigation, primary and
   secondary actions, cards/rows, inputs, dialogs/sheets, toasts, media/player
   controls if relevant, and status badges.
10. **Engagement patterns.** The retention loop the product will support (for
    example a fresh edition, saving favorites, personal collections) with its
    ethical limits, and the patterns that are prohibited.
11. **Platform adaptations.** How each foundation maps to every target surface:
    safe areas and touch targets on mobile, window/keyboard/density on desktop,
    color depth and no-color fallback in a terminal.

## 5. Record the definition in the repository

Write one durable design document using the repository's documentation
conventions (location, file-name casing, language). If none exist, propose
`docs/design-system.md`. Use the
[design document template](references/design-document-template.md). It must
contain:

- the concept, principles, and the audit findings it answers;
- every token with its value, role, and computed contrast where relevant;
- typography, space, shape, motion, icon, imagery, and voice rules;
- component anatomy and states, and page/screen patterns;
- **directives**: numbered MUST / MUST NOT rules that a reviewer can check;
- anti-patterns observed in the audit and why they are banned;
- a pre-delivery checklist;
- research sources with dates, and what was not researched;
- a short change log.

For non-trivial decisions, also record the decision in the repository's existing
decision log or ADR structure (context, decision, alternatives, consequences)
before or alongside the design document, and link the two. Update the agent
instructions file (for example `AGENTS.md`) to name the design document as the
source of truth for interface work. Do not create parallel documents that drift.

Optional assets, offered rather than assumed: a social/Open Graph image and
favicon/app icon derived from the system (brand-only, no third-party artwork you
are not licensed to use); a living showcase page for tokens and components that
is excluded from production builds or gated off by environment, never writes
user data, and is not indexed.

## 6. Prove the definition before handing off

- Recompute contrast for every documented pair; fix or flag failures.
- Apply the definition to one representative screen (prototype, mockup, or a
  real implementation slice in a branch) and capture it at the relevant sizes.
  A definition never shown on a real screen is unproven.
- Review that screen against each directive and the checklist; revise the
  definition where it was ambiguous.
- Present the concept, palette, type, and the sample screen to the owner for
  approval before a full redesign. Approval of the definition is not approval to
  deliver, commit, or publish.

Report what was decided, where it is recorded, what was verified (with the
evidence), what was not researched or not verified, and open questions.

## Guardrails

- Never fabricate content to make a mockup look full: no fake rankings, user
  counts, reviews, artists, prices, or photos. Use real data or an honest empty
  state.
- Engagement serves the user's goal; prohibited: infinite feeds without a
  natural end, manufactured scarcity or urgency, guilt or confirmshaming copy,
  hidden opt-outs, and notifications the user did not ask for.
- Preserve the product's established content contracts, data keys, URLs, and
  required copy; a design change is not a reason to break them.
- Keep private brand material, credentials, and internal references out of
  public repositories.
