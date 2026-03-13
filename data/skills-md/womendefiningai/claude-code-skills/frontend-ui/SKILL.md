---
name: frontend-ui
description: Create aesthetically pleasing, visually distinctive frontend UIs using research-backed prompting strategies from Anthropic's frontend aesthetics cookbook
---

# Frontend UI Design

Create visually distinctive, aesthetically pleasing frontend interfaces that avoid generic "AI slop" patterns.

## When to Use

Use this skill when:
- User requests frontend UI creation (HTML, CSS, JavaScript, or React)
- User asks to build a webpage, landing page, or web interface
- User wants to create visual components or layouts
- User mentions design, aesthetics, or "make it look good"
- User asks for dashboard, portfolio, or application UI

## Core Principle

**CRITICAL**: Without explicit aesthetic guidance, Claude defaults to generic, conservative designs (white backgrounds, purple accents, Inter/Roboto fonts, predictable layouts). This skill provides research-backed strategies to create distinctive, visually interesting interfaces.

## The Four Design Dimensions

Always address these four areas when creating frontend UIs:

### 1. Typography

**AVOID these overused fonts**:
- Inter, Roboto, Arial, Helvetica, system fonts

**USE distinctive alternatives**:
- **Monospace**: JetBrains Mono, Fira Code, IBM Plex Mono, Space Mono
- **Display/Geometric**: Space Grotesk, Clash Display, Epilogue, Syne
- **Serif**: Playfair Display, Crimson Pro, Libre Baskerville, Merriweather
- **Modern Sans**: Outfit, Manrope, General Sans, Satoshi

**Typography Best Practices**:
- Use **high contrast pairings**: display + monospace, serif + geometric sans
- Employ **extreme weight variations**: 100/200 vs 800/900 (not just 400 vs 600)
- Create **dramatic size jumps**: 3x+ differences, not 1.5x
- Load fonts from Google Fonts and state choices explicitly before coding

**Example pairing**:
```
Heading: Clash Display (800 weight, 4rem)
Body: JetBrains Mono (300 weight, 0.9rem)
Accent: Space Grotesk (700 weight, 1.2rem)
```

### 2. Color & Theme

**AVOID these clichéd schemes**:
- Purple gradients on white backgrounds
- Generic blue-and-white corporate palettes
- Timid, evenly-distributed colors
- Predictable light mode with subtle accents

**USE cohesive aesthetics with CSS variables**:
- **Commit to a theme**: Cyberpunk, Solarpunk, Brutalist, Neo-Tokyo, Retro-Future, Terminal, Vaporwave
- **Dominant colors with sharp accents**: Not all colors equally represented
- **Draw from IDE themes**: Dracula, Nord, Gruvbox, Tokyo Night, Monokai
- **Cultural aesthetics**: Japanese minimalism, Swiss design, Memphis style

**Color Strategy**:
1. Define CSS custom properties for consistency
2. Choose 2-3 dominant colors and 1-2 sharp accents
3. Consider dark themes as often as light themes
4. Use gradients sparingly but boldly when used

**Example theme (Cyberpunk)**:
```css
--bg-primary: #0a0e27;
--bg-secondary: #16213e;
--accent-neon: #00ff9f;
--accent-pink: #ff006e;
--text-primary: #e0e0e0;
--text-muted: #8892b0;
```

### 3. Motion

**Implementation approach**:
- **For HTML**: CSS-only animations
- **For React**: Use Framer Motion library when available
- Focus on **high-impact moments** over scattered micro-interactions
- One well-orchestrated page load with staggered reveals > many small animations

**Motion Best Practices**:
- Use `animation-delay` for staggered effects
- Animate on mount/page load for impact
- Keep animations smooth (ease-out, ease-in-out)
- Duration: 0.4s-0.8s for most transitions

**Example staggered reveal**:
```css
.fade-in {
  animation: fadeIn 0.6s ease-out forwards;
  opacity: 0;
}

.fade-in:nth-child(1) { animation-delay: 0.1s; }
.fade-in:nth-child(2) { animation-delay: 0.2s; }
.fade-in:nth-child(3) { animation-delay: 0.3s; }

@keyframes fadeIn {
  to { opacity: 1; transform: translateY(0); }
  from { opacity: 0; transform: translateY(20px); }
}
```

### 4. Backgrounds

**AVOID**: Solid white or solid single-color backgrounds

**USE atmosphere and depth**:
- **Layered CSS gradients**: Multiple gradients with varying opacity
- **Geometric patterns**: Grid lines, dots, diagonal stripes
- **Contextual effects**: Noise texture, grain, subtle animations
- **Thematic elements**: Match overall aesthetic (circuits for tech, organic shapes for nature)

**Background Techniques**:

```css
/* Layered gradients */
background:
  radial-gradient(circle at 20% 50%, rgba(120, 0, 255, 0.3) 0%, transparent 50%),
  radial-gradient(circle at 80% 80%, rgba(0, 255, 200, 0.2) 0%, transparent 50%),
  linear-gradient(135deg, #0a0e27 0%, #16213e 100%);

/* Grid pattern */
background-image:
  linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
  linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
background-size: 50px 50px;

/* Dots pattern */
background-image: radial-gradient(circle, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
background-size: 20px 20px;
```

## Critical Warnings: Avoid "AI Slop"

**Think outside the box!** It is CRITICAL that you:

- ✅ **Vary between light and dark themes** (don't default to light)
- ✅ **Use different fonts each time** (avoid convergence on Space Grotesk)
- ✅ **Try different aesthetics** (cyberpunk, brutalist, retro, minimalist)
- ❌ **Never use**: Inter, Roboto, Arial as primary fonts
- ❌ **Never default to**: White background with purple accents
- ❌ **Avoid**: Cookie-cutter layouts, predictable component patterns
- ❌ **Don't create**: Generic designs lacking context-specific character

## Workflow

When creating frontend UIs, follow this process:

### Step 1: Understand Context
Ask clarifying questions about:
- Purpose of the interface
- Target audience
- Desired mood/feeling
- Any specific aesthetic preferences

### Step 2: Choose Aesthetic Direction
Pick a cohesive theme based on context:
- **Tech/Dev**: Terminal, Cyberpunk, Hacker aesthetic
- **Creative**: Vaporwave, Memphis, Brutalist
- **Professional**: Swiss design, Minimalist, Editorial
- **Organic**: Solarpunk, Nature-inspired, Warm tones

### Step 3: State Design Decisions Explicitly
Before writing code, declare:
```
Theme: [chosen aesthetic]
Fonts: [heading font], [body font], [accent font]
Colors: [dominant colors and accents]
Motion: [key animations planned]
Background: [approach chosen]
```

### Step 4: Implement with Best Practices

**Technical Requirements**:
- Use vanilla HTML, CSS, JavaScript OR React as requested
- Include Tailwind CSS if appropriate
- Inline all CSS and JavaScript for single-file deliverables
- Load fonts from Google Fonts
- Use CSS custom properties for theming
- Ensure responsive design (mobile-first approach)

### Step 5: Create High-Impact Moments
- Orchestrate page load animations
- Use staggered reveals for content
- Add hover states that feel responsive
- Consider scroll-triggered animations sparingly

## Examples

### Example 1: Developer Portfolio (Dark Theme)

**Stated Design**:
- Theme: Terminal/Hacker aesthetic with green accents
- Fonts: JetBrains Mono (all text), weight variations for hierarchy
- Colors: Dark bg (#0d1117), green accent (#39ff14), muted gray text
- Motion: Typing animation on hero text, staggered fade-in on projects
- Background: Subtle grid pattern with scanline effect

**Key Features**:
- Monospace typography throughout
- CRT monitor aesthetic with scanlines
- Green phosphor glow effects
- Terminal-style navigation

### Example 2: Creative Agency Landing (Light Theme)

**Stated Design**:
- Theme: Swiss Brutalist with bold typography
- Fonts: Clash Display (headings 900 weight), Space Grotesk (body 300 weight)
- Colors: Off-white (#f5f5f0), black, one sharp red accent (#ff0000)
- Motion: Bold elements sliding in from edges on load
- Background: Off-white with subtle noise texture

**Key Features**:
- Extreme type sizing (hero at 6rem+)
- Asymmetric grid layout
- Sharp geometric shapes as accents
- High contrast black/white with red sparingly

### Example 3: App Dashboard (Dark Theme)

**Stated Design**:
- Theme: Neo-Tokyo night with pink/cyan accents
- Fonts: Outfit (headings 700), IBM Plex Mono (data/numbers)
- Colors: Dark navy (#0a1128), pink (#ff006e), cyan (#00f5ff)
- Motion: Smooth transitions on card hovers, data count-up animations
- Background: Dark with subtle radial gradient and grid

**Key Features**:
- Neon-style accents on interactive elements
- Glassmorphism cards with backdrop blur
- Monospace for all numerical data
- Glowing borders on focus states

## Isolated Dimension Prompting

For targeted control, you can isolate single dimensions:

### Typography-Only Adjustment
"Keeping all other design elements the same, update only the typography using Crimson Pro for headings and Fira Code for body text with extreme weight contrast."

### Theme-Only Adjustment
"Lock the aesthetic to a Solarpunk theme: warm earth tones, organic shapes, nature-inspired patterns, green/gold accents, optimistic futuristic feel."

### Motion-Only Enhancement
"Add a well-orchestrated page load sequence: hero fades in first (0.5s), then navigation staggers in (0.2s delays), then content cards reveal bottom-to-top."

## Font Rotation Strategy

To avoid convergence on the same fonts, rotate through these distinctive combinations:

**Set 1 - Terminal Aesthetic**:
- JetBrains Mono + IBM Plex Mono

**Set 2 - Modern Editorial**:
- Playfair Display + Space Grotesk

**Set 3 - Geometric Bold**:
- Clash Display + Manrope

**Set 4 - Retro Future**:
- Space Mono + Outfit

**Set 5 - Elegant Tech**:
- Crimson Pro + Fira Code

**Set 6 - Neo Brutalist**:
- Syne + General Sans

## Quality Checklist

Before delivering, verify:

- [ ] Fonts are NOT Inter, Roboto, Arial, or system fonts
- [ ] Color scheme is NOT white background with purple accents
- [ ] Typography has extreme weight variations (100-200 vs 800-900)
- [ ] Size jumps are 3x+ for hierarchical contrast
- [ ] Background has depth (gradients, patterns, or effects)
- [ ] Motion is orchestrated (staggered, purposeful)
- [ ] Theme is cohesive and context-appropriate
- [ ] CSS custom properties are used for consistency
- [ ] Design avoids generic, cookie-cutter patterns
- [ ] Aesthetic is distinctive and memorable

## Notes

- **Source**: Based on Anthropic's "Prompting for Frontend Aesthetics" research
- **Variety is critical**: Consciously vary themes, fonts, and approaches across different projects
- **Context matters**: Match aesthetic to purpose (playful vs professional, technical vs creative)
- **Bold choices**: Better to be distinctive than safe and generic
- **Performance**: Keep animations performant (CSS transforms, not layout changes)
- **Accessibility**: Ensure sufficient contrast ratios and readable font sizes

## References

For deeper exploration, consult REFERENCE.md for:
- Extended font pairing library
- Detailed color palette examples
- Animation cookbook
- Background pattern recipes
- Theme architecture examples
