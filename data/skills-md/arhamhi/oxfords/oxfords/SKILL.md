---
name: oxfords
description: Use when building, changing or reviewing any interface a person operates - dashboard, admin panel, table, form, settings, modal, onboarding, mobile app screen, landing page - or when a UI looks AI-generated, cluttered, generic, "vibe coded", over-decorated, unfinished, or hard to scan. Also use when asked to remove AI slop, make a UI clean, plain, polished or professional, fix the UX, or check a build before shipping.
license: MIT
---

# Oxfords

Oxfords, not brogues. An Oxford is the plain shoe. A brogue is the same shoe with decoration
punched into it. This skill makes interfaces that are polished, plain and finished, and
removes the decoration that marks a screen as machine-made.

It does not make a product look striking or give it a brand. It decides what goes on the
screen, where, how visible, how it responds, and what must not be there.

**The test behind every rule:** nobody reads a screen. They arrive with one question and hunt
for the answer. A choice either makes that hunt faster or it is decoration.

**Plain is not generic, and it is not colourless.** Stripping slop and stopping leaves a
white page with grey text and one blue button. That is a default too. Plain is about
structure: every element there for a reason, and finished. Colour is where the product gets
its character. Build on neutrals (white, black, greys) and put a real palette on top of
them.

## How to use

| Job | Do this |
|---|---|
| Build | Work the Build order, read the reference for your surface, fill the Done gate. |
| Review | Run the checker, then read `references/review.md`. Report `symptom -> fix -> why`. |
| Fix | Change only what the finding names. Keep existing copy, names and identity. |

A project's own design system, tokens or brand rules beat this skill. Follow them and use
Oxfords for everything they leave open.

| Surface | Read first |
|---|---|
| Dashboard, admin, table, chart, settings (including on a phone browser) | `references/app-ui.md` |
| Native mobile app screen | `references/mobile.md` |
| Landing page, marketing site | `references/landing.md` |
| States, forms, errors, UX copy | `references/states-forms-copy.md` |
| Colour: choosing and applying a palette | `references/palettes.md` (read this for every build) |
| Fonts, icons, the full ban list | `references/slop-floor.md` |
| Motion, gestures, reduced motion | `references/motion.md` |
| Reviewing a finished screen | `references/review.md` |

## Build order

1. **Intent.** Name what the user came to do. Start with the control that does it. For each
   thing you add, ask whether it does anything the plain version did not. Add function only
   as intent grows.
2. **Content first.** Write every label, number and name before laying anything out. Use
   uneven, believable data: real-looking names, odd totals, one long value. Show only what a
   person scans for; detail lives one step in. One surface does one job.
3. **Let the data pick the component.** A fixed set of values is a chip. Numbers are
   right-aligned with tabular figures. Time-based data is a timeline or a roll-up chart, not
   a time-sorted table. Inactive items stay in place, greyed. Do not reach for a table or a
   row of tiles by reflex.
4. **Layout on edges.** Left-align labels, right-align values, centre only what is not meant
   to be read. Every element locks to an edge and creates the edge for the next. Fill empty
   space by moving content onto edges, not by adding content. Use the layout people expect
   (top to bottom, left to right, navigation on top or left) before anything distinctive.
5. **Colour.** Start from neutrals: a white, black or grey page, neutral surfaces, near-black
   or near-white text. Then, unless the project has its own colours, choose a palette from
   `references/palettes.md` and place its three colours on top as lead, support and pop.
   Write one line on why it fits. Never a bone or cream page; never neutrals with one blue
   button.
6. **Hierarchy.** Size, position, weight, then colour. Most important goes top-left and
   largest. Group, rank, stack, then delete every label the layout already implies. Emphasis
   is relative: quiet the neighbours instead of colouring the hero.
7. **Disclosure.** Primary action always visible with a label. Secondary actions in a menu,
   or revealed on hover with a visible equivalent on touch. Rare ones in a popover. Never
   put a primary item behind a click.
8. **Container.** Inline first, if it fits. Then: simple and non-blocking is a popover;
   complex but same page is a modal followed by a confirmation; large or permanent is a new
   page with a way back; on mobile, picking without leaving is a bottom sheet.
9. **The invisible layer.** States, feedback, focus, empty and broken content. This is the
   half that gets skipped. The Done gate lists it.

## Done gate

Answer every line for the screen you built. "None" needs a reason.

| Slot | Must exist |
|---|---|
| Buttons | default, hover, focus-visible, pressed, disabled with the reason in text beside it; loading only where the user waits |
| Inputs | a persistent label above, focus, error below the field that says how to fix it, input kept after an error |
| Every action | a response where the user is looking, within 100ms: the control changes in place, or a toast with undo |
| Destructive actions | undo where possible; otherwise a confirm that names the object and labels the button with the action |
| Icon-only controls | an accessible name and a tooltip; anything not universally known gets a text label instead |
| Empty | first run (one sentence and the one action that fills it) and no results (quote the query, offer to clear it) |
| Loading and failure | skeleton shaped like the result after about 300ms; error says what failed and how to recover; offline and no-permission handled |
| Messy content | long names truncate with the full value available, 0 / 1 / 10,000 rows work, a missing image is handled |
| Tables | search, filter or sort; numbers right-aligned; one primary action per row; selection reveals a bulk action in the existing toolbar |
| Charts | plain line or bar; axis values, grid lines, labels, a range or metric control, a value on hover or focus |
| Navigation | current location shown, items named for their contents, grouped, rare items last, about five top-level items |
| Keyboard and contrast | everything reachable by Tab with visible focus, Esc closes overlays, text 4.5:1, large text and icons 3:1, state never by colour alone |
| Touch | 44px targets, nothing that works only on hover, 16px inputs, safe areas respected |
| Motion | under 250ms for feedback, never blocks input, a reduced-motion version that keeps the feedback |
| Colour | a neutral base (white, black, greys) covering most of the screen; a named palette with a reason; all three of its colours used, each for one job; no bone or cream page |
| Consistency | one type family, one palette, one icon set at one weight, one radius per tier, same thing looks and behaves the same everywhere |
| Slop floor | the checker passes, or every warning has a one-line reason |

## Slop floor

The marks of a generated interface. Remove them; do not restyle them. Full list with
replacements in `references/slop-floor.md`.

- **Structure:** a coloured bar down the side of the active nav item or a card; a card around
  everything; cards inside cards; a small uppercase label above every heading; numbered
  section labels; a greeting header; a row of icon-and-number tiles; the same figures
  repeated on several pages; controls that do nothing.
- **Type and icons:** a default font nobody chose (Inter, Geist, Roboto, Poppins, Montserrat,
  DM Sans, Space Grotesk, Instrument Serif, Playfair Display, Fraunces); a serif word dropped
  into a sans headline; emoji as icons; the stock icon set at its default stroke; an icon in
  a tinted square above every heading.
- **Colour:** a bone or cream page with an orange or red accent; a neutral page whose only
  colour is one blue button; a whole interface tinted in palette colours with no neutrals;
  purple or indigo gradients; gradient text; glows and blurred colour blobs; a tinted pill on
  every status.
- **Motion:** bounce; everything fading up on scroll; pulsing dots; marquees; content hidden
  until a script reveals it.
- **Copy:** seamless, effortless, unlock, elevate, supercharge; "Get started" and "Submit";
  Acme and Jane Doe; round invented numbers; exclamation marks and em dashes.

Run the checker on what you built:

```bash
node scripts/check.mjs path/to/build
```

It fails on the mechanical tells and warns on the judgement ones. Fix each finding or write
one line on why it is deliberate.

## Numbers

| Thing | Value |
|---|---|
| Spacing | multiples of 4; unequal by role: 4-12 inside a group, 24-40 between groups; more space above a heading than below it |
| Radius | one per tier (controls, cards); nested inner = outer minus the gap |
| Button padding | horizontal about twice vertical |
| Icon size | the text line height; stroke matched to the text weight |
| Type scale | about six steps, plus at most one hero figure or headline outside the scale. Web app 13-14px body, rarely above 24px. Native app 17pt body, 15 minimum. Marketing 16px body and up. Nothing under 11px |
| Line length and leading | 45-75 characters; body leading about 1.5, display 1.05-1.2 |
| Heading tracking | -2% to -4% on large display type only; body 0 |
| Targets | 44px touch; 24px absolute floor on desktop |
| Feedback timing | press 100-150ms; routine transitions 150-250ms; overlays up to 400ms; exits faster than entrances |
| Easing | ease-out with no overshoot |
| Shadows | soft, low contrast, tinted to the background; if you notice the shadow it is wrong |
| Dark mode depth | no shadows: each layer up is slightly lighter and less saturated than the one below |
| Phone ground | pure black `#000` or pure white `#FFF`; navigation layer in Liquid Glass |
| Contrast | 4.5:1 text, 3:1 large text, icons, input borders and focus rings |

## Four tests before you call it done

- **Squint.** Blur your eyes. One thing should land first, and it should be the right thing.
- **Subtract.** Remove an element. If nothing got worse, it stays out.
- **Swap.** Put a competitor's logo on it. If it still fits, the content is too generic.
- **Defend.** Point at any value. You should be able to say why it is that and not the default.

## Credits

Oxfords stands on other people's work. See `CREDITS.md` in the repository.
