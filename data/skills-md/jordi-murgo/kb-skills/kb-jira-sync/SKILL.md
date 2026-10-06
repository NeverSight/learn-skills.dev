---
name: kb-jira-sync
description: >
  Refresh the vault's raw Jira data from the Jira REST API, then reconcile the
  derived wiki issue pages against it. Triggers on: "sync jira", "import jira",
  "refresh jira issues", "update the tickets", "/kb-jira-sync".
allowed-tools: Read Write Edit Bash Grep Glob
---

# kb-jira-sync: Refresh Jira Source Data

Two distinct stages. Do not conflate them:

1. **Import** — `.agents/skills/kb-jira-sync/scripts/import-jira.py` refreshes
   `.raw/jira/` from the API.
2. **Reconcile** — the wiki pages under `wiki/jira-issues/` are *derived*, and
   the import does not touch them. They go stale silently.

An optional **Stage 0 — Discovery** uses the `twg` CLI to find related Atlassian
content (linked issues, Confluence pages, Rovo search) that the import alone
misses. See [Stage 0 — TWG Discovery](#stage-0--twg-discovery-optional) below.

---

## Stage 0 — TWG Discovery (optional)

The [`twg` CLI](https://www.npmjs.com/package/@twg/cli) connects to Atlassian
Cloud via OAuth and provides graph traversal, semantic search (Rovo), and
context discovery that the flat REST API import cannot match.

**When to run it:** after the import, during the reconcile phase, when you
need to find issues or pages related to the project that are not in the
`.raw/jira/` output — cross-project links, Confluence docs, or semantically
related work items.

**Prerequisites:**

- `twg` installed (`curl -fsSL https://teamwork-graph.atlassian.com/cli/install | bash`)
- Authenticated against the project's Atlassian site

**Project-local credentials.** TWG supports `TWG_CONFIG_DIR` to store
credentials inside the project directory (gitignored) instead of the
global `~/.config/twg/`. This isolates per-project Atlassian sessions and
enables multi-site/multi-tenant workflows.

Setup (one-time, interactive — opens browser):

```bash
# Create the project-local TWG config directory
mkdir -p .twg

# Login against the project's Atlassian site
TWG_CONFIG_DIR=.twg twg login --site <site-prefix>

# Verify
TWG_CONFIG_DIR=.twg twg doctor
```

Add `.twg/` to `.gitignore` and `TWG_CONFIG_DIR=.twg` to `.env.local` (both
already gitignored). After that, all `twg` commands in this skill assume
`TWG_CONFIG_DIR` is set in the environment — either via `.env.local` or
exported in the shell.

**No `kb-config.yaml` section needed.** TWG reads its own auth from
`TWG_CONFIG_DIR` and resolves the site from the stored credentials.

### Commands

All commands assume `TWG_CONFIG_DIR=.twg` is set in the environment (via
`.env.local` or shell export). If not, prefix each command with
`TWG_CONFIG_DIR=.twg`.

```bash
# 1. Context graph of an issue — shows parent, children, sprints, links, assignee
twg context get BI2614-3

# 2. Semantic search across Jira (Rovo) — finds related issues by meaning, not text
twg rovo search "infrascan security" --app jira --limit 20

# 3. Confluence search — finds wiki pages related to the project
twg confluence search "project name" --limit 10

# 4. JQL query via TWG (richer relationship data than the import script)
twg jira workitem query --jql "project = BI2614 AND updated >= -7d ORDER BY updated DESC"

# 5. Work tree — rollup of a person's work across Jira, PRs, docs
twg work-tree <account-id>
```

### What TWG adds over the import script

| Capability | import-jira.py | twg |
|---|---|---|
| Issue fields + comments | ✅ | ✅ |
| Parent/child relationships | flat field | ✅ graph traversal |
| Cross-project issue links | ❌ | ✅ `context get` |
| Semantic search (Rovo) | ❌ | ✅ `rovo search` |
| Confluence pages | ❌ | ✅ `confluence search` |
| Sprint membership | ❌ | ✅ `context get` |
| Person work rollup | ❌ | ✅ `work-tree` |

### How to use it in the reconcile phase

1. Run the import (Stage 1) as usual.
2. For each new or modified issue, run `twg context get <KEY>` to discover
   relationships the flat import misses — cross-project links, sprint
   membership, related Confluence pages.
3. If the context graph surfaces issues outside the project key, note them
   as cross-references in the wiki page (do not import them into `.raw/jira/`
   — they belong to other projects).
4. If Confluence has pages about the project, ingest them via `wiki-ingest`
   as additional sources.

### When TWG is not available

If `twg` is not installed, not authenticated, or `.twg/auth.conf` is missing,
the reconcile phase proceeds normally without it. TWG is a discovery
accelerator, not a dependency. The import script and the wiki reconcile work
standalone.

```bash
# Check if twg is available and project-local credentials exist
command -v twg >/dev/null 2>&1 && [ -f .twg/auth.conf ] && echo "twg ready" || echo "twg not found or not authenticated — skipping discovery"
```

---

## Stage 1: import

```bash
export ATLASSIAN_EMAIL="your-email@example.com"
export ATLASSIAN_API_KEY="<api token>"
python3 .agents/skills/kb-jira-sync/scripts/import-jira.py
```

Everything else comes from the `jira` section of `kb-config.yaml` at the vault
root: `base_url`, `project_key`, `output_dir`, `cache_dir`.

The script refuses to run and names the problem when `enabled` is false, the
config is missing, or a required key is absent — it never guesses a project key.

Never commit the API token. If the user pastes one into chat, use it for the run
and do not write it to any file.

### Two directories, two jobs

| Path | Content | Git |
|---|---|---|
| `cache_dir` (default `.cache/jira`) | `<ISSUE-KEY>.json` — the API payload verbatim | **ignored** |
| `output_dir` (default `.raw/jira`) | `<ISSUE-KEY>.md` — rendered, e.g. `PROJ-45.md` | **committed** |

The markdown is the artefact. The cache exists so the renderer can change
without re-fetching: Atlassian Cloud bills API calls against an hourly point
quota, so re-syncing a whole project to fix a formatting bug is a real cost.

```bash
python3 .../import-jira.py --render-only   # rebuild every .md from cache, no API
python3 .../import-jira.py --full          # ignore the cursor, resync everything
python3 .../import-jira.py --debug         # list unhandled ADF node types
```

Deleting the cache is safe. The next run refills it.

### Incremental by default

Each run reads `updated:` from the frontmatter of the existing `.md` files and
asks Jira only for what changed since — rewound 24h, because JQL resolves bare
timestamps in the requesting user's timezone and over-fetching is free while
under-fetching is a silent gap.

A single file without parseable frontmatter forces a full sync, and the script
says so. That is what happens on the first run after this format change.

### Failures are not written

If an issue's comments cannot be read, the issue is **skipped** — no file is
written — it is listed on stderr, and the script exits non-zero. The previous
version returned an empty comment list on any error, so a 401 or a dropped
connection rendered as "No comments", counted as a modification, and overwrote
the good file. Treat a non-zero exit as "the vault is incomplete", not "noise".

### What reaches git

The renderer decides what leaves the machine. The JSON cache holds every custom
field, `accountId` and avatar URL Jira returns; the markdown carries only the
frontmatter schema below plus rendered content. Assignee and reporter **display
names do reach git** — that is a deliberate trade, and it is why the vault
repository must stay private.

## Stage 2: reconcile the wiki

After the import, reconcile `.raw/jira/` against `wiki/jira-issues/`.

Read state from the **frontmatter**, not the body:

```yaml
---
key: PROJ-45
source: jira
type: Story
status: In Progress
resolution: ""
priority: High
assignee: Ada Lovelace
reporter: Alan Turing
created: "2026-01-05T09:00:00.000+0100"
updated: "2026-07-28T14:22:00.000+0200"
due: ""
project: PROJ
parent: PROJ-12
labels: [auth, backend]
components: [gateway]
url: "https://org.atlassian.net/browse/PROJ-45"
---
```

So `rg '^status:' .raw/jira/` answers the status question for the whole project
in one call. Do not parse the body for it.

Scope the work with git rather than re-reading everything — the import already
wrote only what changed:

```bash
git status --short .raw/jira/
```

- **Status drift** — issue closed or started in Jira but the wiki page still
  shows the old `status:`. Update the field and bump `updated:`.
- **New issues** — a `<ISSUE-KEY>.md` in `.raw/jira/` with no wiki page. Create
  one from `_templates/jira-issue.md`.
- **Canonical link** — every issue page carries its Jira URL. Preserve it.

Then update `wiki/index.md`, append to `wiki/log.md` (newest entry at the TOP),
and refresh `wiki/hot.md`. When wiki content changed, also refresh
`wiki/dashboard.md` from `wiki/goals.md` and the changed evidence. Raw-only
connector fetches do not create wiki content events.

---

## Verify, do not assume

`.raw/` is generated, never hand-edited: the import overwrites it. To change how
it looks, change the renderer and run `--render-only`.

The converter is a pure function with its own tests, which need no credentials
and no vault:

```bash
python3 -m pytest .agents/skills/kb-jira-sync/tests/ -q
```

After reconciling, run the gate:

```bash
python3 .agents/skills/wiki-lint/scripts/run-lint.py
```

Exit `1` means a check failed. A batch of new issue pages most often trips
`lint-orphans.py` — new pages nothing links to yet — which is a real finding, not
noise. Link them from the relevant domain or index page.

Watch for wikilink case: `[[proj-45]]` resolves, `[[PROJ-45]]` is reported
dead even though the wiki accepts both.

`lint-contradictions.py` reads `.raw/**/*` to decide whether an entity is
sourced. That is why the rendered markdown stays in git: ignore `.raw/` and the
check still passes, but it passes vacuously with every entity unsourced.
