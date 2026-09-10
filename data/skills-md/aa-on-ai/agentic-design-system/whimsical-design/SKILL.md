---
name: whimsical-design
description: >
  Creative pack — use only when a UI task explicitly needs personality, delight,
  brand expression, marketing/editorial energy, or a non-default visual direction.
  Skip for utility UI unless the default-safe output is the problem.
---

# Whimsical Design Skill

## ⚠️ Creative Pack — NOT auto-apply

This skill is part of the creative pack. Do NOT apply it by default on every visual task.

**Use ONLY when at least one is true:**
- user explicitly asks for personality, delight, whimsy, or brand expression
- task is marketing, landing page, portfolio, launch, or editorial
- the default/safe output is clearly the problem (everything looks the same)
- multiple creative directions are being explored on purpose

**Do NOT use when:**
- building utility UI, admin tools, settings pages, or internal tools
- the product already has a clear design language you should match
- the default aesthetic is already appropriate for the product category
- task is primarily about structure, states, or production hardening

If in doubt, skip this skill. Core skills (design-review, ux-baseline-check, ui-polish-pass) are always safe. This one requires judgment about whether "push past safe" is actually what the product needs.

## When It Applies
Design-review catches quality problems. This skill pushes toward delight. Use alongside `<skills-root>/design-review/SKILL.md` when the triggers above are met.

## The Bar
Would someone screenshot this and send it to a friend? Would it make them smile? If no, push further.

## Core Principles

### 1. Whimsy Over Sterile
Default away from corporate SaaS. Toward warmth, personality, surprise. Think: the feeling of opening a Playdate box, or the first time you saw a Teenage Engineering product page.
- Pixel art, hand-drawn textures, playful illustrations
- Warm color palettes over cold neutral grays
- Personality in empty states, loading screens, error messages
- Small details that reward people who look closely

### 2. Juice
Everything should feel alive. Static interfaces are dead interfaces.
- Micro-interactions on hover, click, drag
- Subtle spring animations on state changes
- Parallax, bob, breathe — things that move even when idle
- Sound design where appropriate (click, whoosh, chirp)
- The difference between "functional" and "delightful" is 50ms of easing

**Concrete recipes:**
- Hover on cards: `scale(1.02)` + subtle shadow increase + 150ms ease-out
- Button press: `scale(0.97)` for 100ms, then back. feels tactile.
- Page entrance: stagger children with 50ms delay each, fade+translateY(8px), 300ms ease-out
- Status indicators: pulse animation on "live" items (opacity 1→0.4→1, 2s infinite)
- Charts: animate data points in on mount, left-to-right, 400ms ease-out with 30ms stagger
- Hover on table rows: background-color transition 150ms + slight translateX(2px) to feel "picked up"
- Toggle switches: spring physics (slight overshoot on slide, ~200ms)
- Empty states: gentle floating animation on the illustration (translateY ±4px, 3s ease-in-out infinite)

### 3. Bold Aesthetic Commitment
Before writing a single line of code, commit to a specific aesthetic direction. not "clean and modern" — that's a non-decision. pick an extreme and execute it with intention:

- brutally minimal (nothing that doesn't earn its place)
- maximalist chaos (dense, layered, overwhelming in the best way)
- retro-futuristic (old tech aesthetics, modern capability)
- organic/natural (textures, warmth, imperfection)
- luxury/refined (thin weights, generous space, precious materials)
- playful/toy-like (rounded, bouncy, colorful, tactile)
- editorial/magazine (type-forward, dramatic scale, reading rhythm)
- brutalist/raw (exposed structure, no decoration, confrontational)
- industrial/utilitarian (functional, dense, no-nonsense)

the key is intentionality, not intensity. bold maximalism and refined minimalism both work. what doesn't work is the timid middle — the agent default of "a little of everything."

write one sentence describing your aesthetic direction before building. if you can't articulate it, you haven't committed.

### 4. Background Atmosphere
agents default to flat solid color backgrounds. that's the single biggest "AI built this" tell after card grids. backgrounds create mood before any content loads.

techniques:
- **noise/grain texture** — `background-image: url("data:image/svg+xml,...")` with a subtle noise pattern at 3-5% opacity. makes flat colors feel tactile.
- **gradient mesh** — 2-3 radial gradients layered at low opacity. creates depth without being gaudy.
- **subtle pattern** — dots, lines, or geometric shapes at 2-4% opacity. adds texture without distraction.
- **layered transparencies** — overlapping semi-transparent shapes in the background. creates depth and atmosphere.

```css
/* noise texture overlay — canonical copy of this recipe; world-build Layer 1 reuses the same
   SVG data-URI as a fixed full-screen variant. If you change it here, sync it there. */
.textured {
  position: relative;
}
.textured::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 1;
}

/* gradient mesh */
.atmospheric {
  background: 
    radial-gradient(ellipse at 20% 50%, rgba(232, 114, 58, 0.08) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(45, 106, 79, 0.06) 0%, transparent 50%),
    #FAFAF8;
}
```

don't: use these on every surface. use them on the page background and hero sections. inner components should be clean.

### 5. Craft Signals
The opposite of "AI generated this." Every surface should feel touched by a human.
- Grain textures, noise overlays, subtle paper feel
- Intentional imperfection — slightly uneven, hand-placed, organic
- Serif accents mixed with clean sans (not all one or the other)
- Asymmetric layouts that feel composed, not random
- Custom illustrations over stock icons where possible
- SVG elements that respond to cursor or scroll

### 6. Color With Feeling
Color should create mood, not just differentiate elements.
- **Dominant + accent, not evenly distributed** — one dominant color owns the page. one sharp accent draws attention to what matters. a timid, evenly-spread palette is an agent default. commit: what's the ONE color someone remembers?
- Studio Ghibli palettes: warm earth tones, saturated sky blues, forest greens
- Pantone-chip energy: specific, intentional, named
- Avoid: gray-on-white corporate void, neon-on-dark "developer tool"
- Dark modes should feel cozy (deep indigos, warm blacks), not cold

**Concrete recipes:**
- Warm light mode: background `#FAFAF8` (not pure white), text `#1A1A1A` (not pure black), accent `#E8723A` (warm orange) or `#2D6A4F` (forest green)
- Cozy dark mode: background `#1C1917` (warm black, not zinc-900), text `#E7E5E4`, accent `#F59E0B` (amber) or `#818CF8` (soft indigo)
- Data viz palette (warm): `#E8723A`, `#2D6A4F`, `#D4A373`, `#588157`, `#BC6C25` — earthy, distinct, accessible
- Data viz palette (cool): `#3B82F6`, `#8B5CF6`, `#06B6D4`, `#6366F1`, `#14B8A6` — techy but not cold
- Status colors: success `#16A34A` (not neon green), warning `#D97706` (not yellow), error `#DC2626` (not pink), info `#2563EB`
- Gradient (subtle, not gaudy): `from-amber-50 to-orange-50` for warm sections, `from-slate-50 to-blue-50` for cool sections — backgrounds only, never on text

### 7. Typography as Character
Type carries personality before anyone reads a word.
- Mix weights dramatically (thin headlines + chunky body, or vice versa)
- Consider display faces for headers — not just system fonts
- Letterspacing and line-height are design decisions, not defaults
- Monospace for data/code, but make it feel intentional (not "I forgot to style this")

## References (study these)

**Product / Physical**
- Teenage Engineering — products as objects of desire, every surface designed
- Panic / Playdate — joy in every interaction, surprise and delight as core values
- Nothing Phone — glyphs, transparency, making tech feel human

**Digital**
- Perplexity marketing pages — confident whitespace, editorial feel, illustrations
- Linear changelog — density with craft, every detail considered
- Vercel ship pages — motion, drama, typographic confidence
- Raycast — command palette as art form
- Arc Browser — sidebar as expression

**Visual Language**
- Old Apple ads (Think Different era) — simplicity with soul
- Studio Ghibli color grading — warm, lived-in, natural light
- Indie game UIs (Celeste, Hollow Knight, Slay the Spire) — personality in every pixel
- Poolsuite / Poolsuite FM — retro-futurism, nostalgia as design language

## Anti-Patterns (NEVER DO THESE)
- Glassmorphism for its own sake (blur ≠ design)
- Neon gradients as a substitute for personality
- Generic card grids with drop shadows
- Bootstrap energy (you know it when you see it)
- "Clean and modern" as the entire design brief
- Stock illustrations from undraw/humaaans (everyone uses these)
- Gray-200 backgrounds with gray-300 borders everywhere
- Tailwind defaults without customization
- Cookie-cutter hero sections (headline + subhead + CTA + mockup)
- Animations that don't serve meaning (spinning logos, floating shapes)

## Pre-Flight Checklist (run alongside design-review)

### Whimsy Check
- [ ] **The smile test** — does this make you smile? Would you show someone?
- [ ] **Personality audit** — remove one element. Does it still feel like "us"? If yes, you haven't gone far enough.
- [ ] **Empty state check** — what happens when there's no data? Is it delightful or depressing?
- [ ] **Error state check** — is the error message human? Funny? At least warm?
- [ ] **Hover state check** — does hovering over things feel rewarding?

### Craft Check
- [ ] **Texture** — is there grain, noise, or tactile quality? Or is it flat vectors on white?
- [ ] **Typography** — are font choices intentional? Is there contrast in scale/weight?
- [ ] **Color** — does the palette create a mood? Could you name the vibe in one word?
- [ ] **Motion** — do transitions have easing? Do elements enter and exit with intention?
- [ ] **Detail** — is there at least one "easter egg" level detail someone might notice on second look?

### Kill Switch
- [ ] **Not whimsy for whimsy's sake** — does the personality serve the product or distract from it?
- [ ] **Readable** — is body text still legible? Are CTAs still clear?
- [ ] **Accessible** — does color contrast pass WCAG? Do animations respect prefers-reduced-motion?
- [ ] **Performance** — are animations GPU-accelerated? Are textures optimized?

## Updating This Skill
After design reviews where the user gives feedback on visual personality, tone, or craft:
- What delighted the user → add to Principles or References
- What felt flat → add to Anti-Patterns
- Specific decisions (texture style, color choice, animation timing) → `DESIGN.md` or the project decision log

The goal: every build should feel more "us" than the last.
