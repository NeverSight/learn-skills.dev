---
name: youtube-comment-miner
description: "Mine YouTube comments for content ideas, audience questions, pain points, and monetization signals using YouTube Data API v3. Analyze comments from specific videos, top videos of a channel, or search results for a topic. Use when users want to (1) Find what their audience is asking for, (2) Mine content ideas from comments, (3) Discover audience pain points, (4) Find FAQ patterns in comments, (5) Detect monetization signals, (6) Understand audience language and sentiment. Requires user's YouTube Data API v3 key."
---

# YouTube Comment Miner

Mine YouTube comments to extract content ideas, audience questions, pain points, and monetization signals.

## Usage

```
/youtube-comment-miner https://youtube.com/watch?v=VIDEO_ID
/youtube-comment-miner @ChannelHandle --top 5
/youtube-comment-miner --topic "meditation for beginners" --top 10
/youtube-comment-miner VIDEO_ID1 VIDEO_ID2 VIDEO_ID3
```

## Instructions

### Step 1: Parse Arguments

Input mode (one of):
- **Video URL(s) or ID(s)**: specific videos to mine
- **Channel** (`@handle`, URL, or ID) + `--top N`: mine the channel's top N videos by views (default: 5)
- **Topic** (`--topic "keyword"`) + `--top N`: search for videos on the topic, mine the top N (default: 10)

Also:
- **--max-comments N** (optional): max comments per video (default: 100, max: 500)
- **--scan-limit N** (optional, channel mode): cap how many uploads get scanned (default: whole channel)

### Step 2: Get the API Key

Check the user's Claude memory for a YouTube Data API v3 key. If not found, ask:
> "I need a YouTube Data API v3 key to mine comments. You can get one from the Google Cloud Console. Please paste your key."

### Step 3: Run the Bundled Script

Run `scripts/mine_comments.py` — resolve the path relative to this skill's own directory:

```bash
# Specific videos
YT_API_KEY=API_KEY python3 <skill-dir>/scripts/mine_comments.py --videos VIDEO_ID1 VIDEO_ID2 --max-comments 100

# Channel top videos
YT_API_KEY=API_KEY python3 <skill-dir>/scripts/mine_comments.py --channel "@handle" --top 5 --max-comments 100

# Topic search
YT_API_KEY=API_KEY python3 <skill-dir>/scripts/mine_comments.py --topic "topic keyword" --top 10 --max-comments 100
```

Dependency: `pip3 install google-api-python-client`.

The script fetches relevance-ordered top-level comments, tags each one into
categories (question, content_request, pain_point, praise, criticism, suggestion,
monetization_signal, personal_story), flags "gold nuggets" (5+ likes on a question
or request), and builds an audience-language word frequency list.

**Channel mode note:** the script finds top videos by paging the uploads playlist
and ranking by actual view count, which is both cheaper and more accurate than
`search.list(order=viewCount)` — that endpoint only ever sees a truncated slice
of a channel.

### Step 4: Read the Data

```
reports/data/comment-mine-<slug>-<YYYY-MM-DD>.json
```

### Step 5: Write the Report

Write to the path the script printed:

```
reports/comment-mine-<slug>-<YYYY-MM-DD>.md
```

```markdown
# Comment Mining Report: [Source]
*Analyzed [date] | [N] comments across [N] videos*

## Executive Summary
- 3-4 bullet points: Key findings from comment analysis
- What the audience wants, worries about, and loves

## Videos Analyzed
| # | Title | Views | Comments Mined |
|---|-------|-------|----------------|

## Content Requests (What Your Audience Wants)
Top requests ranked by likes. Include exact quotes.
- "Can you make a video about..." patterns
- Specific topics requested multiple times

## Frequently Asked Questions
Questions ranked by frequency/likes.
Group similar questions together.
These are potential video topics.

## Pain Points & Struggles
What viewers are struggling with.
Each pain point = potential video solving that problem.

## Audience Language Patterns
- Words and phrases viewers use repeatedly
- This is the language to mirror in titles, descriptions, thumbnails
- Common vocabulary table

## Praise Patterns (What Works)
What viewers love -- tells you what to do MORE of.

## Criticism Patterns (What to Fix)
What viewers complain about -- tells you what to avoid/improve.

## Gold Nugget Comments
High-engagement comments with questions or requests.
Each one is a validated content idea.

## Monetization Signals
Comments asking about courses, products, tools, etc.
Revenue diversification opportunities.

## Suggestions & Tips from Viewers
Viewer-suggested improvements and ideas.

## Actionable Content Ideas
5-8 specific video ideas derived from comment data:
- Idea title
- Source (which comments inspired it)
- Why it would work
- Priority (based on frequency/engagement)

## Quota Usage
| Operation | Calls | Units |
|-----------|-------|-------|
Use the `quota_used.breakdown` block from the JSON.
```

### Step 6: Report Completion

Tell the user the report path, total comments mined, the top finding, the number
of content ideas generated, and the quota consumed.

## Quota Estimate

`commentThreads.list` costs 1 unit per 100 comments.

| Mode | Operations | Total |
|------|-----------|-------|
| Direct videos (5 videos, 100 comments each) | 1 `videos.list` + 5 `commentThreads.list` | **~6** |
| Channel (500-video channel, top 5) | 1 `channels.list` + ~10 `playlistItems.list` + ~10 `videos.list` + 5 `commentThreads.list` | **~26** |
| Topic (top 10) | 1 `search.list` + 1 `videos.list` + 10 `commentThreads.list` | **~111** |

Channel mode previously cost ~107 units because it used `search.list`; the uploads-playlist
route cuts that to ~26 and scans the whole channel instead of a partial slice.
Daily default allowance is 10,000 units, resetting at midnight Pacific Time.
