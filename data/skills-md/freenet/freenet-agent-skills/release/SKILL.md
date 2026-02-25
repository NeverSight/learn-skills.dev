---
name: release
description: Orchestrate a new Freenet release. Determines next version, shows changelog, confirms with user, and runs the release pipeline. Use when the user says "do a release", "new release", "release", or "/release".
user_invocable: true
license: LGPL-3.0
---

# Freenet Release Skill

## Overview

This skill orchestrates a complete Freenet release. It determines the next version, shows what's changed since the last release, confirms with the user, and runs the automated release pipeline.

## Arguments

- If an argument is provided (e.g., `/release 0.1.133`), use that as the target version
- If no argument is provided, auto-detect the next patch version

## Step 1: Determine Current State

Run these commands to gather release context:

```bash
# Get current version from Cargo.toml
grep "^version" crates/core/Cargo.toml | cut -d'"' -f2

# Get the last release tag
git describe --tags --abbrev=0

# Get commits since last release
git log --oneline $(git describe --tags --abbrev=0)..HEAD
```

**Auto-version logic:** If no version argument was provided, increment the patch version of the current version (e.g., `0.1.132` -> `0.1.133`).

## Step 2: Show Changelog and Confirm

Present the user with:
1. **Current version** and **target version**
2. **Commits since last release** (categorized by conventional commit type)
3. **fdev version** that will be auto-incremented

Then ask the user to confirm before proceeding.

## Step 3: Pre-flight Checks

Before running the release script, verify:

```bash
# Must be on main branch (or a release worktree)
git branch --show-current

# Must have clean working directory
git status --porcelain  # Should be empty

# Must be up to date with origin
git fetch origin main
git rev-parse HEAD  # Compare with:
git rev-parse origin/main
```

If any check fails, inform the user and stop.

### Optional: Create a Release Worktree

To avoid disrupting the main worktree:

```bash
cd ~/code/freenet/freenet-core/main  # or wherever main worktree is
git worktree add -b release-work ../release-X.Y.Z
cd ../release-X.Y.Z
```

Clean up after release:
```bash
git worktree remove ../release-X.Y.Z
git branch -d release-work
```

## Step 4: Run the Release

Execute the release script:

```bash
./scripts/release.sh --version <VERSION> [--skip-tests]
```

The script handles the entire pipeline:
1. **Version bump** - Updates `crates/core/Cargo.toml` and `crates/fdev/Cargo.toml`
2. **Release PR** - Creates a branch, commits, pushes, opens PR with auto-merge
3. **Wait for CI** - Monitors GitHub CI on the release PR (up to 30 min)
4. **Publish crates** - Publishes `freenet` then `fdev` to crates.io
5. **GitHub Release** - Creates tag, generates release notes, creates release
6. **Cross-compile** - Triggered automatically by the tag push
7. **Wait for binaries** - Waits for cross-compile to attach binaries to the release
8. **Gateway updates** - SSHes into all gateways and triggers immediate update
9. **Announcements** - Matrix and River notifications (if tools available)

### Important Options

- `--skip-tests` - Skip local pre-release tests (CI still runs on the PR)
- `--dry-run` - Show what would be done without executing

### Resumability

The release script is **resumable**. If it fails partway through, re-running with the same `--version` will auto-detect completed steps and skip them. State is saved to `/tmp/release-<VERSION>.state`.

You can also resume explicitly: `./scripts/release.sh --resume /tmp/release-<VERSION>.state`

## Step 5: Handle Common Issues

**PR title / Conventional Commits check fails:**
Release PRs must use "build:" prefix (not "chore:"). The commit-msg hook only allows: feat, fix, docs, style, refactor, perf, test, build, ci.
```bash
gh api repos/freenet/freenet-core/pulls/XXXX --method PATCH -f title="build: release X.Y.Z"
```

**Auto-merge not triggering:**
- GitHub auto-merge can take 5-10 minutes after checks pass
- The script waits up to 30 minutes (showing progress every 30s)
- You can manually merge the PR — the script detects manual merges and continues

**Test failures:**
Check CI logs. Either fix the issue or inform the user and ask how to proceed.

## Step 6: Verify Release Artifacts

**CRITICAL: Do NOT announce until cross-compile binaries are available.** The `Build and Cross-Compile` workflow triggers on tag push and takes ~15-20 min to build binaries for all platforms. Gateway auto-update depends on these binaries.

```bash
# Check crates.io publication
cargo search freenet --limit 1

# Check GitHub release exists
gh release view v<VERSION>

# Verify binaries are attached
gh release view v<VERSION> --json assets --jq '.assets[].name'
# Should show: freenet-x86_64-unknown-linux-musl.tar.gz, freenet-aarch64-unknown-linux-musl.tar.gz, etc.

# Monitor cross-compile workflow if binaries not yet available
gh run list --workflow=cross-compile.yml --limit 3
```

## Step 7: Announcements

Only after binaries are confirmed available:

**Matrix** (#freenet-locutus channel):
```bash
# Use matrix-send wrapper if available (handles E2E encryption, retries, timeouts)
matrix-send -r '!ygHfYcXtXmivTbOwjX:matrix.org' -m "Freenet vX.Y.Z released - [summary]. https://github.com/freenet/freenet-core/releases/tag/vX.Y.Z"
```

**River** (Freenet Official room):
```bash
riverctl message send 69Ht4YjZsT884MndR2uWhQYe1wb9b2x77HRq7Dgq7wYE "Freenet vX.Y.Z released - [summary]. https://github.com/freenet/freenet-core/releases/tag/vX.Y.Z"
```

## Step 8: Post-Release Verification

**A release is NOT complete until the network is verified healthy.**

Wait 10-15 minutes for gateways to auto-update, then verify:

1. **Gateway versions updated** — Check that gateways are running the new version
2. **Gateway logs clean** — No new errors, warnings, panics, or log spam
3. **Network health** — Peers connecting, contracts propagating, subscriptions working

If you have access to gateway machines, check logs directly. If you have access to telemetry, monitor network-wide health. The specific verification steps depend on your access level — see your local environment's release skill for machine-specific commands.

**What to look for:**
- **Log spam** — Same message repeating hundreds of times (can fill disks within hours)
- **Rapid log growth** — Normal is ~1MB/hour; much faster indicates a problem
- **New error patterns** — Errors not present before the release
- **Connection failures** — "connection refused", "timeout", "handshake failed"
- **Resource issues** — "out of memory", "no space left", "too many open files"

**If critical issues found:** Roll back immediately, create GitHub issue, announce rollback.

## Rollback

If a release needs to be rolled back:

```bash
# Rollback (keeps crates.io versions)
./scripts/release-rollback.sh --version <VERSION>

# Rollback and yank from crates.io (irreversible!)
./scripts/release-rollback.sh --version <VERSION> --yank-crates

# Dry run
./scripts/release-rollback.sh --version <VERSION> --dry-run
```

## Version Scheme

- **freenet:** `0.1.X` - patch incremented each release
- **fdev:** `0.3.X` - patch auto-incremented by release script (independent versioning)

## Incident Learnings

These are real issues from past releases that the release process has been hardened against:

- **"Text file busy" during deployment** — Deploy script now disables systemd auto-restart, waits for binary release, re-enables after
- **PR title must use "build:" prefix** — Changed from "chore:" to comply with commit-msg hook
- **Matrix announcements can hang** — matrix-send wrapper has 20s timeout and 3 retries; matrix-commander handles E2E encryption that raw curl cannot
- **PATH shadowing** — Old `cargo install freenet` may leave stale binary at `~/.cargo/bin/freenet` shadowing `/usr/local/bin/freenet`; always use absolute paths when verifying versions
- **Binary vs running process mismatch** — Deploying a new binary doesn't mean the service is running it; verify via `systemctl show -p MainPID` + `/proc/PID/exe`, not just binary on disk
- **Don't announce before binaries exist** — Cross-compile takes 15-20 min; gateway auto-update (especially aarch64) depends on release binaries being attached
- **Log spam can fill disks** — Always review logs 10-15 min after release; previous releases introduced logging that consumed disk space within hours

## Gateway Updates

The release script automatically SSHes into all known gateways and triggers `gateway-auto-update.sh --force` immediately after cross-compile binaries are available. This eliminates the 10-minute polling delay that previously caused version mismatch issues (users installing the new version before gateways updated).

Gateways also have a 10-minute polling timer as a fallback. Peers self-update when they detect a version mismatch with the gateway (exit code 42), which triggers `freenet update` automatically.

## Success Criteria

Release is complete when:
- ✓ PR merged to main
- ✓ Published to crates.io
- ✓ GitHub release created with tag and binaries attached
- ✓ Gateways updated to new version
- ✓ Matrix announcement sent
- ✓ River announcement sent
- ✓ Network verified healthy post-release (logs clean, telemetry normal)
