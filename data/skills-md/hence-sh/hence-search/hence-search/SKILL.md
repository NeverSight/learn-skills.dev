---
name: hence-search
description: Browse and search the Hence gallery (hence.sh) to discover projects built with AI coding agents. Use when the user wants inspiration, wants to see what others have built, asks about projects on Hence, or mentions searching for AI-built projects. Triggers on queries like "show me cool projects", "search Hence", "find CLI tools on Hence", or "what are people building with Claude Code".
---

# Hence Search

Search the Hence gallery to find projects and draw inspiration from what others are building with AI.

## Workflow

### 0. Authenticate

Check for existing credentials. If none found, start the device flow:

```bash
python scripts/auth.py --check
```

If the check fails, run the device flow:

```bash
python scripts/auth.py
```

The script will print a URL and a one-time code. **Before running the command, tell the user** they'll need to:
1. Open the URL in their browser
2. Log in to Hence if they aren't already (via GitHub or Google)
3. Enter the code shown in the terminal

The script will wait and automatically complete once the user approves. No further action is needed from the agent after that.

For CI/CD environments, pass an API key directly:

```bash
python scripts/auth.py <api-key>
```

### 1. Determine search strategy

- **Specific query** (e.g. "Rust CLI tools"): run `search.py` directly with keywords.
- **Broad browsing** (e.g. "show me cool stuff"): run `fetch_metadata.py topics` first, suggest 3–5 relevant categories, then search by topic.

### 2. Execute search

```bash
python scripts/search.py "productivity cli"
python scripts/search.py "" --topic game --limit 10
python scripts/search.py "dashboard" --topic react --offset 20
```

For valid topic slugs:

```bash
python scripts/fetch_metadata.py topics
```

Pass `--json` to either script for raw JSON output when further processing is needed.

### 3. Present results

For each project include:
- **Title and pitch** — the name and one-liner
- **Built with** — agent/model if available
- **Link** — `https://hence.sh/p/<id>`

### 4. Connect inspiration

After showing results, ask: *"Does any of this spark ideas for your current build?"*

If the user identifies a project as inspiring, store its ID and title via `save_memory` so the `hence-share` skill can suggest an "Inspired by" link later.

### 5. Paginate

If results are truncated, offer to load more by incrementing `--offset`.

## API details

See [references/api.md](references/api.md) for full endpoint documentation, response schemas, and available metadata endpoints.
