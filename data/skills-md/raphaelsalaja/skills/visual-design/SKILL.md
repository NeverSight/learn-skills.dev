---
name: visual-design
description: Sets concentric radii, layered shadows, alpha borders and a shared spacing scale.
license: MIT
metadata:
  author: raphael-salaja
  version: "1.0.0"
  source: https://www.userinterface.wiki
---

# Visual design

This skill reviews nested radii, shadows, borders and spacing. It uses the values published for userinterface.wiki.

Every check is a pair. The broken line sits beside the line that replaces it.

Where two rounded boxes nest with an even gap, the outer radius equals the inner radius plus that padding. A single hard shadow is a finding when the surface is meant to lift. Motion timing of a hover belongs to `timing-functions`. A pseudo-element used for a non-shadow decoration belongs to `pseudo-elements`.

## When to use

Use this when building or reviewing cards, buttons, menus and the space between them. Use `interface-typography` for type. Use `laws-of-ux` for target size and grouping laws.

## 1. Read the surfaces

Read the files in scope. List radii, `box-shadow`, borders and raw padding values. If the project already has tokens for these, use the tokens and only flag departures.

## 2. Check radius, shadow and border

For an even inset, `outer radius = inner radius + padding`. The published pair is an inner radius of `8px` and padding of `8px`, so the outer radius is `16px`. The same radius on both boxes is `visual-concentric-radius`.

Layer at least three shadows, with blur growing and opacity falling. A published card is `0 1px 2px rgba(0, 0, 0, 0.06)`, `0 4px 8px rgba(0, 0, 0, 0.04)`, `0 12px 24px rgba(0, 0, 0, 0.03)`. One `0 4px 16px rgba(0, 0, 0, 0.2)` shadow is `visual-layered-shadows`. Every shadow on the screen shares one light direction. A tooltip shadow upward while cards shadow downward is `visual-shadow-direction`. Do not use a hard pure-black shadow such as `rgba(0, 0, 0, 0.25)`. A published neutral is `rgba(17, 24, 39, 0.08)`. That is `visual-no-pure-black-shadow`.

Elevation uses one scale. The published steps are `--shadow-1: 0 1px 2px rgba(0, 0, 0, 0.05)` for a card, `--shadow-2: 0 2px 8px rgba(0, 0, 0, 0.08)` for a dropdown, `--shadow-3: 0 8px 24px rgba(0, 0, 0, 0.12)` for a modal. That is `visual-shadow-matches-elevation`. Do not transition `box-shadow`. Put the raised shadow on a `::after` and transition its `opacity` over `0.2s`. That is `visual-animate-shadow-pseudo`.

Borders use a translucent token such as `var(--gray-a4)`, not a hardcoded `#e5e5e5`. That is `visual-border-alpha-colors`.

A polished button uses six layers. Those are a `0.5px` outer cut, a `1px` inset ambient highlight and a `1px` inset top highlight. Add at least three external shadows, a `1px` text shadow and a gradient so slight you barely see it. The published stack is below. That is `visual-button-shadow-anatomy`.

```css
.button {
  background: linear-gradient(
    to bottom,
    color-mix(in srgb, var(--gray-12) 100%, white 4%),
    var(--gray-12)
  );
  box-shadow:
    0 0 0 0.5px rgba(0, 0, 0, 0.3),
    inset 0 0 0 1px rgba(255, 255, 255, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.07),
    0 1px 2px rgba(0, 0, 0, 0.1),
    0 2px 4px rgba(0, 0, 0, 0.06),
    0 4px 8px rgba(0, 0, 0, 0.03);
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.15);
}
```

## 3. Check spacing

Use a scale. The published steps are `4, 8, 12, 16, 24, 32, 48`. Padding of `17px` or a gap of `13px` is `visual-consistent-spacing-scale`. Match the project's scale when it already has one.

## 4. Report and stop

Write findings, then the summary. Do not restyle a surface the user did not include.
## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `visual-concentric-radius` | Outer and inner both `border-radius: 16px` with `8px` padding | Outer radius `calc(8px + 8px)` |
| `visual-layered-shadows` | `box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2)` | Three layers, blur growing, opacity falling |
| `visual-shadow-direction` | A card shadow down and a tooltip shadow up | One downward offset on every surface |
| `visual-no-pure-black-shadow` | `rgba(0, 0, 0, 0.25)` | `rgba(17, 24, 39, 0.08)` |
| `visual-animate-shadow-pseudo` | `transition: box-shadow 0.2s ease` | Opacity on a `::after` that holds the raised shadow |
| `visual-border-alpha-colors` | `border: 1px solid #e5e5e5` | `border: 1px solid var(--gray-a4)` |
| `visual-button-shadow-anatomy` | `box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)` on a raised button | The six-layer stack in this skill |
| `visual-consistent-spacing-scale` | `padding: 17px` and `gap: 22px` | `4, 8, 12, 16, 24, 32, 48` |

## Reporting

**Severity.** `HIGH` is a nested radius that breaks the curve, or shadows that point in conflicting directions. `MEDIUM` is a single harsh shadow, a hardcoded opaque border, or spacing off the scale. `LOW` is a button missing one layer of an otherwise present anatomy.

**Verification.** Read the declared values in the files in scope. A browser is optional. Mark any check you could not run as `Not verified`.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a summary:

| Rule | Count | Severity |
| --- | --- | --- |

`Block` when any `HIGH` remains. `Approve` otherwise, and leave lesser rows in the table. Never `Approve` a file you did not read. With nothing to report, say "No actionable findings" and list what was not verified.
