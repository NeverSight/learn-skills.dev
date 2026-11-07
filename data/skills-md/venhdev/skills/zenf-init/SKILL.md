---
name: zenf-init
description: "Scaffold repository task tracking, test harness anchor, dev environment profile, Git ignore privacy, documentation index, and agent constitution."
disable-model-invocation: true
---

# zenf-init — Repository Scaffolding Engine

## Operating Invariants

- **Pre-Mutation Gate**: Stage strictly missing assets via Changeset and halt turn for human approval; never overwrite valid existing configurations.
- **Privacy Baseline**: Always isolate `.agents/scratch/` in `.gitignore`; forbid committing transient scratch files or secrets.

## Domain Rubric

### 1. Task Tracker Matrix (`.agents/task-tracker.md`)

- Remote GitHub + `gh auth status` valid ──> Propose **GitHub Issues (`gh`)** (template [`references/issue-tracker-github.md`](./references/issue-tracker-github.md)) or **Local Markdown**.
- Remote GitLab + `glab auth status` valid ──> Propose **GitLab Issues (`glab`)** (template [`references/issue-tracker-gitlab.md`](./references/issue-tracker-gitlab.md)) or **Local Markdown**.
- Unauthenticated CLI / Other remotes / Offline ──> Propose **Local Markdown** (`.agents/tasks/`, template [`references/issue-tracker-local.md`](./references/issue-tracker-local.md)). Report CLI auth status to user so they can choose to authenticate or remain local.

### 2. Harness Anchor (`.agents/harness-anchor.md`)

Propose **Harness Anchor** using template [`references/harness-anchor.md`](./references/harness-anchor.md).
- **SSOT Discovery**: Scan for existing testing guides (`test/AGENTS.md`, `tests/AGENTS.md`, `docs/**/testing*.md`, `<subsystem>/test/AGENTS.md`). Record all discovered SSOT paths as relative paths under Governing Testing SSOTs without transcribing content, preventing stale copies and routing agents directly to authoritative sources.
- **Hermetic Primitives Discovery**: Scan test helper directories (`test/helpers/`, `test/fixtures/`) to register existing foundation helpers in the Hermetic Primitives Registry.

### 3. Environment Specification (`.agents/environment.md`)

Propose **Environment Specification** using template [`references/environment.md`](./references/environment.md). Populate or replace the `## 1. Toolchain & Environment` section via [`scripts/discover-toolchain.sh`](./scripts/discover-toolchain.sh) (`--file` defaults to `.agents/environment.md`), recording active runtime wrappers, canonical test/analysis commands, and installed host CLIs. Non-applicable sections (services, datastores) remain omissible.

### 4. Git Privacy Configuration (`.gitignore`)

- `.agents/scratch/`: Private scratchpad (immutable).
- `.agents/tasks/`: Local-Only default for local markdown; omit if user requests team-shared tracking.

### 5. Git Core Safety Configuration (`.git/config`)

Apply repository safety defaults:
```bash
git config --local merge.conflictstyle zdiff3
git config --local diff.algorithm histogram
git config --local push.useForceIfIncludes true
git config --local rebase.autoStash true
```

### 6. Documentation Placement Matrix (`docs/README.md`)

```markdown
# Documentation Index & Placement Matrix

| Topic / Scope | Authoritative SSOT | Responsibility |
| :--- | :--- | :--- |
| **Tasks & Execution** | Defined in `.agents/task-tracker.md` | Decomposed task units and progress tracking |
| **Testing Governance** | Defined in `.agents/harness-anchor.md` | Test harness infrastructure and invariant testing |
| **Documentation Governance** | `docs/` | Governed via `/ssot` |
```

### 7. Agent Constitution Hook (`AGENTS.md` or `CLAUDE.md`)

Target `CLAUDE.md` if present; otherwise target `AGENTS.md` (create if absent). If target file exists, append this block; do not overwrite:

```markdown
## Agent Workflow
- **Environment**: Governed by `.agents/environment.md` (local runners, zero-touch for `.env*` secrets).
- **Task Tracker**: Governed by `.agents/task-tracker.md`.
- **Harness Anchor**: Governed by `.agents/harness-anchor.md` (via `/harness-audit`).
- **Documentation**: Governed by `docs/README.md` (via `/ssot`).
```

### Routing

- The caller requests design deliberation after setup → (via /clarify).
- The caller requests harness health inspection → (via /harness-audit).
- The caller requests documentation authority review → (via /ssot).

## Execution Protocol

### Phase 1: Read-Only Discovery

1. **Remote & Topology**: Run `git remote -v` to resolve host and repository path (`owner/repo`).
2. **Toolchain Pre-flight**: Run `bash scripts/discover-toolchain.sh <path_to_repository> --dry-run` to inspect tracker CLI auth (`gh` / `glab`), inferred runtime wrappers, test/analysis commands, and installed host tools without mutating disk.
3. **Workspace Signals**:
   - Check `AGENTS.md` vs `CLAUDE.md` (preserve existing, forbid duplicating).
   - Check `.gitignore`, `.agents/environment.md`, `.agents/task-tracker.md`, `.agents/harness-anchor.md`, `.agents/tasks/`.
   - Scan existing documentation (`docs/README.md` or `README.md`).
4. **Clean-Pass Short-Circuit**: If all scaffolding assets (`.agents/environment.md`, `.agents/task-tracker.md`, `.agents/harness-anchor.md`, `.gitignore` privacy rules, `docs/README.md`, and constitution hook) are already configured and valid, report:

   ```text
   Repository ecosystem is already initialized and up-to-date.
   ```

   Halt turn immediately without staging redundant mutations.

### Phase 2: Staging & Authorization Gate

1. Stage missing or unconfigured scaffolding assets in Changeset format:

   ```text
   # Changeset: Repository Initialization

   |-- .agents/
   |   |-- environment.md
   |   |   `-- [CREATE] Record environment toolchains, runners, and service contracts.
   |   |-- task-tracker.md
   |   |   `-- [CREATE] Configure task tracking mode and execution protocols.
   |   `-- harness-anchor.md
   |       `-- [CREATE] Establish test SSOT routing and hermetic primitives registry.
   |-- docs/README.md
   |   `-- [<ACTION>] Establish documentation Placement Matrix.
   |-- .gitignore
   |   `-- [<ACTION>] Add .agents/scratch/ and .agents/tasks/ privacy rules.
   `-- <AGENTS.md | CLAUDE.md>
       `-- [<ACTION>] Add agent workflow, secret privacy rules, and documentation pointers.

   Summary: <N> files affected (<C> created, <U> updated).
   ```

2. Present Changeset summary, recommended tracker choice, and toolchain status (report auth status if CLI is unauthenticated); keep raw file bodies out of chat.
3. Halt turn immediately for human authorization.

### Phase 3: Atomic Application & Handoff

1. Upon receiving approval, write staged files to disk, apply Git core safety configurations, and run `bash scripts/discover-toolchain.sh <path_to_repository> [--file <path.md>]` to create or update `.agents/environment.md`.
2. Report setup complete and any caller-relevant follow-up gaps.
