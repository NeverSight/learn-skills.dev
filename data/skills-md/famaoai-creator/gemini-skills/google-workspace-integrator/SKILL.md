---
name: google-workspace-integrator
description: Automates Google Docs, Sheets, and Mail. Generates reports, tracks KPIs in spreadsheets, and drafts professional emails for stakeholders.
status: implemented
arguments:
  - name: action
    short: a
    type: string
    description: Action to perform
  - name: input
    short: i
    type: string
    description: Input data file (JSON)
  - name: to
    short: t
    type: string
    description: Email recipient
  - name: dry-run
    type: boolean
    description: Simulate without API calls
  - name: out
    short: o
    type: string
    description: Output file path
category: Integration & API
last_updated: '2026-02-13'
tags:
  - automation
  - cloud
  - documentation
  - gemini-skill
---

# Google Workspace Integrator

This skill connects the monorepo to your primary productivity tools.

## Capabilities

### 1. Document & Sheet Automation

- **Sheets**: Automatically updates financial KPIs from `budget-variance-tracker`.
- **Docs**: Converts Markdown deliverables into shared Google Docs for collaborative review.

### 2. Strategic Email Drafting

- Drafts polished emails for clients or partners based on `stakeholder-communicator` strategy.

## Usage

- "Export the latest P&L forecast to our Google Sheet 'Financial_Overview'."
- "Draft an email to the client summarizing the project completion and share the link to the delivery doc."

## Knowledge Protocol

- Adheres to `knowledge/tech-stack/google/workspace_best_practices.md`.
