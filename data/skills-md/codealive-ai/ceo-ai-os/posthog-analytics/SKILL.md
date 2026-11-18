---
name: posthog-analytics
description: Raw PostHog data queries via MCP — event catalog, query recipes, dashboards, funnels, experiments. Use for specific data questions. For CEO-level metric interpretation and frameworks, use metrics-briefing instead.
user-invocable: true
---

# PostHog Analytics

Direct access to PostHog data for your projects.

## Projects

| Name | ID | Use |
|------|----|-----|
| app | [YOUR_APP_PROJECT_ID] | Main product analytics (DEFAULT) |
| landing | [YOUR_LANDING_PROJECT_ID] | Landing page analytics |
| documentation | [YOUR_DOCS_PROJECT_ID] | Docs site analytics |

## Tool

Call the native MCP tool `posthog__<tool-name>` directly (server=posthog, tool=<tool-name>). Parameters go in a JSON object — examples below use shorthand key=value.

## Event Catalog

### Journey & Funnel Events
| Event | Description | Key Properties |
|-------|------------|----------------|
| `conversion_funnel` | Funnel stage tracking | funnel (value_realization, onboarding, workspace_collaboration, primary_resource_activation, primary_resource_import) |
| `funnel_next_stage_available` | Stage transition | currentStage, nextStage, nextStageName, funnelId, organizationId |
| `user_journey_milestone` | User milestone reached | milestone, milestoneId, journeyId, timeSincePrevious, organizationId, signup_method |
| `journey_critical_path_progress` | Critical path progress | progress, completedMilestones, journeyId, organizationId |
| `key_milestone_reached` | Query milestone | — |

### Funnel Stages (from funnel_next_stage_available)
```
signup_started → account_created → email_confirmed
→ workspace_created → first_value_moment
→ first_primary_resource_added → primary_resource_connect_started
→ primary_resource_connected → primary_resource_processed
→ first_key_action_executed → first_value_delivered
→ return_usage → regular_usage → power_user
→ team_invitation_sent
```

### Milestone Values (from user_journey_milestone)
Return Visit, Weekly Active, First Resource Connected, Account Created, workspace_activated, First Value Moment, First Workspace Created

### Chat & Search Events
| Event | Key Properties |
|-------|----------------|
| `core_action` | — (core product usage) |
| `session_started` | — |
| `session_resumed` | — |
| `context_sources_changed` | — |
| `context_source_selected` | — |
| `core_query_performed` | query, searchMode, searchType, resultCount, timeToResults, workspaceId, totalRepositories |
| `deep_workflow_started` | — |
| `example_selected` | — |
| `core_action_retry` | — |

### Repository Events
| Event | Key Properties |
|-------|----------------|
| `primary_resource_action` | action, repositoryType, processingStatus, repositoryName, isReindex, autoReindex, isPrivate, organizationId |
| `primary_resource_listing_viewed` | — |
| `primary_resource_ready` | — |

### Workspace Events
| Event | Key Properties |
|-------|----------------|
| `workspace_create_started` | — |
| `workspace_updated` | — |
| `workspace_deleted` / `workspace_delete_initiated` | — |
| `workspace_edit_started` | — |
| `workspace_resources_updated` | — |
| `workspace_refresh_triggered` | — |
| `team_collaboration_event` | — |
| `workspace_usage_patterns` | — |
| `primary_action_started` | — |

### Sharing Events (virality signals)
| Event | Key Properties |
|-------|----------------|
| `output_sharing_enabled` | — |
| `share_link_copied` | — |
| `public_output_viewed` | — |

### Person Properties (B2B-relevant)
| Property | Type | Use |
|----------|------|-----|
| `email_verified` | Boolean | Qualified signup filter |
| `has_primary_integration_connected` | Boolean | Activation signal |
| `has_secondary_integration_connected` | Boolean | Activation signal |
| `$initial_utm_source` | String | First-touch attribution |
| `$initial_utm_medium` | String | First-touch attribution |
| `$initial_utm_campaign` | String | First-touch attribution |
| `$initial_referring_domain` | String | First-touch attribution |
| `$initial_current_url` | String | Landing page attribution |

### Event Properties (cross-event)
| Property | Type | Found On |
|----------|------|----------|
| `organizationId` | String | Most events — B2B account grouping |
| `workspace_id` / `workspaceId` | String | Workspace events, search, journey |
| `workspace_name` / `workspaceName` | String | Workspace events |
| `source` | String | Journey, funnel, search events |
| `isAuthenticated` | Boolean | Most events |
| `timeSincePrevious` | Numeric | Journey milestones |

## Key Tools

### Discovery
```bash
posthog__event-definitions-list
posthog__event-definitions-list q="signup"
posthog__properties-list type=event eventName="conversion_funnel"
posthog__properties-list type=person
posthog__entity-search query="activation"
```

### Natural Language Queries (recommended)
```bash
posthog__query-generate-hogql-from-question question="..."
```

Best for:
- Complex breakdowns by multiple properties
- Account-level (organizationId) aggregations
- Attribution analysis ($initial_* properties)
- Time-between-events calculations

### Saved Insights
```bash
posthog__insights-get-all
posthog__insight-get insightId="123"
posthog__insight-query insightId="123"
```

### Dashboards
```bash
posthog__dashboards-get-all
posthog__dashboard-get dashboardId=[YOUR_DASHBOARD_ID]
```

### Experiments & Feature Flags
```bash
posthog__experiment-get-all
posthog__experiment-results-get experimentId=123 refresh=false
posthog__feature-flag-get-all
posthog__feature-flag-get-definition flagKey="my-flag"
```

### Errors
```bash
posthog__list-errors orderBy=occurrences dateFrom="2026-01-01T00:00:00Z"
posthog__error-details issueId="uuid-here"
```

### Surveys
```bash
posthog__surveys-get-all
posthog__survey-stats survey_id="uuid"
```

## Switching Projects

Default project is "app" ([YOUR_APP_PROJECT_ID]). To query landing or docs:
```bash
posthog__switch-project projectId=[YOUR_LANDING_PROJECT_ID]
# Now all queries target "landing"
# Switch back after:
posthog__switch-project projectId=[YOUR_APP_PROJECT_ID]
```

## Query Recipes

### CEO Morning Briefing
```bash
# DAU yesterday
posthog__query-generate-hogql-from-question question="How many unique users had pageview events yesterday?"

# New signups yesterday
posthog__query-generate-hogql-from-question question="How many user_journey_milestone events with milestone Account Created happened yesterday?"

# Funnel progression yesterday
posthog__query-generate-hogql-from-question question="Show all funnel_next_stage_available events from yesterday, count by currentStage to nextStage transition"
```

### Weekly CEO Dashboard
```bash
# Funnel health
posthog__query-generate-hogql-from-question question="Show funnel_next_stage_available events in the last 7 days, count unique users for each currentStage to nextStage pair"

# Active companies
posthog__query-generate-hogql-from-question question="How many distinct organizationId values had any events in the last 7 days?"

# TTFV
posthog__query-generate-hogql-from-question question="What is the average timeSincePrevious for user_journey_milestone where milestone is First Value Moment, last 30 days?"

# Source attribution
posthog__query-generate-hogql-from-question question="For users who reached first_value_delivered in funnel_next_stage_available last 30 days, what are the top initial UTM sources?"
```

### Product Health
```bash
# Search quality
posthog__query-generate-hogql-from-question question="What is the average resultCount and timeToResults for core_query_performed events this week?"

# Primary resource connection success
posthog__query-generate-hogql-from-question question="How many primary_resource_action events by processingStatus in the last 7 days?"
```

## Output Format

Present results concisely for chat platforms:
- Key number + trend (vs previous period)
- Flag anomalies
- Link to metric class (Primary CEO / Secondary / B2B bridge)
- Always segment by target cohort when possible
