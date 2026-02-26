---
name: slack-communicator-pro
description: Manages high-fidelity notifications and team engagement on Slack. Sends automated summaries, alerts, and strategic announcements.
status: implemented
arguments:
  - name: action
    short: a
    type: string
    description: Action
  - name: channel
    short: c
    type: string
    description: Slack channel
  - name: input
    short: i
    type: string
    description: Input message or JSON file
  - name: dry-run
    type: boolean
    description: Simulate without sending
  - name: out
    short: o
    type: string
    description: Output file path
category: Integration & API
last_updated: '2026-02-13'
tags:
  - communication
  - gemini-skill
---

# Slack Communicator Pro

This skill gives the agent a professional and empathetic voice in your team's chat.

## Capabilities

### 1. Intelligent Notifications

- Sends "Daily Standup" summaries of AI activities.
- Delivers critical alerts from `crisis-manager` with immediate action items.

### 2. Interactive Polls & Feedback

- Orchestrates human feedback loops by sending "Option A vs B" polls to Slack channels.

## Usage

- "Notify the #engineering channel that the security scan passed with zero vulnerabilities."
- "Send a summary of this week's technical achievements to the #stakeholders channel."

## Knowledge Protocol

- Follows the `empathy-engine` guidelines for tone and timing.
