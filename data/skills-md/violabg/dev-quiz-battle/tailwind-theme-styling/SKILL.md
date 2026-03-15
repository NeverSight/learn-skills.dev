---
name: tailwind-theme-styling
description: Style the dev-quiz-battle app using Tailwind CSS v4 with OKLCH colors, dark mode support, and modern design patterns. Use when creating responsive layouts, applying themes, and implementing visual components.
license: MIT
metadata:
  author: dev-quiz-battle
  version: "1.0"
---

# Tailwind Theme Styling

This skill covers styling the dev-quiz-battle application with Tailwind CSS v4.

## Step-by-step instructions

### 1. Using Tailwind v4 Syntax

Tailwind 4 uses simplified syntax:

```css
@import "tailwindcss";

@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors;
  }

  .card {
    @apply rounded-lg border border-gray-200 shadow-sm p-6;
  }
}
```

### 2. OKLCH Color Format

Use OKLCH for CSS custom properties:

```css
:root {
  --color-primary: oklch(0.65 0.15 260);
  --color-accent: oklch(0.7 0.12 40);
  --color-success: oklch(0.65 0.15 150);
  --color-error: oklch(0.65 0.22 30);
}

.element {
  color: var(--color-primary);
}
```

### 3. Dark Mode Implementation

Use next-themes for theme switching:

```typescript
// In layout.tsx
import { ThemeProvider } from "@/components/theme-provider";

export default function RootLayout({ children }) {
  return (
    <html suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
```

### 4. Responsive Design

Use Tailwind breakpoints:

```typescript
export const ResponsiveLayout = ({ children }: Props) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {children}
    </div>
  );
};
```

### 5. Component Styling

Style game components with utility classes:

```typescript
export const GameCard = ({ title, children }: Props) => {
  return (
    <div className="rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm p-6 hover:shadow-md transition-shadow bg-white dark:bg-gray-900">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        {title}
      </h3>
      {children}
    </div>
  );
};
```

### 6. Animation and Transitions

Use Tailwind's animation utilities:

```typescript
export const LoadingSpinner = () => {
  return (
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
  );
};

export const FadeInComponent = ({ children }: Props) => {
  return <div className="animate-fade-in duration-300">{children}</div>;
};
```

### 7. Gradient Text

Create modern gradient effects:

```typescript
export const GradientHeading = ({ text }: Props) => {
  return (
    <h1 className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent text-4xl font-bold">
      {text}
    </h1>
  );
};
```

## Common Patterns

- **Card components**: Border, shadow, rounded corners
- **Buttons**: Primary, secondary, danger variants
- **Forms**: Input styling, error states, labels
- **Navigation**: Sticky headers, active states
- **Games**: Score displays, player cards, status badges

## Color Palette

Use these Tailwind colors throughout:

- **Primary**: `blue-500`, `blue-600`
- **Secondary**: `purple-500`, `purple-600`
- **Success**: `green-500`, `green-600`
- **Error**: `red-500`, `red-600`
- **Background**: `white`/`gray-900` (dark mode)

## Dark Mode Classes

Always include dark mode variants:

```typescript
className = "bg-white dark:bg-gray-900 text-gray-900 dark:text-white";
```

See [Theme Configuration Reference](references/THEME_CONFIG.md) for detailed color system.
