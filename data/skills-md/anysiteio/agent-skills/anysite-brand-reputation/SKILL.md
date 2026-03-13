---
name: anysite-brand-reputation
description: Monitor brand reputation and sentiment across Twitter/X, Reddit, Instagram, YouTube, and LinkedIn using anysite MCP server. Track brand mentions, analyze customer sentiment, monitor social conversations, identify reputation issues, and measure brand health. Supports social media listening, sentiment analysis, mention tracking, and crisis detection. Use when users need to monitor brand mentions, track customer sentiment, identify reputation risks, analyze brand perception, or measure social media presence and brand health across platforms.
---

# anysite Brand Reputation Monitoring

Monitor and protect your brand reputation across social media platforms. Track mentions, analyze sentiment, and identify issues before they escalate.

## Overview

- **Track brand mentions** across social platforms
- **Analyze sentiment** (positive, negative, neutral)
- **Monitor conversations** about your brand
- **Identify reputation risks** and crisis signals
- **Measure brand health** over time

**Coverage**: 65% - Pivoted from review platforms to social media monitoring; strong for Twitter, Reddit, Instagram, YouTube, LinkedIn

## Supported Platforms

- ✅ **Twitter/X**: Real-time mentions, sentiment, viral content
- ✅ **Reddit**: Community discussions, detailed feedback, sentiment
- ✅ **Instagram**: Visual brand mentions, hashtag tracking, influencer posts
- ✅ **YouTube**: Video mentions, comment sentiment, brand coverage
- ✅ **LinkedIn**: Professional mentions, company updates, B2B sentiment

## Quick Start

**Step 1: Set Up Monitoring**

Define:
- Brand keywords (company name, product names, misspellings)
- Platforms to monitor (Twitter, Reddit, Instagram, etc.)
- Monitoring frequency (real-time, daily, weekly)
- Alert thresholds (negative sentiment, volume spikes)

**Step 2: Search for Mentions**

Platform searches:
```
Twitter: search_twitter_posts(query="brand name", count=100)
Reddit: search_reddit_posts(query="brand name", count=100)
Instagram: search_instagram_posts(query="#brandname", count=100)
LinkedIn: search_linkedin_posts(keywords="brand name", count=50)
```

**Step 3: Analyze Sentiment**

For each mention:
- Classify: Positive, negative, neutral
- Categorize: Complaint, praise, question, general
- Prioritize: Urgency, reach, influence

**Step 4: Take Action**

Based on findings:
- Respond to negative mentions
- Amplify positive feedback
- Address product issues
- Engage with community

## Common Workflows

### Workflow 1: Daily Brand Monitoring

**Scenario**: Monitor brand mentions across all platforms daily

**Steps**:

1. **Search All Platforms**
```
# Twitter (real-time pulse)
search_twitter_posts(query="brand name OR @brandhandle", count=100)
Filter: Last 24 hours

# Reddit (detailed discussions)
search_reddit_posts(query="brand name", count=50)
Filter: Last 24 hours

# Instagram (visual mentions)
search_instagram_posts(query="#brandname OR brand name", count=50)

# LinkedIn (professional mentions)
search_linkedin_posts(keywords="brand name", count=20)

# YouTube (video coverage)
search_youtube_videos(query="brand name review OR brand name unboxing", count=20)
```

2. **Classify Mentions**
```
For each mention:

Sentiment:
- Positive: Praise, recommendation, satisfaction
- Negative: Complaint, criticism, problem
- Neutral: Question, general mention, factual

Category:
- Product feedback
- Customer service issue
- Feature request
- General discussion
- Competitor comparison
```

3. **Prioritize Issues**
```
High Priority:
- Negative + High reach (viral potential)
- Multiple complaints about same issue
- Influencer negative mention
- Legal/safety concerns

Medium Priority:
- Individual complaints
- Feature requests
- Questions
- General feedback

Low Priority:
- Positive mentions
- Neutral discussions
- General brand awareness
```

4. **Generate Daily Report**
```
Summary:
- Total mentions (by platform)
- Sentiment breakdown (% positive/negative/neutral)
- Top issues identified
- Viral/trending mentions
- Recommended actions
```

**Expected Output**:
- Daily mention count: 50-200
- Sentiment distribution
- Top 5 issues to address
- Action items for team

### Workflow 2: Crisis Detection and Management

**Scenario**: Identify and track potential PR crises

**Steps**:

1. **Monitor for Anomalies**
```
Track baseline:
- Average mentions per day
- Average sentiment score
- Typical engagement levels

Alert triggers:
- Mentions >2x baseline
- Negative sentiment >50%
- Viral negative content (high engagement)
```

2. **Deep Dive on Spikes**
```
When alert triggered:

search_twitter_posts(query="brand name", count=500)
→ Identify what's driving spike

search_reddit_posts(query="brand name", count=200)
→ Check community discussions

For viral posts:
  get_twitter_post(post_id) or get_reddit_post(url)
  → Analyze reach and engagement
  → Read comments for context
```

3. **Assess Crisis Severity**
```
Severity factors:
- Volume (how many mentions)
- Velocity (how fast growing)
- Reach (influencer involvement, media coverage)
- Sentiment (how negative)
- Validity (legitimate issue vs. misunderstanding)
```

4. **Track Crisis Evolution**
```
Hourly monitoring:
- Mention volume trend
- Sentiment shifts
- Platform spread
- Media pickup
- Official response impact
```

5. **Measure Resolution**
```
Track until:
- Volume returns to baseline
- Sentiment improves
- No new negative mentions for 24-48h
```

**Expected Output**:
- Crisis timeline
- Mention volume graph
- Sentiment tracking
- Key influencers/posts
- Response effectiveness

### Workflow 3: Competitive Reputation Benchmarking

**Scenario**: Compare brand sentiment vs. competitors

**Steps**:

1. **Define Competitors**
```
List 3-5 main competitors
```

2. **Gather Mentions for All**
```
For brand + each competitor:
  search_twitter_posts(query=brand, count=200)
  search_reddit_posts(query=brand, count=100)
  search_linkedin_posts(keywords=brand, count=50)
```

3. **Calculate Brand Health Scores**
```
For each brand:

Mention Volume: Total mentions
Sentiment Score: (Positive - Negative) / Total
Engagement Rate: Avg engagement per mention
Share of Voice: Your mentions / Total category mentions
```

4. **Analyze Strengths/Weaknesses**
```
Compare:
- What are competitors praised for?
- What are competitors criticized for?
- Where do we excel?
- Where do we fall short?
```

5. **Identify Opportunities**
```
Look for:
- Unmet customer needs (complaints about competitors)
- Messaging gaps (what they're not saying)
- Product differentiation opportunities
- Customer service advantages
```

**Expected Output**:
- Competitive sentiment matrix
- Brand health scores comparison
- Strength/weakness analysis
- Strategic opportunities

## MCP Tools Reference

### Twitter/X
- `search_twitter_posts(query, count)` - Find brand mentions
- `get_twitter_user(user)` - Check brand profile stats
- `get_twitter_user_posts(user, count)` - Monitor brand account

### Reddit
- `search_reddit_posts(query, subreddit, count)` - Find discussions
- `get_reddit_post(url)` - Get post details and sentiment
- `get_reddit_post_comments(url)` - Deep dive on discussions

### Instagram
- `search_instagram_posts(query, count)` - Find visual mentions
- `get_instagram_post(post_id)` - Analyze mention engagement
- `get_instagram_post_comments(post, count)` - Read feedback

### YouTube
- `search_youtube_videos(query, count)` - Find video mentions
- `get_youtube_video(video)` - Get video details
- `get_youtube_video_comments(video, count)` - Analyze sentiment

### LinkedIn
- `search_linkedin_posts(keywords, count)` - Professional mentions
- `get_linkedin_company_posts(urn, count)` - Monitor own posts

## Sentiment Analysis Framework

**Manual Sentiment Classification**:

**Positive Indicators**:
- "Love", "great", "amazing", "best"
- Recommendations ("highly recommend")
- Repeat purchase ("buying again")
- Comparisons ("better than X")

**Negative Indicators**:
- "Disappointed", "worst", "terrible", "awful"
- Problems ("doesn't work", "broken")
- Comparisons ("X is better")
- Demands ("need refund", "fix this")

**Neutral Indicators**:
- Questions without sentiment
- Factual statements
- General mentions
- Informational content

**Sentiment Score**:
```
Score = (Positive mentions - Negative mentions) / Total mentions × 100

+50 to +100: Excellent
+20 to +49: Good
-19 to +19: Neutral/Mixed
-20 to -49: Poor
-50 to -100: Critical
```

## Monitoring Metrics

**Volume Metrics**:
- Total mentions per day/week/month
- Mentions by platform
- Trend over time

**Sentiment Metrics**:
- Sentiment distribution (% positive/negative/neutral)
- Sentiment score (net promoter style)
- Sentiment trend over time

**Engagement Metrics**:
- Average likes/shares per mention
- Viral mentions (>1000 engagements)
- Influencer mentions

**Issue Tracking**:
- Top complaints (by frequency)
- Product/service issues mentioned
- Feature requests
- Customer service mentions

## Output Formats

**Chat Summary**:
- Daily mention highlights
- Sentiment overview
- Top issues identified
- Recommended actions

**CSV Export**:
- Mention list with sentiment
- Platform, date, reach
- Issue categorization

**JSON Export**:
- Complete mention data
- Time-series sentiment
- Engagement metrics

## Reference Documentation

- **[MONITORING_GUIDE.md](references/MONITORING_GUIDE.md)** - Best practices for brand monitoring, crisis response protocols, and sentiment analysis techniques

---

**Ready to monitor your brand?** Ask Claude to help you track mentions, analyze sentiment, or identify reputation risks across social platforms!
