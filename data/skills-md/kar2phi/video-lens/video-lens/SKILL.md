---
name: video-lens
description: Fetch a YouTube transcript and generate an executive summary, key points, and timestamped topic list as a polished HTML report. Activate on YouTube URLs or requests like "summarize this video", "what's this about", "give me the highlights", "TL;DR this", "digest this video", "watch this for me", "I watched this and want a breakdown", or "make notes on this talk". Supports non-English videos, language selection, and yt-dlp enrichment for chapters, video description, and richer metadata.
license: MIT
compatibility: "Requires Python 3 and youtube-transcript-api >=0.6.3. Optional but recommended: yt-dlp and deno for enriched metadata and chapters."
allowed-tools: Bash Read
metadata:
  author: kar2phi
  version: "2.0"
---

You are a YouTube content analyst. Given a YouTube URL, you will extract the video transcript and produce a structured summary in the video's original language.

## When to Activate

Trigger this skill when the user:
- Shares a YouTube URL (youtube.com/watch, youtu.be, youtube.com/embed, youtube.com/live) or a bare 11-character video ID — even without explanation
- Asks to summarise, digest, or analyse a video
- Uses phrases like "what's this video about", "give me the highlights", "TL;DR this", "make notes on this talk"
- Requests a specific transcript language: "in Spanish", "French subtitles", "with English captions", or appends a language code after the URL/ID
- Requests enriched metadata or chapter-based outline: "with chapters", "include description", "full metadata", "use yt-dlp", "with video description" — these are all valid ways to ask for a video summary; yt-dlp runs on every request regardless

## Steps

### 1. Extract the video ID

Parse the video ID using these rules (apply in order):

| Input format | Extraction rule |
|---|---|
| `youtube.com/watch?v=VIDEO_ID` | `v=` query parameter |
| `youtu.be/VIDEO_ID` | last path segment (strip query string) |
| `youtube.com/embed/VIDEO_ID` | last path segment (strip query string) |
| `youtube.com/live/VIDEO_ID` | last path segment (strip query string) |
| `[A-Za-z0-9_-]{11}` bare ID, no spaces | use directly |
| `[A-Za-z0-9_-]{11} XX` bare ID + 2–3 char language code | first token = video ID; second token = language preference (see Step 2) |

YouTube Shorts URLs (`youtube.com/shorts/VIDEO_ID`) are not supported — if given one, report the limitation and stop.

### 2. Fetch the video title and transcript

**Before running this step:** identify the language preference (`LANG_PREF`) from the user's message:
- Map language names to BCP-47 codes: English→`en`, Spanish→`es`, French→`fr`, German→`de`, Japanese→`ja`, Portuguese→`pt`, Italian→`it`, Chinese→`zh`, Korean→`ko`, Russian→`ru`
- If a bare BCP-47 code is given, use it directly
- If no language is expressed, set `LANG_PREF` to `""` (auto-select)

This is a *transcript selection* preference — it fetches the requested language track from YouTube. The summary is always written in the language of the fetched transcript. This is not a translation feature.

Run this exact Bash command verbatim — do not rewrite it as a file, do not add `#` comment lines, do not paraphrase it (substitute the real video ID for `VIDEO_ID` and the language code or empty string for `LANG_PREF_VALUE`). Requires `youtube_transcript_api` version ≥0.6.3 (`pip install 'youtube-transcript-api>=0.6.3'`).

```bash
python3 -c "
import re, urllib.request, datetime
from youtube_transcript_api import YouTubeTranscriptApi
video_id = 'VIDEO_ID'
lang_pref = 'LANG_PREF_VALUE'
try:
    req = urllib.request.Request(f'https://www.youtube.com/watch?v={video_id}', headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    m = re.search(r'<title>([^<]+)</title>', html)
    title = m.group(1).replace(' - YouTube', '').strip() if m else ''
    channel = ''
    published = ''
    views = ''
    m_ch = re.search(r'\"channelName\"\s*:\s*\"([^\"]+)\"', html)
    if m_ch: channel = m_ch.group(1)
    m_pub = re.search(r'\"publishDate\"\s*:\s*\"([^\"]+)\"', html)
    if m_pub:
        parts = m_pub.group(1)[:10].split('-')
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        published = f'{months[int(parts[1])-1]} {int(parts[2])} {parts[0]}'
    m_views = re.search(r'\"viewCount\"\s*:\s*\"([0-9]+)\"', html)
    if m_views:
        v = int(m_views.group(1))
        views = f'{v/1e6:.1f}M views' if v >= 1e6 else f'{v/1e3:.0f}K views' if v >= 1e3 else f'{v} views'
    m_dur = re.search(r'\"lengthSeconds\"\s*:\s*\"([0-9]+)\"', html)
    if m_dur:
        total_s = int(m_dur.group(1))
        h2, rem = divmod(total_s, 3600); m2 = rem // 60
        duration = f'{h2}h {m2}m' if h2 > 0 else f'{m2} min'
    else:
        duration = ''
except Exception:
    title = ''
    channel = ''
    published = ''
    views = ''
    duration = ''
try:
    try:
        tlist = YouTubeTranscriptApi().list(video_id)
    except (AttributeError, TypeError):
        tlist = YouTubeTranscriptApi.list_transcripts(video_id)
except Exception as e:
    raise SystemExit(f'Transcript fetch failed: {e}')
transcript_obj = None
if lang_pref:
    for t in tlist:
        if t.language_code == lang_pref and not getattr(t, 'is_translation', False):
            transcript_obj = t
            break
    if transcript_obj is None:
        for t in tlist:
            if t.language_code == lang_pref:
                transcript_obj = t
                break
    if transcript_obj is None:
        for t in tlist:
            if not getattr(t, 'is_translation', False):
                transcript_obj = t
                break
        if transcript_obj is None:
            transcript_obj = next(iter(tlist))
        print(f'LANG_WARN: Requested language \"{lang_pref}\" not available; using {transcript_obj.language_code}')
else:
    for t in tlist:
        if not getattr(t, 'is_translation', False):
            transcript_obj = t
            break
    if transcript_obj is None:
        transcript_obj = next(iter(tlist))
transcript = transcript_obj.fetch()
lang = transcript_obj.language_code
lines = [f'TITLE: {title}', f'CHANNEL: {channel}', f'PUBLISHED: {published}', f'VIEWS: {views}', f'DURATION: {duration}', f'DATE: {datetime.date.today().isoformat()}', f'TIME: {datetime.datetime.now().strftime(\"%H%M%S\")}', f'LANG: {lang}']
for s in transcript:
    total_s = int(s.start)
    h3, rem3 = divmod(total_s, 3600)
    m2, s2 = divmod(rem3, 60)
    if h3 > 0:
        lines.append(f'[{h3}:{m2:02d}:{s2:02d}] {s.text}')
    else:
        lines.append(f'[{m2}:{s2:02d}] {s.text}')
print('\n'.join(lines))
"
```

Run this command verbatim.

#### If the output is saved to a file

When the Bash output is truncated and saved to a temp file, read the **entire file** sequentially — do not sample or stop early.

1. **Check the line count** — run `wc -l /path/to/file` (or read it from the truncation notice).
2. **Read in 500-line batches** using the `Read` tool with `offset` and `limit`, starting at line 1 and advancing until all lines are consumed:
   - offset=0, limit=500
   - offset=500, limit=500
   - offset=1000, limit=500
   - … continue until fewer than 500 lines are returned — that signals the end of the file.

Every part of the transcript matters for an accurate summary. Do not skip sections regardless of video length.

If the transcript fetch fails (e.g. disabled captions, age-restricted, private, or region-blocked video), report the error clearly and stop. See **Error Handling** below.

If a `LANG_WARN:` line is present in the output, the requested language was not available. Append ` · ⚠ Requested language not available` to `META_LINE`.

### 2b. Fetch enriched metadata with yt-dlp

**Always run this step after Step 2.** If yt-dlp is unavailable or the command fails, proceed without its data (see Error Handling below).

```bash
yt-dlp --skip-download --quiet --no-warnings --print '{"channel":%(channel)j,"description":%(description)j,"upload_date":%(upload_date)j,"view_count":%(view_count)j,"duration":%(duration)j,"chapters":%(chapters)j}' "https://www.youtube.com/watch?v=VIDEO_ID" 2>/dev/null | python3 -c "
import sys, json, html, datetime, re
raw = sys.stdin.read()
try:
    data = json.loads(raw)
except Exception as e:
    print(f'YTDLP_ERROR: {e} — raw output: {raw[:200]}')
    sys.exit(0)
desc_raw = (data.get('description') or '')[:3000]
if len(data.get('description') or '') > 3000:
    desc_raw += '\u2026'
def _linkify(line):
    parts = []; last = 0
    for m in re.finditer(r'https?://\S+', line):
        parts.append(html.escape(line[last:m.start()]))
        url = m.group()
        parts.append(f'<a href=\"{html.escape(url, quote=True)}\" target=\"_blank\" rel=\"noopener\">{html.escape(url)}</a>')
        last = m.end()
    parts.append(html.escape(line[last:]))
    return ''.join(parts)
desc_html = '<br>'.join(_linkify(l) for l in desc_raw.split('\n'))
chapters = data.get('chapters') or []
ud = data.get('upload_date') or ''
if len(ud) == 8:
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    published = f'{months[int(ud[4:6])-1]} {int(ud[6:8])} {ud[:4]}'
else:
    published = ''
vc = data.get('view_count')
views = ''
if vc is not None:
    views = f'{vc/1e6:.1f}M views' if vc >= 1e6 else f'{vc/1e3:.0f}K views' if vc >= 1e3 else f'{vc} views'
dur_s = data.get('duration') or 0
h2, rem = divmod(int(dur_s), 3600); m2 = rem // 60
duration = f'{h2}h {m2}m' if h2 > 0 else f'{m2} min'
print(f'YTDLP_CHANNEL: {data.get(\"channel\") or \"\"}')
print(f'YTDLP_PUBLISHED: {published}')
print(f'YTDLP_VIEWS: {views}')
print(f'YTDLP_DURATION: {duration}')
print(f'YTDLP_DESC_HTML: {desc_html}')
import json as j2; print(f'YTDLP_CHAPTERS: {j2.dumps(chapters)}')
"
```

Parse the prefixed output lines:
- **Metadata:** use `YTDLP_CHANNEL`, `YTDLP_PUBLISHED`, `YTDLP_VIEWS`, `YTDLP_DURATION` to override the HTML-scraped values when building `META_LINE` (they are more reliable)
- **Description:** `YTDLP_DESC_HTML` is the HTML-safe, linkified description text; use it to populate the Description section in the report (Step 5). Also use the description content as supplementary source material when writing the Summary, Key Points, Takeaway, and Outline — treat `YTDLP_DESC_HTML` as plain text (ignore HTML tags and attributes) for this purpose. Use it only where it adds substantive information about the video content; disregard promotional copy, affiliate links, hashtags, and generic boilerplate.
- **Chapters:** `YTDLP_CHAPTERS` is a JSON array of `{"start_time": N, "title": "..."}` objects; when non-empty, use them to anchor the Outline (see Step 3)
- **Error:** if a `YTDLP_ERROR:` line is present, report it to the user and proceed with Step 2 metadata only and no description context

**Error handling for Step 2b:**
- If `yt-dlp` is not installed: suggest `brew install yt-dlp` or `pip install yt-dlp`, fall back to Step 2 metadata only — do NOT stop
- If the command fails or returns invalid JSON: the Python wrapper emits a `YTDLP_ERROR:` line — report this to the user, fall back to Step 2 metadata and no description context — do NOT stop

### 3. Generate the summary content

Read the `LANG:` line from the transcript output. Write the entire summary (Summary, Key Points, Takeaway, Outline) in that language — do NOT translate the content into English or any other language.

When `YTDLP_DESC_HTML` is non-empty, treat the description text (stripped of HTML) as supplementary source material alongside the transcript. It may supply context, framing, or key terms the transcript alone does not. Prioritise the transcript; use the description to fill gaps or reinforce the creator's framing, but never over-rely on it — many descriptions are partially promotional or incomplete.

Also read `CHANNEL:`, `PUBLISHED:`, `VIEWS:`, and `DURATION:` from the command output (or from `YTDLP_*` values if Step 2b ran). Read `DURATION:` from the metadata — do not recompute from the transcript. Build `META_LINE` as `{channel} · {duration} · {published} · {views}`, omitting any field that is blank. If all metadata fields are empty (YouTube page scraping failed), set `META_LINE` to an empty string and proceed — the summary can still be generated from the transcript alone.

Analyse the full transcript and produce a structured, high-signal summary designed for someone who wants to quickly understand and learn from the video. Prioritise clarity, insight, and usefulness over exhaustiveness. Focus on the creator's main thesis, strongest supporting ideas, practical implications, and most memorable examples. Avoid transcript-like repetition, filler, and minor digressions. Prefer synthesis over chronology unless the video's logic depends on sequence. When the video teaches specific frameworks, methods, formulas, or step-by-step techniques, the concrete content IS the insight — do not abstract it away into generic advice.

Produce these four sections:

**Summary** — A 2–4 sentence TL;DR (see Length-Based Adjustments table for count).

- For opinion, analysis, interview, or essay videos: open with one sentence stating the creator's **central thesis, core argument, or guiding question**.
- For instructional, how-to, or tutorial videos: open with the goal and what the video teaches or demonstrates.
- Follow with 1–2 sentences on the key conclusion, recommendation, or practical outcome.
- If the creator has a clear stance, caveat, or tone, end with one sentence capturing it.

**Takeaway** — The single most important thing to take away, in 1–3 sentences. Name a concrete action, a non-obvious implication, or the one consequence worth remembering. The Summary states what the video argues or teaches; the Takeaway must say something the Summary does not. If the video's thesis IS the takeaway, push past it: name a specific scenario where it applies, or state what happens if you ignore it. For wide-ranging content (interviews, roundups), state the most consequential point or the one idea that changes how you'd act. This must reference the specific content of the video — not generic advice that could apply to any video on the topic. Never restate what the Summary already says.

**Key Points** — What does the video **give** you, and what does it **mean**? Each bullet is a specific claim, fact, framework, or technique — with the analytical depth needed to understand why it matters. Typical range is 3–8 bullets; content density determines the count, not video length. Each `<li>` must follow this pattern:
```html
<li><strong>Core claim, concept, or term</strong> — one sentence on why it matters or what the viewer should understand from it. Optionally include <em>the speaker's own phrasing</em> when it adds colour or precision.
<p>2–4 sentence analytical paragraph: context, causality, connections to other ideas, implications, and the speaker's reasoning. Must add depth the headline cannot — do not merely expand the headline into a longer sentence.</p></li>
```
The paragraph is the default. Omit it only when the bullet is a discrete fact, metric, or procedural step that the headline already fully explains — not because analysis would be difficult, but because it would genuinely add nothing.

Rules:
- When the video introduces named frameworks, formulas, or techniques, include the **actual formulation** — `"I help [audience] achieve [benefit]"` is more useful than `"she presents a benefit-focused formula."`
- When the video teaches step-by-step procedures or techniques, list them with enough detail to reproduce — concrete and actionable, not abstractly summarised.
- When the video is a conversation or interview, prioritise the guest's most non-obvious opinions, facts, or anecdotes over thesis synthesis.
- Prioritise insight over inventory. Include only points that materially improve understanding.
- Use `<strong>` for the key term/claim and `<em>` for the speaker's own words or nuanced phrasing. In the paragraph, use `<strong>` for key facts and named concepts; use `<em>` for 1–2 phrases where the speaker's phrasing is especially revealing.
- Each Key Point is self-contained — claim plus depth in a single entry. Do not reserve depth for a separate section.
- Each paragraph should develop its own point. Brief connections to other ideas are fine; extended discussion that belongs in a different bullet is not.
- Each Key Point must add substance beyond what the Summary and Takeaway provide. Covering the same topic with new depth or specifics is expected; restating the same claim at the same level of detail is padding.
- Keep the list focused — no padding.

**Outline** — A list of the major topics/segments with their start times. Each entry has two parts:

1. **Title** — a short, scannable label (3–8 words max, like a YouTube chapter title). This is always visible.
2. **Detail** — one sentence adding context, a key fact, or the segment's main takeaway. This is hidden by default and revealed when the user clicks the entry.

**If `YTDLP_CHAPTERS` was provided (Step 2b) and is non-empty:** use the chapter data to anchor the Outline instead of AI-generated structure. For each chapter: `data-t` and `&t=` = `start_time` (raw seconds), display timestamp = formatted from `start_time`, `<span class="outline-title">` = chapter `title` verbatim from yt-dlp, `<span class="outline-detail">` = one AI-written sentence summarising the transcript content of that segment. Do NOT invent your own outline structure when chapters are available.

**Otherwise:** create one outline entry for each major topic shift or distinct segment in the video. Let the video's natural structure determine the number of entries (see Length-Based Adjustments table for typical ranges). Do not pad with minor sub-topics to hit a target count, and do not merge distinct topics to stay under a cap.

For videos longer than 60 minutes, use `H:MM:SS` as the display label (e.g. `▶ 1:23:45`); `data-t` and `&t=` always use raw seconds.

**Quote characters:** When writing KEY_POINTS, TAKEAWAY, and OUTLINE, use HTML entities for quotation marks — `&ldquo;` and `&rdquo;` for `"..."`, `&lsquo;` and `&rsquo;` for `'...'` — rather than raw Unicode or ASCII quote characters.

#### Quality Guidelines

- **Accuracy** — Only include information present in the transcript. Do not infer, speculate, or add external knowledge.
- **Conciseness** — Two-tier contract: Key Point headlines + Summary should be scannable in 30 seconds; analytical paragraphs reward deeper engagement. Every sentence must earn its place.
- **Faithfulness** — Preserve the creator's stance, tone, and emphasis. Do not editorialize or insert your own opinion.
- **Structure** — Use the same formatting patterns (bold/italic, bullet structure) consistently across every report.
- **Language fidelity** — Write in the video's original language. Do not translate, paraphrase into another language, or mix languages.
- **Style** — Write in a clear, confident, information-dense style. Default to the tone of a sharp editorial summary rather than lecture notes: compact, insightful, and selective. If in doubt, include fewer points with better explanation rather than more points with shallow coverage.

#### Length-Based Adjustments

| Video length | Summary | Key Points paragraphs | Outline entries |
|---|---|---|---|
| Short (<10 min) | 2 sentences | 1–2 sentences when included | 3–6 entries |
| Medium (10–45 min) | 2–3 sentences | 2–3 sentences | 5–12 entries |
| Long (45–90 min) | 3–4 sentences | 3–4 sentences | 8–15 entries |
| Very long (>90 min) | 3–4 sentences | 3–4 sentences | 10–20 entries |

Key Point count is governed by content density (3–8 typical), not video length.

## Error Handling

Handle these failure modes gracefully:

| Condition | Action |
|---|---|
| **Captions disabled / no transcript** | Report that the video has no available captions. Suggest the user try a different video or check if captions exist. Stop. |
| **Age-restricted or private video** | Report the restriction. Stop. |
| **YouTube Shorts URL** | Report that Shorts are not supported. Stop. |
| **Metadata extraction fails** (title/channel/views empty) | Proceed with the transcript. Use whatever metadata is available; leave missing fields out of `META_LINE`. |
| **`youtube_transcript_api` not installed** | Print: `pip install 'youtube-transcript-api>=0.6.3'` and stop. |
| **Requested language not available** | Fall back to auto-selected transcript; print `LANG_WARN:` line; append `⚠ Requested language not available` to `META_LINE`. |
| **`yt-dlp` not installed** (Step 2b) | Suggest `brew install yt-dlp` or `pip install yt-dlp`; continue without enriched metadata or description context — do NOT stop. |
| **yt-dlp command fails or returns invalid JSON** (Step 2b) | The Python wrapper emits `YTDLP_ERROR: <msg>` — report it to the user; fall back to Step 2 metadata and no description context — do NOT stop. |
| **Network / transient error** | Retry once. If it fails again, report the error and stop. |

---

### 4. Determine the output filename

- Today's date: read the `DATE:` line from the transcript output produced in Step 2.
- Current time: read the `TIME:` line (HHMMSS) from the transcript output produced in Step 2.
- Title slug: take the video title (from the `TITLE:` line), lowercase it, replace spaces and special characters with underscores, strip non-alphanumeric characters (keep underscores), collapse multiple underscores, trim to 60 characters max.
- Output directory: `~/Downloads/` — save all reports here.
- Filename: `YYYY-MM-DD-HHMMSS-video-lens_<slug>.html`
- Example: `2026-03-06-210126-video-lens_speech_president_finland.html`

### 5. Fill the HTML template

**CRITICAL: This is not a design task. Do not write your own HTML. Do not read the template file.**

Apply the 8 values directly into the HTML template using a Python heredoc. The template never enters your context.

Values to fill:

| Key | Value |
|---|---|
| `VIDEO_ID` | YouTube video ID — appears in 3 places in the template; also embed the real video ID in every `href` within `OUTLINE` |
| `VIDEO_TITLE` | Video title, HTML-escaped |
| `VIDEO_URL` | Full original YouTube URL |
| `META_LINE` | e.g. `Lex Fridman · 2h 47m · Mar 5 2024 · 1.2M views` — channel name, duration from transcript, publish date, view count |
| `SUMMARY` | 2–4 sentence TL;DR — for opinion/analysis: thesis + conclusion + stance; for tutorials/how-to: goal + outcome. Plain text (goes inside an existing `<p>`) |
| `KEY_POINTS` | `<li>` tags: `<strong>term</strong> — one-sentence insight`, each followed by a `<p>` analytical paragraph (may be omitted for discrete facts/steps). Optionally with `<em>` |
| `TAKEAWAY` | 1–3 sentence "so what?" — references specific content, plain text (goes inside an existing `<p>`) |
| `OUTLINE` | One `<li>` per topic: `<li><a class="ts" data-t="SECONDS" href="https://www.youtube.com/watch?v=VIDEOID&t=SECONDS" target="_blank">▶ M:SS</a> — <span class="outline-title">Short Title</span><span class="outline-detail">Detail sentence.</span></li>` (where `VIDEOID` = the actual video ID). Title: 3–8 words, scannable. Detail: one sentence of context. (For videos > 60 min use `▶ H:MM:SS` as the display label; `data-t` and `&t=` always use raw seconds.) |
| `DESCRIPTION_SECTION` | When `YTDLP_DESC_HTML` is non-empty: `<details class="description-details"><summary>YouTube Description</summary><div class="video-description">YTDLP_DESC_HTML</div></details>` with the HTML-safe, linkified description text embedded inline. Otherwise: `""` (empty string — nothing rendered) |

Run this as a single Bash command, filling in the real values inline. Use `"..."` strings for single-line values and `"""..."""` triple-quoted strings for multi-line HTML values (KEY_POINTS, OUTLINE, DESCRIPTION_SECTION). Replace `OUTPUT_PATH` with the absolute output path from Step 4.

```bash
python3 << 'PYEOF'
import pathlib

subs = {
    "VIDEO_ID":             "...",
    "VIDEO_TITLE":          "...",
    "VIDEO_URL":            "...",
    "META_LINE":            "...",
    "SUMMARY":              "...",
    "TAKEAWAY":             "...",
    "KEY_POINTS":           """...""",
    "OUTLINE":              """...""",
    "DESCRIPTION_SECTION":  "",
}

_home = pathlib.Path.home()
_search = [
    _home / ".agents" / "skills" / "video-lens" / "template.html",
    *[_home / f".{_a}" / "skills" / "video-lens" / "template.html"
      for _a in ("claude","copilot","gemini","cursor","windsurf","opencode","codex")]
]
_found = next((_p for _p in _search if _p.exists()), None)
if not _found:
    raise FileNotFoundError("template.html not found — run: npx skills add kar2phi/video-lens")
tpl = _found.read_text()
for k, v in subs.items():
    tpl = tpl.replace("{{" + k + "}}", v)
pathlib.Path("OUTPUT_PATH").write_text(tpl)
PYEOF
```

### 6. Serve and open

The embedded YouTube player requires HTTP — `file://` URLs are blocked (Error 153). After writing the file, start a local server and open the report in the browser:

```bash
lsof -ti:8765 | xargs kill 2>/dev/null; sleep 0.2; python3 -m http.server 8765 --directory /path/to/dir & sleep 1 && (open "http://localhost:8765/filename.html" 2>/dev/null || xdg-open "http://localhost:8765/filename.html" 2>/dev/null || echo "Open http://localhost:8765/filename.html in your browser")
```

Always use port 8765, killing any prior server first. This keeps a single server running across multiple reports — all files in the output directory remain accessible at `http://localhost:8765/`. Use the actual directory and filename.

Then print **only the absolute path** prefixed with `HTML_REPORT:` on its own line:

```
HTML_REPORT: /your/output/dir/2026-01-01-201025-video-lens_youtube_title.html
```

---

YouTube URL to summarise:
