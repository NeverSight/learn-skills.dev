---
name: m3-web-ink
description: Implement Material Design 3 in terminal CLIs using Ink (React for CLIs) with @inkjs/ui components. Covers M3 token mapping to terminal colors, ThemeProvider setup, component mapping, and ANSI fallbacks. Use this when building M3-styled command-line interfaces.
license: Apache-2.0
---

# Material Design 3 — Ink (React CLI)

## Overview

Ink is a React renderer for building interactive command-line interfaces. Combined with `@inkjs/ui`, it provides themeable CLI components. M3 design tokens can be mapped to terminal colors for consistent, Material-styled CLI experiences.

**Keywords**: Material Design 3, M3, Ink, CLI, terminal, command-line, @inkjs/ui, React CLI, terminal UI

## When to Use

- Node.js CLI tools and developer tooling
- Interactive terminal applications
- When you want M3-consistent styling in the terminal
- React-based CLI projects

## Install

```bash
npm install ink react @inkjs/ui
```

## M3 Theme Setup

Map M3 tokens to terminal colors:

```jsx
// m3-theme.js
export const m3Theme = {
  colors: {
    primary: '#6750A4',
    onPrimary: '#FFFFFF',
    secondary: '#625B71',
    tertiary: '#7D5260',
    error: '#B3261E',
    surface: '#FEF7FF',
    onSurface: '#1D1B20',
    outline: '#79747E',
    // Terminal-friendly named colors (for broader compatibility)
    primaryTerminal: 'magenta',
    secondaryTerminal: 'gray',
    errorTerminal: 'red',
    successTerminal: 'green',
  },
};

// For dark terminal backgrounds
export const m3ThemeDark = {
  colors: {
    primary: '#D0BCFF',
    onPrimary: '#381E72',
    secondary: '#CCC2DC',
    error: '#F2B8B5',
    surface: '#141218',
    onSurface: '#E6E0E9',
    primaryTerminal: 'magentaBright',
    errorTerminal: 'redBright',
  },
};
```

## Component Examples

### Full App with M3 Tokens

```jsx
import React from 'react';
import {render, Box, Text} from 'ink';
import {TextInput, Select, Spinner, Badge} from '@inkjs/ui';
import {m3Theme} from './m3-theme.js';

function App() {
  return (
    <Box flexDirection="column" padding={1} gap={1}>
      {/* M3 Primary colored heading */}
      <Text color={m3Theme.colors.primary} bold>
        ✦ Material Design 3 CLI
      </Text>

      {/* M3 Surface container */}
      <Box
        borderStyle="round"
        borderColor={m3Theme.colors.outline}
        paddingX={2}
        paddingY={1}
        flexDirection="column"
        gap={1}
      >
        <Text color={m3Theme.colors.onSurface}>
          Welcome to the M3-styled terminal
        </Text>

        <TextInput
          placeholder="Enter your name..."
          onSubmit={name => {}}
        />

        <Select
          options={[
            {label: 'Option 1', value: '1'},
            {label: 'Option 2', value: '2'},
          ]}
          onChange={value => {}}
        />
      </Box>

      {/* M3 Status indicators */}
      <Box gap={1}>
        <Badge color="green">Success</Badge>
        <Badge color={m3Theme.colors.errorTerminal}>Error</Badge>
      </Box>

      <Spinner label="Loading..." />
    </Box>
  );
}

render(<App />);
```

### Button Equivalent

```jsx
import {Box, Text} from 'ink';

<Box paddingX={2} paddingY={0}>
  <Text backgroundColor="magenta" color="white" bold> Action </Text>
</Box>
```

### Navigation (Select)

```jsx
import {Select} from '@inkjs/ui';

<Select
  options={[
    {label: '🏠 Home', value: 'home'},
    {label: '🔍 Search', value: 'search'},
    {label: '⚙️ Settings', value: 'settings'},
  ]}
  onChange={value => {}}
/>
```

## ThemeProvider for M3

```jsx
import {ThemeProvider, extendTheme} from '@inkjs/ui';

const m3InkTheme = extendTheme({
  components: {
    TextInput: {
      styles: {
        focusColor: 'magenta', // M3 primary
      },
    },
    Select: {
      styles: {
        highlightColor: 'magenta',
      },
    },
    Spinner: {
      styles: {
        color: 'magenta',
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={m3InkTheme}>
      {/* All child components use M3-inspired theme */}
    </ThemeProvider>
  );
}
```

## Terminal Color Considerations

- Modern terminals support 24-bit (true color) via hex values — use full M3 hex tokens
- For legacy terminals (256/16 color), map M3 roles to named ANSI colors:
  - Primary → `magenta` (closest to M3 purple primary)
  - Secondary → `gray`
  - Tertiary → `cyan`
  - Error → `red`
  - Success → `green` (custom role for CLI)
- Detect color support with `chalk.level` or `supports-color` package
- Always provide fallback named colors for maximum compatibility

## M3 Component Mapping for CLI

| M3 Component | Ink/ink-ui Equivalent | Notes |
|--------------|----------------------|-------|
| Filled Button | `<Box>` + `<Text>` styled | Background color + text |
| Text Field | `<TextInput>` | From `@inkjs/ui` |
| Select / Menu | `<Select>` | From `@inkjs/ui` |
| Multi-select | `<MultiSelect>` | From `@inkjs/ui` |
| Progress Indicator | `<Spinner>`, `<ProgressBar>` | From `@inkjs/ui` |
| Badge / Chip | `<Badge>` | From `@inkjs/ui` |
| Confirm Dialog | `<ConfirmInput>` | From `@inkjs/ui` |
| Card | `<Box borderStyle="round">` | Bordered container |
| Divider | `<Text>{'─'.repeat(n)}</Text>` | Horizontal rule |
| List | `<UnorderedList>`, `<OrderedList>` | From `@inkjs/ui` |
| Alert / Snackbar | `<Alert>` | From `@inkjs/ui` |

## Checklist

- [ ] M3 color tokens defined in a theme object
- [ ] Terminal color fallbacks provided for legacy terminals
- [ ] `@inkjs/ui` ThemeProvider configured with M3-inspired colors
- [ ] Components use theme tokens (not hard-coded colors)
- [ ] Dark terminal variant provided
- [ ] Color detection implemented (true color vs 256 vs 16)

## Resources

- Ink: https://github.com/vadimdemedes/ink
- Ink UI components: https://github.com/vadimdemedes/ink-ui
- npm (ink): https://www.npmjs.com/package/ink
- npm (@inkjs/ui): https://www.npmjs.com/package/@inkjs/ui
