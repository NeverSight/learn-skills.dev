---
name: css-styling-standards
description: CSS styling standards and best practices for responsive, accessible, and maintainable web interfaces with special considerations for multilingual content and Chuukese text display. Includes Mantine UI v8 integration for React components. Use when creating or modifying stylesheets and CSS components.
---

# CSS Styling Standards

## Core Principles

- **Mobile-first design**: Start with mobile styles, enhance for larger screens
- **Accessibility compliance**: Meet WCAG 2.1 AA standards
- **Multilingual support**: Proper display of accented characters and different writing systems
- **Consistent naming**: Use BEM methodology for class naming (unless using Mantine)
- **Performance optimization**: Minimize CSS size and loading time
- **Mantine Integration**: Use Mantine UI v8 component system for React frontend

## Mantine UI v8 Integration

### 1. Theme Configuration

```typescript
// frontend/src/theme.ts
import { createTheme, MantineColorsTuple } from '@mantine/core';

// Custom color palette for Chuukese dictionary
const primaryBlue: MantineColorsTuple = [
  '#e5f4ff',
  '#cde4ff',
  '#9bc5ff',
  '#64a4ff',
  '#3988fe',
  '#1d77fe',
  '#096fff',
  '#005ee4',
  '#0053cd',
  '#0047b5',
];

export const theme = createTheme({
  primaryColor: 'blue',
  colors: {
    blue: primaryBlue,
  },
  fontFamily: "'Noto Sans', 'Arial Unicode MS', sans-serif",
  
  // Chuukese-optimized typography
  headings: {
    fontFamily: "'Noto Sans', 'Arial Unicode MS', sans-serif",
    fontWeight: '600',
  },
  
  // Default to dark color scheme
  defaultColorScheme: 'dark',
  
  // Component overrides for Chuukese text
  components: {
    Text: {
      defaultProps: {
        style: { 
          fontFeatureSettings: "'kern' 1, 'liga' 1" 
        }
      }
    },
    TextInput: {
      defaultProps: {
        styles: {
          input: {
            fontFamily: "'Noto Sans', 'Arial Unicode MS', sans-serif",
          }
        }
      }
    },
    Textarea: {
      defaultProps: {
        styles: {
          input: {
            fontFamily: "'Noto Sans', 'Arial Unicode MS', sans-serif",
            lineHeight: 1.6,
          }
        }
      }
    }
  }
});
```

### 2. Mantine Provider Setup

```tsx
// frontend/src/main.tsx
import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';

import { MantineProvider } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import { ModalsProvider } from '@mantine/modals';
import { theme } from './theme';

function App() {
  return (
    <MantineProvider theme={theme} defaultColorScheme="dark">
      <Notifications position="top-right" />
      <ModalsProvider>
        {/* App content */}
      </ModalsProvider>
    </MantineProvider>
  );
}
```

### 3. Chuukese Text with Mantine

```tsx
import { Text, Title, Badge, Card } from '@mantine/core';

// Chuukese word display component
function ChuukeseWord({ word, definition }: { word: string; definition: string }) {
  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Title order={3} style={{ fontFeatureSettings: "'kern' 1" }}>
        {word}
      </Title>
      <Text c="dimmed" size="sm" mt="xs">
        {definition}
      </Text>
    </Card>
  );
}

// Translation input with Mantine
function TranslationInput({ direction }: { direction: 'chk_to_en' | 'en_to_chk' }) {
  return (
    <Textarea
      label={direction === 'chk_to_en' ? 'Chuukese Text' : 'English Text'}
      placeholder={direction === 'chk_to_en' 
        ? 'Enter Chuukese text to translate...' 
        : 'Enter English text to translate...'}
      minRows={4}
      autosize
      styles={{
        input: {
          fontFamily: "'Noto Sans', 'Arial Unicode MS', sans-serif",
          fontSize: '1.1rem',
        }
      }}
    />
  );
}
```

### 4. Common Mantine Patterns

```tsx
// Loading state
import { Loader, Center, Stack, Text } from '@mantine/core';

<Center h={200}>
  <Stack align="center">
    <Loader size="lg" />
    <Text c="dimmed">Translating...</Text>
  </Stack>
</Center>

// Notifications
import { notifications } from '@mantine/notifications';

notifications.show({
  title: 'Translation Complete',
  message: 'Your text has been translated successfully',
  color: 'green',
});

// Modals
import { modals } from '@mantine/modals';

modals.openConfirmModal({
  title: 'Delete Entry',
  children: <Text>Are you sure you want to delete this entry?</Text>,
  labels: { confirm: 'Delete', cancel: 'Cancel' },
  confirmProps: { color: 'red' },
  onConfirm: () => handleDelete(),
});
```

## CSS Architecture (Non-Mantine Styles)

### 1. File Organization

```css
/* Main stylesheet structure */
@import 'normalize.css';           /* CSS reset */
@import 'variables.css';           /* Custom properties */
@import 'typography.css';          /* Font and text styles */
@import 'layout.css';              /* Grid and flexbox layouts */
@import 'components.css';          /* Reusable components */
@import 'utilities.css';           /* Utility classes */
@import 'responsive.css';          /* Media queries */
```

### 2. CSS Custom Properties (Variables)

```css
:root {
  /* Colors - should align with Mantine theme */
  --primary-color: #228be6;
  --secondary-color: #64748b;
  --accent-color: #f59e0b;
  --text-color: #c1c2c5;
  --text-light: #909296;
  --background-color: #1a1b1e;
  --surface-color: #25262b;
  
  /* Typography */
  --font-family-primary: 'Noto Sans', 'Arial Unicode MS', sans-serif;
  --font-family-chuukese: 'Noto Sans', 'Doulos SIL', 'Arial Unicode MS', sans-serif;
  --font-size-base: 1rem;
  --font-size-large: 1.125rem;
  --line-height-base: 1.6;
  --line-height-tight: 1.4;
  
  /* Spacing - matches Mantine spacing scale */
  --spacing-xs: 0.625rem;   /* 10px - Mantine xs */
  --spacing-sm: 0.75rem;    /* 12px - Mantine sm */
  --spacing-md: 1rem;       /* 16px - Mantine md */
  --spacing-lg: 1.25rem;    /* 20px - Mantine lg */
  --spacing-xl: 2rem;       /* 32px - Mantine xl */
  
  /* Mantine-aligned breakpoints */
  --breakpoint-xs: 576px;
  --breakpoint-sm: 768px;
  --breakpoint-md: 992px;
  --breakpoint-lg: 1200px;
  --breakpoint-xl: 1400px;
}

/* Dark mode (Mantine default) */
[data-mantine-color-scheme="dark"] {
  --text-color: #c1c2c5;
  --background-color: #1a1b1e;
  --surface-color: #25262b;
}

/* Light mode */
[data-mantine-color-scheme="light"] {
  --text-color: #1f2937;
  --background-color: #ffffff;
  --surface-color: #f9fafb;
}
```

## Component Standards

### 1. Chuukese Text Display

```css
/* 
 * Chuukese Text Component
 * Purpose: Proper display of Chuukese text with accent support
 * Usage: Apply to any element containing Chuukese content
 */
.chuukese-text {
  font-family: var(--font-family-chuukese);
  font-size: var(--font-size-large);
  line-height: var(--line-height-base);
  direction: ltr;
  unicode-bidi: embed;
  font-feature-settings: 'kern' 1, 'liga' 1;
}

/* Emphasis for Chuukese headings */
.chuukese-text--heading {
  font-weight: 600;
  letter-spacing: 0.02em;
  margin-bottom: var(--spacing-md);
}

/* Inline Chuukese within English text */
.chuukese-text--inline {
  font-style: italic;
  font-weight: 500;
  color: var(--primary-color);
}
```

### 2. Translation Interface Components

```css
/* 
 * Translation Input Component
 * Purpose: Input fields for translation interface
 * Dependencies: Requires .form-group wrapper
 */
.translation-input {
  width: 100%;
  min-height: 120px;
  padding: var(--spacing-md);
  border: 2px solid var(--surface-color);
  border-radius: 0.5rem;
  font-family: var(--font-family-chuukese);
  font-size: var(--font-size-base);
  line-height: var(--line-height-base);
  resize: vertical;
  transition: border-color 0.2s ease-in-out;
}

.translation-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px hsla(217, 91%, 60%, 0.1);
}

.translation-input--chuukese {
  direction: ltr;
  text-align: left;
}

.translation-input--error {
  border-color: #ef4444;
}
```

### 3. Dictionary Entry Component

```css
/* 
 * Dictionary Entry Card
 * Purpose: Display individual dictionary entries
 * Usage: Container for dictionary entry information
 */
.dictionary-entry {
  background: var(--background-color);
  border: 1px solid var(--surface-color);
  border-radius: 0.5rem;
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s ease-in-out;
}

.dictionary-entry:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.dictionary-entry__word {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: var(--spacing-sm);
}

.dictionary-entry__definition {
  color: var(--text-color);
  margin-bottom: var(--spacing-sm);
}

.dictionary-entry__pronunciation {
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: var(--text-light);
  background: var(--surface-color);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: 0.25rem;
  display: inline-block;
}

.dictionary-entry__cultural-note {
  font-style: italic;
  color: var(--text-light);
  border-left: 3px solid var(--accent-color);
  padding-left: var(--spacing-sm);
  margin-top: var(--spacing-sm);
}
```

## Layout Standards

### 1. Grid System

```css
/* 
 * Custom Grid System
 * Purpose: Flexible grid layout for various screen sizes
 */
.grid {
  display: grid;
  gap: var(--spacing-md);
}

.grid--2-col {
  grid-template-columns: 1fr 1fr;
}

.grid--3-col {
  grid-template-columns: repeat(3, 1fr);
}

.grid--auto-fit {
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

/* Responsive grid adjustments */
@media (max-width: 768px) {
  .grid--2-col,
  .grid--3-col {
    grid-template-columns: 1fr;
  }
}
```

### 2. Container and Spacing

```css
/* 
 * Container Component
 * Purpose: Main content wrapper with responsive max-width
 */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

@media (min-width: 768px) {
  .container {
    padding: 0 var(--spacing-lg);
  }
}

/* Spacing utilities */
.mb-sm { margin-bottom: var(--spacing-sm); }
.mb-md { margin-bottom: var(--spacing-md); }
.mb-lg { margin-bottom: var(--spacing-lg); }
.mt-sm { margin-top: var(--spacing-sm); }
.mt-md { margin-top: var(--spacing-md); }
.mt-lg { margin-top: var(--spacing-lg); }
```

## Responsive Design

### 1. Mobile-First Media Queries

```css
/* Base styles for mobile */
.navigation {
  display: flex;
  flex-direction: column;
  padding: var(--spacing-sm);
}

/* Tablet and up */
@media (min-width: 768px) {
  .navigation {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-md);
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .navigation {
    padding: var(--spacing-lg);
  }
}
```

### 2. Responsive Typography

```css
/* 
 * Fluid Typography
 * Purpose: Responsive font scaling for better readability
 */
.heading-1 {
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  font-weight: 700;
  line-height: var(--line-height-tight);
  margin-bottom: var(--spacing-lg);
}

.heading-2 {
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 600;
  line-height: var(--line-height-tight);
  margin-bottom: var(--spacing-md);
}

/* Responsive text scaling for Chuukese content */
.chuukese-text {
  font-size: clamp(1rem, 2.5vw, 1.125rem);
}

@media (max-width: 480px) {
  .chuukese-text {
    font-size: 1.125rem; /* Larger on small screens for readability */
  }
}
```

## Accessibility Standards

### 1. Focus Management

```css
/* 
 * Focus Styles
 * Purpose: Clear visual indication for keyboard navigation
 */
.btn:focus,
.form-input:focus,
.translation-input:focus {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

/* High contrast focus for better visibility */
@media (prefers-contrast: high) {
  .btn:focus,
  .form-input:focus {
    outline: 3px solid #000;
    outline-offset: 2px;
  }
}
```

### 2. Color and Contrast

```css
/* 
 * Color Accessibility
 * Purpose: Ensure sufficient contrast ratios
 */
:root {
  --text-contrast-ratio: 4.5; /* WCAG AA standard */
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  :root {
    --primary-color: #000;
    --text-color: #000;
    --background-color: #fff;
    --surface-color: #f0f0f0;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Utility Classes

### 1. Common Utilities

```css
/* Display utilities */
.d-none { display: none; }
.d-block { display: block; }
.d-inline { display: inline; }
.d-inline-block { display: inline-block; }
.d-flex { display: flex; }
.d-grid { display: grid; }

/* Text utilities */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }
.text-primary { color: var(--primary-color); }
.text-secondary { color: var(--secondary-color); }
.text-muted { color: var(--text-light); }

/* Responsive utilities */
@media (min-width: 768px) {
  .d-md-block { display: block; }
  .d-md-none { display: none; }
  .text-md-left { text-align: left; }
  .text-md-center { text-align: center; }
}
```

## Best Practices

### 1. Performance Optimization

- Use CSS custom properties for consistent theming
- Minimize the use of expensive properties (box-shadow, gradients)
- Optimize for critical rendering path
- Use efficient selectors (avoid deep nesting)

### 2. Maintainability

- Follow BEM naming convention
- Group related styles together
- Comment complex or non-obvious styles
- Use meaningful variable names

### 3. Cross-Browser Compatibility

- Test in major browsers (Chrome, Firefox, Safari, Edge)
- Use autoprefixer for vendor prefixes
- Provide fallbacks for modern CSS features
- Test with different font settings

### 4. Multilingual Considerations

- Support for RTL languages if needed
- Font stack that supports Unicode characters
- Proper spacing for accented characters
- Consider text expansion/contraction in different languages

## Validation Criteria

CSS should:

- ✅ Pass W3C CSS validation
- ✅ Meet WCAG 2.1 AA accessibility standards
- ✅ Display correctly across major browsers
- ✅ Support proper Chuukese text rendering
- ✅ Follow consistent naming conventions
- ✅ Include responsive breakpoints
- ✅ Optimize for performance and loading speed
