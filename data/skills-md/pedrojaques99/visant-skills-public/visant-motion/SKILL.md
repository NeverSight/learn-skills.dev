---
name: visant-motion
description: 'Visant motion and micro-interaction system: easing/duration tokens mirrored in CSS and framer-motion, plus motion-lint and URL measurement. Use on "animation", "transition", "make it smoother", "apple-like", "loading", "skeleton", "animação", "deixa mais suave", "tela de espera", "micro-transições", /visant-motion.'
---

# Visant Motion

Build interfaces where motion is invisible-correct: every transition has a purpose, responds instantly, and stays under the perception of "slow". Governing rule: **SSoT, never hardcode a cubic-bezier or a duration in a component.**

**§1 and §2 are the whole skill in practice.** Everything after them is reference for a specific moment; the SSoT bootstrap is at §10 because it only matters once per repo (why: [references/cases.md](references/cases.md)).

**Source of the principles:** Emil Kowalski's skills, https://github.com/emilkowalski/skills (`emil-design-eng`, `apple-design`, `improve-animations`, `review-animations`), distilled from animations.dev + Apple *Designing Fluid Interfaces* (WWDC 2018). Consult that repo for the upstream, canonical guidance; this skill is Visant's applied, SSoT-ized version of it.

## 0. Find the target repo's motion SSoT first

Before writing or auditing any motion, find where the repo keeps it. Look for:

- a JS/TS module exporting easings and durations: grep for `EASE_OUT`, `cubic-bezier`, `DUR`, `transitions` (common names: `lib/motion.ts`, `src/lib/motion.ts`, `utils/animation.ts`);
- CSS custom properties: grep the global stylesheet for `--ease-` and `--dur-`;
- the shared primitives that already carry motion: `Button` (press feedback), overlay wrappers (popover/dropdown/dialog), a toast library (`sonner`), a delayed-loader hook.

Found one → **use it**, adapt the symbol names below to it, and never create a parallel system. Found none → §10. Every `lib/motion.ts` / `@/lib/motion` below means "the repo's motion SSoT", whatever its real path.

## 1. Decision rules (the short version)

Decide in this order. Full numeric catalog + severity for audits → **`references/motion-rules.md`**.

1. **Should it animate?** 100+×/day (shortcut, toggle, ⌘K) → **don't**. Occasional (modal, toast) → standard. Rare (onboarding) → can delight.
2. **Easing:** enter/exit → `EASE_OUT`. Move on-screen → `EASE_IN_OUT`. Hover/color → `ease`. Constant (marquee/shimmer/progress) → `linear`. **Never `ease-in` on UI**, with one exception (§5 rule 2).
3. **Duration:** UI < 300ms. press 100-160 · dropdown 150-250 · modal 200-300. Route passages (§5), marketing, scroll and 3D may be long & deliberate; the ceiling is about a control answering a click.
4. **Never `scale(0)`**: start at `scale(.95)` + opacity.
5. **Only `transform` + `opacity`** (GPU). Never animate `width/height/margin/padding`.
6. **Springs** only for momentum/gesture (drag, flick). A menu fade uses duration, not spring.
7. **Interruptible** = CSS transition / spring, not `@keyframes` (which restarts from zero).

## 2. Gotchas (non-obvious, all battle-tested; read before you write)

1. **`duration-[var(--dur-x)]` throws a build "ambiguous" warning** (Tailwind can't tell transition- from animation-duration). Use property-explicit: **`[transition-duration:var(--dur-base)]`**.
2. **framer-motion overrides CSS transforms.** If a `motion.div` animates `y`/`scale`, a Tailwind `hover:-translate-y-*` is silently eaten by the inline transform. Fix: let framer own transform (`whileHover={{y:-2}}` + `whileTap`), CSS handles only shadow/border.
3. **`whileTap` needs its own transition** or it inherits the (slow) enter transition: `whileTap={{ scale:.985, transition:{ duration: DUR.press, ease: EASE_OUT } }}`.
4. **Never `transition-all`**: it animates unexpected props and janks. Scope: `transition-colors`, or `transition-[color,background-color,border-color,box-shadow,opacity]`, or `transition-transform`. Use the codemod (§7) to sweep a repo.
5. **Origin-aware overlays:** Radix exposes `--radix-<primitive>-content-transform-origin`. Add `origin-[var(--radix-popover-content-transform-origin)]` (and dropdown-menu/select/context-menu/tooltip/hover-card) so they scale FROM the trigger. **Exception: modals stay `transform-origin: center`** (not anchored to a trigger).
6. **Reduced motion is a real signal, not "off".** Keep opacity/color, drop movement/spring. A global `@media (prefers-reduced-motion) { *{…0.001ms} }` guard is the cheap safety net. On a list-row exit that means the row still *leaves*: you zero the animation, never the outcome.
7. **An exit animation played behind an open modal is wasted, and it stalls the close.** Completing an item from a dialog where the payoff is the row collapsing out of the list, the naive order awaits the ~300ms exit (a `completing` flag on the row) and *then* closes the modal, so the collapse runs hidden under the modal and the modal sits ~300ms doing nothing. Close the surface **first**: the modal closing is itself the exit-with-weight, and the row then collapses in view. Same rule as skipping the ritual when a kanban card changes column (the column-move *is* the exit). One visible exit per surface, never two. Pattern → `visant-frontend` › [Close the surface before the exit ritual](../visant-frontend/references/stack-tailwind-react.md#close-the-surface-before-the-exit-ritual).
8. **Amplitude, not duration, is what reads as amateur.** A delete with a big spin, overshoot and a cloud of particles was rejected as amateur; the fix kept the timing and cut the amplitude (~12° spin, row shrinks to 40%, neighbours pulled ≤ 4px, no overshoot on anything that disappears). Rule: halve the amplitude, then halve it again; good motion is barely noticed. Full case: [cases.md](references/cases.md).
9. **One focus of motion per surface.** Queue ticking, images streaming in, an export counting %, an error shaking and a toast sliding, all at once, reads as too much happening. Sequence the states (sent → generating → ready → exporting) so only one thing moves at a time.
10. **Born in the best state.** A tilt/gleam/perspective that only appears on hover doesn't exist on touch, in a grid thumbnail or in a screenshot. Start in the hero pose; hover intensifies, it never reveals.
11. **Scaled stages lie to motion code.** Inside a `transform: scale` container (a component showcase, a zoomed preview): pointer deltas must be divided by the scale, `position: fixed` measures from the transformed box (portal to `body`), and R3F canvases need `resize={{ offsetSize: true }}`. Test any drag at `scale(0.5)`.

## 2b. Sound (SFX): analog clicks, only where the person acts

Sound is motion for the ear and obeys the same ceilings. The house engine is `sfx-bus` (Web Audio synthesis, zero files, zero requests; `npx shadcn@latest add @visant/sfx-bus` from the Visant library at [ui.visantlabs.com](https://ui.visantlabs.com/llms.txt), which also ships ready motion pieces: `motion-layer`, `fold-motion`, `line-reveal`, `text-morph`, `count-up`, `toast-stack`). Check first whether the target repo already has a sound layer.

- **Model each timbre on a real analog object, never a synth note.** Filtered noise bursts through high-Q band-passes (modal synthesis), several hits at different instants for a mechanism. The palette: `click` (camera button), `detent` (knob/selector tooth), `toggle` (lever with body), `focus` (lens focus ring ratchet, for continuous drags), `complete` (shutter arming and releasing, for a confirmed action), `drop` (needle landing/soft air, for a strong action). No pitch, no tail: pitched sounds with reverb tire in an interface.
- **Map gesture → timbre:** discrete step (knob, tab, dock icon crossed) → `detent`; continuous drag (slider) → `focus` per 1/20–1/40 of travel; switch → `toggle`; hold/slide to confirm reaching the end → `complete`. A drag must not play on every pixel, and a parametric curve someone tweaks for minutes should stay silent.
- **Never on hover by default**, only where the person acts. Exception that works: a dock where the pointer crossing icons ticks a tiny `detent`, throttled ~45ms.
- **Armed, not autoplayed:** AudioContext created only after a real gesture (`navigator.userActivation`), muted under `prefers-reduced-motion`, a saved preference wins, per-timbre minimum interval, random offset/±6% pitch so twelve hits don't read as a loop. Only on `(pointer: fine)`; the toggle hides on touch.
- **Level:** every timbre below a typical UI click (~-44 dBFS RMS); measure with an `OfflineAudioContext` render and keep the numbers in a table in the source comment.

## 3. The API (the starter's `lib/motion.ts`; map to the repo's own names)

```ts
import { EASE_OUT, EASE_IN_OUT, EASE_DRAWER, DUR, transitions,
         fadeInUp, fade, itemEnter, pressable } from "@/lib/motion";
```

| Symbol | Value | Use |
|---|---|---|
| `EASE_OUT` | `[0.23,1,0.32,1]` | enter/exit, responds to input: **the default** |
| `EASE_IN_OUT` | `[0.77,0,0.175,1]` | move/morph ON screen (not enter/exit) |
| `EASE_DRAWER` | `[0.32,0.72,0,1]` | sheets/drawers (iOS-like) |
| `DUR` | `{press:.12, fast:.16, base:.2, slow:.3}` | duration scale (seconds) |
| `transitions.*` | `fast/base/slow/spring/springSoft` | ready-made transition objects |
| `fadeInUp`, `fade` | variants (`hidden`/`show`) | house entrances |
| `itemEnter(i, step=.04, cap=.4)` | (function) | list-item entrance, short capped stagger |
| `pressable` | (object) | subtle `whileTap` for clickable cards/tiles |

CSS form (property-explicit, see gotcha #1): `[transition-duration:var(--dur-base)] [transition-timing-function:var(--ease-out)]`.

## 4. Waiting is a surface (design every pending state)

Every moment the user waits has motion on it whether you designed it or not; a bare spinner is just the default nobody chose. Waits are also **rare-frequency** by §1 rule 1, so this is where the delight budget actually lives: illustration, brand character, a loop worth watching. It's the one place in the product where charm doesn't fight the work.

Pick by **how long the wait is**, not by what's convenient:

| Wait | Design it as | Never |
|---|---|---|
| < 100ms | nothing: optimistic write + undo toast | a spinner (it only flashes) |
| 100–300ms | current UI holds; the press feedback already answered | swapping the surface to a loader |
| 0.3–1s | skeleton in the final layout, crossfade to content | spinner, layout jump on arrival |
| 1–5s | skeleton + progressive reveal; determinate bar only if the % is real | fake progress that parks at 90% |
| 5s+ | narrated steps + an illustration/loop, label what's happening *now* | one static spinner for a minute |
| unknown | stream partials: content arriving **is** the loader | indeterminate anything |

1. **Answer the click before the server does.** Press feedback + immediate state change is frame one of loading. Optimistic patch + undo (§6) beats every spinner; and if the surface closes on click, the in-button spinner can never show at all, so it's dead chrome: `visant-frontend` › [unreachable spinner](../visant-frontend/references/stack-tailwind-react.md).
2. **Anti-flicker pair:** don't show a loader before ~300ms; once shown, hold it ~500ms. A loader that blinks reads as a bug, not as speed.
3. **Skeleton ≈ the real layout** (same box sizes, radius, gaps) so content lands without shift. Shimmer is `linear`, infinite, ~1.2–1.6s: constant motion (§1 rule 2). It's the one legitimate `@keyframes` in the app, because nothing ever interrupts it.
4. **Never hard-swap skeleton→content.** Crossfade at `DUR.base`, tiny `y` on the first block only; everything else is already in place.
5. **An empty state is a wait too**, waiting on the user's first data. It earns the same treatment: illustration plus the single action that ends the wait. (Whether it earns space at all is `visant-frontend`'s call, not this skill's.)
6. **Reduced motion:** shimmer/pulse degrades to a static tint or slow opacity fade. The progress readout stays: it's information, not decoration.
7. **One waiting animation per surface.** Skeleton rows + spinner + progress bar together are three answers to one question.
8. **Never let the entrance cost more than the wait.** A 400ms reveal on a 200ms fetch means you built the latency yourself.
9. **A wait ends in a result: design the losing branch too.** Skeleton → error is the transition everyone forgets, and it's the one that lands hardest: the skeleton has been promising content for 3s. Don't collapse the layout; swap the skeleton in place for the error, keep the box, put retry inside it. Same crossfade, no bounce, no red flash. An error is information, not a scare.

Progress meters, gauges and sparkline-style readouts for long jobs are drawn by **`visant-refine`**; this section only governs their timing.

## 5. Navigation & shared elements (the passage between routes)

The <300ms ceiling governs a control answering a click. A route passage is a different animal, and it's where a web app stops feeling like a web app.

**Don't write this from scratch.** Vercel maintains the patterns and the full CSS as an official skill; install it and follow it for the *how*:

```bash
npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-view-transitions
```

This section owns the *when* and the house deltas. Four patterns, each making a different claim to the user:

| Pattern | What it claims | Reach for it when |
|---|---|---|
| Shared-element morph (`<ViewTransition name>`) | "same object, going deeper" | thumbnail → detail, row → record page |
| Suspense reveal (`enter`/`exit` on the boundary) | "the data arrived" | §4's skeleton handoff, at route scale |
| Directional slide (`transitionTypes` on `<Link>`) | "forward / back" | there's a real hierarchy to encode |
| Same-route crossfade (`key={slug}`) | "same place, different content" | tabs, filters, period switches |

House rules:

1. **Durations live in `--dur-vt-*`**, never inline: exit 150 · enter 210 (delayed by the exit) · move 400. The asymmetry is the point: the old view leaves fast because it already lost the argument; the new one arrives calmly enough to read.
2. **The one exception to "never `ease-in`" is `::view-transition-old`.** Nothing is waiting on an exit, so front-loading its stillness costs nothing. Everywhere else the ban holds, and `motion-lint` encodes exactly this exception.
3. **`default="none"` on every named pair,** or each named `ViewTransition` animates during unrelated transitions. Counter-trap: with `default="none"` and no explicit `share`, the morph silently stops morphing.
4. **Anchor something.** The header must not slide. Without one fixed reference the user reads "the whole viewport jumped" instead of "the content changed".
5. **The wrapper goes in `page.tsx`, never the layout** (Next App Router): layouts persist across navigation, so enter/exit never fire there. Costs an hour to discover by hand.
6. **`::view-transition { pointer-events: none }`**, already in the starter CSS. Without it, a tap during a 400ms passage is silently swallowed.
7. **Browser back carries no transition type.** Don't encode meaning that only exists on your own links.
8. **Reduced motion needs its own rule**: the global `*` guard does not reach view-transition pseudo-elements (they hang off the document). Directional slides are the top motion-sickness trigger; this is the one guard you cannot skip. Also in the starter CSS.
9. **Not every morph is a navigation.** A row reordering, a card changing column, an item moving between lists: nothing navigated, so View Transitions is the wrong instrument. That's framer-motion's `layout` / `layoutId` (it FLIPs, so the size change runs on `transform` and stays honest with §1 rule 5). Two costs to know: `layout` on a long list re-measures every child on each commit, so scope it to what actually moves; and a `layoutId` pair must be mounted in the same `AnimatePresence` or the morph degrades to a plain crossfade. Rule of thumb: **route changed → View Transitions; DOM reshuffled in place → `layout`.**

**Scroll-driven motion:** prefer native `animation-timeline: scroll()` / `view()` over a scroll library: it runs off the main thread, so it can't jank. Gate it behind `@supports (animation-timeline: view())` and keep the JS path as the fallback, not the default. Scroll and marketing motion may be long and deliberate; they're audited-and-kept, not defects.

## 6. Reuse before rebuilding

In the target repo, look for these before writing anything new (a filled-in example from a real app is in [cases.md](references/cases.md)):

- **Press feedback on the shared `Button`** (`active:scale-[0.97]` or similar). If it's there, every button already has it; don't re-add it per button. If not, put it on the shared primitive once.
- **Origin-aware shared overlays.** New custom overlay? Apply the same Radix var.
- **The feedback pattern** (often optimistic UI + a toast like `sonner` + undo). Reuse it; don't invent modal confirmations.
- **Any completion ritual** (celebrate → row exit → optimistic patch → undo). Grep for the hook that owns it (`use*Actions`, `useComplete*`, the mutation hook behind the list). A new surface that needs to complete/act on an item calls that hook on the **same data key**; it does not re-implement the ritual, or its counts silently diverge. High-frequency sub-values (a running clock) belong in their own context so the ritual's consumers don't re-render every second: `visant-frontend` › [Split a per-second value into its own context](../visant-frontend/references/stack-tailwind-react.md#split-a-per-second-value-into-its-own-context).

## 7. Tooling: lint, then codemod

### `motion-lint.mjs`: the severity table, executable

The audit rules only bind if something enforces them. `scripts/motion-lint.mjs` runs the HIGH/MEDIUM catalog as 12 regex rules with file:line, reason and fix. No dependencies, no config.

```bash
node scripts/motion-lint.mjs                     # human output, cwd
node scripts/motion-lint.mjs src app --strict    # fail on MEDIUM too
node scripts/motion-lint.mjs --json              # for CI or an agent
```

Exit 1 on any HIGH (`--strict` adds MEDIUM), so it drops straight into a pre-push hook or CI. It knows the real exceptions: `ease-in` on `::view-transition-old`, `--dur-vt-*` above 300ms, `cubic-bezier` inside the SSoT file itself, a loader in a file that imports `useDelayedFlag`. When a rule is genuinely wrong for a line (long, deliberate marketing/scroll motion), suppress it *with a reason*:

```
// motion-lint-disable-next-line slow-ui-duration  scroll-driven hero, deliberate
```

Rules: `ease-in-on-ui` · `scale-zero` · `transition-all` · `slow-ui-duration` · `hardcoded-curve` · `hardcoded-duration` · `layout-property-animation` · `background-position-shimmer` · `whiletap-inherits-transition` · `loader-without-guard` · `fake-progress` · `popover-origin`.

**After editing any rule, run `node scripts/motion-lint.mjs --self-test`.** It checks the three things a regex suite loses silently over time: every rule still fires against `scripts/__fixtures__/bad.*`, the clean fixture still reports zero (no false positives), and suppression still suppresses. A rule that quietly stopped matching is worse than no rule: the audit comes back green. Add a fixture case with every new rule; the self-test fails if a rule has no case.

### `--fix`: the mechanical half, in one command

```bash
node scripts/motion-lint.mjs --fix <target>   # runs both codemods below
```

Most of a real audit is not judgement (in one round, 48 of 55 findings were inline durations wanting a token). `--fix` is the door; the codemods own the decision of what is safe to rewrite. What it deliberately leaves alone: `ease-in` on UI, `scale(0)`, non-origin-aware popovers, blinking loaders, undesigned waits. Those are design decisions, not text substitution.

### `codemod-duration.mjs`: inline durations → `DUR.*`

```bash
node scripts/codemod-duration.mjs                 # dry-run: the plan, in three buckets
node scripts/codemod-duration.mjs --apply         # exact + near
node scripts/codemod-duration.mjs --apply --over  # also >300ms (read the list first)
```

Three buckets, because the rewrites are not equivalent. **EXACT**: the number already *is* a token (`0.2` → `DUR.base`); pure rename. **NEAR**: within 25% of a token and under the 300ms ceiling (`0.25` → `DUR.base`). **OVER**: above 300ms (`0.6` → `DUR.slow`), which *halves the animation*: that's a behaviour change, not a refactor, so it needs `--over` and a look at the list. Route passages and marketing are legitimate exceptions and only someone watching the screen can say so.

A value far from every token stays **UNMAPPED** instead of being guessed: `0.08` may be a deliberately drier press, and silently snapping it to `DUR.press` erases the decision rather than recording it. The import is added using whatever path the repo itself already uses for the SSoT.

### `codemod-transition-all.mjs`: sweep the second biggest finding

`scripts/codemod-transition-all.mjs` rewrites `transition-all` to the minimal correct target, **skipping** elements that animate a transform in an interactive state, and **excluding** shared `ui/**` primitives. Guarded, idempotent, dry-run first:

```bash
node scripts/codemod-transition-all.mjs          # dry-run: prints the plan + skips
node scripts/codemod-transition-all.mjs --apply  # writes changes
```

Adjust the `ROOTS` / `isUi` constants at the top to the target repo's layout before applying. Always run `tsc` + tests + build after.

## 8. Feel-check: measure the URL, then judge with your eyes

**Measure first, on the deployed URL.** A source scan passes clean on a page that janks; only the running page tells the truth.

```bash
node scripts/measure-motion.mjs https://app.example.com
node scripts/measure-motion.mjs <url> --click "[data-testid=row],#open"
node scripts/measure-motion.mjs <url> --reduced-motion --no-inp
```

It drives the page (hover → click → escape → scroll) and reports what the device actually did:

- **INP** with attribution, via `web-vitals`. Read the split: `presentation` dominating means the *animation* is the cost; `processing` dominating means the handler is. Different bug, different fix.
- **Long Animation Frames** (Chromium 123+) with per-script attribution: the frame that blocked, and the function that blocked it. This is the jank users feel and never report.
- **Reduced-motion audit:** with `reduce` forced, anything still running over 100ms is listed as a leak. The check nobody does by hand, and the reason the starter CSS carries a separate view-transition guard.

Exit 1 past budget (`--budget-inp 200`, `--budget-blocking 100`), so it gates a deploy.

**Then judge with your eyes**; the numbers can't. DevTools → Animations → 25% speed: press gives an instant scale-down? popover grows from its trigger? no two overlapping states during a crossfade? stagger reads as a short cascade, not one-by-one? Review again the next day with fresh eyes.

## 9. Auditing a codebase

**Start with §0 (find the SSoT), then `node scripts/motion-lint.mjs --json` (§7)**: it does the whole grep sweep for you, with severity and fixes already attached. Then measure the deployed URL (§8). Only then read code, and only where the tools pointed.

Two things the lint can't see, so audit them by hand: **waiting states** (list every `isLoading`/`isPending`/`Suspense`/empty branch and ask what the user is looking at during each, §4) and **navigation**, which is judged by whether the passage makes a true claim, not by any pattern in the source (§5). Then load **`references/motion-rules.md`** for the audit categories, HIGH/MEDIUM severity criteria, and exact fixes. Report findings by leverage (impact ÷ effort); fix core/shared primitives first (they propagate to every route). Long, deliberate marketing/scroll/3D animations are audited-and-kept, not flagged.

## 10. Bootstrap the SSoT (only when §0 found nothing)

Motion lives in ONE place, mirrored across JS and CSS so framer-motion and Tailwind/Radix stay in lockstep. Put the files where the repo keeps its shared libs (check the `@/` alias in `tsconfig.json`):

- **JS:** `assets/motion-ssot-starter/motion.ts` → e.g. `lib/motion.ts` (easings, `DUR`, variants, and the `WAIT` thresholds of §4).
- **CSS:** merge `assets/motion-ssot-starter/globals-tokens.css` into the `:root` + a `@layer utilities` block of the app's global stylesheet. Ships the `.skeleton` shimmer, the `--dur-vt-*` route-transition scale, and the two reduced-motion guards the global `*` rule can't reach.
- **Waiting:** `assets/motion-ssot-starter/use-delayed-flag.ts` → e.g. `lib/use-delayed-flag.ts`. Every loader in the app goes through it (§4.2), so the anti-flicker pair is a shared primitive and not a thing each dev re-derives wrong.

If the repo already has an equivalent, **use it**; do not create a parallel system. `node scripts/motion-lint.mjs` (§7) is what keeps the SSoT single instead of merely stated.
