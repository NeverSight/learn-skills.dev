---
name: animate
description: Master animation and micro-interaction skill that audits every interactive element in the project, adds or fixes animations using correct timing, easing, and CSS properties, verifies results with Playwright hover screenshots and video recording, and ensures prefers-reduced-motion is always respected. Use when user wants to add animations, improve micro-interactions, make the UI feel more premium, or invokes /animate.
---

# /animate — Master UI Animation

Adds and fixes animations across every interactive element, making the UI feel premium and alive. Works through elements in priority order, verifies every animation visually with screenshots and video, and never animates a property that triggers layout.

Before starting: read `~/.claude/skills/ui-design-principles/SKILL.md` — timing rules (100–250ms hover, ease-out enter, ease-in exit, only `transform` + `opacity`) live there and apply throughout.

If a `DESIGN-BRIEF.md` exists in the project root: read it before starting. The brief's **Animation level** field (Minimal / Subtle / Expressive / Very animated) overrides the default audit — don't add scroll-reveal animations to a product that decided on Minimal, and don't skip them for one that decided on Expressive.

---

## Phase 0 — Environment Setup

### 0a. Check / start dev server
```bash
curl -s --max-time 2 -o /dev/null -w "%{http_code}" http://localhost:3000
```
If not `200`, find and start the dev command in the background, then wait:
```bash
until curl -s --max-time 2 http://localhost:3000 > /dev/null 2>&1; do sleep 1; done && echo "ready"
```

### 0b. Detect animation library
```bash
grep -r "framer-motion\|motion/react\|@motionone\|react-spring\|gsap\|auto-animate" ./package.json ./apps/*/package.json 2>/dev/null || echo "none"
```

Map the result to the implementation approach used throughout:
- **Framer Motion** → use `<motion.div>` with `initial`, `animate`, `exit`, `whileHover`, `whileTap`
- **Motion One / `motion`** → use `animate()` function from `motion`
- **None (CSS / Tailwind)** → use Tailwind `transition-*` classes + `@keyframes` in globals.css

### 0c. Verify Playwright
```bash
node -e "require('@playwright/test')" 2>/dev/null && echo "ready" || echo "missing"
```
If missing: `pnpm add -D @playwright/test && npx playwright install chromium`

### 0d. Write the animation verification script
Write this to the **project root** (needs node_modules). Deleted in Phase 4.

**`_animate_verify.mjs`:**
```js
import { chromium } from '@playwright/test';
import { mkdirSync, renameSync } from 'fs';

const get = (f) => { const i = process.argv.indexOf(f); return i !== -1 ? process.argv[i+1] : null; };

const url      = get('--url');
const selector = get('--selector');
const action   = get('--action') ?? 'hover';   // hover | click | scroll | focus
const before   = get('--before') ?? '/tmp/animate-before.png';
const after    = get('--after')  ?? '/tmp/animate-after.png';
const video    = get('--video')  ?? '/tmp/animate.webm';
const width    = parseInt(get('--width')  ?? '1280');
const height   = parseInt(get('--height') ?? '900');
const auth     = get('--auth');

if (!url) { console.error('--url required'); process.exit(1); }

const videoDir = '/tmp/animate-video/';
mkdirSync(videoDir, { recursive: true });

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width, height },
  recordVideo: { dir: videoDir, size: { width, height } },
  ...(auth ? { storageState: auth } : {}),
});
const page = await context.newPage();
await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
await page.screenshot({ path: before, fullPage: false });

if (selector || action === 'scroll') {
  try {
    if (action === 'hover') {
      const el = page.locator(selector).first();
      if (!await el.count()) throw new Error(`Selector not found: ${selector}`);
      await el.hover();
    } else if (action === 'click') {
      const el = page.locator(selector).first();
      if (!await el.count()) throw new Error(`Selector not found: ${selector}`);
      await el.click();
    } else if (action === 'focus') {
      const el = page.locator(selector).first();
      if (!await el.count()) throw new Error(`Selector not found: ${selector}`);
      await el.focus();
    } else if (action === 'scroll') {
      if (selector) {
        // Scroll the target element into view
        await page.locator(selector).first().scrollIntoViewIfNeeded();
      } else {
        // No selector: scroll to bottom to trigger all scroll-reveal elements
        await page.evaluate(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }));
      }
    }
  } catch (err) {
    console.error(`Action failed: ${err.message}`);
    console.error('Check that the selector exists and the page has fully loaded.');
    await page.close(); await context.close(); await browser.close();
    process.exit(1);
  }
}

// Scroll reveals need longer — stagger + animation can exceed 800ms
const waitMs = action === 'scroll' ? 1500 : 600;
await page.waitForTimeout(waitMs);
await page.screenshot({ path: after, fullPage: false });

// Save video path BEFORE closing — the only reliable way to get it
const videoObj = page.video();
await page.close();    // triggers video file write
await context.close();
await browser.close();

if (videoObj) {
  const saved = await videoObj.path();
  renameSync(saved, video);
}
console.log(`before: ${before}\nafter:  ${after}\nvideo:  ${video}`);
```

**Usage:**
```bash
# hover state
node _animate_verify.mjs --url http://localhost:3000/pricing --selector ".pricing-card" --action hover --before /tmp/b.png --after /tmp/a.png --video /tmp/card-hover.webm

# modal open
node _animate_verify.mjs --url http://localhost:3000/dashboard --selector "[data-trigger='modal']" --action click --video /tmp/modal.webm

# scroll reveal
node _animate_verify.mjs --url http://localhost:3000 --action scroll --video /tmp/scroll.webm
```

After every run: **use the `Read` tool on both `before` and `after` PNG files** to see the difference. The video is the ground truth for whether the animation feels right.

### 0e. Handle auth-protected pages
Check if any interactive elements live behind a login wall. If so:

**Option A — reuse `/uiux` auth state (if already created):**
```bash
ls /tmp/uiux-auth-state.json 2>/dev/null && echo "exists" || echo "missing"
```
If it exists, pass `--auth /tmp/uiux-auth-state.json` to every `_animate_verify.mjs` call for protected routes. Done.

**Option B — create a fresh session:**
Write `_animate_auth.mjs` to the project root:
```js
import { chromium } from '@playwright/test';
const { TEST_EMAIL, TEST_PASSWORD, LOGIN_URL, SUCCESS_URL } = process.env;
if (!TEST_EMAIL || !TEST_PASSWORD) { console.error('Set TEST_EMAIL and TEST_PASSWORD'); process.exit(1); }
const browser = await chromium.launch();
const page    = await browser.newPage();
await page.goto(LOGIN_URL ?? 'http://localhost:3000/sign-in');
await page.fill('input[type="email"]',    TEST_EMAIL);
await page.fill('input[type="password"]', TEST_PASSWORD);
await page.click('button[type="submit"]');
await page.waitForURL(SUCCESS_URL ?? '**/dashboard**', { timeout: 15000 });
await page.context().storageState({ path: '/tmp/animate-auth-state.json' });
await browser.close();
console.log('Auth session saved → /tmp/animate-auth-state.json');
```
Run from the project root, then use `--auth /tmp/animate-auth-state.json`:
```bash
TEST_EMAIL=you@example.com TEST_PASSWORD=secret node _animate_auth.mjs
```

If no credentials are available: animate all public pages now, flag protected pages, revisit later.

---

## Phase 1 — Animation Audit

Find every interactive element and transition point.

**Step 1 — Locate the source root:**
```bash
# Find the src/ directory that contains the actual source (skips node_modules, .next, dist)
find . -type d -name "src" \
  -not -path "*/node_modules/*" \
  -not -path "*/.next/*" \
  -not -path "*/dist/*" \
  -not -path "*/.turbo/*" \
  | head -1
```
Use the result as `<SRC>` in all commands below (e.g. `./src`, `./apps/web/src`).
If no `src/` directory exists (some Next.js projects skip it), use the `app/` directory instead:
```bash
find . -type d -name "app" \
  -not -path "*/node_modules/*" \
  -not -path "*/.next/*" \
  | head -1
```

**Step 2 — Find element types and current animation state:**
```bash
SRC=<result from above>

# What transitions/animations already exist
grep -rn "transition\|animation\|@keyframes\|duration-\|ease-" "$SRC" --include="*.tsx" --include="*.css" -l

# Existing keyframes (check globals)
find "$SRC" -name "*.css" | xargs grep -n "@keyframes" 2>/dev/null

# Buttons
grep -rn "Button\|<button" "$SRC" --include="*.tsx" -l

# Modals / dialogs / sheets / drawers
grep -rn "Dialog\|Modal\|Sheet\|Drawer\|Popover" "$SRC" --include="*.tsx" -l

# Dropdowns / menus
grep -rn "DropdownMenu\|NavigationMenu\|Select\|Combobox" "$SRC" --include="*.tsx" -l

# Cards
grep -rn "Card" "$SRC" --include="*.tsx" -l

# Toasts / notifications
grep -rn "Toast\|Sonner\|useToast" "$SRC" --include="*.tsx" -l

# Loading / skeletons
grep -rn "Skeleton\|isLoading\|spinner" "$SRC" --include="*.tsx" -l

# Scroll-triggered sections
grep -rn "IntersectionObserver\|whileInView\|reveal\|scroll-" "$SRC" --include="*.tsx" --include="*.ts" -l

# Tabs / accordions / collapsibles
grep -rn "Tabs\|Accordion\|Collapsible" "$SRC" --include="*.tsx" -l

# Page/layout wrappers
grep -rn "layout\|PageWrapper\|AnimatePresence" "$SRC" --include="*.tsx" -l
```

For each element type found, screenshot it with `_animate_verify.mjs` and rate:
- **None** — no transition or animation at all
- **Wrong** — animating layout-triggering property, or wrong duration (instant/too slow), or wrong easing
- **Present** — has animation but needs tuning
- **Good** — correct property, duration, easing — skip

Present the full list grouped by type before continuing.

---

## Phase 2 — Priority Ranking

| Factor | Points |
|--------|--------|
| User interacts with it on every page visit | +3 |
| Currently has **no** animation | +3 |
| Currently has **wrong** animation | +2 |
| High visual impact (hero, modal, card) | +2 |
| Used only in settings / edge cases | −1 |

Rank by score. Ask the user to confirm before starting Phase 3.

---

## Phase 3 — Recursive Animation Loop

Work through element types in ranked order. Maximum **3 iterations per element type**.

---

### 3a. Screenshot / record before
Run `_animate_verify.mjs` with the correct `--action` for this element. **Read the before and after PNGs.** Note what the animation currently does (or doesn't do).

### 3b. Analyse
Check against the animation rules:

- Is it animating `transform` and/or `opacity` only? (never `width`, `height`, `padding`, `margin`, `top`, `left`, `border-radius` directly if it causes layout)
- Is the duration within the correct range? (see [PATTERNS.md](PATTERNS.md))
- Is the easing correct? (ease-out entering, ease-in exiting)
- Is the enter duration longer than exit? (enter = landing, exit = leaving)
- Does `prefers-reduced-motion` disable or reduce it?
- Does the animation feel mechanical (too linear) or floaty (too slow / bouncy)?
- Does it distract from the content or enhance it?

### 3c. Issue list
- **Critical** — animating layout-triggering property, missing prefers-reduced-motion, animation blocks interaction
- **Major** — wrong easing, wrong duration, no animation where expected
- **Minor** — slight timing tweak, stagger missing, could be more polished

### 3d. Implement fix
Apply the correct pattern from [PATTERNS.md](PATTERNS.md). Rules applied automatically:

**Always:**
- Only animate `transform` and `opacity`
- Enter: ease-out (decelerates into place — feels like landing)
- Exit: ease-in (accelerates away — feels like leaving)
- Enter duration > exit duration
- Every animation must include `prefers-reduced-motion` rule

**Never:**
- Animate `width`, `height`, `padding`, `margin`, `top`, `left`, `right`, `bottom`
- Go above 400ms for any UI element (scroll reveals can go to 600ms)
- Use `linear` easing — always use a curve
- Leave out the `prefers-reduced-motion` media query

**For height expand (accordion, collapsible):**
Use `max-height` from `0` to a known max, or use `grid-template-rows: 0fr → 1fr` (CSS-only, no layout thrash), or JS to measure real height.

**`prefers-reduced-motion` template:**
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```
(This should already exist in globals.css — verify, don't duplicate.)

### 3e. Wait and verify
```bash
sleep 3  # hot reload
node _animate_verify.mjs --url <URL> --selector <SELECTOR> --action <ACTION> \
  --before /tmp/after-b.png --after /tmp/after-a.png --video /tmp/after.webm
```
**Read both PNGs.** Watch the before/after difference.

Answer from what you see and what you know about the implementation:
1. **Property** — Is only `transform`/`opacity` moving?
2. **Duration** — Does it feel snappy (micro) or deliberate (medium)? Not instant, not slow.
3. **Easing** — Does it decelerate into place (enter) or accelerate away (exit)?
4. **Feel** — Does it feel premium, or robotic/floaty?
5. **Reduced motion** — Would it respect the user's preference?

If any answer is no: go back to 3d (increment iteration, max 3).

### 3f. Pixel-perfect animation checklist
Before advancing to the next element type:

- [ ] Only `transform` and/or `opacity` are animated
- [ ] Duration within range for this element type (see PATTERNS.md)
- [ ] Enter: ease-out. Exit: ease-in.
- [ ] Enter duration > exit duration
- [ ] Before/after screenshots show clear visual difference
- [ ] `prefers-reduced-motion` is respected (check globals.css rule exists)
- [ ] No layout thrash (no width/height/margin/padding animation)
- [ ] Animation doesn't block content or interaction
- [ ] Consistent with other elements of same type across the app

Any fail → go back to 3d. After iteration 3: flag and advance.

---

## Phase 4 — Cleanup & Report

Delete temp scripts:
```bash
rm -f _animate_verify.mjs _animate_auth.mjs
```

After each element type:
```
✓ [Element type] — K iterations — A critical + B major + C minor fixed
```

Final summary:

| Element Type | Count | Issues Fixed | Iterations | State |
|-------------|-------|-------------|------------|-------|
| Button hover | ...  | ...         | ...        | ✓ / ⚠ |
| Modal enter/exit | ... | ...      | ...        | ✓ / ⚠ |

List flagged items at the bottom.

---

## Rules

1. **Only `transform` and `opacity`.** If you're about to animate anything else, stop and find an alternative.
2. **Read every before/after screenshot.** The image wins over the code.
3. **Enter is ease-out, exit is ease-in.** No exceptions.
4. **Enter is longer than exit.** Entering deserves attention; exiting should be quick.
5. **`prefers-reduced-motion` is non-negotiable.** Every animation must respect it.
6. **Max 3 iterations per element type.** Flag and move on.
7. **Preserve functionality.** Never change logic or accessibility semantics.
8. **Consistency.** All buttons animate the same way. All modals animate the same way.

---

See [PATTERNS.md](PATTERNS.md) for all specific durations, easings, and code patterns by element type.
