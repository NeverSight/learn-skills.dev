---
name: visualize
version: 0.7.0
license: MIT
user-invocable: true
argument-hint: "[teach | explore | simplify | bolder | quieter | animate | polish | review | publish] [<topic-or-path>]"
allowed-tools:
  - Bash(node $SKILL_DIR/scripts/detect.mjs*)
  - Bash(node $SKILL_DIR/scripts/browser-contrast.mjs*)
  - Bash(node $SKILL_DIR/scripts/browser-diagram.mjs*)
  - Bash(node $SKILL_DIR/scripts/render-mermaid.mjs*)
  - Bash(node $SKILL_DIR/scripts/palette.mjs*)
  - Bash(node $SKILL_DIR/scripts/teach.mjs*)
  - Bash(node $SKILL_DIR/scripts/generate-image.mjs*)
  - Bash(node $SKILL_DIR/scripts/record-image.mjs*)
  - Bash(bash $SKILL_DIR/scripts/publish.sh*)
  - Bash($SKILL_DIR/scripts/publish.sh*)
  - Bash(node */visualize/scripts/detect.mjs*)
  - Bash(node */visualize/scripts/browser-contrast.mjs*)
  - Bash(node */visualize/scripts/browser-diagram.mjs*)
  - Bash(node */visualize/scripts/render-mermaid.mjs*)
  - Bash(node */visualize/scripts/palette.mjs*)
  - Bash(node */visualize/scripts/teach.mjs*)
  - Bash(node */visualize/scripts/generate-image.mjs*)
  - Bash(node */visualize/scripts/record-image.mjs*)
  - Bash(bash */visualize/scripts/publish.sh*)
  - Bash(*/visualize/scripts/publish.sh*)
description: >
  Generate beautiful, on-brand HTML artifacts — reports, diagrams, diff
  reviews, slide decks, plans, recaps, dashboards. Loads on creation
  intents ("create a plan", "make me an implementation plan",
  "generate a diagram", "build a slide deck", "draft a recap",
  "visualize this", "render this as HTML", "make me a status update")
  and exploration intents ("show me three layouts", "explore document
  shapes", "compare visual treatments", "explore a new design system",
  "compare replacement brand directions") and iteration intents ("make this beautiful", "polish this report",
  "make this less generic", "design this", "theme this", "use my
  brand", "iterate on this design", "review this artifact", "make
  this bolder", "make this quieter", "simplify this design",
  "animate this", "improve the look of", "give this a refresh").
  Captures brand from the user's codebase, asking, or live site, then
  applies it to every artifact.
---

# visualize — beautiful, on-brand HTML artifacts

Generate self-contained HTML artifacts composed from `templates/*/template.md` contracts against the resolved visual context. The project's `DESIGN.md`, `PRODUCT.md`, and sidecar `tokens.css` provide the default; artifact themes below allow reference systems within the user's approved scope. Shared pattern recipes live in `patterns/` and are read only when the selected template and user ask make them relevant; shell mechanics are loaded automatically only when a template declares `shell: <slug>`.

## Design judgment

Find the artifact's organizing idea before choosing its visual treatment. Look for a relationship, contrast, sequence, decision, or object in the source that the composition itself can make easier to understand. Use that idea to shape the opening, section rhythm, and any explanatory primitive. When the source has no useful spatial or structural idea, prefer a restrained reading experience over manufacturing one.

Artifact mode describes how the reader consumes the information, not the aesthetic family it must use. A document can use product-native, application-like, spatial, editorial, or technical-drawing grammar when that grammar serves the source, reader, and brand. Do not equate `document` with editorial publishing, or `canvas` with diagram chrome.

Visual conviction can come from composition, typography, density, spatial rhythm, imagery, interaction, or color. Do not add hues, decoration, or components merely to make an artifact feel designed. A restrained palette can carry a strong point of view when another dimension does the expressive work.

Before responding to feedback, compare the observation with the artifact's reader, purpose, source, and approved brief where one exists. Distinguish an implementation defect, a design that fails its existing requirements, and evidence that a requirement or assumption has changed. The current composition is a solution, not a constraint.

Make authorized corrections within the existing brief directly. If feedback implies a change to established requirements that the user has not already approved, explain the proposed change and obtain agreement before editing. When several structural or visual directions remain plausible, recommend `explore artifact` within its supported scope. When the direction is established, use the ordinary creation or refinement workflow. Follow that workflow's approval requirements; a small correction does not need a new exploration.

Evaluate proposed fixes together against the reader's task. Do not turn every critique finding into an addition or treat a small diff as evidence that the direction is sound. Preserve decision-relevant deferred observations in existing review or task notes.

## Commands

`{{command_prefix}}visualize` invokes the skill. The argument tells the agent what to do.

**Default (no command, or the first argument is a topic):** `{{command_prefix}}visualize <topic-or-path>` creates a new artifact. The agent picks a template from intent across all of `templates/`, composes against the resolved project or artifact-theme context, writes self-contained HTML. **The flow is gated:** preflight checklist + shape-gate before code, no self-authored briefs. See `reference/create.md`.

**Named commands:**

| Category | Command | Argument | What it does | Reference |
|---|---|---|---|---|
| **Build** | `teach` | none | Bootstrap (or refresh) the brand profile. Writes `DESIGN.md` + `PRODUCT.md` at the project root. | `reference/teach.md` |
| **Build** | `explore` | `artifact\|system <topic-or-path>` | Compare one artifact's treatment or a new/replacement project system; review before applying. | `reference/explore.md` |
| **Refine** | `simplify` | `<path>` | Strip decoration that isn't earning its pixel. Hands off to `polish`. | `reference/simplify.md` |
| **Refine** | `bolder` | `<path>` | Amplify visual punch on safe / generic artifacts. Hands off to `polish`. | `reference/bolder.md` |
| **Refine** | `quieter` | `<path>` | Tone down over-decoration without going generic. Hands off to `polish`. | `reference/quieter.md` |
| **Refine** | `animate` | `<path>` | Purposeful motion, `prefers-reduced-motion` compliant. Hands off to `polish`. | `reference/animate.md` |
| **Refine** | `polish` | `<path>` | Terminal quality pass — walks every dimension and reports per-dimension findings. The other Refine verbs hand off to this one. | `reference/polish.md` |
| **Evaluate** | `review` | `<path>` | Deterministic detector findings + LLM judgment. Reports; doesn't modify the file. | `reference/review.md` |
| **Publish** | `publish` | `<path>` | Push the artifact to display.dev via MCP / CLI / HTTP cascade. | `reference/publish.md` |

Invocation forms: `{{command_prefix}}visualize teach`, `{{command_prefix}}visualize explore artifact ./report.html`, `{{command_prefix}}visualize polish ./report.html`, `{{command_prefix}}visualize publish ./diagram.html`. On hosts without a slash-command form, the skill loads on intent-match from the description above; natural-language is the primary entry there.

## Routing rules

1. **No argument**: render the Commands table above as the user-facing menu, grouped by category. Ask what they'd like to do.
2. **First word matches a command**: **load its reference file before doing anything else.** Non-negotiable — the table row + this section is insufficient; the procedure lives in the reference. Everything after the command name is the target.
3. **Natural-language intent**: requests to compare design alternatives load `reference/explore.md`; capturing or reconciling project identity loads `reference/teach.md`. Otherwise load `reference/create.md` for creation or an explicitly requested restyling of an existing artifact. A named theme follows Artifact themes below; it does not require an exploration round.
4. **Relationship-diagram route during creation**: when preflight first identifies a likely relationship diagram, load `reference/diagram.md` and the one tentative non-spatial type reference needed for that figure before presenting the shape gate. For multi-figure artifacts, load one reference for each distinct tentative family: `reference/diagram-flow.md`, `reference/diagram-system.md`, `reference/diagram-sequence.md`, `reference/diagram-state.md`, or `reference/diagram-hierarchy.md`. Spatial figures use `reference/diagram.md` alone. If approval changes a figure's type, load the replacement reference before authoring; do not load unrelated families.
5. **Generated-image route during creation**: when the approved shape requires generated bitmap imagery, load `reference/image-generation.md` before selecting or invoking a route. Use only the active callable inventory or an explicitly selected API adapter. Never infer a route from a key, executable, mount, or model claim, and never retry or fall back after an ambiguous attempt.
6. **Explore scope**: `explore` always loads `reference/explore.md`, which distinguishes artifact treatment from project-system creation or explicit replacement. Comparing treatments for one artifact does not require creating a project design system first. System Explore uses its opt-in authority classification instead of applying the render fallback as an incumbent identity.

## Hand-off output shape

After a refine verb (`simplify` / `bolder` / `quieter` / `animate`) finishes its run, summarise to the user in plain markdown. Don't render the summary as a fenced code block — it's conversational output, not machine-readable. Vary phrasing across runs; pick wording per context (engineer reading detector output vs. designer iterating on a brand brief). `polish` has its own output shape — see `reference/polish.md`.

Every refine run's summary covers four facts:

- Which verb ran, against which artifact.
- What the verb actually did. Pull the verb-specific content from the per-verb reference's "what to surface" list (focal moment, cuts + audit trail, strategy, what stayed, hero moment, reduced-motion handling — depends on the verb).
- Diff size as a percent of the artifact.
- Which next action makes sense, if any. Polish is the default next step from a successful refine run.

Variant rules (behaviour, not surface text):

- **Context source note.** If the run cannot use a persisted `DESIGN.md` / `PRODUCT.md`, mention once which fallback source anchored the work: project instructions, README/docs, generated seed, or Clean defaults. Also nudge the user to run `{{command_prefix}}visualize teach` so that fallback can become a real brand profile. Clean defaults are the last resort after the Brand profile rules below find no usable project guidance.
- **Diff exceeded the 40% guard.** Stop refinement and report the affected scope. Apply Design judgment to recommend exploration when the structural direction remains unresolved, or a fresh creation pass when it is established. Do not continue into polish.
- **Verb shouldn't have run** (Absolute bans present, no decoration to remove, no focal moment, etc.). Skip the standard run summary entirely. Surface a short refusal that names the reason and routes to the right alternative verb. Each per-verb reference's "When `<verb>` is the right verb (and when it isn't)" section enumerates the verb's specific refusal conditions.

Tone is conversational. Lead with what changed, not with a banner. Don't capitalise words for emphasis. Don't print a `<Verb> pass complete ·` header — the summary's content is the proof of completion.

For `animate` specifically: when the brand declares `motion: none`, a fifth variant applies — see `reference/animate.md`.

## Absolute bans

Match-and-refuse. Apply on every command and the default creation flow. These ban specific patterns — not aesthetics, not registers. A brand can declare a font, a hue, or a layout that looks unusual; it cannot redeem any of these patterns by declaring them as identity. An explicit `.visualize-detect.json` skip can waive only a detector-backed ban with a concrete rule ID; it is project policy, not runtime brand suppression, and cannot waive a Layer-2 ban.

```
BAN 1 — Gradient text on metrics or headings
  PATTERN:   background-clip: text + gradient background on <h*>, [class*="metric"], [class*="kpi"]
  INCLUDES:  -webkit-background-clip: text; CSS `background-image: linear-gradient(…)` + `color: transparent`
  WHY:       AI-essay register tell; reads as 2023-template "make the number pop"
  REWRITE:   Solid `--primary` (or `--foreground`) at one weight up; emphasis through weight + size, not gradient

BAN 2 — Side-stripe callout (border-left as accent)
  PATTERN:   `.callout`, `.tldr`, `.note`, `.tip` with border-left ≥ 3px in --primary / --warning / --destructive
  INCLUDES:  border-inline-start, border-l-4 utility class, ::before pseudo with positioned bar
  WHY:       Notion / Confluence template tell; reads as productivity-app default
  REWRITE:   Full thin border (1px var(--border)), background tint at 4–8% chroma, or no chrome — just a label heading

BAN 3 — Triple-feature-card grid
  PATTERN:   3-column grid of <h3>adjective + noun</h3> + one paragraph + one icon each
  INCLUDES:  4-column variants, "Why us" sections with identical card-icon-heading-blurb shape
  WHY:       AI-landing canonical pattern; the surest "AI generated this" tell on the visualize corpus
  REWRITE:   Asymmetric — one hero claim with two supporting facts, OR a numbered list with body prose, OR a single comparison table

BAN 4 — Hero-metric template
  PATTERN:   Centered <h1 class="…huge…">N×</h1> + <p class="…small…">supporting label</p> + 3 stat tiles below
  INCLUDES:  "10× faster", "99.9% uptime", "1M requests/day" hero blocks with the same shape
  WHY:       SaaS-landing cliché; the most-copied AI-marketing-page shape in 2024-2026
  REWRITE:   Specific claim in body prose with the number inline; data tiles only when the artifact is actually a dashboard

BAN 5 — Icon-tile section markers
  PATTERN:   Every <h2> preceded by a rounded-square tile carrying a Lucide / Heroicons / Phosphor glyph
  INCLUDES:  Circle-icon variants, icon-on-coloured-pill variants, gradient-icon-tile variants
  WHY:       AI section-marker tell; reads as "every section needs visual chrome"
  REWRITE:   Heading alone, or heading + small accent rule above, or numbered sections — no per-heading iconography

BAN 6 — Imperative tricolon
  PATTERN:   Three short imperative sentences ending in periods, in the same paragraph or hero
  INCLUDES:  "Ship faster. Build smarter. Scale forever." / "Move fast. Stay safe. Be bold." (any topic)
  WHY:       AI-copywriting cliché — the structure is identical across thousands of generated landing pages
  REWRITE:   One specific claim with the verb in the right tense, OR a sentence that names the actor and the action

BAN 7 — Sycophant / AI-attribution footer
  PATTERN:   "I hope you find this useful", "Let me know if you have questions", "Best, Claude", "Generated by AI", "As an AI…"
  INCLUDES:  Footer-line variants, comment-line variants in the HTML source
  WHY:       The artifact is the work; the model is invisible. Sycophant footers contaminate the artifact register
  REWRITE:   No footer of this shape. A real footer carries metadata (date, version, source-of-truth link) or is absent
```

If you're about to author one of these patterns, stop and rewrite the element with the alternative. The list is shared across creation, every Refine verb, and `polish`.

## Model-specific operating rules

These are not brand aesthetics; they are observed model reflexes with required corrective behavior. Apply them after the universal bans, especially during no-brand greenfield creation.

**Codex-specific rules:**

- **Border plus big shadow:** avoid pairing a 1px border with a large fuzzy drop shadow on the same card or button. Choose a crisp edge or a small elevation cue.
- **Over-rounded containers:** ordinary cards, sections, inputs, and panels should usually stay at 12-16px radius. Larger radii need an explicit brand reason.
- **Decorative stripe backgrounds:** do not use `repeating-linear-gradient(...)` as body or section filler. Use an intentional texture/rule system, or leave the background plain.
- **Crude SVG fallback:** do not draw rough SVG scenes because no real asset is available. Use generated bitmap imagery, a geometric diagram, or no illustration.
- **Compressed display type:** keep display heading letter-spacing ≥ -0.04em and clamp max ≤ 6rem unless the template is a slide/poster register that explicitly needs larger type.
- **Meta-contrast copy:** avoid "X theater", "actually X", and "not just X, it's Y" framing. Say what the artifact literally does.
- **Color judgment:** use `reference/color.md` to assess character, relationships, roles, distribution, and actual pairings. No hue, hue combination, neutral tint, or accent count is a universal taste gate. Preserve approved identity and explicit artifact exceptions.
- **Palette as a substitute for composition:** assign semantic color roles in the shape gate and use them consistently, but do not add accent tracks merely to manufacture visual interest. Neutral surfaces plus one accent are valid when composition, type, density, imagery, or interaction carries the point of view. Revise when the opening has no expressive dimension, not when it has too few hues.

**Gemini-specific guard:**

- Do not animate `<img>` elements on hover. If a card needs hover feedback, animate the card's border, background, or action affordance instead.

**Metadata / TOC guard:** static document context needs explicit labels, not anonymous rounded chips. In document mode, keep metadata close to the title/thesis inside the reading flow; a right rail, split-cover facts column, or standalone metadata panel usually turns context into competing chrome. TOC rails are allowed for genuinely long documents, but they should support navigation rather than dominate the opening. Mobile TOCs must remain navigable lists or deliberate grids, never free-wrapping word clouds. Read `patterns/metadata.md` or `patterns/toc.md` when those structures are part of creation.

**Table guard:** tables are reading instruments, not hero sections. Keep caption, header, body, row-key, and numeric roles distinct; scope monospace to fixed-width values. Read `patterns/table.md` when the artifact carries dense comparison or evidence.

**Interactive-state route:** when creation includes functional controls or changes state in place, read `patterns/interactive-states.md`.

## AI slop test (two altitudes)

Run both. The second catches what the first misses.

**First-order**: if someone could guess the template + palette from the topic alone, you've hit the first training-data reflex. Topic stereotypes are prompts to inspect the brief, not color prohibitions: red, purple gradients, or navy-and-gold can fit a specific artifact. Rework unsupported defaults, not approved identity.

**Second-order**: if someone could guess the aesthetic family from topic-plus-anti-references ("AI workflow tool that's not SaaS-cream → editorial-typographic," "fintech that's not navy-and-gold → terminal-native dark mode"), the second-tier reflex isn't avoided. Currently-saturated families to watch for: editorial-Tufte clone (cream + Georgia + side-margin notes when the topic isn't editorial), brutalist-terminal clone (mono + grid + heavy borders when the topic isn't dev-tool), Swiss-poster clone (uppercase + grotesk + grid when the topic isn't presentation). Rework until both altitudes return "no, you couldn't have guessed."

## Brand profile

Every render reads available `DESIGN.md` (visual identity + design tokens) and `PRODUCT.md` (voice, audience, tone) at the project root. `teach` derives custom design tokens for the brand and writes them in `DESIGN.md` as YAML frontmatter (the Google Stitch canonical format: machine-readable tokens) plus a six-section markdown body (Overview / Colors / Typography / Elevation / Components / Do's and Don'ts), with a sidecar `tokens.css` at the project root carrying the CSS-form tokens templates read at render time. Project profiles retain concrete tokens, not a `theme: <name>` pointer.

Brand authority is identity-scoped. If the request fixes a named identity but the resolved project profile clearly belongs to another product, do not substitute, relabel, or approximate it. Stop before the shape gate or any artifact edit and request matching authority or explicit permission for an artifact-only override.

The design systems under `design-systems/` are reference packages with design guidance, tokens, and previews. `teach` and System Explore read them when deriving project identities; artifact creation and exploration can use them as themes under the shared contract below.

**Fallback when no DESIGN.md exists:** an approved artifact reference supplies the visual baseline where project guidance is absent; do not replace it with a seed or Clean defaults. Otherwise, first read available project instructions (`AGENTS.md`, `CLAUDE.md`, README, docs) for product positioning, visual direction, anti-references, and design principles. If those files contain usable brand/design guidance, treat it as binding brand context while using Clean's token **surface** as the structural floor. Explicit cues in repo guidance override Clean values: named fonts become the artifact font stack, named palette roles become the artifact color tokens, and named anti-references rule out the corresponding fallback register. If the guidance points at concrete token files, stylesheet files, logo components, or design guidelines, read those referenced files and use their values before approximating from prose. Using Clean's token surface means keeping the semantic variable shape, not copying Clean's fonts, monochrome values, or warm/cream defaults. Only run `node {{scripts_path}}/palette.mjs --from "<topic-or-project-name>"` when the project has no usable visual direction at all. When a seed is used, compose the temporary `--primary`, `--background`, `--foreground`, `--accent`, chart, and state tokens from the seed + artifact brief; do not copy Clean's monochrome palette unchanged. Use the script's `derived` block (real contrast numbers, per-hue chroma budgets, light + dark lightness ladders) instead of estimating those values; if the seed's register fights the brief, re-run with `--not <zone,...>` or `--vary <n>` and note the veto in the shape gate. After composing, validate with `node {{scripts_path}}/palette.mjs --check <tokens-or-html> --strict` and fix error findings (exit 2) before render. Nudge `{{command_prefix}}visualize teach` once per session so repo guidance or the temporary seed can become a real brand profile.

**Refine verbs on missing persisted brand files:** `simplify` / `bolder` / `quieter` / `animate` / `polish` use the same fallback hierarchy as creation. Project instructions, README/docs, or other already-loaded context can be a valid qualitative brand anchor. Clean defaults are only the anchor when no usable project guidance exists. Whenever a fallback source is used, mention that source once and nudge `{{command_prefix}}visualize teach` so the fallback can become a real brand profile.

**Refine verbs on artifacts that carry ≥3 Absolute bans:** `bolder` / `quieter` / `animate` / `polish` refuse and route. State in the run summary: `"REFUSED — N Absolute bans present (listed). The artifact needs structural cleanup before <verb> applies. Recommend {{command_prefix}}visualize simplify <path> first (removes the ban patterns), then re-evaluate."` Simplify accepts ban-carrying input as its core case; the other Refine verbs assume a clean baseline and must not run on ban-heavy artifacts.

## Artifact themes

A theme is a reference design system applied to one artifact, not a new stored object or a project-wide adoption. Use the current project system by default. Resolve binding project choices, approved artifact exceptions, and open design dimensions before borrowing from a reference. A named reference or a request to make an artifact more expressive does not silently override binding project choices; clarify conflicts that the request leaves unresolved. Explicit permission to replace visual styling applies only to the named artifact and dimensions. Do not invent constraints where the project is silent.

Read the selected `design-systems/<slug>/README.md` when present, then its `DESIGN.md` and `tokens.css`. README is the package entry point; DESIGN owns suitability, identity, and adaptation guidance. Use previews to understand the treatment, not as required layouts. If the user wants alternatives, propose a small relevant shortlist rather than loading the entire catalog. A missing README does not make a package unavailable.

Apply a named treatment through ordinary creation or revision; compare unresolved treatments through `explore artifact`. Neither requires a new layout or a project profile first. For new content, derive structure from the reader's task and source. For existing artifacts, preserve content, order, assets, and behavior unless those changes were requested. A broad restyling uses `reference/create.md` with that preservation scope, not a narrow refine verb forced past its diff guard. Existing approval gates still apply; an explicit request already covering the proposed changes does not need reconfirmation.

Translate the reference's hierarchy, spacing, surfaces, and component treatment as well as its palette and type. Keep non-overridden project choices. Embed the resolved tokens, including designed light/dark and OS-dark behavior, in the artifact; do not replace the project's token source. Verify against the resolved artifact context, not the overridden project values. Describe partial borrowing and retained constraints rather than claiming an unchanged reference application. Keep the approved exception and its scope in existing task notes or a short artifact comment so later refinement can preserve it; unexplained styling drift alone is not approval.

For project-wide capture or direct derivation, use `teach`. To compare new or explicitly requested replacement systems, use `explore system`. Neither route is a prerequisite for artifact themes.

## Universal laws

Apply on every command, every template, every prompt. These override contextual taste findings, not non-contextual correctness constraints:

1. **Resolved context and voice trump contextual taste rules.** A finding that merely conflicts with the approved register is a category error. Context cannot suppress an unskipped Absolute ban, an artifact fossil or placeholder, an accessibility requirement, or an honesty/data-truth failure. Permission to refine an artifact does not authorize changes to the project's brand profile or shared token source. Propose necessary changes to those authorities separately unless the user has already authorized them.
2. **Commands interpret, not regenerate.** Iteration commands return a targeted diff, not a fresh draft. If the diff is >40% of the artifact, the command has misfired.
3. **Ship-blockers and taste-calls are different.** A11y and contrast must be fixed; taste-calls are negotiable.
4. **Severity follows context, including aggregate.** An `info` rule can ship-block in aggregate; an `error` rule can be a taste-call only when it is context-sensitive and the brand whitelists it. The non-contextual constraints in law 1 do not demote.
5. **Don't strip-mine into invisibility.** After a command runs, the artifact should still feel anchored to the resolved context.
6. **The reader is the judge.** Every finding maps to: does this make the reader's job harder, or just satisfy a rule?
7. **Detector output is defect-evidence, never done-evidence.** A clean `detect.mjs` result is not proof the artifact is strong — it's proof the mechanical floor passes. The detector catches what regex can identify; verb work covers everything else. Don't declare done on a clean detector reading.
8. **Rendered mobile beats desktop theory.** A desktop-strong composition that merely stacks on phone can still be worse than a plain document. Judge the first two mobile screens as a finished reading state: heading scale, metadata wraps, TOC placement, card chrome, and body rhythm all have to feel intentional at narrow width.
9. **Metadata should explain itself.** Bare chips such as `display.dev strategy` or `Updated May 29, 2026` force the reader to infer the field. Prefer explicit labels: `Memo type / display.dev strategy`, `Updated / May 29, 2026`, `Input / method, vision, competitor refresh`. For document artifacts, those labels belong near the opening argument, not in a side rail that competes with the body.
10. **Clean is not enough.** An artifact can pass every ban, detector rule, and mobile check and still fail because it has no visual point of view. Boring-but-clean is a failure when the user asked for a visual artifact. The output needs at least one deliberate composition choice that helps the reader understand the content faster or remember it longer. If the strongest honest description of the first viewport is only "clean," "polished," "on-brand," or "easy to read," the composition is unfinished; its strongest quality should describe what this specific artifact helps the reader see.
