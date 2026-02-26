---
name: backlog-connector
description: Specialized connector for Nulab Backlog API. Automatically resolves Project IDs and handles pagination for fetching issues and wikis.
status: implemented
arguments:
  - name: project
    short: p
    type: string
    required: true
    description: Project Key (e.g., NBS_INCIDENT)
  - name: action
    short: a
    type: string
    default: fetch-issues
    choices:
      - fetch-issues
      - get-project-info
      - list-users
  - name: count
    type: number
    default: 100
  - name: out
    short: o
    type: string
category: Integration & API
last_updated: '2026-02-13'
tags:
  - gemini-skill
  - integration
---

# Backlog Connector

This skill automates interactions with the Backlog API using credentials stored in the Personal/Confidential tiers.

## Usage

- "Use `backlog-connector` to fetch all issues from NBS_INCIDENT."
- "Get the user list from the project."

## Knowledge Protocol

- Reads `knowledge/personal/connections/backlog.md` for API Key.
- Reads `knowledge/confidential/connections/inventory.json` for Project ID mapping.
