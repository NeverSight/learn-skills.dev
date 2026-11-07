---
name: color
description: Holds text and control contrast to exact ratios, routes colour through role tokens and gives dark mode its own palette.
---

# Color

This skill holds the colour rules that apply on every screen. It covers contrast, role tokens, translucent neutrals, dark mode and what the accent is for.

## Ratios are exact, measured on screen

The contrast ratios here are exact and apply in every theme. A ratio is read from the colour the screen draws, never guessed from a token's name. A ratio under the threshold is a finding in any style.

Searching for an existing token belongs to `reuse`. `color-scheme`, `theme-color`, the theme switch and status shown by colour alone belong to `defaults`. Whether a colour should be there at all belongs to `restraint`.

## Body text clears 4.5:1

Text under 24px, or under 18.66px when bold, meets 4.5:1 against what sits behind it. Larger text meets 3:1. Placeholders and secondary text count, and disabled controls do not. `#999` text on white, at 2.8:1, is `color-text-contrast`.

## Field edges and icons clear 3:1

The edge that shows where a field is, a toggle's track and an icon that carries meaning meet 3:1 against their surround. A field whose only edge is a `#e5e5e5` border on white, at 1.3:1, is `color-ui-contrast`. Dividers and the ring on a floating surface are decoration and exempt.

## Measure the colour on screen

Translucent colours and `opacity` composite over every layer behind them before the ratio is read. Read each theme and each surface the text appears on. A ratio taken from the token's hex while the text sits at `opacity: 0.6` is `color-measure-composited`.

Run [contrast.js](contrast.js) in the page through the browser's evaluate call. Treat each result as a candidate, and confirm it in a zoomed crop before reporting it.

## Text over images takes a scrim

Text on a photo or a video sits on a gradient scrim or a solid plate. The ratio holds at the lightest point of the image under the text. White text over a bright sky is `color-scrim-under-text`.

## Components use role tokens

Components reference tokens named for their role, such as `--text-secondary` or `--surface-raised`. Only the theme file maps a role to a palette step. `color: var(--gray-500)` inside a component is `color-role-tokens`.

## Neutrals on surfaces are translucent

Borders, dividers, hover fills and pressed fills use alpha neutrals, so they read on any surface beneath them. A solid `#f5f5f5` hover fill that vanishes on a grey card is `color-alpha-neutrals`.

## Dark mode is its own palette

Dark surfaces rise by getting lighter, because a shadow barely shows on a dark page. A dark popover the colour of the page, raised by a shadow alone, is `color-dark-raises-lighter`.

Accents and status colours take dark values tuned for contrast. The light `#2563eb` link reused on a `#0a0a0a` page, at 3.8:1, is `color-dark-tuned-accents`.

## The accent marks action

The accent colour marks the primary action, the selection and focus. An accent heading or a row of accent icons is `color-one-accent`.

Each status colour keeps one meaning. Red marks errors and destructive actions only. A red "New" badge is `color-status-meaning`.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `color-text-contrast` | `color: #999` on white, 2.8:1 | `color: #737373`, 4.7:1 |
| `color-ui-contrast` | A field edged by `#e5e5e5` on white, 1.3:1 | `border-color: #8a8a8a`, 3.5:1 |
| `color-measure-composited` | "The token is `#171717`, so it passes" | The ratio of the drawn colour at `opacity: 0.6`, read on screen |
| `color-scrim-under-text` | White text straight over a photo | `linear-gradient(to top, rgba(0, 0, 0, 0.6), transparent)` under the text |
| `color-role-tokens` | `color: var(--gray-500)` in `Card` | `color: var(--text-secondary)` |
| `color-alpha-neutrals` | `background: #f5f5f5` on hover | `background: var(--gray-a3)` on hover |
| `color-dark-raises-lighter` | A dark popover at the page's `#0a0a0a` | The popover at `#1a1a1a` over the `#0a0a0a` page |
| `color-dark-tuned-accents` | `#2563eb` links on `#0a0a0a`, 3.8:1 | `#60a5fa` in the dark theme, 7.8:1 |
| `color-one-accent` | Section headings in the accent colour | Headings in `--text-primary`, the accent on the primary button |
| `color-status-meaning` | A red "New" badge | A neutral or accent badge |

## Reporting

**Severity.** `HIGH` is body text under its ratio on a primary surface, a field whose edge fails 3:1 or text over an image with no scrim. `MEDIUM` is a palette step inside a component, a solid neutral that vanishes on a surface or a ratio never read on screen. It is also a dark surface raised by shadow alone or a light accent reused in dark mode. `LOW` is the accent used for decoration or a status colour carrying a second meaning.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong (measured ratio)
```

Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Never `Approve` a theme you did not open. Mark text over canvas, video and cross-origin frames as `Not verified`.
