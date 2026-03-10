---
name: instagram-marketing
description: Generate Instagram marketing content from product URLs. Extract product information and create engaging Instagram posts with image suggestions, captions, and hashtags optimized for engagement. Use when user provides a product URL from e-commerce sites like Amazon, Shopify, Taobao, etc. and wants Instagram marketing content such as Image/text post ideas, engaging captions with CTAs, hashtag strategy, or Story/reels content suggestions.
---

# Instagram Marketing Generator

## Overview

Transform any product URL into scroll-stopping Instagram content. Extract product details, analyze brand positioning, and generate platform-native marketing assets that drive engagement and conversions.

## Quick Start

1. **Input**: Provide product URL
2. **Extract**: Use `scripts/extract_product.py` to fetch product details
3. **Generate**: Apply Instagram content frameworks from `references/`
4. **Deliver**: Output ready-to-post content package

## Content Frameworks

### Framework Selection Guide

Choose based on product type and brand personality:

| Product Type   | Recommended Framework | Reference      |
| -------------- | --------------------- | -------------- |
| Fashion/Beauty | Aesthetic + Lifestyle | `FASHION.md`   |
| Tech/Gadgets   | Feature-First + Demo  | `TECH.md`      |
| Food/Beverage  | Sensory + Lifestyle   | `LIFESTYLE.md` |
| Home/Decor     | Transformation + Tips | `HOME.md`      |
| Services       | Trust + Results       | `SERVICE.md`   |

### Core Content Elements

Every Instagram post package includes:

#### 1. Image/Video Brief

```
• Visual style (aesthetic direction)
• Composition guidelines
• Text overlay suggestions (optional)
• Product angle recommendations
• Background/props guidance
```

#### 2. Caption Structure

```
HOOK → [First line - stops the scroll]
  |
  ├── BODY → [Value proposition, benefits, story]
  |
  └── CTA → [Clear action: link, DM, save, share]
```

**Caption Length Guide:**

- Feed posts: 138-150 characters (optimal engagement)
- Carousel: 150-200 characters
- Educational: Up to 300 characters

#### 3. Hashtag Strategy (30 max)

```
• 3-5 branded/niche tags (high relevance)
• 10-15 trend tags (moderate volume)
• 5-10 broad tags (max reach)
• Mix of: #branded #descriptive #trend #location #emotion
```

See `references/HASHTAG_STRATEGY.md` for detailed hashtag optimization.

## Product Information Extraction

### Script Usage

```bash
python3 scripts/extract_product.py <url>
```

**Extracted fields:**

- Product name
- Price/value proposition
- Key features (3-5)
- Target audience
- Unique selling proposition
- Brand tone
- Visual assets (existing images)

### Manual Extraction Fallback

If script fails, extract manually:

1. Visit product URL
2. Identify: name, price, features, benefits
3. Note brand visual style
4. Capture 3-5 product angles

## Content Generation Workflow

### Step 1: Analyze Product & Audience

```
PRODUCT → [What is it? What problem does it solve?]
  |
  ├── TARGET AUDIENCE → [Who needs this? Why?]
  |
  ├── BRAND TONE → [Luxury? Playful? Minimal? Bold?]
  |
  └── PLATFORM FIT → [Feed post, Story, Reel, Carousel?]
```

**Key Questions:**

- What emotion should the user feel?
- What's the "scroll-stopping" moment?
- What's the post-purchase transformation?

### Step 2: Choose Content Format

#### Feed Post (Single Image)

- **Best for**: Product showcases, announcements
- **Visual**: High-quality product shot, clean background
- **Caption**: Punchy hook + benefits + CTA

#### Carousel (Swipe-able)

- **Best for**: Features, tutorials, transformations
- **Structure**: 5-10 slides
  1. Hook slide
     2-4. Feature/benefit slides
  2. CTA slide

#### Story (15-60 sec)

- **Best for**: Flash sales, polls, Q&A, behind-scenes
- **Elements**: Interactive stickers, tap-through links

#### Reel (15-90 sec video)

- **Best for**: Demos, unboxing, transformations
- **Hook**: First 1 second critical
- **Music**: Trending audio boost

### Step 3: Generate Content Package

Output format (see `templates/OUTPUT_TEMPLATE.md`):

```markdown
## Instagram Content Package

### Post Type: [Feed/Carousel/Story/Reel]

### Image/Video Brief

[Visual direction + composition]

### Caption

[Hook + Body + CTA]

### Hashtags

[30 optimized hashtags]

### Posting Strategy

[Time, frequency, cross-post suggestions]
```

## Instagram Style Guidelines

### Visual Principles

1. **Consistency First**
   - Cohesive color palette (3-5 colors max)
   - Consistent filter/preset
   - Recognizable brand aesthetic

2. **Quality Over Quantity**
   - High-resolution images (1080x1080 or 1080x1350)
   - Good lighting (natural preferred)
   - Clean composition (rule of thirds)

3. **Native Feel**
   - Avoid over-polished, stock-looking content
   - Embrace authenticity
   - Show real people/products

### Caption Best Practices

✅ DO:

- Start with a hook (question, bold statement, emotion)
- Write conversationally (like talking to a friend)
- Use line breaks for readability
- Include clear CTA
- Add 3-5 relevant hashtags

❌ DON'T:

- Write paragraphs longer than 3 lines
- Use excessive emojis (1-3 max)
- Overuse hashtags (30 max, quality > quantity)
- Sound robotic or overly promotional
- Include "link in bio" more than once

### Engagement Triggers

Embed these in content:

```
• Questions: "Which color would you choose?"
• Opinions: "Yes or No?"
• Saves: "Save this for later"
• Shares: "Tag someone who needs this"
• CTAs: "Link in bio to shop"
```

## Content Templates

### Template 1: Problem-Solution

```
Hook: Tired of [problem]?
Body: Meet [product]. It [benefit 1], [benefit 2], and [benefit 3].
CTA: Shop now → link in bio
```

### Template 2: Transformation

```
Hook: Before → After
Body: How [product] transformed [situation].
CTA: See the difference → link in bio
```

### Template 3: Social Proof

```
Hook: ⭐⭐⭐⭐⭐ "Review quote"
Body: Join [number]+ happy customers.
CTA: Try it risk-free → link in bio
```

### Template 4: Educational

```
Hook: 5 things you didn't know about [product/category]
Body: [Value-packed tips]
CTA: Save this post + follow for more
```

### Template 5: Limited Time

```
Hook: 🚨 Only [number] left!
Body: [Product] at [price] for [timeframe].
CTA: Don't miss out → link in bio
```

## Advanced: Multi-Post Series

For product launches or campaigns, create 3-5 post series:

### Series Structure

1. **Teaser** (2-3 days before)
   - Build anticipation
   - "Something big coming"

2. **Launch** (Day 1)
   - Product reveal
   - Key features

3. **Deep Dive** (Day 2-3)
   - Benefits, use cases
   - Social proof

4. **Urgency** (Day 4-5)
   - Limited availability
   - Last chance

See `references/CAMPAIGN_STRATEGY.md` for complete campaign planning.

## References

### Detailed Guides

- `references/FASHION.md` - Fashion & beauty content
- `references/TECH.md` - Tech & gadgets content
- `references/HASHTAG_STRATEGY.md` - Hashtag optimization
- `references/CAMPAIGN_STRATEGY.md` - Multi-post campaigns
- `references/ENGAGEMENT_TACTICS.md` - Comment management & growth

### Templates

- `templates/CAROUSEL_TEMPLATE.md` - Swipe-able post structure
- `templates/STORY_TEMPLATE.md` - Interactive story framework
- `templates/REEL_TEMPLATE.md` - Video script structure
- `templates/OUTPUT_TEMPLATE.md` - Final content format

## Tips

- Always match content to brand voice
- Test different hook styles
- Analyze competitor posts for inspiration
- Repurpose content across formats (feed → story → reel)
- Save high-performing posts as templates
- Time posts for peak audience hours
- Engage with comments within 1 hour
- Use Instagram Insights to optimize
