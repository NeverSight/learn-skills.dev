---
name: docs-coverage
description: "Audit whether a design system's documentation surface keeps pace with its component library — coverage gaps (components with no docs), staleness (docs that predate the component's last code change), and orphaned docs. Works with zero integration from the codebase and a Storybook build; Zeroheight, Supernova, and custom docs sites are optional layers. Trigger when someone says: docs coverage, documentation audit, are our docs up to date, which components are undocumented, is our documentation keeping pace, stale docs check, documentation health, Storybook coverage, or anything about whether the documentation surface matches the components. Do NOT trigger for WRITING documentation — use usage-guidelines, pattern-documentation, token-documentation, or ai-component-description for that. Do NOT trigger for general system health (use system-health) or for documentation usage/analytics (use adoption-report)."
references:
  - ../../knowledge-notes/documentation-coverage.md
  - ../../knowledge-notes/output-discipline.md
  - ../../knowledge-notes/adoption-measurement.md
---

# Docs coverage

A skill for auditing whether a design system's documentation surface keeps pace with its components. It measures the code (the source of truth for what exists) against each documentation surface and reports three things: **coverage gaps** (components with no documentation), **staleness** (documentation that predates the component's last code change), and **orphaned docs** (pages for components that no longer exist). Produces a severity-rated finding table with per-signal confidence labelling.

## Context

Code is the source of truth for what components exist; the documentation surface is measured against it. A component in code with no docs is a coverage gap; a page for a deleted component is an orphan; a page older than the component's last change is a staleness risk.

This skill is built to work with **no integration at all**: a components directory plus a Storybook build plus git history answer coverage and staleness for most teams. Hosted platforms (Zeroheight, Supernova, custom docs sites) are optional layers that light up when configured — never prerequisites. The audit never blocks on an integration; it logs what is unavailable and proceeds with what it can reach.

The hard part is trust. Coverage is a join between two lists — components in code and entries in the doc surface — and the join is only as reliable as the key that links them. Every coverage finding carries a confidence tier so a fuzzy guess is never presented as a fact. See `documentation-coverage.md` for the full model.

---

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `system.framework` — affects how component files are discovered (e.g. `.tsx` / `.vue` / `.twig`)
- `severity.*` — severity-rating overrides, applied the same way the other audit skills apply them
- `integrations.storybook.static_path` — local Storybook build directory (e.g. `storybook-static`); the preferred source
- `integrations.storybook.url` — published Storybook URL for pulling `/index.json` when no local build exists
- `integrations.documentation` — optional hosted platform: `platform`, `url`, `api_key_env`, plus `styleguide_id` (Zeroheight) or `design_system_id` (Supernova)
- `integrations.github` — if enabled, used to read change history when the audit runs outside a local clone
- `docs_coverage.staleness_threshold_days` — grace window before a doc is flagged stale (default 90)
- `recurring.*` — if this is a recurring run, load the previous report for trend comparison

If no config file exists, proceed with defaults and codebase discovery.

## Auto-pull integrations

If integrations are configured, pull data automatically before asking the user for manual input.

**Storybook — the primary surface (`integrations.storybook.enabled: true` or a local build):**
- Prefer a local static build: read the index from `integrations.storybook.static_path` (default `storybook-static/index.json`). No server, no auth.
- If only a URL is configured, fetch `<url>/index.json`.
- Branch on the top-level `v` field, which tracks the Storybook version: `v: 3` is the SB 6 `stories.json` (entries under the `stories` key); `v: 4` and `v: 5` are the SB 7+ `index.json` (entries under `entries`), and `v: 5` (SB 8.1+) adds `componentPath`. `componentPath` is opt-in and not guaranteed even on recent Storybook — use it for the Tier A join when present, and **fall back to the Tier B name join whenever it is absent, regardless of `v`**.
- The official Storybook MCP (`@storybook/addon-mcp`) is **optional** — at the time of writing it needs a running server and is React-only/experimental. Use it only if the tools are already available; never make it a dependency.

**Documentation platform — optional layers (`integrations.documentation.enabled: true`):**
- `zeroheight`: use the REST API (Enterprise) — `GET /styleguides/{id}/pages` and `GET /pages/{id}` give the documented-page set and `updated_at` per page (high-confidence staleness). There is no components endpoint, so reconstruct the coverage diff by name-matching pages against the code/Storybook inventory (Tier C).
- `supernova`: use the MCP "Relay" or `@supernovaio/sdk` — `get_design_system_component_list` vs `get_documentation_page_list` gives a coverage diff (heuristic link, Tier B/C). Per-page staleness timestamps are not reliably exposed — mark staleness unknown unless a page timestamp is actually present.
- `custom`: crawl the sitemap or rendered HTML for page titles; name-match only (Tier C).

If an integration is configured but fails (auth, rate limit, missing build), log the failure and fall back to the codebase-only baseline. Never block the audit because a platform is unavailable.

## Step 0: Build the component inventory (the source of truth)

Establish what components exist before looking at any documentation.

1. If a `codebase-index` output exists (`.ai/index/`), use its component list — it is already resolved and classified.
2. Otherwise glob the components directory. Common roots: `src/components/**`, `packages/*/src/**`, `lib/components/**`, `app/components/**`. Treat each component file/symbol as a candidate (e.g. `Button.tsx`, not `Button.test.tsx`, `Button.stories.tsx`, or `index.ts` barrels).
3. Record, per component: name, resolved file path (repo-relative, forward-slash), and category if a classification is available.

Produce a brief inventory line before continuing: `N components found across M directories.` If discovery finds nothing, ask the user where components live.

## Step 1: Build the documentation inventory

For each available surface, list what is documented.

- **Storybook:** parse `index.json`. Group entries by `title`. For each component, record: has a `type: 'story'` entry (rung 1, *exists*), has a `type: 'docs'` entry — autodocs or MDX via `tags` (rung 2, *described*), and the resolved `componentPath` and `importPath`. Optionally parse the CSF file for `argTypes`/`args` and `play` presence (documented controls, interaction tests).
- **Hosted platform (if configured):** list documented pages and, where exposed, their `updated_at`/last-modified timestamp.
- **Usage guidance (rung 3):** if the system documents usage separately (a `usage-guidelines` output, MDX "When to use" sections, a Zeroheight guideline page), record which components reach rung 3.

## Step 2: Join the inventories

Join code components to documentation entries using the reliability hierarchy from `documentation-coverage.md`, and **record the tier on every match**:

- **Tier A (high):** Storybook v5 `componentPath`, normalised, matched to the component file path. Exact.
- **Tier B (medium):** component export name or `title` last segment. Display strings can drift — flag it.
- **Tier C (low):** fuzzy name match against page titles/headings (hosted platforms, custom sites). Never stated as fact.

## Step 3: Coverage gap analysis

From the join, produce:

- **Undocumented components** — in code, no entry on any surface. Report each with the join tier that found (or failed to find) it. Group by the documentation rung they fall short of.
- **Rung distribution** — how many components reach *exists* / *described* / *guided*. A high story count with few described/guided components is itself a finding.
- **Orphaned docs** — pages/stories whose component no longer exists in code. These point the opposite direction and are usually quick removals.

## Step 4: Staleness analysis

For each documented component, compare change dates:

- Component last change: `git log -1 --format=%cI -- <component source path>`. "Component change" means the last commit touching the component's source — by default the whole component file or directory.
- **Be aware this proxy can over-flag.** A commit that only touched a test file, a story, or a comment still moves this date, so a doc can be flagged stale when nothing user-facing changed. This is acceptable for a risk flag (over-inclusion is safer than missing real drift), but when a flagged component's most recent commit looks test-only or cosmetic, inspect what actually changed (`git log -1 --name-only -- <component path>`) and either confirm a substantive change or lower the finding's confidence. Do not hard-exclude file types by pattern — judge the commit.
- Doc last change: `git log -1 --format=%cI -- <story/MDX file>`, or the platform timestamp (`updated_at`).
- Apply the comparison explicitly: flag **stale** when `component_last_change − doc_last_change > staleness_threshold_days` (default 90) — the component changed and the doc has not caught up within the grace window. If the doc is the same age as or newer than the component, it is never stale.
- `git log` returns **empty output (not an error)** for a file with no commits in the current branch/clone. Treat an empty result as untracked and mark staleness **unknown** — never as fresh. Do the same when a platform exposes no timestamp. (Shallow clones and un-`--follow`ed renames can also produce misleading dates — prefer a full clone when staleness matters.)
- Frame stale findings as a **risk**, not a defect: "docs predate a code change on [date] — confirm they still match," with both dates shown.

## Step 5: Produce the report

Open with a headline sentence stating overall state and where to focus. Example: "Of 84 components, 71 have a story but only 38 have a docs page, and 9 docs pages predate a code change. The coverage floor is solid; the described/guided layer and 9 staleness risks are where to focus."

Structure the report:

---

### Docs coverage report

**Date:** [date]
**Inventory:** [N components] · **Surfaces audited:** [Storybook / Zeroheight / Supernova / custom] · **Join confidence:** [the tier used for most components — A, B, or C]

**Summary**
One paragraph. Overall state, the most urgent gap, and an explicit note on which signals were measured vs estimated or unavailable. Write it like a peer review, not a compliance filing.

**Coverage by rung** — count each component at the **highest rung it reaches**. The rows are mutually exclusive (a "guided" component is not also counted under "described" or "exists"), so they sum to the full inventory. "Undocumented" is the rung-0 bucket: components on none of the three documentation rungs.
| Rung | Count | % of inventory |
|---|---|---|
| Guided (usage guidance) | | |
| Described (docs/autodocs page, no usage guidance) | | |
| Exists (≥1 story, no docs page) | | |
| Undocumented (no surface) | | |

**Findings**
List each finding with:
- Finding ID (e.g. DC-01)
- Severity: 🔴 Critical / 🟠 High / 🟡 Medium / ⚪ Low
- Category: Coverage gap / Staleness / Orphan
- Confidence: Tier A / B / C (and timestamp source for staleness)
- Description, affected component(s), and recommended action

**Orphaned documentation**
List pages/stories with no matching component, with the suggested removal.

**Action list**
- **Immediate:** undocumented high-traffic or foundational components; orphans
- **Planned:** raising the described/guided layer; resolving staleness risks
- **Review:** Tier C matches needing manual confirmation

---

## Recurring workflow

If `recurring` is configured in `.ds-ops-config.yml`:

1. Load the previous docs-coverage report from `recurring.output_directory` matching `{skill}-{date}`.
2. Compare: coverage-by-rung deltas, newly undocumented components (regressions — these are the priority), newly resolved gaps, and staleness count trend.
3. Add a "Trend since last audit" section to the header: previous date, rung deltas, and one sentence — "Documentation coverage is improving / stable / declining since [date]."
4. Save the output to `recurring.output_directory` using `recurring.naming_pattern`, and prune beyond `recurring.retain_count`.

If no previous report exists, note "This is the baseline audit. Trend analysis will be available from the next run."

## Closing note (include in every report)

End the report with:

> **A note on context:** This audit measures your documentation surface against your code — it does not see why a component was left undocumented or why a doc predates a change. Some gaps are deliberate (internal-only components) and some "stale" docs are still correct after a refactor. Tier C matches are best-guesses, not facts. If a finding describes an intentional choice, let me know — I'll calibrate future runs. The goal is to surface drift you haven't seen, not to second-guess decisions you've already made.

## Quality checks

- Every coverage finding carries a join confidence tier; no Tier C result is stated as fact
- Staleness findings show both change dates and name the timestamp source; unavailable timestamps are marked unknown, not assumed fresh
- The report distinguishes the rungs (exists / described / guided, plus the undocumented rung-0 bucket), counted at highest-attained — not a single coverage percentage
- Orphaned docs are reported separately from coverage gaps — they point the opposite direction
- The summary states which signals were measured vs estimated or unavailable
- The audit ran on whatever was available and did not block on a missing integration
- The closing note about intentional choices is present
