---
name: anysite-audience-analysis
description: Analyze audience demographics, engagement patterns, and follower behavior across Instagram, YouTube, and LinkedIn using anysite MCP server. Understand who engages with content, track audience growth, analyze follower quality, identify engagement patterns, and profile audience characteristics. Supports Instagram audience analysis, YouTube subscriber research, and LinkedIn connection profiling. Use when users need to understand target audiences, validate influencer audiences, analyze follower demographics, track engagement patterns, or optimize content for specific audience segments.
---

# anysite Audience Analysis

Understand your audience through demographic analysis, engagement patterns, and follower behavior across Instagram, YouTube, and LinkedIn.

## Overview

- **Analyze follower demographics** and characteristics
- **Track engagement patterns** and behavior
- **Evaluate audience quality** and authenticity
- **Identify content preferences** by audience segment
- **Optimize targeting** based on audience insights

**Coverage**: 60% - Focused on Instagram, YouTube, LinkedIn

## Supported Platforms

- ✅ **Instagram**: Follower analysis, engagement patterns, audience location
- ✅ **YouTube**: Subscriber insights, comment demographics, viewer behavior
- ✅ **LinkedIn**: Connection analysis, professional demographics, engagement

## Quick Start

**Step 1: Identify Audience Source**

Choose platform:
- Instagram: `get_instagram_user` + `get_instagram_user_friendships`
- YouTube: `get_youtube_channel_videos` + comment analysis
- LinkedIn: `get_linkedin_user_posts` + engagement analysis

**Step 2: Collect Audience Data**

Gather:
- Follower/subscriber counts
- Engagement metrics
- Demographics (from profiles)
- Behavior patterns

**Step 3: Analyze Patterns**

Look for:
- Audience segments
- Engagement drivers
- Content preferences
- Peak activity times

**Step 4: Generate Insights**

Deliver:
- Audience profile summary
- Engagement patterns
- Content recommendations
- Targeting suggestions

## Common Workflows

### Workflow 1: Instagram Audience Analysis

**Steps**:

1. **Get Profile Overview**
```
get_instagram_user(username)
→ Follower count, post count, bio
```

2. **Analyze Followers** (sample)
```
get_instagram_user_friendships(
  user=username,
  type="followers",
  count=100
)

For each follower (sample):
- Profile type (personal, business, creator)
- Bio indicators (interests, location)
- Follower count (influence level)
```

3. **Engagement Pattern Analysis**
```
get_instagram_user_posts(username, count=50)

For each post:
  get_instagram_post_likes(post_id, count=100)
  get_instagram_post_comments(post_id, count=50)

Analyze:
- Who engages most (power users)
- When engagement happens (timing)
- What content drives engagement
- Comment quality and topics
```

4. **Audience Segmentation**
```
Group followers by:
- Engagement level (active, passive, ghost)
- Interests (from bios)
- Location (from profiles)
- Influence (follower counts)
```

**Expected Output**:
- Audience demographics summary
- Engagement patterns
- Top engaged followers
- Content preferences

### Workflow 2: YouTube Audience Insights

**Steps**:

1. **Channel Overview**
```
get_youtube_channel_videos(channel, count=50)

Aggregate:
- Total views
- Subscriber milestones
- Content mix
```

2. **Viewer Engagement Analysis**
```
For recent videos:
  get_youtube_video(video_id)
  → Views, likes, comments

  get_youtube_video_comments(video_id, count=200)
  → Analyze commenter patterns
```

3. **Audience Demographics from Comments**
```
From comments analyze:
- Questions asked (knowledge level)
- Topics discussed (interests)
- Language and tone
- Technical depth
```

4. **Content Performance by Audience**
```
Correlate:
- High-view videos → audience interests
- High-comment videos → engagement topics
- High-like videos → quality indicators
```

**Expected Output**:
- Viewer interest profile
- Engagement drivers
- Content optimization insights
- Audience knowledge level

### Workflow 3: LinkedIn Audience Profiling

**Steps**:

1. **Get Post History**
```
get_linkedin_user_posts(urn, count=50)
```

2. **Analyze Engagement**
```
For each post:
- Reaction count and types
- Comment depth
- Share count
- Post reach indicators
```

3. **Profile Engagers** (if accessible)
```
From reactions/comments:
- Job titles
- Industries
- Companies
- Seniority levels
```

4. **Content-Audience Mapping**
```
Correlate:
- Which topics get most engagement
- Which formats perform best
- Which audiences engage with what
- When different audiences are active
```

**Expected Output**:
- Professional audience profile
- Engagement patterns by topic
- Content-audience fit analysis
- Posting optimization recommendations

## MCP Tools Reference

### Instagram
- `get_instagram_user` - Profile stats
- `get_instagram_user_friendships` - Follower/following lists
- `get_instagram_user_posts` - Post history
- `get_instagram_post_likes` - Who liked posts
- `get_instagram_post_comments` - Comment analysis

### YouTube
- `get_youtube_channel_videos` - Channel content
- `get_youtube_video` - Video metrics
- `get_youtube_video_comments` - Audience engagement

### LinkedIn
- `get_linkedin_user_posts` - Post history
- `get_linkedin_profile` - Profile insights

## Audience Analysis Framework

**Demographic Analysis**:
```
- Age range (inferred from profiles)
- Location (from bio/profiles)
- Interests (from bio keywords)
- Professional level (LinkedIn titles)
```

**Behavioral Analysis**:
```
- Engagement frequency
- Content preferences
- Peak activity times
- Interaction patterns
```

**Quality Metrics**:
```
- Real vs. fake followers
- Engagement authenticity
- Audience overlap
- Influence distribution
```

## Output Formats

**Chat Summary**:
- Audience profile highlights
- Key engagement patterns
- Content recommendations
- Strategic insights

**CSV Export**:
- Follower sample data
- Engagement metrics
- Segment distribution

**JSON Export**:
- Complete audience data
- Engagement time series
- Segmentation details

## Reference Documentation

- **[PLATFORM_COVERAGE.md](references/PLATFORM_COVERAGE.md)** - Platform-specific audience analysis capabilities
- **[TOOL_MAPPING.md](references/TOOL_MAPPING.md)** - Mapping analysis needs to MCP tools

---

**Ready to understand your audience?** Ask Claude to help you analyze followers, track engagement patterns, or profile audience characteristics!
