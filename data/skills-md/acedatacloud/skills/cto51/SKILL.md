---
name: cto51
description: Read the connected 51CTO 博客 (blog.51cto.com) account and create Markdown article drafts with the user's own login cookies (BYOC). Use when the user mentions 51CTO, wants to save a 51CTO draft, or asks who their connected 51CTO account is.
when_to_use: |
  Trigger for the user's 51CTO 博客 account driven by their own login cookie:
  show the connected account, or turn Markdown into a 51CTO article draft.
  The write API creates a draft, so this skill stops there and hands the user
  the editor URL. Writes are gated behind explicit confirmation.
connections: [cto51]
allowed_tools: [Bash]
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
---

# cto51 — read & draft on 51CTO 博客 via your own cookies

Drives the user's **real** 51CTO account through the same `blog.51cto.com`
endpoints the site uses, authenticated by the login cookie they captured with
the ACE extension. No browser, no third-party deps — just `urllib`.

The connector injects the cookie jar as a JSON env var `$CTO51_COOKIES`. Never
print it.

```bash
python3 "$SKILL_DIR/scripts/cto51.py" whoami
```

If `$SKILL_DIR` points at a different skill loaded in the same turn, resolve
this skill's directory explicitly before running the commands below.

## Important: draft only

51CTO's write endpoint creates a **draft**. This skill returns the draft's
editor URL and does not publish. Tell the user plainly that they must open that
URL and publish themselves — do not claim the article went live.

## Verify the connection first

```bash
python3 "$SKILL_DIR/scripts/cto51.py" whoami
```

If this fails with a redirect or auth error, the cookie has expired. Ask the
user to reconnect at `https://studio.acedata.cloud/console/connectors` rather than
retrying.

## Create a draft — GATED

Prepare the complete Markdown in a file. The first call is always a dry run and
does not write anything.

```bash
# Dry run — shows exactly what would be written.
python3 "$SKILL_DIR/scripts/cto51.py" draft \
  --title "标题" --content-file /tmp/article.md --tags "python,api"

# Actually create the draft after the user confirms.
python3 "$SKILL_DIR/scripts/cto51.py" draft \
  --title "标题" --content-file /tmp/article.md --tags "python,api" --confirm
```

Options: `--content-file <path.md>` (preferred) or `--content "<markdown>"` for
short inline text; `--tags "a,b"` comma-separated; `--abstract "…"` sets the
summary shown in listings. The dry run echoes every field that will be written,
including the abstract — show that output to the user before confirming.

`--confirm` is valid only as the final argument. Show the title, tags and full
content to the user before writing.

## Gotchas

- 51CTO sits behind a WAF that answers a bare request with HTTP 567. The CLI
  always sends a full browser fingerprint, so do not strip its headers or
  re-implement the calls with plain `curl`.
- Both the identity and the `_csrf` token come from the publish page. A
  redirect there means the session is dead — reconnect, do not retry.
- Content is sent as Markdown (`is_old=0`). Do not pre-render it to HTML.
- Images referenced by external URL are not re-hosted. If the source host
  blocks hotlinking they will not render; mention this when the article has
  images.
- Do not retry a timed-out write automatically — the outcome may be unknown and
  a retry can create a duplicate draft.

## Record the output

This skill only produces drafts, so do **not** call `publish_artifact`. Report
the returned `draft_id` and `edit_url` to the user instead.
