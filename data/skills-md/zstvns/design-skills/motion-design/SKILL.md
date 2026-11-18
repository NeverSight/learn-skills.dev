---
name: motion-design
description: "Design and build UI motion with intent — micro-interactions, transitions, entrances, scroll and hover behavior — applying the twelve principles of animation to a brand's settled system, in custom code. Use when the user mentions 'animation,' 'motion,' 'micro-interactions,' 'hover effect,' 'transition,' 'scroll animation,' 'page-load animation,' 'make it feel alive,' 'the interactions feel off,' 'add motion,' 'easing,' or 'why does this feel cheap/janky.' This is where a static surface becomes something that moves with weight, emotion, and restraint — not fade-up-on-everything."
metadata:
  version: 1.6.1
---

# Motion Design

You design and build **UI motion** — and you build it in custom code. Motion is not decoration sprinkled on a finished page; it is the arrangement of *time* the same way layout is the arrangement of space. Done right it gives a surface weight, emotion, and life, and keeps a person on the page. Done wrong it is the single loudest tell of an amateur build.

Read `design-principles` first. Everything here is that philosophy in the time dimension: **hierarchy** (not everything moves, and not equally), **restraint** (protect the few motions that carry meaning by cutting the ones that compete), **emotion before execution** (know the feeling before you pick the easing), and **defaults-not-laws** (every animation earns its place with a reason, or the default — no motion — stands).

> **Position in the sequence:** an Application skill, sibling to `web-design`. `web-design` ships the surface with a *light motion floor* and defers the real motion craft — expressive easing, timing, choreography — to here. Motion applies to a built, structurally-sound artifact; it does not invent one. It consumes the system's motion character; it does not define the system.

## Front-Door Diagnosis — Is There Anything to Animate Yet?

Motion is the **last layer.** Before adding a single transition, confirm two things:

1. **The artifact is structurally sound.** Proper markup, real hierarchy, working layout, real copy in place. *If the layout is still moving, don't animate it* — you'll polish motion onto something that's about to change. Route back to `web-design` (or whichever Application skill built the surface).
2. **The visual system is settled and its motion character is known.** Open `.agents/design.md`. A brand has a motion *feel* the same way it has a color and a type feel — playful and springy, or calm and premium, or precise and mechanical. That feeling traces to the **emotional target** and the muses (`creative-direction`). If the system is being defined or reworked (Revolution / heavy Evolution), **route back to `creative-direction`** — motion character is part of the identity, not something you invent at the end.

The rule of thumb mirrors `web-design`: **proceed only when the surface is built and the system is settled.** Otherwise, go back.

## Motion Is Emotion — the Core Insight

It's in the word: **e-motion.** Motion is not a finishing layer applied to a design — it is one of the most direct carriers of feeling the brand has. The proof is counterintuitive: **the same element, animated two different ways, communicates two entirely different things.** A button with a fast springy overshoot reads *fun and loose*; the identical button scaling up slowly and settling reads *premium and serious*. You have not changed the pixels — you changed the time, and the feeling flipped.

Two levers do most of that work at the element level:

- **Speed encodes cost.** Fast is snappy, casual, inexpensive. Slow is deliberate, luxurious, expensive — a thing that takes its time because it's serious.
- **Size sets pace.** Small things move fast; big things move slow — a mouse scurries, an elephant lumbers. A tiny toggle that eases lazily feels broken; a full-screen panel that snaps feels cheap. Match duration to the mass of the thing moving.

So before you touch the easing, ask what `design-principles` asks of every choice: **what should this feel like?** The answer picks your timing and your curve. And that answer is not yours to invent — it comes from the brand.

## Motion Character Is Brand-Derived — Calibrate the Whole System First

**How motion is executed is contingent on the brand being built.** Motion character is part of the identity, defined in `creative-direction` and traceable to the **emotional target** and the muses in `.agents/design.md` / `.agents/brand.md`. Two brands can apply every principle in this skill correctly and end up with motion that looks nothing alike — and both be right.

Before animating anything, set the **system-level dial**, not just per-element curves. Four things vary by brand:

- **Easing personality** — how strange the curves are allowed to be. Springy, elastic, overshooting, even sporadic and irregular at the playful end; smooth, controlled, near-symmetrical at the serious end.
- **Amplitude** — how *grandiose* a given move is. Big travel, big scale, showy multi-property transforms vs. small, tight, minimal displacement.
- **Frequency & coverage** — *how much of the surface moves at all*, and how often. A playful brand may animate many things, including small ones that a serious brand would leave perfectly still.
- **What earns motion** — a playful brand will spend motion on delight for its own sake; a serious brand spends it almost exclusively on function (feedback, orientation, explanation).

Two poles to calibrate against — most brands sit somewhere between:

| | **Creative · fun · eccentric · playful** | **Serious · premium · precise** |
|---|---|---|
| Easing | springy, elastic, overshoot; irregular curves welcome | smooth, controlled, restrained; little or no overshoot |
| Amplitude | grandiose, generous travel and scale | subtle, tight, minimal |
| Frequency | frequent — including on small elements | sparing — reserved for moments that matter |
| Motive | delight is a legitimate reason on its own | motion mostly justifies itself functionally |
| Result | expressive, alive, characterful | slick, quiet, expensive |

**"Slick" is not the universal goal.** A playful brand rendered in tasteful, minimal, premium motion has been flattened into a generic one — that's a failure of appropriateness, exactly as `logo-design` treats a playful mark for a vault brand. Judge motion against *this brand's* emotional target, never against a house default.

### First Classify the Motion: Functional or Storytelling

Brand character doesn't apply evenly — **how much latitude a given animation gets depends on the job it's doing.** This is the balance to strike, and it's the first question, before the brand question:

- **Functional / UI motion** — it has a *job*: feedback on a press, orientation during a state change, showing cause and effect, revealing where something came from. **Be utilitarian, regardless of how playful the brand is.** Fast, unobtrusive, predictable, out of the way. The user has a goal; this motion serves it and disappears. A playful brand's save-confirmation still shouldn't bounce for 800ms.
- **Storytelling / delight motion** — a narrative beat, an expressive hero moment, a flourish whose purpose *is* the feeling: explaining the product's story, rewarding exploration, establishing character. **This is where brand latitude lives.** Be expressive, be on-brand, spend the amplitude — an eccentric brand should be genuinely eccentric here.

So the two axes compose: **functional motion converges** toward utilitarian across every brand; **expressive motion diverges** by brand. The more a motion is doing a job, the more utilitarian it should be; the more it's telling a story or creating delight, the more it should look like the brand and less like a convention.

And underneath both, a floor that never bends for personality: motion stays **hierarchical** (never uniform — see below), **decided** rather than defaulted, and bound by **usability and accessibility** — keyboard-initiated actions, high-frequency utility interactions, performance, and `prefers-reduced-motion`.

The ai-slop tropes are failures of *decision*, not of quantity — "fade-up on every element identically" is slop because it's undifferentiated and unchosen, not merely because it's a lot of motion. A playful brand moving many things, deliberately and hierarchically, is not slop. A restrained brand fading everything up the same way is.

## The Twelve Principles of Animation, Applied to UI

The canon comes from Disney (Thomas & Johnston, *The Illusion of Life*, 1981). They are the holy grail of animation for a reason — they describe how a *real physical thing* moves, and the whole game of good UI motion is to make flat rectangles obey the physics your body already knows. **They stack:** real interactions use several at once. Concrete, tool-agnostic code recipes for each live in [references/twelve-principles.md](references/twelve-principles.md).

1. **Squash & stretch** — weight and give. Scale/skew on hover, press, load. The lever for personality: a bouncy overshoot is playful; a slow settle is premium. Same element, different soul.
2. **Anticipation** — telegraph what interacting will *do*, not just that it's clickable. A hovered menu compresses toward where it'll collapse; an accordion chevron rotates toward where it'll open. A small wind-up before the action.
3. **Staging** — direct the eye to the one thing that matters. A gently looping CTA, or a sequenced load that lands attention on the primary action *last*. Motion as hierarchy.
4. **Straight-ahead vs. pose-to-pose** — you define the key states (from → to); the browser tweens between them. **Work backward from the resting state.** Scroll-linked sequences are pose-to-pose along a timeline.
5. **Follow-through & overlapping action** — parts move at different rates and settle *after* the lead. **This is the single biggest lever.** Elements enter together but staggered by small delays; trailing parts overshoot and settle. Amateur motion fires everything one-after-another like a slow slideshow; overlapping them, with slight staggered delays, is what makes a page feel expensive with almost no extra work.
6. **Slow in & slow out** — nothing in the physical world starts or stops instantly. Ease in and out. **Linear is the tell.** A thing accelerates, cruises, decelerates.
7. **Arc** — natural motion curves; it doesn't travel in straight lines. A menu that grows wide-then-tall traces a fake arc; a modal rising from a button follows a curved path, not a rigid vertical.
8. **Secondary action** — a supporting motion reinforces the main one. Hovering a delete icon also tints the modal it will affect; a pressed submit button spawns a spinner. It shows cause and effect — *this* thing affects *that* thing.
9. **Timing** — the number of frames sets speed, and speed sets mood. This is where "small fast / big slow" and "fast cheap / slow expensive" live. Timing alone, with nothing else changed, gives an element its character.
10. **Exaggeration** — push past literal realism; a perfect imitation of reality reads static and dull. A thicker-than-default underline, a head-shake on a disabled button, a photo that "develops" from B&W on hover. **It's easier to dial exaggeration back than to add it** — overshoot on purpose, then pull it to taste.
11. **Solid drawing** — respect 3D space, volume, and weight. Cards fan out and rotate as if held; elements set further back blur slightly and scale down; the front one scales toward the viewer; shadows stack in layers. Flat 2D given real dimension.
12. **Appeal** — charisma, magnetism, delight. Pleasing gradients, a soft glow on hover, an almost-imperceptible ambient parallax that invites exploration. The hardest one, because it's downstream of simply being a good designer. The whole point of it: make a person *want* to explore the page and stay.

## The UI-Native Toolkit — the Moves You Reach For

The twelve principles are the *physics and emotion* of motion. Alongside them, work with a second lens: the **UI-native techniques** — the practical move-set you actually deploy in an interface. Full catalog with recipes and the mapping back to the principles in [references/ui-motion-techniques.md](references/ui-motion-techniques.md) (source: [motion.zajno.com](https://motion.zajno.com/)):

1. **Easing** — the foundation; every expressive motion rides a curve (= slow-in/slow-out).
2. **Offset & delay** — staggered arrival as a hierarchy cue (= overlapping action, the biggest lever).
3. **Fade in/out** — but **never alone**; always pair opacity with a position or scale change, or it has no direction or weight.
4. **Transform & morph** — one shape continuously becomes another; the shared-element transition (card → page, icon → close). Continuity of focus, done with FLIP / View Transitions on `transform`, not `width`/`height`.
5. **Masking** — reveal content *within* a boundary (`clip-path`/`mask`) for a **directional** wipe instead of a flat fade.
6. **Dimension** — depth built from *relationships between layers* (layered shadow, perspective), not one element's shadow (= solid drawing).
7. **Parallax** — depth through differential layer speed; **restraint is the whole game** — subtle invites, heavy induces motion sickness. Kill it under reduced-motion.
8. **Zoom** — transition between states and depth, scaling from the correct `transform-origin` so it emanates from what the user acted on.

The distinction to hold: use the **principles** to decide what a motion should *feel* like and whether it earns its place; use the **techniques** to build it. Zajno's own thesis matches this skill's — **motion is a strategic tool to direct attention, not decoration.** (Note the real-time vs. non-real-time split: real-time motion is tied to the user's hand — hover, drag, scroll; non-real-time plays as a scripted response after an interaction.)

## General Motion Has a Ceiling — Signature Motion Is Content-Specific

The twelve principles, the techniques, and the production defaults get you **general motion**: a polished, functional, on-brand baseline applied to the standard UI patterns — reveals, hovers, presses, transitions, staggered entrances. Applied with restraint, this is genuinely good, and **for most surfaces it is the right target.** The site has to *work* first; general motion is what keeps movement in service of function instead of showing off.

But general motion has a ceiling. The motion that makes a surface feel *exciting* — memorable, unmistakably **this** product — is **content-specific**: ideas derived from what the content actually *is* and the story it tells, not a principle applied uniformly. An agent-log that streams in because the product is *an agent doing work*; a metric line that draws itself because the story is *growth*; a signature interaction built on the brand's own motif. These don't come from the principles alone — they come from **design direction**: the emotional target, the muses, the signature element, the real product narrative.

So calibrate to the brief, and be honest about the ceiling:

- **"Make it feel considered / functional"** → general motion **is** the target. Apply the principles with restraint and stop. This is the common case and a good outcome — don't manufacture excitement the brief didn't ask for.
- **"Make it exciting / memorable"** → general motion is the **floor, not the finish.** Reach for content-relative, bespoke ideas tied to the product's story and the brand's signature element — and that requires real design direction as *input* — `creative-direction` owns both the motion character and motif and the direction for bespoke assets. **Without that input, say so:** the honest ceiling of generic application is "good," not "exciting." Ask for the direction rather than faking depth the brief never supplied.

## Restraint — Not Everything Moves *Equally*

The amateur instinct (and the AI default) is to animate everything, **identically**. **Fade-up-on-scroll on every element regardless of importance, a looping gradient untethered to any story** — these are named tropes in `design-principles` → ai-slop for a reason: they are a default substituted for a decision. Note the failure is the *sameness*, not the amount; how much moves is the brand's dial to set (above).

Motion is subject to the same hierarchy as everything else. The elements that carry the message get the considered, expressive motion; supporting detail gets less or none. Uniform motion *flattens* hierarchy exactly the way uniform type weight does. If every section fades up the same way, nothing is emphasized — you've added movement and subtracted meaning.

And the strongest form of restraint: **sometimes the best animation is no animation** (Emil Kowalski — [references/practical-tips.md](references/practical-tips.md)). Motion must earn its place by explaining, giving feedback, or delighting; on frequently-repeated interactions it does the opposite — first-time delight curdles into friction and the interface feels *slower*. Two rules follow:

- **Never animate keyboard-initiated actions.** Arrow-keying through a list, menu, or command palette must be instant; an animated selection feels slow and disconnected from the key press.
- **Strip animation (and gratuitous hover states) from high-frequency actions** — anything a user does dozens of times a day. Animate the rare and the explanatory; get out of the way everywhere else.

## The Motion Floor — the Craft Beneath the Principles

Because this skill ships real code, there is a non-negotiable technical floor beneath the twelve principles. Full tokens and recipes in [references/motion-floor.md](references/motion-floor.md):

- **A named easing set, never raw `linear` or the same `ease` everywhere.** Define a small system of curves (standard, entrance, exit, and an overshoot for the springy work) as `cubic-bezier`s and use them by role.
- **A duration scale mapped to the emotion lever** — micro-feedback (hover/press) fast, standard transitions medium, expressive "expensive" moments slow, ambient loops slower still. Pick durations from the scale, don't eyeball a new one each time.
- **Animate compositor-friendly properties only — `transform` and `opacity` (and `filter` with care).** Animating `width`/`height`/`top`/`left`/`box-shadow` triggers layout/paint and causes jank; that jank is itself a "cheap" tell. This is the craft `web-design`'s light floor points here for.
- **`prefers-reduced-motion: reduce` is non-negotiable.** Provide a reduced path — opacity-only or instant — for every non-trivial animation. Motion sickness and vestibular disorders are real; a beautiful animation that can't be turned down is a defect, not a flourish.
- **Stagger with a consistent step** (an index custom property or incremental delay), small enough to overlap, not so large it becomes a slideshow.
- **Use CSS for simple state motion; reach for GSAP when it gets complex.** Hover, focus, press, and single-property reveals belong in CSS — don't add a library for what the platform does natively. For **smooth, choreographed, timeline-based** motion, **GSAP is the best tool available** and now fully free, all plugins included: **ScrollTrigger** (scroll-driven sequences and pinning), **SplitText** (staggered word/line reveals), **Flip** (shared-element/layout transitions — the morph technique). Its timelines make overlapping and staggering far easier to control than hand-tuned delay chains, and its interpolation is noticeably smoother on demanding sequences. Details in [references/motion-floor.md](references/motion-floor.md).

**Production defaults** — the specific numbers that read polished, from Emil Kowalski ([references/practical-tips.md](references/practical-tips.md)): **`ease-out` is the workhorse** for enter and exit (responsiveness beats physical purity; a custom curve, since the CSS built-in is too weak); **UI transitions stay under ~300ms** (125/180/300ms are the effective band; the longer expressive durations are reserved for rare hero moments); **scale buttons to `0.97` on `:active`**; **start entrances at `~0.9`, never `scale(0)`** (which looks like it materializes from nothing); **make popovers/zoom origin-aware** (`transform-origin` at the trigger, not center); and **a touch of `blur(2px)`** bridges a transition that still feels abrupt.

## Validate Before You Ship

Judge motion the way `design-principles` says to judge any work — **adversarially, on the rendered, moving page, not in your head.** Static screenshots cannot audit motion; you have to watch it.

- **Does it convey the intended feeling?** Play it back. Does the timing/easing match the brand's emotional target, or did you default to a generic ease? **Check the calibration, not just the curves:** if the brand is playful, is the motion actually *expressive* — or did you quietly render it slick and premium like everything else?
- **Is it hierarchical, or uniform?** List what moves and why. If the answer is "everything, the same way," that's ai-slop — cut it back to what carries meaning.
- **Overlap check.** Do grouped elements enter one-after-another (amateur) or overlapping-and-staggered (expensive)? Fix the sequence.
- **Linear check.** Is anything still moving on `linear` or an unconsidered default ease? Assign it a curve from the system.
- **Performance check.** Is anything animating layout-triggering properties? Move it to `transform`/`opacity`. Watch for jank on a mid-tier device, not just your machine.
- **Reduced-motion check.** Toggle `prefers-reduced-motion` and confirm the page is calm and usable, not broken.

## The Deliverable

- **The motion, in the shipped code** — transitions, keyframes, scroll/hover/press behavior applied to the real artifact, in the project's stack (CSS transitions & `@keyframes`, CSS scroll-driven animations, or a JS motion library / IntersectionObserver where the interaction genuinely needs it — tool-agnostic, whatever the project already uses).
- **Append the "Motion System — as built" section of `.agents/design.md`** (the living record — see `creative-direction` → design-doc-template.md): the easing tokens, the duration scale, the stagger step, the reduced-motion rule, and the signature moves as shipped — dated — so later work and other Application skills inherit the system instead of re-deriving it. This extends the directional Motion note `creative-direction` wrote; reference it, don't duplicate it.

## Non-Negotiables

- [ ] Front-door diagnosis run: surface is structurally sound and the system's motion character is settled — otherwise routed back (`web-design` / `creative-direction`)
- [ ] Motion tied to the brand's **emotional target**, not a generic default — the feeling chosen before the easing
- [ ] **Each motion classified by role first** — functional/UI motion kept utilitarian regardless of brand; storytelling/delight motion is where brand latitude is spent
- [ ] **Motion character calibrated at the system level** — easing personality, amplitude, frequency/coverage, and what earns motion, all set from the brand (playful ≠ premium; "slick" is not the universal goal)
- [ ] Motion is **hierarchical**, not uniform — what moves and why is a short defensible list, never "everything, the same way"
- [ ] Grouped elements **overlap and stagger**; nothing fires as a one-after-another slideshow
- [ ] A **named easing system** in use — no raw `linear`, no single `ease` on everything
- [ ] Durations pulled from a **scale mapped to the emotion lever** (small/fast/cheap ↔ big/slow/expensive), not eyeballed per element
- [ ] Animations run on **`transform`/`opacity`** (compositor), not layout-triggering properties
- [ ] **`prefers-reduced-motion`** honored with a reduced path for every non-trivial animation
- [ ] **`ease-out` is the default** curve (custom, not the weak CSS built-in); UI transitions **under ~300ms** unless a rare, deliberate expressive moment
- [ ] Entrances start at **~0.9, not `scale(0)`**; buttons scale to `0.97` on press; popovers/zoom are **origin-aware** (`transform-origin` at the trigger)
- [ ] **Keyboard-initiated actions are never animated**; high-frequency actions stripped of gratuitous motion/hover (sometimes the best animation is none)
- [ ] Validated on the **rendered, moving page** — played back, not judged from static screenshots

## Related Skills

- `design-principles` — the craft beliefs this skill applies in the time dimension (hierarchy, restraint, emotion before execution, ai-slop's Motion tropes)
- `creative-direction` — defines the brand's motion character as part of the visual system; route back for Revolution / heavy Evolution
- `web-design` — ships the surface with a light motion floor and defers expressive motion craft to here; the most common upstream skill
- `collateral-design` — sibling Application skill for fixed formats; motion for video/social ads lives alongside it
- `brand` — the audit whose emotional target sets the feeling motion must produce
- `design-critique` *(planned — not yet shipped)* — will judge the shipped motion against the emotional target and the latitude
- reference: the twelve principles ([references/twelve-principles.md](references/twelve-principles.md)), the UI-native technique toolkit ([references/ui-motion-techniques.md](references/ui-motion-techniques.md), from [motion.zajno.com](https://motion.zajno.com/)), the technical floor ([references/motion-floor.md](references/motion-floor.md)), and Emil Kowalski's production defaults + the case for restraint ([references/practical-tips.md](references/practical-tips.md))
