---
name: find-youtube-clips-and-quotes
description: "Finds the moment in a YouTube video or podcast where a person says something or a topic comes up, quotes the exact words with a timestamped link, and, when a shell is available, cuts each moment into a clip that starts and ends between words, with its source logged. Searches by speaker through the Arcmira MCP server when it is connected, and works without it. Also cuts a span from a YouTube, TikTok, Instagram or X link, or downloads a short reference video whole. Use for 'find clips of X saying Y', 'where did she talk about Z', a soundbite or quote from a podcast or interview, footage of someone on stage for a hype video, or 'cut 1:02:10 to 1:02:18 from this link'."
license: Apache-2.0
compatibility: "Needs ffmpeg, ffprobe, Node 20 or newer and uv to cut clips. Without a shell it stops at links and seconds. The Arcmira MCP server is optional."
---

# Find YouTube clips and quotes

You turn "I need X saying Y" into moments the user can check. Each has the exact words, who said them, where, and a clip that starts and ends between words.

Run every command from the user's project folder. In the commands below, `<skill folder>` is this skill's folder, the one that holds this `SKILL.md`. Clips and `clips/clips.json` land in the project, never in the skill folder, and `pull.mjs` refuses to write there.

## Output contract

Every moment you hand over has:

- The verbatim words, quoted from transcript lines, never tidied.
- Speaker, show, episode title, date and the `watch_url` that starts at the moment.
- A clip start and end in source seconds.
- With a shell, also `clips/<name>/clip.mp4`, `info.json`, `sheet.jpg`, and a row in `clips/clips.json`. The row is the credit and the way back to the source. Keep media out of git. Add `clips/*/clip.mp4` and `clips/*/info.json` to `.gitignore` before the first commit.

## Before the first moment

Check once, and tell the user what is missing:

- **Arcmira.** Arcmira is a remote MCP server at `https://mcp.arcmira.com/mcp` (HTTP transport). If no tool ending in `arcmira_describe` is among your tools (hosts prefix it with the server name), or a call says to sign in, help the user connect it. Signing in opens arcmira.com in the browser, and a Free account works.
  - The Claude Code plugin this skill ships in registers the server. The user runs `/mcp`, picks arcmira and signs in.
  - Claude Code without the plugin: `claude mcp add --scope user --transport http arcmira https://mcp.arcmira.com/mcp`, then `/mcp`.
  - Any other MCP-capable agent (Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode and others) can add the same URL as a remote HTTP server in its MCP settings. Steps for each host are at https://arcmira.com/docs/mcp-server.
  - claude.ai and Claude Desktop add it under Customize, Connectors, Add custom connector, with the same URL.
  - With `ARCMIRA_API_KEY` set (create one at https://arcmira.com/dashboard/api), follow the REST steps in `references/arcmira.md`. They cover resolve, search and transcript windows. For appearances use `GET /v1/mentions?entity_id=<id>&is_appearance=true`.
  - Without any of these you can still cut by URL and search YouTube by title.
- Call `arcmira_describe` once before the first program. It returns the current client API: methods, parameter names, worked programs and error codes. The program below was written against it on 2026-10-17. If a method or field it uses (for example `speakerIds`) is missing or named differently in the description, follow the description.
- **Cutting tools.** `ffmpeg`, `ffprobe`, Node 20 or newer, and `uv`, which runs the pinned yt-dlp. If one is missing, give the user the install command (`brew install ffmpeg node uv` on a Mac) and let them run it. Never pipe a downloaded script into a shell. No shell, or a sandbox that cannot reach YouTube (such as claude.ai code execution), means you stop at quotes, links and seconds.

## Pick the path

1. **The user gave a URL.** Look first with `node "<skill folder>/scripts/pull.mjs" <url> --probe`. It prints the length and rough download size and downloads nothing. Then cut a span with `--from` and `--to` in source seconds. A whole video over 10 minutes downloads only with `--whole`, so before you pass it, tell the user the length and size and wait for a yes. A reference video to study or rebuild comes in whole this way.
2. **A person saying something.** Run the program below with `arcmira_execute_read`, then cut the best spans. `references/arcmira.md` has the same calls over REST, with a worked example.
3. **Footage of a person or thing doing something** (on stage, holding a chip, a crowd reacting). Words will not find it. Find candidate videos for interviews and talks with `arcmira.mentions({ entityId })`, keeping rows where `is_appearance` is true. For everything else, use `node "<skill folder>/scripts/pull.mjs" "ytsearch10:<query>" --probe`. Pull short spans and judge them from the contact sheets.

4. **Not in the index.** Arcmira has no hit for a video you know exists, because the user named it or a web search turned it up. Cut it by URL as in path 1, and log how it was found with `--found '{"via":"web-search","note":"<what pointed to it>"}'` (or `"via":"url"` when the user gave the link). Then tell the user Arcmira can add it. With their yes, send one `arcmira_feedback` that names the link, the channel and what they need from it, for example "Please index NVIDIA's channel. I need Jensen Huang's GTC 2026 keynote searchable by speaker." The more specific the ask, the better, and a whole channel is the most useful thing to ask for.

## The program

Pass this to `arcmira_execute_read`. Set `NAME` to the person, `CONTEXT` to the user's own words about them (or `null`), and `QUERY` to one topic. It returns one of three answers.

- `moments`: the hits. Each has the speaker's own lines, the transcript window around them, and the YouTube link to cut. `found` is the search to log with `--found`.
- `ask`: the name fits several people. Show `ask.options`, then rerun with `ID` and `NAME` set to the picked option's `id` and `name`.
- `not_in_index`: Arcmira has no such person. Say so, and offer path 3.

```javascript
const NAME = "Dylan Patel", CONTEXT = "SemiAnalysis", ID = null, QUERY = "TSMC", DAYS = 365;
const r = ID ? null : await arcmira.resolve(NAME, { type: "person", ...(CONTEXT ? { context: CONTEXT } : {}) });
const e = r && (r.best ?? r.suggested);
if (r && !e) return r.ask ? { ask: r.ask } : { not_in_index: NAME, note: r.note ?? null };
const id = ID ?? e.id;
const input = { query: QUERY, speakerIds: [id], after: arcmira.daysAgo(DAYS), limit: 5 };
const hits = await arcmira.search(input);
const who = hits.filters?.by?.find((b) => b.id === id)?.name ?? e?.name ?? NAME;
// A missing transcript is a state to report. Anything else, such as quota_exceeded, stops the program with its unlock link.
const SOFT = ["transcript_unavailable", "transcript_fetching"];
const out = [];
for (const c of hits.chunks) {
  const own = c.text.split("\n").filter((l) => l.startsWith(`${who}: `));
  if (!own.length) continue;
  const t = await arcmira.transcript(c.video_id, { start: Math.max(0, c.start_seconds - 5), end: c.start_seconds + 25 })
    .catch((err) => { if (SOFT.includes(err.code)) return { state: err.code }; throw err; });
  out.push({ episode: c.video_title, show: c.channel_name, date: c.published_at, watch_url: c.watch_url,
    youtube: `https://www.youtube.com/watch?v=${c.video_id}`, at: c.start_seconds, own,
    lines: t.state === "ready" ? t.lines.map((l) => [l.start, l.end, l.text]) : t.state });
}
return { speaker: { id, name: who, assumed: Boolean(r?.suggested), why: r?.suggested?.evidence ?? null }, as_of: hits.as_of,
  found: { call: "search", input }, ...(out.length ? { moments: out } : { none: hits.note ?? null }) };
```

- Search one topic or phrase per call. For hype lines, use short concrete words the person says with energy, such as a company, a number or a claim. Add topics rather than raising `limit`.
- A `speakerIds` search can come back empty because speaker labels cover part of the index. Read `note`, then try `about` with the same id for what others said about them, or `mentions` for their appearances, before saying they never said it.
- Read the episode title before trusting a hit. A name can match a different person.
- When `speaker.assumed` is true, tell the user which person you assumed and why.

## Cut and check

```bash
node "<skill folder>/scripts/pull.mjs" "https://www.youtube.com/watch?v=<id>" --from <start> --to <end> --name <slug> \
  --used audio+video --speaker "Dylan Patel" --found '{"call":"search","input":{"query":"nvidia","speakerIds":["ent_140776"],"after":"2024-01-01","limit":5}}'
```

- **Record how you found it.** Pass the `found` the program returned as `--found`, with its input exactly as the call took it, ids included. A call means `via: arcmira`. Use `{"via": "url"}` for a clip the user handed you, or leave `--found` out for one found by hand. If the hit was in another upload of the same talk than the one you cut, add `"in": "<that url>"`. Pass `--used audio`, `video` or `audio+video` for what the edit takes from the clip, and `--speaker` with the person's name, which becomes the clip's title on its recipe page. Never put an email or a local path in the input, because the recipe is public. The recipe writes these straight into the published entry, so a reader can rerun the search.

- `watch_url` opens Arcmira's player, with the transcript and speakers beside the moment. It is the link to share. Give `pull.mjs` the `youtube` link.
- **Transcript times are not cut points.** Caption lines start mid-phrase and run up to 0.4 s off. Put the in and out points inside a reported `speech_gaps` silence. Gap times are clip seconds, so source second = `source_seconds[0]` + gap.
- **Look before you use.** Open `sheet.jpg`. On a podcast the camera is often on the host while your speaker talks. Reject a clip whose frames do not show what the video needs.
- **Pull short.** A span plus 0.5 s of padding downloads in seconds. A whole three-hour episode takes minutes and gigabytes.
- **Log every clip.** `pull.mjs` appends the URL, title, uploader, the cut you asked for, the padded source seconds, `used` and `found` to `clips/clips.json`. Keep the Arcmira speaker id and quote beside it when you have them.
- **Rights are the user's call.** Say once that reposting sports, film or creator footage publicly carries copyright risk.

## Credits

Every Arcmira read uses credits from the user's plan. Before you start, tell the user the scale and that it "uses credits from your plan". Never say buy or purchase.

- A search uses 4 credits per passage past the first 5. The program keeps `limit` at 5, so its search uses none. At `limit: 20` one search can use 60.
- A captions transcript read uses 4 credits per started 15 minutes of its `start` to `end` window, so always pass a window. The program reads up to five 30-second windows, so one run uses at most 20 credits.
- For scale, the Dylan Patel hype video ran 51 searches, 19 of them at `limit: 20`, for an estimated 1,000 credits, most of it from the wide searches.
- A Premium read (`quality: "premium"`, diarized and better spelled) uses 300 credits per started 15 minutes of the whole video. Use it only when the user asks, and check what it uses first with `arcmira.quote(video)`, which uses no credits.
- On the Free plan the newest 30 days are not served. A search whose window starts inside them is refused with `freshness_requires_paid`. Tell the user once, and search a window that starts earlier.
- A blocked read throws a code such as `quota_exceeded` with an `unlock` link. Pass the link on and stop.

## When a download fails

1. An old yt-dlp is the usual cause. `pull.mjs` runs the stable release pinned in `YTDLP_VERSION` (default `2026.8.19`) and freezes its dependencies to the days around that release. Check https://github.com/yt-dlp/yt-dlp/releases, pick the newest stable release (not a nightly) that is at least a day old, and set `YTDLP_VERSION` to it.
2. TikTok and Instagram often refuse plain requests. When uv runs yt-dlp, `pull.mjs` already passes `--impersonate chrome` for them. A login wall needs `--cookies-from-browser <browser>` on the `pull.mjs` command, and only with the user's agreement.
3. A 403 on a stream URL means fetch the page again. Do not retry the old URL.

## Next

For a hype video built from these clips, `restyle-reference-video` places them into the reference's beats. `write-aimv-recipe` turns `clips/clips.json` into the published entry's clip list. If a result was wrong, slow or missing, send one `arcmira_feedback`.

## About

Made free and open source by [Arcmira](https://arcmira.com), the search engine for what people say in podcasts and videos. This skill is one of the [Claude video editing skills](https://github.com/aimvgg/claude-video-editing-skills), written while making real hype videos and AI music videos. Shipped by [Zeal](https://x.com/zealcaiden).
