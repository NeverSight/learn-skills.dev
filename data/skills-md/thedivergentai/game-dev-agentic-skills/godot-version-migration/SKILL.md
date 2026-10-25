---
name: godot-version-migration
description: "Full-history Godot version migration hub. Use when upgrading any Godot project toward the library target (currently 4.7)—from 1.x/2.x legacy eras through 3→4 and hop-by-hop 4.x minors—or finding Domain Skill-scoped migration notes. Trigger keywords: upgrade Godot, migrate Godot version, Godot 3 to 4, Godot 2 to 3, upgrading_to_godot, version migration, breaking changes, convert-3to4, TileMapLayer, AnimationMixer, engine.cfg, project.godot."
---

# Godot Version Migration

Orchestrator for **engine version upgrades** from early Godot through the library target. Domain Skills document **current** APIs; this hub owns the upgrade path.

**Library target:** Godot **4.7+**

Corpus: [docs changelog](https://docs.godotengine.org/en/stable/about/docs_changelog.html) · [interactive changelog](https://godotengine.github.io/godot-interactive-changelog/) · [download archive](https://godotengine.org/download/archive/) · [GitHub releases](https://github.com/godotengine/godot/releases) · [migrating index](https://docs.godotengine.org/en/stable/tutorials/migrating/index.html)

## NEVER Do

- **NEVER skip majors** — route 1.x → 2.x → latest 3.x → 4.0 before any 4.x minor ladder.
- **NEVER skip 4.x hops** — upgrade `4.0 → 4.1 → … → 4.7` one minor at a time; stabilize after each hop.
- **NEVER** claim automatic 1.x→4.x conversion or bit-exact autopilot.
- **NEVER** treat Domain Skill bodies as migration changelogs — load `references/<topic>.md` (mirrored from each skill’s `references/migration-notes.md`).
- **NEVER** load all module notes at once — only subsystems present in the project.
- **NEVER** mix server/client Godot minors for high-level multiplayer (especially across 4.2→4.3 SceneMultiplayer protocol changes).
- **NEVER** choose Mesh “Restart & Upgrade” without VCS backup (4.1→4.2 mesh format).
- **NEVER** run the 3→4 converter without a full backup (tool does not backup).

## Version detect

1. Read `project.godot` (`config_version`, `config/features`) or legacy `engine.cfg`.
2. Ask the user if files are ambiguous.
3. Map to an era in [references/era-index.md](references/era-index.md).

## Workflow router (MANDATORY)

| Detected era | Load | Do NOT |
|--------------|------|--------|
| 1.x / early 2 | [legacy/pre-2-context.md](references/legacy/pre-2-context.md) | Invent a 1→4 converter |
| 2.x | [legacy/2-to-3.md](references/legacy/2-to-3.md) then stabilize on **latest 3.x** | Jump straight to 4.7 notes |
| 3.x | [bridges/3-to-4.md](references/bridges/3-to-4.md) + official 3→4 guide | Skip latest-3.x stabilize gate |
| 4.x `< 4.7` | Official hop guide + [hop-index.md](references/hop-index.md) module notes for touched systems | Skip minors |
| Already 4.7+ | [godot-master](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-master/SKILL.md) / Domain Skills | Treat this hub as a coding tutorial |

### Steps (4.x minors)

1. While `current < 4.7`, perform **exactly one** hop to `current + 0.1`.
2. Open the official upgrading page for the destination version.
3. From [hop-index.md](references/hop-index.md), open only module notes for subsystems present in the project.
4. Apply fixes; open in the new editor; playtest; repeat.

## Hop table

### Majors / bridges

| Era | Resource |
|-----|----------|
| 1.x archaeology | [legacy/pre-2-context.md](references/legacy/pre-2-context.md) |
| 2.x → 3.x | [legacy/2-to-3.md](references/legacy/2-to-3.md) |
| 3.x → 4.0 | [bridges/3-to-4.md](references/bridges/3-to-4.md) · [official guide](https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.html) |
| Ladder overview | [era-index.md](references/era-index.md) |

### 4.x minors

| Hop | Official guide |
|-----|----------------|
| 4.0 → 4.1 | https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.1.html |
| 4.1 → 4.2 | https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.2.html |
| 4.2 → 4.3 | https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.3.html |
| 4.3 → 4.4 | https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.4.html |
| 4.4 → 4.5 | https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.5.html |
| 4.5 → 4.6 | https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.6.html |
| 4.6 → 4.7 | https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.7.html |

Cross-skill checklist: [references/hop-index.md](references/hop-index.md)

## Module directory

Mirrored Domain Skill migration notes live at `references/<topic>.md` (e.g. `references/2d-physics.md`). Hub-native `legacy/`, `bridges/`, and `era-index.md` are **not** Domain Skill mirrors.

```text
sync_godot_version_migration.py --all
```

## Reference

### Official docs

- [Migrating to a new version](https://docs.godotengine.org/en/stable/tutorials/migrating/index.html)
- [Upgrading from Godot 3 to Godot 4](https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.html)
- [Docs changelog](https://docs.godotengine.org/en/stable/about/docs_changelog.html)

### Related Skills

#### Master
- [godot-master](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-master/SKILL.md) — Library router for current Domain Skill modules after migration is complete.

#### Downstream / consumers
- [godot-analyst](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-analyst/SKILL.md) — Score architecture on the **target** APIs after hops land.
- [godot-auditor](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-auditor/SKILL.md) — Never-list / legacy-syntax verification after upgrades.
- [godot-builder](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-builder/SKILL.md) — CI / headless bake against the new engine target after each hop.

#### Complements
- [godot-project-foundations](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-project-foundations/SKILL.md) — Project settings / structure once on the target version.
- [godot-gdscript-mastery](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-gdscript-mastery/SKILL.md) — Typed GDScript 2.0 idioms after 3→4 / 4.x language hops.
- [godot-export-builds](https://github.com/thedivergentai/gd-agentic-skills/blob/main/skills/godot-export-builds/SKILL.md) — Re-validate exports after each hop that touches platforms.
