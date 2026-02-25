---
name: gemini-visual
description: Visual and front-end development assistant powered by Google Gemini 3. Use for UI analysis, design comparison, accessibility audits, color palette extraction, screenshot-to-code conversion, generating UI assets, and text-based design assistance from briefs.
---

# Gemini Visual - Front-End & Visual Development Assistant

## Overview

A comprehensive toolkit leveraging Google Gemini 3's advanced visual reasoning capabilities for front-end development and design tasks. Gemini 3 provides state-of-the-art multimodal understanding with spatial reasoning, document understanding, and high-resolution image processing.

## When to Use

- **UI/UX Analysis**: Analyze screenshots for layout issues, visual hierarchy, and design patterns
- **Accessibility Audits**: Check contrast ratios, text readability, and WCAG compliance
- **Design Comparison**: Compare mockups, before/after screenshots, or different design variations
- **Color Palette Extraction**: Extract colors from images with HEX, RGB, and HSL values
- **Screenshot to Code**: Generate HTML/CSS from design screenshots
- **UI Asset Generation**: Create icons, backgrounds, gradients, and UI graphics
- **Responsive Design Review**: Analyze multi-device screenshots for consistency
- **Visual Debugging**: Identify rendering issues, broken layouts, or visual bugs
- **Design from Brief**: Generate designs, code, and components from text descriptions
- **Interactive Design Sessions**: Multi-turn conversations for iterative design refinement

## Prerequisites

- Python 3.9+
- `google-genai` package
- `GEMINI_API_KEY` environment variable

## Installation

```bash
pip install google-genai
```

### Getting an API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and set it as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key"
```

Add to your shell profile (`~/.zshrc` or `~/.bashrc`) for persistence:

```bash
echo 'export GEMINI_API_KEY="your-api-key"' >> ~/.zshrc
```

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `analyze_ui.py` | Analyze UI screenshots for issues, patterns, and suggestions |
| `generate_ui_assets.py` | Generate icons, backgrounds, and UI graphics |
| `compare_designs.py` | Compare two designs and highlight differences |
| `extract_colors.py` | Extract color palettes from images |
| `screenshot_to_code.py` | Convert screenshots to HTML/CSS code |
| `design_from_brief.py` | Generate designs and code from text briefs (no image required) |

## Available Models

| Model | Best For | Context |
|-------|----------|---------|
| `gemini-3-pro-preview` | Visual analysis, code generation, complex reasoning | 1M input, 64k output |
| `gemini-3-pro-image-preview` | Asset generation, image editing | 65k input, 32k output |

## Media Resolution Options

Control token usage and detail level with `--resolution`:

| Resolution | Tokens/Image | Best For |
|------------|--------------|----------|
| `low` | 70 | Quick scans, thumbnails |
| `medium` | 560 | Standard screenshots, OCR |
| `high` | 1120 | Detailed UI analysis |
| `ultra_high` | 2240+ | Fine text, complex layouts |

---

## Script Reference

### 1. analyze_ui.py - UI Analysis

Analyze UI screenshots for design issues, accessibility problems, and improvement suggestions.

```
python scripts/analyze_ui.py [options] IMAGE

Required:
  IMAGE                    Path to UI screenshot to analyze

Options:
  -m, --mode MODE          Analysis mode (default: comprehensive)
                           Modes: comprehensive, accessibility, layout, ux
  -r, --resolution RES     Media resolution (default: high)
  -o, --output FILE        Save analysis to file (JSON or text)
  -f, --format FORMAT      Output format: text, json, markdown (default: text)
  --thinking LEVEL         Thinking level: low, high (default: high)
  -v, --verbose            Show detailed progress
```

**Examples:**

```bash
# Comprehensive UI analysis
python scripts/analyze_ui.py screenshot.png

# Accessibility-focused analysis
python scripts/analyze_ui.py -m accessibility app_screen.png

# Layout analysis with JSON output
python scripts/analyze_ui.py -m layout -f json -o report.json mockup.png

# Quick UX review
python scripts/analyze_ui.py -m ux --thinking low mobile_app.png
```

**Analysis Modes:**

- **comprehensive**: Full analysis including layout, colors, typography, accessibility, and UX
- **accessibility**: WCAG compliance, contrast ratios, screen reader compatibility, touch targets
- **layout**: Visual hierarchy, spacing, alignment, responsive issues
- **ux**: User flow, affordances, cognitive load, interaction patterns

---

### 2. generate_ui_assets.py - Asset Generation

Generate UI assets like icons, backgrounds, patterns, and graphics.

```
python scripts/generate_ui_assets.py [options]

Required:
  -p, --prompt TEXT        Description of asset to generate

Options:
  -t, --type TYPE          Asset type (default: icon)
                           Types: icon, background, pattern, illustration, badge
  -s, --style STYLE        Design style (default: modern)
                           Styles: modern, minimal, flat, gradient, glassmorphism,
                                   neumorphism, material, ios, outlined
  -c, --colors COLORS      Color palette (comma-separated HEX or names)
  -a, --aspect-ratio RATIO Aspect ratio (default: 1:1)
  --size SIZE              Resolution: 1K, 2K, 4K (default: 1K)
  -o, --output FILE        Output file path
  -r, --reference IMAGE    Reference image for style guidance
  -v, --verbose            Show detailed progress
```

**Examples:**

```bash
# Generate app icon
python scripts/generate_ui_assets.py -p "Weather app icon with sun and clouds" -t icon

# Create gradient background
python scripts/generate_ui_assets.py -p "Soft gradient for login screen" -t background \
  -c "#667eea,#764ba2" -a 9:16 -o login_bg.png

# Generate pattern for UI
python scripts/generate_ui_assets.py -p "Subtle geometric pattern for card backgrounds" \
  -t pattern -s minimal -o pattern.png

# Create illustration from reference
python scripts/generate_ui_assets.py -p "Onboarding illustration, person using phone" \
  -t illustration -r brand_style.png -o onboarding.png

# Generate badge/label
python scripts/generate_ui_assets.py -p "Premium badge with star" -t badge \
  -c "gold,white" -s gradient
```

---

### 3. compare_designs.py - Design Comparison

Compare two design screenshots and analyze differences.

```
python scripts/compare_designs.py [options] IMAGE1 IMAGE2

Required:
  IMAGE1                   First design image (before/version A)
  IMAGE2                   Second design image (after/version B)

Options:
  -m, --mode MODE          Comparison mode (default: full)
                           Modes: full, visual, content, accessibility
  -f, --format FORMAT      Output format: text, json, markdown (default: text)
  -o, --output FILE        Save comparison to file
  -r, --resolution RES     Media resolution (default: high)
  -v, --verbose            Show detailed progress
```

**Examples:**

```bash
# Full design comparison
python scripts/compare_designs.py before.png after.png

# Visual-only comparison
python scripts/compare_designs.py -m visual old_design.png new_design.png

# Compare for accessibility changes
python scripts/compare_designs.py -m accessibility v1.png v2.png -o report.md

# A/B test comparison as JSON
python scripts/compare_designs.py -m full variant_a.png variant_b.png -f json
```

**Comparison Modes:**

- **full**: Comprehensive comparison of all visual and functional aspects
- **visual**: Focus on colors, typography, spacing, visual hierarchy
- **content**: Text changes, layout shifts, information architecture
- **accessibility**: Contrast, readability, touch targets, WCAG compliance changes

---

### 4. extract_colors.py - Color Palette Extraction

Extract color palettes from images with multiple output formats.

```
python scripts/extract_colors.py [options] IMAGE

Required:
  IMAGE                    Image to extract colors from

Options:
  -n, --count COUNT        Number of colors to extract (default: 6)
  -f, --format FORMAT      Output format: text, json, css, tailwind, scss (default: text)
  -o, --output FILE        Save palette to file
  --named                  Include closest CSS color names
  --contrast               Calculate contrast ratios between colors
  -v, --verbose            Show detailed progress
```

**Examples:**

```bash
# Extract 6 main colors
python scripts/extract_colors.py screenshot.png

# Extract palette as CSS variables
python scripts/extract_colors.py -f css -o colors.css brand_image.png

# Get Tailwind config
python scripts/extract_colors.py -f tailwind -o tailwind.config.js design.png

# Detailed palette with contrast info
python scripts/extract_colors.py -n 8 --named --contrast hero_image.jpg

# SCSS variables output
python scripts/extract_colors.py -f scss -o _colors.scss mockup.png
```

---

### 5. screenshot_to_code.py - Screenshot to Code

Convert UI screenshots to HTML/CSS code.

```
python scripts/screenshot_to_code.py [options] IMAGE

Required:
  IMAGE                    UI screenshot to convert

Options:
  -f, --framework FRAME    CSS framework (default: tailwind)
                           Frameworks: tailwind, css, bootstrap, vanilla
  -c, --components         Extract as reusable components
  --responsive             Generate responsive code
  -o, --output DIR         Output directory for files
  -r, --resolution RES     Media resolution (default: ultra_high)
  --thinking LEVEL         Thinking level: low, high (default: high)
  -v, --verbose            Show detailed progress
```

**Examples:**

```bash
# Convert to Tailwind HTML
python scripts/screenshot_to_code.py landing_page.png

# Generate vanilla CSS
python scripts/screenshot_to_code.py -f vanilla -o ./output mockup.png

# Create responsive Bootstrap components
python scripts/screenshot_to_code.py -f bootstrap -c --responsive card.png

# Full page conversion with components
python scripts/screenshot_to_code.py -f tailwind -c --responsive -o ./components page.png
```

---

### 6. design_from_brief.py - Text-Based Design Assistant

Generate frontend designs, code, and components from text descriptions without needing visual input.

```
python scripts/design_from_brief.py [options]

Input (one required):
  -p, --prompt TEXT      Design brief or prompt text
  -b, --brief-file FILE  Read brief from a file
  --interactive          Start interactive design session

Options:
  -m, --mode MODE        Generation mode (default: code)
                         Modes: design, code, component, review, brainstorm
  -fw, --framework FW    Framework for code generation (default: tailwind)
                         Frameworks: tailwind, css, bootstrap, react, vue, svelte, vanilla
  -c, --context TEXT     Additional context (existing code, constraints)
  -f, --format FORMAT    Output format: text, json, markdown (default: text)
  -o, --output FILE      Save output to file
  -v, --verbose          Show detailed progress
```

**Examples:**

```bash
# Generate code from a brief
python scripts/design_from_brief.py -p "Create a pricing table with 3 tiers" -m code -fw tailwind

# Get design advice and guidance
python scripts/design_from_brief.py -p "Design a modern SaaS landing page" -m design

# Generate a React component
python scripts/design_from_brief.py -p "A toggle switch with smooth animation" -m component -fw react

# Review a design idea
python scripts/design_from_brief.py -p "Is a hamburger menu good for desktop navigation?" -m review

# Brainstorm creative ideas
python scripts/design_from_brief.py -p "Ideas for a fitness app dashboard" -m brainstorm

# Read brief from file
python scripts/design_from_brief.py -b project_brief.txt -m code -fw vue

# Interactive multi-turn session
python scripts/design_from_brief.py --interactive -m code -fw tailwind
```

**Generation Modes:**

- **design**: Get design guidance including colors, typography, layout, and UX recommendations
- **code**: Generate complete, production-ready frontend code
- **component**: Design and code reusable UI components with props and variants
- **review**: Get feedback and recommendations on design ideas or code
- **brainstorm**: Generate creative ideas and multiple design directions

**Supported Frameworks:**

| Framework | Description |
|-----------|-------------|
| `tailwind` | Tailwind CSS utility classes |
| `css` | Custom CSS with variables and BEM |
| `bootstrap` | Bootstrap 5 components |
| `react` | React functional components with TypeScript |
| `vue` | Vue 3 Composition API with TypeScript |
| `svelte` | Svelte components |
| `vanilla` | Plain HTML/CSS/JavaScript |

**Interactive Session Commands:**

When using `--interactive`, you can use these commands:

| Command | Description |
|---------|-------------|
| `/mode <mode>` | Change generation mode |
| `/framework <fw>` | Change framework |
| `/save <file>` | Save last response to file |
| `/clear` | Clear conversation history |
| `/quit` | Exit session |

---

## Use Cases

### Front-End Development Workflow

```bash
# 1. Analyze a design mockup
python scripts/analyze_ui.py mockup.png -f markdown -o analysis.md

# 2. Extract brand colors
python scripts/extract_colors.py mockup.png -f tailwind -o colors.js

# 3. Generate code from screenshot
python scripts/screenshot_to_code.py mockup.png -f tailwind -c -o ./src

# 4. Generate placeholder icons
python scripts/generate_ui_assets.py -p "Settings gear icon" -t icon -s outlined
```

### Design Review Process

```bash
# Compare design iterations
python scripts/compare_designs.py v1.png v2.png -f markdown -o review.md

# Check accessibility
python scripts/analyze_ui.py final_design.png -m accessibility -o a11y_report.json
```

### Asset Production Pipeline

```bash
# Generate icon set
for icon in "home" "search" "profile" "settings"; do
  python scripts/generate_ui_assets.py -p "${icon} icon" -t icon -s outlined -o icons/${icon}.png
done

# Generate backgrounds for different screens
python scripts/generate_ui_assets.py -p "Auth screen gradient" -t background -a 9:16 -o bg_auth.png
python scripts/generate_ui_assets.py -p "Dashboard header" -t background -a 21:9 -o bg_header.png
```

### Design from Text Brief

```bash
# Start with design exploration
python scripts/design_from_brief.py -p "E-commerce product page for sneakers" -m design -o design_spec.md

# Generate the code
python scripts/design_from_brief.py -p "E-commerce product page with image gallery,
size selector, add to cart button, and reviews section" -m code -fw react -o product_page.tsx

# Create reusable components
python scripts/design_from_brief.py -p "Star rating component, 1-5 stars,
supports half stars, shows count" -m component -fw react

# Interactive refinement session
python scripts/design_from_brief.py --interactive -m code -fw tailwind
# Then iterate: "Add a sticky header", "Make the CTA more prominent", etc.
```

### Full Project Workflow (No Images Needed)

```bash
# 1. Brainstorm ideas
python scripts/design_from_brief.py -p "Modern dashboard for analytics SaaS" -m brainstorm

# 2. Get detailed design spec
python scripts/design_from_brief.py -p "Analytics dashboard with sidebar nav,
KPI cards, charts, and data tables" -m design -f markdown -o design.md

# 3. Generate components
python scripts/design_from_brief.py -p "KPI card showing metric, trend, and sparkline" \
  -m component -fw react -o components/KPICard.tsx

python scripts/design_from_brief.py -p "Data table with sorting, filtering, pagination" \
  -m component -fw react -o components/DataTable.tsx

# 4. Generate full page layout
python scripts/design_from_brief.py -p "Dashboard layout combining sidebar, header,
and main content area with the KPI cards and data table" -m code -fw react
```

---

## API Capabilities Summary

### Gemini 3 Visual Features

- **Spatial Reasoning**: Understands element positioning, alignment, and relationships
- **Document Understanding**: OCR, text extraction, layout parsing
- **High Resolution**: Up to ultra-high resolution for fine details and small text
- **Multi-Image Input**: Compare up to 3,600 images per request
- **Thought Signatures**: Maintains reasoning context for multi-turn editing

### Image Support

- **Input Formats**: PNG, JPEG, WebP, HEIC, HEIF
- **Max File Size**: 20MB inline, larger via File API
- **Output Formats**: PNG (generated images)
- **Resolutions**: 1K, 2K, 4K (generation), configurable input resolution

---

## Troubleshooting

### "GEMINI_API_KEY environment variable not set"

Set your API key:
```bash
export GEMINI_API_KEY="your-api-key"
```

### "Rate limit exceeded"

Wait a few minutes and retry. For batch operations, add delays between requests.

### Low quality analysis

Use higher resolution:
```bash
python scripts/analyze_ui.py -r ultra_high screenshot.png
```

### Missing fine details

For detailed UI analysis, use ultra_high resolution:
```bash
python scripts/analyze_ui.py -r ultra_high -m comprehensive app.png
```

### Code generation issues

Use high thinking level and ultra_high resolution:
```bash
python scripts/screenshot_to_code.py --thinking high -r ultra_high mockup.png
```

### Asset generation blocked by content moderation

If you see "No image content returned. The request may have been blocked by content moderation", try:
- Simplifying or rephrasing your prompt
- Removing specific brand names or copyrighted references
- Using more generic descriptions

This is a safety filter from the Gemini API and not all prompts will be accepted.

### Resolution affects token usage

The `--resolution` parameter controls how many tokens are used for image processing:
- `low`: ~70 tokens/image - Quick scans, thumbnails
- `medium`: ~560 tokens/image - Standard screenshots, OCR
- `high`: ~1120 tokens/image - Detailed UI analysis (default)

Higher resolution provides better accuracy but uses more tokens.

---

## Best Practices

1. **Use appropriate resolution**: Higher resolution = more tokens but better accuracy
2. **Match model to task**: Use `gemini-3-pro-preview` for analysis, `gemini-3-pro-image-preview` for generation
3. **Provide context**: Add relevant details to prompts for better results
4. **Iterate on assets**: Use multi-turn conversations for refinement
5. **Combine scripts**: Use extraction + generation for consistent design systems
6. **Save outputs**: Use `-o` flag to save reports for documentation
7. **Batch similar tasks**: Process multiple similar items together for efficiency

## Sources

- [Gemini 3 Developer Guide](https://ai.google.dev/gemini-api/docs/gemini-3)
- [Image Understanding](https://ai.google.dev/gemini-api/docs/image-understanding)
- [Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Google Developers Blog - Gemini 3](https://developers.googleblog.com/new-gemini-api-updates-for-gemini-3/)
