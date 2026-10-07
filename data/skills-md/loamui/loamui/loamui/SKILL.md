---
name: loamui
description: >-
  Design and build UI with @loamui/core. The conductor for LoamUI work. It holds the philosophy
  and composition model, orders the work across the frontend-design, modern-css and
  modern-web-guidance skills, and runs the review before anything is reported. Use for any
  LoamUI build, design, theme or review task.
metadata:
  library: "@loamui/core"
  docs: https://loamui.com
  llms: https://loamui.com/llms.txt
---

# Using LoamUI

> Modern UI primitives for agent-assisted developers. A region declares what it
> means and the components inside adapt; you compose parts rather than configure
> props. The result must conform, and it must look designed for its subject.

## Where the truth lives

- **Offline references** generated from the docs ship under `references/`;
  start at [the index](references/index.md). Live twins: append `.md` to any
  <https://loamui.com> page; index at <https://loamui.com/llms.txt>.
- **Read a component's reference before using it**: parts, props, custom
  properties, when to use it and its accessibility contract live there.
- **Recipes** under `references/recipes/` are portable React and CSS with
  their design decisions. Match one by purpose, then adapt it; the
  [recipe guide](references/guides/guide.md) says how.
- The references match the library at the same commit. If behaviour differs,
  check the installed version in `node_modules/@loamui/core/package.json`.

## 1. Check the project

Run `npx loamui@latest doctor`. If it reports gaps, `npx loamui@latest init`
completes them additively; ask before it would replace conflicting tools or
styles. Setup is the tool's job, not yours: do not wire the stylesheet, lint
or checks by hand when the tool can. The `## LoamUI` section of `AGENTS.md`
records what it set up and the `check` command. Confirm the four skills are
discoverable by the active agent: `loamui`, `frontend-design`, `modern-css`
and `modern-web-guidance`. If setup is blocked or declined, agree a reduced
deliverable and say so in the report. Without a repository, establish what
the environment can do first; never fake `@loamui/core` exports, borrow
`loam-*` classes on raw elements, or call an approximation LoamUI.

## 2. Design before code

Follow the `frontend-design` skill: ground the work in the subject and
audience, write a short design plan (palette, typefaces, layout concept,
principles, the one memorable thing), review it for genericness, then build.
Where skills disagree the split is fixed: **the user's brief decides what;
frontend-design decides the direction; LoamUI decides the expression.** The
plan's colours become the token inputs as `light-dark()` pairs in `oklch()`,
its typefaces become `--loam-font` and `--loam-font-display`, its spacing
comes from the space scale, its rules live in layers and scopes, and no reset
goes underneath. [Design](references/guides/design.md) gives the mapping, the
theme stylesheet and the page-level guidance. The default palette and
`system-ui` are a starting point, not a design: a real product gets its own
theme.

## The three primitives

1. **Tokens** (`--loam-*`): a handful of semantic inputs, everything else
   derived. Theming is overriding the inputs.
2. **Element styles**: native HTML already styled, responsive and light/dark
   aware, page-wide.
3. **Components**: a curated set composed from the two above, added only
   where a native element lacks the structure: a field that wires its label
   and error, a dialog that traps focus, a menu with roving focus. For
   anything else, a semantic element with a scoped rule is your component.

## The rules

- **Native platform.** Real elements for semantics, static CSS for styling.
  Actions are buttons; destinations are links. `<dialog>` with `showModal()`,
  `<details>`, native controls with their labels and keyboard support.
- **Modern CSS.** Recipe rules in `@layer loamui.components` inside
  `@scope (.recipe) to ([class*="loam-"])`; nesting, logical properties,
  container queries, intrinsic grid and flex, additive non-overlapping query
  ranges. Inside a scope the markup is the API: reference elements by type
  (`h2`, `figure`, `nav`, `h1 + p`); a class is for a real distinction between
  siblings of the same type, never a hook for styling, and no wrapper element
  exists only to carry one. No `!important`, BEM, resets, pixel sizing or
  viewport units for size. The order `@layer loamui.tokens, loamui.elements, loamui.components;`
  must be established before any recipe registers a layer. Baseline Widely
  and Newly Available features are used natively; anything beyond that is a
  progressive enhancement, and the project's browser policy is never changed
  silently.
- **Composition.** Callable components for simple needs, named parts for
  composition, `render` for supported element swaps. Icons and loaders are
  children. Controls inside `Field.Root` receive their label, description and
  error wiring; `Field.Item` scopes a grouped option.
- **Contextualism.** Declare `--loam-context` on the region that carries the
  meaning; everything inside adapts. Size follows the available space. No
  `size`, `variant`, `color` or `fullWidth` props exist; the exceptions are
  intrinsic display sizes (`Badge`, `Loader`, `Progress`, `Meter`) and the
  platform's own numbers. Identity is the last resort: a brand-coloured
  wrapper is legitimate, a per-element colour is not.
- **Accessible.** Semantic HTML, named controls, keyboard and focus, user
  preferences. Never remove focus rings or carry state by colour alone.
  Required is the unmarked default; mark optional in words. Errors say what
  happened and how to fix it, in the words of the question. Show new errors
  after submission and clear a native constraint error once its correction
  is valid.

## Components

| Category     | Components                                                                                                                                                                                                 |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Inputs       | Field, Fieldset, ErrorSummary, Button, Input, Textarea, Select, DateInput, Checkbox, Radio, Switch, Range, Search, QuantityInput, Rating, FileInput, CopyButton, Combobox, PasswordInput, SegmentedControl |
| Data display | Badge, Price, Time, Card, Avatar, Table, Separator, Carousel, Stepper                                                                                                                                      |
| Feedback     | Alert, Progress, Meter, Skeleton, Loader, Toast                                                                                                                                                            |
| Disclosures  | Details, Tooltip, Modal, Drawer, Popover, Menu                                                                                                                                                             |
| Navigation   | Tabs, SignpostLink, SkipLink, Breadcrumbs, Pagination, Nav                                                                                                                                                 |
| Utilities    | VisuallyHidden                                                                                                                                                                                             |

No layout components (native grid, flex or flow with the space tokens), no
`Heading` or `Text` (a semantic element plus a scoped rule), no `Accordion`
(that is `Details`), no `Slider` (that is `Range`).

## 3. Compose

1. Search `modern-web-guidance` for each platform pattern the work needs and
   read the `modern-css` rules that apply; read the recipe guide, the nearest
   recipe and the contract of every part you use.
2. Write the theme stylesheet from the design plan; load it after core.
3. Assemble the page from recipes in a purposeful order, with section rhythm
   from the space scale and prose capped at `var(--loam-measure)`.
4. Lay out with native CSS. Theme with tokens on `:root` or a scope; never
   touch a component's internals or its private `--_*` properties.
5. Keep the deliverable portable: React and CSS, the integration the
   application needs, real actions behind a clear boundary, no docs-only
   machinery.

### When there is no recipe

The recipes are worked references, not a catalogue. A footer, a stats band, a
testimonial, a logo row, a pricing table: most of a real site has no recipe,
and building it well is the skill's job, not a gap. Work down the ladder and
stop at the first rung that answers the need:

1. A native element the element styles already dress: a `<footer>`, a
   `<table>`, a `<blockquote>`. Often nothing more is needed.
2. A semantic element with a scoped rule: `@scope (blockquote.testimonial)`.
   Name it for what it is in your product, not for a design-system alias.
3. A composition of existing components and elements: a `Card` grid, a
   `Nav`, a `Field` form.
4. Only then a new component, and only for behaviour a native element lacks.

Whatever the rung, give it the shape every recipe has: its own component
file with its stylesheet beside it, never inline JSX in a page; one root
class, rules in `@layer loamui.components` inside
`@scope (.root) to ([class*="loam-"])`, colour, space and type from tokens,
the measuring container outside the layout it controls, one job per section,
the right heading level, real content. A page assembles sections; it does
not contain them. Model the structure on the nearest recipe; never force its content.
Never borrow `loam-*` class names, invent a part, or substitute another
library. The review in step 4 applies to it exactly as to an adapted recipe.

## Mistakes people make by default

- **Inventing `size`, `variant` or `color` props.** Colour is a region, size is
  the container, width is the parent's layout. Modal and Drawer width are
  `--loam-modal-size` and `--loam-drawer-size`.
- **Leaving the defaults.** See Design before code.
- **`type="number"` for a count.** A count nudged by one is `QuantityInput`;
  any other number is `Input` with `inputMode`.
- **Borrowing `loam-*` classes on raw elements.** Class names are not API; the
  component carries wiring and tests the class does not.
- **A link dressed as a button.** Prominent navigation is `SignpostLink`;
  ordinary navigation is `<a>`; `Button` is for actions.
- **Duplicating Field wiring.** Let `Field.Root` supply it; add explicit IDs
  only for a real relationship. `useId` for repeated recipes.
- **Required asterisks and "This field is required".** See the rules.
- **Reset-then-restyle.** The element styles are the baseline; build on them.
- **Input's wrapper.** `className`, `style` and `ref` target the native input;
  `wrapperProps` targets its box. Input has `startSection` and `endSection`.
- **Removed spacing names.** `--loam-space-sm/md/lg` no longer exist; the scale
  is `4xs` to `4xl` with `--loam-space-fixed-*` for fixed geometry.

## 4. Review, then report

Nothing is reported until it has been reviewed, as a distinct pass with its
findings written down, in this order:

1. **Gates.** Run the project's `check` script (CSS lint, JS lint,
   composition, format), its type checker and tests. Fix what they report;
   never disable a check to pass it. Do not hand-review what they verify.
2. **Philosophy.** Reread the composition against the rules above: primitives
   in the right order, a native element before a component, context not
   props, parts not configuration, Field wiring, the scope donut, no reset,
   identity only where legitimate, each section its own component file.
3. **Modern CSS.** Reread the authored CSS against the `modern-css` rules no
   lint enforces: `oklch()` only, fluid `clamp()` with a rem term, flow-relative
   properties, `:has()` over state classes, container units over fixed
   spacing, non-overlapping ranges, motion opt-in, and for every class inside
   a scope, whether a type selector would have done.
4. **Modern Web Guidance.** For each pattern searched in step 3, confirm the
   guide's approach was taken, or say why not.
5. **Rendered result.** Both colour schemes at a narrow and a wide width,
   long copy, keyboard and focus, reduced motion, forced colours; every
   contrast pair the theme changed, measured. Then the design plan: one
   memorable thing, everything else quiet, one thing removed.

Each finding is `file:line`, the rule it breaks and the fix; fix it and
re-run the affected gate. Report what ran, what was found and fixed, what you
looked at, and what remains unverified. Passing checks are evidence for what
they check, never a blanket claim of conformance.

## Worked references

- Design, theme and page rhythm: `references/guides/design.md`.
- Tokens and dark mode: `references/guides/tokens.md`; layout:
  `references/guides/layout.md`; typography: `references/guides/typography.md`.
- Regions and identity: `references/guides/contextualism.md`.
- What `init` set up, and the agent contract in full:
  `references/guides/agent-workflow.md`.
- A composed form: `references/recipes/forms/sign-in-with-errors.md`; a page
  opener: `references/recipes/heroes/hero-with-image.md`.
- Every component: `references/components/<slug>.md`.
