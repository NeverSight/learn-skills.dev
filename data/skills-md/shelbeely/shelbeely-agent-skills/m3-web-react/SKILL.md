---
name: m3-web-react
description: Implement Material Design 3 in React using MUI (Material UI) with M3-aligned theming, or @material/web with React wrappers. Covers theme setup, component usage, dark mode, and Next.js SSR integration. Use this when building M3-styled React or Next.js applications.
license: Apache-2.0
---

# Material Design 3 — React / MUI

## Overview

MUI (`@mui/material`) is the most popular React UI library. MUI v6 adds the Pigment CSS engine for better performance. M3 theming support is evolving — MUI primarily implements M2 component APIs but supports M3 color tokens and theming through customization.

**Keywords**: Material Design 3, M3, React, MUI, Material UI, @mui/material, Next.js, SSR, React Server Components, material-web-components-react

## When to Use

- React projects where you want the largest ecosystem and most mature library
- Next.js projects needing M3 styling with SSR and React Server Components
- When you want the best React/Next.js integration

## Install

```bash
npm install @mui/material @emotion/react @emotion/styled
```

For Next.js SSR:
```bash
npm install @mui/material @emotion/react @emotion/styled @mui/material-nextjs
```

## M3-Aligned Theme Setup

```jsx
import { createTheme, ThemeProvider } from '@mui/material/styles';

const m3Theme = createTheme({
  palette: {
    primary: { main: '#6750A4' },
    secondary: { main: '#625B71' },
    error: { main: '#B3261E' },
    background: {
      default: '#FEF7FF',
      paper: '#F3EDF7',
    },
  },
  shape: { borderRadius: 20 }, // M3 Large radius
  typography: {
    fontFamily: '"Roboto", sans-serif',
  },
});

const m3ThemeDark = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#D0BCFF' },
    secondary: { main: '#CCC2DC' },
    error: { main: '#F2B8B5' },
    background: {
      default: '#141218',
      paper: '#2B2930',
    },
  },
  shape: { borderRadius: 20 },
  typography: {
    fontFamily: '"Roboto", sans-serif',
  },
});

function App() {
  return (
    <ThemeProvider theme={m3Theme}>
      {/* Your M3-styled components */}
    </ThemeProvider>
  );
}
```

## Component Examples

### Buttons

```jsx
import Button from '@mui/material/Button';

<Button variant="contained">Filled</Button>
<Button variant="outlined">Outlined</Button>
<Button variant="text">Text</Button>
```

### Cards

```jsx
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

<Card elevation={1}>
  <CardContent>
    <Typography variant="h6">Title</Typography>
    <Typography variant="body2">Content</Typography>
  </CardContent>
</Card>
```

### Text Fields

```jsx
import TextField from '@mui/material/TextField';

<TextField label="Email" variant="outlined" />
<TextField label="Name" variant="filled" />
```

### Navigation

```jsx
import BottomNavigation from '@mui/material/BottomNavigation';
import BottomNavigationAction from '@mui/material/BottomNavigationAction';
import HomeIcon from '@mui/icons-material/Home';
import SearchIcon from '@mui/icons-material/Search';

<BottomNavigation value={value} onChange={handleChange}>
  <BottomNavigationAction label="Home" icon={<HomeIcon />} />
  <BottomNavigationAction label="Search" icon={<SearchIcon />} />
</BottomNavigation>
```

## Next.js SSR Integration

```tsx
// app/layout.tsx
import { AppRouterCacheProvider } from '@mui/material-nextjs/v14-appRouter';
import { ThemeProvider } from '@mui/material/styles';
import { m3Theme } from './theme';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <AppRouterCacheProvider>
          <ThemeProvider theme={m3Theme}>
            {children}
          </ThemeProvider>
        </AppRouterCacheProvider>
      </body>
    </html>
  );
}
```

## Alternative: `@material/web` in React

Use Google's official web components directly in React:

```jsx
// Client component (Next.js or Vite)
'use client';
import '@material/web/button/filled-button.js';

export function M3Button({ children }) {
  return <md-filled-button>{children}</md-filled-button>;
}
```

React wrappers: `material-web-components-react` provides thin React abstractions over `@material/web`.

## Checklist

- [ ] M3 theme created with `createTheme` using M3 color roles
- [ ] Both light and dark themes defined
- [ ] Shape uses M3 radius values (e.g., `borderRadius: 20`)
- [ ] Typography uses Roboto or M3-compatible font
- [ ] For Next.js: `AppRouterCacheProvider` wraps the app for SSR
- [ ] Components use theme-aware styling (no hard-coded colors)

## Resources

- `theme.ts` — Ready-to-use MUI theme config with M3 orange palette (light + dark) included in this skill's directory. Copy into your project and customize.
- `material-theme-builder` skill — Generate a custom palette from any source color.
- MUI: https://mui.com/material-ui/
- MUI + Next.js: https://mui.com/material-ui/integrations/nextjs/
- MUI Theming: https://mui.com/material-ui/customization/theming/
- M3 adoption tracking: https://github.com/mui/material-ui/issues/29345
