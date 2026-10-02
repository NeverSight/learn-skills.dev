---
name: content-decay-monitor-setup
description: Save monitored pages and topics to schedule recurring decay scans in local agents. Use when Codex needs to set up ongoing content performance monitoring for a set of pages or topics.
---

# Content Decay Monitor Setup

## Overview

Configure a recurring monitor that checks a list of pages or topics for organic performance changes. The monitor runs on a schedule (weekly/monthly) and alerts when performance drops below a threshold.

## Inputs

- List of URLs or topics to monitor
- Monitoring frequency (weekly, biweekly, monthly)
- Alert threshold (e.g., 15% click decline, 20% impression drop)
- Optional: GSC property or GA4 property

## Workflow

1. Define the monitor scope: pages, topics, or both.
2. Set baseline performance from current GSC/GA4 data.
3. Configure the check frequency and alert threshold.
4. Store the monitor configuration in a local file or agent config.
5. On each check cycle: fetch current data, compare to baseline, flag pages below threshold.
6. Route alerts to the user (with traffic-decay-detector for deeper analysis).

## Output

Monitor configuration file and recurring check instructions for the agent runtime.
