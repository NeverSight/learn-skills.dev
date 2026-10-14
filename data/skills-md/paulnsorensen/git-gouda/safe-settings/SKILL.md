---
license: MIT
name: safe-settings
description: >
  Set up GitHub's `safe-settings` (a Probot-based GitHub App from the
  github org) for declarative, org-wide repository policy as code. Use when
  the user says "settings as code", "safe-settings", "manage repos
  declaratively", "centralize repo settings", "org-level branch protection",
  "scaffold an admin repo", "github settings app", or invokes
  /safe-settings on an org that wants to manage repo settings, branch
  protection, rulesets, labels, teams, environments, and collaborators
  from one admin repo. Scaffolds the admin-repo layout (`settings.yml` +
  `suborgs/` + `repos/`), the GitHub App installation steps, and a
  scheduled `full-sync` GitHub Actions workflow. Distinct from /gh-bootstrap
  (one-shot `gh api` config of a single repo) — this skill is for
  **org-scale settings as code** that reconciles continuously. Not for
  per-task GitHub ops (PRs, issues, CI status) or local git work — those
  are out of this catalog's scope.
---

# safe-settings

Onboard [`github-community-projects/safe-settings`](https://github.com/github-community-projects/safe-settings) — a Probot GitHub App that reconciles repo settings, branch protection, rulesets, labels, teams, environments, and collaborators from YAML files in a single admin repo.

Use this skill when an org wants to manage repository policy declaratively at scale, instead of clicking through each repo's settings page or running `gh api` one-shot scripts.

## When to reach for safe-settings vs alternatives

| Situation | Tool |
|---|---|
| Single repo, one-time policy lockdown | `/gh-bootstrap` (gh CLI, imperative) |
| Many repos, central policy that must stay in sync, drift detection, dry-run on PR | safe-settings (this skill) |
| Per-task GitHub ops (PRs, issues, CI status) | out of this catalog's scope |

safe-settings is **the right answer when policy is shared across repos** and you want PRs + dry-run gating on policy changes themselves. It's overkill for a single repo.

## What gets configured (by safe-settings, after this skill runs)

- Repo metadata (description, homepage, topics, visibility, default branch, feature toggles)
- Merge button settings (squash / merge / rebase, delete-on-merge, auto-merge, update-branch)
- Security toggles (vulnerability alerts, automated security fixes)
- Branch protection (classic) and rulesets (modern)
- Labels (with rename via `oldname`, exclusion patterns)
- Milestones
- Collaborators (per-user, with `include` / `exclude` repo lists)
- Teams (with permissions, visibility)
- Environments and deployment rules
- Custom properties
- Autolinks (Jira-style references)

The same YAML schema is layered org → suborg → repo, with repo-level files taking precedence.

## Protocol

### 1. Pick the admin repo and confirm scope

safe-settings reads its config from a single **admin repo** in the org. Two common layouts:

| Admin repo | When |
|---|---|
| `<org>/.github` | Quickest — the org already has this repo for community health files. Set `ADMIN_REPO=.github`. |
| `<org>/admin` (dedicated) | Cleaner for large orgs where a dedicated policy team owns the repo. Set `ADMIN_REPO=admin`. |

Confirm with the user:

- Org name (`gh api user --jq '.login'` if it's a user, `gh api orgs/<org>` to verify org)
- Admin repo choice (`.github` is the common default)
- Sub-org grouping needed? (e.g. group repos by team for different policy)
- Will deployment be **GitHub Actions cron** (simplest) or **hosted Probot app** (real-time webhooks)?

### 2. Scaffold the admin repo layout

The standard layout under the admin repo:

```
<admin-repo>/
└── .github/
    ├── settings.yml              # org-level baseline — applies to all repos
    ├── suborgs/                  # optional — overrides for groups of repos
    │   └── <suborg-name>.yml
    └── repos/                    # optional — per-repo overrides
        └── <repo-name>.yml
```

Files to copy from `assets/`:

- `assets/settings.yml` → `.github/settings.yml` — minimal, opinionated org baseline (see below)
- `assets/suborg.yml` → `.github/suborgs/example.yml` — commented sub-org template
- `assets/repo.yml` → `.github/repos/example.yml` — commented per-repo override template

The org baseline in `assets/settings.yml` mirrors the gh-bootstrap defaults: squash-only merging, PR-title commit subjects, and delete-on-merge. Its ruleset starts disabled; narrow the repository selector, observe real check names, and obtain explicit authorization before activation. Add a merge_queue rule only when the target organization and plan support it. Read `references/schema.md` for the full key catalog and layering behavior.

### 3. Choose the deployment path

#### GitHub Actions cron (recommended starting point)

- Lowest setup cost — no hosting, no webhook tunnel
- Reconciles every N hours via `npm run full-sync`
- Drift gets fixed within the cron interval, not in real time
- Copy `assets/full-sync.yml` → `<admin-repo>/.github/workflows/safe-settings.yml`

#### Hosted Probot app

- Real-time response to webhook events (push to `.github/settings.yml`, repo created, etc.)
- Needs hosting (AWS Lambda, Docker, Heroku, k8s) and a public URL for webhooks
- Use this once the cron path is proven and the org wants instant reconciliation
- See `references/deploy.md` for the deployment matrix and env-var reference

The skill defaults to the GHA cron path. Only switch to hosted if the user asks.

### 4. Create the GitHub App

Both deployment paths need a GitHub App installation. Walk the user through the manifest flow:

1. Clone safe-settings locally: `git clone https://github.com/github-community-projects/safe-settings`
2. `cd safe-settings`
3. `cp .env.example .env`, set `GH_ORG=<org>`
4. `npm install && npm run dev`
5. Open the printed URL → "Register a GitHub App" → install on the org
6. Save these values:
   - **App ID** → `vars.SAFE_SETTINGS_APP_ID` (repo or org variable)
   - **Private key** (downloaded `.pem`) → `secrets.SAFE_SETTINGS_PRIVATE_KEY` (paste the file contents)
   - **Client ID** → `vars.SAFE_SETTINGS_GITHUB_CLIENT_ID`
   - **Client secret** → `secrets.SAFE_SETTINGS_GITHUB_CLIENT_SECRET`
   - **Webhook secret** → `secrets.SAFE_SETTINGS_WEBHOOK_SECRET` (only needed for hosted Probot)

The GitHub App needs admin access to the org's repos to manage settings. The manifest flow requests the right permissions automatically — don't hand-roll the permission list.

### 5. Wire and test

For the GHA path:

```bash
# Set the variables and secrets on the admin repo (or org-wide).
gh variable set SAFE_SETTINGS_GH_ORG --body "<org>" --repo "<org>/<admin-repo>"
gh variable set SAFE_SETTINGS_APP_ID --body "<app-id>" --repo "<org>/<admin-repo>"
gh variable set SAFE_SETTINGS_GITHUB_CLIENT_ID --body "<client-id>" --repo "<org>/<admin-repo>"
gh secret set SAFE_SETTINGS_PRIVATE_KEY --repo "<org>/<admin-repo>" < private-key.pem
gh secret set SAFE_SETTINGS_GITHUB_CLIENT_SECRET --repo "<org>/<admin-repo>"
```

Trigger the first sync manually via `workflow_dispatch`:

```bash
gh workflow run safe-settings.yml --repo "<org>/<admin-repo>"
gh run watch --repo "<org>/<admin-repo>"
```

Check the run output. The first `full-sync` reconciles repositories immediately and logs the changes it applies. Confirm the affected organization and settings scope before this first run.

### 6. Validate guardrails

safe-settings can provide two safety nets, but the deployment must wire them:

- **Hosted-app PR dry-run** — the hosted Probot webhook path can post a status check for settings changes. The default cron and `workflow_dispatch` workflow does not provide this PR guardrail. Report it as unavailable unless the hosted path is configured.
- **Validators** — `assets/settings.yml` includes a `validator.pattern` for repo names. It only adds a `validation-error` topic to a mis-named repo; it does not block settings reconciliation. To exclude a repo from sync, configure the deployment's `restrictedRepos` setting instead.

For a more rigorous setup, add `enforcement: evaluate` on new rulesets to test them in shadow mode before flipping to `active`. See `references/schema.md`.

## Idempotency

safe-settings is reconciliation-shaped — running `full-sync` on an unchanged config is a no-op. The skill itself is also idempotent:

- File scaffolding: diff against `assets/` templates and ask before overwriting any existing file
- Variables/secrets: `gh variable set` and `gh secret set` are idempotent (last write wins); the skill should ask before overwriting an existing value
- The GHA workflow file: same diff-and-ask treatment

Re-running the skill on a partially-set-up admin repo should fill in only the missing pieces.

## What this skill is NOT for

- Setting policy on a single one-off repo with no org behind it — use `/gh-bootstrap`
- Running PR / issue / CI ops, or local git work — out of this catalog's scope
- Authoring new safe-settings rules upstream — this skill consumes the released app, doesn't develop it
- Migrating from the older `github/settings` app — safe-settings is the supported successor; the skill assumes you're starting fresh or already off `github/settings`

## Gotchas

- The admin repo path matters. By default safe-settings looks for config under `.github/` in `ADMIN_REPO`; if you put it elsewhere, set `CONFIG_PATH` to the directory.
- The GitHub App needs **admin** access to manage settings on member repos. A user-installed token won't cut it — it has to be the App, installed on the org.
- `full-sync` via GHA visits every repo installed for the App on every run — suborg files only select which override applies per repo, they do not narrow the set of repos visited. For huge orgs (>1000 repos) the run can take an hour and burn Actions minutes — configure the deployment's `restrictedRepos` setting or install the App on fewer repos to cut the workload.
- The same YAML key can mean different things at different layers. `branches` at org level applies to every repo; at repo level it overrides only that repo. The merge order is deep — read `references/schema.md` before writing complex overrides.
- The org-level `settings.yml` asset ships with rulesets disabled and a narrow `repository_name.include: ["example-repo"]` placeholder. Replace it with an observed, narrow selector and obtain explicit authorization before activation; active org rulesets cannot be weakened by lower-scope files.
- `settings.yml` ships its `labels` block commented out. It reconciles by deleting every unlisted label org-wide during `full-sync`. Before enabling it, inventory existing labels across the org and get the operator's approval for the include/exclude list.
- Before the first sync, protect the admin repo itself: an active ruleset on its default branch with at least one required review and code-owner review for the config paths, plus a `CODEOWNERS` file, and confirm who has write access. The admin repo is the trust boundary — anyone who can push to it controls every repo in the org through the App.
- `force_create: true` in a `repos/<name>.yml` will create the repo if it doesn't exist. This is powerful and dangerous — use it deliberately.
- safe-settings does not unset every API field by default. `labels.exclude` preserves matching labels; it does not delete them. To remove a collaborator, you typically delete the entry and run sync. Read the schema before assuming "remove from YAML" means "remove from GitHub".
- The merge queue is a `merge_queue` rule inside a `rulesets` entry — not a top-level toggle. Same shape as `/gh-bootstrap`'s ruleset payload, just expressed in YAML and applied org-wide.
