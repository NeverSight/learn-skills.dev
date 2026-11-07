---
name: visant-refine
description: 'visant-killer sub-skill: one shared anatomy for charts, gauges, sparklines, simulation sliders, metric tiles and control panels, so a screen looks designed, not assembled. Use on "add a chart", "simulator slider", "control panel", "inspector", "polish this", "gráfico", "painel de controles", "burilar", "refinar".'
---

# Visant Refine

Finishing. This skill assumes the decision to **include** the element was
already made and defended elsewhere, and only answers how it is drawn.

## The hierarchy, and it is not negotiable

| Skill | Decides |
|---|---|
| `visant-frontend` | **whether** the element exists, and which business variable it moves. The *cut test* runs there. |
| `dataviz` | whether the chart is **correct**: form, color by function, palette validation, anti-patterns. |
| `visant-motion` | the **SSoT** for easing and duration, plus the React, Tailwind and Radix gotchas. |
| `revenue-centric-design` | **why** animate this and not that (where attention is directed). |
| **this skill** | how the element is drawn, and how it looks like the same family as its neighbors. |

**Refine never justifies an element.** If the answer to "which variable does
this move" is silence, the fix is to delete, not polish. A beautiful chart of
data nobody uses is slop with better finishing, and it costs more attention than
the ugly version.

Work order, always in this sequence:

1. Pass the `visant-frontend` *cut test*. Name the variable per element.
2. Inventory what already exists. See "Before drawing" below.
3. Pick the form. Load `dataviz` **before** the first line of chart code.
4. Draw with the shared anatomy (table below).
5. Only then decide the animation, with [references/smart-motion.md](references/smart-motion.md).
6. Verify the way `visant-frontend` says (390px with real data, backend down,
   keyboard), and run both gates:

```bash
node ~/.claude/skills/visant-refine/scripts/refine-scan.mjs <target>   # finishing layer
node ~/.claude/skills/visant-killer/scripts/killer-scan.mjs --report AUDIT.md <target>
```

`--report` is not optional: `killer-scan` refuses to print GATE OPEN without
the surface table and the `## Screen seen` section (`## Tela vista` also works;
generate the skeleton with
`--init-report AUDIT.md`). And a zero from `refine-scan` alone is **not** a
complete pass: a clean detector feels like finishing because it ends in an exit
code, and that is exactly how `visant-frontend` gets skipped entirely.

`refine-scan` has six rules, all for things that compile, pass lint and still
break: raw color in a chart prop (only in files that import recharts), chart
without a state wrapper, unscoped `defs` `id`, easing or duration outside the
SSoT, `transition-all` and `ease-in` in UI, and width or height animation.
The state wrapper counts if the file mentions `ChartState`, `isEmpty`, `noData`,
`semDado` or `vazio`, so it works in any repo. Findings in `components/ui` are
suppressed (upstream primitive) and **counted at the end**, never hidden.
`--self-test` proves the six rules both ways before you trust a zero.

## Before drawing: discover what the repo already has

No new primitive without searching first. Almost every refine request is
composition, not construction, but you only know after looking. Run at the root
of the target repo, in this order:

```bash
# 1. installed chart lib (recharts, visx, nivo, chart.js, echarts, d3)
grep -E '"(recharts|@visx/[a-z-]+|@nivo/[a-z-]+|chart\.js|react-chartjs-2|echarts|d3)"' package.json
# 2. existing chart state wrapper and tooltip
grep -rlE 'ChartState|ChartContainer|ChartTooltip|isEmpty' --include=*.tsx --exclude-dir=node_modules .
# 3. slider, ratio bar and skeleton primitives
find . -path ./node_modules -prune -o -type f \( -iname 'slider.tsx' -o -iname 'progress.tsx' -o -iname 'skeleton.tsx' \) -print
# 4. motion tokens (easing and duration SSoT)
grep -rnE -- '--(ease|dur|duration)-[a-z0-9-]+:' --include=*.css --exclude-dir=node_modules . | head
find . -path ./node_modules -prune -o -type f -iname 'motion.ts*' -print
# 5. color token format (bare HSL channels or full color)
grep -nE -- '--(primary|muted-foreground|destructive):' $(find . -path ./node_modules -prune -o -name 'globals.css' -print)
```

Write down what you found in a "need | exists at" table before the first line.
For whatever is missing, search in this order:

1. **The repo itself** (the commands above).
2. **The Visant library**, [ui.visantlabs.com](https://ui.visantlabs.com/llms.txt),
   already-refined pieces from any project: `gauge`, `sim-slider`, `measure-bar`,
   `activity-heatmap`, `streamgraph`, `count-up`, `elastic-slider`, `skeleton-rail`.
   Install with `npx shadcn@latest add @visant/<name>`, with
   `"@visant": "https://ui.visantlabs.com/r/{name}.json"` in `components.json`;
   each one's spec sheet at `/r/<name>.md`.
3. **The official shadcn primitive** (`npx shadcn@latest add slider progress skeleton`).

Design system components are never created or edited without explicit
permission. Warn before installing. Primitive default overrides go **in the
consumer**.

## The shared anatomy

What makes a screen look designed is not each element being beautiful, it is all
of them telling the same thing in the same order. Every finishing element
carries these four roles, always in the same visual sequence:

| Role | What it is | How it shows |
|---|---|---|
| **label** | the name of what is measured | `text-xs uppercase tracking-wider text-muted-foreground` |
| **value** | the number that decides | heaviest weight in the block, `tabular-nums`, neutral |
| **qualifier** | the ruler that gives the value meaning (limit, goal, period, base) | `text-xs text-muted-foreground`, next to the value |
| **evidence** | the shape that shows the value against the ruler | bar, gauge, sparkline, band |

Rules for all four, in any element:

- **Color is the exception.** One neutral, and color only where there is a real
  exception. Text uses a text token, never the series color. Color follows the
  entity, never the ranking position.
- **No number without a ruler.** A value without a qualifier is trivia.
  "R$ 25.201,42" says nothing; "11,3% da receita bruta" does.
- **No denominator, no ratio.** Zero denominator is `null` and the row does not
  render. "0,0%" states a false fact.
- **A shape is only valid inside its domain.** A ratio bar has scale while the
  value fits the limit; past it, the bar saturates and lies, and the number
  saying how far it went replaces the bar. This is not a detail, it is the rule
  that shows up most.
- **Empty, error and loading are three states**, and all three are designed.
- **Same family at both ends:** when adding the second element of a kind,
  extract the first. Two variants of the same thing is the start of three.

Element catalog, each with anatomy, props and its typical mistake:
[references/elements.md](references/elements.md).

## Charts

Load `dataviz` and follow its procedure. What changes here, and is not there:

- **Series color comes from a token, and the token format is checked before the
  first line** (command 5 above). Where the CSS stores bare HSL channels
  (`--primary: 0 0% 9%`, the older shadcn default) the prop needs the wrapper:
  `stroke="hsl(var(--primary))"`. Bare `var(--primary)` yields the string
  `0 0% 9%`, which is not a color, and the stroke disappears with no error in
  `tsc`, lint or detector. Raw Tailwind palette and hex in JSX are out too: a
  class like `text-purple-400` slips past generic detectors.
- **A state wrapper surrounds every chart** (the repo's `ChartState`, or the
  equivalent command 2 found). An empty framed axis is dataviz's "0 items".
- **`clipPath` and `defs` ids collide by name.** Two charts on the same page with
  the same `id` overwrite each other; scope per instance.
- **Limits and goals are a `ReferenceLine`**, labeled, not a background color.
  The line is the fact; the color would be opinion.
- **`description` and heavy payloads stay out of the chart data.**

Ready recharts recipes (limit with `ReferenceLine`, cumulative crossing a band,
axis-less sparkline, ratio gauge) and the token-by-function map:
[references/charts.md](references/charts.md).

## Slider simulation

A slider that projects a scenario is a lying machine if the design does not
separate projection from fact. The minimum contract:

1. **The real value stays on screen, always**, marked on the track itself, and
   the label says which is which. Two numbers of the same unit and different
   kinds without labels corrupt the reading.
2. **Stops at the limits that matter.** The slider stops at the numbers that
   change the decision (a regime ceiling, a tax bracket), not at round multiples.
3. **The band is drawn on the track**, so the user sees where the regime changes
   before dragging.
4. **Back to real is one click**, and it only shows while a simulation is active.
5. **Nothing persists.** Simulation does not write to the database, and the URL
   only carries state if sharing is part of the request.
6. **Keyboard moves it**, `aria-valuetext` speaks the formatted value.

Full contract, with the state pattern and the classic mistakes:
[references/simulators.md](references/simulators.md).

## Control panels

An inspector or editor sidebar is the same anatomy at row scale: label left,
value right in `tabular-nums`, the unit as qualifier one tone dimmer, the
slider fill as evidence. What makes one look engineered instead of assembled:

- **The control takes the shape of the data.** 2–5 options are a segmented
  control, a point in 2D is a 3 × 3 grid, a vector is one row of fields, a
  gradient is its bar with stops on it, a curve is the curve plus its numbers.
  Cover the labels: if the shapes still say what they edit, it is designed.
- **The chrome takes the shape of the state.** Reset appears in a folder header
  only after a value changed; a dependent control exists only while its switch
  is On; rare actions sit behind one `⋯`; help is on demand, not a caption.
- **Depth by line, not by box.** Sticky folder headers, a dashed divider for
  nesting, quiet rows and loud values.
- **The mode comes before what it changes**, and every number takes drag,
  typing and arrow keys.

A dev-only tweak panel is an install (Leva, Tweakpane, DialKit), not a build.
Full rules, the data-to-control table and the DialKit-vs-fork case that
measured them: [references/control-panels.md](references/control-panels.md).

## Smart animation

Smart means **chosen by the variable**, not by opportunity. The rule that
generates the others: animate what carries the decision, at the moment the
decision changes.

- A value the user is producing by hand (dragging the slider) **does not
  animate**: it follows the finger. Animating here is latency that looks nice.
- A value that changes **as a consequence** (the total the slider recalculated,
  after release) may count up to the new number, short, once.
- **Crossing a limit is an event**, and an event deserves weight: the band's
  state change is the animation, not a glow on the card.
- Nothing animates on mount if the user already read that number in the previous
  navigation.
- A hundred times a day does not animate.

Decision table per case, with SSoT values:
[references/smart-motion.md](references/smart-motion.md).

## Worked case: tax panel

A tax simulation panel is the canonical example of all three topics together,
written step by step (what went in, what was refused and why) in
[references/tax-panel-case.md](references/tax-panel-case.md). Read it before
refining any number panel, because the mistakes are the same: a saturating bar,
projection confused with fact, and animation on the wrong data.
