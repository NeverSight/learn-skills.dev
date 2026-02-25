---
name: anysite-trend-analysis
description: Discover and track emerging trends across Twitter/X, Reddit, YouTube, LinkedIn, and Instagram using anysite MCP server. Identify viral content, monitor topic momentum, detect trending hashtags, analyze search patterns, and track industry shifts. Supports multi-platform trend detection, sentiment analysis, and momentum tracking. Use when users need to identify emerging trends, track viral content, monitor market shifts, discover trending topics, or analyze social media conversations for strategic insights.
---

# anysite Trend Analysis

Discover emerging trends and track viral content across social platforms using anysite MCP. Identify what's gaining momentum before it peaks.

## Overview

- **Detect emerging trends** across multiple platforms
- **Track viral content** and identify breakout topics
- **Monitor hashtag performance** and trending keywords
- **Analyze topic momentum** and growth patterns
- **Identify market shifts** through social listening

**Coverage**: 75% - Good for Twitter, Reddit, YouTube, LinkedIn, Instagram

## Supported Platforms

- ✅ **Twitter/X**: Trending topics, viral tweets, hashtag tracking
- ✅ **Reddit**: Trending posts, subreddit activity, upvote velocity
- ✅ **YouTube**: Trending videos, search trends, rising channels
- ✅ **LinkedIn**: Professional trends, industry discussions
- ✅ **Instagram**: Trending hashtags, viral content

## Quick Start

**Step 1: Search for Trending Content**

By platform:
- Twitter: `search_twitter_posts(query, count)` sorted by engagement
- Reddit: `search_reddit_posts(query, count)` sorted by upvotes
- YouTube: `search_youtube_videos(query, count)` by recent
- LinkedIn: `search_linkedin_posts(keywords, count)`
- Instagram: `search_instagram_posts(query, count)`

**Step 2: Analyze Momentum**

Check indicators:
- Engagement velocity (growth rate)
- Cross-platform presence
- Comment volume and sentiment
- Share/retweet patterns

**Step 3: Track Over Time**

Monitor changes:
- Daily engagement growth
- New platform adoption
- Mainstream vs. niche spread
- Peak timing prediction

**Step 4: Report Insights**

Deliver:
- Trending topics list
- Momentum indicators
- Strategic recommendations
- Early warnings or opportunities

## Common Workflows

### Workflow 1: Multi-Platform Trend Detection

**Scenario**: Identify what's trending in tech/AI space

**Steps**:

1. **Search Across Platforms**
```
# Twitter
search_twitter_posts(query="AI OR artificial intelligence", count=100)
Filter for: Posted within 24-48h, high engagement

# Reddit
search_reddit_posts(query="artificial intelligence", count=100)
Filter: r/technology, r/MachineLearning, r/singularity

# YouTube
search_youtube_videos(query="AI news", count=50)
Filter: Published this week, views >10k

# LinkedIn
search_linkedin_posts(keywords="artificial intelligence", count=50)
Filter: High engagement, recent
```

2. **Extract Common Themes**
```
Analyze content for recurring:
- Keywords and phrases
- Company/product mentions
- Events or announcements
- Questions or concerns
```

3. **Calculate Trend Score**
```
For each theme:
- Platform count (how many platforms)
- Total engagement
- Growth velocity
- Sentiment distribution
```

4. **Identify Breakout Trends**
```
Trends with:
- Presence on 3+ platforms
- Engagement growing >50% daily
- Positive or controversial sentiment
- Coverage by influencers/media
```

**Expected Output**:
- Top 5-10 trending themes
- Platform-by-platform breakdown
- Momentum indicators
- Strategic implications

### Workflow 2: Hashtag Performance Tracking

**Scenario**: Monitor hashtag growth and adoption

**Steps**:

1. **Search by Hashtag**
```
# Instagram
search_instagram_posts(query="#sustainability", count=100)
Group by: Last 24h, last week, last month

# Twitter
search_twitter_posts(query="#sustainability", count=100)
Track tweet volume over time

# LinkedIn
search_linkedin_posts(keywords="sustainability", count=50)
Check professional adoption
```

2. **Calculate Velocity**
```
Hashtag velocity:
- Posts in last 24h vs. previous 24h
- Engagement rate change
- New accounts using hashtag
- Geographic spread
```

3. **Analyze Content Evolution**
```
Compare early vs. recent posts:
- Topic shifts
- Audience changes
- Influencer involvement
- Commercial adoption
```

4. **Predict Peak**
```
Based on growth curve:
- Early stage (accelerating)
- Peak stage (plateauing)
- Decline stage (slowing)
```

**Expected Output**:
- Hashtag performance report
- Growth trajectory
- Peak timing estimate
- Strategic recommendations

### Workflow 3: Reddit Trend Mining

**Scenario**: Find emerging discussions in specific communities

**Steps**:

1. **Search Target Subreddits**
```
search_reddit_posts(
  query="",
  subreddit="technology"
)
→ Get top posts from last week
```

2. **Analyze Post Momentum**
```
For each post:
  get_reddit_post(post_url)
  get_reddit_post_comments(post_url)

Calculate:
- Upvotes per hour
- Comment velocity
- Award count
- Controversial score
```

3. **Extract Discussion Themes**
```
From high-momentum posts:
- What problems are discussed?
- What solutions are proposed?
- What companies/products mentioned?
- What sentiment (positive, negative, concerned)?
```

4. **Track Cross-Pollination**
```
Check if trending Reddit topics appear on:
- Twitter (mainstream awareness)
- LinkedIn (professional discussion)
- YouTube (explainer content)
```

**Expected Output**:
- Top Reddit trends
- Community sentiment
- Mainstream potential
- Early mover opportunities

## MCP Tools Reference

### Twitter/X
- `search_twitter_posts(query, count)` - Find tweets, filter by engagement
- `get_twitter_user(user)` - Check influencer adoption

### Reddit
- `search_reddit_posts(query, subreddit, count)` - Find discussions
- `get_reddit_post(url)` - Get post details and momentum
- `get_reddit_post_comments(url)` - Analyze discussion depth

### YouTube
- `search_youtube_videos(query, count)` - Find trending videos
- `get_youtube_video(video)` - Track view velocity
- `get_youtube_video_comments(video, count)` - Gauge interest

### LinkedIn
- `search_linkedin_posts(keywords, count)` - Professional trends
- `get_linkedin_company_posts(urn, count)` - Corporate adoption

### Instagram
- `search_instagram_posts(query, count)` - Hashtag trends
- `get_instagram_post(post_id)` - Engagement metrics

## Trend Identification Framework

**Trend Stages**:

1. **Emergence** (0-20% awareness)
   - Niche communities discussing
   - Low but accelerating engagement
   - Early adopters experimenting
   - Action: Monitor closely, prepare strategy

2. **Growth** (20-50% awareness)
   - Crossing into mainstream platforms
   - Rapid engagement growth
   - Influencer adoption
   - Action: Create content, engage actively

3. **Peak** (50-80% awareness)
   - Maximum visibility
   - Slowing growth rate
   - Saturation approaching
   - Action: Maximize presence before decline

4. **Decline** (80-100% awareness)
   - Engagement decreasing
   - Moving to "background noise"
   - New trends emerging
   - Action: Shift focus to next trend

**Momentum Indicators**:
- **Volume**: Mentions per day
- **Velocity**: Growth rate (% change)
- **Reach**: Unique accounts discussing
- **Spread**: Number of platforms
- **Sentiment**: Positive/negative ratio
- **Influence**: Key accounts involved

## Output Formats

**Chat Summary**:
- Top 5 trends with momentum scores
- Platform breakdown
- Strategic recommendations

**CSV Export**:
- Trend name, platforms, volume
- Growth rate, sentiment
- Key influencers mentioning

**JSON Export**:
- Complete trend data
- Time-series metrics
- Cross-platform correlations

## Reference Documentation

- **[SOCIAL_MONITORING.md](references/SOCIAL_MONITORING.md)** - Social listening techniques, monitoring strategies, and trend prediction methods

---

**Ready to discover trends?** Ask Claude to help you identify emerging topics, track viral content, or monitor market shifts across social platforms!
