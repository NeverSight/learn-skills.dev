---
name: tactile-design
description: Design-engineering rules and the decision process behind tactile, layered, quiet product UI. Use when building, restyling or reviewing product interfaces such as dashboards, settings pages, onboarding flows, forms, modals and bottom sheets, menus, tables, cards, toasts, buttons and motion; when deciding primary versus secondary actions, how much data to show, where controls go or how hierarchy should read; when making UI feel tactile and layered in both light and dark mode; or when adapting this system to any typeface, brand colours and data.
---

# Tactile design

Interfaces built with this skill feel physical but quiet. A soft ground. White surfaces raised by a fine ring and a crisp drop. One black action that says "do this next". Controls that squeeze when pressed. Motion that is quick and has a reason. Hierarchy comes from contrast steps, not from bold text, big size jumps or colour.

Everything is written as **roles and ratios** ("ink-12", "the -3 tint with its -11 text", "one step above its ground"). The concrete numbers are the defaults, taken from a production dashboard built on a warm 12-step neutral (Radix sand) and Inter. To use your own palette and typeface, remap the tokens in [tokens.md](references/tokens.md) and keep the roles.

**Vocabulary**

- `ink-N`: step N of your 12-step neutral. 1–2 grounds, 3–5 fills, 6–8 lines, 9–10 faint text, 11 secondary text, 12 strong text.
- `hue-N` (or `accent-N`, `red-N`, `green-N`): step N of a coloured 12-step scale. 3 tint fill, 6 edge, 9 solid, 10 solid hover, 11 text.
- **Ground** (the parent): what a thing sits on. A thing's fill, edge and drop are taken from it. **Raised**: above its ground. **Well**: sunk into it. **Overlay**: floats over the page.
- **Phone**: viewport under 768px. **Touch**: coarse pointer (phones and tablets).

## Operating posture

- **Smallest change that fixes it.** Move in 2px, one ink step, or 5% of opacity or scale. Don't redesign when a nudge will do.
- **Reuse before inventing.** Find the recipe the product already uses and match it exactly: its role constants (button, pill, sheet and table class strings) first. Stock library primitives are legacy unless they already carry the recipe. A new component needs a reason.
- **Remove before adding.** Borders, containers, separators, icons, eyebrows, repeated words. Decoration (gradients, patterns, glows, stripes) nearly always comes back out.
- **Match the neighbour.** Siblings share height, padding, radius, text size and ink. An unmatched sibling is a bug.
- **Borrow from the parent.** Tactility is never absolute. A control's fill, edge and drop come from the surface it sits on, so it reads equally pressable on a panel, card, rail, table row, sheet or tint, in both themes.
- **A rule is global.** Once a rule is decided, apply it to every instance in the same change. Audit; don't fix one.
- **Light first, dark on purpose.** Elevation is designed per theme. Sizes, spacing and shapes never fork. A light-mode restyle doesn't touch dark unless dark is named.
- **Show only what this state needs.** New and returning users can see different pages. Never show fake data.
- **Check at zoom.** 4–8×, both themes, worst-case data, every state, before calling it done.
- **Plain words.** In the UI and in your replies. Short bullets, no walls of text.

## The decision order

Work top to bottom. Each step constrains the next. Most weak UI comes from starting at step 4.

1. **Hierarchy: what must the user do first?** Name the single next step on this surface. That is the one primary (black) action, or there is none. Rank everything else below it: secondary (white, raised), utility (round pill or icon), tertiary (ghost or underlined text). Destructive is never the primary.
2. **Amount of data: the least that answers the question.** One strong figure beats six small ones. Lists stop at 5–6 rows, then a pager or "View all". Hide sections that are empty, finished or not yet relevant. Don't repeat what a heading already says.
3. **Placement.** Pick the column by page type: 800px to read, 1200px for data, 440px for a form or flow. A section's actions sit at the right of its title, above the data they act on. Paging sits below the data, outside its card. A control sits next to what it sets.
4. **Component.** Button role by weight (step 1). Plain rows for lists and navigation, a card for one unit of related data, a table for many records. Inline first. A modal only for a focused task or a confirm; on a phone it becomes a bottom sheet. A toast only for a result the user can't otherwise see.
5. **Surface and layer.** Decide the ground, then raise or sink, taking fill, edge and drop from that ground. Light: raised = white + 1px ring + a crisp 1px drop. Dark: raised = one or two steps lighter + one solid 0.5px outline + a tight black drop. Fields are wells. Overlays are white in light, with a crisp shadow in both themes.
6. **Type and spacing.** One weight. Hierarchy is a size step plus an ink step (12, 11, 10). 13/20 body, 16/24 card and dialog titles, 20/28 section titles. 4px grid: 4–8px inside a control, 12–16px between items, 24–32px between sections.
7. **Colour roles.** The neutral carries structure. Hue carries meaning only: a status (success, danger, warning, info) or an identity (a category or tier), as the -3 tint with -11 text. Status wins a clash. Hue never ranks importance and fills no button except the final destructive confirm (red-9) and an opted-in accent primary.
8. **Motion gate.** Should it move at all? The more often it's seen, the less it moves. If it moves: name one purpose, animate transform and opacity, use the strong ease-out, 150–300ms, exits faster than entrances, and ship a reduced-motion version.
9. **Phone.** 44pt targets, 15px text floor (fields 16px), 20px gutters, stacked full-width actions, dialogs as sheets, nothing that only shows on hover.
10. **Review.** Zoom in on both themes. Look for 1px seams, double borders, mismatched radii, wrapped or cropped labels, layout that jumps, and siblings that don't match.

## Rules at a glance

### Tactile treatment

Every part comes from the parent, the surface the thing sits on. The tactile tokens are built from working steps, so redeclare them on each surface class or the edge won't follow ([tokens.md](references/tokens.md) §3).

| Part | Light | Dark |
|---|---|---|
| Fill | `--surface-top` | parent + 2 steps for controls, + 1 for cards |
| Edge | 1px `rgb(ink / .08)` ring over whatever is beneath (`.07` on cards and modals) | one solid 0.5px outline lighter than the fill, three steps above a control's fill (ink-7 on an ink-4 control; ink-6 on cards), the same colour all round; never a lit top edge |
| Drop | `0 1px 2px 0 rgb(ink / .12)` | `0 1px 2px 0 rgb(0 0 0 / .5)`; always darker than the parent, never a glow |
| Badge edge | its own colour: 1px ring at 14% + the drop at 16% of its text colour | solid 0.5px `color-mix(in srgb, currentColor 34%, #000)` + the black drop |

- **Crisp, not blurry.** Every shadow is the ring and the 1px drop plus at most one short drop: card `0 3px 4px -2px`, menu `0 4px 8px -4px`, modal `0 6px 8px -4px`. No big soft blurs.
- **White on white** (a secondary button on a white card, a neutral badge) gets its edge from the ring and drop, never from a fill change.

### Type and ink

| Role | Default | Rule |
|---|---|---|
| Weight | one weight (Inter at Medium) | For another face, pick it with the weight test in "Typeface fit" ([tokens.md](references/tokens.md)). Bold is rare emphasis. |
| Body, controls | 13/20; values ink-12, descriptions ink-11 | 13px, not 14 |
| Meta | 12/16, ink-10 | timestamps, footnotes, "/ total", "(optional)" |
| Card, dialog title | 16/24, ink-12 | |
| Section, in-column page title | 20/28, ink-12 | 13/20 ink-11 description 4–6px under it |
| Top-strip page title | 13/20, ink-12 | centred in the 52px strip |
| Display | 32/40, −0.02em | lead words ink-11, key noun ink-12 |
| Button labels | −0.01em tracking | |
| Mono | IDs, code, keys, machine values only | a table keeps one typeface |

### Buttons and controls

| Item | Default |
|---|---|
| Primary | `--primary-bg` (ink-12) fill, `--primary-fg` (ink-1) text; light adds a 1px ring in the surface colour, dark a 0.5px ring in its own fill + the black drop; hover `--primary-hover` (a 7% mix toward the text colour); one per surface |
| Accent primary | opt-in only, when the brand requires it: accent-9 fill, accent-contrast text, accent-10 hover; that hue leaves status use |
| Secondary | light: white + `--shadow-button`, no border. Dark: two steps above its ground, a solid 0.5px outline three steps above its fill (ink-7 on a card) + the black drop |
| Utility pill | fully round, 28px, white + the button shadow; belongs to content (copy, filter, back) |
| Badge | fully round; hue-3 fill, hue-11 text, `--shadow-badge` from its own colour (above). A neutral status is white with `--shadow-button`; in dark one step above its parent with the control's outline and drop |
| Copy | the icon turns to a tick on the click, before the clipboard answers; reverts, or says "Copy failed", if it refuses; no toast |
| Destructive | trigger: white with red-11 text; final confirm inside its dialog: solid red-9 with red-contrast text |
| Heights | 36px desktop, 44px phone; 32 compact, 28 pills, 24 inline, 22 row icons, 20 badges, 18 key chips |
| Radius | 6px for controls (set to match your icon set; the ladder follows), full for pills and badges |
| Padding | 12–14px a side; the side with a leading icon is 2px tighter |
| Press | `scale(.97)`, 150ms; smaller targets squeeze more (.92 at 22px), cards less (.99) |
| Field | a well: ink-3 fill, no border; focus deepens to ink-4, plus the focus ring for keyboard focus |
| Focus | one token on every control, `--focus-ring` (ink-10), drawn 2px: 3:1 on white, wells and dark surfaces; never a hard-coded dark alpha |
| Field error | 1px red-11 ring as a box-shadow; 12/16 red-11 message under it; validate on blur and submit |
| Disabled | `.6` buttons, switches, fields; `.4` icon buttons; dark primary goes solid ink-4 / ink-8 |
| Loading | label swaps in place to spinner + "Saving…" in the same button |

### Surfaces

| Item | Default |
|---|---|
| Ground | ink-2 in light; below ink-1 in dark (#080807 with sand) |
| Panel | white in light, ink-1 in dark; floats 8px off the window; radius 8 |
| Raised card | light: white + `--shadow-card`; dark: ink-2, a solid 0.5px ink-6 outline + the black drops; radius 8. Charts and settings groups too. A confirm shown in place takes `--shadow-button` |
| Hairline | 0.5px ink-6; one step darker in dark |
| Overlay | white in light, ink-2 in dark, radius 8; the shadow's ring is its edge: `--shadow-menu` or `--shadow-modal` |
| Menu | trigger: the secondary button, chevron turns over while open; 36px items 2px apart; highlighted item local ground + 1, chosen item local ground + 2 in ink-12, no tick |
| Backdrop | black 30% (light), 90% (dark), 2px blur |
| Modal | 620px default, 460px confirm; header 20/20/16, body 16, footer 12; Cancel left, confirm right; focus the first field, trap Tab, lock scroll |
| Side panel | 400–480px, modal structure, overlay surface, no dim unless fullscreen; a sheet on a phone |
| Table | 38px rows, 0.5px frame and column dividers, radius 8, `--shadow-table`, 12–16px cells; white rows (stripes only on long tables: white/ink-2, dark ink-2/ink-3); header and first column ink-12, other cells ink-10 (ink-11 if it misses 4.5:1); every cell left-aligned, one typeface, tabular figures; status as a dot in its hue; the frame hugs the last row |
| Toast | one at a time, bottom centre, tinted pill; never for a copy |

### Layout

| Item | Default |
|---|---|
| Columns | 800px read, 1200px data, 440px form or flow |
| Section | title 20/28, 6px, description, 24px, content; 32px above and below |
| Actions | right of the title, above the data; under the title at full width on a phone |
| Lists | 5–6 rows, then a pager under the card or "View all" after it |
| Figure | 24/32 ink-12 number, 13/20 ink-10 label directly under it (ink-11 if ink-10 misses 4.5:1) |
| Empty | bare centred ink-2 panel, 18px icon, two lines (ink-9, or ink-11 where ink-9 misses 4.5:1): what's missing, what to do |
| Failed load | the empty layout, two lines, one secondary "Try again" |
| Worst-case data | free text truncates past 32ch with a tooltip; figures over 6 digits go compact; missing values are an en dash |

### Motion

| Item | Default |
|---|---|
| Curve | `cubic-bezier(.23, 1, .32, 1)` for anything the user caused, hover and colour included |
| Hover | colour only, 150ms, fine pointer only; each row fades its own fill in place, never one highlight sliding between rows |
| Menu | in 150ms from `scale(.97)` + fade, origin at the trigger; out 120ms |
| Modal | in 240ms (16px rise, 4px blur, fade), out 200ms |
| Sheet | up 320ms, down 200ms, solid the whole way |
| Springs | `{ bounce, duration }`: .12 / 0.4s for every toggle's sliding pill and .2 / 0.45s for a switch knob, so the overshoot stays inside the track's inset (a pill travelling 100px at .35 overshoots ~7px, past a 4px inset, and is seen hitting the edge); up to .45 for rare celebrations |
| Reduced motion | travel, blur and scale become a 150–200ms crossfade; a switch knob moves at once |

### Phone

| Item | Default |
|---|---|
| Targets | 44pt; small visuals keep their look and get an invisible 44×44 hit area |
| Text | 15px floor for body, controls and meta; 14/20 for descriptions under a larger lead; 16px in fields |
| Fields | 44pt tall, 16px text on any touch screen (iOS zooms into a field set smaller and stays zoomed); 36px at body size with a mouse |
| Toggles | segmented: a 42px track, 34px options in the 4px inset, 44pt to a finger; switch: an iPhone's (Apple HIG), 51×31 with a 23px knob 4px in; at a row's end, as far from its right edge as the toggle is from the row's top and bottom |
| Gutter | 20px each side |
| Stacking | full width; page stacks keep 12px, dialog and sheet footers 8px; a dialog's confirm goes on top |
| Dialogs | bottom sheet, white in light, 14px top corners; a white tactile grab handle (36×5, the button's ring and drop, 44pt hit area) instead of ×, and a tap on it closes the sheet |
| Sheet drag | from anywhere once a press moves 4px; closes past min(64px, 15% of its height) or on a 0.11 px/ms flick, else springs back |

## Never ship

- [ ] More than one primary on a surface, or a primary that isn't the real next step
- [ ] A grey filled button in light mode, more than one coloured fill on a surface, or a brand colour on anything but an opted-in accent primary
- [ ] A destructive action styled as the primary
- [ ] A dark-mode style that changes padding, height, radius or border width
- [ ] A shadow as the only elevation cue in dark mode
- [ ] A fill, edge or drop set as a fixed value that ignores the surface beneath it
- [ ] A big, soft shadow blur
- [ ] In dark: a lit top edge, an outline that changes colour round the edge, an edge over 0.5px, or a shadow lighter than its parent (a glow, such as a badge's text colour used as its shadow)
- [ ] Double borders, or an inner radius that isn't the outer radius minus the border
- [ ] Structural lines thicker than 0.5px
- [ ] Hierarchy made with bold, or with colour
- [ ] Text the user must read to act under 4.5:1 contrast
- [ ] Actions placed below the data they act on (paging is the exception)
- [ ] A pager or action buttons inside a table's card
- [ ] Fake data, or a wrong label shown while loading
- [ ] Layout that jumps when data, a label or a loading state arrives
- [ ] An eyebrow label, "Step 1 of 4" over a progress bar, or a warning icon before an alert title
- [ ] Title Case labels, three dots instead of "…", em dashes in UI copy
- [ ] A toast for a successful copy, or a copy tick that waits for the clipboard
- [ ] A tick on the chosen menu item
- [ ] One hover highlight that slides between rows
- [ ] `transition: all`, ease-in on UI, scaling from 0, or keyframes on something that can be re-triggered
- [ ] Animation on keyboard actions, drag, resize or data figures
- [ ] A transition with no reduced-motion path
- [ ] Hover-only information, or hover styles that stick on touch
- [ ] Touch targets under 44pt, fields under 16px on touch screens, scrollbars or rubber-banding on a phone
- [ ] Not checked at 4–8× in both themes

## References

Open the file for the area you're working on. Each pairs the default value with the role or reason, so it transfers.

- [tokens.md](references/tokens.md): the role-based token system, default values, the surface step-shift rule, contrast gates, and how to remap to any palette and typeface (typeface fit, a CSS template and a Tailwind mapping).
- [buttons-and-controls.md](references/buttons-and-controls.md): choosing a button role, recipes, sizes, states, fields, toggles, switches, choice rows, badges, labels.
- [surfaces-and-layering.md](references/surfaces-and-layering.md): layers, shadows, light vs dark elevation, shell, modals, sheets, menus, toasts, cards, tables.
- [layout-and-hierarchy.md](references/layout-and-hierarchy.md): columns, rhythm, proportion, placement, amount of data, figures, steps, badges, empty and loading states, copy.
- [motion.md](references/motion.md): the motion decision order, curves, durations, springs, patterns with values, reduced motion.
- [mobile.md](references/mobile.md): breakpoint, touch, type floor, stacking, sheets and drag, phone tables, native feel.
- [decisions.md](references/decisions.md): the designer's recurring decisions and the reasons behind them; pitfalls; how to handle a new request; a worked example.
