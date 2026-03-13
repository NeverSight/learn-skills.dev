---
name: wechat-to-md
description: Convert WeChat Official Account (微信公众号) articles to clean Markdown files with locally downloaded images.
---

# WeChat Article to Markdown Converter

## What this tool does

Converts WeChat public account articles into clean Markdown files with:
- YAML frontmatter (title, author, date, source URL)
- Locally downloaded images
- Preserved code blocks with language detection
- Audio/video reference extraction
- Clean formatting (no WeChat UI noise)

## Prerequisites

- Python 3.10+
- Install dependencies: `pip install -r requirements.txt`
- Camoufox browser will be auto-downloaded on first run

## Usage

### CLI (single article)

```bash
python main.py "https://mp.weixin.qq.com/s/ARTICLE_ID"
```

### CLI (batch from file)

```bash
python main.py -f urls.txt -o ./output -v
```

### CLI Options

| Flag | Description |
|------|-------------|
| `-f FILE` | Text file with URLs (one per line) |
| `-o DIR` | Output directory (default: ./output) |
| `-c N` | Image download concurrency (default: 5) |
| `--no-images` | Skip image download, keep remote URLs |
| `--no-headless` | Show browser (for solving CAPTCHAs) |
| `--force` | Overwrite existing output |
| `--no-frontmatter` | Use blockquote metadata instead of YAML |
| `-v` | Verbose/debug logging |

### MCP Server

Run as an MCP server for AI tool integration:

```bash
python mcp_server.py
```

Exposes two tools:
- `convert_article(url, output_dir, download_images, concurrency, use_frontmatter)` — Convert a single article
- `batch_convert(urls, output_dir, download_images, concurrency)` — Convert multiple articles

### MCP Configuration (for claude_desktop_config.json or similar)

```json
{
  "mcpServers": {
    "wechat-to-md": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "<path-to-this-project>"
    }
  }
}
```

## Output Structure

```
output/
  <article-title>/
    <article-title>.md    # Markdown file with YAML frontmatter
    images/
      img_001.png
      img_002.jpg
      ...
```

## Common Issues

- **CAPTCHA/verification page**: Run with `--no-headless` to manually solve the CAPTCHA in the browser window, then retry.
- **Empty content**: WeChat may rate-limit requests. Wait a few minutes and try again.
- **Image download failures**: Failed images keep their remote URLs in the markdown. Re-run with `--force` to retry.

## Limitations

- Only supports articles from `mp.weixin.qq.com`
- Requires a working internet connection and the ability to run a headless browser
- WeChat may block automated access; Camoufox helps evade detection but is not guaranteed
