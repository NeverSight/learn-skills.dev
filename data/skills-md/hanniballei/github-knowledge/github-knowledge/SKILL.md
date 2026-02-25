---
name: github-knowledge
description: |
  GitHub knowledge base manager for storing, indexing, and querying GitHub repositories locally.
  Maintains a BASE.md index file with summaries of all saved repos.

  Trigger this skill when the user asks a question or makes a request related to:
  - A specific GitHub repository (download, query, analyze, summarize, compare)
  - GitHub issues, PRs, releases, or repository search
  - 仓库、GitHub项目、开源项目 的下载、查询、分析等操作

  Do NOT trigger for unrelated git operations (e.g., "init a local git repo", "git commit").

  Core actions:
  1. Explicit download request → require URL → clone or pull → summarize → update BASE.md
  2. Query + repo exists locally → pull → maybe update summary → answer question
  3. Query + repo NOT local → search GitHub via gh/curl → answer question (do NOT clone)
---

# GitHub Knowledge

## Reading the Knowledge Base Path

At the start of every operation, read the configured path:

```bash
GITHUB_KNOWLEDGE_PATH=$(printenv GITHUB_KNOWLEDGE_PATH 2>/dev/null \
  || bash -c 'source ~/.bashrc 2>/dev/null; source ~/.zshrc 2>/dev/null; echo $GITHUB_KNOWLEDGE_PATH')
echo "$GITHUB_KNOWLEDGE_PATH"
```

If empty, ask the user for their desired storage path, then guide them to configure it:

- **bash / zsh**: add to `~/.bashrc` or `~/.zshrc`:
  ```bash
  export GITHUB_KNOWLEDGE_PATH=/path/chosen/by/user
  ```
  Then reload: `source ~/.bashrc`

- **fish**: add to `~/.config/fish/config.fish`:
  ```fish
  set -x GITHUB_KNOWLEDGE_PATH /path/chosen/by/user
  ```
  Then reload: `source ~/.config/fish/config.fish`

---

## Intent Decision Tree

**Determine user intent before taking any action.**

```
User asks about github/repo/仓库?
│
├─ Intent: explicitly download/clone/save a repo?  ──→ [Download Flow]
│   (keywords: 下载, clone, 保存, 收藏, 加入知识库)
│
└─ Intent: ask about / query a repo?               ──→ [Query Flow]
    (keywords: 怎么用, 介绍, 有什么issue, 看看, 了解, 搜索)
```

---

## Download Flow

### 1. Require a repo URL

The user **must** provide a full GitHub URL before cloning. If not given, ask:

> "请提供要下载的 GitHub 仓库链接（格式：https://github.com/owner/repo）"

Do not proceed until a URL is confirmed.

### 2. Resolve owner and repo name

```bash
OWNER=$(echo "$REPO_URL" | awk -F'/' '{print $4}')
REPO=$(echo "$REPO_URL" | awk -F'/' '{print $5}')
LOCAL_PATH="$GITHUB_KNOWLEDGE_PATH/$OWNER/$REPO"
```

### 3. Check if already local

```bash
[ -d "$LOCAL_PATH" ] && echo "EXISTS" || echo "NEW"
```

### 4a. New repo → Clone

For large repos use `--depth 1` to save time and disk space; omit for smaller repos where full history is useful:

```bash
mkdir -p "$GITHUB_KNOWLEDGE_PATH/$OWNER"
git clone --depth 1 "$REPO_URL" "$LOCAL_PATH"
```

**If clone fails:**
- Print the error message to the user
- If the directory was partially created, clean it up: `rm -rf "$LOCAL_PATH"`
- Common causes to mention: network issues, private repo (requires authentication), wrong URL format
- Do not proceed with summarization; ask the user to verify the URL and try again

Read the repo contents and generate a summary (see [Summarization](#summarization)).
Write a new entry to BASE.md (see [BASE.md format](references/base-md-format.md)).

### 4b. Existing repo → Pull and assess

Use the [Pull Helper](#pull-helper) with `OWNER` and `REPO` set. Then:

If skipping pull: use local files as-is.
If pull ran and there were meaningful changes (new features, major fixes, architecture changes): update the summary in BASE.md.
If only minor changes (docs, typos, deps): keep existing summary.

---

## Query Flow

### 1. Resolve the repo

Extract `owner/repo` from the user's message if provided.

If only a repo name is given (no owner), **first search BASE.md locally** before hitting GitHub API:

```bash
BASE_MD="$GITHUB_KNOWLEDGE_PATH/BASE.md"
# REPO is the name extracted from the user's message (e.g. "react" → REPO=react)
# Match all entries whose repo name (after the /) equals the given name (case-insensitive)
MATCHES=$(grep -i "## \[.*/$REPO\]" "$BASE_MD" 2>/dev/null | grep -oE '\[[^]]+\]' | tr -d '[]')
COUNT=$(echo "$MATCHES" | grep -c '[^[:space:]]' 2>/dev/null || echo 0)
```

- **0 matches** → fall back to GitHub search:
  - Run `gh search repos <name> --sort stars --limit 1` to find the most popular match
  - Use that repo and inform the user: "已使用 `owner/repo`，如需其他版本请提供完整链接"
  - If `gh` is unavailable:
    ```bash
    curl -s "https://api.github.com/search/repositories?q=<name>&sort=stars&per_page=1" \
      | python3 -c "import sys,json; r=json.load(sys.stdin)['items'][0]; print(r['full_name'])"
    ```

- **1 match** → extract `OWNER` and `REPO` from it, proceed

- **2+ matches** → ambiguous; list all matches and ask the user to clarify:

  > "本地知识库中有多个同名仓库，请指定：
  > 1. facebook/react
  > 2. some-fork/react"

  Wait for user selection before proceeding.

### 2. Check if exists locally

```bash
[ -d "$GITHUB_KNOWLEDGE_PATH/$OWNER/$REPO" ] && echo "EXISTS" || echo "NOT_FOUND"
```

### 3a. Found locally → Pull and answer

Use the [Pull Helper](#pull-helper) with `OWNER` and `REPO` set.

Read local files to answer the user's question.

Check if summary needs updating using the same criteria as Download Flow:
- Meaningful changes (new features, major fixes, architecture changes) → update BASE.md
- Minor changes (docs, typos, deps) → keep existing summary

### 3b. NOT found locally → Search GitHub and answer

Do **not** clone. Use `gh` CLI or curl to fetch information:

```bash
# With gh CLI
gh repo view owner/repo
gh search repos <query> --limit 5
gh search issues --repo owner/repo "<query>"
gh pr list --repo owner/repo --state open --limit 10

# Fallback with curl (60 req/hr unauthenticated)
curl -s "https://api.github.com/repos/owner/repo"
curl -s "https://api.github.com/search/repositories?q=<query>&per_page=5"
curl -s "https://api.github.com/repos/owner/repo/issues?state=open&per_page=10"
curl -s "https://api.github.com/repos/owner/repo/pulls?state=open&per_page=10"
```

Answer the user's question from the fetched data.

> **Rate limit note**: unauthenticated curl requests are limited to 60/hr. If you receive a `403` response, inform the user:
> "GitHub API 访问频率超限（匿名 60次/小时）。建议在 `~/.bashrc` 中配置：`export GITHUB_TOKEN=your_token`，然后在 curl 请求中加上 `-H "Authorization: Bearer $GITHUB_TOKEN"`"。
> If `GITHUB_TOKEN` is already set in the environment, always include the Authorization header in curl calls.

---

## Summarization

When generating or updating a repo summary, read in order:
1. `README.md` (primary source)
2. `docs/` directory if present
3. `package.json` / `pyproject.toml` / `Cargo.toml` for tech stack
4. Top-level source structure (`ls -la`)

Write a concise paragraph covering: what it does, the problem it solves, key technologies, and status (active/archived).

Then update BASE.md. See [BASE.md format](references/base-md-format.md).

---

## BASE.md Management

See [BASE.md format](references/base-md-format.md) for the full format specification.

Quick rule: one entry per repo, most recently updated at the top. Update in-place when refreshing; never duplicate entries.

---

## Pull Helper

Used by both Download Flow (step 5b) and Query Flow (step 3a). Requires `OWNER` and `REPO` to be set.

```bash
BASE_MD="$GITHUB_KNOWLEDGE_PATH/BASE.md"
LOCAL_PATH="$GITHUB_KNOWLEDGE_PATH/$OWNER/$REPO"
TODAY=$(date +%Y-%m-%d)
UPDATED=$(grep -A3 "## \[$OWNER/$REPO\]" "$BASE_MD" 2>/dev/null | grep "^\*\*Updated\*\*" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')

if [ "$UPDATED" = "$TODAY" ]; then
  echo "SKIP_PULL: already up-to-date today"
else
  cd "$LOCAL_PATH"
  IS_SHALLOW=$(git rev-parse --is-shallow-repository 2>/dev/null)
  if [ "$IS_SHALLOW" = "true" ]; then
    git pull --depth 1
  else
    git pull
  fi
  git log --oneline -20
fi
```

- If `SKIP_PULL`: use local files as-is
- If pull ran: inspect `git log` output to decide if the summary needs updating
