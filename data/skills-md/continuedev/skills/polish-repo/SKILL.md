---
name: polish-repo
description: Polish an open-source repository with branding, community files, README overhaul, OG card, usage skill, PR checks, and publishing setup. Designed as a reusable template for Continue repos.
metadata:
  author: continuedev
  version: "1.0.0"
---

# Polish Repository

You are polishing an open-source repository to production quality. Follow each step in order, adapting to the project's language, ecosystem, and existing state.

## Step 1: Gather context

Before making any changes, understand what you're working with:

1. **Read the package manifest** — `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`, etc. Note the project name, description, license field, and any existing scripts.
2. **Check for CI workflows** — look in `.github/workflows/` for existing build, test, and release pipelines.
3. **Check for branding assets** — look for banner images, logos, or OG cards in `.github/assets/`, `public/`, or the repo root. If none exist, download the shared Continue banner from `https://raw.githubusercontent.com/continuedev/continue/main/media/github-readme.png` and save it as `.github/assets/continue-banner.png`.
4. **Determine ecosystem** — npm/Node.js, Go, Rust, Python, etc. This affects publishing setup and contributing instructions.
5. **Read the existing README** — understand what documentation already exists so you preserve and improve it rather than losing content.
6. **Check for existing community files** — `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, issue templates, PR templates.

## Step 2: README overhaul

Restructure the README with this template:

```markdown
<p align="center">
  <a href="https://continue.dev">
    <img src=".github/assets/continue-banner.png" width="800" alt="Continue" />
  </a>
</p>

<h1 align="center">{project-name}</h1>

<p align="center">{one-line description}</p>

---

## Why?

[Before/after comparison or 2-3 sentences explaining the problem this solves]

## Table of Contents

[Links to all sections]

## Quick start
[Existing quick start content — preserve and improve]

[... all existing documentation sections ...]

## Contributing
[Link to CONTRIBUTING.md]

## License
[Link to LICENSE with copyright line]

---

<p align="center">Built by <a href="https://continue.dev">Continue</a></p>
```

Key principles:
- **No shields.io badges** — keep the header clean
- **Preserve all existing content** — don't lose documentation, just restructure
- **Add a "Why?" section** — show the before/after or explain the value proposition concisely
- **Add TOC** — for any README with more than 5 sections
- **Add Contributing + License sections** at the bottom

## Step 3: Community files

Create these files in `.github/` (skip any that already exist and are adequate):

### LICENSE (repo root)

All Continue repos use the **Apache-2.0** license. Create `LICENSE` at the repo root with the full Apache License 2.0 text and this copyright notice at the end:

```
Copyright (c) 2025 Continue Dev, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
```

Also ensure the `license` field in the package manifest (`package.json`, `Cargo.toml`, etc.) is set to `Apache-2.0`.

### CONTRIBUTING.md

Include:
- Dev setup instructions (clone, install, build, test)
- Project structure overview
- Conventional Commits convention (`feat:`, `fix:`, `docs:`, etc.)
- PR process
- Link to bug report template

### SECURITY.md

Include:
- Report to **security@continue.dev**
- 48-hour acknowledgment SLA
- Scope section specific to the project's attack surface (e.g., SSRF for fetch-based tools, injection for template engines)
- Out-of-scope items (upstream dependencies, requires existing access)

### Issue templates (`.github/ISSUE_TEMPLATE/`)

**`bug_report.yml`** — YAML form with:
- Version input
- Environment/framework version input
- Relevant dropdown (project-specific — e.g., detection method for next-geo, platform for CLI tools)
- Description textarea
- Repro steps textarea
- Logs textarea (with `render: shell`)

**`feature_request.yml`** — YAML form with:
- Problem textarea
- Proposed solution textarea
- Alternatives considered textarea

**`config.yml`** — Disable blank issues:
```yaml
blank_issues_enabled: false
```

### PULL_REQUEST_TEMPLATE.md

```markdown
## Description

<!-- What does this PR do? Why? -->

## Type of change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactor
- [ ] Other (describe below)

## Checklist

- [ ] Tests added/updated
- [ ] Types are correct
- [ ] Commit messages follow Conventional Commits
- [ ] README updated (if applicable)
```

### release.yml

Categorize GitHub release notes:

```yaml
changelog:
  categories:
    - title: New Features
      labels:
        - enhancement
    - title: Bug Fixes
      labels:
        - bug
    - title: Documentation
      labels:
        - documentation
    - title: Other
      labels:
        - "*"
```

### What to skip

- **FUNDING.yml** — Continue is VC-backed, not seeking sponsorships
- **CODE_OF_CONDUCT.md** — Only add if the project has an active community with multiple external contributors

## Step 4: OG card

Create `.github/assets/og-card.html` — a self-contained 1280x640 HTML file that can be screenshotted for the GitHub social preview.

Copy the watercolor background image from another Continue repo's `.github/assets/og-bg.png` (e.g., `next-geo`) into `.github/assets/` to use as the ambient background.

**Design — dark theme with watercolor background and Continue logo:**
- **Background:** Dark navy (`#1a1a2e`) as the base color
- **Watercolor image:** Full-bleed `og-bg.png` behind everything via `background: url('./og-bg.png') center/cover no-repeat`
- **Gradient overlay:** Left-to-right gradient darkening the left side for text readability: `rgba(10, 10, 30, 0.7)` on the left fading to `rgba(10, 10, 30, 0.15)` on the right
- **Typography:** IBM Plex Sans (light 300 weight for the title, regular 400 for tagline) + IBM Plex Mono (400 for labels and the install command). Load from Google Fonts.
- **Title:** Large (~80px), light weight, tight tracking (-2px), color `rgba(255, 255, 255, 0.95)`
- **Tagline:** Below the title, ~24px, `rgba(255, 255, 255, 0.6)`
- **Label:** Small monospace "CONTINUE" label above the title, uppercase, wide tracking (0.2em), `rgba(255, 255, 255, 0.5)`
- **Install pill:** Monospace install command (e.g., `npm install {package}`) in a pill with `rgba(255, 255, 255, 0.08)` background and `rgba(255, 255, 255, 0.15)` border
- **Continue logo:** Large (~520px) Continue SVG icon on the right side, vertically centered, white fill — serves as the primary visual element
- **Layout:** Text content on the left (padded 100px), logo on the right
- **Overall feel:** Dark, atmospheric, professional — the watercolor background adds visual richness while the gradient keeps text readable

Reference implementation: `next-geo/.github/assets/og-card.html`

After creating the HTML, also **pre-crop** the background image to exactly 1280x640 so headless rendering doesn't depend on `object-fit`:

```bash
sips --resampleWidth 1280 .github/assets/og-bg.png --out /tmp/og-bg-resized.png
sips --cropOffset 0 0 -c 640 1280 /tmp/og-bg-resized.png --out .github/assets/og-bg-card.png
```

Reference `og-bg-card.png` in the HTML `<img>` tag with explicit `width: 1280px; height: 640px` — no `object-fit` needed.

Then generate the screenshot with Puppeteer (not Chrome's `--screenshot` flag, which leaves rendering artifacts):

```bash
npx -y puppeteer browsers install chrome
node -e "
import puppeteer from 'puppeteer';
const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 640, deviceScaleFactor: 1 });
await page.goto('file://$(pwd)/.github/assets/og-card.html', { waitUntil: 'networkidle0' });
await page.screenshot({ path: '/tmp/og-card.png', clip: { x: 0, y: 0, width: 1280, height: 640 } });
await browser.close();
"
sips -s format jpeg -s formatOptions 85 /tmp/og-card.png --out .github/assets/og-card.jpg
```

**Important:** Verify the image visually before committing — check that the background fills edge to edge with no dark strips or blank space. The image must be under 1MB (JPEG at 85% quality typically produces ~300KB).

Commit `og-card.html` and `og-card.jpg`. The social preview image must be uploaded manually in Settings → General → Social preview (no API for this).

## Step 5: Usage skill

Create a `skill/SKILL.md` that walks a coding agent through installing and using the package/tool in their project. This is the "how do I adopt this?" guide.

Reference example: `next-geo/skill/SKILL.md`

The skill should:
- Have YAML frontmatter with `name`, `description`, and `metadata` (author, version)
- Include prerequisites and environment checks
- Walk through installation step by step
- Cover configuration and integration with existing code
- Include optional advanced steps
- End with verification steps
- Include a troubleshooting section

## Step 6: PR checks

Create `.continue/checks/` with project-specific checks. These checks run on PRs and flag issues that require human judgment — things linters can't catch.

Point the user to [continue.dev/walkthrough](https://continue.dev/walkthrough) for the full guide on writing checks.

Reference example: `next-geo/check/geo.md`

Good checks target:
- Content consistency (e.g., page.md files staying in sync with page.tsx)
- API contract changes that might break consumers
- Configuration changes that affect behavior
- Missing documentation for new features
- Security-sensitive changes

Bad checks (avoid — linters handle these):
- Code style
- Import ordering
- Type errors
- Test coverage thresholds

## Step 7: Publishing setup

If the project will be published to a package registry, set up automated releases.

### For npm packages

See [publishing-npm.md](publishing-npm.md) for the full reference.

Summary:
1. Install semantic-release and plugins as devDependencies
2. Create `release.config.cjs`
3. Create `.github/workflows/release.yaml` with OIDC-based npm publishing
4. Ensure `package.json` has correct `name`, `version`, `repository`, `files`, and `exports`

### For Go CLI tools

See [publishing-go.md](publishing-go.md) for the full reference.

Summary:
1. Create `.goreleaser.yml` with cross-platform build config
2. Create `.github/workflows/release.yml` triggered on `v*` tags
3. Set up version injection via ldflags
4. Document the release process (`git tag v1.0.0 && git push origin v1.0.0`)

## Step 8: Postinstall message (npm packages)

For npm packages that have a companion skill, add a postinstall script that tells users how to get started with a coding agent. This runs after `npm install` and prints a short message.

Create `scripts/postinstall.js`:

```js
#!/usr/bin/env node

// Skip during CI or global installs
if (process.env.CI || process.env.npm_config_global) {
  process.exit(0);
}

const name = "{package-name}";
const skill = "{skill-name}";
const org = "continuedev/skills";

console.log();
console.log(`  ${name} installed.`);
console.log();
console.log(`  Get started with a coding agent:`);
console.log(`    npx skills add ${org} --skill ${skill}`);
console.log();
console.log(`  Then ask your agent: "Set up ${name} in this project."`);
console.log();
```

Then update `package.json`:
- Add `"postinstall": "node scripts/postinstall.js || true"` to `scripts` (the `|| true` prevents install failures if the script errors)
- Add `"scripts"` to the `files` array so it's included in the published package

Key principles:
- **Keep it short** — 5 lines max, no ASCII art, no color codes
- **Fail silently** — use `|| true` so the postinstall never blocks installation
- **Skip in CI** — check `process.env.CI` to avoid noise in automated environments
- **One clear action** — the `npx skills add` command is the main CTA

Reference implementation: `next-geo/scripts/postinstall.js` and `next-geo/package.json`

## Step 9: GitHub repo settings

After all files are committed and pushed, configure the repo via the GitHub API using `gh`. Do **not** ask the user to do these manually — automate them.

### 9a: Description, website, and topics

Use `gh api` to PATCH the repo with description (from the README tagline), homepage URL, and relevant topics:

```bash
gh api repos/{owner}/{repo} --method PATCH --input - <<'EOF'
{
  "description": "{one-line description from README}",
  "homepage": "https://continue.dev",
  "topics": ["relevant", "topics", "for", "the", "project"]
}
EOF
```

Choose topics relevant to the project's ecosystem and purpose (e.g., `webhooks`, `cli`, `go`, `nextjs`, `react`, `automation`).

### 9b: Branch protection ruleset

Create a ruleset requiring PR reviews and status checks on `main`:

```bash
gh api repos/{owner}/{repo}/rulesets --method POST --input - <<'EOF'
{
  "name": "Protect main",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["refs/heads/main"],
      "exclude": []
    }
  },
  "rules": [
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 1,
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": false
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": false,
        "required_status_checks": [
          {
            "context": "{ci-job-name}"
          }
        ]
      }
    }
  ]
}
EOF
```

Set `{ci-job-name}` to match the job name from the CI workflow created in Step 7 (e.g., `test`, `build`, `release`).

### 9c: Social preview (manual)

The social preview image cannot be uploaded via the API. Instruct the user to:

1. Open `.github/assets/og-card.html` in a browser
2. Screenshot at 1280x640
3. Upload in Settings → General → Social preview
