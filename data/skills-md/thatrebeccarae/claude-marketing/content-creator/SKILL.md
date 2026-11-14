---
name: content-creator
description: Comprehensive content marketing toolkit with brand voice analysis, SEO optimization scripts, content frameworks, social media strategy, and content calendar planning. Use when writing blog posts, creating social media content, analyzing brand voice, optimizing SEO, planning content calendars, or developing content strategy. For deep SEO writing optimization, see the seo-content-writer skill.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: content
  domain: content-creation
  updated: 2026-03-18
  tested: 2026-03-18
  tested_with: "Claude Code v2.1"
---

# Content Creator

Professional-grade brand voice analysis, SEO optimization, and platform-specific content frameworks with executable Python tools.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/content-creator ~/.claude/skills/
```

> **How this differs from seo-content-writer:** The seo-content-writer skill focuses on deep SEO writing — keyword research, on-page optimization, meta tags, heading hierarchy. This skill is the broader content marketing toolkit — brand voice development, content calendars, multi-platform strategy, and includes executable Python scripts for analysis.

## Core Workflows

### Brand Voice Development

1. **Analyze Existing Content** (if available)
   ```bash
   python scripts/brand_voice_analyzer.py existing_content.txt
   ```

2. **Define Voice Attributes**
   - Review brand personality archetypes in REFERENCE.md
   - Select primary and secondary archetypes
   - Choose 3-5 tone attributes
   - Document in brand guidelines

3. **Create Voice Sample**
   - Write 3 sample pieces in chosen voice
   - Test consistency using analyzer
   - Refine based on results

### Creating SEO-Optimized Blog Posts

1. **Keyword Research**
   - Identify primary keyword (search volume 500-5000/month)
   - Find 3-5 secondary keywords
   - List 10-15 LSI keywords

2. **Content Structure**
   - Use blog template from REFERENCE.md
   - Include keyword in title, first paragraph, and 2-3 H2s
   - Aim for 1,500-2,500 words for comprehensive coverage

3. **Optimization Check**
   ```bash
   python scripts/seo_optimizer.py blog_post.md "primary keyword" "secondary,keywords,list"
   ```

4. **Apply SEO Recommendations**
   - Adjust keyword density to 1-3%
   - Ensure proper heading structure
   - Add internal and external links
   - Optimize meta description

### Social Media Content Creation

1. **Platform Selection** — Identify primary platforms based on audience
2. **Content Adaptation** — Start with core message, use repurposing matrix from REFERENCE.md
3. **Optimization** — Platform-appropriate length, optimal posting time, correct image dimensions

### Content Calendar Planning

1. **Monthly Planning** — Set goals and KPIs, identify key themes
2. **Weekly Distribution** — Follow 40/25/25/10 content pillar ratio
3. **Batch Creation** — Create all weekly content in one session

## Key Scripts

### brand_voice_analyzer.py

Analyzes text content for voice characteristics, readability, and consistency.

**Usage**: `python scripts/brand_voice_analyzer.py <file> [json|text]`

**Returns**: Voice profile (formality, tone, perspective), readability score, sentence structure analysis, improvement recommendations.

### seo_optimizer.py

Analyzes content for SEO optimization and provides actionable recommendations.

**Usage**: `python scripts/seo_optimizer.py <file> [primary_keyword] [secondary_keywords]`

**Returns**: SEO score (0-100), keyword density analysis, structure assessment, meta tag suggestions, specific optimization recommendations.

## Quality Indicators

- SEO score above 75/100
- Readability appropriate for audience
- Consistent brand voice throughout
- Clear value proposition
- Actionable takeaways
- Platform-optimized

## Performance Metrics

### Content Metrics
- Organic traffic growth
- Average time on page
- Bounce rate, social shares, backlinks

### Engagement Metrics
- Comments, email CTR, engagement rate, downloads

### Business Metrics
- Leads generated, conversion rate, CAC, revenue attribution, ROI per piece
