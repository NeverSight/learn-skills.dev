---
name: find-animation-opportunities
description: >
  Find the places in an iOS app's UI where motion would genuinely help, what to leave still, and what
  existing motion is broken or overdone, and recommend real shipped interactions to copy for each.
  Use when asked where an app should animate, how to make it feel more alive or polished, to audit
  or review its motion or haptics, or what micro-interactions to add. Reads SwiftUI and UIKit code.
  iOS only.
license: MIT
compatibility: Needs the 60fps MCP server (https://mcp.60fps.design/mcp), signed in with OAuth.
metadata:
  author: 60fps-Design
  version: "1.0"
---

# Find animation opportunities

Most apps do not need more animation. They need it in a few places that carry meaning, and nowhere
else. Your job is to find those places in the user's code, say plainly what should stay still or
be toned down, and back each recommendation with a real interaction from the `60fps` library.

Motion here means visual motion AND haptics: both are part of how an app feels.

Do not change any code in this pass. The deliverable is a short report.

## 1. Take stock of the motion that is already there

Before looking for gaps, search the code for what the app already does: `withAnimation`,
`.animation(`, `.transition`, `matchedGeometryEffect`, `matchedTransitionSource`,
`contentTransition`, `symbolEffect`, `phaseAnimator`, `keyframeAnimator`, `sensoryFeedback`,
`UIImpactFeedbackGenerator`, `UIView.animate`, and any reduce motion checks. On a big app this is a long list: group it by file and read the
haptics and transitions first, they are where most problems hide.

Then say which kind of app this is:

- **Little motion.** Most of the value is new opportunities.
- **Already rich.** Say so at the top. The value is now the few gaps, motion that is broken, and
  motion that is overdone. Do not recommend what the app already does.

Note the app's tone from its existing motion and design: calm and restrained, or bold and playful.
Every recommendation must match it.

## 2. Decide the scope

If the user named a screen or a feature, look only there. Otherwise cover the screens a user sees
most: the root view and whatever it presents (tabs, overlays, sheets, the flows they open), plus
widgets, Live Activities and other extensions, which are easy to forget. Widgets cannot run their
own animations: the only motion there is a content transition when the timeline changes (rolling
digits, a crossfade), so never suggest more. Read the state that drives
a view too (`@Observable` models, view models, the code that assigns new data), not only the view:
the fix is often where the state changes.

Skip views nothing constructs and code paths that cannot run today (for example behind a flag that
is always on). If one matters later, mention it once and label it as not reachable yet.

Report at most 10 findings, counting the table and the fixes together (the leave still list does not
count). A short table is fine when the real value is in the fixes. When there are more candidates, rank by how much the moment means
against how often it happens: rare and meaningful first, frequent and minor last.

## 3. Find the moments

Moments worth motion:

- **Waiting.** A network call or slow work with only a spinner, or nothing at all.
- **Success and failure.** A save, send, purchase or completion that ends silently, or an error that
  just resets with no feedback.
- **Things appearing and leaving.** Rows inserted, deleted or reordered, cards dismissed, items added.
- **Where did it go.** A thumbnail that opens to detail, anything where continuity helps the user
  keep their place.
- **Choice and state.** Toggles, selection, tabs, segmented controls that snap with no feedback.
- **Numbers that change.** Balances, counts, timers, progress.
- **Empty and first-run states.** The first thing a new user sees.
- **Direct manipulation.** Drags, swipes and long presses that should follow the finger.

Also check the motion that exists:

- **Broken.** A `.transition` whose state change is not inside `withAnimation`, so it never plays.
  An animation attached to the wrong value. A reduce motion check read once instead of from
  `@Environment(\.accessibilityReduceMotion)`, so it misses changes while the app is open.
- **Overdone.** A success haptic or a celebration on something routine (every refresh, every poll).
  Search for every `.success` haptic: if the app saves it for one big moment, any other use is a
  finding. A long animation on a path the user takes many times a day.
- **Fallback that removes meaning.** A reduce motion branch that makes a meaningful change snap with
  nothing at all, where a crossfade would keep the meaning. Existing motion with no fallback at all
  is a fix too.

For each finding note the file and line where the change should happen (usually where the state is
set), and the view it shows up in if that is a different file.

## 4. Decide what to leave still

Say this out loud in the report. It is half the value.

Leave it still when:

- **It repeats.** Actions done many times a day (typing, scrolling a feed, a tab bar tapped fifty
  times, data that refreshes every few seconds) wear out any animation. Keep these instant or plain.
- **People are reading.** Long text, settings, data tables, forms. Motion pulls the eye away.
- **It is in the way.** Never make the user wait for an animation to finish before they can act.
  Anything longer than about 300 ms on a frequent path is too long.
- **The system already does it.** Navigation pushes, sheets, alerts, keyboard, system sign in.
  Restyling them usually makes the app feel less native, not more.
- **It is decoration.** A loop or flourish that says nothing about state.
- **The screen already has a moment.** One memorable motion per screen. Two compete.

Every recommendation needs a Reduce Motion fallback: a crossfade, or no motion.

## 5. Find a real reference for each opportunity

For every opportunity in the table, call **`60fps_search_shots`**. Describe the MOTION and the moment,
plus the app's tone, in plain words: "a calm ring that fills once to mark a milestone" works,
"achievement" does not. Do not lead with the surface name (widget, settings, cell): it pulls in
shots about that surface instead of the motion.

The search always returns something and its scores barely separate good matches from poor ones, so
judge every result yourself by its title and summary. Prefer results whose `intensity` and `mood`
match the app's tone. If the first search misses, try once more with different words (add mood
words like calm, subtle, playful). If nothing fits after that, write "No close match" rather than
stretching, and describe the motion in words instead. Fixes need no search, and neither does a
haptic-only change. A partial fit is fine when you say which part to take: "the row slide only, not the
confetti".

Only fetch more when the user picks one. Then `60fps_get_motion_breakdown` gives the timing and
`60fps_get_motion_code` the SwiftUI to adapt (see the `motion-reference` skill).

## 6. Report

Lead with the answer in two or three sentences, including whether the app already moves well. If a
fix is severe (content invisible, a broken flow), say it in the lead, not only in the fixes. If a
non-motion fact changes a recommendation (the screen a tap should open does not exist yet), add one
line under the table. Then
one table, most valuable first:

| Where | Moment | What to do | Reduce Motion | Shots |
|---|---|---|---|---|
| `CheckoutView.swift:84` | Pay ends with no feedback | Morph the button into a check, then dismiss | Crossfade to the check | [Shot title](shotUrl), take the check only |

Then, only if there are any, **Fix or tone down**: broken or overdone motion, each with file, line
and a one-line fix. Then **Leave these still**, each with a one-line reason.

End by asking which one to build, and point out any that are a one-line fix. Write plainly: short
sentences, common words, no hype. Never use em dashes or en dashes.

## Not for

Android, Flutter, React Native or web apps: say the library is iOS only and give general advice
without shots. Performance or frame rate problems are a different question.
