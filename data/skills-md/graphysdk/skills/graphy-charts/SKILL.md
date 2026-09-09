---
name: graphy-charts
description: Build highly expressive charts with Graphy's viz stack (@graphysdk/react; advanced embedding via @graphysdk/viz-engine + @graphysdk/react-renderer). Also covers installing and setting up the SDK in a React codebase.
---

# graphy-charts

Build charts with **`@graphysdk/react`** — one package carrying the whole stack: the spec builders, `<GraphProvider>`/`<GraphRenderer>`, and the hooks. Under the hood it composes `@graphysdk/viz-engine` (a grammar-of-graphics compiler, framework-agnostic) and `@graphysdk/react-renderer` (paints the compiled output to SVG/DOM in React); install those two directly only for advanced embedding — see "Related packages" in `reference/react-api.md`.

## Mental model

The engine is a grammar of graphics in the ggplot2 / Vega-Lite tradition. You do not pick a chart type from a menu; you compose one from orthogonal primitives:

- A **layer** = a **geom** (geometry kind: `point`, `line`, `area`, `bar`, `rule`, `tile`) + an **aesthetic mapping** (data variable → visual channel) + a **stat** (per-layer reshape: `count`, `sum`, `mean`, `smooth`) + a **position adjuster** (`identity`, `stack`, `dodge`, `fill`).
- Chart types are compositions: a pie chart is `bar` + `position: 'fill'` + `coord.polar({ theta: 'y' })`; a donut adds `innerRadius`; a horizontal bar chart is `coord.flip()`; a radar chart is `line`/`area` + `coord.polar({ theta: 'x' })`; a heatmap is `tile` with the value on `color`.
- A reference line is `geom.rule()`. A trendline is `stat.smooth`. An average line is `stat.mean`.
- **Transforms** reshape data declaratively inside the spec: `transform.filter`, `transform.sort`, `transform.aggregate`, `transform.reshape` (wide→long), `transform.constant`. Prefer them over preprocessing `rows` in JS. Full option tables in `reference/spec-api.md`.
- **Scales** map data to visual values; **guides** (axes, legends, headline numbers) make scales legible. Calling `scale.x()` / `scale.y()` with no arguments infers the scale type from the data. Add a scale for every mapped positional aesthetic; `color` gets a default scale automatically.
- A **stylesheet** (`styles({ tokens, defaults, overrides })`) is a spec item like any other and owns **all paint**: geoms, grid and tick lines, panel border, graph background, every text, the tooltip, legend pills, headline cards, annotations (`reference/styling.md`).
- **Highlights** (predicate-driven emphasis) and **annotations** (arrows, text, shapes, images, …) are spec-level and serializable — the storytelling layer.

Data flows one way: raw `Data` → resolved `Spec` (defaults applied, types inferred, the authored stylesheet folded onto the built-in one) → `CompiledSpec` (render-ready, paint resolved per observation) → painted React output. You author the first step; the rest is automatic.

## Minimal chart

```tsx
import { createSpec, pipe, mapping, geom, scale, GraphProvider, GraphRenderer } from '@graphysdk/react';

const data = {
  columns: [{ key: 'month' }, { key: 'revenue' }],
  rows: [
    { month: 'Jan', revenue: 1200 },
    { month: 'Feb', revenue: 1850 },
    { month: 'Mar', revenue: 1600 },
  ],
};

const input = pipe(createSpec(), mapping({ x: 'month', y: 'revenue' }), geom.bar(), scale.x(), scale.y());

export function RevenueChart() {
  return (
    <GraphProvider data={data} input={input}>
      <GraphRenderer />
    </GraphProvider>
  );
}
```

This assumes the SDK is installed from npm and built by a bundler (`reference/install.md`). The
same chart also runs on a plain HTML page with no bundler, loading the SDK from a CDN URL — only
the imports change (`reference/cdn.md`).

Reference and recipe samples import from the underlying packages (`@graphysdk/viz-engine`,
`@graphysdk/react-renderer`). With the standard `@graphysdk/react` install, the builders, the
provider/renderer and the hooks come from `'@graphysdk/react'` instead — it re-exports the authoring
surface plus all of `@graphysdk/react-renderer`. A few engine internals the plugin and theme recipes
use (`RichTextContent`, `Rect`, `IdentityKey`, `readAuthoredNumber`, …) still import from
`@graphysdk/viz-engine`, which is installed as its dependency.

## The expressiveness ladder

1. **Spec + `config()`** — chart structure and chart-level options: layers, scales, coords, legend/axes settings, titles, headline numbers, number formats, layout.
2. **Stylesheet** — pipe `styles({ ... })` into the spec to repaint anything the chart draws, from geom fill to the tooltip box and legend pills. Predicate- and state-aware, serializable. This is the restyling tier — `reference/styling.md`.
3. **Theme tokens** — `themeOverrides` on `GraphProvider`, only for the HTML chrome the stylesheet has no target for: header/footer type, hover guide, tooltip row gap, legend overflow pill. React-only, not serializable.
4. **Slots** — replace whole regions (header, footer, tooltip, legend, headline, grid, axis ticks, axis label, swatch) with your own React components via the `slots` prop on `GraphRenderer`.
5. **Plugins** — change how a geom is painted (render-only override of a built-in geom) or add entirely new geoms/stats/transforms (`defineGeomRenderer`, `createGraphyKit`).

See `recipes/themes/` for complete worked examples at each tier.

## Where to look

Route by the intent of the request, not only the chart type it names. Comparative and narrative phrasing — "compare this with that", "show the increase", "call out the dip", "what changed since X" — is the storytelling layer (`reference/storytelling.md`).

| I want to… | Read |
|---|---|
| Official website, docs, or Discord support | [graphy.dev](https://graphy.dev) · [docs.graphy.dev](https://docs.graphy.dev) · [Discord](https://discord.gg/yGmYCjkSr) |
| Install the SDK, or fix a failed install (peer errors, unstyled graph, missing types) | `reference/install.md` |
| Use the SDK on a page with no bundler or npm (`<script type="module">`, jsDelivr) | `reference/cdn.md` |
| See the full spec builder API and every `config()` key | `reference/spec-api.md` |
| Check the exact signature, option keys, or accepted values of an exported symbol | `reference/types.md` |
| Filter, sort, aggregate or derive data inside the spec (`transform.*`) | `reference/spec-api.md` |
| Understand the `Data` format, parsing, value formats, wide→long reshape | `reference/data.md` |
| Render in React: provider/renderer props, sizing, animation, locales, error handling | `reference/react-api.md` |
| Recolor geoms; restyle grid, ticks, panel border, background, text, tooltip, legend pills, headline cards | `reference/styling.md` |
| Set the chart font, series palette, or dark mode colors | `reference/styling.md` |
| Replace the header, footer, tooltip, legend, headline, grid, axis ticks or axis label with React components | `reference/slots.md` |
| Annotate, highlight, add reference lines/trendlines/headline numbers/data labels | `reference/storytelling.md` |
| Compare two values or periods, show a change/gap/drop (difference arrows) | `reference/storytelling.md` |
| Author plugins: repaint a built-in geom or define a new one | `reference/plugins.md` |
| Bar or column chart (grouped, stacked, 100%, horizontal, negative) | `recipes/charts/bar.md` |
| Line chart (multi-series, dash styles, smoothing, missing values) | `recipes/charts/line.md` |
| Area chart (stacked, flipped) | `recipes/charts/area.md` |
| Scatter or bubble chart | `recipes/charts/scatter.md` |
| Pie or donut chart | `recipes/charts/pie-donut.md` |
| Radar / spider chart | `recipes/charts/radar.md` |
| Rose or racetrack (polar bars) | `recipes/charts/polar-bar.md` |
| Combo chart, dual y-axes | `recipes/charts/combo.md` |
| Heatmap, matrix, cohort grid, waffle | `recipes/charts/heatmap.md` |
| Apply a complete house style | `recipes/themes/` — see the Themes section below |
| Repaint a built-in geom | `recipes/plugins/sketchy-bar.md` |
| Minimal custom geom to model a new one after | `recipes/plugins/lollipop.md` |
| Custom geom with two geometries per observation | `recipes/plugins/dumbbell.md` |
| Custom positional aesthetics (open/high/low/close) | `recipes/plugins/candlestick.md` |
| Custom layout + hit-testing geometry | `recipes/plugins/treemap.md`, `recipes/plugins/voronoi.md` |
| Simulation-driven or pointer-owning geoms | `recipes/plugins/beeswarm.md`, `recipes/plugins/force-directed.md` |
| Multi-part flow geometry | `recipes/plugins/sankey.md` |
| Check a spec compiles before rendering | `scripts/validate-spec.mjs` (module shape in its usage header) |

## Themes

Complete house styles ready to apply or adapt. Each file states its tier, then gives palette/font constants, the spec stylesheet (geoms, chrome, tooltip, legend, headline), a small `ThemeOverrides` for the header/footer chrome, a shared `config()` builder, and worked example specs. All are stylesheet + config unless noted.

| Theme | Look | File |
|---|---|---|
| Braun | Dieter Rams minimalism: warm greys, ink pill bars, no grid, one orange accent | `recipes/themes/braun.md` |
| Financial Times | FT editorial: salmon paper, claret + Oxford blue, color-keyed headlines | `recipes/themes/financial-times.md` |
| International | Newspaper style: white plates, ink-and-grey series, one red accent | `recipes/themes/international.md` |
| Lenny's Newsletter | Warm newsletter: cream grounds, rounded corners, autumn orange ramp | `recipes/themes/lennys-newsletter.md` |
| Neo Brutalist | Near-black sheets, dashed borders, acid `#C8FF00` for data only (one `Swatch` slot) | `recipes/themes/neo-brutalist.md` |
| Mexico 68 | Olympic op-art: magenta-led palette, concentric outline geoms (plugin tier) | `recipes/themes/mexico-68.md` |

## Validating without rendering

The engine compiles without a DOM. `scripts/validate-spec.mjs` compiles a `{ data, input }` module headlessly and prints diagnostics — run it to check a spec before wiring it into React:

```bash
node scripts/validate-spec.mjs path/to/my-spec.mjs
```

## Hard rules

- Mappings, transforms and aesthetics reference columns by `key`, never by `label`.
- Every consumer must wrap `GraphRenderer` in a `GraphProvider`; the renderer has no standalone mode.
- The `plugins` array on `GraphProvider` is frozen at mount — remount with a React `key` to change it.
- Everything the chart draws is painted from the spec stylesheet (`styles`), varying per observation via `style.geom(decls, { where })` and per series via `{ layer }`. Reach for `themeOverrides` only for header/footer type, the hover guide, tooltip row gap and the legend overflow pill.
- Built-in style tokens are `geom`, `geomBorder`, `ruleLine`, `gridLine`, `graphBackground`, `textPrimary`, `textSecondary`, … (`reference/styling.md`). A declaration outside a target's vocabulary is dropped with an `INVALID_STYLE_RULE` warning; an unknown geom param is dropped silently — a change with no visible effect is usually one the wrong target carried.
- Chart text never inherits the page font. Set `style.graph({ fontFamily })`, and load the font before the chart measures.
- You never import a stylesheet; each entry point imports its own CSS. Editing lives behind the `@graphysdk/react-renderer/editable` entry point (`EditableGraphRenderer`, `EditorPanel`) — `mode="editable"` on a plain `GraphRenderer` renders no editor surface. Making charts editable, editing them programmatically, and the editor panel are the `graphy-editor` skill.

## Resources

- [Website](https://graphy.dev)
- [Docs](https://docs.graphy.dev)
- [Discord](https://discord.gg/yGmYCjkSr)
