---
name: marp-deck-gen
description: Generate the final MARP deck markdown from definition, deck plan, and visual design artifacts, applying deck-template layout rules deterministically. Use only when all three source artifacts exist.
---

# Marp Deck Generator

## Purpose

Assemble the **final MARP deck** by applying:
- planned structure
- finalized layout decisions
- materialized visuals (diagrams/images)

This skill performs **no planning, no interpretation, no visual design**.

It is a deterministic renderer.

---

## Inputs and outputs

### Inputs (all mandatory)

- `definition/deck-definition.md`  
  *Semantic intent and authoritative content scope*

- `planning/deck-plan.md`  
  *Slide sequence and content intent*

- `planning/deck-visual-design.md`  
  *Authoritative layout and visual execution*

If any input is missing → **stop and report the error**.

### Outputs

- `slides/deck.md` *(required)*
- `slides/deck-notes.md` *(required)*
- `.marp/themes/deck-theme.css` *(only if a new class is explicitly required)*

---

## Required references (hard dependencies)

Read and follow exactly — both are mandatory:

1. **`.marp/references/deck-template.md`** — the *how*: CSS classes, Markdown/HTML syntax, layout legality, density caps.
2. **`.marp/references/brand-style-guide.md`** — the *what and why*: cover/section tone guidance, callout patterns, breadcrumb format, emoji rules, logo variant rules, brand color usage.

If either file cannot be found, **stop immediately** and report the missing file.

Do not guess or re-implement rules from either reference.

Also read: `.marp/themes/deck-theme.css`

Use it to make render-safe choices (title wrapping, density modifiers, image fit) while staying within
the template's allowed classes and patterns.

---

## Authority and precedence rules

When sources conflict, apply this strict order:

1. **deck-template.md** → layout legality (classes that exist; Markdown/HTML rules)
   - includes the effective behavior implied by `.marp/themes/deck-theme.css`
2. **brand-style-guide.md** → brand compliance (tone choices, callout labels, emoji, breadcrumbs)
   - cannot override what the template forbids, but constrains choices within the allowed set
3. **deck-visual-design.md** → layout & visuals per slide
4. **deck-plan.md** → content intent
5. **deck-definition.md** → semantic boundaries

Never override a higher-priority artifact.

---

## Workflow

### 1. Validate structural alignment

Before rendering:

- Slide count must match between:
  - `planning/deck-plan.md`
  - `planning/deck-visual-design.md`
- Slide order must be identical
- Titles and section boundaries must align

If not → stop and report mismatch.

---

### 2. Build deck skeleton

Create `slides/deck.md` with:

- Required MARP metadata header
- Frontpage slide (structure unchanged; cover variant may vary)
- Closing slide (unchanged)

Insert all user slides **between** frontpage and closing.

#### Cover and section style preferences

Use the cover and section variant MARP class tokens exactly as listed in `.marp/references/deck-template.md`.

Selection rules (deterministic):
- If `definition/deck-definition.md` includes an explicit preference (recommended), use it:
  - `Style preferences: cover=<name>, section=<name>`
  - Example: `Style preferences: cover=light, section=dark`
- Else, consult `.marp/references/brand-style-guide.md §5` and apply the tone guidance there without overriding it.
  - Only ask the user if the tone is still ambiguous after consulting the brand guide.
- Apply the background selection policy in `.marp/references/deck-template.md`.

---

### 3. Render slides deterministically

For each slide (in order):

#### 3.1 Section slides

If the slide is a section divider:

- Use the class comment from the section variant table (e.g. `<!-- _class: section dark -->`)
- Render only the section title as `# Section Title`
- Ignore visuals and content

---

#### 3.2 Standard slides

For each standard slide:

1. **Layout**
 - Read `## Layout` from `deck-visual-design.md`
 - Map it to the closest valid pattern in `deck-template.md`
 - If no valid mapping exists → stop and report

2. **Content**
 - Render content strictly from `planning/deck-plan.md`
 - Use semantic Markdown or minimal HTML
 - Respect density and structure constraints

3. **Visuals**

- If `## Image` references an asset, insert it according to the layout context.

#### Slide class tokens (from visual design)

If `planning/deck-visual-design.md` includes explicit slide class tokens inside `## Layout`
(e.g. `Slide class: content visual-split image-wide no-top-accent`), render them verbatim
as the slide class comment, as long as they are allowed by `.marp/references/deck-template.md`.

If a class is requested but not supported by the template, stop and report the mismatch.

#### Branded rendering patterns (brand-style-guide compliance)

Apply the following patterns exactly as defined in `.marp/references/brand-style-guide.md`:
- Breadcrumbs → §9
- Callout labels → §10 (class tokens from `.marp/references/deck-template.md`)
- STEP labels → §9
- Emoji → §11
- Closing / tagline lines → §7

---

#### Render-safety modifiers (allowed, deterministic)

To prevent common theme-related rendering failures (overflow, cropped visuals), it is allowed to
apply these additional modifiers even if they are not explicitly listed in `deck-visual-design.md`,
as long as they are defined in `.marp/references/deck-template.md` and `.marp/themes/deck-theme.css`:

- `compact`:
  - Use when slide density is too high to fit at default typography.
  - Never use it to hide content; if it still doesn’t fit, stop and report the slide as unrenderable.
- `image-wide` / `image-tall`:
  - Compute the image aspect ratio from the PNG header; apply `image-wide` or `image-tall` per the threshold rules in `.marp/references/deck-template.md`.
  - Only apply when the slide class includes `visual-split` (or another image-centric pattern where it helps fit).

Slide title length rule (mandatory): Apply the slide title length rule from `.marp/references/deck-template.md`.

Respect the content budget hard caps defined in `.marp/references/deck-template.md`.

When the content budget is exceeded:
1. First reduce content (fewer bullets, shorter phrasing) — always preferred.
2. If all content is essential, add `compact` to the slide class token.
3. If the slide still exceeds budget with `compact`, stop and report the slide as unrenderable.

Use the image placement patterns and Markdown/HTML image syntax rules from `.marp/references/deck-template.md`.

---

### 4. CSS extension (exception-only)

Extend `.marp/themes/deck-theme.css` **only if**:

- `deck-visual-design.md` explicitly requires a layout
- AND no existing template class can express it

Rules:
- Minimal, reusable classes only
- No slide-specific CSS
- Follow CSS extension rules in the template

If extension is optional → do **not** add it.

---

### 5. Generate presenter notes

Create `slides/deck-notes.md`:

- One note block per slide
- Same order as `slides/deck.md`
- Notes must:
- Summarize slide intent
- Provide speaking cues
- Avoid adding new content or interpretation

Notes must remain aligned with the **plan**, not the visuals.

---

## Quality gates (mandatory)

Before finalizing:

- Frontpage and closing slide structures are unchanged
- Slide order and count match all inputs
- Every visual reference resolves to an existing asset
- No content appears that is not in the plan
- No layout appears that is not allowed by the template
- Slide density is moderate and readable
- CSS is extended only when unavoidable
- **Vertical balance**: every `content` slide must have its title near the top with body content flowing immediately below. A large whitespace gap between title and content signals the wrong layout class or a structural error in the HTML — do not patch by adding filler content. Verify the class tokens match the template mapping.
- **Bottom clearance**: no content element (card, tile, bullet, or table row) may be clipped at the slide bottom. If content overflows: reduce text first → then add `compact` → then report as unrenderable.
- **Process-flow constraint**: `process-flow` slides must not contain any content below the `.flow-cards` container. The baseline rail CSS extends below the card row; additional elements will overlap it or fall outside the safe area.
- **Brand compliance gate**: verify all brand rules by re-reading `.marp/references/brand-style-guide.md` — do not rely on any inline summary.

The output must be **render-ready and deterministic**.
