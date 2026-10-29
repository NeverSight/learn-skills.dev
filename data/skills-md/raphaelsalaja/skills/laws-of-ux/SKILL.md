---
name: laws-of-ux
description: Reviews targets, choices, response time and grouping against the UX laws used on userinterface.wiki.
license: MIT
metadata:
  author: raphael-salaja
  version: "1.0.0"
  source: https://www.userinterface.wiki
---

# Laws of UX

This skill reviews an interface against the UX laws published on userinterface.wiki. It flags a concrete mismatch, not a wish that the screen were simpler.

Every check is a pair. The broken line sits beside the line that replaces it.

A control under `32px` with no expanded hit area is a finding. A blank wait with no feedback is a finding. "This could be prettier" is not a finding. Spacing tokens and shadows belong to `visual-design`. The pseudo-element hit recipe belongs to `pseudo-elements`. Animation length belongs to `timing-functions`. The `400ms` rule here is the time until the interface responds, not the length of a transition.

## When to use

Use this when reviewing a flow, a form, a menu or an empty and loading state for friction. Use the domain skill that owns a visual value when the issue is type, color, motion or sound.

## 1. Name the surface

Read the files or the screen in scope. Restate the primary action in one sentence. If the request is "review the whole product", ask which flow.

## 2. Check the body and the clock

Interactive targets are at least `32px` on the smaller side. That is `ux-fitts-target-size`. When the visible glyph is smaller, expand the hit area. The inset recipe is `pseudo-elements`. That requirement is `ux-fitts-hit-area`.

The interface responds within `400ms` or shows immediate feedback. Silence during `await` is `ux-doherty-under-400ms`. When the work cannot finish that fast, show a skeleton, an optimistic value or a progress indicator. A loading branch that returns `null` is `ux-doherty-perceived-speed`. Show progress toward a multi-step goal. That is `ux-goal-gradient-progress`. Show an incomplete profile or checklist rather than hiding the gap. That is `ux-zeigarnik-show-incomplete`. End the flow with an explicit success state. That is `ux-peak-end-finish-strong`.

## 3. Check choices, order and grouping

Do not present every option at once when most users need a short set. Advanced options go behind a disclosure. That is `ux-hicks-minimize-choices` and `ux-progressive-disclosure`. Chunk long data into groups of about `5–9`, as in a card number split by fours. That is `ux-millers-chunking`. Put the key item first or last, not in the middle of a menu. That is `ux-serial-position`.

Accept messy input and display clean output. A phone field that rejects a normal paste is `ux-postels-accept-messy-input`. Use a control people already know. A custom navigation gesture with no label is `ux-jakobs-familiar-patterns`. Move formatting and calculation into the system. That is `ux-teslers-complexity`.

Related items sit closer than unrelated ones. The published form sample uses `4px` under a label, `2px` under the input and `24px` before the next group. Uniform `16px` between label, field, hint and divider is `ux-proximity-grouping`. The same function looks the same. That is `ux-similarity-consistency`. Group with a boundary or a shared region, not only with whitespace. That is `ux-common-region-boundaries`. Connect steps that are one process, such as a line between them. That is `ux-uniform-connectedness`.

The primary or destructive action is visually distinct. That is `ux-von-restorff-emphasis`. A raw control inside a styled product, or a styled control inside a raw one, is `ux-aesthetic-usability`. Simplify a noisy cluster into one clear form. That is `ux-pragnanz-simplify`. Cut extraneous copy and chrome that do not serve the step. That is `ux-cognitive-load-reduce`.

Do not flag a feature as the unimportant `80%` unless the user asked what to cut. When they did, the critical path stays prominent and the rest stays reachable. That is `ux-pareto-prioritize-features`.

## 4. Report and stop

Write findings, then the summary. One row per root cause. Do not propose a new information architecture in the same pass.
## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `ux-fitts-target-size` | `.icon-button { width: 16px; height: 16px }` | `width: 32px; height: 32px` |
| `ux-fitts-hit-area` | A link whose hit box equals the text | `inset: -8px -12px` on `::before` |
| `ux-hicks-minimize-choices` | Every setting rendered in one list | Common rows first, the rest in `<details>` |
| `ux-millers-chunking` | `4532015112830366` | `4532 0151 1283 0366` |
| `ux-doherty-under-400ms` | `await fetchData()` and then `setResult` | `setResult(optimisticData)` before the await |
| `ux-doherty-perceived-speed` | `if (isLoading) return null` | `if (isLoading) return <Skeleton />` |
| `ux-postels-accept-messy-input` | A field that rejects a normal paste | Accept the paste, display it clean |
| `ux-progressive-disclosure` | Advanced controls beside the primary ones | Hide them until asked |
| `ux-serial-position` | The primary action in the middle of a peer list | First or last |
| `ux-proximity-grouping` | Label, field, hint and divider all at `margin-bottom: 16px` | `4px` under the label, `24px` before the next group |
| `ux-von-restorff-emphasis` | A destructive action in the same weight as a neutral one | A distinct treatment |
| `ux-peak-end-finish-strong` | The flow ends on the last click | An explicit success state |

## Reporting

**Severity.** `HIGH` is a target under `32px` with no expanded hit area, or a wait with no feedback past the point the user can notice. `MEDIUM` is a missing success or progress state, a choice list with no disclosure, or related fields spaced like unrelated ones. `LOW` is a serial-position or similarity miss on a secondary control.

**Verification.** Read the declared values in the files in scope. A browser is optional. Mark any check you could not run as `Not verified`.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a summary:

| Rule | Count | Severity |
| --- | --- | --- |

`Block` when any `HIGH` remains. `Approve` otherwise, and leave lesser rows in the table. Never `Approve` a file you did not read. With nothing to report, say "No actionable findings" and list what was not verified.
