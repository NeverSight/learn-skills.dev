---
name: designlang-design-extract
description: Extract complete design systems from any website — colors, typography, spacing, shadows, and more — using the designlang CLI.
triggers:
  - extract design tokens from a website
  - reverse engineer a website's design system
  - get colors and fonts from a site
  - generate tailwind config from existing site
  - copy design language from website
  - extract CSS variables from a URL
  - analyze website design system
  - clone a website's visual design
---

# DESIGNLANG — Design System Extraction

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

**designlang** crawls any website with a headless browser (Playwright), extracts every computed style from the live DOM, and generates 8 output files: AI-optimized markdown, visual HTML preview, Tailwind config, React theme, shadcn/ui theme, Figma variables, W3C design tokens, and CSS custom properties.

## Installation

```bash
# No install needed — run directly
npx designlang https://stripe.com

# Install globally
npm install -g designlang

# Install as an agent skill
npx skills add Manavarya09/design-extract
```

## Core Commands

### Basic Extraction

```bash
# Extract everything from a site
npx designlang https://stripe.com

# Extract everything with all captures enabled
npx designlang https://stripe.com --full

# Custom output directory and file prefix
npx designlang https://stripe.com --out ./tokens --name stripe

# Wait for SPA to load before extracting
npx designlang https://app.example.com --wait 2000

# Crawl multiple internal pages for site-wide tokens
npx designlang https://stripe.com --depth 3
```

### Specialized Extraction

```bash
# Extract dark mode styles
npx designlang https://vercel.com --dark

# Capture at 4 responsive breakpoints
npx designlang https://stripe.com --responsive

# Capture hover/focus/active interaction states
npx designlang https://stripe.com --interactions

# Take component screenshots (buttons, cards, nav, hero)
npx designlang https://stripe.com --screenshots

# Everything at once
npx designlang https://stripe.com --full
```

### Authentication

```bash
# With cookies for protected pages
npx designlang https://internal-app.com --cookie "session=abc123" --cookie "user_id=42"

# With custom headers
npx designlang https://internal-app.com --header "Authorization:Bearer $TOKEN"

# Combined
npx designlang https://app.example.com \
  --cookie "session=$SESSION_COOKIE" \
  --header "X-API-Key:$API_KEY"
```

### Utility Commands

```bash
# Score a site's design quality (A-F rating, 7 categories)
npx designlang score https://vercel.com

# Compare two sites side-by-side
npx designlang diff https://stripe.com https://paddle.com

# Compare N brands in a matrix
npx designlang brands stripe.com vercel.com github.com linear.app

# Apply extracted design directly to your project (auto-detects framework)
npx designlang apply https://stripe.com --dir ./my-app

# Generate a working Next.js starter with extracted design
npx designlang clone https://stripe.com

# Monitor a site for design changes hourly
npx designlang watch https://stripe.com --interval 60

# Sync local tokens with live site
npx designlang sync https://stripe.com --out ./src/tokens

# View design change history
npx designlang history https://stripe.com
```

## Output Files

Running `npx designlang https://stripe.com` produces:

| File | Purpose |
|------|---------|
| `stripe-com-design-language.md` | AI-optimized markdown with all 19 design sections |
| `stripe-com-preview.html` | Visual report with swatches, type scale, a11y score |
| `stripe-com-design-tokens.json` | W3C Design Tokens format |
| `stripe-com-tailwind.config.js` | Drop-in Tailwind CSS theme |
| `stripe-com-variables.css` | CSS custom properties |
| `stripe-com-figma-variables.json` | Figma Variables import (light + dark) |
| `stripe-com-theme.js` | React/CSS-in-JS theme (Chakra, Stitches, etc.) |
| `stripe-com-shadcn-theme.css` | shadcn/ui `globals.css` variables |

## Full CLI Reference

```bash
designlang <url> [options]

Options:
  -o, --out <dir>         Output directory (default: ./design-extract-output)
  -n, --name <name>       Output file prefix (default: derived from URL)
  -w, --width <px>        Viewport width (default: 1280)
      --height <px>       Viewport height (default: 800)
      --wait <ms>         Wait after page load for SPAs (default: 0)
      --dark              Also extract dark mode styles
      --depth <n>         Internal pages to crawl (default: 0)
      --screenshots       Capture component screenshots
      --responsive        Capture at multiple breakpoints
      --interactions      Capture hover/focus/active states
      --full              Enable all captures
      --cookie <val>      Cookie for auth pages (name=value, repeatable)
      --header <val>      Custom header (name:value, repeatable)
      --framework <type>  Only generate specific theme (react, shadcn)
      --no-history        Skip saving to history
      --verbose           Detailed progress output
```

## Common Patterns

### Pattern 1: Extract and apply to a Tailwind project

```bash
# Extract design tokens from a reference site
npx designlang https://linear.app --out ./design-tokens --name linear

# The generated tailwind.config.js can be merged into your project:
# ./design-tokens/linear-tailwind.config.js
```

Generated `tailwind.config.js` looks like:

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#5E6AD2',
        background: '#FFFFFF',
        surface: '#F7F8F9',
        // ... all extracted colors
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        xs: ['11px', { lineHeight: '16px' }],
        sm: ['13px', { lineHeight: '20px' }],
        base: ['15px', { lineHeight: '24px' }],
        // ... full type scale
      },
      borderRadius: {
        sm: '4px',
        md: '6px',
        lg: '8px',
        // ... extracted radii
      },
      boxShadow: {
        card: '0 1px 3px rgba(0,0,0,0.12)',
        // ... extracted shadows
      },
    },
  },
}
```

### Pattern 2: Feed the markdown to an LLM

```bash
# Extract the AI-optimized markdown
npx designlang https://stripe.com --out ./tokens

# Then use in a prompt:
cat ./tokens/stripe-com-design-language.md | \
  pbcopy  # macOS: copies to clipboard

# Or reference it directly in Claude/Cursor:
# "Use the design language in ./tokens/stripe-com-design-language.md
#  to style this component..."
```

### Pattern 3: Compare competitors

```bash
npx designlang brands stripe.com braintree.com paddle.com adyen.com

# Generates:
# brands.md  — markdown comparison matrix
# brands.html — visual side-by-side with color overlap analysis
```

### Pattern 4: Apply to a shadcn/ui project

```bash
# Auto-detect project structure and write to the right files
npx designlang apply https://stripe.com --dir ./my-nextjs-app

# Or manually use the generated shadcn theme:
# Copy stripe-com-shadcn-theme.css content into app/globals.css
```

Generated `shadcn-theme.css`:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 238 72% 57%;
    --primary-foreground: 210 40% 98%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --border: 214.3 31.8% 91.4%;
    --radius: 0.5rem;
    /* ... all extracted variables */
  }
}
```

### Pattern 5: W3C Design Tokens for tooling

```bash
npx designlang https://github.com --out ./tokens
```

Generated `design-tokens.json`:

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "color": {
    "primary": {
      "$value": "#0969da",
      "$type": "color"
    },
    "background": {
      "default": {
        "$value": "#ffffff",
        "$type": "color"
      }
    }
  },
  "typography": {
    "fontFamily": {
      "sans": {
        "$value": "-apple-system, BlinkMacSystemFont, 'Segoe UI'",
        "$type": "fontFamily"
      }
    }
  }
}
```

### Pattern 6: React theme object

```bash
npx designlang https://chakra-ui.com --out ./tokens
```

Generated `theme.js`:

```js
export const theme = {
  colors: {
    primary: '#319795',
    secondary: '#553C9A',
    // ...
  },
  fonts: {
    body: 'Inter, system-ui, sans-serif',
    heading: 'Inter, system-ui, sans-serif',
  },
  space: {
    1: '4px',
    2: '8px',
    4: '16px',
    8: '32px',
    // ...
  },
  radii: {
    sm: '4px',
    md: '6px',
    lg: '8px',
    full: '9999px',
  },
}
```

### Pattern 7: Monitor a design system for changes

```bash
# Check every 30 minutes, output to a dedicated folder
npx designlang watch https://vercel.com \
  --interval 30 \
  --out ./design-monitoring

# Useful in CI — run once and diff against stored baseline
npx designlang diff \
  https://vercel.com \
  ./design-monitoring/vercel-com-design-tokens.json
```

### Pattern 8: Clone a site's design as a Next.js starter

```bash
npx designlang clone https://stripe.com

# Creates ./cloned-design/ with:
# - Next.js app with extracted colors/fonts/spacing applied
# - tailwind.config.js pre-populated
# - globals.css with CSS variables
# - Basic component stubs styled to match

cd cloned-design
npm install
npm run dev
```

## What Gets Extracted

The markdown output covers **19 sections**:

1. **Color Palette** — all unique colors with usage context
2. **Typography** — font families, weights, sizes, line heights, letter spacing
3. **Spacing** — padding/margin/gap values used across the site
4. **Border Radii** — all radius values with component context
5. **Box Shadows** — elevation system
6. **CSS Custom Properties** — all `--var` declarations
7. **Breakpoints** — detected responsive breakpoints
8. **Transitions & Animations** — duration, easing, properties animated
9. **Component Patterns** — button, card, input, nav with full CSS snippets
10. **Layout System** — grid columns, flex patterns, container widths
11. **Responsive Design** — what changes across breakpoints (with `--responsive`)
12. **Interaction States** — hover/focus/active deltas (with `--interactions`)
13. **Accessibility** — WCAG 2.1 contrast scores for all fg/bg pairs
14. **Gradients** — type, direction, stops, classification
15. **Z-Index Map** — layer hierarchy, z-index wars detection
16. **SVG Icons** — deduplicated, size/style classified, color palette
17. **Font Files** — source (Google/self-hosted/CDN/system), `@font-face` CSS
18. **Image Style Patterns** — aspect ratios, filters, shape treatments
19. **Quick Start** — ready-to-use snippet to recreate the design

## Design Scoring

```bash
npx designlang score https://your-site.com
```

Scores 7 categories on a 0–100 scale with A-F grade:

- **Color Discipline** — palette size, harmony, usage consistency
- **Typography** — scale rationality, weight/size combinations
- **Spacing System** — whether spacing follows a scale
- **Shadows** — elevation system coherence
- **Border Radii** — consistency across components
- **Accessibility** — WCAG 2.1 contrast pass rate
- **Tokenization** — CSS custom property usage

## Troubleshooting

### Site loads blank or styles are missing

```bash
# Add wait time for JavaScript-heavy SPAs
npx designlang https://app.example.com --wait 3000

# Or use a higher viewport for desktop-only layouts
npx designlang https://example.com --width 1440 --height 900
```

### Authentication-protected pages

```bash
# Get your session cookie from browser DevTools → Application → Cookies
npx designlang https://app.example.com \
  --cookie "auth_token=$AUTH_TOKEN" \
  --cookie "csrf=$CSRF_TOKEN"
```

### Output files are too large

```bash
# Only generate a specific framework's theme
npx designlang https://stripe.com --framework react
npx designlang https://stripe.com --framework shadcn

# Single-page only (no depth crawling)
npx designlang https://stripe.com --depth 0
```

### Too many colors extracted (utility CSS sites)

```bash
# Limit to the main page at desktop viewport, no deep crawl
npx designlang https://tailwindcss.com \
  --depth 0 \
  --width 1280 \
  --no-history
```

### Playwright/browser not found

```bash
# Playwright needs browsers installed
npx playwright install chromium

# Or if installed globally:
npm install -g designlang
playwright install chromium
```

### `apply` command doesn't detect my framework

```bash
# Explicitly point to your project root with a tailwind config present
npx designlang apply https://stripe.com --dir ./my-app

# Ensure ./my-app contains tailwind.config.js or tailwind.config.ts
# for Tailwind detection, or components.json for shadcn detection
```

## Integration with AI Agents

The `-design-language.md` file is specifically structured for LLM consumption. Feed it directly to Claude, GPT-4, or Cursor to:

- Recreate UI components matching the extracted design
- Generate new components consistent with the design system
- Audit your own components against a reference design
- Document your own site's design system automatically

```bash
# Extract your own site's design language for agent context
npx designlang https://your-production-site.com \
  --out ./docs/design \
  --name my-app

# Reference in CLAUDE.md or .cursorrules:
# "When creating UI components, follow the design language
#  documented in ./docs/design/my-app-design-language.md"
```
