---
name: tooyoung:gh-star-list
description: "Automatically categorize GitHub starred repositories into GitHub Lists using AI analysis. Supports full batch mode and selective mode (specific repos or latest N stars). Use when the user wants to organize, categorize, sort, or clean up their GitHub stars, or manage GitHub Lists. Trigger phrases include 'organize my stars', 'categorize stars', '整理 stars', 'stars 分类', 'gh-star-list'."
metadata:
  version: "1.0.0"
---

# GitHub Star List

Organize GitHub starred repos into GitHub Lists automatically.

## Prerequisites

Verify environment before starting. Run these checks and guide user through any failures:

```bash
# 1. Check gh CLI installed
gh --version || echo "MISSING"

# 2. Check gh authenticated with 'user' scope
gh auth status  # must show 'user' in scopes

# 3. Check jq installed
jq --version || echo "MISSING"
```

**Troubleshooting:**

| Problem              | Solution                                                                 |
| -------------------- | ------------------------------------------------------------------------ |
| `gh` not installed   | macOS: `brew install gh`. Others: <https://cli.github.com>               |
| `gh` not logged in   | `gh auth login -h github.com -p https -w` (opens browser)                |
| `user` scope missing | `gh auth refresh -s user -h github.com`                                  |
| `jq` not installed   | macOS: `brew install jq`. Others: <https://jqlang.github.io/jq/download> |

All checks must pass before proceeding. The `user` scope is required for GitHub Lists API access.

## Scripts

All scripts are in `scripts/` relative to this skill's directory.

| Script            | Purpose                                                            |
| ----------------- | ------------------------------------------------------------------ |
| `fetch_stars.sh`  | Fetch starred repos (paginated). Outputs one JSON object per line. |
| `manage_lists.sh` | CRUD for GitHub Lists: `get`, `create`, `delete`, `add`            |

## Modes

### Mode 1: Full Batch (default)

Categorize all starred repos at once. Trigger: "整理所有 stars", "organize all my stars".

### Mode 2: Selective

Categorize specific repos or the latest N stars. Trigger: "整理最近 10 个 star", "把 xxx/yyy 加到合适的 list".

When no specific repos are mentioned and user says "整理一下" without "所有/全部/all", default to **latest 10 stars**.

## Workflow

### Step 1: Fetch Data

**Full batch mode:**

```bash
bash scripts/fetch_stars.sh > /tmp/stars.jsonl
bash scripts/manage_lists.sh get > /tmp/lists.json
```

**Selective mode (latest N):**

```bash
bash scripts/fetch_stars.sh --limit N > /tmp/stars.jsonl
bash scripts/manage_lists.sh get > /tmp/lists.json
```

For specific repos, use `gh api` to fetch individual repo info:

```bash
gh api repos/{owner}/{repo} --jq '{id: .node_id, full_name: .full_name, description: (.description // ""), topics: (.topics // []), language: (.language // ""), url: .html_url}'
```

Tell user how many stars to process and how many existing lists found.

### Step 2: Analyze and Propose Categories

Read `/tmp/stars.jsonl` and `/tmp/lists.json`.

Analyze all repos and existing lists. Propose a categorization plan.

#### Classification Principles (IMPORTANT)

1. **Classify by PURPOSE, not language** (unless the user explicitly requests language-based grouping): A Rust-written JS bundler belongs in "Build & DX", not "Rust". A Swift-written clipboard tool belongs in "CLI & Tools", not "iOS". Language is metadata, not category.
2. **Description > Topics > Name > Language**: Prioritize description to understand what the repo DOES. Language is the weakest signal and should only be used as a tiebreaker.
3. **Ask "what does this repo help the user DO?"**: A framework for building mobile apps → Mobile. A linter for Python → Build & DX. A deepfake tool → AI or Misc.
4. **Avoid over-broad categories**: If a list exceeds 40 items, consider splitting by sub-purpose.
5. **Framework vs Library vs Tool**: Web frameworks (Express, Hono, Koa) → Backend. UI component libraries (Ant Design, shadcn) → UI & Design. Build tools (Vite, Rspack) → Build & DX.

#### Recommended Categories

Use these as a starting template for full batch mode. Adjust based on user's actual star composition — skip empty categories, merge small ones, split large ones (>40 repos).

| Category           | Description                                          | Typical repos                       |
| ------------------ | ---------------------------------------------------- | ----------------------------------- |
| AI                 | LLMs, ML frameworks, AI apps, agents                 | langchain, ollama, stable-diffusion |
| React              | React ecosystem: frameworks, hooks, state management | next.js, react, zustand             |
| React Native       | React Native core, navigation, UI libs               | react-navigation, expo              |
| Vue                | Vue ecosystem: frameworks, plugins, tools            | nuxt, vueuse, element-plus          |
| Flutter            | Flutter/Dart packages and apps                       | flutter, riverpod                   |
| Mobile Native      | iOS/Android native development                       | Kotlin/Swift libs, Jetpack          |
| WeChat             | Mini programs, WeChat SDK, WePY                      | wepy, vant-weapp                    |
| Backend            | Server frameworks, databases, APIs                   | express, fastapi, prisma            |
| Build & DX         | Bundlers, linters, dev tools, monorepo               | vite, eslint, turborepo             |
| CLI & Tools        | Desktop apps, CLI utilities, productivity            | homebrew, raycast, warp             |
| UI & Design        | Component libraries, CSS, animation                  | tailwindcss, shadcn, framer-motion  |
| Network & Proxy    | HTTP clients, proxies, VPN, network tools            | clash, axios, nginx                 |
| DevOps & Docker    | CI/CD, containers, infra, monitoring                 | docker, k8s, terraform              |
| Low-Code & Admin   | Admin panels, low-code platforms, CMS                | strapi, appsmith, refine            |
| Awesome & Learning | Curated lists, tutorials, books, courses             | awesome-xxx, free-programming-books |
| Misc               | Repos that don't fit elsewhere                       |                                     |

#### Category Guidelines

- **Respect existing lists**: Keep lists that already have items. Prefer assigning to existing lists when they match.
- **Generate new categories**: Only for repos that don't fit any existing list.
- **Total lists cap**: Stay within GitHub's 32-list limit.
- **Full batch**: Target 15-25 total lists.
- **Selective**: Prefer assigning to existing lists; only propose new lists if truly needed.

Present the plan as a table. Wait for user confirmation or adjustments.

### Step 3: Execute

After user confirms:

1. Create new lists: `bash scripts/manage_lists.sh create "<name>" "<description>"`
2. Collect all list IDs (existing + new)
3. Add repos to lists: `bash scripts/manage_lists.sh add <repo_node_id> <list_id>`

**Critical**: The `add` command calls `updateUserListsForItem` which **replaces** all list memberships for a repo. The `listIds` param is the **complete** set of lists the repo should belong to. To preserve existing membership, include ALL list IDs (old + new) in a single call.

Full batch: process in batches, report progress every 50 repos.
Selective: process all at once.

### Step 4: Summary

Run `bash scripts/manage_lists.sh get` and present a summary table showing list name, repo count, and whether each list is new or existing.
