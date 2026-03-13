---
name: Meeting Weekly Review
description: |
  Aggregate weekly meeting performance review with stats, trends, alerts, and highlights.
  Use when a user asks "how did my meetings go this week", "weekly meeting recap",
  "meeting stats", "meeting performance this week", "weekly meeting review", or wants
  a summary of all meetings over a time period. Aggregates across multiple meetings --
  unlike meeting-digest-truth-extractor which handles a single meeting. Uses dashboard
  metrics, trends, alerts, sentiment trends, talk time, and conversion signals.
  Do NOT use for single-meeting summaries or coaching feedback on individual calls.
metadata:
  author: sixty-ai
  version: "2"
  category: sales-ai
  skill_type: atomic
  is_active: true
  context_profile: sales
  agent_affinity:
    - meetings
    - pipeline
  triggers:
    - pattern: "how did my meetings go this week"
      intent: "weekly_meeting_review"
      confidence: 0.90
      examples:
        - "how were my meetings this week"
        - "recap my meetings for the week"
        - "how did my calls go"
    - pattern: "weekly meeting review"
      intent: "weekly_review"
      confidence: 0.88
      examples:
        - "weekly meeting recap"
        - "meeting review for the week"
        - "this week's meetings"
    - pattern: "meeting stats"
      intent: "meeting_statistics"
      confidence: 0.82
      examples:
        - "meeting statistics"
        - "how many meetings did I have"
        - "meeting numbers this week"
    - pattern: "meeting performance this week"
      intent: "weekly_performance"
      confidence: 0.85
      examples:
        - "my meeting performance"
        - "meeting performance summary"
        - "how am I doing with meetings"
  keywords:
    - "weekly"
    - "review"
    - "recap"
    - "stats"
    - "performance"
    - "meetings"
    - "this week"
    - "how did"
    - "summary"
    - "trends"
  required_context:
    - user_id
  inputs:
    - name: period
      type: string
      description: "Time period to review: 'this_week', 'last_week', 'this_month', 'last_month'. Defaults to 'this_week'."
      required: false
      default: "this_week"
    - name: include_trends
      type: boolean
      description: "Whether to include week-over-week trend comparisons"
      required: false
      default: true
    - name: include_alerts
      type: boolean
      description: "Whether to include alerts and concerns from meeting analytics"
      required: false
      default: true
  outputs:
    - name: weekly_stats
      type: object
      description: "Aggregate statistics: meeting count, total hours, avg sentiment, avg performance score"
    - name: top_performer
      type: object
      description: "Highest-scoring meeting with key highlights"
    - name: deals_progressed
      type: array
      description: "Deals that advanced during the review period based on meeting outcomes"
    - name: alerts
      type: array
      description: "Alerts and concerns flagged by meeting analytics"
    - name: trends
      type: object
      description: "Week-over-week trend data for key metrics"
    - name: outstanding_actions
      type: array
      description: "Action items from the period that remain open"
    - name: recommendations
      type: array
      description: "Suggested focus areas for the coming week"
  requires_capabilities:
    - calendar
    - crm
  priority: high
  tags:
    - sales-ai
    - meetings
    - analytics
    - weekly-review
    - aggregate
---

## Available Context & Tools
@_platform-references/org-variables.md
@_platform-references/capabilities.md

# Meeting Weekly Review

## Why Weekly Meeting Reviews Matter

Most sales reps finish the week with no idea how their meetings actually went. They remember the one that went well and the one that was painful -- everything else is a blur.

- **Reps who review their week systematically outperform peers by 23%** (Gong analysis of top-quartile performers). Patterns only emerge when you look across meetings, not one at a time.
- **Without structured review, reps repeat the same mistakes** across calls without realizing it. A single coaching session on one call misses systemic issues.
- **Pipeline velocity is driven by meeting quality, not meeting quantity.** Knowing you had 12 meetings is meaningless without understanding which ones moved deals forward.

This skill exists to answer the question every rep and manager should ask on Friday: "How did my meetings actually go this week, and what should I focus on next week?"

## Data Gathering (via execute_action)

Gather data from multiple sources to build a complete weekly picture:

1. **Fetch meetings for the period**: `execute_action("get_meetings_for_period", { period: "this_week", includeContext: true })` -- all meetings with CRM context
2. **Fetch meeting count**: `execute_action("get_meeting_count", { period: "this_week" })` -- total meeting count
3. **Fetch time breakdown**: `execute_action("get_time_breakdown", { period: "this_week" })` -- hours by meeting type
4. **Fetch booking stats**: `execute_action("get_booking_stats", { period: "this_week" })` -- booking trends and sources
5. **Fetch pipeline deals**: `execute_action("get_pipeline_deals", { filter: "closing_soon" })` -- deals with upcoming close dates to correlate with meetings
6. **Fetch tasks**: `execute_action("list_tasks", { status: "open" })` -- outstanding tasks from meeting commitments

Additionally, use the meeting analytics endpoints for deeper metrics:
- **Dashboard metrics** (`/api/dashboard/metrics`): aggregate performance scores, sentiment, conversion signals
- **Dashboard trends** (`/api/dashboard/trends`): week-over-week comparison data
- **Dashboard alerts** (`/api/dashboard/alerts`): flagged concerns and anomalies
- **Dashboard top performers** (`/api/dashboard/top-performers`): highest-scoring meetings
- **Sentiment trends** (`/api/analytics/sentiment-trends`): sentiment trajectory across meetings
- **Talk time** (`/api/analytics/talk-time`): talk-to-listen ratios per meeting
- **Conversion signals** (`/api/analytics/conversion`): buying signals detected across meetings

## Weekly Review Framework

### Section 1: Weekly Snapshot

Provide a quick-scan summary covering:

- **Meeting count**: Total meetings held vs. scheduled (cancellation/no-show rate)
- **Total hours**: Time spent in meetings
- **Time breakdown**: Hours by category (discovery, demo, negotiation, internal, etc.)
- **Average sentiment**: Across all meetings with external attendees
- **Average performance score**: From meeting analytics dashboard metrics

Present as a compact stat block. Example format:
```
This Week: 14 meetings | 11.5 hours | Avg Sentiment: 7.2/10 | Avg Performance: 78/100
vs Last Week: 12 meetings | 9.8 hours | Avg Sentiment: 6.8/10 | Avg Performance: 74/100
```

### Section 2: Highlights

Identify the top 2-3 meetings that stood out positively:
- Highest performance score
- Strongest buying signals detected
- Most positive sentiment shift
- Deal stage advancement during or after the meeting

For each highlight, include:
- Meeting title, date, and attendees
- Why it stood out (specific metric or signal)
- Deal impact (if applicable)

### Section 3: Concerns & Alerts

Surface meetings or patterns that need attention:
- Meetings with negative sentiment or declining sentiment trajectory
- Deals where meetings happened but no stage advancement occurred
- High talk-to-listen ratio meetings (rep dominated the conversation)
- Meetings where key commitments were made but no follow-up tasks exist
- Stale deals that had meetings but show no momentum
- Any alerts from the meeting analytics dashboard

For each concern:
- What happened (specific evidence)
- Why it matters (impact on deal/pipeline)
- Suggested action

### Section 4: Deal Impact

Connect meetings to pipeline movement:
- Which deals had meetings this week?
- Which deals advanced stage? (Correlate meeting dates with stage change dates)
- Which deals are stuck despite having meetings?
- Total pipeline value touched by this week's meetings

### Section 5: Week-over-Week Trends

Compare the current period to the previous period:
- Meeting volume trend (up/down/stable)
- Sentiment trend (improving/declining/stable)
- Performance score trend
- Talk ratio trend (are you listening more or less?)
- Conversion signal frequency (more/fewer buying signals detected)

Flag any significant changes (>10% movement in either direction).

### Section 6: Outstanding Action Items

Aggregate open action items from all meetings in the period:
- Items committed to during meetings that don't yet have corresponding tasks
- Open tasks that originated from meetings in this period
- Overdue items from previous weeks' meetings

### Section 7: Recommendations

Based on the data, suggest 3-5 specific focus areas for the coming week:
- Follow-up actions on high-potential meetings
- Rescue plans for concerning meetings
- Skill improvement areas (based on patterns like consistently high talk ratio)
- Meetings to schedule (deals that need attention but have no upcoming meetings)

## Period Handling

- **this_week**: Monday through current day (or Sunday if end of week)
- **last_week**: Previous full week (Monday-Sunday)
- **this_month**: First of month through current day
- **last_month**: Previous full month

When the user says "this week" but it's Monday, adjust: "It's early in the week -- I'll review last week's meetings and show what's scheduled for this week."

## Output Contract

Return a SkillResult with:

- `data.weekly_stats`: Object with `meeting_count`, `total_hours`, `avg_sentiment`, `avg_performance_score`, `cancellation_rate`, `time_breakdown` (hours by category)
- `data.highlights`: Array of top meeting objects with `title`, `date`, `attendees`, `score`, `reason`, `deal_impact`
- `data.concerns`: Array of concern objects with `meeting_title`, `issue`, `evidence`, `impact`, `suggested_action`
- `data.deal_impact`: Object with `deals_touched`, `deals_advanced`, `deals_stuck`, `total_pipeline_value_touched`
- `data.trends`: Object with metric comparisons: `meeting_volume`, `sentiment`, `performance`, `talk_ratio`, `conversion_signals` -- each with `current`, `previous`, `change_pct`, `direction`
- `data.outstanding_actions`: Array of action items with `description`, `source_meeting`, `owner`, `due_date`, `status`, `days_overdue`
- `data.recommendations`: Array of recommendation objects with `action`, `reason`, `priority`, `related_deal`
- `references`: Links to individual meeting records, deals mentioned

## Quality Checklist

Before returning the review, verify:

- [ ] **All meetings in the period are accounted for.** Cross-check meeting count from `get_meeting_count` against the list from `get_meetings_for_period`.
- [ ] **Stats are computed from actual data, not estimated.** Every number has a source.
- [ ] **Trends compare apples to apples.** Same period length, same metrics. Don't compare a 3-day partial week to a full previous week without noting the difference.
- [ ] **Concerns are evidence-based.** Every flagged concern cites a specific meeting, metric, or signal.
- [ ] **Recommendations are actionable.** "Improve discovery skills" is not actionable. "In 3 of 5 discovery calls, talk ratio exceeded 60% -- practice asking more open-ended questions" is actionable.
- [ ] **Deal correlations are verified.** Don't assume a stage change was caused by a meeting without checking timing.
- [ ] **Outstanding actions are deduplicated.** The same action item should not appear twice from different sources.

## Error Handling

### No meetings in the period
Return a minimal review: "No meetings found for [period]. Consider scheduling discovery calls or follow-ups with active deals."

### Meeting analytics endpoints unavailable
Fall back to CRM-only data. Generate stats from `get_meetings_for_period` and `get_booking_stats`. Note: "Meeting analytics data is unavailable. This review is based on calendar and CRM data only. Sentiment, performance scores, and conversion signals are not included."

### Partial data (some meetings lack transcripts)
Generate the review with available data. Note which meetings lacked transcript analytics and flag them: "[N] of [total] meetings did not have transcript analytics. Review is based on [total - N] meetings with full data."

### No previous period for comparison
Skip the trends section. Note: "No data available for the previous period. Week-over-week trends will be available in future reviews."

## Guidelines

- Keep the review scannable. Use bullet points, stat blocks, and short sentences. A manager should be able to read this in 2 minutes.
- Prioritize insights over data. Don't just list meetings -- tell the user what matters and why.
- Be honest about bad weeks. If meetings went poorly, say so with evidence and constructive suggestions.
- Connect meetings to business outcomes. Every stat should tie back to pipeline or deal impact where possible.
- Use ${company_name} context to identify which meetings involved key deals or target accounts.
- When comparing periods, always note if the comparison is uneven (e.g., partial week vs. full week, holiday-shortened week).
