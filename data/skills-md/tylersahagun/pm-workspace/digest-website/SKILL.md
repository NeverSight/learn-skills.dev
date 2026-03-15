---
name: digest-website
description: Generate a shareable website from digests with newspaper-style design and past issues archive. Use when running /publish-digest or when user wants a public digest page.
---

# Digest Website Generator

Transform markdown digests into a polished, shareable website inspired by [Dia Browser's release notes](https://www.diabrowser.com/release-notes/latest).

## When to Use

- Running `/publish-digest` or `/publish-digest [date]`
- User asks for "shareable page", "public digest", or "release notes page"
- Creating a web presence for weekly/daily updates
- Generating an archive of past issues

## Design Inspiration

Reference: https://www.diabrowser.com/release-notes/latest

Key elements:

- **Newspaper/editorial aesthetic** - Clean, typographic focus
- **Issue numbering** - Sequential issue numbers (No. 001, 002, etc.)
- **Timestamp + location** - "January 23, 2026 • San Francisco, USA"
- **Past issues archive** - Clickable list of previous issues
- **Minimal color palette** - Black, white, subtle accent
- **Large typography** - Headlines that command attention
- **Generous whitespace** - Editorial breathing room

## Site Structure

```
docs/
├── index.html                    # Latest issue (redirects or shows latest)
├── issues/
│   ├── 001.html                  # Issue 001 (oldest)
│   ├── 002.html
│   ├── ...
│   └── latest.html              # Symlink/redirect to newest
├── archive.html                  # All past issues
├── assets/
│   ├── style.css                # Shared styles
│   └── logo.svg                 # AskElephant logo
└── CNAME                        # Custom domain (optional)
```

## Issue Numbering Schema

Track issue numbers in a manifest file:

**`pm-workspace-docs/status/activity/digest-manifest.json`**:

```json
{
  "$schema": "digest-manifest-v1",
  "site_title": "AskElephant Weekly",
  "tagline": "What shipped this week",
  "location": "San Francisco, USA",
  "issues": [
    {
      "number": 1,
      "type": "weekly",
      "date": "2026-01-10",
      "week": "W02",
      "source": "digest-2026-W02.md",
      "published": "2026-01-10T17:00:00Z",
      "headline": "Global Chat Goes Live"
    },
    {
      "number": 2,
      "type": "weekly",
      "date": "2026-01-17",
      "week": "W03",
      "source": "digest-2026-W03.md",
      "published": "2026-01-17T17:00:00Z",
      "headline": "HubSpot Workflow Builder"
    },
    {
      "number": 3,
      "type": "weekly",
      "date": "2026-01-24",
      "week": "W04",
      "source": "digest-2026-W04.md",
      "published": "2026-01-24T17:00:00Z",
      "headline": "Dialpad Integration Now Live"
    }
  ],
  "current_issue": 3,
  "app_version_pattern": "2026.W{week}.{patch}"
}
```

## HTML Template

### Latest Issue Page (`index.html`)

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AskElephant Weekly | Latest</title>
    <meta name="description" content="What shipped this week at AskElephant" />
    <meta
      property="og:title"
      content="AskElephant Weekly - Issue {{ISSUE_NUMBER}}"
    />
    <meta property="og:description" content="{{HEADLINE}}" />
    <meta property="og:image" content="/assets/og-image.png" />
    <link rel="stylesheet" href="/assets/style.css" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link
      href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,700;1,6..72,400&family=Inter:wght@400;500;600&display=swap"
      rel="stylesheet"
    />
  </head>
  <body>
    <div class="container">
      <!-- Masthead -->
      <header class="masthead">
        <div class="masthead-meta">
          <time datetime="{{ISO_DATE}}">{{FORMATTED_DATE}}</time>
          <span class="separator">•</span>
          <span class="location">San Francisco, USA</span>
        </div>
        <div class="masthead-issue">
          <span class="issue-label">Issue No.</span>
          <span class="issue-number">{{ISSUE_NUMBER_PADDED}}</span>
        </div>
      </header>

      <!-- Title -->
      <div class="title-block">
        <h1 class="site-title">AskElephant Weekly</h1>
        <p class="tagline">What shipped this week</p>
      </div>

      <!-- Headline -->
      <article class="headline-card">
        <h2 class="headline">{{HEADLINE}}</h2>
        <p class="headline-description">{{HEADLINE_DESCRIPTION}}</p>
      </article>

      <!-- Stats Banner -->
      <div class="stats-banner">
        <div class="stat">
          <span class="stat-value">{{FEATURES_COUNT}}</span>
          <span class="stat-label">New Features</span>
        </div>
        <div class="stat">
          <span class="stat-value">{{IMPROVEMENTS_COUNT}}</span>
          <span class="stat-label">Improvements</span>
        </div>
        <div class="stat">
          <span class="stat-value">{{BUGS_COUNT}}</span>
          <span class="stat-label">Bugs Fixed</span>
        </div>
      </div>

      <!-- Content Sections -->
      <main class="content">
        {{#if FEATURES}}
        <section class="section">
          <h3 class="section-title">New Features</h3>
          <ul class="feature-list">
            {{#each FEATURES}}
            <li>
              <strong>{{this.title}}</strong>
              {{#if this.description}}<span class="item-desc"
                >— {{this.description}}</span
              >{{/if}}
            </li>
            {{/each}}
          </ul>
        </section>
        {{/if}} {{#if IMPROVEMENTS}}
        <section class="section">
          <h3 class="section-title">Improvements</h3>
          <ul class="item-list">
            {{#each IMPROVEMENTS}}
            <li>{{this}}</li>
            {{/each}}
          </ul>
        </section>
        {{/if}} {{#if BUGS_COUNT}}
        <section class="section">
          <h3 class="section-title">Bugs Fixed</h3>
          <p class="bugs-summary">{{BUGS_COUNT}} bugs squashed this week</p>
        </section>
        {{/if}} {{#if COMING_NEXT}}
        <section class="section">
          <h3 class="section-title">Coming Next</h3>
          <ul class="item-list">
            {{#each COMING_NEXT}}
            <li>{{this}}</li>
            {{/each}}
          </ul>
        </section>
        {{/if}}
      </main>

      <!-- Past Issues -->
      <aside class="past-issues">
        <h3>Past Issues</h3>
        <ul class="archive-list">
          {{#each PAST_ISSUES}}
          <li>
            <a href="/issues/{{this.number}}.html">
              <span class="archive-date">{{this.short_date}}</span>
              <span class="archive-number">No. {{this.number_padded}}</span>
              <span class="archive-headline">{{this.headline}}</span>
            </a>
          </li>
          {{/each}}
        </ul>
        <a href="/archive.html" class="view-all">View All Issues →</a>
      </aside>

      <!-- Footer -->
      <footer class="footer">
        <div class="footer-logo">
          <img
            src="/assets/logo.svg"
            alt="AskElephant"
            width="24"
            height="24"
          />
          <span>AskElephant</span>
        </div>
        <p class="footer-tagline">Meeting intelligence for revenue teams</p>
      </footer>
    </div>
  </body>
</html>
```

### Stylesheet (`assets/style.css`)

```css
/* AskElephant Weekly - Newspaper Style */

:root {
  --color-bg: #fafafa;
  --color-paper: #ffffff;
  --color-ink: #1a1a1a;
  --color-ink-light: #6b7280;
  --color-accent: #d4ff00;
  --color-border: #e5e7eb;

  --font-serif: "Newsreader", Georgia, serif;
  --font-sans: "Inter", -apple-system, sans-serif;

  --space-xs: 8px;
  --space-sm: 16px;
  --space-md: 24px;
  --space-lg: 48px;
  --space-xl: 64px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-sans);
  background: var(--color-bg);
  color: var(--color-ink);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

.container {
  max-width: 680px;
  margin: 0 auto;
  padding: var(--space-lg) var(--space-md);
}

/* Masthead */
.masthead {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding-bottom: var(--space-md);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--space-md);
}

.masthead-meta {
  font-size: 12px;
  color: var(--color-ink-light);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.masthead-meta .separator {
  margin: 0 8px;
}

.masthead-issue {
  text-align: right;
}

.issue-label {
  display: block;
  font-size: 10px;
  color: var(--color-ink-light);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.issue-number {
  font-family: var(--font-serif);
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 2px;
}

/* Title Block */
.title-block {
  text-align: center;
  padding: var(--space-lg) 0;
  border-bottom: 2px solid var(--color-ink);
}

.site-title {
  font-family: var(--font-serif);
  font-size: 42px;
  font-weight: 700;
  letter-spacing: -1px;
  margin-bottom: var(--space-xs);
}

.tagline {
  font-size: 14px;
  color: var(--color-ink-light);
  font-style: italic;
}

/* Headline Card */
.headline-card {
  background: var(--color-paper);
  padding: var(--space-lg);
  margin: var(--space-lg) 0;
  border: 1px solid var(--color-border);
  text-align: center;
}

.headline {
  font-family: var(--font-serif);
  font-size: 28px;
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: var(--space-sm);
}

.headline-description {
  font-size: 16px;
  color: var(--color-ink-light);
  max-width: 500px;
  margin: 0 auto;
}

/* Stats Banner */
.stats-banner {
  display: flex;
  justify-content: center;
  gap: var(--space-lg);
  padding: var(--space-md) 0;
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--space-lg);
}

.stat {
  text-align: center;
}

.stat-value {
  display: block;
  font-family: var(--font-serif);
  font-size: 36px;
  font-weight: 700;
  line-height: 1;
}

.stat-label {
  font-size: 11px;
  color: var(--color-ink-light);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Content Sections */
.content {
  margin-bottom: var(--space-xl);
}

.section {
  margin-bottom: var(--space-lg);
}

.section-title {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--color-ink-light);
  margin-bottom: var(--space-sm);
  padding-bottom: var(--space-xs);
  border-bottom: 1px solid var(--color-border);
}

.feature-list,
.item-list {
  list-style: none;
}

.feature-list li,
.item-list li {
  padding: var(--space-sm) 0;
  border-bottom: 1px solid var(--color-border);
  font-size: 15px;
}

.feature-list li:last-child,
.item-list li:last-child {
  border-bottom: none;
}

.item-desc {
  color: var(--color-ink-light);
}

.bugs-summary {
  font-style: italic;
  color: var(--color-ink-light);
}

/* Past Issues */
.past-issues {
  background: var(--color-paper);
  padding: var(--space-md);
  border: 1px solid var(--color-border);
  margin-bottom: var(--space-lg);
}

.past-issues h3 {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: var(--space-sm);
}

.archive-list {
  list-style: none;
}

.archive-list li {
  border-bottom: 1px solid var(--color-border);
}

.archive-list li:last-child {
  border-bottom: none;
}

.archive-list a {
  display: flex;
  align-items: baseline;
  gap: var(--space-sm);
  padding: var(--space-sm) 0;
  text-decoration: none;
  color: var(--color-ink);
  transition: opacity 0.2s;
}

.archive-list a:hover {
  opacity: 0.7;
}

.archive-date {
  font-size: 12px;
  color: var(--color-ink-light);
  min-width: 80px;
}

.archive-number {
  font-size: 11px;
  color: var(--color-ink-light);
  min-width: 60px;
}

.archive-headline {
  font-size: 14px;
  flex: 1;
}

.view-all {
  display: block;
  text-align: center;
  padding-top: var(--space-sm);
  font-size: 13px;
  color: var(--color-ink-light);
  text-decoration: none;
}

.view-all:hover {
  color: var(--color-ink);
}

/* Footer */
.footer {
  text-align: center;
  padding-top: var(--space-lg);
  border-top: 1px solid var(--color-border);
}

.footer-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-xs);
  font-weight: 600;
  margin-bottom: var(--space-xs);
}

.footer-tagline {
  font-size: 13px;
  color: var(--color-ink-light);
}

/* Responsive */
@media (max-width: 600px) {
  .container {
    padding: var(--space-md) var(--space-sm);
  }

  .site-title {
    font-size: 32px;
  }

  .headline {
    font-size: 22px;
  }

  .stats-banner {
    gap: var(--space-md);
  }

  .stat-value {
    font-size: 28px;
  }
}
```

## Generation Procedure

### Step 1: Load or Create Manifest

Check for `digest-manifest.json`:

- If exists, load current issue number
- If not, create with issue number 1

### Step 2: Parse Markdown Digest

Extract from source digest:

1. Date and week number
2. Headline text and description
3. Features list with titles/descriptions
4. Improvements list
5. Bugs count
6. Coming next items

### Step 3: Generate HTML

1. Increment issue number
2. Fill HTML template with extracted data
3. Generate past issues list (last 5)
4. Save to `docs/issues/{number}.html`
5. Update `docs/index.html` to show latest

### Step 4: Update Manifest

Add new issue to manifest:

```json
{
  "number": 4,
  "type": "weekly",
  "date": "2026-01-24",
  "week": "W04",
  "source": "digest-2026-W04.md",
  "published": "2026-01-24T17:00:00Z",
  "headline": "Dialpad Integration Now Live"
}
```

### Step 5: Commit and Deploy

If using GitHub Pages:

```bash
git add docs/
git commit -m "Publish digest issue #{{NUMBER}}"
git push
```

## Command Options

| Command                      | Description                      |
| ---------------------------- | -------------------------------- |
| `/publish-digest`            | Publish most recent digest       |
| `/publish-digest YYYY-WXX`   | Publish specific weekly digest   |
| `/publish-digest YYYY-MM-DD` | Publish specific daily digest    |
| `/publish-digest --preview`  | Generate but don't commit        |
| `/publish-digest --rebuild`  | Rebuild all issues from manifest |

## Hosting Options

### Option 1: GitHub Pages (Recommended)

1. Enable GitHub Pages on `docs/` folder
2. Optionally set custom domain (e.g., `weekly.askelephant.com`)
3. Commits to `docs/` auto-deploy

**Setup:**

```bash
# In pm-workspace repo settings:
# Pages → Source → Deploy from branch → main → /docs
```

### Option 2: Netlify/Vercel

Drop-in deployment from `docs/` folder with custom domain support.

### Option 3: Internal/Private

Host on internal server if digests shouldn't be public.

## File Locations

| File           | Location                                                 |
| -------------- | -------------------------------------------------------- |
| Generated site | `pm-workspace-docs/docs/` (or root `docs/`)              |
| Manifest       | `pm-workspace-docs/status/activity/digest-manifest.json` |
| Source digests | `pm-workspace-docs/status/activity/digest/digest-*.md`   |

## Integration

### With Activity Reporter

After generating a digest with `/eod --digest` or `/eow --digest`:

```
Digest saved to digest-2026-W04.md

Would you like to publish this to the website?
Run /publish-digest to create issue #4.
```

### With Visual Digest

The website can embed or link to visual assets:

- OG image for social sharing
- Header graphics

## Example Output

For digest-2026-W04.md → Issue #3:

**URL:** `https://weekly.askelephant.com/` or `https://weekly.askelephant.com/issues/003.html`

**Masthead:**

```
January 24, 2026 • San Francisco, USA          Issue No.
                                               003
```

**Title:**

```
         AskElephant Weekly
         What shipped this week
```

**Content:**

```
┌────────────────────────────────────────────┐
│                                            │
│    Dialpad Integration Now Live            │
│                                            │
│    Customers using Dialpad can now         │
│    connect their telephony directly        │
│    to AskElephant                          │
│                                            │
└────────────────────────────────────────────┘

        21              6              14
    New Features   Improvements    Bugs Fixed
```

## Customization

### Adjust Design

Edit `assets/style.css` to change:

- Colors (update CSS variables)
- Typography (change font imports)
- Layout (adjust spacing, max-width)

### Add Branding

Replace in `assets/`:

- `logo.svg` - Your logo
- `og-image.png` - Social preview image (1200x630px)
- `favicon.ico` - Browser tab icon

### Change Frequency

Modify manifest schema for daily vs weekly preference:

```json
{
  "publish_frequency": "weekly", // or "daily"
  "publish_day": "friday", // for weekly
  "publish_time": "17:00" // local time
}
```

## Error Handling

### No Digest Found

```
⚠️ No digest found for the specified date.

Available digests:
- digest-2026-W04.md (January 20-24)
- digest-2026-W03.md (January 13-17)

Run /eow --digest to generate a new weekly digest first.
```

### Manifest Missing

```
ℹ️ No digest manifest found. Creating new manifest.

This will be Issue #1. Continue? [Y/n]
```

### Already Published

```
⚠️ digest-2026-W04.md was already published as Issue #3.

Options:
- /publish-digest --force to republish (updates existing)
- /publish-digest 2026-W05 to publish a different week
```
