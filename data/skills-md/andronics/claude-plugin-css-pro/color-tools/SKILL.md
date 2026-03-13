---
name: color-tools
description: Color palette generation, contrast checking (WCAG), color space conversion, and color harmony tools. Ensures accessible and visually appealing color systems. Use when designing color schemes, checking accessibility, or creating design tokens.
allowed-tools: Read, Write, Edit
---

# Color Tools Skill

This skill helps you create accessible, harmonious color palettes and ensures your colors meet WCAG contrast requirements. I provide color calculations, palette generation, and accessibility validation.

## What I Can Do

### Color Contrast Checking
- Calculate contrast ratios
- Verify WCAG AA/AAA compliance
- Suggest accessible alternatives
- Check text/background combinations

### Palette Generation
- Create tint/shade scales (50-900)
- Generate color harmonies
- Build complementary palettes
- Design theme variations

### Color Conversions
- HEX ↔ RGB ↔ HSL
- Calculate opacity variations
- Generate CSS custom properties
- Create color tokens

### Accessibility Tools
- Find accessible color pairs
- Suggest minimum contrast fixes
- Validate interactive state colors
- Check large text requirements

## WCAG Contrast Requirements

### Minimum Ratios
- **Normal text**: 4.5:1 (AA), 7:1 (AAA)
- **Large text** (18px+ or 14px+ bold): 3:1 (AA), 4.5:1 (AAA)
- **UI components**: 3:1 (AA)
- **Graphical objects**: 3:1 (AA)

### Contrast Formula
Contrast Ratio = (L1 + 0.05) / (L2 + 0.05)
Where L1 is lighter color luminance and L2 is darker

## Example: Contrast Checking

**You**: "Check if #3b82f6 on white background is accessible"

**I'll provide**:
```
Color: #3b82f6 (Blue)
Background: #ffffff (White)

Contrast Ratio: 4.52:1

WCAG Compliance:
✓ Normal text AA (4.5:1 required) - PASS
✗ Normal text AAA (7:1 required) - FAIL
✓ Large text AA (3:1 required) - PASS
✓ Large text AAA (4.5:1 required) - PASS
✓ UI Components (3:1 required) - PASS

Recommendation:
For AAA compliance with normal text, use #2563eb (darker blue)
New contrast: 7.02:1 - Passes all requirements
```

## Palette Generation

### Tint & Shade Scale
```css
/* Generate 50-900 scale from base color */
:root {
  /* Base color: #3b82f6 */

  --color-blue-50: #eff6ff;   /* 90% lighter */
  --color-blue-100: #dbeafe;  /* 80% lighter */
  --color-blue-200: #bfdbfe;  /* 60% lighter */
  --color-blue-300: #93c5fd;  /* 40% lighter */
  --color-blue-400: #60a5fa;  /* 20% lighter */
  --color-blue-500: #3b82f6;  /* Base */
  --color-blue-600: #2563eb;  /* 20% darker */
  --color-blue-700: #1d4ed8;  /* 40% darker */
  --color-blue-800: #1e40af;  /* 60% darker */
  --color-blue-900: #1e3a8a;  /* 80% darker */
}

/* Usage guide:
 * 50-100: Backgrounds, subtle highlights
 * 200-300: Hover states, borders
 * 400-600: Primary UI, text on light backgrounds
 * 700-900: Text, emphasis, dark themes
 */
```

### Color Harmonies

#### Complementary Colors
```css
/* Base: #3b82f6 (Blue) */
:root {
  --color-primary: #3b82f6;      /* Blue (210°) */
  --color-complement: #f6823b;   /* Orange (30°) - opposite */
}
```

#### Analogous Colors
```css
/* Base: #3b82f6 (Blue) */
:root {
  --color-primary: #3b82f6;      /* Blue (210°) */
  --color-analogous-1: #3bf6db;  /* Cyan (180°) */
  --color-analogous-2: #823bf6;  /* Purple (270°) */
}
```

#### Triadic Colors
```css
/* Base: #3b82f6 (Blue) */
:root {
  --color-primary: #3b82f6;      /* Blue (210°) */
  --color-triadic-1: #f6db3b;    /* Yellow (90°) */
  --color-triadic-2: #db3bf6;    /* Magenta (330°) */
}
```

#### Split-Complementary
```css
/* Base: #3b82f6 (Blue) */
:root {
  --color-primary: #3b82f6;      /* Blue (210°) */
  --color-split-1: #f6db3b;      /* Yellow-Orange (45°) */
  --color-split-2: #f6493b;      /* Red-Orange (15°) */
}
```

## Accessible Color Palettes

### Light Theme
```css
:root {
  /* Backgrounds - Lightest colors */
  --color-bg: #ffffff;           /* Pure white */
  --color-bg-secondary: #f9fafb; /* Near white */
  --color-bg-tertiary: #f3f4f6;  /* Light gray */

  /* Text - Darkest colors (AAA contrast) */
  --color-text-primary: #111827;   /* 16.04:1 */
  --color-text-secondary: #4b5563; /* 8.49:1 */
  --color-text-tertiary: #6b7280;  /* 5.77:1 */

  /* Primary color (accessible) */
  --color-primary: #2563eb;      /* 7.02:1 on white */
  --color-primary-hover: #1d4ed8; /* 9.52:1 on white */

  /* Interactive states */
  --color-link: #2563eb;         /* 7.02:1 */
  --color-link-hover: #1d4ed8;   /* 9.52:1 */
  --color-link-visited: #7c3aed; /* 7.09:1 */

  /* Status colors (all AAA compliant) */
  --color-success: #047857;      /* 7.36:1 */
  --color-warning: #b45309;      /* 7.01:1 */
  --color-error: #dc2626;        /* 7.29:1 */
}
```

### Dark Theme
```css
[data-theme="dark"] {
  /* Backgrounds - Darkest colors */
  --color-bg: #111827;           /* Very dark gray */
  --color-bg-secondary: #1f2937; /* Dark gray */
  --color-bg-tertiary: #374151;  /* Medium-dark gray */

  /* Text - Lightest colors (AAA contrast) */
  --color-text-primary: #f9fafb;   /* 14.73:1 */
  --color-text-secondary: #d1d5db; /* 10.31:1 */
  --color-text-tertiary: #9ca3af;  /* 6.16:1 */

  /* Primary color (lighter for dark mode) */
  --color-primary: #60a5fa;      /* 7.38:1 on dark bg */
  --color-primary-hover: #93c5fd; /* 10.73:1 on dark bg */

  /* Status colors (adjusted for dark mode) */
  --color-success: #34d399;      /* 7.53:1 */
  --color-warning: #fbbf24;      /* 13.44:1 */
  --color-error: #f87171;        /* 7.03:1 */
}
```

## Color Conversion Examples

### HEX to RGB
```
#3b82f6 → rgb(59, 130, 246)

Calculation:
R: 3b (hex) = 59 (decimal)
G: 82 (hex) = 130 (decimal)
B: f6 (hex) = 246 (decimal)
```

### RGB to HSL
```
rgb(59, 130, 246) → hsl(217, 91%, 60%)

Calculation:
H: 217° (hue)
S: 91% (saturation)
L: 60% (lightness)
```

### Adding Opacity
```css
/* HEX with alpha */
--color-primary: #3b82f6;
--color-primary-10: #3b82f61a; /* 10% opacity */
--color-primary-50: #3b82f680; /* 50% opacity */

/* RGB with alpha */
--color-primary-rgb: 59, 130, 246;
--color-primary-10: rgba(var(--color-primary-rgb), 0.1);
--color-primary-50: rgba(var(--color-primary-rgb), 0.5);

/* HSL with alpha */
--color-primary: hsl(217, 91%, 60%);
--color-primary-10: hsl(217, 91%, 60%, 0.1);
--color-primary-50: hsl(217, 91%, 60%, 0.5);
```

## Color Token System

### Complete Token Architecture
```css
:root {
  /* 1. Global tokens - Raw colors */
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-gray-50: #f9fafb;
  --color-gray-900: #111827;

  /* 2. Semantic tokens - Purpose */
  --color-primary: var(--color-blue-600);
  --color-text-primary: var(--color-gray-900);
  --color-surface: var(--color-gray-50);

  /* 3. Component tokens - Specific */
  --button-bg-primary: var(--color-primary);
  --button-text-primary: white;
  --card-bg: var(--color-surface);
}
```

## Checking Interactive States

### Button States Example
```css
.button-primary {
  /* Default state */
  background: #2563eb;  /* 7.02:1 on white */
  color: white;

  /* Hover state */
  &:hover {
    background: #1d4ed8; /* 9.52:1 on white */
  }

  /* Focus state */
  &:focus-visible {
    outline: 2px solid #2563eb;
    outline-offset: 2px;
    /* Outline must have 3:1 contrast with adjacent colors */
  }

  /* Active/pressed state */
  &:active {
    background: #1e40af; /* 11.19:1 on white */
  }

  /* Disabled state */
  &:disabled {
    background: #93c5fd; /* 3.24:1 - may fail for text */
    color: #6b7280;     /* Reduced contrast acceptable when disabled */
    opacity: 0.6;
  }
}
```

## Color Accessibility Tips

### ✓ Good Practices
- Test all text/background combinations
- Check hover and focus states
- Verify status colors (success, warning, error)
- Don't rely on color alone (use icons/text too)
- Test with color blindness simulators
- Provide high contrast mode
- Use semantic color names

### ❌ Common Mistakes
- Light gray text on white (#999 on #fff = 2.85:1 - fails)
- Relying only on color for information
- Insufficient contrast in disabled states
- Forgetting to test dark mode
- Not checking focus indicators
- Ignoring links and interactive elements

## Example Usage

**You**: "Create an accessible blue palette for a light theme"

**I'll provide**:
```css
:root {
  /* Blue palette - All colors tested for accessibility */

  /* Primary actions - AAA compliant on white */
  --color-primary: #1d4ed8;      /* 9.52:1 */
  --color-primary-hover: #1e40af; /* 11.19:1 */

  /* Backgrounds */
  --color-primary-bg: #eff6ff;   /* Subtle background */
  --color-primary-border: #93c5fd; /* 3.24:1 - good for borders */

  /* Text on primary buttons */
  --color-primary-text: #ffffff; /* 9.52:1 on #1d4ed8 */

  /* Links */
  --color-link: #2563eb;         /* 7.02:1 - AAA for large text */
  --color-link-hover: #1d4ed8;   /* 9.52:1 - AAA */
  --color-link-visited: #7c3aed; /* 7.09:1 - AAA */

  /* Status indicators */
  --color-info: #0284c7;         /* 7.24:1 */
  --color-info-bg: #e0f2fe;      /* Background for info messages */
}

/* Usage example */
.button-primary {
  background: var(--color-primary);
  color: var(--color-primary-text);
}

.button-primary:hover {
  background: var(--color-primary-hover);
}

.link {
  color: var(--color-link);
}

.link:hover {
  color: var(--color-link-hover);
}
```

## Just Ask!

Tell me what you need:
- "Check contrast for #3b82f6 on white"
- "Generate a blue color palette"
- "Create accessible dark theme colors"
- "Find a complementary color for #2563eb"
- "Make this color more accessible"
- "Convert #3b82f6 to RGB and HSL"

I'll help you create accessible, beautiful color systems!
