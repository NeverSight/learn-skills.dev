---
name: contributions-update
description: >
  Keep the project tables in mmontes11/contributions current: scrape mmontes11's GitHub star lists,
  compute the delta against the README's tracked tables, score only the new repos against the repo's
  #scoring rubric, rebuild only the touched category tables, and commit a small diff directly to
  main. Use whenever the user wants to refresh, update, or re-score the contributions tracking —
  "update the contributions tables", "re-run the contributions scrape", "refresh
  mmontes11/contributions", "score the new repos in the contributions repo" — and for the scheduled
  runs driven by the Contributions autopilot.
license: Apache-2.0
metadata:
  author: mmontes11
  version: "1.0"
compatibility: Requires a checkout of the contributions repository (canonical path ~/code/contributions), GitHub access via the GitHub MCP tools and the authenticated gh CLI, and push access to main.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*), Bash(gh:*)
---

# Update the contributions tables

Keep the project tables in [mmontes11/contributions](https://github.com/mmontes11/contributions)
current. The root `README.md` is the **contract**: its **Source** section maps each category to a star
list, its **Scoring** section is the 0–10 project rubric, and its **Metadata** section defines the
per-category `Updated` line. This skill is the *workflow* — it does not restate those specs; it scores
only what changed and lands a small, reviewable diff.

## Locate the contributions repo

Work inside the contributions repository. The canonical local checkout is `~/code/contributions`; if it
is absent, `git clone git@github.com:mmontes11/contributions.git ~/code/contributions`. All paths below
are relative to the repository root.

## Tooling

**MCP-first, `gh` as fallback.** Use the GitHub MCP tools for every operation they cover (repo metadata,
root file contents, issue and pull-request search). Fall back to the authenticated `gh` CLI **only** for
operations the MCP tools do not offer or that would flood the context with raw JSON:

- **Star lists** — `https://github.com/stars/mmontes11/lists/<slug>` has no MCP operation (the lists API
  is GraphQL-only); fetch it with `gh` (a small script is fine), keeping only `owner/name` pairs in
  context.
- **Bulk search counts** — when scoring many new repos, the three search counts per repo are cheaper
  through `gh search` / `gh api` than through dozens of MCP calls; throttle search calls ~2.2 s apart to
  stay under the 30/min search limit.

Either way, **never JSON-dump a full MCP or API response into the conversation** — extract only the
fields the rubric needs.

## Invariants that keep it cheap

1. **Diff before you score.** The set of repos already listed is read straight from the README (repo
   names only — tiny). Score **only** repos that are new since the last run, and drop repos removed from
   a list.
2. **The tables are the cache.** Do not re-score a repo that is already listed in a category whose
   `Updated` date is fresh (< 90 days).
3. **Skip personal repos.** Repos owned by `mmontes11` are personal projects, not contribution targets:
   skip them while scraping and drop any `mmontes11/*` row found in a table (never re-add).

## Procedure

1. **Scrape the lists.** For every list in the README's Source table, fetch
   `https://github.com/stars/mmontes11/lists/<slug>` (paginate, via `gh` — see Tooling) and collect the
   repo names, skipping `mmontes11/*` → `repo -> {lists}`.
2. **Compute the delta** against the repo names already in the README's Potential contributions tables:
   - **New** — in a list, not in a table → score these (step 3).
   - **Removed** — in a table, not in any list → delete these rows.
   - **Personal** — an `mmontes11/*` row in a table → delete it.
3. **Score the new repos** against the README's **Scoring** rubric (0–10). For each new repo:
   - Repo metadata — `language`, `stargazers_count`, `pushed_at`, `archived`. **Drop the repo if
     `archived`.**
   - Root contents — presence of `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md` on the default branch.
   - Three search counts — open `good first issue`, open `help wanted`, merged AI-authored PRs (AI
     co-author: Claude, Codex, or Copilot).
4. **Rebuild the tables.** Regenerate each **touched** category sub-section sorted by score (desc) then
   stars (desc), refresh its metadata `Updated` date, and leave categories with no delta
   byte-for-byte unchanged (no diff).
5. **Commit to `main` directly** — no pull request:
   ```bash
   git add README.md && git commit -m "Update contributions tables" && git push origin main
   ```

## Cadence & full re-score

Run on demand or on a schedule (the Contributions autopilot runs it monthly — the 15th of each month at 09:00, Europe/Madrid). Ignore the 90-day freshness
cache and re-score a category from scratch when its `Updated` date is older than **90 days** or when the
**Scoring** rubric itself changes.

## Deliverable (when run from a Multica issue)

Post one summary comment on the driving issue: repos added / removed / dropped per category, plus the
top new scorers. If there is no delta (nothing added, removed, or dropped), post a comment stating the
lists were re-checked and unchanged, and skip the commit.
