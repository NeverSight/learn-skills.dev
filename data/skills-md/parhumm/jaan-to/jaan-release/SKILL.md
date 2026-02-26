---
name: jaan-release
description: Automated jaan-to release preparation with validation, docs sync, version bump, and PR creation
allowed-tools: Read, Glob, Grep, Bash(git *), Bash(gh *), Bash(jq *), Bash(npm *), Bash(bash .claude/scripts/*), Bash(bash scripts/validate-security.sh*), Skill(jaan-to:pm-roadmap-update), Skill(jaan-to:release-iterate-changelog), Skill(jaan-to:docs-update)
argument-hint: "[vX.Y.Z] [\"release summary\"]"
---

# jaan-release

> Automate jaan-to release preparation from validation to PR creation.

**LOCAL SKILL** — For jaan-to maintainers only. Not distributed to plugin users.

## What This Does

Orchestrates the complete release preparation workflow:
1. ✅ Validates 24 compliance & plugin standards checks
2. 📝 Syncs documentation (roadmap, docs, website, changelog)
3. 🔢 Bumps version atomically across 4 files
4. 🚀 Creates release PR (dev → main)
5. ⏸️ Stops for human review and merge

## Input

- **Optional:** `vX.Y.Z` - Target version (auto-suggested if omitted)
- **Optional:** `"release summary"` - 1-sentence description (extracted from CHANGELOG if omitted)

## Pre-Execution Protocol

**MANDATORY** — Execute before PHASE 1:

**Step 0:** Init Guard — Verify we're in jaan-to repository root
**Step A:** Load Lessons — Read `.claude/skills/jaan-release/LEARN.md`
**Step B:** Branch Check — Verify on `dev` branch (releases prepare from dev)
**Step C:** Offer Dry Run — Ask: "Run validation checks first? [y/n]"

---

# PHASE 1: Pre-Release Validation

**Purpose:** Run all validation checks locally for fast feedback before any changes.

## Step 1.1: Run Validation Scripts

Invoke all 4 validation scripts in sequence:

```bash
# Check 1-10: Advisory compliance (warnings OK)
bash .claude/scripts/validate-compliance.sh

# Check 11-16: Critical plugin standards (must pass)
bash .claude/scripts/validate-plugin-standards.sh

# Security standards (must pass — no blocking errors)
bash scripts/validate-security.sh

# Check git state, docs sync, version detection
bash .claude/scripts/validate-release-readiness.sh
```

**Expected output:**
- Compliance: 10 checks (warnings are advisory)
- Plugin Standards: 6 checks (must pass)
- Security Standards: 4 sections (must pass — no blocking errors)
- Release Readiness: Git clean, docs synced, suggested version

**Capture:**
- `SUGGESTED_VERSION` from validate-release-readiness.sh output
- Any blocking errors from plugin standards

## Step 1.2: Aggregate Results

Parse validation output and summarize:

```
Pre-Release Validation Report
═══════════════════════════════════════════════════════════

## Compliance Checks (10/10)
  ✓ Check 1: Skill Alignment (all skills have two-phase + HARD STOP)
  ✓ Check 2: Generic Applicability (no user-specific refs)
  ✓ Check 3: Multi-Stack Coverage (Node.js/PHP/Go)
  ...
  ✓ Check 10: Security Review (no dangerous patterns)

## Plugin Standards (6/6)
  ✓ Check 11: Plugin Manifests (JSON valid, versions match)
  ✓ Check 12: Hooks Validation (4 hooks defined)
  ✓ Check 13: Skills Structure (40 skills, all have frontmatter)
  ✓ Check 14: Context Files (all have headers)
  ✓ Check 15: Output Structure (0 errors)
  ✓ Check 16: Permission Safety (no dangerous patterns)

## Security Standards (4/4)
  ✓ Section A: Skill Permission Safety (no bare Write/Bash/Edit)
  ✓ Section B: Shell Script Safety (set -euo pipefail, no eval/curl|sh)
  ✓ Section C: Hook Safety (static paths, no user input)
  ✓ Section D: Dangerous Patterns (no exec(), no rm -rf /)

## Git State (3/3)
  ✓ Working tree clean (0 uncommitted changes)
  ✓ On dev branch (up to date with origin/dev)
  ✓ Remotes fetched

## Documentation (2/2)
  ✓ Sync check: 0 stale files
  ✓ README indexes: all up to date

## Release Content (3/3)
  ✓ [Unreleased] section: 5 entries (3 Added, 1 Changed, 1 Fixed)
  ✓ CHANGELOG format: Keep a Changelog ✓
  ✓ Suggested version: v6.3.0 (minor bump - new features added)

───────────────────────────────────────────────────────────────
✅ All 24 checks passed. Ready for Phase 2.
───────────────────────────────────────────────────────────────
```

**If any errors:**
- Show specific failures with remediation commands
- Block Phase 2 until fixed
- Suggest: `git status`, `git stash`, fix commands from script output

# HARD STOP 1: Validation Report

**Ask user:**
```
Validation complete. All 24 checks passed.
Suggested version: v6.3.0 (minor bump)

Proceed to Phase 2 (Documentation & Version Prep)? [y/n/abort]
```

**Options:**
- `y` → Continue to Phase 2
- `n` → Show detailed validation output, then re-ask
- `abort` → Exit skill (no changes made)

**Rollback:** None needed (read-only phase)

---

# PHASE 2: Documentation & Version Prep

**Purpose:** Sync all documentation and prepare release content.

## Step 2.1: Roadmap Sync

Invoke: `/jaan-to:pm-roadmap-update sync`

**This skill:**
- Reads git history since last version tag
- Marks completed tasks as "done" in roadmap.md
- Updates task statuses based on commit messages

**Expected:** `✓ Roadmap synced: 3 tasks marked done`

## Step 2.2: Documentation Auto-Fix

Invoke: `/jaan-to:docs-update --fix`

**This skill:**
- Updates stale timestamps in docs
- Generates missing doc files
- Rebuilds README.md indexes

**Expected:** `✓ Documentation updated: 2 files fixed, 0 missing`

## Step 2.3: Website Update (ENHANCED)

Run intelligent website updater:

```bash
bash .claude/scripts/update-website.sh
```

**This script:**
- Updates version badge (v6.1.0 → v6.3.0)
- Updates skill counts (3 locations)
- Updates role counts (2 locations)
- Detects new/removed skills from CHANGELOG
- Generates HTML for catalog updates
- Smart suggestions (new roles, efficiency metrics, etc.)

**Expected output:**
```
Website Update Summary
────────────────────────────────────────────────────────────
  ✓ Version badge:   v6.3.0
  ✓ Skill counts:    40 skills (3 locations)
  ✓ Role count:      11 roles (2 locations)

  ⚠ MANUAL REVIEW REQUIRED

  Next steps:
  1. Review catalog changes above
  2. Edit website/index.html to add/remove skills
  3. Preview: open website/index.html in browser
```

**If new skills detected:**
- Script shows generated HTML for each new skill
- Ask user: "Apply these catalog updates? [y/n/manual]"
- If `y`: Apply updates automatically
- If `n`: Skip catalog updates (user will do manually)
- If `manual`: Open website/index.html in editor, wait for user confirmation

## Step 2.4: Changelog Generation

Invoke: `/jaan-to:release-iterate-changelog auto-generate`

**This skill:**
- Parses git commits since last tag
- Generates CHANGELOG entries from conventional commits
- Categorizes: Added, Changed, Fixed, Removed
- Merges with existing [Unreleased] items

**Expected:** `✓ CHANGELOG generated: 5 entries categorized`

# HARD STOP 2: Review Prepared Changes

**Show diff summary:**
```bash
git status --short
```

**Expected files modified:**
- `docs/roadmap/roadmap.md` (3 tasks marked done)
- `docs/**/*.md` (2 README indexes updated)
- `website/index.html` (version, counts, possibly catalog)
- `CHANGELOG.md` (5 entries organized)

**Ask user:**
```
Documentation Sync Complete
───────────────────────────
Modified files:
  M CHANGELOG.md
  M docs/roadmap/roadmap.md
  M website/index.html
  M docs/guides/README.md

Preview changes? [y/n/proceed]
```

**Options:**
- `y` → Show `git diff` for each file
- `n` → Skip preview
- `proceed` → Continue to Phase 3
- `abort` → Rollback changes

**Rollback if aborted:**
```bash
git restore CHANGELOG.md docs/ website/index.html
```

---

# PHASE 3: Atomic Version Bump

**Purpose:** Create single atomic commit with version bump across all files.

## Step 3.1: Determine Target Version

**If version provided as argument:**
- Use provided version (e.g., `v6.3.0`)

**If version omitted:**
- Use `SUGGESTED_VERSION` from Step 1.2
- Confirm with user: "Use suggested version v6.3.0? [y/n/custom]"

**Validate version:**
- Check format: `vX.Y.Z` (semantic versioning)
- Check tag doesn't exist: `git tag -l v6.3.0`
- If exists: Error and abort

## Step 3.2: Atomic Version Bump

Invoke: `/jaan-to:pm-roadmap-update release v6.3.0 "Add jaan-release skill"`

**This skill atomically:**
1. Moves CHANGELOG `[Unreleased]` → `[6.3.0]` with date
2. Creates roadmap version section with tasks from this release
3. Updates `.claude-plugin/plugin.json` → `"version": "6.3.0"`
4. Updates `.claude-plugin/marketplace.json` → 2 version fields
5. Creates commit: `release: 6.3.0 — Add jaan-release skill`
6. Creates tag: `v6.3.0` (local only, not pushed)

**Expected:**
```
✓ Version bumped: v6.2.0 → v6.3.0
✓ Files updated: CHANGELOG.md, roadmap.md, plugin.json (×3)
✓ Commit created: abc1234
✓ Tag created: v6.3.0 (local)
```

## Step 3.3: CI Simulation (Local Validation)

Run the same checks CI will run:

```bash
# Check version consistency
V1=$(jq -r '.version' .claude-plugin/plugin.json)
V2=$(jq -r '.version' .claude-plugin/marketplace.json)
V3=$(jq -r '.plugins[0].version' .claude-plugin/marketplace.json)

if [[ "$V1" == "$V2" ]] && [[ "$V1" == "$V3" ]]; then
  echo "✓ Version consistency: $V1"
else
  echo "✗ Version mismatch (CI will fail)"
  exit 1
fi

# Validate skill description budget
bash scripts/validate-skills.sh || exit 1

# Security standards validation
bash scripts/validate-security.sh || exit 1
echo "✓ Security standards passed"

# Build docs site (verify no build errors)
cd website/docs && npm ci && npm run build && cd ../..
echo "✓ Docs site builds successfully"
```

**Expected:** All checks pass (CI will run same checks)

# HARD STOP 3: Version Bump Confirmation

**Show complete atomic operation result:**
```
Version Bump Complete
─────────────────────
Version: 6.3.0 ✓
Files Updated:
  - CHANGELOG.md (new [6.3.0] section with date)
  - docs/roadmap/roadmap.md (version section added)
  - .claude-plugin/plugin.json (version: "6.3.0")
  - .claude-plugin/marketplace.json (version: "6.3.0" × 2)

Git State:
  - Commit: abc1234 (release: 6.3.0 — Add jaan-release skill)
  - Tag: v6.3.0 (local, not pushed)

CI Simulation: ✓ PASS (all checks)

Push to origin and create PR? [y/n/abort]
```

**Options:**
- `y` → Continue to Phase 4
- `n` → Show commit details, then re-ask
- `abort` → Rollback

**Rollback if aborted:**
```bash
git tag -d v6.3.0              # Delete local tag
git reset --soft HEAD~1        # Undo commit, keep changes staged
# OR
git reset --hard HEAD~1        # Undo commit and discard all changes
```

---

# PHASE 4: PR Creation

**Purpose:** Push changes and create PR for human review.

## Step 4.1: Push Branch with Tag

```bash
git push origin dev --tags
```

**Expected:**
```
✓ Pushed to origin/dev
✓ Pushed tag v6.3.0
```

**If push fails:**
- Check network connectivity
- Check GitHub authentication: `gh auth status`
- Show error, offer retry

## Step 4.2: Create PR (dev → main)

```bash
gh pr create --base main \
  --title "release: 6.3.0 — Add jaan-release skill" \
  --body "$(cat <<'EOF'
## Release Summary
Add jaan-release skill for automated release preparation.

## Changes This Release
### Added
- jaan-release skill for release automation
- Compliance validation (10-item checklist)
- Documentation sync automation

### Changed
- (list from CHANGELOG [6.3.0] section)

### Fixed
- (list from CHANGELOG [6.3.0] section)

## Pre-Merge Checklist
- [x] All 24 validation checks passed locally
- [x] Security standards validation passed
- [x] Documentation synced and up to date
- [x] CHANGELOG entry complete
- [x] Version bumped in all 3 locations
- [x] CI simulation passed locally
- [ ] CI checks pass on GitHub (wait for workflow)
- [ ] Human review approved

## Post-Merge Steps
After merging this PR:
1. **Tag on main**: \`git checkout main && git pull && git tag v6.3.0 && git push origin main --tags\`
2. **Create release**: \`gh release create v6.3.0 --title "v6.3.0" --notes-file CHANGELOG.md\`
3. **Sync dev**: \`git checkout dev && git merge main && git push\`
4. **Bump dev**: \`./scripts/bump-version.sh 6.4.0 && git commit -am "chore: bump to 6.4.0" && git push\`
5. **Acknowledge issues**: For each closed issue in this release, run \`/jaan-issue-solve #{issue_number}\`

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Expected:**
```
✓ PR created: https://github.com/parhumm/jaan-to/pull/123
```

## Step 4.3: Monitor CI Checks

```bash
gh pr checks --watch
```

**Show CI status:**
```
CI Checks:
  - release-check.yml: ✓ PASSED (2m 15s)
  - deploy-docs.yml: ⏳ Running...
```

**If CI fails:**
- Show error logs: `gh run view <run-id> --log`
- Suggest fixes based on error type
- User can push fixes to same branch

# HARD STOP 4: PR Created — Human Takes Over

**Show final status:**
```
PR Created Successfully
───────────────────────
URL: https://github.com/parhumm/jaan-to/pull/123
Status: Waiting for CI checks

CI Checks:
  - release-check.yml: ✓ PASSED
  - deploy-docs.yml: ✓ PASSED

Next Steps (Manual):
1. Review PR at URL above
2. Approve and merge PR (via GitHub UI or gh pr merge)
3. Follow "Post-Merge Steps" in PR description

SKILL COMPLETE - Human merge required.
```

**Skill exits here.** Human performs:
- PR review and approval
- Merge to main
- Tag creation on main (not dev)
- GitHub release publication
- Dev branch sync and version bump
- Issue acknowledgments via `/jaan-issue-solve`

---

## Definition of Done

- [x] All 24 validation checks passed
- [x] Documentation synced (roadmap, docs, website, CHANGELOG)
- [x] Version bumped atomically (4 files + commit + tag)
- [x] CI simulation passed locally
- [x] PR created (dev → main)
- [x] CI checks passed on GitHub
- [ ] **Human review and merge** (manual)
- [ ] **Post-merge steps** (tag, release, sync, bump - manual)
- [ ] **Issue acknowledgments** (manual)

---

## Skill Alignment

**Aligns with jaan-to principles:**
- ✅ Two-phase workflow with HARD STOP gates (4 gates)
- ✅ Single source of truth (validation logic in `.claude/scripts/`)
- ✅ Reuses existing skills (pm-roadmap-update, docs-update, release-iterate-changelog)
- ✅ Token-optimized (orchestrates, doesn't duplicate)
- ✅ Maintains human control (stops at PR creation)
- ✅ Generic and scalable (works for any version)
- ✅ LOCAL skill (not distributed to users)

---

## Error Handling

**Common issues:**

1. **Dirty working tree** → Block at Phase 1, show uncommitted files
2. **Version already exists** → Block at Phase 3, suggest next version
3. **CI workflow failure** → Show logs, continue (user fixes manually)
4. **Merge conflict on PR** → Show conflicting files, continue (user resolves)
5. **GitHub CLI not authenticated** → Block at Phase 4, show `gh auth login` instructions
6. **Documentation build failure** → Block at Phase 3, show npm error

**Rollback at each gate:**
- Phase 1: None needed (read-only)
- Phase 2: `git restore <files>`
- Phase 3: `git tag -d v6.3.0 && git reset --hard HEAD~1`
- Phase 4: `gh pr close <PR> && git push origin :v6.3.0`

---

## Local Development Only

**This skill is LOCAL to jaan-to repository:**
- Location: `.claude/skills/jaan-release/`
- Not in `skills/` (not distributed to users)
- References LOCAL scripts in `.claude/scripts/`
- Only jaan-to maintainers have access

**Users don't see this skill** when they install jaan-to plugin.
