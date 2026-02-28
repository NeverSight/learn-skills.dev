---
name: twitterapi-cli
description: Twitter data retrieval CLI tool. Use when user requests Twitter data - user profiles, follower counts, tweet searches, user timelines, follower/following lists, or Twitter user metrics. Supports field filtering for structured output. For detailed API endpoint documentation, see the original API skill at https://docs.twitterapi.io/skill.md
---

# TwitterAPI CLI

A token-efficient CLI tool for retrieving Twitter data via TwitterAPI.io. Filters API responses to reduce token usage by 70-90% compared to full responses.

## Prerequisites

- **Bun** runtime must be installed on the system
- **API Key** from TwitterAPI.io

## Setup & Build

**IMPORTANT: This CLI must be built before first use.**

```bash
# Navigate to the CLI directory
cd skills/twitterapi-cli/cli

# Install dependencies
bun install

# Build the CLI
bun run build
```

The build process creates a standalone binary at `scripts/twitterapi` (one level above the cli directory).

## Quick Start

```bash
# Get user profile (compact output)
twitterapi user info elonmusk --compact

# Get recent tweets
twitterapi user tweets elonmusk --limit 10 --compact

# Search for tweets
twitterapi tweet search "AI tools" --limit 20 --compact

# Get followers
twitterapi user followers elonmusk --limit 50

# Get following
twitterapi user following elonmusk --limit 50
```

## Command Overview

| Command | Description | Key Options |
|---------|-------------|-------------|
| `user info <username>` | User profile | `--compact`, `--fields` |
| `user tweets <username>` | User timeline | `--limit`, `--include-replies`, `--compact`, `--fields` |
| `user followers <username>` | Follower list | `--limit`, `--compact` |
| `user following <username>` | Following list | `--limit`, `--compact` |
| `tweet search <query>` | Search tweets | `--limit`, `--compact`, `--fields` |

**Full reference:** See `references/cli.md` for complete command documentation.

## Field Filtering

The CLI's core feature is field filtering - extracting only the data you need from API responses.

### Using Compact Mode

```bash
# Use preset field sets (saves 70-90% tokens)
twitterapi user info elonmusk --compact
twitterapi user tweets elonmusk --limit 10 --compact
twitterapi tweet search "AI tools" --compact
```

### Custom Fields

```bash
# Specify exact fields with dot notation
twitterapi user info elonmusk --fields "id,name,description,verified"

# Nested fields use dots
twitterapi user tweets elonmusk --fields "id,text,public_metrics.like_count,public_metrics.retweet_count"
```

**Complete guide:** See `references/fields.md` for all presets, dot notation syntax, and examples.

## Output Format

All commands return JSON to stdout for easy parsing.

**Success:**
```json
{
  "id": "123456",
  "screen_name": "elonmusk",
  "name": "Elon Musk",
  "followers_count": 150000000
}
```

**Error:**
```json
{
  "error": true,
  "type": "api_error",
  "message": "User not found",
  "status_code": 404
}
```

## Configuration

Set your API key via environment variable:

```bash
export TWITTERAPI_KEY="your-api-key-here"
```

Or create `~/.twitterapi/config.json`:

```json
{
  "api_key": "your-api-key",
  "base_url": "https://api.twitterapi.io",
  "timeout": 30
}
```

**Note:** The config file path is `~/.twitterapi/config.json` (automatically created if it doesn't exist).

## Usage Patterns

### User Profile Analysis
```bash
# Get compact profile
twitterapi user info elonmusk --compact

# Get specific metrics
twitterapi user info elonmusk --fields "id,name,followers_count,verified"
```

### Tweet Engagement Analysis
```bash
# Get tweets with engagement metrics
twitterapi user tweets elonmusk --limit 20 --compact

# Custom engagement fields
twitterapi user tweets elonmusk --limit 50 --fields "id,text,created_at,public_metrics.like_count,public_metrics.retweet_count"
```

### Follower/Following Analysis
```bash
# Get follower list (compact)
twitterapi user followers elonmusk --limit 100

# Get following list
twitterapi user following elonmusk --limit 100
```

### Content Search
```bash
# Search for specific topics
twitterapi tweet search "machine learning" --limit 50 --compact

# Search with custom fields
twitterapi tweet search "openai" --limit 20 --fields "id,text,created_at,author_id"
```

## Error Handling

The CLI exits with status code 1 on API errors and outputs structured JSON to stderr:

```json
{
  "error": true,
  "type": "api_error",
  "message": "Error description",
  "command": "user info",
  "status_code": 404
}
```

Common errors:
- `401` - Invalid API key
- `404` - User not found
- `429` - Rate limit exceeded
- `500` - API server error

## Related Documentation

- **CLI Command Reference:** `references/cli.md` - Complete command and option documentation
- **Field Filtering Guide:** `references/fields.md` - Presets, dot notation, and examples
- **API Endpoints:** https://docs.twitterapi.io/skill.md - Original API skill with detailed endpoint documentation

## Technical Notes

- **Source:** `cli/src/` - TypeScript source code
- **Build:** `cd cli && bun run build` - Creates standalone binary at `scripts/twitterapi`
- **Development Mode:** `cd cli && bun run src/cli.ts <command>` - Run directly without building
- **Production:** `./scripts/twitterapi <command>` - Use built binary
- **Re-build Required:** After any source code changes, run `bun run build` again (from cli directory)
- **Output:** JSON only (designed for agent/AI consumption)
- **Token Savings:** 70-90% reduction with field filtering
- **Rate Limits:** Handled automatically (retry after delay)

## Execution Methods

### Method 1: Using built binary (recommended for agents)
```bash
cd skills/twitterapi-cli
./scripts/twitterapi user info elonmusk --compact
```

### Method 2: Development mode (for testing changes)
```bash
cd skills/twitterapi-cli/cli
bun run src/cli.ts user info elonmusk --compact
```
