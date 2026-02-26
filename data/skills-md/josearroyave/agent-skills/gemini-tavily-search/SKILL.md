---
name: gemini-tavily-search
description: "Use this skill when the user asks about current events, real-time information, recent news, live scores, financial data, price updates, recent changes, or any question that may require up-to-date web information. This skill first determines if web search is necessary using Gemini, then attempts Google Search Grounding via Gemini, and automatically falls back to Tavily if any failure occurs."
---

# gemini-tavily-search

## Purpose

Provide reliable, up-to-date web information using a resilient multi-provider strategy:

Gemini (primary, optional google_search grounding)  
→ automatic fallback → Tavily

The agent always receives normalized JSON output and never raw provider errors.

## Activation Criteria

Use this skill ONLY when:

- The question involves current or recent information
- News, events, live scores, financial updates
- Time-sensitive data
- Facts that may have changed recently
- Verification against authoritative sources is required
- The model may not have the latest information in its training data

## Do NOT Activate When

Do NOT use this skill when:

- The question is stable general knowledge
- Historical facts that do not change
- Conceptual explanations
- Code-related tasks
- Local file operations
- Documentation already available in context
- Another more specific skill is better suited

## Internal Logic

1. Perform a lightweight Gemini classification call to determine if web search is required.
2. If web search is NOT required → answer directly via Gemini without tools.
3. If web search IS required → call Gemini with `google_search` tool enabled.
4. If Gemini fails for ANY reason (timeout, quota error, HTTP error, invalid JSON, API error object, malformed response):
   - Automatically execute Tavily fallback.
5. Normalize provider output into unified JSON schema.
6. Always return valid structured JSON.

The agent must not describe fallback logic to the user.

## Input

Call the script with a single JSON argument.

### Required

- `query` (string)

### Optional (forwarded to Tavily if fallback occurs)

- `search_depth`
- `topic`
- `max_results`
- `time_range`
- `start_date`
- `end_date`
- `include_domains`
- `exclude_domains`
- `country`
- additional Tavily-compatible parameters

## Environment Requirements

Required:

- `TAVILY_API_KEY`
- `GEMINI_API_KEY`

Optional:

- `GEMINI_MODEL` (default: gemini-2.5-flash-lite)

```json
{
  "env": {
    "GEMINI_MODEL": "gemini-2.5-flash-lite",
    "GEMINI_API_KEY": "your-gemini-key",
    "TAVILY_API_KEY": "your-tavily-key"
  }
}
```

## Output Schema (Unified)

The tool always returns JSON in this format:

```json
{
  "provider": "gemini | tavily",
  "answer": "text or null",
  "results": [
    {
      "title": "Source title",
      "url": "https://example.com",
      "snippet": "Relevant excerpt"
    }
  ],
  "fallback": true | false
}
```

If both providers fail:

```json
{
  "provider": "tavily",
  "answer": null,
  "results": [],
  "fallback": true,
  "error": "tavily_failed"
}
```

## Post-Processing Requirement

After generating the final answer for the user, append:

_Searched with: <provider>_

Where `<provider>` matches the returned JSON:

- "gemini"
- "tavily"

If no web search was used:

_Searched with: none_
