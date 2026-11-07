---
name: true-web-clone
description: "True Web Clone: clone public websites from a URL into local files with source-first, asset-first, runtime-aware fidelity. Use when the user says True Web Clone, web clone, clone this website, mirror/download/recreate a website locally, preserve animations/components/special assets/Lottie/GSAP/Swiper/smooth scrolling/dynamic effects, clone WebGL/Three.js/Rive/canvas/3D resources, compare clone approaches, or says Chinese phrases such as 克隆网站, 复刻网站, 扒站, 下载到本地, 复制到本地, 完整复刻, 复刻动效, 直接复用资源, 复刻3D网站, 复杂动效网站."
---

# True Web Clone

## Goal

Produce a local, inspectable clone of a public website from one or more URLs. Prefer direct reuse of public frontend assets and runtime behavior before rebuilding by hand. Verify the clone with browser automation, not just visual intuition.

Use this skill for local research, learning, prototyping, migration analysis, or interaction study. Do not bypass authentication, paywalls, DRM, private APIs, or domain-bound third-party service keys. When a resource is authorization-bound, mark it and build a local fallback instead of pretending it was cloned.

## Default Output

Create a sandbox in the current workspace:

- `work/web-clone-benchmark/` for scripts, raw captures, candidate outputs, screenshots, and reports.
- `outputs/<site-name>-clone/` or the user-requested folder for the final chosen clone.

For each run, save:

- `ASSETS.json`: downloaded, failed, skipped, and blocked resources.
- `VERIFY.json`: runtime metrics, console errors/warnings, failed requests, screenshot paths.
- Desktop and mobile screenshots for source and clone.
- Short notes for anything that could not be directly reused.

## Workflow

1. **Clarify only if scope is risky**
   - If the user gives one URL, default to that page.
   - If the user says "whole site", crawl same-origin public pages with a conservative depth/limit, then report the page count and skipped areas.
   - If cloning could require login, payment, private data, or bypassing access controls, stop that part and propose a public/local fallback.

2. **Capture the source baseline**
   - Open the URL with Playwright or the available browser tool.
   - Save desktop and mobile screenshots, preferably `1440px` and `390px`.
   - Collect rendered HTML after network idle and after initial animations.
   - Record `console` messages and failed requests.
   - Record `performance.getEntriesByType("resource")` after load, after a short wait, and after scrolling through major sections. Many modern sites lazy-load models, textures, galleries, and videos only after scroll or after an initial scene is ready.
   - Detect runtime libraries with page evaluation:
     - `window.gsap`, `window.ScrollTrigger`
     - `window.Swiper`
     - `window.lottie` or `bodymovin`
     - `window.lenis`
     - custom canvas, WebGL, Three.js, Rive, video, map, feed, or player globals
   - If the source has canvas/WebGL/Rive/3D, read `references/complex-motion-3d.md` before building. These sites often need iterative resource discovery rather than a single static scrape.

3. **Inventory resources**
   - Extract resource URLs from rendered DOM, inline styles, CSS files, JS strings, `srcset`, `data-*` fields, manifests, and JSON.
   - Include images, SVG, fonts, CSS, JS, videos, Lottie JSON, Rive `.riv`, wasm, WebGL assets, shader/source maps when requested by the runtime, 3D buffers, compressed splats, poster frames, feed thumbnails, and same-origin API payloads that are public and reproducible.
   - Treat `.buf`, `.bin`, `.glb`, `.gltf`, `.ktx2`, `.basis`, `.hdr`, `.exr`, `.sog`, `.riv`, `.wasm`, `.mp4`, `.webm`, `.json`, `.webp`, `.avif`, and MSDF font atlas files as first-class clone assets.
   - Download same-origin public resources first. Download third-party library files only when needed for offline operation and permitted by normal browser access.
   - Preserve original filenames when possible. Use deterministic hashed names only when collisions occur.

4. **Build direct-reuse candidate first**
   - Start from the rendered DOM and original CSS/JS.
   - Rewrite all localizable URLs to `assets/...`.
   - Rewrite inside:
     - `src`, `href`, `poster`, `srcset`
     - CSS `url(...)`
     - inline style URLs
     - JSON strings, including escaped forms like `https:\/\/example.com\/...`
     - plugin data attributes such as `data-json`, `data-image-urls`, `data-src`
   - Keep original class names and DOM structure unless they actively break local execution.
   - Add a small local `clone-fixes.js` or `clone-fixes.css` only for stubs, fallbacks, loader unblocking, and compatibility repairs.

5. **Handle fragile dependencies**
   - Stub or block analytics, ads, cookie banners, tag managers, social trackers, and A/B testing scripts.
   - Treat Google Maps, form endpoints, WordPress nonces, admin AJAX, Instagram feeds, booking widgets, and private APIs as fragile.
   - Treat Typekit/Adobe font binaries, Vimeo/YouTube players, payment widgets, and domain-keyed SDKs as fragile. Localize what normal browsing can fetch; leave the service external or build a fallback when it is domain-bound.
   - If a fragile dependency is domain-bound but visually important, keep its container and data, then create a local fallback component.
   - Read `references/pitfalls.md` when diagnosing missing animation, blank blocks, blocked external scripts, or resource-rewrite failures.

6. **Restore motion only after reuse is exhausted**
   - If original JS runs, prefer fixing initialization order and missing globals over rewriting motion.
   - If original motion cannot run locally, add a focused `motion.js`.
   - Use the original libraries when detected: GSAP/ScrollTrigger, Swiper, Lottie/bodymovin, Lenis, Three.js, video players.
   - Avoid overusing `ScrollTrigger` scrub animations. Use once-only reveal animations for ordinary content and reserve scrub for sections that visibly need it.
   - Prefer official Lenis or the site's smooth-scroll library over custom wheel hijacking.

7. **Compare alternative candidates only when useful**
   - Test SingleFile when the user wants a quick saved-page baseline.
   - Test `website-scraper` plus Puppeteer when a site has many static resources but direct scripting is not enough.
   - Use AI rebuild only for missing, blocked, or unmaintainable parts. Do not make AI rebuild the primary path for special assets or complex motion.

8. **Verify with Playwright**
   - Serve the clone over a local HTTP server. Do not rely only on `file://`.
   - Use correct MIME types for module JS, wasm, fonts, images, `.buf`, `.riv`, `.sog`, video, and manifests. Complex clones can appear broken simply because the local server served a runtime asset as the wrong type.
   - Check:
     - no critical console errors
     - no failed local resources
     - expected image/font/script counts
     - runtime libraries exist
     - Lottie creates SVG/canvas
     - Swiper has an instance or equivalent behavior
     - smooth scroll exists when the source uses it
     - desktop and mobile screenshots look structurally aligned
   - Scroll through key sections and check hover/click states for navigation, cards, CTA buttons, sliders, maps, feeds, forms, canvas scenes, Rive canvases, video overlays, and 3D configurators.
   - For lazy-loaded 3D/canvas sites, repeat the loop: reload local page, collect local 404s, download missing same-origin resources, refresh, and continue until local 404s are gone or only intentionally external/blocked services remain.

9. **Choose and package**
   - Pick the highest-fidelity candidate, usually direct-reuse plus targeted fixes.
   - Copy only the final candidate into `outputs/...`.
   - Keep benchmark artifacts in `work/...`.
   - Tell the user what was directly reused, what was rebuilt, and what could not be reused due to authorization or server dependence.

## Scoring

When comparing candidates, score out of 100:

- Static visual fidelity: 30
- Motion and interaction fidelity: 35
- Offline/local reliability: 20
- Maintainability and editability: 15

Prefer a slightly less elegant codebase if it preserves public original assets and runtime behavior more faithfully.

## Common Triggers To Recognize

- "帮我克隆这个网站"
- "把这个网站下载到本地"
- "完整复刻这个网页/网站"
- "能不能直接复用它的资源/动效/组件"
- "clone this website"
- "mirror this site locally"
- "save this animated page with its interactions"
- "recreate the GSAP/Lottie/Swiper effects"

## Reporting

Keep the final user report short and concrete:

- output folder
- best approach used
- verification result
- non-reusable resources and why
- next useful fix if any
