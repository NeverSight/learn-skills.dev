---
name: redmine-issues
description: This skill is used when users mention "create issue", "register bug", "create task", "issue list", "my tasks", "assigned issues", "update issue", "change issue status", "search issues", "ticket", "issue", "bug report", etc. Provides Redmine issue management functionality.
version: 1.0.0
---

# Redmine Issue Management Skill

Manages issues through integration with the Redmine issue tracking system.

## Overview

This skill automatically activates Redmine issue management features. When users request issue-related operations, it uses the appropriate Redmine tools.

## Trigger Conditions

Activates for the following requests:

### Issue Creation
- "create issue", "register bug", "create task"
- "new ticket", "feature request"
- "create issue", "create bug", "new ticket"

### Issue Query
- "show my issues", "assigned issues list"
- "open issues", "in-progress tasks"
- "search issues", "find bugs"
- "list my issues", "show open tickets"

### Issue Update
- "change issue status", "update issue"
- "complete issue", "close issue"
- "change assignee", "change priority"
- "update issue", "close ticket"

## Tools Used

### redmine_list_issues
Queries the issue list.

**Key Parameters:**
- `project_id`: Project ID or identifier
- `assigned_to_id`: "me" or user ID
- `status_id`: "open", "closed", "*" or status ID
- `tracker_id`: Tracker ID (Bug, Feature, Task, etc.)
- `limit`: Maximum results (default 25)

**Examples:**
```
"show my issues" → assigned_to_id: "me", status_id: "open"
"completed issues" → status_id: "closed"
"all bugs" → tracker_id: 1 (Bug)
```

### redmine_get_issue
Queries detailed information for a specific issue.

**Key Parameters:**
- `id`: Issue ID (required)
- `include`: Additional information (journals, attachments, relations, etc.)

### redmine_create_issue
Creates a new issue.

**Key Parameters:**
- `project_id`: Project ID (required)
- `subject`: Issue title (required)
- `description`: Issue description
- `tracker_id`: Tracker ID
- `priority_id`: Priority ID
- `assigned_to_id`: Assignee ID

### redmine_update_issue
Updates an existing issue.

**Key Parameters:**
- `id`: Issue ID (required)
- `status_id`: Status ID
- `done_ratio`: Completion percentage (0-100)
- `notes`: Add comments

## Workflow Guide

### When Creating Issues
1. If project ID is missing, first use `redmine_list_projects` to confirm
2. If tracker/priority IDs are needed, use `redmine_list_trackers`, `redmine_list_priorities`
3. Create issue with `redmine_create_issue`

### When Searching Issues
1. Set filter parameters matching conditions
2. Query list with `redmine_list_issues`
3. If needed, confirm details with `redmine_get_issue`

### When Updating Issues
1. Confirm issue ID (find from list or ask user)
2. Confirm fields and values to change
3. Update with `redmine_update_issue`
