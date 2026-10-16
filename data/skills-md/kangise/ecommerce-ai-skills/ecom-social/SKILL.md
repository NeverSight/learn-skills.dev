---
name: ecom-social
description: Create and optimize e-commerce social media content, ads, and community management across platforms (Instagram, YouTube, TikTok, Pinterest, Reddit, WhatsApp, 小红书). Use for content creation, posting strategy, hashtags, captions, influencer collaboration, or cross-channel campaigns.
---

# Social Media Skill

## When to Use

Create and optimize e-commerce social media content and advertising across platforms. Use for content creation (Reels, Shorts, Stories, Carousel, Pin, 种草笔记), posting strategy, hashtag research, ad copy, influencer collaboration, community management, or cross-channel repurposing.

## Method

### Step 1: Read Platform Constraints

Read `references/constraints.md` for platform-level rules. Social media has no numeric constraints in the ontology yet — platform-specific best practices live in each chapter's prompt templates in the playbook.

### Step 2: Review Boundaries

Read `references/boundaries.md` to know when this skill should NOT be used (e.g. no visual story, no local-language capacity, chasing this-month conversion, mechanical reposting).

### Step 3: Pick the Prompt

Pick the appropriate prompt from `references/playbook.md` for your platform and scenario:

- **e1** — Instagram/Facebook: Reels, Stories, Carousel, Shopping, Meta Ads, hashtags, influencer collaboration
- **e2** — YouTube: SEO keywords, titles, scripts, Shorts, thumbnails, affiliate descriptions
- **e3** — 小红书: 种草笔记, SEO, 达人合作, 算法优化, 数据分析
- **e4** — Pinterest: SEO, Pins, Idea Pins, Shopping, seasonal calendar, Shopping Ads
- **e5** — WhatsApp: 客服 AI, chatbot flows, 复购营销, sales assistant
- **e6** — Reddit: community participation, Ads, reputation monitoring, GEO
- **e7** — Cross-channel: content adaptation, weekly repurposing, cross-platform analytics, attribution

### Step 4: Execute and Verify

Execute the prompt with your data. Use the `<自检>/<self_check>/<セルフチェック>` self-check block in each prompt to verify output quality before delivering results.

## References

- [Constraints](references/constraints.md) — Platform rules and limits
- [Playbook](references/playbook.md) — Prompt collection (54 prompts, e1–e7)
- [Boundaries](references/boundaries.md) — When not to use

## Templates

Copy-ready prompt templates (in `assets/templates/`):

- [Instagram Reels Scripts](assets/templates/template-1-instagram-reels-scripts.md)
- [YouTube Video Description](assets/templates/template-2-youtube-video-description.md)
- [小红书种草笔记](assets/templates/template-3-xiaohongshu-seeding-note.md)
- [Cross-Channel Content Adaptation](assets/templates/template-4-cross-channel-adaptation.md)
