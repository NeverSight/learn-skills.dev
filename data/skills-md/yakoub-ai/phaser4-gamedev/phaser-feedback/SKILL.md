---
name: phaser-feedback
description: This skill should be used when the user pastes raw player feedback, playtester notes, bug reports, Discord or Reddit comments, itch.io comments, App Store reviews, QA notes, or a list of complaints about their Phaser game, or asks to "triage this feedback", "fix what players reported", "reproduce this bug report", "act on playtest notes", "turn feedback into tests", "what should I fix first", or "respond to this reviewer". Use it whenever feedback about a running game needs to become reproducible tests, prioritised fixes, and a verified re-release.
version: 0.7.0
---

# Turning Player Feedback Into Shipped Fixes

Feedback arrives as prose written by someone who does not know your code:

> "the jump feels floaty and sometimes i just fall through the platform. also the boss
> is impossible. the shop is broken"

Four statements, four different kinds of problem, and exactly one of them is a bug in
the sense the word usually means. Treating them all the same is how a fix session ends
with the player's actual complaint untouched.

The loop this skill runs:

```
intake ──► triage ──► group by root cause ──► reproduce (failing scenario)
                                                       │
                                    report back ◄── verify ◄── fix
                                          │
                                          └──► scenario is kept as a regression test
```

The step that makes the difference is **reproduce before fix**. A playtest scenario that
fails for the reason the player described is proof you understood them. Without it you
are pattern-matching prose against code, and the most common outcome is a plausible fix
to something nobody complained about.

---

## Step 1 — Intake

Take the feedback **verbatim**. Do not tidy it, translate it into technical language, or
drop the parts that seem vague. The exact words carry information:

- "sometimes" / "occasionally" / "once" → a frequency claim, which changes how you
  reproduce it (see `--repeat` below)
- "after a while" / "later on" → a state-accumulation or leak claim
- "on my phone" / "in fullscreen" → a platform claim; you need device posture
- "it used to work" → a regression claim; find the commit before hunting the bug

Record each item with its source and any context the reporter gave. If several
reporters said the same thing, note the count — frequency is the cheapest priority
signal you will get.

For anything platform-shaped, get the posture before doing anything else: browser and
version, iOS vs Android, Safari tab vs PWA vs Capacitor, orientation, touch vs mouse.
Most "mobile bugs" are specific-platform bugs and are indistinguishable without it.

---

## Step 2 — Triage into four kinds

This is the step that decides whether the session succeeds. Each kind needs a different
response, and misfiling one wastes the whole cycle.

| Kind | The game… | What it needs | Who decides |
|---|---|---|---|
| **Defect** | does something it should not | a failing scenario, then a fix | you |
| **Tuning** | does what the code says, but the numbers feel wrong | a numeric target, then a value change | the user |
| **Design** | does what it was designed to do, and that design is unwanted | a GDD change | the user |
| **Unactionable** | — | a specific question back to the reporter | the reporter |

Applied to the example above:

| Quote | Kind | Why |
|---|---|---|
| "sometimes i just fall through the platform" | **Defect** | Collision is failing. Nobody designed that. |
| "the jump feels floaty" | **Tuning** | Gravity and jump velocity are doing exactly what they are set to. |
| "the boss is impossible" | **Tuning** or **Design** | Ambiguous — an HP number, or the whole fight? Ask. |
| "the shop is broken" | **Unactionable** | Broken how? No route to a repro. |

**Do not invent a metric for a taste question.** Difficulty feel, art readability, audio
mix and "is it fun" cannot be settled by a headless browser. Label them as needing a
human and leave them labelled — a fake numeric target on a taste question produces a
confident change in an arbitrary direction.

**Do not silently upgrade a tuning report into a defect.** "The boss is impossible" fixed
as a defect means hunting a damage-calculation bug that is not there. Fixed as tuning it
means asking "what should the fight take — how many hits, how long?" and changing a
number. The second one is nearly always right, and it needs the user's answer.

Write the triage down before touching code, and show it to the user. Getting a
misclassification corrected costs one sentence; discovering it after the fix costs the
session.

---

## Step 3 — Group by suspected root cause

Separate reports frequently share one cause. Group them before investigating — a single
root cause explains more than a stack of individual patches, and grouped symptoms point
at it much faster than any one symptom does.

```
"sometimes i fall through the platform"
"the moving platform drops me at the top"      ──► one suspect:
"i clipped into the wall when i dashed"             high velocity vs. collision step
```

Three tickets, likely one fix: a body moving far enough per frame to tunnel through a
thin collider. If you patch them separately you will write three special cases and the
fourth report will arrive next week.

Reports that resist grouping are their own group. Do not force it.

---

## Step 4 — Reproduce as a failing scenario

**Write the scenario before the fix. Watch it fail. Keep it forever.**

The scenario is where the player's prose becomes something the machine can check. The
translation is mechanical once you know the vocabulary — see
`references/feedback-to-scenario.md` for the full mapping.

```javascript
// playtest/repro-fall-through-platform.mjs
export default [
  { name: 'set up the reported situation', action: 'eval', code: `
      const s = scene('GameScene');
      s.player.setPosition(400, 100);      // above the platform
      s.player.body.setVelocityY(1200);    // the reporter was falling fast
  ` },
  { name: 'player lands on the platform, does not pass through',
    action: 'waitFor',
    expression: `scene('GameScene').player.body.blocked.down`,
    timeout: 3000 },
  { name: 'and is still above it',
    action: 'expect',
    expect: { expression: `scene('GameScene').player.y`, below: 500 } },
];
```

Run it:

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/phaser-playtest/scripts/playtest.mjs" \
  --project . --scenario playtest/repro-fall-through-platform.mjs
```

**It must fail.** A repro that passes on the first run has not reproduced anything, and
the fix you write next will be aimed at nothing. When that happens, the scenario is
wrong, not the report — go back and get more detail.

### "Sometimes" is a frequency claim, and it has its own tool

```bash
node ".../playtest.mjs" --project . --scenario playtest/repro.mjs --repeat 10
```

The verdict tells you what kind of bug you have:

| Verdict | Diagnosis |
|---|---|
| `10/10 runs clean` | Not reproduced. Your scenario is missing something the player did. |
| `INTERMITTENT — failed in 3/10` | Real, and race- or RNG-shaped. |
| `failed in all 10 — consistent` | Not a flake at all. Your repro is exact; fix it directly. |

For an intermittent result, add `--seed 42`. If it becomes consistent, the bug depends
on an RNG path — a spawn roll or loot roll reaching a state the code does not handle. If
it stays intermittent under a seed, the cause is timing: frame ordering, an async load,
or an event racing `update()`. Those two need different fixes, and this is the cheapest
way to tell them apart.

### Matching the claim to the assertion

| The reporter said | Assert with |
|---|---|
| "it happens sometimes" | `--repeat 10` |
| "enemies get stuck" | `sample` + `expect: { stat: 'range', atLeast: n }` |
| "the camera jitters" | `sample` + `expect: { stat: 'stddev', atMost: n }` |
| "it takes forever to kill" | `waitFor` with a `timeout` |
| "my health drops for no reason" | `sample` + `expect: { stat: 'delta', equals: 0 }` |
| "it slows down after a while" | `--heap`, plus a `repeat` block that restarts the scene |
| "it only breaks on my phone" | `--device iphone` / `--device android` |
| "the controls fight me" | `hold` with several keys — diagonals are their own input path |
| "it broke after the update" | Check out the previous commit and run the same scenario |

---

## Step 5 — Fix

Standard discipline applies, and it applies *harder* here because you are working from a
second-hand description:

1. **Investigate first.** Read the source. Explain what is causing it, why it happens,
   and what you propose — before writing the fix.
2. **Two attempts, then pivot.** If two attempts at an approach fail, stop and propose
   two or three genuinely different approaches. Do not iterate a third time on an
   approach that has failed twice.
3. **Fix the cause you grouped, not each symptom.** If three reports shared a root
   cause, one fix should close all three. If it closes only one, your grouping was
   wrong — say so and re-group rather than patching the other two separately.

---

## Step 6 — Verify

Two things must be true, and both must be checked:

```bash
# 1. The repro now passes — and for an intermittent bug, passes repeatedly.
node ".../playtest.mjs" --project . --scenario playtest/repro-fall-through-platform.mjs --repeat 10

# 2. Nothing else broke.
npx tsc --noEmit
node ".../playtest.mjs" --project . --mode build
for f in playtest/*.mjs; do node ".../playtest.mjs" --project . --scenario "$f"; done
```

For a bug that was intermittent, a single green run is not verification — it is the same
coin flip that made the bug hard to find. Re-run it at least as many times as it took to
reproduce.

**Report the result faithfully.** If the repro passes but two other scenarios now fail,
say that. A fix that trades one bug for two is not done.

---

## Step 7 — Report back, and keep the scenario

Write the response in the reporter's language, not yours. They described an experience;
tell them what changed about that experience:

> **"sometimes i just fall through the platform"** — Fixed. Falling fast enough could
> carry you through a thin platform between physics steps. Fast falls now land properly.
>
> **"the jump feels floaty"** — Changed: you now reach the top of a jump in 0.35s
> instead of 0.6s. Worth telling me whether that is what you meant.
>
> **"the boss is impossible"** — Not changed yet. How long should the fight take, or how
> many attempts felt fair? I can move its health, its damage, or its attack rate.
>
> **"the shop is broken"** — I could not reproduce this. What did you click, and what
> happened instead?

Three things earn their place in that reply: what you fixed, what you changed and want
checked, and what you still need from them. A reply that only lists fixes loses the two
items that need the reporter.

**Commit the scenario.** `playtest/repro-*.mjs` is now a permanent regression test. This
is what makes feedback compound: every report fixed this way leaves behind a check that
stops it returning. Six months of reports become a suite that encodes what real players
actually did to your game — which no amount of unit testing produces.

---

## Anti-patterns

- **Fixing before reproducing.** The most expensive mistake here. You are working from a
  stranger's description of your own code; the odds that your first reading is right are
  not good, and a passing repro is the only cheap way to find out.
- **Sanitising the report.** "Feels floaty" rewritten as "adjust gravity" throws away the
  fact that you do not yet know what they wanted.
- **Treating a taste question as a metric.** Assign a number to "is the boss fun" and you
  will confidently change something in a direction nobody asked for.
- **Fixing one report at a time when they share a cause.** Produces special cases, and
  the underlying bug keeps generating new tickets.
- **A single green run on an intermittent bug.** That is the coin flip that hid the bug
  in the first place.
- **Deleting the repro after the fix.** Throwing away the one artifact that stops it
  coming back.
- **Silence on the items you did not fix.** The reporter cannot tell "I decided not to"
  apart from "I ignored you", and the second one costs you the next report.

---

## Additional Resources

### Reference Files
- **`references/triage-guide.md`** — The four kinds in depth, with real feedback strings
  worked through, ambiguous cases, and how to prioritise once classified.
- **`references/feedback-to-scenario.md`** — The full translation table from feedback
  phrasing to scenario constructs, with complete worked scenarios for the common
  complaint shapes.
- **`references/response-templates.md`** — Replying to reporters, writing player-facing
  changelogs, and closing the loop so the next report is better than this one.

### Examples
- **`examples/worked-session.md`** — One messy Discord paste taken end to end: triage,
  grouping, three repro scenarios, the fixes, verification, and the reply sent back.

### Related
- `skills/phaser-playtest/` — the harness, the full scenario reference, and the
  instrumentation a game needs before any of this works
- `skills/phaser-debugger/` — root-cause investigation once a repro exists
- `skills/phaser-gdd/` — where design-kind feedback goes: Section 13 acceptance criteria
- `skills/phaser-analyze/` — for performance reports, before assuming a leak
