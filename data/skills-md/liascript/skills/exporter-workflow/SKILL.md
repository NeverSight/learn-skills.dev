---
name: exporter-workflow
description: >
  Generates LiaScript export workflows, GitHub Actions, and project.yaml files for LiaScript repositories.
  Use when a user wants to: export a LiaScript course to PDF/SCORM/IMS/ePub/DOCX/xAPI/Android; create or update
  a GitHub Actions workflow for LiaScript; build a project website (index page) that aggregates multiple courses;
  set up automated deployment to GitHub Pages; add quality checks (spell/style) to a LiaScript repo;
  or asks anything involving the liaex CLI, @liascript/exporter, or LiaScript CI/CD.
license: CC0-1.0
---

# LiaScript Exporter & Workflow Skill

> **Reference for AI agents:** Read this entire file before generating any workflow, `project.yaml`, or `liaex` command.

---

## Agent Role

You are a LiaScript Workflow Engineer. Your task is to help users automate the generation, transformation, and publishing of LiaScript courses.

**Core outputs you produce:**
1. `liaex` CLI commands (for local use)
2. GitHub Actions workflow YAML files (`.github/workflows/*.yml`)
3. `project.yaml` files (for course catalog websites)
4. Configuration files (`.cspell.json`, `.alexrc`, `.proselintrc`)

**Before generating anything:**
- Ask what the user's target LMS or output goal is (if not clear)
- Identify whether they want a single-course export or a multi-course project website
- Check if they already have a `project.yaml` or existing workflows

---

## Agent Workflow

### Step 1: Determine the Goal

Ask or infer from context:

| User Goal | What to produce |
|-----------|----------------|
| Export one course to Moodle/ILIAS/OPAL | `liaex` command + optional GitHub Action |
| Export to PDF/ePub/DOCX | `liaex` command + optional GitHub Action |
| Build a course catalog / index page | `project.yaml` + GitHub Actions workflow |
| Automate exports on every push | GitHub Actions workflow |
| Deploy a project website to GitHub Pages | Full GitHub Actions deployment workflow |
| Add quality checks | Quality check workflow |

### Step 2: Choose the Right Format

Use the decision matrix in Section 11 to select format and required flags based on the target LMS or output type.

**Critical LMS-specific rules — always apply:**
- Moodle 3.x → `scorm1.2 --scorm-iframe`
- Moodle 4.x / OPAL / Open edX / OpenOLAT → `scorm1.2 --scorm-embed`
- ILIAS / learnworlds.com / scorm.cloud → `scorm2004 --scorm-iframe`
- State persistence needed → use `scorm2004` (not `scorm1.2`)

### Step 3: Generate the Artifact

Use the templates in Sections 4–5 as starting points. Always:
- Use `force_orphan: true` in `peaceiris/actions-gh-pages` steps
- Use `raw.githubusercontent.com` URLs in `project.yaml` (never HTML GitHub URLs)
- Set `--pdf-timeout 50000` (or higher) for large courses
- Add `--project-generate-cache -p ./cache` for large project websites
- Isolate exporter outputs from source files: write to a temp directory outside the repo (e.g., `/tmp/lia-exports-${{ github.run_id }}` or `${{ runner.temp }}` when valid in step scope)
- For Docker-based exports, mount source as read-only and mount a separate output directory (`-v "$GITHUB_WORKSPACE:/work:ro"` and `-v "$EXPORT_DIR:/out"`)
- Stage release assets only after all exports finish (copy final files into `outputs/`), never export directly into `outputs/`

### Step 4: Explain Setup Steps

After generating the workflow:
1. Tell the user where to place the file (e.g., `.github/workflows/deploy.yml`)
2. If deploying to GitHub Pages: remind them to enable Pages on the `gh-pages` branch in repo Settings
3. If PDF is generated: note Puppeteer dependencies may be needed on Ubuntu runners (Section 8)

---

## Output Isolation (Critical)

When generating multiple export formats in one workflow run, do not write output files into the same tree that contains the LiaScript source input (for example the repository root or a checked out subfolder like `project/`).

If outputs are written next to source content, later exports may include previous export artifacts recursively (ZIP inside ZIP behavior), causing package size growth on every run.

Use this safe pattern:
1. Export all formats into an isolated temporary directory outside source tree (`$EXPORT_DIR` in `/tmp` or runner temp).
2. Run Docker Android export with separate source/output mounts and read-only source.
3. Copy only final files to a clean `outputs/` staging folder.
4. Upload assets from `outputs/`.

---

---

## Quick Start — Example Files

Use these ready-made examples as starting points:

| File | What it shows |
|------|---------------|
| [examples/project-minimal.yaml](examples/project-minimal.yaml) | Minimal course catalog with 3 courses |
| [examples/project-course.yaml](examples/project-course.yaml) | Full single-repo catalog with HTML separators, sub-collections, per-course options |
| [examples/workflow-single-course.yml](examples/workflow-single-course.yml) | Export one course to PDF + SCORM 2004 + IMS, attach to GitHub Release |
| [examples/workflow-project-basic.yml](examples/workflow-project-basic.yml) | Generate project website from `project.yaml` and deploy to GitHub Pages |
| [examples/workflow-multi-project.yml](examples/workflow-multi-project.yml) | Multi-project site: multiple YAML files in `project/`, with PDFs + SCORM + Pages |

---

## 1. Installation

```bash
npm install -g @liascript/exporter
# Linux/macOS may require sudo:
sudo npm install -g @liascript/exporter
```

The CLI command is `liaex` (also available as `liascript-exporter`).

**Alternative: Desktop App**
Download from [GitHub Releases](https://github.com/LiaScript/LiaScript-Exporter/releases) — no Node.js required.

**Alternative: Docker (Android exports)**
```bash
docker pull liascript/exporter
docker run --rm \
  -v "$(pwd):/work:ro" \
  -v "/tmp/lia-exports:/out" \
  liascript/exporter \
  liaex -f android -i /work/README.md --android-appId io.github.example.course --output /out/android
```

---

## 2. Core CLI Syntax

```bash
liaex -i <input-file> -f <format> -o <output-name> [options]
```

| Flag | Long form | Description |
|------|-----------|-------------|
| `-i` | `--input` | Input file (Markdown or YAML for projects) |
| `-f` | `--format` | Output format (see Section 3) |
| `-o` | `--output` | Output name (extension set by format) |
| `-p` | `--path` | Path to pack (defaults to input file's directory) |
| `-s` | `--style` | Inject additional CSS |
| `-k` | `--key` | ResponsiveVoice key for TTS |
| `-v` | `--version` | Print version |
| `-h` | `--help` | Show help |

**Web UI mode:**
```bash
liaex serve          # starts local web server on port 3000
liaex serve --port 8080
```

---

## 3. Export Formats

### 3.1 SCORM 1.2

```bash
liaex -i README.md --format scorm1.2 --output my-course
```

Produces `my-course.zip`. SCORM 1.2 stores only location (not quiz/survey states — use SCORM 2004 for state persistence).

**Key options:**
| Option | Description |
|--------|-------------|
| `--scorm-masteryScore` | 0–100, default 80. Set to 0 to let everyone pass. |
| `--scorm-typicalDuration` | ISO 8601 duration, e.g. `PT1H30M0S`. Default: `PT0H5M0S` |
| `--scorm-organization` | Sets organization in `imsmanifest` |
| `--scorm-iframe` | Fix for ILIAS, OpenOLAT, learnworlds.com that break startingParameter |
| `--scorm-embed` | Embeds Markdown into JS code — use for Moodle 4, OPAL, Open edX |
| `--lia-subfolder` | Places course files in `content/` subfolder (implies `--scorm-embed`) |
| `--key` | ResponsiveVoice key for TTS |

**LMS-specific commands:**
```bash
# ILIAS / learnworlds.com
liaex -i course/README.md -f scorm2004 --scorm-masteryScore 80 --scorm-iframe

# Moodle 3.x
liaex -i course/README.md -f scorm1.2 --scorm-masteryScore 80 --scorm-iframe

# Moodle 4.x / OPAL / Open edX / OpenOLAT
liaex -i course/README.md -f scorm1.2 --scorm-masteryScore 80 --scorm-embed

# scorm.cloud
liaex -i course/README.md -f scorm2004 --scorm-masteryScore 80 --scorm-iframe
```

---

### 3.2 SCORM 2004

```bash
liaex -i README.md --format scorm2004 --output my-course
```

Same options as SCORM 1.2. **Supports persistent state** for quizzes, surveys, tasks.

---

### 3.3 IMS Content

```bash
liaex -i README.md --format ims --output course
```

Produces `course.zip`. Simplistic LMS packaging format (IMS v1.1.4).

| Option | Description |
|--------|-------------|
| `--ims-indexeddb` | Persist quiz/coding states in browser's IndexedDB |
| `--lia-subfolder` | Places course files in `content/` subfolder |

---

### 3.4 WEB (Standalone)

```bash
liaex --format web -i README.md -o outputFolder
```

Generates a self-contained web project that can be uploaded to any server.

> ⚠️ Web exports must be served over HTTP — opening `index.html` via `file://` does not work.

**Preview locally:**
```bash
npx serve outputFolder
# or
python3 -m http.server --directory outputFolder
```

| Option | Description |
|--------|-------------|
| `--web-zip` | Bundle into a zip file instead of a folder |
| `--web-iframe` | Hides the course URL (but breaks direct slide linking) |
| `--web-indexeddb [key]` | Persist states in browser IndexedDB |

---

### 3.5 PDF

```bash
liaex --format pdf -i README.md -o output
```

Uses Puppeteer (headless Chrome) to render the entire course as PDF.

**Preview mode:**
```bash
liaex --format pdf --pdf-preview -i https://raw.githubusercontent.com/.../README.md
```

**Key options:**
| Option | Description |
|--------|-------------|
| `--pdf-stylesheet` | Inject custom CSS |
| `--pdf-theme` | `default`, `turquoise`, `blue`, `red`, `yellow` |
| `--pdf-timeout` | Wait time in ms (default: 15000). Increase for large courses. |
| `--pdf-scale` | 0.1–2, default 1 |
| `--pdf-displayHeaderFooter` | Show header/footer (default: false) |
| `--pdf-headerTemplate` | HTML template (classes: `date`, `title`, `url`, `pageNumber`, `totalPages`) |
| `--pdf-footerTemplate` | Same as header template |
| `--pdf-printBackground` | Print background graphics (default: false) |
| `--pdf-landscape` | Landscape orientation (default: false) |
| `--pdf-pageRanges` | e.g. `"1-5, 8, 11-13"` |
| `--pdf-format` | Paper format, e.g. `A4`, `A3`, `Letter` (default: a4) |
| `--pdf-width` / `--pdf-height` | Custom dimensions with units |
| `--pdf-margin-top/right/bottom/left` | Margins with units |
| `--pdf-preferCSSPageSize` | CSS `@page` size takes priority |
| `--pdf-omitBackground` | Transparent background (default: true) |

**Custom CSS example:**
```css
:root {
  --color-highlight: 2, 255, 0;
  --color-background: 122, 122, 122;
  --color-text: 0, 0, 255;
  --global-font-size: 1rem;
  --font-size-multiplier: 2;
}
```

---

### 3.6 ePub

```bash
liaex -i README.md --format epub --epub-title "My Course" --epub-author "Author Name" --output course
```

| Option | Description |
|--------|-------------|
| `--epub-title` | **Required.** Title of the book |
| `--epub-author` | **Required.** Semicolon-separated for multiple authors |
| `--epub-publisher` | Publisher name |
| `--epub-cover` | Path or URL to cover image |
| `--epub-description` | Book description |
| `--epub-language` | 2-letter language code (default: `en`) |
| `--epub-version` | EPUB version: `2` or `3` (default: 3) |
| `--epub-stylesheet` | Custom CSS path |
| `--epub-theme` | `default`, `turquoise`, `blue`, `red`, `yellow` |
| `--epub-toc-title` | TOC title (default: `"Table Of Contents"`) |
| `--epub-hide-toc` | Hide TOC (default: false) |
| `--epub-timeout` | Render wait in ms (default: 15000) |
| `--epub-fonts` | Comma-separated custom font paths |
| `--epub-chapter-title` | Main chapter title (default: course title) |
| `--epub-preview` | Open preview browser |

---

### 3.7 DOCX

```bash
liaex -i README.md --format docx --output course
```

Compatible with Word 2007+, LibreOffice Writer, Google Docs.

| Option | Description |
|--------|-------------|
| `--docx-title` | Document title |
| `--docx-author` | Author name |
| `--docx-subject` | Subject |
| `--docx-description` | Description |
| `--docx-language` | Language code for spell checker (default: `en-US`) |
| `--docx-orientation` | `portrait` or `landscape` (default: `portrait`) |
| `--docx-font` | Font name (default: `Arial`) |
| `--docx-font-size` | In half-points/HIP (default: 22 = 11pt) |
| `--docx-header` / `--docx-footer` | Enable header/footer |
| `--docx-header-html` / `--docx-footer-html` | Custom HTML |
| `--docx-page-number` | Add page numbers to footer |
| `--docx-stylesheet` | Custom CSS path |
| `--docx-theme` | `default`, `turquoise`, `blue`, `red`, `yellow` |
| `--docx-timeout` | Render wait in ms (default: 15000) |
| `--docx-preview` | Open preview browser |

---

### 3.8 xAPI

```bash
liaex -i README.md --format xapi --output course
```

Generates a self-contained web package with `tincan.xml` manifest.

| Option | Description |
|--------|-------------|
| `--xapi-endpoint` | LRS endpoint URL |
| `--xapi-auth` | Auth string (e.g., `"Basic dXNlcm5hbWU6cGFzc3dvcmQ="`) |
| `--xapi-actor` | JSON actor string (default: anonymous) |
| `--xapi-course-id` | Custom course identifier |
| `--xapi-course-title` | Custom course title |
| `--xapi-mastery-threshold` | Score threshold (default: 0.8) |
| `--xapi-progress-threshold` | Progress threshold (default: 0.9) |
| `--xapi-debug` | Enable debug logging |
| `--xapi-zip` | Package as zip |
| `--lia-subfolder` | Place course files in `content/` subfolder |

---

### 3.9 Android APK

```bash
liaex -f android \
  -i README.md \
  --android-sdk /home/user/Android/Sdk \
  --android-appId io.github.myorg.mycourse \
  --output output
```

Produces `output.apk`. Uses Capacitor.js. Best done via Docker (see Section 1).

| Option | Description |
|--------|-------------|
| `--android-sdk` | Path to Android SDK |
| `--android-appId` | Unique reverse-domain app ID |
| `--android-appName` | App name (default: course title) |
| `--android-icon` | App icon (1024×1024 px) |
| `--android-splash` | Splash screen image (2732×2732 px) |
| `--android-splashDuration` | Splash duration in ms (default: 0) |
| `--android-preview` | Open Android Studio preview |

---

### 3.10 RDF / JSON-LD

```bash
liaex --format rdf --rdf-preview -i README.md
liaex --format rdf --rdf-format n-quads -i README.md -o output
```

Exports LiaScript course metadata as JSON-LD or N-Quads (schema.org `Course`).

| Option | Description |
|--------|-------------|
| `--rdf-preview` | Print to console instead of file |
| `--rdf-format` | `jsonld` (default) or `n-quads` |
| `--rdf-url` | Set remote URL for local file input |
| `--rdf-type` | Default `Course` — can be `EducationalResource`, etc. |
| `--rdf-educationalLevel` | e.g., `beginner`, `intermediate`, `advanced` |
| `--rdf-license` | License URL (auto-detects LICENSE file in root) |
| `--rdf-template` | Base template URL or local JSON file |

---

### 3.11 Project (Index Website)

See Section 4 for the full project workflow.

```bash
liaex -i project.yaml --format project --output index
```

---

## 4. Project Website (`project.yaml`)

A project website is a single `index.html` that aggregates multiple LiaScript courses into a searchable, filterable catalog.

### 4.1 Full project.yaml Reference

```yaml
# Page title — supports HTML
title: >
  <span style="background-color: rgba(0,106,179,0.75); padding: 5px; color: white">
    My OER Collection
  </span>

# Subtitle / description — supports HTML
comment: >
  <br>
  <span style="background-color: rgba(0,106,179,0.75); padding: 5px; color: white">
    Interactive courses made with LiaScript
  </span>

# Page header image (local file or URL)
logo: logo.jpg

# Browser tab favicon or social media icon (URL recommended)
icon: https://example.com/icon.svg

# Optional sticky navigation bar
navbar:
  brand: My OER Collection           # text/logo on the left
  background: "#0B6E75"              # optional bar color (default: #0B6E75)
  theme: dark                        # dark (white text) | light (dark text)
  links:
    - label: Home
      url: "#"
    - label: Section 1
      url: "#section-1"

# Footer — supports HTML
footer: >
  Made with LiaScript —
  <a href="https://liascript.github.io" target="_blank">https://LiaScript.github.io</a>

# Social media / OpenGraph metadata
# If omitted, title/comment/logo are used. Disable with --project-no-meta
meta:
  title: My OER Collection
  description: A collection of interactive open educational resources
  # image: https://example.com/og-image.jpg

# Global tags applied to ALL courses
tags:
  - Education
  - Interactive
  - OER

# Main course collection
collection:
  # Simple course entry — metadata auto-extracted from the LiaScript header
  - url: https://raw.githubusercontent.com/username/repo/main/README.md

  # Course with overridden metadata
  - url: https://raw.githubusercontent.com/username/repo2/main/README.md
    title: Custom Title
    comment: Custom description shown on the card.
    logo: https://example.com/custom-logo.jpg   # leave empty (logo:) to hide image
    tags:
      - Tutorial
      - Beginner

  # Per-course export override (long flag names without --)
  - url: https://raw.githubusercontent.com/username/repo3/main/README.md
    arguments:
      - pdf-format: A3
      - project-generate-scorm2004: true
      - scorm-organization: My Organization
      - project-generate-pdf: false   # disable PDF for this specific course

  # HTML separator / section header between course groups
  - html: >
      <hr>
      <h1>Programming Courses</h1>
      <p>Learn various languages and paradigms.</p>

  # Sub-collection (grouped courses with optional grid layout)
  - title: Python Track
    comment: From beginner to advanced Python
    grid: true     # smaller preview cards in a grid layout
    tags:
      - Python
      - Programming
    collection:
      - url: https://raw.githubusercontent.com/username/python-intro/main/README.md
        tags:
          - Beginner
      - url: https://raw.githubusercontent.com/username/python-advanced/main/README.md
        tags:
          - Advanced
```

### 4.2 Tags in LiaScript Document Headers

Tags in the LiaScript course header are automatically extracted:

```markdown
<!--
author:  Your Name
email:   your.email@example.com
version: 1.0.0
language: en
narrator: US English Female
comment: Introduction to Python programming
tags: Python, Programming, Beginner, Computer Science
-->
```

### 4.3 Project Export CLI Options

```bash
# Basic project website
liaex -i project.yaml --format project --output index

# With PDF generation for every course
liaex -i project.yaml --format project --output index --project-generate-pdf

# With SCORM 1.2 for every course
liaex -i project.yaml --format project --output index --project-generate-scorm12

# With SCORM 2004
liaex -i project.yaml --format project --output index --project-generate-scorm2004

# With IMS packages
liaex -i project.yaml --format project --output index --project-generate-ims

# Combined PDF + SCORM
liaex -i project.yaml --format project --output index \
  --project-generate-pdf --project-generate-scorm12

# With caching (skip already-generated files)
liaex -i project.yaml --format project --output index \
  --project-generate-pdf --project-generate-scorm12 --project-generate-cache -p ./cache

# PDF with custom theme
liaex -i project.yaml --format project --output index \
  --project-generate-pdf --pdf-theme blue --pdf-printBackground

# Disable tag/category filtering
liaex -i project.yaml --format project --output index --project-no-categories

# Blur non-matching courses instead of hiding them
liaex -i project.yaml --format project --output index --project-category-blur

# Disable social media meta tags
liaex -i project.yaml --format project --output index --project-no-meta

# Enable full-text fuzzy search (adds search icon to navbar or floating button)
liaex -i project.yaml --format project --output index --project-search
```

**All project-specific flags:**
| Flag | Description |
|------|-------------|
| `--project-no-meta` | Disable OpenGraph/Twitter card meta generation |
| `--project-no-rdf` | Disable JSON-LD generation |
| `--project-no-categories` | Disable tag/category filter dropdown |
| `--project-category-blur` | Blur non-matching courses instead of hiding |
| `--project-generate-pdf` | Auto-generate PDF for every course card |
| `--project-generate-scorm12` | Auto-generate SCORM 1.2 for every course |
| `--project-generate-scorm2004` | Auto-generate SCORM 2004 for every course |
| `--project-generate-ims` | Auto-generate IMS package for every course |
| `--project-generate-cache` | Skip generation if output file already exists |
| `--project-search` | Enable full-text fuzzy search across all courses |

---

## 5. GitHub Actions Workflows

### 5.1 Simple: Transform Single Course to Multiple Formats

**File:** `.github/workflows/generate-outputs.yml`

```yaml
name: Generate LiaScript Outputs

on:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          path: project

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install LiaScript Exporter
        run: npm install -g @liascript/exporter

      - name: Generate PDF
        env:
          PUPPETEER_ARGS: "--no-sandbox --disable-setuid-sandbox"
        run: liaex -i project/README.md --format pdf --output Documentation --pdf-timeout 50000

      - name: Generate SCORM 2004
        run: liaex -i project/README.md --format scorm2004 --output SCORM

      - name: Generate IMS Package
        run: liaex -i project/README.md --format ims --output IMS

      - name: Create GitHub Release
        id: create_release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: 'latest'
          release_name: 'Latest LiaScript Documentation'
          draft: false
          prerelease: false

      - name: Upload PDF
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: Documentation.pdf
          asset_name: Documentation.pdf
          asset_content_type: application/pdf

      - name: Upload SCORM
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: SCORM.zip
          asset_name: SCORM.zip
          asset_content_type: application/zip

      - name: Upload IMS
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: IMS.zip
          asset_name: IMS.zip
          asset_content_type: application/zip
```

---

### 5.2 Project Website: Basic Deployment to GitHub Pages

**File:** `.github/workflows/deploy-project.yml`

```yaml
name: Generate and Deploy Project Website

on:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  run_exporter:
    runs-on: ubuntu-latest
    steps:
      - name: Install LiaScript Exporter
        run: npm install -g @liascript/exporter

      - name: Check out repository
        uses: actions/checkout@v4

      - name: Generate project website
        run: liaex -i project.yaml --format project --output index

      - name: Prepare deployment directory
        run: |
          mkdir -p gh-pages-deploy
          mv index.html gh-pages-deploy/
          cp logo.jpg gh-pages-deploy/

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_branch: gh-pages
          publish_dir: gh-pages-deploy
          force_orphan: true     # REQUIRED: always overwrite gh-pages history completely
```

> ⚠️ **`force_orphan: true` is required.** This ensures the `gh-pages` branch is always completely replaced, with no accumulated history.

---

### 5.3 Project Website: Full Production Workflow (PDF + SCORM + Cache + Schedule)

**File:** `.github/workflows/deploy-full.yml`

```yaml
name: Generate and Deploy LiaScript Project Website

on:
  push:
    branches:
      - main
  schedule:
    - cron: '0 0 * * 0'   # Every Sunday at midnight UTC

permissions:
  contents: write

jobs:
  run_exporter:
    runs-on: ubuntu-latest
    steps:
      - name: Install LiaScript Exporter
        run: npm install -g @liascript/exporter

      - name: Check out repository
        uses: actions/checkout@v4

      - name: Restore cached resources
        uses: actions/cache@v4
        with:
          path: ./cache
          key: ${{ runner.os }}-resources-${{ hashFiles('project.yaml') }}
          restore-keys: |
            ${{ runner.os }}-resources-

      - name: Create cache directory
        run: mkdir -p ./cache

      - name: Generate website with PDFs and SCORM packages
        run: |
          liaex -i project.yaml --format project --output index \
            --project-generate-pdf \
            --project-generate-scorm12 \
            --project-generate-cache \
            -p ./cache

      - name: Prepare deployment directory
        run: |
          mkdir -p gh-pages-deploy
          cp index.html gh-pages-deploy/

          # Copy assets
          [ -f logo.jpg ] && cp logo.jpg gh-pages-deploy/
          [ -f icon.png ] && cp icon.png gh-pages-deploy/

          # Copy generated PDFs and SCORM ZIPs from cache
          find ./cache -name "*.pdf" -exec cp {} gh-pages-deploy/ \;
          find ./cache -name "*.zip" -exec cp {} gh-pages-deploy/ \;

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_branch: gh-pages
          publish_dir: gh-pages-deploy
          force_orphan: true
          commit_message: "Deploy: ${{ github.event.head_commit.message || 'Scheduled update' }}"

      - name: Output website URL
        run: |
          echo "Deployed to: https://${{ github.repository_owner }}.github.io/${{ github.event.repository.name }}/"
```

---

### 5.4 Multi-Project Website (multiple YAML files)

Use when one repository contains several distinct subject areas, each with their own catalog page, PDFs, and SCORM packages.

**Repository layout:**
```
project/
  index.yaml           ← top-level navigation page
  topic-a.yaml         ← one section/audience
  topic-b.yaml
assets/                ← shared images referenced by project pages
```

**File:** `.github/workflows/deploy.yml` — see full example at [examples/workflow-multi-project.yml](examples/workflow-multi-project.yml).

Key points:
- Run `liaex` with `working-directory: project` (or use `liaex -i project/topic-a.yaml`)
- Set `PUPPETEER_ARGS: "--no-sandbox --disable-setuid-sandbox"` env var on the generate step
- Use `force_orphan: true` on `peaceiris/actions-gh-pages@v4`
- Preserve PDF/ZIP subdirectory structure when copying to the deploy directory:
  ```bash
  find project -name "*.pdf" | while read f; do
    rel="${f#project/}"
    mkdir -p "gh-pages-deploy/$(dirname "$rel")"
    cp "$f" "gh-pages-deploy/$rel"
  done
  ```

---

### 5.5 Quality Check Workflow

**File:** `.github/workflows/quality-checks.yml`

```yaml
name: Quality Checks

on:
  pull_request:
  push:
    branches: [main, master]

jobs:
  cspell-spellcheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install cspell
        run: npm install -g cspell
      - name: Run spell check
        run: npx cspell --locale en-US --show-suggestions "**/*.md"

  write-good:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - name: Install write-good
        run: npm install -g write-good
      - name: Run style check
        run: npx write-good *.md

  alex:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - name: Install alex
        run: npm install -g alex
      - name: Run inclusive language check
        run: npx alex *.md

  proselint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - name: Install proselint
        run: |
          npm install -g proselint
          pip install proselint
      - name: Run proselint
        run: npx proselint *.md
```

---

### 5.6 GitHub Action (LiaScript's own Action)

Use directly in a workflow without installing the exporter:

```yaml
- name: Export to SCORM
  uses: LiaScript/LiaScript-Exporter@master
  with:
    input-file: 'README.md'
    format: 'scorm1.2'
    output-name: 'my-course'
    scorm-organization: 'My Organization'

- name: Upload SCORM
  uses: actions/upload-artifact@v4
  with:
    name: scorm-package
    path: '*.zip'
```

Full documentation: [action/README.md](https://github.com/liascript/liascript-exporter/blob/HEAD/action/README.md)

---

### 5.7 Triggering Strategies

```yaml
# Run on push to main only
on:
  push:
    branches: [main]

# Run on push + weekly
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'    # Every Sunday midnight UTC

# Run on push + daily
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'    # Every day at midnight UTC

# Run on push AND pull requests
on:
  pull_request:
  push:
    branches: [main, master]
```

---

## 6. Quality Check Tools

### 6.1 CSpell (Spell Checking)

```bash
npm install -g cspell
npx cspell --locale en-US --show-suggestions "**/*.md"

# German support
npm install -g @cspell/dict-de-de
npx cspell --locale en-US,de-DE --show-suggestions "**/*.md"
```

**Config file `.cspell.json`:**
```json
{
  "version": "0.2",
  "language": "en-US",
  "ignoreWords": [
    "LiaScript", "Markdown", "GitHub", "workflow"
  ],
  "dictionaries": ["en_US"]
}
```

**Inline language switching:**
```markdown
<!-- cspell:language de-DE -->
Hier ist ein deutscher Absatz.
<!-- cspell:language en-US -->
Here is an English paragraph.
```

### 6.2 Write-Good (Style Checking)

Flags: passive voice, weasel words, clichés, redundant phrases.

```bash
npm install -g write-good
npx write-good *.md
npx write-good *.md --no-passive    # disable passive voice check
```

Options: `--no-passive`, `--no-illusion`, `--no-so`, `--no-adverb`, `--no-tooWordy`, `--no-cliches`

**German:** `npm install -g schreib-gut && write-good *.md --checks=schreib-gut`

### 6.3 Alex (Inclusive Language)

Flags: gender bias, ableist language, racially insensitive terms.

```bash
npm install -g alex
npx alex *.md
```

**Config `.alexrc`:**
```json
{ "allow": ["special"] }
```

### 6.4 Proselint (Advanced Style)

Flags: redundancy, jargon, typography, consistency.

```bash
npm install -g proselint && pip install proselint
npx proselint *.md
```

**Config `.proselintrc`:**
```json
{
  "checks": {
    "typography.diacritical_marks": false,
    "typography.exclamation": false
  }
}
```

---

## 7. GitHub Pages Setup

After first workflow run:
1. Go to repo → **Settings** → **Pages**
2. Under **Source**, select branch: `gh-pages`
3. Click **Save**

Website URL: `https://<username>.github.io/<repository-name>/`

---

## 8. PDF Generation: Puppeteer on GitHub Actions

Puppeteer (headless Chrome) requires two things on GitHub Actions runners:

**1. The `PUPPETEER_ARGS` environment variable (critical — do not skip this):**
```yaml
- name: Generate PDF
  env:
    PUPPETEER_ARGS: "--no-sandbox --disable-setuid-sandbox"
  run: liaex -i README.md --format pdf --output output --pdf-timeout 60000
```

**2. Chromium system libraries (Ubuntu 24 / `ubuntu-latest`):**
```yaml
- name: Install Chromium system dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y \
      libgbm-dev libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
      libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
      libpango-1.0-0 libcairo2 libasound2t64 libnss3 libnspr4 \
      fonts-liberation ca-certificates wget
```

> ⚠️ **Ubuntu 24 uses `libasound2t64`**, not `libasound2`. The old package name causes `apt-get` to fail on `ubuntu-latest` runners.

---

## 9. Minimal `project.yaml` Template

For a LiaScript course project (copy and adapt):

```yaml
title: Course Collection Title

comment: Short description of this collection.

logo: logo.jpg

footer: >
  Created with LiaScript —
  <a href="https://liascript.github.io" target="_blank">LiaScript.github.io</a>

meta:
  title: Course Collection
  description: A collection of interactive educational materials

collection:
  - url: https://raw.githubusercontent.com/USERNAME/REPO/main/materials/1-lecture.md
  - url: https://raw.githubusercontent.com/USERNAME/REPO/main/materials/2-lecture.md
  - url: https://raw.githubusercontent.com/USERNAME/REPO/main/materials/3-exercise.md
```

---

## 10. Key Rules and Gotchas

1. **`force_orphan: true`** — Always use in `peaceiris/actions-gh-pages` to prevent gh-pages branch history from growing. Required for clean deployments.

2. **`project.yaml` URLs must point to raw Markdown** — Use `raw.githubusercontent.com`, not the GitHub HTML page URL.

3. **Web exports need HTTP** — `liaex --format web` outputs cannot be opened via `file://`. Use `npx serve` or Python HTTP server for local testing.

4. **Caching with `-p ./cache`** — Use `--project-generate-cache -p ./cache` to avoid regenerating unchanged PDFs/SCORM in large collections.

5. **SCORM state persistence** — SCORM 1.2 stores location only; use SCORM 2004 for quiz/survey state persistence.

6. **LMS-specific SCORM quirks** — Moodle 4, OPAL, Open edX need `--scorm-embed`; ILIAS, learnworlds.com need `--scorm-iframe`.

7. **Per-course argument overrides** — In `project.yaml`, use `arguments:` under a course entry with long flag names (no leading `--`) to override export settings for individual courses.

8. **Tags are auto-extracted** — If the LiaScript document header has `tags:`, they appear automatically. Override or supplement in `project.yaml`.

9. **Navbar is optional** — If `navbar:` is absent from `project.yaml`, no navigation bar is rendered.

10. **`--project-search`** — Adds full-text fuzzy search (Ctrl+K / Cmd+K shortcut). Requires `navbar:` for the search icon, otherwise shows a floating button.

11. **PDF on GitHub Actions needs two things:** (a) set env var `PUPPETEER_ARGS: "--no-sandbox --disable-setuid-sandbox"` on the PDF step, AND (b) install Chromium system libraries. Use `libasound2t64` — not `libasound2` — on `ubuntu-latest` (Ubuntu 24). See Section 8.

12. **Prevent recursive package growth (critical):** never export into the repository source tree when creating multiple formats in one run. Export into an isolated temp directory first, then copy the final artifacts into a clean staging folder for upload. For Docker exports, mount source read-only and outputs on a separate mount.

---

## 11. Quick Reference: Format Decision Matrix

| Goal | Format | Key flag(s) |
|------|--------|-------------|
| Upload to Moodle 3.x | `scorm1.2` | `--scorm-iframe` |
| Upload to Moodle 4.x | `scorm1.2` | `--scorm-embed` |
| Upload to ILIAS / OpenOLAT | `scorm2004` | `--scorm-iframe` |
| Upload to OPAL / Open edX | `scorm1.2` | `--scorm-embed` |
| Printable PDF | `pdf` | `--pdf-theme`, `--pdf-format` |
| E-reader / ePub | `epub` | `--epub-title`, `--epub-author` |
| Word document | `docx` | optional `--docx-*` |
| Self-hosted interactive course | `web` | `--web-indexeddb` for persistence |
| Android app | `android` | `--android-appId` |
| xAPI / LRS tracking | `xapi` | `--xapi-endpoint` |
| Course catalog website | `project` | `project.yaml` input |
| Metadata export | `rdf` | `--rdf-format jsonld` |

---

---

*Sources: [LiaScript-Exporter GitHub](https://github.com/liascript/liascript-exporter), [Automating LiaScript Transformations](https://liascript.github.io/blog/automating-liascript-transformations-on-github/), [Quality Checks](https://liascript.github.io/blog/quality-checks-on-liascript-with-github-ensuring-document-excellence/), [Creating Project Websites](https://liascript.github.io/blog/creating-project-websites-with-liascript-exporter/) — Retrieved May 2026*
