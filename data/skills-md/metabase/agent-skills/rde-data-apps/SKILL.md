---
name: rde-data-apps
description: >
  Build or change a Metabase data app on an rde machine: settles what the `metabase-data-app-*` skills need from the local setup (the remote-sync repository, the Metabase URL, the API key rde stores, how the app reaches Metabase), makes sure everything the app reads is Library content already synced into that repository, confirms every sync step with the user, and hands the build to them. Use only when an app is asked for explicitly: "build me an app for X", "create a data app", "make an internal tool / portal in Metabase", "add a page / a form / a filter to my data app". A dashboard, a question, or a metric is not an app; those stay with the `rde` skill.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# rde-data-apps

A data app is a React bundle Metabase serves at `/apps/<slug>` from `data_apps/<slug>/` in the repository connected through remote sync. The `metabase-data-app-*` skills build it. This skill answers their questions from what rde already knows, so the user is asked only what rde cannot know, makes sure the content the app reads is in that repository before the app is built, then hands over. Sections 4 to 6 override the data-app skills wherever they differ: the schema scope, the order of commits and pushes, and the confirmation before any sync.

## 1. The instance

`rde status --json`: `url` is the instance (not a secret) and `version` must be v65+ or a head build. `mb auth list --json` names the profile whose `url` matches; use it as `$PROFILE`. Metabase serves apps only under a license with remote sync and data apps: `rde doctor --json`, row `license`. Without one, the user activates it in their own terminal with `rde init --only license` (or `! rde init --only license` in this session); the token never enters the chat. Syncing content needs `remote-sync-type` set to `read-write` (`mb setting get remote-sync-type --json`); switching it is a sync change, confirmed like one (section 6).

## 2. The repository

`contentRepository` in `rde status --json` is the working directory of the remote-sync repository, and the answer to `metabase-data-app-setup`'s Step 1: name it and use it, do not ask. When it is null and the license has remote sync, ask where the repository should live, then run `rde init --only git-sync --git-dir <path> --git-remote local` (a bare remote inside `~/.rde`, no account). A hosted remote needs a git token, so the user runs `rde init --only git-sync` themselves. A repository rde creates already ignores `.env.local`, `node_modules/`, and the rest a data app must not push.

## 3. The credentials

The data-app skills read `DATA_APP_MB_URL` and `DATA_APP_MB_API_KEY` from `.env.local` at the repository root and forbid the key in the conversation. rde stores the API key `mb` uses, and `rde credentials --api-key` prints it alone. When the setup skill reaches its credentials step, or its check prints `MISSING`, fill the file with this command instead of asking the user, `<url>` from step 1 and `<repo>` from step 2. It prints only `creds written`, keeps the file's other lines, and makes sure `.env.local` is ignored:

```bash
ROOT="$(git -C "<repo>" rev-parse --show-toplevel)" && KEY="$(rde credentials --api-key)" &&
{ grep -qxF .env.local "$ROOT/.gitignore" 2>/dev/null || echo .env.local >> "$ROOT/.gitignore"; } &&
{ if [ -f "$ROOT/.env.local" ]; then grep -v -e '^DATA_APP_MB_URL=' -e '^DATA_APP_MB_API_KEY=' "$ROOT/.env.local"; fi
  printf 'DATA_APP_MB_URL=%s\nDATA_APP_MB_API_KEY=%s\n' "<url>" "$KEY"; } > "$ROOT/.env.local.tmp" &&
mv "$ROOT/.env.local.tmp" "$ROOT/.env.local" && chmod 600 "$ROOT/.env.local" && echo "creds written"
```

Never run `rde credentials --api-key` where its output comes back to you, and never print `.env.local`. The key belongs to rde's admin, so the dev preview sees every table; say so when the app is meant for a narrower audience.

## 4. The repository is the source of truth

A data app exists only through remote sync, so here it is a requirement, not a suggestion: section 2 sets it up when it is missing, and that is the only place rde proposes remote sync unprompted, because the user asked for an app. Record it in STATE.md as `remote_sync`. Outside an app, the `rde` skill raises syncing only when remote sync is already configured.


The bundle refers to Metabase objects by id and through the typed schema. An app built on content that lives only in the instance works there and nowhere else: importing the repository into another instance brings the app without the definitions it reads, and its queries fail. So everything the app reads is in the repository before the app is built, and everything the build creates goes there with the app.

- **What the app may read.** Library-published tables with their field metadata, measures, and segments; metrics filed in the Library's Metrics collection; models whose actions the app runs, in a synced collection. Nothing else.
- **What "in the repository" means.** The Library collections carry `is_remote_synced: true` (`synced_collections` in `mb git-sync status --json`), the content has been exported, and `git pull` has brought it into the working tree: the files are there under `databases/…/tables/<table>/` and `collections/…`, checked, not assumed.
- **Measures and segments need a published table** (the `rde` skill's `references/remote-sync.md`, "What belongs in git"). Without the Library (`mb library get --json` fails), file metrics in a synced collection and say that measures and segments cannot be carried.
- **The app's own collection is synced too.** `npm run build` runs `sync-resources`, which saves each `queries/` definition as a question in `Data App: <slug>`. Flag that collection for sync with the app, and after every build that creates or changes questions, `mb git-sync dirty --json` lists them for export. If they never appear there, say so in the hand-back rather than working around it.
- **Schema scope.** Generate `metabase.data.ts` from Library scopes only: `include-data-library=true`, `include-metric-library=true`, or `library-collections=<ids>`, plus `include-models=true` when the app runs actions. Never `database=<id>`: it reads tables straight off the instance, synced or not, and is how an app ends up built on content the repository does not have.
- **A missing entity found mid-build** (a measure, a segment, a metric, a published table, an action) goes back to the `rde` skill: create it in the Library, pass its gate, sync it (sections 5 and 6), `git pull`, regenerate the schema, then continue. Never create it ad hoc to unblock the UI.
- **Before the first line of app code**, every entity the app needs is in the schema generated from Library scopes and its file is in the working tree. When one is missing, stop and go back to `rde`.

## 5. Syncing safely

Remote sync merges nothing and resolves no conflicts. The instance side (what to check before every import or export, which goes first, never `--force` without the user's yes) and the staging hand-back: the `rde` skill's `references/remote-sync.md`, "Before each step" and "Staging". Here a `git push` behind a Metabase export is rejected too, and two writers push to the same remote, Metabase's export and the app's commits, so keep them in step:

- **Working-tree side.** The app's commits touch only `data_apps/<slug>/`; exported Metabase YAML is never edited by hand. Before pulling a Metabase export: `git stash --include-untracked`, `git pull --ff-only`, `git stash pop`. Before every `git push`: `git pull --ff-only` again. A pull that cannot fast-forward is a stop: report both histories, do not merge or force.
- **Delivery order**, each step starting from a clean state: `npm run build` (may create app questions) → export the instance's dirty set (the app's questions and any new definition) → stash, pull, pop in the working tree → commit the app, `resources_metadata.json` included → pull, push → `mb git-sync import` → open `<url>/apps/<slug>`.
- **Branch.** The instance tracks one branch (`mb git-sync status --json`, `branch`). Export or push to `main` or `master` only with an explicit yes; otherwise `mb git-sync create-branch agent/<slug>` and push the app to the same branch, so the content and the app travel together.

## 6. Ask before anything touches sync

Every sync step, every `git push` to the synced remote included, is approved first, one checkpoint per sync point: the `rde` skill's `references/remote-sync.md`, "Ask before every sync step". "Yes for the rest of this job" is recorded and not asked again; anything less is asked again at the next sync point.

"Not now" before the build leaves one path: a dev preview only, labelled as working on this instance alone and breaking wherever the repository is imported. Nothing is pushed to the synced branch until the content it reads is synced.

## 7. Hand off

One skill per step; follow it for the app's code, with sections 4 to 6 taking precedence:

| The step | Skill |
| --- | --- |
| No app yet: create, scaffold, set up | `metabase-data-app-setup` |
| The app reads Metabase tables, metrics, measures, or segments (the generated `metabase.data.ts`) | `metabase-data-app-semantic-layer`, with the Library scopes from section 4 |
| More than one page | `metabase-data-app-routing` |
| A write: a form, an update, a delete, a saved action | `metabase-data-app-actions` |

## 8. The data behind it

The app reads what the semantic layer publishes to the Library. A number it shows with no metric or measure behind it yet goes back to the `rde` skill first (its semantic-layer playbook, clean tables before that when the source is raw), then through sections 4 to 6 into the repository, so the app queries the definition by id and never re-derives it in `queries/`. When the `rde` skill keeps `./.scratch/STATE.md`, record there the app's slug, the ids it reads, the synced collections, and each sync decision.

## 9. Delivery

The setup skill ends with a commit and a push; make them in section 5's order, after section 6's question. With rde's local remote the push lands in the bare repository inside `~/.rde`; `mb --profile $PROFILE git-sync import --json` then brings the app into Metabase, and it opens at `<url>/apps/<slug>`. The hand-back names what was synced, to which branch, and at which commit.
