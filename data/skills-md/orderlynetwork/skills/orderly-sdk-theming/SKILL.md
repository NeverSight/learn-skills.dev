---
name: orderly-sdk-theming
description: Customize the visual appearance of your Orderly DEX with CSS variables, colors, fonts, logos, and TradingView chart styling.
---

# Orderly Network: SDK Theming

Customize the look and feel of your DEX using CSS variables, the theme provider, and component overrides.

## When to Use

- Rebranding your DEX
- Changing color schemes
- Adding custom fonts
- Styling TradingView charts
- Creating PnL share cards

## Prerequisites

- Orderly SDK packages installed
- Tailwind CSS configured
- Basic CSS knowledge

## Overview

Orderly UI uses a CSS variable-based theming system with Tailwind CSS integration:

1. **CSS Variables** - Define colors, spacing, border radius
2. **Tailwind Preset** - Orderly's custom Tailwind configuration
3. **OrderlyThemeProvider** - Component-level overrides
4. **Assets** - Logo, favicon, PnL backgrounds

## 1. CSS Variables

All UI components use CSS variables prefixed with `--oui-`. Override them in your CSS to customize the theme.

### Create Theme File

```css
/* src/styles/theme.css */

:root {
  /* BRAND COLORS */
  --oui-color-primary: 99 102 241;
  --oui-color-primary-light: 165 180 252;
  --oui-color-primary-darken: 79 70 229;
  --oui-color-primary-contrast: 255 255 255;

  --oui-color-link: 99 102 241;
  --oui-color-link-light: 165 180 252;

  /* SEMANTIC COLORS */
  --oui-color-success: 34 197 94;
  --oui-color-success-light: 134 239 172;
  --oui-color-success-darken: 22 163 74;
  --oui-color-success-contrast: 255 255 255;

  --oui-color-danger: 239 68 68;
  --oui-color-danger-light: 252 165 165;
  --oui-color-danger-darken: 220 38 38;
  --oui-color-danger-contrast: 255 255 255;

  --oui-color-warning: 245 158 11;
  --oui-color-warning-light: 252 211 77;
  --oui-color-warning-darken: 217 119 6;
  --oui-color-warning-contrast: 255 255 255;

  /* TRADING COLORS */
  --oui-color-trading-profit: 34 197 94;
  --oui-color-trading-loss: 239 68 68;

  /* BACKGROUND SCALE (dark theme: 1=lightest, 10=darkest) */
  --oui-color-base-1: 100 116 139;
  --oui-color-base-2: 71 85 105;
  --oui-color-base-3: 51 65 85;
  --oui-color-base-4: 45 55 72;
  --oui-color-base-5: 39 49 66;
  --oui-color-base-6: 30 41 59;
  --oui-color-base-7: 24 33 47;
  --oui-color-base-8: 18 26 38;
  --oui-color-base-9: 15 23 42;
  --oui-color-base-10: 10 15 30;

  --oui-color-base-foreground: 255 255 255;
  --oui-color-line: 255 255 255;
  --oui-color-fill: 30 41 59;
  --oui-color-fill-active: 39 49 66;

  /* GRADIENTS */
  --oui-gradient-primary-start: 79 70 229;
  --oui-gradient-primary-end: 139 92 246;

  /* TYPOGRAPHY */
  --oui-font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

  /* BORDER RADIUS */
  --oui-rounded-sm: 2px;
  --oui-rounded: 4px;
  --oui-rounded-md: 6px;
  --oui-rounded-lg: 8px;
  --oui-rounded-xl: 12px;
  --oui-rounded-2xl: 16px;
  --oui-rounded-full: 9999px;
}
```

### Import Theme

```css
/* src/styles/index.css */
@import '@orderly.network/ui/dist/styles.css';
@import './theme.css';
@import './fonts.css';

@tailwind base;
@tailwind components;
@tailwind utilities;
```

> **Note**: CSS variables use space-separated RGB values (e.g., `99 102 241`) not `rgb()` syntax. This allows Tailwind to apply opacity modifiers.

## 2. Color Variable Reference

### Brand Colors

| Variable                       | Usage                                   |
| ------------------------------ | --------------------------------------- |
| `--oui-color-primary`          | Primary buttons, active states, accents |
| `--oui-color-primary-light`    | Hover states, secondary highlights      |
| `--oui-color-primary-darken`   | Active/pressed states                   |
| `--oui-color-primary-contrast` | Text on primary backgrounds             |
| `--oui-color-link`             | Link text color                         |

### Semantic Colors

| Variable              | Usage                                       |
| --------------------- | ------------------------------------------- |
| `--oui-color-success` | Profit, positive values, success messages   |
| `--oui-color-danger`  | Loss, negative values, errors, sell buttons |
| `--oui-color-warning` | Warnings, alerts, caution states            |

### Trading Colors

| Variable                     | Usage                               |
| ---------------------------- | ----------------------------------- |
| `--oui-color-trading-profit` | Green for profits in orderbook, PnL |
| `--oui-color-trading-loss`   | Red for losses in orderbook, PnL    |

### Background Scale

```
base-1 (lightest) → base-10 (darkest)
```

| Variable                         | Usage                  |
| -------------------------------- | ---------------------- |
| `--oui-color-base-1` to `base-3` | Muted/disabled text    |
| `--oui-color-base-4` to `base-5` | Borders, dividers      |
| `--oui-color-base-6` to `base-7` | Card/panel backgrounds |
| `--oui-color-base-8` to `base-9` | Page backgrounds       |
| `--oui-color-base-10`            | Darkest background     |

## 3. Custom Fonts

### Add Custom Font

```css
/* src/styles/fonts.css */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Or use local font files */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/CustomFont-Regular.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
}
```

### Apply Font

```css
/* In theme.css */
:root {
  --oui-font-family: 'CustomFont', 'Inter', sans-serif;
}
```

## 4. Logo & Assets

### Configure App Icons

```tsx
import { OrderlyAppProvider } from "@orderly.network/react-app";

<OrderlyAppProvider
  brokerId="your_broker_id"
  brokerName="Your DEX"
  networkId="mainnet"
  appIcons={{
    main: {
      img: "/logo.svg",
    },
    secondary: {
      img: "/logo-small.svg",
    },
  }}
>
```

### Favicon

```html
<head>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
</head>
```

## 5. PnL Share Backgrounds

Customize the backgrounds for the PnL sharing feature:

### Add Background Images

```
public/
├── pnl/
│   ├── profit-bg-1.png
│   ├── profit-bg-2.png
│   └── loss-bg-1.png
```

### Configure in TradingPage

```tsx
<TradingPage
  symbol={symbol}
  sharePnLConfig={{
    backgroundImages: ['/pnl/profit-bg-1.png', '/pnl/profit-bg-2.png'],
    color: 'rgba(255, 255, 255, 0.98)',
    profitColor: 'rgb(34, 197, 94)',
    lossColor: 'rgb(239, 68, 68)',
    brandColor: 'rgb(99, 102, 241)',
  }}
/>
```

## 6. TradingView Chart Colors

Customize the TradingView chart to match your theme:

```tsx
<TradingPage
  symbol={symbol}
  tradingViewConfig={{
    scriptSRC: '/tradingview/charting_library/charting_library.js',
    library_path: '/tradingview/charting_library/',
    colorConfig: {
      chartBG: '#0f172a',
      upColor: '#22c55e',
      downColor: '#ef4444',
      pnlUpColor: '#22c55e',
      pnlDownColor: '#ef4444',
      textColor: '#e2e8f0',
    },
    overrides: {
      'paneProperties.background': '#0f172a',
      'scalesProperties.textColor': '#e2e8f0',
    },
  }}
/>
```

## 7. Component Overrides

Use `OrderlyThemeProvider` for component-level customization:

```tsx
import { OrderlyThemeProvider } from '@orderly.network/ui';

<OrderlyThemeProvider
  overrides={{
    button: {
      primary: {
        className: 'custom-primary-button',
      },
    },
    input: {
      className: 'custom-input',
    },
  }}
>
  {children}
</OrderlyThemeProvider>;
```

## 8. Tailwind Configuration

### tailwind.config.ts

```ts
import type { Config } from 'tailwindcss';
import { OUITailwind } from '@orderly.network/ui';

export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
    './node_modules/@orderly.network/**/*.{js,mjs}',
  ],
  presets: [OUITailwind.preset],
  theme: {
    extend: {
      colors: {
        brand: {
          500: '#6366f1',
          600: '#4f46e5',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
} satisfies Config;
```

## 9. Complete Theme Example

### Blue/Cyan Theme

```css
:root {
  --oui-font-family: 'Inter', sans-serif;

  /* Brand - Cyan */
  --oui-color-primary: 6 182 212;
  --oui-color-primary-light: 103 232 249;
  --oui-color-primary-darken: 8 145 178;
  --oui-color-primary-contrast: 255 255 255;

  --oui-color-link: 34 211 238;

  /* Trading */
  --oui-color-trading-profit: 34 197 94;
  --oui-color-trading-loss: 239 68 68;

  /* Dark backgrounds */
  --oui-color-base-6: 17 24 39;
  --oui-color-base-7: 17 24 39;
  --oui-color-base-8: 10 15 25;
  --oui-color-base-9: 5 10 20;
  --oui-color-base-10: 0 5 15;

  /* Gradients */
  --oui-gradient-primary-start: 8 145 178;
  --oui-gradient-primary-end: 34 211 238;
}
```

## Best Practices

1. **Use RGB values** - CSS variables use space-separated RGB (e.g., `99 102 241`)
2. **Import order matters** - Import Orderly styles first, then your overrides
3. **Test all states** - Verify hover, active, disabled states look correct
4. **Check accessibility** - Ensure sufficient color contrast (WCAG 2.1)
5. **Test on mobile** - Some components have different mobile styling
6. **Match TradingView** - Keep chart colors consistent with your theme

## Related Skills

- **orderly-sdk-dex-architecture** - Project structure
- **orderly-sdk-install-dependency** - Installing packages
- **orderly-sdk-page-components** - Using pre-built components
