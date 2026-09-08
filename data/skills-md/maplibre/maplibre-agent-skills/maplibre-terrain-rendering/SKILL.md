---
name: maplibre-terrain-rendering
description: Drawing elevation in MapLibre GL JS once a raster-dem source works — hillshade and `hillshade-method`, the `color-relief` layer and the `["elevation"]` expression, runtime contours with `maplibre-contour`, and 3D terrain with its camera and sky. Use when relief looks harsh, flat, or absent, or when the layer type or property for an elevation effect is unclear.
status: verified
---

# MapLibre Terrain Rendering

A `raster-dem` source is elevation, not a picture. Four different things draw it, each with its own layer
type or API, and most of the wrong answers here are Mapbox GL JS properties that MapLibre never had.

## When to Use This Skill

These are symptoms as you would observe them, before you know the cause:

- **Harsh hillshade contrast:** black-and-white ridges, blown-out slopes, chalky valleys — or several hillshade layers stacked to soften them (one layer with `hillshade-method: "multidirectional"`).
- **Dynamic elevation coloring:** the map needs coloring by height, client-side, with no pre-rendered tiles (a `color-relief` layer over `["elevation"]`, not `raster-color` on a `raster` layer).
- **Runtime contour lines:** contour lines straight from a `raster-dem` source, with no pre-generated contour tileset (`maplibre-contour`, not a hand-rolled marching-squares pipeline).
- **Flat 3D terrain:** `map.setTerrain()` is on and nothing extrudes (the camera is at `pitch: 0`, and raising `exaggeration` will not fix it).
- **Blank horizon:** pitching the camera shows empty page background above the terrain (no root-level `sky` object or `map.setSky()`; there is no `type: "sky"` layer in MapLibre).
- **Silent property failures:** a hillshade, sky, or terrain-coloring property does nothing and raises no error (a Mapbox GL JS property MapLibre never had).
- **Terrain lag or frame drops:** stutter when panning or tilting with terrain on (stacked hillshade passes, dense draped layers).

**Not this skill.** Elevation values that are wrong, spiky, or inverted, choosing an elevation tileset,
`encoding`, and generating DEM tiles — the style specification's `raster-dem` source page,
<https://maplibre.org/maplibre-style-spec/sources/#raster-dem>. Where hillshade sits among the other layers
of a style — [maplibre-cartography](../maplibre-cartography/SKILL.md).

## Which one you want

| Goal                                            | What draws it                                                         |
| ----------------------------------------------- | --------------------------------------------------------------------- |
| Shaded relief under a 2D map                    | A `hillshade` layer. No `setTerrain` needed — the two are independent |
| Color by height (hypsometric tint)              | A `color-relief` layer (GL JS 5.6)                                    |
| Contour lines, without pre-generating a tileset | The `maplibre-contour` library, feeding a `vector` source             |
| A tilted, extruded surface you fly over         | `map.setTerrain()` plus camera pitch                                  |

All four read the same `raster-dem` source; one source can serve all of them.

## Hillshade, and the harshness fix that is not stacking

Every `hillshade-*` property is a **paint** property.[1] The defaults that matter: `hillshade-exaggeration`
`0.5`, `hillshade-illumination-direction` `335`, `hillshade-illumination-anchor` `viewport` (the light is
fixed to the top of the screen, so it does not turn with the map's bearing unless you set `map`),
`hillshade-shadow-color` `#000000`, `hillshade-highlight-color` `#FFFFFF`.

Harsh output usually comes from the shading **method**, not the colors. `hillshade-method` (GL JS 5.5)
takes `standard` (the default), `basic`, `combined`, `igor`, and `multidirectional`.[1] `multidirectional`
lights the surface from several independent directions in one pass and `igor` minimizes the effect on the
map features drawn beneath it; both soften terrain on a single layer.

```json
{
  "id": "hillshade",
  "type": "hillshade",
  "source": "terrain-dem",
  "paint": {
    "hillshade-method": "multidirectional",
    "hillshade-exaggeration": 0.4,
    "hillshade-illumination-anchor": "map",
    "hillshade-shadow-color": "rgba(30,40,80,0.45)",
    "hillshade-highlight-color": "rgba(255,240,200,0.4)"
  }
}
```

**Do not stack several `hillshade` layers at different illumination directions.** It was the only way to
get multi-directional shading before 5.5; since then it is one paint property against N extra draw passes
over the same DEM. Pure black shadows and pure white highlights are the other harshness lever: give both an
alpha, and use warm highlights with cool shadows over imagery.

## Color-relief: coloring by height

`color-relief` (GL JS 5.6) colors a `raster-dem` source directly, client-side; there is no pre-rendering
step and no `raster` layer involved. Its paint properties are `color-relief-color`,
`color-relief-opacity` (default `1`), and, from GL JS 5.20, `resampling`.[1] The ramp is an `interpolate` expression over `["elevation"]`,
which returns meters above the DEM's vertical datum and **is only valid inside
`color-relief-color`**.[2]

```json
{
  "id": "hypsometric",
  "type": "color-relief",
  "source": "terrain-dem",
  "paint": {
    "color-relief-color": [
      "interpolate",
      ["linear"],
      ["elevation"],
      0,
      "#2c7bb6",
      500,
      "#abd9e9",
      1500,
      "#ffffbf",
      2500,
      "#fdae61",
      4000,
      "#ffffff"
    ],
    "color-relief-opacity": 0.8
  }
}
```

MapLibre has no `raster-color`, `raster-value`, or `raster-color-mix`; those belong to another renderer and
will be dropped as unknown properties. A `raster` layer pointed at a DEM shows packed RGB, not a tint.

## Contours at runtime

[`maplibre-contour`](https://github.com/onthegomap/maplibre-contour) derives vector contour tiles in a Web
Worker from the same DEM tiles and serves them through a registered protocol — no contour tileset to
build.[3]

```javascript
import mlcontour from 'maplibre-contour';

const demSource = new mlcontour.DemSource({
  url: 'https://tiles.mapterhorn.com/{z}/{x}/{y}.webp',
  encoding: 'terrarium',
  maxzoom: 12,
  worker: true
});
demSource.setupMaplibre(maplibregl);

map.addSource('contours', {
  type: 'vector',
  tiles: [
    demSource.contourProtocolUrl({
      thresholds: { 11: [200, 1000], 12: [100, 500], 14: [50, 200] },
      elevationKey: 'ele',
      levelKey: 'level',
      contourLayer: 'contours'
    })
  ],
  maxzoom: 15
});

map.addLayer({
  id: 'contour-lines',
  type: 'line',
  source: 'contours',
  'source-layer': 'contours',
  paint: { 'line-color': 'rgba(0,0,0,0.4)', 'line-width': ['match', ['get', 'level'], 1, 1.2, 0.6] }
});
```

`thresholds` maps zoom to `[minor, major]` intervals in meters; `level` is `1` on major contours, which is
what the line width and any label layer key on.[3] The `encoding` here must match the DEM exactly as it
does on the style source.

## 3D terrain, the camera, and the sky

```javascript
map.addSource('terrain-dem', { type: 'raster-dem', url: 'https://tiles.mapterhorn.com/tilejson.json' });
map.setTerrain({ source: 'terrain-dem', exaggeration: 1 });
map.setSky({
  'sky-color': '#199EF3',
  'sky-horizon-blend': 0.5,
  'horizon-color': '#ffffff',
  'horizon-fog-blend': 0.5,
  'fog-color': '#0000ff',
  'fog-ground-blend': 0.5
});
```

- **`terrain` takes only `source` and `exaggeration`** (default `1`).[4] It is a root-level style object,
  set in the style or through `map.setTerrain()`; `map.setTerrain(null)` turns it off.
- **Pitch is what makes it visible.** At `pitch: 0` an extruded surface is seen straight down and reads as
  flat. Set `pitch` on the map (or `map.easeTo({ pitch: 60 })`) before concluding the terrain is broken —
  and raise `exaggeration` only after the camera is tilted, never as the fix for a flat-looking map.
- **There is no `sky` layer type in MapLibre.** The layer types are `fill`, `line`, `symbol`, `circle`,
  `heatmap`, `fill-extrusion`, `raster`, `hillshade`, `color-relief`, and `background`.[1] Sky is a
  root-level `sky` object, or `map.setSky()`: `sky-color`, `horizon-color`, `fog-color`,
  `sky-horizon-blend`, `horizon-fog-blend`, `fog-ground-blend`, `atmosphere-blend`.[5] `sky-type`,
  `sky-atmosphere-sun`, and `sky-atmosphere-sun-intensity` are Mapbox GL JS properties and do nothing here.
  `fog-color` requires 3D terrain.[5]
- `map.queryTerrainElevation(lngLat)` returns the elevation under a location once terrain is on.[6]

**Cost.** Terrain decodes DEM tiles, builds a mesh, and re-draws every layer draped over it, so it is the
most expensive thing on this page — noticeably so at high zoom and pitch on low-end devices. Keep the
terrain stack small: one shared `raster-dem` source, one or two elevation layers, and only the overlays you
need.

## Related Skills

- [**maplibre-cartography**](../maplibre-cartography/SKILL.md) — Where a hillshade layer belongs in the layer order, and palettes that survive over relief.
- [**maplibre-pmtiles-patterns**](../maplibre-pmtiles-patterns/SKILL.md) — Serving DEM and imagery tiles from a single PMTiles file.

## References

1. **Style Specification: layers** — `hillshade` and `color-relief` paint properties, defaults, `hillshade-method` values, and the complete list of layer types — <https://maplibre.org/maplibre-style-spec/layers/>
2. **Style Specification: expressions** — `["elevation"]`, valid only in `color-relief-color` — <https://maplibre.org/maplibre-style-spec/expressions/>
3. **`maplibre-contour`** — `DemSource`, `setupMaplibre`, `contourProtocolUrl` — <https://github.com/onthegomap/maplibre-contour>
4. **Style Specification: terrain** — <https://maplibre.org/maplibre-style-spec/terrain/>
5. **Style Specification: sky** — <https://maplibre.org/maplibre-style-spec/sky/>
6. **GL JS `Map` API** — `setTerrain`, `setSky`, `queryTerrainElevation` — <https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/>
7. **Examples** — [3D terrain](https://maplibre.org/maplibre-gl-js/docs/examples/3d-terrain/), [sky, fog, terrain](https://maplibre.org/maplibre-gl-js/docs/examples/sky-fog-terrain/), [color relief](https://maplibre.org/maplibre-gl-js/docs/examples/add-a-color-relief-layer/), [contour lines](https://maplibre.org/maplibre-gl-js/docs/examples/add-contour-lines/), [multidirectional hillshade](https://maplibre.org/maplibre-gl-js/docs/examples/add-a-multidirectional-hillshade-layer/)

---

**This skill is a snapshot.** Where a primary source contradicts it — the References above, MapLibre's current documentation, or what MapLibre does when you run it — that source wins. Follow it, then [report the disagreement](https://github.com/maplibre/maplibre-agent-skills/issues/new?template=ai-failure-report.md), citing the source and your MapLibre version: editing your installed copy helps no one else and is overwritten on the next update.
