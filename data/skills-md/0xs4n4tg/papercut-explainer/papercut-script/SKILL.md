---
name: papercut-script
description: Turn a link into a papercut reel script. Researches a sourced facts list, writes the 75-95 word script on the 10-beat spine, a banner fact track, a staging table with one set per banner, and the humour pass. Use for "write the script", "research this repo for a reel".
---

# Papercut script

Research, script, banner track, staging and gags are written together, because each one feeds the others. The full system, with the phrase bank and two staged examples, is `references/storytelling.md`. Gag and format banks: `references/comedy.md`.

Every beat runs three tracks that do different jobs:
- **Voiceover** (shown as caption tags): tells the story, casual and second person, changes every sentence.
- **Banner**: adds the hard fact, number or honest caveat the voiceover skips, changes every 1.8-3 s.
- **Set**: literally illustrates a concrete noun from the voiceover, with the product UI doing the demo, changes with the banner.

## Preflight

- Install: Minimal is enough. Resolve `$PAPERCUT_LIB` only if you want the backdrop sheet (`library/papercut/public/bg/backdrops/_sheet.jpg`) when choosing sets. Each image costs about 0.7-1.5k tokens, so open only what the step needs.
- Needs the BRIEF at the top of `episodes/NN-slug/research/facts.md` and the HOOK block at the top of `episodes/NN-slug/papercut/STORYBOARD.md`. Missing one: run `papercut-strategy` or `papercut-hook` first.
- Research needs web fetch or search, and any browser tool for screenshots. Without them, ask the user for screenshots and facts.

## 1. Research and rough UI

- Collect facts from the source with a source for each: name, maker, numbers, price, requirements, limitations, competitor numbers. Mark anything uncertain.
- Grab the key screens (2-4), real labels and button text, the accent colour and hero images. The video rebuilds a rough version of the UI as papercut props, not a screen recording (`references/storytelling.md` section 5).
- Confirm the role framing from the BRIEF. Never invent product behaviour. See the role-framing note in `../papercut-explainer/references/frame-breakdown.md`.
- Write the list to `research/facts.md` under the BRIEF. Every number in the script, banners and UI must trace back to it.

## 2. Pick the mode

| Mode | When |
|---|---|
| Open-source drop | A free or local alternative to a paid product |
| News launch / worth-it | A new paid tier, model or feature from a big company |
| Feature unlock / how-to | A hidden setting or command that changes how a tool works |

Hook formulas and the middle of each mode: `references/storytelling.md` section 6. Apply the hook update: open the gap and the stake, not the news.

## 3. Script on the spine

Write 75-95 words for 22-30 s, about 3.5-4 words a second, inside the chosen format, with a new set every 1.5-3 s. The 10 beats:

1. Hook (0-3 s), already fixed by `papercut-hook`
2. Proof or tension
3. Reframe ("So instead of..., you can...")
4. Name reveal ("It's called...", never before the hook)
5. How it works, one concrete demo
6. Escalation ("And X is just the start, because..." plus a stack of exactly three)
7. Peak ("And get this:" plus the biggest number)
8. Catch (the honest counterpoint)
9. Payoff ("which means...")
10. CTA ("Good thing I made [freebie]. For the link, comment KEYWORD.")

Shorten beats rather than speeding up the voice. Rules:
- Second person, contractions, short clauses joined by "and", "because", "which means". Vocabulary at the audience level in `SERIES.md`.
- Name a big brand in the first sentence, even when the subject is something else.
- Every number is concrete and sourced. One feature stack, always three items.
- At least one real limitation, in the VO or the banners. The CTA keyword is one short word tied to the topic.
- The last line repeats the hook's key word or number, then gives the keyword.

Write it to `narration/script.json` as `[{"id": "l1_hook", "text": "..."}, ...]`, one line per sentence or clause group. Line `l1_hook` is SAY from the HOOK block. Mark the one or two words each line leans on (the number, the twist word, the verdict) in the staging table; `papercut-voice` uses them.

## 4. Banner track

10-18 banners, 3-7 words, ALL CAPS, one fact each, about one every 2-3 s. They never repeat the VO: read alone they are a fact sheet. Include a headline stat, a price translation, a credibility fact, availability, at least one honest caveat, at least one trust or safety fact, feature claims, at least one competitor contrast, and a range/decision banner before the CTA. Types and examples: `references/storytelling.md` section 3.

## 5. Staging table

One row per banner, written into `STORYBOARD.md` under the HOOK block:

`t (s)` | VO words under it | BANNER | SET (room + bg colour) | HERO PROP (a visual pun from the VO's concrete noun) | PRODUCT UI moment | MASCOT action and costume prop | GAG

- A new set for every banner, background colours rotating. The set illustrates a word in the VO line, not the banner.
- Numbers become physical props: price signs, scales, multiplier walls, gauges, meters, races. Competitors appear as pinned cards, never as the hero.
- The mascot is the viewer's proxy and reacts. Product UI is a rough rebuild on a paper monitor or laptop with fake interactions.
- One callback to an earlier set before the CTA. The CTA set shows a comment box typing the keyword.
- `papercut-storyboard` adds the camera and transition columns.

## 6. Humour pass (after the script, before staging is final)

Add the GAG column. The voiceover stays straight; only the picture is silly.
1. One format for the whole reel.
2. One gag per banner that acts out the point, from `references/comedy.md`.
3. A costume prop per idea. The mascot's own item stays on and gets one prop on top.
4. One struggling-mascot beat, on the catch line.
5. A prop on frame 0 that returns changed in the CTA set (I'M OUT becomes FREE).
6. One absurd, unexplained background moment.
7. At most one meme, rebuilt in the series' own style, never a real clip, still or audio.

No gag may cover the banner, the captions or the key number, and each must read in under 1 s.

## Gate

- [ ] 75-95 words, 22-30 s, one honest limitation, a stack of exactly three.
- [ ] Every number and banner traces to `facts.md`; banners alone read as a fact sheet.
- [ ] Last line repeats the hook's key word or number.
- [ ] Humour pass done: costume per idea, a struggling beat, a returning prop, one absurd moment, at most one meme.

## Hand-off

Next is `papercut-storyboard`. It reads `narration/script.json` and the HOOK block and staging table in `episodes/NN-slug/papercut/STORYBOARD.md`. For a script-only run, stop here and give the user those files. The copy-paste storytelling prompt for another tool is `references/storytelling.md` section 7.
