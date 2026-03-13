---
name: branch-commit-pr
description: "Complete git development workflow: detect default branch, create feature branches with smart naming, make atomic commits following repo conventions, and open pull requests with GitHub Issues or Jira linking. Use when asked to 'start working on', 'create a branch', 'commit', 'open a PR', 'submit changes', or any full dev-cycle task."
license: MIT
allowed-tools: Read Write Bash Glob Grep
---

# Branch → Commit → PR

A complete git development workflow skill. Handles the entire cycle from branch creation to pull request submission.

---

## MODE DETECTION (FIRST STEP)

Analyze the user's request to determine which phase(s) to execute:

| User Request Pattern | Mode | Phases |
|---------------------|------|--------|
| "start work on X", "begin feature X" | `FULL_CYCLE` | Phase 0 → 1 → (work) → 2 → 3 |
| "create branch for X" | `BRANCH_ONLY` | Phase 0 → 1 |
| "commit", "save changes" | `COMMIT_ONLY` | Phase 0 → 2 |
| "open PR", "create pull request", "submit" | `PR_ONLY` | Phase 0 → 3 |
| "commit and PR", "finish up" | `COMMIT_AND_PR` | Phase 0 → 2 → 3 |
| "set default branch to X" | `CONFIG` | Phase 0 (override + persist) |

**If ambiguous, ask the user which phase(s) they want.**

---

## PHASE 0: Context Gathering (MANDATORY — runs before every other phase)

Execute ALL of the following in parallel:

```bash
# Group 0: User-configured default branch (highest priority)
git config --local bcp.default-branch 2>/dev/null || echo "NOT_SET"

# Group 1: Repository state
git status --porcelain
git branch --show-current
git remote -v

# Group 2: Default branch detection (if not user-configured)
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||'
git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}'

# Group 3: Branch naming conventions (sample existing branches)
git branch -r --sort=-committerdate | head -20

# Group 4: Commit style detection
git log -30 --pretty=format:"%s"

# Group 5: Upstream & PR tooling check
gh auth status 2>/dev/null
git rev-parse --abbrev-ref @{upstream} 2>/dev/null || echo "NO_UPSTREAM"
```

### 0.1 Default Branch Resolution

```
PRIORITY ORDER:
1. git config --local bcp.default-branch → user explicitly set (persistent, per-repo)
2. User says "use X as default branch" in current conversation → use + offer to persist
3. git symbolic-ref refs/remotes/origin/HEAD → auto-detect from remote
4. git remote show origin → fallback (requires network)
5. Check if 'main' or 'master' exists in remote branches → last resort
6. FAIL with clear error → ask user to set: "Which branch should I use as the base?"

TO SET/CHANGE DEFAULT BRANCH:
  git config --local bcp.default-branch <branch-name>

TO CLEAR (revert to auto-detect):
  git config --local --unset bcp.default-branch
```

**When user says "set default branch to X" or "use X as base branch":**
1. Validate that branch X exists (`git branch -r` or `git branch`)
2. Run `git config --local bcp.default-branch X`
3. Confirm: "Default branch set to X for this repo. All future branches will be created from X."

**Store as `DEFAULT_BRANCH` for all subsequent phases.**

### 0.2 Branch Naming Convention Detection

Analyze the 20 most recent remote branches:

```
PATTERNS TO DETECT:
- Conventional: feat/xxx, fix/xxx, chore/xxx → TYPE = "conventional"
- Issue-prefixed: feat/123-xxx, fix/PROJ-456-xxx → TYPE = "issue-prefixed"
- Slash-separated: feature/xxx, bugfix/xxx → TYPE = "slash-separated"
- Flat: xxx-yyy-zzz (no prefix) → TYPE = "flat"
- Custom: any other consistent pattern → TYPE = "custom"

DETECTION:
  Count branches matching each pattern.
  If any pattern >= 40% of branches → adopt that pattern.
  If no clear pattern → default to "conventional" (feat/xxx, fix/xxx).
```

### 0.3 Commit Style Detection

Analyze the 30 most recent commits:

```
DETECTION:
  semantic_count = commits matching /^(feat|fix|chore|refactor|docs|test|ci|style|perf|build)(\(.+\))?:/
  plain_count = non-semantic commits with >3 words
  short_count = commits with <=3 words

  IF semantic_count >= 50%: COMMIT_STYLE = "semantic"
  ELSE IF plain_count >= 50%: COMMIT_STYLE = "plain"
  ELSE: COMMIT_STYLE = "plain" (safe default)

LANGUAGE:
  Count Korean/CJK characters vs English-only commits.
  IF CJK >= 50%: COMMIT_LANG = "cjk"
  ELSE: COMMIT_LANG = "english"
```

### 0.4 Issue Tracker Detection

```
CHECK in order:
1. Environment variable JIRA_URL is set → JIRA_ENABLED = true
2. gh CLI authenticated → GITHUB_ISSUES_ENABLED = true
3. Neither → ISSUE_TRACKING = "none"

JIRA CONFIG (if enabled):
  JIRA_URL = $JIRA_URL (e.g. https://team.atlassian.net)
  JIRA_EMAIL = $JIRA_EMAIL
  JIRA_API_TOKEN = $JIRA_API_TOKEN
  All three must be set. If any missing → warn user, disable Jira.
```

### 0.5 MANDATORY OUTPUT

```
CONTEXT DETECTED
================
Default branch: [main | master | develop | ...] (source: user-configured | auto-detected)
Current branch: [branch-name]
Branch naming: [conventional | issue-prefixed | slash-separated | flat]
Commit style: [semantic | plain] + [english | cjk]
Issue tracking: [GitHub Issues | Jira (PROJ) | both | none]
Working directory: [clean | N files modified]
Upstream: [tracked | untracked]
gh CLI: [authenticated | not available]
```

---

## PHASE 1: Branch Management

### 1.1 Pre-flight Checks

```
ABORT IF:
- Not in a git repository
- DEFAULT_BRANCH not resolved

DIRTY WORKING DIRECTORY HANDLING (smart defaults — do NOT ask unless necessary):
- COMMIT_ONLY / COMMIT_AND_PR → Dirty is EXPECTED. Proceed directly.
- BRANCH_ONLY / FULL_CYCLE →
    1. Try: git stash → checkout DEFAULT_BRANCH → pull → checkout -b BRANCH → git stash pop
    2. If stash pop conflicts → warn user and let them resolve
    3. NEVER ask "do you want to stash?" — just do it automatically
- PR_ONLY → Changes must be committed first. Auto-stage + commit, or warn.

WARN IF:
- Already on a feature branch (not default)
  → Ask: "You're on [branch]. Create new branch from DEFAULT_BRANCH, or continue here?"
```

### 1.2 Sync Default Branch

```bash
# Always fetch latest before branching
git fetch origin $DEFAULT_BRANCH

# Switch to default branch and pull
git checkout $DEFAULT_BRANCH
git pull origin $DEFAULT_BRANCH
```

### 1.3 Generate Branch Name

Based on detected convention (Phase 0.2):

```
INPUT: User's description of the work (e.g. "add user authentication")

CONVENTIONAL:
  → feat/add-user-authentication
  → fix/null-pointer-in-login
  Prefix types: feat, fix, chore, refactor, docs, test, ci, perf

ISSUE-PREFIXED (if issue number provided):
  → feat/123-add-user-authentication
  → fix/PROJ-456-null-pointer-in-login

SLASH-SEPARATED:
  → feature/add-user-authentication
  → bugfix/null-pointer-in-login

FLAT:
  → add-user-authentication

RULES:
  - Lowercase only
  - Hyphens for spaces (no underscores, no dots)
  - Max 60 characters (truncate description, never truncate prefix)
  - Strip special characters
  - No trailing hyphens
```

### 1.4 Create and Push Branch

```bash
# Create branch from updated default
git checkout -b $BRANCH_NAME

# Set upstream immediately
git push -u origin $BRANCH_NAME
```

### 1.5 Output

```
BRANCH CREATED
==============
Branch: feat/add-user-authentication
Base: main (up to date with origin/main)
Upstream: origin/feat/add-user-authentication

Ready to work. When done, I can commit and create a PR.
```

---

## PHASE 2: Smart Commit

### 2.1 Analyze Changes

```bash
# Parallel execution
git status --porcelain
git diff --stat
git diff --staged --stat
```

```
ABORT IF:
- No changes (staged or unstaged) → "Nothing to commit."

SMART DEFAULTS (do NOT ask — just do):
- Only unstaged changes → Stage all and proceed.
- Both staged and unstaged → Commit only staged changes (respect user's intent).
- Only staged changes → Commit them directly.
```

### 2.2 Atomic Commit Planning

**HARD RULE: Multiple files → consider multiple commits.**

```
FORMULA: min_commits = ceil(changed_file_count / 4)

SPLIT BY (in priority order):
1. Different directories/modules → different commits
2. Different concerns (logic/style/config/test) → different commits
3. New files vs modifications → consider splitting
4. Implementation + its test → SAME commit (always)

COMBINE ONLY WHEN:
- Same atomic unit (function + its direct test)
- Splitting would break compilation
- Files are tightly coupled (type def + sole consumer)
```

### 2.3 Generate Commit Messages

Based on `COMMIT_STYLE` and `COMMIT_LANG` from Phase 0.3:

```
SEMANTIC + ENGLISH:
  "feat: add user authentication middleware"
  "fix: resolve null pointer in login handler"
  "refactor: extract validation logic to utils"

SEMANTIC + CJK:
  "feat: ユーザー認証ミドルウェアを追加"
  "feat: 添加用户认证中间件"

PLAIN + ENGLISH:
  "Add user authentication middleware"
  "Fix null pointer in login handler"

PLAIN + CJK:
  "ユーザー認証ミドルウェアを追加"
  "添加用户认证中间件"
```

### 2.4 Execute Commits

For each commit group, in dependency order:

```bash
# Stage files
git add <file1> <file2> ...

# Verify staging
git diff --staged --stat

# Commit
git commit -m "<message>"
```

### 2.5 Push

```bash
# If upstream is set
git push

# If no upstream yet
git push -u origin $(git branch --show-current)
```

### 2.6 Output

```
COMMITS CREATED
===============
Strategy: 3 atomic commits from 8 files

  abc1234  feat: add auth middleware (3 files)
  def5678  feat: add login/signup endpoints (3 files)
  ghi9012  test: add auth integration tests (2 files)

Pushed to origin/feat/add-user-authentication
```

---

## PHASE 3: Pull Request Creation

### 3.1 Pre-flight Checks

```
ABORT IF:
- gh CLI not authenticated → "Install and authenticate gh CLI: gh auth login"
- On default branch → "You're on the default branch. Nothing to PR."
- No commits ahead of default branch → "No new commits to create PR for."

CHECK:
- All changes committed? (git status clean)
- All commits pushed? (not ahead of origin)
  → If behind: auto-push before PR
```

### 3.2 Gather PR Content

```bash
# Commits that will be in the PR
git log --oneline $(git merge-base HEAD origin/$DEFAULT_BRANCH)..HEAD

# Full diff stat
git diff origin/$DEFAULT_BRANCH...HEAD --stat

# Detailed diff for summary generation
git diff origin/$DEFAULT_BRANCH...HEAD
```

### 3.3 Generate PR Title

Based on commit style:

```
IF single commit:
  → Use commit message as PR title

IF multiple commits, same feature:
  → Synthesize: "feat: add user authentication system"

IF multiple commits, mixed:
  → Synthesize the overarching theme

ALWAYS:
  → Match COMMIT_STYLE (semantic prefix or plain)
  → Match COMMIT_LANG
```

### 3.4 Generate PR Body

```markdown
## Summary
<2-4 bullet points describing WHAT changed and WHY>

## Changes
<Commit list with brief descriptions>
- abc1234 feat: add auth middleware
- def5678 feat: add login/signup endpoints
- ghi9012 test: add auth integration tests

## Testing
<How these changes were tested, or "Needs review">
```

### 3.5 Issue Linking

#### GitHub Issues (default)

```
IF user mentions issue number (e.g. "closes #42", "fixes #123"):
  → Add to PR body: "Closes #42"
  → Add to PR title if issue-prefixed branch naming is used

IF no issue mentioned:
  → Don't add issue references (don't guess)
```

#### Jira (optional — only if JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN are all set)

```
IF Jira is enabled AND user mentions Jira ticket (e.g. "PROJ-123"):
  → Add to PR body: "Jira: [PROJ-123]($JIRA_URL/browse/PROJ-123)"
  → Optionally transition ticket status via API:

  curl -s -X POST \
    -H "Authorization: Basic $(echo -n $JIRA_EMAIL:$JIRA_API_TOKEN | base64)" \
    -H "Content-Type: application/json" \
    "$JIRA_URL/rest/api/3/issue/PROJ-123/transitions" \
    -d '{"transition": {"id": "31"}}'

  → Only transition if user explicitly asks (e.g. "move to In Review")
  → NEVER transition without user confirmation

IF Jira enabled but no ticket mentioned:
  → Don't add Jira references (don't guess)
```

### 3.6 Create PR

```bash
gh pr create \
  --title "$PR_TITLE" \
  --body "$(cat <<'EOF'
$PR_BODY
EOF
)" \
  --base $DEFAULT_BRANCH
```

Optional flags based on context:
```bash
--draft          # If user says "draft PR" or "WIP"
--reviewer USER  # If user specifies reviewers
--assignee USER  # Auto-assign to current user if desired
--label LABEL    # If user specifies labels
```

### 3.7 Output

```
PULL REQUEST CREATED
====================
Title: feat: add user authentication system
URL: https://github.com/org/repo/pull/42
Base: main ← feat/add-user-authentication
Commits: 3
Status: Open

Issues linked:
  - Closes #15 (GitHub)
  - PROJ-123 (Jira)

Next: Waiting for review. Use 'gh pr view 42' to check status.
```

---

## FULL CYCLE EXAMPLE

When user says "Start working on adding dark mode (closes #28)":

```
1. PHASE 0: Detect context
   → Default branch: main, Branch style: conventional, Commit style: semantic

2. PHASE 1: Create branch
   → git fetch origin main
   → git checkout main && git pull
   → git checkout -b feat/add-dark-mode
   → git push -u origin feat/add-dark-mode

3. [User works on code with agent assistance]

4. PHASE 2: Commit changes
   → Analyze: 6 files changed across components/ and styles/
   → Commit 1: "feat: add dark mode toggle component" (3 files)
   → Commit 2: "feat: add dark theme CSS variables" (2 files)
   → Commit 3: "test: add dark mode toggle tests" (1 file)
   → git push

5. PHASE 3: Create PR
   → Title: "feat: add dark mode support"
   → Body with summary, commit list, "Closes #28"
   → gh pr create ...
   → Return PR URL
```

---

## CONFIGURATION OVERRIDE

Users can override detected conventions by stating preferences:

```
"Use conventional commits" → COMMIT_STYLE = "semantic"
"Branch name should be feature/xxx" → BRANCH_STYLE = "slash-separated"
"Default branch is develop" → DEFAULT_BRANCH = "develop"
"Link to PROJ-456" → Add Jira reference
```

**Always prefer explicit user instructions over auto-detection.**

---

## ERROR HANDLING

| Error | Recovery |
|-------|----------|
| `git push` rejected (behind remote) | `git pull --rebase origin $BRANCH` then retry push |
| Merge conflict during rebase | Show conflicts, ask user to resolve, then `git rebase --continue` |
| `gh` not authenticated | Print: `Run 'gh auth login' to authenticate` |
| No remote configured | Print: `Run 'git remote add origin <url>'` |
| Branch already exists | Ask: "Branch X exists. Switch to it, or create X-2?" |
| PR already exists for branch | Show existing PR URL, ask if user wants to update it |
| Jira API fails | Warn and continue without Jira linking (non-blocking) |
| Dirty working directory | Smart default: auto-stash for branch ops, proceed for commit ops (see Phase 1.1) |

---

## PLATFORM ADAPTATION

This skill is model-agnostic. It works with any AI coding agent that has shell access.

### Claude Code
Native support. Install via:
```bash
claude install-skill https://github.com/anthropics/personage/tree/main/commit_pr
```
Or add `SKILL.md` to your project's `.claude/skills/` directory.

### OpenAI Codex
Add `SKILL.md` content to your Codex system prompt or project instructions:
```bash
# In your repo, reference it as agent instruction
cp SKILL.md .codex/instructions/branch-commit-pr.md
```
Or paste the content into Codex's "Instructions" field in the UI.

### Cursor
Add as a project-level rule:
```bash
cp SKILL.md .cursor/rules/branch-commit-pr.mdc
```
Prefix the file with frontmatter to control activation:
```yaml
---
description: Git workflow — branch, commit, PR
globs:
alwaysApply: false
---
```

### Windsurf
Add to workspace rules:
```bash
cp SKILL.md .windsurf/rules/branch-commit-pr.md
```

### Gemini CLI
Reference in your `GEMINI.md` or project instructions:
```markdown
<!-- In GEMINI.md -->
Follow the workflow defined in .gemini/skills/branch-commit-pr.md
```

### Other Agents (Cline, Aider, etc.)
Most agents support custom system prompts. The general approach:
1. Copy `SKILL.md` into the agent's instruction/rules directory
2. Or paste content into the agent's system prompt configuration
3. Ensure the agent has `git` and `gh` CLI access in its shell

### Cross-Model Tips
- **Be explicit over implicit** — this skill uses concrete defaults ("auto-stash and proceed") rather than open-ended questions, which ensures consistent behavior across models of varying capability.
- **Bash is the universal interface** — all operations use standard `git` and `gh` commands. No model-specific APIs or tool names are required.
- **Structured format aids weaker models** — decision tables and numbered steps reduce ambiguity compared to prose instructions.

---

## ANTI-PATTERNS (NEVER DO)

1. **NEVER** create a branch without fetching latest default branch first
2. **NEVER** force-push without explicit user request
3. **NEVER** guess issue numbers — only link what user explicitly mentions
4. **NEVER** transition Jira tickets without user confirmation
5. **NEVER** commit with empty message or generic "update" message
6. **NEVER** create PR from default branch
7. **NEVER** push to default branch directly
8. **NEVER** delete branches without asking
9. **NEVER** make a single commit from 5+ unrelated files — split atomically
10. **NEVER** skip the context gathering phase — conventions matter
