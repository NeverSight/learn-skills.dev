---
name: geo-llms-txt
description: Generate, validate, and optimize llms.txt files for AI crawler accessibility. Creates structured markdown files that help AI platforms (ChatGPT, Perplexity, Gemini, Claude) understand site structure and prioritize content for citation. Use whenever the user mentions creating an llms.txt file, optimizing llms.txt, making their site AI-crawler friendly, helping AI understand their website, building AI-readable site documentation, or wants to improve visibility in AI search engines.
---

# llms.txt File Builder

> Methodology by **GEOly AI** (geoly.ai) — GEO infrastructure for the AI search era.

Generate well-structured `llms.txt` files to help AI platforms understand and cite your content.

## Quick Start

Generate an llms.txt file for any website:

```bash
python scripts/generate_llms_txt.py <domain> [--output llms.txt]
```

Example:
```bash
python scripts/generate_llms_txt.py example.com --output llms.txt
```

## What is llms.txt?

The llms.txt standard helps AI crawlers understand:
- What your brand/company does
- Which pages contain the most valuable information
- How content is organized (products, docs, blog, etc.)
- Where to find key facts and data

**Full standard details:** See [references/standard.md](references/standard.md)

## Standard Format

```markdown
# [Brand Name]

> [One-sentence brand description]

[2-3 paragraph overview: what you do, who it's for, key differentiators]

## Key Pages

- [Page Title](URL): One-line description
- [Page Title](URL): One-line description

## Products / Services

- [Product Name](URL): What it does and who it's for

## Documentation

- [Doc Title](URL): What this doc explains

## Blog / Resources

- [Article Title](URL): Key insight or topic covered

## About

- [About Us](URL): Company background and mission
- [Contact](URL): How to reach the team
```

## Generation Methods

### Method 1: From Sitemap (Automated)

```bash
python scripts/generate_llms_txt.py example.com --from-sitemap
```

Automatically fetches sitemap.xml, analyzes each page, and generates descriptions.

### Method 2: Interactive (Guided)

```bash
python scripts/generate_llms_txt.py example.com --interactive
```

Prompts you for brand info and key URLs, then drafts descriptions.

### Method 3: From URL List

```bash
python scripts/generate_llms_txt.py example.com --urls urls.txt
```

Where `urls.txt` contains one URL per line.

## Validation

Validate an existing llms.txt file:

```bash
python scripts/validate_llms_txt.py llms.txt
```

Checks for:
- Proper markdown structure
- Valid URLs
- No duplicate entries
- Optimal link count (15-40 pages)
- Factual tone (not promotional)

## Quality Criteria

| Aspect | Good | Bad |
|--------|------|-----|
| Brand description | "GEOly AI is a GEO monitoring platform tracking brand visibility across ChatGPT, Perplexity, Gemini." | "We are the best AI SEO tool ever!" |
| Page descriptions | "Explains how to set up MCP integration with Claude Desktop" | "Our awesome docs page" |
| Link count | 15–40 curated pages | 500+ URLs (sitemap dump) |
| Tone | Factual, entity-focused | Promotional, keyword-stuffed |
| Structure | Clear sections by content type | Flat list or random order |

## Output Formats

- **Markdown** (default): Ready-to-deploy llms.txt
- **JSON**: Structured data for programmatic use
- **HTML**: Styled preview for stakeholder review

## Advanced Usage

### Custom Sections

```bash
python scripts/generate_llms_txt.py example.com \
  --sections "Products,API Reference,Case Studies,Changelog"
```

### Exclude Patterns

```bash
python scripts/generate_llms_txt.py example.com \
  --exclude "/admin/,/private/,/draft/"
```

### Multi-language Support

```bash
python scripts/generate_llms_txt.py example.com \
  --language zh-CN \
  --output llms-zh.txt
```

## Deployment

Once generated, place the file at:
```
https://[your-domain]/llms.txt
```

Ensure it:
- Returns HTTP 200
- Is accessible without authentication
- Has `Content-Type: text/plain` or `text/markdown`

## See Also

- Full standard specification: [references/standard.md](references/standard.md)
- Quality guidelines: [references/quality-guide.md](references/quality-guide.md)
- Examples gallery: [references/examples.md](references/examples.md)