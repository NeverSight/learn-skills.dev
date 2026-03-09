---
name: repo-explorer
description: Use this skill when the user asks to explore a repository, get familiar with a project, "repo explorer", "tell me about this repo", "repo-explorer", "what does this repository do", or wants an overview of a Gitee repository. Requires Gitee MCP Server to be configured.
version: 1.0.0
requires:
  mcp-servers:
    - gitee
---

> **Note**: If you have `mcporter` installed locally, you should use `mcporter` to invoke the MCP tool instead of directly calling the MCP tool. The `mcporter` CLI provides a more convenient interface and better error handling.

# Repo Explorer via Gitee MCP

Quickly explore the structure and core content of a Gitee repository and generate an overview report to help get up to speed on an unfamiliar project.

## Prerequisites

- Gitee MCP Server configured (tools: `get_file_content`, `search_files_by_content`, `list_user_repos`)
- User must provide: repository owner, repository name
- Optional: specific area of interest (e.g., "I want to understand the authentication mechanism")

## Steps

### Step 1: Fetch Key Documentation

Start by reading these files using `get_file_content`:

1. `README.md` or `README_CN.md`: project introduction
2. `CONTRIBUTING.md`: contribution guide (development conventions)
3. `CHANGELOG.md`: change history (evolution of the project)
4. `package.json` / `go.mod` / `pom.xml` / `requirements.txt`: tech stack and dependencies

### Step 2: Explore Project Structure

First, use `get_file_content` with `path="/"` to get the root directory tree:

```
get_file_content(owner="[owner]", repo="[repo]", path="/")
```

This returns the top-level directory structure in a single call, providing a quick overview of the project's layout.

Then, browse key subdirectories to identify:

**Common project structure patterns**
- `src/` or `lib/`: core source code
- `cmd/` or `bin/`: CLI entry points (Go / C++ projects)
- `api/` or `routes/`: API definitions
- `tests/` or `test/`: test code
- `docs/`: detailed documentation
- `scripts/` or `.gitee/` or `.github/`: build / CI scripts
- `config/` or `configs/`: configuration files

### Step 3: Analyze Core Code

Based on the project type, read key files in depth:

**Web application**
- Entry file (main.go / index.js / app.py)
- Route definition files
- Database schema or model definitions

**Library / SDK**
- Main entry file (public API entry point)
- Core algorithm files

**CLI tool**
- Command definition files
- Configuration handling logic

Use `search_files_by_content` to locate core logic:
- Search for `main`, `init`, `Router`, etc.
- Search for specific keywords matching the user's area of interest

### Step 4: Generate Repository Overview Report

```
# Repository Overview: [owner/repo]

## About
[One-paragraph description summarizing the project based on the README]

## Tech Stack
- **Language**: [primary language]
- **Framework**: [main framework]
- **Storage**: [database / cache]
- **Deployment**: [Docker / K8s / other]

## Directory Structure
[Key directory annotations]
├── src/          # Core source code
├── api/          # API definitions
├── tests/        # Tests
└── docs/         # Documentation

## Core Modules
| Module | Path | Responsibility |
|--------|------|---------------|
| [name] | [path] | [one-sentence description] |

## Data Models (if applicable)
[Main entities and their relationships]

## Getting Started
[Setup steps extracted from README / CONTRIBUTING]

\`\`\`bash
# Install dependencies
[command]

# Start the project
[command]
\`\`\`

## Contribution Highlights
[Key conventions from CONTRIBUTING.md]

## Recent Activity
[Latest version highlights from CHANGELOG or README]
```

### Step 5: Deep Dive (optional)

If the user has a specific area of interest, use `search_files_by_content` for targeted searches:
- Authentication: search `auth`, `token`, `permission`
- Database operations: search `SELECT`, `INSERT`, `Model`
- Configuration: search `config`, `env`, `ENV`

## Notes

- Prefer smaller files when reading; avoid loading very large files all at once
- Keep the report focused and concise — do not try to cover everything
- If the project has no README, infer its purpose from the code structure and comments
