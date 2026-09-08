---
name: md-lark-converter
description: "Bidirectional conversion between Markdown and Feishu (Lark) documents using md2fs and fs2md CLI tools. Use this skill whenever the user mentions Feishu, Lark, 飞书, feishu.cn URLs, md2fs, fs2md, md-lark-converter, pasting documents to Feishu, exporting from Feishu, converting to/from Feishu format, syncing content with Feishu, setting up Feishu cookies, or any workflow involving Markdown and Feishu documents — even if they don't explicitly say 'convert'. Also trigger when the user shares a feishu.cn or lark link."
---

# Markdown ↔ Feishu Converter

Two CLI commands handle the conversion:

- **`md2fs`** — Markdown → Feishu clipboard format (paste directly into Feishu docs)
- **`fs2md`** — Feishu → Markdown (fetch via URL, with automatic image download)

Both are provided by `@md-lark-converter/cli`.

## First: Check CLI Availability

Before running any command, verify the CLI is installed:

```bash
which md2fs 2>/dev/null || echo "NOT_INSTALLED"
```

If not installed, install it:

```bash
npm install -g @md-lark-converter/cli
```

## Markdown → Feishu (md2fs)

The most common use case — the user has Markdown content and wants it in Feishu.

```bash
# Convert and copy to clipboard — user pastes directly into Feishu
md2fs <file.md> --copy

# Pipe content from stdin
echo "# Hello World" | md2fs --stdin --copy

# Save raw Lark JSON (for debugging or programmatic use)
md2fs <file.md> -o output.json
```

After `md2fs --copy` succeeds, tell the user: "Content copied to clipboard — paste into your Feishu document with Cmd+V / Ctrl+V."

If clipboard copy fails (common on headless/remote environments), `md2fs` falls back to printing HTML to stdout. In that case, suggest saving to a JSON file with `-o` instead.

## Feishu → Markdown (fs2md)

Fetches a Feishu document by URL and converts to Markdown. Requires authentication — see Cookie Setup below.

```bash
# Save to file (images auto-downloaded to ./images/ next to the output)
fs2md <feishu-url> -o output.md

# Copy Markdown to clipboard instead of saving
fs2md <feishu-url>

# Skip image downloading
fs2md <feishu-url> -o output.md --no-images
```

### Supported URL formats

Both document types are supported — wiki URLs are auto-resolved to the underlying docx:

- `https://xxx.feishu.cn/docx/TOKEN`
- `https://xxx.feishu.cn/wiki/TOKEN`

### Image handling

By default, all images in the document are downloaded to an `images/` directory alongside the output file, and Markdown references are rewritten to `./images/filename.png`. Use `--no-images` if you only need the text.

## Cookie Setup (Required for fs2md)

`fs2md` needs a Feishu session cookie to access documents. The cookie is resolved in this order:

1. `--cookie` CLI flag (one-off use)
2. `FEISHU_COOKIE` environment variable
3. `~/.md-lark-converter.json` config file (recommended for persistent use)

### Check if cookie is already configured

```bash
cat ~/.md-lark-converter.json 2>/dev/null
```

If the config file exists and contains a cookie, try using it directly. Only proceed with cookie setup if it's missing or expired (authentication errors).

### Obtaining the cookie

When a cookie is needed (missing or expired), **proactively ask the user**:

> "I need a Feishu session cookie to fetch documents. Would you like me to automatically open a browser and extract it after you log in? Or would you prefer to copy it manually from DevTools?"

#### Option A: Automatic extraction via `agent-browser` (recommended)

**IMPORTANT: Do NOT write a Playwright/Puppeteer script file. Use `agent-browser` CLI commands directly.**

**Prerequisite:** This requires [`agent-browser`](https://github.com/vercel-labs/agent-browser). If not installed, tell the user:

```bash
npm install -g agent-browser
```

Once installed, use `agent-browser` CLI commands to:

1. Launch a headed browser and navigate to Feishu:
   ```bash
   agent-browser navigate https://www.feishu.cn --headed
   ```
2. Tell the user to log in within the browser window. Wait for the user to confirm they have logged in.
3. Read cookies from the browser:
   ```bash
   agent-browser cookies
   ```
4. From the output, collect all cookies whose domain includes `feishu.cn` or `lark`, format as `name=value; name=value; ...`
5. Save to `~/.md-lark-converter.json`:
   ```json
   { "cookie": "<collected-cookie-string>" }
   ```
6. Close the browser:
   ```bash
   agent-browser close
   ```

#### Option B: Manual extraction from DevTools (default)

Guide the user through manual extraction:

1. Open a Feishu document in the browser (e.g. `https://xxx.feishu.cn/docx/...`)
2. Open DevTools — `F12` (Windows/Linux) or `Cmd+Option+I` (macOS)
3. Switch to the **Network** tab, refresh the page
4. Click any request to `feishu.cn`
5. In the request headers, copy the entire **Cookie** header value (it's long — that's expected)
6. Save to config file:

```bash
cat > ~/.md-lark-converter.json << 'EOF'
{
  "cookie": "YOUR_COOKIE_HERE"
}
EOF
```

### Cookie expiration

The cookie expires periodically (typically after a few days). If `fs2md` returns authentication errors or empty results, the cookie needs to be refreshed. Ask the user again whether they'd like automatic or manual extraction.

## Decision Flow

When the user's request involves Feishu:

**User has Markdown, wants it in Feishu →**
1. Identify the Markdown file path or content
2. Run `md2fs <path> --copy`
3. Confirm clipboard is ready for pasting

**User wants Feishu content as Markdown →**
1. Get the Feishu document URL
2. Check cookie: `cat ~/.md-lark-converter.json 2>/dev/null`
3. If no cookie exists, ask the user whether to auto-extract via browser automation or manually copy from DevTools
4. Run `fs2md <url> -o <output-path>`
5. Report the saved file path and image count

**User shares a feishu.cn link without explicit instructions →**
Ask whether they want to export it as Markdown. If yes, follow the Feishu → Markdown flow.

**User mentions Feishu cookie / authentication issues →**
Check the existing config, then offer automatic browser extraction first, with manual DevTools as fallback.
