---
name: bird-fast
description: Post tweets, read threads, search X/Twitter from the terminal using bird CLI. Use when automating Twitter, posting from scripts, analyzing tweet threads, monitoring mentions, or working with the Twitter/X API without OAuth.
---

# bird CLI

A command-line interface for interacting with X/Twitter directly from the terminal, using your existing browser session for authentication.

## Overview

bird is a TypeScript-based CLI that provides terminal access to X/Twitter functionality without requiring API keys or OAuth flows. It extracts authentication cookies from your web browser (Safari, Chrome, or Firefox) and uses Twitter's internal GraphQL API with automatic query ID management.

**Key Features:**
- Zero-configuration authentication via browser cookies
- Full tweet lifecycle: post, reply, read, search
- Media uploads (images, GIFs, videos) with alt text
- Multiple output formats (human-readable, JSON, plain)
- Automatic GraphQL query ID refresh and REST API fallback

## When to Use

- Posting tweets or replies from scripts or automation
- Reading and analyzing tweet threads programmatically
- Searching for mentions or specific content
- Building social media automation workflows
- Testing Twitter integrations from the command line
- Extracting tweet content for analysis

## Prerequisites

- **Node.js >= 22** (for npm/pnpm/bun installation) OR Homebrew (for standalone binary)
- **Browser login**: Must be logged into x.com in Safari, Chrome, or Firefox

## Installation

```bash
# npm
npm install -g @steipete/bird

# pnpm
pnpm add -g @steipete/bird

# bun
bun add -g @steipete/bird

# Homebrew (macOS - standalone binary, no Node.js required)
brew install steipete/tap/bird
```

One-shot execution without installation:
```bash
bunx @steipete/bird whoami
npx @steipete/bird whoami
```

## Authentication

bird resolves credentials using a three-tier priority chain:

| Priority | Source | Configuration |
|----------|--------|---------------|
| 1 (highest) | CLI flags | `--auth-token`, `--ct0` |
| 2 | Environment variables | `AUTH_TOKEN`, `CT0` (or `TWITTER_AUTH_TOKEN`, `TWITTER_CT0`) |
| 3 (lowest) | Browser cookies | Auto-extracted from Safari, Chrome, or Firefox |

**Browser cookie extraction** (default behavior):
- Requires being logged into x.com in your browser
- Default order: Safari → Chrome → Firefox
- Customize with `--cookie-source` flag or config file

**Verify authentication:**
```bash
bird whoami    # Shows authenticated user
bird check     # Shows credential source
```

## Quick Start

```bash
# Post a tweet
bird tweet "Hello from the terminal!"

# Read a tweet
bird read https://x.com/user/status/1234567890123456789

# Reply to a tweet
bird reply 1234567890123456789 "Great point!"

# Search tweets
bird search "from:elonmusk" -n 20

# View your mentions
bird mentions
```

## Command Reference

### Writing Commands

#### tweet
Post a new tweet with optional media attachments.

```bash
bird tweet "<text>" [options]
```

**Options:**
- `--media <path>` - Attach media file (repeatable, up to 4 images/GIFs or 1 video)
- `--alt <text>` - Alt text for corresponding `--media` (repeatable)

**Examples:**
```bash
bird tweet "Check this out!"
bird tweet "Photo gallery" --media img1.jpg --alt "First photo" --media img2.jpg
bird tweet "Demo video" --media demo.mp4
```

#### reply
Reply to an existing tweet.

```bash
bird reply <tweet-id-or-url> "<text>" [options]
```

**Examples:**
```bash
bird reply 1234567890123456789 "I agree!"
bird reply https://x.com/user/status/1234567890123456789 "Great thread!"
bird reply 1234567890123456789 "Here's a screenshot" --media screenshot.png --alt "Screenshot"
```

### Reading Commands

#### read
Fetch a single tweet's content. Handles standard tweets, Notes (long-form), and Articles.

```bash
bird read <tweet-id-or-url>

# Shorthand: just provide the ID or URL
bird 1234567890123456789
bird https://x.com/user/status/1234567890123456789
```

#### replies
List all replies to a tweet.

```bash
bird replies <tweet-id-or-url>
```

#### thread
Show a full conversation thread.

```bash
bird thread <tweet-id-or-url>
```

### Search Commands

#### search
Search for tweets matching a query.

```bash
bird search "<query>" [-n <count>]
```

**Options:**
- `-n, --count <number>` - Number of results (default: 10)

**Examples:**
```bash
bird search "claude ai" -n 20
bird search "from:anthropic"
bird search "@username"
```

#### mentions
Find mentions of a user.

```bash
bird mentions [-u <handle>] [-n <count>]
```

**Options:**
- `-u, --user <handle>` - User handle (defaults to authenticated user)
- `-n, --count <number>` - Number of results (default: 10)

#### bookmarks
List bookmarked tweets.

```bash
bird bookmarks [-n <count>]
```

**Options:**
- `-n, --count <number>` - Number of results (default: 20)

### Utility Commands

#### whoami
Display authenticated user information.

```bash
bird whoami
```

#### check
Verify credential availability and show their source.

```bash
bird check
```

#### query-ids
Inspect or refresh the GraphQL query ID cache.

```bash
bird query-ids [--fresh] [--json]
```

**Options:**
- `--fresh` - Force refresh by scraping X.com web client bundles
- `--json` - Output as JSON

#### help
Show help for a command.

```bash
bird help [command]
```

## Global Options

| Option | Description |
|--------|-------------|
| `--auth-token <token>` | Twitter auth_token cookie |
| `--ct0 <token>` | Twitter ct0 cookie |
| `--cookie-source <source>` | Browser priority (repeatable: `safari`, `chrome`, `firefox`) |
| `--chrome-profile <name>` | Chrome profile name |
| `--firefox-profile <name>` | Firefox profile name |
| `--timeout <ms>` | Request timeout in milliseconds |
| `--plain` | Stable output: disables emoji and color |
| `--no-emoji` | Disable emoji in output |
| `--no-color` | Disable ANSI colors |
| `--json` | Output as JSON (command-specific) |

## Media Attachments

### Supported Formats

| Type | Extensions | Limit |
|------|------------|-------|
| Images | `.jpg`, `.jpeg`, `.png`, `.webp` | Up to 4 |
| GIFs | `.gif` | Up to 4 |
| Videos | `.mp4`, `.m4v`, `.mov` | 1 only |

**Note:** Cannot mix videos with images/GIFs.

### Alt Text

Specify alt text for accessibility:
```bash
bird tweet "Three photos" \
  --media photo1.jpg --alt "Beach sunset" \
  --media photo2.jpg --alt "Mountain view" \
  --media photo3.jpg --alt "City skyline"
```

## Output Formats

| Format | Flag | Use Case |
|--------|------|----------|
| Human-readable | (default) | Interactive terminal use |
| Plain | `--plain` | Scripting (no emoji/color) |
| JSON | `--json` | Programmatic parsing |

**Example:**
```bash
# Parse tweet data in a script
bird read 1234567890123456789 --json | jq '.text'
```

## Configuration Files

Optional JSON5 configuration files:

| Location | Scope |
|----------|-------|
| `~/.config/bird/config.json5` | Global (all projects) |
| `./.birdrc.json5` | Project-specific |

**Example config:**
```json5
{
  cookieSource: ["firefox", "safari"],
  firefoxProfile: "default-release",
  timeoutMs: 20000
}
```

## Examples

### Automation Workflow

```bash
#!/bin/bash
# Post a daily update
DATE=$(date +"%Y-%m-%d")
bird tweet "Daily standup for $DATE: All systems operational."
```

### Thread Analysis

```bash
# Get all replies to a viral tweet
bird replies https://x.com/user/status/1234567890123456789 --json | \
  jq '.[] | .text'
```

### Mention Monitoring

```bash
# Check recent mentions
bird mentions -n 50 --json | jq '.[] | {user: .user.screen_name, text: .text}'
```

### Multi-Image Post

```bash
bird tweet "Product launch gallery" \
  --media hero.png --alt "Product hero shot" \
  --media feature1.png --alt "Feature overview" \
  --media feature2.png --alt "Technical specs" \
  --media pricing.png --alt "Pricing table"
```

## Best Practices

- **Use `--json` for scripting**: Always use `--json` output when parsing results programmatically
- **Use `--plain` in CI/CD**: Avoids emoji/color issues in log files
- **Refresh query IDs proactively**: Run `bird query-ids --fresh` if you haven't used bird in a while
- **Set up environment variables for automation**: Use `AUTH_TOKEN` and `CT0` env vars instead of browser cookies for scripts
- **Add alt text for accessibility**: Always include `--alt` when attaching images
- **Check auth first**: Run `bird whoami` before complex operations to verify credentials
- **Handle rate limits**: Twitter may throttle requests; add delays in automation scripts

## Troubleshooting

### "No auth token found"
- Ensure you're logged into x.com in Safari, Chrome, or Firefox
- Try specifying the browser: `bird whoami --cookie-source safari`
- Use environment variables: `export AUTH_TOKEN=... CT0=...`

### GraphQL 404 errors
Query IDs may be stale. Refresh the cache:
```bash
bird query-ids --fresh
```

### Error 226 (automation detected)
bird automatically falls back to the REST API. If it persists, wait a few minutes and retry.

### Wrong account detected
Multiple browser profiles may have different sessions:
```bash
bird whoami --cookie-source chrome --chrome-profile "Profile 1"
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Runtime error (network, auth, API) |
| 2 | Invalid usage (unknown command, bad arguments) |

## Technical Notes

- Uses Twitter's private GraphQL API endpoints
- Query IDs are cached locally (`~/.config/bird/query-ids-cache.json`) with 24-hour TTL
- Automatic query ID refresh on 404 errors
- REST API fallback (`statuses/update.json`) for error 226
- Subject to breakage if Twitter changes their internal API

## Resources

- [bird.fast](https://bird.fast) - Official website
- [GitHub Repository](https://github.com/steipete/bird) - Source code and issues
- [Changelog](https://github.com/steipete/bird/blob/main/CHANGELOG.md) - Version history
