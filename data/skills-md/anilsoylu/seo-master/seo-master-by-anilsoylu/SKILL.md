---
name: seo-master-by-anilsoylu
description: >
  This skill should be used when the user asks to audit, review, or diagnose
  SEO issues on a website. Common triggers include "SEO audit," "technical SEO,"
  "why am I not ranking," "SEO health check," "on-page SEO review," "meta tags
  review," "keyword research," "backlink audit," "SEO content strategy,"
  "link building strategy," "SEO checklist," "SEO landing page," or
  "programmatic SEO." Also appropriate when the user wants to optimize existing
  pages for search engines or plan a content operations workflow.
---

# SEO Audit & Optimization Workflow

Run a comprehensive SEO audit using this 10-step framework. Each step includes actionable checks and links to detailed reference guides.

## Step 1: Basic Technical SEO Foundation

Verify core technical infrastructure is in place: Google Analytics 4, Google Search Console, robots.txt, XML sitemap, SSL certificate, and mobile responsiveness. Eliminate duplicate content issues. Ensure the site provides a good user experience.

→ Full checklist: `references/technical-seo.md`

## Step 2: Site Speed Optimization

Compress all images (use WebP format). Enable lazy loading for below-fold content. Minify CSS/JS. Enable CDN caching (Cloudflare recommended). Target page load under 3 seconds. Pass Core Web Vitals.

→ Full checklist: `references/technical-seo.md` (Speed section)

## Step 3: Keyword Research (200-300+ targets)

1. Define 5-10+ seed keywords for the niche
2. Run seeds through Semrush, filter KD 0-20 first
3. Extract all relevant keywords, then repeat for higher KD ranges
4. Run discovered keywords through AI to generate additional variations
5. Classify by search intent: informational, commercial, transactional
6. Group into content clusters

→ AI prompts for keyword research: `references/seo-checklists.md`

## Step 4: Create SEO Landing Pages

Build 10-50+ landing pages targeting high buyer-intent keywords. Interlink them in navbar and footer. Ensure all blog content links to relevant landing pages. Each page needs clear value prop at top, search-optimized content below.

→ Template patterns: `references/programmatic-seo.md`

## Step 5: Optimize Landing Pages (On-Page SEO)

For every page, verify:
- Target keyword in H1, H2, body, first 100 words, URL, title tag, meta description
- Semantically related keywords throughout
- SEO-friendly FAQ section at bottom
- Keyword-rich anchor text for internal links
- Content depth 1.5x competitors

→ Full on-page checklist: `references/on-page-seo.md`

## Step 6: Content Operations Setup

Target 10-20+ articles/month. Create detailed content outlines manually (AI is weak at this). Hire 2-5+ writers. Use AI as writing assistant, not replacement. Every piece must beat competitors in depth and quality.

Key AI content workflow:
1. Set up AI project with brand voice, top content, competitor articles
2. Build outline manually after analyzing top 3 SERP results
3. Collaborate with AI iteratively - give feedback, fix output
4. Inject real expertise: case studies, screenshots, specific numbers
5. Edit ruthlessly - kill all AI red flags

→ Full workflow + blacklist: `references/content-strategy.md`

## Step 7: Internal Linking Strategy

All new content must link to older relevant posts. Monthly interlinking audit: connect old and new content. Use keyword variations as anchor text (never "click here"). 3-5 internal links minimum per post. No orphan pages.

→ Linking checklist: `references/on-page-seo.md` (Internal Linking section)

## Step 8: Competitor Backlink Audit

Run a competitor backlink gap analysis using Semrush to determine how many links per month are needed to close the gap. Filter for quality do-follow links only.

→ Full audit process + calculation method: `references/link-building.md`

## Step 9: Link Building Operations

Set up outreach infrastructure:
- Branded email domain, 30-50 emails/day per inbox, 2-3 inboxes
- 2 follow-ups per prospect (day 3 and day 7)
- Minimum 3,000 outreach emails/month
- 20+ campaigns/month
- Always offer value (guest post, feature, data)

Focus on quality: DA 40+ sites with 1,000+ monthly traffic. Budget $75-150 per placement. 10 quality links > 200 garbage links.

→ Sprint plan + email templates: `references/link-building.md`

## Step 10: Ongoing Operations

- Monitor rankings weekly, find content improvement opportunities
- Publish more and better content than competitors
- Build more and better links than competitors
- Update existing content every 6 months
- Create stats pages as backlink magnets
- Run digital PR campaigns based on search trends

→ Growth strategies: `references/link-building.md` (Digital PR section)

---

## Quick Reference: Which File Has What

| Topic | Reference File |
|-------|---------------|
| Domain, hosting, robots.txt, sitemap, speed, mobile, Core Web Vitals, schema | `references/technical-seo.md` |
| Title tags, meta descriptions, headers, URLs, images, internal links, E-E-A-T | `references/on-page-seo.md` |
| AI content workflow, writing blacklist, system prompts, editing checklist | `references/content-strategy.md` |
| Backlink audit, 10-day sprint, outreach, digital PR, HARO, stats pages | `references/link-building.md` |
| Programmatic SEO templates, city pages, comparison pages, AI batch generation | `references/programmatic-seo.md` |
| Keyword placement, pre/post-publish, launch checklist, AI prompts | `references/seo-checklists.md` |
