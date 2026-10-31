---
name: topographic
description: "Topographic terrain with the topographic library: 2D contour maps and 3D landscapes, generated or from real elevation data, for websites, videos and games. Use when asked to install topographic, or to add, change or export a topographic map or terrain with it."
---

# topographic

topographic draws moving contour lines with WebGL, as a flat 2D map or a 3D landscape, in plain HTML, any framework or React.

## Install check

Look for `topographic` in the dependencies of the project's `package.json`.

- **Missing:** follow [references/install.md](references/install.md) to its end, then continue below.
- **Present:** continue below.

## Example

One settings object drives everything, and `update()` changes it live:

```js
import { createTopography } from 'topographic';

const topography = createTopography(element, { shape: 'long-ridge', mode: '3d' });
topography.update({ terrain: { peaks: 3 } });
```

The same settings are props on `<Topography>` from `topographic-react`, and attributes on `<topographic-view>` after `import 'topographic/element'`.

## Guide sections

The guide is the source of truth for every name, range and default.
Read the section for the task before you write code:

| Task | Guide section |
|---|---|
| The API for vanilla, the web component and React | [Three ways to use it](https://github.com/yahyabedirhan/topographic/blob/main/docs/guide.md#three-ways-to-use-it) |
| Shape, lines, terrain, motion, layout | [Settings](https://github.com/yahyabedirhan/topographic/blob/main/docs/guide.md#settings) and [Shapes](https://github.com/yahyabedirhan/topographic/blob/main/docs/guide.md#shapes) |
| 3D view and camera | [Three dimensions](https://github.com/yahyabedirhan/topographic/blob/main/docs/guide.md#three-dimensions) |
| Colours and dark mode | [Colours, CSS variables and dark mode](https://github.com/yahyabedirhan/topographic/blob/main/docs/guide.md#colours-css-variables-and-dark-mode) |
| Size it, or put it behind content | [Sizing and layering](https://github.com/yahyabedirhan/topographic/blob/main/docs/guide.md#sizing-and-layering) |
| Next.js and server rendering | [Server rendering and Next.js](https://github.com/yahyabedirhan/topographic/blob/main/docs/guide.md#server-rendering-and-nextjs) |
| PNG, frames or video | [Snapshots and PNG export](https://github.com/yahyabedirhan/topographic/blob/main/docs/guide.md#snapshots-and-png-export), and `record()` in [Three ways to use it](https://github.com/yahyabedirhan/topographic/blob/main/docs/guide.md#three-ways-to-use-it) |
| Real elevation data | `setHeightfield()` in [Three ways to use it](https://github.com/yahyabedirhan/topographic/blob/main/docs/guide.md#three-ways-to-use-it) |
| It does not show or move | [Troubleshooting](https://github.com/yahyabedirhan/topographic/blob/main/docs/guide.md#troubleshooting) |

The guide on `main` matches the newest release.
For an older installed version, read the guide at its tag: `https://github.com/yahyabedirhan/topographic/blob/v<version>/docs/guide.md`.

To design a look by eye, open the playground at `https://topographic.yahyapak.dev/?analytics_agent=<name>&analytics_purpose=integrating`, with `<name>` such as `claude`, `cursor` or `other`, and copy its code from **Export**.

The work is done when the contour lines draw in the running page, or the exported file is written.
