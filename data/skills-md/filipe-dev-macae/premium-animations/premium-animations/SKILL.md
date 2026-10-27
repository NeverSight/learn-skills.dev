---
name: premium-animations
description: Use when designing, building, reviewing, or refining premium frontend interfaces with purposeful motion. Covers React, Next.js, GSAP, Motion, Lenis, ScrollTrigger, SplitType, SVG animation, Three.js, React Three Fiber, layout polish, UX hierarchy, micro-interactions, reduced-motion support, and performance for landing pages, SaaS, dashboards, portfolios, ecommerce, pricing, FAQ, heroes, navbars, cards, forms, CTAs, timelines, feature grids, and bento grids.
license: MIT
compatibility: Designed for Magic Patterns and Agent Skills-compatible coding agents.
metadata:
  author: filipe-dev-macae
  version: "1.0.0"
---

# Premium Animations

## Purpose

1. Build interfaces that feel premium, calm, intentional, and production-ready.
2. Use motion as part of the product experience, not decoration added at the end.
3. Prefer real implementation details over vague design language.
4. Produce React and Next.js interfaces that could plausibly ship for a serious brand.
5. Help the agent choose between GSAP, Motion, Lenis, SVG animation, and Three.js.
6. Avoid copying proprietary designs from Apple, Stripe, Linear, Vercel, Raycast, Framer, Supabase, Clerk, Notion, Figma, Aceternity UI, Magic UI, Origin UI, or Awwwards projects.
7. Learn from those references at the level of restraint, hierarchy, polish, timing, clarity, and technical craft.
8. Never imitate protected brand assets, exact layouts, exact copy, proprietary illustrations, or recognizable visual systems.

## Activation

1. Use this skill when the user asks for premium UI, world-class UI, polished UI, modern UI, animated UI, landing page design, SaaS design, dashboard design, portfolio design, ecommerce design, app shell design, interaction design, scroll animation, motion design, Framer Motion, Motion, GSAP, Lenis, ScrollTrigger, SplitType, SVG animation, Three.js, React Three Fiber, page transitions, micro-interactions, or high-end web experience.
2. Use this skill when the user complains that a design feels generic, static, flat, boring, too template-like, too AI-generated, too childish, too flashy, or not premium.
3. Use this skill when improving navbar, hero, pricing, FAQ, testimonials, forms, feature sections, bento grids, timelines, cards, dashboards, modals, accordions, loading states, empty states, or CTAs.
4. Use this skill for frontend work only. Do not use it for backend-only tasks unless the backend task directly supports a motion or UI feature.
5. If a request is primarily about accessibility, performance, responsiveness, or design QA on an animated interface, use this skill.

## Required First Steps

1. Inspect the current project before proposing new libraries.
2. Identify the framework, styling system, component library, router, and animation dependencies already installed.
3. Prefer existing conventions when they are strong enough.
4. If no animation library is installed, recommend the smallest library set that matches the actual interaction.
5. If the user wants Magic Patterns output, optimize for clear promptable behavior and production-ready React patterns.
6. If generating code, include reduced-motion behavior from the start.
7. If editing an existing project, read representative layout, theme, and component files before changing UI.
8. If building from scratch, define visual direction, typography, color strategy, spacing scale, motion hierarchy, and interaction states before code.

## Core Standard

1. The interface should look expensive without looking loud.
2. Every animation needs a job.
3. Every visual effect needs a reason.
4. Every component must remain usable without animation.
5. The static layout must be excellent before motion begins.
6. Motion should clarify hierarchy, causality, navigation, affordance, feedback, or emotional tone.
7. Avoid one-size-fits-all reveal animations across every section.
8. Avoid making every card float, every button glow, and every heading split into characters.
9. Use a small set of motion motifs and repeat them with disciplined variation.
10. Let restraint carry the premium feeling.

## Design Philosophy

1. Minimal does not mean empty.
2. Premium does not mean glass everywhere.
3. Elegant does not mean low contrast.
4. Confident does not mean oversized everything.
5. Large whitespace is useful only when information density is still intentional.
6. Typography should establish trust before effects begin.
7. Subtle motion beats spectacle unless spectacle is explicitly the product.
8. Never make the interface childish, gimmicky, chaotic, or toy-like.
9. Never use motion to compensate for weak layout.
10. Never hide weak content behind animation.

## Reference Inspirations

1. Apple: study spatial clarity, patient pacing, precise hierarchy, and material restraint.
2. Stripe: study systems thinking, diagrammatic clarity, dense information handled elegantly, and confident gradients used sparingly.
3. Linear: study product sharpness, quiet density, exact spacing, and useful keyboard-first interactions.
4. Vercel: study monochrome discipline, technical credibility, and fast transitions.
5. Raycast: study command surfaces, crisp contrast, and delightful but restrained micro-interactions.
6. Framer: study motion-native thinking, layout flow, and confident visual composition.
7. Supabase: study developer-facing clarity, product cards, code-adjacent UI, and balanced color.
8. Aceternity UI: study expressive interaction ideas, but reduce excess when shipping production pages.
9. Magic UI: study motion recipes, but make each one serve content.
10. Origin UI: study component craft and clean interaction states.
11. Clerk: study onboarding clarity, authentication flow polish, and form confidence.
12. Notion: study calm information architecture and approachable density.
13. Figma: study tool-like UI, collaboration affordances, and precise controls.
14. Awwwards: study ambition, but reject inaccessible, slow, or confusing execution.

## Never Copy

1. Do not reproduce proprietary layouts exactly.
2. Do not copy brand color systems exactly.
3. Do not copy product illustrations exactly.
4. Do not copy copywriting, icon sets, screenshots, demo data, or marketing claims.
5. Do not describe a design as being "Apple-style" or "Stripe-style" in visible UI copy.
6. Do not use inspiration brands as a substitute for a project-specific visual direction.
7. Do not create clone pages.
8. Do not embed unlicensed assets.
9. Do not recreate proprietary animations frame by frame.
10. Translate principles, not artifacts.

## Motion Library Selection

1. Prefer Motion for React component state.
2. Prefer Motion for layout animations.
3. Prefer Motion for shared layout transitions.
4. Prefer Motion for AnimatePresence.
5. Prefer Motion for hover, tap, drag, and gesture interactions.
6. Prefer Motion for variants and declarative component choreography.
7. Prefer Motion for `whileHover`, `whileTap`, and `whileInView`.
8. Prefer Motion when the animation belongs to component state and React lifecycle.
9. Prefer GSAP for complex sequences.
10. Prefer GSAP for hero entrance timelines.
11. Prefer GSAP for nested timelines.
12. Prefer GSAP for ScrollTrigger.
13. Prefer GSAP for SVG path drawing.
14. Prefer GSAP for SplitType text reveal.
15. Prefer GSAP for precise stagger control.
16. Prefer GSAP when animation needs imperative orchestration.
17. Prefer Lenis for smooth scrolling only when the page benefits from it.
18. Prefer ScrollTrigger for scroll-linked animations.
19. Prefer CSS transitions for simple hover states.
20. Prefer native CSS `scroll-timeline` only when browser support and project constraints allow it.
21. Prefer Three.js or React Three Fiber only when 3D is meaningful to the concept.
22. Do not add Three.js for a simple decorative background.
23. Do not add GSAP when Motion or CSS is enough.
24. Do not add Motion when CSS is enough.
25. Do not add Lenis to dashboards, forms, admin tools, or dense product UIs by default.

## GSAP Rules

1. Use GSAP when timing precision matters.
2. Use one top-level timeline for major sequences.
3. Use nested timelines for reusable motion phrases.
4. Keep timeline labels meaningful.
5. Use `gsap.context()` in React when wiring animations inside effects.
6. Revert GSAP contexts on cleanup.
7. Register plugins once at module scope or inside guarded client code.
8. Use `useLayoutEffect` or an isomorphic layout effect for measurements.
9. Avoid measuring repeatedly during animation.
10. Use `autoAlpha` when visibility and opacity must be coordinated.
11. Use transforms instead of layout properties.
12. Use `clearProps` when temporary animation styles should not linger.
13. Keep ScrollTrigger instances scoped and cleaned up.
14. Use `invalidateOnRefresh` when responsive measurements change.
15. Use `matchMedia()` for breakpoint-specific animation behavior.
16. Use `scrub` only when the scroll relationship should be direct.
17. Use non-scrubbed triggers for entrance moments.
18. Do not pin sections casually.
19. Pinning must serve storytelling, comparison, steps, or focused comprehension.
20. Keep pinned sections short enough to avoid scroll fatigue.
21. Never stack too many pinned sections.
22. Avoid `ScrollTrigger.refresh()` loops.
23. Refresh after fonts, images, or layout-changing content load.
24. Avoid animating thousands of SplitType characters.
25. Split words first; split characters only for short display lines.

## GSAP Timeline Pattern

1. Start with the final static composition.
2. Identify the first meaningful visual event.
3. Create a timeline with defaults.
4. Add labels for phases such as `intro`, `content`, `cta`, and `ambient`.
5. Use overlap syntax deliberately, such as `"<0.08"` or `"-=0.25"`.
6. Keep entrance duration around 0.6 to 1.2 seconds for hero content.
7. Keep micro-interactions around 0.12 to 0.28 seconds.
8. Keep section reveals around 0.45 to 0.9 seconds.
9. Use `power3.out`, `power4.out`, `expo.out`, or custom cubic curves.
10. Avoid bounce and elastic unless the brand genuinely supports play.

## Motion Rules

1. Use Motion for stateful UI.
2. Use `layout` for layout transitions that users need to understand.
3. Use `layoutId` for shared element transitions.
4. Use `AnimatePresence` for mount and unmount transitions.
5. Use variants for coordinated parent-child animation.
6. Keep variants named by meaning, not by implementation.
7. Good variant names include `hidden`, `visible`, `active`, `inactive`, `selected`, `collapsed`, and `expanded`.
8. Avoid deeply nested variant magic that future maintainers cannot follow.
9. Use `transition` objects consistently.
10. Use spring transitions for physical UI movement.
11. Use duration-based easing for opacity and reveal effects.
12. Use `whileHover` for buttons and cards only when the hover communicates affordance.
13. Use `whileTap` for tactile controls.
14. Use drag only when dragging is a real interaction.
15. Use `useReducedMotion()` and branch motion behavior.
16. Prefer stable keys for `AnimatePresence`.
17. Avoid layout animations on huge lists.
18. Avoid animating expensive shadows through Motion.
19. Use `LazyMotion` when bundle size matters.
20. Do not combine Motion and GSAP on the same property of the same element.

## Lenis Rules

1. Use Lenis for marketing pages, portfolios, editorial pages, and scroll-led experiences.
2. Avoid Lenis for dashboards, tables, admin panels, editors, forms, and productivity tools unless requested.
3. Always synchronize Lenis with ScrollTrigger when both are used.
4. Use a single Lenis instance per page.
5. Clean up Lenis on unmount.
6. Drive Lenis through `requestAnimationFrame`.
7. Do not create multiple RAF loops for the same scroll system.
8. Use `ScrollTrigger.update` on Lenis scroll events.
9. Use `gsap.ticker.add` only when deliberately integrating GSAP ticker.
10. Disable GSAP lag smoothing when appropriate for Lenis synchronization.
11. Keep smooth scroll subtle.
12. Do not make scroll feel drunk, delayed, or detached from input.
13. Respect anchor links and focus movement.
14. Respect keyboard navigation.
15. Respect reduced motion by disabling or simplifying smooth scroll.

## Lenis ScrollTrigger Integration

1. Create Lenis in a client-only component.
2. Subscribe `lenis.on("scroll", ScrollTrigger.update)`.
3. Add a RAF loop that calls `lenis.raf(time)`.
4. Cancel the RAF loop during cleanup.
5. Destroy the Lenis instance during cleanup.
6. Register ScrollTrigger before creating triggers.
7. Refresh ScrollTrigger after layout-affecting content settles.
8. Do not use Lenis and CSS `scroll-behavior: smooth` together.
9. Keep wrapper and content configuration standard unless there is a real need.
10. Test wheel, touchpad, keyboard, anchors, and mobile.

## Text Reveal

1. Text reveal must preserve readability.
2. The text should exist in the DOM as real text.
3. Never reveal critical content so slowly that users wait for meaning.
4. Prefer word reveals for paragraphs.
5. Prefer line reveals for headings and editorial copy.
6. Prefer character reveals only for short, high-impact display text.
7. Avoid character reveals on long headings.
8. Use SplitType only on client-rendered text.
9. Revert SplitType after animation setup cleanup.
10. Avoid layout shift when splitting text.
11. Set overflow hidden on line wrappers only when clipping is intentional.
12. Use masks for premium reveal when typography is large.
13. Use opacity plus `y` translation for simple reveals.
14. Use clip-path for bold section reveals.
15. Use stagger values between 0.015 and 0.08 for words.
16. Use stagger values between 0.008 and 0.03 for characters.
17. Use reduced motion to show text immediately.
18. Do not hide text permanently before JavaScript runs.
19. The no-JS state must be readable.
20. Avoid splitting text that screen readers need to parse unless aria handling is correct.

## Mask Reveal

1. Use mask reveals for hero images, product screenshots, cards, and editorial imagery.
2. Prefer CSS clip-path or mask when the geometry is simple.
3. Prefer SVG masks when the reveal shape is meaningful.
4. Keep masked content visible in reduced motion.
5. Use transform and clip-path carefully; clip-path can be more expensive than transform.
6. Do not combine heavy blur, mask, and shadow on many elements at once.
7. Use image placeholders to avoid layout jumps.
8. Reveal image and adjacent copy as a sequence.
9. Keep the final state crisp.
10. Avoid reveals that look like generic template wipes.

## Clip Path Reveal

1. Use `clip-path: inset()` for directional reveals.
2. Use polygon clip paths for diagonal or editorial transitions.
3. Keep clip-path animation durations under 1 second for normal content.
4. Pair clip reveals with subtle scale when revealing imagery.
5. Avoid complex clip-path animation on low-end mobile.
6. Provide a non-animated fallback.
7. Avoid hiding interactive controls behind delayed clip reveals.
8. Use clip reveals to explain order, not to create noise.

## SVG Animation

1. Use SVG animation for paths, diagrams, icons, progress, and technical storytelling.
2. Prefer GSAP for path drawing.
3. Use `stroke-dasharray` and `stroke-dashoffset` for path reveal.
4. Use `pathLength="1"` when it simplifies normalized animation.
5. Keep SVGs semantic when they convey information.
6. Mark decorative SVGs as aria-hidden.
7. Avoid huge inline SVGs unless they are central to the design.
8. Avoid sketchy placeholder drawings.
9. Avoid random decorative squiggles.
10. Animate SVG in response to content, scroll, or interaction.
11. Use consistent stroke width.
12. Use rounded caps only when they fit the visual language.
13. Use masks for high-end logo or diagram reveals.
14. Do not animate every icon in a feature grid.
15. Make icon motion subtle and fast.

## Three.js and React Three Fiber

1. Use Three.js when spatial depth is core to the experience.
2. Use React Three Fiber in React projects unless the project already uses raw Three.js.
3. Keep 3D scenes focused.
4. Use real geometry, materials, lighting, and camera composition.
5. Avoid generic floating spheres as filler.
6. Avoid heavy postprocessing by default.
7. Use `prefers-reduced-motion` to pause or simplify animated scenes.
8. Provide fallback content if WebGL fails.
9. Keep canvas accessible and non-blocking.
10. Do not trap pointer events unless the canvas is interactive.
11. Test performance on laptop-class hardware.
12. Use compressed assets when loading models.
13. Avoid huge HDRs unless necessary.
14. Use Suspense fallback thoughtfully.
15. Do not put the primary 3D scene inside a tiny decorative card.

## Motion Hierarchy

1. Primary motion belongs to page-level story and navigation.
2. Secondary motion belongs to section reveals and component state.
3. Tertiary motion belongs to hover, tap, focus, and small feedback.
4. Ambient motion must be rare.
5. Never let ambient motion compete with reading.
6. The most important element should enter first or with the clearest emphasis.
7. CTA motion should be confident, not desperate.
8. Navigation motion should be fast and predictable.
9. Modal motion should clarify layering.
10. Accordion motion should clarify containment.
11. Dashboard motion should be minimal and information-preserving.
12. Pricing motion should improve comparison, not distract from plans.

## Animation Sequencing

1. Establish the container.
2. Reveal the primary message.
3. Reveal proof or supporting content.
4. Reveal the primary action.
5. Let secondary details arrive last.
6. Keep related elements grouped.
7. Use stagger only inside a meaningful group.
8. Avoid page-wide cascading entrance effects.
9. Avoid delays longer than 0.4 seconds before useful content appears.
10. Avoid sequencing that blocks interaction.
11. Sequence hero, nav, and CTA as one coherent moment.
12. Sequence scroll sections independently.
13. Sequence modals from backdrop to panel to content.
14. Sequence toasts instantly; users need feedback now.
15. Sequence loading states with honesty, not theater.

## Hero Entrance

1. The hero must make the product, offer, or subject obvious in the first viewport.
2. Animate the hero only after the static composition works.
3. Reveal headline with line or word motion.
4. Reveal visual media with mask or scale.
5. Reveal CTA after the core message.
6. Keep navbar entrance faster than hero content.
7. Avoid long intro animations.
8. Do not block scrolling.
9. Do not hide the hero until JavaScript loads.
10. Use one signature motion idea, not five.
11. For SaaS, show product reality early.
12. For portfolios, show actual work early.
13. For ecommerce, show the product clearly.
14. For agencies, show taste through layout and proof, not buzzwords.
15. For dashboards, avoid theatrical hero language.

## Navbar Animations

1. Navbar motion must be quick.
2. Dropdowns should open in 120 to 220 milliseconds.
3. Use opacity, scale, and slight y movement.
4. Use layout animations for active indicators.
5. Do not over-animate every nav link.
6. Hover states should be legible and keyboard-equivalent.
7. Sticky nav transitions should not jump.
8. Mobile menus should trap focus when open.
9. Mobile menu exit should be clean.
10. Reduced motion should open menus instantly or with a fade.

## CTA Animations

1. CTA motion should communicate affordance.
2. Use subtle lift, scale, arrow translation, shine, or magnetic behavior.
3. Avoid infinite pulsing by default.
4. Avoid aggressive glow.
5. The main CTA must remain readable in all states.
6. Hover should not move the button so far that the cursor loses it.
7. Tap state should feel tactile.
8. Loading state should preserve button width.
9. Success state should be clear and quick.
10. Disabled state should not animate as interactive.

## Magnetic Buttons

1. Use magnetic buttons sparingly.
2. Use them for hero CTAs, portfolio links, or expressive brand moments.
3. Avoid magnetic behavior in dense dashboards.
4. Keep movement within a small radius.
5. Reset position smoothly on pointer leave.
6. Use RAF and passive pointer handling.
7. Respect reduced motion.
8. Keep focus states visible.
9. Do not make the text unreadable while moving.
10. Do not apply magnetic behavior to every button.

## Cursor Follower

1. Use cursor followers only for expressive marketing, portfolio, or agency experiences.
2. Never use custom cursors in productivity tools by default.
3. Never hide the native cursor unless the replacement is excellent.
4. Do not degrade text selection.
5. Do not interfere with form fields.
6. Disable on touch devices.
7. Disable or simplify for reduced motion.
8. Keep it small, subtle, and purposeful.
9. Change state over links only when useful.
10. Avoid trailing blobs and generic glow circles.

## Parallax and Depth

1. Parallax should create spatial hierarchy.
2. Use shallow depth for premium interfaces.
3. Avoid seasick scroll effects.
4. Move background slower than foreground.
5. Keep text mostly stable.
6. Use perspective only when it clarifies physical relationships.
7. Use 3D transforms sparingly.
8. Avoid rotating cards into illegibility.
9. Avoid scroll effects that make users fight the page.
10. Disable or simplify for reduced motion.

## Glassmorphism

1. Use glass only when the underlying scene makes it meaningful.
2. Avoid glass as the default card style.
3. Keep blur radius moderate.
4. Ensure contrast remains compliant.
5. Use borders and tint to preserve edges.
6. Do not stack glass on glass.
7. Avoid glass over busy images.
8. Prefer solid surfaces for dashboards and forms.
9. Use glass for overlays, nav, or hero elements only when it fits.
10. Test on low-power devices.

## Floating Cards

1. Floating cards must represent layered information or spatial storytelling.
2. Avoid generic floating card clusters.
3. Cards should align to a real grid even when visually offset.
4. Motion should be subtle.
5. Avoid random rotations.
6. Do not float every card.
7. Keep shadows realistic.
8. Use depth with scale, opacity, and z-index.
9. Ensure text remains readable.
10. Reduce or remove on small screens.

## Reveal on Scroll

1. Scroll reveals should be content-aware.
2. Use IntersectionObserver, Motion `whileInView`, or ScrollTrigger depending on complexity.
3. Do not reveal everything with the same `fade-up`.
4. Do not hide content before JavaScript is ready.
5. Reveals should trigger once unless repeated feedback is useful.
6. Use small y offsets.
7. Avoid reveal delays that make scrolling feel laggy.
8. Avoid revealing items after they are already past the user's focus.
9. Make reduced-motion content visible immediately.
10. Test fast scrolling.

## Sticky Sections

1. Sticky sections should support comparison, narrative, or focused reading.
2. Use sticky for feature walkthroughs, product tours, timelines, and visual explanations.
3. Avoid sticky for ordinary content lists.
4. Keep sticky content shorter than the viewport.
5. Ensure mobile fallback is natural.
6. Avoid nested sticky complexity.
7. Watch z-index and stacking contexts.
8. Avoid sticky elements covering anchors.
9. Test keyboard navigation.
10. Provide reduced-motion behavior.

## Horizontal Scrolling

1. Use horizontal scrolling only when the content benefits from lateral comparison or gallery flow.
2. Do not hijack scroll casually.
3. Make scroll progress obvious.
4. Provide mobile-friendly native alternatives.
5. Avoid horizontal scroll for critical form or pricing decisions.
6. Use ScrollTrigger pinning only with clear purpose.
7. Keep content accessible in DOM order.
8. Make keyboard access possible.
9. Avoid excessive scroll distance.
10. Respect reduced motion.

## Page Transitions

1. Page transitions must be fast.
2. Preserve user orientation.
3. Use shared layout when moving from list to detail.
4. Use fades for simple route changes.
5. Use masks for editorial or brand-heavy transitions.
6. Avoid full-screen loaders between normal pages.
7. Do not delay navigation for animation vanity.
8. Make focus management correct after navigation.
9. Scroll restoration must be intentional.
10. Reduced motion should use instant transitions or short fades.

## Loading Animations

1. Loading states must communicate progress or waiting honestly.
2. Prefer skeletons for content loading.
3. Prefer optimistic UI when action outcome is predictable.
4. Avoid fancy loaders that hide slow performance.
5. Keep spinners small and rare.
6. Use shimmer carefully and with reduced-motion alternatives.
7. Preserve layout dimensions.
8. Avoid cumulative layout shift.
9. Button loading should preserve width.
10. Success feedback should arrive immediately.

## Pricing Animations

1. Pricing pages need clarity over spectacle.
2. Animate plan comparison lightly.
3. Use Motion layout for billing toggle changes.
4. Keep prices stable and readable.
5. Avoid number animations that confuse actual cost.
6. Highlight recommended plans with structure, not blinking.
7. Animate feature expansion only when helpful.
8. Make keyboard and screen reader behavior correct.
9. Avoid scroll hijacking near purchase decisions.
10. Respect reduced motion.

## FAQ and Accordion Animations

1. Accordion motion should make expansion direction clear.
2. Use height animation carefully.
3. Prefer CSS grid rows or Motion height when needed.
4. Keep duration short.
5. Rotate icons subtly.
6. Preserve focus.
7. Support keyboard controls.
8. Do not animate long FAQ content slowly.
9. Avoid nested accordions unless necessary.
10. Reduced motion should open instantly.

## Dashboard Animations

1. Dashboards are tools; motion must serve comprehension.
2. Animate data updates subtly.
3. Avoid scroll smoothers by default.
4. Avoid dramatic entrance animations after every navigation.
5. Use layout animation to preserve object constancy.
6. Use skeletons for loading panels.
7. Use small transitions for filters, tabs, and drawers.
8. Avoid animated backgrounds.
9. Avoid hover effects that reduce density.
10. Never obscure data with decorative motion.

## Modal Animations

1. Modal entrance should clarify layering.
2. Fade backdrop quickly.
3. Scale or translate panel subtly.
4. Trap focus.
5. Restore focus on close.
6. Close on Escape when appropriate.
7. Do not animate destructive confirmations playfully.
8. Keep exit shorter than entrance.
9. Avoid moving modals across large distances.
10. Reduced motion should fade or appear instantly.

## Hover Interactions

1. Hover should reveal affordance or useful secondary information.
2. Use hover effects that also have focus equivalents.
3. Avoid hover-only content required for task completion.
4. Keep hover duration short.
5. Use transform and opacity.
6. Avoid huge shadow changes.
7. Avoid layout shifts.
8. Avoid hover effects on non-interactive elements unless clearly decorative.
9. Disable hover assumptions on touch devices.
10. Test pointer and keyboard.

## Micro Interactions

1. Micro-interactions should make the interface feel responsive.
2. Use them for toggles, copy buttons, tabs, filters, checkboxes, form validation, saves, drag handles, and menu state.
3. Keep feedback immediate.
4. Keep animation short.
5. Use spring only where physical movement makes sense.
6. Use sound never unless explicitly requested.
7. Use haptics only in platforms that support them and when appropriate.
8. Do not celebrate routine actions too loudly.
9. Use success states sparingly.
10. Error states should be calm, clear, and useful.

## Performance Rules

1. Avoid `transition: all`.
2. Avoid animating width, height, top, left, right, bottom, margin, padding, or border radius when transform can work.
3. Avoid large animated box shadows.
4. Avoid expensive filters on many elements.
5. Avoid layout thrashing.
6. Avoid forced reflow in pointermove handlers.
7. Avoid too many observers.
8. Avoid scroll handlers that do real work on every event.
9. Prefer transform.
10. Prefer opacity.
11. Prefer `translate3d`.
12. Prefer scale.
13. Prefer rotate.
14. Prefer `requestAnimationFrame`.
15. Prefer passive event listeners.
16. Use `will-change` only shortly before an animation or on a very small number of elements.
17. Remove `will-change` when no longer needed.
18. Use CSS containment when useful.
19. Use image dimensions to prevent layout shift.
20. Lazy-load below-fold heavy media.
21. Defer heavy animation setup until needed.
22. Keep animation bundles justified.
23. Tree-shake libraries where possible.
24. Test mobile performance.
25. Test CPU throttling when the experience is animation-heavy.

## Accessibility Rules

1. Respect `prefers-reduced-motion`.
2. Animations should never block interaction.
3. Animations should never make content unreachable.
4. Keep interfaces keyboard accessible.
5. Preserve visible focus states.
6. Do not remove outlines without replacing them.
7. Avoid motion that can trigger vestibular discomfort.
8. Avoid flashing.
9. Avoid parallax on essential text.
10. Avoid scroll hijacking for core workflows.
11. Ensure contrast remains compliant in animated states.
12. Ensure screen readers get meaningful content order.
13. Keep DOM order aligned with visual order when possible.
14. Announce async state changes when needed.
15. Do not rely on color alone.
16. Do not rely on motion alone.
17. Use semantic controls.
18. Use buttons for actions.
19. Use links for navigation.
20. Test reduced motion manually.

## Reduced Motion Pattern

1. In CSS, use `@media (prefers-reduced-motion: reduce)`.
2. In Motion, use `useReducedMotion()`.
3. In GSAP, branch before creating complex timelines.
4. In Lenis, disable smooth scrolling or reduce smoothing.
5. In Three.js, pause camera movement and ambient loops.
6. Replace large movement with opacity or instant state.
7. Remove parallax.
8. Remove scroll-linked transforms.
9. Keep user feedback visible.
10. Never use reduced motion as reduced quality.

## Color

1. Build a color strategy before picking colors.
2. Avoid one-note palettes dominated by one hue.
3. Avoid default purple-to-blue gradients unless the brand demands them.
4. Avoid beige, cream, sand, tan, and coffee palettes as a reflex.
5. Avoid all-slate SaaS monotony unless the product truly benefits.
6. Use contrast as a design material.
7. Use accent colors to guide attention.
8. Use color sparingly in product UIs.
9. Use color more boldly in brand pages only when the concept supports it.
10. Make disabled states clear but readable.
11. Make placeholder text readable.
12. Keep body text high contrast.
13. Use OKLCH when defining a fresh system.
14. Test light and dark surfaces separately.
15. Avoid gray text on colored backgrounds.

## Typography

1. Typography carries most of the premium feeling.
2. Pick fonts that match the product's audience and tone.
3. Do not default to Inter for every project.
4. Use one family well before adding a second.
5. Pair fonts by contrast when pairing.
6. Keep display letter spacing controlled.
7. Avoid cramped headlines.
8. Use `text-wrap: balance` on headings.
9. Use `text-wrap: pretty` on prose when supported.
10. Keep paragraph measure around 55 to 75 characters.
11. Use tabular numbers in dashboards and pricing.
12. Use optical sizing when available.
13. Avoid giant type inside compact components.
14. Avoid tiny uppercase eyebrow labels everywhere.
15. Ensure animated text remains selectable when practical.

## Layout

1. Start with content hierarchy.
2. Use a spacing scale.
3. Align to a grid without making the page rigid.
4. Use cards only when they are the right container.
5. Avoid cards inside cards.
6. Avoid decorative section cards.
7. Use full-width bands or unframed sections.
8. Keep repeated items consistent.
9. Break symmetry deliberately.
10. Preserve responsive rhythm.
11. Avoid text overflow.
12. Avoid overlapping UI unless intentionally layered and tested.
13. Use stable dimensions for fixed-format elements.
14. Use aspect ratios for media.
15. Use container queries when helpful.

## Component Expectations

1. Buttons need default, hover, focus, active, loading, disabled, and reduced-motion states.
2. Cards need clear hierarchy, click affordance when clickable, and non-click styling when static.
3. Forms need labels, help text, errors, success, loading, disabled, and focus behavior.
4. Navbars need desktop, mobile, active, dropdown, and keyboard behavior.
5. Modals need focus management and escape behavior.
6. Accordions need aria-expanded and keyboard support.
7. Tabs need roving or native accessible behavior.
8. Pricing toggles need clear state and no confusing price animation.
9. Dashboards need loading, empty, error, and updated states.
10. Feature grids need varied content rhythm, not identical icons and text.

## Landing Pages

1. Make the offer clear immediately.
2. Show proof early.
3. Use one strong hero motion idea.
4. Avoid generic SaaS card grids.
5. Vary section rhythm.
6. Use real product visuals when possible.
7. Make CTA placement obvious.
8. Animate transitions between story beats.
9. Keep scroll effects purposeful.
10. End with a confident final CTA.

## SaaS Interfaces

1. Prioritize product clarity.
2. Show actual workflow.
3. Use diagrams only when they clarify.
4. Avoid fake metrics unless examples are labeled.
5. Use motion to explain flow.
6. Use subdued micro-interactions.
7. Use strong empty states.
8. Use pricing clarity.
9. Use trust signals without clutter.
10. Avoid startup-template clichés.

## Dashboards

1. Prioritize scanning and comparison.
2. Keep density useful.
3. Use restrained animation.
4. Use stable layout.
5. Animate changed values subtly.
6. Avoid decorative backgrounds.
7. Use color for status and priority.
8. Keep charts legible.
9. Avoid theatrical page transitions.
10. Make repeated workflows efficient.

## Agency Sites

1. Show taste through work, not claims.
2. Use confident typography.
3. Use strong case study rhythm.
4. Use motion to frame work samples.
5. Avoid vague premium jargon.
6. Avoid overusing awards-style effects.
7. Make contact CTA easy.
8. Use real constraints and outcomes.
9. Keep performance high.
10. Ensure mobile feels designed, not collapsed.

## Portfolios

1. Put work first.
2. Make project cards feel specific.
3. Use motion to support browsing.
4. Avoid hiding work behind mystery navigation.
5. Use page transitions to preserve orientation.
6. Use high-quality imagery.
7. Keep bio concise.
8. Make contact obvious.
9. Do not over-animate reading pages.
10. Let personality appear in details.

## Ecommerce

1. Product visibility beats effects.
2. Keep purchase flow calm.
3. Use hover media transitions carefully.
4. Use cart animations for clear feedback.
5. Avoid scroll hijacking.
6. Keep filters fast.
7. Preserve image aspect ratios.
8. Use motion to communicate selection and add-to-cart.
9. Do not distract from price, variant, stock, shipping, or checkout.
10. Reduced motion must keep commerce fully functional.

## Pricing

1. Comparison clarity is the goal.
2. Use plan hierarchy without manipulation.
3. Use Motion for billing cycle transitions.
4. Keep feature lists easy to scan.
5. Animate expansion only if it improves comprehension.
6. Avoid gimmicky savings counters.
7. Keep enterprise CTA distinct.
8. Make all terms clear.
9. Avoid hover-only details.
10. Test mobile plan comparison.

## FAQ

1. Group questions by decision stage.
2. Animate accordion open and close quickly.
3. Keep answers readable.
4. Do not bury critical objections.
5. Use accessible accordion markup.
6. Use focus-visible states.
7. Avoid smooth scroll traps.
8. Keep reduced motion instant.
9. Let deep links work if supported.
10. Do not use FAQ as filler.

## Hero

1. The hero should identify the thing being offered.
2. The hero should show why it matters.
3. The hero should provide a next action.
4. The hero should reveal enough visual substance to feel real.
5. Use one strong composition.
6. Avoid generic gradient blobs.
7. Avoid vague product mockups.
8. Avoid oversized empty hero sections.
9. Make mobile hero excellent.
10. Leave a hint of the next section when appropriate.

## Testimonials

1. Use testimonials as evidence, not decoration.
2. Animate testimonial changes gently.
3. Avoid auto-rotating carousels unless pause controls exist.
4. Keep attribution clear.
5. Use real logos only with permission.
6. Make quotes readable.
7. Avoid overdesigned quote cards.
8. Use motion to compare proof points.
9. Do not hide all proof in a slider.
10. Keep mobile reading easy.

## Navbar

1. Make navigation predictable.
2. Use active states.
3. Use fast dropdown motion.
4. Use accessible mobile menus.
5. Avoid massive nav animation.
6. Keep CTA distinct.
7. Handle scroll state smoothly.
8. Avoid layout shift on sticky behavior.
9. Keep keyboard order logical.
10. Ensure reduced motion is clean.

## Footer

1. Footer should close the experience calmly.
2. Use clear link groups.
3. Avoid oversized decorative footers unless brand-led.
4. Use subtle entrance motion.
5. Keep newsletter forms accessible.
6. Include legal links.
7. Avoid hiding important links.
8. Use contrast correctly.
9. Keep mobile columns usable.
10. Do not animate footer content excessively.

## Cards

1. Cards must have a reason to be cards.
2. Do not nest cards.
3. Keep card radius restrained.
4. Use hover for affordance only when clickable.
5. Avoid giant soft shadows everywhere.
6. Use image, icon, stat, or label hierarchy deliberately.
7. Keep equal-height cards only when comparison benefits.
8. Use varied cards for editorial rhythm.
9. Avoid identical feature-card monotony.
10. Make focus states clear.

## Forms

1. Forms must feel trustworthy.
2. Labels should be visible.
3. Placeholders are not labels.
4. Animate validation without hostility.
5. Keep errors specific.
6. Preserve input height.
7. Use loading states on submit.
8. Use success states clearly.
9. Respect autofill.
10. Keep keyboard flow excellent.

## Timeline

1. Use timelines only for real sequences.
2. Animate progress when it helps orientation.
3. Use ScrollTrigger for rich scroll-linked timelines.
4. Keep dates or steps readable.
5. Avoid decorative numbers everywhere.
6. Use sticky details for complex timelines.
7. Provide mobile linear fallback.
8. Respect reduced motion.
9. Avoid long pinned fatigue.
10. Make completion state clear.

## Feature Grid

1. Features should be grouped by user value.
2. Avoid same icon, heading, text repeated endlessly.
3. Use varied scale only when hierarchy requires it.
4. Use motion to reveal relationships.
5. Keep copy concrete.
6. Avoid fake depth.
7. Avoid card overload.
8. Use icons sparingly.
9. Ensure scanning works without animation.
10. Make mobile order intentional.

## Bento Grid

1. Bento grids need true content hierarchy.
2. Do not use bento layout as a trend wrapper.
3. Large cells should contain high-value proof or product visuals.
4. Small cells should contain concise supporting details.
5. Animate cells in groups.
6. Avoid every cell having the same hover.
7. Keep responsive reflow designed.
8. Avoid nested cards.
9. Use background materials sparingly.
10. Make the grid readable before motion.

## Prompt Behavior

1. When the user asks for a page, build the page, not a marketing explanation.
2. When the user asks for polish, inspect existing UI and make concrete changes.
3. When the user asks for animation, choose the library based on interaction type.
4. When the user asks for premium, improve hierarchy, type, spacing, color, media, and motion.
5. When the user asks for Awwwards-like, preserve usability and performance.
6. When the user asks for Apple-like, translate restraint and clarity, not Apple assets.
7. When the user asks for Stripe-like, translate systems clarity, not Stripe visuals.
8. When the user asks for Linear-like, translate density and precision, not Linear's exact UI.
9. When unsure, ask only if the decision changes the implementation materially.
10. Otherwise make a tasteful choice and proceed.

## Good Prompt Examples

1. "Build a premium SaaS landing page with a scroll-led product walkthrough, using GSAP ScrollTrigger for the hero and Motion for component states."
2. "Polish this dashboard so it feels like a serious product: tighten spacing, improve hierarchy, add subtle update animations, and preserve accessibility."
3. "Create an agency portfolio homepage with Lenis smooth scroll, masked case-study reveals, and reduced-motion support."
4. "Add Motion-based page transitions to the product detail flow without delaying navigation."
5. "Improve this pricing section with a billing toggle, accessible accordions, and restrained micro-interactions."
6. "Make this hero feel more premium without adding generic gradients or floating blobs."
7. "Use GSAP SplitType for a short headline reveal and keep the no-JS fallback readable."
8. "Add a Three.js product object only if it materially improves the hero concept."
9. "Audit this animated page for performance, reduced motion, and visual hierarchy."
10. "Create a Magic Patterns prompt for a sophisticated fintech interface with calm, credible motion."

## Bad Prompt Patterns To Correct

1. "Make it pop" without defining audience, product, or outcome.
2. "Add animations everywhere."
3. "Make it look like Apple exactly."
4. "Use Awwwards effects" for a checkout form.
5. "Add smooth scrolling" to a dense dashboard.
6. "Use Three.js in the background" without conceptual need.
7. "Make every section fade up."
8. "Use glassmorphism cards for everything."
9. "Add a custom cursor" to a business app.
10. "Make it premium with purple gradients."

## Anti Patterns

1. `transition: all`.
2. Infinite CTA pulsing.
3. Bounce easing in serious products.
4. Elastic menus in enterprise software.
5. Generic floating orbs.
6. Gradient text as the main visual idea.
7. Cards nested inside cards.
8. Giant rounded cards everywhere.
9. Scroll hijacking ordinary content.
10. Smooth scrolling in data tools.
11. Hiding text until JS animation runs.
12. SplitType on long body copy.
13. Character staggers across paragraphs.
14. No reduced-motion support.
15. Animating layout properties in large lists.
16. Large animated shadows.
17. Heavy blur over busy backgrounds.
18. Custom cursor that breaks selection.
19. Page transition that delays navigation.
20. Decorative 3D with no meaning.
21. Pinning every section.
22. Horizontal scroll with no reason.
23. Hover-only essential content.
24. Low contrast muted text.
25. Design references copied too literally.

## Implementation Checklist

1. Confirm framework and styling system.
2. Confirm existing animation dependencies.
3. Define motion hierarchy.
4. Choose CSS, Motion, GSAP, Lenis, SVG, or Three.js intentionally.
5. Build static layout first.
6. Add semantic structure.
7. Add responsive layout.
8. Add accessible states.
9. Add motion.
10. Add reduced-motion branch.
11. Test keyboard.
12. Test mobile.
13. Test fast scroll.
14. Test slow network if media-heavy.
15. Test no-JS readability when relevant.
16. Check contrast.
17. Check text overflow.
18. Check layout shift.
19. Check bundle impact.
20. Remove unused effects.

## Code Preferences

1. Use TypeScript when the project uses TypeScript.
2. Use client components only where animation needs the client.
3. Keep animation hooks isolated.
4. Avoid mixing animation ownership.
5. Prefer reusable motion primitives only after duplication appears.
6. Keep magic numbers named or localized.
7. Keep easing constants shared.
8. Keep duration constants consistent.
9. Clean up listeners, observers, timelines, and RAF loops.
10. Avoid global side effects unless deliberate.

## React Pattern

1. Use refs for GSAP targets.
2. Use scoped selectors inside GSAP context.
3. Use Motion props for component-level state.
4. Use stable arrays for staggered children.
5. Avoid remounting large animated trees unnecessarily.
6. Use `useMemo` for expensive config only when needed.
7. Use `useReducedMotion` in animated components.
8. Use CSS variables for theme values.
9. Keep animation state separate from business state.
10. Clean up on unmount.

## Next.js Pattern

1. Keep server components as server components where possible.
2. Move animation islands into client components.
3. Avoid making the whole page client-side for one animation.
4. Use dynamic imports for heavy 3D or animation modules when appropriate.
5. Ensure route transitions work with the App Router.
6. Avoid hydration mismatches from random animation values.
7. Use deterministic initial states.
8. Use font loading strategies that avoid layout shift.
9. Use image optimization.
10. Test production build behavior.

## Magic Patterns Guidance

1. Be explicit about the visual system you want.
2. Specify motion libraries only when they match the goal.
3. Ask for real responsive states.
4. Ask for reduced-motion support.
5. Ask for concrete component states.
6. Ask for premium restraint.
7. Avoid asking for clones of named brands.
8. Ask for inspiration translated into principles.
9. Ask for production-ready React, not just a mockup.
10. Ask for accessible interactions.

## Output Style

1. If coding, implement directly.
2. If writing a prompt, write a ready-to-use prompt with constraints and acceptance criteria.
3. If reviewing, lead with concrete issues.
4. If designing, describe choices briefly and then build.
5. If choosing libraries, explain the choice in one or two sentences.
6. Do not over-explain obvious UI features inside the app.
7. Do not put instructional text in the visible UI unless the product needs it.
8. Keep user-facing copy refined and specific.
9. Use examples from `examples/` when helpful.
10. Use references from `references/` when deeper guidance is needed.

## Reference Files

1. Read `references/gsap-philosophy.md` for GSAP, timelines, ScrollTrigger, SplitType, and SVG path animation.
2. Read `references/motion-philosophy.md` for Motion, variants, layout animation, shared layout, and AnimatePresence.
3. Read `references/lenis-philosophy.md` for smooth scrolling and ScrollTrigger synchronization.
4. Read `references/animation-principles.md` for timing, easing, sequencing, reveals, and reduced motion.
5. Read `references/micro-interactions.md` for controls, feedback, hover, tap, forms, accordions, modals, and dashboards.
6. Read `references/scroll-design.md` for scroll-linked motion, sticky sections, pinning, parallax, and horizontal scroll.
7. Read `references/premium-ui-principles.md` for typography, color, layout, inspiration handling, and anti-patterns.

## Example Files

1. Use `examples/landing-page.md` for landing page patterns.
2. Use `examples/saas.md` for SaaS patterns.
3. Use `examples/dashboard.md` for dashboard patterns.
4. Use `examples/agency.md` for agency patterns.
5. Use `examples/portfolio.md` for portfolio patterns.
6. Use `examples/ecommerce.md` for ecommerce patterns.
7. Use `examples/pricing.md` for pricing patterns.
8. Use `examples/faq.md` for FAQ patterns.
9. Use `examples/hero.md` for hero patterns.
10. Use `examples/testimonials.md` for testimonial patterns.
11. Use `examples/navbar.md` for navbar patterns.
12. Use `examples/footer.md` for footer patterns.
13. Use `examples/cards.md` for card patterns.
14. Use `examples/forms.md` for form patterns.
15. Use `examples/cta.md` for CTA patterns.
16. Use `examples/timeline.md` for timeline patterns.
17. Use `examples/feature-grid.md` for feature grid patterns.
18. Use `examples/bento-grid.md` for bento grid patterns.

## Final Quality Bar

1. The interface should feel deliberate before it feels animated.
2. The motion should feel inevitable, not pasted on.
3. The layout should remain strong with animation disabled.
4. The code should be maintainable by a normal frontend team.
5. The user should not need manual fixes after generation.
6. The result should be compatible with Magic Patterns and Agent Skills-compatible tools.
7. The skill repository should remain installable with `npx skills add`.
8. The front matter should remain valid YAML.
9. The skill name should remain `premium-animations`.
10. The skill directory or root should contain this exact `SKILL.md`.
