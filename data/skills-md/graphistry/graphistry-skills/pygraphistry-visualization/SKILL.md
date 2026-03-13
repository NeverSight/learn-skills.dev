---
name: pygraphistry-visualization
description: "Build PyGraphistry visualizations with bindings, encodings, layout controls, static export, and privacy-aware sharing. Use for color/size/icon/badge styling, layout tuning, map/static output, and plot link sharing workflows."
---

# PyGraphistry Visualization

## Doc routing (local + canonical)
- First route with `../pygraphistry/references/pygraphistry-readthedocs-toc.md`.
- Use `../pygraphistry/references/pygraphistry-readthedocs-top-level.tsv` for section-level shortcuts.
- Only scan `../pygraphistry/references/pygraphistry-readthedocs-sitemap.xml` when a needed page is missing.
- Use one batched discovery read before deep-page reads; avoid `cat *` and serial micro-reads.
- Use local icon lookup notes from `references/fa-icons.md`.
- In user-facing answers, prefer canonical `https://pygraphistry.readthedocs.io/en/latest/...` links.

## Core pattern
```python
g2 = (
    # Keep a plain 'type' column on both nodes and edges for legend-friendly defaults
    g.bind(point_label='label', point_color='type', edge_color='type')
     .encode_point_color('type', categorical_mapping={'agent': '#3b82f6'}, default_mapping='#94a3b8')
     # Optional: default node sizing is often degree for exploratory passes
     .encode_point_size('degree')
     .settings(url_params={'play': 3000, 'info': True})
)
g2.plot()
```

## External layout pattern
```python
# nodes_df contains x/y layout columns
g2 = graphistry.edges(edges_df, 'src', 'dst').nodes(nodes_df, 'id').bind(point_x='x', point_y='y').settings(url_params={'play': 0})
g2.plot()
```

## URL parameters reference
Use `settings(url_params={...})` to control visualization behavior. Full reference: https://hub.graphistry.com/docs/api/1/rest/url/#urloptions

### Layout
| Param | Type | Default | Range | Description |
|-------|------|---------|-------|-------------|
| `play` | int | 5000 | 0-10000 (0, 1000, 2000, 5000) | Layout duration ms. 0=fixed |
| `lockedX` | bool | false | | Lock X axis (with `bind(point_x=...)`) |
| `lockedY` | bool | false | | Lock Y axis (with `bind(point_y=...)`) |
| `lockedR` | bool | false | | Lock radial position |
| `linLog` | bool | false | | Strong separation; good for <1000 nodes |
| `scalingRatio` | float | 1.0 | 0.1-10 (0.5, 1, 2, 5) | Expansion ratio. Combine with `linLog` |
| `strongGravity` | bool | false | | Compact layout with pull to center |
| `dissuadeHubs` | bool | false | | Reduce hub dominance in layout |
| `gravity` | float | 1.0 | 0.1-10 (0.1, 1, 2, 10) | Pull strength toward center |
| `edgeInfluence` | float | 1.0 | 0-10 (0, 0.7, 1, 2, 5, 7) | Edge weight impact on layout |
| `precisionVsSpeed` | float | 1.0 | 0.1-10 (0.1, 1, 10) | Higher=precise but slower |
| `left/right/top/bottom` | int | auto | | Manual camera bounds on load |

### Scene / Rendering
| Param | Type | Default | Range | Description |
|-------|------|---------|-------|-------------|
| `pointSize` | float | 1.0 | 0.1-10 (0.3, 0.5, 1, 2, 3) | Point size multiplier (not encoding) |
| `pointOpacity` | float | 1.0 | 0-1 (0.3, 0.5, 0.8, 1) | Node transparency |
| `pointStrokeWidth` | float | 0 | 0-5 (0, 1, 2) | Node border width |
| `edgeCurvature` | float | 0 | 0-1 (0, 0.5, 1) | Edge bending amount |
| `edgeOpacity` | float | 1.0 | 0-1 (0.3, 0.5, 0.8, 1) | Edge transparency |
| `showArrows` | bool | true | | Show edge direction arrows |
| `neighborhoodHighlight` | str | both | incoming/outgoing/both/node | Hover highlight mode |
| `neighborhoodHighlightHops` | int | 1 | 1-5 (1, 2, 3) | Hops in hover highlight |

### Labels / Points of Interest
| Param | Type | Default | Range | Description |
|-------|------|---------|-------|-------------|
| `showLabels` | bool | true | | Toggle all label visibility |
| `showLabelOnHover` | bool | true | | Show labels only on hover |
| `showPointsOfInterest` | bool | true | | Highlight key nodes as POI |
| `showPointsOfInterestLabel` | bool | true | | Show labels on POI nodes |
| `pointsOfInterestMax` | int | 5 | 0-100 (0, 5, 10, 20) | Max POIs. 0=disable |
| `shortenLabels` | bool | true | | Truncate long labels |
| `showLabelPropertiesOnHover` | bool | false | | Show extra properties on hover |
| `labelOpacity` | float | 1.0 | 0-1 (0.5, 0.8, 1) | Label transparency |
| `labelColor` | str | | hex no # (000000, FFFFFF) | Label text color |
| `labelBackground` | str | | hex no # (000000, FFFFFF) | Label bg color |

Note: URL params use hex **without** `#`. Python API (`encode_*`, `palette`) uses `#` prefix.

### UI Controls
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `menu` | bool | true | Show all menus |
| `info` | bool | true | Show graph size stats |
| `showHistograms` | bool | true | Show histogram panel |
| `showInspector` | bool | true | Show entity inspector |
| `showCollections` | bool | false | Show collections panel |

### Examples
```python
# Ring layout with strong separation for small graphs (<1000 nodes)
g2 = g.settings(url_params={'play': 3000, 'linLog': True, 'scalingRatio': 2.0})

# Fixed position layout (external coordinates)
g2 = g.bind(point_x='x', point_y='y').settings(url_params={'play': 0, 'lockedX': True, 'lockedY': True})

# Disable POI labels entirely
g2 = g.settings(url_params={'showLabels': False, 'pointsOfInterestMax': 0})

# Larger points, more transparent edges
g2 = g.settings(url_params={'pointSize': 3.0, 'edgeOpacity': 0.3})

# Minimal UI for embedding
g2 = g.settings(url_params={'menu': False, 'info': False, 'showHistograms': False, 'showInspector': False})
```

## Icon/badge pattern
```python
g2 = (
    g.encode_point_icon('type', categorical_mapping={'person': 'user', 'org': 'building'})
     .encode_point_badge('risk', categorical_mapping={'high': 'exclamation-triangle'})
)
g2.plot()
```

Use valid Font Awesome names and keep icon mappings category-driven by `type`.
See `references/fa-icons.md` for lookup links and examples.

## Continuous-color pattern (beyond categorical maps)
```python
g2 = g.encode_edge_color('amount', palette=['#46327e', '#1fa187', '#fde724'], as_continuous=True)
g2.plot()
```

## Focused subgraph views (collection-like workflow)
```python
# Use GFQL slices to publish multiple focused views from one base graph
high_risk = g.gfql([...]).name('high-risk-slice')
partner_flow = g.gfql([...]).name('partner-flow-slice')
urls = [high_risk.plot(render=False), partner_flow.plot(render=False)]
```

## Privacy-safe sharing pattern
```python
graphistry.privacy(mode='private')
plot_url = g.plot(render=False)
```
- Use explicit `graphistry.privacy(mode='private'|'organization'|'public')` before plotting share links.
- Do not treat `plot()` kwargs like `as_files` or `memoize` as privacy controls.

## Common tasks
- Encodings: `encode_point_color`, `encode_edge_color`, `encode_point_size`, `encode_point_icon`, `encode_point_badge`.
- Layouts: runtime force layout settings, ring/GIB/modularity, graphviz/igraph/cugraph plugin layouts.
- Static outputs: `plot_static()` for SVG/PNG and text engines like `graphviz-dot`/`mermaid-code`.
- Sharing controls: `graphistry.privacy(mode='private'|'organization'|'public')`.
- For advanced gradients, use `palette=[...]` with `as_continuous=True` on `encode_point_color`/`encode_edge_color`.
- For large investigations, generate multiple focused GFQL slices instead of one overloaded plot.

## Big-graph defaults
- Filter and aggregate before plotting.
- Keep only essential columns (drop large text blobs unless needed).
- Use focused subgraphs (time slice, one-hop neighborhood, top-k signals).
- Prefer plain `type` columns on both nodes and edges so legends and default category encodings stay stable.
- Avoid dotted column names like `node.type` / `edge.type`; prefer plain names.
- Use native datetime types for time encodings and time-sliced comparisons.

## Canonical docs
- Visualization hub: https://pygraphistry.readthedocs.io/en/latest/visualization/index.html
- 10min visualization: https://pygraphistry.readthedocs.io/en/latest/visualization/10min.html
- Layout guide: https://pygraphistry.readthedocs.io/en/latest/visualization/layout/intro.html
- Layout catalog: https://pygraphistry.readthedocs.io/en/latest/visualization/layout/catalog.html
- URL parameters reference: https://hub.graphistry.com/docs/api/1/rest/url/#urloptions
- Privacy/sharing: https://pygraphistry.readthedocs.io/en/latest/server/privacy.html
- Visualization notebooks index: https://pygraphistry.readthedocs.io/en/latest/notebooks/visualization.html
- Icon lookup reference: `references/fa-icons.md`
