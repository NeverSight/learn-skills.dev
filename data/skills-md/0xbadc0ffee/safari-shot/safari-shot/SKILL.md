---
name: safari-shot
description: Screenshot a web page as iPhone Safari shows it, without a simulator, to check what Safari paints under the status bar and toolbar (theme color, fixed headers and footers, Liquid Glass, overscroll, dark mode). Use when building or reviewing how a page looks in iOS Safari, or when a page's top or bottom bar color looks wrong on iPhone.
---

# safari-shot

`npx -y safari-shot` renders a page the way iOS Safari frames it on an iPhone: the page, the color
Safari paints under the status bar and toolbar (the **panels**), the glass toolbar and status bar
glyphs. Each PNG comes with a JSON report that says *why* each panel has its color.

## Steps

1. **Serve the page.** Any URL works, including `http://localhost:<port>` and `./file.html`. Done
   when the URL loads in a normal browser.
2. **Shoot every state the question touches.** Start with the defaults, then add what the page
   actually does:

   ```bash
   npx -y safari-shot http://localhost:3000 --state all --theme all
   ```

   `npx -y safari-shot --help` lists devices, iOS versions (27 by default; 26 and 18 selectable),
   orientations and the other options. The first run downloads Playwright's WebKit (about 100 MB).
   Progress goes to stderr; stdout is a JSON manifest of every PNG and report written. Done when
   the manifest lists one entry per requested combination.
3. **Read the PNGs and the reports.** Look at each PNG, then read `panels` in its JSON report to
   learn why each panel looks that way. Done when you can name, for every panel that matters,
   where its color comes from.
4. **Change the page and shoot again** until the panels look as intended (see
   [Steering the panels](#steering-the-panels)). Done when the new shots show the intended panels in
   every state from step 2.

## Reading a report

```json
"panels": {
  "top":    { "fill": "extension", "color": "#ff9800", "reason": "background-color of header.bar" },
  "bottom": { "fill": "content",   "color": "#ffffff", "reason": "no fixed/sticky container; ..." },
  "statusBar": "dark-content",
  "glass": "light",
  "overscrollColor": "#ff9800"
}
```

- `fill: "extension"`: Safari paints a solid `color` under that bar, taken from the fixed or sticky
  element named in `reason`.
- `fill: "content"`: page content scrolls under the glass and fades into the scroll edge.
- iOS 18 reports `fill: "tint"` (the solid status-bar band), `"material"` (expanded toolbar) and
  `"bar"` (collapsed toolbar).
- `statusBar`: `dark-content` is black glyphs, `light-content` white.
- `fixedEdges.atLoad` / `fixedEdges.final`: the raw per-side detection before and after scrolling.
  Safari keeps an edge color found at load while its element stays visible.
- `underPageBackground`: the color of the overscroll area and of every panel without an extension.
- `themeColor.usedByPanels`: whether `theme-color` affected the shot. iOS 26 and 27 ignore it;
  iOS 18 uses it for the status-bar band.

## Steering the panels

On iOS 26 and 27 the panels follow the page's own elements:

- **Solid color under a bar**: a `position: fixed` or `sticky` element touching that edge, about
  as wide as the viewport, with an opaque `background-color`.
- **Content under the glass**: no fixed or sticky element at that edge.
- **Overscroll and fallback color**: `html` and `body` backgrounds (images and gradients are ignored).
- **Dark mode**: declare `color-scheme: light dark` (CSS on `:root`, or
  `<meta name="color-scheme">`); otherwise Safari keeps a white page base in dark mode.

The full rules, with their WebKit sources, are in
[safari-rules.md](https://github.com/0xBADC0FFEE/safari-shot/blob/main/docs/safari-rules.md).

## Limits

- Standalone (home screen) mode is not modeled; iOS 18 is portrait only.
- Text renders in the host's fonts, not SF Pro, so text rows can sit a few points off; panel
  colors are unaffected.
- On Linux the first run may need system libraries: `npx playwright install --with-deps webkit`.
