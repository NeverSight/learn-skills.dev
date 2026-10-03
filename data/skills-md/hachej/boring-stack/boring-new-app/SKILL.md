---
name: boring-new-app
description: Set up a new app repository for the Boring Factory end to end — create it from the app template (hachej/boring-app), set its secrets and settings, invite the expert, verify the first runs, and hand the expert their next steps. Use when the maintainer asks to create, bootstrap or set up a new app or repository for the Factory, or to connect an existing repository to it.
---

# Set up a new app repository, end to end

You act for the **maintainer** (the person who owns the Factory). The result is a
repository where the expert's agent can start a feature and the Factory takes
it from there. Do every step yourself; ask the person only for the decisions
below and for what needs their browser.

## 0. Decide with the person (one message, all at once)

- **Repository**: `OWNER/NAME` (new) — or an existing repository (then go to §6).
- **Title** of the app.
- **Runtime**: `vm` (a container on a host you own; agents run in the app) or
  `cloudflare` (a Worker with D1; its agents are declarative and run by the
  hub, no agent with code, no job). Default `vm`.
- **Expert**: their GitHub login. It must not be the bot's account (GitHub
  forbids approving your own pull request, and the bot opens contract PRs).
- **Bot**: the account whose token is `FACTORY_TOKEN` (default: the maintainer).

## 1. Preconditions (check, fix what you can)

```bash
gh auth status                       # signed in as the maintainer, scopes repo + workflow
gh auth setup-git                    # git (and npx github:…) use gh's credentials
gh api repos/hachej/boring-factory --jq .full_name    # read access to the factory
gh api repos/hachej/boring-app --jq .is_template      # the app template: must print true
gh api repos/hachej/boring-factory/actions/permissions/access --jq .access_level   # must be "user"
```

If the access level is not `user`, other repositories cannot call the
factory's workflows: `gh api -X PUT repos/hachej/boring-factory/actions/permissions/access -f access_level=user`.

Ask the person to confirm once (cannot be checked with a token):
- the **Claude GitHub App** is installed with access to **all repositories**
  (https://github.com/apps/claude) — otherwise install it on the new repo;
- for Cursor workers: **Cursor's GitHub integration** sees the repository and
  on-demand usage is enabled (https://cursor.com/dashboard).

## 2. The three secrets

Never print a secret; pipe it into `gh secret set`.

| Secret | Where it comes from |
|---|---|
| `FACTORY_TOKEN` | The bot's token. When the bot is the signed-in maintainer: `gh auth token` |
| `CURSOR_API_KEY` | The maintainer's Cursor key (from your secret store) |
| `CLAUDE_CODE_OAUTH_TOKEN` | Only the person: `claude setup-token` on their machine (Claude Pro/Max). Never ask them to paste it into the chat: they run `gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo OWNER/NAME` themselves, or export it before §3 |

Export what you can before §3 so that `init` sets them:

```bash
export FACTORY_TOKEN="$(gh auth token)"
export CURSOR_API_KEY="…"            # read from your secret store, never echoed
```

## 3. Create the repository

Dry run first, read the plan back to the person in three lines, then create:

```bash
npx -y github:hachej/boring-factory init OWNER/NAME --expert EXPERT --bot BOT --title "TITLE" --runtime vm
npx -y github:hachej/boring-factory init OWNER/NAME --expert EXPERT --bot BOT --title "TITLE" --runtime vm --yes
```

`init` creates the private repository from the template hachej/boring-app
(`gh repo create --template`), pushes one commit that makes it this app (name,
title, port, runtime: `scripts/init-app.mjs` keeps only `deploy/<runtime>/`;
CODEOWNERS; the expert in `project.md`), applies the labels and settings,
invites the expert, sets the secrets found in the environment and the
`FACTORY_BOT` variable. Then set any secret it reports missing (§2). The app
carries no skills and pins nothing: its workflows call boring-factory at `@main`.

Production is set up later, by hand, from `deploy/<runtime>/DEPLOY.md` in the
app; `init` prints the commands. On Cloudflare the production token lives only
in the GitHub environment `production` (restricted to `main`), never as a
repository secret, and previews use a separate account's token.

## 4. Verify, do not assume

```bash
gh secret list --repo OWNER/NAME                     # the three names
gh variable list --repo OWNER/NAME                   # FACTORY_BOT
gh label list --repo OWNER/NAME --limit 100 | wc -l  # 26 or more
gh api repos/OWNER/NAME/invitations --jq '.[].invitee.login'
gh run list --repo OWNER/NAME --limit 5
```

The first `ci` run on `main`:
- `paths` is **red, expected**: the customising commit was pushed straight to `main`.
- `check` must be **green**. If it is red, read `gh run view <id> --log-failed`,
  fix the cause **in the template, hachej/boring-app,** first (it will hit
  every new app), then in the app through a pull request.

## 5. Hand over to the expert

Send the person this, filled in:

> Accept the invitation to OWNER/NAME, then on your machine:
> `npx skills add hachej/boring-stack --skill boring-pm -g` and `gh repo clone OWNER/NAME`, open your
> agent (Claude Code, Codex or Cursor) inside the clone and describe what you want.

Tell the maintainer what to watch: the **factory** workflow in the Actions tab
(`context → ci → triage → checks → gates → build`), triage's one comment per
event, and the checks `boring/ci` and `boring/proof` on each pull request.

## 6. An existing repository instead

```bash
npx -y github:hachej/boring-factory sync OWNER/NAME --dry-run
npx -y github:hachej/boring-factory sync OWNER/NAME --yes     # labels + the "Adopt the Boring Factory" pull request
```

The pull request adds only the files the repository lacks, copied from the
template (the `factory.yml` caller, forms, PR template, CODEOWNERS, the ask
rules, `project.md`). Fill `setup` and `check` in `project.md` on its branch,
merge it by hand once (the Factory is not active before it lands), then §2, §4,
§5. It is a one-shot adoption: nothing is tracked or bumped afterwards.

## When something fails

| Symptom | Cause | Fix |
|---|---|---|
| `factory / context` fails with `gh api …: Not Found (404)` | A factory bug or a token without access | Read the exact path in the log; if the token is fine, fix it in boring-factory's main (apps call it at `@main`) |
| A job says it cannot use `hachej/boring-factory/.github/workflows/…` | The factory's workflows are not shared | §1, access level `user` |
| `check` red on a fresh app | A template bug | Fix it in hachej/boring-app, then in the app |
| `check` refuses an agent on a Cloudflare app | An agent or chat with `index.mjs`, a job, or Node in server code | Make the agent declarative, or choose `runtime: vm` |
| Triage or the claude worker never runs | `CLAUDE_CODE_OAUTH_TOKEN` missing or expired | §2 |
| The expert cannot approve the contract PR | The expert is the bot's account | Use another account for the expert |
| A Cursor task fails at once | Cursor quota or GitHub integration | Enable on-demand usage; connect the repo; or label the task `builder:claude` |
| `npx github:hachej/boring-factory` cannot fetch | git has no credentials | `gh auth setup-git` |

Fix the cause in boring-factory (the process) or hachej/boring-app (the
template) when it is theirs, so the next app does not hit it; never patch only the app.
