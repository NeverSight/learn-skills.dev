---
name: video-search
description: Find a moment in a video or ask a question about it. Use when the user wants to search inside a video, a library, or a meeting recording ("find where they talk about pricing", "which scenes show a phone", "what did she say about hiring"), get an answer with timestamps, count what appears, or get a clip of that moment. A highlight reel from a prompt, a cut by time range, or a vertical cut is video-clips. Works on YouTube links, public URLs and the user's VideoDB videos.
---

# Find a moment, or ask a video

## Which path

1. **VideoDB connector tools present** (names such as `upload_media`, `search_video`, `ask_video`, `understand_video`): use them. This is the path in Claude chat on web, desktop and mobile, and in Cowork. Do not install anything and do not ask for an API key.
2. **No VideoDB tools, but you have a shell** (Claude Code, Cowork, any agent that can run Python): ask for the VideoDB API key in one friendly line (free at https://console.videodb.io, $20 of credits, no card). When the user gives it, in chat or any other way, save it yourself to the project's `.env` as `VIDEO_DB_API_KEY`, never print it, and continue with the Python SDK path at the end of this file. In Claude Code, `/mcp` then authorizing videodb also works.
3. **No VideoDB tools and no shell**: you are in Claude chat. Reply with only this, adapted to the request: "VideoDB isn't connected yet. Open Settings → Connectors, find VideoDB, click Connect and log in (free, no card). Then send this request again and I'll take it from there." Do not mention API keys, `.env`, shells, Claude Code or `/mcp` here; none of them apply in chat, and a key pasted into chat cannot be used because nothing runs code there.

Talking to the user: never write "index", "indexed" or "indexing" in a reply. Say "searchable" ("it is now searchable by what was said and what is shown"), and "transcribe" rather than naming a job. One line of status at a time, then the result.

Long jobs return `status: processing`. The reply carries an `output_url` and names the tool to poll (`poll_with`, or `retry_with` on older servers). Call that tool with the `output_url` until it is `done`; several `processing` replies in a row are normal (a 10-minute YouTube upload takes about five), and a `done` reply with an empty result means poll once more. Never re-run the write; that starts a second job.

## With the connector tools

**1. Get the video.** First `search_videos_by_title(query)` with the video's title or the link's words; reuse the `m-` id if it is already in the account. Otherwise, for a YouTube link or public URL, `upload_media(url)`, poll until `done`, and note the `m-` id and the `length` in seconds. The user has no URL and the file is on their computer: the connector cannot take local files; point them to the console at https://console.videodb.io to upload, then continue with the `m-` id.

**2. Pick the fast path or the index path.**

*Fast path, the default for a one-off question about what was said.* Read the transcript yourself and find the moments:

```
generate_transcript(media_id)                                   # a job; poll until done (instant if already transcribed)
get_transcript(media_id, timestamped=true, segmenter="sentence")   # sentence segments with start and end seconds
```

Scan the segments for the moments the user described, note their start and end, and go to step 4. No index needed. Two traps: the transcript job's `done` result includes text and a word list, but the list is truncated, so always read with `get_transcript`; and the default segmenter is one segment per word, capped at 2000 segments, so pass `segmenter="sentence"` (a couple of hours of speech fit) or `start` and `end` windows. A video the tool still truncates, or one the user will keep asking about, is a sign to use the index path.

Nothing matches: say so plainly and do not stretch a loose match into the thing the user asked for. A YouTube upload can be an excerpt of a longer talk. Offer the nearest moment, clearly labelled as such, or ask for another video.

*Index path.* Use it when the question is about what is shown rather than said, when the user wants counts or exact filters, when they will ask many questions about the same video or library, or when the transcript is too long to read. Check `list_indexes(video_id)` first; if nothing is ready:

```
understand_video(video_id, analyzers=[
  {"type": "spoken_words", "name": "transcript"},
  {"type": "vlm", "name": "scene", "config": {"prompt": "Describe the scene and any on-screen text."}}
])
```

Poll `get_understanding(video_id, understanding_id)` until every analyzer is `done`, then build one index per analyzer:

```
create_index(video_id, understanding_id, analyzer_name="transcript")
create_index(video_id, understanding_id, analyzer_name="scene")
```

Only speech matters (a podcast, a call): run just the `spoken_words` analyzer. Objects and counts ("how many cars"): add `{"type": "object_detection"}` or `{"type": "activity_recognition"}`.

**3. Retrieve (index path).**

| The user wants | Call |
|---|---|
| Moments with timestamps | `search_video(video_id, query, include_clip=true)` |
| A written answer with sources | `ask_video(video_id, question, include_sources=true)` |
| Across a whole library | `search_collection(query)` or `ask_collection(question)` |
| Counts and groups ("which objects appear most") | `aggregate_index(video_id, index_name="objects", group_by="frames.detections.label")` |
| Exact filters ("scenes with label = car") | `query_index(video_id, index_name, filter)` |
| A deeper investigation with follow-ups | `search_video(..., mode="deepsearch")`, then pass `session_id` on the next call |

**4. Deliver.** Give the moments as `start` to `end` in mm:ss with the words that matched (quote the transcript, or the `text` of each search hit), and the `player_url` of each clip when `include_clip` was set. Make one clip of the matches: `generate_clip(video_id, timeline=[[start, end], ...])` (seconds, a few seconds of padding on each side reads better), poll, then share the `player_url`.

Older videos that were indexed with `index_spoken_words` or `index_scenes` (v1) are searched with `legacy_search_video` and `legacy_search_collection`.

## With the Python SDK (Claude Code)

Set up first with `/videodb:setup` if `import videodb` fails. Full reference: `${CLAUDE_PLUGIN_ROOT}/python/SKILL.md` and `${CLAUDE_PLUGIN_ROOT}/python/reference/search.md`.

```python
from dotenv import load_dotenv; load_dotenv(".env")
import videodb, time
conn = videodb.connect(); coll = conn.get_collection()
video = coll.upload(url="https://www.youtube.com/watch?v=VIDEO_ID")
u = video.understand(analyzers=[{"type": "spoken_words", "name": "transcript"},
                                {"type": "vlm", "name": "scene", "config": {"prompt": "Describe the scene."}}])
u.wait_until_complete()
for a in u.list_analyzers():
    if a.is_successful: video.index(source=a, name=a.name).wait_until_complete()
r = video.search("the part about pricing")
for s in r.shots: print(f"[{s.start:.0f}s-{s.end:.0f}s] {s.text}")
print(r.compile())   # stream URL of the matches; player: https://console.videodb.io/player?url={STREAM_URL}
```
