---
name: review
description: Review and process the pull request created by Laravel Shift
arguments: <shift-number>
---

# Review Laravel Shift #$ARGUMENTS

Review and process the pull request created by Laravel Shift #$ARGUMENTS.

## Important: Respect Shift's Changes

**Never revert or undo any changes made by Shift in this PR.** Shift's changes are intentional and authoritative. If you believe a change made by Shift is incorrect or needs to be different, do NOT make any changes — instead, flag it to the user with your findings and let them decide how to proceed.

## Step 1: Detect Platform

Run:
```bash
git remote get-url origin
```

Parse the URL to detect the platform and extract `owner/repo` (handle both SSH and HTTPS formats, strip `.git`):
- `github.com` → **GitHub**
- `gitlab.com` or any other non-Bitbucket host → **GitLab**
- `bitbucket.org` → **Bitbucket**

**GitHub only**: Check that `gh` is installed (`gh --version`). If not, tell the user to install it from https://cli.github.com and stop.

## Step 2: Find the PR and Fetch Details

**GitHub:**
```bash
gh pr list --head "shift-$ARGUMENTS" --json number,title,body,url
```

If no PR is found, try the fallback branch name:
```bash
gh pr list --head "shift-build-$ARGUMENTS" --json number,title,body,url
```

If still no PR is found, tell the user and stop. If multiple PRs are found, show the list and ask which one to use. Store the PR number for subsequent steps.

Then fetch the description, comments, and diff:
```bash
gh pr view {PR_NUMBER} --comments
gh pr diff {PR_NUMBER}
```

**GitLab and Bitbucket:**

The Shift branch is `shift-$ARGUMENTS`. Fetch it and generate the diff:
```bash
git fetch origin shift-$ARGUMENTS
git diff $(git merge-base HEAD origin/shift-$ARGUMENTS)...origin/shift-$ARGUMENTS
```

If that fetch fails, fall back to `shift-build-$ARGUMENTS`:
```bash
git fetch origin shift-build-$ARGUMENTS
git diff $(git merge-base HEAD origin/shift-build-$ARGUMENTS)...origin/shift-build-$ARGUMENTS
```


## Step 3: Check for Uncommitted Changes

Before checking out the PR branch, verify the working directory is clean:
```bash
git status --porcelain
```

If there are any uncommitted changes, **STOP immediately** and tell the user:
> "You have uncommitted changes in your working directory. Please commit or discard them before running this skill."

Do NOT stash, reset, or otherwise modify their working directory. Only proceed if `git status --porcelain` returns empty output.

## Step 4: Checkout the PR Branch

**GitHub:**
```bash
gh pr checkout {PR_NUMBER}
```

**GitLab and Bitbucket** — use native git, checking out whichever branch name succeeded in Step 2:
```bash
git checkout {SHIFT_BRANCH}
```

(`git fetch` was already run in Step 2.)

## Step 5: Understand the Changes

Analyze what Laravel Shift has done:
- What Laravel version upgrade is this (if applicable)?
- What packages were updated?
- What code changes were made?
- Are there any breaking changes noted?

## Step 6: Composer Update

First, check whether `composer.json` was changed as part of this PR:

**GitHub:**
```bash
gh pr diff {PR_NUMBER} --name-only | grep -q "^composer\.json$"
```

**GitLab and Bitbucket:**
```bash
git diff $(git merge-base HEAD origin/{SHIFT_BRANCH})...origin/{SHIFT_BRANCH} --name-only | grep -q "^composer\.json$"
```

If `composer.json` was **not** changed, skip the rest of this step entirely and proceed to Step 7.

If `composer.json` **was** changed, scan it for any `dev-*` version constraints (e.g. `"dev-main"`, `"dev-master"`, `"dev-fix-something"`). For each one found:
1. Look up the package on Packagist to check if a stable release exists: `composer show {package} --all`
2. If a compatible stable version is available, update the constraint in `composer.json` to the appropriate semver range (e.g. `^1.2`) and track it as a swapped dependency for the summary in Step 10
3. If no stable release exists, leave the `dev-*` constraint as-is

Then run `composer update`.

After running (whether it succeeds or fails):

**GitLab and Bitbucket only** — ask the user to paste the PR comments:
> "Please paste any comments from the pull request here, or let me know if there are none."

Then scan the pasted comments for any linked Shift suggestions — these are typically laravelshift.com URLs mentioned in comments recommending a follow-up Shift to run.

When collecting these suggestions:
- Preserve comment order — surface them in the order they appear
- **Exclude the last comment** if it contains Shift links or "you're now running the latest version of Laravel" — set it aside and surface it in Step 10 instead
- If any remaining (non-last) comments contain Shift suggestions, surface them to the user now:

> "The PR suggests running additional Shifts: [list links in comment order]. Would you like to run any of these before continuing?"

If `composer update` failed, attempt to systematically resolve the incompatibilities before stopping:
1. Read the error output carefully to identify which packages have conflicting version constraints
2. For each conflicting package, check the latest compatible version: `composer show {package} --all` or look up the package on packagist.org
3. Update the version constraint in `composer.json` to one that satisfies all dependencies, then re-run `composer update`
4. Repeat for any remaining conflicts
5. If a conflict involves a package that has a suggested follow-up Shift (from comments above), surface that to the user as the recommended resolution instead of manually editing constraints
6. If you cannot resolve the incompatibilities after a systematic attempt, stop and explain exactly which packages are conflicting and why, so the user can decide how to proceed

## Step 7: Act on Instructions

Follow any instructions given in the PR description or comments. This typically includes:
- Running migrations
- Updating configuration files
- Making code changes that Shift couldn't automate
- Addressing deprecations

Pay special attention to the "Automate more with AI..." section of each step, since it's specifically directed towards LLM comprehension.

## Step 8: Handle Optional Upgrades

For any changes marked as "optional" in the PR:
- **Small changes** (one-liner, simple config tweaks, straightforward updates): Just do them automatically
- **Medium to large changes** (new features, architectural changes, changes requiring decisions): Ask the user before proceeding

## Step 9: Test the Application

After making changes:
1. Run `php artisan test --compact` to verify tests pass
2. Fix code style on changed files: check `composer.json` for `laravel/pint` or `friendsofphp/php-cs-fixer` (in that priority order) and run the first one found. Use the `--dirty` flag for Pint. If none are found, skip this step.
3. If tests fail, investigate and fix the issues

## Important: Do Not Commit or Push

Do NOT commit any changes or push to the remote. Leave all changes as uncommitted modifications in the working directory so the user can review them before committing.

## Step 10: Report Back

Summarize:
- What changes were made by Shift
- What additional changes you made
- Any `dev-*` dependencies that were swapped for a stable release (package name, old constraint → new constraint)
- Any optional upgrades you skipped (and why they need user input)
- Test results
- Any remaining action items

End with: "Would you like to merge this PR?"

If the user confirms they want to merge:
1. Check for any uncommitted local changes: `git status --porcelain`
2. If there are uncommitted changes:
   - Check if the only changed files match `composer.*` (i.e. `composer.json` and/or `composer.lock`). If so, stage and commit them automatically with the message `composer update` — do not prompt the user.
   - Otherwise, offer to commit them:
     > "You have uncommitted local changes. Would you like me to commit them for you with a summary?"
     If the user agrees, stage all changes and commit using "Finalize upgrade" as the subject and the summary from Step 10 as the commit body.
     If the user declines, wait for them to confirm they've committed their changes before proceeding.
3. Once the working directory is clean, check if the branch has unpushed commits: `git log origin/{BRANCH}..HEAD`
4. If there are unpushed commits, push them: `git push`
5. Merge using the appropriate method for the platform:

**GitHub:**
```bash
gh pr merge {PR_NUMBER} --merge --delete-branch
```

**GitLab and Bitbucket** — the branch has already been pushed. Tell the user:
> "Please merge the pull request on {platform} and delete the source branch."

If the last PR comment contained Shift links (set aside in Step 6):
- If the comment contains "you're now running the latest version of Laravel":
  - If there were Shift suggestions from non-last comments (surfaced in Step 6), append:
    > "Congratulations, you're now running the latest version of Laravel!"
    >
    > "Once merged, the next suggested Shifts to run are: [link(s) from non-last comments, in comment order]."
  - Otherwise, append:
    > "Congratulations, you're now running the latest version of Laravel!"
    >
    > "Once merged, consider running the [Laravel Fixer](https://laravelshift.com/laravel-fixer) to clean up any remaining issues."
- Otherwise, append:
  > "Once merged, the next suggested Shift to run is: [link(s)]"
