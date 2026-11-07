---
name: cc-design-html-prototyping
description: High-fidelity HTML design and prototype creation skill for AI coding agents — slide decks, interactive prototypes, landing pages, UI mockups, animations, and brand style cloning.
triggers:
  - design a landing page for my product
  - create a slide deck or pitch deck
  - build an interactive prototype
  - explore visual directions for the UI
  - clone a brand style like Stripe or Notion
  - make a UI mockup or design exploration
  - animate a component or motion study
  - design screens for mobile or web
---

# CC Design

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

CC Design is a structured design workflow skill for AI coding agents. It enables Claude Code, Codex, and compatible agents to act as expert product designers — producing high-fidelity HTML artifacts including slide decks, interactive prototypes, landing pages, UI mockups, and animated motion studies. It supports brand style cloning from 68+ design systems and uses Playwright for visual verification.

---

## Installation

Clone into the Claude Code skills directory:

```bash
git clone https://github.com/ZeroZ-lab/cc-design.git ~/.claude/skills/cc-design
```

Or as a submodule in an existing skill collection:

```bash
git submodule add https://github.com/ZeroZ-lab/cc-design.git skills/cc-design
```

Install export script dependencies (for PPTX, PDF, and inline HTML export):

```bash
cd ~/.claude/skills/cc-design/scripts && npm install && cd -
npx playwright install chromium
```

---

## Project Structure

```
cc-design/
├── SKILL.md                      # Core skill definition (always loaded)
├── EXAMPLES.md                   # Brand cloning and advanced usage examples
├── agents/
│   └── openai.yaml               # Codex-compatible interface config
├── references/
│   ├── getdesign-loader.md       # Brand style loading from getdesign.md
│   ├── platform-tools.md         # Claude Code + Playwright tool reference
│   ├── react-babel-setup.md      # React/Babel pinned versions and scope rules
│   ├── starter-components.md     # Starter component catalog
│   └── tweaks-system.md          # In-page tweak controls
├── templates/
│   ├── deck_stage.js             # Slide presentation stage
│   ├── design_canvas.jsx         # Side-by-side option grid
│   ├── ios_frame.jsx             # iPhone device frame
│   ├── android_frame.jsx         # Android device frame
│   ├── macos_window.jsx          # macOS window chrome
│   ├── browser_window.jsx        # Browser window chrome
│   └── animations.jsx            # Timeline animation engine
└── scripts/
    ├── package.json
    ├── gen_pptx.js               # HTML → PPTX export
    ├── super_inline_html.js      # HTML + assets → single file
    └── open_for_print.js         # HTML → PDF via Playwright
```

---

## Design Workflow

The skill follows a six-phase loop for every design request:

```
Understand → Explore → Plan → Build → Verify → Deliver
```

1. **Understand** — Clarify intent, audience, constraints, and existing brand context before writing any code.
2. **Explore** — Read existing design tokens, component libraries, or product code in the repo. Load brand systems from `getdesign.md` when a brand name is mentioned.
3. **Plan** — Write a brief todo list of components, layout decisions, and variation axes.
4. **Build** — Produce HTML + inline React/Babel components. Use pinned CDN versions (see below).
5. **Verify** — Use Playwright to take a screenshot and check the browser console for errors.
6. **Deliver** — Write the final file, offer export options (PPTX, PDF, single-file HTML).

---

## Core Principles

- **Context-first design** — Never design from scratch when existing brand systems, component libraries, or product code is available. Scan the repo and load relevant context before creating new visual directions.
- **Progressive disclosure** — The main `SKILL.md` stays concise. Technical references in `references/` are loaded on demand to keep context window usage minimal.
- **3+ variations** — Always generate at least three design directions across layout, visual intensity, interaction model, or motion axes.

---

## Key Capabilities

| Category | Details |
|---|---|
| Output formats | Interactive prototypes, slide decks, landing pages, UI mockups, animated motion studies, design explorations |
| Brand style cloning | 68+ brands via [getdesign.md](https://getdesign.md): Stripe, Vercel, Notion, Linear, Apple, Tesla, Figma, GitHub, Airbnb, and more |
| Design systems | Auto-discovers and reuses existing tokens, typography, spacing, and color patterns from the project |
| Variations | Generates 3+ directions across layout, interaction, visual intensity, and motion axes |
| Prototyping | React + Babel inline JSX with pinned CDN versions, component scope management |
| Tweaks system | Self-contained in-page design controls with real-time preview and `localStorage` persistence |
| Verification | Playwright screenshot + console error check after every build step |
| Export | PPTX via `gen_pptx.js`, PDF via `open_for_print.js`, single-file via `super_inline_html.js` |

---

## React + Babel Setup (Pinned Versions)

All prototypes use pinned CDN versions to guarantee reproducibility:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Prototype</title>
  <script src="https://unpkg.com/react@18.2.0/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18.2.0/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone@7.23.5/babel.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    const { useState, useEffect, useRef } = React;

    function App() {
      return (
        <div className="min-h-screen bg-white flex items-center justify-center">
          <h1 className="text-4xl font-bold text-gray-900">Hello, CC Design</h1>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
```

**Rules for inline JSX:**
- Always use `type="text/babel"` on script tags containing JSX.
- Destructure hooks from `React` at the top of the script block — do not use `React.useState` inline.
- Keep all components in a single script block unless explicitly splitting files.
- Never use ES module `import` syntax — CDN UMD builds expose globals only.

---

## Brand Style Cloning

Mention a brand name in the prompt to trigger automatic loading of its design system from [getdesign.md](https://getdesign.md):

```
"Create a pricing page with Stripe's aesthetic"
"Notion-style kanban board"
"Mix Vercel's minimalism with Linear's purple accents"
"Show me this dashboard in Apple style vs Tesla style"
```

The agent will:
1. Fetch the brand's design tokens (colors, typography, spacing, radius, shadow, motion).
2. Apply them as CSS custom properties on `:root`.
3. Reference them consistently throughout the component tree.

Example of brand tokens applied as CSS custom properties:

```html
<style>
  :root {
    /* Stripe-inspired tokens */
    --color-primary: #635bff;
    --color-primary-dark: #4b44cc;
    --color-surface: #ffffff;
    --color-surface-alt: #f6f9fc;
    --color-text: #0a2540;
    --color-text-muted: #425466;
    --color-border: #e3e8ee;
    --radius-md: 8px;
    --radius-lg: 12px;
    --font-sans: 'Inter', system-ui, sans-serif;
    --shadow-card: 0 4px 24px rgba(10,37,64,0.08);
  }
</style>
```

---

## Export Scripts

### HTML → PPTX

```bash
node ~/.claude/skills/cc-design/scripts/gen_pptx.js \
  --input ./output/deck.html \
  --output ./output/deck.pptx
```

### HTML → PDF

```bash
node ~/.claude/skills/cc-design/scripts/open_for_print.js \
  --input ./output/prototype.html \
  --output ./output/prototype.pdf
```

### HTML → Single Inline File

Embeds all linked CSS, JS, and images as base64 data URIs:

```bash
node ~/.claude/skills/cc-design/scripts/super_inline_html.js \
  --input ./output/prototype.html \
  --output ./output/prototype.standalone.html
```

---

## Playwright Verification

After every build step, take a screenshot and check for console errors:

```javascript
// Playwright verification snippet (used by the agent internally)
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });

  await page.goto(`file://${process.cwd()}/output/prototype.html`);
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: 'output/preview.png', fullPage: true });

  if (errors.length > 0) {
    console.error('Console errors detected:', errors);
    process.exit(1);
  }

  console.log('Screenshot saved to output/preview.png — no console errors.');
  await browser.close();
})();
```

Run manually if needed:

```bash
node verify.js
```

---

## Tweaks System

The tweaks system adds self-contained in-page design controls to any prototype. Controls persist via `localStorage`. Include at the bottom of any HTML file:

```html
<script type="text/babel">
  function TweaksPanel({ tweaks, onChange }) {
    const [open, setOpen] = React.useState(false);
    return (
      <div style={{ position: 'fixed', bottom: 16, right: 16, zIndex: 9999 }}>
        <button
          onClick={() => setOpen(o => !o)}
          style={{ background: '#635bff', color: '#fff', border: 'none',
                   borderRadius: 8, padding: '8px 16px', cursor: 'pointer' }}
        >
          {open ? 'Close' : '⚙ Tweaks'}
        </button>
        {open && (
          <div style={{ background: '#fff', border: '1px solid #e3e8ee',
                        borderRadius: 12, padding: 16, marginTop: 8,
                        boxShadow: '0 4px 24px rgba(0,0,0,0.12)', minWidth: 240 }}>
            {tweaks.map(t => (
              <label key={t.key} style={{ display: 'block', marginBottom: 12 }}>
                <span style={{ fontSize: 13, color: '#425466' }}>{t.label}</span>
                <input
                  type={t.type || 'range'}
                  min={t.min} max={t.max} step={t.step}
                  value={t.value}
                  onChange={e => onChange(t.key, e.target.value)}
                  style={{ display: 'block', width: '100%', marginTop: 4 }}
                />
              </label>
            ))}
          </div>
        )}
      </div>
    );
  }
</script>
```

Usage pattern in a prototype:

```javascript
const [tweaks, setTweaks] = useState(() => {
  const saved = JSON.parse(localStorage.getItem('cc-tweaks') || '{}');
  return {
    borderRadius: saved.borderRadius ?? 12,
    fontSize: saved.fontSize ?? 16,
    spacing: saved.spacing ?? 24,
  };
});

function handleTweak(key, value) {
  setTweaks(prev => {
    const next = { ...prev, [key]: Number(value) };
    localStorage.setItem('cc-tweaks', JSON.stringify(next));
    return next;
  });
}
```

---

## Starter Templates

Copy a template into your project to scaffold a new design:

```bash
# Slide deck
cp ~/.claude/skills/cc-design/templates/deck_stage.js ./src/deck.js

# Side-by-side option grid (3 directions)
cp ~/.claude/skills/cc-design/templates/design_canvas.jsx ./src/canvas.jsx

# iPhone device frame
cp ~/.claude/skills/cc-design/templates/ios_frame.jsx ./src/ios_frame.jsx

# macOS window chrome
cp ~/.claude/skills/cc-design/templates/macos_window.jsx ./src/macos_window.jsx

# Timeline animation engine
cp ~/.claude/skills/cc-design/templates/animations.jsx ./src/animations.jsx
```

---

## Common Patterns

### Landing Page with 3 Variations

```
"Design a SaaS landing page for a developer tool. Show 3 visual directions:
one minimal/technical, one bold/marketing, one warm/community-focused."
```

The agent will produce a single HTML file with a `DesignCanvas` grid showing all three side by side, plus a full-page version of each.

### Pitch Deck (10 slides)

```
"Create a 10-slide seed round pitch deck for a B2B AI startup.
Use Notion-style typography and Linear's purple accent color."
```

The agent loads both brand systems, merges tokens, and scaffolds `deck_stage.js` with a slide navigator.

### Mobile Prototype

```
"Build an interactive onboarding flow for iOS — 4 screens, swipe to advance,
show it inside an iPhone frame."
```

The agent copies `ios_frame.jsx`, builds the 4-screen flow with `useState` for navigation, and verifies with a Playwright screenshot at 390×844 viewport.

### Animation Study

```
"Animate a card component: entrance fade-up, hover lift, click ripple.
Show slow/medium/fast timing variations."
```

The agent uses `animations.jsx` as the base timeline engine and adds a tweaks panel for duration control.

---

## Troubleshooting

**Babel/React not rendering:**
- Confirm `type="text/babel"` is on the script tag.
- Check the browser console (or Playwright error log) for `Uncaught ReferenceError` — usually means a hook was called as `React.useState` instead of destructured `useState`.
- Ensure CDN scripts load before the Babel script tag.

**Playwright screenshot is blank:**
- Add `await page.waitForLoadState('networkidle')` before the screenshot call.
- For animated content, add `await page.waitForTimeout(500)` to let transitions settle.

**PPTX export has missing styles:**
- Run `super_inline_html.js` first to produce a fully self-contained HTML file, then pass that to `gen_pptx.js`.

**Brand tokens not applied:**
- Verify the CSS custom properties are on `:root`, not scoped to a component class.
- Check that component inline styles reference `var(--token-name)` rather than hardcoded values.

**`npm install` fails in scripts/:**
- Requires Node.js ≥ 18. Check with `node --version`.
- If `playwright` install hangs, run `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install` and install Chromium separately with `npx playwright install chromium`.

---

## References (Load on Demand)

| File | When to load |
|---|---|
| `references/getdesign-loader.md` | Brand style cloning is requested |
| `references/platform-tools.md` | Playwright MCP or host tool mapping needed |
| `references/react-babel-setup.md` | Complex multi-component JSX scope issues |
| `references/starter-components.md` | Selecting or adapting a template |
| `references/tweaks-system.md` | Adding in-page design controls |
