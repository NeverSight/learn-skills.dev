---
name: scrape-docs
description: Scrape and extract documentation from a URL using Firecrawl. Use when you need to read external documentation.
context: fork
agent: Explore
---

# Scrape Documentation

Scrape and extract documentation from: $ARGUMENTS

## Strategy
1. Use Firecrawl MCP to scrape the target URL
2. Extract the key information and structure
3. Summarize the most important points
4. Identify code examples and configuration samples
5. Return a concise summary suitable for implementation

Focus on extracting actionable information, not reproducing the entire page.
