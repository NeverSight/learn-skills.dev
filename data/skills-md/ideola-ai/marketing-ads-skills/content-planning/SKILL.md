---
name: content-planning
description: Create content calendar and organize tasks in ClickUp for social media campaigns. Use when user asks to create content plan, content calendar, schedule posts, or organize content tasks. Triggers on - "content plan", "jadwal konten", "content calendar", "/content-plan" command, or requests to schedule/organize social media content with tasks.
---

# Content Calendar & Task Planning

## Overview

This skill creates structured content calendars based on brief outputs and organizes tasks in ClickUp for execution. It transforms strategic briefs into actionable content schedules with clear deliverables.

## Marketing OS Workflow Position

```
brand-voice → content-brief → content-planning → content-creation
                                          ↓
                                        marketing-campaign
                                          ↓
                                          ads-audit
```

**This skill is THIRD** - Plan content after creating brief, before creating assets.

**Input from:**
- `/brand-voice` - Tone and style guidelines
- `/content-brief` - Audience, angles, platforms, visual direction

**Output to:**
- `/content-creation` - Content queue becomes input for asset creation

## Workflow

### Step 1: Gather Required Context

Before creating a content plan, ensure you have these inputs:

**From Brief (if available):**
- Content angles and key messages
- Platform strategy
- Target audience
- Visual direction

**Additional Information Needed:**
- Campaign duration (1 week, 2 weeks, 1 month, etc.)
- Posting frequency per platform
- Start date of campaign
- Whether to create ClickUp tasks (yes/no)

**Ask if not provided:**
1. Berapa lama durasi campaign yang mau direncanakan?
2. Seberapa sering posting per platform per minggu?
3. Kapan campaign mau mulai?
4. Mau buat ClickUp tasks juga?

### Step 2: Define Content Pillars

Based on the brief angles or general content strategy, define 3-5 content pillars:

**Content Pillar Framework:**

| Pillar Type | Description | Example Topics |
|-------------|-------------|----------------|
| **Educational** | Teach audience something | Tips, tutorials, how-tos, myth-busting |
| **Entertainment** | Engage and entertain | Trends, humor, behind-the-scenes |
| **Inspiration** | Motivate or inspire | Quotes, success stories, transformations |
| **Promotional** | Showcase products/services | Features, benefits, offers, launches |
| **Community** | Build connection | UGC, spotlights, conversations, Q&A |
| **Social Proof** | Build credibility | Testimonials, reviews, case studies, results |

**Output Format:**
```markdown
## Content Pillars

1. **[Pillar Name]** - [Brief description]
   - Focus: [What type of content]
   - Frequency: [X posts per week]

2. **[Pillar Name]** - [Brief description]
   - Focus: [What type of content]
   - Frequency: [X posts per week]
```

### Step 3: Create Content Calendar

Build a weekly content structure that can be replicated:

**Weekly Structure Template:**

| Day | Platform | Content Type | Pillar | Topic |
|-----|----------|--------------|--------|-------|
| Monday | Instagram | Carousel | Educational | [Topic from brief angle] |
| Monday | TikTok | Video | Entertainment | [Trending format + brand twist] |
| Tuesday | LinkedIn | Static | Promotional | [Product/service feature] |
| Wednesday | Instagram | Reel | Behind-the-scenes | [Team/process content] |
| Thursday | TikTok | Video | Educational | [Quick tip format] |
| Friday | Instagram Stories | Interactive | Community | [Poll, Q&A, or quiz] |
| etc. | | | | |

**Calendar Format:**
```markdown
## Content Calendar

### Week 1: [Dates]

#### Monday, [Date]
- **Instagram (9:00 AM)** - Carousel - [Pillar] - [Topic]
- **TikTok (12:00 PM)** - Video - [Pillar] - [Topic]

#### Tuesday, [Date]
- **LinkedIn (8:00 AM)** - Static Post - [Pillar] - [Topic]
- **Instagram (3:00 PM)** - Story - [Pillar] - [Topic]

[Continue for all days...]
```

### Step 4: Build Content Queue

Create detailed content queue for production:

**Content Queue Format:**
```markdown
## Content Queue

| ID | Platform | Format | Pillar | Topic | Key Message | CTA | Due Date | Status |
|----|----------|--------|--------|-------|-------------|-----|----------|--------|
| C001 | Instagram | Carousel | Educational | [Topic] | [Key message] | [CTA] | [Date] | Pending |
| C002 | TikTok | Video | Entertainment | [Topic] | [Key message] | Follow | [Date] | Pending |
| C003 | LinkedIn | Static | Promotional | [Topic] | [Key message] | Link in bio | [Date] | Pending |
```

### Step 5: ClickUp Task Creation (Optional)

If user wants ClickUp tasks, use ClickUp MCP to create:

**Task Structure:**
```markdown
## ClickUp Tasks

### Task Format for Each Content Item:
**Task Name:** [ID] [Platform] [Format] - [Topic]
**Description:**
- Platform: [Platform]
- Format: [Format]
- Pillar: [Pillar]
- Topic: [Topic]
- Key Message: [Key message]
- CTA: [CTA]
- Visual Notes: [From brief visual direction]

**Due Date:** [Posting date - 1 day buffer]
**Assignee:** [To be assigned]
**Status:** To Do
```

**ClickUp MCP Usage (when available):**
- Create folder for campaign
- Create list for each week
- Create tasks for each content item
- Add tags for platform, format, pillar

### Step 6: Output Structure

Compile final content plan:

```markdown
# [Brand/Campaign] Content Plan

## Campaign Overview
- **Duration:** [X weeks, dates]
- **Platforms:** [List]
- **Total Posts:** [Number]
- **Posting Frequency:** [Posts per week per platform]

## Content Pillars
[From Step 2]

## Weekly Structure
[From Step 3 - show one example week]

## Content Calendar
[From Step 3 - full calendar for all weeks]

## Content Queue
[From Step 4 - detailed table]

## ClickUp Tasks
[From Step 5 - if applicable]

## Production Notes
- **Content batching recommendation:** [Group similar formats together]
- **Lead time needed:** [X days for design, Y days for approval]
- **Posting schedule:** [Best times per platform]
```

## Best Practices

1. **Mix content types** - Don't overuse any single format or pillar
2. **Peak times matter** - Schedule posts when audience is most active
3. **Batch production** - Group similar content for efficient creation
4. **Buffer time** - Build in 1-2 days buffer for approvals and revisions
5. **Platform-native** - Adapt content for each platform's unique format

## Platform-Specific Best Practices

### Instagram
- **Feed posts:** 3-5 per week max
- **Stories:** Daily, 3-5 stories per day
- **Reels:** 2-3 per week for growth
- **Best times:** 9-11 AM, 7-9 PM (local time)

### TikTok
- **Posts:** 1-3 per day for growth
- **Best times:** 7-9 AM, 12-3 PM, 7-11 PM
- **Trend timing:** Jump on trends within 24-48 hours

### LinkedIn
- **Posts:** 2-5 per week
- **Best times:** 8-10 AM, 5-6 PM on weekdays
- **Format:** Text, carousel, and PDF perform best

### Twitter/X
- **Posts:** 3-5 per day
- **Best times:** 8-10 AM, 12-1 PM, 5-6 PM
- **Threads:** 2-3 threads per week

## Common Scenarios

### New Product Launch (1 Week Sprint)
- High frequency: 3-4 posts/day across platforms
- Mix: Educational (40%), Promotional (40%), Social Proof (20%)
- Build urgency as launch approaches

### Ongoing Brand Presence (Monthly)
- Steady frequency: 1-2 posts/day per platform
- Mix: Educational (30%), Entertainment (25%), Inspiration (20%), Promotional (15%), Community (10%)

### Campaign-Heavy (Specific Period)
- Very high frequency: 5+ posts/day
- Heavy on promotional and urgency angles
- Coordinated messaging across all platforms

## Integration with Marketing OS Workflow

**Input from:**
- `/brand-voice` - Tone and style guidelines for content scheduling
- `/content-brief` - Audience, angles, platforms, and visual direction

**Output to:**
- `/content-creation` - Content queue becomes input for asset creation
- `/campaign` - Calendar informs paid media scheduling

## Quick Start Example

```bash
# User runs:
/content-plan

# Agent asks:
1. Duration campaign? "2 minggu"
2. Posting frequency? "Instagram 3x/minggu, TikTok 5x/minggu"
3. Start date? "Senin depan, 17 Februari"
4. ClickUp tasks? "Ya, buat tasks juga"

# Agent produces:
- Content pillars based on brief
- 2-week content calendar
- Content queue table
- ClickUp tasks ready for execution
```
