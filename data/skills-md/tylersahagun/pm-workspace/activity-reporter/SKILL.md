---
name: activity-reporter
description: Generate time-bounded activity reports (end-of-day, end-of-week, digest) that aggregate work across GitHub, Linear, and PM workspace. Use when running /eod, /eow, /digest, or /eod --sam commands.
---

# Activity Reporter Skill

Generate activity reports that focus on **what happened** during a specific period and **what should happen next**.

## Report Modes

| Mode              | Command         | Length     | Style               | Audience            |
| ----------------- | --------------- | ---------- | ------------------- | ------------------- |
| **Full EOD**      | `/eod`          | ~200 lines | Technical report    | PM/Engineering      |
| **Full EOW**      | `/eow`          | ~300 lines | Technical + trends  | PM/Engineering      |
| **Daily Digest**  | `/eod --digest` | ~50 lines  | Newspaper headlines | Anyone              |
| **Weekly Digest** | `/eow --digest` | ~60 lines  | Newspaper headlines | Anyone              |
| **Rob Mode**      | `/eod --rob`    | ~40 lines  | Simple + verified   | Revenue/CRO         |
| **Sam EOD**       | `/eod --sam`    | ~150 lines | Outcome-oriented    | Sam Ho (remote mgr) |
| **Sam EOW**       | `/eow --sam`    | ~250 lines | Outcome + portfolio | Sam Ho (remote mgr) |

See `_references/report-templates.md` for full output templates and examples.
See `_references/sam-report-template.md` for Sam Mode templates and data source details.

### Digest Mode (`--digest`)

Quick "Sunday paper" format for revenue team. Business impact, not technical metrics.

**Core Team:** Matt Noxon, Jason, Eduardo, Palmer, Kaden, Dylan, Bryan, Adam, Skylar

**Sections:** Headline, New Features, Improvements, Bugs Fixed, Team Focus, Revenue Wins, What's Coming Next, Stats

**DO NOT INCLUDE:** PM Workspace Advances, PR counts, GitHub handles (use real names), technical infrastructure.

### Rob Mode (`--rob`)

Named after Robert Henderson (CRO). Simplified, verified report for revenue team.

Key differences from digest: high school reading level, zero technical jargon, features verified against PostHog, internal features hidden, benefit-focused language.

**Lead with EXPERIENCE IMPACT, not feature lists.** For each shipped item, answer:

- What can a customer DO now that they couldn't before?
- How do they discover it?
- What does it feel like to use?

**Format:** "[Customer persona] can now [experience], which means [business outcome]."
**NOT:** "We shipped [feature name] with [technical details]."

**Sections:** What's New (experience language), What We Fixed, Revenue Wins, Coming Soon, Quick Stats

**Mandatory:** All features checked against PostHog feature flags. Only include GA features (100% rollout).

**Output:** `status/activity/rob/rob-YYYY-MM-DD.md`

### Sam Mode (`--sam`)

For Sam Ho (VP/GM Product, Tyler's remote manager). Designed around Sam's stated preferences from 1:1s and team conversations.

**Key principles:**

- **Outcomes, not outputs** — Don't list PRs. Show what moved the needle for users/business.
- **Notion Projects DB is source of truth** — Every project references the Projects database (`2c0f79b2c8ac802c8b15c84a8fce3513`).
- **Done / Up Next / Blocked** per project — Sam asked for this exact format.
- **SCQA for decisions** — Situation, Complication, Question, Answer when Sam needs to weigh in.
- **Data, not handwaving** — Include numbers, metrics, customer feedback quotes.
- **Full Slack visibility** — Sam is remote. Surface all signal from ALL channels including DMs.
- **Meeting log** — Pulled from AskElephant internal search. Sam can't walk by and see who Tyler met with.
- **Email highlights** — External communications, customer threads.
- **Sprint progress** — Sam wants concrete deliverables every 2 weeks.
- **Growth section (EOW only)** — What Tyler learned, PM skill development.

**Data Sources (more comprehensive than other modes):**

| Source                    | What to Pull                                            | Tool/Method                                                      |
| ------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------- |
| **Notion Projects DB**    | Project phase, status updates, target dates, objectives | `NOTION_QUERY_DATABASE` (ID: `2c0f79b2c8ac802c8b15c84a8fce3513`) |
| **AskElephant meetings**  | Today's/week's meetings with key takeaways              | AskElephant internal search                                      |
| **ALL Slack channels**    | Decisions, signals, team sentiment, DM highlights       | `SLACK_FETCH_CONVERSATION_HISTORY`, `SLACK_SEARCH_MESSAGES`      |
| **Gmail**                 | Key email threads, customer communications              | `GOOGLESUPER_FETCH_EMAILS`                                       |
| **Linear**                | Active cycle, completions, blockers by assignee         | Linear MCP tools                                                 |
| **GitHub (elephant-ai)**  | Merged PRs, what shipped                                | `gh pr list`                                                     |
| **GitHub (pm-workspace)** | Workspace changes, docs updated                         | `git log`                                                        |
| **HubSpot**               | Deals closed/lost, pipeline changes                     | `hubspot-activity` subagent                                      |

**Slack Channel Coverage (Sam Mode is comprehensive):**

Unlike other modes that only check revenue + engineering channels, Sam Mode checks:

- Revenue: #sales-closed-won, #team-sales, #sdr-stats, #expansion-opportunities, #churn-alert
- Product: #product-forum, #product-requests, #product-updates, #product-issues
- Engineering: #team-dev, #team-dev-code-review
- Leadership: #council-product, #council-five
- Cross-functional: #general, #watering-hole
- **Tyler's DMs** with: Sam, Rob, Bryan, Woody, Skylar, Adam, Ben, Tony, Kensi

**Output:** `status/activity/sam/sam-eod-YYYY-MM-DD.md` or `status/activity/sam/sam-eow-YYYY-WXX.md`

**Delivery:** After saving to file, optionally DM Sam on Slack with a condensed version. Sam said: "If you DM me, I may not get to it right away, but I'll focus on those."

**Full template:** See `_references/sam-report-template.md`

## Key Difference from Portfolio Status

| Aspect       | `/status-all`        | `/eod` / `/eow`         |
| ------------ | -------------------- | ----------------------- |
| Focus        | What artifacts exist | What happened (bounded) |
| Time Range   | Current state        | Today / This week       |
| Output       | Artifact gap matrix  | Activity by initiative  |
| Action Items | "Missing X artifact" | "Continue Y, involve Z" |

## Data Sources

### 0. HubSpot - Authoritative Revenue Data (PRIMARY)

Uses `hubspot-activity` subagent. HubSpot is more reliable than Slack for deal data.

**Data Retrieved:** Deals closed (closedwon), Deals lost (closedlost), Meetings booked (SDR sets), ARR metrics.

**Priority:** Primary = HubSpot (authoritative), Supplement = Slack (context/celebrations), Merge when same deal appears in both.

### 1. Slack - Revenue & Engineering Activity

Uses `slack-sync` skill. Supplement to HubSpot for qualitative context.

**Revenue Channels:** #sales-closed-won, #team-sales, #sdr-stats (C0A05H709SM), #expansion-opportunities, #churn-alert, #team-partners, #customer-quotes

**Engineering Channels:** #product-updates, #product-issues, #team-dev-code-review

**Name Resolution:** Use `pm-workspace-docs/company-context/org-chart.md` to map Slack IDs to names.

### 2. GitHub (Engineering Activity)

```bash
# Merged PRs
gh pr list -R askelephant/elephant-ai -s merged --search "merged:>=YYYY-MM-DD" --json number,title,author,mergedAt,headRefName,labels,body

# PM workspace changes
git log --since="YYYY-MM-DD" --name-only --pretty=format:"%h|%s|%an|%ai" -- "pm-workspace-docs/"
```

### 3. Linear (Development Tracking)

Use Linear MCP tools: `linear_getActiveCycle`, `linear_searchIssues`, `linear_getProjectIssues`

### 4. Local Workspace State

```bash
git log --since="YYYY-MM-DD" --name-only -- "pm-workspace-docs/initiatives/active/*/_meta.json"
```

## Initiative Mapping

### Primary: ASK-XXXX Extraction

Extract Linear issue IDs from branch names, PR titles, commit messages. Then resolve: ASK-XXXX -> Linear Issue -> Project -> `_meta.json` -> Initiative.

### Secondary: File Path Heuristics

Map prototype/doc paths to initiatives (e.g., `prototypes/src/components/HubSpotConfig/` -> `hubspot-agent-config-ui`).

## Integration & Product Taxonomy

See `_references/taxonomy.md` for complete product/integration classification. Critical rule: **Dialpad, Aircall, RingCentral are Telephony/Dialers, NOT CRMs.**

## Linear Label Taxonomy

Group work by **type first** (Feature/Improvement/Bug), then by **product area** (Recording & Capture, CRM Integrations, Workflows, Platform).

## Report Generation Procedure

1. **Collect** raw activity from all sources (GitHub, Linear, Slack, HubSpot, local workspace)
2. **Map** each activity item to an initiative (ASK-XXXX -> initiative, file path -> initiative, else "Unlinked")
3. **Load** initiative context (\_meta.json, artifact existence)
4. **Generate** per-initiative summary (What Got Done, What Needs to Continue, Stakeholder Involvement)
5. **Generate** stakeholder narratives based on phase + artifact gaps
6. **Generate** focus recommendations (P0 items, blocked items, phase-ready items)
7. **Save** report and update activity-history.json

## Stakeholder Narrative Templates

| Situation                   | Recommendation                                               |
| --------------------------- | ------------------------------------------------------------ |
| discovery, no research.md   | "Gather user evidence through interviews or signal analysis" |
| define, no design-brief     | "Design should create brief based on PRD"                    |
| define, all docs present    | "Ready for engineering handoff"                              |
| build, stale docs (>7 days) | "Sync documentation with implementation progress"            |
| validate, jury < 70%        | "Design should address jury feedback"                        |
| validate, no GTM            | "Revenue team should prepare GTM brief"                      |
| blocked                     | "Owner should unblock by [action]"                           |

## File Locations

| Report Type | Location                                                      |
| ----------- | ------------------------------------------------------------- |
| End of Day  | `pm-workspace-docs/status/activity/eod/eod-YYYY-MM-DD.md`     |
| End of Week | `pm-workspace-docs/status/activity/eow/eow-YYYY-WXX.md`       |
| Digest      | `pm-workspace-docs/status/activity/digest/digest-*.md`        |
| Rob Mode    | `pm-workspace-docs/status/activity/rob/rob-*.md`              |
| Sam EOD     | `pm-workspace-docs/status/activity/sam/sam-eod-YYYY-MM-DD.md` |
| Sam EOW     | `pm-workspace-docs/status/activity/sam/sam-eow-YYYY-WXX.md`   |

## Execution Checklist

### Standard Modes (EOD, EOW, Digest, Rob)

- [ ] Determine time range (today vs this week)
- [ ] Invoke hubspot-activity subagent for revenue data
- [ ] Fetch Slack activity via slack-sync skill (revenue + engineering channels)
- [ ] Fetch GitHub elephant-ai PRs and pm-workspace git log
- [ ] Query Linear for issue updates
- [ ] Map all activity to initiatives
- [ ] Check feature availability via PostHog (for digest/rob modes)
- [ ] Map Slack user IDs to real names (from org-chart.md)
- [ ] Generate Revenue Team Wins section (merge HubSpot + Slack)
- [ ] Generate stakeholder narratives
- [ ] Compile focus recommendations
- [ ] Save report
- [ ] Run post-generation validation

### Sam Mode Checklist (additional steps)

- [ ] Query Notion Projects DB (`2c0f79b2c8ac802c8b15c84a8fce3513`) for all project statuses
- [ ] Pull Tyler's meetings from AskElephant internal search for the period
- [ ] Fetch ALL Slack channels (not just revenue/engineering — include product, leadership, cross-functional)
- [ ] Fetch Tyler's DM conversations with leadership (Sam, Rob, Bryan, Woody, Skylar, Adam, Ben, Tony, Kensi)
- [ ] Fetch Gmail for key email threads via `GOOGLESUPER_FETCH_EMAILS`
- [ ] Cross-reference Notion project phases with Linear engineering progress
- [ ] Flag any Notion status updates that are stale (>7 days)
- [ ] Format each project using Done/Up Next/Blocked structure
- [ ] Include feedback status for anything in beta (Got feedback / Awaiting / No mechanism)
- [ ] Include objectives and success metrics per project (from Notion)
- [ ] Format any decision points in SCQA structure
- [ ] Add sprint progress table (EOW only)
- [ ] Add portfolio view table (EOW only)
- [ ] Add growth/learning section (EOW only)
- [ ] Save to `status/activity/sam/` directory
- [ ] Optionally DM Sam on Slack with condensed version

## Post-Generation Validation

After generating any report, validate:

1. **Day-of-week** matches actual date (Jan 1, 2026 = Thursday)
2. **Stats counts** match listed items
3. **Team member names** are valid (no GitHub handles)
4. **Week numbers** are correct (ISO weeks)
5. **Dates** are internally consistent
6. **Product categories** are correct (Dialpad is NOT a CRM)
7. **All required sections** are present

## Integration Points

- **slack-sync skill**: Handles all Slack MCP interactions
- **slack-block-kit skill**: Format messages when posting to Slack (Rob Report, Newsletter, Daily Digest templates)
- **hubspot-activity subagent**: Authoritative revenue data
- **org-chart.md**: Slack ID to name mapping
