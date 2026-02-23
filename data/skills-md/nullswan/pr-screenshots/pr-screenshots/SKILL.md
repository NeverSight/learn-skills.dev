---
name: pr-screenshots
description: Capture before/after screenshots for pull requests to document visual changes. Supports both agent-browser CLI and Playwright Python approaches. Use when creating PRs with UI changes, comparing visual states between branches, documenting frontend changes for code review, or generating visual diff reports.
allowed-tools: Bash(agent-browser:*), Bash(python:*), Bash(mkdir:*), Bash(gh:*), Bash(git:*), Bash(cat:*), Bash(echo:*)
license: MIT
---

# PR Screenshots

Capture before/after screenshots to document visual changes in pull requests.

**Helper Scripts Available**:
- `scripts/capture_screenshots.py` - Capture screenshots with Playwright
- `scripts/compare_branches.sh` - Automate branch switching and capture
- `scripts/generate_report.py` - Generate markdown comparison report

**Always run scripts with `--help` first** to see usage.

## Decision Tree: Choosing Your Approach

```
Task → Need quick single screenshot?
    ├─ Yes → Use agent-browser CLI (fast, simple)
    │         agent-browser open <url>
    │         agent-browser screenshot <path>
    │
    └─ No → Need batch/automated capture?
        ├─ Multiple pages → Use scripts/capture_screenshots.py
        │
        └─ Full PR workflow → Use scripts/compare_branches.sh
            1. Captures "before" on base branch
            2. Captures "after" on feature branch
            3. Generates comparison report
            4. Optionally attaches to PR
```

## Quick Start: agent-browser CLI

For simple, interactive screenshot capture:

```bash
# Setup
mkdir -p .pr-screenshots/{before,after}

# Capture screenshots
agent-browser open http://localhost:3000
agent-browser wait --load networkidle
agent-browser screenshot --full-page .pr-screenshots/before/home.png

# Multiple viewports
agent-browser viewport 375 812  # Mobile
agent-browser screenshot .pr-screenshots/before/home-mobile.png
```

## Automated Capture: Playwright Script

For batch capture with more control:

```bash
python scripts/capture_screenshots.py --help
python scripts/capture_screenshots.py \
  --url http://localhost:3000 \
  --pages "/" "/login" "/dashboard" \
  --output .pr-screenshots/before \
  --viewports desktop mobile tablet
```

## Full PR Workflow

```bash
# Run the complete workflow
bash scripts/compare_branches.sh --help
bash scripts/compare_branches.sh \
  --base main \
  --feature feature/new-ui \
  --url http://localhost:3000 \
  --pages "/" "/about" \
  --start-cmd "npm run dev"
```

This will:
1. Stash current changes
2. Checkout base branch, start server, capture "before"
3. Checkout feature branch, capture "after"
4. Generate `VISUAL_CHANGES.md` comparison report
5. Optionally post to PR with `--post-to-pr <PR_NUMBER>`

## Example: Manual Workflow

### Step 1: Capture BEFORE (base branch)

```bash
FEATURE_BRANCH=$(git branch --show-current)
git stash --include-untracked
git checkout main

# Start your dev server (in another terminal or background)
# npm run dev &

mkdir -p .pr-screenshots/before
agent-browser open http://localhost:3000
agent-browser wait --load networkidle
agent-browser screenshot --full-page .pr-screenshots/before/home.png
```

### Step 2: Capture AFTER (feature branch)

```bash
git checkout $FEATURE_BRANCH
git stash pop

mkdir -p .pr-screenshots/after
agent-browser open http://localhost:3000
agent-browser wait --load networkidle
agent-browser screenshot --full-page .pr-screenshots/after/home.png
```

### Step 3: Generate Report

```bash
python scripts/generate_report.py \
  --before .pr-screenshots/before \
  --after .pr-screenshots/after \
  --output .pr-screenshots/VISUAL_CHANGES.md
```

### Step 4: Attach to PR

```bash
# Option A: Commit screenshots
git add .pr-screenshots/
git commit -m "Add visual comparison screenshots"
git push

# Option B: Post as PR comment
gh pr comment <PR_NUMBER> --body-file .pr-screenshots/VISUAL_CHANGES.md
```

## Reconnaissance Pattern (from webapp-testing)

When working with dynamic apps, use the reconnaissance-then-action pattern:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:3000')
    page.wait_for_load_state('networkidle')  # CRITICAL: Wait for JS

    # Capture for inspection
    page.screenshot(path='/tmp/inspect.png', full_page=True)

    # Discover elements
    buttons = page.locator('button').all()
    print(f"Found {len(buttons)} buttons")

    browser.close()
```

## agent-browser Commands Reference

| Command | Description |
|---------|-------------|
| `agent-browser open <url>` | Navigate to URL |
| `agent-browser wait --load networkidle` | Wait for page load |
| `agent-browser wait --time 2000` | Wait N milliseconds |
| `agent-browser screenshot <path>` | Capture viewport |
| `agent-browser screenshot --full-page <path>` | Capture full page |
| `agent-browser viewport <width> <height>` | Set viewport size |
| `agent-browser snapshot -i` | Get interactive elements |
| `agent-browser click @ref` | Click element |
| `agent-browser fill @ref "text"` | Fill input |

## Viewport Presets

| Name | Dimensions | Use Case |
|------|------------|----------|
| desktop-xl | 1920x1080 | Large monitors |
| desktop | 1280x720 | Standard desktop |
| tablet | 768x1024 | iPad portrait |
| mobile | 375x812 | iPhone |

## Best Practices

1. **Always wait for networkidle** before capturing dynamic content
2. **Use --full-page** for scrollable pages
3. **Capture multiple viewports** for responsive designs
4. **Add delays for animations**: `agent-browser wait --time 1000`
5. **Include interactive states** (hover, focus, filled forms)
6. **Name files descriptively**: `home-desktop.png`, `login-mobile-filled.png`

## Cleanup

```bash
rm -rf .pr-screenshots/
# Or add to .gitignore
echo ".pr-screenshots/" >> .gitignore
```

## Reference Files

- **scripts/** - Automation scripts:
  - `capture_screenshots.py` - Batch screenshot capture with Playwright
  - `compare_branches.sh` - Full branch comparison workflow
  - `generate_report.py` - Markdown report generator
- **examples/** - Usage examples:
  - `basic_capture.py` - Simple screenshot capture
  - `responsive_capture.py` - Multi-viewport capture
  - `interactive_capture.py` - Capture with interactions
- **templates/** - Report templates:
  - `comparison_report.md` - PR comment template
