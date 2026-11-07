---
name: roomfile
description: Use when decorating, furnishing, or restyling any room; discovering preferences from inspiration; preserving photos, measurements, constraints, products, and decisions across turns; checking furniture fit; researching regional retailers; or turning a room concept into a shopping and execution plan.
---

# Roomfile

Treat interior decoration as a durable project, not a sequence of disposable
image prompts. Keep room truth, taste evidence, concepts, products, and
decisions in `roomfile/`.

Work with any room and any style. Treat region, currency, units, retailers, and
local restrictions as project settings, not product boundaries.

## Resolve the skill directory

Resolve the absolute directory containing this `SKILL.md` as
`ROOMFILE_SKILL_DIR`. Run every bundled script from that directory.

## Route the request

Use `$roomfile` without arguments as `status`. Route explicit commands:

| Command | Outcome |
|---|---|
| `init` | Initialize a private room project and collect region, units, budget, retailers, constraints, and rendering preferences. |
| `status` | Inspect completeness and recommend the next actions. |
| `style` | Research a style, comparison, or design-history question without treating a label as the user's taste. |
| `taste` | Convert inspiration and reactions into evidence-backed preferences. |
| `capture` | Record canonical photos, measurements, fixed elements, and uncertainty. |
| `brief` | Create an approval-ready room design brief. |
| `explore` | Produce three materially different design directions. |
| `refine` | Revise one concept while preserving locks and decisions. |
| `place` | Check and visualize a named product in a concept. |
| `source` | Research current purchasable products without buying. |
| `plan` | Produce phased shopping, assembly, placement, and styling steps. |
| `audit` | Find spatial, evidence, sourcing, privacy, and reality gaps. |

Read `references/workflows.md` for command procedures.

For `style`, `taste`, `brief`, `explore`, `refine`, or style-aware rendering,
read `references/style-atlas.md`. The Atlas sharpens the conversation; it is
neither a preset library nor a style allowlist. Concrete user evidence always
outranks pack guidance.

## Start from project truth

`style` may answer a general research question without an initialized project.
Persist live research only when a project exists; otherwise provide cited
results in the response and offer `init`.

Before any project command except `init`:

1. Locate `roomfile/roomfile.json` from the working directory or the user-given
   project path.
2. Read the manifest, active room `ROOM.md`, `facts.json`, `geometry.json`,
   `products.json`, `STYLE.md`, `INVENTORY.md`, and approved decisions.
3. Treat provider sessions in `.runtime/` as local state. Never publish them.
4. Run `validate-project.mjs` before `brief`, `place`, `plan`, or final audit.

Classify every room fact as:

- **observed** — visible in a referenced photo or document;
- **measured** — supplied or confirmed with a physical measurement;
- **inferred** — plausible but unconfirmed;
- **desired** — a proposed change.

Never silently promote an observed or inferred fact to measured. A fact marked
`critical_for_fit` MUST be measured before claiming physical fit.

Read `references/data-model.md` before creating or changing structured files.

## Initialize mechanically

For `init`, first interview for country or region, ZIP or postal code (which may
remain blank until delivery checks), currency, units, budget, rooms, preferred
retailers, and whether the user wants agent-suggested local retailers. Write
those answers to a temporary JSON file matching
`references/schemas/profile.schema.json`, then run:

```bash
node "$ROOMFILE_SKILL_DIR/scripts/init-project.mjs" \
  --target ABSOLUTE_PROJECT_DIRECTORY \
  --privacy private \
  --profile ABSOLUTE_PROFILE_JSON \
  --json
```

Record household needs, local or rental restrictions, existing furniture, and
external image-processing consent in the generated project. Never assume a
country, currency, measurement unit, retailer, or delivery area. Direct script
use without `--profile` creates a neutral `needs-profile` scaffold.

Derive every direction from style evidence and enforce no style allowlist.

## Separate imagination from proof

Use image generation for visual exploration and label every result:

> Visual approximation — verify dimensions, color, material, and availability
> before purchasing.

Use `check-fit.mjs` and `render-layout.mjs` for dimension-based placement.
Photorealistic imagery cannot prove that an item fits.

Read `references/rendering.md` before `explore`, `refine`, or visual `place`.
Prefer Banana when installed; use the same `render-request.json` contract with
another available renderer. Ask before sending private room images to a new
external provider.

Before invoking a renderer, convert the structured request into a provider-ready
brief:

```bash
node "$ROOMFILE_SKILL_DIR/scripts/build-render-brief.mjs" \
  --request ABSOLUTE_RENDER_REQUEST_JSON \
  --output ABSOLUTE_RENDER_BRIEF_MD \
  --adapter banana \
  --json
```

When Banana is available, load Banana's current instructions, attach the
canonical image on the first render, and retain its returned interaction ID in
`.runtime/render-sessions.json`. Pass that interaction ID on refinements.

## Source real products carefully

Use the project-configured region and retailer preferences. Before searching,
ask for missing location, currency, units, delivery area when needed, and
`retailer_strategy`. If the strategy is `user-preferred`, search those
retailers first. If it is `agent-suggested`, propose locally available sources
that fit the role and record the chosen order. Record dated evidence,
dimensions, seller, region, delivery result, and retailer identifiers. Do not
use affiliate links.

Read `references/sourcing.md` before `source`, product-backed `place`, or
shopping-plan work. Never purchase, add to cart, contact a seller, or commit
money.

## Require approval at decision boundaries

Require explicit user approval before:

- marking a concept or product `approved`;
- replacing a locked element or approved decision;
- treating a proposed layout as the execution baseline;
- finalizing the shopping or execution plan.

Preserve rejected options and the reason for rejection. Do not equate aesthetic
preference with spatial safety or product evidence.

## Validate before reporting completion

Run:

```bash
node "$ROOMFILE_SKILL_DIR/scripts/validate-project.mjs" \
  --project ABSOLUTE_PATH_TO_ROOMFILE_DIRECTORY \
  --json
```

For placement, additionally run:

```bash
node "$ROOMFILE_SKILL_DIR/scripts/check-fit.mjs" \
  --geometry ABSOLUTE_GEOMETRY_JSON \
  --products ABSOLUTE_PRODUCTS_JSON \
  --json

node "$ROOMFILE_SKILL_DIR/scripts/render-layout.mjs" \
  --geometry ABSOLUTE_GEOMETRY_JSON \
  --products ABSOLUTE_PRODUCTS_JSON \
  --output ABSOLUTE_LAYOUT_SVG \
  --json
```

Report errors, warnings, dated sources, remaining assumptions, and the next
user decision. Read `references/safety.md` for rental, structural, electrical,
privacy, and professional-advice boundaries.
