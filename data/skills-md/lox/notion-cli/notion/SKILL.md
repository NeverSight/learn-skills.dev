---
name: notion
description: Manage Notion pages, databases, and comments from the command line. Search, view, create, and edit content in your Notion workspace.
allowed-tools: Bash(notion-cli:*)
---

# Notion CLI

A CLI to manage Notion from the command line, using Notion's remote MCP server.

## Prerequisites

The `notion-cli` command must be available on PATH. To check:

```bash
notion-cli --version
```

If not installed:

```bash
go install github.com/lox/notion-cli@latest
```

Or see: https://github.com/lox/notion-cli

## Authentication

The CLI uses OAuth authentication. On first use, it opens a browser for authorization:

```bash
notion-cli auth login      # Authenticate with Notion
notion-cli auth status     # Check authentication status
notion-cli auth logout     # Clear credentials
```

For CI/headless environments, set `NOTION_ACCESS_TOKEN` environment variable.

## Available Commands

```
notion-cli auth            # Manage authentication
notion-cli page            # Manage pages (list, view, create, upload, edit)
notion-cli db              # Manage databases (list, query)
notion-cli search          # Search the workspace
notion-cli comment         # Manage comments (list, create)
notion-cli tools           # List available MCP tools
```

## Common Operations

### Search

```bash
notion-cli search "meeting notes"           # Search workspace
notion-cli search "project" --limit 5       # Limit results
notion-cli search "query" --json            # JSON output
```

### Pages

All page commands accept a **URL**, **name**, or **ID** to identify pages.

```bash
# List pages
notion-cli page list
notion-cli page list --limit 10
notion-cli page list --json

# View a page (renders as markdown in terminal)
notion-cli page view <page>
notion-cli page view <page> --raw            # Show raw Notion markup
notion-cli page view <page> --json           # JSON output
notion-cli page view "Meeting Notes"         # By name
notion-cli page view https://notion.so/...   # By URL

# Create a page
notion-cli page create --title "New Page"
notion-cli page create --title "Doc" --content "# Heading\n\nContent here"
notion-cli page create --title "Child" --parent "Engineering"   # Parent by name
notion-cli page create --title "Child" --parent <page-id>       # Parent by ID

# Upload a markdown file as a page
notion-cli page upload ./document.md
notion-cli page upload ./doc.md --title "Custom Title"
notion-cli page upload ./doc.md --parent "Parent Page Name"

# Sync a markdown file (create or update)
# First run creates the page and writes notion-id to the file's frontmatter.
# Subsequent runs update the page content using the stored notion-id.
notion-cli page sync ./document.md
notion-cli page sync ./document.md --parent "Engineering"   # Set parent on first sync
notion-cli page sync ./document.md --title "Custom Title"

# Edit a page
notion-cli page edit <page> --replace "New content"
notion-cli page edit <page> --find "old text" --replace-with "new text"
notion-cli page edit <page> --find "section" --append "additional content"
```

### Databases

```bash
notion-cli db list                          # List databases
notion-cli db list --json

notion-cli db query <database-url-or-id>    # Query a database
notion-cli db query <id> --json
```

### Comments

```bash
notion-cli comment list <page-id>           # List comments on a page
notion-cli comment list <page-id> --json

notion-cli comment create <page-id> --content "Great work!"
```

## Output Formats

Most commands support `--json` for machine-readable output:

```bash
notion-cli page list --json | jq '.[0].url'
notion-cli search "api" --json | jq '.[] | .title'
```

## Tips for Agents

1. **Search first** - Use `notion-cli search` to find pages before operating on them
2. **Use URLs or IDs** - Both work for page/database references
3. **Check --help** - Every command has detailed help: `notion-cli page edit --help`
4. **Raw output** - Use `--raw` with `page view` to see the original Notion markup
5. **JSON for parsing** - Use `--json` when you need to extract specific fields
