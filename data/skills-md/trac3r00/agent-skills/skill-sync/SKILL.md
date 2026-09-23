---
name: skill-sync
description: Discovers custom skills across every AI provider install on the machine — Claude Code, Codex, OMO, gjc, OpenCode, Gemini, Cursor, Factory, and plugin caches — and unifies them into one universal directory (symlinks by default) so any SKILL.md-reading agent can use all of them. Reports provenance, dedupes by name and resolved path, and surfaces cross-provider conflicts.
when_to_use: You have skills scattered across multiple agent CLIs and want one canonical inventory or one directory every agent reads. Also for auditing what is installed where, or gating CI on cross-provider name conflicts. NOT a marketplace client — it never downloads anything; it only unifies what is already installed locally.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [skills, interop, discovery, sync, multi-agent]
---

# Skill Sync

One machine, many agents, one skill library. `skill_sync.py` scans the known
skill roots of every AI provider, parses each `SKILL.md` frontmatter, dedupes,
and can materialize the union into a single universal directory.

## Commands

```bash
python3 scripts/skill_sync.py doctor          # which provider roots exist here
python3 scripts/skill_sync.py list            # unified inventory with provenance
python3 scripts/skill_sync.py list --json     # machine-readable
python3 scripts/skill_sync.py sync --dry-run  # preview what would be linked
python3 scripts/skill_sync.py sync            # symlink all into ~/.agents/skills
python3 scripts/skill_sync.py sync --copy --target /some/dir   # portable copies
```

## Scanned providers (priority order — earlier wins name conflicts)

1. `~/.agents/skills` (the universal target itself)
2. `~/.claude/skills` (Claude Code user skills)
3. `~/.codex/skills` (Codex)
4. `~/.omo/skills` and the omo-ai plugin install (OMO/Senpi)
5. `~/.gjc/skills` (gajae-code)
6. `~/.config/opencode/skills` (OpenCode)
7. `~/.gemini`, `~/.cursor`, `~/.factory` skills dirs
8. `~/.claude/plugins/cache/*/*/*/skills` (installed plugin skills; newest
   version of a plugin wins over older cached versions)

Add any other root with `--root DIR` (repeatable). Missing roots are skipped
silently — `doctor` shows what exists. `--no-default-roots` scans only the
`--root` dirs you pass (useful for tests and scripted audits).

## Semantics

- **Dedupe**: identical resolved paths (symlinks back to the same skill) count
  once; same name from different providers keeps the highest-priority one and
  records a conflict.
- **Sync is non-destructive**: existing entries in the target are never
  overwritten; a mismatch is reported as `skip-exists`. Symlinks keep the
  provider's copy as the single source of truth; `--copy` makes standalone
  copies for machines you'll sync to.
- **Gate**: `--fail-on-conflict` exits 1 when two providers ship different
  skills under the same name — useful in CI or a dotfiles check.

## Making agents read the universal directory

Most SKILL.md-reading agents accept a skills directory: point Claude Code,
Codex, OMO, or any other harness at `~/.agents/skills` (many already read it).
After `sync`, every provider-specific skill is available to every agent.
