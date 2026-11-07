---
name: oschina
description: Read the connected 开源中国 / OSChina (my.oschina.net) account and create Markdown blog drafts with the user's own login cookies (BYOC). Use when the user mentions 开源中国 / OSChina, wants to save a 开源中国 draft, or asks who their connected 开源中国 account is.
when_to_use: |
  Trigger for the user's 开源中国 (my.oschina.net) account driven by their own
  login cookie: show the connected account, or turn Markdown into a 开源中国
  blog draft. 开源中国 exposes no publish API, so this skill stops at a draft
  and hands the user the editor URL. Writes are gated behind explicit
  confirmation.
connections: [oschina]
allowed_tools: [Bash]
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
---

# oschina — read & draft on 开源中国 via your own cookies

Drives the user's **real** 开源中国 account through the same
`apiv1.oschina.net` endpoints the site uses, authenticated by the login cookie
they captured with the ACE extension. No browser, no third-party deps — just
`urllib`.

The connector injects the cookie jar as a JSON env var `$OSCHINA_COOKIES`.
Never print it.

```bash
python3 "$SKILL_DIR/scripts/oschina.py" whoami
```

If `$SKILL_DIR` points at a different skill loaded in the same turn, resolve
this skill's directory explicitly before running the commands below.

## Important: draft only

**开源中国 has no public publish API.** Every open-source client for this
platform (including the upstream adapter this skill is modelled on) stops at
draft creation. This skill does the same: it saves the Markdown as a draft and
returns the editor URL. Tell the user plainly that they must open that URL and
click publish themselves — do not claim the article was published.

## Verify the connection first

```bash
python3 "$SKILL_DIR/scripts/oschina.py" whoami
```

If this fails with an auth error, the cookie has expired. Ask the user to
reconnect at `https://studio.acedata.cloud/console/connectors` rather than retrying.

## Create a draft — GATED

Prepare the complete Markdown in a file. The first call is always a dry run and
does not write anything.

```bash
# Dry run — shows exactly what would be written.
python3 "$SKILL_DIR/scripts/oschina.py" draft \
  --title "标题" --content-file /tmp/article.md

# Actually create the draft after the user confirms.
python3 "$SKILL_DIR/scripts/oschina.py" draft \
  --title "标题" --content-file /tmp/article.md --confirm
```

`--confirm` is valid only as the final argument. Show the title and full
content to the user before writing.

## Gotchas

- Content is sent as Markdown (`contentType: 1`). Do not pre-render it to HTML.
- Images referenced by external URL are not re-hosted. If the source host
  blocks hotlinking they will not render; mention this when the article has
  images.
- `--catalog` takes a 开源中国 catalog id; the default `0` uses the account's
  default catalog. If the API rejects the catalog, ask the user for the right
  id rather than guessing.
- Do not retry a timed-out write automatically — the outcome may be unknown and
  a retry can create a duplicate draft.

## Record the output

This skill only produces drafts, so do **not** call `publish_artifact`. Report
the returned `draft_id` and `edit_url` to the user instead.
