---
name: fast-mp-inspector
description: High-speed, zero-click E2E, MVVM data, and WXSS layout/occlusion verification skill for WeChat Mini Programs (Native, uni-app, Taro). Combines static subpackage bundle probes, miniprogram-automator direct route jumping, AppService page.data() assertions, NodesRef.fields() geometry/AABB occlusion math, and instant simulator screenshots.
---

# Fast Mini-Program E2E & WXSS Layout Inspector (`fast-mp-inspector`)

Use this skill whenever verifying WeChat Mini Program (微信小程序 — Native, uni-app, or Taro) UI changes, diagnosing white screens or subpackage load failures, checking WXSS `rpx`/`px` layout width regressions, debugging `z-index` fixed-bar/modal occlusion, or asserting MVVM `Page.data` states.

## Core Philosophy: Respect the Mini Program Dual-Thread Architecture

Unlike web browsers, WeChat Mini Programs split execution across two threads:
- **AppService (Logic Thread)**: Runs JavaScript, `Page({ data })`, `wx.*` APIs, and `getCurrentPages()`. **Note: `window` and `document` do NOT exist inside `miniProgram.evaluate()`!**
- **WebView / Skyline (Render Thread)**: Renders WXML & WXSS.

Traditional Mini Program MCP servers force AI agents into slow, token-heavy loops (taking a screenshot $\rightarrow$ dumping the entire WXML tree $\rightarrow$ tapping tab bars $\rightarrow$ tapping lists $\rightarrow$ taking another screenshot).

Instead, follow this **4-Layer Short-Circuit Verification Pipeline** ordered from `0.05s` to `1.5s`:

```
Layer 1: Static Bundle & Subpackage Probe (0.05s) -> Check app.json routes, .wxml/.wxss/.js integrity & 2MB package limits
Layer 2: Git WXSS/Vue/TSX Diff Analysis (0.2s)    -> Separate global app.wxss changes from page-scoped styles
Layer 3: Direct Route Jump & Storage Mock (0.5s)  -> Inject wx.setStorageSync auth + miniProgram.reLaunch() + page.callMethod()
Layer 4: MVVM Data + SelectorQuery Geometry Math  -> Assert page.data(), NodesRef.fields() bounding rects, AABB occlusion & screenshot
```

---

## Layer 1: Static Mini Program Bundle & Subpackage Probe (No DevTools Needed)

When a Mini Program page renders a white screen or fails to navigate (`navigateTo:fail page not found` or subpackage load error):

1. **Do NOT wait for WeChat DevTools first.**
2. Locate the compiled Mini Program output directory:
   - **Native WeChat**: Project root or `miniprogram/`
   - **uni-app**: `dist/dev/mp-weixin` or `dist/build/mp-weixin` (or `unpackage/dist/...`)
   - **Taro**: `dist/` or `dist/weapp/`
3. Run `scripts/check-mp-bundle.mjs` to verify:
   - Every page registered in `app.json` (`pages` + `subPackages`/`subpackages`) has non-empty `.js`, `.json`, `.wxml`, and `.wxss` files on disk.
   - Main package and each subpackage stay strictly under WeChat's **2MB (2,048 KB)** single-package limit and **20MB** total limit.

```bash
node scripts/check-mp-bundle.mjs ./dist/dev/mp-weixin
```

---

## Layer 2: Git Baseline WXSS / Component Diff Analysis

When checking if recent changes caused style regressions against a baseline commit:
```bash
git diff <baseline-commit>..HEAD -- '*.wxss' '*.css' '*.scss' '*.vue' '*.tsx'
```
- **`app.wxss` / `uni.scss` / custom tab-bar / global components**: High blast radius; verify representative pages across main and subpackages.
- **Page-level `.wxss` or `<style scoped>`**: Zero impact outside that page route; jump directly to that single route via `miniProgram.reLaunch()`.

---

## Layer 3: Auth Injection, Direct `reLaunch` Navigation & Direct Method Invocation

Bypass slow UI login flows and multi-step `tabBar` tapping via `miniprogram-automator`:

1. **Connect to Existing DevTools WebSocket Port (Fastest, `<100ms`)**:
   Start DevTools automation port once (`cli --auto <project-path> --auto-port 9420`), then connect via `automator.connect({ wsEndpoint: 'ws://127.0.0.1:9420' })`.
2. **Inject Storage / Auth State Directly in AppService**:
   ```js
   await miniProgram.evaluate((storageMap) => {
     for (const [k, v] of Object.entries(storageMap)) {
       wx.setStorageSync(k, v);
     }
   }, { token: 'jwt-xxx', userInfo: { id: 1 } });
   ```
3. **Jump Directly to Any Deep Subpackage Route**:
   ```js
   const page = await miniProgram.reLaunch('/subpages/order/detail?id=1001');
   await page.waitFor(500);
   ```
4. **Trigger Business Logic or Custom Events Without UI Tapping**:
   ```js
   // Directly invoke a Page method defined in Page({ onConfirmTap(e) {} })
   await page.callMethod('onConfirmTap', { currentTarget: { dataset: { id: 1001 } } });
   ```

---

## Layer 4: MVVM `page.data()` + `SelectorQuery` Geometry & Occlusion Math + Screenshot

### 4.1 Direct MVVM State Assertion (`page.data()`)
Before parsing WXML text, inspect the reactive data model directly from AppService:
```js
const detailData = await page.data('detail');
const itemCount = (await page.data('items'))?.length ?? 0;
```

### 4.2 Single-Roundtrip Geometry & Computed WXSS via `NodesRef.fields()`
Remember: `document.getBoundingClientRect()` and `window.getComputedStyle()` do NOT exist in `miniProgram.evaluate()`. Instead, use WeChat's native `SelectorQuery.selectAll().fields({ rect: true, size: true, computedStyle: [...] })`:

```js
const layoutMetrics = await miniProgram.evaluate(({ parentSel, targetSel }) => {
  return new Promise((resolve) => {
    const sys = wx.getSystemInfoSync();
    const pages = getCurrentPages();
    const curPage = pages[pages.length - 1];
    const q = curPage && curPage.createSelectorQuery ? curPage.createSelectorQuery() : wx.createSelectorQuery();

    q.select(parentSel).fields({ rect: true, size: true, computedStyle: ['display', 'padding'] });
    q.select(targetSel).fields({
      rect: true,
      size: true,
      computedStyle: ['width', 'maxWidth', 'margin', 'padding', 'boxSizing', 'position', 'zIndex']
    });
    q.exec((res) => {
      const [p, t] = res || [];
      if (!t) return resolve({ error: 'Target element not found' });
      const pWidth = p ? p.width : sys.windowWidth;
      const pLeft = p ? p.left : 0;
      const pRight = p ? p.right : sys.windowWidth;
      resolve({
        windowWidth: sys.windowWidth,
        windowHeight: sys.windowHeight,
        pixelRatio: sys.pixelRatio,
        parentWidth: pWidth,
        targetWidth: t.width,
        leftGapPx: Math.round(t.left - pLeft),
        rightGapPx: Math.round(pRight - t.right),
        horizontalFillRatio: Number((t.width / Math.max(pWidth, 1)).toFixed(4)),
        targetWXSS: {
          width: t.width,
          maxWidth: t.maxWidth,
          margin: t.margin,
          padding: t.padding,
          boxSizing: t.boxSizing,
          position: t.position,
          zIndex: t.zIndex
        }
      });
    });
  });
}, { parentSel: '.page-container', targetSel: '.form-card' });
```

### 4.3 Deterministic AABB + Z-Index Occlusion Detection
Because `document.elementFromPoint(x, y)` is unavailable in AppService, detect whether a target element (e.g., a bottom action button or dropdown) is covered by fixed/sticky overlays (`.fixed-footer`, `.custom-nav`, `.modal-mask`) using **Axis-Aligned Bounding Box (AABB) intersection + Computed `z-index` comparison** inside `inspect-mp.mjs`.

### 4.4 Live In-Page `wx.request` Capture & Simulator Screenshot Guardrails
- **NEVER use external `curl` or hand-write fake JSON files** when verifying what an active Mini Program page requested. Use `--bounce-route "/pages/index/index" --capture-api "<api-path-pattern>" --save-api-json ./response.json` so `inspect-mp.mjs` leaves the page, hooks `wx.request` inside AppService, re-enters the target route, and saves the exact HTTP `statusCode` and `res.data` received by that page.
- **NEVER use OS window `screencapture` + image cropping/tiling (`sips`/`magick`/Python PIL)** to inspect the WeChat DevTools GUI window or slice it into dozens of tiles! That pollutes the workspace and report with dozens of garbage debugger fragments.
- **Preventing `EADDRINUSE` & Automator Timeouts**: Never manually invoke `cli --auto --auto-port 9420` or `automator.launch()` when WeChat DevTools is already open on port `9420` (doing so triggers a blocking `BackendManager listen EADDRINUSE` crash dialog inside DevTools). Always use `scripts/inspect-mp.mjs`, which automatically probes `127.0.0.1:9420` first to attach via `automator.connect()`, auto-resolves `dist/build/mp-weixin` or `dist/dev/mp-weixin`, and dynamically allocates a free port when launching a new instance.

---

## Bundled Scripts & Examples

- [`scripts/inspect-mp.mjs`](./scripts/inspect-mp.mjs): Standalone CLI runner supporting `--ws`, `--project-path`, `--route`, `--storage`, `--parent`, `--target`, `--occlude`, `--data-path`, `--screenshot`, and `--self-test`.
- [`scripts/check-mp-bundle.mjs`](./scripts/check-mp-bundle.mjs): Zero-dependency static analyzer for Native / uni-app / Taro Mini Program bundles (`app.json` route integrity + 2MB subpackage limit checks).
- [`examples/mp-assertion-recipes.mjs`](./examples/mp-assertion-recipes.mjs): Reusable assertion helpers (`assertMpFullWidthLayout`, `assertMpNotOccluded`, `assertMpPageData`, `triggerMpComponentMethod`, `captureMpScreenshot`).
