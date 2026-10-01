---
name: github-flow
description: Automate the end-to-end GitHub issue lifecycle starting work, quality checks, opening PRs with GraphQL issue linking, squash-merging, project board status synchronization, and post-merge deployment webhooks. Use for standardized issue pickup, PR linking, and deployment flows across projects. Triggers on flow.sh, issue flow, start issue, ship PR, link PR, deploy hook, and GitHub lifecycle workflow requests.
metadata:
  type: workflow
  version: "1.0"
  stack: git+gh
---

# GitHub Flow

Automate the full GitHub issue-to-production lifecycle through a unified CLI script (`scripts/flow.sh`) and standardized GitHub CLI/GraphQL patterns.

This skill connects three separate GitHub systems into a single seamless loop:

1. **Repository Git & PRs** (`git` + `gh pr`)
2. **Issue Tracking & Project Boards** (`gh project` + GitHub Projects v2)
3. **Continuous Deployment** (Cloudflare, Vercel, Netlify, or custom webhooks)

---

## Workflow Lifecycle

```mermaid
flowchart LR
    A[0. next] --> B[1. start <issue>]
    B --> C[2. check]
    C --> D[3. pr <issue>]
    D --> E[4. ship <pr>]
```

| Step         | Command                                          | What It Does                                                                                                                     |
| ------------ | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| **0. Next**  | `./scripts/flow.sh next [--start]`               | Lists open backlog issues, displays next candidate in queue, and optionally starts work.                                         |
| **1. Start** | `./scripts/flow.sh start <issue_no> [slug]`      | Syncs default branch, sets Project board status to **In Progress**, and creates `feature/<slug>` branch.                         |
| **2. Check** | `./scripts/flow.sh check`                        | Runs project verification gates (typecheck, tests, build) and shows git status.                                                  |
| **3. PR**    | `./scripts/flow.sh pr <issue_no> [title] [body]` | Commits changes, pushes branch, opens PR, and links PR to issue via GraphQL.                                                     |
| **Link**     | `./scripts/flow.sh link <issue_no> <pr_no>`      | Standalone command to link any PR to an issue via GraphQL.                                                                       |
| **4. Ship**  | `./scripts/flow.sh ship [pr_no]`                 | Squash-merges PR, deletes remote branch, syncs local default branch, marks board item **Done**, and triggers deployment webhook. |
| **Deploy**   | `./scripts/flow.sh deploy`                       | Standalone trigger for the deployment webhook (`POST`).                                                                          |
| **Status**   | `./scripts/flow.sh status`                       | Displays active branch, associated PR, and project board link.                                                                   |

---

## Step Chaining & Agent Response Rules (MANDATORY)

To guarantee high engineering velocity and maintain clear conversational context, **every step in the `github-flow` lifecycle deterministically points to the next command**.

### Transition Rules

| Step Completed            | State / Context                                  | Next Command to Run / Recommend     |
| :------------------------ | :----------------------------------------------- | :---------------------------------- |
| **0. `next`**             | Backlog issue reviewed/selected                  | `pnpm flow start <issue_no> [slug]` |
| **1. `start <issue_no>`** | Feature branch created, code changes ready       | `pnpm flow check`                   |
| **2. `check`**            | Quality gates passed (typecheck, tests, build)   | `pnpm flow pr <issue_no> "[title]"` |
| **3. `pr <issue_no>`**    | PR created and linked to issue                   | `pnpm flow ship [pr_no]`            |
| **4. `ship [pr_no]`**     | PR merged, branch deleted, default branch synced | `pnpm flow next [--start]`          |

### AI Agent Reporting Requirement

Whenever an AI agent completes a step or presents a status summary (e.g. after running `flow check` or `flow start`), **it MUST always append the next command to execute immediately below its summary report**:

````markdown
### Sonraki Adım / Next Step

```bash
pnpm flow <next_command>
```
````

Agents must never end a status report without this explicit next step block.

---

## Branch Divergence & Squash-Merge Protection

To prevent `main` and `origin/main` history divergence when working with squash merges or unpushed commits:

1. **Pre-Start Unpushed Commits Gate (`flow.sh start`)**:
   - Automatically inspects the local default branch before creating feature branches.
   - If local `main` has unpushed commits ahead of `origin/main`, the command aborts with an error, preventing work from starting on a dirty/diverged base.
2. **Post-Merge Clean Resync (`flow.sh ship`)**:
   - If fast-forwarding the local default branch fails (e.g. commit hashes diverged due to squash-merge replacement on GitHub), `flow.sh ship` automatically verifies the working tree is clean and safely resyncs local `main` to `origin/main` via `git reset --hard`.
3. **Zero Direct Commits on `main`**:
   - All code edits, fixes, refactorings, and chore tasks must be completed inside dedicated branches created by `pnpm flow start <issue_no>`.

---

## Configuration (`.flowrc`)

`github-flow` works zero-config on standard repos, but can be tailored per repository using a `.flowrc` file in the repository root.

```bash
# .flowrc

# GitHub Projects v2 Integration (Optional)
PROJECT_NUM="5"
PROJECT_OWNER="cemcakirlar"
STATUS_FIELD_NAME="Status"
STATUS_IN_PROGRESS_NAME="In Progress"
STATUS_DONE_NAME="Done"

# Quality Verification Gate (Optional)
# If omitted, flow.sh auto-detects from package.json, Makefile, or Cargo.toml
CHECK_CMD="pnpm -r --parallel run typecheck && pnpm build"

# Deployment Webhook (Optional)
# Triggered via POST on `ship` and `deploy`
if [[ -n "${REPO_ROOT:-}" && -f "$REPO_ROOT/.secrets" ]]; then
  source "$REPO_ROOT/.secrets"
fi
DEPLOY_HOOK_URL="${DEPLOY_HOOK_URL:-https://api.cloudflare.com/client/v4/workers/builds/deploy_hooks/YOUR_DEPLOY_HOOK_UUID}"

# Branching Conventions (Optional)
DEFAULT_BRANCH="main"
BRANCH_PREFIX="feature/"
```

See `references/flowrc.example` for a complete template.

---

## Adopting in a New Repository

1. **Install or vendor the skill**: Ensure `github-flow` exists in your `.agents/skills/` directory.
2. **Add an alias (optional but recommended)**:
   In `package.json`:
   ```json
   "scripts": {
     "flow": "bash .agents/skills/github-flow/scripts/flow.sh"
   }
   ```
   Or execute directly: `bash .agents/skills/github-flow/scripts/flow.sh <command>`.
3. **Configure (optional)**: Create `.flowrc` if using GitHub Projects v2 boards or deploy hooks.
4. **Document in `AGENTS.md`**:

   ```markdown
   ## Issue workflow

   Use `pnpm flow` (`.agents/skills/github-flow/scripts/flow.sh`) for issue lifecycle:

   - `pnpm flow start <issue_no>`
   - `pnpm flow check`
   - `pnpm flow pr <issue_no> [title]`
   - `pnpm flow ship [pr_no]`
   ```
