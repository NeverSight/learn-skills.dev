---
name: upgrade-js-deps
description: Upgrade JavaScript dependencies using npm-check-updates, then run post-upgrade checks to ensure nothing is broken.
allowed-tools: [
    Bash(npx npm-check-updates *),
    Bash(make npm-install *),
    Bash(make npm-build *),
    Bash(make npm-type-check *),
    Bash(make test *),
]
---

## Your task

Upgrade all JavaScript dependencies and verify nothing is broken.

### Step 1: Check for available upgrades

Run `npx npm-check-updates` to see what upgrades are available. Review the output and
present the list to the user.

### Step 2: Update package.json

Run `npx npm-check-updates -u` to update `package.json` with the new versions.

### Step 3: Install updated dependencies

Run `make npm-install` to install the upgraded dependencies and update `package-lock.json`.

### Step 4: Run post-upgrade checks

Run these checks sequentially, stopping if any step fails:

1. **TypeScript type checking**: Run `make npm-type-check` and report any new type errors.
2. **Build**: Run `make npm-build` to verify the production build still works.
3. **Tests**: Run `make test` to verify the test suite still passes.

### Step 5: Summarize and commit

Summarize what was done:
- Which packages were upgraded (notable version changes)
- Whether any type errors were introduced
- Whether the build succeeded
- Whether all tests passed
- Any issues that need manual attention

If there were failures, present the issues and ask how the user wants to proceed.

If everything passed, ask the user if they'd like to commit the changes. If yes, commit
using the `/commit` skill.
