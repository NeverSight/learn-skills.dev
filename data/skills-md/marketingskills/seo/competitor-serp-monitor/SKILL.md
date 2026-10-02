---
name: competitor-serp-monitor
description: Track competitors new pages, ranking shifts, SERP feature changes, and content strategies. Use when Codex needs to monitor competitor movements in organic search.
---

# Competitor SERP Monitor

## Overview

Monitor a set of competitor domains for changes in their organic search presence: new pages appearing in top positions, ranking shifts, SERP feature acquisition or loss, and content strategy changes.

## Inputs

- List of competitor domains to monitor
- Optional: shared keyword list or topic cluster
- Check frequency (default: weekly)

## Workflow

1. Define the competitor set and shared keywords or topics.
2. For each keyword, fetch the current SERP and record:
   - Which competitor domains appear and at what rank
   - SERP features (featured snippets, PAAs, video, images)
   - New URLs from competitors (not seen in previous check)
3. Compare against the prior SERP snapshot.
4. Flag changes: new competitor entries, rank improvements, SERP feature gains.
5. Analyze new competitor content for angle, format, depth, and entities covered.
6. Surface threats (competitor gaining on your positions) and opportunities (competitor losing ground).

## Output

Competitor movement report with new pages, rank changes, SERP feature shifts, and content analysis.
