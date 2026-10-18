---
name: feedback-states
description: >
  Design how one feature or screen in an iOS app behaves while it works: loading, showing saved data
  while refreshing, success, empty, error and retry, with the motion, haptics and words for each
  state, backed by real shipped apps. Use when asked to add or improve loading states, success or
  error feedback, empty states, retry flows, or "what should happen while this loads". SwiftUI and
  UIKit, iOS only.
license: MIT
compatibility: Needs the 60fps MCP server (https://mcp.60fps.design/mcp), signed in with OAuth.
metadata:
  author: 60fps-Design
  version: "1.0"
---

# Feedback states

Every action that takes time has the same few states, and most apps only design the happy one. Your
job is to take one feature, find every state it can be in, and make each one clear: what the user
sees, how it moves, what they feel, and what it says. The `60fps` library supplies real references.

Work on one feature or screen at a time: a save, a send, a purchase, a search, or how one screen
loads its data. If the user did not name one, ask which. Do not change code until step 5.

## 1. Map the triggers and the states from the code

Read the feature's view and the code that does the work (the view model, the `async` function, the
network call), plus any shared loading, error or freshness views and modifiers the app already has.

First list what starts the work, and every place it can start from (a button and a cell can both
add the same thing, and two entry points are how races happen). A user action (a tap on Save) is
one trigger. A screen load often
has several: opening the screen, coming back to the app, a timer, changing a filter, pull to refresh,
a Refresh or Try again button. Feedback differs by trigger, so keep them apart.

Then list every state the feature can actually reach, not just the ones it draws today:

- **Working, nothing to show yet**: the first load, or a user action in progress. Note how long it
  can take: under a second, a few seconds, or longer.
- **Working, saved data on screen**: showing what was there before while fresh data loads. For any
  data screen this is the most important state.
- **Success**: it worked. Is there a next step, or does the user stay put?
- **Partial success**: the main thing worked but a side effect failed (saved, but not exported).
- **Empty**: it worked but there is nothing to show.
- **Error**: it failed. Which errors are possible (offline, server, validation, permission), and is
  saved data still on screen?
- **Retry**: what happens when they try again, and when that fails too.
- **Interrupted**: they leave, background the app, change the filter, or tap again while it works.

States inside a system screen you cannot restyle (the photo picker, the camera, a share sheet) are
out of scope: design what happens after it closes.

If the action replaces or deletes something, check in the code that the old data survives a failure
(is it removed before the new data is safely saved?). Losing data is worse than any missing state.

For each, note the file and line and what the user sees today. Note feedback code that can never run
(an overlay inside a sheet that is already closed) so it can be removed. Also check that every promise in the
words is true in the code: "we will refresh when you are back online" needs something that watches
the network. If you cannot tell a state's look without running the app, say "not verified".

If a state is already handled well, mark it **Keep** and move on. The report is about the gaps.

## 2. Decide each state

Keep the whole flow calm and quick. Rules that hold almost everywhere:

- **Haptics answer a touch.** Success, error and confirmation haptics only when the result answers
  something the user just did (Save, Refresh, Try again), even if the work took a few seconds. Never
  for a load that started on its own (opening the screen, a timer, coming back to the app), and never
  two haptics for one event: search every haptic call the success path reaches, across files, since
  a view and a cell often each add one.
- **Working**: under about 400 ms, show no spinner (a flash reads as a glitch), but a load the user
  asked for still needs a small sign that it happened. Longer, show progress in place, on the thing
  being worked on, not a full screen blocker. After about 3 seconds, say what is happening.
- **Saved data on screen**: keep it visible and readable while fresh data loads, with a quiet sign
  that it is updating. Never blank a screen that had data.
- **Success**: confirm in place, on the control the user touched, then get out of the way.
- **Empty**: say why it is empty and what to do next. A still illustration is fine; a looping one is
  usually noise.
- **Error**: keep what the user typed or chose, and keep saved data on screen. Say what went wrong in
  plain words and what to do. If it answers a tap, an error haptic and a small, brief shake on that
  control are enough (about 6 points, 3 swings, 0.3 seconds). If nobody tapped, no haptic and no shake: a calm notice is enough.
- **Partial success**: confirm what worked, then a quiet note about what did not. Never an alert
  titled as a failure for something that mostly worked.
- **Retry**: if there is no way to retry (an alert that only says "try again"), add one, and keep the
  user's input in memory so retrying does not mean starting over. The button shows a working state
  while it tries. A second failure must look different
  from the first ("Still offline. Tried at 14:05."), or it looks like the tap did nothing.
- **Interrupted**: never leave a spinner running when the work has stopped, and never let a late
  result overwrite a newer one.

Match the app's tone and reuse its own shared views and modifiers before proposing new ones. Every
motion needs a Reduce Motion version (a crossfade, or no motion).

## 3. Find references

Search only for the states you are changing that need motion, usually success and retry, sometimes
working. Skip states marked Keep and states with no motion.

Call `60fps_search_shots` with the motion, the moment and the tone in plain words ("calm in-place
check after saving", "button shows a small spinner while it retries"). Do not lead with a surface
name like widget or settings. Judge results yourself by title, summary, `intensity` and `mood`; the
scores barely separate good from poor matches. The library is strong on celebrations and button
feedback and thin on calm errors, retries, offline notices and loading skeletons: for those, search once at most,
and expect "No close match" plus the motion described in words to be the answer.

## 4. Report

Lead with the gaps in one to three sentences, worst first (a wrong haptic or a broken promise beats
a missing animation). Then one table, in the order the user meets the states:

| State | Where | Today | What to do | Haptic | Words | Shot |
|---|---|---|---|---|---|---|

Use **Keep** for states that are already right, and "Not needed" in the Shot column for states with
no motion. Reuse the app's own error messages where it already maps errors to words. Below the table,
list any data loss risk first, then dead feedback code to remove. Then the Reduce Motion version in one line, and ask whether to build it.

## 5. Build it, when asked

Model the states explicitly (an enum with the cases you listed) rather than a set of booleans, so
impossible combinations cannot happen. Fetch `60fps_get_motion_breakdown` and
`60fps_get_motion_code` only for the shots the user picked, and adapt their timing, not their look.
Keep the user's design system. Make sure it compiles.

Write plainly: short sentences, common words. Never use em dashes or en dashes.

## Not for

Android, Flutter, React Native or web. Where an app should animate in general: use
`find-animation-opportunities`.
