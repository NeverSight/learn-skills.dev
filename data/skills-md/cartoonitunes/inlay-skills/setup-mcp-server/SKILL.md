---
name: setup-mcp-server
description: |
  Set up an MCP (Model Context Protocol) server for any website via Inlay.
  Enables AI agents to search, browse, and interact with your site programmatically.
  Use when adding MCP support, enabling AI agent access, or setting up Inlay.
triggers:
  - "MCP server"
  - "MCP setup"
  - "Model Context Protocol"
  - "AI agent access"
  - "Inlay setup"
---

# Setup MCP Server Skill

Set up an MCP (Model Context Protocol) server for your website using [Inlay](https://inlay.dev). This lets AI agents like Claude, ChatGPT, and others interact with your site programmatically — searching pages, retrieving content, and using your site's functionality.

## What is MCP?

MCP (Model Context Protocol) is a standard that lets AI agents connect to external tools and data sources. An MCP server for your website gives AI agents tools like:

- `get_site_info` — Get site metadata and description
- `search_pages` — Search your site's content
- `get_page_content` — Retrieve specific page content
- `list_pages` — Browse available pages

## Workflow

### Step 1: Sign Up for Inlay

1. Go to [inlay.dev](https://inlay.dev)
2. Create an account
3. Add your website (enter your domain)

### Step 2: Install the Embed Script

Add the Inlay embed script to your site. This enables Inlay to index your content and serve it via MCP.

**Next.js (App Router):**
```tsx
// app/layout.tsx
import Script from 'next/script'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Script
          src="https://cdn.inlay.dev/embed.js"
          data-site-id="YOUR_SITE_ID"
          strategy="afterInteractive"
        />
      </body>
    </html>
  )
}
```

**Next.js (Pages Router):**
```tsx
// pages/_app.tsx
import Script from 'next/script'

export default function App({ Component, pageProps }) {
  return (
    <>
      <Component {...pageProps} />
      <Script
        src="https://cdn.inlay.dev/embed.js"
        data-site-id="YOUR_SITE_ID"
        strategy="afterInteractive"
      />
    </>
  )
}
```

**Astro:**
```html
<!-- src/layouts/Base.astro -->
<script src="https://cdn.inlay.dev/embed.js" data-site-id="YOUR_SITE_ID"></script>
```

**Plain HTML:**
```html
<script src="https://cdn.inlay.dev/embed.js" data-site-id="YOUR_SITE_ID"></script>
```

Replace `YOUR_SITE_ID` with the Site ID from your Inlay dashboard.

### Step 3: Verify MCP Endpoint

Once the embed script is installed and Inlay has indexed your site, your MCP endpoint is available at:

```
https://mcp.inlay.dev/YOUR_SITE_SLUG
```

Test it:

```bash
# Check MCP endpoint is responding
curl -s https://mcp.inlay.dev/YOUR_SITE_SLUG

# List available tools
curl -s -X POST https://mcp.inlay.dev/YOUR_SITE_SLUG \
  -H 'Content-Type: application/json' \
  -d '{"method":"tools/list"}'
```

### Step 4: Test MCP Tools

Test each tool to make sure it works:

```bash
# Get site info
curl -s -X POST https://mcp.inlay.dev/YOUR_SITE_SLUG \
  -H 'Content-Type: application/json' \
  -d '{"method":"tools/call","params":{"name":"get_site_info","arguments":{}}}'

# Search pages
curl -s -X POST https://mcp.inlay.dev/YOUR_SITE_SLUG \
  -H 'Content-Type: application/json' \
  -d '{"method":"tools/call","params":{"name":"search_pages","arguments":{"query":"getting started"}}}'

# Get specific page content
curl -s -X POST https://mcp.inlay.dev/YOUR_SITE_SLUG \
  -H 'Content-Type: application/json' \
  -d '{"method":"tools/call","params":{"name":"get_page_content","arguments":{"path":"/"}}}'
```

### Step 5: Advertise Your MCP Server

Make your MCP server discoverable:

1. **Add to llms.txt:**
```text
## MCP
- Endpoint: https://mcp.inlay.dev/YOUR_SITE_SLUG
- Tools: get_site_info, search_pages, get_page_content, list_pages
```

2. **Add meta tag (optional):**
```html
<meta name="mcp-server" content="https://mcp.inlay.dev/YOUR_SITE_SLUG">
```

### Step 6: Verify with Audit

Run an AI readiness audit to confirm MCP is detected:

```bash
curl -s -X POST https://www.inlay.dev/api/audit \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://YOUR_SITE"}'
```

The MCP Server category score should now be high.

## Tips

- Inlay re-indexes your site periodically — new pages appear automatically
- The MCP server works with any AI agent that supports MCP (Claude Desktop, Cursor, etc.)
- You can configure which pages are indexed in the Inlay dashboard
- For private/authenticated content, check Inlay's access control settings
