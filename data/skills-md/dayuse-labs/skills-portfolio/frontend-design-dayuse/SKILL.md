---
name: frontend-design-dayuse
description: Create production-grade frontend interfaces following the Dayuse brand identity and design system. This skill should be used when the user asks to "build a page", "create a component", "design a UI", "make a frontend", "build a landing page", "create a dashboard", or any frontend development task for Dayuse. Applies the official Dayuse color palette, typography (Manrope + MaisonNeue), border-radius conventions, shadow system, and animation patterns.
---

This skill guides creation of frontend interfaces that strictly follow the Dayuse brand identity. All code produced must feel like it belongs in the Dayuse product ecosystem: warm, modern, premium, and conversion-focused.

## Design Philosophy

Dayuse is a premium day-use hotel booking platform. The brand communicates:
- **Warmth & Energy** through golden-orange gradients and accent colors
- **Trust & Clarity** through clean layouts, generous white space, and legible typography
- **Modern Premium** through glass-morphism effects, smooth animations, and refined micro-interactions
- **Conversion Focus** through prominent CTAs with gradient pill buttons and clear visual hierarchy

Before coding, determine:
- **Context**: What part of the Dayuse experience is this? (booking flow, search, marketing, dashboard, internal tool)
- **Audience**: End-user (consumer) or internal (ops/admin)?
- **Density**: Marketing pages use generous spacing; app screens can be denser
- **Priority**: What is the single most important action the user should take?

## Dayuse Brand Colors

Use these exact values. Never deviate from this palette:

### Primary Accent (CTA & Brand Energy)
- **Primary Gradient**: `linear-gradient(62deg, #FFAF36 0%, #FFC536 100%)` — all primary CTAs
- **Primary Hover**: `linear-gradient(62deg, #FF9F26 0%, #FFB526 100%)`
- **Amber Solid**: `#FFB800` — loading indicators, badges, highlights
- **Gold Alt**: `#FFC34C` — golden accent variant (brand presentations)

### Brand Extended Palette (from official presentations)
- **Orange Brand**: `#F66236` — warm accent, illustrations, data viz
- **Orange Alt**: `#FE7335` — orange variant, hover states, secondary CTAs
- **Coral Red**: `#F45C5A` — alerts, important highlights, energy accents
- **Purple**: `#6E69AC` — secondary brand accent, categories, charts
- **Purple Deep**: `#635CBA` — deeper purple variant, active states
- **Gray Mid**: `#7F7F86` — intermediate text, icons on light backgrounds

### Hero Gradients (Marketing & Landing)
- **Title Gradient**: `linear-gradient(90deg, #FEB900 0%, #FD7030 33%, #FDAA9A 67%, #B7D5D5 100%)`
- **Thinking/Loading**: `linear-gradient(90deg, #F55F30 0%, #FFAF36 25%, #FFC536 50%, #FFAF36 75%, #F55F30 100%)`

### Text Colors
- **Primary Text**: `#292935` — headings, body text, high-emphasis content
- **Secondary Text**: `#54545D` — descriptions, labels, supporting content
- **Tertiary Text**: `#8E8E93` — placeholders, timestamps, subtle info
- **Muted Text**: `#999999` — disabled states, ultra-low emphasis

### Backgrounds
- **White**: `#FFFFFF` — cards, inputs, primary surfaces
- **Light Gray**: `#F9F9F9` — page backgrounds, secondary surfaces
- **Context BG**: `#F5F5F7` — message backgrounds, info panels
- **User BG**: `#EEEEF0` — user messages, active states
- **AI Recommendation**: `linear-gradient(135deg, #FFF8ED 0%, #FFFBF5 100%)` — highlighted content

### Semantic / Status Colors
- **Teal Accent**: `#51B0B0` — features, pool icons, secondary brand accent
- **Pool Blue**: `#3597C8` — pool-related badges
- **Best Value**: `#FF5722` — urgency badges, best-value indicators
- **Popular**: `#FFC107` — popular badges
- **Support Blue**: `#2196F3` / bg `#E3F2FD` — info cards
- **Success Green**: `#4CAF50` / bg `#E8F5E9` — policy, confirmation cards
- **Warning Orange**: `#FF9800` / bg `#FFF3E0` — special offers, warnings

### Borders & Dividers
- **Primary Border**: `#EAEAEB` — inputs, card dividers
- **Secondary Border**: `#D4D4D7` — chips, secondary dividers
- **Subtle Border**: `rgba(0, 0, 0, 0.06)` — header borders

## Typography

### Font Stack
- **Primary Font**: `'Manrope', sans-serif` — all UI text. Import weights 400, 500, 600, 700, 800 from Google Fonts.
- **Display Font**: `'MaisonNeueExtended-Bold'` — hero headings, weight 800. Use sparingly for maximum impact.

### Type Scale
| Context | Size | Weight | Line Height |
|---------|------|--------|-------------|
| Hero H1 (desktop) | 56px | 800 | 1.2 |
| Hero H1 (mobile) | 36px | 800 | 1.2 |
| Page Heading | 24px | 700 | 1.3 |
| Section Heading | 20px | 600 | 1.3 |
| Card Title | 18px | 600 | 1.3 |
| Body | 14px | 400 | 1.6 |
| Subtitle | 22px (desktop) / 17px (mobile) | 500 | 1.5 |
| Small/Label | 12px | 500-600 | 1.4 |
| Caption | 11px | 500 | 1.35 |

### Letter Spacing
- Hero headings: `-1.5px`
- Mobile headings: `-0.5px`
- Headers/nav: `0.02em`

## Border Radius

Dayuse uses a specific radius system. Follow these conventions:
- **Pill / Full Round**: `100px` — buttons, inputs, badges, tags, chips
- **Circle**: `50%` — avatar, round icons, carousel dots
- **Timeslot pills**: `20px`
- **Message bubbles**: `18px`
- **Cards & Containers**: `12px`
- **Main layout containers**: `10px`
- **Secondary panels**: `8px`
- **Never**: square corners (0px) unless full-bleed mobile

## Shadows

### Elevation System
```css
/* Level 1 — Cards, subtle elevation */
box-shadow: 0 2px 12px rgba(0, 0, 0, 0.10);

/* Level 2 — Floating cards, booking panels */
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);

/* Level 3 — Dropdowns, overlays */
box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18);

/* Level 4 — Hero inputs, prominent elements */
box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);

/* Container shadow */
box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.10);
```

## Buttons

All Dayuse buttons are **pill-shaped** (`border-radius: 100px`).

### Primary CTA
```css
background: linear-gradient(62deg, #FFAF36 0%, #FFC536 100%);
color: #292935;
font-weight: 600;
font-size: 14px;
padding: 12px 24px;
border-radius: 100px;
border: none;
cursor: pointer;
transition: all 0.2s ease;
```
Hover: `background: linear-gradient(62deg, #FF9F26 0%, #FFB526 100%);`

### Secondary / Ghost Button
```css
background: rgba(255, 255, 255, 0.82);
border: 1px solid rgba(41, 41, 53, 0.14);
border-radius: 100px;
color: #292935;
padding: 12px 24px;
```
Hover: `border-color: rgba(41, 41, 53, 0.26);`

### Small Buttons / Chips
```css
padding: 4px 10px;
font-size: 12px;
border-radius: 100px;
```

## Inputs

```css
padding: 12px 20px;
border: 1px solid #EAEAEB;
border-radius: 100px;
font-family: 'Manrope', sans-serif;
font-size: 14px;
color: #292935;
background: #FFFFFF;
transition: border-color 0.2s ease;
```
Focus: `border-color: #FFAF36; outline: none;`

## Glass Morphism (Frosted Glass)

Dayuse uses glass morphism for headers and overlays:
```css
background: rgba(255, 255, 255, 0.72);
backdrop-filter: blur(16px);
-webkit-backdrop-filter: blur(16px);
```

## Animations & Transitions

### Standard Transitions
- **Quick**: `transition: all 0.2s ease;` — hover states, color changes
- **Smooth**: `transition: all 0.3s ease;` — layout shifts, reveals
- **Slow**: `transition: all 0.5s ease-in-out;` — page transitions

### Loading Pulse
```css
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.1); }
}
animation: pulse 1s infinite;
```

### Gradient Shift (for loading/thinking states)
```css
@keyframes gradientShift {
  0% { background-position: 0% center; }
  100% { background-position: 200% center; }
}
animation: gradientShift 2s linear infinite;
background-size: 200% auto;
```

## Layout Patterns

### Max Widths
- Content container: `max-width: 800px; margin: 0 auto;`
- Full-width sections: use padding `0 40px` (desktop) / `0 16px` (mobile)

### Spacing Scale
Use multiples of 4px:
- `4px` — tight gaps
- `8px` — small gaps, inline spacing
- `12px` — standard padding
- `16px` — card padding, section gaps
- `20px` — container padding
- `24px` — section margins
- `40px` — large section spacing

### Responsive Breakpoint
- **Mobile**: `max-width: 768px`
- On mobile: remove border-radius from full-width containers, stack horizontally scrollable content, reduce font sizes per type scale, hide carousel nav buttons

## Cards

### Hotel Card Pattern
```css
border-radius: 12px;
box-shadow: 0 2px 12px rgba(0, 0, 0, 0.10);
overflow: hidden;
background: #FFFFFF;
```
Image: `height: 160px; object-fit: cover;`
Content: `padding: 12px 16px;`

### Info Cards (Support / Policy / Special)
Use the semantic color pairs:
- Support: bg `#E3F2FD`, title `#1976D2`, icon `#2196F3`
- Special: bg `#FFF3E0`, title `#F57C00`, icon `#FF9800`
- Policy: bg `#E8F5E9`, title `#2E7D32`, icon `#4CAF50`
All with `border-radius: 12px; padding: 16px;`

## Scrollbar

Hide scrollbars for clean appearance:
```css
scrollbar-width: none;
-ms-overflow-style: none;
&::-webkit-scrollbar { display: none; }
```

## Implementation Checklist

Before delivering any frontend code, verify:

1. [ ] `font-family: 'Manrope', sans-serif` is set globally
2. [ ] Google Fonts import includes Manrope weights 400-800
3. [ ] Primary CTA uses the golden gradient, not a flat color
4. [ ] All buttons and inputs have `border-radius: 100px`
5. [ ] Cards have `border-radius: 12px` with appropriate shadow
6. [ ] Text colors use the exact Dayuse palette (never pure black `#000`)
7. [ ] Spacing follows the 4px grid
8. [ ] Mobile breakpoint at 768px is handled
9. [ ] Transitions on interactive elements (min `0.2s ease`)
10. [ ] No generic fonts (Inter, Roboto, Arial, system-ui)

## Additional Resources

### Reference Files
For the complete design token inventory, consult:
- **`references/design-system.md`** — Full color palette, shadows, spacing, and component specs
- **`references/components.md`** — Dayuse-specific component patterns (hotel cards, booking UI, carousel, chat interface)
