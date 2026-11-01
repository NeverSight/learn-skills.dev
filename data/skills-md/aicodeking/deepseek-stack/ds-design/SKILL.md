---
name: ds-design
description: "Builds a frontend with a clear visual direction instead of the generic AI look. Use when you create a new page, app screen, or component, or restyle one that looks templated. Run as /ds-design."
---

Build a UI that does not look like the default output for any similar prompt.

## Steps

1. Read the brief and the project. Find the subject, the audience, the one action you want the user to take, the stack, the existing brand, and the images you actually have. If the brief is vague, write down how you interpret it in one line and continue.
2. Write a direction note of five lines or fewer before you write code. Include the purpose, the audience, the tone, the one memorable thing, and the mode (persuade, operate, or read). Take it from the subject's own world, not the usual look of its category.
3. Define the tokens before you write components:
   - Type: a display font and a body font that are clearly different. Do not use a default font for display. Use a 5-7 step scale, body text of 16px or more, and lines under 80 characters.
   - Color: 4-6 named hex values. Use one dominant color for large areas and one sharp accent for actions only.
   - Use a 4px or 8px spacing base, one or two radius values, and one shadow style or none.
4. Ask: "Would I make this plan for any similar prompt?" Change each part where the answer is yes.
5. Lay out the page with intent. Choose a density: airy for persuading, compact for tools. Use asymmetry or scale contrast where it serves the content. Use real copy and plausible data. Do not use lorem ipsum.
6. Use motion only where it does a job. Use one orchestrated reveal, plus feedback on user actions.
7. Build every state: hover, focus-visible, disabled, empty, loading, error, and long content.
8. Meet the accessibility floor. Contrast must be 4.5:1, focus rings must be visible, and fields must have labels. Touch targets must be at least 44px, images need alt text, and reduced motion must be respected.
9. Take screenshots at about 1440px and 390px wide. Check them against the banned defaults and the direction note. Fix the problems in one batch, then take new screenshots. Remove one decoration that does no work.

## Banned defaults

Use one of these only if the brief asks for it:

- Purple-blue gradients and decorative gradient washes.
- Inter, Roboto, or the system font as the display face.
- Emoji used as icons. Use one set of SVG icons.
- A centered hero with three identical cards below it.
- Glassmorphism or glow on every surface.
- Gray text on a gray background with low contrast.
- Stock copy such as "Unlock your potential" or "Seamless".
- All-caps eyebrow labels above every heading.
- The same radius and soft shadow on every card.

## Stop when

- The direction note and the tokens exist, and the code uses the tokens.
- The screenshots at both widths show no banned default and no horizontal scroll.
- All the states are built and the accessibility floor is met.
- The one memorable thing is visible in the screenshot.

## Rules

- When the brief specifies a font, color, or style, use it, even if it is on the banned list.
- A refinement keeps the identity of the UI. A redesign keeps its content and function.
