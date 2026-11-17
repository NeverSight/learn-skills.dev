---
name: sticky
description: "Eases position sticky in and out. The element slows down as it reaches its line and speeds up gradually when its container ends, instead of stopping and starting in one frame. Native sticky still does the pinning; this adds one offset on top as a scroll-driven animation. Use when asked to ease, smooth or soften a sticky element (a sidebar, a rail, a sticky heading, a pinned card), when someone says position sticky feels abrupt or snaps, or when asked for 'eased sticky', 'smooth sticky' or @alpacka/sticky. The implementation ships inside the skill as one file to copy in; there is no package to install."
---

# Sticky, eased

`position: sticky` changes speed instantly at both ends of the pin: from scroll
speed to still, and back. This eases both ends.

It does not replace sticky. The element stays `position: sticky` and the
browser pins it. One offset is added on `translate`, as a scroll-driven
animation, and it is zero except in a short stretch of scroll at each end of
the pin. Where it does not run, the element is plain sticky and the layout is
the same.

The whole implementation is in [sticky.ts](sticky.ts), next to this file: one
file, no dependencies, about 25 kB with its comments. You do not install
anything. You copy that file into the project. Read its header comment before
changing it.

## 1. Decide what to ease

Ease these:

- a sidebar or rail that sticks beside longer content
- a sticky heading or label inside a section
- a card or media box pinned while text scrolls past

Leave these alone. They stay plain sticky, and the code refuses them anyway:

- a site header whose container is the whole page (nothing to ease into)
- table headers (`th`, `thead`)
- a `bottom` or `left` sticky
- a sticky inside its own scroll container

Do not use it for a pin written in script (`position: fixed` toggled on
scroll, GSAP ScrollTrigger `pin`, a transform written from the scroll
position). Those are not sticky. Either convert them to `position: sticky`
first, or leave them.

## 2. Check the element can be eased

All four must hold. Fix the markup or CSS first if one does not.

1. The element's computed `position` is `sticky` and `top` is a length, not
   `auto`.
2. Its **parent** is the box it sticks within, and the parent is taller than
   the element. The room between them is the pin's length.
3. No ancestor between the element and the page has `overflow` other than
   `visible` or `clip`. (That also breaks native sticky. `overflow: clip` is
   the fix when the ancestor only needs to hide overflow.)
4. Nothing else sets `translate` on the element. The offset owns that
   property while it runs. `transform` is free; so is a wrapper.

## 3. Add the code

Copy [sticky.ts](sticky.ts) into the project, where its own helpers live
(`src/lib/sticky.ts`, `app/utils/sticky.ts`, `lib/sticky.ts`), and import
from there:

```ts
import { sticky } from '@/lib/sticky'
```

- Copy it whole and unchanged, header comment included. Its first line names
  the version.
- In a JavaScript project, compile it once
  (`npx tsc sticky.ts --target es2022 --module esnext --declaration false`)
  or strip the types by hand.
- **If the project already has a copy**, compare the version on its first
  line with this one. Replace it if it is older, and keep any change the
  project made to it deliberately.
- Fit it to the project only at the edges: its lint and formatting rules, its
  import alias. Leave the measuring and the maths alone.

The same code is on npm as `@alpacka/sticky`, for a project that would rather
have a dependency it can update:

```sh
npm i @alpacka/sticky
```

The examples below import from `@/lib/sticky`. With the package, import from
`@alpacka/sticky` instead; nothing else changes.

## 4. Call it

Client only. It reads layout, so never during server rendering.

One element:

```ts
const stick = sticky(document.querySelector('.rail')!)

stick.refresh() // measure again, for a change that resizes neither box
stick.freeze()  // keep the current offset and stop following the scroll
stick.destroy() // back to plain sticky
```

Every sticky on the page, in one call:

```ts
const all = sticky.all()        // finds them from the stylesheets' own rules
const some = sticky.all('.rail') // or only the ones named

all.scan()    // look again after content was added or removed
all.destroy()
```

`all()` reads the page's CSS for rules that set `position: sticky`, so a
sticky that only applies from a breakpoint up is found at any width and turns
on when the rule applies. Prefer it over a hand-kept list of selectors.

Per element, in the markup:

```html
<aside data-sticky-ease="off">…</aside>
<aside data-sticky-ease="expo" data-sticky-distance="0.3">…</aside>
```

### Options

| option | default | |
| --- | --- | --- |
| `distance` | `0.4` | How much scroll the ease in, and the ease out, takes. A fraction of the viewport height. |
| `ease` | `'power2'` | `'power1'`, `'power2'`, `'power3'`, `'expo'`, or any ease-out function. |
| `media` | pointer devices | Media query for where it runs. `'all'` runs it everywhere. |
| `engine` | `'auto'` | `'compositor'` (scroll-driven animation) or `'main'` (script). |
| `ticker` | `requestAnimationFrame` | `(fn) => unsubscribe`, the frame loop the script engine uses. |

Start from the defaults. If the project has motion tokens, take `ease` and
`distance` from them rather than inventing values.

## 5. Wire it to the framework

Always destroy on unmount. An element that goes away with its stick still
attached leaks observers.

**Vue / Nuxt**

```ts
import { onMounted, onBeforeUnmount, type Ref } from 'vue'
import { sticky, type Sticky, type StickyOptions } from '@/lib/sticky'

export const useSticky = (target: Readonly<Ref<HTMLElement | null>>, options?: StickyOptions) => {
	let stick: Sticky | null = null

	onMounted(() => {
		if (target.value) stick = sticky(target.value, options)
	})

	onBeforeUnmount(() => stick?.destroy())

	return { freeze: () => stick?.freeze() }
}
```

**React**

```tsx
import { useEffect, useRef } from 'react'
import { sticky, type StickyOptions } from '@/lib/sticky'

export function useSticky<T extends HTMLElement>(options?: StickyOptions) {
	const ref = useRef<T>(null)

	useEffect(() => {
		if (!ref.current) return
		const stick = sticky(ref.current, options)
		return () => stick.destroy()
	}, [])

	return ref
}
```

**Whole site, once.** Call `sticky.all()` in the root layout's mount, and
`scan()` after each route change so new pages' stickies are picked up.

**Page transitions.** If a transition resets the scroll while the old page is
still on screen, call `freeze()` on its sticks first, or the element jumps as
the scroll goes to zero.

**A smooth-scroll library (Lenis and the like).** Nothing to do where the
compositor engine runs. For the script engine, pass the library's frame as
`ticker` so the write lands in the frame the page moves in:

```ts
sticky(el, {
	ticker: (fn) => {
		gsap.ticker.add(fn)
		return () => gsap.ticker.remove(fn)
	},
})
```

**A virtual scroll** has no `position: sticky` at all. Use the maths alone:

```ts
import { curve } from '@/lib/sticky'

const c = curve({ travel: 1200, span: innerHeight * 0.4, ease: 'power2' })
const offset = c.clamp(scroll - engage) // where a plain clamp would go
```

## 6. Verify

Do not report it done from the code alone. In a browser:

1. `stick.engine` is `'compositor'` or `'main'`. `null` means it is not
   running: go back to section 2, or the device is touch, or reduced motion is
   on.
2. Scroll to where the element reaches its line.
   `getComputedStyle(el).translate` is a non-zero `0px Npx` just before and
   after that point.
3. Scroll to the middle of the pin. It is `none` or `0px`: the element sits
   exactly on its line.
4. No console errors, in Firefox as well as Chrome. They take different code
   paths.

## What to know before changing anything

- **Touch is off by default.** On a phone the offset can run out of step with
  the scroll, depending on the browser. `media: 'all'` forces it on. Do not
  turn that on unless asked, and say it needs checking on a real phone.
- **Reduced motion turns it off.** Leave that.
- **Engines.** Chrome, Edge, Safari 26+ and Firefox run it as a scroll-driven
  animation; older browsers write the same offset from script.
- **Range offsets are strings** (`'exit-crossing 120px'`), not Typed OM
  values. Firefox has scroll-driven animations without the Typed OM.
- **`all()` looks again on `load`.** A module script can run before its
  stylesheet has loaded, and then there are no rules to read yet.
- **It measures again** when the element, its parent or the viewport resizes,
  and only rebuilds if the numbers moved.
- Supported: `top` stickies on the block axis of the root scroller.

## How it works, in four lines

Sticky's own offset is `clamp(scroll − engage, 0, travel)`. The ease in takes
`W` of scroll (`distance` × viewport height) on an ease-out `E` with starting
slope `m = E′(0)`. To start at exactly scroll speed the element may only
cover `A = W / m` while it eases, so the offset is `A · (min(m·t, 1) − E(t))`
for `t` from 0 to 1, and the ease out is the same mirrored.
