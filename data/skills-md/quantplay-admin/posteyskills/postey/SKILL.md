---
name: postey
description: >
  Create, schedule, and manage social media posts via Postey. ALWAYS use this
  skill when asked to draft, schedule, post, or check tweets, posts, threads, or
  social media content for Twitter/X, LinkedIn.
last-updated: 2026-02-15
allowed-tools: Bash(./scripts/postey.js:*)
---

# Postey Skill

Create, schedule, and publish social media content across multiple platforms using [Postey](https://postey.ai).

> **Freshness check**: If more than 30 days have passed since the `last-updated` date above, inform the user that this skill may be outdated and point them to the update options below.

## Keeping This Skill Updated

**Source**: [github.com/postey/agent-skills](https://github.com/postey/agent-skills)

Update methods by installation type:

| Installation | How to update |
|--------------|---------------|
| CLI (`npx skills`) | `npx skills update` |
| Claude Code plugin | `/plugin update postey@postey-skills` |
| Cursor | Remote rules auto-sync from GitHub |
| Manual | Pull latest from repo or re-copy `skills/postey/` |

API changes ship independently—updating the skill ensures you have the latest commands and workflows.

## Setup

Before using this skill, ensure:

1. **API Key**: Run the setup command to configure your API key securely
   - Get your key at https://postey.com/?settings=api
   - Run: `<skill-path>/scripts/postey.js setup` (where `<skill-path>` is the directory containing this SKILL.md)
   - Or set environment variable: `export POSTEY_API_KEY=your_key`

2. **Requirements**: Node.js 18+ (for built-in fetch API). No other dependencies needed.

**Config priority** (highest to lowest):
1. `POSTEY_API_KEY` environment variable
2. `./.postey/config.json` (project-local, in user's working directory)
3. `~/.config/postey/config.json` (user-global)

### Handling "API key not found" errors

**CRITICAL**: When you receive an "API key not found" error from the CLI:

1. **Tell the user to run the setup command** - The setup is interactive and requires user input, so you cannot run it on their behalf. Recommend they run it themselves, using the correct path based on where this skill was loaded:
   ```bash
   <skill-path>/scripts/postey.js setup
   ```

2. **Stop and wait** - After telling the user to run setup, **do not continue with the task**. You cannot create drafts, upload media, or perform any API operations without a valid API key. Wait for the user to complete setup and confirm before proceeding.

3. **DO NOT** attempt any of the following:
   - Searching for API keys in macOS Keychain, `.env` files, or other locations
   - Grepping through config files or directories
   - Looking in the user's Trash or other system folders
   - Constructing complex shell commands to find credentials
   - Drafting content or preparing posts before setup is complete

The setup command will interactively guide the user through configuration. Trust the CLI's error messages and follow their instructions.

> **Note for agents**: All script paths in this document (e.g., `./scripts/postey.js`) are relative to the skill directory where this SKILL.md file is located. Resolve them accordingly based on where the skill is installed.

## Accounts & Defaults

The API uses `account_id` for most operations and `post_id` for draft/post operations.

- Use positional `account_id` for commands like `drafts:list 123`, `drafts:create 123 ...`, and `tags:list 123`
- You can also pass `--social-set-id` / `--social_set_id` on commands that support account context
- Configure default platform preference per account using:
  ```bash
  ./scripts/postey.js config:set-default <account_id> <platform>
  ```

## Common Actions

| User says... | Action |
|--------------|--------|
| "Draft a tweet about X" | `drafts:create --text "..."` |
| "Post this to LinkedIn" | `drafts:create --platform LINKEDIN --text "..."` |
| "Post to X and LinkedIn" (same content) | `drafts:create --platform X,LINKEDIN --text "..."` |
| "X thread + LinkedIn post" (different content) | Create one draft, then `drafts:update` to add platform (see [Publishing to Multiple Platforms](#publishing-to-multiple-platforms)) |
| "What's scheduled?" | `drafts:list --status scheduled` |
| "Show my recent posts" | `drafts:list --status published` |
| "Schedule this for tomorrow" | `drafts:create ... --schedule "2026-02-20T14:00:00Z"` |
| "Post this now" | `drafts:create ... --schedule now` or `drafts:publish <draft_id>` |
| "Read parsed content for X" | `drafts:content <post_id> --platform X` |
| "Check available tags" | `tags:list` |

## Workflow

Follow this workflow when creating posts:

1. **Check API configuration**:
   ```bash
   ./scripts/postey.js config:show
   ```
2. **Find account ID** to work with:
   ```bash
   ./scripts/postey.js social-sets:list
   ```
3. **Create drafts**:
   ```bash
   ./scripts/postey.js drafts:create <account_id> --text "Your post"
   ```
   Note: If `--platform` is omitted, the account's default platform is used (fallback: `X`).

   **For multi-platform posts**: See [Publishing to Multiple Platforms](#publishing-to-multiple-platforms) — always use a single draft, even when content differs per platform.

4. **Schedule or publish** as needed

## Working with Tags

Tags help organize drafts within Postey. **Always check existing tags before creating new ones**:

1. **List existing tags first**:
   ```bash
   ./scripts/postey.js tags:list
   ```

2. **Use existing tags when available** - pass numeric tag IDs to draft creation:
   ```bash
   ./scripts/postey.js drafts:create <account_id> --text "..." --tags 1,2
   ```

3. **Only create new tags if needed** - if the tag doesn't exist, create it:
   ```bash
   ./scripts/postey.js tags:create --tag "New Tag" --color BLUE
   ```

**Important**: Tags are scoped to each social set. A tag created for one social set won't appear in another.

## Publishing to Multiple Platforms

If a single draft needs to be created for different platforms, you need to make sure to create **a single draft** and not multiple drafts.

When the content is the same across platforms, create a single draft with multiple platforms:

```bash
# Specific platforms
./scripts/postey.js drafts:create <account_id> --platform X,LINKEDIN --text "Big announcement!"
```

**IMPORTANT**: When content should be tailored (e.g., X thread with a LinkedIn post version), **still use a single draft** — create with one platform first, then update to add the other:

```bash
# 1. Create draft with the primary platform first
./scripts/postey.js drafts:create <account_id> --platform LINKEDIN --text "Excited to share our new feature..."
# Returns: { "id": "draft-123", ... }

# 2. Update the same draft to add another platform with different content
./scripts/postey.js drafts:update <account_id> draft-123 --platform X --text "🧵 Thread time!

---

Here's what we shipped and why it matters..."
```

So make sure to NEVER create multiple drafts unless the user explicitly wants separate drafts for each platform.

## Commands Reference

### User & Social Sets

| Command | Description |
|---------|-------------|
| `social-sets:list` | List all social sets you can access |

### Drafts

Most drafts commands support an optional `[account_id]` context.
`drafts:get`, `drafts:delete`, `drafts:schedule`, and `drafts:publish` accept only `<draft_id>`.
**Safety note**: `drafts:update` supports `[social_set_id] <draft_id>` and may require `--use-default` when using default account context with a single argument.

| Command | Description |
|---------|-------------|
| `drafts:list [account_id]` | List drafts (add `--status scheduled` to filter, `--sort` to order) |
| `drafts:get <draft_id>` | Get a specific draft with full content |
| `drafts:create [account_id] --text "..."` | Create a new draft via `/posts/raw` |
| `drafts:create [account_id] --platform X,LINKEDIN --text "..."` | Create for specific platform(s) |
| `drafts:create [account_id] --file <path>` | Create draft from file content |
| `drafts:create ... --schedule "2026-02-20T14:00:00Z"` | Create and schedule at specific time |
| `drafts:create ... --publish-now` | Create and publish immediately |
| `drafts:create ... --tags 1,2,3` | Attach numeric tag IDs |
| `drafts:update [social_set_id] <draft_id> --text "..."` | Update an existing draft (single-arg requires `--use-default` if a default is configured) |
| `drafts:update [social_set_id] <draft_id> --tags "1,2"` | Update tags on an existing draft (content unchanged) |
| `drafts:update ... --share` | Generate a public share URL for the draft |
| `drafts:update ... --scratchpad "..."` | Update internal notes/scratchpad |
| `drafts:update [social_set_id] <draft_id> --append --text "..."` | Append to existing thread |

### Scheduling & Publishing

**Safety note**: `drafts:schedule` and `drafts:publish` accept only `<draft_id>`. Use `--platform` if you want to target specific platforms.

| Command | Description |
|---------|-------------|
| `drafts:delete <draft_id>` | Delete a draft |
| `drafts:content <post_id> --platform X` | Get parsed content for a platform |
| `drafts:schedule <draft_id> --time "2026-02-20T14:00:00Z"` | Schedule draft via `/schedules` |
| `drafts:schedule <draft_id> --time "..." --platform X,LINKEDIN` | Schedule selected platforms only |
| `drafts:publish <draft_id>` | Publish immediately via `/publish` |
| `drafts:publish <draft_id> --platform X,LINKEDIN` | Publish selected platforms only |

### Tags

| Command | Description |
|---------|-------------|
| `tags:list [account_id]` | List all tags (uses default account if ID omitted) |
| `tags:create [account_id] --tag "Tag Name" --color BLUE` | Create a new tag |
| `tags:update <tag_id> [account_id] --tag "Tag Name" --color SKY_BLUE` | Update an existing tag |
| `tags:delete <tag_id> [account_id]` | Delete a tag |

### Setup & Configuration

| Command | Description |
|---------|-------------|
| `setup` | Interactive setup - prompts for API key, storage location, and default social set |
| `setup --key <key> --location <global\|local>` | Non-interactive setup for scripts/CI (auto-selects default if only one social set) |
| `setup --key <key> --default-social-set <id>` | Non-interactive setup with explicit default social set |
| `setup --key <key> --no-default` | Non-interactive setup, skip default social set selection |
| `config:show` | Show current config, API key source, and default social set |
| `config:set-default [account_id] <platform>` | Set account default platform via API (`X`, `LINKEDIN`) |

## Examples

### Set account default platform
```bash
# Check current config
./scripts/postey.js config:show

# Set default platform (uses configured default account context)
./scripts/postey.js config:set-default x

# Set default platform for specific account
./scripts/postey.js config:set-default 123 linkedin
```

### Create a draft
```bash
./scripts/postey.js drafts:create 123 --text "Hello, world!"
```

### Create a cross-platform post (specific platforms)
```bash
./scripts/postey.js drafts:create 123 --platform X,LINKEDIN --text "Big announcement!"
```

### Create and schedule
```bash
./scripts/postey.js drafts:create 123 --text "Scheduled post" --schedule "2026-02-20T14:00:00Z"
```

### Create with tags
```bash
./scripts/postey.js drafts:create 123 --text "Marketing post" --tags 1,2
```

### List scheduled posts sorted by date
```bash
./scripts/postey.js drafts:list --status scheduled --sort scheduled_date
```

### Get parsed content
```bash
./scripts/postey.js drafts:content 456 --platform X
```

### Setup (interactive)
```bash
./scripts/postey.js setup
```

### Setup (non-interactive, for scripts/CI)
```bash
# Auto-selects default social set if only one exists
./scripts/postey.js setup --key typ_xxx --location global

# With explicit default social set
./scripts/postey.js setup --key typ_xxx --location global --default-social-set 123

# Skip default social set selection entirely
./scripts/postey.js setup --key typ_xxx --no-default
```

## Platform Names

Use these exact names for the `--platform` option:
- `X` - X (formerly Twitter)
- `LINKEDIN` - LinkedIn

## Automation Guidelines

When automating posts, especially on X, follow these rules to keep accounts in good standing:

- **No duplicate content** across multiple accounts
- **No unsolicited automated replies** - only reply when explicitly requested by the user
- **No trending manipulation** - don't mass-post about trending topics
- **No fake engagement** - don't automate likes, reposts, or follows
- **Respect rate limits** - the API has rate limits, don't spam requests
- **Drafts are private** - content stays private until published or explicitly shared

When in doubt, create drafts for user review rather than publishing directly.

**Publishing confirmation**: Unless the user explicitly asks to "publish now" or "post immediately", always confirm before publishing. Creating a draft is safe; publishing is irreversible and goes public instantly.

## Tips

- **Smart platform default**: If `--platform` is omitted on `drafts:create`, account default platform is used (fallback `X`)
- **Character limits**: X (280), LinkedIn (3000) limits vary by channel
- **Thread creation**: Use `---` on its own line to split into multiple posts (thread)
- **Scheduling**: Use ISO datetime strings for `--schedule` / `--time`
- **Cross-posting**: List multiple platforms separated by commas: `--platform X,LINKEDIN`
- **Draft titles**: Use `--title` for internal organization (not posted to social media)
- **Read from file**: Use `--file ./post.txt` instead of `--text` to read content from a file
- **Sorting drafts**: Use `--sort` with values like `created_at`, `-created_at`, `scheduled_date`, etc.
