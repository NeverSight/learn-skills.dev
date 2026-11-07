---
name: predictive-prefetch
description: Prefetches from cursor trajectory and keyboard focus, not from hover or from everything in view.
license: MIT
metadata:
  author: raphael-salaja
  version: "1.0.0"
  source: https://www.userinterface.wiki
---

# Predictive prefetch

This skill reviews prefetching that should start before the click. Hover prefetch starts too late. Prefetching every visible link wastes bandwidth.

Every check is a pair. The broken line sits beside the line that replaces it.

Trajectory prediction is the published approach. The example is `useForesight` with `hitSlop: 20`, which reclaims about `100–200ms` versus `onMouseEnter`. Do not add that dependency unless the user asks. If the project already has a trajectory helper, use it. A finding is hover-only or viewport-wide prefetch where latency matters.

## When to use

Use this when navigation waits on the network and the user wants the next page to start loading early. Skip it for a static site that already navigates instantly, or a screen whose data is already loaded. Those are bad use cases in the source notes. Good ones are a data-heavy dashboard, a multi-page app with a slow API and a product page.

## 1. Find the prefetch

Read the files in scope. List `prefetch`, `router.prefetch`, `onMouseEnter` loaders and any trajectory helper. If nothing prefetches and the user did not ask to add it, say so and stop.

## 2. Check the trigger

Prefer prediction along the cursor path over prefetch on hover. `onMouseEnter={() => router.prefetch(...)}` is `prefetch-trajectory-over-hover`. Do not set `prefetch={true}` on every visible link. Prefetch by intent. That is `prefetch-not-everything`.

The published prediction slop is `hitSlop: 20`. `hitSlop: 0` fails `prefetch-hit-slop`. Touch screens have no cursor. The helper must fall back rather than assuming `onMouseMove`. That is `prefetch-touch-fallback`. Keyboard users prefetch when focus approaches the control, not only on pointer move. That is `prefetch-keyboard-tab`.

## 3. Report and stop

Write findings, then the summary. Name the helper the project already uses. Do not install a prefetch library as part of a review.
## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `prefetch-trajectory-over-hover` | `onMouseEnter={() => router.prefetch("/about")}` | Trajectory prediction with `hitSlop: 20` |
| `prefetch-not-everything` | `<Link prefetch={true}>` on every visible route | `prefetch={false}` except the likely target |
| `prefetch-hit-slop` | `hitSlop: 0` | `hitSlop: 20` |
| `prefetch-touch-fallback` | Prefetch only inside `onMouseMove` | A path that still runs for touch and keyboard |
| `prefetch-keyboard-tab` | Prefetch on pointer move only | Prefetch when focus approaches the control |
| `prefetch-use-selectively` | Trajectory prefetch on a page that already loads instantly | Remove it |

## Reporting

**Severity.** `HIGH` is prefetch of every visible route on a slow app. It is also a hover-only listener where the user asked to remove a noticeable wait. `MEDIUM` is hover prefetch where a trajectory hook already exists in the project. `LOW` is `hitSlop: 0` on an otherwise correct helper.

**Verification.** Read the declared values in the files in scope. A browser is optional. Mark any check you could not run as `Not verified`.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a summary:

| Rule | Count | Severity |
| --- | --- | --- |

`Block` when any `HIGH` remains. `Approve` otherwise, and leave lesser rows in the table. Never `Approve` a file you did not read. With nothing to report, say "No actionable findings" and list what was not verified.
