---
name: jira
description: 'Interact with Atlassian Jira from the terminal: search issues with
  JQL, view details, create issues, add comments, count matches with fast
  approximate-count, list projects, discover valid transitions, and change
  status. Includes a full JQL language reference (functions, operators, history
  predicates, date expressions, saved filters, performance tuning) plus REST
  auth/pagination guidance. Use when the user mentions Jira, a ticket key
  (e.g. PROJ-123), asks about issues, bugs, tasks, projects, or sprint work,
  or needs to write, debug, or optimize JQL queries. Do not use for GitHub or
  GitLab issue tracking, Jira site administration, or generic ticketing systems.'
license: MIT
compatibility: Requires JIRA_EMAIL and JIRA_API_TOKEN env vars (free API token from
  id.atlassian.com/manage/api-tokens), Python 3.8+, and the `requests` library.
  JIRA_SERVER defaults to your-domain.atlassian.net format.
metadata:
  tags: jira, atlassian, issue-tracking, project-management, api-client
  sources: https://developer.atlassian.com/cloud/jira/platform/rest/v3/, https://id.atlassian.com/manage/api-tokens
---

# jira — Jira Issue Tracker from the Terminal

Interact with Atlassian Jira Cloud via the REST API v3. Search issues, view details, create issues, add comments, count matches, list projects, and transition status.

## Setup

1. Generate an API token at [id.atlassian.com/manage/api-tokens](https://id.atlassian.com/manage/api-tokens)
2. Set environment variables:

```bash
export JIRA_EMAIL="your-email@example.com"       # Atlassian account email
export JIRA_API_TOKEN="YOUR_API_TOKEN"           # from id.atlassian.com
export JIRA_SERVER="https://your-domain.atlassian.net"
```

Auth is HTTP Basic over `base64(email:token)` — your **email address**, never a password (passwords are deprecated for API use). Cloud has no Personal Access Tokens; Bearer PATs are Data Center only. Tokens now expire after at most one year. `--help` and `--dry-run` work without credentials.

## Essential Commands

### me / projects — identity and scope

```bash
jira me                       # verify auth; your accountId, timezone
jira projects --json          # all accessible projects
```

### list — search issues

```bash
jira list                                                # recent issues
jira list --project PROJ                                 # by project
jira list --jql 'assignee=currentuser() AND status=Open' # custom JQL
jira list --project PROJ --max 120 --json                # >50 auto-pages via startAt offsets
```

### view — issue details

```bash
jira view PROJ-123                        # summary, status, assignee, description
jira view PROJ-123 --json                 # machine-readable
```

Descriptions arrive as Atlassian Document Format (ADF); the CLI extracts plain text for display.

### count — fast match total

```bash
jira count --jql 'issuetype = Bug AND resolution = Unresolved'   # {"count": N}
```

Uses `POST /search/approximate-count` — no fetching rows. JQL itself has no COUNT/aggregation.

### create — new issues

```bash
jira --yes create --project PROJ --summary "Fix login bug"            # Task (default)
jira --yes create --project PROJ --summary "Crash on startup" --type Bug
jira --yes create --project PROJ --summary "Add dark mode" --type Story --priority High
jira create --project PROJ --summary "Test" --dry-run           # preview payload
```

Descriptions are sent as ADF documents. Rich formatting beyond plain paragraphs needs raw ADF JSON — see references/rest-issues-and-transitions.md.

### comment — add to threads

```bash
jira --yes comment PROJ-123 -m "Fixed in latest build"
jira comment PROJ-123 -m "Looking into it" --dry-run
```

### transitions + transition — status changes

```bash
jira transitions PROJ-123                     # LIST valid transition IDs first
jira --yes transition PROJ-123 --to "In Progress"   # then apply by name or ID
jira --yes transition PROJ-123 --to Done --resolution Done
jira transition PROJ-123 --to "In Review" --dry-run
```

Always run `transitions` first when unsure: IDs differ per workflow and current status, and names repeat across workflows. `--resolution` satisfies Done-style screens that require one; omitting it yields `400` with an error naming the missing field.

## Global Flags

All flags work in any position. Read commands need credentials; `--help` and `--dry-run` do not. Mutating commands require an explicit `--yes`/`--force` gate:

```bash
jira --json list --project PROJ                        # machine output anywhere
jira --dry-run create --project PROJ --summary "Test"  # offline preview
jira --yes create --project PROJ --summary "Test"      # explicit write authorization
jira --quiet list                                      # suppress non-essential output
```

`--json` emits one JSON object per command on stdout — pipe to jq for structure.

## Multi-Step Pipeline Recipes

### Sprint hygiene sweep

Find stalled sprint work, review each ticket, close what's finished:

```bash
jira list --jql 'sprint IN openSprints() AND updated < -14d AND resolution = Unresolved' --json \
  | jq -r '.issues[].key' \
  | while read -r key; do jira view "$key"; jira transitions "$key"; done
# after human review, per key:
jira --yes transition "$key" --to Done --resolution Done
```

The `list --json` shape is `{"total": N, "issues": [{"key", "summary", "status", "assignee", "issuetype", "priority"}]}`.

### Bulk-close with safe discovery

Transition IDs are workflow-specific — resolve before writing:

```bash
for key in $(jira list --jql 'status = "In Progress" AND updated < -30d' --json | jq -r '.issues[].key'); do
  tid=$(jira transitions "$key" --json | jq -r '.transitions[] | select(.status_category=="completed") | .id' | head -1)
  [ -n "$tid" ] && jira --yes transition "$key" --to "$tid" --resolution Done
done
```

### Weekly digest via jq

```bash
jira list --jql 'assignee = currentUser() AND updated >= startOfWeek()' --max 50 --json \
  | jq -r '.issues[] | "\(.key)\t\(.status)\t\(.summary)"'
```

More ready-to-run queries live in [references/jql-cookbook.md](references/jql-cookbook.md), organized by role.

## Using --json with jq

```bash
jira list --project PROJ --json | jq '.issues[] | {key, status, assignee}'
jira count --jql 'project = PROJ' --json | jq .count
jira transitions PROJ-123 --json | jq -r '.transitions[] | "\(.id)=\(.name) -> \(.to_status)"'
```

## Known Gotchas

- **Search endpoint duality** — this CLI uses the classic `/rest/api/3/search` with offset pagination (`startAt`, `maxResults`, `total`). Atlassian's enhanced `/rest/api/3/search/jql` replaces it with an opaque `nextPageToken` (+ `isLast`), no `startAt`, no `total`, ids-only default fields, and it rejects unbounded JQL (`order by key desc` alone → 400). The classic endpoint is deprecated ("currently being removed", announced Oct 2024, removal promised after May 1 2025), so expect forced migration; mixing the two pagination models is the classic source of infinite-page-one loops.
- **Pagination caps** — legacy pages default to `maxResults=50`; `total` can shrink between pages, so always tolerate empty pages instead of trusting a stale total.
- **Transitions need GET first** — transition IDs (`"31"`, `"711"`) belong to one workflow/status; asking for an invalid one returns an *empty list*, not an error. Done-style screens frequently require `resolution`; missing required fields come back as `400` with `"errors": {"resolution": "..."}` naming them.
- **ADF everywhere** — descriptions, comments, and environment fields take ADF JSON objects in v3 payloads; bare strings are rejected.
- **Authentication** uses HTTP Basic with email + API token. CAPTCHA lockouts (repeated bad logins) block REST auth entirely; symptom header: `X-Seraph-LoginReason: AUTHENTICATION_DENIED`. Fix in the browser, not by retrying.
- **Rate limits** return 429 with `Retry-After` and `RateLimit-Reason` headers; the CLI surfaces both but does not auto-retry. Writes also cap at ~20/2s per issue.
- **Project keys are case-sensitive** in some contexts, though the API generally accepts either case.
- **accountId, not username** — user fields accept Atlassian account IDs (GDPR migration); usernames were removed from the API.

### JQL gotchas

- **`!=` excludes empty values** — `assignee != currentUser()` silently drops unassigned issues. Write `(assignee != currentUser() OR assignee IS EMPTY)`.
- **AND binds tighter than OR** — `A OR B AND C` parses as `A OR (B AND C)`. Always parenthesize OR groups; without parentheses evaluation is left-to-right.
- **No leading wildcards** — `summary ~ "*bug"` forces a full scan; put wildcards after the first characters.
- **Filter by project first** — the biggest performance lever on large instances (official optimization guidance).
- **History operators have a field whitelist** — `WAS`/`CHANGED` work only on Assignee, Fix Version, Priority, Reporter, Resolution, Status, and silently return nothing on fields without history tracking.
- **Relative dates are case-sensitive** — `-1m` is minutes, `-1M` is months; day-grain expressions evaluate in each user's timezone.
- **JQL has no aggregation** — no COUNT/SUM; use `jira count` (approximate-count endpoint) or dashboard gadgets.

## When to use

- Any Jira Cloud interaction from the terminal: search, view, create, comment, transition
- Writing, debugging, or optimizing JQL queries — full language reference included
- Sprint reviews, triage sweeps, bulk status hygiene, dashboards and saved-filter design

## When not to use

Do not use this skill for GitHub or GitLab issue tracking (use those platforms' own tooling such as `gh`), for Jira site administration like permission schemes or workflow editing (admin UI territory), for Confluence content, or for building server-side integrations against the Jira API (use official Atlassian SDK docs instead).

## Reference Files

| File | Topic | Read when |
|------|-------|-----------|
| [references/rest-auth-and-search.md](references/rest-auth-and-search.md) | Basic-auth/token mechanics vs OAuth/PATs, rate-limit headers, error envelopes, legacy-vs-enhanced search pagination duality | Setting up credentials, handling 429/401s, paginating large searches, or migrating off `/search` |
| [references/rest-issues-and-transitions.md](references/rest-issues-and-transitions.md) | GET/POST/PUT issue shapes, transitions GET→POST flow with screen-field requirements, ADF document model | Creating/editing issues programmatically, resolving transition failures, formatting rich text |
| [references/jql-functions-catalog.md](references/jql-functions-catalog.md) | Every JQL function with supported fields/operators — date/time, user, sprint/version, custom field, JSM approvals & SLAs | Checking which operators/functions a query can use |
| [references/jql-best-practices.md](references/jql-best-practices.md) | Operator precedence, performance rules, the empty-value trap, troubleshooting flows, marketplace extensions | A query is slow, wrong, or mixes AND/OR |
| [references/jql-cookbook.md](references/jql-cookbook.md) | 50 ready-to-run queries organized by role (developers, scrum masters, POs/managers, power users, admins) | Building filters, automation rules, sprint reviews |
| [references/jql-history-and-dates.md](references/jql-history-and-dates.md) | WAS/CHANGED predicate walkthrough, relative-date expression tables, saved-filter composition and naming conventions | History queries, date math, or designing reusable saved filters |

## Available Scripts

| Script | Purpose | Invocation |
|---|---|---|
| `scripts/jira` | The CLI this skill drives: `me`, `list`, `view`, `projects`, `create`, `comment`, `count`, `transitions`, `transition` — all with `--json`/`--dry-run`, lazy auth, offset-pagination fetches above 50 results, parsed API error messages, and 429 Retry-After surfacing. Run it for every Jira data question above. | `scripts/jira list --project PROJ --json` |
| `scripts/test_jira.py` | Offline pytest/unittest suite covering help text, argument errors, dry-run plans, pagination loops, error envelopes, and transition resolution logic — zero network. Run after modifying `scripts/jira`. | `.venv/bin/python3 -m pytest -p no:cacheprovider --strict-markers scripts/test_jira.py` |

## Prerequisites

- Python 3.8+ with `requests` (stdlib otherwise); invoke as `python3 scripts/jira ...` if not executable directly
- `JIRA_EMAIL` + `JIRA_API_TOKEN` exported for any non-dry-run command (token from https://id.atlassian.com/manage/api-tokens); `JIRA_SERVER` defaults to `https://your-domain.atlassian.net`
- `jq` recommended for `--json` post-processing

## Limitations

- Targets Jira **Cloud** REST v3; Data Center sites authenticate differently (Bearer PAT) and expose older API surfaces
- The classic search endpoint this CLI uses is deprecated upstream; expect eventual forced migration to `/search/jql` token paging
- Rich-text creation beyond plain paragraphs requires hand-built ADF JSON
- No auto-retry on 429; loops over many writes should sleep between calls
