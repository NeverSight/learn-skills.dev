---
name: brand-designer
description: |
  Creates cohesive brand identities including logos, color palettes, typography systems, and brand guidelines documents. Generates SVG logo components with variants, configures Tailwind color tokens, builds type scales, and produces social media and business card templates.

  Use when designing a logo, building a color palette, setting up typography systems, creating brand guidelines, generating social media templates, or organizing brand asset files. Use for branding, visual identity, logo design, brand guidelines, color systems.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# Brand Designer

## Overview

Brand Designer creates complete visual identity systems from discovery through asset delivery. It covers logo design with SVG components, color palette generation with accessibility compliance, typography scale configuration, brand guidelines documentation, and template creation for social media and print collateral.

**When to use:** New brand identity projects, logo design with SVG variants, color palette creation with Tailwind integration, typography system setup, brand guidelines documentation, social media template generation, brand asset file organization.

**When NOT to use:** UI component library design (use `design-system`), image optimization pipelines (use `asset-manager`), Figma-to-code workflows (use `figma-developer`), marketing copy or content strategy.

## Quick Reference

| Pattern            | Approach                                        | Key Points                                    |
| ------------------ | ----------------------------------------------- | --------------------------------------------- |
| Logo design        | SVG component with full/icon/wordmark variants  | Design monochrome first, then add color       |
| Color palette      | Primary, secondary, neutral, semantic layers    | 60/30/10 rule: neutral/primary/accent         |
| Typography system  | Display + body font pair with CSS custom props  | Maximum two font families                     |
| Brand guidelines   | Logo usage, colors, typography, voice and tone  | Include clear space rules and minimum sizes   |
| Social templates   | SVG templates at platform-specific dimensions   | 1200x630 for Open Graph, 400x400 for profiles |
| Asset organization | Structured directories: logo, colors, fonts     | SVG as primary format, PNG at @1x/@2x/@3x     |
| Favicon generation | Sharp-based script from SVG source              | Generate 16, 32, 48, 64, 128, 256px sizes     |
| Accessibility      | WCAG AA contrast ratios for text on backgrounds | Verify primary color passes AA on white       |

## Brand Discovery Checklist

| Question                            | Purpose                                 |
| ----------------------------------- | --------------------------------------- |
| What does the company do?           | Industry context                        |
| Who is the target audience?         | Demographic and psychographic targeting |
| What are the brand values?          | Core identity pillars                   |
| What feeling should the logo evoke? | Emotional direction                     |
| Any colors or symbols to avoid?     | Constraints and sensitivities           |
| Who are the competitors?            | Differentiation opportunities           |

## Common Mistakes

| Mistake                                     | Correct Pattern                                                                    |
| ------------------------------------------- | ---------------------------------------------------------------------------------- |
| Designing the logo in color first           | Design in monochrome first; logo must work in a single color before adding palette |
| Skipping the brand discovery checklist      | Always gather company values, audience, competitors, and constraints before design |
| Using more than two font families           | Limit to one display font and one body font for cohesion                           |
| Not providing logo variants                 | Create full, icon-only, and wordmark-only variants plus monochrome versions        |
| Exporting logos only as PNG                 | Provide SVG as primary format; add PNG at @1x, @2x, @3x for raster needs           |
| Using brand color for large backgrounds     | Follow 60/30/10 rule: 60% neutral, 30% primary, 10% accent                         |
| Adding effects to logo (shadows, gradients) | Logo is used as-is from approved variants only                                     |
| Missing clear space rules                   | Define clear space equal to height of tallest letter around logo                   |
| No minimum size specification               | Digital: 120px full / 40px icon; Print: 1in full / 0.25in icon                     |

## Delegation

When working on brand design, delegate to:

- `design-system` -- Token hierarchy and component architecture
- `asset-manager` -- Image optimization and asset pipeline
- `figma-developer` -- Figma-to-code implementation

## References

- [Logo Design](references/logo-design.md) -- SVG logo component with full, icon, and wordmark variants
- [Color Palette](references/color-palette.md) -- Brand color definitions, Tailwind config, usage guidelines
- [Typography](references/typography.md) -- Font selection, CSS custom properties, React typography components
- [Brand Guidelines](references/brand-guidelines.md) -- Complete guidelines template with voice, tone, and visual rules
- [Templates](references/templates.md) -- Social media, business card, and profile image SVG templates
- [Asset Management](references/asset-management.md) -- File organization, favicon generation, HTML meta tags
