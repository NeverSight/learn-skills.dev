---
name: social-preview
description: "Generate Open Graph social preview images (1280x640) for GitHub repositories. Creates branded OG images that display when repos are shared on Twitter, LinkedIn, and Slack. Supports custom templates, dark/light themes, and automated generation."
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: devops
  domain: github
  updated: 2026-03-19
  tested: 2026-03-19
  tested_with: "Claude Code v2.1"
---

# Social Preview

Generate Open Graph social preview images (1280x640px) for GitHub repositories. The social preview is the single highest-leverage visual asset when repos are shared on Twitter, LinkedIn, Slack, and Discord.

## Install

```bash
claude skill install social-preview
```

## When to Use

- New public repo needs a social preview before sharing
- Rebranding a project (new colors, name change, logo update)
- Major release or launch -- refresh the preview to reflect the milestone
- Before marketing pushes (LinkedIn posts, Twitter threads, blog features)
- Audit existing repos to catch missing or outdated social previews

## Usage

```
/social-preview generate [repo-path]   # Create OG image from repo context
/social-preview audit [repo-path]      # Check if social preview is set, dimensions correct
```

Default `repo-path` is the current working directory if omitted.

---

## Procedure: Generate

Execute each step in order. Do not skip steps.

### Step 0: Parse Command

Expect: `/social-preview {mode} [repo-path]`

Extract mode (`generate` or `audit`). If missing or invalid:
```
Error: Invalid or missing mode.
Usage:
  /social-preview generate [repo-path]
  /social-preview audit [repo-path]
```
STOP.

Validate `repo-path` is a directory containing `.git`. Default to cwd if omitted.

### Step 1: Scan Repo for Context

Gather:
- **Project name** -- from `package.json` name, `Cargo.toml` [package] name, `pyproject.toml` name, or directory name
- **Description/tagline** -- from package.json description, repo description, or ask user
- **Primary language** -- from file extensions, package manager files, or `gh repo view --json primaryLanguage`
- **Logo/icon** -- check for `logo.png`, `logo.svg`, `icon.png`, `icon.svg`, `.github/logo.png`, `assets/logo.*`, `branding/logo.*`
- **Git remote** -- `git remote get-url origin` to extract owner/repo
- **Existing social preview** -- `gh api repos/{owner}/{repo}` to check current state

### Step 2: Select Template

Present template options to the user:

1. **Dark** (recommended) -- Dark background (#0d1117 or #141414), light text. Highest contrast, best performance on most feeds.
2. **Light** -- Light background (#fafbfc), dark text. Matches certain brand aesthetics.
3. **Minimal** -- Just project name + tagline, no decoration. Clean and typographic.

Ask: "Which template? [dark/light/minimal] (default: dark)"

If the repo has established brand colors (detected from CSS variables, tailwind config, or user-specified), offer to use those as accent colors.

### Step 3: Generate HTML Template

Create a standalone HTML file (1280x640px viewport) containing:

- **Project name** -- large, prominent, max 40 characters displayed. Use system-safe fonts only (no external font dependencies).
- **One-line description/tagline** -- below the name, lighter weight, max 80 characters.
- **Primary language/tech icon** (optional) -- simple text-based indicator or Unicode symbol. No external image dependencies.
- **Author/org attribution** (optional) -- small, bottom corner. GitHub username or org name.
- **Background** -- solid color, CSS gradient, or subtle CSS pattern (dots, grid). No external images.

Write the HTML file to `{repo-path}/social-preview.html` (or `/tmp/social-preview-{repo-name}.html` if user prefers).

### Step 4: Render to PNG

Guide the user through one of three rendering paths:

**Option A -- Browser screenshot (simplest, no deps):**
1. Open the HTML file in any browser
2. Set viewport to exactly 1280x640
3. Take a full-page screenshot
4. Save as PNG

**Option B -- Puppeteer/Playwright (automated, requires Node):**
```bash
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 640, deviceScaleFactor: 2 });
  await page.goto('file:///PATH/TO/social-preview.html', { waitUntil: 'networkidle0' });
  await page.screenshot({ path: 'social-preview.png', clip: { x: 0, y: 0, width: 1280, height: 640 } });
  await browser.close();
})();
"
```

**Option C -- Cloud renderer:**
- Use `npx @vercel/og` or a hosted OG image service if the user prefers URL-based generation.

### Step 5: Set as Social Preview

Guide the user through one of two methods:

**Method A -- GitHub UI:**
1. Go to `https://github.com/{owner}/{repo}/settings`
2. Scroll to "Social preview"
3. Click "Edit" -> "Upload an image..."
4. Upload the generated PNG
5. Click "Save"

**Method B -- GitHub API:**
```bash
gh api repos/{owner}/{repo} \
  --method PATCH \
  --field "social_preview=$(base64 -i social-preview.png)"
```

Note: The GitHub REST API does not directly support uploading social preview images via base64. The UI method is the most reliable. For automation, use the repository settings page.

### Step 6: Verify

Provide validation URLs:
- Twitter Card Validator: `https://cards-dev.twitter.com/validator`
- Facebook Sharing Debugger: `https://developers.facebook.com/tools/debug/`
- LinkedIn Post Inspector: `https://www.linkedin.com/post-inspector/inspect/`
- Open Graph Debugger: `https://opengraph.dev/`

Tell user to paste the repo URL and verify the preview renders correctly.

---

## Procedure: Audit

### Step 1: Check Repo

Validate repo-path is a git repo with a remote.

### Step 2: Fetch Current Social Preview State

```bash
gh api repos/{owner}/{repo} --jq '.description, .homepage'
```

Check if a custom social preview image is set (GitHub auto-generates one if not).

### Step 3: Report

```
=== Social Preview Audit: {repo-name} ===

Custom preview set: {YES / NO (using auto-generated)}
Description:       {repo description or "MISSING -- add one"}
Homepage URL:       {homepage or "not set"}

Recommendations:
  - {actionable items: missing preview, missing description, etc.}

Run /social-preview generate to create one.
```

---

## Design Principles

- **Readable at thumbnail size.** Social feeds show previews at ~400px wide. Text must be legible at that scale.
- **High contrast.** Dark backgrounds with light text outperform on most platforms. Minimum 4.5:1 contrast ratio.
- **No small text.** If it won't be readable at 400px wide, remove it. Project name should be 48-72px at 1280px canvas.
- **2:1 aspect ratio.** 1280x640 is the standard. Platforms crop outside this ratio.
- **No external dependencies.** HTML must render with zero network requests. System fonts only. Inline all CSS.
- **Keep text minimal.** Project name + one-line tagline. Nothing else is guaranteed to be readable.
- **Test at actual share size.** Always preview at 400x200 before finalizing.

## Key Principles

1. Dark backgrounds perform better across Twitter, LinkedIn, and Slack feeds.
2. Keep text to two lines maximum: name + tagline.
3. Test at actual share size (400px wide), not at full resolution.
4. PNG format, under 1MB. Avoid JPEG for text-heavy images (compression artifacts).
5. Update the preview when the project description or branding changes.
6. A missing social preview is worse than a simple one -- GitHub's auto-generated preview is generic and forgettable.

## Files

- **HTML template:** `{repo-path}/social-preview.html` or `/tmp/social-preview-{repo-name}.html`
- **PNG output:** `{repo-path}/social-preview.png`

## Anti-Patterns

- No external font CDN links -- system fonts only for guaranteed rendering
- No images or logos that require network requests -- inline SVG or omit
- No text below 24px at 1280px canvas (will be illegible at thumbnail size)
- No busy backgrounds or photographic backgrounds -- solid or gradient only
- No more than 3 colors total (background, primary text, accent)
- No rounded corners or complex shapes that get lost at small sizes
- Do not include full URLs in the image -- waste of space, unreadable at thumbnail
