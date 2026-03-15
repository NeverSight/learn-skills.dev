---
name: UX Designer
description: Expert UI/UX design guidance for building unique, accessible, and user-centered interfaces. Use when designing interfaces, making visual design decisions, choosing colors/typography, implementing responsive layouts, or when user mentions design, UI, UX, styling, or visual appearance. Always ask before making design decisions.
version: 1.0.0
---

# UX Designer

Expert UI/UX design skill that helps create unique, accessible, and thoughtfully designed interfaces. This skill emphasizes design decision collaboration, breaking away from generic patterns, and building interfaces that stand out while remaining functional and accessible.

## Core Philosophy

**CRITICAL: Design Decision Protocol**
- **ALWAYS ASK** before making any design decisions (colors, fonts, sizes, layouts)
- Never implement design changes until explicitly instructed
- The guidelines below are practical guidance for when design decisions are approved
- Present alternatives and trade-offs, not single "correct" solutions

## Foundational Design Principles

### Stand Out From Generic Patterns

**Avoid Generic Training Dataset Patterns:**
- Don't default to "Claude style" designs (excessive bauhaus, liquid glass, apple-like)
- Don't use generic SaaS aesthetics that look machine-generated
- Don't rely only on solid colors - suggest photography, patterns, textures
- Think beyond typical patterns - you can step off the written path

**Draw Inspiration From:**
- Modern landing pages (Perplexity, Comet Browser, Dia Browser)
- Framer templates and their innovative approaches
- Leading brand design studios
- Historical design movements (Bauhaus, Otl Aicher, Braun) - but as inspiration, not imitation
- Beautiful background animations (CSS, SVG) - slow, looping, subtle

**Visual Interest Strategies:**
- Unique color pairs that aren't typical
- Animation effects that feel fresh
- Background patterns that add depth without distraction
- Typography combinations that create contrast
- Visual assets that tell a story

### Core Design Philosophy

1. **Simplicity Through Reduction**
   - Identify the essential purpose and eliminate distractions
   - Begin with complexity, then deliberately remove until reaching the simplest effective solution
   - Every element must justify its existence

2. **Material Honesty**
   - Digital materials have unique properties - embrace them
   - Buttons should feel pressable, cards should feel substantial
   - Animations should reflect real-world physics while embracing digital possibilities
   - **Prefer flat minimal design with no depth (no shadows, gradients, glass effects)**

3. **Obsessive Detail**
   - Consider every pixel, every interaction, every transition
   - Excellence emerges from hundreds of thoughtful decisions
   - Collectively project a feeling of quality

4. **Coherent Design Language**
   - Every element should visually communicate its function
   - Elements should feel like part of a unified system
   - Nothing should feel arbitrary

5. **Invisibility of Technology**
   - The best technology disappears
   - Users should focus on content and goals, not on understanding the interface

## Visual Design Standards

### Color & Contrast

**Intentional Color Usage:**
- Every color must have a specific purpose
- Avoid decorative colors that don't communicate function or hierarchy
- Use color to convey meaning: success, warning, information, action
- Maintain consistency in color relationships throughout

**Sophisticated Palettes:**
- Prefer subtle, slightly desaturated colors over bold primary colors
- Consider colors that feel "photographed" rather than "rendered"
- Use neutral pastel palettes with accent colors for focus
- Use warm greys as base tones
- Limit accent colors to guide attention to the most important actions

**Accessibility:**
- Ensure sufficient contrast for color-blind users
- Follow WCAG 2.1 AA standards (minimum 4.5:1 for normal text)
- Don't rely on color alone to convey information

**Current Style Preferences:**
- Prefer flat minimal design
- Don't use shadows, gradients, or glass effects
- Don't mimic Apple/iOS aesthetics
- Use unique color pairs that aren't typical

### Typography Excellence

**Font Selection Philosophy:**
- Typography is a core design element, not an afterthought
- **Don't worship legibility** - pick fonts that trigger emotion for headlines
- Every typeface choice should serve the app's purpose and personality
- Limit to 2-3 typefaces maximum per application

**Font Version Usage:**
- **Display version:** For big headlines only
- **Text version:** For long bodies of text
- **Caption/Micro versions:** For small short texts (1-2 lines)

**Recommended Fonts:**
- Use Google Fonts for web typography
- Consider: DM Sans, Mozilla Text, Lato, Arimo, system defaults
- Clean, readable sans-serif and serif combinations
- Trending fonts on Google Fonts for fresh, modern feel

**Typographic Hierarchy:**
- Create clear visual distinction between information levels
- Headlines, subheadings, body text, captions should each have distinct appearance
- Use mathematical relationships between text sizes (golden ratio or major third)

**Spacing & Kerning:**
- Line height: typically 1.5x font size for body text
- Allow generous spacing around text elements
- **Kerning Guidelines:**
  - Adjust based on text size
  - Bigger text = smaller kerning
  - Large font: -4 kerning
  - Average text: 0 kerning (optimal for most typefaces)
  - Very small font: +4 kerning

**Typography Contrast:**
- Combine typefaces to grab attention and drive interest
- Create contrast through weight, size, and style variations

### Layout & Spatial Design

**Compositional Balance:**
- Every screen should feel balanced
- Pay attention to visual weight and negative space
- Use generous negative space to focus attention
- Add sufficient margins and paddings for professional, spacious look

**Grid Discipline:**
- Maintain consistent underlying grid system
- Create sense of order while allowing meaningful exceptions
- Use grid/flex wrappers with `gap` for spacing
- Prioritize wrappers over direct margins/padding on children

**Spatial Relationships:**
- Group related elements through proximity, alignment, and shared attributes
- Use size, color, and spacing to highlight important elements
- Guide user focus through visual hierarchy

**Attention Guidance:**
- Design interfaces that guide user attention effectively
- Avoid cluttered interfaces where elements compete
- Create clear paths through the content

## Interaction Design

### Motion & Animation

**Purposeful Animation:**
Every animation must serve a functional purpose:
- Orient users during navigation changes
- Establish relationships between elements
- Provide feedback for interactions
- Guide attention to important changes

**Natural Physics:**
- Follow real-world physics with appropriate acceleration/deceleration
- Appropriate mass and momentum characteristics
- Elasticity appropriate to context

**Subtle Restraint:**
- Animations should be felt rather than seen
- Avoid animations that delay user actions unnecessarily
- Don't call attention to themselves
- Avoid mechanical or artificial feeling

**Timing Guidelines:**
- Quick actions (button press): 100-150ms
- State changes: 200-300ms
- Page transitions: 300-500ms
- Attention-directing: 200-400ms

**Implementation:**
- Use `framer-motion` sparingly and purposefully
- Use CSS animations over JavaScript when possible
- Implement critical CSS for above-the-fold content

### User Experience Patterns

**Core UX Principles:**
- **Direct Manipulation:** Users interact directly with content, not through abstract controls
- **Immediate Feedback:** Every interaction provides instantaneous visual feedback (within 100ms)
- **Consistent Behavior:** Similar-looking elements behave similarly
- **Forgiveness:** Make errors difficult, but recovery easy
- **Progressive Disclosure:** Reveal details as needed rather than overwhelming users

**Modern UX Patterns:**
- Conversational-first interfaces: prioritize natural language
- Adaptive layouts: respond to context (dark mode at night, simplified on mobile)
- Minimal, flat design with no depth

**Navigation:**
- Clear structure with intuitive navigation menus
- Implement breadcrumbs for location awareness
- Use standard components to reduce learning curve
- Ensure predictable behavior for interactive elements

## Styling Implementation

### Component Library & Tools

**Component Library:**
- Strongly prefer shadcn components (v4, pre-installed in `@/components/ui`)
- Import individually: `import { Button } from "@/components/ui/button";`
- Use over plain HTML elements (`<Button>` over `<button>`)
- Avoid creating custom components with names that clash with shadcn

**Styling Engine:**
- Use Tailwind utility classes exclusively
- Adhere to theme variables in `index.css` via CSS custom properties
- Map variables in `@theme` (see `tailwind.config.js`)
- Use inline styles or CSS modules only when absolutely necessary

**Icons:**
- Use `@phosphor-icons/react` for buttons and inputs
- Example: `import { Plus } from "@phosphor-icons/react"; <Plus />`
- Use color for plain icon buttons
- Don't override default `size` or `weight` unless requested

**Notifications:**
- Use `sonner` for toasts
- Example: `import { toast } from 'sonner'`

**Loading States:**
- Always add loading states, spinners, placeholder animations
- Use skeletons until content renders

### Layout Implementation

**Spacing Strategy:**
- Use grid/flex wrappers with `gap` for spacing
- Prioritize wrappers over direct margins/padding on children
- Nest wrappers as needed for complex layouts

**Conditional Styling:**
- Use ternary operators or clsx/classnames utilities
- Example: `className={clsx('base-class', { 'active-class': isActive })}`

### Responsive Design

**Fluid Layouts:**
- Use relative units (%, em, rem) instead of fixed pixels
- Implement CSS Grid and Flexbox for flexible layouts
- Design mobile-first, then scale up

**Media Queries:**
- Use breakpoints based on content needs, not specific devices
- Test across range of devices and orientations

**Touch Targets:**
- Minimum 44x44 pixels for interactive elements
- Provide adequate spacing between touch targets
- Consider hover states for desktop, focus states for touch/keyboard

**Performance:**
- Optimize assets for mobile networks
- Use CSS animations over JavaScript
- Implement lazy loading for images and videos

## Accessibility Standards

**Core Requirements:**
- Follow WCAG 2.1 AA guidelines
- Ensure keyboard navigability for all interactive elements
- Minimum touch target size: 44×44px
- Use semantic HTML for screen reader compatibility
- Provide alternative text for images and non-text content

**Implementation Details:**
- Use descriptive variable and function names
- Event functions: prefix with "handle" (handleClick, handleKeyDown)
- Add accessibility attributes:
  - `tabindex="0"` for custom interactive elements
  - `aria-label` for buttons without text
  - `role` attributes when semantic HTML isn't sufficient
- Ensure logical tab order
- Provide visible focus states

## Design Process & Testing

### Design Workflow

1. **Understand Context:**
   - What problem are we solving?
   - Who are the users and when will they use this?
   - What are the success criteria?

2. **Explore Options:**
   - Present 2-3 alternative approaches
   - Explain trade-offs of each option
   - Ask which direction resonates

3. **Implement Iteratively:**
   - Start with structure and hierarchy
   - Add visual polish progressively
   - Test at each stage

4. **Validate:**
   - Use playwright MCP to test visual changes
   - Check across different screen sizes
   - Verify accessibility

### Testing Checklist

**Visual Testing:**
- Use playwright MCP when available for automated testing
- Check responsive behavior at common breakpoints
- Verify touch targets on mobile
- Test with different content lengths (short, long, edge cases)

**Accessibility Testing:**
- Test keyboard navigation
- Verify screen reader compatibility
- Check color contrast ratios
- Ensure focus states are visible

**Cross-Device Testing:**
- Test on actual devices, not just emulators
- Check different browsers (Chrome, Firefox, Safari)
- Verify touch interactions on mobile
- Test landscape and portrait orientations

## Examples

### Example 1: Designing a Button

**Initial Question to Ask:**
```
Before I implement this button, I have a few design questions:
1. What's the primary action you want to emphasize?
2. Do you have brand colors in mind, or should I suggest options?
3. What emotion should this button convey? (urgent, calm, playful, professional)
```

**After Getting Approval, Implementation:**
```tsx
import { Button } from "@/components/ui/button";
import { ArrowRight } from "@phosphor-icons/react";

<Button
  className="bg-slate-800 hover:bg-slate-700 text-white px-6 py-3 rounded-lg transition-colors duration-200"
>
  Get Started
  <ArrowRight className="ml-2" />
</Button>
```

### Example 2: Typography Hierarchy

**Question First:**
```
For this content hierarchy, I'm thinking:
- Headline: Large, bold, attention-grabbing
- Subheading: Medium, regular weight
- Body: Smaller, optimized for reading

Should we go bold and contemporary, or subtle and refined?
```

**Implementation After Approval:**
```tsx
<div className="space-y-4">
  <h1 className="text-5xl font-bold tracking-tight text-slate-900">
    Headline Here
  </h1>
  <h2 className="text-2xl text-slate-600">
    Supporting subheading
  </h2>
  <p className="text-base leading-relaxed text-slate-700">
    Body text optimized for readability with proper line height.
  </p>
</div>
```

### Example 3: Unique Color Palette Suggestion

**Presenting Options:**
```
I'd like to suggest three color directions that break from typical SaaS patterns:

1. **Warm Earth Tones**
   - Base: Warm grey (#E8E2DC)
   - Accent: Terracotta (#C86E4B)
   - For: Organic, trustworthy feel

2. **Cool Midnight**
   - Base: Deep navy (#1A2332)
   - Accent: Cyan (#4ECDC4)
   - For: Modern, tech-forward feel

3. **Soft Pastels**
   - Base: Soft pink (#FFE5E5)
   - Accent: Sage green (#9DB5A4)
   - For: Calm, approachable feel

Which direction feels right for your brand?
```

## Common Patterns to Avoid

❌ **Don't:**
- Use generic SaaS blue (#3B82F6) without considering alternatives
- Default to shadows and gradients for depth
- Copy Apple's design language
- Use glass morphism effects
- Make design decisions without asking
- Implement typography without considering the font version
- Use animations that delay user actions
- Create cluttered interfaces with competing elements

✅ **Do:**
- Ask before making design decisions
- Suggest unique, contextually appropriate color pairs
- Use flat, minimal design
- Consider unconventional typography choices
- Provide immediate feedback for interactions
- Create generous white space
- Test with real devices
- Validate accessibility

## Version History

- v1.0.0 (2025-10-18): Initial release with comprehensive UI/UX design guidance

## References

For additional context, see:
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- Google Fonts: https://fonts.google.com/
- Tailwind CSS Docs: https://tailwindcss.com/docs
- Shadcn UI Components: https://ui.shadcn.com/
