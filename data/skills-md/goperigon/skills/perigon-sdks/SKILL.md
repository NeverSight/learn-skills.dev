---
name: perigon-sdks
description: Best practices for using the official Perigon SDKs (TypeScript, Python, Go). Use this skill when installing, configuring, or writing code with any Perigon SDK to search news, track stories, summarize content, perform vector search, query Wikipedia, or look up people, companies, journalists, and sources.
license: Apache-2.0
metadata:
  author: goperigon
  version: "1.0.0"
  organization: Perigon
  date: February 2026
  abstract: Comprehensive guide for integrating the Perigon News Intelligence API using the official TypeScript, Python, and Go SDKs. Covers installation, client setup, all endpoint methods, error handling, and idiomatic patterns for each language.
---

# Perigon SDKs Best Practices

Guide for using the official Perigon SDKs to integrate the Perigon News Intelligence API into TypeScript/Node.js, Python, and Go applications.

## When to Apply

Reference these guidelines when:
- Installing or setting up a Perigon SDK in a new or existing project
- Initializing the Perigon client and configuring authentication
- Calling any Perigon API endpoint through an SDK (articles, stories, vector search, summarizer, Wikipedia, entities)
- Handling errors, retries, or rate limits from SDK calls
- Choosing which SDK to use for a given project or runtime
- Writing async code with the Python SDK or context-based code with the Go SDK
- Constructing typed request parameters or parsing typed responses

## SDK Selection Guide

```
TypeScript/JavaScript project?  → @goperigon/perigon-ts
Python project?                 → perigon (PyPI)
Go project?                     → github.com/goperigon/perigon-go-sdk/v2
```

All three SDKs cover the same API surface. Choose based on your project language.

## SDK Comparison

| | TypeScript | Python | Go |
|---|---|---|---|
| **Package** | `@goperigon/perigon-ts` | `perigon` | `github.com/goperigon/perigon-go-sdk/v2` |
| **Install** | `npm install @goperigon/perigon-ts` | `pip install perigon` | `go get github.com/goperigon/perigon-go-sdk/v2` |
| **Client init** | `new V1Api(new Configuration({apiKey}))` | `V1Api(ApiClient(api_key=...))` | `perigon.NewClient(option.WithAPIKey(...))` |
| **Method style** | `perigon.searchArticles({...})` | `api.search_articles(...)` | `client.All.List(ctx, params)` |
| **Async** | Native Promises | `_async` suffix methods | Context-based |
| **Type system** | Full TS types | Pydantic models, PEP 561 | Strongly-typed with `param.Opt[T]` |
| **Error type** | `ResponseError` | `ApiException` | `*perigon.Error` |
| **Retries** | Manual | Manual | Built-in (default 2) |

## Authentication

All SDKs read the API key from the `PERIGON_API_KEY` environment variable by default. You can also pass it explicitly:

**TypeScript:**
```ts
import { Configuration, V1Api } from "@goperigon/perigon-ts";
const perigon = new V1Api(new Configuration({ apiKey: process.env.PERIGON_API_KEY }));
```

**Python:**
```python
from perigon import V1Api, ApiClient
api = V1Api(ApiClient(api_key=os.environ["PERIGON_API_KEY"]))
```

**Go:**
```go
client := perigon.NewClient() // reads PERIGON_API_KEY env var
// or explicitly:
client := perigon.NewClient(option.WithAPIKey("your-key"))
```

## Endpoint-to-Method Mapping

| API Endpoint | TypeScript | Python | Go |
|---|---|---|---|
| `GET /v1/articles/all` | `searchArticles()` | `search_articles()` | `client.All.List()` |
| `GET /v1/stories/all` | `searchStories()` | `search_stories()` | `client.Stories.List()` |
| `POST /v1/summarize` | `searchSummarizer()` | `search_summarizer()` | `client.Summarize.New()` |
| `POST /v1/vector/news/all` | `vectorSearchArticles()` | `vector_search_articles()` | `client.Vector.News.Search()` |
| `GET /v1/wikipedia/all` | `searchWikipedia()` | `search_wikipedia()` | `client.Wikipedia.Search()` |
| `POST /v1/vector/wikipedia/all` | `vectorSearchWikipedia()` | `vector_search_wikipedia()` | `client.Wikipedia.VectorSearch()` |
| `GET /v1/companies/all` | `searchCompanies()` | `search_companies()` | `client.Companies.List()` |
| `GET /v1/people/all` | `searchPeople()` | `search_people()` | `client.People.List()` |
| `GET /v1/journalists/all` | `searchJournalists()` | `search_journalists()` | `client.Journalists.List()` |
| `GET /v1/journalists/{id}` | `getJournalistById()` | `get_journalist_by_id()` | `client.Journalists.Get()` |
| `GET /v1/sources/all` | `searchSources()` | `search_sources()` | `client.Sources.List()` |
| `GET /v1/topics/all` | `searchTopics()` | `search_topics()` | `client.Topics.List()` |

## Common Patterns

### Search Articles

**TypeScript:**
```ts
const { articles } = await perigon.searchArticles({ q: "AI", size: 10, sortBy: "date" });
```

**Python:**
```python
result = api.search_articles(q="AI", size=10, sort_by="date")
```

**Go:**
```go
result, err := client.All.List(ctx, perigon.AllListParams{
    Q:      perigon.String("AI"),
    Size:   perigon.Int(10),
    SortBy: perigon.AllEndpointSortByDate,
})
```

### Vector Search

**TypeScript:**
```ts
const results = await perigon.vectorSearchArticles({
    articleSearchParams: { prompt: "impact of AI on healthcare", size: 5 },
});
```

**Python:**
```python
from perigon.models import ArticleSearchParams
results = api.vector_search_articles(
    article_search_params=ArticleSearchParams(prompt="impact of AI on healthcare", size=5)
)
```

**Go:**
```go
results, err := client.Vector.News.Search(ctx, perigon.VectorNewsSearchParams{
    Prompt: "impact of AI on healthcare",
    Size:   perigon.Int(5),
})
```

### Error Handling

**TypeScript:**
```ts
try {
    const result = await perigon.searchArticles({ q: "test" });
} catch (error) {
    if (error.status === 429) console.error("Rate limited");
}
```

**Python:**
```python
from perigon.exceptions import ApiException
try:
    result = api.search_articles(q="test")
except ApiException as e:
    print(f"HTTP {e.status}: {e.body}")
```

**Go:**
```go
result, err := client.All.List(ctx, perigon.AllListParams{Q: perigon.String("test")})
if err != nil {
    var apierr *perigon.Error
    if errors.As(err, &apierr) {
        fmt.Printf("HTTP %d\n", apierr.StatusCode)
    }
}
```

## SDK-Specific Gotchas

1. **Python `from` keyword**: Use `var_from` instead of `from` for date filtering (Python reserved word).
2. **Python POST body params**: Vector search and summarization require model objects (`ArticleSearchParams`, `SummaryBody`, `WikipediaSearchParams`).
3. **Go optional fields**: Use `perigon.String()`, `perigon.Int()`, `perigon.Float()`, `perigon.Time()` constructors for optional parameters.
4. **Go retries**: Built-in exponential backoff (2 retries by default). Override with `option.WithMaxRetries()`.
5. **TypeScript middleware**: Use `Configuration({ middleware: [...] })` for request/response hooks.

## How to Use References

Read individual reference files for detailed SDK-specific documentation:

```
references/typescript-sdk.md  — Full @goperigon/perigon-ts reference
references/python-sdk.md      — Full perigon Python SDK reference
references/go-sdk.md          — Full perigon-go-sdk/v2 reference
```

Each reference contains:
- Installation and setup instructions
- Complete method reference with all parameters
- Code examples for every endpoint
- Error handling patterns
- Advanced features (middleware, async, retries, pagination)

## External References

- [TypeScript SDK — GitHub](https://github.com/goperigon/perigon-ts)
- [Python SDK — GitHub](https://github.com/goperigon/perigon-python)
- [Go SDK — GitHub](https://github.com/goperigon/perigon-go-sdk)
- [Perigon API Documentation](https://docs.perigon.io)
- [Perigon API Reference](https://www.perigon.io/reference)
