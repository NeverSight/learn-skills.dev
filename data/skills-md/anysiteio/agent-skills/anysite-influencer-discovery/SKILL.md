---
name: anysite-influencer-discovery
description: Discover and analyze influencers across Instagram, Twitter/X, LinkedIn, YouTube, and Reddit using anysite MCP server. Find content creators by niche, analyze engagement metrics, evaluate audience quality, track influencer activity, and identify partnership opportunities. Supports multi-platform influencer search, profile enrichment, follower analysis, and engagement tracking. Use when users need to find brand ambassadors, research content creators, identify thought leaders, build influencer lists, or evaluate influencer partnerships for marketing campaigns.
---

# anysite Influencer Discovery

Find and analyze influencers across social platforms using anysite MCP. Discover content creators, evaluate their reach and engagement, and identify partnership opportunities.

## Overview

- **Discover influencers** across Instagram, Twitter, LinkedIn, YouTube
- **Analyze engagement** and audience quality
- **Track activity** and content patterns
- **Evaluate partnership fit** based on niche and metrics
- **Build influencer lists** with contact information

**Coverage**: 85% - Excellent for Instagram, Twitter, LinkedIn, YouTube influencers.

## Supported Platforms

- ✅ **Instagram**: Profile stats, posts, followers, engagement, Reels
- ✅ **Twitter/X**: User search, followers, tweets, engagement
- ✅ **LinkedIn**: B2B influencers, thought leaders, professional content
- ✅ **YouTube**: Channel search, subscribers, views, video performance
- ✅ **Reddit**: Community influencers, karma, post quality

## Quick Start

**Step 1: Search for Influencers**

By platform:
- Instagram: `search_instagram_posts` with niche keywords + hashtags
- Twitter: `search_twitter_users` with niche keywords
- LinkedIn: `search_linkedin_users` with industry + "thought leader"
- YouTube: `search_youtube_videos` with niche, then analyze channels

**Step 2: Analyze Profiles**

Get detailed metrics:
- Instagram: `get_instagram_user` → followers, posts, engagement rate
- Twitter: `get_twitter_user` → followers, tweet frequency
- YouTube: `get_youtube_channel_videos` → subscribers, views, growth
- LinkedIn: `get_linkedin_profile` → connections, post engagement

**Step 3: Evaluate Engagement**

Check engagement quality:
- Post likes, comments, shares
- Engagement rate (engagement / followers)
- Audience authenticity (comment quality)
- Content consistency (posts per week)

**Step 4: Build Influencer List**

Export with:
- Name, handle, platform
- Follower count, engagement rate
- Niche/topics, content type
- Contact info (if available)
- Partnership fit score

## Common Workflows

### Workflow 1: Instagram Influencer Discovery

**Scenario**: Find Instagram influencers in sustainable fashion (10k-100k followers)

**Steps**:

1. **Search by Hashtag/Keywords**
```
search_instagram_posts(
  query="sustainable fashion OR eco friendly fashion",
  count=100
)
→ Extract unique user handles from results
```

2. **Analyze Each Creator**
```
For each unique handle:
  get_instagram_user(username)
  → Follower count, bio, profile type

Filter for:
- 10k-100k followers
- Business/Creator account
- Bio mentioning sustainability
```

3. **Evaluate Content**
```
For qualified creators:
  get_instagram_user_posts(username, count=30)

Analyze:
- Post frequency (consistency)
- Engagement rate per post
- Content quality and style
- Brand partnerships visible
```

4. **Check Audience Quality**
```
get_instagram_post_likes(post_id, count=100)
get_instagram_post_comments(post_id, count=50)

Look for:
- Real comments (not just emojis)
- Engaged community (questions, discussions)
- Geographic relevance
```

5. **Get Contact Information**
```
From Instagram bio:
- Email addresses
- Website links

If LinkedIn mentioned:
  search_linkedin_users(first_name, last_name)
  get_linkedin_profile(user)
```

**Expected Output**:
- 20-40 qualified influencers
- Engagement metrics for each
- Contact information for 60-70%
- Partnership fit scores

### Workflow 2: LinkedIn Thought Leader Identification

**Scenario**: Find B2B thought leaders in SaaS/sales

**Steps**:

1. **Search for Active Posters**
```
search_linkedin_users(
  keywords="SaaS sales thought leader",
  title="VP Sales OR Head of Sales OR Chief Revenue Officer",
  count=100
)
```

2. **Analyze Post Activity**
```
For each candidate:
  get_linkedin_user_posts(urn, count=50)

Filter for:
- Posts 2-3x per week minimum
- High engagement (100+ reactions)
- Original content (not just shares)
```

3. **Evaluate Influence**
```
Check post engagement:
- Average reactions per post
- Comment quality and quantity
- Share count
- Follower growth signals
```

4. **Assess Content Quality**
```
Review posts for:
- Expertise demonstration
- Original insights
- Engagement with comments
- Consistency of messaging
```

**Expected Output**:
- 15-25 active thought leaders
- Content themes and topics
- Engagement metrics
- Partnership opportunities (guest posts, quotes, etc.)

### Workflow 3: YouTube Creator Research

**Scenario**: Find YouTube creators in tech reviews

**Steps**:

1. **Search for Niche Content**
```
search_youtube_videos(
  query="tech review 2026",
  count=100
)
→ Extract unique channel names
```

2. **Analyze Channels**
```
For each channel:
  get_youtube_channel_videos(channel, count=30)

Check:
- Subscriber count
- Upload frequency
- Average views per video
- Video length (long-form vs shorts)
```

3. **Evaluate Video Performance**
```
For top videos:
  get_youtube_video(video_id)

Metrics:
- View count
- Like/dislike ratio
- Comments count
- Watch time signals (retention)
```

4. **Analyze Audience Engagement**
```
get_youtube_video_comments(video_id, count=100)

Look for:
- Active community
- Technical discussions
- Purchase decisions influenced
```

**Expected Output**:
- 10-20 relevant channels
- Subscriber and view metrics
- Engagement analysis
- Partnership fit assessment

## MCP Tools Reference

### Instagram
- `search_instagram_posts` - Find posts by keywords/hashtags
- `get_instagram_user` - Get profile with followers, bio
- `get_instagram_user_posts` - Get recent posts with engagement
- `get_instagram_post_likes` - Check audience authenticity
- `get_instagram_post_comments` - Analyze engagement quality
- `get_instagram_user_friendships` - Get followers list (for analysis)

### Twitter/X
- `search_twitter_users` - Find users by keywords/bio
- `get_twitter_user` - Get profile with followers, tweets
- `get_twitter_user_posts` - Get recent tweets with engagement
- `search_twitter_posts` - Find influential tweets in niche

### LinkedIn
- `search_linkedin_users` - Find professionals by keywords/title
- `get_linkedin_profile` - Get complete profile
- `get_linkedin_user_posts` - Get post history and engagement
- `get_linkedin_user_skills` - Verify expertise
- `get_linkedin_user_connections` - Network size (for own account)

### YouTube
- `search_youtube_videos` - Find videos by keywords
- `get_youtube_channel_videos` - Get all videos from channel
- `get_youtube_video` - Get video metrics (views, likes)
- `get_youtube_video_comments` - Analyze audience engagement

### Reddit
- `search_reddit_posts` - Find influential posts in subreddits
- `reddit_user_posts` - Get user's post history
- `reddit_user_comments` - Analyze community engagement

## Output Formats

**Chat Summary**:
- Top 10 influencers with key metrics
- Engagement rate comparison
- Partnership recommendations
- Contact information found

**CSV Export**:
- Influencer name, handle, platform
- Followers, engagement rate
- Niche, content type
- Email, website
- Fit score (1-100)

**JSON Export**:
- Complete profile data
- All posts with engagement
- Audience demographics (if available)
- Historical metrics

## Influencer Evaluation Framework

### Reach Metrics
- **Followers**: Total audience size
- **Views**: Average content views
- **Growth**: Follower growth rate

### Engagement Metrics
- **Rate**: Engagement / Followers
- **Quality**: Comment depth and relevance
- **Consistency**: Regular engagement patterns

### Authenticity Indicators
- **Audience Quality**: Real vs. fake followers
- **Comment Quality**: Meaningful discussions
- **Growth Pattern**: Organic vs. purchased
- **Engagement Distribution**: Consistent vs. spiky

### Content Quality
- **Production Value**: Visual/audio quality
- **Originality**: Unique vs. repurposed
- **Consistency**: Regular posting schedule
- **Niche Alignment**: On-brand content

### Partnership Fit
- **Audience Overlap**: Match with target market
- **Brand Alignment**: Values and messaging
- **Professionalism**: Past partnerships, disclosure
- **Availability**: Contact information, responsiveness

## Advanced Features

### Micro-Influencer Strategy

Focus on 10k-50k followers for higher engagement:
```
Benefits:
- Higher engagement rates (5-10% vs. 1-3%)
- More authentic audience connections
- Lower partnership costs
- Niche expertise

Discovery approach:
- Use hashtag searches
- Analyze engagement vs. reach
- Prioritize niche relevance over size
```

### Multi-Platform Presence Analysis

Identify influencers active across platforms:
```
1. Find on Instagram/Twitter
2. Search LinkedIn for professional presence
3. Check for YouTube channel
4. Look for website/blog (parse_webpage)

Benefits:
- Multiple touchpoints
- Diverse content formats
- Professional credibility
- Larger total reach
```

### Audience Demographics Research

Analyze who follows the influencer:
```
Instagram:
- get_instagram_user_friendships(followers, count=100)
- Analyze follower profiles for patterns

LinkedIn:
- Check who engages with posts
- Identify follower job titles/industries

YouTube:
- Analyze comment demographics
- Check subscriber locations (if available)
```

## Reference Documentation

- **[DISCOVERY_CRITERIA.md](references/DISCOVERY_CRITERIA.md)** - Influencer evaluation criteria, scoring frameworks, and niche identification strategies

## Troubleshooting

**No Influencers Found**:
- Broaden search keywords
- Try multiple hashtags
- Search across multiple platforms
- Reduce minimum follower requirements

**Low Engagement Rates**:
- Filter for engagement rate > 2-3%
- Focus on micro-influencers (smaller = higher engagement)
- Check for bot followers (sudden spikes)

**No Contact Information**:
- Check bio for email/website
- Look for LinkedIn profile
- Try website domain (parse_webpage)
- Search for media kit or press page

---

**Ready to discover influencers?** Ask Claude to help you find content creators, analyze engagement, or build influencer lists for your marketing campaigns!
