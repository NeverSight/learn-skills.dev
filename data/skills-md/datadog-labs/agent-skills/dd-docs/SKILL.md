---
name: dd-docs
description: Datadog docs lookup using docs.datadoghq.com/llms.txt and linked Markdown pages.
metadata:
  version: "1.0.0"
  author: datadog-labs
  repository: https://github.com/datadog-labs/agent-skills
  tags: datadog,docs,llms.txt,dd-docs
  alwaysApply: "false"
---

# Datadog Docs

Use this skill to locate Datadog documentation and limits.

## LLM-Friendly Documentation

Datadog provides an LLM-optimized documentation index at:

```
https://docs.datadoghq.com/llms.txt
```

This file contains:
- Overview of all Datadog products organized by use case
- Full list of documentation pages with URLs and descriptions
- Direct links to Markdown sources (append `.md` to URLs)

### How to Use llms.txt

1. **Fetch the index** to understand available documentation:
   ```bash
   curl -s https://docs.datadoghq.com/llms.txt | head -100
   ```

2. **Search for specific topics**:

Examples:

   ```bash
   curl -s https://docs.datadoghq.com/llms.txt | grep -i "monitors"
   curl -s https://docs.datadoghq.com/llms.txt | grep -i "apm"
   curl -s https://docs.datadoghq.com/llms.txt | grep -i "logs"
   ```

3. **Fetch specific doc pages** (add .md to most Datadog Docs URLs for raw content):
   ```bash
   curl -s https://docs.datadoghq.com/monitors.md
   curl -s https://docs.datadoghq.com/tracing.md
   ```

### Key Documentation Sections

| Topic | URL |
|-------|-----|
| APM/Tracing | https://docs.datadoghq.com/tracing/ |
| Logs | https://docs.datadoghq.com/logs/ |
| Metrics | https://docs.datadoghq.com/metrics/ |
| Monitors | https://docs.datadoghq.com/monitors/ |
| Dashboards | https://docs.datadoghq.com/dashboards/ |
| Security | https://docs.datadoghq.com/security/ |
| Synthetics | https://docs.datadoghq.com/synthetics/ |
| RUM | https://docs.datadoghq.com/real_user_monitoring/ |
| Incidents | https://docs.datadoghq.com/service_management/incident_management/ |
| API Reference | https://docs.datadoghq.com/api/ |

## Scope Guardrails

- Use llms.txt for documentation lookups
- Defer to official docs for feature availability and limits

## Failure Handling

- If docs.datadoghq.com is unreachable, check network connectivity
- For region-specific docs, use appropriate site (datadoghq.eu, etc.)
