---
name: saas-ui-master
description: "Comprehensive UI/UX design intelligence combining a 4-Layer SaaS Master Guide with a robust CLI search system. 50 styles, 97 palettes, 57 font pairings, 25 chart types, 9 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, mobile app. Topics: 4-layer color palette, OKLCH theming, layout, typography, font pairing, accessibility, animation, hover, dark mode contrast."
---

# UI/UX Pro Max - SaaS Design Intelligence

Comprehensive design guide for web and mobile applications, specifically optimized for production-ready SaaS products. Contains 50+ styles, 97 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types across 9 technology stacks. Searchable database with priority-based recommendations, strictly enforcing professional design standards to prevent amateur, "vibe-coded" interfaces.

## When to Apply

Reference these guidelines when:
- Designing new UI components, pages, or complex SaaS dashboards
- Choosing color palettes (especially defining 4-layer systems and dark mode) and typography
- Reviewing code for UX, layout, or accessibility issues
- Building landing pages that require high conversion trust
- Implementing theming engines using modern color spaces (OKLCH)

## Rule Categories by Priority

| Priority | Category | Impact | Domain |
|----------|----------|--------|--------|
| 1 | Accessibility | CRITICAL | `ux` |
| 2 | Touch & Interaction | CRITICAL | `ux` |
| 3 | Layout & Architecture | HIGH | `ux`, `product` |
| 4 | Performance | HIGH | `ux` |
| 5 | Typography & 4-Layer Color | MEDIUM | `typography`, `color` |
| 6 | Animation | MEDIUM | `ux` |
| 7 | Style Selection | MEDIUM | `style`, `product` |
| 8 | Charts & Data | LOW | `chart` |

## Quick Reference: Core SaaS Philosophy

### 1. Component Architecture (HIGH)
- **Consolidate Navigation:** Group administrative links (Settings, Billing, Profile, API Keys, Logout) into a unified Account Popover menu rather than cluttering the main sidebar.
- **Clean Lists/Tables:** Hide secondary row actions (Edit, Delete, Duplicate) behind a clean ellipsis (three-dot) menu.
- **Modals for Focus:** Use centered modals with collapsed advanced options for simple forms. Never use empty, full-height flyout menus.

### 2. The 4-Layer Color System (MEDIUM)
- **Layer 1 (Neutral Foundation):** Never use pure white (`#FFFFFF`) as the app background. Use off-white/light gray (`bg-slate-50`). Surface interactive cards as pure white to pop. Use ultra-faint borders (85% white) or subtle drop shadows.
- **Layer 2 (Functional Accents):** Generate a scale from 50 to 950. Main buttons = 500/600, Hover = 700, Text links = 400/500.
- **Layer 3 (Semantic Communication):** Success = Green, Warning = Yellow/Orange, Destructive = Red. Use OKLCH color space for charts to keep lightness/chroma constant.
- **Layer 4 (Theming Engine):** Generate programmatic themes using OKLCH math: convert neutral hex to OKLCH, drop lightness `-0.03`, increase chroma `+0.02`, and slide the Hue value.

### 3. Dark Mode Rules (CRITICAL)
- **Double the Distance:** Dark colors bleed together. If light mode backgrounds step up by 2% lightness, dark mode MUST step up by 4% to 6%.
- **Shift Accents Lighter:** Shift primary brand colors to the 300 or 400 range for buttons/active states to ensure legibility.

---

## How to Use

Search specific domains using the CLI tool below.

### Prerequisites

Check if Python is installed:

```bash
python3 --version || python --version

```

If Python is not installed, install it based on the user's OS:

**macOS:**

```bash
brew install python3

```

**Ubuntu/Debian:**

```bash
sudo apt update && sudo apt install python3

```

**Windows:**

```powershell
winget install Python.Python.3.12

```

---

## Workflow Instructions

When a user requests UI/UX work (design, build, create, implement, review, fix, improve), follow this workflow:

### Step 1: Analyze User Requirements

Extract key information from the user request:

* **Product type**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
* **Style keywords**: minimal, playful, professional, elegant, dark mode, etc.
* **Industry**: healthcare, fintech, gaming, education, etc.
* **Stack**: React, Vue, Next.js, or default to `html-tailwind`

### Step 2: Generate Design System (REQUIRED)

**Always start with `--design-system**` to get comprehensive recommendations with reasoning:

```bash
python3 skills/saas-ui-master/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]

```

This command:

1. Searches 5 domains in parallel (product, style, color, landing, typography)
2. Applies reasoning rules from `ui-reasoning.csv` to select best matches
3. Returns complete design system: pattern, style, colors, typography, effects
4. Includes anti-patterns to avoid

### Step 2b: Persist Design System (Master + Overrides Pattern)

To save the design system for **hierarchical retrieval across sessions**, add `--persist`:

```bash
python3 skills/saas-ui-master/scripts/search.py "<query>" --design-system --persist -p "Project Name"

```

This creates:

* `design-system/MASTER.md` — Global Source of Truth with all design rules
* `design-system/pages/` — Folder for page-specific overrides

**With page-specific override:**

```bash
python3 skills/saas-ui-master/scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"

```

**How hierarchical retrieval works:**

1. When building a specific page (e.g., "Checkout"), first check `design-system/pages/checkout.md`
2. If the page file exists, its rules **override** the Master file
3. If not, use `design-system/MASTER.md` exclusively

### Step 3: Supplement with Detailed Searches (as needed)

After getting the design system, use domain searches to get additional details:

```bash
python3 skills/saas-ui-master/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]

```

**When to use detailed searches:**

| Need | Domain | Example |
| --- | --- | --- |
| More style options | `style` | `--domain style "glassmorphism dark"` |
| Chart recommendations | `chart` | `--domain chart "real-time dashboard"` |
| UX best practices | `ux` | `--domain ux "animation accessibility"` |
| Alternative fonts | `typography` | `--domain typography "elegant luxury"` |
| Landing structure | `landing` | `--domain landing "hero social-proof"` |

### Step 4: Stack Guidelines (Default: html-tailwind)

Get implementation-specific best practices. If the user doesn't specify a stack, **default to `html-tailwind**`.

```bash
python3 skills/saas-ui-master/scripts/search.py "<keyword>" --stack html-tailwind

```

Available stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

---

## Search Reference

### Available Domains

| Domain | Use For |
| --- | --- |
| `product` | Product type recommendations (SaaS, e-commerce, portfolio) |
| `style` | UI styles, colors, effects (glassmorphism, minimalism) |
| `typography` | Font pairings, Google Fonts |
| `color` | Color palettes by product type |
| `landing` | Page structure, CTA strategies (hero, pricing, social-proof) |
| `chart` | Chart types, library recommendations |
| `ux` | Best practices, anti-patterns (animation, accessibility) |
| `prompt` | AI prompts, CSS keywords |

---

## Output Formats & Tips

The `--design-system` flag supports two output formats:

```bash
# ASCII box (default) - best for terminal display
python3 skills/saas-ui-master/scripts/search.py "fintech crypto" --design-system

# Markdown - best for documentation
python3 skills/saas-ui-master/scripts/search.py "fintech crypto" --design-system -f markdown

```

**Tips for Better Results:**

1. **Be specific** - "healthcare SaaS dashboard" > "app"
2. **Combine domains** - Style + Typography + Color = Complete design system
3. **Always check UX** - Search "animation", "z-index", "accessibility" for common issues

---

## Common Rules for Professional UI

These are frequently overlooked issues that make UI look unprofessional:

### Icons & Visual Elements

| Rule | Do | Don't |
| --- | --- | --- |
| **No emoji icons** | Use SVG icons (Heroicons, Lucide, Phosphor) | Use emojis like 🎨 🚀 ⚙️ as UI icons |
| **Stable hover states** | Use color/opacity transitions on hover | Use scale transforms that shift layout |
| **Correct brand logos** | Research official SVG from Simple Icons | Guess or use incorrect logo paths |
| **Consistent icon sizing** | Use fixed viewBox (24x24) with w-6 h-6 | Mix different icon sizes randomly |

### Typography & Component Layout

| Rule | Do | Don't |
| --- | --- | --- |
| **Text Hierarchy** | Use shades for hierarchy (slate-900, 700, 500) | Rely solely on font-weight (bold/normal) |
| **Action Consolidation** | Group settings/logout into an Account Popover | Leave administrative links loose in the sidebar |
| **Table Actions** | Collapse row actions into an ellipsis menu | Show 3+ icon buttons on every single row |
| **Form Modals** | Use centered modals for simple creation flows | Use full-height, mostly empty flyout sidebars |

### Interaction & Cursor

| Rule | Do | Don't |
| --- | --- | --- |
| **Cursor pointer** | Add `cursor-pointer` to all clickable cards | Leave default cursor on interactive elements |
| **Hover feedback** | Provide visual feedback (color, shadow) | No indication element is interactive |
| **Smooth transitions** | Use `transition-colors duration-200` | Instant state changes or too slow (>500ms) |

### Light/Dark Mode Contrast

| Rule | Do | Don't |
| --- | --- | --- |
| **Base Background** | Use off-white/slate-50 for app background | Use pure `#FFFFFF` as the main app background |
| **Dark Mode Spacing** | Double contrast distance (4-6% steps) | Use the exact same lightness steps as light mode |
| **Dark Mode Accents** | Shift brand buttons to 300/400 range | Keep dark mode buttons the same dark shade |
| **Border visibility** | Use `border-gray-200` or subtle shadows | Use harsh, thick black borders |

---

## Pre-Delivery Checklist

Before delivering UI code, verify these items:

### Visual Quality & Architecture

* [ ] No emojis used as icons; SVG set utilized (Heroicons/Lucide).
* [ ] Navigation is consolidated (Account Popovers used instead of flat lists).
* [ ] Table/List row actions are tucked behind an ellipsis menu.
* [ ] Pure white (`#FFFFFF`) is NOT used as the base app background.
* [ ] Borders use ultra-faint shades/shadows, not harsh black lines.

### Interaction

* [ ] All clickable elements have `cursor-pointer`.
* [ ] Hover states provide clear visual feedback without shifting layouts.
* [ ] Transitions are smooth (150-300ms).
* [ ] Focus states are visible for keyboard navigation.

### Light/Dark Mode

* [ ] Light mode text meets 4.5:1 contrast ratio (`#0F172A` for primary).
* [ ] Glass/transparent elements are visible in light mode.
* [ ] Dark mode backgrounds have doubled contrast distances (4-6% steps).
* [ ] Dark mode accents are shifted lighter (300/400 range) for legibility.
* [ ] Test both modes before delivery.

### Accessibility & Layout

* [ ] Floating elements have proper spacing from edges (`top-4 left-4`).
* [ ] All images have descriptive alt text.
* [ ] Form inputs have properly linked labels.
* [ ] Color is not the only indicator of status.
* [ ] Responsive at 375px, 768px, 1024px, 1440px without horizontal scroll on mobile.

### Credits & Attribution

The underlying CLI search engine, Python scripts (`search.py`), and foundational data arrays in this skill were originally created by **nextlevelbuilder**. This skill builds upon their excellent technical framework by injecting a strict, 4-Layer SaaS UI/UX Design philosophy.
