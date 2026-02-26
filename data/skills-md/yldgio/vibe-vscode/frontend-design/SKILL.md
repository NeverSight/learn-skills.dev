---
name: Frontend Design
description: Create production-grade, distinctive frontend interfaces with modern UX/UI patterns for web applications
---

# Frontend Design

This skill guides you in creating exceptional, memorable frontend user interfaces that stand out with professional design quality.

## When to Use This Skill

Use this skill when you need to:
- Design and build distinctive, professional user interfaces
- Create unique visual experiences that reflect brand identity
- Implement modern UX/UI patterns with accessibility in mind
- Build responsive, performant frontend applications
- Avoid generic, template-like "AI slop" designs

## Core Principles

### 1. Distinctive Design
- **Intentional choices**: Make deliberate design decisions that serve the user
- **Have a point of view**: Create interfaces with clear visual direction
- **Be memorable**: Design experiences that users remember
- **Show personality**: Reflect brand or product identity clearly

### 2. Production Quality
- **Pixel-perfect**: Attention to spacing, alignment, typography
- **Responsive**: Works beautifully on all screen sizes
- **Performant**: Fast load times, smooth animations
- **Accessible**: WCAG 2.1 AA compliant minimum

### 3. Modern Patterns
- **Current best practices**: Use contemporary design patterns
- **Progressive enhancement**: Core functionality works everywhere
- **Mobile-first**: Design for smallest screens first
- **Component-driven**: Reusable, maintainable code

## Design Process

### Step 1: Understand Context

Before writing code, analyze:
- **Purpose**: What problem does this solve?
- **Audience**: Who will use this?
- **Brand**: What's the personality/identity?
- **Constraints**: Technical, business, accessibility requirements

### Step 2: Choose an Aesthetic

Select a design direction that fits the context:

**Minimalist**: Clean, spacious, focused
- High contrast
- Generous whitespace
- Limited color palette
- System fonts or elegant serifs

**Maximalist**: Bold, rich, expressive
- Layered elements
- Rich colors and gradients
- Custom typography
- Visual hierarchy through size/weight

**Brutalist**: Raw, honest, functional
- Stark contrasts
- Monospace fonts
- Unpolished aesthetic
- Clear structure

**Neumorphic**: Soft, tactile, modern
- Soft shadows and highlights
- Subtle depth
- Limited colors
- Gentle animations

**Glassmorphic**: Transparent, layered, sleek
- Frosted glass effects
- Backdrop blur
- Light transparency
- Depth through layering

### Step 3: Implement with Quality

Focus on:
- **Typography**: Hierarchy, readability, rhythm
- **Color**: Purposeful palette, contrast, meaning
- **Spacing**: Consistent scale, breathing room
- **Motion**: Subtle, purposeful animations
- **Components**: Well-structured, reusable elements

## Code Examples

### Example 1: Modern Hero Section

```tsx
import React from 'react';

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
      {/* Animated background */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500 rounded-full filter blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-pink-500 rounded-full filter blur-3xl animate-pulse animation-delay-2000"></div>
      </div>
      
      {/* Content */}
      <div className="relative z-10 text-center px-4 max-w-5xl">
        <h1 className="text-6xl md:text-8xl font-bold text-white mb-6 tracking-tight">
          Build Something
          <span className="block bg-clip-text text-transparent bg-gradient-to-r from-pink-400 to-purple-400">
            Remarkable
          </span>
        </h1>
        
        <p className="text-xl md:text-2xl text-purple-200 mb-12 leading-relaxed max-w-3xl mx-auto">
          A design system that helps you create memorable, accessible, and performant user interfaces.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button className="group relative px-8 py-4 bg-white text-purple-900 rounded-full font-semibold text-lg hover:shadow-2xl transition-all duration-300 hover:scale-105">
            Get Started
            <span className="absolute inset-0 rounded-full bg-gradient-to-r from-pink-500 to-purple-500 opacity-0 group-hover:opacity-20 transition-opacity"></span>
          </button>
          
          <button className="px-8 py-4 border-2 border-white/30 text-white rounded-full font-semibold text-lg backdrop-blur-sm hover:bg-white/10 transition-all duration-300">
            Learn More
          </button>
        </div>
      </div>
    </section>
  );
}
```

### Example 2: Glassmorphic Card Component

```tsx
interface CardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
}

export function GlassCard({ title, description, icon }: CardProps) {
  return (
    <div className="group relative">
      {/* Glow effect on hover */}
      <div className="absolute -inset-1 bg-gradient-to-r from-pink-600 to-purple-600 rounded-2xl blur opacity-0 group-hover:opacity-75 transition duration-1000"></div>
      
      {/* Card */}
      <div className="relative bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-all duration-300">
        <div className="mb-4 text-purple-400 transform group-hover:scale-110 transition-transform duration-300">
          {icon}
        </div>
        
        <h3 className="text-2xl font-bold text-white mb-3">
          {title}
        </h3>
        
        <p className="text-purple-200 leading-relaxed">
          {description}
        </p>
      </div>
    </div>
  );
}
```

### Example 3: Minimalist Form

```tsx
export function MinimalistForm() {
  return (
    <form className="max-w-md mx-auto space-y-8 p-8">
      <div className="space-y-2">
        <label 
          htmlFor="email" 
          className="block text-sm font-medium text-gray-900 uppercase tracking-wide"
        >
          Email Address
        </label>
        <input
          type="email"
          id="email"
          className="w-full px-0 py-3 border-0 border-b-2 border-gray-200 focus:border-black focus:ring-0 text-lg transition-colors bg-transparent placeholder:text-gray-400"
          placeholder="you@example.com"
        />
      </div>
      
      <div className="space-y-2">
        <label 
          htmlFor="message" 
          className="block text-sm font-medium text-gray-900 uppercase tracking-wide"
        >
          Message
        </label>
        <textarea
          id="message"
          rows={4}
          className="w-full px-0 py-3 border-0 border-b-2 border-gray-200 focus:border-black focus:ring-0 text-lg transition-colors bg-transparent placeholder:text-gray-400 resize-none"
          placeholder="What's on your mind?"
        />
      </div>
      
      <button
        type="submit"
        className="w-full bg-black text-white py-4 px-8 uppercase tracking-widest text-sm font-bold hover:bg-gray-900 transition-colors"
      >
        Send Message
      </button>
    </form>
  );
}
```

## Typography Guidelines

### Font Pairing

**Modern & Professional**:
```css
--font-heading: 'Inter', system-ui, sans-serif;
--font-body: 'Inter', system-ui, sans-serif;
font-weight: 700 for headings, 400 for body
```

**Editorial & Elegant**:
```css
--font-heading: 'Playfair Display', Georgia, serif;
--font-body: 'Source Sans Pro', sans-serif;
```

**Tech & Precise**:
```css
--font-heading: 'Space Grotesk', monospace;
--font-body: 'IBM Plex Sans', sans-serif;
```

### Type Scale

Use a consistent scale (e.g., 1.25 ratio):
```css
--text-xs: 0.64rem;   /* 10.24px */
--text-sm: 0.8rem;    /* 12.8px */
--text-base: 1rem;    /* 16px */
--text-lg: 1.25rem;   /* 20px */
--text-xl: 1.563rem;  /* 25px */
--text-2xl: 1.953rem; /* 31.25px */
--text-3xl: 2.441rem; /* 39px */
--text-4xl: 3.052rem; /* 48.83px */
```

## Color Systems

### Building a Palette

1. **Choose a primary color** that reflects brand
2. **Generate shades** (50-900 scale)
3. **Add neutral grays** for text and backgrounds
4. **Select accent colors** for states (success, error, warning)
5. **Ensure accessibility** (4.5:1 contrast minimum)

```javascript
// Example: Generate color shades
const primaryShades = {
  50:  '#f0f9ff',
  100: '#e0f2fe',
  200: '#bae6fd',
  300: '#7dd3fc',
  400: '#38bdf8',
  500: '#0ea5e9',  // Base color
  600: '#0284c7',
  700: '#0369a1',
  800: '#075985',
  900: '#0c4a6e',
};
```

## Accessibility Checklist

- [ ] **Color contrast**: Minimum 4.5:1 for text, 3:1 for UI components
- [ ] **Keyboard navigation**: All interactive elements accessible via keyboard
- [ ] **Focus indicators**: Visible focus states on all interactive elements
- [ ] **ARIA labels**: Proper labels for screen readers
- [ ] **Semantic HTML**: Use correct HTML elements
- [ ] **Alt text**: Descriptive alt text for images
- [ ] **Form labels**: Associated labels for all inputs
- [ ] **Error messages**: Clear, actionable error messages

## Performance Best Practices

### Loading Strategy
```tsx
// Lazy load components
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// Use Suspense for loading states
<Suspense fallback={<Spinner />}>
  <HeavyComponent />
</Suspense>
```

### Image Optimization
```tsx
// Use Next.js Image component or similar
<Image
  src="/hero.jpg"
  width={1200}
  height={600}
  alt="Hero image"
  priority // For above-the-fold images
  placeholder="blur"
/>
```

### CSS Optimization
- Use CSS-in-JS with critical CSS extraction
- Implement CSS modules for component scoping
- Minimize animation complexity
- Use `will-change` sparingly

## Animation Principles

### Micro-interactions

```tsx
// Subtle hover effect
const buttonVariants = {
  initial: { scale: 1 },
  hover: { 
    scale: 1.05,
    transition: { duration: 0.2, ease: 'easeOut' }
  },
  tap: { scale: 0.95 }
};

<motion.button
  variants={buttonVariants}
  initial="initial"
  whileHover="hover"
  whileTap="tap"
>
  Click me
</motion.button>
```

### Page Transitions

```tsx
const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.5, ease: [0.6, -0.05, 0.01, 0.99] }
  },
  exit: { opacity: 0, y: -20 }
};
```

## Responsive Design

### Mobile-First Approach

```tsx
// Start with mobile styles, enhance for larger screens
<div className="
  px-4 py-8
  md:px-8 md:py-12
  lg:px-16 lg:py-16
  xl:px-24 xl:py-20
">
  {/* Content */}
</div>
```

### Container Queries (Modern)

```css
@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}
```

## Common Pitfalls to Avoid

❌ **Don't**:
- Use default blue links and browser styles
- Create walls of text without hierarchy
- Ignore accessibility
- Use too many fonts (max 2-3)
- Animate everything
- Make users guess (unclear CTAs)

✅ **Do**:
- Make intentional design decisions
- Create clear visual hierarchy
- Test with real users
- Optimize for performance
- Consider accessibility from the start
- Use consistent spacing and colors

## Tools and Resources

- **Design Tools**: Figma, Sketch, Adobe XD
- **Color**: Coolors.co, Adobe Color, Realtime Colors
- **Typography**: Google Fonts, Font Pair, Type Scale
- **Accessibility**: WebAIM Contrast Checker, axe DevTools
- **Inspiration**: Dribbble, Awwwards, SiteInspire, Mobbin

## References

- [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/WCAG21/quickref/)
- [Material Design](https://material.io/design)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Refactoring UI](https://www.refactoringui.com/)
- [Laws of UX](https://lawsofux.com/)
