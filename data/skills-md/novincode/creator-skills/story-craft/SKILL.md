---
name: story-craft
description: Builds the story underneath any piece of content, as a beat sheet where every beat changes something. Use when the user wants a story, a plot, a narrative, an outline, a structure for a video, short, film, animation, ad or documentary, when content feels flat, random, boring or like a list of facts, or when they ask why a story isn't working.
license: MIT
metadata:
  version: "0.1.0"
  status: beta
  category: writing
  pack: creator-skills
---

# Story Craft

A story is someone who wants something, something in the way, and a change. Without the change you have a list of events. Your job is to find the change and build every beat so it pushes toward it.

You hand off a **beat sheet**, not prose. `hook-craft` writes the opening, `script-writing` writes the words.

## The floor

1. **Somebody wants something.** A person, a company, a city, the viewer. If nobody wants anything, nothing is at stake.
2. **Every beat turns.** Something is different at the end of each beat than at the start: better or worse, known or unknown. A beat that turns nothing gets cut [C; McKee's "value shift"].
3. **But / therefore, never "and then".** Beats connect by cause and conflict. "And then" is a list. [C; Parker & Stone]
4. **Stakes are specific and personal.** "Everything was at risk" is nothing. "Her kid was on that street" is something.
5. **Start late, leave early.** Enter each scene as close to the turn as you can. Leave the moment it lands.
6. **The ending is surprising and inevitable.** Unexpected in the moment, obvious in hindsight because you planted it.
7. **Show the meaning, don't state it.** No closing moral. The last image does the work.
8. **Never invent facts about real people or events.** Fiction is fine when it's labeled. If the user needs a personal story, ask for the real moment; don't make one up.

## Procedure

1. **Find the premise.** One sentence: *[who] wants [what], but [obstacle], so [action], and [change].* If you can't fill it, you don't have a story yet. Ask, or offer three candidate premises.
2. **Find the five-second moment.** The instant where something changes in someone. Everything else exists to set it up and pay it off [C; Matthew Dicks, *Storyworthy*].
3. **Pick the structure for the format** ([references/formats.md](references/formats.md)). Short = one turn. Long-form = nested turns. Film = acts. Don't force a 15-beat film structure onto a 40-second Short.
4. **Draft the beats.** One line each: what happens, what turns, what the audience now wants to know.
5. **Run the but/therefore pass.** Read the beats joined by "but" or "therefore". Any join that only works with "and then" is a dead beat. Fix or cut.
6. **Check the open questions.** At every beat, there should be at least one question the viewer wants answered. Map where each opens and closes ([references/psychology.md](references/psychology.md)).
7. **Test the ending.** Does it pay off the opening question? Is it planted earlier? Could you cut the last line and lose nothing? Then cut it.
8. **Diagnose if stuck** with [references/diagnostics.md](references/diagnostics.md): symptom → cause → fix.

## Output: the beat sheet

```markdown
## Beat sheet: <title>
Premise: <who wants what, but, so, change>
Format: <Short 45s | YouTube 12m | short film 5m | ...>   Structure: <name>
Five-second moment: <the instant of change>
Open question at start: <what the viewer wants to know>

| # | Beat | Turn (from → to) | Question opened / closed | Est. time |
|---|------|-------------------|--------------------------|-----------|
| 1 | ...  | safe → threatened | opens: will it hold?     | 0:00–0:05 |

Ending: <final image or line> — planted at beat <n>
```

Keep beats to one line. If a beat needs a paragraph, it's two beats.

## Choosing a structure (quick map)

| Format | Default structure | Why |
|---|---|---|
| Short (15–60 s) | Hook → one turn → button | Room for exactly one change |
| Explainer / essay | ABT (And, But, Therefore) | Turns information into a problem and an answer |
| YouTube long-form | Mystery chain: question → investigation → reveals that open bigger questions | Keeps loops open for minutes |
| Personal story | Storyworthy: start opposite the ending, build to the five-second moment | Change in a person is the payload |
| Short animation, no dialogue | Story Spine or Kishōtenketsu | Simple, visual, twist-friendly |
| Feature or episodic | Story Circle or a beat sheet | Character change across acts |

All frameworks with when-to-use and traps: [references/frameworks.md](references/frameworks.md).

## Voice floor (for any prose you write here)

Plain words. Payload first. Name concrete things. Say it once. No moral at the end. Profanity per `.creator/profile.md`. Full rules: the `human-writing` skill.

## References

| File | Read when |
|---|---|
| [references/frameworks.md](references/frameworks.md) | Choosing or explaining a structure |
| [references/formats.md](references/formats.md) | Building beats for a specific format and length |
| [references/psychology.md](references/psychology.md) | Why stories hold attention; open loops; graded evidence |
| [references/diagnostics.md](references/diagnostics.md) | A story isn't working and you need to know why |
