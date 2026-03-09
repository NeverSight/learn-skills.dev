---
name: ai-news-collector
description: Automatically collect and summarize daily AI industry news, trends, and hot topics from platforms like GitHub (trending repos), X/Twitter (AI influencers/hashtags), and AI news aggregators. Use this skill when the user asks for "today's AI news", "AI industry updates", "what's trending in AI", or wants a daily digest of AI developments.
---

# AI News Collector

This skill provides workflows and tools to collect, filter, and summarize the latest developments in the AI industry across major platforms.

## Core Capabilities

- **GitHub Trending**: Extract trending AI/ML repositories, new tools, and open-source models.
- **X (Twitter) Updates**: Gather updates from key AI researchers, organizations, and trending AI hashtags.
- **News Aggregation**: Summarize top AI headlines from tech news sources.
- **Digest Generation**: Compile the collected information into a structured, easy-to-read markdown digest.

## Workflows

### 1. Generating a Daily AI Digest

When a user requests a daily AI news summary, follow this process:

1. **Information Gathering**:
   - MUST RESTRICT SEARCH TO THE LAST 7 DAYS. Use explicit date filters (e.g., in `curl` or `web_search`) to ensure no news or repositories older than one week are included.
   - Use the web search tool to find the current GitHub trending repositories (filter by spoken language or programming language like Python/Jupyter Notebook).
   - Search for recent AI news using queries like "AI news today", "latest artificial intelligence developments", or specific topics (e.g., "OpenAI news", "new LLM releases").
   - If applicable and accessible, search for trending AI discussions on X (Twitter).

2. **Filtering & Curation**:
   - Filter out noise and generic news.
   - Focus on: New model releases, significant open-source projects, major industry announcements, breakthrough research, and trending developer tools.
   - STRICTLY exclude any items older than 7 days.

3. **Formatting the Digest**:
   - Use the template provided in `references/digest-template.md` to structure the output.
   - Group items logically (e.g., Open Source & GitHub, Industry News, Research & Papers).
   - Provide brief, 1-2 sentence summaries for each item.
   - **MANDATORY**: Every single news item, repository, paper, or tweet MUST include its original source URL as a markdown link `[Link](url)`.

### 2. Deep Dive on a Specific AI Topic

If the user asks for news about a specific sub-field (e.g., "What's new in AI image generation?"):

1. Adjust search queries to focus strictly on that niche.
2. Structure the response to highlight the most impactful recent developments in that specific area.
3. Ensure all links and 7-day time limits are strictly applied.

## Best Practices

- **Freshness (Critical)**: Always verify that the news or repositories are actually recent (Strictly within the last 7 days). Discard anything older.
- **Conciseness**: Avoid long articles; extract the core value proposition of a new tool or the main takeaway of a news item.
- **Categorization**: Well-organized digests are much easier to read than flat lists.
- **Citations (Critical)**: Always include URLs to the original source (GitHub repo, news article, or tweet). A report item without a source link is considered invalid.

## Available Resources

- **Template**: See `references/digest-template.md` for the standard output format.
