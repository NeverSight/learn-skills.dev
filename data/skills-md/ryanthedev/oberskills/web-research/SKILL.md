---
name: web-research
description: >-
  Runs parallel multi-angle web research at four depth modes (scan, brief,
  breadth, deep): a planner grounds the query in local context and plans
  search dimensions, parallel search agents pull verbatim extracts with source
  URLs, every mode above scan adds a standing counter-evidence dimension, and
  synthesis is grounded back in the local project. Use when researching a
  topic, library, or tool on the web, comparing options or products, surveying
  a landscape of approaches, or checking current, version-sensitive, or
  time-sensitive information. Not for: driving or automating a live browser
  session (use oberskills:browser), academic literature search across arXiv or
  Semantic Scholar, or questions about the current repo, project, or files
  already on disk — read those directly.
when_to_use: >-
  research this on the web, look up how to do X, find the best tool or library
  for Y, compare these options, what are the alternatives to X, survey the
  landscape of Z, is this still the recommended approach, what is the current
  or latest way to do this, check whether X supports Y, a version-sensitive
  lookup. Not for browser automation, arXiv or Semantic Scholar paper search,
  or anything about this repo or this project — summarizing a README, finding
  where code lives, reading local files.
---

# web-research

Parallel, multi-angle web search. Ground results in local context and return only the relevant findings, each one carrying a source URL.

---

## Depth Modes

If the user specifies a depth, use it. Otherwise, infer from the query or ask:

| Mode | When | Output |
|------|------|--------|
| **scan** | Quick answer, sanity check, "is this a thing?" | 1-pager: top 3 findings + URLs |
| **brief** | Standard research question | Synthesized brief with recommendations |
| **breadth** | Map a space, survey options, "what's out there?" | Landscape map: categories, key players, gaps |
| **deep** | Decision-critical, needs verification | Full report with confidence levels and verified sources |

**Inference rules:**
- "Quick" / "is there" / "does X support" / "what's the syntax for" → **scan**
- "Research" / "how to" / "best way to" / no depth cue → **brief**
- "Survey" / "landscape" / "what are the options" / "compare" → **breadth**
- "Deep dive" / "report" / "I need to make a decision about" / "thorough" → **deep**

**After selecting mode, load the mode's prompts:**
- scan/brief: `references/search-prompts.md` in this skill directory + `references/synthesis-prompts.md` in this skill directory
- breadth: same two files (breadth-specific sections)
- deep: same two files + `references/deep-mode.md` in this skill directory

---

## Pipeline

The stages are strictly sequential: each one consumes the previous stage's output. A dispatched agent's result does not exist until the host reports that agent complete, so **wait for a stage's result before starting the next** — never proceed on an assumed or predicted result. How the host signals completion varies; the per-host mechanism is under [Host Mapping](#host-mapping).

### Step 0: Check Existing Knowledge (skip for scan)

Before hitting the web, ground in what's already available.

1. Check local files relevant to the query (package.json, configs, code, docs).
2. Use what you find to skip dimensions already covered and focus the search on gaps.

**If existing knowledge covers the query:** Present it. Ask whether they want fresh web results.

### Step 1: Plan

Dispatch the planner with the host's subagent/delegation tool when available; otherwise plan inline. It grounds in local context and plans dimensions by mode:
- scan: one focused dimension
- brief: a few dimensions targeting different angles
- breadth: wide coverage of the landscape, shallow per dimension
- deep: a handful of high-value dimensions, prioritized by quality likelihood

Exact counts per mode live in the planner prompt (`references/search-prompts.md` in this skill directory). Breadth's fan-out deliberately sits above the agent skill's default parallel ceiling: search dimensions are independent and non-overlapping, never refine each other, and each writes its own file — the case that skill's fan-out sizing allows to go wider.

Wait for the planner's result before dispatching search. Show the user the plan before dispatching search agents.

### Step 2: Search

**Set up the run directory first.** Create `~/.local/state/web-research/{timestamp}-{query-slug}/` and confirm it is writable by saving the approved plan there as `plan.md`. If that fails — a headless or SDK run denies writes outside the project, and the path is POSIX-only — fall back to the host's session temp/scratch directory, or failing that a `.web-research/` directory in the project (tell the user; it is not git-ignored for them). Tell the user which directory the run used: nothing prunes it, and it is safe to delete afterwards.

Dispatch all search agents in parallel, in one turn, with the host's subagent/delegation tool when available; otherwise run the searches inline and keep artifacts small. Each writes `{run-dir}/{dimension}.md` and returns that path only. Per-mode agent templates: `references/search-prompts.md` in this skill directory.

**Wait for ALL search agents to complete, then check the files before anything reads them.** List the run directory with sizes (a listing, not a read — extracts stay out of this context). A path whose file is missing or empty is a failed dimension even though the agent "returned" it: the write was denied or the agent stopped early. Re-dispatch that dimension once (into the fallback directory if the write was denied); if it fails again, drop it and note the gap. Pass only verified paths downstream.

If a search returns nothing, reformulate the query and retry once. If still nothing, report the gap.

### Step 3: Cross-Pollinate (deep mode only)

One agent reviews all extract files and fills gaps. Wait for its result, and verify its output file the same way, before synthesis. See `references/deep-mode.md` in this skill directory.

### Step 4: Synthesize

Per-mode templates: `references/synthesis-prompts.md` in this skill directory. Scan mode skips this (return search results directly).

Synthesis agent inherits the user's model. Never override it. Synthesis stops with an input error instead of synthesizing around a missing or empty file — treat that return as a pipeline failure to fix, not a report to present.

### Step 5: Verify (deep mode only)

After synthesis returns, a separate verifier agent checks cited URLs and returns verdicts only. See `references/deep-mode.md` in this skill directory.

---

## Handling Failures

| Situation | Action |
|-----------|--------|
| Search agent returns nothing | Reformulate and retry once. Report the gap if still nothing. |
| Search agent fails | Continue with others. Note the failed dimension. |
| Returned path is missing or empty, or agent returns `WRITE FAILED` | Failed dimension. If the write was denied, move the run to the Step 2 fallback directory first. Re-dispatch once, then drop it and note the gap. Never hand the path to synthesis. |
| Run directory isn't writable | Fall back per Step 2 before dispatching anything. |
| Synthesis returns an input error | Fix the named file (re-run that dimension or remove it from the list), then re-dispatch synthesis. |
| All agents fail | Report failure with attempted queries. Suggest alternatives. |
| URL 404s during verification | Flag it. Remove from recommendations if sole source. |

---

## Model and Effort Selection

| Agent | Tier | Effort | Why |
|-------|------|--------|-----|
| Planner | mid | medium | Weighs which angles are worth searching; doesn't need the strongest model |
| Search agents | mid | low | Bounded extract-and-write work. Tier is a deliberate deviation from the agent skill's cheaper research/lookup default: verbatim extraction and source triage need the reasoning depth |
| Cross-pollination | mid | low–medium | Gap-filling is search, not synthesis |
| Verifier (deep) | mid | low | Checking a claim against a page is easier than producing it |
| Synthesis | (inherit) | (inherit) | Never override the user's model |

"mid" is the host's workhorse tier, a step below its strongest model. Effort is the first lever and tier the second; the canonical guidance on both, and what each effort level buys, is the `oberskills:agent` skill's model-and-effort section. Set effort only where the host exposes it per subagent — otherwise the scope limits written into each prompt do that job.

Search agents return file paths only, not full page content.

---

## Host Mapping

The pipeline above is host-neutral: dispatch with the host's subagent or delegation tool, wait for each stage's result before starting the next, and work inline when the host has no such tool. Per host:

| Concept | Claude Code | Codex/other hosts |
|---|---|---|
| Dispatch a stage | `Agent(...)` — the templates in `references/` are written in this syntax | Host-provided subagent/delegation tool, same prompt text |
| Wait for a stage | Completion notification in a later turn (details below) | Host-provided wait or result operation |
| Mid tier / inherit | `model="sonnet"` / omit `model` | Equivalent workhorse tier / no model override |
| Effort | Subagent-definition frontmatter only (details below) | Per-subagent effort setting, where one exists |
| Web search / fetch | `WebSearch` / `WebFetch` | Host's web search and fetch tools |
| No delegation surface | Work inline | Work inline; keep artifacts small |

### Claude Code specifics

Checked against the live `Agent` tool schema and the [subagents docs](https://code.claude.com/docs/en/sub-agents), 2026-09-21:

- **Waiting.** In an interactive session every `Agent` dispatch runs in the background and its result arrives as a completion notification in a later turn; the orchestrator cannot request a foreground run. "Wait" therefore means: after a gating dispatch, do nothing that depends on the result, and resume the pipeline when the notification arrives. For Step 2, count notifications against the dimensions dispatched and hold until every one is in. Headless (`-p`) and SDK runs may block on the dispatch instead; if the live schema offers a foreground option, use it for the gating dispatches. The rule is the same either way.
- **Effort.** `effort` is a subagent-definition frontmatter field, not an `Agent` call parameter; a plain dispatch inherits the session's effort. The Effort column applies only when dispatching through a definition that sets it.
- **Permissions.** Where no dialog host exists (headless, SDK), a permission prompt is auto-denied rather than shown (mechanics: the `oberskills:agent` skill's mechanics reference), so a subagent's write outside the project can fail while the agent still reports a path — the reason Step 2 probes the run directory and checks file sizes.
