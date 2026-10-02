---
name: atlassian-cloud
description: >
  Use for Atlassian Cloud work — Jira Cloud, Confluence Cloud
  (지라/컨플루언스 클라우드) — when no MCP server is configured. Covers full
  CRUD (including delete) for issues/pages, JQL/CQL search, attachments, and
  Confluence macros of any kind (built-in or marketplace-installed), all via
  direct REST calls with zero third-party dependencies. Trigger words —
  Jira, Confluence, Atlassian Cloud, atlassian.net, JQL, CQL, PROJ-123,
  macro, attachment, 지라, 컨플루언스, 아틀라시안 클라우드, 매크로, 첨부파일.
  For Bitbucket Cloud work, use the separate bitbucket-cloud skill instead.
---

# atlassian-cloud — direct REST access to Jira/Confluence Cloud

This skill is for **Cloud** only (`*.atlassian.net`). It talks to the REST
APIs directly over HTTPS with a single dependency-free Python script — no
MCP server, no SDK install required.

**Bitbucket Cloud is not covered here** — it needs a Bitbucket-scoped API
token and a different auth shape than Jira/Confluence. Use the separate
`bitbucket-cloud` skill for PRs/repos.

## Setup (once per machine — not per session)

Two ways to provide credentials; **the config file is the recommended,
global one** — set it once and every future shell/session already has it,
no `export` needed. Env vars still work and always take priority (handy for
CI or a one-off override). See `references/setup.md` for how to generate the
token.

**Recommended — global config file**, written once with `configure`:

```bash
python3 scripts/atlassian_cloud.py configure \
  --site yourcompany --email you@yourcompany.com \
  --token xxxx
```

This writes `~/.config/atlassian-cloud/credentials.json` (mode `0600`) and
every subsequent command — in any shell, any session, from now on — reads it
automatically. Re-run `configure` with just the flags you want to change;
it merges into the existing file. Override the path with
`ATLASSIAN_CLOUD_CONFIG=/some/other/path` if you need per-project
credentials instead of one global set.

**Alternative — env vars** (session-scoped, or exported from your shell rc
for a pseudo-global effect):

```bash
export ATLASSIAN_SITE=yourcompany          # https://yourcompany.atlassian.net
export ATLASSIAN_EMAIL=you@yourcompany.com
export ATLASSIAN_API_TOKEN=xxxx            # id.atlassian.com → Security → API tokens
```

The same email + API token authenticates both Jira and Confluence Cloud.

Verify before real work:

```bash
python3 scripts/atlassian_cloud.py jira issue-search "order by created DESC" --max-results 1
```

## Command shape

`scripts/atlassian_cloud.py <product> <action> [args]`, product ∈
`jira|confluence`. JQL/CQL are **positional**, same convention as other
Atlassian CLIs in this environment — don't pass them as `--jql=`.

```bash
python3 scripts/atlassian_cloud.py jira issue-get PROJ-123
python3 scripts/atlassian_cloud.py jira issue-search "project = PROJ AND status = 'In Progress'"
python3 scripts/atlassian_cloud.py jira issue-create --project PROJ --type Task --summary "Title" --description "Body text"
python3 scripts/atlassian_cloud.py jira issue-update PROJ-123 --summary "New title"
python3 scripts/atlassian_cloud.py jira issue-delete PROJ-123
python3 scripts/atlassian_cloud.py jira comment-add PROJ-123 "A plain-text comment"
python3 scripts/atlassian_cloud.py jira transition PROJ-123 --list
python3 scripts/atlassian_cloud.py jira transition PROJ-123 --to "Done" --comment "closing out"
python3 scripts/atlassian_cloud.py jira attachment-add PROJ-123 ./report.pdf
python3 scripts/atlassian_cloud.py jira attachment-list PROJ-123
python3 scripts/atlassian_cloud.py jira attachment-download 10001 --output report.pdf

python3 scripts/atlassian_cloud.py confluence page-get 123456
python3 scripts/atlassian_cloud.py confluence search 'space = "ENG" AND text ~ "runbook"'
python3 scripts/atlassian_cloud.py confluence page-create --space-id 98765 --title "New Page" --body-file body.xhtml
python3 scripts/atlassian_cloud.py confluence page-update 123456 --title "New Page" --body-file body.xhtml --if-version 3
python3 scripts/atlassian_cloud.py confluence page-delete 123456
python3 scripts/atlassian_cloud.py confluence attachment-add 123456 ./diagram.png
python3 scripts/atlassian_cloud.py confluence attachment-list 123456
python3 scripts/atlassian_cloud.py confluence attachment-download 123456 diagram.png
python3 scripts/atlassian_cloud.py confluence macro-wrap info --plain-body "Heads up"
python3 scripts/atlassian_cloud.py confluence macro-wrap code --param language=python --plain-body "print(1)"
```

Every command prints the raw Atlassian JSON response to stdout on success,
and the error payload plus a non-zero exit code on failure — read the JSON,
don't guess from exit code alone.

## Body-format gotchas (Cloud differs from Server/DC)

- **Jira Cloud fields (`description`, comment bodies) are ADF**, not wiki
  markup or Markdown. `issue-create`/`issue-update`/`comment-add` auto-wrap
  plain text into minimal ADF paragraphs (blank line = new paragraph). For
  lists, links, mentions, or any other rich structure, build ADF by hand and
  pass it via `--fields-json` — see `references/api-notes.md`.
- **Confluence Cloud page bodies are storage format (XHTML-like)**, passed via
  `--body-file`; there is no Markdown body option in this script. Write the
  file in storage format, not Markdown.
- **Confluence updates require `--if-version`** = the current version number
  (read it from `page-get` first: `body.version.number` or top-level
  `version.number`). The script always sends `version.number + 1`; a stale
  version returns a 409 from the API — re-`page-get` and retry, don't guess.

## Confluence macros — built-in and marketplace, same syntax

Storage format passes macro XML through untouched, so there is no difference
in mechanism between a built-in macro (info/note/warning/tip/panel/code/toc/
expand/status/jira) and one added by a marketplace app — only the macro
`name` and its parameter names differ, and the API has no endpoint to list
either. Use `confluence macro-wrap` to generate the XML, then paste it into
the body file (or compose several and concatenate):

```bash
python3 scripts/atlassian_cloud.py confluence macro-wrap panel --param title="Status" --body-file panel-body.xhtml
python3 scripts/atlassian_cloud.py confluence macro-wrap jira --param key=PROJ-123   # embeds a live Jira issue
```

If a custom app macro's exact `ac:name`/parameter names aren't documented,
the reliable way to learn them is `page-get` on an existing page that already
contains one — the storage XML returned is the ground truth to copy from.

## Attachments

Jira and Confluence attachment uploads are `multipart/form-data` (handled by
the script's stdlib-only multipart builder, no `requests` needed) plus the
mandatory `X-Atlassian-Token: no-check` header, which the script sets
automatically.

Download flows differ per product: `jira attachment-download ID` takes the
attachment's numeric id (from `attachment-list`); `confluence
attachment-download PAGE_ID FILENAME` takes the page id plus the attachment's
title/filename (Confluence has no stable numeric-only lookup by id in this
flow).

## Full CRUD, including delete

Delete is destructive and has no undo:

- `jira issue-delete KEY` — pass `--delete-subtasks` if the issue has children.
- `confluence page-delete ID` — moves the page to trash (not permanently
  gone immediately, but treat it as delete).

## Search specifics

- `jira issue-search` uses the current `/rest/api/3/search/jql` endpoint (the
  old GET `/search` is deprecated on Cloud). `--fields` is a comma-separated
  list; omit it to get Jira's default field set.
- `confluence search` uses CQL against `/wiki/rest/api/content/search` (the v1
  API — Confluence's v2 API has no CQL search endpoint yet). Quote space keys
  and text clauses as shown above.

## Error triage

- `401`/`403` → check `ATLASSIAN_EMAIL`/`ATLASSIAN_API_TOKEN` are for the same
  account that has access to that site.
- `404` on a Jira/Confluence call → check `ATLASSIAN_SITE` resolves to the
  right `https://<site>.atlassian.net`; a wrong site 404s rather than
  redirecting.
- `409` on `confluence page-update` → version conflict; `page-get` again for
  the fresh version and retry.

## Reference

- `references/setup.md` — generating the API token, workspace/site lookup
- `references/api-notes.md` — endpoint table, ADF structure for rich content,
  pagination (`nextPageToken`/`next` link following for large result sets)
