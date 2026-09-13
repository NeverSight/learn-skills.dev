---
name: posterskill-academic-posters
description: AI-assisted academic conference poster generation from Overleaf source using Claude Code
triggers:
  - make a conference poster from my paper
  - generate an academic poster
  - create a poster from my overleaf project
  - build a print-ready poster HTML file
  - convert my latex paper to a poster
  - make a poster with posterskill
  - run the make-poster skill
  - help me design an academic poster
---

# posterskill — Academic Poster Generator

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

posterskill is a Claude Code skill that generates print-ready, interactive conference posters from your Overleaf paper source. It produces a single self-contained HTML file with a built-in drag-and-drop visual editor — no build step, no server required.

## Installation & Setup

```bash
git clone git@github.com:ethanweber/posterskill.git poster
cd poster

# Clone your Overleaf paper source
git clone https://git.overleaf.com/YOUR_PROJECT_ID overleaf

# Optional: add reference posters for style matching
cp ~/Downloads/some_reference_poster.pdf references/
```

Start Claude Code and trigger the skill:

```bash
claude
```

```
/make-poster
```

Claude will ask for your project website URL and any formatting specs, then generate a `poster/` directory with `index.html`.

## Directory Structure

```
poster/                  # this repo
├── .claude/
│   └── commands/
│       └── make-poster.md   # the skill command
├── overleaf/            # your cloned Overleaf project
├── references/          # optional reference PDFs for style matching
└── poster/              # generated output
    ├── index.html       # the poster (self-contained)
    └── logos/           # downloaded institutional logos
```

## What Gets Generated

The output `poster/index.html` is a React app (loaded via CDN) containing:

- **`CARD_REGISTRY`** — each card's title, color, and JSX body content
- **`DEFAULT_LAYOUT`** — column structure and card ordering
- **`DEFAULT_LOGOS`** — institutional logos for the header
- **`window.posterAPI`** — programmatic API for layout automation

## Visual Editor Features

Open `poster/index.html` in Chrome to access the built-in editor:

| Feature | How to Use |
|---------|-----------|
| Resize columns | Drag column dividers left/right |
| Resize cards | Drag row dividers up/down within a column |
| Swap cards | Click one diamond handle, then another |
| Move/insert cards | Click a handle, then click a drop zone |
| Adjust font size | Click **A-** / **A+** buttons in toolbar |
| Preview print layout | Click **Preview** button |
| Export layout | Click **Copy Config** to get JSON |

## Programmatic API (`window.posterAPI`)

Available in the browser console or via Playwright automation:

```js
// Swap two cards by ID
posterAPI.swapCards('method', 'results')

// Move a card to a specific column and position
posterAPI.moveCard('quant', 'col1', 2)

// Resize a column (in mm)
posterAPI.setColumnWidth('col1', 280)

// Set a specific card's height (in mm)
posterAPI.setCardHeight('method', 150)

// Scale all text globally
posterAPI.setFontScale(1.5)

// Measure whitespace waste (lower = better layout)
posterAPI.getWaste()

// Get the current layout as an object
posterAPI.getLayout()

// Get the full config as JSON (paste back to Claude)
posterAPI.getConfig()

// Reset to default layout
posterAPI.resetLayout()
```

## Iteration Workflow

The core loop for refining your poster:

1. **Claude generates** first draft, opens `poster/index.html` in your browser
2. **You edit** in the browser — drag dividers, swap cards, resize columns
3. **Click "Copy Config"** in the toolbar to export your layout as JSON
4. **Paste the JSON back to Claude** — it updates `DEFAULT_LAYOUT` in the HTML
5. **Repeat** until the layout is perfect
6. **Print to PDF**: File → Print → Margins: None, Background Graphics: On

## Playwright Automation (used internally by Claude)

Claude uses Playwright to automate layout verification. You can use it too:

```js
const { chromium } = require('playwright');

async function optimizePoster() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.goto(`file://${__dirname}/poster/index.html`);
  
  // Use the posterAPI to adjust layout programmatically
  const waste = await page.evaluate(() => posterAPI.getWaste());
  console.log('Whitespace waste:', waste);
  
  // Resize a column
  await page.evaluate(() => posterAPI.setColumnWidth('col1', 300));
  
  // Take a screenshot for visual verification
  await page.screenshot({ path: 'poster-preview.png', fullPage: true });
  
  // Generate PDF at print resolution
  await page.pdf({
    path: 'poster.pdf',
    width: '841mm',   // A0 landscape width
    height: '1189mm',
    printBackground: true,
  });
  
  await browser.close();
}
```

## Card Registry Structure

Each card in the poster is defined in `CARD_REGISTRY`:

```js
const CARD_REGISTRY = {
  abstract: {
    title: "Abstract",
    color: "#f0f4ff",
    body: `
      <p>Your abstract text here. Supports full JSX including
      <strong>bold</strong>, <em>italic</em>, and inline math.</p>
    `
  },
  method: {
    title: "Method",
    color: "#fff8f0",
    body: `
      <img src="figures/pipeline.png" style={{width:'100%'}} />
      <p>Caption describing the pipeline above.</p>
    `
  },
  results: {
    title: "Results",
    color: "#f0fff4",
    body: `
      <table>...</table>
    `
  }
};
```

## Default Layout Structure

```js
const DEFAULT_LAYOUT = {
  columns: [
    {
      id: 'col1',
      widthMm: 280,
      cards: ['abstract', 'method']
    },
    {
      id: 'col2', 
      widthMm: 320,
      cards: ['results', 'quant']
    },
    {
      id: 'col3',
      widthMm: 280,
      cards: ['conclusion', 'references']
    }
  ]
};
```

## Inputs Claude Uses

| Input | Where It Comes From | Required |
|-------|--------------------|---------:|
| Paper content | `overleaf/` directory | Yes |
| Project website | URL (asked at runtime) | Yes |
| Reference posters | `references/*.pdf` | No |
| Author website | URL for brand matching | No |
| Formatting specs | Conference URL or text | Asked if missing |
| Logos | Auto-downloaded to `poster/logos/` | Auto |

## Common Patterns

### Adding a custom figure card

```js
// In CARD_REGISTRY, add a new card
custom_fig: {
  title: "Qualitative Results",
  color: "#fafafa",
  body: `
    <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'8px'}}>
      <img src="figures/result1.png" style={{width:'100%'}} />
      <img src="figures/result2.png" style={{width:'100%'}} />
    </div>
    <p style={{fontSize:'0.85em', textAlign:'center'}}>
      Comparison on held-out test scenes.
    </p>
  `
}
```

Then add it to `DEFAULT_LAYOUT`:

```js
{ id: 'col2', widthMm: 320, cards: ['results', 'custom_fig'] }
```

### Logos configuration

```js
const DEFAULT_LOGOS = [
  { src: 'logos/university.png', height: 60 },
  { src: 'logos/lab.png', height: 50 },
  { src: 'logos/sponsor.png', height: 45 },
];
```

### Printing to PDF

In Chrome:
1. Open `poster/index.html`
2. Click **Preview** to verify layout
3. `Ctrl+P` / `Cmd+P`
4. Set **Margins: None**
5. Enable **Background graphics**
6. Set paper size to your conference spec (A0, 36×48in, etc.)
7. Save as PDF

## Troubleshooting

**Poster looks different in print vs browser**
→ Use Chrome (not Firefox/Safari). Enable "Background graphics" in print dialog.

**Figures not loading**
→ Ensure figure paths in the HTML are relative to `poster/index.html`. Claude copies figures to `poster/figures/` — verify the directory exists.

**Logos not fetched**
→ Claude uses Playwright to download logos from your project website. If it fails, manually copy logo files to `poster/logos/` and update `DEFAULT_LOGOS` paths.

**Layout config not updating after paste**
→ Make sure you paste the full JSON from **Copy Config** — Claude looks for the complete `DEFAULT_LAYOUT` and `DEFAULT_LOGOS` objects to replace.

**Font too small/large for poster size**
→ Use `posterAPI.setFontScale(1.2)` in the browser console, or click **A+** / **A-** buttons, then Copy Config and paste to Claude.

**Whitespace gaps between cards**
→ Run `posterAPI.getWaste()` in console to quantify. Use `posterAPI.setCardHeight('cardId', heightMm)` to tune card heights, or drag row dividers manually.

## Example Output

See the [Fillerbuster poster](http://ethanweber.me/fillerbuster-poster) ([repo](https://github.com/ethanweber/fillerbuster-poster)) as a live example of posterskill output.
