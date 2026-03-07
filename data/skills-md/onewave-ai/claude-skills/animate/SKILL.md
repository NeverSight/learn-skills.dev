---
name: animate
description: Generate animated videos and motion graphics from natural language descriptions. Creates a standalone Vite + React project with Framer Motion scenes that auto-play in the browser. Use when the user wants to create animations, motion graphics, video intros, animated presentations, or product demos.
argument-hint: [description of the animation you want]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
---

# Animation Generator

Create animated videos and motion graphics from a natural language description. Outputs a standalone Vite + React + Framer Motion project that plays in the browser.

## Workflow

### Step 1: Parse the Request

Break the user's description into a scene plan:
- **3-7 scenes**, each 3-5 seconds long
- Identify the story arc: hero/intro, problem, solution, features, CTA/outro
- Pick a color palette and typography that fits the brand/mood
- Use `$ARGUMENTS` for the user's animation description

### Step 2: Choose the Animation Stack

Auto-detect the best approach based on the request:

| Request Type | Stack | When to Use |
|---|---|---|
| Product intro, presentation, marketing | **Framer Motion** (default) | Scene-based with text, icons, transitions |
| Generative art, particles, patterns | **p5.js** | Creative/algorithmic visuals |
| 3D objects, environments, product renders | **Three.js + react-three-fiber** | 3D scenes needed |
| Simple text/logo animation | **CSS animations only** | Minimal, no heavy deps |

Default to **Framer Motion** unless the request clearly needs something else.

### Step 3: Scaffold the Project

1. Create a directory: `~/animations/[project-name]/`
2. Run the scaffold script: `bash ~/.claude/skills/animate/scripts/scaffold.sh [project-name] [stack]`
3. Copy template files from `~/.claude/skills/animate/assets/template-files/` into the project

### Step 4: Generate Scene Components

Read the references for animation presets and scene patterns:
- `references/animation-presets.md` — all available transitions, springs, easings
- `references/scene-patterns.md` — example scene code patterns

For each scene, create a React component in `client/src/components/video/video_scenes/`:
- Use `motion.div` with scene transition presets (fadeBlur, scaleFade, slideLeft, splitHorizontal, morphExpand, etc.)
- Use `containerVariants` and `itemVariants` for staggered content reveals
- Use `vw` units for responsive sizing (works at any resolution)
- Use CSS variables for theming (`var(--color-accent)`, `var(--color-bg-dark)`, etc.)
- Use Lucide icons for visual elements
- Use `.glass-panel` class for frosted glass cards
- Use `.text-gradient` and `.text-gradient-accent` for gradient text

### Step 5: Generate the VideoTemplate

Create `client/src/components/video/VideoTemplate.tsx`:
- Import all scene components
- Define `SCENE_DURATIONS` object (scene name -> milliseconds)
- Use `useVideoPlayer` hook to manage scene advancement
- Wrap scenes in `AnimatePresence mode="wait"` for smooth transitions
- Each scene renders conditionally based on `currentScene` index

### Step 6: Customize Theme

Update `client/src/index.css` with the right colors:
- If the user specified brand colors, update CSS variables
- Choose fonts that match the mood (Space Grotesk for tech, Playfair Display for elegant, etc.)
- Update gradient and glow styles to match the palette

### Step 7: Gemini 3.1 Pro Enhancement (Optional)

If `GEMINI_API_KEY` environment variable is available:

1. Read `references/gemini-integration.md` for API details
2. Send the user's description to Gemini 3.1 Pro asking for:
   - Scene breakdown with descriptions and suggested transitions
   - Color palette as CSS variables
   - Copy/headlines for each scene
   - SVG graphics if applicable
3. Use the Gemini output to inform scene generation
4. If no API key, skip this step — Claude handles all creative decisions directly

### Step 8: Build and Preview

```bash
cd ~/animations/[project-name]
npm install
npm run dev
```

Tell the user the animation is running at `http://localhost:5173` and open it in the browser.

## Scene Transition Reference (Quick)

Pick transitions that match the story beat:

- **fadeBlur** — Soft intro/outro, dreamy reveals
- **scaleFade** — Confident reveals, product showcases
- **slideLeft/slideRight** — Sequential progression, timeline flow
- **splitHorizontal/splitVertical** — Dramatic reveals, before/after
- **morphExpand** — Grand finale, CTA screens
- **clipCircle** — Focus attention, spotlight effect
- **perspectiveFlip** — Card flips, perspective changes
- **wipe** — Clean transitions, directional flow
- **zoomThrough** — Immersive, forward momentum
- **crossDissolve** — Gentle, emotional transitions

## Element Animation Reference (Quick)

- **popIn** — Bouncy scale entrance for icons/badges
- **fadeUp/fadeDown** — Subtle content reveals
- **slideInLeft/slideInRight** — Directional content
- **blurIn** — Soft focus reveals
- **elasticScale** — Playful, energetic entrances
- **perspectiveRotateIn** — 3D card reveals
- **pulse** — Looping attention grab
- **float** — Gentle hovering effect

## Important Rules

1. Always use `vw` units for sizing so animations look good at any resolution
2. Keep scenes between 3-5 seconds each — total video 15-30 seconds
3. Use `AnimatePresence mode="wait"` so one scene exits before the next enters
4. Every scene must have a background treatment (gradient, image, or animated shape)
5. Use staggered animations for lists and grids (staggerChildren: 0.1-0.2)
6. Include a loading state if assets are heavy
7. The project must be completely self-contained — no external dependencies beyond npm packages
8. Do NOT use emojis anywhere in the generated code or content
