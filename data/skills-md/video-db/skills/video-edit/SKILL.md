---
name: video-edit
description: Edit and compose video on a timeline. Use when the user wants to add background music, a voiceover or another audio track, put text, a logo or an image overlay on a video, join several videos or images into one with fades or other transitions, add animated or word-by-word karaoke captions, change the resolution or aspect ratio of a composition, or generate music, voiceover, images or video with AI for a composition. Static subtitles with a chosen font and position belong to video-subtitles.
---

# Edit and compose

## Which path

1. **VideoDB connector tools present** (names such as `render_timeline`, `upload_media`, `download_timeline_render`): use them. This is the path in Claude chat on web, desktop and mobile, and in Cowork. Do not install anything and do not ask for an API key.
2. **No VideoDB tools, but you have a shell** (Claude Code, Cowork, any agent that can run Python): ask for the VideoDB API key in one friendly line (free at https://console.videodb.io, $20 of credits, no card). When the user gives it, in chat or any other way, save it yourself to the project's `.env` as `VIDEO_DB_API_KEY`, never print it, and continue with the Python SDK path at the end of this file. In Claude Code, `/mcp` then authorizing videodb also works.
3. **No VideoDB tools and no shell**: you are in Claude chat. Reply with only this, adapted to the request: "VideoDB isn't connected yet. Open Settings → Connectors, find VideoDB, click Connect and log in (free, no card). Then send this request again and I'll take it from there." Do not mention API keys, `.env`, shells, Claude Code or `/mcp` here; none of them apply in chat, and a key pasted into chat cannot be used because nothing runs code there.

Talking to the user: never write "index", "indexed" or "indexing" in a reply. Say "searchable" ("it is now searchable by what was said and what is shown"), and "transcribe" rather than naming a job. One line of status at a time, then the result.

Rendering is a long job: the call returns `status: processing`. The reply carries an `output_url` and names the tool to poll (`poll_with`, or `retry_with` on older servers). Call that tool with the `output_url` until it is `done`; several `processing` replies in a row are normal (a 10-minute YouTube upload takes about five), and a `done` reply with an empty result means poll once more. Never re-run the write; that starts a second job. Share the finished `player_url`.

Do not fall back to ffmpeg, moviepy or local encoding for anything below; it all runs on VideoDB's servers.

## With the connector tools

**Assets first.** Every piece of media needs a VideoDB id: videos `m-`, audio `a-`, images `img-`. `upload_media(url)` takes a public URL or YouTube link (`media_type="audio"` for a music file, `"image"` for a logo). `list_videos`, `list_audios`, `list_images` show what is already there. Local files cannot come through the connector; the user uploads at https://console.videodb.io.

**One call composes everything:** `render_timeline(tracks=[...], resolution="1920x1080", background="#000000")`. Each track holds clips; each clip has `start` (seconds on the timeline), `duration`, and an `asset`. Tracks stack by `z_index` (higher on top).

| The user wants | Asset in the clip |
|---|---|
| A video, from second 10 of the source | `{"type": "video", "id": "m-...", "start": 10, "volume": 1}` |
| Background music at 20% | `{"type": "audio", "id": "a-...", "volume": 0.2}` on its own track |
| A title or lower-third | `{"type": "text", "text": "Launch day", "font": {"size": 64, "color": "#FFFFFF"}, "background": {"color": "#000000", "opacity": 0.6, "border_width": 12}}` with clip `fit: "contain"` and `position: "bottom"` |
| A logo or image | `{"type": "image", "id": "img-..."}` with clip `scale: 0.2`, `position: "top_right"`, `opacity: 0.9` |
| Captions from speech | `{"type": "caption", "src": "auto", "animation": "box_highlight"}`; the video must already be transcribed (`generate_transcript`, or a `spoken_words` analyzer run) or the render shows no captions and no error |
| A fade between clips | clip `transition: {"in": "fade", "out": "fade", "duration": 0.5}` |
| Vertical for social | `resolution="1080x1920"`, clip `fit: "crop"` |

Text assets: `width` and `height` are honoured only with `fit: "contain"`; the default `crop` scales the text box up to fill the frame.

Example, a 20-second clip with a title and quiet music:

```
render_timeline(resolution="1920x1080", tracks=[
  {"z_index": 0, "clips": [{"start": 0, "duration": 20, "asset": {"type": "video", "id": "m-abc", "start": 30}}]},
  {"z_index": 1, "clips": [{"start": 0, "duration": 4, "fit": "contain", "position": "bottom",
                            "transition": {"in": "fade", "out": "fade"},
                            "asset": {"type": "text", "text": "Launch day", "font": {"size": 64}}}]},
  {"z_index": 0, "clips": [{"start": 0, "duration": 20, "asset": {"type": "audio", "id": "a-xyz", "volume": 0.2}}]}
])
```

**An MP4 file:** `download_timeline_render(stream_url)`, poll, share the download URL.

**Generating music, voiceover, images or video with AI, and dubbing:** not available through the connector. In Claude Code the SDK does it (below). In chat, ask the user for a hosted audio or image URL to upload instead, and say that generation needs Claude Code or the SDK.

## With the Python SDK (Claude Code)

Set up first with `/videodb:setup` if `import videodb` fails. Full guide: `${CLAUDE_PLUGIN_ROOT}/python/reference/editor.md`; generation: `${CLAUDE_PLUGIN_ROOT}/python/reference/generative.md`.

```python
from dotenv import load_dotenv; load_dotenv(".env")
import videodb
from videodb.editor import Timeline, Track, Clip, VideoAsset, AudioAsset, TextAsset, Fit, Transition
conn = videodb.connect(); coll = conn.get_collection()
video = coll.upload(url="https://www.youtube.com/watch?v=VIDEO_ID")
music = coll.generate_music(prompt="warm acoustic background", duration=20)   # or coll.upload(url=..., media_type="audio")
voice = coll.generate_voice(text="Welcome to the show", voice_name="Default")
timeline = Timeline(conn); timeline.resolution = "1920x1080"
v = Track(); v.add_clip(0, Clip(asset=VideoAsset(id=video.id, start=30), duration=20))
a = Track(); a.add_clip(0, Clip(asset=AudioAsset(id=music.id, volume=0.2), duration=20))
timeline.add_track(v); timeline.add_track(a)
stream_url = timeline.generate_stream()
print(f"https://console.videodb.io/player?url={stream_url}")
```

Dubbing: `coll.dub_video(video.id, language_code="es")`.
