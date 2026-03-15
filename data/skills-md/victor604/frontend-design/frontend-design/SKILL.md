---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
---

# Frontend Design

Transform web interfaces into bold, memorable experiences with distinctive aesthetics and production-grade implementation.

## When to Use This Skill

Use when:
- User uploads a screenshot asking for design improvements
- User requests to build a website, landing page, or web app
- User asks to "make it look better" or "improve the design"
- User wants to create a dashboard, portfolio, or marketing site
- User needs to transform existing UI into something memorable
- User asks for creative or bold design direction

## Design Thinking Process

Before writing any code, analyze and commit to a design direction:

### 1. Understand Context (30 seconds)

Ask yourself:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Users**: Technical? Non-technical? Age group? Context of use?
- **Content**: Heavy text? Visual-first? Data-driven? E-commerce?
- **Brand**: Startup? Enterprise? Creative? Professional? Playful?

### 2. Choose Bold Aesthetic Direction (CRITICAL)

Pick ONE extreme direction and commit fully:

**Minimalist Directions:**
- **Brutally Minimal** - Stark contrast, system fonts, zero decoration, maximum whitespace
- **Swiss Modernism** - Grid-based, geometric, structured, limited color
- **Japanese Zen** - Natural materials, subtle shadows, breathing room, muted tones
- **Scandinavian** - Clean lines, natural light, soft colors, functional beauty

**Maximalist Directions:**
- **Maximalist Chaos** - Layered elements, bold typography, explosive color, controlled chaos
- **Neo-Brutalism** - Bold shapes, thick borders, shadow extrusion, high contrast
- **Y2K/Cyber** - Metallic gradients, chrome effects, futuristic UI, neon accents
- **Retro-Futuristic** - 70s/80s sci-fi, analog/digital fusion, warm gradients

**Distinctive Styles:**
- **Editorial/Magazine** - Bold typography hierarchy, generous images, asymmetric grids
- **Art Deco/Geometric** - Symmetry, gold accents, geometric patterns, luxury feel
- **Organic/Natural** - Curves, earth tones, textures, hand-drawn elements
- **Soft/Pastel** - Gentle gradients, rounded corners, light colors, dreamy atmosphere
- **Industrial/Utilitarian** - Raw materials, monospace fonts, technical aesthetic
- **Glassmorphism** - Frosted glass effects, transparency, layered depth, subtle blur
- **Neumorphism** - Soft shadows, subtle extrusion, tactile interfaces
- **Claymorphism** - 3D clay-like textures, soft shadows, playful depth

**NEVER** choose generic, context-free aesthetics. The direction must fit the purpose.

### 3. Define Differentiation

What makes this design UNFORGETTABLE?

Examples:
- "The hero section uses diagonal type layout with aggressive cropping"
- "Navigation dissolves into view with particle effects"
- "Cards cast dramatic shadows that respond to cursor position"
- "Typography scales dramatically from 12px to 120px in one scroll"
- "Background has animated gradient mesh that shifts with scroll"
- "Interactive elements have tactile, physics-based feedback"

**One Memorable Thing Rule**: Every design needs ONE standout feature people will remember.

### 4. Technical Constraints

Consider:
- Framework (HTML/CSS, React, Vue, etc.)
- Performance requirements
- Accessibility (WCAG AA minimum)
- Browser support
- Animation performance
- Responsive behavior

## Typography: The Foundation

Typography is 80% of design. Get this right first.

### Font Selection Strategy

**AVOID THESE OVERUSED FONTS:**
- ❌ Inter
- ❌ Roboto
- ❌ Arial
- ❌ Helvetica
- ❌ System fonts (unless intentionally brutalist)
- ❌ Space Grotesk (overused in AI designs)

**RECOMMENDED FONT CATEGORIES:**

**Display/Heading Fonts (Bold Personality):**
- Serif: Playfair Display, Crimson Pro, Spectral, Lora, Fraunces
- Sans-serif: DM Sans, Manrope, Outfit, Sora, Cabinet Grotesk, Archivo
- Geometric: Montserrat, Raleway, Poppins (use sparingly)
- Condensed: Anton, Bebas Neue, Oswald, Barlow Condensed
- Editorial: Bodoni Moda, Libre Baskerville, Cormorant
- Experimental: Righteous, Unbounded, Rubik, Recursive

**Body/Text Fonts (Readable Comfort):**
- Classic: Source Sans Pro, Public Sans, IBM Plex Sans, Work Sans
- Modern: Instrument Sans, Geist, Satoshi, Plus Jakarta Sans
- Editorial: Lora, Merriweather, Source Serif Pro, Bitter
- Technical: JetBrains Mono, Fira Code, IBM Plex Mono

### Typography Hierarchy

Create dramatic contrast in scale:

```css
/* GOOD - Dramatic contrast */
.hero-title { font-size: clamp(48px, 8vw, 120px); }
.section-title { font-size: clamp(32px, 4vw, 64px); }
.body-text { font-size: 18px; }
.caption { font-size: 14px; }

/* BAD - Timid scaling */
.hero-title { font-size: 36px; }
.section-title { font-size: 24px; }
.body-text { font-size: 16px; }
```

### Font Pairing Patterns

**Pattern 1: Contrast** (Serif + Sans)
```css
:root {
  --font-display: 'Playfair Display', serif;
  --font-body: 'DM Sans', sans-serif;
}
```

**Pattern 2: Harmony** (Same family, different weights)
```css
:root {
  --font-display: 'Outfit', sans-serif;
  --font-body: 'Outfit', sans-serif;
  --weight-display: 700;
  --weight-body: 400;
}
```

**Pattern 3: Editorial** (Display Serif + Text Serif)
```css
:root {
  --font-display: 'Fraunces', serif;
  --font-body: 'Lora', serif;
}
```

## Color Theory & Themes

### Avoid Generic Palettes

**NEVER USE:**
- ❌ Purple gradients on white background
- ❌ Blue (#0070f3) + White (Vercel clone)
- ❌ Generic rainbow gradients
- ❌ Equal distribution of colors

### Color Strategy

**Dominant + Accent Pattern:**
```css
:root {
  /* One dominant color (60%) */
  --primary: #1a1a1a;
  
  /* One accent color (30%) */
  --accent: #ff6b35;
  
  /* One highlight (10%) */
  --highlight: #f7f052;
  
  /* Neutrals */
  --background: #fafafa;
  --text: #2d2d2d;
}
```

**Monochromatic with Punch:**
```css
:root {
  /* Single hue, varied lightness */
  --color-900: #0a2540;
  --color-700: #1a4d7a;
  --color-500: #2a7ab0;
  --color-300: #5fa8d3;
  --color-100: #b8dced;
  
  /* One contrasting accent */
  --accent: #ff6b35;
}
```

**Natural/Earthy:**
```css
:root {
  --clay: #d4a574;
  --stone: #6b7280;
  --moss: #4a5d23;
  --sand: #f4f1e8;
  --rust: #a0522d;
}
```

**High Contrast/Bold:**
```css
:root {
  --black: #000000;
  --white: #ffffff;
  --red: #ff0000;
  --yellow: #ffff00;
}
```

### Dark Mode Excellence

Don't just invert colors:

```css
/* GOOD - Thoughtful dark mode */
:root[data-theme="dark"] {
  --background: #0a0a0a;
  --surface: #1a1a1a;
  --text: #e5e5e5;
  --text-muted: #a3a3a3;
  --border: rgba(255,255,255,0.1);
  --accent: #ff6b35; /* Slightly desaturated */
}

/* BAD - Simple inversion */
:root[data-theme="dark"] {
  --background: #333;
  --text: #fff;
}
```

## Motion & Animation

### Animation Philosophy

**One Orchestrated Moment > Many Scattered Micro-interactions**

Focus on:
1. **Page Load** - Staggered reveals create delight
2. **Scroll Triggers** - Major section transitions
3. **Hover States** - Surprising, meaningful responses
4. **State Changes** - Smooth transitions between UI states

### CSS-First Approach

Prefer CSS animations for performance:

```css
/* Staggered fade-in on load */
.hero-content > * {
  animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) backwards;
}

.hero-content > *:nth-child(1) { animation-delay: 0.1s; }
.hero-content > *:nth-child(2) { animation-delay: 0.2s; }
.hero-content > *:nth-child(3) { animation-delay: 0.3s; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### High-Impact Hover Effects

```css
/* Lift & Shadow */
.card {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1),
              box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* Color shift */
.button {
  background: linear-gradient(135deg, var(--color-1), var(--color-2));
  background-size: 200% 200%;
  transition: background-position 0.5s ease;
}

.button:hover {
  background-position: 100% 100%;
}

/* Morphing border */
.link {
  position: relative;
}

.link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--accent);
  transition: width 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.link:hover::after {
  width: 100%;
}
```

### Scroll-Triggered Animations

```css
/* Elements start invisible */
.reveal {
  opacity: 0;
  transform: translateY(50px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

/* Add visible class via JavaScript */
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
```

```javascript
// Intersection Observer for scroll reveals
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

### React Motion (Framer Motion)

For React projects, use Framer Motion:

```jsx
import { motion } from 'framer-motion';

// Staggered children
<motion.div
  initial="hidden"
  animate="visible"
  variants={{
    visible: { transition: { staggerChildren: 0.1 } }
  }}
>
  {items.map((item, i) => (
    <motion.div
      key={i}
      variants={{
        hidden: { opacity: 0, y: 30 },
        visible: { opacity: 1, y: 0 }
      }}
    >
      {item}
    </motion.div>
  ))}
</motion.div>

// Hover scale
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={{ type: "spring", stiffness: 400, damping: 17 }}
>
  Click Me
</motion.button>
```

## Spatial Composition

Break the grid. Create visual interest through unexpected layouts.

### Asymmetric Layouts

```css
/* Two-column asymmetric */
.grid-asymmetric {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 60px;
}

/* Broken grid with overlap */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 20px;
}

.feature-1 { grid-column: 1 / 7; grid-row: 1; }
.feature-2 { grid-column: 6 / 13; grid-row: 1; z-index: 2; }
.feature-3 { grid-column: 1 / 8; grid-row: 2; margin-top: -40px; }
```

### Diagonal Flow

```css
/* Diagonal section transition */
.section-diagonal {
  clip-path: polygon(0 0, 100% 10%, 100% 100%, 0 90%);
  margin-top: -10vh;
}

/* Diagonal text layout */
.hero-title {
  transform: rotate(-5deg);
  transform-origin: left center;
}
```

### Generous Negative Space

```css
/* GOOD - Breathing room */
.hero {
  padding: 15vh 10vw;
  min-height: 100vh;
}

.section {
  padding: 120px 60px;
}

/* BAD - Cramped */
.hero {
  padding: 40px 20px;
}
```

## Backgrounds & Visual Details

Create atmosphere, not just flat colors.

### Gradient Meshes

```css
.gradient-mesh {
  background: 
    radial-gradient(circle at 20% 30%, rgba(255, 107, 53, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(98, 0, 234, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(52, 211, 153, 0.2) 0%, transparent 50%),
    linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
}
```

### Noise Texture

```css
.noise-texture {
  position: relative;
}

.noise-texture::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.05'/%3E%3C/svg%3E");
  pointer-events: none;
}
```

### Geometric Patterns

```css
.geometric-bg {
  background-image: 
    linear-gradient(30deg, transparent 40%, rgba(255, 255, 255, 0.03) 40%, rgba(255, 255, 255, 0.03) 60%, transparent 60%),
    linear-gradient(60deg, transparent 40%, rgba(255, 255, 255, 0.03) 40%, rgba(255, 255, 255, 0.03) 60%, transparent 60%);
  background-size: 80px 140px;
}
```

### Glassmorphism

```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px) saturate(180%);
  -webkit-backdrop-filter: blur(10px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
```

### Dramatic Shadows

```css
/* Layered shadow for depth */
.card-elevated {
  box-shadow:
    0 2px 4px rgba(0, 0, 0, 0.05),
    0 8px 16px rgba(0, 0, 0, 0.1),
    0 16px 32px rgba(0, 0, 0, 0.1),
    0 32px 64px rgba(0, 0, 0, 0.1);
}

/* Colored shadow matching element */
.button-primary {
  background: #ff6b35;
  box-shadow: 0 10px 40px rgba(255, 107, 53, 0.4);
}
```

## Production-Grade Implementation

### Code Quality Standards

**Structure:**
- Semantic HTML5 elements
- BEM or utility-class methodology
- CSS custom properties for theming
- Mobile-first responsive design
- Accessibility attributes (ARIA, alt text, labels)

**Performance:**
- Optimize images (WebP, lazy loading)
- Minimize JavaScript for interactions
- Use CSS transforms for animations
- Implement proper loading states
- Consider reduced motion preferences

**Accessibility:**
```css
/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Sufficient color contrast */
/* Check: https://webaim.org/resources/contrastchecker/ */
```

### Responsive Design Patterns

```css
/* Mobile-first approach */
.container {
  padding: 20px;
}

@media (min-width: 768px) {
  .container {
    padding: 40px;
  }
}

@media (min-width: 1200px) {
  .container {
    padding: 60px;
  }
}

/* Fluid typography */
.title {
  font-size: clamp(32px, 5vw, 80px);
  line-height: 1.1;
}
```

## Implementation Workflow

When user provides a screenshot or requests design:

### Step 1: Analyze (If screenshot provided)

Extract:
- Current aesthetic (generic, minimal, bold?)
- Color palette
- Typography choices
- Layout structure
- Interactive elements
- Problems/weaknesses

### Step 2: Propose Direction

Suggest 2-3 bold directions based on context:

```
"I see three directions for this e-commerce homepage:

1. **Editorial Luxury** - Bold serif typography, asymmetric grid, dramatic product photography, minimal color (black/white/gold)

2. **Neo-Brutalism** - Thick borders, shadow extrusion, bold sans-serif, high contrast, interactive 3D effects

3. **Soft Glassmorphism** - Frosted glass cards, gentle gradients, rounded corners, ambient light effects

Which aesthetic resonates with your brand?"
```

### Step 3: Implement with Precision

Create production-ready code that:
- Fully realizes the chosen aesthetic
- Includes all necessary HTML/CSS/JS
- Works responsively
- Has smooth animations
- Follows accessibility standards
- Can be copied and used immediately

### Step 4: Explain Decisions

After code, briefly explain:
- Why this typography pairing
- Color psychology choices
- Animation strategy
- Layout innovations
- How it achieves memorability

## Common Scenarios

### Landing Page
- Hero: Bold typography + striking visual
- Features: Asymmetric grid with icons
- Testimonials: Editorial card layout
- CTA: High-contrast, animated button

### Dashboard
- Sidebar: Clean navigation with icons
- Cards: Data visualization with shadows
- Charts: Custom styled (not default)
- Interactions: Smooth transitions

### Portfolio
- Hero: Large typography + personal photo
- Projects: Grid with hover reveals
- About: Two-column asymmetric
- Contact: Simple form with style

### E-commerce
- Product Grid: Hover zoom effects
- Product Page: Large images + clean details
- Cart: Glassmorphic overlay
- Checkout: Step progress indicator

## Critical Reminders

1. **Never converge** on the same aesthetic twice
2. **Avoid generic** fonts (Inter, Roboto, Arial, Space Grotesk)
3. **One memorable thing** - every design needs a standout feature
4. **Match complexity to vision** - maximalist = elaborate code, minimalist = precise restraint
5. **Bold choices** - commit fully to the aesthetic direction
6. **Context matters** - design for the actual use case, not generic templates
7. **Production-ready** - code should work, not just look pretty
8. **Accessibility** - beautiful AND usable by everyone

## Example Transformations

**Generic → Neo-Brutalist:**
- Add thick black borders (3-5px)
- Use shadow extrusion (offset shadows)
- Bold sans-serif headings (Anton, Bebas Neue)
- High contrast color blocks
- Geometric button shapes

**Generic → Editorial:**
- Large serif display font (Playfair Display)
- Asymmetric two-column grid
- Generous whitespace
- Black/white with one accent color
- Large, impactful images

**Generic → Glassmorphism:**
- Semi-transparent cards with backdrop-filter
- Soft gradients in background
- Rounded corners (20-30px)
- Subtle shadows
- Light, airy spacing

Remember: Claude is capable of extraordinary creative work. Every design should feel handcrafted for its specific context, with bold choices that make it unforgettable.
