---
name: tikspyder
description: Run the TikSpyder tool to collect TikTok data — search by keyword, username, or hashtag download videos, extract keyframes, and export structured data. Use this skill whenever the user wants to collect TikTok data, search TikTok profiles or hashtags, search TikTok videos, download TikTok content, run tikspyder, or launch the TikSpyder Streamlit interface. Also trigger when the user mentions data collection from TikTok, even if they don't say "tikspyder" by name.
---

# TikSpyder — Guided TikTok Data Collection

You are guiding a user (who may not be technical) through collecting TikTok data using TikSpyder, an open-source data collection tool. Your job is to set up the environment, configure credentials, gather search parameters conversationally, run the tool, and summarize results.

Throughout this process, communicate clearly and explain what you're doing at each step. If something fails, explain the error in plain language and suggest a fix.

---

## Phase 1: Locate TikSpyder & Environment Check

Before anything else, find (or install) TikSpyder and verify the environment is ready. Work through these steps in order and track two key variables:

- **TIKSPYDER_DIR** — the root of the TikSpyder source repo (contains `main.py`, `config/`, etc.)
- **SKILL_DIR** — the directory where this skill file lives

### Conda activation note

Throughout this skill, whenever you need to activate a conda environment in a bash command, you must initialize the shell hook first. The pattern is:

```bash
conda_init="eval \"\$(conda shell.bash hook)\"" && $conda_init && conda activate tikspyder
```

Bare `conda activate` will fail in non-interactive shells. Always use the full pattern above. This applies to Phase 1, Phase 4, and Phase 5.

### 1.1 Find the skill directory

The skill directory contains this SKILL.md file. Search for it in standard locations:

```bash
for candidate in .claude/skills/tikspyder "$HOME/.claude/skills/tikspyder"; do
  if [ -f "$candidate/SKILL.md" ]; then
    echo "SKILL_DIR=$candidate"
    break
  fi
done
```

Store this as SKILL_DIR for later use.

### 1.2 Check if tikspyder is already installed

Try these checks in order. Stop at the first one that works.

**Step A — Check current environment:**

```bash
pip show tikspyder 2>&1
```

If found, extract `Location:` and verify `main.py` exists there. Set TIKSPYDER_DIR accordingly.

**Step B — Check for a conda/mamba environment named `tikspyder`:**

```bash
conda env list 2>/dev/null | grep tikspyder
```

If a `tikspyder` environment exists, activate it (using the conda pattern from above) and run `pip show tikspyder` again. If found, use that environment for all subsequent commands.

**Step C — Check if repo is already cloned in the skill directory:**

```bash
ls "$SKILL_DIR/tik-spyder/main.py" 2>/dev/null
```

If found, set `TIKSPYDER_DIR=$SKILL_DIR/tik-spyder`.

### 1.3 Download and install if needed

If TikSpyder isn't found by any of the checks above, download the official repository from GitHub into the skill directory:

```bash
cd "$SKILL_DIR"
git clone https://github.com/estebanpdl/tik-spyder.git
```

Then set `TIKSPYDER_DIR=$SKILL_DIR/tik-spyder`.

### 1.4 Python version

```bash
python --version 2>&1 || python3 --version 2>&1
```

TikSpyder needs Python 3.11 or newer. If the version is too old, tell the user and stop.

### 1.5 Create environment and install (only if tikspyder wasn't found in 1.2)

If tikspyder is already installed (found in Step A or B), skip this entirely.

Otherwise, create an environment and install. First check whether conda/mamba is available:

```bash
conda --version 2>/dev/null || mamba --version 2>/dev/null
```

**If conda/mamba is available**, create a dedicated environment, activate it (using the conda pattern), and install TikSpyder from the cloned repository with `pip install -e .` inside TIKSPYDER_DIR.

**If conda/mamba is not available**, use Python's built-in venv:

```bash
cd "$TIKSPYDER_DIR"
python -m venv .venv
```

Activate — the path differs by platform:
- **Windows (Git Bash):** `source "$TIKSPYDER_DIR/.venv/Scripts/activate"`
- **macOS / Linux:** `source "$TIKSPYDER_DIR/.venv/bin/activate"`

Then install with `pip install -e .` inside TIKSPYDER_DIR.

Verify it works regardless of which environment type was created:

```bash
tikspyder --help
```

Tell the user which environment type was set up (conda or venv) so they know for future reference.

### 1.6 Check ffmpeg

```bash
ffmpeg -version 2>&1 | head -1
```

ffmpeg is needed for audio extraction and keyframe extraction. If missing, tell the user clearly what they'll lose and ask whether to proceed:

- "ffmpeg is not installed. Without it, TikSpyder can still download videos and collect metadata, but audio extraction and keyframe extraction will be skipped. You can install it from https://ffmpeg.org/download.html. Would you like to proceed without ffmpeg, or install it first?"

If the user wants to proceed without ffmpeg, that's fine — just remember this for Phase 4 so you're not surprised by `No such file or directory: 'ffmpeg'` errors in the output (they're expected and harmless).

### 1.7 Summary and readiness check (STOP HERE before continuing)

Before moving to Phase 2, present a readiness report and wait for user confirmation. Do NOT proceed until the user says it's OK. This prevents wasting API credits or running commands in a broken environment.

Show something like:

```
Environment readiness:
- Python: 3.12 (OK)
- TikSpyder: v0.1.0 installed (conda env: tikspyder)
- ffmpeg: not installed (audio extraction and keyframes will be skipped)

Ready to continue with API key setup?
```

If any critical requirement is missing (Python too old, tikspyder failed to install), stop here and help the user fix it. If only ffmpeg is missing, the user can choose to proceed — but they must explicitly confirm.

---

## Phase 2: API Key Configuration

TikSpyder uses two external APIs:

- **SerpAPI** — powers Google-based TikTok search (Google search results + Google Images thumbnails)
- **Apify** — powers direct TikTok profile and hashtag data collection

**Important:** TikSpyder runs SerpAPI calls in ALL modes — even `--user` and `--tag` modes trigger Google search and Google Images calls before the Apify step. Without a valid SerpAPI key, those calls will fail with 401 errors. The Apify step will still work, but data collection will be incomplete. For best results, configure both keys regardless of which search mode the user plans to use.

### 2.1 Check existing keys

Read the config file at `$TIKSPYDER_DIR/config/config.ini` using the Read tool. Check whether `api_key` and `apify_token` contain real credentials.

**A key is NOT valid if it:**
- Is empty or whitespace
- Contains the word `your` (e.g., `your_serp_api_key`, `your_apify_token`)
- Is literally `<the_key>` or `<the_token>`
- Is shorter than 20 characters (real API keys are longer)

**Security rules:**
- NEVER print, display, or echo API keys back to the user
- When reporting status, say "SerpAPI key: configured" or "Apify token: not configured" — never show the actual values
- When writing keys to the config file, use the Write tool directly — do not use echo/cat in bash where the key would appear in the command

### 2.2 Ask for missing keys

If either key is invalid, ask the user for it. Ask for ALL missing keys at once — don't ask for just one and discover the other is missing later during execution.

Explain what each API is for:

- "**SerpAPI key** — This lets TikSpyder search Google for TikTok content. You can get one at https://serpapi.com/ (they have a free tier)."
- "**Apify token** — This lets TikSpyder collect TikTok profiles and hashtags directly. You can get one at https://apify.com/ (they have a free tier). Required for user profile and hashtag searches."

If the user can only provide one key, that's OK — explain what will and won't work:
- SerpAPI only: keyword searches work fully; user/hashtag modes will fail
- Apify only: user/hashtag collection works but Google search/images steps will show 401 errors (data collection still succeeds via Apify, just with incomplete results)

### 2.3 Save keys

Write the config file at `$TIKSPYDER_DIR/config/config.ini` using this exact format:

```ini
[SerpAPI Key]
api_key = <the_key>

[Apify Token]
apify_token = <the_token>
```

Preserve any existing valid key if the user only provides one of the two.

---

## Phase 3: Collect Search Parameters

Ask the user what they want to collect. Use AskUserQuestion to make this conversational. Here's the decision tree:

### 3.1 Search mode (required)

Ask: "What would you like to search for?"

| Mode | CLI flag | Notes |
|------|----------|-------|
| Keyword search | `--q "term"` | Searches Google for TikTok results matching the term |
| User profile | `--user username` | Collects a specific TikTok user's videos (requires `--apify`) |
| Hashtag | `--tag hashtag` | Collects videos with a specific hashtag (requires `--apify`) |

If the user picks user or hashtag mode, the `--apify` flag is automatically required — add it without asking.

Also validate that the required API key is configured for the chosen mode. If user picks keyword search but SerpAPI key is missing, go back to Phase 2. Same for Apify with user/hashtag modes.

### 3.2 Additional parameters

After knowing the search mode, ask about these options. You don't need to ask about every single one — use judgment based on the user's goal. Present the most relevant options:

**For keyword searches:**
- Country (`--gl`, e.g., `us`, `gb`, `mx`) — "Which country should Google search from?"
- Language (`--hl`, e.g., `en`, `es`, `fr`) — "What language?"
- Date range (`--after` / `--before`, format YYYY-MM-DD) — "Want to limit to a specific date range?"
- Search depth (`--depth`, default 3) — "How deep should related content search go? Default is 3 levels."

**For user/hashtag searches (Apify):**
- Date filters (`--oldest-post-date` / `--newest-post-date`, format YYYY-MM-DD)
- Number of results (`--number-of-results`, default 25)

**For all modes:**
- Download videos? (`--download`) — "Do you want to download the actual video files?"
- Output directory (`--output`) — "Where should I save the results? Default creates a timestamped folder in `./tikspyder-data/`."
- Worker threads (`--max-workers`) — Only mention if the user seems technical or asks about speed. Default is 5 for downloads, 3 for keyframes.

### 3.3 Date synchronization (critical)

TikSpyder uses **two separate date filtering systems** that operate independently:

- **SerpAPI dates** (`--after` / `--before`) — filter the Google search results
- **Apify dates** (`--oldest-post-date` / `--newest-post-date`) — filter the Apify results

When the user specifies any date range, you MUST set the corresponding flags for BOTH systems. Otherwise one API returns filtered results while the other returns everything, mixing date-filtered and unfiltered data.

**Mapping:**
| User says | SerpAPI flag | Apify flag |
|-----------|-------------|------------|
| "after [date]" / "since [date]" / "from [date]" | `--after [date]` | `--oldest-post-date [date]` |
| "before [date]" / "until [date]" | `--before [date]` | `--newest-post-date [date]` |

**Example:** If the user says "videos after January 2026", the command needs BOTH:
```
--after 2026-01-01 --oldest-post-date 2026-01-01
```

This applies to all search modes — keyword, user, and hashtag.

### 3.4 Confirm before running

Before executing, show the user a plain-language summary of what will happen:

```
Here's what I'm about to run:
- Search: keyword "election misinformation"
- Country: US, Language: English
- Date range: after 2025-01-01
- Download videos: yes
- Output: ./tikspyder-data/1234567890/
```

Ask for confirmation before proceeding.

---

## Phase 4: Execute

### 4.1 Activate environment if needed

Reactivate the same environment that was discovered/created in Phase 1. If using conda, use the conda activation pattern from the top of this document. If using venv, source the activate script (Windows: `.venv/Scripts/activate`, macOS/Linux: `.venv/bin/activate`).

### 4.2 Build and run the command

Construct the tikspyder CLI command from the collected parameters. Always `cd` into TIKSPYDER_DIR first so the config file is found correctly.

Example commands:

```bash
# Keyword search with date filter
cd "$TIKSPYDER_DIR" && tikspyder --q "search term" --gl us --hl en \
  --after 2025-01-01 --before 2025-06-01 --output ./data/ --download

# User profile with date filter (note: BOTH --after AND --oldest-post-date)
cd "$TIKSPYDER_DIR" && tikspyder --user username --apify \
  --after 2025-01-01 --oldest-post-date 2025-01-01 --output ./data/

# Hashtag with date filter
cd "$TIKSPYDER_DIR" && tikspyder --tag hashtag --apify \
  --after 2025-01-01 --oldest-post-date 2025-01-01 \
  --number-of-results 50 --output ./data/ --download
```

Remember to prepend the conda or venv activation before `cd` if needed.

Run the command and let the user see the output. Use a generous timeout (up to 10 minutes) since data collection can take a while depending on the search scope.

### 4.3 Error handling

The command may exit with errors even when data was partially collected. Check the output directory before concluding the run failed — partial success is common.

**Expected noise (not errors):**

| Output | Explanation |
|--------|-------------|
| `Error extracting audio: No such file or directory: 'ffmpeg'` | ffmpeg not installed — videos are still downloaded, only audio extraction is skipped. Harmless if user chose to proceed without ffmpeg in Phase 1. |

**Errors that need action:**

| Error | Likely cause | Fix |
|-------|-------------|-----|
| `ValueError: Either --user, --q or --tag must be provided` | Missing search term | Ask what they want to search |
| `401 Client Error: Unauthorized` from serpapi.com | SerpAPI key is invalid or still a placeholder | This should NOT happen — it means Phase 2 failed to detect an invalid key. Ask the user for the correct key, save it, and rerun. Review Phase 2.1 validation rules to understand what went wrong. |
| `IndexError: list index out of range` in `sql_manager.py` | SerpAPI returned no data, leaving the SQL database empty | This is a downstream symptom of a bad SerpAPI key. Same fix as above. |
| `ApifyApiError: User was not found or authentication token is not valid` | Bad Apify token | Ask user to check their token at https://console.apify.com/account |
| `RuntimeError` with asyncio | Event loop conflict | Run `cd "$TIKSPYDER_DIR" && git pull` to get the latest fix |
| Connection/timeout errors | Network issues | Suggest checking internet connection, or trying with fewer results |

### 4.4 Post-run summary

After the command finishes, inspect the output directory and summarize what was collected:

```bash
find <output_dir> -type f | head -50
ls -la <output_dir>/*.csv 2>/dev/null
ls <output_dir>/downloaded_videos/ 2>/dev/null | wc -l
ls <output_dir>/keyframes/ 2>/dev/null | wc -l
du -sh <output_dir>
```

Report to the user:
- Number of CSV data files generated
- Number of videos downloaded (if applicable)
- Number of keyframes extracted (if applicable)
- Total size of the output directory
- Path to the main CSV file(s) they can open in Excel or Google Sheets

---

## Phase 5: Streamlit App (Alternative)

If the user says they'd prefer a visual interface, or if they seem unsure about parameters and might benefit from a UI, offer to launch the Streamlit web app instead.

Make sure environment and API keys are configured (Phases 1-2) before launching.

Activate the environment (conda or venv, same as Phase 4), then run:

```bash
cd "$TIKSPYDER_DIR" && tikspyder --app
```

This starts a local web server at `http://localhost:8501`. Tell the user:
- "I've launched the TikSpyder web interface. It should open in your browser at http://localhost:8501"
- "The web interface lets you configure searches, set download options, and track progress visually"
- "When you're done, come back and tell me — I'll stop the server"

The Streamlit app runs as a blocking process. To keep the conversation going while it runs, launch it in the background using `run_in_background`. When the user is done, find and stop the process listening on port 8501.

---

## Quick Reference: Full CLI Flags

| Flag | Type | Description |
|------|------|-------------|
| `--q` | string | Search keyword/phrase |
| `--user` | string | TikTok username |
| `--tag` | string | TikTok hashtag |
| `--gl` | string | Country code (e.g., `us`) |
| `--hl` | string | Language code (e.g., `en`) |
| `--cr` | string | Multiple country filter |
| `--lr` | string | Multiple language filter |
| `--safe` | string | Adult content filter: `active` (default) or `off` |
| `--google-domain` | string | Google domain (default: `google.com`) |
| `--depth` | int | Related content depth (default: 3) |
| `--before` | string | Date upper bound (YYYY-MM-DD) |
| `--after` | string | Date lower bound (YYYY-MM-DD) |
| `--apify` | flag | Enable Apify integration |
| `--oldest-post-date` | string | Apify: oldest post date (YYYY-MM-DD) |
| `--newest-post-date` | string | Apify: newest post date (YYYY-MM-DD) |
| `--number-of-results` | int | Apify: max results (default: 25) |
| `-d, --download` | flag | Download video files |
| `-w, --max-workers` | int | Thread count for downloads |
| `-o, --output` | string | Output directory path |
| `--app` | flag | Launch Streamlit web UI |
