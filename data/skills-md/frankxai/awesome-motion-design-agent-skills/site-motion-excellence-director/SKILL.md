---
name: site-motion-excellence-director
description: Use when planning, auditing, specifying, implementing, or improving premium website/app motion across FrankX, Arcanea, Starlight, or Vercel/Next.js sites. Use for motion design systems, site choreography, scroll motion, generated media integration, runtime selection, reduced-motion planning, visual QA, and turning rough motion ideas into implementation-ready specs.
---

# Site Motion Excellence Director

Use this skill before adding substantial motion to a website or app.

## Workflow

1. Identify the brand, route, audience, and first user task.
2. Define the first read before animation.
3. Name the motion job: orient, reveal, explain, confirm, compare, express brand, or convert.
4. Pass the still-frame gate.
5. Write a beat sequence: setup, trigger, primary move, secondary support, hold, final state.
6. Choose the lightest runtime that preserves the intent.
7. Specify reduced motion in the same pass.
8. Implement only after the spec is clear.
9. Verify with browser screenshots, mobile, reduced motion, and video/frame proof.
10. Score with the excellence gate.

## Runtime Rules

- Use CSS for simple state changes, hover/focus, skeletons, and low-risk reveals.
- Use Motion for React for component choreography, layout transitions, presence, and React scroll work.
- Use GSAP ScrollTrigger for pinned, scrubbed, snapped, SVG/canvas, or complex authored timelines.
- Use Rive for interactive vector state machines.
- Use Lottie/dotLottie for portable non-interactive vector loops.
- Use Three.js only when 3D is central and visually verified.
- Use Remotion for rendered video, social variants, product explainers, and exact text/layout in media.
- Use Grok/imagegen/Veo/Sora/Luma/Runway/Higgsfield only as source generation, then finish and QA in context.

## Taste Rules

- Motion is hierarchy over time.
- Do not animate a weak still frame.
- Make one object the hero.
- Use stillness as contrast.
- Keep repeated task motion short and quiet.
- Do not bake exact product text into generated images or videos.
- Treat mobile as separate choreography.
- Never ship meaningful motion without reduced-motion behavior.

## Required Spec

Use `templates/site-motion/SITE_MOTION_SPEC.md` for substantial site motion.

Use `rubrics/site-motion-excellence-gate.md` before handoff.

## Output Shape

Return: motion thesis, first-read diagnosis, still-frame verdict, motion map, runtime choice, reduced-motion plan, implementation tasks, QA proof required, and excellence score.
