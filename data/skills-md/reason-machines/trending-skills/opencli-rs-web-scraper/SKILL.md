---
name: opencli-rs-web-scraper
description: Blazing fast Rust CLI tool to fetch information from 55+ websites (Twitter, Reddit, YouTube, Bilibili, Zhihu, etc.) with a single command, plus AI-native discovery and Electron app control.
triggers:
  - fetch data from twitter using opencli
  - scrape website with opencli-rs
  - get hacker news top stories command line
  - control cursor app from terminal
  - fetch bilibili trending videos cli
  - integrate github docker kubectl with opencli
  - generate yaml adapter for website scraping
  - install opencli-rs rust web fetcher
---

# opencli-rs Web Scraper & Site Fetcher

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

opencli-rs is a single 4.7MB Rust binary that fetches real-time data from 55+ websites (Twitter/X, Reddit, YouTube, HackerNews, Bilibili, Zhihu, Xiaohongshu, and more) with one command. It reuses your browser session via a Chrome extension, supports AI-native API discovery, controls Electron desktop apps (Cursor, ChatGPT, Notion), and passes through to external CLIs (gh, docker, kubectl). Up to 12x faster and 10x less memory than the Node.js original.

---

## Installation

### One-line (macOS / Linux)
```bash
curl -fsSL https://raw.githubusercontent.com/nashsu/opencli-rs/main/scripts/install.sh | sh
```

### Windows (PowerShell)
```powershell
Invoke-WebRequest -Uri "https://github.com/nashsu/opencli-rs/releases/latest/download/opencli-rs-x86_64-pc-windows-msvc.zip" -OutFile opencli-rs.zip
Expand-Archive opencli-rs.zip -DestinationPath .
Move-Item opencli-rs.exe "$env:LOCALAPPDATA\Microsoft\WindowsApps\"
```

### Build from Source
```bash
git clone https://github.com/nashsu/opencli-rs.git
cd opencli-rs
cargo build --release
cp target/release/opencli-rs /usr/local/bin/
```

### Chrome Extension (required for Browser-mode commands)
1. Download `opencli-rs-chrome-extension.zip` from [GitHub Releases](https://github.com/nashsu/opencli-rs/releases/latest)
2. Extract to any directory
3. Open `chrome://extensions` → enable **Developer mode** → **Load unpacked** → select the extracted folder
4. Extension auto-connects to the opencli-rs daemon

### AI Agent Skill Install
```bash
npx skills add https://github.com/nashsu/opencli-rs-skill
```

---

## Command Modes

| Mode | Requirement | Examples |
|------|-------------|---------|
| **Public** | Nothing — calls public APIs directly | hackernews, devto, arxiv, wikipedia |
| **Browser** | Chrome + extension running | twitter, bilibili, reddit, zhihu |
| **Desktop** | Target Electron app running | cursor, chatgpt, notion, discord |

---

## Key Commands

### Global Flags
```bash
opencli-rs --help                        # list all commands
opencli-rs <site> --help                 # site-specific help
opencli-rs <site> <cmd> --format json    # output: table | json | yaml | csv | markdown
opencli-rs <site> <cmd> --limit 20       # limit results
opencli-rs doctor                        # run diagnostics
opencli-rs completion bash >> ~/.bashrc  # shell completions (bash/zsh/fish)
```

### Public Commands (no browser needed)
```bash
# Hacker News
opencli-rs hackernews top --limit 10
opencli-rs hackernews search "rust async" --limit 5
opencli-rs hackernews user pg

# arXiv
opencli-rs arxiv search "large language models" --limit 10
opencli-rs arxiv paper 2303.08774

# Wikipedia
opencli-rs wikipedia summary "Rust programming language"
opencli-rs wikipedia search "memory safety"
opencli-rs wikipedia random

# Stack Overflow
opencli-rs stackoverflow hot
opencli-rs stackoverflow search "tokio async runtime"

# Dev.to
opencli-rs devto top
opencli-rs devto tag rust

# Linux.do
opencli-rs linux-do hot
opencli-rs linux-do search "Rust"
```

### Browser Commands (Chrome extension required)
```bash
# Twitter/X
opencli-rs twitter search "rust lang" --limit 10
opencli-rs twitter trending
opencli-rs twitter timeline
opencli-rs twitter bookmarks
opencli-rs twitter profile elonmusk
opencli-rs twitter post "Hello from opencli-rs!"
opencli-rs twitter follow rustlang

# Bilibili
opencli-rs bilibili hot --limit 20
opencli-rs bilibili search "Rust教程"
opencli-rs bilibili ranking
opencli-rs bilibili feed
opencli-rs bilibili download <video_url>

# Reddit
opencli-rs reddit frontpage
opencli-rs reddit popular
opencli-rs reddit subreddit rust
opencli-rs reddit search "async await"
opencli-rs reddit upvote <post_id>

# Zhihu
opencli-rs zhihu hot
opencli-rs zhihu search "Rust 内存安全"
opencli-rs zhihu question 12345

# Xiaohongshu
opencli-rs xiaohongshu search "旅行攻略"
opencli-rs xiaohongshu feed
opencli-rs xiaohongshu user <user_id>

# YouTube
opencli-rs youtube search "rust tutorial"
opencli-rs youtube video <video_id>
opencli-rs youtube transcript <video_id>

# Weibo
opencli-rs weibo hot
opencli-rs weibo search "科技"

# Douban
opencli-rs douban top250
opencli-rs douban search "三体"
opencli-rs douban movie-hot

# Medium
opencli-rs medium search "rust programming"
opencli-rs medium feed
opencli-rs medium user graydon_hoare

# Xueqiu (stock)
opencli-rs xueqiu hot-stock
opencli-rs xueqiu search "茅台"
opencli-rs xueqiu stock SH600519
```

### Desktop App Control (Electron)
```bash
# Cursor IDE
opencli-rs cursor status
opencli-rs cursor send "Refactor this function to use async/await"
opencli-rs cursor read
opencli-rs cursor ask "What does this code do?"
opencli-rs cursor screenshot
opencli-rs cursor extract-code
opencli-rs cursor model

# ChatGPT Desktop
opencli-rs chatgpt new
opencli-rs chatgpt send "Explain Rust lifetimes"
opencli-rs chatgpt read

# Notion
opencli-rs notion search "project notes"
opencli-rs notion read <page_id>
opencli-rs notion write <page_id> "New content"
opencli-rs notion sidebar

# Discord Desktop
opencli-rs discord-app channels
opencli-rs discord-app send "Hello team"
opencli-rs discord-app read
```

### External CLI Passthrough
```bash
# GitHub CLI
opencli-rs gh repo list
opencli-rs gh pr list
opencli-rs gh issue create --title "Bug report"

# Docker
opencli-rs docker ps
opencli-rs docker images
opencli-rs docker logs my-container

# Kubernetes
opencli-rs kubectl get pods
opencli-rs kubectl get services -n production
opencli-rs kubectl logs <pod-name>
```

### AI Discovery Commands
```bash
# Explore a website's API surface
opencli-rs explore https://example.com

# Auto-detect authentication strategies
opencli-rs cascade https://api.example.com/data

# Auto-generate an adapter (YAML pipeline)
opencli-rs generate https://example.com --goal "hot posts"

# Synthesize adapter from discovered API
opencli-rs synthesize https://news.example.com
```

---

## Output Formats

```bash
# Default: ASCII table
opencli-rs hackernews top --limit 5

# JSON — great for piping to jq
opencli-rs hackernews top --limit 5 --format json | jq '.[].title'

# YAML
opencli-rs hackernews top --format yaml

# CSV — for spreadsheets
opencli-rs hackernews top --format csv > hn_top.csv

# Markdown — for docs
opencli-rs hackernews top --format markdown
```

---

## Declarative YAML Pipeline (Custom Adapters)

Add new site adapters without writing Rust code. Create a YAML file describing the scraping pipeline:

```yaml
# ~/.config/opencli-rs/adapters/my-site.yaml
name: my-site
description: Fetch top posts from my-site
base_url: https://api.my-site.com
commands:
  top:
    description: Get top posts
    endpoint: /v1/posts/top
    method: GET
    params:
      limit:
        flag: --limit
        default: 10
        query_param: count
    response:
      items_path: $.data.posts
      fields:
        - name: title
          path: $.title
        - name: url
          path: $.url
        - name: score
          path: $.points
        - name: author
          path: $.author.name
```

```bash
# Use the custom adapter
opencli-rs my-site top --limit 20
opencli-rs my-site top --format json
```

---

## Real-World Patterns

### Pipe JSON output to jq for filtering
```bash
# Get only titles from HN top stories
opencli-rs hackernews top --limit 20 --format json | jq -r '.[].title'

# Get Twitter trending topics as plain list
opencli-rs twitter trending --format json | jq -r '.[].name'

# Find Bilibili videos with >1M views
opencli-rs bilibili ranking --format json | jq '[.[] | select(.view > 1000000)]'
```

### Shell scripting
```bash
#!/bin/bash
# Daily digest script

echo "=== HackerNews Top 5 ==="
opencli-rs hackernews top --limit 5 --format table

echo ""
echo "=== Bilibili Trending ==="
opencli-rs bilibili hot --limit 5 --format table

echo ""
echo "=== Zhihu Hot ==="
opencli-rs zhihu hot --limit 5 --format table
```

### Export to file
```bash
opencli-rs reddit popular --format csv > reddit_$(date +%Y%m%d).csv
opencli-rs hackernews top --format json > hn_top.json
```

### Use in Rust project via subprocess
```rust
use std::process::Command;
use serde_json::Value;

fn fetch_hn_top(limit: u32) -> anyhow::Result<Vec<Value>> {
    let output = Command::new("opencli-rs")
        .args(["hackernews", "top", "--limit", &limit.to_string(), "--format", "json"])
        .output()?;

    let json: Vec<Value> = serde_json::from_slice(&output.stdout)?;
    Ok(json)
}

fn fetch_twitter_search(query: &str) -> anyhow::Result<Vec<Value>> {
    let output = Command::new("opencli-rs")
        .args(["twitter", "search", query, "--format", "json"])
        .output()?;

    if !output.status.success() {
        let err = String::from_utf8_lossy(&output.stderr);
        anyhow::bail!("opencli-rs error: {}", err);
    }

    let json: Vec<Value> = serde_json::from_slice(&output.stdout)?;
    Ok(json)
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let stories = fetch_hn_top(10)?;
    for story in &stories {
        println!("{}", story["title"].as_str().unwrap_or(""));
    }
    Ok(())
}
```

### AI Agent integration (AGENT.md / .cursorrules)
```markdown
# AGENT.md

## Available Tools
Run `opencli-rs list` to discover all available commands.

### Web Data Fetching
- `opencli-rs hackernews top --format json` — HN top stories
- `opencli-rs twitter search "<query>" --format json` — Twitter search
- `opencli-rs arxiv search "<topic>" --format json` — Research papers
- `opencli-rs reddit subreddit <name> --format json` — Subreddit posts

### Local CLI Tools
- `opencli-rs gh <args>` — GitHub operations
- `opencli-rs docker <args>` — Docker operations
- `opencli-rs kubectl <args>` — Kubernetes operations

Register custom tools: `opencli-rs register mycli`
```

---

## Configuration

### Config file location
```
~/.config/opencli-rs/config.toml   # macOS / Linux
%APPDATA%\opencli-rs\config.toml   # Windows
```

### Custom adapter directory
```toml
# ~/.config/opencli-rs/config.toml
adapter_dir = "~/.config/opencli-rs/adapters"
default_format = "table"
default_limit = 20
```

### Register a custom external CLI
```bash
# Register your own CLI tool for passthrough
opencli-rs register mycli

# Now use it via opencli-rs
opencli-rs mycli --help
opencli-rs mycli some-command --flag value
```

---

## Troubleshooting

### Run diagnostics first
```bash
opencli-rs doctor
```

### Chrome extension not connecting
```bash
# Check extension is loaded at chrome://extensions
# Verify Developer mode is ON
# Reload the extension after reinstalling opencli-rs
# Check daemon is running:
opencli-rs doctor
```

### Browser command returns empty / auth error
- Open Chrome and ensure you are **logged in** to the target site
- The extension reuses your existing browser session — no tokens needed
- Try refreshing the target site tab, then retry the command

### Binary not found after install
```bash
# Verify install location
which opencli-rs
ls /usr/local/bin/opencli-rs

# Add to PATH if missing
export PATH="/usr/local/bin:$PATH"
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
```

### Build errors from source
```bash
# Ensure Rust toolchain is up to date
rustup update stable
rustup target add aarch64-apple-darwin   # macOS Apple Silicon
cargo build --release
```

### Command slow or timing out
- Browser commands require Chrome + extension; without it they will hang
- Run `opencli-rs doctor` to verify extension connectivity
- Public commands (hackernews, arxiv, etc.) need no browser and run in ~1-2s

### Windows path issues
```powershell
# Verify binary location
Get-Command opencli-rs
# If not found, ensure the directory is in $env:PATH
$env:PATH += ";$env:LOCALAPPDATA\Microsoft\WindowsApps"
```

---

## Supported Sites Reference

| Category | Sites |
|----------|-------|
| **Tech News** | HackerNews, Dev.to, Lobsters, Linux-do |
| **Social** | Twitter/X, Reddit, Facebook, Instagram, TikTok, Jike |
| **Video** | YouTube, Bilibili, Weixin |
| **Chinese** | Zhihu, Xiaohongshu, Weibo, Douban, Xueqiu, Weread, Sinablog, Sinafinance |
| **Research** | arXiv, Hugging Face |
| **Finance** | Yahoo Finance, Barchart, Xueqiu |
| **Jobs** | Boss, LinkedIn |
| **Reading** | Medium, Substack, Wikipedia, BBC, Bloomberg, Reuters |
| **Shopping** | Steam, SMZDM, Ctrip, Coupang |
| **AI/Desktop** | Cursor, ChatGPT, Codex, Doubao, ChatWise, Notion, Discord |
| **Podcast** | Apple Podcasts, Xiaoyuzhou |
| **External CLI** | gh, docker, kubectl, obsidian, readwise, gws |
