---
name: media-summary
description: Downloads and summarizes audio/video media — podcasts, YouTube videos, talks, interviews, lectures, and conference presentations. Saves a structured markdown summary locally, publishes it as a public GitHub Gist, and opens it in the system default application. Use when the user provides a URL to any audio or video content (Apple Podcasts, Spotify, YouTube, conference recordings, etc).
license: MIT
compatibility: Requires yt-dlp, Python 3, and gh CLI (authenticated)
metadata:
  author: cristoslc
argument-hint: <media-url>
user-invocable: true
allowed-tools: Bash, Write, Read, WebFetch, Agent
---

The user has provided a media URL: $ARGUMENTS

Follow these steps exactly:

## Step 1 — Resolve a YouTube URL

If the URL is already a YouTube URL (`youtube.com` or `youtu.be`), use it directly.

Otherwise (Apple Podcasts, Spotify, conference sites, etc.), extract the title from the page, then search YouTube for the matching video/episode. Use `mcp__MCP_DOCKER__fetch_content` or `mcp__MCP_DOCKER__brave_web_search` to find it.

## Step 2 — Download the transcript with yt-dlp

Run:

```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format vtt -o "/tmp/media_transcript" "<YOUTUBE_URL>"
```

This produces `/tmp/media_transcript.en.vtt`. (The raw transcript stays in `/tmp/` — only the final summary goes to `~/Downloads/`.)

## Step 3 — Parse the VTT into clean timestamped lines

Run this Python script. It deduplicates overlapping caption windows using word-overlap detection and preserves timestamps so they can be used as deep-links in the summary:

```bash
python3 - << 'EOF'
import re

with open('/tmp/media_transcript.en.vtt', 'r') as f:
    content = f.read()

# Parse all cue blocks
cues = []
for block in re.split(r'\n\n+', content):
    lines = [l.strip() for l in block.split('\n') if l.strip()]
    timestamp_line = None
    text_lines = []
    for line in lines:
        if '-->' in line:
            m = re.match(r'(\d{2}:\d{2}:\d{2})', line)
            if m:
                timestamp_line = m.group(1)
        elif not re.match(r'^\d+$', line) and not line.startswith('WEBVTT') \
             and not line.startswith('Kind:') and not line.startswith('Language:'):
            clean = re.sub(r'<[^>]+>', '', line).strip()
            if clean:
                text_lines.append(clean)
    if timestamp_line and text_lines:
        cues.append((timestamp_line, ' '.join(text_lines)))

# Emit only new words per cue, preserving the timestamp of first appearance
result_lines = []
emitted_words = []

for timestamp, text in cues:
    words = text.split()
    overlap = 0
    for i in range(min(len(words), len(emitted_words)), 0, -1):
        if words[:i] == emitted_words[-i:]:
            overlap = i
            break
    new_words = words[overlap:]
    if new_words:
        result_lines.append(f'[{timestamp}] {" ".join(new_words)}')
        emitted_words.extend(new_words)

with open('/tmp/media_clean_transcript.txt', 'w') as f:
    f.write('\n'.join(result_lines))
print(f"Saved {len(result_lines)} lines")
EOF
```

Output format — one line per segment:
```
[00:00:00] I'm doing something absolutely insane right now.
[00:00:04] Artificial intelligence is a little bit perplexing
```

## Step 4 — Read the transcript in chunks, then generate the summary

### 4a — Check size and read in batches

First check how many lines the transcript has:

```bash
wc -l /tmp/media_clean_transcript.txt
```

Then use the **Read tool** (not Bash) to read the file in batches of **400 lines** using `offset` and `limit`. For a 1000-line file, make three Read calls: offset=1/limit=400, offset=401/limit=400, offset=801/limit=400. Read all batches before writing anything.

### 4b — Write the summary

After reading all batches, write a comprehensive, well-structured markdown summary covering:

- **Speaker/guest background** and why they were invited or why this talk matters
- **Core thesis / main argument**
- **All major topics discussed** with concrete details, examples, frameworks, and notable quotes
- **Key takeaways and actionable insights**
- **Books, tools, or resources mentioned**
- **One-sentence bottom line**

Use `##` section headers, bullet points, and bold text for scannability. Aim for 800–1200 words of substance.

**Timestamps:** For each major topic or section in the summary, include a YouTube deep-link using the timestamp from the transcript. Convert `[HH:MM:SS]` to total seconds for the `?t=` parameter (e.g. `[01:05:30]` → 3930 seconds). Format as a linked timestamp at the start of the relevant bullet or subheading:

```markdown
### [[01:05:30]](https://youtu.be/VIDEO_ID?t=3930) Power Concentration
```

or inline for bullets:

```markdown
- **[[00:14:00]](https://youtu.be/VIDEO_ID?t=840) Epistemic collapse** — We are entering...
```

Use the YouTube URL from Step 1 as the base. Include timestamps for every major topic/section — aim for one timestamp per significant topic shift.

## Step 5 — Write the markdown file

Determine a clean, slug-style filename from the title, e.g. `jenny-wen-design-process`. Save the summary to:

```
~/Downloads/<slug>_summary.md
```

Follow the template at `references/media-summary-template.md.j2` (relative to this skill's directory). Key points:

- The metadata fields (Guest, Hosts, Podcast, Published) **must be a bullet list**, not bare lines — bare consecutive lines collapse into a single paragraph in CommonMark.
- **No horizontal rules (`---`) between sections.** Use only one, directly before the italicised source attribution at the bottom.
- Key Takeaways is the first section, before Guest Background.
- `gist_url` starts as `(to be filled after publishing)` and is updated in Step 6.
- The source link at the bottom **prefers YouTube or PocketCasts over Apple Podcasts**. If you already have a YouTube URL from Step 1, use that. Otherwise check for a PocketCasts link (`pca.st` or `pocketcasts.com`). Fall back to the original URL only if neither is available.

## Step 6 — Publish as a public GitHub Gist

Create a public GitHub Gist with the summary content. The gist filename must be prefixed with `summary-`, e.g. `summary-jenny-wen-design-process.md`.

Use the `gh` CLI:

```bash
gh gist create --public --filename "summary-<slug>.md" --desc "<Title> — Media Summary" ~/Downloads/<slug>_summary.md
```

Once you have the Gist URL, update the `gist_url` field in the frontmatter of `~/Downloads/<slug>_summary.md`, then run:

```bash
gh gist edit <gist-id> ~/Downloads/<slug>_summary.md
```

so the published Gist also contains the self-referencing URL.

Print the resulting Gist URL to the user.

## Step 7 — Open the file

```bash
open ~/Downloads/<slug>_summary.md 2>/dev/null || xdg-open ~/Downloads/<slug>_summary.md 2>/dev/null || true
```

## Final output to user

Tell the user:
- The local file path
- The public Gist URL
- A one-paragraph teaser of what the content is about
