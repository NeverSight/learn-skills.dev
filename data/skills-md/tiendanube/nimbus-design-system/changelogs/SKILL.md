---
name: changelogs
description: Update CHANGELOG.md files based on changes made in the current branch. Use when the user asks to update changelogs, document changes, or prepare release notes.
---

# Changelogs Skill

Update CHANGELOG.md files to reflect changes made in the current git branch.

## When to Use

- When asked to update or write changelogs
- When preparing a PR for merge
- When documenting recent changes before release

## Instructions

### Step 1: Analyze Branch Changes

Run these git commands to understand what changed:

```bash
# Get the base branch (usually master or main)
git log --oneline -1 origin/master

# List all commits in current branch not in master
git log origin/master..HEAD --oneline

# Show changed files with their packages
git diff origin/master --name-only
```

### Step 2: Identify Affected Packages

Determine which packages were modified by checking changed file paths:

- `packages/react/src/atomic/<Component>/*` → Update `packages/react/src/atomic/<Component>/CHANGELOG.md` and `react` directory `CHANGELOG.md`
- `packages/react/src/composite/<Component>/*` → Update `packages/react/src/composite/<Component>/CHANGELOG.md` and `react` directory `CHANGELOG.md`
- `packages/core/styles/*` → Update `packages/core/styles/CHANGELOG.md`
- `packages/core/tokens/*` → Update `packages/core/tokens/CHANGELOG.md`
- Any root monorepo configuration change → Also update the root `CHANGELOG.md`

### Step 3: Classify the Change

Determine the change type based on commit messages and diff:

| Type                            | Category                       | Version Bump  |
| ------------------------------- | ------------------------------ | ------------- |
| Breaking API changes            | `🛠 Breaking changes`           | Major (x.0.0) |
| New props, components, features | `🎉 New features`              | Minor (0.x.0) |
| Bug fixes, corrections          | `🐛 Bug fixes`                 | Patch (0.0.x) |
| Dependency updates              | `📚 3rd party library updates` | Patch         |
| Refactors, docs, tooling        | `💡 Others`                    | Patch         |

### Step 4: Write the Entry

**Format:**

```markdown
## YYYY-MM-DD `version`

#### <emoji> <category>

- <Summary of the change>. ([#PR](https://github.com/TiendaNube/nimbus-design-system/pull/PR) by [@contributor](https://github.com/contributor))
```

**Writing Guidelines:**

1. **Be concise**: One sentence summarizing the user-facing impact
2. **Focus on "what"**: Describe the outcome, not implementation details
3. **Use past tense**: "Added", "Fixed", "Updated", not "Add", "Fix", "Update"
4. **Avoid code details**: No mention of specific functions, variables, or files

**Good examples:**

- `Added disabled state styling to Input component.`
- `Fixed focus ring not appearing on keyboard navigation.`
- `Updated Button to support icon-only variant.`

**Bad examples:**

- `Update Input.tsx to add handleFocus callback and modify CSS classes.`
- `Fixes bug in line 45 of nimbus-input.css.ts where outline was missing.`

### Step 5: Ask for Missing Information

If any of the following is unknown, ask the user:

1. **PR number**: Required for the entry link
2. **GitHub username**: Required for contributor attribution
3. **Version number**: If not clear from existing changelog

### Step 6: Update the Files

1. Read the existing CHANGELOG.md for the affected package(s)
2. Determine the next version based on current version + change type
3. Insert the new entry at the TOP, below the `# Changelog` header
4. Use today's date in YYYY-MM-DD format
5. Update package-specific CHANGELOG.md file, and only update the root CHANGELOG.md file if the change is related to the root monorepo.

## Reference

Full formatting rules are defined in `.cursor/rules/changelogs.mdc`.
