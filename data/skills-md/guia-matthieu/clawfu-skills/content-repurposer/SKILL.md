---
name: content-repurposer
description: "Transform long-form content into multiple short-form pieces. Use when: converting podcast to social posts; extracting Twitter threads from blog posts; pulling quotes from transcripts; creating content variants from single source"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Content Repurposer

> Turn one piece of content into 10+ pieces using AI-powered extraction and reformatting - the "create once, publish everywhere" workflow.

## When to Use This Skill

- **Podcast repurposing** - Convert episode transcripts to threads, posts, quotes
- **Blog distribution** - Transform articles into LinkedIn posts, Twitter threads
- **Video content recycling** - Extract quotable moments and insights
- **Newsletter content** - Generate social snippets from weekly newsletters
- **Webinar follow-up** - Create post-event content from recordings


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## Dependencies

```bash
pip install anthropic jinja2 click pyyaml
# Requires ANTHROPIC_API_KEY environment variable
```

## Commands

### Multi-Format Repurpose
```bash
python scripts/main.py repurpose transcript.txt --formats "twitter,linkedin,instagram"
python scripts/main.py repurpose blog-post.md --formats all
```

### Twitter Thread
```bash
python scripts/main.py thread article.md --max-tweets 10
python scripts/main.py thread transcript.txt --style educational
```

### Quote Extraction
```bash
python scripts/main.py quotes podcast-transcript.txt --count 5
python scripts/main.py quotes interview.txt --style inspirational
```

### Hook Generation
```bash
python scripts/main.py hooks content.txt --count 10
python scripts/main.py hooks product-page.txt --style curiosity
```

## Examples

### Example 1: Podcast Episode → Full Content Suite
```bash
# Input: 45-minute podcast transcript
python scripts/main.py repurpose episode-42-transcript.txt --formats all

# Output directory: episode-42-transcript_repurposed/
# ├── twitter_thread.md (10-tweet thread)
# ├── linkedin_post.md (long-form post)
# ├── instagram_carousel.md (10 slides)
# ├── quotes.md (5 quotable moments)
# └── hooks.md (5 attention grabbers)
```

### Example 2: Blog Post → Twitter Thread
```bash
# Convert 2000-word article to thread
python scripts/main.py thread positioning-strategy.md --max-tweets 12 --style educational

# Output: positioning-strategy_thread.md
# 1/ Here's how the best B2B companies position themselves (thread)
# 2/ First, they identify their competitive alternatives...
# ...
# 12/ TL;DR: Position for differentiation, not features. Link in bio.
```

### Example 3: Extract Quotable Moments
```bash
# Pull shareable quotes from interview
python scripts/main.py quotes founder-interview.txt --count 10 --style inspirational

# Output: founder-interview_quotes.md
# 1. "We didn't build a product, we built a belief system."
# 2. "Your first 100 customers should feel like co-founders."
# ...
```

## Output Formats

| Format | Best For | Typical Length |
|--------|----------|----------------|
| `twitter` | Thread with numbered tweets | 8-15 tweets |
| `linkedin` | Long-form professional post | 1,200-1,500 chars |
| `instagram` | Carousel slide content | 10 slides |
| `quotes` | Shareable quote graphics | 5-10 quotes |
| `hooks` | Opening lines for posts | 10 hooks |
| `summary` | Executive summary | 200-300 words |
| `newsletter` | Email-friendly summary | 500-800 words |

## Content Styles

| Style | Tone | Use Case |
|-------|------|----------|
| `educational` | Teaching, explaining | Tutorials, how-tos |
| `inspirational` | Motivating, uplifting | Founder stories |
| `provocative` | Challenging assumptions | Thought leadership |
| `conversational` | Casual, relatable | Personal brand |
| `professional` | Formal, authoritative | B2B, enterprise |

## How It Works

1. **Content Analysis** - AI reads full content, identifies key themes
2. **Format Adaptation** - Restructures for each platform's constraints
3. **Hook Generation** - Creates attention-grabbing openings
4. **Quote Extraction** - Pulls most shareable moments
5. **Consistency Check** - Ensures message alignment across formats

## Best Practices

1. **Start with transcripts** - Raw transcripts work better than polished content
2. **Review hooks** - AI-generated hooks need human judgment
3. **Edit threads** - Check flow between tweets
4. **Add context** - AI can't know your audience's inside jokes
5. **Test variations** - Generate multiple versions, pick the best

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## Related Skills

- [whisper-transcription](../whisper-transcription/) - Create transcripts to repurpose
- [youtube-downloader](../youtube-downloader/) - Get video content to repurpose
- [copywriting-schwartz](../../content/copywriting-schwartz/) - Improve repurposed copy

## Skill Metadata


- **Mode**: cyborg
```yaml
category: automation
subcategory: content-automation
dependencies: [anthropic, jinja2]
difficulty: beginner
time_saved: 8+ hours/week
api_cost: ~$0.02-0.10 per repurpose
```
