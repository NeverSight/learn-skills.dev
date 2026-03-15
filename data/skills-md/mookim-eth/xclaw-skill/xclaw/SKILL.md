---
name: xclaw
description: XClaw Intelligence Skill. Provides real-time trending tweets, KOL deep analysis, live user crawling, profile history, and social relation tracking.
allowed-tools: Bash(node:*) Read Write
metadata:
  {
    "openclaw": { "requires": { "env": ["XCLAW_API_KEY", "CRYPTOHUNT_API_KEY"] } },
    "homepage": "https://pro.xclaw.info",
    "codelink": "https://github.com/mookim-eth/xclaw-skill"
  }
---

# Skill: XClaw Intelligence 🚀

XClaw is the premier intelligence layer for OpenClaw creators, providing real-time social data and insights from the XClaw engine.

## Prerequisites
- **API Key Required**: Set `XCLAW_API_KEY` in your environment. (**Note**: `CRYPTOHUNT_API_KEY` is supported as a **legacy** option but will be **retired soon**. Please migrate to `XCLAW_API_KEY` as soon as possible.)
- **Get your Key**: Visit [apidashboard.xclaw.info](https://apidashboard.xclaw.info) and **login with Twitter** to claim **50 free credits**.
- **Official API Docs**: Detailed endpoint documentation can be found at [pro.xclaw.info](https://pro.xclaw.info).
- **Stay Updated**: Follow our Twitter **[@xclawlab](https://x.com/xclawlab)** for the latest updates.

## Core Capabilities

### 1. Trending Discovery (`xclaw_hot`)
- **Action**: Fetch the top performing tweets in the last 1/4/24 hours.
- **Filtering**: Support for region (`cn`/`global`) and tags (e.g., `AI`, `meme`).

### 2. Recent Tweets (`xclaw_tweets`)
- **Action**: Fetches latest tweets with intelligent filtering. 
- **Default**: Includes Original + Quote + Retweets, excludes Replies. (Slim mode by default).
- **Options**:
  - Use `--full` to include raw text and HTML content.
  - Use `--verbose` to include reply tweets.
- **Count**: Specify number of tweets (e.g., `xclaw tweets elonmusk 20`). 
- **Compatibility**: Legacy aliases `xclaw_analyze` / `xclaw_crawl` are supported.

### 3. Ghost Analysis (`xclaw_ghost`)
- **Action**: Sniff out tweets that have been **deleted** by a specific user.

### 4. Identity Traces (`xclaw_traces`)
- **Action**: Retrieve history of profile changes (Bio, Avatar, Name) for a specific user to track identity evolution.

### 5. Social Pulse (`xclaw_social`)
- **Action**: Track recent **Follow** and **Unfollow** actions of a specific user.

### 6. Account Deep Rank (`xclaw_rank`)
- **Action**: Comprehensive account analysis including rankings, ability model, soul score, and interest tags.

### 7. Tweet Deep Dive (`xclaw_detail`)
- **Action**: Fetches full content, metrics, and thread data for a specific tweet.

### 8. Smart Content Ideation (`xclaw_draft`)
- **Action**: Fetch viral topics tailored by region and tag to generate high-conversion tweet drafts with original links.

## User Commands for Agent
- `xclaw find hot`: Get the last 4h of Chinese crypto hot tweets.
- `xclaw tweets <username>`: Get recent slimmed tweets from @username.
- `xclaw ghost <username>`: See what @username tried to delete.
- `xclaw traces <username>`: Check profile history.
- `xclaw social <username>`: See who @username recently followed or unfollowed.
- `xclaw rank <username>`: Get soul score, rankings and ability model.
- `xclaw detail <URL_or_ID>`: Fetch all details and stats for a specific tweet.
- `xclaw draft`: Automatically fetch viral hooks and suggest 3 tweet versions.

---
*XClaw Intelligence - Data for Creators. Follow [@xclawlab](https://x.com/xclawlab) for updates.*

Code link: https://github.com/mookim-eth/xclaw-skill
