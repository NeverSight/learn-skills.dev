---
name: htmldrop
description: >-
  Upload local HTML or Markdown artifacts to baseurl.ai and return a shareable,
  password-bearing preview URL. Use this skill whenever the user asks to
  publish, share, host, preview, send a link for, or make accessible any local
  .html, .htm, .md, or .markdown file, including reports or documents you just
  generated. Also use it when a workflow produces renderable local content and
  the next useful step is a URL someone else can open. Do not use it for
  production deployments, long-term hosting, or non-renderable source files
  unless you first create a local HTML or Markdown artifact.
argument-hint: <file>
allowed-tools: Bash
---

# HTMLDrop

Use this skill to turn a local HTML or Markdown artifact into a temporary
baseurl.ai preview URL. The full URL includes the access password as `?p=...`;
anyone with that full URL can view the page.

## Before Uploading

1. Identify the artifact to upload.
   - If the user gave a path, use that exact file after confirming it exists.
   - If you just generated an HTML or Markdown report, use that generated file.
   - If several candidate files exist and the user did not identify one, choose
     the most relevant recently generated `.html`, `.htm`, `.md`, or
     `.markdown` file only when the context is unambiguous. Otherwise ask one
     concise question.
2. Check content sensitivity before upload.
   - If the file appears to contain credentials, private keys, tokens, secrets,
     or data the user did not intend to share externally, stop and ask before
     uploading.
   - Treat the returned URL as a secret-bearing link because the password is in
     the query string.
3. Use HTMLDrop only for renderable artifacts. If the user asks to share raw
   source, logs, JSON, CSV, or other non-renderable files, first create a small
   HTML or Markdown wrapper when that matches the request; otherwise explain
   that this skill is for HTML/Markdown previews.

## Command

Run the published CLI through `npx`:

```bash
npx -y htmldrop-cli "<file>"
```

The bare form creates a new preview. The explicit create form is equivalent:

```bash
npx -y htmldrop-cli create "<file>"
```

The CLI accepts relative paths, absolute paths, `~/...`, and `file://` URIs.
Quote the path so spaces are handled correctly.

If a local file is literally named `create` or `update`, use the explicit
create form with a path, for example `npx -y htmldrop-cli create ./update`.

To check the installed CLI version:

```bash
npx -y htmldrop-cli --version
```

Previews are private by default: only the password-bearing link opens them.
When the user wants a link that opens without a password (a public post, a
job ad, anything meant to be forwarded freely), pass `--public`:

```bash
npx -y htmldrop-cli --public "<file>"
```

By default a preview renews when opened: it is deleted after 14 days without
a visit, and each visit restarts those 14 days, up to at most one year after
the upload. `--expires <days>` sets the window to 1 to 30 days; use it when the
user asks for a longer (or shorter) lifetime:

```bash
npx -y htmldrop-cli --expires 30 "<file>"
```

When the user needs the page gone on a date whether or not anyone opens it
("delete it in 3 days", "make sure it disappears after the meeting", anything
time-boxed), or says not to renew it on visits, add `--no-renew`. The preview
is then deleted on the date, opened or not:

```bash
npx -y htmldrop-cli --expires 3 --no-renew "<file>"
```

These flags also work with `update`; `update --private` makes a public preview
private again, and `update --renew` (or `settings --renew`) turns renew-on-visit back on after
`--no-renew`. Without a renew flag, `update` keeps the preview's current
setting. Do not pass `--public` unless the user asked for a public or
password-free link, and do not pass `--no-renew` unless the user asked for a
fixed deletion date or for no renewal on visits.

To change who can open a live preview, or how long it lives, without uploading
it again, use `settings` with the full password-bearing URL:

```bash
npx -y htmldrop-cli settings "https://baseurl.ai/<id>?p=<password>" --public
npx -y htmldrop-cli settings "https://baseurl.ai/<id>?p=<password>" --private
npx -y htmldrop-cli settings "https://baseurl.ai/<id>?p=<password>" --expires 30
npx -y htmldrop-cli settings "https://baseurl.ai/<id>?p=<password>" --no-renew
```

`settings` needs at least one of `--public`, `--private`, `--expires`,
`--renew` or `--no-renew`. A new `--expires` counts from now; changing only
visibility or the renew setting keeps the current expiry date.
The page content and its URLs stay the same, and nothing is overwritten, so
`settings` does not need the update confirmation gate below. Prefer it over
`update` whenever the user only wants to change access or lifetime.

Use `--no-inline` only when the user explicitly wants references left as-is or
when the default inlining makes the upload too large:

```bash
npx -y htmldrop-cli --no-inline "<file>"
```

To overwrite an existing preview while keeping the same URL, pass the full
password-bearing URL back to the CLI:

```bash
npx -y htmldrop-cli update "https://baseurl.ai/<id>?p=<password>" "<file>"
```

Before running any `update` command, complete one blocking confirmation gate
unless the same user request already names the exact target URL, includes its
password, names the local file, and explicitly says to overwrite, update, or
replace that URL.

- Use the harness's blocking question tool: Claude Code `AskUserQuestion`,
  Codex `request_user_input`, or the equivalent blocking ask in another
  harness.
- Show the target URL, the local file that will replace it, and this statement:
  "This irreversibly overwrites the existing HTMLDrop preview at that URL."
- If the target URL is missing `?p=<password>` or the password is otherwise not
  available, ask for the password in that same blocking interaction instead of
  asking once for the password and again for confirmation.
- Run `update` only after an explicit yes and a non-empty password. If the
  answer is no, unclear, lacks a needed password, or no blocking ask is
  available, do not update; offer a fresh upload that creates a new URL instead.

`update` is a destructive overwrite: anyone with the full URL can view the
page, and anyone using that same full URL to update can replace its content.

Old `--update <url> <file>` instructions are obsolete. Use
`update <url> <file>` instead.

## Migrating Comments on Update

A preview can carry reviewer comments anchored to quoted text. When you
overwrite a preview whose document you edited, the quoted text may have moved or
changed, so the anchors should be migrated. The viewer falls back to re-finding
each quote at render time, but only an agent that edited the document knows
where a reworded passage went, so the agent owns the semantic remap. The CLI
only transports it; remapping is never automatic or guaranteed.

Do this only when overwriting a preview that has comments, and still complete
the destructive-update confirmation gate above.

1. Fetch the current comments before editing:

   ```bash
   npx -y htmldrop-cli comments "https://baseurl.ai/<id>?p=<password>"
   ```

   This prints a JSON array. Each root comment has `cid`, `anchor`
   (`{ "exact", "prefix", "suffix" }` or `null`), `author`, `text`, `resolved`;
   replies carry `parentId`.

2. For each root comment, find the corresponding passage in the new local file
   and build a fresh anchor: `exact` is the new quoted text, `prefix`/`suffix`
   are the text immediately before/after it (a few words each).

3. Write a JSON array of remaps to a file, for example `anchors.json`:

   ```json
   [
     { "cid": "<cid>", "anchor": { "exact": "new quote", "prefix": "...", "suffix": "..." } },
     { "cid": "<cid-gone>", "anchor": null }
   ]
   ```

   Use `"anchor": null` to mark a comment whose target no longer exists, or omit
   that `cid` entirely. Do not invent an anchor when the new document has no
   reliable matching quote.

4. Update with the remaps:

   ```bash
   npx -y htmldrop-cli update "https://baseurl.ai/<id>?p=<password>" "<file>" --comment-anchors anchors.json
   ```

Unknown or reply `cid`s in the file are ignored by the service. Omitting
`--comment-anchors` leaves the existing anchors untouched (the viewer then
relies on text-quote fallback, orphaning anchors it can no longer locate).

## Verified CLI Behavior

- Markdown files (`.md`, `.markdown`) are rendered to GitHub-flavored HTML
  before upload.
- Relative `<img src>`, `<link href>`, and `<script src>` references are
  inlined by default. Remote URLs, data URLs, fragment links, and JavaScript
  URLs are left alone.
- `--no-inline` leaves local references untouched.
- The service accepts a page up to 50 MiB (UTF-8 bytes after rendering and
  inlining). Asset inlining and Markdown rendering can make the final payload
  larger than the original file.
- The upload response contains a URL shaped like
  `https://baseurl.ai/<id>?p=<password>`. By default a link is deleted after
  14 days without a visit (or the `--expires <days>` value, 1 to 30), each
  visit restarts that window, and it is kept at most one year after the
  upload. With `--no-renew` it is deleted on the date, opened or not.
- With `--public` the CLI prints two stdout lines: first the bare
  `https://baseurl.ai/<id>` that anyone can open, then the password link, which
  is the edit link (needed for `update` and `comments`).
- `update <url> <file>` sends the `id` and password from that URL with the new
  content, returns the same URL, restarts the expiry window, and keeps the
  preview's visibility, lifetime, and renew setting unless `--public`,
  `--private`, `--expires`, `--renew`, or `--no-renew` say otherwise.
- `settings <url>` changes visibility, expiry, and/or the renew setting in
  place (`--public`, `--private`, `--expires`, `--renew`, `--no-renew`) and
  prints the same lines as an upload: the shareable URL first, then the edit
  link if the preview is public.
- `--version` prints the installed `htmldrop-cli` version and exits without
  uploading.
- Unknown options fail before upload. Use `--` before the file path when a local
  filename starts with `-`.
- In non-interactive shells the CLI prints the URL on stdout. In an interactive
  TTY it also prints `id`, an expiry, and a clipboard note when `pbcopy`
  succeeds. The expiry reads `expires: <date> if unopened (renews on visit,
  until <date>)` for a renewing preview, `expires: <date>` for a fixed one, and
  `expires: never` for a pinned one.

## Handling Output

Read both stdout and stderr from the command.

- The first stdout line is the shareable URL. Give that URL to the user.
- If there is a second stdout line (you passed `--public`), it is the edit
  link with the password. Tell the user the first link is public and the
  second one is for updating; do not present the second one as the link to
  forward.
- If you used `update`, say the existing preview was overwritten at the same
  URL.
- If you used `settings`, say what changed (now public, now private, the new
  expiry, or renew on/off) and that the content and link are unchanged. After
  `--private`, the bare public URL no longer opens the page.
- Mention the expiry in plain words, using the days you asked for (14 unless
  `--expires` was used):
  - Default (renews on visit): "deleted after 14 days without a visit; each
    visit restarts that." If the CLI printed `if unopened (renews on visit,
    until <date>)`, you may add that it is kept at most until that last date.
  - With `--no-renew`: "deleted on <date>, opened or not." Relay the exact date
    only if the CLI printed one; otherwise say "in N days".
  - Do not invent an exact timestamp the CLI did not print.
  - If it printed `expires: never`, the page was pinned by an operator: say the
    link does not expire and skip the expiry note.
- For a private preview, say the link is self-authenticating because the
  password is already in the URL. Do not print the password separately unless
  the user asks.
- Only say the URL was copied to the clipboard if the CLI actually printed the
  clipboard message.
- If stderr reports asset warnings such as `not found`, surface them. A URL may
  still be created, but unresolved local references can make the remote preview
  incomplete.

Suggested final response:

```text
Uploaded: <url>
The link includes the access password and can be forwarded as-is. It is
deleted after 14 days without a visit; each visit restarts that.
```

Add a short warning line when relevant:

```text
Warning: 2 local assets were not found during upload, so the remote preview may
be missing those images or styles.
```

## Troubleshooting

- `file not found`: re-check the path with `ls -l` or use an absolute path.
- unknown option: re-check the flag spelling.
- `markdown conversion failed`: the CLI could not render Markdown through
  `marked`; report the exact error and ask whether to install or use an HTML
  export instead.
- `File too large` or HTTP `413`: the final HTML payload exceeded the service
  limit. Try `--no-inline`, reduce embedded assets, split the report, or create
  a smaller summary page.
- `update` or `settings` with a malformed URL, missing `?p=...`, or HTTP
  `403`: re-check that the user provided the original full HTMLDrop URL (for a
  public preview, the edit link, not the bare public one). Do not try to
  recover the password from a clean preview URL.
- `settings failed (409)`: the page was re-uploaded while its settings were
  being saved. Run the same `settings` command again.
- Old `--update <url> <file>` examples fail on the 0.2 CLI. Rewrite them as
  `update <url> <file>`.
- If the CLI says the installed htmldrop skill is outdated, run
  `npx skills update htmldrop`, then retry.
- `upload failed`: report the exact status and stderr. Do not claim a URL was
  created unless stdout contains one.
- Asset warnings: if the preview needs to be portable, resolve missing local
  assets and upload again.
