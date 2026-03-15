---
name: scrapesocial-reddit
description: Use when the user wants Reddit research or workflow guidance for lead generation, influencer discovery, brand monitoring, competitor analysis, content analytics, trend research, or audience analysis, including subreddit inspection, subreddit or Reddit-wide search, post comment retrieval, and Reddit ad research.
license: MIT
prerequisites:
  - Scrape Creators API key
metadata:
  author: Skill Atlas
  version: "0.1.2"
  homepage: https://skillatlas.sh/
---

# Scrapesocial Reddit

Use this skill for Reddit discovery, content research, comment extraction, and ad intelligence.

## Prerequisites

- A Scrape Creators API key is required for this skill. Get one at [scrapecreators.com](https://scrapecreators.com).

## Quick start

Install the CLI once:

```bash
npm install -g scrapesocial@0.1.0
```

Make sure the CLI can authenticate:

```bash
export SCRAPECREATORS_API_KEY=<your-api-key>
scrapesocial reddit search --query "site reliability"
```

## How it works

This skill uses the `scrapesocial` CLI (installed from [npm](https://www.npmjs.com/package/scrapesocial)) to query the Scrape Creators API. All requests are authenticated with your `SCRAPECREATORS_API_KEY` environment variable. The CLI sends search queries to the Scrape Creators API and returns Reddit content. No data is sent elsewhere. No data is stored locally beyond command output.

## Goal-led workflows

### Lead generation

Use it for demand-led prospecting and lead qualification by finding communities and posts that reveal active need. It is not a contact-export workflow. Start with `reddit search`, then inspect strong matches with `reddit subreddits get` and `reddit posts comments`.

### Influencer discovery

Use it to spot recurring experts, operators, or visible community voices rather than creator-style influencer lists. Start with `reddit search` or `reddit subreddits posts`, then inspect post and comment authors in the returned discussions.

### Brand monitoring

Use it to watch brand mentions, subreddit conversations, and recurring complaints or praise. Start with `reddit search` for brand terms, then move into `reddit subreddits posts` or `reddit posts comments` where the discussion is strongest.

### Competitor analysis

Use it to compare competitor mentions, objections, community fit, and ad activity. Start with `reddit search` for each competitor, then add `reddit subreddits search` or `reddit ads search` when you need narrower coverage.

### Content analytics

Use it to understand which themes, titles, and discussion hooks create traction inside a subreddit. Start with `reddit subreddits posts`, then use `reddit posts comments` on representative posts.

### Trend research

Use it when you need fast, cross-community signal on emerging topics, questions, or pain points. Start with `reddit search`, then validate which subreddits matter with `reddit subreddits get` and `reddit subreddits posts`.

### Audience analysis

Use it for qualitative audience analysis from comments, repeated language, objections, and subreddit norms. Start with `reddit posts comments` on strong threads or `reddit subreddits search` for topic-specific community language.

## Command selection

Choose the command by the object you need:

- `reddit subreddits get`: Inspect one subreddit. Use this first when you need subreddit metadata, need to confirm the exact subreddit, or want a starting point before deeper scraping.
- `reddit subreddits posts`: Pull the feed for a subreddit. Use this for trend checks, post collection, or monitoring what is getting posted in a community over a timeframe.
- `reddit subreddits search`: Search inside one subreddit. Use this when the user already knows the target community and wants topic-specific matches there.
- `reddit search`: Search across Reddit. Use this for broad discovery, demand research, finding discussions across communities, or identifying which subreddits are active around a topic.
- `reddit posts comments`: Expand a specific post into its comment thread. Use this after finding a promising post URL and you need replies, objections, pain points, or discussion detail.
- `reddit ads search`: Search Reddit ads by topic and optionally narrow by industry, budget, format, placement, or objective. Use this for ad research and competitive intelligence.
- `reddit ads get`: Retrieve one specific ad once you already have an ad ID and want the full ad payload.

## Common workflows

### Explore a subreddit

1. Start with `reddit subreddits get` to confirm the subreddit.
2. Use `reddit subreddits posts` to pull the current feed.
3. Switch to `reddit subreddits search` if the user wants only posts about a particular topic.

Example:

```bash
scrapesocial reddit subreddits get --subreddit AskReddit
scrapesocial reddit subreddits posts --subreddit AskReddit --sort top --timeframe week --trim
scrapesocial reddit subreddits search --subreddit AskReddit --query "first job" --sort top
```

### Discover discussions across Reddit

Use `reddit search` first when the right subreddit is unknown or the task is market research, social listening, or idea validation.

```bash
scrapesocial reddit search --query "email deliverability" --sort top --timeframe month --trim
```

### Go from posts to comments

When a search or subreddit listing returns a relevant post, follow up with `reddit posts comments` on the post URL to inspect sentiment and detailed discussion.

```bash
scrapesocial reddit posts comments --url "https://www.reddit.com/r/..." --trim
```

### Research advertising

Use `reddit ads search` for category-level ad discovery and `reddit ads get` when you want the full details for one returned ad.

```bash
scrapesocial reddit ads search --query "project management" --formats VIDEO --objectives CLICKS
scrapesocial reddit ads get --id <ad-id>
```

## Important operating notes

- Subreddit names are not interchangeable with `r/...` or full URLs. Use the subreddit name expected by the command, for example `AskReddit`.
- `reddit subreddits get` is case-sensitive according to the catalog. If a lookup fails, verify capitalization.
- Use `--trim` when you want smaller, easier-to-process payloads.
- Use returned pagination tokens to continue:
  - `--after` for `reddit subreddits posts` and `reddit search`
  - `--cursor` for `reddit subreddits search` and `reddit posts comments`
- Start broad, then narrow:
  - `reddit search` to find communities and candidate posts
  - `reddit subreddits search` once the target subreddit is known
  - `reddit posts comments` once the exact post is known

## What this skill is good for

- Finding real user discussions about a topic
- Monitoring a specific subreddit
- Pulling comments for qualitative analysis
- Discovering pain points, feature requests, and objections
- Researching Reddit ad creatives and targeting patterns

## What not to use it for

- Posting to Reddit or managing a Reddit account
- Moderation actions
- Reddit API app setup
- Real-time streaming; this CLI is request/response scraping
