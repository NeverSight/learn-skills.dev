---
name: petition-evidence
description: "Use when collecting, capturing, or organizing evidence for a U.S. O-1A or EB-1A extraordinary ability petition — screenshotting press articles, saving award certificates, capturing paywalled or dead-linked pages, naming evidence files, routing them into a case workspace, or updating an evidence exhibit list. Triggers on evidence collection, screenshots of articles, exhibit tracking, or capturing press coverage for an immigration petition."
---

# Petition Evidence Collection

Turning URLs, PDFs, and scans into filed, tracked exhibits.

> Evidence is what the petition is made of. An adjudicator sees the exhibits, not your
> intentions — a screenshot with a cookie banner across the headline, or a file named
> `Screenshot 2026-03-14 at 4.51.12 PM.png`, weakens an otherwise strong claim.

## The two hard rules

1. **Every captured file gets recorded in `evidence-list.md` in the same working session.**
   Evidence collected but untracked is evidence lost. Update the row the moment the file
   lands, not at the end of a batch.
2. **Never run a general markdown formatter over `evidence-list.md`.** Formatters that
   round-trip markdown through a syntax tree escape the status brackets — `[x]` becomes
   `\[x\]` — and silently break every marker in the file.


Workflow guide for collecting, organizing, and tracking immigration petition evidence files. Covers screenshots, PDFs, file naming, folder routing, and evidence-list.md maintenance.

## When to Use

Activate when:
- Collecting or recapturing raw evidence files (screenshots, PDFs, photos)
- Updating evidence-list.md paths, statuses, or counts
- Batch screenshot operations across multiple URLs
- Organizing files into the `resources/` hierarchy
- Checking evidence collection status or gaps

**Do NOT use for:** Legal drafting, petition writing, or criterion analysis (use `immigration-law` skill instead).

## Master Tracking File

**Location:** `o1a-renewal/evidence-list.md`

### Table Format

Each criterion section uses this table structure:

```markdown
| Exhibit # | Description | Status | Source |
|-----------|-------------|--------|--------|
| | Meridian Robotics Grand Challenge — 1st of 210 teams (2023) | [x] collected | `resources/awards/meridian-grand-challenge-2023/meridian-winners-page-2023.png` |
```

- **Exhibit #** — Left blank until final assembly
- **Description** — Item name with year and key details
- **Status** — Current collection state (see markers below)
- **Source** — File path(s) in backticks, relative to project root

### Status Markers

| Marker | Meaning |
|--------|---------|
| `[x] collected` | File exists and verified |
| `[x] screenshot` | Screenshot captured via browser |
| `[x] PDF` | Saved as PDF |
| `[x] verified` | Content verified against source |
| `[x] complete` | Multi-part evidence fully assembled |
| `[x] photo + translation` | Image with accompanying translation |
| `[x] documented` | Evidence documented via URLs/references (no file needed) |
| `[x] dead URL, skip` | URL defunct, covered by other evidence |
| `[x] duplicate` | Removed as duplicate of another item |
| `[x] removed` | Intentionally excluded from petition |
| `[ ] needs email/invite` | Waiting on external party to provide |
| `[ ]` | Not yet collected |

### Collection Summary Table

At the bottom of evidence-list.md, the Collection Summary must always be reconciled after changes:

```markdown
## Collection Summary

| Category | Total Items | Collected | Remaining |
|----------|------------|-----------|-----------|
| Criterion 1 — Awards | 12 | 12 | 0 |
| ...
| **Total** | **156** | **152** | **4** |
```

**Reconciliation rules:**
1. Count all rows in each criterion table (exclude struck-through/removed items)
2. Count rows with any `[x]` status as "Collected"
3. Count rows with `[ ]` status as "Remaining"
4. Update the Total row as sum of all categories
5. Update the "Remaining Gaps" callout to match

## File Naming Conventions

**Pattern:** `{publication}-{subject}-{year}.{ext}`

- All lowercase, kebab-case (hyphens, no spaces or underscores)
- Include the year when known
- Keep names descriptive enough to identify without opening

### Examples by Type

| Type | Example |
|------|---------|
| Press article screenshot | `automation-review-kestrel-2024.png` |
| Press article PDF | `folha-tecnologica-ferraz-profile-2023.pdf` |
| Award certificate | `meridian-grand-challenge-certificate-2023.pdf` |
| Product screenshot | `kestrel-inspection-suite-product-page.png` |
| Podcast episode | `factory-floor-podcast-vision-systems-2024.png` |
| Conference speaking | `machine-perception-conf-keynote-2024.png` |
| Translation | `translation-folha-tecnologica-profile.md` |
| Company profile | `kestrel-robotics-company-profile.md` |
| Support letter | `halvard-sten-letter.pdf` |

## Resources Folder Hierarchy

All raw evidence files go into `resources/`. Route files using these rules:

| Content Type | Destination | Examples |
|-------------|-------------|---------|
| Press articles (English) | `resources/press/{company}/articles/` | Screenshots and PDFs of news articles, flat (one file per article) |
| Podcast/video appearances | `resources/press/{company}/podcasts/{episode-name}/` | Per-episode folder: screenshot + transcript + translation grouped together |
| Article translations | `resources/press/{company}/translations/` | English translations of non-English article content (NOT podcast translations — those go in the episode folder) |
| Awards (per award) | `resources/awards/{award-name}/` | Certificates, screenshots, announcement pages |
| Memberships (per org) | `resources/memberships/{org-name}/` | Selection docs, program descriptions |
| Judging (per event) | `resources/judging/{event-name}/` | Invitations, event pages, speaker bios |
| Speaking engagements | `resources/speaking/{event-name}/` | Conference page screenshots, schedules |
| Products (per product) | `resources/projects/{product-name}/` | Website screenshots, app screenshots |
| Patents | `resources/patents/` | Patent docs, citation reports |
| Compensation | `resources/compensation/` | Tax docs, W-2s, paystubs, verification |
| Company docs | `resources/company-docs/` | Incorporation, org charts, fundraising |
| Education | `resources/education/` | Diplomas, transcripts, certificates |
| Prior filings | `prior-filings/` | Archive of old O-1 petitions (project root, not inside resources/) |
| Recommendation letters | `resources/recommendation-letters/` | Organized by era: `2011-original/`, `2021-renewal/`, `2024-signed/`, `drafts/` |
| Resume/CV | `resources/resume/` | CV, LinkedIn export, bios |

### Routing Decision Tree

1. Is it about a press article, interview, or media appearance?
   - English article → `press/articles/`
   - Podcast or video interview → `press/podcasts/`
   - Non-English content translation → `press/translations/`
2. Is it an award or recognition? → `awards/{award-name}/`
3. Is it about membership in an organization? → `memberships/{org-name}/`
4. Is it about judging, mentoring, or evaluating others? → `judging/{event-name}/`
5. Is it a conference talk or panel? → `speaking/{event-name}/`
6. Is it a product, app, or tool screenshot? → `projects/{product-name}/`
7. Is it a patent document? → `patents/`
8. Is it compensation-related? → `compensation/`

## Screenshot Collection Workflow

Follow these 10 steps for each evidence item:

1. **Parse evidence-list.md** — Identify items needing collection (status `[ ]` or needing recapture)
2. **Find the URL** — From the evidence-list Source column, prior notes, or web search
3. **Choose capture method** — Use **shot-scraper** (preferred) for all captures, or Chrome MCP for interactive debugging only
4. **Assess the page** — Check for paywalls, 404s, login walls, cookie banners
5. **Clean the page** — Pass `--javascript` cleanup to shot-scraper (see screenshot-standards.md)
6. **Capture full-page screenshot** — shot-scraper captures the full page by default (no flags needed)
7. **Visually verify** — Confirm: headline visible, publication logo, byline, date, body text readable, no overlays
8. **Save to correct path** — Route to the appropriate `resources/` subfolder per the hierarchy above
9. **Update evidence-list.md** — Set status to `[x] screenshot` and add file path in Source column
10. **Reconcile counts** — After a batch, update the Collection Summary table

### Capture Methods

| Method | When to Use | Pros | Cons |
|--------|-------------|------|------|
| **shot-scraper** (preferred) | All captures — single, batch, recaptures | Full-page by default, saves to disk, JS cleanup via `--javascript`, one-liner CLI, no boilerplate | Requires `pipx install shot-scraper && shot-scraper install` |
| **Chrome MCP tools** | Interactive debugging, visually inspecting a page before deciding capture strategy | See the page live, manual intervention possible | Viewport-only screenshots, harder to save to disk |

### shot-scraper Setup (One-Time)

```bash
pipx install shot-scraper && shot-scraper install
```

### Basic Capture Command

```bash
shot-scraper 'https://example.com/article' \
  -w 1200 \
  --wait 3000 \
  --javascript 'CLEANUP_JS_HERE' \
  -o /path/to/output.png
```

- **Full page is the default** — no flag needed (omit `--height` to capture entire page)
- `-w 1200` — article-friendly width
- `--wait 3000` — wait for dynamic content to load
- `--javascript '...'` — run cleanup JS before capture (see screenshot-standards.md for the cleanup script)
- `-o path` — save directly to the target resources/ path

See `references/screenshot-standards.md` for the full cleanup script, batch patterns, and site-specific notes.

## Screenshot Quality Standards

### Must Include
- Article headline / title
- Publication name or logo
- Author byline (if present)
- Publication date
- Opening body text (enough to verify content)

### Must NOT Include
- Cookie consent banners
- Newsletter signup popups/modals
- Advertising overlays
- Paywall gates
- Sticky navigation bars that obscure content
- Chat widgets
- Video autoplay overlays (unless the video IS the evidence)

### Format Selection

| Scenario | Format | Notes |
|----------|--------|-------|
| Short article (1-3 screens) | PNG screenshot | Single or stitched capture |
| Long article (4+ screens) | PDF | Print-to-PDF for full content |
| Video content page | PNG screenshot | Capture the episode/video page, not the video itself |
| Photo + translation | PNG + MD | Screenshot of original + markdown translation file |

## Handling Blocked Content

### Decision Tree

```
Page loads → Check for blockers:
├── Cookie banner only → Clean with JS, proceed
├── Newsletter popup → Dismiss or clean with JS, proceed
├── Soft paywall (limited articles) → Try incognito/clean cookies, proceed
├── Hard paywall → Flag as blocked, note in evidence-list
├── 404 / Not Found → Try Wayback Machine (web.archive.org)
│   ├── Found on Wayback → Screenshot the archived version, note "(via Wayback Machine)" in description
│   └── Not on Wayback → Flag as dead URL
├── Login wall → Flag as blocked
└── Geo-restriction → Flag as blocked
```

### When Flagging
- Set status to `[x] dead URL, skip` if covered by other evidence
- Set status to `[ ] blocked` if not covered and needs manual intervention
- Add a note explaining the blocker in the Source column

## Evidence List Update Protocol

### After Every Save
1. Find the item's row in evidence-list.md
2. Update Status to appropriate `[x]` marker
3. Update Source with the file path in backticks

### After Every Batch
1. Recount all rows in each criterion table
2. Update the Collection Summary table with new totals
3. Update the "Remaining Gaps" callout
4. Verify Total row = sum of all category rows

## Reference

For JavaScript cleanup scripts, site-specific handling notes, and detailed quality criteria, see **`references/screenshot-standards.md`**.
