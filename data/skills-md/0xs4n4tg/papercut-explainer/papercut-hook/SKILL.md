---
name: papercut-hook
description: Write or fix the hook of a papercut reel. Produces the SAY / WRITE / SHOW / ALIGN block, five variants scored with the hook check, the frame-0 cover title and the motion out of the hook. Use for "write a hook for...", or when a reel's first three seconds lose people.
---

# Papercut hook

The hook is the most important step. A reel's hook is three separate, explicit layers, and none may be skipped or left implied. Write all of them before anything else in the script.

## Preflight

- Install: Minimal is enough. No library needed.
- Read the BRIEF at the top of `episodes/NN-slug/research/facts.md` (topic, format, audience, CTA) and the facts list, so every claim can be checked. If there is no BRIEF, run `papercut-strategy` first.
- Read `SERIES.md` for the audience level and regions.

## The HOOK block

```
HOOK
SAY:   <the first spoken sentence>
WRITE: <the frame-0 title, 2-5 words, ideally a number; the episode.json "hook">
SHOW:  <what frame 0 and the first 2 s show: the mid-action moment, the camera move>
ALIGN: <the one idea all three point at>
```

No scene gets built until all four lines are filled and pass the alignment test.

| Layer | Rule |
|---|---|
| SHOW, the first frame | The most striking moment, already mid-action. No establishing shot, no fade-in, no empty room. It must make sense muted. |
| WRITE, the on-screen title | The cover title (2-5 words, ideally a number), fully visible on frame 0 for about 2-3 s. It carries the other half of the gap, never the same words as the voice. |
| SAY, the spoken line | Opens the gap within about 10 words. Names who it's for. The stake or number comes early. Never answers itself. No anonymous news framing ("Someone just released..."); a named, credible source is fine. |

Skip the "stated as news" opening from beat 1 of the spine ("A solo dev just open-sourced..."). Open the gap and the stake instead, and name a big brand the viewer already knows in the first sentence.

## Alignment test

What you show, what you write and what you say all point at one idea. They differ in words, never in subject. If the voice says "your screenshots leaked" while frame 0 is a calm desk and the title is about stars, each layer opens a different loop and none lands. Cover any two layers: the remaining one should still hint at the same idea.

## Variants and the hook check

1. Write 5 variants from at least three of the seven patterns in `references/hook-patterns.md` (borrowed authority + giveaway, name the viewer then a number, one object one number one twist, price shock, pain, verdict or conflict, own authority).
2. Score each with one point per yes:
   1. Does the spoken line open a gap (a question or tension the viewer needs closed) within about 10 words?
   2. Does it say who it's for, or what is at stake?
   3. Does it carry one concrete number, object or twist instead of a vague claim?
   4. Does it leave the answer for later?
   5. Does frame 0 plus the title work with the sound off?
   6. Is every claim true to the facts sheet?
3. Pick the variant with the most points. Drop any variant that fails question 6.

## The frame-0 title (`episode.json` "hook")

Every reel opens on its hook. The `hook` key in `episode.json` puts the cover title on screen from frame 0 (`build_vo.py` writes it into `plan.json`) and holds the banner back until the title leaves.

```
"hook": {"lines": [["AI", "LEAKED"], ["13,000+"]], "hot": ["13,000+"], "until": "yes", "size": 108, "top": 220}
```

- `lines`: the WRITE text as torn tags, one array of words per line. `hot`: the words that get the yellow tag.
- The title leaves at the onset of the `until` word (`["yes", 2]` for its 2nd occurrence), or after `"hold"` seconds (default 2.4).
- Title stays 2-5 words and shares no words with SAY.

## The cut out of the hook carries motion

A hook that ends on a held pose feels abrupt and drops the attention it just earned.
- Give the hook scene's last ~10 frames an accelerating push (a tiny pull back first).
- Scene 2 opens on an impact at its focal prop, then the camera eases back to the set. For example, the proof card slams onto the board with a `stamp`, the camera starts at 1.17x, and a character scurries in from off-frame.
- End the title on the cut with `"hook": {"hold": <S01 seconds>}` so it lifts away during the push instead of covering scene 2's first frames.

## Gate

- [ ] SHOW is mid-action on frame 0 and reads muted.
- [ ] WRITE is on frame 0 and isn't the spoken words.
- [ ] SAY opens the gap within 10 words.
- [ ] All three pass the alignment test, and ALIGN names the one idea.
- [ ] The winning variant scored best and passed question 6.

## Hand-off

Write the HOOK block at the top of `episodes/NN-slug/papercut/STORYBOARD.md` (create the file if it isn't there). Note the hook's key word or number; the script's last line repeats it. Next is `papercut-script`, which also puts SAY into line `l1_hook` of `narration/script.json`.
