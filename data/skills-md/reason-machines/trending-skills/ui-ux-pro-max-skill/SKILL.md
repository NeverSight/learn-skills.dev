---
name: ui-ux-pro-max-skill
description: AI design intelligence skill for building professional UI/UX across multiple platforms with 161 reasoning rules, 67 styles, and automated design system generation
triggers:
  - "build a landing page"
  - "design a UI for"
  - "create a professional interface"
  - "what UI style should I use"
  - "generate a design system"
  - "help me with UI UX design"
  - "build a mobile UI"
  - "make my app look professional"
---

# UI UX Pro Max Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

UI UX Pro Max is an AI skill that injects design intelligence into coding agents — giving them 161 industry-specific reasoning rules, 67 UI styles, 57 font pairings, 161 color palettes, and pre-delivery checklists to produce professional, accessible, conversion-optimized interfaces on the first attempt.

## Installation

### Via CLI (Recommended)

```bash
# Install the CLI globally
npm install -g uipro-cli

# Add the skill to your project
npx uipro-cli install

# Or install globally
npx uipro-cli install --global
```

### Via Python (Direct)

```bash
# Clone the repository
git clone https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git
cd ui-ux-pro-max-skill

# Install dependencies
pip install -r requirements.txt

# Run the design system generator
python main.py
```

### Manual SKILL.md Integration

Copy the generated `SKILL.md` into your project root so agents like Claude Code, Cursor, Codex, or Windsurf automatically pick it up:

```bash
cp SKILL.md /your-project/SKILL.md
```

---

## Core Concepts

### Design System Generator

When you describe a product, the skill runs a multi-domain search across:

| Domain | Count | Purpose |
|--------|-------|---------|
| Reasoning Rules | 161 | Industry-specific layout/style decisions |
| UI Styles | 67 | Visual language (Glassmorphism, Brutalism, etc.) |
| Color Palettes | 161 | Industry-matched palettes |
| Font Pairings | 57 | Typography combinations |
| Landing Page Patterns | 24 | Conversion-optimized structures |

### Output: Complete Design System

Every generation produces:
- **Pattern** — Page structure (sections, CTA placement)
- **Style** — Visual language with keywords
- **Colors** — Primary, secondary, CTA, background, text
- **Typography** — Font pairing + Google Fonts URL
- **Key Effects** — Animations and interactions
- **Anti-Patterns** — What to avoid for this industry
- **Pre-Delivery Checklist** — Accessibility and UX gates

---

## Python API Usage

### Basic Design System Generation

```python
from uiuxpro import DesignSystemGenerator

# Initialize the generator
generator = DesignSystemGenerator()

# Generate a complete design system from a description
result = generator.generate(
    description="A landing page for a luxury beauty spa",
    stack="react",           # react | nextjs | astro | vue | html
    mode="light"             # light | dark | auto
)

print(result.pattern)        # Landing page structure
print(result.style)          # UI style recommendation
print(result.colors)         # Color palette dict
print(result.typography)     # Font pairing + import URL
print(result.effects)        # Animations and interactions
print(result.anti_patterns)  # What to avoid
print(result.checklist)      # Pre-delivery gates
```

### Query Reasoning Rules

```python
from uiuxpro import ReasoningEngine

engine = ReasoningEngine()

# Find rules for a product type
rules = engine.search("fintech payment app")
for rule in rules:
    print(rule.category)       # e.g. "Fintech/Crypto"
    print(rule.pattern)        # Recommended page pattern
    print(rule.style_priority) # Ordered list of styles
    print(rule.color_mood)     # Palette keywords
    print(rule.anti_patterns)  # e.g. ["playful fonts", "neon colors"]

# Get all rules for a category
all_healthcare = engine.get_by_category("Healthcare")
```

### Style Lookup

```python
from uiuxpro import StyleLibrary

styles = StyleLibrary()

# Get all 67 styles
all_styles = styles.list_all()

# Find styles by keyword
matching = styles.search("glass transparent blur")

# Get full style spec
glassmorphism = styles.get("Glassmorphism")
print(glassmorphism.keywords)       # ["frosted glass", "transparency", ...]
print(glassmorphism.best_for)       # ["SaaS dashboards", "tech products"]
print(glassmorphism.css_variables)  # CSS custom properties
print(glassmorphism.tailwind_config) # Tailwind configuration
```

### Color Palette Selection

```python
from uiuxpro import ColorEngine

colors = ColorEngine()

# Get palette for a product type
palette = colors.get_for_product("medical clinic")
print(palette.primary)     # "#2B7A9F"
print(palette.secondary)   # "#E8F4FD"
print(palette.cta)         # "#0066CC"
print(palette.background)  # "#FFFFFF"
print(palette.text)        # "#1A2B3C"
print(palette.notes)       # "Clinical trust with human warmth"

# Get palette by mood
calm_palettes = colors.get_by_mood("calming")
luxury_palettes = colors.get_by_mood("luxury")
```

### Typography Pairing

```python
from uiuxpro import TypographyEngine

typography = TypographyEngine()

# Get font pairing for a mood
pairing = typography.get_for_mood("elegant sophisticated")
print(pairing.heading)      # "Cormorant Garamond"
print(pairing.body)         # "Montserrat"
print(pairing.google_url)   # Google Fonts import URL
print(pairing.css_import)   # @import statement

# Get all pairings for a tech stack
react_pairings = typography.get_for_stack("react")
```

---

## CLI Commands

```bash
# Generate a design system interactively
npx uipro-cli generate

# Generate for a specific product type
npx uipro-cli generate --product "saas dashboard" --stack nextjs

# List all 67 UI styles
npx uipro-cli styles list

# Get style details
npx uipro-cli styles get glassmorphism

# Search reasoning rules
npx uipro-cli rules search "e-commerce luxury"

# List all color palettes
npx uipro-cli colors list

# Get font pairings
npx uipro-cli fonts list
npx uipro-cli fonts get --mood "tech modern"

# Output design system as JSON
npx uipro-cli generate --product "restaurant booking" --output json

# Output as markdown
npx uipro-cli generate --product "portfolio site" --output markdown
```

---

## Real-World Examples

### Example 1: React SaaS Dashboard

```python
from uiuxpro import DesignSystemGenerator

gen = DesignSystemGenerator()
ds = gen.generate(
    description="B2B SaaS analytics dashboard for enterprise teams",
    stack="react",
    tech_details={"component_library": "shadcn/ui", "css": "tailwindcss"}
)

# Result:
# Pattern:   "Data-First + Progressive Disclosure"
# Style:     "Glassmorphism" or "Bento Grid"
# Colors:    Primary #6366F1 (Indigo), CTA #8B5CF6 (Violet)
# Fonts:     Inter / Inter (unified, high legibility)
# Effects:   Subtle card shadows, smooth data transitions 200ms
# Avoid:     Decorative animations, overly complex gradients
```

Generated Tailwind config from `ds.tailwind_config`:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#6366F1',
          50: '#EEF2FF',
          500: '#6366F1',
          900: '#312E81',
        },
        cta: '#8B5CF6',
        surface: 'rgba(255,255,255,0.05)',
      },
      backdropBlur: {
        xs: '2px',
      },
      boxShadow: {
        glass: '0 8px 32px rgba(99,102,241,0.15)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
}
```

### Example 2: Wellness/Spa Landing Page

```python
ds = gen.generate(
    description="Luxury wellness spa booking and services landing page",
    stack="html",
    tech_details={"css": "tailwindcss"}
)

# Auto-generates the full CSS variables block:
print(ds.css_variables)
```

Output `ds.css_variables`:

```css
:root {
  /* Soft UI Evolution - Serenity Spa */
  --color-primary: #E8B4B8;      /* Soft Pink */
  --color-secondary: #A8D5BA;    /* Sage Green */
  --color-cta: #D4AF37;          /* Gold */
  --color-background: #FFF5F5;   /* Warm White */
  --color-text: #2D3436;         /* Charcoal */

  /* Typography */
  --font-heading: 'Cormorant Garamond', Georgia, serif;
  --font-body: 'Montserrat', system-ui, sans-serif;

  /* Effects */
  --shadow-soft: 6px 6px 12px #d1c4c5, -6px -6px 12px #ffffff;
  --transition-base: 200ms ease-in-out;
  --border-radius-organic: 20px 60px 30px 50px;
}
```

### Example 3: Fintech/Banking App

```python
ds = gen.generate(
    description="Personal finance tracker with budgeting and investment tracking",
    stack="react-native",
)

# Anti-patterns automatically flagged for finance:
print(ds.anti_patterns)
# [
#   "Playful rounded fonts (use geometric sans)",
#   "Bright neon colors (erode trust)",
#   "AI purple/pink gradients",
#   "Excessive animations on financial data",
#   "Gamification elements on serious financial actions"
# ]

print(ds.checklist)
# [
#   "✓ WCAG AA contrast on all number displays",
#   "✓ Currency formatted with locale awareness",
#   "✓ Error states are clear and actionable",
#   "✓ Loading states on all async operations",
#   "✓ Biometric auth UI integrated",
#   "✓ No emojis as primary icons — use Lucide or SF Symbols",
# ]
```

### Example 4: Full Stack Integration with Next.js

```python
from uiuxpro import DesignSystemGenerator, StackExporter

gen = DesignSystemGenerator()
ds = gen.generate(
    description="AI-powered recruitment platform for enterprise HR teams",
    stack="nextjs",
    tech_details={
        "component_library": "shadcn/ui",
        "css": "tailwindcss",
        "icons": "lucide-react"
    }
)

# Export as Next.js-ready files
exporter = StackExporter(ds, stack="nextjs")
exporter.write_all(output_dir="./src/design-system/")

# Generates:
# ./src/design-system/tokens.css        — CSS custom properties
# ./src/design-system/tailwind.config.js — Tailwind configuration
# ./src/design-system/typography.ts     — Font configuration
# ./src/design-system/colors.ts         — Color tokens as TypeScript
# ./src/design-system/README.md         — Design decisions + rationale
```

---

## Supported Tech Stacks

| Stack | Key | Notes |
|-------|-----|-------|
| React | `react` | Component patterns + Tailwind |
| Next.js | `nextjs` | App Router + RSC aware |
| Astro | `astro` | Island architecture patterns |
| Vue 3 | `vue` | Composition API patterns |
| Nuxt.js | `nuxt` | Auto-imports aware |
| Nuxt UI | `nuxt-ui` | Component overrides |
| Svelte | `svelte` | Reactive store patterns |
| SwiftUI | `swiftui` | iOS/macOS native patterns |
| React Native | `react-native` | Mobile-first responsive |
| Flutter | `flutter` | Widget tree patterns |
| HTML + Tailwind | `html` | Standalone CSS output |
| shadcn/ui | `shadcn` | Theme token overrides |
| Jetpack Compose | `jetpack` | Android Material3 |

---

## Pre-Delivery Checklist (Universal)

The skill enforces these gates on every generated design:

```
ACCESSIBILITY
[ ] No emojis as icons — use SVG (Heroicons / Lucide / Phosphor)
[ ] cursor-pointer on all clickable elements
[ ] Hover states with smooth transitions (150–300ms)
[ ] Light mode: text contrast ratio 4.5:1 minimum
[ ] Dark mode: text contrast ratio 4.5:1 minimum
[ ] Focus states visible for keyboard navigation
[ ] prefers-reduced-motion respected
[ ] ARIA labels on icon-only buttons

RESPONSIVE
[ ] Mobile: 375px breakpoint tested
[ ] Tablet: 768px breakpoint tested
[ ] Desktop: 1024px breakpoint tested
[ ] Wide: 1440px breakpoint tested

PERFORMANCE
[ ] Images use next-gen formats (WebP / AVIF)
[ ] Fonts loaded with font-display: swap
[ ] No layout shift on font load (reserve space)
[ ] Animations use transform/opacity only (no layout props)

INTERACTION
[ ] Loading states on all async actions
[ ] Error states are clear and actionable
[ ] Empty states are designed (not blank)
[ ] Success feedback on form submissions
```

---

## Common Patterns by Industry

### Tech / SaaS
- **Style**: Glassmorphism, Bento Grid, AI-Native UI
- **Colors**: Indigo/Violet primary, dark backgrounds for dashboards
- **Avoid**: Stock photos, clip art, rainbow gradients

### E-commerce / Luxury
- **Style**: Minimalism, Editorial, Claymorphism (for casual)
- **Colors**: Black/Gold for luxury; bright/bold for casual
- **Avoid**: Cluttered layouts, too many CTAs, Comic Sans adjacent fonts

### Healthcare / Medical
- **Style**: Clean Minimalism, Soft UI
- **Colors**: Blues, teals, whites — clinical but warm
- **Avoid**: Red for primary actions (emergency connotation), dark mode on medical data

### Finance / Fintech
- **Style**: Professional Minimalism, Data-Dense UI
- **Colors**: Deep blues, greens, neutrals
- **Avoid**: Playful fonts, neon colors, AI purple gradients, excessive motion

### Food & Restaurant
- **Style**: Warm Minimalism, Photography-Forward
- **Colors**: Warm neutrals, appetizing reds/oranges, earthy tones
- **Avoid**: Cold blues as primary, low-contrast text over food photos

---

## Troubleshooting

### CLI not found after install
```bash
# Ensure npm global bin is in PATH
export PATH="$(npm bin -g):$PATH"

# Or use npx directly
npx uipro-cli generate
```

### Python import errors
```bash
# Ensure you're in the project directory with venv active
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Generation returns generic output
- Be specific in your description: include industry, audience, and goal
- ✗ `"a website"` → ✓ `"a SaaS landing page for a B2B project management tool targeting remote engineering teams"`
- Include stack context for framework-specific exports

### No matching reasoning rule found
```python
# The engine falls back to closest category match
# Inspect the match score to verify
result = engine.search("autonomous drone delivery fleet")
print(result[0].score)      # BM25 relevance score
print(result[0].category)   # Matched category
print(result[0].fallback)   # True if approximate match
```

### Tailwind config conflicts with existing config
```python
# Get only the theme extension, not the full config
theme_extension = ds.tailwind_theme_extension  # dict, not full config

# Merge manually into your existing tailwind.config.js
import json
print(json.dumps(theme_extension, indent=2))
```

---

## Resources

- **Homepage**: https://uupm.cc
- **GitHub**: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- **npm CLI**: https://www.npmjs.com/package/uipro-cli
- **License**: MIT
