---
name: deco-e2e-testing
description: Implement end-to-end performance tests for any Deco e-commerce site with lazy section tracking, cache analysis, and observability. Use this skill when asked to set up e2e tests, create performance testing infrastructure, or test user journeys on a Deco/VTEX site.
---

# Deco E2E Performance Testing Skill

This skill helps you implement comprehensive e2e performance tests for Deco e-commerce sites. It covers the full user journey: Home → PLP → PDP → Add to Cart, with **lazy section tracking**, **cache analysis**, and **device-specific reports**.

## When to Use This Skill

- Setting up e2e tests from scratch on a Deco site
- Creating performance testing infrastructure
- Testing cache performance (cold vs warm)
- Validating TTFB, FCP, and other Core Web Vitals
- **Debugging slow lazy sections** (`/deco/render` requests)
- **Analyzing page cache and CDN behavior**
- **Comparing performance across desktop/mobile**

## Quick Start

1. **Discover site-specific values** (read `discovery.md`)
2. **Run scaffold script** or copy templates manually
3. **Configure selectors** for your site
4. **Add deno.json tasks** for easy test execution
5. **Run tests** and verify

## Workflow

```
1. Read discovery.md → Find site-specific selectors
2. Run scaffold.sh → Create test directory structure
3. Replace {{PLACEHOLDERS}} → Customize for site
4. Add deno.json tasks → Enable `deno task test:e2e`
5. npm install && deno task test:e2e → Verify tests work
```

## Directory Structure to Create

```
tests/e2e/
├── README.md
├── package.json
├── playwright.config.ts
├── tsconfig.json
├── specs/
│   └── ecommerce-flow.spec.ts
├── utils/
│   └── metrics-collector.ts
├── scripts/
│   └── baseline.ts
└── reports/                    # gitignored
    ├── report-desktop-chrome.json
    ├── report-mobile-chrome.json
    └── baselines/

scripts/
└── run-e2e.ts                  # Test runner with server management
```

## Test Flow

| Step | Page | Metrics |
|------|------|---------|
| 1 | Server Warmup | Liveness check, lazy import trigger |
| 2 | Homepage (cold cache) | TTFB, FCP, lazy sections, scroll |
| 3 | Homepage (warm cache) | Cache improvement |
| 4 | PLP (cold cache) | TTFB, products loaded, lazy sections |
| 5 | PLP (warm cache) | Cache improvement |
| 6 | PDP (cold cache) | TTFB, buy button, lazy sections |
| 7 | PDP (warm cache) | Cache improvement |
| 8 | Add to Cart | Response time |
| 9 | Minicart | Verification (with retry) |

## Key Features

### 1. Lazy Section Tracking

The test tracks all `/deco/render` requests (lazy-loaded sections) with:
- **Section name** extracted from `x-deco-section` header
- **Timing** with color-coded status (🟢 fast, 🟡 medium, 🔴 slow)
- **Cache status** (💾 HIT, ❌ MISS, ⏳ STALE)

```
🔄 Lazy Sections (14):
┌───────────────────────────────────────────────────────────
│ 🔴 Product/ProductShelf: L...  1182ms 💾 cached
│ 🔴 Product/ProductShelfGroup   1000ms 💾 cached
│ 🟢 Footer/Footer                 13ms 💾 cached
└───────────────────────────────────────────────────────────
📊 Summary: 5 fast, 2 medium, 7 slow │ Total: 7121ms
```

### 2. Scroll-Based Lazy Loading

The test scrolls the page to trigger lazy sections and waits for them:

```typescript
// Scroll until footer is visible, waiting for pending renders
await collector.scrollPage(page, true) // full=true for homepage
```

This ensures all lazy sections are triggered and their performance is measured.

### 3. Device-Specific Reports

Tests run on both desktop and mobile with separate reports:

```
reports/
├── report-desktop-chrome.json
├── report-mobile-chrome.json
├── report-latest-desktop.json
└── report-latest-mobile.json
```

### 4. Enhanced Report Structure

Reports include a summary for easy comparison:

```json
{
  "project": "desktop-chrome",
  "timestamp": "2026-01-18T...",
  "summary": {
    "totalPages": 7,
    "avgTTFB": 485,
    "avgFCP": 892,
    "totalLazyRenders": 32,
    "totalLoaders": 12,
    "cacheHits": 28,
    "cacheMisses": 4,
    "pages": [...]
  },
  "metrics": [...]
}
```

### 5. Deco Observability Headers

The test captures custom Deco headers for debugging:
- `x-deco-section` - Section component type and title
- `x-deco-page` - Matched page block name
- `x-deco-route` - Matched route template

## Critical: Server Warmup

**Deco/Fresh lazily loads imports on first request.** This causes artificially high latency for the first request after server start. The test must:

1. Wait for `/deco/_liveness` endpoint to return 200
2. Make a warmup request to trigger lazy imports
3. Only then start measuring performance

```typescript
const LIVENESS_PATH = '/deco/_liveness'

async function waitForServerReady(baseUrl: string) {
    // Step 1: Wait for liveness
    for (let i = 0; i < 30; i++) {
        const res = await fetch(`${baseUrl}/deco/_liveness`)
        if (res.ok) break
        await new Promise(r => setTimeout(r, 1000))
    }

    // Step 2: Warmup request to trigger lazy imports
    await fetch(`${baseUrl}/?__d`)
}
```

## Key Configuration

The `SITE_CONFIG` object centralizes all site-specific values:

```typescript
const SITE_CONFIG = {
    // URLs
    baseUrl: 'https://localhost--{sitename}.deco.site',
    plpPath: '/category-path',
    fallbackPdpPath: '/product-name-sku/p',
    
    // Always use ?__d for Server-Timing headers
    debugParam: '?__d',

    // Deco framework endpoints
    livenessPath: '/deco/_liveness',

    // Selectors
    productCard: '[data-deco="view-product"]',
    productCardFallback: 'a:has-text("R$")',
    buyButton: 'button:has-text("Comprar agora")',
    buyButtonFallback: 'button:has-text("Comprar")',
    minicartText: 'Produtos Adicionados',

    // Sizes (fashion) or voltages (electronics)
    sizes: ['P', 'M', 'G', 'GG'],
    voltages: ['110V', '127V', '220V', 'Bivolt'],

    // Thresholds (ms)
    thresholds: {
        coldTTFB: 5000,
        warmTTFB: 2000,
        homeTTFB: 3000,
        homeWarmTTFB: 1500,
    },

    // Server warmup settings
    warmup: {
        livenessRetries: 30,
        livenessRetryDelay: 1000,
        warmupTimeout: 60000,
    },
}
```

## deno.json Integration

Add these tasks to the site's `deno.json`:

```json
{
  "tasks": {
    "test:e2e": "deno run -A scripts/run-e2e.ts",
    "test:e2e:headed": "deno run -A scripts/run-e2e.ts --headed",
    "test:e2e:install": "cd tests/e2e && npm install && npx playwright install chromium",
    "test:e2e:baseline:save": "deno run -A tests/e2e/scripts/baseline.ts save",
    "test:e2e:baseline:compare": "deno run -A tests/e2e/scripts/baseline.ts compare"
  }
}
```

## .gitignore Updates

Add to `.gitignore`:

```gitignore
# E2E test reports (generated artifacts)
tests/e2e/reports/report-*.json
tests/e2e/reports/test-results/
tests/e2e/reports/results.json
```

## Files in This Skill

| File | Purpose |
|------|---------|
| `SKILL.md` | This overview |
| `discovery.md` | How to find site-specific values |
| `templates/` | Ready-to-use test files |
| `templates/scripts/run-e2e.ts` | Test runner with server management |
| `templates/scripts/baseline.ts` | Baseline save/compare script |
| `selectors.md` | Platform-specific selector patterns |
| `troubleshooting.md` | Common issues and fixes |
| `scripts/scaffold.sh` | Auto-create test structure |

## Expected Output

```
══════════════════════════════════════════════════════════════════════
🖥️  Desktop (desktop-chrome)
══════════════════════════════════════════════════════════════════════

══════════════════════════════════════════════════════════════════════
🏠 HOMEPAGE (cold cache)
══════════════════════════════════════════════════════════════════════
   📜 Scrolling to trigger lazy renders (full)...
      ⏳ Waiting for 1 pending render before next scroll...
      ✅ Footer visible after 47 scrolls
   📜 Triggered 13 lazy renders

   🟢 TTFB:   414ms  🟡 FCP:  1508ms  │  🌐 369 requests (11.7 MB)

   ⚡ Server Timing: 0ms total (1 loaders)

   🔄 Lazy Sections (14):
   ┌───────────────────────────────────────────────────────────
   │ 🔴 Product/ProductShelf: L...  1182ms 💾 cached
   │ 🔴 Product/ProductShelfGroup   1000ms 💾 cached
   │ 🟢 Content/SimpleText            18ms 💾 cached
   │ 🟢 Footer/Footer                 13ms 💾 cached
   └───────────────────────────────────────────────────────────
   📊 Summary: 5 fast, 2 medium, 7 slow │ Total: 7121ms

══════════════════════════════════════════════════════════════════════
📊 PERFORMANCE SUMMARY
══════════════════════════════════════════════════════════════════════

   ┌──────────────────┬─────────────┬─────────────┬────────┐
   │ Page             │       TTFB  │        FCP  │  Lazy  │
   ├──────────────────┼─────────────┼─────────────┼────────┤
   │ Homepage Cold    │ 🟢   414ms │  🟡  1508ms │     14 │
   │ Homepage Warm    │ 🟢   485ms │  🟢   560ms │      4 │
   │ PLP Cold         │ 🟢   456ms │  🟢   508ms │      3 │
   │ PDP Cold         │ 🟢   459ms │  🟢   520ms │      4 │
   └──────────────────┴─────────────┴─────────────┴────────┘

   Legend: 🟢 Good  🟡 Needs Work  🔴 Poor
   Thresholds: TTFB <500ms good, <800ms ok | FCP <1000ms good, <1800ms ok
```

## Baseline Comparison

Save performance baselines and compare future runs to detect regressions.

### Save a Baseline

```bash
deno task test:e2e:baseline:save
```

### Compare Against Baseline

```bash
deno task test:e2e:baseline:compare
```

### Regression Thresholds

| Metric | Threshold |
|--------|-----------|
| TTFB   | +10% |
| FCP    | +10% |
| LCP    | +15% |
| CLS    | +50% |

## Minicart Robustness

The minicart verification uses multiple selectors and retry logic:

```typescript
async isMinicartOpen(): Promise<boolean> {
    const selectors = [
        `text=${SITE_CONFIG.minicartText}`,
        '[data-testid="minicart"]',
        '.minicart',
        '[class*="minicart"]',
        '[class*="cart-drawer"]',
    ]
    
    // Retry with increasing timeout
    for (let attempt = 0; attempt < 3; attempt++) {
        const timeout = 2000 + (attempt * 1000)
        for (const selector of selectors) {
            const visible = await this.page.locator(selector).first()
                .isVisible({ timeout }).catch(() => false)
            if (visible) return true
        }
        await this.page.waitForTimeout(500)
    }
    return false
}
```

## Integration with Deco Runtime

For full lazy section observability, ensure your deco runtime includes:

1. **x-deco-section header** in `/deco/render` responses
2. **x-deco-page header** with matched page block name
3. **x-deco-route header** with matched route template

These are set in:
- `deco/runtime/features/render.tsx` - Section name extraction
- `deco/runtime/routes/render.tsx` - Header setting
- `deco/runtime/middleware.ts` - Page/route headers
- `apps/website/handlers/fresh.ts` - Page block state

## Next Steps

1. Read `discovery.md` to learn how to find the correct selectors and paths
2. Check `selectors.md` for platform-specific patterns (VTEX, Shopify, VNDA)
3. See `troubleshooting.md` if tests fail
4. Use the MCP tools to search for related optimization patterns
