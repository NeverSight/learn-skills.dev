---
name: script-writing
description: Turns a story or idea into a spoken script ready to record, with visual and sound cues in a production format other skills can read. Use when the user asks for a script, voiceover, narration, talking-head script, YouTube or Shorts script, ad script, skit, dialogue, or animation script, or wants an existing script tightened, timed, or made easier to say.
license: MIT
metadata:
  version: "0.1.0"
  status: beta
  category: writing
  pack: creator-skills
---

# Script Writing

A script is a plan for sound and picture, not an essay. Every line is something a person says, a thing we see, or a sound we hear, and every line earns its seconds.

Input: a beat sheet (from `story-craft`) and a hook (from `hook-craft`). If you only have an idea, make a quick beat sheet first: premise, 3–7 beats, the turn, the ending.

## The floor

1. **Write for the ear.** One breath per line. Strongest word last. Contractions. No parentheses.
2. **Every line adds something new.** A fact, a turn, an image, a laugh. If a line restates the previous one, cut it.
3. **Don't narrate what we see.** If the shot shows the tank bursting, the voice says something the picture can't: the sound, the number, the cost.
4. **Fit the runtime.** Count words. ~150 wpm conversational, ~170–180 wpm punchy Shorts, ~130 wpm calm documentary [C].
5. **Keep a loop open at every moment.** Close one question only after the next one is open.
6. **End when the story ends.** No recap. Calls to action are short and come after the payoff.
7. **Facts are checkable.** Real events, people and numbers: list sources under the script. Never invent quotes.
8. **Voice per profile.** Read `.creator/profile.md` and `.creator/taste.md`. Profanity, energy, humor as set there.

## Procedure

1. **Lock the inputs.** Premise, format, runtime, platform, the hook, the ending line. Calculate the word budget: runtime (s) ÷ 60 × wpm.
2. **Draft fast, long.** Write every beat in spoken words. Don't polish. Go 20–30% over budget.
3. **Mark the picture.** Add `VISUAL:` lines where the picture changes or carries meaning. Add `ON-SCREEN:` for text, `SFX:` and `MUSIC:` where sound does a job.
4. **Cut to budget.** Kill restatements first, then setup, then the weakest beat. Never cut the turn or the payoff.
5. **Retention pass** ([references/retention.md](references/retention.md)): loops mapped, re-hooks placed, no stretch over ~20 seconds without a new piece of information.
6. **Voice pass:** run the `human-writing` edit procedure. Then `python3 <human-writing>/scripts/slop_check.py --spoken script.md` if that skill is installed.
7. **Read-aloud pass.** Say every line. Rewrite anything you stumble on.
8. **Time it.** Word count per section → timestamps in the scene headers.

## Output: production format

The full spec is [references/production-format.md](references/production-format.md). Short version:

```markdown
# <Title>
Format: Short · 45 s · 9:16 · ~130 words · profanity 1 · energy punchy

## 1 · HOOK (0:00–0:03)
VO: In 1919, a wave of molasses killed twenty-one people.
VISUAL: Black-and-white street, 1919. Brown wave enters frame left.
ON-SCREEN: 2.3 MILLION GALLONS

## 2 · SETUP (0:03–0:12)
VO: ...

---
Sources: <links>
Word count: 128 · Est. runtime: 0:44 at 175 wpm
```

`storyboarding` and `voice-direction` read this format directly. Keep the tags exact.

## Formats

| Format | Notes |
|---|---|
| Voiceover narrative | VO carries story; visuals add proof and texture. Most of this skill's defaults. |
| Talking head | Write for one person to camera. Shorter lines. Mark `CUT:` for jump cuts and `B-ROLL:` inserts. |
| Short (≤ 60 s) | One turn. No intros. Last line can loop into the first. |
| Long-form YouTube | Chapters as mini-stories. Re-hook at each boundary. Sponsor reads after the hook lands. |
| Skit / dialogue | `NAME:` lines. People interrupt, dodge, and talk past each other. One line, one intention. |
| Animation | `ACTION:` lines describe what moves. Dialogue sparse. Every beat must be visible. |
| Ad | Problem in the first two seconds, product at the turn, changed state at the end. |

More: [references/retention.md](references/retention.md) covers pacing and timing tables per format.

## Voice floor

Plain words. Payload first. Name concrete things. Say it once. Mix the rhythm. No moral at the end. Profanity per profile. Full rules: the `human-writing` skill.

## References

| File | Read when |
|---|---|
| [references/production-format.md](references/production-format.md) | Writing or parsing the script format; tags; timing math |
| [references/retention.md](references/retention.md) | Pacing, re-hooks, word budgets, where viewers leave and why |
