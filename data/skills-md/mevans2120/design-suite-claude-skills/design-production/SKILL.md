---
name: design-production
description: Creates production-ready design files, prototypes, and specifications for development teams. Translates validated concepts into detailed, implementable designs with comprehensive specs for developers. Produces Figma files (via API), high-fidelity prototypes, design specifications, and animation files.
triggers:
  keywords:
    - "design specs"
    - "design specification"
    - "developer handoff"
    - "handoff"
    - "design tokens"
    - "component states"
    - "production design"
    - "design system"
    - "pixel perfect"
    - "responsive specs"
    - "all states"
    - "hover states"
    - "error states"
    - "loading states"
    - "Figma file"
    - "high fidelity"
    - "implementation guide"
    - "spacing specification"
    - "ready for development"
    - "ready for dev"
  contexts:
    - "Concept direction has been approved"
    - "Ready to hand off to engineering team"
    - "Need detailed specifications for implementation"
    - "Creating or documenting design system"
    - "Preparing assets and tokens for developers"
    - "Need to specify all component states and interactions"
    - "Converting approved design to implementable specs"
  prerequisites:
    - "Approved concept or design direction exists"
    - "Know the target platforms and technical constraints"
    - "Ready to provide pixel-level detail"
  anti_triggers:
    - "Still exploring design directions (use design-concepts)"
    - "Need to understand users first (use design-research)"
    - "Reviewing already-built product (use design-qa)"
    - "Concept not yet approved by stakeholders"
    - "Early ideation or brainstorming phase"
---

# Design - Production

This skill guides Claude through creating production-ready design artifacts that development teams can confidently implement. Production design is about precision, completeness, and developer handoff quality.

## Core Methodology

### Purpose of Production Design
Production design provides everything developers need to build accurately:
- **Complete specifications**: Every state, spacing, interaction documented
- **Design system consistency**: Reusable components, tokens, patterns
- **Developer-friendly formats**: Specs that answer common dev questions
- **Reduced ambiguity**: Minimize back-and-forth during implementation

### Production Design Process
1. **Handoff Review**: Understand approved concept, technical constraints
2. **System Setup**: Establish or use design system (components, tokens)
3. **Detailed Design**: Create high-fidelity screens with all states
4. **Specification**: Document spacing, behavior, interactions, edge cases
5. **Asset Preparation**: Export icons, images, animations at correct sizes
6. **Developer Handoff**: Package everything with clear documentation

### Fidelity Requirements
Production designs must be:
- **Pixel-accurate**: Precise spacing, sizing, alignment
- **State-complete**: Loading, error, empty, success states
- **Interaction-specified**: Animations, transitions, micro-interactions
- **Responsive-defined**: Behavior at all breakpoints
- **Accessible**: WCAG guidelines met (AA minimum)

## Tool Usage Patterns

### Initial Setup & Handoff Review

**Step 1: Gather Requirements**
```
Questions to ask user:
1. What concept/direction was approved?
2. Does a design system exist? (Components, tokens)
3. What platforms? (iOS, Android, Web, Desktop)
4. What breakpoints/screen sizes?
5. Any technical constraints? (Framework, performance)
6. Timeline and which screens/flows to prioritize?
7. Do you have Figma API access for creating Figma files?

Use `view` to read:
- Approved concept files
- Design system documentation
- Brand guidelines
- Technical requirements from engineering
```

**Step 2: Determine Output Format**
Based on user needs:
- **Figma files**: Use Figma API to create/update files (if API access provided)
- **HTML/CSS**: Static mockups with precise styling
- **React prototypes**: Interactive prototypes with real components
- **Design specs**: Markdown documentation for developers
- **Animation files**: Lottie JSON for complex animations

### Creating Design System (If None Exists)

**Define Design Tokens First**:
```javascript
// Create design-tokens.js
export const tokens = {
  colors: {
    primary: { 
      50: '#E3F2FD',
      500: '#2196F3',
      900: '#0D47A1'
    },
    neutral: {
      50: '#FAFAFA',
      500: '#9E9E9E',
      900: '#212121'
    },
    semantic: {
      success: '#4CAF50',
      error: '#F44336',
      warning: '#FF9800',
      info: '#2196F3'
    }
  },
  typography: {
    fontFamily: {
      sans: 'Inter, system-ui, sans-serif',
      mono: 'Monaco, monospace'
    },
    fontSize: {
      xs: '0.75rem',    // 12px
      sm: '0.875rem',   // 14px
      base: '1rem',     // 16px
      lg: '1.125rem',   // 18px
      xl: '1.25rem',    // 20px
      '2xl': '1.5rem',  // 24px
      '3xl': '1.875rem' // 30px
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700
    },
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75
    }
  },
  spacing: {
    0: '0',
    1: '0.25rem',  // 4px
    2: '0.5rem',   // 8px
    3: '0.75rem',  // 12px
    4: '1rem',     // 16px
    6: '1.5rem',   // 24px
    8: '2rem',     // 32px
    12: '3rem',    // 48px
    16: '4rem'     // 64px
  },
  borderRadius: {
    none: '0',
    sm: '0.125rem',    // 2px
    base: '0.25rem',   // 4px
    md: '0.375rem',    // 6px
    lg: '0.5rem',      // 8px
    xl: '0.75rem',     // 12px
    full: '9999px'
  },
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    base: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)'
  }
};
```

**Create Reusable Components**:
```jsx
// Button.jsx - Example component
import React from 'react';

export const Button = ({ 
  variant = 'primary',
  size = 'md', 
  children, 
  disabled = false,
  onClick 
}) => {
  const baseStyles = 'font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500 disabled:bg-blue-300',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500 disabled:bg-gray-100',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500 disabled:bg-red-300'
  };
  
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };
  
  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

### Working with Figma API

**Note**: Figma API integration requires user's Figma API token and file permissions.

**Creating Figma Files Programmatically**:
```bash
# First, install Figma API client if needed
# Then use Python or Node.js to interact with Figma API

# Example workflow:
# 1. Create new Figma file
# 2. Set up pages (e.g., "Components", "Screens", "Specs")
# 3. Create frames for each screen
# 4. Add components, text, shapes using API
# 5. Set up auto-layout, constraints
# 6. Add annotations and developer notes
```

**Reading Existing Figma Files**:
```bash
# Use Figma API to:
# 1. Fetch file structure
# 2. Extract component definitions
# 3. Read design tokens (colors, typography)
# 4. Export assets
# 5. Generate specs from Figma data
```

### Creating High-Fidelity Prototypes

**React Component Structure**:
```jsx
// Organize components logically
/components
  /ui          // Base components (Button, Input, Card)
  /features    // Feature-specific components
  /layouts     // Page layouts
  /icons       // Icon components

// Use design tokens consistently
import { tokens } from './design-tokens';

// Include all interactive states
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState(null);
const [data, setData] = useState(null);
```

### Creating Design Specifications

**Specification Document Format**:
```markdown
# [Screen/Component Name] Design Specification

## Overview
[Brief description of purpose and user flow]

## Layout & Structure

### Desktop (1440px+)
- Container max-width: 1280px
- Horizontal padding: 64px
- Vertical spacing between sections: 48px

### Tablet (768px - 1439px)
- Container max-width: 100%
- Horizontal padding: 32px
- Vertical spacing between sections: 32px

### Mobile (< 768px)
- Container max-width: 100%
- Horizontal padding: 16px
- Vertical spacing between sections: 24px

## Components

### Primary CTA Button
**States**:
- Default: bg-blue-600, text-white, px-6 py-3, rounded-lg
- Hover: bg-blue-700, cursor-pointer
- Active: bg-blue-800
- Disabled: bg-blue-300, cursor-not-allowed
- Loading: Show spinner, text "Processing..."

**Interaction**:
- Transition: all 200ms ease
- Focus: 2px blue ring, 2px offset
- Min-width: 120px
- Height: 48px

### Form Input
**States**:
- Default: border-gray-300, bg-white
- Focus: border-blue-500, ring-2 ring-blue-100
- Error: border-red-500, ring-2 ring-red-100
- Disabled: bg-gray-100, cursor-not-allowed

**Validation**:
- Show error message below input
- Error color: text-red-600
- Error icon: Inline, left of message

## Interactions & Animations

### Modal Open Animation
- Duration: 200ms
- Easing: ease-out
- Transform: scale(0.95) → scale(1)
- Opacity: 0 → 1
- Backdrop: blur(4px), bg-opacity-50

### Loading State
- Show skeleton screens during data load
- Skeleton: bg-gray-200, animated pulse
- Min display time: 300ms (prevent flash)

## Edge Cases

### Empty States
[Screenshot or description]
- Centered icon and message
- CTA to take first action
- Copy: "No items yet. Get started by..."

### Error States
[Screenshot or description]
- Error icon with message
- Retry button or next steps
- Copy: "Something went wrong. [Action]"

### Loading States
[Screenshot or description]
- Skeleton screens or spinners
- Preserve layout to prevent jank

### Long Content
- Text truncation after 2 lines
- Tooltip on hover shows full text
- "Show more" expansion if needed

## Accessibility

### Keyboard Navigation
- Tab order: logical, left-to-right, top-to-bottom
- Focus indicators: visible 2px ring
- Escape key: Closes modals/dropdowns
- Enter/Space: Activates buttons/checkboxes

### Screen Reader Support
- All images have alt text
- Forms have associated labels
- Error messages announced
- Loading states announced

### Color Contrast
- Text on background: 4.5:1 minimum
- Large text (18px+): 3:1 minimum
- Interactive elements: 3:1 minimum

## Assets Required

### Icons
- icon-close.svg (24x24)
- icon-check.svg (20x20)
- icon-error.svg (20x20)

### Images
- hero-image@2x.jpg (2880x1620)
- placeholder-avatar.png (128x128)

### Animations
- loading-spinner.json (Lottie)

## Developer Notes

### Implementation Considerations
- Use CSS Grid for main layout
- Lazy load images below fold
- Prefetch critical assets
- Use proper semantic HTML (section, nav, etc.)

### Performance Targets
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s
- Lighthouse Score: 90+

### Browser Support
- Chrome/Edge: Last 2 versions
- Firefox: Last 2 versions
- Safari: Last 2 versions
- Mobile Safari: iOS 14+
```

## Quality Criteria

### Excellent Production Designs:
- **Complete state coverage**: Default, hover, active, focus, disabled, loading, error, empty
- **Precise specifications**: All spacing, sizing, colors documented with exact values
- **Consistent with system**: Uses design tokens, follows established patterns
- **Responsive**: Behavior defined for all breakpoints
- **Accessible**: Meets WCAG AA standards minimum
- **Developer-ready**: Can be implemented without guessing or assumptions
- **Asset-complete**: All images, icons, fonts provided at correct sizes

### Excellent Design Specs:
- **Scannable**: Clear headers, visual hierarchy
- **Precise values**: "16px" not "small gap"
- **Context-aware**: Explains WHY when non-obvious
- **Edge cases covered**: Empty, error, loading states documented
- **Interaction details**: Animations, transitions, micro-interactions specified
- **Accessibility notes**: Keyboard nav, screen reader, color contrast

### Excellent Figma Files:
- **Organized pages**: Components, Screens, Specs logically separated
- **Named layers**: Every layer has descriptive name
- **Auto-layout**: Responsive components use auto-layout
- **Components library**: Reusable components properly structured
- **Developer handoff ready**: Figma Inspect shows correct values
- **Annotated**: Dev notes explain complex interactions

## Deliverable Formats

### File Organization

**IMPORTANT: Organize all deliverables by feature/assignment in dated folders.**

Each production design project should be saved in its own folder with the feature name:
`docs/design/{feature-name}-production-{MMDDYY}/`

**Feature Name Guidelines:**
- Use kebab-case (lowercase with hyphens)
- Examples: `checkout-flow`, `user-profile`, `dashboard-redesign`, `search-filters`
- Ask the user for the feature name if not provided
- Suggest a name based on their description if needed

**Examples:**
- Checkout flow production specs on Oct 24, 2025: `docs/design/checkout-flow-production-102425/`
- Checkout flow updates on Nov 5, 2025: `docs/design/checkout-flow-production-110525/`
- User profile specs on Nov 10, 2025: `docs/design/user-profile-production-111025/`

**Rationale:**
- **Immediate clarity**: Know what feature each file relates to
- **Version history**: Same feature can have multiple dated iterations
- **No conflicts**: Different features can have same-named files
- **Clear handoff**: Which specs correspond to which feature/build
- **Organized**: All production files for one feature stay together

**Folder structure:**
```
docs/design/{feature-name}-production-{MMDDYY}/
├── {feature-name}-design-specification.md
├── {feature-name}-component-guide.md
├── {feature-name}-design-tokens.js
├── {feature-name}-design-system.md
├── {feature-name}-prototype.jsx
└── {feature-name}-animations/
    ├── {animation-name}.json
    └── {animation-name}.json
```

### Figma Files
**Created via**: Figma API (if access provided)
**Structure**:
- Page 1: Components library
- Page 2: Screens (grouped by flow)
- Page 3: Developer specs & annotations
**Naming**: `{feature-name}-component-name`, `{feature-name}-screen-name` (kebab-case)
**Note**: Link to Figma file in design specification document

### High-Fidelity Prototypes
**Location**: `docs/design/{feature-name}-production-{MMDDYY}/`
**File**: `{feature-name}-prototype.jsx` or `.html`
**Format**: React with full design system (or HTML/CSS)
**Include**:
- All screens in primary flow
- All component states
- Realistic interactions
- Design tokens file
- Component library

### Design Specifications
**Location**: `docs/design/{feature-name}-production-{MMDDYY}/`
**File**: `{feature-name}-design-specification.md`
**Format**: Markdown with embedded images
**Include**:
- Layout specifications
- Component specifications
- Interaction details
- Edge case handling
- Accessibility requirements
- Asset list

### Animation Files
**Location**: `docs/design/{feature-name}-production-{MMDDYY}/{feature-name}-animations/`
**File**: `{animation-name}.json`
**Format**: Lottie JSON
**Use cases**: Loading indicators, success confirmations, illustrations
**Tools**: Export from After Effects or create programmatically

### Design System Documentation
**Location**: `docs/design/{feature-name}-production-{MMDDYY}/`
**File**: `{feature-name}-design-system.md`
**Format**: Markdown with code examples
**Include**:
- Design tokens
- Component documentation
- Usage guidelines
- Do's and don'ts
- Accessibility notes

## Examples

### Good vs. Poor Specifications

❌ **Poor Spec**: "Add some space around the button"
✅ **Good Spec**: "Padding: 12px vertical, 24px horizontal (py-3 px-6 in Tailwind)"

❌ **Poor Spec**: "Use the brand blue"
✅ **Good Spec**: "Background: #2196F3 (primary-500 from design tokens)"

❌ **Poor Spec**: "Make it fade in"
✅ **Good Spec**: "Opacity transition: 0 to 1 over 200ms with ease-out easing"

### Good Component Documentation Example

```markdown
## Button Component

### Variants
- **Primary**: Main CTAs, high emphasis actions
- **Secondary**: Supporting actions, medium emphasis
- **Tertiary**: Low emphasis, inline actions
- **Danger**: Destructive actions (delete, remove)

### Sizes
- **Small**: 32px height, 12px vertical padding
- **Medium**: 40px height, 16px vertical padding  
- **Large**: 48px height, 20px vertical padding

### States & Interactions
| State | Visual | Notes |
|-------|--------|-------|
| Default | Solid background | Base state |
| Hover | Darken 10% | Cursor: pointer |
| Active | Darken 15% | During click |
| Focus | 2px ring | Keyboard navigation |
| Disabled | 50% opacity | Cursor: not-allowed |
| Loading | Spinner + "Loading..." | Min 300ms display |

### Accessibility
- Minimum touch target: 44x44px (iOS), 48x48px (Android)
- Color contrast: 4.5:1 text, 3:1 background
- Keyboard: Tab to focus, Enter/Space to activate
- Screen reader: Action announced clearly

### Code Example
\`\`\`jsx
<Button variant="primary" size="md" onClick={handleClick}>
  Save Changes
</Button>
\`\`\`
```

## Common Pitfalls to Avoid

### ❌ Incomplete State Coverage
**Problem**: Only designing default state, forgetting hover/loading/error
**Instead**: Design all states for every interactive element

### ❌ Imprecise Specifications
**Problem**: "Small gap" or "a bit darker" - developers have to guess
**Instead**: Use exact values: "8px gap" or "#1E40AF"

### ❌ Inconsistent Spacing
**Problem**: Random spacing values (13px, 17px, 22px)
**Instead**: Use spacing scale (4px, 8px, 12px, 16px, 24px, 32px...)

### ❌ Missing Responsive Behavior
**Problem**: Only designing for desktop, assuming mobile "works"
**Instead**: Define behavior at each breakpoint

### ❌ Inaccessible Color Contrast
**Problem**: Light gray text on white background
**Instead**: Test contrast ratios, minimum 4.5:1 for body text

### ❌ No Edge Case Consideration
**Problem**: Designs break with long names, empty lists, slow networks
**Instead**: Design for edge cases explicitly

### ❌ Developer-Unfriendly Handoff
**Problem**: Unlabeled Figma layers, no specs, missing assets
**Instead**: Organize files, name everything, provide complete specs

### ❌ Ignoring Technical Constraints
**Problem**: Designs requiring impossible performance or unsupported features
**Instead**: Collaborate with engineering on feasibility

### ❌ Over-Engineering Animations
**Problem**: Complex animations that hurt performance or accessibility
**Instead**: Keep animations subtle, purposeful, and performant

## Integration Points

### Inputs from Other Teams
- **Design Concepts**: Approved visual direction to detail out
- **Design Research**: User needs informing interaction patterns
- **Engineering**: Technical constraints, component architecture, API contracts
- **Product/PM**: Feature requirements, priority, timeline
- **QA**: Testing requirements, edge cases to handle

### Outputs for Other Teams
- **Engineering**: Complete specs, assets, Figma files for implementation
- **Design QA**: Reference designs for validation during build
- **Product/PM**: Visual documentation for stakeholder communication
- **Marketing**: Production-ready assets for launch materials

### Related Skills
- Builds on validated direction from **design-concepts**
- Feeds specifications to **design-qa** for validation
- Coordinates with **PM** teams on delivery timeline
- May require **engineering** input on technical feasibility

## Tips for Best Results

1. **Review concept thoroughly** - Understand what was validated before detailing
2. **Start with design system** - Establish tokens and components first
3. **Design the hard parts first** - Complex interactions, edge cases
4. **Use real content** - Exposes layout issues placeholder text hides
5. **Design all states** - Default, hover, active, focus, disabled, loading, error, empty
6. **Be pixel-precise** - Use 4px/8px grid, align everything
7. **Test responsiveness** - Check all breakpoints, don't assume
8. **Document your thinking** - Explain non-obvious decisions for developers
9. **Organize files clearly** - Developers should find what they need easily
10. **Include accessibility specs** - Keyboard nav, screen readers, contrast

## Handoff Checklist

Before delivering production designs to engineering:

### Completeness
- [ ] All screens in flow designed
- [ ] All component states covered
- [ ] All breakpoints specified
- [ ] Edge cases designed (empty, error, loading)
- [ ] Micro-interactions specified

### Specifications
- [ ] Spacing uses 4px/8px grid
- [ ] Colors reference design tokens
- [ ] Typography uses type scale
- [ ] Exact values provided (not approximations)
- [ ] Animations have duration/easing specified

### Assets
- [ ] Icons exported at correct sizes
- [ ] Images provided at 2x resolution
- [ ] Fonts linked or provided
- [ ] Animation files exported (Lottie)
- [ ] All assets properly named

### Accessibility
- [ ] Color contrast ratios verified (4.5:1 text, 3:1 UI)
- [ ] Keyboard navigation specified
- [ ] Screen reader content defined
- [ ] Touch targets meet minimum size (44x44 / 48x48)
- [ ] Focus indicators visible

### Organization
- [ ] Figma layers named descriptively
- [ ] Components organized logically
- [ ] Specs document is scannable
- [ ] Files in `/mnt/user-data/outputs/`
- [ ] Clear naming convention used

### Developer Communication
- [ ] Technical constraints validated
- [ ] Complex interactions explained
- [ ] Implementation notes included
- [ ] Questions anticipated and answered
- [ ] Contact info provided for questions

## Validation Checklist

Before marking production design complete:
- [ ] Reviewed approved concept and research insights
- [ ] Established or used existing design system
- [ ] Created high-fidelity designs for all key screens
- [ ] Documented all component states and interactions
- [ ] Specified responsive behavior for all breakpoints
- [ ] Verified accessibility standards met (WCAG AA)
- [ ] Provided all required assets at correct sizes
- [ ] Organized Figma files (if applicable) with clear naming
- [ ] Created comprehensive design specification document
- [ ] Tested prototype interactions work smoothly
- [ ] Files delivered to `/mnt/user-data/outputs/`
- [ ] Developer handoff documentation complete
