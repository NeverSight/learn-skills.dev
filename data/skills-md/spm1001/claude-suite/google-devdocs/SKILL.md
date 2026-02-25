---
name: google-devdocs
description: >
  Orchestrates Google developer documentation lookups via REST API using a 2-step
  search-then-retrieve workflow (curl + jq, no MCP). BEFORE scraping or guessing at Google API
  docs, invoke FIRST — returns fresh Markdown from 11 indexed sites including docs.cloud.google.com,
  firebase.google.com, developer.android.com, and ai.google.dev. Triggers on 'check the Google
  docs', 'look up the Firebase docs', 'what do the Cloud docs say', 'Google API documentation',
  'search Google developer docs'. (user)
---

# Google Developer Docs

Search and retrieve official Google developer documentation via the Developer Knowledge REST API. Returns Markdown — no scraping, no MCP server, just `curl` + `jq`.

## Prerequisites

Set the API key as an environment variable:

```bash
export GOOGLE_DEVKNOWLEDGE_API_KEY="your-key-here"
```

To get a key:
1. Enable the [Developer Knowledge API](https://console.cloud.google.com/start/api?id=developerknowledge.googleapis.com) in a Google Cloud project
2. Create an API key on the [Credentials page](https://console.cloud.google.com/apis/credentials)
3. Restrict the key to **Developer Knowledge API** only

If the variable is missing, tell the user and stop — don't attempt calls without it.

## When to Use

- User asks about Google Cloud, Firebase, Android, Chrome, Gemini, TensorFlow, or web.dev APIs
- You need current docs for a Google API (training data may be stale)
- Troubleshooting a Google API error — search for the error message
- Comparing Google services ("Cloud Run vs Cloud Functions for X")

## When NOT to Use

- Non-Google documentation (use web search or mise fetch instead)
- Content not in the corpus (GitHub repos, blogs, YouTube, Stack Overflow)
- User already pasted the relevant docs into the conversation

## Corpus

ai.google.dev · developer.android.com · developer.chrome.com · developers.home.google.com · developers.google.com · docs.cloud.google.com · docs.apigee.com · firebase.google.com · fuchsia.dev · web.dev · www.tensorflow.org

Re-indexed within 24 hours of publication.

## Workflow

### 1. Search — find relevant chunks

```bash
curl -s "https://developerknowledge.googleapis.com/v1alpha/documents:searchDocumentChunks?query=$(python3 -c "import urllib.parse; print(urllib.parse.quote('YOUR QUERY'))")&pageSize=10&key=$GOOGLE_DEVKNOWLEDGE_API_KEY" | jq .
```

This returns up to 10 chunk snippets with `parent` document names. Read the snippets — they may answer the question directly.

**Tip:** Use natural language queries. "How to authenticate with Firebase Admin SDK" works better than keywords.

### 2. Retrieve — get full document if needed

If snippets aren't enough, fetch the full page Markdown:

```bash
curl -s "https://developerknowledge.googleapis.com/v1alpha/PARENT_VALUE?key=$GOOGLE_DEVKNOWLEDGE_API_KEY" | jq -r '.content'
```

Replace `PARENT_VALUE` with the `parent` from a search result (e.g. `documents/firebase.google.com/docs/admin/setup`).

### 3. Batch retrieve — multiple docs at once

```bash
curl -s "https://developerknowledge.googleapis.com/v1alpha/documents:batchGet?names[]=PARENT1&names[]=PARENT2&key=$GOOGLE_DEVKNOWLEDGE_API_KEY" | jq .
```

Max 20 documents per batch.

## Extracting Results with jq

```bash
# List just the parent doc names from search
... | jq -r '.results[].parent'

# Get snippet text from search
... | jq -r '.results[] | "## \(.parent)\n\(.content)\n"'

# Get full doc content as raw markdown
... | jq -r '.content'
```

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Searching without checking the env var | Cryptic 403 error | Check `$GOOGLE_DEVKNOWLEDGE_API_KEY` first |
| Fetching full docs before reading snippets | Wastes tokens on irrelevant pages | Snippets answer most questions |
| Using keywords instead of natural language | Poor search results | Ask a question: "How do I..." |
| Fetching more than 3 full docs at once | Context overload | Read snippets, fetch only the most relevant |
| Scraping the docs site instead | Fragile, may be blocked, stale | Use this API — that's what it's for |
| Adding a corpus/site filter param | Doesn't exist in the API | Scope via natural language: "Firebase authentication" not "site:firebase.google.com auth" |

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 400 | Bad request (e.g. pageSize > 20) | Check parameters |
| 403 | API key invalid or API not enabled | Verify key and project setup |
| 404 | Document not found | Check the `parent` value is correct |
| 429 | Rate limited | Wait and retry |

## Integration

- **With mise:** Use this skill for Google docs; use mise for Drive/Gmail/general web content
- **With web search:** Fall back to web search for content outside the corpus (blogs, GitHub, SO)

## Reference

See `references/api-reference.md` for full endpoint details, response schemas, and the complete corpus list.
