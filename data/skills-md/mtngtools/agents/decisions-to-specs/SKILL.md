---
name: decisions-to-specs
description: Settle a wayfinder map's decisions into durable spec files in the repo — updating existing specs or writing new ones, placed by locality, as ADRs where the decision earns it.
argument-hint: "The wayfinder map (issue URL or number)"
disable-model-invocation: true
metadata:
  type: command
  invocation: human-only
  applies-to: [planning, wayfinder, specs, adrs, worktrees]
---

# Decisions → Specs

> **human-only.** Start this only when a human asks for it by name. If you arrived here from another skill, stop and get explicit confirmation before running any step.

`/wayfinder` charts decisions as GitHub issues — the conversation, captured at that moment. Those issues are the **record**; they are not where a decision *lives*. This skill takes a wayfinder map and settles its resolved decisions into **durable spec files in the repo**, so the next step — `/specs-to-tickets` — has something concrete to slice.

Read GitHub for the decisions; write the repo for the specs. The two surfaces stay split on purpose (see [Split surfaces](#split-surfaces)). This skill is the bridge, and only the bridge — it never creates issues, never moves specs onto the tracker.

**Write the repo from a worktree of its own.** Other sessions share the primary checkout, and this skill edits specs all across the tree. Working in the shared checkout drops half-written specs into someone else's build, or swaps the branch out from under them. Every repo write below happens in a worktree this skill creates, on a branch of its own — see [step 4](#4-branch-into-a-worktree-before-writing). Steps 1–3 read GitHub and the tree, and are safe anywhere.

**Settling a decision supersedes its ticket.** The issue is a snapshot of one conversation; from there the decision lives in the spec — and only the spec moves as later decisions, review, and implementation refine it. A decision ticket read months later is therefore likely stale, so step 8 stamps each one with a **superseded** banner pointing at its spec. The issues stay closed as the rationale trail; the specs are what `/specs-to-tickets` slices into implementation tickets.

**Approvals go on the tracker, not into the specs.** Where the human settles something while this skill runs — a gated name, a spec's home, a decision to drop one — follow the `approval-policy` skill for where that gets written. The spec carries the rule it produced; who approved it, when, and what it beat belong on the decision ticket or the map. An ADR's considered-alternatives section is the one place in the tree that holds the alternative, and it holds it as a decision record, never as an account of the conversation.

## Process

### 1. Load the map and its decisions

Resolve the map from the argument (issue URL or number). If none was given, find the open issue labelled `wayfinder:map`. Read its body — **Destination** and **Decisions so far**. For every decision listed, fetch its child ticket and read the answer `/wayfinder` recorded on close — its resolution comment.

**Done when:** every resolved decision in Decisions-so-far is in hand with its answer. A decision with no durable consequence (a dead end, an explicit "no change") is dropped with a note — not forced into a spec.

### 2. Map the existing spec landscape

Before writing anything, learn where specs already live, so decisions **update rather than duplicate**:

- package/assembly `spec/` folders (and any spec sitting closer to the code)
- root `spec/` — cross-cutting specs
- `spec/adr/` — existing ADRs (the ADR folder is a subfolder of the spec folder, at whichever `spec/` scope owns the decision)

Read `CONTEXT.md` and any ADRs touching the areas these decisions affect. Use the glossary's vocabulary in everything you write; if a decision contradicts an ADR, surface it rather than silently overriding.

**Done when:** for each decision you can name the spec file it belongs in, or state that none exists yet.

### 3. Route each decision — confirm before writing

Apply the [Placement rules](#placement-rules-locality-ladder) to give each decision a home: an existing spec to update, a new spec to create, or an ADR. "Closer to code if it makes sense" is a judgment call — present the full routing table (decision → target file → new/update) and get the user's confirmation **before writing a single file**.

**Done when:** the user has approved a target for every decision.

### 4. Branch into a worktree before writing

Everything from here that touches the repo happens in a **worktree of this skill's own**, cut fresh from the remote — never in the primary checkout, never straight onto `main`:

```
git fetch origin
git worktree add <worktree-path> -b docs/specs-<map-number> origin/main
```

**Put it inside the repo, not beside it, and name it for the map.** Moving a session into a directory outside the project is a thing most harnesses ask the human to approve separately from any tool permission — a prompt that has nothing to do with the work. A path inside the working directory avoids it entirely. Follow whatever the repo already names its branches and worktrees, and name both for the map so it is obvious whose they are.

**If you are Claude Code** — use `.claude/worktrees/specs-<map-number>`, the harness's own worktree home, so nothing new has to be trusted. Enter it with `EnterWorktree` and its `path` argument, which requires the worktree to already appear in `git worktree list`, hence the order above.

**Any other agent** — use a repo-local directory your tooling already ignores; `.worktrees/specs-<map-number>` is a safe default, and `.git/info/exclude` will hide it without touching the tracked `.gitignore`. Then make that directory your working directory for every write below, by whatever mechanism your harness provides. If it has no way to move, pass the path explicitly (`git -C <worktree-path> …`) rather than writing into the primary checkout by accident.

If the fetch moved the base past what you read in step 2, re-read the spec landscape here — the worktree, not the primary checkout, is what you are writing into.

Some harnesses restrict shell redirection inside a worktree. If a heredoc or `>` is refused, use file-writing tools and plain single-purpose commands instead of fighting it.

**Done when:** the session is in a clean worktree on a new branch, and every write from here lands there.

### 5. Write and update

- **Update an existing spec:** weave the decision into the relevant section. Don't restate the conversation — the issue holds that; the spec holds the settled decision.
- **New spec:** use the [New-spec shape](#new-spec-shape) so `/to-tickets` consumes it the same way.
- **ADR:** use the [ADR shape](#adr-shape).

Every decision links back to its source GitHub issue — the spec is the *what*, the issue is the *why it was decided*.

**Done when:** every routed decision from step 3 is reflected in a file in the worktree.

### 6. Tighten with `/concise-copy`

Run `/concise-copy` over every file you touched. Specs are read repeatedly — earn their length.

### 7. Commit the specs and open the PR

The specs are not settled while they sit in a worktree only this session can see. Draft the message with **`/draft-commit-message`**, which owns the commit conventions — follow whatever it says, and don't restate its format here.

Give it what it can't work out for itself: the issues in play and what each is to this commit.

- The **map** is the ticket this work belongs to.
- The **decision issues** that fed the files are its detail.
- **None of them close.** `/wayfinder` closed the decision issues when their conversations ended, and the map stays open until `/specs-to-tickets` has sliced these specs.

Then commit in the worktree, push the branch, and open the PR against `main`.

**This skill never merges.** `/squash-merge-and-clean-up` lands the PR and removes the branch and the worktree; leave both in place until it runs.

**Done when:** every file written in step 5 is committed on this skill's branch and the PR is open.

### 8. Stamp each decision ticket as superseded

Go back to every decision issue that fed a spec and prepend this banner to its **body** — replacing an existing one if you're re-running:

```markdown
> **Superseded by spec — do not build from this ticket.**
> This decision now lives in `src/<Package>/spec/<feature>.md`, which is the source of truth and has almost certainly moved on since this was written. Below is *why* the decision was made; build from the spec.
```

Name every spec the decision fed. A decision dropped in step 1 gets no banner — nothing superseded it.

**Done when:** every decision issue routed in step 3 carries the banner, naming its spec file(s).

### 9. Update the map, then report

Write an overview of what you did back onto the **map body**, under a `## Specs settled` heading (see [contract](#the-maps-specs-settled-section)). This is the durable guide the next step — `/specs-to-tickets` — reads; the map stays the single place that shows where the effort is.

Then report to the user: what landed where, the PR the specs are waiting in, which decision issues were stamped, and that `/specs-to-tickets <map>` is the next step once the PR merges.

**Done when:** the map has a `## Specs settled` section listing every file written in step 5.

## The map's Specs-settled section

The handoff to `/specs-to-tickets`. Write it onto the map body (create the heading if absent; refresh it if re-run). One line per spec file — path, disposition, and the decision issues that fed it:

```markdown
## Specs settled
<!-- written by /decisions-to-specs -->
- `src/<Package>/spec/<feature>.md` — new — decisions: #12, #15
- `spec/<cross-cutting>.md` — updated — decisions: #13
- `src/<Package>/spec/adr/0003-<slug>.md` — ADR — decision: #14
```

Disposition is `new`, `updated`, or `ADR`. ADR lines are recorded but flagged so the next step knows **not** to slice them.

## Placement rules (locality ladder)

Prefer the **tightest scope that fully contains the decision**:

1. **Package/assembly `spec/`** — the decision affects one package. It may sit even closer to the code (beside the module) when that reads better.
2. **Root `spec/`** — cross-cutting: touches multiple packages, or the system's shape.
3. **`spec/adr/` (ADR)** — when the decision is **hard to reverse**, **surprising without context**, and **the result of a real trade-off** (all three, per Matt's ADR criteria). Fewer than three → not an ADR. The ADR folder nests under the `spec/` at the same scope as the decision: a package-scoped ADR goes in `<package>/spec/adr/`, a cross-cutting one in the root `spec/adr/`.

**Spec vs ADR:** a spec describes *what to build*; an ADR records *a decision and its rationale*. A decision can produce both — an ADR for the "why", a spec for the "what" — but split them only when each carries weight alone.

## New-spec shape

Mirror `/to-spec`'s template so `/to-tickets` reads it the same way. Trim any section a decisions-derived spec doesn't need:

- **Problem Statement** — from the user's perspective
- **Solution** — from the user's perspective
- **User Stories** — `As an <actor>, I want <feature>, so that <benefit>`
- **Implementation Decisions** — modules, interfaces, contracts, schema (no file paths / code)
- **Testing Decisions** — seams, what a good test covers
- **Out of Scope**

## ADR shape

Per the suite's ADR format: numbered `spec/adr/NNNN-slug.md` at the owning scope (scan that folder for the highest number, increment). Title + 1–3 sentences: context, decision, why. Add `Status` / `Consequences` only when they earn it. An ADR can be one paragraph — its value is recording *that* a decision was made and *why*.

## Split surfaces

GitHub holds the conversation (wayfinder maps + decision issues) and, later, the implementation tickets. The repo holds specs. Keeping them apart is the point: the record doesn't bloat the repo, and the specs aren't buried in an issue tracker.

## Where this sits in the flow

`/wayfinder` → GitHub **decision** issues (closed, rationale, stamped superseded) → **`/decisions-to-specs`** → repo **spec files** on a worktree branch, opened as a PR (+ `## Specs settled` on the map) → `/squash-merge-and-clean-up` → `/specs-to-tickets` → `/to-tickets` → GitHub **implementation** tickets (fresh, distinct from the decision issues) → `/implement`.

Optional: wire the terminal step into a wayfinder map's `## Notes` — *"when the route is clear, run `/decisions-to-specs`"* — or run it by hand whenever decisions have piled up enough to settle.
