---
name: screenshot-local
description: |
  Use when capturing screenshots of local projects, documenting web app UI,
  taking screenshots of localhost dev servers, or generating images for READMEs and docs.
  Use when asked to "screenshot my app", "capture the UI", "take a screenshot of localhost",
  "generate screenshots for docs", "batch screenshot my pages", or "set up shot-scraper".
license: MIT
metadata:
  author: Antonin Januska
  version: "1.0.0"
  argument-hint: <url-or-file> [--output filename.png]
tags: [screenshot, shot-scraper, docs, localhost, ui, documentation, pipx]
---

# Screenshot Local - Capture Project Screenshots with shot-scraper

## Overview

Capture screenshots of local development projects using [shot-scraper](https://github.com/simonw/shot-scraper) installed globally via pipx. Turn localhost URLs and local HTML files into PNGs, JPEGs, and PDFs for documentation, READMEs, and design reviews.

**Core principle:** Screenshots should be reproducible from a single command or YAML config, not manual screen captures. Version-control your screenshot configs alongside your code.

## When to Use

**Use this skill when:**
- Capturing screenshots of a local dev server for docs or README
- Generating screenshots of multiple pages/states in batch
- Documenting UI changes or new features visually
- Creating before/after comparisons during refactoring
- Automating screenshot generation in CI/CD

**Avoid when:**
- Recording terminal/CLI output (use `record-tui` with VHS instead)
- Capturing non-web content (use native screenshot tools)
- Scraping third-party websites (shot-scraper can do it, but this skill focuses on local projects)

## Prerequisites

**Install shot-scraper globally via pipx:**

```bash
# Install pipx if needed
brew install pipx  # macOS
# or: apt install pipx / pip install pipx

# Install shot-scraper globally
pipx install shot-scraper

# Install the browser engine (Chromium by default)
shot-scraper install
```

**Verify:** `shot-scraper --version`

**Alternative browsers:**
```bash
shot-scraper install -b firefox
shot-scraper install -b webkit
```

## Phase 1: Plan the Screenshots

Before capturing, answer these questions:

1. **What are you capturing?** — localhost URL, local HTML file, or built static site
2. **Which pages/states?** — Single page, multiple routes, or specific UI states
3. **What dimensions?** — Match your target display context
4. **Any interaction needed?** — Click buttons, fill forms, dismiss modals before capture

**Recommended dimensions by use case:**

| Use Case | Width | Height | Format |
|----------|-------|--------|--------|
| README hero image | 1280 | 800 | PNG |
| Docs screenshot | 1200 | auto | PNG |
| Social/OG image | 1200 | 630 | PNG |
| Mobile viewport | 375 | 812 | PNG |
| Tablet viewport | 768 | 1024 | PNG |
| Full page capture | 1280 | (omit) | PNG |

## Phase 2: Capture Screenshots

### Single Screenshot

**Capture a localhost page:**
```bash
shot-scraper http://localhost:3000 -o homepage.png
```

**Capture a local HTML file:**
```bash
shot-scraper index.html -o preview.png
```

**With custom dimensions:**
```bash
shot-scraper http://localhost:3000 -w 1200 -h 800 -o homepage.png
```

**Retina (2x resolution):**
```bash
shot-scraper http://localhost:3000 --retina -o homepage-retina.png
```

**Capture a specific element:**
```bash
shot-scraper http://localhost:3000 -s ".hero-section" -o hero.png
shot-scraper http://localhost:3000 -s "#main-nav" --padding 10 -o nav.png
```

**Wait for dynamic content:**
```bash
# Wait fixed time (ms)
shot-scraper http://localhost:3000 --wait 2000 -o page.png

# Wait for JS condition
shot-scraper http://localhost:3000 --wait-for "document.querySelector('.loaded')" -o page.png
```

**Execute JS before capture (dismiss modals, set state):**
```bash
shot-scraper http://localhost:3000 \
  -j "document.querySelector('.cookie-banner')?.remove()" \
  -o clean-homepage.png
```

### Essential Options

| Flag | Example | Purpose |
|------|---------|---------|
| `-o` | `-o hero.png` | Output filename |
| `-w` | `-w 1280` | Viewport width (default: 1280) |
| `-h` | `-h 800` | Viewport height (omit for full page) |
| `-s` | `-s ".card"` | CSS selector to capture |
| `--selector-all` | `--selector-all ".card"` | All matching elements |
| `-p` | `-p 10` | Padding around selector (px) |
| `--retina` | `--retina` | 2x device pixel ratio |
| `--quality` | `--quality 80` | Save as JPEG with quality |
| `--wait` | `--wait 2000` | Wait ms after page load |
| `--wait-for` | `--wait-for "expr"` | Wait until JS returns true |
| `-j` | `-j "js code"` | Execute JS before screenshot |
| `-b` | `-b firefox` | Browser (chromium/firefox/webkit) |
| `--omit-background` | `--omit-background` | Transparent background (PNG) |
| `--timeout` | `--timeout 10000` | Failure timeout (ms) |

For the complete flag reference, see **[Command Reference](./reference/COMMAND-REFERENCE.md)**.

### Batch Screenshots with YAML

Create a `shots.yml` for capturing multiple pages:

```yaml
# shots.yml
- url: http://localhost:3000
  output: screenshots/homepage.png
  width: 1280
  height: 800

- url: http://localhost:3000/about
  output: screenshots/about.png
  width: 1280

- url: http://localhost:3000/dashboard
  output: screenshots/dashboard.png
  width: 1280
  height: 900
  wait: 2000
  javascript: |
    document.querySelector('.loading-spinner')?.remove()

- url: http://localhost:3000
  output: screenshots/mobile-home.png
  width: 375
  height: 812
```

**Run the batch:**
```bash
shot-scraper multi shots.yml
```

### Advanced YAML Keys

```yaml
- url: http://localhost:3000/form
  output: screenshots/form-filled.png
  width: 1200
  javascript: |
    document.querySelector('#name').value = 'Jane Doe';
    document.querySelector('#email').value = 'jane@example.com';
  wait: 500
  selector: ".form-container"
  padding: 20
  retina: true
```

**Supported YAML keys:** `url`, `output`, `width`, `height`, `quality`, `wait`, `wait_for`, `selector`, `selectors`, `selector_all`, `padding`, `javascript`, `js_selector`, `retina`, `omit_background`

## Phase 3: Smart Config Generation

When asked to generate a screenshot config for a project, follow this process:

### Step 1: Analyze the Project

Read the project to understand:
- **Routes/pages** — Check router config, page files, or navigation
- **Key UI states** — Loading, empty, populated, error states
- **Important components** — Hero sections, dashboards, forms
- **Port** — What port does the dev server run on

### Step 2: Generate shots.yml

Build a YAML config covering the project's key screens:

```bash
# Validate by running
shot-scraper multi shots.yml
```

### Step 3: Iterate

Review screenshots, adjust timing and selectors, re-run.

## Phase 4: Optimize Output

### File Size Reduction

**Use JPEG for photos/complex UIs:**
```bash
shot-scraper http://localhost:3000 --quality 85 -o page.jpg
```

**Use PNG for UI with text/sharp edges (default).**

**Transparent backgrounds (for overlaying on docs):**
```bash
shot-scraper http://localhost:3000 -s ".component" --omit-background -o widget.png
```

### Consistency Tips

- Always set explicit `width` — default 1280 is fine but be intentional
- Omit `height` for full-page captures, set it for fixed viewport
- Use `--retina` for README images viewed on high-DPI screens
- Add `--wait` for SPAs that hydrate client-side
- Use `javascript` to dismiss cookie banners, tooltips, or modals
- Use `selector` + `padding` to capture specific components cleanly

## Phase 5: CI/CD Integration

### GitHub Actions

```yaml
name: Update Screenshots
on:
  push:
    branches: [main]
    paths: ["src/**", "shots.yml"]

jobs:
  screenshots:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install shot-scraper
        run: |
          pip install shot-scraper
          shot-scraper install

      - name: Capture screenshots
        run: |
          npm ci && npm run dev &
          sleep 5
          shot-scraper multi shots.yml

      - name: Commit updated screenshots
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "docs: update screenshots"
          file_pattern: "screenshots/*.png"
```

**Tip:** Use the `server` key in YAML to auto-start a dev server — see **[Templates](./reference/TEMPLATES.md)**.

## Examples

### Good: Well-Structured Screenshot Config

<Good>

```yaml
# shots.yml — explicit dimensions, proper waits, organized output
- url: http://localhost:3000
  output: screenshots/homepage.png
  width: 1280
  height: 800

- url: http://localhost:3000/dashboard
  output: screenshots/dashboard.png
  width: 1280
  height: 900
  wait: 2000
  javascript: |
    document.querySelector('.toast-notification')?.remove()

- url: http://localhost:3000/settings
  output: screenshots/settings.png
  width: 1280
  selector: ".settings-panel"
  padding: 20

- url: http://localhost:3000
  output: screenshots/mobile-home.png
  width: 375
  height: 812
```

</Good>

### Bad: Common Mistakes

<Bad>

```yaml
# No output specified — shot-scraper auto-names from URL, messy results
- url: http://localhost:3000

# No width — relies on default, inconsistent across machines
- url: http://localhost:3000/about
  output: about.png

# No wait for SPA — captures loading spinner instead of content
- url: http://localhost:3000/dashboard
  output: dashboard.png

# Screenshot directory not organized
- url: http://localhost:3000/settings
  output: settings.png
```

</Bad>

### Good: Capturing Specific Components

<Good>

```bash
# Hero section with padding for breathing room
shot-scraper http://localhost:3000 -s ".hero" -p 20 -o docs/hero.png

# Navigation in retina for crisp text
shot-scraper http://localhost:3000 -s "nav" --retina -o docs/nav.png

# Form with pre-filled data via JS
shot-scraper http://localhost:3000/contact \
  -j "document.querySelector('#name').value = 'Jane Doe'" \
  -s ".contact-form" -p 10 -o docs/form.png
```

</Good>

### Bad: Component Capture Anti-Patterns

<Bad>

```bash
# No selector — captures entire page when you only need one section
shot-scraper http://localhost:3000 -o hero.png

# No padding — element cropped tight, looks cramped in docs
shot-scraper http://localhost:3000 -s ".hero" -o hero.png

# No wait — dynamic component hasn't rendered yet
shot-scraper http://localhost:3000 -s ".chart" -o chart.png
```

</Bad>

## Troubleshooting

### Problem: Screenshot shows blank page or loading spinner

**Cause:** SPA hasn't hydrated or async data hasn't loaded.

**Solution:**
```bash
# Fixed wait
shot-scraper http://localhost:3000 --wait 3000 -o page.png

# Wait for specific element
shot-scraper http://localhost:3000 --wait-for "document.querySelector('.content')" -o page.png
```

### Problem: "Connection refused" on localhost

**Cause:** Dev server isn't running or is on a different port.

**Solution:**
1. Start your dev server first: `npm run dev &`
2. Verify the port: `curl -I http://localhost:3000`
3. Or use the `server` key in YAML to auto-start it

### Problem: Screenshot dimensions don't match expectations

**Cause:** Height omitted (captures full page) or retina not accounted for.

**Solution:**
- Set explicit `-h` for fixed viewport
- Omit `-h` intentionally for full-page capture
- `--retina` doubles pixel dimensions (1280w becomes 2560px image)

### Problem: shot-scraper command not found

**Cause:** Not installed or pipx PATH not configured.

**Solution:**
```bash
pipx install shot-scraper
pipx ensurepath      # Add pipx bin to PATH
shot-scraper install # Install browser engine
```

### Problem: Elements missing from screenshot

**Cause:** CSS selector wrong, element behind a modal, or lazy-loaded content.

**Solution:**
```bash
# Use --interactive to debug visually
shot-scraper http://localhost:3000 -i

# Use --devtools for inspector
shot-scraper http://localhost:3000 --devtools
```

## Integration

**This skill pairs with:**
- **record-tui** — For terminal app recordings (use VHS for CLIs, shot-scraper for web UIs)
- **track-session** — Track screenshot iteration progress
- **git-worktree** — Compare screenshots across branches

**Useful alongside:**
- [shot-scraper](https://github.com/simonw/shot-scraper) — The screenshot tool
- [shot-scraper-template](https://github.com/simonw/shot-scraper-template) — GitHub Actions template
- [pipx](https://pipx.pypa.io/) — Global Python app installer

## Quick Reference

```bash
# Single screenshot
shot-scraper http://localhost:3000 -o page.png

# With dimensions
shot-scraper http://localhost:3000 -w 1280 -h 800 -o page.png

# Specific element
shot-scraper http://localhost:3000 -s ".hero" -p 10 -o hero.png

# Retina
shot-scraper http://localhost:3000 --retina -o page@2x.png

# Local HTML file
shot-scraper index.html -o preview.png

# Batch from YAML
shot-scraper multi shots.yml

# Interactive debugging
shot-scraper http://localhost:3000 -i

# PDF export
shot-scraper pdf http://localhost:3000 -o page.pdf
```

## Deep Reference

For detailed guides, load these files when needed:

- **[Command Reference](./reference/COMMAND-REFERENCE.md)** — All shot-scraper commands, flags, and subcommands
- **[Templates](./reference/TEMPLATES.md)** — Copy-paste YAML configs for common project types

*Only load these when specifically needed to save context.*

## References

- [shot-scraper](https://github.com/simonw/shot-scraper) — Official repository
- [shot-scraper documentation](https://shot-scraper.datasette.io/) — Full docs
- [shot-scraper-template](https://github.com/simonw/shot-scraper-template) — GitHub Actions template
- [pipx](https://pipx.pypa.io/) — Global Python app installer
- [Simon Willison's blog](https://simonwillison.net/tags/shot-scraper/) — Author's posts on shot-scraper
