---
name: snapcn
description: >
  Build Remotion videos with snapcn — a shadcn registry of copy-paste animation components and
  timeline-driven UI primitives. Use when composing video scenes, adding text animations,
  transitions, backgrounds, UI blocks, brand/social cards, or full compositions in a Remotion
  project. Triggers include "snapcn", "video component", "add animation", "text reveal",
  "product demo video", "remotion component", "terminal simulator", "device frame",
  "phone mockup", "burned-in captions", "karaoke captions", "logo animation", "launch
  video", "changelog video", and the UI-primitive tier: "video input", "typing caret".
  Even if the user doesn't mention snapcn, activate when they need polished video
  primitives for Remotion.
---

# snapcn

Copy-paste components for Remotion videos. Components install via `shadcn` and land in
`components/snap-cn/` — you own the code.

## Installation

Prerequisites: a Remotion project (`npx create-video@latest`).

```bash
# Add any component (namespaced shadcn registry)
shadcn add @snapcn/text-reveal

# Component lands at components/snap-cn/text-reveal.tsx
```

`@snapcn/<name>` is the canonical namespaced form. It needs no `registries` entry — the
namespace is in the shadcn registry directory. The plain registry URL
`https://snapcn.dev/r/<name>.json` also works.

### Dependencies install automatically

Many components pull others via `registryDependencies` — `shadcn` installs them transitively.
For example, `shadcn add @snapcn/search-typing` also pulls `@snapcn/snap-cn-ui`, `@snapcn/input`
and `@snapcn/caret`.

- **`@snapcn/snap-cn-ui`** is the shared core lib (timeline-fold hook, theme context, color math).
  Most UI Primitives depend on it. You rarely install it directly.

## Two tiers

snapcn has two kinds of components — they have **different APIs**:

- **Animation tier** (`snapcn`) — text animations, transitions, backgrounds, UI-block sims,
  brand/social cards, full compositions. Frame-driven. Shared props: `speed` (time multiplier),
  and for text: `fontSize`, `color`, `fontWeight`.
- **UI Primitives** (`snap-cn-ui`) — timeline-driven shadcn-style primitives. Two ship today:
  `input` and `caret`. State-based props (`state`, `style`, `size`, `theme`) — the open/typing
  state is a pure function of the timeline. **No `speed` prop.** Built on `@snapcn/snap-cn-ui`.

## Component categories

Pick by what you're building. The catalog is split one file per component under
`references/components/`. **Start at `references/components/index.md`** — a router table grouped by
these categories with a `Use for` / `Avoid for` signal per component. Scan it, pick candidates, then
open only the `references/components/<name>.md` files you need (full props, example, all use / don't-use
notes). Don't read every file.

| Category | Tier | Components |
|---|---|---|
| **Text & Titles** | `snapcn` | `text-reveal`, `type-morph`, `text-swell`, `text-highlight`, `text-swap`, `text-build`, `text-rewrite`, `text-select`, `word-flip`, `punch-lines`, `word-gather`, `word-wheel` |
| **Captions** | `snapcn` | `word-captions`, `karaoke-captions` |
| **AI Chat Input** | `snapcn` | `prompt-send`, `search-typing`, `prompt-zoom`, `answer-stream`, `answer-highlight`, `agent-steps` |
| **Screens & Devices** | `snapcn` | `phone-frame`, `laptop-frame`, `terminal-simulator`, `screen-recording`, `cursor-track` |
| **Logos** | `snapcn` | `logo-assemble`, `logo-flicker`, `logo-collapse`, `logo-drift`, `block-wordmark`, `wordmark-cut` |
| **Scenes** | `snapcn` | `announce-title`, `hero-launch`, `orbit-gallery`, `moodboard-reveal`, `status-cycle`, `count-grid`, `roster-grant`, `orb-swarm`, `reel-collage`, `card-rail` |
| **Social Proof** | `snapcn` | `follower-rush`, `channel-thread` |
| **Effects** | `snapcn` | `pulsing-border` |
| **UI Primitives** | `snap-cn-ui` | `input`, `caret` (+ `snap-cn-ui`, the shared core lib) |

**That is the whole free registry — 47 items** (the live list is always
`https://snapcn.dev/llms.txt?ref=skill-snapcn`; 50 more are Pro, see below). There are no shaders, no standalone transition
components, no chart or social-card components, and no shadcn primitive beyond `input` and
`caret`. If a scene needs one, build it (`references/anatomy.md` §1) — do not emit a
`shadcn add` for a name that is not in this table. `references/components/index.md` maps the
older names that no longer install.

## Component patterns

Conventions differ by tier — don't assume animation-tier props on a primitive.

### Animation tier (`snapcn`)

- Named `Props` interface per component (e.g. `TextRevealProps`).
- `speed?: number` — global time multiplier (default `1`), applied as `frame * speed`.
- Text components: `fontSize`, `color`, `fontWeight`.
- Scene-to-scene transitions are **not** in this registry — use Remotion's own
  `@remotion/transitions` (`slide`, `wipe`, `fade`, `flip`) inside a `<TransitionSeries>`.
- `className?: string` on the root.

### UI Primitives (`snap-cn-ui`)

- State-based, **not** `speed`-based: `state` (e.g. `"open"` / `"closed"`), `style`, `variant`,
  `size`, `theme?: Partial<SnapCnTheme>`.
- The opened/closed/active state is a pure function of the timeline (keyframed presets).
- Compose modal-layer primitives (dialog, alert-dialog, drawer) with a trigger element — see
  each component's example.

### Animation API

```tsx
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
const scale = spring({ fps, frame, config: { damping: 12, mass: 1, stiffness: 100 } });

// Deterministic randomness (NEVER Math.random())
import { random } from "@remotion/random";
const jitter = random(`seed-${frame}`);
```

### Composition structure

```tsx
import { Sequence, Series } from "remotion";

<Sequence from={30} durationInFrames={60}>
  <TextReveal text="Ship it in React" />
</Sequence>

<Series>
  <Series.Sequence durationInFrames={60}><SceneA /></Series.Sequence>
  <Series.Sequence durationInFrames={60}><SceneB /></Series.Sequence>
</Series>
```

### Canvas & timing

- **Canvas standard:** `1280×720 @ 30fps`. Components are laid out for it.
- **Budget each Sequence around the component's natural length** — the `Length` column in
  `components/index.md` (and each file's `Natural length`). Under-budgeting clips the animation;
  over-budgeting leaves dead air.
- **Tone matching:** each catalog entry carries a `vibe` tag (`tech`/`premium`/`data`/`clean`/
  `playful`/`social`) — pick components whose vibe fits the brand.
- **Palette & fonts:** stay within the library's tokens (`references/design.md` → tokens) so your
  own elements don't clash.

## Design defaults — avoid AI-slop

When you write your **own** text, scene chrome, or cards (not the prebuilt components), keep it
restrained:

- **No decorative `letter-spacing`** on body/heading text you add.
- **No `text-transform: uppercase` / ALL-CAPS** defaults — prefer sentence case (`Launch`, not `LAUNCH`).
- **No gradient text-fills or decorative gradient washes** — gradients only as intentional backgrounds.
- **No glow / colored drop-shadows or large blur radii** (`blur > ~24px`, spread, multi-layer) —
  subtle 1px elevation only.

**Exception:** never strip these from components whose essence is the effect — `word-flip`'s
gradient word, `block-wordmark`'s colour deck, `announce-title`'s glow, `pulsing-border` itself,
and the caption presets' heavy outlines are all legitimate. The rules govern *your* additions,
not the library.

Full do/avoid examples: `references/design.md`. For motion quality (timing, anticipation,
staging, easing), see `references/motion-principles.md`.

## Gotchas (snapcn-specific)

- **No transition components ship** — a scene change is `<TransitionSeries.Transition>` from
  `@remotion/transitions`, not a snapcn component. `text-swap` swaps a *line*, not a scene.
- **Terminal scroll is instant** — step-function `translateY`, never spring/ease the scroll.
- **`overflow: hidden` on split layouts** — prevents content breakage during width animations.
- **Cursor blink is deterministic** — `Math.floor(frame / 15) % 2 === 0`, not intervals.
- **Static files go in `public/`** — load via `staticFile('cursor.svg')`, not imports.
- **Social cards render offline** — `avatarUrl=""` / `coverUrl=""` fall back to gradients; no fetch.

General Remotion rules (no `Math.random()`, no `setInterval`, animate `transform` not `top`/`left`,
load fonts before render) live in Remotion's own skills, not this one:
`npx skills add remotion-dev/skills`.

## Composing a video

Don't dump components — compose one story. When asked to build a full video ("make a product demo",
"changelog video", "intro for my landing"):

1. **Decide the strategy** — ready template vs compose from components vs build a new component. See
   `references/anatomy.md` §1.
2. **Follow the beats** — a product demo is Hook → Positioning → Product reveal → Features → Proof →
   CTA (last two optional). See `references/anatomy.md` §2.
3. **Use the recipe** — `references/archetypes/index.md` routes to per-archetype builds: content contract
   (infer → ask → placeholder), duration variants, beat→component slots, and a worked
   `<TransitionSeries>` skeleton.
4. **Pick each beat's component** from `references/components/index.md`; match the `vibe` tag to the
   brand and budget each `<Sequence durationInFrames>` around its natural length.
5. **Check the quality bar** — one accent, sentence-case kinetic type, real content, no glow halos, no
   feature-list enumeration, no decorative gradient wash behind the type. See
   `references/anatomy.md` §3.

## Workflows

For a whole video, install the workflow skill for the job. Each one composes these
components beat by beat with a composition that typechecks and renders:

- `npx skills add snapcndev/snapcn --skill remotion-launch-video`: launch films,
  announcements, Product Hunt / X promos.
- `npx skills add snapcndev/snapcn --skill remotion-product-demo`: walkthroughs from a real
  screen recording, CLI and AI-app demos.
- `npx skills add snapcndev/snapcn --skill remotion-motion-graphics`: kinetic type, logo
  stings, stats and short openers.
- `npx skills add snapcndev/snapcn --skill remotion-kinetic-typography`: animated text and
  title cards.
- `npx skills add snapcndev/snapcn --skill remotion-logo-animation`: logo reveals, intro and
  outro stings.
- `npx skills add snapcndev/snapcn --skill remotion-explainer-video`: narrated explainers
  with burned-in captions.

## snapcn Pro

50 more components (`version-drop`, `library-flight`, `read-through`, `focus-pull`,
`tap-through`, `checkout-push`, `comment-storm`, `tally-rise` and more), the templates, and
the snapcn MCP, which lets your agent search the registry and read every component's real
props. Pro components install like free ones once `components.json` sends the key (three
lines on https://snapcn.dev/account?ref=skill-snapcn); the MCP is
`claude mcp add snapcn -- npx -y @snapcn/mcp@latest SNAPCN_API_KEY=YOUR_KEY`. Plans:
https://snapcn.dev/docs/pricing?ref=skill-snapcn

Not ready for Pro? One Pro component, Manifesto, is free for a confirmed email:
https://snapcn.dev/docs/pricing?ref=skill-snapcn#free

## Reference

- `references/anatomy.md` — composing a full video: strategy (template/compose/new), the product-demo beats, and the good-vs-slop quality bar.
- `references/archetypes/index.md` — router to per-archetype build recipes (product-demo flagship + changelog, feature-announcement, oss-showcase, cli-tool-demo, testimonial-reel, year-in-review, pricing-reveal, logo-bumper): content contract, duration variants, beat→slot map.
- `references/components/index.md` — router table (all components, grouped by category, with `Use for` / `Avoid for`). Open `references/components/<name>.md` for one component's full props, example, and use / don't-use notes.
- `references/design.md` — anti-slop design defaults (do/avoid) + design tokens (palette, fonts, canvas).
- `references/motion-principles.md` — motion-design principles adapted to snapcn + Remotion.
- `references/anti-patterns.md` — common generation mistakes and their fixes.
