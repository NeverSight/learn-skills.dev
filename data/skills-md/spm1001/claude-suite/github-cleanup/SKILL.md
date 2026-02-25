---
name: github-cleanup
description: Orchestrates progressive GitHub account cleanup using a 6-phase audit→approve→execute process that prevents accidental deletion. BEFORE any destructive repo action, invoke FIRST — traces Dependabot alerts to unused direct deps (prune) vs transitive-only (upgrade lock file). Triggers on 'clean up GitHub', 'audit my repos', 'Dependabot trouble', 'unused deps', 'stale forks', 'dependency audit'. Requires gh CLI. (user)
---

# Cleanup GitHub

Progressive audit and cleanup of GitHub accounts with user approval before any destructive actions.

## Overview

This skill audits a GitHub account for:
- Failing workflows and misconfigured security scanning
- Stale forks with no custom changes
- Orphaned secrets not used by any workflow
- Dependabot and security configuration
- **Dependabot alert triage** — trace alerts to source, prune unused deps, upgrade transitive deps

**Workflow:** Audit all categories → Present findings → Get approval → Execute cleanup

**Prerequisite:** `gh auth status` must pass.

## When to Use

- "clean up my GitHub" / "audit my repos"
- "check for stale forks" / "orphaned secrets"
- "GitHub hygiene" / "repo cleanup"
- "Dependabot trouble" / "fix Dependabot alerts" / "unused deps"
- Investigating failing GitHub Actions
- Periodic account maintenance

## When NOT to Use

- Creating new repos or workflows
- Managing issues or PRs
- CI/CD pipeline setup
- Repository content changes

## Execution Modes

### Full Audit (default)
Run all phases, present consolidated findings.

### Quick Check
Focus on failing workflows and obvious issues only.

```
quick check my GitHub
```

### Targeted Audit
Focus on specific category:

```
check for stale forks
check for orphaned secrets
check failing workflows
triage Dependabot alerts
audit deps across my repos
```

## Phase Workflow

### Phase 0: Prerequisites

**Verify gh CLI and detect username:**

```bash
gh auth status
GH_USER=$(gh api user --jq '.login')
echo "Auditing GitHub account: $GH_USER"
```

**Verify username matches auth:** The `GH_USER` variable can be shadowed by env vars or stale shells. Cross-check:

```bash
AUTH_USER=$(gh auth status 2>&1 | grep 'account' | awk '{print $NF}' | tr -d '()')
[ "$GH_USER" = "$AUTH_USER" ] && echo "Username verified: $GH_USER" || echo "MISMATCH: API=$GH_USER Auth=$AUTH_USER — investigate before proceeding"
```

**Count repos for expectations:**

```bash
gh repo list $GH_USER --limit 1000 --json name --jq 'length'
```

### Phase 1: Failing Workflows Audit

**List all repos with workflows:**

```bash
# Using bash to iterate (gh CLI doesn't have built-in cross-repo workflow listing)
/bin/bash -c 'for repo in $(gh repo list GH_USER --limit 100 --json name --jq ".[].name"); do
  workflows=$(gh workflow list --repo "GH_USER/$repo" 2>/dev/null)
  if [ -n "$workflows" ]; then
    echo "=== $repo ==="
    echo "$workflows"
  fi
done'
```

**Check CodeQL default setup (NOT a workflow file!):**

```bash
gh api repos/GH_USER/REPO/code-scanning/default-setup --jq '.state'
```

**Key insight:** CodeQL "default setup" is configured via GitHub Security settings, not workflow files. The API endpoint is `code-scanning/default-setup`, not `workflows`.

**Check recent workflow runs for failures:**

```bash
gh run list --repo GH_USER/REPO --limit 5 --json status,conclusion,name \
  --jq '.[] | select(.conclusion == "failure") | "\(.name): \(.conclusion)"'
```

### Phase 2: Stale Forks Audit

**List all forks:**

```bash
gh repo list GH_USER --fork --json name,parent --jq '.[] | "\(.name) (fork of \(.parent.nameWithOwner // "unknown"))"'
```

**Compare fork to upstream:**

```bash
gh api repos/GH_USER/REPO/compare/UPSTREAM_OWNER:main...GH_USER:main \
  --jq '{ahead: .ahead_by, behind: .behind_by}'
```

**Flag candidates for deletion:**
- `ahead_by: 0` = No custom changes
- `behind_by: N` = Stale (upstream has moved on)

**Present finding:**
```
REPO: 0 commits ahead, 445 behind upstream
→ Recommendation: DELETE (no custom changes, very stale)
```

### Phase 3: Orphaned Secrets Audit

**List secrets per repo:**

```bash
gh api repos/GH_USER/REPO/actions/secrets --jq '.secrets[].name'
```

**Cross-reference with workflow files:**

```bash
# Get workflow file content and search for secret references
gh api repos/GH_USER/REPO/contents/.github/workflows --jq '.[].name' | while read file; do
  gh api "repos/GH_USER/REPO/contents/.github/workflows/$file" --jq '.content' | base64 -d | grep -o 'secrets\.[A-Z_]*'
done | sort -u
```

**Flag orphaned secrets:**
- Secret exists but not referenced in any workflow
- Present for user review (secrets are sensitive - never auto-delete)

### Phase 4: Security Config Audit

**Check Dependabot:**

```bash
# Check for dependabot.yml
gh api repos/GH_USER/REPO/contents/.github/dependabot.yml 2>/dev/null && echo "Dependabot configured"

# Check vulnerability alerts status
gh api repos/GH_USER/REPO/vulnerability-alerts 2>/dev/null && echo "Alerts enabled"
```

**Check code scanning status:**

```bash
gh api repos/GH_USER/REPO/code-scanning/default-setup --jq '{state: .state, languages: .languages}'
```

### Phase 4b: Dependabot Alert Triage

Phase 4 checks if Dependabot is *configured*. This phase triages actual alerts by tracing them to their source and recommending the right fix: prune unused deps (preferred) or upgrade lock files.

**Mental model:** `pyproject.toml`/`package.json` is the shopping list (direct deps). The lock file is the trolley (everything installed, including transitive deps). Dependabot scans the trolley. Unused items on the shopping list are pure waste — they expand the attack surface and drag in transitive deps you don't need.

**Step 1: Scan all repos for open alerts**

```bash
# Only count real alerts (JSON arrays), not 403 errors (JSON objects)
for repo in $(gh repo list GH_USER --limit 200 --json name --jq ".[].name"); do
  result=$(gh api "repos/GH_USER/$repo/dependabot/alerts?state=open" 2>/dev/null)
  count=$(echo "$result" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(len(d) if isinstance(d, list) else 0)
" 2>/dev/null)
  if [ "$count" != "0" ] && [ -n "$count" ]; then
    echo "=== $repo ($count) ==="
    echo "$result" | python3 -c "
import sys,json
for a in json.load(sys.stdin):
    sev = a.get('security_advisory',{}).get('severity','?')
    pkg = a.get('dependency',{}).get('package',{}).get('name','?')
    eco = a.get('dependency',{}).get('package',{}).get('ecosystem','?')
    manifest = a.get('dependency',{}).get('manifest_path','?')
    fix = a.get('security_vulnerability',{}).get('first_patched_version')
    fix_v = fix.get('identifier','no fix') if fix else 'no fix'
    print(f'  [{sev:6s}] {pkg} ({eco}) via {manifest} -> fix: {fix_v}')
"
  fi
done
```

**Key gotcha:** Repos with Dependabot *disabled* return HTTP 403 with a JSON error object (3 string fields). Naive JSON length-counting mistakes this for "3 alerts". Always check `isinstance(d, list)`.

**Step 2: For each repo with alerts, audit direct deps**

For Python repos (pyproject.toml + uv.lock):
```bash
# 1. List declared deps
grep -A 50 '^\[project\]' pyproject.toml | grep -A 50 'dependencies' | head -20

# 2. Find all third-party imports in source
grep -rn "^import \|^from " src/ tests/ *.py 2>/dev/null | grep -v "from \." | sort -u

# 3. Compare — any declared dep with zero imports is a removal candidate
```

For Node repos (package.json + package-lock.json):
```bash
# 1. List declared deps
jq '.dependencies, .devDependencies' package.json

# 2. Find all third-party imports in source
grep -rn "from ['\"]" src/ --include="*.ts" --include="*.tsx" --include="*.js" | grep -v "from ['\"]\." | sort -u
grep -rn "require(['\"]" src/ scripts/ --include="*.js" | sort -u
```

**Step 3: Categorise each alert**

| Category | Description | Action |
|----------|-------------|--------|
| **Unused direct dep** | Declared but never imported | Remove from manifest, regenerate lock |
| **Transitive of unused dep** | Alert pkg is transitive, but its parent is unused | Remove the parent — alert clears as side effect |
| **Transitive of used dep** | Alert pkg is transitive, parent is genuinely used | `uv lock --upgrade-package PKG` or `npm update PKG` |
| **Fork/upstream code** | Alert is in someone else's code you forked | Skip or PR upstream |

**Prefer removal over upgrade.** Removing an unused dep is a permanent fix. Upgrading a lock file is a point-in-time fix — new CVEs will trigger new alerts against the same transitive chain.

**Step 4: Execute fixes**

For Python repos:
```bash
# Remove unused dep from pyproject.toml (edit manually)
# Then regenerate and sync:
uv lock --upgrade
uv sync
# Run tests if they exist:
uv run pytest 2>/dev/null || echo "No tests"
```

For Node repos:
```bash
# Remove unused dep:
npm uninstall PACKAGE_NAME
# Or edit package.json then:
npm install
# Run tests:
npm test 2>/dev/null || echo "No tests"
```

**Step 5: Commit and push per-repo**

```bash
git add pyproject.toml uv.lock  # or package.json package-lock.json
git commit -m "Remove unused deps, upgrade transitive deps

[describe what was removed and why]

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push
```

**Important:** GitHub's Dependabot scanner runs asynchronously after push. Alerts take a few minutes to clear. Don't wait — verify by checking the lock file no longer contains the vulnerable version.

**Anti-patterns for this phase:**

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Patching transitive deps when parent is unused | Treats the symptom, not the disease | Remove the unused parent dep instead |
| Adding version overrides for transitives | Adds maintenance burden, fragile | Only use as last resort when parent can't be updated |
| Ignoring "imported but undeclared" deps | Works today via transitive hoisting, breaks on next update | Declare them explicitly |
| Running `uv lock --upgrade` without auditing first | Might upgrade things you want pinned | Prefer `--upgrade-package PKG` for targeted fixes |
| Counting 403 error fields as alerts | Repos with Dependabot disabled return 403 JSON objects | Check `isinstance(result, list)` |

### Phase 4c: General Dependency Hygiene

Phase 4b is reactive (triggered by Dependabot alerts). This phase is proactive — sweep all local repos for unused or missing deps regardless of whether they've triggered alerts. Unused deps that haven't caused a CVE *yet* are still dead weight: slower installs, larger attack surface, unnecessary transitive trees.

**Scope:** All repos in `~/Repos` with a `pyproject.toml` or `package.json`.

**Step 1: Find all repos with dependency manifests**

```bash
echo "=== Python ===" && find ~/Repos -maxdepth 2 -name "pyproject.toml" -not -path "*/.*" | sort
echo "=== Node ===" && find ~/Repos -maxdepth 2 -name "package.json" -not -path "*/node_modules/*" -not -path "*/.*" | sort
```

**Step 2: For each repo, compare declared vs imported**

Use parallel Opus subagents (one per repo) for speed. Each agent should:

1. Read the dependency manifest
2. Search all source files for third-party imports
3. Report two lists:
   - **Declared but not imported** (removal candidates)
   - **Imported but not declared** (fragile transitives to promote)

**Python pattern:**
```bash
# Declared deps
grep -A 20 'dependencies' pyproject.toml

# Actual imports (exclude stdlib and relative)
grep -rn "^import \|^from " src/ tests/ *.py 2>/dev/null | grep -v "from \." | sort -u
```

**Node pattern:**
```bash
# Declared deps
jq '.dependencies, .devDependencies' package.json

# Actual imports
grep -rn "from ['\"]" src/ --include="*.ts" --include="*.tsx" --include="*.js" | grep -v "from ['\"]\." | sort -u
```

**Step 3: Categorise findings**

| Finding | Action |
|---------|--------|
| Declared, never imported, not a runtime engine (like openpyxl for pandas) | **Remove** from manifest |
| Declared, never imported, IS a runtime engine (lxml for BeautifulSoup, kaleido for Plotly) | **Keep** — used indirectly |
| Imported but not declared | **Add** to manifest — fragile transitive today, broken install tomorrow |
| Dead import (imported but variable never used) | **Remove** the import line AND the dep |
| Dev tool never imported (ruff, black, mypy) | **Keep** — CLI tools, not libraries |

**Nuance on "runtime engines":** Some packages are never `import`-ed but are loaded at runtime by other packages. Common examples:
- `openpyxl` — pandas Excel engine (`pd.read_excel()` loads it internally)
- `lxml` — BeautifulSoup parser (`BeautifulSoup(html, 'lxml')`)
- `kaleido` — Plotly static export (`fig.write_image()`)
- `pytest-asyncio` — pytest plugin (loaded via pytest plugin discovery)

Grep for string references like `'lxml'`, `'openpyxl'`, `write_image` to verify these before removing.

**Step 4: Execute fixes, commit per-repo, push**

Same as Phase 4b execution steps. Present findings to user before making changes.

### Phase 5: "What Did We Miss?" Checklist (MANDATORY)

**This phase is NOT optional.** Run through the comprehensive checklist before presenting final findings.

See [references/audit-checklist.md](references/audit-checklist.md) for the full checklist.

**Quick sweep:**

```bash
# Check for local clones that might have stale remotes
find ~/Repos -maxdepth 2 -name ".git" -type d 2>/dev/null | while read gitdir; do
  repo=$(dirname "$gitdir")
  remote=$(git -C "$repo" remote get-url origin 2>/dev/null)
  # Check if remote points to any repo we're considering deleting
  echo "$repo: $remote"
done
```

**Items to verify:**
- [ ] Local clones with stale remotes (to repos being deleted)
- [ ] GitHub Apps installations
- [ ] Deploy keys per repo
- [ ] Webhooks
- [ ] Collaborators on personal repos

### Phase 6: Cleanup Execution

**Present consolidated findings:**

```markdown
## Audit Summary

### Stale Forks (delete)
- repo1 (0 ahead, 200 behind)
- repo2 (0 ahead, 50 behind)

### Orphaned Secrets (delete)
- repo3: SECRET_NAME (not referenced)

### Failing Workflows (disable or fix)
- repo4: CodeQL misconfigured for wrong language

### Local Clone Check
- No local clones found for repos being deleted
```

**Use AskUserQuestion for approval:**

```
Which cleanup actions should I perform?
[ ] Delete stale forks (2)
[ ] Delete orphaned secrets (1)
[ ] Disable failing workflows (1)
```

**Execute approved actions:**

```bash
# Delete fork (requires delete_repo scope)
gh repo delete GH_USER/REPO --yes

# Delete secret
gh api repos/GH_USER/REPO/actions/secrets/SECRET_NAME -X DELETE

# Disable CodeQL
gh api repos/GH_USER/REPO/code-scanning/default-setup -X PATCH -f state=not-configured

# Disable workflow
gh workflow disable "Workflow Name" --repo GH_USER/REPO
```

**Verify after cleanup:**

```bash
# Confirm repo deleted
gh repo view GH_USER/REPO 2>&1 | grep -q "not found" && echo "Confirmed deleted"

# Confirm secret deleted
gh api repos/GH_USER/REPO/actions/secrets --jq '.secrets[].name' | grep -v SECRET_NAME
```

## Quick Reference

### Essential Commands

| Operation | Command |
|-----------|---------|
| List repos | `gh repo list GH_USER --json name,isFork,visibility` |
| List forks | `gh repo list GH_USER --fork --json name,parent` |
| Compare fork | `gh api repos/.../compare/upstream:main...owner:main` |
| List secrets | `gh api repos/.../actions/secrets --jq '.secrets[].name'` |
| Check CodeQL | `gh api repos/.../code-scanning/default-setup` |
| Delete repo | `gh repo delete GH_USER/REPO --yes` |
| Delete secret | `gh api repos/.../actions/secrets/NAME -X DELETE` |

### Scope Requirements

| Operation | Required Scope |
|-----------|---------------|
| Read repos | (default) |
| List secrets | (default) |
| Delete repos | `delete_repo` - run `gh auth refresh -h github.com -s delete_repo` |
| Modify security | `security_events` |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Assuming CodeQL is a workflow | Wrong API, can't find/disable it | Use `code-scanning/default-setup` API |
| Deleting repos without local check | Orphaned git remotes | Check ~/Repos first |
| Auto-deleting secrets | Secrets might be used externally | Always require user approval |
| Only checking the failing fork | Other forks might be stale too | Audit ALL forks |
| Checking `ahead_by` only | Fork might have upstream changes | Check both `ahead_by` AND `behind_by` |
| Ghost CodeQL on private repos | Dynamic CodeQL on free-plan private repos can enter undead state — workflow shows "active" but API says "not enabled", UI shows no toggle | Can't fix via API or CLI. Manual: Settings → Code security. If no toggle visible, the entitlement was revoked — workflow is inert, ignore it |
| Using `USERNAME` as variable name | macOS pre-sets `$USERNAME` to local account, shadowing your capture | Use `GH_USER` and verify against `gh auth status` |

## References

- [gh-cli-patterns.md](references/gh-cli-patterns.md) - Complete CLI reference with jq patterns
- [audit-checklist.md](references/audit-checklist.md) - Comprehensive "what did we miss?" checklist
- [cleanup-operations.md](references/cleanup-operations.md) - Safe patterns for destructive operations
