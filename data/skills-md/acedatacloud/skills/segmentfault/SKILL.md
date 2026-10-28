---
name: segmentfault
description: Read the connected SegmentFault 思否 (segmentfault.com) account and create Markdown article drafts with the user's own login cookies (BYOC). Use when the user mentions SegmentFault / 思否, wants to save a 思否 draft, or asks who their connected 思否 account is.
when_to_use: |
  Trigger for the user's SegmentFault 思否 account driven by their own login
  cookie: show the connected account, or turn Markdown into a 思否 article
  draft. The write API creates a draft, so this skill stops there and hands the
  user the editor URL. Writes are gated behind explicit confirmation.
connections: [segmentfault]
allowed_tools: [Bash]
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
---

# segmentfault — read & draft on 思否 via your own cookies

Drives the user's **real** SegmentFault account through the same
`segmentfault.com/gateway` endpoints the site uses, authenticated by the login
cookie they captured with the ACE extension. No browser, no third-party deps —
just `urllib`.

The connector injects the cookie jar as a JSON env var `$SEGMENTFAULT_COOKIES`.
Never print it.

```bash
python3 "$SKILL_DIR/scripts/segmentfault.py" whoami
```

If `$SKILL_DIR` points at a different skill loaded in the same turn, resolve
this skill's directory explicitly before running the commands below.

## Important: draft only

SegmentFault's write endpoint (`/gateway/draft`) creates a **draft**. This skill
returns the draft's editor URL and does not publish. Tell the user plainly that
they must open that URL and publish themselves — do not claim the article went
live.

## Verify the connection first

```bash
python3 "$SKILL_DIR/scripts/segmentfault.py" whoami
```

If this fails with an auth error, the cookie has expired. Ask the user to
reconnect at `https://studio.acedata.cloud/console/connectors` rather than retrying.

## Create a draft — GATED

Prepare the complete Markdown in a file. The first call is always a dry run and
does not write anything.

```bash
# Dry run — shows exactly what would be written.
python3 "$SKILL_DIR/scripts/segmentfault.py" draft \
  --title "标题" --content-file /tmp/article.md --tags "python,api"

# Actually create the draft after the user confirms.
python3 "$SKILL_DIR/scripts/segmentfault.py" draft \
  --title "标题" --content-file /tmp/article.md --tags "python,api" --confirm
```

`--confirm` is valid only as the final argument. Show the title, tags and full
content to the user before writing.

## Gotchas

- The write API needs a per-session token scraped from the `/write` page. If
  the CLI reports it could not find that token, the cookie is stale — reconnect
  rather than retrying.
- A restricted account (禁言 / 锁定) is reported as an explicit error. Do not
  retry; tell the user their account is restricted.
- Content is sent as Markdown. Do not pre-render it to HTML.
- Images referenced by external URL are not re-hosted. If the source host
  blocks hotlinking they will not render; mention this when the article has
  images.
- Do not retry a timed-out write automatically — the outcome may be unknown and
  a retry can create a duplicate draft.

## Record the output

This skill only produces drafts, so do **not** call `publish_artifact`. Report
the returned `draft_id` and `edit_url` to the user instead.
