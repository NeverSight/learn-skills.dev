---
name: brief
description: Generates a rich, visual HTML one-pager that lets a busy reviewer understand a body of changes and either approve a proposed PR stack or merge a finished one — without reading the diff themselves. Auto-detects whether the run is DRAFT (working-tree changes plus a proposed stack, pre-approval) or FINAL (a real PR stack with review complete, pre-merge). Leads with a TL;DR, surfaces the PR stack near the top, flags high-stakes changes (endpoints, auth, schema), then walks the reviewer through the important code as a numbered Code Tour with inline diff snippets. Use whenever someone wants to eyeball a change before approving or merging — "review the changes", "show me what changed", "summarize the diff / the branch / the stack", "what am I about to approve", "walk me through what shipped", "explain the final code", or any shipping-workflow approval/merge gate — even if they don't say the words "brief" or "HTML".
---

# Brief

Produce a **rich, visual one-pager** — a single self-contained HTML file, designed like a dense dashboard rather than a written document — that lets a time-pressed reviewer understand a body of changes and decide quickly whether to approve or merge them, without reading the diff themselves.

The reader is a busy manager. They may give this 30 seconds or 10 minutes; the brief has to reward both. So the structure is strictly **priority-ordered**: the highest-stakes, hardest-to-undo changes come first, and the long tail of routine edits comes last. The goal is maximum signal in minimum time — but never trade clarity for brevity. Be thorough; just front-load what matters.

The brief is not a report. It is the equivalent of the PR author sitting down with the reviewer and walking them through the work — anchoring every claim to real code, explaining *why* the change exists, not just *what* changed. Most readers will not open the diff. Show them the code that matters, inline.

## Two modes — auto-detect

The same skill produces two flavors of brief depending on the state of the work:

- **DRAFT** — there is a working-tree diff (uncommitted or committed but unpushed) and, typically, a proposed PR stack written out in `proposed-pr-stack.md`. No real PRs exist yet, or the stack is not yet review-complete. The brief is what the user reads at the approval gate before the work is sliced into PRs.
- **FINAL** — a real PR stack exists (one or more open/merged PRs), review is complete (PRs are review-clean or all findings triaged), and the user is about to give the merge signal. The brief is what the user reads at the merge gate.

**How to pick the mode:** look at what exists.

1. Are there real PRs on this branch / stack? (`gh pr list --head <branch>`, `gt log` if Graphite is in use.)
2. If yes, is review complete? (No outstanding review comments, no pending re-review requests, all findings either fixed in follow-up commits or explicitly triaged.)
3. **Both yes → FINAL mode.** Otherwise → **DRAFT mode.**

If the user explicitly asks for one mode ("draft brief" / "final brief"), honor it. Otherwise pick automatically and state your choice at the top of your reply ("Generating a FINAL brief — stack is review-clean.").

The difference between the modes is in *content*, not visual structure. The HTML scaffolding below applies to both; mode-specific content (review status pills on each PR card, commit cause tags, skipped-finding rows) only appears in FINAL mode, inside the same PR Stack section both modes share.

## Voice — make it read like a guided walkthrough

A page of tables and callouts is quick to skim but hard to truly absorb: the reviewer gets facts without the thread that connects them. So beyond being well-structured, the brief should *read* — like an author walking a colleague through the change, not filing a report.

- The TL;DR is **one or two crisp sentences** — what shipped (or is being proposed) and the single thing worth a careful look. No narrative paragraph at the top. Keep it tight.
- Every section opens with a one-sentence plain-prose lead-in that frames what follows. The dense table, callout, or tour stop then sits beneath that lead-in.
- The Code Tour (Step 5) is the heart of the brief and is inherently narrative — each stop is a short explanation of why this code matters, followed by the actual code.
- Prefer plain, connected sentences over terse fragments.

Keep prose as connective tissue, not bulk. A skimmer still gets everything from the structure; a top-to-bottom reader gets a coherent story.

## Step 1 — Gather the material

Identify the trunk branch (usually `main`). Then collect the full picture of what changed against it:

- **Cumulative diff and stats** against trunk — `git diff <trunk>..HEAD --stat` and the full diff for the files that matter.
- **Commits** on the branch / stack — `git log <trunk>..HEAD --oneline`, plus **full commit messages** (`git log <trunk>..HEAD --format=fuller` or `git log <trunk>..HEAD --format=%B`) so you can pull out any explanatory body text the author wrote. Many commits will have only a subject line — that's fine, treat the body as optional. But when a commit *does* carry a meaningful body (a `Why:` paragraph, a rationale, a tradeoff note), it is the author's own explanation of that slice and belongs in the brief.
- **Untracked files** (DRAFT mode especially) — new files often carry the most important code and are easy to miss. `git status --porcelain` then read them directly.
- **Proposed PR stack, if one exists** — may be in the current conversation context, or in `proposed-pr-stack.md` (look in repo root and `.briefs/`). If none exists, omit the stack section. Do not invent one.
- **Real PR stack, if one exists** (FINAL mode) — `gh pr list --head <branch>` and per-PR via `gh pr view <num> --json title,body,state,commits,reviews,reviewDecision`. If Graphite, also `gt log short`.
- **Review threads** (FINAL mode) — `gh pr view <num> --comments` and `gh api repos/{owner}/{repo}/pulls/{num}/comments` for inline review comments. Cross-reference commit messages against findings to build the finding → commit mapping.

**Skip generated files when picking what to show in the Code Tour.** They add noise without informing the walkthrough. Common examples — adapt to the repo:

- `**/*.api.md`, `**/api-report*` — generated API surface reports
- `apps/docs/content/reference/**`, generated reference docs
- `yarn.lock`, `package-lock.json`, `pnpm-lock.yaml`
- `**/CHANGELOG.md` when auto-generated
- Snapshot files, schema dumps, bundled assets — anything with a "DO NOT EDIT" header or a regen command in the repo

These can still appear in the compact file index, but they should not be tour stops or callouts.

**Ignore any pre-existing brief files.** `.briefs/` may already contain briefs from earlier runs or other work. They are never an input — they may be stale or obsolete. Do not read them.

## Step 2 — Triage every change by stakes

Before writing anything, sort what you found into tiers. This ordering drives the page.

**Tier 1 — High-stakes (lead with these, make them impossible to miss):**

- New or changed **service endpoints / API routes / route handlers / server actions** — anything that adds surface area.
- **Auth, authz, access control, sessions, secrets, CORS** — anything touching who-can-do-what.
- **Database schema changes** — new tables/columns, type changes, constraints, indexes, drops.
- New **external dependencies**, changed **config / environment variables**, anything **destructive or irreversible**.

**Tier 2 — Core logic that carries the feature:** business logic, data flow, API response shapes, state machines, the functions a reviewer must actually understand.

**Tier 3 — Routine:** UI tweaks, refactors, tests, docs, formatting.

If a tier is empty, say so explicitly ("No auth or schema changes") — absence of high-stakes change is itself valuable information.

## Step 3 — Schema changes get line-by-line treatment

Schema changes are the most dangerous thing in most diffs and the easiest to wave through. If the schema source changed (`schema.prisma`, `db/schema.ts`, migration files, model definitions), do **not** summarize — walk it.

One row per individual change: table/model, exact field, **before → after**, nullability, default, index/constraint impact, and the practical consequence ("existing rows need a backfill", "this drop loses data", "non-null without default will fail on a populated table"). The reviewer should be able to audit the entire schema delta from this section.

## Step 4 — Plan the Code Tour

This is the heart of the brief and the most important section to get right. The Code Tour is a numbered sequence of "stops" through the change, the way the author would walk a colleague through it. The core idea is borrowed from Graphite Code Tours: instead of forcing the reviewer to scroll between a PR description, comments, and a scattered diff, the narrative lives **alongside the actual code** in one sequential path. Each stop pairs a short prose explanation with the specific hunk being discussed, so the reviewer never has to context-switch to understand what changed.

**Planning rules:**

- **Order by understanding, not by file.** If a new type is defined in one file and consumed in another, the definition comes first, the consumer second. Follow the flow of the feature.
- **Group stops under section headings for larger changes.** A flat list of 12 stops is hard to navigate; the same 12 stops grouped under 3 section headings ("Backend service", "Workflow plumbing", "Admin UI") is immediately scannable. The Graphite Code Tours UI uses this hierarchy — section parents with nested child stops — and the brief should mirror it. For small changes (≤6 stops total) a single flat list is fine.
- **Don't walk every file.** Walk the files that *matter* — the high-stakes surface area, the core logic, anything subtle. Aim for **5–10 stops** for a typical change, grouped if it helps; fewer for tiny changes, more (with grouping) for sprawling ones. If you find yourself listing 20 ungrouped stops, you are turning the tour into a file index — re-prioritize or group.
- **One stop = one focused idea.** A stop usually centers on one file or function, but can group three small related changes if they are the same idea ("type re-exports across `index.ts`, `types.ts`, `public.ts` — just plumbing the new `Foo` type").
- **Each stop must show the actual code**, not just talk about it. Pick the hunks (often 5–30 lines) that carry the meaning. Trim noise around them. For pure new files, show the meaningful chunk, not the whole file.
- **Explain the *why*, not just the *what*.** The code on the page shows what changed. The prose adds the reasoning — the problem it solves, the edge cases it handles, the alternative that was rejected. If you have nothing to say beyond what the diff already shows, the stop is not earning its place.
- **Skip boilerplate, but acknowledge it.** Don't dedicate a stop to every import change. Mention in passing in a wrap-up stop: "Remaining changes are type re-exports and test fixtures."

## Step 5 — Build the HTML one-pager

Write one self-contained `.html` file — all CSS inline in a `<style>` block, no external requests, no JS frameworks, no fetched fonts. It must open straight from disk.

### Structural priorities

The page is dense but **strictly ordered — this order is non-negotiable**, even if you think a particular change would read better another way. Past briefs that reshuffled (PR stack ending up below the code walkthrough, single-PR briefs hiding the PR number in the meta grid) consistently failed reviewers. **A reviewer who reads only the first screenful must see: the title, mode, the TL;DR, the PR stack, and any high-stakes callouts.** Everything below scrolls.

Use this section order exactly:

1. **Hero — slim and concise.** No more than ~1/4 of first viewport.
   - Title line: branch / stack name + a **mode pill that is visually loud** — solid colored background, white text, larger than body type (e.g. amber for `DRAFT`, green for `FINAL · review clean`, red for `FINAL · 2 findings open`). The reader should know which mode they're in from across the room. A muted tag-style chip is not enough.
   - **One or two sentence TL;DR.** No long narrative paragraph here. The single thing the reviewer most needs to know.
   - A compact horizontal meta strip: trunk, files changed, +/−, commits, generated timestamp.
2. **PR Stack — prominent, near the top, and self-contained.** If a stack exists (proposed or real), it lives here, visually distinct, not buried in a four-column meta grid. This section **also absorbs the per-PR commit/finding history** — there is no separate "PR evolution" section further down the page. Everything a reviewer needs to know about a given PR — what it is, what's in it, how it got there — lives on its card. A vertical visual stack of PR cards works well, where each card is a small composite block:
   - **Header row.** Position (`1/3`), PR number / slug, one-line summary, size (e.g. `+312 / −44 · 8 files`), status pill (`open` / `merged` / `draft`). For FINAL mode, also a review-state pill (`review-clean` / `2 findings` / `1 skipped`).
   - **Commit timeline — the body of the card.** A vertical list of every commit on the PR, in chronological order. Each row shows: short SHA, subject in monospace, and (FINAL mode) a cause tag — `initial` for the baseline, `review finding` / `user steering` / `other` (CI fix, restacking fallout, polish) for follow-ups. Cross-reference commit messages against review threads to attribute follow-ups; every follow-up must carry a cause.
   - **Commit explanations, when the author wrote one.** Beneath a commit's subject row, render the **commit message body** (the lines after the subject) as muted, smaller prose. Preserve line breaks but don't show it as code. This is the author's own explanation of that slice and often carries the *why* the diff alone can't show. **Omit the body when it's empty or boilerplate** — a single `Why:` line that restates the subject, AI-attribution trailers, `Co-Authored-By` lines. Sparse is the right default: only the bodies that add signal expand; the rest are subject-only rows. For a PR with many commits and few meaningful bodies, this naturally produces a compact list with a couple of expanded rows.
   - **Skipped review findings** (FINAL mode). Surface them as their own visually distinct row inside the card — warning-colored, with the finding summary and the reason it was skipped. They are part of the PR's history and belong on its card, not in a separate appendix.
   - **Single-PR briefs still get this section** — one PR card carrying the full timeline, not a hidden number in the meta strip. The reviewer needs to see "this is PR #22, open, review-clean, three commits, one follow-up addressing finding X" without hunting.
   - If there is truly no PR yet *and* no proposed stack, omit the section and say so once in the TL;DR ("Working-tree only — no stack proposed yet."). In that case, list the commits on the working branch as a single timeline block under the TL;DR using the same row format, so commit bodies aren't lost.
3. **High-stakes callouts.** A small grid of colored callouts — endpoints, auth, schema, deps, config, destructive actions. Each callout is one or two lines: what surface, what changed, what to watch. If there are no high-stakes changes, show one neutral callout that says so — absence is information.
4. **Endpoint Audit** (when the change adds or modifies more than one route / server action / API surface). A dedicated table — not a callout — with columns: `Route` / `Inputs` / `Success behavior` / `Failure behavior` / `Side effect` / `Auth`. One row per endpoint. This belongs above the schema walk because new surface area is usually the highest-stakes thing in a backend change. Skip this section if the change touches zero or one endpoint — the callout in (3) is enough.
5. **Schema walk** (if any). The line-by-line table from Step 3.
6. **Code Tour.** The stops from Step 4. This is the bulk of the page. Stops are grouped under section headings when there are more than ~6 (see Step 4). Each stop is a small composite block:
   - Stop number + a short descriptive title (e.g. `3. Row-locking the delete path`). Numbers are useful so the reviewer can reference a specific stop; descriptive titles make the TOC scannable.
   - File path in monospace, plus optional "depends on / called from" tags.
   - 1–3 sentences of prose explaining what this code does and why it matters.
   - **Inline code or diff snippet** — see rendering rules below. A tour stop with no code in it is not earning its place; either add the code or merge the stop into prose elsewhere.
   - **Optional: a lifecycle / flow diagram** for changes that introduce a multi-step state machine (purchase → grant → consume; queue → enrich → publish; draft → review → approve). Render it as a horizontal sequence of boxes with arrows using inline CSS — no SVG, no JS. One diagram per brief at most; it sits inside the relevant tour stop, not as a separate section.
   - **For briefs with 8+ tour stops, add a sticky tour TOC.** A left-side `position: sticky` column (or a top-anchored mini-nav for narrower viewports) listing every stop title with `#anchor` links. Highlight grouping by indenting child stops under their section heading. No JS — just sticky CSS and named anchors. This is what makes Graphite's tour navigable; without it a long brief forces linear scrolling.
7. **File index.** Compact, at the bottom. One row per file with a one-line description. Generated files can appear here.

### Rendering inline code and diffs (no JS, no fonts)

The tour stops must show real code, not pseudocode or paraphrase. Use a simple, hand-rolled approach — no syntax highlighter library:

- Wrap snippets in `<pre><code>` with a monospace stack.
- For diff snippets, wrap each line in `<span class="add">`, `<span class="del">`, or `<span class="ctx">` based on its leading `+`/`-`/` ` character; the CSS gives each class a soft green / red / neutral background that spans the full row.
- Optionally include the `@@` hunk header line as `<span class="hunk">` (muted color).
- For non-diff source code (a function or class shown for context), use a single `<pre><code>` block with no per-line classes; just monospace on a neutral panel background.
- Show file path **above** the snippet, not inside it. Keep snippets reasonably short — 5–30 lines per stop. If a function is longer, show the meaningful hunk and use prose to bridge omitted regions ("… argument validation omitted …").
- **Use unchanged-region markers between hunks**, the way Graphite Code Tours does. When two non-contiguous hunks from the same file both belong to one stop, separate them with a styled marker like `↕ 12 lines unchanged` on its own row (muted color, dashed border, smaller type). This lets a single stop show both ends of a long file without faking continuity, and tells the reviewer exactly how much code they're not seeing.
- Long-token wrapping: use `white-space: pre-wrap; word-break: break-word;` on code blocks so wide lines don't blow out the layout.

### Visual craft

This lands in front of a manager, so it should look deliberate, not generic: clear type hierarchy, color used purposefully (priority, severity, review state, add/del), monospace for code and paths, real whitespace rhythm. Aim for a max page width around 1100–1200px. Avoid the generic AI-generated look. If a `frontend-design` skill is available, lean on its principles.

The hero must stay slim — resist the urge to fill it with cards. Most of the visual weight should be the **PR stack** and the **Code Tour**.

## Step 6 — Save, open, and self-check

Save the file into a `.briefs/` directory at the repo root. Naming:

- `draft-brief-<slug>.html` for DRAFT mode.
- `final-brief-<slug>.html` for FINAL mode.

Where `<slug>` is the branch name or a short slug of what the change does, so the file never collides with briefs from other work. Make sure `.briefs/` is ignored by version control so briefs are never committed — prefer a local, uncommitted ignore rule over editing a tracked `.gitignore`. Then open the brief in the user's browser.

Before handing off, check the brief against its purpose:

- Could a reviewer who reads only the first screenful name every high-stakes change and see the PR stack?
- Is the mode pill visually loud enough that DRAFT vs FINAL is obvious at a glance?
- Is the TL;DR one or two sentences, not a paragraph?
- Is the PR Stack section present (even for a single PR) and above the high-stakes callouts?
- Within each PR card, did you surface commit message bodies where the author wrote one — and stay silent (no empty body block) where they didn't?
- Did you follow the exact section order (Hero → PR Stack → High-stakes → Endpoint Audit → Schema → Code Tour → File Index)?
- Does every Code Tour stop show the actual code (diff or source), not just describe it?
- Is the tour ordered by understanding, not by filename?
- Is every schema change accounted for line by line?
- (FINAL) Inside each PR card, is every follow-up commit attributed to a cause and every skipped finding surfaced in its own warning-colored row — all on the card, not in a separate evolution section?
- Did you claim a stack/review section that doesn't exist (or omit one that does)?
- **Orphan check across the stack.** For every PR card, list the new top-level functions / components / exports it introduces, then verify each has at least one caller in the *same* PR's diff. Surface any orphan (introduced in PR N, first used in PR N+1) as a warning-colored row on the introducing PR's card — it means the PR added code "ahead of time" and the symbol should be moved down to the PR that first uses it. If a mermaid / dependency-graph visualization of the stack is rendered, orphan nodes show up as nodes with no incoming edge from anything else in the PR; call them out explicitly.
- Anything padded? Tighten it.

Then tell the user the brief is ready, where it is, and which mode you chose.
