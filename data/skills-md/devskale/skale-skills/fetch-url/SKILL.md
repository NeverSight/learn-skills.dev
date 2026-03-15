---
name: fetch-url
description: Fetch and extract readable text content from web pages. Auto-selects best tool with smart fallback. Use when the user wants to read articles, documentation, or scrape text content from web pages. Works on Reddit, StackOverflow, GitHub, docs sites, and more.
metadata:
  author: skale
  version: "2.1"
---

# Fetch URL

Extract text from any webpage. Works out-of-the-box.

## Quick Start

```bash
cd <skill-path>
./install.sh
./fetch-url "https://example.com"
```

**That's it!** No credentials needed for basic usage (jina/markdown/w3m are free).

## Credentials (Optional)

Only needed for the `--tool api` mode (custom API endpoint). Most users don't need this.

**Configure:**
```bash
# Option 1: Using credgoo (recommended)
credgoo add FETCH_URL_BEARER
# Enter your token when prompted

# Option 2: Environment variable
export FETCH_URL_BEARER=your_token

# Option 3: Add to shell config
echo 'export FETCH_URL_BEARER=your_token' >> ~/.zshrc
```

## Usage

```bash
# Just works (auto-selects best tool)
./fetch-url "https://example.com"

# Blocked sites too (Reddit, StackOverflow)
./fetch-url "https://reddit.com/r/python"
./fetch-url "https://stackoverflow.com/questions/12345"
```

## Options

```bash
./fetch-url "URL"                    # Auto (recommended)
./fetch-url "URL" --tool jina        # Force tool
./fetch-url "URL" -v                 # Verbose (show tool used)
./fetch-url "URL" --no-clean         # Keep empty lines
./fetch-url "URL" --md-method browser  # JS-heavy sites
```

| Option | Description |
|--------|-------------|
| `--tool NAME` | jina, markdown, w3m, lynx, chawan |
| `-v, --verbose` | Show which tool selected |
| `--no-clean` | Keep empty lines |
| `--md-method browser` | For JS SPAs |

## Tools

| Rank | Tool | Best For | Platform |
|------|------|----------|----------|
| 🥇 | jina | Docs, blogs, Wikipedia | All |
| 🥈 | w3m | Reddit, Hacker News | macOS/Linux |
| 🥉 | markdown | Fallback, GitHub | All |
| 4 | lynx | Simple reads | macOS/Linux |
| 5 | chawan | Visual debugging | macOS |

## Optional Browsers

Not required - jina/markdown work everywhere.

```bash
brew install w3m lynx chawan  # macOS
```

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md)
