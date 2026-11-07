---
name: video-subtitles
description: Subtitles, captions and transcripts for a video or audio file. Use when the user wants a transcript (plain or timestamped) of a video, podcast or call recording, static subtitles burned in with a chosen font, colour and position, a transcript or subtitles translated into another language, or dubbing. Animated or karaoke captions belong to video-edit. Works on YouTube links, public video URLs, audio files and media already in the user's VideoDB account.
---

# Subtitles and transcripts

## Which path

1. **VideoDB connector tools present** (names such as `generate_transcript`, `add_subtitles`, `translate_transcript`, `upload_media`): use them. This is the path in Claude chat on web, desktop and mobile, and in Cowork. Do not install anything and do not ask for an API key.
2. **No VideoDB tools, but you have a shell** (Claude Code, Cowork, any agent that can run Python): ask for the VideoDB API key in one friendly line (free at https://console.videodb.io, $20 of credits, no card). When the user gives it, in chat or any other way, save it yourself to the project's `.env` as `VIDEO_DB_API_KEY`, never print it, and continue with the Python SDK path at the end of this file. In Claude Code, `/mcp` then authorizing videodb also works.
3. **No VideoDB tools and no shell**: you are in Claude chat. Reply with only this, adapted to the request: "VideoDB isn't connected yet. Open Settings → Connectors, find VideoDB, click Connect and log in (free, no card). Then send this request again and I'll take it from there." Do not mention API keys, `.env`, shells, Claude Code or `/mcp` here; none of them apply in chat, and a key pasted into chat cannot be used because nothing runs code there.

Talking to the user: never write "index", "indexed" or "indexing" in a reply. Say "searchable" ("it is now searchable by what was said and what is shown"), and "transcribe" rather than naming a job. One line of status at a time, then the result.

Long jobs return `status: processing`. The reply carries an `output_url` and names the tool to poll (`poll_with`, or `retry_with` on older servers). Call that tool with the `output_url` until it is `done`; several `processing` replies in a row are normal (a 10-minute YouTube upload takes about five), and a `done` reply with an empty result means poll once more. Never re-run the write; that starts a second job.

## With the connector tools

**Get the video.** First `search_videos_by_title(query)`; reuse the `m-` id if the video is already in the account. Otherwise, for a YouTube link or public URL, `upload_media(url)` and poll until `done`; note the `m-` id. Local files cannot come through the connector; the user uploads at https://console.videodb.io and shares the `m-` id.

**Transcript.** `generate_transcript(media_id)` (add `language_code` if the speech is not English), poll until `done`, then `get_transcript(media_id, timestamped=true, segmenter="sentence")` for sentence timestamps, or `timestamped=false` for plain text. The default segmenter is one segment per word and timestamped output is capped at 2000 segments, so pass `segmenter="sentence"` or `start` and `end` for long media. The transcript job result also carries text and a word list, but the list is truncated; read the transcript with `get_transcript`.

**Subtitles burned into the video.**

1. `generate_transcript(media_id)` and poll until `done` (instant if the video already has a transcript). `add_subtitles` reads the video's transcript; a `spoken_words` analyzer run from `understand_video` counts too. `index_spoken_words` is the legacy v1 call and is not needed.
2. `add_subtitles(video_id, ...)`. Returns a `stream_url` and a `player_url` at once; it is not a job.
3. An MP4 file: `download_stream(stream_url, name="...")`, poll, then share the download link.

Style options on `add_subtitles`: `font_name`, `font_size` (8 to 72, default 18), `bold`, `italic`, `alignment` (`bottom_center` default, `top_center`, `middle_center`, ...), `border_style` (`outline`, `opaque_box` or `no_border`), `outline`, `outline_colour`, `shadow`, `margin_l`, `margin_r`, `margin_v`. Colours use the ASS format `&HAABBGGRR`: opaque white `&H00FFFFFF`, black `&H00000000`, yellow `&H0000FFFF`. "White text on a black box" is `primary_colour="&H00FFFFFF", back_colour="&H00000000", border_style="opaque_box"`.

**Animated or karaoke captions, or captions on a composed video.** Use the `video-edit` skill's `render_timeline` with a `caption` asset (`src: "auto"`, `animation: "karaoke"`). The video must already be transcribed (`generate_transcript`, or a `spoken_words` analyzer run), or the render comes back with no captions and no error.

**Translate.** `translate_transcript(video_id, language="Spanish")` returns the translated, timestamped segments. Give them to the user as text or as an SRT-style list.

**Dubbing and translated voiceover.** Not available through the connector. In Claude Code, the SDK does it (`${CLAUDE_PLUGIN_ROOT}/python/reference/editor.md`, dubbing section). In chat, offer the translated transcript and say that dubbing needs the SDK.

## With the Python SDK (Claude Code)

Set up first with `/videodb:setup` if `import videodb` fails. Full reference: `${CLAUDE_PLUGIN_ROOT}/python/SKILL.md`.

```python
from dotenv import load_dotenv; load_dotenv(".env")
import videodb
from videodb import SubtitleStyle, SubtitleAlignment, SubtitleBorderStyle
conn = videodb.connect(); coll = conn.get_collection()
video = coll.upload(url="https://www.youtube.com/watch?v=VIDEO_ID")
video.generate_transcript()
print(video.get_transcript_text())
stream_url = video.add_subtitle(SubtitleStyle(font_size=20, primary_colour="&H00FFFFFF",
                                              back_colour="&H00000000", border_style=SubtitleBorderStyle.opaque_box,
                                              alignment=SubtitleAlignment.bottom_center))
print(f"https://console.videodb.io/player?url={stream_url}")
```
