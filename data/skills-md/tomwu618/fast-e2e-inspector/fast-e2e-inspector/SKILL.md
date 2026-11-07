---
name: fast-e2e-inspector
description: High-speed, deterministic E2E UI and CSS layout verification without slow interactive browser clicking. Combines static Git CSS diffing, build-chunk integrity probes, headless Playwright route-direct navigation, and mathematical DOM/CSS assertions (getBoundingClientRect, getComputedStyle, elementFromPoint hit-testing, and synthetic native events).
---

# Fast E2E & CSS Layout Inspector (`fast-e2e-inspector`)

Use this skill whenever verifying frontend UI changes, diagnosing white-screen / chunk-load errors, checking CSS layout width/alignment regressions against a Git baseline, or debugging `z-index` / stacking-context element occlusion.

## Core Philosophy: Never Click Around Blindly in a GUI Browser

Traditional interactive browser automation (opening a headed browser, clicking login, clicking menus step-by-step, taking screenshots at every step, and visually guessing pixel alignment) is slow, token-heavy, and error-prone.

Instead, follow this **4-Layer Short-Circuit Verification Pipeline** ordered from fastest (`0.1s`) to most thorough (`2s`):

```
Layer 1: Build & Network Probe (0.1s)      -> Catch white-screens & missing chunks via CLI before opening a browser
Layer 2: Git CSS Diff Scope Analysis (0.2s)-> Identify affected global/scoped selectors against a baseline commit
Layer 3: Direct-Route Headless Script (1-2s)-> Inject auth state, jump straight to target URLs, dispatch native DOM events
Layer 4: Mathematical DOM/CSS Assertions   -> Assert exact pixels, computed styles, and elementFromPoint(x,y) hit-tests
```

---

## Layer 1: Millisecond White-Screen & Chunk Integrity Probe (No Browser Needed)

When a route fails to load or renders a blank screen in a SPA (Vite / Webpack + Spring Boot / Nginx):

1. **Do NOT launch a browser first.**
2. Inspect `index.html` and the dynamic route chunk in `dist/assets/` vs. the backend's served static directory (e.g., `build/resources/main/static/assets/`).
3. Verify that:
   - Every `.js` and `.css` chunk referenced in `dist/assets/` exists in the served directory with **identical byte size** (catches partial/mid-build file copy race conditions).
   - `curl -sI <target-asset-url>` returns `HTTP 200` and the expected `Content-Length` and `Content-Type: application/javascript`.

Run the bundled helper script:
```bash
bash scripts/check-chunks.sh ./frontend/dist ./build/resources/main/static http://localhost:9020
```

---

## Layer 2: Git Baseline CSS Diff Scope Analysis

When asked to check if recent changes broke existing page styles compared to a baseline commit (e.g., `c0aa7e419`):

1. Extract only style and layout changes since the baseline:
   ```bash
   git diff <baseline-commit>..HEAD -- '*.css' '*.scss' '*.less' '*.vue'
   ```
2. Classify modified selectors into two buckets:
   - **Global / Unscoped Selectors** (e.g., `.el-card`, `.el-table`, `.app-main`, `body`): High blast radius. Must verify representative pages across all subsystems.
   - **Namespaced / Scoped Selectors** (e.g., `.saas-work-view`, `.nav-top[data-v-xxx]`): Zero impact on pages outside that container; only verify pages mounted inside that layout wrapper.

---

## Layer 3: Auth Injection, Direct Route Navigation & Synthetic Events

Bypass slow UI login forms and multi-level menu clicking in headless Playwright scripts:

1. **Auth State Injection**: Obtain a token once via `fetch`/`curl` or inject storage state directly via `context.addInitScript()` before navigation.
2. **Direct URL / Hash Navigation**: Jump straight to deep routes (`page.goto('http://localhost:3000/#/orders/detail?id=1001')`).
3. **Synthetic Native Events**: For special interactions (e.g., middle-mouse click to close tabs, wheel events, drag-and-drop), dispatch native DOM events directly inside `page.evaluate()`:
   ```js
   await page.evaluate((selector) => {
     const el = document.querySelector(selector);
     el.dispatchEvent(new MouseEvent('mousedown', { button: 1, bubbles: true, cancelable: true }));
     el.dispatchEvent(new MouseEvent('auxclick', { button: 1, bubbles: true, cancelable: true }));
   }, '.work-tab-item:nth-child(2)');
   ```

---

## Layer 4: Mathematical DOM & CSS Assertions (Replacing Eyeball Screenshot Guessing)

Never guess layout alignment or `z-index` occlusion from a screenshot alone. Query the browser's layout engine inside `page.evaluate()`:

### 4.1 Full-Width & Container Spacing Check (`getBoundingClientRect` + `getComputedStyle`)
Verify whether a child container fills its parent work area or is constrained by `max-width`, `margin`, or `padding`:

```js
const layoutReport = await page.evaluate(({ parentSel, targetSel }) => {
  const parent = document.querySelector(parentSel);
  const target = document.querySelector(targetSel);
  if (!parent || !target) return { error: 'Element not found' };

  const pRect = parent.getBoundingClientRect();
  const tRect = target.getBoundingClientRect();
  const tStyle = window.getComputedStyle(target);
  const pStyle = window.getComputedStyle(parent);

  return {
    viewportWidth: window.innerWidth,
    parentWidth: Math.round(pRect.width),
    targetWidth: Math.round(tRect.width),
    leftGapPx: Math.round(tRect.left - pRect.left),
    rightGapPx: Math.round(pRect.right - tRect.right),
    fillRatio: Number((tRect.width / pRect.width).toFixed(4)),
    targetCSS: {
      width: tStyle.width,
      maxWidth: tStyle.maxWidth,
      margin: tStyle.margin,
      padding: tStyle.padding,
      boxSizing: tStyle.boxSizing,
    },
    parentCSS: {
      display: pStyle.display,
      padding: pStyle.padding,
    }
  };
}, { parentSel: '.saas-work-content', targetSel: '.el-card' });
```

### 4.2 Z-Index & Stacking Context Occlusion Hit-Test (`document.elementFromPoint`)
Note that Playwright's `toBeVisible()` returns `true` even when an element (like a top-right dropdown menu) is covered by a sticky `<el-table>` column with a higher `z-index`!
Always use **coordinate hit-testing** (`document.elementFromPoint`) to prove an interactive element is truly on top:

```js
const occlusionReport = await page.evaluate((dropdownSel) => {
  const el = document.querySelector(dropdownSel);
  if (!el) return { error: 'Element not found' };

  const rect = el.getBoundingClientRect();
  const samplePoints = [
    { name: 'center', x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 },
    { name: 'topLeft', x: rect.left + 8, y: rect.top + 8 },
    { name: 'bottomRight', x: rect.right - 8, y: rect.bottom - 8 },
  ];

  // Walk up the DOM tree to inspect stacking contexts (position, z-index, transform, opacity)
  const getStackingChain = (node) => {
    const chain = [];
    let cur = node;
    while (cur && cur !== document.body) {
      const s = window.getComputedStyle(cur);
      if (s.zIndex !== 'auto' || s.position !== 'static' || s.transform !== 'none' || Number(s.opacity) < 1) {
        chain.push({
          tag: cur.tagName.toLowerCase(),
          className: cur.className,
          position: s.position,
          zIndex: s.zIndex,
          transform: s.transform,
        });
      }
      cur = cur.parentElement;
    }
    return chain;
  };

  const hits = samplePoints.map((pt) => {
    const hitEl = document.elementFromPoint(pt.x, pt.y);
    const isSelfOrChild = !!hitEl && (hitEl === el || el.contains(hitEl));
    return {
      point: pt.name,
      x: Math.round(pt.x),
      y: Math.round(pt.y),
      occluded: !isSelfOrChild,
      topElementTag: hitEl?.tagName?.toLowerCase(),
      topElementClass: hitEl?.className,
      occluderStackingChain: !isSelfOrChild && hitEl ? getStackingChain(hitEl) : [],
    };
  });

  return {
    targetRect: { left: rect.left, top: rect.top, width: rect.width, height: rect.height },
    targetStackingChain: getStackingChain(el),
    isOccluded: hits.some((h) => h.occluded),
    hits,
  };
}, '.who-drop');
```

---

## Bundled Scripts & Examples

- [`scripts/inspect-ui.mjs`](./scripts/inspect-ui.mjs): Standalone CLI runner that takes a URL, optional auth token, and target selectors, and outputs a JSON diagnostic report (console errors, failed network chunks, bounding box geometry, and `elementFromPoint` occlusion checks).
- [`scripts/check-chunks.sh`](./scripts/check-chunks.sh): Fast shell script to compare frontend `dist/assets` against backend static assets and detect missing or truncated files.
- [`examples/assertion-recipes.mjs`](./examples/assertion-recipes.mjs): Ready-to-copy Playwright snippets for width regression, dropdown occlusion, middle-click tab close, and batch baseline verification.
