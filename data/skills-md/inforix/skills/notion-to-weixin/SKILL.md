---
name: notion-to-weixin
description: Fetch a Notion page by title, export to Markdown, convert Markdown to HTML with a user-provided CSS file, and create a Weixin draft via wxcli. Use when asked to publish Notion content into Weixin draftbox, or when moving Notion pages into Weixin draft as HTML.
---

# Notion to Weixin

## Config (Optional)

Set a default `author` in `~/.agents/config.yaml`:

```yaml
notion_to_weixin:
  author: "Alice Wang"
```

You can also set a global default:

```yaml
author: "Alice Wang"
```

## Workflow (Sequential)

1. Resolve Notion page ID from the given title.
2. Export the page to Markdown.
3. Ensure `author` exists in Markdown front matter (and inject a byline if needed).
4. Process images (upload to Weixin and replace URLs in Markdown).
5. Prepare `thumb_media_id`:
   - If the Notion page has a cover, upload it as a Weixin `thumb` material and use that ID.
   - If no cover, use the last image material ID.
6. Create a new Weixin draft using Markdown input (wxcli converts to HTML, optional CSS).

## Inputs (Ask the user if missing)

- `notion_title`: exact Notion page title to publish.
- `author`: optional author name (used for Markdown front matter and wxcli `--author`). If missing, read from `~/.agents/config.yaml`.
- `css_path`: optional CSS file path (wxcli `--css-path` inlines styles). You can use `assets/default.css`.
- `thumb_media_id`: only required if cover and image fallback both fail.

## Prerequisites

- `notion-cli` installed and authenticated (NOTION_TOKEN or `notion auth set`).
- `wxcli` installed and authenticated (`wxcli auth set` or `wxcli auth login`).
- `curl` and `jq` available.

## Step 1: Resolve Page ID by Title

1. Copy `references/notion-search.json` to a temp file and replace `__TITLE__`.
2. Run `notion search --body @query.json`.
3. Choose the exact-title match. If multiple matches remain, pick the most recently edited or ask the user to confirm.
4. If no match is found, ask for a Notion page ID or URL and extract the ID.

## Step 2: Export Page to Markdown

- Use `notion pages export <page_id> --assets=download -o <workdir>/page.md` when the page contains images.
- Use a workdir like `/tmp/notion-to-weixin/<slug-or-timestamp>`.

## Step 3: Default Author Handling

- If `author` is not provided, read it from `~/.agents/config.yaml`.
- Ensure `author` exists in Markdown front matter (and add a byline if you want it visible in content).



## Step 4: Process Images (Recommended)

If the Notion page contains images, upload them to Weixin and replace Markdown image URLs
so they remain valid for draft rendering.

1. Find image links in `<workdir>/page.md`. Notion exports local images under the assets folder.
2. For each local image file, upload it and capture the `url`:

```bash
wxcli material upload --type image --file <workdir>/assets/<image-file> --json | jq -r '.url'
```

3. Replace the Markdown image URL with the returned `url`:

```markdown
![alt](<weixin-url>)
```

If you skip this step, images that reference local files or expiring Notion URLs may not render in Weixin.

## Step 5: Prepare `thumb_media_id`

### 5.1 If Notion page has a cover

1. Fetch page metadata (use notion-cli):

```bash
notion pages get <page_id> > <workdir>/page.json
```

2. Extract cover type + cover URL:

```bash
cover_type=$(jq -r '.cover.type // ""' <workdir>/page.json)
cover_url=$(jq -r '.cover | if .==null then "" elif .type=="external" then .external.url else .file.url end' <workdir>/page.json)
```

3. If cover type is `file`, download via notion-cli; if `external`, use curl:

```bash
if [ "$cover_type" = "file" ]; then
  jq -c '.cover' <workdir>/page.json | notion files read --body @- --output <workdir>/cover.jpg
else
  curl -L "$cover_url" -o <workdir>/cover.jpg
fi
thumb_media_id=$(wxcli material upload --type thumb --file <workdir>/cover.jpg --json | jq -r '.media_id')
```

Note: Notion file URLs expire quickly. If download fails, re-fetch page metadata and retry.

### 5.2 If no cover exists

1. Get image material count:

```bash
image_count=$(wxcli material count --json | jq -r '.image_count')
```

2. If `image_count > 0`, fetch the last image and use its `media_id`:

```bash
offset=$((image_count - 1))
thumb_media_id=$(wxcli material list --type image --offset "$offset" --count 1 --json | jq -r '.item[0].media_id')
```

3. If no images exist, ask the user to provide a `thumb_media_id` or upload a thumb manually.

## Step 6: Create Weixin Draft (Markdown input)

```bash
wxcli draft add \
  --title "<notion_title>" \
  --author "<author>" \
  --content - \
  --css-path <css_path> \
  --need-open-comment=1 \
  --only-fans-can-comment=0 \
  --thumb-media-id "$thumb_media_id" < <workdir>/page.md
```

If your wxcli build requires an explicit flag to indicate Markdown input, add it to the command.

Recommended (explicit format):

```bash
wxcli draft add \
  --title "<notion_title>" \
  --author "<author>" \
  --format markdown \
  --content - \
  --css-path <css_path> \
  --need-open-comment=1 \
  --only-fans-can-comment=0 \
  --thumb-media-id "$thumb_media_id" < <workdir>/page.md
```

- If you need machine-readable output, add `--json` and capture the returned `media_id`.


## Resources

- `references/notion-search.json`: JSON template for Notion title search.
- `references/cli-commands.md`: Canonical CLI command examples for `notion-cli` and `wxcli`.
- `assets/default.css`: Default CSS theme (optional; pass via `--css-path`).

Notes:
- Use `--page-id` if the title search is ambiguous.
- Use `--thumb-media-id` only if cover and image fallback are unavailable.
