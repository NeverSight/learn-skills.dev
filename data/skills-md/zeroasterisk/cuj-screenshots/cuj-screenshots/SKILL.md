---
name: cuj-screenshots
description: Capture Critical User Journey (CUJ) screenshots and GIFs from web apps using headless Chromium. Use when you need to create visual demos, verify UI changes, or document user flows.
---

# CUJ Screenshots Skill

Automate visual documentation of web app user journeys using headless browser automation.

## When to Use This

**Always run CUJ captures after UI changes.** This is part of the dev loop, not just documentation.

### Triggered By:
- Any frontend component change
- CSS/styling updates
- New features that affect user flow
- Bug fixes that change visible behavior
- Before sharing work with humans ("here's what it looks like now")

### The Loop:
```
Make UI change → Run CUJs → Review screenshots → 
  ├─ Looks good? → Update GIFs, commit, share link
  └─ Looks wrong? → Fix bug, repeat
```

### Proactive Use:
When finishing UI work, don't just say "done" — capture CUJs, update the GIFs, and share:

> "Updated the task card styling. Here's the new CUJ: 
> https://github.com/user/repo/blob/main/docs/CUJs.md"

This gives your human instant visual feedback without them needing to run the app.

## What It Does

1. Launches headless Chromium via Playwright
2. Navigates through a defined user journey
3. Captures screenshots at each step
4. Stitches screenshots into an animated GIF
5. Outputs to a docs folder for commit

## Requirements

- **Playwright**: `uv run --with playwright python script.py`
- **Chromium**: Auto-installed by Playwright on first run
- **ImageMagick**: For GIF creation (`convert` command)

Install Playwright browsers (one-time):
```bash
uv run --with playwright playwright install chromium
```

## Quick Start

### 1. Define Your CUJ

Create a Python script for each journey:

```python
import asyncio
from playwright.async_api import async_playwright
import os

async def capture_my_cuj():
    output_dir = "/tmp/cuj-screenshots/my-cuj"
    os.makedirs(output_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 390, "height": 844},  # Mobile
            device_scale_factor=2  # Retina
        )
        page = await context.new_page()
        
        # Step 1
        await page.goto("http://localhost:5173")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=f"{output_dir}/01-initial.png")
        
        # Step 2: Interact
        await page.click("button:has-text('Submit')")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=f"{output_dir}/02-submitted.png")
        
        # ... more steps
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_my_cuj())
```

### 2. Run Capture

```bash
uv run --with playwright python my_cuj.py
```

### 3. Create GIF

```bash
convert -delay 150 -loop 0 /tmp/cuj-screenshots/my-cuj/*.png output.gif
```

- `-delay 150` = 1.5 seconds per frame (hundredths of a second)
- `-loop 0` = infinite loop

### 4. Commit & Share

```bash
mv output.gif docs/gifs/my-cuj.gif
git add docs/gifs/my-cuj.gif docs/CUJs.md
git commit -m "docs: add my-cuj GIF"
git push
```

## Viewport Presets

| Device | Width | Height | Scale |
|--------|-------|--------|-------|
| iPhone 12 Pro | 390 | 844 | 2 |
| iPhone SE | 375 | 667 | 2 |
| Pixel 5 | 393 | 851 | 2.75 |
| Desktop | 1280 | 720 | 1 |
| Desktop HD | 1920 | 1080 | 1 |

## Common Interactions

```python
# Click button by text
await page.click("button:has-text('Submit')")

# Fill input
await page.fill("input[name='email']", "test@example.com")

# Select dropdown
await page.select_option("select#plan", "premium")

# Wait for element
await page.wait_for_selector(".success-message")

# Scroll
await page.evaluate("window.scrollBy(0, 300)")

# Keyboard shortcut
await page.keyboard.press("Escape")
```

## Full Workflow Example

See `scripts/capture-cujs.py` for a complete example that:
- Starts backend + frontend servers
- Captures multiple CUJs
- Generates GIFs
- Updates CUJs.md

## Tips

- **Wait times**: Use `wait_for_timeout(1000)` after interactions for animations
- **Selectors**: Prefer `text=` or `has-text()` over fragile CSS selectors
- **Error handling**: Wrap interactions in try/except, screenshot on error
- **Naming**: Use numbered prefixes (`01-`, `02-`) for sort order
- **GIF size**: Keep under 500KB for GitHub README display

## CUJs.md Documentation

Create a `docs/CUJs.md` file to document each journey with embedded GIFs:

```markdown
# Critical User Journeys (CUJs)

## CUJ 1: App Tour

**Goal:** Navigate the main app layout.

**Steps:**
1. Open app → Activity tab
2. Switch to Live tab
3. Return to Activity

![App Tour](./gifs/cuj1-app-tour.gif)

---

## CUJ 2: Create Task

**Goal:** Create a new plan and task.

**Steps:**
1. Click "+ Plan"
2. Enter name, submit
3. Click "+ Task"
4. Enter name, submit

![Create Task](./gifs/cuj2-create-task.gif)
```

This serves as both documentation and visual regression baseline.

## Verifying UI Changes

After making UI changes:
1. Run the CUJ capture scripts
2. Review the new screenshots (you can read image files!)
3. If they look correct, update GIFs and commit
4. Update `CUJs.md` if steps changed
5. If something's wrong, you caught a bug!

## Full Workflow

```bash
# 1. Make UI changes
# 2. Start servers
# 3. Capture CUJs
uv run --with playwright python scripts/capture-cujs.py

# 4. Review screenshots (agent can view these)
# 5. Create GIFs
convert -delay 150 -loop 0 /tmp/cuj-screenshots/cuj1/*.png docs/gifs/cuj1.gif

# 6. Update CUJs.md with new steps/descriptions
# 7. Commit everything
git add docs/CUJs.md docs/gifs/
git commit -m "docs: update CUJ screenshots after UI changes"
git push
```
