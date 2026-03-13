---
name: obsidian-to-weixin
description: Find an Obsidian note by title/path with obsidian-cli, keep note content as Markdown, upload note images to Weixin, and create a Weixin draft via node-wxcli from Markdown stdin. Use when publishing Obsidian notes into Weixin draftbox.
---

# Obsidian to Weixin

## Config (Optional)

Set a default `author` in `~/.agents/config.yaml`:

```yaml
obsidian_to_weixin:
  author: "Alice Wang"
```

You can also set a global default:

```yaml
author: "Alice Wang"
```

## Workflow (Sequential)

1. Resolve vault path and note path/title using `obsidian-cli`.
2. Read note file as Markdown (no Notion export/conversion).
3. Ensure `author` exists in front matter (and add visible byline if needed).
4. Upload note images to Weixin (`material image`) and replace Markdown image URLs.
5. Prepare `thumb_media_id`:
   - Use the **first image in note order** as Weixin cover (`material thumb`).
   - If note has no image, fallback to the **latest Weixin image material ID**.
6. Generate `digest` with AI summarization (if user did not provide one).
7. Create Weixin draft from Markdown stdin via `node-wxcli draft add --format markdown --css-path ...`.

## Inputs (Ask if missing)

- `note_path`: Obsidian note path from vault root (recommended), e.g. `Projects/Weekly Update.md`.
- `note_title`: title/name to search when `note_path` is missing.
- `author`: optional, fallback from `~/.agents/config.yaml`.
- `css_path`: required when using `--format markdown`; if missing, default to `assets/default.css`.
- `thumb_media_id`: only needed if first-image + fallback both fail.
- `digest`: optional user-provided summary; if missing, generate via AI from the final Markdown.

## Prerequisites

- `obsidian-cli` installed and default vault configured.
- `node-wxcli` installed and authenticated.
- `curl` + `jq` available.

## Step 1: Resolve note from Obsidian

Get default vault path:

```bash
vault_path=$(obsidian-cli print-default --path-only)
```

If `note_path` is provided, use it directly.

If only `note_title` is provided, search candidates and confirm exact note:

```bash
obsidian-cli search "<note_title>"
obsidian-cli search-content "<note_title>"
```

Then resolve final path (from search result / user confirmation), and read file:

```bash
cat "$vault_path/<note_path>" > <workdir>/note.md
```

## Step 2: Keep Markdown as source

Obsidian notes are already Markdown. Do **not** run any Notion export or Notion-to-Markdown conversion.

## Step 3: Author handling

- If `author` is missing, read from `~/.agents/config.yaml`.
- Ensure front matter contains `author` if your workflow requires it.

## Step 4: Process images and replace URLs

Supported image references:

- Markdown image: `![alt](path-or-url)`
- Obsidian embed: `![[image.png]]`

Process in note order:

1. Parse image references from `<workdir>/note.md`.
2. Resolve each image file:
   - local relative paths -> absolute file path (based on note dir/vault)
   - remote URL -> download to temp file
3. Upload to Weixin image material:

```bash
node-wxcli material upload --type image --file <image-file> --json | jq -r '.url'
```

4. Replace original image target with returned Weixin URL.
5. Rewrite `![[...]]` to standard markdown image form:

```markdown
![image](<weixin-url>)
```

## Step 5: Prepare `thumb_media_id`

### 5.1 Primary: first image in note as cover

Take the **first image reference** (top-to-bottom), resolve file/download if needed, then upload as thumb:

```bash
thumb_media_id=$(node-wxcli material upload --type thumb --file <first-image-file> --json | jq -r '.media_id')
```

### 5.2 Fallback: latest Weixin image material

If note has no image:

```bash
image_count=$(node-wxcli material count --json | jq -r '.image_count')
offset=$((image_count - 1))
thumb_media_id=$(node-wxcli material list --type image --offset "$offset" --count 1 --json | jq -r '.item[0].media_id')
```

If no image materials exist, ask user to provide/upload cover and pass `--thumb-media-id`.

## Step 6: Build `digest` with AI summarization

If `digest` is not provided, summarize the final Markdown content with AI and generate a concise Chinese digest:

- 1-2 sentences
- Prefer 60-120 Chinese characters
- Plain text only (no Markdown / emoji / line breaks)
- Focus on the article purpose and key outcomes

## Step 7: Create draft from Markdown stdin

When using Markdown format, always pass `--css-path`. If `css_path` is missing, set:

```bash
css_path=${css_path:-assets/default.css}
```

```bash
node-wxcli draft add \
  --title "<note_title_or_custom_title>" \
  --author "<author>" \
  --digest "<digest>" \
  --format markdown \
  --content - \
  --css-path <css_path> \
  --need-open-comment=1 \
  --only-fans-can-comment=0 \
  --thumb-media-id "$thumb_media_id" < <workdir>/note.md
```

## Resources

- `references/cli-commands.md`: canonical command snippets (`obsidian-cli` + `node-wxcli`).
- `assets/default.css`: default CSS for `--format markdown` (`--css-path`).

## Notes

- Prefer `note_path` over `note_title`.
- Only use manual `--thumb-media-id` when first-image and fallback both fail.
