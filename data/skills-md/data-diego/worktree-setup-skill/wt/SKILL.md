---
name: wt
description: Set up git worktrees with automatic env file copying, shared service linking, env patching, baseline test verification, and dependency installation. Use when the user wants to create a .wtsetup config for their project, install the wt shell function, or manage worktree workflows. Triggers on mentions of worktrees, .wtsetup, or requests to configure worktree setup for a repo.
---

# wt — Git Worktree Setup

Generate a `.wtsetup` config and provide a `wt` shell function so new worktrees get env files copied, values patched to avoid conflicts, shared resources symlinked, dependencies installed, and baseline tests verified.

## `.wtsetup` Format

```bash
copy=(                    # Files copied to each new worktree
  ".env.local"
  "config/master.key"
)
link=(                    # Symlinked (shared across worktrees, e.g. Docker volumes)
  "pgdata"
)
patch_keys=(              # Env keys that get branch suffix appended to avoid conflicts
  "DATABASE_URL"          # e.g. myapp_dev → myapp_dev_my-feature
  "DB_NAME"
)
install="bundle install"  # Dependency install command
post_setup="bundle exec rspec"  # Baseline verification after setup
# dev="bin/dev"           # Informational hint
```

## Workflow

### 1. Generate `.wtsetup`

Run the analysis script against the project root:

```bash
bash <skill-path>/scripts/analyze-project.sh <project-root>
```

Detects:
- `.env*`, `master.key`, `credentials.yml.enc`, `.secret*` → `copy=()`
- Docker Compose volume mounts → `link=()`
- DATABASE_URL, DB_NAME, DB_DATABASE, REDIS_URL, PORT, APP_PORT in env files → `patch_keys=()`
- Lockfiles → `install=""` (supports: bundler, pnpm, npm, yarn, bun, pip, poetry, go, cargo, mix, composer)
- Test commands → `post_setup=""` (supports: rspec, rails test, pytest, go test, cargo test, mix test, phpunit, pnpm/npm/yarn/bun test)
- Dev commands (Procfile.dev, bin/dev, Procfile) → commented `dev=""` hint
- Warns if `.wtsetup` is not in the global gitignore

After running, show the generated `.wtsetup` and ask the user to review. Common adjustments:
- Add custom files to `copy=()` (e.g. `config/database.yml`, `.tool-versions`)
- Add shared dirs to `link=()` (e.g. Docker volumes, large asset dirs)
- Add/remove keys from `patch_keys=()` depending on what needs isolation per worktree
- Comment out `post_setup` if tests are slow or not needed every time

If `.wtsetup` is not in the user's global gitignore, offer to add it:

```bash
echo '.wtsetup' >> ~/.config/git/ignore
git config --global core.excludesfile ~/.config/git/ignore
```

This is preferred over per-repo `.gitignore` since `.wtsetup` is a local concern like `.env.local`.

### 2. Install the `wt` shell function

Detect the user's shell from `$SHELL` and install the matching function:

| Shell | Source file | Install to |
|-------|------------|------------|
| zsh | `references/wt.bash` | Append to `~/.zshrc` |
| bash | `references/wt.bash` | Append to `~/.bashrc` |
| fish | `references/wt.fish` | Write to `~/.config/fish/functions/wt.fish` |

Only install if `wt` is not already defined in the target file.

The function:
- Takes a branch name: `wt <branch>`
- Auto-detects the main worktree
- Creates `<repo>-<branch>` next to the main worktree
- Copies files from `copy=()`, creating intermediate directories
- Appends a sanitized branch slug to values of `patch_keys=()` in copied env files
- Symlinks paths from `link=()`
- Runs the `install` command
- Runs `post_setup` to verify clean baseline (warns but doesn't abort on failure)
- Errors clearly if no `.wtsetup` exists

### 3. Verify

Suggest the user test with:

```bash
source ~/.zshrc  # or: source ~/.bashrc / restart fish
wt test-branch
```

Then clean up: `git worktree remove <path>`.
