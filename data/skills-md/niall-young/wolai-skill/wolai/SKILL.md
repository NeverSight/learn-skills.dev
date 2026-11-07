---
name: wolai
description: Route Wolai page work through the configured wolai MCP and upload prepared local media as real Wolai blocks. Use whenever a prompt contains a wolai.com URL; asks to read, summarize, search, create, edit, publish, or delete Wolai content; or asks to place pasted screenshots, message attachments, downloaded files, local images/videos, or AI-generated media into Wolai. Treat phrases such as “这是准备好的物料”, “使用我粘贴的图片”, and “把这些图放进去” as explicit authorization to use the current message's media. Never replace an upload with web scraping, a text link, bookmark, external media link, or embed.
---

# Wolai

Use the wolai MCP for every Wolai page operation. Use the bundled upload workflow when local media must become a real Wolai media block.

## Resolve MCP Access Silently

1. If native Wolai MCP tools are available in the current task, call them directly.
2. If native Wolai tools are absent, do not tell the user that tools are unavailable or that the MCP may be disconnected. Immediately call the same configured MCP with `scripts/call-mcp.py`, for example:

   ```bash
   python3 <skill-directory>/scripts/call-mcp.py get_doc \
     --arguments-json '{"doc_id":"PAGE_ID"}'
   ```

   Use `--list-tools` only when the available tool names or schemas must be confirmed.
3. Do not create a task-local MCP bridge or read credentials directly from configuration files. The bundled client resolves the connection with `codex mcp get` and keeps authorization private.
4. User-facing progress may say that Wolai MCP is reading the page, but must not expose native tool-injection state. Only report the actual MCP configuration, authentication, connection, access, or tool error after the bundled fallback also fails.

## Route Wolai URLs

1. Recognize `wolai.com` and `www.wolai.com` URLs before considering browser or web tools.
2. Strip the query, fragment, and trailing slash. Treat the final non-empty path segment as the page/document ID and preserve its case.
3. Call `get_doc` first through the native tool or bundled fallback to validate the ID and access.
4. For content, call `get_page_outline`, then read only the needed sections with `get_section_content`, using the same access path.
5. For edits, read the affected content first. Prefer `rewrite_section`, `insert_under_heading`, `move_section`, or `delete_section`; use block-level tools only for precision work.
6. Stop and report the MCP/configuration/access error if validation fails. Do not silently fall back to web scraping.

## Handle Prepared Media

Use media only when the user's words indicate that the attached or pasted items are material for the Wolai task. Do not infer upload intent merely because a message contains an attachment.

Preserve the current-message order when the user authorizes multiple items. Resolve each item in this order:

1. Use the local path supplied for the current message attachment.
2. If a pasted screenshot has no usable path, immediately run `scripts/save-clipboard-image.py` to create a private temporary PNG.
3. Use the local path produced by a completed download or generation task.
4. If no local bytes can be obtained, ask the user to paste or attach the item again. Never guess or substitute it.

Before any media upload, read [references/media-upload.md](references/media-upload.md) completely and follow it. Upload local bytes with `scripts/upload-media.py`; do not pass large Base64 strings through chat or a model-authored tool argument.

## Choose the Destination

- When the user names a heading or location, use the outline to resolve its section ID and upload with `--page-id` plus `--section-id`.
- When the user explicitly says to append to the page, upload with `--parent-id` set to the page ID.
- When placement is material but cannot be inferred safely, ask before writing.
- Check the upload result. Do not claim success unless the MCP response succeeds.

## Enforce Media Rules

- Create `image`, `video`, `audio`, or `file` blocks from local bytes only.
- Never use `link`, `embed`, or `bookmark` as a substitute for an upload.
- Reject missing, empty, unreadable, extensionless, or larger-than-500-MB files.
- Remove only temporary clipboard files created for this task, and only after success or a terminal failure. Preserve user attachments and source files.
- If Wolai rejects the file because of format, permissions, storage quota, or plan limits, report the actual failure and stop.
