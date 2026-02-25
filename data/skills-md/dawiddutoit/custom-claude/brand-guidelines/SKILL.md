---
name: brand-guidelines
description: |
  Applies Anthropic's official brand identity including colors (Dark #141413, Light #faf9f5,
  Orange #d97757), typography (Poppins, Lora), and design standards to artifacts, presentations,
  documents, and web interfaces. Use when asked to "apply Anthropic branding", "use brand colors",
  "style with company guidelines", "add Anthropic look-and-feel", or "follow design standards".
  Provides official color palettes, font specifications, logo usage, and visual formatting rules.
  Works with HTML artifacts, presentations, PDFs, documents, and any visual deliverables requiring
  consistent brand identity.
license: Complete terms in LICENSE.txt
---

# Anthropic Brand Styling

## Overview

To access Anthropic's official brand identity and style resources, use this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, Anthropic brand, visual formatting, visual design

## When to Use This Skill

Use when asked to:
- Apply Anthropic's brand colors to artifacts or visualizations
- Style documents with Anthropic typography (Poppins, Lora fonts)
- Add corporate visual identity to presentations or outputs
- Format content with Anthropic's design standards
- Apply consistent branding across multiple artifacts

Do NOT use when:
- Content doesn't need Anthropic branding (generic styling is sufficient)
- User requests non-Anthropic brand guidelines
- Technical code output where branding is inappropriate

## Brand Guidelines

### Colors

**Main Colors:**

- Dark: `#141413` - Primary text and dark backgrounds
- Light: `#faf9f5` - Light backgrounds and text on dark
- Mid Gray: `#b0aea5` - Secondary elements
- Light Gray: `#e8e6dc` - Subtle backgrounds

**Accent Colors:**

- Orange: `#d97757` - Primary accent
- Blue: `#6a9bcc` - Secondary accent
- Green: `#788c5d` - Tertiary accent

### Typography

- **Headings**: Poppins (with Arial fallback)
- **Body Text**: Lora (with Georgia fallback)
- **Note**: Fonts should be pre-installed in your environment for best results

## Features

### Smart Font Application

- Applies Poppins font to headings (24pt and larger)
- Applies Lora font to body text
- Automatically falls back to Arial/Georgia if custom fonts unavailable
- Preserves readability across all systems

### Text Styling

- Headings (24pt+): Poppins font
- Body text: Lora font
- Smart color selection based on background
- Preserves text hierarchy and formatting

### Shape and Accent Colors

- Non-text shapes use accent colors
- Cycles through orange, blue, and green accents
- Maintains visual interest while staying on-brand

## Technical Details

### Font Management

- Uses system-installed Poppins and Lora fonts when available
- Provides automatic fallback to Arial (headings) and Georgia (body)
- No font installation required - works with existing system fonts
- For best results, pre-install Poppins and Lora fonts in your environment

### Color Application

- Uses RGB color values for precise brand matching
- Applied via python-pptx's RGBColor class
- Maintains color fidelity across different systems
