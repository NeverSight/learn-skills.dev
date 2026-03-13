---
name: corporate-colors
description: >
  Define corporate color palettes based on Catppuccin warm tones with light/dark mode conventions.
  Trigger: When defining brand colors, creating theme systems, or implementing light/dark modes.
license: Apache-2.0
metadata:
  author: 333-333-333
  version: "2.0"
  type: generic
  scope: [root]
  auto_invoke:
    - "Defining brand color systems"
    - "Creating design tokens or theme systems"
    - "Implementing light/dark mode switching"
    - "Establishing corporate color conventions"
---

## When to Use

- Defining brand color systems for applications
- Implementing light/dark theme switching
- Creating design tokens or style systems
- Establishing color naming conventions across teams

---

## Design Philosophy

**Warm tones only.** Bastet is a pet care platform — the brand must feel warm, inviting, and trustworthy. Cold blues/purples are explicitly avoided for primary and secondary roles.

Based on **Catppuccin** flavors:
- **Light mode**: Latte
- **Dark mode**: Mocha

### Brand Colors

| Role | Catppuccin Name | Light (Latte) | Dark (Mocha) | Usage |
|------|----------------|---------------|--------------|-------|
| **Primary** | Maroon | `#E64553` | `#EBA0AC` | CTAs, buttons, links, focus rings |
| **Secondary** | Flamingo | `#DD7878` | `#F2CDCD` | Badges, tags, supporting elements |
| **Emphasis** | Peach | `#FE640B` | `#FAB387` | Hover states, highlights, accents |
| **Warm info** | Rosewater | `#DC8A78` | `#F5E0DC` | Informational, subtle accents |

### Why These Colors

- **Maroon** — Bold warm red. Reads as "action" with confidence and warmth
- **Flamingo** — Soft pink that complements Maroon without competing
- **Peach** — Energetic orange for emphasis/hover, draws attention to highlights
- **Rosewater** — Delicate pink for info states, keeps everything cohesive

### Colors NOT Used as Primary/Secondary

| Color | Reason |
|-------|--------|
| Blue, Sapphire | Too cold, corporate feel |
| Lavender, Mauve | Purple is cold, doesn't match pet care warmth |
| Teal | Cold, clinical |
| Green | Reserved for semantic "success" only |

---

## Color Categories

| Category | Purpose | Usage |
|----------|---------|-------|
| **Primary** | Main brand actions (CTA, links, focus states) | Buttons, active states, primary actions |
| **Secondary** | Supporting elements, less prominent actions | Badges, tags, secondary buttons |
| **Accent** | Emphasis, highlights, notifications | Alerts, highlights, important info |
| **Surface** | Backgrounds, containers | Cards, modals, panels |
| **Text** | Typography hierarchy | Body text, headings, labels |
| **Border** | Dividers, outlines | Separators, input borders |

---

## Catppuccin Color Mappings

All color token definitions (primary, secondary, accent, surface, text, border) for both light and dark modes:

> See [assets/color-tokens.ts](assets/color-tokens.ts)

---

## Design Tokens

### CSS Custom Properties (light + dark)

> See [assets/styles.css](assets/styles.css)

### Tailwind Configuration

> See [assets/tailwind-colors.js](assets/tailwind-colors.js)

### TypeScript Theme System

> See [assets/theme-tokens.ts](assets/theme-tokens.ts)

### React Component Examples

> See [assets/example-component.tsx](assets/example-component.tsx)

### Flutter Implementation

Reference: `mobile/lib/app/theme/app_colors.dart`

```dart
// Access via Forui theme
final colors = context.theme.colors;
colors.primary;    // Maroon
colors.secondary;  // Flamingo
```

---

## Light/Dark Mode Conventions

### Contrast Requirements

| Element | Light Mode | Dark Mode |
|---------|------------|-----------|
| **Text on backgrounds** | Dark text on light surfaces | Light text on dark surfaces |
| **Primary actions** | High contrast (Maroon `#E64553` on Base `#eff1f5`) | Softer contrast (Maroon `#EBA0AC` on Base `#1e1e2e`) |
| **Borders** | Subtle, darker than background | Subtle, lighter than background |
| **Hover states** | Shift to Peach (warmer, energetic) | Shift to Peach (warmer, energetic) |

### Semantic Color Usage

```typescript
// DO: Use semantic names
<Button color="primary">Submit</Button>
<Alert variant="error">Failed</Alert>

// DON'T: Use specific color names
<Button color="peach">Submit</Button>
<Alert variant="red">Failed</Alert>
```

### Mode Switching

The app MUST respect the device's system brightness preference. Never force a single mode.

```dart
// Flutter — reads system preference automatically
final brightness = MediaQuery.platformBrightnessOf(context);
final scheme = brightness == Brightness.dark
    ? AppColors.dark
    : AppColors.light;
```

---

## Accessibility Guidelines

- **WCAG AA Compliance**: Minimum 4.5:1 contrast for normal text, 3:1 for large text
- **Focus Indicators**: Use primary color with 2px outline
- **Error States**: Always pair error color with icons/text, never rely on color alone
- **Color Blindness**: Peach/Flamingo may appear similar to protanopia — always pair with shape/text cues

---

## Commands

```bash
# Install Catppuccin palette packages (optional)
npm install @catppuccin/palette

# Test contrast ratios
npx polypane # or use online tools like contrast-ratio.com
```

---

## Resources

- **Catppuccin Official**: https://github.com/catppuccin/catppuccin
- **Palette Explorer**: https://catppuccin.com/palette
- **Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Flutter implementation**: `mobile/lib/app/theme/app_colors.dart`
