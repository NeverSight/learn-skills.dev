---
name: css-theming-assistant
description: Specialized skill for maintaining and extending the DWP Hours Tracker's design system using CSS custom properties for centralized theming.
---

# CSS Theming Assistant - DWP Hours Tracker Design System

## Description

A specialized skill for maintaining and extending the DWP Hours Tracker's design system, which uses CSS custom properties for centralized theming. The system provides semantic color naming, light/dark theme support, and automated enforcement through Stylelint to ensure consistency across all components.

## Design System Overview

### Token Structure

The design system is centralized in `client/tokens.css` with the following categories:

- **Color Palette**: Base grays, brand blues, semantic reds/greens/purples/oranges
- **Typography**: Font families, sizes, weights, and line heights
- **Spacing**: Consistent spacing scale (xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px, 2xl: 48px)
- **Borders**: Widths, radii, and styles
- **Shadows**: Small to extra-large shadow definitions
- **Semantic Mappings**: Purpose-driven color assignments (primary, error, success, etc.)

### Naming Conventions

- Colors: `--color-{semantic|palette}-{variant}` (e.g., `--color-primary`, `--color-blue-600`)
- Typography: `--font-{property}-{variant}` (e.g., `--font-size-lg`, `--font-weight-bold`)
- Spacing: `--space-{size}` (e.g., `--space-md`)
- Borders: `--border-{property}-{variant}` (e.g., `--border-radius-lg`)
- Shadows: `--shadow-{size}` (e.g., `--shadow-md`)

### Token Usage Guidelines

This section explains the conceptual purpose of each token category and when to apply them for consistent theming.

#### Color Tokens

- `--color-background`: The main page or application background color. Use for the root background or large areas that serve as the base layer.
- `--color-surface`: Background color for cards, panels, modals, and other elevated elements that sit above the main background. Provides visual hierarchy by creating distinct content areas.
- `--color-surface-hover`: Background color for interactive surface elements when hovered or focused. Enhances user feedback and indicates clickable areas.
- `--color-text`: Primary text color for headings, body text, and important labels. Ensures high contrast and readability as the default text color.
- `--color-text-secondary`: Secondary text color for subtitles, descriptions, and less important information. Provides visual hierarchy in text content without overwhelming the primary text.
- `--color-text-muted`: Muted text color for placeholders, disabled states, and tertiary information. Used when text needs to be de-emphasized or appears less prominent.
- `--color-border`: Default border color for form inputs, dividers, and structural elements. Creates subtle separation between UI elements.
- `--color-border-hover`: Border color for interactive elements when hovered or focused. Indicates interactivity and improves accessibility.
- `--color-primary`: Primary brand color for buttons, links, and key interactive elements. Represents the main action or brand identity in the interface.
- `--color-primary-hover`: Hover state for primary elements. Provides visual feedback on interaction with primary actions.
- `--color-primary-light`: Light variant of primary color, often used for backgrounds or subtle highlights related to primary elements.
- `--color-secondary`: Secondary color for less prominent buttons, links, or accents. Supports primary color without competing for attention.
- `--color-secondary-hover`: Hover state for secondary elements. Maintains consistency with primary hover patterns.
- `--color-error`: Color for error states, validation messages, and destructive actions. Indicates problems, warnings, or critical issues.
- `--color-error-light`: Light background for error-related areas, such as error message containers or validation feedback.
- `--color-success`: Color for success states, confirmations, and positive feedback. Indicates successful operations or positive outcomes.
- `--color-success-light`: Light background for success-related areas, such as confirmation messages or success indicators.
- `--color-warning`: Color for warning states and cautionary information. Indicates potential issues that require attention.
- `--color-warning-light`: Light background for warning-related areas, such as cautionary messages or alerts.
- `--color-info`: Color for informational messages and neutral states. Used for general information that doesn't fit error/success/warning categories.
- `--color-info-light`: Light background for info-related areas, such as informational tooltips or neutral messages.
- `--color-disabled`: Color for disabled states and inactive elements. Provides consistent visual feedback for non-interactive components.
- `--color-success-dark`: Darker variant of success color for emphasis or text on light backgrounds.
- `--color-border-light`: Lighter border color for subtle separations and secondary dividers.

#### Typography Tokens

- `--font-family-base`: Default font family for body text and general use. Provides the primary typeface for most text content.
- `--font-family-heading`: Font family for headings and titles. May differ from base font for better hierarchy and emphasis.
- `--font-size-base`: Base font size, typically 1rem. Serves as the reference size for scaling other text elements.
- `--font-size-xs`, `--font-size-sm`, `--font-size-md`, `--font-size-lg`, `--font-size-xl`, `--font-size-2xl`: Scaled font sizes for text hierarchy. Use progressively larger sizes for headings and smaller sizes for captions.
- `--font-weight-normal`, `--font-weight-medium`, `--font-weight-semibold`, `--font-weight-bold`: Font weights for emphasis. Apply higher weights to important text and lower weights to body text.
- `--line-height-base`: Standard line height for readability. Use for most body text to ensure comfortable reading.
- `--line-height-tight`: Tighter line height for compact text. Apply to headings or dense information where space is limited.

#### Spacing Tokens

- `--space-xs`: Smallest spacing unit (4px), for tight spacing like padding between small elements or fine adjustments.
- `--space-sm`: Small spacing (8px), for input padding, small gaps between elements, or compact layouts.
- `--space-md`: Medium spacing (16px), standard padding and margins for most UI elements.
- `--space-lg`: Large spacing (24px), for section spacing or larger gaps between related content groups.
- `--space-xl`: Extra large spacing (32px), for major layout gaps or separation between distinct sections.
- `--space-2xl`: Double extra large spacing (48px), for page sections or significant visual breaks.
- `--space-header`: Specific spacing for header elements, ensuring consistent header layouts.

#### Border Tokens

- `--border-width`: Standard border width (1px). Use for most borders to maintain consistency.
- `--border-width-thick`: Thicker border width (2px). Apply for emphasis or to create stronger visual separation.
- `--border-radius`: Default border radius (4px). Use for buttons, inputs, and cards to soften edges.
- `--border-radius-sm`, `--border-radius-md`, `--border-radius-lg`, `--border-radius-xl`: Different radius sizes for various UI elements. Smaller radii for compact elements, larger for spacious ones.
- `--border-style-solid`: Solid border style. The primary border style for structural elements.

#### Shadow Tokens

- `--shadow-sm`: Small shadow for subtle elevation. Use for slight depth on flat elements.
- `--shadow-md`: Medium shadow for cards and panels. Provides standard elevation for content containers.
- `--shadow-lg`: Large shadow for modals and overlays. Creates strong visual separation for floating elements.
- `--shadow-xl`: Extra large shadow for prominent elements. Use sparingly for elements requiring maximum attention.

#### Animation Tokens

- `--duration-fast`: Quick animations (150ms). Use for immediate feedback like button presses or small state changes.
- `--duration-normal`: Standard animations (250ms). Apply to most transitions for smooth user experience.
- `--duration-slow`: Slow animations (400ms). Use for larger state changes or entering/exiting elements.
- `--easing-standard`: Standard easing curve. Provides natural motion for most animations.
- `--easing-decelerate`: Decelerating easing. Use when elements come to rest or slow down.
- `--easing-accelerate`: Accelerating easing. Apply when elements start moving or speed up.

### Theme Support

- **Automatic**: Uses `prefers-color-scheme` media queries for system preference detection
- **Manual**: Supports `data-theme="light|dark"` attributes on root element for testing/overrides
- **Default**: Light theme when no preference detected

## Trigger

Activate this skill when users ask about:

- Adding new design tokens or modifying existing ones
- Converting hardcoded styles to use design tokens
- Implementing new components with consistent theming
- Modifying color schemes or theme behavior
- Ensuring CSS follows design system conventions
- Troubleshooting theme-related issues

## Response Pattern

When activated, follow this structured approach:

1. **Review Current Implementation**: Check `client/tokens.css` and component styles to understand current token usage
2. **Validate Token Usage**: Ensure all colors use `var()` references, no hardcoded values
3. **Apply Semantic Naming**: Use purpose-driven names (primary, error, success) over color-specific names (blue, red)
4. **Update Tokens.css**: Add new tokens to the centralized file following established patterns
5. **Apply Tokens**: Modify styles to reference new/updated tokens
6. **Test Theme Consistency**: Verify changes work in both light and dark themes
7. **Run Enforcement**: Execute `npm run lint` to ensure Stylelint passes (bans hardcoded colors)

## Stylelint Enforcement

The system uses Stylelint with custom rules:

- Bans hardcoded colors in `color`, `background-color`, and `border-color` properties
- Requires all color values to use `var()` references
- Ignores `client/tokens.css` (where base colors are defined)
- Extends standard Stylelint config for additional consistency

## CSS Extensions System

The project provides reusable CSS extension libraries in `client/css-extensions/`. These extensions use constructable stylesheets (shared singletons) adopted into shadow roots, keeping styles modular and consistent with the design token system.

### Architecture

```
client/css-extensions/
├── index.ts              # Facade — re-exports all extensions
├── animations/           # Keyframes, utility classes, JS animation helpers
│   ├── animations.ts     # CSS source (keyframes + utility classes)
│   ├── index.ts          # Constructable stylesheet + adoptAnimations()
│   └── types.ts          # AnimationHandle interface
└── toolbar/              # Toolbar layout utility
    ├── toolbar.ts        # CSS source (.toolbar class)
    └── index.ts          # Constructable stylesheet + adoptToolbar()
```

### Token Integration

All CSS extensions reference tokens from `tokens.css` via `var()` — no hardcoded values. This ensures extensions respect both light and dark themes automatically:

- Animation durations: `var(--duration-normal)`, `var(--duration-fast)`
- Animation easings: `var(--easing-standard)`, `var(--easing-decelerate)`
- Toolbar spacing: `var(--space-sm)`, `var(--space-md)`

### Adding New Extensions

When creating a new CSS extension:

1. Create `client/css-extensions/<name>/<name>.ts` with a CSS source string using `var()` tokens
2. Create `client/css-extensions/<name>/index.ts` with a constructable stylesheet singleton and `adopt<Name>()` helper
3. Re-export from `client/css-extensions/index.ts`
4. Include `@media (prefers-reduced-motion: reduce)` overrides for any animations or transitions

## Component Implementation

Components should:

- Use shadow DOM for style isolation
- Reference tokens via `var()` in inline styles
- Avoid hardcoded color/spacing values
- Support both light and dark themes automatically

## Examples

- "Add a new warning color variant to the theme"
- "Convert hardcoded colors to use design tokens"
- "How do I add spacing to a new component?"
- "Fix this component to work in dark mode"
- "What's the correct token for primary button colors?"

## Additional Context

This skill maintains the project's vanilla CSS approach with no CSS-in-JS frameworks. All theming is handled through CSS custom properties, ensuring compatibility with shadow DOM components and build optimization via esbuild. The system prioritizes accessibility with proper contrast ratios in both themes and follows WCAG guidelines.

## Comprehensive Theme Implementation

### Theme Behavior

- **System Preference Detection**: Uses CSS `prefers-color-scheme` media query to detect the user's system theme setting
- **Automatic Switching**:
  - If system is set to dark mode → Uses dark theme
  - If system is set to light mode → Uses light theme
  - If no system preference is set → Defaults to light theme
- **Real-time Updates**: Themes switch automatically when the user changes their system theme settings

### Implementation Details

- **Semantic Color Naming**: Colors are named by their semantic purpose (e.g., `--color-primary`, `--color-error`) rather than appearance (e.g., `--color-blue`, `--color-red`), following CSS-Tricks best practices for maintainable theming
- **CSS Custom Properties Structure**: Theme variables are organized hierarchically:
  - **Base Colors**: Raw color values (e.g., `--color-gray-100: #f5f5f5`)
  - **Semantic Colors**: Purpose-driven assignments (e.g., `--color-primary: var(--color-blue-600)`)
  - **Theme Overrides**: Light/dark specific adjustments using `@media (prefers-color-scheme: dark)`
- **Media Query Integration**: `@media (prefers-color-scheme: dark)` queries apply dark theme styles automatically
- **Fallback Support**: Light theme serves as the default fallback when no preference is detected
- **Accessibility**: All themes maintain proper contrast ratios and accessibility standards
- **Performance**: Zero JavaScript overhead - theming is handled entirely through CSS

**CSS Structure Example:**

```css
:root {
  /* Base color palette */
  --color-gray-100: #f5f5f5;
  --color-gray-900: #111827;
  --color-blue-600: #2563eb;
  /* ... more base colors */

  /* Semantic mappings */
  --color-primary: var(--color-blue-600);
  --color-error: #dc2626;
  --color-text: #1f2937;
}

/* Dark theme overrides */
@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: #3b82f6;
    --color-text: #f9fafb;
  }
}
```

### Key Features

- **Seamless Integration**: No theme toggle buttons or manual selection required
- **Consistent Experience**: All components and UI elements adapt automatically
- **Battery Friendly**: Respects system settings that may optimize for battery life in dark mode
- **Cross-Platform**: Works consistently across different operating systems and browsers
- **Maintainable**: Semantic naming and hierarchical structure make theme updates easy

## Single-Page Print Scaling Pattern

When a page needs to fit entirely on one printed page (regardless of paper size), use the following pattern combining CSS print token overrides with JavaScript dynamic zoom scaling.

### Why `beforeprint` Is Insufficient

The `beforeprint` / `afterprint` window events only fire during actual printing (Ctrl+P). They do **not** fire when Chrome DevTools CSS print emulation mode is activated, which makes development and testing difficult. Use `window.matchMedia("print")` instead — its `change` event fires in both scenarios.

### Implementation Pattern

```typescript
export class MyPage extends BaseComponent {
  private _printMQ: MediaQueryList | null = null;
  private _rafId = 0;

  // Arrow-function handlers for stable add/remove by reference
  private _handlePrintChange = (e: MediaQueryListEvent): void => {
    if (e.matches) {
      this._scaleToFitPage();
    } else {
      this._resetScale();
    }
  };

  private _handleResize = (): void => {
    if (!this._printMQ?.matches) return;
    cancelAnimationFrame(this._rafId);
    this._rafId = requestAnimationFrame(() => this._scaleToFitPage());
  };

  connectedCallback() {
    super.connectedCallback();

    // matchMedia("print") fires in DevTools print emulation AND real printing
    this._printMQ = window.matchMedia("print");
    this._printMQ.addEventListener("change", this._handlePrintChange);
    window.addEventListener("beforeprint", this._handleResize);
    window.addEventListener("afterprint", () => this._resetScale());
    window.addEventListener("resize", this._handleResize);

    // Handle page load while already in print emulation mode
    if (this._printMQ.matches) {
      this._scaleToFitPage();
    }
  }

  disconnectedCallback() {
    this._resetScale();
    cancelAnimationFrame(this._rafId);
    this._printMQ?.removeEventListener("change", this._handlePrintChange);
    window.removeEventListener("beforeprint", this._handleResize);
    window.removeEventListener("resize", this._handleResize);
    this._printMQ = null;
    super.disconnectedCallback();
  }

  /**
   * Scale document.body to fit all content on one printed page.
   * Must target document.body (not a shadow DOM element) so the
   * entire page including header scales uniformly.
   */
  private _scaleToFitPage(): void {
    const body = document.body;
    body.style.zoom = "";
    const contentHeight = body.scrollHeight;
    const pageHeight = window.innerHeight;
    if (contentHeight > pageHeight && pageHeight > 0) {
      const scale = Math.floor((pageHeight / contentHeight) * 100) / 100;
      body.style.zoom = String(scale);
    }
  }

  private _resetScale(): void {
    document.body.style.zoom = "";
  }
}
```

### Key Design Decisions

1. **Scale `document.body`, not a shadow DOM wrapper**: Scaling a shadow DOM element only shrinks the component's content — the header, nav, and other page-level elements remain full-size and still cause overflow. Applying `zoom` to `document.body` scales everything uniformly.

2. **Use `matchMedia("print")` over `beforeprint`/`afterprint`**: The `matchMedia` change event works in Chrome DevTools CSS print emulation mode, enabling visual testing without triggering a real print dialog.

3. **Manage listeners manually, not via `addListener`**: BaseComponent's `addListener` registers cleanup that runs during `renderTemplate()` / `requestUpdate()`. Print scaling listeners must survive re-renders, so add them in `connectedCallback` and remove them in `disconnectedCallback` directly.

4. **Throttle resize with `requestAnimationFrame`**: When the user resizes the DevTools responsive viewport while in print emulation, the resize event fires rapidly. RAF debouncing prevents layout thrashing.

5. **Check `_printMQ.matches` on connect**: If the page loads while already in print emulation mode, the `change` event won't fire. An initial check ensures scaling is applied immediately.

### Companion CSS

Print color overrides should be centralized in `client/media.css` by resetting design tokens under `@media print`, not scattered across component `css.ts` files with `!important`. Per-component `@media print` blocks should contain only layout rules (sizing, hiding elements, grid adjustments). See the task file `TASKS/readonly-pto-calendar-in-prior-year-summary.md` for the full print token strategy.</content>
<parameter name="filePath">/home/ca0v/code/ca0v/dwp-hours/.github/skills/css-theming-assistant/SKILL.md
