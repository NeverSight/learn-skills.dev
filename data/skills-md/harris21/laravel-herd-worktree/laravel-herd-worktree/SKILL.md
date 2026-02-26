---
name: laravel-herd-worktree
description: Use when setting up a Laravel worktree for local development with Laravel Herd, or when user asks to work on a feature branch in isolation
license: MIT
---

# Laravel Herd Worktree Setup

## Overview

Sets up a git worktree for Laravel projects served by Laravel Herd, ensuring the worktree has its own site URL and properly configured environment.

**Announce at start:** "I'm using the laravel-herd-worktree skill to set up an isolated Laravel workspace with Herd."

## IMPORTANT: User Interaction Guidelines

**ALWAYS use the `AskUserQuestion` tool for ALL user interactions.** Never stop and wait for user reply. The AskUserQuestion tool allows the workflow to continue seamlessly.

All question blocks in this skill (shown in YAML-like format) should be implemented using the AskUserQuestion tool with the specified options.

## When to Use

- User wants to work on a feature branch in isolation
- User mentions "worktree" and the project uses Laravel Herd
- Starting work on a task that needs isolation from main branch

## Initial Flow

1. **First, check if any worktrees already exist** using `git worktree list`
2. **If worktrees exist**, immediately use AskUserQuestion to ask if they want to:
   - Set up a new worktree
   - Finish work on an existing worktree (then ask which one and proceed to "Finishing Work" section)
3. **If no worktrees exist**, use AskUserQuestion to ask for the branch name, then proceed with setup

## Prerequisites

- **Laravel Herd** installed and running on macOS
- **Git** for version control
- **Vite** as the frontend build tool (this skill assumes Vite, not Webpack/Mix)
- **npm** as package manager (adjust commands if using yarn/pnpm)
- **Laravel Sanctum** if using API authentication (optional - skill handles this if present)

## Setup Steps

### 0. Get Project Name and Branch Name

**First, detect the project name** (used for the Herd site URL to avoid conflicts between projects with the same branch name):

```bash
# Get project name from the directory name
PROJECT_NAME=$(basename "$PWD")
```

**Use AskUserQuestion to confirm or customize the project name:**

```
AskUserQuestion:
  question: "Project name detected as '$PROJECT_NAME'. This will be used for the Herd URL (e.g., projectname-branchname.test). Is this correct?"
  header: "Project"
  options:
    - label: "Yes, use '$PROJECT_NAME'"
      description: "Use the detected project name"
    - label: "Use a different name"
      description: "I'll provide a custom project name"
```

**Then use AskUserQuestion to get the branch name:**

```
AskUserQuestion:
  question: "What branch name would you like to use for this worktree?"
  header: "Branch Name"
  options:
    - label: "feature/new-feature"
      description: "Generic feature branch - you can provide a custom name"
    - label: "bugfix/fix-issue"
      description: "Bugfix branch pattern"
    - label: "experiment/test"
      description: "Experimental/testing branch"
```

**Note:** Both project name and branch name will be sanitized for the Herd link (slashes replaced with dashes, spaces removed). For example, project `my-app` with branch `feature/new-feature` becomes `my-app-feature-new-feature.test`.

**Construct the site name:**
```bash
SANITIZED_BRANCH_NAME=$(echo "$BRANCH_NAME" | tr '/' '-')
SITE_NAME="$PROJECT_NAME-$SANITIZED_BRANCH_NAME"
```

### 1. Create Worktree (if needed)

```bash
# Check if worktree exists
git worktree list | grep "$BRANCH_NAME"

# If not, create it
git worktree add .worktrees/$SITE_NAME -b $BRANCH_NAME
```

### 2. Link with Laravel Herd

```bash
cd /path/to/project/.worktrees/$SITE_NAME
herd link $SITE_NAME
```

This creates a site at `http://$SITE_NAME.test` (e.g., `http://myproject-feature-branch.test`)

**Note:** Do NOT run `herd secure` - the site should use HTTP to match the Vite dev server.

**Why include project name?** This prevents conflicts when multiple projects have the same branch name (e.g., both `project-a` and `project-b` have a `feature/login` branch).

### 3. Copy and Configure .env

```bash
# Copy .env from main project
cp /path/to/main/project/.env /path/to/worktree/.env

# Update APP_URL to match Herd site (use HTTP, not HTTPS)
sed -i '' "s|APP_URL=.*|APP_URL=http://$SITE_NAME.test|" /path/to/worktree/.env

# Update SESSION_DOMAIN to match the worktree domain
sed -i '' "s|SESSION_DOMAIN=.*|SESSION_DOMAIN=$SITE_NAME.test|" /path/to/worktree/.env

# Add worktree domain to SANCTUM_STATEFUL_DOMAINS (for API auth, if using Sanctum)
sed -i '' "s|SANCTUM_STATEFUL_DOMAINS=\(.*\)|SANCTUM_STATEFUL_DOMAINS=\1,$SITE_NAME.test|" /path/to/worktree/.env

# Ensure secure cookies are disabled for HTTP
echo "SESSION_SECURE_COOKIE=false" >> /path/to/worktree/.env
```

### 4. Install Dependencies

**CRITICAL: Worktrees do NOT share vendor/ or node_modules/ with the main project.**

**Use AskUserQuestion before running composer install:**

```
AskUserQuestion:
  question: "Would you like to add any flags to composer install?"
  header: "Composer"
  options:
    - label: "No flags needed (Recommended)"
      description: "Run 'composer install --no-interaction' with no additional flags"
    - label: "Add --ignore-platform-req=ext-mailparse"
      description: "Ignore the mailparse extension requirement (common issue)"
    - label: "Add custom flags"
      description: "I'll provide specific flags"
```

If user selects "Add custom flags", ask them to provide the flags they want to use.

```bash
# Install PHP dependencies (add user-provided flags if any)
composer install --no-interaction  # Append user's custom flags here if provided

# Install Node.js dependencies
npm install

# Clear Laravel caches
php artisan config:clear
php artisan cache:clear
```

**Ask user if composer/npm install fails:** "The dependency installation failed. Would you like me to:
1. Retry with `--ignore-platform-reqs`
2. Skip and continue (not recommended)
3. Show the error for manual debugging"

### 5. Ensure vite.config.js Has CORS Support

**IMPORTANT:** To avoid Cross-Origin Request Blocked errors, ensure vite.config.js includes:

```javascript
export default defineConfig(() => {
    return {
        server: {
            host: 'localhost',
            cors: true,
        },
        plugins: [
            // ... your plugins
        ]
    }
});
```

**Key settings:**
- `host: 'localhost'` - Prevents CORS issues (do NOT use `0.0.0.0`)
- `cors: true` - Enables CORS for cross-origin requests

### 6. Kill Existing Vite Processes & Start Dev Server

**IMPORTANT:** If Vite is already running from the main project, it will occupy port 5173. You must kill it first to ensure the worktree's Vite uses the correct port and serves the correct assets.

```bash
# Kill any existing Vite processes
pkill -f "node.*vite" 2>/dev/null

# Remove stale hot file
rm -f public/hot

# Start Vite dev server (will use APP_URL from .env)
npm run dev
```

**Why this matters:** Vite reads APP_URL from .env to configure hot module replacement. If the wrong Vite instance is running, assets will fail to load or point to the wrong domain.

## Finishing Work (Integrating Back to Main Tree)

When development is complete and you want to integrate the worktree changes, **immediately use AskUserQuestion** to ask how they want to proceed:

```
AskUserQuestion:
  question: "How would you like to finish your worktree changes?"
  header: "Finish Work"
  options:
    - label: "Create PR from worktree (Recommended)"
      description: "Commit, push, and create a PR directly from the worktree branch"
    - label: "Transfer to main directory"
      description: "Merge changes into the main project directory, then clean up the worktree"
    - label: "Abandon changes"
      description: "Discard all changes and remove the worktree"
```

**After setup completes, tell the user:** "When you're ready to finish your work, run `/laravel-herd-worktree` again and I'll help you integrate or clean up your changes."

---

### Option A: Create PR from Worktree

Use this when you want to keep changes isolated and create a PR directly from the worktree.

#### A.0. Gather Information

**Use AskUserQuestion to gather information (can ask multiple questions at once):**

```
AskUserQuestion:
  questions:
    - question: "Do you have a task/issue number for this work?"
      header: "Task ID"
      options:
        - label: "No task number"
          description: "Skip adding a task identifier to the branch and commit"
        - label: "Enter task number"
          description: "I'll provide a task/issue number to include in the branch name and commit"
    - question: "How would you like to handle the PR description?"
      header: "PR Body"
      options:
        - label: "I'll write it"
          description: "Create PR with empty body - I'll fill in the description on GitHub"
        - label: "Generate for me"
          description: "Analyze the changes and generate a PR description automatically"
        - label: "Leave empty"
          description: "Create PR with no description"
```

#### A.1. Commit All Changes

```bash
cd /path/to/project/.worktrees/$BRANCH_NAME
git add -A
git commit -m "Your commit message (#TASK_NUMBER)"  # Omit (#TASK_NUMBER) if none provided
```

#### A.2. Rename Branch with Task Number (if provided)

If a task number was provided and the branch doesn't include it:

```bash
git branch -m old-branch-name TASK_NUMBER-descriptive-name
```

#### A.3. Push and Create PR

**Note:** The base branch defaults to `develop`. Adjust to your project's default branch (e.g., `main` or `master`) if different. You can detect the default branch with:
```bash
git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'
```

```bash
git push -u origin BRANCH_NAME

# Based on user's PR description preference:
# - "I'll write it" or "Leave empty": gh pr create --base $DEFAULT_BRANCH --title "Title" --body ""
# - "Generate for me": Generate description from git diff, then use --body "$DESCRIPTION"
gh pr create --base $DEFAULT_BRANCH --title "Description (#TASK_NUMBER)" --body "$BODY"
```

#### A.4. Cleanup After Merge

After the PR is merged, clean up the worktree:

```bash
# Stop Vite if running
pkill -f "node.*vite" 2>/dev/null

# From main project directory
cd /path/to/main/project
herd unlink $SITE_NAME
git worktree remove .worktrees/$SITE_NAME
git branch -d TASK_NUMBER-branch-name  # Delete local branch
```

---

### Option B: Transfer Changes to Main Directory

Use this when you want to bring your worktree changes back into the main project directory, review them there, and then commit/push from the main directory.

#### B.1. Confirm Transfer

**Use AskUserQuestion to confirm:**
```
AskUserQuestion:
  question: "This will merge your worktree branch into the main directory. Continue?"
  header: "Confirm"
  options:
    - label: "Yes, transfer changes"
      description: "Merge the worktree branch into the main project and clean up"
    - label: "Cancel"
      description: "Go back without transferring"
```

#### B.2. Stop Vite and Prepare

```bash
# Stop Vite if running in worktree
pkill -f "node.*vite" 2>/dev/null

# Navigate to main project directory
cd /path/to/main/project
```

#### B.3. Merge Worktree Branch

```bash
# Fetch and merge the worktree branch into current branch
git merge $BRANCH_NAME --no-commit --no-ff
```

The `--no-commit` flag stages the changes without committing, allowing the user to review and commit manually. The `--no-ff` ensures a merge commit is created for clarity.

**If merge conflicts occur:**
- Inform the user about the conflicts
- List the conflicting files
- Ask if they want to resolve them now or abort

#### B.4. Clean Up Worktree

After the merge is staged:

```bash
# Unlink from Herd
herd unlink $SITE_NAME

# Remove the worktree
git worktree remove .worktrees/$SITE_NAME

# Delete the worktree branch (it's now merged)
git branch -D $BRANCH_NAME
```

#### B.5. Final Steps

**Inform the user:**
"Your changes have been merged into the main directory and are staged for commit. The worktree has been cleaned up.

You can now:
- Review the changes with `git status` and `git diff --cached`
- Commit when ready with `git commit`
- Or unstage specific files if needed with `git reset HEAD <file>`"

---

### Option C: Abandon Changes

When abandoning a worktree without merging:

```bash
# Stop Vite if running
pkill -f "node.*vite" 2>/dev/null

# Unlink from Herd
herd unlink $SITE_NAME

# Remove worktree
git worktree remove .worktrees/$SITE_NAME

# Delete branch if not needed
git branch -D $BRANCH_NAME
```

## Quick Reference

**Variables:**
- `$PROJECT_NAME` - The project directory name (e.g., `my-laravel-app`)
- `$BRANCH_NAME` - The git branch name (e.g., `feature/login`)
- `$SANITIZED_BRANCH_NAME` - Branch name with slashes replaced by dashes (e.g., `feature-login`)
- `$SITE_NAME` - Combined name for Herd: `$PROJECT_NAME-$SANITIZED_BRANCH_NAME` (e.g., `my-laravel-app-feature-login`)

| Step | Command |
|------|---------|
| Create worktree | `git worktree add .worktrees/$SITE_NAME -b $BRANCH_NAME` |
| Link to Herd | `herd link $SITE_NAME` |
| Copy .env | `cp ../../../.env .env` |
| Update APP_URL | `sed -i '' "s\|APP_URL=.*\|APP_URL=http://$SITE_NAME.test\|" .env` |
| Install PHP deps | `composer install --no-interaction` |
| Install Node deps | `npm install` |
| Clear cache | `php artisan config:clear && php artisan cache:clear` |
| Kill old Vite | `pkill -f "node.*vite"` |
| Start dev | `npm run dev` |
| Unlink | `herd unlink $SITE_NAME` |
| Remove worktree | `git worktree remove .worktrees/$SITE_NAME` |

## Common Issues

### 401 Unauthorized on API routes
- **Cause:** SANCTUM_STATEFUL_DOMAINS doesn't include the worktree domain
- **Symptoms:** Login works but API calls return 401
- **Fix:**
  1. Add worktree domain to SANCTUM_STATEFUL_DOMAINS in .env (use `$SITE_NAME.test`)
  2. Run `php artisan config:clear`

### Cookie rejected for invalid domain
- **Cause:** SESSION_DOMAIN in .env doesn't match the worktree site domain
- **Symptoms:** Console shows "Cookie has been rejected for invalid domain"
- **Fix:**
  1. Update SESSION_DOMAIN in .env: `SESSION_DOMAIN=$SITE_NAME.test`
  2. Add `SESSION_SECURE_COOKIE=false` for HTTP sites
  3. Run `php artisan config:clear`
  4. Clear browser cookies for the domain (or use incognito)

### White page / CORS Errors (Cross-Origin Request Blocked)
- **Cause:** Vite using `host: '0.0.0.0'` instead of `localhost`
- **Symptoms:** Console shows "Cross-Origin Request Blocked" for Vite assets
- **Fix:**
  1. Update vite.config.js to use `host: 'localhost'` and `cors: true`
  2. Restart Vite: `npm run dev`

### Mixed Content Error
- **Cause:** HTTPS site trying to load HTTP Vite assets
- **Symptoms:** Console shows "Mixed Content" errors
- **Fix:**
  1. Unsecure the site: `herd unsecure $SITE_NAME`
  2. Update APP_URL to use `http://` instead of `https://`
  3. Run `php artisan config:clear`
  4. Restart Vite

### White page / Assets not loading
- **Cause:** Vite running from wrong directory or wrong port
- **Fix:**
  1. Kill all Vite: `pkill -f "node.*vite"`
  2. Remove hot file: `rm -f public/hot`
  3. Restart from worktree: `npm run dev`

### Vite uses wrong URL
- **Cause:** APP_URL in .env not updated
- **Fix:** Update APP_URL to match Herd site name

### Missing vendor directory
- **Cause:** Worktrees don't share vendor/
- **Fix:** Run `composer install` in worktree

### Missing node_modules
- **Cause:** Worktrees don't share node_modules/
- **Fix:** Run `npm install` in worktree

### Neo4j/DB connection errors
- **Cause:** Missing .env file
- **Fix:** Copy .env from main project

### Port already in use
- **Cause:** Another Vite instance running
- **Fix:** Kill existing Vite processes: `pkill -f "node.*vite"`

### Permission issues with Herd
- **Cause:** Herd needs to access worktree
- **Fix:** Ensure worktree is in a Herd-accessible path

## Checklist

Before considering setup complete, verify:

- [ ] Worktree created at `.worktrees/$SITE_NAME`
- [ ] Herd link created (`herd link $SITE_NAME`)
- [ ] Site is NOT secured (use HTTP, not HTTPS)
- [ ] vite.config.js has `host: 'localhost'` and `cors: true`
- [ ] .env copied and APP_URL updated to `http://$SITE_NAME.test`
- [ ] SESSION_DOMAIN updated to `$SITE_NAME.test`
- [ ] SESSION_SECURE_COOKIE=false added for HTTP
- [ ] `composer install` completed successfully
- [ ] `npm install` completed successfully
- [ ] Old Vite processes killed
- [ ] `npm run dev` running from worktree directory
- [ ] Site accessible at `http://$SITE_NAME.test` (no white page)

## CRITICAL: Working Directory After Setup

**After worktree setup is complete, ALL subsequent work MUST use the worktree path.**

The worktree is a separate copy of the codebase. Using the main repo path will edit the wrong files.

- **Worktree path:** `/path/to/project/.worktrees/$SITE_NAME/`
- **All file reads, edits, and writes** must use the worktree absolute path (e.g., `/path/to/project/.worktrees/$SITE_NAME/app/...`)
- **All Bash commands** (artisan, tests, pint, etc.) must run from the worktree directory
- **All git operations** must run from the worktree directory

**After setup, remind the user and any subsequent agents:** "All work for this task should use the worktree at `/path/to/project/.worktrees/$SITE_NAME/`. The site is accessible at `http://$SITE_NAME.test`. Do not modify files in the main project directory."

## Integration

**Pairs with:**
- Git worktree workflows
- Any Laravel development workflow