---
name: charles-ux-animation
description: "The 20 principles of UX and animation, extended with Emil Kowalski's animation rules, Interface Craft's motion techniques and more laws of UX, as one procedure for building or reviewing how an interface moves, responds and gets people through a task. Use when adding or reviewing animation, transitions, gestures, micro-interactions, loading and optimistic states, feedback, targets, menus, forms, onboarding or multi-step flows. Triggers on: animate, motion, transition, easing, duration, spring, bounce, stagger, enter, exit, modal, drawer, popover, tooltip, toast, icon swap, press, hover, drag, rubber band, arc, anticipation, squash and stretch, follow-through, compound motion, storyboard, reduced motion, jank, feels slow, optimistic UI, hit area, Fitts's law, Hick's law, Miller's law, Doherty threshold, Postel's law, Jakob's law, proximity, similarity, Von Restorff, serial position, peak-end, Zeigarnik, goal gradient, Tesler's law, Parkinson's law, Occam's razor, Pareto, progressive disclosure, defaults, undo."
---

# UX & Animation

From Charles Liu's "20 Principles of UX & Animation" reel, extended with Emil Kowalski's rules for interface animation, the motion techniques in Josh Puckett's Interface Craft, and more of the laws of UX. Built on Disney's 12 principles of animation (Frank Thomas and Ollie Johnston, *The Illusion of Life*), Raphael Salaja's userinterface.wiki and Jon Yablonski's Laws of UX.

Every interaction answers five questions, in this order: should it move, where should the eye go, how should it move, can people find it, hit it and choose it, and can they finish. Walk them in that order every time. A later answer never rescues an earlier one: the perfect curve on an animation that shouldn't exist is still wrong.

## Run it

1. **Match the stack.** Find what the project already animates with (CSS transitions, Tailwind, Motion as `motion` or `framer-motion`, React Spring, WAAPI) and write in that. State changes stay in CSS transitions. If Motion is installed, use it only for what CSS can't do: animating an element out as it unmounts, layout changes, and springs that follow a finger. Never add a library for what a CSS transition does, and never hand-roll a spring where Motion is installed. Why: two systems animating the same kind of change drift apart in timing and in how they handle interruption.
2. **List the interactions** in scope. For each, write down what triggers it (pointer, touch, keyboard, network, scroll), how often one person fires it, and what it has to tell them. Then cut, or in a review flag, every element and step that doesn't serve the task (Occam's razor, question 5) before polishing anything. Why: restyling something that's about to be deleted is wasted work.
3. **Walk questions 1–5** below, question by question, checking every interaction against each rule. Each subsection says when it applies; skip it when nothing in scope can trigger it (if nothing travels across the screen, skip Arcs).
4. **Name the numbers.** Durations, curves and springs live in named tokens at the top of the file or in the theme, and every animation uses them. A sequence of three or more stages gets a storyboard: a comment listing when each stage starts, a `TIMING` object, and one config object per element ([storyboards](references/techniques.md#storyboards)). When you can run the app, tune the values live (a dev-only control panel), then hard-code what works. Why: a number nobody can find is a number nobody tunes.
5. **Verify** with the checks at the end.

Recipes with exact values for modals, drawers, popovers, tooltips, toasts, entrances, exits, expanders, icon swaps, async buttons, numbers, sliders and carousels are in [references/recipes.md](references/recipes.md), with code wherever a value isn't enough. Curves, springs, interruptibility, arcs, mapping one value to another, rubber banding, loops, masks, cross-fades, storyboards, timelines and performance are in [references/techniques.md](references/techniques.md). Both files open with a list of their sections; read the section a rule points to.

**Reviewing instead of building?** Open the report with the interaction list from step 2. Then write one table row per finding: severity, principle, where (file and line, or frame), before, after. Severity is **broken** (a wrong result, lost input, a blocked or skipped step), **friction** (slower or more confusing than it needs to be) or **polish**. Sort by severity, then by the five questions; a Verify finding goes under the question it serves (reduced motion and animated properties under 3). Bugs no principle covers go in a list after the table.

## 1. Should it move?

### Frequency of use

```
How often will one person trigger this?
├── Many times a session, or from the keyboard (shortcuts, arrow keys, ⌘K, tabs, focus moving)
│     → no transition. The new state shows on the next frame.
├── A few times a session (menu, popover, modal, drawer, toast, saving a form)
│     → animate, within the timing table in question 3.
└── Rarely: a milestone the person won't repeat this session (onboarding, a first success, finishing a big task)
      → may be choreographed: each move up to 500ms, the whole sequence up to about 2.5s.

Then: does the motion answer a question? (Where did this come from? Did my action register? What changed? What caused it?)
├── No  → cut it.
└── Yes → keep it, and make the motion say the answer (question 3, "Make it mean something").
```

Press and hover feedback is exempt: it keeps its 100–150ms transition at every frequency, because it's the response itself. When hover and a keyboard highlight share a style, put the transition on the hover rule only, so the keys stay instant. Marketing pages can run longer and showier; product UI stays inside the timing table. Why: the hundredth time someone sees an animation, it stops informing and starts delaying. Keyboard users act faster than any transition, so a highlight that glides falls behind the keys.

Nothing that is already at rest when the page first paints plays an entrance: motion is for the changes people cause afterward. In Motion, set `initial={false}` on `AnimatePresence` around toggles, tabs and icon swaps, and never around a first-run entrance whose whole point is to play.

### Doherty threshold

People stay in flow when the interface answers within 400ms.

- The pressed state shows on the same frame as the input, never after a network round trip.
- Update optimistically when an action almost never fails: like, favorite, toggle, reorder, mark as read, send a message, remove an item. The change starts on the same frame (a motion that starts at once counts), and rolls back with a message if the server refuses.
- In a multi-step flow, a step that passes validation in the browser saves in the background while people move on, and a failed save shows a toast with Retry that keeps their new place. The exception is a step whose result the next one needs (shipping and tax depend on the saved address): it waits like a final submit.
- Everything else, including every final submit (paying, placing an order): disable the trigger at once against double submits, and show "Saving…" or a spinner only after 300ms, held at least 500ms once shown ([async buttons](references/recipes.md#async-buttons)). Why: fast responses never flash a spinner, and slow ones don't flicker.
- Past 1s, if the result appears somewhere (a list, a page), show a skeleton the size of the content there. If it doesn't, the trigger's pending state is enough.
- Reads show what the person saw last time, from a local cache, then reconcile. Never render a default that flips when the fetch lands, like a bookmark icon jumping from empty to filled.
- Work that takes seconds and can't be skipped (a first import, processing a file) runs in the background, or behind something worth watching, like an onboarding step that shows what the product does. Never a bare spinner. Why: a wait spent reading feels shorter than one spent watching something spin.

## 2. Where should the eye go?

- **Staging.** One primary motion at a time: the element the person touched, or the one that answers them. Everything else holds still or recedes (a 40–50% black scrim behind an expanded card, siblings at 0.5 opacity). When one action sets off several motions, chain them, each starting as the one before lands (the image reaches the cart, then the badge bumps); never run them side by side. Why: the eye follows one thing; two motions at once split attention and neither lands.
- **Stagger.** Only for content that arrives on its own (a list loading in, a page's sections). Content riding in on a container that's already moving (a drawer's rows, a modal's body) arrives with it, in one piece. Copies of one element (list rows, cards, menu items) enter 30–50ms apart, and only the first 6 do; the rest arrive with the sixth. Distinct pieces of a section (the heading, then the copy, then the actions) enter 80–100ms apart. Never move a whole section as one block. Why: small offsets read as one gesture with an order, a block reads as a slide, and a stagger inside a moving container competes with the container.
- **Von Restorff effect.** One element per view breaks the pattern around it: the primary action, filled in the accent color. Never two. Pair the color with size, weight or position, because color alone fails people who can't see it. Motion is the strongest difference there is, so whatever moves gets noticed: spend it on the thing that matters. Why: people notice and remember the one item that differs, and two "different" items cancel each other out.
- **Serial position effect.** People remember the first and last items of a sequence best. Put the most important items at the ends (the first and last tabs, the top of a menu) and the least-used in the middle, and open every screen with what it's for. Why: attention dips in the middle.
- **Secondary action.** Only on top of a primary motion, never alone. It starts with the primary or up to 100ms after, ends within 150ms of it, and moves at most a third as much. Example: the check draws in, then a ring scales from 1 to 1.4 while fading out. Only in the "rarely" branch of question 1. Why: it backs the main action up; as soon as it's as big or as long, it competes with it.
- **Exaggeration.** Only where a moment must register: an error on submit, a failed attempt (wrong password, declined card), a first success. An error shake moves the field that's wrong through translateX 0, −10, 10, −6, 6, −3, 0px over 360ms, puts focus there, and shows the message beside it. Never on blur, and never on neutral transitions like opening a menu or switching tabs. Why: exaggeration is a volume knob; if everything is loud, nothing is.

## 3. How should it move?

### Timing

| What | Duration |
| --- | --- |
| Press, hover, color | 100–150ms |
| Tooltip | 125ms |
| Dropdown, popover | 150–250ms |
| Modal, drawer, sheet, toast | 200–300ms |
| Moving or resizing in place (a progress fill, rows closing a gap, a reorder, an expander) | 200–300ms |
| Page transition, shared-element move, flip, something flying to a new place | 300–400ms |
| Rare, choreographed moment | up to 500ms per move |

Menus, popovers, modals, drawers and toasts take 300ms or less; only the spatial moves take longer. Within a range, larger elements and longer distances take the longer end. If it feels slow, cut the duration before touching the curve. Why: duration is the feel; the same move feels sluggish at 500ms and instant at 150ms.

**Exits** are 20–30% shorter than their entrance, and quieter: a fade with at most a small move, either a nudge of 8–16px toward where the element is going or back to the scale it entered from, never its full height. The exception is something whose destination is the point (a drawer or sheet closing, a card swiped away): it leaves the way it came. Never an instant `display: none`, which loses where it went. Anything kept mounted so it can animate out is inert while closed (`pointer-events: none` and the `inert` attribute), so it can't catch clicks or focus. Why: by the time something leaves, attention has already moved on.

### Slow in and slow out

```
Follows a finger, or can be thrown or redirected mid-gesture (drag, swipe, sheet, slider, carousel)?
      → spring: Motion { type: "spring", duration: 0.5, bounce: 0 }.
        Bounce 0.1–0.3 only for physical, playful objects; never more.
Appearing (popover, menu, modal, toast, page)? → ease-out: cubic-bezier(0.32, 0.72, 0, 1)
Leaving?                                       → ease-in: cubic-bezier(0.55, 0, 1, 0.45), on the shorter exit duration
Moving or resizing while on screen?            → ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)
Hover or color?                                → ease, 150ms
Constant rate, where the motion is time itself (spinner, marquee, countdown, hold-to-confirm ring)? → linear
```

- Never ease-in for an entrance: the slow start reads as lag.
- Never the bare `ease-out` or `ease-in-out` keywords for anything that moves or scales: they're too weak to read as a decision. Use the curves above; [curves](references/techniques.md#curves) has softer and stronger ones.
- Never `transition: all`. Name each property.
- Anything that can be toggled or interrupted uses a CSS transition or a spring, which turns around from where the element is ([interruptibility](references/techniques.md#interruptibility)). Keyframes are only for one-shots nothing can interrupt: an entrance on first paint, a loader, a celebration.

Why: ease-out moves most at the start, so the response feels instant; ease-in gets out of the way at the end; real objects speed up and slow down, so linear only fits things that are time.

### Origin

Popovers, dropdowns and tooltips scale from their trigger, never from their center: `transform-origin: var(--radix-popper-transform-origin)` in Radix, `var(--transform-origin)` in Base UI, or the trigger's side set by hand. Anything that scales in starts at `scale(0.95)` (0.97 for small elements) with `opacity: 0`, never at `scale(0)`. Paired elements (modal and overlay, drawer and backdrop, tooltip and arrow) share one duration and one curve. Why: things grow out of what made them, real objects always have a shape, and two halves of one object on different clocks look broken.

### Arcs

When something travels between two points that differ on both axes by more than 40px (a product image flying to the cart, a thrown card, a floating button moving to a corner), move it on a curve that bulges 10–20% of the distance off the straight line ([code](references/techniques.md#arcs)). For depth, scale it up to at most 1.3 at the top of the arc and fade in a larger shadow with it, so it lifts off the page instead of sliding across it. Single-axis moves (drawers, list reorders) stay straight. Why: thrown and falling things travel in arcs, and a straight diagonal reads as mechanical.

### Anticipation

- A wind-up belongs to the "rarely" branch of question 1: before a launch or a flip the person sets off (confetti on a first success, a card sent off at the end of onboarding, a card turning over), move 5–10% of the travel the opposite way, or scale to 0.95, over 80–120ms, then go. Never before anything people do often, because the wind-up is added latency.
- The everyday form is the press. Buttons, icon buttons and chips scale to 0.96 on `:active` (never below 0.95) with a 150ms ease-out transition, so letting go mid-press glides back. Surfaces wider than 200px (cards, rows) change background on press and on hover instead of scaling, because 4% of a wide surface is a jump. Dense, high-frequency controls (toolbars, editor chrome) skip the scale, so give the button component an opt-out. Put the scale on a wrapper when the element already has a transform. Why: it confirms the press before the result arrives.
- Hover motion runs only where a real pointer hovers: wrap it in `@media (hover: hover) and (pointer: fine)` (Tailwind v4's `hover:` variant already checks `hover: hover`). When a hover moves the element out from under the cursor, it flickers, so animate a child and keep the parent's hover area still. Why: touch screens fire hover on tap.

### Follow through

When a container stops, the non-text parts inside it settle a beat later: a toast's icon, a sheet's grabber, a dragged card's image. Drive them with a softer spring than the parent (damping ratio 0.7–0.85) or start them 20–40ms after it, with overshoot under 4% of the travel. Text never lags or wobbles, so an all-text panel arrives in one piece, and nothing in the "many times" branch of question 1 gets follow-through. In a rare moment, the final settle of the hero object may rebound for up to 1s, because by then the person already knows what happened. Why: parts that all stop on the same frame read as one rigid sticker.

### Squash and stretch

Only for objects that behave physically: something that bounces, lands, or is dropped or caught (a dock icon, a badge landing, a drag-and-drop drop, an envelope that hops). Use it at an impact, or as a springboard: a squash just before a jump stores the energy that launches the next move. Squash the shape, never the text in it. Stretch along the direction of travel at speed and squash on impact, by at most 15%, recovering within 150–200ms, and keep the volume: scaleX × scaleY ≈ 1 (scaleY 0.87 with scaleX 1.15). Never on inputs, layout containers, or anything read while it moves. Why: it shows weight and give; on rigid UI it looks broken.

### Pose to pose

Define the states (closed and open, idle and pressed and done) or keyframes at explicit offsets, and let the engine interpolate between them. Write frame-by-frame code (straight ahead) only for motion driven live by input: drag, scroll, cursor. Why: poses make motion predictable and tunable in one place.

### Solid drawing

Anything that flips, tilts or turns gets real depth:

```css
.scene { perspective: 800px; }   /* 600–1000px at card size; lower values exaggerate the depth */
.card  { transform-style: preserve-3d; transition: transform 400ms cubic-bezier(0.77, 0, 0.175, 1); }
.face  { backface-visibility: hidden; }
.back, .card.flipped { transform: rotateY(180deg); }
```

Press feedback goes on `.scene`, so it never overwrites the rotation. Light it: an overlay that darkens the face turning away, up to 30% black at 90°, and a shadow that shrinks as the object lifts. Never fake a flip with `scaleX`. In a 3D carousel, leave more space around the center item than between the items behind it, so rotated items never cut through each other, even on a slow drag. Why: without `perspective`, a rotation renders as a flat squeeze.

### Make it mean something

Motion carries the meaning of the change, so it needs no words:

- A changing number rolls only the digits that change, upward when it grows and downward when it shrinks, in `tabular-nums` so nothing shifts.
- An item leaves toward where it went: a deleted row collapses, an archived one slides toward the archive, a sent message rises.
- Something drawn as a physical object (a card, a letter, an envelope, a ticket) moves like one: it never fades in or out while in view, never passes through another object, and clears its container's edges before it moves toward the viewer.
- Finished things recede: a completed task collapses, fades back or stacks away, so what's left stands out.
- A hint shows the gesture instead of describing it: a looping hand that swipes, drags or scratches, gone the moment the person hovers or touches.

Why: motion that matches the metaphor reads at once, and motion that's only decoration has to earn a reason it doesn't have.

### Replacements

When one element replaces another in place (a label becomes a spinner, copy becomes a check, one card replaces the next), animate both at once; never wait for the old one to finish leaving. Stack them in the same spot (one grid cell) so nothing around them shifts. In Motion, `AnimatePresence mode="popLayout"` takes a leaving element out of layout at once, so siblings close the gap while it exits. Icons swap through a deep scale (0.3 → 1), opacity and a 3px blur on a spring with no bounce ([icon swaps](references/recipes.md#icon-swaps)). Something that's traveling or changing shape stays one element for the whole move; never swap it for another element mid-move. Why: a sequential swap doubles the wait for no new information, and a swap mid-move twitches.

### Interruptible

Never block input while something animates. When the person changes their mind halfway, the motion turns around from where it is, at the speed it has. Clicks assist: snap to the likely value (a slider click lands on the nearest 10%) and spring there. Drags are direct: the element stays 1:1 under the finger with no easing, and a spring takes over on release, carrying the release velocity. At a bound, rubber-band with diminishing returns after a small dead zone, never a hard stop ([rubber banding](references/techniques.md#rubber-banding)). Why: an interface that makes you wait for its animation is slower than one with none, and people overshoot on purpose to reach an end.

### Compound motion and loops

Only for ambient objects and rare moments (a hero object, an idle hint, a floating badge): layer a small loop on top of the main motion, a y drift within ±10px and a 1–3% scale, out of phase with each other. Drive every loop with a sine wave rather than keyframes, and offset each item's phase rather than delaying it ([loops](references/techniques.md#loops)). Pause loops while they're off screen. Never loop anything people are reading or aiming at. Why: a simple loop stacked on simple motion looks alive, and a keyframe loop shows a seam where it turns around.

## 4. Can people find it, hit it and choose it?

### Law of proximity

Space is the first grouping signal people read. Things that belong together sit closer to each other than to anything else: the gap between groups is at least twice the gap inside one, and a label sits closer to its own field than to the field above. Why: distance reads as relationship before a single word does.

### Law of similarity

Elements that look alike are read as working alike. Give each role one look and keep it everywhere: every link styled the same, every destructive action in one style, every card of a type with the same anatomy. Things that work differently look different. Motion follows the same rule: elements that behave alike share duration and curve tokens. Why: a pattern learned once works everywhere, and an odd one out reads as a bug.

### Uniform connectedness

A shared container or a connecting line groups more strongly than proximity or similarity. Tie a label, its value and its action together with one background or border, join the steps of a stepper or timeline with a line, and never put unrelated items in one container. Why: an edge around things says "these are one" before anything else does.

### Law of Prägnanz

People read a layout in its simplest possible form. Before adding a border, divider, card or icon, check whether spacing and alignment already show the structure; if they do, leave it out. Use the fewest alignment lines, sizes and colors that do the job, and simple, regular shapes. Why: every extra container is one more thing to parse before the content.

### Fitts's law

The bigger and closer a target, the faster it's hit. The primary action is the largest target and sits nearest where the pointer or thumb already is: beside the field it submits, at the bottom of the screen on mobile. Destructive actions sit away from the primary action, so a miss can't trigger them. In a confirmation for a destructive action, Cancel takes the default focus, and the destructive button is never larger than Cancel and names the verb ("Delete address"). Targets are at least 44×44px on touch and 40×40px with a pointer.

### Hit area

When the visual has to stay small (16–24px icons, close buttons, checkboxes, slider thumbs), make the clickable zone bigger than it looks, never the visual:

```css
.icon-button { position: relative; }
.icon-button::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: max(100%, 44px);   /* 40px where the only input is a mouse */
  height: max(100%, 44px);
  translate: -50% -50%;
}
```

Where two zones would overlap, shrink both equally, never below 24×24px (the WCAG 2.2 floor); if they'd still overlap, space the items apart or move one action elsewhere. Icon buttons inside a clickable card sit above the card's link and stop the click from reaching it. When a whole row acts as one link, the whole row is the target. Why: people aim at the center and land near it, and a zone bigger than the visual absorbs the miss.

### Hick's law

Decision time grows with the number of choices. For options people weigh against each other (plans, sort orders, settings, onboarding choices), cut the ones few people pick, and keep each group to 7 or fewer under a heading, so people pick a group and then an item. Put search first when people already know what they want (command palettes, country and font pickers): that's a lookup, and search makes length irrelevant. One decision per step in onboarding and checkout. Mark one option as recommended only when you have a real recommendation, and never pre-select anything that costs money or shares data.

### Miller's law

Working memory holds a handful of items, so chunk anything people read, compare or type that runs past 5 units: card numbers by scheme (4-4-4-4, Amex 4-6-5), phone numbers in their national format, one-time codes as 3 + 3, long forms in sections of at most 5 fields, top-level navigation at 7 items or fewer. Fixed-pattern numbers format as people type. Never make people carry something from one screen to the next; show it where it's needed. Why: a chunk counts as one item, so 16 digits become 4.

### Jakob's law

People spend most of their time in other products, and expect yours to work the same way. Keep the conventions: the logo top-left links home; account and cart sit top-right; ⌘K or Ctrl+K opens the command palette; Esc closes the top layer; Enter submits a single-field form; swiping from the left edge goes back on iOS; a magnifier means search and a gear means settings; links look like links. Put the novelty in the content and the craft, not in where things live or what gestures do. If you must break a convention, teach it the first time and keep the conventional path working.

## 5. Can people finish?

### Tesler's law

Every task carries complexity that can't be removed, only moved, so the product takes it on. Pre-fill what you can infer (the country from the account or locale, the city from the postcode, the name and email from the account), default every choice to what most people pick, and never ask for something you already know. When an option costs extra or shares data, the default is the free, private one (standard delivery, sharing off). Why: whatever the product doesn't absorb, every person pays for, every time.

### Parkinson's law

A task expands to fill the time it's given, so shrink the time. Turn on autofill (`autocomplete` attributes), remember last-used values, offer the common answer as one tap, and keep optional fields off the main path. Say up front how long a long task takes ("About 2 minutes"). Why: every extra field is an invitation to deliberate.

### Occam's razor and progressive disclosure

Of two designs that both work, ship the one with fewer parts, and delete every element and step that doesn't serve the task. This is the cut in step 2 of "Run it", done before any polish. Then reveal complexity gradually: show the options most people need, put the rest behind "More options" or an expander, and show a follow-up field only once the answer that needs it is given. Never hide something most visits need. Why: complexity shown before it's needed is complexity everyone pays for.

### Pareto principle

Most use comes from a few features. Find them (from usage data, or from the product's core task) and give them the prime spots, the defaults and the first polish; move the rest one level down. Why: polish spread evenly is mostly spent where few people look.

### Postel's law

Accept messy input and give back one clean format. A date people choose from a range you know (a delivery day, a booking, a meeting) uses a picker limited to valid days. Anything people type from what they already know (a birthday, a date from a document, a phone or card number, an email) is a text field that parses every common form: dates ("15 jan 2026", "2026-01-15", "1/15/26" in the person's locale), phone and card numbers with spaces, dashes or brackets, emails with stray spaces or capitals, pasted values with trailing whitespace. Free-form values like dates are parsed on blur and shown back normalized ("Thursday, 15 January 2026"). Validate on blur or submit, never while someone is still typing a field for the first time; once an error shows, re-check on every keystroke so it clears the moment it's fixed. When parsing truly fails, keep what they typed and name the format that works, with an example. Never reject input you could have parsed. Why: a strict format moves your work onto the person.

### Errors: prevent, then recover

- **Prevent.** Constrain input to what's valid (a picker limited to valid days, a stepper for counts), disable impossible options with the reason beside them, and show the expected format before people type, not after they fail. Confirm only destructive actions that can't be undone, and name the action on the button ("Delete 3 files").
- **Recover.** Anything reversible gets Undo instead of a confirmation: a toast with Undo for at least 5 seconds after a delete, archive or send. The item leaves the screen at once, and the request goes out when the Undo window closes (or when the page is hidden), so Undo only has to put it back. When something fails, keep everything the person entered, and say what happened and how to fix it in plain words, beside the field or action that failed.

Why: people click through a confirmation dialog by habit, so it prevents nothing, and undo still works after the mistake.

### Zeigarnik effect and goal gradient

Unfinished tasks stay on people's minds, and people speed up as a goal gets close. Show where they are and what's left ("Step 2 of 4", "3 fields left", a checklist with finished items ticked), save partial progress, and offer to continue where they stopped. Count work already done: a step the person finished (creating the account) shows as done, and progress never reads 0% once they've done something. A step progress bar grows from its last value with `scaleX` from the left edge (never `width`), on the ease-in-out curve, and never jumps backward. Why: visible remaining work pulls people back, and a goal that looks close gets finished.

### Peak-end rule

People judge an experience by its most intense moment and by its end. End every flow on a confirmation that says what happened and what comes next, never on a bare redirect. Save celebration for real milestones (the "rarely" branch of question 1); routine completions get a quiet confirmation. Fix the worst moment (an error, a long wait) before polishing an average one. Why: the end is what people remember and tell others about.

## Verify

Run every check you can. In a code-only review, don't build a harness: after the findings, list the checks you couldn't run and what each would catch.

- [ ] **Scrub** every animation at 10% speed (DevTools → Animations, or a frame-by-frame capture). The first frame responds, the last frame settles with no pop, and only one thing leads at a time.
- [ ] **Interrupt** each one halfway. It turns around from where it is.
- [ ] **Hammer the keyboard** through every list and shortcut. Nothing lags behind the keys.
- [ ] **Slow the network** to 1s or more. Presses register at once, nothing flashes a spinner under 300ms, and slow results show progress where they'll land.
- [ ] **Tap the edges** of every small target on a phone. No hover motion fires on tap.
- [ ] **Paste messy input** into every field, and **force each failure** (offline, a server error, invalid data). The person keeps what they typed and can recover.
- [ ] **Finish every flow** once as a new person. Defaults are filled in, progress is visible, and the last screen says what happened.
- [ ] **Reduced motion** (`prefers-reduced-motion: reduce`; `useReducedMotion()` in Motion): every animation is off, fades included, and every end state and every piece of information is the same as with motion on. The one exception is an indicator that work is still happening (a spinner, a progress bar), which keeps moving, because a frozen spinner looks like a hang.
- [ ] **Switch the theme.** No color transitions fire across the page.
- [ ] **Properties:** movement and size changes use only `transform` and `opacity`; color and `stroke-dashoffset` are fine, and blur stays under 20px. Never animate width, height, top, left or margin: collapse a removed row with FLIP (measure, then animate the transform), and open an expander with the grid-rows recipe ([expanders](references/recipes.md#expanders)). An element that shifts 1px at the start or end of a move gets `will-change: transform`.
- [ ] **Tenth use:** once everything else is done, run each animation at full speed as someone seeing it for the tenth time today. Cut or shorten the one that starts to feel slow.

**Appeal** is what you get when everything above holds. You can't add it at the end, only fail to lose it. Final pass: one set of named curves and durations used everywhere; every state designed (empty, loading, error, success, offline); nothing appears from nothing.
