---
name: wxarticle_creator
description: Draft Weixin official account articles from user draft.
metadata:
  short-description: Weixin draft via markdown-to-html-cli and wxcli
---

# WX Article Creator

Use this skill when the user asks to draft or create a Weixin official
account article (plain text or Markdown) and submit it as a draft.

---

## Inputs

- `draft`: User-provided draft text (plain or Markdown)
- `title`: Article title
- `thumb_media_id`: Weixin thumbnail media id for draft (optional, see Workflow)
- `thumb_image`: Path to thumbnail image file (optional, used if thumb_media_id not provided)
- `format`: Optional enum (`auto`, `markdown`, `plain`)

## Outputs

- `markdown`: Final markdown source
- `html`: Rendered HTML
- `wxcli_result`: Command output

---

## Rules

- Do not invent wxcli commands; use README-documented format.
- Always ask for user confirmation before running `wxcli`.
- Render HTML using exactly:
  `npx markdown-to-html-cli --source <SOURCE.md> --style=./style.css`
- CSS must be loaded from `skills/wxarticle_creator/style.css`.
- Preserve meaning; no new facts. Keep length within +/-10% when polishing.

---

## Workflow

1. Detect input format.
   - If `format=auto`, detect Markdown by headings (`#`), lists (`-`/`1.`), links,
     or code fences.
   - If Markdown is provided, keep it.
   - If plain text, convert it to Markdown with clear hierarchy.

2. Convert plain text to structured Markdown (if needed).
   - Use the provided `title` as an H1.
   - Derive H2 sections from topic shifts or leading phrases.
   - Use H3 for subtopics, and bullet/numbered lists for enumerations.
   - Keep original ordering and meaning.

3. Polish Markdown lightly.
   - Fix typos and improve readability.
   - Keep structure; do not add new facts.

4. Handle thumbnail (thumb_media_id):
   - **If `thumb_media_id` is provided**: Use it directly.
   - **If `thumb_image` is provided** (path to image file):
     - Upload the image: `wxcli material upload --type image --file "<thumb_image>"`
     - Extract the returned `media_id` from the output.
   - **If neither is provided**:
     - Get the latest image from materials: `wxcli material list --type image --offset 0 --count 1 --json`
     - Extract the `media_id` from the first item.
     - If no images exist, inform the user and proceed without thumb_media_id.

5. Write Markdown source to a temporary file in a temp directory.
   - Create a temp directory (e.g., `/tmp/wxarticle_creator-<YYYYMMDD-HHMMSS>`).
   - Save as `<TMP_DIR>/article-<YYYYMMDD-HHMMSS>.md` (or another `<SOURCE.md>`).
   - Remove the temp directory after HTML is generated, unless the user requests it.

6. Convert Markdown to HTML with the CLI.
   - Copy `skills/wxarticle_creator/style.css` into the temp directory as `style.css`.
   - Run the command from the temp directory so `./style.css` resolves.
   - Command:
     `npx markdown-to-html-cli --source <SOURCE.md> --style=./style.css`
   - Capture stdout as HTML output.
   - Ensure the content is wrapped in `<div id="nice">...</div>` if it is not
     already, so the stylesheet applies.

7. User confirmation.
   - Show polished markdown and a rendered HTML snippet.
   - If thumb_media_id was auto-fetched, mention which image is being used.
   - Ask: "Proceed to create Weixin draft with wxcli?"

8. Submit via wxcli.
   - Include `--thumb-media-id <thumb_media_id>` only if available.
   - Direct content:
     `wxcli draft add --title "<title>" --content "<html>" --thumb-media-id <thumb_media_id>`
   - From pipeline:
     `npx markdown-to-html-cli --source <SOURCE.md> --style=./style.css | wxcli draft add --title "<title>" --content - --thumb-media-id <thumb_media_id>`
   - Return output to the user.

---

## Failure Handling

- If thumbnail upload fails, show the error and ask to retry or proceed without thumbnail.
- If getting latest image fails, inform the user and proceed without thumb_media_id.
- If the CLI conversion fails, show the error and ask to retry.
- If `wxcli` fails, show the error output and ask whether to retry or adjust inputs.
