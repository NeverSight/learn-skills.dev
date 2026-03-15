---
name: spec-from-screenshot
description: This skill should be used when the user asks to "analyze a screenshot", "generate implementation spec", "create SPEC.md from screenshot", "extract design specs", "spec from image", or provides website screenshots and wants detailed implementation guidance.
---

# Screenshot Analysis & Spec Generation

Analyze website screenshots and generate detailed implementation specifications. This skill guides creation of
comprehensive `SPEC.md` files that document design systems extracted from visual references.

## When to Use

- User provides website screenshots or design mockups
- Request for implementation specifications from visual references
- Need to extract design systems (colors, typography, spacing) from images
- Creating detailed component inventories from UI screenshots

## Workflow

### Step 1: Validate Prerequisites

Ensure screenshots are available in the conversation. If no images are present, request them before proceeding.

### Step 2: Perform Ultra-Detailed Analysis

Analyze all provided screenshots covering these aspects:

**1. Layout Architecture**

- Overall page structure (header, navigation, hero, main content, sidebars, footer)
- Grid system and column layouts
- Container widths and max-widths
- Section hierarchy and nesting

**2. Typography System**

- Font families (identify primary, secondary, monospace)
- Font sizes for each text level (h1-h6, body, small, etc.)
- Font weights used (light, regular, medium, semibold, bold)
- Line heights and letter spacing
- Text colors and contrast ratios

**3. Color Palette**

- Primary brand colors
- Secondary/accent colors
- Background colors (main, sections, cards)
- Text colors (headings, body, muted, links)
- Border colors
- State colors (success, error, warning, info)
- Color codes in hex/rgb (best approximation)

**4. Spacing System**

- Margins between major sections
- Padding within components
- Gap spacing in flex/grid layouts
- Consistent spacing scale (e.g., 4px, 8px, 16px, 24px, 32px)
- Vertical rhythm patterns

**5. Component Inventory**

- Buttons (styles, sizes, states)
- Input fields and forms
- Cards and containers
- Navigation elements
- Icons and their style
- Badges, tags, labels
- Modals, tooltips, dropdowns
- List items and data tables

**6. Visual Design Details**

- Border radius values
- Shadow styles (box-shadow parameters)
- Border styles and thicknesses
- Background patterns or gradients
- Opacity/transparency effects

**7. Images and Media**

- Image locations and dimensions
- Image aspect ratios
- Icon sets (SVG, font icons, or images)
- Logo placement and size
- Decorative vs content images
- Note which images need to be sourced/created

**8. Interactive Elements** (if discernible)

- Hover states visible
- Active/focus states
- Transition/animation hints
- Interactive feedback patterns

**9. Responsive Design** (if multiple viewports shown)

- Breakpoints observable
- Layout changes per breakpoint
- Component behavior changes
- Mobile-specific patterns

**10. Accessibility Considerations**

- Color contrast issues
- Heading hierarchy
- Interactive element sizes
- Text readability

### Step 3: Generate Comprehensive SPEC.md

Write the specification to `./SPEC.md` using this structure:

```markdown
# Website Implementation Specification

> Generated from screenshot analysis on [DATE]

## Overview
[2-3 sentence summary of the website's purpose and design style]

## Layout Architecture
### Page Structure
### Grid System

## Typography
### Font Families
### Text Styles

## Color System

## Spacing System

## Component Inventory
[Document each component with properties]

## Images and Assets

## Responsive Behavior

## Interactive Elements and States

## Implementation Considerations
### Design Complexity Assessment
### Observable Technical Requirements
### Accessibility Observations
### Cannot Determine from Screenshots

## Open Questions / Assumptions

## Next Steps
```

### Step 4: Present Summary

After writing SPEC.md, provide a concise summary:

```
## Screenshot Analysis Complete

### Overview
[1-2 sentence description]

### Key Findings
- **Layout**: [brief description]
- **Components**: [count] distinct components identified
- **Color Palette**: [count] colors in system
- **Typography**: [primary font family], [count] type levels
- **Spacing**: [spacing scale summary]
- **Assets**: [count] images/icons to source

### Output
Full specification: `SPEC.md`

### Recommendations
[1-2 key technical recommendations]
```

## Analysis Tips

- Start with high-level layout observations
- Progressively zoom into details
- Measure or estimate dimensions
- Identify patterns and systems
- Note uncertainties or assumptions
- Cross-reference across multiple screenshots if provided
- Higher resolution screenshots provide more accurate measurements

## Notes

- All measurements are approximations; verify during implementation
- Running this analysis multiple times will overwrite existing SPEC.md
- Multi-screenshot analysis is supported and recommended for comprehensive specs
- Be explicit about states and behaviors that cannot be determined from static images
