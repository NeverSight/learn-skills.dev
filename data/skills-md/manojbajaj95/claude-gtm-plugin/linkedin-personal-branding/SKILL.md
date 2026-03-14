---
name: linkedin-personal-branding
description: Comprehensive LinkedIn personal branding analysis, profile optimization, and visibility improvement skill using Claude for Chrome browser tools. Use when users request LinkedIn profile analysis, personal branding audit, profile optimization recommendations, LinkedIn visibility improvement, headline optimization, About section review, content strategy guidance, engagement analysis, or Social Selling Index improvement. Works with Claude for Chrome to analyze profile photos, banners, headlines, About sections, experience, skills, recommendations, featured content, activity/posts, and network engagement directly from the user's browser.
---

# LinkedIn Personal Branding Skill

## CRITICAL: Mandatory Audit Requirements

Every audit MUST include — no exceptions:

| Field | How to Determine |
|-------|-----------------|
| **Industry/Sector** | Job titles, skills, content topics |
| **Profile Type** | Employee / Consultant / Freelancer / Entrepreneur / Job Seeker |
| **Target Audience** | Recruiters / Clients / Peers / Investors / Partners |
| **Engagement Rate** | CALCULATED: (Reactions+Comments+Shares)/Impressions×100 |
| **SSI Score** | Actual score OR estimation with note |

These fields appear in the report header. Do not skip them.

---

## Core Workflow

### Step 1: Determine Analysis Type

- **Full Profile Audit** — all elements, complete report with scores
- **Quick Profile Review** — priority action items and quick wins
- **Content Strategy Analysis** — posts, engagement, content performance
- **Visibility Optimization** — keyword/SEO discoverability

### Step 2: Access LinkedIn via Chrome DevTools

**Required:** LinkedIn profile open in Chrome, user logged in.

| Tool | MCP Name | Use For |
|------|----------|---------|
| List Pages | `mcp__chrome-devtools__list_pages` | Find LinkedIn tab by URL |
| Select Page | `mcp__chrome-devtools__select_page` | Focus tab |
| Snapshot | `mcp__chrome-devtools__take_snapshot` | Accessibility tree with UIDs |
| Screenshot | `mcp__chrome-devtools__take_screenshot` | Photo and banner analysis |
| Navigate | `mcp__chrome-devtools__navigate_page` | Go to URLs |
| Click/Hover | `mcp__chrome-devtools__click` / `hover` | Interact with elements |
| Wait For | `mcp__chrome-devtools__wait_for` | Lazy-loaded content |

**Extraction workflow:**
1. `list_pages` → find pageId where URL contains `linkedin.com/in/`
2. `select_page` → focus tab
3. `take_snapshot` → get accessibility tree with UIDs
4. `take_screenshot` → analyze photo/banner
5. For lazy-loaded sections: `hover` to scroll → re-snapshot

**Profile sections to analyze:** photo, banner, headline, About, custom URL, experience, education, skills/endorsements, certifications, recommendations, featured section, activity/posts, followers, connections (500+ indicator), groups.

### Step 3: Score Profile Elements

| Category | Weight | Key Factors |
|----------|--------|-------------|
| Visual Identity | 15% | Photo quality, banner, consistency |
| Headline | 15% | Value proposition, keywords, memorability |
| About Section | 15% | Story, keywords, CTA |
| Experience | 20% | Completeness, achievements, metrics |
| Skills & Endorsements | 10% | Relevance, count |
| Recommendations | 10% | Quality, diversity, recency |
| Activity & Content | 15% | Posting frequency, engagement rate |

**Score interpretation:** 90-100 Elite · 80-89 Excellent · 70-79 Good · 60-69 Average · <60 Needs Work

### Step 4: Calculate Mandatory Metrics

**Engagement Rate (REQUIRED):**
```
Engagement Rate = (Reactions + Comments + Shares) / Impressions × 100
```
Example: (15+1+0)/1,376×100 = 1.16% → below 3% target

**SSI Score (REQUIRED):**

Option A — User visits `linkedin.com/sales/ssi` and shares score (target: 70+/100, 20+/25 per component).

Option B — If unavailable, estimate:
| Profile Characteristics | Estimated SSI |
|------------------------|---------------|
| All-Star + active posting + engaged network | 70-85 |
| Complete + regular posting | 55-70 |
| Basic + occasional activity | 40-55 |
| Incomplete + minimal activity | <40 |

**Keyword/SEO:** Check keyword presence in headline, About, experience, skills. Recommend additions for target role/industry.

**Profile completeness (All-Star):** photo, banner, customized headline, About (500+ chars), current position + description, 2+ past positions, education, 5+ skills, location, industry.

### Step 5: Generate Recommendations

**Priority matrix:**
- **Quick Wins** (high impact, low effort) — do immediately
- **Strategic Initiatives** (high impact, high effort) — plan carefully
- **Nice-to-haves** (low impact, low effort) — when possible

**Categories:** Profile optimization, Content strategy (3x/week minimum posting), Engagement (comments, network growth, recommendations), Visibility (keywords, featured section, creator mode).

### Step 6: Deliver Report

**Pre-report checklist:** industry identified, profile type classified, target audience identified, engagement rate calculated, SSI captured or estimated, industry benchmarks applied.

**Report sections:**
1. Executive Summary
2. Classification (Industry, Profile Type, Target Audience)
3. Profile Scorecard
4. Calculated Metrics (Engagement Rate, SSI)
5. Element-by-Element Analysis
6. Quick Wins
7. Strategic Recommendations
8. 30-60-90 Day Action Plan

---

## Profile Element Best Practices

**Photo:** 400×400px minimum, professional attire, approachable expression, clean background, face 60-70% of frame, good lighting.

**Banner (1584×396px):** Branded/industry-relevant, value proposition text, no clutter or small text.

**Headline formula (220 chars max):** Who you are + problems you solve + benefit/result + keywords
- Bad: "Marketing Manager"
- Good: "Marketing Manager | Helping B2B Companies Grow Through Data-Driven Strategies | 45% Revenue Increase Specialist"

**About section (2,600 chars max):** Hook (first 2-3 lines) → story → what you do/who you help → achievements with metrics → skills → CTA. First person, short paragraphs, relevant keywords.

**Experience:** Quantified achievements (%, $, #), scope, key projects, skills demonstrated.

**Skills:** 50+ relevant skills, top 3 pinned, endorsements from colleagues, aligned with target keywords.

**Featured:** 3-6 curated items — portfolio, case studies, articles, media, lead magnets.

**Services (Consultants/Freelancers):** 3-5 keyword-rich service offerings.

---

## Chrome DevTools Navigation Patterns

**Lazy-loaded sections:**
```
hover(uid: "[section_uid]") → wait_for(text: "Show all") → take_snapshot()
```

**Activity/posts:**
```
navigate_page(url: "linkedin.com/in/[user]/recent-activity/")
→ wait_for(text: "reactions") → take_snapshot()
```

**Analytics dashboard:**
```
navigate_page(url: "https://www.linkedin.com/analytics/")
→ wait_for(text: "Profile viewers") → take_snapshot()
```

**SSI:**
```
navigate_page(url: "https://www.linkedin.com/sales/ssi")
→ wait_for(text: "Social Selling Index") → take_snapshot()
```

**Playwright fallback:** If Chrome DevTools MCP unavailable, use `mcp__playwright__browser_*` equivalents (snapshot, screenshot, navigate, click, hover, wait_for).

**Error handling:**

| Error | Recovery |
|-------|----------|
| LinkedIn tab not found | Ask user to open LinkedIn in Chrome |
| Element UID missing | Re-snapshot, find alternative UID |
| Content not loading | Scroll manually, increase timeout, refresh |
| Rate limited/CAPTCHA | Pause 30+ seconds, proceed slowly |
| SSI requires Sales Navigator | Note unavailable, provide estimation |
| Private profile | Document as "Limited visibility" |

---

## Industry-Specific Guidance

Always classify industry first. Load `references/metrics_benchmarks.md` for industry benchmarks across 15+ industries (Tech, Finance, Healthcare, Legal, Marketing, HR, Consulting, Creative, Nonprofit, Startups, etc.).

| Factor | Conservative (Legal, Finance, Healthcare) | Progressive (Tech, Marketing, Startups) |
|--------|------------------------------------------|----------------------------------------|
| Tone | Formal | Casual, personable |
| Content | Thought leadership | Stories, behind-the-scenes |
| Posting | 2-3x/week | 4-5x/week |
| Emojis | Minimal | Acceptable |

**LinkedIn Features to assess:** Creator Mode (enable if 3+/week posting), Open to Work (job seekers), Providing Services (consultants), Newsletter (1000+ followers), Custom URL (always set), Verification Badge.

---

## Reference Files

- `references/scoring_framework.md` — detailed scoring criteria with examples
- `references/metrics_benchmarks.md` — industry benchmarks for SSI, engagement, growth
- `references/content_strategy.md` — content pillars, posting schedules, formats
- `assets/profile_audit_template.md` — complete audit report template
- `assets/quick_review_template.md` — rapid assessment checklist
- `assets/action_plan_template.md` — 30-60-90 day roadmap template
