---
name: human-writing
description: Makes scripts, captions, posts and narration sound like a real person talking instead of an AI. Use when writing or editing any words meant for an audience, when text sounds like AI, robotic, corporate, fluffy, preachy, repetitive or too safe, or when the user asks to humanize, punch up, simplify, tighten, de-slop, or add swearing and attitude.
license: MIT
metadata:
  version: "0.1.0"
  status: beta
  category: writing
  pack: creator-skills
---

# Human Writing

The job: words a real person would say out loud, to one other person, about something that matters to them. Plain words. Concrete things. No padding. If a line wouldn't survive being said across a table to a friend, it doesn't survive the edit.

This skill is the house voice for the whole pack. Every other writing skill carries its floor.

## The floor (every time, no exceptions)

1. **Payload first.** The first sentence carries the point. No warm-up, no "in this video", no scene-setting nobody asked for.
2. **Name things.** "A fifty-foot steel tank" beats "a large structure". Numbers, names, places, objects, prices, times.
3. **Small words.** use, not utilize. help, not facilitate. start, not commence. show, not showcase. <!-- slop:ignore -->
4. **Say it once.** If a sentence repeats the meaning of the one before it, kill one of them.
5. **Mix the rhythm.** Short punch. Then a longer line that rolls forward and carries some weight before it lands. Then short again.
6. **No hedging, no moral at the end.** Commit to the claim. Trust the audience to get the point.
7. **Write speech, not prose** (for anything spoken): contractions, fragments, sentences that start with And or But.
8. **Swear like a person, at the level the profile allows.** On a beat that earns it. Never as filler.

## Dials

Read them from `.creator/profile.md` (and `.creator/taste.md`, which wins). Defaults in brackets.

| Dial | Range | Default |
|---|---|---|
| `profanity` | 0 clean · 1 mild · 2 strong · 3 unfiltered | 1 |
| `energy` | calm · conversational · punchy · unhinged | punchy |
| `humor` | none · dry · playful · comedic | dry |
| `formality` | street · casual · neutral · formal | casual |
| `reading_grade` | 3–12 | 6 |

Full definitions, the same line at every level, and platform notes on profanity: [references/dials.md](references/dials.md).

**Profanity, short version.** Swear at things and about things: surprise, anger, disbelief, emphasis on a fact that deserves it. One well-placed "fuck" hits harder than five. Slurs and punching down are lazy, so they're out at every level. Check the platform note in `dials.md` before putting strong words in a title, thumbnail or the opening seconds.

## The tells to kill

The full catalog with replacements is in [references/ai-tells.md](references/ai-tells.md); the machine-readable list is [assets/kill-list.txt](assets/kill-list.txt). The ones that show up most:

<!-- slop:off -->

- **Inflated words:** delve, tapestry, testament, realm, landscape, navigate, unlock, elevate, seamless, robust, leverage, pivotal, crucial, vibrant, resonate, foster, embark, journey (when nobody travels).
- **Negative parallelism:** "It's not X, it's Y." "Not just X, but Y." State Y.
- **Fake suspense:** "Here's the thing." "But here's the kicker." "The result? Chaos." Once in a script is a choice; three times is a tic.
- **Rule-of-three stacks:** "fast, cheap, and reliable" in every paragraph.
- **Mic-drop endings** on every paragraph, and a moral at the end ("It's a reminder that...").
- **Openers that delay:** "Imagine a world where", "Let's dive in", "Ever wondered".
- **Uniform sentences:** every line 12–18 words. Humans are lumpy.
- **Named emotions instead of shown ones:** "She felt a wave of fear" → what did her hands do?

<!-- slop:on -->

## Procedure: the edit pass

Run in this order. Each pass is one job.

1. **Payload.** Write the single sentence this piece exists to say. Is it in the first two lines? If not, move it there.
2. **Cut.** Remove 20–30%. Delete every sentence the piece survives without. Then every word.
3. **Concrete.** Replace every abstraction with something you can see, count, or hear.
4. **Rhythm.** Look at sentence lengths. If they're all similar, split some and merge others. Put the strongest word at the end of the sentence.
5. **Scrub.** Run the checker (below). Fix every flag, or keep it on purpose and know why.
6. **Read aloud.** Where you'd stumble, run out of breath, or feel like a news anchor, rewrite it the way you'd actually say it.
7. **Ending.** Stop on the last thing that matters: an image, a line, a callback. Not a summary.

## The checker

```bash
python3 scripts/slop_check.py draft.md            # report
python3 scripts/slop_check.py --spoken script.md  # only spoken lines (VO:, NAME:) of a production script
cat draft.txt | python3 scripts/slop_check.py -   # stdin
python3 scripts/slop_check.py --json draft.md     # machine output
python3 scripts/slop_check.py --max-score 6 draft.md   # exit 1 above 6 (for CI)
```

It flags kill-list hits, negative parallelism, em-dash overuse, self-answered questions, monotone sentence length, repeated phrases, rule-of-three habits and long words. It also loads `.creator/kill-list.txt` from the working directory if it exists, so users can ban their own pet hates (or un-ban one with `allow|word`).

A clean score removes the obvious machine marks. It does not make writing good. Taste still decides.

## Output

When writing: the text, nothing else, unless asked.
When editing: the rewritten text first, then at most five short bullets on what changed and why. No essay about the edit.

## References

| File | Read when |
|---|---|
| [references/ai-tells.md](references/ai-tells.md) | Editing text that "sounds like AI" and you need the full catalog |
| [references/dials.md](references/dials.md) | Setting tone, swearing level, energy; platform profanity rules |
| [references/rhythm.md](references/rhythm.md) | Writing for the ear: breath, stress, sentence music, before/after rewrites |
