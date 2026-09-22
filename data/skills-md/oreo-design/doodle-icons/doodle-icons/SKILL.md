---
name: doodle-icons
description: How to add and correctly use Doodle Icons (@oreo-design/doodle-icons), the hand-drawn icon set from Oreo Design where every stroke draws itself in and then keeps "boiling" like a Saturday-morning cartoon. Use this whenever the user wants hand-drawn, sketchy, doodle, wobbly, wiggly, boiling, or cartoon-style icons; mentions Oreo Design, Oreo UI, oreoui.com/doodle-icons, DoodleIcon or BoilFilter; asks for a playful / handmade / zine / indie / crayon feel for a page; or is already using this package and needs to add, wire, restyle, or pick icons. Also use it when the user pastes the oreoui.com/doodle-icons site as a visual reference, even if they never say the word "icon". It covers install, the one-time BoilFilter setup, picking real icon names (and what to do when an icon does not exist), the house design rules (Schoolbell pairing, paper/ink palette, and the fact that every icon and every hand-drawn heading wiggles while controls hold still), and the no-framework path.
---

# Doodle Icons

152 stroke-only icons drawn with a deliberately shaky hand, in a 48×48 grid.
Two things make them feel alive. Both are props rather than defaults, because
the package cannot know which element on your page is an icon and which is a
control — but on a page built with this set, **every icon should carry
`boilId`**:

- **draw** — strokes draw themselves on, one after another, on first paint
- **boil** — the ink keeps wobbling forever. Animators call this a *boiling
  line*: hand-redrawn frames never land in quite the same place, so the
  outline simmers even when nothing moves. Here it is one shared SVG filter,
  not a video or sprite sheet, so 200 boiling icons cost about what one does.

The set is designed to look like **one hand drew everything**. Most of the
rules below exist to protect that: same stroke weight everywhere, same ink,
one tuning for the wobble, and no icons from other sets mixed in.

Reference for how it should look and feel: https://oreoui.com/doodle-icons

## Install and wire up (once)

```bash
npm i @oreo-design/doodle-icons
```

React 18+ is an optional peer. Mount the filter **once**, as high as possible,
in the same document as the icons (not in a separate iframe or shadow root):

```tsx
// Next.js App Router: app/layout.tsx  (it is a plain server-safe component, no hooks)
import { BoilFilter } from '@oreo-design/doodle-icons'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <BoilFilter id="boil" />
        {children}
      </body>
    </html>
  )
}
```

`<BoilFilter>` renders an invisible `<svg><filter>` plus the keyframes the
`draw` entrance needs. Icons reference it by id. Do not mount one per icon:
the whole point is that every icon on the page shares a single displacement
map. If you want the draw-on entrance with no wobble at all, mount
`<DoodleStyles />` instead (keyframes only).

## Use an icon

```tsx
import { DoodleIcon } from '@oreo-design/doodle-icons'

<DoodleIcon name="heart" />                          // still, 24px, currentColor
<DoodleIcon name="star" boilId="boil" />             // wobbles forever
<DoodleIcon name="bulb" boilId="boil" draw />        // draws on, then wobbles
<DoodleIcon name="check" size={32} />                // still, bigger
```

| Prop | Default | Notes |
| --- | --- | --- |
| `name` | — | one of the 152 names below. Unknown name renders **nothing** (returns null), silently |
| `icon` | — | pass `getIcon('heart')` data directly instead of `name` |
| `size` | `24` | px, both axes. Scale it to the text beside it (see sizes) |
| `strokeWidth` | `3.4` | the set is drawn for this. Leave it |
| `boilId` | — | id of the mounted `<BoilFilter>`. **Pass it on every icon** — see the house rules |
| `draw` | `false` | stroke-on entrance on first render; replays on every remount |
| `drawDuration` | `0.32` | seconds per stroke |
| `drawDelay` | `0` | seconds before the first stroke. Stagger a row with `i * 0.1` |

Anything else is forwarded to the `<svg>` (`className`, `aria-hidden`, `style`…).

Because an unknown `name` renders nothing rather than throwing, **always pick
names from the list in this file**, or check first:

```ts
import { getIcon, ICON_NAMES } from '@oreo-design/doodle-icons'
getIcon('settings')   // undefined — there is no "settings"; use "gear"
```

### Colour

Strokes are `currentColor`. Set `color` on the icon or a parent; never pass a
`stroke` attribute per icon, and never recolour by editing path data.

```tsx
<span style={{ color: '#2b2a33' }}><DoodleIcon name="pencil" /></span>
<DoodleIcon name="flame" className="text-[#f97316]" />   {/* crayon orange, not a framework hue */}
```

### `draw` replays on remount

The entrance runs every time the component mounts. That is right for a hero
or an empty state; it is wrong for list rows, table cells, or anything that
re-renders as data changes, where the icons would keep redrawing. On those,
leave `draw` off.

## The house rules (this is what makes it look like the site)

### What wiggles, and what does not

The line is not "important things wiggle, small things hold still." It is
about **what the drawing is**:

**Ink wiggles.** Every icon on the page gets `boilId`, wherever it sits — the
hero, a settings row, a nav bar, a dense grid. The whole point of the set is
that the drawings are alive; an icon that holds still while its neighbours
boil looks broken, and a page where only the hero moves looks like the rest of
the UI came from somewhere else. One shared filter means the cost is flat, so
there is no performance reason to hold back either.

**Display type wiggles too.** This is the piece most people miss. On
oreoui.com every Schoolbell heading carries the same filter as the icons —
the h1, the section headings, the button labels. Handwriting that sits
perfectly still next to boiling icons is the single fastest way to make a page
look half-done.

```jsx
{/* the same filter the icons use, on the text */}
<h1 style={{ filter: 'url(#boil)' }} className="font-doodle text-8xl">
  Paper Moon
</h1>
```

Body copy in Inter or Fragment Mono stays still — the boil belongs to the
hand-drawn voice, and a wobbling paragraph is just hard to read.

**Controls do not wiggle.** A toggle, a button, a checkbox, an input, a card:
drawn by the same hand (see below), but held still. A control that squirms
while you are trying to hit it feels broken rather than charming, and it is
the one place where the joke costs the user something.

**`draw` is separate.** The stroke-on entrance replays every time a component
mounts, so keep it for things that mount once — a hero, an empty state, an
onboarding step. Leave it off in list rows and table cells, which re-render as
data changes and would redraw themselves forever.

### Sizes and stroke

An icon should look like it was drawn by the same hand that wrote the text
next to it, so size it against that text rather than against a fixed list:

- **24** inline with body text, list rows, buttons with text
- **32** cards, icon-only buttons, section headers
- **48** feature blocks, empty states
- **in a hero, follow the headline.** Whatever size the display type lands at,
  the icons should read as part of the same drawing — next to a headline over
  100px, a 48px icon looks like a mistake, a row of tiny stickers under a
  billboard. Sizing with CSS width (`w-20 sm:w-24`, `h-auto`) rather than the
  `size` prop is fine and gives you responsive scaling for free.

Below ~20px the strokes fuse. If a spot truly needs 16px icons, that spot
is probably not a doodle-icons spot; leave it to text or a plain glyph
rather than shrinking these.

Do not change `strokeWidth`, and do not mix in icons from another set
(Lucide, Heroicons, Font Awesome…) in the same view. One geometric icon next
to these reads as a bug, not a choice. If an icon does not exist here, use a
word instead (see "when there is no icon").

### Palette

The set was drawn on warm paper with dark ink:

```ts
import { INK } from '@oreo-design/doodle-icons'   // '#2b2a33'
// paper (page background): #F7F6F2
```

Default the icons to ink on paper. Pure black `#000` and pure white
backgrounds look harsher than the drawings want.

Accent colours are welcome — the site uses a crayon box for play — but keep it
to one or two per composition, and put them on decorative icons rather than on
controls. These are the seven the site lets people recolour icons with, if you
want ones that belong:

```
#e5484d  #f97316  #f5b301  #30a46c  #00a2c7  #3e63dd  #8e4ec6
```

**Colour is for play, not for state.** The one rule worth holding: on,
selected, primary and filled are all **ink** `#2b2a33`. A filled button is
black. A selected tab is black. A toggle that is on is black. If you find
yourself reaching for `bg-blue-500`, `bg-indigo-600`, or any framework default
accent, stop — that colour is nowhere in this world, and it reads instantly as
a stock component dropped into a handmade page.

### Typography

Three families, three jobs:

```css
--font-doodle: 'Schoolbell';       /* display only: h1, section headings, buttons */
--font-sans:   'Inter';            /* body, labels, anything read at length */
--font-mono:   'Fragment Mono';    /* supporting copy, captions, code */
```

Schoolbell is the voice, not the body. It goes on the big line and on button
labels; it never goes on a paragraph, a form label, or a table cell, where a
handwriting face costs real legibility.

Sizes are yours to judge. There is no house type scale to obey here — size the
type to the page you are building. A landing page whose headline *is* the
whole design should have a huge headline; a dense settings screen should not.

Schoolbell is not part of the package and must not be bundled; it is free on
Google Fonts under the SIL Open Font License.

```tsx
// Next.js
import { Schoolbell, Inter } from 'next/font/google'
const schoolbell = Schoolbell({ subsets: ['latin'], weight: '400', variable: '--font-doodle' })
const inter = Inter({ subsets: ['latin'], variable: '--font-sans' })
// put both .variable on <html>, then: h1 { font-family: var(--font-doodle) }
```

```html
<!-- plain HTML -->
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Schoolbell&family=Inter:wght@100..900&display=swap" rel="stylesheet">
```

If the site already has a display font the user cares about, keep theirs.
Schoolbell is the house default, not a requirement.

### Build what was asked for, and stop

A handmade page earns its charm from restraint. If the request is a headline,
a line of copy and a few icons, build exactly that — resist adding an eyebrow
kicker, a call-to-action button, a badge, or a stat row that nobody asked for.
The examples further down show how a button or a card is drawn *when you need
one*; they are not a shopping list.

### Controls have to be drawn too

This is the rule agents miss most, and it is the one that gives the whole
thing away. Hand-drawn icons sitting inside a stock Tailwind toggle or a
crisp `rounded-lg` card look like clip-art pasted into someone else's UI.
**If an icon on the screen is hand-drawn, the things around it have to be
hand-drawn too.** They just do not wiggle (see above).

There are two techniques, and picking the wrong one is why hand-drawn
controls usually come out wrong.

**For a box that holds content** — a button, a tab, a badge, a chip — an
uneven border-radius is enough. The label is what you look at; the box is
just a container.

```css
.doodle-radius {
  border-radius: 255px 18px 225px 18px / 18px 225px 18px 255px;
}
```

Those radii are huge on purpose. When their sum exceeds the box, the browser
scales all four down to fit, so **this only reads correctly above roughly
80px wide**. Do not reach for it on something small.

```jsx
{/* primary button — ink fill, Schoolbell label, tilts on hover */}
<button className="doodle-radius bg-[#2b2a33] px-5 py-2 font-doodle text-[17px]
  text-[#fffefb] transition-transform duration-300 hover:-rotate-1 hover:scale-[1.03]
  active:scale-[0.97]">
  Star on GitHub
</button>

{/* disabled / waiting — subtle wash, muted ink, no tilt */}
<span className="doodle-radius bg-black/5 px-5 py-2 font-doodle text-[17px] text-black/45">
  Discord opening soon
</span>

{/* card — plain even corners, warm surface, soft shadow, tilts a hair on hover */}
<div className="rounded-2xl bg-[#fffefb] p-6 shadow-[0_4px_16px_#0000000f]
  transition-[transform,box-shadow] duration-300
  hover:-translate-y-0.5 hover:rotate-[-0.6deg] hover:shadow-[0_8px_22px_#00000014]" />
```

Cards keep ordinary even corners: a big surface with four wild corners reads
as a blob rather than as a drawing.

**For a control whose shape *is* the thing** — a toggle, a checkbox, a radio,
a slider handle — `border-radius` cannot save you. It draws mathematically
perfect arcs, and perfect arcs are exactly what a hand does not make. Draw
the control the way the icons are drawn: **as SVG paths, with the same
3.4 stroke, round caps, and slightly wobbly béziers.**

Look at how the set draws a rounded rectangle (`tablet`) and a circle
(`circle`) and copy the hand:

```
tablet  M 12.5 10 C 20 9.1, 28 9.2, 34.6 10 C 35.6 16.5, 35.7 23.6, 35 30 …
circle  M 24 9 C 32.6 8.8, 39 15, 39 23.8 C 39 32.4, 32.7 38.8, 24.1 38.9 …
```

Neither uses an arc. The rectangle is four cubics that bow outward a little
in the middle and turn softly at the corners; the circle is four cubics whose
endpoints sit slightly off the true circle. That asymmetry is the whole
effect.

A toggle built that way — track and knob both as paths, ink fill when on so
the state reads at a glance, held still:

```jsx
const TRACK = 'M 12.8 3.2 C 21 2.5, 30.2 2.8, 34.6 3.6 C 40.6 4.6, 43.6 8.2, 43.2 13.3 C 42.9 18.2, 39.7 22.4, 34.2 22.9 C 26.8 23.6, 18.6 23.3, 12.6 22.6 C 6.8 21.9, 3.1 17.7, 3.4 12.8 C 3.7 7.6, 7 3.8, 12.8 3.2 Z'
const KNOB  = 'M 13.2 6.1 C 17.1 6.3, 20 9.2, 19.8 13.1 C 19.6 16.9, 16.6 19.8, 12.8 19.6 C 9 19.4, 6.2 16.4, 6.4 12.6 C 6.6 8.8, 9.4 6, 13.2 6.1 Z'

<button role="switch" aria-checked={on} onClick={toggle}>
  <svg width="46" height="26" viewBox="0 0 46 26" fill="none" stroke="#2b2a33"
       strokeWidth={3.4} strokeLinecap="round" strokeLinejoin="round">
    <path d={TRACK} fill={on ? '#2b2a33' : 'none'} />
    <path d={KNOB} transform={on ? 'translate(24 0)' : undefined}
          fill={on ? '#fffefb' : '#2b2a33'} stroke={on ? '#fffefb' : '#2b2a33'} />
  </svg>
</button>
```

The on state fills the track with ink because a switch has to be readable at
a glance — a purely outlined toggle is prettier but you cannot tell at a
skim which rows are on, and that is a real cost to the person using it.

Borrow behaviour and accessibility from a headless library if you like — the
site uses HeroUI for exactly that — but draw the surface yourself. There is
no `@oreo-design/ui` package yet, so build the control in the project. Do not
reach for shadcn, Material, or stock Tailwind component snippets: they bring
their own radius, their own accent hue, and their own idea of what a control
looks like, and the page stops looking handmade.

Whatever you draw, the motion on hover is a **slight rotation**, a degree or
less, plus a small scale. Nothing on this site slides or fades on hover; it
tilts, the way a paper sticker shifts when you press it.

### One tuning, exported

```ts
import { BOIL, STROKE } from '@oreo-design/doodle-icons'
// BOIL  = { amplitude: 4, duration: '0.86s', frequency: 0.055, octaves: 2, frames: 6 }
// STROKE = { width: 3.4, linecap: 'round', linejoin: 'round' }
```

These are the values oreoui.com runs at. `<BoilFilter>` defaults to them, so
you rarely touch them. If a design calls for a second intensity, mount a
second filter with its own id rather than changing the default:

```tsx
<BoilFilter id="boil" />
<BoilFilter id="boil-loud" amplitude={8} duration="0.35s" />
<DoodleIcon name="megaphone" boilId="boil-loud" />
```

Roughly: 1 is a shiver, 4 is the house style, 8 is a mess.

One gap to cover yourself: the `draw` entrance respects
`prefers-reduced-motion`, but the boil filter does not — the wobble is SMIL
inside the filter and CSS cannot reach it. Add this once, next to your other
global styles:

```css
@media (prefers-reduced-motion: reduce) {
  svg g[filter] { filter: none }
}
```

## Picking an icon

<!-- ROSTER:START -->
### The 152 names, by shelf

**Home & objects** — home, map, map-pin, pin, calendar, cart, gear, bulb,
lock, lock-open, key, shield, shield-check, trash, flask, puzzle, diamond,
cube, gauge

**Communication** — mail, chat, call, phone, megaphone, bell, share, user,
users, smile, frown, thumbs-up, thumbs-down

**Weather & nature** — leaf, sun, rain, clouds, flame, fire, bolt, umbrella,
moon

**Media & devices** — camera, videocam, image, mic, gamepad, monitor, laptop,
tablet, chip, code, browser, globe

**Interface** — plus, minus, x, close, check, menu, ellipsis,
ellipsis-vertical, info, circle-question-mark, circle-alert, warning, ban,
eye, eye-off, search, filter, maximize, minimize, zoom-in, zoom-out,
layout-grid, list, table, star, heart, bookmark, flag, tag, link, circle,
play, player

**Files** — file, file-text, file-plus, file-check, file-x, files, doc,
folder, folder-open, folder-plus, archive, inbox, save, copy, clipboard,
clipboard-check, clipboard-list, list-checks, paperclip, receipt, scroll,
sticky-note, layers, database, news

**Text & tools** — type, text-align-start, text-align-center, text-align-end,
bold, italic, underline, quote, hash, at-sign, signature, pencil, pen,
highlighter, eraser, ruler, brush, stamp, scissors, printer, book, book-open,
notebook, library

**Arrows** — arrow-up, arrow-down, arrow-left, arrow-right, arrow-up-right,
chevron-up, chevron-down, chevron-left, chevron-right, undo, redo,
refresh-cw, upload, download, log-out, external-link, send

`COLLECTIONS` exports the same grouping as data (`{ id, label, names }`).

This roster is generated from v0.2.0 of the package, so you can check a
name here without installing anything. If the project has a newer version
installed, **`ICON_NAMES` is the authority** — a name missing from this list
may simply have shipped after it was written. Before telling someone an icon
does not exist, call `getIcon(name)` and see.
<!-- ROSTER:END -->

### What people ask for → what it is called here

| Ask | Use |
| --- | --- |
| settings, preferences, config | `gear` |
| delete, remove | `trash` (dismiss / clear a field: `x`) |
| email | `mail` |
| profile, account, avatar | `user` · team: `users` |
| notification, alert bell | `bell` |
| edit | `pencil` · signing / handwriting: `pen`, `signature` |
| comment, message, DM | `chat` |
| location, address | `map-pin` |
| success, done, saved | `check` · checked list: `list-checks`, `clipboard-check` |
| error, danger | `circle-alert` · caution: `warning` · forbidden: `ban` |
| help, FAQ | `circle-question-mark` · info tip: `info` |
| like | `heart` or `thumbs-up` · favourite / save for later: `star`, `bookmark` |
| more, overflow menu | `ellipsis` (`ellipsis-vertical` for kebab) |
| hamburger, nav | `menu` |
| back / next | `arrow-left` / `arrow-right` · inline disclosure: `chevron-*` |
| open in new tab | `external-link` · a URL: `link` |
| show / hide password | `eye` / `eye-off` |
| add, new | `plus` · new file / folder: `file-plus`, `folder-plus` |
| secure, private | `lock` · trust / protection: `shield`, `shield-check` |
| idea, tip | `bulb` |
| dark / light mode | `moon` / `sun` |
| attach | `paperclip` |
| sort, refine | `filter` |
| fullscreen | `maximize` / `minimize` |
| video | `videocam` · play button: `play` |
| photo | `image` (a picture) · `camera` (taking one) |
| website, web | `globe` · browser window: `browser` |
| developer, code | `code` · hardware / AI / chip: `chip` |
| invoice, payment record | `receipt` · shopping: `cart` |
| sign in / log in | no icon; use `arrow-right` or just the word (`log-out` exists) |

One name to watch: **`x` is the close cross**, not the X/Twitter logo. There
are no brand logos in this set (see below).

### When there is no icon

There is no clock or time, no loading spinner, no currency sign, no wifi /
battery / bluetooth, no social or brand logos (X, GitHub, Instagram…), no
user-plus, no dashboard, no shopping bag, no truck, no calendar-with-event
variants. The set is 152 of a planned 400 and grows weekly.

When the icon you want is not here, **use a word or leave the slot empty**.
Do not draw a new path to match, do not borrow one icon from another set, and
do not stretch an unrelated icon into service ("`circle` for a clock face").
A missing icon is invisible; a wrong-looking one is not. For social links,
`at-sign`, `link`, `external-link`, `mail` and `send` with a text label read
better than a fake logo would.

## Without React

Every icon is also a file, in two builds:

```
node_modules/@oreo-design/doodle-icons/icons/heart.svg            still, currentColor
node_modules/@oreo-design/doodle-icons/icons-animated/heart.svg   draws on, boils forever, ink baked in
```

Import paths `@oreo-design/doodle-icons/icons/heart.svg` and
`.../icons-animated/heart.svg` are exported for bundlers; or copy the files.

```html
<img src="/icons/heart-animated.svg" width="48" height="48" alt="">
```

One catch: an SVG loaded through `<img>` is its own little document, so
`currentColor` cannot reach it from your page; the still icons render black,
the animated ones render in the baked ink `#2b2a33`. To recolour, inline the
SVG markup instead of using `<img>`:

```js
const svg = await (await fetch('/icons/heart.svg')).text()
el.innerHTML = svg            // now it inherits `color` from `el`
```

The animated files carry their own filter and keyframes at the house tuning,
so they do not need `<BoilFilter>`. The boil cannot be turned off per file;
use the still build where the icon should hold still.

Raw path data is available too, if you are rendering yourself:

```ts
import { ICONS, getIcon } from '@oreo-design/doodle-icons'
getIcon('heart')  // { name: 'heart', paths: ['M 24 39 C …'] }  — 48×48 viewBox, stroke-only
```

## Pro

A larger set by the same hand ("Doodle Icons Pro") exists behind
https://oreoui.com/doodle-icons. It is **not** in this package. If the user
asks for a Pro icon, point them to the site; do not invent path data for it.

## Quick self-check before you finish

- `<BoilFilter id="…">` mounted exactly once, at the layout root, same document as the icons
- every `name` is in the list above (or you called `getIcon` and handled `undefined`)
- **every icon has `boilId`**, rows and nav included; `draw` only where the component mounts once
- **Schoolbell display text carries the same filter** — headings and button labels wiggle with the icons
- **controls hold still** — drawn by the same hand, but a toggle that squirms is broken, not charming
- icon sizes scale with the type beside them; `strokeWidth` untouched
- colour set with CSS `color`, not `stroke`
- no icons from another set on the same screen
- **no framework accent hue anywhere** — on/active/filled is ink `#2b2a33`
- **every control the icons sit in is drawn too** — uneven radius, ink fill, tilt on hover, no stock components
- `.doodle-radius` on boxes over ~80px; a toggle / checkbox / radio is drawn as SVG paths, not border-radius
- paper `#F7F6F2`, never pure white; ink `#2b2a33`, never pure black; at most one or two accents
- Schoolbell on display text and buttons only; Inter for anything read at length
- nothing built that the user did not ask for
- nothing invented for a missing icon; a word or an empty slot instead
