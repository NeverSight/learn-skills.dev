---
name: knowledge-base-add-project
description: >
  Add a new tracked project (or a new category) to the mmontes11/knowledge-base `projects/` section, or
  update an existing project during a maintenance run. Create the fixed set of standard documents (README,
  api-reference, releases, features, optional architecture) populated and attributed from upstream, keep
  frontmatter fresh, register the project in the Tracked projects table, and push to main. Use whenever the
  user wants to add, track, or refresh a project in the knowledge base — "add <repo> to the knowledge base",
  "start tracking <project>", "update the <project> entry", "run the maintenance for <project>", "add a new
  category <x>" — even if they only name the upstream repository.
license: Apache-2.0
metadata:
  author: mmontes11
  version: "1.0"
compatibility: Requires a checkout of the knowledge-base repository (canonical path ~/code/knowledge-base), access to the upstream GitHub repository, and, for architecture diagrams, the mermaid-render wrapper (pre-installed in the docker-opencode image).
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*), Bash(gh:*), Bash(mermaid-render:*), Bash(mmdc:*)
---

# Add or update a project in the knowledge base

Add a new upstream project under `projects/<category>/<project>/`, or refresh an existing one. The root
`README.md` of the knowledge base is the contract: its **Standard documents** section is the authoritative
spec for what each of the fixed files contains, its **Metadata** section defines the frontmatter, and its
**Tracked projects** table is the index. This skill is the *workflow* — it does not restate those specs; it
tells you how to create and update an entry idempotently.

## Locate the knowledge base

Work inside the knowledge-base repository. The canonical local checkout is `~/code/knowledge-base`; if it
is absent, `git clone git@github.com:mmontes11/knowledge-base.git ~/code/knowledge-base`. All paths below are
relative to the repository root.

## Two modes

- **Add** — create a brand-new project folder (and optionally a new category) from upstream.
- **Update** — the idempotent maintenance pass over one existing project; this is what the monthly
  [update schedule](https://github.com/mmontes11/knowledge-base/blob/main/README.md#update-schedule) drives.

## Mode A — Add a project

1. Read the target category's `projects/<category>/README.md`, plus the **Standard documents** and
   **Metadata** sections of the root `README.md`.
2. Pick the **category** (an existing one, or add a new category first — below) and the **project slug** =
   the upstream repository name in lowercase kebab-case.
3. Create `projects/<category>/<project>/` with the four required standard documents, populated from
   upstream and built to the spec in the root `README.md`:
   - `README.md`, `api-reference.md`, `releases.md`, `features.md` — the required four.
   - `architecture.md` — **only** if the project is a complex multi-component system. Render every mermaid
     diagram before finishing:
     ```bash
     mermaid-render /tmp/d.mmd   # a clean, non-empty SVG/PNG means the block renders on GitHub
     ```
4. Frontmatter on every doc: `upstream` (canonical repository URL) and `last_updated` (UTC date).
5. **Link, don't copy** — every factual statement links to its upstream source; never inline full schemas,
   specs, or generated dumps.
6. Add the row to the **Tracked projects** table in the root `README.md`.
7. Commit `docs(<category>/<project>): <summary>` and push directly to `main`.

### Add a category

1. Create `projects/<category>/README.md` with a short description of the domain (lowercase kebab-case name).
2. Add its first project's row to **Tracked projects**.

## Mode B — Update a project (maintenance run)

Every run must be **idempotent**: unchanged upstream state produces an empty diff. For the one project in
scope, in order:

1. Read the current folder and frontmatter.
2. Fetch upstream truth: the latest release tag, any releases newer than the newest entry in `releases.md`,
   and changes to the API/feature documentation.
3. `releases.md` — prepend new entries, keep the 10-entry cap.
4. `api-reference.md` — only if the API surface changed (new/removed/renamed Kinds or surfaces).
5. `features.md` — only if feature documentation or release notes changed.
6. `architecture.md` — **only if it exists** and the component set or interactions changed; re-render every
   mermaid diagram (`mermaid-render`) and confirm it still matches the current components.
7. `README.md` — only if description, license, or upstream URLs changed.
8. Bump `last_updated` in the frontmatter of every file that was modified.
9. Commit once per project: `docs(<category>/<project>): <summary>`.
10. Push directly to `main`. If a Multica issue drove the run, mark it done once the push lands.

## Hygiene (both modes)

- No credentials, tokens, or cluster-specific data — ever.
- Summarize and link; do not copy upstream text wholesale (respect upstream licenses and attribution).
- Every factual statement links to the upstream source it came from.
- Keep the diff small and explainable — one project per run.
