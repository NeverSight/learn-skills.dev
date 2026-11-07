---
name: 24fps-brief
description: Turn "I want to make a short talking-head video about X", or no idea at all, into a confirmed brief and a teleprompter script before anything is recorded or edited. Use whenever the user wants to plan, script or research a short video (Shorts, Reels, TikTok, YouTube, LinkedIn, X), asks "what should I talk about", wants video ideas, topics or hooks, a daily news or new-tools or trending-repos video, a teleprompter script, an outline with sources, or a brief.md. Writes brief.md, research.md, sources.json and topics.json as plain files in the working folder. Not for recording, cutting, captioning or rendering.
license: MIT
compatibility: Needs web search and page fetch to research or find topics. Writing a script from what the user already said needs no network. Works in any agent that can write files.
metadata:
  homepage: https://24fps.dev
---

# 24fps brief

Plan the video before the camera is on. The output is a few ordinary files in the working folder (the current directory, or a folder the user names). Nothing else is needed: whatever records or edits the video reads the files.

## Pick the job

The user names one, or you infer it from the message.

1. **Write it.** Draft the teleprompter script from what they said, plus `research.md` if it exists.
2. **Research it.** Search, read the pages, write an outline with numbered citations and `sources.json`. Then offer to write the script. Read `references/research.md` first.
3. **What should I talk about?** From a standing prompt ("daily AI news", "new AI tools", "trending GitHub repos") or nothing, find timely candidates and pitch them. Read `references/research.md` and `references/pitch.md`.
4. **Sketch shots.** Only when asked, once `brief.md` has a Script: split it into shots, each with a framing and a small line sketch, so the person can record shot by shot. Format in `references/files.md`.

Jobs chain: topics, then research on the chosen one, then a script. Each stage leaves its file behind so the next one starts from it.

## Before you ask anything

- If `brief.md` exists, read it. Ask only about fields it leaves empty. A `status: confirmed` brief is settled: don't reopen it unless the user does.
- If `research.md`, `sources.json` or `topics.json` exist, read them too.
- If the user's message already answers a field, take it as stated. Never ask twice.

## Formed or unformed

- **Formed**: there is a clear message ("explain why X matters to indie devs"). Skip the pitch and go to the missing fields.
- **Unformed**: only a subject ("a video about Cursor"), or nothing. Ask exactly one thing first: **what are you already picturing?** Then run the pitch round (`references/pitch.md`).

## Missing fields

Fields: message (the ONE thing the viewer should take away), audience, platform, aspect, length, tone.

- Ask one question at a time, recommended option first with its reason. At most about four questions in the whole conversation.
- Platform, aspect and length have defaults for shorts: 9:16, 30 to 60 s. Infer them and list them under Inferred. Don't interrogate.
- Tone and audience: infer from the message and the platform when you can, ask when a wrong guess would change the script.
- "You decide", "whatever you think" or "just do it": infer everything, say so in one line, mark the brief confirmed.

## Check the answers together

Before the summary, look for conflicts between fields and propose a fix, don't just flag it. Examples: 30 s with six points (cut to two), vertical with a dense chart (one number on screen, say the rest), a LinkedIn audience with a meme tone, a "last week" claim with no recent source.

## Hand-off summary

Show two visibly separate lists:

- **Stated**: what the user said, each with a short quote.
- **Inferred**: what you filled in, each with its reason.

End with the angle, the hook line and the length, then ask for a yes. A correction means re-present the summary; a revised summary is not a confirmation. Set `status: confirmed` only after an explicit yes (or "just do it"). Until then write `status: draft`.

## Script style

Written for a person reading a teleprompter to camera.

- Spoken English: contractions, short sentences, one sentence per line, no semicolons.
- Line 1 is the hook. It states the payoff or the tension, not the topic ("Cursor just deleted its most loved feature", not "Today I want to talk about Cursor").
- Close on the message, restated in different words. One call to action at most.
- No stage directions, brackets, timestamps, emoji or on-screen text in the lines. Those belong elsewhere.
- Length: about 150 words per minute of `length`. Count the words and fix the script, not the number.
- Only say what the sources support. Numbers and dates in a line must match a cited source. If an unsourced claim is the user's own opinion, keep it phrased as theirs.

## Files

Write to the working folder. Exact formats are in `references/files.md`: keep them stable, other tools parse them.

| File | When |
|---|---|
| `brief.md` | Always. Frontmatter plus Intent, Script, Outline, Stated, Inferred, Notes. |
| `research.md` | After researching: outline with `[n]` citations, then `## Angles`. |
| `sources.json` | With `research.md`: only pages you fetched and read. |
| `topics.json` | After finding topics: 3 to 7, newest first. |
| `shots.json` + `shots/NN.svg` | Only when asked to split the script into shots: one framing and one small sketch per shot. |

Edit existing files in place. Keep unknown frontmatter keys. Optional check: `node scripts/check.mjs [folder]` validates all four.

## Honesty (non-negotiable)

- Cite only pages you fetched and read in this run. Every claim in an outline carries `[n]`.
- Quotes: at most 25 words, verbatim, with the URL. No invented numbers, dates or quotes.
- A page you could not open is not a source. Leave it out, or list it under "could not open" without a number.
- Prefer primary sources (the vendor's post, the repo, the paper) over write-ups of them. Record the publish date.
- For news, look at the last 7 days and say so when nothing recent turned up. Never present an old item as new.

## After the brief

Tell the user where the files are and stop. Don't start recording, cutting or rendering. If they want motion graphics or captions next, the `24fps-motion` skill finds presets for those.
