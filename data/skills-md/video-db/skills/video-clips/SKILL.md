---
name: video-clips
description: Cut clips and highlights from a video. Use when the user wants a clip of a time range, a highlight reel of the moments that match a prompt ("every product demo", "the goals in this match"), a supercut across several videos, a vertical or square cut for Shorts, Reels or TikTok, a thumbnail, or an MP4 to download. One moment found by what was said is video-search, which also cuts that clip; joining whole videos with transitions is video-edit. Works on YouTube links, public URLs and the user's VideoDB videos.
---

# Clips, highlights and social cuts

## Which path

1. **VideoDB connector tools present** (names such as `generate_clip`, `create_highlight_clip`, `compile_clips`, `reframe_video`, `upload_media`): use them. This is the path in Claude chat on web, desktop and mobile, and in Cowork. Do not install anything and do not ask for an API key.
2. **No VideoDB tools, but you have a shell** (Claude Code, Cowork, any agent that can run Python): ask for the VideoDB API key in one friendly line (free at https://console.videodb.io, $20 of credits, no card). When the user gives it, in chat or any other way, save it yourself to the project's `.env` as `VIDEO_DB_API_KEY`, never print it, and continue with the Python SDK path at the end of this file. In Claude Code, `/mcp` then authorizing videodb also works.
3. **No VideoDB tools and no shell**: you are in Claude chat. Reply with only this, adapted to the request: "VideoDB isn't connected yet. Open Settings → Connectors, find VideoDB, click Connect and log in (free, no card). Then send this request again and I'll take it from there." Do not mention API keys, `.env`, shells, Claude Code or `/mcp` here; none of them apply in chat, and a key pasted into chat cannot be used because nothing runs code there.

Talking to the user: never write "index", "indexed" or "indexing" in a reply. Say "searchable" ("it is now searchable by what was said and what is shown"), and "transcribe" rather than naming a job. One line of status at a time, then the result.

Every cut is a long job: the call returns `status: processing`. The reply carries an `output_url` and names the tool to poll (`poll_with`, or `retry_with` on older servers). Call that tool with the `output_url` until it is `done`; several `processing` replies in a row are normal (a 10-minute YouTube upload takes about five), and a `done` reply with an empty result means poll once more. Never re-run the write; that starts a second job. The finished result carries a `stream_url` and a `player_url`; share the `player_url`, it opens in any browser.

## With the connector tools

**Get the video.** First `search_videos_by_title(query)` with the video's title or the link's words; reuse the `m-` id if it is already in the account instead of uploading again. Otherwise, for a YouTube link or public URL, `upload_media(url)` and poll until `done`; note the `m-` id and `length`. Local files cannot come through the connector; the user uploads at https://console.videodb.io and shares the `m-` id.

| The user wants | Call |
|---|---|
| One range, or several ranges joined, from one video | `generate_clip(video_id, timeline=[[10, 25], [60, 90]])` (seconds) |
| The moments that match a description | `generate_transcript(media_id)` once, then `create_highlight_clip(video_id, prompt="every product demo")`, then `compile_clips` with the shots it returns |
| Control over which moments make the cut | `generate_transcript(media_id)`, poll, `get_transcript(media_id, timestamped=true, segmenter="sentence")`, pick the ranges yourself, then `generate_clip` (the `video-search` skill has the details) |
| A reel across several videos | `compile_clips(clips=[{"video_id": "m-a", "shots": [[5, 20]]}, {"video_id": "m-b", "shots": [[0, 12]]}])` |
| Vertical for Shorts, Reels, TikTok, or square | `reframe_video(video_id, start, end, target="vertical")` (`"square"`, `"landscape"`, or `{"width", "height"}`); `mode="smart"` follows the subject |
| A thumbnail | `generate_thumbnail(video_id, time_seconds=42)` |
| An MP4 file | `download_stream(stream_url, name="demo-reel.mp4")`, poll, share the download URL |

Notes that save a retry:

- `create_highlight_clip` matches spoken content by default and returns an empty `shots` list on a video whose speech is not transcribed or indexed. Transcribe first. It returns shots, not a stream; render them with `compile_clips`.
- `reframe_video` is slow. Always pass `start` and `end` for the segment the user wants. It saves a new video in the collection; subtitles or further cuts go on that new `m-` id. On some servers the first `done` reply carries only a `reframe_id` and the new video appears later: keep polling the same `output_url` and check `list_videos` for a new entry, for up to about five minutes. If no video appears, say that the vertical cut is still rendering on VideoDB's side, and give the user a landscape clip of the same range with `generate_clip` so they have something now.
- Subtitles on the clip: reframe first, then `generate_transcript` on the new video, then `add_subtitles` (the `video-subtitles` skill).
- Timestamps the user gives as mm:ss are converted to seconds before any call.

**Deliver.** Share the `player_url`, the ranges used, and offer the MP4.

## With the Python SDK (Claude Code)

Set up first with `/videodb:setup` if `import videodb` fails. Full reference: `${CLAUDE_PLUGIN_ROOT}/python/SKILL.md` and `${CLAUDE_PLUGIN_ROOT}/python/reference/editor.md`.

```python
from dotenv import load_dotenv; load_dotenv(".env")
import videodb
from videodb import ReframeMode
conn = videodb.connect(); coll = conn.get_collection()
video = coll.upload(url="https://www.youtube.com/watch?v=VIDEO_ID")
stream_url = video.generate_stream(timeline=[(10, 30), (45, 60)])        # ranges joined, no re-encode
vertical = video.reframe(start=10, end=30, target="vertical", mode=ReframeMode.smart)
print(f"https://console.videodb.io/player?url={stream_url}")
```
