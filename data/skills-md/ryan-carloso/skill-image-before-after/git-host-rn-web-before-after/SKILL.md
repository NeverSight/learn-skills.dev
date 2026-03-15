---
name: git-host-rn-web-before-after
description: This skill should be used when a user needs automated BEFORE/AFTER screenshots for a React Native web app and wants to commit images to a feature branch and update or create a GitHub pull request or GitLab merge request by auto-detecting the provider from origin.
---

# Git Host RN Web Before/After Screenshot Skill

Keep scope narrow: capture screenshots and review artifacts only. Do not implement product features.

## Purpose

Capture deterministic BEFORE and AFTER screenshots for React Native Web, commit screenshot assets on a feature branch, and update review content.

This skill can:

- Use one run (`both`) or two runs (`before` then `after`).
- Auto-detect GitHub vs GitLab using `git remote get-url origin`.
- Update an existing PR/MR when `--review-id` is provided.
- On GitLab, auto-create an MR when `--review-id` is omitted.

## Output Folder Convention

By default, screenshots are saved in a `/screenshots/` folder in the project root:

- `/screenshots/<branch>-<timestamp>/before.png`
- `/screenshots/<branch>-<timestamp>/after.png`

Example folder name:

- `feature-login-redesign-20260301-163522Z`

Notes:

- The `/screenshots/` folder is automatically created if it does not exist.
- Folder name is built from feature branch + UTC timestamp.
- The same folder is reused for `before` then `after` runs via context.
- If you pass `--before-path` or `--after-path`, custom paths are respected.

## Target Route Resolution

By default, the script does not hardcode a screen path.

- If `--url` is provided, it uses that URL.
- If `--url` is omitted, it infers a route from the feature diff against base (`<base>...<feature>`), prioritizing changed files under `src/app`.
- If no route can be inferred, it falls back to `/`.

## Files

- `scripts/screenshot-before-after.sh`: Main workflow.
- `scripts/capture.js`: Puppeteer capture helper.
- `scripts/package.json`: Runtime dependencies and setup helpers.

## Prerequisites

- `git`
- `node` (18+ recommended)
- `pnpm`
- Chromium/Chrome binary available to Puppeteer
- Optional for automatic review description updates:
  - `gh` for GitHub
  - `glab` for GitLab

## Setup (Step by Step)

Run from this skill directory:

```bash
cd skills/git-host-rn-web-before-after/scripts
pnpm run setup
pnpm run browser:install
chmod +x screenshot-before-after.sh
```

Notes:

- `pnpm run browser:install` installs Playwright Chromium in local user cache.
- On macOS, a common browser path is:
  - `~/Library/Caches/ms-playwright/chromium-1208/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`
- If your environment has another Chromium path, pass it via `--browser`.

## Usage

Provider is always auto-detected from `origin`.
Do not ask users to pick GitHub or GitLab when `origin` exists.

### One-step (recommended)

```bash
./screenshot-before-after.sh --repo /path/to/app --mode both
```

With explicit review ID:

```bash
./screenshot-before-after.sh --repo /path/to/app --review-id 123 --mode both
```

### Two-step

```bash
# Step 1: BEFORE only
./screenshot-before-after.sh --repo /path/to/app --review-id 123 --mode before

# Step 2: AFTER only (reuses context)
./screenshot-before-after.sh --repo /path/to/app --mode after
```

### RN Web debug mode (recommended for Expo)

Use explicit URL, port, and loading options for deterministic captures when needed.
If `--url` is omitted, route is inferred automatically from the branch diff:

```bash
./screenshot-before-after.sh \
  --repo /path/to/app \
  --mode both \
  --server-cmd "pnpm web -- --port 8082 --clear" \
  --server-port 8082 \
  --wait-timeout 120 \
  --wait-until networkidle2 \
  --delay-ms 8000 \
  --browser "/absolute/path/to/chromium"
```

Optional override for a specific page:

```bash
./screenshot-before-after.sh \
  --repo /path/to/app \
  --mode both \
  --url http://127.0.0.1:8082/some/route
```

### Manual server mode

```bash
./screenshot-before-after.sh \
  --repo /path/to/app \
  --mode both \
  --no-server \
  --server-url http://127.0.0.1:19006 \
  --browser "/absolute/path/to/chromium"
```

## GitLab MR behavior

- If `--review-id` is provided, the script updates that MR description.
- If `--review-id` is omitted on GitLab, the script attempts MR creation using push options and prints the MR URL.
- If `glab` is not authenticated, screenshot capture/commit/push still works and the script prints markdown to paste manually.

## Context JSON

Default context path:

`~/.config/opencode/skills/screenshot-skill/state/context.json`

Fields:

- `repo_path`
- `base_branch`
- `feature_branch`
- `review_id`
- `server_url`
- `before_path`
- `after_path`
- `run_folder_name`
- `before_commit`
- `after_commit`
- `timestamp`

Auto mode behavior:

- If context matches `repo_path + feature_branch` and has BEFORE but no AFTER, run AFTER.
- Otherwise run BOTH.

## Operational Notes

- Requires one of these app scripts in target `package.json`:
  - `scripts.web`
  - `scripts["start:web"]`
  - `scripts["web:dev"]`
- Normalizes `--base-branch` so `origin/main` and `main` are both valid.
- Restores the original git branch on exit, including failure paths.
- Prevents write outside repo for screenshots (rejects absolute/traversal paths).
- Uses Node-based server readiness checks (no curl dependency).
- Uses bash-compatible parsing that works in macOS default shell environments.
- Inferred target route comes from app route file changes in diff (`src/app/**`).
- Prints a final action checklist (what was done) at the end of each run.

## Troubleshooting

- **Port already in use**: pass `--server-cmd "pnpm web -- --port 8082 --clear" --server-port 8082`.
- **Expo asks for interactive input**: force explicit `--port` and avoid auto-switch prompts.
- **`window is not defined` or other app runtime error**: this is an app issue, not a skill issue; screenshots will reflect the error state.
- **MR update fails with `glab` auth**: run `glab auth login`, or use printed markdown manually.
- **GitLab push options fail on multiline description**: script now compacts template body for push-option compatibility.
- **No provider CLI installed**: capture/commit/push continues; script prints markdown snippet for manual review description paste.
