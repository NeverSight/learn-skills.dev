---
name: mk-youtube-transcript-summarize
description: Summarize YouTube video content with structured output. Use when user wants a detailed summary from a transcript file path.
license: MIT
metadata:
  version: 2.1.0
  author: kouko
  tags:
    - youtube
    - summary
    - transcript
compatibility:
  claude-code: ">=1.0.0"
---

# YouTube Video Summary

Generate a structured, high-quality summary of a YouTube video from its transcript.

## Quick Start

```
/mk-youtube-transcript-summarize <transcript_file_path> [--force]
/mk-youtube-transcript-summarize --check <URL_or_video_id>
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| transcript_file_path | Yes* | - | Path to transcript file (.txt). *Not needed with `--check`. |
| --force | No | false | Force re-generate summary even if cached file exists |
| --check | No | false | Check if summary exists for a URL or video_id (no transcript file needed) |

## Examples

- `/mk-youtube-transcript-summarize /path/to/captions/20091025__dQw4w9WgXcQ.en.txt`
- `/mk-youtube-transcript-summarize /path/to/transcribe/20091025__dQw4w9WgXcQ.txt`

**Typical workflow:**

```
/mk-youtube-get-caption https://youtube.com/watch?v=xxx
→ outputs transcript file path

/mk-youtube-transcript-summarize /path/to/captions/20091025__VIDEO_ID.en.txt
→ generates structured summary saved to {baseDir}/data/20091025__VIDEO_ID.en.md
```

## Check Mode

Check if a cached summary exists without requiring a transcript file:

```
/mk-youtube-transcript-summarize --check <URL_or_video_id>
```

### Check Mode Examples

- `/mk-youtube-transcript-summarize --check https://youtube.com/watch?v=dQw4w9WgXcQ`
- `/mk-youtube-transcript-summarize --check dQw4w9WgXcQ`

### Check Mode Output

**Summary exists:**
```json
{
  "status": "success",
  "exists": true,
  "output_summary": "{baseDir}/data/20091025__dQw4w9WgXcQ.en.md",
  "summary_char_count": 5000,
  "summary_line_count": 120,
  "video_id": "dQw4w9WgXcQ",
  "title": "Video Title",
  "channel": "Channel Name",
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Summary does not exist:**
```json
{
  "status": "success",
  "exists": false,
  "video_id": "dQw4w9WgXcQ",
  "title": "",
  "channel": "",
  "url": ""
}
```

When `exists: true`, read the summary file at `output_summary` and display its COMPLETE content (Full Display Rule applies).

## How it Works

1. Execute: `{baseDir}/scripts/summary.sh "<transcript_file_path>"` (normal mode)
   OR: `{baseDir}/scripts/summary.sh --check "<URL_or_video_id>"` (check mode)
2. Parse JSON output to get `source_transcript`, `output_summary`, `char_count`, and `strategy`
3. Follow the **Processing Strategy** indicated by `strategy` field
4. Generate a structured summary following the **Summary Generation Rules**
5. **Save to `{baseDir}/data/<basename>.md`** using Write tool (use `output_summary` path from JSON)
6. **Display the FULL summary content** to the user exactly as written to the file — do NOT abbreviate, condense, or re-summarize
7. Include file path in response footer

### Processing Strategy

The `strategy` field from `summary.sh` determines how to handle the transcript:

#### Strategy: `standard` (< 80,000 chars, ~2 hr EN)

- Read the entire file with the Read tool
- Directly apply Summary Generation Rules

#### Strategy: `sectioned` (80,000–200,000 chars, ~2 hr – 5 hr EN)

Use a structured multi-phase approach within the main conversation to counter lost-in-middle effects:

1. **Read** the entire file with the Read tool
2. **Phase 1 — Segment identification**: Identify 5-10 major section boundaries (topic shifts, speaker changes, chapter markers) and list them
3. **Phase 2 — Section-by-section extraction**: For each identified section, extract key points, data, quotes, and arguments
4. **Phase 2.5 — Topic grouping** (if > 6 sections identified):
   - Group related sections into 4-6 macro-topics (e.g., "Background & Context", "Core Argument", "Evidence & Examples", "Implications")
   - Under each macro-topic, aggregate the key points from its constituent sections
   - This reduces synthesis pressure in Phase 3 by providing pre-organized intermediate structure
5. **Phase 3 — Synthesis**: Compose the final structured summary from the macro-topics (or directly from sections if ≤ 6), ensuring every identified section is represented
6. **Cross-check**: Verify that mid-content sections are not underrepresented compared to the beginning and end

#### Strategy: `chunked` (> 200,000 chars, > 5 hr EN)

Use parallel subagents to process chunks independently, keeping the main conversation context clean:

1. Calculate chunk count: `ceil(line_count / 1000)` — each chunk is ~1000 lines
2. **Spawn parallel subagents** using the Task tool (`subagent_type: "general-purpose"`):
   - Each subagent receives: the file path, start line offset, end line limit, and summarization instructions
   - **Chunk overlap**: Each chunk includes a 50-line overlap with the previous chunk for context continuity (chunk 1: lines 1–1000, chunk 2: lines 951–2000, chunk 3: lines 1951–3000, etc.). The first chunk has no leading overlap.
   - Each subagent prompt:
     ```
     Read the file at {file_path} from line {start_offset} to line {end_limit} using the Read tool (with offset and limit parameters).
     Then produce a summary of this section with 5-10 bullet points covering:
     - Main topics and arguments discussed
     - Key data points (numbers, dates, names) in plain text
     - Use sub-bullets for supporting details under a main point (max 2 levels)
     - Notable quotes as blockquotes
     Write the summary in the same language as the transcript (this will be synthesized into the user's language in the final step).
     IMPORTANT — Boundary continuity: If the beginning of your chunk clearly continues a topic from a previous section, prefix your first bullet with [continues from previous]. If the end of your chunk is mid-topic and clearly continues into the next section, suffix your last bullet with [continues to next]. This helps the synthesis step merge cross-chunk topics.
     ```
   - Use `model: "haiku"` for cost efficiency
3. **Collect** all subagent section summaries
4. **Synthesize** a final structured summary in the main conversation following the Summary Generation Rules
   - During synthesis, check for `[continues from previous]` and `[continues to next]` markers across adjacent chunks — merge bullets that belong to the same topic into a single coherent section rather than repeating them

#### Fallback Rules

- **Missing or unknown strategy**: If the `strategy` field is missing, empty, or contains an unrecognized value, default to the `standard` strategy
- **Chunked subagent retry**: If a subagent in `chunked` mode returns an empty result or clearly irrelevant content (e.g., error messages instead of summary bullets), retry that specific chunk once before proceeding with synthesis

## Summary Generation Rules

After obtaining the transcript, generate the summary using EXACTLY this structure and rules:

### Output Structure

```markdown
## Video Info (optional)

| Field | Value |
|-------|-------|
| **Title** | {title} |
| **Channel** | {channel} |
| **Duration** | {duration_string} |
| **Views** | {view_count, formatted with commas} |
| **Upload Date** | {upload_date, formatted as YYYY-MM-DD} |
| **Subtitle** | {subtitle_type} ({transcript_language}) |
| **URL** | {url} |

## Content Summary

#### {Section Title 1}

- Main point expressed concisely
  - Supporting detail or data point
- Another independent point
- ...

#### {Section Title 2}

- ...

(Continue for all logical sections)

## Key Takeaways

- 5-8 most important conclusions or insights from the video
```

### Video Info Table

- **Include** the Video Info table if `/mk-youtube-get-info` results are available in the current conversation context
- **Omit** the table if no metadata is available (proceed directly to Content Summary)

### Content Rules

1. **Section structure**: Divide the summary into logical sections using H4 (`####`) headings
   - If the video description contains chapter timestamps, use those as the section skeleton
   - Otherwise, identify 5-10 logical topic shifts in the transcript
   - Each section should have 3-7 bullet points
   - Prefer more sections with focused content over fewer sections with broad content

   Bullet formatting:
   - Each bullet should express one main point concisely (target: under 60 characters for CJK, under 120 characters for English)
   - When a bullet has 2+ supporting details (data, examples, sub-arguments), use second-level sub-bullets
   - NEVER nest beyond 2 levels (no sub-sub-bullets)
   - When details are independent facts without a shared parent topic, keep them as separate top-level bullets

   Ordering:
   - Arrange sections in the order topics appear in the video (chronological/narrative flow)
   - Within each section, list bullets in the order they were discussed in the transcript (source order)
   - Do NOT reorder bullets by perceived importance — preserve the speaker's narrative progression

2. **Data preservation**: Always preserve specific data points in plain text
   - Percentages, dollar amounts, dates, statistics — include as-is, no formatting
   - Person names, company names, product names — include as-is, no formatting
   - Direct quotes that are impactful → use blockquote format
   - Do NOT use inline bold (`**text**`) anywhere in the summary body (Content Summary and Key Takeaways sections)

3. **Language**: Write the summary in the user's conversation language
   - Detect the language the user is using in the current conversation
   - Write the entire summary (section titles, bullet points, key takeaways) in that language
   - Example: If user speaks Traditional Chinese, summarize in 繁體中文 regardless of transcript language

4. **Length**: Target compression ratio based on processing strategy:

   | Strategy | Compression | Guideline |
   |----------|-------------|-----------|
   | `standard` | 20-30% | Short content, detailed coverage |
   | `sectioned` | 15-20% | Medium-long content, balanced density |
   | `chunked` | 10-15% | Very long content, high-level synthesis |

5. **Tone**: Maintain an informative, neutral tone
   - Present the speaker's arguments faithfully
   - Do not add opinions or editorial commentary
   - Use active voice

6. **Key Takeaways**: End with 5-8 bullet points summarizing the most important insights
   - These should be standalone — understandable without reading the full summary
   - Prioritize actionable insights and surprising findings
   - Order by importance/impact (most significant insight first, descending)

## Save Summary to File

After generating the summary, save it to the **skill-local `data/` directory** using the Write tool:

- **Output path**: Use `output_summary` from the script JSON output (points to `{baseDir}/data/<basename>.md`)
- **Filename**: `<transcript_basename>.md` (preserves unified naming format)

**Example:**
- Input: `.../20091025__dQw4w9WgXcQ.en.txt`
- Output: `{baseDir}/data/20091025__dQw4w9WgXcQ.en.md`

**CRITICAL — Full Display Rule**: After saving the summary file, you MUST display the COMPLETE summary content to the user in your response. Output the full markdown content exactly as written to the file. Do NOT:
- Re-summarize or condense the summary
- Show only selected sections
- Create an abbreviated version
- Paraphrase or rewrite any part

The user expects to see the full summary directly in the conversation without needing to open the file.

End your response with the file path:
```
---
Summary saved to: `{output_summary path from JSON}`
```

## Output Format

### Normal Mode Output

```json
{
  "status": "success",
  "source_transcript": "/path/to/20091025__VIDEO_ID.en.txt",
  "output_summary": "{baseDir}/data/20091025__VIDEO_ID.en.md",
  "char_count": 30000,
  "line_count": 450,
  "strategy": "standard",
  "cached": false,
  "video_id": "dQw4w9WgXcQ",
  "title": "Video Title",
  "channel": "Channel Name",
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Cache hit** (returns existing summary):
```json
{
  "status": "success",
  "source_transcript": "/path/to/20091025__VIDEO_ID.en.txt",
  "output_summary": "{baseDir}/data/20091025__VIDEO_ID.en.md",
  "cached": true,
  "summary_char_count": 5000,
  "summary_line_count": 120,
  "video_id": "dQw4w9WgXcQ",
  "title": "Video Title",
  "channel": "Channel Name",
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

When `cached: true`, the summary file already exists — read and display it directly without regenerating.

### Check Mode Output

See [Check Mode](#check-mode) section above.

The script automatically extracts video metadata from the centralized metadata store if available.

## Notes

- **File caching**: If summary already exists for this video, it will be reused (returns `cached: true`)
- **Check mode**: Use `--check` to check if a cached summary exists without a transcript file
- **Force refresh**: Use `--force` flag to re-generate summary even if cached file exists
- This skill does NOT download videos or subtitles — use `/mk-youtube-get-caption` first to obtain a transcript file
- Uses system jq if available, otherwise auto-downloads on first run
- For best results, combine with `/mk-youtube-get-info` to include the Video Info table in the summary
- Summary is saved to the skill-local `data/` directory
