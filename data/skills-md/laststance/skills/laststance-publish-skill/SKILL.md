---
name: laststance-publish-skill
description: Publish or update a registry skill
---

# Publish Skill to laststance/skills

## Codex Compatibility
When running this skill in Codex, translate Claude Code-only primitives before acting: `AskUserQuestion` -> chat/request_user_input, `TodoWrite` -> `update_plan`, `Task`/`TaskCreate`/`TeamCreate`/`SendMessage` -> `spawn_agent`/`send_input`/`wait_agent` when available and allowed, and `EnterPlanMode`/`ExitPlanMode` -> a concise chat plan plus explicit approval.
Resolve `Read`/`Write`/`Edit`/`Bash`/`WebSearch`/`WebFetch` to Codex file/shell/web tools, and map `~/.claude/...` paths to `~/.agents/...` or `~/.codex/...` unless the task explicitly targets Claude Code.

## Cursor Compatibility
When running this skill in Cursor Agent, translate Claude Code-only primitives before acting: `AskUserQuestion` -> `AskQuestion`; `TodoWrite` -> Cursor `TodoWrite` or an equivalent checklist; `Task`/`TaskCreate`/`TeamCreate`/`SendMessage`/multi-agent flows -> Cursor `Task` (subagents), parallel Tasks, or `run_in_background` when allowed (`TeamCreate`/`SendMessage` may have no exact match); `EnterPlanMode`/`ExitPlanMode` -> Plan mode (`SwitchMode` / `CreatePlan`) plus explicit user approval.
Resolve `Read`/`Write`/`Edit`/`StrReplace`/`Bash`/web/search/MCP via Cursor Composer or Agent equivalents. MCP names written as `mcp__server__tool` typically map to `call_mcp_tool` with configured server identifiers. Map `~/.claude/...` to `~/.cursor/skills/`, `.cursor/skills/`, and `.cursor/rules/` unless the task explicitly targets Claude Code.


Publish a tested skill to the `laststance/skills` repository for distribution via `npx skills add`, or ship local changes to a skill that is already published there.

## Prerequisites

- Skill is stable (passed Phase 2 testing in ~/.codex/skills/ and ~/.vscode/skills/)
- Repository cloned at `~/laststance/skills`, on `main` and level with `origin/main`
- Skill has a valid `SKILL.md` with frontmatter (`name`, `description`)

## Publish Steps

Unmarked text applies to both branches; **new** / **update** marks text for one branch only.

### 1. Pick the branch

```bash
test -d ~/laststance/skills/skills/<name> && echo update || echo new
```

- **new**: `skills/<name>/` is absent, so the skill is not in the registry yet.
- **update**: `skills/<name>/` exists, so the skill is already published and your edits live in the installed copy. `~/.claude/skills/<name>` is a symlink to `~/.agents/skills/<name>/`, which `npx skills` manages and records in `~/.agents/.skill-lock.json`.

### 2. Copy skill to repository

**new**:

```bash
mkdir -p ~/laststance/skills/skills/<name>
cp -r ~/.claude/skills/<name>/* ~/laststance/skills/skills/<name>/
```

**update**: read the difference first, then copy:

```bash
diff -r ~/laststance/skills/skills/<name> ~/.claude/skills/<name>/
cp -r ~/.claude/skills/<name>/* ~/laststance/skills/skills/<name>/
```

Every line of that diff is an intended change. `cp` only adds and overwrites: a new file (`Only in …/.claude/skills/<name>: <file>`) lands in the repo, while a file you deleted locally (`Only in …/laststance/skills/skills/<name>: <file>`) stays there until you `git rm skills/<name>/<file>`. The copy is done when the repo status lists every file the diff reported (`M` changed, `??` new, `D` deleted):

```bash
git -C ~/laststance/skills status --short skills/<name>/
```

Copy only the skill's own files (SKILL.md + supporting files); test artifacts and local-only files stay behind. The repository is public: rewrite project-specific examples, internal names, and secrets into generic wording before the copy lands.

### 3. Update README.md

**update**: the skill already has its install command (A), usage example (C), and a place in the badge count (D); leave those as they are. Re-read its Available Skills row (B) against the new `SKILL.md` and rewrite the row wherever it describes behavior the skill no longer has, or misses behavior it gained. Touch the usage example only when its arguments or one-line summary no longer fit.

**new**: 4 places. Sections A–C maintain **alphabetical order**; D is a count.

**A. Install commands** — Add to the specific skill install list:

```bash
npx skills add laststance/skills --skill <name>
```

**B. Available Skills table** — Add row in alphabetical position:

```markdown
| [<name>](skills/<name>/) | <description> | <dependencies or —> |
```

Dependencies format:
- No deps: `—`
- Optional: `[Name](url) (recommended)`
- Required: `[Name](url) **(required)**`

**C. Usage examples** — Add entry in alphabetical position:

```
/<name> <typical-args>              # Short description
```

**D. Skills count badge** — bump the skill count in the shields.io badge near the top of the README:

```markdown
img.shields.io/badge/skills-<N>-2563EB
```

`<N>` = total skill count after this publish: `ls ~/laststance/skills/skills/*/SKILL.md | wc -l`.

### 4. Commit and push

```bash
cd ~/laststance/skills
git add skills/<name>/ README.md
git commit -m "$(cat <<'EOF'
feat: add <name> skill — <short description>
EOF
)"
git push
```

**update**: title the commit `feat: update <name> skill — <what changed>` or `<type>(<name>): <what changed>`, where `<type>` is the Conventional Commits type of the change (`feat` added behavior, `fix` a correction, `refactor`, `docs`). Skills changed together ship in one commit (`feat: update save/load skills — …`).

### 5. Sync the installed copy

**new**: install via CLI to create symlinks across all AI tools:

```bash
npx skills add laststance/skills --skill <name> -g -y
```

This installs to `~/.agents/skills/<name>/` and creates symlinks in `~/.claude/skills/`, `~/.codex/skills/`, `~/.vscode/skills/`, etc. The hand-created original in `~/.claude/skills/` is replaced by the symlink. `-g` pins the user-level scope: without it a non-interactive run installs into the current directory's `.agents/skills/`, which right after step 4 is the repository. The output line `PromptScript does not support global skill installation` is expected; the command still exits 0.

**update**: run once the push has landed:

```bash
npx skills update <name> [<name>...] -g -y
```

`update` rebuilds `~/.agents/skills/<name>/` from the published repository, so the push comes first: run earlier, it replaces your unpublished edits with the old published files. Afterwards the lock is level with the push:

```bash
git -C ~/laststance/skills rev-parse HEAD:skills/<name>   # equals skillFolderHash of <name> in ~/.agents/.skill-lock.json
```

## Checklist

- [ ] Branch picked (**new** / **update**)
- [ ] Skill files copied to `~/laststance/skills/skills/<name>/`; diff read for project-specific names and secrets
- [ ] **update**: `git status --short skills/<name>/` lists every file `diff -r` reported, deletions included
- [ ] **new**: README install command added (alphabetical)
- [ ] **new**: README skills table row added (alphabetical)
- [ ] **new**: README usage example added (alphabetical)
- [ ] **new**: README skills count badge bumped (`skills-<N>`)
- [ ] **update**: README table row matches the new `SKILL.md`; install command and badge unchanged
- [ ] Committed as `feat: add <name> skill` (**new**) or `feat: update <name> skill — …` / `<type>(<name>): …` (**update**)
- [ ] Pushed to remote
- [ ] **new**: installed with `npx skills add … -g -y`; `~/.claude/skills/<name>` is now a symlink
- [ ] **update**: `npx skills update` run after the push; `skillFolderHash` equals `HEAD:skills/<name>`
