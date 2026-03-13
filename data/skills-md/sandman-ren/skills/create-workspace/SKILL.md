---
name: create-workspace
description: >
  Create and manage multi-repo development workspaces for complex tasks involving
  multiple repositories, dependencies, and parallel agent work. Also manages modular
  agent permissions — add/remove/preview permission modules for GitHub, Docker, Node.js,
  Python, Rust, Go, Playwright, and more. Use when the user wants to set up a workspace,
  add repos/worktrees/deps to an existing workspace, manage workspace permissions,
  or initialize a project that spans multiple repositories. Triggers on requests like
  "create a workspace", "set up a multi-repo project", "add a repo to the workspace",
  "create a worktree", "add github permissions", or "set up workspace permissions".
---

# Create Workspace

A skill for scaffolding structured, multi-repo development workspaces optimized for
parallel work by multiple agents and human developers.

## Workspace Structure

```
{workspace-name}/
├── workspace.yaml              # manifest: repos, worktrees, deps, metadata
├── CLAUDE.md                   # project-wide agent context and conventions
├── .gitignore                  # ignores sketch/ directory
├── .claude/
│   └── settings.json           # permissions for coding agents
├── repositories/
│   └── {repoName}/
│       ├── main/               # regular clone at default branch (worktree parent)
│       └── worktrees/
│           └── {worktreeName}/ # git worktree checkouts
├── docs/                       # cross-repo design docs, ADRs, specs
├── deps/
│   └── {depName}/              # full clones of dependency repos
├── tasks/                      # task assignments and coordination
└── sketch/                     # .gitignored agent scratch space
```

## Workflows

### 1. Create a New Workspace

When the user asks to create a workspace, follow these steps:

**Step 1: Gather information.** Ask the user for:
- Workspace name (will be the root directory name)
- A short description of the project/task
- Where to create the workspace. Offer the current working directory as the default option, and let the user specify a different path. The workspace will be created as a subdirectory at the chosen location (i.e., `{chosen-path}/{workspace-name}/`).
- Repositories to include (and which worktrees/branches to create). Accept any of these formats:
  - HTTPS URL: `https://github.com/user/repo.git`
  - SSH URL: `git@github.com:user/repo.git`
  - GitHub shorthand: `user/repo` or `Username/repoName`
- Dependency repositories (if any), in the same formats above.

If the user provides a `workspace.yaml` file or its contents, parse it directly instead of asking.

**Resolving repository references:**

When the user provides a GitHub shorthand (`user/repo`) instead of a full URL:

1. **Try `gh` CLI first:** Run `gh repo view user/repo --json url -q .url` to get the HTTPS URL. This works if the user has `gh` installed and authenticated.
2. **Try GitHub MCP:** If `gh` CLI is not available, use the GitHub MCP `get_file_contents` or `search_repositories` tool to verify the repository exists and get its URL.
3. **Fallback — web search:** If neither `gh` CLI nor GitHub MCP is available, use web search to find the repository URL, then ask the user to confirm before cloning.

Once resolved, clone using the full URL. Store the resolved URL in `workspace.yaml`.

**Step 2: Create the directory structure.**

```bash
mkdir -p {path}/{workspace-name}/{repositories,docs,deps,tasks,sketch}
```

Where `{path}` is the location chosen in Step 1 (defaults to the current working directory).

**Step 3: Generate the workspace.yaml manifest.**

Use the template from `assets/workspace.yaml.template` as a reference. The manifest should
capture all repositories, their worktrees, and dependencies. Write it to `{workspace-name}/workspace.yaml`.

**Step 4: Resolve and clone repositories.**

First, resolve any GitHub shorthand references to full URLs (see "Resolving repository references" above).

Then, for each repository in the manifest:

```bash
# Clone the repository into the main/ directory
git clone {resolved-url} {workspace-root}/repositories/{repoName}/main

# For each worktree, create a branch and worktree
cd {workspace-root}/repositories/{repoName}/main
git worktree add ../worktrees/{worktreeName} -b {branchName}
```

If the branch already exists on the remote, use checkout instead of `-b`:

```bash
git worktree add ../worktrees/{worktreeName} {branchName}
```

**Important worktree notes:**
- The `main/` clone is the worktree parent. Agents should avoid switching branches in `main/`.
- Each worktree is an independent working directory with its own HEAD, index, and working tree.
- Multiple agents can work on different worktrees of the same repo simultaneously without conflicts.

**Step 5: Clone dependencies.**

For each dependency in the manifest:

```bash
# Full clone (not shallow — deps may contain bugs or ongoing work to analyze)
git clone {url} {workspace-name}/deps/{depName}

# If a specific ref is specified, check it out
cd {workspace-name}/deps/{depName}
git checkout {ref}
```

**Step 6: Generate the CLAUDE.md.**

Use the template from `assets/CLAUDE.md.template` as a starting point. Populate it with:
- The workspace description from the manifest
- The list of repositories with their purposes
- The list of worktrees and what each is for
- The list of dependencies
- Cross-repo relationships (ask the user if not obvious)

**Step 7: Create the .gitignore.**

Write a `.gitignore` at the workspace root:

```
sketch/
```

**Step 8: Set up agent permissions.**

Create `.claude/settings.json` at the workspace root using the modular permission system.
Permissions are built from composable modules in `assets/permissions/`.

```bash
mkdir -p {workspace-name}/.claude
```

**8a. Start with required modules.** Two modules are always included:
- `_base` — Read, Glob, Grep, WebSearch, git read-only, worktree management, general utilities.
- `_security` — Deny rules for destructive operations (`rm -rf`, `sudo`, force push, `git reset --hard`) and sensitive file access (`.env`, SSH keys, cloud credentials, PEM/key files).

Note: `.env.example` and `.env.template` files are intentionally **not** blocked — agents need to read these to understand the environment variable setup.

**8b. Auto-detect optional modules.** Scan the cloned repositories for files that indicate a tech stack.
Use the `detect` field in each module file to match. Modules with `"always_suggest": true` are
always included in the suggestion list regardless of detection signals. Modules with an empty
`detect` array and no `always_suggest` flag are not auto-detected (they must be manually selected).

| Module | Detection signals |
|--------|-------------------|
| `github` | `.git` directory (any git repo) |
| `context7` | _(always suggest — has `always_suggest: true` in module file)_ |
| `nodejs` | `package.json` |
| `python` | `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg`, `Pipfile` |
| `rust` | `Cargo.toml` |
| `go` | `go.mod` |
| `docker` | `Dockerfile`, `docker-compose.yaml`, `docker-compose.yml`, `compose.yaml`, `compose.yml` |
| `playwright` | `playwright.config.ts`, `playwright.config.js` |

**8c. Present the selection to the user.** Show which modules were auto-detected and let them adjust:

> I detected the following permission modules based on your repositories:
> - [x] `github` — GitHub MCP tools and gh CLI
> - [x] `nodejs` — npm/yarn/pnpm/bun build, test, lint, install
> - [ ] `python` — pytest, mypy, ruff, pip, poetry, uv
> - [ ] `rust` — cargo build, test, clippy, add
> - [ ] `go` — go test, build, vet, mod
> - [x] `docker` — Docker inspection, lifecycle, compose
> - [ ] `playwright` — browser automation and inspection
> - [x] `context7` — library documentation lookup
>
> Would you like to add, remove, or adjust any of these?

Wait for the user to confirm or adjust before proceeding.

**8d. Ask about custom permissions.** After module selection, ask:

> Would you like to add any custom permission rules? You can specify:
> - Tools or commands to **auto-allow** (e.g., `Bash(terraform plan *)`)
> - Tools or commands to **require confirmation** (e.g., `Bash(terraform apply *)`)
> - Tools or commands to **always block** (e.g., `Bash(terraform destroy *)`)
>
> Or skip this step if the modules above cover your needs.

If the user provides custom rules, validate the syntax (must follow Claude Code permission format: `Tool`, `Tool(specifier)`, or `Tool(glob*pattern)`) and add them to the appropriate tier.

**8e. Preview the merged permissions.** Before writing, show the user a summary of the final configuration:

> **Permission preview** (modules: `_base`, `_security`, `github`, `nodejs`, `docker`, `context7`):
>
> | Tier | Count | Examples |
> |------|-------|---------|
> | Allow | _N_ | `Read`, `Bash(git log *)`, `mcp__plugin_github_github__issue_read`, `Bash(npm run *)` |
> | Ask | _N_ | `Bash(git push *)`, `mcp__plugin_github_github__create_pull_request`, `Bash(npm install *)` |
> | Deny | _N_ | `Bash(rm -rf *)`, `Bash(git push --force *)`, `Read(./**/.env)` |

Replace `_N_` with the actual deduplicated counts computed from the merged module files.
>
> _Full JSON will be written to `.claude/settings.json`._
> Does this look good?

Wait for the user to confirm. If they want changes, loop back to 8c or 8d.

**8f. Write the settings file.** Merge all selected modules:
1. Read each selected module JSON from `assets/permissions/`.
2. Union all `allow` arrays, then all `ask` arrays, then all `deny` arrays.
3. Deduplicate each array (preserve insertion order).
4. If the user provided custom rules, append them to the appropriate arrays.
5. Write the merged result as `.claude/settings.json`:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [ ... ],
    "ask": [ ... ],
    "deny": [ ... ]
  }
}
```

**Important:** Record which modules were included by adding a top-level `_modules` key to the settings file. This key is ignored by Claude Code but allows the skill to know what's active for future additions/removals:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "_modules": ["_base", "_security", "github", "nodejs", "docker", "context7"],
  "permissions": { ... }
}
```

**Step 9: Confirm completion.** Summarize what was created:
- Number of repositories cloned
- Number of worktrees created
- Number of dependencies cloned
- Location of the workspace

### 2. Add a Repository to an Existing Workspace

When the user asks to add a repo to an existing workspace:

1. Read the existing `workspace.yaml`
2. Clone the repo into `repositories/{repoName}/main/`
3. Create any requested worktrees
4. Update `workspace.yaml` with the new repository entry
5. Update `CLAUDE.md` to include the new repository

### 3. Add a Worktree to an Existing Repository

When the user asks to add a worktree:

1. Read `workspace.yaml` to find the repository
2. Create the worktree:
   ```bash
   cd {workspace}/repositories/{repoName}/main
   git worktree add ../worktrees/{worktreeName} -b {branchName}
   ```
3. Update `workspace.yaml` with the new worktree entry

### 4. Add a Dependency

When the user asks to add a dependency:

1. Clone the dependency into `deps/{depName}/`
2. Optionally check out a specific ref
3. Update `workspace.yaml`
4. Update `CLAUDE.md`

### 5. Show Workspace Status

When the user asks about workspace status:

1. Read `workspace.yaml`
2. For each repository and worktree, run `git status` and `git log --oneline -3`
3. Report: current branches, uncommitted changes, recent commits

### 6. Remove a Worktree

When the user asks to remove a worktree:

1. Run `git worktree remove` from the main clone
2. Update `workspace.yaml`

### 7. Manage Workspace Permissions

A standalone workflow for adding, removing, previewing, or customizing permission modules
in an existing workspace. This operates on the `.claude/settings.json` file at the workspace root.

**Triggers:** "add permissions", "set up github permissions", "add docker permissions to workspace",
"show workspace permissions", "remove python permissions", "add custom permissions".

#### 7a. Add Permission Modules

When the user asks to add permissions (e.g., "add github and docker permissions"):

1. Read the existing `.claude/settings.json` at the workspace root.
2. Check the `_modules` array to see what's already active.
3. Read the requested module JSON files from `assets/permissions/`.
4. Show a **preview** of what will be added:

> **Adding modules: `github`, `docker`**
> Already active: `_base`, `_security`, `nodejs`
>
> New rules being added:
> | Tier | New rules | Examples |
> |------|-----------|---------|
> | Allow | +34 | `mcp__plugin_github_github__issue_read`, `Bash(docker ps *)` |
> | Ask | +37 | `mcp__plugin_github_github__create_pull_request`, `Bash(docker build *)` |
> | Deny | +3 | `Bash(docker system prune *)` |
>
> Proceed?

5. On confirmation, merge the new module rules into the existing arrays (deduplicate).
6. Update the `_modules` array.
7. Write back `.claude/settings.json`.

#### 7b. Remove Permission Modules

When the user asks to remove permissions (e.g., "remove docker permissions"):

1. Read `.claude/settings.json` and the `_modules` array.
2. Verify the module is active. If not, inform the user.
3. Cannot remove `_base` or `_security` — these are required. Warn the user if they try.
4. Show a **preview** of what will be removed:

> **Removing module: `docker`**
> Rules that will be removed: 11 allow, 10 ask, 3 deny
> Proceed?

5. On confirmation, read the module's JSON file to get its rule list.
6. For each rule in the module being removed, check all other active modules' JSON files
   (from the remaining `_modules` array). Only remove the rule from `settings.json` if
   no other active module also declares the same rule. This prevents breaking shared rules.
7. Update the `_modules` array (remove the module name).
8. Write back `.claude/settings.json`.

#### 7c. List Active Permissions

When the user asks about current permissions (e.g., "show workspace permissions", "what permissions are set up"):

1. Read `.claude/settings.json`.
2. Display the active modules from `_modules` and a summary:

> **Active permission modules:**
> | Module | Description | Allow | Ask | Deny |
> |--------|-------------|-------|-----|------|
> | `_base` | Core tools, git read, utilities | _N_ | _N_ | 0 |
> | `_security` | Destructive ops, sensitive files | 0 | 0 | _N_ |
> | `github` | GitHub MCP + gh CLI | _N_ | _N_ | 0 |
> | `nodejs` | npm/yarn/pnpm/bun | _N_ | _N_ | 0 |
> | **Custom** | User-defined rules | _N_ | _N_ | _N_ |
> | **Total** | _(deduplicated)_ | **_N_** | **_N_** | **_N_** |
>
> Compute counts from the actual module JSON files. Do not hardcode counts.

3. If the user asks for details on a specific tier or module, show the actual rules.

#### 7d. Add Custom Permissions

When the user asks to add custom permissions (e.g., "allow terraform plan", "block kubectl delete"):

1. Read the existing `.claude/settings.json`.
2. Ask the user what rules they want. Accept natural language and translate to permission syntax:
   - "allow terraform plan" → `Bash(terraform plan *)` in `allow`
   - "ask before terraform apply" → `Bash(terraform apply *)` in `ask`
   - "block kubectl delete" → `Bash(kubectl delete *)` in `deny`
   - "allow the Jira MCP read tools" → `mcp__jira__get_*` etc. in `allow`
3. Show a **preview** with the translated rules:

> **Custom rules to add:**
> | Tier | Rule |
> |------|------|
> | Allow | `Bash(terraform plan *)` |
> | Allow | `Bash(terraform show *)` |
> | Ask | `Bash(terraform apply *)` |
> | Deny | `Bash(terraform destroy *)` |
>
> Does this look right?

4. On confirmation, add to the appropriate arrays in `.claude/settings.json`.
5. Custom rules are tracked separately — they are NOT associated with any module, so removing a module won't affect them.

#### 7e. Preview Current Settings File

When the user asks to preview the full settings (e.g., "show me the full permissions JSON"):

1. Read `.claude/settings.json`.
2. Display the full JSON contents.
3. Optionally offer to open it in the user's editor.

## Conventions

- **Never modify the `main/` clone's branch** — it anchors all worktrees. Document this in CLAUDE.md.
- **Worktree names should match branch names** when possible for clarity. If the branch has slashes (e.g., `feature/auth`), use a slugified name for the worktree directory (e.g., `feature-auth`).
- **The `sketch/` directory is ephemeral** — agents can write anything there. It is always gitignored.
- **The `tasks/` directory** is for coordination between agents and humans. Files here describe work items, assignments, and status.
- **The `docs/` directory** is for durable design documentation that outlives any single task.
- **Permissions are always project-scoped.** All permission configuration goes in the workspace's
  `.claude/settings.json` (project-level), never in `~/.claude/settings.json` (user-level).
  Project-level settings are portable, version-controllable, and scoped to the workspace — they
  don't leak into the user's other projects. If the user asks to set permissions globally, explain
  the trade-offs (affects all projects, not shareable with collaborators) and confirm before
  proceeding. If they still want global changes, direct them to edit `~/.claude/settings.json`
  manually rather than doing it for them.

## Error Handling

- If a `git clone` fails, report the error and continue with remaining repos. Mark failed repos in the output.
- If a worktree branch already exists locally, use `git worktree add ../worktrees/{name} {branch}` without `-b`.
- If a worktree directory already exists, warn the user and skip unless they confirm overwriting.
- If `workspace.yaml` already exists when creating a new workspace, ask before overwriting.
