---
name: confluence-api-doc
description: 'Sync API documentation from a Markdown file to Confluence pages using acli + REST API. Prompts for Confluence URL, API doc file path, and credentials at runtime — no pre-configured environment variables required. Use this skill whenever: uploading or syncing API docs to Confluence, updating Confluence pages from a Markdown file, publishing documentation, "sync api doc", "push doc to confluence", "อัปเดต api doc ไป confluence", "sync confluence pages", "confluence-api-doc", or when the user wants to publish or update any Markdown-based documentation to Confluence.'
---

# Confluence API Doc Sync

Sync API documentation from a single Markdown file to Confluence — **one API per page**. When a Markdown file documents multiple APIs, split it into individual Confluence pages so each API endpoint has its own dedicated page.

Uses `acli` for authentication verification and page reading (to get current version), and Confluence REST API via `curl` for page updates.

## Core Principle: 1 API = 1 Confluence Page

A single API doc file typically documents many endpoints grouped by domain. This skill splits that file into a Confluence page tree:

```
Parent Folder/Page
├── 2. Consent Management APIs          ← domain group page (H2 intro text only)
│   ├── 2.1 Accept Consent              ← individual API page (full H3 content)
│   ├── 2.2 Revoke Consents             ← individual API page
│   └── 2.3 Get Consents by Citizen ID  ← individual API page
├── 3. Purpose Management APIs          ← domain group page
│   ├── 3.1 Create Purpose              ← individual API page
│   └── 3.2 Get All Purposes            ← individual API page
├── 12. Error Responses                 ← standalone page (H2 with no H3 children)
└── 13. Changelog                       ← standalone page
```

Each H3 section (`### X.Y API Name`) becomes exactly one Confluence page containing everything from that H3 heading down to the next H3 or H2 heading.

## Step 1: Gather Required Information

Ask the user for the following (if not already provided):

1. **API doc file path** — e.g., `docs/api-doc.md` (relative to project root, or absolute)
2. **Parent page URL** — the Confluence page/folder under which API doc pages live (or will be created), e.g., `https://company.atlassian.net/wiki/spaces/PROJ/pages/123456789/API+Reference` or a folder URL like `https://company.atlassian.net/wiki/spaces/PROJ/folder/123456789`

Extract the **page ID** directly from the URL (the numeric segment, e.g., `123456789`).

Do NOT ask for Confluence URL, email, or API token — those are resolved automatically in the next step.

## Step 2: Verify Authentication and Resolve Credentials

```bash
acli auth status
```

If not authenticated or acli not found:
- Not installed → tell user: `brew install atlassian/tap/acli` or visit https://developer.atlassian.com/cloud/acli/install/
- Not authenticated → guide user to run: `acli auth login`

From the output, extract:
- **CONFLUENCE_URL** — `Site:` field prefixed with `https://`, e.g., `company.atlassian.net` → `https://company.atlassian.net`
- **EMAIL** — `Email:` field, e.g., `user@company.com`

> **Why REST API for writes?** `acli confluence page` currently only supports `view`. For page create/update we use Confluence REST API via `curl`. URL and email come from `acli auth status`; only the API token needs to be resolved (at write time).

## Step 3: Read, Parse, and Split into Pages

Read the API doc file and split it into individual pages. The Markdown follows a two-level heading structure:

- **H2 (`## N. Domain Name`)** — domain group header (e.g., `## 2. Consent Management APIs`)
- **H3 (`### N.M API Name`)** — individual API endpoint (e.g., `### 2.1 Accept Consent`)

### Parsing Rules

1. **Scan all H2 and H3 headings** in the file
2. **Classify each H2 section** into one of:
   - **Domain group** — has H3 children → becomes a parent page in Confluence
   - **Standalone page** — has no H3 children (e.g., Error Responses, Changelog) → becomes a leaf page
   - **Skip** — meta sections like `Overview`, `Table of Contents` that don't need their own page (or optionally create a single overview page)
3. **Extract content per H3** — each H3 section includes everything from the `### X.Y` heading down to (but not including) the next `###` or `##` heading. This is one API page's content.
4. **Domain group intro** — text between an H2 heading and its first H3 child becomes the domain group page's content (often just a brief intro paragraph, or empty).

### Content Extraction Example

Given this Markdown structure:
```markdown
## 2. Consent Management APIs

Consent APIs for managing personal data consent.

### 2.1 Accept Consent

- **Method:** `POST`
- **Path:** `/api/v1/consents/accept`
...request/response tables and examples...

### 2.2 Revoke Consents

- **Method:** `POST`
- **Path:** `/api/v1/consents/revoke`
...
```

This produces:
- **Page "2. Consent Management APIs"** → content: `"Consent APIs for managing personal data consent."` (parent page)
- **Page "2.1 Accept Consent"** → content: everything from `### 2.1` to just before `### 2.2` (child page)
- **Page "2.2 Revoke Consents"** → content: everything from `### 2.2` to next heading (child page)

### Summary Output

After scanning, show the user a structured summary:
```
Found N domain groups, M individual APIs, K standalone pages:

  2. Consent Management APIs (5 APIs)
     2.1 Accept Consent
     2.2 Revoke Consents
     2.3 Get Consents by Citizen ID
     2.4 Get Consent History
     2.5 Get Consent by ID
  3. Purpose Management APIs (11 APIs)
     3.1 Create Purpose
     3.2 Get All Purposes
     ...
  12. Error Responses (standalone)
  13. Changelog (standalone)

Total pages to create/update: N (domain groups) + M (APIs) + K (standalone) = T pages
```

Ask the user to confirm or specify which sections to sync (all, specific domains, or specific APIs).

## Step 4: Map Sections to Confluence Page Hierarchy

The page structure in Confluence mirrors the document structure:

```
Parent page (provided by user)
├── Domain Group pages (H2 with children) ← first-level children
│   └── Individual API pages (H3)        ← second-level children
└── Standalone pages (H2 without H3)     ← first-level children
```

### Discover Existing Pages

First, fetch all children (and grandchildren) under the parent page to find existing pages:

```bash
# Get direct children of parent page
curl -s "${CONFLUENCE_URL}/wiki/rest/api/content/${PARENT_PAGE_ID}?expand=space,children.page" \
  -u "${EMAIL}:${API_TOKEN}"
```

From the response extract:
- `space.key` → save as `SPACE_KEY` (needed for creating new pages)
- `children.page.results[]` → list of `{id, title}` for direct children

For each direct child that looks like a domain group, also fetch its children:
```bash
curl -s "${CONFLUENCE_URL}/wiki/rest/api/content/${DOMAIN_GROUP_PAGE_ID}/child/page" \
  -u "${EMAIL}:${API_TOKEN}"
```

### Build the Mapping

Match existing page titles against parsed section titles to build the mapping:

| Section | Type | Matched Page ID | Action |
|---|---|---|---|
| 2. Consent Management APIs | Domain group | 456789 | Update |
| 2.1 Accept Consent | API page | 567890 | Update |
| 2.2 Revoke Consents | API page | — | Create (under 456789) |
| 3. Purpose Management APIs | Domain group | — | Create (under parent) |
| 3.1 Create Purpose | API page | — | Create (under new domain group page) |

**Important ordering**: When creating new pages, domain group pages must be created before their child API pages (because child pages need the parent's page ID as ancestor).

### Matching Strategy

- Match by title similarity (case-insensitive, ignore leading numbers like "2.1")
- If ambiguous, show the user and ask them to confirm the mapping
- For unmatched sections → mark as "Create new"

## Step 5: Get Current Page Versions

For each page in the mapping, fetch its current version number (required for updates):

```bash
acli confluence page view --id <PAGE_ID> --include-version --json
```

Extract `version.number` from the JSON output. Store as `CURRENT_VERSION` per page.

## Step 6: Convert Markdown to Confluence Storage Format

For each section, convert the Markdown content to Confluence storage format (XHTML-based):

| Markdown | Confluence Storage |
|---|---|
| ` ```lang\ncode\n``` ` | `<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">lang</ac:parameter><ac:plain-text-body><![CDATA[code]]></ac:plain-text-body></ac:structured-macro>` |
| `**bold**` | `<strong>bold</strong>` |
| `*italic*` | `<em>italic</em>` |
| `[text](url)` | `<a href="url">text</a>` |
| `## Heading` | `<h2>Heading</h2>` |
| `\| col \| col \|` table | `<table><tbody><tr><td>...</td></tr></tbody></table>` |

For `js`, `javascript`, `sh`, `bash`, `json`, `yaml` code blocks, map to the Confluence language name accordingly (`bash` for `sh`, `javascript` for `js`).

## Step 7: Sync Pages (Create + Update) via REST API

Before writing, resolve the API token:

```bash
echo $CONFLUENCE_API_TOKEN
```

- If set → use it silently, no need to ask
- If empty → ask the user once:
  > "ต้องการ API token สำหรับ write ผ่าน Confluence REST API (acli ยังไม่ support page write) — generate ได้ที่ https://id.atlassian.com/manage-profile/security/api-tokens"

Use `EMAIL` extracted from `acli auth status` in Step 2.

### Execution Order (critical for parent-child hierarchy)

1. **First pass — Domain group pages**: Create or update all H2 domain group pages as children of the parent page. This ensures parent page IDs exist before creating child API pages.
2. **Second pass — Individual API pages**: Create or update all H3 API pages as children of their respective domain group pages.
3. **Third pass — Standalone pages**: Create or update H2 pages that have no H3 children, as direct children of the parent page.

### Creating a New Page

```bash
curl -s -X POST \
  "${CONFLUENCE_URL}/wiki/rest/api/content" \
  -u "${EMAIL}:${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"type\": \"page\",
    \"title\": \"${SECTION_TITLE}\",
    \"ancestors\": [{\"id\": \"${ANCESTOR_PAGE_ID}\"}],
    \"space\": {\"key\": \"${SPACE_KEY}\"},
    \"body\": {
      \"storage\": {
        \"value\": \"${ESCAPED_HTML}\",
        \"representation\": \"storage\"
      }
    }
  }"
```

- For domain group pages: `ANCESTOR_PAGE_ID` = user-provided parent page ID
- For individual API pages: `ANCESTOR_PAGE_ID` = the domain group page ID (created in first pass)
- For standalone pages: `ANCESTOR_PAGE_ID` = user-provided parent page ID

Extract `id` from the response to use as ancestor for child pages.

### Updating an Existing Page

```bash
curl -s -X PUT \
  "${CONFLUENCE_URL}/wiki/rest/api/content/${PAGE_ID}" \
  -u "${EMAIL}:${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"version\": {\"number\": $((CURRENT_VERSION + 1))},
    \"title\": \"${SECTION_TITLE}\",
    \"type\": \"page\",
    \"body\": {
      \"storage\": {
        \"value\": \"${ESCAPED_HTML}\",
        \"representation\": \"storage\"
      }
    }
  }"
```

Check HTTP status — 200 means success.

> **Content comparison tip:** Before updating, compare normalized content (collapse whitespace) to skip pages with no real changes. This avoids unnecessary version bumps.

## Step 8: Report Results

Print a summary table after all operations:

```
| Section                    | Type           | Page ID    | Status                  |
|----------------------------|----------------|------------|-------------------------|
| 2. Consent Management APIs | Domain group   | 456789     | Updated (v3 → v4)       |
| 2.1 Accept Consent         | API page       | 567890     | Updated (v2 → v3)       |
| 2.2 Revoke Consents        | API page       | 678901     | Created                 |
| 2.3 Get Consents           | API page       | 567890     | Skipped (no changes)    |
| 12. Error Responses        | Standalone     | 789012     | Created                 |
| 3.1 Create Purpose         | API page       | —          | Failed (HTTP 401)       |
```

Total: N domain groups, M API pages updated, K created, J skipped, F failed.

## Error Reference

| Scenario | Action |
|---|---|
| `acli` not found | Install via `brew install atlassian/tap/acli` |
| `acli auth status` fails | Run `acli auth login` |
| API doc file not found | Re-ask for correct file path |
| HTTP 401 on REST call | Check API token — re-check `$CONFLUENCE_API_TOKEN` or ask user |
| HTTP 404 on page | Verify page ID is correct; page may have been deleted |
| HTTP 409 version conflict | Re-fetch version with acli and retry |
| Section title has no match | Ask user to manually provide page ID |
