---
name: design-styles
description: "Comprehensive web design aesthetics guide for applying specific design styles to projects. Use when: (1) User mentions a specific design style name (glassmorphism, brutalist, minimalist, neomorphism, cyberpunk, etc.), (2) User asks for design style recommendations or suggestions, (3) User wants to browse/see available design styles, (4) User is starting a frontend project and needs aesthetic guidance, (5) User asks what style fits their industry/audience/brand, (6) Working with the frontend-design skill and style direction is needed. Provides actionable design direction including color palettes, typography, layout principles, and implementation examples."
---

# Design Styles

Apply professional design aesthetics to web and app projects with comprehensive style guidance, recommendations, and implementation details.

## How to Use This Skill

### 1. Apply a Specific Style by Name

When user mentions a style (e.g., "use glassmorphism", "apply brutalist design", "make it minimalist"):

1. Read `references/design-styles-comprehensive-reference.md` and locate the requested style
2. Extract key characteristics, color palettes, typography, and layout principles
3. Provide specific, actionable implementation guidance:
   - Color schemes with hex codes
   - Typography recommendations (font families, sizes, weights)
   - Layout principles (spacing, grid, structure)
   - CSS/code examples demonstrating the style
   - Component-specific guidance (buttons, cards, navigation, etc.)
4. Reference real-world examples from the guide

**Example response structure:**
```
I'll apply [STYLE NAME] to your project.

**Key Characteristics:**
- [List 3-5 defining features]

**Color Palette:**
- Primary: [hex codes]
- Secondary: [hex codes]
- Accents: [hex codes]

**Typography:**
- Headings: [font family, weights]
- Body: [font family, size]

**Layout Principles:**
- [Spacing guidelines]
- [Grid structure]
- [Key layout features]

**Implementation:**
[CSS/code examples]

**Real-world examples:** [List 2-3 from reference]
```

### 2. Recommend Styles Based on Criteria

When user asks "what design style for [X]?" or describes their project/audience/brand:

1. Read the comprehensive reference
2. Analyze based on user's criteria:
   - **Industry** → Check "Choosing the Right Style → By Industry"
   - **Target Audience** → Check "Choosing the Right Style → By Target Audience"
   - **Brand Personality** → Check "Choosing the Right Style → By Brand Personality"
   - **Project Type** → Match to industry categories
3. Recommend 2-4 appropriate styles with brief rationale
4. Ask user to select preferred style or provide more context

**Example response structure:**
```
Based on [CRITERIA], I recommend these design styles:

1. **[STYLE NAME]** - [Why it fits, 1-2 sentences]
2. **[STYLE NAME]** - [Why it fits, 1-2 sentences]
3. **[STYLE NAME]** - [Why it fits, 1-2 sentences]

Which style resonates with your vision? Or I can provide more details about any of these.
```

### 3. Browse/List Available Styles

When user asks "what design styles are available?" or "show me style options":

1. Read the comprehensive reference
2. Present the Quick Reference Table or organized categories
3. Offer to provide details on any specific style
4. Can filter by category if user specifies (e.g., "show me retro styles", "what are the modern styles?")

### 4. Combine with Frontend-Design Skill

When working alongside the frontend-design skill:

1. This skill provides the aesthetic direction (colors, typography, layout principles)
2. Frontend-design skill implements the actual code
3. Pass clear design specifications from this skill to frontend-design
4. Reference the comprehensive guide for style-specific patterns

## Design Style Categories

The comprehensive reference includes 40+ styles organized into:

- **Minimalist & Clean:** Minimalist, Flat Design, Swiss/International
- **Material & Depth:** Glassmorphism, Neomorphism, Neumorphism, Skeuomorphic
- **Maximalist & Bold:** Maximalist Chaos, Memphis Style, Collage
- **Retro & Nostalgic:** Retro-Futuristic, Y2K/Web 2.0, Vaporwave, Art Deco
- **Natural & Organic:** Organic/Natural, Wabi-Sabi, Handcrafted/Artisanal
- **Soft & Gentle:** Soft/Pastel, Kawaii/Cute, Playful/Toy-like
- **Elegant & Refined:** Luxury/Refined, Editorial/Magazine, Corporate/Enterprise
- **Raw & Unconventional:** Brutalist/Raw, Neubrutalism, Grunge, Industrial
- **Tech & Futuristic:** Cyberpunk, Terminal/Hacker, Metro/Modern UI
- **Color-Focused:** Monochromatic, Gradient/Aurora, Dark Mode
- **Layout & Structure:** Grid/Modular, Academic/Research, Outlined/Line Art
- **Interactive & Dynamic:** Kinetic/Motion-First, Atmospheric, Data Visualization
- **Other:** Corporate Memphis, Claymorphism, Isometric, Bauhaus

## Quick Selection Guide

**Common use cases:**

- **Tech/SaaS startup** → Minimalism, Glassmorphism, Gradient, Neubrutalism, Dark Mode
- **E-commerce** → Minimalism, Grid/Modular, Editorial, Luxury/Refined (depends on products)
- **Creative/Agency** → Maximalist, Memphis, Brutalist, Kinetic, Editorial
- **Wellness/Health** → Organic/Natural, Soft/Pastel, Wabi-Sabi, Glassmorphism
- **Finance/Corporate** → Swiss/International, Corporate/Enterprise, Minimalism, Dark Mode
- **Gaming/Entertainment** → Cyberpunk, Retro-Futuristic, Y2K, Maximalist, Vaporwave
- **Fashion/Luxury** → Luxury/Refined, Art Deco, Maximalist, Editorial
- **Portfolio/Personal** → Minimalist, Brutalist, Editorial, any style matching personal brand

**By audience:**

- **Gen Z** → Y2K, Vaporwave, Neubrutalism, Memphis, Playful
- **Millennials** → Minimalism, Flat Design, Organic, Gradient, Dark Mode
- **Professionals/B2B** → Swiss/International, Corporate/Enterprise, Minimalism, Editorial
- **Creatives** → Brutalism, Maximalist, Memphis, Collage, Kinetic
- **Luxury Consumers** → Luxury/Refined, Art Deco, Minimalism, Editorial

**By personality:**

- **Bold & Energetic** → Maximalist, Memphis, Cyberpunk, Y2K
- **Calm & Trustworthy** → Minimalism, Organic/Natural, Soft/Pastel, Swiss
- **Edgy & Rebellious** → Brutalism, Grunge, Cyberpunk, Neubrutalism
- **Sophisticated & Premium** → Luxury/Refined, Art Deco, Editorial, Minimalism
- **Playful & Friendly** → Playful/Toy-like, Kawaii, Corporate Memphis, Soft/Pastel
- **Technical & Professional** → Terminal/Hacker, Swiss, Corporate/Enterprise, Dark Mode

## Style Combinations

Many modern projects blend 2-3 styles. Popular combinations from the reference:

- **Minimalism + Gradients + Kinetic** (e.g., Stripe, Apple)
- **Brutalism + Bold Colors** (Neubrutalism - Gumroad, Pitch)
- **Dark Mode + Glassmorphism** (macOS, modern dashboards)
- **Organic + Soft Pastels** (Wellness apps)
- **Editorial + Data Visualization** (NYT, data journalism)
- **Flat Design + Corporate Memphis** (Big Tech illustrations)
- **Swiss Style + Minimalism** (Premium design agencies)

When suggesting combinations, ensure they complement each other and don't create visual conflict.

## Implementation Guidelines

When providing implementation details:

### Color Palettes

Provide specific hex codes:
- Primary colors (2-3)
- Secondary/accent colors (2-3)
- Neutral colors (grays, backgrounds)
- Text colors (with contrast ratios for accessibility)

### Typography

Specify:
- Font families (with web-safe alternatives or Google Fonts)
- Heading hierarchy (H1-H6 sizes and weights)
- Body text size and line height
- Letter spacing for specific styles when relevant

### Layout Principles

Define:
- Spacing system (e.g., 8px grid, specific margins/padding)
- Grid structure (columns, gutters)
- Border radius values
- Shadow specifications (for relevant styles)
- Responsive breakpoints

### Code Examples

Provide CSS/code demonstrating:
- Component styling (buttons, cards, inputs)
- Layout patterns
- Style-specific effects (glass blur, neumorphic shadows, etc.)
- Responsive behavior

### Accessibility Considerations

Note any accessibility concerns for the style:
- Color contrast ratios (WCAG AA minimum)
- Motion sensitivity (for kinetic/motion-first styles)
- Touch target sizes
- Focus states

## Best Practices

1. **Always reference the comprehensive guide** - Load `references/design-styles-comprehensive-reference.md` to get accurate, detailed information
2. **Be specific and actionable** - Don't just describe the style, provide implementation details
3. **Include real examples** - Reference the examples listed in the comprehensive guide
4. **Consider accessibility** - Always note accessibility requirements for each style
5. **Suggest combinations thoughtfully** - Ensure hybrid styles complement each other
6. **Match to user context** - Consider industry, audience, and brand when recommending
7. **Provide visual hierarchy** - Explain how the style creates hierarchy and guides user attention
8. **Note trend longevity** - Reference whether the style is timeless or trend-dependent

## Resources

### references/design-styles-comprehensive-reference.md

Complete guide to 40+ web design styles including:
- Detailed style descriptions
- Key characteristics
- Real-world examples with URLs
- Quick reference table
- Selection guides by industry, audience, brand personality
- Style combinations and hybrid approaches
- Design resources and inspiration galleries
- Best practices and accessibility notes
- Trend longevity analysis

**When to read:** Always read this file when working with design styles. It's the primary source of truth for all style information.
