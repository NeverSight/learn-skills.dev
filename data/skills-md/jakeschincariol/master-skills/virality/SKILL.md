---
name: virality
description: >-
  Find what is already working in a niche, then rewrite it in the user's own voice for their
  audience and hand back a shoot-ready short-form video script (Reels, TikTok, Shorts), with a
  LinkedIn post or long-form version as a secondary output. Ranks posts by how far each beat its
  creator's own median, names the hook formula, scores hooks, and strips AI tells. Use when the
  user says "make me a viral video", "write a reel/TikTok/short", "what's working in my niche",
  "find viral videos", "rewrite this in my voice", "give me a hook", "script my next video", or
  wants content that performs. Fuses Jake's LinkedIn and YouTube agent skills.
---

# virality

One workflow: niche in, shoot-ready viral video script out. It finds what is already working,
breaks the winners down, and rewrites the pattern (never the video) in the user's voice for the
user's audience. Every tool is Python 3 standard library and runs from `tools/` in this folder.

```bash
python3 tools/collect.py pasted.txt export.csv yt.json -o candidates.json   # normalize
python3 tools/swipe.py candidates.json --min 2.0                            # outliers
python3 tools/hookscore.py hooks.txt                                        # score + formula
python3 tools/hookscore.py --list                                           # the 26 formulas
python3 tools/speech.py --line "I saved \$400 on flights." --wpm 170        # time a line
python3 tools/humanize.py draft.txt --report -o clean.txt                   # strip AI tells
python3 tools/detect.py draft.txt clean.txt                                 # 5-check panel
python3 tools/title.py --title "..." --cover "THREE WORDS"                  # title + cover
```

Paths are relative to this skill folder. Write the user's working files to
`./virality/<slug>/` in their current directory, never inside the skill folder.

## Hard rules (Jake's, non-negotiable)

1. **The hook leads with a concrete payoff**: money made, money saved, time saved, or a number,
   inside the first ~8 words spoken or on the first on-screen card. "I saved $400 on flights"
   beats "AI can book travel". `hookscore.py` reports this as PAYOFF: LEADS / LATE / MISSING.
2. **Real proof over vibes.** The beat after the hook shows the receipt: the screenshot, the
   result, the number on screen. If there is no proof, the hook is a claim, so soften it.
3. **One CTA: comment a keyword.** One word, said out loud and shown on screen, plus what they
   get: `Comment PLAN and I'll send you the list.` Put the same ask as caption line 1.
4. **Never invent a number, result, client or source.** Missing figure: ask, or write
   `{{your number}}` and flag it. A script with placeholders is not shoot-ready.
5. **Copy the formula, never the video.** The hook shape, structure, length and pacing. Not
   their words, footage or edit. Attribute every winner you studied.
6. **No em dashes** in anything you hand over. `humanize.py` removes them.

## Step 1: the brief (niche, audience, offer, voice)

Read `~/.claude/virality/audience.md` and `~/.claude/virality/voice.md` if they exist (also
check `~/.claude/youtube/voice.md` and `~/.claude/linkedin/voice.md` from Jake's other packs).
If missing, fill them from `templates/audience.md` and `templates/voice.md`:

- Ask ONE batched question: niche, the one viewer, the offer and comment keyword, platforms,
  and 3 to 5 of their own captions or video transcripts (or links you can read).
- Build the voice from those samples using the method in `templates/voice.md`. Measure their
  pace with `python3 tools/speech.py their_video.srt` and use it as `--wpm` from then on.
- Collect their proof bank: real numbers they will put their name on.
- Do not proceed on a thin idea. "Post about AI" needs: what happened, to whom, what it cost
  or returned.

## Step 2: find what's working

Goal: 30+ posts across 6 to 12 creators (from `audience.md`), at least 4 per creator, recent
(last 90 days). Sources, in order of preference:

1. **The user's own posts.** Their last 20 to 30 with view counts. Their own outliers are the
   strongest evidence that exists.
2. **YouTube Shorts / YouTube**, public, no login. If yt-dlp is installed
   (`python3 -m yt_dlp --version`), list a channel's public Shorts with counts:
   `python3 -m yt_dlp --flat-playlist --playlist-end 40 -J "https://www.youtube.com/@HANDLE/shorts" > a.json`
   If it is not installed, say so and use another source. Never pass cookies or log in.
3. **TikTok, Instagram, LinkedIn**: the user reads the numbers off their own screen and pastes
   them (they are already logged in on their phone), or a public analytics site. You may use
   web search to find public posts and accounts. Never log into an account, never ask for a
   password, never scrape behind a login, never automate a logged-in browser.

Paste format (one post per line, `|` or tab separated), then normalize:

```
@creator | 1.2M | first line of the hook or caption | url | 0:41
```

```bash
python3 tools/collect.py pasted.txt a.json b.json -o virality/<slug>/candidates.json
python3 tools/swipe.py virality/<slug>/candidates.json --min 2.0
```

`swipe.py` ranks by **views as a multiple of each creator's own median**, so a 400K post on an
account that usually does 30K outranks a 2M post on an account that usually does 2M. Creators
with fewer than 4 posts are skipped, on purpose: one or two posts is not a median. 3x and above
is a strong signal; under 1.5x is that creator's normal day. Say the sample size out loud: 12
posts is an anecdote, 40 across 6 creators is evidence.

## Step 3: break the winners down

Take the top 3 to 5 outliers. Get each transcript (their captions, the user's paste, or
`yt-dlp --write-auto-subs --sub-format json3 --skip-download URL` for public YouTube). For each:

| field | how |
| --- | --- |
| hook formula | `python3 tools/hookscore.py --hook "their first line"` (name from `tools/hooks.json`) |
| payoff | the PAYOFF line from the same run: what number, how early |
| format | talking head, split screen, green screen, screen-share tutorial, listicle, skit, B-roll VO |
| length + pace | `python3 tools/speech.py transcript.srt` (seconds, wpm) |
| structure | hook, proof, steps, rehook at ~50%, payoff, CTA: which beats, in what order |
| CTA | the exact ask and keyword, and where it appears (spoken, on screen, caption line 1) |

Then state the ONE thing the winners share that the rest of the batch does not. The formula
name is a judgement about the words, not a claim about why the video got its views. Say so.

## Step 4: rewrite in their voice, for their audience

Pick the winning pattern and rebuild it from the user's own material:

- Their story, their number (from the proof bank), their viewer's words (from `audience.md`).
  If the hook would work with another creator's name on it, it is not their hook yet.
- Their sentence shape, person, pace and signature phrases from `voice.md`. Contractions.
  Read every SAY line out loud in your head: if they would not say it, rewrite it.
- Then strip machine tells and check the result:

```bash
python3 tools/humanize.py virality/<slug>/draft.txt --report -o virality/<slug>/clean.txt
python3 tools/detect.py virality/<slug>/draft.txt virality/<slug>/clean.txt
```

`humanize.py` fixes invisible characters, typography (em dashes) and the slop lexicon
automatically, and FLAGS structural tells ("it's not just X, it's Y", rule-of-three, clickbait
openers) for you to rewrite by hand. Aim for PASS on `detect.py`. These are local heuristics,
not GPTZero or any detector API; never tell the user their text is "undetectable".

## Step 5: score and pick the hook

Write 5 hooks on 5 different formulas from `tools/hooks.json` (payoff-first ones are marked;
`--list` shows them), each with a spoken line and a separate on-screen line (6 words or fewer).

```bash
python3 tools/hookscore.py virality/<slug>/hooks.txt
```

Keep the top two. Ship the highest score whose PAYOFF is LEADS. If the best is under 50, you do
not have the hook yet: rewrite, do not polish. The score catches greetings, preambles and vague
hooks well; it cannot predict which of two good hooks wins. Show the user both.

## Step 6: package the shoot-ready script

Write `virality/<slug>/script.md` in exactly the format of `templates/script.md` and print it
in chat:

- **Beats** `### N. LABEL (m:ss-m:ss)` with `SAY:`, `SCREEN:`, `VISUAL:`. Labels: HOOK first,
  then PROOF / STEP / REHOOK / PAYOFF, CTA last. Time every SAY line with
  `python3 tools/speech.py --line "..." --wpm <their pace>` and use those timecodes.
- **Pacing**: hook under ~3 s spoken; 20 to 45 s total for a Reel unless the winners say
  otherwise; a rehook line near the middle ("Here's the part nobody does"); no shot held
  longer than ~1.5 s (list several shots per beat in VISUAL, separated by " / ").
- **Visuals**: show the noun on the word it is said (say "receipt", show the receipt). Real
  screens and real proof at real proportions, no invented UI. Keep text in the Reels safe
  zone: y 240 to 1470 on 1080x1920, right rail (x > 950, below y 1000) clear. Captions in
  short 1 to 3 word phrases in the lower third, never over the face.
- **CTA beat**: `Comment KEYWORD and I'll send you <the thing>.` Keyword on screen.
- **Caption**: line 1 is the comment-keyword ask (it survives the "... more" cut, about 125
  characters). Then 2 to 4 short lines with the words people search. No links.
- **Hashtags**: 3 to 5 specific ones. Instagram caps posts at 5 since 18 December 2025.
  Never #fyp, #viral, #explorepage.
- **Cover**: COVER text 2 to 4 words, different words from the title, and a TITLE for Shorts or
  YouTube. Check them as a pair: `python3 tools/title.py --title "..." --cover "..."`.
- **Secondary output** when asked or when LinkedIn is in the brief: a LinkedIn post (first line
  under ~140 characters so it survives "see more", 900 to 1,300 characters, blank line between
  short paragraphs, no link in the body, at most 3 hashtags, a closing question only this post
  could ask). For long-form YouTube: the same hook, a 15-second opening that confirms the
  title, opens a question and proves the payoff exists, then beats with `[ON SCREEN: ...]`.
  Run both through `humanize.py`.

End with a receipt and a question:

```
SCRIPT READY  virality/<slug>/script.md
based on:   @creator, 1.2M views, 24x their median (formula: The Payoff)
hook:       80.8 STRONG, payoff LEADS ($62 at word 3)
length:     27.5s across 6 beats at 190 wpm
keyword:    PLAN (spoken, on screen, caption line 1)
humanizer:  N artefacts stripped, detect.py <score> <verdict>
open flags: none   (or: 2 {{your number}} placeholders to fill before shooting)

Shoot it, or change it?
```

Append one line to `~/.claude/virality/log.md` on "shoot it": date, formula, hook, keyword. Next
run, read it and ask for the views so the user's own results feed step 2.

## Failure handling

- **No data / no tools available**: no yt-dlp, no paste. Ask the user for 10+ posts from their
  niche with view counts. If they cannot, write from the formula library and say plainly that
  the hook is not backed by niche evidence this time.
- **All creators skipped as thin**: collect more per creator, or add a `median` column with
  each creator's typical views (from a public analytics site) so `swipe.py` can rank them.
- **No real number for the hook**: ask. Do not invent. Use `{{your number}}` and flag it.
- **The winner's format needs something the user cannot film** (a lab, a car, a second
  person): pick the next outlier whose format they can shoot this week.
- **A tool errors**: read the message (exit 2 means bad input), fix the input, re-run. Never
  hand-wave a score you did not compute.

## Limits (say these honestly)

- **Nothing here guarantees views.** Reach depends on the face, the edit, the audio, the first
  frame and who the platform shows it to. This raises the odds by copying patterns that are
  measurably working right now and fixing the hook before the take.
- `hookscore.py` separates real hooks from deliberately bad ones well (AUC 0.83 in its original
  calibration) and a creator's hits from their own misses barely at all (AUC 0.56).
- Outlier multiples from a hand-collected batch are evidence, not proof. Formats decay; re-run
  step 2 monthly.
- Nothing logs in, posts, comments, follows or DMs. These tools write; the user publishes.

## Credits

Fused from two MIT packs by Jake Schincariol (same author as this repo):
[linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill) (humanize.py,
detect.py, slop.json, three payoff formulas) and
[youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill) (swipe.py,
title.py, the 21-formula hook library and classifier). The hook scoring panel comes from his
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) because it was
calibrated on short-form hooks. Each copied file carries an origin header. The full packs:

```
/plugin marketplace add Jakeschincariol/linkedin-agent-skill
/plugin marketplace add Jakeschincariol/youtube-agent-skill
```
