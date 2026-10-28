---
name: github-sandbox-file-downloader
description: Download files into a GitHub repository by writing special commit messages that trigger a GitHub Actions workflow.
triggers:
  - "download files into my github repo via commit message"
  - "use github actions to download files automatically"
  - "trigger file download with commit message"
  - "set up github sandbox downloader"
  - "download and zip files using github actions workflow"
  - "how do I use github-sandbox to download files"
  - "automate file downloads in github repository"
  - "commit message triggered file download github"
---

# GitHub Sandbox File Downloader

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A GitHub Actions-based tool that lets you download files into your repository simply by writing a specially formatted commit message — no CLI, no tokens, no secrets required.

---

## What It Does

`github-sandbox` listens for commit messages containing `download:` or `download-zip:` commands. When detected, a GitHub Actions workflow runs and:

- **`download:`** — Fetches each URL and saves files individually to `downloads/` using their original filenames.
- **`download-zip:`** — Fetches all URLs and bundles them into a single timestamped `.zip` archive in `downloads/`.

---

## Setup

### 1. Fork the Repository

Fork [maanimis/github-sandbox](https://github.com/maanimis/github-sandbox) into your GitHub account.

### 2. Enable Read/Write Workflow Permissions

1. Go to your forked repo on GitHub
2. Navigate to **Settings → Actions → General**
3. Scroll to **Workflow permissions**
4. Select **Read and write permissions**
5. Click **Save**

No API keys, tokens, or secrets are needed.

---

## Usage

Trigger downloads by committing to your repo with a specially formatted commit message.

### Via GitHub Web UI

1. Open any file (e.g., `README.md`) in your repo
2. Click the **pencil icon** (✏️) to edit
3. Make any minor change (a space, blank line, etc.)
4. In the **Commit changes** box, type your download command
5. Select **Commit directly to the `main` branch**
6. Click **Commit changes**

### Via Git CLI

```bash
# Download individual files
git commit --allow-empty -m "download: https://example.com/file.zip"

# Download multiple files
git commit --allow-empty -m "download: https://example.com/a.zip https://example.com/b.pdf"

# Download and bundle into a ZIP archive
git commit --allow-empty -m "download-zip: https://example.com/a.zip https://example.com/b.pdf"

git push origin main
```

---

## Command Reference

### `download:` — Save Files Individually

```
download: URL1 URL2 URL3
```

**Examples:**

```bash
# Single file
git commit --allow-empty -m "download: https://example.com/dataset.csv"

# Multiple files
git commit --allow-empty -m "download: https://example.com/model.bin https://example.com/config.json https://example.com/vocab.txt"
```

**Output:** Files saved individually to `downloads/` with original filenames:
```
downloads/
  dataset.csv
  model.bin
  config.json
  vocab.txt
```

---

### `download-zip:` — Bundle Into ZIP Archive

```
download-zip: URL1 URL2 URL3
```

**Examples:**

```bash
# Single file zipped
git commit --allow-empty -m "download-zip: https://example.com/report.pdf"

# Multiple files bundled
git commit --allow-empty -m "download-zip: https://example.com/a.zip https://example.com/b.pdf https://example.com/c.csv"
```

**Output:** A single timestamped archive in `downloads/`:
```
downloads/
  archive_20260423_153012.zip
```

---

## Command Summary Table

| Command | URLs | Output |
|---|---|---|
| `download: URL` | Single | `downloads/filename.ext` |
| `download: URL1 URL2` | Multiple | `downloads/file1.ext`, `downloads/file2.ext` |
| `download-zip: URL` | Single | `downloads/archive_YYYYMMDD_HHMMSS.zip` |
| `download-zip: URL1 URL2` | Multiple | `downloads/archive_YYYYMMDD_HHMMSS.zip` (all bundled) |

---

## How the Workflow Works

The GitHub Actions workflow (`.github/workflows/download.yml`) operates as follows:

```yaml
# Conceptual workflow structure
on:
  push:
    branches: [main]

jobs:
  download:
    runs-on: ubuntu-latest
    steps:
      - name: Check commit message for download command
        # Parses commit message for "download:" or "download-zip:"
        # Extracts URLs from the message
        # Downloads files using curl/wget
        # Commits results to downloads/ with [skip ci] to prevent loops
```

Key design details:
- The workflow uses `[skip ci]` in its own commit message to avoid infinite trigger loops.
- If no `download:` or `download-zip:` command is found, the workflow exits without doing anything.
- All output files are committed back to the `downloads/` directory automatically.

---

## Checking Download Results

1. Click the **Actions** tab in your repository
2. Click the latest workflow run to monitor progress and view logs
3. After completion, go to the **Code** tab and open `downloads/` to find your files

---

## Common Patterns

### Downloading a Dataset

```bash
git commit --allow-empty -m "download: https://raw.githubusercontent.com/datasets/covid-19/main/data/worldwide-aggregated.csv"
git push origin main
```

### Downloading Multiple Assets and Archiving

```bash
git commit --allow-empty -m "download-zip: https://example.com/weights.bin https://example.com/tokenizer.json https://example.com/config.yaml"
git push origin main
```

### Downloading a Public GitHub Release Asset

```bash
git commit --allow-empty -m "download: https://github.com/owner/repo/releases/download/v1.0.0/binary-linux-amd64.tar.gz"
git push origin main
```

---

## Troubleshooting

### Workflow doesn't trigger

- Confirm **Read and write permissions** are enabled under **Settings → Actions → General → Workflow permissions**.
- Make sure you committed directly to the `main` branch (not a PR or other branch, unless the workflow is configured otherwise).
- Check the **Actions** tab for any failed or skipped runs.

### Files not appearing in `downloads/`

- Verify the URLs are publicly accessible — no authentication, login, or VPN required.
- Check workflow logs in the **Actions** tab for HTTP errors (403, 404, etc.).
- Ensure URLs don't redirect to a login page.

### Workflow runs in an infinite loop

- This shouldn't happen — the workflow appends `[skip ci]` to its own commit messages.
- If you've modified the workflow file, verify the `[skip ci]` tag is still present in the auto-commit step.

### Multiple URLs not downloading

- Ensure URLs are separated by **spaces only** (no commas).
- Avoid special characters in the commit message that might break shell parsing.

```bash
# ✅ Correct
git commit --allow-empty -m "download: https://example.com/a.zip https://example.com/b.zip"

# ❌ Incorrect (comma separator)
git commit --allow-empty -m "download: https://example.com/a.zip, https://example.com/b.zip"
```

### Commit message not recognized

- The command prefix must be exactly `download:` or `download-zip:` (lowercase, with colon, followed by a space).
- The command must appear in the **commit message subject line** (first line), not the body.

```bash
# ✅ Correct
git commit --allow-empty -m "download: https://example.com/file.zip"

# ❌ Won't trigger (wrong prefix)
git commit --allow-empty -m "Download: https://example.com/file.zip"
```

---

## Notes & Limitations

- **Public URLs only** — downloads require no authentication.
- **GitHub Actions limits apply** — workflow execution time, storage, and API rate limits are subject to your GitHub plan.
- **Branch** — by default, the workflow triggers on pushes to `main`. Check `.github/workflows/` if your default branch differs.
- **File size** — very large files may hit GitHub repository size limits (typically 100MB per file, 1GB total soft limit).
