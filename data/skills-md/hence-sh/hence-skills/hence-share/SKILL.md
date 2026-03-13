---
name: hence-share
description: Share a completed project to the Hence gallery (hence.sh) so the world can see what you built with AI. Use when the user has finished building something and wants to share it, post it to Hence, showcase their work, or upload screenshots of their project. Triggers on phrases like "share this on Hence", "post to Hence", "upload my project", or "let's publish this".
compatibility: Requires Python 3.8+. Screenshot capture requires Node.js and npx (for Playwright).
---

# Hence Share

> **Install from your project root directory.** Running `npx skills add` from a subdirectory will install into the wrong location.

Package and publish a project to the Hence gallery with screenshots, metadata, and attribution.

## Workflow

### 1. Authenticate

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

### 2. Gather metadata

Fetch valid slugs before assembling the project:

```bash
python scripts/fetch_metadata.py topics
python scripts/fetch_metadata.py agents
python scripts/fetch_metadata.py models
```

Pass `--json` for raw JSON when further processing is needed. See [references/api.md](references/api.md) for response schemas.

Ask the user:
- Which **topics** fit their project (pick from the list)
- Which **agent and model** they used (pick from the lists)
- A **title**, **one-liner** pitch, and optionally a **backstory** for the description

### 3. Capture screenshots

Up to 5 screenshots (1 primary + 4 additional).

**For web apps** — use the capture script:

```bash
python scripts/capture.py http://localhost:3000 --output hero.png
python scripts/capture.py http://localhost:3000/features --output features.png
```

**For non-web projects** — ask the user for screenshot file paths.

### 4. Share

```bash
python scripts/share.py \
  --title "My Project" \
  --one-liner "A short pitch" \
  --description "The backstory..." \
  --screenshot hero.png:"Hero view" \
  --screenshot features.png:"Feature tour" \
  --topics '["cli", "productivity"]' \
  --agents '[{"slug": "claude_code", "model_slug": "claude-sonnet-4"}]' \
  --url "https://myproject.dev"
```

Use `path:Caption text` format for `--screenshot` to attach a caption (split on first colon). Omit the colon for no caption.

The script shows a review summary and asks for confirmation before uploading.

Pass `--yes` to skip the confirmation prompt when running non-interactively.

### 5. Update an existing project

```bash
python scripts/update.py <project-id> \
  --title "New Title" \
  --one-liner "Updated pitch" \
  --yes
```

To manage screenshots on an existing project, use `screenshots.py` (see step 6).

### 6. Manage screenshots on an existing project

```bash
# List all screenshots with IDs and captions
python scripts/screenshots.py <project-id> list

# Add a screenshot
python scripts/screenshots.py <project-id> add --file hero.png --caption "Hero view"

# Update caption or image
python scripts/screenshots.py <project-id> update <screenshot-id> --caption "New caption"
python scripts/screenshots.py <project-id> update <screenshot-id> --file new.png

# Remove a screenshot
python scripts/screenshots.py <project-id> remove <screenshot-id>

# Reorder (pass all IDs in desired order; first becomes primary)
python scripts/screenshots.py <project-id> reorder <id1> <id2> <id3>
```

### 7. Inspired-by linking

If the user found inspiration via `hence-search` and you stored a project ID with `save_memory`, include it:

```bash
python scripts/share.py ... --inspired-by <project-id>
```

## CLI Reference

### `capture.py`

```
python scripts/capture.py <url> [--output <file>] [--wait <ms>]
```

| Flag | Default | Description |
|------|---------|-------------|
| `url` | required | URL to capture |
| `--output` | `screenshot.png` | Output filename |
| `--wait` | `2000` | Wait time in ms after page load |

### `share.py`

| Flag | Default | Description |
|------|---------|-------------|
| `--title` | required | Project title |
| `--one-liner` | required | Short pitch |
| `--screenshot` | required, repeatable | `path` or `path:Caption` — first = primary, max 5 |
| `--description` | `""` | Full project description |
| `--topics` | `[]` | JSON array of topic slugs |
| `--agents` | `[]` | JSON array of agent objects |
| `--url` | `""` | Project URL |
| `--deployment-status` | `public` | `local`, `closed`, or `public` |
| `--inspired-by` | `""` | UUID of inspiring project |
| `--yes` / `-y` | false | Skip confirmation prompt |

### `update.py`

| Flag | Default | Description |
|------|---------|-------------|
| `project_id` | required | UUID of project to update |
| `--title` | `""` | New title |
| `--one-liner` | `""` | New pitch |
| `--topics` | `""` | JSON array of topic slugs |
| `--agents` | `""` | JSON array of agent objects |
| `--yes` / `-y` | false | Skip confirmation prompt |

### `screenshots.py`

```
python scripts/screenshots.py <project_id> <subcommand> [options]
```

| Subcommand | Arguments | Description |
|------------|-----------|-------------|
| `list` | — | List all screenshots (id, position, caption, url) |
| `add` | `--file path` `[--caption text]` | Upload and append a screenshot |
| `update` | `<screenshot_id>` `[--file path]` `[--caption text]` | Update image and/or caption |
| `remove` | `<screenshot_id>` | Delete a screenshot; re-sequences positions |
| `reorder` | `<id1> <id2> ...` | Assign positions by order; first becomes primary |

## API details

See [references/api.md](references/api.md) for full endpoint documentation, field formats, and error codes.
