---
name: arize-link
description: Generate deep links to traces, spans, and sessions in the Arize UI. Use when the user wants a clickable URL to open a specific trace, span, or session.
---

# Arize Link

Generate deep links to the Arize UI for traces, spans, and sessions.

## When to Use

- User wants a link to a specific trace, span, or session
- You have trace/span/session IDs from exported data or logs and need to link back to the UI
- User asks to "open" or "view" a trace/span/session in Arize

## Required Inputs

Collect these from the user or from context (e.g., exported trace data, parsed URLs):

- **org_id** -- Base64-encoded organization ID (from URL path or user)
- **space_id** -- Base64-encoded space ID (from URL path or user)
- **project_id** -- Base64-encoded project/model ID (from URL path or user)
- One of:
  - **trace_id** (and optionally **span_id**) for trace/span links
  - **session_id** for session links

## URL Construction

Base URL: `https://app.arize.com` (override for on-prem if the user specifies a custom base URL)

### Trace Link

Opens the trace slideover showing all spans in the trace.

```
{base_url}/organizations/{org_id}/spaces/{space_id}/projects/{project_id}?selectedTraceId={trace_id}&queryFilterA=&selectedTab=llmTracing&timeZoneA=America%2FLos_Angeles&startA={start_epoch_ms}&endA={end_epoch_ms}&envA=tracing&modelType=generative_llm
```

If a **span_id** is also available, add `&selectedSpanId={span_id}` to highlight that span within the trace.

### Span Link

Opens a specific span within a trace. Both trace_id and span_id are required.

```
{base_url}/organizations/{org_id}/spaces/{space_id}/projects/{project_id}?selectedTraceId={trace_id}&selectedSpanId={span_id}&queryFilterA=&selectedTab=llmTracing&timeZoneA=America%2FLos_Angeles&startA={start_epoch_ms}&endA={end_epoch_ms}&envA=tracing&modelType=generative_llm
```

### Session Link

Opens the session view for a conversation/interaction flow.

```
{base_url}/organizations/{org_id}/spaces/{space_id}/projects/{project_id}?selectedSessionId={session_id}&queryFilterA=&selectedTab=llmTracing&timeZoneA=America%2FLos_Angeles&startA={start_epoch_ms}&endA={end_epoch_ms}&envA=tracing&modelType=generative_llm
```

## Time Range

**CRITICAL**: `startA` and `endA` are **required** query parameters. Without them, the Arize UI defaults to the last 7 days and will show a "Your model doesn't have any recent data" error if the trace/span falls outside that window.

- **startA**: Start of the time window as epoch milliseconds
- **endA**: End of the time window as epoch milliseconds

### How to Determine the Time Range

Use these sources in priority order:

1. **User-provided URL**: If the user shared an Arize URL, extract `startA` and `endA` from it and reuse them. This is the most reliable approach since it preserves the user's original time window.

2. **Exported span data**: If you have span data (e.g., from `ax spans export`), use the span's `start_time` field to calculate a range that covers the data:
   ```bash
   # Convert span start_time to epoch ms, then pad ±1 day
   python -c "
   from datetime import datetime, timedelta
   t = datetime.fromisoformat('2026-03-07T05:39:15.822147Z'.replace('Z','+00:00'))
   start = int((t - timedelta(days=1)).timestamp() * 1000)
   end = int((t + timedelta(days=1)).timestamp() * 1000)
   print(f'startA={start}&endA={end}')
   "
   ```

3. **Default fallback**: Use the last 90 days. Calculate:
   - `startA`: `(now - 90 days)` as epoch milliseconds
   - `endA`: current time as epoch milliseconds

## Instructions

1. Gather the required IDs from the user or from available context (URLs, exported trace data, conversation history).
2. Determine `startA` and `endA` epoch milliseconds using the priority order above.
3. Substitute values into the appropriate URL template above.
4. Present the URL as a clickable markdown link.

## Example Output

Given: org_id=`QWNjb3VudE9yZ2FuaXphdGlvbjoxOmFiQzE=`, space_id=`U3BhY2U6MTp4eVo5`, project_id=`TW9kZWw6MTpkZUZn`, trace_id=`0123456789abcdef0123456789abcdef`

Trace link:
```
https://app.arize.com/organizations/QWNjb3VudE9yZ2FuaXphdGlvbjoxOmFiQzE=/spaces/U3BhY2U6MTp4eVo5/projects/TW9kZWw6MTpkZUZn?selectedTraceId=0123456789abcdef0123456789abcdef&queryFilterA=&selectedTab=llmTracing&timeZoneA=America%2FLos_Angeles&startA=1700000000000&endA=1700086400000&envA=tracing&modelType=generative_llm
```
