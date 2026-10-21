---
name: game-dev-combat-animation
description: Build, fix and review character combat animations (melee strikes, bow shots, spell casts, skills, monster attacks, whole move sets) so they read like Diablo IV, Baldur's Gate 3 or Elden Ring and never stretch, lock, wring or break an arm, wrist or hand. A written standard with numbered rules, per-frame tests on the real skinned mesh, keys designed from upper-arm, forearm and blade intents, checks from every camera the player sees, two blind critics plus a blind A/B against the last release, and every critic claim verified against full-resolution frames and live-rig numbers. Use when creating or reworking any attack, skill or move set; when the user says arms, hands, wrists, elbows or weapons look stretched, weird, broken or wrong; when they ask for a standard, rules or tests for animations; or when they ask to score animations or get them to N out of 10.
---

# Game dev: combat animation

Distilled from the Thornvigil knight-and-archer pass (2026-09-30 to 10-01, releases 1.0.71 and 1.0.72). Its outcome:
- Arms and hands won 5 of 8 blind A/B comparisons against the previous release.
- The archer's broken anchor and the knight's frozen, straight-armed follow-through were fixed.
- Seven rounds of fixes came from traps that numbers would have caught earlier. Those traps are listed below.

Read `references/thornvigil.md` for the project's files, commands and current state, and `references/traps.md` before changing keys.

## The loop

1. **Write the standard before touching keys.** Extend `docs/combat-animation-standard.md` (or the project's equivalent) with the move's own numbered rules:
   - Phases on the game's clock: anticipation, the contact or release on the rule's frame, recovery.
   - Body mechanics, weapon path, camera reads.
   - Mark each rule **test** (measured) or reviewed (scored from frames).
   - Ground every rule in a real reference: a Tripo Studio motion-capture preset for body mechanics, or coached technique such as the archery shot cycle. Use Tripo presets only; the user has no Mixamo account and declined Quaternius.
2. **Baseline first.** Capture both surfaces (the Characters page and in play), keep the frames, and get blind scores before changing anything.
3. **Design keys from anatomy, not from hand positions.** For each key pick the upper-arm direction `u`, the forearm direction `f` and the blade `b`, then run `keydesign.mjs`. It returns the hand target and flags:
   - raise over 100°;
   - flex outside 12–140°;
   - a blade outside 25–115° off the forearm.
   Hand keys ride the shoulder; blade and elbow keys are world directions. See `references/techniques.md`.
4. **Measure before looking.** Bake, then:
   - `armcheck.mjs` for joint ranges and the skin's stretch and crush per arm region on the real mesh;
   - `at.mjs` for the fist and blade at given times;
   - the move's own probe: `knight-measure.mjs`, `anchor.mjs` or `drawfit.mjs`.
   Fix numbers that break a rule before spending a capture.
5. **Test.** Run the arm-ranges test and the move's tests. When you add a test for a bug, temporarily restore the bug and prove the test fails; a test that reads the same wrong convention as the code passes forever.
6. **Capture both cameras and look yourself at full resolution.** A pose that reads well from the front can read broken from the game camera, and the reverse. Diff each capture against the previous round to be sure it is new.
7. **Judge.** Use two blind critics with a fixed rubric (5 criteria × 0–2; the lower score counts) and a blind A/B against the last release with identical sheet titles. Then **verify every claim** against full-resolution frames and live-rig numbers before acting on it. See `references/review.md` and `templates/`.
8. **Ship** by the project's rules: tests, build, changelog with real screenshots, push, sizes, publish. Use the `workflow-ship-change` skill. If a pushed but unpublished release regresses, correct it in place with a follow-up commit; don't add a version for something players never saw.
9. **Show it.** When asked for videos, capture at 30 fps on the move's own clock, place the Characters page and in-play views side by side, and play real speed then quarter speed (`vidcompose.py` + `encode.swift`).

## The arm and hand rules

The rig has no twist or corrective bones; past these ranges the skin visibly wrings, crushes or stretches. Every frame of every strike stays inside them, on both bodies, measured on the real skinned mesh.

| Rule | Limit |
|---|---|
| Elbow flexion | 10–152°; the striking or drawing arm keeps ≥20° through the middle 80% of the move |
| Contact reach | sword hand ≥60% of arm length from the shoulder at contact (reach into the blow, never lock) |
| Wrist | bend ≤50°, roll ≤45°; sword wrist capped at 40°; a drawing hand held straight |
| Twist | forearm roll ≤52°, upper-arm roll ≤52° |
| Raise | ≤105° from hanging (shoulder skin crushes beyond); no overhead raises |
| Skin | the worst 1% of each arm or hand region's edges: stretch ≤2×, crush ≤3× against the bind |
| Hands | always in a pose: fist on a grip, hook on a string (set → loose → follow-through), relaxed when empty; never splayed or clawed |
| Paths | hands ride their shoulders and arc about them between keys; blade keys stay reachable (25–115° off the forearm) |

Full rules, with the reasons and the tests that enforce them, are in `references/rules.md`.

## Techniques that worked

- **Shoulder-relative hands with arc interpolation.** A fixed hand target that the lunging trunk drives the shoulder into crushes the arm, and a straight-line lerp folds the elbow shut mid-way.
- **Aim the forearm, not the wrist.** With the wrist capped, the blade lands on the cone the forearm roll allows. To change the blade, change `f`.
- **Read blade keys in world space.** With the trunk wound back about 70°, "over the sword shoulder" points across behind the head. Tilt the chamber tip-up so it reads as a diagonal.
- **Keep the follow-through moving.**
  - Quick cut: carry the hand down past the shield-side hip on a bent elbow, with the blade still on the line.
  - Heavy cut: sink across, then rebound with the elbow folding.
  - Never hold an arm out at the foe with the blade hanging.
- **Bow draw.** Anchor under the jaw beside the chin, where the hand stays in sight from both cameras. The draw elbow rides 6–8 cm under the arrow. Turn the hips side-on, which fixed draw-shoulder crush better than shrug or elbow poles. Hold the hook through the loose, then send the hand out past the shoulder rather than round the head.
- **Kinetic chain.** Hips lead the chest, and the chest leads the arm. A bow's recoil answers the loose and never leads it.

## Traps that each cost a round

`references/traps.md` has symptom → cause → fix for each. The short list:
- **Bone axes.** The HumGen `head` bone is +Y forward and +Z down. Check any bone-local offset against mesh landmarks (`face.mjs`).
- **Masked failures.** The first failing assertion hides every later move in the same test loop, and the first failing gender hides the other.
- **Camera reads.**
  - A hand by the neck reads as "behind the head" from the game camera.
  - A blade pointing at the camera reads as "hanging".
  - An elbow bent in the view plane reads as straight.
- **Critic misreads.** Thumbnails mislead critics. Check full-resolution frames and the live rig before changing anything.
- **Capture traps.**
  - Never edit `src` while a capture runs.
  - After `location.reload()`, wait before evaluating the next script.
  - Hand-stepped frames are not FPS measurements.

## Report

Lead with what changed in the moves and whether it is live. Then give:
- a scores table: before → after, lower of the two critics, per surface;
- the A/B result;
- the faults still open, named by frame;
- the tests added;
- file and push sizes.

Say plainly when a score sits short of the target and why.
