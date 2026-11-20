---
name: reddit-keywords
description: >-
  Mine Reddit for blue-ocean keyword opportunities — high-traffic discussions
  with weak ranking competition, via Google Autocomplete demand signals and
  subreddit discovery. Finds the questions communities ask that no good page
  answers yet. Use when the user asks "find low competition keywords on
  Reddit", "what is my niche discussing on Reddit", "reddit keyword research",
  or wants content topics validated by real community demand.
metadata:
  version: 1.0.0
  author: ZensInk
  source: https://zens.ink/skills/#reddit-keywords
  license: MIT
---

# Reddit blue-ocean keyword mining

Reddit is a demand signal Google lags behind. This tool finds
"reddit <topic>" autocomplete demand, discovers the subreddits, and flags
high-traffic low-competition threads worth answering with real content.

## When to use

- "Find blue ocean keywords for my niche"
- "What are people asking on Reddit about X?"
- Validating a content idea against real community demand.

## When NOT to use

- The user wants to post/spam Reddit — this is research, not promotion.
- B2B enterprise topics with zero Reddit presence — the tool will find
  nothing, correctly.

## Setup

```bash
pip install zens-ink
```

No key needed for the autocomplete demand layer. Direct Reddit API access is
often blocked (403) from datacenter IPs; the tool auto-falls-back to the
autocomplete demand layer when that happens.

## Commands

```bash
python3 -m zens_ink.reddit_blueocean "ai video generator"
python3 -m zens_ink.reddit_blueocean "note taking app" --subreddits r/Productivity,r/productivity
python3 -m zens_ink.reddit_blueocean "ai 写作工具" --lang zh
python3 -m zens_ink.reddit_blueocean "crm" --niche "small business owners" --json
```

## How to read the results

- High demand + thin Google competition = blue ocean: write the definitive
  answer, the thread is proof people are looking.
- Questions repeated across subreddits = evergreen demand, not one thread's
  spike.
- A thread ranking itself in Google for the query = Google could not find
  a better page. That is the loudest possible signal.

Respect the community: answer threads genuinely if participating; the play
here is building the page they linking to, not link spam.

## Next steps

- Candidate topics → `keyword-difficulty` for the go/no-go, then
  `search-intent` for page type.

## Going deeper

ZensInk Pro's Content Radar folds community demand into the editorial
calendar automatically: https://zens.ink/pricing/
