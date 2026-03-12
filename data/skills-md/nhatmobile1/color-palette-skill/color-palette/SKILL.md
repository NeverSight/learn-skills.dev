---
name: color-palette
description: Create distinctive, accessible color palettes for UI/web design that avoid generic AI aesthetics. Use when designing websites, applications, or any digital interface requiring thoughtful color selection. Provides curated domain-specific palettes, color theory guidance, accessibility validation, and strategies to break away from overused patterns (purple gradients, orange-teal combinations, generic tech blues). Includes contrast checkers, palette generators, and comprehensive reference materials organized by domain (Tech/SaaS, E-commerce, Healthcare, Finance, Creative, Food).
---

# Color Palette Creation

## Overview

This skill helps create distinctive, accessible color palettes for UI and web design that stand out from generic AI-generated aesthetics. It provides color theory guidance, curated domain-specific examples, accessibility validation tools, and strategies to avoid overused patterns.

## When to Use This Skill

Use this skill when:
- Designing color palettes for websites, apps, or digital interfaces
- Users request color schemes for specific domains or industries
- Building design systems or style guides
- Ensuring accessibility compliance (WCAG AA/AAA)
- Breaking away from generic "AI-looking" designs
- Need validation of existing color choices

## Workflow

### Step 1: Understand Context and Requirements

Before selecting or generating colors, gather essential context:

**Domain/Industry Questions:**
- What industry or domain is this for? (Tech/SaaS, E-commerce, Healthcare, Finance, Creative, Food, etc.)
- What emotions or associations should the palette convey?
- Are there existing brand colors to work with or extend?

**Technical Requirements:**
- Light mode, dark mode, or both?
- Accessibility requirements? (WCAG AA minimum, AAA preferred)
- How many colors needed? (Typically: 1-2 primary, 1-2 secondary, 1-2 accents, full neutral scale, semantic colors)

**Distinctiveness Goals:**
- Should this avoid looking "AI-generated"?
- Any specific colors or combinations to avoid?
- Preference for warm vs cool tones?

### Step 2: Select Base Approach

Choose one of these approaches based on the context:

#### Approach A: Domain-Specific Curated Palettes

**When to use:** Clear industry/domain, want proven effective combinations

**Process:**
1. Read `references/color-palette-ui-design-reference.md` focusing on the relevant domain section
2. Present 2-3 palette options from that domain
3. Explain what makes each effective
4. Adapt the chosen palette if needed

**Example domains:**
- Tech/SaaS: Trust & stability, Modern minimal, Professional dashboards, Dark mode
- E-commerce: Fashion, Beauty, Sports, Home, Luxury
- Healthcare: Calm professional, Soothing apps, Mental health/wellness
- Finance: Traditional banking, Modern fintech, Investment platforms
- Creative/Portfolio: Bold & modern, Minimalist, Artistic, Developer portfolios
- Food/Restaurant: Warm & appetizing, Delivery apps, Organic, Upscale

#### Approach B: Generate from Brand Color

**When to use:** Starting from existing brand color(s), need to build complete system

**Process:**
1. Use `scripts/generate_palette.py` to create color scales:
   ```bash
   python scripts/generate_palette.py #3B82F6 scale
   ```
2. Generate harmonious colors using color theory:
   ```bash
   python scripts/generate_palette.py #3B82F6 complementary
   python scripts/generate_palette.py #3B82F6 triadic
   python scripts/generate_palette.py #3B82F6 analogous
   ```
3. Validate contrast ratios (Step 3)
4. Apply 60-30-10 rule (see reference document)

#### Approach C: Custom Palette from Inspiration

**When to use:** Need unique, distinctive palette; have specific inspiration sources

**Process:**
1. If user provides inspiration (image, artwork, location), extract colors from that source
2. Review "Common AI Design Pitfalls" section in references to avoid generic patterns
3. Apply color harmony principles from reference document
4. Use "Anti-AI Checklist" to ensure distinctiveness
5. Validate accessibility (Step 3)

### Step 3: Validate Accessibility

**Always validate contrast ratios** using the contrast checker script:

```bash
python scripts/check_contrast.py <foreground> <background> <text-size>
```

**Examples:**
```bash
# Check normal text on background
python scripts/check_contrast.py #1A1A1A #FFFFFF normal

# Check large text (headings)
python scripts/check_contrast.py #4A4A4A #FFFFFF large

# Check button contrast
python scripts/check_contrast.py #FFFFFF #3B82F6 normal
```

**Requirements:**
- Normal text: 4.5:1 minimum (AA), 7:1 preferred (AAA)
- Large text (18pt+): 3:1 minimum (AA), 4.5:1 preferred (AAA)
- UI components (buttons, borders, icons): 3:1 minimum

**If validation fails:**
- Darken the foreground color
- Lighten the background color
- Use the palette generator to create darker/lighter shades
- Consider alternative color combinations

### Step 4: Structure Complete Color System

Organize the palette following design system best practices:

#### Primary Colors
- Main brand identity (1-2 colors)
- Full scale (50-950 shades)
- Use for: Logo, primary buttons, active states

#### Secondary Colors
- Supporting brand colors (1-3 colors)
- Full or partial scale depending on usage
- Use for: Secondary buttons, icons, less prominent features

#### Accent Colors
- Attention-drawing colors (1-2 colors)
- Apply 60-30-10 rule: Use for only 10% of the design
- Use for: CTAs, highlights, badges, notifications

#### Neutral Colors
- Grays/neutrals for structure
- Full scale (50-950) required
- Use for: Text, backgrounds, borders, disabled states

#### Semantic/Functional Colors
- Success: Green shades
- Error: Red shades
- Warning: Yellow/Orange shades
- Info: Blue shades

**Naming Convention:**
```
Primitive tokens: blue-500, gray-100, red-700
Semantic tokens: background-surface-primary, text-body, button-primary-background
```

### Step 5: Avoid AI Design Pitfalls

Before finalizing, review against the Anti-AI Checklist from the reference document:

**Critical checks:**
- [ ] NOT purple/blue gradients on white (unless brand-appropriate)
- [ ] NOT orange and teal combination
- [ ] NOT high-saturation gradients everywhere
- [ ] Includes context-specific colors (not generic)
- [ ] Has real-world inspiration source
- [ ] Reflects specific brand story or domain
- [ ] Uses unique shades, not default values

**If any red flags appear**, revise using:
- Nature-inspired gradients instead of purple-blue
- Muted accents instead of neon on dark
- Unexpected color combinations that still harmonize
- Industry-specific references from the curated palettes

### Step 6: Present the Palette

Format the final palette clearly:

```
Primary Color - [Name] (#HEX)
├─ 50:  #XXXXXX
├─ 100: #XXXXXX
├─ ...
└─ 950: #XXXXXX

Secondary Color - [Name] (#HEX)
[Similar structure]

Accent Color - [Name] (#HEX)
[Similar structure]

Neutral Colors - Gray (#HEX)
[Full scale]

Semantic Colors:
├─ Success: #XXXXXX (contrast: X.X:1)
├─ Error:   #XXXXXX (contrast: X.X:1)
├─ Warning: #XXXXXX (contrast: X.X:1)
└─ Info:    #XXXXXX (contrast: X.X:1)
```

**Include:**
- Color names and hex values
- Contrast ratios for key combinations
- Usage guidance (what each color is for)
- Why this palette is effective for the domain
- How it avoids generic AI patterns

## Quick Reference

### Color Theory Harmonies

**Complementary**: Colors opposite on color wheel (high contrast, maximum tension)
**Analogous**: Adjacent colors (harmonious, smooth, low contrast)
**Triadic**: Three colors equally spaced (vibrant, balanced)
**Split-Complementary**: Base + two adjacent to complement (high contrast, less tension)

For detailed explanations, see `references/color-palette-ui-design-reference.md` → Color Theory Fundamentals

### 60-30-10 Rule

**60%** - Dominant color (backgrounds, main surfaces)
**30%** - Secondary color (cards, secondary surfaces)
**10%** - Accent color (CTAs, highlights, focal points)

### Common Pitfalls to Avoid

1. **Purple/blue gradients** - Most overused AI pattern
2. **Orange and teal** - Instantly recognizable as AI-generated
3. **High-saturation everywhere** - No visual rest
4. **Generic semantic colors** - Standard blue/green/red without uniqueness
5. **Template thinking** - Not considering specific context

### Resources

**scripts/check_contrast.py** - Validate WCAG contrast ratios
**scripts/generate_palette.py** - Generate color scales and harmonies
**references/color-palette-ui-design-reference.md** - Comprehensive guide including:
- Color theory fundamentals
- Color psychology
- 60+ curated palette examples by domain
- Design system approaches (Material Design, Tailwind, Ant Design)
- Accessibility guidelines
- Anti-AI design strategies

## Examples

### Example 1: Tech SaaS Dashboard

**User request:** "Create a professional color palette for a B2B SaaS analytics dashboard"

**Process:**
1. Read Tech/SaaS section from references
2. Choose "Professional SaaS Dashboard" palette as base
3. Validate contrast ratios
4. Extend with full scales using generator

**Output:**
```
Primary: Professional Blue (#0072BB)
├─ Use for: Primary actions, active states, links
└─ Contrast validated: 4.6:1 on white background ✓

Secondary: Dark Navy (#28324E)
├─ Use for: Headers, important text, secondary buttons
└─ Contrast validated: 12.4:1 on white background ✓

Success: Soft Green (#77D38C)
Warning: Amber (#F0AD4E)
Error: Muted Red (#C1666B)

Neutral: Blue-Gray scale (#B5BDD7 to #28324E)

Why this works:
- Calm blue conveys trust and professionalism
- Muted semantic colors don't overwhelm data visualizations
- Full blue-gray neutral scale maintains cohesive color temperature
- Avoids purple-gradient cliche while staying professional
```

### Example 2: E-commerce Fashion Site

**User request:** "I need warm, earthy colors for a sustainable fashion e-commerce site"

**Process:**
1. Read E-commerce → Fashion & Apparel from references
2. Select earthy palette, modify for sustainability emphasis
3. Validate all key combinations

**Output:**
```
Primary: Dark Teal (#264653)
├─ Evokes nature, sustainability, calm
└─ Use for: Navigation, primary buttons

Secondary: Living Teal (#2A9D8F)
├─ Fresh, natural, growth
└─ Use for: Highlights, hover states

Accent 1: Terracotta (#E76F51)
├─ Warm, earthy, organic
└─ Use for: CTAs, sale badges

Accent 2: Gold (#E9C46A)
└─ Use for: Premium products, special offers

Why this avoids AI-generic:
- Uses earthy tones instead of bright tech colors
- Warm accents on cool base (intentional temperature mixing)
- Terracotta is distinctive, not overused
- Reflects real sustainable fashion brand aesthetics
```

### Example 3: Dark Mode App

**User request:** "Dark mode palette for a creative tools app, want to avoid the generic neon-on-dark look"

**Process:**
1. Review "Dark Mode SaaS" and "Common AI Pitfalls" sections
2. Choose muted accents instead of full neon
3. Generate custom scales
4. Validate all contrast ratios

**Output:**
```
Background: Very Dark Navy (#0A0E27)
Surface: Dark Blue-Gray (#1E2749)

Primary: Vibrant Blue (#4A9EFF)
├─ Bright enough for contrast, not neon
└─ Contrast: 8.2:1 on background ✓

Secondary: Lavender Indigo (#8B7FE8)
├─ Creative, sophisticated
└─ Contrast: 7.1:1 on background ✓

Text: Off-White (#E8EAF6)
└─ Contrast: 13.2:1 on background ✓

Why this works:
- Deep, rich backgrounds (not pure black)
- Accents are vibrant but not harsh neon
- Lavender adds creativity without purple-gradient cliche
- Excellent contrast without eye strain
```

## Tips for Success

1. **Always start with context** - Don't jump to colors before understanding domain, audience, and purpose
2. **Use references liberally** - The curated palettes have been validated in real products
3. **Validate early and often** - Check contrast ratios as you build, not at the end
4. **Be distinctive** - Actively avoid the most common AI patterns
5. **Tell a story** - Every color choice should relate to brand narrative or domain
6. **Consider the whole system** - Think beyond just primary colors to complete scales and semantic colors
7. **Test in context** - Colors look different on screens, in different lighting, next to different content

## Advanced Usage

### Creating Color Palettes from Images

If user provides an image for inspiration:
1. Identify 2-3 dominant colors manually or describe the color scheme
2. Extract hex values or approximate them
3. Use those as base colors for palette generation
4. Apply color theory to create harmonious extensions
5. Validate and refine for accessibility

### Multi-Brand Color Systems

For products with multiple brands or themes:
1. Establish shared neutral scale (used across all themes)
2. Create distinct primary colors for each brand
3. Ensure all themes meet same accessibility standards
4. Use semantic token naming for easy theme switching
5. Document when to use each brand variant

### Accessibility-First Approach

For products requiring AAA compliance:
1. Start with contrast requirements (7:1 for normal text)
2. Work backward to find valid color combinations
3. Use darker/lighter shades than typical
4. Test with colorblind simulators
5. Provide high-contrast mode as option

## Common Questions

**Q: How do I make a palette feel unique without sacrificing usability?**
A: Use unique shades of standard semantic colors. Green for success is expected, but use a distinctive shade with appropriate cultural/domain context.

**Q: The palette generator created colors that don't match my brand. What do I do?**
A: The generator creates mathematically uniform scales. You can manually adjust specific levels while keeping others, or use it as a starting point and refine by hand.

**Q: How many colors should a complete palette have?**
A: Minimum: 1 primary (with scale), 1 neutral (with scale), 4 semantic colors. Typical: 1-2 primary, 1-2 secondary, 1-2 accent, 1 neutral (all with scales), 4 semantic colors. Complex: Multiple primaries, extensive semantic colors, specialized scales.

**Q: What if the user insists on purple gradients?**
A: If it's genuinely part of their brand, make it distinctive: use unique purple shades, unexpected gradient combinations, or pair with unexpected accent colors. Avoid the default #6366F1 → #8B5CF6 → white pattern.
