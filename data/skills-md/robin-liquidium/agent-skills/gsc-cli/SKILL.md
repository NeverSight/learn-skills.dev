---
name: gsc-cli
description: "Google Search Console CLI: sites, analytics, sitemaps, URL Inspection."
allowed-tools: Bash(./scripts/gsc-cli:*)
---

# gsc-cli

Use the local Google Search Console CLI wrapper for Search Console API work.

This skill exists because Google Search Console has an official API but no first-party Search Console CLI. The local wrapper keeps common GSC reads low-noise and makes write-capable sitemap/site actions explicit.

## Quick rules

- Prefer read-only OAuth unless the user specifically needs sitemap or site writes.
- Do not run `sites add`, `sites delete`, `sitemaps submit`, or `sitemaps delete` with `--execute` unless the user explicitly approved that exact action.
- Keep analytics queries narrow: short date ranges first, then expand if needed.
- Parse JSON output instead of scraping terminal text.
- Read `references/google-search-console-api.md` when endpoint behavior, auth scopes, quotas, or dimensions matter.

## Local setup

Prefer the skill-local script over any global or third-party GSC CLI.

Primary config path:

```bash
~/.config/gsc-cli/config.json
```

Recommended one-time setup:

```bash
<skill-path>/scripts/setup-auth.sh
```

For a headless machine, the OAuth flow prints a Google auth URL. The user opens it in their own browser, grants access, then pastes back the final redirected URL or code. The CLI stores the refresh token in the config file.

Setup prerequisites:

- Enable the **Google Search Console API** in the same Google Cloud project that owns the OAuth client.
- Use a Google OAuth **Desktop app** client, not TV/Limited Input.
- Keep the OAuth app internal or in production when possible so refresh tokens do not expire like External Testing grants.
- If `doctor` returns `SERVICE_DISABLED`, open the activation URL from the error, enable the API, wait a minute, then retry.

## Commands

### Show name and description

```bash
<skill-path>/scripts/gsc-cli info
```

### Authenticate

Read-only access:

```bash
<skill-path>/scripts/setup-auth.sh
```

Write-capable access for sitemap/site mutations:

```bash
<skill-path>/scripts/gsc-cli auth url --scope full
```

Use a Google OAuth **Desktop app** client for `auth url`. Google's device flow may reject Search Console scopes with `invalid_scope`.

`full` permits Search Console write actions such as sitemap submit/delete and site add/delete. It does not provide an API equivalent of the Search Console UI's manual "Request indexing" action for arbitrary normal pages; for normal page discovery, update/submit sitemaps.

### Check auth

```bash
<skill-path>/scripts/gsc-cli auth status
<skill-path>/scripts/gsc-cli doctor
```

### List Search Console properties

```bash
<skill-path>/scripts/gsc-cli sites list
```

### Get one property

```bash
<skill-path>/scripts/gsc-cli sites get --site 'sc-domain:example.com'
```

### Query search analytics

```bash
<skill-path>/scripts/gsc-cli analytics query \
  --site 'sc-domain:example.com' \
  --start-date 2026-05-01 \
  --end-date 2026-05-31 \
  --dimensions query,page \
  --type web \
  --row-limit 100
```

Filter examples:

```bash
<skill-path>/scripts/gsc-cli analytics query \
  --site 'https://www.example.com/' \
  --start-date 2026-05-01 \
  --end-date 2026-05-31 \
  --dimensions page,query \
  --filter 'page:contains:/blog/' \
  --filter 'device:equals:MOBILE'
```

### Inspect a URL's Google index status

```bash
<skill-path>/scripts/gsc-cli url inspect \
  --site 'sc-domain:example.com' \
  --url 'https://www.example.com/page' \
  --language-code en-US
```

### Work with sitemaps

```bash
<skill-path>/scripts/gsc-cli sitemaps list --site 'sc-domain:example.com'
<skill-path>/scripts/gsc-cli sitemaps get --site 'sc-domain:example.com' --sitemap 'https://www.example.com/sitemap.xml'
<skill-path>/scripts/gsc-cli sitemaps submit --site 'sc-domain:example.com' --sitemap 'https://www.example.com/sitemap.xml'
<skill-path>/scripts/gsc-cli sitemaps submit --site 'sc-domain:example.com' --sitemap 'https://www.example.com/sitemap.xml' --execute
```

## Workflow

1. Read `references/google-search-console-api.md` if the task needs API details.
2. Run `scripts/gsc-cli info` or `help` if command shape is unclear.
3. Run `auth status` or `doctor` before assuming credentials are usable.
4. Use `sites list` to confirm the exact property string, especially `sc-domain:` versus URL-prefix properties with trailing slash.
5. Query analytics, URL Inspection, or sitemaps with the narrowest useful request.
6. For any write, dry-run first, show the target/action JSON, then use `--execute` only after explicit approval.

## Expected outputs

The CLI returns JSON by default.

- `sites list` returns `siteEntry` rows with `siteUrl` and `permissionLevel`.
- `analytics query` returns GSC `rows` with `keys`, `clicks`, `impressions`, `ctr`, and `position`.
- `url inspect` returns `inspectionResult`.
- Write commands without `--execute` return a dry-run JSON object.

## Files

- Launcher: `scripts/gsc-cli`
- Python implementation: `scripts/gsc_cli.py`
- Auth helper: `scripts/setup-auth.sh`
- API notes and official docs: `references/google-search-console-api.md`
- Config storage: `~/.config/gsc-cli/config.json`

## Official Docs

- Search Console API reference: `https://developers.google.com/webmaster-tools/v1/api_reference_index`
- Authorization: `https://developers.google.com/webmaster-tools/v1/how-tos/authorizing`
- Search Analytics query: `https://developers.google.com/webmaster-tools/v1/searchanalytics/query`
- URL Inspection index.inspect: `https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect`
- Usage limits: `https://developers.google.com/webmaster-tools/limits`

## When to stop and ask

Stop and ask before:
- enabling write scope when read-only would be enough
- executing site or sitemap mutations
- adding broad/backfill analytics loops
- changing where credentials are stored
