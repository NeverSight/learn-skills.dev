---
name: uiux
description: Master UI/UX redesign skill that audits every screen in the project, ranks them by priority, then redesigns each one recursively until pixel-perfect — applying color theory, typography, hierarchy, spacing, and accessibility principles automatically. Use when user wants to improve, redesign, or polish the UI/UX of an app, says "make the UI better", "redesign this", "pixel perfect", or invokes /uiux.
---

# /uiux — Master UI/UX Redesign

A systematic, recursive redesign loop. Works through every screen from highest to lowest priority, iterating each one until pixel-perfect based on **what the rendered UI actually looks like**, not what the code says.

Before starting: read `~/.claude/skills/ui-design-principles/SKILL.md` — all color, typography, spacing, and hierarchy rules live there and apply automatically throughout.

If a `DESIGN-BRIEF.md` exists in the project root: read it before touching any file. It sets the visual direction (palette, typography, component style, animation level, defining screen). Design decisions in the brief override defaults — don't re-derive what's already decided.

---

## Phase 0 — Environment Setup

### 0a. Check / start dev server
```bash
curl -s --max-time 2 -o /dev/null -w "%{http_code}" http://localhost:3000
```
If the result is not `200`, find the dev command (`pnpm dev`, `npm run dev`, etc.) and start it in the background. Then wait for it to be ready:
```bash
until curl -s --max-time 2 http://localhost:3000 > /dev/null 2>&1; do sleep 1; done
echo "Server ready"
```

### 0b. Verify Playwright
```bash
node -e "require('@playwright/test')" 2>/dev/null && echo "ready" || echo "missing"
```
If missing:
```bash
pnpm add -D @playwright/test && npx playwright install chromium
```
If installation is impossible, ask the user to share screenshots after each fix. Do not make visual claims without real visual input.

### 0c. Write the screenshot script
Write this file to the **project root** (so it can resolve node_modules). It stays for the whole session and is deleted in Phase 4.

**`_uiux_screenshot.mjs`** (write to project root):
```js
import { chromium } from '@playwright/test';

const get = (flag) => {
  const i = process.argv.indexOf(flag);
  return i !== -1 ? process.argv[i + 1] : null;
};

const url    = get('--url');
const output = get('--output');
const width  = parseInt(get('--width')  ?? '1280');
const height = parseInt(get('--height') ?? '900');
const auth   = get('--auth');

if (!url || !output) { console.error('--url and --output required'); process.exit(1); }

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width, height },
  ...(auth ? { storageState: auth } : {}),
});
const page = await context.newPage();
await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
await page.screenshot({ path: output, fullPage: true });
await browser.close();
console.log('saved:', output);
```

**Usage — desktop:**
```bash
node _uiux_screenshot.mjs --url http://localhost:3000<ROUTE> --output /tmp/uiux-<name>-desktop.png
```
**Usage — mobile (375px):**
```bash
node _uiux_screenshot.mjs --url http://localhost:3000<ROUTE> --output /tmp/uiux-<name>-mobile.png --width 375 --height 812
```
**Usage — authenticated:**
```bash
node _uiux_screenshot.mjs --url http://localhost:3000<ROUTE> --output /tmp/uiux-<name>-desktop.png --auth /tmp/uiux-auth-state.json
```

After every screenshot: **use the `Read` tool on the image file to actually see it.** The image is the source of truth, not the code.

### 0d. Handle auth-protected screens
Check for auth middleware or providers (`middleware.ts`, `next-auth`, `clerk`, `supabase`, `lucia`, route guards).

If auth exists, write this to the **project root** and ask the user for test credentials (`TEST_EMAIL`, `TEST_PASSWORD`) and the post-login URL pattern (`SUCCESS_URL`, e.g. `**/dashboard**`):

**`_uiux_auth.mjs`** (write to project root):
```js
import { chromium } from '@playwright/test';

const { TEST_EMAIL, TEST_PASSWORD, LOGIN_URL, SUCCESS_URL } = process.env;
if (!TEST_EMAIL || !TEST_PASSWORD) {
  console.error('Set TEST_EMAIL and TEST_PASSWORD'); process.exit(1);
}

const browser = await chromium.launch();
const page    = await browser.newPage();
await page.goto(LOGIN_URL ?? 'http://localhost:3000/sign-in');
await page.fill('input[type="email"]',    TEST_EMAIL);
await page.fill('input[type="password"]', TEST_PASSWORD);
await page.click('button[type="submit"]');
await page.waitForURL(SUCCESS_URL ?? '**/dashboard**', { timeout: 15000 });
await page.context().storageState({ path: '/tmp/uiux-auth-state.json' });
await browser.close();
console.log('Auth session saved → /tmp/uiux-auth-state.json');
```

Run from the project root:
```bash
TEST_EMAIL=you@example.com TEST_PASSWORD=secret LOGIN_URL=http://localhost:3000/sign-in SUCCESS_URL="**/dashboard**" node _uiux_auth.mjs
```

If no test credentials are available: screenshot public screens now, mark protected screens **auth-blocked**, revisit them when credentials are provided.

### 0e. Find design tokens
Search for the token layer (`packages/tokens/`, `tokens.css`, `tailwind.config.ts`, CSS custom properties in a globals file). Note where spacing, colors, and font sizes are defined. **Fixes that apply globally go into tokens, not components.**

---

## Phase 1 — Screen Audit

Walk the codebase and list every distinct screen. For each:
- Route path + file path
- One-line description
- Auth-protected: yes/no
- Screenshot it (with `--auth` flag if protected), **Read the image**, rate: **broken / rough / decent / polished**

Discover screens from:
- App Router: every `app/**/page.tsx`
- Pages Router: `pages/**/*.tsx` (skip `_app`, `_document`, `api/`)
- Modal/drawer components
- Empty, error, loading, not-found states
- Auth flows (sign in, sign up, forgot password, verify email)
- Onboarding, settings, profile, billing pages

Present the full numbered list with quality ratings before continuing.

---

## Phase 2 — Priority Ranking

Score each screen:

| Factor | Points |
|--------|--------|
| Entry point / first impression | +3 |
| Revenue or conversion critical | +3 |
| Highest traffic / most-seen | +2 |
| Current quality is broken or rough | +2 |
| Auth-blocked (can't screenshot yet) | −1 |
| Power-user only | −1 |

Produce a ranked list (highest score = rank 1). Show reasoning for the top 5. **Ask the user to confirm or reorder before starting Phase 3.**

---

## Phase 3 — Recursive Redesign Loop

Work through screens in ranked order. Maximum **3 iterations per screen** — flag and advance if the checklist still fails after 3 passes. Track shared component fixes throughout (3f).

---

### 3a. Screenshot before
Take desktop and mobile screenshots. **Read both image files.** Describe in 2–3 sentences what you actually see — this is the baseline.

### 3b. Analyse
Read the page component, layout wrappers, child components, and CSS/Tailwind classes. Cross-reference everything against the screenshots — the screenshot overrides code assumptions. Check every dimension:

**Hierarchy** — One clear MIT per screen? Eye flows naturally?
**Color** — States derived with S+B rule? 60-30-10 applied? WCAG AA met?
**Typography** — Max 2 fonts? Heading/body ratio ≥1.75×? Weights correct?
**Spacing** — Padding rhythm consistent? Whitespace doubled from comfortable?
**Shadows & depth** — Light from sky? Shadow opacity matched to luminosity?
**Controls** — Adjacent to what they affect? Unnecessary dropdowns?
**Text on images** — Overlay / blur / floor-fade used?
**Alignment** — Alignment lines present? Icons/bullets hanging?
**Empty states** — Designed and instructive, not blank?
**Responsive** — Mobile 375px unbroken in screenshot?
**Accessibility** — Tap targets ≥44px, aria labels, color not the only signal?

### 3c. Issue list
Numbered, grouped by severity:
- **Critical** — broken, unreadable, accessibility failure
- **Major** — hierarchy wrong, color system violated, poor spacing
- **Minor** — polish, animation, edge cases

### 3d. Fix — tokens first, then components
Before touching any component, ask: **does this fix apply to ≥2 screens?**
- Yes → edit the token/config file. Do not hardcode it in the component.
- No → edit the component directly.

Apply all fixes, critical first. Apply rules automatically — no permission needed:
- Darker state: increase S + decrease B + shift hue toward 0°/120°/240°
- Lighter state: decrease S + increase B + shift hue toward 60°/180°/300°
- Neutral surfaces: brand hue whisper (~0.005 chroma), never pure gray
- Whitespace: double until it feels like too much — that is correct
- One MIT — only the page title gets all-out up-pop
- Font size: body ≥15px, labels ≥12px
- Shadow on light bg: 20–30% opacity. On dark bg: 40–50% opacity.
- Replace dropdowns (≤5 options) with segmented, toggle, stepper, or typeahead

### 3e. Wait for hot reload, then screenshot
After making edits, wait for the dev server to recompile:
```bash
sleep 3
```
Then take desktop and mobile screenshots. **Read both image files.** Compare visually against the `before` screenshots.

Answer from the images (not the code):
1. **MIT** — Is the most important element the first thing the eye lands on?
2. **Flow** — Does attention travel in the right order?
3. **Space** — Does the screen breathe, or is it cramped?
4. **Consistency** — Does this screen feel like the same product as the others?

If any answer is no: go back to **3b** (increment iteration counter, max 3).

### 3f. Shared component tracking
When a fix touches a component used across multiple screens:
```
SHARED FIX: <ComponentName> — affects screens: [list routes]
```
When reaching those screens later: skip re-fixing, but screenshot and verify the component renders correctly in that context.

### 3g. Pixel-perfect checklist
Every item verified from the **screenshot**, not the code:

- [ ] MIT immediately obvious when looking at the screenshot
- [ ] Color states derived with S+B rule (no raw opacity hacks)
- [ ] Neutral surfaces have brand hue whisper, not pure gray
- [ ] Body text ≥15px, labels ≥12px, heading/body ratio ≥1.75×
- [ ] Whitespace doubled — padding ≥ font-size on all sides
- [ ] Consistent spacing rhythm (4/8/16/24/32/48px)
- [ ] Shadow opacity matches background luminosity
- [ ] All controls adjacent to what they affect
- [ ] Tap targets ≥44px — verified on mobile screenshot
- [ ] WCAG AA contrast: 4.5:1 body, 3:1 headlines
- [ ] Empty states designed (not blank)
- [ ] No unnecessary dropdowns
- [ ] Icons match typeface stroke weight and corner radius
- [ ] Text on images uses overlay / text-box / blur / floor-fade
- [ ] Alignment lines consistent across the screen
- [ ] Mobile 375px: no overflow, no broken layout

Any fail → go back to **3d**, increment iteration. After iteration 3: flag and advance.

---

## Phase 4 — Cleanup & Progress Report

Delete the temp scripts from the project root:
```bash
rm -f _uiux_screenshot.mjs _uiux_auth.mjs
```

After each screen:
```
✓ Screen name (rank N, iteration K) — A critical + B major + C minor fixed
  Shared fixes: [list or none] | Flagged: [list or none]
```

After all screens, full summary table:

| Rank | Screen | Route | Issues Fixed | Iterations | State |
|------|--------|-------|-------------|------------|-------|
| 1    | ...    | ...   | ...         | ...        | ✓ polished / ⚠ review needed / 🔒 auth-blocked |

List all flagged and auth-blocked screens at the bottom with specific unresolved items.

---

## Rules

1. **Read every screenshot with the Read tool.** Never describe the UI from code alone. The image wins.
2. **Tokens before components.** Global fixes go in the token/config layer first.
3. **Shared components once.** Fix once, track affected screens, verify in context.
4. **Max 3 iterations per screen.** Flag and move on. Don't get stuck.
5. **Apply design rules automatically.** No permission needed for color, spacing, or typography.
6. **Preserve functionality.** Never change logic, routing, data fetching, or accessibility semantics.
7. **Mobile first.** Every fix must pass at 375px before it is done.
8. **Auth-blocked screens.** Screenshot what you can now. Revisit when credentials are provided.
9. **One screen at a time.** Complete checklist and all iterations before advancing.
10. **Report progress.** The user always knows which screen is active and how many remain.

---

## Supported project types

Next.js (App Router or Pages), React + Vite, SvelteKit, Nuxt, Astro, plain HTML/CSS. Adjust file discovery for the project structure found.

See [PRINCIPLES.md](PRINCIPLES.md) for the full design knowledge base quick reference.
