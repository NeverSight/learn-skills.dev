---
name: agents-md
description: >-
  AGENTS.md: create, audit, or maintain the file. Use when the user mentions
  AGENTS.md, project instructions, instruction budget, or progressive disclosure of
  agent instructions.
license: MIT
metadata:
  capabilities: shell, edits-agent-instructions
---

# AGENTS.md

https://agents.md/ is the format baseline: plain Markdown, no required fields.
Nested files are optional. The closest `AGENTS.md` to the edited files has
precedence; some tools also load ancestor files, so keep root facts repo-wide
and package facts in the package file. Repo evidence and the user's explicit
instructions govern the content.

## Instruction budget

Every line loads on every turn, and every new session writes it to the prompt
cache again at a premium. Keep the file an index, not a manual. A line
earns its place when it is relevant to every single task, or when looking it
up in the environment is expensive.

Root file holds:

- One-sentence project description (what this repo is, and why work happens here)
- Package manager, when it is not the ecosystem default
- Build/test/typecheck commands that are non-standard or costly to discover
- Context pointers to domain docs, schemas, gold-standard tests, and skills
- Prevent Recurrence so later agents lock discoveries down

Everything else lives behind a pointer: a domain doc, a nested `AGENTS.md`, or
a skill. Hand-author from repo evidence; skip init-script dumps.

**Progressive Disclosure**: keep `AGENTS.md` lean (about 100 lines is a
heuristic, not a gate; a pointer table may run past it). Offload SOPs
and single-domain rules to a pointer or a skill.

**Pointers**: backtick paths, not `@path` and not markdown links. Occasion
plus `read` when the doc has a distinct branch; a label when it does not.
Shapes and why `@path` is a finding live in
[references/templates.md](references/templates.md). Convert `@path` and
markdown links in `AGENTS.md` to the matching shape. Convert `@path` in
`docs/agents/*.md` to a backtick path; markdown links there stay. Keep
`@AGENTS.md` at the top of a regular sibling `CLAUDE.md`; that is Claude
Code's include.

**Trust Model Judgment**: keep project-specific, non-derivable constraints.
Generic style and hygiene already live in the model.

**Single Source of Truth**: `package.json`, configs, and the tree are the live
source. Restate a fact here only when the lookup is expensive (a cache). Point
rather than copy.

**Rich References**: point at schemas and gold-standard tests instead of prose
specs. Describe capabilities and stable domain terms; skip file-by-file maps
(paths drift).

Write pointers in light-touch language: a conversational reference, not ALL-CAPS
or "ALWAYS".

## Monorepo boundaries

Root `AGENTS.md` owns policy, shared `docs/`, cross-package completion, and
Prevent Recurrence. Add a nested file only at an **autonomous boundary**. It is an
adapter for local invariants, domain pointers, and completion criteria.

Do not create files for `src/` or `tests`; add a deeper file only for a durable
local decision, and remove it when the decision disappears. Keep commands in
package config unless discovery is costly. Independently cloned packages need
their own root `AGENTS.md`; verify tool inheritance before relying on ancestors.
Start a package file with its one-sentence purpose. Repeat the package manager
only when its toolchain differs from the root or ancestor loading is unavailable.

## Workflows

### 1. Discovery & Quality Assessment

```bash
find . -name "AGENTS.md" -o -name "CLAUDE.md" -o -name ".claude.md" 2>/dev/null | head -50
```

Choose the target `AGENTS.md` explicitly:

- If exactly one `AGENTS.md` exists, use it.
- If multiple files exist, prefer the nearest `AGENTS.md` that governs the
  user's requested path or current working directory; otherwise ask before
  editing.
- In nested repositories or monorepos, the closest `AGENTS.md` to the edited
  files has precedence for that subtree (nested files are optional).
- If none exists, create the root `AGENTS.md` unless the user requested a
  narrower package/module path.

Done when the target path is named.

Then grade that file with [references/quality-criteria.md](references/quality-criteria.md):
Micromanagement Audit, Bloat, contradictions, every-task placement, stale
caches, `@path` file references, and markdown links in `AGENTS.md`. Scan
`docs/agents/*.md` for the same `@path` file references; markdown links
there stay. Propose the matching pointer shape from
[references/templates.md](references/templates.md) §4 — occasion plus
`read`, or `Label: path`, and a backtick path in a domain doc. Emit a
Quality Report before any edit.

Done when the report is in the conversation and no edit has started.

### 2. Claude Code Check

Claude Code 2.1.277+ reads a project's `AGENTS.md` when it has no `CLAUDE.md`,
so leave `CLAUDE.md` absent: no file, no symlink.

- **Sibling `CLAUDE.md` is a symlink to `AGENTS.md`**: leave it; mention it is
  optional on 2.1.277+ and the user may delete it.
- **Regular `CLAUDE.md` that imports its local `AGENTS.md` and adds only
  Claude-specific rules**: preserve it.
- **Any other regular `CLAUDE.md`**: it shadows `AGENTS.md`. Read it, summarize
  unique instructions, propose migration, and ask approval before replacing it.
- **`CLAUDE.local.md` present**: it also counts as a `CLAUDE.md` and stops
  `AGENTS.md` from loading; the user sets `/config` Project instructions to
  `claude-md-and-agents-md` to read both.
- **Older Claude Code**: tell the user they can run
  `ln -s AGENTS.md CLAUDE.md` themselves.

Done when the next action is known and a regular `CLAUDE.md` is still intact
unless the user approved replacement.

### 3. Creation & Updates

Load [references/templates.md](references/templates.md) for this branch.

- Build or slim the file as an index: one-sentence description, non-default
  package manager, non-standard commands, pointers.
- Apply **Progressive Disclosure**: offload multi-step SOPs and single-domain
  rules. Convert `@path` and markdown links in `AGENTS.md` to the matching
  pointer shape. Convert `@path` in `docs/agents/*.md` to backtick paths.
- On a bloated existing file, group leftovers by domain, ask which of any
  contradictory pair to keep, and flag no-ops / vague / obvious lines for
  deletion.
- Include the `Prevent Recurrence` section rules in `AGENTS.md` so all future
  agents follow them.

Done when every remaining root line passes the every-task test or is a pointer.

### 4. Prevent Recurrence (on problem-solving)

When solving a problem turns up a gotcha, a hidden config, or an env var
quirk, the agent MUST:

1. **Candidate**: Name who hits it again, in which file, on what change. No
   such scenario, nothing to propose. Then sort it: a preventable slip, or an
   environment fact no assertion can reach? Gates in
   [references/quality-criteria.md](references/quality-criteria.md).
2. **Promote**: Offer the first tier that applies and only that one — the same
   knowledge twice is the duplicate Prune exists to remove. Every tier waits on
   the user's explicit confirmation.
   - **Enforce it**: an assert, a type, or a test leaves nothing to remember.
     Quote its size and the files it touches so one word can authorize it. It
     has to be able to fail on the mistake itself; where only the symptom is
     checkable, the knowledge belongs a tier down.
   - **Comment at the site that must be passed**: the constant a new caller
     imports, the declaration a change has to touch. Cross-reference from the
     other sites rather than restating it.
   - **An agent-facing doc**, only for what no site owns (environment,
     toolchain, CI, a process spanning files) — and say in one sentence why
     the tiers above cannot hold it. Merge into an existing topic doc;
     otherwise follow the repo's agent-facing docs convention —
     `docs/agents/<topic>.md` where none exists yet — without relocating
     existing files. Fall back to `lessons-learned.md` beside it. Add or update
     a single backtick-path line per file under Pointers, never a standalone
     "Lessons Learned" heading.
3. **Prune**: Whenever Promote reaches the doc tier, read that whole file
   before writing to it — you are already in it with the gates in hand, so
   the audit costs one pass — and propose deletions alongside the addition,
   judged per entry rather than by a count. An entry goes once stale
   (library/version upgraded past the tagged context, now enforced by a
   linter/type/test, duplicated across files, or a one-off debugging
   transcript). Enforcement prunes too: an entry it supersedes in a doc
   already read this session goes with it.
   "Periodically" is not a trigger an agent can act on; the file being open is.
4. **Legacy migration**: If this section under any earlier heading stops at
   writing to a file, or gotchas sit inline under `## Lessons Learned`, propose
   the current heading and wording, and move inline entries out to the
   topic/fallback file(s), leaving reference line(s) — pending confirmation.

Done when one means of prevention is in front of the user, or no recurrence
scenario survived the gates.

## References

- Audit rubric: [references/quality-criteria.md](references/quality-criteria.md)
- Starter templates: [references/templates.md](references/templates.md)
- Mock runs: [references/examples.md](references/examples.md)
