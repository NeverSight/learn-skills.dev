---
name: living-world
description: Build a living 3D world of any real place, after studying it. Studies the place first (its trees and where each grows, what grows under them, its birds, the colour of its buildings, what happens there), writes that into a profile, then calls render_world, which builds one HTML file you can walk through, hear and share. Use when someone says "build a living world of <place>", "make a living world", "a world I can fly through", "make it look like a game", "real trees", "the forest in 3D", or wants to stand in a place rather than look down on it.
---

# Living world

You have the `render_world` tool from the living-worlds MCP server. If it is not visible yet, the server is still starting (the first run builds its Python environment with uv); wait a few seconds and look again before doing anything else.

## 1. Study the place first

A few minutes of searching, before anything is built. Say in one line that you are studying it, then look up:

- **Its trees:** the main species of its forest, where each grows (by water, on dry slopes, in an elevation band), their crown shapes and colours.
- **What grows under them:** ferns, shrubs or grass, its colour and how thick it is.
- **Its birds:** the ones a visitor sees or hears there. GBIF's records fill in the rest, and every bird gets its own recorded voice.
- **Its buildings:** what is distinctive about their walls and roofs. OpenStreetMap supplies the footprints and heights; the study supplies the colours.
- **What happens there:** one to three things the place is known for, as `events`: `roost` (birds gathering at dusk and streaming to a roost), `migration` (skeins of geese or cranes crossing), `crowd` (a stadium on game day). Each is `{ "kind", "title", "blurb", "hours": [from, to] }` plus its own fields.

Use the place's own ecology, not a generic forest. Keep only what you found support for, and say what you assumed.

## 2. Write the profile

The shape is in `render_world`'s description; `examples/multnomah-falls.profile.json` in this repo is a full one. Up to six species, each with `form` (`conifer` or `broad`), colours, `share`, and where it grows. Give each its `sci` name so its picture can be found. For a city, set `"setting": "city"`.

## 3. Build it

`render_world(place, profile=<the profile>)`, or `at=[lon, lat]` to build at an exact point. It takes about four minutes; say so before you start. `core_km` (default 4) is the detailed middle; `radius_km` (default 25) is how far the distance reaches, so widen it to take in a mountain someone names.

## 4. Show it

The world is one HTML file of 15 to 30 MB that opens in any browser with no server. It also appears in the Maps gallery at http://127.0.0.1:27530, beside every Groundstation map on the computer.

Reply with a short table of what it is made of and what the study found, then what to try: the three view buttons, time of day, wind, clouds, "Hear this place" for the sound mix, and pressing any bird's picture to hear it and fly to one.

Quote `caveats`. Where `core.lidar_share` is low or zero, tree heights are estimates. Tree shapes are always generated; their positions and heights are the data. Some bird recordings are licensed for non-commercial use only, and the caveat says so.
