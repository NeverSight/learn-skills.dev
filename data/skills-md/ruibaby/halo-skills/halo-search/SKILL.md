---
name: halo-search
description: Search post content on websites built with Halo CMS using public API. Use when the user provides a Halo site URL and wants to search, query, or find posts or content on that site.
---

# Halo CMS Post Search

Search posts on any Halo-powered website via its public REST API (no authentication required).

## Workflow

1. Extract the base URL from the user (e.g., `https://example.com`)
2. Ask for the search keyword if not provided
3. Call the search API using `curl` via the Shell tool
4. Parse the JSON response and present results to the user

## Search API

**Endpoint**: `POST {baseUrl}/apis/api.halo.run/v1alpha1/indices/-/search`

**Request Body** (JSON):

```json
{
  "keyword": "search term",
  "limit": 10,
  "highlightPreTag": "<B>",
  "highlightPostTag": "</B>"
}
```

### Request Fields

| Field                | Type     | Required | Default | Description              |
| -------------------- | -------- | -------- | ------- | ------------------------ |
| keyword              | string   | Yes      | -       | Search keyword           |
| limit                | int      | No       | 10      | Result limit (1-1000)    |
| highlightPreTag      | string   | No       | `<B>`   | Highlight open tag       |
| highlightPostTag     | string   | No       | `</B>`  | Highlight close tag      |
| includeTypes         | string[] | No       | all     | Filter by type           |
| includeTagNames      | string[] | No       | all     | Filter by tag names      |
| includeCategoryNames | string[] | No       | all     | Filter by category names |
| includeOwnerNames    | string[] | No       | all     | Filter by owner names    |

### Response Structure

```json
{
  "hits": [
    {
      "id": "...",
      "metadataName": "post-abc",
      "title": "Post Title with <B>keyword</B> highlighted",
      "description": "Post description...",
      "content": "Plain text content...",
      "categories": ["category-name"],
      "tags": ["tag-name"],
      "ownerName": "author-name",
      "permalink": "/archives/post-slug",
      "type": "post.content.halo.run",
      "creationTimestamp": "2025-01-01T00:00:00Z",
      "updateTimestamp": "2025-01-15T00:00:00Z"
    }
  ],
  "keyword": "search term",
  "total": 5,
  "limit": 10,
  "processingTimeMillis": 42
}
```

## Example curl Command

```bash
curl -s -X POST '{baseUrl}/apis/api.halo.run/v1alpha1/indices/-/search' \
  -H 'Content-Type: application/json' \
  -d '{"keyword":"your keyword","limit":10,"highlightPreTag":"**","highlightPostTag":"**"}' | python3 -m json.tool
```

Use `highlightPreTag` / `highlightPostTag` set to `**` for markdown-friendly bold highlighting in output.

## Post Detail API

When the user wants to read the full content of a search result, fetch the post detail.

**Endpoint**: `GET {baseUrl}/apis/api.content.halo.run/v1alpha1/posts/{name}`

The `{name}` is the `metadataName` field from a search hit.

```bash
curl -s '{baseUrl}/apis/api.content.halo.run/v1alpha1/posts/{metadataName}' | python3 -m json.tool
```

### Key Response Fields

| Path                            | Description                            |
| ------------------------------- | -------------------------------------- |
| `spec.title`                    | Post title                             |
| `spec.slug`                     | URL slug                               |
| `spec.cover`                    | Cover image URL                        |
| `spec.publishTime`              | Publish time                           |
| `spec.pinned`                   | Whether pinned                         |
| `spec.visible`                  | Visibility (PUBLIC, PRIVATE, etc.)     |
| `spec.excerpt.raw`              | Manual excerpt                         |
| `status.excerpt`                | Auto-generated excerpt                 |
| `status.permalink`              | Post permalink                         |
| `content.content`               | Full rendered HTML content             |
| `content.raw`                   | Raw content (usually Markdown or HTML) |
| `owner.displayName`             | Author display name                    |
| `stats.visit`                   | Visit count                            |
| `stats.comment`                 | Comment count                          |
| `stats.upvote`                  | Upvote count                           |
| `categories[].spec.displayName` | Category display name                  |
| `tags[].spec.displayName`       | Tag display name                       |
| `tags[].spec.color`             | Tag color                              |
| `contributors[].displayName`    | Contributor display name               |

### Presenting Post Detail

Display:

1. **Title** (`spec.title`) with full URL (`{baseUrl}` + `status.permalink`)
2. **Author** (`owner.displayName`)
3. **Date** (`spec.publishTime`)
4. **Categories / Tags** (from `categories[].spec.displayName` and `tags[].spec.displayName`)
5. **Content** — prefer `content.raw` for readable text; use `content.content` (rendered HTML) as fallback
6. **Stats** (visits, comments, upvotes) if relevant

## Presenting Search Results

For each hit, display:

1. **Title** (with permalink as full URL: `{baseUrl}{permalink}`)
2. **Description** or a snippet of content
3. **Tags / Categories** if present
4. **Date** (creationTimestamp)

If the user wants the full post, call the Post Detail API using `metadataName`.

If `total` is 0, inform the user that no results were found.

If the request fails with a connection error, verify the URL is correct and the site is accessible. If it returns a search engine error, the site may not have a search plugin enabled.
