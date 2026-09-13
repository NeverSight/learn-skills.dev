---
name: upstash-box-remote-work
description: Do work in an Upstash Box, a sandboxed cloud container driven through the remote Upstash MCP server (mcp.upstash.com), instead of on the local machine. Use when the user asks to run, build, test, clone, or edit something remotely, in a sandbox, in the cloud, or in a box, when the deliverable is a pull request, a public preview URL, or a screenshot of a running app, when the local machine cannot deliver (no GitHub login for gh, no way to expose a port, a dirty or slow local checkout), or when several independent tasks should run in parallel on separate machines, a code factory that turns a list of tasks into a list of pull requests. Applies whenever the session has the box_* and blob_* MCP tools, even when Upstash is not named.
---

A box is a sandboxed Linux container in the cloud with a shell, a filesystem,
git, an optional headless Chromium, and public URLs for its ports. Everything
here goes through the remote Upstash MCP server. There is no SDK to install
and no API key in the environment: the server forwards the session's OAuth
token to the Box API, and screenshot bytes travel from the box to Blob
without passing through the server.

## When to take work into a box

- The user asks for it: remote, in a sandbox, in the cloud, in a box, not on
  my machine.
- The deliverable is a **pull request**, a **public preview URL**, or a
  **screenshot** of the running result. A box has GitHub credentials, public
  ports and a browser; the local machine often has none of the three.
- The work needs isolation: untrusted or generated code, a heavy dependency
  install, a clean checkout, branches the local tree should not carry.
- The work scales out: several independent tasks, one box each, in parallel.

Once a task is in a box, do all of it there. The box's filesystem is not the
local one, so an edit made locally and a build run in the box act on two
different checkouts, and neither side reports the mismatch.

## Connect

The plugin already registers `https://mcp.upstash.com/mcp`, and the box and
blob tools are part of its default tool set. To add the server by hand:

```bash
claude mcp add --scope user --transport http upstash "https://mcp.upstash.com/mcp"
```

On first use the client opens the Upstash consent page. Pick the account or
team the boxes and buckets should live in, and **turn the read-only switch
off**: every step below except listing is refused with 403 on a read-only
grant.

## Tools

| Tool | Actions / purpose |
|---|---|
| `box_manage` | create, list, get, delete, pause, resume, fork |
| `box_exec` | run a shell command in the box (`command` is an argv array, `folder` is the working directory) |
| `box_git` | clone, status, diff, commit, checkout, push, create_pr |
| `box_preview` | create, list, delete public URLs for ports in the box |
| `box_browser` | goto, content, screenshot, tabs, tab_new, tab_close, live_view |
| `box_snapshots` | create, list, list_all, delete, restore (a new box from a snapshot) |
| `box_logs`, `box_runs` | what happened inside a box, and its run history |
| `box_apikey` | list, create, delete Box API keys for a deployed app or CI (the key outlives the OAuth grant, so tell the user to revoke it when done) |
| `blob_bucket` | list, create (create defaults to `visibility: public`) |
| `blob_upload_url` | presigned PUT URLs for paths in a bucket, plus `public_url` on public buckets |

## The flow: one task, one box

1. **Create.** `box_manage` `create`. Set `browser: true` if you will take
   screenshots or check pages. Use `ephemeral: true` with a `ttl` for
   throwaway work (no paid plan needed); use `keep_alive: true` when a preview
   URL must outlive the session (paid plan). Note the returned `id`.
2. **Clone with `box_git` `clone`**, never with `git` in `box_exec`. The clone
   is what writes the account's GitHub credentials into the box; without it
   `push` and `create_pr` fail with a bare 500. The checkout lands at
   `/workspace/home/<repo name>`. Pass that as `folder` on every later
   `box_exec` and `box_git` call: the default is the workspace root, which is
   not a repository.
3. **Work.** `box_exec` for install, build, tests, and the app itself. Each
   call waits for the command, so detach servers:
   `["sh", "-c", "( pnpm preview --host 0.0.0.0 --port 4321 > /workspace/home/app.log 2>&1 & )"]`,
   then poll the port with `curl` in a second call. Edit files with shell
   commands or a short script in `box_exec`, not with local file tools.
4. **Preview URL.** `box_preview` `create` with the `port`. The app must
   listen on `0.0.0.0`; a server bound to `127.0.0.1` answers curl inside the
   box and still gives 502 through the preview. The URL has the shape
   `https://<box-id>-<port>.preview.box.upstash.com`. Add `basic_auth` or
   `bearer_token` when the page should not be open to anyone with the link;
   the credential is returned once. Say in the reply how long the URL lives:
   an ephemeral box takes it down at `expires_at`.
5. **Screenshots.** `box_browser` `goto` the page on `http://localhost:<port>`,
   then `screenshot`. With no `path` the PNG comes back as an image you can
   look at; with a `path` it is written inside the box and only `{saved,
   bytes}` returns. Look while you work, save the ones that count, and pass
   `full_page: true` for long pages.
6. **Publish screenshots.** GitHub's attachment endpoint rejects the box's
   token, so images go through Blob. `blob_bucket` `list`, and `create` a
   **public** one if none fits (private buckets only serve short-lived
   signed URLs). `blob_upload_url` with `bucket_id` and
   `files: [{path: "<repo>/<branch>/after.png", content_type: "image/png", size: <bytes>}]`,
   minted right before use (a URL lives at most 10 minutes). Then `box_exec`
   the `curl_example` from the result, sending the returned headers verbatim
   (they are part of the signature). Bytes go straight from the box to storage.
7. **Pull request.** `box_git` `checkout` a branch, `commit`, `push` with the
   branch name, then `create_pr` with `base`, `title`, and a `body` that
   carries the preview URL and `![after](<public_url>)` for each screenshot.
   `create_pr` pushes nothing itself. Reply with the PR URL, the preview URL,
   and the screenshot URLs.
8. **Clean up.** `box_manage` `delete` (or `pause`) unless the user wants the
   box or its preview kept. Ephemeral boxes expire on their own.

## Scaling out

- One box per independent task. Create them with a shared `labels` entry,
  drive them in parallel, and `box_manage` `list` with `label` to find and
  delete them at the end. Never run two tasks in one box at once.
- When every task needs the same expensive setup (clone, dependency install,
  build cache), do it once, `box_snapshots` `create`, then `restore` one new
  box per task from the snapshot. `fork` does the same for an idle or paused
  non-ephemeral box.
- `size` is `small`, `medium` or `large`; pick it per task rather than
  oversizing all of them.
- A `live_view` URL lets a person watch a box's browser tab as it works
  (frames out, no input in); hand it over for long runs.

## Gotchas

- Read-only grant → 403 on create, exec, screenshot-to-path, git writes and
  upload URLs. Re-consent with read-only off.
- `box_git` `create_pr` fails if the account has no GitHub installation
  covering the repo; ask the user to connect GitHub in the Upstash console
  under Box settings.
- Prefer `box_git` `clone` over `clone_repo` on `box_manage` `create`: on an
  ephemeral box the option can be ignored, and on a persistent one it runs in
  the background with no completion signal beyond `box_logs`.
- Paths inside the box are relative to `/workspace/home` unless absolute.
  `ls /workspace` itself is denied (root-owned, mode 711).
- The `node` image has no corepack and boxuser cannot `npm i -g`, so a
  `packageManager`-pinned pnpm fails to self-install. Use
  `npx -y pnpm@<version>` or `export npm_config_manage_package_manager_versions=false`
  (the preinstalled pnpm); `sudo npm i -g pnpm@<version>` also works, sudo is
  passwordless.
- `blob_upload_url` headers are signed. A missing or changed `content-type`
  or `cache-control` → 403 from storage (`SignatureDoesNotMatch`). An expired
  URL → mint again.
- Bucket names are account-wide. Reuse one bucket such as `agent-proof` with
  per-repo prefixes rather than creating one per run.
- `box_browser` fails with "browser is not enabled for this box" unless the
  box was created with `browser: true`; there is no way to add it later.
