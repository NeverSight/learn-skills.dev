---
name: motion-system
description: >
  Give an iOS app one consistent motion language: a small set of named timings, springs and haptics
  in a single Motion.swift, derived from the app's own code and from real shipped apps with the same
  feel. Use when asked to make an app's animations consistent, create motion tokens or a motion
  system, clean up scattered animation values, or define how the app should move. SwiftUI, iOS only.
license: MIT
compatibility: Needs the 60fps MCP server (https://mcp.60fps.design/mcp), signed in with OAuth.
metadata:
  author: 60fps-Design
  version: "1.0"
---

# Motion system

An app feels like one app when the same kind of moment always moves the same way. Most codebases
drift: a dozen durations, springs nobody could tell apart, a success haptic used for everything. Your
job is to replace that drift with a few named values, grounded in the app's own best motion and in
real apps from the `60fps` library.

The deliverable is a proposal, then one new file. Do not edit existing call sites until the user
agrees to the proposal.

## 1. Find the floor

Read the app target's `IPHONEOS_DEPLOYMENT_TARGET`. When the target sets its own value it overrides
the project-wide one, in either direction. Look wherever the project defines it: the `.xcodeproj`,
an XcodeGen `project.yml`, `.xcconfig` files, or `Package.swift`. Every API you propose must exist at
that version. Note the Swift language mode and any default actor isolation setting too; you need them to
compile in step 5.

## 2. Inventory what the app does now

Search the code for every motion value and everything timed against one:

- **Animations**: `withAnimation(`, `.animation(`, `.spring(`, `.interactiveSpring`,
  `.interpolatingSpring`, `.smooth`, `.snappy`, `.bouncy`, `.easeIn`, `.easeOut`, `.easeInOut`,
  `.linear`, `.default`, `duration:`, `.delay(`, `response:`, `dampingFraction:`. A bare `.smooth`,
  `.snappy` or `.bouncy` is a value too (0.5 s by default), so count it.
- **Transitions and effects**: `.transition(`, `contentTransition`, `matchedGeometryEffect`,
  `matchedTransitionSource`, `phaseAnimator`, `keyframeAnimator`, `symbolEffect`.
- **Timing coupled to animation**: `Task.sleep`, `asyncAfter`, completion handlers. These are the
  riskiest to change: a sleep tuned to a 0.35 s animation breaks when the animation changes.
- **Haptics**: `sensoryFeedback`, the `UI...FeedbackGenerator` classes, and the call sites of any
  wrapper the app has around them (a `HapticManager` with 50 call sites matters more than the class).
- **Reduce Motion**: every way it is read (`accessibilityReduceMotion`, `isReduceMotionEnabled`).
- **Existing helpers**: any `Motion`, `Animation` or haptics extension or manager.

Group the values by the job they do, not by file:

- **Feedback**: a press, a toggle, a selection, a small swap in place. Should be quick.
- **Change**: content swapping, a row appearing, a number changing.
- **Arrival**: a sheet, a card, a screen element entering.
- **Emphasis**: the rare moment that should be felt (a success, a milestone).
- **Haptics**: which kind is used for what.

Count the distinct values in each group. That count is the problem statement: "Arrival uses 8
different timings between 0.3 s and 0.7 s". Some motion is not a job and stays out of the system:
gesture tracking (parallax, a finger-following drag) and values a comment says are load-bearing.
List those as deliberate exceptions.

Extend what exists. If the app has a haptics wrapper (often with an in-app on/off switch), new haptic
roles go through it, never around it: `sensoryFeedback` would bypass the switch. If an existing
motion helper is broken or unused, say so and propose fixing or removing it, never a second helper
beside it.

## 3. Find the app's tone

Read the existing motion and the design (colours, type, how playful the copy is) and name the tone in
a few words: calm and precise, soft and friendly, bold and playful. Every value you propose must fit
it. A finance app should not get game springs.

## 4. Ground it in real apps

Call `60fps_search_shots` once per job that needs a reference. Describe the motion and the tone, not
the object: "sections fading in one after another as a screen loads, calm" finds arrivals, while
"cards arriving" finds card stacks. Pick 3 to 5 shots that match the tone, judging by title,
summary, `intensity` and `mood`, not by the score. Prefer shots whose `motion` tags suggest springs,
fades or crossfades: timing driven by a `TimelineView` or custom math has no animation values to
read. When nothing fits the tone (calm apps rarely find a calm celebration), the app's own best
value is the source, and say so.

For those shots only, call `60fps_get_motion_code`. Use it only when `source` is `generated`, and read
the `generated` field's own lines: `withAnimation` and `.animation` values, spring parameters,
delays, haptic calls. Ignore the response's top-level `animation`, `recipes` and `stagger_delay`
fields: they are generic starter values, often identical across shots. A `recipes` result has no shot
numbers at all, and neither does a demo whose timing is computed, so skip it and pick another. The file is a self-running demo, so skip its loops and replays.

In this skill, do NOT show the code files to the user, even though the tool's own instructions say
to: you only need a few timing lines from each, and the files are long. The numbers come from an AI
recreation of a real app's video, so they are a strong reference, not a measurement. Each call
counts against the user's daily allowance, so stop at 5.

## 5. Propose the system

Keep it small. A system nobody can remember is not a system.

- **Animations**: about 4 named values, one per job, for example `Motion.feedback`,
  `Motion.change`, `Motion.arrival`, `Motion.emphasis`, plus the deliberate exceptions from step 2.
  Use the newest spring API the floor allows. At iOS 17 and up, prefer `.spring(duration:bounce:)`, or
  `.smooth`, `.snappy` and `.bouncy` with `duration:`. Note that `extraBounce:` is added to the
  preset's own bounce (`.snappy` already has some), so write converted values with
  `.spring(duration:bounce:)`. To convert `.spring(response:dampingFraction:)`: duration equals the
  response; bounce is 1 minus the damping fraction when the damping fraction is 1 or less, and
  1 divided by the damping fraction, minus 1, when it is above 1. Any `blendDuration` is dropped.
- **Stagger**: one step per item for lists that reveal in order. Stagger only the first several items
  (about 8) and show the rest together, so long lists never make people wait and the steps stay big
  enough to read.
- **Haptics**: a role each for selection, a light tap, a firm tap for primary or destructive actions,
  success and error, but only the roles the app has a call site for or the proposal adds one for. Success is for real achievements only, never routine refreshes or
  syncs. One haptic per event, never one per item in a list.
- **Reduce Motion**: one rule for the whole app. In views read
  `@Environment(\.accessibilityReduceMotion)`; in models and other code with no environment, read
  `UIAccessibility.isReduceMotionEnabled` on the main actor. Transitions become `.opacity`. Swapping
  the animation alone does not stop movement: a state-driven `scaleEffect` or `offset` still scales
  or moves, just faster, so hold those values at rest. Layout changes (rows inserted, a list growing)
  always move their neighbours; there, a short `.easeInOut` (about 0.2 s) is the practical rule.
  Meaningful changes still change, they just do not travel. A helper that returns `nil` gives an
  instant change, not a fade: use `nil` only where instant is the deliberate choice (a whole-screen
  move), and a short `.easeInOut` where the rule is a crossfade.

Present it as a table: name, value, what it is for, which current values it replaces, and where the
value comes from (a shot, or the app's own code). Then list every call site that would change,
grouped by file, with the old and new value, and every sleep that must change with it. Ask before
touching them.

## 6. Write the file

When the user agrees, write the values into the app's existing motion file or type if it has one
(from step 2), otherwise a new `Motion.swift`, with short comments saying what each is for, the
haptic roles (through the app's haptics wrapper if it has one, `sensoryFeedback` if not), and small
helpers that apply the Reduce Motion rule.
Compile it before handing it over: build the app if you can, or typecheck the file against the floor
from step 1, adding a small stub file for any app type it uses:

```
xcrun --sdk iphonesimulator swiftc -typecheck -target arm64-apple-ios<floor>-simulator \
  -swift-version <mode> Motion.swift Stub.swift
```

Add the project's isolation and concurrency flags if it sets them. The `-target` floor is what
catches an API that is too new. Then migrate call sites in small batches, file by file, only if the
user asks, moving each coupled sleep to the animation's completion.

Write plainly: short sentences, common words. Never use em dashes or en dashes.

## Not for

Android, Flutter, React Native or web. A single animation: use the `motion-reference` skill. Where
an app should animate at all: use `find-animation-opportunities` first.
