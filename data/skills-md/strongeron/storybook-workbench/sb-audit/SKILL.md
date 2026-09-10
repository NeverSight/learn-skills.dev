---
name: sb-audit
description: "Periodic Storybook audit — naming-drift survey, archived/decision-board review, lifecycle tagging, usage refresh. Use for 'audit my Storybook', 'find drift', 'show pending decisions', or a periodic catalog health check."
compatibility: "Requires bash and python3; git optional (decision-board date fallback in audit-archived/prune-to-ledger)."
allowed-tools: Bash Read Glob Grep Write
license: MIT
metadata:
  author: strongeron
  version: '2.3.0'
  bundle: storybook-workbench
  vendor:
    # Files this skill needs at runtime. Skill-local ones live in scripts/; the rest are resolved
    # from shared/ ($CORE) in dev and copied into dist/ by build.sh on export.
    scripts: [audit-drift.sh, audit-archived.sh, find-stories-by-tag.sh, prune-to-ledger.sh, extract-component-usage.sh, audit-controls.sh, refresh-usage.sh]
    wrappers: false
    references: [galleries-and-tags.md, lifecycle-tags.md, propagate-workflow.md, anti-patterns.md]
    templates: [design-decisions.md]   # templates/ — propagate-workflow.md points readers to it; vendored on export
---

# sb-audit — drift survey + decision board

The periodic gate. Surveys the catalog, seeds the ledger, names consolidation candidates.

## Run it

```bash
SKILL=${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}
CORE=${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}
"$SKILL/scripts/audit-drift.sh"                 # naming drift across stories
"$SKILL/scripts/audit-archived.sh"              # L1/L2/L3 preservation surveillance (HEAVY warning)
"$CORE/scripts/find-stories-by-tag.sh" decision:pending   # stale decisions needing a nudge
"$CORE/scripts/extract-component-usage.sh"      # REFRESH real prop-usage → component-usage.json (auto, no hand-edits)
"$SKILL/scripts/audit-controls.sh" .            # Controls-panel coverage: component stories missing argTypes + manager showPanel
"$CORE/scripts/refresh-usage.sh" --docs .       # ONE-COMMAND refresh: components + tokens + routes + health JSON + re-stamp per-component usage MDX

# App flow + component lists: re-run the repo-local app-graph extractor if present, then VALIDATE it
[ -f .storybook/scripts/extract-app-graph.mjs ] && node .storybook/scripts/extract-app-graph.mjs   # refresh app-graph.json + component-pages.json
[ -f .storybook/app-graph.json ] && node -e 'const g=require("./.storybook/app-graph.json"); const by={}; for(const e of g.edges) by[e.attribution]=(by[e.attribution]||0)+1; console.log("flow edges by attribution:", by, "| unresolved:", g.unresolvedEdges.length); for (const u of g.unresolvedEdges) console.log("  UNRESOLVED", u.provenance, "→", u.to, "—", u.reason)'
```

**Sequence — don't run all six cold.** Start with `audit-drift.sh` (cheap, names consolidation
candidates). The **HEAVY `audit-archived.sh`** L1/L2/L3 scan only earns its cost once the catalog is
sizable — **skip it under ~20 chosen stories** (nothing to prune yet). Run `audit-controls.sh` +
`extract-component-usage.sh` when you're checking coverage; `refresh-usage.sh --docs` is the
all-in-one rendered refresh — run it last, not alongside the individual extractors it supersedes.

**One-command usage refresh.** `refresh-usage.sh` runs all four extractors (inventory/token map,
component prop-usage, routes, design-system health — every **rendered** file; see `CONTEXT.md`
§STORAGE MAP) and — with `--docs` — re-stamps every `<Name>.usage.mdx`. The autodocs
import the JSON, so a Storybook rebuild after this reflects current reality with no hand-editing. Trigger
it three ways: per-script (here, or call one extractor directly), every audit (this step), or in CI before
`storybook build`. The `usage` prop on `StateGrid`/`StateMatrix` reads the same JSON to badge each
variant cell with its real call-site count (declared-but-unused → struck through).

**Auto-refresh usage (no human authoring).** Re-running `extract-component-usage.sh` here keeps
`component-usage.json` current as the app changes; the `usage-profile.mdx` autodocs read that JSON at
build time, so the "real usage in this app" tables update themselves on the next Storybook build. Wire
the same one-liner into CI for repos that want it always fresh. If usage shifted (a variant that was
`declaredButUnused` is now shipped, or vice-versa), flag the affected stories' `usage:unused` tags as a
drift finding.

## Decide (ask yourself)

- **Drift** — 17 names for "empty state" → consolidation candidate; 1 cluster → noise, ignore.
- **Archive** — `audit-archived.sh` flags >20 chosen stories → prune to the durable ledger seeded from
  `templates/design-decisions.md` (`$SKILL/scripts/prune-to-ledger.sh`); otherwise leave it.
- **Pending decisions** — stale `decision:pending` → remind stakeholders.
- **Controls coverage** — `audit-controls.sh` flags component stories that pass `args` but wire neither
  `argTypes` nor a controls-disable (so they expose no usable Controls panel), and warns if
  `.storybook/manager.ts` doesn't `showPanel`. Fix by wiring `argTypes` (unions → select, flags →
  boolean, group via `table.category`, hide non-serializable props) — or disabling controls on
  render-only stories — per the Controls pattern in sb-stories (its without-mcp reference, §13).
- **Flow / app-graph drift** — the validate step above prints edges-by-attribution + every
  `UNRESOLVED`. If `unresolvedEdges` grew, or a new entry's reason is "dynamic dispatch" / a nav idiom
  the extractor doesn't parse, that's a **real edge being dropped** — the app added a navigation
  pattern the script misses. Work the under-extraction loop in sb-flows (`flow-capture.md`), extend
  the repo-local `extract-app-graph.mjs`, re-validate. Never accept a silently shrinking map: an edge
  with no source is unresolved, not absent. (Same JSON also feeds the component lists — a component
  that lost all `parents`/`pages` is a dead-component or import-trace finding.)

Load `references/galleries-and-tags.md` when scaffolding a `TagGallery`,
`references/lifecycle-tags.md` for archive/deprecation, `references/propagate-workflow.md`
when a prune candidate appears, `references/anti-patterns.md` when reviewing AI-generated stories
(the full list — mega-stories, inline mocks, CSF2, pseudo-class misuse) — pick based on what surfaced, don't load all four.

## Ledger (durable memory you steer)

Append findings to `.storybook/audit/findings.md` (timestamped, append-only). **Log-only rule:** a
real prod issue out of scope for the story pass (unassociated `<label>`, sub-AA contrast, headless
crash) gets a `LOG-ONLY:` marker — record it, keep moving, don't touch app code unless asked. After
seeding the ledger, prompt to **commit it** (`git add .storybook/audit/`) — an uncommitted ledger is
one `git clean` from gone.

## Next

`/sb-hub` → usually a `sb-stories` consolidation pass or a `sb-ship` for a graduated Explore.
