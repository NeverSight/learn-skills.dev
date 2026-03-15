---
name: anysite-person-analyzer
description: Deep multi-platform intelligence analysis combining LinkedIn (profile, posts, activity), Twitter/X (tweets, engagement), Reddit (discussions, community), web presence (articles, GitHub, blogs), and company intelligence. Use when analyzing people for networking, sales, partnerships, or recruitment. Accepts LinkedIn URL or name+context. Produces comprehensive cross-platform reports with conversation strategies and strategic value assessment for AnySite.
---

# Person Intelligence Analyzer

Comprehensive multi-platform intelligence analysis combining LinkedIn, Twitter/X, Reddit, GitHub, and web presence data to create actionable intelligence reports with cross-platform personality insights.

## Analysis Workflow

Execute phases sequentially, adapting depth based on available data and user requirements.

### Phase 1: Initial Data Collection

**Starting with LinkedIn Profile URL:**
1. Use `get_linkedin_profile` with full parameters (education, experience, skills)
2. Extract and save the **full URN** (format: `urn:li:fsd_profile:ACoAAABCDEF`) - this is critical for all subsequent API calls
3. Also extract: company URN, current role, location, connections count
4. Record profile completeness for confidence scoring

**IMPORTANT - URN Format:** 
Always use the complete URN format `urn:li:fsd_profile:ACoAAABCDEF` from the profile response for all subsequent calls to `get_linkedin_user_posts`, `get_linkedin_user_comments`, and `get_linkedin_user_reactions`. Do not use shortened versions or profile URLs.

**Starting with Name + Context:**
1. Use `search_linkedin_users` with all available filters:
   - Name, title, company keywords, location, school
2. If multiple matches: present top 3-5 candidates with distinguishing details
3. After user confirmation, proceed with confirmed profile

**Critical Data Points to Capture:**
- Current company and role (with start date)
- Previous roles (last 2-3 positions)
- Education background
- Skills and endorsements
- Connection count (indicator of network size)
- Profile headline and summary

### Phase 2: Activity & Engagement Analysis

**Content Analysis (Posts):**
1. Use `get_linkedin_user_posts` with the full URN (format: `urn:li:fsd_profile:ACoAAABCDEF`)
   - Count: 20-50 depending on activity level
   - Posted after filter: last 90 days for active users, 180 days if low activity
2. Analyze for:
   - Topics and themes (use clustering: technical, leadership, industry trends, personal)
   - Engagement metrics (likes, comments per post - calculate averages)
   - Posting frequency (calculate posts per week/month)
   - Content style (thought leadership, sharing, personal stories, company updates)
   - Language and tone

**Engagement Analysis (Comments & Reactions):**
1. Use `get_linkedin_user_comments` with the full URN (format: `urn:li:fsd_profile:ACoAAABCDEF`)
   - Count: 30
2. Use `get_linkedin_user_reactions` with the full URN (format: `urn:li:fsd_profile:ACoAAABCDEF`)
   - Count: 50
3. Analyze for:
   - Who they engage with (seniority levels, industries)
   - Topics that spark their engagement
   - Engagement style (supportive, challenging, informational)
   - Response patterns (quick reactions vs thoughtful comments)

**CRITICAL:** All three tools (`get_linkedin_user_posts`, `get_linkedin_user_comments`, `get_linkedin_user_reactions`) require the complete URN in the format `urn:li:fsd_profile:ACoAAABCDEF` obtained from Phase 1. Using LinkedIn profile URLs or partial URNs will result in errors.

**Output: Engagement Profile**
- Primary content themes (ranked by frequency)
- Engagement level: High/Medium/Low (posts per month, reactions per week)
- Influence indicators: follower count, average post engagement rate
- Communication style: formal/casual, technical/general, etc.

### Phase 3: Company Intelligence

**Current Company Deep Dive:**
1. Use `get_linkedin_company` with company URN from profile
2. Extract:
   - Company size, industry, specialties
   - Growth indicators (employee count trends if available)
   - Company description and mission
   - Recent updates/news

3. Use `get_linkedin_company_posts` (count: 20)
   - Analyze company communication themes
   - Identify strategic priorities
   - Note any mentions of funding, hiring, expansion

4. Use `duckduckgo_search` for recent news:
   - "[Company name] funding news"
   - "[Company name] expansion launch product"
   - Prioritize results from last 6 months

**Company Social Media Presence:**

5. **Company Twitter/X Analysis:**
   - Use `search_twitter_users` to find official company account: "[Company Name] official"
   - If found, use `get_twitter_user` for profile stats
   - Use `get_twitter_user_posts` (count: 20-30) to analyze:
     - Product announcements and launches
     - Company culture and values
     - Engagement with customers and community
     - Hiring announcements (growth signals)
     - Technical content (if tech company)
   - Use `search_twitter_posts` for company mentions: "[Company Name]"
     - Customer sentiment (complaints vs praise)
     - Industry discussion about the company
     - Competitor comparisons
     - Notable tweets from employees

6. **Company Reddit Presence:**
   - Use `search_reddit_posts` for company mentions: "[Company Name]"
   - Look for:
     - r/startups discussions about the company
     - Industry-specific subreddit mentions (r/SaaS, r/artificial, etc.)
     - Customer experiences and reviews
     - Technical discussions about their product/platform
     - Hiring experiences (Glassdoor-like insights)
     - Founder/team AMAs or discussions
   - Sentiment analysis: positive/negative/neutral community perception
   - Pain points mentioned by users/customers

**Company Context Analysis:**
- Business model and revenue streams
- Technology stack (if tech company)
- Market position and competitors
- Recent achievements or challenges
- Cultural indicators from company posts
- **Social sentiment** (Twitter mentions, Reddit discussions)
- **Community engagement** (how company responds on social platforms)
- **Growth signals** (hiring tweets, expansion announcements on Twitter)
- **Customer pain points** (Reddit complaints, Twitter issues)

### Phase 4: Multi-Platform Intelligence Enrichment

**A. Twitter/X Analysis (if handle found or identifiable):**

1. **Find Twitter Handle:**
   - Check LinkedIn profile bio/description for @username
   - Use `search_twitter_users` with name if not found: "[First Name] [Last Name] [Company]"
   - Verify match by checking bio, profile description

2. **Profile Analysis:**
   - Use `get_twitter_user` with username
   - Extract: follower count, following count, tweet count, bio, location
   - Note: verification status, profile creation date

3. **Content Analysis:**
   - Use `get_twitter_user_posts` (count: 50-100 recent tweets)
   - Analyze for:
     - Technical expertise signals (code snippets, tech discussions)
     - Industry opinions and hot takes
     - Personal interests and hobbies
     - Engagement with other thought leaders
     - Retweets vs original content ratio
   - Calculate: tweets per day, avg engagement rate

4. **Topic Discovery:**
   - Use `search_twitter_posts` with person's key interests: "[topic] from:@username"
   - Identify recurring themes and expertise areas
   - Note controversial or strongly-held opinions

**B. Reddit Activity (if username discoverable):**

1. **Find Reddit Presence:**
   - Search for username from other platforms
   - Use `search_reddit_posts` with name/company mentions
   - Look for: "AMA" posts, technical discussions, community contributions

2. **Content Analysis:**
   - Use `search_reddit_posts` with username if known: "author:[username]"
   - Analyze for:
     - Subreddit preferences (which communities they're active in)
     - Technical depth of contributions
     - Helping behavior vs self-promotion ratio
     - Community reputation indicators

3. **Topic Expertise:**
   - Use `search_reddit_posts` for specific topics: "[topic] [username or company]"
   - Identify where they're seen as expert/helpful
   - Note any popular posts or discussions they started

**C. Instagram Presence (optional, if B2C relevant or personal brand focus):**

1. **Profile Discovery:**
   - Check if mentioned in LinkedIn or Twitter
   - Use `search_instagram_posts` with hashtags: "#[name] #[company]"
   - Use `get_instagram_user` if handle known

2. **Content Style:**
   - Use `get_instagram_user_posts` (count: 20-30)
   - Analyze for: personal brand vs professional content
   - Note: visual style, posting frequency, engagement rate

**D. Web Intelligence & Media Presence:**

1. **Professional Presence:**
   - `duckduckgo_search`: "[Name] [Company] speaker conference"
   - `duckduckgo_search`: "[Name] interview podcast"
   - `duckduckgo_search`: "[Name] article blog post"

2. **Expertise & Thought Leadership:**
   - `duckduckgo_search`: "[Name] expertise [primary topic from posts]"
   - Check for: publications, talks, media mentions
   - `duckduckgo_search`: "[Name] [key topic] site:medium.com OR site:dev.to OR site:substack.com"

3. **Company-Specific Context:**
   - `duckduckgo_search`: "[Name] [Company] announcement"
   - Look for: press releases, product launches, executive quotes

4. **GitHub/Tech Presence (if technical role):**
   - `duckduckgo_search`: "[Name] site:github.com"
   - Look for: open source contributions, personal projects

**E. Parse Key Pages:**
- Use `parse_webpage` for high-value sources:
  - Personal blog/website (if mentioned in any profile)
  - Recent interviews or podcast appearances
  - Conference speaker profiles
  - Company "About Team" pages
  - Notable Medium/Substack articles
  - Popular Reddit AMAs or discussions
- Extract: bio, expertise areas, quotes, interests, unique perspectives

**Platform Priority Strategy:**

1. **Always analyze:** LinkedIn (mandatory) + Web Search
2. **High priority:** Twitter/X (if found) - usually most revealing for tech audience
3. **Medium priority:** Reddit (if active) - shows technical depth and community engagement
4. **Low priority:** Instagram - only if B2C focus or strong personal brand element
5. **Context-dependent:** GitHub - critical for engineering roles, less for business roles

**Cross-Platform Analysis:**
- Compare tone across platforms (professional LinkedIn vs casual Twitter)
- Identify platform-specific content themes
- Note engagement levels per platform
- Synthesize consistent interests vs platform-specific behavior

### Phase 5: Cross-Platform Strategic Analysis & Report Generation

**Connection Strategy:**
1. **Conversation Topics** (ranked by relevance, synthesized across all platforms):
   - Top 3-5 topics from their LinkedIn posts/comments
   - Hot takes or strong opinions from Twitter/X
   - Technical discussions from Reddit
   - Industry trends they've engaged with across platforms
   - Shared interests or connections (if any)
   - Recent company achievements to acknowledge

2. **Engagement Approach:**
   - Best channels: LinkedIn comment, Twitter reply, Reddit comment, DM, email
   - Channel preference: Note where they're most active/responsive
   - Timing: based on posting patterns per platform (e.g., "most active on Twitter evenings, LinkedIn Tuesday mornings")
   - Ice-breakers: reference specific post/comment/tweet that relates to AnySite
   - Platform-specific tone: professional LinkedIn vs casual Twitter vs technical Reddit

3. **Cross-Platform Personality Synthesis:**
   - Professional persona (LinkedIn) vs Personal persona (Twitter/Reddit)
   - Technical depth indicators (Reddit discussions, GitHub activity)
   - Communication style differences per platform
   - Authentic interests (topics mentioned across multiple platforms)

**Value Assessment for AnySite:**

Analyze fit across multiple dimensions:

**A. Direct Business Value:**
- Potential customer: Does their company match AnySite ICP?
  - B2B SaaS, AI companies, data-intensive businesses
  - Size indicators: 10-500 employees, growth stage
  - Pain points: mentions of data extraction, API integrations, agent development
- Decision maker level: C-suite, VP, Director, Manager
- Budget authority indicators

**B. Partnership Potential:**
- Technology synergies (complementary tools/platforms)
- Channel partnership opportunities
- Integration possibilities
- Co-marketing potential

**C. Network & Influence:**
- Network size and quality (10k+ connections = super-connector)
- Industry influence (thought leader, frequent speaker)
- Investor connections (VC, angels in their network)
- Potential for introductions

**D. Talent & Advisory:**
- Expertise match for advisor/mentor role
- Potential hire for future scaling
- Domain knowledge that fills gaps

**Prioritization Matrix:**
- **Tier 1 (Hot Lead)**: Decision maker + ICP match + high engagement
- **Tier 2 (Warm Lead)**: Mid-level + ICP match OR influencer + relevant network
- **Tier 3 (Long-term Nurture)**: Potential future value, build relationship
- **Tier 4 (Low Priority)**: No clear fit, maintain basic connection

## Output Format

Generate comprehensive markdown report with sections:

```markdown
# Person Intelligence Report: [Name]

**Generated:** [Date]
**Analysis Depth:** [Quick/Standard/Deep]
**Confidence Score:** [0-100%] based on data availability

## Executive Summary
[2-3 sentences: who they are, what they do, why they matter to AnySite]

## Professional Profile
- **Current Role:** [Title] at [Company] (since [date])
- **Location:** [City, Country]
- **Experience:** [X years in industry/role]
- **Education:** [Degree, Institution]
- **Network Size:** [LinkedIn connections count]
- **LinkedIn Profile:** [URL]
- **Twitter/X:** [@handle or "Not found"] ([follower count if found])
- **Reddit:** [u/username or "Not found/searched"]
- **GitHub:** [username or "Not found"] (if technical role)
- **Personal Website:** [URL if found]

## Key Background
[2-3 paragraphs covering:]
- Career trajectory and notable positions
- Expertise and specializations
- Notable achievements or credentials

## Multi-Platform Activity Analysis

### LinkedIn Activity (Last 90 Days)

#### Content Themes
1. **[Theme 1]** (40% of posts)
   - Key topics: [list]
   - Example post: "[quote or summary]"

2. **[Theme 2]** (30% of posts)
   - Key topics: [list]
   
3. **[Theme 3]** (20% of posts)

#### Engagement Patterns
- **Posting Frequency:** [X posts/month]
- **Engagement Rate:** [Average likes, comments per post]
- **Response Style:** [Description]
- **Active Topics:** [Topics they comment on most]

### Twitter/X Activity (if found)

#### Profile Stats
- **Followers:** [count]
- **Following:** [count]
- **Tweets:** [total count]
- **Account Age:** [created date]

#### Content Analysis (Recent 50-100 tweets)
- **Posting Frequency:** [tweets per day/week]
- **Content Mix:** [% original tweets vs retweets vs replies]
- **Primary Topics:** [list top 3-5 themes]
- **Engagement Level:** [avg likes, retweets per tweet]
- **Notable Takes:** [any strong opinions or viral tweets]
- **Technical Depth:** [code snippets, technical discussions level]

#### Community Engagement
- **Engages with:** [types of accounts: VCs, founders, engineers, etc.]
- **Tone:** [professional/casual/humorous/technical]

### Reddit Activity (if found)

#### Subreddit Preferences
- **Most Active In:** [list top 3-5 subreddits]
- **Karma:** [post/comment karma if visible]

#### Contribution Style
- **Activity Type:** [% asking questions vs answering vs discussions]
- **Technical Depth:** [level of detail in technical responses]
- **Community Reputation:** [helpful, expert, casual participant]
- **Notable Contributions:** [any popular posts or helpful answers]

### Cross-Platform Synthesis

#### Personality Comparison
- **LinkedIn Persona:** [professional characteristics]
- **Twitter Persona:** [casual/personal characteristics]
- **Reddit Persona:** [technical/community characteristics]
- **Consistency:** [topics/interests mentioned across platforms]

#### Platform Preferences
- **Most Active:** [which platform has highest activity]
- **Best Engagement:** [where they get most responses]
- **Content Types:** [professional insights on LinkedIn, hot takes on Twitter, deep tech on Reddit]

#### Communication Style
[Synthesized description: formal/casual, technical depth, storytelling approach, cross-platform consistency or variation]

## Company Intelligence: [Company Name]

### Company Overview
- **Industry:** [Sector]
- **Size:** [Employee count]
- **Stage:** [Startup/Scale-up/Enterprise]
- **Mission:** [Brief description]
- **Twitter:** [@handle or "Not found"] ([follower count if found])
- **Reddit Presence:** [Active/Mentioned/Not found]

### Strategic Context
- **Recent News:** [Key developments from last 6 months]
- **Growth Indicators:** [Hiring, funding, expansion signals]
- **Market Position:** [Brief competitive context]
- **Technology Focus:** [If relevant]

### Company LinkedIn Content Analysis
[Themes from company LinkedIn posts, strategic priorities]

### Company Social Media Presence

#### Twitter/X Activity (if found)
- **Account Stats:** [Followers, following, tweets]
- **Content Mix:** [Product announcements, culture, technical content, engagement]
- **Recent Highlights:** [Key tweets from last 30 days]
- **Posting Frequency:** [tweets per week]
- **Engagement Level:** [avg likes, retweets]
- **Notable Announcements:** [Hiring, funding, launches]

#### Reddit Community Sentiment (if mentioned)
- **Primary Subreddits:** [Where company is discussed]
- **Discussion Volume:** [Number of mentions found]
- **Sentiment Analysis:** [Positive/Mixed/Negative - with examples]
- **Common Topics:**
  - **Praise:** [What users like]
  - **Complaints:** [Pain points mentioned]
  - **Questions:** [What people ask about]
- **Notable Threads:** [Links to significant discussions]

#### Social Intelligence Synthesis
- **Brand Perception:** [How company is viewed on social vs LinkedIn]
- **Customer Insights:** [Real feedback from Twitter/Reddit vs official messaging]
- **Growth Signals:** [Hiring activity, expansion mentions across platforms]
- **Cultural Indicators:** [Company values in practice vs stated]
- **Competitive Context:** [How they're compared to competitors on social]

## External Intelligence

### Web Presence
- **Speaking/Conferences:** [List if any]
- **Publications/Interviews:** [List if any]
- **Blog Posts/Articles:** [Medium, Substack, Dev.to, personal blog]
- **Media Mentions:** [Notable press mentions]
- **GitHub Projects:** [Open source contributions, personal projects if technical]

### Technical Footprint (if applicable)
- **GitHub Activity:** [contribution level, popular repos]
- **Stack Overflow:** [reputation, areas of expertise]
- **Technical Writing:** [blog posts, tutorials, documentation]

### Additional Context
[Insights from parsed webpages, quotes, expertise areas, unique perspectives]

## Connection Strategy

### Recommended Conversation Topics
1. **[Topic 1]** - [Why: specific post/tweet/comment from which platform]
2. **[Topic 2]** - [Why: company context or cross-platform theme]
3. **[Topic 3]** - [Why: shared interest/industry trend across platforms]
4. **[Topic 4]** - [Why: technical interest from Reddit/GitHub]
5. **[Topic 5]** - [Why: personal interest from Twitter]

### Platform-Specific Engagement

**LinkedIn:**
- **Timing:** [Best days/times based on activity]
- **Approach:** [Professional, comment on specific post]
- **Ice-breaker:** "[Example referencing their LinkedIn content]"

**Twitter/X** (if active):
- **Timing:** [Best days/times]
- **Approach:** [Casual reply to tweet, quote tweet with value-add]
- **Ice-breaker:** "[Example referencing their tweet or discussion]"

**Reddit** (if active):
- **Timing:** [When they're most active]
- **Approach:** [Helpful comment in their frequented subreddit]
- **Ice-breaker:** "[Technical question or insight in relevant subreddit]"

**Direct Outreach:**
- **Best Channel:** [Email/LinkedIn DM/Twitter DM - ranked by likelihood]
- **Timing:** [Optimal day/time synthesized from all platforms]
- **Value Proposition:** [How to position AnySite relevance based on their interests]

### Potential Pain Points
[Inferred from their role, company, posts across platforms - where AnySite could help]
- [Pain point 1 with evidence from platform]
- [Pain point 2 with evidence from platform]
- [Pain point 3 with evidence from platform]

## Strategic Value for AnySite

### Primary Classification
**[Tier 1/2/3/4]: [Customer/Partner/Influencer/Advisor/Talent]**

### Value Dimensions
**Customer Potential:** [High/Medium/Low]
- ICP Fit: [Yes/No - reasoning]
- Decision Authority: [Level]
- Buying Signals: [List any indicators]

**Partnership Potential:** [High/Medium/Low]
- [Specific opportunities if any]

**Network Value:** [High/Medium/Low]
- [Influence level, connection value]

**Advisory/Talent Value:** [High/Medium/Low]
- [Specific expertise value]

### Action Priority
**Priority Level:** [Critical/High/Medium/Low]
**Recommended Timeline:** [Contact within: X days/weeks]

### Next Steps
1. [Specific action item with reasoning]
2. [Follow-up action]
3. [Long-term nurture plan if applicable]

## Analysis Metadata
- **Platforms Analyzed:**
  - LinkedIn: [✓ Profile, Posts, Comments, Reactions]
  - Twitter/X: [✓ Found and analyzed / ✗ Not found / - Not searched]
  - Reddit: [✓ Activity found / ✗ No activity / - Not searched]
  - GitHub: [✓ Projects found / ✗ Not found / - Not applicable]
  - Web: [✓ Articles/interviews found]
- **Data Sources:** [List specific tools used]
- **Data Freshness:**
  - LinkedIn posts: [date range analyzed]
  - Twitter: [date range if analyzed]
  - Reddit: [date range if analyzed]
- **Total Data Points:** [approximate: X posts, Y tweets, Z comments analyzed]
- **Confidence Factors:**
  - Profile completeness: [High/Medium/Low]
  - Activity data: [High/Medium/Low - per platform]
  - External validation: [High/Medium/Low]
  - Cross-platform consistency: [High/Medium/Low]
- **Limitations:** [Any data gaps, platforms not accessible, or constraints]
```

## Error Handling & Edge Cases

**Insufficient Data:**
- If posts/comments are minimal: focus more on company analysis and role-based inferences
- If profile is sparse: use web search more heavily
- If company is small/unknown: focus on person's expertise and network

**Multiple Profile Matches:**
- Always confirm with user before proceeding with deep analysis
- Present distinguishing factors clearly

**Rate Limiting / API Errors:**
- Continue with available data from other sources
- Note limitations in report
- Suggest manual verification steps

**Privacy Considerations:**
- Only analyze publicly available information
- No speculation on private/personal matters
- Focus on professional context

## Customization Parameters

Users may request analysis depth adjustment:

**Quick Analysis (10-15 min):**
- LinkedIn: Profile + last 10 posts + company basics
- Company: LinkedIn company profile only
- Twitter/X: Person profile check only (if handle found)
- Web: 2-3 targeted searches
- Reddit/GitHub: Skip unless specifically requested
- Output: Essential info only

**Standard Analysis (20-30 min) - DEFAULT:**
- LinkedIn: Full profile + 20-50 posts + comments/reactions + company analysis
- **Company: LinkedIn + Twitter account + Reddit mentions search** (NEW)
- Twitter/X: Person profile + 50 recent tweets (if found)
- Reddit: Search for person username + activity (if found)
- Web: 5-7 strategic searches + parse 2-3 key pages
- GitHub: Quick check for presence (if technical role)
- Output: Full workflow as described above

**Deep Dive (45-60 min):**
- LinkedIn: Extended analysis (100+ posts), all activity types, detailed company research
- **Company: LinkedIn + Twitter (30 posts) + Reddit (comprehensive mentions) + sentiment analysis** (NEW)
- Twitter/X: Person 100+ tweets, thread analysis, engagement patterns (if found)
- Reddit: Person comprehensive comment history, subreddit analysis (if found)
- Web: 10-15 searches, parse 5-10 webpages, deep technical footprint
- GitHub: Detailed repo analysis, contribution patterns (if technical)
- Instagram: Profile and content analysis (if relevant)
- Output: Comprehensive cross-platform synthesis with deep insights

**Platform-Specific Focus:**
Users can also request focus on specific platforms:
- "Focus on Twitter presence" → Deep Twitter analysis for person AND company, standard LinkedIn
- "Technical profile only" → LinkedIn + GitHub + Reddit + Stack Overflow (person focused)
- "Business profile" → LinkedIn + web presence + media, skip Reddit/GitHub
- **"Company deep dive" → Extended company social analysis across all platforms** (NEW)

Default to **Standard Analysis** unless specified.
