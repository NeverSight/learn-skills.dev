---
name: observe
description: Use this skill when the user asks to "check observations", "what did Crawlio see", "show crawl timeline", "query the observation log", or wants to review what happened during a crawl session. Queries the append-only observation log with filtering by host, source, operation, and time range.
---

# observe

Query Crawlio's observation log — the append-only timeline of everything Crawlio observed during a crawl session.

## When to Use

Use this skill when the user wants to:
- See what happened during a crawl
- Review extension captures (framework detection, network requests, console logs)
- Reconstruct a timeline of events
- Find specific observations by host, source, or time range

## Quick Reference

### Get Recent Observations

```
get_observations({ limit: 20 })
```

### Filter by Host

```
get_observations({ host: "example.com", limit: 50 })
```

### Filter by Source

| Source | What It Captures |
|--------|-----------------|
| `extension` | Chrome extension enrichment (framework, network, console, DOM) |
| `engine` | Crawl lifecycle events (crawl_start, crawl_done) |
| `webkit` | WebKit runtime capture |
| `agent` | AI-created findings |

```
get_observations({ source: "extension", limit: 30 })
```

### Filter by Operation

| Op | Meaning |
|----|---------|
| `observe` | Raw data capture |
| `finding` | Agent-created insight |
| `crawl_start` | Crawl began |
| `crawl_done` | Crawl completed |
| `page` | Single page observation |

```
get_observations({ op: "crawl_done" })
```

### Time-Based Query

Use Unix timestamps to query a time range:

```
get_observations({ since: 1708444200, limit: 100 })
```

### Combine Filters

```
get_observations({
  host: "example.com",
  source: "extension",
  op: "observe",
  limit: 50
})
```

## Reading Observations

Each observation entry contains:

- **id** — unique identifier (`obs_` prefix for observations, `fnd_` for findings)
- **op** — what type of event this is
- **ts** — ISO 8601 timestamp
- **url** — the URL this relates to
- **source** — what produced this entry
- **data** — composite payload (framework detection, network requests, console logs, progress, etc.)

## Common Patterns

### Timeline Reconstruction
Query by host with no limit to see the full story of a crawl:
```
get_observations({ host: "example.com" })
```

### Crawl Summary
Get start and end events to see crawl performance:
```
get_observations({ op: "crawl_start" })
get_observations({ op: "crawl_done" })
```
The `crawl_done` entry includes progress data (totalDiscovered, downloaded, failed).

### Extension Audit
See everything the Chrome extension captured:
```
get_observations({ source: "extension", limit: 200 })
```

### After Observation — Create Findings
Once you've identified patterns in observations, use the `finding` skill to record insights with evidence chains.
