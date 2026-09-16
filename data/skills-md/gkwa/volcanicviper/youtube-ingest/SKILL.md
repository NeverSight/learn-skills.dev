---
name: youtube-ingest
description: Full YouTube video ingestion workflow — given a YouTube URL, fetch the video title, take the thumbnail URL directly, create a note in the Obsidian vault with a hero image, and commit it. Use when the user shares a YouTube URL and wants a permanent note in the vault.
---

## YouTube Ingest Workflow

Given a YouTube URL (e.g. `https://youtu.be/0EHFgu7V7N4`), run the following steps in order.
Carry outputs forward — do not prompt the user between steps unless a step fails.

### Step 1: Fetch video metadata

Run yt-dlp to get the video title:

```
uvx yt-dlp --get-title "<youtube_url>"
```

Collect from the output:
- The video title

Also fetch the page to identify the channel name and a one-sentence summary of the topic.
Use WebFetch on the canonical YouTube watch URL with a prompt asking for title, channel, and topic.

### Step 2: Take the thumbnail URL directly

YouTube already hosts the thumbnail at a stable URL, so do not run the `social-to-imgur` skill here.

Build the URL from the video id: `https://i.ytimg.com/vi/<VIDEO_ID>/maxresdefault.jpg`

Use that for both `pic:` and the hero image.

The Imgur round trip adds nothing for YouTube and runs into the egress-IP 429. Instagram and other platforms with expiring CDN URLs still need the upload.

### Step 3: Derive the vault filename

Convert the video title to a vault-safe filename:
- All lowercase
- Words separated by spaces (no hyphens or underscores)
- Strip special characters (pipes, colons, slashes, etc.)
- Strip filler words that add no meaning (e.g. "how to", "a", "the") only when the result is still descriptive

Example: "How To Make Dumpling Wrappers From Scratch | KitchenAid Pasta Attachment"
becomes: `dumpling wrappers from scratch kitchenaid pasta attachment.md`

### Step 4: Write the vault note

Write the note to `/Users/mtm/Documents/Obsidian Vault/<filename>.md` with this structure:

```
<youtube_url>

![hero](https://i.ytimg.com/vi/<VIDEO_ID>/maxresdefault.jpg)
```

No frontmatter is needed unless the user asks for it.

### Step 5: Commit

Stage and commit the new file:

```
git add "<filename>.md"
git commit -m "Add <short topic> note with YouTube link and hero image"
```

Run each git command as a separate Bash call (no chaining with &&).

### Final report

After all steps complete, report:
- The vault note filename
- The i.ytimg.com thumbnail URL
- The original YouTube URL
