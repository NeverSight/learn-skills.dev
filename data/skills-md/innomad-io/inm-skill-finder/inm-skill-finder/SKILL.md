---
name: inm-skill-finder
description: "Search and install Claude Code skills from multiple sources (skills.sh leaderboard, GitHub repositories like awesome-claude-skills and anthropics/skills). Use when user wants to find, discover, search, browse, or install Claude Code skills, plugins, or extensions. Supports non-English keywords through automatic translation."
disable-model-invocation: true
allowed-tools: Bash, WebSearch, WebFetch, Read, Write, Glob, Grep, AskUserQuestion, Task
argument-hint: [search keywords]
---

# Skill Finder

Search and install Claude Code skills from multiple sources.

## Workflow

Follow these steps in order when the user invokes this skill.

### Step 1: Detect Language and Parse Keywords

Take the search keywords from `$ARGUMENTS`.

- If no keywords provided, use AskUserQuestion to ask the user what kind of skill they're looking for.
- **Detect the primary language** of the user's keywords:
  - If keywords contain CJK characters (Chinese/Japanese/Korean), primary language is CJK
  - If keywords contain non-ASCII characters (e.g., Spanish, French, German), detect that language
  - Otherwise, primary language is English
- **Store the detected language** for later use in result presentation (Step 3)
- If keywords are **not in English**, translate them to English while keeping the originals. Generate 2-4 English keyword variants for broader matching.
  - Example: "数据库管理" → detected: Chinese → keywords: ["database", "db", "management", "sql"]
  - Example: "文件处理" → detected: Chinese → keywords: ["file", "processing", "document", "handler"]
  - Example: "Slack 通知" → detected: Chinese → keywords: ["slack", "notification", "messaging"]
- If keywords **are in English**, still consider adding 1-2 synonyms/related terms.
- Remove common stop words (automation, tool, plugin, skill) from matching but keep them for display.

### Step 2: Search Multiple Sources

Run the following searches **in parallel** to maximize speed.

#### Source A: skills.sh Leaderboard (via `skills` CLI)

Run for each primary keyword (up to 3):

```bash
npx skills find <keyword> 2>&1 | head -60
```

Parse the output to extract:
- Skill identifier: `owner/repo@skill-name`
- Install count
- URL

#### Source B: GitHub Skill Registries (via search script)

Locate and run the TypeScript search script included with this skill (runs via `npx -y bun`):

```bash
SKILL_DIR=$(find ~/.claude/skills .claude/skills -name "search_github.ts" -path "*/inm-skill-finder/*" -exec dirname {} \; 2>/dev/null | head -1)
SKILL_DIR=$(dirname "$SKILL_DIR")  # go up from scripts/ to skill root
npx -y bun run "$SKILL_DIR/scripts/search_github.ts" keyword1 keyword2 --descriptions
```

This searches all enabled registries. Registries are configured in:
- **config.yaml** (recommended) — unified YAML configuration with simplified registry format
- **registries.json** + **registries.local.json** (legacy) — still supported for backward compatibility

**Preferred: Edit config.yaml directly**

Users can simply add GitHub repo URLs to `config.yaml`:

```yaml
registries:
  - url: https://github.com/your-org/your-skills
    enabled: true
  - url: owner/repo  # Short format also works
    enabled: true
```

Copy `config.example.yaml` to `config.yaml` to get started.

**Alternative: CLI commands** (creates registries.local.json):

```bash
# List all registries and their status
npx -y bun run "$SKILL_DIR/scripts/search_github.ts" --list-registries

# Add a custom registry
npx -y bun run "$SKILL_DIR/scripts/search_github.ts" --add-registry owner/repo --name "My Skills"

# Remove a custom registry
npx -y bun run "$SKILL_DIR/scripts/search_github.ts" --remove-registry owner/repo

# Disable/enable a registry
npx -y bun run "$SKILL_DIR/scripts/search_github.ts" --disable-registry composio
npx -y bun run "$SKILL_DIR/scripts/search_github.ts" --enable-registry composio
```

If the script is not found, fall back to the `skills find` CLI command from Source A.

#### Source C: General Web Search (supplementary)

Use WebSearch to find additional skills:

```
[keyword] claude code skill site:github.com
```

Extract any GitHub repos that contain SKILL.md files and are relevant.

### Step 3: Deduplicate and Present Results

1. Merge results from all sources, removing duplicates (same skill name from same repo).
2. Sort by relevance: exact matches first, then by install count (if available), then by fuzzy score.
3. **Localize the presentation** based on the detected language from Step 1:
   - If user used **Chinese** keywords: Present UI text in Chinese (table headers, prompts, instructions)
   - If user used **other non-English** keywords: Present in that language if you can, otherwise English
   - If user used **English** keywords: Present in English (default)
   - **Skill names and descriptions** remain in their original language (typically English from GitHub)
4. Present results in a clear numbered table format:

**Example (Chinese input):**
```
## 搜索结果："数据库管理" → [database, db, management, sql]

| #  | 技能名称                    | 来源              | 安装数   | 描述                 |
|----|----------------------------|-------------------|----------|----------------------|
| 1  | postgres-automation        | skills.sh         | 5.2K     | Automate Postgres... |
| 2  | mysql-manager              | awesome-claude... | -        | MySQL management...  |
```

**Example (English input):**
```
## Search Results for: database management → [database, db, management, sql]

| #  | Skill Name                  | Source            | Installs | Description          |
|----|----------------------------|-------------------|----------|----------------------|
| 1  | postgres-automation         | skills.sh         | 5.2K     | Automate Postgres... |
| 2  | mysql-manager               | awesome-claude... | -        | MySQL management...  |
```

5. Use **AskUserQuestion** with `multiSelect: true` to let the user choose which skills to install.
   - List top 4 options (or fewer if less results)
   - Each option: `"[name] (from [source])"`
   - Question text should be localized based on detected language

### Step 4: Check User Preferences and Ask Installation Options

**FIRST: Check if user has predefined preferences in config.yaml:**

```bash
SKILL_DIR=$(find ~/.claude/skills .claude/skills -name "search_github.ts" -path "*/inm-skill-finder/*" -exec dirname {} \; 2>/dev/null | head -1)
SKILL_DIR=$(dirname "$SKILL_DIR")
PREFS=$(npx -y bun run "$SKILL_DIR/scripts/search_github.ts" --show-preferences 2>/dev/null)
```

Parse the JSON output to extract `install_method` and `install_location`:
- If `install_method` is **not** 'ask': Use that method directly, skip Question 1
- If `install_location` is **not** 'ask': Use that location directly, skip Question 2
- If both are 'ask' or undefined: Ask both questions

**If questions are needed**, use **AskUserQuestion** and localize based on detected language from Step 1:

**Question 1 - Installation Method** (ask only if preference is 'ask'):
- **`npx skills add` (Recommended)** — Uses the skills.sh CLI tool. Easiest and most standard method. Works for skills.sh listings and GitHub repos.
- **Direct download** — Downloads SKILL.md (and supporting files) directly via curl. Lightweight, no extra tools needed.
- **`git clone`** — Clones the full repository, then copies the skill directory. Best for skills with many supporting files.

**Question 2 - Installation Level** (ask only if preference is 'ask'):
- **Project-level (Recommended)** — Installs to `.claude/skills/` in the current project. Only available in this project.
- **User-level (global)** — Installs to `~/.claude/skills/`. Available across all your projects.

**Example localized questions (Chinese):**
- Question 1: "选择安装方式" with options like "npx skills add（推荐）", "直接下载", "git clone"
- Question 2: "选择安装级别" with options like "项目级别（推荐）", "用户级别（全局）"

### Step 5: Execute Installation

Based on user choices, execute the appropriate installation command.

#### Method: `npx skills add`

```bash
# For skills.sh listings (owner/repo@skill format):
npx skills add owner/repo --skill skill-name          # project-level
npx skills add owner/repo --skill skill-name -g        # user-level (global)

# For standalone repos:
npx skills add owner/repo                              # project-level
npx skills add owner/repo -g                            # user-level (global)
```

For skills from ComposioHQ/awesome-claude-skills:
```bash
npx skills add ComposioHQ/awesome-claude-skills --skill skill-name
npx skills add ComposioHQ/awesome-claude-skills --skill skill-name -g
```

#### Method: Direct Download

```bash
# Determine target directory
TARGET="$HOME/.claude/skills/SKILL_NAME"    # user-level
TARGET=".claude/skills/SKILL_NAME"          # project-level

mkdir -p "$TARGET"

# Download SKILL.md
curl -sL "RAW_SKILL_URL" -o "$TARGET/SKILL.md"

# If there are additional files (scripts/, resources/), download those too
# Check the repo for extra files first
```

#### Method: `git clone`

```bash
# Determine target directory
TARGET="$HOME/.claude/skills/SKILL_NAME"    # user-level
TARGET=".claude/skills/SKILL_NAME"          # project-level

TEMP=$(mktemp -d)
git clone --depth 1 --filter=blob:none --sparse \
  "https://github.com/OWNER/REPO.git" "$TEMP/repo"
cd "$TEMP/repo"
git sparse-checkout set "SKILL_PATH"

mkdir -p "$TARGET"
cp -r "SKILL_PATH/." "$TARGET/"
rm -rf "$TEMP"
```

### Step 6: Verify and Report

After installation:

1. Verify the SKILL.md file exists at the target location.
2. Read the installed SKILL.md and display:
   - Skill name
   - Description
   - How to invoke it (e.g., `/skill-name` or automatic invocation)
3. If `user-invocable` is not `false` in the skill's frontmatter, inform the user they can invoke it with `/skill-name`.
4. If the skill has `requires` in frontmatter (e.g., MCP servers), warn the user about prerequisites.
5. **Localize the completion message** based on the detected language from Step 1:
   - Chinese user → report in Chinese
   - Other language user → report in that language or English
   - English user → report in English

## Error Handling

- **No results found**: Suggest the user try different keywords, broader terms, or browse https://skills.sh directly.
- **GitHub API rate limit**: Advise setting `GITHUB_TOKEN` environment variable. Fall back to `skills find` CLI.
- **Installation failure**: Show the error, suggest alternative installation method.
- **Network issues**: Suggest checking internet connection and trying again.

## Notes

- The `skills` CLI (`npx skills`) is the primary tool from https://skills.sh and supports search, install, update, and removal.
- The search script uses a configurable registry system (`registries.json` + `registries.local.json`) with 7 default repos including ComposioHQ, Anthropic, VoltAgent, BehiSecc, Antigravity, and more.
- READMEs are fetched via `raw.githubusercontent.com` (no API quota consumed). If a README can't be parsed, the script falls back to the GitHub Trees API.
- Search matches against both skill names and descriptions, so searching "email" will find skills like `sendgrid-automation` whose description mentions email.
- Skills installed at project-level (`.claude/skills/`) are auto-discovered by Claude Code with live reload.
- Skills installed at user-level (`~/.claude/skills/`) work across all projects.
