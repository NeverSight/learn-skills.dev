---
name: new-workspace
description: Create a new Git branch or worktree for experiments or features. Use when starting a new experiment branch, creating an isolated workspace, or setting up a feature branch with worktree support and UV environment sync.
allowed-tools: Read, Write, Bash, Glob
---

# Create New Git Workspace (Branch or Worktree)

You are helping the user create a new Git branch or worktree for experiments or features.

## Workflow

### 1. Ask User for Workspace Type

Ask the user to choose:
- **branch**: Create a new branch in the current working directory
- **worktree**: Create a new worktree in a separate directory

### 2. Ask for Branch Type and Name

Ask the user to choose the branch type:
- **feature**: For new features (creates `feature/<name>`)
- **exp**: For experiments (creates `exp/<name>`)

Then ask for the branch name (without prefix). For example:
- User inputs: `authentication`
- Result: `feature/authentication` or `exp/authentication`

### 3. Verify Current Git State

Before creating anything, check:
```bash
# Ensure we're in a git repository
git rev-parse --git-dir

# Check for uncommitted changes
git status --porcelain
```

If there are uncommitted changes, warn the user and ask if they want to:
- Stash changes and continue
- Commit changes first
- Cancel operation

### 4. Create Branch or Worktree

#### Option A: Create Branch Only

```bash
# Create and checkout new branch
git checkout -b <branch-type>/<branch-name>
```

Show success message and current branch.

#### Option B: Create Worktree

**Steps:**

1. **Get project root directory:**
```bash
git rev-parse --show-toplevel
```

2. **Create worktree directory structure:**
```bash
# Worktrees will be at: <project-root>/../worktrees/<branch-name>/
PROJECT_ROOT=$(git rev-parse --show-toplevel)
WORKTREE_DIR="$PROJECT_ROOT/../worktrees/<branch-type>-<branch-name>"

# Create worktree
git worktree add "$WORKTREE_DIR" -b <branch-type>/<branch-name>
```

3. **Sync IDE configuration directories:**

Automatically copy IDE configuration folders from project root to worktree:

```bash
# Copy IDE configuration directories
for config_dir in .vscode .cursor .claude; do
    if [ -d "$PROJECT_ROOT/$config_dir" ]; then
        echo "Copying $config_dir configuration..."
        cp -r "$PROJECT_ROOT/$config_dir" "$WORKTREE_DIR/"
        echo "✓ $config_dir synced"
    fi
done
```

**Important**: These directories are **copied** (not symlinked) so that:
- Each worktree can have independent IDE settings if needed
- Changes in one worktree don't affect others
- You can customize settings per experiment/feature

4. **Check for .worktree-links configuration:**

Look for `.worktree-links` file in the project root:
```bash
LINKS_CONFIG="$PROJECT_ROOT/.worktree-links"
if [ -f "$LINKS_CONFIG" ]; then
    # Read and process links
    while IFS= read -r line; do
        # Skip empty lines and comments
        [[ -z "$line" || "$line" =~ ^#.* ]] && continue

        # Create symlink from worktree to original location
        SOURCE="$PROJECT_ROOT/$line"
        TARGET="$WORKTREE_DIR/$line"

        if [ -e "$SOURCE" ]; then
            # Create parent directory if needed
            mkdir -p "$(dirname "$TARGET")"
            ln -s "$SOURCE" "$TARGET"
            echo "Linked: $line"
        else
            echo "Warning: Source not found: $line"
        fi
    done < "$LINKS_CONFIG"
fi
```

**Format of `.worktree-links` file:**
```
# Lines starting with # are comments
# List relative paths from project root to link

data/
models/
.env
configs/local_settings.yaml
```

4. **Sync UV environment in the new worktree:**

```bash
cd "$WORKTREE_DIR"

# Check if pyproject.toml exists (indicating a Python project with uv)
if [ -f "pyproject.toml" ]; then
    echo "Syncing UV environment..."
    uv sync
    echo "UV environment synced successfully"
else
    echo "No pyproject.toml found, skipping UV sync"
fi
```

5. **Display summary:**
```
✓ Worktree created at: <worktree-path>
✓ Branch created: <branch-type>/<branch-name>
✓ Symlinks created: <count> items
✓ UV environment synced

To start working:
  cd <worktree-path>
```

### 5. Error Handling

Handle common errors:

- **Not in a git repository**: Show clear error message
- **Branch already exists**: Ask if user wants to:
  - Create worktree from existing branch (if applicable)
  - Choose a different name
  - Cancel
- **Worktree directory already exists**: Ask to remove or choose different name
- **UV sync fails**: Show error but don't rollback worktree creation
- **.worktree-links not found**: Continue without creating symlinks (this is optional)

### 6. Additional Features

**Optional: List existing worktrees**

If user chooses worktree option, first show existing worktrees:
```bash
git worktree list
```

This helps user see what already exists.

## Configuration File Template

If `.worktree-links` doesn't exist in the project, you can offer to create it with common defaults:

```
# .worktree-links
#
# Symlinks to create in new worktrees
# List paths relative to project root
# Lines starting with # are ignored

# Example entries:
# data/
# models/
# .env
# configs/production.yaml
```

## Important Notes

- **Worktree isolation**: Each worktree has its own working directory but shares the same Git object database
- **UV environment**: Each worktree gets its own `.venv/` (not symlinked) to avoid conflicts
- **Symlinks are absolute paths**: Use absolute paths in symlinks to ensure they work from the worktree location
- **Branch tracking**: New branches are created as local branches (not tracking remote)
