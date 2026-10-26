---
name: papercut-strategy
description: Decide what a papercut reel should be. Picks the topic, one familiar format, the audience level, the comment-keyword funnel and caption, studies competitor reels, and runs the post-publish autopsy. Use before any hook or script, or when reviewing how a posted reel did.
---

# Papercut strategy

These notes decide what a reel says and why it holds attention. The other papercut skills decide how it is written, staged and built. The rules come from studying high-performing faceless tech reels and from reading platform insights after posting. Keep your own evidence in the series' `research/analytics/`.

## Preflight

- Install: Minimal is enough. No library needed.
- Find the series folder and read its `SERIES.md` first. It holds the audience (who, level, regions to aim for and avoid), voice, palette and mascot notes, the visual style, the keyword log and what has worked so far. If it is missing, ask the user for those fields and write the file.
- For a competitor study: `yt-dlp`, `ffmpeg` and any speech-to-text tool. For an autopsy: the platform's insights numbers from the user.

## 1. Topic

- Re-skin proven winners. A topic that worked (for you or a competitor) in a new familiar format beats a new topic in a plain format. Example: a reel about running several AI agents as a council, remade as "a jury of 12 AIs puts your idea on trial".
- The viewer must be able to use the outcome. If they can't do anything with it, skip it.
- Something to give away: every winner promises a free skill, prompt, template, cheat sheet or setup by DM.
- Speed on a hot repo. The first reel on a trending repo takes most of the views. Ship within a day or two, on an angle the earlier reels didn't use (`../papercut-hook/references/hook-patterns.md`).
- Demand signals: competitor outliers (likes at 5x or more of their median), trending repos (stars per day), front-page threads, same-day launches. Save candidates to the series' idea backlog.

## 2. Format

Pick one familiar real-world format for the whole reel before writing a word: courtroom, pitch show, cooking show, heist movie, nature documentary, dating show, character-select screen, boss fight, job interview, Olympic podium. The viewer gets the premise in a second and every set and gag comes from it. A plain list of facts has no premise to grasp, so it gets less attention than the same facts told inside a format. The bank, with the story each format carries, is `../papercut-script/references/comedy.md`.

## 3. Audience level

Write at the level `SERIES.md` sets. There is no default audience. The feeling to leave behind: you're not behind, and now you know something most people don't.

## 4. Funnel and caption

- Spoken CTA: "Good thing I made [freebie]. For the link, comment KEYWORD." One short keyword tied to the topic.
- Deliver the freebie by DM with whatever comment-to-DM tooling the account allows. Keep sends slow and spaced, because platforms rate-limit bursts.
- Caption: the hook as the first line, a follow line so the DM lands, "READ BELOW" with the useful part written out, one send prompt ("Send this to the friend who..."), 3-5 hashtags.
- Shares matter most to the algorithm. A funny or useful reel gets sent.

## 5. Write the BRIEF

Put this block at the top of `episodes/NN-slug/research/facts.md`. `papercut-hook` and `papercut-script` read it.

```
BRIEF
Source:   <link(s)>
Claim:    <the one claim the video proves>
Role:     <who or what does the work vs who advises or approves>
Mode:     open-source drop | news launch / worth-it | feature unlock
Format:   <the one familiar format>
Audience: <level, copied from SERIES.md>
CTA:      <KEYWORD> -> <the freebie>
Length:   22-30 s
```

## 6. Competitor study (when the user shares reels)

Method, setup and the subagent prompt: `references/competitor-analysis.md`.
- One subagent per reel, up to 4 at a time. Each downloads the reel, extracts frames at 2 fps, transcribes it, applies the six-question hook check and returns a fixed-format report.
- Synthesise into a comparison table (likes and comments vs the creator's typical reel, age at fetch, look, length), what drove the outliers, what to borrow and what stays your difference.
- Save it to `research/analytics/YYYY-MM-DD-<creator>-reels.md`. One reel is noise; look for a pattern across 4 or more.

## 7. After posting: the autopsy

- At about 2 h and 24 h collect views, skip rate, average watch time, the retention curve, likes, comments, saves, shares, follows, traffic source, top countries and ages.
- Read them in this order: hook, topic, format, audience, timing. Fix the earliest thing that failed before touching later ones.
- If most viewers are gone by 3-5 s, or the skip rate is clearly worse than your own median, the hook failed. Run `papercut-hook`.
- Write `research/analytics/YYYY-MM-DD-autopsy.md` and update `SERIES.md` with what changed.

## Gate

- [ ] `SERIES.md` read; audience, regions and voice respected.
- [ ] Topic has a demand signal, a usable outcome and a freebie by DM.
- [ ] One format named in a line.
- [ ] Vocabulary and the DM match the audience level.
- [ ] BRIEF written; caption planned.

## Hand-off

Next is `papercut-hook`. It reads the BRIEF in `episodes/NN-slug/research/facts.md` and writes the HOOK block at the top of `episodes/NN-slug/papercut/STORYBOARD.md`. If the episode folder isn't scaffolded yet, create `research/` and `papercut/` by hand; `papercut-build` merges them when it scaffolds.
