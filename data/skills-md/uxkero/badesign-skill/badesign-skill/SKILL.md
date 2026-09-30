---
name: badesign-skill
description: Design judgment for any user interface work, including web apps, dashboards, landing pages, ecommerce, forms, mobile apps, redesigns and design reviews.
---

# BADESIGN

## How to weigh this guidance

When two considerations pull in different directions, resolve them in this order and move on:

1. The user's explicit instructions.
2. The project's existing design system and conventions.
3. The hard limits below. They are measurable and have no exceptions.
4. What the brief's users need to accomplish.
5. The visual idea you chose for this brief.
6. The defaults in this skill.

Everything outside the hard limits is a default with a reason. When the brief or your visual idea gives a better reason, follow it.

## Hard limits

- Text people need to read is 12px or larger, with contrast of at least 4.5:1 (3:1 for text 24px and larger).
- Interactive elements have a hit area of at least 44 by 44px on touch screens and 24 by 24px with a pointer.
- Nothing is clipped, overlapping or overflowing its container at the target screen sizes, and the page has no horizontal scroll from 320px up.
- Text and icons inside buttons, badges, chips, tabs and inputs are vertically centered, and controls in the same row share the same height.
- Every requirement in the brief is present and usable, and the code is complete, with no placeholders.
- Inputs have labels, controls are reachable by keyboard with a visible focus state, and zoom is never disabled.

## Understand before designing

- **The job.** Who uses this, for what task, how often, on what device, in what conditions. A tool used every day, a page that has to persuade, a flow that has to be finished and a piece meant to be experienced call for different amounts of expression.
- **The content.** What the screen must contain, what matters most, and realistic data including imperfect cases: long names, missing values, errors, items that need attention.
- **The whole product.** A screen belongs to a real product. It keeps that product's navigation, secondary actions and the small functional details a shipped app has, even when the brief describes only one screen.
- **The visual idea.** One concept taken from the subject's own world (its objects, materials, places, era, printed matter, vocabulary) rather than from how interfaces in this category usually look. It decides color, type, shape, density, imagery and composition together, so the screen feels designed as one thing.

## Principles

**Composition**
- Each view has one focal point, reached through clear contrast in scale, weight and position between levels of importance.
- The layout is shaped by the content: a sequence reads as a sequence, a comparison as a comparison, a queue as a queue. Repeating the same block structure section after section is the sign of a template.
- Use a grid and align to it. Break it deliberately where emphasis needs it.
- Rhythm varies: dense areas next to open ones, large type next to small.

**Craft**
- Be opinionated. When two paths are equally valid, commit to one and carry it through every detail.
- Fewer elements, fully resolved, beat many half-finished ones. Within the brief's requirements, spend effort on finishing rather than adding.
- The details nobody asks for are the ones that show quality: a number that does not jump, a border that does not move on hover, a focus state that looks designed.

**Expression**
- Express the visual idea with conviction in type, color and at least one element that could only belong to this subject.
- Tools and flows carry the idea through typography, color, density and detail while their layout stays predictable. Persuasive and expressive pages can also carry it through composition, imagery, scale and motion.
- Comfortable values are the starting point on every axis. Extremes such as square corners everywhere, very small or very thin type, condensed faces for body text, heavy or stacked shadows, and very tight spacing need a reason that comes from the idea.
- Decoration is welcome when it comes from the idea. The patterns listed under "Habits of generated interfaces" do not count as an idea.

**Structure and grouping**
- Group with proximity first: space inside a group is smaller than space between groups.
- Shadows belong to elements that float above the page, such as menus, dialogs, popovers and dragged items.
- Containers such as cards, panels and bordered boxes mark real objects and real groups. Page regions are separated by space, bands of color or rules.
- One separation method per boundary.

**Typography**
- Choose typefaces for a reason that comes from the visual idea.
- Use a small scale with visible steps. Running text is about 16px on web and 17pt on iOS; dense product interfaces use 13 to 14px. Secondary text stays close to the body size; small sizes are for short metadata only.
- Keep lines of running text to 45 to 75 characters, with line height around 1.5 for text and 1.1 to 1.25 for headings.
- Use tabular figures for numbers that are compared, right-aligned in tables, with units.

**Color**
- Assign color by role: surfaces, text levels, the accent for action and selection, and status colors that always come with text or an icon.
- The color strategy follows the idea. It can be quiet neutrals with one accent, or one color owning large areas.
- Build ramps in a perceptual space such as OKLCH. On dark grounds, surfaces lighten as they rise.

**Data and detail**
- Short values such as names, IDs, dates, phone numbers and amounts stay on one line. Long text truncates with the full value reachable.
- Values that identify themselves need no label.
- Radii of nested elements shrink inward. Icons come from one set, sized to the text beside them. Edges and baselines line up.

**Behavior**
- Every view that loads data has designed loading, empty and error states. Controls show hover, focus, pressed and disabled states.
- Use each platform's own navigation conventions and keep primary mobile actions within thumb reach.
- In mobile flows the top bar and the primary action stay in place while content scrolls, with space reserved so nothing is covered.
- Layouts reflow by priority across screen sizes.

**Motion and interaction**
- Motion explains cause and effect: what appeared, where it came from, what changed, that an action registered. Its amount follows frequency: actions repeated many times a day respond instantly, occasional ones get a short transition, and rare moments such as a first load or a completed task may carry one crafted animation.
- Every interactive element responds to input: a hover change on pointer devices, a press state (a slight scale to about 0.97 or a darker fill), and a focus state.
- Durations: 100 to 160ms for press and hover, 150 to 250ms for menus and popovers, 200 to 300ms for dialogs, sheets and panels. Exits are faster than entrances.
- Easing: ease-out for anything entering or responding to the user, such as cubic-bezier(0.23, 1, 0.32, 1); ease-in-out for elements moving across the screen; linear only for continuous progress.
- Elements enter from where they originate: a menu grows from its trigger, a sheet slides from its edge, a new row appears in its place. Scale starts at 0.9 or above, combined with opacity.
- Animate transform and opacity; list the properties you transition. Motion stays interruptible, so a reversed hover or a second click changes course from the current state.
- Hover effects apply only on devices that hover. Under reduced-motion settings, movement becomes an instant change or a short fade.

**Copy**
- Buttons name their outcome. Headings name what an area is.
- The interface does not describe itself or explain how to use it.
- Write in the language of the brief. Where content is missing, invent plausible fictional content without disclaimers, and do not present real brands or people as customers or endorsers.

## Habits of generated interfaces

These appear so often in AI-generated UI that they read as the absence of a decision. Use one only when the brief asks for it or your visual idea needs it and you can name why.

- Purple, indigo or violet-to-blue accents and gradients.
- Palettes built from one hue family: all slate, all beige, all purple.
- Dark ground with a neon accent.
- Gradient text, glows, glass panels, blurred orbs and blobs, grid or dot backgrounds.
- A thin border combined with a wide soft shadow.
- Every section wrapped in a rounded card, and cards nested inside cards.
- Rows of identical cards with an icon in a tinted square, a title and two lines.
- Rows of big-number stat tiles, especially with captions that repeat the number.
- A centered hero with a badge above the headline, or one highlighted word in the headline.
- Small uppercase tracked labels above headings, and numbered section labels.
- Pills and badges on ordinary metadata.
- A descriptive subtitle under every heading.
- A greeting as the most prominent text of a tool.
- Fade-and-rise on every section, pulsing dots, marquees, scale on hover.
- Buzzwords, slogans and em dashes in copy.

These are never used, because they have no legitimate use in a finished interface:

- A colored stripe on one side of a card, row or callout to mark it.
- A drawn device frame, fake status bar, fake browser window or terminal dots around content that is itself the screen.
- Emoji standing in for icons.
- Lorem ipsum, "John Doe" or "Acme".

## Before delivering

If you can render, look at the result at the target sizes. Check the hard limits, the focal point, and the habits list, fix what you find, and deliver.
