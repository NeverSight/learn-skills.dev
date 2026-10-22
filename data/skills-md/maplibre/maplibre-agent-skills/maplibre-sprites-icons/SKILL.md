---
name: maplibre-sprites-icons
description: Sprites and icon images for MapLibre GL JS — choosing a `Marker`, a sprite, or `addImage`; the `sprite` base URL and its `{id, url}` array form for several sheets; self-hosting and building sprites; runtime images, SVGs included, with `addImage`; finding a missing icon with the console warning and `hasImage`; and route shields that render as bare numbers. Use when deciding how to put icons on a map, when a symbol layer's icons never appear, when adding your own icons to a style whose sprite you do not control, or when shields are missing their badge.
status: provisional
---

# MapLibre Sprites and Icons

An icon on a MapLibre GL JS map is either part of the map, drawn by a symbol layer from a **sprite** (a PNG atlas plus a JSON index served from the style's `sprite` URL) or from an image registered at runtime with `addImage`, or on top of the map as a `Marker`, outside the style. For icon color, halos, and figure-ground against imagery, see [maplibre-cartography](../maplibre-cartography/SKILL.md); for text and glyph setup, see [maplibre-fonts-glyphs](../maplibre-fonts-glyphs/SKILL.md).

## When to Use This Skill

- Choosing between a `Marker`, a sprite, and `addImage` for icons on a map
- A symbol layer's icons do not render
- Adding your own icon sheet to a style whose `sprite` you do not control
- Setting up, self-hosting, or building a `sprite` from SVGs (for `glyphs`, see [maplibre-fonts-glyphs](../maplibre-fonts-glyphs/SKILL.md))
- Registering icons, including SVGs, for a layer your app adds at runtime
- Route shields render as bare numbers or missing badges
- Writing tooling that reads or generates symbol layers and has to recognize a shield

## Choosing a `Marker`, a sprite, or `addImage`

Two questions, in order; the sections below follow them.

1. **Is the icon part of the map, or on top of it?** Part of the map means a symbol layer's `icon-image`: placed together with the labels, hidden when it collides, and drawn in layer order, for a point dataset of any size. A small number of annotations on top of the map, that people drag or that need their own HTML, are [`Marker`s](#markers).
2. **For a symbol layer, where does the image come from?**
   - **The style.** POIs, town spots, shields, pattern textures, and any other icon or texture layered into the style, where it takes part in the visual hierarchy and collisions: a [sprite](#sprites). Your own set on a basemap whose sprite you do not control is a [second sheet](#multiple-sprite-sheets-in-one-style), still a sprite.
   - **Your app, at runtime.** Icons for a layer the app adds, such as a GeoJSON source, that no sheet carries: [`addImage`](#runtime-images-with-addimage). Use it deliberately. Each image is its own request and `addImage` call, where a sprite arrives as one PNG and one JSON, and its icons collide with the style's labels and with each other like sprite icons.

## Sprites

The style's `sprite` value is a **base URL with no file extension**; MapLibre appends `.json`, `.png`, and `@2x` variants itself.[1] A symbol layer names a sprite image in `icon-image` (other layers in their `*-pattern` property), and the name must exactly match an ID in the sprite JSON index or the icon is not drawn.

```json
{
  "sprite": "https://example.com/sprites/poi",
  "layers": [
    {
      "id": "cafes",
      "type": "symbol",
      "source": "places",
      "source-layer": "poi",
      "layout": { "icon-image": "cafe" }
    }
  ]
}
```

`https://demotiles.maplibre.org/styles/osm-bright-gl-style/sprite` works for testing; do not use it in production.

### Multiple sprite sheets in one style

`sprite` is not limited to a single string. Since MapLibre GL JS 3.0 ([#1805](https://github.com/maplibre/maplibre-gl-js/pull/1805)) it also accepts an **array of `{id, url}` objects**,[1] so a style can load its own icons alongside a basemap provider's sheet. Before 3.0 a style could name only one sprite, so adding your own icons meant merging them into the provider's sheet; with the array form, each sheet stays where it is hosted.

```json
{
  "sprite": [
    { "id": "default", "url": "https://tiles.openfreemap.org/sprites/ofm_f384/ofm" },
    { "id": "my-icons", "url": "https://example.com/sprites/poi" }
  ]
}
```

Rules that follow from that form:

- **Reference images by `id:image-name`** — `"icon-image": "my-icons:cafe"`. An unprefixed `"cafe"` resolves against the `default` sheet only.
- **The `id` `default` is the one exception**: its images take no prefix, which is what keeps an existing style's `icon-image` values working when you convert its string `sprite` to the array form. Give the basemap's sheet `id: "default"` and the shield and POI layers already in the style keep resolving unchanged.
- **All ids and all URLs must be unique.** Duplicates are a validation error (`all the sprites' ids must be unique, but <id> is duplicated`), not a last-one-wins merge.
- **Each URL is still extension-less** — MapLibre appends `.json`, `.png`, and the `@2x` variants per entry, exactly as for the string form.
- **From code, `map.addSprite('my-icons', 'https://example.com/sprites/poi')` adds a sheet** once the style has loaded; a string `sprite` becomes the array's `default` entry.[3]
- ❌ `{ "id": "my-icons", "url": "https://example.com/sprites/poi.json" }` → requests `poi.json.json`
- ❌ Typing `sprite` as `string` in your own tooling: an array value stringifies to `[object Object]`, and the loader rejects it with `Invalid sprite URL "[object Object]", must be absolute`. Handle both shapes wherever you read a style's `sprite`.

### Self-hosted sprites

To avoid third-party dependencies, copy an existing sprite directory (PNG + JSON, plus any @2x files) from a style or tileset provider and host it under your own domain, pointing the style's `sprite` property at its base URL. Always check the provider's license before republishing and add attribution if required.

Host sprite assets on a static host you control (same origin as the style). **Do not point production styles at `raw.githubusercontent.com`.** Raw is for serving repository blobs, not production assets: anonymous requests are aggressively rate-limited so real users see intermittent HTTP 429s [5], caching is fixed at five minutes with no control, there is no SLA, and private-repo URLs return 404 to everyone but authenticated collaborators (it works for you while logged in, then fails for every other user) [6].

### Building a sprite from SVGs

Generate sprite assets from a directory of SVGs with tools such as [spritezero](https://github.com/mapbox/spritezero), [spreet](https://github.com/flother/spreet), or [Martin](https://maplibre.org/martin/sources-sprites/).

Useful icon sources include [Maki](https://github.com/mapbox/maki) and [Temaki](https://github.com/ideditor/temaki). These are common source repositories for map-style SVG icons, but check each repository's license before republishing derived sprite assets.

## Runtime images with `addImage`

For a layer your app adds at runtime, register each image under an ID once the style has loaded, then name that ID in the layer's `icon-image`. Check the ID with `hasImage()` first: `addImage` on an ID the style already has fires an error (`An image named "<id>" already exists.`) instead of replacing it.[3] [8]

```js
map.on('load', async () => {
  // PNG, WebP, or JPEG: loadImage() resolves to a response whose data is the image
  const { data } = await map.loadImage('https://example.com/icons/cafe.png');
  if (!map.hasImage('cafe')) map.addImage('cafe', data);

  // SVG: an Image element, rasterized at its width and height
  const park = new Image(24, 24);
  park.crossOrigin = 'anonymous'; // or addImage throws on a cross-origin SVG
  await new Promise((resolve, reject) => {
    park.onload = resolve;
    park.onerror = reject;
    park.src = 'https://example.com/icons/park.svg';
  });
  if (!map.hasImage('park')) map.addImage('park', park);

  map.addSource('venues', { type: 'geojson', data: 'https://example.com/venues.geojson' });
  map.addLayer({
    id: 'venues',
    type: 'symbol',
    source: 'venues',
    layout: { 'icon-image': ['get', 'category'] } // 'cafe' or 'park'
  });
});
```

- ❌ `map.loadImage(url, callback)`. GL JS 4.0.0 removed the callback form,[4] so the callback never runs; `await` the promise.[3]
- ❌ An SVG through `map.loadImage()`, which takes PNG, WebP, or JPEG.[3] To load SVGs on demand, GL JS 6's `setMissingStyleImageResolver` takes the same `Image` route, as in MapLibre's [Display a remote SVG symbol](https://maplibre.org/maplibre-gl-js/docs/examples/display-a-remote-svg-symbol/) example.
- ❌ `sdf: true` on an ordinary SVG. An image marked `sdf` has its alpha read as a distance field and every opaque pixel painted `icon-color` (default black), so a multicolor icon turns into a one-color silhouette. Without `sdf`, `icon-color` and `icon-halo-*` do nothing: they only work on SDF icons.[2]
- **A symbol layer hides icons that collide by default** (`icon-allow-overlap` is `false`, and `icon-overlap` overrides it when set); `symbol-sort-key` decides which survive. Turning overlap on (`icon-allow-overlap: true`, or `icon-overlap: "always"`) draws every icon without checking collisions, which the GL JS [large-data guide](https://maplibre.org/maplibre-gl-js/docs/guides/large-data/) suggests at high feature counts; the icons then stack.
- ❌ `"icon-optional": true` to make colliding icons disappear. It applies only to a symbol with both an icon and text, letting the text show without its icon when the icon collides and the text does not; on a layer with no `text-field` it changes nothing.

`addImage`'s options take the same per-image metadata as the sprite index: `pixelRatio`, `sdf`, `stretchX`, `stretchY`, `content`, `textFitWidth`, and `textFitHeight`.[3]

## Markers

A `Marker`[7] is an HTML element over the map canvas, outside the style: drawn above every layer, labels included, and never part of collision detection.

```js
new maplibregl.Marker({ draggable: true })
  .setLngLat([-122.42, 37.77])
  .setPopup(new maplibregl.Popup().setText('Pickup point'))
  .addTo(map);
```

- **A `Marker` is one DOM element, repositioned on every camera move.** Fine for a small number of annotations on top of the map; for a point dataset, put the points in a GeoJSON source and draw them as a symbol layer.

## When an icon does not render

GL JS reports every icon it cannot find: the map fires `styleimagemissing`, and the console warns once per image ID, `Image "<id>" could not be loaded`.[8] A `sprite` URL that fails to load also fires the map's `error` event, which goes to `console.error` when nothing listens for it.[8]

After the `load` event, `map.hasImage(id)` tells the two causes apart:[3]

- **The sheet never loaded** when `hasImage()` is `false` for IDs the sprite JSON does contain. Check that the style sets `sprite`, that its URL has no extension, that its `.json` and `.png` return 200, and CORS.
- **The sheet loaded without that ID** when other sprite IDs return `true`. Compare the `icon-image` value with the sprite JSON's keys, including the `id:` prefix of a non-default sheet; `map.listImages()` returns every ID the map has.

## Broken route shields

Broken-looking route shields (bare floating numbers, missing badges) are almost always a **missing sprite image**. The shield number is text (font) and usually renders fine; the badge behind it is an `icon-image` from the sprite. Diagnose in this order:

1. **Confirm glyphs load.** Probe the `glyphs` server for the exact `text-font` names and expect HTTP 200. If they 200, you can deduce the culprit is a missing sprite image or broken reference.
2. **Confirm the sprite carries the shield images.** OSM Bright's shield layers use `icon-image: "{network}_{ref_length}"` for US networks (e.g. `us-interstate_2`, `us-highway_3`, `us-state_2`) and `road_{ref_length}` for other refs; OSM Liberty's use `default_{ref_length}`. A missing icon is omitted, so grep the sprite JSON for those keys.

The `https://demotiles.maplibre.org/styles/osm-bright-gl-style/sprite` and `https://openmaptiles.github.io/osm-bright-gl-style/sprite` sheets currently carry `road_1`–`_6`, `us-state_1`–`_6`, `us-highway_1`–`_3`, and `us-interstate_1`–`_3` (`_1`–`_5` on openmaptiles.github.io), but a minimal or custom sprite may ship only the generic `road_*`. If yours lacks the shield images and your tiles populate `network`, `ref`, and `ref_length` (the OSM US OpenMapTiles tiles do), point `sprite` at one that has them — the `{network}_{ref_length}` style layers then resolve with no layer edits.

**A shield is a badge image behind the route ref, sized one of two ways.** OSM Bright and OSM Liberty pick a pre-drawn badge per ref length, using the OpenMapTiles `ref_length` attribute to select the right one.[9] OSM Bright's interstate shield layer, abridged:

```json
{
  "id": "highway-shield-us-interstate",
  "layout": {
    "icon-image": "{network}_{ref_length}",
    "symbol-placement": {
      "base": 1,
      "stops": [
        [7, "point"],
        [7, "line"],
        [8, "line"]
      ]
    },
    "text-field": "{ref}"
  }
}
```

To use one badge image for every ref length, make it stretchable. In the badge's sprite JSON entry, `stretchX` and `stretchY` list the pixel ranges that may stretch, and `content` is the box the text must fit inside. On the shield layer, set `icon-text-fit` to `"both"` or `"width"`, plus `icon-text-fit-padding` for a margin around the text.[1] [2] `I-5` and `I-405` then share one image at two widths. OSM Bright and OSM Liberty use no stretchable badges, so a tool that recognizes shield layers must accept both kinds. Only a stretchable badge sets `icon-text-fit` (default `none`), and `text-anchor` defaults to `center`, so leaving it unset says nothing about a layer.

Code that reads layout values out of a style must not assume they are strings. OSM Bright's three shield layers and OSM Liberty's one set `symbol-placement` with a legacy zoom function, an object with `stops` that switches from `point` to `line`. Any symbol layout value can also be an expression, which is an array. A check like `layer.layout['symbol-placement'] === 'point'` is false for those layers, so the code skips them. Check whether the value is a string, a zoom function, or an expression before comparing it.

## Related Skills

- [**maplibre-cartography**](../maplibre-cartography/SKILL.md) — Icon color, `icon-halo-color`/`icon-halo-width`, and figure-ground for point symbols on aerial imagery; style layer ordering.
- [**maplibre-fonts-glyphs**](../maplibre-fonts-glyphs/SKILL.md) — The `glyphs` URL, font PBFs, and the GL JS local-font fallback; the text half of a shield.
- [**maplibre-source-wiring**](../maplibre-source-wiring/SKILL.md) — Where `sprite` sits among a style's other root properties, and CORS for self-hosted assets.
- [**maplibre-v6-migration**](../maplibre-v6-migration/SKILL.md) — `styleimagemissing` is notify-only in v6; `setMissingStyleImageResolver` is how a v6 map supplies an `icon-image` that is not in the sheet.

## References

1. [**Style Spec: `sprite`**](https://maplibre.org/maplibre-style-spec/sprite/) — the string and `{id, url}` array forms, image-name prefixing, the `default` id, and the sprite index file's `content`, `stretchX`/`stretchY`, and `textFitWidth`/`textFitHeight` fields
2. [**Style Spec: symbol layer properties**](https://maplibre.org/maplibre-style-spec/layers/#icon-text-fit) — `icon-text-fit` values (`none` default, `width`, `height`, `both`) and `icon-text-fit-padding`; `icon-color` and `icon-halo-*` are SDF-only
3. [**`Map.addImage()` (MapLibre GL JS API)**](https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/#addimage) — with `hasImage()`, `listImages()`, `addSprite()`, and `loadImage()` on the same page: `loadImage` takes PNG, WebP, or JPEG and resolves to a response whose `data` is the image
4. [**MapLibre GL JS CHANGELOG**](https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md) — "Add support for multiple `sprite` declarations in one style file" ships in 3.0.0; `map.loadImage` returns a `Promise` and drops its callback in 4.0.0 ([#3233](https://github.com/maplibre/maplibre-gl-js/pull/3233), [#3422](https://github.com/maplibre/maplibre-gl-js/pull/3422))
5. [**Unauthenticated rate limits on `raw.githubusercontent.com` (GitHub Community Discussion)**](https://github.com/orgs/community/discussions/159123) — anonymous requests are rate-limited; production traffic sees intermittent HTTP 429
6. [**`raw.githubusercontent.com` and private repositories (GitHub Community Discussion)**](https://github.com/orgs/community/discussions/69281) — private-repo raw URLs return 404/403 to anonymous requests
7. [**`Marker` (MapLibre GL JS API)**](https://maplibre.org/maplibre-gl-js/docs/API/classes/Marker/) — the `draggable` option, `setLngLat`, and `setPopup`
8. [**GL JS 6.11.2 `image_manager.ts`**](https://github.com/maplibre/maplibre-gl-js/blob/v6.11.2/src/render/image_manager.ts#L335-L338) — `styleimagemissing` and the missing-image warning; the duplicate-ID error is in [`style.ts`](https://github.com/maplibre/maplibre-gl-js/blob/v6.11.2/src/style/style.ts#L1004-L1007), and an `error` event with no listener goes to `console.error` in [`evented.ts`](https://github.com/maplibre/maplibre-gl-js/blob/v6.11.2/src/util/evented.ts#L191-L195)
9. [**OpenMapTiles `transportation_name` layer**](https://github.com/openmaptiles/openmaptiles/blob/master/layers/transportation_name/transportation_name.yaml) — `ref_length`: "Useful for having a shield icon as background for labeling motorways."

---

**This skill is a snapshot.** Where a primary source contradicts it — the References above, MapLibre's current documentation, or what MapLibre does when you run it — that source wins. Follow it, then [report the disagreement](https://github.com/maplibre/maplibre-agent-skills/issues/new?template=ai-failure-report.md), citing the source and your MapLibre version: editing your installed copy helps no one else and is overwritten on the next update.
