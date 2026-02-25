---
name: pr
description: Create a pull request following project conventions
version: "1.1.0"
---

## Gather Context

Run the following commands to understand the current state:
1. `git log --oneline main..HEAD 2>/dev/null || git log --oneline -10` — list commits on this branch
2. `git diff main...HEAD --stat 2>/dev/null || echo "Could not determine diff"` — list changed files

If the base branch is not `main`, adjust the commands to use the correct base branch.

## Determine PR Type

Parse `$ARGUMENTS`:
- If it contains **"release"** → use the **Release PR Template** below.
- Otherwise → use the **Individual PR Template**.

---

## PR Title Convention

Format: `{Type}: {description}`

### Type Prefixes (capitalize first letter — differs from commit messages)

| Type | Purpose |
|------|---------|
| `Feat:` | New feature |
| `Fix:` | Bug fix |
| `Refactor:` | Code restructuring |
| `Perf:` | Performance improvement |
| `Docs:` | Documentation |
| `Test:` | Test changes |
| `Chore:` | Maintenance |
| `Hotfix:` | Urgent fix |
| `Release:` | Release integration (e.g., `Release: dev → main 통합 (v0.5.0)`) |

Write the description in the language configured in the project's CLAUDE.md.
If no language is configured, follow the user's conversational language.

---

## Individual PR Template

Apply this template for feature, fix, refactor, and other non-release PRs.

```markdown
## 📌 개요

{1-3 sentences: background, problem, and solution}

> ⚠️ **Breaking Change**: {only if applicable — describe migration needed}

## ✅ 변경 사항

### 1. {Change category title}

{Detailed description. Include before/after comparisons, code snippets, or diagrams where helpful.}

### 2. {Change category title}

{...}

## 📁 파일 변경 요약

| 구분 | 파일 |
|------|------|
| 추가 | `path/to/new/file.py` |
| 수정 | `path/to/modified/file.py` |
| 삭제 | `path/to/deleted/file.py` |

## 🧪 테스트

- [ ] {Test item 1}
- [ ] {Test item 2}

## 📌 관련 이슈/PR

- #{number}

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## Release PR Template

Apply this template when `$ARGUMENTS` contains "release". Typically used for `dev → main` integration.

Collect all merged PRs since the last release:
```
gh pr list --state merged --base dev --limit 30 --json number,title --jq '.[] | "- #\(.number) \(.title)"'
```

Title format: `Release: dev → main 통합 (vX.Y.Z)`

```markdown
## 📝 개요

{Release summary — what this release includes}

> ⚠️ **배포 공지**: {Deployment impact notice — which servers are affected, migration steps if any}

## ✨ 주요 변경사항

### 1. {Feature/Fix name} (#{PR number})

{Brief summary of this PR's changes}

### 2. {Feature/Fix name} (#{PR number})

{...}

## 📁 변경된 파일

| 파일 | 변경 내용 |
|------|----------|
| `file.py` | {description} |

## 🔍 테스트

- [ ] {Test checklist item}

## 📌 관련 PR

- #{number1}
- #{number2}

## 🚀 배포 정보

| 환경 | 서버 | 브랜치 |
|------|------|--------|
| 개발 | {dev server} | dev |
| 운영 | {prod server} | main |

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## Task

1. Determine PR type: Release (if `$ARGUMENTS` contains "release") or Individual.
2. Draft the PR title and body using the appropriate template above.
3. Present the proposed title and body to the user.
4. Sync check before pushing:
   - `git fetch origin {base-branch}`
   - If the local branch is behind, inform the user and suggest an appropriate action (rebase, merge, or proceed as-is).
5. Push the branch if not already pushed: `git push -u origin {branch-name}`
6. Create the PR: `gh pr create --title "..." --body "$(cat <<'EOF' ... EOF)"`
7. Return the PR URL.

**Important:**
- For Release PRs, automatically collect all included PRs from the merge history.
- Adapt section headers and content language to the project's CLAUDE.md language setting.
- The file change table should be generated from the actual diff, not guessed.
