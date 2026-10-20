---
name: youtube-transcript-note
description: Create a structured Obsidian vault note from a YouTube video transcript — fetches captions with timestamps, cleans the text, divides into sections, adds a TOC and per-section video links, takes the thumbnail URL directly, and commits. Use when the user shares a YouTube URL and wants a full transcript note in the vault.
---

## YouTube Transcript Note Workflow

Given a YouTube URL, run the following steps in order.
Carry outputs forward — do not prompt the user between steps unless a step fails.

### Step 1: Fetch the timestamped transcript

Run `benevolentbadger` with SRT format to get captions with timestamps:

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/benevolentbadger benevolentbadger --format srt "<youtube_url>"
```

Save the full SRT output — you will need the timestamps in step 5.

Also run with plain text to get the raw transcript for cleaning:

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/benevolentbadger benevolentbadger "<youtube_url>"
```

### Step 2: Clean the transcript

This is a transcription task, NOT a summarization task.
Every piece of spoken content must appear in the output — do not skip, condense, or summarize any portion of the transcript.
If the transcript is long, output all of it.

Apply these rules to the plain-text transcript:

- Correct all spelling errors
- Fix grammatical mistakes (subject-verb agreement, tense consistency, etc.)
- Add proper punctuation (periods, commas, apostrophes, contractions)
- Capitalize proper nouns and sentence beginnings
- Place each complete sentence on its own line
- Separate each sentence with a blank line
- Combine fragmented phrases into complete, coherent sentences
- Remove filler words (um, uh, like, you know, so, kinda, gonna, wanna — replace contractions like "gonna" with "going to")
- Remove false starts and repeated words
- Remove narrator labels like `[Narrator]`, stage directions like `(laughing)`, and any trailing URLs

### Step 3: Divide into sections

Read the cleaned transcript and identify 4–7 natural topic breaks.

Every sentence from the cleaned transcript must appear under exactly one section — nothing may be dropped or omitted.

For each section:
- Write a `##` heading that names the topic (title case, concise)
- Place ALL cleaned sentences for that topic under the heading

Using the SRT output from step 1, find the `start` time (in seconds) for the first caption that falls under each section.
Add the video timestamp URL as a bare link on the line immediately after the `##` heading:

```
## Section name

https://youtu.be/<VIDEO_ID>?t=<seconds>s

First sentence of section.
```

### Step 4: Build the TOC

At the top of the body (before the first `##` section), add a table of contents using Obsidian wikilink heading format — not standard markdown anchors:

```
## Table of contents

- [[#Section one]]
- [[#Section two]]
- [[#Section three]]
```

### Step 5: Take the thumbnail URL directly

YouTube already hosts the thumbnail at a stable URL, so do not run the `social-to-imgur` skill here.

Build the URL from the video id: `https://i.ytimg.com/vi/<VIDEO_ID>/maxresdefault.jpg`

The Imgur round trip adds nothing for YouTube and runs into the egress-IP 429. Instagram and other platforms with expiring CDN URLs still need the upload.

### Step 6: Derive the vault filename

Convert the video title to a vault-safe filename:

- All lowercase
- Words separated by spaces (no hyphens or underscores)
- Strip special characters (pipes, colons, slashes, etc.)

Prefix with the channel/creator name when it helps distinguish the note.
Example: `tasty kitchen cast iron skillet care and cooking.md`

### Step 7: Write the vault note

Write the note to `/Users/mtm/Documents/Obsidian Vault/<filename>.md` with this structure:

```
---
tags:
  - <relevant-tag>
pic: https://i.ytimg.com/vi/<VIDEO_ID>/maxresdefault.jpg
---

![<filename without .md>](https://i.ytimg.com/vi/<VIDEO_ID>/maxresdefault.jpg)

https://youtu.be/<VIDEO_ID>

<intro sentences — any content before the first natural section break>

## Table of contents

- [[#Section one]]
...

## Section one

https://youtu.be/<VIDEO_ID>?t=<seconds>s

<sentences>

## Section two

https://youtu.be/<VIDEO_ID>?t=<seconds>s

<sentences>
```

Rules:
- No `# Title` heading — the filename is the title in Obsidian
- Tags: use only pre-existing vault tags; do not mint new ones without user approval
- One sentence per line, blank line between sentences throughout
- No italics or bold anywhere in the file
- Link named products to their local vault page (e.g. `[[flaxseed oil]]`) if one exists, or to a Google Image Search URL otherwise

### Step 8: Commit

Stage and commit the new file:

```
git add "<filename>.md"
git commit -m "Add <short topic> note from YouTube transcript"
```

Run each git command as a separate Bash call (no chaining with &&).

### Step 9: Apply recipe cleanup (cooking/recipe content only)

Assess whether the video content is recipe or cooking-focused by examining any of the following signals:

- The video title contains words like: recipe, sauce, how to make, cooking, bake, roast, stir-fry, marinade, dipping, dumpling, noodle, soup, fry, etc.
- The channel name is associated with food or cooking
- The transcript contains ingredient measurements, quantities, or cooking technique vocabulary

If any signal indicates recipe/cooking content, invoke the `recipe-cleanup` skill, passing the path to the vault note just written:

```
/recipe-cleanup <absolute path to vault note>
```

The skill will fetch the printable recipe from the YouTube description (if one exists), add structured `### Ingredients` checklists and `### Instructions` blocks, update frontmatter with a `creator` field, and resolve ingredient wikilinks.

After the skill completes, commit the updated file:

```
git add "<filename>.md"
git commit -m "Apply recipe cleanup to <short topic> note"
```

If the content is not recipe or cooking-focused, skip this step entirely — do not invoke `recipe-cleanup`.

### Final report

After all steps complete, report:
- The vault note filename
- The i.ytimg.com thumbnail URL
- The section breakdown with their video timestamps
- Whether recipe cleanup was applied
