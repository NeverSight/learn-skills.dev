---
name: storyboarding
description: Turns a script into a shot-by-shot storyboard where every image has a reason to exist, ready for filming, animation or AI generation. Use when the user wants a storyboard, shot list, visual plan, scene breakdown, B-roll plan, animatic notes, camera directions, or says visuals feel random, generic, stock-footage-y or like AI slop.
license: MIT
metadata:
  version: "0.1.0"
  status: alpha
  category: production
  pack: creator-skills
---

# Storyboarding

A storyboard decides what the audience sees at every moment and why. Random visuals are the fastest way to make content feel like AI slop: a glowing brain for "thinking", a handshake for "deal", a spinning globe for "world". Every shot here has an intent, and the intent is written down.

Input: a script in production format (from `script-writing`). If you get raw text, split it into lines first, one spoken thought per line.

## The floor

1. **Every shot has a job.** Write it: *show, prove, contrast, reveal, react, breathe, joke, orient*. No job, no shot.
2. **Picture adds, voice doesn't repeat.** If the line says "the tank burst", the picture shows what the words can't: the rivet, the kid, the paint. [C; "say vs. show"]
3. **Specific over symbolic.** A neighbor's jar under a real drip beats a generic "danger" visual.
4. **Ban the stock clichés.** Typing hands, handshakes, glowing brains, spinning globes, lightbulbs, chess pieces, people pointing at screens. Use one only as a deliberate joke.
5. **Motifs carry meaning.** Pick 1–3 visual motifs (an object, a color, a framing) that return and change meaning. The ending should rhyme with the opening.
6. **Pace with the story.** Faster cuts in escalation, a held shot on the turn, silence-and-stillness before the reveal.
7. **Respect the bible.** Palette, framing rules, character designs and motion language from `.creator/bible.md` if it exists.
8. **First frame = hook.** Shot 1 must already be interesting with the sound off.

## Procedure

1. **Read the script and bible.** Note format, aspect ratio, runtime, and every `VISUAL:` the writer already gave.
2. **Pick motifs.** 1–3 objects or images that carry the theme. Decide how each changes by the end.
3. **Pick the color script** (one line per act: e.g., "warm sepia → sickly brown → cold gray"). Hand detail to `color-design` if needed.
4. **Break into shots.** For each spoken line (or each change in a visual-only stretch), one or more shots. Shorts: a new visual idea every ~1–3 seconds [C]. Long-form: slower, but never static without reason.
5. **For each shot, decide:** size, angle, movement, subject, intent, text, sound ([references/shot-grammar.md](references/shot-grammar.md)).
6. **Run the intent check:** read only the Intent column. Does it tell the story? Any shot with a vague intent ("looks cool", "B-roll") gets replaced.
7. **Run the cliché check:** any shot a stock site would return for the keyword? Replace it with the specific version.
8. **Mark generation needs.** For AI-generated shots, note the reference image or character sheet needed for consistency, and hand prompt writing to `visual-prompting`.

## Output: the storyboard table

```markdown
## Storyboard: <title>
Aspect: 9:16 · Runtime: 0:45 · Motifs: brown paint (cover-up → evidence), the jar (curiosity → loss)
Color script: sepia warm (setup) → brown, oppressive (escalation) → near-monochrome (turn)

| # | Time | Line (VO / dialogue) | Shot | Visual | Intent | On-screen text | Sound | Source |
|---|------|----------------------|------|--------|--------|----------------|-------|--------|
| 1 | 0:00–0:02 | "In 1919, a wave of molasses..." | WS, eye level, static | Boston street, 1919. A brown wall enters frame left. | Hook: impossible image | 2.3 MILLION GALLONS | low rumble | gen: image→video |
| 2 | 0:02–0:03 | "...killed twenty-one people." | CU, high angle | A child's shoe in the brown flood | Stakes: make it human | — | rumble cuts | gen: image |
```

Shot column shorthand: size (ECU, CU, MCU, MS, WS, EWS), angle (eye, low, high, top, dutch), movement (static, push, pull, pan, tilt, track, handheld).
Source column: `film`, `archive` (with license), `screen`, `gen: image`, `gen: video`, `gen: image→video`, `motion gfx`.

## Visual-only moments

Leave space for picture without voice: a 0.5–2 second hold after a reveal, before a turn, or on the final image. Mark these rows with `—` in the Line column.

## Voice floor (for text in the table)

Plain, specific descriptions. "A rivet shoots out of the steel" beats "dramatic shot of structural failure". Full rules: the `human-writing` skill.

## References

| File | Read when |
|---|---|
| [references/shot-grammar.md](references/shot-grammar.md) | Choosing shot size, angle, movement, cuts, and what each one means |
| [references/visual-intent.md](references/visual-intent.md) | Motifs, show-don't-tell, avoiding AI-slop visuals, continuity |
