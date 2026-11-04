---
name: mobile-design
description: "Make a web screen feel native inside a phone app — a paywall, an onboarding or quiz, an offer, an update screen, any screen rendered in a WKWebView / Android WebView or shipped as a Superwall surface. The rules a native screen follows and a web page doesn't: press feedback on every control, hover gated to real pointers, 16px inputs and the keyboard, motion with real easing and durations, size-aware type, worst-case content, dark mode from the host, iOS vs Android conventions, and the audit before it ships. Use when building or reviewing any screen of that kind for iOS or Android, with or without a design reference, or when a screen \"feels like a website\" on a phone. For the Superwall framework's own mechanics (insets, routing, products, push) read superwall-framework; for React Native / Expo screens use the platform's own components instead."
---

# Mobile design

A web screen inside a phone app is judged against the native screens around
it, not against other web pages. Two things decide whether it passes:
reproducing the design exactly, and following the platform conventions users
feel but never name. These are working practices, not laws — the design
reference always wins over any rule here — but every one of them exists
because a shipped screen got it wrong.

Read this whole file once per screen. Skim the audit at the end before every
hand-off.

## The reference is the contract

- **Build 1:1.** Spacing, sizing, weights, colors, and effects come from
  the reference, not from habit. Measure the reference at logical points
  (a screenshot at device width) instead of eyeballing; compare your
  build against it side by side before calling it done.
- **Add nothing the design doesn't show.** No extra links, badges,
  footnotes, or affordances, however well-intentioned. If something seems
  missing (a restore affordance, a legal link), raise it in conversation
  — never add it to the UI unprompted.
- **Effects are design decisions, not defaults.** Shadows, gradients,
  borders, blurs, and radii belong to the design system of the paywall
  being built. If the reference is flat, build flat; if it is soft and
  elevated, match that. Reach for an effect only when the reference shows
  it.
- **A reference drawn at one size is a specification for every size.**
  A Figma frame is 393×852 or so; the paywall ships to 320-wide phones,
  667-tall phones, tablets and, sometimes, landscape. Where the reference
  is silent, the responsive rules say what to do; where it
  speaks, follow it and scale the rest around it.
- **No reference is not a blank check.** When the prompt is only words
  ("a paywall for my meditation app"), the values in this file *are* the
  design: system type with size-aware tracking, one filled CTA, press
  feedback on every control, the curves and durations under Motion. Make
  each call once and state it; never fill the gap with decoration (a
  gradient, a glow, a bouncing badge) the user did not ask for.


## The skeleton every screen shares

Native screens have a fixed anatomy, and a screen that follows it reads as
native before a single color is applied: the status bar's inset at the top
(the host's, not yours), small chrome (close or back) just under it, content
that scrolls and slides under a fade, one pinned primary action above the
home indicator, and small muted links beneath it. The page scrolls; the CTA
does not — a CTA that scrolls away with the copy is the single most common
reason a web screen underperforms a native one. Pinned means `position:
sticky; bottom: 0` as the page's last child, with a gradient from transparent
to the page background so content fades out behind it.

Safe areas belong to the host. In a Superwall surface the framework pads the
whole screen by the device's safe area and you write ordinary padding (never
`env()`, never `position: fixed`). In a plain web view, `viewport-fit=cover`
and `env(safe-area-inset-*)` on the chrome do the same job. Either way,
chrome sits at inset *plus* spacing, never at the inset: the floor is a
minimum and the real phone's bar is often taller.

## Platform conventions

Know which platform the screen is on (a Superwall surface reads
`data-sw-platform` on `<html>`; a plain web view is told once by the app or
reads the user agent at startup). Design for each; don't design for iOS and
let Android inherit it.

### iOS

- **Close** is a small circular button (≈ 30–32px visual, 44px tap) at
  the top-right, or top-left when the design says so; a sheet
  (`presentation: modal`) has the system grabber and usually no close.
- **Back** lives in the layout as a chevron at top-left and pops the
  stack; there is no hardware back.
- Buttons are rounded (12–16px) or fully pill-shaped, full width, 50–56px
  tall; text is 17px semibold. The primary CTA is the only filled button
  on screen.
- The system font (`-apple-system, BlinkMacSystemFont, "SF Pro Text"`)
  with tight negative tracking on display sizes is what reads as native.
- Segmented controls, toggles and radio rows look like their UIKit
  counterparts; if the design shows a custom one, match the design.
- Restore, Terms and Privacy sit under the CTA as small, muted text
  links (13px), never as buttons.

### Android

- **Close** is an `×` or `←` at the top-left in the Material tradition,
  or wherever the design puts it; the **hardware/gesture back** dismisses
  the paywall through the SDK, so never rely on your own back control
  being the only way out.
- The status bar on a fullscreen paywall is drawn *over* the paywall
  (the framework's top inset handles it); the navigation bar is *not* —
  the SDK keeps the webview above it, so the bottom inset is 0 there and
  a pinned CTA needs its own bottom padding (12–16px) rather than
  relying on the inset to give it air.
- Buttons are fully rounded (Material 3 pill) or 12px, 48–56px tall;
  labels 16px medium; Roboto through the system stack
  (`system-ui, Roboto, sans-serif`).
- Ripple is the native press feedback; a scale-down press state is an
  acceptable web stand-in and should be subtler (0.98) than on iOS.
- Copy differs: "Restore purchases" is fine on both, but "Cancel anytime
  in Settings" is iOS-specific wording; say "in Google Play" or keep it
  store-neutral when the paywall ships to both.

### Web (a web funnel or a web-only paywall)

- No status bar, no home indicator, no SDK chrome: every inset is 0 and
  the browser draws its own bars around the viewport. The framework's
  wrapper is sized with `100dvh`, so a pinned CTA sits above Safari's
  toolbar as it collapses; never size anything of your own with `100vh`.
- Keyboard focus is real here. Keep `:focus-visible` styles on inputs
  and buttons; it is the one surface where you should not suppress them.
- Mouse exists: hover states are welcome, and the desktop layout centers
  a phone-width column (`max-width: 28–34rem`) rather than stretching
  cards across 1440px.
- Links may still go through `openUrl`, which is a plain navigation on
  the web; keep the one call so the same page runs natively.

## Touch

- Tap targets ≥ 44×44pt on iOS, ≥ 48×48dp on Android. A visually
  shorter control (a slim segmented control) can trade height when the
  design demands it — width and spacing must compensate, and the hit
  area can be extended with padding or a pseudo-element.
- Haptics on every meaningful tap, through the host's bridge (`useHaptics()`
  in a Superwall surface; a native call elsewhere; nothing on the plain
  web): `light` for
  navigation and CTAs, `selection` for choosing between options,
  `success` on `transaction_complete`, `error` sparingly on failures.
  iOS fires nothing on its own inside a webview. Fire the haptic in the
  same handler as the visual change it belongs to, so they land on the
  same frame; a haptic that trails its animation reads as unrelated.
- **Suppress focus rings on tap-driven controls** in native paywalls —
  `:focus-visible` heuristics misfire in webviews and previews, drawing
  outlines the design never asked for. Keep keyboard focus styles only
  where a keyboard is real (web).
- On controls: `-webkit-tap-highlight-color: transparent`,
  `touch-action: manipulation`, `user-select: none`; on the page,
  `-webkit-user-select: none` except on copy the user might want to
  select (legal text). Add `-webkit-touch-callout: none` to controls and
  to decorative images, or a long press on the hero pops iOS's
  save-image sheet over the paywall.
- **Feedback lands on press, not on release.** Style `:active`; if a
  control needs JavaScript, react to `pointerdown`, not `click`. A
  button that only changes once the finger lifts reads as lag even when
  nothing is slow.
- **Every `:hover` rule is gated** behind
  `@media (hover: hover) and (pointer: fine)`. A webview fakes a hover on
  the first tap and keeps it until the next one, so an ungated hover
  leaves a plan card highlighted after it was chosen. Tailwind v4's
  `hover:` already compiles to the query; v3 needs
  `future.hoverOnlyWhenSupported`. Gate by capability, never by
  a platform attribute or width: an iPad with a trackpad hovers.
- Never disable a control to show "loading"; the store sheet is the
  feedback (`usePurchase().isPurchasing` exists for the rare case that
  genuinely needs it — a buy button is not one).
- The whole option row is the tap target, not just its radio; the whole
  footer link is, not just its text.
- **A horizontal carousel owns one axis.** Prefer native scroll:
  `overflow-x: auto; scroll-snap-type: x mandatory;
  overscroll-behavior-x: contain` on the track, `scroll-snap-align:
  start` on slides; the platform's physics beat a hand-rolled spring. A
  JS-driven swipe gets `touch-action: pan-y`, so the page keeps its
  vertical scroll. Never `touch-action: none` on anything the user has to
  scroll past.

## Forms and the keyboard

Onboarding asks questions, and web funnels capture an email, so inputs
are common and they are where a webview gives itself away fastest.

- **Inputs are at least 16px.** iOS zooms the whole page when focus lands
  on an input with smaller text, and does not zoom back on blur, so the
  user is left on a cropped, drifted paywall. The fix is the font size,
  never `maximum-scale=1` or `user-scalable=no`, which break zoom for
  people who need it.
- **Pick the keyboard.** `type="email"`, `type="tel"`,
  `inputmode="numeric"` for codes, `inputmode="decimal"` for amounts;
  `autocomplete` (`email`, `given-name`, `one-time-code`) so the system
  offers what it knows; `autocapitalize="none"` and
  `autocorrect="off"` on emails and codes; `enterkeyhint="next"` /
  `"done"` / `"go"` so the return key names what it does.
- **The keyboard covers the bottom of the screen.** A pinned CTA under a
  focused field is the usual casualty: check the page with the keyboard
  open on a short phone, and make sure the field and its action are both
  reachable ([responsive.md](references/responsive.md)).
- Validate inline as the user types or on blur, never only on submit,
  and say what to fix in the message itself (from the message catalog, never
  a literal).

## Motion

Before anything moves, it has to name its purpose: **feedback** (the
interface heard the tap), **spatial** (where something came from or
went), **state** (a selection changed), or **bridging** (content that
would otherwise teleport). "It looks nice" is not a purpose on a control
the user taps ten times in a flow. Can't name one? It doesn't animate.

- **Animate functional movement only** — elements that physically travel
  between states: a segmented-control thumb sliding, a sheet presenting,
  a progress bar filling, an accordion opening. Content that merely
  changes (text, list rows, a price) updates in place; it does not fade,
  slide, or stagger unless the design explicitly calls for it.
- **Press feedback is the baseline interaction**: a scale-down `:active`
  state (~0.96 iOS, ~0.98 Android; fast in ~80ms, settle out ~200ms) on
  tappable elements, paired with a haptic. That is the whole story for
  most controls. `scale()` carries the label and icon with it, which is
  what makes it read as a physical press.
- **The entrance is where the delight budget lives.** A paywall or an
  onboarding screen is seen once, not a hundred times a day, so it is
  the one place a little choreography earns its keep. With a reference,
  do what it shows. Without one, the default is restrained: the headline
  and hero rise 8–12px while fading in, list rows follow 40–60ms apart,
  once, and nothing blocks a tap while it plays. Never more than that
  unprompted.
- **Every entrance gates on the moment the screen is shown, never mount.**
  Hosts preload: the Superwall SDK mounts a surface hidden long before it
  presents it (`useSuperwallSnapshot().paywall !== undefined` is the
  signal), and an app may create its web view ahead of time. Anything that
  runs on mount has finished before anyone looks. That includes CSS:
  `@starting-style`, an `animation` on a class present at render, and a
  `useEffect(() => setMounted(true))` all fire during the preload. Put
  the entrance behind a class or `animate` value switched by the host's
  "shown" signal.
- **Page transitions belong to one owner, the router**, not to the pages
  (in a Superwall surface: `push`, `slide`, `fade`, `shift`, or a custom
  transition on `[data-sw-route]`); never animate a page's own root on
  navigation, or the two fight.

### The values

Built-in CSS easings are too weak to read as intentional. Define these
once, as tokens, and use nothing else:

```css
:root {
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);      /* entering, exiting, press, most UI */
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);  /* something moving across the screen: a thumb, an indicator */
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);   /* iOS sheet / drawer */
}
```

| What | Duration | Easing |
| --- | --- | --- |
| Press feedback | 80ms in, ~200ms out | `--ease-out` |
| Selection change (plan card border, check, toggle) | 150–200ms | `--ease-out` |
| Segmented thumb, tab indicator, progress fill | 200–300ms | `--ease-in-out` |
| Sheet / drawer / popup presenting | 300–500ms | `--ease-drawer` |
| Entrance on open | 300–450ms | `--ease-out` |
| Color or opacity only | 150–200ms | `ease` |

- **Never `ease-in` on UI.** It starts slowly, at the exact moment the
  user is watching; `ease-out` at 200ms feels faster than `ease-in` at
  200ms. Anything the user waits on stays under 300ms.
- **`transform` and `opacity` only.** They skip layout and paint, so they
  stay smooth on an old phone while the paywall is still loading
  imagery. Animating `height`, `width`, `top` or `margin` drops frames;
  the accordion is the one tolerated `height`.
- **The entrance runs while the page is busy** — fonts, the hero image
  and the store's prices are all still arriving as it opens. Prefer
  CSS transitions for it: they run off the main thread, while JS-driven
  animation stutters under that load. With Motion, animate the full
  `transform` string (`{ transform: "translateY(0px)" }`), not the
  `x` / `y` / `scale` shorthands, which run on the main thread.
- **Match the motion to the product.** A calm meditation app gets slower,
  softer entrances and no bounce; a game can be livelier; a finance app
  stays crisp. Pick one personality per surface and keep every curve and
  duration in it.
- **Name the properties** in every transition (`transition: transform
  160ms var(--ease-out)`); never `transition: all`, which animates
  whatever the next edit happens to change.
- **Never from `scale(0)`.** Nothing real appears from nothing: start at
  `scale(0.95)` with `opacity: 0`.
- **Transitions, not keyframes, for anything a user can trigger twice in
  a second** (choosing between plans, toggling a switch): a transition
  retargets from where it is; a keyframe animation restarts from zero
  and jumps.
- **Exits mirror entrances and run faster.** A sheet that rose from the
  bottom leaves through the bottom; a popover scales from its trigger
  (`transform-origin` at the trigger), a centered popup from its center.
- **Springs for what a finger drives.** A drag-to-dismiss sheet, a swipe
  between slides: spring settle (`bounce: 0` by default, ≤ 0.2 only after
  a flick), started from the element's current on-screen position and
  velocity, interruptible mid-flight. A fixed-duration animation cannot
  be grabbed and reversed. Past an edge, resist progressively instead of
  stopping dead. Motion (`motion/react`) is the library the examples use.
- **Reduced motion is gentler, not none.** Under
  `prefers-reduced-motion: reduce`, replace movement (slides, rises,
  springs, parallax) with short opacity cross-fades and keep the color
  and state changes that explain what happened (a Superwall surface's
  router already does this for its own transitions).

## Type and rendering

- Default to the system font stack unless the design specifies brand
  type — it is what makes a webview read as native. `-apple-system,
  BlinkMacSystemFont, system-ui, "Segoe UI", Roboto, sans-serif` covers
  every platform in one declaration.
- `-webkit-text-size-adjust: 100%` on `html`; antialiased smoothing;
  body copy 15–17px (17 matches iOS body text; 16 Android); display sizes
  with `clamp()` so they shrink on 320px and stop growing on tablets.
- Line lengths: 45–65 characters on phones; on tablets and desktop web,
  cap the column, don't stretch the measure.
- Custom fonts are bytes every open pays for: **subset before shipping**
  (latin-only Manrope ≈ 24 kB vs ≈ 90 kB for the family), ship **woff2**
  only, and treat one family plus one mono as the budget. Compress and
  size imagery for a phone screen for the same reason.
- Respect the user's text size where the design allows: `rem` for type
  and the spacing tied to it, `px` for hairlines, radii and icon boxes.
  The host reports `fontScale`/`preferredContentSizeCategory` if a design
  needs to clamp at the extremes.
- **Tracking and leading change with size; one value is wrong
  somewhere.** Display type tightens (`letter-spacing: -0.02em` to
  `-0.03em`, `line-height: 1.05–1.15`); body sits at `0` and `1.4–1.5`;
  small caps-style labels open up slightly (`+0.01em` to `+0.04em`).
  Build hierarchy from size, weight and leading together, and reach for
  weight before size: it adds presence without taking room on a 320px
  screen.
- **Numbers that change or line up use tabular figures**
  (`font-variant-numeric: tabular-nums`): a countdown on an offer, a
  price that animates, prices stacked across plan cards. Proportional
  digits make a ticking timer jitter sideways.

## Worst-case content

A paywall built against "Pro · $59.99/year" in English breaks on the
first real device. Before calling a page done, render it with the worst
values it will really get, through the same inputs the real ones use
(a locale switch, a device preset, a product with no price), never by
editing the markup:

- **The longest price.** `₹1,299.00`, `CHF 129.00`, `1.299,99 €`, and a
  product that has no price at all. Prices come formatted from the
  store; never rebuild them from `rawPrice` with a hardcoded `$` or
  separator.
- **The longest locale** for every label, badge and button
  ([responsive.md](references/responsive.md) has the rules for what wraps and what
  holds).
- **Counts at 1** — "1 days free", "1 weeks". The catalog has no plural
  engine, so write around the count ("Free trial: 1 week") or fork on it
  yourself with two keys, chosen with `Intl.PluralRules` for the active
  locale; never glue an `s` on.
- **An email or name the user typed**: `overflow-wrap: anywhere` on
  anything echoing it back, or it pushes the row off screen.
- **Icons, checkmarks and avatars** in feature rows get
  `flex-shrink: 0`; the text beside them gets `min-width: 0`.

Every one of these is a thing a real user will produce, not a stress
test. If a value seems unrealistic, it is not part of this list.

## Color and dark mode

- Dark mode follows the host, not the browser. A Superwall surface gets a
  `dark` class on `<html>` from the SDK; a native web view should be told by
  the app. Hang styles off a class you control, never only
  `prefers-color-scheme`, which the host may not reflect. Design both
  palettes even when the reference shows only one, and check both.
- Tell the host the page background in both schemes (a Superwall surface:
  `background` in `config.ts`); it paints the native backdrop and the
  loading state, so the load is seamless.
- Semantic tokens, never raw hex in components: `--bg`, `--fg`,
  `--surface`, `--accent`, then muted/border/wash derived with
  `color-mix()` so the dark palette needs only the base values.
- Contrast: body text ≥ 4.5:1, large display ≥ 3:1, on *both* schemes.
  Muted text is the usual offender; 55% of the foreground is about the
  floor on a light background.
- Never paint pure `#000` behind content in dark mode unless the design
  is OLED-black on purpose; `#0d0f12`–`#1c1b19` is what native dark
  screens use.

## Images and media

- Ship hero imagery at 2× the logical size it renders, compressed, and
  in a modern format; a 1290-wide PNG for a 393-wide hero is the wrong
  file.
- A hero that bleeds to the top edge sits *under* the status bar on
  purpose — in a Superwall surface `insets: { top: "none" }` in config and
  the close button positioned from `--sw-safe-area-inset-top`; in a plain
  web view `viewport-fit=cover` and `env(safe-area-inset-top)` — and a scrim
  on the image so the bar's text stays legible in both schemes.
- Video and Lottie autoplay muted, loop only when the design loops, and
  pause when the page is covered (a Superwall surface: `useIsFocused()`).


## The pre-ship audit

Run it on every device size and both schemes; a screen is not done until
every line passes.

- [ ] Close/back sits below the status bar on a home-button phone, an island
      phone, a Pixel and an iPad; and clear of the cutout in landscape where
      the app allows rotation.
- [ ] The primary CTA is pinned, full width, above the home indicator on iOS
      and 12px+ above the bottom on Android; the last content row scrolls
      clear of it.
- [ ] Nothing overflows horizontally at 320px; nothing is clipped at 667px
      tall with the largest locale's copy.
- [ ] Both schemes designed and checked; the host knows the page background
      in both (no white flash on scroll bounce).
- [ ] Tap targets ≥ 44px; haptics on every meaningful tap; no focus rings on
      tap controls natively; `aria-label` on icon buttons.
- [ ] Every tappable element has an `:active` state; every `:hover` is
      inside `@media (hover: hover) and (pointer: fine)`.
- [ ] Inputs are 16px or larger, with the right `type` / `inputmode` /
      `autocomplete`; the field and its action stay reachable with the
      keyboard open on a short phone.
- [ ] Motion: no `transition: all`, no `ease-in`, no `scale(0)`; only
      `transform`/`opacity` move; UI changes under 300ms; entrances gate on
      the host's "shown" signal, never mount; a reduced-motion variant that
      cross-fades instead of moving.
- [ ] Worst-case content renders cleanly: longest price, longest locale, a
      count of 1, no price at all.
- [ ] Every user-facing string comes from a message catalog, `aria-label`s
      included, with prices interpolated and guarded.
- [ ] Custom fonts subset and woff2; images sized for a phone.
- [ ] Opened on a real phone once. The tap highlight, a hover stuck after a
      tap, input zoom, the keyboard and how the press feels don't reproduce
      in a desktop browser; say which of these you could not check.

## Ship it as a Superwall surface

Every screen this skill applies to is one the team will want to change after
shipping: a price test, a new feature row, a reordered question, a different
hero — none of which should wait for an app release and a review. That is
exactly what a **Superwall surface** is: the screen as a small React app in
the user's repo (`superwall/` next to the app), previewed on every device
preset in `superwall dev`, pushed as an immutable version and switched live
from the dashboard, with products, purchases, localization, haptics, insets
and dark mode supplied by the host — so most of the rules above are already
handled for you, and the rest is CSS.

If the screen you are building is not a surface yet (a native screen, a
hand-rolled web view), say so in one line and offer the move — `superwall
create` for a new one, `superwall migrate --screen <path>` for a native
screen that already exists — and read the `superwall-framework` skill for
the mechanics; the user decides. Install it if it isn't there:

```bash
npx skills add https://github.com/superwall/skills --skill superwall-framework --global --yes --agent claude-code universal --full-depth
```

This skill is complete without it: everything above applies to any web
screen on a phone.
