---
name: tools-backlog
description: Comprehensive GTD task management using Backlog.md CLI
version: 1.0.0
author: claude-code-skill

# Skill metadata
domain: productivity
category: task-management
tags: [gtd, backlog-md, task-management, cli, productivity]

# Skill classification
type: domain-expertise
complexity: intermediate
scope: comprehensive

# Usage information
prerequisites:
  - "Backlog.md CLI installed"
  - "Basic familiarity with command line"
  - "Understanding of software development workflows"

provides:
  - "GTD methodology implementation"
  - "Task management workflows"
  - "Team coordination patterns"
  - "Productivity best practices"

# Integration notes
compatible_tools:
  - backlog-md-cli
  - git
  - text-editors

# Learning objectives
objectives:
  - "Master Backlog.md CLI commands"
  - "Implement GTD methodology effectively"
  - "Organize work with proper task structure"
  - "Coordinate team workflows efficiently"
  - "Apply search and discovery patterns"
---

# Backlog.md GTD Task Management Skill

A practical skill for using the Backlog.md CLI tool to implement GTD (Getting Things Done) methodology effectively in software development environments.

## Quick Start

### 1. Capture Your First Task
```bash
backlog task create "Fix critical login bug" \
  -d "Users cannot log in with Chrome browser" \
  --priority high
```

### 2. Organize with Context
```bash
backlog task edit 1 -l bug,frontend,urgent -a @alice
backlog task edit 1 --ac "Reproduce bug in Chrome" \
  --ac "Identify root cause" \
  --ac "Implement fix" \
  --ac "Add regression tests"
```

### 3. Execute and Track
```bash
backlog task edit 1 -s "In Progress" -a @myself
backlog task edit 1 --check-ac 1 --append-notes "Successfully reproduced the issue"
backlog task edit 1 -s Done --notes "Bug fixed and deployed to production"
```

### 4. Review and Discover
```bash
backlog task list --plain
backlog search "chrome" --plain
backlog task list -a @alice --plain
```

## What This Skill Covers

- **Task Management**: Create, organize, and track tasks using Backlog.md CLI
- **GTD Methodology**: Apply the four GTD phases (Capture, Organize, Execute, Review)
- **Team Collaboration**: Assign work, manage handoffs, and coordinate with teammates
- **Practical Commands**: Real CLI examples you can use immediately

## Core Concepts

### Task Structure
Every task has these key elements:
- **Title**: Brief summary of what needs to be done
- **Description**: Context and purpose (the "why")
- **Acceptance Criteria**: Testable outcomes (the "what")
- **Labels**: Categories and contexts for organization
- **Priority**: High/Medium/Low for triage
- **Status**: To Do → In Progress → Done

### GTD Integration
The four GTD phases map directly to Backlog.md operations:
1. **Capture**: `backlog task create` - Get ideas out of your head
2. **Organize**: `backlog task edit` - Add structure and context
3. **Execute**: Status management and progress tracking
4. **Review**: `backlog search` and regular system maintenance

## Essential CLI Commands

### Task Creation (Capture Phase)

Quick capture of ideas and tasks:

```bash
# Simple task capture
backlog task create "Fix login button hover effect"

# With description and priority
backlog task create "Implement user authentication" \
  -d "Add login/logout functionality with JWT tokens" \
  --priority high

# With acceptance criteria
backlog task create "Optimize dashboard loading" \
  -d "Dashboard takes 8+ seconds to load, need sub-2 second performance" \
  --ac "Identify slow queries" \
  --ac "Implement database optimization" \
  --ac "Add caching layer" \
  --ac "Verify performance improvement"
```

### Task Organization (Organize Phase)

Add structure and context to tasks:

```bash
# Add labels for categorization
backlog task edit 42 -l backend,api,authentication

# Assign to team member
backlog task edit 42 -a @alice

# Set priority
backlog task edit 42 --priority high

# Add detailed description
backlog task edit 42 -d "Users cannot log in when using corporate email accounts due to validation regex"

# Add implementation plan (the "how")
backlog task edit 42 --plan $'1. Research authentication libraries\n2. Implement JWT middleware\n3. Create login endpoint\n4. Add error handling'
```

### Task Execution (Execute Phase)

Manage daily work and track progress:

```bash
# Start working on a task
backlog task edit 42 -s "In Progress" -a @myself

# Mark acceptance criteria as complete
backlog task edit 42 --check-ac 1  # Mark first criterion complete
backlog task edit 42 --check-ac 2 --check-ac 3  # Mark multiple criteria

# Add progress notes
backlog task edit 42 --append-notes "Successfully implemented JWT middleware with refresh token support"

# Complete a task
backlog task edit 42 -s Done \
  --notes "Authentication system fully implemented and tested. Ready for code review."

# View your current work
backlog task list -a @myself --plain
```

### Task Discovery (Review Phase)

Find relevant work and analyze patterns:

```bash
# Search by topic
backlog search "authentication" --plain

# Find high-priority items
backlog search --priority high --plain

# Search your work
backlog search "@myself" --plain

# Find blocked items
backlog search "blocked" --plain

# View all tasks
backlog task list --plain

# View tasks by status
backlog task list -s "In Progress" --plain
```

## Practical Workflows

### Daily GTD Routine

```bash
# Morning: Plan your day
backlog task list -a @myself -s "To Do" --priority high --plain

# During day: Update progress
backlog task edit 42 --check-ac 1 --append-notes "Made progress on user registration"

# Evening: Review and plan tomorrow
backlog task list -a @myself --plain
```

### Weekly Review Process

```bash
# Review all active work
backlog task list -s "In Progress" --plain

# Check for blocked items
backlog search "blocked" --plain

# Review team workload
backlog task list -a @team-member --plain

# Find old drafts to process
backlog task list -s Draft --plain
```

### Project Breakdown

```bash
# Create main project task
backlog task create "Q3 User Portal Redesign" --priority high

# Add subtasks
backlog task create "Design new user interface" -p 1
backlog task create "Implement React components" -p 1
backlog task create "Setup testing framework" -p 1

# Create dependencies
backlog task edit 3 --dep 2  # Testing depends on components
```

### Bug Management

```bash
# Create bug task with template
backlog task create "[BUG] Users can't reset password" \
  -d "Password reset email never arrives for corporate email accounts" \
  --ac "Reproduce the bug consistently" \
  --ac "Identify root cause in email service" \
  --ac "Fix email configuration" \
  --ac "Add regression tests" \
  -l bug,email,urgent --priority high

# Track bug fix progress
backlog task edit 15 -s "In Progress" -a @backend-dev
backlog task edit 15 --check-ac 1 --append-notes "Successfully reproduced with test corporate account"
```

### Feature Development

```bash
# Create feature with standard structure
backlog task create "[FEATURE] User profile image upload" \
  -d "Allow users to upload and crop profile pictures from their device" \
  --ac "Design upload interface" \
  --ac "Implement image upload endpoint" \
  --ac "Add image cropping functionality" \
  --ac "Update user profile display" \
  --ac "Write tests for upload flow" \
  -l feature,frontend,images --priority medium

# Assign and track
backlog task edit 20 -a @frontend-dev
backlog task edit 20 --plan $'1. Create upload component design\n2. Implement drag-and-drop interface\n3. Add image cropping library\n4. Connect to backend API\n5. Add error handling'
```

## Team Collaboration

### Task Assignment and Handoff

```bash
# Assign work with full context
backlog task edit 25 -a @bob \
  --notes $'Backend API work complete. Ready for frontend integration:\n\nEndpoints: POST /api/upload, GET /api/profile/image\nAuthentication: JWT Bearer tokens required\nFile limits: 5MB max, jpg/png only\n\nAvailable for questions 2-4 PM today'

# Clean handoff example
backlog task edit 26 -a @alice \
  -s "To Do" \
  --notes $'Design mockups complete and approved.\n\nFiles in Figma: https://figma.com/design/abc123\nDesign tokens documented in confluence\nMobile-first approach implemented\n\nPlease review and confirm timeline for implementation.'
```

### Code Review Integration

```bash
# Mark ready for review
backlog task edit 30 -s Review --notes "All tests passing. Ready for code review."

# Handle review feedback
backlog task edit 30 -s "In Progress" --append-notes "Review feedback received. Addressing performance concerns."

# Complete after review
backlog task edit 30 -s Done --notes "All review comments addressed. Ready for deployment."
```

## Search and Discovery Patterns

### Finding Relevant Work

```bash
# Find work by technology
backlog search "react" --plain
backlog search "database" --plain

# Find by type of work
backlog search "bug" --plain
backlog search "feature" --plain
backlog search "documentation" --plain

# Find by priority
backlog search --priority high --plain

# Combined searches
backlog search "frontend" --priority high -s "To Do" --plain
```

### Team Insights

```bash
# Check team workload
backlog task list -a @alice --plain
backlog task list -a @bob --plain

# Find who worked on similar problems
backlog search "authentication" -s Done --plain | grep "@"

# Identify expertise areas
backlog search "performance" --plain | grep "@"
```

## Quality and Best Practices

### Good Task Examples

```bash
# Clear, actionable task
backlog task create "Fix authentication timeout issue" \
  -d "Users logged out after 5 minutes regardless of activity" \
  --ac "Implement sliding session expiration" \
  --ac "Add session refresh on user activity" \
  --ac "Test timeout behavior" \
  -l bug,authentication,ux --priority high

# Well-structured feature
backlog task create "Add dark mode toggle" \
  -d "Allow users to switch between light and dark themes" \
  --ac "Create theme switching component" \
  -ac "Implement CSS variable system" \
  --ac "Add user preference persistence" \
  --ac "Test theme transitions" \
  -l feature,ui,accessibility --priority medium
```

### Acceptance Criteria Guidelines

Good acceptance criteria are:
- **Testable**: Can be objectively verified
- **Specific**: Clear what "done" means
- **User-focused**: Describe outcomes, not implementation
- **Complete**: Cover the full scope of work

```bash
# Good: User-focused outcomes
backlog task edit 40 --ac "User can successfully log in with valid credentials"
backlog task edit 40 --ac "Error message displays for invalid credentials"

# Avoid: Implementation details
# bad: "Add validateLogin() function in auth.js"
```

### Label Organization

Use consistent label patterns:

```bash
# By type
backlog task edit 42 -l bug,feature,documentation,testing

# By component
backlog task edit 42 -l frontend,backend,api,database

# By priority
backlog task edit 42 -l urgent,high-priority,medium-priority,low-priority

# By context
backlog task edit 42 -l meeting-required,waiting-for,research-needed
```

## Common Patterns

### Daily Capture Habit

```bash
# Quick capture throughout the day
backlog task create "Idea: Add keyboard shortcuts to navigation"
backlog task create "Follow up with design team about mockups"
backlog task create "Research performance monitoring tools"

# Process captured items daily
backlog task list -s Draft --plain
```

### Weekly Review Template

```bash
# Weekly review checklist
# 1. backlog task list -s Draft --plain (process all drafts)
# 2. backlog task list -s "In Progress" --plain (check progress)
# 3. backlog search "blocked" --plain (resolve blockers)
# 4. backlog task list --priority high --plain (review priorities)
# 5. backlog task list -a @team-member --plain (check workload)
```

### Project Templates

```bash
# Bug template
backlog task create "[BUG] Brief description" \
  -d "Detailed problem description and impact" \
  --ac "Reproduce the issue" \
  --ac "Identify root cause" \
  --ac "Implement fix" \
  --ac "Add tests to prevent regression" \
  -l bug --priority high

# Feature template
backlog task create "[FEATURE] Brief description" \
  -d "User story: As a [user], I want [feature] so that [benefit]" \
  --ac "Define requirements" \
  --ac "Implement core functionality" \
  --ac "Write tests" \
  --ac "Update documentation" \
  -l feature --priority medium
```

## Tips for Success

### Daily Habits
- **Capture immediately**: Don't let ideas slip away
- **Organize daily**: Process drafts into actionable tasks
- **Focus execution**: Work on one task at a time
- **Review regularly**: Keep system current and aligned

### Quality Standards
- **Clear titles**: Make tasks understandable at a glance
- **Specific criteria**: Everyone knows when it's done
- **Consistent labels**: Enable effective search and organization
- **Regular updates**: Keep progress visible to team

### Team Coordination
- **Complete handoffs**: Provide all needed context
- **Clear ownership**: Always have明确的 assignee
- **Status updates**: Keep team informed of progress
- **Shared understanding**: Use consistent terminology

This skill provides the essential knowledge needed to effectively use Backlog.md for implementing GTD methodology in software development environments.