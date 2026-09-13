---
name: find-vc-backed-ai-jobs-munich
description: Discover, evaluate, deduplicate, and store VC-backed AI startup jobs in Munich, Germany, and nearby/remote markets using web search, browser extraction, and a tracker or Notion database.
---

# Find VC-Backed AI Jobs In Munich

## Purpose

Use this skill to find roles at VC-backed AI companies in Munich, Germany, DACH, or remote Europe, then evaluate and store them in a tracker or Notion database.

The skill is role-flexible. It should search across adjacent titles, not only one narrow title family.

Good target role families include:

- Forward Deployed Engineer
- AI Engineer
- Applied AI Engineer
- Agentic AI Engineer
- AI Solutions Engineer
- Solutions Engineer
- Deployment Engineer
- Customer Engineer
- Implementation Engineer
- Product Engineer
- Founding Engineer
- Developer Productivity Engineer
- Internal AI Platform Engineer

## Source Discovery Methods

### 1. Similar-company graph

Use known relevant companies as seed nodes, then expand through:

- LinkedIn similar pages
- people also viewed/followed sections
- founder/investor networks
- alumni/follower overlap
- related companies in the same domain

Workflow:

```text
Seed company
-> related companies
-> company website
-> careers page
-> relevant roles
-> tracker/database
```

Do not overfit to the seed company. Use it to discover a market cluster.

### 2. Direct web search by title and location

Search broad combinations of role family, AI domain, and location:

```text
Forward Deployed AI Engineer jobs Munich
Forward Deployed Engineer AI Germany
Agentic AI Engineer Munich
AI Solutions Engineer GenAI Munich
AI Deployment Engineer Germany
AI Engineer MCP Claude Code Codex Germany
Forward Deployed GenAI Engineer Germany
AI Product Engineer Munich startup
Founding AI Engineer Munich
AI Implementation Engineer Germany startup
```

Use aggregators as discovery layers, then prefer the original company or ATS page.

### 3. Startup and company list portals

Search for company lists, not only job listings:

```text
top AI startups Munich 2026
best funded AI startups Munich
Munich GenAI startups
Germany AI startups funding 2026
B2B AI startups Munich
AI agent startups Germany
procurement AI startups Germany
industrial AI startups Germany
```

Workflow:

```text
Find funded/startup list
-> extract company names, domain, funding, location
-> open company sites
-> inspect careers pages
-> add relevant roles
```

### 4. VC portfolio job boards

Search portfolio pages and job boards from global and European VCs that invest in German or European startups.

Useful sources include:

- a16z
- Sequoia Capital
- Accel
- Index Ventures
- Lightspeed
- General Catalyst
- Northzone
- Atomico
- Balderton
- Cherry Ventures
- La Famiglia / General Catalyst
- Earlybird
- HV Capital
- UVC Partners
- Picus Capital
- Project A
- Cavalry Ventures
- Lakestar
- Point Nine
- Visionaries Club
- Speedinvest
- Creandum
- Headline
- LocalGlobe
- EQT Ventures

Workflow:

```text
Open VC portfolio/jobs page
-> filter Germany / Munich / Berlin / DACH / EU remote
-> filter Engineering / AI / Product / Solutions / Customer Engineering
-> search titles with AI, GenAI, Agent, Forward Deployed, Solutions, Deployment, Productivity
-> add relevant roles
```

### 5. Specialized job boards

Use specialist boards where startup and AI roles appear:

- Y Combinator jobs
- Wellfound
- FWDDeploy
- Ashby-powered career pages
- Lever-powered career pages
- Welcome to the Jungle
- Munich Startup job board
- Join.com startup listings

## Tool Selection

Use `opportunity-tool-selection` before choosing tools.

Default pattern:

```text
web search for discovery
-> browser automation for dynamic job boards
-> MCP/API for tracker or Notion updates
-> local files for private profile and logs
```

Do not use browser automation to edit Notion when Notion MCP/API tools are available.

## Deduplication

Before adding a role, search the tracker/database by:

- company name + role title
- company name + job URL
- job URL domain/path

If a likely duplicate exists, update it instead of creating a new row.

## Fields To Capture

Capture at minimum:

- Role
- URL
- Company
- Status
- Priority Score
- Rationale
- Role Family
- Location
- Salary Range
- Salary Rationale
- Source

`Status` is an application pipeline state, not a fit label. Use `Priority Score` and `Rationale` for fit.

Recommended status values:

- Needs enrichment
- Enriching
- Backlog
- To do
- In progress
- Human blocked
- Ready to apply
- Submitted
- Waiting for response
- Interview invite
- Interview scheduled
- Interview completed
- Assessment received
- Assessment in progress
- Assessment submitted
- Rejected
- Closed

Use `Needs enrichment` for newly discovered roles that have not yet been scored and researched. Use `Enriching` while an agent is filling fit, score, rationale, salary, and source fields. Use `Backlog` only after the row is enriched enough to rank. Use `To do` only after a role is intentionally selected for the next application batch.

Before full enrichment, confirm access to candidate context: resume or experience evidence, target role preferences, location/remote constraints, compensation expectations if relevant, and dealbreakers. If context is unavailable, ask whether to perform partial public-only enrichment. Partial enrichment can fill company, role family, location, salary, salary rationale, source, and public notes, but should not invent fit rationale or priority score.

Minimum enrichment before `Backlog`:

- valid URL
- company
- role family
- location
- priority score
- consolidated rationale
- source
- salary range if credible, otherwise blank
- salary rationale explaining source, confidence, or unknown salary

## Scoring

Use a 0-100 priority score:

- 90-100: strong role and company fit, credible application target
- 75-89: relevant and worth review
- 60-74: adjacent or stretch, useful if pipeline needs volume
- 40-59: benchmark, closed, too senior, or weak fit
- 0-39: archive or skip

Score higher when the role has:

- production AI, GenAI, or agent deployment
- direct user, customer, or stakeholder interaction
- workflow automation or enterprise integration
- ambiguous problem definition
- startup or scaleup context
- broad ownership and high agency
- AI developer productivity, internal tooling, deployment, or applied AI shape
- plausible compensation/title upside for the candidate

Score lower when the role is:

- mostly generic backend/data engineering
- pure RPA or operations automation without engineering leverage
- too corporate/process-heavy
- too senior to be actionable but useful as a benchmark
- poorly located or incompatible with the candidate's constraints

## Output

Return:

- sources searched
- roles found
- deduplication actions
- rows created or updated
- top roles by score
- blockers or pages requiring browser follow-up
