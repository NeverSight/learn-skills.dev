---
name: frontend-design
description: UI/UX design — color theory (60-30-10 rule), responsive layouts, WCAG accessibility, CSS/Tailwind patterns, wireframes, and visual review. Use when designing interfaces, choosing palettes, writing CSS, or fixing layout/accessibility issues.
license: Complete terms in LICENSE.txt
---

# Frontend Design

Expert guidance for creating beautiful, accessible, and responsive frontend designs using modern UI principles, color theory, and React+Tailwind CSS patterns.

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

## Activation Conditions

**Color & Design:**
- Choosing color palettes for applications
- Applying the 60-30-10 design rule
- Creating accessible color combinations
- Designing backgrounds, text, and accent colors
- Triggered on color selection, UI color palette design, gradient creation
- Ensuring WCAG contrast compliance

**UI Components & Layouts:**
- Creating React UI components with Tailwind CSS
- Building forms, modals, cards, badges, buttons, inputs, tabs, tables
- Implementing responsive design patterns
- Designing accessible UI components
- Working with states, variants, and animations

**Design Review & Correction:**
- Reviewing website design (local or remote)
- Checking UI for consistency issues
- Finding and fixing layout breakage
- Detecting responsive design problems
- Fixing accessibility violations
- "Review website design", "check UI", "fix layout", "find design problems"

## Part 1: Color Theory & Palettes

### Color Categories

- **Hot Colors**: Oranges, reds, and yellows - energizing, attention-grabbing
- **Cool Colors**: Blues, greens, and purples - calming, professional
- **Neutral Colors**: Grays and grayscale variations - balancing, sophisticated
- **Binary Colors**: Black and white - high contrast, stark

### The 60-30-10 Rule

**Golden Ratio for Color Balance:**

| Proportion | Role | Recommended Colors |
|------------|------|-------------------|
| **60%** | Primary/Dominant | Cool or light colors, neutrals |
| **30%** | Secondary | Complementary or analogous colors |
| **10%** | Accent | Complementary hot color for emphasis |

### Application in Code

```css
/* Tailwind CSS CSS Variables Approach */
:root {
  /* 60% - Primary (backgrounds, large areas) */
  --color-primary-bg: #f5f7fa;
  --color-primary-text: #374151;

  /* 30% - Secondary (cards, sections) */
  --color-secondary-bg: #ffffff;
  --color-secondary-border: #e5e7eb;
  --color-secondary-text: #1f2937;

  /* 10% - Accent (buttons, highlights) */
  --color-accent-primary: #3b82f6;
  --color-accent-hover: #2563eb;
  --color-accent-text: #ffffff;
}

/* Implementing in Tailwind config */
module.exports = {
  theme: {
    extend: {
      colors: {
        // 60% - Primary
        primary: {
          bg: 'var(--color-primary-bg)',
          text: 'var(--color-primary-text)',
        },
        // 30% - Secondary
        secondary: {
          bg: 'var(--color-secondary-bg)',
          border: 'var(--color-secondary-border)',
          text: 'var(--color-secondary-text)',
        },
        // 10% - Accent
        accent: {
          primary: 'var(--color-accent-primary)',
          hover: 'var(--color-accent-hover)',
          text: 'var(--color-accent-text)',
        },
      },
    },
  },
};
```

### Color Palette Examples

#### Modern Professional

```javascript
const palette = {
  // 60% - Primary
  primary: {
    background: '#f8fafc',  // Slate-50
    surface: '#ffffff',       // White
    text: '#334155',         // Slate-700
  },
  // 30% - Secondary
  secondary: {
    border: '#e2e8f0',      // Slate-200
    muted: '#94a3b8',        // Slate-400
    mutedForeground: '#64748b', // Slate-500
  },
  // 10% - Accent
  accent: {
    foreground: '#0f172a',   // Slate-900
    primary: '#3b82f6',      // Blue-500
    'primary-hover': '#2563eb', // Blue-600
    destructive: '#ef4444',  // Red-500
  },
};
```

#### Warm & Inviting

```javascript
const palette = {
  primary: {
    background: '#fff7ed',  // Orange-50
    surface: '#ffffff',
    text: '#431407',         // Orange-950
  },
  secondary: {
    border: '#fed7aa',        // Orange-200
    muted: '#fdba74',         // Orange-300
    mutedForeground: '#9a3412', // Orange-800
  },
  accent: {
    primary: '#f97316',      // Orange-500
    'primary-hover': '#ea580c', // Orange-600
  },
};
```

#### Deep & Dark

```javascript
const palette = {
  primary: {
    background: '#020617',  // Slate-950
    surface: '#0f172a',       // Slate-900
    text: '#f8fafc',         // Slate-50
  },
  secondary: {
    border: '#1e293b',        // Slate-800
    muted: '#64748b',          // Slate-500
    mutedForeground: '#94a3b8', // Slate-400
  },
  accent: {
    primary: '#6366f1',       // Indigo-500
    'primary-hover': '#4f46e5', // Indigo-600
  },
};
```

### Background Colors

#### ✅ Recommended

```css
/* Clean, readable backgrounds */
.bg-clean {
  background: #ffffff;                    /* Pure white */
  background: #fafbfc;                    /* Off-white */
  background: #f5f7fa;                    /* Light cool gray */
  background: #f0f2f5;                    /* Another neutral option */
}

/* Subtle gradients */
.bg-gradient-subtle {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f2 100%);
}

/* Color tints for sections */
.bg-tint-blue {
  background: #f1f5f9;          /* Light blue tint (10% blue) */
}
.bg-tint-green {
  background: #f0fdf4;         /* Light green tint */
}
```

#### ❌ Avoid

```css
/* Too dark or saturated */
.bg-bad {
  background: #2d3748;                    /* Dark background with light text can strain eyes */
  background: #ff0000;                    /* Pure red - never use as primary bg */
  background: repeating-linear-gradient(...);  /* Busy patterns - distracting */
}
```

---

## Part 2: Accessibility (WCAG Compliance)

### Web Content Accessibility Guidelines (WCAG 2.1 Level AA

#### Contrast Requirements

| Element | Minimum Contrast Ratio | Recommended |
|----------|----------------------|-------------|
| Normal text (< 18pt) | 4.5:1 | 7:1 |
| Large text (18pt+) or bold | 3:1 | 4.5:1 |
| Graphical objects and UI components | 3:1 | Higher is better |

### Contrast Validation

```javascript
// Calculate contrast ratio
function getContrastRatio(foreground: string, background: string): number {
  const lum1 = getLuminance(foreground);
  const lum2 = getLuminance(background);

  function getLuminance(hex: string): number {
    const rgb = hexToRgb(hex);
    const [r, g, b] = rgb.map(c => {
      c /= 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r[0] + 0.7152 * r[1] + 0.0722 * r[2];
  }

  const lighter = Math.max(lum1, lum2);
  const darker = Math.min(lum1, lum2);

  return (lighter + 0.05) / (darker + 0.05);
}

// Validate
const ratio = getContrastRatio('#3b82f6', '#ffffff');
console.log(ratio >= 4.5 ? '✅ WCAG AA compliant' : '❌ Not compliant');
```

### Accessibility Best Practices

#### Color Independence

```css
/* ❌ BAD - Color-only indication */
.success {
  color: green;
}
.error {
  color: red;
}

/* ✅ GOOD - Color + other visual indicator */
.success {
  color: #22c55e;
  border-left: 4px solid #22c55e;
  padding-left: 8px;
}
.error {
  color: #ef4444;
  border-left: 4px solid #ef4444;
  padding-left: 8px;
}
```

#### Focus States

```css
/* Keyboard navigation needs visible focus */
button:focus-visible,
a:focus-visible,
input:focus-visible,
select:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Tailwind */
<button className="focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
```

#### ARIA Labels

```jsx
// Icon-only buttons need labels
<button aria-label="Close dialog">
  <CloseIcon />
</button>

// Toggle buttons need pressed state
<button aria-pressed={isSelected}>
  {isSelected ? 'Selected' : 'Not selected'}
</button>

// Screen reader only text
<span className="sr-only">Required field</span>
```

### Responsive Typography

```css
/* Use relative units for scalability */
html {
  font-size: 100%;  /* Browser default usually 16px */
}

body {
  font-size: 1rem;      /* 16px */
  line-height: 1.5;      /* Readable line height */
}

/* Responsive scaling */
@media (min-width: 768px) {
  body {
    font-size: 1.125rem;  /* 18px on tablets+ */
  }
}
```

---

## Part 3: Responsive Design

### Mobile-First Approach

```css
/* Base styles - mobile by default */
.container {
  width: 100%;
  padding: 1rem;
  display: block;  /* Column layout on mobile */
}

/* Tablet - 768px+ */
@media (min-width: 768px) {
  .container {
    max-width: 720px;
    display: grid;  /* Grid on tablet */
    grid-template-columns: 1fr 1fr;
  }
}

/* Desktop - 1024px+ */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    grid-template-columns: 1fr 1fr 1fr;
  }
}

/* Large desktop - 1280px+ */
@media (min-width: 1280px) {
  .container {
    max-width: 1400px;
  }
}
```

### Tailwind Responsive Classes

```jsx
// Mobile-first approach
<div className="
  container
  mx-auto
  px-4        /* 16px padding on all sizes */
  py-8
">
  <div className="
    grid
    grid-cols-1      /* 1 column on mobile */
    md:grid-cols-2  /* 2 columns on tablet */
    lg:grid-cols-3  /* 3 columns on desktop */
    gap-4
  ">
    {items.map(item => (
      <Card key={item.id}>{item.content}</Card>
    ))}
  </div>
</div>
```

### Responsive Breakpoints (Tailwind Default)

| Breakpoint | Width | Device |
|-----------|--------|---------|
| sm | 640px | Small phones, portrait |
| md | 768px | Tablets, small laptops |
| lg | 1024px | Laptops, desktops |
| xl | 1280px | Large desktops |
| 2xl | 1536px | Extra large displays |

---

## Part 4: UI Component Patterns

### Button Component

```jsx
const buttonVariants = {
  primary: 'bg-blue-600 hover:bg-blue-700 text-white',
  secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-900',
  danger: 'bg-red-600 hover:bg-red-700 text-white',
  ghost: 'hover:bg-gray-100 text-gray-700',
  outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50',
};

const buttonSizes = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-5 py-2.5 text-lg',
  xl: 'px-6 py-3 text-xl',
};

export function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  isLoading = false,
  className = '',
  children,
  ...props
}) {
  return (
    <button
      disabled={disabled || isLoading}
      className={cn(
        // Base styles
        'rounded-lg font-medium transition-all',
        'focus:outline-none focus:ring-2 focus:ring-offset-2',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        // Variant styles
        buttonVariants[variant],
        // Size styles
        buttonSizes[size],
        // Additional classes
        className
      )}
      aria-busy={isLoading}
      {...props}
    >
      {isLoading ? (
        <LoadingSpinner size="sm" className="mr-2" />
      ) : null}
      {children}
    </button>
  );
}
```

### Card Component

```jsx
export function Card({
  children,
  variant = 'default',
  hoverable = false,
  className = '',
  ...props
}) {
  const variants = {
    default: 'bg-white border border-gray-200',
    elevated: 'bg-white shadow-lg border border-gray-100',
    outlined: 'bg-transparent border-2 border-gray-300',
    // Interactive variants
    hover: 'hover:shadow-xl transition-shadow duration-200',
  };

  return (
    <div
      className={cn(
        'rounded-lg overflow-hidden',
        variants.default,
        variants[variant],
        hoverable && variants.hover,
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

// Usage examples
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
  </CardHeader>
  <CardContent>
    <p>Card content goes here.</p>
  </CardContent>
</Card>
```

### Modal Component

```jsx
export function Modal({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
}) {
  // Prevent body scroll when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  // Close on escape key
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const sizes = {
    sm: 'max-w-md',
    md: 'max-w-2xl',
    lg: 'max-w-4xl',
    xl: 'max-w-6xl',
  };

  return createPortal(
    <div
      className="fixed inset-0 z-50"
      role="dialog"
      aria-modal="true"
      aria-labelledby={title}
    >
      <!-- Backdrop -->
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      <!-- Modal Container -->
      <div
        className="
          relative
          bg-white
          rounded-lg
          shadow-2xl
          mx-4
          my-8
          max-h-[calc(100vh-4rem)]
          overflow-y-auto
          {sizes[size]}
        "
      >
        <div className="flex items-center justify-between p-6 border-b">
          <h2 id="modal-title" className="text-2xl font-bold">
            {title}
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full"
            aria-label="Close modal"
          >
            <CloseIcon />
          </button>
        </div>
        <div className="p-6">
          {children}
        </div>
      </div>
    </div>,
    document.body
  );
}
```

### Form Component

```jsx
export function FormField({
  label,
  error,
  hint,
  required = false,
  children,
}) {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      {children}
      {hint && (
        <p className="mt-1 text-sm text-gray-500">{hint}</p>
      )}
      {error && (
        <p className="mt-1 text-sm text-red-600 flex items-center">
          <ExclamationIcon className="w-4 h-4 mr-1" />
          {error}
        </p>
      )}
    </div>
  );
}

// Usage
<FormField
  label="Email Address"
  error={errors.email}
  hint="We'll never share your email."
  required
>
  <input
    type="email"
    className="w-full px-3 py-2 border rounded-lg"
    {...register('email')}
  />
</FormField>
```

---

## Part 5: Design Review Checklist

### Visual Inspection Process

```markdown
## Design Review Workflow

### Step 1: Information Gathering
- [ ] Understand target audience and use cases
- [ ] Identify design constraints (brand, accessibility)
- [ ] Review existing design system/component library
- [ ] Gather user feedback or pain points

### Step 2: Visual Inspection
- [ ] Capture screenshots of current implementation
- [ ] Review layout at multiple viewport sizes
- [ ] Test color contrast with accessibility tools
- [ ] Check spacing and alignment
- [ ] Verify hierarchy and readability

### Step 3: Issue Identification
- [ ] Document发现的问题s with severity ratings
- [ ] Group related issues together
- [ ] Prioritize by impact on UX

### Step 4: Issue Fixing
- [ ] Fix issues at source code level
- [ ] Test fixes across browsers and devices
- [ ] Verify accessibility improvements
- [ ] Get user/stakeholder validation

### Step 5: Re-verification
- [ ] Compare before/after results
- [ ] Ensure no regressions introduced
- [ ] Document changes made
```

### Common Design Issues

#### Layout & Spacing Issues

```css
/* Issue: Inconsistent spacing */
.bad {
  padding: 10px;    /* Magic number */
  margin: 5px;      /* Different from padding */
}

/* Fix: Consistent spacing scale */
.good {
  padding: 1rem;     /* 16px - using scale */
  gap: 0.5rem;      /* 8px - consistent with scale */
}
```

#### Color Contrast Issues

```jsx
// Issue: Poor contrast
<button className="bg-blue-300 text-blue-100">
  Can't read this
</button>

// Fix: WCAG compliant
<button className="bg-blue-600 text-white">
  Readable
</button>
```

#### Typography Issues

```css
/* Issue: Line height too tight */
.bad {
  line-height: 1;  /* Can be hard to read */
}

/* Fix: Comfortable reading */
.good {
  line-height: 1.6;  /* Recommended for body text */
}
```

### Responsive Testing Checklist

```markdown
## Responsive Testing

### Viewport Testing
- [ ] Mobile: 375px (iPhone SE)
- [ ] Mobile: 414px (iPhone Max)
- [ ] Tablet: 768px (iPad)
- [ ] Desktop: 1024px (Small laptop)
- [ ] Desktop: 1440px (Large desktop)
- [ ] Desktop: 1920px (Fullscreen)

### Design Elements to Check
- [ ] Navigation menu accessible on all sizes
- [ ] Text readable at all breakpoints
- [ ] Images scale correctly
- [ ] Forms usable without horizontal scroll
- [ ] Touch targets ≥ 44x44px on mobile
- [ ] No horizontal scrollbar

### Content Flow
- [ ] Content stacks vertically on mobile
- [ ] Content uses grid/multi-column on larger screens
- [ ] Important content above the fold on all sizes
- [ ] No content cut off or hidden
```

---

## Part 6: Design System Integration

### Design Tokens

```javascript
// tokens.js - Centralized design tokens
export const tokens = {
  colors: {
    brand: {
      primary: '#3b82f6',
      secondary: '#6366f1',
      accent: '#f97316',
    },
    neutral: {
      50: '#f8fafc',
      100: '#f1f5f9',
      200: '#e2e8f0',
      300: '#cbd5e1',
      400: '#94a3b8',
      500: '#64748b',
      600: '#475569',
      700: '#334155',
      800: '#1e293b',
      900: '#0f172a',
      950: '#020617',
    },
  },
  spacing: {
    0: '0',
    1: '0.25rem',    /* 4px */
    2: '0.5rem',     /* 8px */
    3: '0.75rem',    /* 12px */
    4: '1rem',       /* 16px */
    5: '1.25rem',    /* 20px */
    6: '1.5rem',     /* 24px */
    8: '2rem',       /* 32px */
    10: '2.5rem',    /* 40px */
    12: '3rem',      /* 48px */
  },
  typography: {
    fontSizes: {
      xs: '0.75rem',   /* 12px */
      sm: '0.875rem',  /* 14px */
      base: '1rem',     /* 16px */
      lg: '1.125rem',  /* 18px */
      xl: '1.25rem',   /* 20px */
      '2xl': '1.5rem',  /* 24px */
      '3xl': '1.875rem', /* 30px */
      '4xl': '2.25rem',  /* 36px */
    },
    fontWeights: {
      normal: '400',
      medium: '500',
      semibold: '600',
      bold: '700',
    },
    lineHeights: {
      tight: '1.25',
      normal: '1.5',
      relaxed: '1.75',
    },
  },
  borderRadius: {
    none: '0',
    sm: '0.25rem',    /* 4px */
    DEFAULT: '0.375rem',  /* 6px */
    md: '0.5rem',     /* 8px */
    lg: '0.75rem',    /* 12px */
    xl: '1rem',       /* 16px */
    full: '9999px',
  },
  shadows: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    DEFAULT: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
  },
};

// Tailwind configuration with tokens
module.exports = {
  theme: {
    extend: {
      colors: tokens.colors,
      spacing: tokens.spacing,
      fontSize: tokens.typography.fontSizes,
      fontWeight: tokens.typography.fontWeights,
      lineHeight: tokens.typography.lineHeights,
      borderRadius: tokens.borderRadius,
      boxShadow: tokens.shadows,
    },
  },
};
```

---

## Frontend Design Best Practices

### Color & Visual Design
- [ ] Follow 60-30-10 rule for color balance
- [ ] Maintain contrast ratio ≥ 4.5:1 for normal text
- [ ] Use color for decoration, not sole indicator of meaning
- [ ] Document color palette and usage guidelines
- [ ] Test colorblind accessibility

### Typography
- [ ] Use max-width for optimal reading length (~65-75 characters)
- [ ] Maintain consistent line height (1.5-1.75 for body text)
- [ ] Use relative font sizes (rem, em) for scalability
- [ ] Establish type scale and use consistently
- [ ] Ensure heading hierarchy is clear

### Layout & Spacing
- [ ] Use consistent spacing scale (4px or 6px base)
- [ ] Ensure adequate white space for breathing room
- [ ] Align elements to grid for visual harmony
- [ ] Test responsive behavior at all breakpoints
- [ ] Maintain touch targets ≥ 44x44px on mobile

### Accessibility
- [ ] Keyboard navigation works without mouse
- [ ] Focus states are clearly visible
- [ ] ARIA labels on icon-only buttons
- [ ] Form fields have associated labels
- [ ] Images have alt text (except decorative)
- [ ] Screen reader only text for visual-only info
- [ ] Skip navigation for reaching main content

### Performance
- [ ] Optimize images (WebP, AVIF when supported)
- [ ] Use responsive images with srcset
- [ ] Implement code splitting for large bundles
- [ ] Lazy load offscreen images and components
- [ ] Minimize layout shifts (CLS) and paint issues (LCP)

---

## References & Resources

### Documentation
- [Tailwind Component Patterns](./references/tailwind-component-patterns.md) — Cards, forms, navigation, modals, tables, and skeleton loading patterns
- [Accessibility Checklist](./references/accessibility-checklist.md) — WCAG 2.2 checklist with React/HTML/ARIA code examples

### Scripts
- [Contrast Checker](./scripts/contrast-checker.py) — Python WCAG contrast ratio checker with batch mode for CSS files

### Examples
- [Responsive Recipe Card](./examples/responsive-recipe-card.md) — Complete React+Tailwind recipe card with responsive variants and states

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [react-development](../react-development/SKILL.md) | Implement designs as React components |
| [stitch-design](../stitch-design/SKILL.md) | Design system and component conversion |
| [web-design-reviewer](../web-design-reviewer/SKILL.md) | Visual review of implemented designs |
| [canvas-design](../canvas-design/SKILL.md) | Design philosophy and visual aesthetics |
