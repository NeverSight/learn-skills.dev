---
name: prototype
description: Builds several real, labelled variants of one idea on a single page so the user can pick, then deletes the rest.
disable-model-invocation: true
---

# Prototype

This skill explores one idea as several working variants. The user compares them in the running app, picks one and the others are deleted.

## Real code, then gone

Each variant is real code with real data in the real app, not a mockup. Build the number asked for. With no number, build five that differ in approach, not only in colour. The page is temporary and goes once a variant is picked.

Every state of an existing component on one page belongs to `lab`. Copying an outside reference belongs to `match`.

## 1. Restate the idea

Write the idea in one line and the axis the variants explore, such as layout, motion or density. Ask one question when the idea has two readings.

## 2. Build real variants

Use the project's components and real or realistic data. A static image or lorem ipsum is `prototype-real-code` or `prototype-real-data`.

## 3. Put them on one page

Show every variant on one route. Separate pages per variant is `prototype-one-page`. Copy [switcher.js](switcher.js) into the app beside that route and load it once, as its header comment shows. Wrap the variants in `<prototype-switcher>`, one child each with `data-variant` and an optional `data-note`.

The switcher ships with the skill, so write the variants only. A switcher, tab row or grid written from scratch is `prototype-shipped-switcher`.

Give each a short label that says how it differs. "Variant 3" is `prototype-label-variants`. Use the app's current theme unless the user asked for both. Light and dark side by side by default is `prototype-one-theme`.

## 4. Open it

Start the dev server, open the page and look at every variant once. A path in the reply with nothing opened is `prototype-open-it`.

## 5. Prune after the pick

The bar's Pick button copies a line such as "Pick Inline Filters from /prototypes/filters" for the user to paste back. When the user picks, move that variant into the product. Delete the losing variants with the route, `switcher.js` and its type declaration. Leftover variants after a pick is `prototype-prune-after-pick`.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `prototype-real-code` | A static mockup image | The variant built from project components |
| `prototype-real-data` | Lorem ipsum rows | Real or realistic rows |
| `prototype-label-variants` | `Variant 3` | `Inline Filters` |
| `prototype-one-page` | Five routes, one per variant | One route with a switcher |
| `prototype-shipped-switcher` | A switcher written from scratch | `switcher.js` loaded, only the variants written |
| `prototype-one-theme` | Light and dark side by side, unasked | The app's current theme |
| `prototype-open-it` | "Built at `/prototypes/filters`" | The page opened, every variant checked |
| `prototype-prune-after-pick` | Four losing variants left in `src/` | The pick shipped, the rest deleted |

## Reporting

**Severity.** `HIGH` is a variant that does not run, or losing variants left after a pick. `MEDIUM` is placeholder data, unlabelled variants, variants that differ only in colour or a hand-built switcher. `LOW` is a page that was not opened for the user.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Mark every variant you could not open as `Not verified`.
