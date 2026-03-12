---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
---

# Frontend Design Expert

Create production-grade frontend interfaces that are distinctive, polished, and avoid generic "AI slop" aesthetics. This skill activates when building web components, pages, or applications.

## Design Thinking

Before writing code, understand context and commit to intentional design choices:

1. **Purpose**: What problem does this interface solve? What action should users take?
2. **Audience**: Upper middle class American Muslim professionals (doctors, lawyers, engineers)
3. **Tone**: Pick a direction with conviction—minimalist restraint, data-forward trust, or warm sophistication
4. **Constraints**: React 19, Tailwind v4, existing theme system, accessibility requirements
5. **Differentiation**: What makes this memorable? What will someone recall after leaving?

**Critical**: Bold intentionality beats timid compromise. A clear aesthetic point-of-view—whether minimal or maximal—is always better than splitting the difference.

---

## Audience Profile

The primary audience is upper middle class American Muslim professionals:

| Trait | Implication |
|-------|-------------|
| **Highly educated** | Don't oversimplify; they understand nuance |
| **Time-constrained** | Get to the point; respect their attention |
| **Discerning** | They notice quality (or lack thereof) |
| **Data-literate** | Show numbers, methodology, sources |
| **Skeptical of hype** | Substance over marketing speak |
| **Quality expectations** | They use Stripe, Notion, Apple—match that bar |

**What they value:**
- Transparency over emotional appeals
- Data over vague impact claims
- Intellectual respect over patronizing explanations
- Efficiency over decoration

---

## Project Tech Stack

### Framework
- **React 19** with Vite 6.2
- **TypeScript 5.8** for type safety
- **Tailwind CSS v4.1** with PostCSS (no custom config file)

### Theme System

**Light/Dark Mode:**
```tsx
import { useLandingTheme } from '@/contexts/LandingThemeContext';
const { isDark, toggleTheme } = useLandingTheme();
```

**Brand Variants:**
```tsx
import { useTheme } from '@/types/theme';
const { variant } = useTheme(); // 'amal' | 'third-bucket'
```

### Component Patterns
- Icons: Lucide React (`import { Icon } from 'lucide-react'`)
- Charts: Recharts for data visualization
- Sanitization: DOMPurify for user-generated content

### Key Reference Files
- `website/src/components/CharityCard.tsx` - Color pattern examples
- `website/src/components/BaselineCharityDetail.tsx` - Wallet tag styling
- `website/src/themes.tsx` - Experimental theme presets
- `website/contexts/LandingThemeContext.tsx` - Dark mode implementation

---

## Typography

| Purpose | Class | Notes |
|---------|-------|-------|
| Headlines, brand moments | `font-merriweather` | Serif, distinctive |
| Body text, UI | `font-sans` | System stack, readable |
| Quranic references | `font-arabic` | Arabic typography only |
| Data displays, technical | `font-mono` | Monospace for numbers |

**Typography Principles:**
- Clear hierarchy: One dominant element per section
- Readable line lengths: ~60-75 characters
- Generous line height: `leading-relaxed` for body copy
- Restrained headings: Meaningful, not "Welcome to our platform"

---

## Color & Theme

### Primary Palette
- **Emerald**: Primary actions, positive states (`emerald-600`, `emerald-700`)
- **Slate**: Neutrals, backgrounds (`slate-100` to `slate-950`)
- **White/Black**: Text, highest contrast

### Semantic Colors (Wallet Tags - Self-Assertion Model)
- **Emerald** (`emerald-700`): Zakat Eligible (ZAKAT-ELIGIBLE) - charity claims zakat on website
- **Indigo** (`indigo-700`): Strategic Sadaqah (SADAQAH-STRATEGIC) - high-impact systemic work
- **Gray** (`gray-600`): General Sadaqah (SADAQAH-GENERAL) - standard charitable giving
- **Slate** (`slate-500`): Insufficient Data (INSUFFICIENT-DATA)

### Dark Mode
- Background: `slate-950` (not pure black)
- Surface: `slate-900` for cards
- Text: `white` / `slate-400` for hierarchy
- Always provide dark mode variants: `isDark ? 'bg-slate-900' : 'bg-white'`

### Color Pattern Example
```tsx
const colors = {
  bg: isDark ? 'bg-slate-900' : 'bg-white',
  text: isDark ? 'text-white' : 'text-slate-900',
  muted: isDark ? 'text-slate-400' : 'text-slate-600',
  border: isDark ? 'border-slate-800' : 'border-slate-200',
};
```

---

## Motion & Animation

**Philosophy**: Purposeful, not decorative. Every animation should serve UX.

| Purpose | Pattern |
|---------|---------|
| Standard interactive | `transition-all duration-300` |
| Theme switching | `transition-colors duration-500` |
| Hover lift | `hover:shadow-lg hover:-translate-y-1` |
| Arrow indicators | `group-hover:translate-x-1` |

**Avoid**: Parallax for its own sake, spinners that spin forever, bouncing elements, page load fireworks.

---

## What NOT to Do (AI Slop Detection)

### Visual Anti-Patterns

**AVOID:**
- Generic gradients (purple→blue on white)
- Glassmorphism cards without purpose
- Oversized hero sections with tiny CTAs
- Parallax scrolling that adds nothing
- Blob shapes behind text
- Neon accents on dark backgrounds (the "Discord look")
- Cards with excessive rounded corners + drop shadows
- Placeholder icons (generic house, heart, people silhouettes)

### Typography Anti-Patterns

**AVOID:**
- Inter, Roboto, Poppins, Montserrat (the default AI fonts)
- Hero text 80px+ with no content hierarchy
- Excessive letter-spacing everywhere
- ALL CAPS subheadings on everything
- "Welcome to our platform" headers

### Islamic Design Anti-Patterns

**AVOID:**
- Bright green (#00FF00) as primary (the "masjid green" trap)
- Crescent moon icons everywhere
- Mosque dome silhouettes in backgrounds
- Stock photos of people praying or giving money
- Arabic calligraphy as meaningless decoration
- Overwhelming geometric tessellations
- "Salam" as the hero greeting (performative authenticity)

### Charity Website Anti-Patterns

**AVOID:**
- "Just $1 can save a life" emotional manipulation
- Crying children imagery
- Progress bars showing "90% of goal reached" (fake urgency)
- Impact counters that spin up on scroll
- Vague claims: "We've helped millions" without methodology
- Generic world map with pins
- "Your donation goes directly to..." without actual breakdown

### Copy Anti-Patterns

**AVOID:**
- "Empowering communities through innovative solutions"
- "Making a difference, one [X] at a time"
- "Join our mission to transform..."
- Bullet points all starting with verbs (Empower, Transform, Enable)
- Three-column feature grids with identical structure
- FAQ sections with softball questions

### Interaction Anti-Patterns

**AVOID:**
- Hover effects on everything
- Skeleton loaders that never resolve
- Infinite scroll without pagination option
- Modal popups on page load
- Chatbot widgets in bottom-right corner
- Newsletter popup within 5 seconds

### Technical Tells (These Scream "AI Generated")

**AVOID:**
- Components that ignore theme context
- Hardcoded colors instead of Tailwind tokens
- Inconsistent spacing (mixing `px-4` with `px-6` randomly)
- Missing dark mode variants
- Buttons without proper states (hover, active, disabled)
- No loading states for async operations
- No error states
- No empty states

---

## Trust Architecture

Build trust through transparency, not emotional appeals.

### Show Your Work
- Display data sources (Form 990, ProPublica, IRS data)
- Link to primary documents
- Explain methodology in accessible terms
- Show confidence levels when data is uncertain

### Acknowledge Complexity
- Note where scholars differ on zakat eligibility
- Don't pretend contested topics are settled
- Provide nuance, not false certainty

### Avoid Trust Destroyers
- Vague impact claims ("millions helped")
- Round numbers without context
- Hidden methodology
- Unverifiable testimonials

---

## Cultural Authenticity

### Do
- Bismillah in Arabic (subtle, not dominant)
- Geometric patterns used sparingly
- References to Islamic scholarship with proper citation
- Inclusive of diverse Muslim backgrounds (not just Arab aesthetics)
- Respect for legitimate differences (madhab pluralism)

### Don't
- Performative religiosity (excessive "insha'Allah" in UI copy)
- Stereotypical imagery (domes, minarets, prayer photos)
- Assuming one correct interpretation
- Excluding converts, non-Arabic speakers, or non-traditional Muslims

---

## Implementation Checklist

Before shipping any component:

- [ ] Theme-aware (responds to `useLandingTheme`)
- [ ] Uses Tailwind tokens (no hardcoded colors)
- [ ] Dark mode tested
- [ ] Mobile responsive
- [ ] Loading state implemented
- [ ] Error state implemented
- [ ] Empty state implemented
- [ ] Hover/focus/active states on interactive elements
- [ ] Accessible (semantic HTML, proper contrast, keyboard navigation)
- [ ] No AI slop patterns (review list above)
