---
name: boring-youtube-mining
description: |
  Pull recent YouTube transcripts from pre-selected channels and generate
  topic ideas from them. Use when someone says "mine YouTube", "find video
  ideas", "what are creators talking about", "YouTube research", "transcript
  ideas", "content mining", "what should I talk about", "topic ideas from
  YouTube", or wants to turn other creators' videos into their own content
  angles. World Code integrated — ideas map to your Bridge when available.
metadata:
  version: 1.0.0
---

# YouTube Mining — World Code Edition

You pull recent videos from pre-selected YouTube channels, download their transcripts, and generate content ideas the user can actually use. One pass. No back-and-forth.

## Before Starting — Check Dependencies

Run this silently:

```bash
which yt-dlp
```

**If `yt-dlp` is NOT installed**, stop and tell the user:

> **`yt-dlp` is required but not installed.**
>
> Install it for your platform:
> - **macOS:** `brew install yt-dlp`
> - **Windows:** `winget install yt-dlp`
> - **Linux:** `pip install yt-dlp` or your package manager
> - **Universal:** `pip install yt-dlp`
>
> Then run `/boring-youtube-mining` again.

Do not proceed without `yt-dlp`. Stop gracefully.

---

## Before Starting — Load World Code (Optional)

Try to read these files silently:
- `world-code/voice.md` — Voice rules (NOT applied to output — this is research, not published content)
- `world-code/conversation.md` — Bridge structure (walls, struggles, goblins, treasures)

**If conversation.md exists:** Use the Bridge to filter and prioritize ideas. Every idea gets mapped to a wall, struggle, or goblin. Ideas that don't connect to any get deprioritized (still listed, just flagged as "no Bridge connection").

**If conversation.md doesn't exist:** Generate ideas purely from transcript analysis. Don't nag about missing files.

---

## Step 1: Load Channel List

Read `settings/youtube-channels.md`.

**If the file doesn't exist**, create it with starter content and tell the user:

> I created `settings/youtube-channels.md` with some example channels. Edit it in Obsidian to add the channels you want to mine, then run `/boring-youtube-mining` again.

Starter content for `settings/youtube-channels.md`:

```markdown
# YouTube Channels

Add channels you want to mine for content ideas. Use the @ handle format.
Add a short description so Claude knows the context.

- @AlexHormozi - Business, offers, scaling
- @ChrisDo - Branding, pricing, positioning
```

Stop after creating the file. Let the user configure it first.

---

## Step 2: Fetch Recent Videos

For each channel in the list, run:

```bash
yt-dlp --flat-playlist --playlist-items 1:5 --print "%(id)s | %(title)s | %(duration_string)s" "https://www.youtube.com/@{handle}/videos" 2>/dev/null
```

Process channels **sequentially** (not in parallel) to avoid rate limiting.

**Present the results as a numbered list:**

```
## Recent Videos

### @AlexHormozi
1. [dQw4w9WgXcQ] How to Price Your Offer (12:34)
2. [abc123def] The $100M Framework Nobody Uses (18:22)
...

### @ChrisDo
3. [xyz789ghi] Why Your Brand Is Invisible (9:45)
...
```

Ask the user:

> Which videos should I analyze? Enter numbers (e.g., "1, 3, 5") or "all".

**If a channel handle fails to resolve**, report it and continue with the remaining channels:

> Could not fetch videos from @BadHandle — check the handle in `settings/youtube-channels.md`.

---

## Step 3: Download Transcripts

For each selected video, first check if a cached transcript exists:

```bash
ls "content/youtube-transcripts/{video_id}.md" 2>/dev/null
```

**If cached:** Skip download, read from cache. Tell the user:

> Transcript for "{title}" already cached — skipping download.

**If not cached:** Download the auto-generated English captions:

```bash
yt-dlp --write-auto-sub --sub-lang en --sub-format vtt --skip-download -o "content/youtube-transcripts/%(id)s" "https://www.youtube.com/watch?v={video_id}" 2>/dev/null
```

Then clean the VTT file and save as markdown. Create the directory if needed:

```bash
mkdir -p "content/youtube-transcripts"
```

### Cleaning VTT Captions

The raw VTT file contains timestamps and duplicate lines. Clean it:
1. Strip all timestamp lines (lines matching `XX:XX:XX.XXX --> XX:XX:XX.XXX`)
2. Strip the `WEBVTT` header and `Kind:`/`Language:` metadata lines
3. Remove duplicate consecutive lines (VTT repeats lines across cue boundaries)
4. Remove position/alignment tags like `<c>`, `</c>`, `align:start position:0%`
5. Join into paragraphs (group sentences, add line breaks at natural pauses)

Save as `content/youtube-transcripts/{video_id}.md` with frontmatter:

```markdown
---
video_id: {video_id}
title: {video title}
channel: {channel handle}
date_fetched: {YYYY-MM-DD}
url: https://www.youtube.com/watch?v={video_id}
---

# {video title}

**Channel:** {channel handle}
**URL:** https://www.youtube.com/watch?v={video_id}

## Transcript

{cleaned transcript text}
```

Delete the raw VTT file after conversion.

### Edge Cases

- **No English auto-captions available:** Skip the video with a message:
  > No English captions available for "{title}" — skipping.

- **Very long transcripts (estimated 10,000+ words):** Chunk-summarize before idea generation. Break into ~3,000 word sections, summarize each section's key points, then use the summaries for idea generation. Note in the output that the transcript was summarized.

---

## Step 4: Generate Ideas

For each transcript, generate ideas through two lenses:

### Lens 1: Direct Response

How would the user respond to this video's ideas? Generate 2-3 ideas:

- **Agree & Expand** — They made a point you also believe. What's your unique angle on it?
- **Disagree & Counter** — They said something you see differently. What's your take?
- **Build On** — They touched on something but stopped short. Where would you take it?

### Lens 2: Gap Ideas

What's missing? Generate 1-2 ideas:

- Topics they mentioned but didn't go deep on
- Adjacent topics their audience would care about but weren't covered
- The question their video raises but doesn't answer

### Per Idea, Include:

| Field | Description |
|-------|-------------|
| **Idea title** | Sharp, specific — not "Thoughts on pricing" but "Why Hourly Pricing Kills Solo Businesses" |
| **Angle** | Direct Response (agree/disagree/expand) or Gap |
| **Source** | Video title + timestamp range if identifiable |
| **Your take (1-2 sentences)** | The core argument you'd make |
| **Bridge mapping** | Which wall/struggle/goblin this connects to (if conversation.md exists) |
| **Content type** | Post, thread, email, essay, video script, carousel |
| **Draft hook** | One opening line that would stop the scroll |

### Quality Over Quantity

- **3-5 ideas per video.** Not 10. Not 20. The best 3-5.
- Every idea must pass the "would I actually make this?" test
- If an idea is generic ("Content is important"), kill it
- Ideas without a clear angle aren't ideas — they're topics. Topics aren't useful.

### Bridge-First Filtering (when conversation.md exists)

After generating all ideas, sort them:

1. **Strong Bridge connection** — directly maps to a wall, struggle, or goblin
2. **Loose Bridge connection** — related to the user's world but not a direct map
3. **No Bridge connection** — interesting but disconnected from their World Code

Group 3 still gets listed but flagged. The user decides if it's worth pursuing.

---

## Step 5: Save Output

Write the output file to `content-ideas/youtube-mining-{YYYY-MM-DD}.md`:

```markdown
---
type: youtube-mining
date: {YYYY-MM-DD}
channels_mined: [{list of channels}]
videos_analyzed: {count}
ideas_generated: {count}
---

# YouTube Mining — {YYYY-MM-DD}

## Sources

| Video | Channel | Ideas |
|-------|---------|-------|
| {title} | {channel} | {count} |
...

## Ideas

### From: "{video title}" (@channel)

#### 1. {Idea Title}

- **Angle:** {Direct Response — Agree/Disagree/Expand | Gap}
- **Source:** {video title}, ~{timestamp context if available}
- **Your take:** {1-2 sentences}
- **Bridge:** {wall/struggle/goblin or "No direct connection"}
- **Content type:** {post/thread/email/essay/video/carousel}
- **Draft hook:** "{opening line}"

---

{repeat for each idea}

## Bridge Summary

### Strong Connections
- {idea} → {wall/struggle}
...

### No Connection
- {idea} — interesting but not tied to your current World Code
...

## Next Steps

- Pick an idea and run `/boring-copywriting` to draft it
- Run `/boring-social-content` to turn an idea into platform-specific posts
- Run `/boring-remix` to generate multiple angles on your favorite idea
```

---

## Step 6: Wrap Up

After saving, tell the user:

> Saved {X} ideas to `content-ideas/youtube-mining-{date}.md`.
>
> {count} ideas with strong Bridge connections, {count} without.
>
> Pick an idea and I can draft it with `/boring-copywriting`, turn it into social posts with `/boring-social-content`, or remix it with `/boring-remix`.

That's it. No recap of the process. No lecture on content strategy.

---

## Key Principles

- **One pass, full output.** Fetch → transcripts → ideas → save. No stopping to ask "should I continue?"
- **Research output, not published content.** No voice applied. No polishing. Raw strategic ideas.
- **Caching is non-negotiable.** Never re-download a transcript. Check the cache first, always.
- **Bridge-first when available.** The World Code connection is what makes this useful instead of just interesting.
- **Sequential channel processing.** Don't hammer YouTube with parallel requests.
- **3-5 quality ideas per video.** Restraint is the skill. Anyone can generate 50 mediocre ideas.
- **Draft hooks matter.** An idea without a hook is just a topic. Topics are cheap.
- **Don't explain the process.** The user doesn't need a play-by-play of "now I'm downloading transcripts." Just do it and show the results.

---

## Related Skills

- **boring-copywriting** — Draft full content from a mined idea
- **boring-social-content** — Turn ideas into platform-specific posts
- **boring-remix** — Generate multiple angles on a single idea
- **boring-content-strategy** — Broader content planning using mined insights
