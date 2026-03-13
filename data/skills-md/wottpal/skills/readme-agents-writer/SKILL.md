---
name: readme-agents-writer
description: Build and maintain unified README.md + AGENTS.md + CLAUDE.md docs where symlink-triplet policy is strict, and the canonical README remains an in-depth, high-signal agent instruction and engineering playbook.
---

# README/AGENTS/CLAUDE Writer

## Mission

Produce documentation that works for both humans and coding agents:

- Keep the 3-file schema strict (`README.md`, `AGENTS.md`, `CLAUDE.md`).
- Keep the instruction quality high enough for autonomous execution (guardrails, conventions, playbooks, do/don't rules, verification steps, and escalation rules).
- Keep guidance agent-agnostic: no model/vendor-specific logic unless a separate compatibility note is unavoidable.

If `AGENTS.md` and `CLAUDE.md` symlink to `README.md`, the README is no longer "just a project readme"; it is the full operational source of truth.

## When To Use

- Creating or updating documentation triplets (`README.md`, `AGENTS.md`, `CLAUDE.md`)
- Converting dedicated `AGENTS.md` / `CLAUDE.md` files to symlinked companions
- Refactoring large docs while keeping agent guidance accurate, explicit, and current
- Strengthening weak instruction files that are vague, stale, or hard for agents to execute safely

## When Not To Use

- Repos that intentionally keep different content in `README.md`, `AGENTS.md`, and `CLAUDE.md`.
- Environments where symlinks are disallowed by policy/tooling.
- Requests that are only content edits where triplet ownership is already intentionally defined elsewhere.

## Non-Negotiables

### 1) File Structure Policy (Triplet Contract)

For any directory that owns this documentation unit, use one of these two allowed patterns:

1. Standard pattern
   - `README.md` is the canonical file in that directory.
   - `AGENTS.md -> README.md`
   - `CLAUDE.md -> README.md`

2. Shared-doc exception
   - `README.md`, `AGENTS.md`, and `CLAUDE.md` are all symlinks to the same canonical `README.md` in another directory.
   - Use this only when all of these are true:
     - Same owner/team and release cadence.
     - Same audience and operational intent.
     - No directory-specific setup/rules that would diverge.

Never keep dedicated/non-symlink `AGENTS.md` or `CLAUDE.md` when a directory uses this triplet model.
Avoid shared-doc mode when docs are expected to evolve independently.

### 2) Instruction Depth Policy (Canonical README Must Be Agent-Operational)

Even with symlinked companions, the canonical `README.md` must include in-depth agent-operational guidance:

- Scope and ownership boundaries
- Safety guardrails and non-negotiable constraints
- Conventions and coding standards (repo-specific, not generic)
- Engineering playbook (setup, test/lint/build, release, and troubleshooting)
- Do/Don't rules with concrete examples
- Verification workflow (how to prove claims and detect stale docs)
- Escalation policy for ambiguity, destructive actions, and risky operations

If this depth is missing, the triplet setup is incomplete even when symlinks are correct.

## Required Commands

Default workflow (recommended):

```bash
scripts/set-doc-triplet.sh <dir>
scripts/set-doc-triplet.sh <dir> <relative-path-to-canonical-README.md>
python3 scripts/check-doc-triplets.py [root]
```

Manual fallback (advanced):

```bash
cd <dir>
# Standard pattern
ln -snf README.md AGENTS.md
ln -snf README.md CLAUDE.md

# Shared-doc exception
TARGET=<relative-path-to-canonical-README.md>
ln -snf "$TARGET" README.md
ln -snf "$TARGET" AGENTS.md
ln -snf "$TARGET" CLAUDE.md
```

Instruction-quality review (always run during doc updates):

```bash
rg -n 'TODO|TBD|FIXME|maybe|probably|should be' README.md
python3 scripts/check-doc-triplets.py [root]
```

## Workflow

1. Classify scope first
   - Root doc, workspace/app/package/service doc, or module/feature doc.
   - Choose section depth based on scope (load `references/scope-patterns.md`).
2. Confirm triplet mode is actually desired
   - If separate files are intentionally different, do not enforce symlink triplets.
3. Build a verified fact inventory
   - Verify every filepath, variable/constant name, command, dependency, and version.
   - Do not trust existing docs without checking live code/config.
   - Use `references/fact-verification.md`.
4. Design instruction architecture before prose
   - Separate hard constraints from preferences.
   - Convert vague guidance into trigger/action rules ("When X, do Y").
   - Keep rules agent-agnostic (do not assume one tool's private behavior model).
   - Plan sections for guardrails, conventions, playbooks, and escalation.
   - Use `references/agent-instruction-best-practices.md`.
5. Plan with temporary structure files (avoid local maxima and context bloat)
   - Create concise planning files under `.tmp/readme-doc-plan/` before final writing.
   - Keep these as bullet/TODO artifacts, not full prose.
   - Use `references/low-context-drafting.md`.
6. Draft and refactor in two passes
   - Pass 1: structure, ownership boundaries, must/never rules, key commands.
   - Pass 2: remove stale statements, collapse duplication, sharpen actionability and determinism.
7. Enforce triplet symlink policy
   - Use `scripts/set-doc-triplet.sh` for direct creation/fix.
   - Use `scripts/check-doc-triplets.py` for audit + auto-generated fix commands.
8. Run instruction quality QA
   - Check for ambiguity, contradictory rules, and missing failure-mode guidance.
   - Ensure there are repo-specific examples (good/bad where useful).
   - Re-check against `references/agent-instruction-best-practices.md`.
9. Final freshness pass
   - Re-run verification commands for anything changed during writing.
   - Ensure scope-appropriate content (no root-only setup details in small module docs).

## Quality Bar

All of the following are required:

- Content is specific, verifiable, and operational.
- Commands are copy/paste ready and runnable from stated working dirs.
- Paths exist at time of writing.
- Variable names and constants match code exactly and are used as described.
- Versions reflect currently installed/declared dependencies.
- Instructions use explicit trigger/action language, not soft ambiguity.
- Hard constraints are clearly marked as mandatory vs optional guidance.
- Safety-critical operations include confirmation/escalation rules.
- Examples demonstrate both compliant and non-compliant patterns where ambiguity risk is high.
- Wording stays agent-agnostic and portable across tooling.

## References

- `references/scope-patterns.md`
- `references/fact-verification.md`
- `references/low-context-drafting.md`
- `references/agent-instruction-best-practices.md`

## Scripts

- `scripts/set-doc-triplet.sh`
- `scripts/check-doc-triplets.py`
