---
name: design-system-analyzer
description: Use when analyzing UI screenshots or designs to extract and document design system elements. Analyzes images to identify colors, typography, spacing, components, and patterns, then generates a structured design system with design tokens and CSS snippets. Ideal for reverse-engineering designs, creating style guides, or documenting existing UIs.
---

# Design System Analyzer

## Overview

This skill enables systematic analysis of UI screenshots and design images to extract and document design system elements. Extract colors, typography, spacing patterns, and component styles from any UI, then generate a comprehensive, interactive design system with design tokens and CSS snippets ready for implementation.

## When to Use This Skill

Use this skill when:
- Analyzing UI screenshots to understand the design system
- Reverse-engineering a design to create a style guide
- Documenting an existing UI's design patterns
- Converting visual designs into code-ready design tokens
- Creating a design system from mockups or screenshots
- Auditing UI consistency across different screens

## Analysis Process

When analyzing a UI image, systematically examine and document the following elements in order:

### 1. Color Analysis

Identify and categorize all colors visible in the UI:

**Primary Colors:**
- Main brand colors used for primary actions and key elements
- Note hex codes, usage context, and prominence

**Secondary Colors:**
- Supporting colors for secondary actions and elements
- Document their relationship to primary colors

**Accent Colors:**
- Highlight colors for attention-grabbing elements
- Success, warning, error, and info states

**Background Colors:**
- Base backgrounds (light/dark themes)
- Card backgrounds
- Surface colors and overlays

**Text Colors:**
- Heading colors
- Body text colors
- Muted/secondary text colors
- Link colors and states (default, hover, visited)

**Gradients (if needed)**
Some design are heavy on gradients, document them if needed

For each color, provide:
- Hex code
- RGB values
- Usage context
- Semantic naming suggestion (e.g., `--color-primary-500`)

### 2. Typography Analysis

Examine all text elements and document:

**Font Families:**
- Identify fonts used (if recognizable)
- Suggest web-safe or similar alternatives if needed

**Heading Styles (h1-h6):**
- Font size (px, rem, or estimate)
- Font weight
- Line height
- Letter spacing
- Text color
- Margin/padding patterns

**Body Text Styles:**
- Default body font size and line height
- Paragraph spacing
- Text color and contrast ratios

**Special Text Styles:**
- Links
- Captions
- Labels
- Button text
- Code/monospace text
- Any other distinct text treatments

For each style, generate:
- CSS class definitions
- Design token recommendations
- Usage guidelines

### 3. Spacing Analysis

Analyze spatial relationships and document:

**Spacing Scale:**
- Identify the spacing unit (likely 4px or 8px base)
- Document the scale (e.g., 4, 8, 12, 16, 24, 32, 48, 64)

**Padding Patterns:**
- Component internal spacing
- Button padding
- Card padding
- Input field padding

**Margin Patterns:**
- Vertical rhythm between sections
- Spacing between components
- Layout margins

**Grid System:**
- Identify column structure if visible
- Gutter widths
- Container max-widths
- Responsive breakpoint hints

Provide spacing tokens like:
```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;
```

### 4. Component Analysis

Components are the building blocks of the UI. Systematically identify, analyze, and document each recurring UI pattern with comprehensive detail.

#### Component Identification Strategy

1. **Scan the entire UI** for repeating visual patterns
2. **Group similar elements** (all buttons together, all inputs together, etc.)
3. **Identify variants** within each component type
4. **Document states** for interactive elements
5. **Note composition patterns** (how components combine)

#### Core Components to Analyze

**Buttons:**

For each button variant found:
- **Visual characteristics:**
  - Background color (fill or transparent)
  - Text color and font weight
  - Border (width, color, style)
  - Border radius
  - Padding (horizontal and vertical)
  - Icon presence and positioning
  - Shadow effects
  - Height/min-height

- **Variants to identify:**
  - Primary (main CTA)
  - Secondary (less emphasis)
  - Tertiary (minimal styling)
  - Ghost/Text (no background)
  - Destructive (delete/remove actions)
  - Link-style buttons

- **Sizes:**
  - Small (compact interfaces, inline actions)
  - Medium (default)
  - Large (hero sections, prominent CTAs)
  - Full-width variants

- **States:** Document visual changes for:
  - Default/Rest
  - Hover (background, shadow, transform)
  - Active/Pressed
  - Focus (outline, ring, shadow)
  - Disabled (opacity, cursor, colors)
  - Loading (spinner, text changes)

- **Icon combinations:**
  - Icon-only buttons
  - Icon + text (left/right positioning)
  - Icon size relative to text

- **CSS Implementation:** Provide complete styles including transitions

**Input Fields:**

Analyze all form controls:

- **Text Inputs:**
  - Border style, color, and width
  - Border radius
  - Padding
  - Font size and color
  - Placeholder styling
  - Background color
  - Height/min-height
  - Focus ring/outline style
  - Error state styling (red border, icon, message)
  - Success state (if present)
  - Disabled state appearance

- **Textareas:**
  - Resizing behavior
  - Min/max height
  - Differences from text inputs

- **Select Dropdowns:**
  - Dropdown indicator icon
  - Menu appearance
  - Selected item styling
  - Option hover states
  - Search functionality (if present)

- **Checkboxes:**
  - Size and shape
  - Border and fill colors
  - Checkmark style
  - Checked state appearance
  - Indeterminate state (if present)
  - Label positioning and spacing

- **Radio Buttons:**
  - Circle size
  - Border and fill colors
  - Selected state (inner dot)
  - Label positioning

- **Toggles/Switches:**
  - Track width and height
  - Handle/knob size and style
  - On/off colors
  - Animation/transition

- **Label patterns:**
  - Position (top, left, inline)
  - Font size and weight
  - Required field indicators (asterisk, "Required" text)
  - Helper text styling

**Cards:**

- **Structure:**
  - Overall shape and dimensions
  - Border or shadow for definition
  - Background color
  - Border radius
  - Internal padding
  - Content sections (header, body, footer)

- **Variants:**
  - Basic card
  - Card with image/media
  - Card with header
  - Card with actions/buttons
  - Interactive cards (clickable, hoverable)
  - List/feed cards

- **Elevation:**
  - Default shadow
  - Hover shadow (if interactive)
  - Border treatment vs shadow

- **Internal spacing:**
  - Content padding
  - Spacing between sections
  - Spacing around images

**Navigation Components:**

- **Navigation Bar/Header:**
  - Height and padding
  - Background color and transparency
  - Border or shadow
  - Logo size and positioning
  - Navigation item spacing
  - Mobile hamburger menu (if visible)

- **Navigation Items:**
  - Default text color and weight
  - Hover state
  - Active/current page indicator
  - Underline, background, or other active indicators
  - Dropdown indicators (if present)

- **Breadcrumbs:**
  - Separator style (/, >, icon)
  - Text size and color
  - Current item styling
  - Link vs non-link items

- **Tabs:**
  - Tab button styling
  - Active tab indicator (underline, background, border)
  - Spacing between tabs
  - Tab bar border/separator

- **Sidebar Navigation:**
  - Width
  - Background color
  - Item padding and spacing
  - Active item styling
  - Nested/collapsible sections
  - Icons + text patterns

**Modals/Dialogs:**

- **Overlay/backdrop:**
  - Background color and opacity
  - Blur effect (if any)

- **Modal container:**
  - Width (fixed or responsive)
  - Background color
  - Border radius
  - Shadow
  - Padding
  - Positioning (centered, top-offset)

- **Header:**
  - Title styling
  - Close button (X icon, position, size)
  - Border separator

- **Body:**
  - Content spacing
  - Scrolling behavior

- **Footer:**
  - Button alignment (right, center, space-between)
  - Button spacing
  - Border separator

**Alerts/Notifications:**

- **Types:**
  - Success (color, icon)
  - Warning (color, icon)
  - Error (color, icon)
  - Info (color, icon)

- **Structure:**
  - Background color (solid or tinted)
  - Border (left accent, full border)
  - Border radius
  - Padding
  - Icon size and positioning
  - Close/dismiss button
  - Shadow or elevation

- **Variants:**
  - Inline alerts (within forms)
  - Toast/snackbar notifications
  - Banner notifications

**Badges/Tags:**

- **Appearance:**
  - Size (height, padding)
  - Border radius (rounded corners or pills)
  - Background color variants
  - Text size and weight
  - Text transform (uppercase, etc.)

- **Variants:**
  - Status badges (success, warning, error, info)
  - Count badges (notification counters)
  - Removable tags (with X icon)
  - Outlined vs filled

**Loading States:**

- **Spinners:**
  - Size variants
  - Color
  - Animation speed and style

- **Skeleton screens:**
  - Shape and sizing
  - Animation (pulse, shimmer)
  - Color

- **Progress bars:**
  - Height
  - Background and fill colors
  - Border radius
  - Indeterminate vs determinate

**Tooltips:**

- Background color
- Text color and size
- Padding
- Border radius
- Arrow/pointer style
- Shadow
- Max-width
- Positioning relative to trigger

**Dropdowns/Menus:**

- Container background and border
- Border radius
- Shadow
- Item padding
- Item hover state
- Divider style
- Icon spacing
- Max-height and scrolling

**Other Components to Consider:**

- Avatars (size variants, placeholder states)
- Dividers/separators
- Empty states
- Error pages
- Icons (size scale, style consistency)
- Images (border radius, aspect ratios)
- Lists (bullet/numbered styling, spacing)
- Pagination
- Search bars
- Tables (header styling, row hover, borders)
- Accordions/collapsible sections
- Steppers/progress indicators
- Date pickers
- File upload components

#### Component Documentation Template

For each component identified, provide:

1. **Component Name & Description**
   - Brief explanation of purpose and usage

2. **Visual Characteristics**
   - Detailed measurements and styling
   - Color values with tokens

3. **Variants**
   - List all variations discovered
   - Visual differences between variants

4. **States** (for interactive components)
   - Default, hover, active, focus, disabled, loading, error, success

5. **Sizing Options**
   - Small, medium, large (if applicable)
   - Responsive behavior

6. **Composition Patterns**
   - How the component combines with others
   - Common usage patterns

7. **CSS Implementation**
   - Complete, copy-paste ready code
   - Using design tokens
   - Including all states and variants

8. **Accessibility Notes**
   - ARIA attributes needed
   - Keyboard navigation patterns
   - Focus management
   - Color contrast issues (if any)

9. **Usage Guidelines**
   - When to use this component
   - When NOT to use it
   - Common patterns and anti-patterns

## Output Format

Present the analysis as a comprehensive, interactive design system documentation using the following structure:

### Structure

The output should follow this comprehensive structure, with heavy emphasis on the Components section:

```markdown
# Design System Documentation

## 🎨 Design Tokens

### Colors
[Present complete color palette with visual swatches and tokens]

### Typography
[Present type scale with examples and CSS classes]

### Spacing
[Present spacing scale with usage examples]

### Shadows & Effects
[Document shadows, border radius, and other visual treatments]

---

## 📐 Components Library

This is the MOST IMPORTANT section. Document every component identified with comprehensive detail.

### Buttons

#### Overview
[Brief description of button usage in this design]

#### Variants
- **Primary Button**: [Description, usage, visual characteristics]
- **Secondary Button**: [Description, usage, visual characteristics]
- **Tertiary Button**: [Description, usage, visual characteristics]
- **Ghost/Text Button**: [Description, usage, visual characteristics]
- **Destructive Button**: [Description for dangerous actions]

#### Sizing
- Small: [Dimensions, padding, font size]
- Medium (Default): [Dimensions, padding, font size]
- Large: [Dimensions, padding, font size]

#### States
- Default
- Hover
- Active/Pressed
- Focus
- Disabled
- Loading

#### CSS Implementation
[Complete button styles with all variants, sizes, and states]

#### Usage Guidelines
[When to use each variant, best practices]

---

### Form Components

#### Text Input
[Complete documentation following component template]

#### Textarea
[Complete documentation]

#### Select/Dropdown
[Complete documentation]

#### Checkbox
[Complete documentation]

#### Radio Button
[Complete documentation]

#### Toggle/Switch
[Complete documentation if present]

---

### Cards

#### Overview
[Card usage and purpose]

#### Variants
- Basic Card
- Card with Header
- Card with Image
- Interactive Card
- [Other variants found]

#### Structure
- Header styling
- Body styling
- Footer styling
- Image/media treatment

#### CSS Implementation
[Complete card styles]

---

### Navigation

#### Navigation Bar
[Complete documentation]

#### Navigation Items
[Item styling, states, active indicators]

#### Breadcrumbs
[If present]

#### Tabs
[If present]

#### Sidebar Navigation
[If present]

---

### Modals & Overlays

#### Modal/Dialog
[Complete documentation including backdrop, structure, sizing]

#### Tooltip
[If present]

#### Dropdown Menu
[If present]

#### Popover
[If present]

---

### Feedback Components

#### Alerts
- Success Alert
- Warning Alert
- Error Alert
- Info Alert

[Complete documentation for each]

#### Toast/Snackbar Notifications
[If present]

#### Loading States
- Spinners
- Skeleton screens
- Progress bars

---

### Data Display

#### Tables
[If present - header, rows, borders, hover states]

#### Lists
[Styling for ordered/unordered lists]

#### Empty States
[If present]

---

### Other Components

[Document any additional components found:]
- Avatars
- Badges/Tags
- Dividers
- Pagination
- Search Bars
- Accordions
- Steppers
- Date Pickers
- [Etc.]

---

## 💻 Complete CSS Implementation

### Design Tokens (CSS Variables)
```css
:root {
  /* Colors */
  --color-primary-500: #...;
  --color-secondary-500: #...;

  /* Typography */
  --font-family-sans: ...;
  --font-size-base: ...;

  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;

  /* Shadows */
  --shadow-sm: ...;
  --shadow-md: ...;

  /* Border Radius */
  --radius-sm: ...;
  --radius-md: ...;
}
```

### Component Styles

[Provide all component CSS in one place for easy copy-paste]

---

## 📱 Implementation Guidelines

### Getting Started
[How to use this design system]

### Best Practices
[General guidance]

### Accessibility Notes
[Important accessibility considerations across components]

### Responsive Considerations
[Any responsive patterns observed]
```

### Presentation Style

- Use clear headings and sections with emoji for visual hierarchy
- Include color swatches (use colored emoji or describe visually)
- Provide both design tokens and CSS snippets
- Make it actionable and implementation-ready
- Include usage examples where helpful
- Note any accessibility considerations (color contrast, focus states, etc.)

## Best Practices

**Be Thorough:**
- Examine every visible element in the image
- Look for subtle variations (hover states, shadows, borders)
- Identify patterns and inconsistencies

**Be Specific:**
- Provide exact or well-estimated measurements
- Use specific color values, not vague descriptions
- Document context for each element

**Be Actionable:**
- Generate implementation-ready CSS
- Suggest semantic naming conventions
- Provide design tokens that can be used immediately

**Consider Accessibility:**
- Check color contrast ratios where possible
- Note focus states and keyboard navigation cues
- Suggest ARIA labels or semantic HTML where relevant

**Organize Logically:**
- Start with foundations (colors, typography, spacing)
- Progress to components
- Conclude with implementation code

## Additional Notes

- If the image quality makes it difficult to determine exact values, provide best estimates and note uncertainty
- If multiple screens or states are visible, document variations
- Consider responsive design patterns if multiple viewport sizes are shown
- Look for design inconsistencies that should be standardized
