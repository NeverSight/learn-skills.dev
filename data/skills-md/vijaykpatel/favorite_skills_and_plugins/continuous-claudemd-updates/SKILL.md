---
name: continuous-claudemd-updates
description: Maintains CLAUDE.md in sync with codebase changes after commits. Use when (1) A commit has been made and CLAUDE.md needs updating, (2) User explicitly requests CLAUDE.md update or audit, (3) Major refactoring or architectural changes occur, (4) New conventions or patterns are established, (5) Files referenced in CLAUDE.md are deleted/moved. Keeps documentation concise by moving verbose content to docs/ folder with links, removes outdated information, and ensures CLAUDE.md reflects current codebase state.
---

# Continuous CLAUDE.md Updates

## Overview

Keeps CLAUDE.md synchronized with codebase changes through automatic analysis after commits and periodic audits. Maintains conciseness by moving detailed content to docs/ folder, removes outdated information, and ensures documentation accuracy.

**Announce at start**: "I'm using the continuous-claudemd-updates skill to sync CLAUDE.md with recent changes."

## Workflow

### After Each Commit (Automatic Mode)

Follow this sequence when a commit has been made:

#### 1. Analyze Changes

Run the analysis script to understand the impact:

```bash
python scripts/analyze_changes.py --commit HEAD
```

This outputs JSON with:
- Changed files categorized by type (config, source, tests, docs, assets)
- Change magnitude (insertions, deletions, total changes)
- Impact level (minor, moderate, major)
- Commit message for context

#### 2. Review CLAUDE.md Relevance

Based on analysis, determine if CLAUDE.md needs updates:

**Update if:**
- Config files changed (package.json, tsconfig.json, etc.)
- New patterns/conventions introduced in source files
- Architecture or structure modified
- Files referenced in CLAUDE.md were changed/deleted
- Major features added (impact: "major" or "moderate")

**Skip if:**
- Only test files changed
- Documentation-only changes
- Minor bug fixes with no pattern changes
- Impact level: "minor" with no config changes

#### 3. Read Current CLAUDE.md

```bash
cat CLAUDE.md
```

Understand current structure and content before modifying.

#### 4. Compare Against Changes

For each changed file category:

**Config changes**: Check if CLAUDE.md mentions these configs
- Update version numbers, dependency changes, new scripts
- Add new configuration requirements
- Remove references to deleted configs

**Source changes**: Identify pattern changes
- New component structures
- Changed API conventions
- Modified file organization
- Updated workflows

**Deletions**: Remove obsolete references
- Check for file paths that no longer exist
- Remove outdated pattern descriptions
- Delete deprecated workflow instructions

#### 5. Apply Updates

When updating CLAUDE.md:

**Keep entries concise (1-4 sentences)**:
```markdown
## API Client

All API calls use `src/lib/api.ts`. Handles auth, retries, errors.

See [docs/api-patterns.md](docs/api-patterns.md) for advanced patterns.
```

**Move verbose content to docs/**:

If adding >3 paragraphs or >20 lines of code examples:

1. Create a docs/ note using the template from `assets/note-template.md`
2. Place detailed content there
3. Add concise summary to CLAUDE.md with link

Example:
```bash
# Create detailed note
cp assets/note-template.md docs/authentication-flow.md
# Edit docs/authentication-flow.md with details
```

Then in CLAUDE.md:
```markdown
## Authentication

Using NextAuth.js with session-based auth. Config in `pages/api/auth/[...nextauth].ts`.

Full setup guide: [docs/authentication-flow.md](docs/authentication-flow.md)
```

**Remove outdated information**:
- Delete references to renamed/deleted files
- Remove deprecated patterns
- Eliminate historical context ("previously we used...")
- Update file paths that changed

#### 6. Verify Links

Check that all docs/ links are valid:

```bash
# Manual verification or use audit script
python scripts/audit_claudemd.py --claudemd CLAUDE.md
```

Fix any broken links before committing.

#### 7. Commit Updates

Create a commit for CLAUDE.md changes:

```bash
git add CLAUDE.md docs/
git commit -m "$(cat <<'EOF'
Update CLAUDE.md: [brief description of changes]

- [Specific change 1]
- [Specific change 2]

Synced with commit: [original commit hash]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### Manual Audit Mode

When explicitly requested or for periodic maintenance:

#### 1. Run Full Audit

```bash
python scripts/audit_claudemd.py --claudemd CLAUDE.md --report
```

This checks for:
- Broken file references
- Outdated configuration mentions
- Overly verbose sections
- Broken docs/ links

#### 2. Review Audit Results

The audit categorizes issues:

**missing_file**: File referenced in CLAUDE.md no longer exists
- Remove the reference or update to correct path

**config_check**: Configuration file mentioned may be outdated
- Verify the reference matches actual config state
- Update or remove if inaccurate

**verbosity**: Section is too long
- Move content to docs/ with link
- Condense to essential points

**broken_link**: docs/ link is invalid
- Fix the link or create the missing doc

#### 3. Systematic Cleanup

Work through audit issues systematically:

1. **Fix file references**: Update all missing file paths
2. **Verify configs**: Check each config reference against actual files
3. **Reduce verbosity**: Move long sections to docs/
4. **Repair links**: Create missing docs or fix paths

#### 4. Overall Coherence Check

After fixing audit issues, review CLAUDE.md as a whole:

**Structure check**:
- Is organization logical?
- Are sections clearly labeled?
- Is there a natural flow?

**Content check**:
- Does each section add value?
- Are examples current and accurate?
- Is information duplicated anywhere?

**Completeness check**:
- Are critical conventions documented?
- Are new patterns from recent commits included?
- Is anything essential missing?

#### 5. Commit Audit Changes

```bash
git add CLAUDE.md docs/
git commit -m "$(cat <<'EOF'
Audit and update CLAUDE.md

- Fix [N] broken file references
- Move verbose sections to docs/
- Update configuration references
- Remove outdated information

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

## Content Guidelines

See [references/guidelines.md](references/guidelines.md) for comprehensive content standards.

**Quick reference**:

- **Be concise**: Bullet points over paragraphs
- **Be current**: Remove outdated info immediately
- **Be specific**: Link to actual file paths
- **Split when verbose**: >3 paragraphs → docs/ folder
- **Link generously**: Point to details rather than include everything

## Examples

See [references/examples.md](references/examples.md) for good vs bad examples covering:

- Configuration changes
- Component patterns
- API conventions
- Testing requirements
- Major refactoring scenarios
- When to create docs/ notes

## Common Patterns

### Pattern 1: New Feature Added

```
1. Analyze: Major source changes detected
2. Review: New component pattern introduced
3. Update: Add concise entry to CLAUDE.md
4. If complex: Create docs/component-patterns.md
5. Commit: "Update CLAUDE.md: Document new component pattern"
```

### Pattern 2: Configuration Changed

```
1. Analyze: Config file modified (e.g., package.json)
2. Review: New scripts or dependencies
3. Update: Modify relevant CLAUDE.md section
4. Verify: Ensure all config references accurate
5. Commit: "Update CLAUDE.md: Sync with package.json changes"
```

### Pattern 3: Files Renamed/Deleted

```
1. Analyze: File deletions detected
2. Review: CLAUDE.md for references to deleted files
3. Update: Remove or fix file path references
4. Verify: Run audit to catch any missed references
5. Commit: "Update CLAUDE.md: Fix stale file references"
```

### Pattern 4: Audit Finds Verbosity

```
1. Audit: Section flagged as too long
2. Create: New docs/ note using template
3. Move: Detailed content to docs/ file
4. Update: Replace with concise summary + link
5. Commit: "Refactor CLAUDE.md: Move [topic] details to docs/"
```

## Decision Tree

```
Commit made or update requested?
├─ Automatic after commit
│  ├─ Run analyze_changes.py
│  ├─ Impact level "minor" + no config changes?
│  │  └─ Skip update (notify user)
│  └─ Impact "moderate"/"major" or config changed?
│     ├─ Read CLAUDE.md
│     ├─ Compare against changes
│     ├─ Apply updates (concise, split if verbose)
│     └─ Commit changes
│
└─ Manual audit requested
   ├─ Run audit_claudemd.py --report
   ├─ Review audit issues
   ├─ Fix systematically (files → configs → verbosity → links)
   ├─ Overall coherence check
   └─ Commit audit changes
```

## Resources

### scripts/analyze_changes.py

Analyzes git changes and determines impact on CLAUDE.md.

**Usage**:
```bash
python scripts/analyze_changes.py [--commit <hash>]
```

**Output**: JSON with change analysis (magnitude, categories, impact level)

### scripts/audit_claudemd.py

Audits CLAUDE.md against actual codebase state.

**Usage**:
```bash
python scripts/audit_claudemd.py [--claudemd <path>] [--report] [--json]
```

**Checks**:
- Missing file references
- Outdated config mentions
- Overly verbose sections
- Broken docs/ links

### references/guidelines.md

Comprehensive content guidelines for CLAUDE.md including:
- When to include vs move to docs/
- Content quality standards
- Section organization
- Maintenance workflow
- Red flags to watch for

Load when you need detailed guidance on content decisions.

### references/examples.md

Good vs bad examples covering:
- Configuration changes
- Component patterns
- API conventions
- Major refactoring scenarios
- When to create docs/ notes

Load when you need specific examples for comparison.

### assets/note-template.md

Template for creating detailed docs/ notes with standard structure:
- Purpose statement
- Overview
- Sections with examples
- Common patterns
- Troubleshooting
- Last updated date

Copy this template when creating new docs/ notes.

## Red Flags

**Never**:
- Leave outdated file references in CLAUDE.md
- Add verbose content (>4 paragraphs) directly to CLAUDE.md
- Include historical context ("we used to...")
- Skip verification after updates
- Commit without descriptive message

**Always**:
- Run analysis before updates (automatic mode)
- Check for verbosity (split to docs/ if needed)
- Remove outdated information immediately
- Verify links before committing
- Create commit with specific change description

## Integration

This skill runs:

**Automatically (if configured)**:
- After git commit via post-commit hook
- Triggered by commit workflow skills

**Manually**:
- User requests CLAUDE.md update
- User requests CLAUDE.md audit
- After major refactoring
- Periodic maintenance (weekly/monthly)

**Pairs with**:
- Commit workflow skills
- Documentation maintenance tasks
- Code review processes
