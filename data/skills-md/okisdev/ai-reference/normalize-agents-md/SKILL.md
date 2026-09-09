---
name: normalize-agents-md
description: Rewrite a repository's AGENTS.md and CLAUDE.md files into short normative instruction files, routing incidents, inventories, and module internals to where they belong, within the size caps every harness reads.
argument-hint: "[scope]"
---

## Context

Instruction files and caps: !`python3 "$HOME/.agents/skills/normalize-agents-md/scripts/measure.py" . 2>/dev/null | head -40 || echo "(measure script unavailable)"`

Uncommitted instruction files: !`out=$(git status --short 2>/dev/null | grep -E '(AGENTS|CLAUDE|GEMINI)[^/]*\.md$' | head -5); echo "${out:-(none)}"`

Docs homes present: !`out=""; for f in README.md CONTRIBUTING.md ARCHITECTURE.md docs; do test -e "$f" && out="$out $f"; done; echo "${out:-(none)}"`

## Instructions

Rewrite every instruction file in scope into a short normative document: keep the rules, move everything else to its owning home, remove what generators wrote, add a file only where the tree needs one, prove nothing load-bearing was lost, and stop at an uncommitted tree.

### Process

1. Parse `$ARGUMENTS` (a scope path, default the repository root; every instruction file under the scope is processed, and files above it are read for inheritance only). Keep the Context measurement as the before state. A file with uncommitted changes is `skip: uncommitted changes`, because another session may own it.
2. Read [references/standard.md](references/standard.md) (layout, caps, altitude test, routing table, coverage test, template, placeholder and generator dispositions, README handling), then the project memory index via `use-project-memory`, then the repository's docs homes (README, CONTRIBUTING, ARCHITECTURE.md, `docs/`), so moved content lands in an existing home.
3. Inventory each file in scope: harness owner, symlink target, `@import` lines, placeholders and generator blocks per the standard, the nested files whose scope it overlaps, and the READMEs the measurement flags as carrying agent-facing lines. Every placeholder is removed (a framework's fixed block, a scaffold preamble, a file-name title, an empty template heading, a TODO); a file that was only placeholder is deleted together with its CLAUDE.md stub; the one obligation a block carried moves to the root as a single line; a generator with a switch is turned off in the same pass (Next.js: `agentRules: false` in that app's next.config) and one without is named in the report. A template directory and anything under a vendored or fixture tree are classified, left unchanged, and reported.
4. Build the ledger in the scratchpad, never in the repository: split each editable file, and each flagged README's agent-facing sections, into clauses (a bullet holding several rules yields several entries), classify each clause with the standard's categories and its reader (a person or an agent), and assign `keep`, `move <destination>`, or `drop <reason>`. A clause that claims a test, lint, or script enforces it stays a rule until the enforcer is found and its assertion read. A path or command the clause names is checked for existence, and a factual claim about the tree (a directory holds no X, a file is the only Y) is checked by grep; a stale one is corrected or dropped, never carried forward.
5. Write destinations before touching the source: incidents and decisions become a project memory topic via `use-project-memory` with the SHA or issue as citation; package-scoped rules go down into that package's AGENTS.md (created with the CLAUDE.md stub when missing); contributor process rules go to CONTRIBUTING.md when the repository is public; human-facing content goes to the README when it lacks it; agent-facing README sections come the other way into AGENTS.md, leaving at most one pointer line in the README; roles nobody can read from names go to the existing ARCHITECTURE.md or docs page, never a docs tree created for this; everything else goes nowhere.
6. Cover the tree: list the workspace packages and apps (`pnpm-workspace.yaml`, `package.json` workspaces, `turbo.json`, top-level `apps/` and `packages/`) and apply the standard's coverage test to every directory without an AGENTS.md, reading its README, manifest, and scripts for commands and traps; create the file only when at least one rule or command survives the altitude test, and record `covered by root` for the rest. A repository with no root file gets the minimal root from the template: title line, commands, editing contract, and the CLAUDE.md stub.
7. Rewrite each file to the standard's template: one rule per bullet with at most one because-clause naming the failure it prevents, a rule an existing check asserts becomes a one-line pointer, a nested file holds only what the root does not. Import lines stay byte-identical. CLAUDE.md becomes exactly `@AGENTS.md` and a newline, plus a `## Claude Code` section only for Claude-only content; a diverging CLAUDE.md and AGENTS.md pair merges into AGENTS.md; CLAUDE.local.md is never touched. Then reread the result section by section and delete every survivor an agent could get from one `ls` or one manifest read, because filler survives the first pass in slimmed form, most often as pointers that only say what a directory holds.
8. Loss check in a fresh subagent with none of the rewriting context: hand it the old files (instruction files and any edited README), the new files, and the destinations, and ask for every obligation in the old files absent from the new files and their destinations. Restore or consciously drop each item it names, and record the reason. Then rerun `python3 "$HOME/.agents/skills/normalize-agents-md/scripts/measure.py" <scope> --strict`: every file within the caps, no generator left on beside a deleted block, and every overflow past a target named with the rules that could not be cut.
9. Report per file the before and after bytes and lines, the Codex chain and Grok cap status, deleted generated files and disabled generators, created files with the coverage reason, moved items with destinations, dropped items with reasons, contradictions resolved, skipped files, and the `measure.py --strict` command a repository can wire into CI. Stop at an uncommitted tree; committing composes `commit-changes`, shipping composes `ship-pr`.

### Rules

- A rule the file says nothing enforces is never dropped; it moves to the top of Rules.
- Narrative never flows back into an instruction file from memory or a session; content crosses between README and AGENTS.md only by reader, and neither keeps the other's copy beyond one pointer line.
- A size target is never met by deleting a rule; overflow is reported instead.
- A placeholder never survives because it might come back; the switch lands in the same pass when one exists, and the marker is reported when none does.
- A new file with nothing to say is never created; absence is the valid outcome.
- No new dependency; the measure script stays Python 3 standard library.
