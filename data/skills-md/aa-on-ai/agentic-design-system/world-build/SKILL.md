---
name: world-build
description: >
  Creative pack — use only when the user explicitly asks for immersion,
  atmosphere, narrative depth, or a page that should feel like a place. Skip for
  normal product UI, dashboards, forms, settings, and docs.
---

# World Build

## ⚠️ Creative Pack — NOT auto-apply

This skill is part of the creative pack. Do NOT apply it by default on every visual task.

**Use ONLY when explicitly triggered:**
- user says "world-build this" or "make this feel like a place"
- task is explicitly about immersive experience (portfolio, launch, game UI, interactive storytelling)
- user asks for atmosphere, narrative arc, or sensory design

**Do NOT use when:**
- no one asked for immersion — most UI tasks don't need this
- building product UI, dashboards, forms, settings, or tools
- content needs to be scannable and fast (docs, settings pages)
- MVP prototypes where speed matters more than atmosphere

If this skill wasn't explicitly requested, skip it. Use design-review instead.

## What This Is
The creative development playbook for building things that feel like *places*, not pages. Whimsical-design asks "does it have personality?" World-build provides the construction manual for **depth**.

---

## Phase 1: The World (BEFORE any code)

Every immersive build starts with a creative brief. Answer these three questions:

**1. What world does this live in?**
Not "what does it look like" but "where ARE we?" Examples:
- Killian Herzer: a detective's case file / surveillance system
- Clawbotomy: a behavioral forensics lab
- Context Window: a decaying AI consciousness
- Inflight: a mission control dashboard for creators

**2. What's the core metaphor?**
One metaphor that every UI element reinforces:
- Investigation → evidence, case files, classified stamps, redacted text
- Laboratory → specimens, test results, diagnostic readouts
- Space mission → coordinates, telemetry, signal strength
- Nature → growth, seasons, organic shapes, weathering

**3. What does the user FEEL when they arrive?**
Name one emotion. Not "impressed" — that's a reaction. An emotion:
- Intrigue (I want to explore this)
- Wonder (this is beautiful and alive)
- Tension (something is happening here)
- Warmth (I feel welcomed into someone's world)

Write these three answers down. Share with the user. Get alignment. THEN build.

---

## Phase 2: The Atmosphere System

Every world-build site needs these layers. They're what separate "a page with nice CSS" from "a place."

### Layer 1: Background Texture
The canvas is never blank white or flat black.

The noise technique below is the same recipe as whimsical-design §4 "Background Atmosphere"
(canonical copy lives there — keep the SVG data-URI in sync). This is the fixed full-screen
overlay variant for immersive pages.

```css
/* Noise overlay — subtle grain that makes everything feel tactile */
.noise-overlay {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.03;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
}

/* Ambient glow — soft colored light that sets mood */
.ambient-glow {
  position: fixed;
  width: 60vw;
  height: 60vh;
  border-radius: 50%;
  opacity: 0.05;
  filter: blur(120px);
  mix-blend-mode: normal;
  pointer-events: none;
  will-change: transform;
  animation: drift 20s ease-in-out infinite alternate;
}

/* Grid background — subtle structure */
.grid-bg {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
}
```

### Layer 2: Corner Elements (HUD)
Persistent UI that reinforces the world. Small, monospace, low opacity.

```
┌─ TOP LEFT                          TOP RIGHT ─┐
│  Status indicator                  Timestamp    │
│  Signal/connection                 Language      │
│                                                  │
│                                                  │
│                                                  │
│  BOTTOM LEFT                    BOTTOM RIGHT     │
│  Live indicator                 System status    │
└──────────────────────────────────────────────────┘
```

These should be thematic:
- Detective world: "Camera 04 recording", "Signal strong", "Analyzer active"
- Lab world: "Sample 0042", "Temperature 21.3 °C", "Protocol active"
- Space world: "Latitude 34.0195 N", "Orbit stable", "Comms open"

### Layer 3: Custom Cursor
Replace the default cursor. Even a simple dot + trailing ring transforms the feel.

```css
.cursor-main {
  width: 12px;
  height: 12px;
  border: 1.5px solid var(--accent);
  border-radius: 50%;
  position: fixed;
  pointer-events: none;
  z-index: 10000;
  transition: transform 0.15s ease;
}
/* Scale up on interactive elements, show text labels on hover */
```

### Layer 4: Scan Lines / Atmospheric FX
Pick ONE signature effect. Don't stack them all:
- Scan line (horizontal bar sweeping slowly)
- Vignette (darkened edges)
- CRT flicker (very subtle, for retro worlds)
- Floating particles (for organic/nature worlds)
- Spotlight/flashlight mask (for investigation worlds)

---

## Phase 3: Typography as World-Building

**Rule: Minimum 2 font families. Always.**

### The Formula
- **Display/Headline:** Serif or statement font (Playfair Display, EB Garamond, Fraunces, Space Grotesk)
- **Body:** Clean sans (Inter, Rethink Sans, Plus Jakarta Sans)
- **System/Data:** Monospace (JetBrains Mono, IBM Plex Mono, Space Mono)

The contrast between headline and system text creates visual tension — serif warmth vs mono coldness. That tension IS the design.

### Scale
Headlines should be dramatically large. `clamp(2.5rem, 5vw, 4rem)` minimum for hero text. Body stays readable. The gap between them is the hierarchy.

---

## Phase 4: Animation Choreography

Everything enters. Nothing just appears.

### GSAP ScrollTrigger Setup
```js
// Every section reveals on scroll
gsap.utils.toArray('.reveal-section').forEach(section => {
  gsap.from(section, {
    y: 60,
    opacity: 0,
    duration: 1,
    ease: 'power3.out',
    scrollTrigger: {
      trigger: section,
      start: 'top 80%',
      toggleActions: 'play none none none'
    }
  });
});

// Staggered children (cards, list items)
gsap.from('.stagger-item', {
  y: 40,
  opacity: 0,
  duration: 0.8,
  stagger: 0.1,
  ease: 'power2.out',
  scrollTrigger: { trigger: '.stagger-container', start: 'top 75%' }
});
```

### Timing Rules
- **Entrance:** 0.8-1.2s with `power3.out` (fast start, gentle land)
- **Hover:** 0.2-0.3s with `power2.out`
- **Page transition:** 0.4-0.6s
- **Stagger delay:** 0.08-0.12s between items
- **Never use linear easing.** Everything has organic acceleration.

### Parallax
Background elements move slower than foreground. Even 10% difference creates depth.

```js
gsap.to('.parallax-bg', {
  yPercent: -20,
  ease: 'none',
  scrollTrigger: {
    trigger: '.parallax-section',
    start: 'top bottom',
    end: 'bottom top',
    scrub: true
  }
});
```

---

## Phase 5: The Loading Sequence

The first 2-3 seconds set the entire mood. Never skip this.

### Minimum Viable Loader
1. Full-screen curtain in the world's dominant color
2. One animated element (progress bar, counter, spinner — thematic)
3. One line of thematic text ("Initializing...", "Loading evidence...", "Entering lab...")
4. Curtain splits/fades to reveal the site

### Advanced Loader (for portfolio/showcase sites)
- Terminal text typing effect
- Progress counter (00% → 100%)
- Thematic animation (radar sweep, heartbeat line, particle formation)
- Sound cue on completion (optional, powerful if done right)

---

## Phase 6: The Project Showcase Pattern

If the site shows work/projects/case studies, use the evidence board pattern:

1. **Horizontal slider** with large preview cards (not a grid)
2. **Click to expand** into full-screen viewer/terminal
3. **Metadata sidebar** with structured data (year, stack, role)
4. **Gallery** within the viewer
5. **Navigation** between projects without closing

This pattern works because it's interactive (not just scrolling), it treats each project as important (full-screen), and it lets the user control the pace.

---

## Pre-Flight Checklist

Before presenting a world-build to the user:

### World Check
- [ ] Creative brief exists (world, metaphor, emotion)
- [ ] Every UI element reinforces the world — nothing breaks the fiction
- [ ] The world is consistent — you wouldn't see a detective badge in a space station

### Atmosphere Check
- [ ] Background texture layer (noise, grain, or gradient)
- [ ] At least 2 ambient/decorative layers (glow, grid, particles, corners)
- [ ] Custom cursor or cursor modification on hover
- [ ] One signature atmospheric effect

### Typography Check
- [ ] 2+ font families loaded and used intentionally
- [ ] Serif/sans or display/mono contrast visible
- [ ] Headlines are dramatically sized
- [ ] Monospace used for data/system elements

### Animation Check
- [ ] GSAP (or equivalent) loaded
- [ ] Sections reveal on scroll, not on page load
- [ ] Hover states on all interactive elements
- [ ] Staggered animations on repeated elements
- [ ] No element just "appears" — everything enters

### Loading Check
- [ ] Loading sequence exists
- [ ] Loading sequence is thematic (not a generic spinner)
- [ ] Site content is hidden until loader completes

### Screenshot Test
- [ ] Take a screenshot. Cover the text. Does it still feel like a place?
- [ ] Compare to reference (Killian Herzer, Inflight, etc.)
- [ ] Would someone screenshot this and send to a friend?

---

## Reference Sites (study the source)
- **killianherzer.com** — investigation/surveillance world, GSAP + Three.js, noise + grid + corners + custom cursor, full loader sequence
- **inflight.co** — mission control for creators, data viz, interactive SVG
- **3d.killianherzer.com** — Three.js immersive 3D version of portfolio
- **poolsuite.net** — retro-futurist world, nostalgia as design language
- **lusion.co** — WebGL showcase, creative development studio
- **void.st** — minimal but atmospheric, particle systems

## Updating This Skill
After builds where the user gives feedback on atmosphere, depth, or immersion:
- What created the right feeling → add to recipes
- What fell flat → add to anti-patterns
- New reference sites → add to the list
- Code patterns that worked well → add as snippets
