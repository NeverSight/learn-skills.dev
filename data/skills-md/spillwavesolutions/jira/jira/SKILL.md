---
name: jira
description: Manages JIRA issues, projects, and workflows using Atlassian MCP. Use when asked to "create JIRA ticket", "search JIRA", "update JIRA issue", "transition issue", "sprint planning", or "epic management".
---

# JIRA Management Skill

A comprehensive Claude Code skill for managing JIRA issues, projects, and workflows using the Atlassian MCP server.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Skill Workflow](#skill-workflow)
  - [Issue Creation](#1-issue-creation-workflow)
  - [Issue Search and Management](#2-issue-search-and-management)
  - [Workflow and Transitions](#3-workflow-and-transitions)
  - [Agile/Scrum Operations](#4-agilescrum-operations)
  - [Linking and Relationships](#5-linking-and-relationships)
  - [Comments and Collaboration](#6-comments-and-collaboration)
  - [Batch Operations](#7-batch-operations)
  - [Project and Version Management](#8-project-and-version-management)
- [Best Practices](#best-practices)
- [Common Use Cases](#common-use-cases)
- [References](#references)
- [Troubleshooting](#troubleshooting)

## Overview

This skill provides intelligent JIRA management capabilities including:
- Creating and managing issues with proper field validation
- Searching and filtering issues using JQL
- Managing workflows and transitions
- Working with epics, sprints, and agile boards
- Adding comments, attachments, and links
- Batch operations for efficiency
- Project and version management

## Prerequisites

### Required MCP Server
- **Atlassian MCP** (`mcp__atlassian`) must be configured in Claude Code
- JIRA credentials (API token or OAuth) must be set up
- Appropriate JIRA permissions for the operations you need

### Environment Configuration
The Atlassian MCP may use environment variables:
- `JIRA_URL`: Your JIRA instance URL
- `JIRA_API_TOKEN`: API token for authentication
- `JIRA_EMAIL`: Email associated with API token
- `JIRA_PROJECTS_FILTER`: (Optional) Comma-separated project keys to filter

## Skill Workflow

### 1. Issue Creation Workflow

When creating JIRA issues, follow this sequence:

#### Step 1: Gather Requirements
Ask the user for:
- **Project key** (e.g., "PROJ", "DEV", "SUPPORT") - NEVER ASSUME
- **Issue type** (Task, Bug, Story, Epic, Subtask)
- **Summary** (title/description)
- **Priority** (if applicable)
- **Assignee** (optional - email, display name, or account ID)
- **Additional fields** (components, labels, custom fields)

#### Step 2: Validate Project
Use `mcp__atlassian__jira_get_all_projects` to:
- Verify project exists
- Get available projects if user unsure
- Confirm project key matches exactly

#### Step 3: Search Available Fields (if needed)
Use `mcp__atlassian__jira_search_fields` to find custom field names and IDs. See [Custom Field Discovery](references/custom_field_discovery.md) for detailed methodology.

#### Step 4: Create Issue
Use `mcp__atlassian__jira_create_issue` with:
```json
{
  "project_key": "PROJ",
  "summary": "Implement user authentication",
  "issue_type": "Task",
  "description": "Detailed description in Markdown format",
  "assignee": "user@example.com",
  "components": "Frontend,API",
  "additional_fields": {
    "priority": {"name": "High"},
    "labels": ["security", "authentication"],
    "parent": "PROJ-123"
  }
}
```

#### Step 5: Follow-up Actions (if needed)
- Link to epic: `mcp__atlassian__jira_link_to_epic`
- Add attachments: Include in update or create
- Add comments: `mcp__atlassian__jira_add_comment`
- Create issue links: `mcp__atlassian__jira_create_issue_link`

### 2. Issue Search and Management

#### Searching Issues
Use `mcp__atlassian__jira_search` with JQL. For comprehensive JQL documentation, see [JQL Guide](references/jql_guide.md).

**Essential JQL Patterns:**
```jql
# Open issues in project
project = PROJ AND status = Open

# Your assigned issues
assignee = currentUser() AND status != Done

# Issues in current sprint
sprint IN openSprints()

# Recently updated
updated >= -7d AND project = PROJ
```

Parameters:
- `jql`: JQL query string
- `fields`: "summary,status,assignee,priority" or "*all"
- `limit`: Max results (1-50, default 10)
- `start_at`: Pagination offset

#### Getting Issue Details
Use `mcp__atlassian__jira_get_issue`:
- `issue_key`: "PROJ-123"
- `fields`: Comma-separated or "*all"
- `expand`: "renderedFields", "transitions", "changelog"
- `comment_limit`: Number of comments to include

#### Updating Issues
Use `mcp__atlassian__jira_update_issue`:
```json
{
  "issue_key": "PROJ-123",
  "fields": {
    "summary": "Updated summary",
    "assignee": "user@example.com",
    "priority": {"name": "Critical"}
  },
  "additional_fields": {
    "labels": ["urgent", "hotfix"]
  },
  "attachments": "/path/to/file1.txt,/path/to/file2.pdf"
}
```

### 3. Workflow and Transitions

#### Get Available Transitions
Use `mcp__atlassian__jira_get_transitions`:
- Returns list of valid transitions for current issue state
- Each transition has an ID and name

#### Transition Issue
Use `mcp__atlassian__jira_transition_issue`:
```json
{
  "issue_key": "PROJ-123",
  "transition_id": "31",
  "fields": {
    "resolution": {"name": "Fixed"}
  },
  "comment": "Moving to Done after completing implementation"
}
```

### 4. Agile/Scrum Operations

#### Working with Boards
1. **Get boards**: `mcp__atlassian__jira_get_agile_boards`
   - Filter by: `board_name`, `project_key`, `board_type` (scrum/kanban)

2. **Get board issues**: `mcp__atlassian__jira_get_board_issues`
   - Requires `board_id` and `jql` filter

#### Working with Sprints
1. **Get sprints**: `mcp__atlassian__jira_get_sprints_from_board`
   - Filter by state: "active", "future", "closed"

2. **Get sprint issues**: `mcp__atlassian__jira_get_sprint_issues`
   - Returns all issues in specified sprint

3. **Create sprint**: `mcp__atlassian__jira_create_sprint`
```json
{
  "board_id": "1000",
  "sprint_name": "Sprint 15",
  "start_date": "2025-01-21T09:00:00.000+0000",
  "end_date": "2025-02-04T17:00:00.000+0000",
  "goal": "Complete authentication feature"
}
```

4. **Update sprint**: `mcp__atlassian__jira_update_sprint`

#### Working with Epics
1. **Find epics**: Use JQL: `issuetype = Epic AND project = PROJ`
2. **Link to epic**: `mcp__atlassian__jira_link_to_epic`
3. **Find issues in epic**: Use JQL: `parent = EPIC-KEY`

### 5. Linking and Relationships

#### Issue Links
Use `mcp__atlassian__jira_create_issue_link`:
```json
{
  "link_type": "Blocks",
  "inward_issue_key": "PROJ-123",
  "outward_issue_key": "PROJ-456",
  "comment": "This issue blocks the other"
}
```

Get link types: `mcp__atlassian__jira_get_link_types`

#### Remote Links (Web/Confluence)
Use `mcp__atlassian__jira_create_remote_issue_link`:
```json
{
  "issue_key": "PROJ-123",
  "url": "https://confluence.example.com/pages/123456",
  "title": "Technical Design Doc",
  "summary": "Detailed architecture documentation",
  "relationship": "documentation"
}
```

### 6. Comments and Collaboration

#### Add Comment
Use `mcp__atlassian__jira_add_comment`:
- Supports Markdown format
- Visible in issue activity

#### Get Comments
Use `mcp__atlassian__jira_get_issue` with appropriate fields

### 7. Batch Operations

#### Batch Create Issues
Use `mcp__atlassian__jira_batch_create_issues`:
```json
{
  "issues": "[{\"project_key\":\"PROJ\",\"summary\":\"Task 1\",\"issue_type\":\"Task\"},{\"project_key\":\"PROJ\",\"summary\":\"Task 2\",\"issue_type\":\"Bug\"}]",
  "validate_only": false
}
```

#### Batch Get Changelogs
Use `mcp__atlassian__jira_batch_get_changelogs`:
- Get history for multiple issues
- Filter by specific fields
- Cloud only feature

### 8. Project and Version Management

#### List Projects
Use `mcp__atlassian__jira_get_all_projects`:
- Returns accessible projects
- Respects JIRA_PROJECTS_FILTER if configured

#### Get Project Issues
Use `mcp__atlassian__jira_get_project_issues`:
- Returns all issues for specific project
- Supports pagination

#### Version Management
1. **Get versions**: `mcp__atlassian__jira_get_project_versions`
2. **Create version**: `mcp__atlassian__jira_create_version`
3. **Batch create**: `mcp__atlassian__jira_batch_create_versions`

## Best Practices

### 1. Always Validate Input
- Never assume project keys - always verify
- Use `jira_search_fields` to find custom field IDs
- Check available transitions before transitioning

### 2. Use Appropriate Field Selection
- Request only needed fields to reduce token usage
- Use `"*all"` sparingly, only when necessary
- Specify fields explicitly for better performance

### 3. JQL Query Construction
See [JQL Guide](references/jql_guide.md) for comprehensive documentation.

### 4. Error Handling
- Check for required fields before creating issues
- Validate transition IDs before executing
- Handle permission errors gracefully

### 5. Efficiency
- Use batch operations for multiple issues
- Paginate large result sets
- Use JQL filters to reduce result size

## Common Use Cases

### Create Story with Subtasks
```
1. Create Epic (if needed)
2. Create Story and link to Epic
3. Create multiple Subtasks with parent = Story key
4. Optionally add to sprint
```

### Bug Triage Workflow
```
1. Search for bugs: issuetype = Bug AND status = Open
2. For each bug: Update priority, assign, add to sprint, transition
```

### Sprint Planning
```
1. Get active sprint
2. Search backlog issues
3. Move selected issues to sprint
4. Update estimates and assign
```

### Release Management
```
1. Create version for release
2. Search issues: fixVersion = "1.0.0"
3. Verify all are Done
4. Create release notes
```

## References

See `references/` directory for detailed documentation:
- [jql_guide.md](references/jql_guide.md) - Comprehensive JQL query guide
- [custom_field_discovery.md](references/custom_field_discovery.md) - Custom field discovery methodology

See `templates/` directory for:
- [issue_creation.json](templates/issue_creation.json) - Standard issue creation templates

## Troubleshooting

### Common Issues

**Issue: "Project not found"**
- Verify project key is correct (case-sensitive)
- Use `jira_get_all_projects` to list available projects
- Check JIRA_PROJECTS_FILTER environment variable

**Issue: "Field required but not provided"**
- Use `jira_search_fields` to find required fields
- Check project configuration for mandatory fields
- Some fields may be required by workflow

**Issue: "Invalid transition"**
- Use `jira_get_transitions` to see available transitions
- Check current issue status
- Verify permissions for transition

**Issue: "Custom field not found"**
- See [Custom Field Discovery](references/custom_field_discovery.md) for discovery methodology
- Format: `customfield_10010`
- Check if field applies to issue type

## Skill Invocation

This skill is automatically invoked when users:
- Ask to "create a JIRA ticket/issue"
- Request "search JIRA for..."
- Say "update JIRA issue..."
- Request "move issue to..." or "transition..."
- Ask about "sprint", "epic", or "board" operations
- Request batch operations on JIRA issues

## Notes

- The Atlassian MCP (`mcp__atlassian`) prefix is used for all tools
- All date/time values use ISO 8601 format
- JQL syntax is similar to SQL but has specific JIRA operators
- Cloud vs Server/Data Center may have feature differences
