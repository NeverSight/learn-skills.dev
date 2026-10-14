---
name: awesome-claude-design
description: Use ready-to-use DESIGN.md files to scaffold complete design systems in Claude Design with colors, typography, components, and UI kits
triggers:
  - "scaffold a design system from DESIGN.md"
  - "use Claude Design with a DESIGN.md file"
  - "generate UI from design system inspiration"
  - "create components from DESIGN.md"
  - "set up Claude Design with design tokens"
  - "build a design system with Claude"
  - "import DESIGN.md into Claude Design"
  - "use awesome-claude-design templates"
---

# Awesome Claude Design

> Skill by [ara.so](https://ara.so) — Design Skills collection.

This skill helps you use the `awesome-claude-design` collection: 68 ready-to-use `DESIGN.md` files that Claude Design expands into full UI scaffolds with design tokens, components, and working UI kits in a single shot.

## What This Project Does

`awesome-claude-design` is a curated collection of `DESIGN.md` files extracted from real brands (Claude, Vercel, Stripe, Linear, etc.). Each file describes a complete visual design system in a markdown format that AI design agents can parse and execute.

When you upload a `DESIGN.md` to [Claude Design](https://claude.ai/design), it automatically generates:

- **Design tokens** (colors, typography, spacing) as CSS variables
- **Component library** (buttons, cards, nav, forms)
- **Preview cards** showcasing the design system
- **Working UI kit** (`index.html` + CSS) applying the system
- **`SKILL.md`** for reusable design patterns

This skips the blank-page design brief and gives Claude Design a concrete starting point that matches your desired aesthetic.

## Installation & Setup

### 1. Browse the Collection

Visit the GitHub repository to see all 68 design systems:

```bash
# Clone the repository to browse locally
git clone https://github.com/VoltAgent/awesome-claude-design.git
cd awesome-claude-design
```

Or browse online at: `https://github.com/VoltAgent/awesome-claude-design`

### 2. Select a Design System

Each `DESIGN.md` has a preview page at `https://getdesign.md/<brand>/design-md`. Examples:

- Claude: `https://getdesign.md/claude/design-md`
- Vercel: `https://getdesign.md/vercel/design-md`
- Stripe: `https://getdesign.md/stripe/design-md`
- Linear: `https://getdesign.md/linear.app/design-md`

Preview pages show:
- Color palettes with hex codes
- Typography scales and font families
- Component examples
- Brand voice and personality
- Download link for `DESIGN.md`

### 3. Download the DESIGN.md

Click the download button on any preview page, or fetch directly:

```bash
# Example: Download Vercel's DESIGN.md
curl -O https://getdesign.md/vercel/DESIGN.md

# Example: Download Linear's DESIGN.md
curl -O https://getdesign.md/linear.app/DESIGN.md
```

## Using DESIGN.md in Claude Design

### Option A: Start from Design System

1. Go to `https://claude.ai/design/#org`
2. Click **Create new design system**
3. On the *Set up your design system* screen, upload the `DESIGN.md` under **Add assets**
4. Claude Design automatically parses it and generates the full system

### Option B: Start from Prototype

1. Go to Claude Design dashboard
2. Create a new prototype
3. Attach the `DESIGN.md` file in the chat
4. Send prompt:

```
Create a design system from this DESIGN.md
```

Claude Design will generate the complete package within minutes.

## DESIGN.md Structure

A `DESIGN.md` file typically contains:

```markdown
# Brand Name Design System

## Brand Identity
- **Voice**: [conversational, technical, playful, premium, etc.]
- **Personality**: [key adjectives]
- **Target audience**: [who this is for]

## Colors
### Primary Palette
- **Brand Primary**: `#HEX` - [usage context]
- **Brand Secondary**: `#HEX` - [usage context]
- **Accent**: `#HEX` - [usage context]

### Semantic Colors
- **Success**: `#HEX`
- **Warning**: `#HEX`
- **Error**: `#HEX`
- **Info**: `#HEX`

### Neutral Scale
- **Background**: `#HEX`
- **Surface**: `#HEX`
- **Text Primary**: `#HEX`
- **Text Secondary**: `#HEX`
- **Border**: `#HEX`

## Typography
- **Font Family**: [Primary font name] / [Fallback]
- **Display**: [weight, size, line-height]
- **Heading 1-6**: [specs for each level]
- **Body**: [regular text specs]
- **Caption**: [small text specs]

## Spacing Scale
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px
- 3xl: 64px

## Components
### Button
- **Primary**: [styles]
- **Secondary**: [styles]
- **Ghost**: [styles]
- **States**: hover, active, disabled

### Card
- [padding, border-radius, shadow, background]

### Input
- [height, padding, border, focus states]

## Layout
- **Container max-width**: [value]
- **Grid columns**: [number]
- **Gutter**: [value]
- **Breakpoints**: mobile, tablet, desktop

## Imagery
- **Style**: [photography, illustrations, abstract]
- **Treatment**: [filters, overlays]
- **Aspect ratios**: [common ratios used]

## Motion
- **Easing**: [transition timing functions]
- **Duration**: [animation speeds]
- **Key animations**: [hover, page transitions, etc.]
```

## Working with Generated Output

After Claude Design processes a `DESIGN.md`, it produces:

### 1. README.md
Brand context, design principles, and usage guidelines:

```markdown
# [Brand] Design System

## Overview
[Brand voice and positioning]

## Color Tokens
CSS variables for all colors

## Typography
Font stack and type scale

## Components
Usage patterns for each component
```

### 2. colors_and_type.css
CSS custom properties ready to use:

```css
:root {
  /* Colors */
  --color-primary: #6366f1;
  --color-secondary: #8b5cf6;
  --color-background: #ffffff;
  --color-text: #111827;
  
  /* Typography */
  --font-primary: 'Inter', system-ui, sans-serif;
  --font-display: 'Cal Sans', 'Inter', sans-serif;
  --text-base: 16px;
  --text-scale: 1.25;
  
  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  
  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
}
```

### 3. Component Files
Individual HTML/CSS for buttons, cards, inputs, etc:

```html
<!-- button.html -->
<button class="btn btn--primary">
  Primary Button
</button>

<button class="btn btn--secondary">
  Secondary Button
</button>

<button class="btn btn--ghost">
  Ghost Button
</button>
```

```css
/* button.css */
.btn {
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  font-family: var(--font-primary);
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn--primary {
  background: var(--color-primary);
  color: white;
}

.btn--primary:hover {
  background: var(--color-primary-dark);
  transform: translateY(-1px);
}
```

### 4. UI Kit (index.html)
A working page demonstrating the system:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Design System UI Kit</title>
  <link rel="stylesheet" href="colors_and_type.css">
  <link rel="stylesheet" href="components.css">
</head>
<body>
  <header>
    <nav class="navbar">
      <div class="container">
        <a href="#" class="logo">Brand</a>
        <div class="nav-links">
          <a href="#">Features</a>
          <a href="#">Pricing</a>
          <a href="#">Docs</a>
          <button class="btn btn--primary">Get Started</button>
        </div>
      </div>
    </nav>
  </header>
  
  <main>
    <section class="hero">
      <h1>Build faster with [Brand]</h1>
      <p>Design system description</p>
      <button class="btn btn--primary btn--lg">Start Building</button>
    </section>
  </main>
</body>
</html>
```

## Common Patterns

### Pattern 1: Customize an Existing Design System

1. Download a `DESIGN.md` that's close to your target
2. Edit the file to adjust colors, fonts, or components
3. Upload the modified `DESIGN.md` to Claude Design
4. Iterate with prompts like:

```
Update the primary color to #FF6B6B and regenerate the components
```

### Pattern 2: Mix Design Systems

Combine elements from multiple `DESIGN.md` files:

```
Use Vercel's color palette with Linear's typography and Stripe's component style
```

Attach multiple `DESIGN.md` files and specify which aspects to use from each.

### Pattern 3: Extract Design Tokens for Code

Use the generated CSS variables in your actual codebase:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
        background: 'var(--color-background)',
      },
      fontFamily: {
        sans: 'var(--font-primary)',
        display: 'var(--font-display)',
      },
      spacing: {
        xs: 'var(--space-xs)',
        sm: 'var(--space-sm)',
        md: 'var(--space-md)',
        lg: 'var(--space-lg)',
      }
    }
  }
}
```

### Pattern 4: Generate New Screens On-System

After establishing the design system, request new pages:

```
Create a pricing page using this design system
```

```
Design a dashboard layout with cards, charts, and a sidebar
```

Claude Design will generate new screens that automatically follow the established tokens and component patterns.

## Design System Categories

The collection includes 68 design systems across categories:

### AI & LLM Platforms
Claude, Cohere, ElevenLabs, Mistral AI, Ollama, Replicate, RunwayML, Together AI, VoltAgent, xAI

### Developer Tools & IDEs
Cursor, Expo, Lovable, Raycast, Superhuman, Vercel, Warp

### Backend & DevOps
ClickHouse, Composio, HashiCorp, MongoDB, PostHog, Sanity, Sentry, Supabase

### Productivity & SaaS
Cal.com, Intercom, Linear, Mintlify, Notion, Resend, Zapier

### Design & Creative Tools
Airtable, Clay, Figma, Framer, Miro, Webflow

### Fintech & Crypto
Binance, Coinbase, Kraken, Mastercard, Revolut, Stripe, Wise

### E-commerce & Retail
Airbnb, Meta, Nike, Shopify

### Media & Consumer Tech
Apple, IBM, NVIDIA, Pinterest, PlayStation, SpaceX, Spotify

## Troubleshooting

### Issue: Claude Design doesn't recognize the DESIGN.md

**Solution**: Ensure the file is named exactly `DESIGN.md` (case-sensitive) and follows the standard structure. Try explicitly prompting:

```
Parse this DESIGN.md file and create a design system from it
```

### Issue: Fonts not loading

**Solution**: Claude Design uses Google Fonts substitutes for proprietary fonts. Check the generated CSS for `@import` statements and ensure they're included in your HTML `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### Issue: Colors look different than expected

**Solution**: Check if the `DESIGN.md` uses color names vs hex codes. Claude Design interprets hex more reliably:

```markdown
<!-- Less reliable -->
- Primary: "Blue"

<!-- More reliable -->
- Primary: #3B82F6
```

### Issue: Components don't match the reference site exactly

**Solution**: `DESIGN.md` captures design *principles* not pixel-perfect replicas. To get closer:

```
Match the button style from [brand].com more closely - use 12px padding, 500 font weight, and 0.5px letter spacing
```

### Issue: Generated UI kit is too simple

**Solution**: Request more complex examples:

```
Create a dashboard UI kit with a sidebar, data tables, charts, and a multi-column layout
```

```
Add a blog post template with hero image, article body, and related posts section
```

## API Reference (Claude Design Prompts)

While Claude Design doesn't have a traditional API, these prompts work reliably:

### System Generation
```
Create a design system from this DESIGN.md
```

### Token Extraction
```
Show me all color tokens as CSS custom properties
```

```
Export the typography scale as Tailwind config
```

### Component Requests
```
Create a [button/card/nav/form/modal] component following this design system
```

```
Design a [hero/feature/pricing/testimonial] section
```

### Iteration
```
Update the primary color to [#HEX] and regenerate affected components
```

```
Make the typography more [compact/spacious/bold/lightweight]
```

```
Add dark mode variants to all components
```

### Export
```
Package this design system for Figma import
```

```
Generate a Storybook-compatible component library
```

## Integration Examples

### React Component Library

```typescript
// Button.tsx
import './colors_and_type.css';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({ 
  variant = 'primary',
  size = 'md',
  children 
}) => {
  return (
    <button className={`btn btn--${variant} btn--${size}`}>
      {children}
    </button>
  );
};
```

### Vue Component

```vue
<template>
  <button :class="buttonClasses">
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import './colors_and_type.css';

interface Props {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md'
});

const buttonClasses = computed(() => [
  'btn',
  `btn--${props.variant}`,
  `btn--${props.size}`
]);
</script>
```

### Svelte Component

```svelte
<script lang="ts">
  import './colors_and_type.css';
  
  export let variant: 'primary' | 'secondary' | 'ghost' = 'primary';
  export let size: 'sm' | 'md' | 'lg' = 'md';
</script>

<button class="btn btn--{variant} btn--{size}">
  <slot />
</button>
```

## Contributing Your Own DESIGN.md

To add a new design system to the collection:

1. Fork the repository
2. Create a new `DESIGN.md` following the structure above
3. Add a preview to `getdesign.md` (if contributing to the main collection)
4. Submit a pull request with:
   - The `DESIGN.md` file
   - Screenshots of the generated output
   - Brief description of the brand aesthetic

## Resources

- **Main repo**: `https://github.com/VoltAgent/awesome-claude-design`
- **Claude Design**: `https://claude.ai/design`
- **DESIGN.md spec**: `https://getdesign.md/what-is-design-md`
- **Discord**: `https://s.voltagent.dev/discord`

## Related Skills

- `claude-code` - AI coding agent by Anthropic
- `figma-api` - Programmatic Figma access
- `tailwind-css` - Utility-first CSS framework (pairs well with generated tokens)
