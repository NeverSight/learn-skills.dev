---
name: interface-sound
description: Reviews UI audio so sound confirms, stays optional and never replaces a visual cue.
license: MIT
metadata:
  author: raphael-salaja
  version: "1.0.0"
  source: https://www.userinterface.wiki
---

# Interface sound

This skill reviews whether a sound should play and how the user controls it. It does not design the waveform. Synthesis belongs to `synthesize-sound`.

Every check is a pair. The broken line sits beside the line that replaces it.

Every sound needs a visual twin. Sound on typing, hover or scroll is a finding. A missing mute control is a finding. Taste about a melody is not.

## When to use

Use this when adding, reviewing or removing UI sound. Use `synthesize-sound` when the sound is generated with the Web Audio API and the question is the buffer, the filter or the envelope.

## 1. List the cues

Read the files in scope. List each `play`, `Audio` or synth trigger and the interaction that fires it. If there is no audio, say so and stop.

## 2. Check whether it should play

Each cue has a visible state as well, such as a status attribute or a toast. Sound alone is `a11y-visual-equivalent`. The product exposes a setting that disables sound. That is `a11y-toggle-setting`. If `prefers-reduced-motion: reduce` matches, do not play. That is `a11y-reduced-motion-check`. Volume comes from a preference, not a hardcoded `1`. That is `a11y-volume-control`. The published default is `0.3`, which is `impl-default-subtle`.

Do not play on typing, keyboard navigation, hover or scroll. That is `appropriate-no-high-frequency` and `appropriate-no-decorative`. Sound fits payment, upload and submit confirmations. It also fits errors or warnings that must not be missed. Those are `appropriate-confirmations-only` and `appropriate-errors-warnings`. An error sound is quiet information, not a buzzer. That is `appropriate-no-punishing`.

Match weight to the action. A toggle gets a soft click. A purchase may get a short chime. That is `weight-match-action`. The sound's length matches the action. A `50ms` click for an instant press. Not a `2000ms` whoosh. That is `weight-duration-matches-action`.

## 3. Check playback

Preload files at startup with `audio.load()`. Creating `new Audio` inside the handler is `impl-preload-audio`. Set `currentTime = 0` before `play()` so a second trigger is heard. That is `impl-reset-current-time`.

## 4. Report and stop

Write findings, then the summary. Do not add sound to a surface that does not have it unless the user asked.
## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `a11y-visual-equivalent` | `playSound("success")` and no status change | `setStatus("success")` beside the sound |
| `a11y-toggle-setting` | `<SoundProvider>` with no off switch | `<SoundProvider enabled={soundEnabled}>` |
| `a11y-reduced-motion-check` | `audio.play()` with no media query | Return when `prefers-reduced-motion: reduce` matches |
| `a11y-volume-control` | `audio.volume = 1` | `audio.volume = volume` from a preference |
| `impl-default-subtle` | `const DEFAULT_VOLUME = 1` | `const DEFAULT_VOLUME = 0.3` |
| `appropriate-no-high-frequency` | `playSound("keystroke")` inside `onChange` | No sound on typing |
| `appropriate-no-punishing` | `playSound("loud-buzzer")` on invalid input | A short quiet cue and the visible error |
| `impl-preload-audio` | `new Audio(url)` inside the click handler | Preload once, then replay |
| `impl-reset-current-time` | `audio.play()` on a clip that may already be running | `audio.currentTime = 0` before `play()` |
| `weight-duration-matches-action` | A `2000ms` whoosh on an instant press | A cue near `50ms` |

## Reporting

**Severity.** `HIGH` is sound with no visual equivalent, sound on a high-frequency action, or no way to turn sound off. `MEDIUM` is missing preload, a full default volume, or a cue that ignores reduced motion. `LOW` is a cue whose length is slightly off the action.

**Verification.** Read the declared values in the files in scope. A browser is optional. Mark any check you could not run as `Not verified`.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a summary:

| Rule | Count | Severity |
| --- | --- | --- |

`Block` when any `HIGH` remains. `Approve` otherwise, and leave lesser rows in the table. Never `Approve` a file you did not read. With nothing to report, say "No actionable findings" and list what was not verified.
