---
name: daily-digest
description: >
  Run a daily content digest pipeline that fetches Podcast RSS feeds and YouTube
  channels, transcribes audio, generates AI summaries in Traditional Chinese, and
  optionally sends notifications via Telegram. Use this skill whenever the user wants
  to: set up or run a daily digest, summarize podcasts or YouTube videos, create a
  content briefing, aggregate RSS/YouTube content, or build an automated summary
  system. Also triggers for: "daily digest", "每日摘要", "podcast 摘要",
  "YouTube 整理", "跑摘要", "內容彙整", "幫我整理今天的 podcast",
  "summarize my subscriptions", or any request to periodically collect and
  summarize media content. Even if the user just says "digest" or "摘要",
  check if this skill applies.
user-invocable: true
argument-hint: "[run|setup|add <url>|status|cleanup|help]"
metadata:
  author: abe1272001
  original-author: ray870211
  version: 0.5.0
  license: MIT
compatibility: >
  Requires: Python 3.10+, yt-dlp, faster-whisper, feedparser, httpx, pyyaml.
  macOS/Linux. Claude CLI authenticated.
---

# Daily Digest — Execution Skill

You are an autonomous content digest operator. Your job is to save the user time by
turning hours of podcast/YouTube content into a concise, actionable briefing they can
read in minutes.

Pipeline: fetch → transcribe → summarize → cross-analyze → output (→ notify).

## Environment Setup

All runtime data lives in a fixed home directory so it works from any CWD:

```bash
DD_HOME="$HOME/.daily-digest"
VENV_PY="$DD_HOME/venv/bin/python"
DD_CONFIG="$DD_HOME/config"
DD_WORKSPACE="$DD_HOME/workspace"
SCRIPTS="${CLAUDE_SKILL_DIR}/scripts"
```

Every script invocation: `$VENV_PY $SCRIPTS/script_name.py ...`

### Pre-flight check (run before ANY command except `setup`)

Before executing pipeline, status, cleanup, or add — ensure directory structure exists
and venv is valid:

```bash
mkdir -p "$DD_HOME/config" "$DD_HOME/workspace/fetched" "$DD_HOME/workspace/summaries" "$DD_HOME/workspace/transcripts"
test -f "$DD_HOME/venv/bin/python" && echo "OK" || echo "MISSING"
```

If **MISSING**, tell the user and run setup automatically:
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/setup.py" --install --venv-dir "$DD_HOME/venv"
```

This prevents the pipeline from silently failing when dependencies aren't installed.

## Language / i18n

Read `$DD_CONFIG/settings.yaml` for the `language` field. Default: `en`.

## Display Strategy

Present all status, progress, and results **directly in your response as markdown**.
Claude Code collapses Bash tool output, so users miss Rich panels rendered by scripts.
Instead, format information yourself using markdown headers, tables, bold text, and
lists — these are always visible in the conversation.

Use scripts only for **data gathering** (fetch, transcribe, config loading, etc.),
then format and present the results in your own response text.

## Command Routing

Parse `$ARGUMENTS`:

| Command | Action |
|---------|--------|
| (empty) / `help` | Show help (see template below) |
| `run` | Execute the full pipeline |
| `setup` | Run first-time setup |
| `add <url>` | Add a new source |
| `status` | Show status |
| `cleanup` | Clean up old workspace files |

Do NOT execute pipeline when showing help.

### Help display

When showing help, output this directly (adapt language per settings):

```
## 📰 Daily Digest v0.5.0

| Command | Description |
|---------|-------------|
| `/daily-digest setup` | First-time setup (sources + notifications) |
| `/daily-digest run` | Run the full digest pipeline |
| `/daily-digest add <url>` | Add a Podcast or YouTube source |
| `/daily-digest status` | View sources and run status |
| `/daily-digest cleanup` | Clean up old workspace files |
| `/daily-digest help` | Show this help |
```

## Important: You ARE the summarizer

You are already an LLM running inside the user's session. Summarize and analyze
content directly — no need to shell out to `claude -p`. This is faster, uses fewer
tokens, and produces better results because you have the full pipeline context.

## First-Time Setup

Use **AskUserQuestion** for all user interaction. Display progress in your response.

### [1/4] Check Dependencies

Output: `**[1/4] ✓ Check dependencies**`

Create home directory, venv, and install deps (uses system Python since venv doesn't exist yet):
```bash
mkdir -p "$DD_HOME/config" "$DD_HOME/workspace/fetched" "$DD_HOME/workspace/summaries" "$DD_HOME/workspace/transcripts"
python3 "${CLAUDE_SKILL_DIR}/scripts/setup.py" --install --venv-dir "$DD_HOME/venv"
```

After this, all subsequent commands use `$VENV_PY`.

### [2/4] Configure Sources

Output: `**[2/4] ● Configure sources**`

**AskUserQuestion**: "What Podcast RSS feeds or YouTube channels do you want to track?"

For each source, look up the real name so the user sees proper channel names:
```bash
$VENV_PY $SCRIPTS/fetch_podcast.py --url "RSS_URL" --get-feed-title --output-dir /tmp/dd-test
$VENV_PY $SCRIPTS/fetch_youtube.py --channel "@handle" --get-channel-name --output-dir /tmp/dd-test
```

Create `$DD_CONFIG/sources.yaml`:
```yaml
sources:
  - name: "Actual Channel Name"
    type: podcast
    url: "https://..."
    limit: 5
```

### [3/4] Configure Notifications (OPTIONAL)

Output: `**[3/4] ● Configure notifications**`

**AskUserQuestion** with radio options:

```
Would you like to set up notifications?
  ○ Telegram Bot — recommended, works great on mobile & desktop
  ○ Skip for now — digests saved as local Markdown only
```

**If Telegram:** ask for Bot Token and Chat ID, save to `$DD_CONFIG/telegram.yaml`.
**If Skip:** do NOT create `telegram.yaml`.

### [4/4] Validate

Output: `**[4/4] ● Validate setup**`

Test each source with a 1-item fetch:
```bash
$VENV_PY $SCRIPTS/fetch_podcast.py --url "URL" --limit 1 --output-dir /tmp/dd-test
$VENV_PY $SCRIPTS/fetch_youtube.py --channel "HANDLE" --limit 1 --output-dir /tmp/dd-test
```

If Telegram configured:
```bash
$VENV_PY $SCRIPTS/notify_telegram.py --config "$DD_CONFIG/telegram.yaml" --test
```

Create `$DD_CONFIG/settings.yaml`:
```yaml
language: en
```

Show completion summary in your response:

```
## ✅ Setup Complete

**Sources:**
- 🎙 [podcast] Gooaye 股癌
- 📺 [youtube] M觀點

**Notifications:** Telegram ✓
**Next step:** `/daily-digest run`
```

## Status Command

```bash
$VENV_PY $SCRIPTS/config_loader.py --sources "$DD_CONFIG/sources.yaml" --state "$DD_CONFIG/state.json"
```

Parse the JSON output, check if `$DD_CONFIG/telegram.yaml` exists, then display in your response:

```
## 📊 Daily Digest Status

| # | Type | Name | URL |
|---|------|------|-----|
| 1 | podcast | 股癌 | https://... |

**Notifications:** Telegram ✓
**Last run:** 2026-03-08
**Processed:** 42 items
```

## Pipeline Execution

Show progress **in your response text** as you complete each step. Use a checklist
format that you update by outputting the current state:

```
**Pipeline Progress:**
- ✅ Load config — 3 sources
- ✅ Fetch content — 12 items
- ⏳ Deduplicate...
- ○ Transcribe
- ○ Summarize
- ○ Cross-analyze
- ○ Write output
- ○ Notify
- ○ Update state
- ○ Cleanup
```

### Step 1: Load Config & State

```bash
$VENV_PY $SCRIPTS/config_loader.py \
  --sources "$DD_CONFIG/sources.yaml" \
  --state "$DD_CONFIG/state.json"
```

If `state.json` doesn't exist (first run), use `--since-days 2` for YouTube to
avoid an overwhelming backlog of old videos.

### Step 2: Fetch Content

**Podcast:**
```bash
$VENV_PY $SCRIPTS/fetch_podcast.py \
  --url "RSS_URL" --limit 5 --source-name "Name" \
  --download-audio --output-dir "$DD_WORKSPACE/fetched/"
```

**YouTube** (auto-skips member-only content):
```bash
$VENV_PY $SCRIPTS/fetch_youtube.py \
  --channel "HANDLE" --limit 5 --source-name "Name" \
  --filter-livestream --transcript both \
  --since-days 2 \
  --output-dir "$DD_WORKSPACE/fetched/"
```

### Step 3: Deduplicate

Compare fetched item IDs against `processed_ids` from Step 1. The state file
tracks every processed item, so duplicates are automatically filtered out
regardless of how often a channel publishes.

### Step 4: Transcribe (if needed)

Only for items that have audio but no transcript (e.g., podcasts without subtitles):
```bash
$VENV_PY $SCRIPTS/transcribe.py --audio "path/to/audio.wav" --model tiny --language zh
```

### Step 5: Summarize (YOU do this)

Read transcripts and produce summaries **directly in your response**.
Write in the language specified in settings.yaml.

Each item gets:
- **Key Summary** — 3-5 bullet points covering the main content
- **Key Insights** — Notable analysis, quotes, data points
- **Key Numbers** — Specific stats or metrics mentioned (if any)

Keep each summary 300-800 characters. Be faithful to the source — save your
opinions for the cross-analysis.

### Step 6: Cross-Source Analysis (YOU do this)

This is where you add real analytical value. Generate 6 dimensions:

1. **Common Themes** — What the ecosystem is talking about across sources
2. **Different Perspectives** — Where sources disagree or offer different angles
3. **Sentiment Map** — Per-source tone on each major topic
4. **Key Numbers** — Most important data points aggregated in one place
5. **Actionable Takeaways** — Categorized as 🔍 Research / 👁 Monitor / 🚀 Try
6. **Priority Reading** — Rank items by relevance so the user knows what to read first

### Step 7: Write Output (Dual Format)

Save **both** formats — Markdown for the user, JSON for programmatic access:

```bash
# Markdown → $DD_WORKSPACE/summaries/YYYY-MM-DD.md
# JSON    → $DD_WORKSPACE/summaries/YYYY-MM-DD.json
```

For the JSON schema, read `${CLAUDE_SKILL_DIR}/references/pipeline.md`.
Save transcripts to `$DD_WORKSPACE/transcripts/`.

### Step 8: Notify (if configured)

Only if `$DD_CONFIG/telegram.yaml` exists:
```bash
$VENV_PY $SCRIPTS/notify_telegram.py \
  --config "$DD_CONFIG/telegram.yaml" \
  --file "$DD_WORKSPACE/summaries/YYYY-MM-DD.md"
```

### Step 9: Update State

```bash
$VENV_PY $SCRIPTS/update_state.py \
  --state "$DD_CONFIG/state.json" \
  --processed-ids "id1,id2,id3"
```

### Step 10: Cleanup (auto)

Keep workspace size manageable by removing old audio files after each run:
```bash
$VENV_PY $SCRIPTS/cleanup.py --workspace "$DD_WORKSPACE/"
```

### Pipeline Complete

Display the digest preview and completion summary in your response:

```
## 📰 Daily Digest — 2026-03-08

### 🎙 股癌 — EP.420 標題
📅 2026-03-08
**Key Summary:** • point 1 • point 2
**Key Numbers:** 📊 stat 1

---

## 🔗 Cross-Source Analysis
### Common Themes
...
### Actionable Takeaways
- 🔍 [Research] ...
- 🚀 [Try] ...

---

✅ **Pipeline Complete**
- **Date:** 2026-03-08
- **New items:** 5 (2 podcast + 3 youtube)
- **Digest:** `~/.daily-digest/workspace/summaries/2026-03-08.md`
- **Notification:** ✓ Telegram sent
```

## Cleanup Command

Manually trigger workspace cleanup. Useful with `/loop` for automated scheduling:

```bash
$VENV_PY $SCRIPTS/cleanup.py --workspace "$DD_WORKSPACE/" [--dry-run] [--verbose]
```

Display results in your response:

```
## 🧹 Workspace Cleanup

- **Deleted:** 12 files
- **Freed:** 245.3 MB
- **Kept:** 38 files

💡 Automate with: `/loop 1d /daily-digest cleanup`
```

Retention policy: audio kept 1 week, transcripts 1 month, summaries indefinitely.
Full retention details in `references/pipeline.md`.

## Error Handling

- Fetch fails for one source → log and continue with others
- Transcription fails → skip item, note in digest
- Telegram fails → digest still saved locally, tell user
- Never let one failure abort the entire pipeline

## Adding Sources

**AskUserQuestion** to confirm source details. Get the real name:
```bash
$VENV_PY $SCRIPTS/fetch_podcast.py --url "URL" --get-feed-title --output-dir /tmp/dd-test
$VENV_PY $SCRIPTS/fetch_youtube.py --channel "HANDLE" --get-channel-name --output-dir /tmp/dd-test
```

Edit `$DD_CONFIG/sources.yaml`, validate with a 1-item fetch, then display:

```
## ✅ Source Added

- **Name:** Some Podcast 好節目
- **Type:** podcast
- **URL:** https://feeds.soundon.fm/...
- **Validation:** ✓ Fetched 1 test item
```

## Scheduling

Read `${CLAUDE_SKILL_DIR}/references/scheduling.md` for launchd/cron setup.
