---
name: tikhub-api-helper
description: Search and query TikHub APIs for TikTok, Douyin, Xiaohongshu, Lemon8, Instagram, YouTube, Twitter, Reddit, and more. Use when user asks about  needs to fetch data from social media platforms. Supports both English and Chinese queries.
---

# TikHub API Helper

A skill to help users search, find, and call TikHub API endpoints for social media data.

## Quick Start

When a user asks about TikHub API or wants to fetch social media data:

1. **Search for relevant APIs** using the searcher script
2. **Show the user available options** with parameters
3. **Call the API** with appropriate parameters
4. **Return formatted results** to the user

## Available Scripts

### API Searcher - `api_searcher.py`

Search and find relevant TikHub API endpoints.

```bash
# Search by keyword
python api_searcher.py "user profile"
python api_searcher.py "视频评论"
python api_searcher.py "trending"

# List all APIs for a specific tag/category
python api_searcher.py tag:TikTok-Web-API
python api_searcher.py tag:Douyin-App-V3-API

# List popular/common APIs
python api_searcher.py popular

# List all available tags/categories
python api_searcher.py tags

# Get detailed info for a specific API
python api_searcher.py detail:tiktok_web_fetch_user_profile_get
```

### API Client - `api_client.py`

Make HTTP requests to TikHub API endpoints.

```bash
# Health check (no authentication required)
python api_client.py GET /api/v1/health/check

# Get user profile
python api_client.py GET /api/v1/tiktok/web/fetch_user_profile "sec_user_id=MS4wLjABAAAA..."

# Search for videos
python api_client.py GET /api/v1/tiktok/web/fetch_search_video "keyword=gaming"

# POST request with JSON body
python api_client.py POST /api/v1/tiktok/web/generate_xgnarly '{"url": "https://..."}'
```

## Supported Platforms

| Platform | Tag Name | APIs Available |
|----------|----------|----------------|
| TikTok Web | `TikTok-Web-API` | 58 endpoints |
| TikTok App | `TikTok-App-V3-API` | 76 endpoints |
| Douyin Web | `Douyin-Web-API` | 76 endpoints |
| Douyin App | `Douyin-App-V3-API` | 45 endpoints |
| Douyin Search | `Douyin-Search-API` | 20 endpoints |
| Douyin Billboard | `Douyin-Billboard-API` | 31 endpoints |
| Xiaohongshu Web | `Xiaohongshu-Web-API` | 26 endpoints |
| Instagram | `Instagram-V2-API` | 26 endpoints |
| YouTube | `YouTube-Web-API` | 16 endpoints |
| Twitter | `Twitter-Web-API` | 13 endpoints |
| Reddit | `Reddit-APP-API` | 23 endpoints |
| Bilibili | `Bilibili-Web-API` | 24 endpoints |
| Weibo | `Weibo-Web-V2-API` | 33 endpoints |
| Zhihu | `Zhihu-Web-API` | 32 endpoints |

Use `python api_searcher.py tags` to see all categories.

## Common Use Cases

### Get User Profile

```bash
# TikTok user profile
python api_searcher.py "fetch user profile tiktok"
python api_client.py GET /api/v1/tiktok/web/fetch_user_profile "sec_user_id=USER_ID"
```

### Get Video Details

```bash
# TikTok video details
python api_searcher.py "fetch post detail"
python api_client.py GET /api/v1/tiktok/web/fetch_post_detail "post_id=POST_ID"
```

### Search Content

```bash
# Search for videos/users
python api_searcher.py "search video"
python api_client.py GET /api/v1/tiktok/web/fetch_search_video "keyword=YOUR_KEYWORD"
```

### Get Comments

```bash
# Get video comments
python api_searcher.py "fetch comment"
python api_client.py GET /api/v1/tiktok/web/fetch_post_comment "post_id=POST_ID"
```

## Authentication

API requests use a default token for development. For production use, users should:

1. Get their API token from [TikHub User](https://www.tikhub.io)
2. Set the `TIKHUB_TOKEN` environment variable
3. Or modify `DEFAULT_TOKEN` in `api_client.py`

Request format:
```json
{
  "Authorization": "Bearer YOUR_API_TOKEN"
}
```

## Base URLs

- **China users**: `https://api.tikhub.dev` (bypasses GFW)
- **International**: `https://api.tikhub.io`

The API client auto-detects the appropriate URL. To override, modify the `use_china_domain` parameter in the client.

## Rate Limits

- **QPS**: 10 requests per second per endpoint
- **Timeout**: 30-60 seconds
- **Retry**: Max 3 retries on error

## Instructions for Claude

When helping users with TikHub API:

1. **Understand the user's goal** - What data do they want? From which platform?
2. **Search for relevant APIs** - Use `api_searcher.py` with appropriate keywords
3. **Present options** - Show matching APIs with brief descriptions
4. **Guide parameters** - Check what parameters are required using `detail:OPERATION_ID`
5. **Make the request** - Use `api_client.py` with the user's parameters
6. **Format results** - Present the API response in a clear, readable format

### Example Workflow

User: "I want to get a TikTok user's profile"

```bash
# Step 1: Search for the relevant API
python api_searcher.py "tiktok user profile"

# Step 2: Show results and confirm endpoint
# Found: GET /api/v1/tiktok/web/fetch_user_profile

# Step 3: Get detailed parameter info
python api_searcher.py detail:tiktok_web_fetch_user_profile_get

# Step 4: Make the API call with user's parameters
python api_client.py GET /api/v1/tiktok/web/fetch_user_profile "sec_user_id=MS4wLjABAAAA..."

# Step 5: Format and present results
```

## Error Handling

Common errors and solutions:

| Error | Solution |
|-------|----------|
| `401 Unauthorized` | Check API token is valid |
| `429 Too Many Requests` | Rate limit exceeded, wait before retry |
| `Connection error` | Check network, try China domain if in mainland China |
| `Missing parameter` | Check API details for required parameters |

## Reference

- **Full API Documentation**: [TikHub API Docs](https://api.tikhub.io)
- **Apifox Docs**: [docs.tikhub.io](https://docs.tikhub.io)
- **API Status**: [monitor.tikhub.io](https://monitor.tikhub.io)
- **GitHub**: [github.com/TikHub](https://github.com/TikHub)
