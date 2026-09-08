---
name: maplibre-v6-migration
description: Upgrading a MapLibre GL JS app from v5 to v6 — the ESM-only build, the removed default export, CommonJS require() breakage, the styleimagemissing/setMissingStyleImageResolver change, the removal of the internal map.transform, the MapDataEvent → MapSourceDataEvent/MapStyleDataEvent split, and the bundler-only setWorkerUrl() requirement. Use when a v5 app breaks after upgrading to v6, or before pinning a v6 install.
status: verified
---

# MapLibre GL JS v5 → v6 Migration

MapLibre GL JS v6 (released 2026-07-22) removed several things v5 code relied on: the UMD/CSP browser bundles, the default export, CommonJS support, the internal `map.transform`, and the `MapDataEvent` type. Most models' training data predates v6. So the natural-sounding answer to "how do I do X" is usually the v5 answer, and it breaks on v6.

**Primary reference:** the [MapLibre GL JS v5→v6 migration guide](https://maplibre.org/maplibre-gl-js/docs/guides/v5-to-v6-migration-guide/). This skill adds the gaps a model tends to fill with v5-era defaults. If the guide and this skill disagree, follow the guide and [report it](https://github.com/maplibre/maplibre-agent-skills/issues/new?template=ai-failure-report.md).

## When to Use This Skill

- Upgrading an existing MapLibre GL JS v5 app to v6, or debugging a map that "used to work" after a dependency update
- Writing one of the seven patterns below: a CDN `<script>` tag, an import statement, a `require()` call, a `styleimagemissing` handler, code that reads `map.transform`, a typed `data`/`dataloading`/`dataabort` handler, or a bundler setup (Vite, webpack, esbuild, Rspack, Rollup)
- Debugging errors like `ERR_PACKAGE_PATH_NOT_EXPORTED`, a blank map after a CDN update, a sprite icon that never appears, a TypeScript error naming `MapDataEvent`, or a worker-loading error that blocks render

**Don't use this skill to pad an unrelated answer.** It covers seven narrow breaking changes, not general v6 best practice. A question about sources, layers, styling, or terrain gets a normal, focused answer with no migration reminders attached.

## 1. CDN script tag: ESM-only now

v6 removed the UMD bundle and the separate CSP build. There's no `dist/maplibre-gl.js` for a plain `<script src="...">` tag anymore. Only the ESM build, `dist/maplibre-gl.mjs`, remains, and it needs `type="module"`.

```html
<!-- ❌ v5 — dist/maplibre-gl.js no longer exists in v6 -->
<script src="https://unpkg.com/maplibre-gl@5/dist/maplibre-gl.js"></script>

<!-- ✅ v6 — ESM build, type="module" required -->
<script type="module">
  import maplibregl from 'https://unpkg.com/maplibre-gl@^6.0.0/dist/maplibre-gl.mjs';
  const map = new maplibregl.Map({ container: 'map', style: '...' });
</script>
```

**Always pin an explicit major** (`@^6.0.0`, or a specific version). Never use `@latest` or a bare unversioned specifier — an unpinned CDN URL breaks the page silently the moment the next major version publishes. This already happened at the v5→v6 boundary.

## 2. No default export — named or namespace import only

v5's `import maplibregl from 'maplibre-gl'` (default import) no longer works in v6.

```js
// ❌ v5 — default export removed
import maplibregl from 'maplibre-gl';

// ✅ v6 — namespace import
import * as maplibregl from 'maplibre-gl';

// ✅ v6 — or import only what you use
import { Map, NavigationControl } from 'maplibre-gl';
```

This applies whether the code is new or converted from a Mapbox GL JS snippet (`import mapboxgl from 'mapbox-gl'`). Don't carry the default-import shape over either way.

## 3. No CommonJS — `require('maplibre-gl')` throws

`maplibre-gl`'s `package.json` `exports` field has only an `"import"` condition in v6, not `"require"`. So `require('maplibre-gl')` throws `ERR_PACKAGE_PATH_NOT_EXPORTED` in plain Node. That's expected behavior, not a bug in the caller's setup.

```js
// ❌ throws ERR_PACKAGE_PATH_NOT_EXPORTED in v6
const maplibregl = require('maplibre-gl');

// ✅ convert the file to ESM (named/namespace import — see item 2)
import { Map } from 'maplibre-gl';

// ✅ or, if the caller must stay CommonJS, load it dynamically
const { Map } = await import('maplibre-gl');
```

This section is only about a bare Node `require()` call. If a bundler is involved (webpack, Vite, etc.) and `require()` still fails, that's a separate ESM-interop config issue.

## 4. `styleimagemissing` no longer resolves the request — use `setMissingStyleImageResolver`

In v5, listening for `styleimagemissing` and calling `map.addImage()` synchronously from the handler would supply the missing icon. In v6, `styleimagemissing` is **notify-only**. Calling `addImage` from the handler no longer resolves the pending request.

```js
// ❌ v5 pattern — no longer resolves the request in v6
map.on('styleimagemissing', (e) => {
  map.addImage(e.id, generateIcon(e.id));
});

// ✅ v6 — register a resolver
map.setMissingStyleImageResolver((id) => {
  return generateIcon(id); // or return a Promise
});
```

Use this whenever a style references `icon-image` names that aren't in the sprite sheet and need to be generated or fetched at runtime.

## 5. `map.transform` is gone — use the public Camera API

v6 refactored `Map` to compose a `Camera` instead of extending it. `Map` now extends `Evented` directly and forwards the camera API. The internal `map.transform` property was removed as part of that change.

```js
// ❌ v5 — reaching into the internal transform
const { zoom, bearing, pitch } = map.transform;
const center = map.transform.center;

// ✅ v6 — public accessors
const zoom = map.getZoom();
const bearing = map.getBearing();
const pitch = map.getPitch();
const center = map.getCenter();
```

**There's no general public replacement for the raw projection/view matrix.** It was never exposed on `Map` itself, in v5 or v6 — it only ever lived on `map.transform`. The one place a matrix is still available is inside a custom layer's `render()` callback, via the callback's arguments (`CustomRenderMethodInput.getProjectionData()` / `defaultProjectionData`; see the [custom layers API](https://maplibre.org/maplibre-gl-js/docs/API/interfaces/CustomLayerInterface/)). Outside a custom layer, use the public getters above. For anything else the public API doesn't expose, open an issue or PR instead of reintroducing a private accessor.

## 6. `MapDataEvent` removed — use `MapSourceDataEvent` / `MapStyleDataEvent`

v6 made every fired event a real class, instantiated per event. The old catch-all `MapDataEvent` type is gone. `data`, `dataloading`, and `dataabort` are now typed as `MapSourceDataEvent | MapStyleDataEvent`. A source data event carries its full source info (`sourceId`, `tile`, `sourceDataType`, ...) directly on its own type, instead of a generic shared shape.

```ts
// ❌ v5 — MapDataEvent no longer exists in v6
import type { MapDataEvent } from 'maplibre-gl';
map.on('data', (e: MapDataEvent) => {
  /* ... */
});

// ✅ v6 — narrow on the union MapLibre now exports
import type { MapSourceDataEvent, MapStyleDataEvent } from 'maplibre-gl';
map.on('data', (e: MapSourceDataEvent | MapStyleDataEvent) => {
  if ('sourceId' in e) {
    // MapSourceDataEvent — e.sourceId, e.sourceDataType, e.tile
  } else {
    // MapStyleDataEvent
  }
});
```

The same fix applies anywhere a type import or annotation names `MapDataEvent`, including `dataloading` and `dataabort` handlers.

## 7. Bundled builds still need `setWorkerUrl()` — CDN ESM does not

v6 changed how the source-processing worker is located, but only for bundled apps. A plain CDN `<script type="module">` (item 1) auto-detects the worker URL from `import.meta.url` and needs no extra setup. Inside a bundler (Vite, webpack, esbuild, Rspack, Rsbuild, Rollup), `import.meta.url` doesn't reliably resolve to the worker file within the bundler's own module graph. Each of these setups needs one explicit `setWorkerUrl()` call, made once before creating the `Map`.

```ts
// ❌ v6 with a bundler, no setWorkerUrl() call — worker fails to load, map never renders
import { Map } from 'maplibre-gl';
const map = new Map({
  /* ... */
});

// ✅ Vite — the `?worker&url` query bundles the worker's own dependencies with it
import { Map, setWorkerUrl } from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url';

setWorkerUrl(workerUrl);
const map = new Map({
  /* ... */
});

// ✅ Webpack 5+ (Rspack and Rsbuild use the same pattern) — call setWorkerUrl() the same way, then create the Map
import { Map, setWorkerUrl } from 'maplibre-gl';

setWorkerUrl(new URL('maplibre-gl/dist/maplibre-gl-worker.mjs', import.meta.url).toString());
```

In Vite, use `?worker&url`, not plain `?url`. The worker file imports a sibling `maplibre-gl-shared.mjs`, and plain `?url` emits the worker verbatim without it. That makes the worker fail on its first import in production, so no vector tiles load. Esbuild, Rollup, and Turbopack need the same one-time call with their own asset-handling syntax; Next.js needs a different approach entirely. See the [install guide](https://maplibre.org/maplibre-gl-js/docs/) for current per-bundler snippets — this changes with tooling versions faster than the rest of this skill.

**Don't carry this into item 1's CDN case.** A plain `<script type="module">` import from a CDN URL never needs `setWorkerUrl()`.

## Reference

- [MapLibre GL JS v5→v6 migration guide](https://maplibre.org/maplibre-gl-js/docs/guides/v5-to-v6-migration-guide/) and its [CHANGELOG](https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md) (v6.0.0 section)
- [CustomLayerInterface API docs](https://maplibre.org/maplibre-gl-js/docs/API/interfaces/CustomLayerInterface/) and [install guide](https://maplibre.org/maplibre-gl-js/docs/) (per-bundler `setWorkerUrl()` snippets)
