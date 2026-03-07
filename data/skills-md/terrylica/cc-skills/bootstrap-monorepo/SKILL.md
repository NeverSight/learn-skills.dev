---
name: bootstrap-monorepo
description: Autonomous polyglot monorepo bootstrap meta-prompt. TRIGGERS - new monorepo, polyglot setup, scaffold Python+Rust+Bun, monorepo from scratch.
allowed-tools: Read
disable-model-invocation: true
---

# Bootstrap Polyglot Monorepo

This skill redirects to the canonical reference in mise-tasks.

→ **See**: [mise-tasks/references/bootstrap-monorepo.md](../mise-tasks/references/bootstrap-monorepo.md)

## When to Use This Skill

Use this skill when:

- Starting a new polyglot monorepo from scratch
- Setting up Python + Rust + Bun/TypeScript project structure
- Need autonomous 9-phase bootstrap workflow (includes release setup)
- Want Pants + mise integration for affected detection

## Stack

| Tool      | Responsibility                                                         |
| --------- | ---------------------------------------------------------------------- |
| **mise**  | Runtime versions (Python, Node, Rust) + environment variables          |
| **Pants** | Build orchestration + native affected detection + dependency inference |

## Quick Commands

```bash
# After bootstrap, use these Pants commands:
pants --changed-since=origin/main test    # Test affected
pants --changed-since=origin/main lint    # Lint affected
pants tailor                               # Generate BUILD files
pants list ::                              # List all targets
```

## Related Skills

- `itp:mise-tasks` - Task orchestration and affected detection (Level 11)
- `itp:mise-configuration` - Environment and tool version management
- `itp:semantic-release` - Release automation (Phase 8 reference)

---

## Troubleshooting

| Issue                      | Cause                      | Solution                                          |
| -------------------------- | -------------------------- | ------------------------------------------------- |
| Pants not found            | Not installed              | Install via `brew install pantsbuild/tap/pants`   |
| mise not loading           | Shell hook not configured  | Configure mise shell hook in ~/.zshrc             |
| BUILD files not generated  | Missing `pants tailor`     | Run `pants tailor` to generate BUILD files        |
| Affected detection empty   | No base branch set         | Ensure `origin/main` exists and is up to date     |
| Python version mismatch    | mise vs Pants conflict     | Align Python version in mise.toml and pants.toml  |
| Rust targets not found     | Pants Rust backend missing | Enable Rust backend in pants.toml                 |
| Node/Bun not detected      | Not in mise tools          | Add to mise.toml: `node = "latest"` or `bun`      |
| Dependency inference fails | Missing imports in source  | Ensure explicit imports, run `pants tailor` again |
