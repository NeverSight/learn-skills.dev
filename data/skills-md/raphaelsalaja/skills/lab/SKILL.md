---
name: lab
description: Builds a temporary page that shows every variant and state of real components at once, each linked to its source.
disable-model-invocation: true
---

# Lab

This skill builds a page for inspecting components. Every variant and every state of the real components sits open on one screen, so the user can tune them without clicking through the app.

## Every state open, nothing faked

The lab renders the real components, not copies. States that need a click, such as an open menu or a hover, are forced open. The lab is a development page and never ships.

Exploring new options for one idea belongs to `prototype`. The values on the page come from `defaults`, `motion`, `color` and the project's tokens.

## 1. Find the states

Read each component and list its variants, sizes and states: hover, pressed, focus, open, selected, disabled, loading, empty and error. A lab that shows the resting state only is `lab-every-state`.

## 2. Build one route

Add one development-only route, such as `/lab`, that imports the real components. Copy [lab.js](lab.js) into the app and load it once on that route. A lab built from copied markup is `lab-real-components`.

## 3. Force states open

Render menus, popovers, tooltips and submenus open with their controlled props or `data-*` attributes. Hold hover and focus with `force` on the entry, such as `force="hover"`. A menu that needs a click to see is `lab-states-open`. Use the app's current theme unless the user asked for both. That is `lab-one-theme`.

## 4. Link each entry to its source

Wrap each state in a `lab-entry` naming its component, state and source line, as the header comment in `lab.js` shows. An unlabelled grid is `lab-link-the-source`. When the user asked to tune values, add a `lab-tune` for each custom property with its range.

The grid, labels, filters and controls ship with the skill, so write entries only. A lab page with its own grid, labels or styles is `lab-shipped-frame`.

## 5. Open it

Start the dev server and open the lab. A route named in the reply but never opened is `lab-open-it`.

## 6. Keep it out of the release

Gate the route and `lab.js` to development, or delete both before release. A lab reachable in production is `lab-not-in-production`.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `lab-every-state` | The resting button only | Rest, hover, pressed, focus, disabled and loading |
| `lab-real-components` | Copied markup for each state | The real `Button` imported |
| `lab-states-open` | A menu behind a trigger | `<Menu open>` with its submenu open |
| `lab-one-theme` | Light and dark side by side, unasked | The app's current theme |
| `lab-link-the-source` | An unlabelled grid | `Menu / Submenu Open` linked to `menu/index.tsx` |
| `lab-shipped-frame` | A lab grid and labels written from scratch | `lab.js` loaded, only `lab-entry` elements written |
| `lab-open-it` | "Added `/lab`" | The lab opened for the user |
| `lab-not-in-production` | `/lab` live on the production site | The route gated to development |

## Reporting

**Severity.** `HIGH` is a lab built from copies, or a lab reachable in production. `MEDIUM` is a missing state, a state that still needs a click or a hand-written lab page. `LOW` is an unlabelled entry, or a lab that was not opened for the user.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Mark every state you could not render as `Not verified`.
