---
name: codebase-skill
description: "Codebase.blog auto-posting via MCPorter + OAuth. Trigger words: 자동포스팅, 자동포스팅해, 포스팅해줘, 블로그 포스팅해줘, 글 발행해줘, create post, publish post. Route rule: skill로 -> mcporter (/mcp-remote), mcp로 -> direct MCP (/mcp), ambiguous defaults to skill."
---

# Codebase.blog Auto-Posting (MCP + MCPorter)

This skill is **OAuth-first** and intended to be used via `mcporter` so non-developers can run blog auto-posting as plain commands.

## What This Skill Does

- Authenticate once via OAuth (browser)
- Call MCP tools like normal commands
- Publish posts with `create_post`
- Optional image upload via presigned URL (`get_image_upload_url` -> `curl PUT` -> `finalize_uploaded_image`)

## Trigger Phrases

- 자동포스팅
- 자동포스팅해
- 포스팅해줘
- 블로그 포스팅해줘
- 글 발행해줘
- create post
- publish post

## Routing Contract (Skill vs MCP Direct)

Use explicit user intent to choose one execution path. Do not mix both in one run.

### Route Selection

- `skill` route (via `mcporter`): if user says `codebase-skill`, `skill 사용`, `skill로`, `스킬로`, or uses style flags like `--podcast`, `--research`, `--tutorial`.
- `mcp` route (direct MCP tools): if user says `mcp로`, `MCP tool`, `codebase-blog-mcp`, `툴로 직접`.
- ambiguous phrase only (for example: `자동포스팅해`): default to `skill` route.
- user can always override by adding one explicit token: `skill로` or `mcp로`.

### Route Guard

Before `create_post`, always run `check_auth` and validate the expected auth mode:

- `skill` route expected output: `인증 방식 : OAuth 2.1`
- `mcp` route expected output: `인증 방식 : API Key`

If mismatch:

1. retry once on the correct route
2. if still mismatched, stop and report route mismatch (do not post)

### Preflight Log Line (required)

Print one route line before tool execution:

- skill route: `[Route] mode=skill transport=mcporter endpoint=/mcp-remote alias=codebase-blog-oauth`
- mcp route: `[Route] mode=mcp transport=direct endpoint=/mcp server=codebase-blog-mcp`

## Setup (Once)

```bash
# DEV (DEFAULT for this skill)
# - Safe default: prevents accidental production posting while testing.
npx -y mcporter config add codebase-blog-oauth \
  --url http://localhost:3002/mcp-remote \
  --auth oauth \
  --allow-http \
  --oauth-redirect-url http://127.0.0.1:33334/callback \
  --scope project

# PROD (explicit opt-in)
npx -y mcporter config add codebase-blog-oauth-prod \
  --url https://mcp.codebase.blog/mcp-remote \
  --auth oauth \
  --oauth-redirect-url http://127.0.0.1:33333/callback \
  --scope home

# Browser OAuth (first time only)
npx -y mcporter auth codebase-blog-oauth
```

## Verify (Always First)

> Important: treat `check_auth` as the real success gate. Do not rely on the browser page text alone.

```bash
npx -y mcporter call codebase-blog-oauth.check_auth
```

## Safe Gate (Recommended)

`mcporter` may print errors without a non-zero exit code. Gate on the presence of `"error"` in the output before posting.

```bash
AUTH_OUT=$(npx -y mcporter call codebase-blog-oauth.check_auth --output json 2>&1 || true)
echo "$AUTH_OUT"

if echo "$AUTH_OUT" | grep -q '"error"'; then
  echo "[STOP] OAuth verification failed. create_post not executed."
  exit 1
fi
```

## Publish

```bash
npx -y mcporter call 'codebase-blog-oauth.create_post(
  title: "자동포스팅 테스트",
  content_markdown: "## Hello\\n\\nmcporter로 발행한 글입니다.",
  category: "Tech",
  tags: ["mcp","mcporter","automation"]
)'
```

## Writing Style Guide (Optional)

```bash
npx -y mcporter call 'codebase-blog-oauth.get_writing_style_guide(style: "default")'
```

## Image Upload (Optional)

```bash
# 1) ask for presigned URL
npx -y mcporter call 'codebase-blog-oauth.get_image_upload_url(mimeType: "image/webp", fileSize: 245760)'

# 2) upload with curl PUT (use uploadUrl from step 1)
curl -X PUT -H "Content-Type: image/webp" -T ./cover.webp "UPLOAD_URL_FROM_PREVIOUS_STEP"

# 3) finalize upload
npx -y mcporter call 'codebase-blog-oauth.finalize_uploaded_image(fileKey: "uploads/...", mimeType: "image/webp", fileSize: 245760)'
```

## Troubleshooting

- If the login UI does not appear: you may already be logged in. Try a private window or `npx -y mcporter auth codebase-blog-oauth --reset`.
- If you see `SSE error: Invalid content type, expected "text/event-stream"` during `mcporter auth`: tokens may still be saved. Run `check_auth` to confirm.
- If port `33333` is in use: pick another fixed callback port and re-add the server.
