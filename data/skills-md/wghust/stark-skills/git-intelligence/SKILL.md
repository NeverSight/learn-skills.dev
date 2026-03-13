---
name: git-intelligence
description: |
  AI-powered git repository analysis. Summarizes commits, generates release notes,
  analyzes PR risk, detects risky changes, and maps code impact — no installation required.
  AI 驱动的 git 仓库分析。汇总提交、生成 Release Notes、分析 PR 风险、检测高危变更、映射代码影响范围。零安装，安装即用。
triggers:
  - summarize commits
  - release notes
  - analyze PR
  - PR risk
  - code impact
  - git history
  - 提交总结
  - 发版说明
  - PR 分析
  - 代码影响
  - git 分析
---

# git-intelligence Skill

Zero-install git analysis skill. The agent runs read-only git commands directly and uses its own reasoning to produce structured reports — no CLI tools, no API keys, no compilation.

## When to Use

Activate when the user asks to:

- "Summarize commits from the last N days / this week"
- "Generate release notes between two tags"
- "Analyze this PR / branch"
- "Is this branch / PR risky?"
- "What does this branch affect?"
- "Who should review this PR?"

## Step 1 — Verify Git Repository

Before any analysis, run:

```bash
git rev-parse --git-dir
```

- If it returns a path → proceed
- If it fails → stop and tell the user: "This directory is not a git repository. Please navigate to your project root first."

## Step 2 — Intent Mapping

| User says | Capability | Go to |
|---|---|---|
| "Summarize commits" / "What changed this week?" | summarize-commits | Step 3A |
| "Release notes" / "What's in v1.3?" | release-notes | Step 3B |
| "Analyze this PR" / "Full PR review" | analyze-pr | Step 3C |
| "Is this risky?" / "Risk check" | detect-risk | Step 3D |
| "What does this branch affect?" / "Impact?" | change-impact | Step 3E |

---

## Step 3A — Summarize Commits

**Collect data:**

```bash
# Convert duration: 7d=7 days ago, 2w=14 days, 1mo=1 month
git log --since="<ISO date>" --oneline --no-merges
```

**Analyze:** Classify each commit message by keyword:
- `feat / add / new / implement / support` → **Features**
- `fix / bug / patch / resolve / hotfix` → **Fixes**
- `refactor / clean / move / rename` → **Refactor**
- `perf / optim / speed / cache` → **Performance**
- `BREAKING CHANGE` or `!:` notation → **Breaking Changes**
- Unmatched → **Features** (default)

Use your own understanding to improve on keyword matching when the meaning is clear.

**Output format:**

```markdown
## Commit Summary (since <duration>)

### Features
- <commit message>

### Fixes
- <commit message>

### Performance
- <commit message>
```

Omit empty sections. If no commits found: "No commits found since <date>."

---

## Step 3B — Release Notes

**Collect data:**

```bash
# Verify tags exist first
git rev-parse --verify refs/tags/<from>
git rev-parse --verify refs/tags/<to>

# Get commits between tags
git log <from>..<to> --oneline --no-merges
```

If a tag doesn't exist, stop and report: "Tag `<tag>` not found. Run `git tag -l` to list available tags."

**Analyze:** Same classification as Step 3A, but rewrite commit messages into user-facing language where appropriate.

**Output format:**

```markdown
## Release Notes: <from> → <to>

### Breaking Changes
- <change>

### Features
- <feature description>

### Fixes
- <fix description>

### Performance
- <improvement>
```

Omit empty sections (especially Breaking Changes).

---

## Step 3C — Analyze PR

Combines risk detection + impact analysis + reviewer suggestion.

**Collect data:**

```bash
# Auto-detect base branch
git symbolic-ref refs/remotes/origin/HEAD   # e.g. refs/remotes/origin/main → "main"
# If fails → use "master"

# Get diff statistics
git diff <base>...<branch> --numstat

# For reviewer suggestion: blame top changed files (up to 5)
git blame --porcelain -- <file>
```

**Analyze:**
1. Compute risk score (same rules as Step 3D)
2. Map changed files → logical modules (group by top 2 path segments)
3. Parse blame output → count lines per author email → take top 3 authors by blame-line count
4. If fewer than 2 blame authors found, add role fallbacks: `auth/` → "security team", `payment/` → "payments team", `infra/` → "infra team"
5. Suggest test cases based on affected modules and sensitive areas

**Output format:**

```markdown
## PR Analysis: <branch>

### Summary
<1–2 sentence description of what the branch changes>

### Impacted Modules
- <module>

### Risk Score
<🔴/🟡/🟢> <score>/10

### Suggested Reviewers
- <name or role>

### Suggested Tests
- <test scenario>
```

---

## Step 3D — Detect Risk

**Collect data:**

```bash
git symbolic-ref refs/remotes/origin/HEAD   # base branch, fallback to master
git diff <base>...<branch> --numstat
```

**Risk scoring (heuristic):**

| Condition | Points |
|---|---|
| Files changed > 50 | +3 |
| Total lines changed > 1000 | +3 |
| Sensitive folder touched: `auth/`, `payment/`, `infra/`, `middleware/`, `cache/` | +2 per folder (max +4) |
| Test files < 10% of changed files | +1 |

Start at 1. Clamp final score to [1, 10]. Add your own reasoning on top of the heuristic if the code context warrants it.

**Risk label:** `🔴` score ≥ 8 · `🟡` score 5–7 · `🟢` score ≤ 4

**Output format:**

```markdown
## Risk Assessment: <branch>

**Risk Score**: 🔴 8/10

**Reasons**:
- Large diff (1200 lines)
- Middleware module modified
- Low test coverage for changed files
```

---

## Step 3E — Change Impact

**Collect data:**

```bash
git symbolic-ref refs/remotes/origin/HEAD   # base branch, fallback to master
git diff <base>...<branch> --numstat
```

**Analyze:**
- Group files by top 2 path segments → logical module names
- Identify sensitive modules (auth, payment, infra, middleware, cache) and flag them
- Use your understanding of the codebase to infer downstream effects

**Output format:**

```markdown
## Change Impact: <branch>

### Modules Affected
- <module path> — <brief impact note>

### Potential Risks
- <risk description>
```

---

## Handling Edge Cases

| Situation | Action |
|---|---|
| No commits in range | "No commits found for this period." |
| Tag not found | Report tag name, suggest `git tag -l` |
| Branch doesn't exist | Report error from git diff, suggest `git branch -a` |
| Large diff (> 100 files) | Analyze first 100 files, note truncation |
| Empty repository | "No commits yet in this repository." |
| Detached HEAD | Use `git rev-parse HEAD` as current ref |

## Read-Only Guarantee

This skill ONLY runs read-only git commands: `git log`, `git diff`, `git blame`, `git rev-parse`, `git symbolic-ref`, `git tag`, `git show`.

It NEVER runs: `git commit`, `git checkout`, `git merge`, `git push`, `git stash`, `git reset`, `git add`.

No files are created or modified in the repository.
