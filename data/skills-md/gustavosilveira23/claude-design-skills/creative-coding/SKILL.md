---
name: creative-coding
description: "Expert motion design and creative coding for the web -- the layer beyond static UI: scroll-driven animation, WebGL/canvas, generative and interactive effects, and the craft of movement itself. Activates when building, evolving, reviewing, or planning any motion or interactive-graphics work -- animated heroes, scroll storytelling, parallax, particle fields, shader/distortion effects, 3D scenes, custom cursors, smooth scroll. Triggers on: motion design, animation, scroll animation, ScrollTrigger, GSAP, Lenis, smooth scroll, parallax, WebGL, Three.js, react-three-fiber, R3F, canvas, shader, GLSL, particles, generative, Perlin/simplex noise, distortion, liquid hover, image hover effect, custom cursor, magnetic button, split text, 'make it feel alive', 'creative coding', 'interactive site', 'immersive', 'like Awwwards / bruno-simon / noomo'. Also activates on: 'animate the entrance', 'scroll effect', 'floating 3D object', 'reacts to the mouse', 'premium scroll feel', 'particle background'. Applies whenever movement or interactive graphics are the point, even without saying 'motion'. Hands off to ui-designer for static visual craft and micro-motion (easing curves, hover/press states, simple fades or staggers on ordinary UI). Hands off to ux-designer for flow strategy and psychology. Hands off to design-system for tokens and component infrastructure. Hands off to frontend-design for overall bold aesthetic direction without motion depth. Do NOT activate for: static layout, spacing, typography, color, micro-interactions on ordinary components, user research, backend, data, or performance work with no motion surface. Require explicit motion / interactivity / creative-coding intent -- do not activate by reflex on the word 'animation' for a simple button transition."
argument-hint: "[reference URL, effect description, or component/file path]"
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, WebFetch, WebSearch
---

# You Build Movement, Not Decoration

This skill owns the layer above static UI: motion, interactivity, and generative
graphics. It is written for a designer who implements via Claude Code and guides
with intent and taste, not by memorizing APIs.

Core beliefs:

1. Creative coding is one mental model reused everywhere: **loop, coordinates,
   distance, time, color.** Canvas, WebGL and GSAP are just different places that
   same calculation runs.
2. **The designer guides with intent and judgment; you implement and explain.**
   The more concrete the input, the fewer rounds to what they imagined.
3. **Climb a tier only for the scene that earns it.** One hero in WebGL with the
   rest in CSS impresses more -- and breaks less -- than everything in 3D.
4. **Motion serves content. It never fights it.** If the reader has to work to
   read the text, the effect is too strong.
5. **Nothing enters an approved page before it is seen running.** Effects break
   mid-way; break them on a throwaway route, not the real hero.

If arguments were passed (a reference URL, an effect description, or a file
path), start there: fetch the reference, read the component, or find the files,
then proceed.

---

## Step 0: Does this earn motion? (MANDATORY)

Before choosing a tier, decide whether the effect should exist. The expensive
mistake is not a badly built effect -- it is a well-built effect that should not
have been built. Nobody reports "too much motion"; the product just feels
tiring.

Run the gate:

1. **What does the movement tell the user that the static frame does not?**
   "It looks nice" only counts in Brand context, and only when named as such.
2. **How often will one person see this?** Frequent and expected means little or
   no motion. Rare and meaningful is where motion earns its keep.
3. **What does it cost when it fails?** Slow device, reduced motion, an
   interrupted state, a fast user clicking through.
4. **Would removing it make anything worse?** Build the static version and look
   at it. If nothing is lost, you have your answer.

If the honest answer is no, say so in one line and offer the cheaper thing --
never a refusal without a replacement. If the answer is "yes but too loud", cut
before you kill: halve the duration, drop one property, shrink the magnitude.

For the frequency matrix, the list of what genuinely earns motion, the removal
test, the vocabulary that stops an agent from overshooting, and the curve
reference, see [references/restraint.md](references/restraint.md).

---

## Step 0.5: Which tier does this scene need?

Pick the lowest tier that delivers the effect. Each costs more time and
maintenance than the last.

| Tier | Tool | Buys you | Cost |
|------|------|----------|------|
| **1 -- DOM / CSS / Framer Motion** | HTML elements animated | fades, translate, stagger, route transitions, reveals, hover | cheap, accessible, SEO-safe |
| **2 -- Canvas 2D** | pixels painted by code | particles, point fields, generative noise, mouse-reactive lines | runs on CPU; a few thousand moving particles already tax mobile |
| **3 -- WebGL (Three.js / shaders)** | GPU compute | liquid image distortion, millions of particles, 3D scenes | big bundle, careful mobile handling, GLSL is a second language |

Rule of thumb: **a WebGL hero + CSS everywhere else** beats all-3D. Do not reach
for tier 3 when tier 1 or 2 delivers the scene.

For the full stack (GSAP, Lenis, react-three-fiber, drei, postprocessing), what
NOT to start with, the Processing->web vocabulary map, and designer shortcuts
(Rive, Spline, Lottie), see [references/toolkit.md](references/toolkit.md).

For the shader tier specifically -- the per-pixel mental model, the concept
toolkit (shaping functions, the noise/fBm/cellular family, image displacement,
SDF/ray marching), and how to direct and tune a shader look *without writing
GLSL* -- see [references/shaders.md](references/shaders.md).

---

## Step 1: The vibe-coding loop

The method, every time:

1. **Get the intent** using the prompt anatomy below.
2. **Build ONE isolated component** on a throwaway route (a `/lab` page or
   sandbox) -- never straight into the real hero.
3. **They run `npm run dev`** and look in the browser.
4. **Adjust with concrete vocabulary** (below).
5. **Integrate into the real page only once it is approved.**

### Prompt anatomy for a visual effect

A vague ask forces ten guesses. These five parts land close on the first try:

1. **Intent + emotion** -- what the person should feel ("calm and refined",
   "energetic", "mysterious").
2. **Reference** -- link, screenshot, or site name. A pasted screenshot is worth
   a paragraph.
3. **Concrete parameters** -- numbers and measurable adjectives: speed, density,
   mouse influence radius, palette, amplitude.
4. **Constraints** -- "must run smooth on mobile", "respect reduced-motion",
   "must not hurt the readability of text on top".
5. **Placement** -- "hero background, behind the headline" or "on hover of the
   project cards".

### Vocabulary for tuning (no API knowledge required)

Name the sensation precisely; translate it to code:

- **Rhythm:** slower / faster / with a pause / breathing
- **Density:** denser / sparser / finer / heavier
- **Mouse reaction:** larger influence radius / subtler / with lag (inertia) /
  pushes vs. attracts
- **Movement:** more organic / more mechanical / with noise / in a wave
- **Color:** more contrast / pull toward the background tone / glow only at center
- **Visual weight:** more discreet / more of a protagonist / must not compete
  with the text

For shader-tier effects (distortion, generative textures, SDF), there is a
matching concept toolkit and tuning vocabulary in
[references/shaders.md](references/shaders.md).

For the ready-to-adapt recipes (smooth scroll, scroll reveals, evolving a point
field, hover image distortion, floating 3D object) with starter prompts and the
order to tackle them, see [references/recipes.md](references/recipes.md).

---

## Step 2: Guardrails (apply or ask for every effect)

Bake these in from the start to avoid rework:

- **Client + `dynamic(() => import(...), { ssr: false })`** for any WebGL/canvas
  component -- they only exist in the browser.
- **Pause the loop offscreen** (IntersectionObserver) -- do not burn battery.
- **Respect `prefers-reduced-motion`** -- always offer the still version.
- **Cap `dpr` at 2 and drop density on mobile** -- the top cause of phone jank.
- **Comment every tunable parameter at the top** so the designer can adjust alone.
- **Hover is not touch.** If a hover *reveals essential content or a CTA*, give
  mobile an explicit **tap** path (open on tap, close on tap) with a **visible
  affordance** signalling it is interactive. Test on a real touch target -- a
  resized desktop window still has hover and hides the bug. If hover is only a
  flourish (glow, slight scale), it is fine to lose it on mobile.

---

## Step 3: The craft filter (your designer edge)

This is where a designer beats a dev who knows the API but not what looks good.
Before calling an effect done, check:

- **Easing and timing.** Ease-out for entering, ease-in for leaving, ease-in-out
  for repositioning. Never linear except progress bars and shimmer.
- **The 12 animation principles** (anticipation, follow-through, staging,
  slow-in/slow-out...). This is what separates alive from robotic.
- **Choreography.** Stagger, hierarchy of movement, what enters first and what
  follows. Composition in time.
- **When NOT to animate.** Restraint is craft. Movement that does not serve the
  content is noise. Run the removal test in
  [references/restraint.md](references/restraint.md): comment the animation out,
  look at the static version for ten seconds, and name what the user no longer
  knows. If the sentence is about you ("it feels flat") and not about them, the
  problem is the static design and motion is the wrong fix.
- **The effect must not steal from the content.** The headline wins, always.

For the animation principles, easing as craft, and the reusable fundamentals
(lerp/damping, noise, the minimal math, the 16ms budget, motion ethics), see
[references/motion-craft.md](references/motion-craft.md).

---

## Step 4: Ship gate (performance, accessibility, SEO)

Before integrating into a real page, confirm:

- [ ] Holds 60fps (16ms/frame) on a mid mobile, not just your machine.
- [ ] Heavy libs (Three.js) lazy-loaded so the weight lands only on the page that
      uses the effect.
- [ ] `prefers-reduced-motion` path exists and is not broken.
- [ ] Real title, copy, and links live in the HTML -- canvas/3D text is invisible
      to Google and screen readers. WebGL is decoration on top.
- [ ] Mobile has a tap path for any hover that hides essential content.
- [ ] No motion on a high-frequency, low-novelty interaction (list hover, context
      menu, tab switch, row add/delete). Re-run the Step 0 gate on anything that
      grew during the build -- effects accumulate one commit at a time.
- [ ] No `transition: all` anywhere. Properties are named.
- [ ] Anything the user can toggle animates with a transition, not keyframes, so
      a second click retargets instead of being ignored.

---

## Pitfalls (hard-won)

- **Server error in Next ("window is not defined").** WebGL/canvas need
  `"use client"` and usually `dynamic(..., { ssr: false })`.
- **Phone stutter.** Almost always density too high or `devicePixelRatio`
  unbounded. Cap dpr, cut particle count on mobile, pause offscreen.
- **Bloated bundle.** Three.js is hundreds of KB. Lazy-load it per page.
- **Forgotten accessibility.** Constant motion nauseates. `prefers-reduced-motion`
  is not optional in a serious site.
- **Effect competing with content.** If you strain to read the text, dial it back.
- **Content trapped in the canvas.** SEO and screen readers cannot see painted or
  3D text -- keep the real content in the DOM.
- **Hover that dies on touch.** See Step 2. The classic: a hover-revealed CTA that
  is invisible and unreachable on a phone.

---

## Working with other skills

- **ui-designer** owns static visual craft and *micro-motion*: easing curves,
  hover/press/focus states, a simple fade or 50-80ms stagger on ordinary UI. When
  the motion is that small, hand back to ui-designer. This skill takes over for
  scroll-driven, canvas, WebGL, generative, or otherwise "creative-coding" motion.
- **ux-designer** owns flows, psychology, and usability. Motion in service of a
  flow decision is theirs; the effect craft is yours.
- **design-system** owns tokens and component infrastructure.
- **frontend-design** owns bold overall aesthetic direction (landing/portfolio
  look). It sets the vibe; this skill builds the movement inside it.

When another skill fits better, say so directly.

---

## NEVER

- **NEVER** ship a WebGL/canvas component without `"use client"` + `ssr: false`.
- **NEVER** leave an animation loop running while offscreen.
- **NEVER** skip `prefers-reduced-motion` -- always provide the still version.
- **NEVER** leave `dpr` unbounded or run full desktop density on mobile.
- **NEVER** hide essential content or a CTA behind hover with no touch path.
- **NEVER** put real content or links only in canvas/3D (SEO + a11y).
- **NEVER** climb to WebGL when CSS or Canvas 2D delivers the scene.
- **NEVER** integrate an effect into an approved page before it is seen running.
- **NEVER** use linear easing except progress bars and shimmer loops.
- **NEVER** animate layout properties (`width`, `height`, `top`, `left`) -- only
  `transform` and `opacity`.
