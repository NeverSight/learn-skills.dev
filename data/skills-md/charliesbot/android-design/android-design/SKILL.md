---
name: android-design
description: >
  Material 3 Expressive design judgment for Android apps in Jetpack Compose. Load it for any task that
  decides how an Android screen looks, even when the request reads as plain Compose coding: building or
  polishing a screen, reviewing UI code or screenshots, setting up a theme (color, typography, shape),
  choosing components, adapting layouts to tablet, foldable, and desktop windows (list-detail, supporting
  pane, what fills the space), Wear OS app screens, and adding motion. It owns the design decisions: load
  it first, then any skill that covers the APIs. Wear tiles, watch faces, and widgets are other skills'
  work.
---

# Android Design

How Google designs Android apps with Material 3 Expressive, translated into decisions and Compose code. Expressive is not a separate design language: it is Material 3 plus opt-in APIs, components, and design tactics that Google calls an "expansion pack."

The through-line: **a screen feels designed when emphasis is spent deliberately.** Rank what the screen is for, then spend size, color contrast, shape, type, containment, and motion on the top goal, less on the next, and almost none on the rest. Stock Material code gives every element equal weight, and the result is a **template**: catalog components at uniform emphasis, assembled rather than composed. Every step below exists to keep a screen from being a template.

Quotes and rules marked **(Google)** come from Google's guidance. Rules marked **(default)** are this skill's starting points: follow them unless the screen's direction gives a reason not to.

**Surfaces.** This skill targets phone, tablet, desktop, and Wear OS app screens. For a Wear OS screen read [references/wear-os.md](references/wear-os.md) first; it wins over this file where they differ. Use the `wear-compose-m3` skill for scaffolding and migration. Wear tiles, watch faces, and home screen widgets belong to the `wear-widgets` skill (Wear widgets and tiles) and the Glance skills (home screen widgets).

## Workflow

1. **Route** the request: proposal first, or straight to code ([Route](#route)).
2. **Answer the [design questions](#design-questions)** in your reply, before any code.
3. **[Compose the screen](#compose-the-screen)** from those answers.
4. **Build** it with the [reference](#reference) below: theme, color, type, shape, motion, layout, and the Expressive components. Building is done when the screen compiles and renders.
5. **Run the [screen check](#screen-check)** on the rendered result.

### Route

When the request cares about the design of a new app, a new screen, or a redesign (it asks for polish, a visual direction, or Material 3 Expressive, or names this skill), start with a proposal, even when it says "build": follow the `android-design-explore` skill, show its proposal in the previewer app, and wait for the user to approve a direction before writing any Compose. Skip the proposal when the user says to ("skip the proposal", "just code it") or an approved proposal already exists; port an approved proposal with that skill's "Approve and port" steps, which start with `export_kotlin`.

A plain build that does not ask about design goes straight to code, through the design questions and the screen check.

Changes inside an existing design (a fix, a tweak, a review, a new state of an approved screen) go straight to the actual project under its own approval and branch rules, using the design questions and screen check.

A UI Builder design authoring request follows the `compose-ui-builder` skill; this skill still owns its design decisions.

The step is done when you are following `android-design-explore` for a proposal, or have chosen to go straight to code.

### Design questions

Answer these in your reply before any code, a sentence or two each. These answers are what keep a screen from being a template.

1. **Rank the goals.** What is the one primary task on this screen? What is secondary and tertiary? (Google: "Simplifying to one primary task on each page.")
2. **Choose a direction.** Name the screen's emotional character, the content or interaction that defines it, and one visual idea that ties type, imagery, color, and shape together. Each answer must name a decision ("the total set in tall numerals fills the top third"), not an adjective ("modern, clean"). If the idea describes how most apps of this type already look, it isn't an idea yet.
3. **Decide the hero moment.** Is this screen one of the product's one or two hero moments (the most emotional or most central interaction)? If yes, plan how several tactics combine there ([Hero moments](#hero-moments-and-restraint)). If no, keep it calm (Google).
4. **Choose the color source.** Dynamic (wallpaper), brand (a generated scheme), or content-based (from an image on screen) ([Color](#color)).
5. **Spend emphasis by rank.** The primary goal gets the most, usually size first. Secondary goals get fewer tactics; tertiary ones get containment and type (Google). Content can dominate the screen when it is the product, as long as the primary action stays unmistakable.
6. **Pick components from the [Components](#components) table**, not from memory of older Material.
7. **Answer the adaptation question.** For each size class you will render (compact; medium or expanded; large or extra large), name what the extra space reveals: a second pane, an expanded rail, more detail. Use the five questions in [references/layout.md](references/layout.md), starting with "What should be revealed?". Navigation stays consistent: if a larger layout has a rail, compact has a navigation bar for the same destinations. For a control-based screen like a media player, the controls reflow and content is revealed. A larger layout that is only the phone content spread wider has not answered it: "Additional space doesn't just mean making the same thing bigger." (Google)

The step is done when all seven are answered in your reply.

### Compose the screen

Components are the last step. Compose from the direction and the content itself:

1. **One element leads.** Decide what fills the most space: the content (a photo, a number, a headline), the primary control, or a key summary. Only one leads; everything else is arranged around it, with "empty space to focus attention." (Google)
2. **Space follows rank.** The lead gets scale and room; supporting information packs into compact groups; tertiary details sit at the edges or behind a tap. The most important content gets "ample space and the brightest surface mapping." (Google)
3. **Type can be the structure.** A display-size title or number can anchor the layout by itself, with no card around it. Heavier weight, larger size, color, and spacing create "editorial-like moments." (Google)
4. **Group by spacing or by containers, deliberately.** Proximity and alignment group implicitly and keep the screen open; containers and surface steps group explicitly and add weight (Google). Use containers where a group must read as one unit or be tapped as one; use spacing when items flow as a list or a story. Ungrouped information blends together. When containment marks a state in a list (unread mail, pending tasks), gather the items in that state under one heading and one container group, and let the rest follow as plain rows under their own heading. Rows that alternate between contained and flat read as stripes, not as a state (default; Google groups by "rhythm, similarity").
5. **Give different information different forms.** A summary, a comparison, and a history rarely want the same card grid. Match the grid to the content: hierarchical for editorial and detail screens, modular for equal items, a column for flowing lists (Google, via [references/layout.md](references/layout.md)). One container shape repeated for everything is the template look.
6. **Let content set the color.** When an image or a subject leads, derive the screen's color from it ([Color](#color)) instead of adding accents around it.

Keep familiar patterns underneath ([Hero moments](#hero-moments-and-restraint)): the composition is new, the interaction model is not.

Patterns seen in shipped Expressive apps (metric card, editorial header, pill hero control, and others) are in [references/components.md](references/components.md#patterns-from-shipped-expressive-apps). Read them for examples after choosing the composition, not to choose it.

The step is done when the lead element, the grouping, and each region's form are decided.

### Screen check

For a proposal, use the `android-design-explore` skill's Check step instead of rendering.

Look at the rendered screen, not the code. Render it with the `compose-preview` skill, which owns tool selection, rendering, and troubleshooting; for a UI Builder design, use the builder skill's visual verification workflow and identify the output type. If you can't render it (a tool is unavailable or the render fails), report "visual quality unverified" instead of answering from code, and refer the user to this repository's README setup section rather than installing tools or substituting another renderer.

- Is the hierarchy obvious at first glance: does the eye land on the primary goal?
- What gives the screen its character, and does every expressive choice serve the direction?
- Does the distribution of color reinforce the hierarchy and the atmosphere, with accents on elements that have a job?
- Are supporting content and actions still easy to find and use? Every action must look tappable: text-only buttons belong inside a clear group of actions (a dialog, card, or snackbar).
- Does it hold up with real content lengths, 200% text, and a smaller window?
- Would it still be clear with the expressive flourishes removed?
- Is it still a template? A screen that could pass for the Material component catalog is not done.

When the render contradicts the direction or the hierarchy, fix the largest mismatch and capture it again. For stateful screens, also capture the alternate state that changes emphasis or layout (playing and paused, selected and unselected, empty and populated).

Code checks, separately:

- [ ] Theme and type: `MaterialExpressiveTheme` with the chosen color source, Google Sans Flex for plain text, and at most one bundled brand face on Display, Headline, and Title Large.
- [ ] Components from the right column of the [Components](#components) table.
- [ ] Text and icons use their intended role pairs: no `copy(alpha = ...)`, no hard-coded hex colors.
- [ ] Custom animations use `MaterialTheme.motionScheme`, not `tween()`.
- [ ] Navigation, dismissal, and selection match the chosen Android component's semantics ([Android conventions](#android-conventions)); content drawn edge-to-edge.

The check is done when every question passes on the latest capture and every code check passes. After two fix rounds, report what still fails instead of looping.

## Reference

### Theme setup

Wrap the app in `MaterialExpressiveTheme` with `MotionScheme.expressive()`, the color scheme from your chosen source, and the type scale from [Typography](#typography). Expressive needs `androidx.compose.material3:material3` **1.5.0-alpha** or later; stable 1.4.0 has almost none of these APIs. Read [references/theming.md](references/theming.md) when setting up or changing a theme: the theme code, the newest version and its toolchain, the opt-in APIs, seed schemes, the type scale, shape morphing, motion specs, and spacing.

### Emphasis and hierarchy

Emphasis is how people find the primary action: larger key actions and deliberate hierarchy reduce errors and make key UI elements faster to find (Google).

- **Size is the loudest lever, and it is relative.** "The most important action or the main call to action (CTA) should be the largest element" (Google): larger key actions mean fewer errors and more satisfied users, so the primary *leads* the actions around it, whatever their size. Content is not competing with it: a summary card or a list row can be physically bigger. Start from the component's default size with the strongest fill (a small button; for a FAB, Google's "medium FAB is recommended for most situations") and grow it only as far as leading its peers takes; one focal point per screen, and when everything is large, nothing is. Grouped actions share one size by default ("all buttons in a standard group should be the same size"), and the primary leads through fill or shape: Google's group rule is "largest, widest, or most visually prominent." Extra-large belongs to a control-led hero, such as a player or a breathing session, where the control is the screen's content. The label sets the floor: Google says "Don't truncate or wrap label text" and a container "shouldn't be narrower than its label text." When a label does not fit on one line at the chosen size in its container (a phone-width card, a pane), shorten it to 1 to 3 words, give the button more room, or step down a size (Google: size can change "across different breakpoints", and emphasis comes "through size, color, or shape").
- **Placement:** put the key action where the hands and eyes already are. Google's email study: moving Send from a small top-bar icon to a larger button just above the keyboard, in `secondary`, made people find it 4x faster; Aura's home screen puts its extra-large start button low, last in the vertical flow. Choose the position from the interaction and the space the content needs (default).
- **The primary action gets the strongest fill** (Google: primary roles go to crucial calls to action; filled buttons sparingly). Secondary actions are tonal or standard; toggles like favorite show state with a filled icon or a tonal container, leaving the one loud fill to the main control.
- **Contrast between roles, not one role everywhere:** `primary` for the main action, `secondary` or `secondaryContainer` for supporting controls, `tertiary` for status or accents. Using `primary` and `primaryContainer` for everything flattens the screen.
- **Containment:** group related items in containers; give the most important content "ample space and the brightest surface."
- **Summaries support the task, they don't outrank it.** When the primary goal is acting on a list (checking off habits, replying to messages), the next actionable item must stay the most inviting thing on screen. Stat cards can be bold, but give actionable rows clear containers and let completed items recede (quieter color, no strong fill), grouped by state rather than interleaved ([Compose the screen](#compose-the-screen), step 4). Selection highlighting is for what the user chose, not for what is finished.
- **Order of work:** build the hierarchy first (size, color, spacing, placement, containment), *then* add unique emphasis (shape, scale, morph) to celebrate success or progress.

#### Google's worked example: the Aura breathing app

Each screen spends emphasis by goal rank. Use this as the reasoning model.

| Screen | Rank | Emphasis |
| --- | --- | --- |
| Home | Primary: start a session | Extra-large "Start breathing" button in dark `primary` on a soft surface, low on screen. Settings grouped as list items in `secondary`. Daily message in a soft container, least emphasis. |
| Session | Hero moment | A screen-filling flower shape (`MaterialShapes.Flower` and `Sunny`) grows and shrinks with each breath on spring motion; vibrant yellow on inhale; huge countdown numerals against small labels; pause/stop small at the bottom; navigation bar hidden. |
| Report | Secondary | Fewer tactics "to reduce cognitive load": metrics in uniform flower shapes, emphasized numbers, a medium (not XL) Finish button. |
| Progress | Tertiary | Subtle: key data in `primary`, completed days as small secondary shapes, numbers "large enough to scan, but they don't dominate." |

Their v1-to-v2 lesson: ungrouped settings of similar size and inconsistent color competed for attention; grouping them above one extra-large button went "from cluttered to calm."

### Hero moments and restraint

> "Hero moments use multiple expressive tactics to break from predictable or uniformly applied design ideas."

- A hero moment layers type, shape, color, motion, and flexible components on the product's key interaction: the Phone dialer, a media player, a completed goal, a breathing session. Ask: *is it emotionally impactful?* and *is it a key interaction?*
- **One or two per product.** They're "brief, delightful, surprising, and unexpected"; more than that overwhelms. Secondary screens use fewer tactics.
- In a hero moment, **one custom thing moves**: keep text stable while the shape animates (Google). Built-in component morphs (a button changing shape on press) don't count.
- **When content is the product, the content is the hero.** In players, galleries, and trips, give the album art or photo scale and let its color set the screen. A library-shape mask, a full bleed, or a title layered over the image are options, not requirements: an ordinary rounded crop is just as strong when the composition around it carries the idea.
- **Keep familiar patterns.** Expressive styles the patterns; it doesn't replace them. In Google's tests, a playlist rebuilt as scattered album art "looked modern and exciting" but people didn't recognize it as a playlist, and removing text labels from email actions hurt usability. Context matters too: what suits a media player may not suit a banking app.
- "No amount of emotion can compensate for a lack of clarity." Expressive sharpens a screen that already works; it doesn't rescue a confused one.

### Color

- **The generator makes the palette; you assign the roles.** Material's color utilities turn one source color into the accent, surface, light, and dark roles (Google). Take the generated palette as it comes and spend the design effort on which element gets which role.
  - *Dynamic* (wallpaper) is Google's recommendation and gives personalization. The M3 Expressive update made dynamic color richer at the source ("higher chroma across all hues"); apps get it automatically. The app shares hues with the rest of the phone, so its identity comes from hierarchy, shape, and type.
  - *Brand* gives the app its own identity: a scheme generated from the brand color with Material Theme Builder, or with MaterialKolor at runtime at the default palette style (theming reference). Keep the default palette style: MaterialKolor's `PaletteStyle.Expressive` is a hue-shifting scheme variant unrelated to M3 Expressive, and it pulls the palette away from the brand's hue.
  - *Content-based* colors a contained area from an image on screen (album art, a photo). Limit a screen to two color sources and keep the source image visible (Google).
  - `expressiveLightColorScheme()` is only the light fallback when dynamic color is unavailable, as in Google's `MaterialExpressiveTheme` sample.
- **Accents mark meaning.** "Accent colors usually exhibit the most expressiveness within a UI, whether it's for branding, highlighting actions, personal expression, or user expression." Apply them by importance: primary to crucial actions (the FAB), secondary and tertiary "down the hierarchy." "Use all accent colors mindfully, taking into account that the human eye is particularly drawn to vibrant colors." (Google)
- **Different jobs get different roles.** Use "a variety of primary, secondary, and tertiary accent colors for hierarchy and distinction": action (`primary`), selection (`secondary`), status or delight (`tertiary`). Google's example: data in `primary`, progress accents in `secondary` yellow.
- **Surfaces are most of the screen.** Surface colors "represent the majority of your app's colors. Don't be shy to use lots of surface space; the human eye needs space to relax." (Google) Build hierarchy with surface steps and put accent containers only on elements with a job (the hero, a selection, a key status), not on every card.
- **Apply roles only in their intended pairs or layering orders** (Google's rule): `onX` on `X`; `onSurface`, `onSurfaceVariant`, and `primary` on surfaces; `inverseOnSurface` and `inversePrimary` on `inverseSurface`. Containers are fills, never text colors. Default text is `onSurface`; `onSurfaceVariant` for lower emphasis.
- **Lower emphasis on text or icons by stepping down to a quieter role** (such as `onSurfaceVariant`), never with `copy(alpha = ...)`, which breaks the contrast the role pairs guarantee.
- **Surfaces:** `surface` for the body, `surfaceContainer` for navigation regions, and the five container levels for nesting. The most important container gets the brightest surface.
- Dividers use `outlineVariant`; text field borders use `outline`.
- **Surface steps:** use each component's prescribed surface mapping (search, for example, specifies containers "more than one step apart"; see the components reference). For custom groups, use a surface difference when the boundary needs emphasis; proximity and alignment can group without another fill.
- **Vibrant** component styles are high emphasis; use them sparingly ("Vibrant menus are more prominent, and should be used sparingly"). Vibrant menus are tertiary-based; vibrant toolbars use `primaryContainer` ([references/components.md](references/components.md#toolbars)).
- Semantic colors (error red, a success green defined as a static color) never come from content color, and keep one meaning everywhere: "if you establish a pattern, repeat it throughout the app." (Google)
- **Inverse containers** (`inverseSurface` / `inverseOnSurface`) reverse one element out of the screen, like a snackbar or a total next to lighter metric cards.
- **Color can follow state:** a scheme derived from the app's content or context (the sky in a weather app, album art in a player) is content-based color at screen scale. Offering the seed and palette style (and a pure black dark mode) as user settings is common in shipped Expressive apps.
- **One strong fill: the hero, or one coherent group** (default). A set of related filled controls can read as one unit; unrelated saturated cards side by side read as noise, not hierarchy. A hero screen still mixes two or three container roles (default). Google: "Mixing these colors for key components or visual elements can help emphasize the main takeaway of a screen." Give the few key elements with distinct jobs their own accent container (`primaryContainer`, `secondaryContainer`, `tertiaryContainer`, or an inverse surface): a key metric, a selection, a status. Everything else stays on surfaces ("Create visual hierarchy with surface tones"), so a list of cards does not get one accent each. The cap counts what renders saturated, not role names: in testing, a content-based or vibrant scheme renders container roles near full strength, so read the rendered color (a proposal's `check_proposal` `colors`, or the layout tree's hex), and if an accent container comes out as strong as the hero's fill, move it to a surface or a quieter role.
- **Category colors** need clearly different hues so each is recognizable at a glance. Two can use `primaryContainer` and `tertiaryContainer` (tertiary sits at a different hue; secondary shares primary's hue at lower chroma, so it reads as the same color); more get a static color each (four roles from one seed, not harmonized, since harmonizing pulls hues together; recipe in [references/theming.md](references/theming.md#extra-colors-semantic-and-categories)), never an improvised hex. Color the badge or icon, not a whole card, and give each category one visible color across the screen: every mark of a category (bar segment, legend, badge) uses the same role, not a solid color in one place and its pale container in another.
- **Charts and data graphics** use the solid roles (`primary`, `secondary`, `tertiary`, a static color's main role), not containers: graphics need 3:1 against their background (Google), and pale containers disappear.

### Typography

- Use the role scale: **Display** for short important text and numerals, **Headline** for short high-emphasis text on phones, **Title** for secondary regions, **Body** for reading, **Label** inside components. Most screens need about five styles; pick sizes with clear contrast between them, not near-duplicates.
- **Emphasized styles** (`MaterialTheme.typography.displayLargeEmphasized` through `labelSmallEmphasized`) are heavier variants. Components don't use them by default; apply them to the primary button label, selected items, unread items, key numbers, and headlines. "Give extra impact to a headline, or subtly strengthen text of the same size."
- **Google Sans Flex for plain text and by default** in phone, tablet, and desktop apps (this skill's standard, not a Google requirement). Six variable axes: weight, width, optical size, slant, grade, and roundness (`ROND`); ranges, bundling, and per-style axes are in [references/theming.md](references/theming.md#google-sans-flex).
- **Optionally one brand face for Display, Headline, and Title Large.** Material's type scale has a brand typeface "used for larger type styles, like Headline and Display, to focus on expression" and a plain one "used for smaller type styles, like Body and Label, to focus on readability", and says "Consider replacing Roboto with different typefaces to boost brand expression in your product." Pick at most one from this skill's bundled set (Fraunces, Bricolage Grotesque, Big Shoulders Display, and Doto at Display only) by the direction it serves; the set, each face's character, and how to set it (including `titleLarge`, which small app bar and side sheet titles draw in) are in [references/theming.md](references/theming.md#brand-faces-display-headline-and-title-large-only). Title Medium and Small, Body, and Label stay Google Sans Flex.
- **Google Sans Code for numbers and data** (timers, tabular values, codes, metadata), at any size, in any proposal; it is a mono face that pairs with any of the above.
- Brand faces change character, not size: keep the scale's sizes and adjust line height and tracking ("Avoid changing the type size; this can affect how components render and reflow").
- **Expressive voices on large styles, the text voice on small:** give Display and Headline the voice that serves the direction; keep Body and Label on default axes so they stay highly readable. Be careful at Title.
- **The hero title or number needs a real voice.** With Google Sans Flex (default) the character comes through strong axis settings (heavy weight, very narrow or very wide width, or high roundness); a medium weight at a middle width looks like any sans. With a bundled brand face, use it at Display or Headline size on purpose (its own axes, weight, tracking), not as a regular-weight swap. Keep the calm voices for secondary text.
- **Axes carry feeling and meaning.** Google describes weight as ranging from "calm as a whisper" to "loud and rugged", roundness as "personal, playful", and taller, narrower styles as more premium and engaging. Axes also carry state: heavy in a filled container for the selected item, light for the rest, at the same size so nothing reflows. Grade adds emphasis without changing width.
- **Always match optical size to the text size.** It reshapes letters to stay legible at every size; one setting across Display and Label hurts both. Set `opsz` per style (see the theming reference).
- **Pick voices, not random axis values.** Define each voice once as a style and reuse it; two or three per app, each with one job. Starting points for Google Sans Flex voices and the brand faces are in [references/theming.md](references/theming.md#google-sans-flex); tune them to the direction rather than copying the nearest preset.
- **Editorial treatments** let type dominate a hero moment: a huge number, an album title over a photo, text that widens as a slider rises. Keep them consistent, match the emotion (narrow and light for calm, bold and wide for energy), and keep labels in the plain text voice.
- **Contrast inside one line:** two voices in the same phrase can carry meaning, such as a flight's origin light and condensed and its destination heavy, wide, and slanted ("PDX › SFO"). The line reads as past and future without extra UI.
- **Type as graphic:** oversized words or numbers cropped by the screen edge, or tinted close to their background ("68" behind a weather summary, a trip name behind the traveler). When text becomes art, repeat the information readably elsewhere and hide the decorative copy from accessibility services (`Modifier.clearAndSetSemantics {}`).
- **Number plus unit:** a huge numeral with its unit in a small label style on the same baseline ("15 min", "0%", "68°"): put both in a `Row` with `Modifier.alignByBaseline()`.
- Line height about 1.2x on large styles (about 1.25x for heavy or narrow custom voices, measured), 1.5x on body. Tabular numbers (`fontFeatureSettings = "tnum"`) for timers and changing values. Sentence case everywhere.

### Shape

- **Corner scale:** 4, 8, 12, 16, **20**, 28, **32**, **48**dp and full (`MaterialTheme.shapes.extraSmall` to `extraExtraLarge`; the bold ones are Expressive additions). Buttons default to full; cards to medium.
- **Tension creates focus.** Mix round and square; "break from the surrounding shape style to draw attention to a particular element." Material "historically focused on rounded shapes"; sharp contrast is more memorable.
- **The primary control contrasts in shape with its neighbors** (default). In a cluster of controls (player controls, a button group, a toolbar), make the primary a rounded square among fully round secondaries, or the reverse, at a larger size. Google: "Add unexpected moments by switching between square and fully rounded shapes."
- **Shape signals state.** Expressive buttons, icon buttons, toggles, and list items morph on press and selection (round to square or back). Use the components' `shapes` parameters to get this for free.
- **The shape library** (`MaterialShapes`: Cookie9Sided, Sunny, Flower, Clover4Leaf, Burst, Pill, Heart, and 28 more) is for avatars, image crops, decorative graphics, achievements, and a bespoke hero button. Not for text-heavy containers. "Shapes without clear meaning... add more visual clutter than delight."
- **Abstract library shapes as masks on imagery are the normal use.** Photos, album art, avatars, and other non-interactive imagery take them freely: Google says "Use abstract shapes on imagery and decorative UI" and "Get creative when using shape in graphics, for photography cropping, personalized avatar masking, and other non-interactive elements." A mask needs no depicted meaning.
- **A standalone decorative graphic needs a reason from the subject.** This applies to shapes drawn as their own element, not to masks. Google: "Ensure that shapes resonate with the product's narrative." A sun and cloud on a weather screen, a setting sun for a meditation app, and album art cut into a scalloped record label all depict something; a blob or ripple that depicts nothing is clutter. When a shape depicts an object, keep it recognizable (default): give it the object's color as a static color ([references/theming.md](references/theming.md#extra-colors-semantic-and-categories)) instead of a pale scheme role chosen to quiet it, and make it smaller or crop it if it competes with the hero.
- **Uniform among peers:** equally important data meant for comparison (metrics, calendar days) uses the same shape and size, evenly spaced, without overlap (Google: "Use uniform shapes and sizes"). Vary scale or form when the data has a deliberate hierarchy, keeping items aligned and comparable. Decorative layering, such as type over an image, is fine when controls and text stay clear.
- **Optical roundness:** nested radius = outer radius minus padding (28dp card with 12dp padding holds 16dp corners).
- Grouped items use small inner corners and large outer ones (segmented lists: 4dp inner, 16dp outer; selected morphs to 16dp all around).

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
Image(painter = avatar, contentDescription = null, contentScale = ContentScale.Crop,
    modifier = Modifier.size(96.dp).clip(MaterialShapes.Cookie9Sided.toShape()))
```

Morphing between two library shapes: see [references/theming.md](references/theming.md#shape-morphing).

### Motion

Material motion is spring physics, themed through `MotionScheme`:

- **Spatial** specs (position, size, rotation, corner radius) overshoot and settle. **Effects** specs (color, opacity) never overshoot.
- Speeds: **fast** for small components (buttons, switches), **default** for partial-screen motion (sheets, rails), **slow** for full-screen changes.
- Custom components use the theme instead of `tween()`, so they match Material components and follow scheme changes:

```kotlin
val scale by animateFloatAsState(if (pressed) 0.94f else 1f, MaterialTheme.motionScheme.fastSpatialSpec())
val tint by animateColorAsState(if (selected) colors.primary else colors.surfaceContainerHigh,
    MaterialTheme.motionScheme.defaultEffectsSpec())
```

- Spring values for both schemes: [references/theming.md](references/theming.md#motion).
- **Expressive** is the default choice and belongs on hero moments. **Standard** suits utilitarian products. Override a subtree by nesting `MaterialTheme(motionScheme = ...)`.
- Springs are interruptible and carry velocity when retargeted; input stays live during every animation.
- **Screen transitions stay simple.** Bounce belongs to components and hero moments. Use container transform for card or list item to detail only in hero moments and shallow hierarchies ("Don't use container transform in apps with deep hierarchies"); platform-default forward/backward for everyday hierarchy; a quick fade between top-level destinations, never a lateral slide (it conflicts with carousel and list gestures). (Google) Fade content out fully before fading new content in; never fade a bottom sheet.
- **Reduced motion:** swap to a scheme whose specs `snap()` (Google's own pattern) and drop decorative morphs and parallax; keep meaningful fades.

### Spacing and layout

- **Spacing sets the mood.** "A denser layout can feel more serious and focused, while a more spacious layout can feel calm and open." Negative space around the primary element is emphasis.
- Use an 8dp scale (4, 8, 12, 16, 24, 32, 48). Put padding and gaps on parents, not margins on children. Compact screens use 16dp side margins; medium and up 24dp.
- **Group with gaps and containers instead of dividers.** Expressive lists, menus, and search results separate groups with gaps between filled items; dividers are for uncontained lists only.
- Keep reading text at 40 to 60 characters per line.
- **Adapt by breakpoint** (600 and 840dp): compact is one pane with a navigation bar, expanded and up is two full-height panes with a navigation rail, and each step up reveals what your adaptation answer named. Read [references/layout.md](references/layout.md) for every multi-size layout: the breakpoint table, tall medium windows (foldables and tablets held upright), canonical layouts, landscape, and desktop windows with mouse and keyboard.

### Components

Stock code reaches for the left column. Lint won't flag it.

| Instead of | Use | Compose |
| --- | --- | --- |
| Medium/large top app bar | Flexible app bar (shorter, bigger title, subtitle) | `MediumFlexibleTopAppBar`, `LargeFlexibleTopAppBar` |
| Bottom app bar | Floating or docked toolbar | `HorizontalFloatingToolbar` (FAB overload), `FlexibleBottomAppBar` |
| Segmented buttons | Connected button group | `Row` of `ToggleButton` with `ButtonGroupDefaults.connected*ButtonShapes()` |
| Navigation drawer | Expanded navigation rail | `WideNavigationRail`, `ModalWideNavigationRail` |
| `NavigationBar` | Flexible navigation bar | `ShortNavigationBar` + `ShortNavigationBarItem` |
| Small FAB, speed dial | Medium/large FAB, FAB menu | `MediumFloatingActionButton`, `FloatingActionButtonMenu` |
| Spinner for short waits | Loading indicator (200ms to 5s) | `LoadingIndicator`, `ContainedLoadingIndicator` |
| Plain progress bar | Wavy progress where expressiveness fits (default strokes) | `LinearWavyProgressIndicator`, `CircularWavyProgressIndicator` |
| `ListItem(headlineContent=)` with dividers | Segmented expressive list | `SegmentedListItem` spaced by `ListItemDefaults.SegmentedGap` |
| Flat dropdown menu | Grouped vertical menu | `DropdownMenuPopup` + `DropdownMenuGroup` |
| One-size buttons | Sized, morphing buttons (XS 32 to XL 136dp) | `Button(shapes = ButtonDefaults.shapesFor(height))` |

- **App bar vs toolbar:** "Where app bar supports navigation, toolbar provides critical actions for the current page." App bars get one action (two at most), boosted with a filled or tonal icon button; page controls (such as lyrics and queue in a player) go in a floating toolbar of icon buttons or in the app bar within its one or two actions, never as loose text buttons. A floating toolbar can instead be local navigation when the selection swaps the content in place (labeled items with one selected); a screen shows either a toolbar or a navigation bar, never both ([references/components.md](references/components.md#toolbars)).
- **One FAB per screen** for the single most important action; not every screen needs one. An action that belongs to one card or section (logging water in a water card) is a button inside that container: "individual components, such as cards, shouldn't have their own FAB," and FABs aren't for minor actions (Google). When a screen's only action belongs to one section, it has no FAB.
- **Button groups:** same size and shape by default; mixed sizes only in hero moments.
- Read [references/components.md](references/components.md) when choosing a component, writing one you haven't used in this session, or customizing one (use as-is, wrap, style, or fork).

### Accessibility and writing

- Contrast 4.5:1 for small text and 3:1 for large text, icons, and controls. Correct role pairs give this automatically, including in medium and high contrast modes; generated or hand-made schemes must read the system contrast setting ([references/theming.md](references/theming.md#contrast-levels)).
- Pair color with an icon, label, or underline for every state and link.
- Touch targets 48dp with 8dp between them. Support 200% text scaling: text grows, padding doesn't, layouts reflow. Icons, checkboxes, and progress indicators keep their size as text scales. An ellipsis is acceptable only when the full text is reachable (tooltip, link, or expanded view); otherwise wrap (Google).
- Content descriptions state purpose ("Voice search"), not appearance, and never the role.
- Sentence case, second person, no periods on single-sentence labels, contractions, exclamation points only for real celebrations.

### Android conventions

Material says how components look; Android's own design guides say how an app behaves on the platform. Generated code often carries iOS habits instead (Google, "10 steps to Android"):

| iOS habit | Android |
| --- | --- |
| Centered navigation title by habit | Start-aligned title by default (centered is valid when the composition calls for it); large titles are flexible app bars that collapse on scroll |
| Back chevron; "Cancel" and "Done" text in the top bar | Up arrow for hierarchy (system back handles "back"); a close icon to dismiss full-screen modals, with the confirming action in their app bar. Dialogs keep their labeled text buttons |
| Action sheets | Bottom sheets |
| Segmented control | Tabs for peer content destinations; a connected button group for options or view modes within one screen |
| Table rows with disclosure chevrons and hairline dividers | List items without chevrons, grouped with gaps ([Spacing and layout](#spacing-and-layout)) |
| SF Symbols | Material Symbols, one style (outlined, rounded, or sharp) app-wide |

- **Edge-to-edge:** backgrounds, images, and scrolling content draw behind the system bars; text and controls stay inset. The gesture bar stays transparent. The status bar is transparent unless content scrolls under it, then it gets one protection (Material top app bars already provide it). Keep tap targets clear of the system gesture insets. Pin text inputs above the keyboard. Implementation: the `edge-to-edge` skill.
- **Settings, onboarding and sign-in, permissions, notifications:** read [references/android-conventions.md](references/android-conventions.md) when the work touches a settings screen or where Settings sits in navigation, onboarding, sign-in, a permission request, or a notification.
- **Support landscape, window resizing, and both light and dark themes** on every screen; never lock orientation or theme.
