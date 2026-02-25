---
name: jira-agile-assistant
description: Automates Jira operations (Cloud/On-prem). Creates issues, updates sprints, and synchronizes the backlog with the technical roadmap.
status: implemented
arguments:
  - name: action
    short: a
    type: string
    description: Action
  - name: input
    short: i
    type: string
    description: Input JSON file
  - name: project
    short: p
    type: string
    description: Jira project key
  - name: dry-run
    type: boolean
    description: Simulate without API calls
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Jira Agile Assistant

This skill integrates your project management with your engineering ecosystem.

## Capabilities

### 1. Issue Lifecycle Management

- **Create**: Automatically drafts Jira issues from `requirements-wizard` outputs.
- **Update**: Syncs ticket status when a PR is merged via `gh pr merge`.

### 2. Backlog Grooming

- Analyzes technical debt (via `strategic-roadmap-planner`) and creates prioritized Jira tasks.

## Usage

- "Create a new Jira task for the 'User Auth Fix' and link it to our current sprint."
- "Sync all completed PRs since yesterday with their corresponding Jira tickets."

## Knowledge Protocol

- Adheres to `knowledge/tech-stack/atlassian/jira_best_practices.md`.
