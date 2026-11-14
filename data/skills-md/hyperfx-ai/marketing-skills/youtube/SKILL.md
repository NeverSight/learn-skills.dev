---
name: youtube
description: Work with YouTube content end to end — fetch transcripts and turn them into summaries, blog posts, social content, quotes, or show notes; create high-CTR thumbnails (with the user's face from an upload), clone the style of top-ranking thumbnails; and produce SEO-optimised titles + descriptions. Use when the user pastes a YouTube URL, wants to repurpose video content, research competitor videos, make or refresh a thumbnail, or package a video for upload.
use_cases:
  - Get the transcript of a YouTube video
  - Summarize a YouTube video or extract key points without watching
  - Turn a video into a blog post, LinkedIn post, or show notes
  - Pull verbatim quotes with timestamps
  - Generate a YouTube thumbnail from a video idea, transcript, or YouTube URL
  - Research the top-performing thumbnails for a search term and clone their style
  - Add the user's face (uploaded as an image) to a thumbnail
  - Produce an SEO-optimised title set and description for an upcoming video
triggers:
  - youtube
  - youtube transcript
  - youtube video
  - video summary
  - repurpose video
  - show notes
  - thumbnail
  - youtube thumbnail
  - thumbnail clone
  - SEO titles
  - video description
  - youtube title
requires_toolkits:
  - youtube_toolkit
suggested_toolkits:
  - image_gen
  - sandbox
  - file_manager
icon: youtube
short_description: Fetch transcripts, repurpose video content, and create thumbnails for YouTube.
---

# YouTube

Fetch the full transcript of any YouTube video and turn it into whatever the user needs — summaries, blog posts, social content, quotes, show notes, or raw text. Then package videos for upload: high-CTR thumbnails, SEO titles, and descriptions.

## Routing

| User intent | Where to go |
| --- | --- |
| Transcript, summary, repurposing, quotes, chapters | This guide (below) |
| Thumbnails, style cloning, SEO titles/descriptions | `references/thumbnails.md` |

## Requirements

- **Hyper MCP installed.** [https://app.hyperfx.ai/mcp](https://app.hyperfx.ai/mcp)
- **Sandbox text workflows:** require `ai_functions_run` in the connected catalog and the sandbox toolkit. These scripts run inline LLM calls through the sandbox tool bridge.
- **YouTube toolkit enabled** at [https://app.hyperfx.ai/apps](https://app.hyperfx.ai/apps) — provides `youtube_video_transcripts_fetch` and `youtube_videos_read`.
- Thumbnail workflows additionally need the image generation and sandbox toolkits.

If `youtube_video_transcripts_fetch` is not found, the toolkit to enable is YouTube (`youtube_toolkit`).

### How to run the tools in this skill

Every tool in this skill is named by its canonical tool name. Run it with the call your surface gives you:

| Surface | Find a tool | Run it |
| --- | --- | --- |
| Hyper chat | Call the tool by its name; `search_tools(queries=["<provider> <action>"])` shows its parameters | `<name>(...)` |
| MCP client (Claude, Cursor, Codex, ChatGPT) | `search("<what you want to do>")`, then `describe("<name>")` | `call_read("<name>", {...})`, `call_write` or `call_destructive`: the one that `describe` names in `call_with` |
| Hyper CLI | `hyperai search "<what you want to do>"`, then `hyperai describe <name>` | `hyperai call <name> --json '{...}'` |

If a tool is not found: in Hyper chat, find its toolkit id with `discover_toolkits` and pass it to `enable_toolkit`. On an MCP client or the CLI, tell the user which integration to connect in Hyper.

## Two tools — pick the right one

| Tool | When to use | Returns |
| --- | --- | --- |
| `youtube_video_transcripts_fetch` | You need the raw transcript text or timestamped segments. Fast, reliable, always get this first. | Full text string + segments with start/duration timestamps |
| `youtube_videos_read` | You need AI-powered extraction from the video — summaries, Q&A, topic segmentation, translation, visual descriptions. | Free-form answer to your instruction |

**Default: start with `youtube_video_transcripts_fetch`.** Use `youtube_videos_read` when you need something the raw text can't give you (e.g. visual descriptions, translation, or a structured extraction from a very long video).

## Critical rules

1. **`youtube_video_transcripts_fetch` takes 15–30 seconds.** It spins up an isolated sandbox. Tell the user it's running and to expect a short wait — don't make them think it's stuck.
2. **Both video IDs and full URLs are accepted.** `"NZLAdOL9fP8"` and `"https://www.youtube.com/watch?v=NZLAdOL9fP8"` both work.
3. **Don't fabricate transcript content.** Always fetch before summarizing. Never rely on training knowledge about what a specific video says.
4. **Very long videos (>2 hours):** `youtube_video_transcripts_fetch` handles these fine. Only use `youtube_videos_read` on long videos if you specifically need AI-powered extraction — it can hit token limits on very long content.
5. **No transcript available:** Some videos have transcripts disabled. If `youtube_video_transcripts_fetch` fails, try `youtube_videos_read` as a fallback — it uses a different extraction method.

## Fetching the transcript

```python
youtube_video_transcripts_fetch(
    video_id_or_url="https://www.youtube.com/watch?v=NZLAdOL9fP8",
    language="en"   # optional — omit to auto-detect
)
```

**Response structure:**

```json
{
  "success": true,
  "video_id": "NZLAdOL9fP8",
  "language": "English (auto-generated)",
  "text": "Full transcript as one string...",
  "segments": [
    { "text": "This week we launched Hyper MCP.", "start": 0.0, "duration": 3.2 },
    { "text": "It brings Hyper's built-in tools...", "start": 3.2, "duration": 4.1 }
  ],
  "total_duration": 342.0
}
```

Use `text` for most tasks. Use `segments` when you need timestamps (e.g. chapters, clip references, karaoke captions).

## Using youtube_videos_read for AI-powered extraction

```python
youtube_videos_read(
    url="https://www.youtube.com/watch?v=NZLAdOL9fP8",
    instruction="Summarize the key points. Then list the main features demonstrated, with timestamps."
)
```

Good `instruction` examples:
- `"Extract every claim made about pricing or cost."`
- `"List the action items mentioned, in order."`
- `"Translate this to Spanish."`
- `"What tools or products does the speaker mention by name?"`
- `"Identify the main sections of this video and give me a timestamp for each."`

## What to do with the transcript

Once you have the text, ask the user what they need — or infer it from context:

| What the user wants | What to produce |
| --- | --- |
| Blog post | Restructure the transcript into intro → sections → CTA. Clean up filler words. Add subheadings. |
| LinkedIn / Twitter post | Extract the 1–2 sharpest insights. Rewrite in first person if it's the user's own video. |
| Summary | 3–5 bullet points of key takeaways. |
| Show notes / description | Title, 2-sentence summary, timestamped chapters, links mentioned. |
| Quote extraction | Pull verbatim quotes with `start` timestamps from the segments array. |
| Repurpose for email | Rewrite as a narrative email — opening hook, key insight, CTA. |
| Research / competitive analysis | Summarize what the speaker claims, what products they recommend, and what pain points they describe. |

## Thumbnails and SEO packaging

For making or refreshing thumbnails, cloning the style of top-ranking thumbnails, adding the user's face, and generating SEO titles/descriptions, read `references/thumbnails.md`. Every thumbnail workflow is a sandbox script under `scripts/` (`generate_thumbnail.py`, `research_top_thumbnails.py`, `clone_top_thumbnail_style.py`) — the reference doc is the routing table and the rules for using them.

## Example outputs

**Input:** `"Get the transcript of https://www.youtube.com/watch?v=NZLAdOL9fP8 and write a LinkedIn post from it"`

**Flow:**
1. Call `youtube_video_transcripts_fetch(video_id_or_url="https://www.youtube.com/watch?v=NZLAdOL9fP8")`
2. Read the returned `text`
3. Identify the 1–2 sharpest moments — what's surprising, useful, or quotable
4. Draft a LinkedIn post in the speaker's voice (first person) with a hook and a clear point

**Input:** `"Summarize this video for me: [URL]"`

**Flow:**
1. Call `youtube_video_transcripts_fetch(video_id_or_url="[URL]")`
2. Return 4–6 bullet points of key takeaways, without padding or filler

**Input:** `"Make me a thumbnail like the top videos for 'AI agents'"`

**Flow:**
1. Read `references/thumbnails.md`
2. Run `scripts/clone_top_thumbnail_style.py` with `query="AI agents"` and the user's topic
3. Show the top thumbnails, let the user pick a rank, re-run with `chosen_rank` to generate

## Related skills

| When to hand off | Skill |
| --- | --- |
| Mining comments from YouTube videos for customer research | [`customer-research`](../customer-research) |
| Finding top YouTube videos by topic | Use `youtube_videos_search_top` directly |
| Generating video content | [`video-generation`](../video-generation) |

For title options, descriptions and thumbnail concepts, run `generate_seo_titles.py`, `generate_seo_description.py` and `analyze_thumbnail_concepts.py` under `scripts/`. They call `ai_functions_run` from the sandbox using fetched transcript and video context. Follow the output contracts in `references/packaging-schemas.json`; the thumbnail reference explains the workflow.
