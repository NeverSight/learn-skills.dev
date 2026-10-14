---
name: design-system
description: How a snapcn component is allowed to look. READ THIS BEFORE you write a colour, a border, a shadow, a radius or a font stack into a registry component. snapcn ships a shadcn design system (SnapCnTheme) and a tier of shadcn UI primitives (snap-cn-ui) — components compose them, they do not re-invent them. Explains which tokens exist, how to resolve them, how to reuse a primitive's own surface instead of hand-rolling one, and why var(--token) does not survive a Remotion render. Triggers - color, colour, hex, rgba, box-shadow, drop shadow, border, hairline, radius, surface, background, theme, dark mode, styling a component, "looks wrong on white", "the shadow is bad", shadcn, Input, Button, Card.
---

# The design system

snapcn is a **shadcn** registry. That is not branding — it is a constraint. Every
component we ship lands in somebody's shadcn project, next to their `Input` and
their `Button`, and it has to look like it belongs there. A scene component that
paints its own greys is a scene component that will clash with the app that
installs it.

**So: no component invents a colour, a border, a shadow or a radius.** They come
from the design system, or they come from a primitive that already solved it.

---

## Rule 1 — the tokens are the source of truth

`registry/snap-cn-ui/core/theme.ts` is a shadcn token set (`SnapCnTheme`), and it
is a **mirror of `app/globals.css`** — the same values the site's
`components/ui/*` paint from. That is not a coincidence to be maintained by hand:
`pnpm run check:tokens` fails the moment the two disagree. It exists because they
*did* disagree, for long enough that the site was warm and the videos it sells
were cool.

| token | light | what it is |
| --- | --- | --- |
| `background` | `#faf9f6` | the page (warm off-white — **not** `#fff`) |
| `card` | `#ffffff` | a surface **on** the page |
| `foreground` | `#141414` | text (**not** `#000`) |
| `mutedForeground` | `#6e6a63` | secondary text, leading icons |
| `border` / `input` | `#d9d9d9` | hairline |
| `ring` / `primary` | `#3577e0` | focus, accent |
| `radius` | `10` | controls |

Dark is the `.dark` block of the same file (`#0a0a0b` page, `#141417` card,
`#26272b` hairline, the same `#3577e0`).

**Never edit this table or `theme.ts` on its own.** A token changes in
`globals.css` first, because that is what the shadcn components obey; `theme.ts`
follows, and `check:tokens` proves it did. The one exception runs the other way:
`--radius: 0.28rem` is set so its `--radius-3xl` step lands on this `10`.

Resolve them with the hook, never by importing the object:

```tsx
import { type SnapCnTheme, useSnapCnTheme } from "@/lib/snap-cn-ui";

const t = useSnapCnTheme(theme, mode);   // prop > provider > light/dark default
```

and take `theme?: Partial<SnapCnTheme>` + `mode?: "light" | "dark"` as props, like
every other component does. That is what lets a user drop the component into their
own palette without forking it.

## Rule 2 — reuse a primitive's surface, don't re-derive it

The UI tier already exports the *style context* each control paints itself from.
A field that wants to look like a shadcn input should get its surface from the
shadcn input:

```tsx
import { inputStyleContext } from "@/components/snap-cn/input";

const ui = inputStyleContext(t);
// → idleBorder, hoverBorder, activeBorder, ring, background, foreground, mutedForeground
```

Now the two cannot drift apart. Declare the primitive in `registryDependencies`
(`@snapcn/input`, `@snapcn/caret`, `@snapcn/snap-cn-ui`) so a user installing
your component gets it.

Composing the *rendered* primitive is a different question, and often the wrong
one — `Input` is a 320px control with a state machine and a slice-based text
reveal. A hero field with measured proportions, a clipped reveal and a camera
cannot be built out of it. **Take its tokens; don't take its box.**

## Rule 3 — shadows

This is where it went wrong, and the bug is worth keeping:

> `search-typing` shipped a `rgba(9,9,12,0.45)` drop shadow at a `0.12 × height`
> blur, because that is what the *reference video* had. The reference sat on a dark
> violet field, where a heavy shadow reads as depth. Put the same component on a
> white page and the shadow reads as a **grey smear** under the control. It looked
> cheap, and it was the first thing anyone noticed.

Softening it to "a shadow you have to look for" was **still wrong** — the next
round of feedback was the same word: *worst*. A drop shadow big enough to be seen
under a field that size is a grey smear on a light page, full stop.

**The default is no drop shadow at all.** shadcn defines a control with a hairline
border, and the border does the whole job:

```tsx
background: t.card,                          // #ffffff
border: `1px solid ${ui.idleBorder}`,        // #d9d9d9
boxShadow: "none",
```

A gradient fill is the same mistake wearing a hat: the reference's grey-crown-to-
white field reads as an *inner* shadow on a light page. Flat fill, hairline border,
nothing else.

A shadow lifted off a reference is lit for *that reference's backdrop*. It is not
a property of the component. If you want the lit surface, ship it as an opt-in
(`surface="glass"`) and say which backdrop it is lit for.

## Rule 3b — a token is specified at a control's scale, not at yours

Having killed the shadow, the border was next: *"border is very light."* It was —
and the token was not wrong, the **scale** was.

`#d9d9d9` at `1px` is a hairline on a **40px** control: 2.5% of its height. Put the
identical border on a 190px hero field and it is 0.5% of its height, and it all but
vanishes. A token carries a weight *relative to the thing it edges*.

So scale it, but scale it **through the system**, not by inventing a grey:

```tsx
const border = Math.max(1, 0.009 * H);                        // width: a ratio of the field
const borderColor = mixOklch(ui.idleBorder, t.foreground, 0.28);  // contrast: the system's own mix
```

`mixOklch` walks the hairline toward `foreground` in the system's colour space, so
the result still belongs to the palette and still follows a user's theme override.
Never reach for a hex because the token "looked too light".

## Rule 3c — burned-in video type is not app chrome

Captions, lower thirds and titles are the one place the app palette does NOT apply.
They are burned into footage, they sit next to nobody's `Input`, and they have to be
legible over a face, a sky or a white desk. What governs them is craft, not tokens:

- **A heavy outline, drawn OUTSIDE the letterform.** `-webkit-text-stroke` centres
  the stroke and eats the glyph from the inside — measured, a 14px stroke takes a
  38px stem down to **22px**. `paint-order: stroke fill` draws the stroke first and
  the fill over it, and the stem comes back to 38px. Without that one line, captions
  look cheap and nobody can say why.
- **Display weight and display size.** Montserrat 800–900 at 11–13% of the frame's
  short side. `word-captions` shipped at Inter 700 and 2.8% of the height — a
  subtitle wearing a caption's name.
- **The accent is the design.** A caption's yellow is not a brand token, it is the
  look. Expose it as a prop; do not reach for `theme.primary`.

Still take the *neutrals* from the system where a component has app chrome (a pill, a
card). The exception is the burned-in type itself.

## Rule 4 — a token has to survive the renderer

Animated colours must be concrete `oklch`/`hex`/`rgb` and interpolated with
`mixOklch`. **`var(--token)` cannot be resolved by Remotion's headless renderer**
for JS interpolation — a Remotion bundle has none of the app's CSS. Static,
never-animated colours may use `var()` in an inline `style`; anything you tween
may not.

The same trap catches fonts: reaching for `var(--font-outfit)` gets you the face on
the *site* and a fallback in the *render*. Load the face with
`@remotion/google-fonts` so the Player, the mp4 and a user's own project all agree.

## Rule 5 — measure the reference for *proportion*, not for *palette*

When a component is modelled on a reference, the geometry is worth measuring to the
pixel — radius/height, cap height, stroke, spacing. That is what makes it feel like
the thing.

Its **colours are the reference's brand, not yours.** Slack's violet, Slack's
glassy grey-to-white field, Slack's shadow: none of that belongs in a registry
component that ships to strangers. Take the shape. Leave the paint.

If a measured surface is genuinely worth keeping, ship it as an *option* next to
the design-system default — `surface="glass"` vs the default `surface="shadcn"` —
and say in its doc which backdrop it is lit for.
