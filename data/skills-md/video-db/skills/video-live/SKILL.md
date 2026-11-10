---
name: video-live
description: "Live video and screen recording. Use when the user wants to connect a camera or live stream (RTSP, RTMP, HLS), watch it for an event and get alerted, search or play back what a stream showed, join and record a Zoom, Google Meet or Teams meeting that is happening now, or record their desktop screen and audio and get a summary or searchable timeline of that session. A recording that already exists as a file is a normal video: use video-search to ask about it."
---

# Live streams, meetings and screen capture

## Which path

1. **VideoDB connector tools present** (names such as `connect_rtstream`, `index_rtstream_scenes`, `create_rtstream_alert`, `record_meeting`): use them for cameras, streams and meetings. This is the path in Claude chat on web, desktop and mobile, and in Cowork. Do not install anything and do not ask for an API key.
2. **No VideoDB tools, but you have a shell** (Claude Code, Cowork, any agent that can run Python): ask for the VideoDB API key in one friendly line (free at https://console.videodb.io, $20 of credits, no card). When the user gives it, in chat or any other way, save it yourself to the project's `.env` as `VIDEO_DB_API_KEY`, never print it, and continue with the Python SDK path at the end of this file. In Claude Code, `/mcp` then authorizing videodb also works.
3. **No VideoDB tools and no shell**: you are in Claude chat. Reply with only this, adapted to the request: "VideoDB isn't connected yet. Open Settings → Connectors, find VideoDB, click Connect and log in (free, no card). Then send this request again and I'll take it from there." Do not mention API keys, `.env`, shells, Claude Code or `/mcp` here; none of them apply in chat, and a key pasted into chat cannot be used because nothing runs code there.
4. **Desktop screen capture** needs a local recorder, so it runs only with a shell (Claude Code, Cowork) through the Python SDK path, on macOS and Windows. In chat, say so in one line.

Talking to the user: never write "index", "indexed" or "indexing" in a reply; say "searchable". One line of status at a time, then the result.

## With the connector tools

**Connect a camera or stream.** `connect_rtstream(url="rtsp://...", name="Lobby cam")` registers an RTSP, RTMP or HLS feed and starts ingesting. Note the `rts-` id. `set_rtstream_status(rtstream_id, action="stop")` stops it; streams bill while they run, so stop when the user is done.

**Watch for an event and alert.**

1. `index_rtstream_scenes(rtstream_id, prompt="Describe who is in the frame and what they are doing", window_seconds=10)`; note the scene index id.
2. `create_event(event_prompt="a person enters the room after hours", label="after-hours-entry")`.
3. `create_rtstream_alert(rtstream_id, index_id, event_id, callback_url="https://...")`. Alerts POST to the user's URL each time the event is seen. No callback URL from the user: skip the alert and offer search instead.

Spoken words on a stream: `index_rtstream_audio(rtstream_id)`; read the live text with `get_rtstream_transcript`.

**Search and play back.** `search_rtstream(rtstream_id, query)` over the indexed records; `get_rtstream_scenes(rtstream_id, scene_index_id, start, end)` to read descriptions for a window. Timestamps are Unix seconds. `get_rtstream_stream(rtstream_id, start, end)` returns a playable `player_url` for a window. `export_rtstream_recording(rtstream_id, name)` turns the latest recording into a regular video, after which the `video-search`, `video-clips` and `video-subtitles` skills apply.

**Record a meeting.** `record_meeting(meeting_url, bot_name="VideoDB Notetaker")` sends a recorder bot to Zoom, Google Meet or Microsoft Teams. Poll `get_meeting(meeting_id)` until `status` is `done` and a `video_id` appears, then `generate_transcript(media_id=video_id)` and read it with `get_transcript(media_id, timestamped=true, segmenter="sentence")` for a one-off question, or the `video-search` skill's make-it-searchable flow for `search_video` and `ask_video`.

Long jobs return `status: processing`. The reply carries an `output_url` and names the tool to poll (`poll_with`, or `retry_with` on older servers). Call that tool with the `output_url` until it is `done`; several `processing` replies in a row are normal (a 10-minute YouTube upload takes about five), and a `done` reply with an empty result means poll once more. Never re-run the write; that starts a second job.

## With the Python SDK (Claude Code)

Set up first with `/videodb:setup` if `import videodb` fails. Streams: `${CLAUDE_PLUGIN_ROOT}/python/reference/rtstream.md`. Desktop capture, step by step, with the WebSocket listener script: `${CLAUDE_PLUGIN_ROOT}/python/reference/capture.md` and `${CLAUDE_PLUGIN_ROOT}/python/SKILL.md` (Screen Recording section). The capture extra installs with `pip install "videodb[capture]>=0.5.0"`.

```python
from dotenv import load_dotenv; load_dotenv(".env")
import videodb
conn = videodb.connect(); coll = conn.get_collection()
rtstream = coll.connect_rtstream(url="rtsp://camera.local/stream", name="Lobby cam")
```
