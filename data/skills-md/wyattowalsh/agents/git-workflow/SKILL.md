---
name: git-workflow
description: >-
  Git operations: conventional commits, PR descriptions, branch strategy,
  conflict resolution, code archaeology, bisect. Use for git workflow tasks.
  NOT for code review, CI/CD, or changelogs.
argument-hint: "<mode> [args]"
license: MIT
model: sonnet
metadata:
  author: wyattowalsh
  version: "1.0"
---

# Git Workflow

Git operations assistant. Lightweight, high-frequency tool for commit messages, PR descriptions, branch strategy, conflict resolution, code archaeology, and bisect debugging.

**Scope:** Git workflow operations only. NOT for code review (honest-review), CI/CD pipelines (devops-engineer), changelogs or release notes (changelog-writer), or writing application code.

## Dispatch

| $ARGUMENTS | Mode |
|------------|------|
| `commit` | Generate conventional commit message from staged diff |
| `pr` | Generate PR description from branch diff |
| `strategy` | Recommend branch strategy for project |
| `conflict` | Guide merge conflict resolution |
| `archaeology <file or function>` | Analyze git history for code understanding |
| `bisect` | Assist with git bisect to find regression commits |
| Empty | Show mode menu with examples |

## Canonical Vocabulary

Use these terms exactly throughout all modes:

| Term | Definition |
|------|------------|
| **conventional commit** | Structured commit format: `type(scope): subject` per Conventional Commits 1.0 |
| **commit type** | One of: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert |
| **breaking change** | Commit with `!` suffix or `BREAKING CHANGE:` footer requiring major version bump |
| **scope** | Optional parenthesized component name after type: `feat(auth): ...` |
| **trunk-based** | Strategy where all developers commit to main/trunk with short-lived feature branches |
| **git-flow** | Strategy with develop, feature, release, and hotfix branches |
| **github-flow** | Simplified strategy: main + feature branches with PR-based merging |
| **conflict marker** | Git-inserted `<<<<<<<`, `=======`, `>>>>>>>` delimiters in conflicted files |
| **blame** | `git blame` annotation showing last modifier per line |
| **archaeology** | Using git history commands to understand why code exists |
| **bisect** | Binary search through commits to find the one introducing a bug |
| **good/bad commit** | Bisect terminology: good = before bug, bad = after bug |

## Mode 1: Commit

Generate a conventional commit message from the current staged diff.

### Commit Steps

1. Run `git diff --cached` to get staged changes
2. If nothing staged, run `git diff` and report: "No staged changes. Stage files first with `git add`."
3. Run `uv run python skills/git-workflow/scripts/diff-summarizer.py` on the diff output
4. Analyze the diff to determine:
   - **Type**: feat/fix/docs/style/refactor/perf/test/build/ci/chore/revert
   - **Scope**: affected component (from file paths, module names)
   - **Subject**: imperative, lowercase, no period, max 72 chars
   - **Body**: what changed and why (wrap at 72 chars)
   - **Breaking**: whether `BREAKING CHANGE:` footer is needed
5. Reference `data/conventional-commits.json` rules for type selection
6. Present the commit message. Ask: "Commit with this message? [yes / edit / cancel]"
7. If approved, run `git commit -m "$(cat <<'EOF'\n<message>\nEOF\n)"`

## Mode 2: PR

Generate a PR description from the branch diff against the base branch.

### PR Steps

1. Detect base branch: `git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@'` (fallback: `main`)
2. Run `git log --oneline <base>..HEAD` to list commits
3. Run `uv run python skills/git-workflow/scripts/commit-parser.py` on git log output
4. Run `git diff <base>...HEAD --stat` for change statistics
5. Run `uv run python skills/git-workflow/scripts/diff-summarizer.py` on the diff stat
6. Generate PR description with:
   - **Title**: short summary under 70 chars
   - **Summary**: 1-3 bullet points of what changed
   - **Changes**: grouped by commit type from parsed commits
   - **Test plan**: checklist of verification steps
   - **Breaking changes**: if any commits have breaking changes
7. Present the description. Ask: "Create PR with this? [yes / edit / skip]"

## Mode 3: Strategy

Recommend a branch strategy for the project.

### Strategy Steps

1. Analyze the repository:
   - Team size: check `git shortlog -sn --all | wc -l`
   - Release cadence: check tags with `git tag -l --sort=-creatordate | head -20`
   - Branch count: `git branch -r | wc -l`
   - CI/CD presence: check for `.github/workflows/`, `Jenkinsfile`, `.gitlab-ci.yml`
2. Reference `data/branch-strategies.json` for strategy comparison
3. Score each strategy against the project profile
4. Present recommendation with:
   - Recommended strategy and why
   - Comparison table showing trade-offs
   - Migration steps if switching from current approach
   - Team size and release cadence alignment

## Mode 4: Conflict

Guide merge conflict resolution.

### Conflict Steps

1. Run `git diff --name-only --diff-filter=U` to list conflicted files
2. If no conflicts: "No merge conflicts detected."
3. For each conflicted file:
   - Read the file to identify conflict markers
   - Analyze both sides (ours vs theirs)
   - Check `git log --merge -p -- <file>` for context on diverging changes
   - Determine the intent of each side
4. Present resolution guidance per file:
   - What each side changed and why
   - Recommended resolution (keep ours / keep theirs / merge both / rewrite)
   - The resolved content
5. Ask: "Apply this resolution? [yes / edit / skip per file]"
6. After resolving: remind to `git add <files>` and continue the merge/rebase

## Mode 5: Archaeology

Analyze git history to understand why code exists and how it evolved.

### Archaeology Steps

1. Parse `$ARGUMENTS[1]` as a file path or function name
2. For file paths:
   - `git log --follow --oneline -- <file>` for full history
   - `git log --follow --diff-filter=A -- <file>` for creation commit
   - `git blame <file>` for line-by-line attribution
3. For function names:
   - `git log -p --all -S '<function>' -- '*.py' '*.js' '*.ts'` (pickaxe search)
   - `git log -L :<function>:<file>` if file is known (function-level log)
4. Analyze the history to answer:
   - When was this code introduced and by whom?
   - What was the original intent? (from commit messages)
   - How has it evolved? (key modification commits)
   - Are there related changes in other files?
5. Present a narrative timeline with key commits and their context

## Mode 6: Bisect

Assist with git bisect to find the commit that introduced a regression.

### Bisect Steps

1. Ask for (if not provided):
   - **Bad commit**: where the bug exists (default: HEAD)
   - **Good commit**: where the bug did not exist
   - **Test command**: how to verify (optional, for `git bisect run`)
2. Start bisect: `git bisect start <bad> <good>`
3. If test command provided:
   - Run `git bisect run <command>`
   - Parse output for the first bad commit
4. If manual:
   - At each step, explain the current commit context
   - Ask: "Is this commit good or bad?"
   - Run `git bisect good` or `git bisect bad`
5. When bisect identifies the commit:
   - Show the full commit with `git show <hash>`
   - Explain what the commit changed
   - Suggest investigation areas
6. Clean up: `git bisect reset`

## Reference Files

Load ONE reference at a time. Do not preload all references into context.

| File | Content | Load When |
|------|---------|-----------|
| `references/commit-and-pr-guide.md` | Conventional commit patterns, PR templates, diff analysis | commit or pr mode |
| `references/branch-strategies.md` | Strategy comparison, migration paths, team sizing | strategy mode |
| `references/history-and-debugging.md` | Conflict resolution, archaeology techniques, bisect patterns | conflict, archaeology, or bisect mode |

| Data File | Content | Load When |
|-----------|---------|-----------|
| `data/conventional-commits.json` | Full spec as structured data with type definitions | commit mode (script input) |
| `data/branch-strategies.json` | Strategy comparison with pros/cons/team size | strategy mode (script input) |

| Script | When to Run |
|--------|-------------|
| `scripts/commit-parser.py` | pr mode -- parse git log into structured JSON |
| `scripts/diff-summarizer.py` | commit or pr mode -- summarize diff statistics |

## Critical Rules

1. Never commit without user approval -- always present the message first
2. Never force-push, reset --hard, or run destructive git commands
3. Always use conventional commit format per the spec in data/conventional-commits.json
4. Commit subjects must be imperative, lowercase, no period, max 72 chars
5. PR descriptions must link changes to evidence from the diff
6. Never skip `git bisect reset` after a bisect session
7. Archaeology mode is read-only -- never modify code or history
8. Conflict resolution must explain both sides before recommending
9. Branch strategy must consider actual team size and release cadence, not ideals
10. Scripts output JSON to stdout -- parse programmatically, never regex
11. Stage-before-commit: if diff --cached is empty, do not fabricate a commit message
12. Do not generate changelogs or release notes -- redirect to changelog-writer
