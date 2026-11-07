---
name: yuque
description: Read and write Yuque (语雀) documents on the user's own account — list knowledge bases (知识库), read a document, publish Markdown, and update or delete one. Works with either the user's browser login (free) or a personal access token. Use when the user wants to publish Markdown to 语雀, list their 语雀 knowledge bases, or read a 语雀 document.
when_to_use: |
  Trigger for 语雀 / Yuque document management: verify the connected account,
  list knowledge bases or the documents inside one, read a document, create a
  Markdown document, and (token connections only) update or delete one.
  Writes and destructive actions require explicit confirmation.
connections: [yuque]
allowed_tools: [Bash]
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "2.0"
---

# 语雀 — two connection modes

The connector injects exactly one credential, and the CLI picks its mode from it:

- **`$YUQUE_COOKIES`** — the user's own browser login jar, captured by the ACE
  extension. **Free.** Drives 语雀's internal web API.
- **`$YUQUE_TOKEN`** — a 语雀 personal access token for the official open API.
  **Requires a paid 语雀超级会员.**

Both are **secret — never echo, print, log or return them.** Every command
reports the active mode back as `auth_mode`; read that instead of guessing.

| Command | cookie | token |
|---|---|---|
| `whoami`, `repos`, `docs`, `doc` | ✅ | ✅ |
| `create` | ✅ | ✅ |
| `update`, `delete` | ❌ refused with a clear error | ✅ |

If the user asks to edit or delete on a cookie connection, tell them that needs
a personal token (created at `https://www.yuque.com/settings/tokens`, 超级会员
required) and offer to create a new document instead. Do not attempt a
workaround.

## Script resolution

Bash calls do not share shell variables. Resolve the helper inside **every**
fenced Bash invocation before using it:

```sh
Y="${SKILL_DIR:-}/scripts/yuque.py"; [ -f "$Y" ] || Y=$(find /tmp -maxdepth 8 -path '*/skills/*/yuque/scripts/yuque.py' -print -quit 2>/dev/null)
[ -f "$Y" ] || { echo "yuque script not found (SKILL_DIR=$SKILL_DIR)" >&2; exit 1; }
python3 "$Y" whoami
```

On an auth error, ask the user to reconnect at
<https://studio.acedata.cloud/console/connectors>. Never ask for their password,
and never ask them to paste a Cookie into the chat.

## Read

A knowledge base (`repo`) is addressed by its `user/book` namespace or its
numeric id. **Always run `repos` first — never guess a namespace or an id.**
Pass back exactly the `repo_id` that `repos` printed; on a cookie connection a
`user/book` namespace is resolved by matching the account's own knowledge
bases, so it fails for a base the account does not own, and an ambiguous slug
is refused rather than guessed.

```sh
Y="${SKILL_DIR:-}/scripts/yuque.py"; [ -f "$Y" ] || Y=$(find /tmp -maxdepth 8 -path '*/skills/*/yuque/scripts/yuque.py' -print -quit 2>/dev/null)
python3 "$Y" repos
python3 "$Y" docs REPO_ID --limit 20
python3 "$Y" doc REPO_ID DOC_ID
```

## Create

Prepare the complete Markdown in a file. 语雀 has no draft state — a document is
either private or public — so the CLI creates **private** documents by default
and only publishes publicly with an explicit `--public`.

```sh
Y="${SKILL_DIR:-}/scripts/yuque.py"; [ -f "$Y" ] || Y=$(find /tmp -maxdepth 8 -path '*/skills/*/yuque/scripts/yuque.py' -print -quit 2>/dev/null)

# The first call is always a dry run: it loads no credentials and calls no API.
python3 "$Y" create REPO_ID --title "标题" --content-file /tmp/article.md

# Create it privately after the user confirms.
python3 "$Y" create REPO_ID --title "标题" --content-file /tmp/article.md --confirm

# Public publishing additionally requires --public.
python3 "$Y" create REPO_ID --title "标题" --content-file /tmp/article.md --public --confirm
```

`--confirm` is honored **only as the final argument**. Before a public publish,
always show the user the target knowledge base, the title, the visibility and
the full content. Default to private unless they explicitly ask to publish
publicly.

## Update and delete (token connections only)

```sh
python3 "$Y" update REPO_NAMESPACE DOC_ID --title "新标题" --content-file /tmp/a.md --confirm
python3 "$Y" delete REPO_NAMESPACE DOC_ID --confirm
```

`update` rewrites the whole document body — read the current document first if
the user only wants part of it changed.

## Gotchas

- Use the real returned `doc_id` and `url`; never invent either. A cookie
  connection cannot always resolve a public URL, in which case `url` is `null`
  — report the `doc_id` instead of guessing a link.
- If a write times out its outcome is **unknown** — run `docs` to check before
  retrying, or you will create a duplicate.
- Images referenced by external URL are not re-hosted; 语雀 renders them from
  the original host. If that host blocks hotlinking, upload the images in 语雀
  manually first and reference the returned URLs.
- 语雀's terms allow the API for normal reading and writing of 语雀 content;
  abnormal automated behaviour can get the account blocked. Keep the volume
  human-scale and never batch-publish.

## Record the output

After a confirmed **public** publish, if the response carries a non-null `url`,
call `publish_artifact` once with `kind="article"`, `channel="yuque"`, the
title, that URL, and `status="delivered"`. If `url` is `null`, **do not invent
one** — report the `doc_id` to the user and skip `publish_artifact`. Do not
record private documents or failed/unknown writes.
