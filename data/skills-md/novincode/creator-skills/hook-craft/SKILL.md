---
name: hook-craft
description: Writes the opening seconds of a video or post, the part that decides whether anyone stays, plus the re-hooks that keep them. Use when the user asks for a hook, intro, opener, cold open, first line, first three seconds, scroll-stopper, or re-hook, or when viewers drop off at the start, retention dies early, or an intro feels slow, generic or clickbaity.
license: MIT
metadata:
  version: "0.1.0"
  status: beta
  category: writing
  pack: creator-skills
---

# Hook Craft

A hook has one job: make a stranger need the next sentence. It does that by opening a question the viewer wants answered, fast, with something specific enough to believe.

A hook is a promise. The video must keep it. A hook that lies gets the click and loses the viewer, and platforms measure the loss.

## The floor

1. **The first line carries the hook.** No greeting, no channel name, no "in this video".
2. **Specific noun in the first sentence.** "A wave of molasses" stops people. "A strange disaster" doesn't.
3. **Open a loop you can name.** Write down the question the hook makes the viewer ask. If you can't write it, there's no hook.
4. **Give enough context to feel the gap.** Curiosity needs a little knowledge. A hook with zero context is noise. [A; Loewenstein]
5. **Match the packaging.** On YouTube the hook confirms what the title and thumbnail promised, immediately. On Shorts the hook *is* the packaging.
6. **Say, show and write the same thing.** The spoken line, the first frame and the on-screen text all point at the same question, through different channels. [C]
7. **One breath.** If you can't say it in one breath, cut it.
8. **Pay it off.** Mark where in the script the hook's question gets answered.

## Procedure

1. **Read the package and beat sheet.** What's the promise? What's the most surprising true thing in the story? What's at stake?
2. **Write the question first.** The single question the viewer should be asking at second three.
3. **Generate at least 15 hooks across at least 5 archetypes** ([references/archetypes.md](references/archetypes.md)). Volume first. The first three you write are what every other creator would write.
4. **Score each one** 1–5 on:
   - **Clarity:** understood in one listen?
   - **Curiosity:** does it open a gap you need closed?
   - **Stakes:** does someone stand to lose or gain something?
   - **Truth:** does the video fully pay this off?
   Any hook with Truth below 4 is out, whatever else it scores.
5. **Build the top 3 as full openings** for the format ([references/openings-by-format.md](references/openings-by-format.md)): spoken line + first frame + on-screen text + what happens in the next 5–15 seconds.
6. **Plan the re-hooks** for anything over 60 seconds: where each new question opens before the last one closes.
7. **Run the voice floor and `slop_check`.** Hooks attract machine tells more than anything else ("Ever wondered...", "What if I told you...").

## Output

```markdown
## Hook set: <title>
Question the viewer should be asking at 0:03: <question>
Paid off at: <beat / timestamp>

### 1. <archetype> (C5 Q5 S4 T5)
SAY: <spoken first line(s)>
SHOW: <first frame / first 2 seconds of visuals>
TEXT: <on-screen text, ≤ 6 words>
NEXT: <what the next 5–15 seconds do to keep the loop open>

### 2. ...
### 3. ...

Re-hooks: <timestamp → new question>, ...
Rejected (and why): <one line each for the best of the rest>
```

## What kills hooks

<!-- slop:off -->
- **Throat-clearing:** "So today I want to talk about...", "Hey guys, welcome back."
- **The fake question:** "Have you ever wondered why...?" Nobody had. State the weird fact.
- **"What if I told you"**, "You won't believe", "This will blow your mind": cliches that read as bait.
- **Context before hook:** three sentences of background, then the interesting part.
- **The vague tease:** "This changed everything." What did? How?
- **The roadmap:** "First we'll cover X, then Y, then Z." It closes loops before opening them.
- **Bait and switch:** promising something the video doesn't deliver.
<!-- slop:on -->

## Voice floor

Plain words. Payload first. Name concrete things. Say it once. Profanity per `.creator/profile.md`; check the platform note in `human-writing` before swearing in the first seconds. Full rules: the `human-writing` skill.

## References

| File | Read when |
|---|---|
| [references/archetypes.md](references/archetypes.md) | Generating hooks: 14 archetypes, the psychology behind each, templates, original examples |
| [references/openings-by-format.md](references/openings-by-format.md) | Building the full first 3/15/30 seconds for Shorts, long-form, film, ads; re-hook timing |
