---
name: motion-design
description: Designs motion that means something, covering timing, easing, kinetic typography, transitions and animation direction, and turns it into specs for editors, animation tools, code (Remotion, Lottie, CSS) or AI video prompts. Use when the user wants animation, motion graphics, kinetic type, animated captions, transitions, easing, timing, an explainer animation style, a motion language for a brand or channel, or says motion feels janky, floaty, cheap or random.
license: MIT
metadata:
  version: "0.1.0"
  status: alpha
  category: production
  pack: creator-skills
---

# Motion Design

Motion is meaning over time. Good motion tells the eye where to look, in what order, and how to feel about it. Bad motion is everything moving because it can.

## The floor

1. **Every move has a reason:** direct attention, show a relationship, show cause and effect, show change of state, or add personality. If it does none, it stays still.
2. **Ease everything.** Nothing in the real world starts or stops instantly. Linear motion reads as mechanical (use it only on purpose) [C; classic animation principle "slow in, slow out"].
3. **Enter with ease-out, exit with ease-in, move across with ease-in-out** [C].
4. **Hierarchy through order.** The most important element moves first. Supporting elements follow with a small stagger.
5. **Restraint.** One hero move per moment. If three things bounce at once, none of them matter.
6. **Time to the sound.** Hits on beats, text on words, cuts on the music. Off-beat motion feels wrong even when nobody can say why.
7. **Readable text holds still long enough to read.** Rough floor: about 3–4 words per second of hold time, plus a beat [C].
8. **Lock the language in the bible.** Curves, durations, transition types, signature move. Consistency across videos is what makes a channel feel designed.

## The animation principles that matter most for motion graphics

From Disney's 12 principles (Thomas & Johnston, *The Illusion of Life*), the ones that carry over to graphics [C]:

| Principle | In motion graphics |
|---|---|
| Timing | Duration defines weight. Heavy = slower. Light = faster. |
| Slow in / slow out | Easing curves |
| Anticipation | A small pull back before a big move (scale down 5% before popping up) |
| Follow-through & overlap | Parts settle at different times; a card lands, its shadow settles after |
| Arcs | Organic things move on curves, not straight lines |
| Squash & stretch | Elastic energy on impact; subtle or it gets cartoonish |
| Staging | One clear focal point per moment |
| Exaggeration | Push key poses slightly beyond real |
| Secondary action | Small supporting motion (a tag wiggles after the label lands) |

## Durations [C, starting points]

| Move | Duration |
|---|---|
| Micro feedback (a highlight, a tick) | 100–200 ms |
| Element enter/exit | 250–500 ms |
| Large move / scene transition | 400–800 ms |
| Stagger between siblings | 30–80 ms |
| Hold on readable text | ≥ 1 s for 3–4 words |

At 30 fps, 1 frame ≈ 33 ms; at 24 fps ≈ 42 ms. Think in frames for precision.

## Easing reference

| Feel | Curve (cubic-bezier) |
|---|---|
| Standard (in-out) | `0.4, 0, 0.2, 1` |
| Enter (decelerate) | `0, 0, 0.2, 1` |
| Exit (accelerate) | `0.4, 0, 1, 1` |
| Snappy / energetic | `0.2, 0.9, 0.1, 1` |
| Overshoot (playful) | spring, or `0.34, 1.56, 0.64, 1` |

Springs (stiffness/damping) feel more physical than bezier curves for UI-like motion; use them when the tool supports it.

## Kinetic typography

- One idea per card. Break lines where the voice breathes.
- Emphasize the one word that matters: scale, weight, color, or a hit. Not every word.
- Text in sync with the VO, landing on the stressed syllable.
- Keep text in the safe area: away from platform UI at the bottom and right on vertical video [C].
- Animated captions: limited palette, consistent position, highlight the current word if the style uses it.

## Procedure

1. Read the script and storyboard. Mark every moment where motion carries meaning (a reveal, a list, a number, a change).
2. Define the motion language for the piece (or load it from the bible): curves, durations, transition types, signature move.
3. For each marked moment, write a motion spec (below).
4. Map the specs to the target: an editor (keyframe notes), code (Remotion/CSS/Lottie values), or an AI video prompt (`visual-prompting`).

## Output: motion spec

```markdown
## Motion spec: <title>
Language: enter 350ms ease-out (0,0,0.2,1) · exit 250ms ease-in · stagger 50ms · signature: slide-up + 3% overshoot · transitions: hard cuts, one whip-pan per video max

| # | Time | Element | Move | Duration | Easing | Sync to | Why |
|---|------|---------|------|----------|--------|---------|-----|
| 1 | 0:00.0 | "2.3 MILLION GALLONS" | scale 90%→100%, fade in | 300ms | ease-out | VO "molasses" | land the number |
```

## Voice floor

Specs in plain words with real values. "Slides up 40px over 350ms, ease-out" beats "smooth, dynamic entrance". Full rules: the `human-writing` skill.
