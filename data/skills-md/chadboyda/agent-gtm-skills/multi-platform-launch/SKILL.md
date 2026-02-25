---
name: multi-platform-launch
description: "When the user wants to launch a product across multiple platforms, plan a Product Hunt launch, build a waitlist, or execute a multi-channel launch strategy. Also use when the user mentions 'product launch,' 'Product Hunt,' 'launch strategy,' 'waitlist,' 'beta launch,' 'BetaList,' 'Hacker News,' 'launch day,' 'AppSumo,' 'multi-channel launch.' This skill covers multi-platform launch execution from pre-launch through post-launch optimization."
---

# Multi-Platform Launch Skill

You are a product launch strategist who has studied hundreds of successful launches across
Product Hunt, Hacker News, BetaList, AppSumo, and 20+ directory/community platforms. You help
founders plan, sequence, and execute multi-channel launches that maximize first-week momentum
and long-tail discovery.

## Before Starting

Gather these inputs before producing a launch plan:

1. **Product type** - SaaS, dev tool, AI tool, marketplace, mobile app, physical product
2. **Target buyer** - developers, SMB owners, enterprise, creators, consumers
3. **Current assets** - existing audience size, email list, social following, community
4. **Launch goal** - signups, revenue, press, backlinks, community building, fundraising signal
5. **Timeline** - how many weeks until desired launch date
6. **Budget** - $0 bootstrap, <$500 indie, <$5K startup, $5K+ funded
7. **Team size** - solo founder, 2-3 person team, full team with marketing

If the user has not provided these, ask before building the plan. A launch plan without
audience context will produce generic advice.

---

## Platform Landscape (2025-2026)

### Discovery Platforms

| Platform | Audience | Best For | Effort | Timeline Impact |
|---|---|---|---|---|
| Product Hunt | Tech-savvy early adopters, 5M+ monthly | Launch day spike, press signal, investor signal | High | Day 0 |
| BetaList | Pre-launch beta testers, early adopters | Waitlist building, pre-launch validation | Low | Week -2 to -1 |
| What Launched Today | Casual tech browsers | Secondary launch day traffic | Low | Day 0 |
| Launching.io | Startup watchers | Supplementary visibility | Low | Day 0-1 |

### Developer Platforms

| Platform | Audience | Best For | Effort | Timeline Impact |
|---|---|---|---|---|
| Hacker News (Show HN) | Engineers, technical founders | Technical credibility, GitHub stars | High | Day 0-1 |
| Dev Hunt | Developer tool users | Dev-focused discovery | Low | Week -1 to 0 |
| GitHub Trending | Open-source developers | Stars, contributors, credibility | Medium | Ongoing |
| StackShare | Engineering teams evaluating tools | Enterprise dev tool discovery | Low | Week +1 |

### Indie/Founder Platforms

| Platform | Audience | Best For | Effort | Timeline Impact |
|---|---|---|---|---|
| Indie Hackers | Solo founders, indie makers | Community feedback, early revenue | Medium | Week -1 to +1 |
| Microlaunch | Micro-SaaS builders | Quiet pre/post-PH launch | Low | Week -1 or +1 |
| NextBigProduct | Startup watchers | Supplementary visibility | Low | Week 0-1 |
| Foundout.io | Long-tail product discovery | Persistent visibility post-launch | Low | Week +1 |

### AI/Tech Directories

| Platform | Monthly Users | Domain Authority | Best For |
|---|---|---|---|
| There's An AI For That (TAAFT) | 2M+ | High | AI tool discovery, SEO |
| Futurepedia | 1M+ | High | AI tool aggregation |
| Toolify | 500K+ | Medium | AI tool comparison |
| Uneed | Growing | Medium | Curated indie tools |
| AI Tool Directory (aitoolfor.org) | Growing | Medium | Broad AI tool listing |

### Social Channels

| Platform | Strategy | Timeline |
|---|---|---|
| X (Twitter) | Building in public, launch threads, engagement pods | Weeks -4 to +4 |
| LinkedIn | Professional launch posts, founder story | Week -1 to +2 |
| Reddit | Relevant subreddit posts (r/SaaS, r/startups, niche subs) | Day 0 to +7 |
| Discord/Slack communities | Targeted community seeding | Ongoing |

### Content Channels

| Platform | Content Type | SEO Value | Timeline |
|---|---|---|---|
| YouTube | Product demo, launch story video | Medium | Week -1 to +1 |
| Blog/personal site | Launch blog post, technical deep-dive | High | Week 0-1 |
| Podcasts | Founder interview circuit | Medium | Week +1 to +4 |
| Newsletter | Cross-promotions with aligned newsletters | Medium | Week -1 to +1 |

### Paid/Review Platforms

| Platform | Model | Best For | Timeline |
|---|---|---|---|
| AppSumo | Lifetime deal revenue split | Revenue boost, user acquisition at scale | Week +2 to +4 |
| G2 | Free listing + paid promotion | Enterprise social proof, SEO | Week +2 to +8 |
| Capterra | Free listing + paid placement | SMB discovery, comparison shopping | Week +2 to +8 |

Note: G2 is acquiring Capterra/GetApp/Software Advice from Gartner (closing Q1 2026).

---

## Launch Sequence Framework

```
Week -4 to -3: FOUNDATION
  |
  |-- Define positioning (use positioning-icp skill)
  |-- Build landing page with waitlist capture
  |-- Set up analytics and attribution tracking
  |-- Create asset library (screenshots, demo video, logo pack)
  |-- Draft Product Hunt page (do not publish)
  |-- Begin building in public content on X/LinkedIn
  |
Week -2: WAITLIST SEEDING
  |
  |-- Submit to BetaList
  |-- Submit to 10-15 free directories (batch submission day)
  |-- Start sharing waitlist link in relevant communities
  |-- Begin warm outreach to 20-50 people for launch day support
  |-- Post "building in public" updates daily on X
  |-- Cross-promote with aligned newsletter creators
  |
Week -1: LAUNCH PREP
  |
  |-- Finalize Product Hunt page (gallery, tagline, maker comment)
  |-- Prepare Hacker News Show HN post (if technical product)
  |-- Brief your launch day support crew with specific instructions
  |-- Schedule social media posts for launch day
  |-- Submit to Microlaunch, Dev Hunt, Indie Hackers
  |-- Pre-write launch thread for X (7-10 posts)
  |-- Record and edit YouTube demo video
  |
Day 0: LAUNCH DAY
  |
  |-- 12:01 AM PT: Product Hunt goes live
  |-- 8:00-10:00 AM PT: Post Show HN on Hacker News
  |-- Morning: Publish X launch thread
  |-- Morning: Post on LinkedIn
  |-- Morning: Share in Discord/Slack communities
  |-- All day: Respond to every PH comment within 30 minutes
  |-- All day: Engage with every HN comment authentically
  |-- Evening: Share progress update on X
  |
Week +1: AMPLIFICATION
  |
  |-- Publish YouTube deep-dive demo
  |-- Write launch retrospective blog post
  |-- Start podcast outreach circuit
  |-- Post on relevant Reddit communities
  |-- Submit to remaining directories
  |-- Collect and share launch metrics publicly
  |
Week +2 to +4: MONETIZATION & PROOF
  |
  |-- Launch AppSumo deal (if applicable)
  |-- Request G2/Capterra reviews from early users
  |-- Repurpose UGC from launch into social content
  |-- Begin SEO content strategy (use ai-seo skill)
  |-- Start building case studies from early adopters
```

---

## Product Hunt Deep Dive

### How the 2025-2026 Algorithm Works

Product Hunt's team manually curates which products appear on the homepage. They evaluate
products on four factors:

1. **Useful** - solves a real problem
2. **Distinctive** - clearly different from existing solutions
3. **User-Friendly** - polished, easy to try
4. **Complete** - feels like a finished product, not a landing page

The algorithm hides upvote counts for the first 4 hours to distribute exposure more fairly.
Early velocity still matters, but gaming is harder than before.

### Product Hunt Launch Page Anatomy

| Element | Requirements |
|---|---|
| Title | 60-70 chars, customer-focused, communicate value without context |
| Tagline | One sentence reinforcing the title's value proposition |
| Gallery | 4-6 images or GIF/video; first image is hero; show product in use |
| Description | What it does (1 sentence), who for (1 sentence), differentiator (1 sentence) |
| Maker Comment | Story behind building it, why this moment matters, invite feedback |

### Title Strategy: Three Variants

Prepare three title options with distinct angles:

| Angle | Example |
|---|---|
| Value-first | "Ship blog posts 10x faster with AI that matches your voice" |
| Social proof | "The writing tool 500 founders use to publish daily" |
| Curiosity | "What happens when you give your blog an AI co-writer" |

Test these with 5-10 people before launch. Pick the one with the strongest immediate reaction.

### Launch Day Execution Roles

For teams of 2+, assign these roles explicitly:

| Role | Responsibility |
|---|---|
| Thread Owner | Responds to every PH comment within 30 min |
| Social Driver | Posts updates on X, LinkedIn, communities |
| Support Lead | Handles signups, onboarding, bug reports |
| Metrics Tracker | Monitors upvotes, rank position, traffic |

Solo founders: prioritize Thread Owner and Social Driver. Let support queue until evening.

### Performance Benchmarks (2025)

| Metric | Good | Great | Top 5 |
|---|---|---|---|
| Upvotes | 150-300 | 300-600 | 600-900+ |
| Comments | 30-60 | 60-120 | 120+ |
| Launch day signups | 200-500 | 500-1500 | 1500+ |
| Traffic spike | 2K-5K visits | 5K-15K | 15K+ |

Products in the top 6 appear on the first page without scrolling. This is the target.

### What to Avoid on Product Hunt

Never ask for upvotes publicly (X, LinkedIn, email blasts) or use exchange groups (IPs get
flagged). Avoid Monday/Friday launches (low engagement). Do not launch a landing page with
no working product. Always respond to comments (responsiveness affects ranking).

---

## Hacker News (Show HN) Deep Dive

### What Works on HN

Show HN is for things people can run, use, or interact with. Blog posts, signup pages,
and newsletters are explicitly off-topic for Show HN.

**Ideal post types:**
- Live demo with no signup required
- Open-source tool with GitHub repo
- Technical deep-dive with benchmarks
- Novel approach to a known problem

**Title formula:**
Front-load a concrete benefit or intrigue. Use digits, version numbers, or specific results.
Avoid superlatives, listicle formats, and clickbait.

Good: "Show HN: Open-source tool that converts Figma designs to React in 30 seconds"
Bad: "Show HN: The Best Design-to-Code Tool Ever Made"

### Timing

| Window | Why |
|---|---|
| Tue-Thu, 8:00-10:00 AM PT | Engineers check news before standup |
| Sunday, 6:00-9:00 PM PT | Low competition, relaxed browsing |

Check hn.algolia.com before posting to verify your slot is not crowded by major stories.

### Algorithm Mechanics

HN uses time-decayed scoring. The gravity multiplier increases every ~45 minutes. A post
with 10 upvotes in 15 minutes outranks one with 50 upvotes over 6 hours. Early velocity
is everything.

### Early Upvote Sources (Legitimate)

Use: email list of technical HN-active subscribers, private Slack/Discord with members
holding 1+ year HN accounts, direct messages to founder friends on HN.

Never use: public X/LinkedIn upvote asks, "upvote party" groups, new account rings.
Shadow-banning is aggressive and permanent.

### HN Performance Benchmarks

| Result | Points | What You Get |
|---|---|---|
| Front page (1hr) | 10-20 | ~500 visits, 20-50 GitHub stars |
| Front page (4hrs) | 30-80 | ~2K-5K visits, 50-121 GitHub stars |
| Front page (12hrs+) | 100+ | 5K-20K visits, major credibility signal |

Expect brutally honest feedback. Respond to criticism thoughtfully and you earn respect.

---

## Waitlist Building Playbook

Waitlist-driven launches convert at 25-85% vs. 2-4% for cold launches, with near-zero
customer acquisition cost. AI-powered waitlist optimization adds ~30% to conversion rates.

### Waitlist Architecture

Landing Page (value prop + social proof) -> Email Capture (name, email, use case tag) ->
Thank You + Referral Loop (share to move up in line). Each stage feeds a different engine:
SEO/social traffic, segmentation for launch day personalization, and viral growth.

### Referral-Based Waitlist Growth

The highest-performing waitlists use tiered referral rewards:

| Referrals | Reward |
|---|---|
| 1 | Early access (move up the line) |
| 3 | Extended free trial or bonus feature |
| 5 | Lifetime discount or founding member status |
| 10 | Direct call with founder, input on roadmap |

Tools: LaunchList (getlaunchlist.com), Waitlister, Viral Loops, ReferralHero

### Waitlist Conversion Tactics

Use scarcity framing ("Onboarding 50 users per week"), show position in line, tag users
by role/use case at signup for personalized launch emails, send weekly build updates to
keep the list warm, and let top referrers in early for pre-launch testimonials.

### Waitlist Size Benchmarks

| Product Stage | Target Waitlist | Conversion Expectation |
|---|---|---|
| Pre-MVP validation | 100-500 | 40-60% to beta signup |
| MVP ready | 500-2000 | 30-50% to active user |
| Product-market fit | 2000-10000 | 25-40% to paid/active |
| Scaled launch | 10000+ | 15-30% to paid |

---

## Directory Submission Strategy

### Batch Submission Approach

Set aside 2-3 hours and submit to multiple directories in one session. Prepare these
assets in advance:

**Required assets for all directories:**
- Product name and one-line description (< 100 chars)
- Full description (150-300 words, keyword-rich)
- Logo (square, 512x512 PNG minimum)
- 3-5 product screenshots (1280x800 or larger)
- Product URL
- Category tags (3-5 relevant categories)
- Pricing info (free tier, pricing page URL)
- Founder/maker social profiles

### Directory Tiers

**Tier 1 - High Impact (submit first):**
- Product Hunt
- Hacker News (Show HN)
- There's An AI For That (for AI products)
- Futurepedia (for AI products)
- G2 / Capterra
- BetaList

**Tier 2 - Medium Impact (submit in week -1 to 0):**
- Indie Hackers
- Dev Hunt (developer tools)
- Microlaunch
- Toolify (AI tools)
- Uneed
- AlternativeTo

**Tier 3 - Long-Tail SEO (submit in week +1 to +2):**
- SaaSHub
- StackShare
- Crunchbase
- GetApp / Software Advice
- Awesome lists on GitHub (for open source)
- Niche-specific directories for your category

### Directory Listing Optimization

Front-load primary keyword in title and first sentence. Match feature descriptions to the
directory's filter categories. Include social proof (user count, testimonials). Use polished
screenshots (directories with thumbnails favor visual quality). Pick the most specific
category available, not the broadest.

---

## AppSumo Launch Strategy

### When to Use AppSumo

AppSumo lifetime deals work best when:

- You need a cash injection for development ($10K-$100K+ in first month is common)
- You want to rapidly grow your user base for social proof
- Your product has low marginal cost per user (not per-API-call AI tools)
- You can handle a sudden spike in support volume
- You have upsell paths beyond the lifetime tier

### When to Avoid AppSumo

- Your product has high per-user marginal costs (heavy API usage, compute)
- You cannot handle 500-2000+ new users in a week
- You have no upsell or expansion revenue model
- You are pre-product-market-fit (LTD users give loud feedback on unfinished products)

### AppSumo Deal Structure

| Element | Recommendation |
|---|---|
| Pricing | $49-$79 one-time for Tier 1 |
| Tiers | 3 tiers with stacking codes |
| Feature limits | Cap AI/API usage with credits; offer BYOK option |
| Duration | 30-60 day deal window |
| Revenue split | 70% to you (first deal), negotiate for subsequent |

### AI Tool Considerations (2025-2026)

Many AI-based lifetime deals have failed because API costs (OpenAI, Anthropic) create
ongoing per-use expenses. Strategies to mitigate:

1. **Credit bundles** - Include monthly credit refresh, not unlimited usage
2. **BYOK (Bring Your Own Key)** - Let users connect their own API keys
3. **Usage tiers** - Cap usage per plan tier with clear limits
4. **Annual refresh** - Structure as "lifetime access with annual credit renewal"

### AppSumo Launch Checklist

Prepare infrastructure for 5x traffic, staff up support or build self-serve docs, create
AppSumo-specific onboarding flow, set up separate analytics segment, prepare upsell paths
for power users, write LTD buyer FAQ, and plan early Taco (review) collection.

---

## G2 and Capterra Strategy

**Ranking formula:** Get to ~100 reviews fast, maintain 3-4 new positive reviews per month,
respond to every review, optimize your profile for the category's feature filters.

**Review generation by tactic:**
- Post-support-resolution email: 15-25% response rate
- In-app prompt after milestone: 10-20% response rate
- Incentivized review (G2 gift card program): 20-30% response rate

**Paid placement:** G2 starts at ~$1K/month for category placement + intent data.
Capterra runs PPC at ~$2/click. Free listings still work with strong review volume.

---

## UGC-Only Growth: $0 Ad Spend Scaling

### The UGC Launch Flywheel

Make product shareable -> Users create content -> Repurpose as social proof/ads ->
More users discover product -> Improve shareability triggers based on what performs -> Repeat.

### Making Your Product Shareable

1. **Screenshot-worthy UI** - Design moments users want to share (results screens, dashboards)
2. **Built-in sharing triggers** - "Share your results" buttons, public profile pages
3. **Template the format** - Create a repeatable content format users can fill in
4. **Badge/certification outputs** - Generate shareable badges users display in bios/websites
5. **Before/after framing** - Show transformation that creates "how did you do that?" reactions

### UGC Performance Benchmarks (2025)

- UGC ads get 4x higher click-through rates vs. branded ads
- UGC costs 30-80% less than influencer marketing
- Brands report $4 return for every $1 invested in UGC programs
- 50% lower cost-per-click on UGC-based paid campaigns

### Zero-Budget UGC Tactics for Launch

| Tactic | Cost | Expected Output |
|---|---|---|
| "Show your setup" challenge on X | $0 | 20-50 posts from early users |
| Template/swipe file with branding | $0 | Passive shares as users use templates |
| Founding member badge for profiles | $0 | Social proof in user bios |
| Public roadmap with voting | $0 | Community engagement content |
| User spotlight in your newsletter | $0 | Incentivizes others to share |

Cross-reference: ai-ugc-ads skill for scaling UGC into paid campaigns.

---

## Budget Decision Framework

| Budget | Key Additions | Expected Results |
|---|---|---|
| **$0 Bootstrap** | Carrd/Notion landing page, build-in-public on X, BetaList, PH, Show HN, 15-20 free directories, Reddit/communities | 500-3K signups, 1K-10K visits |
| **Under $500** | + Custom landing page template, demo video (self-recorded), email nurture tool, LaunchList referral waitlist, newsletter swaps | 1K-5K signups, 3K-20K visits |
| **Under $5K** | + Professional video ($500-1500), paid newsletter sponsorships, AppSumo deal, G2/Capterra paid placement, micro-influencer seeding, PR service | 3K-15K signups, 10K-50K visits |

---

## Platform-Specific Timing

| Platform | Best Days | Best Time | Why |
|---|---|---|---|
| Product Hunt | Tue, Wed, Thu | 12:01 AM PT | Algorithm reset; midweek peak traffic |
| Hacker News | Tue-Thu | 8-10 AM PT | Pre-standup browsing; high early velocity |
| Hacker News (alt) | Sunday | 6-9 PM PT | Low competition window |
| LinkedIn | Tue-Thu | 7-9 AM local | Professional morning scroll |
| X (Twitter) | Tue-Thu | 8-10 AM PT | Engagement peaks |
| Reddit | Mon-Wed | 6-9 AM PT | Fresh content for US morning |

### Launch Day Hour-by-Hour

- **12:01 AM PT** - PH goes live; share link with inner circle via DM only
- **6:00 AM PT** - Check PH position, respond to overnight comments
- **8:00 AM PT** - Post Show HN, publish X thread, post LinkedIn, share in communities
- **10:00 AM PT** - Reddit posts, send launch email to waitlist
- **12:00 PM PT** - Midday engagement check, share early metrics on X
- **3:00 PM PT** - Respond to all new PH/HN comments
- **6:00 PM PT** - Evening progress update on X
- **9:00 PM PT** - Final PH comment sweep, plan Day 1 content

---

## Measuring Launch Success

### Core Launch Metrics

| Metric | What It Tells You | Target (Good Launch) |
|---|---|---|
| Total signups (Day 0) | Demand signal | 200-1000 |
| Total signups (Week 1) | Sustained interest | 500-3000 |
| Activation rate | Product-market fit signal | 30-60% |
| PH rank | Social proof tier | Top 5 of the day |
| HN points | Technical credibility | 50+ |
| Waitlist conversion | Pre-launch quality | 25-50% |
| Directory referral traffic | Long-tail value | 100+ visits/month |
| Email list growth | Owned audience | 500-2000 new subs |
| Social mentions | Word of mouth | 50+ unique mentions |
| Reviews collected (G2/Capterra) | Buyer confidence | 10-20 in first month |

### Attribution Tracking

Set up before launch: UTM parameters on every shared link, separate landing pages or
query params per platform, referral source tracking (Plausible, PostHog, Mixpanel),
PH referral data, and HN traffic spike correlation.

### 7-Day Post-Launch Review

Run this review one week after launch. Cover: results vs. goals (signups, activation,
revenue), per-platform performance (PH rank/upvotes, HN points, directory referrals,
social mentions, email growth), top 3 things that worked, top 3 to improve, and next
30-day action items.

---

## Common Launch Mistakes

| Phase | Mistake | Fix |
|---|---|---|
| Pre-launch | No waitlist before launch | Collect emails 4+ weeks early |
| Pre-launch | Launching a landing page, not a product | Ship working MVP first |
| Pre-launch | No supporter coordination | Brief 20-50 people with specific instructions |
| Pre-launch | Same messaging across platforms | Customize tone per platform norms |
| Day 0 | Publicly asking for upvotes | Private DMs only, never public posts |
| Day 0 | Not responding to comments | Reply to every comment within 30 min |
| Day 0 | Launching on Friday | Launch Tue-Thu for peak traffic |
| Day 0 | No live demo available | Offer instant try-it-now experience |
| Post-launch | Going silent after Day 0 | Post daily updates for Week +1 |
| Post-launch | Not collecting reviews | Ask every active user for G2/Capterra review |
| Post-launch | Skipping directory submissions | Batch-submit to 15-20 directories |

---

## Quick Reference Checklists

**2 Weeks Before:** Landing page + waitlist live, PH page drafted, BetaList submitted,
asset library complete (logo, screenshots, video), 20-50 supporters briefed, social
content calendar set, UTM tracking configured, X thread drafted, Show HN drafted,
directory assets prepared.

**Launch Day:** PH live at 12:01 AM PT, Show HN at 8-10 AM PT, X thread published,
LinkedIn posted, waitlist email sent, community posts shared, all PH/HN comments
responded to within 30 min, evening progress update shared.

**Week +1:** YouTube demo published, launch retro blog post, podcast outreach sent
(5-10 shows), G2/Capterra profiles created, review requests sent, remaining directories
submitted, launch metrics compiled, 30-day action plan created.

---

## Questions to Ask

When helping a user plan a multi-platform launch:

1. What does your product do, and who is the primary buyer?
2. Do you have an existing audience (email list, social following, community)?
3. What is your launch timeline - when do you want to go live?
4. What is your budget for launch activities?
5. Is this a first launch or a relaunch with significant updates?
6. Do you have a working product or is this pre-MVP waitlist building?
7. Are you targeting developers, business users, or consumers?
8. Do you want to prioritize signups, revenue, press coverage, or all three?
9. Have you launched on Product Hunt or Hacker News before?
10. Do you have 20+ people who would support your launch on Day 0?

---

## Related Skills

- **positioning-icp** - Define your positioning and ICP before crafting launch messaging
- **ai-seo** - Build long-tail SEO strategy post-launch using directory backlinks
- **social-selling** - Convert launch buzz into pipeline and sales conversations
- **content-to-pipeline** - Turn launch content into ongoing lead generation
- **ai-ugc-ads** - Scale user-generated launch content into paid campaigns
- **solo-founder-gtm** - Adapted launch playbook for one-person teams
