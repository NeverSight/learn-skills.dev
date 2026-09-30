---
name: compare
description: Compare a site against its own baseline, against a staging deployment, against up to four competitors, or against the pages that already answer a query (content gap). Produces score, category, finding and structure deltas from persisted audit runs. Read-only. Use when the user asks what changed after a deploy, whether staging is worse than production, how they stack up against competitors, or what rivals cover that they do not.
argument-hint: "<urlA> <urlB> [<urlC>…] | --baseline [latest] --against <url|run> | --staging <url> --prod <url> | <url> --gap \"<query>\""
allowed-tools: Read, Glob, Bash(node "${CLAUDE_PLUGIN_ROOT}/scripts/*"), WebSearch
---

# /claude-seo-ai:compare

Four comparisons, one script. **Read-only**: everything is written under `${CLAUDE_PLUGIN_DATA}/runs` (comparisons land in `<root>/compare/<a>__<b>/compare.json`), never in the user's project.

`$ARGUMENTS` decides the shape:

| The user gave you | Run |
| --- | --- |
| two URLs / run refs | `compare.mjs <refA> <refB>` — same host is a **baseline**, a staging-looking host is **staging**, two sites are **competitor** |
| three to five refs | `compare.mjs <refA> <refB> <refC> …` — competitor matrix (max 5) |
| "since my last audit" | `compare.mjs --baseline latest --against <url\|run>` |
| staging vs production | `compare.mjs --prod <ref> --staging <ref>` (add `--map staging.example.com=example.com` when the hosts do not look related) |
| "what do the pages ranking for X have that I don't" | the content-gap flow below |

A `<ref>` is a run directory, a `report.json`, `latest[:<host>]`, `baseline[:<host>]`, or a URL.

## Flow A — baseline, staging, competitor

1. **Get a run for every side.** A ref that is already a run (`latest`, `latest:example.com`, a path) needs nothing. For a URL with no run, audit it first so the user sees the acquisition and can ask for more pages:
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/audit.mjs" <url> --pages 3 --checks deterministic --render static --out "${CLAUDE_PLUGIN_DATA}/runs"`
   (If you skip this, `compare.mjs` audits the URL itself with exactly those settings.)
2. **Compare:**
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/compare.mjs" --baseline <refA> --against <refB> --out "${CLAUDE_PLUGIN_DATA}/runs"`
   Useful flags: `--mode auto|baseline|staging|competitor|gap` · `--map <from-host>=<to-host>` (repeatable) · `--no-host-normalize` (keep `www.` and the raw host) · `--format md` (also writes `compare.md`) · `--data` (print the whole document) · `--fail-on-regression` (exit 3) · `--set-baseline` (mark the newer run as the baseline).
3. **Read `compare.json`** (the stdout summary names its path) and present, in this order:
   - **Verdict** — `improved` / `regressed` / `mixed` / `unchanged`, with the two score deltas and their bands. Never blend the axes.
   - **Categories that moved**, biggest first. A category that was inactive on one side has `delta: null` — say "not measured on <side>", never "0".
   - **Findings**: `regressed` and `new` first (these are what broke), then `fixed` and `improved`, then the `unchanged` count. Quote the `from → to` status and the location of each.
   - **Coverage changes** as their own list, with the sentence that they are *not* results: a `needs_api` / `manual_review` transition and a location the other run never visited say the two runs measured different things.
   - **Structural gaps** (`gaps`): schema types, agentic/discovery endpoints, AI-crawler posture, heading-topic overlap, answer blocks, entity links, word count, render mode, hreflang. When `gaps.available` is false, say which side had no page snapshots instead of showing zeros.
   - **Pages that moved**, by normalized path, and the `only_a` / `only_b` paths. A page whose row carries `coverage_change: true` moved *coverage*, not score — one of the two runs did not score it (a 429 or 404 the second time round, for instance). Read those from `page_coverage.changes` as their own list.
   - **Page coverage** (`page_coverage`): when `same_pages` is false the two rollups averaged different page sets, the axis deltas do not count towards the verdict, and the warning says so. Say it out loud instead of presenting the axis movement as a change in the site.
   - In competitor mode there is **no findings diff** (`findings: null`): show the score/category table, the presence matrix and the "subject vs best in set" gaps, and say why a finding on one site is not the same fact on another.
4. **Offer next steps**: `--set-baseline` to make this run the reference for later comparisons, `/claude-seo-ai:fix <target>` for what regressed, and `--fail-on-regression` in CI.

## Flow B — content gap

1. **Find the comparison set.** `WebSearch` the query, keep the top 3–5 **organic** result URLs that are not on the subject's host. Skip aggregators, marketplaces and listicles that are not the kind of page the user is trying to be, and **tell the user which URLs you skipped and why** — the set is the whole method, so it has to be visible.
2. **Snapshot each one** (no audit needed; the gap matrix is structural):
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/snapshot.mjs" <url> --run gap-<slug> --render static --out "${CLAUDE_PLUGIN_DATA}/runs"`
   Do the same for the subject page unless it already has a run (`latest:<host>`).
3. **Build the matrix:**
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/compare.mjs" --mode gap --subject <ref> --set <ref,ref,ref> --query "<the query>" --out "${CLAUDE_PLUGIN_DATA}/runs"`
4. **Present the matrix, then the narrative.** The deterministic rows are: heading topics present on at least two comparison pages and absent from the subject; schema types; capitalized terms (a proper-noun proxy, not extracted entities); agentic/discovery endpoints; word count; substantive numbers per 100 words; question headings and how many carry a direct answer. Give each row the page count that supports it. Then write the qualitative reading — what the set treats as table stakes, what the subject could add — and mark every item **directional**.
5. Offer to turn the gap list into an outline or a `/claude-seo-ai:fix` plan. Never write to the user's project from here.

## Honesty

- **A comparison is two measurements, not a ranking.** Scores describe the structure of the pages that were crawled. A higher score is not a prediction that one site outranks another.
- **`WebSearch` is one engine at one moment.** The comparison set is a snapshot of one result page, not rank tracking, and not a sample of anything. Say so whenever you present a gap matrix, and repeat it if the user asks "so will this rank?".
- **Not measured is never a pass.** `needs_api` and `manual_review` transitions live in `coverage_changes` and are excluded from `fixed`/`regressed` by construction — present them that way, and never describe a page the other run did not visit as fixed. A page that stopped answering 2xx is the same class of event: it leaves the rollup, lands in `page_coverage`, and is never reported as a score improvement.
- **Label the coverage.** When `coverage` is `deterministic` on either side, say the model-judged modules were not evaluated; when `coverage_warning` is set, read it out. A provisional band (`state: "partial"`) is reported with its coverage percentage in the same sentence.
- **Directional stays directional.** Every gap row is a structural difference between pages, so it carries `directional` confidence — never promote one to "this will improve rankings".
- Reply in the user's language (EN/ES). Nothing here writes to the user's project: run artifacts and comparisons live under `${CLAUDE_PLUGIN_DATA}`.
