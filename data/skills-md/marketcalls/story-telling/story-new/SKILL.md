---
name: story-new
description: Create a new story video from a context. Writes story.json, gets the script approved, then generates the Sarvam voiceover and FLUX 2 artwork and renders the mp4.
argument-hint: "[slug] [context] [seconds] [orientation]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

Turn a context into a finished narrated video.

## Arguments

Parse `$ARGUMENTS` as: slug context seconds orientation

- `$0` = slug, lowercase and hyphenated, e.g. `big-bull`. Becomes the folder
  under `public/` and, in PascalCase, the composition id
- `$1` = context: a file path, a URL already fetched, or the text itself
- `$2` = length in seconds. Default 60
- `$3` = `landscape` or `vertical`. Default `landscape`

If no arguments, ask what the video is about, how long it should be, and where
it will be published.

## Instructions

0. Check the pipeline is present, since the skills can be installed without it:

   ```bash
   test -f cli/generate.ts && test -f src/Root.tsx && echo present || echo missing
   ```

   If missing, run the `story-setup` skill first. It fetches the project,
   installs dependencies, creates `.env` and verifies the keys. Everything
   below runs from the project root.
1. Read the `story-telling` rules before writing anything:
   `rules/story-formats.md` to pick the shape, `rules/narration.md` for the
   script, `rules/images.md` for the prompts, `rules/pitfalls.md` for the
   checklist.
2. Pick the format from `rules/story-formats.md` and start from the matching
   template in `rules/assets/<format>/story.json`. Copy it to
   `public/<slug>/story.json` and change `slug` and `compositionId` first.
3. Write the narration from the context:
   - Scene count is roughly seconds divided by ten, clamped 3 to 10
   - 24 to 32 words per scene
   - Numbers spelled as words; digits only on `stat` cards
   - Every fact traceable to the given context, nothing invented
   - Note any contradiction in the source and say which reading was used
4. Write the image prompts:
   - Scene direction only. The house style lives in `style.artPrompt`
   - Two images per scene for movement, one for a calmer feel
   - Never name a real person. If the user supplied reference photos, add them
     to `references` and set `reference` on those images, putting the likeness
     clause first in the prompt
   - Image ids unique across the whole story, and `outro.imageId` must be one
     of them
5. **Show the narration to the user and wait for approval.** Voices and images
   cost money; a wrong fact caught here is free.
6. Generate:
   ```bash
   npm run generate -- --slug <slug>
   ```
   This writes voices, images and the measured `durationInFrames` back into
   `story.json`. Existing files are skipped, so reruns are cheap.
7. Preview or render:
   ```bash
   npm run studio
   npx remotion render <CompositionId> out/<slug>.mp4 --codec h264
   ```
8. Verify before reporting: check the output exists and read its real duration
   rather than assuming the planned one.
9. Report scene count, total duration, image count, output path and size, plus
   any assumption made about an ambiguous fact.

## Fully automatic alternative

When the user wants no review step and has `OPENAI_API_KEY` set:

```bash
npm run story -- --slug big-bull --context ./article.md --seconds 60 --render
```

This drafts with OpenAI, generates, and renders in one pass. Quality of facts
is lower than a hand-written `story.json`, so prefer the reviewed path for
anything that will be published.

## Formats

| Format | Template | Length | Scenes |
|---|---|---|---|
| Biography | `assets/biography/story.json` | 60s | 6 |
| Concept explainer | `assets/explainer/story.json` | 60s | 6 |
| Vertical short | `assets/reel/story.json` | 30s | 3 |
| Numbered list | `assets/listicle/story.json` | 60s | 6 |
| News or event | `assets/news/story.json` | 45s | 5 |
| Myth versus fact | `assets/myth-buster/story.json` | 45s | 5 |

## Example usage

`/story-new big-bull ./article.md 60 landscape`
`/story-new repo-rate "Explain the repo rate to a first time borrower" 30 vertical`
`/story-new fed-cut ./notes/fed.md`
