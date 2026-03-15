---
name: anysite-content-analytics
description: Track and analyze content performance across Instagram, YouTube, LinkedIn, Twitter/X, and Reddit using anysite MCP server. Measure engagement metrics, analyze post effectiveness, benchmark content strategy, identify top-performing content, and optimize posting strategies. Supports post performance tracking, engagement analysis, content type comparison, and competitive benchmarking. Use when users need to measure content ROI, optimize social strategy, identify viral content patterns, or analyze content engagement across platforms.
---

# anysite Content Analytics

Measure and optimize content performance across social platforms using anysite MCP. Track engagement, identify top performers, and refine your content strategy.

## Overview

- **Track post performance** across Instagram, YouTube, LinkedIn, Twitter/X
- **Analyze engagement metrics** (likes, comments, shares, views)
- **Identify top content** and viral patterns
- **Benchmark against competitors** for strategy insights
- **Optimize posting strategy** based on data

**Coverage**: 80% - Strong for Instagram, YouTube, LinkedIn, Twitter, Reddit

## Supported Platforms

- ✅ **Instagram**: Posts, Reels, likes, comments, engagement rates
- ✅ **YouTube**: Videos, views, likes, comments, watch time indicators
- ✅ **LinkedIn**: Posts, articles, reactions, comments, shares
- ✅ **Twitter/X**: Tweets, retweets, likes, replies
- ✅ **Reddit**: Posts, upvotes, comments, awards

## Quick Start

**Step 1: Collect Content Data**

Platform-specific:
- Instagram: `get_instagram_user_posts(username, count=50)`
- LinkedIn: `get_linkedin_user_posts(urn, count=50)`
- Twitter: `get_twitter_user_posts(user, count=100)`
- YouTube: `get_youtube_channel_videos(channel, count=30)`

**Step 2: Analyze Engagement**

Calculate metrics:
- Engagement rate: (likes + comments + shares) / followers
- Best performing content: Top 10% by engagement
- Content types: Video vs. image vs. text
- Posting frequency: Posts per week

**Step 3: Identify Patterns**

Look for:
- Best posting times (day of week, time)
- Top-performing topics/themes
- Optimal content length
- High-engagement formats

**Step 4: Optimize Strategy**

Based on findings:
- Double down on top content types
- Post more during peak engagement times
- Replicate successful topics
- Adjust content mix

## Common Workflows

### Workflow 1: Instagram Content Audit

**Steps**:

1. **Get All Posts**
```
get_instagram_user_posts(username, count=100)
```

2. **Calculate Metrics**
```
For each post:
- Engagement rate = (likes + comments) / follower_count
- Engagement per hour = engagement / hours_since_posted
- Content type (Reel, carousel, single image, video)
```

3. **Identify Top Performers**
```
Sort by engagement rate
Top 10%: Analyze for common patterns
- Topics/themes
- Visual style
- Caption style and length
- Hashtag strategy
```

4. **Analyze Content Mix**
```
Count by type:
- Reels: X% of posts, Y% of engagement
- Carousels: X% of posts, Y% of engagement
- Single images: X% of posts, Y% of engagement
```

5. **Benchmark Against Competitors**
```
For each competitor:
  get_instagram_user_posts(competitor, count=50)
Compare:
- Posting frequency
- Engagement rates
- Content types
- Top themes
```

**Expected Output**:
- Content performance report
- Top 10 performing posts
- Content type effectiveness
- Posting frequency analysis
- Competitive benchmark

### Workflow 2: LinkedIn Content Strategy Analysis

**Steps**:

1. **Collect Post History**
```
get_linkedin_user_posts(urn, count=100)
```

2. **Categorize Content**
```
Group by type:
- Text-only posts
- Image posts
- Video posts
- Article shares
- LinkedIn articles
- Polls
```

3. **Analyze Engagement by Type**
```
For each content type:
- Average reactions
- Average comments
- Average shares
- Engagement rate
```

4. **Topic Analysis**
```
Extract themes from top posts:
- Industry insights
- Personal stories
- How-to/educational
- Company news
- Thought leadership
```

5. **Posting Timing Analysis**
```
Group posts by:
- Day of week
- Time of day
Calculate average engagement for each group
```

**Expected Output**:
- Best content types for engagement
- Top topics by engagement
- Optimal posting times
- Content frequency recommendations

### Workflow 3: YouTube Channel Performance Analysis

**Steps**:

1. **Get Channel Videos**
```
get_youtube_channel_videos(channel, count=50)
```

2. **Analyze Each Video**
```
For each video:
  get_youtube_video(video_id)

Metrics:
- Views
- Likes/dislikes
- Comments
- View velocity (views per day since upload)
```

3. **Identify Patterns**
```
Analyze top 20% by views:
- Video length
- Titles (keywords, style)
- Thumbnail patterns
- Topics/themes
- Upload timing
```

4. **Engagement Analysis**
```
Check comments:
  get_youtube_video_comments(video_id, count=100)

Analyze:
- Comment quality
- Questions asked
- Sentiment
- Engagement timing
```

5. **Content Mix Optimization**
```
Compare:
- Long-form (>10 min) vs short (<5 min)
- Tutorial vs entertainment vs review
- Series vs one-offs
```

**Expected Output**:
- Video performance rankings
- Optimal video length
- Best topics and formats
- Title and thumbnail insights
- Upload strategy recommendations

## MCP Tools Reference

### Instagram
- `get_instagram_user_posts(user, count)` - Get posts with engagement
- `get_instagram_post(post_id)` - Get detailed post metrics
- `get_instagram_post_likes(post, count)` - Analyze likers
- `get_instagram_post_comments(post, count)` - Get comments

### LinkedIn
- `get_linkedin_user_posts(urn, count)` - Get post history
- `get_linkedin_company_posts(urn, count)` - Company page posts

### Twitter/X
- `get_twitter_user_posts(user, count)` - Get tweets
- `search_twitter_posts(query, count)` - Find trending tweets

### YouTube
- `get_youtube_channel_videos(channel, count)` - All videos
- `get_youtube_video(video)` - Video details and metrics
- `get_youtube_video_comments(video, count)` - Comments

### Reddit
- `reddit_user_posts(username, count)` - User's posts
- `search_reddit_posts(query, count)` - Find popular posts

## Key Metrics

**Engagement Rate**:
- Formula: (Likes + Comments + Shares) / Followers × 100
- Instagram benchmark: 3-6%
- LinkedIn benchmark: 2-5% of connections
- Twitter benchmark: 0.5-1%

**Content Performance Score**:
```
Score = (Engagement Rate × 40) +
        (Comments/Likes Ratio × 30) +
        (Share Rate × 30)
```

**Viral Potential Indicators**:
- Engagement rate >2x average
- High share rate (>5% of engagement)
- Rapid engagement velocity (50% within 24h)
- Quality comments (questions, discussions)

## Output Formats

**Chat Summary**:
- Top 5 performing posts
- Key insights and patterns
- Recommendations for optimization

**CSV Export**:
- Post URL, date, type
- Likes, comments, shares
- Engagement rate
- Performance rank

**JSON Export**:
- Full post data with metadata
- Time-series engagement data
- Historical trends

## Reference Documentation

- **[METRICS_GUIDE.md](references/METRICS_GUIDE.md)** - Detailed metrics definitions, calculation formulas, and benchmarks

---

**Ready to analyze content?** Ask Claude to help you track performance, identify top content, or optimize your posting strategy!
