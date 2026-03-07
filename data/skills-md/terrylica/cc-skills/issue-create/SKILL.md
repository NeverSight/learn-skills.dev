---
name: issue-create
description: "Create well-formatted GitHub issues with intelligent AI-powered label suggestions and content type detection. Use whenever the user wants to create a bug report, feature request, question, or documentation issue on GitHub, or says 'file an issue', 'create an issue', or 'gh issue create'. Do NOT use for managing existing issues, organizing issue hierarchies (use issues-workflow instead), or for PR creation."
allowed-tools: Read, Bash, Grep, Glob
---

# Issue Create Skill

Create well-formatted GitHub issues with intelligent automation including AI-powered label suggestions, content type detection, template formatting, and related issue linking.

## When to Use This Skill

Use this skill when:

- Creating bug reports, feature requests, questions, or documentation issues
- Need AI-powered label suggestions from repository's existing taxonomy
- Want automatic duplicate detection and related issue linking
- Need consistent issue formatting across different repositories

## Invocation

**Slash command**: `/gh-tools:issue-create`

**Natural language triggers**:

- "Create an issue about..."
- "File a bug for..."
- "Submit a feature request..."
- "Report this problem to..."
- "Post an issue on GitHub..."

## Features

### 1. Repository Detection

- Auto-detects repository from current git directory
- Supports explicit `--repo owner/repo` flag
- Checks permissions before attempting to create

### 2. Content Type Detection

- AI-powered detection (gpt-4.1 via gh-models)
- Fallback to keyword matching
- Types: Bug, Feature, Question, Documentation

### 3. Title Extraction

- Extracts informative title from content
- Adds type prefix (Bug:, Feature:, etc.)
- **Maximizes GitHub's 256-character limit** for informative titles

### 4. Template Formatting

- Auto-selects template based on content type
- Bug: Steps to reproduce, Expected/Actual behavior
- Feature: Use case, Proposed solution
- Question: Context, What was tried
- Documentation: Location, Suggested change

### 5. Label Suggestion

- Fetches repository's existing labels
- AI suggests 2-4 relevant labels
- Only suggests labels that exist (taxonomy-aware)
- 24-hour cache for performance

### 6. Related Issues

- Searches for similar issues
- Links related issues in body
- Warns about potential duplicates

### 7. Preview & Confirm

- Full preview before creation
- Dry-run mode available
- Edit option for modifications

## Usage Examples

### Basic Usage

```bash
# From within a git repository
bun ~/eon/cc-skills/plugins/gh-tools/scripts/issue-create.ts \
  --body "Login page crashes when using special characters in password"
```

### With Explicit Repository

```bash
bun ~/eon/cc-skills/plugins/gh-tools/scripts/issue-create.ts \
  --repo owner/repo \
  --body "Feature: Add dark mode support for better accessibility"
```

### Dry Run (Preview Only)

```bash
bun ~/eon/cc-skills/plugins/gh-tools/scripts/issue-create.ts \
  --repo owner/repo \
  --body "Bug: API returns 500 error" \
  --dry-run
```

### With Custom Title and Labels

```bash
bun ~/eon/cc-skills/plugins/gh-tools/scripts/issue-create.ts \
  --repo owner/repo \
  --title "Bug: Login fails with OAuth" \
  --body "Detailed description..." \
  --labels "bug,authentication"
```

### Disable AI Features

```bash
bun ~/eon/cc-skills/plugins/gh-tools/scripts/issue-create.ts \
  --body "Question: How to configure..." \
  --no-ai
```

## CLI Options

| Option      | Short | Description                     |
| ----------- | ----- | ------------------------------- |
| `--repo`    | `-r`  | Repository in owner/repo format |
| `--body`    | `-b`  | Issue body content (required)   |
| `--title`   | `-t`  | Issue title (optional)          |
| `--labels`  | `-l`  | Comma-separated labels          |
| `--dry-run` |       | Preview without creating        |
| `--no-ai`   |       | Disable AI features             |
| `--verbose` | `-v`  | Enable verbose output           |
| `--help`    | `-h`  | Show help                       |

## Dependencies

- `gh` CLI (required) - GitHub CLI tool
- `gh-models` extension (optional) - Enables AI features

### Installing gh-models

```bash
gh extension install github/gh-models
```

## Permission Handling

| Level       | Behavior                                |
| ----------- | --------------------------------------- |
| WRITE/ADMIN | Full functionality                      |
| TRIAGE      | Can apply labels                        |
| READ        | Shows formatted content for manual copy |
| NONE        | Suggests fork workflow                  |

## Logging

Logs to: `~/.claude/logs/gh-issue-create.jsonl`

Events logged:

- `preflight` - Initial checks
- `type_detected` - Content type detection
- `labels_suggested` - Label suggestions
- `related_found` - Related issues search
- `issue_created` - Successful creation
- `dry_run` - Dry run completion

## Related Documentation

- [Content Types Reference](./references/content-types.md)
- [Label Strategy Reference](./references/label-strategy.md)
- [AI Prompts Reference](./references/ai-prompts.md)

## Embedding Images in Issues

GitHub Issues have **no API for programmatic image upload**. The web UI's drag-and-drop uses an internal S3 policy flow that is intentionally not exposed to API clients ([cli/cli#1895](https://github.com/cli/cli/issues/1895)).

### Preflight: Ensure Images Are Reachable

The `?raw=true` URL resolves via `github.com` — if the image doesn't exist at that path on the remote, it silently 404s (broken image, no error). **Run this preflight before creating the issue:**

```bash
# 1. Detect repo context
OWNER_REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
BRANCH=$(git rev-parse --abbrev-ref HEAD)
VISIBILITY=$(gh repo view --json visibility -q '.visibility')

# 2. Verify images are git-tracked (not gitignored)
IMG_DIR="path/to/images"
for f in ${IMG_DIR}/*.png; do
  git ls-files --error-unmatch "$f" >/dev/null 2>&1 \
    || echo "WARNING: $f is NOT tracked by git (check .gitignore)"
done

# 3. Verify images are committed (not just staged or untracked)
UNCOMMITTED=$(git diff --name-only HEAD -- "${IMG_DIR}/" 2>/dev/null)
UNTRACKED=$(git ls-files --others --exclude-standard -- "${IMG_DIR}/" 2>/dev/null)
if [[ -n "$UNCOMMITTED" || -n "$UNTRACKED" ]]; then
  echo "FAIL: Images not committed — commit and push first"
  echo "  Uncommitted: ${UNCOMMITTED}"
  echo "  Untracked:   ${UNTRACKED}"
  exit 1
fi

# 4. Verify commit is pushed to remote (local commits invisible to github.com)
LOCAL_SHA=$(git rev-parse HEAD)
REMOTE_SHA=$(git rev-parse "origin/${BRANCH}" 2>/dev/null)
if [[ "$LOCAL_SHA" != "$REMOTE_SHA" ]]; then
  echo "FAIL: Local commits not pushed — run: git push origin ${BRANCH}"
  exit 1
fi

# 5. Build image base URL
IMG_BASE="https://github.com/${OWNER_REPO}/blob/${BRANCH}/${IMG_DIR}"
echo "Image base URL: ${IMG_BASE}/<filename>.png?raw=true"
echo "Repo visibility: ${VISIBILITY}"
if [[ "$VISIBILITY" == "PRIVATE" ]]; then
  echo "NOTE: Images only visible to authenticated collaborators"
fi
```

**Preflight checklist** (what each step catches):

| Step | Check                  | Failure Mode                                     |
| ---- | ---------------------- | ------------------------------------------------ |
| 1    | Repo context exists    | No `OWNER_REPO` to build URLs                    |
| 2    | Images are git-tracked | `.gitignore` silently excludes them              |
| 3    | Images are committed   | Staged/untracked files don't exist on remote     |
| 4    | Commit is pushed       | Local-only commits are invisible to `github.com` |
| 5    | URL construction       | Wrong branch name → 404                          |

### URL Format: `?raw=true` vs `raw.githubusercontent.com`

For images already committed and pushed, use `github.com/blob/...?raw=true` URLs — **not** `raw.githubusercontent.com`:

```markdown
<!-- BROKEN for private repos (no browser cookies on raw.githubusercontent.com) -->

![img](https://raw.githubusercontent.com/owner/repo/main/path/image.png)

<!-- WORKING for all repos (browser has cookies on github.com, gets signed redirect) -->

![img](https://github.com/owner/repo/blob/main/path/image.png?raw=true)
```

**Scripting pattern** (batch images → issue body):

```bash
IMG_BASE="https://github.com/${OWNER_REPO}/blob/${BRANCH}/${IMG_DIR}"

gh issue create --title "Feedback with screenshots" --body "$(cat <<EOF
## Item 1
![description](${IMG_BASE}/01-screenshot.png?raw=true)

## Item 2
![description](${IMG_BASE}/02-screenshot.png?raw=true)
EOF
)"
```

See [AP-07 in GFM Anti-Patterns](../issues-workflow/references/gfm-antipatterns.md#ap-07-private-repo-image-urls-render-as-broken) for the full technical explanation.

### Images NOT in the Repository

For images only on disk (not committed), four options:

| Method                    | How                                                              | Permanent?                   | Preflight?   |
| ------------------------- | ---------------------------------------------------------------- | ---------------------------- | ------------ |
| **Commit + push first**   | `git add` images, push, run preflight, then use `?raw=true` URLs | Yes (repo-hosted)            | Yes (5-step) |
| **Web UI paste**          | Open issue in browser, Ctrl/Cmd+V images into comment box        | Yes (`user-attachments` CDN) | None         |
| **Web UI drag-and-drop**  | Drag image files into the comment box                            | Yes (`user-attachments` CDN) | None         |
| **Playwright automation** | Script automates the browser file-attachment flow                | Yes (`user-attachments` CDN) | None         |

#### Playwright Automation (Programmatic CDN Upload)

GitHub has no API for image uploads, but the browser's file-attachment flow can be automated via Playwright to get permanent `user-attachments` CDN URLs without any commit/push preflight.

**How it works:**

1. Playwright opens the issue page in Chromium with a persistent profile (`~/.claude/tools/pw-github-profile/`)
2. First run only: user logs in to GitHub (any method — Google SSO, passkey, password). Cookies persist.
3. Script clicks "Paste, drop, or click to add files" → intercepts the file chooser → sets the image file
4. GitHub uploads to its S3 backend and inserts an `<img>` tag with a `user-attachments` CDN URL into the comment textarea
5. Script extracts the CDN URL and clears the textarea (no comment is actually posted)

**Key implementation details** (GitHub's 2026 React comment composer):

- Comment textarea selector: `textarea[placeholder="Use Markdown to format your comment"]` (dynamic React IDs — do NOT match by `id`)
- File upload trigger: click the "Paste, drop, or click to add files" text, then intercept `page.waitForEvent("filechooser")`
- Upload result format: `<img width="W" height="H" alt="Image" src="https://github.com/user-attachments/assets/UUID" />` (HTML `<img>` tag, not `![](...)` markdown)
- Old `textarea#new_comment_field` and `file-attachment input[type='file']` selectors no longer exist
- Batch uploads: clear textarea between uploads with `textarea.fill("")`

**Chrome CDP note**: `chromium.connectOverCDP()` fails with Chrome 136+ (WebSocket timeout). Use `chromium.launchPersistentContext()` with Playwright's bundled Chromium instead. Chrome 136+ also requires `--user-data-dir` for CDP (`DevTools remote debugging requires a non-default data directory`), making CDP impractical for reusing existing browser sessions.

---

## Troubleshooting

### "No repository context"

Run from a git directory or use `--repo owner/repo` flag.

### Labels not suggested

- Check if gh-models is installed: `gh extension list`
- Verify repository has labels: `gh label list --repo owner/repo`
- Check label cache: `ls ~/.cache/gh-issue-skill/labels/`

### AI features not working

Install gh-models extension:

```bash
gh extension install github/gh-models
```
