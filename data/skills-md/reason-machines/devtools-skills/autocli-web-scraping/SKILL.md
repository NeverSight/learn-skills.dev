---
name: autocli-web-scraping
description: Blazing fast Rust CLI tool to fetch data from 55+ websites (Twitter, Reddit, YouTube, Bilibili, etc.) with single commands
triggers:
  - fetch twitter trending topics
  - scrape reddit posts from subreddit
  - get bilibili hot videos
  - search xiaohongshu content
  - download youtube video transcript
  - extract data from any website
  - use autocli to get social media data
  - generate web scraper adapter with AI
---

# AutoCLI Web Scraping Skill

> Skill by [ara.so](https://ara.so) — Devtools Skills collection.

AutoCLI is a blazing fast, memory-safe command-line tool written in Rust that fetches information from 55+ websites with a single command. It covers Twitter/X, Reddit, YouTube, HackerNews, Bilibili, Zhihu, Xiaohongshu, and more, with support for browser session reuse, AI-powered adapter generation, and multi-format output.

**Key Features:**
- 55 sites, 333 commands built-in
- Browser session reuse (no token management needed)
- AI-powered adapter generation via autocli.ai
- Declarative YAML pipeline for custom adapters
- Single 4.7MB binary, zero runtime dependencies
- Up to 12x faster and 10x less memory than Node.js alternatives

## Installation

### One-line Install (macOS / Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/nashsu/autocli/main/scripts/install.sh | sh
```

### Manual Installation

Download the appropriate binary from [GitHub Releases](https://github.com/nashsu/autocli/releases/latest):

- macOS (Apple Silicon): `autocli-aarch64-apple-darwin.tar.gz`
- macOS (Intel): `autocli-x86_64-apple-darwin.tar.gz`
- Linux (x86_64): `autocli-x86_64-unknown-linux-musl.tar.gz`
- Windows (x64): `autocli-x86_64-pc-windows-msvc.zip`

Extract and place in your PATH:

```bash
tar -xzf autocli-*.tar.gz
sudo mv autocli /usr/local/bin/
```

### Chrome Extension (Required for Browser Commands)

1. Download `autocli-chrome-extension.zip` from releases
2. Extract to any directory
3. Open `chrome://extensions`
4. Enable "Developer mode"
5. Click "Load unpacked" and select the extracted folder

Public API commands (hackernews, devto, etc.) work without the extension.

## Basic Usage

### Discovery Commands

```bash
# List all available commands
autocli --help

# List commands for specific site
autocli twitter --help
autocli bilibili --help

# Run diagnostics
autocli doctor

# List all sites and their command counts
autocli list
```

### Public API Commands (No Browser Required)

```bash
# Hacker News top stories
autocli hackernews top --limit 10

# Hacker News search
autocli hackernews search "rust" --limit 5

# Dev.to top articles
autocli devto top --limit 10

# Lobsters hot stories
autocli lobsters hot --limit 10

# Stack Overflow hot questions
autocli stackoverflow hot --limit 10

# arXiv paper search
autocli arxiv search "machine learning" --limit 5

# Wikipedia search
autocli wikipedia search "rust programming"

# Linux.do forum hot topics
autocli linux-do hot --limit 10
```

### Browser-Based Commands (Requires Extension + Login)

```bash
# Twitter trending topics
autocli twitter trending

# Twitter search
autocli twitter search "rust lang" --limit 10

# Twitter timeline
autocli twitter timeline --limit 20

# Reddit frontpage
autocli reddit frontpage --limit 10

# Reddit subreddit posts
autocli reddit subreddit rust --limit 15

# Bilibili hot videos
autocli bilibili hot --limit 20

# Bilibili search
autocli bilibili search "rust programming" --limit 10

# Xiaohongshu search
autocli xiaohongshu search "travel" --limit 10

# Zhihu hot topics
autocli zhihu hot --limit 10

# YouTube search
autocli youtube search "rust tutorial" --limit 5

# Weibo hot topics
autocli weibo hot --limit 10
```

## Output Formats

AutoCLI supports multiple output formats for easy integration with other tools:

```bash
# Table format (default)
autocli hackernews top --limit 5

# JSON output
autocli hackernews top --limit 5 --format json

# YAML output
autocli hackernews top --limit 5 --format yaml

# CSV output
autocli hackernews top --limit 5 --format csv

# Markdown output
autocli hackernews top --limit 5 --format markdown
```

### JSON Processing with jq

```bash
# Extract specific fields
autocli hackernews top --limit 5 --format json | jq '.[].title'

# Filter by score
autocli hackernews top --limit 20 --format json | jq '.[] | select(.score > 100)'

# Count results
autocli reddit frontpage --limit 50 --format json | jq 'length'
```

## AI-Powered Features

AutoCLI integrates with [autocli.ai](https://autocli.ai) for AI-powered adapter generation and sharing.

### Authentication

```bash
# Authenticate with autocli.ai
autocli auth
```

This opens your browser to get an API token and saves it to `~/.autocli/config.json`.

### Generate Adapters with AI

Use the Chrome extension to visually select data elements:

1. Navigate to any website in Chrome
2. Click the AutoCLI extension icon
3. Use the selector tool to pick data elements
4. Click "Generate" to let AI create the adapter
5. The adapter is saved locally and synced to autocli.ai

### Search Community Adapters

```bash
# Search by URL
autocli search https://news.ycombinator.com

# Search by domain
autocli search producthunt.com
```

Searches autocli.ai for community-shared adapters. Select one to download and use immediately.

### Environment Variables

```bash
# Override API server (default: https://www.autocli.ai)
export AUTOCLI_API_BASE=https://custom-server.com
```

## Advanced Usage

### Download Media

```bash
# Download YouTube video (requires yt-dlp)
autocli youtube download "https://youtube.com/watch?v=..."

# Download Bilibili video
autocli bilibili download "https://www.bilibili.com/video/..."

# Download Xiaohongshu content
autocli xiaohongshu download "https://www.xiaohongshu.com/..."
```

### Social Media Interactions

```bash
# Twitter operations
autocli twitter post "Hello from AutoCLI!"
autocli twitter reply TWEET_ID "Great post!"
autocli twitter like TWEET_ID
autocli twitter bookmark TWEET_ID
autocli twitter follow USERNAME
autocli twitter bookmarks --limit 10

# Reddit operations
autocli reddit upvote POST_ID
autocli reddit comment POST_ID "Interesting discussion"
autocli reddit subscribe SUBREDDIT_NAME
autocli reddit saved --limit 10

# Xiaohongshu publishing
autocli xiaohongshu publish --title "My Post" --content "Content here" --images "image1.jpg,image2.jpg"
```

### Job Search (BOSS Zhipin)

```bash
# Search jobs
autocli boss search "Rust developer" --city "Beijing"

# Greet recruiter
autocli boss greet JOB_ID "Hello, I'm interested in this position"

# Batch greet
autocli boss batchgreet JOB_ID1,JOB_ID2,JOB_ID3 "Hello, I'm interested"

# View chat list
autocli boss chatlist

# View messages
autocli boss chatmsg BOSS_ID
```

## Shell Completion

Generate shell completions for better autocomplete experience:

```bash
# Bash
autocli completion bash >> ~/.bashrc

# Zsh
autocli completion zsh >> ~/.zshrc

# Fish
autocli completion fish > ~/.config/fish/completions/autocli.fish

# PowerShell
autocli completion powershell >> $PROFILE
```

## Configuration

AutoCLI stores configuration in `~/.autocli/config.json`:

```json
{
  "api_token": "your-autocli-ai-token",
  "browser_ws_endpoint": "ws://localhost:9222",
  "default_format": "table",
  "adapters_dir": "~/.autocli/adapters"
}
```

## Creating Custom Adapters

AutoCLI uses declarative YAML pipelines for custom adapters. Adapters are stored in `~/.autocli/adapters/`.

### Example Adapter Structure

```yaml
name: example-site
description: Example site adapter
version: 1.0.0
author: Your Name
commands:
  - name: hot
    description: Get hot posts
    mode: public  # or 'browser'
    pipeline:
      - step: fetch
        url: https://api.example.com/hot
        method: GET
      - step: extract
        selector: $.data[*]
        fields:
          - name: title
            path: $.title
          - name: url
            path: $.url
          - name: score
            path: $.score
      - step: output
        format: table
```

### Adapter Modes

- **public**: Uses public APIs, no authentication needed
- **browser**: Requires Chrome extension and browser session

### Pipeline Steps

1. **fetch**: HTTP request to target URL
2. **extract**: Extract data using JSON path or CSS selectors
3. **transform**: Modify/filter extracted data
4. **output**: Format and display results

## Integration with AI Agents

### Register in Agent Configuration

Add to `.cursorrules` or `AGENT.md`:

```bash
# Discover all available AutoCLI commands
autocli list

# Use specific commands as needed
autocli hackernews top --limit 10 --format json
autocli twitter search "topic" --format json
```

### Register Local CLI Tools

```bash
# Register local CLI tools for AI agent access
autocli register gh      # GitHub CLI
autocli register docker  # Docker CLI
autocli register kubectl # Kubernetes CLI
```

## Common Patterns

### Pipeline Data from Multiple Sites

```bash
# Get tech news from multiple sources
autocli hackernews top --limit 5 --format json > hn.json
autocli lobsters hot --limit 5 --format json > lobsters.json
autocli devto top --limit 5 --format json > devto.json
jq -s 'add' hn.json lobsters.json devto.json > combined.json
```

### Monitor Topics Across Platforms

```bash
#!/bin/bash
TOPIC="rust"

echo "=== Hacker News ==="
autocli hackernews search "$TOPIC" --limit 3

echo "=== Reddit ==="
autocli reddit search "$TOPIC" --limit 3

echo "=== Twitter ==="
autocli twitter search "$TOPIC" --limit 3

echo "=== Dev.to ==="
autocli devto tag "$TOPIC" --limit 3
```

### Archive Bookmarks

```bash
# Export Twitter bookmarks
autocli twitter bookmarks --limit 100 --format json > bookmarks_$(date +%Y%m%d).json

# Export Reddit saved posts
autocli reddit saved --limit 100 --format json > reddit_saved_$(date +%Y%m%d).json
```

## Troubleshooting

### Browser Connection Issues

```bash
# Run diagnostics
autocli doctor

# Check Chrome extension is loaded and active
# Verify browser is running on ws://localhost:9222

# Restart Chrome with remote debugging:
# macOS:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# Linux:
google-chrome --remote-debugging-port=9222

# Windows:
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

### Authentication Errors

```bash
# Re-authenticate
autocli auth

# Verify token in config
cat ~/.autocli/config.json | jq '.api_token'

# Clear and re-auth
rm ~/.autocli/config.json
autocli auth
```

### Command Not Found

```bash
# Verify installation
which autocli

# Check available commands
autocli --help

# Update to latest version
curl -fsSL https://raw.githubusercontent.com/nashsu/autocli/main/scripts/install.sh | sh
```

### Rate Limiting

Some sites may rate-limit requests. Use `--limit` to reduce request size:

```bash
# Reduce limit to avoid rate limiting
autocli twitter search "topic" --limit 5

# Add delays between requests (if supported)
autocli twitter timeline --limit 10 --delay 1000
```

### Extension Not Connecting

1. Ensure Chrome extension is enabled
2. Check extension has permissions for target sites
3. Verify autocli daemon is running
4. Restart browser and extension

## Performance Tips

- Use `--format json` for processing with other tools
- Limit results with `--limit` for faster responses
- Public API commands are faster than browser commands
- Browser commands reuse logged-in sessions (no token refresh)
- Use `--quiet` flag to suppress progress output in scripts

## Resources

- GitHub: https://github.com/nashsu/autocli
- AutoCLI.ai: https://autocli.ai (adapter marketplace)
- Documentation: Check `autocli --help` and subcommand help
- Issues: https://github.com/nashsu/autocli/issues
