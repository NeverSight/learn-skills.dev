---
name: youtube-content
description: Extract and analyze YouTube video content (transcripts + metadata). Use when the user explicitly requests to analyze, summarize, extract wisdom from, or get context from a YouTube video. Supports wisdom extraction, summary, Q&A prep, key quotes, and custom analysis. Does NOT auto-trigger on YouTube URLs - only when analysis is explicitly requested.
license: Apache-2.0
---

# YouTube Content

Extract transcripts and metadata from YouTube videos for analysis.

## Workflow

1. Extract video ID from URL
2. Run fetch script from skill directory
3. Present metadata summary to user
4. Apply requested analysis mode to transcript
5. Save analysis and raw transcript to knowledge base (auto, use `--no-save` to skip)

## Fetch Script

Run from the skill directory (`~/.claude/skills/youtube-content/`):

```bash
uv run ~/.claude/skills/youtube-content/scripts/fetch_youtube.py "https://youtube.com/watch?v=VIDEO_ID"
```

Options:
- `--metadata-only` - Skip transcript extraction
- `--transcript-only` - Skip metadata extraction
- `--with-segments` - Include timestamped segments (for quote extraction)

Output: JSON with `{video_id, metadata, transcript, errors}`

By default, transcript contains only `text` and `language`. Use `--with-segments` when timestamps are needed (e.g., Quotes mode).

## Supported URL Formats

- `youtube.com/watch?v=VIDEO_ID`
- `youtu.be/VIDEO_ID`
- `youtube.com/embed/VIDEO_ID`
- `youtube.com/v/VIDEO_ID`
- Bare video ID (11 characters)

## Analysis Modes

Select based on user request:

| User Says | Mode | Action |
|-----------|------|--------|
| "extract wisdom", "key insights" | Wisdom | See [analysis-modes.md](references/analysis-modes.md#wisdom) |
| "summarize", "TLDR", "overview" | Summary | See [analysis-modes.md](references/analysis-modes.md#summary) |
| "questions", "Q&A", "discussion" | Q&A | See [analysis-modes.md](references/analysis-modes.md#qa) |
| "quotes", "notable statements" | Quotes | Use `--with-segments`, see [analysis-modes.md](references/analysis-modes.md#quotes) |
| Other specific requests | Custom | Apply user's instructions directly |

## Error Handling

The script returns partial results when possible:

- **Transcripts disabled**: Returns metadata only, notes error
- **Private video**: Clear error message with video ID
- **No transcript found**: Returns metadata, suggests alternatives
- **Rate limiting**: Retry after 30-60 seconds

Check the `errors` array in output for any issues.

## Background Analysis (Subagent)

For video analysis that shouldn't block the main conversation, spawn a background subagent:

```
Task(
  subagent_type: "general-purpose",
  prompt: "Read ~/.claude/skills/youtube-content/SKILL.md and follow the workflow.
    Analyze this YouTube video: {url}
    Mode: {wisdom|summary|qa|quotes}
    Save to knowledge base: {yes|no}"
)
```

## Knowledge Persistence

Analyses and raw transcripts are automatically saved to a knowledge base for future reference.

### Configuration

Set `CLAUDE_KNOWLEDGE_DIR` to customize storage location (default: `~/.claude/knowledge`).

### Save Analysis

Saves both the analysis (markdown) and raw transcript (JSON):

```bash
echo '{"video_id": "...", "metadata": {...}, "transcript": {...}, "analysis": "..."}' | \
  uv run scripts/save_analysis.py --mode wisdom --tags "ai,coding"
```

Output: `{"saved": true, "analysis_path": "...", "transcript_path": "..."}`

### Search Knowledge

```bash
uv run scripts/search_knowledge.py --list          # List recent
uv run scripts/search_knowledge.py "react"         # Search keyword
uv run scripts/search_knowledge.py --tag ai        # Filter by tag
```

### File Structure

```
$CLAUDE_KNOWLEDGE_DIR/youtube/
├── .gitignore                  # Ignores transcripts/
├── index.md                    # Quick reference
├── analyses/
│   └── 2025-12-30_VIDEO_ID.md  # Formatted analysis with frontmatter
└── transcripts/                # Raw data (gitignored)
    └── 2025-12-30_VIDEO_ID.json # Full fetch output with transcript
```

**Note**: Raw transcripts are gitignored by default as they can be large and re-fetched from YouTube if needed.
