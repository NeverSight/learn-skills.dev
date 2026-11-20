---
name: copy
description: Master UI copywriting skill that audits every user-facing string in the project — CTAs, error messages, empty states, placeholders, loading messages, headings, tooltips, confirmations — and rewrites them to be specific, benefit-first, and actionable. Works screen by screen in priority order with visual verification. Use when user wants to improve UI copy, fix button labels, write empty states, improve error messages, or invokes /copy.
---

# /copy — Master UI Copywriting

Audits every word the user sees and rewrites it to be clear, specific, and benefit-first. Works screen by screen, from highest to lowest priority, verifying every change visually before advancing.

Before starting: read `~/.claude/skills/ui-design-principles/SKILL.md` — writing rules (expose benefit not action, strongest statement first, $1000 per deleted word) are in there and apply throughout.

Full copy rules by category: [PRINCIPLES.md](PRINCIPLES.md)

---

## Phase 0 — Environment Setup

### 0a. Check / start dev server
```bash
curl -s --max-time 2 -o /dev/null -w "%{http_code}" http://localhost:3000
```
If not `200`, find and start the dev command, then wait:
```bash
until curl -s --max-time 2 http://localhost:3000 > /dev/null 2>&1; do sleep 1; done && echo "ready"
```

### 0b. Find source root
```bash
find . -type d -name "src" \
  -not -path "*/node_modules/*" \
  -not -path "*/.next/*" \
  -not -path "*/dist/*" \
  -not -path "*/.turbo/*" \
  | head -1
```
If no `src/` exists: `find . -type d -name "app" -not -path "*/node_modules/*" -not -path "*/.next/*" | head -1`

Use the result as `<SRC>` throughout.

### 0b-i. Detect i18n
```bash
grep -r "i18next\|next-intl\|react-i18next\|@lingui\|formatjs\|next-translate" package.json packages/*/package.json apps/*/package.json 2>/dev/null | head -5
```
If a translation library is found:
- Find the message files: `find . -name "*.json" -path "*/locales/*" -not -path "*/node_modules/*" | head -10`
- **All copy fixes go into the message files**, not hardcoded in component files.
- Note the library and message file paths — reference them throughout Phase 3.

### 0c. Write the screenshot script
Write to the **project root** (needs node_modules). Deleted in Phase 4.

**`_copy_screenshot.mjs`:**
```js
import { chromium } from '@playwright/test';
import { mkdirSync } from 'fs';

const get = (f) => { const i = process.argv.indexOf(f); return i !== -1 ? process.argv[i+1] : null; };

const url    = get('--url');
const output = get('--output') ?? '/tmp/copy-screenshot.png';
const width  = parseInt(get('--width')  ?? '1280');
const height = parseInt(get('--height') ?? '900');
const auth   = get('--auth');

if (!url) { console.error('--url required'); process.exit(1); }

mkdirSync('/tmp/copy-screens', { recursive: true });

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width, height },
  ...(auth ? { storageState: auth } : {}),
});
const page = await context.newPage();
try {
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
} catch {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
}
await page.screenshot({ path: output, fullPage: true });
await browser.close();
console.log('saved:', output);
```

Usage:
```bash
node _copy_screenshot.mjs --url http://localhost:3000/dashboard --output /tmp/copy-dashboard.png
node _copy_screenshot.mjs --url http://localhost:3000/settings  --output /tmp/copy-settings-mobile.png --width 375 --height 812
```

**After every screenshot: use the `Read` tool on the image file.**

### 0d. Handle auth-protected screens
Check for an existing auth state from a previous skill run:
```bash
ls /tmp/uiux-auth-state.json /tmp/animate-auth-state.json 2>/dev/null | head -1
```
If found, pass `--auth <path>` to all screenshot calls for protected routes.

If not found and protected screens exist, write `_copy_auth.mjs` to the project root:
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
await page.context().storageState({ path: '/tmp/copy-auth-state.json' });
await browser.close();
console.log('saved → /tmp/copy-auth-state.json');
```
```bash
TEST_EMAIL=you@example.com TEST_PASSWORD=secret node _copy_auth.mjs
```

---

## Phase 1 — Copy Audit

### 1a. Find all screens
Same discovery as `/uiux` — every `page.tsx` in App Router, every page in Pages Router, modals, auth flows, settings, onboarding. List each with its route.

### 1b. Read and extract copy for each screen
For each screen, **read the file** (and its key child components) and extract every user-facing string, grouped by category:

| Category | What to look for |
|----------|-----------------|
| **CTAs** | Button labels, link text, submit text |
| **Headings** | h1, h2, h3, page titles, section titles |
| **Errors** | Error messages, validation text, failed states |
| **Empty states** | "No results", "Nothing here", blank state text |
| **Placeholders** | Input placeholder attributes |
| **Loading** | Loading text, skeleton labels, progress messages |
| **Tooltips** | title attributes, tooltip content, aria-labels, aria-describedby, aria-placeholder |
| **Confirmations** | Dialog text, "Are you sure?", destructive action warnings |
| **Microcopy** | Helper text, hints, descriptions under fields |
| **Marketing** | Hero headlines, subheadlines, feature descriptions |

Rate each string:
- **Bad** — generic, vague, action-not-benefit, or missing entirely
- **Weak** — technically correct but could be stronger
- **Good** — specific, benefit-first, clear — skip

### 1c. Screenshot each screen
Take a desktop screenshot of every screen. **Read every image.** Note where copy looks too long, truncated, or misaligned after rewriting (copy changes affect layout).

**Also scan for hidden copy in accessibility attributes:**
```bash
grep -rn "aria-label\|aria-description\|aria-placeholder\|title=" "$SRC" --include="*.tsx" --include="*.jsx" | grep -v "node_modules"
```
These strings are read by screen readers but invisible in the UI — they must follow the same copy rules.

Present the full audit grouped by screen before continuing.

---

## Phase 2 — Priority Ranking

Score each screen:

| Factor | Points |
|--------|--------|
| Entry point / first impression (landing, sign-up, onboarding) | +3 |
| Revenue / conversion critical (pricing, checkout, CTA) | +3 |
| Has **Bad** copy (generic, missing, or actively misleading) | +3 |
| High traffic / seen on every visit | +2 |
| Has **Weak** copy (improvable but not broken) | +1 |
| Admin / power-user only | −1 |

Rank highest to lowest. Ask user to confirm before starting Phase 3.

---

## Phase 3 — Recursive Copy Loop

Work through screens in ranked order. Maximum **3 iterations per screen**.

### 3a. Screenshot before
Take desktop and mobile screenshots. **Read both.** Describe the copy problems you can see in context — not just in the code.

```bash
node _copy_screenshot.mjs --url http://localhost:3000<ROUTE> --output /tmp/copy-before-<name>-desktop.png
node _copy_screenshot.mjs --url http://localhost:3000<ROUTE> --output /tmp/copy-before-<name>-mobile.png --width 375 --height 812
```

### 3b. Analyse
Read the screen's files. For each string, apply the rules from [PRINCIPLES.md](PRINCIPLES.md). Note every issue:
- **Critical** — actively wrong (misleading, broken error message, inaccessible label)
- **Major** — generic CTA, vague error, blank empty state, label-as-placeholder
- **Minor** — could be shorter, stronger, or more specific

### 3c. Rewrite
Apply all fixes, starting with critical. Rules from PRINCIPLES.md applied automatically — no permission needed:

- CTAs: verb-first + benefit ("Start Free Trial" not "Submit")
- Errors: what failed + what to do ("Email already in use — try signing in instead")
- Empty states: what's possible + a CTA ("No projects yet — create your first one")
- Placeholders: real example ("you@company.com" not "Email address")
- Loading: what is happening ("Generating your report…" not "Loading…")
- Confirmations: name the thing + consequence ("Delete 'Q4 Report'? This can't be undone.")
- Headings: strongest claim first, cut every filler word
- Microcopy: one sentence max, conversational, no jargon

**Length discipline:** after rewriting, check that no string is longer than necessary. Cut every word that isn't pulling weight. If the original was 8 words, the rewrite should be 5 or fewer.

**Layout impact:** if a rewrite is significantly longer than the original, note it — it may break the layout. Prefer shorter rewrites that fit the existing space.

### 3d. Screenshot after
```bash
sleep 3  # hot reload
node _copy_screenshot.mjs --url http://localhost:3000<ROUTE> --output /tmp/copy-after-<name>-desktop.png
node _copy_screenshot.mjs --url http://localhost:3000<ROUTE> --output /tmp/copy-after-<name>-mobile.png --width 375 --height 812
```
**Read both images.** Check:
1. Does the new copy fit without truncation or overflow — on both desktop AND mobile?
2. Does it read naturally in context?
3. Is the hierarchy still clear (heading → subtext → CTA)?
4. Does the tone match the rest of the product?

If any answer is no: go back to 3c (increment iteration, max 3).

### 3e. Copy checklist
Before advancing to the next screen:

- [ ] Every CTA is verb-first and exposes a benefit
- [ ] No button says "Submit", "OK", "Click here", or "Continue" without context
- [ ] Every error message says what failed AND what to do next
- [ ] No error says "Something went wrong" or "An error occurred"
- [ ] Every empty state explains what goes here AND has a CTA
- [ ] No placeholder is just the field label repeated
- [ ] Every placeholder shows a real example
- [ ] Every loading message says what is happening specifically
- [ ] Every confirmation names the thing being acted on and the consequence
- [ ] Every heading is the strongest true statement — no filler words
- [ ] No microcopy exceeds one sentence
- [ ] All copy fits in its container without truncation (verified in desktop screenshot)
- [ ] All copy fits at 375px mobile — no wrapping that breaks the layout (verified in mobile screenshot)
- [ ] All aria-labels and title attributes follow the same copy rules
- [ ] If i18n is detected: all changes are in message files, not hardcoded
- [ ] Tone is consistent with the rest of the product on this screen

Any fail → go back to 3c. After iteration 3: flag and advance.

---

## Phase 4 — Cleanup & Report

Delete temp scripts:
```bash
rm -f _copy_screenshot.mjs _copy_auth.mjs
```

After each screen:
```
✓ Screen name (rank N, iteration K) — A critical + B major + C minor fixed
```

Final summary table:

| Rank | Screen | Route | Strings Fixed | Iterations | State |
|------|--------|-------|--------------|------------|-------|
| 1    | ...    | ...   | ...          | ...        | ✓ / ⚠ |

List all flagged strings at the bottom with the specific issue that couldn't be resolved.

---

## Rules

1. **Read every screenshot.** Copy that fits perfectly in code can truncate or overflow in the browser. The image wins.
2. **Shorter is always better.** If two rewrites are equally clear, pick the shorter one.
3. **Benefit before action.** Every CTA should answer "what do I get?" not "what will I do?"
4. **Specific beats generic.** "Delete 'March Report'?" beats "Are you sure?". "Email already in use" beats "Invalid input".
5. **Match the tone.** Don't make one screen sound like a startup and another like an enterprise tool.
6. **Layout first.** If a rewrite breaks the layout, shorten it — don't ask the developer to change the layout for copy.
7. **Max 3 iterations per screen.** Flag and move on.
8. **Never change logic or functionality.** Only strings the user sees.

---

See [PRINCIPLES.md](PRINCIPLES.md) for rules and good/bad examples by copy category.
