---
name: zlib-download
description: Search and download books from Z-Library and Anna's Archive. Use when user wants to find, search, download, or look up books, papers, or ebooks. Trigger phrases include "find book", "search book", "download book", "找书", "下载书籍", "搜书", "book search", "zlibrary", "anna's archive".
---

# Book Tools

Search and download books from multiple sources through a unified CLI.

## Backends

| Backend | Source | Auth Required | Best For |
|---------|--------|---------------|----------|
| **zlib** | Z-Library (EAPI) | Email + Password | Largest catalog, direct download |
| **annas** | Anna's Archive | API Key (donation) | Aggregated sources, multiple mirrors |

## First-Time Setup

On first invocation, run the setup check and guide the user through configuration interactively.

### Step 1: Check Dependencies

```bash
bash ${SKILL_PATH}/scripts/setup.sh check
```

Output is key=value pairs. Check each:

| Key | OK | Missing Action |
|-----|----|----------------|
| `PYTHON` | `ok` | Python 3 not found — user must install it |
| `REQUESTS` | `ok` | Run `bash ${SKILL_PATH}/scripts/setup.sh install-deps` |
| `ANNAS_BINARY` | `ok` | Run `bash ${SKILL_PATH}/scripts/setup.sh install-annas` (optional) |

### Step 2: Configure Credentials

Credentials are stored in `~/.claude/book-tools/.env`. Create the file from the skill's bundled template:

```bash
mkdir -p ~/.claude/book-tools
cp ${SKILL_PATH}/scripts/.env.example ~/.claude/book-tools/.env
```

The `.env` file looks like this:

```
# Z-Library credentials
ZLIB_EMAIL=your_email@example.com
ZLIB_PASSWORD=your_password_here

# Anna's Archive (optional, requires donation for API key)
# ANNAS_SECRET_KEY=your_api_key_here
```

**IMPORTANT**: Do NOT ask the user for credentials directly in chat. Instead:
1. Create the `.env` file (or `.env.example` template)
2. Tell the user to edit `~/.claude/book-tools/.env` with their credentials
3. Wait for the user to confirm they've filled it in
4. Then proceed with search

Alternatively, credentials can be set via CLI (less recommended — visible in shell history):

```bash
python3 ${SKILL_PATH}/scripts/book.py config set --zlib-email "user@example.com" --zlib-password "password"
```

### Step 3: Verify

```bash
python3 ${SKILL_PATH}/scripts/book.py setup
```

Expected output when Z-Library is configured:
```json
{
  "zlib": { "requests_installed": true, "configured": true },
  "annas": { "binary_found": true, "api_key_configured": false }
}
```

If `configured` is `true`, the skill is ready to use.

### Credential Storage Details

Two sources are merged (`.env` values take priority):

| Source | Path | Format |
|--------|------|--------|
| `.env` file | `~/.claude/book-tools/.env` | `KEY=value` per line |
| Config JSON | `~/.claude/book-tools/config.json` | JSON (auto-managed) |

On first successful Z-Library login, remix tokens are cached in `config.json` — subsequent calls skip the email/password login and use tokens directly.

## Workflow

The typical flow is: **search → pick → download**.

### 1. Search

```bash
# Auto-detect backend (tries zlib first, then annas)
python3 ${SKILL_PATH}/scripts/book.py search "machine learning" --limit 10

# Z-Library with filters
python3 ${SKILL_PATH}/scripts/book.py search "deep learning" --source zlib --lang english --ext pdf --limit 5

# Anna's Archive
python3 ${SKILL_PATH}/scripts/book.py search "reinforcement learning" --source annas

# Chinese books
python3 ${SKILL_PATH}/scripts/book.py search "莱姆 索拉里斯" --source zlib --lang chinese --limit 5
```

**Output** (JSON to stdout):
```json
{
  "source": "zlib",
  "count": 5,
  "books": [
    {
      "source": "zlib",
      "id": "12345",
      "hash": "abc123def",
      "title": "Deep Learning",
      "author": "Ian Goodfellow",
      "year": "2016",
      "language": "english",
      "extension": "pdf",
      "filesize": "22.5 MB"
    }
  ]
}
```

### 2. Present Results to User

After searching, present results as a **numbered table** so the user can pick:

```
| # | Title | Author | Year | Format | Size |
|---|-------|--------|------|--------|------|
| 1 | Deep Learning | Ian Goodfellow | 2016 | pdf | 22.5 MB |
| 2 | ... | ... | ... | ... | ... |
```

If results span multiple languages or editions, **group them by language or category** with sub-headings for clarity.

Ask: "Which book would you like to download? (number)"

### 3. Download

```bash
# Z-Library download (needs id + hash from search results)
python3 ${SKILL_PATH}/scripts/book.py download --source zlib --id 12345 --hash abc123def -o ~/Downloads/

# Anna's Archive download (needs MD5 hash from search results)
python3 ${SKILL_PATH}/scripts/book.py download --source annas --hash a1b2c3d4e5 --filename "deep_learning.pdf" -o ~/Downloads/
```

**Output**:
```json
{
  "source": "zlib",
  "status": "ok",
  "path": "~/Downloads/Deep Learning (Ian Goodfellow).pdf",
  "size": 23592960
}
```

### 4. Report to User

After download, report:
- File path (so user can open it)
- File size
- Any remaining download quota (Z-Library has daily limits)

## Other Commands

### Book Info (Z-Library only)

```bash
python3 ${SKILL_PATH}/scripts/book.py info --source zlib --id 12345 --hash abc123def
```

Returns full metadata: description, ISBN, pages, table of contents, etc.

### Check Config

```bash
python3 ${SKILL_PATH}/scripts/book.py config show
```

### Check Backend Status

```bash
python3 ${SKILL_PATH}/scripts/book.py setup
```

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| "Z-Library not configured" | No credentials | Guide user to edit `~/.claude/book-tools/.env` |
| "Z-Library login failed" | Bad credentials or service down | Ask user to verify credentials. Z-Library domains change — if persistent, the vendored `Zlibrary.py` domain may need updating. |
| "annas-mcp binary not found" | Binary not installed | Run `setup.sh install-annas` |
| "Anna's Archive API key not configured" | No API key | Guide user to donate at Anna's Archive for API access, then add key to `.env` |
| Search timeout | Network issue | Retry once. If persistent, try the other backend. |
| "No backend available" | Neither backend configured | Walk through full setup flow from Step 1 |

## Tips

- Z-Library has a daily download limit (usually 10/day for free accounts). Use `info` to check a book before downloading to avoid wasting quota.
- Anna's Archive requires an API key for both search and download (obtained via donation).
- For Chinese books, use `--lang chinese` with Z-Library for best results.
- If Z-Library is unreachable, automatically fall back to Anna's Archive with `--source auto`.
- When searching for a specific author in multiple languages, run parallel searches (e.g. English name + Chinese name) and merge results into one table.
