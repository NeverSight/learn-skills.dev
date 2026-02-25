---
name: finding
description: Use this skill when the user asks to "create a finding", "record an insight", "what findings exist", "show findings", or wants to create or review evidence-backed analysis insights from crawl observations. Creates and queries curated findings with evidence chains.
---

# finding

Create and query curated findings in Crawlio's observation log. Findings are agent-created insights backed by observation evidence.

## When to Use

Use this skill when the user wants to:
- Record an insight or issue discovered during analysis
- Create an evidence-backed finding that persists across sessions
- Review previously created findings for a site

## Creating Findings

Findings are the agent's judgment layer on top of raw observations. A good finding:
1. Has a clear, descriptive title
2. References specific observation IDs as evidence
3. Includes a synthesis explaining the pattern or issue

### Workflow

1. **Query observations** to identify patterns:
```
get_observations({ host: "example.com", source: "extension", limit: 50 })
```

2. **Identify the pattern** — look for recurring issues, framework signals, error patterns, or notable behaviors.

3. **Create the finding** with evidence:
```
create_finding({
  title: "Mixed content: HTTP images on HTTPS page",
  url: "https://example.com",
  evidence: ["obs_a3f7b2c1", "obs_b4e8c3d2"],
  synthesis: "Homepage loads 3 images over HTTP despite serving over HTTPS. Network observations show requests to http://cdn.example.com/img/ which should use HTTPS. This triggers mixed content warnings in Chrome and may cause images to be blocked in strict mode."
})
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `title` | string | Yes | Short, descriptive title |
| `url` | string | No | URL this finding relates to |
| `evidence` | [string] | No | Array of observation IDs (`obs_xxx`) |
| `synthesis` | string | No | Detailed explanation |

### Finding Quality Checklist

- **Title**: Is it specific? "Mixed content on homepage" > "Issue found"
- **Evidence**: Do the observation IDs actually support the claim?
- **Synthesis**: Does it explain *why* this matters, not just *what* was observed?
- **URL**: Is it scoped to the right page or left empty for site-wide findings?

## Querying Findings

### All Findings

```
get_findings({})
```

### Findings for a Specific Host

```
get_findings({ host: "example.com" })
```

### Recent Findings

```
get_findings({ limit: 10 })
```

## Finding Categories

When creating findings, consider these common categories:

| Category | Example Title |
|----------|--------------|
| **Performance** | "Render-blocking scripts delay FCP by 2.3s" |
| **Security** | "Mixed content: HTTP resources on HTTPS page" |
| **SEO** | "Missing meta descriptions on 12 pages" |
| **Framework** | "Next.js App Router with ISR detected" |
| **Errors** | "3 JavaScript errors on product pages" |
| **Structure** | "Orphaned pages not linked from navigation" |
| **Accessibility** | "Missing alt attributes on hero images" |

## Tips

- Create findings as you analyze, not all at the end — they persist across sessions
- Reference multiple observation IDs when a finding draws from several data points
- Use synthesis to explain the *impact*, not just restate the observation
- Findings with evidence chains are much more useful than findings without
