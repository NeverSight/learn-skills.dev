---
name: flomo-web-crud
description: Query, insert, edit, and delete flomo memos through the flomo Web UI using Chrome MCP tools (no official API required). Use when a user wants CRUD operations on live flomo memos in an already logged-in browser session.
---

# Flomo Web CRUD

## Overview

Use Chrome MCP tools to operate on live flomo memos at `https://v.flomoapp.com/mine`.

This skill is for Web UI automation only. It does not depend on flomo official APIs.

Default behavior (v1):
- Full CRUD (`query/search`, `create/insert`, `edit`, `delete`)
- Text search first, but lock a target by `memo_id` before write actions
- `edit` defaults to full content replacement (`replace`)
- `delete` always requires explicit second confirmation
- Auto deep scan for search with default cap of `50` memos
- Minimal logging (do not persist memo body text)

## Preconditions

- User is already logged in to flomo Web in Chrome
- Chrome MCP is available and working in this Codex session
- Prefer desktop layout (wide viewport). Mobile layout is best-effort only.

## Use This Skill When

- The user asks to search or find live flomo memos
- The user asks to insert/create a flomo memo in their real account
- The user asks to edit/update an existing flomo memo
- The user asks to delete a flomo memo and accepts confirmation steps

## Do Not Use This Skill When

- The user only wants to process exported flomo HTML/archives (use `flomo-memo-to-markdown` instead)
- The user asks for batch operations across many memos (not v1)
- The user asks for attachment upload/edit support (not v1)

## Default Workflow (High Level)

1. Confirm Chrome MCP connectivity and switch to the flomo tab (or navigate to flomo).
2. For `query/edit/delete`, run search workflow and build memo candidates from visible memo cards/links.
3. If needed, deep-scan by scrolling and repeating reads up to the scan cap.
4. For write operations, lock the target by `memo_id` and present a confirmation step.
5. Execute UI actions with `chrome_read_page` refs first; refresh refs if they expire.
6. Validate the result by re-reading the page and summarizing the outcome.

## Safety Rules (Must Follow)

- `delete`: Always require explicit second confirmation before actual deletion.
- `edit` via text search: Require candidate confirmation before writing.
- Do not persist memo body text to local files.
- If target UI controls cannot be located reliably, stop and report a recoverable failure instead of guessing.

## Tool Priority

Use `mcp-chrome-global` Chrome MCP tools in this order of preference:

1. `chrome_switch_tab` / `chrome_navigate`
2. `chrome_read_page` (structured refs)
3. `chrome_get_web_content` (fast visible text read)
4. `chrome_click_element`, `chrome_fill_or_select`, `chrome_keyboard`
5. `chrome_screenshot` (debugging / visual confirmation)
6. `chrome_computer` (coordinate fallback, minimal use)
7. `chrome_request_element_selection` (human-in-the-loop fallback after repeated failures)

## Intent Mapping

### `query/search`

Return candidate memos with:
- `memo_id`
- visible timestamp text
- short snippet
- match reason

### `create/insert`

Insert a new memo through the top editor and report success with best-effort new `memo_id` detection.

### `edit`

Default mode is `replace` (replace full memo body). `append`/`prepend` are reserved optional modes and may be unsupported in v1 unless explicitly implemented during the run.

### `delete`

Delete a single target memo only after the user confirms the selected candidate.

## Candidate / Action / Result Shapes

Use these internal conventions in responses and reasoning (no code API required):

### `MemoCandidate`

- `memo_id: string`
- `timestamp_text: string`
- `snippet: string`
- `match_reason: string`
- `score?: number`

### `ActionPlan`

- `action: query | create | edit | delete`
- `target_query?: string`
- `target_memo_id?: string`
- `edit_mode?: replace | append | prepend`
- `scan_limit: number` (default `50`)
- `requires_confirmation: boolean`

### `ActionResult`

- `success: boolean`
- `action: string`
- `memo_id?: string`
- `matched_count?: number`
- `message: string`
- `warnings?: string[]`

## Follow-Up Questions (Ask Only When Needed)

Ask only if it changes the action materially:
- Multiple candidates match and a write action is requested
- The user did not provide new content for `create` or `edit`
- The user wants a scan cap larger than the default `50`
- The page layout is mobile or controls cannot be found reliably
- A destructive action (`delete`) reaches the final confirmation point

## References

- Workflow details: `references/workflows.md`
- UI locator strategy and fallback policy: `references/ui-locators.md`
- Safety and logging policy: `references/safety.md`
- Validation checklist: `references/test-checklist.md`
