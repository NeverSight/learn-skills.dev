---
name: webflow-browser-api
description: Control Webflow Analyze and Optimize from JavaScript via the Browser API. Use when managing tracking consent, integrating CMPs (OneTrust, TrustArc), tracking experiment variations, setting custom visitor attributes, or personalizing user experiences.
license: MIT
metadata:
  author: "Ben Sabic"
  repository: "https://github.com/224-industries/webflow-skills"
  url: "https://skills.224ai.au/webflow-browser-api.skill"
  version: "1.0.0"
  keywords: "ai, agent, skill, analyze, browser, api, webflow, optimize, cookie consent, tracking, performance, user experience, consent management, web analytics, automation"
---

# Webflow Browser API

The Browser API is a JavaScript interface exposed via the global `wf` object on all Webflow sites with Analyze and Optimize enabled. It requires no manual installation. Use it to manage consent, track experiments, and personalize user experiences.

## Key Concepts

- **Global `wf` object** — Automatically available on all sites with Analyze or Optimize enabled
- **`wf.ready()`** — All Browser API calls must be wrapped in this readiness callback. See `references/wf-ready.md`
- **Consent management** — Three methods to manage tracking consent: `getUserTrackingChoice()`, `allowUserTracking()`, `denyUserTracking()`
- **Variations** — Track experiment results via `onVariationRecorded()` and forward to analytics tools
- **Custom attributes** — Set visitor attributes via `setAttributes()` for audience targeting and result filtering (Enterprise only)

## API Methods

| Method | Description |
|--------|-------------|
| `wf.ready(callback)` | Execute code after the Browser API loads |
| `wf.getUserTrackingChoice()` | Returns `"allow"`, `"deny"`, or `"none"` |
| `wf.allowUserTracking(options?)` | Opt user into tracking |
| `wf.denyUserTracking(options?)` | Opt user out of tracking |
| `wf.onVariationRecorded(callback)` | Register a callback for variation events |
| `wf.setAttributes(scope, attributes)` | Set custom visitor attributes |

## Important Notes

- The Browser API is only available on sites with Webflow Analyze or Optimize enabled
- Custom JavaScript attributes (`setAttributes`) are only available on Enterprise sites
- Always wrap all API calls inside `wf.ready()` to prevent calls before initialization
- Place scripts in `<head>` custom code for earliest possible execution

## Reference Documentation

Each reference file includes YAML frontmatter with `name`, `description`, and `tags` for searchability. Use the search script in `scripts/search_references.py` to find relevant references.

### Getting Started

- **[references/introduction.md](references/introduction.md)**: Overview, capabilities, placement options, getting started
- **[references/wf-ready.md](references/wf-ready.md)**: `wf.ready()` API reference

### Consent Management

- **[references/consent-management.md](references/consent-management.md)**: Consent APIs, CMP integrations (OneTrust, TrustArc), custom consent solutions

### Optimize

- **[references/optimize-overview.md](references/optimize-overview.md)**: Optimize overview and quickstart
- **[references/variations.md](references/variations.md)**: Variations concept and `onVariationRecorded()` API reference
- **[references/attributes.md](references/attributes.md)**: Custom attributes and `setAttributes()` API reference

### Searching References

```bash
# List all references with metadata
python scripts/search_references.py --list

# Search by tag (exact match)
python scripts/search_references.py --tag <tag>

# Search by keyword (across name, description, tags, and content)
python scripts/search_references.py --search <query>
```

## Scripts

- **`scripts/search_references.py`**: Search reference files by tag, keyword, or list all with metadata
