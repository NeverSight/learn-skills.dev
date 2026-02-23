---
name: apple-hig-designer
description: Design Apple-style iOS/macOS interfaces following Human Interface Guidelines. Creates HIG-compliant components with SF Symbols, San Francisco typography, and proper accessibility. Supports optional modern effects. Use when designing Apple-style UI, iOS/macOS interfaces, HIG-compliant components, or implementing design system specifications.
---

# Apple HIG Designer

A professional-grade frontend design skill that enables Claude Code to create interfaces following Apple's Human Interface Guidelines (HIG), achieving the quality standards of Apple's design team.

## When to Use This Skill

Activate this skill when users request:
- Apple-style or iOS/macOS-style interfaces
- HIG-compliant UI components
- SF Symbols integration
- San Francisco typography implementation
- Modern glass effects (optional, user must explicitly request)

**Trigger phrases:**
- "Design an Apple-style..."
- "Create a HIG-compliant..."
- "iOS/macOS style component"
- "苹果风格的界面"
- "符合 HIG 的设计"

---

## Core Design Principles

### The Four Pillars of Apple Design

1. **Clarity (清晰)**
   - Every element has a purpose
   - Eliminate unnecessary complexity
   - Users understand immediately without instructions
   - Use clear visual hierarchy

2. **Deference (尊重内容)**
   - UI elements support, not compete with content
   - Minimize chrome and visual noise
   - Let content be the hero
   - Use subtle backgrounds and borders

3. **Depth (层次)**
   - Create clear visual hierarchy through layers
   - Use shadows, blur, and translucency purposefully
   - Motion reinforces spatial relationships
   - Z-axis communicates importance

4. **Consistency (一致性)**
   - Familiar patterns across platforms
   - Predictable interactions
   - Unified visual language
   - Respect platform conventions

---

## Design System Specifications

### Typography System

**Font Family:** San Francisco (SF Pro)

```css
/* System Font Stack for Web */
:root {
  --font-system: -apple-system, BlinkMacSystemFont, 'SF Pro Display',
                 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
  --font-mono: 'SF Mono', SFMono-Regular, Menlo, Monaco, monospace;
}

/* Font Size Scale (iOS) */
--text-caption2: 11px;    /* Caption 2 */
--text-caption1: 12px;    /* Caption 1 */
--text-footnote: 13px;    /* Footnote */
--text-subhead: 15px;     /* Subheadline */
--text-body: 17px;        /* Body - Default */
--text-headline: 17px;    /* Headline (semibold) */
--text-title3: 20px;      /* Title 3 */
--text-title2: 22px;      /* Title 2 */
--text-title1: 28px;      /* Title 1 */
--text-large-title: 34px; /* Large Title */
```

**Typography Rules:**
- Use SF Pro Display for sizes ≥ 20pt
- Use SF Pro Text for sizes < 20pt
- Maintain consistent line-height (1.2-1.5)
- Use weight for hierarchy, not just size

### Color System

```css
/* Apple System Colors - Light Mode */
:root {
  /* Primary Colors */
  --system-blue: #007AFF;
  --system-green: #34C759;
  --system-indigo: #5856D6;
  --system-orange: #FF9500;
  --system-pink: #FF2D55;
  --system-purple: #AF52DE;
  --system-red: #FF3B30;
  --system-teal: #5AC8FA;
  --system-yellow: #FFCC00;

  /* Gray Scale */
  --system-gray: #8E8E93;
  --system-gray2: #AEAEB2;
  --system-gray3: #C7C7CC;
  --system-gray4: #D1D1D6;
  --system-gray5: #E5E5EA;
  --system-gray6: #F2F2F7;

  /* Semantic Colors */
  --label-primary: #000000;
  --label-secondary: rgba(60, 60, 67, 0.6);
  --label-tertiary: rgba(60, 60, 67, 0.3);
  --label-quaternary: rgba(60, 60, 67, 0.18);

  /* Backgrounds */
  --bg-primary: #FFFFFF;
  --bg-secondary: #F2F2F7;
  --bg-tertiary: #FFFFFF;

  /* Separators */
  --separator: rgba(60, 60, 67, 0.29);
  --separator-opaque: #C6C6C8;
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  :root {
    --system-blue: #0A84FF;
    --system-green: #30D158;
    --system-indigo: #5E5CE6;
    --system-orange: #FF9F0A;
    --system-pink: #FF375F;
    --system-purple: #BF5AF2;
    --system-red: #FF453A;
    --system-teal: #64D2FF;
    --system-yellow: #FFD60A;

    --system-gray: #8E8E93;
    --system-gray2: #636366;
    --system-gray3: #48484A;
    --system-gray4: #3A3A3C;
    --system-gray5: #2C2C2E;
    --system-gray6: #1C1C1E;

    --label-primary: #FFFFFF;
    --label-secondary: rgba(235, 235, 245, 0.6);
    --label-tertiary: rgba(235, 235, 245, 0.3);
    --label-quaternary: rgba(235, 235, 245, 0.18);

    --bg-primary: #000000;
    --bg-secondary: #1C1C1E;
    --bg-tertiary: #2C2C2E;

    --separator: rgba(84, 84, 88, 0.6);
    --separator-opaque: #38383A;
  }
}
```

### Spacing System

**8pt Grid System:**
```css
:root {
  --space-1: 4px;   /* Extra small */
  --space-2: 8px;   /* Small */
  --space-3: 12px;  /* Medium-small */
  --space-4: 16px;  /* Medium */
  --space-5: 20px;  /* Medium-large */
  --space-6: 24px;  /* Large */
  --space-8: 32px;  /* Extra large */
  --space-10: 40px; /* 2X large */
  --space-12: 48px; /* 3X large */
}
```

**Touch Target Requirements:**
- **iOS:** Minimum 44×44 points
- **visionOS:** Minimum 60 points tap area
- Always add sufficient padding for small visual elements

### Border Radius (Concentric Design)

```css
:root {
  /* Base radius values */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  --radius-2xl: 24px;
  --radius-full: 9999px; /* Capsule */
}

/* Concentric Rule: inner_radius + padding = outer_radius */
/* Example: 8px inner + 8px padding = 16px outer */
```

---

## Component Patterns

The following components should follow Apple HIG conventions. For complete CSS implementations, see [resources/design-tokens.css](resources/design-tokens.css) and [resources/ui-patterns.md](resources/ui-patterns.md). For React component examples, see [resources/components.jsx](resources/components.jsx).

### Buttons
- **Primary:** Capsule shape (`border-radius: 9999px`), `min-height: 44px`, system-blue background, white text, 600 weight
- **Secondary:** Same capsule shape, system-blue text on `rgba(0, 122, 255, 0.1)` background
- **Press feedback:** `scale(0.98)` on `:active`

### Glass Effect (Optional - Only When Requested)
- **Only use when user explicitly requests** glass/frosted effects
- Default designs should use solid backgrounds for readability and performance
- `backdrop-filter: blur(20px) saturate(180%)` with semi-transparent background
- Always provide non-glass fallback

### Cards
- **Default:** Solid background (`--bg-tertiary`), `border-radius: 16px`, subtle box-shadow
- **Grouped style:** `--bg-secondary` outer with `--bg-tertiary` inner items, separated by `--separator`

### Input Fields
- `min-height: 44px`, `--bg-secondary` background, `border-radius: 12px`
- Focus state: `box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.3)`

### Tab Bars
- Position fixed at bottom, `height: 49px` + safe-area padding
- Minimum 44x44pt touch targets per tab
- Always display text labels (never icon-only)
- Use filled SF Symbols for selected state, outline for unselected
- Support badge for notifications (red oval, white text)

### Toolbars
- Three sections: leading (back/title), center (tools), trailing (actions)
- Maximum 3 item groups
- Use SF Symbols without borders
- Primary action uses `.prominent` style on trailing side
- Back button: circular with symbol only (no text)

### Sheets
- Detents: `large` (100%), `medium` (50%)
- Include grabber indicator (36x5px, centered)
- Done button: top-right; Cancel button: top-left
- Semi-transparent backdrop `rgba(0,0,0,0.4)`

### Alerts
- Use only for critical information (sparingly)
- Maximum 3 buttons; use specific verb titles, avoid "OK"
- Cancel: leading side; Destructive: only for unintended destructive actions
- Width: 270px, `border-radius: 14px`

### Lists and Tables
- Minimum row height: 44px
- Info button: reveals details without navigation
- Disclosure indicator (>): navigates to subview
- Grouped style: 10px border-radius, inset separators start at 60px

---

## Animation Guidelines

### Timing Functions

```css
:root {
  /* Apple's preferred easing */
  --ease-default: cubic-bezier(0.25, 0.1, 0.25, 1);
  --ease-in: cubic-bezier(0.42, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.58, 1);
  --ease-in-out: cubic-bezier(0.42, 0, 0.58, 1);

  /* Spring-like easing */
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

### Duration Scale

```css
:root {
  --duration-instant: 100ms;  /* Micro-interactions */
  --duration-fast: 200ms;     /* Hover, focus states */
  --duration-normal: 300ms;   /* Standard transitions */
  --duration-slow: 500ms;     /* Complex animations */
}
```

### Interaction Feedback

```css
/* Press feedback */
.interactive {
  transition: transform var(--duration-instant) var(--ease-out);
}

.interactive:active {
  transform: scale(0.97);
}

/* Hover glow */
.interactive:hover {
  box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.15);
}
```

---

## SF Symbols Integration

### Rendering Modes

1. **Monochrome:** Single color for all layers
2. **Hierarchical:** Opacity variations for depth
3. **Palette:** Custom colors per layer
4. **Multicolor:** Apple's intrinsic symbol colors

### Usage Guidelines

- **Toolbar/Navigation:** Use outline variant
- **Tab Bar:** Use fill variant
- **Match text size:** Symbols auto-align with SF font
- **Provide text alternatives:** Always include aria-label

### Web Implementation (Icon Font Alternative)

```html
<!-- Using SF Symbols via system font -->
<span class="sf-symbol" aria-label="Settings">􀣋</span>

<!-- Or use equivalent system icons -->
<svg class="icon" aria-hidden="true">
  <use href="#icon-gear"></use>
</svg>
```

---

## Accessibility Requirements

### Color Contrast
- **Normal text:** 4.5:1 minimum (WCAG AA)
- **Large text:** 3:1 minimum
- **Interactive elements:** Clearly distinguishable states

### Motion
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Semantic HTML
```html
<!-- Always use semantic elements -->
<button type="button">Action</button>
<nav aria-label="Main navigation">...</nav>
<main role="main">...</main>
```

---

## Output Format

When generating Apple-style UI code, always include:

1. **Complete, runnable code** (CSS/React/Vue)
2. **Light/Dark mode support** via CSS custom properties
3. **Design rationale** explaining HIG compliance
4. **Responsive breakpoints** for different devices
5. **Accessibility attributes** (aria-*, role, etc.)

### Default Behavior

- **Use solid backgrounds by default** for better readability
- **Glass/blur effects only when user explicitly requests**
- **Always provide non-glass fallback** for browsers without backdrop-filter support

### Example Output Structure

```jsx
/**
 * Apple HIG Compliant Component
 *
 * Design Decisions:
 * - Uses SF Pro system font stack for native feel
 * - 44pt minimum touch target for accessibility
 * - Capsule shape for primary actions (HIG recommendation)
 * - Solid background for optimal readability
 * - Supports prefers-color-scheme for auto theming
 */

const AppleButton = ({ children, variant = 'primary', ...props }) => {
  return (
    <button
      className={`btn btn-${variant}`}
      {...props}
    >
      {children}
    </button>
  );
};
```

---

## Best Practices Checklist

Before finalizing any design output, verify:

- [ ] **Typography:** Using SF Pro with correct size thresholds
- [ ] **Colors:** System colors with Light/Dark variants
- [ ] **Spacing:** Following 8pt grid
- [ ] **Touch targets:** Minimum 44×44pt
- [ ] **Border radius:** Concentric relationships maintained
- [ ] **Animations:** Using Apple-standard easing curves
- [ ] **Accessibility:** WCAG AA compliant, reduced motion support
- [ ] **Consistency:** Matches platform conventions
- [ ] **Backgrounds:** Solid by default, glass only when requested

---

## Additional Resources

### Local References (read these for detailed implementations)
- For complete design patterns and real-world examples, see [REFERENCE.md](REFERENCE.md)
- For CSS custom properties and design tokens, see [resources/design-tokens.css](resources/design-tokens.css)
- For React component templates, see [resources/components.jsx](resources/components.jsx)
- For detailed UI pattern documentation, see [resources/ui-patterns.md](resources/ui-patterns.md)

### External References
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines)
- [Apple Design Resources](https://developer.apple.com/design/resources/)
- [SF Symbols](https://developer.apple.com/sf-symbols/)
- [Apple Fonts](https://developer.apple.com/fonts/)

---

*This skill ensures Claude Code produces interfaces that meet Apple's exacting design standards, creating cohesive, accessible, and beautiful user experiences.*
