---
name: web-fetch
description: Retrieves and analyzes content from user-provided URLs or search results using the WebFetch tool. Manages domain filtering and max_uses limits to prevent data exfiltration. Use when users provide URLs to fetch, when analyzing web pages, or when following up on search results.
version: 1.0.0
allowed-tools: WebFetch, Read, Write, Bash
---

# Web Fetch Skill

This skill enables Claude to safely retrieve and analyze web content from user-provided URLs or search results while implementing security controls to prevent data exfiltration.

## When to Use This Skill

Use this skill when:
- User provides a URL to fetch and analyze
- User asks to retrieve content from a web page
- User wants to follow up on WebSearch results by fetching full content
- User needs to extract information from a PDF hosted online
- User requests analysis of documentation, blog posts, or web resources

## Security Controls

### Domain Filtering

The WebFetch tool supports domain filtering to restrict which sites can be accessed:

1. **Allowed Domains** - Whitelist approach (only these domains permitted)
2. **Blocked Domains** - Blacklist approach (all except these domains)

**IMPORTANT**: Never build or guess URLs. Only use:
- URLs explicitly provided by the user
- URLs returned from WebSearch results
- URLs found in local files (with user confirmation)

### Max Uses Tracking

To prevent data exfiltration, track the number of WebFetch calls per session:

- **Default limit**: 10 fetches per conversation (adjustable based on user needs)
- **Warning threshold**: Alert user at 7 fetches
- **Hard stop**: Require explicit user approval beyond limit

## Usage Guidelines

### 1. Single URL Fetch

When user provides a single URL:

```markdown
User: "Can you fetch and analyze https://example.com/article"

Steps:
1. Validate the URL is user-provided (not generated)
2. Determine appropriate prompt for analysis
3. Use WebFetch with clear, specific prompt
4. Increment fetch counter
5. Analyze and present results
```

Example:
```
WebFetch:
  url: https://example.com/article
  prompt: Extract and summarize the main points of this article, including key arguments and conclusions.
```

### 2. Multiple URLs from Search Results

When following up on WebSearch results:

```markdown
User: "Search for Python async best practices and analyze the top results"

Steps:
1. Perform WebSearch first
2. Present search results to user
3. Ask user which URLs to fetch (don't assume)
4. Fetch user-approved URLs sequentially
5. Track total fetches against max_uses
6. Synthesize findings across sources
```

### 3. Domain Filtering

When user specifies domain restrictions:

```markdown
User: "Fetch Python docs but avoid third-party blogs"

Apply filters:
- allowed_domains: ["docs.python.org", "peps.python.org"]
OR
- blocked_domains: ["medium.com", "dev.to", "blogger.com"]
```

Example:
```
WebFetch:
  url: https://docs.python.org/3/library/asyncio.html
  prompt: Explain the asyncio event loop and provide key usage examples
  allowed_domains: ["docs.python.org", "peps.python.org"]
```

### 4. PDF Content Retrieval

When fetching PDF documents:

```markdown
User: "Can you analyze this research paper: https://example.com/paper.pdf"

Steps:
1. Verify URL ends in .pdf or user confirms it's a PDF
2. Use specific prompt for academic content
3. WebFetch automatically processes PDF pages
4. Extract text and visual content
5. Provide structured analysis
```

Example:
```
WebFetch:
  url: https://example.com/paper.pdf
  prompt: Extract the abstract, methodology, key findings, and conclusions from this research paper.
```

## Workflow Pattern

```
1. Receive URL request from user
   ↓
2. Validate URL source (user-provided/search result)
   ↓
3. Check fetch counter against max_uses
   ↓
4. Apply domain filters if specified
   ↓
5. Construct specific, clear prompt
   ↓
6. Execute WebFetch tool
   ↓
7. Increment counter
   ↓
8. Analyze results
   ↓
9. Present findings to user
```

## Max Uses Implementation

Track fetches within conversation:

```
Fetch Count Tracking:
- Initialize: fetch_count = 0
- After each WebFetch: fetch_count += 1
- At 7 fetches: "Note: Approaching fetch limit (7/10). Let me know if you need to adjust."
- At 10 fetches: "Reached fetch limit (10/10). Do you want to continue? This helps prevent unintended data access."
- Beyond 10: Require explicit user "yes" before proceeding
```

### Reset Conditions

The fetch counter resets:
- At the start of each new conversation
- When user explicitly requests reset
- Never automatically mid-conversation

## Prompt Crafting Best Practices

Create specific, actionable prompts for WebFetch:

### Good Prompts ✓
- "Extract the installation instructions and list all dependencies mentioned"
- "Summarize the main argument and supporting evidence from this article"
- "List all API endpoints documented on this page with their parameters"
- "Extract code examples showing async/await usage"

### Poor Prompts ✗
- "Tell me about this page" (too vague)
- "What does this say?" (unclear goal)
- "Read this" (no analysis requested)
- "Everything" (overly broad)

## Error Handling

### Redirect Detection

When WebFetch returns a redirect message:
```
1. WebFetch indicates redirect to different host
2. Present redirect URL to user
3. Ask for confirmation to follow
4. Make new WebFetch with redirect URL
5. Count as separate fetch
```

### Fetch Failures

If WebFetch fails:
```
1. Check URL format (valid, fully-formed)
2. Verify domain filters aren't blocking
3. Confirm URL is accessible (not behind auth)
4. Suggest alternative approach (search for cached version)
5. Don't retry automatically (counts against max_uses)
```

## Examples

### Example 1: Simple Article Fetch
```
User: "Can you fetch and summarize https://example.com/blog/new-features"

Response:
1. Use WebFetch with:
   - url: https://example.com/blog/new-features
   - prompt: "Summarize the new features described, including their benefits and any code examples provided"
2. Fetch count: 1/10
3. Present summary with key points
```

### Example 2: Search + Selective Fetch
```
User: "Find articles about Rust error handling and analyze the best one"

Response:
1. WebSearch: "Rust error handling best practices"
2. Present top 5 results
3. User selects: "The second one looks good"
4. WebFetch selected URL only
5. Fetch count: 1/10
6. Analyze and explain Rust error handling patterns
```

### Example 3: Multiple Fetches with Domain Filter
```
User: "Compare official Python and Rust async documentation"

Response:
1. WebFetch: https://docs.python.org/3/library/asyncio.html
   - allowed_domains: ["docs.python.org"]
   - prompt: "Explain Python's async/await model and event loop"
   - Fetch count: 1/10

2. WebFetch: https://doc.rust-lang.org/book/async-await.html
   - allowed_domains: ["doc.rust-lang.org"]
   - prompt: "Explain Rust's async/await model and futures"
   - Fetch count: 2/10

3. Synthesize comparison
```

### Example 4: PDF Research Paper
```
User: "Analyze this ML paper: https://arxiv.org/pdf/2301.12345.pdf"

Response:
1. WebFetch with:
   - url: https://arxiv.org/pdf/2301.12345.pdf
   - prompt: "Extract abstract, methodology, datasets used, key results, and main conclusions from this machine learning research paper"
2. Fetch count: 1/10
3. Present structured analysis:
   - Abstract summary
   - Methods overview
   - Key findings
   - Conclusions and implications
```

## Security Checklist

Before each WebFetch, verify:

- [ ] URL is user-provided or from search results (not generated)
- [ ] Fetch count is within limits or user approved
- [ ] Domain filters applied if specified
- [ ] Prompt is specific and purposeful
- [ ] Not fetching sensitive/internal URLs
- [ ] User understands what will be fetched

## Integration with Other Skills

This skill works well with:

- **summarization**: Fetch content, then summarize it
- **code-review**: Fetch code examples for analysis
- **research**: Gather information from multiple sources
- **learning**: Fetch documentation and tutorials

## Limitations

Be aware of:

1. **Cannot build URLs**: Only use explicitly provided URLs
2. **No authentication**: Cannot fetch content behind login
3. **Rate limits**: Some sites may block automated requests
4. **Large content**: Very large pages may be summarized
5. **Dynamic content**: JavaScript-rendered content may not be available
6. **Cache timing**: 15-minute cache may show stale content

## Best Practices Summary

1. ✅ Always use user-provided or search-returned URLs
2. ✅ Track fetch count and warn before limits
3. ✅ Write specific, actionable prompts
4. ✅ Apply domain filters when appropriate
5. ✅ Handle redirects explicitly
6. ✅ Present findings clearly to user
7. ❌ Never generate or guess URLs
8. ❌ Never auto-fetch without user intent
9. ❌ Never bypass max_uses without approval
10. ❌ Never fetch sensitive/internal domains

## Quick Reference

| Task | Command | Notes |
|------|---------|-------|
| Fetch single URL | `WebFetch(url, prompt)` | Count: +1 |
| Fetch with whitelist | `WebFetch(url, prompt, allowed_domains=[...])` | Restricts to list |
| Fetch with blacklist | `WebFetch(url, prompt, blocked_domains=[...])` | Blocks list |
| Fetch PDF | `WebFetch(url, prompt)` | Auto-detects PDF |
| Check fetch count | Review internal counter | Warn at 7, stop at 10 |
| Handle redirect | Get redirect URL → new WebFetch | Count: +1 each |

---

**Remember**: This skill prioritizes security through URL validation, domain filtering, and usage limits while enabling powerful web content retrieval capabilities.
