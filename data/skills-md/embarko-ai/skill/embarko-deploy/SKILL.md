---
name: embarko-deploy
description: Deploys an application to Embarko, a managed hosting environment that builds your app automatically (no Dockerfile required) and makes it reachable at a generated URL. Use this whenever the user asks to deploy, redeploy, ship, push, or release an app, to make a deployed app do something on a timer (daily report, nightly clean-up), to change who is alerted when a deployed app goes down (email, Slack, webhook, phone), to store files for an app (user uploads, images, PDFs, a public link to a file), or to showcase / feature / list a deployed app on an Embarko showcase page (public or event).
---

# Embarko Deploy

Embarko hosts an app and gives it a live URL at `<app-name>.embarko.app`.
It builds from source automatically: no Dockerfile, no build configuration.

This skill adds one thing: `scripts/deploy.sh`, which does the whole deploy
for you. Everything else (how to talk to the person, what an app needs,
keeping it, managing it, Showcase, errors) is in the Embarko agent guide,
and the guide is the only copy. Open the one topic you need when you need
it:

| You need | Read |
| --- | --- |
| How to reply to the person, which route to use, whether the app fits | https://embarko.ai/docs/prerequisites.md |
| The whole flow, step by step | https://embarko.ai/docs/quickstart.md |
| What an app needs to run (PORT, 0.0.0.0, DATA_DIR, no Dockerfile) | https://embarko.ai/docs/deploy.md |
| An error code | https://embarko.ai/docs/errors.md |
| Keeping a temporary app | https://embarko.ai/docs/claim.md |
| Running something on a timer | https://embarko.ai/docs/schedules.md |
| Crash alerts: who is told when the app goes down, adding Slack, a webhook or a phone (M91), muting | https://embarko.ai/docs/alerts.md |
| The embarko.json file | https://embarko.ai/docs/embarko-json.md |
| Secrets, domains, logs, rollback, rename, delete | https://embarko.ai/docs/index.md (contents) |
| Storing files: uploads, generated PDFs, images, a public link for each | https://embarko.ai/docs/files.md |
| Showcase | https://embarko.ai/docs/showcase.md |
| Reporting a problem | https://embarko.ai/docs/feedback.md |

Every Embarko reply also carries `next` (the one thing to do now) and, when
there is more to know, `links.help` (the guide topic to read). Follow them.

## Deploy

```bash
./scripts/deploy.sh                 # the current directory
./scripts/deploy.sh path/to/app     # a specific directory
./scripts/deploy.sh . other-name    # a different app name
```

The script packages the app, names and versions it, uploads it, waits for
the build, and prints the live URL. It also checks first that Embarko is
reachable and that the app doesn't use unsupported storage. Don't replace
it with your own `tar`/`curl` calls.

- **Report the live URL only once the script exits 0.** A zero exit means
  the app is live.
- **Then do what it prints under `==> Next:`.** After a first deploy
  without a token that is keeping the app; on a failure, how to fix it.
- **`==> Keep it:`** is the claim link for a temporary app. Give it to the
  person: opening it and signing in keeps the app. It is printed once only.
- Deploying again is the same command. After the first deploy the script
  writes the app's id to `embarko.json` as `"appId"`, so every later deploy
  reaches the same app even if its name was changed in the dashboard. Keep
  the file and commit it with the app. When copying an app's code to start
  a new app, remove `"appId"` first: under a new name the deploy is refused
  with `app_id_mismatch` rather than overwriting the original.
- **`==> Changed outside this deploy:`** means the person changed something
  in the dashboard, e.g. renamed the app. The deploy still reached the
  right app; tell the person its current name and URL.

Optional settings:

| Variable | What it is |
| --- | --- |
| `EMBARKO_AGENT_NAME` | Your agent name in lowercase (`claude-code`, `claude`, `cursor`...). Filled in automatically inside Claude Code. |
| `EMBARKO_APP_TYPE` | A short label for what the app is (`portfolio`, `task management`...). Use it if you know; otherwise leave it out. |
| `DEPLOY_TOKEN` | The person's deploy token. Without one, the first deploy is temporary (24 hours) until kept. |

The script finds a token in `DEPLOY_TOKEN`, then in `~/.embarko/credentials`.
Once one is saved there, never ask the person for it again, and never print
it back.

## Run something on a timer

When the person wants something done at set times ("every Monday at 9",
"each night"), use schedules, not a cron library or crontab. Needs a
deploy token.

1. Put the job in a GET route, e.g. `/tasks/weekly-report`. Answer 2xx when
   it worked. Keep anything it must remember under `DATA_DIR`.
2. First line of that route: answer 401 unless `Authorization` is
   `Bearer ` + `process.env.CRON_SECRET`. Embarko creates that variable.
3. Add `embarko.json` to the app's top folder, in the person's time zone:

   ```json
   {
     "$schema": "https://embarko.ai/schema/embarko.json",
     "schedules": [
       { "cron": "0 9 * * 1", "path": "/tasks/weekly-report", "timezone": "Asia/Kolkata" }
     ]
   }
   ```

4. Deploy as usual. Once live, the script runs each schedule once and
   prints `ok` or the error. Fix and redeploy until every line says `ok`.

The file is the app's full list: edit it and redeploy to change times,
`"schedules": []` removes all. Never put secrets in it; use env vars. If
the script prints warnings, fix them before telling the person it's done.
Details: https://embarko.ai/docs/schedules.md and
https://embarko.ai/docs/embarko-json.md

## Connect another service

When the app's users need Slack, Google Sheets, a CRM or similar, don't
build and host that glue. Turn Integrations on and the app gets an
embedded integrations panel (viaSocket's prebuilt embed) where its users
connect tools and build their own flows. Needs a deploy token, and the
app must be claimed. Static sites can't use it.

**1. Turn it on.** Safe to repeat; a second call answers `alreadyEnabled: true`.

```bash
curl -sS -X POST "https://ship.embarko.ai/api/apps/$APP/integrations" \
  --oauth2-bearer "$DEPLOY_TOKEN" \
  -H 'Content-Type: application/json' -d '{"apply": true}'
```

This sets three env vars on the app: `INTEGRATIONS_ORG_ID`,
`INTEGRATIONS_PROJECT_ID`, `INTEGRATIONS_SECRET`.
`"apply": true` pushes them to the running app; without it they arrive
on the next deploy. They live on Embarko, not in the local `.env`: to run
the app locally, the person copies them from the app's App setup tab.

**2. Build the panel** by following viaSocket's skill. Download
https://flow.viasocket.com/documentation/skill.md to
`.claude/skills/viasocket-integrations/SKILL.md` inside the app folder
and follow it; keep it there for next time, and download it again if a
call in it fails. Use its prebuilt embed UI route. Add `viasocket-apps`
to the app's dependencies; Embarko's build installs it.

Two things differ on Embarko from what that skill says:

- **Don't ask the person for the org ID, project ID or secret.** Embarko
  already set them. Where viaSocket's skill reads `VIASOCKET_ORG_ID`,
  `VIASOCKET_PROJECT_ID` and `VIASOCKET_EMBED_SECRET`, use
  `INTEGRATIONS_ORG_ID`, `INTEGRATIONS_PROJECT_ID` and
  `INTEGRATIONS_SECRET` instead, in that order. Never hardcode them;
  never send the secret to the browser. To the person, say "Integrations",
  not viaSocket.
- **Its check script may not run in your sandbox.** If running downloaded
  code is blocked, skip the proof step and say so in your report.

Then decide who supplies each value (the app's code, the user in a
picker, or you per run) and who picks the action, and report each line
of the viaSocket skill's "Finished when" list.

`409 integrations_disabled_for_workspace`: the workspace has Integrations
off. Embarko has already emailed the workspace Owners about this app with
a link to turn it on; tell the person and do not retry until they say it
is on. `502` is worth retrying. Details:
https://embarko.ai/docs/integrations.md

## Store a file

Every app has a file store: PUT the bytes, get a public link back that
works until the file is deleted. Use it for files people open or download
(photos, PDFs, exports, images for the site); records still go in SQLite
under `DATA_DIR`.

From your terminal, with the deploy token (the app must be claimed):

```bash
curl -sS -X PUT "https://ship.embarko.ai/storage/apps/$APP/files/hero.png" \
  --oauth2-bearer "$DEPLOY_TOKEN" --data-binary @hero.png
```

Reply `201 {id, url, sizeBytes, contentType}`. The `url` is the link to
use. List `GET .../files`, room left `GET .../usage`, delete
`DELETE .../files/<id>`.

From inside the app, same call: Embarko sets `STORAGE_URL` (the base) and
`STORAGE_TOKEN` (the bearer, good only for this app's files) on every
server app, and the app's name is in `APP_NAME`. Read them from the
environment; never hardcode or print them. Save the returned `id` and
`url` with the record, and delete the file by `id` when the record goes.

Files are public to anyone with the link. Allowed types, plan limits,
`409 storage_quota_reached` and the other errors:
https://embarko.ai/docs/files.md

**Showcase tip.** A listing with an image gets opened far more. If the
person has no screenshot, offer to take one of the live app, upload it
here and put the `url` in `screenshotUrls` (see
https://embarko.ai/docs/showcase.md).

## No script, or no network

- `scripts/deploy.sh` missing: follow https://embarko.ai/docs/quickstart.md,
  which has the same deploy as two commands.
- The script says Embarko can't be reached: your environment is blocking
  it. Read the routes in https://embarko.ai/docs/prerequisites.md and tell
  the person the fix in one line.
