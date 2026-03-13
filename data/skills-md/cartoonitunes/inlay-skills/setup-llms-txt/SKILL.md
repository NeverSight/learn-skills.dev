---
name: setup-llms-txt
description: |
  Create and configure llms.txt for any website or project.
  Analyzes project structure, generates llms.txt and llms-full.txt,
  places files in the correct location for your framework.
  Use when setting up llms.txt, improving AI discoverability, or
  making a site LLM-friendly.
triggers:
  - "llms.txt"
  - "llms-full.txt"
  - "LLM discoverability"
  - "AI readable"
---

# Setup llms.txt Skill

Create and configure `llms.txt` and `llms-full.txt` for any website. These files help LLMs understand your site — think of them as `robots.txt` for AI models.

## What is llms.txt?

`llms.txt` is a standard file (served at `/llms.txt`) that tells AI models:
- What your site/product does
- Where to find key resources (docs, API, guides)
- How to interact with your service

`llms-full.txt` is an expanded version with full content that LLMs can ingest without following links.

**Spec:** https://llmstxt.org

## Workflow

### Step 1: Analyze the Project

Examine the project structure to understand:
- What the site/product does
- Key pages and documentation
- API endpoints (if any)
- Framework being used

```bash
# Check framework
ls package.json next.config.* astro.config.* gatsby-config.* nuxt.config.* 2>/dev/null

# Find key content
find . -name "*.md" -o -name "*.mdx" | head -20
ls -la public/ static/ 2>/dev/null

# Check for existing llms.txt
curl -s "https://YOUR_SITE/llms.txt" | head -5
```

### Step 2: Generate llms.txt

Create the file following the standard format:

```text
# [Site/Product Name]

> [One-line description of what the site does]

## Docs
- [Getting Started](/docs/getting-started): How to get started with [Product]
- [API Reference](/docs/api): Full API documentation
- [Examples](/docs/examples): Code examples and tutorials

## API
- Base URL: https://api.example.com
- [Authentication](/docs/auth): How to authenticate API requests
- [Rate Limits](/docs/rate-limits): API rate limiting details

## Key Pages
- [Pricing](/pricing): Plans and pricing
- [Blog](/blog): Latest updates and articles
- [Changelog](/changelog): Product updates

## Contact
- Support: support@example.com
- Twitter: @example
```

**Guidelines:**
- Use Markdown format
- Start with `#` heading and `>` blockquote summary
- Group links by category with `##` headings
- Use descriptive link text with brief explanations
- Include all important pages and resources
- Keep it concise — this is a summary, not full docs

### Step 3: Generate llms-full.txt (Optional but Recommended)

Create an expanded version with full content inline:

```text
# [Site/Product Name]

> [Description]

## Getting Started

[Full getting started content here, not just a link]

## API Reference

[Full API docs inline]

...
```

This is especially valuable for documentation sites — LLMs can ingest the full content in one request.

### Step 4: Place Files

Place based on framework:

| Framework | Location |
|-----------|----------|
| Next.js | `public/llms.txt` |
| Astro | `public/llms.txt` |
| Gatsby | `static/llms.txt` |
| Hugo | `static/llms.txt` |
| Nuxt | `public/llms.txt` |
| SvelteKit | `static/llms.txt` |
| Vite/React | `public/llms.txt` |
| Plain HTML | Root directory |
| Express/API | Serve via route handler |

### Step 5: Validate

```bash
# Check it's accessible
curl -s https://YOUR_SITE/llms.txt | head -20

# Verify content type (should be text/plain or text/markdown)
curl -sI https://YOUR_SITE/llms.txt | grep -i content-type

# Check llms-full.txt too
curl -s https://YOUR_SITE/llms-full.txt | head -20
```

### Step 6: Verify with Inlay

Run an AI readiness audit to confirm the llms.txt is detected:

```bash
curl -s -X POST https://www.inlay.dev/api/audit \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://YOUR_SITE"}'
```

The llms.txt category score should improve after adding the file.

## Tips

- Keep llms.txt under 10KB — it's a summary
- llms-full.txt can be larger but aim for under 500KB
- Update when you add major features or change docs structure
- Include API endpoints if you have a public API
- Link to your MCP server if you have one
