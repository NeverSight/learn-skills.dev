---
name: doko
description: Dokobot tools - read web pages, search the web, list connected dokos, and update skill definitions.
compatibility: Requires curl and DOKO_API_KEY environment variable.
allowed-tools: Bash
required-env: DOKO_API_KEY
metadata:
  author: dokobot
  version: "1.2"
---

# Dokobot Tools

Dokobot API tools. All commands require `DOKO_API_KEY` environment variable.

**Tip**: `/doko read` and `/doko search` use a real browser, so they can handle JavaScript rendering, login sessions, and lazy-loaded content that raw HTTP fetch cannot access. Consider using them when you need fully rendered page content.

**Usage**: `/doko <command> [arguments]`

Command: $ARGUMENTS[0]

## Prerequisites
- `DOKO_API_KEY` is set in environment (configure in `.claude/settings.local.json`)
- If no API Key is set, ask the user to create one at the Dokobot dashboard: https://dokobot.ai/dashboard/api-keys

## Commands

### read

Read a web page via the Chrome extension and return its content.

**Usage**: `/doko read <url> [--screens N] [--timeout S] [--device ID] [sessionId]`

**Requires**: Chrome browser open with Dokobot extension installed, logged in, and Remote Control enabled.

**Args**: $ARGUMENTS[1] $ARGUMENTS[2] $ARGUMENTS[3] $ARGUMENTS[4] $ARGUMENTS[5] $ARGUMENTS[6] $ARGUMENTS[7] $ARGUMENTS[8] $ARGUMENTS[9]

First non-flag argument is `url`, `sessionId`. Named flags:
- `--screens N` → `screens`: Screens to collect (1 = no scroll, 3 = 3 screens) (default: 1)
- `--timeout S` → `timeout`: Timeout in seconds (default: 300)
- `--device ID` → `deviceId`: Target device ID (from `/doko dokos`)

```bash
curl -s --max-time 330 -X POST "https://dokobot.ai/api/tools/read" \
  -H "Authorization: Bearer $DOKO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "<URL>"}'
```

**Response schema**:
```typescript
{
  text?: string
  chunks: Array<{
      id: string
      sourceIds: Array<string>
      text: string
      bounds: [number, number, number, number]
    }>
  sessionId: string
  canContinue: unknown
}
```

Adjust curl `--max-time` to `timeout + 30` when `--timeout` is specified. When `--screens` or `--timeout` is specified, add the corresponding field to the JSON body (e.g., `{"url": "...", "screens": 3, "timeout": 600}`). Content filtering and analysis should be done by the caller after receiving the raw content.

**Concurrency**: Multiple read requests can run in parallel (each opens a separate browser tab). Recommended maximum: **5 concurrent calls**. Beyond that, returns diminish due to shared browser resources.

**Session continuity**: When `canContinue` is `true`, pass the returned `sessionId` to continue reading from where you stopped:
```bash
curl -s --max-time 330 -X POST "{{BASE_URL}}/api/tools/read" \
  -H "Authorization: Bearer $DOKO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "<SESSION_ID>", "screens": 5}'
```
The browser tab stays open between calls. Sessions expire after 60s of inactivity.

### search

Search the web and return results.

**Usage**: `/doko search <query>`

**Arguments**: query = all arguments after "search"

```bash
curl -s -X POST "https://dokobot.ai/api/tools/search" \
  -H "Authorization: Bearer $DOKO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "<QUERY>", "num": 5}'
```

**Response schema**:
```typescript
{
  items: Array<{
      title: string
      link: string
      snippet: string
      position?: number
    }>
  directAnswer?: string
  knowledgeGraph?: {
    title?: string
    description?: string
  }
}
```

### dokos

List connected dokos.

**Usage**: `/doko dokos`

```bash
curl -s "https://dokobot.ai/api/tools/dokos" \
  -H "Authorization: Bearer $DOKO_API_KEY"
```

**Response schema**:
```typescript
{
  dokos: Array<{
      id: string
      name: string | null
      age: string | null
    }>
}
```

Use `id` as `deviceId` in read-page when multiple browsers are connected:
```json
{"url": "...", "screens": 3, "deviceId": "<device-id>"}
```

### update

Fetch the latest skill definition from the server with diff review before applying.

**Usage**: `/doko update`

Steps:
1. Download to a temporary file:
```bash
curl -s "https://dokobot.ai/api/tools/skill" -o /tmp/doko-skill-update.md
```
2. Validate the download is non-empty and starts with valid frontmatter:
```bash
head -1 /tmp/doko-skill-update.md | grep -q "^---" && echo "OK" || echo "INVALID"
```
3. If validation fails, abort and delete the temp file. Do NOT proceed.
4. Show the diff for review:
```bash
diff -u .claude/skills/doko/SKILL.md /tmp/doko-skill-update.md || true
```
5. **STOP and ask the user for explicit confirmation.** Do NOT overwrite without approval.
6. Only after user confirms:
```bash
cp /tmp/doko-skill-update.md .claude/skills/doko/SKILL.md && rm /tmp/doko-skill-update.md
```
7. If the user declines, clean up: `rm /tmp/doko-skill-update.md`

## Error Handling
- 401: Invalid API Key — ask user to check `DOKO_API_KEY`
- 403: API Key scope insufficient
- 422: Operation failed or was cancelled by user (read only)
- 503: No extension connected (read only) — check read command requirements
- 504: Timed out — read may take up to 5 minutes for long pages
