---
name: maps
description: "Use when building interactive map tools - Explains MapLibre setup, tiles, and common UI patterns."
---

## MapLibre basics

- Include MapLibre's CSS before your styles and load the script from https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js.
- Keep the map container absolutely positioned to fill the viewport (see `#map` styles in `tools/map-explorer/index.html`).
- Use the OpenFreeMap Liberty style (`https://tiles.openfreemap.org/styles/liberty`) unless a different basemap is required.
- Add navigation controls with `map.addControl(new maplibregl.NavigationControl(), 'top-right');`.
- Guard against missing globals: if `typeof maplibregl === 'undefined'`, disable map-dependent UI and show an error.

## Geolocation pattern

- Provide a dedicated button for `navigator.geolocation.getCurrentPosition`.
- Disable the button while locating, apply a loading state, and reset it in success/error callbacks.
- On success, create or update a `maplibregl.Marker` and `map.easeTo` the new center.
- On errors, surface user-friendly messages for permission, availability, and timeout cases.

## Overlay & interaction tips

- Keep status text in small, unobtrusive elements and update it via helper functions.

## Accessibility & layout

- Generally prefer maps that take up the whole viewport, with UI controls and panels overlayed
- Footer links in an overlay too.
