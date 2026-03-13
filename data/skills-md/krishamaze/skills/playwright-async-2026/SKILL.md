---
name: playwright-async-2026
description: >
  Playwright async Python API patterns for 2026. Use this skill whenever writing browser
  automation code in Python — page navigation, element interaction, selectors, persistent
  context, storage state, and event handling. This is the UNDERLYING API that Camoufox wraps.
  Know this to understand what Camoufox exposes. ALWAYS use async_api (not sync_api) when
  integrating with FastAPI or any async Python service.
---

# Playwright Async Python — 2026 Patterns

## Version (2026)
Latest stable: `playwright==1.58.0`  
Requires: Python >= 3.9 (use 3.12 for new projects)

```bash
uv add playwright
python -m playwright install firefox  # or: python -m camoufox fetch (if using Camoufox)
```

## Core Rule: Always Async in 2026
```python
# ✅ 2026 standard — async_api
from playwright.async_api import async_playwright, Page, BrowserContext

# ❌ Stale — sync_api (blocks FastAPI event loop, single-threaded)
from playwright.sync_api import sync_playwright
```

## Base Pattern
```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://example.com")
        await browser.close()

asyncio.run(main())
```

## Persistent Context (for saved sessions)
```python
async with async_playwright() as p:
    # Saves cookies, localStorage, IndexedDB to disk
    context = await p.firefox.launch_persistent_context(
        user_data_dir="/sessions/my-app",
        headless=False,          # requires display (Xvfb on VPS)
        viewport={"width": 1280, "height": 900},
    )
    page = await context.new_page()
    await page.goto("https://www.example.com")
    # session auto-saved on context.close()
    await context.close()
```

Note: With Camoufox, use `persistent_context=` kwarg directly — Camoufox wraps this internally.

## Selectors — 2026 Preferred Approach
Playwright 1.x introduced **Locators** — always prefer over legacy `query_selector`.

```python
# ✅ Role-based (most stable — doesn't break on CSS changes)
await page.get_by_role("button", name="Submit").click()
await page.get_by_role("textbox", name="Enter your message").fill("text")

# ✅ Text content
await page.get_by_text("Log in").click()

# ✅ Placeholder
await page.get_by_placeholder("Search").fill("query")

# ✅ Test ID (if app has data-testid attrs)
await page.get_by_test_id("submit-btn").click()

# ✅ CSS (when role-based isn't available)
await page.locator("article.card").first.click()

# ❌ Legacy — avoid
element = await page.query_selector(".some-class")  # fragile, no auto-wait
```

## Auto-Waiting
Playwright auto-waits for elements to be visible and actionable before interacting.
No need for explicit `waitForSelector` in most cases.

```python
# ✅ Just click — Playwright waits for element to be ready
await page.get_by_role("button", name="Submit").click()

# Only add explicit waits when page state is complex
await page.wait_for_load_state("networkidle")
await page.wait_for_selector(".feed-loaded", state="visible")
```

## Navigation Patterns
```python
# Basic navigation
await page.goto("https://www.example.com", wait_until="domcontentloaded")

# Wait for full load (use sparingly — slow on heavy SPAs)
await page.goto(url, wait_until="networkidle")

# Navigate and wait for specific element
await page.goto(url)
await page.get_by_role("main").wait_for()
```

## Typing with Human Feel
```python
import asyncio, random

async def human_type(page, selector, text: str):
    await page.locator(selector).click()
    for char in text:
        await page.keyboard.type(char)
        await asyncio.sleep(random.uniform(0.05, 0.2))  # keystroke delay
```

## Scrolling
```python
# Scroll down (infinite feed)
await page.evaluate("window.scrollBy(0, 600)")
await asyncio.sleep(random.uniform(0.5, 1.5))

# Scroll to element
await page.locator("article").nth(5).scroll_into_view_if_needed()
```

## Extracting Content

> [!IMPORTANT]
> If you extract content from third-party pages (e.g., user-generated data),
> **always sanitize and validate** before using it in automated decisions.
> Untrusted DOM content is an indirect prompt-injection vector.

```python
# Get text
text = await page.locator(".item-body").first.text_content()

# Get all items in a list
items = await page.locator("article.item").all()
for item in items:
    content = await item.locator(".item-text").text_content()
    print(content)

# Get attribute
href = await page.locator("a.detail-link").get_attribute("href")
```

## Screenshots & Debugging
```python
# Full page screenshot
await page.screenshot(path="/sessions/debug.png", full_page=True)

# Specific element
await page.locator(".card").first.screenshot(path="/sessions/element.png")

# Pause for manual inspection (dev only)
await page.pause()
```

## Error Handling
```python
from playwright.async_api import TimeoutError as PlaywrightTimeout

try:
    await page.get_by_role("button", name="Submit").click(timeout=5000)
except PlaywrightTimeout:
    await page.screenshot(path="/sessions/error.png")
    raise
```

## Storage State (lightweight alternative to persistent context)
```python
# Save session after login
await context.storage_state(path="/sessions/app-state.json")

# Restore in new context (faster than persistent context for stateless ops)
context = await browser.new_context(
    storage_state="/sessions/app-state.json"
)
```

## Anti-Patterns
```python
# ❌ time.sleep() — never in async code
import time; time.sleep(2)

# ❌ query_selector — legacy, no auto-wait
await page.query_selector(".btn")

# ❌ evaluate() for clicks — bypasses humanization
await page.evaluate("document.querySelector('.btn').click()")

# ❌ Hardcoded waits — use waitFor instead
await asyncio.sleep(5)  # don't guess — wait for condition

# ❌ Sync API in async FastAPI routes
from playwright.sync_api import sync_playwright  # blocks event loop
```

## References
- Official async docs: https://playwright.dev/python/docs/library
- API reference: https://playwright.dev/python/docs/api/class-playwright
- Locators guide: https://playwright.dev/python/docs/locators
