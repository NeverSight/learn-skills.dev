---
name: bird-cli
description: Use this skill when the user wants to interact with X/Twitter via command line. Triggers include requests to tweet, reply to tweets, read tweets or threads, search X/Twitter, check mentions, view bookmarks, get trending topics, manage lists, or any other X/Twitter operations via CLI. Also use when the user mentions the Bird CLI tool specifically or wants to automate X/Twitter interactions from the terminal. Do NOT use for web-based Twitter interactions or Twitter API integrations.
---

# Bird CLI - Fast X/Twitter Command Line Interface

## Overview

Bird is a fast CLI for X/Twitter that uses your existing browser session (cookie authentication) and X's internal GraphQL API. It enables tweeting, replying, reading threads, searching, and more from the terminal.

**CRITICAL WARNINGS:**
- Bird uses X/Twitter's **undocumented** GraphQL API - expect breakage without notice
- **DO NOT use for automated tweeting** - you will hit blocks very quickly
- Bots are not welcome on X/Twitter
- Primary use case: **reading tweets**, not creating them
- For tweet creation, use browser automation or pay for the Twitter API

## Installation

### npm / pnpm / bun
```bash
npm install -g @steipete/bird
# or
pnpm add -g @steipete/bird
# or
bun add -g @steipete/bird
```

### One-shot (no install)
```bash
bunx @steipete/bird whoami
```

### Homebrew (macOS)
```bash
brew install steipete/tap/bird
```

**Requirements:** Node ≥ 20

## Quick Start

```bash
# Verify installation and show logged-in account
bird whoami

# Get help for any command
bird help
bird help [command]

# Read a tweet
bird read https://x.com/user/status/1234567890123456789
bird 1234567890123456789 --json

# View a thread
bird thread https://x.com/user/status/1234567890123456789

# Search
bird search "from:username" -n 5

# Check mentions
bird mentions -n 5
```

## Authentication

Bird uses **cookie authentication** from your browser - no password required.

### Credential Resolution Order
1. **CLI flags**: `--auth-token`, `--ct0`
2. **Environment variables**: `AUTH_TOKEN`, `CT0` (or `TWITTER_AUTH_TOKEN`, `TWITTER_CT0`)
3. **Browser cookies**: Safari/Chrome/Firefox (via `@steipete/sweet-cookie`)

### Browser Cookie Sources
- **Safari**: `~/Library/Cookies/Cookies.binarycookies`
- **Chrome**: `~/Library/Application Support/Google/Chrome/<Profile>/Cookies`
- **Firefox**: `~/Library/Application Support/Firefox/Profiles/<profile>/cookies.sqlite`

### Override Cookie Source
```bash
# Specify browser order
bird --cookie-source safari whoami
bird --cookie-source firefox --cookie-source chrome whoami

# Chrome profile selection
bird --chrome-profile "Profile 2" whoami
bird --chrome-profile-dir "/path/to/profile" whoami

# Firefox profile selection
bird --firefox-profile "default-release" whoami
```

### Manual Cookie Setup
```bash
# Via CLI flags
bird --auth-token "your-token" --ct0 "your-ct0" whoami

# Via environment variables
export AUTH_TOKEN="your-token"
export CT0="your-ct0"
bird whoami
```

### Verify Credentials
```bash
bird check  # Shows available credentials and their source
```

## Core Commands

### Reading Tweets

#### Read Single Tweet
```bash
bird read <tweet-id-or-url> [--json]
bird <tweet-id-or-url> [--json]  # Shorthand

# Examples
bird read https://x.com/user/status/1234567890123456789
bird 1234567890123456789 --json
```

**Returns:** Full text including Notes and Articles when present

#### View Thread
```bash
bird thread <tweet-id-or-url> [options]

# Options
--all                  # Fetch all replies (no limit)
--max-pages n          # Maximum pages to fetch
--cursor string        # Start from specific cursor
--delay ms            # Delay between requests
--json                # Output as JSON

# Examples
bird thread https://x.com/user/status/1234567890123456789
bird thread 1234567890123456789 --max-pages 3 --json
```

#### View Replies
```bash
bird replies <tweet-id-or-url> [options]

# Same options as thread
bird replies 1234567890123456789 --all
bird replies 1234567890123456789 --max-pages 3 --json
```

### Searching

```bash
bird search "<query>" [options]

# Options
-n count              # Number of results
--all                 # Fetch all results
--max-pages n         # Maximum pages (requires --all or --cursor)
--cursor string       # Start from specific cursor
--json               # Output as JSON

# Examples
bird search "from:steipete" -n 5
bird search "AI agents" --all --max-pages 10 --json
```

### Mentions

```bash
bird mentions [options]

# Options
-n count              # Number of results
--user @handle        # Check mentions for specific user
--json               # Output as JSON

# Examples
bird mentions -n 5
bird mentions --user @steipete -n 10 --json
```

### Home Timeline

```bash
bird home [options]

# Options
-n count              # Number of tweets
--following           # Show Following feed (default: For You)
--json               # Output as JSON
--json-full          # Include full API response

# Examples
bird home -n 20
bird home --following -n 10 --json
```

### User Tweets

```bash
bird user-tweets <@handle> [options]

# Options
-n count              # Number of tweets
--cursor string       # Start from specific cursor
--max-pages n         # Maximum pages
--delay ms           # Delay between requests
--json               # Output as JSON

# Examples
bird user-tweets @steipete -n 20
bird user-tweets @steipete -n 50 --json
```

### User Information

```bash
bird about <@handle> [--json]

# Returns account information:
# - Account location (country/region)
# - Account creation details
# - Location accuracy
# - Data source

# Examples
bird about @steipete
bird about @username --json
```

## Bookmarks

### List Bookmarks
```bash
bird bookmarks [options]

# Basic Options
-n count                        # Number of bookmarks
--folder-id id                 # Specific bookmark folder
--all                          # Fetch all bookmarks
--max-pages n                  # Max pages (requires --all or --cursor)
--cursor string                # Start from cursor
--json                         # Output as JSON

# Thread Expansion Options
--expand-root-only             # Expand only root tweet threads
--author-chain                 # Keep author's self-reply chain
--author-only                  # All tweets from bookmarked author
--full-chain-only             # Entire reply chain (all authors)
--include-ancestor-branches    # Include sibling branches (with --full-chain-only)
--include-parent              # Include direct parent tweet
--thread-meta                 # Add thread metadata to each tweet

# Display Options
--sort-chronological          # Sort oldest to newest

# Examples
bird bookmarks -n 5
bird bookmarks --folder-id 123456789123456789 -n 5
bird bookmarks --all --json
bird bookmarks --include-parent --author-chain --json
```

### Remove Bookmarks
```bash
bird unbookmark <tweet-id-or-url...>

# Examples
bird unbookmark 1234567890123456789
bird unbookmark https://x.com/user/status/1234567890123456789
bird unbookmark 123456 789012 345678  # Multiple bookmarks
```

## Likes

```bash
bird likes [options]

# Options
-n count              # Number of likes
--all                # Fetch all likes
--max-pages n        # Max pages (requires --all or --cursor)
--cursor string      # Start from cursor
--json              # Output as JSON
--json-full         # Include full API response

# Examples
bird likes -n 5
bird likes --all --max-pages 2 --json
```

## News & Trending

```bash
bird news [options]
bird trending [options]  # Alias

# Options
-n count                # Number of news items
--ai-only              # Only AI-curated content (filters regular trends)
--with-tweets          # Include related tweets for each item
--tweets-per-item n    # Tweets per news item (with --with-tweets)

# Tab Filters (can combine multiple)
--for-you              # For You tab only
--news-only            # News tab only
--sports               # Sports tab only
--entertainment        # Entertainment tab only
--trending-only        # Trending tab only

--json                # Output as JSON
--json-full          # Include raw API response

# Examples
bird news -n 10
bird news --ai-only -n 20
bird news --sports --entertainment -n 15
bird news --with-tweets --tweets-per-item 3 -n 10
bird news --news-only --ai-only --json
```

**Default behavior:** Fetches from For You, News, Sports, and Entertainment tabs (Trending excluded). Headlines are auto-deduplicated.

## Lists

### View Your Lists
```bash
bird lists [options]

# Options
--member-of          # Show lists you're a member of (not owned)
-n count            # Number of lists
--json             # Output as JSON

# Examples
bird lists
bird lists --member-of -n 10 --json
```

### View List Timeline
```bash
bird list-timeline <list-id-or-url> [options]

# Options
-n count              # Number of tweets
--all                # Fetch all tweets
--max-pages n        # Max pages (implies --all)
--cursor string      # Start from cursor
--json              # Output as JSON

# Examples
bird list-timeline 1234567890 -n 20
bird list-timeline https://x.com/i/lists/1234567890 --all --json
bird list-timeline 1234567890 --max-pages 3 --json
```

## Following & Followers

### Following (Who You Follow)
```bash
bird following [options]

# Options
--user <userId>       # Check who another user follows (by user ID)
-n count             # Number of users
--cursor string      # Start from cursor
--all               # Fetch all
--max-pages n       # Max pages (requires --all)
--json             # Output as JSON

# Examples
bird following -n 20
bird following --user 12345678 -n 10
bird following --all --max-pages 5 --json
```

### Followers (Who Follows You)
```bash
bird followers [options]

# Options
--user <userId>       # Check another user's followers (by user ID)
-n count             # Number of users
--cursor string      # Start from cursor
--all               # Fetch all
--max-pages n       # Max pages (requires --all)
--json             # Output as JSON

# Examples
bird followers -n 20
bird followers --user 12345678 -n 10
bird followers --all --json
```

## Posting (Use Sparingly!)

### Tweet
```bash
bird tweet "<text>" [options]

# Options
--media <path>        # Attach media (repeatable, max 4 images or 1 video)
--alt <text>         # Alt text for corresponding media (repeatable)
--plain             # No emoji, no color output

# Examples
bird tweet "Hello from Bird!"
bird tweet "Check this out" --media image.png --alt "Screenshot"
bird tweet "Multiple images" --media img1.jpg --media img2.jpg --alt "First" --alt "Second"
```

**Supported media:** jpg, jpeg, png, webp, gif, mp4, mov
**Limits:** Up to 4 images/GIFs OR 1 video (no mixing)

### Reply
```bash
bird reply <tweet-id-or-url> "<text>" [options]

# Same media options as tweet
bird reply 1234567890123456789 "Great point!"
bird reply https://x.com/user/status/123456 "Thanks!" --media response.png
```

**Fallback behavior:** If GraphQL returns error 226 (automated request), Bird falls back to legacy `statuses/update.json` endpoint.

## Configuration

### Config File Locations
Config precedence: CLI flags > env vars > project config > global config

- **Global:** `~/.config/bird/config.json5`
- **Project:** `./.birdrc.json5`

### Example Config (`~/.config/bird/config.json5`)
```json5
{
  // Cookie source order for browser extraction
  cookieSource: ["firefox", "safari"],
  
  // Browser-specific settings
  chromeProfileDir: "/path/to/Chromium/Profile",
  firefoxProfile: "default-release",
  
  // Timeouts (milliseconds)
  cookieTimeoutMs: 30000,
  timeoutMs: 20000,
  
  // Quote depth in JSON output
  quoteDepth: 1
}
```

### Environment Variables
```bash
# Authentication
export AUTH_TOKEN="your-token"
export CT0="your-ct0"

# Shortcuts
export BIRD_TIMEOUT_MS=20000
export BIRD_COOKIE_TIMEOUT_MS=30000
export BIRD_QUOTE_DEPTH=1
```

## Global Options

Available for all commands:

```bash
# Authentication
--auth-token <token>              # Set auth_token cookie manually
--ct0 <token>                     # Set ct0 cookie manually

# Cookie Sources
--cookie-source <browser>         # Browser cookie source (repeatable)
--chrome-profile <name>           # Chrome profile name (e.g., "Default", "Profile 2")
--chrome-profile-dir <path>       # Chrome profile directory or cookie DB path
--firefox-profile <name>          # Firefox profile name

# Timeouts
--cookie-timeout <ms>             # Cookie extraction timeout
--timeout <ms>                    # Request timeout

# Output Control
--quote-depth <n>                 # Max quoted tweet depth in JSON (default: 1)
--plain                          # Stable output (no emoji, no color)
--no-emoji                       # Disable emoji
--no-color                       # Disable ANSI colors (or set NO_COLOR=1)
--json                           # JSON output
--json-full                      # Full JSON with raw API response
```

## JSON Output Format

### Tweet Objects
```json
{
  "id": "1234567890",
  "text": "Full tweet text",
  "author": {
    "username": "handle",
    "name": "Display Name"
  },
  "authorId": "98765432",
  "createdAt": "2026-01-15T10:30:00.000Z",
  "replyCount": 5,
  "retweetCount": 10,
  "likeCount": 25,
  "conversationId": "1234567890",
  "inReplyToStatusId": "9876543210",  // If reply
  "quotedTweet": { /* same schema */ }  // Depth controlled by --quote-depth
}
```

### User Objects (following/followers)
```json
{
  "id": "12345678",
  "username": "handle",
  "name": "Display Name",
  "description": "User bio",
  "followersCount": 1000,
  "followingCount": 500,
  "isBlueVerified": true,
  "profileImageUrl": "https://...",
  "createdAt": "2015-03-20T12:00:00.000Z"
}
```

### News Objects
```json
{
  "id": "unique-id",
  "headline": "News headline or trend title",
  "category": "AI · Technology",
  "timeAgo": "2h ago",
  "postCount": 1500,
  "description": "Item description",
  "url": "https://...",
  "tweets": [ /* array of tweet objects */ ],  // With --with-tweets
  "_raw": { /* raw API response */ }  // With --json-full
}
```

### Paginated Responses
When using `--json` with pagination (`--all`, `--cursor`, `--max-pages`):
```json
{
  "tweets": [ /* tweet objects */ ],
  "nextCursor": "cursor-string"  // For continuing pagination
}
```

## Query IDs (GraphQL)

X rotates GraphQL "query IDs" frequently. Bird handles this automatically.

### Runtime Cache
- **Default path:** `~/.config/bird/query-ids-cache.json`
- **Override:** `BIRD_QUERY_IDS_CACHE=/path/to/file.json`
- **TTL:** 24 hours (stale cache is still used but marked "not fresh")

### Auto-Recovery
- On GraphQL 404 (invalid query ID), Bird forces refresh and retries
- For `TweetDetail`/`SearchTimeline`, rotates through known fallback IDs

### Manual Refresh
```bash
bird query-ids --fresh           # Refresh query IDs cache
bird query-ids --fresh --json    # JSON output
```

## Library Usage

Bird can be used as a library in Node.js/TypeScript:

```javascript
import { TwitterClient, resolveCredentials } from '@steipete/bird';

// Setup client
const { cookies } = await resolveCredentials({ cookieSource: 'safari' });
const client = new TwitterClient({ cookies });

// Search for tweets
const searchResult = await client.search('from:steipete', 50);

// Get news and trending topics
const newsResult = await client.getNews(10, { aiOnly: true });

// Get news from specific tabs with tweets
const sportsNews = await client.getNews(10, {
  aiOnly: true,
  withTweets: true,
  tabs: ['sports', 'entertainment']
});

// Get user account details
const aboutResult = await client.getUserAboutAccount('steipete');
if (aboutResult.success && aboutResult.aboutProfile) {
  console.log(aboutResult.aboutProfile.accountBasedIn);
  console.log(aboutResult.aboutProfile.createdCountryAccurate);
}
```

## Exit Codes

- **0:** Success
- **1:** Runtime error (network, authentication, etc.)
- **2:** Invalid usage/validation error

## Rate Limiting

- GraphQL uses internal X endpoints - can be rate limited (429)
- Write operations hit blocks very quickly
- Use read operations primarily
- For heavy automation, consider Twitter API

## Common Workflows

### Research a Topic
```bash
# Search for recent tweets
bird search "topic keyword" -n 20 --json > results.json

# View trending topics
bird news --news-only -n 10

# Check what people are saying
bird search "from:expert_handle topic" -n 10
```

### Monitor Account Activity
```bash
# Check your mentions
bird mentions -n 20

# See your latest likes
bird likes -n 10

# Review bookmarked threads
bird bookmarks --author-chain -n 5
```

### Analyze Threads
```bash
# Read full conversation
bird thread <tweet-url> --all --json > thread.json

# Get just replies
bird replies <tweet-url> --max-pages 5 --json
```

### Export Data
```bash
# Export all bookmarks
bird bookmarks --all --json > bookmarks.json

# Export liked tweets
bird likes --all --json > likes.json

# Export user timeline
bird user-tweets @handle -n 100 --json > timeline.json
```

## Troubleshooting

### Authentication Issues
```bash
# Check available credentials
bird check

# Try specific browser
bird --cookie-source firefox whoami

# Use manual tokens
bird --auth-token "token" --ct0 "ct0-value" whoami
```

### Query ID Errors
```bash
# Refresh query IDs
bird query-ids --fresh

# If still failing, wait for upstream updates
# (X may have changed their GraphQL schema)
```

### Rate Limiting
- Reduce request frequency
- Add delays between requests (`--delay ms`)
- Avoid automated posting (high-risk activity)

### Media Upload Failures
- Check file format (jpg, jpeg, png, webp, gif, mp4, mov)
- Verify file size limits
- Don't mix images and video
- Max 4 images or 1 video per tweet

## Best Practices

1. **Use for reading, not posting** - Bird excels at data retrieval
2. **Cache results locally** - Use `--json` and save to files
3. **Respect rate limits** - Add delays, don't spam requests
4. **Verify credentials** - Run `bird check` before automation
5. **Keep query IDs fresh** - Run `bird query-ids --fresh` periodically
6. **Use configuration files** - Set defaults in `~/.config/bird/config.json5`
7. **Handle errors gracefully** - Check exit codes, expect API changes

## Version Information

```bash
bird --version
# Output: 0.3.0 (3df7969b)  # version + git sha
```

## Resources

- **Homepage:** https://bird.fast
- **npm Package:** https://www.npmjs.com/package/@steipete/bird
- **GitHub:** https://github.com/steipete/bird
- **Issues:** https://github.com/steipete/bird/issues
- **License:** MIT

## Development

If helping a user develop or contribute to Bird:

```bash
# Clone and setup
cd ~/Projects/bird
pnpm install

# Build
pnpm run build          # dist/ + bun binary
pnpm run build:dist     # dist/ only
pnpm run build:binary   # binary only

# Development
pnpm run dev tweet "Test"
pnpm run dev -- --plain check

# Test and lint
pnpm test
pnpm run lint

# Update GraphQL query IDs baseline
pnpm run graphql:update
```

## Important Reminders

1. **This uses undocumented APIs** - expect breaking changes
2. **Automated posting will get you blocked** - use sparingly
3. **Primary use case is reading** - search, threads, bookmarks, etc.
4. **Always authenticate via browser cookies** - simplest approach
5. **Check `bird check` before troubleshooting** - verifies credentials
6. **Query IDs rotate** - refresh when seeing 404 errors
7. **Be a good citizen** - respect X's terms and rate limits
