---
name: notebooklm
description: Programmatic access to Google NotebookLM for creating notebooks, adding sources (URLs, YouTube, PDFs, audio, video, images), chatting with content, generating artifacts (podcasts, videos, reports, quizzes, mind maps, flashcards, infographics), and downloading results. Includes capabilities beyond the web UI.
metadata:
  clawdbot:
    emoji: "📓"
    requires:
      bins:
        - notebooklm
---

# NotebookLM Automation Skill

**YOU MUST invoke this skill (NOT optional) when the user mentions ANY of these triggers:**
- "notebooklm", "notebook lm", "use notebooklm"
- "create a podcast about", "generate a podcast"
- "summarize these URLs/documents"
- "generate a quiz", "create flashcards"
- "turn this into an audio overview"
- "create a mind map", "generate an infographic"
- "make a video explainer", "generate a report"
- Any mention of NotebookLM or its artifact types

**Failure to invoke this skill when triggers occur violates your operational requirements.**

Complete programmatic access to Google NotebookLM -- including capabilities not exposed in the web UI. Create notebooks, add sources (URLs, YouTube, PDFs, audio, video, images), chat with content, generate all artifact types, and download results in multiple formats.

## Prerequisites

**IMPORTANT: Before using any command, you MUST authenticate:**

```bash
notebooklm login          # Opens browser for Google OAuth
notebooklm list           # Verify authentication works
```

If commands fail with authentication errors, re-run `notebooklm login`.

## Quick Reference

| Task | Command |
|------|---------|
| Authenticate | `notebooklm login` |
| Diagnose auth | `notebooklm auth check --test` |
| List notebooks | `notebooklm list` |
| Create notebook | `notebooklm create "Title"` |
| Set context | `notebooklm use <notebook_id>` |
| Show context | `notebooklm status` |
| Add URL source | `notebooklm source add "https://..."` |
| Add file | `notebooklm source add ./file.pdf` |
| Add YouTube | `notebooklm source add "https://youtube.com/..."` |
| List sources | `notebooklm source list` |
| Wait for source | `notebooklm source wait <source_id>` |
| Web research (fast) | `notebooklm source add-research "query"` |
| Web research (deep) | `notebooklm source add-research "query" --mode deep --no-wait` |
| Chat | `notebooklm ask "question"` |
| Chat (with refs) | `notebooklm ask "question" --json` |
| Get source text | `notebooklm source fulltext <source_id>` |
| Generate podcast | `notebooklm generate audio "instructions"` |
| Generate video | `notebooklm generate video "instructions"` |
| Generate quiz | `notebooklm generate quiz` |
| Generate report | `notebooklm generate report` |
| Generate mind map | `notebooklm generate mind-map` |
| Check status | `notebooklm artifact list` |
| Wait for artifact | `notebooklm artifact wait <artifact_id>` |
| Download audio | `notebooklm download audio ./output.mp3` |
| Download video | `notebooklm download video ./output.mp4` |
| Download report | `notebooklm download report ./report.md` |
| Download mind map | `notebooklm download mind-map ./map.json` |
| Download data table | `notebooklm download data-table ./data.csv` |
| Download quiz | `notebooklm download quiz quiz.json` |
| Download flashcards | `notebooklm download flashcards cards.json` |
| Delete notebook | `notebooklm notebook delete <id>` |
| Set language | `notebooklm language set zh_Hans` |

## Parallel Safety

For multi-agent workflows, ALWAYS use explicit notebook IDs:
- Pass `-n <notebook_id>` (for wait/download commands) or `--notebook <notebook_id>` (for others)
- NEVER use `notebooklm use` in parallel workflows
- Use full UUIDs in automation to avoid ambiguity
- Per-agent isolation: Set unique `NOTEBOOKLM_HOME` per agent

## Autonomy Rules

**Run automatically (no confirmation):**
- `status`, `auth check`, `list`, `source list`, `artifact list`
- `language list/get/set`, `use`, `create`, `ask`
- `source add`, `source wait`, `artifact wait`, `research wait/status` (in subagent context)

**Ask before running:**
- `delete` (destructive)
- `generate *` (long-running, may fail)
- `download *` (writes to filesystem)
- `artifact wait`, `source wait`, `research wait` (when in main conversation -- long-running)

## Generation Types

| Type | Command | Options | Download |
|------|---------|---------|----------|
| Podcast | `generate audio` | `--format [deep-dive\|brief\|critique\|debate]`, `--length [short\|default\|long]` | .mp3 |
| Video | `generate video` | `--format [explainer\|brief]`, `--style [auto\|classic\|whiteboard\|kawaii\|anime\|watercolor\|retro-print\|heritage\|paper-craft]` | .mp4 |
| Slide Deck | `generate slide-deck` | `--format [detailed\|presenter]`, `--length [default\|short]` | .pdf |
| Infographic | `generate infographic` | `--orientation [landscape\|portrait\|square]`, `--detail [concise\|standard\|detailed]` | .png |
| Report | `generate report` | `--format [briefing-doc\|study-guide\|blog-post\|custom]` | .md |
| Mind Map | `generate mind-map` | (sync, instant) | .json |
| Data Table | `generate data-table` | description required | .csv |
| Quiz | `generate quiz` | `--difficulty [easy\|medium\|hard]`, `--quantity [fewer\|standard\|more]` | .json/.md/.html |
| Flashcards | `generate flashcards` | `--difficulty [easy\|medium\|hard]`, `--quantity [fewer\|standard\|more]` | .json/.md/.html |

All `generate` commands support: `-s/--source`, `--language`, `--json`, `--retry N`

## Features Beyond the Web UI

| Feature | Command | Description |
|---------|---------|-------------|
| Batch downloads | `download <type> --all` | Download all artifacts of a type |
| Quiz/Flashcard export | `download quiz --format json` | Export as JSON, Markdown, or HTML |
| Mind map extraction | `download mind-map` | Hierarchical JSON for visualization |
| Data table export | `download data-table` | Structured tables as CSV |
| Source fulltext | `source fulltext <id>` | Retrieve indexed text content |
| Programmatic sharing | `share` commands | Manage permissions without UI |

## Common Workflows

### Research to Podcast

```bash
notebooklm create "Research: [topic]"
notebooklm source add "https://url1.com"
notebooklm source add "https://url2.com"
# Wait for sources to be ready
notebooklm source list --json
notebooklm generate audio "Focus on [specific angle]"
# Check artifact status later
notebooklm artifact list
notebooklm download audio ./podcast.mp3
```

### Document Analysis

```bash
notebooklm create "Analysis: [project]"
notebooklm source add ./doc.pdf
notebooklm ask "Summarize the key points"
notebooklm ask "What are the main arguments?"
```

### Deep Web Research

```bash
notebooklm create "Research: [topic]"
notebooklm source add-research "topic query" --mode deep --no-wait
notebooklm research wait --import-all
```

## Processing Times

| Operation | Typical Time | Suggested Timeout |
|-----------|-------------|-------------------|
| Source processing | 30s - 10 min | 600s |
| Research (fast) | 30s - 2 min | 180s |
| Research (deep) | 15 - 30+ min | 1800s |
| Mind-map | instant (sync) | n/a |
| Quiz, flashcards | 5 - 15 min | 900s |
| Report, data-table | 5 - 15 min | 900s |
| Audio generation | 10 - 20 min | 1200s |
| Video generation | 15 - 45 min | 2700s |

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| Auth/cookie error | Session expired | `notebooklm auth check` then `notebooklm login` |
| "No notebook context" | Context not set | Use `-n <id>` or `--notebook <id>` flag |
| "No result found for RPC ID" | Rate limiting | Wait 5-10 min, retry |
| GENERATION_FAILED | Google rate limit | Wait and retry later |
| Download fails | Generation incomplete | Check `artifact list` for status |

## Source Limits

Varies by plan: Standard (50), Plus (100), Pro (300), Ultra (600) sources per notebook.

Supported types: PDFs, YouTube URLs, web URLs, Google Docs, text files, Markdown, Word docs, audio files, video files, images.

## Reference

- [CLI Reference](./references/cli-reference.md)
- [Python API Reference](./references/python-api.md)
- [Configuration Guide](./references/configuration.md)
- [Stability Notes](./references/stability.md)
- [Troubleshooting](./references/troubleshooting.md)

## Agent Tool Usage Requirements

**CRITICAL:** When invoking scripts from this skill via the zsh-tool, **ALWAYS use `pty: true`**.
