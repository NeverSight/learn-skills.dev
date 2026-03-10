---
name: docs-update
description: Update documentation after code changes. Use when adding features, changing keybindings, modifying config options, or updating TUI behavior. Automatically finds and updates relevant documentation files (README, recipes, help text).
compatibility: claude
---

# Documentation Update Workflow

Streamline documentation updates when code changes are made. This skill helps identify what documentation needs updating and guides you through the process.

## When to Use

Use this skill after:
- Adding new TUI keybindings
- Adding new CLI commands or flags
- Adding new config options
- Changing default behavior
- Adding new features or integrations
- Modifying user-facing functionality

## Workflow

### Step 1: Identify Changes

Analyze recent commits or current changes to identify documentation-impacting changes:

```bash
# Check uncommitted changes
git diff

# Check recent commits
git log -5 --oneline
git show <commit-sha>

# Check specific files
git diff HEAD~1 internal/tui/model.go
```

**Look for:**
- New keybindings in TUI code
- New commands in CLI code
- New config fields
- Changed default values
- New features or integrations

### Step 2: Find Relevant Documentation

Documentation files to check:

| File | Update When |
|------|-------------|
| `README.md` | Keybindings, features, config options, CLI commands |
| `docs/recipes/*.md` | Integration-specific changes |
| CLI help text | New commands, flags, or changed behavior |

**Search commands:**
```bash
# Find documentation files
find . -name "*.md" -not -path "./agent-deck/*" | head -20

# Search for specific content
grep -r "keybindings" README.md docs/
grep -r "Default keybindings" README.md
```

### Step 3: Update Documentation

#### README.md Sections to Update

**Default Keybindings** (around line 311):
```markdown
**Default keybindings:**

- `:` - Open command palette (when user commands configured)
- `v` - Toggle preview sidebar (shows tmux pane output)
- `r` - Recycle session
- `d` - Delete session
...
```

**TUI Features** (around line 303):
```markdown
**Features:**

- Tree view of sessions grouped by repository
- Real-time terminal status monitoring (with tmux integration)
- Preview sidebar showing live tmux pane output (`v` to toggle)
...
```

**Configuration Options** (around line 238):
Add new config fields to the table with type, default, and description.

**CLI Reference** (starting line 288):
Add new commands or flags with descriptions and examples.

#### Recipe Updates

Update `docs/recipes/tmux-integration.md` when:
- Adding tmux-specific keybindings
- Changing tmux integration behavior
- Adding new status indicators

### Step 4: Verify Updates

Check that documentation is accurate and complete:

```bash
# Search for old keybinding references
grep -r "old-key" README.md docs/

# Verify all new features are documented
grep -r "new-feature" README.md

# Check for consistency
grep -rn "keybindings" README.md
```

### Step 5: Commit

Commit documentation changes separately from code changes:

```bash
git add README.md docs/
git commit -m "docs: describe what was updated

Detailed description of changes."
```

## Examples

### Example 1: New TUI Keybinding

**Change:** Added `v` key to toggle preview sidebar

**Documentation Updates:**
1. README.md line ~315: Add `v` key to keybindings list
2. README.md line ~305: Add preview feature to features list
3. Verify no other mentions of keybindings need updating

**Commit:**
```bash
git add README.md
git commit -m "docs: add preview sidebar to TUI features and keybindings

Document the new 'v' key for toggling the tmux pane preview sidebar
in the default keybindings list and TUI features section."
```

### Example 2: New Config Option

**Change:** Added `tui.preview_enabled` config option

**Documentation Updates:**
1. README.md Configuration Options table: Add new row with type, default, description
2. README.md Config example: Add to YAML example if commonly used
3. Check if any recipes should mention it

### Example 3: New CLI Command

**Change:** Added `hive preview` command

**Documentation Updates:**
1. README.md CLI Reference: Add new section with command description
2. Add flag table if command has flags
3. Add usage examples
4. Update command list in Quick Start if relevant

## Checklist

Use this checklist for every documentation update:

- [ ] Identified all code changes that impact users
- [ ] Found all relevant documentation files
- [ ] Updated README.md keybindings (if applicable)
- [ ] Updated README.md features list (if applicable)
- [ ] Updated README.md config options (if applicable)
- [ ] Updated README.md CLI reference (if applicable)
- [ ] Updated recipes (if applicable)
- [ ] Searched for old references to changed behavior
- [ ] Verified accuracy of all updates
- [ ] Committed with clear message

## Tips

**Be Proactive:**
- Update docs in the same PR as code changes when possible
- Review documentation as part of code review

**Be Thorough:**
- Search for all mentions of changed behavior
- Update examples to match new behavior
- Check both inline docs and separate files

**Be Clear:**
- Use consistent terminology
- Provide examples for complex features
- Document the "why" not just the "what"

**Keep Organized:**
- Separate doc commits from code commits when updating after the fact
- Use descriptive commit messages
- Link docs commits to related code commits
