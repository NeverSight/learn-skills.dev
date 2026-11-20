---
name: tokens
description: Design token audit and enforcement skill. Finds every hardcoded color, spacing value, shadow, border radius, font size, and z-index in the codebase, maps them to an existing or proposed token system, then replaces hardcoded values with tokens — making the design system maintainable, themeable, and dark-mode-ready. Use when user wants to set up a token system, enforce design consistency, prepare for dark mode, or invokes /tokens.
---

# /tokens — Design Token System

Audits every hardcoded design value in the codebase, builds or enforces a three-layer token system (primitives → semantic → component), and replaces hardcoded values with tokens throughout.

Token architecture and naming conventions: [SYSTEMS.md](SYSTEMS.md)

If a `DESIGN-BRIEF.md` exists in the project root: read it before starting. The brief's **Color System** and **Typography** fields give you the exact starting point for primitive tokens — use those hex values and font names directly rather than deriving them from scratch.

---

## Phase 0 — Environment Setup

### 0a. Find source root
```bash
find . -type d -name "src" \
  -not -path "*/node_modules/*" \
  -not -path "*/.next/*" \
  -not -path "*/dist/*" \
  -not -path "*/.turbo/*" \
  | head -1
```
If no `src/`: `find . -type d -name "app" -not -path "*/node_modules/*" -not -path "*/.next/*" | head -1`

Use the result as `<SRC>` throughout.

### 0b. Detect CSS-in-JS
```bash
grep -r "styled-components\|@emotion\|@stitches\|vanilla-extract\|linaria" package.json packages/*/package.json apps/*/package.json 2>/dev/null | head -5
```
If found, the color/spacing greps in Phase 1 must also scan `.ts` files and template literals — the Phase 1 commands include these where needed. Note which library is in use.

### 0c. Detect the existing token system
Run all of these — note which ones return results:

```bash
# CSS custom properties (most common)
find . -name "globals.css" -o -name "variables.css" -o -name "tokens.css" | grep -v node_modules

# Tailwind config
find . -name "tailwind.config.*" -not -path "*/node_modules/*"

# Style Dictionary / tokens.json
find . -name "tokens.json" -o -name "design-tokens.json" | grep -v node_modules
find . -type d -name "tokens" -not -path "*/node_modules/*"

# shadcn/ui pattern (CSS vars in globals.css under :root)
grep -rn ":root" . --include="*.css" -l | grep -v node_modules | head -5

# Existing token usage (CSS vars already in use)
grep -rn "var(--" "$SRC" --include="*.tsx" --include="*.css" | head -10
```

Map the result to one of these token homes — all fixes go here:
- **CSS custom properties** → `globals.css` `:root` block
- **Tailwind `theme.extend`** → `tailwind.config.ts`
- **Style Dictionary** → `tokens/` directory JSON files
- **None** → create `globals.css` with `:root` block (see SYSTEMS.md)

### 0d. Snapshot the current token set
Read the token home file(s) found in 0b. List every existing token name and value. This is the baseline — new tokens must not conflict with or duplicate these.

### 0e. Check / start dev server (for visual verification)
```bash
curl -s --max-time 2 -o /dev/null -w "%{http_code}" http://localhost:3000
```
If not `200`, start the dev command and wait:
```bash
until curl -s --max-time 2 http://localhost:3000 > /dev/null 2>&1; do sleep 1; done && echo "ready"
```

### 0f. Write the screenshot script
Write to the **project root** (needs node_modules). Deleted in Phase 4.

**`_tokens_screenshot.mjs`:**
```js
import { chromium } from '@playwright/test';
import { mkdirSync } from 'fs';

const get = (f) => { const i = process.argv.indexOf(f); return i !== -1 ? process.argv[i+1] : null; };
const url    = get('--url');
const output = get('--output') ?? '/tmp/tokens-screenshot.png';
const width  = parseInt(get('--width')  ?? '1280');
const height = parseInt(get('--height') ?? '900');
const auth   = get('--auth');

if (!url) { console.error('--url required'); process.exit(1); }
mkdirSync('/tmp/tokens', { recursive: true });

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

**After every screenshot: use the `Read` tool on the image.**

### 0g. Handle auth-protected screens
```bash
ls /tmp/uiux-auth-state.json /tmp/animate-auth-state.json /tmp/copy-auth-state.json /tmp/a11y-auth-state.json 2>/dev/null | head -1
```
If found, pass `--auth <path>` to all screenshot calls for protected routes.

---

## Phase 1 — Token Audit

### 1a. Find all hardcoded colors
```bash
SRC=<your source root>

# Hex colors in TSX/JSX (inline styles, arbitrary Tailwind values)
echo "=== Hex colors in TSX ===" && \
grep -rn "#[0-9a-fA-F]\{3,8\}" "$SRC" --include="*.tsx" --include="*.jsx" \
  | grep -v "//.*#[0-9a-fA-F]" | grep -v "\.md"

# Hex colors in CSS
echo "=== Hex colors in CSS ===" && \
grep -rn "#[0-9a-fA-F]\{3,8\}" "$SRC" --include="*.css" --include="*.scss" \
  | grep -v "^.*:.*var(--"

# rgb/hsl inline values
echo "=== RGB/HSL values ===" && \
grep -rn "rgba\?\|hsla\?" "$SRC" --include="*.tsx" --include="*.css" | grep -v "var(--"

# Arbitrary Tailwind color values (hex)
echo "=== Arbitrary Tailwind colors (hex) ===" && \
grep -rn "\(bg\|text\|border\|ring\|shadow\|fill\|stroke\)-\[#" "$SRC" --include="*.tsx"

# Named Tailwind palette colors that should be semantic tokens
# e.g. bg-blue-500 should become bg-primary if blue-500 is the primary color
echo "=== Named Tailwind palette colors ===" && \
grep -rn "\(bg\|text\|border\|ring\|fill\|stroke\)-\(slate\|gray\|zinc\|neutral\|stone\|red\|orange\|amber\|yellow\|lime\|green\|emerald\|teal\|cyan\|sky\|blue\|indigo\|violet\|purple\|fuchsia\|pink\|rose\)-[0-9]\{2,3\}" "$SRC" --include="*.tsx" \
  | grep -v "hover:\|focus:\|dark:\|disabled:" | head -40
# Note: filter hover/focus/dark variants — those are less likely to be primary brand usage
# High-frequency named colors (>5 occurrences) are strong tokenization candidates
```

**If CSS-in-JS detected (styled-components / emotion):** also run:
```bash
# Hex colors in template literals
grep -rn "#[0-9a-fA-F]\{3,8\}" "$SRC" --include="*.ts" --include="*.tsx" \
  | grep "styled\.\|css\`\|createGlobalStyle\|keyframes" | grep -v "//.*#"

# CSS property values inside template literals
grep -rn "color:\s*#\|background:\s*#\|border.*:\s*#" "$SRC" --include="*.ts" --include="*.tsx"
```

### 1b. Find all hardcoded spacing
```bash
# Off-grid pixel values in CSS (not on 4px scale)
echo "=== Off-grid spacing in CSS ===" && \
grep -rn "\b[0-9]*[13579]\b\s*px\|[0-9]\+\.\s*[0-9]\+\s*px" "$SRC" --include="*.css" \
  | grep -v "border\|outline\|shadow\|translate"

# Arbitrary Tailwind spacing values
echo "=== Arbitrary Tailwind spacing ===" && \
grep -rn "\(p\|m\|gap\|space\|w\|h\|inset\|top\|left\|right\|bottom\)-\[[0-9]" "$SRC" --include="*.tsx"

# Inline style pixel values
echo "=== Inline style px values ===" && \
grep -rn "style={{" "$SRC" --include="*.tsx" | grep "[0-9]px\|[0-9]rem" | head -20
```

### 1c. Find all hardcoded typography values
```bash
# Font sizes in CSS not from scale
echo "=== Hardcoded font sizes ===" && \
grep -rn "font-size:" "$SRC" --include="*.css" | grep -v "var(--"

# Arbitrary Tailwind font sizes
echo "=== Arbitrary Tailwind font sizes ===" && \
grep -rn "text-\[[0-9]" "$SRC" --include="*.tsx"

# Font weights not from scale
echo "=== Hardcoded font weights ===" && \
grep -rn "font-weight:\s*[0-9]" "$SRC" --include="*.css" | grep -v "var(--"

# Line heights
echo "=== Hardcoded line heights ===" && \
grep -rn "line-height:\s*[0-9]" "$SRC" --include="*.css" | grep -v "var(--"
```

### 1d. Find all hardcoded shadows, radii, and z-indices
```bash
# Box shadows not from token
echo "=== Hardcoded shadows ===" && \
grep -rn "box-shadow:" "$SRC" --include="*.css" | grep -v "var(--" && \
grep -rn "shadow-\[" "$SRC" --include="*.tsx"

# Border radii not from token
echo "=== Hardcoded border radii ===" && \
grep -rn "border-radius:" "$SRC" --include="*.css" | grep -v "var(--" && \
grep -rn "rounded-\[[0-9]" "$SRC" --include="*.tsx"

# Magic z-index numbers
echo "=== Magic z-index ===" && \
grep -rn "z-index:\s*[0-9]\|z-\[[0-9]" "$SRC" --include="*.css" --include="*.tsx"
```

### 1e. Find duplicate and inconsistent values
```bash
# Same color used with different names (group by hex value to find duplicates)
grep -rh "#[0-9a-fA-F]\{3,8\}" "$SRC" --include="*.tsx" --include="*.css" \
  | grep -oE "#[0-9a-fA-F]{3,8}" | sort | uniq -c | sort -rn | head -20
```

High-count values = the most-used hardcoded colors. These are highest priority for tokenization.

### 1f. Screenshot every major screen (before state)
Take desktop and mobile for each screen — token changes to spacing and typography can break mobile layouts that look fine at 1280px.

```bash
node _tokens_screenshot.mjs --url http://localhost:3000 --output /tmp/tokens/home-before-desktop.png
node _tokens_screenshot.mjs --url http://localhost:3000 --output /tmp/tokens/home-before-mobile.png --width 375 --height 812
```
Take 3–5 of the most visually distinct screens. **Read every image.** These are your before-state baseline.

Present the full audit findings grouped by category before continuing.

---

## Phase 2 — Token Map

Before writing any code, build a token map — a translation table from every hardcoded value to its proposed token name.

**Format:**
```
Hardcoded value | Occurrences | Proposed token name | Layer
#3b82f6         | 23          | --color-primary      | semantic
#1d4ed8         | 8           | --color-primary-dark  | semantic
#f9fafb         | 31          | --color-surface       | semantic
13px            | 4           | --spacing-3-5         | primitive
```

**Rules for naming (from SYSTEMS.md):**
- Primitive tokens: `--color-{hue}-{shade}`, `--space-{n}`, `--radius-{size}`
- Semantic tokens: `--color-primary`, `--color-surface`, `--color-text`, `--color-border`
- Component tokens: `--button-bg`, `--card-shadow` (only when component-specific)
- Never name by visual appearance: `--blue` or `--dark-gray` → use semantic name
- Semantic names survive color changes: `--color-primary` stays right when brand changes from blue to green

Group by token layer:
1. **New primitive tokens** — raw values not already in the system
2. **New semantic tokens** — meaning-based aliases to primitives
3. **Existing tokens to use** — values that map to already-defined tokens

Ask user to confirm the token map before starting Phase 3.

---

## Phase 3 — Recursive Token Loop

Work category by category: colors → spacing → typography → shadows → radii → z-index.
Maximum **3 iterations per category**.

### 3a. Define new tokens
Add all new primitive and semantic tokens to the token home file before replacing any usage.

**CSS custom properties pattern:**
```css
/* In globals.css */
:root {
  /* Primitives */
  --color-blue-500: #3b82f6;
  --color-blue-700: #1d4ed8;
  --space-1: 4px;
  --space-2: 8px;

  /* Semantic */
  --color-primary:      var(--color-blue-500);
  --color-primary-dark: var(--color-blue-700);
  --color-surface:      #f9fafb;
  --color-text:         #111827;
  --color-border:       #e5e7eb;
}

/* Dark mode — same semantic names, different values */
.dark {
  --color-primary:  var(--color-blue-400);
  --color-surface:  #111827;
  --color-text:     #f9fafb;
  --color-border:   #374151;
}
```

**Tailwind pattern:**
```ts
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary:  'var(--color-primary)',
        surface:  'var(--color-surface)',
        border:   'var(--color-border)',
      },
      spacing: {
        '3.5': 'var(--space-3-5)',
      },
    },
  },
}
```

### 3b. Replace hardcoded values in components
Work file by file through the highest-occurrence values first. For each:

1. Read the file
2. Replace the hardcoded value with the token
3. Never change logic, layout, or component structure — only the value

**CSS replacement:**
```css
/* Before */
color: #3b82f6;

/* After */
color: var(--color-primary);
```

**Tailwind class replacement:**
```tsx
/* Before */
<div className="bg-[#3b82f6] text-[#111827]">

/* After */
<div className="bg-primary text-text">
```

**Inline style replacement (last resort — prefer moving to CSS/Tailwind):**
```tsx
/* Before */
style={{ backgroundColor: '#3b82f6' }}

/* After — move to CSS class if possible */
className="bg-primary"

/* Or if dynamic: */
style={{ backgroundColor: 'var(--color-primary)' }}
```

### 3c. Screenshot after each category
```bash
sleep 3  # hot reload
node _tokens_screenshot.mjs --url http://localhost:3000 --output /tmp/tokens/home-after-<category>-desktop.png
node _tokens_screenshot.mjs --url http://localhost:3000 --output /tmp/tokens/home-after-<category>-mobile.png --width 375 --height 812
```
**Read both images.** Compare against the before screenshots at both viewports.

The UI should look **identical** at both sizes. If anything changed:
- Wrong color → token value is wrong, fix the token definition
- Layout shift on mobile → a spacing/size token resolves to a different value than the hardcoded one, fix the token value

### 3d. Token checklist
Before advancing to the next category:

- [ ] All values in this category replaced with tokens
- [ ] No new hardcoded values introduced during replacement
- [ ] Before/after desktop screenshots are visually identical
- [ ] Before/after mobile screenshots (375px) are visually identical — spacing/typography tokens don't shift layout
- [ ] Token names follow the primitive → semantic hierarchy
- [ ] Dark mode block defines overrides for all semantic tokens (if dark mode exists)
- [ ] No two tokens have the same value and different semantic meaning (consolidate duplicates)
- [ ] No token name describes its appearance (`--blue`) — only its role (`--color-primary`)

Any fail → go back to 3b. After iteration 3: flag and advance.

---

## Phase 4 — Cleanup & Report

Delete temp scripts:
```bash
rm -f _tokens_screenshot.mjs
```

After each category:
```
✓ Colors (iteration 1) — 47 hardcoded values → 8 tokens
✓ Spacing (iteration 2) — 12 hardcoded values → 4 tokens
```

Final summary table:

| Category | Hardcoded Before | Tokens Created | Values Replaced | Iterations | State |
|----------|-----------------|---------------|----------------|------------|-------|
| Colors   | ...             | ...           | ...            | ...        | ✓ / ⚠ |
| Spacing  | ...             | ...           | ...            | ...        | ✓ / ⚠ |
| Typography | ...           | ...           | ...            | ...        | ✓ / ⚠ |
| Shadows  | ...             | ...           | ...            | ...        | ✓ / ⚠ |
| Radii    | ...             | ...           | ...            | ...        | ✓ / ⚠ |
| Z-index  | ...             | ...           | ...            | ...        | ✓ / ⚠ |

**Token inventory** — all tokens defined, their values, and number of usages.

List all flagged hardcoded values that couldn't be resolved, with the reason.

---

## Rules

1. **Define before you replace.** Token must exist in the token home before any component references it.
2. **Primitive before semantic.** Raw value first, semantic alias second, component token only when necessary.
3. **Name by role, never by appearance.** `--color-primary` survives a rebrand. `--color-blue` doesn't.
4. **Screenshots are the regression test.** Before/after must be visually identical. If they differ, the token value is wrong.
5. **Dark mode is the test for a good semantic layer.** If swapping `.dark` changes colors correctly with no component edits, the tokens are right.
6. **One token per meaning.** Two tokens with the same value and same meaning → merge them.
7. **Don't tokenize everything.** `border: 1px solid` — the `1px` doesn't need a token. Focus on values that change across themes or appear in multiple places.
8. **Max 3 iterations per category.** Flag and move on.
9. **Never change logic.** Only the design value — not the condition, component structure, or functionality.

---

See [SYSTEMS.md](SYSTEMS.md) for token architecture, naming conventions, and complete code patterns.
