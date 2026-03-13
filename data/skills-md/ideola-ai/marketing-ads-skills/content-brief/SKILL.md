---
name: content-brief
description: Create comprehensive social media content brief with research-backed strategy. Use when user asks to create content brief, social media strategy document, or needs research foundation for content planning. Triggers on - "buat brief", "brief social media", "content strategy", "research konten", "/brief" command, or any request for strategic content planning with audience analysis, platform guidelines, and content angles.
version: 1.0.0
---

# Social Media Brief Research

## Overview

This skill creates comprehensive social media content briefs with research-backed strategy. It transforms brand/product information into actionable audience insights, platform guidelines, content angles, and visual direction.

## Marketing OS Workflow Position

```
brand-voice → content-brief → content-planning → content-creation
                                          ↓
                                        marketing-campaign
                                          ↓
                                          ads-audit
```

**This skill is SECOND** - Create brief after defining brand voice, before planning content or campaigns.

**Input from:**
- `/brand-voice` - Brand attributes, tone guidelines, messaging pillars

**Output to:**
- `/content-planning` - Audience, angles, platforms become inputs for calendar
- `/campaign` - Audience and angles inform paid media strategy

## Workflow

### Step 1: Gather Brand Context

Collect essential information about the brand or product:

**Required Information:**
- Brand/product name and description
- Unique value proposition (UVP)
- Campaign objective (awareness, consideration, conversion, retention)
- Target location/geographic

**Ask if not provided:**
1. Brand atau produk apa yang mau dibuatkan brief?
2. Apa objective utama campaign ini?
3. Target lokasi geografis mana?

### Step 2: Define Target Audience

Create detailed audience profiles based on the product and objective.

**Audience Profile Framework:**

| Element | Description | Example |
|---------|-------------|---------|
| **Demographics** | Age, gender, location, income, education | Women 25-34, urban, middle income |
| **Psychographics** | Interests, values, lifestyle, personality | Health-conscious, career-driven, eco-friendly |
| **Pain Points** | Problems they need solving | "No time to cook healthy meals" |
| **Goals/Desires** | What they want to achieve | Want to feel energized, save time |
| **Behaviors** | How they consume content | Active on Instagram, watches recipe videos |
| **Barriers** | Objections to overcome | "Too expensive", "Tastes bland" |

**Output Format:**
```markdown
## Target Audience

### Primary Audience
- **Demographics:** [Age, gender, location, income, education]
- **Psychographics:** [Interests, values, lifestyle, personality]
- **Pain Points:** [Top 3-5 problems they face]
- **Goals/Desires:** [What they want to achieve]
- **Content Consumption:** [Platforms they use, content formats they prefer]
- **Barriers to Purchase:** [Objections to overcome]

### Secondary Audience (if applicable)
[Same structure as primary]
```

### Step 3: Platform Strategy

Define which platforms to use and how to adapt content for each.

**Platform Selection Criteria:**

| Platform | Best For | Audience Type | Content Format |
|----------|----------|---------------|----------------|
| **Instagram** | Visual storytelling, brand aesthetic | 18-44, urban | Carousels, Reels, Stories |
| **TikTok** | Viral reach, younger demographics | 16-30, trend-followers | Short-form video, trends |
| **LinkedIn** | B2B, professional authority | 25-55, professionals | Static posts, carousels, PDF |
| **Twitter/X** | Real-time engagement, news | 18-50, information-seekers | Threads, text posts |
| **YouTube** | Long-form education, search | 18-50, learners | Long-form video, Shorts |

**Output Format:**
```markdown
## Platform Strategy

### Primary Platforms
1. **[Platform]**
   - **Why this platform:** [Rationale based on audience]
   - **Content focus:** [What type of content works]
   - **Best times to post:** [Based on audience behavior]
   - **Key tactics:** [Platform-specific strategies]

### Secondary Platforms (if applicable)
[Same structure]
```

### Step 4: Develop Content Angles

Create 3-5 distinct content angles based on audience insights.

**Content Angle Framework:**

| Angle Type | Description | Example |
|------------|-------------|---------|
| **Problem-Solution** | Address pain point with solution | "5 signs you're burned out (and how to fix it)" |
| **Social Proof** | Show others benefiting | "How Sarah saved 10 hours/week with our tool" |
| **Educational** | Teach something valuable | "The science behind why this works" |
| **Entertainment** | Engage through humor or trends | [Trending format] + [brand twist] |
| **Inspiration** | Motivate or inspire | "From [struggle] to [success] in 30 days" |
| **Behind-the-Scenes** | Show authenticity | "Day in the life at [company]" |
| **Myth-Busting** | Challenge misconceptions | "3 myths about [industry] debunked" |

**Each Angle Should Include:**
- Angle name
- Key message (the core idea)
- Sample topics (3-5 specific content ideas)
- Tone/mood

**Output Format:**
```markdown
## Content Angles

### Angle 1: [Angle Name]
- **Key Message:** [Core idea to communicate]
- **Why this works:** [Connection to audience pain/desire]
- **Sample Topics:**
  1. [Topic idea]
  2. [Topic idea]
  3. [Topic idea]
- **Tone:** [e.g., Empathetic, authoritative, playful]

### Angle 2: [Angle Name]
[Continue for 3-5 angles]
```

### Step 5: Define Visual Direction

Provide clear visual guidance for content creation.

**Visual Direction Framework:**

| Element | Description |
|---------|-------------|
| **Color Palette** | Primary, secondary, accent colors |
| **Typography** | Font styles for headers, body, CTAs |
| **Imagery Style** | Photo style, illustration style, or mixed |
| **Layout Style** | Minimal, bold, eclectic, etc. |
| **Brand Elements** | Logo usage, patterns, icons |

**Output Format:**
```markdown
## Visual Direction

### Brand Aesthetic
- **Overall vibe:** [e.g., Clean and modern, warm and friendly, bold and edgy]
- **Color palette:**
  - Primary: [Color hex codes]
  - Secondary: [Color hex codes]
  - Accent: [Color hex codes]
- **Typography:** [Font styles]

### Content Visual Guidelines
- **Image style:** [Photography, illustration, mixed, UGC]
- **Composition:** [Center-focused, rule of thirds, asymmetrical]
- **Key elements:** [What should appear in every visual]
- **Avoid:** [What NOT to include]
```

### Step 6: Compile Final Brief

Combine all sections into a comprehensive brief document.

```markdown
# [Brand/Campaign] Social Media Brief

## Brand Overview
- **Brand/Product:** [Name]
- **Campaign Objective:** [Objective]
- **Unique Value Proposition:** [UVP]

## Target Audience
[From Step 2]

## Platform Strategy
[From Step 3]

## Content Angles
[From Step 4]

## Visual Direction
[From Step 5]

## Key Messages by Platform
[Summary of what to communicate on each platform]

## Success Metrics
[How to measure campaign success]
```

## Best Practices

1. **Start with audience** - Everything flows from understanding who you're talking to
2. **Be specific** - Vague briefs lead to vague content
3. **Platform-native** - Each platform needs tailored approach
4. **Data-backed** - Use research and insights, not assumptions
5. **Actionable** - Brief should guide content creation directly

## Common Scenarios

### New Product Launch
- Focus on awareness and consideration
- Heavy on educational and social proof angles
- Multi-platform approach with coordinated messaging

### Brand Awareness
- Focus on entertainment and inspiration
- Emphasize brand personality and values
- Visual-heavy, shareable content

### Conversion-Focused
- Focus on social proof and problem-solution
- Strong CTAs and urgency elements
- Retargeting angles included

### Community Building
- Focus on community and UGC
- Two-way conversation emphasis
- Authentic, behind-the-scenes content

## Integration with Marketing OS Workflow

**Input from:**
- `/brand-voice` - Brand attributes, tone guidelines, messaging pillars (if already defined)

**Output to:**
- `/content-planning` - Audience, angles, platforms, and visual direction become inputs
- `/campaign` - Audience and angles inform paid media strategy
- `/content-creation` - Visual direction and key messages guide asset creation

## Quick Start Example

## Quick Start Example

```bash
# User runs:
/brief

# Agent asks:
1. Brand/produk apa? "Healthy meal delivery service untuk busy professionals"
2. Objective? "Conversion - dapatkan 100 trial order"
3. Lokasi? "Jakarta dan Surabaya"

# Agent produces:
- Detailed audience profile (busy professionals, 25-40, urban)
- Platform strategy (Instagram + TikTok for visual food content)
- 5 content angles with sample topics
- Visual direction (fresh, appetizing, clean aesthetic)
```

## Research Resources

When available, use these research sources:
- **Competitor analysis** - What competitors are doing well
- **Industry trends** - Current topics and formats in the industry
- **Audience data** - Existing customer insights or social analytics
- **Platform trends** - Trending formats and features on target platforms
