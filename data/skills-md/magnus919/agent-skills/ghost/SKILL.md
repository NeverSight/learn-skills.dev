---
name: ghost
description: Manage Ghost CMS content over the Admin API — browse posts, pages,
  and tags, draft and publish content, schedule posts, and inspect site info from
  the terminal. Do not use this skill for Ghost server installation or site
  administration (installing, nginx, SSL, systemd, updates); those belong to the
  official npm ghost-cli tooling.
license: MIT
compatibility: Requires GHOST_URL and GHOST_ADMIN_KEY env vars. Admin key in "id:secret"
  format from Ghost Admin → Integrations. Python 3.8+ and the `requests` library.
metadata:
  tags: ghost, cms, blog, blogging, post, page, tag, ghost-cms, content-management,
    api-client
  sources: https://docs.ghost.org/admin-api/, https://docs.ghost.org/content-api/
---

# ghost — Ghost CMS content from the terminal

Drive a Ghost CMS site's Admin API (v5/v6, `Accept-Version: v6.0`): list posts by status including drafts, create and publish pages and posts, manage tags, and check site info. Drafts, scheduled posts, and published content are all visible here because every call authenticates with a per-request Admin JWT built from your `id:secret` integration key.

## Setup

```bash
export GHOST_URL="https://your-ghost-site.com"
export GHOST_ADMIN_KEY="<RECORD_KEY>"   # id:secret from Ghost Admin → Integrations
```

1. In **Ghost Admin → Settings → Integrations**, create (or open) a Custom Integration.
2. Copy its **Admin API Key** — one string, two colon-separated hex halves (`id:secret`). The separate **Content API key** from the same screen will NOT let you see drafts; see Known Gotchas.
3. At request time the CLI signs a short-lived JWT per call: HS256 signature keyed by the secret half **after hex-decoding it to raw bytes**, `kid` header carrying the id half, audience `/admin/`, `exp` five minutes after `iat`, sent as `Authorization: Ghost <token>`. You never handle the token yourself.
4. `--help` and `--dry-run` work without credentials (lazy auth).

## Essential commands

### Inspect

```bash
ghost site                       # title, url, description, version
ghost get-post POST_ID           # full record incl. exact updated_at for edits
```

### Browse (intent: find content)

```bash
ghost posts                                   # latest 20
ghost posts --status draft                    # unpublished work queue
ghost posts --status scheduled                # what publishes next
ghost posts --limit 100 --page 2              # paginate (max page size 100)
ghost posts --order "updated_at desc"         # SQL-style ordering
ghost pages                                   # static pages
ghost tags                                    # tags with usage counts
```

### Create and publish

```bash
ghost create-post --title "Notes"                              # safe default: draft
ghost create-post --title "Hello" --html "<p>Hi</p>"
ghost create-post --title "Launch" --status published --html "<p>We're live</p>"
ghost create-post --title "Later" --status scheduled \
  --published-at "2026-09-01T09:00:00.000Z"                    # future ISO-8601 required together
ghost create-page --title "About" --html "<p>…</p>" --slug about
ghost create-tag --name "Engineering" --description "Technical posts"
```

### Edit and remove

```bash
ghost update-post POST_ID --title "New title" \
  --updated-at "<RECORD_UPDATED_AT>"          # REQUIRED: latest updated_at, re-read first
ghost update-post POST_ID --status published --updated-at "<RECORD_UPDATED_AT>"
ghost delete-post POST_ID                     # permanent, 204-style removal
```

## Pipeline recipes

### Draft now, publish after review

```bash
ghost --json create-post --title "Release notes" > /tmp/post.json
id=$(jq -r '.post.id // .post_id // empty' /tmp/post.json)
ghost get-post "$id"                          # read fresh updated_at
ghost update-post "$id" --status published \
  --updated-at "<exact string from get-post output>"
```

Never fabricate `updated_at`; copy it verbatim from a fresh read or Ghost rejects the edit with HTTP 409 `UpdateCollisionError`.

### Review queue across statuses

```bash
for s in draft scheduled; do
  ghost posts --status "$s" --json | jq -r '.posts[] | "\(.status)\t\(.title)\t\(.slug)"'
done
```

### Complete export

Loop pages by `meta.pagination.next` (surfaced as `.page.next`) instead of trusting totals:

```bash
page=1
while :; do
  ghost posts --limit 100 --page "$page" --json > "/tmp/posts-$page.json"
  jq -r '.posts[].id' "/tmp/posts-$page.json"
  next=$(jq -r '.page.next // empty' "/tmp/posts-$page.json")
  [ -z "$next" ] && break
  page=$next; sleep 0.2
done
```

## JSON output and jq

`--json` works before or after the subcommand:

```bash
ghost --json posts        # same as: ghost posts --json
```

JSON shapes worth knowing:

- Lists emit `{"total", "page": {pagination}, "posts": [...]}`; detail/create emit the resource under its noun (`post`, `page`, `tag`, `site`).
- Pagination mirrors the API: `.page = {"page", "limit", "pages", "total", "next", "prev"}`; `next`/`prev` are numbers or `null`.
- `--dry-run --json` emits the executed plan instead of results: `{"dry_run": true, "method", "url", "params"/"json"}` — preview the exact request before running it live.
- Errors exit non-zero with the API's own message plus code on stderr; JSON mode never wraps errors in stdout JSON.

## Global flags

| Flag | Effect |
|------|--------|
| `--json` | Machine-readable JSON (position-independent) |
| `--dry-run` | Print the planned API call (method, URL, payload) without executing |
| `--quiet` | Suppress diagnostics |
| `--verbose` | Debug logging |

## Known gotchas

- **Drafts need the Admin plane.** The public Content API (that key-as-query-param API) serves published posts only and hides drafts silently — no error, just absent, even with a perfectly valid key. Its filters like `status:draft` are ignored rather than rejected. Everything this CLI does goes through the Admin API precisely so drafts and scheduled posts stay reachable.
- **Two keys, same integration screen.** The Content key is browser-safe but read-only-public; the Admin key (`GHOST_ADMIN_KEY`) signs mutations and reaches drafts. Never point scripts at the Content key and expect draft visibility.
- **Five-minute tokens.** Each JWT lives at most 300 seconds (`exp ≤ iat + 300`) and the verifier caps token age too, so long batch jobs must re-sign per request (the CLI does). Skewed clocks break signing windows; keep NTP healthy.
- **HS256 only, decoded-secret keying.** Tokens signed with HS512 are refused ("invalid algorithm"); signing without first hex-decoding the secret half produces "valid-looking" garbage that 401s. The CLI handles both rules.
- **`Authorization: Ghost`, not Bearer.** `Bearer` scheme answers 401 `INVALID_AUTH_HEADER`.
- **Edits require collision guards.** PUTs without the post's current `updated_at` fail with 409; relation arrays (`tags`, `authors`) replace wholesale rather than merge.
- **`--html` requires `source=html` and stays lossy.** Every write carrying an `html` payload (create-post, update-post, create-page) must send the `?source=html` query flag — the CLI attaches it automatically, and dry-run plans show it in `params` — or Ghost parses the body as mobiledoc/lexical. Even with the flag, conversion is lossy: send proper Lexical, or wrap fixed markup in HTML card comments.
- **Pagination caps at 100** since Ghost 6 removed `limit=all`; oversized limits silently return ≤100 rows, so always loop by `next`.
- **Deletion is permanent** and takes effect on the public site immediately.

## When to use

Use this skill whenever the task is content workflow against a running Ghost site: browsing or exporting posts, drafting, publishing, scheduling, tag upkeep, page creation, or diagnosing those flows (auth errors, pagination, missing drafts).

## When not to use

Do not use it to install, host, or operate a Ghost server (`ghost install`, nginx/SSL/systemd setup, upgrades, backups) — that is Ghost's official npm ghost-cli site-management tool, unrelated despite the shared name. Not for other publishing platforms (WordPress, Hugo have their own tooling), not for theme development, and not for site configuration better done once in the Admin dashboard (staff accounts, membership tiers).

## Reference files

| File | Use it for |
| ---- | ---------- |
| [references/admin-auth-and-basics.md](references/admin-auth-and-basics.md) | Full JWT signing walkthrough, key format, audience/expiry rules, auth error table |
| [references/content-vs-admin-api.md](references/content-vs-admin-api.md) | Choosing between planes; the draft-visibility trap; diagnostic checklist |
| [references/posts-pages-tags-endpoints.md](references/posts-pages-tags-endpoints.md) | Endpoint map, field semantics, pagination loop, error envelope |
| [references/worked-recipes.md](references/worked-recipes.md) | Copy-paste workflows: draft→publish, exports, scheduling, triage |
| [references/gotchas-field-guide.md](references/gotchas-field-guide.md) | Symptom-first incident lookup for auth, editing, volume problems |

## Scripts and prerequisites

- `scripts/ghost` — executable Python CLI (stdlib + requests only). Flags above; lazy auth; structured logging.
- `scripts/test_ghost.py` — offline test suite (mocked HTTP, zero network).
- Python 3.8+, `requests`. Nothing listens, nothing installs; scope limited to one configured site via `GHOST_URL`.
