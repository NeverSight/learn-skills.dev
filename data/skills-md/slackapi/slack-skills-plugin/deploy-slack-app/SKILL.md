---
name: deploy-slack-app
description: Use when a developer wants to deploy, host, or run a Slack app somewhere it keeps working after the local process stops, or mentions Railway, Heroku, `railway up`, `git push heroku`, `slack deploy`, a `deploy` hook in `.slack/hooks.json`, hosting a Socket Mode or Request URL (HTTP) Bolt app, deploying from Windows, graduating an app out of a developer sandbox, or tearing down a deployed app.
---

# Deploy Slack App

Take a Slack app that already works locally and deploy it to a hosting provider as a separate Slack app, with its own app ID, that keeps running without the developer's machine. The local development app is unchanged, and **Step 5: Deploy** explains how the two coexist. This is the step after the `slack:test-slack-app` skill confirms the app responds.

The mechanism is the Slack CLI's `deploy` hook. Adding a `deploy` key to the project's `.slack/hooks.json` replaces Slack's own hosted deployment with a script of your choosing, and the CLI runs that script _after_ it has created and installed the deployed app. That ordering is the whole reason this approach is worth using: the app's bot and app-level tokens are already in the script's environment by the time it runs, so nothing here has to prompt for a secret or store one.

Two supported providers, both running the app as a long-lived worker process:

| Provider | Process type | Deploys from | Secrets | Current pricing |
| --- | --- | --- | --- | --- |
| Railway | Service, no port binding required | The working directory | Passed on stdin | <https://railway.com/pricing> |
| Heroku | `worker` dyno | A git push of committed code | Passed as arguments | <https://www.heroku.com/pricing> |

Railway is the better default, and the reasons are in **Step 2a: Choose a Provider**.

---

## Step 1: Check Prerequisites

### 1a. Detect the Slack CLI

Use the `slack:slack-cli` skill (**Step 1: Detect the Slack CLI**) to check whether the public Slack CLI is installed and resolve its command name. The fingerprint check, alias fallback, and install instructions all live there; do not duplicate them. Refer to the resolved command as `SLACK_CMD` throughout.

This matters more than it looks. Some machines have an unrelated internal tool named `slack` on the path, and running that instead produces confusing failures well into the deploy.

### 1b. Confirm the App Uses Socket Mode

**Read the app's manifest rather than asking.** The project already declares which mode it uses, so a question here is redundant. Check `manifest.json` for `settings.socket_mode_enabled`. If `.slack/config.json` sets the manifest source to `remote`, there is no local file, so read it with `SLACK_CMD manifest info` instead.

- **Socket Mode enabled:** continue. The app opens an outbound websocket to Slack, needs no public URL, and binds no HTTP port.
- **Socket Mode disabled, or the app uses a Request URL:** **stop here.** This skill does not cover Request URL apps yet, because a hosted Request URL app also needs a public address captured after the deploy and written back into the app manifest. Tell the developer plainly that this is the gap, and that converting the app to Socket Mode is the supported path today. Support may have shipped in a newer version of the Slack Skills Plugin, so ask the developer to update the plugin and try again. If they are already on the latest version, point them to <https://github.com/slackapi/slack-skills-plugin/issues/172> to add a reaction or comment.

If the manifest is ambiguous, read the app's entrypoint. A Bolt for JavaScript app constructed with `socketMode: true` and an `appToken`, or a Bolt for Python app started through `SocketModeHandler`, is a Socket Mode app.

### 1c. Confirm the Runtime Is Supported

This flow is verified on macOS and Linux. The deploy hook is a shell script, so a Windows developer needs a PowerShell equivalent that does not exist yet. On Windows, say so rather than letting the deploy fail partway through. WSL is a workable path in the meantime. Support may have shipped in a newer version of the Slack Skills Plugin, so ask the developer to update the plugin and try again. If they are already on the latest version, point them to <https://github.com/slackapi/slack-skills-plugin/issues/171> to add a reaction or comment.

---

## Step 2: Choose a Provider and a Team

Ask the developer two things the project cannot tell you: which provider to deploy to, and which Slack team to deploy into.

### 2a. Choose a Provider

Ask which provider, because cost is the thing the developer cannot infer from the project. Give the developer both pricing links from the table above so they can check current terms. **Do not fetch the pages or quote prices, plan names, or trial terms.** Providers change them often, and this skill can be installed long after it was written.

What does not change with the price list, and is worth saying:

- **Railway** is the default recommendation. It accepts secrets on stdin, so the tokens never appear in process arguments. It deploys the working directory, so a re-deploy needs no commit, and it needs no `Procfile`.
- **Heroku** fits when the developer already has an account, or a team standard that points there. It builds from git, so only committed code is deployed. Some accounts, including enterprise-managed ones, cannot own a personal app and must create it on a Heroku team. Personal apps and team apps can have different plans and billing, so ask which team to use rather than picking one: a shared team has a shared budget.

Say plainly that **both providers keep the app running continuously**, which is what a Socket Mode app requires. Always-on hosting is a paid service in the end, so expect it to cost something once any trial runs out.

Once the developer picks one, read that provider's reference file and follow it: `references/railway.md` or `references/heroku.md`. Each holds the install and authentication commands, the provider's own requirements for the project, and the environment variables its deploy script reads. **Step 4: Wire Up the Deploy Hook** works through them.

### 2b. Choose a Team

Run `SLACK_CMD auth list`. If it lists one team, use it. If it lists more than one, show the developer each team's name and ID and ask which one to deploy into.

**Never pick the team yourself.** Do not assume the standalone workspace or the Enterprise org, and do not reuse the team from `.slack/apps.dev.json`, which is often a developer sandbox. A wrong guess installs the app into a team the developer did not intend, and a later deploy to the right team creates a second Slack app.

---

## Step 3: Confirm It Works Locally First

**Do not deploy an app that has not been seen working.** A broken deploy and a broken app look identical in a provider's logs, and separating them afterwards costs far more than checking first.

Use the `slack:test-slack-app` skill to run the app with `SLACK_CMD run` and exercise at least one real surface, so there is a known-good behaviour to re-check after the deploy. Note which surface was used: the same one is the check in **Step 6: Verify the Deployment**.

---

## Step 4: Wire Up the Deploy Hook

Three things to set up. **Check whether each already exists before writing it**, because re-deploying an app is the common case and clobbering a developer's edited script is not recoverable.

### 4a. Prepare the Provider

Work through the chosen provider's reference file before writing anything, because the deploy script only checks these and stops. It cannot fix them.

- **Install and authenticate the provider's CLI.** Run its `whoami` check. Logging in opens a browser, so if the check fails, ask the developer to run the login command in their own terminal rather than running it yourself.
- **Settle the names and ownership with the developer.** For Heroku: a distinctive app name, and whether the app belongs to a team (`heroku teams`). For Railway: the workspace, if the account has more than one. These become environment variables on the deploy command in **Step 5: Deploy**.
- **Meet the provider's project requirements.** For Heroku, write the `Procfile` and commit it. For Railway, confirm the start command it will detect.

### 4b. Write the Deploy Script

Copy the provider's deploy script into the project's `.slack/` directory under the same name, then make it executable:

- Railway: `references/deploy-railway.sh` to `.slack/deploy-railway.sh`
- Heroku: `references/deploy-heroku.sh` to `.slack/deploy-heroku.sh`

For example, `chmod +x .slack/deploy-railway.sh`.

Each script is self-contained. It validates that both tokens arrived, reads the deployed app ID from `.slack/apps.json` for its log line, and then runs the provider's preflight, provision, configure, and deploy steps in order. There is nothing else to copy. The CLI runs the hook from the project root, so the script's relative paths resolve there even though the file lives in `.slack/`.

**If the script already exists**, show the developer that it is there and ask before overwriting. A developer may have adjusted it.

### 4c. Register the Hook

Add a `deploy` key inside the existing `hooks` object in `.slack/hooks.json`, pointing at the provider's script. For Railway:

```json
"deploy": "./.slack/deploy-railway.sh"
```

For Heroku, the value is `./.slack/deploy-heroku.sh`. **Leave the `get-hooks` entry exactly as it is.** Its value differs between Bolt for JavaScript and Bolt for Python projects, so do not copy one from elsewhere.

**If a `deploy` key is already present, do not add a second one.** A duplicate key produces invalid JSON, and the CLI will reject the project rather than deploy it. If the existing key already points at the chosen provider's script, leave it. If it points somewhere else, such as the other provider's script, show the developer and ask before changing it.

---

## Step 5: Deploy

Run `SLACK_CMD deploy` from the project root and watch the output. The CLI creates the deployed app, installs it, and then runs the hook script, so the first part of the output is app installation and the second is the provider's build.

Four flags matter when running this outside an interactive terminal, which includes most agent sessions. The CLI asks four questions, and each one is fatal unanswered: a non-interactive shell gets `The input device is not a TTY or does not support interactivity` and nothing is deployed.

- `--skip-update` stops the CLI pausing to offer an upgrade.
- `--team <team ID>` picks the workspace or organization. Use the team the developer chose in **Step 2b: Choose a Team**.
- `--app deployed` selects the deployed app environment, and creates that app on a first deploy. Without it the CLI asks the developer to choose between an existing app and a new one. This is the flag most easily missed, because the prompt it answers only appears on a project that has never been deployed.
- `--org-workspace-grant all` answers the workspace-grant prompt for an org-installed app.

So the full command is `SLACK_CMD deploy --skip-update --team <team ID> --app deployed --org-workspace-grant all`.

Put any provider variables settled in **Step 4a: Prepare the Provider** in front of it. The hook inherits the CLI's environment, so this is how they reach the script:

```sh
HEROKU_TEAM=<team> HEROKU_APP_NAME=<name> SLACK_CMD deploy --skip-update --team <team ID> --app deployed --org-workspace-grant all
```

**The deployed app is a different app from the one `SLACK_CMD run` uses.** The CLI writes the deployed app to `.slack/apps.json` and the local development app to `.slack/apps.dev.json`, keyed by team. Both keep working independently, which is the intended design, not a mistake to correct.

**Commit `.slack/apps.json` after the first deploy.** It holds app and team IDs, not secrets, and the project's `.slack/.gitignore` leaves it tracked on purpose. Committing it keeps every later deploy pointed at the same app. On Heroku it also stops the deploy script warning about uncommitted changes on each re-deploy.

One consequence to warn the developer about: the two apps declare the same slash commands in the same workspace. Running `SLACK_CMD run` while the deployed app is live makes it ambiguous which one answers a slash command. Stop the local process when checking the deployed app, which **Step 6: Verify the Deployment** does anyway.

---

## Step 6: Verify the Deployment

Check all three of these. The first two can pass while the app is silent in Slack.

### 6a. The Service Is Running

Use the status and log commands from the provider's reference file. Look for the app's own startup logging and the Socket Mode websocket connecting. A build that succeeded and a process that then exited look very different here, so read the logs rather than trusting the build result.

### 6b. The App Answers in Slack, With Nothing Running Locally

**Stop the local process first.** This is the only check that proves the deployed app is doing the work rather than the developer's laptop. Exercise the surface noted in **Step 3: Confirm It Works Locally First**, and confirm the response appears in Slack and the corresponding request appears in the provider's logs.

### 6c. Both Apps Are Distinct

Show the developer the app ID in `.slack/apps.json` and the one in `.slack/apps.dev.json` and confirm they differ. Then confirm `SLACK_CMD run` still drives the development app.

---

## Step 7: Re-deploy

Shipping a change is the same `SLACK_CMD deploy` command, with the same flags as **Step 5: Deploy**. Everything in **Step 4: Wire Up the Deploy Hook** is already in place, so skip it and go straight to the deploy, and expect the same app rather than a second one.

Two provider differences to know about, both handled by the deploy scripts:

- **Railway** uploads the working directory and rebuilds every time, so no commit is needed.
- **Heroku** builds from a git push, so uncommitted changes are not deployed. A push with no new commit builds nothing, so the script restarts the dynos instead, which picks up any changed tokens. Commit code changes before re-deploying.

If a re-deploy creates a second Slack app, the deployed app entry in `.slack/apps.json` was lost. Before deploying again, confirm `.slack/apps.json` has an entry for the `--team` ID, rather than deleting apps afterwards.

---

## Step 8: Tear Down a Deployment

Use this when the developer is done with the deployed app, for example after trying the skill out. It deletes the host's copy and the deployed Slack app, and leaves the development app alone.

**Name every resource and ask once before deleting anything.** These deletes are permanent. Say which provider project or app goes, and which Slack app ID from `.slack/apps.json`, then wait for a yes.

1. **Delete the provider's copy first**, so nothing is left holding a connection to Slack with tokens that are about to stop working. The commands are in the provider's reference file, under "Tearing down".
2. **Delete the deployed Slack app** with `SLACK_CMD app delete --team <team ID> --app deployed --force`. Read the team ID from `.slack/apps.json`. `--force` skips the confirmation prompt, which would otherwise fail in a non-interactive shell. When it was the only deployed app, the CLI removes `.slack/apps.json` as well, so commit that deletion.
3. **Leave the development app** unless the developer asks for it too. It is the app `SLACK_CMD run` uses, and they will usually keep working on it. If they ask, the same command with `--app local` deletes it.

Leave `.slack/hooks.json` and the deploy script in place, so a later `SLACK_CMD deploy` sets everything up again from the start.

---

## Notes

**Serverless providers cannot host a Socket Mode app.** A Socket Mode app is a process that stays resident and holds an outbound websocket open. Vercel, AWS Lambda, and similar platforms run per-request functions with a maximum duration and no always-on process type, so there is nothing for the websocket to live in. When a developer asks for one of these, explain the constraint rather than attempting it. Hosting a Slack app on a serverless platform means a Request URL app, which this skill does not cover yet.

**Other providers.** When a developer asks about a provider this skill does not cover, the two things to check are whether it offers an always-on background worker process type and how that process is billed.

**The token handoff is not a documented contract.** The Slack CLI does not pass the tokens to the deploy hook explicitly. It sets them on its own process during app installation, and the hook script inherits them because it runs later in that same process. It works, and it only works for apps with no Slack-hosted function runtime, which covers every Bolt app. That is why each deploy script checks for both tokens and stops with a readable message instead of assuming they are present.

**Not `slack deploy` without a hook.** With no `deploy` key in `.slack/hooks.json`, `SLACK_CMD deploy` targets Slack's own hosted infrastructure, which is a different product for a different kind of app. The `slack:slack-cli` skill covers the CLI's commands generally.

**Building the app comes first.** If there is no app yet, start with the `slack:create-slack-app` skill and come back here once it runs locally.
